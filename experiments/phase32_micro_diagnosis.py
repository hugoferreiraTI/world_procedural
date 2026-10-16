"""Reproduções controladas das causas, em mundos descartáveis; não são correções."""
from dataclasses import asdict
import json
import math
from pathlib import Path

from procedural.engine import Engine
from procedural.generation import generate_world, GenerationConfig
from procedural.models import Fact, Goal, Observation, Personality
from procedural.persistence import dumps, loads

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'reports/fase_3_2_diagnostico'


def main():
    baseline = dumps(generate_world('DiagnosticoFase32', with_player=False,
                                   config=GenerationConfig(kingdom_count=1, historical_turns=0)))
    def stock(e, town, kind, amount):
        old = e.items.count(town.id, kind)
        if old:
            e.items.consume(town.id, kind, old)
        if amount:
            e.items.create(town.id, kind, amount)
    def fixture(profession='agricultor'):
        e = Engine(loads(baseline));e.world.turn = 100
        p = next(c for c in e.world.characters.values() if c.profession == profession)
        t = e.world.towns[p.town_id]
        e.navigation.relocate(p,t.market)
        p.money, p.health, p.hunger, p.thirst, p.fatigue = 0,100,30,0,0
        p.needs.clear();p.goal=None;p.observations.clear();p.knowledge.clear();p.failures.clear()
        p.personality=Personality(honesty=100,compassion=0,courage=90,independence=0,
                                  greed=0,diligence=0,family_loyalty=0,persistence=0,
                                  temperament=0,vengefulness=0,ambition=0)
        e.needs.personal.kin[p.id]=set()
        q=e.items.count(p.id,'food')
        if q:e.items.consume(p.id,'food',q)
        p.food_state.clear();p.financial_since=100;p.wage_credit=0
        t.money=500;t.economic_report={}
        stock(e,t,'food',100);stock(e,t,'grain',10)
        return e,p,t
    result={}

    # A segunda ração não pode financiar trabalho sob a necessidade de reserva,
    # embora o ramo geral de money ainda possa oferecer trabalho.
    gaps=[]
    for owned in (0,1):
        e,p,t=fixture()
        if owned:e.items.create(p.id,'food',owned)
        e.economy.observe(p)
        n=next(n for n in e.needs.refresh(p) if n.kind=='food_reserve')
        choices=e.goals.solutions(p,n)
        gaps.append({'owned':owned,'money':p.money,'known_unaffordable':e.economy.known_unaffordable(p),
                     'reserve_priority':n.priority,'candidate_actions':[c.action for c in choices]})
    assert 'work' in gaps[0]['candidate_actions'] and 'work' not in gaps[1]['candidate_actions']
    result['work_for_reserve_disappears_with_one_ration']=gaps

    # A oferta geral não consulta a demanda de distribuição já atendida.
    e,p,t=fixture()
    t.economic_report={'stock':{'food':100},'expected_demand':10,'bottlenecks':['AFFORDABILITY_PROBLEM']}
    t.meals_served_today=math.ceil((t.abstract_population or 0)/120)
    e.economy.observe(p)
    n=next(n for n in e.needs.refresh(p) if n.kind=='food_reserve')
    offered=any(c.action=='temporary_service' for c in e.goals.solutions(p,n))
    before=e.items.count(t.id,'food')
    done=e.professions.temporary_service(p,1)
    assert offered and not done[0] and before==e.items.count(t.id,'food')
    result['temporary_service_advertised_after_daily_demand_filled']={
        'offered':offered,'municipal_food':before,'daily_demand':t.meals_served_today,'result':done}

    # Produzir uma ração com restos rende 2/6 de moeda, não uma moeda inteira.
    e,p,t=fixture('cozinheiro');stock(e,t,'grain',1)
    e.navigation.relocate(p,p.workplace)
    need=e.needs.ensure(p,'money',60,'fixture','Renda',None)
    goal=Goal(e.world.allocate_id(),need.id,'work',60,e.world.turn)
    before_food=e.items.count(t.id,'food');before_cash=t.money+p.money
    done=e.goals.execute(p,goal,1)
    assert not done[0] and p.wage_credit==2 and e.items.count(t.id,'food')==before_food+1
    assert t.money+p.money==before_cash
    result['productive_work_flagged_as_failure_with_fractional_wage']={
        'food_produced':e.items.count(t.id,'food')-before_food,'money_paid':p.money,
        'wage_credit_sixths':p.wage_credit,'municipal_cash':t.money,'result':done,
        'money_conserved':True,'note':'O decide aplica cooldown de 12h após resultado falso; execute isolado não aplica esse cooldown.'}

    # O culpado conhecido, mesmo com pouca reputação, permanece candidato.
    e,p,t=fixture()
    guard=next(c for c in e.world.characters.values() if c.town_id==t.id and c.profession=='guarda')
    e.navigation.relocate(guard,p.position)
    p.observations[guard.id]=Observation(100,guard.position,30,0,100,True,'guarda')
    fact=Fact(e.world.allocate_id(),'ItemStolen',guard.id,t.id,guard.position,100,'Crime controlado.',source_kind='direct')
    e.knowledge.learn(p,fact,True)
    need=e.needs.personal.create(p,'revenge',guard.id,60,f'event:{fact.event_id}','Reparação',100,
        {'source_event':fact.event_id,'culprit':guard.id,'victim':t.id,'known_location':asdict(guard.position)})
    candidates=e.personal_actions.candidates(p,need)
    assert ('denounce',guard.position,guard.id) in candidates
    goal=Goal(e.world.allocate_id(),need.id,'denounce',60,100,target_id=guard.id)
    done=e.personal_actions.execute(p,goal,need)
    assert done[0] and need.status=='satisfied'
    result['suspect_guard_is_valid_report_recipient']={
        'reporter_id':p.id,'culprit_id':guard.id,'recipient_id':goal.target_id,
        'candidate_exists':True,'result':done,'need_status':need.status}

    # Informar retorna sucesso mesmo quando aprender o fato já conhecido seria noop.
    e,p,t=fixture()
    helper=next(c for c in e.world.characters.values() if c.town_id==t.id and c.profession=='guarda')
    relative=next(c for c in e.world.characters.values() if c.town_id==t.id and c.id not in (p.id,helper.id))
    e.navigation.relocate(helper,p.position)
    old=Fact(e.world.allocate_id(),'PersonLocated',helper.id,relative.id,p.position,30,
             'Localização antiga controlada.',source_kind='direct',context={'hunger':30,'health':100,'thirst':0})
    e.knowledge.learn(helper,old,True);e.knowledge.learn(p,old,True)
    need=e.needs.personal.create(p,'family',relative.id,60,'fixture','Ausência atual',72,
        {'mode':'missing','last_seen':70,'known_location':asdict(p.position),'searched':True})
    transmitted=e.knowledge.transmitted(old,helper,p)
    duplicate_learn=e.knowledge.learn(p,transmitted,False)
    goal=Goal(e.world.allocate_id(),need.id,'ask_personal_help',60,100,target_id=helper.id)
    done=e.personal_actions.execute(p,goal,need)
    assert not duplicate_learn and done[0] and need.status not in ('satisfied','expired')
    result['stale_already_known_location_still_returns_success']={
        'source_fact_turn':30,'last_seen':70,'need_created_at':need.created_at,
        'duplicate_learn_changed_fact':duplicate_learn,'execution_result':done,'need_status':need.status,
        'information_shared_events':sum(ev.kind=='InformationShared' for ev in e.world.events)}

    OUT.mkdir(exist_ok=True)
    (OUT/'microdiagnosticos.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(result,ensure_ascii=False,indent=2))


if __name__=='__main__':main()
