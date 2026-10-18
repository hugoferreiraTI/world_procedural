"""Ações espaciais acopladas a Need/Goal, Sociedade, Fé, itens e conhecimento existentes."""
from .organization_context import organization_id, bind_organization
from dataclasses import asdict

from .models import DivineContract, Group, Location

ACTIONS = {'take_site_supplies','explore_poi','claim_location','invite_person','request_membership',
           'answer_invitation','store_supplies','seek_divine_contact','accept_contract','refuse_contract',
           'abandon_contract','form_expedition','follow_expedition','formalize_organization'}


class AccessActions:
    def __init__(self, engine):
        self.e, self.w = engine, engine.world
        self.e.bus.subscribe('DivineMessage', self.contract_message)
        self.e.bus.subscribe('*', self.route_history)

    def emit(self, kind, p, target=None, **context):
        return self.e.recorder.emit(kind, f'{p.name}: {kind}.',p.id,target,p.position,historical=True,context=context)

    def bootstrap(self):
        for god in self.w.divinities.values():
            self.w.sacred_sites.setdefault(god.location.map_id, {'god':god.id,'position':asdict(god.location),'source':'regional_tradition'})
        for p in self.w.characters.values():
            for god in self.w.divinities.values():
                if p.beliefs.get(god.id,{}).get('believed_divine') and p.devotion>=65:
                    self.teach_site(p,god.id,god.location,'cultural_pilgrimage_tradition')
            for fid in p.organization_ids:
                self.know_faction(p,self.w.factions[fid],'member')

    def teach_site(self,p,gid,location,source,source_fact=None):
        if gid in p.known_sacred_sites:return
        p.known_sacred_sites[gid]={'position':asdict(location),'source':source,'source_fact':source_fact,'learned_at':self.w.turn}
        self.e.geography.know_place(p,location.map_id,source,80,source_id=source_fact)
        self.emit('SacredSiteKnown',p,gid,place_id=location.map_id,source=source,source_fact=source_fact)

    def know_faction(self,p,f,source,source_fact=None):
        if f.id in p.known_factions:return
        p.known_factions[f.id]={'learned_at':self.w.turn,'source':source,'source_fact':source_fact,'headquarters':f.headquarters_id}
        self.e.geography.know_place(p,f.headquarters_id,source,80,source_id=source_fact)
        self.emit('FactionKnown',p,f.id,headquarters=f.headquarters_id,source=source,source_fact=source_fact)

    def on_fact(self,p,fact):
        if fact.kind in ('FactionKnown','FactionInvite','FactionMemberJoined','FactionHQChanged'):
            fid=fact.context.get('faction_id') or fact.target_id
            f=self.w.factions.get(fid)
            if f and fact.confidence>=30:self.know_faction(p,f,'contact_report',fact.event_id)
        if fact.kind=='SacredSiteKnown' and fact.target_id in self.w.divinities and fact.confidence>=60:
            site=self.w.sacred_sites.get(fact.context.get('place_id'))
            if site:self.teach_site(p,fact.target_id,Location(**site['position']),'received_tradition',fact.event_id)
        if fact.kind=='DivineManifestation' and fact.location and fact.confidence>=60:
            self.teach_site(p,fact.actor_id,fact.location,'manifestation_report',fact.event_id)

    def route_history(self,event):
        if event.kind not in ('CharacterKilled','CharacterDied','ItemStolen','CharacterAttacked'):return
        p=self.w.characters.get(event.actor_id) or self.w.characters.get(event.target_id)
        if p and p.journey:
            route=self.w.routes[p.journey.route_ids[p.journey.leg]]
            route.history.append(event.id);del route.history[:-16]
        if event.kind in ('CharacterKilled','CharacterDied'):
            q=self.w.characters.get(event.target_id)
            point=self.w.points.get(q.position.map_id) if q else None
            if point:point.remains.append(q.id)

    def refresh(self,p):
        if p.is_player:return
        # Conhecimento de uma organização nasce de encontro, não de inventário global de candidatos.
        for id in self.e.spatial.at(p.position):
            if id==p.id:continue
            for fid in self.w.characters[id].organization_ids:
                f=self.w.factions.get(fid)
                if f and f.status=='active':self.know_faction(p,f,'member_encounter')
        for fid in p.organization_ids:
            f=self.w.factions.get(fid)
            if not f or f.status!='active':continue
            if p.id==f.leader_id and (len(f.member_ids)<4 or f.money<4):
                reason='few_members' if len(f.member_ids)<4 else 'resource_need'
                if not f.norms.get('recruitment_interest'):
                    f.norms['recruitment_interest']=reason
                    self.emit('FactionRecruitmentInterest',p,f.id,reason=reason,members=len(f.member_ids))
                need=self.e.needs.ensure(p,'organizational_access',53,'organization',
                    'Procurar pessoas e recursos para a organização',f.id)
                need.context['faction_id']=f.id
        invitations=[(f,record) for f in self.w.factions.values() if (record:=f.norms.get('invitations',{}).get(p.id)) and record['status']=='offered' and f.id in p.known_factions]
        if invitations and not p.organization_ids:
            f,record=invitations[0]
            need=self.e.needs.ensure(p,'affiliation',43,'invitation','Responder convite conhecido',f.id)
            need.context['invitation']=True
        elif not p.organization_ids and p.personality.ambition>=65 and (p.money<15 or any(a.domain in ('belong','recognition','become_stronger') and a.status=='active' for a in p.aspirations)):
            candidates=[fid for fid in p.known_factions if self.w.factions.get(fid) and self.w.factions[fid].status=='active']
            if candidates:self.e.needs.ensure(p,'affiliation',36,'known_organization','Buscar adesão por interesse próprio',candidates[0])
        if p.access_state.get('contact_after',0)<=self.w.turn and p.devotion>=80 and p.known_sacred_sites and (p.personality.ambition>=65 or p.emotions.losses or p.emotions.desperation>=55):
            gid=next(iter(p.known_sacred_sites))
            n=self.e.needs.ensure(p,'divine_contact',min(65,35+p.devotion*.15),'personal_faith','Buscar contato por devoção, ambição ou perda',gid)
            n.context['source_fact']=p.beliefs.get(gid,{}).get('source_fact')
            if not p.access_state.get('contact_intent'):
                p.access_state['contact_intent']=True
                self.emit('SeekDivineContact',p,gid,cause='loss' if p.emotions.losses else 'devotion_and_ambition',source_fact=n.context['source_fact'])
        else:self.e.needs.satisfy(p,'divine_contact')
        for cid,c in self.w.divine_contracts.items():
            if c.mortal!=p.id:continue
            if c.status=='active' and self.w.turn>c.conditions.get('deadline',self.w.turn):
                c.status='failed';self.emit('DivineContractBroken',p,c.god,contract_id=c.id,status='failed')
            if c.status=='offered' or c.status=='active' and p.personality.independence>=85:
                self.e.needs.ensure(p,'divine_contract',48,'audience','Responder ou reconsiderar pacto conhecido',cid)
        known=[id for id,k in p.place_knowledge.items() if id in self.w.points and k.get('confidence',0)>=60 and p.access_state.get(f'explored:{id}') is None]
        if known and not p.organization_ids and (p.profession in ('mineiro','caçador','lenhador') and p.money<15 or p.personality.ambition>=85 and p.personality.independence>=65):
            target=known[0]
            self.e.needs.ensure(p,'exploration',35+p.personality.ambition*.12,'known_site','Buscar recurso, abrigo ou descoberta em lugar conhecido',target)
        else:self.e.needs.satisfy(p,'exploration')
        for id in p.group_ids:
            g=self.w.groups.get(id)
            if g and g.plan.get('purpose')=='expedition' and g.status=='active' and p.access_state.get(f'explored:{g.subject_id}') is None:
                self.e.needs.ensure(p,'exploration',52,'expedition','Participar de expedição aceita',g.subject_id)
        for fid in p.organization_ids:
            f=self.w.factions.get(fid)
            if f and p.id==f.leader_id and (not self.e.geography.place(f.headquarters_id) or f.norms.get('need_new_base')):
                sites=[id for id in p.place_knowledge if id in self.w.points and self.w.points[id].kind in ('castelo abandonado','caverna')]
                if sites:
                    need=self.e.needs.ensure(p,'organizational_base',55,'organization','Buscar sede em abrigo conhecido',sites[0]);need.context['faction_id']=f.id
        if p.position.map_id in self.w.points and p.access_state.get(f'explored:{p.position.map_id}') is not None and p.home.map_id!=p.position.map_id:
            self.e.needs.ensure(p,'return_from_site',48,'exploration_completed','Retornar por caminho conhecido após explorar',p.home.map_id)
        else:self.e.needs.satisfy(p,'return_from_site')
        if p.journey:
            self.e.needs.ensure(p,'spatial_journey',58,'journey','Prosseguir viagem já iniciada',p.journey.destination)
        else:self.e.needs.satisfy(p,'spatial_journey')

    def faction_fit(self,p,f):
        profession = p.profession in ({'caçador','lenhador'} if f.purpose=='hunters' else {'guarda','caçador','soldado'} if f.purpose=='mercenaries' else {'agricultor','cozinheiro','ferreiro','comerciante','guarda'})
        return 35*profession + p.personality.courage*.25 + p.personality.ambition*.2 + (10 if p.money<15 else 0)

    def candidates(self,p,n):
        geo=self.e.geography
        if n.kind=='return_from_site':return geo.candidates(p,n.target_id,'return_from_exploration',n)
        if n.kind=='spatial_journey':return [('route_travel',None,p.journey.destination)] if p.journey else []
        if n.kind in ('rest','food','water','recovery') and p.position.map_id not in self.w.towns:
            if n.kind in ('rest','recovery'):return [('sleep',None,None)]
            if p.position.map_id in self.w.points and self.e.items.count(p.position.map_id,'food' if n.kind=='food' else 'water'):
                return [('take_site_supplies',None,p.position.map_id)]
        if n.kind=='organizational_base':
            if p.position.map_id!=n.target_id:return geo.candidates(p,n.target_id,'organizational_base',n)
            return [('claim_location',Location(n.target_id,self.w.maps[n.target_id].width//2,self.w.maps[n.target_id].height//2),n.target_id)]
        if n.kind=='organizational_access':
            f=self.w.factions.get(n.target_id)
            if not f or f.leader_id!=p.id:return []
            if p.position.map_id in self.w.points:
                if self.e.items.count(p.id,'food')>3 and self.w.turn-p.access_state.get('last_storage',-1000)>=24:return [('store_supplies',None,f.id)]
                destinations=[rk.destination for rk in p.route_knowledge.values() if rk.origin==p.position.map_id and rk.destination in self.w.towns]
                return geo.candidates(p,destinations[0],'recruitment',n) if destinations else []
            local=self.w.towns.get(p.position.map_id)
            if not local:return []
            if p.position!=local.market:return [('invite_person',local.market,f.id)]
            choices=[]
            if self.w.turn-p.access_state.get('last_invite',-1000)>=6:
                choices.append(('invite_person',None,f.id))
            if self.e.items.count(p.id,'food')>3 or p.money>18:choices.append(('store_supplies',None,f.id))
            if len(f.member_ids)>=3 and self.e.items.count(p.id,'food')>=3 and p.money<=18:
                return geo.candidates(p,f.headquarters_id,'headquarters',n)
            return choices
        if n.kind=='affiliation':
            f=self.w.factions.get(n.target_id)
            if not f:return []
            record=f.norms.get('invitations',{}).get(p.id)
            leader=self.w.characters.get(f.leader_id)
            if not leader or not leader.alive:return []
            if any(id in self.e.spatial.at(p.position) for id in f.member_ids):return [('answer_invitation' if record else 'request_membership',None,f.id)]
            known=p.observations.get(leader.id)
            if known and self.w.turn-known.turn<=24 and known.position.map_id==p.position.map_id:return [('answer_invitation' if record else 'request_membership',known.position,f.id)]
            return geo.candidates(p,p.known_factions[f.id]['headquarters'],'membership',n)
        if n.kind=='exploration':
            target=n.target_id;point=self.w.points.get(target)
            if not point:return []
            if p.position.map_id!=target:
                groups=[self.w.groups[i] for i in p.group_ids if i in self.w.groups and self.w.groups[i].plan.get('purpose')=='expedition']
                if groups and groups[0].leader_id!=p.id:
                    guide=self.w.characters[groups[0].leader_id]
                    if guide.position==p.position and guide.journey:return [('follow_expedition',None,guide.id)]
                choices=geo.candidates(p,target,'exploration',n)
                if point.danger>=20 and not groups and len(p.group_ids)<3 and self.e.spatial.at(p.position):
                    choices.append(('form_expedition',None,target))
                return choices
            center=Location(target,self.w.maps[target].width//2,self.w.maps[target].height//2)
            return [('explore_poi',center,target)]
        if n.kind=='divine_contact':
            site=p.known_sacred_sites.get(n.target_id)
            if not site:
                self.e.observability.gate('seek_divine_contact','NO_SACRED_SITE',n.target_id)
                return []
            location=Location(**site['position'])
            if p.position.map_id!=location.map_id:return geo.candidates(p,location.map_id,'divine_contact',n)
            return [('seek_divine_contact',location,n.target_id)]
        if n.kind=='divine_contract':
            contract=self.w.divine_contracts.get(n.target_id)
            if contract and contract.status=='active':return [('abandon_contract',None,n.target_id)]
            return [('accept_contract',None,n.target_id),('refuse_contract',None,n.target_id)]
        if n.kind=='organizational_survival':
            g=self.w.groups.get(organization_id(n.context,'group'))
            if g and self.e.institutions.can_formalize(p,g,[self.w.characters[i] for i in self.e.spatial.at(p.position)])['eligible']:
                return [('formalize_organization',None,g.id)]
        return []

    def invite(self,p,f):
        if not f or f.leader_id!=p.id or len(f.member_ids)>=24:return False,'Liderança indisponível.'
        invitations=f.norms.setdefault('invitations',{})
        retired=[id for id,x in invitations.items() if x.get('status')!='offered']
        for id in retired[:-24]:invitations.pop(id)
        for id in self.e.spatial.at(p.position):
            q=self.w.characters[id]
            if q.id==p.id or q.organization_ids or q.id in invitations or self.faction_fit(q,f)<50:continue
            self.know_faction(q,f,'personal_invitation')
            invitations[q.id]={'status':'offered','created_at':self.w.turn,'inviter':p.id,'terms':self.e.institutions.invitation_info(p,f)}
            p.access_state['last_invite']=self.w.turn
            self.emit('FactionInvite',p,f.id,candidate=q.id,headquarters=f.headquarters_id,reason=f.norms.get('recruitment_interest'))
            return True,'Convite presencial entregue; aceitação pertence ao candidato.'
        p.access_state['last_invite']=self.w.turn
        return False,'Nenhum candidato local disponível e coerente.'

    def membership(self,p,f,request=False):
        return self.e.institutions.membership(p,f,request)

    def expedition(self,p,point):
        if any(self.w.groups.get(i) and self.w.groups[i].plan.get('purpose')=='expedition' for i in p.group_ids):return False,'Expedição já existente.'
        peers=[self.w.characters[i] for i in self.e.spatial.at(p.position) if i!=p.id and self.w.characters[i].alive and len(self.w.characters[i].group_ids)<3 and self.e.graph.value(p.id,i,'confiança',10)>=30 and self.w.characters[i].personality.courage>=40]
        if not peers:return False,'Ninguém presente aceitou a expedição.'
        need=p.needs.get('exploration')
        if not need:return False,'Falta motivo de exploração.'
        members=[p]+peers[:2]
        g=Group(self.w.allocate_id(),f'Expedição a {point.name}',p.town_id,'expedition',point.id,p.id,[q.id for q in members],self.w.turn,need.id,
                last_relevant=self.w.turn,plan={'purpose':'expedition','destination':point.id})
        self.w.groups[g.id]=g
        for q in members:
            q.group_ids.append(g.id);self.e.geography.know_place(q,point.id,'accepted_expedition',80)
        self.emit('ExpeditionFormed',p,g.id,place_id=point.id,members=g.member_ids,cause=need.reason)
        return True,'Grupo temporário aceito presencialmente; cada membro ainda deve viajar.'

    def explore(self,p,point):
        if not point or p.position.map_id!=point.id or p.access_state.get(f'explored:{point.id}') is not None:return False,'Local não alcançado ou já explorado.'
        motive=p.needs.get('exploration')
        if not motive:return False,'Exploração sem motivo pessoal.'
        capacity=self.e.conflicts.power(p)+p.personality.courage*.3
        company=sum(self.w.characters[i].position.map_id==point.id for g in self.w.groups.values() if g.plan.get('purpose')=='expedition' and p.id in g.member_ids for i in g.member_ids if i!=p.id and self.w.characters[i].alive)
        damage=max(0,int(point.danger-capacity-company*8))
        if damage:self.e.recovery.damage(p,min(18,damage),'exploration')
        moved=[]
        for id,amount in list(point.inventory.items()):
            if self.w.items[id].kind not in ('iron','tool','weapon'):continue
            item=self.e.items.transfer(point.id,p.id,id,min(2,amount));moved.append(item.id)
            if len(moved)>=2:break
        p.fatigue=min(100,p.fatigue+8)
        p.access_state[f'explored:{point.id}']=self.w.turn
        self.e.geography.know_place(p,point.id,'explored',state='EXPLORED')
        event=self.emit('POIExplored',p,point.id,place_id=point.id,motive=motive.reason,items=moved,damage=damage,depth=point.depth,remains=list(point.remains))
        point.history.append(event.id);del point.history[:-16]
        self.e.needs.satisfy(p,'exploration')
        if p.health<=0:self.e.finish_death(p,'exploration')
        return True,'Recursos existentes encontrados, risco e custo físico aplicados.'

    def claim(self,p,point,f):
        if not point or not f or f.leader_id!=p.id or p.position.map_id!=point.id or point.kind not in ('castelo abandonado','caverna'):
            return False,'Reivindicação exige liderança presente em abrigo utilizável.'
        if not any(q.id!=p.id and q.position.map_id==point.id for q in self.e.society.living(f.member_ids)):
            return False,'Ocupação organizacional exige companhia presente.'
        if point.claimant_id and point.claimant_id!=f.id:
            if f.id not in point.contested_by:point.contested_by.append(f.id)
            self.emit('POIClaimContested',p,point.id,occupant=point.claimant_id,claimant=f.id)
            return False,'Há ocupante; contestação registrada sem transferência automática.'
        if point.danger>self.e.conflicts.power(p)+p.personality.courage*.3:return False,'O grupo não consegue assegurar o local.'
        previous=f.headquarters_id;point.claimant_id=f.id;f.headquarters_id=point.id
        self.e.geography.know_place(p,point.id,'occupation',state='CLAIMED')
        event=self.emit('POIClaimed',p,point.id,place_id=point.id,faction_id=f.id,legal_ownership=False)
        point.history.append(event.id)
        self.emit('FactionHQChanged',p,f.id,faction_id=f.id,previous=previous,headquarters=point.id)
        return True,'Base ocupada; reivindicação não equivale a propriedade legal.'

    def audience(self,p,god,prayer):
        row=next((m for m in reversed(god.messages) if m['actor']==p.id and m['source_fact']==prayer.id),None)
        favor=self.e.divine_relations.affinity(god,p.id)
        gates=[]
        if not row:gates.append('NO_DIVINE_KNOWLEDGE')
        if not god.alive or not self.e.divine_relations.present(god,p.position.map_id):gates.append('INSUFFICIENT_ACCESS')
        if god.energy<45:gates.append('DIVINE_ENERGY')
        if god.values['honor']<50 or p.devotion<80 or favor<30:gates.append('INSUFFICIENT_ACCESS')
        if self.w.turn-god.essence.get('last_audience',-1000)<72:gates.append('DIVINE_COOLDOWN')
        if hasattr(self.e,'audit'):
            self.e.audit.count('audience:candidate')
            self.e.audit.sample('religion_gates',{'actor':p.id,'god':god.id,'turn':self.w.turn,
                'gates':gates,'has_message':bool(row),'energy':god.energy,'affinity':favor,
                'devotion':p.devotion,'honor':god.values['honor'],'regional_presence':self.e.divine_relations.present(god,p.position.map_id)})
        for code in gates:self.e.observability.gate('divine_audience',code,god.id)
        if gates:return False
        god.energy-=10;god.essence['last_audience']=self.w.turn
        event=self.e.recorder.emit('DivineAudience',f'{god.name} reconheceu a busca de {p.name}.',god.id,p.id,p.position,historical=True,
            context={'channel':'direct_sign','source_fact':prayer.id,'energy_cost':10,'physical_access':False})
        if favor>=60 and god.energy>=55 and row.get('context',{}).get('grave_request'):
            self.manifest(god,p.position,prayer.id)
        if favor>=40 and god.affinities.get(p.id,{}).get('deeds',0)>=2 and not any(c.mortal==p.id and c.god==god.id and c.status in ('offered','active') for c in self.w.divine_contracts.values()):
            c=DivineContract(self.w.allocate_id(),god.id,p.id,'protection','protect_person',{'report_channel':'prayer_or_bond','direct_knowledge':False,'deadline':self.w.turn+240,'source_fact':prayer.id},'offered',self.w.turn,event.id)
            self.w.divine_contracts[c.id]=c
            self.emit('DivineContractOffered',p,god.id,contract_id=c.id,god_obligation=c.god_obligation,mortal_obligation=c.mortal_obligation)
        return True

    def manifest(self,god,location,source):
        if not god.alive or not self.e.divine_relations.present(god,location.map_id) or god.energy<35:return False
        god.energy-=25;god.essence['manifested_until']=self.w.turn+12;god.essence['physical_location']=asdict(location)
        self.w.sacred_sites[location.map_id]={'god':god.id,'position':asdict(location),'source':'manifestation','source_fact':source}
        point=self.w.points.get(location.map_id)
        if point and god.id not in point.sacred_to:point.sacred_to.append(god.id)
        self.e.recorder.emit('DivineManifestation',f'{god.name} manifestou-se fisicamente.',god.id,location=location,historical=True,context={'source_fact':source,'energy_cost':25,'until':self.w.turn+12,'place_id':location.map_id})
        return True

    def physical_access(self,p,god):
        return god.alive and god.essence.get('manifested_until',-1)>self.w.turn and god.essence.get('physical_location')==asdict(p.position)

    def contract_message(self,event):
        row=event.context
        for c in self.w.divine_contracts.values():
            if c.god!=event.actor_id:continue
            god=self.w.divinities[c.god]
            if c.status=='active' and row.get('actor')==c.mortal and row.get('kind') in ('ProtectionGiven','FirstAidGiven') and row.get('turn',-1)>=c.created_at and row.get('confidence',0)>=60:
                c.status=c.known_by_god='fulfilled';c.fulfilled_at=self.w.turn
                p=self.w.characters[c.mortal]
                c.conditions['god_fulfilled']=bool(p.alive and god.energy>=8)
                if c.conditions['god_fulfilled']:
                    god.energy-=8;p.social_state['divine_protection_until']=self.w.turn+24
                self.emit('DivineContractFulfilled',p,god.id,contract_id=c.id,source_fact=row['source_fact'],god_obligation=c.god_obligation)
            elif c.status=='active' and row.get('actor')==c.mortal and row.get('kind')=='CharacterKilled' and row.get('subject') in god.known_followers and row.get('confidence',0)>=60:
                c.status=c.known_by_god='betrayed'
                self.emit('DivineContractBroken',self.w.characters[c.mortal],god.id,contract_id=c.id,status='betrayed',source_fact=row['source_fact'])
            elif c.status in ('abandoned','betrayed','failed') and row.get('kind')=='DivineContractBroken' and row.get('context',{}).get('contract_id')==c.id:
                c.known_by_god=c.status

    def execute(self,p,goal,n):
        a,target=goal.action,goal.target_id;point=self.w.points.get(target)
        if a=='take_site_supplies':
            if not point or p.position.map_id!=point.id or point.claimant_id and point.claimant_id not in p.organization_ids:return False,'Suprimento local não acessível.'
            moved=0
            for kind in ('food','water'):
                id=self.e.items.first(point.id,kind)
                if id and self.e.items.count(p.id,kind)<6:self.e.items.transfer(point.id,p.id,id,min(2,point.inventory[id]));moved+=1
            return bool(moved),'Suprimentos existentes transferidos.'
        if a=='invite_person':return self.invite(p,self.w.factions.get(target))
        if a in ('request_membership','answer_invitation'):return self.membership(p,self.w.factions[target],a=='request_membership')
        if a=='store_supplies':
            f=self.w.factions.get(target)
            if not f or p.id not in f.member_ids:return False,'Organização indisponível.'
            moved=0
            if p.money>18:p.money-=1;f.money+=1;moved+=1
            if p.position.map_id==f.headquarters_id and self.e.items.count(p.id,'food')>3:self.e.items.transfer(p.id,f.id,self.e.items.first(p.id,'food'));moved+=1
            p.access_state['last_storage']=self.w.turn
            if moved:self.emit('FactionContribution',p,f.id,transfers=moved)
            return bool(moved),'Contribuição de recursos existentes.'
        if a=='form_expedition':return self.expedition(p,point)
        if a=='follow_expedition':
            guide=self.w.characters.get(target)
            return self.e.geography.begin(p,n.target_id,'expedition',mode='follow_person',guide=guide)
        if a=='explore_poi':return self.explore(p,point)
        if a=='claim_location':return self.claim(p,point,self.w.factions.get(organization_id(n.context,'faction')) if n else None)
        if a=='formalize_organization':
            g=self.w.groups.get(target);present=[self.w.characters[i] for i in self.e.spatial.at(p.position)]
            f=self.e.institutions.formalization(p,g,present,True) if g else None
            if f:self.emit('GroupFormalized',p,f.id,group_id=g.id,members=list(f.member_ids));self.know_faction(p,f,'founder')
            return bool(f),'Formalização custeada por membros presentes.'
        if a=='seek_divine_contact':
            god=self.w.divinities.get(target);site=p.known_sacred_sites.get(target)
            if not god or not site or p.position!=Location(**site['position']):return False,'Local de contato conhecido não alcançado.'
            p.known_places['sacred']=p.position
            self.e.faith.execute(p,type(goal)(goal.id,goal.need_id,'pray',goal.score,goal.created_at,target,p.position),n)
            prayer=next((event for event in reversed(self.w.events) if event.kind=='PrayerOffered' and event.actor_id==p.id and event.turn==self.w.turn),None)
            if not prayer:return False,'O rito não pôde ser realizado.'
            self.emit('DivineAccessAchieved',p,target,place_id=p.position.map_id,source_fact=prayer.id)
            self.audience(p,god,prayer)
            p.access_state['contact_after']=self.w.turn+72;p.access_state['contact_intent']=False
            self.e.needs.satisfy(p,'divine_contact')
            return True,'Acesso e rito realizados; resposta continua sendo decisão divina.'
        if a in ('accept_contract','refuse_contract','abandon_contract'):
            c=self.w.divine_contracts.get(target)
            if not c or c.mortal!=p.id or c.status not in ('offered','active'):return False,'Contrato recebido indisponível.'
            if a=='accept_contract' and p.personality.independence<85:
                c.status=c.known_by_god='active';kind='DivineContract'
            elif a=='abandon_contract':c.status='abandoned';kind='DivineContractBroken'
            else:c.status=c.known_by_god='refused';kind='DivineContractRefused'
            self.emit(kind,p,c.god,contract_id=c.id,status=c.status)
            self.e.needs.satisfy(p,'divine_contract')
            return True,'Resposta pessoal registrada; descumprimento não é conhecimento global do deus.'
        return False,'Ação espacial indisponível.'
