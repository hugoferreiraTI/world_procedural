"""Auditoria fisiológica: campanha nova, observação sem recalcular decisões."""
import argparse,gzip,hashlib,heapq,json,resource,time
from collections import Counter,defaultdict
from dataclasses import asdict
from pathlib import Path
import procedural
from procedural.engine import Engine
from procedural.generation import GenerationConfig,generate_world
from procedural.persistence import dumps
from procedural.validation import validate_world

PLOTS={'ItemStolen','CharacterAttacked','CharacterKilled','CharacterDied','CharacterCaptured',
 'CharacterFled','CharacterSurrendered','FirstAidGiven','HelpGiven','ComfortGiven','RestitutionGiven',
 'MigrationStarted','MigrationArrived','ResidentMoved','SuccessionChanged','ProfessionChanged','ProtectionGiven'}

def core_hash():
    h=hashlib.sha256()
    for p in sorted(Path(procedural.__file__).parent.glob('*.py')):h.update(p.name.encode());h.update(p.read_bytes())
    return h.hexdigest()

def state(e,p):
    return {'hp':p.health,'hunger':p.hunger,'thirst':p.thirst,'food':e.items.count(p.id,'food'),
      'water':e.items.count(p.id,'water'),'position':asdict(p.position),
      'deprivation':getattr(p,'recoverable_deprivation_damage',None),'injured':p.combat.injured}

