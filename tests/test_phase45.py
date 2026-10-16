"""Dezoito regressões sobre continuidade, informação e consequências reais."""
import unittest
from dataclasses import replace
from procedural.generation import generate_world, GenerationConfig
from procedural.engine import Engine
from procedural.models import Fact, Goal, Personality, Grievance, Location
from procedural.persistence import dumps, loads
from procedural.validation import assert_valid


class Phase45Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.template=dumps(generate_world('Fase45',with_player=False,
            config=GenerationConfig(kingdom_count=1,historical_turns=0)))

    def setUp(self):
        self.w=loads(self.template);self.e=Engine(self.w)
        self.p=next(p for p in self.w.characters.values() if p.profession=='agricultor')
        self.t=self.w.towns[self.p.town_id]
        self.q=next(p for p in self.w.characters.values() if p.town_id==self.t.id and p.id!=self.p.id and p.profession!='guarda')
        self.guard=next(p for p in self.w.characters.values() if p.town_id==self.t.id and p.profession=='guarda')
        for p in (self.p,self.q,self.guard):
            self.e.navigation.relocate(p,self.t.market);p.hunger=p.thirst=p.fatigue=0
            p.needs.clear();p.goal=None;p.money=40
        self.p.personality=Personality(vengefulness=100,courage=100,persistence=100,compassion=0,ambition=90)
        self.e.graph.set(self.p.id,self.q.id,'amizade',80)

    def fact(self,kind='CharacterAttacked',actor=None,victim=None,location=None):
        f=Fact(self.w.allocate_id(),kind,actor or self.q.id,victim or self.p.id,
               location or self.t.market,self.w.turn,kind,source_kind='direct')
        self.e.knowledge.learn(self.p,f,True)
        return f

    def need(self):
        f=self.fact()
        n=self.e.needs.ensure(self.p,'revenge:test',65,f'event:{f.event_id}','Responder ao dano',self.q.id)
        n.context.update(source_event=f.event_id,known_location=vars(self.t.market),confidence=100)
        c=self.e.agency.adopt(self.p,n,force=True)
        return n,c

    def test_01_commitment_survives_food_interruption_and_returns(self):
        n,c=self.need();food=self.e.needs.ensure(self.p,'food',100,'physiology','Fome')
        self.e.agency.selected(self.p,[n,food],food,'eat');self.assertEqual('paused',c.status)
        self.e.agency.selected(self.p,[n],n,'investigate');self.assertEqual('active',c.status)
        self.assertEqual(n.id,c.originating_need)
        dest=next(iter(self.p.known_towns))
        travel=self.e.needs.ensure(self.p,'migration',65,'known_towns','Viagem',dest)
        travel.context['reason']='family';journey=self.e.agency.adopt(self.p,travel,force=True)
        self.e.needs.ensure(self.p,'migration',65,'migration','Continuar viagem',dest)
        self.e.agency.refresh(self.p)
        self.assertIn(journey.status,('active','paused'));self.assertIs(journey,self.e.agency.current(self.p,travel))
        self.e.needs.finish(self.p,n)
        next_fact=self.fact()
        replacement=self.e.needs.ensure(self.p,'revenge:test',65,f'event:{next_fact.event_id}',
                                        'Novo dano depois da resolução',self.q.id)
        replacement.context['source_event']=next_fact.event_id
        self.e.agency.refresh(self.p)
        self.assertEqual('satisfied',c.status)

    def test_02_pin_keeps_cause_without_duplicate_shock(self):
        n,c=self.need();anger=self.p.emotions.anger;origin=c.originating_fact
        for i in range(80):
            self.e.knowledge.learn(self.p,Fact(self.w.allocate_id(),'Notice',None,None,None,0,'Aviso'),True)
        self.assertIn(origin,self.p.knowledge);self.assertEqual(64,len(self.p.knowledge))
        self.e.knowledge.learn(self.p,self.p.knowledge[origin],True)
        self.assertEqual(anger,self.p.emotions.anger)
        evidence=Fact(self.w.allocate_id(),'CharacterAttacked',self.q.id,self.p.id,
                      self.t.market,0,'Notícia confiável',source_kind='known',confidence=60)
        self.e.knowledge.learn(self.p,evidence,False)
        reported=self.e.needs.ensure(self.p,'protection:confidence',65,f'event:{evidence.event_id}',
                                     'Proteção por notícia',self.p.id)
        reported.context.update(source_event=evidence.event_id,threat=self.q.id)
        adopted=self.e.agency.adopt(self.p,reported,force=True)
        self.assertEqual(60,adopted.context['confidence'])

    def test_03_activity_without_progress_changes_preference(self):
        n,c=self.need();before=self.e.agency.snapshot(self.p,n)
        for _ in range(4):self.e.agency.outcome(self.p,n,'pursue',before,True)
        terms={};score=self.e.agency.adjust(self.p,n,'pursue',100,terms)
        self.assertLess(score,60);self.assertEqual(4,c.activity_count);self.assertEqual(0,c.meaningful_progress)
        self.e.agency.outcome(self.p,n,'ask_personal_help',before,False)
        self.assertEqual(1,c.strategy_changes)

    def test_04_persistent_person_can_abandon(self):
        n,c=self.need();c.last_progress_at=0;self.w.turn=1100
        self.e.agency.refresh(self.p);self.assertEqual('abandoned',c.status)
        self.assertEqual('no_progress_or_lost_agency',c.context['ending_reason'])
        f=Fact(self.w.allocate_id(),'CharacterAttacked',self.q.id,self.p.id,
               self.t.market,self.w.turn,'Crime conhecido',source_kind='direct')
        self.e.knowledge.learn(self.guard,f,True);self.e.justice.refresh(self.guard)
        pursuit=next(n for n in self.guard.needs.values() if n.kind=='pursuit')
        persistent=self.e.agency.adopt(self.guard,pursuit,force=True)
        record=self.w.wanted_records[pursuit.context['record_id']]
        self.w.turn=record.created_at+self.e.justice.duration(record,self.guard.id)+1
        self.e.justice.refresh(self.guard);self.e.agency.refresh(self.guard)
        self.assertEqual('expired',pursuit.status);self.assertEqual('expired',persistent.status)
        self.assertFalse(self.e.conflicts.candidates(self.guard,pursuit))

    def test_05_impulse_and_aspiration_do_not_execute(self):
        n,c=self.need();money=self.p.money;hp=self.q.health
        self.e.agency.refresh(self.p);self.e.agency.profile(self.p,n)
        self.assertIsNone(self.p.goal);self.assertEqual(money,self.p.money);self.assertEqual(hp,self.q.health)

    def test_06_agency_ignores_remote_inventory_and_position(self):
        n,c=self.need();self.e.navigation.relocate(self.q,self.q.home)
        before=self.e.agency.profile(self.p,n)
        self.e.items.create(self.q.id,'weapon');self.q.money=10000
        self.e.navigation.relocate(self.q,self.w.towns[next(i for i in self.w.towns if i!=self.t.id)].market)
        self.assertEqual(before,self.e.agency.profile(self.p,n))

    def test_07_extreme_need_expands_without_forcing_crime(self):
        self.q.profession='comerciante';self.e.conflicts.observe(self.p)
        self.p.personality.honesty=100;self.p.hunger=100;self.p.health=1
        n=self.e.needs.ensure(self.p,'food',100,'physiology','Fome');n.context['emergency']=True
        self.assertNotIn('steal_person',[a for a,d,t in self.e.conflicts.candidates(self.p,n)])
        n.context['unresolved']={'failures':4}
        self.assertIn('steal_person',[a for a,d,t in self.e.conflicts.candidates(self.p,n)])
        self.assertIsNone(self.p.goal)

    def test_08_unknown_killer_is_not_inferred(self):
        f=Fact(self.w.allocate_id(),'CharacterKilled',None,self.q.id,self.t.market,0,'Morte de autoria desconhecida',source_kind='direct')
        self.e.knowledge.learn(self.p,f,True)
        n=next(n for n in self.p.needs.values() if n.kind=='revenge')
        c=self.e.agency.adopt(self.p,n,force=True)
        self.assertIsNone(n.target_id);self.assertIsNone(c.target_id)

    def test_09_later_evidence_fills_target_and_is_retained(self):
        self.test_08_unknown_killer_is_not_inferred()
        evidence=Fact(self.w.allocate_id(),'CharacterKilled',self.guard.id,self.q.id,
                      self.t.market,0,'Autor identificado em notícia confiável',
                      source_kind='known',confidence=60)
        self.e.knowledge.learn(self.p,evidence,False)
        c=next(c for c in self.p.commitments.values() if c.motivation=='revenge')
        self.assertEqual(self.guard.id,c.target_id);self.assertTrue(c.context['supporting_facts'])
        uncertain=replace(evidence,event_id=self.w.allocate_id(),actor_id=self.p.id,confidence=30)
        self.e.knowledge.learn(self.p,uncertain,False)
        self.assertEqual(self.guard.id,c.target_id)

    def test_10_intent_does_not_change_physical_power(self):
        n,c=self.need();power=self.e.conflicts.power(self.p)
        self.p.grievances[self.q.id]=Grievance(self.q.id,'CharacterKilled',100,0,0,c.originating_fact)
        self.p.emotions.anger=100;self.p.emotions.resentment=100
        self.e.conflicts.intent(self.p,self.q,n)
        self.assertEqual(power,self.e.conflicts.power(self.p))

    def test_11_nonlethal_incapacity_ends_normally(self):
        n,c=self.need();self.p.personality.compassion=100;self.p.emotions.anger=0
        self.q.health=13
        self.e.conflicts.execute(self.p,Goal(self.w.allocate_id(),n.id,'attack',0,0,self.q.id),n)
        self.assertTrue(self.q.alive);self.assertFalse(self.p.combat.opponents)
        self.assertFalse(self.p.combat.pending_judgments)

    def test_12_lethal_incapacity_requires_new_moral_decision(self):
        n,c=self.need();self.e.graph.set(self.p.id,self.q.id,'amizade',0)
        self.e.graph.set(self.p.id,self.q.id,'casamento',0)
        cause=self.fact('CharacterKilled',self.q.id,self.guard.id)
        n.context['source_event']=cause.event_id
        self.p.grievances[self.q.id]=Grievance(self.q.id,'CharacterKilled',100,0,0,c.originating_fact)
        self.p.emotions.anger=100;self.p.emotions.resentment=100;self.q.health=13
        self.e.navigation.relocate(self.guard,self.guard.home)
        self.e.conflicts.observe(self.p)
        self.e.conflicts.execute(self.p,Goal(self.w.allocate_id(),n.id,'attack',0,0,self.q.id),n)
        self.e.conflicts.observe(self.p)
        self.assertEqual('kill',self.p.combat.violence_intents[self.q.id])
        choices=self.e.conflicts.candidates(self.p,n)
        self.assertIn('spare',[a for a,d,t in choices]);self.assertIn('attack',[a for a,d,t in choices])
        self.w.rng_state=self.e.rng.getstate();lethal=Engine(loads(dumps(self.w)))
        actor=lethal.world.characters[self.p.id];victim=lethal.world.characters[self.q.id]
        lethal_need=next(m for m in actor.needs.values() if m.id==n.id)
        for _ in range(6):
            if not victim.alive:break
            lethal.conflicts.observe(actor)
            lethal.conflicts.execute(actor,Goal(lethal.world.allocate_id(),n.id,'attack',0,lethal.world.turn,victim.id),lethal_need)
            lethal.world.turn+=1
        self.assertFalse(victim.alive)
        self.e.conflicts.execute(self.p,Goal(self.w.allocate_id(),n.id,'spare',0,0,self.q.id),n)
        self.assertTrue(self.q.alive);self.assertFalse(self.p.combat.pending_judgments)

    def test_13_known_death_can_generate_related_commitment(self):
        self.fact('CharacterKilled',self.guard.id,self.q.id)
        self.e.agency.refresh(self.p)
        self.assertTrue(any(c.motivation in ('revenge','grief') for c in self.p.commitments.values()))
        unrelated=next(p for p in self.w.characters.values() if p.town_id!=self.t.id)
        self.assertFalse(unrelated.commitments)

    def test_14_institution_shares_with_latency_and_multiple_guards(self):
        others=[p for p in self.w.characters.values() if p.id not in (self.p.id,self.q.id,self.guard.id) and p.town_id==self.t.id][:2]
        for p in others:p.profession='guarda';self.e.navigation.relocate(p,self.t.market)
        f=Fact(self.w.allocate_id(),'CharacterKilled',self.q.id,self.p.id,self.t.market,0,'Crime grave',source_kind='direct')
        self.e.knowledge.learn(self.guard,f,True)
        self.e.justice.communicate();self.assertNotIn(f.event_id,others[0].knowledge)
        self.w.turn=6;self.e.justice.communicate()
        self.assertIn(f.event_id,others[0].knowledge)
        record=next(iter(self.w.wanted_records.values()))
        self.assertEqual(3,len(record.assignments));self.assertEqual(3,len(set(record.assignments.values())))
        attack=Fact(self.w.allocate_id(),'CharacterAttacked',self.q.id,self.guard.id,self.t.market,6,'Ataque ao guarda',source_kind='direct')
        self.assertEqual(4,self.e.justice.severity(self.guard,attack))
        observer=others[0]
        self.e.justice.refresh(observer)
        need=next(n for n in observer.needs.values() if n.kind=='pursuit')
        commitment=self.e.agency.adopt(observer,need,force=True)
        self.e.navigation.relocate(observer,observer.home)
        self.q.health=10
        self.assertTrue(self.e.justice.capture(self.guard,self.q)[0])
        self.assertEqual('active',record.known_status[observer.id])
        self.assertFalse(any(f.kind=='CharacterCaptured' for f in observer.knowledge.values()))
        self.e.navigation.relocate(observer,self.t.market)
        self.e.justice.communicate();self.e.needs.refresh(observer)
        self.assertEqual('satisfied',need.status)
        self.assertEqual('satisfied',commitment.status)
        self.assertFalse(self.e.conflicts.candidates(observer,need))

    def test_15_guard_outside_service_remains_uninformed(self):
        self.test_14_institution_shares_with_latency_and_multiple_guards()
        other=next(p for p in self.w.characters.values() if p.town_id!=self.t.id)
        other.profession='guarda'
        self.e.justice.communicate();record=next(iter(self.w.wanted_records.values()))
        self.assertNotIn(record.originating_fact,other.knowledge)

    def test_16_interlocal_following_uses_only_known_lead(self):
        n,c=self.need();dest=next(iter(self.p.known_towns))
        n.context['known_location']=vars(self.w.towns[dest].market)
        self.e.items.create(self.p.id,'food',6);self.e.items.create(self.p.id,'water',6)
        self.assertIn('follow_lead',[a for a,d,t in self.e.agency.travel_candidates(self.p,n)])
        self.w.turn=20;self.p.active_until=0;self.p.combat.opponents.clear()
        self.assertTrue(self.e.agency.follow_lead(self.p,dest,n)[0])
        self.assertEqual(1,self.e.feeding.decision_interval(self.p))
        self.p.known_towns.clear();self.assertFalse(self.e.agency.travel_candidates(self.p,n))

    def test_17_aspiration_derived_stable_and_ambition_changes_intensity(self):
        self.p.personality.greed=100;self.p.personality.family_loyalty=0;self.p.personality.diligence=0
        self.e.agency.aspirations(self.p);a=self.p.aspirations[0]
        self.assertEqual('wealth',a.domain)
        self.w.turn=48;self.e.agency.aspirations(self.p);self.assertIs(a,self.p.aspirations[0])
        self.q.personality=replace(self.p.personality,ambition=0)
        self.e.agency.aspirations(self.q);self.assertLess(self.q.aspirations[0].intensity,a.intensity)
        high=self.e.needs.refresh(self.p);low=self.e.needs.refresh(self.q)
        high_need=next(n for n in high if n.context.get('aspiration_domain')=='wealth')
        low_need=next(n for n in low if n.context.get('aspiration_domain')=='wealth')
        self.assertGreater(high_need.priority,low_need.priority)
        self.assertIsNotNone(self.e.agency.current(self.p,high_need))
        self.e.goals.debug=True;self.e.goals.decide(self.p,1)
        self.assertEqual('advancement',self.e.goals.traces[self.p.id]['need'])
        skill=self.e.needs.ensure(self.p,'advancement:aspiration:competence',40,'aspiration:competence','Aprender')
        skill.context['aspiration_domain']='competence'
        self.p.market_observation={'town_id':self.t.id,'turn':self.w.turn,'training_offer':True}
        self.assertEqual({'train'},{c.action for c in self.e.goals.solutions(self.p,skill)})

    def test_18_save_load_and_deterministic_continuation(self):
        n,c=self.need();self.e.agency.refresh(self.p);self.w.rng_state=self.e.rng.getstate()
        assert_valid(self.w);e2=Engine(loads(dumps(self.w)))
        self.assertEqual(self.p.commitments,e2.world.characters[self.p.id].commitments)
        self.e.simulate(24);e2.simulate(24)
        self.assertEqual(dumps(self.w),dumps(e2.world));assert_valid(self.w)
