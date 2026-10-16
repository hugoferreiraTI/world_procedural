"""Afinidade dirigida e canais divinos explícitos; presença não é conhecimento."""
from .models import Location, Fact
from .navigation import distance

DEEDS={'CharacterKilled','CharacterAttacked','FirstAidGiven','ProtectionGiven','HelpGiven',
       'IncapacitatedSpared','SpiritualReport','CultDefenseDeclared','FaithReinterpreted','CharacterDied'}
ACTOR_EVENTS={'WantedIssued','ThreatReported','CharacterCaptured','RestitutionGiven','ConflictForgiven',
              'InformationShared','InvestigationReply','SearchClueShared','SuspectExonerated'}

class DivineRelations:
    def __init__(self,e):
        self.e,self.w=e,e.world
        for kind in DEEDS|ACTOR_EVENTS|{'PrayerOffered'}:e.bus.subscribe(kind,self.on_activity)
        for kind in DEEDS|{'PrayerOffered'}:e.bus.subscribe(kind,self.on_event)
    def actor_alignment(self,god,event,actor):
        """Significado do ato, separado do favor e da observação divina."""
        c=event.context;source=c.get('source_fact') or c.get('fact_id') or c.get('source_testimony')
        fact=actor.knowledge.get(source)
        reliable=bool(fact and fact.confidence>=60)
        wrongdoing=reliable and fact.kind in ('ItemStolen','CharacterAttacked','CharacterKilled','CharacterThreatened') and not (fact.context.get('lawful') or fact.context.get('self_defense'))
        if god.domain in ('justice','judgment'):
            justified=event.kind in ('WantedIssued','ThreatReported','CharacterCaptured') and wrongdoing
            justified|=event.kind=='InformationShared' and wrongdoing and self.w.characters.get(event.target_id) is not None and self.w.characters[event.target_id].profession=='guarda'
            justified|=event.kind=='ProtectionGiven' and c.get('physical',False) and wrongdoing and fact.target_id==event.target_id
            justified|=event.kind=='RestitutionGiven' and reliable and fact.kind=='ItemStolen' and c.get('quantity',0)>0
            justified|=event.kind=='CharacterKilled' and bool(c.get('lawful'))
            return (6+god.values.get('honor',0)*.04) if justified else 0
        if god.domain=='protection':
            protective=(event.kind=='HelpGiven' and c.get('urgency',0)>=70 or
                        event.kind=='ProtectionGiven' and (c.get('physical',False) or reliable and wrongdoing) or
                        event.kind=='FirstAidGiven' and c.get('food_used',0)>0 and c.get('water_used',0)>0)
            return (6+god.values.get('compassion',0)*.05) if protective else 0
        if god.domain=='knowledge':
            receiver=self.w.characters.get(event.target_id)
            received=receiver.knowledge.get(source) if receiver else None
            informative=(event.kind=='InformationShared' and reliable and received and received.confidence>=60 and c.get('utility') in ('new_useful','better_confidence') or
                         event.kind=='SearchClueShared' and c.get('confidence',0)>=60 and c.get('clue_source_kind')!='rumor' and self.w.turn-c.get('observed_at',-1000)<=48 or
                         event.kind=='InvestigationReply' and c.get('result')=='author_identified' and reliable and c.get('confidence',0)>=60)
            return (6+god.values.get('patience',0)*.04) if informative else 0
        return self.alignment(god,event) if event.kind=='CharacterKilled' else 0
    def on_activity(self,event):
        actor=self.w.characters.get(event.actor_id)
        if not actor:return
        for god in self.w.divinities.values():
            if not god.alive:continue
            aligned=self.actor_alignment(god,event,actor)>=4
            cult=event.kind in ('PrayerOffered','SpiritualReport','CultDefenseDeclared') and event.target_id==god.id
            if not (aligned or cult):continue
            activity=actor.social_state.setdefault('religious_activity',{})
            r=activity.setdefault(god.id,{'acts':0,'last_actor':-1000,'last_cult':-1000})
            if aligned:r['acts']+=1;r['last_actor']=self.w.turn
            if cult:r['last_cult']=self.w.turn
    def present(self,god,region):return region in (god.presence_regions or [god.location.map_id])
    def affinity(self,god,subject):return god.affinities.get(subject,{}).get('value',0)
    def alignment(self,god,event):
        intentional=event.context.get('violence_intent')=='kill';lawful=event.context.get('lawful') or event.context.get('self_defense')
        if event.kind=='PrayerOffered':return .4+min(1,event.context.get('offering',0)*.6)
        if event.kind=='FaithReinterpreted':
            from .faith import GODS
            current=event.context.get('current','')
            return -12 if event.target_id==god.id and not (current=='Culto de '+god.name or GODS.get(current,('',None))[0]==god.name) else 0
        if event.kind in ('SpiritualReport','CultDefenseDeclared') and event.target_id==god.id:return 4
        if god.domain=='death':
            return 18 if event.kind=='CharacterKilled' and intentional and god.values.get('rewards_intentional_killing',False) else 0
        if event.kind=='CharacterKilled':
            if lawful:return 7 if god.domain in ('justice','judgment','protection') else 0
            return -18 if god.domain in ('justice','judgment','protection') else -6 if god.values.get('compassion',0)>=65 else 0
        if event.kind=='CharacterAttacked':return -4 if not lawful and god.values.get('compassion',0)>=50 else 0
        if event.kind in ('ProtectionGiven','FirstAidGiven','HelpGiven','IncapacitatedSpared'):
            meaningful=event.kind!='HelpGiven' or event.context.get('urgency',0)>=25
            if not meaningful:return 0
            return 12 if god.domain=='protection' else 8 if god.domain in ('justice','judgment') else 4 if god.values.get('compassion',0)>=50 else 0
        return 0
    def adjust(self,god,subject,amount,source,confidence=100):
        if subject not in self.w.characters or not amount:return
        if subject not in god.affinities and len(god.affinities)>=64:
            # Protege vínculos/extremos; não cria afinidade ilimitada.
            removable=[i for i in god.affinities if i not in god.bonds]
            if not removable:return
            weakest=min(removable,key=lambda i:(abs(god.affinities[i]['value']),god.affinities[i]['updated_at'],i))
            del god.affinities[weakest]
        r=god.affinities.setdefault(subject,{'value':0,'deeds':0,'facts':{},'updated_at':self.w.turn})
        previous_confidence=r['facts'].get(source,0)
        if confidence<=previous_confidence:return
        delta=amount*(confidence-previous_confidence)/100;old=r['value']
        if amount<=1 and old>=12:return  # Oração isolada tem contribuição limitada.
        r['value']=round(max(-100,min(100,old+delta)),2);r['updated_at']=self.w.turn
        r['facts'][source]=confidence
        while len(r['facts'])>12:r['facts'].pop(next(iter(r['facts'])))
        if amount>=7 and previous_confidence==0:r['deeds']+=1
        if abs(r['value']-old)>=3 or int(old//10)!=int(r['value']//10):
            self.e.recorder.emit('DivineAffinityChanged',f'{god.name} mudou sua afinidade por um mortal.',god.id,
                witnesses=[],historical=True,context={'mortal':subject,'before':old,'value':r['value'],'source_fact':source,'confidence':confidence})
        if r['value']>=85 and r['deeds']>=3 and subject not in god.bonds and len(god.bonds)<8:
            god.bonds.append(subject)
            self.e.recorder.emit('DivineBondCreated',f'{god.name} estabeleceu um vínculo raro.',god.id,
                witnesses=[],historical=True,context={'mortal':subject,'affinity':r['value'],'source_fact':source})
        if r['value']<60 and subject in god.bonds:god.bonds.remove(subject)
        p=self.w.characters[subject]
        if r['value']>=75 and r['deeds']>=3 and p.health>=60 and (p.mythic_development>=40 or self.e.conflicts.weapon(p)):
            candidates=god.essence.setdefault('champion_candidates',[])
            if subject not in candidates and len(candidates)<4:
                candidates.append(subject)
                self.e.recorder.emit('ChampionCandidate',f'{god.name} considerou um mortal como campeão.',god.id,
                    witnesses=[],historical=True,context={'mortal':subject,'source_fact':source,'recognized':False})
    def receive(self,god,source,channel,confidence=60,subject=None,context=None):
        if not god.alive or channel not in ('prayer','local_observation','cult_report','divine_bond','devoted_report'):return None
        location=source.location
        row={'source_fact':source.id if hasattr(source,'id') else source.event_id,'kind':source.kind,'actor':(context or {}).get('killer') if channel=='divine_bond' and (context or {}).get('shock') else source.actor_id,'subject':subject if subject is not None else source.target_id,
             'region':location.map_id if location else None,'location':vars(location) if location else None,
             'confidence':confidence,'channel':channel,'turn':source.turn,'received_at':self.w.turn,'context':context or {}}
        if any(m['source_fact']==row['source_fact'] and m['channel']==channel and m['confidence']>=confidence for m in god.messages):return None
        god.messages.append(row);del god.messages[:-16]
        self.e.recorder.emit('DivineMessage',f'{god.name} recebeu informação por {channel}.',god.id,
            witnesses=[],historical=True,context=row)
        if channel=='cult_report' and confidence>=60 and row['context'].get('rival_growth',0)>0:
            self.e.recorder.emit('RivalFaithGrowthKnown',f'{god.name} recebeu notícia de mudanças para outra fé.',god.id,
                witnesses=[],historical=True,context={'source_fact':row['source_fact'],'region':row['region'],
                    'known_conversions':row['context']['rival_growth'],'confidence':confidence,'channel':channel})
        return row
    def on_event(self,event):
        actor=self.w.characters.get(event.actor_id)
        for god in self.w.divinities.values():
            if not god.alive:continue
            amount=self.alignment(god,event)
            local=event.location==god.location
            ritual=event.kind=='PrayerOffered' and event.target_id==god.id
            bonded=event.actor_id in god.bonds and abs(amount)>=7
            if local or ritual or bonded:
                channel='prayer' if ritual else 'local_observation' if local else 'divine_bond'
                self.receive(god,event,channel,100 if local else 60 if ritual else 80)
                if event.actor_id and amount:self.adjust(god,event.actor_id,amount,event.id,100 if local else 60 if ritual else 80)
                if ritual and actor:
                    # Uma oração pode transportar feitos próprios/conhecidos;
                    # é relato com confiança limitada, não censo ou visão remota.
                    for source_id in event.context.get('deed_sources',[])[:3]:
                        fact=actor.knowledge.get(source_id)
                        if not fact or fact.kind not in DEEDS or fact.confidence<60 or self.w.turn-fact.turn>168:continue
                        self.receive(god,fact,'devoted_report',60,context={'reported_by':actor.id})
                        alignment=self.alignment(god,fact)
                        if fact.actor_id and alignment:self.adjust(god,fact.actor_id,alignment,fact.event_id,60)
            if ritual and actor:
                for fact_id in event.context.get('contract_sources',[])[:3]:
                    fact=actor.knowledge.get(fact_id)
                    if fact and fact.kind=='DivineContractBroken' and fact.confidence>=60:
                        self.receive(god,fact,'devoted_report',60,context={'contract_id':fact.context.get('contract_id'),'reported_by':actor.id})
            victim=self.w.characters.get(event.target_id)
            if victim and event.target_id in god.bonds and event.kind in ('CharacterKilled','CharacterDied','CharacterAttacked'):
                if event.kind=='CharacterAttacked' and victim.health>20:continue
                killer_known=bool(event.actor_id and any(f.kind=='CharacterAttacked' and f.actor_id==event.actor_id and f.target_id==victim.id and f.confidence>=60 and self.w.turn-f.turn<=12 for f in victim.knowledge.values()))
                payload={'follower':victim.id,'affinity':self.affinity(god,victim.id),
                         'killer':event.actor_id if killer_known else None,'cause':event.context.get('cause'),
                         'shock':'favored_death' if not victim.alive else 'favored_near_death'}
                row=self.receive(god,event,'divine_bond',80,subject=victim.id,context=payload)
                if row:
                    # Retira autoria oculta também do envelope da mensagem.
                    row['actor']=event.actor_id if killer_known else None
                    if not victim.alive:
                        self.e.recorder.emit('FavoredFollowerKilled',f'{god.name} soube da perda de um favorito.',god.id,
                            witnesses=[],historical=True,context=row)
    def manifest(self,god,message):
        region=message.get('region');location=message.get('location')
        if not region or not location or region not in self.w.maps or message.get('confidence',0)<60:return False
        if self.present(god,region):return True
        if god.energy<50 or self.w.turn-god.essence.get('last_manifestation',-1000)<72:return False
        a=self.w.towns.get(god.location.map_id);b=self.w.towns.get(region)
        travel=distance(a.position,b.position) if a and b else 20
        cost=min(45,25+travel*.5)
        god.energy-=cost;god.location=Location(**location);god.presence_regions=[region]
        god.essence['last_manifestation']=self.w.turn
        self.e.recorder.emit('DivinePresenceChanged',f'{god.name} deslocou sua presença sobrenatural.',god.id,
            witnesses=[],historical=True,context={'region':region,'source_fact':message['source_fact'],'channel':message['channel'],'energy_cost':cost})
        return True
    def assessment(self,god):
        messages=[m for m in god.messages if self.w.turn-m['received_at']<=200 and m['confidence']>=60]
        severe=[]
        for m in messages:
            c=m['context'];state=c.get('state')
            if c.get('shock') in ('favored_death','favored_near_death'):
                severe.append((95 if c['shock']=='favored_death' else 75,m))
            elif state in ('CORE_EROSION','REGIONAL_CRISIS','CULT_COLLAPSE','EXISTENTIAL_RELIGIOUS_THREAT'):
                important=c.get('importance',0)>=60
                severity=90 if state in ('CULT_COLLAPSE','EXISTENTIAL_RELIGIOUS_THREAT') else 80 if important else 65
                severe.append((severity,m))
        if not severe:return None
        severity,m=max(severe,key=lambda x:(x[0],x[1]['received_at']))
        ap=self.e.action_pressure.disposition(severity,100-god.values.get('patience',50)*.4,70,god.action_pressure.failures,0,(100-god.energy)/160)
        return {'world_pressure':severity,'action_pressure':ap,'eligibility_causes':[m['context'].get('shock') or 'received_'+m['context'].get('state','religious_crisis')],
                'source_facts':[m['source_fact']],'capacity':god.energy,'perceived_capacity':god.energy,
                'major_barriers':[],'eligible':god.energy>=20 and self.w.turn-god.last_intervention>=168,
                'known_losses':m['context'].get('losses',1),'message':m}
