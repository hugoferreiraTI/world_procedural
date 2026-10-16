"""Quests representam necessidades reais nas quais o jogador se envolve."""

from .models import Quest
from .items import NAMES
from .needs import FINISHED


class QuestSystem:
    def __init__(self, world, graph, recorder, needs, items, social, economy):
        self.world, self.graph, self.recorder, self.needs, self.items = world, graph, recorder, needs, items
        self.social = social
        self.economy = economy

    def contract(self, npc, need):
        if need.kind == "food":
            if self.items.count(npc.id, "food") or self.economy.can_seek_food(npc):
                return None
            return "food", npc.id, f"Conseguir alimento para {npc.name}", {}
        location = self.needs.personal.location(need.context) if self.needs.personal else None
        if need.kind == "family" and location and location.map_id == npc.position.map_id:
            if need.context.get("mode") == "care":
                return "family_care", need.target_id, f"Levar provisões ao familiar de {npc.name}", {"resource": need.context.get("resource", "food"), "known_location": dict(need.context["known_location"])}
            return "family", need.target_id, f"Localizar familiar de {npc.name} e informar", {"known_location": dict(need.context["known_location"])}
        if need.kind == "grief":
            return "companionship", npc.id, f"Acompanhar {npc.name} em seu luto", {}
        if need.kind == "protection":
            return "protection", npc.id, f"Acompanhar {npc.name} diante de uma ameaça", {}
        if need.kind == "revenge" and need.target_id is not None and location and location.map_id == npc.position.map_id:
            return "information", need.target_id, f"Localizar o responsável conhecido e informar {npc.name}", {"known_location": dict(need.context["known_location"])}
        return None

    def offer(self, npc, player, origin: str = "conversation", need=None) -> Quest | None:
        active = self.needs.refresh(npc) if need is None else [need]
        if not player.is_player or not self.social.can_request(npc, player):
            return None
        eligible = [(n, self.contract(npc, n)) for n in active if n.status not in FINISHED and n.priority >= 50]
        selected = next(((n, contract) for n, contract in eligible if contract), None)
        if selected is None:
            return None
        need, (kind, target_id, title, context) = selected
        existing = next((quest for quest in self.world.quests.values()
                         if quest.owner_id == npc.id and quest.status in ("offered", "accepted")), None)
        if existing:
            return existing
        # A recusa não elimina a necessidade. Evita insistir no mesmo pedido no mesmo dia.
        if any(quest.owner_id == npc.id and self.world.turn - quest.created_at < 24
               for quest in self.world.quests.values()):
            return None
        quest = Quest(self.world.allocate_id(), npc.id, need.id,
                      title, self.world.turn, kind=kind, target_id=target_id,
                      context={**context, "source": need.source})
        self.world.quests[quest.id] = quest
        self.recorder.emit("HelpRequested", f"{npc.name} pediu ajuda a {player.name}: {title}.",
                           npc.id, player.id, npc.position, context={"origin": origin, "kind": kind, "need_kind": need.kind})
        self.needs.count("Quest", need.kind, npc)
        return quest

    def respond(self, quest_id: int, accept: bool) -> tuple[bool, str]:
        quest = self.world.quests.get(quest_id)
        if not quest or quest.status != "offered":
            return False, "Pedido inexistente ou já respondido."
        npc, player = self.world.characters[quest.owner_id], self.world.characters[self.world.player_id]
        if not npc.alive or player.position != npc.position:
            return False, "Responda ao pedido num encontro com o NPC."
        quest.status = "accepted" if accept else "declined"
        if not accept:
            npc = self.world.characters[quest.owner_id]
            player = self.world.characters[self.world.player_id]
            need = next((n for n in npc.needs.values() if n.id == quest.need_id), None)
            # Sem encontro atual não inferimos condições físicas remotas.
            incapable = (player.position == npc.position and
                         (player.health < 30 or player.hunger >= 85))
            self.recorder.emit("PlayerRefusedRequest", f"{player.name} recusou o pedido de {npc.name}.",
                               player.id, npc.id, player.position,
                               context={"urgency": need.priority if need else 0,
                                        "incapable": incapable,
                                        "trust": self.graph.value(npc.id, player.id, "confiança", 10)})
        return True, "Pedido aceito." if accept else "Pedido recusado; o NPC continuará procurando uma solução."

    def complete(self, quest, player):
        quest.status, quest.completed_at = "completed", self.world.turn
        npc = self.world.characters[quest.owner_id]
        self.recorder.emit("QuestCompleted", f"{player.name} cumpriu o pedido de {npc.name}: {quest.title}.",
                           player.id, npc.id, player.position, context={"kind": quest.kind})
        if quest.kind == "food" and sum(q.status == "completed" and q.kind == "food" and
                self.world.characters[q.owner_id].town_id == npc.town_id for q in self.world.quests.values()) >= 3:
            player.nickname = f"Protetor de {self.world.towns[npc.town_id].name}"

    def informed(self, giver, receiver, fact):
        if not giver.is_player or fact.confidence < 30:
            return
        for quest in self.world.quests.values():
            if (quest.owner_id == receiver.id and quest.status == "accepted" and
                    quest.kind in ("family", "information") and quest.target_id == fact.target_id and
                    fact.kind in ("PersonLocated", "CharacterDied", "CharacterKilled", "RemainsLocated") and
                    (fact.kind != "PersonLocated" or fact.turn >= quest.created_at)):
                self.complete(quest, giver)

    def supported(self, giver, receiver, event_kind):
        if giver.is_player:
            for quest in self.world.quests.values():
                if quest.owner_id == receiver.id and quest.status == "accepted" and (
                        quest.kind == "companionship" and event_kind == "ComfortGiven" or
                        quest.kind == "protection" and event_kind == "ProtectionGiven"):
                    self.complete(quest, giver)

    def delivered(self, player, npc, kind: str, urgency: float = 0) -> None:
        self.recorder.emit("HelpGiven", f"{player.name} entregou {NAMES[kind].lower()} a {npc.name}.",
                           player.id, npc.id, npc.position, context={"urgency": urgency, "item_kind": kind})
        for quest in self.world.quests.values():
            if quest.status == "accepted" and (
                    quest.kind == "food" and kind == "food" and quest.owner_id == npc.id or
                    quest.kind == "family_care" and quest.target_id == npc.id and kind == quest.context.get("resource", "food")):
                self.complete(quest, player)

    def reconcile(self) -> None:
        for quest in self.world.quests.values():
            if quest.status not in ("offered", "accepted"):
                continue
            owner = self.world.characters[quest.owner_id]
            need = next((n for n in owner.needs.values() if n.id == quest.need_id), None)
            if not owner.alive:
                quest.status = "failed"
            elif need and need.status == "satisfied":
                quest.status = "resolved_elsewhere"
            elif need and need.status in ("expired", "failed"):
                quest.status = "failed"
        # Pedidos concluídos não desaparecem: fazem parte da campanha do jogador.
