"""Candidatos e execução pessoais chamados pelo GoalSystem existente."""

from .needs import FINISHED
from .personal import PERSONAL_KINDS


class PersonalActions:
    def __init__(self, engine):
        self.world, self.needs, self.items = engine.world, engine.needs, engine.items
        self.personal, self.knowledge = engine.needs.personal, engine.knowledge
        self.spatial, self.social, self.graph = engine.spatial, engine.social, engine.graph
        self.economy, self.recorder, self.quests = engine.economy, engine.recorder, engine.quests

    def available_surplus(self, person):
        for item_id, quantity in person.inventory.items():
            kind = self.world.items[item_id].kind
            if kind in ("grain", "iron", "wood") or kind == "food" and quantity > 2 and person.hunger < 55:
                return item_id
        return None

    def candidates(self, person, need):
        """Somente enumera intenções; utility e escolha continuam no GoalSystem."""
        choices, here = [], self.spatial.at(person.position)
        location = self.personal.location(need.context)
        peers = [self.world.characters[i] for i in here if i != person.id]
        if need.kind in ("money", "advancement"):
            if person.profession not in (None, "estudante"):
                choices.append(("work", person.workplace, None))
            if self.available_surplus(person) and "market" in person.known_places:
                choices.append(("sell_surplus", person.known_places["market"], None))
        elif need.kind == "family":
            if need.target_id in here:
                if need.context.get("mode") == "missing":
                    choices.append(("check_relative", None, need.target_id))
                else:
                    resource = need.context.get("resource", "food")
                    if self.items.count(person.id, resource) > (1 if resource == "food" and person.hunger >= 25 else 0):
                        choices.append(("give_supplies", None, need.target_id))
                    if resource == "food" and person.hunger < 55:
                        if self.economy.can_seek_food(person):
                            choices.append(("buy_food", person.known_places["market"], None))
                        if "forage" in person.known_places:
                            choices.append(("forage", person.known_places["forage"], None))
            elif location and not need.context.get("searched"):
                choices.append(("check_relative", location, need.target_id))
        elif need.kind == "grief":
            for peer in peers:
                if self.graph.value(person.id, peer.id, "amizade") >= 20 or self.social.known(person, peer.id):
                    choices.append(("seek_company", None, peer.id))
            choices.append(("remember_relative", location or person.home, need.target_id))
        elif need.kind in ("revenge", "protection"):
            if need.kind == "revenge" and need.target_id is not None and location and not need.context.get("investigated"):
                choices.append(("investigate", location, need.target_id))
            for target, observation in person.observations.items():
                if (observation.alive and observation.profession == "guarda" and not need.context.get("reported")
                        and need.context.get("source_event") in person.knowledge):
                    choices.append(("denounce", observation.position, target))
            safe = person.home if location != person.home else person.known_places.get("forage")
            if safe and person.personality.courage < 65 and not need.context.get("avoided"):
                choices.append(("avoid_threat", safe, None))
            protected = need.context.get("protected")
            if need.kind == "protection" and protected in here and protected != person.id:
                choices.append(("stay_near", None, protected))
        elif need.kind == "status":
            for peer in peers:
                if peer.hunger >= 55 and self.items.count(person.id, "food") > 1 and person.hunger < 65:
                    choices.append(("give_supplies", None, peer.id))
            if person.profession not in (None, "estudante"):
                choices.append(("work", person.workplace, None))
        if need.kind in ("family", "revenge", "protection", "grief"):
            for peer in peers:
                if self.social.can_request(person, peer) and person.failures.get(f"request:{peer.id}", 0) <= self.world.turn:
                    choices.append(("ask_personal_help", None, peer.id))
        return choices

    def inform(self, giver, receiver, fact):
        if giver.position != receiver.position or fact.required_trust > self.graph.value(giver.id, receiver.id, "confiança", 10):
            return False, "Informação indisponível neste encontro."
        received = self.knowledge.transmitted(fact, giver, receiver)
        self.knowledge.learn(receiver, received, False)
        self.recorder.emit("InformationShared", f"{giver.name} informou {receiver.name}: {fact.description}",
                           giver.id, receiver.id, giver.position, context={"fact_id": fact.event_id})
        self.quests.informed(giver, receiver, received)
        return True, "Informação transmitida."

    def locate(self, observer, target_id):
        target = self.world.characters.get(target_id)
        if not target or target.position != observer.position or target_id == observer.id:
            return False, "A pessoa não foi localizada nesta posição."
        if not target.alive:
            self.recorder.emit("RemainsLocated", f"{observer.name} identificou os restos de {target.name}.",
                               observer.id, target.id, observer.position, witnesses=[observer.id])
            return True, "Morte confirmada no local; o fato pode ser informado."
        self.recorder.emit("PersonLocated", f"{observer.name} localizou {target.name}.",
                           observer.id, target.id, observer.position, witnesses=[observer.id],
                           context={"hunger": target.hunger, "thirst": target.thirst, "health": target.health})
        return True, "Pessoa localizada; o fato pode ser informado a outro personagem."

    def accompany(self, giver, receiver):
        if giver.position != receiver.position or not receiver.alive:
            return False, "A pessoa não está aqui."
        kinds = {n.kind for n in receiver.needs.values() if n.status not in FINISHED}
        if not kinds.intersection({"grief", "protection"}):
            return False, "Não há necessidade conhecida de companhia ou proteção."
        kind = "ComfortGiven" if "grief" in kinds else "ProtectionGiven"
        self.recorder.emit(kind, f"{giver.name} permaneceu ao lado de {receiver.name}.",
                           giver.id, receiver.id, giver.position, context={"urgency": 50})
        self.quests.supported(giver, receiver, kind)
        return True, "Companhia prestada neste encontro."

    def execute(self, person, goal, need):
        action, target = goal.action, self.world.characters.get(goal.target_id)
        if action == "sell_surplus":
            item_id = self.available_surplus(person)
            if item_id is None:
                return False, "Não há excedente disponível."
            return self.economy.sell(person.id, person.town_id, item_id)
        if action == "check_relative":
            found, message = self.locate(person, goal.target_id)
            if found:
                self.needs.finish(person, need)
            else:
                need.context["searched"] = True
                self.recorder.emit("FamilySearch", f"{person.name} verificou um local conhecido sem encontrar o familiar.",
                                   person.id, location=person.position, witnesses=[person.id],
                                   context={"relative_id": need.target_id, "source": need.source})
            return True, message
        if action == "give_supplies":
            if not target or target.id not in self.spatial.at(person.position):
                return False, "O destinatário não está aqui."
            resource = need.context.get("resource", "food")
            item_id = self.items.first(person.id, resource)
            if item_id is None or resource == "food" and person.hunger >= 65:
                return False, "Não há provisões disponíveis para ajudar."
            urgency = (target.hunger if resource == "food" else target.thirst) if not self.items.count(target.id, resource) else 0
            self.items.transfer(person.id, target.id, item_id)
            self.recorder.emit("HelpGiven", f"{person.name} entregou provisões a {target.name}.",
                               person.id, target.id, person.position,
                               context={"urgency": urgency, "item_kind": resource})
            self.needs.finish(person, need)
            return True, "Ajuda material prestada."
        if action == "seek_company":
            if not target or target.id not in self.spatial.at(person.position):
                return False, "A companhia procurada não está aqui."
            self.recorder.emit("ComfortGiven", f"{target.name} ouviu {person.name} durante seu luto.",
                               target.id, person.id, person.position, context={"urgency": need.priority})
            self.needs.finish(person, need)
            return True, "Buscou companhia para lidar com a perda."
        if action == "remember_relative":
            self.recorder.emit("Remembrance", f"{person.name} dedicou um momento à memória de uma pessoa próxima.",
                               person.id, location=person.position, witnesses=[person.id],
                               context={"relative_id": need.target_id, "source": need.source})
            self.needs.finish(person, need)
            return True, "Visitou um local relacionado à perda."
        if action == "investigate":
            self.locate(person, goal.target_id)
            need.context["investigated"] = True
            self.recorder.emit("InvestigationPerformed", f"{person.name} verificou o último local conhecido do responsável.",
                               person.id, location=person.position, witnesses=[person.id],
                               context={"suspect_id": need.target_id, "source": need.source})
            return True, "Investigou o local conhecido; não houve confronto."
        if action == "denounce":
            fact = person.knowledge.get(need.context.get("source_event"))
            if not target or target.id not in self.spatial.at(person.position) or not fact:
                return False, "Faltam informante, guarda presente ou evidência conhecida."
            success, message = self.inform(person, target, fact)
            if success:
                need.context["reported"] = True
                self.recorder.emit("ThreatReported", f"{person.name} denunciou um acontecimento conhecido a {target.name}.",
                                   person.id, target.id, person.position, context={"fact_id": fact.event_id})
                self.needs.finish(person, need)
            return success, message
        if action == "avoid_threat":
            need.context["avoided"] = True
            self.recorder.emit("ThreatAvoided", f"{person.name} buscou um local seguro conhecido.",
                               person.id, location=person.position, witnesses=[person.id],
                               context={"source": need.source})
            if need.kind == "protection":
                self.needs.finish(person, need)
            return True, "Afastou-se do local da ameaça."
        if action == "stay_near":
            if not target or target.id not in self.spatial.at(person.position):
                return False, "O protegido não está aqui."
            self.recorder.emit("ProtectionGiven", f"{person.name} permaneceu próximo de {target.name}.",
                               person.id, target.id, person.position, context={"source": need.source})
            self.needs.finish(person, need)
            return True, "Acompanhou o protegido."
        if action == "ask_personal_help":
            if not target or target.id not in self.spatial.at(person.position):
                return False, "A pessoa procurada não está aqui."
            if target.is_player:
                quest = self.quests.offer(person, target, origin="autonomous", need=need)
                if quest:
                    person.failures[f"request:{target.id}"] = self.world.turn + 24
                return bool(quest), "Pedido pessoal apresentado." if quest else "Pedido indisponível."
            if need.kind == "grief":
                return self.accompany(target, person)
            if need.kind == "protection" and target.profession == "guarda":
                return self.accompany(target, person)
            query = need.target_id if need.kind == "family" else need.context.get("victim")
            facts = [f for f in target.knowledge.values() if f.target_id == query and
                     f.kind in ("PersonLocated", "CharacterDied", "CharacterKilled", "RemainsLocated")]
            if facts:
                return self.inform(target, person, max(facts, key=lambda f: (f.turn, f.confidence)))
            return False, "O interlocutor não conhece informação útil."
        return False, "Solução pessoal indisponível."
