"""Evidência conhecida por autoridades locais; não é um rastreador global."""
from collections import defaultdict
import heapq

from .models import WantedRecord
from .rules import INTERACTION
from .needs import FINISHED

CRIMES = {'ItemStolen':1, 'CharacterThreatened':2, 'CharacterAttacked':3, 'CharacterKilled':5}


class JusticeSystem:
    def __init__(self, engine):
        self.engine,self.world = engine,engine.world
        self.by_guard=defaultdict(set)
        self.active={}
        self.expiries=[]
        for record in self.world.wanted_records.values():
            if self.world.turn-record.created_at<=INTERACTION.maximum_pursuit_hours:
                heapq.heappush(self.expiries,(record.created_at+INTERACTION.maximum_pursuit_hours+1,record.id))
                for i in record.known_by:
                    if record.known_status.get(i,'active')=='active':self.by_guard[i].add(record.id)
                if record.status=='active':self.active[record.jurisdiction,record.suspect_id]=record.id

    def on_fact(self, person, fact):
        if person.profession!='guarda' or fact.confidence<INTERACTION.warrant_confidence:
            return
        if fact.kind in ('CharacterCaptured','CharacterKilled','CharacterDied','GuardResponded'):
            for record in self.known_active(person):
                if record.suspect_id==fact.target_id:
                    record.known_status[person.id]='captured' if fact.kind=='CharacterCaptured' else 'resolved' if fact.kind=='GuardResponded' else 'dead'
                    self.by_guard[person.id].discard(record.id)
            return
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
        if fact.kind in ('PersonLocated','SuspectLocated','CharacterFled') and fact.location:
            for record in self.known_active(person):
                if record.suspect_id==(fact.actor_id if fact.kind=='CharacterFled' else fact.target_id) and fact.turn>=record.location_turns.get(person.id,-1):
                    from .models import Location
                    record.known_locations[person.id]=Location(**fact.context['new_location']) if fact.kind=='CharacterFled' else fact.location
                    record.location_turns[person.id]=fact.turn
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
            record.severity=max(record.severity,CRIMES[fact.kind])
            record.confidence=max(record.confidence,fact.confidence)
            if fact.turn>=record.created_at:record.last_known_location=fact.location
            if person.id not in record.known_by:record.known_by.append(person.id)
        else:
            record=WantedRecord(self.world.allocate_id(),suspect.id,person.town_id,fact.event_id,
                CRIMES[fact.kind],fact.confidence,self.world.turn,fact.location,[person.id])
            record.known_locations[person.id]=fact.location
            record.location_turns[person.id]=fact.turn
            self.world.wanted_records[record.id]=record
            heapq.heappush(self.expiries,(record.created_at+INTERACTION.maximum_pursuit_hours+1,record.id))
            self.active[key]=record.id
            # O aviso usa cidade como alvo: não dá informação a suspeito remoto.
            witnesses=self.engine.spatial.at(person.position)
            self.engine.recorder.emit('WantedIssued',f'{person.name} registrou procura por {suspect.name}.',
                person.id,person.town_id,person.position,witnesses=witnesses,
                context={'record_id':record.id,'suspect_id':suspect.id,'source_fact':fact.event_id,
                         'severity':record.severity,'confidence':fact.confidence,
                         'last_known_location':vars(fact.location)})
        self.by_guard[person.id].add(record.id)
        record.known_status[person.id]='active'
        record.known_facts[person.id]=fact.event_id
        record.known_severity[person.id]=max(record.known_severity.get(person.id,0),CRIMES[fact.kind])
        if fact.turn>=record.location_turns.get(person.id,-1):
            record.known_locations[person.id]=fact.location
            record.location_turns[person.id]=fact.turn
        person.active_until=max(person.active_until,self.world.turn+6)

    def known_active(self, person):
        if person.profession!='guarda':return []
        return [self.world.wanted_records[i] for i in sorted(self.by_guard.get(person.id,()))
                if self.world.wanted_records[i].known_status.get(person.id,'active')=='active'
                and self.world.wanted_records[i].jurisdiction==person.town_id
                and self.world.turn-self.world.wanted_records[i].created_at<=INTERACTION.maximum_pursuit_hours]

    def record_for(self, guard, suspect_id):
        return next((r for r in self.known_active(guard) if r.suspect_id==suspect_id),None)

    def refresh(self, person):
        if person.combat.detention_until>self.world.turn:
            return
        for record in self.known_active(person):
            if self.world.turn-record.created_at>INTERACTION.maximum_pursuit_hours:
                continue
            source=record.known_facts.get(person.id,record.originating_fact)
            key=f'pursuit:{record.suspect_id}'
            previous=person.needs.get(key)
            if previous and previous.context.get('record_id')!=record.id:
                self.engine.needs.finish(person,previous,'expired')
            need=self.engine.needs.ensure(person,key,65+record.known_severity.get(person.id,1)*3,
                f'event:{source}','Localizar pessoa procurada com evidência conhecida',record.suspect_id)
            location=record.known_locations.get(person.id)
            if location is None:continue
            observed=person.observations.get(record.suspect_id)
            if observed and observed.alive and observed.turn>record.location_turns.get(person.id,-1):
                location=observed.position
                record.known_locations[person.id]=location
                record.location_turns[person.id]=observed.turn
            if need.context.get('known_location')!=vars(location):
                need.context['search_attempts']=0
            need.context.update(record_id=record.id,known_location=vars(location),
                                source_event=source,originating_fact=record.originating_fact,severity=record.known_severity.get(person.id,1))
            if need.expires_at is None:need.expires_at=record.created_at+INTERACTION.maximum_pursuit_hours
        for need in person.needs.values():
            if need.kind=='pursuit' and need.status not in FINISHED:
                record=self.world.wanted_records.get(need.context.get('record_id'))
                if not record or record.known_status.get(person.id,'active')!='active' or self.world.turn>need.expires_at:
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
        record.status,record.resolved_at='captured',self.world.turn
        self.active.pop((record.jurisdiction,record.suspect_id),None)
        self.engine.conflicts.end(suspect,'capture',guard)
        self.engine.recorder.emit('CharacterCaptured',f'{guard.name} deteve {suspect.name} e cobrou {fine} moedas.',
            guard.id,suspect.id,guard.position,historical=True,
            context={'record_id':record.id,'fine':fine,'release_at':suspect.combat.detention_until,
                     'source_fact':record.originating_fact})
        return True,'Captura e detenção temporária registradas.'

    def tick(self):
        while self.expiries and self.expiries[0][0]<=self.world.turn:
            _,record_id=heapq.heappop(self.expiries)
            record=self.world.wanted_records[record_id]
            for i in record.known_by:self.by_guard[i].discard(record.id)
            if record.status=='active':
                record.status,record.resolved_at='expired',self.world.turn
                if self.active.get((record.jurisdiction,record.suspect_id))==record.id:
                    self.active.pop((record.jurisdiction,record.suspect_id),None)
                self.engine.recorder.emit('PursuitEnded','Uma procura local terminou sem captura.',
                    target_id=record.jurisdiction,context={'record_id':record.id,'suspect_id':record.suspect_id,
                    'reason':'evidence_expired'},witnesses=[])
        for person in self.world.characters.values():
            state=person.combat
            if person.alive and state.captor_id is not None and state.detention_until<=self.world.turn:
                captor=state.captor_id;state.captor_id=None
                self.engine.recorder.emit('CharacterReleased',f'{person.name} foi liberado da detenção temporária.',
                    captor,person.id,person.position,context={'detention_ended':True})
