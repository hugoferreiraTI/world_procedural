"""Campanhas completas em três checkpoints, com auditoria de moeda e domínios."""

import argparse
from collections import Counter
import json
from pathlib import Path
import time

from procedural.engine import Engine
from procedural.generation import generate_world
from procedural.validation import assert_valid


def money(world):
    return (sum(c.money for c in world.characters.values()) +
            sum(t.money + t.abstract_money for t in world.towns.values()) +
            sum(k.treasury for k in world.kingdoms.values()))


def run(seed, output):
    start = time.monotonic()
    world = generate_world(seed, with_player=False)
    engine = Engine(world)
    engine.goals.debug = True
    initial_turn, initial_money = world.turn, money(world)
    initial_source = world.metrics.get("MoneySourceAbstractWork", 0)
    checkpoints = []
    for elapsed in (1000, 5000, 10000):
        engine.simulate(initial_turn + elapsed - world.turn)
        assert_valid(world)
        expected = initial_money + world.metrics.get("MoneySourceAbstractWork", 0) - initial_source
        assert money(world) == expected, "Moeda criada/perdida fora das fontes registradas"
        dead_towns = [t.name for t in world.towns.values()
                      if not any(world.characters[i].alive and world.characters[i].position.map_id == t.id
                                 for i in t.resident_ids)]
        record = {"elapsed": elapsed, "alive": sum(c.alive for c in world.characters.values()),
                  "initial_characters": len(world.characters), "money": money(world),
                  "legitimate_money_created": expected - initial_money,
                  "money_balance": "exact", "items": len(world.items),
                  "fact_ledger_entries": sum(len(c.applied_facts) for c in world.characters.values()),
                  "towns_without_living_local_npcs": dead_towns,
                  "political_states": dict(Counter(k.political_state for k in world.kingdoms.values())),
                  "economic_states": dict(Counter(k.economic_state for k in world.kingdoms.values())),
                  "invariants": "valid"}
        checkpoints.append(record)
        print(json.dumps({"seed": seed, **record}, ensure_ascii=False), flush=True)
    report = {"seed": seed, "rules_version": world.rules_version,
              "checkpoints": checkpoints, "metrics": world.metrics,
              "decision_examples": list(engine.goals.traces.values())[:8],
              "population_replacement": "deferred_by_user", "seconds": round(time.monotonic() - start, 2)}
    output.mkdir(parents=True, exist_ok=True)
    (output / f"{seed.lower()}.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", default="Dovha")
    parser.add_argument("--output", type=Path, default=Path("reports/hardening"))
    args = parser.parse_args()
    run(args.seed, args.output)
