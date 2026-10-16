"""Uma seed nova, 500h, um save; material narrativo filtrado, sem repetir histórico."""
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

STORY={'ItemStolen','ConflictStarted','CharacterAttacked','CharacterKilled','LethalDecision','LethalDecisionUpdated','LethalDecisionAbandoned',
 'LethalDecisionResolved','ExecutionOpportunity','TerminalDecision','PostKillAppraisal','DeathAffinityIncrease',
 'SerialViolencePattern','WantedIssued','CharacterCaptured','CharacterReleased','CharacterFled','CharacterWithdrew',
 'GroupFormed','GroupProtested','ProposalCreated','ProposalSubmitted','PolicyDecided','PolicyRead','ResponseRelayed',
 'FactionJoined','OrganizationalAction','OrganizationalPreparation','FaithReinterpreted','SpiritualReport','PrayerOffered',
 'DivineAffinityChanged','DivineBondCreated','DivineIntervention','ChampionCandidate','ReligiousDeclineReported',
 'PersonLocated','FamilyConcern','AbsenceNoticed','ResidentMoved','ProtectionGiven','FirstAidGiven','HelpGiven',
 'IncapacitatedSpared','PowerTrained','TrainingStarted','TrainingCompleted','MayorAppointed','CharacterDied'}
IMPORTANT={'CharacterKilled','LethalDecision','TerminalDecision','PostKillAppraisal','ProposalSubmitted','ResponseRelayed',
 'OrganizationalAction','DivineIntervention','DivineBondCreated','ChampionCandidate','FaithReinterpreted','TrainingCompleted'}

class Audit52:
    def __init__(self,e):
        self.e,self.w=e,e.world;self.counts=Counter();self.violations=[];self.checks=[]
        self.decisions=set();self.attacking=set();self.finishing=set();self.actor_actions=Counter();self.sources={}
        self.first_social=None;self.by_person=defaultdict(list);self.metrics_before=dict(self.w.metrics)
        self.initial_people={p.id:self.person(p) for p in self.w.characters.values()}
        e.bus.subscribe('*',self.event)
    def person(self,p):
        return {'id':p.id,'name':p.name,'profession':p.profession,'town':p.town_id,'home':asdict(p.home),
            'faith':p.religion,'devotion':p.devotion,'health':p.health,'alive':p.alive,'mythic':p.mythic_trait,
            'sadism':p.personality.sadism,'money':p.money}
    def event(self,ev):
        self.counts[ev.kind]+=1;c=ev.context
        if ev.kind=='LethalDecision':self.decisions.add(c['decision']['id'])
        if ev.kind in ('CharacterAttacked','CharacterKilled') and c.get('violence_intent')=='kill':
            audit=c.get('lethal_audit',{});decision=audit.get('decision_id') or c.get('decision_id')
            if decision:self.attacking.add(decision)
            self.actor_actions[ev.actor_id]+=1
            a=c.get('action_audit',{})
            if not a.get('eligible') or not a.get('eligibility_causes') or not decision:
                self.violations.append({'event':ev.id,'kind':ev.kind,'audit':a,'decision':decision})
        if ev.kind=='TerminalDecision' and c.get('decision')=='finish':
            self.finishing.add(c.get('terminal_context',{}).get('decision_id'))
        if ev.kind in ('DivineIntervention','DivinePresenceChanged'):
            if not c.get('source_fact') or not c.get('energy_cost'):self.violations.append({'event':ev.id,'kind':ev.kind,'cause':'missing_received_cause_or_cost'})
        if ev.kind in STORY:
            if self.first_social is None and ev.historical and ev.kind in ('ItemStolen','ConflictStarted','GroupFormed','ProposalSubmitted','CharacterKilled'):
                self.first_social=ev.id
            participants={ev.actor_id,ev.target_id,c.get('target_id'),c.get('mortal')}
            participants|={c.get('decision',{}).get('actor_id')} if isinstance(c.get('decision'),dict) else set()
            for p in participants:
                if p in self.w.characters:self.by_person[p].append(ev.id)
    def check(self):
        errors=validate_world(self.w)
        for ev in self.w.history:
            if ev.kind not in ('CharacterAttacked','CharacterKilled','LethalConsideration'):continue
            references=set(ev.context.get('action_audit',{}).get('source_facts',[]))
            references.update(ev.context.get('lethal_audit',{}).get('known_facts',[]))
            if any(fact>ev.id for fact in references):
                self.violations.append({'event':ev.id,'kind':ev.kind,'cause':'future_fact_in_historical_audit'})
        if errors or self.violations:raise RuntimeError(str((errors+self.violations)[:4]))
        self.checks.append(self.w.turn)
        print(json.dumps({'hour':self.w.turn,'alive':sum(p.alive for p in self.w.characters.values()),
            'decisions':self.counts['LethalDecision'],'lethal_attacks':self.w.metrics.get('LethalAttack',0),
            'deliberate_deaths':self.w.metrics.get('IntentionalCombatKill',0)+self.w.metrics.get('DeliberateFinish',0),
            'terminal_opportunities':self.counts['ExecutionOpportunity'],'interventions':self.counts['DivineIntervention']},ensure_ascii=False),flush=True)
    def material(self):
        lookup={ev.id:ev for ev in self.w.history};scores={}
        for id,refs in self.by_person.items():
            kinds=Counter(lookup[i].kind for i in refs if i in lookup)
            score=sum(min(v,3)*(10 if k in IMPORTANT else 1) for k,v in kinds.items())+len(kinds)*2
            if kinds['CharacterKilled']:score+=80
            if kinds['LethalDecision']:score+=40
            if kinds['DivineIntervention'] or kinds['DivineBondCreated']:score+=100
            scores[id]=score
        chosen=[];covered=set()
        # Diversidade de trajetórias, sem buscar outra seed.
        categories=[{'CharacterKilled','PostKillAppraisal'},{'LethalDecision'},
            {'ProposalSubmitted','ResponseRelayed'},{'DivineAffinityChanged','PrayerOffered'},
            {'TrainingCompleted','PowerTrained'},{'PersonLocated','AbsenceNoticed'}]
        for category in categories:
            choices=[i for i in scores if i not in covered and any(lookup[r].kind in category for r in self.by_person[i] if r in lookup)]
            if choices:
                id=max(choices,key=lambda i:(scores[i],-i));chosen.append(id);covered.add(id)
        for id in sorted(scores,key=lambda i:(-scores[i],i)):
            if id not in covered and len(chosen)<8:chosen.append(id);covered.add(id)
        trajectories=[]
        for id in chosen:
            all_events=[lookup[i] for i in self.by_person[id] if i in lookup]
            selected={}
            by_kind=defaultdict(list)
            for ev in all_events:by_kind[ev.kind].append(ev)
            for kind,events in by_kind.items():
                for ev in events[:2]+events[-2:]:selected[ev.id]=ev
            # Fonte conhecida de decisão e encadeamento de propostas selecionadas.
            sources=set()
            for ev in list(selected.values()):
                c=ev.context
                sources.update(c.get('source_facts',[]));sources.update(c.get('decision',{}).get('facts',[]) if isinstance(c.get('decision'),dict) else [])
                for source in ('source_fact','death_fact','source_event'):
                    if isinstance(c.get(source),int):sources.add(c[source])
            for source in sources:
                if source in lookup:selected[source]=lookup[source]
            p=self.w.characters[id]
            trajectories.append({'initial':self.initial_people.get(id),'final':self.person(p),
                'final_goal':asdict(p.goal) if p.goal else None,'decisions':[asdict(d) for d in p.lethal_decisions.values()],
                'death_state':p.death_state,'death_affinity':p.death_affinity,
                'relations':[asdict(r) for r in self.w.relationships.values() if r.source_id==id and r.kind in ('casamento','pai_de','filho_de','amizade') and r.value>=40][:8],
                'events':[asdict(ev) for ev in sorted(selected.values(),key=lambda ev:(ev.turn,ev.id))[:75]]})
        return {'first_social':asdict(lookup[self.first_social]) if self.first_social in lookup else None,
            'trajectories':trajectories,'names':{p.id:p.name for p in self.w.characters.values()},
            'places':{t.id:t.name for t in self.w.towns.values()},
            'religious_transitions':[asdict(ev) for ev in self.w.history if ev.kind in ('RegionalFaithHealthChanged','GlobalFaithHealthChanged','DivinePresenceChanged','DivineIntervention','FavoredFollowerKilled')][:100]}

