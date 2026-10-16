"""Compara geração e invariantes econômicos sem prolongar campanhas."""
import json,os,subprocess,sys
from pathlib import Path

SOURCE='''
import json
from dataclasses import asdict
from procedural.generation import generate_world,GenerationConfig
w=generate_world('Fase5-preservacao',with_player=False,config=GenerationConfig(kingdom_count=1,historical_turns=0))
print(json.dumps({'maps':{i:asdict(m) for i,m in w.maps.items()},
 'characters':{i:{'name':p.name,'profession':p.profession,'town':p.town_id,'category':p.category,
 'position':asdict(p.position),'personality':asdict(p.personality),'money':p.money,'hunger':p.hunger,
 'thirst':p.thirst,'fatigue':p.fatigue,'health':p.health,'inventory':p.inventory} for i,p in w.characters.items()},
 'towns':{i:{'name':t.name,'kind':t.kind,'population':t.population,'abstract':t.abstract_population,
 'money':t.money,'inventory':t.inventory,'residents':t.resident_ids} for i,t in w.towns.items()},
 'items':{i:{'name':v.name,'kind':v.kind,'quality':v.quality,'rarity':v.rarity,'owner':v.owner_id,
 'creator':v.creator_id,'origin':v.origin,'damage':v.damage} for i,v in w.items.items()}},ensure_ascii=False))
'''

def main():
    root=Path(__file__).resolve().parents[1]
    snapshots=[]
    for path in (root/'reports/fase_5/baseline_code',root):
        env=dict(os.environ);env['PYTHONPATH']=str(path)
        snapshots.append(json.loads(subprocess.check_output([sys.executable,'-c',SOURCE],cwd='/tmp',env=env,text=True)))
    before,after=snapshots
    result={'seed':'Fase5-preservacao','historical_turns':0,'baseline':'mvp-7-fase4.6','current':'mvp-8-fase5',
            'comparison':{key:before[key]==after[key] for key in before},
            'counts':{'characters':len(after['characters']),'towns':len(after['towns']),'items':len(after['items'])},
            'scope':'Geração física, traços, população e estoques. A sequência de simulação muda com as novas decisões e consumo legítimo de RNG.'}
    (root/'reports/fase_5/PRESERVACAO_GERACAO.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
    print(json.dumps(result,ensure_ascii=False))
    if not all(result['comparison'].values()):raise SystemExit(1)

if __name__=='__main__':main()
