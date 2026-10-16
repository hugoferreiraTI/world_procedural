"""Catálogo verificável de histórias: somente dados dos logs, sem reexecutar regras."""
from collections import Counter
from dataclasses import asdict
import gzip
import json
from pathlib import Path

from procedural.persistence import loads

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'reports/correcao_alimentar'


def rows(path):
    with gzip.open(path, 'rt', encoding='utf-8') as stream:
        for line in stream:
            yield json.loads(line)


STORIES = [
    ('S01', 'jogador', 'Marie: cuidado, denúncia, investigação e luto', [77, 74, 91],
     [10487, 21822, 21823, 22173, 28609, 30885, 37189, 38086, 38088, 39312],
     lambda e: e['id'] in (14464, 21346, 24539),
     lambda a: a['npc_id'] == 77 and a['turn'] in (46, 106, 118, 160, 166, 202, 208)),
    ('S02', 'espectador', 'Lyra Valerius: sucessão e procura de Bela', [1452, 1455, 1458],
     [94161, 95157, 105966, 201247, 209637, 211206],
     lambda e: (e['kind'] == 'SuccessionChanged' and e['turn'] == 430) or
               (e['kind'] == 'CharacterDied' and e['target_id'] in (1452, 1455)),
     lambda a: a['npc_id'] == 1458 and a['turn'] in (491, 548, 1148, 1157)),
    ('S03', 'mundo', 'Lyra Douran: uma ausência e 54 horas de busca', [254, 257],
     [87191, 95738, 96790], lambda e: False,
     lambda a: a['npc_id'] == 254 and a['turn'] in (517, 523)),
    ('S04', 'espectador', 'Elena e John: duas reações ao mesmo crime', [1592, 1595, 1597],
     [16126, 28377, 28378], lambda e: False,
     lambda a: a['npc_id'] in (1592, 1595) and a['turn'] in (154, 160, 175, 181)),
    ('S05', 'jogador', 'Elena denuncia um guarda ao próprio suspeito', [1595, 1597],
     [879781, 883259, 883260], lambda e: False,
     lambda a: a['npc_id'] == 1595 and a['turn'] == 5428),
    ('S06', 'jogador', 'Arthus: a informação antiga que não encerra a procura', [38, 41, 44],
     [63306, 77503, 78420, 78608, 78815, 80984, 81150], lambda e: False,
     lambda a: a['npc_id'] == 41 and a['turn'] in (405, 406, 407, 418, 419)),
    ('S07', 'jogador', 'Cael: um trabalho observado vira reputação', [684, 687, 675, 678],
     [762383], lambda e: False,
     lambda a: a['npc_id'] == 687 and a['turn'] == 4652),
    ('S08', 'espectador', 'Ruan Kars: estabilizar renda pela mudança de profissão', [1480], [],
     lambda e: e['actor_id'] == 1480 and e['kind'].startswith(('Training', 'Profession')) and 1263 <= e['turn'] <= 1599,
     lambda a: a['npc_id'] == 1480 and a['goal']['action'] == 'train' and a['turn'] in (1263, 1599)),
    ('S09', 'espectador', 'Mira Montes: onze tentativas de aprender uma profissão', [915], [],
     lambda e: e['actor_id'] == 915 and e['kind'].startswith(('Training', 'Profession')) and 685 <= e['turn'] <= 5719,
     lambda a: a['npc_id'] == 915 and a['goal']['action'] == 'train' and a['turn'] in (685, 4478, 4917)),
    ('S10', 'mundo', 'Bela Solaris: habitante abstrato torna-se aprendiz persistente', [152312], [],
     lambda e: e['actor_id'] == 152312 and e['kind'] in ('WorkerMaterialized', 'TrainingStarted', 'TrainingProgress', 'ProfessionChanged'),
     lambda a: a['npc_id'] == 152312 and a['goal']['action'] == 'train' and a['turn'] in (865, 961)),
    ('S11', 'jogador', 'Iria pede água; o jogador aceita, mas a quest expira', [38, 41, 7676],
     [1507116, 1507428], lambda e: False,
     lambda a: a['npc_id'] == 38 and a['turn'] == 9514),
    ('S12', 'jogador', 'Arthus Valerius recebe a ração e come na hora seguinte', [24, 7676],
     [18732], lambda e: False, lambda a: False),
]


