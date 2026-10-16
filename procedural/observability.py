"""História nativa V1: dados privados, sem RNG, Facts ou regras de gameplay.

NORMAL conserva decisões/recebimentos estruturais e anéis ordinários limitados.
AUDIT aumenta detalhes/anéis, sem duplicar o algoritmo de decisão. OFF mantém
somente identificadores causais dos Events, sem reter traces/recebimentos.
"""
from collections import defaultdict, deque
from contextlib import contextmanager

from .models import ActionAttempt, DecisionTrace, LearningReceipt

IMPORTANT = frozenset('''CharacterDied CharacterKilled CharacterAttacked CharacterIncapacitated
ItemStolen PersonalItemStolen LethalDecision LethalDecisionCreated TerminalDecision
ExecutionOpportunity GroupFormed NewGroupCreated GroupJoined GroupDissolved ExpeditionFormed
ProposalCreated ProposalSubmitted PolicyDecided PolicyDecision PolicyCreated PolicyCompleted
FactionFounded FactionFormalized GroupFormalized FactionJoined FactionMemberJoined FactionMemberLeft
FactionMembershipAccepted FactionLocalStatusChanged MayorAppointed LocalOfficeAssumed
DivineAudience DivineIntervention DivinityKilled Apotheosis DivineContractAccepted DivineContractBroken
POIExplored POIClaimed FactionHQChanged JourneyStarted JourneyArrived MigrationStarted MigrationArrived ResidentMoved WorkerMaterialized
KingdomFounded SuccessionChanged DivineManifestation DivineContractOffered DivineContractRefused
DivineContractAbandoned DivineContractFulfilled
PostKillAppraisal WantedIssued CharacterCaptured'''.split())
REASON_CODES = frozenset('''NO_KNOWN_ROUTE NO_KNOWN_TARGET INSUFFICIENT_MONEY NO_STOCK
ACTION_COOLDOWN LOW_SOCIAL_AFFINITY NO_AUTHORITY TARGET_NOT_PRESENT NO_CAPABILITY
NO_INPUT NO_WORKER NO_GENERATED_ACTION SURVIVAL_NOT_VIABLE EXCESS_RESERVE
TERMINAL_UNAVAILABLE FORMALIZATION_REQUIREMENTS'''.split())
FACT_KEYS=('source_fact','source_event','originating_fact','death_fact','belief_source','attack_fact')
FACT_LIST_KEYS=('source_facts','known_facts','deed_sources','contract_sources','faith_change_sources')


def fact_ids(context):
    """Somente campos cujo contrato identifica explicitamente eventos/Facts."""
    refs=[context.get(k) for k in FACT_KEYS]
    for key in FACT_LIST_KEYS:
        value=context.get(key,())
        if isinstance(value,(list,tuple,set)):refs.extend(value)
    for key in ('lethal_audit','action_audit'):
        nested=context.get(key)
        if isinstance(nested,dict):refs.extend(fact_ids(nested))
    decision=context.get('decision')
    if isinstance(decision,dict):refs.extend(decision.get('facts',()))
    return sorted({i for i in refs if isinstance(i,int) and not isinstance(i,bool) and i>0})


class EventIndex:
    """QUERY_WITH_CACHE: índices reconstruíveis; não entram no save."""
    def __init__(self,world):
        self.world=world
        self.events={}
        self.permanent=set()
        self.recent=deque()
        self.by={name:defaultdict(dict) for name in ('actor','target','location','kind','turn')}
        for event in world.history:self.add(event,True)
        for event in world.observability.event_archive.values():self.add(event,True)
        for event in world.events:self.add(event,event.id in self.permanent)

    def add(self,event,permanent=False):
        if permanent:self.permanent.add(event.id)
        if event.id in self.events:return
        self.events[event.id]=event
        for name in self.by:
            value=getattr(event, name+'_id' if name in ('actor','target') else name)
            self.by[name][value][event.id]=None
        self.recent.append(event.id)
        while len(self.recent)>4096:
            old=self.recent.popleft()
            if old in self.permanent:continue
            item=self.events.pop(old,None)
            if item:
                for name in self.by:
                    value=getattr(item,name+'_id' if name in ('actor','target') else name)
                    bucket=self.by[name][value];bucket.pop(old,None)
                    if not bucket:del self.by[name][value]

    def query(self,dimension,value):
        if dimension not in self.by:raise ValueError('Índice histórico desconhecido.')
        return tuple(self.events[i] for i in self.by[dimension].get(value,()))

    def reference(self,kind,target_id=None,context=None,actor_id=None):
        """QUERY: ID de uma emissão conhecida pelo código que criou a entidade."""
        for id in reversed(self.by['kind'].get(kind,{})):
            event=self.events[id]
            if actor_id is not None and event.actor_id!=actor_id:continue
            if target_id is not None and event.target_id!=target_id:continue
            if context and any(event.context.get(k)!=v for k,v in context.items()):continue
            return id
        return None


