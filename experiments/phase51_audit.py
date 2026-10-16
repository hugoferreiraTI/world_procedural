"""Um mundo: marco de 200h, depois 1000h. Um save e exemplos filtrados."""
import argparse,hashlib,json,resource,time
from collections import Counter,defaultdict
from dataclasses import asdict
from pathlib import Path
from procedural import RULES_VERSION
from procedural.engine import Engine
from procedural.generation import generate_world,GenerationConfig
from procedural.validation import validate_world
from procedural.persistence import dumps
from procedural.action_pressure import band,KINDS,FORWARD
from experiments.phase41_audit import core_hash

RELEVANT={'GroupFormed','GroupMeeting','GroupProtested','GroupDissolved','ProposalCreated','ProposalSubmitted',
 'PolicyDecided','PolicyRead','ResponseRelayed','FactionJoined','FactionFounded','FactionReport',
 'OrganizationalPreparation','OrganizationalOrder','OrganizationalAction','PrayerOffered','SpiritualReport',
 'DivineIntervention','FaithReinterpreted','ViolenceIntentChanged','ExecutionOpportunity','TerminalDecision',
 'CharacterKilled','DivinityKilled','Apotheosis'}

class Audit51:
    def __init__(self,e):
        self.e=e;self.w=e.world;self.events=Counter();self.formed={};self.group_actions=set();self.faction_actions=set()
        self.responses=set();self.lethal_actors=set();self.lethal_active=set();self.extreme_violations=[]
        self.kill_changes=0;self.commitment_intentions=set();self.forward_progress=set()
        self.samples=[];self.cases={};self.group_chains=defaultdict(list);self.checks=[]
        self.initial_metrics=dict(self.w.metrics);e.bus.subscribe('*',self.event)
    def event(self,event):
        if event.kind in ('CommitmentCreated','CommitmentProgress'):
            c=event.context
            if c.get('origin') in KINDS:
                if event.kind=='CommitmentCreated':self.commitment_intentions.add(c['commitment_id'])
                elif c.get('action') in FORWARD:self.forward_progress.add(c['commitment_id'])
            return
        if event.kind not in RELEVANT and event.kind!='CharacterAttacked':return
        self.events[event.kind]+=1;c=event.context
        gid=c.get('group_id') or (event.target_id if event.kind.startswith('Group') or event.kind=='ResponseRelayed' else None)
        if event.kind=='GroupFormed':
            self.formed[event.target_id]={'name':self.w.groups[event.target_id].name,'town':c['town_id'],
                'cause':c['cause'],'leader':event.actor_id,'turn':event.turn,'source_fact':c['source_fact']}
        if gid:
            if len(self.group_chains[gid])<8:self.group_chains[gid].append(asdict(event))
            if event.kind in ('ProposalSubmitted','GroupProtested','ResponseRelayed'):self.group_actions.add(gid)
        if event.kind=='ProposalSubmitted':
            group=self.w.groups.get(gid);kind='village_representation' if group and self.w.towns[group.town_id].kind=='vila' else 'local_representation'
            self.case(kind,event,group_id=gid,origin=self.formed.get(gid),chain=self.group_chains[gid][-6:])
        if event.kind=='GroupProtested':self.case('received_failure_and_protest',event,origin=self.formed.get(gid),chain=self.group_chains[gid][-6:])
        if event.kind=='ResponseRelayed':self.case('physical_response_return',event,origin=self.formed.get(gid),chain=self.group_chains[gid][-6:])
        if event.kind=='PolicyDecided':
            group=self.w.groups.get(gid)
            if group:
                for i in group.member_ids:
                    p=self.w.characters[i]
                    if event.id in p.knowledge:self.responses.add((event.id,i))
            self.case('material_policy',event,origin=self.formed.get(gid))
        if event.kind in ('PolicyRead','ResponseRelayed'):
            for fact in c.get('new_source_facts',c.get('source_facts',[]) if event.kind=='ResponseRelayed' else []):
                for i in c.get('recipients',[event.actor_id]):self.responses.add((fact,i))
        if event.kind=='OrganizationalPreparation':self.case('faction_capacity_preparation',event)
        if event.kind in ('OrganizationalAction','FactionJoined') or event.kind=='OrganizationalPreparation' and c.get('resources_transferred',0)>0:
            self.faction_actions.add(event.target_id);self.case('faction_action',event)
        if event.kind=='DivineIntervention':self.case('divine_action',event)
        if event.kind=='ViolenceIntentChanged' and c.get('intent')=='kill':
            self.lethal_actors.add(event.actor_id);self.kill_changes+=1
        if event.kind=='CharacterAttacked' and c.get('violence_intent')=='kill':self.lethal_active.add(event.actor_id)
        if event.kind=='CharacterKilled':
            self.case('combat_death',event)
            if c.get('death_context')=='deliberate_finish':self.case('deliberate_finish',event)
        if (event.kind in ('TerminalDecision','DivineIntervention') or event.kind=='OrganizationalAction' and c.get('action')=='raid'
                or event.kind in ('CharacterAttacked','CharacterKilled') and c.get('violence_intent')=='kill'):
            a=c.get('action_audit') or {}
            if not a.get('eligibility_causes') or a.get('world_pressure',0)<60:
                self.extreme_violations.append({'event':event.id,'kind':event.kind,'audit':a})
    def case(self,key,event,**extra):
        if key in self.cases:return
        actor=self.w.characters.get(event.actor_id);sources=[]
        ids=(event.context.get('action_audit') or {}).get('source_facts',[])
        for i in ids:
            fact=actor.knowledge.get(i) if actor else None
            if not fact and event.actor_id in self.w.divinities:
                god=self.w.divinities[event.actor_id]
                seen=next((x.get('record') for x in god.essence.get('seen_deeds',[]) if x['fact']==i),None)
                fact=seen
            if fact:sources.append(asdict(fact))
        self.cases[key]={'event':asdict(event),'sources':sources,**extra}
    def check(self):
        errors=validate_world(self.w)
        if errors or self.extreme_violations:raise RuntimeError(str((errors+self.extreme_violations)[:5]))
        self.checks.append(self.w.turn)
        distributions={}
        scopes={'npc':[max((r.value for r in p.action_pressures.values()),default=0) for p in self.w.characters.values() if p.alive],
            'group':[g.action_pressure.value for g in self.w.groups.values() if g.status=='active'],
            'faction':[f.action_pressure.value for f in self.w.factions.values() if f.status=='active'],
            'god':[g.action_pressure.value for g in self.w.divinities.values() if g.alive]}
        for kind,values in scopes.items():distributions[kind]=dict(Counter(band(v) for v in values))
        self.samples.append({'hour':self.w.turn,'pressure':distributions})
        print(json.dumps({'hour':self.w.turn,'alive':sum(p.alive for p in self.w.characters.values()),
            'groups_with_action':len(self.group_actions),'submitted':self.events['ProposalSubmitted'],
            'responses_learned':len(self.responses),'organizational_actions':self.events['OrganizationalAction'],
            'interventions':self.events['DivineIntervention']},ensure_ascii=False),flush=True)
    def summary(self,initial,start):
        w=self.w;metrics={k:v-self.initial_metrics.get(k,0) for k,v in w.metrics.items() if k.startswith(('ActionPressure:','Faith:','Society:'))}
        def count(k):return metrics.get('ActionPressure:'+k,0)
        def rate(a,b):return round(a/b,4) if b else None
        conversions={'npc':{'pressure_record_creations':count('records_created:npc'),
            'commitment_episodes_created':len(self.commitment_intentions),'commitments_with_forward_progress':len(self.forward_progress & self.commitment_intentions),
            'forward_progress_fraction':rate(len(self.forward_progress & self.commitment_intentions),len(self.commitment_intentions)),
            'action_executions':count('actions:npc'),'consequence_executions':count('consequences:npc'),
            'actions_per_pressure_record_creation':rate(count('actions:npc'),count('records_created:npc'))},
            'group':{'formed':self.events['GroupFormed'],'with_meaningful_action':len(self.group_actions),
                'proposals_created':self.events['ProposalCreated'],'proposals_submitted':self.events['ProposalSubmitted'],
                'response_actor_pairs_learned':len(self.responses),'responses_relayed':self.events['ResponseRelayed'],
                'groups_with_action_fraction':rate(len(self.group_actions),self.events['GroupFormed']),
                'submission_fraction':rate(self.events['ProposalSubmitted'],self.events['ProposalCreated'])},
            'faction':{'existing':len(w.factions),'with_meaningful_action':len(self.faction_actions),
                'organizational_actions':self.events['OrganizationalAction'],'preparation_attempts':self.events['OrganizationalPreparation'],
                'joined':self.events['FactionJoined']},
            'god':{'prayers':self.events['PrayerOffered'],'intention_episodes':count('intentions:god'),
                'action_considered':count('considered:god'),'interventions':self.events['DivineIntervention'],
                'interventions_per_consideration':rate(self.events['DivineIntervention'],count('considered:god'))},
            'lethal':{'intent_changes':self.kill_changes,'lethal_option_evaluations_available':w.metrics.get('Lethal:available',0),
                'actors_with_kill_intent':len(self.lethal_actors),'actors_with_lethal_attack':len(self.lethal_active),
                'actual_attack_fraction':rate(len(self.lethal_active),len(self.lethal_actors)),
                'terminal_opportunities':self.events['ExecutionOpportunity'],'terminal_decisions':self.events['TerminalDecision']}}
        deaths=dict(Counter(d['cause'] for d in w.death_records.values()))
        new_values=sum(len(json.dumps(asdict(r),separators=(',',':')).encode()) for p in w.characters.values() for r in p.action_pressures.values())
        new_values+=sum(len(json.dumps(asdict(o.action_pressure),separators=(',',':')).encode()) for o in (*w.groups.values(),*w.factions.values(),*w.divinities.values()))
        return {'seed':w.seed,'rules':RULES_VERSION,'core_sha256':core_hash(),'hours':w.turn,'initial':initial,
            'alive':sum(p.alive for p in w.characters.values()),'death_causes':deaths,
            'deprivation_deaths_with_food':sum(d['cause'] in ('hunger','both') and d.get('food',0)>0 for d in w.death_records.values()),
            'events':dict(self.events),'conversions':conversions,'pressure_samples':self.samples,
            'metrics':metrics,'integrity_checks':self.checks,'invariant_errors':[],
            'extreme_semantic_violations':self.extreme_violations,'runtime_seconds':time.monotonic()-start,
            'memory_peak_including_export_mib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024,
            'pressure_record_value_bytes':new_values,'history_events':len(w.history),
            'faith_influence_objective_audit_only':self.e.faith.influence(),
            'gods_known_influence':{g.id:g.essence.get('follower_regions',{}) for g in w.divinities.values()},
            'factions_final':{f.id:{'name':f.name,'members':f.member_ids,'pressure':asdict(f.action_pressure),
                'leader_position':asdict(w.characters[f.leader_id].position),'leader_goal':asdict(w.characters[f.leader_id].goal) if w.characters[f.leader_id].goal else None} for f in w.factions.values()},
            'method':'Um mundo novo; checkpoint 200h e continuação até 1000h. Sem jogador, sem história prévia, sem save anterior. Contadores de execução não são pessoas nem sagas.'}

