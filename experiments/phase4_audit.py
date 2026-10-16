"""Uma curta e uma única longa; registro causal sem três campanhas/replay longo."""
import argparse, gzip, hashlib, json, resource, time
from dataclasses import asdict
from pathlib import Path
from collections import Counter
from procedural import RULES_VERSION
from procedural.generation import generate_world, GenerationConfig
from procedural.engine import Engine
from procedural.persistence import dumps, loads
from procedural.validation import validate_world
from procedural.conflicts import ACTIONS

INTERESTING=ACTIONS|{'migrate','denounce','investigate','avoid_threat','stay_near','check_relative','seek_company','remember_relative','train','ask_personal_help'}
EVENTS={'ItemStolen','CharacterAttacked','CharacterKilled','CharacterDied','ConflictStarted','ConflictEnded',
'CharacterDefended','CharacterFled','CharacterWithdrew','CharacterSurrendered','CharacterCaptured','CharacterReleased',
'ProtectionGiven','FirstAidGiven','CharacterConfronted','CharacterThreatened','RestitutionDemanded','RestitutionGiven',
'CharacterWarned','CharacterInsulted','ApologyGiven','ImmediateHelpRequested','ThirdPartyAlerted','CalmingAttempted',
'ConflictForgiven','WantedIssued','PursuitSearch','PursuitEnded','SuspectLocated','MigrationStarted','MigrationArrived',
'ResidentMoved','PersonalityAdapted','GuardResponded','CrimeReported','ComfortGiven','PersonLocated','InformationShared',
'TrainingStarted','TrainingAbandoned','ProfessionChanged','SuccessionChanged','WorkerMaterialized',
'ThreatReported','InvestigationPerformed','ThreatAvoided','HelpGiven','ResponsibilityFulfilled'}

def core_hash():
 h=hashlib.sha256()
 for path in sorted(Path('procedural').glob('*.py')):h.update(path.name.encode());h.update(path.read_bytes())
 return h.hexdigest()

def snapshot(engine,start,elapsed):
 w=engine.world;alive=[c for c in w.characters.values() if c.alive]
 return {'turn':w.turn,'alive':len(alive),'dead':len(w.characters)-len(alive),
 'abstract':sum(t.abstract_population for t in w.towns.values()),'seconds':round(elapsed,3),
 'metrics':dict(w.metrics),'lod':dict(Counter(c.lod for c in alive)),
 'emotions':{k:{'mean':round(sum(getattr(c.emotions,k) for c in alive)/max(1,len(alive)),2),
                   'over50':sum(getattr(c.emotions,k)>=50 for c in alive),
                   'maximum':round(max((getattr(c.emotions,k) for c in alive),default=0),2)}
                 for k in ('anger','resentment','humiliation','desperation')},
 'grievances':sum(len(c.grievances) for c in alive),'injured':sum(c.combat.injured>=6 for c in alive),
 'memory_peak_mib':round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024,2),
 'invariants':validate_world(w)}

