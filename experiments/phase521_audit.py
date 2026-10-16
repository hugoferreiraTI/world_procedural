"""Uma campanha nova de 1000h: evidência terminal compacta e um único save."""
import argparse,hashlib,json,resource,time
from collections import Counter,defaultdict
from dataclasses import asdict
from pathlib import Path
from procedural import RULES_VERSION
from procedural.engine import Engine
from procedural.generation import generate_world,GenerationConfig
from procedural.persistence import dumps
from procedural.validation import validate_world
from experiments.phase41_audit import core_hash
from experiments.phase52_audit import Audit52,STORY,IMPORTANT

HOURS=1000
STORY521=STORY|{'LethalDecisionUpdated','DivineMessage','CharacterIncapacitated','GlobalFaithHealthChanged'}
TERMINAL={'finish','spare','capture','help','withdraw'}

def write(path,data):path.write_text(json.dumps(data,ensure_ascii=False,indent=2))
def ages(decisions,turn):
    result=dict.fromkeys(('<24h','24–72h','72–168h','>168h'),0)
    for d in decisions:
        age=turn-d.created_at
        result['<24h' if age<24 else '24–72h' if age<=72 else '72–168h' if age<=168 else '>168h']+=1
    return result

class Audit521(Audit52):
    def __init__(self,e):
        self.original={};self.opportunities=[];self.pending={};self.closures=[];self.terminal=[]
        self.snapshots=[];self.first_relevant=None;self.structural_errors=[];self.output_folder=None
        super().__init__(e)
    def person(self,p):
        return super().person(p)|{'category':p.category,'position':asdict(p.position),
            'development':p.mythic_development,'profile':{k:getattr(p.personality,k) for k in
                ('compassion','honesty','courage','vengefulness','persistence','sadism')}}
    def event(self,ev):
        super().event(ev);c=ev.context
        if ev.kind in STORY521-STORY:
            for p in (ev.actor_id,ev.target_id,c.get('target_id'),c.get('mortal'),c.get('actor'),c.get('subject')):
                if p in self.w.characters:self.by_person[p].append(ev.id)
        if ev.historical and self.first_relevant is None and ev.kind in ('GroupFormed','ConflictStarted','CharacterKilled','ProposalSubmitted'):
            self.first_relevant=asdict(ev)
        if ev.kind=='LethalDecision':
            d=c['decision'];self.original[d['id']]={k:d[k] for k in ('id','actor_id','target_id','mode','cause','facts','created_at','intensity','world_pressure','rumination')}
        if ev.kind=='ExecutionOpportunity':
            p=self.w.characters[ev.actor_id];q=self.w.characters[ev.target_id];d=self.e.lethal_decisions.active(p,q.id)
            if not d:
                self.violations.append({'event':ev.id,'cause':'opportunity_without_active_decision'});return
            row={'event_id':ev.id,'hour':ev.turn,'actor':p.id,'target':q.id,'decision_id':d.id,
                'original':self.original.get(d.id),'context':self.e.lethal_decisions.terminal(p,q),
                'actor_present':p.position==q.position,'actor_capable':self.e.lethal_decisions.action_audit(p,q.id)['eligible'],
                'target_incapacitated':q.health<=15,'location':asdict(p.position),
                'chosen':None,'terminal_event':None}
            self.opportunities.append(row);self.pending[p.id,q.id,d.id]=len(self.opportunities)-1
        if ev.kind=='TerminalDecision':
            t=c.get('terminal_context',{});row={'event_id':ev.id,'hour':ev.turn,'actor':ev.actor_id,'target':ev.target_id,
                'choice':c['decision'],'executed':c.get('executed',True),'context':t}
            self.terminal.append(row)
            index=self.pending.get((ev.actor_id,ev.target_id,t.get('decision_id')))
            if index is not None:self.opportunities[index].update(chosen=c['decision'],terminal_event=ev.id,chosen_at=ev.turn,executed=row['executed'])
            if t.get('choice')!=c['decision']:self.violations.append({'event':ev.id,'cause':'terminal_winner_changed','preferred':t.get('choice'),'actual':c['decision']})
        if ev.kind in ('LethalDecisionAbandoned','LethalDecisionResolved'):
            original=self.original.get(c['decision_id'],{})
            self.closures.append({'event_id':ev.id,'hour':ev.turn,'actor':ev.actor_id,'target':c.get('target_id'),
                'decision_id':c['decision_id'],'status':'resolved' if ev.kind.endswith('Resolved') else 'abandoned',
                'reason':c['reason'],'age':ev.turn-original.get('created_at',ev.turn),'source_facts':list(c.get('source_facts',[]))})
    def religion(self,include_ids=False):
        composition=self.e.religious_health.composition();sets={g.id:set() for g in self.w.divinities.values()}
        for p in self.w.characters.values():
            if not p.alive:continue
            for g in self.w.divinities.values():
                a=p.social_state.get('religious_activity',{}).get(g.id,{})
                if a.get('acts',0)>0 and self.w.turn-a.get('last_actor',-1000)<=200:sets[g.id].add(p.id)
        rows={}
        for g in self.w.divinities.values():
            counts={key:sum(r.get(key,0) for r in composition[g.id].values()) for key in ('followers','devoted','cultists','actors','favorites')}
            others=set().union(*(s for id,s in sets.items() if id!=g.id))
            rows[g.id]={'name':g.name,'domain':g.domain,**counts,'exclusive_actors':len(sets[g.id]-others),
                'shared_actors':{id:len(sets[g.id]&s) for id,s in sets.items() if id!=g.id}}
            if include_ids:rows[g.id]['actor_ids']=sorted(sets[g.id])
        return {'gods':rows,'unique_actors_total':len(set().union(*sets.values()))}
    def check(self):
        errors=validate_world(self.w)
        if errors:
            self.structural_errors.extend(errors);raise RuntimeError(str(errors[:4]))
        # Reconciliação histórica: listas devem conservar o instante original.
        for ev in self.w.history:
            if ev.kind not in ('CharacterAttacked','CharacterKilled','LethalConsideration'):continue
            refs=set(ev.context.get('action_audit',{}).get('source_facts',[]))
            refs.update(ev.context.get('lethal_audit',{}).get('known_facts',[]))
            if any(f>ev.id for f in refs):
                violation={'event':ev.id,'kind':ev.kind,'hour':ev.turn,'actor':ev.actor_id,'target':ev.target_id,
                           'cause':'future_fact_in_history','references':sorted(refs)}
                if not any(v.get('event')==ev.id and v.get('cause')==violation['cause'] for v in self.violations):self.violations.append(violation)
        active=[d for p in self.w.characters.values() if p.alive for d in p.lethal_decisions.values() if d.status=='active']
        for p in self.w.characters.values():
            if not p.alive:continue
            for d in p.lethal_decisions.values():
                if d.status=='active' and any(f.target_id==d.target_id and f.kind in ('CharacterDied','CharacterKilled','RemainsLocated') and f.confidence>=60 for f in p.knowledge.values()):
                    v={'actor':p.id,'decision':d.id,'cause':'active_despite_known_target_death'}
                    if v not in self.violations:self.violations.append(v)
        self.checks.append(self.w.turn)
        snapshot={'hour':self.w.turn,'alive':sum(p.alive for p in self.w.characters.values()),'active_decisions':len(active),
            'ages':ages(active,self.w.turn),'religion':self.religion(),'decisions':self.counts['LethalDecision'],
            'lethal_attacks':self.w.metrics.get('LethalAttack',0),'opportunities':self.counts['ExecutionOpportunity'],
            'terminal_choices':dict(Counter(t['choice'] for t in self.terminal)),
            'deliberate_deaths':self.w.metrics.get('IntentionalCombatKill',0)+self.w.metrics.get('DeliberateFinish',0),
            'causal_violations':len(self.violations)}
        self.snapshots.append(snapshot)
        if self.output_folder:
            write(self.output_folder/'checkpoint_resumo.json',{'latest':snapshot,'snapshots':self.snapshots,
                'causal_violations':self.violations,'structural_errors':self.structural_errors})
        print(json.dumps({k:v for k,v in snapshot.items() if k!='religion'},ensure_ascii=False),flush=True)
    def material(self):
        lookup={ev.id:ev for ev in self.w.history};scores={}
        for id,refs in self.by_person.items():
            kinds=Counter(lookup[r].kind for r in refs if r in lookup)
            scores[id]=sum(min(v,3)*(10 if k in IMPORTANT else 1) for k,v in kinds.items())+len(kinds)*2
        chosen=[]
        def pick(ids):
            ids=set(ids)-set(chosen)
            if ids:chosen.append(max(ids,key=lambda id:(scores.get(id,0),-id)))
        pick(t['actor'] for t in self.terminal if t['choice']=='finish' and t['executed'])
        pick(t['actor'] for t in self.terminal if t['choice']=='spare' and t['context'].get('reason')=='incapacity_removed_immediate_threat')
        pick(c['actor'] for c in self.closures if c['reason']=='known_target_death')
        unknown=[]
        for p in self.w.characters.values():
            if p.alive:
                for d in p.lethal_decisions.values():
                    q=self.w.characters.get(d.target_id)
                    if d.status=='active' and q and not q.alive:unknown.append(p.id)
        pick(unknown)
        affinities=[(v['value'],id) for g in self.w.divinities.values() for id,v in g.affinities.items() if id not in chosen and v['value']>0]
        if affinities:chosen.append(max(affinities)[1])
        if len(chosen)<6:pick(t['actor'] for t in self.terminal)
        for id in sorted(scores,key=lambda id:(-scores[id],id)):
            if len(chosen)>=6:break
            if id not in chosen:chosen.append(id)
        trajectories=[]
        for id in chosen:
            p=self.w.characters[id];selected={};by_kind=defaultdict(list)
            for ref in self.by_person[id]:
                if ref in lookup:by_kind[lookup[ref].kind].append(lookup[ref])
            for kind,events in by_kind.items():
                for ev in events[:2]+events[-2:]:selected[ev.id]=ev
            for ev in list(selected.values()):
                c=ev.context;refs=c.get('decision',{}).get('facts',[]) if isinstance(c.get('decision'),dict) else []
                refs=list(refs)+list(c.get('source_facts',[]))
                refs+=[c.get(k) for k in ('source_fact','source_event','death_fact') if isinstance(c.get(k),int)]
                for ref in refs:
                    if ref in lookup:selected[ref]=lookup[ref]
            # Preserva desfechos centrais; amostra de atos repetidos fica limitada.
            final=sorted(selected.values(),key=lambda ev:(ev.turn,ev.id))
            if len(final)>90:
                essential=[ev for ev in final if ev.kind in ('CharacterKilled','CharacterDied','TerminalDecision','PostKillAppraisal','LethalDecisionResolved')]
                final=sorted({ev.id:ev for ev in essential+final[:35]+final[-35:]}.values(),key=lambda ev:(ev.turn,ev.id))
            trajectories.append({'initial':self.initial_people[id],'final':self.person(p),'goal':asdict(p.goal) if p.goal else None,
                'decisions':[asdict(d) for d in p.lethal_decisions.values()],'death_affinity':p.death_affinity,'death_state':p.death_state,
                'death_record':self.w.death_records.get(id),'events':[asdict(ev) for ev in final],
                'relationships':[asdict(r) for r in self.w.relationships.values() if r.source_id==id and r.kind in ('amizade','casamento','pai_de','filho_de') and r.value>=40][:8],
                'divine_affinities':{g.id:g.affinities[id] for g in self.w.divinities.values() if id in g.affinities}})
        return {'first_relevant':self.first_relevant,'trajectories':trajectories,
            'names':{p.id:p.name for p in self.w.characters.values()},'places':{t.id:{'name':t.name,'kind':t.kind,'kingdom':t.kingdom_id} for t in self.w.towns.values()},
            'original_decisions':self.original}

