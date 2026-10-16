"""Integridade do baseline, geração, regras vitais e campanhas da Fase 3.2."""
import ast
import gzip
import hashlib
import json
from pathlib import Path
import subprocess

from experiments.feeding_audit import core_hash
from procedural.engine import Engine
from procedural.persistence import JsonRepository, dumps, loads
from procedural.validation import validate_world

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'reports/fase_3_2'


def read(path):return json.loads(path.read_text())
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def function(path, name):
    return ast.dump(next(n for n in ast.walk(ast.parse(path.read_text()))
                         if isinstance(n,ast.FunctionDef) and n.name==name),include_attributes=False)


def main():
    assert core_hash() == read(OUT/'manifesto_auditoria.json')['core_sha256']
    preserved = read(OUT/'arquivos_anteriores.json')
    for path,sha in preserved.items():assert digest(ROOT/path) == sha, path
    for path in (OUT/'baseline_code/tests').glob('*.py'):
        assert path.read_bytes() == (ROOT/'tests'/path.name).read_bytes()
    for path in (OUT/'codigo_congelado').glob('*.py'):
        assert path.read_bytes() == (ROOT/'procedural'/path.name).read_bytes()
    for name in ('physiology','rest'):
        assert function(ROOT/'procedural/needs.py',name) == function(OUT/'baseline_code/procedural/needs.py',name)
    for name in ('inventory_changed','emergency','immediate_meal_needed','survival_margin'):
        assert function(ROOT/'procedural/feeding.py',name) == function(OUT/'baseline_code/procedural/feeding.py',name)
    assert (ROOT/'procedural/rules.py').read_bytes() == (OUT/'baseline_code/procedural/rules.py').read_bytes()
    initial_script = '''from dataclasses import asdict
import json,hashlib
from procedural.generation import generate_world,GenerationConfig
for seed in ('Dovha','Mira'):
 w=generate_world(seed,with_player=False,config=GenerationConfig(historical_turns=0))
 data=asdict(w);data['rules_version']='masked-only-version'
 print(seed,hashlib.sha256(json.dumps(data,sort_keys=True,ensure_ascii=False).encode()).hexdigest())
'''
    old = subprocess.check_output(['python3','-c',initial_script],cwd=OUT/'baseline_code',text=True)
    new = subprocess.check_output(['python3','-c',initial_script],cwd=ROOT,text=True)
    assert old == new,(old,new)
    result = {'core_sha256':core_hash(),'previous_files_preserved':len(preserved),'original_130_tests_unchanged':True,
              'vital_physiology_rest_and_emergency_unchanged':True,'initial_generation_hashes':new.splitlines(),'campaigns':{}}
    for mode in ('jogador','espectador','mundo'):
        directory = OUT/'auditorias'/mode;path=directory/'save_final.json'
        world = JsonRepository().load(path)
        assert not validate_world(world)
        assert dumps(world) == path.read_text() == dumps(loads(path.read_text()))
        report=read(directory/'relatorio.json')
        assert report['actual_turns']==10000
        assert all(not c['validation_errors'] and c['money_balance_difference']==0 for c in report['checkpoints'])
        short_stage=read(OUT/'manifesto_auditoria.json')['short_audit']
        short=read(OUT/short_stage/mode/'metricas_fase32.json')
        assert (directory/'save_1000.json').read_bytes() == (OUT/short_stage/mode/'save_final.json').read_bytes()
        a,b=Engine(loads(dumps(world))),Engine(loads(dumps(world)))
        a.simulate(24);b.simulate(24)
        assert dumps(a.world)==dumps(b.world)
        assert not validate_world(a.world)
        invalid_reports=0;reported=0;empty_information_success=0;personal_lines=0
        with gzip.open(directory/'acoes_pessoais.jsonl.gz','rt') as stream:
            for line in stream:
                row=json.loads(line);personal_lines+=1
                if row['goal']['action']=='denounce' and row['success']:
                    reported+=1
                    need=row['need'];source=need['context'].get('source_event')
                    fact=next((f for f in row['knowledge_before'] if f['event_id']==source),{})
                    excluded={row['npc_id'],fact.get('actor_id'),need['context'].get('culprit'),need['context'].get('threat')}
                    if need['kind']=='revenge':excluded.add(need['target_id'])
                    invalid_reports+=row['goal']['target_id'] in excluded
                if row['goal']['action']=='ask_personal_help' and row['success'] and row['outcome'].startswith(('Resposta sem avanço','Informação sem avanço')):
                    empty_information_success+=1
        assert invalid_reports==empty_information_success==0
        result['campaigns'][mode]={'save_sha256':digest(path),'roundtrip_identical':True,
             'short_1000_checkpoint_identical':True,'deterministic_continuation_24_hours':True,'continuation_errors':0,
             'money_difference':0,'population_invariants':True,'valid_reports':reported,'invalid_independent_reports':invalid_reports,
             'false_information_success':empty_information_success,'personal_action_rows':personal_lines}
    (OUT/'verificacao_final.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(result,ensure_ascii=False,indent=2))


if __name__ == '__main__':main()
