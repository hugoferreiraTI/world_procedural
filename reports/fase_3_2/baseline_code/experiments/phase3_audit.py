"""Auditoria da fase 3, reutilizando políticas e observadores das fases anteriores."""
import argparse
from collections import Counter
from copy import deepcopy
from dataclasses import asdict
import hashlib
import json
from pathlib import Path
from experiments.phase2_audit import Audit
from experiments.perspective_audit import WorldAudit,write_json
from experiments.player_audit import run as player_run,money
from procedural.engine import Engine
from procedural.generation import generate_world
from procedural.persistence import JsonRepository,dumps
from procedural.validation import validate_world

ECONOMIC_EVENTS={'LocalEconomicResponse','TemporaryWorkPerformed','TrainingStarted','TrainingProgress',
                 'TrainingAbandoned','ProfessionChanged','WorkerMaterialized'}


def snapshot(engine):
    world=engine.world
    people=[c for c in world.characters.values() if not c.is_player]
    alive=[c for c in people if c.alive]
    towns=[]
    for t in world.towns.values():
        report=engine.economy.food_diagnosis(t)
        towns.append({'id':t.id,'name':t.name,'population':engine.population.counts(t),
                      'report':report,'professional_demand':deepcopy(t.professional_demand),
                      'production_total':dict(t.production_total),'money':t.money,
                      'abstract_money':t.abstract_money,'grain_credit':t.grain_credit})
    empty=[t for t in towns if t['report']['stock']['food']==0]
    return {'turn':world.turn,'summary':{
        'alive':len(alive),'dead':sum(not c.alive for c in people),'empty_food':len(empty),
        'empty_food_full_grain':sum(t['report']['stock']['grain']>=240 for t in empty),
        'empty_food_live_cook':sum(t['report']['cook_count']>0 for t in empty),
        'empty_food_no_cook':sum(t['report']['cook_count']==0 for t in empty),
        'poor_below_one_meal':sum(c.money<engine.economy.price(c.town_id,'food') for c in alive),
        'poor_below_10':sum(c.money<10 for c in alive),
        'hunger_70':sum(c.hunger>=70 for c in alive),'thirst_70':sum(c.thirst>=70 for c in alive),
        'hunger_85':sum(c.hunger>=85 for c in alive),'thirst_85':sum(c.thirst>=85 for c in alive),
        'localities_functionally_empty':sum(not any(c.alive and c.position.map_id==t.id for c in people) for t in world.towns.values()),
        'kingdoms_without_ruler':sum(k.ruler_id is None for k in world.kingdoms.values()),
        'known_water_sources':sum(any(k.startswith('well') or k=='market' for k in c.known_places) for c in alive),
        'professional_deficits':sum(t['report']['professional_deficit'] for t in towns)},'towns':towns}