class HistoricalObserver:
    def __init__(self,world):
        self.world=world;self.data=world.observability
        if self.data.level not in ('OFF','NORMAL','AUDIT'):raise ValueError('Nível histórico inválido.')
        self.index=EventIndex(world);self.current=None;self.attempt=None
        self.important_receipts=defaultdict(list)
        for receipt in self.data.learning:self.important_receipts[receipt.event_id].append(receipt)

    def identifier(self,prefix):
        value=f'{prefix}{self.data.next_id}';self.data.next_id+=1
        return value

    def count(self,key):
        if self.data.level!='OFF':self.data.counters[key]=self.data.counters.get(key,0)+1

    @contextmanager
    def decision(self,person,lod):
        previous=self.current
        start_id=self.data.next_id
        is_player=getattr(person,'is_player',False)
        previous_counts=dict(self.data.counters) if is_player else None
        trace=DecisionTrace(self.identifier('d'),person.id,self.world.turn,lod)
        self.current=trace
        self.count('decisions')
        try:yield trace
        finally:
            self.current=previous
            if is_player and trace.success is False and not trace.emitted_event_ids:
                # Entrada rejeitada não avançou o mundo nem é decisão histórica.
                self.data.next_id=start_id;self.data.counters=previous_counts
                if trace.action_attempt_id:self.data.attempts.pop(trace.action_attempt_id,None)
            else:self.retain_trace(trace)

    def retain_trace(self,trace):
        previous=self.data.last_decision_ids.get(trace.actor_id)
        self.data.last_decision_ids[trace.actor_id]=trace.id
        if self.data.level=='OFF':return
        self.data.decisions[trace.id]=trace
        if previous and previous not in self.data.recent_decisions:self.discard_ordinary(previous)
        if trace.important:return
        self.data.recent_decisions.append(trace.id)
        limit=1024 if self.data.level=='AUDIT' else 256
        while len(self.data.recent_decisions)>limit:
            old=self.data.recent_decisions.pop(0)
            self.discard_ordinary(old)

    def discard_ordinary(self,id):
        row=self.data.decisions.get(id)
        if row and not row.important and self.data.last_decision_ids.get(row.actor_id)!=id:
            del self.data.decisions[id]
            if row.action_attempt_id:self.data.attempts.pop(row.action_attempt_id,None)

    def detail(self,field,row):
        trace=self.current
        if not trace or self.data.level=='OFF':return
        values=getattr(trace,field)
        limit=128 if self.data.level=='AUDIT' else 12
        if len(values)<limit:values.append(row)
        else:trace.truncated[field]=trace.truncated.get(field,0)+1

    def candidates(self,need,choices):
        if not choices:
            self.blocked(need,None,'NO_GENERATED_ACTION')
        for choice in choices:
            self.detail('generated_actions',self.option(need,choice))

    @staticmethod
    def option(need,choice):
        return {'need_episode_id':need.need_episode_id,'action':choice.action,
                'target_id':choice.target_id,'resource_kind':choice.resource_kind}

    def blocked(self,need,choice,reason,details=None):
        if reason not in REASON_CODES:raise ValueError('reason_code histórico desconhecido.')
        row=self.option(need,choice) if choice else {'need_episode_id':need.need_episode_id,'action':None}
        row['reason_code']=reason
        if details:row['details']=details
        self.detail('blocked_actions',row)
        self.count('blocked:'+reason)

    def scored(self,need,choice):
        row=self.option(need,choice);row['score']=choice.score
        if self.data.level=='AUDIT':row['terms']=dict(choice.considerations)
        self.detail('evaluated_scores',row)

    def gate(self,action,reason,target_id=None,details=None):
        if reason not in REASON_CODES:raise ValueError('reason_code histórico desconhecido.')
        self.detail('blocked_actions',{'action':action,'target_id':target_id,'reason_code':reason,'details':details})
        self.count('blocked:'+reason)

    def selected(self,need,choice,goal):
        trace=self.current
        if not trace:return
        trace.need_episode_id=need.need_episode_id;trace.need_kind=need.kind
        trace.need_priority=need.priority;trace.source_fact_ids=fact_ids(need.context)
        if need.source.startswith('event:'):
            try:trace.source_fact_ids=sorted(set(trace.source_fact_ids+[int(need.source.split(':')[1])]))
            except ValueError:pass
        trace.selected_action=choice.action;trace.goal_id=goal.id
        trace.selected_score=choice.score;trace.selected_target_id=choice.target_id
        trace.selected_resource_kind=choice.resource_kind

    @contextmanager
    def action(self,person,goal):
        previous=self.attempt
        attempt=ActionAttempt(self.identifier('a'),person.id,self.world.turn,goal.id,goal.action,goal.target_id)
        self.attempt=attempt
        if self.current:
            self.current.action_attempt_id=attempt.id
            self.current.goal_id=goal.id;self.current.selected_action=goal.action
        try:yield attempt
        finally:
            self.attempt=previous
            if self.data.level!='OFF':self.data.attempts[attempt.id]=attempt

    def outcome(self,result):
        if self.attempt:self.attempt.success,self.attempt.outcome=result
        if self.current:self.current.success,self.current.outcome=result

    def on_event(self,event,parents=()):
        refs=set(parents)|set(fact_ids(event.context))
        if self.current:
            event.decision_id=self.current.id
            refs.update(self.current.source_fact_ids)
            self.current.emitted_event_ids.append(event.id)
            if event.kind in IMPORTANT:self.current.important=True
        if self.attempt:
            event.action_attempt_id=self.attempt.id
            self.attempt.emitted_event_ids.append(event.id)
        refs.discard(event.id)
        # IDs de evento são monotônicos; nenhuma ligação futura/autorreferência.
        event.parent_event_ids=sorted(i for i in refs if isinstance(i,int) and i<event.id)
        if event.kind in ('CharacterDied','CharacterKilled') and event.target_id is not None:
            last=self.data.last_decision_ids.get(event.target_id)
            if last:
                # Relação temporal de contexto; NÃO é prova de causa da morte.
                event.related_decision_ids=[last]
                row=self.data.decisions.get(last)
                if row:
                    row.important=True;row.related_event_ids.append(event.id)
        self.index.add(event,event.historical)
        if event.kind in IMPORTANT and self.data.level!='OFF':
            self.retain_event(event)
            for id in event.parent_event_ids:
                parent=self.index.events.get(id)
                if parent:self.retain_event(parent)
        self.count('events')

    def retain_event(self,event):
        if event.id not in self.index.permanent:
            self.data.event_archive[event.id]=event
            self.index.permanent.add(event.id)
        row=self.data.decisions.get(event.decision_id)
        if row:row.important=True

    def learned(self,person,fact,previous,firsthand):
        if self.data.level=='OFF':return
        receipt=LearningReceipt(person.id,fact.event_id,self.world.turn,
            'direct' if firsthand else fact.source_kind,fact.source_id,
            previous.confidence if previous else 0,fact.confidence)
        if fact.kind in IMPORTANT:
            self.data.learning.append(receipt);self.important_receipts[fact.event_id].append(receipt)
        else:
            self.data.recent_learning.append(receipt)
            limit=4096 if self.data.level=='AUDIT' else 1024
            if len(self.data.recent_learning)>limit:del self.data.recent_learning[0]
        self.count('learning_receipts')

    def event_details(self,event_id):
        """QUERY: verdade, rastros privados e recebimentos em coleções distintas."""
        event=self.index.events.get(event_id)
        if not event:return None
        trace=self.data.decisions.get(event.decision_id)
        return {'event':event,'actor':self.world.characters.get(event.actor_id),
                'target':self.world.characters.get(event.target_id),'location':event.location,'turn':event.turn,
                'parents':tuple(self.index.events.get(i) for i in event.parent_event_ids),
                'parent_event_ids':tuple(event.parent_event_ids),'decision':trace,
                'attempt':self.data.attempts.get(event.action_attempt_id),
                'related_decisions':tuple(self.data.decisions.get(i) for i in event.related_decision_ids),
                'related_fact_ids':tuple(sorted(set(event.parent_event_ids)|set(trace.source_fact_ids if trace else ()))),
                'learning_receipts':tuple(self.important_receipts.get(event_id,()))+
                    tuple(r for r in self.data.recent_learning if r.event_id==event_id)}
