"""Onze regressões da Fase 5.1; condições controladas não são frequência natural."""
import unittest
from procedural.engine import Engine
from procedural.generation import generate_world,GenerationConfig
from procedural.models import Fact,Goal,Grievance
from procedural.goals import Solution
from procedural.persistence import dumps,loads
from procedural.validation import validate_world

class Phase51Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.template=dumps(generate_world('Liraven-51-controlada',with_player=False,
            config=GenerationConfig(kingdom_count=1,historical_turns=0)))
    def setUp(self):
        self.w=loads(self.template);self.e=Engine(self.w);self.w.turn=96
        self.t=next(t for t in self.w.towns.values() if t.mayor_id)
        self.p,self.q,self.r=[self.w.characters[i] for i in self.t.resident_ids if i!=self.t.mayor_id and self.w.characters[i].category=='comum'][:3]
        for p in (self.p,self.q,self.r):
            self.e.navigation.relocate(p,self.t.market);p.health=100;p.hunger=p.thirst=p.fatigue=10
            p.personality.persistence=p.personality.ambition=p.personality.courage=95
            p.personality.compassion=60;p.financial_since=0;p.financial_setbacks=15;p.money=0
        self.e.graph.set(self.p.id,self.q.id,'confiança',80);self.e.graph.set(self.p.id,self.q.id,'amizade',80)
    def act(self,p,n,a,target=None):
        return self.e.goals.execute(p,Goal(self.w.allocate_id(),n.id,a,0,self.w.turn,target),1)
    def group(self):
        self.e.society.refresh(self.q);qn=self.q.needs['political_pressure'];self.act(self.q,qn,'share_problem')
        self.e.society.refresh(self.p);n=self.p.needs['political_pressure']
        g=self.e.society.form(self.p,'resource_pressure',None,n)
        self.assertIsNotNone(g);return g
    def lethal(self):
        self.p.personality.compassion=0;self.p.personality.vengefulness=95;self.p.personality.honesty=5
        self.e.graph.set(self.p.id,self.r.id,'amizade',100);self.e.finish_death(self.r,'combat',self.q)
        n=next(n for n in self.p.needs.values() if n.kind=='revenge' and n.target_id==self.q.id)
        self.p.grievances[self.q.id]=Grievance(self.q.id,'known_loss',100,self.w.turn,self.w.turn,n.context['source_event'])
        self.p.emotions.anger=self.p.emotions.resentment=100
        self.e.agency.adopt(self.p,n,force=True).intensity=100
        self.e.conflicts.observe(self.p);self.e.action_pressure.refresh(self.p,[n]);return n
    def faction(self,capable=False):
        f=next(iter(self.w.factions.values()))
        for id in f.member_ids:
            old=self.w.characters[id]
            if f.id in old.organization_ids:old.organization_ids.remove(f.id)
        f.member_ids=[self.p.id,self.q.id] if capable else [self.p.id]
        f.leader_id=self.p.id;f.purpose='mercenaries';f.norms.update(allow_theft=True,harm_civilians=False,risk=1,hostile_town=self.t.id)
        f.assignments={id:{'rank':f.ranks[0],'deeds':0,'joined_at':0} for id in f.member_ids}
        for id in f.member_ids:
            self.w.characters[id].organization_ids=[f.id]
            if not self.e.conflicts.weapon(self.w.characters[id]):self.e.items.create(id,'weapon')
            self.e.items.create(id,'food',2)
        f.norms['former_members']=[self.r.id]
        self.e.graph.set(self.p.id,self.r.id,'amizade',80)
        self.e.finish_death(self.r,'combat',self.w.characters[self.t.mayor_id])
        fact=next(x for x in self.p.knowledge.values() if x.kind=='CharacterKilled' and x.target_id==self.r.id)
        f.knowledge[fact.event_id]=fact
        self.p.known_towns[self.t.id]={'position':vars(self.t.position),'confidence':100,'learned_at':0}
        self.e.society.refresh(self.p);n=self.p.needs['organizational_survival'];return f,n
    def prayer(self,p,god):
        self.e.navigation.relocate(p,god.location);p.known_places['sacred']=god.location
        p.beliefs[god.id]={'confidence':50,'interpretation':'cultural_tradition','believed_divine':True,'known_divinity':False}
        n=self.e.needs.ensure(p,'religious_interest',40,'test','Ritual controlado',god.id)
        self.assertTrue(self.act(p,n,'pray',god.id)[0])
    def test_01_low_cause_blocks_strong_action_even_with_personality(self):
        n=self.e.needs.ensure(self.p,'revenge',95,'test','Intenção sem base grave',self.q.id)
        self.p.personality.vengefulness=100;self.p.personality.compassion=0;self.p.emotions.anger=100
        self.e.action_pressure.refresh(self.p,[n]);a=self.e.action_pressure.assess(self.p,n,'finish',self.q.id)
        self.assertFalse(a['eligible']);self.assertEqual(0,a['world_pressure'])
        self.assertFalse(self.act(self.p,n,'finish',self.q.id)[0]);self.assertTrue(self.q.alive)
    def test_02_grave_known_loss_enables_intention_execution(self):
        n=self.lethal();a=self.e.action_pressure.assess(self.p,n,'finish',self.q.id)
        self.assertTrue(a['eligible']);self.assertGreaterEqual(a['world_pressure'],80)
        self.assertEqual(0,self.e.action_pressure.assess(self.p,n,'finish',self.t.mayor_id)['world_pressure'])
        self.p.health=40;self.p.fatigue=145
        self.assertTrue(self.e.lethality.evaluate(self.p,self.q,n)['available'])
        self.assertFalse(self.e.goals._evaluate(self.p,n,[Solution('attack',0,target_id=self.q.id)]))
        hp=self.q.health;rng=self.e.rng.getstate()
        self.assertFalse(self.act(self.p,n,'attack',self.q.id)[0]);self.assertEqual(hp,self.q.health)
        self.assertEqual('kill',self.p.combat.violence_intents[self.q.id]);self.assertEqual(rng,self.e.rng.getstate())
        self.p.health=100;self.p.fatigue=10;self.e.action_pressure.refresh(self.p,[n])
        self.e.recovery.damage(self.q,90,'combat');self.p.combat.violence_intents[self.q.id]='kill';self.p.combat.pending_judgments[self.q.id]=self.w.turn+6
        self.assertTrue(self.act(self.p,n,'finish',self.q.id)[0]);self.assertFalse(self.q.alive)
        death=next(x for x in reversed(self.w.history) if x.kind=='CharacterKilled' and x.target_id==self.q.id)
        self.assertTrue(death.context['action_audit']['eligibility_causes'])
    def test_03_many_weak_factors_do_not_become_grave_world_pressure(self):
        n=self.e.needs.ensure(self.p,'response',90,'test','Danos leves',self.q.id)
        for _ in range(3):
            f=Fact(self.w.allocate_id(),'CharacterAttacked',self.q.id,self.p.id,self.t.market,self.w.turn,'Dano leve',source_kind='direct',context={'damage':1})
            self.e.knowledge.learn(self.p,f,True);n.context['source_event']=f.event_id
        self.p.personality.vengefulness=100;self.p.personality.compassion=0;self.p.emotions.anger=self.p.emotions.resentment=100
        self.p.grievances[self.q.id]=Grievance(self.q.id,'weak_harm',90,self.w.turn,self.w.turn,f.event_id)
        self.e.agency.adopt(self.p,n,force=True)
        self.assertFalse(self.e.action_pressure.world_pressure(self.p,n)['grave'])
        self.assertFalse(self.e.action_pressure.assess(self.p,n,'finish',self.q.id)['eligible'])
        # Relatos incertos podem produzir desejo irracional, mas não comprovar
        # dano extremo atribuído. O HP abaixo cai por privação, não pelo suspeito.
        n=self.e.needs.ensure(self.p,'revenge',100,'rumor','Vingança incerta',self.q.id)
        for _ in range(4):
            self.w.turn+=72
            f=Fact(self.w.allocate_id(),'CharacterAttacked',self.q.id,self.p.id,self.t.market,self.w.turn,
                'Relato incerto',confidence=35,source_kind='rumor',context={'damage':12})
            self.e.knowledge.learn(self.p,f,False);n.context['source_event']=f.event_id
        self.p.grievances[self.q.id]=Grievance(self.q.id,'alleged_harm',100,self.w.turn,self.w.turn,f.event_id)
        self.p.personality.honesty=0;self.e.graph.set(self.p.id,self.q.id,'amizade',0);self.e.graph.set(self.p.id,self.q.id,'casamento',0)
        self.e.items.create(self.p.id,'weapon');self.e.recovery.damage(self.p,65,'hunger')
        self.e.agency.adopt(self.p,n,force=True).intensity=100
        self.assertTrue(self.e.lethality.evaluate(self.p,self.q,n)['available'])
        self.assertFalse(self.e.action_pressure.world_pressure(self.p,n)['grave'])
        hp=self.q.health;self.assertFalse(self.act(self.p,n,'attack',self.q.id)[0]);self.assertEqual(hp,self.q.health)
    def test_04_received_group_failures_raise_pressure_without_duplicate(self):
        g=self.group();leader=self.w.characters[g.leader_id];prop=self.e.society.propose(leader,g)
        self.e.collective.group_pressure(g,leader);before=g.action_pressure.value
        for _ in range(2):
            self.w.turn+=1
            fact=Fact(self.w.allocate_id(),'PolicyDecided',self.t.mayor_id,prop.id,self.t.market,self.w.turn,'Recusa controlada',source_kind='direct',context={'group_id':g.id,'result':{'decision':'reject','material':{}}})
            self.e.knowledge.learn(leader,fact,True);self.e.collective.group_pressure(g,leader)
        self.assertGreater(g.action_pressure.value,before);self.assertEqual(2,g.failures)
        self.e.society.react(leader,fact);self.assertEqual(2,g.failures)
        self.w.turn+=1
        fact=Fact(self.w.allocate_id(),'PolicyDecided',self.t.mayor_id,prop.id,self.t.market,self.w.turn,
            'Terceira recusa',source_kind='direct',context={'group_id':g.id,'result':{'decision':'reject','material':{}}})
        self.e.knowledge.learn(leader,fact,True)
        old=next(f for f in leader.knowledge.values() if f.kind=='PolicyDecided' and f.target_id==prop.id and f.event_id!=fact.event_id)
        self.e.society.react(leader,old);self.assertEqual(3,g.failures)
        self.assertEqual(fact.event_id,g.proposal_knowledge[prop.id]['response_fact'])
        for i in g.member_ids:self.w.characters[i].financial_setbacks=25
        self.e.collective.group_pressure(g,leader);self.e.society.refresh(leader)
        n=leader.needs['organizational_survival']
        self.assertIn('assume_local_office',[a for a,d,t in self.e.society.candidates(leader,n)])
        self.assertTrue(self.e.action_pressure.assess(leader,n,'assume_local_office',g.id)['eligible'])
        leader.profession='guarda';self.assertFalse(self.e.action_pressure.assess(leader,n,'assume_local_office',g.id)['eligible'])
    def test_05_resolution_reduces_collective_pressure(self):
        g=self.group();leader=self.w.characters[g.leader_id];self.e.collective.group_pressure(g,leader)
        before=g.action_pressure.value
        for i in g.member_ids:self.w.characters[i].financial_since=None;self.w.characters[i].money=30
        self.w.turn+=1;self.e.collective.group_pressure(g,leader)
        self.assertGreater(before,g.action_pressure.value);self.assertEqual(0,g.action_pressure.value)
    def test_06_incapable_faction_prepares_without_magic_resources(self):
        f,n=self.faction();self.p.social_state['last_report']=self.w.turn
        self.assertFalse(self.e.collective.faction_assessment(f,self.p)['eligible'])
        self.assertIn('faction_prepare',[a for a,d,t in self.e.society.candidates(self.p,n)])
        self.p.money=20;before=self.p.money+f.money
        self.e.action_pressure.refresh(self.p,[n]);self.assertTrue(self.act(self.p,n,'faction_prepare',f.id)[0])
        self.assertEqual(before,self.p.money+f.money);self.assertGreater(f.money,0)
    def test_07_capable_faction_acts_with_cost_and_ideology_filter(self):
        f,n=self.faction(True)
        for i in self.e.spatial.at(self.p.position):
            q=self.w.characters[i]
            if q.id not in f.member_ids and q.profession in ('guarda','soldado'):self.e.navigation.relocate(q,q.home)
        self.e.action_pressure.refresh(self.p,[n]);a=self.e.collective.faction_assessment(f,self.p)
        self.assertTrue(a['eligible']);before=self.e.items.count(self.t.id,'food')
        f.norms['allow_theft']=False;self.assertFalse(self.act(self.p,n,'faction_raid',f.id)[0]);f.norms['allow_theft']=True
        self.assertTrue(self.act(self.p,n,'faction_raid',f.id)[0]);self.assertEqual(2,before-self.e.items.count(self.t.id,'food'))
        self.assertEqual(2,self.e.items.count(f.id,'food'));self.assertGreater(self.p.fatigue,10)
        self.assertFalse(self.e.collective.faction_assessment(f,self.p)['eligible'])
        self.e.society.orders(self.p,f)
        self.assertIn('perform_assignment',[a for a,d,t in self.e.society.candidates(self.p,n)])
        f.money=2;before=f.money+self.p.money
        self.assertTrue(self.act(self.p,n,'perform_assignment',f.id)[0]);self.assertEqual(before,f.money+self.p.money)
        self.assertNotIn('order',f.assignments[self.p.id])
    def test_08_god_reacts_to_received_loss_not_remote_truth(self):
        god=next(iter(self.w.divinities.values()));god.values.update(compassion=90,honor=90,patience=40)
        for p in (self.p,self.q):self.prayer(p,god)
        for p in (self.p,self.q):
            p.religion='';p.beliefs[god.id]['believed_divine']=False
        self.assertEqual(0,self.e.faith.divine_assessment(god)['known_losses'])
        god.essence['requests']=[]
        for p in (self.p,self.q):
            self.e.recorder.emit('FaithReinterpreted','Abandono declarado controlado',p.id,god.id,god.location,
                context={'previous':'Culto de '+god.name,'current':''})
        before=god.energy;self.e.faith.tick()
        self.assertEqual(2,self.e.faith.divine_assessment(god)['known_losses']);self.assertEqual(before-20,god.energy)
        self.assertTrue(god.interventions)
        self.assertFalse(god.essence['requests']);self.assertEqual('',self.p.religion)
        event=next(x for x in self.w.history if x.id==god.interventions[-1])
        self.assertIn(event.context['source_fact'],[x['fact'] for x in god.essence['known_faith_losses']])
    def test_09_single_prayer_is_not_sufficient_cause(self):
        god=next(iter(self.w.divinities.values()));god.values.update(compassion=100,honor=100,patience=0)
        self.prayer(self.p,god);before=god.energy;self.e.faith.tick()
        self.assertFalse(god.interventions);self.assertEqual(before+.5 if self.w.turn%24==0 and before<100 else before,god.energy)
        self.assertFalse(self.e.faith.divine_assessment(god)['eligible'])
    def test_10_village_representation_travels_and_response_returns(self):
        village=next(t for t in self.w.towns.values() if t.kind=='vila' and t.office.get('representing_town'))
        p,q=[self.w.characters[i] for i in village.resident_ids][:2]
        for x in (p,q):
            self.e.navigation.relocate(x,village.market);x.financial_since=0;x.financial_setbacks=15;x.money=0
            x.personality.compassion=70;x.personality.ambition=x.personality.persistence=95
        self.e.graph.set(p.id,q.id,'confiança',90);self.e.graph.set(p.id,q.id,'amizade',90)
        self.e.society.refresh(q);self.act(q,q.needs['political_pressure'],'share_problem');self.e.society.refresh(p)
        g=self.e.society.form(p,'resource_pressure',None,p.needs['political_pressure']);self.assertIsNotNone(g)
        leader=self.w.characters[g.leader_id];prop=self.e.society.propose(leader,g);self.assertIsNotNone(prop)
        peer=next(self.w.characters[i] for i in g.member_ids if i!=leader.id)
        self.assertNotEqual(village.id,prop.town_id)
        n=self.e.needs.ensure(leader,'organizational_survival',70,'test','Representação física',leader.id);n.context['group_id']=g.id
        def visit(target):
            steps=0
            while leader.position.map_id!=target and steps<1000:
                old=leader.position;self.assertTrue(self.act(leader,n,'represent_travel',target)[0]);steps+=1;self.w.turn+=1
                if old.map_id==leader.position.map_id:self.assertLessEqual(abs(old.x-leader.position.x)+abs(old.y-leader.position.y),1)
            self.assertEqual(target,leader.position.map_id)
            while leader.position!=self.w.towns[target].market:self.e.navigation.approach(leader,self.w.towns[target].market,1);self.w.turn+=1
            return steps
        self.assertGreater(visit(prop.town_id),1);leader.hunger=70
        mayor=self.w.characters[self.w.towns[prop.town_id].mayor_id];self.e.navigation.relocate(mayor,leader.position)
        self.assertTrue(self.act(leader,n,'submit_proposal',prop.id)[0]);prop.solution='food_distribution'
        mayor.personality.compassion=100;mayor.personality.greed=0;mayor.personality.diligence=0
        self.assertTrue(self.e.society.resolve(mayor,prop)[0]);self.assertIn(prop.status,('accepted','partial'))
        self.assertEqual('submitted',g.proposal_knowledge[prop.id]['status'])
        self.assertFalse(any(f.kind=='PolicyDecided' and f.target_id==prop.id for f in peer.knowledge.values()))
        visit(village.id);self.assertEqual(village.id,leader.town_id)
        self.assertTrue(self.act(leader,n,'relay_response',g.id)[0]);self.assertEqual(prop.status,g.proposal_knowledge[prop.id]['status'])
        self.assertTrue(any(f.kind=='PolicyDecided' and f.target_id==prop.id for f in peer.knowledge.values()))
        self.assertEqual([],validate_world(self.w))
    def test_11_pressure_save_queries_and_deterministic_continuation(self):
        g=self.group();self.e.society.refresh(self.p);n=self.p.needs['organizational_survival']
        self.e.action_pressure.refresh(self.p,[n]);self.w.rng_state=self.e.rng.getstate()
        before=dumps(self.w);self.e.goals.solutions(self.p,n);self.assertEqual(before,dumps(self.w))
        other=Engine(loads(before));self.e.simulate(8);other.simulate(8)
        self.assertEqual(dumps(self.w),dumps(other.world));self.assertEqual([],validate_world(self.w))
        targets=list(self.w.characters)[:12]
        bulk=[self.e.needs.ensure(self.p,f'political_pressure:cache:{i}',60+i,'own_state',
            'Pressões concorrentes controladas',target) for i,target in enumerate(targets)]
        self.e.action_pressure.refresh(self.p,bulk);keys=set(self.p.action_pressures)
        records=self.w.metrics['ActionPressure:records_created:npc']
        selected=next(iter(self.p.action_pressures.values()));selected.failures=2
        self.w.turn+=1;self.e.action_pressure.refresh(self.p,bulk)
        self.assertEqual(keys,set(self.p.action_pressures));self.assertEqual(8,len(keys))
        self.assertEqual(records,self.w.metrics['ActionPressure:records_created:npc']);self.assertEqual(2,selected.failures)
