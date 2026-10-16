"""Dez testes focados, em quatro famílias controladas; não são lore natural."""
import unittest
from procedural.engine import Engine
from procedural.generation import generate_world,GenerationConfig
from procedural.models import Fact,Goal,Grievance
from procedural.persistence import dumps,loads
from procedural.validation import validate_world
from procedural.religious_health import ReligiousHealth

class Phase52Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.template=dumps(generate_world('Neravien-52-controle',with_player=False,
            config=GenerationConfig(kingdom_count=1,historical_turns=0)))
    def setUp(self):
        self.w=loads(self.template);self.e=Engine(self.w);self.w.turn=96
        self.t=next(t for t in self.w.towns.values() if t.mayor_id)
        people=[self.w.characters[i] for i in self.t.resident_ids if i!=self.t.mayor_id and self.w.characters[i].category=='comum']
        self.p,self.q,self.r,self.s=people[:4]
        for i in self.e.spatial.at(self.t.market):self.e.navigation.relocate(self.w.characters[i],self.w.characters[i].home)
        for p in (self.p,self.q,self.r,self.s):
            self.e.navigation.relocate(p,self.t.market);p.health=100;p.hunger=p.thirst=p.fatigue=10
            p.personality.compassion=5;p.personality.honesty=10;p.personality.courage=95
            p.personality.persistence=p.personality.vengefulness=90;p.personality.sadism=0
        for kind in ('amizade','casamento','pai_de','filho_de'):self.e.graph.set(self.p.id,self.q.id,kind,0)
        self.e.items.create(self.p.id,'weapon');self.e.conflicts.observe(self.p)
        self.god=next(iter(self.w.divinities.values()))
    def act(self,p,n,a,target):return self.e.goals.execute(p,Goal(self.w.allocate_id(),n.id,a,0,self.w.turn,target),1)
    def fact(self,kind,actor,target,context=None,location=None):
        return Fact(self.w.allocate_id(),kind,actor,target,location or self.t.market,self.w.turn,'Fato controlado',source_kind='direct',context=context or {})
    def moderate(self):
        self.e.recovery.damage(self.p,10,'combat')
        f=self.fact('CharacterAttacked',self.q.id,self.p.id,{'damage':10,'violence_intent':'hurt'})
        self.e.knowledge.learn(self.p,f,True);self.p.emotions.anger=55;self.p.emotions.resentment=40
        n=next(n for n in self.p.needs.values() if n.kind=='response' and n.target_id==self.q.id)
        self.e.lethal_decisions.refresh(self.p)
        return n,self.e.lethal_decisions.active(self.p,self.q.id)
    def revenge(self):
        self.e.graph.set(self.p.id,self.r.id,'amizade',100)
        self.e.finish_death(self.r,'combat',self.q)
        self.p.emotions.anger=self.p.emotions.resentment=80
        n=next(n for n in self.p.needs.values() if n.kind=='revenge' and n.target_id==self.q.id)
        self.e.lethal_decisions.refresh(self.p)
        return n,self.e.lethal_decisions.active(self.p,self.q.id)
    def test_01_moderate_cause_consolidates_without_several_extreme_injuries(self):
        n,d=self.moderate();self.assertIsNotNone(d);self.assertEqual('reactive_threat',d.mode)
        self.assertEqual(55,d.world_pressure);self.assertTrue(d.facts)
        self.assertEqual('kill',self.e.conflicts.intent(self.p,self.q,n))
        self.assertTrue(self.act(self.p,n,'attack',self.q.id)[0])
        self.assertGreater(self.w.metrics.get('LethalAttack',0),0)
    def test_02_traits_without_instigation_and_first_kill_do_not_make_murderer(self):
        self.p.personality.sadism=100;self.p.emotions.anger=100
        n=self.e.needs.ensure(self.p,'response:test',100,'test','Sem causa',self.q.id)
        before=dumps(self.w);rng=self.e.rng.getstate()
        self.assertFalse(self.e.lethality.evaluate(self.p,self.q,n)['available'])
        self.e.goals.solutions(self.p,n);self.assertEqual(before,dumps(self.w));self.assertEqual(rng,self.e.rng.getstate())
        self.p.death_affinity=100;self.p.death_state['positive_kills']=1
        self.assertFalse(self.e.lethal_decisions.seeking(self.p))
    def test_03_hysteresis_survival_pause_and_real_repair(self):
        n,d=self.moderate();self.assertIsNotNone(d)
        consideration=next(ev for ev in reversed(self.w.history) if ev.kind=='LethalConsideration' and ev.actor_id==self.p.id)
        self.assertTrue(self.act(self.p,n,'attack',self.q.id)[0])
        attack=next(ev for ev in reversed(self.w.history) if ev.kind=='CharacterAttacked' and ev.actor_id==self.p.id)
        recorded_facts=list(attack.context['action_audit']['source_facts'])
        considered_facts=list(consideration.context['lethal_audit']['known_facts'])
        self.p.hunger=100;self.p.fatigue=100;self.w.turn+=48
        self.e.conflicts.begin(self.p,self.r,None)
        self.e.conflicts.end(self.p,'timeout',self.q);self.e.lethal_decisions.refresh(self.p)
        self.assertIs(d,self.e.lethal_decisions.active(self.p,self.q.id))
        self.assertLessEqual(self.p.combat.truces.get(self.q.id,0),self.w.turn)
        self.p.fatigue=100;self.p.health=13
        self.assertFalse(self.e.lethal_decisions.action_audit(self.p,self.q.id,n)['eligible'])
        self.p.health=90;self.p.hunger=self.p.fatigue=10
        self.e.recovery.damage(self.p,10,'combat')
        reinforced=self.fact('CharacterAttacked',self.q.id,self.p.id,{'damage':10})
        self.e.knowledge.learn(self.p,reinforced,True)
        self.assertEqual('retributive',d.mode)
        self.assertIn(reinforced.event_id,d.facts)
        self.assertEqual(recorded_facts,attack.context['action_audit']['source_facts'])
        self.assertEqual(recorded_facts,attack.context['lethal_audit']['known_facts'])
        self.assertEqual(considered_facts,consideration.context['lethal_audit']['known_facts'])
        f=self.fact('ConflictForgiven',self.p.id,self.q.id)
        self.e.knowledge.learn(self.p,f,True)
        self.assertIsNone(self.e.lethal_decisions.active(self.p,self.q.id))
        self.assertEqual('forgiveness_or_meaningful_repair',d.reason)
    def test_04_terminal_spare_in_defense_finish_in_revenge_no_rng(self):
        n,d=self.moderate();self.assertIsNotNone(d)
        self.e.recovery.damage(self.q,90,'combat');self.e.conflicts.observe(self.p);self.e.terminal_combat.refresh(self.p)
        self.assertEqual('spare',self.e.lethal_decisions.terminal(self.p,self.q)['choice'])
        self.assertEqual('spare',self.e.goals.solutions(self.p,n)[0].action)
        self.assertFalse(self.act(self.p,n,'finish',self.q.id)[0]);self.assertTrue(self.act(self.p,n,'spare',self.q.id)[0]);self.assertTrue(self.q.alive)
        self.setUp();n,d=self.revenge();self.assertIsNotNone(d)
        self.e.recovery.damage(self.q,90,'combat');self.e.conflicts.observe(self.p);self.e.terminal_combat.refresh(self.p)
        self.assertEqual('finish',self.e.lethal_decisions.terminal(self.p,self.q)['choice'])
        choices=self.e.goals.solutions(self.p,n)
        self.assertEqual('finish',choices[0].action)
        self.assertEqual(self.e.lethal_decisions.terminal(self.p,self.q)['scores']['finish'],choices[0].score)
        self.assertFalse(any(c.action in ('attack','denounce','investigate') for c in choices))
        rng=self.e.rng.getstate();self.assertTrue(self.act(self.p,n,'finish',self.q.id)[0]);self.assertEqual(rng,self.e.rng.getstate())
        self.assertFalse(self.q.alive);self.assertEqual('deliberate_finish',self.w.death_records[self.q.id]['death_context'])
    def test_05_post_kill_guilt_versus_positive_reinforcement_and_decay(self):
        self.p.personality.compassion=self.p.personality.honesty=95
        self.e.finish_death(self.q,'combat',self.p,context={'violence_intent':'kill','post_incapacity':True})
        self.assertGreater(self.p.death_state['guilt'],60);self.assertEqual(0,self.p.death_affinity)
        self.r.personality.sadism=100;self.r.personality.compassion=self.r.personality.honesty=0
        victims=[self.s,self.p,next(p for p in self.w.characters.values() if p.id not in (self.p.id,self.q.id,self.r.id,self.s.id))]
        for victim in victims:self.e.finish_death(victim,'combat',self.r,context={'violence_intent':'kill'})
        self.assertEqual(3,self.r.death_state['positive_kills']);self.assertGreaterEqual(self.r.death_affinity,55)
        self.assertTrue(self.e.lethal_decisions.seeking(self.r))
        old=self.r.death_affinity;self.w.turn+=240;self.e.aftermath.refresh(self.r);self.assertLess(self.r.death_affinity,old)
    def test_06_action_oriented_god_values_known_deeds_more_than_prayer(self):
        g=self.god;g.domain='death';g.values['rewards_intentional_killing']=True
        self.e.navigation.relocate(self.p,g.location);self.e.navigation.relocate(self.q,g.location)
        for _ in range(4):self.e.recorder.emit('PrayerOffered','Oração controlada',self.p.id,g.id,g.location,context={'request':'sign','offering':0})
        prayer=self.e.divine_relations.affinity(g,self.p.id);self.assertLess(prayer,4)
        self.e.finish_death(self.q,'combat',self.p,context={'violence_intent':'kill'})
        self.assertGreater(self.e.divine_relations.affinity(g,self.p.id),prayer+10)
        unknown=next(t for t in self.w.towns.values() if t.id!=g.location.map_id)
        self.e.navigation.relocate(self.r,unknown.market);self.e.navigation.relocate(self.s,unknown.market)
        self.e.finish_death(self.s,'combat',self.r,context={'violence_intent':'kill'})
        self.assertEqual(0,self.e.divine_relations.affinity(g,self.r.id))
        known=next(ev for ev in self.w.history if ev.kind=='CharacterKilled' and ev.target_id==self.s.id)
        fact=Fact(known.id,known.kind,known.actor_id,known.target_id,known.location,known.turn,known.description,confidence=60,source_kind='known',context=known.context)
        self.e.knowledge.learn(self.p,fact,False)
        self.e.recorder.emit('PrayerOffered','Relato de feito conhecido',self.p.id,g.id,g.location,context={'request':'sign','offering':0,'deed_sources':[fact.event_id]})
        self.assertGreater(self.e.divine_relations.affinity(g,self.r.id),0)
    def test_07_composite_crisis_and_passive_loss_with_core_growth(self):
        before={'followers':100,'devoted':40,'cultists':10,'actors':8}
        collapse={'followers':50,'devoted':15,'cultists':0,'actors':1}
        self.assertIn(ReligiousHealth.classify(before,collapse,80,100),('CULT_COLLAPSE','REGIONAL_CRISIS','EXISTENTIAL_RELIGIOUS_THREAT'))
        healthy={'followers':60,'devoted':45,'cultists':12,'actors':9}
        self.assertEqual('STABLE',ReligiousHealth.classify(before,healthy,80,100))
        self.assertEqual('CORE_EROSION',ReligiousHealth.classify(before,{**before,'actors':3},30,100))
        # Crescimento rival chega apenas por conversão conhecida de membro
        # observado; o censo não informa uma divindade automaticamente.
        g=self.god;rival=next(god for god in self.w.divinities.values() if god.id!=g.id)
        for follower in (self.q,self.r):
            self.e.knowledge.learn(self.p,self.fact('PrayerOffered',follower.id,g.id),True)
        conversion=self.fact('FaithReinterpreted',self.q.id,g.id,{'current':'Culto de '+rival.name})
        self.e.knowledge.learn(self.p,conversion,True)
        self.e.knowledge.learn(self.p,self.fact('CharacterKilled',None,self.r.id),True)
        self.assertEqual(1,self.e.religious_health.report(self.p,g)['rival_growth'])
        self.assertFalse(any(ev.kind=='RivalFaithGrowthKnown' for ev in self.w.history))
        self.assertTrue(self.e.religious_health.send_report(self.p,g))
        self.assertTrue(any(ev.kind=='RivalFaithGrowthKnown' and ev.actor_id==g.id for ev in self.w.history))
    def test_08_god_requires_received_report_and_remote_presence_has_cost(self):
        g=self.god;g.values.update(compassion=95,patience=0,anger=0)
        self.w.faith_health[g.id]['global']['state']='CULT_COLLAPSE'
        self.assertEqual(0,self.e.faith.divine_assessment(g)['world_pressure'])
        self.e.navigation.relocate(self.p,g.location)
        for follower in (self.q,self.r):
            ritual=self.fact('PrayerOffered',follower.id,g.id,location=g.location);self.e.knowledge.learn(self.p,ritual,True)
            loss=self.fact('CharacterKilled',None,follower.id,location=g.location);self.e.knowledge.learn(self.p,loss,True)
        other=next(t for t in self.w.towns.values() if t.id!=g.location.map_id)
        g.location=other.market;g.presence_regions=[other.id]
        self.assertTrue(self.e.religious_health.send_report(self.p,g));self.assertTrue(self.e.faith.divine_assessment(g)['eligible'])
        request={'actor':self.p.id,'fact':g.messages[-1]['source_fact'],'location':vars(self.p.position),'turn':self.w.turn,'need':'protection','offering':0}
        energy=g.energy;self.assertFalse(self.e.faith.intervene(g,request))
        self.assertTrue(self.e.divine_relations.manifest(g,g.messages[-1]));self.assertLess(g.energy,energy)
        self.assertTrue(self.e.faith.intervene(g,request));self.assertGreaterEqual(energy-g.energy,45)
    def test_09_bond_death_signal_keeps_unknown_killer_unknown(self):
        g=self.god;g.domain='protection'
        self.e.navigation.relocate(self.p,g.location)
        for _ in range(8):self.e.recorder.emit('ProtectionGiven','Proteção controlada',self.p.id,self.q.id,g.location)
        self.assertIn(self.p.id,g.bonds)
        other=next(t for t in self.w.towns.values() if t.id!=g.location.map_id)
        self.e.navigation.relocate(self.p,other.market);self.e.navigation.relocate(self.q,other.market)
        # Um agressor conhecido em sinal de quase morte não transforma ajuda
        # ao favorito em maldição contra ele. A morte seguinte tem outro autor.
        g.values.update(compassion=95,patience=0,anger=90)
        self.e.recovery.damage(self.p,80,'combat')
        for _ in range(2):self.e.recorder.emit('CharacterAttacked','Agressão observada controlada',self.r.id,self.p.id,other.market,context={'damage':1})
        hp=self.p.health;self.e.faith.tick();self.assertGreaterEqual(self.p.health,hp)
        self.e.finish_death(self.p,'combat',self.q,context={'violence_intent':'kill'})
        message=next(m for m in reversed(g.messages) if m['context'].get('shock')=='favored_death')
        self.assertIsNone(message['actor']);self.assertIsNone(message['context']['killer'])
        emitted=next(e for e in reversed(self.w.history) if e.kind=='DivineMessage' and e.actor_id==g.id)
        self.assertIsNone(emitted.context['actor']);self.assertEqual(95,self.e.faith.divine_assessment(g)['world_pressure'])
    def test_10_unknown_homicide_pattern_investigation_and_persistence(self):
        guard=next(self.w.characters[i] for i in self.t.resident_ids if self.w.characters[i].profession=='guarda')
        for victim in (self.q,self.r):
            f=self.fact('CharacterKilled',None,victim.id,{'death_context':'deliberate_finish','weapon_id':None})
            self.e.knowledge.learn(guard,f,True)
        n=guard.needs['security:repeated_homicide'];self.assertIsNone(n.target_id);self.assertTrue(n.context['unknown_author'])
        self.assertIn('watch_case',[a for a,d,t in self.e.conflicts.candidates(guard,n)])
        self.assertFalse(self.e.justice.known_active(guard))
        self.w.rng_state=self.e.rng.getstate();saved=dumps(self.w);restored=loads(saved)
        self.assertEqual(saved,dumps(restored));self.assertFalse(validate_world(restored))
