"""Incapacidade muda o contexto; não refaz a barreira de entrada da decisão."""
from .rules import INTERACTION

class TerminalCombat:
    def __init__(self,e):self.e,self.w=e,e.world
    def situational(self,p,target,n):
        return self.e.lethal_decisions.evaluate(p,target,n)
    def opportunity(self,p,target):
        return bool(p.alive and p.health>12 and p.combat.detention_until<=self.w.turn and
                    p.combat.surrendered_until<=self.w.turn and target.alive and target.position==p.position and
                    target.health<=INTERACTION.incapacity_health and self.e.lethal_decisions.active(p,target.id))
    def refresh(self,p):
        for i,d in p.lethal_decisions.items():
            q=self.w.characters.get(i)
            if d.status!='active' or not q or not self.opportunity(p,q):continue
            p.combat.pending_judgments[i]=self.w.turn+6
            if d.context.get('terminal_episode')!=q.combat.last_active:
                d.context['terminal_episode']=q.combat.last_active
                self.e.recorder.emit('ExecutionOpportunity',f'{p.name} pode decidir o desfecho diante de {q.name}.',p.id,q.id,p.position,
                    historical=True,context={'decision_id':d.id,'expires_at':self.w.turn+6,'violence_intent':'kill'})
    def execute(self,p,target,n):
        if not target or not self.opportunity(p,target):return False,'Não existe oportunidade terminal válida.'
        terminal=self.e.lethal_decisions.terminal(p,target)
        action_audit=self.e.lethal_decisions.action_audit(p,target.id,n,terminal=True)
        if not action_audit['eligible']:return False,'A mudança de contexto favorece parar ou falta capacidade.'
        audit=self.e.lethal_decisions.evaluate(p,target,n)
        self.e.recorder.emit('TerminalDecision',f'{p.name} escolheu finalizar o confronto.',p.id,target.id,p.position,
            historical=True,context={'decision':'finish','terminal_context':terminal,'lethal_audit':audit,'action_audit':action_audit})
        self.w.metrics['TerminalDecisionFinish']=self.w.metrics.get('TerminalDecisionFinish',0)+1
        weapon=self.e.conflicts.weapon(p)
        self.e.finish_death(target,'combat',p,weapon.id if weapon else None,
            {'death_context':'deliberate_finish','violence_intent':'kill','post_incapacity':True,
             'lethal_audit':audit,'action_audit':action_audit,'terminal_context':terminal,
             'source_fact':audit.get('source_fact'),'actor_groups':list(p.group_ids)})
        self.e.lethality.count('death');self.e.lethality.count('finish')
        self.e.conflicts.end(target,'deliberate_finish',p)
        return True,'Desfecho fatal deliberado executado, sem nova rolagem de dano.'
