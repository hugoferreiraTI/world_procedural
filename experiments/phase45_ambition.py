"""Comparação curta: mesmo mundo/ator, alterando só ambição inicial."""
import json
import argparse
from pathlib import Path
from collections import Counter
from procedural.generation import generate_world,GenerationConfig
from procedural.persistence import dumps,loads
from procedural.engine import Engine
from experiments.phase41_audit import core_hash

def run(output='reports/fase_4_5/comparacao_ambicao_controlada.json'):
    base=generate_world('Ambicao-45',with_player=False,config=GenerationConfig(kingdom_count=1,historical_turns=0))
    p=next(p for p in base.characters.values() if p.profession=='agricultor')
    p.money=40;p.personality.greed=90;p.personality.diligence=70;p.personality.family_loyalty=25;p.personality.persistence=70
    template=dumps(base);result={}
    for ambition in (15,85):
        w=loads(template);actor=w.characters[p.id];actor.personality.ambition=ambition;e=Engine(w)
        activity=Counter();created=[];finished=[]
        def event(ev):
            if ev.actor_id==actor.id and ev.kind=='CommitmentCreated':created.append(ev.context)
            if ev.actor_id==actor.id and ev.kind in ('CommitmentCompleted','AspirationSatisfied'):finished.append(ev.context)
        e.bus.subscribe('*',event);original=e.goals.execute
        def execute(person,goal,hours):
            if person.id==actor.id:
                n=next((n for n in person.needs.values() if n.id==goal.need_id),None)
                activity[(n.kind if n else 'none')+':'+goal.action]+=1
            return original(person,goal,hours)
        e.goals.execute=execute;e.simulate(120)
        result[str(ambition)]={'alive':actor.alive,'hp':actor.health,'money':actor.money,
            'aspirations':[{'domain':a.domain,'intensity':a.intensity,'status':a.status,'progress':a.progress} for a in actor.aspirations],
            'actions':dict(activity),'commitments_created':created,'endings':finished}
    Path(output).write_text(json.dumps({'seed':'Ambicao-45','core_sha256':core_hash(),
        'hours':120,'owner':p.id,'same_initial_world':True,'only_changed_trait':'ambition','results':result},ensure_ascii=False,indent=2))
    print({k:{'money':v['money'],'asp':v['aspirations'],'commitments':len(v['commitments_created']),
        'advancement_actions':sum(x for a,x in v['actions'].items() if a.startswith('advancement:'))} for k,v in result.items()})
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',default='reports/fase_4_5/comparacao_ambicao_controlada.json')
    run(parser.parse_args().output)
