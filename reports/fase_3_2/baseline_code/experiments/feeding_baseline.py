"""Mede a alimentação anterior sem modificar seus saves, decisões ou RNG."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'reports/correcao_alimentar'
# Executado como arquivo: os imports abaixo carregam o motor anterior preservado.
sys.path.insert(0, str(OUT/'baseline_code'))
from procedural.engine import Engine
from procedural.generation import generate_world
from procedural.persistence import dumps


class BaselineObserver:
    def __init__(self, engine):
        self.e = engine
        self.state = {}
        self.sums, self.counts = Counter(), Counter()
        self.frames = []
        self.last_frame = None
        self.start = engine.world.turn
        engine.goals.debug = True
        decide = engine.goals.decide
        execute = engine.goals.execute

        def decision(person, elapsed=1):
            before = (person.hunger, person.health, engine.items.count(person.id, 'food'))
            decide(person, elapsed)
            trace = engine.goals.traces.get(person.id, {})
            if trace.get('turn') == engine.world.turn and trace.get('need') == 'food' and trace.get('selected') != 'eat':
                s = self.state.setdefault(person.id, {'queue': []})
                if s.get('search') is None:
                    s['search'] = engine.world.turn
                    self.add('HungerAtFoodSearchStart', before[0])
                    self.add('HPAtFoodSearchStart', before[1])
                    self.add('FoodOwnedAtSearchStart', before[2])
        engine.goals.decide = decision

        def execution(person, goal, hours):
            if not person.is_player and goal.action != 'eat':
                need = next((n for n in person.needs.values() if n.id == goal.need_id), None)
                s = self.state.setdefault(person.id, {'queue': []})
                if need and need.kind == 'food' and s.get('search') is None:
                    s['search'] = engine.world.turn
                    self.add('HungerAtFoodSearchStart', person.hunger)
                    self.add('HPAtFoodSearchStart', person.health)
                    self.add('FoodOwnedAtSearchStart', engine.items.count(person.id, 'food'))
            return execute(person, goal, hours)
        engine.goals.execute = execution

        create, transfer, consume = engine.items.create, engine.items.transfer, engine.items.consume

        def creation(owner_id, kind, quantity=1, **kwargs):
            result = create(owner_id, kind, quantity, **kwargs)
            if kind == 'food':self.acquired(owner_id, quantity)
            return result

        def movement(source, target, item_id, quantity=1):
            kind = engine.world.items[item_id].kind
            result = transfer(source, target, item_id, quantity)
            if kind == 'food':
                self.removed(source, quantity, False)
                self.acquired(target, quantity)
            return result

        def consumption(owner_id, kind, quantity=1):
            result = consume(owner_id, kind, quantity)
            if result and kind == 'food':self.removed(owner_id, quantity, True)
            return result
        engine.items.create, engine.items.transfer, engine.items.consume = creation, movement, consumption

    def add(self, name, value):
        self.sums[name] += value;self.counts[name] += 1

    def acquired(self, owner, quantity):
        person = self.e.world.characters.get(owner)
        if person is None or person.is_player:return
        s = self.state.setdefault(owner, {'queue': []})
        search = s.get('search')
        s['queue'].append({'turn': self.e.world.turn, 'quantity': quantity, 'search': search})
        self.add('HungerAtAcquisition', person.hunger);self.add('HPAtAcquisition', person.health)
        if search is not None:self.add('TimeFromSearchToAcquisition', self.e.world.turn-search)

    def removed(self, owner, quantity, eaten):
        person = self.e.world.characters.get(owner)
        if person is None or person.is_player:return
        s = self.state.setdefault(owner, {'queue': []})
        queue = s['queue']
        old = max(0, self.e.items.count(owner, 'food')+quantity-sum(b['quantity'] for b in queue))
        remaining = max(0, quantity-old)
        while remaining and queue:
            batch = queue[0];used = min(remaining, batch['quantity'])
            if eaten:
                self.add('TimeFromAcquisitionToConsumption', self.e.world.turn-batch['turn'])
                if batch['search'] is not None:self.add('TimeFromSearchToConsumption', self.e.world.turn-batch['search'])
            batch['quantity'] -= used;remaining -= used
            if not batch['quantity']:queue.pop(0)
        if eaten:
            self.add('HungerAtConsumption', person.hunger);self.add('HPAtConsumption', person.health)
            self.add('NutritionUsed', min(person.hunger, 40))
            s['search'] = None

    def frame(self):
        elapsed = self.e.world.turn-self.start
        if elapsed%250 or elapsed == self.last_frame:return
        self.last_frame = elapsed
        people = [c for c in self.e.world.characters.values() if c.alive and not c.is_player]
        owned = [self.e.items.count(c.id, 'food') for c in people]
        self.frames.append({'elapsed': elapsed, 'alive_npcs': len(people),
                            'maintaining_two_rations': sum(q >= 2 for q in owned),
                            'maintaining_reserve_percent': 100*sum(q >= 2 for q in owned)/len(people),
                            'average_personal_food': sum(owned)/len(people),
                            'municipal_food_total': sum(self.e.items.count(t.id, 'food') for t in self.e.world.towns.values())})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mode', required=True, choices=('jogador', 'espectador', 'mundo'))
    args = parser.parse_args()
    mode = args.mode
    base = ROOT/'reports/fase_3/auditorias'/mode
    engine = Engine(generate_world('Mira' if mode == 'mundo' else 'Dovha', 'Auditor', with_player=mode == 'jogador'))
    observer = BaselineObserver(engine);observer.frame()
    if mode == 'jogador':
        for line in (base/'acoes.jsonl').read_text().splitlines():
            action = json.loads(line)
            assert engine.world.turn == action['turn_before']
            result = engine.execute(action['command'])
            assert result.success == action['success'] and engine.world.turn == action['turn_after']
            observer.frame()
    else:
        for i in range(10000):
            engine.step();observer.frame()
            if (i+1)%2500 == 0:print(mode, i+1, flush=True)
    checksum = hashlib.sha256(dumps(engine.world).encode()).hexdigest()
    assert checksum == hashlib.sha256((base/'save_final.json').read_bytes()).hexdigest()
    result = {'mode': mode, 'identical_original_save': True, 'save_sha256': checksum,
              'means': {k: observer.sums[k]/observer.counts[k] for k in observer.sums},
              'counts': dict(observer.counts), 'frames': observer.frames}
    directory = OUT/'baseline_medicoes';directory.mkdir(exist_ok=True)
    (directory/f'{mode}.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'frames'}, ensure_ascii=False), flush=True)


if __name__ == '__main__':main()
