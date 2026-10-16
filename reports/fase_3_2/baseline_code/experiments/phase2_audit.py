"""Campanha pública de 10.000 horas com auditoria observacional da fase 2."""

import argparse
from collections import Counter, defaultdict
from dataclasses import asdict
import hashlib
import json
from pathlib import Path

from experiments.player_audit import run
from procedural.persistence import JsonRepository, dumps

GROUPS = {"food": "physiological", "water": "physiological", "rest": "physiological",
          "money": "work_income", "work": "work_income", "family": "family",
          "grief": "grief", "revenge": "revenge", "protection": "protection",
          "status": "status", "advancement": "advancement", "security": "guard_security"}


class Audit:
    def __init__(self, directory):
        self.directory = directory
        self.initial = None
        self.initial_active = Counter()
        self.last_trace = {}
        self.decisions = Counter()
        self.examples = defaultdict(list)
        self.comparable = defaultdict(dict)
        self.by_type = defaultdict(dict)
        self.event_count = Counter()
        self.events = (directory / "eventos_pessoais.jsonl").open("w", encoding="utf-8")

    def __call__(self, engine):
        if self.initial is None:
            self.initial = dict(engine.world.metrics)
            self.initial_active = Counter(n.kind for c in engine.world.characters.values() if not c.is_player
                                          for n in c.needs.values() if n.status not in ("satisfied", "expired", "failed", "inactive"))
            engine.goals.debug = True
            engine.bus.subscribe("*", self.on_event)
        for npc_id, trace in engine.goals.traces.items():
            stamp = trace["turn"]
            if self.last_trace.get(npc_id) == stamp:
                continue
            self.last_trace[npc_id] = stamp
            npc = engine.world.characters[npc_id]
            group = GROUPS.get(trace["need"], trace["need"])
            self.decisions[group] += 1
            if group not in ("physiological", "work_income", "guard_security"):
                record = {"npc_id": npc.id, "name": npc.name, "personality": asdict(npc.personality),
                          "trace": trace, "goal": asdict(npc.goal) if npc.goal else None,
                          "health": npc.health, "hunger": npc.hunger, "thirst": npc.thirst}
                if len(self.examples[group]) < 30:
                    self.examples[group].append(record)
                self.by_type[group].setdefault(trace["selected"], record)
                if trace["source"].startswith("event:") and group in ("grief", "revenge", "protection"):
                    self.comparable[(trace["source"], group)].setdefault(npc_id, record)

    def on_event(self, event):
        if event.kind in ("FamilyConcern", "AbsenceNoticed", "FamilySearch", "PersonLocated", "RemainsLocated",
                          "ComfortGiven", "Remembrance", "InvestigationPerformed", "ThreatReported",
                          "ThreatAvoided", "ProtectionGiven", "InformationShared", "ResponsibilityFulfilled"):
            self.event_count[event.kind] += 1
            self.events.write(json.dumps(asdict(event), ensure_ascii=False) + "\n")

    def finish(self, report):
        self.events.close()
        world = JsonRepository().load(self.directory / "save_final.json")
        lifecycle = {transition: defaultdict(Counter) for transition in
                     ("Created", "Satisfied", "Expired", "Blocked", "Quest", "Selected")}
        for key, value in world.metrics.items():
            if not key.startswith("NPCNeed"):
                continue
            transition, kind = key[len("NPCNeed"):].split(":", 1)
            if transition in lifecycle:
                lifecycle[transition][GROUPS.get(kind, kind)][kind] += value - self.initial.get(key, 0)
        comparable = []
        different_npcs = set()
        for (source, group), people in self.comparable.items():
            actions = {r["trace"]["selected"] for r in people.values()}
            if len(people) >= 2 and len(actions) >= 2:
                different_npcs.update(people)
                if len(comparable) < 30:
                    comparable.append({"source": source, "group": group, "responses": list(people.values())})
        # A continuação é verificada sem tocar o arquivo: somente cópias em memória.
        from procedural.engine import Engine
        a = JsonRepository().load(self.directory / "save_final.json")
        b = JsonRepository().load(self.directory / "save_final.json")
        Engine(a).simulate(24)
        Engine(b).simulate(24)
        assert dumps(a) == dumps(b)
        result = {"seed": report["seed"], "rules_version": world.rules_version,
                  "start_turn": report["start_turn"], "actual_turns": report["actual_turns"],
                  "selected_distribution": {group: sum(kinds.values()) for group, kinds in lifecycle["Selected"].items()},
                  "trace_observation_counts": dict(self.decisions),
                  "initial_active_need_counts": dict(self.initial_active),
                  "lifecycle": {state: {group: dict(kinds) for group, kinds in data.items()}
                                for state, data in lifecycle.items()},
                  "quest_types": dict(Counter(q.kind for q in world.quests.values())),
                  "quest_outcomes_by_type": {kind: dict(Counter(q.status for q in world.quests.values() if q.kind == kind))
                                             for kind in {q.kind for q in world.quests.values()}},
                  "personal_event_counts": dict(self.event_count), "examples": dict(self.examples),
                  "comparable_events_with_different_choices": comparable,
                  "different_choices_by_pressure_type": {group: list(actions.values()) for group, actions in self.by_type.items()},
                  "npcs_with_different_choices_on_comparable_events": len(different_npcs),
                  "save_sha256": hashlib.sha256((self.directory / "save_final.json").read_bytes()).hexdigest(),
                  "deterministic_continuation_24_hours": True,
                  "note": "Contagens de criação/satisfação/expiração são episódios, não apenas IDs. Bloqueio é contado uma vez por episódio. Exemplos são observados, sem fixtures na campanha."}
        (self.directory / "metricas_fase2.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(json.dumps({"selected_distribution": result["selected_distribution"],
                          "quest_types": result["quest_types"], "personal_event_counts": result["personal_event_counts"],
                          "different_npcs": len(different_npcs)}, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", default="Dovha")
    parser.add_argument("--turnos", type=int, default=10000)
    parser.add_argument("--output", type=Path, default=Path("reports/fase_2/auditoria_10000"))
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    auditor = Audit(args.output)
    result = run(args.seed, args.turnos, args.output, observer=auditor)
    auditor.finish(result)
