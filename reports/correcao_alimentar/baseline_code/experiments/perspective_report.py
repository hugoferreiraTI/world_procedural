"""Extrai encadeamentos narrativos sem avançar ou editar os saves."""

from collections import Counter, defaultdict
import json
from pathlib import Path

from experiments.perspective_audit import write_json
from procedural.persistence import JsonRepository

ROOT = Path(__file__).resolve().parents[1] / "reports/tres_perspectivas_20261007"


def extract(mode):
    directory = ROOT / mode
    cast = json.loads((directory / "elenco.json").read_text())
    names = {c["id"]: c for c in cast["characters"]}
    towns = {t["id"]: t for t in cast["towns"]}
    episodes = {}
    source_ids = set()
    with (directory / "necessidades_pessoais.jsonl").open() as stream:
        for line in stream:
            record = json.loads(line)
            need = record["need"]
            key = (record["npc_id"], need["id"], need["created_at"])
            if key not in episodes:
                episodes[key] = {"first": record, "last": record, "statuses": set()}
            episode = episodes[key]
            episode["last"] = record
            episode["statuses"].add(need["status"])
            if need["source"].startswith("event:"):
                source_ids.add(int(need["source"].split(":")[1]))
    sources, deeds = {}, defaultdict(list)
    deed_kinds = {"Remembrance", "ComfortGiven", "InvestigationPerformed", "ThreatReported",
                  "ThreatAvoided", "ProtectionGiven", "ResponsibilityFulfilled", "PersonLocated",
                  "HelpGiven", "InformationShared", "FamilySearch", "SuccessionChanged"}
    with (directory / "cronica.jsonl").open() as stream:
        for line in stream:
            event = json.loads(line)
            if event["id"] in source_ids or event["kind"] in ("CharacterDied", "SuccessionChanged"):
                sources[event["id"]] = event
            if event["kind"] in deed_kinds:
                for entity in {event["actor_id"], event["target_id"]} - {None}:
                    deeds[entity].append(event)
    candidates = []
    for (npc_id, _, _), episode in episodes.items():
        first, last = episode["first"], episode["last"]
        need = last["need"]
        if last["observed_at"] <= cast["start_turn"] or need["kind"] not in ("grief", "revenge", "protection", "family", "status", "advancement"):
            continue
        source_id = int(need["source"].split(":")[1]) if need["source"].startswith("event:") else None
        first_source = first["need"]["source"]
        first_source_id = int(first_source.split(":")[1]) if first_source.startswith("event:") else None
        matching = []
        for event in deeds.get(npc_id, []):
            if not need["created_at"] <= event["turn"] <= last["observed_at"]:
                continue
            k, ctx = event["kind"], event["context"]
            actor, target = event["actor_id"], event["target_id"]
            keep = False
            if need["kind"] == "grief":
                keep = (k == "Remembrance" and actor == npc_id and ctx.get("relative_id") == need["target_id"] or
                        k == "ComfortGiven" and target == npc_id)
            elif need["kind"] == "family":
                keep = (k in ("PersonLocated", "HelpGiven") and actor == npc_id and target == need["target_id"] or
                        k == "FamilySearch" and actor == npc_id and ctx.get("relative_id") == need["target_id"])
            elif need["kind"] in ("revenge", "protection"):
                keep = actor == npc_id and (ctx.get("source") == need["source"] or ctx.get("fact_id") == source_id)
            elif need["kind"] == "status":
                keep = k == "ResponsibilityFulfilled" and actor == npc_id and ctx.get("need_source") == need["source"]
            if keep:
                matching.append(event)
        if not matching and need["status"] != "satisfied" and need["kind"] != "grief":
            continue
        person = names[npc_id]
        victim = need["context"].get("loss", need["context"].get("victim", need["target_id"]))
        candidates.append({
            "npc_id": npc_id, "name": person["name"], "town_id": person["town_id"],
            "town_name": towns[person["town_id"]]["name"], "kingdom_id": towns[person["town_id"]]["kingdom_id"],
            "profession": person["profession"], "personality": person["personality"],
            "kind": need["kind"], "need_id": need["id"], "created_at": need["created_at"],
            "carried_from_preparation": first["initial_snapshot"],
            "observed_until": last["observed_at"], "outcome": need["status"],
            "actor_alive_at_outcome": last["alive"], "need_context": need["context"],
            "victim_id": victim, "victim_name": names.get(victim, {}).get("name"),
            "source": need["source"], "source_event": sources.get(source_id),
            "first_source": first_source, "first_source_event": sources.get(first_source_id),
            "source_changed_in_episode": first_source != need["source"],
            "deeds": matching[:12], "deed_count": len(matching),
            "observed_statuses": sorted(episode["statuses"]),
            "first_priority_observed": first["need"]["priority"],
        })
    # Não atribui ação ao dono de vingança encerrada pela ação de um guarda.
    candidates.sort(key=lambda x: (-bool(x["deeds"]), -len(x["deeds"]), x["created_at"], x["npc_id"]))
    selected = []
    for kind in ("grief", "family", "revenge", "protection", "status", "advancement"):
        selected.extend([c for c in candidates if c["kind"] == kind][:15])
    selected_keys = {(x["npc_id"], x["need_id"], x["created_at"]) for x in selected}
    focus = [c for c in candidates if c["town_id"] == cast["focus_town_id"]]
    for candidate in focus[:15]:
        if (candidate["npc_id"], candidate["need_id"], candidate["created_at"]) not in selected_keys:
            selected.append(candidate)
    result = {"seed": cast["seed"], "mode": mode, "focus_town_id": cast["focus_town_id"],
        "focus_town_name": towns[cast["focus_town_id"]]["name"],
        "note": "Encadeamentos de necessidade e eventos reais. Satisfied pode significar resolução externa; deeds é evidência específica de ação do personagem/apoio recebido. Uma pressão ativa pode receber novas fontes de dano: first_source e source distinguem início e contexto final. Amostragem de fim de hora não substitui contadores oficiais.",
        "observed_episode_count": len(episodes),
        "candidate_count_by_kind": dict(Counter(c["kind"] for c in candidates)),
        "selected_stories": selected,
        "historical_events": [e for e in sources.values() if e["kind"] in ("CharacterDied", "SuccessionChanged")],
    }
    write_json(directory / "historias.json", result)
    return result


