"""Observa 1.000 horas canônicas sem alterar regras, decisões ou aleatoriedade."""
import argparse
from collections import Counter, defaultdict
from dataclasses import asdict
import gzip
import hashlib
import json
from pathlib import Path

from experiments.feeding_audit import core_hash
from procedural.engine import Engine
from procedural.generation import generate_world
from procedural.persistence import dumps

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT/'reports/correcao_alimentar'
OUT = ROOT/'reports/fase_3_2_diagnostico'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mode', required=True, choices=('jogador', 'espectador', 'mundo'))
    mode = parser.parse_args().mode
    original_hash = core_hash()
    assert original_hash == json.loads((BASE/'manifesto_auditoria.json').read_text())['core_sha256']
    engine = Engine(generate_world('Mira' if mode == 'mundo' else 'Dovha', 'Auditor', with_player=mode == 'jogador'))
    engine.goals.debug = True
    OUT.mkdir(exist_ok=True)
    counts, by_selected, by_first, healthy_first = Counter(), Counter(), Counter(), Counter()
    wage_counts, execution_counts, failures = Counter(), Counter(), Counter()
    example_counts = Counter()
    context = None
    with gzip.open(OUT/f'{mode}_amostras.jsonl.gz', 'wt', encoding='utf-8') as stream:
        def sample(category, row):
            if example_counts[category] < 12:
                stream.write(json.dumps({'category': category, **row}, ensure_ascii=False, separators=(',', ':'))+'\n')
                example_counts[category] += 1

        original_refresh = engine.needs.refresh
        def refresh(person):
            active = original_refresh(person)
            if context is not None and person.id == context['npc_id']:
                context['active'] = [{'id': n.id, 'kind': n.kind, 'priority': n.priority,
                    'base': n.base_urgency, 'age': min(8, (engine.world.turn-n.created_at)*.15),
                    'emergency': n.context.get('emergency', False)} for n in active]
            return active
        engine.needs.refresh = refresh

        original_solutions = engine.goals.solutions
        def solutions(person, need):
            choices = original_solutions(person, need)
            if context is not None and person.id == context['npc_id']:
                context['last_solutions_need'] = need.kind
                if context['first_need'] is None:
                    context['examined'].setdefault(need.kind, {'actions': [c.action for c in choices],
                        'rejected': [c.feeding for c in engine.goals.rejected_food.get(person.id, [])]})
            return choices
        engine.goals.solutions = solutions

        original_choose = engine.goals.choose
        def choose(choices):
            selected = original_choose(choices)
            if context is not None and context['first_need'] is None:
                context['first_need'] = context.get('last_solutions_need')
                context['first_action'] = selected.action
            return selected
        engine.goals.choose = choose

        original_count = engine.needs.count
        def count(transition, kind, owner=None):
            original_count(transition, kind, owner)
            if context is not None and transition == 'Selected' and getattr(owner, 'id', None) == context['npc_id']:
                context['selection'] = kind
        engine.needs.count = count

        original_decide = engine.goals.decide
        def decide(person, elapsed=1):
            nonlocal context
            town = engine.world.towns[person.town_id]
            context = {'turn': engine.world.turn, 'npc_id': person.id, 'name': person.name,
                'profession': person.profession, 'hunger': person.hunger, 'fatigue': person.fatigue,
                'money': person.money, 'food_owned': engine.items.count(person.id, 'food'),
                'town_money': town.money, 'municipal_food': engine.items.count(town.id, 'food'),
                'real_local_price_for_auditor_only': engine.economy.price(town.id, 'food'),
                'previous_goal': asdict(person.goal) if person.goal else None,
                'active': [], 'examined': {}, 'first_need': None, 'selection': None}
            original_decide(person, elapsed)
            counts['npc_decisions'] += 1
            reserve = next((n for n in context['active'] if n['kind'] == 'food_reserve'), None)
            if reserve:
                counts['active_reserve_evaluations'] += 1
                by_selected[context['selection'] or 'none'] += 1
                by_first[context['first_need'] or 'none'] += 1
                if context['hunger'] < 50:
                    counts['active_reserve_hunger_below_50'] += 1
                    counts['reserve_selected_hunger_below_50'] += context['selection'] == 'food_reserve'
                    healthy_first[context['first_need'] or 'none'] += 1
                    if context['selection'] != 'food_reserve':
                        counts['healthy_reserve_lost_with_stock_and_affordable_meal'] += (
                            context['municipal_food'] > 0 and context['money'] >= context['real_local_price_for_auditor_only'])
                if context['selection'] == 'food_reserve':
                    reason = 'reserve_selected'
                    counts['reserve_preserved_by_goal_continuity'] += context['first_need'] != 'food_reserve'
                elif context['first_need'] == 'food_reserve':
                    reason = 'reserve_vetoed_by_goal_continuity'
                elif 'food_reserve' in context['examined']:
                    reason = 'reserve_without_candidate'
                else:
                    first = next((n for n in context['active'] if n['kind'] == context['first_need']), None)
                    if first and first['emergency']:
                        reason = 'unexamined_emergency_precedence'
                    elif first and first['priority'] > reserve['priority']:
                        reason = 'unexamined_higher_priority'
                    elif first and first['priority'] == reserve['priority']:
                        reason = 'unexamined_priority_tie'
                    else:
                        reason = 'unexamined_other'
                counts[reason] += 1
                context['diagnosis'] = reason
                context['final_goal'] = asdict(person.goal) if person.goal else None
                # O snapshot final pode ter consumido/recebido alimento nesta ação.
                context['food_after'] = engine.items.count(person.id, 'food')
                sample(reason, context)
                if reason.startswith('unexamined'):
                    counts['unexamined_can_afford_one_real_meal'] += (context['municipal_food'] > 0 and
                        context['money'] >= context['real_local_price_for_auditor_only'])
            context = None
        engine.goals.decide = decide

        original_wage = engine.economy.wage
        def wage(person, hours, sixths=False):
            town = engine.world.towns[person.town_id]
            before = {'turn': engine.world.turn, 'npc_id': person.id, 'profession': person.profession,
                      'town_money': town.money, 'money': person.money, 'credit': person.wage_credit,
                      'new_credit_sixths': hours if sixths else hours*6}
            due = (person.wage_credit+before['new_credit_sixths'])//6
            paid = original_wage(person, hours, sixths)
            wage_counts['calls'] += 1
            wage_counts['paid_coins'] += paid
            wage_counts['calls_no_coin_paid'] += paid == 0
            wage_counts['calls_integer_payment_due'] += due > 0
            wage_counts['calls_integer_payment_due_but_zero_paid'] += due > 0 and paid == 0
            wage_counts['calls_payment_shortfall'] += paid < due
            wage_counts['calls_town_money_zero_before'] += before['town_money'] == 0
            if paid < due:
                sample('wage_shortfall', before | {'due_coins': due, 'paid_coins': paid, 'credit_after': person.wage_credit})
            return paid
        engine.economy.wage = wage

        original_execute = engine.goals.execute
        def execute(person, goal, hours):
            before_money, before_food = person.money, engine.items.count(person.id, 'food')
            result = original_execute(person, goal, hours)
            if goal.action in ('work', 'train', 'temporary_service', 'work_for_food', 'service_meal', 'work_for_meal'):
                prefix = goal.action
                execution_counts[prefix+':attempts'] += 1
                execution_counts[prefix+':successes'] += bool(result[0])
                execution_counts[prefix+':money_gained'] += max(0, person.money-before_money)
                execution_counts[prefix+':food_inventory_gained'] += max(0, engine.items.count(person.id, 'food')-before_food)
                if not result[0]:
                    failures[prefix+':'+result[1]] += 1
                    sample('work_failure:'+prefix, {'turn':engine.world.turn, 'npc_id':person.id, 'name':person.name,
                        'profession':person.profession, 'goal':asdict(goal), 'hours_requested':hours,
                        'money_before':before_money, 'food_before':before_food, 'result':result,
                        'town_money':engine.world.towns[person.town_id].money})
            return result
        engine.goals.execute = execute

        if mode == 'jogador':
            for line in (BASE/'auditorias'/mode/'acoes.jsonl').read_text().splitlines():
                if engine.world.turn >= 1024:
                    break
                a = json.loads(line)
                assert engine.world.turn == a['turn_before']
                result = engine.execute(a['command'])
                assert result.success == a['success'] and engine.world.turn == a['turn_after']
        else:
            for _ in range(1000):
                engine.step()
    expected = hashlib.sha256((BASE/'auditorias'/mode/'save_1000.json').read_bytes()).hexdigest()
    checksum = hashlib.sha256(dumps(engine.world).encode()).hexdigest()
    assert checksum == expected, (mode, checksum, expected)
    assert core_hash() == original_hash
    result = {'mode':mode, 'hours_replayed':1000, 'checkpoint_identical':True,
              'checkpoint_sha256':checksum, 'core_sha256':original_hash,
              'counts':dict(counts), 'final_selected_need_with_active_reserve':dict(by_selected),
              'first_choice_need_with_active_reserve':dict(by_first),
              'first_choice_need_with_active_reserve_and_hunger_below_50':dict(healthy_first),
              'wage_calls':dict(wage_counts), 'income_action_executions':dict(execution_counts),
              'income_action_failures':dict(failures),
              'method':'Somente envolve chamadas originais com observadores. Não recalcula needs/choices fora do fluxo nem consome RNG extra. Amostra de 1.000 horas iniciais, não extrapolada como frequência dos 10.000 turnos.'}
    (OUT/f'{mode}_replay.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps(result, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
