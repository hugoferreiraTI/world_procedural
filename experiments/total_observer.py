"""Perfil externo: sem monkeypatch, decisões extras, RNG ou fatos novos."""
import argparse
import dataclasses
import hashlib
import importlib
import inspect
import json
import statistics
import sys
import time
import types
from collections import Counter,defaultdict,deque
from pathlib import Path

from procedural.generation import generate_world,GenerationConfig
from procedural.engine import Engine
from procedural.persistence import dumps,JsonRepository
from procedural.validation import validate_world
from procedural.feeding import MEALS,ACQUISITIONS
from .total_static import ROOT,OUT,fingerprint,jwrite

SEED='Thalven-Radiografia55'
HOURS=300
def plain(v,depth=0):
 if depth>9:return '<profundidade omitida>'
 if dataclasses.is_dataclass(v):return {f.name:plain(getattr(v,f.name),depth+1) for f in dataclasses.fields(v)}
 if isinstance(v,dict):return {str(k):plain(x,depth+1) for k,x in v.items()}
 if isinstance(v,(list,tuple,set,deque)):return [plain(x,depth+1) for x in v]
 if v is None or isinstance(v,(str,int,float,bool)):return v
 return '<'+type(v).__name__+'>'
def pos(p):return {'map_id':p.map_id,'x':p.x,'y':p.y} if p else None
def dist(values):
 a=sorted(values)
 if not a:return {'n':0}
 def q(p):
  x=(len(a)-1)*p;i=int(x);j=min(i+1,len(a)-1);return round(a[i]+(a[j]-a[i])*(x-i),4)
 return {'n':len(a),'min':a[0],'p25':q(.25),'median':q(.5),'mean':round(statistics.mean(a),4),'p75':q(.75),'p90':q(.9),'max':a[-1]}
def codes():
 result={}
 def add(code,module):
  if '/procedural/' not in code.co_filename:return
  if not code.co_name.startswith('<'):result[code]=f"{module}.{code.co_qualname.replace('.<locals>','')}"
  for c in code.co_consts:
   if isinstance(c,types.CodeType):add(c,module)
 for path in (ROOT/'procedural').glob('*.py'):
  module=importlib.import_module('procedural.'+path.stem)
  for obj in vars(module).values():
   if inspect.isfunction(obj) and obj.__module__.startswith('procedural.'):
    add(obj.__code__,obj.__module__.rsplit('.',1)[-1])
   elif inspect.isclass(obj) and obj.__module__==module.__name__:
    for fn in vars(obj).values():
     if isinstance(fn,(staticmethod,classmethod)):fn=fn.__func__
     if isinstance(fn,property):fn=fn.fget
     if inspect.isfunction(fn):add(fn.__code__,path.stem)
 return result

KINDS={
 'food':'food','food_reserve':'food','water':'water','rest':'rest','recovery':'recovery',
 'money':'money','work':'work','advancement':'career','professional':'career','family':'family','grief':'family',
 'revenge':'crime','protection':'combat','response':'combat','assistance':'combat','security':'justice','pursuit':'investigation',
 'investigation':'investigation','status':'social','recognition':'social','affiliation':'faction','organizational_access':'faction',
 'organizational_base':'faction','organizational_survival':'group','political_pressure':'group','governance':'proposal',
 'institutional_work':'policy','institutional_response':'faction','religious_interest':'religion','divine_contact':'religion',
 'divine_contract':'religion','power':'religion','spatial_journey':'travel','return_from_site':'travel','exploration':'travel','migration':'migration'}
SPECIAL={
 'goals.GoalSystem.decide':'decide','needs.NeedSystem.refresh':'refresh','goals.GoalSystem._evaluate':'evaluate',
 'goals.GoalSystem.choose':'choose','goals.GoalSystem.execute':'execute','goals.GoalSystem.preventive_choice':'prevent',
 'events.EventRecorder.emit':'event','knowledge.KnowledgeSystem.learn':'learn','engine.Engine.finish_death':'death',
 'feeding.FeedingSystem.decision_interval':'lod','needs.NeedSystem.finish':'need_finish',
 'professions.ProfessionSystem.work':'work','institutions.Institutions.decision_scores':'political',
 'institutions.Institutions.membership_scores':'membership','lethality.LethalPressure.evaluate':'lethal_pressure',
 'lethal_decisions.LethalDecisionSystem.evaluate':'lethal_decision','lethal_decisions.LethalDecisionSystem.terminal':'terminal',
 'action_pressure.ActionPressureSystem.assess':'capacity','geography.Geography.begin':'journey_begin',
 'geography.Geography.step':'journey_step','institutions.Institutions.formalization':'formalization',
 'aftermath.AftermathSystem.on_kill':'aftermath','divine_relations.DivineRelations.audience':'audience'}

