"""Regressões e contratos comportamentais da fase_2.md."""

from dataclasses import replace
import unittest

from procedural.engine import Engine
from procedural.models import Fact, Location, Personality
from procedural.persistence import dumps, loads
from procedural.utility import evaluate
from procedural.validation import assert_valid
from test_simulation import small_world


class Phase2BugTests(unittest.TestCase):
    def setUp(self):
        self.world = small_world("Fase2", with_player=True)
        self.engine = Engine(self.world)
        self.player = self.engine.player
        self.town = self.world.towns[self.player.town_id]
        self.npc = next(c for c in self.world.characters.values()
                        if c.town_id == self.town.id and c.profession == "agricultor")

    def test_player_and_npc_follow_same_survival_timing(self):
        for person in (self.player, self.npc):
            self.engine.navigation.relocate(person, self.town.market)
            person.health, person.hunger, person.thirst, person.fatigue = 1, 100, 0, 0
            self.engine.items.create(person.id, "food", 2)
        self.assertTrue(self.engine.execute("comer").success)
        self.assertTrue(self.player.alive)
        self.assertEqual(self.player.alive, self.npc.alive)
        self.assertEqual(self.player.health, self.npc.health)
        self.assertEqual(self.player.hunger, self.npc.hunger)

    def test_food_help_uses_real_affordability(self):
        self.engine.navigation.relocate(self.player, self.town.market)
        self.engine.navigation.relocate(self.npc, self.town.market)
        for c in self.engine.nearby():
            if c.id != self.npc.id:
                self.engine.navigation.relocate(c, c.home)
        self.engine.items.consume(self.npc.id, "food", self.engine.items.count(self.npc.id, "food"))
        self.engine.items.consume(self.town.id, "food", self.engine.items.count(self.town.id, "food"))
        self.engine.items.create(self.town.id, "food")
        self.npc.money, self.npc.hunger = 10, 90
        self.npc.personality = Personality(compassion=100, independence=0, honesty=100)
        self.engine.graph.set(self.npc.id, self.player.id, "confiança", 80)
        self.assertEqual(self.engine.economy.price(self.town.id, "food"), 14)
        need = self.engine.needs.refresh(self.npc)[0]
        self.assertNotIn("buy_food", [s.action for s in self.engine.goals.solutions(self.npc, need)])
        self.assertIsNotNone(self.engine.quests.offer(self.npc, self.player))

    def test_invalid_action_has_no_persistent_effect(self):
        for command in ("coletar", "trabalhar", "comer"):
            if command == "comer":
                self.engine.items.consume(self.player.id, "food", self.engine.items.count(self.player.id, "food"))
            before = dumps(self.world)
            self.assertFalse(self.engine.execute(command).success)
            self.assertEqual(dumps(self.world), before, command)

    def test_stronger_evidence_updates_existing_fact_without_duplicate_reputation(self):
        for c in self.world.characters.values():
            self.engine.navigation.relocate(c, c.home)
            c.knowledge.clear()
        self.engine.navigation.relocate(self.npc, Location(self.town.id, 4, 4))
        self.engine.navigation.relocate(self.player, Location(self.town.id, 5, 4))
        self.engine.graph.set(self.player.id, self.npc.id, "confiança", 95)
        fact = Fact(self.world.allocate_id(), "HelpGiven", self.npc.id, self.player.id,
                    self.npc.position, 0, "Ajuda real", context={"urgency": 90})
        self.engine.knowledge.learn(self.npc, fact, True)
        self.engine.knowledge.learn(self.player, replace(fact, confidence=30), False)
        self.engine.knowledge.gossip()
        self.assertEqual(self.player.knowledge[fact.event_id].confidence, 80)
        before = self.player.reputations[self.npc.id].tags.copy()
        self.engine.knowledge.gossip()
        self.assertEqual(self.player.reputations[self.npc.id].tags, before)


