"""Pesos e considerações normalizadas; nenhuma regra de execução aqui."""

from .rules import UTILITY
from .social import normalized

BASE = {"eat": 200, "drink": 200, "drink_well": 100, "drink_stream": 80,
        "sleep": 100, "buy_food": 75, "forage": 35, "steal": 70,
        "ask_help": 25, "work": 50, "work_for_food": 45, "secure": 70,
        "check_relative": 55, "give_supplies": 55, "seek_company": 45,
        "remember_relative": 40, "investigate": 45, "denounce": 45,
        "avoid_threat": 40, "stay_near": 35, "ask_personal_help": 25, "sell_surplus": 50}
BASE.update({"train":45,"temporary_service":45,"fill_water":100,
             "expand_farming":60,"publish_temporary_work":55,"open_training":50,
             "materialize_worker":45,"improve_utilization":55})
WEIGHTS = {"buy_food": {"honesty": 20},
           "forage": {"independence": 50, "hunter": 20},
           "steal": {"greed": 100 / 3, "honesty": -100, "courage": 10},
           "ask_help": {"compassion": 50, "trust": UTILITY.trust_weight,
                        "reputation": UTILITY.reputation_weight, "relationship": 10},
           "work": {"diligence": 50}, "work_for_food": {"diligence": 25},
           "secure": {"courage": 100 / 3},
           "check_relative": {"independence": 25, "family_loyalty": 25},
           "give_supplies": {"compassion": 35, "family_loyalty": 20},
           "seek_company": {"compassion": 20, "independence": -35, "trust": 35, "relationship": 20},
           "remember_relative": {"independence": 25, "persistence": 20},
           "investigate": {"vengefulness": 40, "courage": 40, "independence": 30,
                           "compassion": -10, "temperament": 10},
           "denounce": {"honesty": 35, "vengefulness": 20, "courage": 15, "trust": 25},
           "avoid_threat": {"courage": -40, "compassion": 15, "vengefulness": -20},
           "stay_near": {"family_loyalty": 35, "courage": 25},
           "ask_personal_help": {"independence": -30, "compassion": 20,
                                 "trust": UTILITY.trust_weight, "reputation": UTILITY.reputation_weight,
                                 "relationship": 10},
           "sell_surplus": {"greed": 30, "diligence": 20}}
WEIGHTS.update({"train":{"diligence":25,"ambition":25,"local_demand":20,"financial_pressure":20,
                         "training_cost":-10,"current_job_value":-15,"risk":-15},
                "temporary_service":{"diligence":25,"compassion":10},
                "fill_water":{"diligence":10}})

BASE.update(dict(watch_case=45,follow_lead=55,spare=50,attack=28,defend=40,flee=35,surrender=25,intervene=35,protect=35,
    confront=35,threaten=25,demand_return=40,warn=30,insult=15,apologize=25,withdraw=35,
    call_help=25,alert=35,calm=35,forgive=25,first_aid=45,seek_treatment=60,pursue=55,
    capture=115,steal_person=62,return_stolen=45,self_harm=0,migrate=55))
WEIGHTS.update({
    'spare':{'compassion':55,'honesty':20,'authority':20,'risk':20,'vengefulness':-20},
    'follow_lead':{'persistence':25,'courage':15,'vengefulness':15},
    'attack':{'anger':45,'resentment':30,'vengefulness':30,'courage':25,'risk':-55,
              'compassion':-30,'authority':-25,'low_health':-35,'defensive':25,'bond':-25},
    'defend':{'risk':25,'courage':15,'defensive':30,'injury':-10},
    'flee':{'fear':40,'risk':30,'courage':-25,'low_health':45,'injury':-20,'authority':15},
    'withdraw':{'risk':25,'compassion':15,'courage':-15,'defensive':-20},
    'surrender':{'authority':40,'risk':25,'low_health':45,'courage':-25,'defensive':-10},
    'confront':{'courage':30,'anger':15,'risk':-15,'vengefulness':15},
    'threaten':{'anger':30,'courage':20,'temperament':20,'compassion':-25,'authority':-25},
    'demand_return':{'honesty':25,'persistence':20,'courage':15},
    'warn':{'compassion':20,'honesty':15},
    'insult':{'anger':30,'humiliation':20,'temperament':15,'compassion':-35},
    'apologize':{'honesty':25,'compassion':25,'culpability':35,'anger':-25},
    'return_stolen':{'honesty':45,'compassion':20,'culpability':30,'authority':15,'greed':-20},
    'forgive':{'compassion':35,'bond':25,'vengefulness':-30,'resentment':-20},
    'calm':{'compassion':30,'bond':25,'anger':-15},
    'intervene':{'compassion':30,'courage':35,'bond':30,'risk':-25},
    'protect':{'family_loyalty':25,'compassion':25,'courage':30,'bond':30,'risk':-20},
    'first_aid':{'compassion':35,'bond':25,'diligence':15},
    'call_help':{'fear':25,'independence':-20,'injury':20},
    'alert':{'honesty':25,'risk':25,'courage':-15},
    'pursue':{'courage':20,'diligence':15,'vengefulness':20},
    'capture':{'honesty':15,'diligence':15},
    'steal_person':{'greed':40,'honesty':-90,'authority':-40,'courage':10},
    'self_harm':{'desperation':100},
    'migrate':{'independence':25,'fear':20,'financial_pressure':15,'family_loyalty':-10}})


