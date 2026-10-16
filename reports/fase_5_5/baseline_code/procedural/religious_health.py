"""Censo objetivo compacto e relatos religiosos construídos de conhecimento local."""
from .models import Fact
LAYERS=('followers','devoted','cultists','actors')
SEVERE={'CORE_EROSION','REGIONAL_CRISIS','CULT_COLLAPSE','EXISTENTIAL_RELIGIOUS_THREAT'}

class ReligiousHealth:
    def __init__(self,e):
        self.e,self.w=e,e.world
        for kind in ('CharacterKilled','CharacterDied'):e.bus.subscribe(kind,self.shock)
        e.knowledge.listeners.append(self.on_fact)
    def composition(self):
        data={g.id:{} for g in self.w.divinities.values()}
        for p in self.w.characters.values():
            if not p.alive:continue
            for god in self.w.divinities.values():
                b=p.beliefs.get(god.id,{});a=p.social_state.get('religious_activity',{}).get(god.id,{})
                follower=b.get('believed_divine',False) and b.get('confidence',0)>=30
                cult=self.w.turn-a.get('last_cult',-1000)<=200
                actor=a.get('acts',0)>0 and self.w.turn-a.get('last_actor',-1000)<=200
                if not (follower or cult or actor):continue
                r=data[god.id].setdefault(p.town_id,{**dict.fromkeys(LAYERS,0),'favorites':0,'population':0})
                r['followers']+=int(follower);r['devoted']+=int(follower and p.devotion>=65)
                r['cultists']+=int(cult);r['actors']+=int(actor)
                r['favorites']+=int(self.e.divine_relations.affinity(god,p.id)>=75)
        populations={t.id:sum(self.w.characters[i].alive for i in t.resident_ids) for t in self.w.towns.values()}
        for regions in data.values():
            for region,r in regions.items():r['population']=populations.get(region,0)
        return data
    @staticmethod
    def classify(before,current,importance=0,duration=100,shock=False,rival_growth=0):
        lost={k:max(0,before.get(k,0)-current.get(k,0)) for k in LAYERS}
        ratios={k:lost[k]/max(1,before.get(k,0)) for k in LAYERS}
        core_losses=[k for k in ('devoted','cultists','actors') if lost[k]>0 and ratios[k]>=.3]
        core_growth=any(current.get(k,0)>before.get(k,0) for k in ('devoted','cultists','actors'))
        if shock:return 'REGIONAL_CRISIS' if importance>=60 else 'CORE_EROSION'
        if not any(lost.values()):return 'STABLE'
        if before.get('cultists',0)>=2 and current.get('cultists',0)==0 and core_losses and duration>=100:return 'CULT_COLLAPSE'
        if len(core_losses)>=2 and ratios['followers']>=.5 and duration>=100:return 'EXISTENTIAL_RELIGIOUS_THREAT'
        if len(core_losses)>=2 and ratios['followers']>=.3 and importance>=60:return 'REGIONAL_CRISIS'
        if core_losses and (lost['actors']>=1 or lost['cultists']>=2 or lost['devoted']>=2):return 'CORE_EROSION'
        if lost['followers'] and core_growth:return 'STABLE'
        return 'REGIONAL_CRISIS' if ratios['followers']>=.4 and lost['followers']>=3 and importance>=60 and rival_growth>=2 and duration>=100 else 'MINOR_DECLINE'
    def importance(self,god,region,counts):
        birthplace=god.essence.setdefault('birth_region',god.location.map_id)
        return min(100,(70 if region==birthplace else 25 if region in god.influence else 0)+
                   (20 if counts.get('followers',0)/max(1,counts.get('population',0))>=.5 else 0)+
                   min(30,counts.get('favorites',0)*15))
    def shock(self,event):
        for god in self.w.divinities.values():
            affinity=self.e.divine_relations.affinity(god,event.target_id)
            if affinity<75:continue
            row=self.w.faith_health.setdefault(god.id,{'regions':{},'global':{},'shocks':[]})
            row.setdefault('shocks',[]).append({'fact':event.id,'turn':self.w.turn,'region':event.location.map_id,'affinity':affinity,'follower':event.target_id})
            del row['shocks'][:-8]
            self.e.recorder.emit('HighAffinityFollowerLost',f'A fé de {god.name} perdeu um mortal favorecido.',
                witnesses=[],historical=True,context={'god':god.id,'follower':event.target_id,'source_fact':event.id,'affinity':affinity})
    def tick(self,force=False):
        if not force and self.w.turn%24:return
        counts=self.composition();empty=dict.fromkeys((*LAYERS,'favorites','population'),0)
        for god in self.w.divinities.values():
            state=self.w.faith_health.setdefault(god.id,{'regions':{},'global':{},'shocks':[]})
            regions=set(counts[god.id])|set(state['regions'])
            total=dict(empty)
            for region in sorted(regions):
                now=counts[god.id].get(region,dict(empty));old=state['regions'].setdefault(region,{'snapshots':[],'state':'STABLE','counts':dict(now)})
                snapshots=old['snapshots']
                if not snapshots:snapshots.append({'turn':self.w.turn,'counts':dict(now)})
                candidates=[s for s in snapshots if s['turn']<=self.w.turn-100]
                baseline=max(candidates,key=lambda s:s['turn']) if candidates else snapshots[0]
                importance=self.importance(god,region,now)
                shocks=[s for s in state.get('shocks',[]) if s['region']==region and self.w.turn-s['turn']<=100]
                rival_growth=0
                for rival in self.w.divinities:
                    if rival==god.id:continue
                    other=self.w.faith_health.get(rival,{}).get('regions',{}).get(region,{})
                    past=other.get('snapshots',[])
                    first=past[0]['counts']['followers'] if past else counts[rival].get(region,{}).get('followers',0)
                    rival_growth=max(rival_growth,counts[rival].get(region,{}).get('followers',0)-first)
                label=self.classify(baseline['counts'],now,importance,self.w.turn-baseline['turn'],bool(shocks),rival_growth)
                if label!=old['state']:
                    if now['followers']!=baseline['counts']['followers']:
                        self.e.recorder.emit('FaithInfluenceChanged',f'A participação religiosa de {god.name} mudou na região.',
                            witnesses=[],historical=True,context={'god':god.id,'region':region,
                                'before':baseline['counts']['followers'],'followers':now['followers'],
                                'population':now['population'],'objective_audit_only':True})
                    self.e.recorder.emit('RegionalFaithHealthChanged',f'A condição religiosa de {god.name} mudou em {self.w.maps[region].name}.',
                        witnesses=[],historical=True,context={'god':god.id,'region':region,'previous':old['state'],'state':label,
                            'counts':now,'baseline':baseline['counts'],'importance':importance,'rival_growth':rival_growth,
                            'objective_audit_only':True})
                    metric={'CORE_EROSION':'CoreErosionDetected','REGIONAL_CRISIS':'RegionalReligiousCrisisDetected','CULT_COLLAPSE':'CultCollapseDetected'}.get(label)
                    if metric:self.w.metrics[metric]=self.w.metrics.get(metric,0)+1
                old.update(counts=dict(now),state=label,importance=importance,rival_growth=rival_growth,baseline=baseline['counts'])
                if self.w.turn-snapshots[-1]['turn']>=100:
                    snapshots.append({'turn':self.w.turn,'counts':dict(now)});del snapshots[:-3]
                for k in total:total[k]+=now.get(k,0)
            global_old=state['global'];snapshots=global_old.setdefault('snapshots',[])
            if not snapshots:snapshots.append({'turn':self.w.turn,'counts':dict(total)})
            baseline=next((s for s in reversed(snapshots) if s['turn']<=self.w.turn-100),snapshots[0])
            label=self.classify(baseline['counts'],total,0,self.w.turn-baseline['turn'])
            if label!=global_old.get('state','STABLE'):
                self.e.recorder.emit('GlobalFaithHealthChanged',f'A condição religiosa global de {god.name} mudou.',
                    witnesses=[],historical=True,context={'god':god.id,'state':label,'previous':global_old.get('state','STABLE'),
                        'counts':total,'baseline':baseline['counts'],'objective_audit_only':True})
            global_old.update(counts=total,state=label)
            if self.w.turn-snapshots[-1]['turn']>=100:snapshots.append({'turn':self.w.turn,'counts':dict(total)});del snapshots[:-3]
    def on_fact(self,p,f):
        if f.confidence<60:return
        congregations=p.social_state.setdefault('known_congregations',{}) if f.kind in ('PrayerOffered','CultDefenseDeclared','FaithReinterpreted') else p.social_state.get('known_congregations',{})
        if f.kind in ('PrayerOffered','CultDefenseDeclared') and f.target_id in self.w.divinities:
            members=congregations.setdefault(f.target_id,{})
            members[f.actor_id]={'active':True,'cultist':True,'fact':f.event_id,'region':f.location.map_id,'turn':f.turn}
            while len(members)>16:members.pop(next(iter(members)))
        if f.kind in ('CharacterKilled','CharacterDied','FaithReinterpreted'):
            subject=f.target_id if f.kind!='FaithReinterpreted' else f.actor_id
            for god,members in congregations.items():
                if subject not in members:continue
                if f.kind=='FaithReinterpreted':
                    from .faith import GODS
                    name=self.w.divinities[god].name;current=f.context.get('current','')
                    if current=='Culto de '+name or GODS.get(current,('',None))[0]==name:continue
                    rival=next((g.id for g in self.w.divinities.values() if current=='Culto de '+g.name or GODS.get(current,('',None))[0]==g.name),None)
                    members[subject]['rival']=rival
                members[subject].update(active=False,loss_fact=f.event_id,loss_turn=f.turn)
    def report(self,p,god):
        members=p.social_state.get('known_congregations',{}).get(god.id,{})
        local={i:r for i,r in members.items() if r['region']==p.position.map_id and self.w.turn-r['turn']<=200}
        lost=[r for r in local.values() if not r['active']]
        if len(lost)<2:return None
        sources=[r['loss_fact'] for r in lost][-3:]
        before={'followers':len(local),'devoted':0,'cultists':len(local),'actors':0}
        current={**before,'followers':len(local)-len(lost),'cultists':len(local)-len(lost)}
        importance=70 if god.essence.get('birth_region',god.location.map_id)==p.position.map_id else 25
        state=self.classify(before,current,importance,100)
        return {'state':state,'losses':len(lost),'layers':['cultists','followers'],'counts':current,
                'baseline':before,'importance':importance,'source_facts':sources,'scope':'observed_congregation',
                'estimated':True,'rival_growth':sum(bool(r.get('rival')) for r in lost)}
    def send_report(self,p,god):
        summary=self.report(p,god)
        if not summary:return False
        if self.w.turn-p.social_state.get('last_congregation_report',-1000)<72:return False
        event=self.e.recorder.emit('ReligiousDeclineReported',f'{p.name} relatou perdas de sua congregação.',p.id,god.id,p.position,
            historical=True,context=summary)
        self.e.divine_relations.receive(god,event,'cult_report',60,context=summary)
        self.w.metrics['FaithLossLearnedByGod']=self.w.metrics.get('FaithLossLearnedByGod',0)+1
        p.social_state['last_congregation_report']=self.w.turn;return True
