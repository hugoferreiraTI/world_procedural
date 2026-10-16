"""Reprodução integral de 10.000h para medir observações e validar determinismo."""
import argparse
from collections import Counter
import hashlib
import json
from dataclasses import asdict
from pathlib import Path

from experiments.feeding_audit import core_hash
from procedural.engine import Engine
from procedural.generation import generate_world
from procedural.persistence import dumps
from procedural.needs import FINISHED

ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'reports/fase_3_2'


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--mode',required=True,choices=('jogador','espectador','mundo'))
    mode=p.parse_args().mode;directory=OUT/'auditorias'/mode
    assert (directory/'save_final.json').exists()
    checksum=core_hash();assert checksum==json.loads((OUT/'manifesto_auditoria.json').read_text())['core_sha256']
    engine=Engine(generate_world('Mira' if mode=='mundo' else 'Dovha','Auditor',with_player=mode=='jogador'))
    engine.goals.debug=True
    counts=Counter();examples=[];context={};last_observation={};blocked_episodes=set();poverty=Counter()
    original_observe=engine.economy.observe
    def observe(person):
        previous=person.market_observation
        original_observe(person)
        current=person.market_observation
        if current is previous:return
        offers=current.get('temporary_offers',{})
        for service,offer in offers.items():
            key=person.id,service
            if last_observation.get(key)!=current.get('offers_observed_at'):
                last_observation[key]=current.get('offers_observed_at')
                counts['observed:'+service]+=1
                assert offer['capacity']>0
        if 'meal_distribution' in offers:
            town=engine.world.towns[person.town_id]
            assert engine.professions.temporary_capacity(town).get('meal_distribution',{}).get('capacity',0)>0
    engine.economy.observe=observe
    original_candidates=engine.personal_actions.candidates
    def candidates(person,need):
        choices=original_candidates(person,need)
        if need.kind in ('revenge','protection') and not need.context.get('reported'):
            guards=[i for i,o in person.observations.items() if o.alive and o.profession=='guarda']
            if guards and not any(engine.personal_actions.valid_report_recipient(person,need,i) for i in guards):
                known = need.context.get('source_event') in person.knowledge
                reason='no_independent_known_guard' if known else 'missing_report_evidence'
                key=reason,person.id,need.id,need.created_at,need.context.get('source_event')
                if key not in blocked_episodes:
                    blocked_episodes.add(key);counts['episodes:'+reason]+=1
                    if len(examples)<10:
                        examples.append({'turn':engine.world.turn,'npc_id':person.id,'name':person.name,
                                         'need_id':need.id,'block_reason':reason,'source_fact_known':known,
                                         'context':dict(need.context),'known_guard_ids':guards})
        return choices
    engine.personal_actions.candidates=candidates
    original_execute=engine.goals.execute
    def execute(person,goal,hours):
        observed=person.market_observation
        result=original_execute(person,goal,hours)
        service={'temporary_service':'meal_distribution','service_meal':'meal_distribution',
                 'work_for_food':'food_preparation','work_for_meal':'food_preparation'}.get(goal.action)
        if service:
            counts['executed:'+service]+=bool(result[0])
            if not result[0] and observed.get('temporary_offers',{}).get(service,{}).get('capacity',0)>0:
                counts['observed_offer_lost_before_execution:'+service]+=1
        return result
    engine.goals.execute=execute
    terminal=[]
    original_decide=engine.goals.decide
    def decide(person,elapsed=1):
        row=None
        if mode=='jogador' and person.id==520 and 8307<=engine.world.turn<=8310:
            row={'turn':engine.world.turn,'npc_id':person.id,'health':person.health,'hunger':person.hunger,
                 'thirst':person.thirst,'starvation_hours':person.starvation_hours,
                 'food':engine.items.count(person.id,'food'),'water':engine.items.count(person.id,'water')}
        original_decide(person,elapsed)
        if row is not None:
            row['goal_after']=asdict(person.goal) if person.goal else None
            row['trace']=engine.goals.traces.get(person.id)
            row['hunger_after_action']=person.hunger;row['thirst_after_action']=person.thirst
            terminal.append(row)
    engine.goals.decide=decide
    start=engine.world.turn
    if mode=='jogador':
        for line in (directory/'acoes.jsonl').read_text().splitlines():
            row=json.loads(line);assert engine.world.turn==row['turn_before']
            result=engine.execute(row['command'])
            assert result.success==row['success'] and engine.world.turn==row['turn_after']
    else:
        engine.simulate(10000)
    actual=hashlib.sha256(dumps(engine.world).encode()).hexdigest()
    expected=hashlib.sha256((directory/'save_final.json').read_bytes()).hexdigest()
    assert actual==expected,(mode,actual,expected)
    assert core_hash()==checksum and engine.world.turn-start==10000
    result={'mode':mode,'hours':10000,'final_checkpoint_identical':True,'save_sha256':actual,
            'observations_and_executions':dict(counts),'blocked_report_examples':examples,'terminal_dual_need_case':terminal,
            'method':'Reprodução integral com debug canônico, comandos públicos já registrados e observadores sem RNG adicional. Observações são atualizações locais, não vagas únicas.'}
    path=OUT/'reproducao_integral';path.mkdir(exist_ok=True)
    (path/f'{mode}.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(result,ensure_ascii=False))


if __name__=='__main__':main()
