"""Condições observadas nas mortes remanescentes; não presume causa econômica."""
from collections import Counter, defaultdict, deque
import gzip
import json
from pathlib import Path

from procedural.persistence import loads

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'reports/correcao_alimentar'


def main():
    result = {}
    for mode in ('jogador', 'espectador', 'mundo'):
        directory = OUT/'auditorias'/mode
        world = loads((directory/'save_final.json').read_text())
        records = {i: r for i, r in world.death_records.items() if r['turn'] >= 24 and not world.characters[i].is_player}
        recent_rejections = defaultdict(lambda: deque(maxlen=40))
        deaths = []
        with gzip.open(directory/'alimentacao.jsonl.gz', 'rt') as stream:
            for line in stream:
                row = json.loads(line); npc = row['npc_id']
                if npc not in records:
                    continue
                if row['kind'] == 'FoodSolutionRejected':
                    recent_rejections[npc].append(row)
                if row['kind'] == 'DeathBeforeConsumption':
                    c = world.characters[npc]; record = records[npc]
                    seen = c.market_observation
                    quote_fresh = seen.get('town_id') == c.town_id and record['turn'] - seen.get('price_turn', -1000) <= 24
                    price = seen.get('price') if quote_fresh else None
                    deaths.append({'npc_id': npc, 'money_at_death': c.money, 'record': record,
                        'food_state_at_death': c.food_state,
                        'fresh_known_price_at_death': price,
                        'cannot_afford_fresh_known_meal': c.money < price if price is not None else None,
                        'rejections_in_last_six_hours': [r for r in recent_rejections[npc] if record['turn'] - r['turn'] <= 6]})
        assert len(deaths) == len(records)
        hunger = [d for d in deaths if d['record']['cause'] in ('hunger', 'both')]
        personal = json.loads((directory/'metricas_fase3.json').read_text())['personal_outcomes']
        result[mode] = {'summary': {
            'deaths': len(deaths), 'hunger_deaths': len(hunger),
            'hunger_deaths_with_food': sum(d['record']['food'] > 0 for d in hunger),
            'hunger_death_terminal_goals': dict(Counter(d['record']['goal'] for d in hunger)),
            'hunger_death_last_successful_actions': dict(Counter(d['record']['last_successful_action'].get('action') for d in hunger)),
            'hunger_deaths_zero_money': sum(d['money_at_death'] == 0 for d in hunger),
            'hunger_deaths_fresh_known_quote': sum(d['fresh_known_price_at_death'] is not None for d in hunger),
            'hunger_deaths_cannot_afford_fresh_known_quote': sum(d['cannot_afford_fresh_known_meal'] is True for d in hunger),
            'hunger_deaths_with_recent_slow_rejection': sum(any(r['reason'] == 'SolutionTooSlow' for r in d['rejections_in_last_six_hours']) for d in hunger),
            'active_personal_needs_closed_by_owner_death': {k.split(':')[1]: v for k, v in personal.items() if k.endswith(':OwnerDied')},
            'note': 'Condições terminais e conhecimento vigente, sem reconstrução completa de todas as causas. Cotações desconhecidas não são contadas como falta de dinheiro. Stock municipal final não é stock no turno da morte.'
        }, 'deaths': deaths}
    (OUT/'mortes_remanescentes.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps({m: r['summary'] for m, r in result.items()}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
