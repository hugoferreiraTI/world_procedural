"""Controles causais da Fase 6: não constituem narrativa natural."""
import copy
from dataclasses import asdict,fields
import unittest
import test_phase55 as fixtures
from procedural.engine import Engine
from procedural.generation import generate_world,GenerationConfig
from procedural.models import Fact,Goal,Location
from procedural.goals import Solution
from procedural.persistence import dumps,loads,encode
from procedural.sustainability import initial_water_infrastructure
from procedural.validation import assert_valid


class CausalDepthTests(unittest.TestCase):
    setUp=fixtures.InstitutionalTests.setUp
    group=fixtures.InstitutionalTests.group
    proposal=fixtures.InstitutionalTests.proposal
    policy=fixtures.InstitutionalTests.policy

    def test_capital_capacity_follows_final_population_without_stock_creation(self):
        t=self.t;before=self.e.items.count(t.id,'water')
        t.resident_ids=t.resident_ids*10
        design=initial_water_infrastructure(self.w,t)
        self.assertGreaterEqual(design['water_daily'],len(t.resident_ids)*48/45)
        self.assertEqual(before,self.e.items.count(t.id,'water'))
        self.w.maps[t.id].areas.clear()
        self.assertEqual(0,initial_water_infrastructure(self.w,t)['water_daily'])

    def test_insufficient_infrastructure_remains_insufficient(self):
        self.t.infrastructure.update(water_daily=0,water_storage=0)
        self.e.items.consume(self.t.id,'water',self.e.items.count(self.t.id,'water'))
        self.e.economy.daily();self.assertEqual(0,self.e.items.count(self.t.id,'water'))

    def test_physical_visitors_count_in_food_demand_without_changing_census(self):
        other=next(p for p in self.w.characters.values() if p.alive and p.town_id!=self.t.id)
        before=self.e.economy.food_diagnosis(self.t)['expected_demand'];census=self.t.population
        self.e.navigation.relocate(other,self.t.market)
        after=self.e.economy.food_diagnosis(self.t)['expected_demand']
        self.assertAlmostEqual(1.2,after-before);self.assertEqual(census,self.t.population)

    def test_capacity_is_not_realized_production(self):
        self.e.items.create(self.t.id,'water',self.t.infrastructure['water_storage'])
        self.e.economy.daily()
        self.assertEqual(0,self.t.production_today.get('water',0))
        self.assertGreater(self.t.infrastructure['water_daily'],0)

    def test_active_background_equal_local_emergency(self):
        a=self.p;b=self.q
        for p in (a,b):
            p.hunger=100;p.thirst=100;p.health=12;p.position=p.home;p.category='comum';p.active_until=0
        self.assertEqual(1,self.e.feeding.decision_interval(a));self.assertEqual(1,self.e.feeding.decision_interval(b))
        self.e.needs.refresh(a)
        self.assertEqual(100,a.needs['food'].priority);self.assertEqual(100,a.needs['water'].priority)

    def test_known_urgent_obligation_promotes_only_owner(self):
        p=self.p;p.category='comum';p.hunger=p.thirst=0;p.health=100
        self.e.navigation.relocate(p,p.home);p.active_until=0;p.combat.opponents.clear()
        self.assertEqual(12,self.e.feeding.decision_interval(p))
        n=self.e.needs.ensure(p,'institutional_task',70,'known','Obrigação recebida');n.priority=70
        self.assertEqual(1,self.e.feeding.decision_interval(p))
        self.e.needs.finish(p,n);self.assertEqual(12,self.e.feeding.decision_interval(p))

    def test_work_gate_no_payer_no_input_saturation_and_paid_output(self):
        p=self.p;p.profession='cozinheiro';p.workplace=self.t.market
        self.t.money=0;self.assertEqual('NO_PAYER',self.e.professions.work_gate(p))
        self.t.money=50
        self.e.items.consume(self.t.id,'grain',self.e.items.count(self.t.id,'grain'));self.t.grain_credit=0
        self.assertEqual('NO_INPUT',self.e.professions.work_gate(p))
        self.e.items.create(self.t.id,'grain',2);before=p.money+self.t.money
        result=self.e.professions.work(p,1)
        self.assertTrue(result.success);self.assertGreater(result.produced,0);self.assertGreater(result.paid,0)
        self.assertEqual(before,p.money+self.t.money)

    def test_remote_work_gate_does_not_know_empty_inputs(self):
        p=self.p;p.profession='cozinheiro';p.workplace=self.t.market
        self.e.navigation.relocate(p,p.home);self.e.items.consume(self.t.id,'grain',self.e.items.count(self.t.id,'grain'))
        n=self.e.needs.ensure(p,'money',60,'test','Trabalho')
        choices=self.e.goals._evaluate(p,n,[Solution('work',0,p.workplace)])
        self.assertTrue(choices)

    def test_unemployed_can_take_known_training_need(self):
        p=self.p;p.profession=None;p.money=0
        p.market_observation={'turn':0,'training_offer':'cozinheiro','town_id':self.t.id}
        self.e.needs.refresh(p)
        self.assertIn('money',p.needs)
        self.assertNotIn(p.needs['money'].status,('satisfied','expired'))

    def test_training_requires_real_teacher_and_produces_paid_output(self):
        p=self.p;q=self.q;p.profession=None;q.profession='agricultor';q.workplace=self.t.market
        self.t.professional_demand['agricultor']={'deficit':1,'since':-60}
        offers=self.e.professions.training_opportunities(p,self.t)
        offer=next(o for o in offers if o.profession=='agricultor')
        p.market_observation={'training_offer':'agricultor','training_details':{'agricultor':asdict(offer)}}
        before=self.e.items.count(self.t.id,'grain');money=p.money+self.t.money
        self.assertTrue(self.e.professions.train(p,3)[0]);self.assertEqual(before+3,self.e.items.count(self.t.id,'grain'))
        self.assertEqual(money,p.money+self.t.money)
        self.e.navigation.relocate(q,q.home)
        self.assertFalse(self.e.professions.train(p,3)[0])

    def test_training_completion_changes_profession_and_known_workplace(self):
        p=self.p;q=self.q;p.profession=None;q.profession='lenhador';q.workplace=self.t.market
        self.t.professional_demand['lenhador']={'deficit':1,'since':-60}
        offer=next(o for o in self.e.professions.training_opportunities(p,self.t) if o.profession=='lenhador')
        p.market_observation={'training_offer':'lenhador','training_details':{'lenhador':asdict(offer)}}
        self.assertTrue(self.e.professions.train(p,36)[0]);self.assertEqual('lenhador',p.profession)
        self.assertEqual(q.workplace,p.known_places['work'])

    def test_apprentice_keeps_known_teacher_location_when_teacher_leaves(self):
        p=self.p;q=self.q;p.profession=None;q.profession='agricultor'
        rural=p.known_places['forage'];q.workplace=rural
        self.e.navigation.relocate(p,rural);self.e.navigation.relocate(q,rural)
        self.t.professional_demand['agricultor']={'deficit':1,'since':-60}
        self.e.economy.observe(p);self.assertTrue(self.e.professions.train(p,1)[0])
        self.e.navigation.relocate(q,q.home);self.w.turn+=1;self.e.economy.observe(p)
        info=p.market_observation['training_details']['agricultor']
        self.assertEqual(asdict(rural),info['location']);self.assertEqual(q.id,info['teacher'])
        self.assertFalse(self.e.professions.train(p,1)[0])
        self.e.navigation.relocate(q,rural)
        self.assertTrue(self.e.professions.train(p,1)[0])

    def test_low_social_affinity_alone_does_not_block_shared_cause(self):
        g=self.group([self.q,self.r]);self.e.institutions.know_group(self.p,g,'encounter')
        self.p.personality.compassion=0;self.p.personality.ambition=0
        self.e.graph.set(self.p.id,self.q.id,'confiança',10);self.e.graph.set(self.p.id,self.q.id,'amizade',0)
        result=self.e.institutions.group_compatibility(self.p,g,'security',None)
        self.assertLess(self.e.society.affinity(self.p,self.q,'security'),25)
        self.assertTrue(result.acceptable)

    def test_hostility_and_known_strategy_conflict_still_prevent_join(self):
        g=self.group([self.q,self.r]);self.e.institutions.know_group(self.p,g,'encounter')
        self.e.graph.set(self.p.id,self.q.id,'confiança',0)
        self.assertFalse(self.e.institutions.acceptable_group(self.p,g,'security',None)[0])
        self.e.graph.set(self.p.id,self.q.id,'confiança',65)
        self.p.known_groups[g.id]['strategy']='criminal_cooperation'
        self.assertEqual('strategy_conflict',self.e.institutions.acceptable_group(self.p,g,'security',None)[1])

    def test_delegate_delivers_while_leader_absent_and_task_survives_load(self):
        g=self.group([self.p,self.q,self.r]);prop=self.proposal(g)
        task=next(t for t in self.w.institutional_tasks.values() if t.kind=='deliver_proposal')
        self.assertIn(self.q.id,self.e.tasks.representatives(g))
        self.e.navigation.relocate(self.p,self.p.home)
        self.assertIn(task.id,self.q.social_state['known_tasks'])
        self.w.rng_state=self.e.rng.getstate();e=Engine(loads(dumps(self.w)))
        q=e.world.characters[self.q.id]
        goal=Goal(e.world.allocate_id(),0,'perform_institutional_task',55,e.world.turn,task.id)
        self.assertTrue(e.tasks.execute(q,goal,None)[0]);self.assertEqual('submitted',e.world.proposals[prop.id].status)
        self.assertEqual([self.q.id],e.world.institutional_tasks[task.id].executor_ids)

    def test_remote_delegate_does_not_know_task_completed_without_receipt(self):
        g=self.group([self.p,self.q,self.r]);prop=self.proposal(g)
        task=next(t for t in self.w.institutional_tasks.values() if t.kind=='deliver_proposal')
        self.e.navigation.relocate(self.q,self.q.home)
        self.assertTrue(self.e.institutions.submit(self.p,prop)[0])
        self.assertEqual('completed',task.status)
        self.assertEqual('pending',self.q.social_state['known_task_status'][task.id])
        self.e.tasks.refresh(self.q)
        self.assertNotIn(self.q.needs['institutional_task'].status,('satisfied','expired'))
        self.e.navigation.relocate(self.q,self.t.market);self.e.tasks.refresh(self.q)
        self.assertEqual('completed',self.q.social_state['known_task_status'][task.id])
        self.assertEqual('satisfied',self.q.needs['institutional_task'].status)

    def test_unknown_or_unauthorized_task_cannot_execute(self):
        g=self.group([self.p,self.q,self.r]);self.proposal(g)
        task=next(t for t in self.w.institutional_tasks.values() if t.kind=='deliver_proposal')
        goal=Goal(self.w.allocate_id(),0,'perform_institutional_task',55,0,task.id)
        self.assertFalse(self.e.tasks.execute(self.s,goal,None)[0])
        self.q.social_state['known_tasks']=[]
        self.assertFalse(self.e.tasks.execute(self.q,goal,None)[0])

    def test_formalization_explains_exact_gate_without_relaxing_threshold(self):
        g=self.group([self.p,self.q,self.r]);g.investment=4;self.w.turn=167
        check=self.e.institutions.can_formalize(self.p,g,[self.p,self.q,self.r])
        self.assertIn('TOO_YOUNG',check['gates']);self.assertFalse(check['eligible'])
        self.w.turn=200;g.investment=5
        self.assertTrue(self.e.institutions.can_formalize(self.p,g,[self.p,self.q,self.r])['eligible'])

    def test_remote_crime_not_filed_until_guard_reaches_station(self):
        p=self.p;p.profession='guarda';self.e.navigation.relocate(p,p.home)
        fact=Fact(self.w.allocate_id(),'CharacterAttacked',self.q.id,self.r.id,p.home,0,'Crime conhecido',confidence=100)
        self.e.knowledge.learn(p,fact,True)
        record=self.e.justice.record_for(p,self.q.id)
        self.assertIsNotNone(record);self.assertIsNone(record.institutional_fact)
        self.e.navigation.relocate(p,self.t.market);self.e.justice.communicate()
        self.assertIsNotNone(record.institutional_fact)

    def test_guard_without_fact_has_no_case_but_known_case_can_capture(self):
        p=self.p;q=self.q;p.profession='guarda'
        self.assertFalse(self.e.justice.capture(p,q)[0])
        fact=Fact(self.w.allocate_id(),'CharacterAttacked',q.id,self.r.id,self.t.market,0,'Agressão',confidence=100)
        self.e.knowledge.learn(p,fact,True);q.combat.surrendered_until=6
        self.assertTrue(self.e.justice.capture(p,q)[0])
        self.assertGreater(q.combat.detention_until,0)

    def test_divine_gates_distinguish_missing_knowledge_from_valid_access(self):
        p=self.p;god=next(iter(self.w.divinities.values()))
        prayer=self.e.recorder.emit('PrayerOffered','Oração controlada',p.id,god.id,p.position,context={'request':'sign'})
        god.messages=[]
        self.assertFalse(self.e.access.audience(p,god,prayer))
        self.assertIn('NO_DIVINE_KNOWLEDGE',self.w.observability.causal['religion_gates'][-1]['gates'])
        god.alive=True;god.presence_regions=[p.position.map_id];god.energy=100;god.values['honor']=100;p.devotion=100
        god.affinities[p.id]={'value':60,'deeds':0};god.messages=[{'actor':p.id,'source_fact':prayer.id,'context':{}}]
        self.assertTrue(self.e.access.audience(p,god,prayer));self.assertEqual(90,god.energy)

    def test_tombstone_preserves_discarded_causal_metadata(self):
        event=self.e.recorder.emit('EphemeralControl','Origem',self.p.id,location=self.p.position,witnesses=[])
        for i in range(4100):self.e.recorder.emit('EphemeralNoise','Ruído',witnesses=[])
        self.assertNotIn(event.id,self.e.observability.index.events)
        row=self.e.observability.event_details(event.id)
        self.assertEqual(event.kind,row['tombstone']['kind']);self.assertIsNone(row['event'])

    def test_need_metrics_do_not_invent_solvability_and_track_blocking(self):
        p=self.p
        a=self.e.needs.ensure(p,'food',100,'test','Fome');a.priority=100
        b=self.e.needs.ensure(p,'money',40,'test','Dinheiro');b.priority=40
        p.profession='agricultor';p.workplace=self.t.market
        self.e.audit.selection(p,[a,b],a)
        row=self.w.observability.causal['episodes'][b.need_episode_id]
        self.assertEqual(1,row['blocked_by_higher_need_count'])
        n=self.e.needs.ensure(p,'unknown_kind',20,'test','Sem probe')
        self.e.audit.selection(p,[a,n],a)
        self.assertIsNone(self.w.observability.causal['episodes'][n.need_episode_id]['last_solvable'])

    def test_physiology_growth_excludes_prior_consumption(self):
        p=self.p;p.hunger=50
        n=self.e.needs.ensure(p,'food',70,'test','Fome')
        self.e.audit.selection(p,[n],n)
        p.hunger=10  # Refeição depois da decisão, antes das horas seguintes.
        self.e.needs.physiology(p);self.e.needs.physiology(p)
        self.w.turn+=2;self.e.audit.selection(p,[n],n)
        counts=self.w.observability.causal['counts']
        self.assertEqual(4,counts['physiology_gap:'+p.lod+':hunger'])
        self.assertEqual(0,counts['net_gap:'+p.lod+':hunger'])

    def test_death_funnel_separates_owned_stock_and_world_shortage(self):
        self.p.hunger=100;self.p.health=0
        self.e.audit.death(self.p)
        row=self.w.observability.causal['deaths'][self.p.id]
        self.assertIn('RESOURCE_OWNED_AT_DEATH',row['factors'])
        self.assertNotIn('WORLD_SHORTAGE',row['factors'])
