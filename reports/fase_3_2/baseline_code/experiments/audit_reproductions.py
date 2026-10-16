"""Reproduções isoladas de suspeitas; não corrigem nem alteram a campanha.

As fixtures configuram encontros, fome, recursos e relações em mundos descartáveis.
O resultado registra se o comportamento suspeito ocorre na versão examinada.
"""

from dataclasses import asdict, replace
import json
from pathlib import Path

from procedural.engine import Engine
from procedural.generation import GenerationConfig, generate_world
from procedural.models import Fact, Goal, Location, Personality


def fixture():
    engine = Engine(generate_world("Dovha", "Auditor", config=GenerationConfig(
        kingdom_count=1, historical_turns=0)))
    npc = next(c for c in engine.world.characters.values()
               if c.town_id == engine.player.town_id and c.profession == "agricultor")
    return engine, npc


def request_fixture():
    engine, npc = fixture()
    town = engine.world.towns[npc.town_id]
    engine.navigation.relocate(engine.player, town.market)
    engine.navigation.relocate(npc, town.market)
    engine.items.consume(npc.id, "food", engine.items.count(npc.id, "food"))
    npc.hunger, npc.money = 90, 0
    npc.personality = Personality(honesty=100, compassion=0, independence=0, persistence=100)
    engine.graph.set(npc.id, engine.player.id, "confiança", 60)
    return engine, npc, town


