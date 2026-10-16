import unittest
from dataclasses import asdict

from procedural.engine import Engine
from procedural.generation import GenerationConfig, generate_world
from procedural.models import Group, Goal, Location
from procedural.persistence import dumps, loads
from procedural.validation import validate_world


class GeographyAccessTests(unittest.TestCase):
    def setUp(self):
        self.w=generate_world('Controlled-54',with_player=False,
                              config=GenerationConfig(kingdom_count=1,historical_turns=0))
        self.e=Engine(self.w)
        capital=next(iter(self.w.kingdoms.values())).capital_id
        self.p,self.q=[c for c in self.w.characters.values() if c.town_id==capital and c.profession in ('agricultor','cozinheiro')][:2]
        self.p.route_knowledge.clear();self.q.route_knowledge.clear()
        self.e.navigation.relocate(self.p,self.w.towns[capital].market)
        self.e.navigation.relocate(self.q,self.p.position)
        self.origin=capital
        self.route=next(r for r in self.w.routes.values() if r.origin==capital and r.destination in self.w.towns)
        self.target=self.route.destination
        for c in (self.p,self.q):
            self.e.items.create(c.id,'food',20);self.e.items.create(c.id,'water',20)
            self.e.geography.know_place(c,self.target,'test_known_place')

    def teach(self,p,route=None):
        r=route or self.route
        for id in (r.origin,r.destination):self.e.geography.learn(p,r,id,'controlled_map')

    def travel_until_arrived(self,p,limit=180):
        for _ in range(limit):
            self.w.turn+=1
            result=self.e.geography.step(p)
            self.assertTrue(result[0],result)
            if not p.journey:return
        self.fail('Viagem não concluiu dentro do limite físico.')

    def test_01_place_without_route_and_save_roundtrip(self):
        position=self.p.position
        self.assertFalse(self.e.geography.begin(self.p,self.target,'test')[0])
        self.assertEqual(position,self.p.position)
        self.assertIsNone(self.p.journey)
        restored=loads(dumps(self.w))
        self.assertEqual(len(restored.routes),len(self.w.routes))
        self.assertFalse(restored.characters[self.p.id].route_knowledge)
        # Receiving family news between decisions must also respect the memory cap.
        from procedural.models import Observation, Fact
        ids=[id for id in self.w.characters if id not in (self.p.id,self.q.id)][:64]
        self.p.observations={id:Observation(0,self.p.position,0,0,100) for id in ids}
        self.e.needs.ensure(self.p,f'family:{self.q.id}',40,'test','Localizar familiar',self.q.id)
        self.w.turn=1
        fact=Fact(self.w.allocate_id(),'PersonLocated',self.q.id,self.q.id,self.q.position,1,'Familiar encontrado',confidence=100)
        self.e.needs.personal.on_fact(self.p,fact)
        self.assertLessEqual(len(self.p.observations),64)
        self.assertIn(self.q.id,self.p.observations)


    def test_02_directions_enable_physical_trip_and_audit(self):
        self.teach(self.q);self.q.profession='guarda'
        self.assertTrue(self.e.geography.ask(self.p,self.target)[0])
        self.assertTrue(self.e.geography.plan(self.p,self.target))
        self.assertTrue(self.e.geography.begin(self.p,self.target,'instructions')[0])
        self.travel_until_arrived(self.p)
        self.assertEqual(self.p.position.map_id,self.target)
        self.assertEqual([],self.e.geography.audit())

    def test_03_multihop_has_no_unknown_edge(self):
        other=next(t for t in self.w.towns.values() if t.id not in (self.origin,self.target))
        self.e.geography.connect(self.target,other.id)
        second=next(r for r in self.w.routes.values() if {r.origin,r.destination}=={self.target,other.id})
        self.teach(self.p)
        self.e.geography.know_place(self.p,other.id,'location_only')
        self.assertIsNone(self.e.geography.plan(self.p,other.id))
        self.teach(self.p,second)
        plan=self.e.geography.plan(self.p,other.id)
        self.assertEqual([self.route.id,second.id],plan[0])
        self.assertTrue(self.e.geography.begin(self.p,other.id,'multihop')[0])
        self.travel_until_arrived(self.p,250)
        self.assertEqual([],self.e.geography.audit())

    def test_04_follow_and_escort_learn_after_walking(self):
        for mode in ('follow_person','escort'):
            self.setUp()
            self.teach(self.q)
            self.assertTrue(self.e.geography.begin(self.q,self.target,'guide')[0])
            self.assertTrue(self.e.geography.begin(self.p,self.target,'following',mode,self.q)[0])
            self.assertFalse(self.p.route_knowledge)
            for _ in range(200):
                self.w.turn+=1
                if self.q.journey:self.e.geography.step(self.q)
                if self.p.journey:self.e.geography.step(self.p)
                if not self.p.journey and not self.q.journey:break
            self.assertIsNone(self.p.journey)
            self.assertEqual(self.target,self.p.position.map_id)
            self.assertTrue(self.p.route_knowledge)
            self.assertEqual([],self.e.geography.audit())


    def test_05_poi_rumor_does_not_grant_route(self):
        from procedural.models import Fact
        point=next(x for x in self.w.points.values() if x.kind!='quartel-general')
        fact=Fact(self.w.allocate_id(),'POIRumor',self.q.id,point.id,self.q.position,0,
                  'Relato de caverna',confidence=60,context={'place_id':point.id})
        self.e.knowledge.learn(self.p,fact,False)
        self.assertEqual('RUMORED',self.p.place_knowledge[point.id]['state'])
        self.assertFalse(self.p.route_knowledge)
        self.assertFalse(self.e.geography.begin(self.p,point.id,'rumor')[0])

    def test_06_recruitment_requires_meeting_and_acceptance(self):
        f=next(iter(self.w.factions.values()));leader=self.w.characters[f.leader_id]
        self.p.profession='caçador';self.p.personality.courage=80;self.p.personality.ambition=80;self.p.personality.independence=30
        self.assertFalse(self.e.access.membership(self.p,f,True)[0])
        self.e.navigation.relocate(leader,self.p.position)
        self.assertTrue(self.e.access.invite(leader,f)[0])
        self.assertNotIn(self.p.id,f.member_ids)
        self.e.access.know_faction(self.p,f,'meeting')
        self.assertTrue(self.e.access.membership(self.p,f,True)[0])
        self.assertIn(self.p.id,f.member_ids)
        self.assertEqual(f.ranks[0],f.assignments[self.p.id]['rank'])

    def test_07_existing_group_can_formalize_without_new_money(self):
        third=next(c for c in self.w.characters.values() if c.id not in (self.p.id,self.q.id) and not c.organization_ids)
        self.e.navigation.relocate(third,self.p.position)
        self.w.turn=180
        need=self.e.needs.ensure(self.p,'organizational_survival',60,'test','Grupo duradouro')
        g=Group(self.w.allocate_id(),'Associação de ensaio',self.origin,'security',None,self.p.id,[self.p.id,self.q.id,third.id],0,need.id,investment=4,last_relevant=180)
        self.w.groups[g.id]=g
        for c in (self.p,self.q,third):c.money=25;c.group_ids.append(g.id)
        total=sum(c.money for c in self.w.characters.values())+sum(f.money for f in self.w.factions.values())
        f=self.e.society.found_faction(self.p,g,[self.p,self.q,third])
        self.assertIsNotNone(f)
        self.assertEqual(total,sum(c.money for c in self.w.characters.values())+sum(f.money for f in self.w.factions.values()))

    def test_08_castle_claim_and_inventory_are_real(self):
        point=next(x for x in self.w.points.values() if x.kind=='castelo abandonado')
        f=next(iter(self.w.factions.values()));leader=self.w.characters[f.leader_id]
        self.e.access.know_faction(self.p,f,'fixture');self.e.navigation.relocate(leader,self.p.position)
        self.p.profession='caçador';self.p.personality.courage=95;self.p.personality.ambition=95;self.p.personality.independence=5
        self.e.access.membership(self.p,f,True)
        self.e.navigation.relocate(leader,Location(point.id,4,4));self.e.navigation.relocate(self.p,leader.position)
        point.danger=0
        self.assertTrue(self.e.access.claim(leader,point,f)[0])
        self.assertEqual(point.id,f.headquarters_id)
        self.assertEqual(f.id,point.claimant_id)
        before=self.e.items.count(point.id,'food')+self.e.items.count(leader.id,'food')
        # A transferência conserva os mantimentos já existentes.
        self.e.items.consume(leader.id,'food',self.e.items.count(leader.id,'food'))
        before=self.e.items.count(point.id,'food')+self.e.items.count(leader.id,'food')
        goal=Goal(self.w.allocate_id(),0,'take_site_supplies',0,self.w.turn,point.id)
        self.assertTrue(self.e.access.execute(leader,goal,None)[0])
        self.assertEqual(before,self.e.items.count(point.id,'food')+self.e.items.count(leader.id,'food'))
        cave=next(x for x in self.w.points.values() if x.kind=='caverna')
        self.e.navigation.relocate(self.p,Location(cave.id,4,4))
        self.e.needs.ensure(self.p,'exploration',45,'test_resource_report','Buscar minério',cave.id)
        before_iron=self.e.items.count(self.p.id,'iron')+self.e.items.count(cave.id,'iron')
        self.assertTrue(self.e.access.explore(self.p,cave)[0])
        self.assertEqual(before_iron,self.e.items.count(self.p.id,'iron')+self.e.items.count(cave.id,'iron'))
        self.assertFalse(self.e.access.explore(self.p,cave)[0])
        self.e.access.refresh(self.p)
        self.assertEqual(self.p.home.map_id,self.p.needs['return_from_site'].target_id)


    def test_09_contact_travel_does_not_force_response_contract_is_optional(self):
        god=self.w.divinities[next(iter(self.p.beliefs))]
        self.e.access.teach_site(self.p,god.id,god.location,'test_tradition')
        self.p.devotion=95
        self.e.navigation.relocate(self.p,god.location)
        need=self.e.needs.ensure(self.p,'divine_contact',50,'test','Busca de contato',god.id)
        goal=Goal(self.w.allocate_id(),need.id,'seek_divine_contact',50,0,god.id,god.location)
        god.values['honor']=80;god.affinities[self.p.id]={'value':0,'deeds':0,'facts':{},'updated_at':0}
        self.assertTrue(self.e.access.execute(self.p,goal,need)[0])
        self.assertFalse(self.w.divine_contracts)
        god.affinities[self.p.id].update(value=45,deeds=3);self.w.turn=80
        self.assertTrue(self.e.access.execute(self.p,goal,need)[0])
        contract=next(iter(self.w.divine_contracts.values()))
        self.assertEqual('offered',contract.status)
        self.p.personality.independence=20
        accept=Goal(self.w.allocate_id(),need.id,'accept_contract',50,80,contract.id)
        self.e.access.execute(self.p,accept,need)
        self.assertEqual('active',contract.status)
        abandon=Goal(self.w.allocate_id(),need.id,'abandon_contract',50,80,contract.id)
        self.e.access.execute(self.p,abandon,need)
        self.assertEqual('abandoned',contract.status)
        self.assertEqual('active',contract.known_by_god)

    def test_10_invisible_god_cannot_be_physically_attacked(self):
        god=next(iter(self.w.divinities.values()))
        self.e.navigation.relocate(self.p,god.location);self.p.mythic_development=100
        self.assertFalse(self.e.faith.divine_death(self.p,god,'test'))
        self.assertTrue(god.alive)
        self.assertTrue(self.e.access.manifest(god,self.p.position,self.w.allocate_id()))
        self.assertTrue(self.e.access.physical_access(self.p,god))
        self.assertTrue(self.e.faith.divine_death(self.p,god,'controlled_confrontation'))
        self.assertFalse(god.alive)
        self.assertNotIn('actual_divinity',self.p.social_state)


if __name__=='__main__':unittest.main()
