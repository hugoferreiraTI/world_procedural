import json
from collections import Counter
from pathlib import Path
from procedural.generation import generate_world
from procedural.engine import Engine
from procedural.navigation import distance
w=generate_world('Dovha',with_player=False); e=Engine(w)
meals={}; drinks={}; actions={}; deaths=[]; original=e.goals.execute
def execute(c,g,h):
    result=original(c,g,h)
    if result[0]:
        actions[c.id]={'action':g.action,'turn':w.turn}
        if g.action=='eat': meals[c.id]=w.turn
        if g.action in ('drink','drink_well','drink_stream'): drinks[c.id]=w.turn
    return result
e.goals.execute=execute
def died(event):
    c=w.characters[event.target_id]
    sources=[p for key,p in c.known_places.items() if key.startswith('well') or key=='market']
    deaths.append({'id':c.id,'turn':w.turn,'health':c.health,'hunger':c.hunger,'thirst':c.thirst,'fatigue':c.fatigue,
      'food':e.items.count(c.id,'food'),'water':e.items.count(c.id,'water'),'last_meal':meals.get(c.id),
      'last_drink':drinks.get(c.id),'last_action':actions.get(c.id),'goal':c.goal.action if c.goal else None,
      'water_distance':min((distance(c.position,p) for p in sources),default=None)})
e.bus.subscribe('CharacterDied',died)
e.simulate(1000)
a=Counter('both' if d['hunger']>=100 and d['thirst']>=100 else 'thirst' if d['thirst']>=100 else 'hunger' for d in deaths)
Path('../agua_baseline_1000.json').write_text(json.dumps({'seed':'Dovha','turns':1000,'rules':'mvp-3','deaths_by_condition':dict(a),'deaths':deaths},ensure_ascii=False,indent=2))
print(dict(a))
