"""Fama deriva de fatos aprendidos. História objetiva de item não é crença."""
from .models import Reputation, FactImpact
DEEDS={'FirstAidGiven':('generosity',12),'ProtectionGiven':('protection',8),
       'IncapacitatedSpared':('mercy',15),'CharacterKilled':('violence',18),
       'MayorAppointed':('leadership',15),'FactionFounded':('leadership',25),
       'PolicyDecided':('leadership',10),'DivinityKilled':('divine_association',80),
       'Apotheosis':('divine_association',80),'OrganizationalAction':('competence',8),
       'DivineIntervention':('divine_association',20),'ItemCreated':('craftsmanship',3)}
TITLES={'generosity':'Mão Generosa','protection':'Protetor','mercy':'Misericordioso',
        'violence':'Açougueiro','leadership':'Voz da Cidade','divine_association':'Tocado pelos Deuses',
        'competence':'Veterano','craftsmanship':'Artífice'}

class RenownSystem:
    def __init__(self,e):
        self.e,self.w=e,e.world;e.bus.subscribe('CharacterKilled',self.item_event);e.bus.subscribe('DivinityKilled',self.item_event)
    def count(self,key,n=1):
        key='Renown:'+key;self.w.metrics[key]=self.w.metrics.get(key,0)+n
    def learn(self,p,f):
        if f.kind=='ItemLegendReported':
            id=f.context.get('item_id')
            if id in self.w.items:
                p.item_beliefs[id]={'confidence':f.confidence,'source_fact':f.event_id,
                    'property':f.context.get('alleged_property'),'source_id':f.source_id,'learned_at':self.w.turn}
                while len(p.item_beliefs)>8:p.item_beliefs.pop(next(iter(p.item_beliefs)))
            return
        if f.kind not in DEEDS or f.actor_id is None or f.actor_id==p.id:return
        domain,weight=DEEDS[f.kind]
        if f.kind=='ItemCreated':
            actor=p.observations.get(f.actor_id)
            if actor and actor.profession=='cozinheiro':domain='cooking'
            elif actor and actor.profession=='caçador':domain='hunting'
        # Um mesmo fato, mesmo reaprendido, não fabrica fama repetida.
        ledger=p.applied_facts.setdefault(f.event_id,FactImpact(f.actor_id,0))
        old=ledger.renown_confidence
        effective=min(100,f.confidence)
        if effective<=old:return
        record=p.renown.setdefault(f.actor_id,{'domains':{},'facts':{},'regions':{},'epithet':'','updated_at':self.w.turn})
        delta=weight*(effective-old)/100;record['facts'][f.event_id]=effective;ledger.renown_confidence=effective
        while len(record['facts'])>16:record['facts'].pop(next(iter(record['facts'])))
        record['domains'][domain]=min(200,record['domains'].get(domain,0)+delta)
        while len(record['domains'])>5:record['domains'].pop(next(iter(record['domains'])))
        region=str(p.position.map_id);record['regions'][region]=record['regions'].get(region,0)+delta
        while len(record['regions'])>4:record['regions'].pop(next(iter(record['regions'])))
        strongest=max(record['domains'],key=record['domains'].get)
        score=record['domains'][strongest]
        if score>=30 and len(record['facts'])>=2:
            previous_epithet=record['epithet']
            record['epithet']=TITLES.get(strongest,'Especialista')+' de '+self.w.maps[p.position.map_id].name
            actor=self.w.characters.get(f.actor_id)
            if actor:actor.social_state.setdefault('regional_epithets',{})[region]=record['epithet']
            if actor:
                while len(actor.social_state['regional_epithets'])>6:actor.social_state['regional_epithets'].pop(next(iter(actor.social_state['regional_epithets'])))
            if record['epithet']!=previous_epithet:self.count('epithet')
        record['updated_at']=self.w.turn
        while len(p.renown)>12:p.renown.pop(next(iter(p.renown)))
        self.count('fact_learned')
        # Divinização social exige histórias confiáveis e vínculo, não só fama numérica.
        if f.actor_id in self.w.characters and p.devotion>=85 and score>=80 and len(record['facts'])>=3 and f.confidence>=60:
            trust=self.e.graph.value(p.id,f.actor_id,'confiança',10)
            if trust>=60 and strongest in ('protection','divine_association','leadership'):
                if not p.beliefs.get(f.actor_id,{}).get('believed_divine'):
                    self.e.faith.remember_belief(p,f.actor_id,{'believed_divine':True,'known_divinity':False,
                        'confidence':60,'source_fact':f.event_id,'interpretation':'social_veneration',
                        'learned_at':self.w.turn,'town_id':p.town_id})
                    self.count('mortal_venerated')
    def item_event(self,event):
        id=event.context.get('weapon_id')
        item=self.w.items.get(id)
        if item is None:return
        target=self.w.characters.get(event.target_id)
        important=event.kind=='DivinityKilled' or target and (target.category!='comum' or any(t.mayor_id==target.id or t.general_id==target.id for t in self.w.towns.values()))
        if not important:return
        if event.id not in item.important_events:item.important_events.append(event.id);del item.important_events[:-8]
        if event.kind=='DivinityKilled':item.divine_contact=event.target_id
        # Importância histórica não aumenta automaticamente poder nem qualidade.
        item.historical_title='Testemunha de '+str(target.name if target else 'queda divina')
        self.count('historical_item')
    def reach(self,subject):
        records=[(p,r) for p in self.w.characters.values() if (r:=p.renown.get(subject))]
        towns={p.town_id for p,r in records};kingdoms={self.w.towns[i].kingdom_id for i in towns}
        credible=sum(any(v>=60 for v in r['facts'].values()) for p,r in records)
        repeated=sum(len(r['facts'])>=2 for p,r in records)
        scope='personal'
        if len(records)>=3 and credible>=2:scope='local'
        if len(towns)>=2 and repeated>=2:scope='regional'
        if len(kingdoms)>=2 and credible>=5:scope='interregional'
        return {'scope':scope,'observers':len(records),'towns':sorted(towns),'credible_observers':credible,'repeated_observers':repeated}
