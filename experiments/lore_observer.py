"""Observação de mundo novo: não importa nem carrega saves.

O observador registra resultados de avaliações já feitas pelo motor. Nunca
reavalia utility, muda o RNG ou executa ações adicionais.
"""
import argparse,gzip,hashlib,json,resource,time
from collections import Counter
from dataclasses import asdict
from pathlib import Path
from procedural import RULES_VERSION
from procedural.engine import Engine
from procedural.generation import GenerationConfig,generate_world
from procedural.persistence import dumps
from procedural.validation import validate_world
from experiments.phase4_audit import EVENTS,INTERESTING,core_hash,snapshot

PLOT_EVENTS=EVENTS|{'FamilyConcern','FamilySearch','AbsenceNoticed','RemainsLocated','Remembrance',
                  'ProfessionChanged','LocalEconomicResponse','FoodShortage'}
PLOT_ACTIONS=INTERESTING|{'steal','steal_meal','secure','give_supplies','seek_company','remember_relative'}
CAUSAL_KINDS={'ItemStolen','CharacterAttacked','CharacterKilled','CharacterDied','CharacterCaptured',
 'CharacterThreatened','CharacterInsulted','RestitutionDemanded','ApologyGiven','RestitutionGiven',
 'WantedIssued','PersonLocated','RemainsLocated','ProtectionGiven','ComfortGiven','FirstAidGiven'}
CONTEXT_KEYS={'source_event','originating_fact','record_id','threat','victim','protected','culprit',
 'known_location','stolen_fact','confidence','relationship','family','loss','mode','last_seen',
 'destination','reason','travel_hours','money_target','low_money_hours','known_location','resolution'}

def need_data(n):
    if n is None:return None
    return {'id':n.id,'kind':n.kind,'target_id':n.target_id,'priority':n.priority,
       'base_urgency':n.base_urgency,'source':n.source,'reason':n.reason,'status':n.status,
       'created_at':n.created_at,'expires_at':n.expires_at,
       'context':{k:v for k,v in n.context.items() if k in CONTEXT_KEYS}}

