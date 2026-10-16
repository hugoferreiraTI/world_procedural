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
        # Memória própria de dano atribuído com confiança suficiente. A suspeita
        # pode alimentar desejo, mas não comprova dano grave para ActionPressure.
        if (f.kind=='CharacterAttacked' and f.target_id==p.id and f.confidence>=60
                and f.event_id>h.get('last_confirmed_injury_fact',-1)):
            h['last_confirmed_injury_fact']=f.event_id
            h['confirmed_injury_received']=min(100,h.get('confirmed_injury_received',0)+f.context.get('damage',0))
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
        return bool(g and g.intensity>=30 and
                    (h.get('hostile_episodes',0)>=2 and h.get('injury_received',0)>=10 or
                     h.get('injury_received',0)>=10))

    def evaluate(self,p,target,n,audit=False):
        result=self.e.lethal_decisions.evaluate(p,target,n)
        if audit:
            self.count('evaluated');self.count('available' if result['available'] else 'precondition_failed')
            for reason in result['blocking']:self.count('blocked:'+reason)
        return result