def run(seed,folder):
    folder=Path(folder);folder.mkdir(parents=True,exist_ok=True)
    if any(folder.iterdir()):raise RuntimeError('Pasta de campanha deve estar vazia.')
    frozen=core_hash();start=time.monotonic();w=generate_world(seed,with_player=False,config=GenerationConfig(historical_turns=0));e=Engine(w)
    initial={'persistent':len(w.characters),'abstract':sum(t.abstract_population for t in w.towns.values()),'towns':len(w.towns),'mythic':sum(bool(p.mythic_trait) for p in w.characters.values())}
    (folder/'manifesto.json').write_text(json.dumps({'seed':seed,'rules':RULES_VERSION,'core_sha256':frozen,'short_checkpoint':200,'main_total_hours':1000,'one_world':True,'final_saves':1,'initial':initial},ensure_ascii=False,indent=2))
    audit=Audit51(e);audit.check()
    try:
        for hour in range(1,1001):
            e.step()
            if hour%50==0:audit.check()
            if hour==200:
                if core_hash()!=frozen:raise RuntimeError('Código alterado durante a curta.')
                (folder/'curta_200h.json').write_text(json.dumps(audit.summary(initial,start),ensure_ascii=False,indent=2))
                print('200h estáveis; continuando o mesmo mundo até 1000h.',flush=True)
        if core_hash()!=frozen:raise RuntimeError('Código alterado durante a campanha.')
        save_start=time.monotonic();(folder/'save_final.json').write_text(dumps(w));save_seconds=time.monotonic()-save_start
        result=audit.summary(initial,start);result.update(save_seconds=save_seconds,save_bytes=(folder/'save_final.json').stat().st_size)
        (folder/'principal_1000h.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
        (folder/'exemplos_filtrados.json').write_text(json.dumps(audit.cases,ensure_ascii=False,indent=2))
        (folder/'nomes.json').write_text(json.dumps({'characters':{p.id:p.name for p in w.characters.values()},'towns':{t.id:t.name for t in w.towns.values()},'gods':{g.id:g.name for g in w.divinities.values()}},ensure_ascii=False))
        print('CONCLUÍDO '+json.dumps({'hours':w.turn,'deaths':result['death_causes'],'save_mib':result['save_bytes']/2**20,'conversions':result['conversions']},ensure_ascii=False),flush=True)
    except Exception as error:
        (folder/'falha_resumida.json').write_text(json.dumps({'hour':w.turn,'core_sha256':frozen,'error':str(error)},ensure_ascii=False,indent=2));raise

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--seed',required=True);p.add_argument('--folder',required=True)
    a=p.parse_args();run(a.seed,a.folder)
