"""Observador passivo: uma seed nova, decisões do motor, fatos e limites verificáveis."""
import argparse,gzip,json,resource,time
from collections import Counter,defaultdict
from dataclasses import asdict
from pathlib import Path
import procedural
from procedural.engine import Engine
from procedural.generation import generate_world,GenerationConfig
from procedural.persistence import dumps
from procedural.validation import validate_world
from procedural.society import SOCIAL_ACTIONS
from procedural.faith import FAITH_ACTIONS
from experiments.phase41_audit import Audit,core_hash,PLOTS

NEW={'MayorAppointed','OfficeAttended','MilitaryAppointed','ProblemShared','GroupFormed','GroupJoined','GroupMeeting',
     'GroupDissolved','ProposalCreated','ProposalSubmitted','PolicyDecided','PolicyRead','GroupProtested','RoyalAidDecided',
     'FactionFounded','FactionJoined','FactionPromoted','FactionDeserted','FactionReport','FactionContribution',
     'OrganizationalOrder','OrganizationalAction','MilitaryOrder','PrayerOffered','DivineIntervention',
     'SpiritualReport','FaithReinterpreted','CultDefenseDeclared','DivinityKilled','Apotheosis',
     'PowerTrained','DivineChallengeFailed','ExecutionOpportunity','TerminalDecision','IncapacitatedSpared',
     'ViolenceIntentChanged','ItemLegendReported'}