for action in ('work', 'train', 'work_for_food', 'temporary_service'):
    WEIGHTS.setdefault(action, {})['physical_depletion'] = -35
for action in ('attack', 'threaten', 'pursue'):
    WEIGHTS.setdefault(action, {})['critical_depletion'] = -45
for action in ('sleep', 'seek_treatment'):
    WEIGHTS.setdefault(action, {})['recovery_pressure'] = 50


def evaluate(action, character, social_terms=None, travel=0):
    values = {trait: normalized(getattr(character.personality, trait))
              for trait in ("honesty", "greed", "courage", "independence", "compassion", "diligence",
                            "family_loyalty", "persistence", "temperament", "vengefulness", "ambition")}
    values["devotion"] = normalized(getattr(character,'devotion',0))
    values.setdefault("risk", 0)
    values["hunter"] = float(character.profession == "caçador")
    values.update(social_terms or {})
    for key in ('physical_depletion', 'critical_depletion', 'recovery_pressure'):
        values.setdefault(key, 0)
    # Termos ficam entre -1 e 1; score apresentado em pontos para facilitar debug.
    terms = {"base": BASE[action] / 200}
    terms.update({name: values[name] * weight / 200
                  for name, weight in WEIGHTS.get(action, {}).items()})
    terms["travel"] = -min(1, travel * UTILITY.distance_weight / 200)
    return 200 * sum(terms.values()), terms

BASE.update(search_area=55,ask_about_person=55,return_from_search=65)
WEIGHTS.update(search_area={'persistence':25,'courage':15},ask_about_person={'diligence':20,'compassion':15,'independence':-15},return_from_search={'diligence':20})

BASE.update(share_problem=45,organize=55,join_group=45,meet_group=50,submit_proposal=70,
    review_proposal=65,protest=40,seek_royal_aid=50,recruit_member=40,report_to_faction=45,
    contribute=35,perform_assignment=55,seek_local_office=40,assume_local_office=50,
    pray=50,offer_resource=40,spread_faith=45,reinterpret=30,challenge_divinity=20,
    claim_essence=30,train_power=50,defend_cult=40,finish=20)
WEIGHTS.update(organize={'ambition':25,'compassion':20,'persistence':20},
    share_problem={'compassion':15,'independence':-15},join_group={'compassion':20,'independence':-20},
    meet_group={'diligence':20,'persistence':20},submit_proposal={'ambition':25,'persistence':20},
    review_proposal={'diligence':25,'honesty':15},protest={'temperament':20,'courage':15},
    recruit_member={'ambition':25},contribute={'compassion':25,'greed':-20},
    train_power={'diligence':20,'ambition':25},finish={'vengefulness':40,'anger':40,'compassion':-60,'honesty':-10})

BASE.update(issue_local_order=60)
BASE.update(tell_item_history=35)
BASE.update(serve_office=55)
BASE.update(read_response=55)
BASE.update(attend_group=50,represent_travel=60,relay_response=75,faction_prepare=50,faction_raid=45)
BASE.update(plan_incursion=55,attend_faction=50)
WEIGHTS.update(attend_group={'persistence':20,'diligence':15},represent_travel={'persistence':20,'courage':10},
    relay_response={'diligence':25,'compassion':20},faction_prepare={'diligence':20},
    faction_raid={'courage':20,'greed':15,'honesty':-30})

# Ações semânticas da Fase 5.4 usam a mesma avaliação de alternativas.
BASE.update(route_travel=58, ask_route=70, take_site_supplies=95, explore_poi=55,
            claim_location=55, invite_person=55, request_membership=52, answer_invitation=65,
            store_supplies=40, seek_divine_contact=55, accept_contract=55, refuse_contract=40,
            abandon_contract=25, form_expedition=62, follow_expedition=58, formalize_organization=65)
WEIGHTS.update({'route_travel':{'persistence':20,'risk':-20},'ask_route':{'persistence':20},
                'explore_poi':{'ambition':20,'courage':25,'risk':-35},
                'seek_divine_contact':{'devotion':25,'ambition':15},
                'accept_contract':{'devotion':25,'independence':-25},
                'refuse_contract':{'independence':35}})

BASE.update(policy_work=65,support_proposal=65,institutional_support=65,institutional_patrol=60,institutional_purchase=60,institutional_supply=85,institutional_raid=55,institutional_response=55)
WEIGHTS.update(policy_work={"diligence":25,"financial_pressure":25},institutional_patrol={"diligence":20,"courage":15},institutional_raid={"greed":35,"honesty":-75,"courage":15})

# Relato é comunicação religiosa de fatos conhecidos, como report_to_faction;
# afinidade vem da devoção e dever da diligência. Viagem usa a penalidade comum.
BASE['report_congregation'] = BASE['report_to_faction']
WEIGHTS['report_congregation'] = {'diligence':20, 'devotion':25}
