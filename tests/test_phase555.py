"""Regressões causais da 5.5.5; cenários controlados não provam emergência."""
import copy
import unittest

import test_phase55 as fixtures
from procedural.engine import Engine
from procedural.goals import Solution
from procedural.models import Fact, Goal, Location
from procedural.observability import EventIndex
from procedural.persistence import dumps, loads, encode
from procedural.organization_context import bind_organization, organization_id


class StabilizationTests(unittest.TestCase):
    setUp=fixtures.InstitutionalTests.setUp
    group=fixtures.InstitutionalTests.group
    share=fixtures.InstitutionalTests.share
    proposal=fixtures.InstitutionalTests.proposal
    faction=fixtures.InstitutionalTests.faction

    def test_b01_nested_snapshots_and_fact_independence(self):
        payload={'members':[self.p.id], 'nested':{'values':[1,2]},'set':{2,3}}
        event=self.e.recorder.emit('SnapshotControl','Controle',self.p.id,location=self.p.position,
                                   historical=True,context=payload)
        before=encode(event)
        payload['members'].append(self.q.id);payload['nested']['values'].append(3);payload['set'].add(4)
        self.assertEqual(before,encode(event))
        self.p.knowledge[event.id].context['nested']['values'].append(9)
        self.assertEqual(before,encode(event))
        self.assertEqual([1,2],self.q.knowledge[event.id].context['nested']['values'])
        self.assertEqual(dumps(self.w),dumps(loads(dumps(self.w))))
        fact=Fact(999999,'Snapshot',None,None,None,0,'Fato',context=payload)
        before=copy.deepcopy(fact.context);payload['members'].clear()
        self.assertEqual(before,fact.context)

    def test_b01_group_join_same_after_load(self):
        self.share(self.q)
        n=self.e.needs.ensure(self.p,'political_pressure',70,'fixture','Causa')
        g=self.e.society.form(self.p,'security',None,n)
        event=next(e for e in self.w.history if e.kind=='GroupFormed' and e.target_id==g.id)
        before=encode(event)
        self.w.rng_state=self.e.rng.getstate();loaded=loads(dumps(self.w));other=Engine(loaded)
        for engine in (self.e,other):
            p=engine.world.characters[self.r.id];group=engine.world.groups[g.id]
            engine.institutions.know_group(p,group,'controlled_contact')
            self.assertTrue(engine.institutions.join(p,group)[0])
        self.assertEqual(before,encode(event));self.assertEqual(dumps(self.w),dumps(loaded))

    def test_b02_received_rejection_records_responsibility_once(self):
        g=self.group([self.p,self.q,self.r]);prop=self.proposal(g)
        self.assertIsNone(g.responsibility_id)
        prop.status='rejected';self.assertIsNone(g.responsibility_id)
        fact=Fact(self.w.allocate_id(),'PolicyDecided',self.mayor.id,prop.id,self.t.market,0,'Recusa',
                  source_kind='direct',context={'group_id':g.id,'result':{'decision':'reject'}})
        self.e.knowledge.learn(self.p,fact,True)
        self.assertEqual(self.mayor.id,g.responsibility_id);self.assertEqual(1,g.failures)
        self.e.society.react(self.q,fact);self.assertEqual(1,g.failures)
        remote=self.group([self.r,self.s]);self.assertIsNone(remote.responsibility_id)

    def test_b02_better_confidence_does_not_duplicate_failure(self):
        g=self.group([self.p,self.q,self.r]);prop=self.proposal(g)
        fact=Fact(self.w.allocate_id(),'PolicyDecided',self.mayor.id,prop.id,self.t.market,0,'Recusa',
                  confidence=30,context={'group_id':g.id,'result':{'decision':'reject'}})
        self.e.knowledge.learn(self.p,fact,False)
        self.assertEqual(1,g.failures);self.assertIsNone(g.responsibility_id)
        fact.confidence=100;self.e.knowledge.learn(self.p,fact,True)
        self.assertEqual(1,g.failures);self.assertEqual(self.mayor.id,g.responsibility_id)

    def test_b03_preparation_respects_cooldown_and_known_empty_source(self):
        p=self.p;p.thirst=70;self.e.items.consume(p.id,'water',self.e.items.count(p.id,'water'))
        choice=Solution('work',50,p.home)
        self.assertEqual('fill_water',self.e.goals.preventive_choice(p,choice).action)
        p.failures['fill_water']=self.w.turn+12
        self.assertIsNone(self.e.goals.preventive_choice(p,choice))
        p.failures.clear();self.e.navigation.relocate(p,Location(self.t.id,5,5))
        p.market_observation={'town_id':self.t.id,'turn':self.w.turn,'stock':{'water':0}}
        self.assertIsNone(self.e.goals.preventive_choice(p,choice))
        p.market_observation={};self.e.items.consume(self.t.id,'water',self.e.items.count(self.t.id,'water'))
        self.e.navigation.relocate(p,self.t.market)
        source=Solution('fill_water',100,self.t.market)
        self.assertEqual('NO_STOCK',self.e.goals.eligibility(p,source))

    def test_b04_all_entrypoints_share_formalization_requirements(self):
        g=self.group([self.p,self.q,self.r]);self.w.turn=200;g.investment=4
        present=[self.p,self.q]
        self.assertFalse(self.e.institutions.can_formalize(self.p,g,present)['eligible'])
        self.e.navigation.relocate(self.r,self.r.home)
        self.assertIsNone(self.e.society.found_faction(self.p,g,present))
        goal=Goal(self.w.allocate_id(),g.originating_need,'formalize_organization',0,200,g.id)
        self.assertFalse(self.e.access.execute(self.p,goal,None)[0])
        self.e.navigation.relocate(self.r,self.p.position);g.failures=1
        self.assertTrue(self.e.institutions.can_formalize(self.p,g,[self.p,self.q,self.r])['eligible'])
        self.assertIsNotNone(self.e.society.found_faction(self.p,g,[self.p,self.q,self.r]))

    def test_b05_supply_commits_to_available_resource(self):
        f=self.faction();p=self.q
        self.e.items.consume(f.id,'water',self.e.items.count(f.id,'water'))
        n=self.e.needs.ensure(p,'organizational_survival',70,'test','Recursos')
        bind_organization(n.context,'faction',f.id);p.thirst=95;p.hunger=40
        candidate=next(c for c in self.e.institutions.faction_candidates(p,n) if tuple(c)[0]=='institutional_supply')
        self.assertEqual('food',candidate.resource_kind)
        sol=Solution.candidate(candidate)
        goal=Goal(self.w.allocate_id(),n.id,sol.action,sol.score,self.w.turn,sol.target_id,
                  resource_kind=sol.resource_kind)
        before=self.e.items.count(p.id,'food');self.assertTrue(self.e.institutions.execute(p,goal,n)[0])
        self.assertEqual(before+1,self.e.items.count(p.id,'food'))

    def test_b06_reused_need_has_single_typed_identity(self):
        f=self.faction();self.p.organization_ids.append(f.id)
        self.e.society.refresh(self.p);n=self.p.needs['organizational_survival']
        self.assertEqual(f.id,organization_id(n.context,'faction'))
        g=self.group([self.p,self.r,self.s]);self.e.society.refresh(self.p)
        self.assertEqual('group',n.context['organization_type']);self.assertNotIn('faction_id',n.context)
        self.assertEqual(g.id,organization_id(n.context,'group'))
        self.assertIsNone(organization_id(n.context,'faction'))
        self.assertEqual(f'organizational_survival:group:{g.id}',self.e.action_pressure.key(n))
        self.assertIsNone(self.e.institutions.faction_candidates(self.p,n))
        f.member_ids.append(self.p.id)
        goal=Goal(self.w.allocate_id(),n.id,'institutional_supply',0,0,f.id,resource_kind='food')
        self.assertFalse(self.e.institutions.execute(self.p,goal,n)[0])

    def test_b07_exploration_and_unknown_death_have_truthful_text(self):
        for p,cause in ((self.p,'exploration'),(self.q,'unrecognized_cause')):
            self.e.finish_death(p,cause)
            event=next(e for e in reversed(self.w.history) if e.target_id==p.id and e.kind=='CharacterDied')
            self.assertEqual(cause,event.context['cause']);self.assertNotIn('autoinfligida',event.description)
            self.assertIn('exploração' if cause=='exploration' else cause,event.description)

    def test_b08_religious_report_producer_utility_goal_execution(self):
        god=next(iter(self.w.divinities.values()))
        for p in (self.p,self.q,self.r):self.e.navigation.relocate(p,self.p.known_places['sacred'])
        for p in (self.q,self.r):
            self.e.recorder.emit('PrayerOffered','Oração',p.id,god.id,p.position,
                                context={'request':'sign','offering':0,'reported_severity':0})
            p.health=0;p.hunger=100;self.e.finish_death(p,'deprivation')
        n=self.e.needs.ensure(self.p,'religious_interest',60,'controlled_loss','Relatar perdas',god.id)
        choice=next(s for s in self.e.goals.solutions(self.p,n) if s.action=='report_congregation')
        self.assertIn('diligence',choice.considerations);self.assertIn('devotion',choice.considerations)
        goal=Goal(self.w.allocate_id(),n.id,choice.action,choice.score,0,choice.target_id,choice.destination)
        self.assertTrue(self.e.goals.execute(self.p,goal,1)[0])

    def test_query_is_pure_and_need_episode_changes_on_reactivation(self):
        n=self.e.needs.ensure(self.p,'food',60,'test','Fome');episode=n.need_episode_id
        self.w.rng_state=self.e.rng.getstate();before=dumps(self.w);rng=self.e.rng.getstate()
        self.e.goals.solutions(self.p,n)
        self.assertEqual(before,dumps(self.w));self.assertEqual(rng,self.e.rng.getstate())
        self.e.needs.finish(self.p,n);self.e.needs.ensure(self.p,'food',60,'test','Outra fome')
        self.assertNotEqual(episode,n.need_episode_id);self.assertEqual(2,n.episode)

    def test_native_causal_receipts_and_indices_survive_load(self):
        event=self.e.recorder.emit('ProblemShared','Problema',self.p.id,location=self.p.position,historical=True,
                                   context={'cause':'security','subject':None,'severity':75})
        n=self.e.needs.ensure(self.p,'food',60,'test','Comer');n.context['source_event']=event.id
        goal=Goal(self.w.allocate_id(),n.id,'eat',200,0)
        self.assertTrue(self.e.goals.execute(self.p,goal,1)[0])
        obs=self.w.observability
        trace=next(t for t in obs.decisions.values() if t.goal_id==goal.id)
        self.assertEqual(n.need_episode_id,trace.need_episode_id)
        self.assertIsNotNone(trace.action_attempt_id)
        death=self.e.recorder.emit('CharacterDied','Controle histórico',target_id=None,historical=True,
                                  context={'source_fact':event.id},witnesses=[self.p.id])
        details=self.e.observability.event_details(death.id)
        self.assertEqual((event.id,),details['parent_event_ids']);self.assertTrue(details['learning_receipts'])
        self.assertNotIn('DecisionTrace',[f.kind for f in self.p.knowledge.values()])
        self.w.rng_state=self.e.rng.getstate();loaded=loads(dumps(self.w));idx=EventIndex(loaded)
        for dimension,value in (('actor',None),('target',None),('location',None),('kind','CharacterDied'),('turn',0)):
            self.assertIn(death.id,[e.id for e in idx.query(dimension,value)])

    def test_ordinary_observability_has_bounded_retention(self):
        obs=self.e.observability
        for _ in range(600):
            with obs.decision(self.p,1):pass
        self.assertLessEqual(len(obs.data.recent_decisions),256)
        self.assertLessEqual(len([t for t in obs.data.decisions.values() if not t.important]),256)

    def test_death_keeps_private_appraisal_separate_from_original_event(self):
        self.q.health=1
        n=self.e.needs.ensure(self.p,'response',70,'test','Confronto',self.q.id)
        goal=Goal(self.w.allocate_id(),n.id,'attack',0,0,self.q.id)
        self.assertTrue(self.e.goals.execute(self.p,goal,1)[0])
        death=next(e for e in self.w.history if e.kind=='CharacterKilled' and e.target_id==self.q.id)
        self.assertNotIn('post_kill_appraisal',death.context)
        appraisal=next(e for e in self.w.history if e.kind=='PostKillAppraisal' and e.context['death_fact']==death.id)
        self.assertIn(death.id,appraisal.parent_event_ids)
        self.assertTrue(self.e.observability.event_details(death.id)['decision'].important)

    def test_old_save_is_rejected_explicitly(self):
        import json
        data=json.loads(dumps(self.w));data['format_version']=1
        with self.assertRaisesRegex(ValueError,'incompatível'):loads(json.dumps(data))
