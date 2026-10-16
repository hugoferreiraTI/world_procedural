"""Contratos econômicos/populacionais e cenários A–G da fase 3."""
import unittest
from dataclasses import replace
from procedural.engine import Engine
from procedural.models import Goal, Location, Personality
from procedural.persistence import dumps,loads
from procedural.validation import assert_valid
from test_simulation import small_world


class Phase3Tests(unittest.TestCase):
    def setUp(self):
        self.world=small_world('Fase3',with_player=True)
        self.engine=Engine(self.world)
        self.town=self.world.towns[self.engine.player.town_id]
        self.people=[self.world.characters[i] for i in self.town.resident_ids]
        self.farmer=next(c for c in self.people if c.profession=='agricultor')
        self.cook=next(c for c in self.people if c.profession=='cozinheiro')
        self.stock('food',0); self.stock('grain',240)
        for c in self.people:
            c.hunger=c.thirst=c.fatigue=0; c.money=40
            c.personality=Personality(ambition=0,diligence=60)
        self.town.cooking_slots=8

    def stock(self,kind,amount):
        old=self.engine.items.count(self.town.id,kind)
        if old: self.engine.items.consume(self.town.id,kind,old)
        if amount: self.engine.items.create(self.town.id,kind,amount)

    def die(self,c):
        c.alive=False;c.health=0
        self.engine.spatial.positions[c.position].discard(c.id)
        return self.engine.recorder.emit('CharacterDied','Morte em cenário dirigido',target_id=c.id,location=c.position)

    def report(self):
        return self.engine.economy.food_diagnosis(self.town)

    def vacancy(self,age=96):
        self.world.turn=age
        self.town.professional_demand['cozinheiro']={'deficit':3,'required':4,'since':0,'stage':'training'}
        self.town.economic_report=self.report()

    def no_candidates(self):
        self.farmer.profession='estudante'
        for c in self.people:
            c.money=40;c.personality.ambition=0

    def test_food_shortage_with_low_grain_prefers_farming(self):
        self.stock('grain',10)
        self.engine.economy.daily()
        self.assertEqual(self.town.goal.action,'expand_farming')

    def test_food_shortage_with_full_grain_does_not_expand_farming(self):
        self.engine.economy.daily()
        self.assertNotEqual(self.town.goal.action,'expand_farming')

    def test_food_shortage_without_cook_creates_professional_demand(self):
        self.die(self.cook);self.engine.economy.daily()
        self.assertGreater(self.town.professional_demand['cozinheiro']['deficit'],0)
        self.assertIn('LABOR_SHORTAGE',self.town.economic_report['bottlenecks'])

    def test_cook_alive_but_insufficient_capacity_detects_capacity_deficit(self):
        self.town.population=6000
        self.town.abstract_population=6000-len(self.people)
        self.assertIn('PROCESSING_CAPACITY_SHORTAGE',self.report()['bottlenecks'])
        self.assertGreater(self.report()['professional_deficit'],0)

    def test_food_available_but_population_poor_detects_affordability_problem(self):
        self.stock('food',200);self.farmer.money=1
        self.engine.items.consume(self.farmer.id,'food',self.engine.items.count(self.farmer.id,'food'))
        self.assertIn('AFFORDABILITY_PROBLEM',self.report()['bottlenecks'])

    def food_choices(self,money):
        self.stock('food',1); self.farmer.money=money;self.farmer.hunger=70
        self.engine.items.consume(self.farmer.id,'food',self.engine.items.count(self.farmer.id,'food'))
        self.engine.navigation.relocate(self.farmer,self.town.market)
        need=self.engine.needs.refresh(self.farmer)[0]
        return [s.action for s in self.engine.goals.solutions(self.farmer,need)]

    def test_work_for_food_does_not_use_fixed_five_coin_threshold(self):
        for money in (5,10,12,13):
            self.assertIn('work',self.food_choices(money))

    def test_known_unaffordable_food_keeps_work_as_valid_solution(self):
        self.assertIn('work',self.food_choices(12))
        self.assertNotIn('buy_food',self.food_choices(12))
        self.assertEqual(self.engine.economy.price(self.town.id,'food'),14)

    def test_unknown_market_price_does_not_use_global_omniscience(self):
        self.farmer.hunger=70;self.farmer.money=12
        self.engine.items.consume(self.farmer.id,'food',self.engine.items.count(self.farmer.id,'food'))
        self.engine.navigation.relocate(self.farmer,self.farmer.home)
        need=self.engine.needs.refresh(self.farmer)[0]
        a=[s.action for s in self.engine.goals.solutions(self.farmer,need)]
        self.stock('food',200)
        b=[s.action for s in self.engine.goals.solutions(self.farmer,need)]
        self.assertEqual(a,b)
        self.assertFalse(self.farmer.market_observation)

    def test_unknown_or_expired_price_does_not_trap_affluent_npc_in_food_work(self):
        self.farmer.hunger=90;self.farmer.money=40
        self.engine.items.consume(self.farmer.id,'food',self.engine.items.count(self.farmer.id,'food'))
        self.engine.navigation.relocate(self.farmer,self.farmer.home)
        self.world.turn=100
        need=next(n for n in self.engine.needs.refresh(self.farmer) if n.kind=='food')
        for observation in ({},{'town_id':self.town.id,'price':14,'price_turn':70,'stock':{'food':1}}):
            self.farmer.market_observation=observation
            actions=[s.action for s in self.engine.goals.solutions(self.farmer,need)]
            self.assertIn('buy_food',actions)
            self.assertNotIn('work',actions)

    def test_unknown_price_still_allows_work_when_known_minimum_is_unaffordable(self):
        self.farmer.hunger=70;self.farmer.money=1
        self.engine.items.consume(self.farmer.id,'food',self.engine.items.count(self.farmer.id,'food'))
        self.engine.navigation.relocate(self.farmer,self.farmer.home)
        need=next(n for n in self.engine.needs.refresh(self.farmer) if n.kind=='food')
        actions=[s.action for s in self.engine.goals.solutions(self.farmer,need)]
        self.assertIn('work',actions)
        self.assertNotIn('buy_food',actions)

    def test_empty_market_is_not_a_financial_shortage_for_affluent_npc(self):
        self.farmer.hunger=90;self.farmer.money=99
        self.engine.items.consume(self.farmer.id,'food',self.engine.items.count(self.farmer.id,'food'))
        self.engine.navigation.relocate(self.farmer,self.town.market)
        self.engine.economy.observe(self.farmer)
        need=next(n for n in self.engine.needs.refresh(self.farmer) if n.kind=='food')
        for position in (self.town.market,self.farmer.home):
            self.engine.navigation.relocate(self.farmer,position)
            actions=[s.action for s in self.engine.goals.solutions(self.farmer,need)]
            self.assertNotIn('work',actions)
            self.assertNotIn('buy_food',actions)
            self.assertIn('forage',actions)

    def test_full_stock_can_allow_alternative_work(self):
        self.farmer.money=1;self.engine.economy.daily()
        self.engine.navigation.relocate(self.farmer,self.farmer.workplace)
        self.engine.economy.observe(self.farmer)
        need=self.engine.needs.refresh(self.farmer)
        work=next(n for n in need if n.kind=='money')
        self.assertIn('work_for_food',[s.action for s in self.engine.goals.solutions(self.farmer,work)])

    def test_partial_stock_space_allows_partial_production(self):
        self.stock('food',238);self.engine.navigation.relocate(self.cook,self.cook.workplace)
        before=self.engine.items.count(self.town.id,'grain')*3+self.town.grain_credit
        self.assertTrue(self.engine.professions.work(self.cook)[0])
        self.assertEqual(self.engine.items.count(self.town.id,'food'),240)
        self.assertEqual(before-(self.engine.items.count(self.town.id,'grain')*3+self.town.grain_credit),4)

    def test_partial_production_pays_proportionally(self):
        self.engine.navigation.relocate(self.cook,self.cook.workplace)
        before=self.cook.money+self.cook.wage_credit/6
        total=self.cook.money+self.town.money
        self.stock('food',238); self.engine.professions.work(self.cook)
        self.assertAlmostEqual(self.cook.money+self.cook.wage_credit/6-before,2/3)
        self.assertEqual(self.cook.money+self.town.money,total)

    def test_professional_capacity_scales_with_local_demand(self):
        first=self.report()['required_cooks']
        self.town.population+=6000;self.town.abstract_population+=6000
        self.assertGreater(self.report()['required_cooks'],first)

    def test_materialization_preserves_total_population(self):
        self.die(self.cook);self.no_candidates();self.vacancy()
        before=self.engine.population.counts(self.town)
        self.assertTrue(self.engine.professions.materialize(self.town))
        after=self.engine.population.counts(self.town)
        self.assertEqual(after['total_living'],before['total_living'])
        self.assertEqual(after['abstract'],before['abstract']-1)
        self.assertEqual(after['persistent_alive'],before['persistent_alive']+1)
        assert_valid(self.world)

    def test_death_reduces_living_population_once(self):
        before=self.town.population
        event=self.die(self.cook)
        self.engine.population.on_death(event);self.engine.population.on_death(event)
        self.assertEqual(self.town.population,before-1)
        assert_valid(self.world)

    def test_materialization_never_duplicates_population(self):
        before=self.engine.population.counts(self.town)
        self.assertFalse(self.engine.population.register(self.town,self.farmer))
        self.assertEqual(self.engine.population.counts(self.town),before)

    def test_professional_demand_does_not_instantly_spawn_worker(self):
        self.die(self.cook);self.no_candidates()
        count=len(self.world.characters); self.engine.economy.daily()
        self.assertEqual(len(self.world.characters),count)

    def test_existing_candidate_preferred_before_materialization(self):
        self.die(self.cook);self.vacancy();self.farmer.money=1
        self.assertFalse(self.engine.professions.materialize(self.town))
        self.engine.economy.daily()
        self.assertEqual(self.town.goal.action,'open_training')

    def test_training_requires_time(self):
        self.die(self.cook);self.vacancy();self.farmer.money=1
        self.engine.navigation.relocate(self.farmer,self.town.market)
        self.engine.economy.observe(self.farmer)
        self.assertTrue(self.engine.professions.train(self.farmer)[0])
        self.assertEqual(self.farmer.profession,'agricultor')
        required=self.farmer.training_required
        for _ in range(required-1):
            self.world.turn+=1;self.engine.professions.train(self.farmer)
        self.assertEqual(self.farmer.profession,'cozinheiro')

    def test_materialized_worker_has_new_identity(self):
        self.die(self.cook);self.no_candidates();self.vacancy()
        before=set(self.world.characters)
        self.assertTrue(self.engine.professions.materialize(self.town))
        new=self.world.characters[next(iter(set(self.world.characters)-before))]
        self.assertNotEqual(new.id,self.cook.id)
        self.assertEqual(new.category,'comum')
        self.assertIsNotNone(new.training_target)
        self.assertTrue(new.origin.startswith('Habitante abstrato'))

    def test_materialized_worker_does_not_copy_dead_workers_memories(self):
        self.die(self.cook);self.no_candidates();self.vacancy()
        before=set(self.world.characters);self.engine.professions.materialize(self.town)
        new=self.world.characters[next(iter(set(self.world.characters)-before))]
        self.assertFalse(set(new.knowledge)&set(self.cook.knowledge))
        self.assertFalse(new.processed_personal_facts)

    def test_replacement_is_limited_by_abstract_population(self):
        self.die(self.cook);self.no_candidates();self.vacancy()
        self.town.abstract_population=0;self.town.population=sum(c.alive for c in self.people)
        self.assertFalse(self.engine.professions.materialize(self.town))

    def test_preventive_survival_uses_known_information_only(self):
        from procedural.goals import Solution
        self.farmer.thirst=70;self.farmer.known_places={}
        choice=Solution('check_relative',10,Location(self.town.id,1,1))
        self.engine.navigation.relocate(self.farmer,self.town.market)
        self.assertIsNone(self.engine.goals.preventive_choice(self.farmer,choice))
        self.farmer.known_places={'well_home':self.farmer.home}
        self.assertEqual(self.engine.goals.preventive_choice(self.farmer,choice).action,'fill_water')
        self.stock('water',0)
        self.assertEqual(self.engine.goals.preventive_choice(self.farmer,choice).action,'fill_water')

    def test_personal_need_records_higher_priority_loss(self):
        self.farmer.hunger=100
        need=self.engine.needs.personal.create(self.farmer,'grief',self.cook.id,40,'fixture','Perda conhecida',48)
        self.engine.goals.decide(self.farmer)
        self.assertEqual(need.context['diagnostic']['reason'],'LostToHigherPriority')
        self.assertEqual(need.context['diagnostic']['competing'],'food')

    def test_personal_need_records_no_viable_solution(self):
        self.farmer.personality.courage=100
        self.engine.navigation.relocate(self.farmer,Location(self.town.id,1,1))
        self.farmer.known_places={};self.farmer.observations={}
        need=self.engine.needs.personal.create(self.farmer,'protection',None,80,'fixture','Ameaça conhecida',48)
        self.farmer.home=Location(1,5,5)
        self.engine.goals.decide(self.farmer)
        self.assertEqual(need.context['diagnostic']['reason'],'NoViableSolution')

    def test_determinism_after_phase3_changes(self):
        self.engine.simulate(144)
        restored=loads(dumps(self.world))
        other=Engine(restored)
        self.engine.simulate(144);other.simulate(144)
        self.assertEqual(dumps(self.world),dumps(restored))

    def test_save_load_preserves_population_and_professional_state(self):
        self.die(self.cook);self.vacancy();self.farmer.money=1
        self.engine.navigation.relocate(self.farmer,self.town.market)
        self.engine.economy.observe(self.farmer);self.engine.professions.train(self.farmer)
        self.assertEqual(dumps(loads(dumps(self.world))),dumps(self.world))

    def test_distribution_consumes_real_food_and_respects_daily_demand(self):
        self.stock('food',200)
        self.engine.navigation.relocate(self.farmer,self.town.market)
        before=self.engine.items.count(self.town.id,'food')+self.engine.items.count(self.farmer.id,'food')
        self.assertTrue(self.engine.professions.temporary_service(self.farmer)[0])
        after=self.engine.items.count(self.town.id,'food')+self.engine.items.count(self.farmer.id,'food')
        self.assertEqual(before-after,1)
        self.assertEqual(self.town.meals_served_today,1)

    def test_worker_abroad_stays_in_population(self):
        before=self.engine.population.counts(self.town)
        self.engine.navigation.relocate(self.farmer,self.town.position)
        self.assertEqual(self.engine.population.counts(self.town),before)

    def test_deprivation_record_identifies_water_and_carried_food(self):
        self.farmer.hunger=0;self.farmer.thirst=100;self.farmer.health=1
        self.farmer.known_places={};self.farmer.last_update=self.world.turn
        self.engine.needs.physiology(self.farmer);self.engine.record_deprivation(self.farmer)
        self.assertEqual(self.world.death_records[self.farmer.id]['cause'],'thirst')
        self.assertGreater(self.world.death_records[self.farmer.id]['food'],0)


if __name__=='__main__':
    unittest.main()