class Phase5Audit(Audit):
    def __init__(self,e,folder):
        self.new_events=Counter();self.lethal_modes=Counter();self.interpretations=[]
        self.shared_faith=defaultdict(set);self.group_arcs={};self.proposal_arcs={};self.last_phase5_trace={}
        self.scope_changes=[];self.last_scope={};self.social_samples=[]
        self.maxima=Counter();self.mythic_ids={p.id for p in e.world.characters.values() if p.mythic_trait}
        super().__init__(e,folder)
        self.social_traces=gzip.open(folder/'decisoes_fase5.jsonl.gz','wt',encoding='utf-8')
    def on_event(self,event):
        super().on_event(event)
        if event.kind not in NEW:return
        self.new_events[event.kind]+=1
        if event.kind not in PLOTS:self.events.write(json.dumps(asdict(event),ensure_ascii=False)+'\n')
        ctx=event.context
        if event.kind=='GroupFormed':
            self.group_arcs[event.target_id]={'formed_at':event.turn,'leader':event.actor_id,'cause':ctx['cause'],
                'source_fact':ctx['source_fact'],'originating_need':ctx['originating_need'],'initial_members':ctx['members'],'events':[asdict(event)]}
        gid=ctx.get('group_id') or (event.target_id if event.kind in ('GroupMeeting','GroupDissolved','GroupJoined') else None)
        if gid in self.group_arcs and len(self.group_arcs[gid]['events'])<40:self.group_arcs[gid]['events'].append(asdict(event))
        pid=event.target_id if event.kind in ('ProposalCreated','PolicyDecided') else ctx.get('proposal_id')
        if pid is not None:
            self.proposal_arcs.setdefault(pid,[]).append(asdict(event))
        if event.kind=='ViolenceIntentChanged' and ctx.get('intent')=='kill':self.lethal_modes[ctx.get('lethal_audit',{}).get('mode','unknown')]+=1
        if event.kind=='SpiritualReport' and event.location:self.shared_faith[ctx['believed_subject']].add(event.location.map_id)
        if event.kind=='DivineIntervention':
            rows=[]
            for i in event.witnesses:
                p=self.w.characters.get(i)
                if p:
                    belief=next((b for b in p.beliefs.values() if b.get('source_fact')==event.id),None)
                    rows.append({'observer':i,'name':p.name,'devotion':p.devotion,'belief':belief})
            self.interpretations.append({'event':asdict(event),'observers':rows})
    def on_execute(self,p,goal,hours):
        need=next((n for n in p.needs.values() if n.id==goal.need_id),None)
        social=goal.action in SOCIAL_ACTIONS|FAITH_ACTIONS|{'finish','spare'} or p.id in self.mythic_ids
        before={'hp':p.health,'money':p.money,'groups':list(p.group_ids),'organizations':list(p.organization_ids),
                'development':p.mythic_development,'religion':p.religion,'position':asdict(p.position)} if social else None
        result=super().on_execute(p,goal,hours)
        if social:
            marker=(goal.action,goal.target_id,result[0]);last=self.last_phase5_trace.get(p.id,(-1000,None))
            if last[1]!=marker or self.w.turn-last[0]>=24:
                c=self.e.agency.current(p,need) if need else None
                self.social_traces.write(json.dumps({'turn':self.w.turn,'actor':p.id,'name':p.name,
                    'need':asdict(need) if need else None,'commitment':asdict(c) if c else None,
                    'action':goal.action,'target':goal.target_id,'score':goal.score,'success':result[0],
                    'outcome':result[1],'before':before,'after':{'hp':p.health,'money':p.money,'groups':p.group_ids,
                    'organizations':p.organization_ids,'development':p.mythic_development,'religion':p.religion,
                    'position':asdict(p.position)}},ensure_ascii=False)+'\n')
                self.last_phase5_trace[p.id]=(self.w.turn,marker)
        return result
    def after_hour(self):
        super().after_hour()
        if self.w.turn%50:return
        self.maxima['groups']=max(self.maxima['groups'],len(self.w.groups))
        self.maxima['proposals']=max(self.maxima['proposals'],len(self.w.proposals))
        self.maxima['factions']=max(self.maxima['factions'],len(self.w.factions))
        self.maxima['divinities']=max(self.maxima['divinities'],len(self.w.divinities))
        self.maxima['group_membership']=max(self.maxima['group_membership'],max(len(p.group_ids) for p in self.w.characters.values()))
        prominent={i for p in self.w.characters.values() for i,r in p.renown.items() if r['epithet']}
        for i in prominent:
            reach=self.e.renown.reach(i)
            if self.last_scope.get(i)!=reach['scope']:
                self.scope_changes.append({'turn':self.w.turn,'subject':i,**reach});self.last_scope[i]=reach['scope']
        row={'turn':self.w.turn,'groups':dict(Counter(g.status for g in self.w.groups.values())),
             'proposals':dict(Counter(p.status for p in self.w.proposals.values())),
             'society':{k:v for k,v in self.w.metrics.items() if k.startswith(('Society:','Faith:','Renown:'))},
             'alive':sum(p.alive for p in self.w.characters.values())}
        self.social_samples.append(row)
        (self.folder/'progresso_fase5.json').write_text(json.dumps(row,ensure_ascii=False))
        self.social_traces.flush()
        print('FASE5 '+json.dumps({'turn':row['turn'],'alive':row['alive'],'groups':row['groups'],'proposals':row['proposals']},ensure_ascii=False),flush=True)
    def finish(self):
        result=super().finish();self.social_traces.close()
        w=self.w;people=list(w.characters.values())
        subjects={i for p in people for i in p.renown}
        reaches={i:self.e.renown.reach(i) for i in subjects}
        result['phase5']={'events':dict(self.new_events),'lethal_modes':dict(self.lethal_modes),
            'groups_final':dict(Counter(g.status for g in w.groups.values())),
            'groups_by_cause_final':dict(Counter(g.cause for g in w.groups.values())),
            'proposal_status_final':dict(Counter(p.status for p in w.proposals.values())),
            'factions_final':dict(Counter(f.status for f in w.factions.values())),
            'ranks_final':dict(Counter(r for t in w.towns.values() for r in t.military_ranks.values())),
            'faith_final':dict(Counter(p.religion or 'sem fé' for p in people if p.alive)),
            'spiritual_report_locations':{i:sorted(v) for i,v in self.shared_faith.items()},
            'interpretations':self.interpretations,'scope_changes':self.scope_changes,
            'reach_distribution':dict(Counter(r['scope'] for r in reaches.values())),
            'reach_by_subject':reaches,
            'believed_divine_mortals':sorted({i for p in people for i,b in p.beliefs.items() if i in w.characters and b.get('believed_divine')}),
            'actual_divine_mortals':sorted(p.id for p in people if p.social_state.get('actual_divinity')),
            'actual_gods':len(w.divinities),'gods_with_confirmed_knowers':sum(any(p.beliefs.get(g.id,{}).get('known_divinity') for p in people) for g in w.divinities.values()),
            'mythic_total':len(self.mythic_ids),'mythic_distribution':dict(Counter(w.characters[i].mythic_trait for i in self.mythic_ids)),
            'mythic_alive':sum(w.characters[i].alive for i in self.mythic_ids),
            'historical_items':sum(bool(i.important_events) for i in w.items.values()),
            'items_with_divine_contact':sum(i.divine_contact is not None for i in w.items.values()),
            'items_with_beliefs':len({i for p in people for i in p.item_beliefs}),
            'epithet_subjects':len({i for p in people for i,r in p.renown.items() if r['epithet']}),
            'maxima':dict(self.maxima),'samples':self.social_samples}
        (self.folder/'arcos_grupos.json').write_text(json.dumps(self.group_arcs,ensure_ascii=False,indent=2))
        (self.folder/'arcos_propostas.json').write_text(json.dumps(self.proposal_arcs,ensure_ascii=False,indent=2))
        (self.folder/'instituicoes.json').write_text(json.dumps({'groups':{i:asdict(g) for i,g in w.groups.items()},
            'proposals':{i:asdict(p) for i,p in w.proposals.items()},'factions':{i:asdict(f) for i,f in w.factions.items()},
            'divinities':{i:asdict(g) for i,g in w.divinities.items()},
            'offices':{t.id:{'mayor':t.mayor_id,'office':t.office,'general':t.general_id,'ranks':t.military_ranks,'policies':t.policies} for t in w.towns.values()},
            'items':{i:asdict(item) for i,item in w.items.items() if item.important_events or item.divine_contact}},ensure_ascii=False,default=asdict))
        (self.folder/'personagens_fase5.json').write_text(json.dumps({p.id:{'name':p.name,'town':p.town_id,'alive':p.alive,
            'profession':p.profession,'personality':asdict(p.personality),'state':{'hp':p.health,'money':p.money,'position':asdict(p.position)},
            'groups':p.group_ids,'organizations':p.organization_ids,'beliefs':p.beliefs,'renown':p.renown,'item_beliefs':p.item_beliefs,
            'mythic':p.mythic_trait,'development':p.mythic_development,'social_state':p.social_state,
            'aspirations':[asdict(a) for a in p.aspirations],'commitments':[asdict(c) for c in p.commitments.values()]}
            for p in people},ensure_ascii=False))
        return result

