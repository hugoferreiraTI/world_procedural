"""Observação sem intervenção: crônica global, pressões pessoais e localidades.

O observador nunca escreve no mundo nem influencia escolhas. As observações de
necessidades são amostras ao fechar cada hora; métricas oficiais vêm do motor.
"""

import argparse
from collections import Counter, defaultdict
from dataclasses import asdict
import json
from pathlib import Path
import time

from experiments.phase2_audit import Audit, GROUPS
from experiments.player_audit import money
from procedural.engine import Engine
from procedural.generation import generate_world
from procedural.needs import FINISHED
from procedural.personal import PERSONAL_KINDS
from procedural.persistence import JsonRepository
from procedural.validation import validate_world

NARRATIVE_EVENTS = {
    "CharacterDied", "SuccessionChanged", "FamilyConcern", "AbsenceNoticed",
    "FamilySearch", "PersonLocated", "RemainsLocated", "ComfortGiven",
    "Remembrance", "InvestigationPerformed", "ThreatReported", "ThreatAvoided",
    "ProtectionGiven", "InformationShared", "ResponsibilityFulfilled",
    "HelpGiven", "HelpRequested", "QuestCompleted", "PlayerRefusedRequest",
    "ItemStolen", "GuardResponded", "FoodShortage",
}


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


class WorldAudit(Audit):
    def __init__(self, directory, mode):
        super().__init__(directory)
        self.mode = mode
        self.engine = None
        self.start = None
        self.focus = None
        self.needs_seen = {}
        self.trace_seen = {}
        self.frames = []
        self.region_events = defaultdict(Counter)
        self.localities_decisions = defaultdict(Counter)
        self.need_transitions = Counter()
        self.deaths = []
        self.narrative = (directory / "cronica.jsonl").open("w", encoding="utf-8")
        self.need_stream = (directory / "necessidades_pessoais.jsonl").open("w", encoding="utf-8")

    def __call__(self, engine):
        self.engine = engine
        world = engine.world
        if self.start is None:
            self.start = world.turn
            self.focus = next(iter(world.kingdoms.values())).capital_id
            write_json(self.directory / "elenco.json", {
                "seed": world.seed, "start_turn": self.start,
                "focus_town_id": self.focus,
                "characters": [{"id": c.id, "name": c.name, "town_id": c.town_id,
                    "profession": c.profession, "category": c.category,
                    "personality": asdict(c.personality), "alive_at_start": c.alive}
                    for c in world.characters.values() if not c.is_player],
                "relationships": [asdict(r) for r in world.relationships.values()
                    if r.kind in ("casamento", "pai_de", "filho_de", "amizade")],
                "kingdoms": [{"id": k.id, "name": k.name, "capital_id": k.capital_id,
                    "bounds": k.bounds, "royal_family": k.royal_family} for k in world.kingdoms.values()],
                "towns": [{"id": t.id, "name": t.name, "kingdom_id": t.kingdom_id,
                    "position": asdict(t.position), "capital": t.capital, "kind": t.kind}
                    for t in world.towns.values()],
            })
        super().__call__(engine)
        for npc_id, trace in engine.goals.traces.items():
            if self.trace_seen.get(npc_id) == trace["turn"]:
                continue
            self.trace_seen[npc_id] = trace["turn"]
            town_id = world.characters[npc_id].town_id
            self.localities_decisions[town_id][GROUPS.get(trace["need"], trace["need"])] += 1
        for character in world.characters.values():
            if character.is_player:
                continue
            for key, need in character.needs.items():
                if need.kind not in PERSONAL_KINDS:
                    continue
                signature = (need.status, need.created_at, need.source, need.target_id)
                if self.needs_seen.get((character.id, key)) == signature:
                    continue
                initial = world.turn == self.start
                self.needs_seen[character.id, key] = signature
                if not initial:
                    self.need_transitions[need.kind] += 1
                record = {"observed_at": world.turn, "initial_snapshot": initial,
                    "npc_id": character.id, "name": character.name, "town_id": character.town_id,
                    "need": asdict(need), "alive": character.alive,
                    "health": character.health, "hunger": character.hunger,
                    "thirst": character.thirst}
                self.need_stream.write(json.dumps(record, ensure_ascii=False) + "\n")
        if (world.turn - self.start) % 250 == 0:
            self.frame()

    def on_event(self, event):
        super().on_event(event)
        if event.kind not in NARRATIVE_EVENTS:
            return
        world = self.engine.world
        town_id = event.location.map_id if event.location and event.location.map_id in world.towns else None
        if town_id is None and event.actor_id in world.characters:
            town_id = world.characters[event.actor_id].town_id
        if town_id is None and event.target_id in world.characters:
            town_id = world.characters[event.target_id].town_id
        if event.kind == "SuccessionChanged" and event.target_id in world.kingdoms:
            town_id = world.kingdoms[event.target_id].capital_id
        self.region_events[town_id][event.kind] += 1
        record = {**asdict(event), "town_id": town_id, "in_focus_town": town_id == self.focus}
        self.narrative.write(json.dumps(record, ensure_ascii=False) + "\n")
        if event.kind == "CharacterDied":
            victim = world.characters[event.target_id]
            self.deaths.append({"turn": event.turn, "id": victim.id, "name": victim.name,
                "town_id": victim.town_id, "profession": victim.profession,
                "hunger": victim.hunger, "thirst": victim.thirst,
                "food_carried": self.engine.items.count(victim.id, "food"),
                "water_carried": self.engine.items.count(victim.id, "water"),
                "last_goal": asdict(victim.goal) if victim.goal else None})

    def frame(self):
        world = self.engine.world
        here = defaultdict(list)
        for c in world.characters.values():
            if not c.is_player:
                here[c.position.map_id].append(c)
        self.frames.append({"turn": world.turn, "elapsed": world.turn - self.start,
            "global_alive": sum(c.alive and not c.is_player for c in world.characters.values()),
            "global_dead": sum(not c.alive and not c.is_player for c in world.characters.values()),
            "outside_local_maps_npc_ids": [c.id for c in world.characters.values()
                if not c.is_player and c.position.map_id not in world.towns],
            "towns": [{"id": t.id, "alive": sum(c.alive for c in here[t.id]),
                "dead": sum(not c.alive for c in here[t.id]),
                "food": self.engine.items.count(t.id, "food"),
                "grain": self.engine.items.count(t.id, "grain"),
                "water": self.engine.items.count(t.id, "water"),
                "money": t.money,
                "active_needs": dict(Counter(n.kind for c in here[t.id] if c.alive
                    for n in c.needs.values() if n.status not in FINISHED))}
                for t in world.towns.values()],
            "kingdoms": [{"id": k.id, "ruler_id": k.ruler_id,
                "political": k.political_state, "economic": k.economic_state}
                for k in world.kingdoms.values()]})

    def finish(self, report):
        self.narrative.close()
        self.need_stream.close()
        write_json(self.directory / "quadros_mundo.json", self.frames)
        write_json(self.directory / "cobertura.json", {
            "mode": self.mode, "seed": report["seed"], "focus_town_id": self.focus,
            "all_npcs_inspected": len(self.engine.world.characters),
            "all_localities_inspected": len(self.engine.world.towns),
            "all_kingdoms_inspected": len(self.engine.world.kingdoms),
            "snapshot_interval_hours": 250, "frames": len(self.frames),
            "personal_state_transitions_observed": dict(self.need_transitions),
            "narrative_events_by_locality": {str(k): dict(v) for k, v in self.region_events.items()},
            "decision_samples_by_locality": {str(k): dict(v) for k, v in self.localities_decisions.items()},
            "note": "Todas as necessidades de todos os NPCs são lidas após cada hora. Transições instantâneas dentro da hora podem escapar da amostra; métricas persistentes são a contagem oficial. Crônica registra eventos reais, não conhecimento universal dos personagens.",
        })
        super().finish(report)


