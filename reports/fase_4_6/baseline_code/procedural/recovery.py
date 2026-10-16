"""Dano por origem e recuperação; sem recursos ou escolhas automáticas."""
from .rules import RECOVERY, SURVIVAL, FEEDING


class RecoverySystem:
    def __init__(self, engine):
        self.engine, self.world = engine, engine.world

    def count(self, key, amount=1):
        key = 'Recovery:'+key
        self.world.metrics[key] = self.world.metrics.get(key, 0)+amount

    def damage(self, person, amount, origin):
        actual = min(person.health, max(0, int(amount)))
        person.health -= actual
        person.damage_by_origin[origin] = person.damage_by_origin.get(origin, 0)+actual
        if origin in ('hunger', 'thirst', 'both'):
            person.recoverable_deprivation_damage += actual
        self.count('Damage:'+origin, actual)
        return actual

    def safe(self, person, location=None):
        return (location or person.position) == person.home and not person.combat.opponents

    def fast_rate(self, person):
        if not self.safe(person):
            return 0
        level = max(person.hunger, person.thirst)
        if level <= RECOVERY.excellent_level:
            return RECOVERY.excellent_rate
        if level <= RECOVERY.acceptable_level:
            return RECOVERY.acceptable_rate
        return RECOVERY.poor_rate if level <= RECOVERY.poor_level else 0

    def recover_hp(self, person, hours=1, treatment=0):
        """Um orçamento por descanso; cura rápida só debita privação real.

        O teto total é max(cura normal, cura fisiológica), nunca a soma.
        Socorro limitado atende dano físico primeiro, debitando privação se
        necessário para manter ledger <= HP ausente.
        """
        if not person.alive:
            return 0
        missing = 100-person.health
        ledger = min(missing, person.recoverable_deprivation_damage)
        normal = SURVIVAL.rest_healing*hours
        band = SURVIVAL.band(max(person.hunger, person.thirst))
        if band in ('critical', 'starvation'):
            normal = 0
        elif band == 'severe':
            normal = int(normal*SURVIVAL.reduced_healing)
        fast = self.fast_rate(person)*hours if ledger else 0
        if treatment:
            physical = min(missing-ledger, treatment)
            physiological = min(ledger, treatment-physical)
        else:
            budget = max(normal, fast)
            physiological = min(ledger, fast or normal, budget)
            physical = min(missing-ledger, normal, budget-physiological)
        healed = physiological+physical
        person.health += healed
        person.recoverable_deprivation_damage -= physiological
        self.count('DeprivationHealed', physiological)
        self.count('PhysicalHealed', physical)
        if healed:
            person.recovery_state['last_healed_at'] = self.world.turn
            person.recovery_state['last_hp'] = person.health
        if not treatment and normal:
            person.combat.injured = max(0, person.combat.injured-2*hours)
        if ledger and not person.recoverable_deprivation_damage:
            self.count('DeprivationFullyRecovered')
        return healed

    def refresh(self, person):
        if person.health < RECOVERY.target_hp:
            # 80/60/40/20 HP => 25/45/65/85 de pressão; vitais críticas
            # continuam acima e a baixa vida não proíbe trabalho/autodefesa.
            urgency = min(95, 25+max(0, RECOVERY.target_hp-person.health))
            need = self.engine.needs.ensure(person, 'recovery', urgency,
                'own_physiology', 'Recuperar condição física após dano', person.id)
            need.context.update(hp=person.health,
                deprivation_damage=person.recoverable_deprivation_damage,
                physical_damage=max(0, 100-person.health-person.recoverable_deprivation_damage),
                critical=person.health < RECOVERY.critical_hp)
        else:
            self.engine.needs.satisfy(person, 'recovery')

    def candidates(self, person):
        """Enumera etapas conhecidas de estabilização, não executa uma cura."""
        choices = []
        level = max(person.hunger, person.thirst)
        if person.thirst > RECOVERY.excellent_level and person.thirst >= person.hunger:
            return 'water'
        if person.hunger > RECOVERY.excellent_level:
            # Reutiliza aquisições, ajuda e estimativa alimentar existentes.
            return 'food'
        if person.thirst > RECOVERY.excellent_level:
            return 'water'
        if person.combat.opponents:
            # Respostas defensivas continuam no sistema de conflitos.
            return []
        if person.combat.injured >= 6:
            choices.append(('seek_treatment', person.home, person.id))
            for i in self.engine.spatial.at(person.position):
                if i != person.id and self.engine.social.can_request(person, self.world.characters[i]):
                    choices.append(('call_help', None, i))
        if level <= RECOVERY.poor_level:
            choices.append(('sleep', person.home, None))
        return choices

    def known_pursuit(self, person):
        facts = person.knowledge.values()
        closed = max((f.turn for f in facts if f.kind in ('GuardResponded', 'CharacterCaptured')
                      and f.target_id == person.id), default=-1)
        return any(f.kind == 'WantedIssued' and f.context.get('suspect_id') == person.id
                   and f.turn > closed and self.world.turn-f.turn <= 168 for f in facts)

    def material_stable(self, person):
        return (max(person.hunger, person.thirst) <= RECOVERY.excellent_level
                and (person.health >= 60 or self.world.turn-person.recovery_state.get('last_healed_at', -9999) <= 6)
                and self.safe(person) and not self.known_pursuit(person)
                and self.engine.items.count(person.id, 'food') >= 1
                and self.engine.items.count(person.id, 'water') >= 1)
