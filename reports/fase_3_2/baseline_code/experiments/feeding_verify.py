"""Verifica integridade, campanhas, contabilidade e persistência da correção."""
import ast
import gzip
import hashlib
import json
from pathlib import Path

from experiments.feeding_audit import core_hash
from procedural.persistence import JsonRepository, dumps, loads
from procedural.validation import validate_world

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'reports/correcao_alimentar'


def read(path):
    return json.loads(path.read_text())


def function(path, name):
    return ast.dump(next(n for n in ast.walk(ast.parse(path.read_text()))
                         if isinstance(n, ast.FunctionDef) and n.name == name), include_attributes=False)


def main():
    manifest = read(OUT/'manifesto_auditoria.json')
    assert core_hash() == manifest['core_sha256']
    for p in (ROOT/'procedural').glob('*.py'):
        assert p.read_bytes() == (OUT/'codigo_congelado'/p.name).read_bytes()
    for name in ('physiology', 'rest'):
        assert function(ROOT/'procedural/needs.py', name) == function(OUT/'baseline_code/procedural/needs.py', name)
    for name in ('economy.py', 'professions.py', 'personal.py'):
        assert (ROOT/'procedural'/name).read_bytes() == (OUT/'baseline_code/procedural'/name).read_bytes()
    for p in (OUT/'baseline_code/tests').glob('*.py'):
        assert p.read_bytes() == (ROOT/'tests'/p.name).read_bytes()
    for path, checksum in read(OUT/'baseline_arquivos.json').items():
        assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest() == checksum
    result = {'core_sha256': core_hash(), 'frozen_code_identical': True,
              'all_original_tests_preserved': True, 'phase3_artifacts_preserved': True,
              'physiology_rest_economy_professions_personal_unchanged': True, 'campaigns': {}}
    for mode in ('jogador', 'espectador', 'mundo'):
        directory = OUT/'auditorias'/mode
        path = directory/'save_final.json'
        world = JsonRepository().load(path)
        assert not validate_world(world)
        assert dumps(world) == path.read_text()
        assert dumps(loads(dumps(world))) == dumps(world)
        report = read(directory/'relatorio.json')
        feeding = read(directory/'metricas_alimentacao.json')
        economic = read(directory/'metricas_fase3.json')
        personal = read(directory/'metricas_fase2.json')
        assert report['actual_turns'] == economic['turns'] == feeding['turns'] == 10000
        assert len(report['checkpoints']) == 10
        assert all(not c['validation_errors'] and c['money_balance_difference'] == 0 for c in report['checkpoints'])
        assert personal['deterministic_continuation_24_hours']
        checksum = hashlib.sha256(path.read_bytes()).hexdigest()
        assert checksum == economic['save_sha256']
        assert read(OUT/'baseline_medicoes'/f'{mode}.json')['identical_original_save']
        counts = {}
        for p in directory.glob('*.jsonl*'):
            opener = gzip.open if p.suffix == '.gz' else open
            with opener(p, 'rt', encoding='utf-8') as stream:
                count = 0
                for line in stream:
                    json.loads(line);count += 1
            counts[p.name] = count
        result['campaigns'][mode] = {'turns': 10000, 'roundtrip_identical': True,
            'deterministic_continuation_24_hours': True, 'validation_errors': 0,
            'money_balance_difference': 0, 'save_sha256': checksum,
            'hunger_deaths_with_food': feeding['hunger_deaths_with_food'],
            'fresh_acquisition_hunger_deaths': feeding['hunger_deaths_fresh_acquisition'],
            'prior_food_hunger_deaths': feeding['hunger_deaths_prior_food'], 'valid_stream_lines': counts}
    (OUT/'verificacao_final.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