def run(hours,folder):
 folder=Path(folder);folder.mkdir(parents=True,exist_ok=True)
 if any((folder/name).exists() for name in ('resumo.json','save_final.json','progresso.json')):
  raise RuntimeError('Pasta contém campanha/checkpoint; recuperar evidências em vez de repetir a auditoria.')
 initial_core=core_hash()
 t=time.perf_counter();w=generate_world('Mira',with_player=False,config=GenerationConfig(historical_turns=0))
 engine=Engine(w);initial=snapshot(engine,0,0)
 people={str(i):{'name':c.name,'profession':c.profession,'town_id':c.town_id,'personality':asdict(c.personality),
                 'home':asdict(c.home),'money':c.money} for i,c in w.characters.items()}
 (folder/'personagens_iniciais.json').write_text(json.dumps(people,ensure_ascii=False),encoding='utf-8')
 (folder/'mapa_inicial.json').write_text(json.dumps({str(i):asdict(t) for i,t in w.towns.items()},ensure_ascii=False),encoding='utf-8')
 initial_metrics=dict(w.metrics);samples=[];event_count=0;decision_count=0
 # Detailed traces only for selected interaction needs. Audit-only observer;
 # does not alter RNG, world state, decisions, or save format.
 trace_last={}
 original_execute=engine.goals.execute
 decisions=gzip.open(folder/'decisoes.jsonl.gz','wt',encoding='utf-8')
 def observed_execute(character,goal,hours):
  nonlocal decision_count
  need=next((n for n in character.needs.values() if n.id==goal.need_id),None)
  key=(character.id,goal.action,goal.target_id,goal.need_id,need.context.get('source_event') if need else None)
  trace=goal.action in INTERESTING and (goal.action in ('attack','capture','flee','surrender','migrate','return_stolen')
        or w.turn-trace_last.get(key,-10000)>=24)
  if trace:
   trace_last[key]=w.turn
   alternatives=engine.goals.solutions(character,need) if need else []
   data={'turn':w.turn,'actor':character.id,'action':goal.action,'target':goal.target_id,
     'position':asdict(character.position),'health':character.health,'money':character.money,'hunger':character.hunger,
     'emotions':{k:getattr(character.emotions,k) for k in ('anger','resentment','humiliation','desperation','strain','adaptation','last_support')},'personality':asdict(character.personality),
     'need':asdict(need) if need else None,'score':goal.score,
     'known_source':asdict(character.knowledge[need.context['source_event']])
                    if need and need.context.get('source_event') in character.knowledge else None,
     'candidates':[{'action':s.action,'score':round(s.score,3),'target':s.target_id,'terms':s.considerations} for s in alternatives]}
   # Contexts carry growing diagnostic counters: retained for reconstruction,
   # but large emotional fact ledgers are unnecessary per decision.
   data['emotions'].pop('processed',None)
   decisions.write(json.dumps(data,ensure_ascii=False)+'\n');decision_count+=1
  return original_execute(character,goal,hours)
 engine.goals.execute=observed_execute
 with gzip.open(folder/'eventos.jsonl.gz','wt',encoding='utf-8') as events:
  def record(event):
   nonlocal event_count
   if event.kind in EVENTS:
    events.write(json.dumps(asdict(event),ensure_ascii=False)+'\n');event_count+=1
  engine.bus.subscribe('*',record)
  begin=time.perf_counter();last=begin
  for hour in range(1,hours+1):
   engine.step()
   if hour%1000==0:
    trace_last={key:turn for key,turn in trace_last.items() if w.turn-turn<=168}
   if hour%100==0 or hour==hours:
    errors=validate_world(w)
    if errors:
     (folder/'FALHA.json').write_text(json.dumps({'turn':w.turn,'errors':errors},ensure_ascii=False),encoding='utf-8')
     raise RuntimeError(str(errors[:6]))
    print(f'{hour}/{hours}h; vivos={sum(c.alive for c in w.characters.values())}; ataques={w.metrics.get("AttackExecuted",0)}; migrações={w.metrics.get("ResidentMoved",0)}; {time.perf_counter()-begin:.1f}s',flush=True)
   if hour%1000==0 or hour==hours:
    samples.append(snapshot(engine,0,time.perf_counter()-begin))
    (folder/'progresso.json').write_text(json.dumps(samples[-1],ensure_ascii=False),encoding='utf-8')
    (folder/'amostras.json').write_text(json.dumps(samples,ensure_ascii=False),encoding='utf-8')
  elapsed=time.perf_counter()-begin
 engine.bus.handlers['*'].remove(record)
 decisions.close()
 recorded_deaths=dict(w.death_records)
 recorded_wanted={i:asdict(r) for i,r in w.wanted_records.items()}
 emotion_causes=dict(sum((Counter(c.emotions.causes) for c in w.characters.values()),Counter()))
 if core_hash()!=initial_core:raise RuntimeError('O núcleo mudou durante a auditoria.')
 # Save/load benchmark and bounded exact continuation, not another 10k replay.
 ts=time.perf_counter();save=dumps(w);save_time=time.perf_counter()-ts
 (folder/'save_final.json').write_text(save,encoding='utf-8')
 ts=time.perf_counter();copy=loads(save);load_time=time.perf_counter()-ts
 engine.goals.execute=original_execute
 checkpoint_hash=hashlib.sha256(save.encode()).hexdigest()
 save_bytes=len(save.encode())
 del save
 ecopy=Engine(copy);engine.simulate(24);ecopy.simulate(24)
 continuation_equal=hashlib.sha256(dumps(w).encode()).digest()==hashlib.sha256(dumps(copy).encode()).digest()
 summary={'rules':RULES_VERSION,'seed':'Mira','mode':'global','hours':hours,'core_sha256':initial_core,
 'initial':initial,'samples':samples,'final':samples[-1],'metrics':{k:v-initial_metrics.get(k,0) for k,v in samples[-1]['metrics'].items()},
 'runtime_seconds':round(elapsed,3),'seconds_per_1000h':round(elapsed/hours*1000,3),
 'recorded_events':event_count,'recorded_decisions':decision_count,
 'save_bytes':save_bytes,'save_seconds':round(save_time,3),'load_seconds':round(load_time,3),
 'save_sha256':checkpoint_hash,'continuation_24h_equal':continuation_equal,
 'death_causes':dict(Counter(r['cause'] for r in recorded_deaths.values())),
 'emotion_causes':emotion_causes,
 'death_records':recorded_deaths,'wanted':recorded_wanted,
 'peak_after_persistence_mib':round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024,2)}
 (folder/'resumo.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
 if not continuation_equal:raise RuntimeError('Continuação de 24h divergiu; resumo/checkpoint foram preservados.')
 print(json.dumps({k:summary[k] for k in ('hours','runtime_seconds','seconds_per_1000h','save_bytes','death_causes','continuation_24h_equal')},ensure_ascii=False),flush=True)

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--hours',type=int,required=True);p.add_argument('--folder',required=True)
 args=p.parse_args();run(args.hours,args.folder)