class Observer:
 def __init__(self):
  self.code_names=codes();self.tags={c:SPECIAL[n] for c,n in self.code_names.items() if n in SPECIAL}
  self.phase='generation';self.w=None;self.e=None;self.current=None;self.pending={}
  self.calls=Counter();self.edges=Counter();self.events=Counter();self.event_sources=defaultdict(Counter)
  self.generation_calls=Counter();self.generation_events=Counter();self.errors=Counter();self.error_examples=[]
  self.eval_calls=Counter();self.candidate=Counter();self.available=Counter();self.utility=Counter();self.selected=Counter();self.executed=Counter();self.success=Counter();self.failure=Counter();self.failed_reasons=Counter();self.pre_gates=Counter();self.zero_candidates=Counter();self.need_seen=Counter();self.need_finish=Counter();self.lod=Counter();self.lod_selected=Counter()
  self.raw_scores=defaultdict(Counter);self.latency=defaultdict(Counter);self.learned=Counter();self.learning_log=defaultdict(lambda:{'count':0,'first':None,'last':None,'first_people':[]})
  self.pools=defaultdict(list);self.rings=defaultdict(lambda:deque(maxlen=2));self.deaths=[];self.important=[]
  self.retained_events={};self.groups={};self.group_previous={};self.removals=defaultdict(list);self.temporal=[];self.checks=[];self.step_seconds=[];self.rejection=Counter()
  self.lethal_cases=[];self.rare_calls=[];self.context_lost=Counter();self.need_lost=Counter();self.call_scores=[]
  self.proposal_start={};self.proposal_submit={};self.policy_start={};self.policy_first_work={};self.invited={};self.journey_start={};self.group_start={};self.need_start={}
 def bind(self,e):self.e=e;self.w=e.world;self.phase='campaign'
 def qty(self,owner,kind):
  return sum(n for i,n in owner.inventory.items() if self.w.items[i].kind==kind)
 def state(self,p):
  town=self.w.towns.get(p.position.map_id)
  return {'id':p.id,'name':p.name,'hour':self.w.turn,'alive':p.alive,'profession':p.profession,'category':p.category,'lod':p.lod,
   'position':pos(p.position),'home':pos(p.home),'workplace':pos(p.workplace),'residence':p.town_id,
   'hp':p.health,'hunger':p.hunger,'thirst':p.thirst,'fatigue':p.fatigue,'money':p.money,'food':self.qty(p,'food'),'water':self.qty(p,'water'),
   'recoverable_deprivation':p.recoverable_deprivation_damage,'starvation_hours':p.starvation_hours,
   'local_food':self.qty(town,'food') if town else None,'local_water':self.qty(town,'water') if town else None,
   'personality':vars(p.personality).copy(),'emotions':vars(p.emotions).copy(),'failures':p.failures.copy(),
   'known_places':{k:pos(v) for k,v in p.known_places.items()},'market_observation':{k:plain(v) for k,v in p.market_observation.items() if k in ('turn','town_id','stock','price','price_turn','temporary_work','offers_expire_at','training_offer')},
   'groups':list(p.group_ids),'factions':list(p.organization_ids),'known_groups':list(p.known_groups),'known_factions':list(p.known_factions),
   'route_knowledge_count':len(p.route_knowledge),'known_towns':list(p.known_towns),'journey':plain(p.journey),
   'training':{'target':p.training_target,'progress':p.training_progress,'required':p.training_required},'devotion':p.devotion,'religion':p.religion,
   'goal':plain(p.goal),'suspended_goal':plain(p.suspended_goal)}
 def need(self,n):
  keys=('source_event','source_fact','known_location','culprit','victim','threat','emergency','mode','faction_id','group_id','proposal_id','policy_id','diagnostic','institutional_role','condition','resolution','invitation','source','reason')
  return {'id':n.id,'kind':n.kind,'target':n.target_id,'base':n.base_urgency,'priority':n.priority,'status':n.status,'source':n.source,'reason':n.reason,'created':n.created_at,'expires':n.expires_at,'context':{k:plain(v) for k,v in n.context.items() if k in keys}}
 def solution(self,s):
  return {'action':s.action,'score':s.score,'target':s.target_id,'destination':pos(s.destination),'terms':s.considerations.copy(),'feeding':plain(s.feeding),'action_pressure':plain(s.action_audit)}
 def category(self,n,action):
  if action in ('finish','spare','capture','first_aid','attack','flee','surrender','defend','withdraw'):return 'lethal' if action=='finish' else 'combat'
  if action in ('steal','steal_meal','steal_person','person_meal'):return 'crime'
  if action in ('train','materialize_worker','open_training'):return 'career'
  if action in ('submit_proposal','review_proposal','support_proposal','read_response','relay_response'):return 'proposal'
  if action=='policy_work':return 'policy'
  if action in ('route_travel','follow_expedition','explore_poi','ask_route'):return 'travel'
  if action.startswith('institutional_') or action in ('answer_invitation','invite_person','request_membership','report_to_faction'):return 'faction'
  return KINDS.get(n,'social')
 def keep(self,category,row,limit=4):
  key=f"{category}:{row.get('actor',row.get('state_before',{}).get('id'))}:{row.get('hour')}:{row.get('action','')}"
  priority=int.from_bytes(hashlib.sha256(key.encode()).digest()[:8],'big')
  pool=self.pools[category]
  if any(k==priority for k,v in pool):return
  if len(pool)<limit:pool.append((priority,row))
  elif priority<max(pool,key=lambda x:x[0])[0]:
   worst=max(range(len(pool)),key=lambda i:pool[i][0]);pool[worst]=(priority,row)
 def profile(self,frame,event,arg):
  if event not in ('call','return'):return
  name=self.code_names.get(frame.f_code)
  if name is None:return
  tag=self.tags.get(frame.f_code)
  if event=='call':
   if self.phase=='generation':self.generation_calls[name]+=1
   else:
    self.calls[name]+=1
    parent=self.code_names.get(frame.f_back.f_code) if frame.f_back else None
    if parent:self.edges[(parent,name)]+=1
  if tag is None:return
  try:self.observe(tag,frame,event,arg)
  except Exception as exc:
   key=f'{name}:{event}:{type(exc).__name__}:{exc}';self.errors[key]+=1
   if len(self.error_examples)<5:
    import traceback
    self.error_examples.append({'hour':self.w.turn if self.w else None,'error':key,'traceback':traceback.format_exc()})
 def observe(self,tag,frame,event,arg):
  x=frame.f_locals
  if tag=='event' and event=='return' and arg is not None:
   if self.phase=='generation':self.generation_events[arg.kind]+=1;return
   self.on_event(arg,frame);return
  if self.phase!='campaign':return
  if tag=='utility':
   if event=='return' and arg is not None:
    self.utility[x['action']]+=1;self.raw_scores[x['action']][round(arg[0]/10)*10]+=1
   return
  if event=='call':
   if tag=='decide':
    p=x['character'];self.current={'actor':p.id,'hour':self.w.turn,'state_before':self.state(p),'needs':[],'evaluations':[],'choices':[],'preparations':[],'calculations':[],'events':[],'knowledge_before':list(p.knowledge),'status':'in_progress'}
   elif tag=='execute':
    p=x['character'];goal=x['goal'];self.executed[goal.action]+=1
    if self.current and self.current['actor']==p.id:self.current['execution']={'goal_at_entry':plain(goal),'state_before':self.state(p)}
   elif tag=='death':
    p=x['person']
    if p.alive:self.deaths.append({'actor':p.id,'hour':self.w.turn,'state':self.state(p),'cause_argument':x['cause'],'last_decisions':list(self.rings[p.id])})
   elif tag=='work':
    p=x['character'];town=self.w.towns.get(p.town_id)
    self.pending[id(frame)]={'actor':p.id,'town':p.town_id,'money_before':p.money,'treasury_before':town.money if town else None,'inputs_before':{k:self.qty(town,k) for k in ('food','grain','iron','wood')} if town else {}}
   return
  # CPython also signals return(None) while unwinding; never mask an engine error.
  if arg is None and tag in ('execute','evaluate','refresh','choose','learn','political','membership','lod','work'):return
  current=self.current
  if tag=='refresh':
   p=x['character']
   for n in arg:self.need_seen[n.kind]+=1
   if current and current['actor']==p.id:
    current['needs']=[self.need(n) for n in arg]
    refs={n.context.get(k) for n in arg for k in ('source_event','source_fact') if n.context.get(k) is not None}
    current['known_source_facts']=[plain(p.knowledge[k]) for k in refs if k in p.knowledge][:10]
    current['knowledge_after_perception']=list(p.knowledge)
  elif tag=='evaluate':
   p,n=x['character'],x['need'];self.eval_calls[n.kind]+=1
   choices=x['choices'];kept={id(s) for s in arg};rejected={id(s) for s in x.get('rejected',[])};gates=[]
   self.candidate[n.kind]+=len(choices);self.available[n.kind]+=len(arg)
   if not choices:self.zero_candidates[n.kind]+=1
   for s in choices:
    if id(s) in kept:continue
    a=MEALS.get(s.action,s.action)
    if s.action_audit and not s.action_audit['eligible']:reason='ActionPressure.capacity_or_cause_gate'
    elif id(s) in rejected:reason='feeding.survival_viable_false'
    elif max(p.failures.get(s.action,0),p.failures.get(a,0))>self.w.turn:reason='cooldown_after_failure'
    elif a=='ask_help' and p.failures.get(f'request:{s.target_id}',0)>self.w.turn:reason='request_cooldown'
    elif s.destination and s.destination.map_id!=p.position.map_id:reason='destination_other_map'
    elif a in ('work_for_food','temporary_service') and s.action not in MEALS and self.qty(p,'food')>p.food_state.get('reserve_target',10000):reason='carried_food_exceeds_reserve'
    elif n.kind=='family' and a in ACQUISITIONS and self.qty(p,'food')>=p.food_state.get('reserve_target',10000)+1:reason='family_supply_already_covered'
    elif n.kind=='food' and any(c.action in MEALS and MEALS[c.action]==s.action and c.destination==s.destination and c.target_id==s.target_id for c in arg):reason='acquisition_replaced_by_immediate_meal_after_scoring'
    else:reason='discard_gate_not_observable_per_choice'
    stage='after_Utility' if reason in ('feeding.survival_viable_false','acquisition_replaced_by_immediate_meal_after_scoring') else 'before_Utility_or_unresolved'
    self.pre_gates[f'{n.kind}:{reason}']+=1;gates.append({'action':s.action,'target':s.target_id,'reason':reason,'stage':stage,'action_pressure':plain(s.action_audit),'feeding':plain(s.feeding),'proof':'leitura das condições do frame/objetos; sem executar decisões adicionais'})
   if current and current['actor']==p.id:
    if len(current['evaluations'])<22:current['evaluations'].append({'need_id':n.id,'kind_at_evaluation':n.kind,'input_actions':[s.action for s in choices],'discarded':gates[:12],'available':[self.solution(s) for s in arg[:10]],'input_count':len(choices),'available_count':len(arg)})
    else:self.context_lost['evaluation_sample_cap']+=1
  elif tag=='choose' and arg is not None and current:
   if len(current['choices'])<8:current['choices'].append({'chosen':self.solution(arg),'near_scores':[s.score for s in x['alternatives'][:8]],'variation_draws':'não capturados; RNG não consultado pelo observador'})
  elif tag=='prevent' and arg is not None and current:
   current['preparations'].append({'input':self.solution(x['choice']),'replacement':self.solution(arg),'travel':x.get('travel'),'horizon':x.get('horizon')})
  elif tag=='execute':
   action=x['goal'].action
   if arg[0]:self.success[action]+=1
   else:self.failure[action]+=1;self.failed_reasons[f'{action}:{arg[1]}']+=1
   if current and current['actor']==x['character'].id:
    current['execution'].update(success=bool(arg[0]),result=plain(arg),state_after=self.state(x['character']))
  elif tag=='decide':
   p=x['character'];selected=x.get('selected');choice=x.get('choice')
   if not current or current['actor']!=p.id:return
   if selected is not None and choice is not None:
    current.update(selected_need=self.need(selected),winner=self.solution(choice),goal_after=plain(p.goal),state_after=self.state(p),action=choice.action,status='decided')
    self.selected[f'{selected.kind}:{choice.action}']+=1;self.lod_selected[p.lod]+=1
    for need in current['needs']:
     if need['id']!=selected.id:
      stage='evaluated' if any(e['need_id']==need['id'] for e in current['evaluations']) else 'not_evaluated'
      self.need_lost[f"{need['kind']}->{selected.kind}:{stage}"]+=1
    target=choice.target_id;current['known_target']=plain(p.observations.get(target)) if target is not None else None
    current['relations_to_target']=[plain(r) for r in self.w.relationships.values() if r.source_id==p.id and r.target_id==target] if target is not None else []
    self.rings[p.id].append(current)
    self.keep(self.category(selected.kind,choice.action),current)
   else:
    current.update(status='no_viable_selection',state_after=self.state(p))
    self.keep('blocked',current,5)
   self.current=None
  elif tag=='learn' and arg:
   p,f=x['character'],x['fact'];accepted=p.knowledge.get(f.event_id);confidence=accepted.confidence if accepted else None
   self.learned[f'{f.kind}:{"firsthand" if x["firsthand"] else "transmitted"}']+=1
   delay=max(0,self.w.turn-f.turn);self.latency['event_to_knowledge'][delay]+=1
   item=self.learning_log[f.event_id];item['count']+=1;item['first']=self.w.turn if item['first'] is None else min(item['first'],self.w.turn);item['last']=self.w.turn
   if len(item['first_people'])<6 and p.id not in item['first_people']:item['first_people'].append(p.id)
   if current and len(current.setdefault('learning_during_decision',[]))<12:current['learning_during_decision'].append({'npc':p.id,'event':f.event_id,'kind':f.kind,'source':f.source_id,'firsthand':x['firsthand'],'confidence':confidence,'latency':delay})
  elif tag=='lod':self.lod[f"{x['person'].lod}:{arg}"]+=1
  elif tag=='need_finish':
   n=x['need'];self.need_finish[f"{n.kind}:{n.status}"]+=1;self.latency['need_lifetime_when_finish_called'][max(0,self.w.turn-n.created_at)]+=1
  elif tag=='work':
   before=self.pending.pop(id(frame),{});before['result']=plain(arg)
   if current and len(current['calculations'])<20:current['calculations'].append({'system':'work','actual':before})
  elif tag in ('political','membership','lethal_pressure','lethal_decision','terminal','capacity','formalization','journey_begin','journey_step','aftermath','audience'):
   detail={'system':tag,'function':self.code_names[frame.f_code],'result':plain(arg),'inputs':{k:plain(x[k]) for k in ('score','scores','pressure','cost','avoid','funds','age','mode','cause','reason','benefit','risk','execute') if k in x}}
   if current and len(current['calculations'])<20:current['calculations'].append(detail)
   if tag in ('political','membership','formalization','aftermath','audience') and len(self.rare_calls)<80:self.rare_calls.append({'hour':self.w.turn,**detail})
  # Utility call counting is performed separately via the code tag below.
 def on_event(self,event,frame):
  self.events[event.kind]+=1
  parent=frame.f_back;source=[]
  for _ in range(3):
   if parent is None:break
   name=self.code_names.get(parent.f_code)
   if name:source.append(name)
   parent=parent.f_back
  self.event_sources[event.kind][' → '.join(reversed(source))]+=1
  row={'id':event.id,'kind':event.kind,'hour':event.turn,'actor':event.actor_id,'target':event.target_id,'position':pos(event.location),
       'witnesses':list(event.witnesses),'historical':event.historical,'context':plain(event.context),'emitter_stack':source}
  if self.current and len(self.current['events'])<14:self.current['events'].append(row)
  k=event.kind;c=event.context
  if k=='GroupJoinRejected':self.rejection[c.get('reason','unspecified')]+=1
  if k=='NewGroupCreated':self.groups[event.target_id]={'id':event.target_id,'created':event.turn,'founders':list(c.get('members',[])),'joins':[]};self.group_start[event.target_id]=event.turn
  if k=='GroupJoined' and event.target_id in self.groups:self.groups[event.target_id]['joins'].append({'hour':event.turn,'npc':event.actor_id})
  if k=='GroupMeeting' and event.target_id in self.group_start:self.latency['group_to_first_or_repeated_meeting'][event.turn-self.group_start[event.target_id]]+=1
  pid=c.get('proposal_id',event.target_id)
  if k=='ProposalCreated':self.proposal_start[pid]=event.turn
  if k=='ProposalSubmitted' and pid not in self.proposal_submit:
   self.proposal_submit[pid]=event.turn
   if pid in self.proposal_start:self.latency['proposal_creation_to_first_submission'][event.turn-self.proposal_start[pid]]+=1
  if k=='PolicyDecided' and pid in self.proposal_submit:self.latency['proposal_submission_to_decision'][event.turn-self.proposal_submit[pid]]+=1
  if k=='PolicyCreated':self.policy_start[event.target_id]=event.turn
  if k=='PolicyEffect' and event.target_id not in self.policy_first_work:
   self.policy_first_work[event.target_id]=event.turn
   if event.target_id in self.policy_start:self.latency['policy_to_first_work'][event.turn-self.policy_start[event.target_id]]+=1
  if k=='FactionInvite':self.invited[(event.target_id,c.get('candidate'))]=event.turn
  if k.startswith('FactionMembership') and (event.target_id,event.actor_id) in self.invited:self.latency['invitation_to_response'][event.turn-self.invited[(event.target_id,event.actor_id)]]+=1
  if k=='JourneyStarted':self.journey_start[event.actor_id]=event.turn
  if k=='JourneyArrived' and event.actor_id in self.journey_start:self.latency['journey_start_to_arrival'][event.turn-self.journey_start.pop(event.actor_id)]+=1
  important=('ProposalCreated','ProposalSubmitted','PolicyDecided','PolicyCreated','PolicyEffect','PolicyCompleted','PolicyBlocked','FactionInvite','FactionMembershipAccepted','FactionMembershipRejected','FactionMembershipDeferred','FactionFormalized','FactionAction','GroupDissolved','CharacterKilled','DivineAudience','DivineContractOffered','DivineManifestation','DivinityKilled','Apotheosis','WorkerMaterialized','ProfessionChanged','TrainingCompleted','JourneyArrived')
  if k in important:self.important.append(row)
 def money(self):
  w=self.w
  result={name:sum(getattr(o,'money',0) for o in coll.values()) for name,coll in [('characters',w.characters),('towns',w.towns),('kingdoms',w.kingdoms),('groups',w.groups),('factions',w.factions),('policies',w.institutional_policies)]}
  result['abstract_money']=sum(t.abstract_money for t in w.towns.values());result['total']=sum(result.values());return result
 def checkpoint(self):
  w=self.w
  for gid,g in w.groups.items():
   members=set(g.member_ids)
   for pid in self.group_previous.get(gid,set())-members:self.removals[gid].append({'npc':pid,'hour':w.turn,'dead':not w.characters[pid].alive})
   self.group_previous[gid]=members
  if w.turn%25:return
  errors=validate_world(w);self.checks.append({'hour':w.turn,'errors':errors})
  if errors:raise RuntimeError(str(errors[:8]))
  self.temporal.append({'hour':w.turn,'alive':sum(p.alive for p in w.characters.values()),'abstract':sum(t.abstract_population for t in w.towns.values()),'deaths':dict(Counter(r['cause'] for r in w.death_records.values())),
    'money':self.money(),'events':dict(self.events),'groups':len(w.groups),'proposals':len(w.proposals),'policies':len(w.institutional_policies)})
 def finish(self):
  w=self.w
  for d in self.deaths:d['record']=plain(w.death_records.get(d['actor']))
  samples=[]
  for category,pool in sorted(self.pools.items()):
   for priority,row in sorted(pool):samples.append({'category':category,'sampling_priority':str(priority),**row})
  # Deduplicated event receipts for selected decisions and significant transitions.
  retained={ev['id']:ev for row in samples for ev in row.get('events',[])}
  retained.update({ev['id']:ev for ev in self.important})
  for ev in retained.values():ev['learned']=dict(self.learning_log.get(ev['id'],{}))
  group_rows=[]
  for gid,g in w.groups.items():group_rows.append({**plain(g),**self.groups.get(gid,{}),'removals':self.removals[gid],'living_members':[i for i in g.member_ids if w.characters[i].alive]})
  proposals=[]
  for p in w.proposals.values():
   g=w.groups.get(p.group_id);town=w.towns[p.town_id];rep=w.characters[g.leader_id] if g else None;mayor=w.characters.get(town.mayor_id)
   proposals.append({**plain(p),'representative':self.state(rep) if rep else None,'mayor':self.state(mayor) if mayor else None})
  factions=[]
  for f in w.factions.values():
   place=w.towns.get(f.headquarters_id) or w.points.get(f.headquarters_id)
   factions.append({**plain(f),'leader_state':self.state(w.characters[f.leader_id]),'member_states':[self.state(w.characters[i]) for i in f.member_ids],
    'inventory_quantities':{k:self.qty(f,k) for k in ('food','water','weapon','tool')},'hq_inventory':{k:self.qty(place,k) for k in ('food','water','weapon','tool')} if place else {},
    'capabilities':self.e.institutions.capabilities(f,w.characters[f.leader_id])})
  metrics={'seed':SEED,'hours':w.turn,'calls':dict(self.calls),'generation_calls':dict(self.generation_calls),'generation_events':dict(self.generation_events),
   'call_edges':[{'caller':a,'callee':b,'count':n} for (a,b),n in self.edges.most_common()],
   'events':dict(self.events),'event_sources':{k:dict(v) for k,v in self.event_sources.items()},'world_metrics':plain(w.metrics),
   'need_seen':dict(self.need_seen),'evaluate_calls':dict(self.eval_calls),'raw_candidates':dict(self.candidate),'available':dict(self.available),
   'utility_calls':dict(self.utility),'selected':dict(self.selected),'executed':dict(self.executed),'success':dict(self.success),'failure':dict(self.failure),'failed_reasons':dict(self.failed_reasons),
   'pre_utility_and_post_gates':dict(self.pre_gates),'no_candidates_at_evaluate':dict(self.zero_candidates),'need_finished':dict(self.need_finish),'need_lost':dict(self.need_lost),
   'lod_calls':dict(self.lod),'lod_selected':dict(self.lod_selected),'learned':dict(self.learned),
   'latencies':{k:{'distribution':dist([int(v) for v,n in hist.items() for _ in range(n)]),'histogram':dict(hist)} for k,hist in self.latency.items()},
   'checks':self.checks,'temporal':self.temporal,'step_seconds':dist(self.step_seconds),'observer_errors':dict(self.errors),'observer_error_examples':self.error_examples,'sample_caps_reached':dict(self.context_lost),
   'population':{'named_total':len(w.characters),'named_alive':sum(p.alive for p in w.characters.values()),'abstract':sum(t.abstract_population for t in w.towns.values())},
   'money_final':self.money(),'deaths':plain(w.death_records),'groups':group_rows,'proposals':proposals,'policies':plain(list(w.institutional_policies.values())),'factions':factions,
   'towns':[{'id':t.id,'name':t.name,'kingdom':t.kingdom_id,'capital':t.capital,'kind':t.kind,'money':t.money,'abstract_money':t.abstract_money,'population':t.abstract_population,'alive_residents':sum(w.characters[i].alive for i in t.resident_ids),
     'infrastructure':t.infrastructure,'economic_report':t.economic_report,'production_total':t.production_total,'inventory':{k:self.qty(t,k) for k in ('food','water','grain','iron','wood')}} for t in w.towns.values()],
   'divinities':plain(list(w.divinities.values())),'contracts':plain(list(w.divine_contracts.values())),
   'routes':{'count':len(w.routes),'uses':sum(r.uses for r in w.routes.values()),'journeys_remaining':sum(bool(p.journey) for p in w.characters.values() if p.alive)},
   'group_rejection_reasons':dict(self.rejection),'sampling':{'method':'bottom-k por SHA256 de categoria/NPC/hora/ação, sem RNG do mundo','per_category_max':4,'samples':len(samples)}}
  jwrite(OUT/'metrics.json',metrics)
  jwrite(OUT/'traces.json',{'decisions':samples,'death_cases':self.deaths,'important_events':list(retained.values()),'rare_computations':self.rare_calls})

