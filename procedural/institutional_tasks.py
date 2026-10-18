"""Obrigações persistentes, executadas por pessoas informadas e autorizadas."""
from .models import InstitutionalTask,Goal,Fact,Location
from .needs import FINISHED


class InstitutionalTasks:
    def __init__(self,e):self.e,self.w=e,e.world

    def representatives(self,g):
        return [g.leader_id]+list(g.plan.get('representatives',()))

    def authorize(self,p,g):
        if p.id!=g.leader_id:return
        # Delegação exige encontro e consentimento por compromisso já assumido.
        present=[q for q in self.e.society.living(g.member_ids) if q.id!=p.id and q.position==p.position]
        ids=g.plan.setdefault('representatives',[])
        added=[q.id for q in sorted(present,key=lambda q:(-q.personality.diligence,q.id))[:2] if q.id not in ids]
        ids.extend(added)
        if added:self.e.recorder.emit('InstitutionalDelegation',f'{p.name} autorizou representantes presentes.',p.id,g.id,p.position,
            historical=True,context={'group_id':g.id,'authorized':added,'roles':['representative'],'delegator':p.id})

    def authorized(self,p,task):
        if not p.alive:return False
        if task.institution_type=='group':
            g=self.w.groups.get(task.institution_id)
            return bool(g and g.status=='active' and p.id in g.member_ids and p.id in self.representatives(g))
        t=self.w.towns.get(task.institution_id)
        if not t or p.town_id!=t.id:return False
        if 'worker' in task.authorized_roles:
            policy=self.w.institutional_policies.get(task.target)
            return bool(policy and self.e.institutions.worker_eligible(p,policy))
        return p.id==t.mayor_id or p.id in t.office.get('clerks',())

    def issue(self,p,institution_type,institution_id,kind,target,location,priority=55,requirements=None,roles=None):
        for task in self.w.institutional_tasks.values():
            if task.institution_type==institution_type and task.institution_id==institution_id and task.kind==kind and task.target==target and task.status in ('pending','blocked'):
                return task
        task=InstitutionalTask(self.w.allocate_id(),p.id,institution_type,institution_id,kind,target,location,
            self.w.turn,priority,requirements or {},roles or ['leader','representative'])
        self.w.institutional_tasks[task.id]=task
        ev=self.e.recorder.emit('InstitutionalTaskIssued',f'{p.name} registrou a obrigação {kind}.',p.id,task.id,p.position,
            historical=True,context={'task_id':task.id,'institution_type':institution_type,'institution_id':institution_id,
                'task_kind':kind,'target':target,'priority':priority,'authorized_roles':task.authorized_roles,
                'source_facts':task.requirements.get('source_facts',[])})
        task.event_id=task.last_event_id=ev.id
        return task

    def on_fact(self,p,fact):
        if fact.kind=='InstitutionalTaskIssued' and fact.confidence>=60:
            task=self.w.institutional_tasks.get(fact.context.get('task_id'))
            if task and self.authorized(p,task):
                known=p.social_state.setdefault('known_tasks',[])
                if task.id not in known:known.append(task.id)
                p.social_state.setdefault('known_task_status',{}).setdefault(task.id,'pending')
        if fact.confidence>=60:
            for id in p.social_state.get('known_tasks',()):
                task=self.w.institutional_tasks.get(id)
                if not task:continue
                completed=(fact.kind=='InstitutionalTaskCompleted' and fact.context.get('task_id')==id or
                    fact.kind=='ProposalSubmitted' and task.kind=='deliver_proposal' and fact.context.get('proposal_id')==task.target or
                    fact.kind=='PolicyCompleted' and task.kind=='work_policy' and fact.target_id==task.target or
                    fact.kind=='GroupMeeting' and task.kind=='hold_meeting' and fact.target_id==task.target and fact.turn>=task.created)
                if completed:p.social_state.setdefault('known_task_status',{})[id]='completed'
        if fact.kind=='PolicyDecided' and fact.confidence>=60:
            for g in self.w.groups.values():
                if p.id in self.representatives(g) and p.id in g.member_ids and fact.target_id in g.proposal_ids:
                    if fact.event_id not in g.plan.get('relayed_responses',()):
                        self.issue(p,'group',g.id,'return_response',g.id,self.w.towns[g.town_id].market,55,
                                   {'source_facts':[fact.event_id]})

    def refresh(self,p):
        # Consulta de balcão presencial. Ler registro não transmite a cidade inteira.
        t=self.w.towns.get(p.position.map_id)
        if t and p.position==t.market:
            for task in self.w.institutional_tasks.values():
                if task.institution_type!='town' or task.institution_id!=t.id or not self.authorized(p,task):continue
                ev=self.e.observability.index.events.get(task.last_event_id or task.event_id)
                if ev:
                    fact=Fact(ev.id,ev.kind,ev.actor_id,ev.target_id,ev.location,ev.turn,ev.description,
                              source_kind='known',confidence=80,context=ev.context)
                    self.e.knowledge.learn(p,fact,False)
                policy=self.w.institutional_policies.get(task.target) if task.kind=='work_policy' else None
                if policy and policy.id not in p.known_policies:
                    for event in reversed(self.w.history):
                        if event.kind=='PolicyCreated' and event.target_id==policy.id:
                            self.e.knowledge.learn(p,Fact(event.id,event.kind,event.actor_id,event.target_id,event.location,event.turn,event.description,
                                source_kind='known',confidence=80,context=event.context),False);break
        for id in list(p.social_state.get('known_tasks',())):
            task=self.w.institutional_tasks.get(id)
            if not task or p.position!=task.location or not self.authorized(p,task):continue
            ev=self.e.observability.index.events.get(task.last_event_id)
            if ev:
                self.e.knowledge.learn(p,Fact(ev.id,ev.kind,ev.actor_id,ev.target_id,ev.location,ev.turn,ev.description,
                    source_kind='known',confidence=80,context=ev.context),False)
        available=[]
        for id in p.social_state.get('known_tasks',()):
            task=self.w.institutional_tasks.get(id)
            if not task or p.social_state.get('known_task_status',{}).get(id,'pending') not in ('pending','blocked') or not self.authorized(p,task):continue
            if self.w.turn<task.requirements.get('not_before',0):continue
            available.append(task)
        if available:
            task=min(available,key=lambda t:(-t.priority,t.created,t.id))
            n=self.e.needs.ensure(p,'institutional_task',task.priority,'received_obligation','Cumprir obrigação institucional conhecida',task.id)
            n.context.update(task_id=task.id,known_location=vars(task.location),source_facts=task.requirements.get('source_facts',[]))
        else:self.e.needs.satisfy(p,'institutional_task')

    def candidates(self,p,n):
        if n.kind=='institutional_task':tasks=[self.w.institutional_tasks.get(n.target_id)]
        elif n.kind=='organizational_survival':
            from .organization_context import organization_id
            gid=organization_id(n.context,'group')
            tasks=[self.w.institutional_tasks[i] for i in p.social_state.get('known_tasks',())
                   if i in self.w.institutional_tasks and self.w.institutional_tasks[i].institution_type=='group'
                   and self.w.institutional_tasks[i].institution_id==gid]
        else:return []
        tasks=[t for t in tasks if t and p.social_state.get('known_task_status',{}).get(t.id,'pending') in ('pending','blocked') and self.authorized(p,t)
               and self.w.turn>=t.requirements.get('not_before',0)]
        if not tasks:return []
        task=min(tasks,key=lambda t:(-t.priority,t.created,t.id))
        if task.location.map_id!=p.position.map_id:
            return self.e.geography.candidates(p,task.location.map_id,'institutional_task',n)
        return [('perform_institutional_task',task.location,task.id)]

    def closed_by_event(self,kind,target,event,actor):
        for task in self.w.institutional_tasks.values():
            if task.kind==kind and task.target==target and task.status in ('pending','blocked'):
                task.status='completed';task.last_event_id=event.id
                task.executor_ids=list(dict.fromkeys(task.executor_ids+[actor.id]))

    def execute(self,p,goal,n):
        task=self.w.institutional_tasks.get(goal.target_id)
        if (not task or task.id not in p.social_state.get('known_tasks',()) or not self.authorized(p,task)
                or task.status not in ('pending','blocked') or self.w.turn<task.requirements.get('not_before',0) or p.position!=task.location):return False,'Tarefa desconhecida, sem autorização ou sem presença.'
        task.attempts+=1
        if task.kind=='deliver_proposal':result=self.e.institutions.submit(p,self.w.proposals[task.target])
        elif task.kind=='return_response':result=self.e.collective.execute(p,Goal(goal.id,goal.need_id,'relay_response',goal.score,self.w.turn,task.target),None)
        elif task.kind=='hold_meeting':result=self.e.society.meeting(p,self.w.groups[task.target])
        elif task.kind=='work_policy':result=self.e.institutions.policy_work(p,self.w.institutional_policies[task.target])
        else:return False,'Tipo de obrigação não possui executor.'
        task.status='completed' if result[0] and (task.kind!='work_policy' or self.w.institutional_policies[task.target].status=='completed') else 'pending' if result[0] else 'blocked'
        task.block_reason=None if result[0] else result[1]
        if result[0]:
            task.executor_ids=list(dict.fromkeys(task.executor_ids+[p.id]))
            ev=self.e.recorder.emit('InstitutionalTaskCompleted' if task.status=='completed' else 'InstitutionalTaskProgress',
                f'{p.name} executou {task.kind}.',p.id,task.id,p.position,historical=True,
                context={'task_id':task.id,'task_kind':task.kind,'institution_type':task.institution_type,
                    'institution_id':task.institution_id,'delegated':p.id!=task.issuer,'issuer':task.issuer,
                    'source_facts':task.requirements.get('source_facts',[])})
            task.last_event_id=ev.id
        self.e.audit.count('task_delegated' if p.id!=task.issuer else 'task_issuer_executed')
        return result
