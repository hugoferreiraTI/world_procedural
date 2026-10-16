"""Causa, disposição e capacidade separadas; consultas não alteram o mundo."""
from .models import ActionPressure
from .needs import FINISHED

KINDS={'security','revenge','response','protection','pursuit','political_pressure','organizational_survival',
       'governance','military_service','religious_interest','power','family'}
STRONG={'finish','challenge_divinity','assume_local_office','faction_raid'}
FORWARD={'meet_group','attend_group','submit_proposal','read_response','relay_response','represent_travel',
         'review_proposal','report_to_faction','perform_assignment','recruit_member','faction_prepare',
         'faction_raid','follow_lead','pursue','search_area','ask_about_person','finish','challenge_divinity'}

def clamp(x):return round(max(0.,min(100.,x)),2)
def band(value):return 'low' if value<25 else 'medium' if value<55 else 'high' if value<80 else 'extreme'

class ActionPressureSystem:
    def __init__(self,e):self.e,self.w=e,e.world
    @staticmethod
    def key(n):return f"{n.kind}:{n.context.get('group_id',n.context.get('faction_id',n.target_id))}"
    def record(self,p,n):return p.action_pressures.get(self.key(n),ActionPressure())
    def known_harm(self,p,target):
        d=self.e.lethal_decisions.active(p,target)
        if d:return {'grave':True,'severity':d.world_pressure,'causes':[d.cause],'facts':d.facts}
        cause=self.e.lethal_decisions.cause(p,target)
        if cause['grave']:return cause
        facts=[f for f in p.knowledge.values() if f.actor_id==target and f.confidence>=60
               and f.kind in ('CharacterAttacked','CharacterKilled','CharacterThreatened') and
               (f.target_id==p.id or self.e.needs.personal.relationship(p,f.target_id)[0]>=40)]
        attacks=[f for f in facts if f.kind=='CharacterAttacked' and f.target_id==p.id]
        history=p.combat.conflict_history.get(target,{})
        loss=any(f.kind=='CharacterKilled' and self.e.needs.personal.relationship(p,f.target_id)[0]>=40 for f in facts)
        immediate=any(self.w.turn-f.turn<=3 for f in attacks) and (p.health<40 or sum(f.context.get('damage',0) for f in attacks if self.w.turn-f.turn<=3)>=15)
        confirmed=history.get('confirmed_injury_received',sum(f.context.get('damage',0) for f in attacks))
        repeated=(history.get('hostile_episodes',0)>=2 and confirmed>=20)
        severe=(confirmed>=35 and p.health<40)
        grave=loss or immediate or repeated or severe
        sources=[f.event_id for f in sorted(facts,key=lambda f:f.turn)[-3:]]
        if repeated or severe:
            source=history.get('last_confirmed_injury_fact')
            if source and source not in sources:sources.append(source)
        return {'grave':grave,'severity':90 if loss else 85 if immediate else 80 if repeated or severe else 35 if attacks else 15 if facts else 0,
                'causes':['known_close_loss'] if loss else ['immediate_extreme_threat'] if immediate else ['repeated_grave_harm'] if repeated or severe else ['limited_harm'] if facts else [],
                'facts':sources[-3:]}
    def world_pressure(self,p,n):
        if n.kind=='security' and n.context.get('violence_pattern'):
            f=p.knowledge.get(n.context.get('source_event'))
            return {'grave':bool(f and f.confidence>=60),'severity':75 if f and f.confidence>=60 else 0,
                    'causes':['received_local_homicide_pattern'] if f else [],'facts':[f.event_id] if f else []}
        if n.kind in ('revenge','response','protection','pursuit'):
            target=n.context.get('threat',n.target_id) if n.kind=='protection' else n.target_id
            return self.known_harm(p,target)
        if n.kind=='organizational_survival':
            g=self.w.groups.get(n.context.get('group_id'));f=self.w.factions.get(n.context.get('faction_id'))
            owner=g or f
            if owner:return {'grave':owner.action_pressure.world>=80,'severity':owner.action_pressure.world,
                             'causes':[owner.action_pressure.reason],'facts':owner.action_pressure.source_facts}
        if n.kind=='political_pressure':
            own=self.e.society.pressure(p)
            return {'grave':False,'severity':min(75,own[2]) if own else 0,'causes':['continued_personal_problem'] if own else [],'facts':[]}
        if n.kind=='governance':return {'grave':False,'severity':min(85,n.base_urgency) if n.context.get('proposal_id') else 30,'causes':['received_request'] if n.context.get('proposal_id') else ['office_duty'],'facts':[]}
        if n.kind=='religious_interest':
            b=p.beliefs.get(n.target_id,{})
            f=p.knowledge.get(b.get('source_fact'))
            return {'grave':bool(f and f.kind in ('DivinityKilled','DivineIntervention') and f.confidence>=60),
                    'severity':70 if f and f.kind in ('DivinityKilled','DivineIntervention') else 20,
                    'causes':['known_religious_event'] if f else ['personal_faith'],'facts':[f.event_id] if f else []}
        source=p.knowledge.get(n.context.get('source_event'))
        return {'grave':False,'severity':min(65,n.base_urgency),'causes':[n.source], 'facts':[source.event_id] if source else []}
    def disposition(self,severity,persistence,agency,failures,investment,barriers):
        # A causa limita a escala; traços médios nunca fabricam gravidade.
        motivation=(.45+.25*persistence/100+.30*agency/100)
        continuity=min(1.25,1+min(6,failures)*.025+min(48,investment)*.002)
        return clamp(severity*motivation*continuity*(1-min(.8,barriers)))
    def update(self,owner,record,value,world,reason,facts=(),agent_type='npc'):
        previous=record.value
        record.value=clamp(value);record.world=clamp(world);record.updated_at=self.w.turn
        record.reason=reason;record.source_facts=list(dict.fromkeys(facts))[-3:]
        self.count('distribution:'+agent_type+':'+band(record.value))
        if band(previous)!=band(record.value) and (record.value>=55 or previous>=55):
            self.e.recorder.emit('ActionPressureChanged','A pressão contextual para agir mudou.',owner.id,
                location=getattr(owner,'position',getattr(owner,'location',None)),witnesses=[],
                context={'agent_type':agent_type,'before':previous,'value':record.value,'world_pressure':record.world,
                         'reason':reason,'source_facts':record.source_facts})
    def refresh(self,p,active):
        selected={}
        for n in sorted((n for n in active if n.kind in KINDS),key=lambda n:(-n.priority,n.id)):
            selected.setdefault(self.key(n),n)
            if len(selected)==8:break
        # Atualizar todos os interesses numa memória de oito entradas causava
        # expulsão circular e apagava continuidade em toda decisão.
        for key,n in selected.items():
            if key not in p.action_pressures:
                if len(p.action_pressures)>=8:
                    victim=next(k for k in p.action_pressures if k not in selected)
                    p.action_pressures.pop(victim)
                p.action_pressures[key]=ActionPressure()
                self.count('records_created:npc')
            record=p.action_pressures[key];wp=self.world_pressure(p,n)
            c=self.e.agency.current(p,n)
            profile=self.e.agency.profile(p,n);agency=profile['perceived_agency']*100
            barrier=max(p.fatigue/180,max(p.hunger,p.thirst)/250,
                        profile['risk']*.3+profile['uncertainty']*.15)
            if record.last_failure>=0 and self.w.turn-record.last_failure>72:record.failures=max(0,record.failures-1);record.last_failure=self.w.turn
            emotional_persistence=(1+min(.1,(p.emotions.anger+p.emotions.resentment)/2000)) if wp['grave'] else 1
            value=clamp(self.disposition(wp['severity'],p.personality.persistence,agency,record.failures,c.investment if c else 0,barrier)*emotional_persistence)
            self.update(p,record,value,wp['severity'],wp['causes'][0] if wp['causes'] else 'no_current_cause',wp['facts'])
            n.priority=min(100,n.priority+record.value*.14)
        live={self.key(n) for n in active if n.kind in KINDS}
        for key,record in p.action_pressures.items():
            if key not in live and record.value:
                self.update(p,record,record.value*.5,0,'problem_no_longer_active')
    def count(self,key,amount=1):
        k='ActionPressure:'+key;self.w.metrics[k]=self.w.metrics.get(k,0)+amount
    def assess(self,p,n,action,target=None):
        if action in ('attack','finish') and target in self.w.characters:
            decision=self.e.lethal_decisions.active(p,target)
            if action=='finish' or decision:
                q=self.w.characters[target]
                return self.e.lethal_decisions.action_audit(p,target,n,terminal=action=='finish' and q.health<=12)
        if action=='attack' and target in self.w.characters:
            scores=self.e.conflicts.intent_scores(p,self.w.characters[target],n)
            if max(scores,key=lambda k:(scores[k],k))=='kill':
                audit=self.e.lethal_decisions.action_audit(p,target,n)
                return {**audit,'selected_alternative':'attack','violence_intent':'kill'}
        wp=self.known_harm(p,target) if action=='finish' else self.world_pressure(p,n) if n else {'grave':False,'severity':0,'causes':[],'facts':[]}
        value=self.record(p,n).value if n else 0
        if not value and (n or wp['grave']):
            value=self.disposition(wp['severity'],p.personality.persistence,50,0,0,max(p.fatigue/180,max(p.hunger,p.thirst)/250))
        capacity=clamp(p.health*(1-p.fatigue/150))
        barriers=[];eligible=True
        if action=='finish':
            q=self.w.characters.get(target)
            lethal=self.e.lethality.evaluate(p,q,n) if q else {'available':False}
            eligible=wp['grave'] and lethal['available'] and value>=35
            if not eligible:barriers.append('no_grave_supported_lethal_action')
        elif action=='challenge_divinity':
            eligible=wp['grave'] and p.mythic_development>=60 and value>=35
            if not eligible:barriers.append('no_grave_religious_cause_or_capacity')
        elif action=='assume_local_office':
            g=self.w.groups.get(target)
            eligible=bool(g and g.failures>=3 and g.responsibility_id and g.action_pressure.world>=70 and p.profession not in ('guarda','soldado'))
            if not eligible:barriers.append('no_received_escalated_political_cause')
        if action in STRONG and (capacity<12 or p.combat.detention_until>self.w.turn or p.combat.surrendered_until>self.w.turn):
            eligible=False;barriers.append('actor_incapacity')
        return {'eligible':bool(eligible),'world_pressure':wp['severity'],'action_pressure':round(value,2),
                'eligibility_causes':list(wp['causes']),'source_facts':list(wp['facts']),'capacity':capacity,
                'perceived_capacity':clamp(capacity*(.6+p.personality.courage/125)),
                'major_barriers':barriers,'selected_alternative':action}
    def outcome(self,p,n,action,success,before,before_progress=0):
        if not n or n.kind not in KINDS:return
        record=p.action_pressures.get(self.key(n))
        if not record:return
        if not success and self.w.turn-record.last_failure>=12:
            record.failures=min(6,record.failures+1);record.last_failure=self.w.turn
            faction=self.w.factions.get(n.context.get('faction_id'))
            if faction and action in ('faction_prepare','perform_assignment','faction_raid') and faction.knowledge:
                faction.action_pressure.failures=min(6,faction.action_pressure.failures+1)
        if success and action in FORWARD:
            self.count('actions:npc')
            # Avançar de célula, entregar, transmitir ou alterar recurso é consequência.
            if p.position!=before or p.social_state.get('meaningful_social_actions',0)>before_progress or action in ('faction_prepare','faction_raid','perform_assignment','finish','challenge_divinity'):
                self.count('consequences:npc')
            if action in ('submit_proposal','relay_response','perform_assignment'):record.failures=max(0,record.failures-1)
