"""Jogador automatizado: apenas comandos públicos e conhecimento local."""

from collections import Counter
import json
from pathlib import Path
import time

from procedural.engine import Engine
from procedural.generation import generate_world
from procedural.validation import assert_valid


def run(turns=10000):
    started = time.monotonic()
    engine = Engine(generate_world("Dovha", "Codex"))
    world, player = engine.world, engine.player
    start = world.turn
    directory = Path("reports/hardening")
    directory.mkdir(parents=True, exist_ok=True)
    actions, reactions, contacts = Counter(), [], {}
    checkpoints = []
    rest_healing_in_starvation = 0
    queued_gift = None

    def capture(event):
        if event.target_id == player.id and event.actor_id != player.id:
            reactions.append({"turn": event.turn, "kind": event.kind, "description": event.description,
                              "origin": event.context.get("origin")})

    engine.bus.subscribe("*", capture)
    with (directory / "jogador_acoes.jsonl").open("w", encoding="utf-8") as stream:
        def command(text):
            nonlocal rest_healing_in_starvation
            before_turn, health = world.turn, player.health
            starving = max(player.hunger, player.thirst) >= 100
            result = engine.execute(text)
            if result.success and world.turn > before_turn:
                actions[text.split()[0]] += world.turn - before_turn
            if text == "descansar" and starving and player.health > health:
                rest_healing_in_starvation += 1
            stream.write(json.dumps({"command": text, "turn": world.turn, "success": result.success,
                                     "message": result.message, "health": player.health,
                                     "hunger": player.hunger, "thirst": player.thirst,
                                     "money": player.money}, ensure_ascii=False) + "\n")
            return result

        command("entrar")
        rural = player.known_places["forage"]  # Lugar aprendido ao entrar; estado do próprio personagem.
        attempts = 0
        while player.alive and world.turn - start < turns:
            attempts += 1
            if attempts > turns * 8:
                raise RuntimeError("Política presa em ações inválidas")
            view = engine.execute("status").data
            inventory = engine.execute("inventario").data
            food = next((i for i in inventory if i["kind"] == "food"), None)
            if player.hunger >= 55 and food:
                command("comer")
                continue
            if player.thirst >= 50:
                if command("beber").success:
                    continue
            if player.position != rural:
                x, y = view["position"]
                direction = ("norte" if y > rural.y else "sul" if y < rural.y else
                             "oeste" if x > rural.x else "leste")
                command(direction)
                continue
            if not food or food["quantity"] < 3:
                if command("coletar").success or command("trabalhar").success:
                    continue
            if player.fatigue >= 60 or player.health < 90 and max(player.hunger, player.thirst) <= 60:
                command("descansar")
                continue
            present = {n["id"] for n in view["npcs"]}
            quests = engine.execute("quests").data
            offered = next((q for q in quests if q["status"] == "offered"), None)
            if offered:
                response = "recusar" if sum(q["status"] == "accepted" for q in quests) % 3 == 2 else "aceitar"
                command(f"{response} {offered['id']}")
                continue
            if queued_gift is not None:
                target, queued_gift = queued_gift, None
                if target in present and food and food["quantity"] >= 3:
                    command(f"entregar {target} {food['id']}")
                    continue
            npc = next((n for n in view["npcs"] if world.turn - contacts.get(n["id"], -24) >= 24), None)
            if npc:
                result = command(f"conversar {npc['id']}")
                contacts[npc["id"]] = world.turn
                if "Estou com fome" in result.message:
                    queued_gift = npc["id"]
                continue
            command("esperar 1")
            if (world.turn - start) // 1000 > len(checkpoints):
                assert_valid(world)
                checkpoints.append({"elapsed": world.turn - start, "health": player.health,
                                    "hunger": player.hunger, "thirst": player.thirst,
                                    "alive": player.alive})
                print(json.dumps(checkpoints[-1], ensure_ascii=False), flush=True)
    assert_valid(world)
    report = {"requested_turns": turns, "actual_turns": world.turn - start,
              "rules_version": world.rules_version, "player_alive": player.alive,
              "health": player.health, "hunger": player.hunger, "thirst": player.thirst,
              "money": player.money, "actions": dict(actions), "reactions": reactions,
              "quests": dict(Counter(q.status for q in world.quests.values())),
              "contacts": len(contacts), "rest_healing_in_starvation": rest_healing_in_starvation,
              "checkpoints": checkpoints, "invariants": "valid",
              "seconds": round(time.monotonic() - started, 2)}
    (directory / "jogador.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False), flush=True)
    return report


if __name__ == "__main__":
    run()
