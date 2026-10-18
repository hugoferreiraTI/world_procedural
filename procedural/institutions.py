"""Continuidade institucional sobre Sociedade, Need/Goal, itens, trabalho e eventos."""
from .models import MaterialCandidate
from .organization_context import organization_id, bind_organization
from dataclasses import asdict
from .models import Proposal, Policy, Fact, Location

ACTIONS = {'policy_work','support_proposal','institutional_patrol','institutional_purchase',
           'institutional_supply','institutional_raid','institutional_response','institutional_support'}
ACTIVE_PROPOSALS = {'draft','submitted','deferred','ignored','accepted','partial'}
INVITATIONS = {'offered','considering','conditioned','conditional','deferred','delayed'}
SECTORS = {'water_access':'WATER','resource_pressure':'FOOD','security':'SECURITY',
           'religious_interest':'SECURITY','criminal_cooperation':'SECURITY'}


class Institutions:
    def __init__(self,e):
        self.e,self.w=e,e.world

    def bootstrap(self):
        for t in self.w.towns.values():
            t.infrastructure.setdefault('water_daily',80)
            t.infrastructure.setdefault('water_storage',160)
            t.infrastructure.setdefault('water_work',0)

    def emit(self,kind,p,target=None,parent_event_ids=(),**context):
        return self.e.recorder.emit(kind,f'{p.name}: {kind}.',p.id,target,p.position,
                                   historical=True,context=context,parent_event_ids=parent_event_ids)

    def remember(self,book,id,row,limit=64):
        book[id]=row
        while len(book)>limit:book.pop(next(iter(book)))

    def know_group(self,p,g,source,source_fact=None):
        if g.id in p.known_groups:return
        self.remember(p.known_groups,g.id,{'source':source,'source_fact':source_fact,
                      'learned_at':self.w.turn,'meeting':asdict(self.w.towns[g.town_id].market),
                      'strategy':g.plan.get('strategy',g.cause if g.cause=='criminal_cooperation' else 'cooperation'),'dues':g.plan.get('dues',0)})
        self.emit('GroupKnown',p,g.id,group_id=g.id,source=source,source_fact=source_fact)

    def on_fact(self,p,fact):
        ctx=fact.context
        gid=ctx.get('group_id') or (fact.target_id if fact.kind in ('GroupFormed','GroupJoined','GroupMeeting','GroupKnown') else None)
        g=self.w.groups.get(gid)
        if g and fact.confidence>=30:self.know_group(p,g,'received_fact',fact.event_id)
        propid=ctx.get('proposal_id') or (fact.target_id if fact.kind in ('ProposalCreated','ProposalSupported','PolicyDecided') else None)
        prop=self.w.proposals.get(propid)
        if prop and fact.confidence>=30:
            self.remember(p.known_proposals,prop.id,{'source_fact':fact.event_id,'learned_at':self.w.turn})
        policyid=ctx.get('policy_id') or (fact.target_id if fact.kind in ('PolicyCreated','PolicyEffect','PolicyBlocked','PolicyCompleted') else None)
        policy=self.w.institutional_policies.get(policyid)
        if policy and fact.confidence>=30:
            self.remember(p.known_policies,policy.id,{'source_fact':fact.event_id,'learned_at':self.w.turn,'status':policy.status})
            for gid in self.w.proposals[policy.proposal_id].supporting_group_ids:
                g=self.w.groups.get(gid)
                if not g or p.id not in g.member_ids:continue
                if fact.kind in ('PolicyEffect','PolicyBlocked','PolicyCompleted'):
                    seen=g.plan.setdefault('policy_effects',{})
                    if seen.get(policy.id)==fact.event_id:continue
                    seen[policy.id]=fact.event_id
                    while len(seen)>12:seen.pop(next(iter(seen)))
                    self.e.society.remember(g,fact)
                    if fact.kind=='PolicyBlocked':g.failures=min(12,g.failures+1)
                    elif fact.kind=='PolicyEffect':
                        g.plan['last_material_effect']=fact.event_id
                        g.failures=max(0,g.failures-1)
                        # Alívio requer observação do próprio problema, não apenas aprovação.
                        own=self.e.society.pressure(p)
                        if not own or own[:2]!=(g.cause,g.subject_id):g.pressure=max(0,g.pressure-15)
        if fact.kind in ('ItemStolen','CharacterKilled') and fact.actor_id==p.id and not ctx.get('lawful'):
            crimes=p.social_state.setdefault('own_crime_facts',[])
            if fact.event_id not in crimes:crimes.append(fact.event_id);del crimes[:-8]
        fid=ctx.get('faction_id')
        faction=self.w.factions.get(fid)
        if faction and fact.kind=='FactionAction' and fact.confidence>=60:
            t=self.w.towns.get(p.town_id)
            if t and t.mayor_id==p.id and fact.location and fact.location.map_id==t.id:
                self.authority_response(p,faction,fact)
        if fact.kind=='FactionLocalStatusChanged' and fact.confidence>=60:
            faction=self.w.factions.get(fact.target_id)
            if faction and p.id in faction.member_ids:
                p.social_state.setdefault('known_faction_law',{})[faction.id]={'status':ctx['status'],'town_id':ctx['town_id'],'source_fact':fact.event_id}

    def own_pressure(self,p):
        t=self.w.towns.get(p.position.map_id)
        if t:
            wells=[v for k,v in p.known_places.items() if k.startswith('well')]
            if p.position==t.market or p.position in wells:
                if self.e.items.count(t.id,'water')==0 and p.thirst>=45:
                    since=p.social_state.setdefault('water_shortage_since',self.w.turn)
                    return 'water_access',None,min(90,45+p.thirst*.35+(self.w.turn-since)/8)
                if self.e.items.count(t.id,'water'):
                    p.social_state.pop('water_shortage_since',None)
        if p.thirst>=45 and 'water_shortage_since' in p.social_state:
            return 'water_access',None,min(90,45+p.thirst*.35)
        if p.personality.honesty<35 and p.personality.greed>=60 and len(p.social_state.get('own_crime_facts',[]))>=2:
            for f in p.knowledge.values():
                q=self.w.characters.get(f.actor_id)
                if (f.kind=='ItemStolen' and q and q.id!=p.id and f.confidence>=60 and self.w.turn-f.turn<=168
                    and q.id in self.e.spatial.at(p.position) and self.e.graph.value(p.id,q.id,'confiança',10)>=30):
                    return 'criminal_cooperation',None,65
        return None

    def group_compatibility(self,p,g,cause,subject):
        from .organizational_compatibility import assess
        return assess(self.e,p,g,cause,subject)

    def acceptable_group(self,p,g,cause,subject):
        result=self.group_compatibility(p,g,cause,subject)
        return result.acceptable,result.reason

    def search_groups(self,p,cause,subject,audit=True):
        if audit and self.w.turn-p.social_state.get('last_group_search',-1000)>=12:
            p.social_state['last_group_search']=self.w.turn
            self.emit('GroupSearchAttempt',p,cause=cause,subject=subject,known=len(p.known_groups))
        result=[]
        for gid in p.known_groups:
            g=self.w.groups.get(gid)
            if not g or p.id in g.member_ids or g.town_id!=p.town_id:continue
            compatibility=self.group_compatibility(p,g,cause,subject)
            ok,reason=compatibility.acceptable,compatibility.reason
            if audit and hasattr(self.e,'audit') and g.cause==cause:
                self.e.audit.count('compatibility:'+str(int(compatibility.score//10)*10))
                self.e.audit.sample('compatibility',{'actor':p.id,'group':g.id,'turn':self.w.turn,
                    'score':compatibility.score,'reason':reason,'components':compatibility.components},256)
            if ok:result.append(g)
            elif audit and g.cause==cause and g.subject_id==subject:
                key=f'group_rejected:{gid}'
                if self.w.turn-p.social_state.get(key,-1000)>=24:
                    p.social_state[key]=self.w.turn
                    self.emit('GroupJoinRejected',p,gid,reason=reason,compatibility=compatibility.score,components=compatibility.components)
        if result and audit:
            chosen=max(result,key=lambda g:(len(g.member_ids),-g.created_at))
            if p.social_state.get('last_group_found')!=chosen.id:
                p.social_state['last_group_found']=chosen.id
                self.emit('ExistingGroupFound',p,chosen.id,cause=cause,source=p.known_groups[chosen.id])
        return sorted(result,key=lambda g:(-self.group_compatibility(p,g,cause,subject).score,-len(g.member_ids),g.created_at,g.id))

    def collective_candidates(self,p,n):
        cause=n.context['cause'];subject=n.context.get('subject')
        choices=[]
        groups=self.search_groups(p,cause,subject)
        if groups:
            g=groups[0]
            if p.position.map_id!=g.town_id:return self.e.geography.candidates(p,g.town_id,'collective_contact',n)
            return [('join_group',Location(**p.known_groups[g.id]['meeting']),g.id)]
        if self.w.turn-p.social_state.get('last_share',-1000)>=24:choices.append(('share_problem',None,None))
        if len(p.group_ids)<3 and not any(self.w.groups[i].cause==cause and self.w.groups[i].subject_id==subject for i in p.group_ids if i in self.w.groups):
            if self.e.society.shared_facts(p,cause,subject):choices.append(('organize',None,None))
        if not choices:choices.append(('share_problem',self.w.towns[p.town_id].market,None))
        return choices

    def join(self,p,g):
        self.emit('GroupJoinAttempt',p,g.id)
        if g.id not in p.known_groups:return False,'Grupo desconhecido.'
        ok,reason=self.acceptable_group(p,g,g.cause,g.subject_id)
        contacts=[q for q in self.e.society.living(g.member_ids) if q.position==p.position]
        if not ok or not contacts or not self.e.society.compatible(p,g.cause,g.subject_id) or len(g.member_ids)>=64:
            self.emit('GroupJoinRejected',p,g.id,reason=reason if not ok else 'contact_or_capacity')
            return False,'Grupo não disponível para adesão presente.'
        if p.id in g.member_ids:return False,'Já participa.'
        g.member_ids.append(p.id);p.group_ids.append(g.id);g.support[p.id]=self.e.society.affinity(p,self.w.characters[g.leader_id],g.cause)
        g.last_relevant=self.w.turn
        self.emit('GroupJoined',p,g.id,group_id=g.id,contact=contacts[0].id,reason='known_compatible_group')
        self.e.society.count('group_joined')
        for id in g.proposal_ids:
            prop=self.w.proposals.get(id)
            if prop and prop.status in ACTIVE_PROPOSALS:self.support(p,g,prop)
        return True,'Adesão por contato e problema compartilhado.'

    def register_group(self,p,g):
        g.plan.setdefault('objective',g.cause)
        for q in self.e.society.living(g.member_ids):self.know_group(q,g,'founder')
        parent=self.e.observability.index.reference('GroupFormed',g.id)
        self.emit('NewGroupCreated',p,g.id,group_id=g.id,cause=g.cause,members=g.member_ids,parent_event_ids=[parent] if parent else [])
        if hasattr(self.e,'tasks'):
            self.e.tasks.authorize(p,g)
            self.e.tasks.issue(p,'group',g.id,'hold_meeting',g.id,self.w.towns[g.town_id].market,55,{'not_before':self.w.turn+24,'source_facts':[parent] if parent else []})

    def proposal_key(self,g):
        sector=SECTORS.get(g.cause,'EMPLOYMENT')
        effect={'water_access':'increase_capacity','security':'patrol','resource_pressure':'produce',
                'religious_interest':'cult_recognition','criminal_cooperation':'legal_access'}.get(g.cause,'commission_work')
        return sector,effect

    def public_proposals(self,p):
        t=self.w.towns.get(p.position.map_id)
        if not t or p.position!=t.market:return
        for id in t.office.get('public_proposals',[]):
            if id in self.w.proposals:self.remember(p.known_proposals,id,{'source':'public_submission','learned_at':self.w.turn})

    def support(self,p,g,prop):
        # Apoio apenas de membros presentes: não lê consentimento de gente distante.
        if prop.id not in p.known_proposals and g.id not in prop.supporting_group_ids:return False
        present=[q.id for q in self.e.society.living(g.member_ids) if q.position==p.position]
        added=set(present)-set(prop.supporter_ids)
        new_group=g.id not in prop.supporting_group_ids
        prop.support_by_group[g.id]=sorted(set(prop.support_by_group.get(g.id,[]))|set(present))
        prop.supporter_ids=sorted(set(prop.supporter_ids)|set(present));prop.support=len(prop.supporter_ids)
        if new_group:prop.supporting_group_ids.append(g.id)
        if g.town_id not in prop.affected_locality_ids:prop.affected_locality_ids.append(g.town_id)
        if prop.id not in g.proposal_ids:g.proposal_ids.append(prop.id);del g.proposal_ids[:-6]
        g.proposal_knowledge[prop.id]={'status':prop.status,'source_fact':prop.source_fact,'confidence':100}
        self.remember(p.known_proposals,prop.id,{'source':'own_support','learned_at':self.w.turn})
        prop.urgency=max(prop.urgency,g.pressure)
        if prop.id in self.w.towns[prop.town_id].office.get('public_proposals',[]):
            g.plan['proposal_delivery_needed']=prop.id
        self.pressure(prop,p)
        if added or new_group:self.emit('ProposalSupported',p,prop.id,proposal_id=prop.id,group_id=g.id,added_people=sorted(added),supporter_ids=list(prop.supporter_ids),supporting_groups=list(prop.supporting_group_ids))
        return True

    def propose(self,p,g):
        t=self.e.collective.authority(g)
        if not t or t.mayor_id is None:return None
        self.public_proposals(p);sector,effect=self.proposal_key(g)
        compatible=[self.w.proposals[i] for i in p.known_proposals if i in self.w.proposals
                    and self.w.proposals[i].town_id==t.id and self.w.proposals[i].sector==sector
                    and self.w.proposals[i].desired_effect==effect and self.w.proposals[i].subject_id==g.subject_id
                    and self.w.proposals[i].status in ACTIVE_PROPOSALS
                    and (self.w.proposals[i].policy_id is None or self.w.institutional_policies.get(self.w.proposals[i].policy_id) and self.w.institutional_policies[self.w.proposals[i].policy_id].status in ('active','stalled'))]
        if compatible:
            prop=min(compatible,key=lambda x:x.created_at)
            self.emit('CompatibleProposalFound',p,prop.id,proposal_id=prop.id,group_id=g.id)
            self.support(p,g,prop);return prop
        if len(t.proposal_ids)>=24:return None
        solution={'WATER':'water_capacity','FOOD':'food_production','SECURITY':'security_funding'}.get(sector,'commission_work')
        if g.cause=='religious_interest':solution='recognize_cult'
        prop=Proposal(self.w.allocate_id(),g.id,t.id,t.mayor_id,g.cause,g.cause,solution,g.pressure,0,self.w.turn,g.originating_fact,
                      subject_id=g.subject_id,sector=sector,desired_effect=effect)
        self.w.proposals[prop.id]=prop;t.proposal_ids.append(prop.id)
        self.remember(p.known_proposals,prop.id,{'source':'author','learned_at':self.w.turn})
        self.support(p,g,prop)
        parent=self.e.observability.index.reference('GroupFormed',g.id)
        self.emit('ProposalCreated',p,prop.id,proposal_id=prop.id,group_id=g.id,sector=sector,effect=effect,source_fact=g.originating_fact,parent_event_ids=[parent] if parent else [])
        self.e.society.count('proposal_created')
        if hasattr(self.e,'tasks'):
            self.e.tasks.authorize(p,g)
            self.e.tasks.issue(p,'group',g.id,'deliver_proposal',prop.id,t.market,55,{'source_facts':[self.e.observability.index.reference('ProposalCreated',prop.id)]})
        return prop

    def faction_support(self,p,f,prop):
        if (p.id!=f.leader_id or f.status!='active' or prop.id not in p.known_proposals
            or prop.status not in ACTIVE_PROPOSALS or p.position!=self.w.towns[prop.town_id].market):
            return False,'Apoio institucional exige proposta conhecida e representante presente.'
        present=[q.id for q in self.e.society.living(f.member_ids) if q.position==p.position]
        added=set(present)-set(prop.supporter_ids)
        if f.id in prop.supporting_faction_ids and not added:return False,'Apoio já registrado.'
        prop.supporter_ids=sorted(set(prop.supporter_ids)|set(present));prop.support=len(prop.supporter_ids)
        prop.delivered_supporter_ids=sorted(set(prop.delivered_supporter_ids)|set(present))
        if f.id not in prop.supporting_faction_ids:prop.supporting_faction_ids.append(f.id)
        if p.position.map_id not in prop.affected_locality_ids:prop.affected_locality_ids.append(p.position.map_id)
        self.pressure(prop,p)
        self.emit('FactionProposalSupported',p,prop.id,proposal_id=prop.id,faction_id=f.id,
                  added_people=sorted(added),supporter_ids=list(prop.supporter_ids))
        return True,'Apoio de membros presentes, sem bônus político artificial.'

    def deliver_support(self,p,prop,g):
        t=self.w.towns[prop.town_id]
        if p.position!=t.market or p.id not in self.e.tasks.representatives(g) or prop.id not in g.proposal_ids:return False,'Apoio precisa chegar à jurisdição.'
        prop.delivered_supporter_ids=sorted(set(prop.delivered_supporter_ids)|set(prop.support_by_group.get(g.id,[])))
        g.plan.pop('proposal_delivery_needed',None)
        self.pressure(prop,p)
        self.emit('ProposalSupportDelivered',p,prop.id,proposal_id=prop.id,group_id=g.id,supporter_ids=list(prop.delivered_supporter_ids),source_fact=prop.source_fact)
        return True,'Apoios assinados entregues sem duplicar pessoas.'

    def submit(self,p,prop):
        t=self.w.towns[prop.town_id];mayor=self.w.characters.get(t.mayor_id)
        g=next((self.w.groups[i] for i in prop.supporting_group_ids if i in self.w.groups and p.id in self.e.tasks.representatives(self.w.groups[i])),None)
        receivers=[q for q in self.e.society.living([t.mayor_id]+list(t.office.get('clerks',()))) if q.position==p.position]
        if not g or not mayor or not receivers or p.position!=t.market or prop.status not in ('draft','submitted','deferred','ignored'):return False,'Representante e autoridade devem se encontrar.'
        prop.status='submitted';prop.target_id=mayor.id
        for key in ('public_proposals','known_proposals'):
            ids=t.office.setdefault(key,[])
            if prop.id not in ids:ids.append(prop.id)
            del ids[:-24]
        self.deliver_support(p,prop,g)
        parent=self.e.observability.index.reference('ProposalCreated',prop.id)
        submitted=self.emit('ProposalSubmitted',p,receivers[0].id,receiver_id=receivers[0].id,authority_id=mayor.id,proposal_id=prop.id,group_id=g.id,supporter_ids=list(prop.delivered_supporter_ids),source_fact=prop.source_fact,parent_event_ids=[parent] if parent else [])
        self.e.tasks.closed_by_event('deliver_proposal',prop.id,submitted,p)
        g.proposal_knowledge[prop.id]={'status':'submitted','confidence':100,'source_fact':prop.source_fact}
        return True,'Proposta e apoio recebidos presencialmente.'

    def pressure(self,prop,p=None):
        t=self.w.towns[prop.town_id]
        age=min(20,(self.w.turn-prop.created_at)/6)
        visibility=10 if prop.id in t.office.get('known_proposals',[]) else 2
        crisis=10 if t.economic_report.get('deficit',0) or prop.urgency>=70 else 0
        living=sum(self.w.characters[i].alive for i in prop.delivered_supporter_ids)
        value=min(100,living*2+prop.urgency*.3+age+visibility+crisis)
        previous=prop.pressure;prop.pressure=value
        prop.pressure_state={'unique_support':living,'severity':prop.urgency,'persistence':age,'visibility':visibility,'local_crisis':crisis,'affected_localities':list(prop.affected_locality_ids)}
        if p and abs(previous-value)>=2:self.emit('PoliticalPressureChanged',p,prop.id,proposal_id=prop.id,previous=previous,pressure=value,factors=prop.pressure_state)
        return value

    def decision_scores(self,p,prop):
        t=self.w.towns[prop.town_id];pressure=self.pressure(prop)
        cost=25 if t.money<8 else 5
        # Sem capacidade material ou sob exaustão, uma demanda de baixa pressão
        # pode ser deixada sem encaminhamento. A alternativa não é dominada
        # matematicamente pela recusa em todos os contextos.
        avoid=(25 if t.money<2 and pressure<45 else 0)+(30 if p.fatigue>=85 and pressure<45 else 0)
        return {'approve':pressure*.55+p.personality.compassion*.3+p.personality.diligence*.15-cost-p.personality.greed*.15,
                'partial':22+pressure*.35+p.personality.diligence*.25-cost*.4,
                'reject':18+p.personality.greed*.45+p.personality.independence*.1-pressure*.15,
                'defer':25+p.personality.persistence*.2+cost*.6-pressure*.2,
                'ignore':p.personality.independence*.25+p.personality.greed*.25-pressure*.35+avoid}

    def create_policy(self,p,prop,partial=False):
        t=self.w.towns[prop.town_id]
        existing=next((v for v in self.w.institutional_policies.values() if v.jurisdiction==t.id and v.sector==prop.sector and v.objective==prop.desired_effect and v.status in ('active','stalled')),None)
        if existing:
            prop.policy_id=existing.id
            original=self.w.proposals[existing.proposal_id]
            original.supporting_group_ids=list(dict.fromkeys(original.supporting_group_ids+prop.supporting_group_ids))
            return existing
        budget=min(t.money,8 if partial else 16)
        if budget<2:return None
        t.money-=budget
        policy=Policy(self.w.allocate_id(),t.id,prop.id,prop.sector,prop.desired_effect,prop.pressure,budget,budget,self.w.turn,work_required=4 if partial else 8,source_fact=prop.source_fact)
        self.w.institutional_policies[policy.id]=policy;prop.policy_id=policy.id
        parent=self.e.observability.index.reference('ProposalSubmitted',context={'proposal_id':prop.id})
        event=self.emit('PolicyCreated',p,policy.id,policy_id=policy.id,proposal_id=prop.id,sector=policy.sector,objective=policy.objective,budget=budget,source_fact=prop.source_fact,parent_event_ids=[parent] if parent else [])
        policy.history.append(event.id)
        if hasattr(self.e,'tasks'):
            self.e.tasks.issue(p,'town',t.id,'work_policy',policy.id,t.market,55,{'source_facts':[event.id]},['worker'])
        return policy

    def resolve(self,p,prop):
        t=self.w.towns[prop.town_id]
        if t.mayor_id!=p.id or p.position!=t.market or prop.id not in t.office.get('known_proposals',[]) or prop.status not in ('submitted','deferred','ignored'):return False,'Proposta não foi recebida para decisão.'
        scores=self.decision_scores(p,prop);decision=max(scores,key=scores.get)
        policy=self.create_policy(p,prop,decision=='partial') if decision in ('approve','partial') else None
        if decision in ('approve','partial') and not policy:decision='defer'
        prop.status={'approve':'accepted','partial':'partial','reject':'rejected','defer':'deferred','ignore':'ignored'}[decision]
        prop.decided_at=self.w.turn
        prop.result={'decision':decision,'scores':scores,'reason':'pressure_personality_and_material_budget','political_pressure':prop.pressure,
                     'policy_id':policy.id if policy else None,'material':{'food':0,'money':0,'recipients':[]}}
        t.office.setdefault('decisions',[]).append(prop.id);del t.office['decisions'][:-12]
        parents=[self.e.observability.index.reference('ProposalSubmitted',context={'proposal_id':prop.id})]
        if policy:parents.append(self.e.observability.index.reference('PolicyCreated',policy.id))
        event=self.emit('PolicyDecided',p,prop.id,proposal_id=prop.id,group_id=prop.group_id,supporting_groups=list(prop.supporting_group_ids),town_id=t.id,solution=prop.solution,result=prop.result,parent_event_ids=[id for id in parents if id])
        self.emit('PolicyDecision',p,prop.id,proposal_id=prop.id,decision=decision,pressure=prop.pressure,reason=prop.result['reason'],policy_id=prop.policy_id)
        t.office.setdefault('public_responses',[]).append(Fact(event.id,event.kind,p.id,prop.id,p.position,self.w.turn,event.description,confidence=80,source_id=p.id,source_kind='known',context=event.context))
        del t.office['public_responses'][:-12]
        return True,'Decisão registra uma tentativa institucional; produção ainda depende de execução.'

    def react_decision(self,p,fact):
        prop=self.w.proposals.get(fact.target_id)
        if not prop:return
        for gid in prop.supporting_group_ids:
            g=self.w.groups.get(gid)
            if not g or p.id not in g.member_ids:continue
            record=g.proposal_knowledge.get(prop.id,{})
            if record.get('response_fact',-1)>fact.event_id:continue
            if record.get('response_fact')==fact.event_id:
                if fact.confidence>record.get('confidence',0):
                    record['confidence']=fact.confidence
                    if fact.context['result']['decision']=='reject' and fact.confidence>=60:g.responsibility_id=fact.actor_id
                continue
            decision=fact.context['result']['decision']
            g.proposal_knowledge[prop.id]={'status':{'approve':'accepted','partial':'partial','reject':'rejected','defer':'deferred','ignore':'ignored'}[decision],'confidence':fact.confidence,'response_fact':fact.event_id,'source_fact':fact.event_id}
            self.e.society.remember(g,fact)
            if decision in ('reject','defer','ignore'):
                g.failures=min(12,g.failures+1);g.pressure=min(100,g.pressure+5)
                g.action_pressure.failures=min(6,g.failures);g.action_pressure.updated_at=-1
                if decision=='reject' and fact.confidence>=60:
                    g.responsibility_id=fact.actor_id
            else:g.plan['awaiting_material_policy']=fact.context['result'].get('policy_id')
            p.social_state['meaningful_social_actions']=p.social_state.get('meaningful_social_actions',0)+1

    def worker_eligible(self,p,policy):
        return {'WATER':p.profession in ('mineiro','lenhador','ferreiro','agricultor'),
                'FOOD':p.profession in ('cozinheiro','agricultor','caçador'),
                'PROCESSING':p.profession=='cozinheiro','RAW_MATERIAL':p.profession in ('mineiro','lenhador','agricultor'),
                'WEAPONS':p.profession=='ferreiro','SECURITY':p.profession in ('guarda','soldado'),
                'EMPLOYMENT':self.e.professions.temporary_eligible(p),'TRANSPORT':p.profession=='comerciante'}.get(policy.sector,False)

    def policy_barrier(self,p,policy,reason):
        code='NO_WORKER' if reason=='worker_unfit' else 'INSUFFICIENT_MONEY' if reason=='budget_exhausted' else 'NO_KNOWN_ROUTE' if reason=='missing_known_route_or_cargo' else 'NO_INPUT'
        self.e.observability.gate('policy_work',code,policy.id,reason)
        if policy.barriers.get('reason')!=reason or self.w.turn-policy.barriers.get('at',-1000)>=24:
            policy.barriers={'reason':reason,'at':self.w.turn};policy.status='stalled'
            ev=self.emit('PolicyBlocked',p,policy.id,policy_id=policy.id,proposal_id=policy.proposal_id,sector=policy.sector,reason=reason)
            policy.history.append(ev.id);del policy.history[:-24]
        return False,'Política sem capacidade material: '+reason

    def policy_work(self,p,policy):
        t=self.w.towns[policy.jurisdiction]
        job=policy.effects.get('transport_jobs',{}).get(p.id)
        location=self.w.towns[job['destination']].market if job else p.workplace if policy.sector=='RAW_MATERIAL' else t.market
        if policy.id not in p.known_policies or p.position!=location or policy.status not in ('active','stalled') or not self.worker_eligible(p,policy):return False,'Trabalho institucional desconhecido ou inacessível.'
        if policy.money<1:return self.policy_barrier(p,policy,'budget_exhausted')
        if p.fatigue>=95 or p.health<30:return self.policy_barrier(p,policy,'worker_unfit')
        effect={};materials={}
        if policy.objective=='cult_recognition':
            prop=self.w.proposals[policy.proposal_id]
            t.policies.setdefault('cults',{})[str(prop.subject_id)]='recognized'
            effect={'cult_recognized':prop.subject_id}
        elif policy.sector=='WATER':
            if not self.e.items.count(t.id,'wood') or not self.e.items.count(t.id,'iron'):return self.policy_barrier(p,policy,'missing_wood_or_iron')
            self.e.items.consume(t.id,'wood');self.e.items.consume(t.id,'iron');materials={'wood':1,'iron':1}
            t.infrastructure['water_work']+=1
            if t.infrastructure['water_work']%2==0:
                before=t.infrastructure['water_daily'];t.infrastructure['water_daily']+=20;t.infrastructure['water_storage']+=40
                effect={'capacity_before':before,'capacity_after':t.infrastructure['water_daily'],'water_created':0}
            else:effect={'construction_progress':t.infrastructure['water_work'],'water_created':0}
        elif policy.sector in ('FOOD','PROCESSING','EMPLOYMENT'):
            before=self.e.items.count(t.id,'grain');produced=self.e.professions.prepare(t,min(4,max(0,240-self.e.items.count(t.id,'food'))))
            if not produced:return self.policy_barrier(p,policy,'missing_grain_or_storage')
            self.e.items.create(t.id,'food',produced,creator_id=p.id,origin='Trabalho financiado por política')
            self.e.professions.record_production(t,'food',produced)
            effect={'food_produced':produced};materials={'grain':before-self.e.items.count(t.id,'grain')}
        elif policy.sector=='WEAPONS':
            if self.e.items.count(t.id,'iron')<2 or not self.e.items.count(t.id,'wood'):return self.policy_barrier(p,policy,'missing_iron_or_wood')
            self.e.items.consume(t.id,'iron',2);self.e.items.consume(t.id,'wood');materials={'iron':2,'wood':1}
            item=self.e.items.create(t.id,'weapon',creator_id=p.id,origin='Encomenda institucional custeada');effect={'weapon_id':item.id}
        elif policy.sector=='RAW_MATERIAL':
            result=self.e.professions.work(p,1)
            if not result.success or not result.produced:return self.policy_barrier(p,policy,result.status)
            effect={'raw_produced':result.produced,'regular_wage':result.paid}
        elif policy.sector=='TRANSPORT':
            if not job:
                destinations=[]
                for id in p.known_towns:
                    dest=self.w.towns.get(id);plan=self.e.geography.plan(p,id)
                    if dest and id!=t.id and dest.kingdom_id==t.kingdom_id and plan:
                        destinations.append((self.e.geography.hours(p,plan),id))
                kind=next((k for k in ('grain','wood','iron') if self.e.items.count(t.id,k)>=3),None)
                if not destinations or not kind:return self.policy_barrier(p,policy,'missing_known_route_or_cargo')
                destination=min(destinations)[1]
                plan=self.e.geography.plan(p,destination);food,water=self.e.migration.supplies(p,self.e.geography.hours(p,plan))
                if self.e.items.count(p.id,'food')<food or self.e.items.count(p.id,'water')<water:
                    return self.policy_barrier(p,policy,'transport_supplies_missing')
                cargo=self.e.items.transfer(t.id,p.id,self.e.items.first(t.id,kind),3)
                policy.effects.setdefault('transport_jobs',{})[p.id]={'origin':t.id,'destination':destination,
                    'kind':kind,'quantity':3,'item_id':cargo.id,'assigned_at':self.w.turn}
                self.emit('PolicyTransportAssigned',p,policy.id,policy_id=policy.id,origin=t.id,destination=destination,
                          cargo_kind=kind,quantity=3,route_ids=plan[0])
                return True,'Carga material atribuída; pagamento exige chegada e entrega.'
            certificate=p.access_state.get('last_journey',{})
            if (certificate.get('origin')!=job['origin'] or certificate.get('destination')!=job['destination']
                or certificate.get('completed_at',-1)<job['assigned_at']):return self.policy_barrier(p,policy,'physical_arrival_unconfirmed')
            if self.e.items.count(p.id,job['kind'])<job['quantity']:return self.policy_barrier(p,policy,'cargo_lost')
            cargo=self.e.items.transfer(p.id,job['destination'],self.e.items.first(p.id,job['kind']),job['quantity'])
            effect={'cargo_delivered':job['quantity'],'cargo_kind':job['kind'],'destination':job['destination'],'item_id':cargo.id}
            policy.effects['transport_jobs'].pop(p.id)
        elif policy.sector=='SECURITY':
            self.e.conflicts.observe(p);self.w.metrics['PatrolPerformed']=self.w.metrics.get('PatrolPerformed',0)+1
            effect={'patrol':p.id,'observed_place':asdict(p.position)}
        else:return self.policy_barrier(p,policy,'specialized_assignment_unavailable')
        policy.money-=1;policy.spent+=1;p.money+=1;p.fatigue=min(100,p.fatigue+2)
        policy.work_done+=1;policy.last_work=self.w.turn;policy.status='active';policy.barriers={}
        if p.id not in policy.workers:policy.workers.append(p.id)
        for key,value in effect.items():
            if isinstance(value,(int,float)):policy.effects[key]=policy.effects.get(key,0)+value if key in ('food_produced','water_created') else value
        parent=self.e.observability.index.reference('PolicyCreated',policy.id)
        ev=self.emit('PolicyEffect',p,policy.id,policy_id=policy.id,proposal_id=policy.proposal_id,sector=policy.sector,effect=effect,materials=materials,wage=1,remaining_budget=policy.money,work_done=policy.work_done,parent_event_ids=[parent] if parent else [])
        policy.history.append(ev.id);del policy.history[:-24]
        if policy.work_done>=policy.work_required:
            policy.status='completed';t.money+=policy.money;policy.refunded+=policy.money;policy.money=0
            completed=self.emit('PolicyCompleted',p,policy.id,policy_id=policy.id,proposal_id=policy.proposal_id,work_done=policy.work_done,effects=policy.effects,refunded=policy.refunded,parent_event_ids=[ev.id])
            self.e.tasks.closed_by_event('work_policy',policy.id,completed,p)
        return True,'Trabalho real e salário do orçamento reservado.'

    def invitation_info(self,p,f):
        caps=self.capabilities(f,p)
        report=f.norms.get('hq_report',{})
        return {'benefits':{'protection':int(caps['patrol']),'food':self.e.items.count(f.id,'food')+report.get('food',0),
                            'water':self.e.items.count(f.id,'water')+report.get('water',0),'income':min(4,f.money),
                            'company':len(f.member_ids),'training':int(caps['train'])},
                'costs':{'dues':f.norms.get('dues',1),'risk':f.norms.get('risk',.4),'autonomy':.2},
                'reported_at':self.w.turn,'source':p.id}

    def membership_scores(self,p,f,record):
        info=record.get('terms',{});b=info.get('benefits',{});c=info.get('costs',{})
        benefit=(min(15,b.get('income',0)*4)*(1 if p.money<15 else .3)+min(20,b.get('food',0)*4)*p.hunger/100+
                 min(25,b.get('water',0)*5)*p.thirst/100+b.get('protection',0)*(20 if self.e.society.pressure(p) else 8)+
                 min(12,b.get('company',0)*4)+p.personality.ambition*.12+self.e.access.faction_fit(p,f)*.35+
                 b.get('training',0)*8)
        cost=c.get('dues',1)*3+p.personality.independence*.2+c.get('risk',.4)*(100-p.personality.courage)*.15
        if f.headquarters_id!=p.position.map_id and not self.e.geography.plan(p,f.headquarters_id):cost+=8
        if self.e.graph.value(p.id,record.get('inviter',f.leader_id),'confiança',10)<5:cost+=30
        return {'perceived_benefit':round(benefit,2),'perceived_cost':round(cost,2)}

    def membership(self,p,f,request=False):
        if f.id not in p.known_factions or p.organization_ids or f.status!='active':return False,'Organização não conhecida ou adesão indisponível.'
        contacts=[q for q in self.e.society.living(f.member_ids) if q.position==p.position]
        record=f.norms.setdefault('invitations',{}).setdefault(p.id,{'created_at':self.w.turn,'inviter':f.leader_id,'status':'considering'})
        if request:self.emit('FactionJoinRequest',p,f.id,leader=f.leader_id,reason='profession_values_or_need')
        if contacts:record['terms']=self.invitation_info(contacts[0],f);record['last_contact']=self.w.turn
        if not record.get('terms'):return False,'Ainda falta conhecer benefícios e deveres por contato.'
        if record.get('status') in ('rejected','accepted','expired_for_reason'):return False,'Resposta encerrada.'
        scores=self.membership_scores(p,f,record);record['evaluation']=scores
        if p.fatigue>=85 or p.health<45:
            record.update(status='deferred',reason='recovery',reconsider_after=self.w.turn+8)
            self.emit('FactionMembershipDeferred',p,f.id,reason='recovery',evaluation=scores)
            self.e.needs.satisfy(p,'affiliation');return True,'Adiado até recuperação, com continuação.'
        if p.personality.independence>=90 or scores['perceived_benefit']<scores['perceived_cost']:
            record.update(status='rejected',reason='cost_exceeds_benefit')
            self.emit('FactionMembershipRejected',p,f.id,reason=record['reason'],evaluation=scores)
            self.e.needs.satisfy(p,'affiliation');return True,'Recusa por avaliação própria de custos e benefícios.'
        if p.profession in ('guarda','soldado') and not self.e.items.count(p.id,'weapon') and record['terms']['costs']['risk']>=.6:
            record.update(status='conditioned',condition='equipment')
            if contacts and self.e.items.count(f.id,'weapon'):
                item=self.e.items.transfer(f.id,p.id,self.e.items.first(f.id,'weapon'));record['equipment_id']=item.id
            else:
                self.emit('FactionMembershipConditioned',p,f.id,condition='equipment',evaluation=scores)
                return True,'Condição de equipamento ainda não cumprida.'
        if not contacts:
            record.update(status='considering',reason='need_institutional_contact')
            return False,'Decisão favorável requer canal institucional para registrar ingresso.'
        if len(f.member_ids)>=64:return False,'Capacidade de admissão esgotada.'
        f.member_ids.append(p.id);p.organization_ids.append(f.id)
        f.assignments[p.id]={'rank':f.ranks[0],'deeds':0,'joined_at':self.w.turn}
        record.update(status='accepted',accepted_at=self.w.turn)
        self.emit('FactionMembershipAccepted',p,f.id,evaluation=scores,contact=contacts[0].id)
        self.emit('FactionMemberJoined',p,f.id,faction_id=f.id,rank=f.ranks[0])
        self.emit('FactionJoined',p,f.id,purpose=f.purpose)
        self.e.needs.satisfy(p,'affiliation');return True,'Ingresso aceito com benefício percebido, custo e contato real.'

    def capabilities(self,f,p):
        members=[q for q in self.e.society.living(f.member_ids) if q.position.map_id==p.position.map_id]
        supplied=[q for q in members if self.e.items.count(q.id,'food') and self.e.items.count(q.id,'water') and q.health>=30]
        guards=[q for q in supplied if q.profession in ('guarda','soldado')]
        hq=self.e.geography.place(f.headquarters_id)
        return {'patrol':bool(guards),'escort':bool(guards and len(supplied)>=2),
                'train':len(guards)>=2,'produce':any(q.profession in ('cozinheiro','ferreiro','agricultor','mineiro','caçador','lenhador') for q in supplied),
                'store':bool(hq),'guard':bool(guards),'investigate':bool(guards),
                'trade':any(q.profession=='comerciante' for q in supplied) and f.money>=2,
                'recruit':f.status=='active' and bool(members),
                'explore':len(supplied)>=2 and any(q.profession in ('mineiro','caçador') for q in supplied),
                'occupy':len(supplied)>=2 and bool(hq)}

    def can_formalize(self,p,g,present):
        """QUERY: única regra de formalização, também na execução direta."""
        if not g:return {'eligible':False,'reason_code':'NO_KNOWN_TARGET','present_ids':[]}
        present=[q for q in present if q.alive and q.id in g.member_ids and q.position==p.position]
        present=list({q.id:q for q in present}.values())
        age=self.w.turn-g.created_at;funds=sum(min(2,max(0,q.money-15)) for q in present)
        score=min(100,min(25,age/8)+g.failures*8+g.investment*5+min(15,len(present)*3)+min(15,funds*2))
        factors={'value':score,'age':age,'known_failures':g.failures,'meetings':g.investment,
                 'present_members':len(present),'available_contributions':funds}
        eligible=(g.status=='active' and g.cause!='expedition' and p.id==g.leader_id and p.id in [q.id for q in present]
                  and len(self.w.factions)<24 and g.investment>=4 and age>=168 and len(g.member_ids)>=3
                  and len(present)>=3 and sum(q.money>15 for q in present)>=2 and funds>=4 and score>=65
                  and not any(len(self.w.characters[i].organization_ids)>=3 for i in g.member_ids))
        ready=g.investment>=4 and age>=168 and len(g.member_ids)>=3 and sum(q.money>15 for q in present)>=2
        gates=[]
        if not p.alive or p.id!=g.leader_id:gates.append('NO_LEADER')
        if age<168:gates.append('TOO_YOUNG')
        if len(g.member_ids)<3:gates.append('TOO_FEW_MEMBERS')
        if len(present)<3:gates.append('NO_PRESENT_MEMBERS')
        if g.investment<4:gates.append('LOW_INVESTMENT')
        if sum(q.money>15 for q in present)<2:gates.append('NO_CONTRIBUTIONS')
        if funds<4:gates.append('INSUFFICIENT_FUNDS')
        if score<65:gates.append('LOW_SCORE')
        if len(self.w.factions)>=24:gates.append('WORLD_LIMIT')
        if any(len(self.w.characters[i].organization_ids)>=3 for i in g.member_ids):gates.append('MEMBERSHIP_LIMIT')
        if g.status!='active' or g.cause=='expedition':gates.append('INCOMPATIBLE')
        return {'eligible':eligible,'ready':ready,'gates':gates,'reason_code':None if eligible else 'FORMALIZATION_REQUIREMENTS',
                'present_ids':[q.id for q in present],'factors':factors}

    def formalization(self,p,g,present,execute=False):
        check=self.can_formalize(p,g,present)
        if hasattr(self.e,'audit'):
            self.e.audit.count('formalization:candidate')
            for gate in check.get('gates',()):self.e.audit.count('formalization_gate:'+gate)
        if not check.get('ready'):return None
        g.plan['formalization_pressure']=check['factors']
        if self.w.turn-g.plan.get('last_formalization_audit',-1000)>=24:
            g.plan['last_formalization_audit']=self.w.turn
            self.emit('FormalizationConsidered',p,g.id,group_id=g.id,factors=check['factors'])
        if execute and check['eligible']:return self.e.society.found_faction(p,g,present)
        return None

    def registered_faction(self,p,g,f):
        f.norms.update(origin_group_id=g.id,founders=list(f.member_ids),cause=g.cause,formalized_at=self.w.turn,
                       origin_history=list(g.memory),allow_theft=g.cause=='criminal_cooperation',harm_civilians=False)
        g.last_relevant=self.w.turn
        for q in self.e.society.living(f.member_ids):self.e.access.know_faction(q,f,'founder')
        self.emit('FactionFormalized',p,f.id,origin_group_id=g.id,founders=list(f.member_ids),cause=g.cause,factors=g.plan.get('formalization_pressure',{}))

    def authority_response(self,p,f,fact):
        t=self.w.towns[p.town_id];previous=f.local_status.get(t.id,{})
        seen=list(previous.get('sources',[]))
        if fact.event_id in seen:return
        illegal=fact.context.get('illegal',False)
        if illegal:seen.append(fact.event_id);del seen[:-8]
        status='ILLEGAL' if len(seen)>=3 else 'RESTRICTED' if illegal else previous.get('status','TOLERATED')
        unchanged=status==previous.get('status')
        f.local_status[t.id]={'status':status,'sources':seen,'updated_at':self.w.turn,'authority':p.id}
        if unchanged:return
        self.emit('FactionLocalStatusChanged',p,f.id,town_id=t.id,status=status,source_fact=fact.event_id,reason='known_illegal_action' if illegal else 'observed_legal_service')

    def refresh(self,p):
        if p.is_player:return
        for fid in p.organization_ids:
            f=self.w.factions.get(fid)
            point=self.w.points.get(p.position.map_id)
            if f and point and point.id==f.headquarters_id and point.claimant_id==f.id:
                f.norms['hq_report']={'food':self.e.items.count(point.id,'food'),'water':self.e.items.count(point.id,'water'),'observed_at':self.w.turn,'observer':p.id}
        self.public_proposals(p)
        for id in self.e.spatial.at(p.position):
            for gid in self.w.characters[id].group_ids:
                g=self.w.groups.get(gid)
                if g and g.status=='active':self.know_group(p,g,'member_encounter')
        # Pedidos adiados preservam a causa e retomam somente após a barreira diminuir.
        for fid in p.known_factions:
            f=self.w.factions.get(fid)
            if not f or f.status!='active':continue
            record=f.norms.get('invitations',{}).get(p.id)
            if not record or record.get('status') not in INVITATIONS or p.organization_ids:continue
            if record.get('status') in ('delayed','deferred') and (self.w.turn<record.get('reconsider_after',0) or p.fatigue>=85 or p.health<45):continue
            severity=max(p.thirst if record.get('terms',{}).get('benefits',{}).get('water') else 0,p.hunger if record.get('terms',{}).get('benefits',{}).get('food') else 0)
            n=self.e.needs.ensure(p,'affiliation',min(76,48+severity*.2),'continuing_invitation','Avaliar benefícios, custos e condição de ingresso',f.id)
            n.context['invitation']=True
            break
        for id in p.known_policies:
            policy=self.w.institutional_policies.get(id)
            if policy and policy.status in ('active','stalled') and (policy.jurisdiction==p.position.map_id or p.id in policy.effects.get('transport_jobs',{})) and self.worker_eligible(p,policy):
                n=self.e.needs.ensure(p,'institutional_work',min(75,48+(15 if p.money<15 else 0)),'known_policy','Cumprir trabalho financiado conhecido',id)
                break
        else:self.e.needs.satisfy(p,'institutional_work')
        for fid in p.organization_ids:
            f=self.w.factions.get(fid)
            if not f or f.status!='active':continue
            notice=p.social_state.get('known_faction_law',{}).get(fid)
            if notice and notice['status'] in ('RESTRICTED','ILLEGAL'):
                n=self.e.needs.ensure(p,'institutional_response',55,'known_local_restriction','Responder a restrição institucional conhecida',fid)
                n.context['notice']=notice

    def faction_candidates(self,p,n):
        f=self.w.factions.get(organization_id(n.context,'faction'))
        if not f or f.status!='active':return None
        caps=self.capabilities(f,p);t=self.w.towns.get(p.position.map_id)
        result=[]
        if t and p.id==f.leader_id:
            own=self.e.society.pressure(p)
            for id in p.known_proposals:
                prop=self.w.proposals.get(id)
                if (prop and prop.town_id==t.id and prop.status in ACTIVE_PROPOSALS and own
                    and prop.cause==own[0] and f.id not in prop.supporting_faction_ids):
                    result.append(('institutional_support',t.market,prop.id));break
        if caps['patrol'] and p.profession in ('guarda','soldado') and self.w.turn-p.social_state.get('last_faction_action',-1000)>=12:
            result.append(('institutional_patrol',t.market if t else p.position,f.id))
        if t and p.id==f.leader_id and f.money>=2 and self.w.turn-p.social_state.get('last_faction_purchase',-1000)>=12:
            result.append(('institutional_purchase',t.market,f.id))
        stocks=[k for k in ('food','water') if self.e.items.count(f.id,k)]
        if stocks:
            preferred='water' if p.thirst>=p.hunger else 'food'
            kind=preferred if preferred in stocks else stocks[0]
            result.append(MaterialCandidate('institutional_supply',None,f.id,kind))
        if f.norms.get('allow_theft') and p.id==f.leader_id and t and p.personality.honesty<35 and p.personality.greed>=60 and self.e.items.count(t.id,'food') and p.hunger>=45:
            result.append(('institutional_raid',t.market,f.id))
        return result or None

    def candidates(self,p,n):
        if n.kind=='institutional_work':
            policy=self.w.institutional_policies.get(n.target_id)
            if policy and policy.sector=='TRANSPORT':
                job=policy.effects.get('transport_jobs',{}).get(p.id)
                if job and p.position.map_id!=job['destination']:
                    return self.e.geography.candidates(p,job['destination'],'policy_transport',n)
                if job:return [('policy_work',self.w.towns[job['destination']].market,policy.id)]
            return [('policy_work',p.workplace if policy.sector=='RAW_MATERIAL' else self.w.towns[policy.jurisdiction].market,policy.id)] if policy else []
        if n.kind=='institutional_response':return [('institutional_response',None,n.target_id)]
        return []

    def execute(self,p,goal,n):
        if goal.action=='institutional_support':
            prop=self.w.proposals.get(goal.target_id);f=self.w.factions.get(organization_id(n.context,'faction')) if n else None
            return self.faction_support(p,f,prop) if prop and f else (False,'Apoio institucional desconhecido.')
        if goal.action=='support_proposal':
            prop=self.w.proposals.get(goal.target_id);g=self.w.groups.get(organization_id(n.context,'group')) if n else None
            return self.deliver_support(p,prop,g) if prop and g else (False,'Representação desconhecida.')
        if goal.action=='policy_work':
            policy=self.w.institutional_policies.get(goal.target_id)
            return self.policy_work(p,policy) if policy else (False,'Política inexistente.')
        f=self.w.factions.get(goal.target_id)
        if not f or p.id not in f.member_ids or f.status!='active':return False,'Sem vínculo institucional válido.'
        if n and n.kind=='organizational_survival' and n.context.get('organization_type'):
            if organization_id(n.context,'faction')!=f.id:return False,'Intenção pertence a outra organização.'
        t=self.w.towns.get(p.position.map_id);effect={};illegal=False
        if goal.action=='institutional_patrol':
            if not self.capabilities(f,p)['patrol'] or p.profession not in ('guarda','soldado'):return False,'Sem capacidade de patrulha.'
            self.e.conflicts.observe(p);self.w.metrics['PatrolPerformed']=self.w.metrics.get('PatrolPerformed',0)+1
            p.fatigue=min(100,p.fatigue+2);effect={'patrol':p.id}
        elif goal.action=='institutional_purchase':
            if not t or p.position!=t.market or p.id!=f.leader_id:return False,'Compra exige representante no mercado.'
            kind='water' if self.e.items.count(f.id,'water')<=self.e.items.count(f.id,'food') else 'food'
            price=self.e.economy.quote(t.id,kind,1)
            if f.money<price or not self.e.items.count(t.id,kind):return False,'Não há estoque ou orçamento para compra.'
            f.money-=price;t.money+=price;item=self.e.items.transfer(t.id,f.id,self.e.items.first(t.id,kind))
            p.social_state['last_faction_purchase']=self.w.turn;effect={'purchased':kind,'item_id':item.id,'paid':price}
        elif goal.action=='institutional_supply':
            # Um membro com estoque deve estar presente: o depósito não vira inventário remoto.
            leader=self.w.characters.get(f.leader_id)
            if p.position.map_id!=f.headquarters_id and (not leader or leader.position!=p.position):return False,'Depósito ou responsável não está presente.'
            kind=goal.resource_kind
            if kind not in ('food','water') or goal.amount!=1:return False,'Intenção material de abastecimento ausente ou inválida.'
            id=self.e.items.first(f.id,kind)
            if not id:return False,'A organização não possui este recurso.'
            item=self.e.items.transfer(f.id,p.id,id);effect={'supplied':kind,'recipient':p.id,'item_id':item.id}
        elif goal.action=='institutional_raid':
            if not t or p.position!=t.market or not f.norms.get('allow_theft') or not self.e.items.count(t.id,'food') or p.hunger<45:return False,'Sem necessidade, local ou meio para roubo.'
            item=self.e.items.transfer(t.id,f.id,self.e.items.first(t.id,'food'))
            crime=self.emit('ItemStolen',p,t.id,item_id=item.id,faction_id=f.id,lawful=False)
            effect={'stolen_item':item.id,'source_fact':crime.id};illegal=True
        elif goal.action=='institutional_response':
            notice=p.social_state.get('known_faction_law',{}).get(f.id)
            if not notice:return False,'Restrição desconhecida.'
            reaction='comply' if p.personality.honesty>=50 else 'reduce_activity' if p.personality.courage<60 else 'negotiate'
            f.plan['authority_response']={'reaction':reaction,'source_fact':notice['source_fact'],'at':self.w.turn}
            if reaction in ('comply','reduce_activity'):f.norms['allow_theft']=False
            self.e.needs.satisfy(p,'institutional_response')
            p.social_state['known_faction_law'].pop(f.id,None);effect={'authority_response':reaction}
        else:return False,'Ação institucional desconhecida.'
        p.social_state['last_faction_action']=self.w.turn
        self.emit('FactionAction',p,f.id,faction_id=f.id,action=goal.action,illegal=illegal,effect=effect,capacity=self.capabilities(f,p))
        return True,'Ação institucional executada com presença e capacidade próprias.'

    def tick(self):
        if self.w.turn%24:return
        for policy in self.w.institutional_policies.values():
            if policy.status not in ('active','stalled'):continue
            t=self.w.towns[policy.jurisdiction];mayor=self.w.characters.get(t.mayor_id)
            if mayor and self.w.turn-policy.last_work>=48 and self.w.turn-policy.start_time>=48:
                self.policy_barrier(mayor,policy,'no_effective_work' if not policy.barriers else policy.barriers['reason'])
        for f in self.w.factions.values():
            invitations=f.norms.get('invitations',{})
            terminal=[id for id,row in invitations.items() if row.get('status') in ('accepted','rejected','expired_for_reason')]
            for id in terminal[:-16]:invitations.pop(id)
            # Candidato morto não pode continuar decidindo; não é expiração por relógio.
            for id,row in invitations.items():
                q=self.w.characters.get(id)
                if q and not q.alive and row.get('status') in INVITATIONS:row.update(status='expired_for_reason',reason='candidate_dead')
