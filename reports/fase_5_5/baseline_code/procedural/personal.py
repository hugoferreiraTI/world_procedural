"""Pressões pessoais: percepção e ciclo de vida dentro do NeedSystem existente.

Este serviço não escolhe objetivos nem executa uma política de decisões.
Observações vêm de encontros; notícias vêm de KnowledgeSystem.learn.
"""

from .models import Observation, Location
from .needs import FINISHED

PERSONAL_KINDS = {"family", "grief", "revenge", "protection", "status", "advancement"}


class PersonalNeeds:
    def __init__(self, world, needs, graph, spatial, items, recorder):
        self.world, self.needs, self.graph = world, needs, graph
        self.spatial, self.items, self.recorder = spatial, items, recorder
        self.kin = {}
        for relation in world.relationships.values():
            if relation.kind in ("casamento", "pai_de", "filho_de"):
                self.kin.setdefault(relation.source_id, set()).add(relation.target_id)

    def relationship(self, person, target):
        family = max((self.graph.value(person.id, target, kind)
                      for kind in ("casamento", "pai_de", "filho_de")), default=0)
        friendship = self.graph.value(person.id, target, "amizade")
        return max(family, friendship), bool(family)

    def create(self, person, kind, target, urgency, source, reason, duration, context=None):
        key = f"{kind}:{target}" if target is not None else kind
        need = self.needs.ensure(person, key, urgency, source, reason, target)
        need.expires_at = self.world.turn + duration
        need.context.update(context or {})
        return need

    def on_fact(self, person, fact):
        if fact.kind not in ("CharacterDied", "CharacterKilled", "RemainsLocated", "ItemStolen", "PersonLocated",
                             "GuardResponded", "ProtectionGiven", "ComfortGiven", "HelpGiven"):
            return
        if fact.confidence < 30:
            return
        if fact.event_id in person.processed_personal_facts:
            person.processed_personal_facts[fact.event_id] = max(person.processed_personal_facts[fact.event_id], fact.confidence)
            for need in person.needs.values():
                if need.context.get("source_event") == fact.event_id:
                    need.context["confidence"] = fact.confidence
            return  # Evidência melhor não é outro luto/ameaça.
        if fact.kind in ("CharacterDied", "CharacterKilled", "RemainsLocated"):
            for need in person.needs.values():
                if (need.kind == "revenge" and need.target_id == fact.target_id or
                        need.kind == "protection" and need.context.get("threat") == fact.target_id):
                    self.needs.finish(person, need)
                    need.context["resolution"] = "Morte conhecida do responsável/ameaça"
            strength, family = self.relationship(person, fact.target_id)
            if strength < 40 or fact.target_id == person.id:
                return
            person.processed_personal_facts[fact.event_id] = fact.confidence
            observed = person.observations.get(fact.target_id)
            if observed:
                observed.alive = False
            concern = person.needs.get(f"family:{fact.target_id}")
            if concern:
                self.needs.finish(person, concern)
            context = {"source_event": fact.event_id, "confidence": fact.confidence,
                       "relationship": strength, "family": family,
                       "known_location": self.location_data(fact.location), "loss": fact.target_id}
            if f"grief:{fact.target_id}" not in person.needs:
                self.create(person, "grief", fact.target_id, 20 + strength * .35, f"event:{fact.event_id}",
                            f"Morte conhecida de {self.world.characters[fact.target_id].name}",
                            48 + int(strength), context)
            if fact.kind == "CharacterKilled":
                self.revenge(person, fact, strength, family)
        elif fact.kind == "ItemStolen":
            if fact.actor_id in (None, person.id):
                return
            direct_harm = fact.target_id == person.id or fact.target_id in self.kin.get(person.id, ())
            local_harm = (fact.target_id == person.town_id and person.hunger >= 55 and
                          fact.location == person.position)
            recurring = sum(f.kind == "ItemStolen" and f.location == fact.location and
                            self.world.turn - f.turn <= 24 for f in person.knowledge.values()) >= 2
            home_threat = fact.location == person.home
            if not (direct_harm or local_harm or recurring or home_threat):
                return
            person.processed_personal_facts[fact.event_id] = fact.confidence
            protected = fact.target_id if fact.target_id in self.kin.get(person.id, ()) else person.id
            if person.profession != "guarda" or protected != person.id:
                self.create(person, "protection", protected, 45 if recurring or direct_harm else 30,
                            f"event:{fact.event_id}", "Crime conhecido ameaça segurança pessoal/familiar",
                            48, {"source_event": fact.event_id, "threat": fact.actor_id,
                                 "known_location": self.location_data(fact.location),
                                 "protected": protected, "scope": "home" if home_threat else "person"})
            if direct_harm or local_harm and person.personality.vengefulness >= 60:
                strength, family = self.relationship(person, fact.target_id)
                self.revenge(person, fact, max(40, strength), family)
        elif fact.kind == "PersonLocated":
            concern = person.needs.get(f"family:{fact.target_id}")
            observation = person.observations.get(fact.target_id)
            newer = not observation or fact.turn > observation.turn
            changed = bool(observation and fact.location != observation.position)
            searched_same = bool(concern and concern.context.get('known_location') == self.location_data(fact.location)
                                 and concern.context.get('searched_at', -1) >= fact.turn)
            if (concern and fact.location and newer and not searched_same and
                    (fact.turn >= concern.created_at or changed)):
                person.observations[fact.target_id] = Observation(fact.turn, fact.location,
                    fact.context.get("hunger"), fact.context.get("thirst"), fact.context.get("health"))
                self.trim_observations(person)
                concern.context["known_location"] = self.location_data(fact.location)
                concern.context['searched'] = False
                concern.context.pop('searched_at', None)
                concern.context['information_progress'] = 'confirmed_location' if fact.turn >= concern.created_at else 'search_lead'
                if concern.context.get("mode") == "missing" and fact.turn >= concern.created_at:
                    self.needs.finish(person, concern)
        elif fact.kind == "GuardResponded":
            for need in person.needs.values():
                if need.kind == "revenge" and need.target_id == fact.target_id:
                    self.needs.finish(person, need)
                    need.context["resolution"] = "Intervenção conhecida do guarda"
        elif fact.kind == "ProtectionGiven" and fact.target_id == person.id:
            for need in person.needs.values():
                if need.kind == "protection" and need.status not in FINISHED:
                    self.needs.finish(person, need)
        elif fact.kind == "ComfortGiven" and fact.target_id == person.id:
            for need in person.needs.values():
                if need.kind == "grief" and need.status not in FINISHED:
                    self.needs.finish(person, need)
        elif fact.kind == "HelpGiven" and fact.context.get("urgency", 0) >= 25:
            concern = person.needs.get(f"family:{fact.target_id}")
            if concern and concern.context.get("mode") == "care" and fact.context.get("item_kind", "food") == concern.context.get("resource", "food"):
                self.needs.finish(person, concern)

    def revenge(self, person, fact, strength, family):
        key = f"revenge:{fact.target_id}"
        previous = person.needs.get(key)
        if previous and previous.context.get("fact_kind") == "CharacterKilled":
            culprit_confidence=previous.context.get('culprit_confidence',
                previous.context.get('confidence',0) if previous.target_id is not None else 0)
            if (fact.actor_id is not None and fact.confidence>=60 and
                    fact.confidence>=culprit_confidence):
                previous.target_id = fact.actor_id
                previous.context.update({"culprit":fact.actor_id,"culprit_confidence":fact.confidence,
                    "confidence":max(previous.context.get('confidence',0),fact.confidence)})
            return  # Identificação complementar da mesma perda, não outra necessidade.
        need = self.create(person, "revenge", fact.target_id, 20 + strength * .25,
                    f"event:{fact.event_id}", "Buscar informação ou reparação por dano conhecido",
                    48 + person.personality.vengefulness * 2,
                    {"source_event": fact.event_id, "victim": fact.target_id,
                     "culprit": fact.actor_id, "relationship": strength, "family": family,
                     "known_location": self.location_data(fact.location), "fact_kind": fact.kind,
                     "confidence": fact.confidence,
                     "culprit_confidence":fact.confidence if fact.actor_id is not None else 0})
        need.target_id = fact.actor_id

    @staticmethod
    def location_data(location):
        return {"map_id": location.map_id, "x": location.x, "y": location.y} if location else None

    @staticmethod
    def location(context):
        data = context.get("known_location")
        return Location(**data) if data else None

    def trim_observations(self, person):
        protected=self.kin.get(person.id, ())
        removable=sorted(person.observations,key=lambda i:(i in protected,person.observations[i].turn,i))
        for id in removable[:max(0,len(person.observations)-64)]:person.observations.pop(id,None)

    def refresh(self, person):
        now, p = self.world.turn, person.personality
        present = self.spatial.at(person.position)
        for target in present:
            if target == person.id:
                continue
            encountered = self.world.characters[target]
            person.observations[target] = Observation(now, encountered.position, encountered.hunger,
                                                    encountered.thirst, encountered.health,
                                                    profession=encountered.profession)
            if target not in self.kin.get(person.id, ()):
                continue
            relative = self.world.characters[target]  # Encontro, sinais observáveis.
            person.observations[target] = Observation(now, relative.position, relative.hunger,
                                                    relative.thirst, relative.health)
            key = f"family:{target}"
            level = max(relative.hunger, relative.thirst)
            if level < 25 and key in person.needs:
                self.needs.finish(person, person.needs[key])
            elif level >= 55 and person.personal_cooldowns.get(key, 0) <= now:
                current = person.needs.get(key)
                if not current or current.status in FINISHED:
                    strength, _ = self.relationship(person, target)
                    event = self.recorder.emit("FamilyConcern", f"{person.name} percebeu a privação de {relative.name}.",
                                               person.id, target, person.position,
                                               witnesses=[person.id], context={"observed_need": level})
                    self.create(person, "family", target, 20 + level * .3 + strength * .2,
                                f"event:{event.id}", "Privação de familiar percebida em encontro", 48,
                                {"mode": "care", "source_event": event.id, "relationship": strength,
                                 "danger": level >= 85, "known_location": self.location_data(relative.position)})
                    person.needs[key].context["resource"] = "water" if relative.thirst > relative.hunger else "food"
            elif key in person.needs and person.needs[key].context.get("mode") == "missing":
                self.needs.finish(person, person.needs[key])
        for target, observation in list(person.observations.items()):
            key = f"family:{target}"
            if (target not in self.kin.get(person.id, ()) or not observation.alive or
                    target in present or now - observation.turn < 36 or
                    person.personal_cooldowns.get(key, 0) > now):
                continue
            current = person.needs.get(key)
            if not current or current.status in FINISHED:
                strength, _ = self.relationship(person, target)
                event = self.recorder.emit("AbsenceNoticed", f"{person.name} não localiza um familiar há {now - observation.turn} horas.",
                                           person.id, location=person.position, witnesses=[person.id],
                                           context={"last_seen": observation.turn, "relative_id": target})
                self.create(person, "family", target, min(75, 20 + strength * .2 + (now - observation.turn) / 6),
                            f"event:{event.id}", "Ausência percebida após encontros anteriores", 72,
                            {"mode": "missing", "source_event": event.id, "relationship": strength,
                             "last_seen": observation.turn, "known_location": self.location_data(observation.position)})
        self.trim_observations(person)
        # Status nasce de um encontro real com alguém numa posição reconhecível.
        if p.ambition >= 60 and person.category == "comum" and person.personal_cooldowns.get("status", 0) <= now:
            role_model = next((self.world.characters[i] for i in present if i != person.id and
                               (self.world.characters[i].category in ("importante", "lendário") or
                                i in person.reputations and person.reputations[i].admiration >= 30)), None)
            current = person.needs.get("status")
            if role_model and (not current or current.status in FINISHED):
                self.create(person, "status", None, 20, f"encounter:{role_model.id}:{now}",
                            f"Buscar reconhecimento após encontrar {role_model.name}", 168,
                            {"role_model": role_model.id, "deeds": 0, "deeds_target": 1})
        # Crescimento concreto de riqueza, distinto de sobrevivência financeira.
        current = person.needs.get("advancement")
        if (p.ambition >= 65 and person.money >= 10 and person.personal_cooldowns.get("advancement", 0) <= now and
                (not current or current.status in FINISHED)):
            self.create(person, "advancement", None, 15, f"self_assessment:{now}",
                        "Acumular uma reserva maior com trabalho e comércio disponíveis", 240,
                        {"domain": "wealth", "money_target": person.money + 10 + p.ambition // 10})
        for need in list(person.needs.values()):
            if need.kind not in PERSONAL_KINDS or need.status in FINISHED:
                continue
            if need.kind == "advancement" and person.money >= need.context.get("money_target", float("inf")):
                self.needs.finish(person, need)
            elif need.expires_at is not None and now >= need.expires_at and not (
                    self.needs.agency and self.needs.agency.current(person,need)):
                self.needs.finish(person, need, "expired")
            if need.status in FINISHED:
                person.personal_cooldowns[need.kind if need.target_id is None else f"{need.kind}:{need.target_id}"] = now + 48

    def priority_modifier(self, person, need):
        p = person.personality
        if need.kind == "family":
            return p.family_loyalty * .15 + (10 if need.context.get("danger") else 0)
        if need.kind == "grief":
            return p.compassion * .1 + (p.family_loyalty * .1 if need.context.get("family") else 0)
        if need.kind == "revenge":
            return p.vengefulness * .22 + p.temperament * .08 - p.compassion * .1
        if need.kind == "protection":
            return (100 - p.courage) * .1 + p.family_loyalty * .1
        if need.kind in ("status", "advancement"):
            return p.ambition * .25
        return 0
