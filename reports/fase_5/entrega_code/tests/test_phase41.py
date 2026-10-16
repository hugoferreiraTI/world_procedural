"""Dez regressões compostas para sobrevivência, recuperação e origem de dano."""
import unittest
from procedural.engine import Engine
from procedural.generation import GenerationConfig, generate_world
from procedural.models import Goal, Personality
from procedural.persistence import dumps, loads
from procedural.validation import assert_valid
from procedural.rules import FEEDING, RECOVERY


class Phase41Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.template=dumps(generate_world('Fase41', with_player=False,
            config=GenerationConfig(kingdom_count=1,historical_turns=0)))

    def setUp(self):
        self.world=loads(self.template);self.engine=Engine(self.world)
        self.p=next(p for p in self.world.characters.values() if p.profession=='agricultor')
        self.town=self.world.towns[self.p.town_id]
        self.q=next(q for q in self.world.characters.values() if q.town_id==self.p.town_id and q.profession=='comerciante')
        for p in self.world.characters.values():self.engine.navigation.relocate(p,p.home)
        for p in (self.p,self.q):
            self.engine.navigation.relocate(p,self.town.market)
            p.hunger=p.thirst=p.fatigue=0;p.health=100;p.needs.clear();p.goal=None
        self.p.personality=Personality(honesty=0,greed=100,diligence=50)
        self.engine.goals.debug=True

    def action(self, action, target=None, need=None):
        return self.engine.goals.execute(self.p,Goal(self.world.allocate_id(),need.id if need else 0,
            action,0,self.world.turn,target),1)

    def test_01_person_acquisition_consumes_real_item_before_fatal_close(self):
        self.p.health=1;self.p.hunger=100;self.p.money=0
        self.engine.items.consume(self.p.id,'food',self.engine.items.count(self.p.id,'food'))
        self.engine.items.create(self.q.id,'food',1)
        need=next(n for n in self.engine.needs.refresh(self.p) if n.kind=='food')
        choices=self.engine.goals.solutions(self.p,need)
        self.assertNotIn('steal_person',[c.action for c in choices])
        self.assertIn('person_meal',[c.action for c in choices])
        before=self.engine.items.count(self.q.id,'food');hp=self.p.health
        self.assertTrue(self.action('person_meal',self.q.id,need)[0])
        self.assertEqual(before-1,self.engine.items.count(self.q.id,'food'))
        self.assertEqual(0,self.engine.items.count(self.p.id,'food'))
        self.assertEqual(60,self.p.hunger);self.assertEqual(hp,self.p.health)
        self.engine.needs.physiology(self.p);self.assertEqual(1,self.p.health)
        self.assertEqual(1,self.world.metrics['FoodEaten'])

    def test_02_purchase_chain_preserves_transfer_and_no_healing(self):
        self.p.hunger=100;self.p.health=1;self.p.money=100
        before=self.engine.items.count(self.town.id,'food');money=self.p.money
        self.assertTrue(self.action('buy_meal')[0])
        self.assertEqual(before-1,self.engine.items.count(self.town.id,'food'))
        self.assertLess(self.p.money,money);self.assertEqual(1,self.p.health)
        self.engine.needs.physiology(self.p);self.assertEqual(1,self.p.health)

    def test_03_early_meal_is_valid_without_becoming_emergency(self):
        self.p.hunger=36
        need=next(n for n in self.engine.needs.refresh(self.p) if n.kind=='food')
        self.assertIn('eat',[c.action for c in self.engine.goals.solutions(self.p,need)])
        self.assertFalse(need.context['emergency']);self.assertLess(need.priority,60)

    def test_04_no_meal_pressure_at_fifteen_and_reserve_separate(self):
        self.p.hunger=15
        active=self.engine.needs.refresh(self.p)
        self.assertNotIn('food',[n.kind for n in active])
        self.assertEqual(2,self.engine.feeding.reserve_target(self.p))

    def test_05_actual_deprivation_damage_tracks_only_real_loss(self):
        self.p.hunger=100;self.p.thirst=0
        for _ in range(10):self.engine.needs.physiology(self.p)
        self.assertEqual(80,self.p.health);self.assertEqual(20,self.p.recoverable_deprivation_damage)
        self.assertEqual(20,self.p.damage_by_origin['hunger'])
        self.p.health=1;self.p.recoverable_deprivation_damage=0
        self.engine.needs.physiology(self.p)
        self.assertEqual(1,self.p.recoverable_deprivation_damage)

    def test_06_recovery_ends_and_material_despair_falls_gradually(self):
        self.engine.recovery.damage(self.p,40,'hunger')
        self.engine.navigation.relocate(self.p,self.p.home)
        self.p.money=25
        self.engine.items.create(self.p.id,'water',3)
        self.p.emotions.desperation=60;self.p.emotions.despair_sources={'poverty':40,'grief':20}
        self.p.emotions.last_updated=100
        for hour in range(1,13):
            self.world.turn=hour+100
            self.engine.goals.decide(self.p,1)
            self.engine.needs.physiology(self.p)
        self.assertGreaterEqual(self.p.health,80)
        self.assertLess(self.p.recoverable_deprivation_damage,40)
        self.assertNotIn('recovery',[n.kind for n in self.engine.needs.refresh(self.p)])
        self.assertLess(self.p.emotions.desperation,60)
        self.assertGreater(self.p.emotions.despair_sources.get('grief',0),0)

    def test_07_attack_does_not_enter_fast_healing_ledger(self):
        self.engine.recovery.damage(self.p,30,'combat');self.p.combat.injured=30
        self.engine.navigation.relocate(self.p,self.p.home)
        self.assertEqual(0,self.p.recoverable_deprivation_damage)
        self.engine.needs.rest(self.p,1)
        self.assertEqual(73,self.p.health);self.assertEqual(28,self.p.combat.injured)

    def test_08_mixed_damage_caps_fast_recovery_and_no_double_heal(self):
        self.engine.recovery.damage(self.p,30,'hunger');self.engine.recovery.damage(self.p,20,'combat')
        self.engine.navigation.relocate(self.p,self.p.home)
        self.engine.needs.rest(self.p,1);self.assertEqual(58,self.p.health)
        for _ in range(3):self.engine.needs.rest(self.p,1)
        self.assertEqual(0,self.p.recoverable_deprivation_damage)
        self.assertEqual(30,self.world.metrics['Recovery:DeprivationHealed'])
        self.assertLess(self.p.health,100)
        self.p.hunger=90;hp=self.p.health;self.engine.needs.rest(self.p,1);self.assertEqual(hp,self.p.health)

    def test_09_save_load_preserves_recovery_and_continuation(self):
        self.engine.recovery.damage(self.p,40,'hunger')
        self.engine.needs.refresh(self.p)
        restored=Engine(loads(dumps(self.world)))
        r=restored.world.characters[self.p.id]
        self.assertEqual(40,r.recoverable_deprivation_damage)
        self.assertEqual(self.p.needs['recovery'],r.needs['recovery'])
        self.assertEqual(self.p.damage_by_origin,r.damage_by_origin)
        self.engine.simulate(12);restored.simulate(12)
        self.assertEqual(dumps(self.world),dumps(restored.world));assert_valid(self.world)

    def test_10_lod_promotes_once_and_critical_recovery_interrupts_work(self):
        self.engine.navigation.relocate(self.p,self.p.home)
        self.p.hunger=0;self.assertEqual(12,self.engine.feeding.decision_interval(self.p))
        self.p.hunger=36;self.assertEqual(3,self.engine.feeding.decision_interval(self.p))
        self.p.hunger=10;self.engine.recovery.damage(self.p,88,'hunger')
        self.assertEqual(1,self.engine.feeding.decision_interval(self.p))
        need=self.engine.needs.ensure(self.p,'money',35,'fixture','Trabalho em curso')
        self.p.goal=Goal(self.world.allocate_id(),need.id,'work',60,self.world.turn,destination=self.p.workplace)
        self.engine.goals.decide(self.p,1)
        self.assertEqual('recovery',self.engine.goals.traces[self.p.id]['need'])
        self.assertEqual('sleep',self.p.goal.action);self.assertEqual(20,self.p.health)