def compare():
    rows = []
    for mode in ("jogador", "espectador", "mundo"):
        directory = ROOT / mode
        report = json.loads((directory / "relatorio.json").read_text())
        metrics = json.loads((directory / "metricas_fase2.json").read_text())
        world = JsonRepository().load(directory / "save_final.json")
        total = sum(metrics["selected_distribution"].values())
        checkpoint = report["checkpoints"][-1]
        rows.append({"mode": mode, "seed": report["seed"], "turns": report["actual_turns"],
            "alive_npcs": checkpoint["alive_npcs"], "deaths": len(report["deaths"]),
            "localities": len(world.towns), "empty_food_markets": checkpoint["food_markets_empty"],
            "kingdoms_without_ruler": checkpoint["kingdoms_without_ruler"],
            "localities_without_alive_npcs": sum(not any(c.alive and c.position.map_id == t.id
                and not c.is_player for c in world.characters.values()) for t in world.towns.values()),
            "all_npc_decisions": total, "selected_distribution": metrics["selected_distribution"],
            "physiological_percent": 100 * metrics["selected_distribution"]["physiological"] / total,
            "personal_events": metrics["personal_event_counts"], "quest_types": metrics["quest_types"],
            "quest_outcomes": report["quests"],
            "checkpoint_errors": sum(len(c["validation_errors"]) for c in report["checkpoints"]),
            "maximum_money_balance_difference": max(abs(c["money_balance_difference"]) for c in report["checkpoints"]),
            "save_sha256": metrics["save_sha256"],
            "deterministic_continuation_24_hours": metrics["deterministic_continuation_24_hours"],
            "seconds": report["seconds"]})
    write_json(ROOT / "comparativo.json", rows)
    return rows


if __name__ == "__main__":
    for mode in ("espectador", "mundo"):
        result = extract(mode)
        print(mode, result["candidate_count_by_kind"])
    for row in compare():
        print(row["mode"], row["alive_npcs"], round(row["physiological_percent"], 4))
