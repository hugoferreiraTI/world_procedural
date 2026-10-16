"""Vinte regressões compostas para causalidade, consequências e persistência."""
import unittest
from dataclasses import replace
from procedural.generation import GenerationConfig, generate_world
from procedural.engine import Engine
from procedural.models import Goal, Fact, Location, Personality
from procedural.persistence import dumps, loads
from procedural.validation import assert_valid, validate_world
from procedural.utility import evaluate


class Phase4Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.template=dumps(generate_world('Fase4',with_player=True,
                          config=GenerationConfig(kingdom_count=1,historical_turns=0,density_multiplier=4)))

    def setUp(self):
        self.world=loads(self.template);self.engine=Engine(self.world)
        self.a=next(c for c in self.world.characters.values() if c.profession=='agricultor')
        self.town=self.world.towns[self.a.town_id]
        self.b=next(c for c in self.world.characters.values() if c.profession=='cozinheiro' and c.town_id==self.town.id)
        self.guard=next(c for c in self.world.characters.values() if c.profession=='guarda' and c.town_id==self.town.id)
        self.remote=next(c for c in self.world.characters.values() if c.town_id!=self.town.id)
        for c in self.world.characters.values():self.engine.navigation.relocate(c,c.home)
        for c in (self.a,self.b,self.guard):
            self.engine.navigation.relocate(c,self.town.market)
            c.hunger=c.thirst=c.fatigue=0;c.money=100
            c.knowledge.clear();c.needs.clear();c.observations.clear();c.goal=None
        self.world.events.clear();self.world.history.clear()

    def action(self,who,action,target=None,need=None):
        goal=Goal(self.world.allocate_id(),need.id if need else 0,action,0,self.world.turn,target)
        return self.engine.goals.execute(who,goal,1)

    def fact(self,kind='CharacterAttacked',actor=None,target=None,context=None):
        return self.engine.recorder.emit(kind,'Cenário controlado',
            self.b.id if actor is None else actor,self.a.id if target is None else target,
            self.town.market,context=context or {})

    def test_01_real_damage_emotion_and_known_grievance(self):
        self.assertTrue(self.action(self.b,'attack',self.a.id)[0])
        self.assertLess(self.a.health,100);self.assertGreater(self.a.combat.injured,0)
        self.assertGreater(self.a.emotions.anger,0)
        g=self.a.grievances[self.b.id]
        self.assertIn(g.source_fact,self.a.knowledge)
        self.assertFalse(self.remote.grievances)
        self.assertNotIn(g.source_fact,self.remote.knowledge)

    def test_02_death_census_body_items_and_dead_no_action(self):
        original=self.town.population;inventory=dict(self.a.inventory)
        self.a.health=1
        self.action(self.b,'attack',self.a.id)
        self.assertFalse(self.a.alive);self.assertEqual(original-1,self.town.population)
        self.assertEqual(inventory,self.a.inventory)
        self.assertFalse(self.action(self.a,'attack',self.b.id)[0])
        self.assertFalse(self.engine.finish_death(self.a,'combat',self.b))
        self.assertEqual(original-1,self.town.population)
        self.assertEqual('combat',self.world.death_records[self.a.id]['cause'])
        assert_valid(self.world)
        kingdom=self.world.kingdoms[self.town.kingdom_id]
        ruler=self.world.characters[kingdom.ruler_id]
        heir=kingdom.heir_id
        self.engine.navigation.relocate(ruler,self.b.position);ruler.health=1
        self.action(self.b,'attack',ruler.id)
        self.assertEqual(heir,kingdom.ruler_id)
        self.assertTrue(any(e.kind=='SuccessionChanged' for e in self.world.history))

    def test_03_observed_death_grief_revenge_unknown_killer(self):
        self.engine.graph.set(self.guard.id,self.a.id,'amizade',90,reciprocal=True)
        self.a.health=1;self.action(self.b,'attack',self.a.id)
        self.assertTrue(any(n.kind=='grief' for n in self.guard.needs.values()))
        self.assertTrue(any(n.kind=='revenge' and n.target_id==self.b.id for n in self.guard.needs.values()))
        fact=Fact(self.world.allocate_id(),'RemainsLocated',self.remote.id,self.a.id,self.town.market,
                  self.world.turn,'Restos encontrados sem autoria conhecida',context={'cause':'unknown'})
        self.engine.graph.set(self.remote.id,self.a.id,'amizade',90)
        self.engine.knowledge.learn(self.remote,fact,True)
        self.assertFalse(any(n.kind=='revenge' and n.target_id==self.b.id for n in self.remote.needs.values()))

    def test_04_defense_and_intervention_redirect_damage(self):
        self.fact()
        need=next(n for n in self.guard.needs.values() if n.kind=='protection')
        self.assertTrue(self.action(self.guard,'protect',self.b.id,need)[0])
        before=self.a.health
        self.action(self.b,'attack',self.a.id)
        self.assertEqual(before,self.a.health);self.assertLess(self.guard.health,100)
        self.assertIn(self.b.id,self.guard.combat.opponents)

    def test_05_flee_physical_and_surrender_stops_attack(self):
        self.action(self.b,'attack',self.a.id)
        old=self.a.position
        self.assertTrue(self.action(self.a,'withdraw',self.b.id)[0])
        self.assertNotEqual(old,self.a.position);self.assertFalse(self.a.combat.opponents)
        self.engine.navigation.relocate(self.a,self.b.position)
        self.world.turn=49;self.a.combat.truces.clear();self.b.combat.truces.clear()
        self.assertTrue(self.action(self.a,'surrender',self.b.id)[0])
        hp=self.a.health;self.assertFalse(self.action(self.b,'attack',self.a.id)[0]);self.assertEqual(hp,self.a.health)

    def test_06_theft_options_personality_and_nonviolent_choice(self):
        self.fact('ItemStolen',context={'item_kind':'food'})
        need=next(n for n in self.a.needs.values() if n.kind=='revenge')
        self.engine.conflicts.observe(self.a)
        self.a.emotions.anger=90;self.a.emotions.resentment=75
        self.a.personality=Personality(courage=95,vengefulness=95,compassion=0)
        choices=self.engine.goals.solutions(self.a,need)
        self.assertIn('attack',[c.action for c in choices]);self.assertIn('confront',[c.action for c in choices])
        self.a.personality=Personality(courage=5,vengefulness=5,compassion=95,honesty=95)
        choices=self.engine.goals.solutions(self.a,need)
        self.assertNotIn('attack',[c.action for c in choices])
        self.assertIn('denounce',[c.action for c in choices])
        self.assertNotEqual('attack',choices[0].action)

    def test_07_evidence_guard_vs_uninformed_and_no_remote_tracking(self):
        event=self.fact('ItemStolen')
        record=self.engine.justice.record_for(self.guard,self.b.id)
        self.assertIsNotNone(record);self.assertIsNone(self.engine.justice.record_for(self.remote,self.b.id))
        old=record.known_locations[self.guard.id]
        self.engine.navigation.relocate(self.b,self.b.home)
        self.engine.needs.refresh(self.guard)
        pursuit=next(n for n in self.guard.needs.values() if n.kind=='pursuit')
        self.assertEqual(vars(old),pursuit.context['known_location'])
        self.assertNotEqual(vars(self.b.position),pursuit.context['known_location'])
        self.assertEqual(event.id,record.originating_fact)

    def test_08_capture_fine_detention_release_and_movement_block(self):
        self.fact('ItemStolen')
        self.action(self.b,'surrender',self.guard.id)
        money=self.b.money;treasury=self.town.money
        self.assertTrue(self.action(self.guard,'capture',self.b.id)[0])
        self.assertEqual(money-5,self.b.money);self.assertEqual(treasury+5,self.town.money)
        old=self.b.position;self.engine.navigation.approach(self.b,self.b.home,3)
        self.assertEqual(old,self.b.position)
        self.assertFalse(self.action(self.b,'attack',self.guard.id)[0])
        self.world.turn=12;self.engine.justice.tick()
        self.assertIsNone(self.b.combat.captor_id)
        self.assertTrue(any(e.kind=='CharacterReleased' for e in self.world.events))

    def test_09_restitution_is_agent_choice_real_item_and_no_magic(self):
        self.action(self.b,'steal',need=None)
        stolen=next(f for f in self.b.knowledge.values() if f.kind=='ItemStolen')
        stock=self.engine.items.count(self.town.id,'food')
        self.fact('RestitutionDemanded',actor=self.a.id,target=self.b.id,context={'source_fact':stolen.event_id})
        self.assertEqual(stock,self.engine.items.count(self.town.id,'food'))
        need=next(n for n in self.b.needs.values() if n.kind=='response' and n.target_id==self.a.id)
        self.assertIn('return_stolen',[a for a,_,_ in self.engine.conflicts.candidates(self.b,need)])
        self.assertTrue(self.action(self.b,'return_stolen',self.a.id,need)[0])
        self.assertEqual(stock+1,self.engine.items.count(self.town.id,'food'))

    def test_10_repair_decay_bounded_personality_and_confidence_dedup(self):
        event=self.fact('CharacterInsulted')
        original=replace(self.a.personality);anger=self.a.emotions.anger
        self.engine.emotions.on_fact(self.a,self.a.knowledge[event.id])
        self.assertEqual(anger,self.a.emotions.anger)
        self.a.emotions.processed.clear()
        self.engine.emotions.on_fact(self.a,self.a.knowledge[event.id])
        self.assertEqual(anger,self.a.emotions.anger)
        self.assertEqual(original,self.a.personality)
        self.action(self.b,'apologize',self.a.id)
        self.assertLess(self.a.emotions.anger,anger)
        self.a.emotions.anger=50;self.world.turn=24;self.engine.emotions.update(self.a)
        self.assertLess(self.a.emotions.anger,50)
        self.a.emotions.strain=720;self.a.emotions.desperation=100
        self.world.turn=744;self.engine.emotions.update(self.a)
        self.assertLessEqual(self.a.personality.vengefulness-original.vengefulness,1)

    def test_11_first_aid_resources_and_wound_rehabilitation(self):
        self.a.combat.injured=30;self.a.health=65
        self.assertFalse(self.action(self.b,'first_aid',self.a.id)[0])
        self.engine.items.create(self.b.id,'water',1)
        food=self.engine.items.count(self.b.id,'food')
        self.assertTrue(self.action(self.b,'first_aid',self.a.id)[0])
        self.assertEqual(24,self.a.combat.injured)
        self.assertEqual(food-1,self.engine.items.count(self.b.id,'food'))
        self.assertEqual(0,self.engine.items.count(self.b.id,'water'))
        self.engine.needs.rest(self.a,2);self.assertEqual(20,self.a.combat.injured)

    def test_12_help_request_creates_need_not_automatic_action(self):
        self.a.combat.injured=30
        self.action(self.a,'call_help',self.b.id)
        self.assertEqual(30,self.a.combat.injured)
        need=next(n for n in self.b.needs.values() if n.kind=='assistance')
        self.engine.items.create(self.b.id,'water',1)
        self.assertIn('first_aid',[a for a,_,_ in self.engine.conflicts.candidates(self.b,need)])

    def test_13_migration_real_route_visit_then_census(self):
        destination=next(i for i in self.a.known_towns if i!=self.town.id)
        target=self.world.towns[destination];before=(self.town.population,target.population)
        self.engine.items.create(self.a.id,'food',6);self.engine.items.create(self.a.id,'water',6)
        self.assertTrue(self.engine.migration.execute(self.a,destination)[0])
        self.assertEqual(self.town.id,self.a.town_id)
        for _ in range(180):
            self.world.turn+=1;self.engine.migration.execute(self.a,destination)
            if self.a.migration.arrived_at is not None:break
        self.assertEqual(destination,self.a.position.map_id);self.assertIsNotNone(self.a.migration.arrived_at)
        self.assertEqual(before,(self.town.population,target.population))
        self.world.turn+=24;self.assertTrue(self.engine.migration.settle(self.a))
        self.assertEqual(destination,self.a.town_id)
        self.assertEqual((before[0]-1,before[1]+1),(self.town.population,target.population))
        self.assertNotIn(self.a.id,self.town.resident_ids);assert_valid(self.world)

    def test_14_unknown_destination_no_travel_and_visitor_local_trade(self):
        self.a.known_towns.clear()
        self.assertFalse(self.engine.migration.execute(self.a,self.remote.town_id)[0])
        self.engine.navigation.relocate(self.a,self.world.towns[self.remote.town_id].position)
        self.engine.navigation.enter(self.a)
        host=self.world.towns[self.remote.town_id]
        self.engine.navigation.relocate(self.a,host.market)
        self.assertNotEqual(host.id,self.a.town_id)
        self.engine.economy.observe(self.a)
        self.assertEqual(host.id,self.a.market_observation['town_id'])
        self.assertTrue(self.action(self.a,'buy_food')[0])

    def test_15_population_balance_geography_identity(self):
        a=generate_world('Mira',with_player=False,config=GenerationConfig(historical_turns=0,density_multiplier=1))
        b=generate_world('Mira',with_player=False,config=GenerationConfig(historical_turns=0))
        self.assertGreater(len(b.characters),1200);self.assertLess(len(b.characters),2400)
        self.assertEqual(len(a.towns),len(b.towns))
        for t in b.towns.values():
            expected=104 if t.capital else 60 if t.kind=='cidade' else 18
            self.assertEqual(expected,len(t.resident_ids))
        self.assertEqual({i:t.position for i,t in a.towns.items()},{i:t.position for i,t in b.towns.items()})
        self.assertEqual(a.maps,b.maps)
        self.assertEqual(len(a.kingdoms),len(b.kingdoms))
        for t in b.towns.values():self.assertTrue(2<=t.abstract_population/len(t.resident_ids)<=3)
        assert_valid(b)

    def test_16_save_load_and_short_deterministic_continuation(self):
        self.action(self.b,'attack',self.a.id)
        text=dumps(self.world);copy=loads(text)
        self.assertEqual(text,dumps(copy))
        self.assertTrue(copy.characters[self.a.id].combat.opponents)
        self.engine.simulate(12);Engine(copy).simulate(12)
        self.assertEqual(dumps(self.world),dumps(copy))

    def test_17_lod_promotes_event_and_keeps_hourly_physiology(self):
        self.a.position=self.a.home;self.engine.spatial.rebuild()
        self.assertEqual(12,self.engine.feeding.decision_interval(self.a))
        self.engine.navigation.relocate(self.a,self.town.market)
        self.fact('CharacterThreatened')
        self.assertEqual(1,self.engine.feeding.decision_interval(self.a))
        hunger=self.remote.hunger;self.engine.needs.physiology(self.remote)
        self.assertEqual(min(100,hunger+2),self.remote.hunger)

    def test_18_extreme_despair_support_and_invalid_state_rejection(self):
        self.world.turn=1000;self.a.emotions.desperation=100
        self.a.emotions.losses=[self.b.id,self.guard.id,self.remote.id]
        self.a.observations.clear();self.a.combat.opponents.clear()
        self.assertTrue(self.engine.conflicts.extreme_despair(self.a))
        self.engine.emotions.support(self.a,5)
        self.assertFalse(self.engine.conflicts.extreme_despair(self.a))
        self.a.emotions.anger=101;self.assertTrue(validate_world(self.world))

    def test_19_resolved_fine_is_not_repeated_and_migration_has_recovery_time(self):
        event=self.fact('ItemStolen')
        self.engine.needs.refresh(self.guard)
        need=self.guard.needs['security']
        pursuit=next(n for n in self.guard.needs.values() if n.kind=='pursuit')
        amount=self.b.money
        self.assertTrue(self.action(self.guard,'secure',self.b.id,need)[0])
        self.assertIsNone(self.engine.justice.record_for(self.guard,self.b.id))
        self.world.turn=6;self.engine.needs.refresh(self.guard)
        self.assertFalse(self.action(self.guard,'secure',self.b.id,need)[0])
        self.assertEqual(amount-5,self.b.money)
        self.fact('ItemStolen')
        self.engine.needs.refresh(self.guard)
        pursuits=[n for n in self.guard.needs.values() if n.kind=='pursuit']
        self.assertEqual(1,len(pursuits));self.assertEqual(pursuit.id,pursuits[0].id)
        # Dois guardas conhecem o roubo. Um se afasta e não aprende a captura;
        # ao voltar, testemunha uma agressão nova do mesmo suspeito.
        other=next(c for c in self.world.characters.values() if c.profession=='guarda'
                   and c.town_id==self.town.id and c.id!=self.guard.id)
        self.engine.navigation.relocate(other,self.town.market)
        self.fact('ItemStolen')
        old=self.engine.justice.record_for(self.guard,self.b.id)
        self.engine.navigation.relocate(self.guard,self.guard.home)
        self.b.combat.surrendered_until=self.world.turn+1
        self.assertTrue(self.action(other,'capture',self.b.id)[0])
        self.assertEqual('active',old.known_status[self.guard.id])
        self.b.combat.detention_until=0;self.b.combat.surrendered_until=0
        self.engine.navigation.relocate(self.guard,self.town.market)
        self.fact('CharacterAttacked')
        self.engine.needs.refresh(self.guard)
        selected=self.engine.justice.record_for(self.guard,self.b.id)
        self.assertEqual(3,selected.known_severity[self.guard.id])
        self.assertEqual(selected.id,self.guard.needs[f'pursuit:{self.b.id}'].context['record_id'])
        created=self.world.metrics['NeedCreated:pursuit']
        self.engine.needs.refresh(self.guard)
        self.assertEqual(created,self.world.metrics['NeedCreated:pursuit'])
        self.assertFalse(self.action(self.guard,'secure',self.b.id,need)[0])
        self.assertEqual('active',selected.status)
        # Um checkpoint da versão auditada pode conter outro caso global ativo
        # que este guarda já considera encerrado. Fechar o caso novo preserva
        # o índice do antigo, sem ensinar ao guarda evidência desconhecida.
        old.status='active';old.known_status[self.guard.id]='captured'
        old.known_status[other.id]='active'
        from procedural.justice import JusticeSystem
        self.engine.justice=JusticeSystem(self.engine)
        self.b.combat.surrendered_until=self.world.turn+1
        self.assertTrue(self.action(self.guard,'capture',self.b.id)[0])
        canonical={(r.jurisdiction,r.suspect_id):r.id for r in self.world.wanted_records.values()
                   if r.status=='active' and self.world.turn-r.created_at<=168}
        self.assertEqual(canonical,self.engine.justice.active)
        self.assertIsNone(self.engine.justice.record_for(self.guard,self.b.id))
        self.a.money=0;self.a.financial_since=0;self.world.turn=500
        self.a.personal_cooldowns['migration']=700
        self.engine.migration.refresh(self.a)
        self.assertFalse(any(n.kind=='migration' and n.status=='active' for n in self.a.needs.values()))

    def test_20_protector_cannot_intercept_own_attack_or_while_surrendered(self):
        self.b.combat.protected_by=[self.a.id]
        self.a.combat.defending_until=5
        hp=self.a.health
        self.assertTrue(self.action(self.a,'attack',self.b.id)[0])
        self.assertEqual(hp,self.a.health);self.assertNotIn(self.a.id,self.a.combat.opponents)
        self.a.combat.protected_by=[self.guard.id]
        self.guard.combat.defending_until=5;self.guard.combat.surrendered_until=5
        hp=self.guard.health
        self.action(self.b,'attack',self.a.id)
        self.assertEqual(hp,self.guard.health)
        assert_valid(self.world)

if __name__=='__main__':unittest.main()