class Phase3Audit:
    def __init__(self,directory,mode):
        self.directory,self.mode=directory,mode
        self.delegate=Audit(directory) if mode=='jogador' else WorldAudit(directory,mode)
        self.initial=None;self.start=None;self.frames=[]
        self.initial_production={};self.engine=None
        self.events=(directory/'economia_eventos.jsonl').open('w',encoding='utf-8')
        self.last_frame=None
        self.initial_ids=set()
        self.completed_existing=0

    def __call__(self,engine):
        self.delegate(engine);self.engine=engine
        if self.initial is None:
            self.initial_ids=set(engine.world.characters)
            self.initial=dict(engine.world.metrics);self.start=engine.world.turn
            self.initial_production={t.id:dict(t.production_total) for t in engine.world.towns.values()}
            engine.bus.subscribe('*',self.on_event)
        elapsed=engine.world.turn-self.start
        if elapsed%250==0 and elapsed!=self.last_frame:
            self.frames.append(snapshot(engine));self.last_frame=elapsed

    def on_event(self,event):
        if event.kind == 'ProfessionChanged' and event.actor_id in self.initial_ids:
            self.completed_existing += 1
        if event.kind in ECONOMIC_EVENTS:
            self.events.write(json.dumps(asdict(event),ensure_ascii=False)+'\n')

    def finish(self,report):
        self.events.close();self.delegate.finish(report)
        world=JsonRepository().load(self.directory/'save_final.json');engine=Engine(world)
        final=snapshot(engine)
        metrics={key:value-self.initial.get(key,0) for key,value in world.metrics.items()}
        records={str(i):r for i,r in world.death_records.items() if r['turn']>=self.start}
        deaths=Counter(r['cause'] for r in records.values())
        result={'mode':self.mode,'seed':world.seed,'rules_version':world.rules_version,'turns':world.turn-self.start,
            'start_turn':self.start,'final':final,'metrics':metrics,'death_conditions':dict(deaths),
            'deaths_carrying_food':sum(r['food']>0 for r in records.values()),
            'deaths_carrying_water':sum(r['water']>0 for r in records.values()),
            'professionals_dead':dict(Counter(r['profession'] for r in records.values())),
            'workers_retrained':self.completed_existing,'workers_trained':metrics.get('ProfessionChanged',0),
            'workers_materialized':metrics.get('WorkerMaterialized',0),
            'average_closed_vacancy_hours':metrics.get('VacancyHours',0)/metrics['VacancyClosed'] if metrics.get('VacancyClosed') else None,
            'personal_outcomes':{k:v for k,v in metrics.items() if k.startswith('PersonalOutcome:')},
            'production_by_locality':{str(t.id):{kind:amount-self.initial_production.get(t.id,{}).get(kind,0)
                for kind,amount in t.production_total.items()} for t in world.towns.values()},
            'save_sha256':hashlib.sha256((self.directory/'save_final.json').read_bytes()).hexdigest()}
        write_json(self.directory/'metricas_fase3.json',result)
        write_json(self.directory/'mortes_diagnostico.json',records)
        write_json(self.directory/'quadros_economicos.json',self.frames)
        write_json(self.directory/'diagnosticos_pessoais_finais.json',world.decision_diagnostics)
        print(json.dumps({'mode':self.mode,**final['summary'],'retrained':result['workers_retrained'],
            'materialized':result['workers_materialized'],'death_conditions':dict(deaths)},ensure_ascii=False),flush=True)


def run(seed,turns,directory,mode):
    directory.mkdir(parents=True,exist_ok=True)
    audit=Phase3Audit(directory,mode)
    if mode=='jogador':
        report=player_run(seed,turns,directory,observer=audit)
    else:
        import time
        started=time.monotonic();engine=Engine(generate_world(seed,with_player=False));world=engine.world
        start=world.turn;initial_money=money(world);initial_source=world.metrics.get('MoneySourceAbstractWork',0)
        audit(engine);checkpoints=[]
        for elapsed in range(1,turns+1):
            engine.step();audit(engine)
            if elapsed%1000==0 or elapsed==turns:
                errors=validate_world(world)
                balance=money(world)-initial_money-world.metrics.get('MoneySourceAbstractWork',0)+initial_source
                point={'elapsed':elapsed,'turn':world.turn,'validation_errors':errors,'money_balance_difference':balance,
                       'alive_npcs':sum(c.alive for c in world.characters.values())}
                checkpoints.append(point);print(json.dumps(point,ensure_ascii=False),flush=True)
                if errors or balance: raise AssertionError(point)
                if elapsed in (1000,5000): JsonRepository().save(world,directory/f'save_{elapsed}.json')
        JsonRepository().save(world,directory/'save_final.json')
        report={'mode':mode,'seed':seed,'rules_version':world.rules_version,'start_turn':start,
                'actual_turns':world.turn-start,'checkpoints':checkpoints,'seconds':round(time.monotonic()-started,2)}
        write_json(directory/'relatorio.json',report)
    audit.finish(report)
    return report


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--seed',default='Dovha');parser.add_argument('--turnos',type=int,default=10000)
    parser.add_argument('--mode',choices=('jogador','espectador','mundo'),required=True)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    if args.turnos<=0: parser.error('Turnos deve ser positivo.')
    run(args.seed,args.turnos,args.output,args.mode)