# Counts the actually invoked evaluator; never recomputes scores.
SPECIAL['utility.evaluate']='utility'

def control():
 path=OUT/'manifesto.json';m=json.loads(path.read_text());assert m['static_complete_before_simulation']
 if 'control' in m:raise RuntimeError('Controle já executado; não duplicar mundos.')
 seed='Controle-Radiografia55';cfg=GenerationConfig(kingdom_count=1,historical_turns=0)
 started=time.perf_counter();a=generate_world(seed,with_player=False,config=cfg);ea=Engine(a)
 for _ in range(8):ea.step()
 ha=hashlib.sha256(dumps(a).encode()).hexdigest()
 obs=Observer();sys.setprofile(obs.profile)
 try:
  b=generate_world(seed,with_player=False,config=cfg);eb=Engine(b);obs.bind(eb)
  for _ in range(8):eb.step();obs.checkpoint()
 finally:sys.setprofile(None)
 hb=hashlib.sha256(dumps(b).encode()).hexdigest()
 assert ha==hb,'Observador mudou estado, RNG ou eventos'
 assert a.rng_state==b.rng_state and a.history==b.history and a.events==b.events
 assert not obs.errors,obs.errors
 m['control']={'seed':seed,'hours_each':8,'kingdoms':1,'world_sha256_plain':ha,'world_sha256_observed':hb,'world_rng_events_equal':True,'observer_errors':dict(obs.errors),'seconds':round(time.perf_counter()-started,3)}
 jwrite(path,m);print(json.dumps(m['control']))

