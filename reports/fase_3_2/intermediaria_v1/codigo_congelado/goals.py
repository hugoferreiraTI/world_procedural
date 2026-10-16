"""Alternativas avaliadas pela personalidade, seguidas de execução e reavaliação."""

from dataclasses import dataclass, field

from .models import Goal, Location, Personality
from types import SimpleNamespace
from .navigation import distance
from .rules import UTILITY, FEEDING
from .feeding import ACQUISITIONS, MEALS
from .utility import evaluate
from .personal import PERSONAL_KINDS


@dataclass
class Solution:
    action: str
    score: float
    destination: Location | None = None
    target_id: int | None = None
    considerations: dict[str, float] = field(default_factory=dict)
    feeding: dict | None = None


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
        self.feeding = None
        self.rejected_food = {}

    def solutions(self, character, need) -> list[Solution]:
        places = character.known_places
        choices = []
        if need.kind in ("food", "food_reserve"):
            owned = self.items.count(character.id, "food")
            if owned and need.kind == "food" and character.hunger >= FEEDING.meal_threshold:
                choices.append(Solution("eat", 0))
            if owned >= self.feeding.reserve_target(character):
                return self._evaluate(character, need, choices)
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
            income_target = self.feeding.reserve_target(character) if need.kind == 'food_reserve' else 1
            if (character.profession not in (None, "estudante") or character.training_target) and self.economy.known_unaffordable(character, income_target):
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
        if need.kind in ("food", "food_reserve", "work", "money", "advancement", "status"):
            seen = character.market_observation
            fresh = seen.get("town_id") == character.town_id and self.world.turn-seen.get("turn",-1000)<=24
            if character.training_target:
                choices = [c for c in choices if c.action != "work"]
                choices.append(Solution("train",0,character.known_places.get("market")))
            elif fresh:
                if self.professions.saturated(character,seen):
                    choices = [c for c in choices if c.action != "work"]
                if seen.get("temporary_work") and self.professions.temporary_eligible(character):
                    offers = seen.get('temporary_offers', {})
                    if offers.get('food_preparation', {}).get('capacity', 0) and "forage" in places:
                        choices.append(Solution("work_for_food",0,places["forage"]))
                    if offers.get('meal_distribution', {}).get('capacity', 0) and "market" in places:
                        choices.append(Solution("temporary_service",0,places["market"]))
                if seen.get("training_offer") and character.category=="comum" and character.profession in (None,"agricultor","mineiro","lenhador","ferreiro","caçador","comerciante"):
                    choices.append(Solution("train",0,places.get("market")))
            choices = [c for c in choices if c.action != 'work' or self.professions.compatible_workplace(character)]
        if need.kind == "food" and self.feeding.immediate_meal_needed(character):
            for action, original in MEALS.items():
                for choice in list(choices):
                    if choice.action != original:
                        continue
                    if original == "ask_help" and self.world.characters[choice.target_id].is_player:
                        continue  # Pedido ao jogador não é entrega imediata garantida.
                    choices.append(Solution(action, 0, choice.destination, choice.target_id))
        return self._evaluate(character, need, choices)

    def _evaluate(self, character, need, choices):
        available, rejected = [], []
        for choice in choices:
            action = MEALS.get(choice.action, choice.action)
            if (action in ("work_for_food", "temporary_service") and choice.action not in MEALS and
                    self.items.count(character.id, 'food') > self.feeding.reserve_target(character)):
                continue
            if (need.kind == 'family' and action in ACQUISITIONS and
                    self.items.count(character.id, 'food') >= self.feeding.reserve_target(character)+1):
                continue  # Reserva própria mais uma provisão para o familiar.
            if max(character.failures.get(choice.action, 0), character.failures.get(action, 0)) > self.world.turn:
                continue
            if action == "ask_help" and character.failures.get(f"request:{choice.target_id}", 0) > self.world.turn:
                continue
            if choice.destination:
                if choice.destination.map_id != character.position.map_id:
                    continue
            travel = distance(character.position, choice.destination) if choice.destination else 0
            terms = self.social.considerations(character, choice.target_id) if action in (
                "ask_help", "ask_personal_help", "seek_company", "denounce", "give_supplies") else {}
            if action == "train":
                terms.update({"local_demand":1.,"financial_pressure":min(1,max(0,20-character.money)/20),
                    "training_cost":max(0,36-character.personality.diligence//5)/36,
                    "current_job_value":0. if self.professions.saturated(character,character.market_observation) else .5,
                    "risk":max(character.hunger,character.thirst)/100})
            choice.score, choice.considerations = evaluate(action, character, terms, travel)
            if need.kind in ("food", "food_reserve"):
                choice.feeding = self.feeding.estimate(character, choice)
                if choice.feeding and not choice.feeding['survival_viable']:
                    rejected.append(choice)
                    continue
            available.append(choice)
        self.rejected_food[character.id] = rejected
        return sorted(available, key=lambda choice: (-choice.score, choice.action, choice.target_id or 0))

    def choose(self, alternatives):
        near = [s for s in alternatives if alternatives[0].score - s.score <= UTILITY.close_choices]
        if len(near) == 1:
            return near[0]
        return max(near, key=lambda s: s.score + self.rng.uniform(-UTILITY.variation, UTILITY.variation))

    def decide(self, character, elapsed: int = 1) -> None:
        self.economy.observe(character)
        character.food_state['food_before_decision'] = self.items.count(character.id, "food")
        character.food_state['last_decision_turn'] = self.world.turn
        active = self.needs.refresh(character)
        if not active:
            # Rotina sem pressão: retornar para casa. Não abandona o mundo parado.
            self.navigation.approach(character, character.home, elapsed)
            character.goal = None
            return
        selected, choice = None, None
        for need in active:
            alternatives = self.solutions(character, need)
            if need.kind in ("food", "food_reserve"):
                self.feeding.rejected(character, need, self.rejected_food.get(character.id, []))
            if alternatives:
                selected, choice = need, self.choose(alternatives)
                break
            need.status = "blocked"
            if not need.context.get("blocked_recorded"):
                self.needs.count("Blocked", need.kind, character)
                need.context["blocked_recorded"] = True
        if selected is None:
            for need in active:
                if need.kind in PERSONAL_KINDS:
                    self.needs.explain(character,need,"NoViableSolution")
            character.goal = None
            return
        current = character.goal
        if character.suspended_goal and not self.feeding.emergency(character) and choice.action != "eat":
            paused = character.suspended_goal
            paused_need = next((n for n in active if n.id == paused.need_id), None)
            if paused_need and any(s.action == paused.action and s.target_id == paused.target_id and
                                   s.destination == paused.destination for s in self.solutions(character, paused_need)):
                current = paused
                current.status = "active"
                character.goal = paused
            character.suspended_goal = None
        meal_interrupt = choice.action == "eat" or (
            choice.action in MEALS and self.feeding.immediate_meal_needed(character))
        # Mantém uma viagem em andamento enquanto outra necessidade não é
        # claramente mais urgente. Fome e sede próximas não devem fazer o
        # personagem alternar destinos a cada hora sem concluir nenhuma ação.
        if current and current.status == "active" and not meal_interrupt and not selected.context.get('emergency'):
            current_need = next((need for need in active if need.id == current.need_id), None)
            if current_need and selected.priority < current_need.priority + 12:
                continuing = next((solution for solution in self.solutions(character, current_need)
                                   if solution.action == current.action and
                                   solution.target_id == current.target_id and
                                   solution.destination == current.destination), None)
                if continuing:
                    selected, choice = current_need, continuing
        for need in active:
            if need.kind not in PERSONAL_KINDS:
                continue
            if need is selected:
                need.context["selections"] = need.context.get("selections",0)+1
                self.needs.explain(character,need,"Selected")
            elif not self.solutions(character,need):
                need.status = "blocked"
                if not need.context.get("blocked_recorded"):
                    self.needs.count("Blocked",need.kind,character)
                    need.context["blocked_recorded"] = True
                self.needs.explain(character,need,"NoViableSolution")
                if need.target_id and need.target_id not in character.observations and not need.context.get("known_location"):
                    self.needs.explain(character,need,"UnknownRequiredInformation")
                elif need.target_id and need.target_id in character.observations and not character.observations[need.target_id].alive:
                    self.needs.explain(character,need,"TargetUnavailable")
            else:
                reason = ("LostToHigherPriority" if selected.priority > need.priority else
                          "LostToTieBreak" if selected.priority == need.priority else "LostToGoalContinuation")
                self.needs.explain(character,need,reason,selected.kind)
        if choice.destination:
            character.food_state['planned_trip'] = self.feeding.travel_assessment(character, choice.destination)
        preparation = self.preventive_choice(character,choice)
        if preparation:
            choice = preparation
            self.world.metrics["PreventiveActionSelected"] = self.world.metrics.get("PreventiveActionSelected",0)+1
        if (current and current.status == "active" and choice.action != current.action and
                (choice.action == "eat" or choice.action in MEALS)):
            character.suspended_goal = current
            current.status = "suspended"
            self.feeding.interrupted(character, current, choice.action)
        if selected.kind in ("food", "food_reserve") and choice.action != "eat":
            self.feeding.search_started(character, choice)
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
                                "considerations": s.considerations, "feeding": s.feeding}
                               for s in self.solutions(character, selected)],
                "rejected_food_solutions": [{"action": s.action, "feeding": s.feeding}
                                             for s in self.rejected_food.get(character.id, [])]}
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
            if current.action != 'ask_personal_help' or not selected.context.get('recent_replies'):
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
        if (current.action == "eat" or current.action in MEALS) and character.hunger < FEEDING.meal_threshold:
            self.needs.satisfy(character, "food")
        elif current.action in ("drink", "drink_well", "drink_stream") and character.thirst < 25:
            self.needs.satisfy(character, "water")
        elif current.action == "sleep" and character.fatigue < 25:
            self.needs.satisfy(character, "rest")

    def execute(self, character, goal, hours: int) -> tuple[bool, str]:
        if goal.action in ("work_for_food", "temporary_service"):
            deficit = max(1, self.feeding.reserve_target(character)-self.items.count(character.id, 'food'))
            hours = min(hours, deficit)
        elif goal.action in MEALS:
            hours = 1  # Uma operação explícita de refeição, sem lote retroativo.
        result = self._execute(character,goal,hours)
        if result[0]:
            character.last_successful_action = {"action":goal.action,"turn":self.world.turn}
            if goal.action == "eat" or goal.action in MEALS: character.last_meal = self.world.turn
            if goal.action in ("drink","drink_well","drink_stream"):
                character.last_drink = self.world.turn
                self.world.metrics["WaterSourceReached"] = self.world.metrics.get("WaterSourceReached",0)+1
                if goal.destination:
                    key="WaterTravelHours"
                    self.world.metrics[key]=self.world.metrics.get(key,0)+max(0,self.world.turn-goal.created_at)
        return result

    def _execute(self, character, goal, hours: int) -> tuple[bool, str]:
        action = goal.action
        if action in MEALS:
            acquisition = Goal(goal.id, goal.need_id, MEALS[action], goal.score, goal.created_at,
                               goal.target_id, goal.destination)
            success, outcome = self._execute(character, acquisition, hours)
            if not success:
                return success, outcome
            meal = Goal(goal.id, goal.need_id, "eat", goal.score, goal.created_at)
            eaten, message = self._execute(character, meal, 1)
            return eaten, outcome+" "+message
        need = next((n for n in character.needs.values() if n.id == goal.need_id), None)
        if action in ("sell_surplus", "check_relative", "give_supplies", "seek_company", "remember_relative",
                      "investigate", "denounce", "avoid_threat", "stay_near", "ask_personal_help"):
            if not need or not self.personal_actions:
                return False, "Falta uma necessidade compatível."
            return self.personal_actions.execute(character, goal, need)
        if action == "eat":
            if self.items.consume(character.id, "food"):
                character.hunger = max(0, character.hunger - FEEDING.meal_reduction)
                self.recorder.emit("FoodEaten", f"{character.name} comeu.",
                                   character.id, location=character.position)
                return True, "Fome reduzida."
            return False, "Comida indisponível."
        if action == "buy_food":
            if need and need.kind == 'food_reserve':
                return self.economy.buy_reserve(character, self.feeding.reserve_target(character),
                                                bulk=need.priority >= 50)
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
        if action == "train":
            return self.professions.train(character,hours)
        if action == "temporary_service":
            return self.professions.temporary_service(character,hours)
        if action == "fill_water":
            town = self.world.towns.get(character.position.map_id)
            _,structures=self.navigation.describe(character.position)
            if not town or "Poço" not in structures or self.items.count(town.id,"water")<1:
                return False,"Não há água para levar nesta fonte."
            amount=min(2,self.items.count(town.id,"water"))
            self.items.transfer(town.id,character.id,self.items.first(town.id,"water"),amount)
            return True,"Reserva de água obtida na fonte local."
        if action == "sleep":
            self.needs.rest(character, hours)
            return True, "Descanso realizado."
        if action == "work_for_food":
            return self.professions.casual_work(character, hours)
        if action == "work":
            result = self.professions.work(character, hours)
            key = 'WorkOutcome:'+result.status
            self.world.metrics[key] = self.world.metrics.get(key, 0)+1
            return tuple(result)
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

    def preventive_choice(self, person, choice):
        # Uma refeição vital precede água para viagem e qualquer outro preparo.
        if (self.items.count(person.id, "food") and self.feeding.emergency(person) and
                choice.action not in ("drink", "drink_well", "drink_stream")):
            return Solution("eat", 200)
        if choice.action in MEALS:
            return None
        if not choice.destination or choice.action in ("eat","drink","drink_well","drink_stream","fill_water","buy_food","forage"):
            return None
        travel=distance(person.position,choice.destination)
        if travel<3 or travel>=1000:
            return None
        horizon=travel+FEEDING.travel_margin_hours
        if person.thirst+2*horizon>=80:
            if self.items.count(person.id,"water") and person.thirst>=25:
                return Solution("drink",200)
            sources=[p for key,p in person.known_places.items() if key.startswith("well") or key=="market"]
            nearby=[p for p in sources if p.map_id==person.position.map_id and distance(person.position,p)<=travel]
            if not self.items.count(person.id,"water") and nearby:
                return Solution("fill_water",100,min(nearby,key=lambda p:distance(person.position,p)))
        if person.hunger+FEEDING.hunger_per_hour*horizon>=FEEDING.high_hunger:
            if self.items.count(person.id,"food") and person.hunger>=FEEDING.meal_threshold:
                return Solution("eat",200)
            seen=person.market_observation
            if (seen.get("price") and self.world.turn-seen.get("price_turn",-1000)<=24 and
                    seen.get("stock",{}).get("food",0)>0 and person.money>=seen["price"] and
                    not self.items.count(person.id,"food") and "market" in person.known_places):
                preparation = Solution("buy_food",75,person.known_places["market"])
                if self.feeding.estimate(person, preparation)['survival_viable']:
                    return preparation
        return None

    def collective(self,town,need,report):
        """Mesmos Solution/Goal/utility; ações administrativas não movem NPCs."""
        proxy=SimpleNamespace(personality=Personality(),profession=None)
        actions=[]
        tags=report['bottlenecks']
        if 'RAW_MATERIAL_SHORTAGE' in tags and self.items.count(town.id,'grain')<240 and town.abstract_population:
            actions.append(('expand_farming',40))
        else:
            actions.append(('improve_utilization',5))
            if report['stock']['food']<report['expected_demand']*2 or 'AFFORDABILITY_PROBLEM' in tags:
                actions.append(('publish_temporary_work',15))
            vacancy=town.professional_demand.get('cozinheiro',{})
            age=self.world.turn-vacancy.get('since',self.world.turn)
            people=[self.world.characters[i] for i in town.resident_ids]
            if vacancy.get('projected_deficit',vacancy.get('deficit')) and age>=48:
                if any(self.professions.suitable_candidate(c,town) for c in people):
                    actions.append(('open_training',30))
                elif age>=72 and self.professions.can_materialize(town):
                    actions.append(('materialize_worker',40))
        choices=[]
        for action,context in actions:
            score,terms=evaluate(action,proxy)
            choices.append(Solution(action,score+context,considerations=terms))
        choices.sort(key=lambda s:(-s.score,s.action))
        choice=self.choose(choices)
        town.goal=Goal(self.world.allocate_id(),need.id,choice.action,choice.score,self.world.turn)
        need.status='selected'
        self.needs.count('Selected',need.kind,town)
        success=True
        if choice.action=='expand_farming':
            units=min(report['raw_required'],(town.abstract_population or 0)//100,town.money,
                      max(0,240-self.items.count(town.id,'grain')))
            if units:
                town.money-=units; town.abstract_money+=units
                self.items.create(town.id,'grain',units,origin='Colheita de trabalhadores locais')
                self.professions.record_production(town,'grain',units)
            success=bool(units)
        elif choice.action=='materialize_worker':
            success=self.professions.materialize(town)
        vacancy=town.professional_demand.get('cozinheiro')
        if vacancy:
            vacancy['stage']=choice.action
        town.goal.status='completed' if success else 'failed'
        if not success: need.status='blocked'
        if need.context.get('last_response')!=choice.action:
            self.recorder.emit('LocalEconomicResponse',f'{town.name} decidiu: {choice.action}.',target_id=town.id,
                               location=town.market,context={'action':choice.action,'bottlenecks':tags})
        need.context['last_response']=choice.action