class Audit:
    def __init__(self,e,folder):
        self.e=e;self.w=e.world;self.folder=folder;self.alive_hours=0;self.meals=0;self.meal_hunger=0;self.meal_hp=0
        self.bands=Counter();self.consumption={};self.damage=Counter();self.healed=Counter();self.actions=Counter()
        self.crises=defaultdict(list);self.current_crisis={};self.low=[];self.last_low=set();self.windows=[]
        self.critical_attack=Counter();self.decisions=0;self.stack=[];self.events=gzip.open(folder/'eventos.jsonl.gz','wt',encoding='utf-8')
        self.traces=gzip.open(folder/'decisoes.jsonl.gz','wt',encoding='utf-8');self.samples=[];self.economy=[];self.negative=[]
        self.last_excerpt={};self.follow_recovered={};self.phy=e.needs.physiology;self.rest=e.needs.rest;self.execute=e.goals.execute
        e.needs.physiology=self.on_phy;e.needs.rest=self.on_rest;e.goals.execute=self.on_execute
        e.feeding.listeners.append(self.on_food);e.bus.subscribe('*',self.on_event)

    def on_food(self,row):
        if row['kind']=='FoodConsumed':self.consumption[row['npc_id']]=row

    def on_event(self,event):
        p=self.w.characters.get(event.actor_id)
        if event.kind=='FoodEaten':
            row=self.consumption.get(event.actor_id,{})
            hunger=row.get('hunger',p.hunger+40);hp=row.get('hp',p.health)
            self.meals+=1;self.meal_hunger+=hunger;self.meal_hp+=hp
            band='below30' if hunger<30 else '30-40' if hunger<40 else '40-60' if hunger<60 else '60-80' if hunger<80 else '80+'
            self.bands[band]+=1
            episodes=self.crises[event.actor_id]
            if episodes:
                episodes[-1]['meals']+=1
                if 'first_meal' not in episodes[-1]:
                    episodes[-1]['max_hp_after_meal']=hp
                episodes[-1].setdefault('first_meal',self.w.turn)
                episodes[-1].setdefault('hp_at_first_meal',hp)
            if p.hunger<90:self.current_crisis.pop(p.id,None)
        if event.kind in ('CharacterAttacked','CharacterKilled'):
            self.critical_attack['all']+=1
            if p and p.health<20:self.critical_attack['actor_hp_below20']+=1
        if event.kind in PLOTS or event.kind=='FoodEaten' and p and p.health<30:
            self.events.write(json.dumps(asdict(event),ensure_ascii=False)+'\n')
        for frame in self.stack:frame.append(event.id)

    def on_phy(self,p):
        before=p.health;old=p.hunger
        result=self.phy(p)
        actual=before-p.health
        if actual:
            origin='both' if p.hunger>=100 and p.thirst>=100 else 'hunger' if p.hunger>=100 else 'thirst'
            self.damage[origin]+=actual
        if p.hunger>=90 and old<90 and p.alive and p.health>0:
            previous=self.crises[p.id]
            if previous:previous[-1]['recurrence_at']=self.w.turn
            episode={'start':self.w.turn,'hp_start':p.health,'meals':0,'max_hp_after_meal':p.health,
              'deprivation_healed_after_meal':0,'physical_healed_after_meal':0}
            previous.append(episode);self.current_crisis[p.id]=episode
        return result

    def on_rest(self,p,hours=1):
        before=p.health;ledger=getattr(p,'recoverable_deprivation_damage',None)
        result=self.rest(p,hours)
        actual=p.health-before
        fast=(ledger-p.recoverable_deprivation_damage) if ledger is not None else 0
        self.healed['deprivation' if ledger is not None else 'unclassified']+=fast if ledger is not None else actual
        if ledger is not None:self.healed['physical']+=actual-fast
        if before<80<=p.health:self.follow_recovered[p.id]=self.w.turn+72
        episodes=self.crises[p.id]
        if episodes and 'first_meal' in episodes[-1]:
            episodes[-1]['max_hp_after_meal']=max(episodes[-1]['max_hp_after_meal'],p.health)
            episodes[-1]['deprivation_healed_after_meal']+=fast
            episodes[-1]['physical_healed_after_meal']+=actual-fast
        return result

    def on_execute(self,p,goal,hours):
        before=state(self.e,p);need=next((n for n in p.needs.values() if n.id==goal.need_id),None)
        frame=[];self.stack.append(frame)
        try:
            result=self.execute(p,goal,hours)
            if len(self.stack)==1:
                self.actions[goal.action+':'+str(result[0])]+=1;self.decisions+=1
                key=(p.id,goal.action,need.id if need else None)
                trace=(before['hp']<30 or need and need.kind=='recovery' or goal.action in ('attack','migrate','seek_treatment','first_aid')
                       or self.follow_recovered.get(p.id,-1)>=self.w.turn)
                if trace and (before['hp']<30 or self.w.turn-self.last_excerpt.get(key,-9999)>=24):
                    self.last_excerpt[key]=self.w.turn
                    self.traces.write(json.dumps({'turn':self.w.turn,'actor':p.id,'action':goal.action,
                      'need':asdict(need) if need else None,'before':before,'after':state(self.e,p),
                      'success':result[0],'outcome':result[1],'event_ids':frame},ensure_ascii=False)+'\n')
            return result
        finally:self.stack.pop()

    def after_hour(self):
        now=self.w.turn;alive=[p for p in self.w.characters.values() if p.alive]
        current_low={p.id for p in alive if p.health<30}
        for pid in current_low-self.last_low:
            p=self.w.characters[pid];entry={'person':pid,'turn':now,'entry':state(self.e,p),'windows':{}}
            self.low.append(entry);index=len(self.low)-1
            for horizon in (24,48,72):heapq.heappush(self.windows,(now+horizon,index,horizon))
        self.last_low=current_low
        while self.windows and self.windows[0][0]<=now:
            _,index,horizon=heapq.heappop(self.windows);entry=self.low[index];p=self.w.characters[entry['person']]
            category='dead' if not p.alive else 'below30' if p.health<30 else '30-50' if p.health<50 else '50-70' if p.health<=70 else 'above70'
            entry['windows'][str(horizon)]={'category':category,'state':state(self.e,p)}
        if now%24==0:
            cities=list(self.w.towns.values());prices=[self.e.economy.price(t.id,'food') for t in cities]
            self.economy.append({'turn':now,'food_stock':sum(self.e.items.count(t.id,'food') for t in cities),
              'empty_markets':sum(self.e.items.count(t.id,'food')==0 for t in cities),'towns':len(cities),
              'mean_price':sum(prices)/len(prices),'food_produced_cumulative':sum(t.production_total.get('food',0) for t in cities)})
        if now%100==0:
            self.last_excerpt={k:t for k,t in self.last_excerpt.items() if now-t<=168}
            errors=validate_world(self.w)
            if errors:self.negative+=errors;raise RuntimeError(str(errors[:5]))
            self.events.flush();self.traces.flush()
        if now%100==0:
            self.samples.append({'turn':now,'alive':len(alive),'dead':len(self.w.death_records),
              'meals':self.meals,'alive_hours':self.alive_hours,'mean_meal_hunger':self.meal_hunger/max(1,self.meals),
              'mean_meal_hp':self.meal_hp/max(1,self.meals),'meal_bands':dict(self.bands),'damage':dict(self.damage),
              'healed':dict(self.healed),'mean_hp':sum(p.health for p in alive)/max(1,len(alive)),
              'hp_below30':len(current_low),'mean_desperation':sum(p.emotions.desperation for p in alive)/max(1,len(alive)),
              'food_deaths':sum(d['cause'] in ('hunger','both') for d in self.w.death_records.values()),
              'combat_deaths':sum(d['cause']=='combat' for d in self.w.death_records.values()),
              'recovery_selected':self.w.metrics.get('NeedSelected:recovery',0)})
            (self.folder/'progresso.json').write_text(json.dumps(self.samples[-1],ensure_ascii=False))
            print(json.dumps(self.samples[-1],ensure_ascii=False),flush=True)

    def finish(self):
        self.events.close();self.traces.close()
        self.w.metrics['Audit:RationsPerPersistentNpcDay']=self.meals/(self.alive_hours/24)
        return {'meals':self.meals,'alive_hours':self.alive_hours,'rations_per_persistent_npc_day':self.meals/(self.alive_hours/24),
          'meal_bands':dict(self.bands),'mean_meal_hunger':self.meal_hunger/max(1,self.meals),
          'mean_meal_hp':self.meal_hp/max(1,self.meals),'damage_observed':dict(self.damage),'rest_healing_observed':dict(self.healed),
          'critical_attacks':dict(self.critical_attack),'root_actions':dict(self.actions),'samples':self.samples,'economy':self.economy,
          'low_hp_episodes':len(self.low),'low_hp_window_counts':{str(h):dict(Counter(e['windows'][str(h)]['category'] for e in self.low if str(h) in e['windows'])) for h in (24,48,72)},
          'censored_windows':len(self.windows),'crisis_people':sum(bool(v) for v in self.crises.values()),
          'crisis_count':sum(len(v) for v in self.crises.values()),'repeat_crisis_people':sum(len(v)>1 for v in self.crises.values()),
          'crises_with_meal_and_hp_improvement':sum('hp_at_first_meal' in e and e['max_hp_after_meal']>e['hp_at_first_meal'] for v in self.crises.values() for e in v),
          'crises_with_meal_and_recorded_healing':sum(e['deprivation_healed_after_meal']+e['physical_healed_after_meal']>0 for v in self.crises.values() for e in v),
          'invariants':self.negative}

