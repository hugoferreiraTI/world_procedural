"""Uma campanha nova; métricas narrativas e fisiologia observadas sem decisões extras."""
import argparse, gzip, hashlib, json, resource, time
from collections import Counter,defaultdict
from dataclasses import asdict
from pathlib import Path
import procedural
from procedural.engine import Engine
from procedural.generation import generate_world,GenerationConfig
from procedural.persistence import dumps
from experiments.phase41_audit import Audit,core_hash,state,PLOTS

SOCIAL={'CommitmentCreated','CommitmentCompleted','CommitmentAbandoned','CommitmentExpired',
 'CommitmentPaused','CommitmentResumed','CommitmentProgress','CommitmentStrategyChanged',
 'CommitmentRetargeted','CommitmentInformation','CommitmentTravel','AspirationAdopted',
 'AspirationSatisfied','AspirationAbandoned','ViolenceIntentChanged','CharacterIncapacitated',
 'IncapacitatedSpared','InstitutionalCaseShared','AgencyDiagnostic','PursuitSearch',
 'SuspectLocated','InvestigationPerformed','ThreatReported','InformationShared','ConflictForgiven',
 'WantedIssued','ConflictStarted','ConflictEnded','ResponsibilityFulfilled','FamilyConcern',
 'AbsenceNoticed','PersonLocated','Remembrance','ThreatAvoided','TrainingAbandoned','ApologyGiven',
 'CharacterThreatened','CharacterInsulted','RestitutionDemanded','CalmingAttempted'}

class SocialAudit(Audit):
    def __init__(self,e,folder):
        self.intent=Counter();self.commit_arcs={};self.impacts=Counter();self.last_social_trace={}
        self.passivity=Counter();self.passivity_examples=[]
        super().__init__(e,folder)
        self.social_traces=gzip.open(folder/'decisoes_sociais.jsonl.gz','wt',encoding='utf-8')

    def on_event(self,event):
        super().on_event(event)
        if event.kind in SOCIAL and event.kind not in PLOTS:
            self.events.write(json.dumps(asdict(event),ensure_ascii=False)+'\n')
        cid=event.context.get('commitment_id')
        if cid:
            arc=self.commit_arcs.setdefault(cid,{'owner':event.actor_id,'created_at':event.turn,
                'origin':event.context.get('origin'),'source_fact':event.context.get('source_fact'),
                'target':event.context.get('target'),'transitions':[],'event_ids':[]})
            arc['event_ids'].append(event.id)
            if event.kind not in ('CommitmentPaused','CommitmentResumed'):
                arc['transitions'].append({'id':event.id,'turn':event.turn,'kind':event.kind,'context':event.context})
            if event.kind in ('CommitmentCompleted','CommitmentAbandoned','CommitmentExpired'):
                arc['ended_at']=event.turn;arc['ending']=event.kind
        if event.kind=='ViolenceIntentChanged':self.intent[event.context['intent']]+=1
        if event.kind in ('CharacterKilled','CharacterCaptured','HelpGiven','ProtectionGiven','ResidentMoved',
                          'ProfessionChanged','InformationShared','ThreatReported','FirstAidGiven'):
            self.impacts[event.kind]+=1

    def on_execute(self,p,goal,hours):
        n=next((n for n in p.needs.values() if n.id==goal.need_id),None)
        before=state(self.e,p);profile=dict(n.context.get('agency',{})) if n else {}
        social=n and n.kind in ('revenge','protection','pursuit','advancement','status','grief','family','migration')
        need_before={k:getattr(n,k) for k in ('id','kind','priority','status','source','reason','target_id')} if social else None
        emotions_before=asdict(p.emotions) if social else None
        if social:before.update(money=p.money,fatigue=p.fatigue)
        c=self.e.agency.current(p,n) if n else None
        progress=c.meaningful_progress if c else 0
        result=super().on_execute(p,goal,hours)
        marker=(goal.action,goal.target_id,result[0]);last=self.last_social_trace.get(p.id,(-1000,None))
        if social and (
                last[1]!=marker or self.w.turn-last[0]>=24 or c and c.meaningful_progress>progress):
            self.social_traces.write(json.dumps({'turn':self.w.turn,'owner':p.id,'name':p.name,
                'need':asdict(n),'commitment':asdict(c) if c else None,'impulse':profile,
                'action':goal.action,'target':goal.target_id,'success':result[0],'outcome':result[1],
                'before':before,'after':{**state(self.e,p),'money':p.money,'fatigue':p.fatigue},
                'need_before':need_before,'emotions_before':emotions_before,'emotions_after':asdict(p.emotions),
                'solution_score':goal.score},ensure_ascii=False)+'\n')
            self.last_social_trace[p.id]=(self.w.turn,marker)
        return result

    def after_hour(self):
        super().after_hour()
        if self.w.turn%24:return
        for p in self.w.characters.values():
            if not p.alive:continue
            for c in p.commitments.values():
                n=next((n for n in p.needs.values() if n.id==c.originating_need),None)
                grievance=p.grievances.get(c.target_id)
                if (c.status not in ('active','paused') or c.motivation!='revenge' or not n or
                        not grievance or grievance.intensity<60 or p.personality.vengefulness<65 or
                        p.personality.compassion>35):continue
                observed=p.observations.get(c.target_id)
                if not observed:reason='unknown_location'
                elif c.target_id not in self.e.spatial.at(p.position):reason='distance_or_stale_lead'
                elif p.health<=12:reason='incapacity'
                elif p.combat.truces.get(c.target_id,0)>self.w.turn:reason='truce'
                elif p.goal and p.goal.need_id!=n.id:reason='other_need'
                elif p.goal and p.goal.action=='attack':reason='attack_selected'
                else:
                    names={a for a,d,t in self.e.conflicts.candidates(p,n)}
                    reason='solution_absent' if 'attack' not in names else 'utility_or_known_risk'
                self.passivity[reason]+=1
                if len(self.passivity_examples)<128:self.passivity_examples.append({'turn':self.w.turn,'owner':p.id,
                    'commitment':c.id,'target':c.target_id,'reason':reason,'goal':p.goal.action if p.goal else None,
                    'grievance':grievance.intensity,'profile':n.context.get('agency',{})})
        self.social_traces.flush()

    def finish(self):
        result=super().finish();self.social_traces.close()
        for p in self.w.characters.values():
            for c in p.commitments.values():
                arc=self.commit_arcs.get(c.id)
                if arc:arc['final']=asdict(c)
        arcs=list(self.commit_arcs.values())
        result['agency']={'violence_intent_transitions':dict(self.intent),'impact_events':dict(self.impacts),
          'commitments_by_origin':dict(Counter(a['origin'] for a in arcs)),
          'commitments_total':len(arcs),'completed':sum(a.get('ending')=='CommitmentCompleted' for a in arcs),
          'abandoned':sum(a.get('ending')=='CommitmentAbandoned' for a in arcs),
          'expired':sum(a.get('ending')=='CommitmentExpired' for a in arcs),
          'duration_mean':sum(a.get('ended_at',self.w.turn)-a['created_at'] for a in arcs)/max(1,len(arcs)),
          'arcs_with_progress':sum(any(t['kind']=='CommitmentProgress' for t in a['transitions']) for a in arcs),
          'arcs_with_strategy_change':sum(any(t['kind']=='CommitmentStrategyChanged' for t in a['transitions']) for a in arcs),
          'arcs_with_three_distinct_causal_transitions':sum(len({t['kind'] for t in a['transitions']}-{'CommitmentCreated'})>=3 for a in arcs),
          'maximum_commitments_per_character':max(len(p.commitments) for p in self.w.characters.values()),
          'principal_aspirations':dict(Counter(p.aspirations[0].domain for p in self.w.characters.values() if p.aspirations)),
          'institutional_cases':sum(r.institutional_fact is not None for r in self.w.wanted_records.values()),
          'multi_guard_cases':sum(len(r.assignments)>1 for r in self.w.wanted_records.values()),
          'maximum_case_assignments':max((len(r.assignments) for r in self.w.wanted_records.values()),default=0),
          'strong_revenge_daily_samples':dict(self.passivity),'strong_revenge_examples':self.passivity_examples}
        (self.folder/'arcos.json').write_text(json.dumps(self.commit_arcs,ensure_ascii=False))
        return result