def run(directory):
    results = []

    engine, npc = fixture()
    before = {"turn": engine.world.turn, "next_id": engine.world.next_id,
              "needs": list(engine.player.needs)}
    response = engine.execute("coletar")
    after = {"turn": engine.world.turn, "next_id": engine.world.next_id,
             "needs": list(engine.player.needs)}
    results.append({"id": "B01", "title": "Ação inválida cria necessidade e consome ID",
                    "reproduced": not response.success and before != after,
                    "before": before, "after": after, "response": response.message})

    engine, npc = fixture()
    engine.player.hunger = npc.hunger = 100
    engine.player.health = npc.health = 1
    engine.player.thirst = npc.thirst = 0
    response = engine.execute("comer")
    results.append({"id": "B02", "title": "Ordem do turno favorece o jogador e mata NPC antes de comer",
                    "reproduced": response.success and engine.player.alive and not npc.alive,
                    "initial": {"both_health": 1, "both_hunger": 100, "both_have_food": True},
                    "after": {"player_alive": engine.player.alive, "player_health": engine.player.health,
                              "npc_alive": npc.alive, "npc_food_carried": engine.items.count(npc.id, "food")}})

    engine, npc, town = request_fixture()
    npc.hunger, npc.health = 100, 1
    quest = engine.quests.offer(npc, engine.player)
    engine.quests.respond(quest.id, True)
    response = engine.execute(f"entregar {npc.id} {engine.items.first(engine.player.id, 'food')}")
    results.append({"id": "B03", "title": "Quest de socorro concluída no turno da morte do beneficiário",
                    "reproduced": response.success and quest.status == "completed" and not npc.alive,
                    "after": {"quest_status": quest.status, "npc_alive": npc.alive,
                              "npc_food_carried": engine.items.count(npc.id, "food"),
                              "events": [{"kind": e.kind, "turn": e.turn} for e in engine.world.events
                                         if e.target_id == npc.id and e.kind in
                                         ("HelpGiven", "QuestCompleted", "CharacterDied")]}})

    engine, npc, town = request_fixture()
    npc.money = 10
    amount = engine.items.count(town.id, "food")
    engine.items.consume(town.id, "food", amount - 1)
    need = engine.needs.refresh(npc)[0]
    candidates = engine.goals.solutions(npc, need)
    candidate = next(c for c in candidates if c.action == "ask_help" and c.target_id == engine.player.id)
    goal = Goal(engine.world.allocate_id(), need.id, candidate.action, candidate.score,
                engine.world.turn, target_id=engine.player.id)
    success, message = engine.goals.execute(npc, goal, 1)
    results.append({"id": "B04", "title": "Dez moedas bloqueiam ajuda mesmo quando comida custa mais",
                    "reproduced": not success and engine.economy.price(town.id, "food") > npc.money,
                    "npc_money": npc.money, "food_price": engine.economy.price(town.id, "food"),
                    "candidates": [{"action": c.action, "target_id": c.target_id, "score": c.score} for c in candidates],
                    "response": message})

    engine, npc = fixture()
    # Só a fonte e o jogador ficam ao alcance. Quem conta viu; quem escuta já
    # recebeu antes um rumor fraco do mesmo fato.
    for c in engine.world.characters.values():
        c.knowledge.clear()
        if not c.is_player:
            engine.navigation.relocate(c, c.home)
    point = Location(npc.town_id, 4, 4)
    engine.navigation.relocate(npc, point)
    engine.navigation.relocate(engine.player, point)
    engine.graph.set(engine.player.id, npc.id, "confiança", 95)
    actor = next(c for c in engine.world.characters.values() if c.id not in (npc.id, engine.player.id))
    fact = Fact(engine.world.allocate_id(), "HelpGiven", actor.id, None, point,
                engine.world.turn, "Um vizinho ajudou uma pessoa faminta.")
    engine.knowledge.learn(npc, fact, True)
    engine.knowledge.learn(engine.player, replace(fact, confidence=30), False)
    before = engine.player.knowledge[fact.event_id].confidence
    engine.knowledge.gossip()
    after_gossip = engine.player.knowledge[fact.event_id].confidence
    engine.execute(f"conversar {npc.id}")
    after_dialogue = engine.player.knowledge[fact.event_id].confidence
    results.append({"id": "B05", "title": "Rumores não reforçam fatos que o destinatário já conhece",
                    "reproduced": before == after_gossip < after_dialogue,
                    "before": before, "after_gossip": after_gossip, "after_dialogue": after_dialogue,
                    "source_firsthand_confidence": 100, "receiver_trust_in_source": 95})

    engine, npc, town = request_fixture()
    quest = engine.quests.offer(npc, engine.player)
    engine.execute("sul")
    engine.execute("sair")
    before = engine.graph.value(npc.id, engine.player.id, "confiança")
    response = engine.execute(f"recusar {quest.id}")
    event = next(e for e in engine.world.events if e.kind == "PlayerRefusedRequest")
    results.append({"id": "B06", "title": "Recusa comunica-se instantaneamente entre mapas diferentes",
                    "reproduced": response.success and npc.position.map_id != engine.player.position.map_id
                    and event.id in npc.knowledge,
                    "player_map": engine.player.position.map_id, "npc_map": npc.position.map_id,
                    "event_location": asdict(event.location), "event_witnesses": event.witnesses,
                    "trust_before": before, "trust_after": engine.graph.value(npc.id, engine.player.id, "confiança")})

    # Comida e água adequadas, mas nenhum descanso. Mede limitação da fisiologia,
    # não a classifica automaticamente como bug: não há regra de exaustão no MVP.
    engine, npc = fixture()
    engine.execute("entrar")
    rural = engine.player.known_places["forage"]
    while engine.player.position != rural:
        p = engine.player.position
        engine.execute("norte" if p.y > rural.y else "sul" if p.y < rural.y else
                       "oeste" if p.x > rural.x else "leste")
    count = 0
    while engine.world.turn < 200 and engine.player.alive:
        if engine.player.hunger >= 55:
            if not engine.items.count(engine.player.id, "food"):
                if not engine.execute("coletar").success:
                    engine.execute("trabalhar")
            else:
                engine.execute("comer")
        elif engine.player.thirst >= 50:
            engine.execute("beber")
        else:
            engine.execute("esperar 1")
        count += 1
        if count > 1000:
            raise AssertionError("Reprodução presa")
    movement = engine.execute("leste")
    results.append({"id": "L03", "title": "Cansaço máximo não impõe penalidade física ao jogador",
                    "reproduced": engine.player.fatigue == 100 and engine.player.health == 100 and movement.success,
                    "turn": engine.world.turn, "fatigue": engine.player.fatigue,
                    "health": engine.player.health, "moving_at_maximum_fatigue": movement.success})

    directory.mkdir(parents=True, exist_ok=True)
    (directory / "reproducoes.json").write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(results, ensure_ascii=False, indent=2))
    return results


if __name__ == "__main__":
    run(Path("reports/auditoria_jogador_10000"))
