"""Testes de invariantes, causalidade e continuação determinística."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from procedural.engine import Engine
from procedural.generation import GenerationConfig, generate_world
from procedural.models import Fact, Location, Personality
from procedural.persistence import JsonRepository, dumps, loads
from procedural.ui import render
from procedural.validation import assert_valid


def small_world(seed="Teste", with_player=False):
    return generate_world(seed, "Hugo", with_player,
                          GenerationConfig(kingdom_count=1, historical_turns=0))


class GenerationTests(unittest.TestCase):
    def test_same_seed_same_world_and_different_seed_changes_it(self):
        a, b = small_world("Dovha"), small_world("Dovha")
        self.assertEqual(dumps(a), dumps(b))
        self.assertNotEqual(dumps(a), dumps(small_world("Mira")))
        self.assertEqual(a.characters[a.primordial_id].name, "Dovha")

    def test_seed_stable_in_separate_python_processes(self):
        script = ("import hashlib; from procedural.generation import generate_world, GenerationConfig; "
                  "from procedural.persistence import dumps; "
                  "w=generate_world('Dovha', with_player=False, config=GenerationConfig(kingdom_count=1,historical_turns=0)); "
                  "print(hashlib.sha256(dumps(w).encode()).hexdigest())")
        import os
        outputs = [subprocess.check_output([sys.executable, "-c", script],
                                           env={**os.environ, "PYTHONHASHSEED": value})
                   for value in ("1", "999")]
        self.assertEqual(*outputs)

    def test_geography_ids_and_family_consistency(self):
        world = generate_world("Geografia", with_player=False,
                               config=GenerationConfig(historical_turns=0))
        assert_valid(world)
        grid = world.maps[world.world_map_id]
        self.assertEqual((grid.width, grid.height), (500, 500))
        self.assertEqual(sum(kingdom.great for kingdom in world.kingdoms.values()), 1)
        positions = [town.position for town in world.towns.values()] + [point.position for point in world.points.values()]
        for index, position in enumerate(positions):
            for other in positions[index + 1:]:
                self.assertGreaterEqual(abs(position.x - other.x) + abs(position.y - other.y), 5)
        for kingdom in world.kingdoms.values():
            capital = world.maps[kingdom.capital_id]
            for city_id in kingdom.city_ids:
                if city_id != kingdom.capital_id:
                    self.assertGreater(capital.width, world.maps[city_id].width)
        for relation in world.relationships.values():
            if relation.kind == "casamento":
                self.assertEqual(world.characters[relation.source_id].surname,
                                 world.characters[relation.target_id].surname)


class EngineTests(unittest.TestCase):
    def setUp(self):
        self.world = small_world(with_player=True)
        self.engine = Engine(self.world)
        self.player = self.engine.player
        self.town = self.world.towns[self.player.town_id]

    def test_cardinal_movement_city_transition_and_action_clock(self):
        start = self.world.turn
        self.assertTrue(self.engine.execute("listar").success)
        self.assertFalse(self.engine.execute("mover diagonal").success)
        self.assertEqual(self.world.turn, start)
        self.assertTrue(self.engine.execute("entrar").success)
        self.assertEqual(self.player.position.map_id, self.town.id)
        gate = self.player.position
        self.assertFalse(self.engine.execute("leste").success)
        self.assertEqual(self.player.position, gate)
        self.assertEqual(self.world.turn, start + 1)
        self.assertTrue(self.engine.execute("norte").success)
        self.assertEqual(self.player.position, self.town.market)
        self.assertEqual(self.world.turn, start + 2)
        self.assertFalse(self.engine.execute("sair").success)
        self.assertTrue(self.engine.execute("sul").success)
        self.assertTrue(self.engine.execute("sair").success)
        self.assertEqual(self.player.position, self.town.position)
        visible = self.engine.view()["map"]
        self.assertEqual((len(visible), len(visible[0])), (5, 5))
        self.assertEqual(visible[2][2], "@")
        self.assertIn("MAPA 5×5", render(self.engine))

    def test_npcs_act_when_player_waits(self):
        before_actions = {p.id:dict(p.last_successful_action) for p in self.world.characters.values()}
        self.assertTrue(self.engine.execute("esperar 12").success)
        self.assertEqual(self.world.turn, 12)
        self.assertGreater(self.world.metrics.get("ItemCreated", 0), 0)
        self.assertTrue(any(npc.goal for npc in self.world.characters.values() if not npc.is_player))
        self.assertTrue(any(p.last_successful_action != before_actions[p.id]
                            for p in self.world.characters.values() if not p.is_player))
        assert_valid(self.world)

    def test_inventory_split_has_one_owner_and_trade_conserves_money(self):
        self.engine.navigation.relocate(self.player, self.town.market)
        food_before = self.engine.items.count(self.player.id, "food")
        combined_money = self.player.money + self.town.money
        stock_before = self.engine.items.count(self.town.id, "food")
        success, _ = self.engine.economy.buy(self.player.id, self.town.id, "food", 2)
        self.assertTrue(success)
        self.assertEqual(self.player.money + self.town.money, combined_money)
        self.assertEqual(self.engine.items.count(self.player.id, "food"), food_before + 2)
        self.assertEqual(self.engine.items.count(self.town.id, "food"), stock_before - 2)
        assert_valid(self.world)
        success, _ = self.engine.economy.buy(self.player.id, self.town.id, "food", 100000)
        self.assertFalse(success)
        # Uma consulta malsucedida pode aumentar demanda, mas nunca muda dinheiro ou posse.
        self.assertEqual(self.player.money + self.town.money, combined_money)
        self.assertEqual(self.engine.items.count(self.player.id, "food"), food_before + 2)

    def test_smith_requires_and_consumes_materials(self):
        smith = next(npc for npc in self.world.characters.values() if npc.profession == "ferreiro")
        town = self.world.towns[smith.town_id]
        self.engine.navigation.relocate(smith, smith.workplace)
        iron = self.engine.items.count(town.id, "iron")
        wood = self.engine.items.count(town.id, "wood")
        weapons = self.engine.items.count(town.id, "weapon")
        success, _ = self.engine.professions.work(smith)
        self.assertTrue(success)
        self.assertEqual(self.engine.items.count(town.id, "iron"), iron - 2)
        self.assertEqual(self.engine.items.count(town.id, "wood"), wood - 1)
        self.assertEqual(self.engine.items.count(town.id, "weapon"), weapons + 1)
        self.engine.items.consume(town.id, "iron", iron - 2)
        success, _ = self.engine.professions.work(smith)
        self.assertFalse(success)
        self.assertEqual(self.engine.items.count(town.id, "weapon"), weapons + 1)

    def test_same_hunger_produces_different_solutions(self):
        npc = next(npc for npc in self.world.characters.values() if npc.profession == "agricultor")
        self.engine.navigation.relocate(npc, self.world.towns[npc.town_id].market)
        self.engine.items.consume(npc.id, "food", self.engine.items.count(npc.id, "food"))
        npc.money, npc.hunger, npc.thirst, npc.fatigue = 0, 90, 0, 0
        npc.personality = Personality(honesty=0, greed=100, compassion=0, independence=0, courage=100)
        self.engine.goals.decide(npc)
        self.assertEqual(npc.goal.action, "steal")
        self.assertEqual(self.world.metrics["ItemStolen"], 1)
        self.engine.items.consume(npc.id, "food", self.engine.items.count(npc.id, "food"))
        npc.personality = Personality(honesty=100, independence=100, compassion=0)
        self.engine.goals.decide(npc)
        self.assertEqual(npc.goal.action, "forage")

    def test_competing_thirst_and_hunger_do_not_cause_endless_travel(self):
        npc = next(npc for npc in self.world.characters.values() if npc.profession == "caçador")
        self.engine.items.consume(npc.id, "food", self.engine.items.count(npc.id, "food"))
        npc.money, npc.hunger, npc.thirst = 0, 90, 90
        npc.personality = Personality(honesty=100, diligence=0, independence=100, compassion=0)
        self.engine.navigation.relocate(npc, npc.known_places["forage"])
        for _ in range(200):
            self.world.turn += 1
            self.engine.needs.physiology(npc)
            self.engine.goals.decide(npc)
            if npc.health == 0:
                self.fail("NPC morreu alternando necessidades apesar de comida e água acessíveis.")
        self.assertGreater(self.world.metrics.get("FoodEaten", 0), 0)

    def test_unpaid_work_cannot_trap_hungry_npc_in_a_loop(self):
        npc = next(npc for npc in self.world.characters.values() if npc.profession == "comerciante")
        town = self.world.towns[npc.town_id]
        town.money = 0
        self.engine.navigation.relocate(npc, npc.workplace)
        self.engine.items.consume(npc.id, "food", self.engine.items.count(npc.id, "food"))
        npc.money, npc.hunger, npc.thirst, npc.fatigue = 0, 90, 0, 0
        npc.personality = Personality(honesty=100, diligence=100, independence=0, compassion=0)
        self.engine.goals.decide(npc)
        self.assertNotEqual(npc.goal.action, "work")
        self.assertTrue(any(row['reason_code']=='NO_PAYER' for row in
            self.world.observability.decisions[self.world.observability.last_decision_ids[npc.id]].blocked_actions))
        self.engine.goals.decide(npc)
        self.assertNotEqual(npc.goal.action, "work")


class KnowledgeAndQuestTests(unittest.TestCase):
    def setUp(self):
        self.world = small_world(with_player=True)
        self.engine = Engine(self.world)

    def test_unwitnessed_crime_does_not_create_remote_reputation(self):
        npcs = [npc for npc in self.world.characters.values() if not npc.is_player]
        actor, remote = npcs[:2]
        remote.knowledge.clear()
        remote.reputations.clear()
        self.engine.navigation.relocate(actor, Location(actor.town_id, 3, 3))
        self.engine.navigation.relocate(remote, Location(remote.town_id, 1, 1))
        event = self.engine.recorder.emit("ItemStolen", "Roubo que não foi visto à distância.",
                                          actor.id, actor.town_id, actor.position)
        self.assertIn(event.id, actor.knowledge)
        self.assertNotIn(event.id, remote.knowledge)
        self.assertNotIn(actor.id, remote.reputations)

    def test_rumor_travels_only_one_contact_per_round(self):
        npcs = [npc for npc in self.world.characters.values() if not npc.is_player]
        a, b, c = npcs[:3]
        for npc in npcs:
            npc.knowledge.clear()
            self.engine.navigation.relocate(npc, Location(npc.town_id, 1, 1))
        for npc, x in ((a, 4), (b, 5), (c, 6)):
            self.engine.navigation.relocate(npc, Location(a.town_id, x, 5))
        event = self.engine.recorder.emit("ItemStolen", "Notícia localizada.", a.id, a.town_id, a.position)
        self.assertNotIn(event.id, b.knowledge)
        self.assertNotIn(event.id, c.knowledge)
        self.engine.knowledge.gossip()
        self.assertIn(event.id, b.knowledge)
        self.assertNotIn(event.id, c.knowledge)

    def test_dialogue_does_not_leak_secret_or_unknown_world_state(self):
        npc = next(npc for npc in self.world.characters.values() if not npc.is_player)
        player = self.engine.player
        npc.knowledge.clear()
        secret = Fact(987654, "FoodShortage", None, None, npc.position, 0,
                      "A reserva secreta fica no templo.", required_trust=90)
        npc.knowledge[secret.event_id] = secret
        text = self.engine.knowledge.dialogue(npc, player)
        self.assertNotIn("reserva secreta", text)
        self.assertNotIn(secret.event_id, player.knowledge)
        self.engine.graph.set(npc.id, player.id, "confiança", 95)
        text = self.engine.knowledge.dialogue(npc, player)
        self.assertIn("reserva secreta", text)
        self.assertIn(secret.event_id, player.knowledge)

    def prepare_request(self):
        player = self.engine.player
        npc = next(npc for npc in self.world.characters.values() if npc.profession == "agricultor")
        self.engine.navigation.relocate(player, npc.position)
        self.engine.items.consume(npc.id, "food", self.engine.items.count(npc.id, "food"))
        npc.hunger, npc.money = 75, 0
        npc.personality = Personality(compassion=100, independence=0)
        self.engine.graph.set(npc.id, player.id, "confiança", 60)
        return npc, player

    def test_quest_is_backed_by_need_and_refusal_preserves_it(self):
        npc, player = self.prepare_request()
        quest = self.engine.quests.offer(npc, player)
        self.assertIsNotNone(quest)
        self.assertEqual(quest.need_id, npc.needs["food"].id)
        success, _ = self.engine.quests.respond(quest.id, False)
        self.assertTrue(success)
        self.assertEqual(quest.status, "declined")
        self.assertNotEqual(npc.needs["food"].status, "satisfied")
        self.assertGreater(npc.hunger, 50)

    def test_delivering_real_food_completes_accepted_quest(self):
        npc, player = self.prepare_request()
        quest = self.engine.quests.offer(npc, player)
        self.engine.quests.respond(quest.id, True)
        food_id = self.engine.items.first(player.id, "food")
        before = self.engine.items.count(player.id, "food")
        result = self.engine.execute(f"entregar {npc.id} {food_id}")
        self.assertTrue(result.success)
        self.assertEqual(quest.status, "completed")
        self.assertEqual(self.engine.items.count(player.id, "food"), before - 1)
        self.assertGreater(self.engine.graph.value(npc.id, player.id, "confiança"), 60)
        assert_valid(self.world)


class PersistenceAndStabilityTests(unittest.TestCase):
    def test_load_continues_exact_simulation_including_rng(self):
        world = small_world("Continuação")
        engine = Engine(world)
        engine.simulate(80)
        restored = loads(dumps(world))
        self.assertEqual(dumps(world), dumps(restored))
        engine.simulate(200)
        Engine(restored).simulate(200)
        self.assertEqual(dumps(world), dumps(restored))
        assert_valid(restored)

    def test_atomic_file_save_and_corruption_detection(self):
        repository = JsonRepository()
        world = small_world()
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "campanha.json"
            repository.save(world, path)
            self.assertEqual(dumps(repository.load(path)), dumps(world))
            document = json.loads(path.read_text())
            document["format_version"] = 999
            with self.assertRaises(ValueError):
                loads(json.dumps(document))
            invalid = loads(dumps(world))
            next(iter(invalid.characters.values())).money = -1
            with self.assertRaises(ValueError):
                loads(dumps(invalid))

    def test_world_stays_valid_and_memory_is_bounded_over_many_days(self):
        for seed in ("Dovha", "Mira", "Arven"):
            with self.subTest(seed=seed):
                world = small_world(seed)
                engine = Engine(world)
                engine.simulate(240)
                early_items = len(world.items)
                for _ in range(5):
                    engine.simulate(240)
                    assert_valid(world)
                self.assertLessEqual(len(world.items), early_items + len(world.towns) * 8)
                self.assertTrue(any(character.alive for character in world.characters.values()))
                self.assertLessEqual(len(world.events), 256)


if __name__ == "__main__":
    unittest.main()
