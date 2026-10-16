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


SURVIVAL = SurvivalRules()
UTILITY = UtilityRules()
SOURCE_RELIABILITY = {"direct": 1., "trusted": .8, "known": .6,
                      "rumor": .3, "untrusted": .1}
