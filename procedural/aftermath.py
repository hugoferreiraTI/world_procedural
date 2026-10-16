"""Avaliação do próprio matador e aprendizagem compacta, sem diagnóstico clínico."""
from .lethal_decisions import clamp

class AftermathSystem:
    def __init__(self,e):
        self.e,self.w=e,e.world;e.bus.subscribe('CharacterKilled',self.on_kill)
    def on_kill(self,event):
        p=self.w.characters.get(event.actor_id);victim=self.w.characters.get(event.target_id)
        if not p or not victim:return
        s=p.death_state
        if event.id in s.get('kill_facts',[]):return
        intentional=event.context.get('violence_intent')=='kill'
        d=p.lethal_decisions.get(victim.id)
        mode=d.mode if d else 'unintended';traits=p.personality
        bond=self.e.needs.personal.relationship(p,victim.id)[0]
        justified=event.context.get('self_defense') or event.context.get('lawful') or mode in ('reactive_threat','protective','moral_punishment')
        vulnerable=event.context.get('post_incapacity',False)
        moral_conflict=clamp(traits.compassion*.7+traits.honesty*.25+bond*.5-(40 if justified else 0)-(traits.sadism*.3 if intentional else 0))
        guilt=clamp(moral_conflict*(1.2 if vulnerable else .9))
        witnesses=len([i for i in event.witnesses if i not in (p.id,victim.id)])
        feelings={'guilt':guilt,'shame':clamp(guilt*.6+min(15,witnesses*3)),
            'fear':clamp(witnesses*(100-traits.courage)*.08+(10 if not justified else 0)),
            'relief':70 if mode=='reactive_threat' else 55 if mode in ('protective','retributive') else 15,
            'pride':clamp((traits.honesty*.5 if justified else traits.vengefulness*.25)-guilt*.3),
            'pleasure':clamp((traits.sadism-35)*.8+p.death_affinity*.25-guilt*.5) if intentional else 0,
            'fascination':clamp(traits.sadism*.5+p.death_affinity*.2-guilt*.6) if intentional else 0,
            'numbness':min(70,s.get('kills',0)*8),'grief':clamp(bond*.8),
            'moral_conflict':moral_conflict}
        # Fé atua por valores percebidos pelo mortal, não pela verdade onisciente.
        approval=0
        for subject,b in p.beliefs.items():
            god=self.w.divinities.get(subject)
            if not god or not b.get('believed_divine') or b.get('confidence',0)<30:continue
            if god.domain=='death' and god.values.get('rewards_intentional_killing',False) and intentional:
                approval=max(approval,p.devotion*.15)
            if god.domain in ('justice','protection') and not justified:guilt=clamp(guilt+p.devotion*.1)
        feelings['guilt']=guilt;feelings['pride']=clamp(feelings['pride']+approval)
        old=p.death_affinity
        positive=intentional and max(feelings['pleasure'],feelings['fascination'])>=25 and guilt<35
        gain=(8+traits.sadism*.12+approval*.3) if positive else 0
        p.death_affinity=clamp(old+gain-guilt*.14-feelings['grief']*.05)
        s.update(kills=s.get('kills',0)+1,intentional_kills=s.get('intentional_kills',0)+int(intentional),
            positive_kills=s.get('positive_kills',0)+int(positive),guilt=guilt,last_kill=self.w.turn,last_decay=self.w.turn)
        facts=s.setdefault('kill_facts',[]);facts.append(event.id);del facts[:-8]
        row={'death_fact':event.id,'victim':victim.id,'turn':self.w.turn,'intentional':intentional,
             'mode':mode,'feelings':feelings,'death_affinity_before':old,'death_affinity_after':p.death_affinity,
             'justified_by_actor':bool(justified),'victim_vulnerable':bool(vulnerable),'bond':bond,
             'decision_id':d.id if d else None}
        history=s.setdefault('appraisals',[]);history.append(row);del history[:-4]
        self.w.death_records[victim.id]['death_context']=event.context.get('death_context','unintended_combat_death')
        self.w.death_records[victim.id]['post_kill_appraisal']=row
        self.e.recorder.emit('PostKillAppraisal',f'{p.name} avaliou a morte que causou.',p.id,
            location=p.position,witnesses=[p.id],historical=True,context=row,parent_event_ids=[event.id])
        if p.death_affinity>old:
            self.e.recorder.emit('DeathAffinityIncrease',f'{p.name} consolidou afinidade com a morte.',p.id,
                location=p.position,witnesses=[p.id],historical=True,context={'before':old,'value':p.death_affinity,'source_fact':event.id})
        if guilt>=50 and p.beliefs:
            subject=max(p.beliefs,key=lambda i:p.beliefs[i].get('confidence',0))
            n=self.e.needs.ensure(p,'religious_interest',min(80,35+guilt*.4),'post_kill_conflict','Buscar sentido para uma morte causada',subject)
            n.context.update(source_event=event.id,post_kill_conflict=True)
    def on_fact(self,p,f):
        s=p.death_state
        if not s:return
        negative=f.kind in ('CharacterCaptured','WantedIssued','ConflictForgiven','FaithReinterpreted') and (
            f.target_id==p.id or f.actor_id==p.id or f.context.get('suspect_id')==p.id)
        positive=f.kind in ('DivineIntervention','GroupMeeting') and f.target_id==p.id and f.context.get('approves_killing')
        if not (negative or positive) or f.confidence<60:return
        seen=s.setdefault('feedback_facts',[])
        if f.event_id in seen:return
        seen.append(f.event_id);del seen[:-8]
        p.death_affinity=clamp(p.death_affinity+4 if positive else p.death_affinity-8)
        if negative:s['guilt']=clamp(s.get('guilt',0)+8)
    def refresh(self,p):
        s=p.death_state
        if not s:return
        elapsed=self.w.turn-s.get('last_decay',self.w.turn)
        if elapsed<24:return
        s['last_decay']=self.w.turn
        if self.w.turn-s.get('last_kill',0)>168:
            p.death_affinity=clamp(p.death_affinity-elapsed*(.005+s.get('guilt',0)/10000))
