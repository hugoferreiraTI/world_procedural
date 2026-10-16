"""Extrai evidências narrativas do save da auditoria, sem avançar o mundo."""

from collections import Counter
from dataclasses import asdict
import hashlib
import json
from pathlib import Path

from procedural.persistence import JsonRepository


def extract(directory):
    save = directory / "save_final.json"
    original_hash = hashlib.sha256(save.read_bytes()).hexdigest()
    repository = JsonRepository()
    world = repository.load(save)
    audit = json.loads((directory / "relatorio.json").read_text(encoding="utf-8"))
    snapshots = [repository.load(directory / name) for name in
                 ("save_1000.json", "save_5000.json")]
    snapshots.append(world)
    selected = (9, 12, 233, 467, 56, 59, 62, 65, 718, 721)

    def stock(entity):
        quantities = Counter()
        for item_id, quantity in entity.inventory.items():
            quantities[world.items[item_id].kind] += quantity
        return dict(quantities)

    dossiers = {}
    for character_id in selected:
        character = world.characters[character_id]
        quests = [q for q in audit["quest_details"] if q["owner_id"] == character_id]
        timeline = []
        for snapshot in snapshots:
            person = snapshot.characters[character_id]
            reputation = person.reputations.get(world.player_id)
            trust = snapshot.relationships.get(f"{character_id}:{world.player_id}:confiança")
            timeline.append({"turn": snapshot.turn, "alive": person.alive,
                             "money": person.money, "hunger": person.hunger,
                             "thirst": person.thirst,
                             "goal": asdict(person.goal) if person.goal else None,
                             "player_reputation": asdict(reputation) if reputation else None,
                             "player_trust": trust.value if trust else None})
        dossiers[character_id] = {
            "name": character.name, "profession": character.profession,
            "town_id": character.town_id, "alive": character.alive,
            "personality": asdict(character.personality), "inventory_by_kind": stock(character),
            "snapshot_timeline": timeline,
            "relationships": [asdict(rel) for rel in world.relationships.values()
                              if rel.source_id == character_id and
                              (rel.target_id in selected or rel.target_id == world.player_id)],
            "quests": quests, "quest_status_counts": dict(Counter(q["status"] for q in quests)),
            "player_events": [e for e in audit["reactions"]
                              if character_id in (e["actor_id"], e["target_id"])],
            "historical_events": [asdict(e) for e in world.history
                                  if character_id in (e.actor_id, e.target_id)],
        }

    # Conhecimentos preservados são cópias de fatos, não o diário completo.
    facts, readers = {}, {}
    for character in world.characters.values():
        for fact in character.knowledge.values():
            readers.setdefault(fact.event_id, []).append(character.id)
            if fact.event_id not in facts or fact.confidence > facts[fact.event_id].confidence:
                facts[fact.event_id] = fact
    canonical = {e.id: e for e in world.history + world.events}
    crimes = []
    for fact in sorted(facts.values(), key=lambda fact: (fact.turn, fact.event_id)):
        if fact.kind in ("ItemStolen", "GuardResponded") and fact.actor_id in (12, 718, 721):
            crimes.append({"fact": asdict(fact), "retained_by": readers[fact.event_id],
                           "canonical_event": asdict(canonical[fact.event_id])
                           if fact.event_id in canonical else None})

    dialogue = []
    with (directory / "acoes.jsonl").open(encoding="utf-8") as stream:
        for line in stream:
            action = json.loads(line)
            if action["command"].startswith("conversar ") and action["success"]:
                dialogue.append({key: action[key] for key in
                                 ("turn_before", "turn_after", "command", "message")})
    living = [c for c in world.characters.values() if c.alive and not c.is_player]
    data = {
        "source_save": str(save.resolve()), "save_sha256": original_hash,
        "turn": world.turn, "player_id": world.player_id,
        "player_nickname": world.characters[world.player_id].nickname,
        "scope": "Leitura do save, checkpoints e diário existente; nenhum turno executado.",
        "npc_alive": len(living), "npc_dead": sum(not c.alive for c in world.characters.values()
                                                  if not c.is_player),
        "history_kind_counts": dict(Counter(e.kind for e in world.history)),
        "recent_event_kind_counts": dict(Counter(e.kind for e in world.events)),
        "retained_distinct_fact_count": len(facts),
        "retained_fact_kind_counts": dict(Counter(f.kind for f in facts.values())),
        "last_goal_counts": dict(Counter(c.goal.action if c.goal else "none" for c in living)),
        "last_goal_status_counts": dict(Counter(c.goal.status if c.goal else "none" for c in living)),
        "world_metrics": world.metrics, "kingdoms": [asdict(k) for k in world.kingdoms.values()],
        "major_history": [asdict(e) for e in world.history],
        "towns": [{"town": asdict(world.towns[i]), "stock_by_kind": stock(world.towns[i]),
                   "npc_on_map": [{"id": c.id, "name": c.name, "alive": c.alive}
                                  for c in world.characters.values()
                                  if not c.is_player and c.position.map_id == i]}
                  for i in (3, 50, 706)],
        "characters": dossiers, "retained_selected_crime_facts": crimes,
        "dialogue_count": len(dialogue),
        "distinct_dialogue_strings": len({d["message"] for d in dialogue}),
        "dialogues": dialogue,
        "quest_count": len(audit["quest_details"]),
        "quest_owner_counts": dict(Counter(q["owner_id"] for q in audit["quest_details"])),
    }
    # Garante que a extração não modificou o arquivo de campanha.
    assert hashlib.sha256(save.read_bytes()).hexdigest() == original_hash
    assert original_hash == audit["save_sha256"]
    destination = directory / "evidencias_historias.json"
    destination.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Evidências: {destination}; turno {world.turn}; save preservado: {original_hash}")


if __name__ == "__main__":
    extract(Path(__file__).resolve().parents[1] / "reports" / "auditoria_jogador_10000")
