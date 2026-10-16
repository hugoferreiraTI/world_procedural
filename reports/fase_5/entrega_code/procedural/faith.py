"""Verdade divina, crença subjetiva e ações religiosas são estados distintos."""
from .models import Divinity, Location, Goal, Aspiration, Fact
from .needs import FINISHED
FAITH_ACTIONS={'pray','offer_resource','spread_faith','reinterpret','challenge_divinity','claim_essence','train_power','defend_cult','tell_item_history'}
GODS={'Culto do Sol':('Aurion','justice'),'Ordem da Maré':('Neruma','protection'),
      'Culto da Aurora':('Elar','knowledge')}

class FaithSystem:
    def __init__(self,e):
        self.e,self.w=e,e.world
        e.bus.subscribe('PrayerOffered',self.hear_prayer)
        e.bus.subscribe('CharacterAttacked',self.hear_local_deed)
        e.bus.subscribe('CharacterKilled',self.hear_local_deed)
    def count(self,key,n=1):
        key='Faith:'+key;self.w.metrics[key]=self.w.metrics.get(key,0)+n
    def bootstrap(self):
        if self.w.divinities:return
        for religion,(name,domain) in GODS.items():
            t=next((t for t in self.w.towns.values() if t.kingdom_id and self.w.kingdoms[t.kingdom_id].religion==religion),next(iter(self.w.towns.values())))
            god=Divinity(self.w.allocate_id(),name,domain,{'compassion':self.e.rng.randint(25,90),
                'honor':self.e.rng.randint(25,90),'anger':self.e.rng.randint(10,80),'patience':self.e.rng.randint(40,95)},
                60,'cosmologia inicial',Location(t.id,self.w.maps[t.id].width//2,1),
                influence=[x.id for x in self.w.towns.values() if x.kingdom_id and self.w.kingdoms[x.kingdom_id].religion==religion])
            self.w.divinities[god.id]=god
        gods=list(self.w.divinities.values())
        for a in gods:
            for b in gods:
                if a.id!=b.id:a.relations[b.id]=self.e.rng.randint(-30,40);self.e.graph.set(a.id,b.id,'afinidade_divina',a.relations[b.id])
        for p in self.w.characters.values():
            god=next((g for g in gods if GODS.get(p.religion,('',None))[0]==g.name),None)
            if god:p.beliefs[god.id]={'confidence':50,'devotion':p.devotion,'interpretation':'cultural_tradition',
                'source_fact':None,'known_divinity':False,'believed_divine':True,'learned_at':0,'town_id':p.town_id}
            grid=self.w.maps.get(p.home.map_id)
            if grid:p.known_places['sacred']=Location(grid.id,grid.width//2,1)
            if not p.is_player and self.e.rng.random()<.0025:
                p.mythic_trait=self.e.rng.choice(('Heroism','Justice','Coldness'))
                p.social_state['mythic_origin']='generation_potential'
                if p.personality.ambition>=60 or p.personality.courage>=65:
                    p.aspirations.append(Aspiration('become_stronger',70,self.w.turn,
                        context={'reason':'exceptional_potential_and_personal_values','target':75}))
                self.count('mythic_generated')
    def remember_belief(self,p,subject,data):
        if subject is None:return
        p.beliefs[subject]=data
        while len(p.beliefs)>6:p.beliefs.pop(next(iter(p.beliefs)))
    def on_fact(self,p,f):
        if f.kind=='DivineIntervention':
            # Receber um relato não transmite automaticamente identidade ontológica.
            subject=f.actor_id if f.actor_id in p.beliefs else next(iter(p.beliefs),None)
            interpretation='miracle' if p.devotion>=60 else 'coincidence' if p.devotion<25 else 'unexplained'
            if subject:
                old=p.beliefs.get(subject,{})
                self.remember_belief(p,subject,{**old,'interpretation':interpretation,'source_fact':f.event_id,
                    'confidence':min(f.confidence,60 if interpretation=='miracle' else 40),'learned_at':self.w.turn,
                    'believed_divine':interpretation=='miracle','known_divinity':False,'town_id':p.town_id})
            self.count('interpretation:'+interpretation)
        if f.kind=='SpiritualReport':
            subject=f.context.get('believed_subject')
            old=p.beliefs.get(subject)
            if old and old.get('confidence',0)>=f.confidence:return
            self.remember_belief(p,subject,{'confidence':min(60,f.confidence),'devotion':p.devotion,
                'interpretation':f.context.get('interpretation','reported'),'source_fact':f.event_id,
                'learned_at':self.w.turn,'known_divinity':False,'believed_divine':True,'town_id':p.town_id,
                'source_id':f.source_id or f.actor_id})
            self.count('spiritual_report_learned')
        if f.kind=='DivinityKilled':
            b=p.beliefs.get(f.target_id)
            if b:b['interpretation']='loss';b['source_fact']=f.event_id
            self.count('divine_history_learned')
        if f.kind=='Apotheosis':
            mortal=p.beliefs.get(f.actor_id)
            previous=p.beliefs.get(f.context.get('previous_divinity'))
            if mortal:
                mortal['interpretation']='claimed_ascension';mortal['source_fact']=f.event_id
            if mortal or previous:
                self.remember_belief(p,f.target_id,{'confidence':min(60,f.confidence),
                    'interpretation':'claimed_ascension','source_fact':f.event_id,
                    'known_divinity':False,'believed_divine':bool(mortal and mortal.get('believed_divine')),
                    'learned_at':self.w.turn,'town_id':p.town_id,'source_id':f.source_id or f.actor_id})
            self.count('divine_history_learned')
    def refresh(self,p):
        if not self.w.social_initialized or p.is_player:return
        stable=p.health>=80 or p.health>=50 and p.recoverable_deprivation_damage==0 and p.combat.injured>=6
        if stable and max(p.hunger,p.thirst)<80 and p.devotion>=40 and p.beliefs and self.w.turn-p.social_state.get('last_ritual',-1000)>=48:
            subject=max(p.beliefs,key=lambda i:p.beliefs[i].get('confidence',0))
            urgency=12+p.devotion*.25+(10 if p.health<50 else 0)
            n=self.e.needs.ensure(p,'religious_interest',urgency,'own_faith','Atender crença pessoal',subject)
            n.context.update(belief_subject=subject,source_event=p.beliefs[subject].get('source_fact'))
        else:self.e.needs.satisfy(p,'religious_interest')
        if p.mythic_trait and any(a.domain=='become_stronger' and a.status=='active' for a in p.aspirations):
            if p.health>=80 and max(p.hunger,p.thirst)<60 and p.mythic_development<75:
                n=self.e.needs.ensure(p,'power',35+p.personality.ambition*.25,'aspiration:become_stronger','Desenvolver capacidade pessoal')
                n.context['aspiration_domain']='become_stronger'
                n.expires_at=self.w.turn+240
            else:self.e.needs.satisfy(p,'power')
    def modifier(self,p,action):
        if not p.mythic_trait:return 0
        if p.mythic_trait=='Heroism':return 35 if action in ('protect','intervene','first_aid','challenge_divinity','train_power') else 0
        if p.mythic_trait=='Justice':
            return (32 if action in ('denounce','organize','confront','train_power') else
                    25 if action=='capture' and p.personality.honesty>=50 else
                    20 if action=='attack' and p.personality.vengefulness>=70 and p.grievances else 0)
        return 25 if action in ('review_proposal','train_power','withdraw') else 12 if action=='attack' and p.combat.opponents else 0
    def candidates(self,p,n):
        if n.kind=='power':return [('train_power',p.home,None)]
        if n.kind!='religious_interest':return []
        subject=n.target_id;choices=[];b=p.beliefs.get(subject,{})
        if self.w.turn-p.social_state.get('last_item_report',-1000)>=72 and any(i!=p.id for i in self.e.spatial.at(p.position)):
            for id in p.inventory:
                item=self.w.items[id]
                if any(i in p.knowledge for i in item.important_events):choices.append(('tell_item_history',None,id))
        t=self.w.towns.get(p.position.map_id)
        restricted=t and t.policies.get('cults',{}).get(str(subject))=='restricted'
        if not restricted and 'sacred' in p.known_places:
            choices.append(('pray',p.known_places['sacred'],subject))
            if self.e.items.count(p.id,'water')>1:choices.append(('offer_resource',p.known_places['sacred'],subject))
        if b.get('source_fact') and any(i!=p.id for i in self.e.spatial.at(p.position)):
            choices.append(('spread_faith',None,subject))
        if b.get('source_fact'):choices.append(('reinterpret',None,subject))
        if restricted:
            choices.append(('defend_cult',None,subject))
        god=self.w.divinities.get(subject)
        if god and god.location==p.position and god.alive and p.mythic_development>=60 and p.mythic_trait=='Justice':
            if any(f.kind=='DivineIntervention' and f.actor_id==subject and f.context.get('effect')=='curse' and f.confidence>=60 for f in p.knowledge.values()):
                choices.append(('challenge_divinity',None,subject))
        if god and not god.alive and god.essence.get('accessible_to')==p.id and p.position==god.location:
            choices.append(('claim_essence',None,subject))
        return choices
    def hear_prayer(self,event):
        god=self.w.divinities.get(event.target_id)
        if god is None:
            mortal=self.w.characters.get(event.target_id)
            god=self.w.divinities.get(mortal.social_state.get('actual_divinity')) if mortal else None
            if god and god.mortal_origin!=event.target_id:god=None
        if not god or not god.alive:return
        if event.actor_id not in god.known_followers:god.known_followers.append(event.actor_id);del god.known_followers[:-64]
        god.memory.append(event.id);del god.memory[:-16]
        # Comunicação divina explícita por ritual, não varredura de necessidades globais.
        god.essence.setdefault('requests',[]).append({'actor':event.actor_id,'fact':event.id,
            'turn':event.turn,'location':vars(event.location),'need':event.context.get('request'),
            'offering':event.context.get('offering',0)})
        del god.essence['requests'][:-8]
        self.count('prayer_received')
    def hear_local_deed(self,event):
        for god in self.w.divinities.values():
            if god.alive and god.location==event.location:
                seen=god.essence.setdefault('seen_deeds',[])
                seen.append({'actor':event.actor_id,'fact':event.id,'turn':event.turn,
                             'harm':not (event.context.get('lawful') or event.context.get('self_defense')),
                             'record':Fact(event.id,event.kind,event.actor_id,event.target_id,event.location,event.turn,
                                           event.description,confidence=60,source_id=god.id,source_kind='known',context=dict(event.context))})
                del seen[:-8]
    def intervene(self,god,request,effect=None):
        p=self.w.characters.get(request['actor'])
        if not god.alive or not p or not p.alive or god.energy<20 or self.w.turn-god.last_intervention<168:return False
        # Uma oração indica local naquele instante; não acompanha o fiel remotamente.
        location=Location(**request['location'])
        if p.position!=location or self.w.turn-request['turn']>24:return False
        if effect is None:
            effect='omen' if god.domain=='knowledge' and god.essence.get('seen_deeds') else 'blessing' if god.values['compassion']>=45 and request['need'] in ('healing','protection') else 'sign'
        if effect=='blessing':amount=self.e.recovery.recover_hp(p,1,treatment=8)
        elif effect=='curse':amount=self.e.recovery.damage(p,min(3,max(0,p.health-1)),'combat')
        else:amount=0
        god.energy-=20;god.last_intervention=self.w.turn
        if effect=='omen':
            # O domínio revela somente o que este deus observou fisicamente.
            self.e.knowledge.learn(p,god.essence['seen_deeds'][-1]['record'],False)
        if effect=='sign':p.social_state['divine_protection_until']=self.w.turn+12
        event=self.e.recorder.emit('DivineIntervention',f'Um acontecimento {effect} foi percebido no local.',
            god.id,p.id,location,historical=True,context={'effect':effect,'amount':amount,'source_fact':request['fact'],
                'objective_divinity':god.id,'domain':god.domain,'energy_cost':20,'judged_fact':request.get('judged_fact')})
        god.interventions.append(event.id);del god.interventions[:-16]
        weapon=self.e.conflicts.weapon(p)
        if weapon and effect=='sign':
            weapon.divine_contact=god.id;weapon.actual_properties['protection_until']=self.w.turn+12
            weapon.important_events.append(event.id);del weapon.important_events[:-8]
        self.count('intervention:'+effect);return True
    def divine_death(self,p,god,cause):
        if not p.alive or not god.alive or p.position!=god.location:return False
        god.alive=False;god.essence={'accessible_to':p.id,'claimed':False,'released_at':self.w.turn,'requests':[]}
        event=self.e.recorder.emit('DivinityKilled',f'{p.name} causou a morte de {god.name}.',p.id,god.id,god.location,
            historical=True,context={'domain':god.domain,'cause':cause,'essence_released':True,'weapon_id':self.e.conflicts.weapon(p).id if self.e.conflicts.weapon(p) else None})
        god.memory.append(event.id);del god.memory[:-16];self.count('divine_death');return True
    def apotheosis(self,p,god):
        if len(self.w.divinities)>=12 or not p.alive or god.alive or p.position!=god.location or god.essence.get('accessible_to')!=p.id or god.essence.get('claimed') or p.mythic_development<75:return False
        # Apropriação separada; o domínio depende do mortal, não do deus anterior.
        domain='judgment' if p.mythic_trait=='Justice' else 'protection' if p.mythic_trait=='Heroism' else 'resolve'
        new=Divinity(self.w.allocate_id(),p.name,domain,{'compassion':p.personality.compassion,'honor':p.personality.honesty,
            'anger':p.emotions.anger,'patience':p.personality.persistence},min(100,30+p.mythic_development*.4),
            'apoteose por essência reivindicada',p.position,mortal_origin=p.id)
        self.w.divinities[new.id]=new;god.essence['claimed']=True;god.essence['claimed_by']=new.id
        p.social_state['actual_divinity']=new.id
        self.e.recorder.emit('Apotheosis',f'{p.name} assumiu uma divindade de {domain}.',p.id,new.id,p.position,
            historical=True,context={'previous_divinity':god.id,'new_domain':domain,'old_domain':god.domain})
        self.count('apotheosis');return True
    def execute(self,p,goal,n):
        a=goal.action;subject=goal.target_id
        if a=='tell_item_history':
            item=self.w.items.get(subject)
            fact=next((p.knowledge[i] for i in item.important_events if i in p.knowledge),None) if item else None
            if not item or subject not in p.inventory or not fact or not any(i!=p.id for i in self.e.spatial.at(p.position)):
                return False,'Faltam item, história conhecida ou interlocutor.'
            self.e.recorder.emit('ItemLegendReported',f'{p.name} contou uma história sobre {item.name}.',p.id,subject,p.position,
                context={'item_id':subject,'source_fact':fact.event_id,'confidence':fact.confidence,
                         'alleged_property':p.item_beliefs.get(subject,{}).get('property','importância histórica')})
            p.social_state['last_item_report']=self.w.turn;self.count('item_report')
            return True,'História conhecida relatada; a crença não cria propriedade física.'
        if a=='train_power':
            if not p.mythic_trait or p.position!=p.home or p.health<80 or max(p.hunger,p.thirst)>=60:return False,'Treino incompatível com condição atual.'
            p.fatigue=min(100,p.fatigue+8);p.hunger=min(100,p.hunger+3);p.mythic_development=min(100,p.mythic_development+1)
            self.e.recorder.emit('PowerTrained',f'{p.name} treinou sua capacidade.',p.id,location=p.position,
                context={'development':p.mythic_development,'cost_fatigue':8,'cost_hunger':3})
            self.count('training')
            for a in p.aspirations:
                if a.domain=='become_stronger':
                    a.progress=min(1,p.mythic_development/75)
                    if a.progress>=1:a.status='satisfied'
            return True,'Potencial desenvolvido por esforço real.'
        b=p.beliefs.get(subject)
        if not b:return False,'Crença/entidade não conhecida.'
        if a in ('pray','offer_resource'):
            if p.position!=p.known_places.get('sacred'):return False,'Local sagrado conhecido não foi alcançado.'
            t=self.w.towns.get(p.position.map_id)
            if t and t.policies.get('cults',{}).get(str(subject))=='restricted':return False,'Prática institucionalmente restringida neste local.'
            offering=0
            if a=='offer_resource':
                if self.e.items.count(p.id,'water')<=1:return False,'Não há excedente de água para oferecer.'
                self.e.items.consume(p.id,'water');offering=1
            request='healing' if p.health<80 else 'protection' if p.combat.opponents else 'sign'
            self.e.recorder.emit('PrayerOffered',f'{p.name} realizou oração.',p.id,subject,p.position,
                context={'request':request,'offering':offering,'belief_source':b.get('source_fact')})
            p.social_state['last_ritual']=self.w.turn;self.e.needs.satisfy(p,'religious_interest');self.count('ritual')
            return True,'Oração executada; não garante intervenção.'
        if a=='spread_faith':
            fact=p.knowledge.get(b.get('source_fact'))
            if not fact or not any(i!=p.id for i in self.e.spatial.at(p.position)):return False,'Não há relato conhecido ou interlocutor.'
            self.e.recorder.emit('SpiritualReport',f'{p.name} transmitiu sua interpretação religiosa.',p.id,subject,p.position,
                context={'believed_subject':subject,'interpretation':b.get('interpretation','reported'),
                    'source_fact':fact.event_id,'confidence':min(fact.confidence,b.get('confidence',30))})
            p.social_state['last_ritual']=self.w.turn;self.count('spiritual_report')
            return True,'Relato espiritual transmitido sem alterar verdade objetiva.'
        if a=='reinterpret':
            if b.get('confidence',0)<30:return False,'Relato pouco confiável para mudar crença.'
            name=self.w.divinities[subject].name if subject in self.w.divinities else self.w.characters[subject].name if subject in self.w.characters else str(subject)
            old=p.religion
            if b.get('interpretation')=='loss' and p.personality.independence>=60:
                p.religion='';p.devotion=max(0,p.devotion-20);self.count('faith_abandoned')
            elif b.get('interpretation') in ('miracle','reported','claimed_ascension') and p.devotion>=60:
                p.religion='Culto de '+name;p.devotion=min(100,p.devotion+2)
                if old!=p.religion:self.count('conversion')
            self.e.recorder.emit('FaithReinterpreted',f'{p.name} reavaliou sua crença.',p.id,subject,p.position,
                context={'previous':old,'current':p.religion,'source_fact':b.get('source_fact')})
            p.social_state['last_ritual']=self.w.turn;return True,'Interpretação escolheu manter, alterar ou abandonar fé.'
        if a=='defend_cult':
            self.e.recorder.emit('CultDefenseDeclared',f'{p.name} declarou defesa de sua fé.',p.id,subject,p.position,
                context={'source_fact':b.get('source_fact')});p.social_state['last_ritual']=self.w.turn
            return True,'Defesa pública sem ataque automático.'
        god=self.w.divinities.get(subject)
        if not god:return False,'Adoração não oferece acesso a divindade real.'
        if a=='challenge_divinity':
            if p.position!=god.location or p.mythic_development<60 or not god.alive:return False,'Não há capacidade/oportunidade de confronto divino.'
            power=self.e.conflicts.power(p)*4+p.mythic_development*.4
            if power>god.power and god.energy<40:
                return self.divine_death(p,god,'confronto local e divindade enfraquecida'),'Confronto divino resolvido.'
            self.e.recovery.damage(p,min(12,p.health),'combat');p.mythic_development=min(100,p.mythic_development+1)
            self.e.recorder.emit('DivineChallengeFailed',f'{p.name} falhou no confronto divino.',p.id,god.id,p.position,
                historical=True,context={'mortal_power':power,'divine_power':god.power})
            if p.health<=0:self.e.finish_death(p,'combat')
            self.count('divine_challenge_failed');return True,'Confronto falhou com custo físico.'
        if a=='claim_essence':return self.apotheosis(p,god),'Apropriação divina avaliada separadamente.'
        return False,'Ação religiosa indisponível.'
    def tick(self):
        if self.w.turn%24:return
        for god in self.w.divinities.values():
            if not god.alive:continue
            god.energy=min(100,god.energy+.5)
            requests=god.essence.get('requests',[])
            viable=[r for r in requests if self.w.turn-r['turn']<=24]
            god.essence['requests']=viable[-8:]
            for r in viable:
                # Valores/divínio, oferta e pedido competem com contenção/custo.
                score=god.values['compassion']*.4+god.values['honor']*.2+15*r['offering']+(15 if r['need']=='healing' else 0)
                if god.domain=='protection' and r['need'] in ('healing','protection'):score+=12
                if god.domain=='knowledge' and god.essence.get('seen_deeds'):score+=8
                restraint=30+god.values['patience']*.25+(100-god.energy)*.2
                harmful=next((x for x in reversed(god.essence.get('seen_deeds',[])) if x['actor']==r['actor'] and x['harm'] and self.w.turn-x['turn']<=72),None)
                curse=god.values['anger']*.5+god.values['honor']*.2+(10 if god.domain=='justice' else 0) if harmful else -1
                effect='curse' if curse>max(restraint,score) else None
                if max(score,curse)>restraint and self.intervene(god,{**r,'judged_fact':harmful['fact'] if harmful else None},effect):break
