"""Cenários dirigidos A–G: fixtures explícitas, não histórias espontâneas."""
from pathlib import Path
import sys,json
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'tests'))
from test_phase3 import Phase3Tests
from dataclasses import asdict

def fixture():
    f=Phase3Tests();f.setUp();return f

def main():
    data={}
    for label in ('A','B','C','D','E','F','G'):
        f=fixture()
        if label in ('B','G'): f.die(f.cook)
        if label=='C':
            f.stock('food',200);f.farmer.money=1
            f.engine.items.consume(f.farmer.id,'food',f.engine.items.count(f.farmer.id,'food'))
        if label=='D': f.farmer.money=1
        if label=='E': f.food_choices(12)
        if label=='F':
            f.town.population=9000;f.town.abstract_population=9000-len(f.people)
        before=f.report();f.engine.economy.daily()
        result={'initial_diagnosis':before,'collective_action':f.town.goal.action,
                'professional_demand':dict(f.town.professional_demand)}
        if label in ('D','E'):
            f.engine.navigation.relocate(f.farmer,f.farmer.workplace if label=='D' else f.town.market)
            f.engine.economy.observe(f.farmer)
            if label=='D':
                need=next(n for n in f.engine.needs.refresh(f.farmer) if n.kind=='money')
            else: need=f.farmer.needs['food']
            result['alternatives']=[s.action for s in f.engine.goals.solutions(f.farmer,need)]
        if label=='G':
            events=[]
            f.engine.bus.subscribe('*',lambda e:events.append(asdict(e)) if e.kind in
                ('TrainingStarted','ProfessionChanged','WorkerMaterialized','LocalEconomicResponse') else None)
            f.engine.simulate(240)
            result['observed_240_hours']=events
            result['final_diagnosis']=f.report()
        data[label]=result
    p=ROOT/'reports/fase_3/cenarios_dirigidos.json'
    p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    print({k:v['collective_action'] for k,v in data.items()})

if __name__=='__main__':main()
