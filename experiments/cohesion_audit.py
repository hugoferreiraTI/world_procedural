"""Auditoria externa: observa chamadas reais, sem editar ou substituir o motor.

sys.setprofile lê argumentos, retornos e variáveis locais. Não ativa debug (que
recalcula alternativas), não chama RNG e não escreve nos objetos da simulação.
"""
import hashlib
import json
import statistics
import sys
import time
from collections import Counter,defaultdict,deque
from dataclasses import asdict,is_dataclass
from pathlib import Path

from procedural import RULES_VERSION,GENERATION_VERSION
from procedural.generation import GenerationConfig,generate_world
from procedural.engine import Engine
from procedural.persistence import JsonRepository
from procedural.validation import validate_world
from procedural.needs import FINISHED

BASE=Path(__file__).resolve().parents[1]
OUT=BASE/'reports/diagnostico_coesao'
SEED='Neravon-Coesao55'
HOURS=300
INSTITUTIONAL={'political_pressure','organizational_survival','organizational_access','affiliation','governance','institutional_work','institutional_response'}
SEMANTIC={'NewGroupCreated','GroupJoined','GroupDissolved','GroupMeeting','ProposalCreated','CompatibleProposalFound',
 'ProposalSupported','ProposalSupportDelivered','ProposalSubmitted','PolicyDecided','PolicyCreated','PolicyEffect','PolicyBlocked','PolicyCompleted',
 'FactionInvite','FactionMembershipAccepted','FactionMembershipRejected','FactionMembershipDeferred','FactionMembershipConditioned',
 'FactionFormalized','FactionAction','FactionLocalStatusChanged','FactionProposalSupported','FormalizationConsidered','FactionDeserted',
 'JourneyStarted','JourneyArrived','CharacterKilled','MayorAppointed','PoliticalPressureChanged'}

def dump(path,value):path.write_text(json.dumps(value,ensure_ascii=False,indent=2),encoding='utf-8')
def safe(value):
    if is_dataclass(value):return safe(asdict(value))
    if isinstance(value,dict):return {str(k):safe(v) for k,v in value.items()}
    if isinstance(value,(list,tuple,set,deque)):return [safe(v) for v in value]
    if value is None or isinstance(value,(str,int,float,bool)):return value
    return str(type(value).__name__)
def fingerprint():
    h=hashlib.sha256()
    for p in sorted((BASE/'procedural').glob('*.py')):h.update(p.name.encode());h.update(p.read_bytes())
    return h.hexdigest()
def distribution(values):
    values=sorted(values)
    if not values:return {'n':0}
    def q(p):
        x=(len(values)-1)*p;a=int(x);b=min(a+1,len(values)-1)
        return round(values[a]+(values[b]-values[a])*(x-a),4)
    return {'n':len(values),'min':values[0],'p25':q(.25),'median':q(.5),'mean':round(statistics.mean(values),4),'p75':q(.75),'p90':q(.9),'max':values[-1]}

