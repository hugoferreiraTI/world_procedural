"""Seis verificações da escolha final, continuidade e classificação dos Actors."""
import unittest
from dataclasses import replace
import test_phase52 as base

class Phase521Tests(unittest.TestCase):
    setUpClass=classmethod(base.Phase52Tests.setUpClass.__func__)
    setUp=base.Phase52Tests.setUp
    fact=base.Phase52Tests.fact
    moderate=base.Phase52Tests.moderate
    revenge=base.Phase52Tests.revenge
    act=base.Phase52Tests.act

    def terminal(self,n):
        self.e.recovery.damage(self.q,90,'combat')
        self.e.conflicts.observe(self.p);self.e.terminal_combat.refresh(self.p)
        return self.e.goals.solutions(self.p,n)

    def test_01_finish_winner_executes_even_when_scores_are_close(self):
        n,d=self.revenge();self.assertIsNotNone(d)
        sources=list(d.facts)
        self.p.lethal_decisions.clear();self.p.commitments.clear();self.p.agency_state.clear()
        self.p.knowledge={i:self.p.knowledge[i] for i in sources}
        for _ in range(64-len(sources)):
            self.e.knowledge.learn(self.p,self.fact('MemoryNoise',None,None),True)
        d=self.e.lethal_decisions.consider(self.p,self.q,n)
        self.assertIsNotNone(d)
        self.assertTrue(all(i in self.p.knowledge for i in d.facts))
        audit=self.e.action_pressure.assess(self.p,n,'warn',self.q.id)
        sources=list(audit['source_facts'])
        reinforcement=self.fact('CharacterAttacked',self.q.id,self.p.id,{'damage':4})
        def nested_hostile_reactions(person,fact):
            if person.id==self.p.id and fact.event_id==reinforcement.event_id:
                for _ in range(65):
                    self.e.knowledge.learn(person,self.fact('MemoryNoise',None,None),True)
        self.e.knowledge.listeners.insert(0,nested_hostile_reactions)
        self.e.knowledge.learn(self.p,reinforcement,True)
        self.assertIn(reinforcement.event_id,d.facts)
        self.assertIn(reinforcement.event_id,self.p.knowledge)
        self.assertLessEqual(len(self.p.knowledge),64)
        self.assertEqual(sources,audit['source_facts'])
        self.terminal(n);d.rumination=80
        before=self.e.lethal_decisions.terminal(self.p,self.q)
        desired=before['scores']['spare']+1
        d.intensity+=(desired-before['scores']['finish'])/.8
        choices=self.e.goals.solutions(self.p,n)
        scores=self.e.lethal_decisions.terminal(self.p,self.q)['scores']
        self.assertAlmostEqual(1,scores['finish']-scores['spare'],places=2)
        rng=self.e.rng.getstate();selected=self.e.goals.choose(choices)
        self.assertEqual('finish',selected.action);self.assertEqual(rng,self.e.rng.getstate())
        self.assertTrue(self.act(self.p,n,selected.action,self.q.id)[0])
        self.assertFalse(self.q.alive);self.assertEqual('deliberate_finish',self.w.death_records[self.q.id]['death_context'])
        self.assertEqual(1,self.p.death_state['intentional_kills'])
        self.assertTrue(any(ev.kind=='PostKillAppraisal' and ev.actor_id==self.p.id for ev in self.w.history))
        self.assertEqual(rng,self.e.rng.getstate())

    def test_02_spare_winner_still_spares_when_defensive_threat_ends(self):
        n,d=self.moderate();self.assertIsNotNone(d)
        choices=self.terminal(n);rng=self.e.rng.getstate()
        selected=self.e.goals.choose(choices);self.assertEqual('spare',selected.action)
        self.assertTrue(self.act(self.p,n,selected.action,self.q.id)[0]);self.assertTrue(self.q.alive)
        self.assertEqual('abandoned',d.status);self.assertEqual('terminal_spared',d.reason)
        self.assertEqual(rng,self.e.rng.getstate())
        event=next(ev for ev in reversed(self.w.history) if ev.kind=='TerminalDecision')
        self.assertEqual('incapacity_removed_immediate_threat',event.context['terminal_context']['reason'])

    def test_03_only_reliable_knowledge_of_target_death_resolves_decision(self):
        n,d=self.moderate();self.assertIsNotNone(d)
        other=next(t for t in self.w.towns.values() if t.id!=self.t.id)
        self.e.navigation.relocate(self.q,other.market);self.e.finish_death(self.q,'hunger')
        self.e.lethal_decisions.refresh(self.p);self.assertEqual('active',d.status)
        event=next(ev for ev in reversed(self.w.history) if ev.kind=='CharacterDied' and ev.target_id==self.q.id)
        rumor=self.fact('CharacterDied',None,self.q.id,location=other.market)
        rumor=replace(rumor,event_id=event.id,confidence=30,source_kind='rumor')
        self.e.knowledge.learn(self.p,rumor,False);self.assertEqual('active',d.status)
        # Reações reentrantes podem expulsar a memória antes dos demais ouvintes.
        # A notícia aceita ainda precisa chegar ao sistema de decisão letal.
        def nested_reactions(person,fact):
            if person.id==self.p.id and fact.event_id==event.id and fact.confidence>=60:
                for _ in range(65):
                    self.e.knowledge.learn(person,self.fact('MemoryNoise',None,None),True)
        self.e.knowledge.listeners.insert(0,nested_reactions)
        self.e.knowledge.learn(self.p,replace(rumor,confidence=60,source_kind='known'),False)
        self.assertEqual('resolved',d.status);self.assertEqual('known_target_death',d.reason)
        self.assertLessEqual(len(self.p.knowledge),64)
        self.assertFalse(self.e.knowledge.processing)

    def test_04_old_decision_closes_by_safe_life_and_rumination_not_timeout(self):
        self.p.personality.vengefulness=60
        n,d=self.moderate();self.assertIsNotNone(d)
        self.e.navigation.relocate(self.p,self.p.home)
        self.w.turn+=240;self.p.hunger=100;self.p.health=10
        self.e.lethal_decisions.refresh(self.p);self.assertEqual('active',d.status)
        self.w.turn+=240;self.p.hunger=10;self.p.health=90
        self.e.lethal_decisions.refresh(self.p)
        self.assertEqual('abandoned',d.status);self.assertEqual('safe_life_and_diminished_rumination',d.reason)

    def test_05_emergency_aid_is_protection_actor_not_every_domain(self):
        self.e.recorder.emit('HelpGiven','Ajuda comum controlada',self.p.id,self.q.id,self.p.position,context={'urgency':25})
        self.assertFalse(any(v.get('acts',0) for v in self.p.social_state.get('religious_activity',{}).values()))
        self.e.recorder.emit('HelpGiven','Ajuda emergencial controlada',self.p.id,self.q.id,self.p.position,context={'urgency':90})
        active={g.name for g in self.w.divinities.values() if self.p.social_state.get('religious_activity',{}).get(g.id,{}).get('acts',0)}
        self.assertEqual({'Neruma'},active)

    def test_06_reliable_crime_information_aligns_with_justice_and_knowledge(self):
        self.r.profession='guarda';self.p.personality.honesty=100
        self.e.graph.set(self.p.id,self.r.id,'confiança',100);self.e.graph.set(self.r.id,self.p.id,'confiança',100)
        f=self.fact('CharacterAttacked',self.q.id,self.p.id,{'damage':4})
        self.e.knowledge.learn(self.p,f,True)
        self.assertTrue(self.e.personal_actions.inform(self.p,self.r,f)[0])
        active={g.name for g in self.w.divinities.values() if self.p.social_state.get('religious_activity',{}).get(g.id,{}).get('acts',0)}
        self.assertEqual({'Aurion','Elar'},active)

if __name__=='__main__':unittest.main()
