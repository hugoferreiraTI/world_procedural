"""Regressões causais de alimentação, prazo, conhecimento e persistência."""
from dataclasses import replace
import unittest

from procedural.engine import Engine
from procedural.models import Goal, Location, Personality
from procedural.persistence import dumps, loads
from procedural.rules import FEEDING
from procedural.validation import assert_valid
from test_simulation import small_world


class FeedingTests(unittest.TestCase):
    def setUp(self):
        self.world = small_world('Alimentacao', with_player=True)
        self.engine = Engine(self.world)
        # Isola o mecanismo alimentar; parentes gerados não começam em crise.
        for other in self.world.characters.values():other.hunger=other.thirst=0
        self.person = next(c for c in self.world.characters.values() if c.profession == 'agricultor')
        self.town = self.world.towns[self.person.town_id]
        self.engine.navigation.relocate(self.person, self.town.market)
        self.person.hunger = self.person.thirst = self.person.fatigue = 0
        self.person.health, self.person.money = 100, 99
        self.person.personality = Personality(honesty=100, compassion=0, independence=0, diligence=100)
        self.person.needs.clear();self.person.goal = None;self.person.suspended_goal = None
        self.engine.items.consume(self.person.id, 'food', self.engine.items.count(self.person.id, 'food'))
        self.person.food_state.clear()
        self.stock('food', 200)
        self.engine.goals.debug = True

    def stock(self, kind, amount):
        old = self.engine.items.count(self.town.id, kind)
        if old:self.engine.items.consume(self.town.id, kind, old)
        if amount:self.engine.items.create(self.town.id, kind, amount)

    def give_food(self, count=2):
        self.engine.items.create(self.person.id, 'food', count)

    def need(self, kind):
        return next(n for n in self.engine.needs.refresh(self.person) if n.kind == kind)

    def active_goal(self, kind, action, destination=None):
        need = self.engine.needs.ensure(self.person, kind, 35, 'fixture', 'Objetivo em curso')
        goal = Goal(self.world.allocate_id(), need.id, action, 60, self.world.turn, destination=destination)
        self.person.goal = goal
        return goal

    def test_moderate_hunger_with_sufficient_reserve_does_not_search(self):
        self.person.hunger = FEEDING.meal_threshold-1;self.give_food()
        active = self.engine.needs.refresh(self.person)
        self.assertFalse(any(n.kind in ('food', 'food_reserve') for n in active))
        self.engine.goals.decide(self.person)
        self.assertNotIn(self.person.goal.action if self.person.goal else None, ('buy_food', 'forage', 'eat'))

    def test_healthy_deficit_generates_moderate_reserve_need(self):
        reserve = self.need('food_reserve')
        self.assertLess(reserve.priority, 50)
        self.assertEqual(reserve.context['ReserveTarget'], 2)
        self.engine.goals.decide(self.person)
        self.assertEqual(self.person.goal.action, 'buy_food')
        self.assertEqual(self.person.hunger, 0)
        self.assertEqual(self.engine.items.count(self.person.id, 'food'), 1)

    def test_reserve_does_not_override_important_personal_need(self):
        self.person.personality.courage = 0
        self.engine.needs.personal.create(self.person, 'protection', None, 80, 'fixture', 'Proteger residência', 48)
        self.engine.goals.decide(self.person)
        self.assertEqual(self.engine.goals.traces[self.person.id]['need'], 'protection')

    def test_meal_at_normal_threshold_uses_most_nutrition(self):
        self.person.hunger = FEEDING.meal_threshold;self.give_food()
        need=self.need('food')
        choices=self.engine.goals.solutions(self.person,need)
        choice=self.engine.goals.choose(choices)
        self.assertEqual('eat',choice.action)
        goal=Goal(self.world.allocate_id(),need.id,choice.action,choice.score,self.world.turn)
        self.assertTrue(self.engine.goals.execute(self.person,goal,1)[0])
        self.assertEqual(self.person.hunger, max(0,FEEDING.meal_threshold-FEEDING.meal_reduction))
        self.assertEqual(self.world.metrics['Feeding:NutritionUsed:sum'], min(FEEDING.meal_threshold,FEEDING.meal_reduction))

    def test_work_is_interrupted_with_food_and_critical_hunger(self):
        self.person.money = 0
        old = self.active_goal('money', 'work', self.person.workplace)
        self.person.hunger = 100;self.person.health = 1;self.give_food(1)
        self.engine.goals.decide(self.person)
        self.engine.needs.physiology(self.person)
        self.assertEqual(self.person.goal.action, 'eat')
        self.assertEqual(self.person.health, 1)
        self.assertIs(self.person.suspended_goal, old)
        self.assertEqual(self.world.metrics['EmergencyGoalInterrupted'], 1)

    def test_critical_meal_beats_older_rest_need_by_risk(self):
        rest = self.engine.needs.ensure(self.person, 'rest', 100, 'fixture', 'Descanso antigo')
        self.person.hunger = self.person.fatigue = 100;self.person.health = 1;self.give_food(1)
        self.assertLess(rest.id, self.need('food').id)
        self.engine.goals.decide(self.person)
        self.assertEqual(self.person.goal.action, 'eat')

    def test_active_trip_does_not_block_immediate_consumption(self):
        self.engine.navigation.relocate(self.person, self.person.home)
        self.person.hunger = 100;self.person.health = 2;self.give_food(1)
        old = self.active_goal('food', 'buy_food', self.town.market)
        position = self.person.position
        self.engine.goals.decide(self.person)
        self.assertEqual(self.person.position, position)
        self.assertEqual(self.person.goal.action, 'eat')
        self.assertIs(self.person.suspended_goal, old)

    def test_training_is_interrupted_for_critical_meal(self):
        self.person.training_target = 'cozinheiro';self.person.training_required = 24
        self.active_goal('money', 'train', self.town.market)
        self.person.hunger = 100;self.person.health = 1;self.give_food(1)
        self.engine.goals.decide(self.person)
        self.assertEqual(self.person.goal.action, 'eat')
        self.assertEqual(self.person.training_progress, 0)

    def test_preparation_does_not_take_water_before_fatal_food(self):
        from procedural.goals import Solution
        self.person.hunger = 100;self.person.health = 1;self.person.thirst = 77;self.give_food(1)
        self.engine.navigation.relocate(self.person, self.person.known_places['forage'])
        choice = Solution('sleep', 100, self.person.home)
        self.assertEqual(self.engine.goals.preventive_choice(self.person, choice).action, 'eat')

    def test_fatal_thirst_is_not_confused_with_high_but_nonfatal_hunger(self):
        self.person.hunger = 80;self.person.thirst = 100;self.person.health = 1;self.give_food(1)
        self.engine.goals.decide(self.person)
        self.engine.needs.physiology(self.person)
        self.assertEqual(self.person.goal.action, 'drink_well')
        self.assertEqual(self.person.health, 1)

    def test_long_income_chain_is_rejected_when_biologically_impossible(self):
        self.stock('food', 1);self.person.money = 0;self.person.hunger = 100;self.person.health = 2
        self.engine.economy.observe(self.person)
        food = self.need('food')
        # COMMAND explícito: este teste inspeciona o diagnóstico do planejamento.
        choices = self.engine.goals.plan_solutions(self.person, food)
        self.assertNotIn('work', [s.action for s in choices])
        rejected = next(s for s in self.engine.goals.rejected_food[self.person.id] if s.action == 'work')
        self.assertTrue(rejected.feeding['economically_viable'])
        self.assertFalse(rejected.feeding['survival_viable'])
        self.assertEqual(rejected.feeding['reason'], 'SolutionTooSlow')
        self.assertGreater(rejected.feeding['EstimatedTimeUntilFoodConsumed'], rejected.feeding['EstimatedSurvivalMargin'])

    def test_poor_person_with_time_can_still_work_for_food(self):
        self.stock('food', 1);self.person.money = 0;self.person.hunger = 70
        self.engine.economy.observe(self.person)
        choices = self.engine.goals.solutions(self.person, self.need('food'))
        work = next(s for s in choices if s.action == 'work')
        self.assertTrue(work.feeding['survival_viable'])

    def test_emergency_market_meal_consumes_real_stock_and_money(self):
        self.person.hunger = 100;self.person.health = 1
        old_stock = self.engine.items.count(self.town.id, 'food')
        cash = self.person.money+self.town.money
        old_money = self.person.money
        self.engine.goals.decide(self.person)
        self.assertEqual(self.person.goal.action, 'buy_meal')
        self.assertEqual(self.engine.items.count(self.person.id, 'food'), 0)
        self.assertEqual(self.engine.items.count(self.town.id, 'food'), old_stock-1)
        self.assertEqual(self.person.money+self.town.money, cash)
        self.assertLess(self.person.money, old_money)
        self.engine.needs.physiology(self.person)
        self.assertEqual(self.person.health, 1)
        self.assertEqual(self.person.hunger, 62)

    def test_empty_market_cannot_produce_emergency_meal(self):
        self.stock('food', 0);self.person.hunger = 100;self.person.health = 1
        self.engine.economy.observe(self.person)
        choices = self.engine.goals.solutions(self.person, self.need('food'))
        self.assertNotIn('buy_meal', [s.action for s in choices])
        self.assertIn('NoProduct', self.engine.feeding.knowledge_status(self.person))

    def test_public_meal_action_uses_same_stock_and_one_hour(self):
        player = self.engine.player
        self.engine.navigation.relocate(player, self.town.market)
        player.health = 1;player.hunger = 100;player.thirst = 0;player.money = 99
        turn = self.world.turn
        self.assertTrue(self.engine.execute('refeicao').success)
        self.assertEqual(self.world.turn, turn+1)
        self.assertEqual(player.health, 1)
        self.assertEqual(player.hunger, 62)

    def test_invalid_public_meal_does_not_mutate_or_advance_time(self):
        before = dumps(self.world)
        self.assertFalse(self.engine.execute('refeicao').success)
        self.assertEqual(dumps(self.world), before)

    def test_purchase_for_reserve_does_not_reduce_hunger(self):
        self.person.hunger = 35
        self.engine.goals.decide(self.person)
        self.assertEqual(self.person.goal.action, 'buy_food')
        self.assertEqual(self.person.hunger, 35)

    def test_food_paid_work_does_not_accumulate_a_six_hour_batch_for_reserve(self):
        self.person.money = 0;self.stock('grain', 100)
        self.engine.navigation.relocate(self.person, self.person.known_places['forage'])
        reserve = self.need('food_reserve')
        goal = Goal(self.world.allocate_id(), reserve.id, 'work_for_food', 60, self.world.turn)
        self.assertTrue(self.engine.goals.execute(self.person, goal, 6)[0])
        self.assertEqual(self.engine.items.count(self.person.id, 'food'), 2)

    def test_full_reserve_and_product_payment_do_not_generate_unbounded_food(self):
        self.person.money = 0;self.give_food(3)
        self.engine.economy.observe(self.person)
        self.person.market_observation.update(temporary_work=True, stock={'food':200,'grain':100})
        money = self.need('money')
        choices = self.engine.goals.solutions(self.person, money)
        self.assertNotIn('temporary_service', [s.action for s in choices])
        self.assertNotIn('work_for_food', [s.action for s in choices])

    def test_trip_reserve_is_bounded_and_uses_known_duration(self):
        near = Location(self.town.id, self.person.position.x+5, self.person.position.y)
        far = Location(self.town.id, self.person.position.x+40, self.person.position.y)
        self.assertEqual(self.engine.feeding.reserve_target(self.person, near), 2)
        self.assertEqual(self.engine.feeding.reserve_target(self.person, far), 3)
        self.assertLessEqual(self.engine.feeding.reserve_target(self.person, Location(self.town.id, 999, 0)), FEEDING.maximum_reserve)
        self.assertEqual(self.engine.feeding.reserve_target(self.person, Location(1, 200, 200)), 2)
        self.assertEqual(self.engine.feeding.travel_assessment(self.person, Location(1, 200, 200))['reason'], 'UnknownRoute')

    def test_unknown_price_and_remote_stock_do_not_change_choices(self):
        self.engine.navigation.relocate(self.person, self.person.home)
        self.person.hunger = 60
        food = self.need('food')
        a = [(s.action, s.score, s.feeding) for s in self.engine.goals.solutions(self.person, food)]
        self.stock('food', 0)
        b = [(s.action, s.score, s.feeding) for s in self.engine.goals.solutions(self.person, food)]
        self.assertEqual(a, b)
        self.assertIn('UnknownPrice', self.engine.feeding.knowledge_status(self.person))

    def test_save_load_preserves_reserve_and_suspended_goal(self):
        self.active_goal('money', 'work', self.person.workplace)
        self.person.money = 0;self.person.hunger = 100;self.give_food(2)
        self.engine.goals.decide(self.person)
        restored = loads(dumps(self.world))
        self.assertEqual(dumps(restored), dumps(self.world))
        self.assertEqual(restored.characters[self.person.id].suspended_goal, self.person.suspended_goal)
        self.assertEqual(restored.characters[self.person.id].food_state, self.person.food_state)
        assert_valid(restored)

    def test_suspended_goal_resumes_after_stabilization_if_valid(self):
        self.person.money = 0
        self.engine.navigation.relocate(self.person, self.person.workplace)
        old = self.active_goal('money', 'work', self.person.workplace)
        self.person.hunger = 100;self.give_food(3)
        self.engine.goals.decide(self.person)
        self.assertLess(self.person.hunger, FEEDING.high_hunger)
        self.engine.goals.decide(self.person)
        self.assertIsNone(self.person.suspended_goal)
        self.assertEqual(self.person.goal.id, old.id)
        self.assertEqual(self.person.goal.action, 'work')

    def test_same_seed_and_actions_continue_deterministically(self):
        # Os estoques do fixture foram criados fora do ciclo Engine.step.
        self.world.rng_state = self.engine.rng.getstate()
        other = Engine(loads(dumps(self.world)))
        self.engine.simulate(72);other.simulate(72)
        self.assertEqual(dumps(self.world), dumps(other.world))

    def test_consumption_timestamps_follow_oldest_acquisition(self):
        self.give_food(1)
        self.world.turn += 4;self.give_food(1)
        self.world.turn += 3;self.person.hunger = 50
        self.engine.goals.decide(self.person)
        metric = self.world.metrics['Feeding:TimeFromAcquisitionToConsumption:sum']
        self.assertEqual(metric, 7)


if __name__ == '__main__':
    unittest.main()
