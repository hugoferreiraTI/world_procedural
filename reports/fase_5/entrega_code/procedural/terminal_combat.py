"""Oportunidade terminal é observável; intenção e decisão não são execução."""
from .rules import INTERACTION

class TerminalCombat:
    def __init__(self,e):self.e,self.w=e,e.world
    def situational(self,p,target,n):
        facts=[f for f in p.knowledge.values() if f.kind=='CharacterAttacked' and f.actor_id==target.id
               and f.target_id==p.id and f.confidence>=60 and self.w.turn-f.turn<=3]
        damage=sum(f.context.get('damage',0) for f in facts)
        t=self.e.conflicts.terms(p,target.id)
        danger=bool(facts and (p.health<40 or damage>=15))
        pressure=((35 if danger else 0)+damage*.5+p.emotions.anger*.25+p.personality.courage*.2+
                  (15 if p.mythic_trait=='Coldness' else 0)-p.personality.compassion*.6-p.personality.honesty*.1-t['bond']*30)
        blocking=[]
        if not danger:blocking.append('no_immediate_extreme_threat')
        if p.health<=12 or p.combat.detention_until>self.w.turn:blocking.append('actor_incapacity')
        if target.id not in self.e.spatial.at(p.position):blocking.append('target_absent')
        if p.personality.compassion>=90:blocking.append('compassion')
        if t['fear']>.8 and p.personality.courage<40:blocking.append('fear')
        pressure-=t['fear']*(20+(100-p.personality.courage)*.1)+t['authority']*20
        if pressure<45:blocking.append('insufficient_pressure')
        return {'available':not blocking,'pressure':round(pressure,2),'mode':'situational','confidence':max((f.confidence for f in facts),default=0),
                'known_facts':[f.event_id for f in facts][-3:],'source_fact':facts[-1].event_id if facts else None,
                'commitment_id':None,'motive':'immediate_self_defense','blocking':blocking,
                'barriers':{'compassion':p.personality.compassion*.6,'bond':t['bond']*30,
                    'fear':t['fear']*(20+(100-p.personality.courage)*.1),'authority_or_witnesses':t['authority']*20},
                'positive_factors':{'danger':35 if danger else 0,'recent_damage':damage*.5},'grave_basis':'immediate_threat'}
    def opportunity(self,p,target):
        return bool(p.alive and p.health>12 and p.combat.detention_until<=self.w.turn and
                    p.combat.surrendered_until<=self.w.turn and target.alive and target.position==p.position and
                    target.health<=INTERACTION.incapacity_health and p.combat.violence_intents.get(target.id)=='kill' and
                    p.combat.pending_judgments.get(target.id,-1)>self.w.turn)
    def refresh(self,p):
        for i,intent in list(p.combat.violence_intents.items()):
            q=self.w.characters.get(i)
            if intent!='kill' or not q or not q.alive or q.position!=p.position or q.health>12 or p.health<=12:continue
            if p.combat.pending_judgments.get(i,-1)<=self.w.turn:
                # Não restaura uma oportunidade expirada sem nova hostilidade.
                if self.w.turn-p.combat.last_active>3:continue
                p.combat.pending_judgments[i]=self.w.turn+6
                self.e.recorder.emit('ExecutionOpportunity',f'{p.name} pode decidir o desfecho diante de {q.name}.',p.id,q.id,p.position,
                    historical=True,context={'expires_at':self.w.turn+6,'violence_intent':'kill'})
    def execute(self,p,target,n):
        if not target or not self.opportunity(p,target):return False,'Não existe oportunidade terminal válida.'
        audit=self.e.lethality.evaluate(p,target,n)
        if not audit['available']:return False,'A reavaliação não sustenta intenção letal.'
        self.e.recorder.emit('TerminalDecision',f'{p.name} escolheu finalizar o confronto.',p.id,target.id,p.position,
            historical=True,context={'decision':'finish','lethal_audit':audit})
        weapon=self.e.conflicts.weapon(p)
        self.e.finish_death(target,'combat',p,weapon.id if weapon else None,
            {'death_context':'deliberate_finish','violence_intent':'kill','post_incapacity':True,
             'lethal_audit':audit,'source_fact':audit.get('source_fact'),'actor_groups':list(p.group_ids)})
        self.e.lethality.count('death');self.e.lethality.count('finish')
        self.e.conflicts.end(target,'deliberate_finish',p)
        return True,'Desfecho fatal deliberado executado, sem nova rolagem de dano.'