class Phase2BehaviorTests(unittest.TestCase):
    def setUp(self):
        self.world = small_world("ComportamentoFase2", with_player=True)
        self.engine = Engine(self.world)
        self.player = self.engine.player
        self.town = self.world.towns[self.player.town_id]
        self.npc = next(c for c in self.world.characters.values()
                        if c.town_id == self.town.id and c.profession == "agricultor")
        self.relative = next(c for c in self.world.characters.values()
                             if c.town_id == self.town.id and c.profession == "cozinheiro")
        self.npc.personality = Personality(ambition=0, family_loyalty=90)
        self.npc.hunger, self.npc.thirst, self.npc.fatigue, self.npc.money = 0, 0, 0, 30
        self.relative.hunger, self.relative.thirst = 0, 0
        self.engine.navigation.relocate(self.npc, self.town.market)
        self.engine.navigation.relocate(self.relative, self.town.market)
        self.engine.navigation.relocate(self.player, self.town.market)
        self.engine.graph.set(self.npc.id, self.player.id, "confiança", 80)

    def death(self, known=True, killer=None, violent=False):
        self.relative.alive, self.relative.health = False, 0
        self.engine.spatial.positions[self.relative.position].discard(self.relative.id)
        if not known:
            self.engine.navigation.relocate(self.npc, self.npc.home)
        return self.engine.recorder.emit("CharacterKilled" if violent else "CharacterDied", "Morte real em fixture.",
                                         killer, self.relative.id, self.relative.position, historical=True)

    def test_personality_generation_is_seed_deterministic(self):
        self.assertEqual(dumps(small_world("Traços")), dumps(small_world("Traços")))
        personalities = [c.personality for c in self.world.characters.values() if not c.is_player]
        self.assertGreater(len({p.ambition for p in personalities}), 1)
        self.assertGreater(len({p.vengefulness for p in personalities}), 1)

    def test_new_traits_and_observations_survive_save_load(self):
        self.engine.needs.refresh(self.npc)
        self.npc.personality.temperament = 93
        self.npc.personality.vengefulness = 86
        self.npc.personality.ambition = 79
        restored = loads(dumps(self.world))
        self.assertEqual(restored.characters[self.npc.id].personality, self.npc.personality)
        self.assertEqual(restored.characters[self.npc.id].observations, self.npc.observations)
        assert_valid(restored)

    def test_low_honesty_does_not_require_duplicate_falsehood_trait(self):
        self.npc.personality.honesty = 0
        self.assertFalse(hasattr(self.npc.personality, "falsehood"))
        self.assertFalse(hasattr(self.npc.personality, "family_orientation"))

    def test_family_relationship_can_generate_executable_family_need(self):
        self.relative.hunger = 90
        self.engine.items.create(self.npc.id, "food", 3)
        before = self.engine.items.count(self.relative.id, "food")
        self.engine.goals.decide(self.npc)
        need = self.npc.needs[f"family:{self.relative.id}"]
        self.assertEqual(self.npc.goal.action, "give_supplies")
        self.assertEqual(need.status, "satisfied")
        self.assertEqual(self.engine.items.count(self.relative.id, "food"), before + 1)
        self.assertTrue(need.source.startswith("event:"))

    def test_family_absence_requires_previous_observation(self):
        self.engine.navigation.relocate(self.relative, self.relative.home)
        self.world.turn = 100
        self.engine.needs.refresh(self.npc)
        self.assertNotIn(f"family:{self.relative.id}", self.npc.needs)
        self.engine.navigation.relocate(self.relative, self.npc.position)
        self.engine.needs.refresh(self.npc)
        self.engine.navigation.relocate(self.relative, self.relative.home)
        self.world.turn += 40
        self.engine.needs.refresh(self.npc)
        self.assertEqual(self.npc.needs[f"family:{self.relative.id}"].context["mode"], "missing")

    def test_unknown_death_does_not_generate_grief(self):
        self.death(known=False)
        self.engine.needs.refresh(self.npc)
        self.assertFalse(any(n.kind == "grief" for n in self.npc.needs.values()))

    def test_known_close_relative_death_can_generate_grief(self):
        self.death()
        need = self.npc.needs[f"grief:{self.relative.id}"]
        self.assertIsNotNone(need.expires_at)
        self.assertTrue(need.context["family"])
        choices = self.engine.goals.solutions(self.npc, need)
        self.assertIn("remember_relative", [s.action for s in choices])
        self.engine.goals.decide(self.npc)
        self.assertIn(self.npc.goal.action, ("seek_company", "remember_relative", "ask_personal_help"))

    def test_same_death_does_not_duplicate_grief_need_after_forgetting(self):
        event = self.death()
        before = self.world.next_id
        fact = self.npc.knowledge[event.id]
        self.npc.knowledge.clear()
        self.engine.knowledge.learn(self.npc, fact, True)
        self.assertEqual(self.world.next_id, before)
        self.assertEqual(sum(n.kind == "grief" for n in self.npc.needs.values()), 1)

    def test_vengefulness_changes_revenge_utility(self):
        self.npc.personality.vengefulness = 0
        low = evaluate("investigate", self.npc)[0]
        self.npc.personality.vengefulness = 100
        self.assertGreater(evaluate("investigate", self.npc)[0], low)

    def test_low_courage_reduces_direct_investigation_preference(self):
        self.npc.personality.courage = 0
        low = evaluate("investigate", self.npc)[0]
        self.npc.personality.courage = 100
        self.assertGreater(evaluate("investigate", self.npc)[0], low)

    def test_revenge_requires_known_or_believed_target(self):
        self.death(violent=True)
        need = next(n for n in self.npc.needs.values() if n.kind == "revenge")
        self.assertIsNone(need.target_id)
        self.assertNotIn("investigate", [s.action for s in self.engine.goals.solutions(self.npc, need)])
        fact = Fact(self.world.allocate_id(), "CharacterKilled", self.player.id, self.relative.id,
                    self.town.market, self.world.turn, "Responsável identificado.")
        self.engine.knowledge.learn(self.npc, fact, True)
        self.assertTrue(any(n.kind == "revenge" and n.target_id == self.player.id for n in self.npc.needs.values()))
        self.assertNotIn("attack", [s.action for s in self.engine.goals.solutions(self.npc, need)])

    def test_protection_need_uses_known_threat(self):
        fact = Fact(self.world.allocate_id(), "ItemStolen", self.player.id, self.town.id,
                    self.npc.home, self.world.turn, "Crime na residência conhecida.")
        self.engine.needs.refresh(self.npc)
        self.assertFalse(any(n.kind == "protection" for n in self.npc.needs.values()))
        self.engine.knowledge.learn(self.npc, fact, True)
        need = next(n for n in self.npc.needs.values() if n.kind == "protection")
        self.assertEqual(need.context["scope"], "home")
        self.assertTrue(self.engine.goals.solutions(self.npc, need))

    def test_financial_pressure_reuses_existing_money_work_system(self):
        self.world.turn = 60
        self.npc.financial_since, self.npc.money = 0, 1
        self.engine.needs.refresh(self.npc)
        self.assertEqual(self.npc.needs["money"].context["money_target"], 20)
        self.assertIn("Estabilizar", self.npc.needs["money"].reason)
        self.assertFalse(any(n.kind in ("income", "financial", "money2") for n in self.npc.needs.values()))
        self.engine.items.create(self.npc.id, "grain", 3)
        self.assertIn("sell_surplus", [s.action for s in self.engine.goals.solutions(self.npc, self.npc.needs["money"])])

    def test_status_need_does_not_directly_increase_popularity(self):
        self.npc.personality.ambition = 100
        before = {i: dict(c.reputations) for i, c in self.world.characters.items()}
        self.engine.needs.refresh(self.npc)
        self.assertIn("status", self.npc.needs)
        self.assertEqual({i: dict(c.reputations) for i, c in self.world.characters.items()}, before)
        self.assertIn("work", [s.action for s in self.engine.goals.solutions(self.npc, self.npc.needs["status"])])

    def test_ambition_trait_can_strengthen_advancement_pressure(self):
        self.npc.personality.ambition = 70
        self.engine.needs.refresh(self.npc)
        need = self.npc.needs["advancement"]
        low = need.priority
        self.npc.personality.ambition = 100
        self.engine.needs.refresh(self.npc)
        self.assertGreater(need.priority, low)
        self.assertGreater(need.context["money_target"], self.npc.money)

    def test_nonphysiological_need_can_beat_mild_hunger(self):
        self.npc.hunger, self.relative.hunger = 25, 90
        self.engine.items.create(self.npc.id, "food", 3)
        self.engine.goals.decide(self.npc)
        selected = next(n for n in self.npc.needs.values() if n.id == self.npc.goal.need_id)
        self.assertEqual(selected.kind, "family")

    def test_critical_survival_need_can_beat_low_priority_ambition(self):
        self.npc.hunger, self.npc.personality.ambition = 100, 100
        self.engine.goals.decide(self.npc)
        self.assertEqual(self.npc.goal.action, "eat")

    def test_new_need_can_create_existing_emergent_quest_flow(self):
        self.engine.needs.refresh(self.npc)
        self.engine.navigation.relocate(self.relative, self.relative.home)
        self.world.turn += 40
        self.engine.needs.refresh(self.npc)
        need = self.npc.needs[f"family:{self.relative.id}"]
        quest = self.engine.quests.offer(self.npc, self.player, need=need)
        self.assertIsNotNone(quest)
        self.assertEqual(quest.kind, "family")
        self.assertTrue(self.engine.quests.respond(quest.id, True)[0])
        self.engine.navigation.relocate(self.player, self.relative.home)
        self.assertTrue(self.engine.execute(f"investigar {self.relative.id}").success)
        fact = next(f for f in reversed(list(self.player.knowledge.values())) if f.kind == "PersonLocated")
        self.engine.navigation.relocate(self.player, self.npc.position)
        self.assertTrue(self.engine.execute(f"informar {self.npc.id} {fact.event_id}").success)
        self.assertEqual(quest.status, "completed")

    def test_unresolvable_need_can_become_blocked_and_expire(self):
        self.npc.profession = "estudante"
        self.npc.personality.ambition = 100
        self.engine.needs.refresh(self.npc)
        need = self.npc.needs["advancement"]
        self.engine.goals.decide(self.npc)
        self.assertEqual(need.status, "blocked")
        self.world.turn = need.expires_at
        self.engine.needs.refresh(self.npc)
        self.assertEqual(need.status, "expired")

    def test_same_seed_produces_same_decisions_with_personal_state(self):
        self.death()
        other = loads(dumps(self.world))
        self.engine.goals.debug = True
        self.engine.simulate(100)
        Engine(other).simulate(100)
        self.assertEqual(dumps(self.world), dumps(other))
        trace = self.engine.goals.traces[self.npc.id]
        self.assertIn("active_needs", trace)
        self.assertIn("source", trace)

    def test_invalid_personal_commands_have_no_persistent_effect(self):
        for command in ("investigar 999999", f"informar {self.npc.id} 999999", f"acompanhar {self.npc.id}"):
            before = dumps(self.world)
            self.assertFalse(self.engine.execute(command).success)
            self.assertEqual(dumps(self.world), before)

    def test_stale_location_does_not_resolve_new_absence(self):
        self.engine.needs.refresh(self.npc)
        self.engine.navigation.relocate(self.relative, self.relative.home)
        self.world.turn = 40
        self.engine.needs.refresh(self.npc)
        need = self.npc.needs[f"family:{self.relative.id}"]
        fact = Fact(self.world.allocate_id(), "PersonLocated", self.player.id, self.relative.id,
                    self.town.market, 0, "Encontro antigo.")
        self.engine.knowledge.learn(self.npc, fact, True)
        self.assertNotEqual(need.status, "satisfied")

    def test_local_remains_can_close_family_search_and_generate_known_grief(self):
        self.engine.needs.refresh(self.npc)
        self.engine.navigation.relocate(self.relative, self.relative.home)
        self.world.turn = 40
        self.engine.needs.refresh(self.npc)
        need = self.npc.needs[f"family:{self.relative.id}"]
        self.relative.alive, self.relative.health = False, 0
        self.engine.spatial.positions[self.relative.home].discard(self.relative.id)
        self.engine.navigation.relocate(self.npc, self.relative.home)
        self.assertTrue(self.engine.personal_actions.locate(self.npc, self.relative.id)[0])
        self.assertEqual(need.status, "satisfied")
        grief = self.npc.needs[f"grief:{self.relative.id}"]
        count = self.world.metrics["NPCNeedCreated:grief"]
        self.engine.personal_actions.locate(self.npc, self.relative.id)
        self.assertEqual(self.world.metrics["NPCNeedCreated:grief"], count)
        self.assertEqual(self.npc.needs[f"grief:{self.relative.id}"].id, grief.id)

    def test_old_death_information_can_complete_current_family_quest(self):
        self.engine.needs.refresh(self.npc)
        self.engine.navigation.relocate(self.relative, self.relative.home)
        fact = Fact(self.world.allocate_id(), "CharacterDied", None, self.relative.id,
                    self.relative.home, 0, "Morte conhecida pelo jogador.")
        self.engine.knowledge.learn(self.player, fact, True)
        self.relative.alive, self.relative.health = False, 0
        self.engine.spatial.positions[self.relative.home].discard(self.relative.id)
        self.world.turn = 40
        self.engine.needs.refresh(self.npc)
        quest = self.engine.quests.offer(self.npc, self.player, need=self.npc.needs[f"family:{self.relative.id}"])
        self.assertIsNotNone(quest)
        self.engine.quests.respond(quest.id, True)
        self.assertTrue(self.engine.personal_actions.inform(self.player, self.npc, fact)[0])
        self.assertEqual(quest.status, "completed")

    def test_observed_reputation_can_trigger_status_without_important_category(self):
        self.engine.navigation.relocate(self.npc, self.npc.home)
        self.engine.navigation.relocate(self.relative, self.npc.home)
        self.npc.personality.ambition = 100
        from procedural.models import Reputation
        self.npc.reputations[self.relative.id] = Reputation(admiration=40)
        self.engine.needs.refresh(self.npc)
        self.assertEqual(self.npc.needs["status"].context["role_model"], self.relative.id)

    def test_personal_response_cannot_be_transmitted_between_maps(self):
        self.relative.hunger = 90
        self.engine.needs.refresh(self.npc)
        quest = self.engine.quests.offer(self.npc, self.player, need=self.npc.needs[f"family:{self.relative.id}"])
        self.assertIsNotNone(quest)
        self.engine.navigation.relocate(self.player, self.town.position)
        before = dumps(self.world)
        self.assertFalse(self.engine.execute(f"recusar {quest.id}").success)
        self.assertEqual(dumps(self.world), before)


if __name__ == "__main__":
    unittest.main()
