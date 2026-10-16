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