def run(seed,hours,folder):
    folder=Path(folder);folder.mkdir(parents=True,exist_ok=True)
    if any(folder.iterdir()):raise RuntimeError('Não sobrescrever auditoria anterior.')
    frozen=core_hash();w=generate_world(seed,with_player=False,config=GenerationConfig(historical_turns=0));e=Engine(w)
    initial={'persistent':len(w.characters),'towns':len(w.towns),'kingdoms':len(w.kingdoms),'abstract':sum(t.abstract_population for t in w.towns.values())}
    initial_people={i:{'name':p.name,'profession':p.profession,'town':p.town_id,'money':p.money,
                       'personality':asdict(p.personality)} for i,p in w.characters.items()}
    (folder/'personagens_iniciais.json').write_text(json.dumps(initial_people,ensure_ascii=False))
    initial_metrics=dict(w.metrics);audit=SocialAudit(e,folder);start=time.monotonic()
    manifesto={'seed':seed,'hours':hours,'rules':procedural.RULES_VERSION,'core_sha256':frozen,
               'loaded_save':False,'historical_turns':0,'initial':initial}
    (folder/'manifesto.json').write_text(json.dumps(manifesto,ensure_ascii=False,indent=2))
    for _ in range(hours):
        audit.alive_hours+=sum(p.alive for p in w.characters.values());e.step();audit.after_hour()
    summary=audit.finish();summary.update(manifesto)
    summary.update(runtime_seconds=time.monotonic()-start,alive=sum(p.alive for p in w.characters.values()),
        metrics={k:v-initial_metrics.get(k,0) for k,v in w.metrics.items()},
        death_causes=dict(Counter(d['cause'] for d in w.death_records.values())),death_records=w.death_records,
        history_events=len(w.history),memory_peak_mib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024)
    if core_hash()!=frozen:raise RuntimeError('Núcleo alterado durante auditoria.')
    summary['food_carried_deaths']=[{'person':i,**d} for i,d in w.death_records.items() if d['cause'] in ('hunger','both') and d.get('food',0)>0]
    (folder/'personagens.json').write_text(json.dumps({i:{'name':p.name,'alive':p.alive,'profession':p.profession,
        'town':p.town_id,'initial_personality':initial_people.get(i,{}).get('personality'),'personality':asdict(p.personality),'state':state(e,p),
        'aspirations':[asdict(a) for a in p.aspirations],'commitments':[asdict(c) for c in p.commitments.values()]} for i,p in w.characters.items()},ensure_ascii=False))
    (folder/'casos_institucionais.json').write_text(json.dumps({i:asdict(r) for i,r in w.wanted_records.items()},ensure_ascii=False))
    (folder/'resumo.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2))
    (folder/'save_final.json').write_text(dumps(w))
    print('CONCLUÍDO '+json.dumps({'hours':hours,'deaths':summary['death_causes'],'agency':summary['agency']},ensure_ascii=False),flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--seed',default='Vespera-47');p.add_argument('--hours',type=int,required=True);p.add_argument('--output',required=True)
    a=p.parse_args();run(a.seed,a.hours,a.output)
