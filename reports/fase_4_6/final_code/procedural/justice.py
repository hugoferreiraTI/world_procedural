"""Evidência conhecida por autoridades locais; não é um rastreador global."""
from collections import defaultdict
import heapq

from .models import WantedRecord
from .rules import INTERACTION, AGENCY
from dataclasses import replace
from .needs import FINISHED

CRIMES = {'ItemStolen':1, 'CharacterThreatened':2, 'CharacterAttacked':3, 'CharacterKilled':5}


class JusticeSystem:
    def __init__(self, engine):
        self.engine,self.world = engine,engine.world
        self.by_guard=defaultdict(set)
        self.active={}
        self.active_cases=defaultdict(set)
        self.expiries=[]
        for record in self.world.wanted_records.values():
            if self.world.turn-record.created_at<=self.duration(record):
                heapq.heappush(self.expiries,(record.created_at+self.duration(record)+1,record.id))
                for i in record.known_by:
                    if record.known_status.get(i,'active')=='active':self.by_guard[i].add(record.id)
                if record.status=='active':
                    key=record.jurisdiction,record.suspect_id
                    self.active[key]=record.id
                    self.active_cases[key].add(record.id)

    def on_fact(self, person, fact):
        if person.profession!='guarda' or fact.confidence<INTERACTION.warrant_confidence:
            return
        if fact.kind in ('CharacterCaptured','CharacterKilled','CharacterDied','GuardResponded'):
            for record in self.raw_known_active(person):
                if record.suspect_id==fact.target_id:
                    record.known_status[person.id]='captured' if fact.kind=='CharacterCaptured' else 'resolved' if fact.kind=='GuardResponded' else 'dead'
                    self.by_guard[person.id].discard(record.id)
            if fact.kind!='CharacterKilled':return
        if fact.kind=='WantedIssued':
            record=self.world.wanted_records.get(fact.context.get('record_id'))
            if record and record.jurisdiction==person.town_id and self.world.turn-fact.turn<=168:
                if person.id not in record.known_by:record.known_by.append(person.id)
                self.by_guard[person.id].add(record.id)
                record.known_status[person.id]='active'
                record.known_severity[person.id]=fact.context.get('severity',1)
                record.known_facts[person.id]=fact.event_id
                location=fact.context.get('last_known_location')
                if location and fact.turn>=record.location_turns.get(person.id,-1):
                    from .models import Location
                    record.known_locations[person.id]=Location(**location)
                    record.location_turns[person.id]=fact.turn
                person.active_until=max(person.active_until,self.world.turn+6)
            return
        if fact.kind in ('PersonLocated','SuspectLocated','CharacterFled','SearchClueShared') and fact.location:
            for record in self.raw_known_active(person):
                if record.suspect_id==(fact.actor_id if fact.kind=='CharacterFled' else fact.context.get('subject') if fact.kind=='SearchClueShared' else fact.target_id) and fact.context.get('observed_at',fact.turn)>=record.location_turns.get(person.id,-1):
                    from .models import Location
                    record.known_locations[person.id]=Location(**fact.context['new_location']) if fact.kind=='CharacterFled' else fact.location
                    record.location_turns[person.id]=fact.context.get('observed_at',fact.turn)
            return
        if fact.kind not in CRIMES or fact.actor_id in (None,person.id) or not fact.location:
            return
        suspect=self.world.characters.get(fact.actor_id)
        if not suspect or fact.location.map_id!=person.town_id:
            return
        # Força legal não vira crime automaticamente: exige fato conhecido
        # anterior contra o alvo, ou agressão observada como autodefesa.
        if fact.context.get('lawful') or fact.context.get('self_defense'):
            return
        key=person.town_id,suspect.id
        record=self.world.wanted_records.get(self.active.get(key))
        if record:
            record.severity=max(record.severity,self.severity(person,fact))
            record.confidence=max(record.confidence,fact.confidence)
            if fact.turn>=record.created_at:record.last_known_location=fact.location
            if person.id not in record.known_by:record.known_by.append(person.id)
        else:
            record=WantedRecord(self.world.allocate_id(),suspect.id,person.town_id,fact.event_id,
                self.severity(person,fact),fact.confidence,self.world.turn,fact.location,[person.id])
            record.known_locations[person.id]=fact.location
            record.location_turns[person.id]=fact.turn
            self.world.wanted_records[record.id]=record
            heapq.heappush(self.expiries,(record.created_at+self.duration(record)+1,record.id))
            self.active[key]=record.id
            self.active_cases[key].add(record.id)
            # O aviso usa cidade como alvo: não dá informação a suspeito remoto.
            witnesses=self.engine.spatial.at(person.position)
            self.engine.recorder.emit('WantedIssued',f'{person.name} registrou procura por {suspect.name}.',
                person.id,person.town_id,person.position,witnesses=witnesses,
                context={'record_id':record.id,'suspect_id':suspect.id,'source_fact':fact.event_id,
                         'severity':record.severity,'confidence':fact.confidence,
                         'last_known_location':vars(fact.location)})
        if record.institutional_fact is None or CRIMES[fact.kind]>CRIMES.get(record.institutional_fact.kind,0):
            record.institutional_fact=replace(fact,context=dict(fact.context))
            record.institutional_available_at=self.world.turn+AGENCY.institutional_latency
        if person.id not in record.assignments and len(record.assignments)<min(AGENCY.maximum_case_guards,1+record.severity//2):
            record.assignments[person.id]=('search','watch','inquire')[len(record.assignments)]
        self.by_guard[person.id].add(record.id)
        record.known_status[person.id]='active'
        record.known_facts[person.id]=fact.event_id
        record.known_severity[person.id]=max(record.known_severity.get(person.id,0),self.severity(person,fact))
        if fact.turn>=record.location_turns.get(person.id,-1):
            record.known_locations[person.id]=fact.location
            record.location_turns[person.id]=fact.turn
        person.active_until=max(person.active_until,self.world.turn+6)

    def raw_known_active(self, person):
        if person.profession!='guarda':return []
        return [self.world.wanted_records[i] for i in sorted(self.by_guard.get(person.id,()))
                if self.world.wanted_records[i].known_status.get(person.id,'active')=='active'
                and self.world.wanted_records[i].jurisdiction==person.town_id
                and self.world.turn-self.world.wanted_records[i].created_at<=self.duration(self.world.wanted_records[i],person.id)]

    def known_active(self, person):
        # Uma pressão por suspeito, escolhida pela gravidade que este guarda
        # conhece. Um caso antigo desconhecidamente encerrado pode coexistir
        # com outro recente; não deve substituir a evidência mais grave.
        selected={}
        def rank(record):
            return (record.known_severity.get(person.id,1),
                    record.location_turns.get(person.id,-1),record.created_at,record.id)
        for record in self.raw_known_active(person):
            previous=selected.get(record.suspect_id)
            if previous is None or rank(record)>rank(previous):
                selected[record.suspect_id]=record
        return [selected[i] for i in sorted(selected)]

    def resolve_known(self, person, suspect_id, status):
        for record in self.raw_known_active(person):
            if record.suspect_id!=suspect_id:continue
            record.known_status[person.id]=status
            self.by_guard[person.id].discard(record.id)
            self.close_global(record,status)

    def close_global(self, record, status):
        if record.status!='active':return
        record.status,record.resolved_at=status,self.world.turn
        key=record.jurisdiction,record.suspect_id
        remaining=self.active_cases[key]
        remaining.discard(record.id)
        if self.active.get(key)==record.id:
            if remaining:self.active[key]=max(remaining)
            else:self.active.pop(key,None)
        if not remaining:self.active_cases.pop(key,None)

    def record_for(self, guard, suspect_id):
        return next((r for r in self.known_active(guard) if r.suspect_id==suspect_id),None)

    def refresh(self, person):
        if person.combat.detention_until>self.world.turn:
            return
        for record in self.known_active(person):
            if record.assignments and person.id not in record.assignments:continue
            if self.world.turn-record.created_at>self.duration(record,person.id):
                continue
            source=record.known_facts.get(person.id,record.originating_fact)
            key=f'pursuit:{record.suspect_id}'
            previous=person.needs.get(key)
            if previous and previous.context.get('record_id')!=record.id:
                self.engine.needs.finish(person,previous,'expired')
            need=self.engine.needs.ensure(person,key,65+record.known_severity.get(person.id,1)*3,
                f'event:{source}','Localizar pessoa procurada com evidência conhecida',record.suspect_id)
            location=record.known_locations.get(person.id)
            own_locations=[r for r in self.raw_known_active(person)
                           if r.suspect_id==record.suspect_id and person.id in r.known_locations]
            freshest=max(own_locations,key=lambda r:r.location_turns.get(person.id,-1),default=None)
            if freshest and freshest.location_turns.get(person.id,-1)>record.location_turns.get(person.id,-1):
                location=freshest.known_locations[person.id]
                record.known_locations[person.id]=location
                record.location_turns[person.id]=freshest.location_turns[person.id]
            if location is None:continue
            observed=person.observations.get(record.suspect_id)
            if observed and observed.alive and observed.turn>record.location_turns.get(person.id,-1):
                location=observed.position
                record.known_locations[person.id]=location
                record.location_turns[person.id]=observed.turn
            if need.context.get('known_location')!=vars(location):
                need.context['search_attempts']=0
            need.context.update(institutional_role=record.assignments.get(person.id,'search'),record_id=record.id,known_location=vars(location),
                                source_event=source,originating_fact=record.originating_fact,severity=record.known_severity.get(person.id,1))
            need.expires_at=max(need.expires_at or 0,record.created_at+self.duration(record,person.id))
        for need in person.needs.values():
            if need.kind=='pursuit' and need.status not in FINISHED:
                record=self.world.wanted_records.get(need.context.get('record_id'))
                known_status=record.known_status.get(person.id) if record else None
                if known_status in ('captured','resolved','dead'):
                    need.context['resolution']='known_institutional_case_closed'
                    self.engine.needs.finish(person,need)
                elif (known_status!='active' or self.world.turn>record.created_at+self.duration(record,person.id)
                      or need.expires_at is not None and self.world.turn>need.expires_at):
                    self.engine.needs.finish(person,need,'expired')

    def capture(self, guard, suspect):
        record=self.record_for(guard,suspect.id)
        if (not record or not suspect.alive or guard.position!=suspect.position or
                suspect.combat.detention_until>self.world.turn):
            return False,'Faltam evidência local, presença ou autoridade válida.'
        if suspect.combat.surrendered_until<=self.world.turn and suspect.health>INTERACTION.incapacity_health:
            return False,'O suspeito não se rendeu nem está incapacitado.'
        fine=min(5,suspect.money)
        suspect.money-=fine;self.world.towns[record.jurisdiction].money+=fine
        suspect.combat.detention_until=self.world.turn+INTERACTION.detention_hours
        suspect.combat.captor_id=guard.id
        self.resolve_known(guard,suspect.id,'captured')
        self.engine.conflicts.end(suspect,'capture',guard)
        self.engine.recorder.emit('CharacterCaptured',f'{guard.name} deteve {suspect.name} e cobrou {fine} moedas.',
            guard.id,suspect.id,guard.position,historical=True,
            context={'record_id':record.id,'fine':fine,'release_at':suspect.combat.detention_until,
                     'source_fact':record.originating_fact})
        return True,'Captura e detenção temporária registradas.'

    def tick(self):
        if self.world.turn % AGENCY.institutional_latency == 0:self.communicate()
        while self.expiries and self.expiries[0][0]<=self.world.turn:
            _,record_id=heapq.heappop(self.expiries)
            record=self.world.wanted_records[record_id]
            if self.world.turn<=record.created_at+self.duration(record):
                heapq.heappush(self.expiries,(record.created_at+self.duration(record)+1,record.id));continue
            for i in record.known_by:self.by_guard[i].discard(record.id)
            if record.status=='active':
                self.close_global(record,'expired')
                self.engine.recorder.emit('PursuitEnded','Uma procura local terminou sem captura.',
                    target_id=record.jurisdiction,context={'record_id':record.id,'suspect_id':record.suspect_id,
                    'reason':'evidence_expired'},witnesses=[])
        for person in self.world.characters.values():
            state=person.combat
            if person.alive and state.captor_id is not None and state.detention_until<=self.world.turn:
                captor=state.captor_id;state.captor_id=None
                self.engine.recorder.emit('CharacterReleased',f'{person.name} foi liberado da detenção temporária.',
                    captor,person.id,person.position,context={'detention_ended':True})

    @staticmethod
    def severity(person, fact):
        value=CRIMES[fact.kind]
        observed=person.observations.get(fact.target_id)
        authority=fact.target_id==person.id or fact.context.get("victim_profession")=="guarda" or observed and observed.profession=="guarda"
        return min(5,value+1) if fact.kind=="CharacterAttacked" and authority else value

    @staticmethod
    def duration(record, guard_id=None):
        severity=record.known_severity.get(guard_id,1) if guard_id else record.severity
        return INTERACTION.maximum_pursuit_hours*(1+severity//2)

    def submit_clue(self,guard,fact):
        """Somente informação aprendida, caso próprio e depósito presencial local."""
        if guard.position!=self.world.towns[guard.town_id].market:return
        for record in self.raw_known_active(guard):
            subject=fact.context.get('subject') if fact.kind=='SearchClueShared' else fact.actor_id if fact.kind=='CharacterFled' else fact.target_id
            if record.suspect_id!=subject:continue
            old=record.institutional_clue
            if old and old.context.get('observed_at',old.turn)>=fact.context.get('observed_at',fact.turn):continue
            record.institutional_clue=replace(fact,context=dict(fact.context))
            record.clue_available_at=self.world.turn+AGENCY.institutional_latency
            self.engine.recorder.emit('InstitutionalClueFiled',f'{guard.name} registrou uma pista no serviço local.',
                guard.id,record.jurisdiction,guard.position,witnesses=[guard.id],historical=True,
                context={'record_id':record.id,'source_fact':fact.event_id,'available_at':record.clue_available_at})

    def communicate(self):
        """Canal de serviço local: latência, presença e até três tarefas por caso."""
        for record in self.world.wanted_records.values():
            if (record.institutional_fact is None or record.institutional_available_at>self.world.turn
                    or self.world.turn>record.created_at+self.duration(record)):
                continue
            town=self.world.towns[record.jurisdiction]
            guards=[self.world.characters[i] for i in self.engine.spatial.at(town.market)
                    if self.world.characters[i].profession=='guarda' and self.world.characters[i].town_id==town.id]
            limit=min(AGENCY.maximum_case_guards,1+record.severity//2)
            for guard in guards:
                if record.status!='active':
                    if guard.id in record.known_by and record.known_status.get(guard.id)=='active':
                        record.known_status[guard.id]=record.status;self.by_guard[guard.id].discard(record.id)
                    continue
                if guard.id not in record.assignments and len(record.assignments)>=limit:continue
                fact=replace(record.institutional_fact,source_kind='known',source_id=None,
                             confidence=min(60,record.institutional_fact.confidence))
                if record.institutional_clue and record.clue_available_at<=self.world.turn:
                    clue=replace(record.institutional_clue,source_kind='known',source_id=None,
                                 confidence=min(60,record.institutional_clue.confidence))
                    if self.engine.knowledge.learn(guard,clue,False):
                        self.engine.recorder.emit('InstitutionalClueShared',f'{guard.name} recebeu uma pista pelo serviço local.',
                            guard.id,town.id,guard.position,witnesses=[guard.id],historical=True,
                            context={'record_id':record.id,'source_fact':clue.event_id,'latency':AGENCY.institutional_latency})
                if self.engine.knowledge.learn(guard,fact,False):
                    self.engine.recorder.emit('InstitutionalCaseShared',f'{guard.name} recebeu um caso pelo serviço local.',
                        guard.id,town.id,guard.position,witnesses=[guard.id],historical=True,
                        context={'record_id':record.id,'source_fact':fact.event_id,'severity':record.severity,
                                 'role':record.assignments.get(guard.id),'latency':AGENCY.institutional_latency})
