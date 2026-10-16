"""Organização local por encontros. Decisões continuam em Need/Solution/Goal."""
from dataclasses import asdict,replace
from .models import Group, Proposal, Faction, Commitment, Goal, Location, Fact
from .needs import FINISHED

SOCIAL_ACTIONS = {'share_problem','organize','join_group','meet_group','submit_proposal',
                  'review_proposal','read_response','serve_office','issue_local_order','protest','seek_royal_aid','recruit_member','report_to_faction',
                  'contribute','perform_assignment','seek_local_office','assume_local_office'}
RANKS = {'protection':['Recruta','Vigia','Veterano','Comandante'],
         'religious':['Iniciado','Devoto','Oficiante','Guardião do culto'],
         'professional':['Aprendiz','Associado','Mestre','Representante'],
         'justice':['Observador','Investigador','Árbitro','Representante'],
         'hunters':['Novato','Caçador','Veterano','Mestre'],
         'mercenaries':['Recruta','Combatente','Veterano','Comandante']}

class SocietySystem:
    def __init__(self,e):self.e,self.w=e,e.world
    def count(self,key,n=1):
        key='Society:'+key;self.w.metrics[key]=self.w.metrics.get(key,0)+n
    def emit(self,kind,p,target=None,**context):
        return self.e.recorder.emit(kind,f'{p.name}: {kind}.',p.id,target,p.position,
                                    historical=True,context=context)
    def remember(self,owner,fact):
        owner.knowledge[fact.event_id]=fact
        while len(owner.knowledge)>24:owner.knowledge.pop(next(iter(owner.knowledge)))
        if fact.event_id not in owner.memory:owner.memory.append(fact.event_id);del owner.memory[:-16]
    def living(self,ids):return [self.w.characters[i] for i in ids if i in self.w.characters and self.w.characters[i].alive]
    def local(self,t):return [p for p in self.living(t.resident_ids) if p.position.map_id==t.id and not p.is_player]
    def appoint(self,t,candidate,reason,source=None):
        old=t.mayor_id;records=t.office;t.mayor_id=candidate.id
        pending=[i for i in records.get('known_proposals',[]) if i in self.w.proposals
                 and self.w.proposals[i].status in ('submitted','deferred')][-24:]
        for i in pending:self.w.proposals[i].target_id=candidate.id
        t.office={'started_at':self.w.turn,'origin':reason,'source_fact':source,'previous':old,
                  'support':{},'decisions':records.get('decisions',[])[-12:],'known_proposals':pending,
                  'public_responses':records.get('public_responses',[])[-12:]}
        candidate.known_places['administration']=t.market
        ruler=self.w.kingdoms[t.kingdom_id].ruler_id if t.kingdom_id else None
        if ruler:self.e.graph.set(candidate.id,ruler,'representa_cidade',60)
        self.emit('MayorAppointed',candidate,t.id,previous=old,reason=reason,source_fact=source)
        self.count('mayor_appointed')
    def hierarchy(self,t):
        # A patrulha fora da cidade não remove patente nem cria outra chefia.
        members=[p for p in self.living(t.resident_ids) if not p.is_player and p.profession in ('guarda','soldado')]
        t.military_ranks={i:r for i,r in t.military_ranks.items() if any(p.id==i for p in members)}
        if not members:t.general_id=None;return
        if t.general_id not in t.military_ranks:
            g=max(members,key=lambda p:(p.personality.diligence+p.personality.courage+
                  sum(self.e.graph.value(q.id,p.id,'confiança',10) for q in members)/len(members),-p.id))
            t.general_id=g.id;t.military_ranks[g.id]='General'
            self.emit('MilitaryAppointed',g,t.id,rank='General');self.count('military_replacement')
        other=[p for p in members if p.id!=t.general_id]
        for index,p in enumerate(other):
            if p.id not in t.military_ranks:
                t.military_ranks[p.id]=('Captain','Lieutenant','Sergeant','Soldier')[min(3,index)]
        mayor=self.w.characters.get(t.mayor_id)
        if mayor:self.e.graph.set(mayor.id,t.general_id,'autoridade_local',50)
    def bootstrap(self):
        if self.w.social_initialized:return
        self.w.social_initialized=True
        for t in self.w.towns.values():
            if t.kind!='cidade' or t.kingdom_id is None:continue
            common=[p for p in self.local(t) if p.category=='comum' and p.profession not in ('guarda','soldado')]
            if common:
                # Nomeação local simplificada, pessoa já residente; não cria população.
                chosen=max(common,key=lambda p:(p.personality.diligence*.4+p.personality.honesty*.3+
                       p.personality.ambition*.2+sum(self.e.graph.value(q.id,p.id,'amizade') for q in common)/max(1,len(common)),-p.id))
                self.appoint(t,chosen,'delegação inicial da família real')
            self.hierarchy(t)
        for f in self.w.factions.values():
            f.purpose='hunters' if f.kind=='caçadores' else 'mercenaries'
            f.ranks=list(RANKS[f.purpose]);f.member_ids=[f.leader_id]
            f.assignments[f.leader_id]={'rank':f.ranks[-1],'deeds':0,'joined_at':self.w.turn}
            p=self.w.characters[f.leader_id];p.organization_ids.append(f.id)
            p.known_towns[p.town_id]={'position':vars(self.w.towns[p.town_id].position),
                'confidence':100,'learned_at':self.w.turn,'source':'known_birthplace_route','source_fact':None}
            f.norms={'dues':1,'risk':p.personality.courage/100,'religion':p.religion,'origin':'initial_foundation'}
            f.norms.update(allow_theft=f.purpose=='mercenaries' and p.personality.honesty<35 and p.personality.greed>=70,
                           harm_civilians=False)
        self.e.collective.bootstrap_routes()
    def pressure(self,p):
        # Conhecimento próprio e sinais locais; não varre necessidades alheias.
        if p.social_state.get('fear_of_killer',0)>=35 and self.w.turn-p.social_state.get('fear_of_killer_updated',-1000)<=168:
            return 'security',None,70
        if p.financial_since is not None and self.w.turn-p.financial_since>=48:
            return 'resource_pressure',None,min(85,35+p.financial_setbacks*2+(self.w.turn-p.financial_since)/24)
        if p.combat.opponents or any(n.kind in ('revenge','protection','pursuit') and n.status not in FINISHED for n in p.needs.values()):
            return 'security',None,55
        n=next((n for n in p.needs.values() if n.kind=='religious_interest' and n.status not in FINISHED),None)
        if n and p.devotion>=60 and p.beliefs.get(n.target_id,{}).get('source_fact') is not None:return 'religious_interest',n.target_id,min(75,20+p.devotion*.4)
        if p.mythic_trait=='Justice' and p.grievances:return 'security',None,60
        return None
    def compatible(self,p,cause,subject):
        own=self.pressure(p)
        if own and own[:2]==(cause,subject):return True
        if cause=='religious_interest':return p.devotion>=60 and subject in p.beliefs
        return False
    def affinity(self,p,q,cause):
        trust=self.e.graph.value(p.id,q.id,'confiança',10)
        bond=self.e.graph.value(p.id,q.id,'amizade')
        return trust*.5+bond*.2+p.personality.compassion*.2+p.personality.ambition*.15+(8 if p.profession==q.profession else 0)
    def groups_here(self,p):
        return [g for g in self.w.groups.values() if g.status=='active' and g.town_id==p.town_id]
    def shared_facts(self,p,cause,subject):
        return [f for f in p.knowledge.values() if f.kind=='ProblemShared' and f.actor_id!=p.id
                and f.context.get('cause')==cause and f.context.get('subject')==subject
                and f.confidence>=60 and self.w.turn-f.turn<=72 and f.actor_id in self.e.spatial.at(p.position)]
    def form(self,p,cause,subject,source):
        t=self.w.towns[p.town_id]
        if len(self.groups_here(p))>=6 or len(p.group_ids)>=3 or any(g.cause==cause and g.subject_id==subject and p.id in g.member_ids for g in self.groups_here(p)):return None
        peers=[self.w.characters[f.actor_id] for f in self.shared_facts(p,cause,subject)
               if self.compatible(self.w.characters[f.actor_id],cause,subject) and self.affinity(p,self.w.characters[f.actor_id],cause)>=35 and len(self.w.characters[f.actor_id].group_ids)<3]
        peers=list({q.id:q for q in peers}.values())[:7]
        if not peers:return None
        members=[p]+peers
        # Autor da iniciativa participa; escolha inclui confiança e conexão, não só um traço.
        leader=max(members,key=lambda q:(q.personality.ambition*.2+q.personality.persistence*.15+
                  sum(self.affinity(v,q,cause) for v in members if v!=q)/len(members)+10*(q.id==p.id),-q.id))
        id=self.w.allocate_id();g=Group(id,f'Círculo de {t.name} — '+{'resource_pressure':'Sustento',
            'security':'Proteção','religious_interest':'Fé'}.get(cause,cause),t.id,cause,subject,leader.id,
            [q.id for q in members],self.w.turn,source.id,self.shared_facts(p,cause,subject)[0].event_id,last_relevant=self.w.turn)
        g.pressure=source.priority;self.w.groups[id]=g
        g.plan={'meeting_place':vars(t.market),'meeting_period':24}
        self.remember(g,p.knowledge[g.originating_fact])
        n=self.e.needs.ensure(g,cause,g.pressure,'individual_pressure',source.reason,subject)
        g.commitment=Commitment(self.w.allocate_id(),g.id,n.id,g.originating_fact,subject,cause,g.pressure,self.w.turn,self.w.turn)
        for q in members:
            if len(q.group_ids)<3:q.group_ids.append(id)
            g.support[q.id]=self.affinity(q,leader,cause)
        event=self.emit('GroupFormed',leader,g.id,cause=cause,members=g.member_ids,originating_need=source.id,
                        source_fact=g.originating_fact,town_id=t.id)
        g.memory.append(event.id);self.count('group_formed');return g
    def refresh(self,p):
        if not self.w.social_initialized:return
        own=self.pressure(p);t=self.w.towns.get(p.town_id)
        if own and t and p.position.map_id==t.id:
            cause,subject,pressure=own
            n=self.e.needs.ensure(p,'political_pressure',min(80,pressure+p.personality.ambition*.15),
                'own_shared_problem','Buscar representação para problema pessoal',subject)
            n.context.update(cause=cause,subject=subject)
        else:self.e.needs.satisfy(p,'political_pressure')
        mine=[self.w.groups[i] for i in p.group_ids if i in self.w.groups and self.w.groups[i].status=='active' and self.w.groups[i].cause!='expedition']
        if mine:
            g=mine[0];n=self.e.needs.ensure(p,'organizational_survival',min(75,25+g.pressure*.4),
                 'group:'+str(g.id),'Participar da organização conhecida',g.leader_id);n.context['group_id']=g.id
        elif p.organization_ids:
            f=next((self.w.factions.get(i) for i in p.organization_ids if self.w.factions.get(i) and self.w.factions[i].status=='active'),None)
            if f:
                n=self.e.needs.ensure(p,'organizational_survival',45,'faction:'+str(f.id),'Atender função organizacional',f.leader_id)
                n.context={'faction_id':f.id}
                if p.id==f.leader_id and p.position.map_id!=p.town_id:
                    n.context['known_location']=vars(self.w.towns[p.town_id].market)
            else:self.e.needs.satisfy(p,'organizational_survival')
        else:self.e.needs.satisfy(p,'organizational_survival')
        if t and t.mayor_id==p.id:
            pending=[i for i in t.office.get('known_proposals',[]) if i in self.w.proposals and
                     (self.w.proposals[i].status=='submitted' or self.w.proposals[i].status=='deferred' and
                      self.w.turn-self.w.proposals[i].decided_at>=24)]
            if pending:
                n=self.e.needs.ensure(p,'governance',min(90,40+max(self.w.proposals[i].urgency for i in pending)*.4),
                    'received_proposals','Responder a proposta formal recebida',p.id)
                n.context['proposal_id']=pending[0]
                n.context['mode']='received_proposal'
            elif p.health>=80 and max(p.hunger,p.thirst)<70 and (self.w.turn-p.social_state.get('last_office',-1000)>=48 or p.social_state.get('office_until',-1)>self.w.turn):
                n=self.e.needs.ensure(p,'governance',60,'own_office_duty','Atender moradores na administração local',p.id)
                n.context={'mode':'office_hours'}
            else:self.e.needs.satisfy(p,'governance')
        if t and t.military_ranks.get(p.id) in ('General','Captain','Lieutenant','Sergeant'):
            cases=[f for f in p.knowledge.values() if f.kind=='WantedIssued' and self.w.turn-f.turn<72]
            if cases and self.w.turn-p.social_state.get('last_command',-1000)>=24:
                n=self.e.needs.ensure(p,'military_service',55,'known_local_case','Orientar segurança local por caso recebido',cases[-1].target_id)
                n.context['source_event']=cases[-1].event_id
            else:self.e.needs.satisfy(p,'military_service')
        if p.mythic_trait or p.personality.ambition>=85:
            if t and t.mayor_id!=p.id and t.kind=='cidade' and p.money>=10 and p.health>=80:
                n=self.e.needs.ensure(p,'recognition',22+p.personality.ambition*.2,'political_aspiration','Buscar apoio para representação local',t.id)
                n.expires_at=self.w.turn+240
        self.e.collective.refresh(p)
    def _outreach_candidates(self,p,n):
        temporary=replace(n,kind='family',context={'known_location':vars(self.w.towns[p.town_id].market)})
        return self.e.agency.travel_candidates(p,temporary)
    def candidates(self,p,n):
        collective=self.e.collective.candidates(p,n)
        if collective is not None:return collective
        if n.kind=='political_pressure':
            cause=n.context['cause'];subject=n.context.get('subject');here=self.e.spatial.at(p.position)
            choices=[]
            if self.w.turn-p.social_state.get('last_share',-1000)>=24:
                choices.append(('share_problem',None,None))
            if len(p.group_ids)<3 and not any(g.cause==cause and g.subject_id==subject and p.id in g.member_ids for g in self.groups_here(p)) and self.shared_facts(p,cause,subject):choices.append(('organize',None,None))
            for g in self.groups_here(p):
                if len(p.group_ids)<3 and g.cause==cause and g.subject_id==subject and p.id not in g.member_ids and g.leader_id in here:
                    choices.append(('join_group',None,g.id))
            return choices
        if n.kind=='military_service':return [('issue_local_order',self.w.towns[p.town_id].market,n.target_id)]
        if n.kind=='governance':
            if n.context.get('mode')=='office_hours':return [('serve_office',self.w.towns[p.town_id].market,p.id)]
            choices=[('review_proposal',self.w.towns[p.town_id].market,n.context['proposal_id'])]
            t=self.w.towns[p.town_id];king=self.w.kingdoms.get(t.kingdom_id)
            if king and king.ruler_id in self.e.spatial.at(p.position) and t.money<30:
                choices.append(('seek_royal_aid',None,king.ruler_id))
            return choices
        if n.kind=='recognition':return [('seek_local_office',self.w.towns[p.town_id].market,n.target_id)]
        if n.kind!='organizational_survival':return []
        gid=n.context.get('group_id');g=self.w.groups.get(gid)
        if g:
            pending=[self.w.proposals[i] for i in g.proposal_ids if i in self.w.proposals and g.proposal_knowledge.get(i,{}).get('status') in ('draft','submitted','deferred')]
            if p.id==g.leader_id and pending and g.proposal_knowledge[pending[0].id]['status']=='draft':
                observed=p.observations.get(pending[0].target_id)
                dest=observed.position if observed and self.w.turn-observed.turn<=24 and observed.position.map_id==g.town_id else self.w.towns[g.town_id].market
                return [('submit_proposal',dest,pending[0].id)]
            choices=[]
            if p.id==g.leader_id and pending and self.w.turn-p.social_state.get('last_policy_read',-1000)>=24:
                choices.append(('read_response',self.w.towns[g.town_id].market,g.id))
            if p.id==g.leader_id and self.w.turn-g.last_meeting>=24:choices.append(('meet_group',self.w.towns[g.town_id].market,g.id))
            if g.failures and self.w.turn-p.social_state.get('last_protest',-1000)>=48:choices.append(('protest',self.w.towns[g.town_id].market,g.id))
            if g.responsibility_id and g.pressure>=85 and g.failures>=3 and p.id==g.leader_id:
                choices.append(('assume_local_office',self.w.towns[g.town_id].market,g.id))
            return choices
        f=self.w.factions.get(n.context.get('faction_id'))
        if not f:return []
        if p.id==f.leader_id and p.position.map_id!=p.town_id:
            # Preparação e percurso existentes, sem teleporte ou mudança de residência.
            temporary=replace(n,kind='family',context={'known_location':vars(self.w.towns[p.town_id].market)})
            return self.e.agency.travel_candidates(p,temporary)
        choices=[]
        if self.w.turn-p.social_state.get('last_report',-1000)>=24:choices.append(('report_to_faction',None,f.id))
        if self.w.turn-p.social_state.get('last_contribution',-1000)>=72 and p.money>15:choices.append(('contribute',None,f.id))
        if p.id==f.leader_id and len(f.member_ids)<24:
            for i in self.e.spatial.at(p.position):
                q=self.w.characters[i]
                if q.id!=p.id and q.id not in f.member_ids and self.affinity(q,p,f.purpose)>=35:choices.append(('recruit_member',None,q.id))
        assignment=f.assignments.get(p.id,{}).get('order')
        if assignment:choices.append(('perform_assignment',Location(**assignment['location']),f.id))
        if p.id==f.leader_id and not choices and p.position.map_id!=p.town_id:
            choices.append(('report_to_faction',None,f.id))
        return choices
    def meeting(self,p,g):
        present=[q for q in self.living(g.member_ids) if q.position==p.position]
        if p.id!=g.leader_id or len(present)<2:return False,'A reunião exige liderança e pelo menos dois membros presentes.'
        g.last_meeting=self.w.turn;g.investment+=1
        for q in present:
            for fact in q.knowledge.values():
                if fact.kind in ('ProblemShared','PolicyDecided','DivineIntervention','SpiritualReport','WantedIssued'):
                    self.remember(g,self.e.knowledge.transmitted(fact,q,p))
        own=[self.pressure(q) for q in present];relevant=[x for x in own if x and x[:2]==(g.cause,g.subject_id)]
        if not relevant:self.dissolve(g,'problem_no_longer_shared');return True,'Problema deixou de ser compartilhado.'
        g.last_relevant=self.w.turn;g.pressure=min(100,sum(x[2] for x in relevant)/len(relevant)+g.failures*5)
        if not any(g.proposal_knowledge.get(i,{}).get('status') in ('draft','submitted','deferred') for i in g.proposal_ids):
            if self.propose(p,g):p.social_state['meaningful_social_actions']=p.social_state.get('meaningful_social_actions',0)+1
        self.emit('GroupMeeting',p,g.id,members=[q.id for q in present],pressure=g.pressure,known_facts=list(g.knowledge)[-3:])
        if g.investment>=4 and self.w.turn-g.created_at>=168 and len(g.member_ids)>=3 and sum(q.money>15 for q in present)>=2:
            self.found_faction(p,g,present)
        return True,'Reunião e avaliação coletiva realizadas.'
    def propose(self,p,g):
        t=self.e.collective.authority(g)
        if not t or t.mayor_id is None or len(t.proposal_ids)>=24:return None
        from .goals import Solution
        from .utility import evaluate
        options={'resource_pressure':['food_distribution','temporary_work'],'security':['security_funding','arms_funding'],
                 'religious_interest':['recognize_cult','restrict_cult']}[g.cause]
        if g.cause=='religious_interest' and not g.grievances:options=['recognize_cult']
        choices=[]
        for action in options:
            score,terms=evaluate('submit_proposal',p)
            if action=='food_distribution':score+=p.personality.compassion*.2+g.pressure*.2
            if action=='temporary_work':score+=p.personality.diligence*.25
            if action=='security_funding':score+=p.personality.honesty*.2
            if action=='arms_funding':score+=p.personality.courage*.25
            if action=='restrict_cult':score+=p.personality.vengefulness*.25-p.personality.compassion*.3
            choices.append(Solution(action,score,considerations=terms))
        solution=self.e.goals.choose(sorted(choices,key=lambda x:-x.score)).action
        prop=Proposal(self.w.allocate_id(),g.id,t.id,t.mayor_id,g.cause,g.cause,solution,g.pressure,
                      len(g.member_ids),self.w.turn,g.originating_fact)
        prop.subject_id=g.subject_id if solution!='restrict_cult' else next((v.get('subject_id') for v in g.grievances.values() if v.get('subject_id') is not None),g.subject_id)
        self.w.proposals[prop.id]=prop;g.proposal_ids.append(prop.id);del g.proposal_ids[:-6]
        g.proposal_knowledge[prop.id]={'status':'draft','confidence':100,'source_fact':g.originating_fact}
        g.proposal_knowledge={i:r for i,r in g.proposal_knowledge.items() if i in g.proposal_ids}
        t.proposal_ids.append(prop.id)
        n=self.e.needs.ensure(g,g.cause,g.pressure,'group_meeting',g.name,g.subject_id)
        g.goal=Goal(self.w.allocate_id(),n.id,'submit_proposal',g.pressure,self.w.turn,prop.id,t.market)
        self.emit('ProposalCreated',p,prop.id,group_id=g.id,solution=solution,source_fact=g.originating_fact);self.count('proposal_created')
        return prop
    def decision_scores(self,p,prop):
        t=self.w.towns[prop.town_id];g=self.w.groups.get(prop.group_id)
        available=(self.e.items.count(t.id,'food') if prop.solution=='food_distribution' else t.money)
        support=min(30,prop.support*4);opposition=min(30,prop.opposition*4)
        urgency=prop.urgency*.4;belief=15 if prop.solution=='recognize_cult' and g and g.subject_id in p.beliefs else -5
        cost=30 if available<max(2,prop.support) else 5
        relations=self.e.graph.value(p.id,g.leader_id,'confiança',10)*.2 if g else 0
        kingdom=self.w.kingdoms.get(t.kingdom_id);royal=self.e.graph.value(p.id,kingdom.ruler_id,'lealdade',0) if kingdom and kingdom.ruler_id else 0
        return {'approve':urgency+support+p.personality.compassion*.4+relations+belief-cost-opposition,
                'partial':25+urgency*.7+p.personality.diligence*.3-cost*.3,
                'reject':20+p.personality.greed*.35+opposition+cost-p.personality.compassion*.15,
                'defer':20+p.personality.persistence*.25+cost*.5+royal*.05-support*.3}
    def material(self,p,prop,partial=False):
        t=self.w.towns[prop.town_id];g=self.w.groups[prop.group_id];result={'food':0,'money':0,'recipients':[]}
        limit=max(1,prop.support//2) if partial else prop.support
        if prop.solution=='food_distribution':
            for q in self.living(g.member_ids):
                if limit<=0 or not self.e.items.count(t.id,'food'):break
                if q.position!=t.market or q.hunger<35:continue
                self.e.items.transfer(t.id,q.id,self.e.items.first(t.id,'food'));result['food']+=1;result['recipients'].append(q.id);limit-=1
        elif prop.solution=='temporary_work':
            # Contrata trabalho existente; o pagamento físico requer estoque e demanda.
            for q in self.living(g.member_ids):
                if limit<=0:break
                if q.position==t.market and self.e.professions.temporary_eligible(q):
                    before=self.e.items.count(q.id,'food');ok,_=self.e.professions.temporary_service(q,1)
                    if ok:result['food']+=self.e.items.count(q.id,'food')-before;result['recipients'].append(q.id);limit-=1
        elif prop.solution=='arms_funding':
            smith=next((q for q in self.local(t) if q.profession=='ferreiro' and q.position==t.market),None)
            guards=[q for q in self.local(t) if q.profession=='guarda' and q.position==t.market]
            if smith and guards and t.money>=2 and self.e.items.count(t.id,'iron')>=2 and self.e.items.count(t.id,'wood')>=1:
                self.e.items.consume(t.id,'iron',2);self.e.items.consume(t.id,'wood');t.money-=2;smith.money+=2
                weapon=self.e.items.create(guards[0].id,'weapon',creator_id=smith.id,origin='Encomenda política custeada')
                result.update(money=2,weapon_id=weapon.id,recipients=[guards[0].id]);t.demand['iron']=min(40,t.demand.get('iron',0)+2)
        elif prop.solution=='security_funding':
            guards=[q for q in self.local(t) if q.profession=='guarda' and q.position==t.market]
            for q in guards[:limit]:
                amount=min(3,t.money);t.money-=amount;q.money+=amount;result['money']+=amount;result['recipients'].append(q.id)
                if amount:t.policies['security_until']=self.w.turn+72
                fact=next((f for f in g.knowledge.values() if f.kind=='WantedIssued'),None)
                if fact and amount:self.e.knowledge.learn(q,self.e.knowledge.transmitted(fact,p,q),False)
        elif prop.solution in ('recognize_cult','restrict_cult'):
            cost=min(2,t.money)
            if cost<2:return result
            t.money-=cost;p.money+=cost;result['money']=cost
            key=str(prop.subject_id);t.policies.setdefault('cults',{})[key]='restricted' if prop.solution=='restrict_cult' else 'recognized'
            while len(t.policies['cults'])>8:t.policies['cults'].pop(next(iter(t.policies['cults'])))
            result['cult']=prop.subject_id;result['policy']=t.policies['cults'][key]
        return result
    def resolve(self,p,prop):
        t=self.w.towns[prop.town_id]
        if t.mayor_id!=p.id or p.position!=t.market or prop.id not in t.office.get('known_proposals',[]):return False,'Proposta não foi recebida pela autoridade presente.'
        if prop.status not in ('submitted','deferred'):return False,'Proposta já encerrada.'
        scores=self.decision_scores(p,prop);decision=max(scores,key=lambda k:(scores[k],k))
        result=self.material(p,prop,decision=='partial') if decision in ('approve','partial') else {}
        if decision in ('approve','partial') and not any(result.get(k) for k in ('food','money','policy')):decision='defer'
        if decision=='defer' and self.w.turn-prop.created_at>96:decision='reject'
        prop.status={'approve':'accepted','partial':'partial','reject':'rejected','defer':'deferred'}[decision]
        prop.decided_at=self.w.turn;prop.result={'decision':decision,'scores':scores,'material':result}
        t.office['decisions'].append(prop.id);del t.office['decisions'][:-12]
        event=self.emit('PolicyDecided',p,prop.id,group_id=prop.group_id,solution=prop.solution,result=prop.result,town_id=t.id,group_subject=self.w.groups[prop.group_id].subject_id)
        t.office.setdefault('public_responses',[]).append(Fact(event.id,event.kind,event.actor_id,event.target_id,
            event.location,event.turn,event.description,confidence=80,source_id=p.id,source_kind='known',context=event.context))
        del t.office['public_responses'][:-12]
        self.count('proposal_'+prop.status);self.count('material_food',result.get('food',0));self.count('material_money',result.get('money',0))
        return True,'Decisão contextual com resultado material registrada.'
    def react(self,p,f):
        g=self.w.groups.get(f.context.get('group_id'))
        if not g or g.status!='active' or p.id not in g.member_ids:return
        if f.kind=='PolicyDecided' and p.id==g.leader_id:
            if p.position.map_id!=g.town_id:return
            if f.target_id not in g.proposal_ids:return
            # Reação só ocorre quando liderança aprende resposta, não lendo status remoto.
            known=g.proposal_knowledge.get(f.target_id,{})
            if f.event_id==known.get('response_fact'):
                known['confidence']=max(known.get('confidence',0),f.confidence);return
            if f.event_id<known.get('response_fact',-1):return
            self.remember(g,f);decision=f.context['result']['decision']
            p.social_state['meaningful_social_actions']=p.social_state.get('meaningful_social_actions',0)+1
            g.proposal_knowledge[f.target_id]={'status':{'approve':'accepted','partial':'partial','reject':'rejected','defer':'deferred'}[decision],
                'confidence':f.confidence,'source_fact':f.event_id,'response_fact':f.event_id}
            while len(g.proposal_knowledge)>6:g.proposal_knowledge.pop(next(iter(g.proposal_knowledge)))
            if decision=='approve':self.dissolve(g,'proposal_accepted')
            elif decision=='partial':
                material=f.context['result'].get('material',{})
                if any(material.get(k) for k in ('food','money','policy')):
                    g.pressure*=.6;g.plan['relief_until']=self.w.turn+48
                    g.action_pressure.value*=.6;g.action_pressure.failures=max(0,g.action_pressure.failures-1)
            elif decision in ('reject','defer'):
                g.failures+=1;g.pressure=min(100,g.pressure+5)
                g.action_pressure.failures=min(6,g.failures);g.action_pressure.updated_at=-1
                if f.confidence>=60 and decision=='reject':g.responsibility_id=f.actor_id
                self.count('pressure_increased')
    def on_fact(self,p,f):
        self.react(p,f)
        if f.kind=='PolicyDecided':
            p.social_state['institutional_opinion']=max(-100,min(100,p.social_state.get('institutional_opinion',0)+(5 if f.context['result']['decision']=='approve' else -3)))
        for gid in p.group_ids:
            g=self.w.groups.get(gid)
            if g and g.status=='active' and f.kind=='PolicyDecided' and f.confidence>=30:
                material=f.context.get('result',{}).get('material',{})
                other=f.context.get('group_id')
                if other!=g.id and material.get('policy')=='restricted' and material.get('cult')==g.subject_id:
                    g.grievances[other]={'source_fact':f.event_id,'severity':f.confidence*.5,'since':f.turn,
                        'status':'active','subject_id':f.context.get('group_subject')}
                    while len(g.grievances)>4:g.grievances.pop(next(iter(g.grievances)))
                    self.count('group_antagonism')

            if g and g.status=='active' and f.kind in ('CharacterAttacked','CharacterKilled') and f.target_id in g.member_ids and f.actor_id!=p.id:
                actor_groups=[i for i in f.context.get('actor_groups',[]) if i!=g.id]
                for other in actor_groups[:2]:
                    g.grievances[other]={'source_fact':f.event_id,'severity':f.confidence*.5,'since':f.turn,'status':'active'}
                while len(g.grievances)>4:g.grievances.pop(next(iter(g.grievances)))
    def dissolve(self,g,reason):
        if g.status!='active':return
        g.status='dissolved';g.last_relevant=self.w.turn
        if g.commitment:g.commitment.status='satisfied' if reason=='proposal_accepted' else 'abandoned'
        for p in self.living(g.member_ids):
            if g.id in p.group_ids:p.group_ids.remove(g.id)
        leader=self.w.characters[g.leader_id];self.emit('GroupDissolved',leader,g.id,reason=reason);self.count('group_dissolved')
    def found_faction(self,p,g,present):
        present=[q for q in present if q.alive and q.id in g.member_ids and q.position==p.position]
        if (len(self.w.factions)>=24 or g.status!='active' or p.id!=g.leader_id or
            g.investment<4 or self.w.turn-g.created_at<168 or len(g.member_ids)<3 or
            any(len(self.w.characters[i].organization_ids)>=3 for i in g.member_ids)):return None
        purpose={'security':'justice','religious_interest':'religious','resource_pressure':'professional','expedition':'professional'}[g.cause]
        total=sum(min(2,max(0,q.money-15)) for q in present)
        if total<4:return None
        f=Faction(self.w.allocate_id(),'Associação '+g.name,p.id,self.w.towns[g.town_id].id,purpose,
                  member_ids=list(g.member_ids),purpose=purpose,ranks=list(RANKS[purpose]),created_at=self.w.turn,
                  norms={'dues':1,'belief':g.subject_id,'origin_group':g.id})
        for q in present:
            amount=min(2,max(0,q.money-15));q.money-=amount;f.money+=amount
        for id in f.member_ids:
            q=self.w.characters[id];q.organization_ids.append(f.id)
            f.assignments[id]={'rank':f.ranks[-1] if id==p.id else f.ranks[0],'deeds':0,'joined_at':self.w.turn}
        f.knowledge=dict(g.knowledge);f.memory=list(g.memory)
        self.w.factions[f.id]=f;g.status='faction'
        for q in self.living(g.member_ids):
            if g.id in q.group_ids:q.group_ids.remove(g.id)
        self.emit('FactionFounded',p,f.id,group_id=g.id,purpose=purpose,members=f.member_ids,cost=total);self.count('faction_founded')
        return f
    def execute(self,p,goal,n):
        from .collective_action import ACTIONS
        if goal.action in ACTIONS:return self.e.collective.execute(p,goal,n)
        a=goal.action;t=self.w.towns.get(p.town_id);here=self.e.spatial.at(p.position)
        if a=='share_problem':
            own=self.pressure(p)
            if not own or not any(i!=p.id for i in here):return False,'Não há problema atual ou interlocutor.'
            p.social_state['last_share']=self.w.turn
            self.emit('ProblemShared',p,cause=own[0],subject=own[1],severity=own[2],source_fact=n.context.get('source_event') if n else None)
            self.count('problem_shared');return True,'Problema próprio comunicado presencialmente.'
        if a=='organize':
            if not n:return False,'Não há necessidade própria de organização.'
            g=self.form(p,n.context['cause'],n.context.get('subject'),n)
            return bool(g),'Grupo formado por afinidade conhecida.' if g else 'Afinidade conhecida insuficiente.'
        if a=='join_group':
            g=self.w.groups.get(goal.target_id)
            if not g or g.status!='active' or p.id in g.member_ids or g.leader_id not in here or len(p.group_ids)>=3 or len(g.member_ids)>=16 or not self.compatible(p,g.cause,g.subject_id):return False,'Grupo não é acessível ou compatível.'
            if self.affinity(p,self.w.characters[g.leader_id],g.cause)<35:return False,'Afinidade insuficiente.'
            g.member_ids.append(p.id);p.group_ids.append(g.id);g.support[p.id]=self.affinity(p,self.w.characters[g.leader_id],g.cause)
            self.emit('GroupJoined',p,g.id);self.count('group_joined');return True,'Adesão voluntária registrada.'
        if a=='meet_group':
            g=self.w.groups.get(goal.target_id)
            return self.meeting(p,g) if g and g.status=='active' else (False,'Grupo ativo inexistente.')
        if a=='submit_proposal':
            prop=self.w.proposals.get(goal.target_id);g=self.w.groups.get(prop.group_id) if prop else None
            t=self.w.towns.get(prop.town_id) if prop else None
            mayor=self.w.characters.get(t.mayor_id) if t else None
            if not prop or not g or p.id!=g.leader_id or not mayor or mayor.id not in here or prop.status!='draft':return False,'Autoridade ou representação não está presente.'
            prop.target_id=mayor.id;prop.status='submitted';t.office.setdefault('known_proposals',[]).append(prop.id)
            g.proposal_knowledge[prop.id]={'status':'submitted','confidence':100,'source_fact':prop.source_fact}
            del t.office['known_proposals'][:-24]
            self.emit('ProposalSubmitted',p,mayor.id,proposal_id=prop.id,group_id=g.id,source_fact=prop.source_fact);self.count('proposal_submitted')
            p.social_state['meaningful_social_actions']=p.social_state.get('meaningful_social_actions',0)+1
            return True,'Proposta formal transmitida em encontro.'
        if a=='read_response':
            g=self.w.groups.get(goal.target_id)
            authority=self.e.collective.authority(g) if g else None
            if not g or p.id not in g.member_ids or not authority or p.position!=authority.market:return False,'Consulta exige membro na administração conhecida.'
            p.social_state['last_policy_read']=self.w.turn
            replies=[f for f in authority.office.get('public_responses',[]) if f.target_id in g.proposal_ids]
            learned=[f.event_id for f in replies if self.e.knowledge.learn(p,f,False)]
            if learned:p.social_state['meaningful_social_actions']=p.social_state.get('meaningful_social_actions',0)+1
            self.emit('PolicyRead',p,g.id,source_facts=[f.event_id for f in replies],new_source_facts=learned);self.count('response_read')
            return True,'Respostas públicas consultadas presencialmente.' if replies else 'Consulta local não encontrou resposta publicada.'
        if a=='issue_local_order':
            chain=['General','Captain','Lieutenant','Sergeant','Soldier'];rank=t.military_ranks.get(p.id) if t else None
            if rank not in chain[:-1]:return False,'Não possui comando militar local.'
            fact=p.knowledge.get(n.context.get('source_event'))
            if not fact:return False,'Comando sem conhecimento do caso.'
            transmitted=[]
            for q in self.local(t):
                if q.id!=p.id and q.position==p.position and q.id in t.military_ranks and chain.index(t.military_ranks[q.id])>chain.index(rank):
                    self.e.knowledge.learn(q,self.e.knowledge.transmitted(fact,p,q),False);transmitted.append(q.id)
            p.social_state['last_command']=self.w.turn
            self.emit('MilitaryOrder',p,t.id,rank=rank,recipients=transmitted,source_fact=fact.event_id);self.count('military_order')
            return True,'Ordem local transmitida a militares presentes.'
        if a=='serve_office':
            if not t or t.mayor_id!=p.id or p.position!=t.market:return False,'Atendimento exige prefeito na administração.'
            if p.social_state.get('office_until',-1)<=self.w.turn:
                p.social_state.update(last_office=self.w.turn,office_until=self.w.turn+4)
                self.emit('OfficeAttended',p,t.id);self.count('office_attended')
            return True,'Prefeito disponível para receber moradores; propostas continuam exigindo encontro.'
        if a=='review_proposal':
            result=self.resolve(p,self.w.proposals[goal.target_id])
            if result[0]:p.social_state['meaningful_social_actions']=p.social_state.get('meaningful_social_actions',0)+1
            return result
        if a=='protest':
            g=self.w.groups[goal.target_id];p.social_state['last_protest']=self.w.turn
            self.emit('GroupProtested',p,t.mayor_id,group_id=g.id,failures=g.failures,source_fact=g.memory[-1] if g.memory else None)
            self.count('protest');return True,'Pressão pública, sem violência automática.'
        if a in ('seek_local_office','assume_local_office'):
            if not t or t.kind!='cidade' or p.position!=t.market:return False,'Função política exige presença local.'
            support=sum(self.e.graph.value(q.id,p.id,'confiança',10)>=60 for q in self.local(t))
            g=self.w.groups.get(goal.target_id) if a=='assume_local_office' else None
            if g and (g.leader_id!=p.id or g.failures<3 or g.pressure<85 or not g.responsibility_id):return False,'Não há causa atribuída para controle local.'
            if support<3 or p.personality.ambition<65:return False,'Apoio e iniciativa política insuficientes.'
            if t.mayor_id and not g:return False,'A autoridade continua ocupando o cargo.'
            self.appoint(t,p,'pressão local organizada' if g else 'apoio local conhecido',g.memory[-1] if g and g.memory else None)
            if g:self.dissolve(g,'local_office_changed')
            return True,'Representação municipal alterada, sem revolução nacional.'
        if a=='seek_royal_aid':
            ruler=self.w.characters.get(goal.target_id);king=self.w.kingdoms.get(t.kingdom_id)
            if not ruler or ruler.id not in here or t.mayor_id!=p.id:return False,'Autoridade central não está no encontro.'
            amount=min(12,king.treasury) if ruler.personality.compassion+ self.e.graph.value(ruler.id,p.id,'confiança',10)>=60 else 0
            king.treasury-=amount;t.money+=amount
            self.emit('RoyalAidDecided',ruler,t.id,representative=p.id,money=amount);self.count('royal_aid',amount)
            return True,'Recursos existentes transferidos por decisão da autoridade central.'
        f=self.w.factions.get(n.context.get('faction_id')) if n else None
        if not f:return False,'Não há função organizacional conhecida.'
        if a=='recruit_member':
            return self.e.access.invite(p,f)
        if a=='report_to_faction':
            leader=self.w.characters.get(f.leader_id)
            if p.id!=f.leader_id and (not leader or leader.id not in here):return False,'O relatório exige encontro com liderança.'
            if p.id==f.leader_id and p.position.map_id!=p.town_id:
                return self.e.agency.follow_lead(p,p.town_id,n)
            p.social_state['last_report']=self.w.turn
            for fact in p.knowledge.values():
                if fact.kind in ('WantedIssued','CharacterAttacked','ProblemShared','DivineIntervention','PolicyDecided'):
                    self.remember(f,self.e.knowledge.transmitted(fact,p,leader))
            self.orders(leader,f);self.promote(leader,f,p)
            for fact in f.knowledge.values():
                if fact.kind in ('CharacterAttacked','CharacterKilled') and fact.target_id in f.member_ids and fact.confidence>=60 and fact.location and fact.location.map_id in self.w.towns:
                    f.norms['hostile_town']=fact.location.map_id
            self.emit('FactionReport',p,f.id,known_facts=list(f.knowledge)[-3:]);self.count('faction_report')
            return True,'Conhecimento transmitido por relatório presencial.'
        if a=='contribute':
            if p.money<=15:return False,'Não há recurso disponível para contribuição.'
            p.money-=1;f.money+=1;p.social_state['last_contribution']=self.w.turn
            self.emit('FactionContribution',p,f.id,money=1);self.count('contribution');return True,'Contribuição real transferida.'
        if a=='perform_assignment':
            order=f.assignments.get(p.id,{}).get('order')
            if not order or p.position!=Location(**order['location']):return False,'Ordem ou local não disponível.'
            fact=f.knowledge.get(order['fact'])
            if not fact:return False,'Fonte institucional indisponível.'
            self.e.knowledge.learn(p,fact,False)
            if f.purpose in ('justice','protection','mercenaries') and fact.kind=='WantedIssued':self.e.justice.on_fact(p,fact)
            # Serviço real: observação e assistência; não concede polícia a mercenário.
            self.e.conflicts.observe(p)
            patient=next((self.w.characters[i] for i in here if i!=p.id and self.w.characters[i].combat.injured>=6),None)
            aided=self.e.conflicts.first_aid(p,patient)[0] if patient else False
            pay=min(1,f.money);f.money-=pay;p.money+=pay
            record=f.assignments[p.id];record['deeds']=record.get('deeds',0)+int(aided);record.pop('order',None)
            self.emit('OrganizationalAction',p,f.id,purpose=f.purpose,source_fact=fact.event_id,paid=pay,assisted=patient.id if aided else None)
            self.count('organizational_action');return True,'Ordem conhecida cumprida com observação/serviço e custo.'
        return False,'Ação social desconhecida.'
    def orders(self,leader,f):
        facts=[x for x in f.knowledge.values() if x.location and x.location.map_id==leader.position.map_id]
        if not facts:return
        fact=facts[-1]
        need=self.e.needs.ensure(f,'organizational_survival',45,'report','Agir sobre relato conhecido',leader.id)
        need.context.update(subject_id=fact.target_id,source_event=fact.event_id)
        f.goal=Goal(self.w.allocate_id(),need.id,'perform_assignment',45,self.w.turn,leader.id,fact.location)
        if f.commitment is None:f.commitment=Commitment(self.w.allocate_id(),f.id,need.id,fact.event_id,leader.id,f.purpose,45,self.w.turn,self.w.turn)
        for q in self.living(f.member_ids):
            if q.position==leader.position:
                f.assignments[q.id]['order']={'fact':fact.event_id,'location':vars(fact.location),'issued_at':self.w.turn}
                self.emit('OrganizationalOrder',leader,q.id,faction_id=f.id,source_fact=fact.event_id);self.count('order')
    def promote(self,leader,f,p):
        record=f.assignments[p.id];index=f.ranks.index(record['rank'])
        if p.id==leader.id or index>=len(f.ranks)-2:return False
        if record.get('deeds',0)<2 or self.w.turn-record['joined_at']<72 or self.e.graph.value(leader.id,p.id,'confiança',10)<40:return False
        # Vaga e propósito relevantes; contribuição monetária sozinha não promove.
        next_rank=f.ranks[index+1]
        if sum(r['rank']==next_rank for r in f.assignments.values())>=max(1,len(f.member_ids)//4):return False
        record['rank']=next_rank;record['deeds']=0
        self.emit('FactionPromoted',leader,p.id,faction_id=f.id,rank=next_rank);self.count('promotion');return True
    def tick(self):
        if not self.w.social_initialized or self.w.turn%24:return
        for t in self.w.towns.values():
            if t.kind!='cidade' or t.kingdom_id is None:continue
            mayor=self.w.characters.get(t.mayor_id)
            if not mayor or not mayor.alive or mayor.town_id!=t.id:
                candidates=[p for p in self.local(t) if p.category=='comum' and p.profession not in ('guarda','soldado')]
                if candidates:self.appoint(t,max(candidates,key=lambda p:(p.personality.diligence+p.personality.honesty,-p.id)),'vacância por morte ou ausência')
            self.hierarchy(t)
            # Conservar apenas 24 propostas locais, encerradas primeiro.
            retired=[i for i in t.proposal_ids if self.w.proposals[i].status not in ('draft','submitted','deferred')]
            for i in retired[:-8]:
                self.w.proposals.pop(i);t.proposal_ids.remove(i)
                for g in self.w.groups.values():
                    if i in g.proposal_ids:g.proposal_ids.remove(i)
                    g.proposal_knowledge.pop(i,None)
                for key in ('known_proposals','decisions'):t.office[key]=[j for j in t.office.get(key,[]) if j!=i]
        for g in list(self.w.groups.values()):
            g.member_ids=[p.id for p in self.living(g.member_ids)]
            if g.cause=='expedition':
                if len(g.member_ids)<2 or self.w.turn-g.created_at>240:self.dissolve(g,'expedition_ended')
                continue
            if g.status=='active':
                if len(g.member_ids)<2 or self.w.turn-g.last_relevant>240:self.dissolve(g,'lost_relevance_or_members')
                elif g.leader_id not in g.member_ids:
                    g.leader_id=max(g.member_ids,key=lambda i:g.support.get(i,0));self.count('group_leadership_changed')
            if g.status!='active' and self.w.turn-g.last_relevant>240:
                # Eventos preservam identidade; remover apenas objetos já encerrados.
                for i in g.proposal_ids:self.w.proposals.pop(i,None)
                for t in self.w.towns.values():
                    t.proposal_ids=[i for i in t.proposal_ids if i in self.w.proposals]
                    for key in ('known_proposals','decisions'):t.office[key]=[i for i in t.office.get(key,[]) if i in self.w.proposals]
                for person in self.w.characters.values():
                    if g.id in person.group_ids:person.group_ids.remove(g.id)
                self.w.groups.pop(g.id)
        for f in self.w.factions.values():
            alive=self.living(f.member_ids)
            departed=[i for i in f.member_ids if i not in [q.id for q in alive]]
            if departed:f.norms['former_members']=list(dict.fromkeys(f.norms.get('former_members',[])+departed))[-8:]
            for id in list(f.assignments):
                if not any(q.id==id for q in alive):f.assignments.pop(id)
            f.member_ids=[q.id for q in alive]
            if not alive:f.status='dissolved';continue
            if f.leader_id not in f.member_ids:
                f.leader_id=max(alive,key=lambda p:(p.personality.diligence+self.e.graph.value(p.id,f.id,'lealdade',10),-p.id)).id
                f.assignments[f.leader_id]['rank']=f.ranks[-1];self.count('faction_leadership_changed')
            for q in alive:
                if q.id!=f.leader_id and q.health<30 and self.w.turn-f.assignments[q.id]['joined_at']>72 and q.personality.independence>75:
                    f.member_ids.remove(q.id);f.assignments.pop(q.id)
                    if f.id in q.organization_ids:q.organization_ids.remove(f.id)
                    self.emit('FactionDeserted',q,f.id,reason='physical_risk_and_independence');self.count('desertion')
