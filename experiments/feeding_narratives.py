"""Extrai episódios causais de ações pessoais, sem escrever ficção."""
from collections import Counter, defaultdict
import gzip
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'reports/correcao_alimentar'
ACTION_EVENTS = {
    'check_relative': {'FamilySearch', 'PersonLocated', 'RemainsLocated'},
    'give_supplies': {'HelpGiven'}, 'seek_company': {'ComfortGiven'},
    'remember_relative': {'Remembrance'},
    'investigate': {'PersonLocated', 'RemainsLocated', 'InvestigationPerformed'},
    'denounce': {'InformationShared', 'ThreatReported'}, 'avoid_threat': {'ThreatAvoided'},
    'stay_near': {'ProtectionGiven'},
    'ask_personal_help': {'InformationShared', 'ComfortGiven', 'ProtectionGiven', 'HelpRequested'},
    'work': {'ResponsibilityFulfilled'},
}


def rows(path):
    with gzip.open(path, 'rt', encoding='utf-8') as stream:
        for line in stream:
            yield json.loads(line)


def main():
    results = {}
    for mode in ('jogador', 'espectador', 'mundo'):
        directory = OUT/'auditorias'/mode
        events = list(rows(directory/'narrativa.jsonl.gz'))
        by_id = {e['id']: e for e in events}
        by_actor_time = defaultdict(list)
        for event in events:
            for actor in {event['actor_id'], event['target_id']}:
                if actor is not None:by_actor_time[actor, event['turn']].append(event)
        groups = defaultdict(list)
        for action in rows(directory/'acoes_pessoais.jsonl.gz'):
            need = action['need']
            groups[action['npc_id'], need['id'], need['created_at'], need['source']].append(action)
        episodes = []
        for (npc, need_id, created, source), actions in groups.items():
            need = actions[0]['need'];source_id = need['context'].get('source_event')
            root = by_id.get(source_id)
            if root is None:
                root = next((f for a in actions for f in a['knowledge_before'] if f['event_id'] == source_id), None)
                if root is not None:root = {**root, 'id': root['event_id'], 'before_audit_or_not_in_narrative_stream': True}
            related = {root['id']: root} if root else {}
            trimmed = []
            for a in actions:
                emitted = [e for e in by_actor_time[a['npc_id'], a['turn']]
                           if e['kind'] in ACTION_EVENTS.get(a['goal']['action'], set())]
                for e in emitted:related[e['id']] = e
                fact = next((f for f in a['knowledge_before'] if f['event_id'] == source_id), None)
                observation = a['observations_before'].get(str(need['target_id']))
                trimmed.append({'turn': a['turn'], 'action': a['goal']['action'], 'success': a['success'],
                    'outcome': a['outcome'], 'hunger': a['hunger'], 'health': a['health'],
                    'source_fact_known_before': fact, 'target_observation_before': observation,
                    'events_at_action_ids': [e['id'] for e in emitted]})
            event_list = sorted(related.values(), key=lambda e: (e['turn'], e['id']))
            root_food = bool(root and root['kind'] in ('ItemStolen', 'FamilyConcern'))
            central_food = need['kind'] == 'family' and need['context'].get('mode') == 'care'
            cause_turn = root['turn'] if root else created
            episodes.append({'mode': mode, 'npc_id': npc, 'need_id': need_id,
                'need_created_at': created, 'need': need, 'source': source,
                'events': event_list, 'actions': trimmed,
                'event_count': len(event_list), 'span_hours': actions[-1]['turn']-cause_turn,
                'need_age_hours_at_last_action': actions[-1]['turn']-created,
                'central_food': central_food, 'root_food': root_food})
        # Ordem prática para leitura: episódios com mais evidência, depois duração.
        episodes.sort(key=lambda e: (-e['event_count'], -e['span_hours']))
        trajectories = defaultdict(list)
        for episode in episodes:
            trajectories[episode['npc_id']].extend(a['turn'] for a in episode['actions'])
        stats = {'narrative_event_counts': dict(Counter(e['kind'] for e in events)),
                 'personal_episodes_with_action': len(episodes),
                 'personal_episode_need_kinds': dict(Counter(e['need']['kind'] for e in episodes)),
                 'episodes_by_event_count': dict(Counter('4+' if e['event_count']>=4 else str(e['event_count']) for e in episodes)),
                 'episodes_with_2_or_more_recorded_events': sum(e['event_count']>=2 for e in episodes),
                 'episodes_spanning_at_least_168_hours': sum(e['span_hours']>=168 for e in episodes),
                 'characters_with_personal_actions_over_at_least_720_hours': sum(max(t)-min(t)>=720 for t in trajectories.values()),
                 'episodes_whose_core_is_not_food_care': sum(not e['central_food'] for e in episodes),
                 'autonomous_campaign': mode != 'jogador',
                 'method': 'Agrupamento por NPC e Need/source, com eventos compatíveis com a ação. Duração parte do fato causal atual, pois crimes novos podem atualizar uma necessidade antiga. Não inclui treinamento/sucessão nestes episódios. Ações capturadas antes da execução; episódios são reações locais, não histórias fechadas nem sagas.'}
        (directory/'episodios_narrativos.json').write_text(json.dumps({'statistics': stats, 'episodes': episodes},ensure_ascii=False,indent=2)+'\n')
        results[mode] = stats
    (OUT/'diversidade_narrativa.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(results,ensure_ascii=False,indent=2))


if __name__ == '__main__':main()
