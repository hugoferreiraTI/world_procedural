"""Dezoito regressões compostas: decisões morais e informação local."""
import unittest
from dataclasses import replace
import test_phase45 as fixtures
from procedural.engine import Engine
from procedural.models import Fact, Goal, Clue, Grievance, Location
from procedural.persistence import dumps,loads
from procedural.validation import assert_valid

class Phase46Tests(unittest.TestCase):
    setUpClass=classmethod(fixtures.Phase45Tests.setUpClass.__func__)
    setUp=fixtures.Phase45Tests.setUp
    fact=fixtures.Phase45Tests.fact
    need=fixtures.Phase45Tests.need
    def extreme(self):
        n,c=self.need()
        self.e.graph.set(self.p.id,self.q.id,'amizade',0);self.e.graph.set(self.p.id,self.q.id,'casamento',0)
        # A Fase 5.1 exige causa grave pessoal para executar a intenção;
        # a vítima conhecida da perda precisa ser alguém próximo.
        self.e.graph.set(self.p.id,self.guard.id,'amizade',100)
        f=self.fact('CharacterKilled',self.q.id,self.guard.id);n.context['source_event']=f.event_id
        self.p.grievances[self.q.id]=Grievance(self.q.id,'CharacterKilled',100,0,0,c.originating_fact)
        self.p.emotions.anger=self.p.emotions.resentment=100
        self.e.navigation.relocate(self.guard,self.guard.home);self.e.conflicts.observe(self.p)
        return n,c
    def search(self):
        n,c=self.need();self.e.investigation.refresh(self.p)
        self.e.navigation.relocate(self.q,self.q.home)
        self.p.observations.pop(self.q.id,None)
        return n,c
    def perform(self,n,action,target=None):
        return self.e.goals.execute(self.p,Goal(self.w.allocate_id(),n.id,action,0,self.w.turn,target),1)
    def test_01_anger_vengefulness_desperation_alone_never_murder(self):
        self.p.emotions.anger=self.p.emotions.resentment=self.p.emotions.desperation=100
        n,c=self.need();self.p.grievances.clear()
        r=self.e.lethality.evaluate(self.p,self.q,n)
        self.assertFalse(r['available']);self.assertIn('insufficient_pressure',r['blocking'])
    def test_02_extreme_convergence_and_evidence_trace(self):
        n,c=self.extreme();r=self.e.lethality.evaluate(self.p,self.q,n)
        self.assertTrue(r['available']);self.assertEqual('kill',self.e.conflicts.intent(self.p,self.q,n))
        self.assertEqual(c.id,r['commitment_id']);self.assertIn(n.context['source_event'],r['known_facts'])
        # Uma perda importante comprovada também é convergência, sem exigir
        # que a vítima da perda já tivesse sofrido ataques pessoais anteriores.
        self.setUp();self.e.graph.set(self.p.id,self.q.id,'amizade',0)
        self.e.graph.set(self.p.id,self.q.id,'casamento',0)
        self.e.graph.set(self.p.id,self.guard.id,'amizade',100)
        self.fact('CharacterKilled',self.q.id,self.guard.id)
        self.e.conflicts.observe(self.p)
        n=next(n for n in self.p.needs.values() if n.kind=='revenge')
        c=self.e.agency.adopt(self.p,n)
        self.assertIsNotNone(c)
        # Remove a autoridade presencial da cena de decisão, conserva a causa.
        self.e.navigation.relocate(self.guard,self.guard.home)
        self.e.conflicts.observe(self.p)
        r=self.e.lethality.evaluate(self.p,self.q,n)
        self.assertTrue(r['available']);self.assertEqual('known_close_loss',r['grave_basis'])
        self.assertGreaterEqual(r['world_pressure'],80);self.assertTrue(r['known_facts'])
    def test_03_low_confidence_and_unknown_author(self):
        n,c=self.extreme()
        for f in self.p.knowledge.values():
            if f.kind=='CharacterKilled':f.confidence=30
        mixed=self.e.lethality.evaluate(self.p,self.q,n)
        self.assertFalse(mixed['available']);self.assertEqual(0,mixed['confidence'])
        self.assertIn('low_confidence',mixed['blocking'])
        for f in self.p.knowledge.values():
            if f.actor_id==self.q.id:f.confidence=30
        r=self.e.lethality.evaluate(self.p,self.q,n)
        self.assertFalse(r['available']);self.assertIn('low_confidence',r['blocking'])
        self.p.knowledge.clear();self.assertFalse(self.e.lethality.evaluate(self.p,self.q,n)['available'])
    def test_04_compassion_fear_and_authority_are_real_barriers(self):
        n,c=self.extreme();base=self.e.lethality.evaluate(self.p,self.q,n)['pressure']
        self.p.personality.compassion=100
        r=self.e.lethality.evaluate(self.p,self.q,n);self.assertFalse(r['available']);self.assertLess(r['pressure'],base)
        self.assertIn('compassion',r['blocking'])
        self.p.personality.compassion=0;self.p.personality.courage=0;self.p.combat.injured=90
        self.assertIn('fear',self.e.lethality.evaluate(self.p,self.q,n)['blocking'])
    def test_05_intent_does_not_modify_damage_or_rng(self):
        n,c=self.extreme();power=self.e.conflicts.power(self.p);rng=self.e.rng.getstate()
        self.e.conflicts.intent(self.p,self.q,n)
        self.assertEqual(power,self.e.conflicts.power(self.p));self.assertEqual(rng,self.e.rng.getstate())
        self.e.agency.refresh(self.p)
        saved=dumps(self.w)
        self.e.goals.solutions(self.p,n);self.e.goals.solutions(self.p,n)
        self.assertEqual(saved,dumps(self.w))
        self.w.rng_state=rng;other=Engine(loads(dumps(self.w)))
        other.world.characters[self.p.id].personality.compassion=100
        g=Goal(self.w.allocate_id(),n.id,'attack',0,0,self.q.id)
        before=self.q.health;self.assertTrue(self.e.conflicts.execute(self.p,g,n)[0])
        op=other.world.characters[self.p.id];on=next(x for x in op.needs.values() if x.id==n.id)
        self.assertTrue(other.conflicts.execute(op,g,on)[0])
        self.assertEqual(before-self.q.health,before-other.world.characters[self.q.id].health)
    def test_06_common_incapacity_ends_conflict(self):
        n,c=self.need();self.p.personality.compassion=100;self.q.health=13
        self.e.conflicts.execute(self.p,Goal(self.w.allocate_id(),n.id,'attack',0,0,self.q.id),n)
        self.assertTrue(self.q.alive);self.assertFalse(self.p.combat.opponents);self.assertFalse(self.p.combat.pending_judgments)
    def test_07_incapacity_requires_new_choice_and_mercy_does_not_forgive(self):
        n,c=self.extreme();self.q.health=13
        self.perform(n,'attack',self.q.id);self.e.conflicts.observe(self.p)
        self.assertTrue(self.e.conflicts.pending_judgment(self.p,self.q.id))
        choices=[a for a,d,t in self.e.conflicts.candidates(self.p,n)]
        self.assertIn('spare',choices);self.assertIn('attack',choices)
        g=self.p.grievances[self.q.id].intensity
        self.perform(n,'spare',self.q.id)
        self.assertTrue(self.q.alive);self.assertEqual(g,self.p.grievances[self.q.id].intensity)
    def test_08_deliberate_death_records_cause_and_commitment(self):
        n,c=self.extreme();self.q.health=13
        for _ in range(6):
            if not self.q.alive:break
            self.e.conflicts.observe(self.p);self.perform(n,'attack',self.q.id);self.w.turn+=1
        self.assertFalse(self.q.alive)
        event=next(f for f in self.w.history if f.kind=='CharacterKilled' and f.target_id==self.q.id)
        audit=event.context['lethal_audit'];self.assertEqual(c.id,audit['commitment_id'])
        self.assertEqual('revenge',audit['motive']);self.assertTrue(audit['known_facts']);self.assertIn('barriers',audit)
    def test_09_episodes_not_blows_and_failed_alternative(self):
        n,c=self.need()
        for _ in range(3):self.e.conflicts.begin(self.p,self.q,n)
        self.assertEqual(1,self.p.combat.conflict_history[self.q.id]['episodes'])
        repair=Fact(self.w.allocate_id(),'CalmingAttempted',self.p.id,self.q.id,self.t.market,0,'Calma',source_kind='direct')
        self.e.knowledge.learn(self.p,repair,True);self.w.turn=1
        f=self.fact();self.assertEqual(1,self.p.combat.conflict_history[self.q.id]['failed_alternatives'])
    def test_10_stale_location_produces_bounded_investigation(self):
        n,c=self.search();self.w.turn=100
        choices=self.e.investigation.candidates(self.p,n)
        self.assertIn('search_area',[a for a,d,t in choices]);self.perform(n,'search_area',self.q.id)
        self.assertEqual(1,c.context['investigation']['attempts'])
        self.e.navigation.relocate(self.q,self.p.position)
        self.perform(n,'search_area',self.q.id)
        self.assertTrue(any(f.kind=='PersonLocated' and f.target_id==self.q.id for f in self.w.history+self.w.events))
        self.e.navigation.relocate(self.q,self.q.home)
        self.e.finish_death(self.q,'deprivation')
        self.e.navigation.relocate(self.p,self.q.home)
        self.perform(n,'search_area',self.q.id)
        self.assertTrue(any(f.kind=='RemainsLocated' for f in self.p.knowledge.values()))
        self.assertEqual(self.t.market,Clue(self.q.id,self.t.market,0,None,100,'cell',None).location)
    def test_11_informant_can_give_new_clue_without_global_position(self):
        n,c=self.search();self.w.turn=10
        f=Fact(self.w.allocate_id(),'PersonLocated',self.guard.id,self.q.id,self.q.home,10,'Vista em casa',source_kind='direct')
        self.e.knowledge.learn(self.guard,f,True);self.e.graph.set(self.guard.id,self.p.id,'confiança',60);self.e.graph.set(self.p.id,self.guard.id,'confiança',60)
        self.perform(n,'ask_about_person',self.guard.id)
        self.assertEqual(self.q.home,c.context['investigation']['clues'][-1].location)
        self.assertEqual(60,c.context['investigation']['clues'][-1].confidence)
        self.setUp();self.e.navigation.relocate(self.q,self.q.home)
        unknown=Fact(self.w.allocate_id(),'CharacterKilled',None,self.q.id,self.t.market,0,'Morte sem autor conhecido',source_kind='direct')
        self.e.knowledge.learn(self.p,unknown,True)
        n=next(n for n in self.p.needs.values() if n.kind=='revenge')
        c=self.e.agency.adopt(self.p,n,force=True);self.e.investigation.refresh(self.p)
        self.assertIsNone(n.target_id)
        testimony=Fact(self.w.allocate_id(),'CharacterKilled',self.guard.id,self.q.id,self.t.market,0,'Autoria conhecida pela fonte',source_kind='direct')
        self.e.knowledge.learn(self.guard,testimony,True)
        self.e.graph.set(self.p.id,self.guard.id,'confiança',60);self.e.graph.set(self.guard.id,self.p.id,'confiança',60)
        self.perform(n,'ask_about_person',self.guard.id)
        self.assertEqual(self.guard.id,n.target_id);self.assertEqual(self.guard.id,c.target_id)
        self.assertEqual(self.guard.id,c.context['investigation']['clues'][-1].subject_id)
        self.assertEqual(60,n.context['culprit_confidence'])
    def test_12_no_information_is_not_invented_and_rumor_keeps_confidence(self):
        n,c=self.search();self.guard.knowledge.clear();self.guard.observations.clear()
        old=list(c.context['investigation']['clues']);self.perform(n,'ask_about_person',self.guard.id)
        self.assertEqual(old,c.context['investigation']['clues'])
        self.w.turn=60;c.context['investigation']['asked'].clear()
        f=Fact(self.w.allocate_id(),'PersonLocated',self.guard.id,self.q.id,self.q.home,60,'Rumor',confidence=30,source_kind='rumor')
        self.e.knowledge.learn(self.guard,f,False);self.e.graph.set(self.guard.id,self.p.id,'confiança',60);self.e.graph.set(self.p.id,self.guard.id,'confiança',60)
        self.perform(n,'ask_about_person',self.guard.id)
        self.assertEqual(30,c.context['investigation']['clues'][-1].confidence)
        self.assertEqual('rumor',c.context['investigation']['clues'][-1].source_kind)
    def test_13_exhaustion_sleeps_without_forgetting_or_replaying_emotion(self):
        n,c=self.search();c.context['investigation']['attempts']=6
        anger=self.p.emotions.anger;self.e.investigation.refresh(self.p)
        self.assertEqual('waiting_for_information',c.status);self.assertEqual('waiting_for_information',n.status)
        self.w.turn=48;self.e.agency.refresh(self.p)
        self.assertEqual('waiting_for_information',c.status);self.assertIn(c.originating_fact,self.e.agency.pinned(self.p))
        self.assertEqual(anger,self.p.emotions.anger);self.assertFalse(self.e.investigation.candidates(self.p,n))
    def test_14_useful_fact_wakes_no_action_and_bad_clue_does_not(self):
        n,c=self.search();self.e.investigation.sleep(self.p,n,'test');before=self.p.position;hp=self.q.health
        old=c.context['investigation']['clues'][-1]
        self.assertFalse(self.e.investigation.accept(self.p,n,replace(old,observed_at=-1,confidence=10)))
        self.assertEqual('waiting_for_information',c.status)
        self.w.turn=24;f=Fact(self.w.allocate_id(),'PersonLocated',self.guard.id,self.q.id,self.q.home,24,'Nova pista',source_kind='direct')
        self.e.knowledge.learn(self.p,f,True)
        self.assertEqual('active',c.status);self.assertEqual(before,self.p.position);self.assertEqual(hp,self.q.health);self.assertIsNone(self.p.goal)
    def test_15_travel_and_return_are_physical_and_save_preserves_sleep(self):
        n,c=self.search();dest=next(iter(self.p.known_towns));self.e.items.create(self.p.id,'food',6);self.e.items.create(self.p.id,'water',6)
        n.context['known_location']=vars(self.w.towns[dest].market)
        first=self.e.agency.travel_candidates(self.p,n);self.e.navigation.relocate(self.q,self.q.workplace)
        self.assertEqual(first,self.e.agency.travel_candidates(self.p,n))
        self.e.investigation.sleep(self.p,n,'test');self.e.navigation.relocate(self.p,self.w.towns[dest].market)
        old=self.p.position;self.e.investigation.return_home(self.p,n)
        self.assertNotEqual(self.p.home,self.p.position);self.assertLessEqual(abs(old.x-self.p.position.x)+abs(old.y-self.p.position.y),1)
        self.w.rng_state=self.e.rng.getstate();other=Engine(loads(dumps(self.w)));assert_valid(other.world)
        self.assertEqual('waiting_for_information',other.world.characters[self.p.id].commitments[c.id].status)
    def test_16_institutional_clue_has_latency_locality_and_known_authority(self):
        n,c=self.search()
        crime=Fact(self.w.allocate_id(),'CharacterAttacked',self.q.id,self.p.id,self.t.market,0,'Ataque',source_kind='direct')
        self.e.knowledge.learn(self.guard,crime,True)
        observer=next(p for p in self.w.characters.values() if p.town_id==self.t.id and p.id not in (self.p.id,self.q.id,self.guard.id))
        observer.profession='guarda';self.e.navigation.relocate(observer,self.t.market)
        self.w.turn=6;self.e.justice.communicate();self.e.needs.refresh(observer)
        self.w.turn=7
        f=Fact(self.w.allocate_id(),'SearchClueShared',self.p.id,self.guard.id,self.q.home,7,'Pista',confidence=60,source_kind='known',context={'subject':self.q.id,'observed_at':7,'specificity':'cell'})
        self.e.knowledge.learn(self.guard,f,False)
        self.e.justice.communicate();self.assertNotIn(f.event_id,observer.knowledge)
        self.w.turn=13;self.e.justice.communicate();self.assertIn(f.event_id,observer.knowledge)
        self.assertEqual(60,observer.knowledge[f.event_id].confidence)

    def test_17_serious_repeated_assault_can_mature_without_trivial_response_commitment(self):
        self.e.graph.set(self.p.id,self.q.id,'amizade',0)
        self.e.graph.set(self.p.id,self.q.id,'casamento',0)
        self.e.navigation.relocate(self.guard,self.guard.home)
        self.e.recovery.damage(self.p,15,'combat')
        self.e.recorder.emit('CharacterAttacked','Agressão conhecida',self.q.id,self.p.id,self.p.position,
                             context={'damage':15})
        self.e.conflicts.observe(self.p)
        self.e.agency.refresh(self.p)
        n=self.p.needs['response:'+str(self.q.id)]
        self.assertIsNone(self.e.agency.current(self.p,n))
        self.e.recorder.emit('CalmingAttempted','Tentativa real de resolução',self.p.id,self.q.id,self.p.position)
        from procedural.rules import INTERACTION
        self.w.turn=INTERACTION.conflict_timeout+1
        self.e.recovery.damage(self.p,15,'combat')
        self.e.recorder.emit('CharacterAttacked','Nova agressão em outro episódio',self.q.id,self.p.id,self.p.position,
                             context={'damage':15})
        self.e.conflicts.observe(self.p)
        self.e.agency.refresh(self.p);c=self.e.agency.current(self.p,n)
        self.assertIsNotNone(c);self.assertEqual('response',c.motivation)
        self.w.turn+=INTERACTION.conflict_timeout+1
        self.e.recovery.damage(self.p,15,'combat')
        self.e.recorder.emit('CharacterAttacked','Reincidência grave conhecida',self.q.id,self.p.id,self.p.position,context={'damage':15})
        self.e.conflicts.observe(self.p);self.e.agency.refresh(self.p)
        self.assertTrue(self.e.lethality.evaluate(self.p,self.q,n)['available'])
        self.assertEqual('kill',self.e.conflicts.intent(self.p,self.q,n))
        self.e.navigation.relocate(self.q,self.q.home)
        self.assertIn('search_area',[a for a,d,t in self.e.investigation.candidates(self.p,n)])

    def test_18_confidence_upgrade_and_old_information_do_not_duplicate_harm_or_alternative(self):
        n,c=self.need()
        f=Fact(self.w.allocate_id(),'CharacterAttacked',self.q.id,self.p.id,self.p.position,0,'Autoria incerta',
               confidence=30,source_kind='rumor',context={'damage':5})
        self.e.knowledge.learn(self.p,f,False)
        h=self.p.combat.conflict_history[self.q.id]
        self.assertEqual(5,h['injury_received'])
        self.e.knowledge.learn(self.p,replace(f,confidence=60,source_kind='known'),False)
        self.assertEqual(5,h['injury_received'])
        old=Fact(self.w.allocate_id(),'CalmingAttempted',self.p.id,self.q.id,self.p.position,0,'Tentativa antiga',source_kind='direct')
        self.e.knowledge.learn(self.p,old,True);self.w.turn=1
        newer=replace(old,event_id=self.w.allocate_id(),turn=1)
        self.e.knowledge.learn(self.p,newer,True)
        for _ in range(80):
            self.e.knowledge.learn(self.p,Fact(self.w.allocate_id(),'Notice',None,None,None,1,'Aviso'),True)
        self.assertNotIn(old.event_id,self.p.knowledge)
        self.e.knowledge.learn(self.p,old,True)
        self.assertEqual(newer.event_id,h['pending_alternative']['fact'])
