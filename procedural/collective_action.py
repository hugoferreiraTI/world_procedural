"""Continuidade presencial de grupos e um conjunto pequeno de ações de facção."""
from .organization_context import organization_id, bind_organization
from .models import Location,Goal
from .navigation import distance
from .action_pressure import clamp

ACTIONS={'attend_group','represent_travel','relay_response','faction_prepare','faction_raid','plan_incursion','attend_faction'}

class CollectiveActionSystem:
    def __init__(self,e):self.e,self.w=e,e.world
    def bootstrap_routes(self):
        for t in self.w.towns.values():
            authority=self.w.towns.get(t.authority_town_id) if t.kind=='vila' else t
            if authority:t.office['representing_town']=authority.id
            for id in t.resident_ids:
                p=self.w.characters[id]
                for place in (t,authority):
                    if place:p.known_towns.setdefault(place.id,{'position':vars(place.position),'confidence':90,'learned_at':self.w.turn,'source':'jurisdiction_known','source_fact':None})

    def authority(self,g):
        home=self.w.towns[g.town_id]
        return self.w.towns.get(home.office.get('representing_town',home.id))
    def group_pressure(self,g,p):
        r=g.action_pressure
        if r.updated_at==self.w.turn:return
        present=[self.w.characters[i] for i in g.member_ids if i in self.e.spatial.at(p.position)]
        communicated=[f for f in g.knowledge.values() if f.kind=='ProblemShared' and f.confidence>=30
                      and self.w.turn-f.turn<=240 and f.context.get('cause')==g.cause]
        own=[self.e.society.pressure(q) for q in present]
        relevant=[x[2] for x in own if x and x[:2]==(g.cause,g.subject_id)]
        if len(present)==len(g.member_ids) and not relevant:severity=0
        else:severity=max(relevant+[f.context.get('severity',0)*max(.25,1-(self.w.turn-f.turn)/300) for f in communicated]+[0])
        relief=g.plan.get('relief_until',-1)>self.w.turn
        if relief:severity*=.6
        harmed=[f for f in g.knowledge.values() if f.kind in ('CharacterAttacked','CharacterKilled')
                and f.target_id in g.member_ids and f.confidence>=60]
        grave=bool(harmed or g.failures>=2 and severity>=65 and self.w.turn-g.created_at>=72)
        world=max(severity,85 if harmed else 80 if grave else 0)
        leader=self.w.characters[g.leader_id];support=sum(g.support.values())/max(1,len(g.support))
        value=self.e.action_pressure.disposition(world,leader.personality.persistence,support,g.failures,g.investment,0)
        g.pressure=clamp(world)
        self.e.action_pressure.update(g,r,value,world,'known_member_harm' if harmed else 'received_failures_and_deprivation' if grave else 'shared_problem',
            [f.event_id for f in harmed+communicated],agent_type='group')
        if not severity and not harmed:r.failures=0
    def faction_assessment(self,f,p):
        facts=[x for x in f.knowledge.values() if x.confidence>=60 and self.w.turn-x.turn<=240]
        hardship=[x for x in facts if x.kind=='ProblemShared' and x.actor_id in f.member_ids and x.context.get('severity',0)>=65]
        harm=[x for x in facts if x.kind in ('CharacterAttacked','CharacterKilled') and x.target_id in f.member_ids+f.norms.get('former_members',[])]
        hostile=f.norms.get('hostile_town')
        motive=[x for x in harm if x.location and x.location.map_id==hostile]
        justified=bool(motive or hardship and f.action_pressure.failures>=2)
        severity=85 if motive else 75 if hardship else 35 if len(f.member_ids)<2 else 20 if facts else 0
        present=[self.w.characters[i] for i in f.member_ids if i in self.e.spatial.at(p.position) and self.w.characters[i].health>30]
        resources=sum(self.e.items.count(q.id,'food') for q in present)
        fighters=sum(bool(self.e.conflicts.weapon(q)) for q in present)
        capacity=min(100,len(present)*20+fighters*10+min(20,resources*5))
        perceived=clamp(capacity*(.5+p.personality.courage/100))
        risk=f.norms.get('risk',p.personality.courage/100)
        pressure=self.e.action_pressure.disposition(severity,p.personality.persistence,perceived,
            f.action_pressure.failures,0,max(p.fatigue/180,max(p.hunger,p.thirst)/250))
        eligible=bool(justified and hostile in p.known_towns and f.norms.get('allow_theft') and
            not f.norms.get('harm_civilians',False) and len(present)>=2 and resources>=2 and
            capacity>=55 and perceived>=40 and risk>=.5 and pressure>=40 and
            self.w.turn-f.plan.get('last_raid',-1000)>=72 and
            (f.action_pressure.failures>=2 or motive and any(x.kind=='CharacterKilled' for x in motive)))
        return {'eligible':eligible,'world_pressure':severity,'action_pressure':pressure,'eligibility_causes':['known_member_harm'] if motive else ['continued_member_deprivation'] if hardship else ['purpose_outreach'],
            'source_facts':[x.event_id for x in (motive or hardship or facts)[-3:]],'capacity':capacity,
            'perceived_capacity':perceived,'major_barriers':[] if eligible else ['insufficient_cause_capacity_or_ideological_permission'],
            'why_this_target':hostile,'why_now':'known_continued_pressure',
            'why_lower_options_failed_or_were_rejected':f.action_pressure.failures,'selected_alternative':'faction_raid'}
    def refresh(self,p):
        for i in p.group_ids:
            g=self.w.groups.get(i)
            if g and g.status=='active' and g.cause!='expedition':self.group_pressure(g,p)
        n=p.needs.get('organizational_survival')
        if not n:return
        g=self.w.groups.get(organization_id(n.context,'group'))
        if g and g.status=='active':
            n.base_urgency=min(82,35+g.action_pressure.value*.55)
            pending=any(g.proposal_knowledge.get(i,{}).get('status') in ('draft','submitted','deferred') for i in g.proposal_ids)
            destination=self.authority(g) if pending and not self.responses(p,g) else self.w.towns[g.town_id]
            if destination:n.context['known_location']=vars(destination.market)
            # Plano de encontro é comunicado na formação/adesão, não posição remota.
            if (self.w.turn-g.created_at)%24<6:n.base_urgency=min(85,n.base_urgency+10)
        f=self.w.factions.get(organization_id(n.context,'faction'))
        if f and f.action_pressure.updated_at!=self.w.turn:
            a=self.faction_assessment(f,p)
            value=self.e.action_pressure.disposition(a['world_pressure'],p.personality.persistence,a['perceived_capacity'],
                f.action_pressure.failures,0,0)
            self.e.action_pressure.update(f,f.action_pressure,value,a['world_pressure'],a['eligibility_causes'][0],a['source_facts'],'faction')
            n.base_urgency=min(75,40+value*.4)
    def responses(self,p,g):
        delivered=g.plan.get('relayed_responses',())
        return [f for f in p.knowledge.values() if f.kind=='PolicyDecided' and
                (f.context.get('group_id')==g.id or g.id in f.context.get('supporting_groups',()))
                and f.target_id in g.proposal_ids and f.confidence>=30
                and f.event_id>=g.proposal_knowledge.get(f.target_id,{}).get('response_fact',-1)
                and f.event_id not in delivered]
    def travel(self,p,target,n):
        return self.e.geography.candidates(p,target,n.kind,n)

    def local_group_candidates(self,p,g,home):
        if p.id==g.leader_id:
            result=[('meet_group',home.market,g.id)] if self.w.turn-g.last_meeting>=24 else []
            if g.failures and self.w.turn-p.social_state.get('last_protest',-1000)>=48:result.append(('protest',home.market,g.id))
            if home.kind=='cidade' and g.responsibility_id and g.pressure>=85 and g.failures>=3:
                result.append(('assume_local_office',home.market,g.id))
            return result
        return [('attend_group',home.market,g.id)] if (self.w.turn-g.created_at)%24<6 else []

    def candidates(self,p,n):
        if n.kind!='organizational_survival':return None
        g=self.w.groups.get(organization_id(n.context,'group'))
        if g and g.status=='active':
            town=self.authority(g);home=self.w.towns[g.town_id]
            delivery=g.plan.get('proposal_delivery_needed')
            if p.id==g.leader_id and delivery in self.w.proposals:
                if p.position.map_id!=town.id:return self.travel(p,town.id,n)
                return [('support_proposal',town.market,delivery)]
            replies=self.responses(p,g)
            if replies:
                if p.position.map_id!=home.id:return self.travel(p,home.id,n)
                return [('relay_response',home.market,g.id)]+self.local_group_candidates(p,g,home)
            pending=[self.w.proposals[i] for i in g.proposal_ids if i in self.w.proposals and
                g.proposal_knowledge.get(i,{}).get('status') in ('draft','submitted','deferred')]
            if p.id==g.leader_id and pending and town:
                if p.position.map_id!=town.id:return self.travel(p,town.id,n)
                if g.proposal_knowledge[pending[0].id]['status']=='draft':return [('submit_proposal',town.market,pending[0].id)]
                if self.w.turn-p.social_state.get('last_policy_read',-1000)>=12:return [('read_response',town.market,g.id)]
                return [('attend_group',town.market,g.id)]
            if p.position.map_id!=home.id:return self.travel(p,home.id,n)
            return self.local_group_candidates(p,g,home)
        f=self.w.factions.get(organization_id(n.context,'faction'))
        if f:
            order=f.assignments.get(p.id,{}).get('order',{})
            if order.get('action')=='raid' and self.w.turn-order['issued_at']<=240:
                target=order['location']['map_id']
                if p.position.map_id!=target:return self.travel(p,target,n)
                if p.position!=Location(**order['location']):return [('attend_faction',Location(**order['location']),f.id)]
                if p.id!=f.leader_id:return [('attend_faction',None,f.id)]
        if f and p.id==f.leader_id:
            order=f.assignments.get(p.id,{}).get('order',{})
            service=[('perform_assignment',Location(**order['location']),f.id)] if order and order.get('action')!='raid' else []
            a=self.faction_assessment(f,p)
            if a['eligible'] and p.position.map_id==a['why_this_target']:
                return service+[('faction_raid',self.w.towns[a['why_this_target']].market,f.id)]
            if a['eligible']:return service+[('plan_incursion',None,f.id)]
            choices=list(service)
            if p.position.map_id!=p.town_id:
                choices.extend(self.e.society._outreach_candidates(p,n))
            else:
                for id in self.e.spatial.at(p.position):
                    q=self.w.characters[id]
                    if q.id!=p.id and not q.organization_ids and self.e.society.affinity(q,p,f.purpose)>=35:
                        choices.append(('invite_person',None,f.id))
                if self.w.turn-p.social_state.get('last_report',-1000)>=24:choices.append(('report_to_faction',None,f.id))
                if self.w.turn-p.social_state.get('last_faction_prepare',-1000)>=24:
                    choices.append(('faction_prepare',p.known_places.get('market',p.position),f.id))
            return choices
        return None
    def execute(self,p,goal,n):
        if goal.action=='represent_travel':
            before=p.position;result=self.e.agency.follow_lead(p,goal.target_id,n)
            g=self.w.groups.get(organization_id(n.context,'group')) if n else None
            if g and g.status=='active' and before!=p.position:g.last_relevant=self.w.turn
            return result
        g=self.w.groups.get(goal.target_id)
        if goal.action in ('attend_group','relay_response') and n and n.context.get('organization_type'):
            if organization_id(n.context,'group')!=goal.target_id:return False,'Intenção pertence a outra organização.'
        if goal.action=='attend_group':
            if not g or p.id not in g.member_ids:return False,'Grupo conhecido indisponível.'
            p.social_state['group_attendance_until']=self.w.turn+4
            return True,'Presença no encontro planejado; tempo consumido sem ação automática do grupo.'
        if goal.action=='relay_response':
            if not g or p.position!=self.w.towns[g.town_id].market:return False,'Resposta precisa retornar fisicamente ao grupo.'
            present=[self.w.characters[i] for i in g.member_ids if i in self.e.spatial.at(p.position)]
            if len(present)<2 or p.id not in self.e.tasks.representatives(g):return False,'Representante e outro membro precisam estar presentes.'
            replies=self.responses(p,g)
            if not replies:return False,'Não há resposta nova recebida.'
            for fact in replies:
                for q in present:
                    if q.id!=p.id:self.e.knowledge.learn(q,self.e.knowledge.transmitted(fact,p,q),False)
                self.e.society.react(p,fact)
                delivered=g.plan.setdefault('relayed_responses',[])
                if fact.event_id not in delivered:delivered.append(fact.event_id)
                del delivered[:-12]
            self.e.recorder.emit('ResponseRelayed','Uma resposta recebida voltou ao grupo.',p.id,g.id,p.position,
                historical=True,context={'source_facts':[x.event_id for x in replies],'recipients':[q.id for q in present]})
            self.e.action_pressure.count('consequences:group');return True,'Resposta conhecida transmitida presencialmente.'
        f=self.w.factions.get(goal.target_id)
        if not f or p.id not in f.member_ids:return False,'Função organizacional indisponível.'
        if n and n.context.get('organization_type') and organization_id(n.context,'faction')!=f.id:
            return False,'Intenção pertence a outra organização.'
        if goal.action=='attend_faction':return True,'Membro presente para ação institucional conhecida; nenhuma agressão automática.'
        if goal.action=='plan_incursion':
            a=self.faction_assessment(f,p)
            if p.id!=f.leader_id or not a['eligible']:return False,'Plano sem liderança, contexto e capacidade.'
            t=self.w.towns[a['why_this_target']]
            fact=next((f.knowledge[i] for i in reversed(a['source_facts']) if i in f.knowledge),None)
            if not fact:return False,'Falta causa conhecida para a ordem.'
            recipients=[]
            for q in self.e.society.living(f.member_ids):
                if q.position!=p.position:continue
                self.e.knowledge.learn(q,self.e.knowledge.transmitted(fact,p,q),False)
                q.known_towns[t.id]={'position':vars(t.position),'confidence':80,'learned_at':self.w.turn,'source':'received_organizational_route','source_fact':fact.event_id}
                f.assignments[q.id]['order']={'action':'raid','location':vars(t.market),'fact':fact.event_id,'issued_at':self.w.turn}
                recipients.append(q.id)
            p.fatigue=min(100,p.fatigue+2)
            self.e.recorder.emit('OrganizationalOrder','Uma incursão foi planejada por causa conhecida.',p.id,f.id,p.position,
                historical=True,context={'recipients':recipients,'action_audit':a,'source_fact':fact.event_id})
            return True,'Ordem entregue a membros presentes; deslocamento e confronto ainda precisam acontecer.'
        if goal.action=='faction_prepare':
            # Contribuição e abastecimento transferem somente itens/moedas existentes.
            moved=0
            for q in self.e.society.living(f.member_ids):
                if q.position!=p.position:continue
                if p.position.map_id==f.headquarters_id and self.e.items.count(q.id,'food')>2:self.e.items.transfer(q.id,f.id,self.e.items.first(q.id,'food'));moved+=1
                if q.money>15:q.money-=1;f.money+=1;moved+=1
            p.social_state['last_faction_prepare']=self.w.turn
            self.e.recorder.emit('OrganizationalPreparation','A organização tentou preparar capacidade.',p.id,f.id,p.position,
                context={'resources_transferred':moved,'reason':f.action_pressure.reason})
            if moved:self.e.action_pressure.count('consequences:faction')
            return bool(moved),'Capacidade custeada com recursos existentes.' if moved else 'Nenhum excedente disponível.'
        if goal.action=='faction_raid':
            a=self.faction_assessment(f,p);t=self.w.towns.get(p.position.map_id)
            if not a['eligible'] or not t or p.position!=t.market or t.id!=a['why_this_target']:return False,'Sem causa, capacidade, ideologia e presença para incursão.'
            members=[q for q in self.e.society.living(f.member_ids) if q.position==p.position and q.health>30]
            guards=[self.w.characters[i] for i in self.e.spatial.at(p.position) if self.w.characters[i].profession in ('guarda','soldado') and i not in f.member_ids]
            if not guards and not self.e.items.count(t.id,'food'):return False,'O alvo não tem o suprimento procurado.'
            for q in members[:2]:self.e.items.consume(q.id,'food');q.fatigue=min(100,q.fatigue+8)
            if guards:
                # Confronto real, sem declarar uma cidade destruída por pontuação.
                result=self.e.conflicts.execute(p,Goal(goal.id,goal.need_id,'attack',goal.score,self.w.turn,guards[0].id),n)
                outcome={'blocked_by_guard':guards[0].id,'physical_attack':result[0]}
            else:
                stolen=min(2,self.e.items.count(t.id,'food'))
                if not stolen:return False,'O alvo não tem o suprimento procurado.'
                self.e.items.transfer(t.id,f.id,self.e.items.first(t.id,'food'),stolen)
                event=self.e.recorder.emit('ItemStolen','Suprimentos foram roubados numa incursão.',p.id,t.id,p.position,
                    historical=True,context={'town_id':t.id,'faction_id':f.id,'quantity':stolen,'product':'food','actor_groups':list(p.group_ids)})
                outcome={'stolen':stolen,'source_fact':event.id}
            self.e.recorder.emit('OrganizationalAction','Incursão organizacional com consequência física.',p.id,f.id,p.position,
                historical=True,context={'purpose':f.purpose,'action':'raid','action_audit':{**a,'action_pressure':f.action_pressure.value},'consequence':outcome})
            f.plan['last_raid']=self.w.turn;self.e.action_pressure.count('consequences:faction')
            for record in f.assignments.values():
                if record.get('order',{}).get('action')=='raid':record.pop('order')
            return True,'Incursão limitada executada; localidade não foi destruída.'
        return False,'Ação coletiva indisponível.'
