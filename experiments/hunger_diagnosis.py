"""Replay observacional de fome; não altera regras, decisões nem saves originais."""
import argparse
from collections import Counter, defaultdict, deque
from dataclasses import asdict
import hashlib
import json
from pathlib import Path
from procedural.engine import Engine
from procedural.generation import generate_world
from procedural.navigation import distance
from procedural.persistence import dumps

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'reports/fase_3/auditorias'
OUT=ROOT/'reports/diagnostico_fome'


class HungerObserver:
    def __init__(self, engine):
        self.engine=engine;self.history=defaultdict(lambda:deque(maxlen=64))
        self.current={};self.last_decision={};self.deaths=[];self.counters=Counter()
        engine.goals.debug=True
        decide=engine.goals.decide;execute=engine.goals.execute
        physiology=engine.needs.physiology;record=engine.record_deprivation

        def decision(person,elapsed=1):
            row={'type':'decision','turn':engine.world.turn,'elapsed':elapsed,'before':self.state(person),
                 'previous_goal':asdict(person.goal) if person.goal else None}
            self.current[person.id]=row
            decide(person,elapsed)
            trace=engine.goals.traces.get(person.id,{})
            row['need']=trace.get('need');row['selected']=trace.get('selected')
            row['priorities']=[{'kind':n['kind'],'priority':n['priority'],'id':person.needs.get(n['kind']).id
                               if person.needs.get(n['kind']) else None} for n in trace.get('active_needs',[])]
            row['candidates']=[{'action':s['action'],'score':s['score']} for s in trace.get('candidates',[])]
            row['after']=self.state(person);row['goal']=asdict(person.goal) if person.goal else None
            self.history[person.id].append(row);self.last_decision[person.id]=row
            if row['before']['hunger']>=85:
                self.counters['critical_decisions']+=1
                self.counters['critical_selected:'+str(row['selected'])]+=1
                if row['before']['food']>0:
                    self.counters['critical_decisions_with_food']+=1
                    self.counters['critical_with_food_selected:'+str(row['selected'])]+=1
            self.current.pop(person.id,None)

        def execution(person,goal,hours):
            before=self.state(person);result=execute(person,goal,hours)
            if person.id in self.current:
                self.current[person.id]['execution']={'action':goal.action,'hours':hours,
                    'success':result[0],'message':result[1],'before':before,'after':self.state(person)}
            return result

        def physics(person):
            relevant=person.hunger>=80 or person.health<=20
            before=self.state(person) if relevant else None
            physiology(person)
            if relevant:
                self.history[person.id].append({'type':'physiology','turn':engine.world.turn,
                    'before':before,'after':self.state(person)})

        def death(person):
            record(person)
            if person.is_player:return
            self.deaths.append({'id':person.id,'category':person.category,'record':dict(engine.world.death_records[person.id]),
                'at_death':self.state(person),'last_decision':self.last_decision.get(person.id),
                'history':list(self.history[person.id]),
                'food_anywhere':sum(engine.items.count(t.id,'food') for t in engine.world.towns.values())})
            self.history.pop(person.id,None)

        engine.goals.decide=decision;engine.goals.execute=execution
        engine.needs.physiology=physics;engine.record_deprivation=death

    def state(self,person):
        e=self.engine;t=e.world.towns[person.town_id]
        return {'health':person.health,'hunger':person.hunger,'thirst':person.thirst,'fatigue':round(person.fatigue,4),
            'food':e.items.count(person.id,'food'),'water':e.items.count(person.id,'water'),
            'money':person.money,'wage_credit':person.wage_credit,'position':asdict(person.position),
            'town_id':t.id,'town_food':e.items.count(t.id,'food'),'town_grain':e.items.count(t.id,'grain'),
            'town_wild_food':t.wild_food,'town_price':e.economy.price(t.id,'food'),
            'distance_market':distance(person.position,t.market),
            'starvation_hours':person.starvation_hours}


def summarize(deaths,counters):
    hungry=[d for d in deaths if d['record']['cause'] in ('hunger','both')]
    carried=[d for d in hungry if d['record']['food']>0]
    fresh=[d for d in carried if d['last_decision']['before']['food']==0 and
           d['last_decision']['after']['food']>0 and d['last_decision']['turn']==d['record']['turn']-1]
    prior=[d for d in carried if d['last_decision']['before']['food']>0]
    supplied=[d for d in hungry if d['at_death']['town_food']>0]
    affordable=[d for d in supplied if d['at_death']['money']>=d['at_death']['town_price']]
    return {'deaths':len(deaths),'hunger_or_both':len(hungry),
        'causes':dict(Counter(d['record']['cause'] for d in deaths)),
        'carrying_food':len(carried),'food_acquired_in_final_decision':len(fresh),
        'food_already_present_before_final_decision':len(prior),
        'prior_food_final_choices':dict(Counter(d['last_decision']['selected'] for d in prior)),
        'prior_food_ids':[d['id'] for d in prior],
        'hunger_with_food_in_home_market':len(supplied),'hunger_with_affordable_home_market':len(affordable),
        'hunger_at_market_and_affordable_food':sum(d['at_death']['distance_market']==0 for d in affordable),
        'hunger_while_food_existed_somewhere':sum(d['food_anywhere']>0 for d in hungry),
        'terminal_choices':dict(Counter(d['last_decision']['selected'] for d in hungry)),
        'terminal_execution_failures':dict(Counter(d['last_decision']['execution']['action'] for d in hungry
            if d['last_decision'].get('execution') and not d['last_decision']['execution']['success'])),
        'fresh_acquisition_health_before':dict(Counter(d['last_decision']['before']['health'] for d in fresh)),
        'counters':dict(counters)}


def run(mode):
    seed='Mira' if mode=='mundo' else 'Dovha'
    engine=Engine(generate_world(seed,'Auditor',with_player=mode=='jogador'))
    observer=HungerObserver(engine)
    if mode=='jogador':
        for line in (BASE/mode/'acoes.jsonl').open(encoding='utf-8'):
            action=json.loads(line)
            assert engine.world.turn==action['turn_before']
            result=engine.execute(action['command'])
            assert result.success==action['success'] and engine.world.turn==action['turn_after']
    else:
        for i in range(10000):
            engine.step()
            if (i+1)%2500==0:print(mode,i+1,flush=True)
    actual=hashlib.sha256(dumps(engine.world).encode('utf-8')).hexdigest()
    expected=hashlib.sha256((BASE/mode/'save_final.json').read_bytes()).hexdigest()
    assert actual==expected,(mode,actual,expected)
    assert {str(d['id']):d['record'] for d in observer.deaths}==json.loads((BASE/mode/'mortes_diagnostico.json').read_text())
    directory=OUT/mode;directory.mkdir(parents=True,exist_ok=True)
    with (directory/'casos.jsonl').open('w',encoding='utf-8') as stream:
        for d in observer.deaths:stream.write(json.dumps(d,ensure_ascii=False)+'\n')
    summary=summarize(observer.deaths,observer.counters)
    summary.update({'mode':mode,'seed':seed,'turns':10000,'replay_identical':True,'save_sha256':actual})
    (directory/'resumo.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in summary.items() if k!='counters'},ensure_ascii=False),flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mode',required=True,choices=('jogador','espectador','mundo'))
    run(parser.parse_args().mode)