def run(seed, turns, directory, mode):
    directory.mkdir(parents=True, exist_ok=True)
    started = time.monotonic()
    engine = Engine(generate_world(seed, with_player=False))
    world = engine.world
    start = world.turn
    initial_money = money(world)
    initial_source = world.metrics.get("MoneySourceAbstractWork", 0)
    observer = WorldAudit(directory, mode)
    observer(engine)
    checkpoints = []
    for elapsed in range(1, turns + 1):
        engine.step()
        observer(engine)
        if elapsed % 1000 == 0 or elapsed == turns:
            errors = validate_world(world)
            balance = money(world) - initial_money - (world.metrics.get("MoneySourceAbstractWork", 0) - initial_source)
            point = {"elapsed": elapsed, "turn": world.turn,
                "alive_npcs": sum(c.alive for c in world.characters.values()),
                "food_markets_empty": sum(engine.items.count(t.id, "food") == 0 for t in world.towns.values()),
                "kingdoms_without_ruler": sum(k.ruler_id is None for k in world.kingdoms.values()),
                "validation_errors": errors, "money_balance_difference": balance}
            checkpoints.append(point)
            print(json.dumps(point, ensure_ascii=False), flush=True)
            if errors or balance:
                raise AssertionError(point)
            if elapsed in (1000, 5000):
                JsonRepository().save(world, directory / f"save_{elapsed}.json")
    JsonRepository().save(world, directory / "save_final.json")
    report = {"mode": mode, "seed": seed, "rules_version": world.rules_version,
        "start_turn": start, "actual_turns": world.turn - start,
        "player_present": False, "player_commands": 0,
        "checkpoints": checkpoints, "deaths": observer.deaths,
        "quests": dict(Counter(q.status for q in world.quests.values())),
        "seconds": round(time.monotonic() - started, 2)}
    write_json(directory / "relatorio.json", report)
    observer.finish(report)
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", default="Dovha")
    parser.add_argument("--turnos", type=int, default=10000)
    parser.add_argument("--mode", choices=("espectador", "mundo"), required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.turnos <= 0:
        parser.error("Turnos deve ser positivo.")
    run(args.seed, args.turnos, args.output, args.mode)
