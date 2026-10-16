"""Regressões causais da Fase 3.2, sobre oportunidades e transferências reais."""
from dataclasses import replace
import unittest

from procedural.engine import Engine
from procedural.models import Fact, Goal, Location, Observation, Personality
from procedural.persistence import dumps, loads
from procedural.validation import assert_valid
from test_simulation import small_world


class Phase32Tests(unittest.TestCase):
    def setUp(self):
        self.world = small_world('Fase32', with_player=True)
        self.engine = Engine(self.world)
        self.person = next(c for c in self.world.characters.values() if c.profession == 'agricultor')
        self.town = self.world.towns[self.person.town_id]
        self.guard = next(c for c in self.world.characters.values() if c.town_id == self.town.id and c.profession == 'guarda')
        self.helper = next(c for c in self.world.characters.values() if c.town_id == self.town.id and c.profession == 'cozinheiro')
        for c in self.world.characters.values():
            self.engine.navigation.relocate(c, c.home)
        for c in (self.person, self.guard, self.helper):
            self.engine.navigation.relocate(c, self.town.market)
            c.knowledge.clear();c.observations.clear();c.needs.clear()
            c.hunger = c.thirst = c.fatigue = 0
            c.goal = None;c.suspended_goal = None
        self.person.personality = Personality(ambition=0, compassion=0, honesty=100, diligence=100)
        self.person.money = 99
        self.person.wage_credit = 0
        self.clear_food(self.person)
        self.stock('food', 100);self.stock('grain', 100)
        self.town.money = 500
        self.engine.goals.debug = True

    def clear_food(self, person):
        self.engine.items.consume(person.id, 'food', self.engine.items.count(person.id, 'food'))

    def stock(self, kind, amount):
        self.engine.items.consume(self.town.id, kind, self.engine.items.count(self.town.id, kind))
        if amount:self.engine.items.create(self.town.id, kind, amount)

    def reserve(self):
        self.engine.economy.observe(self.person)
        return next(n for n in self.engine.needs.refresh(self.person) if n.kind == 'food_reserve')

    def goal(self, need, action, target=None):
        return Goal(self.world.allocate_id(), need.id, action, 50, self.world.turn, target)

    def crime(self, actor=None):
        fact = Fact(self.world.allocate_id(), 'ItemStolen', actor, self.town.id, self.town.market,
                    self.world.turn, 'Roubo testemunhado em cenário controlado.')
        self.person.knowledge[fact.event_id] = fact
        need = self.engine.needs.ensure(self.person, 'revenge:test', 70, f'event:{fact.event_id}', 'Reparação', actor)
        need.context.update(source_event=fact.event_id, culprit=actor)
        self.person.observations[self.guard.id] = Observation(self.world.turn, self.guard.position, 0, 0, 100, profession='guarda')
        return fact, need

    def missing(self):
        self.world.turn = 100
        self.person.observations[self.guard.id] = Observation(60, self.guard.home, 0, 0, 100)
        need = self.engine.needs.ensure(self.person, f'family:{self.guard.id}', 70, 'fixture', 'Ausência', self.guard.id)
        need.context.update(mode='missing', last_seen=60)
        self.engine.graph.set(self.person.id, self.helper.id, 'confiança', 80)
        return need

    def location(self, turn=100, confidence=100):
        return Fact(self.world.allocate_id(), 'PersonLocated', self.helper.id, self.guard.id,
                    self.guard.home, turn, 'Localização em cenário controlado.', confidence=confidence)

    def test_culprit_guard_is_excluded(self):
        _, need = self.crime(self.guard.id)
        self.assertNotIn(('denounce', self.guard.position, self.guard.id), self.engine.personal_actions.candidates(self.person, need))

    def test_another_independent_guard_can_receive(self):
        _, need = self.crime(self.guard.id)
        self.helper.profession = 'guarda'
        self.person.observations[self.helper.id] = Observation(self.world.turn, self.helper.position, 0, 0, 100, profession='guarda')
        choices = self.engine.personal_actions.candidates(self.person, need)
        self.assertIn(('denounce', self.helper.position, self.helper.id), choices)
        self.assertTrue(self.engine.personal_actions.execute(self.person, self.goal(need, 'denounce', self.helper.id), need)[0])
        self.assertEqual(need.status, 'satisfied')

    def test_only_culprit_guard_cannot_close_need(self):
        _, need = self.crime(self.guard.id)
        self.assertFalse(self.engine.personal_actions.execute(self.person, self.goal(need, 'denounce', self.guard.id), need)[0])
        self.assertNotEqual(need.status, 'satisfied')
        self.assertEqual(self.world.metrics.get('ThreatReported', 0), 0)

    def test_unknown_culprit_is_not_excluded_by_global_truth(self):
        _, need = self.crime(None)
        self.assertIn(('denounce', self.guard.position, self.guard.id), self.engine.personal_actions.candidates(self.person, need))

    def test_culprit_learned_after_candidacy_is_revalidated(self):
        fact, need = self.crime(None)
        goal = self.goal(need, 'denounce', self.guard.id)
        self.person.knowledge[fact.event_id] = replace(fact, actor_id=self.guard.id)
        self.assertFalse(self.engine.personal_actions.execute(self.person, goal, need)[0])

    def test_valid_report_can_be_filed_even_if_guard_already_knows(self):
        fact, need = self.crime(self.helper.id)
        self.guard.knowledge[fact.event_id] = fact
        self.assertTrue(self.engine.personal_actions.execute(self.person, self.goal(need, 'denounce', self.guard.id), need)[0])
        self.assertEqual(self.world.metrics['ThreatReported'], 1)
        self.assertEqual(self.world.metrics.get('InformationShared', 0), 0)

    def test_report_save_load(self):
        _, need = self.crime(self.helper.id)
        self.engine.personal_actions.execute(self.person, self.goal(need, 'denounce', self.guard.id), need)
        self.assertTrue(loads(dumps(self.world)).characters[self.person.id].needs['revenge:test'].context['reported'])

    def test_report_is_not_registered_twice(self):
        _, need = self.crime(self.helper.id);goal = self.goal(need, 'denounce', self.guard.id)
        self.engine.personal_actions.execute(self.person, goal, need)
        self.assertFalse(self.engine.personal_actions.execute(self.person, goal, need)[0])
        self.assertEqual(self.world.metrics['ThreatReported'], 1)

    def test_known_fact_does_not_emit_progress(self):
        fact = self.location()
        self.person.knowledge[fact.event_id] = fact
        before = dict(self.world.metrics)
        self.assertFalse(self.engine.personal_actions.inform(self.helper, self.person, fact)[0])
        self.assertEqual(self.world.metrics, before)

    def test_better_confidence_can_be_learned_once(self):
        fact = self.location()
        self.engine.graph.set(self.person.id, self.helper.id, 'confiança', 80)
        self.engine.knowledge.learn(self.person, replace(fact, confidence=30), False)
        self.assertTrue(self.engine.personal_actions.inform(self.helper, self.person, fact)[0])
        self.assertEqual(self.person.knowledge[fact.event_id].confidence, 80)
        reputation = dumps(self.world)
        self.assertFalse(self.engine.personal_actions.inform(self.helper, self.person, fact)[0])
        self.assertEqual(reputation, dumps(self.world))

    def test_location_before_last_observation_is_stale(self):
        need = self.missing()
        self.assertEqual(self.engine.knowledge.information_utility(self.person, self.location(40), need), 'stale_for_need')

    def test_location_before_absence_does_not_close_current_search(self):
        need = self.missing();fact = self.location(80)
        self.helper.knowledge[fact.event_id] = fact
        self.assertFalse(self.engine.personal_actions.execute(self.person, self.goal(need, 'ask_personal_help', self.helper.id), need)[0])
        self.assertEqual(need.status, 'active')

    def test_new_location_closes_current_absence(self):
        need = self.missing();fact = self.location(100)
        self.helper.knowledge[fact.event_id] = fact
        self.assertTrue(self.engine.personal_actions.execute(self.person, self.goal(need, 'ask_personal_help', self.helper.id), need)[0])
        self.assertEqual(need.status, 'satisfied')

    def test_old_unknown_death_is_still_useful(self):
        need = self.missing()
        fact = replace(self.location(10), kind='CharacterDied')
        self.assertEqual(self.engine.knowledge.information_utility(self.person, fact, need), 'new_useful')

    def test_old_location_is_stale_for_current_material_family_help(self):
        need = self.missing();need.context['mode'] = 'care';need.context['resource'] = 'water'
        fact = self.location(80);self.helper.knowledge[fact.event_id] = fact
        self.assertEqual(self.engine.knowledge.information_utility(self.person, fact, need), 'stale_for_need')
        self.assertFalse(self.engine.personal_actions.execute(self.person, self.goal(need, 'ask_personal_help', self.helper.id), need)[0])
        self.assertEqual(need.status, 'active')

    def test_location_confidence_upgrade_can_improve_uncertain_observation(self):
        need = self.missing();need.context['mode'] = 'care'
        fact = self.location(110);self.person.knowledge[fact.event_id] = replace(fact, confidence=30)
        self.person.observations[self.guard.id] = Observation(110, fact.location, None, None, None)
        self.assertEqual(self.engine.knowledge.information_utility(self.person, replace(fact, confidence=80), need), 'better_confidence')

    def test_newer_different_location_is_a_search_lead_before_episode(self):
        need = self.missing();need.context['known_location'] = vars(self.guard.home).copy()
        self.engine.navigation.relocate(self.guard,self.guard.home)
        lead = self.person.known_places['forage']
        fact = replace(self.location(80), location=lead)
        self.helper.knowledge[fact.event_id] = fact
        self.assertTrue(self.engine.personal_actions.execute(self.person, self.goal(need, 'ask_personal_help', self.helper.id), need)[0])
        self.assertEqual(need.context['known_location'], vars(lead))
        self.assertEqual(need.status, 'active')
        self.assertEqual(need.context['information_progress'], 'search_lead')

    def test_location_older_than_failed_search_does_not_restart_same_search(self):
        need = self.missing();need.context.update(searched=True,searched_at=100,known_location=vars(self.guard.home).copy())
        self.world.turn = 120
        fact = self.location(110)
        self.person.observations[self.guard.id].turn = 105
        need.context['searched_at'] = 115
        self.assertEqual(self.engine.knowledge.information_utility(self.person,fact,need), 'stale_for_need')

    def test_useless_reply_does_not_loop_and_new_fact_reopens(self):
        need = self.missing();fact = self.location(40)
        self.helper.knowledge[fact.event_id] = fact
        self.engine.personal_actions.execute(self.person, self.goal(need, 'ask_personal_help', self.helper.id), need)
        self.assertTrue(self.engine.personal_actions.repeated_reply(self.person, self.helper, need))
        new = self.location(100)
        self.helper.knowledge[new.event_id] = new
        self.assertFalse(self.engine.personal_actions.repeated_reply(self.person, self.helper, need))

    def test_reply_memory_is_bounded_and_persisted(self):
        need = self.missing();fact = self.location(40)
        self.helper.knowledge[fact.event_id] = fact
        self.engine.personal_actions.execute(self.person, self.goal(need, 'ask_personal_help', self.helper.id), need)
        restored = loads(dumps(self.world)).characters[self.person.id].needs[f'family:{self.guard.id}']
        self.assertEqual(restored.context['recent_replies'], need.context['recent_replies'])
        self.assertLessEqual(len(restored.context['recent_replies']), 8)

    def test_new_information_is_not_blocked_by_generic_action_cooldown(self):
        need = self.missing();self.person.personality.family_loyalty = 100
        self.engine.navigation.relocate(self.guard, self.guard.home)
        old = self.location(40);self.helper.knowledge[old.event_id] = old
        self.engine.goals.decide(self.person)
        self.assertEqual(self.person.goal.action, 'ask_personal_help')
        self.assertNotIn('ask_personal_help', self.person.failures)
        fresh = self.location(100);self.helper.knowledge[fresh.event_id] = fresh
        self.assertIn('ask_personal_help', [s.action for s in self.engine.goals.solutions(self.person, need)])

    def test_second_ration_still_can_be_financed(self):
        self.person.money = 0
        for owned in (0, 1):
            if owned:self.engine.items.create(self.person.id, 'food')
            actions = [s.action for s in self.engine.goals.solutions(self.person, self.reserve())]
            self.assertIn('work', actions, owned)

    def test_full_normal_reserve_has_no_deficit(self):
        self.engine.items.create(self.person.id, 'food', 2)
        self.assertFalse(any(n.kind == 'food_reserve' for n in self.engine.needs.refresh(self.person)))

    def test_partial_purchase_when_only_one_is_affordable(self):
        self.person.money = self.engine.economy.price(self.town.id, 'food')
        total = self.person.money+self.town.money
        self.assertTrue(self.engine.economy.buy_reserve(self.person, 2, True)[0])
        self.assertEqual(self.engine.items.count(self.person.id, 'food'), 1)
        self.assertEqual(self.person.money+self.town.money, total)

    def test_batch_uses_marginal_price_curve(self):
        self.town.population = 1000
        self.stock('food', 5)
        cost = self.engine.economy.quote(self.town.id, 'food', 2)
        self.assertNotEqual(cost, 2*self.engine.economy.price(self.town.id, 'food'))
        before = self.person.money
        self.assertTrue(self.engine.economy.buy_reserve(self.person, 2, True)[0])
        self.assertEqual(before-self.person.money, cost)
        self.assertEqual(self.engine.items.count(self.person.id, 'food'), 2)
        self.assertEqual(self.engine.items.count(self.town.id, 'food'), 3)

    def test_purchase_limited_by_stock_and_target(self):
        self.stock('food', 1)
        self.assertTrue(self.engine.economy.buy_reserve(self.person, 2, True)[0])
        self.assertEqual(self.engine.items.count(self.person.id, 'food'), 1)
        self.stock('food', 100)
        self.assertTrue(self.engine.economy.buy_reserve(self.person, 2, True)[0])
        self.assertEqual(self.engine.items.count(self.person.id, 'food'), 2)
        self.assertFalse(self.engine.economy.buy_reserve(self.person, 2, True)[0])

    def cook(self):
        self.person.profession = 'cozinheiro';self.person.workplace = self.town.market
        self.person.money = 0;self.person.wage_credit = 0;self.stock('food', 239)

    def test_fractional_credit_is_success_and_accumulates_without_money_creation(self):
        self.cook();total = self.person.money+self.town.money
        result = self.engine.professions.work(self.person)
        self.assertEqual((result.status, result.success, result.produced, result.paid), ('credited', True, 1, 0))
        self.assertEqual(self.person.wage_credit, 2)
        for _ in range(2):
            self.engine.items.consume(self.town.id, 'food')
            self.engine.professions.work(self.person)
        self.assertEqual((self.person.money, self.person.wage_credit), (1, 0))
        self.assertEqual(self.person.money+self.town.money, total)

    def test_fractional_work_does_not_receive_failure_cooldown(self):
        self.cook();self.engine.items.create(self.person.id, 'food', 2)
        self.engine.goals.decide(self.person)
        self.assertEqual(self.person.wage_credit, 2)
        self.assertNotIn('work', self.person.failures)
        self.assertEqual(self.person.goal.status, 'completed')

    def test_wage_credit_survives_save_and_converts_once(self):
        self.cook();self.engine.professions.work(self.person)
        restored = Engine(loads(dumps(self.world)));person = restored.world.characters[self.person.id]
        restored.economy.wage(person, 4, sixths=True)
        self.assertEqual((person.money, person.wage_credit), (1, 0))
        self.assertEqual(restored.economy.wage(person, 0, sixths=True), 0)
        assert_valid(restored.world)

    def test_saturation_and_missing_inputs_are_distinct(self):
        self.cook();self.stock('food', 240)
        self.assertEqual(self.engine.professions.work(self.person).status, 'saturated')
        self.stock('food', 0);self.stock('grain', 0);self.town.grain_credit = 0
        self.assertEqual(self.engine.professions.work(self.person).status, 'no_input')

    def test_no_payer_does_not_create_product_or_salary(self):
        self.cook();self.town.money = 0;before = dumps(self.world)
        self.assertEqual(self.engine.professions.work(self.person).status, 'no_payer')
        self.assertEqual(before, dumps(self.world))

    def offers(self):
        self.town.economic_report = {'stock': {'food': 0}, 'expected_demand': 30, 'bottlenecks': ['AFFORDABILITY_PROBLEM']}
        self.engine.economy.observe(self.person)
        return self.person.market_observation['temporary_offers']

    def test_exhausted_quota_is_not_advertised(self):
        import math
        self.town.meals_served_today = math.ceil(self.town.abstract_population/120)
        self.assertNotIn('meal_distribution', self.offers())
        self.assertNotIn('temporary_service', [s.action for s in self.engine.goals.solutions(self.person, self.reserve())])

    def test_positive_capacity_can_be_advertised(self):
        self.assertGreater(self.offers()['meal_distribution']['capacity'], 0)

    def test_competitor_can_exhaust_quota_after_observation(self):
        import math
        self.town.meals_served_today = math.ceil(self.town.abstract_population/120)-1
        self.offers();self.assertTrue(self.engine.professions.temporary_service(self.helper)[0])
        food = self.engine.items.count(self.person.id, 'food')
        self.assertFalse(self.engine.professions.temporary_service(self.person)[0])
        self.assertEqual(self.engine.items.count(self.person.id, 'food'), food)

    def test_temporary_payment_consumes_actual_stock(self):
        stock = self.engine.items.count(self.town.id, 'food')
        self.assertTrue(self.engine.professions.temporary_service(self.person)[0])
        self.assertEqual(self.engine.items.count(self.town.id, 'food'), stock-2)
        self.assertEqual(self.engine.items.count(self.person.id, 'food'), 1)

    def test_stock_lost_after_offer_is_honest_failure(self):
        self.offers();self.stock('food', 0)
        self.assertFalse(self.engine.professions.temporary_service(self.person)[0])
        self.assertEqual(self.engine.items.count(self.person.id, 'food'), 0)

    def test_expired_offer_does_not_supply_solution(self):
        self.offers();self.world.turn += 25
        need = self.engine.needs.ensure(self.person, 'money', 50, 'fixture', 'Renda')
        self.assertNotIn('temporary_service', [s.action for s in self.engine.goals.solutions(self.person, need)])

    def test_incompatible_installation_does_not_offer_remote_work(self):
        other = next(t for t in self.world.towns.values() if t.id != self.town.id)
        self.person.workplace = other.market
        self.engine.navigation.relocate(self.person, other.market)
        need = self.engine.needs.ensure(self.person, 'money', 50, 'fixture', 'Renda')
        self.assertNotIn('work', [s.action for s in self.engine.goals.solutions(self.person, need)])
        before = self.town.money
        self.assertEqual(self.engine.professions.work(self.person).status, 'incompatible_local')
        self.assertEqual(self.town.money, before)

    def test_healthy_near_market_can_choose_prevention(self):
        self.person.hunger = 20
        reserve = self.reserve()
        self.assertGreater(reserve.priority, 40)
        self.engine.goals.decide(self.person)
        self.assertEqual(self.engine.goals.traces[self.person.id]['need'], 'food_reserve')
        self.assertGreaterEqual(self.engine.items.count(self.person.id, 'food'), 1)
        self.assertEqual(self.person.hunger, 20)

    def test_second_ration_is_legitimate_prevention(self):
        self.person.hunger = 20;self.engine.items.create(self.person.id, 'food')
        self.engine.goals.decide(self.person)
        self.assertEqual(self.engine.items.count(self.person.id, 'food'), 2)

    def test_high_grief_can_beat_second_ration(self):
        self.person.hunger = 20;self.engine.items.create(self.person.id, 'food')
        grief = self.engine.needs.personal.create(self.person, 'grief', self.guard.id, 85, 'fixture', 'Luto', 96)
        self.engine.goals.decide(self.person)
        self.assertEqual(self.person.goal.need_id, grief.id)

    def test_known_departure_increases_coverage_pressure(self):
        self.person.hunger = 25;need = self.reserve();before = need.priority
        self.person.goal = Goal(self.world.allocate_id(), need.id, 'sleep', 50, self.world.turn,
                                destination=Location(self.town.id, self.town.market.x+40, self.town.market.y))
        self.assertGreater(self.engine.feeding.reserve_pressure(self.person, need), before)
        self.assertGreater(need.context['next_known_opportunity_hours'], 40)
        self.assertGreater(need.context['ReserveTarget'], 2)

    def test_no_money_no_work_does_not_invent_purchase_or_income(self):
        self.person.hunger = 25;self.person.money = 0;self.stock('grain', 240)
        self.person.known_places = {'market': self.town.market}
        need = self.reserve()
        choices = [s.action for s in self.engine.goals.solutions(self.person, need)]
        self.assertNotIn('buy_food', choices);self.assertNotIn('work', choices)

    def test_no_known_executable_path_can_remain_blocked(self):
        self.person.hunger = 20;self.person.money = 0;self.person.profession = None
        self.person.known_places = {};self.person.market_observation.clear()
        need = next(n for n in self.engine.needs.refresh(self.person) if n.kind == 'food_reserve')
        self.assertEqual(self.engine.goals.solutions(self.person, need), [])

    def test_critical_sleep_can_win(self):
        self.person.hunger = 25;self.person.fatigue = 100
        self.engine.goals.decide(self.person)
        self.assertEqual(self.engine.goals.traces[self.person.id]['need'], 'rest')

    def test_critical_thirst_can_win(self):
        self.person.hunger = 25;self.person.thirst = 100
        self.engine.goals.decide(self.person)
        self.assertEqual(self.engine.goals.traces[self.person.id]['need'], 'water')

    def test_waiting_continues_past_54_hours_but_is_bounded(self):
        need = self.reserve();self.world.turn += 60
        first = self.engine.feeding.reserve_pressure(self.person, need)
        self.world.turn += 500
        later = self.engine.feeding.reserve_pressure(self.person, need)
        self.assertGreater(later, first);self.assertLessEqual(later, 85)

    def test_remote_stock_changes_do_not_grant_global_knowledge(self):
        self.engine.navigation.relocate(self.person, self.person.home)
        self.person.market_observation.clear()
        need = self.reserve();before = self.engine.feeding.reserve_pressure(self.person, need)
        self.stock('food', 0);self.town.money = 0
        self.assertEqual(self.engine.feeding.reserve_pressure(self.person, need), before)

    def test_emergency_meal_is_not_tied_with_delayed_equivalent_acquisition(self):
        self.person.hunger=100;self.person.thirst=96;self.person.health=5;self.person.starvation_hours=13
        self.person.personality.independence=100
        self.engine.navigation.relocate(self.person,self.person.known_places['forage'])
        food=next(n for n in self.engine.needs.refresh(self.person) if n.kind=='food')
        choices=[s.action for s in self.engine.goals.solutions(self.person,food)]
        self.assertIn('forage_meal',choices);self.assertNotIn('forage',choices)
        self.engine.goals.decide(self.person)
        self.assertEqual(self.person.goal.action,'forage_meal')
        self.engine.needs.physiology(self.person)
        self.assertEqual(self.person.health,5)
        self.engine.goals.decide(self.person)
        self.engine.needs.physiology(self.person)
        self.assertGreater(self.person.health,0)


if __name__ == '__main__':unittest.main()
