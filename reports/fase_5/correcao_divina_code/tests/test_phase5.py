"""30 regressões compostas. Cenários raros são capacidade técnica, não frequência."""
import unittest
from procedural.engine import Engine
from procedural.generation import generate_world,GenerationConfig
from procedural.models import Fact,Goal,Grievance,Aspiration
from procedural.persistence import dumps,loads
from procedural.validation import validate_world
from dataclasses import replace

class Phase5Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.saved=dumps(generate_world('Candeia-5-controlada',with_player=False,
            config=GenerationConfig(kingdom_count=1,historical_turns=0)))
    def setUp(self):
        self.w=loads(self.saved);self.e=Engine(self.w);self.w.turn=96
        self.t=next(t for t in self.w.towns.values() if t.kind=='cidade')
        people=[self.w.characters[i] for i in self.t.resident_ids if self.w.characters[i].category=='comum' and i!=self.t.mayor_id]
        self.p,self.q,self.r=people[:3];self.m=self.w.characters[self.t.mayor_id]
        for p in (self.p,self.q,self.r,self.m):
            self.e.navigation.relocate(p,self.t.market);p.health=100;p.hunger=p.thirst=p.fatigue=10
            p.personality.compassion=70;p.personality.ambition=80;p.personality.persistence=80
        for a,b in ((self.p,self.q),(self.q,self.p),(self.p,self.r),(self.r,self.p)):
            self.e.graph.set(a.id,b.id,'confiança',80);self.e.graph.set(a.id,b.id,'amizade',70)
    def need(self,p=None):
        p=p or self.p;p.money=0;p.financial_since=0;p.financial_setbacks=5
        self.e.society.refresh(p)
        return p.needs['political_pressure']
    def action(self,p,n,a,target=None):
        return self.e.goals.execute(p,Goal(self.w.allocate_id(),n.id,a,0,self.w.turn,target),1)
    def group(self):
        n=self.need();qn=self.need(self.q)
        self.action(self.q,qn,'share_problem')
        return self.e.society.form(self.p,'resource_pressure',None,n)
    def proposal(self):
        g=self.group();leader=self.w.characters[g.leader_id]
        prop=self.e.society.propose(leader,g);prop.solution='food_distribution'
        n=self.e.needs.ensure(leader,'organizational_survival',60,'test','Representar',leader.id);n.context['group_id']=g.id
        self.action(leader,n,'submit_proposal',prop.id)
        return g,prop
    def terminal(self):
        p,q=self.p,self.q;p.personality.compassion=0;p.personality.vengefulness=95;p.personality.courage=95;p.personality.honesty=5
        self.e.graph.set(p.id,q.id,'amizade',0);self.e.graph.set(p.id,q.id,'casamento',0)
        self.e.graph.set(p.id,self.r.id,'amizade',100)
        self.e.finish_death(self.r,'combat',q)
        n=next(n for n in p.needs.values() if n.kind=='revenge' and n.target_id==q.id)
        p.grievances[q.id]=Grievance(q.id,'known_loss',100,self.w.turn,self.w.turn,n.context['source_event'])
        p.emotions.anger=p.emotions.resentment=100;c=self.e.agency.adopt(p,n,force=True);c.intensity=100
        self.e.recovery.damage(q,90,'combat');self.e.conflicts.observe(p)
        self.e.conflicts.intent(p,q,n);p.combat.pending_judgments[q.id]=self.w.turn+6
        return n
    def test_01_group_requires_shared_known_problem_and_contact(self):
        g=self.group();self.assertIsNotNone(g);self.assertIn(self.q.id,g.member_ids)
        self.assertIn(g.originating_fact,self.p.knowledge);self.assertEqual(1,len(self.w.groups))
        self.assertIsNone(self.e.society.form(self.p,'resource_pressure',None,self.p.needs['political_pressure']))
    def test_02_no_group_when_affinity_or_information_missing(self):
        n=self.need();self.assertIsNone(self.e.society.form(self.p,'resource_pressure',None,n))
        qn=self.need(self.q);self.action(self.q,qn,'share_problem')
        self.p.personality.compassion=self.p.personality.ambition=0
        self.e.graph.set(self.p.id,self.q.id,'amizade',0);self.e.graph.set(self.p.id,self.q.id,'confiança',0)
        self.assertIsNone(self.e.society.form(self.p,'resource_pressure',None,n))
    def test_03_proposal_requires_group_and_physical_delivery(self):
        g=self.group();prop=self.e.society.propose(self.w.characters[g.leader_id],g)
        self.assertEqual('draft',prop.status);self.assertNotIn(prop.id,self.t.office['known_proposals'])
        self.e.navigation.relocate(self.m,self.m.home)
        leader=self.w.characters[g.leader_id];n=self.e.needs.ensure(leader,'organizational_survival',50,'test','test');n.context['group_id']=g.id
        self.assertFalse(self.action(leader,n,'submit_proposal',prop.id)[0])
    def test_04_mayor_context_changes_competing_decisions(self):
        g,prop=self.proposal();a=self.e.society.decision_scores(self.m,prop)
        self.m.personality.compassion=0;self.m.personality.greed=100;prop.opposition=10
        b=self.e.society.decision_scores(self.m,prop)
        self.assertNotEqual(a,b);self.assertGreater(b['reject'],a['reject'])
    def test_05_approved_food_is_transferred_not_created(self):
        g,prop=self.proposal();before=self.e.items.count(self.t.id,'food')
        for id in g.member_ids:self.w.characters[id].hunger=60
        result=self.e.society.material(self.m,prop)
        self.assertEqual(result['food'],before-self.e.items.count(self.t.id,'food'))
        self.assertGreater(result['food'],0)
    def test_06_group_response_requires_received_decision(self):
        g,prop=self.proposal();prop.status='rejected';self.assertEqual(0,g.failures)
        leader=self.w.characters[g.leader_id]
        fact=Fact(self.w.allocate_id(),'PolicyDecided',self.m.id,prop.id,self.t.market,self.w.turn,'Recusada',
            context={'group_id':g.id,'result':{'decision':'reject','material':{}}},source_kind='direct')
        self.e.knowledge.learn(leader,fact,True);self.assertEqual(1,g.failures)
        self.assertEqual(self.m.id,g.responsibility_id);self.assertTrue(leader.alive)
    def test_07_antagonism_does_not_automatically_attack(self):
        g=self.group();g.subject_id=next(iter(self.p.beliefs));g.cause='religious_interest'
        other=replace(g,id=self.w.allocate_id(),leader_id=self.q.id,member_ids=[self.q.id,self.r.id],
                      needs={},goal=None,commitment=None,knowledge={},grievances={},support={},proposal_ids=[],memory=[])
        self.w.groups[other.id]=other
        f=Fact(self.w.allocate_id(),'PolicyDecided',self.m.id,None,self.t.market,self.w.turn,'Restrição',source_kind='direct',
            context={'group_id':other.id,'group_subject':next(iter(self.q.beliefs)),'result':{'decision':'approve','material':{'policy':'restricted','cult':g.subject_id}}})
        before=self.p.health;self.e.knowledge.learn(self.p,f,True)
        self.assertIn(other.id,g.grievances);self.assertEqual(before,self.p.health);self.assertFalse(self.p.combat.opponents)
    def test_08_faction_maturation_needs_resources_continuity(self):
        g=self.group();g.member_ids.append(self.r.id);self.r.group_ids.append(g.id)
        leader=self.w.characters[g.leader_id]
        self.assertIsNone(self.e.society.found_faction(leader,g,[self.p,self.q,self.r]))
        for p in (self.p,self.q,self.r):p.money=30
        self.assertIsNone(self.e.society.found_faction(leader,g,[self.p,self.q,self.r]))
        g.investment=4;g.created_at=self.w.turn-168
        before=sum(p.money for p in (self.p,self.q,self.r))
        f=self.e.society.found_faction(leader,g,[self.p,self.q,self.r]);self.assertIsNotNone(f)
        self.assertEqual(before,sum(p.money for p in (self.p,self.q,self.r))+f.money)
    def test_09_military_hierarchy_and_replacement(self):
        self.assertEqual([self.t.general_id],[i for i,r in self.t.military_ranks.items() if r=='General'])
        general=self.w.characters[self.t.general_id]
        substitute=next(p for p in (self.p,self.q,self.r) if p.id!=general.id)
        substitute.profession='guarda'
        self.e.navigation.relocate(general,self.t.position)
        self.e.society.hierarchy(self.t);self.assertEqual(general.id,self.t.general_id)
        self.e.finish_death(general,'deprivation')
        self.e.society.hierarchy(self.t)
        self.assertNotEqual(general.id,self.t.general_id)
        self.assertEqual([self.t.general_id],[i for i,r in self.t.military_ranks.items() if r=='General'])
    def test_10_promotion_not_xp_or_money_only(self):
        f=next(iter(self.w.factions.values()));leader=self.w.characters[f.leader_id]
        self.e.navigation.relocate(leader,self.t.market);self.e.graph.set(self.q.id,leader.id,'confiança',80)
        n=self.e.needs.ensure(leader,'organizational_survival',50,'test','recrutar');n.context['faction_id']=f.id
        self.q.personality.courage=90;self.assertTrue(self.action(leader,n,'recruit_member',self.q.id)[0])
        self.e.graph.set(leader.id,self.q.id,'confiança',80)
        self.assertFalse(self.e.society.promote(leader,f,self.q))
        f.assignments[self.q.id]['deeds']=2;f.assignments[self.q.id]['joined_at']=0
        self.assertTrue(self.e.society.promote(leader,f,self.q));self.assertEqual(f.ranks[1],f.assignments[self.q.id]['rank'])
    def test_11_institution_has_only_received_reports(self):
        f=next(iter(self.w.factions.values()));leader=self.w.characters[f.leader_id]
        fact=Fact(self.w.allocate_id(),'ProblemShared',self.q.id,None,self.t.market,self.w.turn,'Queixa',source_kind='direct',context={'cause':'resource_pressure','subject':None})
        self.e.knowledge.learn(self.q,fact,True);self.assertNotIn(fact.event_id,f.knowledge)
        self.e.navigation.relocate(leader,self.t.market);self.e.knowledge.learn(leader,fact,True)
        n=self.e.needs.ensure(leader,'organizational_survival',50,'test','reportar');n.context['faction_id']=f.id
        self.action(leader,n,'report_to_faction',f.id);self.assertIn(fact.event_id,f.knowledge)
    def test_12_objective_god_is_not_faith(self):
        god=next(iter(self.w.divinities.values()));self.assertTrue(god.alive)
        self.p.beliefs.clear();self.assertTrue(god.alive);self.assertFalse(self.p.beliefs)
    def test_13_mortal_veneration_does_not_create_god(self):
        self.p.devotion=100;self.e.graph.set(self.p.id,self.q.id,'confiança',100)
        for _ in range(5):
            fact=Fact(self.w.allocate_id(),'FactionFounded',self.q.id,None,self.t.market,self.w.turn,'Fundação',source_kind='direct')
            self.e.knowledge.learn(self.p,fact,True)
        self.assertTrue(self.p.beliefs[self.q.id]['believed_divine'])
        self.assertNotIn('actual_divinity',self.q.social_state);self.assertNotIn(self.q.id,self.w.divinities)
    def test_14_spiritual_report_preserves_confidence_and_source(self):
        god=next(iter(self.p.beliefs));self.p.beliefs[god].update(source_fact=999,interpretation='miracle',confidence=30)
        self.e.recorder.emit('SpiritualReport','Relato',self.q.id,god,self.t.market,
            context={'confidence':30,'believed_subject':god,'interpretation':'miracle','source_fact':999})
        f=next(f for f in self.p.knowledge.values() if f.kind=='SpiritualReport')
        self.assertEqual(30,f.confidence);self.assertEqual('rumor',f.source_kind);self.assertEqual(self.q.id,f.source_id)
    def test_15_intervention_cost_cause_and_local_witnesses(self):
        god=next(iter(self.w.divinities.values()));god.last_intervention=-1000;god.energy=100
        self.p.health=80
        req={'actor':self.p.id,'turn':self.w.turn,'location':vars(self.p.position),'fact':123,'need':'healing','offering':1}
        self.assertTrue(self.e.faith.intervene(god,req,'blessing'));self.assertEqual(80,god.energy);self.assertGreater(self.p.health,80)
        self.assertFalse(self.e.faith.intervene(god,req));self.assertIn(god.interventions[-1],self.p.knowledge)
    def test_16_unknown_deed_has_no_social_renown(self):
        remote=self.q.home
        self.e.recorder.emit('FactionFounded','Feito remoto',self.q.id,location=remote,witnesses=[self.q.id])
        self.assertNotIn(self.q.id,self.p.renown)
        self.p.renown.clear()
        f=Fact(self.w.allocate_id(),'FirstAidGiven',self.q.id,None,self.t.market,self.w.turn,'Socorro',source_kind='direct')
        self.e.knowledge.learn(self.p,f,True)
        others=[p for p in self.w.characters.values() if p.id not in (self.p.id,self.q.id)][:12]
        for p in others:
            self.e.knowledge.learn(self.p,replace(f,event_id=self.w.allocate_id(),actor_id=p.id),True)
        self.assertEqual(12,len(self.p.renown));self.assertNotIn(self.q.id,self.p.renown)
        self.p.knowledge.pop(f.event_id,None)
        self.e.knowledge.learn(self.p,replace(f,confidence=30),False)
        self.assertEqual(12,len(self.p.renown));self.assertNotIn(self.q.id,self.p.renown)
    def test_17_renown_and_epithet_use_multiple_known_facts(self):
        for _ in range(3):
            f=Fact(self.w.allocate_id(),'FirstAidGiven',self.q.id,self.r.id,self.t.market,self.w.turn,'Socorro',source_kind='direct')
            self.e.knowledge.learn(self.p,f,True)
        record=self.p.renown[self.q.id];self.assertTrue(record['epithet']);self.assertEqual(3,len(record['facts']))
        self.assertFalse(self.q.social_state.get('actual_divinity'))
    def test_18_reach_requires_spread_and_multiple_evidence(self):
        f=Fact(self.w.allocate_id(),'FactionFounded',self.q.id,None,self.t.market,self.w.turn,'Fundou',source_kind='direct')
        self.e.knowledge.learn(self.p,f,True);self.assertEqual('personal',self.e.renown.reach(self.q.id)['scope'])
        self.assertEqual([self.p.town_id],self.e.renown.reach(self.q.id)['towns'])
    def test_19_mythic_potential_not_immediate_strength_or_destiny(self):
        baseline=self.e.conflicts.power(self.p);self.p.mythic_trait='Heroism'
        self.assertEqual(baseline,self.e.conflicts.power(self.p));self.assertFalse(self.p.social_state.get('actual_divinity'))
        self.e.navigation.relocate(self.p,self.p.home);n=self.e.needs.ensure(self.p,'power',60,'test','Treino')
        self.assertTrue(self.action(self.p,n,'train_power')[0]);self.assertGreater(self.e.conflicts.power(self.p),baseline)
        self.assertEqual(100,self.p.health);self.assertEqual(1,self.p.mythic_development)
        self.p.aspirations=[Aspiration('become_stronger',70,self.w.turn,context={'target':75})]
        self.e.agency.aspirations(self.p);self.e.faith.refresh(self.p)
        self.assertEqual('become_stronger',self.p.needs['power'].context['aspiration_domain'])
        self.assertIsNotNone(self.e.agency.adopt(self.p,self.p.needs['power'],force=True))
    def test_20_subjective_justice_and_power_aspiration(self):
        self.p.mythic_trait='Justice';self.p.personality.vengefulness=90
        self.p.grievances[self.q.id]=Grievance(self.q.id,'test',80,0,0,1)
        self.assertGreater(self.e.faith.modifier(self.p,'attack'),0)
        self.p.personality.vengefulness=0;self.assertEqual(0,self.e.faith.modifier(self.p,'attack'))
        self.assertGreater(self.e.faith.modifier(self.p,'denounce'),0)
    def test_21_divine_death_is_separate_and_not_automatic_apotheosis(self):
        god=next(iter(self.w.divinities.values()));self.e.navigation.relocate(self.p,god.location)
        self.assertTrue(self.e.faith.divine_death(self.p,god,'controlled'));self.assertFalse(god.alive)
        self.assertNotIn('actual_divinity',self.p.social_state);self.assertFalse(self.e.faith.apotheosis(self.p,god))
    def test_22_claimed_essence_transforms_domain(self):
        god=next(iter(self.w.divinities.values()));god.domain='love'
        self.e.navigation.relocate(self.p,god.location);self.p.mythic_trait='Justice';self.p.mythic_development=80
        self.e.navigation.relocate(self.q,god.location)
        self.q.beliefs[god.id]={'confidence':50,'interpretation':'cultural_tradition',
            'known_divinity':False,'believed_divine':True,'source_fact':None}
        previous_religion=self.q.religion
        self.e.faith.divine_death(self.p,god,'controlled')
        self.assertTrue(self.e.faith.apotheosis(self.p,god));new=self.w.divinities[self.p.social_state['actual_divinity']]
        self.assertEqual('judgment',new.domain);self.assertFalse(self.e.faith.apotheosis(self.p,god))
        claim=self.q.beliefs[new.id]
        self.assertEqual('claimed_ascension',claim['interpretation']);self.assertEqual(60,claim['confidence'])
        self.assertFalse(claim['known_divinity']);self.assertFalse(claim['believed_divine'])
        self.assertEqual(previous_religion,self.q.religion)
        self.q.known_places['sacred']=self.q.position
        self.q.beliefs[self.p.id]={'confidence':60,'interpretation':'social_veneration',
            'known_divinity':False,'believed_divine':True,'source_fact':claim['source_fact']}
        n=self.e.needs.ensure(self.q,'religious_interest',50,'controlled','Orar por crença recebida',self.p.id)
        self.assertTrue(self.action(self.q,n,'pray',self.p.id)[0]);self.assertIn(self.q.id,new.known_followers)
        request_count=len(new.essence['requests']);divinity_count=len(self.w.divinities)
        self.q.beliefs[self.r.id]={'confidence':60,'interpretation':'social_veneration',
            'known_divinity':False,'believed_divine':True,'source_fact':None}
        self.assertTrue(self.action(self.q,n,'pray',self.r.id)[0])
        self.assertEqual(request_count,len(new.essence['requests']));self.assertEqual(divinity_count,len(self.w.divinities))
        saved=loads(dumps(self.w));self.assertEqual(self.q.beliefs,saved.characters[self.q.id].beliefs)
        self.assertEqual(new.known_followers,saved.divinities[new.id].known_followers)
        self.assertEqual([],validate_world(self.w))
    def test_23_execution_opportunity_invalid_without_presence_or_intent(self):
        n=self.terminal();self.assertTrue(self.e.terminal_combat.opportunity(self.p,self.q))
        self.e.navigation.relocate(self.q,self.q.home);self.assertFalse(self.action(self.p,n,'finish',self.q.id)[0]);self.assertTrue(self.q.alive)
    def test_24_finish_is_fatal_without_damage_roll_and_records_context(self):
        n=self.terminal();rng=self.e.rng.getstate()
        self.assertTrue(self.action(self.p,n,'finish',self.q.id)[0]);self.assertFalse(self.q.alive);self.assertEqual(rng,self.e.rng.getstate())
        event=next(f for f in self.w.history if f.kind=='CharacterKilled' and f.target_id==self.q.id)
        self.assertEqual('deliberate_finish',event.context['death_context']);self.assertTrue(event.context['lethal_audit']['known_facts'])
    def test_25_mercy_preserves_grievance_and_life(self):
        n=self.terminal();g=self.p.grievances[self.q.id].intensity
        self.assertTrue(self.action(self.p,n,'spare',self.q.id)[0]);self.assertTrue(self.q.alive)
        self.assertEqual(g,self.p.grievances[self.q.id].intensity);self.assertFalse(self.e.terminal_combat.opportunity(self.p,self.q))
    def test_26_situational_lethality_requires_immediate_extreme_threat(self):
        self.p.personality.compassion=0;self.p.personality.courage=95;self.p.personality.honesty=0
        self.p.emotions.anger=90;self.e.graph.set(self.p.id,self.q.id,'amizade',0)
        self.e.graph.set(self.p.id,self.q.id,'casamento',0)
        self.assertFalse(self.e.terminal_combat.situational(self.p,self.q,None)['available'])
        f=Fact(self.w.allocate_id(),'CharacterAttacked',self.q.id,self.p.id,self.t.market,self.w.turn,'Agressão',source_kind='direct',context={'damage':20})
        self.e.knowledge.learn(self.p,f,True)
        self.e.recovery.damage(self.p,20,'combat')
        r=self.e.terminal_combat.situational(self.p,self.q,None);self.assertTrue(r['available']);self.assertEqual('situational',r['mode'])
        self.w.turn+=4;self.assertFalse(self.e.terminal_combat.situational(self.p,self.q,None)['available'])
    def test_27_item_history_not_magical_property_and_transfer_keeps_history(self):
        weapon=self.e.items.create(self.p.id,'weapon');self.r.category='importante'
        self.e.finish_death(self.r,'combat',self.p,weapon.id)
        self.assertTrue(weapon.important_events);self.assertFalse(weapon.actual_properties)
        moved=self.e.items.transfer(self.p.id,self.q.id,weapon.id)
        self.assertEqual(weapon.important_events,moved.important_events);self.assertIn(self.p.id,moved.previous_owners)
    def test_28_save_limits_query_purity_and_seeded_continuity(self):
        self.group();self.w.rng_state=self.e.rng.getstate();self.assertEqual([],validate_world(self.w))
        other=Engine(loads(dumps(self.w)));self.e.simulate(12);other.simulate(12)
        self.assertEqual(dumps(self.w),dumps(other.world));self.assertEqual([],validate_world(self.w))
        n=next(iter(self.p.needs.values()));before=dumps(self.w)
        self.e.goals.solutions(self.p,n);self.assertEqual(before,dumps(self.w))
        player_world=generate_world('Fase5-interface',with_player=True,config=GenerationConfig(kingdom_count=1,historical_turns=0))
        interface=Engine(player_world);before=dumps(player_world)
        for command in ('grupos','organizacoes','renome','crencas','necessidades'):
            self.assertTrue(interface.execute(command).success)
        self.assertEqual(before,dumps(player_world))
    def test_29_office_contact_and_known_physical_faction_route(self):
        g,prop=self.proposal();prop.status='draft';self.t.office['known_proposals']=[]
        self.e.navigation.relocate(self.m,self.m.home)
        self.m.devotion=0;self.m.money=100;self.m.personality.diligence=100
        self.e.items.create(self.m.id,'food',12);self.e.items.create(self.m.id,'water',12)
        self.e.society.refresh(self.m);self.assertEqual('office_hours',self.m.needs['governance'].context['mode'])
        for _ in range(20):
            self.e.goals.decide(self.m,1);self.w.turn+=1
            if self.m.social_state.get('office_until',-1)>self.w.turn:break
        self.assertEqual(self.t.market,self.m.position)
        leader=self.w.characters[g.leader_id];n=self.e.needs.ensure(leader,'organizational_survival',50,'test','Representar',leader.id)
        self.assertTrue(self.action(leader,n,'submit_proposal',prop.id)[0])
        self.assertIn(prop.id,self.t.office['known_proposals'])
        f=next(iter(self.w.factions.values()));leader=self.w.characters[f.leader_id]
        grid=self.w.maps[leader.position.map_id]
        self.e.navigation.relocate(leader,grid.exit_to)
        t=self.w.towns[leader.town_id];self.e.navigation.relocate(leader,t.position)
        self.e.society.refresh(leader);n=leader.needs['organizational_survival']
        self.assertTrue(self.action(leader,n,'report_to_faction',f.id)[0])
        self.assertEqual(t.id,leader.position.map_id);self.assertEqual(t.id,leader.town_id)
        self.assertEqual([],validate_world(self.w))
    def test_30_public_reply_is_physical_and_remote_status_is_not_knowledge(self):
        g,prop=self.proposal();leader=self.w.characters[g.leader_id]
        self.e.navigation.relocate(leader,leader.home)
        self.m.personality.compassion=0;self.m.personality.greed=100;prop.opposition=100
        self.assertTrue(self.e.society.resolve(self.m,prop)[0]);self.assertEqual('rejected',prop.status)
        self.assertEqual('submitted',g.proposal_knowledge[prop.id]['status']);self.assertEqual(0,g.failures)
        self.e.society.refresh(leader);n=leader.needs['organizational_survival']
        self.assertIn('read_response',[a for a,d,t in self.e.society.candidates(leader,n)])
        self.assertFalse(self.action(leader,n,'read_response',g.id)[0])
        self.e.navigation.relocate(leader,self.t.market)
        self.assertTrue(self.action(leader,n,'read_response',g.id)[0])
        self.assertEqual('rejected',g.proposal_knowledge[prop.id]['status']);self.assertEqual(1,g.failures)
        self.assertTrue(self.action(leader,n,'read_response',g.id)[0]);self.assertEqual(1,g.failures)
        self.assertEqual([],validate_world(self.w))
        saved=loads(dumps(self.w));self.assertEqual(g.proposal_knowledge,saved.groups[g.id].proposal_knowledge)
        self.assertIsInstance(saved.towns[self.t.id].office['public_responses'][-1],Fact)

if __name__=='__main__':unittest.main()