def run(seed,hours,folder):
    folder=Path(folder);folder.mkdir(parents=True,exist_ok=True)
    if any(folder.iterdir()):raise RuntimeError('Não sobrescrever campanhas.')
    frozen=core_hash();world=generate_world(seed,with_player=False,config=GenerationConfig(historical_turns=0));engine=Engine(world)
    initial={'persistent':len(world.characters),'abstract':sum(t.abstract_population for t in world.towns.values()),'towns':len(world.towns),'kingdoms':len(world.kingdoms)}
    initial_metrics=dict(world.metrics);audit=Audit(engine,folder);start=time.perf_counter()
    (folder/'manifesto.json').write_text(json.dumps({'seed':seed,'hours':hours,'rules':procedural.RULES_VERSION,'core_sha256':frozen,'loaded_save':False,'historical_turns':0,'initial':initial},ensure_ascii=False,indent=2))
    for _ in range(hours):
        audit.alive_hours+=sum(p.alive for p in world.characters.values());engine.step();audit.after_hour()
    summary=audit.finish()
    if core_hash()!=frozen:raise RuntimeError('Núcleo mudou durante campanha.')
    summary.update(seed=seed,hours=hours,rules=procedural.RULES_VERSION,core_sha256=frozen,initial=initial,
      runtime_seconds=time.perf_counter()-start,metrics={k:v-initial_metrics.get(k,0) for k,v in world.metrics.items()},
      death_causes=dict(Counter(d['cause'] for d in world.death_records.values())),death_records=world.death_records,
      alive=sum(p.alive for p in world.characters.values()),loaded_save=False,
      memory_peak_mib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024)
    summary['food_carried_deaths']=[{'person':i,**d} for i,d in world.death_records.items() if d['cause'] in ('hunger','both') and d['food']>0]
    (folder/'crises_por_npc.json').write_text(json.dumps(audit.crises,ensure_ascii=False))
    (folder/'janelas_recuperacao.json').write_text(json.dumps(audit.low,ensure_ascii=False))
    (folder/'personagens.json').write_text(json.dumps({i:{'name':p.name,'alive':p.alive,'profession':p.profession,'town_id':p.town_id,
        'state':state(engine,p),'damage_by_origin':getattr(p,'damage_by_origin',{}),
        'despair_sources':getattr(p.emotions,'despair_sources',{}),'desperation':p.emotions.desperation} for i,p in world.characters.items()},ensure_ascii=False))
    (folder/'resumo.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2))
    (folder/'save_final.json').write_text(dumps(world))
    print('CONCLUÍDO '+json.dumps({'hours':hours,'rules':procedural.RULES_VERSION,'deaths':summary['death_causes'],'rations_per_npc_day':summary['rations_per_persistent_npc_day']},ensure_ascii=False),flush=True)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--seed',default='Vespera-47');parser.add_argument('--hours',type=int,required=True);parser.add_argument('--folder',required=True)
    args=parser.parse_args();run(args.seed,args.hours,args.folder)
