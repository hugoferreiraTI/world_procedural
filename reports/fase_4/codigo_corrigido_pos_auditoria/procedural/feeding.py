"""Cobertura alimentar, prazo biológico e diagnóstico dentro de Need/Solution.

Não escolhe objetivos nem executa ações. Todas as estimativas usam estado próprio,
destinos conhecidos e observações locais; estoques continuam pertencendo a Items.
"""
import math

from .navigation import distance
from .rules import FEEDING, SURVIVAL

ACQUISITIONS = {"buy_food", "forage", "steal", "ask_help", "work_for_food", "temporary_service"}
MEALS = {"buy_meal": "buy_food", "forage_meal": "forage", "steal_meal": "steal",
         "ask_meal": "ask_help", "work_for_meal": "work_for_food", "service_meal": "temporary_service"}


class FeedingSystem:
    def __init__(self, world, items):
        self.world, self.items = world, items
        self.listeners = []
        self.margin_cache = {}
        items.listeners.append(self.inventory_changed)

    def decision_interval(self, person):
        player = self.world.characters.get(self.world.player_id)
        active=(person.active_until>self.world.turn or person.combat.opponents or person.migration is not None
                and person.migration.arrived_at is None)
        if (active or person.category == "lendário" or person.hunger >= FEEDING.high_hunger or
                person.thirst >= 85 or player and player.alive and distance(person.position, player.position) <= 3):
            person.lod='active'
            return 1
        person.lod='background' if person.position==person.home and person.category=='comum' else 'local'
        return 12 if person.lod=='background' else 3 if person.category == "importante" else 6

    def reserve_target(self, person, destination=None):
        hours = FEEDING.reserve_hours
        if destination is None and person.goal and person.goal.status == "active":
            destination = person.goal.destination
        if destination is not None:
            travel = distance(person.position, destination)
            # Destino de outro mapa não implica conhecimento do trajeto global.
            if travel < 1000:
                hours = max(hours, travel + FEEDING.travel_margin_hours)
        return min(FEEDING.maximum_reserve, math.ceil(hours*FEEDING.hunger_per_hour/FEEDING.meal_reduction))

    def reserve_pressure(self, person, need):
        """Pressão limitada por cobertura e oportunidades que o indivíduo conhece."""
        owned, target = self.items.count(person.id, 'food'), self.reserve_target(person)
        deficit = max(0, target-owned)
        ratio = deficit/max(1, target)
        until_meal = max(0, (FEEDING.meal_threshold-person.hunger)/FEEDING.hunger_per_hour)
        coverage = until_meal + owned*FEEDING.meal_reduction/FEEDING.hunger_per_hour
        horizon = FEEDING.reserve_hours
        market = person.known_places.get('market')
        seen = person.market_observation
        fresh = seen.get('town_id') == person.town_id and self.world.turn-seen.get('price_turn', -1000) <= 24
        affordable = bool(fresh and seen.get('stock', {}).get('food', 0) > 0 and person.money >= seen.get('price', float('inf')))
        market_distance = distance(person.position, market) if market else 1000
        opportunity = max(0, 1-market_distance/6)*8*ratio if affordable else 0
        if market_distance < 1000:
            horizon = market_distance+1+FEEDING.travel_margin_hours
        destination = person.goal.destination if person.goal and person.goal.status == 'active' else None
        travel = distance(person.position, destination) if destination else 0
        leaving = bool(destination and destination != market and travel < 1000)
        next_opportunity = market_distance+1 if market_distance < 1000 else None
        gap = 0
        if leaving and market:
            after_trip = distance(destination, market)
            if after_trip < 1000:
                next_opportunity = travel+after_trip+1
                horizon = max(FEEDING.reserve_hours, horizon, travel+FEEDING.travel_margin_hours)
                gap = min(12, max(0, next_opportunity-coverage)*.5)*ratio
        risk = 18*max(0, min(1, (horizon-coverage)/max(1, horizon)))
        age = max(0, self.world.turn-need.created_at)
        waiting = 18*age/(age+72)*ratio
        pressure = min(85, FEEDING.reserve_priority+FEEDING.reserve_deficit_weight*ratio+
                       FEEDING.reserve_hunger_weight*min(person.hunger, FEEDING.meal_threshold)+
                       risk+opportunity+gap+waiting)
        need.context.update(ReserveTarget=target, ReserveDeficit=deficit,
                            coverage_hours=coverage, coverage_risk=risk, opportunity_pressure=opportunity,
                            next_known_opportunity_hours=next_opportunity, known_replacement_hours=market_distance+1 if market_distance<1000 else None,
                            affordable_observed_market=affordable, waiting_pressure=waiting,
                            opportunity_gap_pressure=gap, planned_travel_hours=travel if leaving else 0)
        return pressure

    def travel_assessment(self, person, destination):
        travel = distance(person.position, destination)
        if travel >= 1000:
            return {'reason': 'UnknownRoute'}
        horizon = travel+FEEDING.travel_margin_hours
        target = self.reserve_target(person, destination)
        water = max(0, math.ceil((person.thirst+2*horizon-50)/45))
        return {'KnownTravelHours': travel, 'SafetyMarginHours': FEEDING.travel_margin_hours,
                'ReserveTarget': target, 'ReserveDeficit': max(0, target-self.items.count(person.id, 'food')),
                'WaterNeeded': water, 'WaterOwned': self.items.count(person.id, 'water'),
                'EstimatedSurvivalMargin': self.survival_margin(person)}

    def survival_margin(self, person):
        symbol = self.world.maps[person.position.map_id].rows[person.position.y][person.position.x]
        key = (person.health, person.hunger, person.thirst, person.starvation_hours, symbol)
        cached = self.margin_cache.get(person.id)
        if cached and cached[0] == key:
            return cached[1]
        hp, hunger, thirst, deprived = person.health, person.hunger, person.thirst, person.starvation_hours
        result = 0
        if hp > 0:
            for hour in range(1, FEEDING.estimate_horizon+1):
                hunger = min(100, hunger+FEEDING.hunger_per_hour)
                thirst = min(100, thirst+(4 if symbol == "D" else 2))
                if max(hunger, thirst) >= SURVIVAL.starvation:
                    deprived += 1
                    hp -= min(SURVIVAL.maximum_damage, SURVIVAL.starvation_damage+
                              deprived//SURVIVAL.progression_hours)
                else:
                    deprived = 0
                if hp <= 0:
                    result = hour
                    break
            else:
                result = FEEDING.estimate_horizon
        self.margin_cache[person.id] = (key, result)
        return result

    def emergency(self, person):
        return person.hunger >= FEEDING.high_hunger or (
            person.hunger >= FEEDING.meal_threshold and self.survival_margin(person) <= FEEDING.emergency_window)

    def immediate_meal_needed(self, person):
        return person.hunger >= FEEDING.meal_threshold and self.survival_margin(person) <= FEEDING.emergency_window

    def knowledge_status(self, person):
        reasons = []
        owned = self.items.count(person.id, "food")
        if owned:
            reasons.append("FoodAlreadyAvailable")
        market = person.known_places.get("market")
        if market is None:
            return reasons+["UnknownMarket"]
        seen = person.market_observation
        if person.position == market:
            town = self.world.towns[person.town_id]
            stock = self.items.count(town.id, "food")
            price = self.world.towns[person.town_id].economic_report.get("price")
            # O preço corrente é calculado pelo Economy.observe, antes de decidir.
            price = seen.get("price", price)
        elif seen.get("town_id") == person.town_id and self.world.turn-seen.get("price_turn", -1000) <= 24:
            stock, price = seen.get("stock", {}).get("food"), seen.get("price")
        else:
            stock, price = None, None
        if stock == 0:
            reasons.append("NoProduct")
        if price is None:
            reasons.append("UnknownPrice")
        elif person.money < price:
            reasons.append("NoMoney")
        if person.position != market:
            reasons.append("DistantProduct")
        return reasons

    def estimate(self, person, choice):
        action = MEALS.get(choice.action, choice.action)
        margin = self.survival_margin(person)
        travel = distance(person.position, choice.destination) if choice.destination else 0
        interval = self.decision_interval(person)
        consumption = 0 if choice.action in MEALS or action == "eat" else interval
        reason = None
        economic = True
        if action == "eat":
            time = 1
        elif action in ACQUISITIONS:
            time = travel+1+consumption
        elif action in ("work", "train"):
            market = person.known_places.get("market")
            seen = person.market_observation
            fresh = seen.get("town_id") == person.town_id and self.world.turn-seen.get("price_turn", -1000) <= 24
            price = seen.get("price", FEEDING.minimum_market_price) if fresh else FEEDING.minimum_market_price
            wage = 1/3 if action == "train" or person.training_target else 1
            earning = max(1, math.ceil(max(0, price-person.money-person.wage_credit/6)/wage))
            work_to_market = distance(choice.destination or person.position, market) if market else 1000
            time = travel+earning+work_to_market+1+interval
            if market is None or work_to_market >= 1000:
                reason, economic = "UnknownMarket", False
        else:
            return None
        if choice.action not in MEALS and action != 'eat' and person.hunger < FEEDING.meal_threshold:
            # Formar reserva não agenda uma refeição precoce: inclui a espera
            # mínima até o limiar normal, além da obtenção física do alimento.
            meal_due = math.ceil((FEEDING.meal_threshold-person.hunger)/FEEDING.hunger_per_hour)+1
            time = max(time, meal_due)
        if travel >= 1000:
            reason, economic = "UnknownRoute", False
        viable = economic and time <= margin
        if reason is None and not viable:
            reason = "SolutionTooSlow"
        return {"EstimatedTimeUntilFoodConsumed": time, "EstimatedSurvivalMargin": margin,
                "economically_viable": economic, "survival_viable": viable,
                "reason": reason, "known_conditions": self.knowledge_status(person)}

    def add_metric(self, name, value):
        self.world.metrics["Feeding:"+name+":sum"] = self.world.metrics.get("Feeding:"+name+":sum", 0)+value
        self.world.metrics["Feeding:"+name+":count"] = self.world.metrics.get("Feeding:"+name+":count", 0)+1

    def record(self, person, kind, **details):
        row = {"kind": kind, "turn": self.world.turn, "npc_id": person.id,
               "hunger": person.hunger, "hp": person.health,
               "food_owned": self.items.count(person.id, "food"), **details}
        self.world.feeding_diagnostics.append(row)
        del self.world.feeding_diagnostics[:-FEEDING.diagnostics_limit]
        for listener in self.listeners:
            listener(dict(row))

    def search_started(self, person, choice):
        state = person.food_state
        if state.get("search_started") is not None or choice.action == "eat":
            return
        target = self.reserve_target(person, choice.destination)
        deficit = max(0, target-self.items.count(person.id, "food"))
        state.update(search_started=self.world.turn, search_hunger=person.hunger, search_hp=person.health,
                     food_owned_at_search=self.items.count(person.id, "food"), reserve_target=target,
                     reserve_deficit=deficit)
        for name, value in (("HungerAtFoodSearchStart", person.hunger), ("HPAtFoodSearchStart", person.health),
                            ("FoodOwnedAtSearchStart", state['food_owned_at_search']),
                            ("ReserveTarget", target), ("ReserveDeficit", deficit)):
            self.add_metric(name, value)
        self.record(person, "FoodSearchStarted", action=choice.action, ReserveTarget=target,
                    ReserveDeficit=deficit, **(self.estimate(person, choice) or {}))

    def rejected(self, person, need, solutions):
        state = person.food_state
        signature = [(s.action, s.feeding['reason']) for s in solutions]
        if not signature or state.get("last_rejection") == signature:
            return
        state['last_rejection'] = signature
        for s in solutions:
            name = "FeedingRejected:"+s.feeding['reason']
            self.world.metrics[name] = self.world.metrics.get(name, 0)+1
            self.record(person, "FoodSolutionRejected", need=need.kind, action=s.action, **s.feeding)

    def interrupted(self, person, previous, action):
        emergency = self.emergency(person)
        metric = "EmergencyGoalInterrupted" if emergency else "MealGoalInterrupted"
        self.world.metrics[metric] = self.world.metrics.get(metric, 0)+1
        self.record(person, metric, previous_action=previous.action, previous_goal=previous.id,
                    action=action, EstimatedSurvivalMargin=self.survival_margin(person))

    def inventory_changed(self, kind, owner_id, product, quantity):
        person = self.world.characters.get(owner_id)
        if product != "food" or person is None or person.is_player:
            return
        state = person.food_state
        queue = state.setdefault("acquisitions", [])
        if kind == "acquired":
            search = state.get("search_started")
            queue.append({"turn": self.world.turn, "quantity": quantity, "search_started": search})
            # Não acumula registros indefinidamente se receber lotes pequenos repetidos.
            if len(queue)>16:
                queue[1]['quantity'] += queue[0]['quantity']
                queue[1]['turn'] = queue[0]['turn']
                queue[1]['search_started'] = queue[0]['search_started']
                state['acquisition_timing_coalesced'] = True
                del queue[0]
            state['last_acquisition'] = self.world.turn
            for name, value in (("HungerAtAcquisition", person.hunger), ("HPAtAcquisition", person.health)):
                self.add_metric(name, value)
            if search is not None:
                self.add_metric("TimeFromSearchToAcquisition", self.world.turn-search)
            self.record(person, "FoodAcquired", quantity=quantity, search_started=search)
            if self.items.count(person.id, "food") >= self.reserve_target(person):
                state['search_started'] = None
            return
        # Parte do inventário inicial não possui carimbo de aquisição. Consumo FIFO
        # não atribui uma ração antiga ao lote recebido mais recentemente.
        tracked = sum(b['quantity'] for b in queue)
        old_untracked = max(0, self.items.count(person.id, "food")+quantity-tracked)
        remaining = max(0, quantity-old_untracked)
        batches = []
        while remaining and queue:
            batch = queue[0]
            used = min(remaining, batch['quantity'])
            batches.append((dict(batch), used))
            batch['quantity'] -= used
            remaining -= used
            if batch['quantity'] == 0:
                queue.pop(0)
        if kind == "consumed":
            self.add_metric("HungerAtConsumption", person.hunger)
            self.add_metric("HPAtConsumption", person.health)
            self.add_metric("NutritionUsed", min(person.hunger, FEEDING.meal_reduction))
            for batch, used in batches:
                self.add_metric("TimeFromAcquisitionToConsumption", self.world.turn-batch['turn'])
                if batch['search_started'] is not None:
                    self.add_metric("TimeFromSearchToConsumption", self.world.turn-batch['search_started'])
            self.record(person, "FoodConsumed", quantity=quantity, acquired_turn=batches[0][0]['turn'] if batches else None,
                        search_started=batches[0][0]['search_started'] if batches else None)
            state['last_consumption'] = self.world.turn
            state['search_started'] = None

    def death(self, person):
        state = person.food_state
        owned = self.items.count(person.id, "food")
        self.record(person, "DeathBeforeConsumption", LastSuccessfulAction=dict(person.last_successful_action),
                    last_acquisition=state.get('last_acquisition'),
                    food_before_last_decision=state.get('food_before_decision'),
                    EstimatedSurvivalMargin=0)
        if owned:
            key = "DeathBeforeConsumption"
            self.world.metrics[key] = self.world.metrics.get(key, 0)+1
