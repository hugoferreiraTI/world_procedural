"""Considerações sociais e interpretação contextual, sem conhecimento global."""

from .rules import UTILITY


def normalized(value: float) -> float:
    return max(0., min(1., value / 100))


class SocialSystem:
    def __init__(self, world, graph, items):
        self.world, self.graph, self.items = world, graph, items

    def reputation(self, observer, target_id: int) -> float:
        rep = observer.reputations.get(target_id)
        if not rep:
            return 0.
        positive = max(rep.admiration, rep.tags.get("prestativo", 0))
        negative = max(rep.tags.get("ladrão", 0), rep.tags.get("perigoso", 0),
                       rep.tags.get("insensível", 0))
        return (positive - negative) / 100

    def considerations(self, observer, target_id: int) -> dict[str, float]:
        return {"trust": normalized(self.graph.value(observer.id, target_id, "confiança", 10)),
                "reputation": self.reputation(observer, target_id),
                "relationship": normalized(self.graph.value(observer.id, target_id, "amizade"))}

    def modifier(self, observer, target_id: int) -> float:
        terms = self.considerations(observer, target_id)
        return (terms["trust"] * UTILITY.trust_weight +
                terms["reputation"] * UTILITY.reputation_weight + terms["relationship"] * 10)

    def known(self, observer, target_id: int) -> bool:
        return (target_id in observer.reputations or
                any(self.graph.value(observer.id, target_id, kind) > 0
                    for kind in ("familiaridade", "confiança", "amizade", "casamento")) or
                any(f.actor_id == target_id for f in observer.knowledge.values()))

    def can_request(self, observer, target) -> bool:
        # Posição e sinais físicos são observáveis neste encontro. Inventário
        # e dinheiro do interlocutor não são consultados para escolher a ação.
        return (target.alive and target.id != observer.id and target.position == observer.position
                and self.known(observer, target.id) and target.health >= 30
                and target.hunger < 85 and
                (self.graph.value(observer.id, target.id, "confiança", 10) >= 20 or
                 self.reputation(observer, target.id) >= .2))

    def willing_to_feed(self, giver, receiver) -> bool:
        score = giver.personality.compassion + self.modifier(giver, receiver.id)
        return (score >= UTILITY.help_threshold and giver.hunger < 65 and
                self.items.count(giver.id, "food") > 1)

    def interpret(self, observer, fact) -> tuple[dict[str, float], float]:
        """Efeitos básicos; confiabilidade é aplicada pelo KnowledgeSystem."""
        p = observer.personality
        trust = 0.
        if fact.kind == "HelpGiven":
            urgency = fact.context.get("urgency", 75)
            relevance = normalized(urgency)
            if urgency < 25:
                return {}, 0.
            weight = 15 * relevance * (.5 + normalized(p.compassion))
            if observer.id == fact.target_id:
                trust = 12 * relevance * (.5 + normalized(p.compassion))
            return {"prestativo": weight}, trust
        if fact.kind in ("ComfortGiven", "ProtectionGiven"):
            return {"prestativo": 6 * (.5 + normalized(p.compassion))}, 4 if fact.target_id == observer.id else 0
        if fact.kind == "ResponsibilityFulfilled":
            return {"responsável": 3 * (.5 + normalized(p.diligence))}, 0.
        if fact.kind == "ItemStolen":
            if observer.id == fact.target_id:
                trust = -12 * normalized(p.honesty)
            return {"ladrão": 15 * (.5 + normalized(p.honesty))}, trust
        if fact.kind in ('ApologyGiven','RestitutionGiven','ConflictForgiven'):
            return {'reparador':8}, 5 if observer.id==fact.target_id else 0
        if fact.kind=='FirstAidGiven':
            return {'prestativo':12,'protetor':8}, 8 if observer.id==fact.target_id else 0
        if fact.kind=='CharacterAttacked':
            if fact.context.get('lawful') or fact.context.get('self_defense'):
                return {'protetor':8},0
            return {'perigoso':12,'agressivo':8},-8 if observer.id==fact.target_id else 0
        if fact.kind in ('CharacterThreatened','CharacterInsulted'):
            if fact.context.get('lawful'):return {'responsável':3},0
            return {'agressivo':6},-4 if observer.id==fact.target_id else 0
        if fact.kind == "CharacterKilled":
            # Contexto registra a filiação da vítima no momento do fato.
            victim_faction = fact.context.get("victim_faction")
            loyalty = self.graph.value(observer.id, observer.faction, "lealdade") if observer.faction else 0
            enemy = (victim_faction is not None and observer.faction is not None and
                     self.graph.value(observer.faction, victim_faction, "diplomacia") < -20)
            if enemy and loyalty >= 60 and p.courage > p.compassion:
                return {"leal": 20 * normalized(loyalty)}, 0.
            kin = max(self.graph.value(observer.id, fact.target_id, k)
                      for k in ("amizade", "casamento", "pai_de", "filho_de")) if fact.target_id else 0
            return {"perigoso": 20 * (.5 + normalized(p.compassion) + normalized(kin) / 2)}, 0.
        if fact.kind == "PlayerRefusedRequest" and fact.target_id == observer.id:
            urgency = normalized(fact.context.get("urgency", 0))
            incapable = fact.context.get("incapable", False)
            understanding = normalized(p.compassion) * (1 if incapable else .35)
            expectation = normalized(fact.context.get("trust", 10))
            resentment = urgency * (1 - understanding) * (.5 + normalized(p.persistence) / 2)
            if resentment < .2:
                return {}, 0.
            return {"insensível": 12 * resentment}, -12 * resentment * (.5 + expectation)
        return {}, 0.