def run(seed,hours,folder):
    folder=Path(folder);folder.mkdir(parents=True,exist_ok=True)
    if any(folder.iterdir()):raise RuntimeError('Não sobrescrever campanhas anteriores.')
    frozen=core_hash();w=generate_world(seed,with_player=False,config=GenerationConfig(historical_turns=0));e=Engine(w)
    initial={'persistent':len(w.characters),'towns':len(w.towns),'kingdoms':len(w.kingdoms),
             'abstract':sum(t.abstract_population for t in w.towns.values()),'groups':len(w.groups),'factions':len(w.factions),
             'mayors':sum(t.mayor_id is not None for t in w.towns.values()),'generals':sum(t.general_id is not None for t in w.towns.values()),
             'divinities':len(w.divinities),'mythic':sum(p.mythic_trait is not None for p in w.characters.values())}
    manifest={'seed':seed,'hours':hours,'rules':procedural.RULES_VERSION,'core_sha256':frozen,
              'loaded_save':False,'historical_turns':0,'initial':initial}
    (folder/'manifesto.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
    (folder/'personagens_iniciais.json').write_text(json.dumps({p.id:{'name':p.name,'town':p.town_id,
        'profession':p.profession,'mythic':p.mythic_trait,'money':p.money,'personality':asdict(p.personality)} for p in w.characters.values()},ensure_ascii=False))
    (folder/'cidades.json').write_text(json.dumps({t.id:{'name':t.name,'kingdom':t.kingdom_id,'kind':t.kind,'mayor':t.mayor_id} for t in w.towns.values()},ensure_ascii=False))
    initial_metrics=dict(w.metrics);audit=Phase5Audit(e,folder);start=time.monotonic()
    initial_errors=validate_world(w)
    if initial_errors:raise RuntimeError(str(initial_errors[:12]))
    for _ in range(hours):
        audit.alive_hours+=sum(p.alive for p in w.characters.values());e.step();audit.after_hour()
    runtime=time.monotonic()-start
    # Preservar o mundo terminado antes de formatar qualquer relatório secundário.
    save_start=time.monotonic();(folder/'save_final.json').write_text(dumps(w))
    save_seconds=time.monotonic()-save_start
    result=audit.finish();result.update(manifest)
    result.update(runtime_seconds=runtime,alive=sum(p.alive for p in w.characters.values()),
        metrics={k:v-initial_metrics.get(k,0) for k,v in w.metrics.items()},
        death_causes=dict(Counter(d['cause'] for d in w.death_records.values())),death_records=w.death_records,
        history_events=len(w.history),memory_peak_mib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024)
    result['food_carried_deaths']=[{'person':i,**d} for i,d in w.death_records.items() if d['cause'] in ('hunger','both') and d.get('food',0)>0]
    result['final_invariants']=validate_world(w)
    if result['final_invariants']:raise RuntimeError(str(result['final_invariants'][:12]))
    if core_hash()!=frozen:raise RuntimeError('Núcleo alterado durante campanha.')
    (folder/'resumo.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
    result['save_mib']=(folder/'save_final.json').stat().st_size/2**20
    result['save_seconds']=save_seconds
    result['memory_peak_after_save_mib']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024
    (folder/'resumo.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
    print('CONCLUÍDO '+json.dumps({'hours':hours,'deaths':result['death_causes'],'phase5_events':dict(audit.new_events),'save_mib':result['save_mib']},ensure_ascii=False),flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--seed',required=True);p.add_argument('--hours',type=int,required=True);p.add_argument('--output',required=True)
    a=p.parse_args();run(a.seed,a.hours,a.output)