def run(seed,folder,attempt=1):
    folder=Path(folder);folder.mkdir(parents=True,exist_ok=True)
    if any(folder.iterdir()):raise RuntimeError('A pasta da campanha deve estar vazia.')
    start=time.monotonic();frozen=core_hash()
    w=generate_world(seed,with_player=False,config=GenerationConfig(historical_turns=0));e=Engine(w);audit=Audit521(e);audit.output_folder=folder
    initial={'persistent':len(w.characters),'abstract':sum(t.abstract_population for t in w.towns.values()),
        'towns':len(w.towns),'town_kinds':dict(Counter(t.kind for t in w.towns.values())),
        'professions':dict(Counter(p.profession or 'sem profissão' for p in w.characters.values())),
        'food_in_town_stores':sum(e.items.count(t.id,'food') for t in w.towns.values()),
        'kingdoms':[{'id':k.id,'name':k.name,'ruler':k.ruler_id,'culture':k.culture,'religion':k.religion} for k in w.kingdoms.values()],
        'gods':[{'id':g.id,'name':g.name,'domain':g.domain,'values':g.values,'region':g.location.map_id,'influence':g.influence} for g in w.divinities.values()],
        'factions':[{'id':f.id,'name':f.name,'purpose':f.purpose,'members':len(f.member_ids)} for f in w.factions.values()],
        'mythics':[audit.person(p) for p in w.characters.values() if p.mythic_trait], 'religion':audit.religion(True)}
    write(folder/'manifesto.json',{'seed':seed,'rules':RULES_VERSION,'core_sha256':frozen,'hours':HOURS,'attempt':attempt,'requested_override':'1000h substituem as 300h do documento por pedido explícito do usuário; reinício autorizado posteriormente',
        'historical_turns':0,'player':False,'natural_campaigns':1,'final_saves':1,'initial':initial})
    try:
        audit.check()
        for hour in range(1,HOURS+1):
            e.step()
            if hour%50==0:
                if core_hash()!=frozen:raise RuntimeError('O núcleo foi alterado durante a campanha.')
                audit.check()
        save=folder/'save_final.json';save_start=time.monotonic();save.write_text(dumps(w));save_seconds=time.monotonic()-save_start
        decisions=[d for p in w.characters.values() for d in p.lethal_decisions.values()]
        active=[d for p in w.characters.values() if p.alive for d in p.lethal_decisions.values() if d.status=='active']
        open_rows=[]
        for p in w.characters.values():
            if not p.alive:continue
            for d in p.lethal_decisions.values():
                if d.status!='active':continue
                q=w.characters.get(d.target_id)
                death_facts=[{'id':f.event_id,'confidence':f.confidence,'kind':f.kind} for f in p.knowledge.values() if f.target_id==d.target_id and f.kind in ('CharacterDied','CharacterKilled','RemainsLocated')]
                open_rows.append({'actor':p.id,'target':d.target_id,'decision_id':d.id,'age':w.turn-d.created_at,'mode':d.mode,'cause':d.cause,
                    'intensity':d.intensity,'rumination':d.rumination,'world_pressure':d.world_pressure,'death_affinity':p.death_affinity,'sadism':p.personality.sadism,
                    'target_alive_objectively':q.alive if q else None,'known_death_facts':death_facts})
        deliberate=[asdict(ev) for ev in w.history if ev.kind=='CharacterKilled' and ev.context.get('violence_intent')=='kill']
        gods={g.id:{'name':g.name,'domain':g.domain,'energy':g.energy,'pressure':asdict(g.action_pressure),
            'affinities':g.affinities,'bonds':g.bonds,'messages':g.messages,'presence_regions':g.presence_regions,
            'known_faith_losses':g.essence.get('known_faith_losses',[]),'interventions':g.interventions} for g in w.divinities.values()}
        counts=Counter(t['choice'] for t in audit.terminal)
        result={'seed':seed,'rules':RULES_VERSION,'core_sha256':frozen,'hours':w.turn,'attempt':attempt,'initial':initial,
            'alive':sum(p.alive for p in w.characters.values()),'events':dict(audit.counts),'metrics':w.metrics,
            'deaths_by_cause':dict(Counter(d['cause'] for d in w.death_records.values())),
            'deaths_by_context':dict(Counter(d.get('death_context',d['cause']) for d in w.death_records.values())),
            'terminal_choices':dict(counts),'terminal_successes':dict(Counter(t['choice'] for t in audit.terminal if t['executed'])),
            'decisions_created':len(audit.decisions),'decisions_with_lethal_attack':len(audit.decisions&audit.attacking),
            'decisions_retained_by_status':dict(Counter(d.status for d in decisions)),'active_decisions_age':ages(active,w.turn),
            'active_decisions':open_rows,'closure_reasons':dict(Counter(c['reason'] for c in audit.closures)),
            'closures':audit.closures,'deliberate_deaths':deliberate,
            'killers':[{**audit.person(p),'death_affinity':p.death_affinity,'death_state':p.death_state} for p in w.characters.values() if p.death_state.get('kills')],
            'religion_final':audit.religion(True),'faith_health':w.faith_health,'gods':gods,
            'extreme_opportunities':sorted(audit.opportunities,key=lambda r:(r['context']['scores']['finish'],r['context']['intensity'],r['event_id']),reverse=True)[:12],
            'snapshots':audit.snapshots,'integrity_checks':audit.checks,'structural_errors':audit.structural_errors,'causal_violations':audit.violations,
            'runtime_seconds':time.monotonic()-start,'save_seconds':save_seconds,'save_bytes':save.stat().st_size,
            'memory_peak_mib_including_export':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024,'history_events':len(w.history),
            'politics_final':[{'name':k.name,'ruler':k.ruler_id,'political':k.political_state,'economy':k.economic_state} for k in w.kingdoms.values()],
            'active_groups':sum(g.status=='active' for g in w.groups.values()),'active_wanted':sum(r.status=='active' for r in w.wanted_records.values()),
            'factions_final':[{'name':f.name,'members':len(f.member_ids),'status':f.status} for f in w.factions.values()]}
        write(folder/'resultado_1000h.json',result)
        write(folder/'oportunidades_terminais.json',{'opportunities':audit.opportunities,'terminal_choices':audit.terminal,
            'method':'Retratos ao vivo no instante da oportunidade e da escolha; observação do auditor, sem fornecer fatos aos NPCs.'})
        write(folder/'material_lore.json',audit.material())
        (folder/'save_sha256.txt').write_text(hashlib.file_digest(save.open('rb'),'sha256').hexdigest()+'\n')
        print('CONCLUÍDO '+json.dumps({'hours':w.turn,'alive':result['alive'],'deaths':result['deaths_by_cause'],
            'terminal_choices':result['terminal_choices'],'deliberate_deaths':len(deliberate),'runtime':result['runtime_seconds'],
            'violations':len(audit.violations),'save_mib':result['save_bytes']/2**20},ensure_ascii=False),flush=True)
    except Exception as error:
        write(folder/'falha_resumida.json',{'hour':w.turn,'core_sha256':frozen,'error':str(error),'structural_errors':audit.structural_errors,'causal_violations':audit.violations})
        write(folder/'evidencia_parcial_falha.json',{'hour':w.turn,'events':dict(audit.counts),'metrics':w.metrics,
            'religion':audit.religion(True),'opportunities':audit.opportunities,'terminal':audit.terminal,
            'closures':audit.closures,'material_lore':audit.material()});raise

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--seed',required=True);parser.add_argument('--folder',required=True);parser.add_argument('--attempt',type=int,default=1)
    args=parser.parse_args();run(args.seed,args.folder,args.attempt)
