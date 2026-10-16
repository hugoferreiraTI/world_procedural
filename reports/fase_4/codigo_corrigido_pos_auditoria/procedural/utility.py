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

BASE.update(dict(attack=28,defend=40,flee=35,surrender=25,intervene=35,protect=35,
    confront=35,threaten=25,demand_return=40,warn=30,insult=15,apologize=25,withdraw=35,
    call_help=25,alert=35,calm=35,forgive=25,first_aid=45,seek_treatment=60,pursue=55,
    capture=115,steal_person=62,return_stolen=45,self_harm=0,migrate=55))
WEIGHTS.update({
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


def evaluate(action, character, social_terms=None, travel=0):
    values = {trait: normalized(getattr(character.personality, trait))
              for trait in ("honesty", "greed", "courage", "independence", "compassion", "diligence",
                            "family_loyalty", "persistence", "temperament", "vengefulness", "ambition")}
    values["hunter"] = float(character.profession == "caçador")
    values.update(social_terms or {})
    # Termos ficam entre -1 e 1; score apresentado em pontos para facilitar debug.
    terms = {"base": BASE[action] / 200}
    terms.update({name: values[name] * weight / 200
                  for name, weight in WEIGHTS.get(action, {}).items()})
    terms["travel"] = -min(1, travel * UTILITY.distance_weight / 200)
    return 200 * sum(terms.values()), terms