class Observer:
    def __init__(self,engine,folder):
        self.e=engine;self.w=engine.world;self.folder=folder
        self.events=gzip.open(folder/'eventos.jsonl.gz','wt',encoding='utf-8')
        self.decisions=gzip.open(folder/'decisoes.jsonl.gz','wt',encoding='utf-8')
        self.reactions=gzip.open(folder/'reacoes.jsonl.gz','wt',encoding='utf-8')
        self.event_counts=Counter();self.action_counts=Counter();self.anomalies=Counter();self.examples={}
        self.last_trace={};self.last_reaction={};self.evaluations={};self.stack=[];self.decision_count=0;self.reaction_count=0
        self.evaluate=engine.goals._evaluate;self.execute=engine.goals.execute
        engine.goals._evaluate=self.on_evaluate;engine.goals.execute=self.on_execute
        engine.bus.subscribe('*',self.on_event);engine.knowledge.listeners.append(self.on_fact)

    def issue(self,kind,data):
        self.anomalies[kind]+=1
        examples=self.examples.setdefault(kind,[])
        if len(examples)<12:examples.append({'turn':self.w.turn,**data})

    def on_evaluate(self,person,need,choices):
        result=self.evaluate(person,need,choices)
        if any(c.action in PLOT_ACTIONS for c in result):
            self.evaluations[person.id,need.id]=(self.w.turn,[
              {'action':c.action,'target':c.target_id,'score':c.score,'terms':dict(c.considerations)} for c in result[:8]])
        return result

    def own_state(self,p):
        return {'health':p.health,'money':p.money,'food':self.e.items.count(p.id,'food'),
           'water':self.e.items.count(p.id,'water'),'hunger':p.hunger,'thirst':p.thirst,
           'position':asdict(p.position),'alive':p.alive}

    def on_execute(self,p,goal,hours):
        n=next((n for n in p.needs.values() if n.id==goal.need_id),None)
        key=(p.id,goal.action,goal.target_id,goal.need_id,n.context.get('source_event') if n else None)
        always=goal.action in {'attack','capture','flee','surrender','migrate','return_stolen','steal','steal_meal','steal_person','secure'}
        trace=goal.action in PLOT_ACTIONS and (always or self.w.turn-self.last_trace.get(key,-9999)>=24)
        frame=[];self.stack.append(frame)
        data=None
        if trace:
            self.last_trace[key]=self.w.turn
            source=n.context.get('source_event') if n else None
            if source is None and n and n.source.startswith('event:'):
                try:source=int(n.source.split(':')[1])
                except ValueError:pass
            known=p.knowledge.get(source)
            evaluated=self.evaluations.get((p.id,n.id if n else None))
            data={'turn':self.w.turn,'actor':p.id,'action':goal.action,'target':goal.target_id,
              'depth':len(self.stack)-1,'goal_id':goal.id,'goal_created_at':goal.created_at,
              'goal_score':goal.score,'need':need_data(n),'before':self.own_state(p),
              'emotions':{k:getattr(p.emotions,k) for k in ('anger','resentment','humiliation','desperation')},
              'personality':asdict(p.personality),'known_source':asdict(known) if known else None,
              'source_event_id':source,'candidate_evaluation_turn':evaluated[0] if evaluated else None,
              'candidates':evaluated[1] if evaluated else [],
              'active_needs':[need_data(x) for x in sorted(p.needs.values(),key=lambda x:-x.priority)
                if x.status not in ('satisfied','expired')][:8]}
            target=self.w.characters.get(goal.target_id)
            if target:
                data['objective_target_before']={'alive':target.alive,'health':target.health,
                  'position':asdict(target.position),'surrender_until':target.combat.surrendered_until,
                  'detention_until':target.combat.detention_until}
                observation=p.observations.get(target.id)
                data['perceived_target']=asdict(observation) if observation else None
            if n and n.kind=='pursuit':
                r=self.e.justice.record_for(p,goal.target_id)
                if r and n.context.get('record_id')!=r.id:self.issue('pursuit_case_mismatch',{'actor':p.id,'need':need_data(n),'execution_record':r.id})
        try:
            result=self.execute(p,goal,hours)
            self.action_counts[goal.action+(':'+str(result[0]))]+=1
            if data:
                data.update(success=result[0],outcome=result[1],after=self.own_state(p),event_ids=list(frame))
                self.decisions.write(json.dumps(data,ensure_ascii=False)+'\n');self.decision_count+=1
            return result
        finally:self.stack.pop()

    def on_fact(self,p,fact):
        if fact.kind not in CAUSAL_KINDS:return
        related=[need_data(n) for n in p.needs.values() if n.context.get('source_event')==fact.event_id]
        if not related:return
        key=p.id,fact.event_id,fact.confidence
        if key in self.last_reaction:return
        self.last_reaction[key]=self.w.turn
        self.reactions.write(json.dumps({'learned_at':self.w.turn,'person':p.id,'fact':asdict(fact),
           'needs':related,'emotions':{k:getattr(p.emotions,k) for k in ('anger','resentment','humiliation','desperation')},
           'kin_of_victim':fact.target_id in self.e.needs.personal.kin.get(p.id,())},ensure_ascii=False)+'\n')
        self.reaction_count+=1

    def on_event(self,event):
        if event.kind not in PLOT_EVENTS:return
        self.events.write(json.dumps(asdict(event),ensure_ascii=False)+'\n');self.event_counts[event.kind]+=1
        for frame in self.stack:frame.append(event.id)
        if event.kind in ('CharacterAttacked','CharacterKilled') and event.actor_id==event.target_id:
            self.issue('self_attack',{'event':asdict(event)})
        if event.kind=='ResidentMoved':
            p=self.w.characters[event.actor_id]
            old=event.context['origin']
            relation=self.e.graph.value(p.id,old,'residente_de')
            if relation>0:self.issue('old_residence_relationship',{'event_id':event.id,'person':p.id,
                'old_town':old,'new_town':p.town_id,'old_relation_value':relation,
                'new_relation_value':self.e.graph.value(p.id,p.town_id,'residente_de'),
                'new_other_label_value':self.e.graph.value(p.id,p.town_id,'reside_em')})

    def checkpoint(self):
        self.last_trace={k:t for k,t in self.last_trace.items() if self.w.turn-t<=168}
        self.last_reaction={k:t for k,t in self.last_reaction.items() if self.w.turn-t<=168}
        self.evaluations={k:v for k,v in self.evaluations.items() if self.w.turn-v[0]<=24}
        canonical={(r.jurisdiction,r.suspect_id):r.id for r in self.w.wanted_records.values()
          if r.status=='active' and self.w.turn-r.created_at<=168}
        if canonical!=self.e.justice.active:self.issue('justice_index_mismatch',{'expected':str(canonical),'actual':str(self.e.justice.active)})
        for f in (self.events,self.decisions,self.reactions):f.flush()

    def close(self):
        self.e.goals._evaluate=self.evaluate;self.e.goals.execute=self.execute
        self.e.bus.handlers['*'].remove(self.on_event);self.e.knowledge.listeners.remove(self.on_fact)
        for f in (self.events,self.decisions,self.reactions):f.close()

def metadata(w):
    return {str(i):{'name':p.name,'profession':p.profession,'town_id':p.town_id,'home':asdict(p.home),
       'personality':asdict(p.personality),'money':p.money,'origin':p.origin,
       'family':[r.target_id for r in w.relationships.values() if r.source_id==i and r.value>0
          and r.kind in ('casamento','pai_de','filho_de')]} for i,p in w.characters.items()}

