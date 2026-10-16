"""Pressão relacional auditável. Não modifica potência, dano ou aleatoriedade."""
from .rules import INTERACTION

REPAIRS={'CalmingAttempted','RestitutionDemanded','CharacterWarned','ApologyGiven'}
HOSTILE={'CharacterAttacked','CharacterThreatened','CharacterInsulted','CharacterKilled'}

class LethalPressure:
    def __init__(self,e):self.e,self.w=e,e.world

    def count(self,key):
        key='Lethal:'+key;self.w.metrics[key]=self.w.metrics.get(key,0)+1

    def history(self,p,target):
        h=p.combat.conflict_history.setdefault(target,{'started':self.w.turn,'episodes':0,'hostile_episodes':0,'failed_alternatives':0})
        while len(p.combat.conflict_history)>8:
            del p.combat.conflict_history[next(iter(p.combat.conflict_history))]
        return h

    def on_fact(self,p,f):
        if f.confidence<30:return
        if f.actor_id==p.id and f.target_id and f.kind in REPAIRS:
            h=self.history(p,f.target_id)
            if f.event_id>h.get('last_alternative_fact',-1):
                h['last_alternative_fact']=f.event_id
                h['pending_alternative']={'fact':f.event_id,'turn':f.turn,'kind':f.kind}
        if f.actor_id in (None,p.id) or f.kind not in HOSTILE:return
        strength,_=self.e.needs.personal.relationship(p,f.target_id)
        if f.target_id!=p.id and strength<40:return
        h=self.history(p,f.actor_id)
        if f.turn-h.get('last_hostility',-1000)>INTERACTION.conflict_timeout:
            h['hostile_episodes']=h.get('hostile_episodes',0)+1
        h['last_hostility']=max(f.turn,h.get('last_hostility',-1))
        h['last_evidence']=f.event_id
        if f.kind=='CharacterKilled':h['known_murder']=f.event_id;h['loss_strength']=strength
        if f.kind=='CharacterAttacked' and f.target_id==p.id and f.event_id>h.get('last_injury_fact',-1):
            h['last_injury_fact']=f.event_id
            h['injury_received']=min(100,h.get('injury_received',0)+f.context.get('damage',0))
        alternative=h.get('pending_alternative')
        if alternative and f.turn>alternative['turn'] and f.confidence>=60:
            h['failed_alternatives']=min(6,h.get('failed_alternatives',0)+1)
            h['last_failed_alternative']=alternative['fact'];h.pop('pending_alternative',None)
        if f.kind in ('CharacterAttacked','CharacterKilled') and f.confidence>=60:
            grievance=p.grievances.get(f.actor_id)
            for c in p.commitments.values():
                if c.status not in ('active','paused','waiting_for_information') or c.motivation not in ('response','revenge','protection'):continue
                n=next((n for n in p.needs.values() if n.id==c.originating_need),None)
                target=n.context.get('threat') if n and n.kind=='protection' else c.target_id
                if target!=f.actor_id or not grievance:continue
                depth=grievance.intensity*f.confidence/100
                if depth>c.intensity:
                    previous=c.intensity;c.intensity=depth
                    sources=c.context.setdefault('supporting_facts',[])
                    if f.event_id not in sources:sources.append(f.event_id);del sources[:-3]
                    if depth-previous>=5:self.e.agency.event(p,'CommitmentDeepened',c,previous=previous,intensity=depth,
                        reinforcing_fact=f.event_id,reason='new_known_harm_against_same_target')


    def sustained_response(self,p,n):
        """Uma reação imediata só amadurece por dano próprio atribuído e grave."""
        f=p.knowledge.get(n.context.get('source_event'))
        target=n.target_id;g=p.grievances.get(target);h=p.combat.conflict_history.get(target,{})
        if not f or f.kind!='CharacterAttacked' or f.confidence<60 or f.actor_id!=target or f.target_id!=p.id:return False
        return bool(g and g.intensity>=60 and
                    (h.get('hostile_episodes',0)>=2 and h.get('injury_received',0)>=20 or
                     h.get('injury_received',0)>=35 and p.health<40))

    def evaluate(self,p,target,n,audit=False):
        t=self.e.conflicts.terms(p,target.id);traits=p.personality
        c=self.e.agency.current(p,n) if n else None
        commitment_strength=max(c.intensity,self.e.agency.profile(p,n)['impulse']) if c else 0
        g=p.grievances.get(target.id);h=p.combat.conflict_history.get(target.id,{})
        source=p.knowledge.get(n.context.get('source_event')) if n else None
        directed=[f for f in p.knowledge.values() if f.actor_id==target.id and f.kind in HOSTILE and
                  (f.target_id==p.id or self.e.needs.personal.relationship(p,f.target_id)[0]>=40)]
        # A fonte do compromisso e da grievance também pode demonstrar autoria;
        # nenhum acesso à lista global de eventos ou à posição remota do alvo.
        for f in (source,p.knowledge.get(g.source_fact) if g else None):
            if f and f.actor_id==target.id and f.kind in HOSTILE and f not in directed:directed.append(f)
        murder_confidence=max((f.confidence for f in directed if f.kind=='CharacterKilled'),default=0)
        injury_confidence=max((f.confidence for f in directed if f.kind=='CharacterAttacked' and f.target_id==p.id),default=0)
        murder=murder_confidence>0
        loss_importance=max((self.e.needs.personal.relationship(p,f.target_id)[0]*f.confidence/100
                             for f in directed if f.kind=='CharacterKilled'),default=0)
        episodes=h.get('hostile_episodes',0)
        injury=h.get('injury_received',0)
        failed=h.get('failed_alternatives',0)
        harm=g.intensity if g else 0
        physical_grave=(episodes>=2 and injury>=20) or (injury>=35 and p.health<40)
        grave=murder or physical_grave
        confidence=max(murder_confidence if murder else 0,injury_confidence if physical_grave else 0) if grave else max((f.confidence for f in directed),default=0)
        grave_basis='known_murder' if murder and (not physical_grave or murder_confidence>=injury_confidence) else 'recurrent_physical_danger' if physical_grave else 'none'
        rage=min(harm,(p.emotions.anger+p.emotions.resentment)/2)
        irrational=(confidence>=30 and episodes>=3 and injury>=35 and traits.vengefulness>=95
                    and traits.compassion<10 and rage>=90)
        positives={'directed_grievance':round(harm*.35,2),'directed_emotion':round(rage*.2,2),
            'vengefulness':traits.vengefulness*.15,'commitment':commitment_strength*.2,
            'grave_loss_or_danger':40 if grave else 0,'attributed_important_loss':loss_importance*.2,'failed_alternatives':min(24,failed*8),
            'investment':min(10,c.investment/12) if c else 0,
            'related_desperation':min(5,p.emotions.desperation*.05) if grave else 0}
        alternatives=not murder and failed==0 and not (injury>=35 and p.health<40)
        barriers={'compassion':traits.compassion*.8,'honesty':traits.honesty*.15,
            'fear':t['fear']*(30+(100-traits.courage)*.2),'risk':t['risk']*15,
            'authority_or_witnesses':t['authority']*25,'bond':t['bond']*50,
            'uncertain_authorship':(100-confidence)*.6,'plausible_nonlethal_alternative':25 if alternatives else 0,
            'institutional_duty':35 if p.profession=='guarda' and self.e.justice.record_for(p,target.id) else 0}
        known_wanted=any(f.kind=='WantedIssued' and f.context.get('suspect_id')==p.id and self.w.turn-f.turn<168 for f in p.knowledge.values())
        witnesses=sum(o.turn==self.w.turn and o.position==p.position and i!=target.id for i,o in p.observations.items())
        reputation=p.reputations.get(target.id)
        barriers['known_criminal_consequences']=10 if known_wanted else 0
        barriers['witnesses']=min(12,witnesses*3)
        barriers['known_reputation']=min(12,reputation.fear*.12) if reputation else 0
        pressure=round(sum(positives.values())-sum(barriers.values()),2)
        reasons=[]
        substantial_cause=harm>=60 or murder_confidence>=60 and loss_importance>=60
        if not directed or not grave or not substantial_cause:reasons.append('insufficient_pressure')
        if confidence<60 and not irrational:reasons.append('low_confidence')
        if not c or commitment_strength<60 or c.status=='waiting_for_information':reasons.append('insufficient_commitment')
        if traits.compassion>=80:reasons.append('compassion')
        if p.health<=INTERACTION.incapacity_health or p.combat.detention_until>self.w.turn:reasons.append('actor_incapacity')
        if target.id not in self.e.spatial.at(p.position):reasons.append('target_absent')
        if t['fear']>.8 and traits.courage<40:reasons.append('fear')
        if pressure<45 and not reasons:
            strongest=max(barriers,key=barriers.get)
            reasons.append({'authority_or_witnesses':'authority_or_witnesses','risk':'risk','fear':'fear',
                'compassion':'compassion','uncertain_authorship':'low_confidence',
                'plausible_nonlethal_alternative':'nonlethal_better'}.get(strongest,'insufficient_pressure'))
        result={'available':not reasons,'pressure':pressure,'positive_factors':positives,'barriers':barriers,
            'blocking':reasons,'confidence':confidence,'known_facts':[f.event_id for f in sorted(directed,key=lambda f:f.turn)[-3:]],
            'source_fact':source.event_id if source else None,'commitment_id':c.id if c else None,
            'motive':n.kind if n else None,'commitment_intensity':c.intensity if c else 0,'current_commitment_strength':commitment_strength,
            'episodes':episodes,'failed_alternatives':failed,'irrational_suspicion':irrational,
            'grave_basis':grave_basis,'loss_importance':loss_importance,'murder_confidence':murder_confidence,'physical_harm_confidence':injury_confidence}
        result['mode']='persistent'
        if not result['available']:
            situational=self.e.terminal_combat.situational(p,target,n)
            if situational['available']:result=situational
        if audit:
            self.count('evaluated');self.count('available' if result['available'] else 'precondition_failed')
            for reason in result['blocking']:self.count('blocked:'+reason)
        return result
