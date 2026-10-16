"""Campanha observadora Fase 4.6: mede pistas e encadeamento sem ações extras."""
import argparse,json
from collections import Counter,defaultdict
from dataclasses import asdict
import experiments.phase45_audit as base

NEW={'InvestigationClue','InvestigationSearched','InvestigationReply','SearchClueShared',
     'CommitmentDormant','CommitmentReactivated','InstitutionalClueFiled','InstitutionalClueShared',
     'CommitmentPreparation','LethalOptionConsidered','CharacterWarned','CharacterConfronted',
     'ImmediateHelpRequested','ThirdPartyAlerted','LethalIntentAbandoned','CommitmentDeepened'}
base.SOCIAL.update(NEW)

class Audit46(base.SocialAudit):
    def __init__(self,e,folder):
        self.clue_quality=[];self.quality_totals=Counter();self.causal={};self.cycles=[];self.cycle_count=0
        self.lethal_examples=[];self.search_examples=[];self.waiting_actions=Counter();self.waiting_life={};self.response_passivity=Counter()
        super().__init__(e,folder)
    def on_event(self,event):
        super().on_event(event)
        parent=event.context.get('source_fact')
        cid=event.context.get('commitment_id')
        if cid and event.kind in NEW:
            arc=self.commit_arcs.get(cid)
            if arc and event.kind in ('InvestigationClue','SearchClueShared','CommitmentReactivated'):
                arc.setdefault('information_changes',0);arc['information_changes']+=1
        if event.kind=='InvestigationClue':
            clue=event.context['clue'];target=self.w.characters.get(clue['subject_id'])
            location=clue['location']
            actual=None if not target else (abs(target.position.x-location['x'])+abs(target.position.y-location['y']) if target.position.map_id==location['map_id'] else 'other_map')
            self.quality_totals['count']+=1;self.quality_totals['age_sum']+=event.context['age']
            self.quality_totals['confidence_sum']+=clue['confidence'];self.quality_totals['specificity:'+clue['specificity']]+=1
            self.quality_totals['actual_other_map' if actual=='other_map' else 'actual_same_cell' if actual==0 else 'actual_same_map_away']+=1
            if len(self.clue_quality)<4096:self.clue_quality.append({'event':event.id,'turn':event.turn,'actor':event.actor_id,
                'age':event.context['age'],'confidence':clue['confidence'],'specificity':clue['specificity'],'auditor_actual_distance':actual})
        if event.kind in ('LethalOptionConsidered','IncapacitatedSpared') or event.kind=='ViolenceIntentChanged' and event.context.get('intent')=='kill':
            if len(self.lethal_examples)<512:self.lethal_examples.append(asdict(event))
        # Encadeamento por fatos efetivamente usados. Não infere por proximidade temporal.
        if event.kind in ('CharacterAttacked','CharacterKilled','ProtectionGiven','CharacterThreatened','CommitmentCreated','WantedIssued'):
            if parent is not None:
                previous=self.causal.get(parent,[])
                chain=(previous+[{'event':event.id,'kind':event.kind,'actor':event.actor_id,'target':event.target_id,'turn':event.turn}])[-8:]
            else:chain=[{'event':event.id,'kind':event.kind,'actor':event.actor_id,'target':event.target_id,'turn':event.turn}]
            self.causal[event.id]=chain
            violent=[r for r in chain if r['kind'] in ('CharacterAttacked','CharacterKilled')]
            indices=[i for i,r in enumerate(chain) if r['kind'] in ('CharacterAttacked','CharacterKilled')]
            strict=False
            if len(indices)>=2:
                first,last=indices[0],indices[-1]
                involved={chain[first]['actor'],chain[first]['target']}
                middle=chain[first+1:last]
                strict=(last<len(chain)-1 and any(r['actor'] not in involved for r in middle))
            if strict:
                self.cycle_count+=1
                if len(self.cycles)<64:self.cycles.append(chain)
    def on_execute(self,p,goal,hours):
        need=next((n for n in p.needs.values() if n.id==goal.need_id),None)
        commitment=self.e.agency.current(p,need) if need else None
        response=bool(need and need.kind=='response' and commitment)
        before=base.state(self.e,p) if response else None
        waiting=[c.id for c in p.commitments.values() if c.status=='waiting_for_information']
        result=super().on_execute(p,goal,hours)
        if response:
            marker=(goal.action,goal.target_id,result[0]);last=self.last_social_trace.get(p.id,(-1000,None))
            if last[1]!=marker or self.w.turn-last[0]>=24:
                self.social_traces.write(json.dumps({'turn':self.w.turn,'owner':p.id,'name':p.name,
                    'need':asdict(need),'commitment':asdict(commitment),'action':goal.action,'target':goal.target_id,
                    'success':result[0],'outcome':result[1],'before':before,'after':base.state(self.e,p)},ensure_ascii=False)+'\n')
                self.last_social_trace[p.id]=(self.w.turn,marker)
        if waiting and result[0]:
            self.waiting_actions[goal.action]+=1
            for cid in waiting:
                row=self.waiting_life.setdefault(cid,{'owner':p.id,'first':self.w.turn,'last':self.w.turn,'actions':{}})
                row['last']=self.w.turn;row['actions'][goal.action]=row['actions'].get(goal.action,0)+1
        return result

    def after_hour(self):
        super().after_hour()
        if self.w.turn%24:return
        for p in self.w.characters.values():
            if not p.alive:continue
            for c in p.commitments.values():
                g=p.grievances.get(c.target_id)
                if c.motivation!='response' or not g or g.intensity<60 or p.personality.vengefulness<65 or p.personality.compassion>35:continue
                if c.status=='waiting_for_information':reason='waiting_for_information'
                elif c.status not in ('active','paused'):continue
                elif c.target_id not in self.e.spatial.at(p.position):reason='distance_or_lead'
                elif p.health<=12:reason='actor_incapacity'
                elif p.combat.truces.get(c.target_id,0)>self.w.turn:reason='truce'
                elif p.goal and p.goal.need_id!=c.originating_need:reason='other_need'
                elif p.goal and p.goal.action=='attack':reason='attack_selected'
                else:reason='utility_or_semantic_barrier'
                self.response_passivity[reason]+=1

    def finish(self):
        result=super().finish()
        result['phase46']={'metrics':{k:v for k,v in self.w.metrics.items() if k.startswith(('Lethal:','Investigation:'))},
            'clue_quality_sample':self.clue_quality,'clue_quality_totals':dict(self.quality_totals),'causal_chain_occurrences':self.cycle_count,'causal_chains':self.cycles,
            'lethal_examples':self.lethal_examples,'waiting_actions':dict(self.waiting_actions),'strong_response_daily_samples':dict(self.response_passivity),
            'sleeping_at_end':sum(c.status=='waiting_for_information' for p in self.w.characters.values() for c in p.commitments.values()),
            'compact_state_bytes':len(json.dumps({p.id:{'conflict':p.combat.conflict_history,
                'search':[asdict(c) for c in p.commitments.values() if c.context.get('investigation')]}
                for p in self.w.characters.values()},ensure_ascii=False,default=lambda v:asdict(v)).encode())}
        (self.folder/'vida_durante_espera.json').write_text(json.dumps(self.waiting_life,ensure_ascii=False))
        (self.folder/'evidencias_fase46.json').write_text(json.dumps(result['phase46'],ensure_ascii=False,indent=2))
        return result

base.SocialAudit=Audit46
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--seed',default='Corven-46');p.add_argument('--hours',type=int,required=True);p.add_argument('--output',required=True)
    args=p.parse_args();base.run(args.seed,args.hours,args.output)
