"""Métricas complementares extraídas dos registros, sem executar ou alterar saves."""
from collections import Counter
import gzip
import json
from pathlib import Path
import statistics

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'reports/fase_3_2'
OLD = ROOT / 'reports/correcao_alimentar'
MODES = ('jogador', 'espectador', 'mundo')


def rows(path):
    with gzip.open(path, 'rt', encoding='utf-8') as stream:
        for line in stream:
            yield json.loads(line)


def feeding(directory):
    counts = Counter()
    targets = {}
    completed = set()
    durations = []
    for row in rows(directory / 'alimentacao.jsonl.gz'):
        if row['kind'] == 'FoodSearchStarted':
            counts['searches'] += 1
            counts['searches_hunger_below_50'] += row['hunger'] < 50
            counts['searches_hunger_at_least_80'] += row['hunger'] >= 80
            counts['searches_hp_at_most_3'] += row['hp'] <= 3
            targets[(row['npc_id'], row['turn'])] = row['ReserveTarget']
        elif row['kind'] == 'FoodAcquired' and row.get('search_started') is not None:
            key = row['npc_id'], row['search_started']
            if key in targets and key not in completed and row['food_owned'] >= targets[key]:
                completed.add(key)
                durations.append(row['turn'] - row['search_started'])
    return dict(counts) | {
        'search_targets_completed': len(durations),
        'hours_to_recorded_target_mean': statistics.mean(durations) if durations else None,
        'hours_to_recorded_target_median': statistics.median(durations) if durations else None,
        'hours_to_recorded_target_maximum': max(durations) if durations else None,
    }


def social(directory):
    counts = Counter()
    missing_episodes = set()
    located_episodes = set()
    empty_reply_episodes = set()
    for row in rows(directory / 'acoes_pessoais.jsonl.gz'):
        need = row['need']
        action = row['goal']['action']
        counts['personal_information_requests'] += action == 'ask_personal_help'
        counts['requests_with_useful_information'] += (
            action == 'ask_personal_help' and row['success'] and row['outcome'] == 'Informação transmitida.')
        if need['kind'] == 'family' and need['context'].get('mode') == 'missing':
            episode = row['npc_id'], need['id'], need['created_at'], need['source']
            missing_episodes.add(episode)
            if action == 'check_relative' and row['outcome'].startswith(('Pessoa localizada', 'Morte confirmada')):
                located_episodes.add(episode)
            if action == 'ask_personal_help' and not row['success']:
                empty_reply_episodes.add(episode)
    for row in rows(directory / 'narrativa.jsonl.gz'):
        if row['kind'] == 'InformationShared':
            counts['useful_facts_transmitted'] += 1
            counts['transmission:' + row['context']['utility']] += 1
    return dict(counts) | {
        'missing_episodes_with_action': len(missing_episodes),
        'missing_episodes_with_direct_location_confirmation': len(located_episodes),
        'missing_episodes_with_failed_help_request': len(empty_reply_episodes),
    }


def main():
    results = {}
    for mode in MODES:
        directory = OUT / 'auditorias' / mode
        detail = json.loads((directory / 'metricas_fase32.json').read_text())
        results[mode] = {
            'before': feeding(OLD / 'auditorias' / mode),
            'after': feeding(directory),
            'mean_coverage_hours_while_reserve_active': (
                detail['counts']['coverage_hours_sum'] / detail['counts']['reserve_active']),
            'reserve_winners': detail['reserve_winners'],
            'healthy_reserve_winners': detail['healthy_reserve_winners'],
            'social': social(directory),
        }
    results['method'] = (
        'Buscas e aquisições são registros alimentares. O alvo é o registrado no início da busca; '
        'conclusões contam uma vez por indivíduo/turno inicial, não uma reserva mantida para sempre. '
        'A média de tempo usa somente buscas com conclusão observada, sem imputar sucesso às demais. '
        'Episódios sociais usam indivíduo/necessidade/criação/fonte e apenas ações capturadas. '
        'Pedido de ajuda pessoal também pode ser companhia ou quest. Confirmação direta não mede '
        'todo reencontro espontâneo. Pedido fracassado não significa episódio definitivamente insolúvel. '
        'Não atribuímos fechamento de necessidade à informação indireta sem registro causal suficiente.')
    path = OUT / 'metricas_complementares.json'
    path.write_text(json.dumps(results, ensure_ascii=False, indent=2) + '\n')
    print(path)


if __name__ == '__main__':
    main()
