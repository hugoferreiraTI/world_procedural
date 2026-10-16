"""Reproduz um prefixo auditado para capturar conhecimento em treinamento/segurança."""
import argparse
from dataclasses import asdict
import gzip
import hashlib
import json
from pathlib import Path

from procedural.engine import Engine
from procedural.generation import generate_world
from procedural.persistence import dumps
from experiments.feeding_audit import core_hash

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'reports/correcao_alimentar'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mode', required=True, choices=('jogador', 'espectador', 'mundo'))
    args = parser.parse_args();mode = args.mode
    assert core_hash() == json.loads((OUT/'manifesto_auditoria.json').read_text())['core_sha256']
    base = OUT/'auditorias'/mode
    engine = Engine(generate_world('Mira' if mode == 'mundo' else 'Dovha', 'Auditor', with_player=mode == 'jogador'))
    engine.goals.debug = True
    directory = OUT/'replay_acoes';directory.mkdir(exist_ok=True)
    count = 0
    with gzip.open(directory/f'{mode}.jsonl.gz', 'wt', encoding='utf-8') as stream:
        original = engine.goals.execute

        def execute(person, goal, hours):
            nonlocal count
            need = next((n for n in person.needs.values() if n.id == goal.need_id), None)
            record = None
            if goal.action in ('train', 'secure') or need and need.kind in ('status', 'advancement'):
                record = {'turn': engine.world.turn, 'npc_id': person.id, 'goal': asdict(goal),
                          'need': asdict(need) if need else None,
                          'hunger': person.hunger, 'health': person.health,
                          'knowledge_before': [asdict(f) for f in person.knowledge.values()]}
            result = original(person, goal, hours)
            if record is not None:
                record.update(success=result[0], outcome=result[1])
                stream.write(json.dumps(record, ensure_ascii=False, separators=(',', ':'))+'\n');count += 1
            return result
        engine.goals.execute = execute
        if mode == 'jogador':
            for line in (base/'acoes.jsonl').read_text().splitlines():
                if engine.world.turn >= 5024:break
                a = json.loads(line)
                assert engine.world.turn == a['turn_before']
                r = engine.execute(a['command'])
                assert r.success == a['success'] and engine.world.turn == a['turn_after']
        else:
            for i in range(5000):engine.step()
    checksum = hashlib.sha256(dumps(engine.world).encode()).hexdigest()
    expected = hashlib.sha256((base/'save_5000.json').read_bytes()).hexdigest()
    assert checksum == expected, (mode, checksum, expected)
    result = {'mode': mode, 'hours_replayed': 5000, 'identical_checkpoint': True,
              'checkpoint_sha256': checksum, 'action_records': count}
    (directory/f'{mode}_verificacao.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps(result, ensure_ascii=False), flush=True)


if __name__ == '__main__':main()