class Audit:
    def __init__(self,e):
        self.e,self.w=e,e.world
        self.events=Counter();self.semantic=[];self.calls=Counter();self.evals={};self.active={};self.rings=defaultdict(lambda:deque(maxlen=3))
        self.pending={};self.last_execution={};self.action_selected=Counter();self.action_executed=Counter();self.action_failed=Counter()
        self.need_selections=Counter();self.institutional_competition=Counter();self.detected_collective=set()
        self.group_samples=[];self.proposal_samples=[];self.membership_samples=[];self.political_samples=[];self.work_samples=[]
        self.affinity_values=[];self.affinity_rejected=set();self.reasons_by_actor=defaultdict(set);self.affinity_pairs=Counter();self.affinity_samples=[]
        self.groups={};self.previous_members={};self.previous_status={};self.group_removals=defaultdict(list)
        self.deaths=[];self.first_vital={};self.checks=[];self.temporal=[]
        self.faction_contacts=defaultdict(set);self.faction_visibility={};self.faction_choices=defaultdict(Counter)
        self.policy_eligible=defaultdict(set);self.policy_awareness=defaultdict(set);self.policy_awareness_hours=defaultdict(Counter)
        self.meeting_gates=[];self.formalization_rows=[]
        self.observer_errors=Counter();self.observer_error_samples=[]
        self.group_checks=defaultdict(list);self.last_affinity=defaultdict(dict);self.last_groups={};self.retired_groups={}
        self.faction_member_knowers=defaultdict(set);self.faction_executions=defaultdict(Counter);self.faction_failures=defaultdict(Counter)
        self.candidate_calls=Counter();self.candidate_viable=Counter();self.executions_this_decision=set()
        self.codes={}
        for tag,fn in [('refresh',e.needs.refresh),('evaluate',e.goals._evaluate),('decide',e.goals.decide),('execute',e.goals.execute),
                       ('form',e.society.form),('meeting',e.society.meeting),('affinity',e.society.affinity),('search',e.institutions.search_groups),
                       ('acceptable',e.institutions.acceptable_group),('propose',e.institutions.propose),
                       ('formalize',e.institutions.formalization),('membership',e.institutions.membership),
                       ('political_scores',e.institutions.decision_scores),('policy_work',e.institutions.policy_work),
                       ('faction_candidates',e.institutions.faction_candidates),('worker_eligible',e.institutions.worker_eligible),
                       ('access_refresh',e.access.refresh),('death',e.finish_death)]:self.codes[fn.__code__]=tag

    def count_items(self,owner,kind):
        return sum(n for id,n in owner.inventory.items() if id in self.w.items and self.w.items[id].kind==kind)

    def needs(self,p):
        return [{'id':n.id,'kind':n.kind,'priority':n.priority,'base':n.base_urgency,'status':n.status,'target':n.target_id,
                 'source':n.source,'reason':n.reason,'context':{k:safe(v) for k,v in n.context.items() if k in ('group_id','faction_id','cause','proposal_id','mode','emergency','diagnostic')}}
                for n in p.needs.values() if n.status not in FINISHED]

    def state(self,p,full=False):
        t=self.w.towns.get(p.position.map_id);obs=p.market_observation
        row={'id':p.id,'name':p.name,'hour':self.w.turn,'alive':p.alive,'profession':p.profession,'town':p.town_id,
             'position':safe(p.position),'hp':p.health,'hunger':p.hunger,'thirst':p.thirst,'fatigue':p.fatigue,'money':p.money,
             'food':self.count_items(p,'food'),'water':self.count_items(p,'water'),'goal':p.goal.action if p.goal else None,
             'goal_status':p.goal.status if p.goal else None,'goal_destination':safe(p.goal.destination) if p.goal else None,
             'local_food':self.count_items(t,'food') if t else None,'local_water':self.count_items(t,'water') if t else None,
             'at_market':bool(t and p.position==t.market),'known_market':safe(p.known_places.get('market')),
             'known_wells':[safe(v) for k,v in p.known_places.items() if k.startswith('well')],
             'market_observation':safe(obs),'last_successful_action':safe(p.last_successful_action),'journey':safe(p.journey) if p.journey else None}
        if full:row.update(personality=asdict(p.personality),needs=self.needs(p),groups=list(p.group_ids),factions=list(p.organization_ids),
                           known_groups=list(p.known_groups),known_factions=safe(p.known_factions),known_policies=list(p.known_policies),
                           commitments=[{'id':c.id,'status':c.status,'target':c.target_id,'reason':c.reason if hasattr(c,'reason') else None} for c in p.commitments.values()])
        return row

    def context(self,p):
        active=self.active.get(p.id,[])
        return {'state':self.state(p,True),'ordered_needs':active,'evaluations':self.evals.get(p.id,{})}

    def event(self,ev):
        self.events[ev.kind]+=1
        if ev.kind in SEMANTIC:self.semantic.append({'id':ev.id,'kind':ev.kind,'hour':ev.turn,'actor':ev.actor_id,'target':ev.target_id,'location':safe(ev.location),'context':safe(ev.context)})
        if ev.kind=='NewGroupCreated':
            g=self.w.groups[ev.target_id];self.groups[g.id]={'id':g.id,'name':g.name,'town':g.town_id,'cause':g.cause,'subject':g.subject_id,'created_at':g.created_at,'founders':list(g.member_ids),'joins':[],'meeting_events':[],'dissolved_at':None}
        if ev.kind=='GroupJoined' and ev.target_id in self.groups:self.groups[ev.target_id]['joins'].append({'hour':ev.turn,'person':ev.actor_id})
        if ev.kind=='GroupMeeting' and ev.target_id in self.groups:self.groups[ev.target_id]['meeting_events'].append({'hour':ev.turn,'present':list(ev.context.get('members',[]))})
        if ev.kind=='GroupDissolved' and ev.target_id in self.groups:self.groups[ev.target_id]['dissolved_at']=ev.turn;self.groups[ev.target_id]['dissolution_reason']=ev.context.get('reason')

    def profile(self,frame,event,arg):
        # Uma falha de leitura nunca deve substituir exceção do motor ou alterar
        # o seu retorno. O erro fica explícito na evidência da auditoria.
        if event not in ('call','return') or frame.f_code not in self.codes:return
        try:self.observe_frame(frame,event,arg)
        except Exception as error:
            import traceback
            key=f'{self.codes.get(frame.f_code)}:{event}:{type(error).__name__}:{error}'
            self.observer_errors[key]+=1
            if len(self.observer_error_samples)<5:self.observer_error_samples.append({'hour':self.w.turn,'error':key,'traceback':traceback.format_exc()})

    def observe_frame(self,frame,event,arg):
        tag=self.codes.get(frame.f_code)
        if tag is None or event not in ('call','return'):return
        if event=='return' and arg is None and tag in ('execute','evaluate','refresh','affinity','acceptable','search','policy_work','political_scores','membership'):
            return  # CPython também sinaliza return(None) ao propagar exceção.
        x=frame.f_locals
        if event=='call':
            self.calls[tag]+=1
            if tag=='decide':
                p=x['character'];self.evals[p.id]={};self.executions_this_decision.discard(p.id);self.group_checks[p.id]=[];self.last_affinity[p.id]={}
            elif tag in ('form','propose','membership','policy_work'):
                p=x['p'];row=self.context(p)
                if tag=='form':
                    row.update(cause=x['cause'],subject=x['subject'],known_groups=[self.group_info(self.w.groups[id]) for id in p.known_groups if id in self.w.groups],existing_ids=list(self.w.groups),group_checks=list(self.group_checks[p.id]))
                if tag=='propose':
                    row.update(group=x['g'].id,known_before=list(p.known_proposals),existing=[{'id':v.id,'town':v.town_id,'sector':v.sector,'effect':v.desired_effect,'subject':v.subject_id,'status':v.status,'created_at':v.created_at} for v in self.w.proposals.values()])
                if tag=='membership':row.update(faction=x['f'].id,record_before=safe(x['f'].norms.get('invitations',{}).get(p.id)))
                if tag=='policy_work':row.update(policy=x['policy'].id,policy_before=safe(x['policy']))
                self.pending[id(frame)]=row
            elif tag=='execute':
                p=x['character'];self.executions_this_decision.add(p.id)
                n=next((n for n in p.needs.values() if n.id==x['goal'].need_id),None)
                fid=n.context.get('faction_id',n.target_id if n.kind in ('affiliation','organizational_access') else None) if n else None
                self.pending[id(frame)]={'action':x['goal'].action,'state':self.state(p),'faction':fid,'need':n.kind if n else None}
            elif tag=='death':
                p=x['person'];self.deaths.append({'state':self.state(p,True),'cause_argument':x['cause'],'last_decisions':list(self.rings[p.id]),'first_vital':self.first_vital.get(p.id,{})})
            return
        if tag=='refresh':
            p=x['character'];self.active[p.id]=[{'id':n.id,'kind':n.kind,'priority':n.priority,'base':n.base_urgency,'status':n.status,'target':n.target_id,'source':n.source} for n in arg]
            for n in arg:
                if n.kind=='political_pressure':self.detected_collective.add((p.id,n.id))
            for key,level in (('food',p.hunger),('water',p.thirst)):
                if level>=50:self.first_vital.setdefault(p.id,{}).setdefault(key,self.w.turn)
        elif tag=='evaluate':
            p,n=x['character'],x['need'];self.candidate_calls[n.kind]+=1
            if arg:self.candidate_viable[n.kind]+=1
            self.evals.setdefault(p.id,{})[n.id]=[{'action':s.action,'target':s.target_id,'score':s.score,'destination':safe(s.destination),'terms':safe(s.considerations),'feeding':safe(s.feeding)} for s in arg[:12]]
        elif tag=='decide':
            p=x['character'];selected=x.get('selected');choice=x.get('choice')
            if selected is None or choice is None:return
            active=self.active.get(p.id,[]);evaluations=self.evals.get(p.id,{})
            original=next((n for n in active if n['id']==selected.id),{})
            record={'hour':self.w.turn,'need':selected.kind,'priority':original.get('priority',selected.priority),'action':choice.action,
                    'score':choice.score,'target':choice.target_id,'alternatives':evaluations.get(selected.id,[]),'state_after':self.state(p),
                    'executed':p.id in self.executions_this_decision,'execution':self.last_execution.get(p.id) if p.id in self.executions_this_decision else None}
            self.rings[p.id].append(record);self.action_selected[choice.action]+=1;self.need_selections[selected.kind]+=1
            for n in active:
                if n['kind'] in INSTITUTIONAL and n['id']!=selected.id:
                    detail='not_evaluated' if n['id'] not in evaluations else 'evaluated_but_not_selected'
                    self.institutional_competition[f"{n['kind']} -> {selected.kind} ({detail})"]+=1
        elif tag=='execute':
            p=x['character'];row=self.pending.pop(id(frame));row['result']=safe(arg);self.last_execution[p.id]=row
            self.action_executed[row['action']]+=1
            if not arg[0]:self.action_failed[row['action']]+=1
            if row['faction']:
                self.faction_executions[row['faction']][row['action']]+=1
                if not arg[0]:self.faction_failures[row['faction']][row['action']]+=1
        elif tag=='affinity' and self.codes.get(frame.f_back.f_code)=='acceptable':
            p=x['p'];score=arg;self.affinity_values.append(score)
            self.last_affinity[p.id][x['q'].id]={'score':score,'trust':x.get('trust'),'friendship':x.get('bond'),'same_profession':p.profession==x['q'].profession}
            if score<25:
                self.affinity_rejected.add(p.id);self.affinity_pairs[(p.id,x['q'].id)]+=1
                if len(self.affinity_samples)<12:self.affinity_samples.append({'hour':self.w.turn,'person':p.id,'leader':x['q'].id,'score':score,'trust':x.get('trust'),'friendship':x.get('bond'),'compassion':p.personality.compassion,'ambition':p.personality.ambition,'same_profession':p.profession==x['q'].profession,'family':any(f"{p.id}:{x['q'].id}:{kind}" in self.w.relationships for kind in ('pai_de','filho_de','casamento'))})
        elif tag=='acceptable':
            if not arg[0]:self.reasons_by_actor[x['p'].id].add(arg[1])
            check={'hour':self.w.turn,'group':x['g'].id,'ok':arg[0],'reason':arg[1]}
            if arg[1] in ('low_social_affinity','shared_problem_and_access'):check['affinity']=self.last_affinity[x['p'].id].get(x['g'].leader_id)
            self.group_checks[x['p'].id].append(check)
            parent=frame.f_back.f_back
            if parent and id(parent) in self.pending and 'group_checks' in self.pending[id(parent)]:self.pending[id(parent)]['group_checks'].append(check)
        elif tag=='meeting':
            g=x['g'];present=x['present']
            self.meeting_gates.append({'hour':self.w.turn,'group':g.id,'success':arg[0],'status':g.status,'meetings':g.investment,
               'age':self.w.turn-g.created_at,'members':len(g.member_ids),'present':len(present),'rich_present':sum(p.money>15 for p in present)})
        elif tag=='formalize':
            self.formalization_rows.append({'hour':self.w.turn,'group':x['g'].id,'score':x['score'],'age':x['age'],'funds':x['funds'],
                                          'present':len(x['present']),'execute':x['execute'],'result':getattr(arg,'id',None)})
        elif tag=='search':
            parent=self.pending.get(id(frame.f_back))
            if parent is not None:parent['search_found']=[g.id for g in arg]
        elif tag in ('form','propose','membership','policy_work'):
            row=self.pending.pop(id(frame));p=x['p'];row['result']=safe(arg) if tag not in ('form','propose') else getattr(arg,'id',None)
            if tag=='form' and arg and arg.id not in row.pop('existing_ids'):
                if len(self.group_samples)<48:row['group']=arg.id;self.group_samples.append(row)
            elif tag=='propose':
                row['known_after']=list(p.known_proposals)
                if len(self.proposal_samples)<80:self.proposal_samples.append(row)
            elif tag=='membership':
                row['record_after']=safe(x['f'].norms.get('invitations',{}).get(p.id));row['actual_contacts']=[q.id for q in x.get('contacts',[])];self.membership_samples.append(row)
            elif tag=='policy_work' and len(self.work_samples)<40:self.work_samples.append(row)
        elif tag=='political_scores':
            self.political_samples.append({'hour':self.w.turn,'mayor':self.state(x['p'],True),'proposal':x['prop'].id,'pressure':x['pressure'],'pressure_state':safe(x['prop'].pressure_state),'town_money':x['t'].money,'cost':x['cost'],'avoid':x['avoid'],'scores':safe(arg)})
        elif tag=='faction_candidates':
            f=x.get('f')
            if f:
                self.faction_choices[f.id]['calls']+=1
                for a,_,_ in arg or []:self.faction_choices[f.id][a]+=1
        elif tag=='worker_eligible' and arg and x['policy'].id in x['p'].known_policies:self.policy_eligible[x['policy'].id].add(x['p'].id)
        elif tag=='access_refresh':
            p=x['p']
            for f in self.w.factions.values():
                if any(self.w.characters[id].alive and self.w.characters[id].position==p.position and id!=p.id for id in f.member_ids):self.faction_contacts[f.id].add(p.id)
                if any(id in p.observations for id in f.member_ids):self.faction_member_knowers[f.id].add(p.id)

    def group_info(self,g):
        return {'id':g.id,'town':g.town_id,'cause':g.cause,'subject':g.subject_id,'leader':g.leader_id,'members':list(g.member_ids),
                'status':g.status,'created_at':g.created_at,'last_relevant':g.last_relevant,'last_meeting':g.last_meeting,'meetings':g.investment,
                'failures':g.failures,'pressure':g.pressure,'money':g.money,'plan':safe(g.plan),'proposals':list(g.proposal_ids)}

    def checkpoint(self):
        for id,g in self.w.groups.items():
            old=self.previous_members.get(id,set());current=set(g.member_ids)
            for p in old-current:self.group_removals[id].append({'hour':self.w.turn,'person':p,'dead':not self.w.characters[p].alive,'group_status':g.status})
            self.previous_members[id]=current
            self.last_groups[id]=self.group_info(g)
        for id in self.last_groups.keys()-self.w.groups.keys():
            if id not in self.retired_groups:self.retired_groups[id]={**self.last_groups[id],**self.groups.get(id,{}),'removed_at':self.w.turn,'removals':self.group_removals.get(id,[])}
        for policy in self.w.institutional_policies.values():
            for p in self.w.characters.values():
                if p.alive and policy.id in p.known_policies:
                    self.policy_awareness[policy.id].add(p.id);self.policy_awareness_hours[policy.id][p.id]+=1
        if self.w.turn%25==0:
            self.temporal.append({'hour':self.w.turn,'alive':sum(p.alive for p in self.w.characters.values()),'deaths':dict(Counter(r['cause'] for r in self.w.death_records.values())),
                                  'groups':len(self.w.groups),'events':dict(self.events)})

    def finish(self):
        w=self.w
        for row in self.deaths:row['record']=safe(w.death_records.get(row['state']['id'],{}))
        group_rows=[]
        for id,g in w.groups.items():
            row={**self.group_info(g),**self.groups.get(id,{})};row['removals']=self.group_removals.get(id,[])
            row['final_members']=list(g.member_ids);row['actor_links']=[p.id for p in w.characters.values() if id in p.group_ids]
            row['leader_state']=self.state(w.characters[g.leader_id],True)
            place=w.towns[g.town_id].market;present=[p for p in w.characters.values() if p.id in g.member_ids and p.alive and p.position==place]
            age=w.turn-g.created_at;funds=sum(min(2,max(0,p.money-15)) for p in present)
            score=min(100,min(25,age/8)+g.failures*8+g.investment*5+min(15,len(present)*3)+min(15,funds*2))
            row['formalization_at_market']={'derived_not_executed':True,'score':score,'age':age,'present':len(present),'funds':funds,'threshold':65,
                  'gates':{'active':g.status=='active','meetings_ge4':g.investment>=4,'age_ge168':age>=168,'members_ge3':len(g.member_ids)>=3,
                           'rich_present_ge2':sum(p.money>15 for p in present)>=2,'present_ge3':len(present)>=3,'funds_ge4':funds>=4,'score_ge65':score>=65,
                           'leader_present':any(p.id==g.leader_id for p in present),'leader_alive':w.characters[g.leader_id].alive,
                           'faction_world_capacity':len(w.factions)<24,'organizational_capacity':all(len(w.characters[i].organization_ids)<3 for i in g.member_ids)}}
            group_rows.append(row)
        proposal_rows=[]
        for p in w.proposals.values():
            row=safe(p);g=w.groups.get(p.group_id);t=w.towns[p.town_id]
            row['representative']=self.state(w.characters[g.leader_id],True) if g else None
            row['mayor']=self.state(w.characters[t.mayor_id],True) if t.mayor_id else None
            row['in_received_office']=p.id in t.office.get('known_proposals',[]);row['public']=p.id in t.office.get('public_proposals',[])
            proposal_rows.append(row)
        fs=[]
        for f in w.factions.values():
            frow={'id':f.id,'name':f.name,'status':f.status,'members':list(f.member_ids),'leader':f.leader_id,'hq':f.headquarters_id,'money':f.money,'purpose':f.purpose,
                  'inventory':{k:self.count_items(f,k) for k in ('food','water','weapon','tool','grain')},'professions':dict(Counter(w.characters[i].profession for i in f.member_ids)),
                  'capabilities':self.e.institutions.capabilities(f,w.characters[f.leader_id]),'pressure':safe(f.action_pressure),'local_status':safe(f.local_status),
                  'knowers':[p.id for p in w.characters.values() if f.id in p.known_factions],
                  'location_knowers':[p.id for p in w.characters.values() if f.headquarters_id in p.place_knowledge],
                  'contact_people':sorted(self.faction_contacts[f.id]),'invitations':safe(f.norms.get('invitations',{})),
                  'member_observation_people':sorted(self.faction_member_knowers[f.id]),'basic_eligible':[p.id for p in w.characters.values() if p.alive and f.id in p.known_factions and not p.organization_ids and f.status=='active'],
                  'executions':dict(self.faction_executions[f.id]),'execution_failures':dict(self.faction_failures[f.id]),
                  'candidates_observed':dict(self.faction_choices[f.id]),'leader_state':self.state(w.characters[f.leader_id],True),'invited_states':{id:self.state(w.characters[id],True) for id in f.norms.get('invitations',{}) if id in w.characters}}
            fs.append(frow)
        towns=[{'id':t.id,'name':t.name,'capital':t.capital,'kind':t.kind,'kingdom':t.kingdom_id,'named_alive':sum(w.characters[i].alive for i in t.resident_ids),
                'abstract':t.abstract_population,'money':t.money,'inventory':{k:self.count_items(t,k) for k in ('food','water','grain','iron','wood')},
                'infrastructure':t.infrastructure,'economy':safe(t.economic_report),'market':safe(t.market)} for t in w.towns.values()]
        metrics={'seed':SEED,'rules':RULES_VERSION,'generation':GENERATION_VERSION,'hours':w.turn,'events':dict(self.events),'world_metrics':w.metrics,
                 'calls':dict(self.calls),'temporal':self.temporal,'checks':self.checks,'deaths':dict(Counter(x['cause'] for x in w.death_records.values())),
                 'observer_errors':dict(self.observer_errors),'observer_error_samples':self.observer_error_samples,
                 'named_alive':sum(p.alive for p in w.characters.values()),'named_total':len(w.characters),'abstract':sum(t.abstract_population for t in w.towns.values()),
                 'towns':towns,'groups':group_rows,'retired_groups':list(self.retired_groups.values()),'proposals':proposal_rows,'policies':safe(list(w.institutional_policies.values())),'factions':fs,
                 'candidate_calls':dict(self.candidate_calls),'candidate_viable':dict(self.candidate_viable),'need_selected':dict(self.need_selections),
                 'action_selected':dict(self.action_selected),'action_executed':dict(self.action_executed),'action_failed':dict(self.action_failed),
                 'institutional_competition':dict(self.institutional_competition),'unique_collective_needs':len(self.detected_collective),
                 'affinity':{'distribution':distribution(self.affinity_values),'rejected_people':len(self.affinity_rejected),
                    'only_affinity_people':sum(rs=={'low_social_affinity'} for rs in self.reasons_by_actor.values()),
                    'repeated_pairs':sum(v>1 for v in self.affinity_pairs.values()),'low_pairs':len(self.affinity_pairs),'low_attempts':sum(self.affinity_pairs.values()),
                    'examples':self.affinity_samples},'policy_awareness':{id:len(v) for id,v in self.policy_awareness.items()},
                 'meeting_gates':self.meeting_gates,'formalization_evaluations':self.formalization_rows,
                 'policy_eligible_aware':{id:len(v) for id,v in self.policy_eligible.items()},'routes':{'count':len(w.routes),'traversals':sum(x.uses for x in w.routes.values())}}
        traces={'group_creation':self.group_samples,'proposal_creation':self.proposal_samples,'membership':self.membership_samples,'political':self.political_samples,
                'policy_work':self.work_samples,'deaths':self.deaths,'events':self.semantic}
        dump(OUT/'metrics.json',safe(metrics));dump(OUT/'traces.json',safe(traces))

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    manifest=json.loads((OUT/'manifesto.json').read_text())
    if 'campaign' in manifest:raise RuntimeError('A campanha já foi iniciada. Não sobrescrever nem escolher outra seed.')
    started=time.monotonic();code=fingerprint()
    w=generate_world(SEED,with_player=False,config=GenerationConfig(historical_turns=0));e=Engine(w);audit=Audit(e)
    manifest['campaign']={'seed':SEED,'rules':RULES_VERSION,'generation':GENERATION_VERSION,'code_sha256':code,'hours_requested':300,
                          'initial_named':len(w.characters),'initial_abstract':sum(t.abstract_population for t in w.towns.values()),'restarts':len(manifest.get('interrupted_attempts',[])),
                          'observer_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                          'observer':'sys.setprofile externo, somente leituras; debug desativado; sem substituição de funções'}
    dump(OUT/'manifesto.json',manifest);e.bus.subscribe('*',audit.event)
    print(json.dumps(manifest['campaign']),flush=True)
    try:
        for _ in range(HOURS):
            sys.setprofile(audit.profile)
            try:e.step()
            finally:sys.setprofile(None)
            audit.checkpoint()
            if w.turn%25==0:
                errors=validate_world(w);audit.checks.append({'hour':w.turn,'errors':errors})
                if errors:raise RuntimeError(str(errors[:8]))
                print(json.dumps({'hour':w.turn,'alive':sum(p.alive for p in w.characters.values()),'groups':audit.events['NewGroupCreated'],
                                  'joins':audit.events['GroupJoined'],'decisions':audit.events['PolicyDecided'],'seconds':round(time.monotonic()-started,1)}),flush=True)
        assert fingerprint()==code,'Fontes do motor alteradas durante a campanha.'
        errors=e.geography.audit()
        if errors:raise RuntimeError(str(errors[:6]))
        audit.finish();JsonRepository().save(w,OUT/'save_temporario.json')
        manifest['campaign'].update(hours_completed=w.turn,runtime_seconds=round(time.monotonic()-started,2),route_errors=errors,code_sha256_after=fingerprint())
        dump(OUT/'manifesto.json',manifest)
    except Exception as error:
        dump(OUT/'falha_auditoria.json',{'hour':w.turn,'seed':SEED,'exception':repr(error),'checks':audit.checks})
        raise
    print(json.dumps({'complete':w.turn,'runtime':manifest['campaign']['runtime_seconds'],'code_unchanged':True}),flush=True)

if __name__=='__main__':main()
