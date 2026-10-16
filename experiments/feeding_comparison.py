"""Comparação factual da Fase 3 com as campanhas da correção alimentar."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'reports/correcao_alimentar'
PERSONAL = {'family', 'grief', 'revenge', 'protection', 'status', 'advancement'}


def read(path):
    return json.loads(path.read_text())


def stats(directory, feeding, frames):
    economic = read(directory/'metricas_fase3.json')
    personal = read(directory/'metricas_fase2.json')
    selected = personal['selected_distribution']
    satisfied = personal['lifecycle']['Satisfied']
    return {'deaths': sum(economic['death_conditions'].values()),
            'hunger_deaths': economic['death_conditions'].get('hunger', 0)+economic['death_conditions'].get('both', 0),
            'physiological_percent': selected['physiological']/sum(selected.values())*100,
            'reserve_selections': selected.get('food_reserve', 0),
            'personal_selections': sum(selected.get(k, 0) for k in PERSONAL),
            'personal_satisfied': sum(sum(satisfied.get(k, {}).values()) for k in PERSONAL),
            'final': economic['final']['summary'],
            'trained': economic['workers_trained'], 'retrained_existing': economic['workers_retrained'],
            'materialized': economic['workers_materialized'],
            'means': feeding['means'], 'reserve_final': frames[-1],
            'average_snapshot_reserve_percent': sum(f['maintaining_reserve_percent'] for f in frames[1:])/len(frames[1:]),
            'average_snapshot_personal_food': sum(f['average_personal_food'] for f in frames[1:])/len(frames[1:]),
            'municipal_food_final': frames[-1]['municipal_food_total']}


def main():
    result = {}
    for mode in ('jogador', 'espectador', 'mundo'):
        old = ROOT/'reports/fase_3/auditorias'/mode
        new = OUT/'auditorias'/mode
        baseline = read(OUT/'baseline_medicoes'/f'{mode}.json')
        feeding = read(new/'metricas_alimentacao.json')
        a = stats(old, baseline, baseline['frames'])
        b = stats(new, feeding, read(new/'quadros_reserva.json'))
        old_death = read(ROOT/'reports/diagnostico_fome'/mode/'resumo.json')
        a.update(hunger_deaths_with_food=old_death['carrying_food'],
                 hunger_deaths_fresh_acquisition=old_death['food_acquired_in_final_decision'],
                 hunger_deaths_prior_food=old_death['food_already_present_before_final_decision'])
        b.update({k: feeding[k] for k in ('hunger_deaths_with_food', 'hunger_deaths_fresh_acquisition',
                                        'hunger_deaths_prior_food', 'emergency_interruptions', 'slow_rejections')})
        result[mode] = {'before': a, 'after': b}
    (OUT/'comparativo.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':main()
