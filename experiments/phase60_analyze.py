"""Leitura pós-campanha, apenas dos registros nativos persistidos."""
from pathlib import Path
from collections import Counter,defaultdict
import json,gzip
from procedural.persistence import decode

OUT=Path(__file__).resolve().parents[1]/'reports/fase_6_0'

def main():
    campaign=json.loads((OUT/'campanha.json').read_text());assert campaign['status']=='completed'
    details=json.loads((OUT/'detalhes_nativos.json').read_text())
    with gzip.open(OUT/'historico_nativo.json.gz','rt') as stream:archive=decode(json.load(stream))
    obs=archive['observability'];events={ev.id:ev for ev in [*archive['events'],*obs.event_archive.values()]}
    reasons=Counter();motives=Counter();injuries=0;latencies=defaultdict(list)
    created={};submitted={};policy_created={};decided=set();deaths_lod=Counter();missing_lod=[]
    for ev in sorted(events.values(),key=lambda e:e.id):
        ctx=ev.context
        if ev.kind=='GroupJoinRejected':reasons[ctx.get('reason','UNKNOWN')]+=1
        if ev.kind=='CharacterAttacked':
            injuries+=ctx.get('damage',0);trace=obs.decisions.get(ev.decision_id)
            mode=ctx.get('action_audit',{}).get('mode')
            if not mode:
                for id in ev.parent_event_ids:
                    parent=events.get(id)
                    if parent and parent.kind=='LethalDecision':mode=parent.context.get('decision',{}).get('mode')
            sources=[events[i] for i in ev.parent_event_ids if i in events]
            if ctx.get('lawful'):motive='law_enforcement'
            elif ctx.get('self_defense'):motive='self_defense'
            elif mode=='hedonic':motive='hedonic'
            elif mode in ('protective','reactive_threat') or trace and trace.need_kind=='protection':motive='protective'
            elif mode in ('retributive','moral_punishment') or trace and trace.need_kind=='revenge':motive='retributive'
            elif mode=='instrumental':motive='instrumental'
            elif any(e.kind in ('ItemStolen','PersonalItemStolen') for e in sources):motive='theft_response'
            else:motive='other_or_unknown'
            motives[motive]+=1
        if ev.kind=='ProposalCreated':created.setdefault(ev.target_id,ev.turn)
        if ev.kind=='ProposalSubmitted':submitted.setdefault(ctx.get('proposal_id'),ev.turn)
        if ev.kind=='PolicyCreated':policy_created.setdefault(ev.target_id,ev.turn)
        if ev.kind=='PolicyDecided' and ev.target_id in created and ev.target_id not in decided:
            latencies['proposal_to_first_decision'].append(ev.turn-created[ev.target_id]);decided.add(ev.target_id)
        if ev.kind=='PolicyCompleted' and ev.target_id in policy_created:latencies['policy_to_completion'].append(ev.turn-policy_created[ev.target_id])
        if ev.kind in ('CharacterKilled','CharacterDied'):
            # Este é o último LOD de DECISÃO conhecido, não um novo snapshot
            # físico inventado do instante da morte.
            actor=obs.causal.get('actors',{}).get(ev.target_id,{})
            lod=actor.get('lod')
            if lod:deaths_lod[lod]+=1
            else:missing_lod.append(ev.target_id)
    for prop,turn in submitted.items():
        if prop in created:latencies['proposal_to_first_submission'].append(turn-created[prop])
    death_events={ev.target_id:ev.id for ev in events.values() if ev.kind in ('CharacterDied','CharacterKilled')}
    after_death=[]
    for task in details.get('tasks',[]):
        event=events.get(task.get('last_event_id'))
        if task['status']=='completed' and event and death_events.get(task['issuer'],event.id+1)<event.id:
            after_death.append({'task':task['id'],'kind':task['kind'],'issuer':task['issuer'],'completion_event':event.id,
                'executor':event.actor_id,'turn':event.turn,'issuer_death_event':death_events[task['issuer']]})
    first_latency={}
    for row in obs.causal.get('episodes',{}).values():
        lod=row.get('first_selection_lod')
        if lod and row['time_until_first_selection'] is not None:
            first_latency.setdefault(lod,[]).append(row['time_until_first_selection'])
    def statistics(rows):return {'observations':len(rows),'mean':sum(rows)/len(rows) if rows else None,'maximum':max(rows) if rows else None}
    result={'seed':campaign['seed'],'source':'historico_nativo.json.gz; no reexecution',
        'join_rejection_reasons':dict(reasons),'attack_motives_refined':dict(motives),
        'tasks_completed_after_issuer_death':after_death,
        'attack_damage_recorded':injuries,'latencies':{k:statistics(v) for k,v in latencies.items()},
        'need_latency_by_first_selection_lod':{k:statistics(v) for k,v in first_latency.items()},
        'all_deaths_by_last_decision_lod':dict(deaths_lod),'deaths_without_decision_lod':missing_lod,
        'scope':'Motivos classificados por flags explícitas, mode auditado/parent e Need. Outros ficam UNKNOWN; múltiplos motivos podem existir. LOD é o último registro de decisão, não posição atual inferida.'}
    (OUT/'analise_nativa.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
    print(json.dumps(result,ensure_ascii=False))

if __name__=='__main__':main()
