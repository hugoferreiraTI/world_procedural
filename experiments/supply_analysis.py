"""Diagnóstico somente de leitura dos saves das três perspectivas."""
from collections import Counter
import hashlib
import json
import math
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from procedural.persistence import loads


def inspect(path):
    raw = path.read_bytes()
    world = loads(raw.decode())
    def count(owner, kind):
        return sum(q for i, q in owner.inventory.items() if world.items[i].kind == kind)
    towns = []
    for town in world.towns.values():
        residents = [world.characters[i] for i in town.resident_ids]
        alive = [c for c in residents if c.alive and not c.is_player]
        stock = {k: count(town, k) for k in ('food', 'grain', 'water', 'iron', 'wood')}
        expected = max(8, town.population // 100)
        price = max(2, math.ceil(3 * (max(.45, min(4, expected / max(1, stock['food'])))
                    + min(1, town.demand.get('food', 0) / 20)) * 1.1))
        poor = [dict(id=c.id, name=c.name, profession=c.profession, money=c.money,
                     hunger=round(c.hunger, 2), thirst=round(c.thirst, 2),
                     carried_food=count(c, 'food')) for c in alive if c.money < price]
        towns.append(dict(id=town.id, name=town.name, population=town.population,
            abstract_population_current_formula=max(0, town.population-len(town.resident_ids)),
            abstract_daily_food_requirement=max(1, math.ceil(max(0, town.population-len(town.resident_ids))/120)),
            stock=stock, money=town.money, abstract_money=town.abstract_money, food_price=price,
            alive=len(alive), alive_professions=dict(Counter(c.profession for c in alive)),
            dead_professions=dict(Counter(c.profession for c in residents if not c.alive)),
            cannot_afford_one_food=poor))
    alive = [c for c in world.characters.values() if c.alive and not c.is_player]
    dead = [c for c in world.characters.values() if not c.alive and not c.is_player]
    empty = [t for t in towns if t['stock']['food'] == 0]
    return dict(path=str(path.relative_to(ROOT)), sha256=hashlib.sha256(raw).hexdigest(),
        turn=world.turn, summary=dict(alive=len(alive), dead=len(dead), towns=len(towns),
            empty_food=len(empty), empty_food_with_grain=sum(t['stock']['grain']>=2 for t in empty),
            empty_food_with_full_grain=sum(t['stock']['grain']>=240 for t in empty),
            empty_food_without_live_cook=sum(not t['alive_professions'].get('cozinheiro',0) for t in empty),
            empty_food_with_live_cook=sum(bool(t['alive_professions'].get('cozinheiro',0)) for t in empty),
            full_grain=sum(t['stock']['grain']>=240 for t in towns),
            towns_with_food_and_unaffordable_residents=sum(t['stock']['food']>0 and bool(t['cannot_afford_one_food']) for t in towns),
            towns_with_food_at_least_100_and_unaffordable_residents=sum(t['stock']['food']>=100 and bool(t['cannot_afford_one_food']) for t in towns),
            towns_with_zero_money=sum(t['money']==0 for t in towns),
            towns_without_alive_residents=sum(t['alive']==0 for t in towns),
            alive_money_below_10=sum(c.money<10 for c in alive),
            alive_money_zero=sum(c.money==0 for c in alive),
            alive_hunger_or_thirst_at_least_70=sum(max(c.hunger,c.thirst)>=70 for c in alive),
            dead_carrying_food=sum(count(c,'food')>0 for c in dead),
            dead_carrying_water=sum(count(c,'water')>0 for c in dead)), towns=towns)


def main():
    result = {}
    for mode in ('jogador','espectador','mundo'):
        result[mode] = [inspect(ROOT/'reports'/'tres_perspectivas_20261007'/mode/name)
                       for name in ('save_1000.json','save_5000.json','save_final.json')]
    destination = ROOT/'reports'/'analise_abastecimento'/'evidencias.json'
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
    for mode, snapshots in result.items():
        print(mode, json.dumps([{'turn':s['turn'], **s['summary']} for s in snapshots], ensure_ascii=False))
        final = snapshots[-1]
        filters = {
            'trigo cheio e comida vazia': lambda t: t['stock']['food']==0 and t['stock']['grain']>=240,
            'muita comida, falta dinheiro': lambda t: t['stock']['food']>=100 and t['cannot_afford_one_food'],
            'comida vazia com cozinheiro vivo': lambda t: t['stock']['food']==0 and t['alive_professions'].get('cozinheiro'),
        }
        for label, predicate in filters.items():
            examples = [t for t in final['towns'] if predicate(t)]
            print(label, json.dumps(examples[:1], ensure_ascii=False))


if __name__ == '__main__':
    main()