def campaign():
 path=OUT/'manifesto.json';m=json.loads(path.read_text());assert m.get('control',{}).get('world_rng_events_equal')
 if 'campaign' in m:raise RuntimeError('Campanha já registrada; não reiniciar/selecionar outra seed.')
 assert fingerprint()==m['code_sha256']
 cfg=GenerationConfig(historical_turns=0);obs=Observer();started=time.perf_counter();sys.setprofile(obs.profile)
 try:w=generate_world(SEED,with_player=False,config=cfg);e=Engine(w)
 finally:sys.setprofile(None)
 obs.bind(e)
 m['campaign']={'seed':SEED,'hours_requested':HOURS,'config':plain(cfg),'initial_named':len(w.characters),'initial_abstract':sum(t.abstract_population for t in w.towns.values()),'initial_money':obs.money(),'restarts':0,'observer_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
 jwrite(path,m);print(json.dumps(m['campaign']),flush=True)
 try:
  for _ in range(HOURS):
   t=time.perf_counter();sys.setprofile(obs.profile)
   try:e.step()
   finally:sys.setprofile(None)
   obs.step_seconds.append(time.perf_counter()-t);obs.checkpoint()
   if w.turn%25==0:print(json.dumps({'hour':w.turn,'alive':sum(p.alive for p in w.characters.values()),'deaths':len(w.death_records),'events':sum(obs.events.values()),'observer_errors':sum(obs.errors.values()),'seconds':round(time.perf_counter()-started,2)}),flush=True)
  assert not obs.errors,obs.errors
  assert fingerprint()==m['code_sha256']
  routes=e.geography.audit();assert not routes,routes
  obs.finish();JsonRepository().save(w,OUT/'save_temporario.json')
  m['campaign'].update(hours_completed=w.turn,runtime_seconds=round(time.perf_counter()-started,2),code_sha256_after=fingerprint(),route_errors=routes)
  jwrite(path,m)
 except Exception as exc:
  jwrite(OUT/'falha.json',{'seed':SEED,'hour':w.turn,'exception':repr(exc),'observer_errors':dict(obs.errors),'checks':obs.checks});raise
 print(json.dumps({'complete':w.turn,'runtime_seconds':m['campaign']['runtime_seconds']}),flush=True)

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('mode',choices=('control','campaign'));args=p.parse_args()
 (control if args.mode=='control' else campaign)()