def trim_action(a):
    need = a.get('need')
    source = need['context'].get('source_event') if need else None
    facts = a['knowledge_before']
    targets = {a['goal']['target_id'], need['target_id'] if need else None}
    return {k: v for k, v in a.items() if k not in ('knowledge_before', 'observations_before')} | {
        'source_fact_known_before': next((f for f in facts if f['event_id'] == source), None),
        'known_related_facts_before': [f for f in facts if f['actor_id'] in targets or f['target_id'] in targets],
        'known_fact_ids_before': [f['event_id'] for f in facts],
        'target_observation_before': a.get('observations_before', {}).get(str(need['target_id'])) if need else None,
    }


def main():
    catalogue = []
    for mode in ('jogador', 'espectador', 'mundo'):
        directory = OUT / 'auditorias' / mode
        world = loads((directory / 'save_final.json').read_text())
        cast = json.loads((directory / 'elenco_completo.json').read_text())
        initial = {c['id']: c for c in cast['characters']}
        events = list(rows(directory / 'narrativa.jsonl.gz'))
        by_id = {e['id']: e for e in events}
        actions = list(rows(directory / 'acoes_pessoais.jsonl.gz'))
        actions.extend(rows(OUT / 'replay_acoes' / f'{mode}.jsonl.gz'))
        player_commands = [json.loads(line) for line in (directory / 'acoes.jsonl').read_text().splitlines()] if mode == 'jogador' else []
        for sid, m, title, people, ids, event_filter, action_filter in STORIES:
            if m != mode:
                continue
            assert all(i in by_id for i in ids), (sid, set(ids) - by_id.keys())
            # Uma ação de status/ascensão pode existir nas duas capturas observacionais.
            selected_actions = list({(a['npc_id'], a['turn'], a['goal']['id']): a
                                     for a in actions if action_filter(a)}.values())
            # Fonte atual da necessidade, e não somente o seu created_at original.
            extra_sources = {a['need']['context'].get('source_event') for a in selected_actions if a.get('need')}
            selected_events = sorted([e for e in events if e['id'] in set(ids) | extra_sources or event_filter(e)], key=lambda e: (e['turn'], e['id']))
            characters = []
            for i in people:
                c = world.characters[i]
                characters.append({
                    'id': i, 'name': c.name, 'initial': initial.get(i),
                    'final_profession': c.profession, 'alive': c.alive,
                    'health': c.health, 'hunger': c.hunger, 'money': c.money,
                    'death_record': world.death_records.get(i),
                    'origin': c.origin,
                    'applied_selected_facts': {str(e['id']): asdict(c.applied_facts[e['id']])
                        for e in selected_events if e['id'] in c.applied_facts},
                    'final_selected_facts_known': [asdict(c.knowledge[e['id']]) for e in selected_events if e['id'] in c.knowledge],
                })
            related = [asdict(r) for r in world.relationships.values() if r.source_id in people and r.target_id in people]
            story = {'id': sid, 'mode': mode, 'title': title,
                     'characters': characters, 'relationships': related,
                     'events': selected_events,
                     'actions': sorted([trim_action(a) for a in selected_actions], key=lambda a: (a['turn'], a['npc_id'])),
                     'source_streams': [str(directory/'narrativa.jsonl.gz'), str(directory/'acoes_pessoais.jsonl.gz'), str(OUT/'replay_acoes'/f'{mode}.jsonl.gz')]}
            if sid == 'S11':
                story['quest'] = asdict(world.quests[1507427])
                story['player_commands'] = [a for a in player_commands if 9514 <= a['turn_before'] <= 9561]
                assert not any(a['command'].startswith('entregar') for a in story['player_commands'])
            if sid == 'S12':
                story['player_commands'] = [a for a in player_commands if a['turn_before'] == 100]
                story['feeding_events'] = [r for r in rows(directory/'alimentacao.jsonl.gz') if r['npc_id'] == 24 and 100 <= r['turn'] <= 102]
                assert any(r['kind'] == 'FoodConsumed' and r['acquired_turn'] == 100 for r in story['feeding_events'])
            catalogue.append(story)
    catalogue.sort(key=lambda s: s['id'])
    (OUT/'historias_evidencias.json').write_text(json.dumps(catalogue, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps([{'id': s['id'], 'mode': s['mode'], 'events': len(s['events']),
                      'actions': len(s['actions']), 'event_kinds': dict(Counter(e['kind'] for e in s['events']))}
                     for s in catalogue], ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