def run(seed,hours,folder):
    folder=Path(folder);folder.mkdir(parents=True,exist_ok=True)
    if any(folder.iterdir()):raise RuntimeError('Diretório de resultados deve estar vazio.')
    frozen=core_hash();w=generate_world(seed,with_player=False,config=GenerationConfig(historical_turns=0))
    e=Engine(w);initial=snapshot(e,0,0);initial_metrics=dict(w.metrics)
    (folder/'personagens_iniciais.json').write_text(json.dumps(metadata(w),ensure_ascii=False))
    (folder/'cidades_iniciais.json').write_text(json.dumps({i:asdict(t) for i,t in w.towns.items()},ensure_ascii=False))
    (folder/'reinos_iniciais.json').write_text(json.dumps({i:asdict(k) for i,k in w.kingdoms.items()},ensure_ascii=False))
    (folder/'manifesto.json').write_text(json.dumps({'seed':seed,'hours':hours,'rules':RULES_VERSION,
      'core_sha256':frozen,'start':'generate_world, historical_turns=0, with_player=False',
      'loaded_save':False,'purpose':'Relatório de lore, incongruências e melhorias; núcleo não é alterado.'},ensure_ascii=False,indent=2))
    observer=Observer(e,folder);samples=[];begin=time.perf_counter()
    for hour in range(1,hours+1):
        e.step()
        if hour%100==0 or hour==hours:
            observer.checkpoint();errors=validate_world(w)
            progress={'turn':w.turn,'alive':sum(p.alive for p in w.characters.values()),
              'attacks':w.metrics.get('AttackExecuted',0),'deaths':dict(Counter(r['cause'] for r in w.death_records.values())),
              'migrations':w.metrics.get('ResidentMoved',0),'seconds':round(time.perf_counter()-begin,2),
              'invariants':errors,'anomalies':dict(observer.anomalies)}
            (folder/'progresso.json').write_text(json.dumps(progress,ensure_ascii=False))
            print(json.dumps(progress,ensure_ascii=False),flush=True)
            if errors:raise RuntimeError(str(errors[:6]))
        if hour%500==0 or hour==hours:
            s=snapshot(e,0,time.perf_counter()-begin)
            s['applied_fact_entries']=sum(len(p.applied_facts) for p in w.characters.values())
            s['reputation_entries']=sum(len(p.reputations) for p in w.characters.values())
            s['wanted_records']=len(w.wanted_records)
            samples.append(s);(folder/'amostras.json').write_text(json.dumps(samples,ensure_ascii=False))
    observer.close()
    if core_hash()!=frozen:raise RuntimeError('Núcleo mudou durante observação.')
    finalpeople={i:{'name':p.name,'alive':p.alive,'profession':p.profession,'town_id':p.town_id,
       'money':p.money,'wage_credit':p.wage_credit,'food':e.items.count(p.id,'food'),'hunger':p.hunger,
       'thirst':p.thirst,'health':p.health,'position':asdict(p.position),'emotions':asdict(p.emotions),
       'injury':p.combat.injured,'migration':asdict(p.migration) if p.migration else None,
       'active_needs':[need_data(n) for n in p.needs.values() if n.status not in ('satisfied','expired')],
       'reputations':{i:asdict(r) for i,r in p.reputations.items()},
       'grievances':{i:asdict(g) for i,g in p.grievances.items()}} for i,p in w.characters.items()}
    (folder/'personagens_finais.json').write_text(json.dumps(finalpeople,ensure_ascii=False))
    (folder/'cidades_finais.json').write_text(json.dumps({i:asdict(t) for i,t in w.towns.items()},ensure_ascii=False))
    (folder/'reinos_finais.json').write_text(json.dumps({i:asdict(k) for i,k in w.kingdoms.items()},ensure_ascii=False))
    summary={'seed':seed,'rules':RULES_VERSION,'hours':hours,'core_sha256':frozen,'initial':initial,
       'final':samples[-1],'samples':samples,'runtime_seconds':round(time.perf_counter()-begin,3),
       'metrics':{k:v-initial_metrics.get(k,0) for k,v in w.metrics.items()},
       'events':dict(observer.event_counts),'actions':dict(observer.action_counts),
       'decision_records':observer.decision_count,'reaction_records':observer.reaction_count,
       'death_records':w.death_records,'death_causes':dict(Counter(r['cause'] for r in w.death_records.values())),
       'anomaly_counts':dict(observer.anomalies),'anomaly_examples':observer.examples,
       'wanted_status':dict(Counter(r.status for r in w.wanted_records.values())),
       'emotion_fact_causes':dict(sum((Counter(p.emotions.causes) for p in w.characters.values()),Counter())),
       'loaded_save':False,'kingdoms':len(w.kingdoms),'towns':len(w.towns)}
    # Exportação final é escrita; a sessão inteira nasce da geração e não usa load.
    t=time.perf_counter();save=dumps(w);summary['save_seconds']=round(time.perf_counter()-t,3)
    summary['save_bytes']=len(save.encode());(folder/'save_final.json').write_text(save)
    (folder/'resumo.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2))
    print('CONCLUÍDO: '+json.dumps({k:summary[k] for k in ('seed','hours','death_causes','anomaly_counts')},ensure_ascii=False),flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--seed',required=True);p.add_argument('--hours',type=int,default=5000);p.add_argument('--folder',required=True)
    a=p.parse_args();run(a.seed,a.hours,a.folder)
