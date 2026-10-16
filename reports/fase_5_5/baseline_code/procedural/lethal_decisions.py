"""Decisão é persistente; avaliações e oportunidades são consultas sem efeitos."""
from dataclasses import asdict
from .models import LethalDecision, Aspiration
from .needs import FINISHED

MODES={'reactive_threat','retributive','protective','instrumental','moral_punishment','hedonic'}
HOSTILE={'CharacterAttacked','CharacterKilled','CharacterThreatened','CharacterInsulted','ItemStolen'}

def clamp(x):return round(max(0,min(100,x)),2)

class LethalDecisionSystem:
    def __init__(self,e):self.e,self.w=e,e.world
    @staticmethod
    def active(p,target):
        d=p.lethal_decisions.get(target)
        return d if d and d.status=='active' else None
    def emit(self,p,kind,target=None,**context):
        return self.e.recorder.emit(kind,f'{p.name}: {kind}.',p.id,location=p.position,
            witnesses=[p.id],historical=True,context={'target_id':target,**context})
    def cause(self,p,target,n=None):
        """Somente fatos próprios e objetivos instrumentais já conhecidos."""
        facts=[f for f in p.knowledge.values() if f.actor_id==target and f.kind in HOSTILE and f.confidence>=60]
        directed=[f for f in facts if f.target_id==p.id or self.e.needs.personal.relationship(p,f.target_id)[0]>=40]
        h=p.combat.conflict_history.get(target,{})
        attacks=[f for f in directed if f.kind=='CharacterAttacked']
        own=[f for f in attacks if f.target_id==p.id]
        recent=[f for f in attacks if self.w.turn-f.turn<=3]
        recent_damage=sum(f.context.get('damage',0) for f in recent)
        confirmed=h.get('confirmed_injury_received',sum(f.context.get('damage',0) for f in own))
        murder=[f for f in directed if f.kind=='CharacterKilled']
        insult=[f for f in directed if f.kind=='CharacterInsulted']
        cause='none';mode='retributive';severity=0;basis=[]
        if murder:severity=90;cause='known_close_loss';basis=murder
        elif recent and (recent_damage>=8 or any(f.context.get('violence_intent')=='kill' for f in recent)):
            severity=75 if recent_damage>=15 or p.health<40 else 55
            mode='reactive_threat' if any(f.target_id==p.id for f in recent) else 'protective'
            cause='immediate_physical_threat';basis=recent
        elif confirmed>=10 and own:
            severity=65 if confirmed>=20 else 45;cause='unresolved_attributed_injury';basis=own
        elif attacks and sum(f.context.get('damage',0) for f in attacks)>=10:
            severity=50;mode='protective';cause='known_harm_to_close_person';basis=attacks
        elif len(insult)>=2 and p.personality.vengefulness>=75 and p.emotions.humiliation>=35:
            severity=40;cause='repeated_humiliation';basis=insult
        elif n and n.kind=='pursuit' and n.context.get('severity',0)>=5:
            murders=[f for f in facts if f.kind=='CharacterKilled']
            if murders:severity=65;mode='moral_punishment';cause='known_homicide_and_duty';basis=murders
        elif n and n.kind=='revenge' and p.personality.greed>=75:
            theft=[f for f in directed if f.kind=='ItemStolen' and f.target_id==p.id]
            if theft and max(p.hunger,p.thirst)>=85:
                severity=45;mode='instrumental';cause='known_theft_of_vital_resource';basis=theft
        if not severity and self.seeking(p):
            obs=p.observations.get(target)
            if obs and obs.alive and self.w.turn-obs.turn<=24 and self.e.needs.personal.relationship(p,target)[0]<40:
                severity=50;mode='hedonic';cause='reinforced_death_seeking_and_known_opportunity'
        return {'severity':severity,'grave':severity>=40,'causes':[cause] if severity else [],
                'facts':[f.event_id for f in sorted(basis,key=lambda f:f.turn)[-3:]],
                'confidence':max((f.confidence for f in basis),default=100 if severity else 0),
                'mode':mode,'confirmed_injury':confirmed}
    def evaluate(self,p,target,n=None):
        if not target:return {'available':False,'pressure':0,'blocking':['unknown_target']}
        d=self.active(p,target.id);cause=self.cause(p,target.id,n);traits=p.personality
        t=self.e.conflicts.terms(p,target.id);g=p.grievances.get(target.id)
        c=self.e.agency.current(p,n) if n else None
        harm=g.intensity if g else 0
        justification=.65 if cause['mode'] in ('reactive_threat','protective') else .8 if cause['mode']=='moral_punishment' else 1
        impellors={'instigation':cause['severity']*.5,'vengefulness':traits.vengefulness*.17,
            'directed_emotion':min(harm,(p.emotions.anger+p.emotions.resentment)/2)*.22,
            'commitment':(c.intensity if c else 0)*.12,'sadism':traits.sadism*.13,
            'death_affinity':p.death_affinity*.15,'failed_repair':min(12,p.combat.conflict_history.get(target.id,{}).get('failed_alternatives',0)*4)}
        inhibitors={'harm_aversion':traits.compassion*.55*justification,'moral_restraint':traits.honesty*.12*justification,
            'fear':t['fear']*(25+(100-traits.courage)*.15),'risk':t['risk']*12,
            'bond':t['bond']*60,'authority_or_witnesses':t['authority']*15,
            'uncertain_authorship':(100-cause['confidence'])*.5,
            'available_nonlethal_alternative':10 if cause['severity']<65 else 0}
        pressure=round(30+sum(impellors.values())-sum(inhibitors.values()),2)
        blocks=[]
        if not cause['grave'] and not d:blocks.append('insufficient_pressure')
        if cause['confidence']<60 and not d:blocks.append('low_confidence')
        if t['fear']>.85 and traits.courage<30:blocks.append('fear')
        if pressure<40 and not d:blocks.append('inhibition')
        if traits.compassion>=90 and cause['mode'] not in ('reactive_threat','protective'):blocks.append('compassion')
        # A capacidade e a localização impedem execução, não apagam desejo.
        if d:
            pressure=max(pressure,55+d.intensity*.25+d.rumination*.15)
            cause={'severity':d.world_pressure,'facts':list(d.facts),'confidence':d.confidence,'mode':d.mode,'causes':[d.cause]}
            blocks=[]
        return {'available':not blocks,'pressure':pressure,'mode':cause['mode'],'confidence':cause['confidence'],
            'known_facts':cause['facts'],'source_fact':cause['facts'][-1] if cause['facts'] else None,
            'commitment_id':d.commitment_id if d else c.id if c else None,'motive':n.kind if n else None,
            'world_pressure':cause['severity'],'grave_basis':cause['causes'][0] if cause['causes'] else 'none',
            'blocking':blocks,'positive_factors':impellors,'barriers':inhibitors,
            'decision_id':d.id if d else None,'rumination':d.rumination if d else 0,
            'current_commitment_strength':c.intensity if c else 0,'commitment_intensity':c.intensity if c else 0}
    def consider(self,p,target,n):
        d=self.active(p,target.id)
        if d:return d
        # Eventos da própria deliberação não podem expulsar a causa avaliada.
        with self.e.knowledge.protect(p,self.cause(p,target.id,n)['facts']):
            return self._consider(p,target,n)
    def _consider(self,p,target,n):
        d=self.active(p,target.id)
        if d:return d
        old=p.lethal_decisions.get(target.id)
        cause=self.cause(p,target.id,n)
        if old and old.status in ('abandoned','resolved') and set(cause['facts'])<=set(old.facts):return None
        audit=self.evaluate(p,target,n)
        # Escolha de intenção compete com contenção comum. Não altera dano.
        scores=self.e.conflicts.intent_scores(p,target,n)
        competitor=max((k for k in scores if k!='kill'),key=lambda k:(scores[k],k))
        rejected=not audit['available'] or audit['pressure']<scores[competitor]
        if cause['severity']>=40:
            transitions=p.agency_state.setdefault('lethal_candidates',{})
            marker=(audit['source_fact'],audit['available'],rejected,tuple(audit['blocking']),competitor)
            if tuple(transitions.get(target.id,()))!=marker:
                # Transição contextual com causa plausível, não consulta por tick.
                transitions[target.id]=marker
                while len(transitions)>4:transitions.pop(next(iter(transitions)))
                telemetry={'mode':audit['mode'],'cause':audit['grave_basis'],'source_facts':list(audit['known_facts']),
                    'world_pressure':audit['world_pressure'],'lethal_score':audit['pressure'],
                    'alternative':competitor,'alternative_score':scores[competitor],'blocking':list(audit['blocking'])}
                self.emit(p,'LethalCandidateEvaluated',target.id,**telemetry)
                if rejected:self.emit(p,'LethalCandidateRejected',target.id,**telemetry)
        if rejected:return None
        marker=(target.id,audit['source_fact'])
        if tuple(p.agency_state.get('lethal_consideration',()))!=marker:
            self.emit(p,'LethalConsideration',target.id,lethal_audit=audit)
            p.agency_state['lethal_consideration']=marker
        if len(p.lethal_decisions)>=4 and target.id not in p.lethal_decisions:
            closed=next((i for i,d in p.lethal_decisions.items() if d.status!='active'),None)
            if closed is None:return None
            del p.lethal_decisions[closed]
        c=self.e.agency.current(p,n)
        if not c:c=self.e.agency.adopt(p,n,force=True)
        wp=audit['world_pressure'];ap=self.e.action_pressure.disposition(wp,p.personality.persistence,65,0,0,0)
        d=LethalDecision(self.w.allocate_id(),p.id,target.id,audit['mode'],audit['grave_basis'],
            list(audit['known_facts']),self.w.turn,self.w.turn,audit['confidence'],clamp(audit['pressure']),wp,ap,
            audit['positive_factors'],audit['barriers'],c.id if c else None,
            rumination=clamp((p.emotions.anger+p.emotions.resentment)/3),last_reinforced=self.w.turn,
            context={'need_id':n.id,'initial_fact':audit['source_fact'],'initial_fear':self.e.conflicts.terms(p,target.id)['fear'],'initial_compassion':p.personality.compassion,'known_location':n.context.get('known_location')})
        p.lethal_decisions[target.id]=d;p.combat.violence_intents[target.id]='kill'
        self.emit(p,'LethalDecision',target.id,decision=asdict(d));return d
    def close(self,p,d,reason,resolved=False):
        if d.status!='active':return
        d.status='resolved' if resolved else 'abandoned';d.reason=reason;d.updated_at=self.w.turn
        p.combat.violence_intents.pop(d.target_id,None);p.combat.pending_judgments.pop(d.target_id,None)
        self.emit(p,'LethalDecisionResolved' if resolved else 'LethalDecisionAbandoned',d.target_id,
            decision_id=d.id,mode=d.mode,reason=reason,source_facts=list(d.facts),rumination=d.rumination)
        n=next((n for n in p.needs.values() if n.id==d.context.get('need_id')),None)
        if n:self.e.needs.finish(p,n)
    def on_fact(self,p,f):
        for d in list(p.lethal_decisions.values()):
            if d.status!='active':continue
            if f.target_id==d.target_id and f.kind in ('CharacterDied','CharacterKilled','RemainsLocated') and f.confidence>=60:
                self.close(p,d,'known_target_death',True);continue
            if f.actor_id==d.target_id and f.kind in HOSTILE and f.target_id==p.id and f.confidence>=60:
                if f.event_id not in d.facts:
                    d.facts.append(f.event_id);del d.facts[:-3];d.rumination=clamp(d.rumination+12)
                    d.last_reinforced=self.w.turn
                    history=p.combat.conflict_history.get(d.target_id,{})
                    grievance=p.grievances.get(d.target_id)
                    if (d.mode in ('reactive_threat','protective') and history.get('confirmed_injury_received',0)>=20
                            and grievance and grievance.intensity>=40 and p.personality.vengefulness>=60):
                        previous=d.mode;d.mode='retributive';d.cause='repeated_unresolved_known_harm'
                        d.world_pressure=max(65,d.world_pressure)
                        self.emit(p,'LethalDecisionUpdated',d.target_id,decision_id=d.id,previous_mode=previous,
                            mode=d.mode,reason=d.cause,source_fact=f.event_id)
            if (f.actor_id==d.target_id and f.kind=='CharacterKilled' and f.confidence>=60
                    and self.e.needs.personal.relationship(p,f.target_id)[0]>=40 and d.mode!='retributive'):
                previous=d.mode;d.mode='retributive';d.cause='known_close_loss';d.world_pressure=90
                d.facts.append(f.event_id);d.facts=list(dict.fromkeys(d.facts))[-3:]
                d.rumination=clamp(d.rumination+25);d.last_reinforced=self.w.turn
                self.emit(p,'LethalDecisionUpdated',d.target_id,decision_id=d.id,previous_mode=previous,
                    mode=d.mode,reason=d.cause,source_fact=f.event_id)
            repaired=(f.actor_id==d.target_id and f.target_id==p.id and f.kind in ('ApologyGiven','RestitutionGiven')
                      or f.actor_id==p.id and f.target_id==d.target_id and f.kind=='ConflictForgiven')
            if repaired and f.confidence>=60:
                d.rumination=clamp(d.rumination-35)
                material_repair=f.kind=='RestitutionGiven' and d.cause=='known_theft_of_vital_resource' and f.context.get('quantity',0)>0
                accepted_apology=f.kind=='ApologyGiven' and (p.personality.compassion>=40 or d.rumination<20) and d.cause!='known_close_loss'
                if f.kind=='ConflictForgiven' or material_repair or accepted_apology:
                    self.close(p,d,'forgiveness_or_meaningful_repair')
            if f.kind=='SuspectExonerated' and f.target_id==d.target_id and f.confidence>=80:
                self.close(p,d,'credible_changed_authorship')
    def seeking(self,p):
        return (p.death_affinity>=55 and p.death_state.get('positive_kills',0)>=2 and
                p.personality.sadism>=65 and p.personality.compassion<25 and p.death_state.get('guilt',0)<25)
    def refresh(self,p):
        now=self.w.turn
        self.e.aftermath.refresh(p)
        if self.seeking(p) and max(p.hunger,p.thirst,p.fatigue)<80 and p.health>35:
            if not any(a.domain=='seek_violent_opportunity' and a.status=='active' for a in p.aspirations):
                if len(p.aspirations)>=2:
                    old=next((a for a in p.aspirations if not a.principal or a.status!='active'),None)
                    if old:p.aspirations.remove(old)
                if len(p.aspirations)<2:
                    p.aspirations.append(Aspiration('seek_violent_opportunity',p.death_affinity,now,principal=False,
                        context={'reason':'repeated_positive_intentional_killing','last_offered':now}))
                    self.emit(p,'ViolenceSeekingCreated',death_affinity=p.death_affinity)
            candidates=[i for i in self.e.spatial.at(p.position) if i!=p.id and self.e.needs.personal.relationship(p,i)[0]<40]
            if candidates:
                target=min(candidates,key=lambda i:(p.observations[i].weapon_power or 6,i))
                n=self.e.needs.ensure(p,'response:death_seeking',60+p.death_affinity*.2,'encounter:reinforced_death_seeking',
                    'Buscar oportunidade violenta por trajetória reforçada',target)
                n.context.update(known_location=vars(p.position),mode='hedonic')
                self.consider(p,self.w.characters[target],n)
        for d in list(p.lethal_decisions.values()):
            if d.status!='active':continue
            dt=max(0,now-d.updated_at);d.updated_at=now
            obs=p.observations.get(d.target_id);present=d.target_id in self.e.spatial.at(p.position)
            if present and p.grievances.get(d.target_id) and now-d.last_reinforced>=24:
                d.rumination=clamp(d.rumination+3);d.last_reinforced=now
            safe=not p.combat.opponents and max(p.hunger,p.thirst)<80 and p.health>=65
            if safe and not present and now-d.last_reinforced>72:
                d.rumination=clamp(d.rumination-dt*(.1+(100-p.personality.persistence)/500))
            fear=self.e.conflicts.terms(p,d.target_id)['fear']
            if present and fear>=.95 and p.personality.courage<25 and fear-d.context.get('initial_fear',fear)>.4:
                self.close(p,d,'new_overwhelming_perceived_danger');continue
            if p.personality.compassion>=90 and d.context.get('initial_compassion',90)<70 and d.mode not in ('reactive_threat','protective'):
                self.close(p,d,'changed_moral_restraint');continue
            bond=self.e.needs.personal.relationship(p,d.target_id)[0]
            if bond>=80 and d.mode not in ('reactive_threat','protective'):
                self.close(p,d,'restored_strong_bond');continue
            if d.rumination<5 and safe and now-d.last_reinforced>168 and p.personality.vengefulness<65:
                self.close(p,d,'safe_life_and_diminished_rumination');continue
            n=next((n for n in p.needs.values() if n.id==d.context.get('need_id')),None)
            if n:
                if n.status in FINISHED:n.status='active'
                n.expires_at=None;n.base_urgency=max(n.base_urgency,min(85,50+d.intensity*.3))
                n.context['lethal_decision_id']=d.id
                if obs and obs.alive:n.context['known_location']=vars(obs.position)
                c=self.e.agency.current(p,n)
                if not c:c=self.e.agency.adopt(p,n,force=True);d.commitment_id=c.id if c else None
            p.combat.violence_intents[d.target_id]='kill'
        for n in list(p.needs.values()):
            if n.kind not in ('revenge','response','protection','pursuit') or n.status in FINISHED:continue
            target=n.context.get('threat') if n.kind=='protection' else n.target_id
            if target in self.w.characters and target!=p.id:self.consider(p,self.w.characters[target],n)
    def action_audit(self,p,target,n=None,terminal=False):
        d=self.active(p,target)
        audit=self.evaluate(p,self.w.characters.get(target),n)
        wp=d.world_pressure if d else audit.get('world_pressure',0)
        capacity=clamp(p.health*(1-p.fatigue/150))
        ap=self.e.action_pressure.disposition(wp,p.personality.persistence,65,0,0,
            max(p.fatigue/180,max(p.hunger,p.thirst)/250))
        eligible=bool(d or audit.get('available')) and capacity>=12 and p.combat.detention_until<=self.w.turn and p.combat.surrendered_until<=self.w.turn
        if terminal:
            t=self.terminal(p,self.w.characters.get(target));eligible=eligible and t['choice']=='finish'
        return {'eligible':eligible,'world_pressure':wp,'action_pressure':ap,'eligibility_causes':[d.cause if d else audit.get('grave_basis','none')],
            'source_facts':list(d.facts if d else audit.get('known_facts',[])),'capacity':capacity,'perceived_capacity':capacity,
            'major_barriers':[] if eligible else ['incapacity_or_contextual_inhibition'],'decision_id':d.id if d else None,
            'selected_alternative':'finish' if terminal else 'attack'}
    def terminal(self,p,target):
        d=self.active(p,target.id) if target else None
        if not d:return {'choice':'spare','scores':{'finish':-1000,'spare':50},'reason':'no_active_decision'}
        reactive=d.mode=='reactive_threat';traits=p.personality
        continued=(d.mode in ('retributive','instrumental','moral_punishment','hedonic') or
                   reactive and traits.vengefulness>=75 and traits.compassion<30 and
                   p.combat.conflict_history.get(target.id,{}).get('confirmed_injury_received',0)>=20)
        inhibition=traits.compassion*.55+self.e.needs.personal.relationship(p,target.id)[0]*.6
        finish=d.intensity*.8+d.rumination*.3+traits.sadism*.2+p.death_affinity*.2-inhibition-(70 if not continued else 0)
        scores={'finish':finish,'spare':35+traits.compassion*.4+(35 if not continued else 0),
                'capture':95+traits.honesty*.1 if self.e.justice.record_for(p,target.id) and p.profession=='guarda' else -1000,
                'help':25+traits.compassion*.45 if self.e.items.count(p.id,'food') and self.e.items.count(p.id,'water') else -1000,
                'withdraw':25+self.e.conflicts.terms(p,target.id)['fear']*50}
        scores['help']+=self.e.faith.modifier(p,'first_aid')
        scores['withdraw']+=self.e.faith.modifier(p,'withdraw')
        return {'choice':max(scores,key=lambda k:(scores[k],k)),'scores':{k:round(v,2) for k,v in scores.items()},
                'reason':'persistent_nondefensive_motive' if continued else 'incapacity_removed_immediate_threat',
                'decision_id':d.id,'defensive_threat':0,'inhibition':inhibition,'mode':d.mode,
                'actor':p.id,'target':target.id,'cause':d.cause,'source_facts':list(d.facts),
                'intensity':d.intensity,'world_pressure':d.world_pressure,'action_pressure':d.action_pressure,
                'rumination':d.rumination,'retribution':d.mode=='retributive','continued_motive':bool(continued),
                'compassion':traits.compassion,'fear':self.e.conflicts.terms(p,target.id)['fear'],
                'attachment':self.e.needs.personal.relationship(p,target.id)[0],
                'death_affinity':p.death_affinity,'sadism':traits.sadism,
                'religious_influence':{'help':self.e.faith.modifier(p,'first_aid'),'withdraw':self.e.faith.modifier(p,'withdraw')},
                'actor_health':p.health,'target_health':target.health,'actor_fatigue':p.fatigue}
