"""Necessidade é pressão; prioridade e ação são decisões separadas."""

from .models import Character, Need, WorldState
from .rules import SURVIVAL

FINISHED = {"satisfied", "failed", "expired", "inactive"}


class NeedSystem:
    def __init__(self, world: WorldState, graph, recorder):
        self.world, self.graph, self.recorder = world, graph, recorder
        self.personal = None

    def explain(self, owner, need, reason, competing=None):
        """Contagens por avaliação; exemplos limitados por transição de motivo."""
        key = f"PersonalOutcome:{need.kind}:{reason}"
        self.world.metrics[key] = self.world.metrics.get(key, 0) + 1
        counts = need.context.setdefault("diagnostic_counts",{})
        counts[reason] = counts.get(reason,0)+1
        diagnostic = {"reason":reason,"competing":competing,"turn":self.world.turn}
        old = need.context.get("diagnostic", {})
        if old.get("reason") != reason or old.get("competing") != competing:
            self.world.decision_diagnostics.append({"owner":owner.id,"need":need.id,"kind":need.kind,
                "priority":need.priority,**diagnostic})
            del self.world.decision_diagnostics[:-256]
        need.context["diagnostic"] = diagnostic

    def count(self, transition, kind, owner=None):
        key = f"Need{transition}:{kind}"
        self.world.metrics[key] = self.world.metrics.get(key, 0) + 1
        if owner is not None:
            scope = "Player" if getattr(owner, "is_player", False) else "NPC" if isinstance(owner, Character) else "Collective"
            scoped = f"{scope}{key}"
            self.world.metrics[scoped] = self.world.metrics.get(scoped, 0) + 1

    def finish(self, owner, need, status="satisfied"):
        if need.status in FINISHED:
            return
        need.status, need.priority, need.updated_at = status, 0, self.world.turn
        self.count("Satisfied" if status == "satisfied" else "Expired", need.kind, owner)
        if need.kind in ("family", "grief", "revenge", "protection", "status", "advancement"):
            self.explain(owner,need,"Satisfied" if status == "satisfied" else
                         "ExpiredBeforeSelection" if not need.context.get("selections") and owner.alive else
                         "OwnerDied" if not owner.alive else "ExpiredAfterSelection")
            key = need.kind if need.target_id is None else f"{need.kind}:{need.target_id}"
            owner.personal_cooldowns[key] = self.world.turn + 48
        if getattr(owner, "goal", None) and owner.goal.need_id == need.id:
            owner.goal.status = "completed" if status == "satisfied" else "failed"

    def ensure(self, owner, key: str, urgency: float, source: str, reason: str,
               target_id: int | None = None) -> Need:
        need = owner.needs.get(key)
        if need is None:
            need = Need(self.world.allocate_id(), owner.id, key.split(":")[0], target_id, urgency,
                        urgency, self.world.turn, self.world.turn, "active", source, reason)
            owner.needs[key] = need
            self.count("Created", key.split(":")[0], owner)
        elif need.status in FINISHED:
            need.created_at = self.world.turn
            need.context, need.expires_at = {}, None
            self.count("Created", need.kind, owner)
        need.base_urgency = max(0, min(100, urgency))
        need.updated_at = self.world.turn
        need.status = "active"
        need.source, need.reason, need.target_id = source, reason, target_id
        return need

    def satisfy(self, owner, key: str) -> None:
        need = owner.needs.get(key)
        if need and need.status not in FINISHED:
            self.finish(owner, need)

    def physiology(self, character: Character) -> None:
        symbol = self.world.maps[character.position.map_id].rows[character.position.y][character.position.x]
        character.hunger = min(100, character.hunger + 2)
        character.thirst = min(100, character.thirst + (4 if symbol == "D" else 2))
        character.fatigue = min(100, character.fatigue + 1.2)
        if max(character.hunger, character.thirst) >= SURVIVAL.starvation:
            character.starvation_hours += 1
            damage = min(SURVIVAL.maximum_damage, SURVIVAL.starvation_damage +
                         character.starvation_hours // SURVIVAL.progression_hours)
            character.health = max(0, character.health - damage)
        else:
            character.starvation_hours = 0

    def rest(self, character: Character, hours: int = 1) -> None:
        character.fatigue = max(0, character.fatigue - 12 * hours)
        band = SURVIVAL.band(max(character.hunger, character.thirst))
        recovery = SURVIVAL.rest_healing * hours
        if band in ("critical", "starvation") or not character.alive:
            recovery = 0
        elif band == "severe":
            recovery = int(recovery * SURVIVAL.reduced_healing)
        character.health = min(100, character.health + recovery)

    def refresh(self, character: Character) -> list[Need]:
        if character.training_target:
            last = character.training_last_practice if character.training_last_practice is not None else character.training_started
            if last is not None and self.world.turn-last > 168:
                character.training_target = None
                character.training_progress = character.training_required = 0
                self.recorder.emit("TrainingAbandoned",f"{character.name} abandonou a aprendizagem sem prática recente.",
                    character.id,character.town_id,character.position)
        for key, level, reason in (("food", character.hunger, "Fome"),
                                   ("water", character.thirst, "Sede"),
                                   ("rest", character.fatigue, "Cansaço")):
            if level >= 25:
                self.ensure(character, key, level, "physiology", reason)
            else:
                self.satisfy(character, key)
        if character.money < 10:
            if character.financial_since is None:
                character.financial_since = self.world.turn
        elif character.money >= 20:
            character.financial_since, character.financial_setbacks = None, 0
        financial_age = self.world.turn - character.financial_since if character.financial_since is not None else 0
        money_target = 20 if financial_age >= 48 else 10
        if character.money < money_target and (character.profession not in (None, "estudante") or character.training_target):
            need = self.ensure(character, "money", min(70, 30 + max(0, 10 - character.money) * 2 +
                               min(12, financial_age / 24) + character.financial_setbacks),
                               "economy", "Estabilizar renda baixa persistente" if financial_age >= 48
                               else "Reservas financeiras baixas")
            need.context.update({"money_target": money_target, "low_money_hours": financial_age})
        else:
            self.satisfy(character, "money")
        working = 8 <= self.world.turn % 24 < 18
        if working and (character.profession not in (None, "estudante") or character.training_target):
            self.ensure(character, "work", 35, "profession", "Responsabilidade profissional")
        else:
            self.satisfy(character, "work")
        crimes = [fact for fact in character.knowledge.values()
                  if fact.kind == "ItemStolen" and self.world.turn - fact.turn < 24 and
                  fact.actor_id != character.id and
                  character.failures.get(f"crime:{fact.event_id}", 0) <= self.world.turn]
        if crimes and character.profession == "guarda":
            fact = crimes[-1]
            self.ensure(character, "security", 60, f"event:{fact.event_id}",
                        fact.description, fact.actor_id)
        else:
            self.satisfy(character, "security")
        character.failures = {key: until for key, until in character.failures.items()
                              if until > self.world.turn}
        if self.personal:
            self.personal.refresh(character)
        active = []
        for need in character.needs.values():
            if need.status in FINISHED:
                continue
            age = min(8, (self.world.turn - need.created_at) * .15)
            personality = 0
            if need.kind in ("money", "work"):
                personality = character.personality.diligence / 5
            elif need.kind == "security":
                personality = character.personality.courage / 10 + 20
            elif self.personal:
                personality = self.personal.priority_modifier(character, need)
            relationship = (self.graph.value(character.id, need.target_id, "amizade") / 10
                            if need.target_id else 0)
            danger = 15 if need.kind in ("food", "water") and need.base_urgency >= 80 else 0
            need.priority = min(100, need.base_urgency + age + personality + relationship + danger)
            active.append(need)
        return sorted(active, key=lambda need: (-need.priority, need.id))