def run(seed,folder):
    folder=Path(folder);folder.mkdir(parents=True,exist_ok=True)
    if any(folder.iterdir()):raise RuntimeError('A pasta da campanha deve estar vazia.')
    start=time.monotonic();frozen=core_hash()
    w=generate_world(seed,with_player=False,config=GenerationConfig(historical_turns=0));e=Engine(w);audit=Audit52(e)
    initial={'persistent':len(w.characters),'abstract':sum(t.abstract_population for t in w.towns.values()),
        'towns':len(w.towns),'kingdoms':len(w.kingdoms),'factions':len(w.factions),'gods':len(w.divinities),
        'mythic':sum(bool(p.mythic_trait) for p in w.characters.values()),
        'professions':dict(Counter(p.profession or 'sem profissão' for p in w.characters.values())),
        'food':sum(e.items.count(t.id,'food') for t in w.towns.values()),
        'faith_composition':e.religious_health.composition(),
        'kingdom_details':[{'id':k.id,'name':k.name,'family':k.family_name,'religion':k.religion,'culture':k.culture,'ruler':k.ruler_id} for k in w.kingdoms.values()],
        'god_details':[{'id':g.id,'name':g.name,'domain':g.domain,'values':g.values,'birth_region':g.location.map_id,'influence':g.influence} for g in w.divinities.values()],
        'faction_details':[{'id':f.id,'name':f.name,'purpose':f.purpose,'members':len(f.member_ids)} for f in w.factions.values()]}
    (folder/'manifesto.json').write_text(json.dumps({'seed':seed,'rules':RULES_VERSION,'core_sha256':frozen,'hours':500,'historical_turns':0,'player':False,'natural_campaigns':1,'final_saves':1,'initial':initial},ensure_ascii=False,indent=2))
    try:
        audit.check()
        for hour in range(1,501):
            e.step()
            if hour%50==0:audit.check()
        if core_hash()!=frozen:raise RuntimeError('O núcleo mudou durante a campanha.')
        save_start=time.monotonic();save=folder/'save_final.json';save.write_text(dumps(w));save_seconds=time.monotonic()-save_start
        metrics={k:v-audit.metrics_before.get(k,0) for k,v in w.metrics.items() if k.startswith(('Lethal','Intentional','Deliberate','Terminal','DeathAffinity','PostKill','ViolenceSeeking','Divine','Faith','Regional','Global','CoreErosion','CultCollapse','HighAffinity','Serial','ActionPressure','Society'))}
        decisions=[d for p in w.characters.values() for d in p.lethal_decisions.values()]
        gods={g.id:{'name':g.name,'domain':g.domain,'region':g.location.map_id,'energy':g.energy,'pressure':asdict(g.action_pressure),
                'affinities':g.affinities,'bonds':g.bonds,'messages':g.messages,'champion_candidates':g.essence.get('champion_candidates',[]),
                'known_losses':g.essence.get('known_faith_losses',[]),'interventions':g.interventions} for g in w.divinities.values()}
        lethal_deaths=[{'id':ev.id,'hour':ev.turn,'actor':ev.actor_id,'target':ev.target_id,'location':asdict(ev.location),'context':ev.context} for ev in w.history if ev.kind=='CharacterKilled' and ev.context.get('violence_intent')=='kill']
        data={'seed':seed,'rules':RULES_VERSION,'core_sha256':frozen,'hours':w.turn,'initial':initial,
            'alive':sum(p.alive for p in w.characters.values()),'death_causes':dict(Counter(d['cause'] for d in w.death_records.values())),
            'death_contexts':dict(Counter(d.get('death_context',d['cause']) for d in w.death_records.values())),
            'events':dict(audit.counts),'metrics':metrics,'decisions_by_mode':dict(Counter(d.mode for d in decisions)),
            'decisions_final_by_status':dict(Counter(d.status for d in decisions)),
            'conversions':{'decisions_created':len(audit.decisions),'decisions_with_lethal_attack':len(audit.attacking & audit.decisions),
                'decisions_with_finish':len(audit.finishing & audit.decisions),'decision_attack_fraction':len(audit.attacking & audit.decisions)/max(1,len(audit.decisions))},
            'deliberate_deaths':lethal_deaths,'killers':[{**audit.person(p),'death_affinity':p.death_affinity,'death_state':p.death_state} for p in w.characters.values() if p.death_state.get('kills')],
            'faith_health_objective':w.faith_health,'composition_final':e.religious_health.composition(),'gods':gods,
            'patterns':{p.id:p.social_state.get('violence_patterns',{}) for p in w.characters.values() if p.social_state.get('violence_patterns')},
            'guard_pattern_needs':sum(any(n.context.get('violence_pattern') for n in p.needs.values()) for p in w.characters.values() if p.profession=='guarda'),
            'integrity_checks':audit.checks,'invariant_errors':[],'causal_violations':audit.violations,
            'runtime_seconds':time.monotonic()-start,'save_seconds':save_seconds,'save_bytes':save.stat().st_size,
            'memory_peak_mib_including_export':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024,'history_events':len(w.history),
            'deprivation_with_food':sum(d['cause'] in ('hunger','both') and d.get('food',0)>0 for d in w.death_records.values()),
            'politics_final':[{'name':k.name,'ruler':k.ruler_id,'political':k.political_state,'economy':k.economic_state,'social':k.social_state} for k in w.kingdoms.values()],
            'unresolved_cases':sum(r.status=='active' for r in w.wanted_records.values()),
            'active_groups':sum(g.status=='active' for g in w.groups.values()),
            'pending_proposals':dict(Counter(p.status for p in w.proposals.values())),
            'factions_final':[{'name':f.name,'members':len(f.member_ids),'status':f.status,'pressure':asdict(f.action_pressure)} for f in w.factions.values()]}
        (folder/'resultado_500h.json').write_text(json.dumps(data,ensure_ascii=False,indent=2))
        (folder/'material_lore.json').write_text(json.dumps(audit.material(),ensure_ascii=False,indent=2))
        (folder/'save_sha256.txt').write_text(hashlib.file_digest(save.open('rb'),'sha256').hexdigest()+'\n')
        print('CONCLUÍDO '+json.dumps({'hours':w.turn,'alive':data['alive'],'deaths':data['death_causes'],'contexts':data['death_contexts'],'runtime':data['runtime_seconds'],'save_mib':data['save_bytes']/2**20},ensure_ascii=False),flush=True)
    except Exception as error:
        (folder/'falha_resumida.json').write_text(json.dumps({'hour':w.turn,'core_sha256':frozen,'error':str(error)},ensure_ascii=False,indent=2));raise

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--seed',required=True);parser.add_argument('--folder',required=True)
    args=parser.parse_args();run(args.seed,args.folder)
