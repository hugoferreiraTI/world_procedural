"""Deslocamento individual por rotas conhecidas, visita e residência separadas."""
import math

from .models import Location, MigrationState
from .navigation import distance
from .needs import FINISHED


class MigrationSystem:
    def __init__(self, engine):
        self.engine,self.world=engine,engine.world

    def learn_town(self, person, town_id, fact=None):
        if town_id not in self.world.towns:return
        town=self.world.towns[town_id]
        person.known_towns[town_id]={'position':vars(town.position),'learned_at':self.world.turn,
            'source_fact':fact.event_id if fact else None,'source':'witnessed_location' if fact else 'visited',
            'confidence':fact.confidence if fact else 100}

    def on_fact(self, person, fact):
        if fact.confidence<60:return
        if fact.kind in ('PersonLocated','TownOpportunityKnown','ResidentMoved'):
            town_id=fact.context.get('town_id') or (fact.location.map_id if fact.location else None)
            self.learn_town(person,town_id,fact)

    def destination(self, person):
        choices=[]
        origin=self.world.towns[person.town_id]
        for town_id,known in person.known_towns.items():
            if town_id==person.town_id or known.get('confidence',0)<60:continue
            location=Location(**known['position'])
            travel=distance(origin.position,location)+8
            if travel>100:continue
            choices.append((travel-10*bool(known.get('family'))-6*bool(known.get('work')),town_id,travel))
        return min(choices) if choices else None

    def refresh(self, person):
        if person.is_player:return
        if person.migration:
            state=person.migration
            if state.arrived_at is not None:
                if self.world.turn-state.arrived_at>=24:self.settle(person)
                return
            need=self.engine.needs.ensure(person,'migration',75 if state.reason=='wanted' else 50,
                'migration','Continuar viagem individual decidida',state.destination_id)
            need.context.update(reason=state.reason,travel_hours=self.remaining(person),destination=state.destination_id)
            return
        if person.personal_cooldowns.get('migration',0)>self.world.turn:
            self.engine.needs.satisfy(person,'migration');return
        resolved={f.context.get('record_id') for f in person.knowledge.values()
                  if f.kind in ('GuardResponded','CharacterCaptured') and f.target_id==person.id}
        wanted=any(f.kind=='WantedIssued' and f.context.get('suspect_id')==person.id and self.world.turn-f.turn<168
                   and f.context.get('record_id') not in resolved
                   for f in person.knowledge.values())
        threat=any(n.kind in ('protection','response') and n.status not in FINISHED for n in person.needs.values())
        poverty=person.financial_since is not None and self.world.turn-person.financial_since>=168
        known_family=any(k.get('family') for i,k in person.known_towns.items() if i!=person.town_id)
        if not (wanted or threat or poverty or known_family):
            self.engine.needs.satisfy(person,'migration');return
        destination=self.destination(person)
        if destination is None:return
        _,town_id,travel=destination
        reason='wanted' if wanted else 'threat' if threat else 'poverty' if poverty else 'family'
        urgency=62 if wanted else 52 if threat else 35
        need=self.engine.needs.ensure(person,'migration',urgency,'known_towns',
            'Considerar mudança por '+reason,town_id)
        need.context.update(reason=reason,destination=town_id,travel_hours=travel)

    def remaining(self, person):
        state=person.migration
        if not state:return 0
        target=self.world.towns[state.destination_id]
        if person.position.map_id==target.id:return distance(person.position,target.market)
        if person.position.map_id==self.world.world_map_id:return distance(person.position,target.position)+3
        grid=self.world.maps[person.position.map_id]
        if not grid.exit_to:return 1000
        gate=Location(grid.id,grid.width//2,grid.height-1)
        return distance(person.position,gate)+1+distance(grid.exit_to,target.position)+3

    def supplies(self, person, hours):
        food=min(6,max(2,math.ceil((person.hunger+2*(hours+6))/40)))
        water=min(6,max(1,math.ceil(max(0,person.thirst+2*(hours+6)-50)/45)))
        return food,water

    def execute(self, person, destination_id, need=None):
        if not person.alive or person.combat.detention_until>self.world.turn or person.combat.surrendered_until>self.world.turn:
            return False,'A condição atual impede esta viagem.'
        if not person.migration:
            known=person.known_towns.get(destination_id)
            if not known or known.get('confidence',0)<60 or destination_id==person.town_id:
                return False,'Não existe destino diferente conhecido com confiança suficiente.'
            origin=self.world.towns[person.town_id]
            hours=distance(origin.position,Location(**known['position']))+8
            food,water=self.supplies(person,hours)
            if self.engine.items.count(person.id,'food')<food or self.engine.items.count(person.id,'water')<water:
                return False,'A reserva conhecida ainda não cobre a viagem.'
            reason=need.context.get('reason','individual') if need else 'player'
            person.migration=MigrationState(destination_id,person.town_id,reason,self.world.turn)
            self.engine.conflicts.end(person,'departure')
            self.engine.recorder.emit('MigrationStarted',f'{person.name} iniciou viagem para uma localidade conhecida.',
                person.id,destination_id,person.position,historical=True,
                context={'origin':person.town_id,'destination':destination_id,'reason':reason,'estimated_hours':hours})
        state=person.migration
        if state.arrived_at is not None:return False,'A visita está em andamento antes da mudança de residência.'
        target=self.world.towns[state.destination_id]
        if person.position.map_id==target.id:
            self.engine.navigation.approach(person,target.market,1)
            if person.position==target.market:
                state.arrived_at=self.world.turn
                self.learn_town(person,target.id)
                self.engine.recorder.emit('MigrationArrived',f'{person.name} chegou como visitante a {target.name}.',
                    person.id,target.id,person.position,historical=True,
                    context={'origin':state.origin_id,'reason':state.reason,'travel_hours':self.world.turn-state.started_at})
                if need:self.engine.needs.finish(person,need)
        elif person.position.map_id==self.world.world_map_id:
            if person.position==target.position:self.engine.navigation.enter(person)
            else:self.engine.navigation.approach(person,target.position,1)
        else:
            grid=self.world.maps[person.position.map_id]
            if not grid.exit_to:return False,'O local não possui saída acessível.'
            gate=Location(grid.id,grid.width//2,grid.height-1)
            if person.position==gate:self.engine.navigation.leave(person)
            else:self.engine.navigation.approach(person,gate,1)
        person.active_until=max(person.active_until,self.world.turn+2)
        return True,'Uma etapa física da viagem foi realizada.'

    def settle(self, person):
        state=person.migration
        if not state or state.arrived_at is None or person.position.map_id!=state.destination_id:return False
        origin,target=self.world.towns[state.origin_id],self.world.towns[state.destination_id]
        if person.id not in origin.resident_ids or person.id in target.resident_ids:return False
        origin.resident_ids.remove(person.id);target.resident_ids.append(person.id)
        origin.population-=1;target.population+=1
        person.town_id=target.id
        person.home=Location(target.id,2,2)
        person.workplace=(Location(target.id,self.world.maps[target.id].width-3,2)
                          if person.profession in ('mineiro','ferreiro','lenhador') else
                          Location(target.id,1,self.world.maps[target.id].height-2)
                          if person.profession in ('agricultor','caçador') else target.market)
        person.known_places.update(home=person.home,work=person.workplace,well_home=person.home)
        person.faction=target.kingdom_id
        self.engine.graph.set(person.id,target.id,'reside_em',100)
        self.engine.recorder.emit('ResidentMoved',f'{person.name} estabeleceu residência em {target.name}.',
            person.id,target.id,person.position,historical=True,
            context={'origin':origin.id,'town_id':target.id,'reason':state.reason,
                     'duration':self.world.turn-state.started_at})
        person.migration=None
        person.personal_cooldowns['migration']=self.world.turn+336
        if person.money<10:person.financial_since=self.world.turn
        person.financial_setbacks=0
        self.engine.needs.satisfy(person,'migration')
        return True

    def candidates(self, person, need):
        if person.combat.detention_until>self.world.turn or person.combat.surrendered_until>self.world.turn:return []
        if need.kind!='migration':return []
        if person.migration:return [('migrate',None,person.migration.destination_id)]
        destination=need.target_id
        hours=need.context.get('travel_hours',0)
        food,water=self.supplies(person,hours)
        choices=[]
        if self.engine.items.count(person.id,'food')<food:
            market=person.known_places.get('market')
            if market and self.engine.economy.can_seek_food(person):choices.append(('buy_food',market,None))
            forage=person.known_places.get('forage')
            if forage:choices.append(('forage',forage,None))
        elif self.engine.items.count(person.id,'water')<water:
            for key in ('well_home','well_rural','market'):
                if key in person.known_places:choices.append(('fill_water',person.known_places[key],None))
        else:choices.append(('migrate',None,destination))
        return choices
