"""Parâmetros pequenos, explícitos e comuns a todas as entidades."""

from dataclasses import dataclass


@dataclass(frozen=True)
class SurvivalRules:
    normal: float = 30
    moderate: float = 60
    severe: float = 80
    starvation: float = 100
    reduced_healing: float = .5
    rest_healing: int = 3
    starvation_damage: int = 2
    progression_hours: int = 12
    maximum_damage: int = 6

    def band(self, level: float) -> str:
        if level <= self.normal:
            return "normal"
        if level <= self.moderate:
            return "moderate"
        if level <= self.severe:
            return "severe"
        return "critical" if level < self.starvation else "starvation"


@dataclass(frozen=True)
class UtilityRules:
    distance_weight: float = 2
    close_choices: float = 3
    variation: float = 1.5
    help_threshold: float = 75
    trust_weight: float = 35
    reputation_weight: float = 45


@dataclass(frozen=True)
class FeedingRules:
    reserve_hours: int = 24
    travel_margin_hours: int = 6
    maximum_reserve: int = 6
    meal_threshold: float = 35
    meal_opportunity_end: float = 40
    meal_important: float = 60
    high_hunger: float = 80
    emergency_window: int = 6
    reserve_priority: float = 26
    reserve_deficit_weight: float = 8
    reserve_hunger_weight: float = .2
    hunger_per_hour: float = 2
    meal_reduction: float = 40
    minimum_market_price: int = 2
    estimate_horizon: int = 128
    diagnostics_limit: int = 256


SURVIVAL = SurvivalRules()
FEEDING = FeedingRules()
UTILITY = UtilityRules()


@dataclass(frozen=True)
class RecoveryRules:
    target_hp: int = 80
    critical_hp: int = 20
    lod_hp: int = 30
    excellent_level: float = 50
    acceptable_level: float = 70
    poor_level: float = 80
    excellent_rate: int = 8
    acceptable_rate: int = 4
    poor_rate: int = 1
    stable_hours: int = 6
    material_desperation_decay: float = .25


RECOVERY = RecoveryRules()


@dataclass(frozen=True)
class InteractionRules:
    unarmed_damage: int = 4
    maximum_weapon_bonus: int = 12
    damage_variation: int = 2
    defense_multiplier: float = .45
    incapacity_health: int = 12
    conflict_timeout: int = 12
    truce_hours: int = 48
    detention_hours: int = 12
    warrant_confidence: int = 60
    maximum_pursuit_hours: int = 168
    anger_decay: float = .3
    resentment_decay: float = .04
    humiliation_decay: float = .1
    adaptation_hours: int = 720


INTERACTION = InteractionRules()
SOURCE_RELIABILITY = {"direct": 1., "trusted": .8, "known": .6,
                      "rumor": .3, "untrusted": .1}


@dataclass(frozen=True)
class AgencyRules:
    maximum_commitments: int = 4
    adoption_pressure: float = 52
    priority_bonus: float = 12
    maximum_duration: int = 720
    institutional_latency: int = 6
    maximum_case_guards: int = 3
    aspiration_return_hours: int = 48
    aspiration_drive_weight: float = .30


AGENCY = AgencyRules()
