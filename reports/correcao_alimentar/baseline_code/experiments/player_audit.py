"""Auditoria de 10 mil ações públicas; leitura global somente para diagnóstico.

O controlador consulta status, inventário, mercado, quests e lugares do próprio
personagem. A auditoria lê o mundo para medir consequências, sem guiar ações.
Não muda regras, atributos, posições, estoque ou RNG diretamente.
"""

import argparse
from collections import Counter, deque
from dataclasses import asdict
import hashlib
import json
from pathlib import Path
import time

from procedural.engine import Engine
from procedural.generation import generate_world
from procedural.models import Location
from procedural.persistence import JsonRepository, dumps
from procedural.validation import validate_world


def money(world):
    return (sum(c.money for c in world.characters.values()) +
            sum(t.money + t.abstract_money for t in world.towns.values()) +
            sum(k.treasury for k in world.kingdoms.values()))


def run(seed, turns, directory, observer=None):
    directory.mkdir(parents=True, exist_ok=True)
    started = time.monotonic()
    engine = Engine(generate_world(seed, "Auditor"))
    world, player = engine.world, engine.player
    start = world.turn
    initial_money = money(world)
    initial_source = world.metrics.get("MoneySourceAbstractWork", 0)
    actions, attempts, failures = Counter(), Counter(), Counter()
    checkpoints, reactions, deaths, observations, examples = [], [], [], [], []
    contacts, last_talk, visited = {}, {}, {}
    pending_gift, route, route_town = None, deque(), None
    last_trip, last_tour, last_sale, last_work = -1000, -1000, -1000, -1000
    last_buy, last_ask = -1000, {}
    response_count = 0
    current_command, before_command_turn = "", world.turn
    context = {}
    health_min, fatigue_peak = player.health, player.fatigue
    money_max = player.money
    starvation_healing = 0
    invalid_mutations = []
    ledger_max = 0
    if observer:
        observer(engine)

    def snapshot_player():
        return {"money": player.money, "inventory": dict(player.inventory),
                "health": player.health, "hunger": player.hunger, "thirst": player.thirst,
                "fatigue": player.fatigue, "position": asdict(player.position),
                "needs": {k: asdict(n) for k, n in player.needs.items()}, "next_id": world.next_id}

    def capture(event):
        if event.kind == "CharacterDied":
            victim = world.characters[event.target_id]
            deaths.append({"turn": event.turn, "id": victim.id, "name": victim.name,
                           "category": victim.category, "profession": victim.profession,
                           "hunger": victim.hunger, "thirst": victim.thirst,
                           "food_carried": engine.items.count(victim.id, "food"),
                           "water_carried": engine.items.count(victim.id, "water"),
                           "last_goal": asdict(victim.goal) if victim.goal else None})
        if event.target_id == player.id or event.actor_id == player.id:
            record = {"turn": event.turn, "id": event.id, "kind": event.kind,
                      "description": event.description, "actor_id": event.actor_id,
                      "target_id": event.target_id, "context": event.context,
                      "command": current_command, "command_turn_before": before_command_turn}
            reactions.append(record)
            if event.kind == "HelpRequested":
                # A mensagem é recebida pelo jogador; associação a ID fica só no relatório.
                owner = world.characters[event.actor_id]
                record["owner_money"] = owner.money
        if event.kind in ("HelpGiven", "QuestCompleted") and event.actor_id == player.id:
            target = world.characters[event.target_id]
            context["delivery_events"].append({"kind": event.kind, "target_alive": target.alive,
                                               "target_hunger": target.hunger,
                                               "target_health": target.health})

    engine.bus.subscribe("*", capture)
    stream = (directory / "acoes.jsonl").open("w", encoding="utf-8")

    def command(text):
        nonlocal current_command, before_command_turn, health_min, fatigue_peak, money_max, starvation_healing
        current_command, before_command_turn = text, world.turn
        context["delivery_events"] = []
        before = snapshot_player()
        old_quests = {q.id: q.status for q in world.quests.values()}
        old_facts = set(player.knowledge)
        result = engine.execute(text)
        if observer:
            observer(engine)
        after = snapshot_player()
        advanced = world.turn - before_command_turn
        attempts[text.split()[0]] += 1
        if advanced:
            actions[text.split()[0]] += advanced
        if not result.success:
            failures[result.message] += 1
            if before != after:
                invalid_mutations.append({"turn": world.turn, "command": text,
                                          "message": result.message, "before": before, "after": after})
        if text == "descansar" and max(before["hunger"], before["thirst"]) >= 100 and player.health > before["health"]:
            starvation_healing += 1
        if text.startswith("entregar") and result.success:
            target = world.characters[int(text.split()[1])]
            if result.success and not target.alive:
                observations.append({"kind": "recipient_died_on_delivery", "turn": world.turn,
                                     "npc_id": target.id, "name": target.name,
                                     "events": context["delivery_events"]})
        health_min = min(health_min, player.health)
        fatigue_peak, money_max = max(fatigue_peak, player.fatigue), max(money_max, player.money)
        record = {"elapsed": world.turn - start, "turn_before": before_command_turn, "turn_after": world.turn,
                  "command": text, "success": result.success, "message": result.message,
                  "state": {k: after[k] for k in ("money", "health", "hunger", "thirst", "fatigue", "position")},
                  "quest_changes": {qid: q.status for qid, q in world.quests.items() if old_quests.get(qid) != q.status},
                  "new_known_facts": sorted(set(player.knowledge) - old_facts)}
        stream.write(json.dumps(record, ensure_ascii=False) + "\n")
        if result.success and text.split()[0] in ("comprar", "vender", "pedir", "trabalhar", "aceitar", "recusar", "entregar", "sair", "entrar") and len(examples) < 150:
            examples.append(record)
        elapsed = world.turn - start
        if advanced and (elapsed % 1000 == 0 or not player.alive):
            checkpoint(elapsed)
        return result

    def checkpoint(elapsed):
        nonlocal ledger_max
        errors = validate_world(world)
        expected_money = initial_money + world.metrics.get("MoneySourceAbstractWork", 0) - initial_source
        deficit = money(world) - expected_money
        empty_towns = [t.id for t in world.towns.values() if not any(
            world.characters[i].alive and world.characters[i].position.map_id == t.id for i in t.resident_ids)]
        ledger_max = max(ledger_max, sum(len(c.applied_facts) for c in world.characters.values()))
        record = {"elapsed": elapsed, "health": player.health, "hunger": player.hunger,
                  "thirst": player.thirst, "fatigue": player.fatigue, "money": player.money,
                  "alive_npcs": sum(c.alive and not c.is_player for c in world.characters.values()),
                  "dead_local_town_ids": empty_towns, "money_balance_difference": deficit,
                  "food_markets_empty": sum(engine.items.count(t.id, "food") == 0 for t in world.towns.values()),
                  "kingdoms_without_ruler": sum(k.ruler_id is None for k in world.kingdoms.values()),
                  "quests": dict(Counter(q.status for q in world.quests.values())),
                  "validation_errors": errors, "total_fact_ledger": ledger_max}
        checkpoints.append(record)
        print(json.dumps(record, ensure_ascii=False), flush=True)
        if errors or deficit:
            raise AssertionError(f"Falha de auditoria: {errors}; balanço {deficit}")
        if elapsed in (1000, 5000):
            JsonRepository().save(world, directory / f"save_{elapsed}.json")

    def walk_to(point):
        # Interior gerado tem corredores livres; usa coordenadas conhecidas e
        # confirma cada passo através da própria ação, sem consultar matriz oculta.
        p = player.position
        if p.map_id != point.map_id:
            return False
        if p.y != point.y:
            direction = "sul" if p.y < point.y else "norte"
        elif p.x != point.x:
            direction = "leste" if p.x < point.x else "oeste"
        else:
            return False
        return command(direction).success

    try:
        # Ações inválidas exercitadas antes de qualquer necessidade do jogador.
        for text in ("coletar", "trabalhar", "mover diagonal", "esperar 0", "comprar comida -1",
                     "vender 999999999", "entregar 999999999 1", "pedir comida 999999999"):
            command(text)
        command("entrar")
        gate = player.position
        origin = world.maps[gate.map_id].exit_to  # posição externa já percorrida pelo jogador
        seen_places = {}
        while player.alive and world.turn - start < turns:
            if sum(attempts.values()) > turns * 8:
                raise RuntimeError("Controlador preso em ações inválidas")
            elapsed = world.turn - start
            view = engine.execute("status").data
            inventory = engine.execute("inventario").data
            food = next((i for i in inventory if i["kind"] == "food"), None)
            water = next((i for i in inventory if i["kind"] == "water"), None)
            food_qty, water_qty = (food["quantity"] if food else 0), (water["quantity"] if water else 0)
            visited[player.position.map_id] = view["map_name"]
            present = view["npcs"]
            for npc in present:
                contacts[npc["id"]] = npc["name"]
            if player.hunger >= 55 and food:
                command("comer")
                continue
            if player.thirst >= 50:
                if command("beber").success:
                    continue
            # Observa pontos externos exclusivamente pelo mapa 5x5 retornado.
            if player.position.map_id == world.world_map_id:
                px, py = view["position"]
                for iy, row in enumerate(view["map"]):
                    for ix, symbol in enumerate(row):
                        if symbol in ("C", "V"):
                            point = Location(player.position.map_id, px + ix - 2, py + iy - 2)
                            if point != origin:
                                seen_places[(point.x, point.y)] = point
                if seen_places and elapsed - last_trip < 100:
                    point = min(seen_places.values(), key=lambda p: abs(p.x - px) + abs(p.y - py))
                    if player.position == point:
                        command("entrar")
                        gate = player.position
                        origin = point
                        seen_places.clear()
                        route.clear()
                        route_town = player.town_id
                        continue
                    if walk_to(point):
                        continue
                if route:
                    if not command(route.popleft()).success:
                        route.clear()
                    continue
                if player.position == origin:
                    command("entrar")
                    gate = player.position
                    continue
                if walk_to(origin):
                    continue
                command("esperar 1")
                continue
            # Água e descanso não exigem consultar o estoque oculto do município.
            if player.fatigue >= 65 or player.health < 85 and max(player.hunger, player.thirst) < 60:
                command("descansar")
                continue
            places = player.known_places
            rural, market = places["forage"], places["market"]
            need_supply = food_qty < 8
            if need_supply:
                if player.position != rural:
                    if walk_to(rural):
                        continue
                if command("coletar").success or command("trabalhar").success:
                    continue
                # Reserva esgotada: mercado e pedidos ainda são alternativas.
                if player.position != market and player.hunger < 85:
                    if walk_to(market):
                        continue
                if player.position == market:
                    if command("comprar comida").success:
                        continue
                if present:
                    if command(f"pedir comida {present[0]['id']}").success:
                        continue
                command("esperar 1")
                continue
            quests = engine.execute("quests").data
            offered = next((q for q in quests if q["status"] == "offered" and
                            q.get("owner_id") in {n["id"] for n in present}), None)
            if offered:
                response_count += 1
                answer = "recusar" if response_count % 3 == 0 else "aceitar"
                command(f"{answer} {offered['id']}")
                continue
            # Contratos pessoais usam somente fatos, pessoas vistas e dados públicos.
            accepted_personal = next((q for q in quests if q["status"] == "accepted" and q.get("kind", "food") != "food"), None)
            if accepted_personal:
                q = accepted_personal
                present_ids = {n["id"] for n in present}
                observable_ids = present_ids | {b["id"] for b in view.get("bodies", [])}
                if q["kind"] in ("companionship", "protection") and q["owner_id"] in present_ids:
                    if command(f"acompanhar {q['owner_id']}").success:
                        continue
                elif q["kind"] == "family_care" and q["target_id"] in present_ids:
                    item = water if q["context"].get("resource") == "water" else food
                    if item and command(f"entregar {q['target_id']} {item['id']}").success:
                        continue
                elif q["kind"] in ("family", "information"):
                    facts = engine.execute("fatos").data
                    known = next((f for f in reversed(facts) if f["kind"] in ("PersonLocated", "CharacterDied", "CharacterKilled", "RemainsLocated") and
                                  f["target_id"] == q["target_id"] and (f["kind"] != "PersonLocated" or f["turn"] >= q["created_at"])), None)
                    if known and q["owner_id"] in present_ids:
                        if command(f"informar {q['owner_id']} {known['id']}").success:
                            continue
                    if not known and q["target_id"] in observable_ids:
                        if command(f"investigar {q['target_id']}").success:
                            continue
            accepted = next((q for q in quests if q["status"] == "accepted" and any(
                q["title"].endswith(n["name"]) for n in present) and q.get("kind", "food") == "food"), None)
            if accepted and food_qty > 8:
                npc = next(n for n in present if accepted["title"].endswith(n["name"]))
                command(f"entregar {npc['id']} {food['id']}")
                continue
            if pending_gift:
                npc_id, kind = pending_gift
                pending_gift = None
                item = food if kind == "food" else water
                if item and any(n["id"] == npc_id for n in present):
                    command(f"entregar {npc_id} {item['id']}")
                    continue
            # Mantém intervalos entre interações; observa consequências materiais.
            npc = next((n for n in present if elapsed - last_talk.get(n["id"], -1000) >= 72), None)
            if npc:
                result = command(f"conversar {npc['id']}")
                last_talk[npc["id"]] = elapsed
                if "Estou com fome" in result.message and food_qty >= 10:
                    pending_gift = (npc["id"], "food")
                elif water_qty >= 10 and elapsed % 2 == 0:
                    pending_gift = (npc["id"], "water")
                continue
            if present and elapsed - last_ask.get(present[0]["id"], -1000) >= 360:
                last_ask[present[0]["id"]] = elapsed
                command(f"pedir comida {present[0]['id']}")
                continue
            if route and route_town == player.town_id:
                next_command = route.popleft()
                if not command(next_command).success:
                    route.clear()
                continue
            if player.position == market:
                catalogue = {i["product"]: i for i in engine.execute("mercado").data}
                if food_qty > 12 and elapsed - last_sale >= 72:
                    last_sale = elapsed
                    command(f"vender {food['id']} {min(4, food_qty - 10)}")
                    continue
                offer = catalogue["agua"]
                if water_qty < 10 and offer["quantity"] >= 4 and player.money >= offer["price"] * 4:
                    if command("comprar agua 4").success:
                        continue
                if elapsed - last_buy >= 120 and player.money > 30 and catalogue["comida"]["quantity"]:
                    last_buy = elapsed
                    command("comprar comida 2")
                    continue
            if player.position == rural and elapsed - last_work >= 96:
                last_work = elapsed
                command("trabalhar")
                continue
            if elapsed - last_trip >= 900 and food_qty >= 12 and water_qty >= 6:
                if player.position != market:
                    if walk_to(market):
                        continue
                last_trip = elapsed
                gate = Location(player.position.map_id, market.x, market.y + 1)
                route = deque(["sul", "sair"] + ["norte"] * 8 + ["leste"] * 8 +
                              ["sul"] * 8 + ["oeste"] * 8 + ["entrar"])
                route_town = player.town_id
                continue
            if elapsed - last_tour >= 180:
                last_tour = elapsed
                # Explora casas, oficinas e praça; passos confirmados publicamente.
                destinations = [(2, 2), (2 * market.x - 2, 2), (market.x, 1), (rural.x, rural.y), (market.x, market.y)]
                px, py = player.position.x, player.position.y
                commands = []
                for x, y in destinations:
                    commands += ["sul" if y > py else "norte"] * abs(y - py)
                    commands += ["leste" if x > px else "oeste"] * abs(x - px)
                    px, py = x, y
                route, route_town = deque(commands), player.town_id
                continue
            if food_qty < 15:
                if player.position != rural:
                    if walk_to(rural):
                        continue
                if command("coletar").success:
                    continue
            command("esperar 1")
        if not checkpoints or checkpoints[-1]["elapsed"] != world.turn - start:
            checkpoint(world.turn - start)
        JsonRepository().save(world, directory / "save_final.json")
    finally:
        stream.close()

    report = {"seed": seed, "rules_version": world.rules_version, "start_turn": start,
              "requested_turns": turns, "actual_turns": world.turn - start, "player": snapshot_player(),
              "alive": player.alive, "minimum_health": health_min, "maximum_money": money_max,
              "maximum_fatigue": fatigue_peak, "actions": dict(actions), "attempts": dict(attempts),
              "failure_messages": dict(failures), "visited_maps": visited, "contacts": contacts,
              "quests": dict(Counter(q.status for q in world.quests.values())),
              "quest_details": [asdict(q) for q in world.quests.values()],
              "reactions": reactions, "deaths": deaths, "observations": observations,
              "invalid_action_mutations": invalid_mutations,
              "starvation_rest_healing": starvation_healing, "checkpoints": checkpoints,
              "towns": [{"id": t.id, "name": t.name, "population": t.population,
                         "food": engine.items.count(t.id, "food"), "grain": engine.items.count(t.id, "grain"),
                         "living_local_residents": sum(world.characters[i].alive and
                           world.characters[i].position.map_id == t.id for i in t.resident_ids),
                         "demand": t.demand} for t in world.towns.values()],
              "kingdoms": [{"id": k.id, "name": k.name, "ruler_id": k.ruler_id,
                            "political": k.political_state, "economic": k.economic_state}
                           for k in world.kingdoms.values()],
              "examples": examples, "world_metrics": world.metrics,
              "save_sha256": hashlib.sha256((directory / "save_final.json").read_bytes()).hexdigest(),
              "seconds": round(time.monotonic() - started, 2)}
    (directory / "relatorio.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({k: report[k] for k in ("actual_turns", "alive", "actions", "quests", "visited_maps", "seconds")}, ensure_ascii=False), flush=True)
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", default="Dovha")
    parser.add_argument("--turnos", type=int, default=10000)
    parser.add_argument("--output", type=Path, default=Path("reports/auditoria_jogador_10000"))
    args = parser.parse_args()
    run(args.seed, args.turnos, args.output)
