"""Auditoria alimentar e narrativa, com regras congeladas e observação local."""
import argparse
from collections import Counter
from dataclasses import asdict
import gzip
import hashlib
import json
from pathlib import Path

from experiments import phase3_audit
from experiments.perspective_audit import NARRATIVE_EVENTS, write_json
from procedural.personal import PERSONAL_KINDS

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'reports/correcao_alimentar'
NARRATIVE = NARRATIVE_EVENTS | phase3_audit.ECONOMIC_EVENTS


def core_hash():
    return hashlib.sha256(b''.join(p.read_bytes() for p in sorted((ROOT/'procedural').glob('*.py')))).hexdigest()


class FeedingAudit(phase3_audit.Phase3Audit):
    def __init__(self, directory, mode):
        super().__init__(directory, mode)
        self.feeding_stream = gzip.open(directory/'alimentacao.jsonl.gz', 'wt', encoding='utf-8')
        self.narrative_stream = gzip.open(directory/'narrativa.jsonl.gz', 'wt', encoding='utf-8')
        self.personal_stream = gzip.open(directory/'acoes_pessoais.jsonl.gz', 'wt', encoding='utf-8')
        self.last_reserve_frame = None
        self.reserve_frames = []
        self.installed = False

    @staticmethod
    def line(stream, row):
        stream.write(json.dumps(row, ensure_ascii=False, separators=(',', ':'))+'\n')

    def __call__(self, engine):
        super().__call__(engine)
        if not self.installed:
            self.installed = True
            engine.feeding.listeners.append(lambda row: self.line(self.feeding_stream, row))
            write_json(self.directory/'elenco_completo.json', {
                'start_turn': engine.world.turn,
                'characters': [{'id': c.id, 'name': c.name, 'town_id': c.town_id,
                                'profession': c.profession, 'is_player': c.is_player,
                                'personality': asdict(c.personality)} for c in engine.world.characters.values()],
                'relationships': [asdict(r) for r in engine.world.relationships.values()],
                'towns': [{'id': t.id, 'name': t.name} for t in engine.world.towns.values()]})
            original = engine.goals.execute

            def execution(person, goal, hours):
                need = next((n for n in person.needs.values() if n.id == goal.need_id), None)
                record = None
                if need and need.kind in PERSONAL_KINDS:
                    # Captura ANTES da ação: não atribui conhecimento adquirido depois.
                    record = {'turn': engine.world.turn, 'npc_id': person.id, 'goal': asdict(goal),
                              'need': asdict(need), 'knowledge_before': [asdict(f) for f in person.knowledge.values()],
                              'observations_before': {str(i): asdict(o) for i, o in person.observations.items()},
                              'health': person.health, 'hunger': person.hunger}
                result = original(person, goal, hours)
                if record is not None:
                    record.update(success=result[0], outcome=result[1])
                    self.line(self.personal_stream, record)
                return result

            engine.goals.execute = execution
        elapsed = engine.world.turn-self.start
        if elapsed % 250 == 0 and self.last_reserve_frame != elapsed:
            self.last_reserve_frame = elapsed
            people = [c for c in engine.world.characters.values() if c.alive and not c.is_player]
            owned = [engine.items.count(c.id, 'food') for c in people]
            maintained = sum(q >= engine.feeding.reserve_target(c) for c, q in zip(people, owned))
            self.reserve_frames.append({'turn': engine.world.turn, 'elapsed': elapsed,
                'alive_npcs': len(people), 'maintaining_reserve': maintained,
                'maintaining_reserve_percent': 100*maintained/len(people) if people else 0,
                'average_personal_food': sum(owned)/len(people) if people else 0,
                'personal_food_total': sum(owned),
                'municipal_food_total': sum(engine.items.count(t.id, 'food') for t in engine.world.towns.values()),
                'reserve_histogram': dict(Counter(owned))})

    def on_event(self, event):
        super().on_event(event)
        if event.kind not in NARRATIVE:
            return
        world = self.engine.world
        receivers = []
        for i in event.witnesses:
            person = world.characters.get(i)
            fact = person.knowledge.get(event.id) if person else None
            if fact:
                receivers.append({'id': i, 'confidence': fact.confidence, 'source_kind': fact.source_kind,
                    'needs_from_event': [asdict(n) for n in person.needs.values()
                                         if n.context.get('source_event') == event.id]})
        self.line(self.narrative_stream, {**asdict(event), 'knowledge_at_event': receivers})

    def finish(self, report):
        self.feeding_stream.close();self.narrative_stream.close();self.personal_stream.close()
        write_json(self.directory/'quadros_reserva.json', self.reserve_frames)
        world = self.engine.world
        metrics = {key: value-self.initial.get(key, 0) for key, value in world.metrics.items()}
        means = {}
        for key, value in metrics.items():
            if key.startswith('Feeding:') and key.endswith(':sum'):
                count = metrics.get(key[:-3]+'count', 0)
                means[key[len('Feeding:'):-len(':sum')]] = value/count if count else None
        records = [r for r in world.death_records.values() if r['turn'] >= self.start]
        people = [c for c in world.characters.values() if not c.is_player]
        carried = [c for c in people if not c.alive and c.id in world.death_records and
                   world.death_records[c.id]['turn'] >= self.start and world.death_records[c.id]['food'] > 0]
        hungry_carried = [c for c in carried if world.death_records[c.id]['cause'] in ('hunger', 'both')]
        fresh = [c for c in hungry_carried if c.food_state.get('last_acquisition') == world.death_records[c.id]['turn']-1
                 and c.food_state.get('food_before_decision') == 0]
        prior = [c for c in hungry_carried if c.food_state.get('food_before_decision', 0) > 0]
        result = {'mode': self.mode, 'turns': world.turn-self.start, 'means': means,
                  'death_conditions': dict(Counter(r['cause'] for r in records)),
                  'deaths_with_food_any_cause': len(carried), 'hunger_deaths_with_food': len(hungry_carried),
                  'hunger_deaths_fresh_acquisition': len(fresh), 'hunger_deaths_prior_food': len(prior),
                  'fresh_ids': [c.id for c in fresh], 'prior_ids': [c.id for c in prior],
                  'final_reserve': self.reserve_frames[-1],
                  'emergency_interruptions': metrics.get('EmergencyGoalInterrupted', 0),
                  'slow_rejections': metrics.get('FeedingRejected:SolutionTooSlow', 0),
                  'nutrition_mean': means.get('NutritionUsed'),
                  'terminal_food_state': {str(c.id): c.food_state for c in carried}}
        write_json(self.directory/'metricas_alimentacao.json', result)
        super().finish(report)
        print(json.dumps(result | {'terminal_food_state': 'ver arquivo'}, ensure_ascii=False), flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mode', required=True, choices=('jogador', 'espectador', 'mundo'))
    parser.add_argument('--turnos', type=int, default=10000)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    manifest = json.loads((OUT/'manifesto_auditoria.json').read_text())
    assert core_hash() == manifest['core_sha256'], 'Motor diferente do manifesto congelado.'
    directory = args.output or OUT/'auditorias'/args.mode
    if directory.exists() and any(directory.iterdir()):
        raise ValueError('A auditoria não sobrescreve uma campanha existente.')
    old = phase3_audit.Phase3Audit
    phase3_audit.Phase3Audit = FeedingAudit
    try:
        phase3_audit.run('Mira' if args.mode == 'mundo' else 'Dovha', args.turnos, directory, args.mode)
    finally:
        phase3_audit.Phase3Audit = old
    assert core_hash() == manifest['core_sha256'], 'As regras mudaram durante a execução.'


if __name__ == '__main__':
    main()
