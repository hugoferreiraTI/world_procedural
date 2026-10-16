"""Regressões reproduzidas nas campanhas; não incluem reposição populacional."""

from dataclasses import replace
import unittest

from procedural.engine import Engine
from procedural.models import Fact, Goal, Personality, Reputation
from procedural.persistence import dumps, loads
from test_simulation import small_world


class HardeningTests(unittest.TestCase):
    def setUp(self):
        self.world = small_world("Hardening", with_player=True)
        self.engine = Engine(self.world)
        self.player = self.engine.player
        self.town = self.world.towns[self.player.town_id]
        self.npc = next(c for c in self.world.characters.values()
                        if c.town_id == self.town.id and c.profession == "agricultor")

    def hungry(self):
        self.engine.navigation.relocate(self.player, self.town.market)
        self.engine.navigation.relocate(self.npc, self.town.market)
        self.engine.items.consume(self.npc.id, "food", self.engine.items.count(self.npc.id, "food"))
        self.npc.hunger, self.npc.money = 90, 0
        self.npc.personality = Personality(honesty=100, compassion=100, independence=0)
        self.engine.graph.set(self.npc.id, self.player.id, "confiança", 60)

    def test_starvation_prevents_unlimited_rest_healing(self):
        self.player.hunger, self.player.thirst, self.player.health = 100, 0, 40
        for _ in range(100):
            if not self.player.alive:
                break
            self.assertTrue(self.engine.execute("descansar").success)
        self.assertFalse(self.player.alive)

    def test_market_buy_sell_loop_cannot_generate_free_money(self):
        self.engine.navigation.relocate(self.player, self.town.market)
        self.player.money = 10000
        for kind in ("wood", "grain", "iron", "food", "water"):
            quantity = self.engine.items.count(self.town.id, kind)
            before = self.player.money
            combined = self.player.money + self.town.money
            self.assertTrue(self.engine.economy.buy(self.player.id, self.town.id, kind, quantity)[0])
            item = self.engine.items.first(self.player.id, kind)
            self.assertTrue(self.engine.economy.sell(self.player.id, self.town.id, item, quantity)[0])
            self.assertLess(self.player.money, before)
            self.assertEqual(self.player.money + self.town.money, combined)

    def test_economic_state_does_not_overwrite_political_state(self):
        kingdom = next(iter(self.world.kingdoms.values()))
        for entity_id in kingdom.royal_family:
            person = self.world.characters[entity_id]
            person.alive, person.health = False, 0
            self.engine.recorder.emit("CharacterDied", "Morte", target_id=person.id)
        self.assertIsNone(kingdom.ruler_id)
        self.engine.economy.daily()
        self.assertEqual(kingdom.status, "crise sucessória")
        self.assertEqual(kingdom.political_state, "crise sucessória")

    def test_same_fact_does_not_apply_reputation_twice(self):
        fact = Fact(self.world.allocate_id(), "HelpGiven", self.player.id, self.npc.id,
                    self.npc.position, 0, "Ajuda")
        self.engine.knowledge.learn(self.npc, fact, True)
        before = self.npc.reputations[self.player.id].tags.copy()
        for _ in range(70):
            self.engine.knowledge.learn(self.npc, Fact(self.world.allocate_id(), "Other", None,
                                                    None, None, 0, "Outra informação"), True)
        self.assertNotIn(fact.event_id, self.npc.knowledge)
        self.engine.knowledge.learn(self.npc, fact, True)
        self.assertEqual(self.npc.reputations[self.player.id].tags, before)

    def test_information_source_reliability_affects_reputation(self):
        other = next(c for c in self.world.characters.values() if c.id not in (self.npc.id, self.player.id))
        other.personality = replace(self.npc.personality)
        fact = Fact(self.world.allocate_id(), "HelpGiven", self.player.id, None, None, 0, "Ajuda")
        self.engine.knowledge.learn(self.npc, fact, True)
        self.engine.knowledge.learn(other, replace(fact, confidence=20), False)
        self.assertGreater(self.npc.reputations[self.player.id].admiration,
                           other.reputations[self.player.id].admiration)

    def test_conversation_cannot_be_used_to_farm_trust(self):
        self.hungry()
        self.npc.hunger = 0
        before = self.engine.graph.value(self.npc.id, self.player.id, "confiança")
        for _ in range(8):
            self.engine.navigation.relocate(self.npc, self.player.position)
            self.assertTrue(self.engine.execute(f"conversar {self.npc.id}").success)
        self.assertEqual(self.engine.graph.value(self.npc.id, self.player.id, "confiança"), before)

    def test_npc_can_autonomously_request_player_help(self):
        self.hungry()
        # Isola o encontro; outro conhecido com confiança maior pode vencer.
        for npc in self.engine.nearby():
            if npc.id != self.npc.id:
                self.engine.navigation.relocate(npc, npc.home)
        self.npc.known_places = {"market": self.town.market}
        self.engine.goals.decide(self.npc)
        self.assertEqual(self.npc.goal.action, "ask_help")
        self.assertEqual(self.npc.goal.target_id, self.player.id)
        self.assertTrue(any(q.owner_id == self.npc.id for q in self.world.quests.values()))

    def test_positive_reputation_changes_npc_behavior(self):
        self.hungry()
        self.player.hunger, self.npc.hunger = 80, 0
        self.engine.items.create(self.npc.id, "food", 3)
        self.npc.personality.compassion = 40
        self.engine.graph.set(self.npc.id, self.player.id, "confiança", 10)
        self.engine.needs.refresh(self.player)
        goal = Goal(self.world.allocate_id(), self.player.needs["food"].id, "ask_help", 0,
                    self.world.turn, target_id=self.npc.id)
        self.assertFalse(self.engine.goals.execute(self.player, goal, 1)[0])
        self.npc.reputations[self.player.id] = Reputation(tags={"prestativo": 80}, admiration=80)
        self.assertTrue(self.engine.goals.execute(self.player, goal, 1)[0])

    def test_request_refusal_is_interpreted_through_context_and_personality(self):
        self.hungry()
        self.npc.personality.compassion = 0
        quest = self.engine.quests.offer(self.npc, self.player)
        before = self.engine.graph.value(self.npc.id, self.player.id, "confiança")
        self.engine.quests.respond(quest.id, False)
        self.assertLess(self.engine.graph.value(self.npc.id, self.player.id, "confiança"), before)
        self.assertTrue(any(e.kind == "PlayerRefusedRequest" for e in self.world.events))

    def test_player_has_multiple_valid_ways_to_satisfy_hunger(self):
        self.engine.navigation.enter(self.player)
        self.engine.navigation.relocate(self.player, self.npc.known_places["forage"])
        self.assertTrue(self.engine.execute("coletar").success)
        before = self.engine.items.count(self.player.id, "food")
        self.assertTrue(self.engine.execute("trabalhar").success)
        self.assertGreater(self.engine.items.count(self.player.id, "food"), before)
        self.hungry()
        self.npc.hunger = 0
        self.npc.personality.compassion = 100
        self.engine.items.create(self.npc.id, "food", 3)
        self.assertTrue(self.engine.execute(f"pedir comida {self.npc.id}").success)

    def test_new_social_state_survives_save_and_load(self):
        self.hungry()
        self.engine.recorder.emit("HelpGiven", "Ajuda", self.player.id, self.npc.id,
                                  self.npc.position)
        restored = loads(dumps(self.world))
        self.assertEqual(dumps(restored), dumps(self.world))

    def test_npc_rest_cannot_cancel_progressive_deprivation(self):
        self.npc.hunger, self.npc.thirst, self.npc.health = 100, 0, 100
        first_damage = None
        for _ in range(100):
            before = self.npc.health
            self.engine.needs.rest(self.npc)
            self.engine.needs.physiology(self.npc)
            if first_damage is None:
                first_damage = before - self.npc.health
            if self.npc.health == 0:
                break
        self.assertEqual(self.npc.health, 0)
        self.assertGreater(self.npc.starvation_hours, 12)
        self.assertGreaterEqual(first_damage, 2)

    def test_bulk_and_split_resale_follow_same_price_curve(self):
        self.engine.navigation.relocate(self.player, self.town.market)
        self.player.money = 10000
        before = self.player.money
        self.assertTrue(self.engine.economy.buy(self.player.id, self.town.id, "wood", 24)[0])
        for quantity in (3, 1, 7, 13):
            item_id = self.engine.items.first(self.player.id, "wood")
            self.assertTrue(self.engine.economy.sell(self.player.id, self.town.id, item_id, quantity)[0])
        self.assertLess(self.player.money, before)
        before = self.player.money
        for _ in range(24):
            self.assertTrue(self.engine.economy.buy(self.player.id, self.town.id, "wood")[0])
        item_id = self.engine.items.first(self.player.id, "wood")
        self.assertTrue(self.engine.economy.sell(self.player.id, self.town.id, item_id, 24)[0])
        self.assertLess(self.player.money, before)

    def test_stronger_evidence_upgrades_only_the_fact_difference(self):
        fact = Fact(self.world.allocate_id(), "HelpGiven", self.player.id, self.npc.id,
                    self.npc.position, 0, "Ajuda", confidence=30)
        self.engine.knowledge.learn(self.npc, fact, False)
        rumor = self.npc.reputations[self.player.id].admiration
        self.engine.knowledge.learn(self.npc, replace(fact, confidence=100), True)
        witnessed = self.npc.reputations[self.player.id].admiration
        self.assertGreater(witnessed, rumor)
        other = next(c for c in self.world.characters.values() if c.id not in (self.npc.id, self.player.id))
        other.personality = replace(self.npc.personality)
        self.engine.knowledge.learn(other, replace(fact, target_id=other.id, confidence=100), True)
        self.assertEqual(witnessed, other.reputations[self.player.id].admiration)
        restored = loads(dumps(self.world))
        npc = restored.characters[self.npc.id]
        npc.knowledge.clear()
        Engine(restored).knowledge.learn(npc, replace(fact, confidence=100), True)
        self.assertEqual(npc.reputations[self.player.id].admiration, witnessed)

    def test_irrelevant_and_repeated_gifts_do_not_farm_trust(self):
        self.hungry()
        self.npc.hunger = 0
        self.engine.items.create(self.player.id, "wood", 5)
        before = self.engine.graph.value(self.npc.id, self.player.id, "confiança")
        for _ in range(5):
            self.engine.navigation.relocate(self.npc, self.player.position)
            item_id = self.engine.items.first(self.player.id, "wood")
            self.assertTrue(self.engine.execute(f"entregar {self.npc.id} {item_id}").success)
        self.assertEqual(self.engine.graph.value(self.npc.id, self.player.id, "confiança"), before)
        self.npc.hunger = 90
        self.engine.navigation.relocate(self.npc, self.player.position)
        food_id = self.engine.items.first(self.player.id, "food")
        self.assertTrue(self.engine.execute(f"entregar {self.npc.id} {food_id}").success)
        after = self.engine.graph.value(self.npc.id, self.player.id, "confiança")
        self.assertGreater(after, before)
        # Deixa o alimento ainda disponível, sem executar a IA do receptor.
        self.engine.quests.delivered(self.player, self.npc, "food", urgency=0)
        self.assertEqual(self.engine.graph.value(self.npc.id, self.player.id, "confiança"), after)

    def test_compassionate_npc_understands_injured_player_refusal(self):
        self.hungry()
        self.npc.hunger = 55
        quest = self.engine.quests.offer(self.npc, self.player)
        self.player.health = 20
        before = self.engine.graph.value(self.npc.id, self.player.id, "confiança")
        self.engine.quests.respond(quest.id, False)
        self.assertEqual(self.engine.graph.value(self.npc.id, self.player.id, "confiança"), before)

    def test_same_killing_is_interpreted_by_faction_and_personality(self):
        guard = self.npc
        rebel = next(c for c in self.world.characters.values() if c.faction in self.world.factions)
        self.engine.graph.set(guard.faction, rebel.faction, "diplomacia", -80)
        self.engine.graph.set(guard.id, guard.faction, "lealdade", 100)
        guard.personality = Personality(courage=100, compassion=0)
        rebel.personality = Personality(courage=0, compassion=100)
        fact = Fact(self.world.allocate_id(), "CharacterKilled", self.player.id, rebel.id,
                    None, 0, "Morte de um rebelde", context={"victim_faction": rebel.faction})
        self.engine.knowledge.learn(guard, fact, True)
        self.engine.knowledge.learn(rebel, fact, True)
        self.assertGreater(guard.reputations[self.player.id].tags.get("leal", 0), 0)
        self.assertGreater(rebel.reputations[self.player.id].tags.get("perigoso", 0), 0)

    def test_player_competes_with_other_social_candidates(self):
        self.hungry()
        other = next(c for c in self.engine.nearby() if c.id != self.npc.id)
        other.hunger = 0
        self.engine.graph.set(self.npc.id, other.id, "confiança", 100)
        self.engine.graph.set(self.npc.id, other.id, "amizade", 100)
        need = self.engine.needs.refresh(self.npc)[0]
        choices = self.engine.goals.solutions(self.npc, need)
        social = [s for s in choices if s.action == "ask_help"]
        self.assertIn(self.player.id, [s.target_id for s in social])
        self.assertEqual(social[0].target_id, other.id)

    def test_collect_and_work_require_local_resources(self):
        self.assertFalse(self.engine.execute("coletar").success)
        self.assertFalse(self.engine.execute("trabalhar").success)
        self.engine.navigation.enter(self.player)
        self.engine.navigation.relocate(self.player, self.player.known_places["forage"])
        self.town.wild_food = 0
        self.engine.items.consume(self.town.id, "grain", self.engine.items.count(self.town.id, "grain"))
        self.assertFalse(self.engine.execute("coletar").success)
        self.assertFalse(self.engine.execute("trabalhar").success)

    def test_decision_trace_explains_normalized_considerations(self):
        self.hungry()
        self.engine.goals.debug = True
        self.engine.goals.decide(self.npc)
        trace = self.engine.goals.traces[self.npc.id]
        self.assertEqual(trace["need"], "food")
        self.assertTrue(trace["candidates"])
        self.assertTrue(all(-1 <= value <= 1 for candidate in trace["candidates"]
                            for value in candidate["considerations"].values()))

    def test_known_source_is_more_persuasive_than_untrusted_rumor(self):
        other = next(c for c in self.world.characters.values() if c.id not in (self.npc.id, self.player.id))
        other.personality = replace(self.npc.personality)
        fact = Fact(self.world.allocate_id(), "HelpGiven", self.player.id, None, None, 0, "Ajuda")
        self.engine.knowledge.learn(self.npc, replace(fact, source_kind="known"), False)
        self.engine.knowledge.learn(other, replace(fact, source_kind="untrusted"), False)
        self.assertGreater(self.npc.reputations[self.player.id].admiration,
                           other.reputations[self.player.id].admiration)

    def test_debug_does_not_change_seeded_choices(self):
        restored = loads(dumps(self.world))
        other = Engine(restored)
        self.engine.goals.debug = True
        self.engine.simulate(100)
        other.simulate(100)
        self.assertEqual(dumps(self.world), dumps(restored))

    def test_pending_player_request_does_not_trap_npc(self):
        self.hungry()
        for npc in self.engine.nearby():
            if npc.id != self.npc.id:
                self.engine.navigation.relocate(npc, npc.home)
        self.npc.known_places = {"forage": self.npc.known_places["forage"]}
        self.engine.goals.decide(self.npc)
        self.assertEqual(self.npc.goal.action, "ask_help")
        self.engine.goals.decide(self.npc)
        self.assertIn(self.npc.goal.action, ("forage", "work"))

    def test_player_receives_request_during_wait_without_conversation(self):
        self.hungry()
        for npc in self.engine.nearby():
            if npc.id != self.npc.id:
                self.engine.navigation.relocate(npc, npc.home)
        self.npc.known_places = {"market": self.town.market}
        self.assertTrue(self.engine.execute("esperar 1").success)
        requests = [event for event in self.world.events if event.kind == "HelpRequested"
                    and event.actor_id == self.npc.id and event.target_id == self.player.id]
        self.assertEqual(len(requests), 1)
        self.assertEqual(requests[0].context["origin"], "autonomous")

    def test_local_market_preconditions_do_not_reveal_remote_stock(self):
        self.hungry()
        self.npc.money = 100
        self.engine.items.consume(self.town.id, "food", self.engine.items.count(self.town.id, "food"))
        need = self.engine.needs.refresh(self.npc)[0]
        self.assertNotIn("buy_food", [s.action for s in self.engine.goals.solutions(self.npc, need)])
        self.engine.navigation.relocate(self.npc, self.npc.home)
        self.assertIn("buy_food", [s.action for s in self.engine.goals.solutions(self.npc, need)])


if __name__ == "__main__":
    unittest.main()
