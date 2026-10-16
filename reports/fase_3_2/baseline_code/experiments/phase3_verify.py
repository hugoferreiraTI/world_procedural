"""Verifica artefatos finais e preservação do baseline, sem alterar saves."""
import ast
import hashlib
import json
from pathlib import Path
from procedural.persistence import JsonRepository, dumps, loads
from procedural.validation import validate_world
from procedural.population import Population

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'reports/fase_3'


def read(path):return json.loads(path.read_text(encoding='utf-8'))


def ast_function(path,name):
    return ast.dump(next(n for n in ast.walk(ast.parse(path.read_text(encoding='utf-8')))
                         if isinstance(n,ast.FunctionDef) and n.name==name),include_attributes=False)


def main():
    core=ROOT/'procedural';baseline=OUT/'baseline_code/procedural'
    checksum=hashlib.sha256(b''.join(p.read_bytes() for p in sorted(core.glob('*.py')))).hexdigest()
    assert checksum==read(OUT/'manifesto_auditoria.json')['core_sha256']
    assert all(ast_function(core/'needs.py',name)==ast_function(baseline/'needs.py',name)
               for name in ('physiology','rest'))
    assert (core/'rules.py').read_bytes()==(baseline/'rules.py').read_bytes()
    assert (core/'personal.py').read_bytes()==(baseline/'personal.py').read_bytes()
    saved_baseline=read(ROOT/'reports/tres_perspectivas_20261007/comparativo.json')
    result={'core_sha256':checksum,'core_unchanged_during_campaigns':True,
            'physiology_rest_rules_and_social_lifetimes_unchanged':True,'campaigns':{}}
    for old in saved_baseline:
        path=ROOT/'reports/tres_perspectivas_20261007'/old['mode']/'save_final.json'
        assert hashlib.sha256(path.read_bytes()).hexdigest()==old['save_sha256']
    result['three_original_saves_preserved']=True
    for mode in ('jogador','espectador','mundo'):
        directory=OUT/'auditorias'/mode;path=directory/'save_final.json'
        world=JsonRepository().load(path);official=read(directory/'metricas_fase2.json')
        metrics=read(directory/'metricas_fase3.json');report=read(directory/'relatorio.json')
        assert not validate_world(world)
        assert metrics['turns']==report['actual_turns']==10000
        assert official['deterministic_continuation_24_hours']
        assert metrics['save_sha256']==hashlib.sha256(path.read_bytes()).hexdigest()
        assert dumps(world)==path.read_text(encoding='utf-8')
        assert dumps(loads(dumps(world)))==dumps(world)
        assert len(report['checkpoints'])==10
        assert all(not c['validation_errors'] and c['money_balance_difference']==0 for c in report['checkpoints'])
        counted=sum(Population(world).counts(t)['persistent_dead'] for t in world.towns.values())
        assert counted==metrics['final']['summary']['dead']
        line_counts={}
        for stream in directory.glob('*.jsonl'):
            with stream.open(encoding='utf-8') as source:
                count=0
                for line in source:json.loads(line);count+=1
            line_counts[stream.name]=count
        result['campaigns'][mode]={'turns':10000,'validation_errors':0,'money_balance_difference':0,
            'counted_deaths':counted,'roundtrip_identical':True,'deterministic_continuation_24_hours':True,
            'save_sha256':metrics['save_sha256'],'jsonl_valid_lines':line_counts}
    (OUT/'verificacao_final.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False,indent=2))


if __name__=='__main__':main()
