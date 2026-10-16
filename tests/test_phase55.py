import unittest
from dataclasses import asdict
from procedural.generation import generate_world,GenerationConfig
from procedural.engine import Engine
from procedural.models import Group,Goal,Fact,Policy
from procedural.validation import validate_world


class InstitutionalTests(unittest.TestCase):
    def setUp(self):
        self.w=generate_world('Controlled-55',with_player=False,config=GenerationConfig(kingdom_count=1,historical_turns=0))
        self.e=Engine(self.w);self.t=next(t for t in self.w.towns.values() if t.capital)
        self.people=[c for c in self.w.characters.values() if c.town_id==self.t.id and c.category=='comum' and c.id!=self.t.mayor_id][:8]
        self.p,self.q,self.r,self.s=self.people[:4]
        for p in self.people:
            self.e.navigation.relocate(p,self.t.market);p.money=30;p.health=100;p.fatigue=10;p.hunger=p.thirst=30
            for name in ('compassion','diligence','persistence','ambition','courage'):setattr(p.personality,name,80)
            p.personality.independence=30;p.personality.honesty=80;p.personality.greed=20
            self.e.items.create(p.id,'food',2);self.e.items.create(p.id,'water',2)
            self.e.needs.ensure(p,'protection',65,'controlled_threat','Problema compartilhado',self.people[-1].id)
            for q in self.people:self.e.graph.set(p.id,q.id,'confiança',65)
        self.mayor=self.w.characters[self.t.mayor_id];self.e.navigation.relocate(self.mayor,self.t.market)
        self.t.money=100

    def group(self,members=None,cause='security'):
        members=members or [self.q,self.r]
        n=self.e.needs.ensure(members[0],'political_pressure',70,'fixture','Organização por causa conhecida')
        g=Group(self.w.allocate_id(),'Grupo controlado',self.t.id,cause,None,members[0].id,[p.id for p in members],0,n.id,pressure=75,last_relevant=0)
        g.plan={'meeting_place':asdict(self.t.market),'meeting_period':24};self.w.groups[g.id]=g
        for p in members:p.group_ids.append(g.id)
        return g

    def share(self,p,cause='security'):
        self.e.recorder.emit('ProblemShared','Problema comunicado',p.id,location=p.position,historical=True,context={'cause':cause,'subject':None,'severity':75})

    def proposal(self,g=None):
        g=g or self.group([self.p,self.q,self.r]);return self.e.institutions.propose(self.w.characters[g.leader_id],g)

    def policy(self,sector='WATER'):
        g=self.group([self.p,self.q,self.r], 'water_access' if sector=='WATER' else 'resource_pressure')
        if sector not in ('WATER','FOOD'):g.subject_id=self.people[-1].id
        prop=self.proposal(g);prop.sector=sector;prop.desired_effect='increase_capacity' if sector=='WATER' else 'produce'
        return self.e.institutions.create_policy(self.mayor,prop)

    def total_money(self):
        return sum(x.money for coll in (self.w.characters,self.w.towns,self.w.factions,self.w.groups,self.w.institutional_policies) for x in coll.values())

    def faction(self):
        f=next(iter(self.w.factions.values()))
        old=self.w.characters[f.leader_id]
        if f.id in old.organization_ids:old.organization_ids.remove(f.id)
        f.leader_id=self.q.id;f.member_ids=[self.q.id];self.q.organization_ids.append(f.id)
        f.assignments={self.q.id:{'rank':f.ranks[-1],'joined_at':0,'deeds':0}}
        f.money=8;f.norms.update(risk=.2,dues=1);self.e.items.create(f.id,'food',4);self.e.items.create(f.id,'water',4)
        self.e.access.know_faction(self.p,f,'controlled_contact')
        return f

    def test_01_known_compatible_group_precedes_creation(self):
        g=self.group();self.e.institutions.know_group(self.p,g,'meeting')
        self.share(self.q);n=self.e.needs.ensure(self.p,'political_pressure',70,'test','Buscar organização')
        before=len(self.w.groups);found=self.e.society.form(self.p,'security',None,n)
        self.assertEqual(g.id,found.id);self.assertEqual(before,len(self.w.groups));self.assertIn(self.p.id,g.member_ids)
        # A consolidação deve sobreviver à validação além do limite antigo de 16.
        for q in self.w.characters.values():
            if q.id in g.member_ids:continue
            self.e.navigation.relocate(q,self.t.market)
            self.e.needs.ensure(q,'protection',65,'test','Problema comum',self.people[-1].id)
            self.e.graph.set(q.id,g.leader_id,'confiança',65);q.personality.compassion=80
            self.e.institutions.know_group(q,g,'meeting')
            self.assertTrue(self.e.institutions.join(q,g)[0])
            if len(g.member_ids)==20:break
        self.assertEqual(20,len(g.member_ids));self.assertEqual([],validate_world(self.w))

    def test_02_unknown_group_does_not_prevent_legitimate_creation(self):
        existing=self.group();self.e.navigation.relocate(self.q,self.q.home);self.e.navigation.relocate(self.r,self.r.home)
        self.share(self.s);n=self.e.needs.ensure(self.p,'political_pressure',70,'test','Causa local')
        created=self.e.society.form(self.p,'security',None,n)
        self.assertNotIn(existing.id,self.p.known_groups);self.assertIsNotNone(created);self.assertNotEqual(existing.id,created.id)

    def test_03_known_hostile_leader_allows_separate_group(self):
        g=self.group();self.e.institutions.know_group(self.p,g,'prior_contact');self.e.graph.set(self.p.id,self.q.id,'confiança',0)
        self.share(self.s);n=self.e.needs.ensure(self.p,'political_pressure',70,'test','Problema')
        result=self.e.society.form(self.p,'security',None,n)
        self.assertIsNotNone(result);self.assertNotEqual(g.id,result.id)
        self.assertTrue(any(e.kind=='GroupJoinRejected' and e.context['reason']=='hostility_or_distrust' for e in self.w.history))

    def test_04_compatible_proposal_is_reused(self):
        a=self.group([self.p,self.q]);first=self.proposal(a)
        b=self.group([self.r,self.s]);second=self.proposal(b)
        self.assertEqual(first.id,second.id);self.assertEqual(1,len(self.w.proposals));self.assertIn(b.id,first.supporting_group_ids)
        first.status='submitted';self.t.office['known_proposals']=[first.id];self.t.office['public_proposals']=[first.id]
        self.e.society.appoint(self.t,self.s,'controlled_succession')
        self.assertEqual([first.id],self.t.office['public_proposals']);self.assertEqual(self.s.id,first.target_id)

    def test_05_shared_people_are_counted_once(self):
        a=self.group([self.p,self.q]);prop=self.proposal(a)
        self.e.institutions.deliver_support(self.p,prop,a);before_pressure=prop.pressure
        b=self.group([self.p,self.r]);self.e.institutions.support(self.p,b,prop)
        self.e.institutions.support(self.p,b,prop)
        self.e.institutions.deliver_support(self.p,prop,b);self.assertGreater(prop.pressure,before_pressure)
        self.assertEqual(3,prop.support);self.assertEqual(2,len(prop.supporting_group_ids));self.assertEqual(3,len(set(prop.supporter_ids)))
        f=self.faction();f.member_ids.append(self.s.id);self.s.organization_ids.append(f.id)
        self.e.institutions.remember(self.q.known_proposals,prop.id,{'source':'public_submission'})
        self.assertTrue(self.e.institutions.faction_support(self.q,f,prop)[0])
        self.assertEqual(4,prop.support);self.assertEqual([f.id],prop.supporting_faction_ids)
        self.assertFalse(self.e.institutions.faction_support(self.q,f,prop)[0]);self.assertEqual(4,prop.support)

    def test_06_pressure_changes_mayor_judgment(self):
        prop=self.proposal();m=self.mayor
        m.personality.compassion=m.personality.diligence=85;m.personality.greed=5;m.personality.persistence=30
        prop.urgency=5;prop.supporter_ids=[self.p.id];prop.support=1;prop.delivered_supporter_ids=list(prop.supporter_ids)
        low=self.e.society.decision_scores(m,prop)
        prop.urgency=90;prop.supporter_ids=[p.id for p in self.people];prop.support=8;prop.delivered_supporter_ids=list(prop.supporter_ids);self.w.turn=60
        high=self.e.society.decision_scores(m,prop)
        self.assertGreater(high['approve'],low['approve']);self.assertNotEqual(max(low,key=low.get),max(high,key=high.get))
        self.t.money=0;m.fatigue=90;m.personality.independence=95;m.personality.greed=95
        prop.supporter_ids=prop.delivered_supporter_ids=[];prop.support=0;prop.urgency=0;self.w.turn=0
        ignored=self.e.institutions.decision_scores(m,prop)
        self.assertEqual('ignore',max(ignored,key=ignored.get))
        prop.status='ignored';prop.decided_at=0;prop.result={'political_pressure':2};self.t.office['known_proposals']=[prop.id]
        self.w.turn=30;self.e.society.refresh(m)
        self.assertEqual(prop.id,m.needs['governance'].context['proposal_id']);self.assertEqual([],validate_world(self.w))

    def test_07_approval_reserves_budget_without_creating_resources(self):
        prop=self.proposal();prop.status='submitted';self.t.office['known_proposals']=[prop.id]
        self.mayor.personality.compassion=self.mayor.personality.diligence=100;self.mayor.personality.greed=0
        before_money=self.total_money();before={k:self.e.items.count(self.t.id,k) for k in ('food','water','iron','wood')}
        self.assertTrue(self.e.society.resolve(self.mayor,prop)[0]);self.assertIsNotNone(prop.policy_id)
        self.assertEqual(before_money,self.total_money());self.assertEqual(before,{k:self.e.items.count(self.t.id,k) for k in before})
        self.assertEqual('active',self.w.groups[prop.group_id].status)

    def test_08_water_capacity_and_food_follow_material_work(self):
        water=self.policy();self.p.profession='mineiro';money=self.total_money();stock=self.e.items.count(self.t.id,'water')
        wood=self.e.items.count(self.t.id,'wood');iron=self.e.items.count(self.t.id,'iron')
        need=self.e.needs.ensure(self.p,'institutional_work',70,'known_policy','Trabalho',water.id)
        self.assertTrue(any(x.action=='policy_work' for x in self.e.goals.solutions(self.p,need)))
        self.assertTrue(self.e.institutions.policy_work(self.p,water)[0]);self.assertTrue(self.e.institutions.policy_work(self.p,water)[0])
        self.assertEqual(100,self.t.infrastructure['water_daily']);self.assertEqual(stock,self.e.items.count(self.t.id,'water'))
        self.assertEqual(wood-2,self.e.items.count(self.t.id,'wood'));self.assertEqual(iron-2,self.e.items.count(self.t.id,'iron'));self.assertEqual(money,self.total_money())
        food=self.policy('FOOD');self.p.profession='cozinheiro'
        balance=3*self.e.items.count(self.t.id,'grain')+self.t.grain_credit+2*self.e.items.count(self.t.id,'food')
        self.assertTrue(self.e.institutions.policy_work(self.p,food)[0])
        self.assertEqual(balance,3*self.e.items.count(self.t.id,'grain')+self.t.grain_credit+2*self.e.items.count(self.t.id,'food'))
        transport=self.policy('TRANSPORT');self.p.profession='comerciante'
        route=next(x for x in self.w.routes.values() if self.t.id in (x.origin,x.destination) and
                   (x.destination if x.origin==self.t.id else x.origin) in self.w.towns)
        dest=route.destination if route.origin==self.t.id else route.origin
        self.e.geography.know_place(self.p,dest,'controlled_directions')
        for origin in (route.origin,route.destination):self.e.geography.learn(self.p,route,origin,'controlled_directions')
        self.e.items.create(self.p.id,'food',20);self.e.items.create(self.p.id,'water',20)
        grain=self.e.items.count(self.t.id,'grain');money=self.total_money()
        self.assertTrue(self.e.institutions.policy_work(self.p,transport)[0]);job=transport.effects['transport_jobs'][self.p.id]
        self.assertEqual(grain-3,self.e.items.count(self.t.id,'grain'));self.assertEqual(money,self.total_money());self.assertEqual(0,transport.spent)
        destination=job['destination'];before=self.e.items.count(destination,'grain')
        self.assertTrue(self.e.geography.begin(self.p,destination,'policy_transport')[0])
        for _ in range(100):
            self.w.turn+=1;self.e.geography.step(self.p)
            if not self.p.journey:break
        self.assertIsNone(self.p.journey);self.e.navigation.relocate(self.p,self.w.towns[destination].market)
        self.assertTrue(self.e.institutions.policy_work(self.p,transport)[0]);self.assertEqual(before+3,self.e.items.count(destination,'grain'))
        self.assertEqual(money,self.total_money());self.assertEqual(1,transport.spent)

    def test_09_policy_can_stall_without_material(self):
        policy=self.policy();self.p.profession='mineiro';self.e.items.consume(self.t.id,'wood',self.e.items.count(self.t.id,'wood'))
        money=self.total_money();stock=self.e.items.count(self.t.id,'water')
        self.assertFalse(self.e.institutions.policy_work(self.p,policy)[0]);self.assertEqual('stalled',policy.status)
        self.assertEqual(80,self.t.infrastructure['water_daily']);self.assertEqual(money,self.total_money());self.assertEqual(stock,self.e.items.count(self.t.id,'water'))

    def test_10_persistent_group_formalizes_with_origin_and_real_funds(self):
        g=self.group([self.p,self.q,self.r]);g.investment=4;g.failures=2;self.w.turn=180
        before=self.total_money();f=self.e.institutions.formalization(self.p,g,[self.p,self.q,self.r],True)
        self.assertIsNotNone(f);self.assertEqual(g.id,f.norms['origin_group_id']);self.assertEqual(before,self.total_money());self.assertEqual('faction',g.status)

    def test_11_capability_requires_profession_and_physical_supplies(self):
        f=self.faction();self.q.profession='guarda'
        self.assertTrue(self.e.institutions.capabilities(f,self.q)['patrol'])
        self.e.items.consume(self.q.id,'water',self.e.items.count(self.q.id,'water'))
        self.assertFalse(self.e.institutions.capabilities(f,self.q)['patrol'])
        goal=Goal(self.w.allocate_id(),0,'institutional_patrol',0,self.w.turn,f.id)
        self.assertFalse(self.e.institutions.execute(self.q,goal,None)[0])

    def test_12_invitation_accept_reject_defer_resume_and_condition(self):
        f=self.faction();self.p.fatigue=90
        self.assertTrue(self.e.access.membership(self.p,f,True)[0]);self.assertEqual('deferred',f.norms['invitations'][self.p.id]['status'])
        self.p.fatigue=10;self.w.turn=9;self.e.institutions.refresh(self.p)
        self.assertIn('affiliation',self.p.needs);self.assertTrue(self.e.access.membership(self.p,f)[0]);self.assertIn(self.p.id,f.member_ids)
        self.e.access.know_faction(self.r,f,'meeting');self.r.personality.independence=95
        self.assertTrue(self.e.access.membership(self.r,f,True)[0]);self.assertEqual('rejected',f.norms['invitations'][self.r.id]['status'])
        self.e.access.know_faction(self.s,f,'meeting');self.s.profession='guarda';f.norms['risk']=.8
        for id in list(self.s.inventory):
            if self.w.items[id].kind=='weapon':self.e.items.consume(self.s.id,'weapon')
        self.assertTrue(self.e.access.membership(self.s,f,True)[0]);self.assertEqual('conditioned',f.norms['invitations'][self.s.id]['status'])
        item=self.e.items.create(f.id,'weapon');self.assertTrue(self.e.access.membership(self.s,f)[0]);self.assertIn(self.s.id,f.member_ids);self.assertNotIn(item.id,f.inventory)

    def test_13_authority_reacts_only_after_learning_illegal_action(self):
        f=self.faction();self.e.navigation.relocate(self.mayor,self.mayor.home)
        event=self.e.institutions.emit('FactionAction',self.q,f.id,faction_id=f.id,illegal=True,action='institutional_raid')
        self.assertNotIn(self.t.id,f.local_status)
        fact=Fact(event.id,event.kind,event.actor_id,event.target_id,event.location,event.turn,event.description,confidence=100,source_kind='direct',context=event.context)
        self.e.knowledge.learn(self.mayor,fact,True)
        self.assertEqual('RESTRICTED',f.local_status[self.t.id]['status']);self.assertEqual([event.id],f.local_status[self.t.id]['sources'])
        for _ in range(2):
            ev=self.e.institutions.emit('FactionAction',self.q,f.id,faction_id=f.id,illegal=True,action='institutional_raid')
            self.e.knowledge.learn(self.mayor,Fact(ev.id,ev.kind,ev.actor_id,ev.target_id,ev.location,ev.turn,ev.description,
                                                confidence=100,source_kind='direct',context=ev.context),True)
        self.assertEqual('ILLEGAL',f.local_status[self.t.id]['status']);self.assertEqual(3,len(f.local_status[self.t.id]['sources']))

    def test_14_criminal_cooperation_uses_generic_group_and_faction(self):
        for p in (self.p,self.q,self.r):
            p.personality.honesty=15;p.personality.greed=80
            for _ in range(2):self.e.recorder.emit('ItemStolen','Crime próprio conhecido',p.id,self.t.id,p.position,historical=True)
        self.assertEqual('criminal_cooperation',self.e.society.pressure(self.p)[0])
        self.share(self.q,'criminal_cooperation');self.share(self.r,'criminal_cooperation')
        n=self.e.needs.ensure(self.p,'political_pressure',70,'known_crime_cooperation','Cooperar com conhecidos')
        g=self.e.society.form(self.p,'criminal_cooperation',None,n);self.assertIsInstance(g,Group)
        g.leader_id=self.p.id;g.investment=4;g.failures=2;self.w.turn=180
        f=self.e.institutions.formalization(self.p,g,[self.p,self.q,self.r],True)
        self.assertIsNotNone(f);self.assertTrue(f.norms['allow_theft']);self.assertEqual('criminal_cooperation',f.norms['cause'])

if __name__=='__main__':unittest.main()
