"""Alternativas avaliadas pela personalidade, seguidas de execução e reavaliação."""

from dataclasses import dataclass, field

from .models import Goal, Location
from .navigation import distance
from .rules import UTILITY
from .utility import evaluate
from .personal import PERSONAL_KINDS


@dataclass
class Solution:
    action: str
    score: float
    destination: Location | None = None
    target_id: int | None = None
    considerations: dict[str, float] = field(default_factory=dict)


class GoalSystem:
    def __init__(self, world, needs, items, economy, professions, navigation,
                 graph, spatial, recorder, social, rng, quests):
        self.world, self.needs, self.items, self.economy = world, needs, items, economy
        self.professions, self.navigation, self.graph = professions, navigation, graph
        self.spatial, self.recorder = spatial, recorder
        self.social, self.rng, self.quests = social, rng, quests
        self.debug = False
        self.traces = {}
        self.personal_actions = None

    def solutions(self, character, need) -> list[Solution]:
        places = character.known_places
        choices = []
        if need.kind == "food":
            if self.items.count(character.id, "food"):
                choices.append(Solution("eat", 0))
            if "market" in places:
                # A intenção de comprar não conhece remotamente o preço nem o estoque.
                town = self.world.towns[character.town_id]
                local = character.position == places["market"] == town.market
                if self.economy.can_seek_food(character):
                    choices.append(Solution("buy_food", 0, places["market"]))
                if not local or self.items.count(town.id, "food"):
                    choices.append(Solution("steal", 0, places["market"]))
            if "forage" in places:
                choices.append(Solution("forage", 0, places["forage"]))
            peers = [entity_id for entity_id in self.spatial.at(character.position)
                     if self.social.can_request(character, self.world.characters[entity_id])]
            if need.priority >= 50:
                for target in peers:
                    choices.append(Solution("ask_help", 0, target_id=target))
            if character.profession not in (None, "estudante") and character.money < 5:
                choices.append(Solution("work", 0, character.workplace))
            elif character.profession is None and "forage" in places:
                choices.append(Solution("work_for_food", 0, places["forage"]))
        elif need.kind == "water":
            if self.items.count(character.id, "water"):
                choices.append(Solution("drink", 0))
            if "market" in places:
                choices.append(Solution("drink_well", 0, places["market"]))
                for key in ("well_home", "well_rural"):
                    if key in places:
                        choices.append(Solution("drink_well", 0, places[key]))
            elif "forage" in places:
                choices.append(Solution("drink_stream", 0, places["forage"]))
        elif need.kind == "rest":
            choices.append(Solution("sleep", 0, character.home))
        elif need.kind in ("work", "money"):
            choices.append(Solution("work", 0, character.workplace))
        elif need.kind == "security":
            event_id = int(need.source.split(":")[1])
            fact = character.knowledge.get(event_id)
            if fact and fact.location:
                choices.append(Solution("secure", 0, fact.location, need.target_id))
        if self.personal_actions and need.kind in PERSONAL_KINDS | {"money"}:
            existing = {(s.action, s.destination, s.target_id) for s in choices}
            for action, destination, target in self.personal_actions.candidates(character, need):
                if (action, destination, target) not in existing:
                    choices.append(Solution(action, 0, destination, target))
                    existing.add((action, destination, target))
        available = []
        for choice in choices:
            if character.failures.get(choice.action, 0) > self.world.turn:
                continue
            if choice.action == "ask_help" and character.failures.get(f"request:{choice.target_id}", 0) > self.world.turn:
                continue
            if choice.destination:
                if choice.destination.map_id != character.position.map_id:
                    continue
            travel = distance(character.position, choice.destination) if choice.destination else 0
            terms = self.social.considerations(character, choice.target_id) if choice.action in (
                "ask_help", "ask_personal_help", "seek_company", "denounce", "give_supplies") else {}
            choice.score, choice.considerations = evaluate(choice.action, character, terms, travel)
            available.append(choice)
        return sorted(available, key=lambda choice: (-choice.score, choice.action, choice.target_id or 0))

    def choose(self, alternatives):
        near = [s for s in alternatives if alternatives[0].score - s.score <= UTILITY.close_choices]
        if len(near) == 1:
            return near[0]
        return max(near, key=lambda s: s.score + self.rng.uniform(-UTILITY.variation, UTILITY.variation))

    def decide(self, character, elapsed: int = 1) -> None:
        active = self.needs.refresh(character)
        if not active:
            # Rotina sem pressão: retornar para casa. Não abandona o mundo parado.
            self.navigation.approach(character, character.home, elapsed)
            character.goal = None
            return
        selected, choice = None, None
        for need in active:
            alternatives = self.solutions(character, need)
            if alternatives:
                selected, choice = need, self.choose(alternatives)
                break
            need.status = "blocked"
            if not need.context.get("blocked_recorded"):
                self.needs.count("Blocked", need.kind, character)
                need.context["blocked_recorded"] = True
        if selected is None:
            character.goal = None
            return
        current = character.goal
        # Mantém uma viagem em andamento enquanto outra necessidade não é
        # claramente mais urgente. Fome e sede próximas não devem fazer o
        # personagem alternar destinos a cada hora sem concluir nenhuma ação.
        if current and current.status == "active":
            current_need = next((need for need in active if need.id == current.need_id), None)
            if current_need and selected.priority < current_need.priority + 12:
                continuing = next((solution for solution in self.solutions(character, current_need)
                                   if solution.action == current.action and
                                   solution.target_id == current.target_id and
                                   solution.destination == current.destination), None)
                if continuing:
                    selected, choice = current_need, continuing
        selected.status = "selected"
        self.needs.count("Selected", selected.kind, character)
        if self.debug:
            self.traces[character.id] = {"turn": self.world.turn, "need": selected.kind,
                "priority": selected.priority, "selected": choice.action, "target_id": choice.target_id,
                "source": selected.source, "reason": selected.reason, "context": dict(selected.context),
                "active_needs": [{"kind": n.kind, "priority": n.priority, "target_id": n.target_id,
                                  "source": n.source, "reason": n.reason, "status": n.status,
                                  "base": n.base_urgency,
                                  "personality_modifier": self.needs.personal.priority_modifier(character, n)
                                  if self.needs.personal else 0} for n in active],
                "candidates": [{"action": s.action, "target_id": s.target_id, "score": s.score,
                                "considerations": s.considerations}
                               for s in self.solutions(character, selected)]}
        if not (current and current.status == "active" and current.need_id == selected.id and
                current.action == choice.action and current.target_id == choice.target_id and
                current.destination == choice.destination):
            current = Goal(self.world.allocate_id(), selected.id, choice.action, choice.score,
                           self.world.turn, choice.target_id, choice.destination)
            character.goal = current
        if current.destination and character.position != current.destination:
            # Tempo de viagem é consumido antes da ação; não recebe horas de
            # produção por um intervalo que passou caminhando.
            steps = min(elapsed, distance(character.position, current.destination))
            arrived = self.navigation.approach(character, current.destination, steps)
            if not arrived:
                return
            elapsed -= steps
            if elapsed <= 0:
                return
        success, outcome = self.execute(character, current, max(1, elapsed))
        current.status = "completed" if success else "failed"
        current.outcome = outcome
        if not success:
            character.failures[current.action] = self.world.turn + 12
            selected.status = "active"
            if selected.kind in ("food", "money") and current.action in ("work", "buy_food", "ask_help"):
                character.financial_setbacks = min(20, character.financial_setbacks + 1)
        elif selected.kind == "status" and current.action == "work":
            self.recorder.emit("ResponsibilityFulfilled", f"{character.name} cumpriu uma responsabilidade local.",
                               character.id, location=character.position,
                               context={"profession": character.profession, "need_source": selected.source})
            self.needs.finish(character, selected)
        # A necessidade depende do estado, não do sucesso nominal de uma ação.
        if current.action == "eat" and character.hunger < 25:
            self.needs.satisfy(character, "food")
        elif current.action in ("drink", "drink_well", "drink_stream") and character.thirst < 25:
            self.needs.satisfy(character, "water")
        elif current.action == "sleep" and character.fatigue < 25:
            self.needs.satisfy(character, "rest")

    def execute(self, character, goal, hours: int) -> tuple[bool, str]:
        action = goal.action
        need = next((n for n in character.needs.values() if n.id == goal.need_id), None)
        if action in ("sell_surplus", "check_relative", "give_supplies", "seek_company", "remember_relative",
                      "investigate", "denounce", "avoid_threat", "stay_near", "ask_personal_help"):
            if not need or not self.personal_actions:
                return False, "Falta uma necessidade compatível."
            return self.personal_actions.execute(character, goal, need)
        if action == "eat":
            if self.items.consume(character.id, "food"):
                character.hunger = max(0, character.hunger - 40)
                self.recorder.emit("FoodEaten", f"{character.name} comeu.",
                                   character.id, location=character.position)
                return True, "Fome reduzida."
            return False, "Comida indisponível."
        if action == "buy_food":
            return self.economy.buy(character.id, character.town_id, "food")
        if action in ("drink", "drink_well", "drink_stream"):
            if action == "drink":
                success = self.items.consume(character.id, "water")
            elif action == "drink_well":
                town = self.world.towns.get(character.position.map_id)
                _, structures = self.navigation.describe(character.position)
                success = bool(town and "Poço" in structures and self.items.consume(town.id, "water"))
            else:
                success = character.position == character.known_places.get("forage")
            if success:
                character.thirst = max(0, character.thirst - 45)
            return success, "Sede reduzida." if success else "Não há água disponível."
        if action == "sleep":
            self.needs.rest(character, hours)
            return True, "Descanso realizado."
        if action == "work_for_food":
            return self.professions.casual_work(character, hours)
        if action == "work":
            before = character.money
            need = next((need for need in character.needs.values() if need.id == goal.need_id), None)
            if need and need.kind in ("food", "money") and self.world.towns[character.town_id].money == 0:
                return False, "O trabalho não pode pagar agora; buscar outra solução."
            success, outcome = self.professions.work(character, hours)
            if success and need and need.kind in ("food", "money") and character.money <= before:
                return False, "O trabalho não trouxe o pagamento necessário; buscar outra solução."
            return success, outcome
        if action == "forage":
            if character.position != character.known_places.get("forage"):
                return False, "Vá até uma área conhecida de coleta."
            town = self.world.towns[character.town_id]
            if character.position.map_id == town.id:
                if town.wild_food <= 0:
                    return False, "Os alimentos silvestres locais acabaram por hoje."
                town.wild_food -= 1
            self.items.create(character.id, "food", creator_id=character.id,
                              origin="Coleta local de alimentos")
            self.recorder.emit("FoodGathered", f"{character.name} coletou alimentos.",
                               character.id, location=character.position)
            return True, "Alimento coletado."
        if action == "ask_help":
            target = self.world.characters.get(goal.target_id)
            if not target or not target.alive or target.position != character.position:
                return False, "A pessoa procurada não está aqui."
            if target.is_player:
                quest = self.quests.offer(character, target, origin="autonomous")
                if quest:
                    character.failures[f"request:{target.id}"] = self.world.turn + 24
                return bool(quest), "Pedido apresentado ao jogador." if quest else "Pedido indisponível."
            if self.social.willing_to_feed(target, character):
                self.items.transfer(target.id, character.id, self.items.first(target.id, "food"))
                self.recorder.emit("HelpGiven", f"{target.name} deu comida a {character.name}.",
                                   target.id, character.id, character.position,
                                   context={"urgency": character.hunger})
                return True, "Recebeu ajuda."
            return False, "Não foi possível obter ajuda."
        if action == "steal":
            town = self.world.towns[character.town_id]
            item_id = self.items.first(town.id, "food")
            if character.position != town.market or item_id is None:
                return False, "Nenhum alimento acessível."
            self.items.transfer(town.id, character.id, item_id)
            self.recorder.emit("ItemStolen", f"{character.name} roubou comida no mercado de {town.name}.",
                               character.id, town.id, character.position)
            return True, "Alimento roubado."
        if action == "secure":
            need = character.needs["security"]
            event_id = int(need.source.split(":")[1])
            suspect = self.world.characters.get(goal.target_id)
            character.failures[f"crime:{event_id}"] = self.world.turn + 24
            self.needs.satisfy(character, "security")
            if suspect and suspect.alive and suspect.position == character.position:
                fine = min(5, suspect.money)
                suspect.money -= fine
                self.world.towns[character.town_id].money += fine
                self.recorder.emit("GuardResponded", f"{character.name} interveio no roubo e cobrou {fine} moedas de {suspect.name}.",
                                   character.id, suspect.id, character.position)
                return True, "Suspeito encontrado; intervenção registrada."
            return True, "O guarda investigou o último local conhecido; o suspeito não estava lá."
        return False, "Ação desconhecida."
