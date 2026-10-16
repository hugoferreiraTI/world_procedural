"""Campanha automatizada por comandos públicos, com registro de reações ao jogador.

Política: mercador local que conversa, ajuda e aceita/recusa pedidos. Decisões
usam estado do próprio jogador, NPCs presentes, respostas e catálogo do mercado.
Inspeção global serve apenas ao relatório. Não há teleporte nem alteração de
vida, dinheiro, necessidades, personalidade, estoques ou relacionamentos.
"""

import argparse
from collections import Counter
import json
from pathlib import Path
import time

from procedural.engine import Engine
from procedural.generation import generate_world
from procedural.persistence import JsonRepository
from procedural.validation import assert_valid


def run_campaign(seed: str, turns: int, directory: Path) -> dict:
    directory.mkdir(parents=True, exist_ok=True)
    world = generate_world(seed, "Codex", with_player=True)
    engine = Engine(world)
    player = engine.player
    start = world.turn
    started = time.monotonic()
    actions = Counter()
    attempts = Counter()
    actor_events, target_events = Counter(), Counter()
    contacts, gifts = Counter(), Counter()
    checkpoints, reactions, trades, limitations = [], [], [], []
    last_talk, last_gift, last_trade = {}, {}, {}
    queued_gift = None
    pending_trade = None
    request_number = 0
    maximum_money = player.money
    minimum_health = player.health
    starvation_rest_count = 0
    last_walk = start
    market_position = None

    def capture(event):
        if event.actor_id == player.id:
            actor_events[event.kind] += 1
        if event.target_id == player.id:
            target_events[event.kind] += 1
        if ((event.target_id == player.id and event.actor_id != player.id) or
                event.actor_id == player.id and event.kind in ("HelpGiven", "QuestCompleted")):
            reactions.append({"turn": event.turn, "event_id": event.id, "kind": event.kind,
                              "description": event.description, "actor_id": event.actor_id,
                              "target_id": event.target_id, "witnesses": event.witnesses})

    engine.bus.subscribe("*", capture)

    def inventory(kind):
        return next((item for item in engine.execute("inventario").data if item["kind"] == kind), None)

    def command(text):
        nonlocal maximum_money, minimum_health, starvation_rest_count
        before_turn, before_money, before_health = world.turn, player.money, player.health
        hungry, thirsty = player.hunger, player.thirst
        result = engine.execute(text)
        attempts[text.split()[0]] += 1
        advanced = world.turn - before_turn
        if advanced:
            actions[text.split()[0]] += advanced
        if text == "descansar" and (hungry >= 100 or thirsty >= 100) and player.health > before_health:
            starvation_rest_count += 1
        maximum_money = max(maximum_money, player.money)
        minimum_health = min(minimum_health, player.health)
        transcript.write(json.dumps({"turn_before": before_turn, "turn_after": world.turn,
                                     "command": text, "success": result.success,
                                     "message": result.message, "health": player.health,
                                     "hunger": round(player.hunger, 2), "thirst": round(player.thirst, 2),
                                     "money_before": before_money, "money_after": player.money},
                                    ensure_ascii=False) + "\n")
        return result

    def checkpoint():
        assert_valid(world)
        opinions = [npc.reputations[player.id] for npc in world.characters.values()
                    if player.id in npc.reputations]
        checkpoints.append({"elapsed": world.turn - start, "health": player.health,
                            "hunger": player.hunger, "thirst": player.thirst, "money": player.money,
                            "npcs_alive": sum(c.alive and not c.is_player for c in world.characters.values()),
                            "npcs_with_helpful_reputation": sum(r.tags.get("prestativo", 0) > 0 for r in opinions),
                            "quests": dict(Counter(q.status for q in world.quests.values()))})
        print(json.dumps(checkpoints[-1], ensure_ascii=False), flush=True)

    with (directory / "acoes.jsonl").open("w", encoding="utf-8") as transcript:
        for unsupported in ("roubar comida", "atacar 26"):
            result = command(unsupported)
            limitations.append({"command": unsupported, "message": result.message,
                                "advanced_turns": world.turn - start})
        command("entrar")
        command("norte")
        market_position = player.position
        last_checkpoint = 0
        while world.turn - start < turns and player.alive:
            elapsed = world.turn - start
            if elapsed // 1000 > last_checkpoint:
                checkpoint()
                last_checkpoint = elapsed // 1000
            if sum(attempts.values()) > turns * 10:
                raise RuntimeError("Política presa em ações inválidas; campanha interrompida.")
            # Sobrevivência usa exatamente as ações disponíveis no jogo.
            if player.health < 75:
                command("descansar")
                continue
            food = inventory("food")
            if player.hunger >= 55 and food:
                command("comer")
                continue
            if player.position != market_position:
                command("sul")
                continue
            if player.thirst >= 55:
                if command("beber").success:
                    continue
            if player.fatigue >= 70:
                command("descansar")
                continue
            nearby = engine.view()["npcs"]
            present = {npc["id"] for npc in nearby}
            catalogue = engine.execute("mercado").data or []
            products = {product["product"]: product for product in catalogue}

            if pending_trade:
                item = inventory(pending_trade["kind"])
                if item:
                    quantity = min(item["quantity"], pending_trade["quantity"])
                    while quantity > 0:
                        result = command(f"vender {item['id']} {quantity}")
                        if result.success:
                            trades.append({"product": pending_trade["product"],
                                           "turn": world.turn, "bought_quantity": pending_trade["quantity"],
                                           "sold_quantity": quantity,
                                           "money_before_purchase": pending_trade["money"],
                                           "money_after_sale": player.money})
                            break
                        quantity //= 2
                    pending_trade = None
                    if result.success:
                        continue
                pending_trade = None

            # Mantém mantimentos e oferece ajuda usando comida realmente comprada.
            supply = products.get("comida")
            food_quantity = food["quantity"] if food else 0
            if (food_quantity < 2 or player.hunger >= 40 and food_quantity < 5) and supply and supply["quantity"] and player.money >= supply["price"]:
                quantity = min(12, supply["quantity"], player.money // supply["price"])
                if command(f"comprar comida {quantity}").success:
                    continue

            quests = engine.execute("quests").data
            offered = next((q for q in quests if q["status"] == "offered"), None)
            if offered:
                request_number += 1
                answer = "recusar" if request_number % 3 == 0 else "aceitar"
                command(f"{answer} {offered['id']}")
                continue
            accepted = [q for q in world.quests.values() if q.status == "accepted"]
            # owner_id é parte do pedido recebido; não fornece posição oculta.
            owner = next((q.owner_id for q in accepted if q.owner_id in present), None)
            if food and food["quantity"] > 2 and owner is not None:
                if command(f"entregar {owner} {food['id']}").success:
                    gifts[owner] += 1
                    last_gift[owner] = world.turn
                    continue
            if queued_gift is not None:
                target, queued_gift = queued_gift, None
                if target in present and food and food["quantity"] > 3:
                    if command(f"entregar {target} {food['id']}").success:
                        gifts[target] += 1
                        last_gift[target] = world.turn
                        continue

            # Comércio em lotes: permite observar oportunidades ou falhas de preço.
            if player.money < 200:
                for label, kind in (("madeira", "wood"), ("trigo", "grain"), ("ferro", "iron")):
                    offer = products.get(label)
                    if not offer or world.turn - last_trade.get(kind, -100) < 24:
                        continue
                    quantity = min(offer["quantity"], player.money // offer["price"])
                    # Compra lotes grandes; lotes pequenos não sustentam este mercador.
                    if quantity < 5 or quantity < offer["quantity"] * .75:
                        continue
                    before_money = player.money
                    result = command(f"comprar {label} {quantity}")
                    last_trade[kind] = world.turn
                    if result.success:
                        pending_trade = {"product": label, "kind": kind, "quantity": quantity,
                                         "money": before_money}
                        break
                if pending_trade:
                    continue

            available = [npc for npc in nearby if world.turn - last_talk.get(npc["id"], -100) >= 12]
            if available:
                npc = min(available, key=lambda npc: (last_talk.get(npc["id"], -100), npc["id"]))
                result = command(f"conversar {npc['id']}")
                if result.success:
                    contacts[npc["id"]] += 1
                    last_talk[npc["id"]] = world.turn
                    if "Estou com fome" in result.message and world.turn - last_gift.get(npc["id"], -100) >= 48:
                        queued_gift = npc["id"]
                    continue
            if world.turn - last_walk >= 48:
                command("norte")
                last_walk = world.turn
                continue
            if player.hunger >= 100 and not food:
                # Registra, em vez de esconder, a cura por descanso em privação.
                command("descansar")
            else:
                command("esperar 1")
        checkpoint()

    opinions = []
    for npc in world.characters.values():
        reputation = npc.reputations.get(player.id)
        if reputation and reputation.tags:
            opinions.append({"id": npc.id, "name": npc.name, "alive": npc.alive,
                             "tags": reputation.tags, "admiration": reputation.admiration,
                             "fear": reputation.fear, "popularity": reputation.popularity,
                             "trust": engine.graph.value(npc.id, player.id, "confiança"),
                             "direct_contacts": contacts[npc.id], "gifts_received": gifts[npc.id]})
    report = {"seed": seed, "requested_turns": turns, "actual_player_turns": world.turn - start,
              "player": {"id": player.id, "name": player.name, "nickname": player.nickname,
                         "alive": player.alive, "health": player.health, "hunger": player.hunger,
                         "thirst": player.thirst, "money": player.money,
                         "maximum_money": maximum_money, "minimum_health": minimum_health},
              "location": engine.view()["map_name"], "actions": dict(actions),
              "attempts": dict(attempts), "player_as_actor_events": dict(actor_events),
              "player_as_target_events": dict(target_events),
              "npc_contacts": len(contacts), "gifts_given": sum(gifts.values()),
              "quest_statuses": dict(Counter(q.status for q in world.quests.values())),
              "quest_details": [{"id": q.id, "owner": world.characters[q.owner_id].name,
                                  "status": q.status, "created_at": q.created_at,
                                  "completed_at": q.completed_at} for q in world.quests.values()],
              "opinions": opinions, "reactions": reactions, "trades": trades,
              "starvation_healed_by_rest": starvation_rest_count,
              "limitations": limitations, "checkpoints": checkpoints,
              "world_metrics": world.metrics, "seconds": round(time.monotonic() - started, 2),
              "invariants": "valid"}
    (directory / "relatorio.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    JsonRepository().save(world, directory / "save_final.json")
    print(json.dumps({key: report[key] for key in ("actual_player_turns", "player", "actions",
                                                  "npc_contacts", "gifts_given", "quest_statuses",
                                                  "player_as_target_events", "starvation_healed_by_rest",
                                                  "seconds", "invariants")}, ensure_ascii=False, indent=2), flush=True)
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", default="Dovha")
    parser.add_argument("--turnos", type=int, default=10000)
    parser.add_argument("--output", type=Path, default=Path("reports/jogador_dovha_10000"))
    args = parser.parse_args()
    if args.turnos < 2:
        parser.error("Use pelo menos dois turnos.")
    run_campaign(args.seed, args.turnos, args.output)


if __name__ == "__main__":
    main()
