"""Padrões pertencem ao conhecimento do observador; autoria pode continuar oculta."""
from .models import Location

class ViolencePatterns:
    def __init__(self,e):self.e,self.w=e,e.world
    def on_fact(self,p,f):
        if f.kind=='SerialViolencePattern' and f.confidence>=30:
            if f.context.get('region')!=p.town_id:return
            p.social_state['fear_of_killer']=max(p.social_state.get('fear_of_killer',0),min(80,f.confidence*.6))
            p.social_state['fear_of_killer_updated']=self.w.turn
            if p.profession=='guarda' and f.confidence>=60 and len(f.context.get('source_facts',[]))>=2:
                n=self.e.needs.ensure(p,'security:repeated_homicide',85,'event:'+str(f.event_id),
                    'Vigiar região com padrão de homicídios reportado',None)
                n.context.update(source_event=f.event_id,known_location=vars(f.location),severity=5,
                    violence_pattern='received_pattern',unknown_author=True)
                n.expires_at=self.w.turn+200
            return
        if f.kind!='CharacterKilled' or f.confidence<60 or not f.location:return
        if f.context.get('lawful') or f.context.get('self_defense') and f.context.get('death_context')!='deliberate_finish':return
        patterns=p.social_state.setdefault('violence_patterns',{})
        # Arma/forma de morte são assinaturas alegadas recebidas, não busca global.
        signature=str(f.location.map_id)+':'+str(f.context.get('weapon_id') or f.context.get('death_context','violent_death'))
        r=patterns.setdefault(signature,{'region':f.location.map_id,'deaths':{},'announced':0,'suspect':None})
        if f.target_id in r['deaths']:
            old=r['deaths'][f.target_id]
            if old['confidence']>=f.confidence:return
        r['deaths'][f.target_id]={'fact':f.event_id,'turn':f.turn,'actor':f.actor_id,'confidence':f.confidence}
        r['deaths']={i:d for i,d in r['deaths'].items() if self.w.turn-d['turn']<=200}
        while len(r['deaths'])>8:r['deaths'].pop(next(iter(r['deaths'])))
        while len(patterns)>4:patterns.pop(next(iter(patterns)))
        deaths=list(r['deaths'].values());authors={d['actor'] for d in deaths if d['actor'] is not None}
        r['suspect']=next(iter(authors)) if len(authors)==1 and all(d['actor'] is not None for d in deaths) else None
        if len(deaths)<2:return
        p.social_state['fear_of_killer']=max(p.social_state.get('fear_of_killer',0),35)
        p.social_state['fear_of_killer_updated']=self.w.turn
        r['epithet']='A Sombra de '+self.w.maps[f.location.map_id].name
        if p.profession=='guarda' and f.location.map_id==p.town_id:
            source=deaths[-1]['fact']
            n=self.e.needs.ensure(p,'security:repeated_homicide',85,'event:'+str(source),
                'Investigar padrão local de homicídios conhecidos',r['suspect'])
            n.context.update(source_event=source,known_location=vars(f.location),severity=5,
                violence_pattern=signature,unknown_author=r['suspect'] is None)
            n.expires_at=self.w.turn+200;p.active_until=max(p.active_until,self.w.turn+6)
            # Casos só recebem gravidade se este guarda conhece o suspeito.
            if r['suspect']:
                record=self.e.justice.record_for(p,r['suspect'])
                if record:record.known_severity[p.id]=5
        if len(deaths)>r['announced']:
            r['announced']=len(deaths)
            self.e.recorder.emit('SerialViolencePattern',f'{p.name} associou mortes recorrentes na região.',p.id,
                location=p.position,witnesses=[p.id],historical=True,
                context={'region':r['region'],'suspect':r['suspect'],'source_facts':[d['fact'] for d in deaths][-3:],
                         'confidence':min(d['confidence'] for d in deaths),'epithet':r['epithet'],'hypothesis':True})
