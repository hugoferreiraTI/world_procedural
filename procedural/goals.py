"""Alternativas avaliadas pela personalidade, seguidas de execução e reavaliação."""

from dataclasses import dataclass, field, replace
from copy import deepcopy

from .models import Goal, Location, Personality
from types import SimpleNamespace
from .navigation import distance
from .rules import UTILITY, FEEDING, RECOVERY
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
    action_audit: dict | None = None
    resource_kind: str | None = None
    amount: int = 1

    @classmethod
    def candidate(cls, candidate):
        action,destination,target=candidate
        return cls(action,0,destination,target,resource_kind=getattr(candidate,'resource_kind',None),
                   amount=getattr(candidate,'amount',1))


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
        self.interactions = None
        self.agency = None
        self.evaluated_choices = {}

    def solutions(self, character, need) -> list[Solution]:
        """QUERY isolada: simula planejamento em cópia, sem RNG/eventos/planos reais.

        Ferramentas externas usam esta API. O ciclo de decisão usa plan_solutions
        (COMMAND), pois alguns fornecedores atualizam planos e diagnósticos.
        """
        from .engine import Engine
        world=deepcopy(self.world);world.rng_state=self.rng.getstate()
        engine=Engine(world)
        person=world.characters[character.id]
        query_need=next((n for n in person.needs.values() if n.id==need.id),deepcopy(need))
        return engine.goals.plan_solutions(person,query_need)

    def plan_solutions(self, character, need) -> list[Solution]:
        """COMMAND: planejamento usado exclusivamente pela decisão executável."""
        places = character.known_places
        choices = []
        if self.interactions:
            target_id=need.context.get('threat') if need.kind=='protection' else need.target_id
            target=self.world.characters.get(target_id)
            if target and self.interactions.terminal_combat.opportunity(character,target):
                choices=[Solution(a,0,d,t) for a,d,t in self.interactions.conflicts.candidates(character,need) if a!='attack']
                return self._evaluate(character,need,choices)
        if self.interactions:
            choices.extend(Solution.candidate(c) for c in self.interactions.tasks.candidates(character,need))
            choices.extend(Solution.candidate(c) for c in self.interactions.society.candidates(character,need))
            choices.extend(Solution(a,0,d,t) for a,d,t in self.interactions.faith.candidates(character,need))
            choices.extend(Solution(a,0,d,t) for a,d,t in self.interactions.access.candidates(character,need))
            choices.extend(Solution(a,0,d,t) for a,d,t in self.interactions.institutions.candidates(character,need))
        if need.kind == 'recovery':
            plan = self.interactions.recovery.candidates(character)
            if isinstance(plan, str):
                return self.plan_solutions(character, replace(need, kind=plan, context={}))
            choices.extend(Solution(action, 0, destination, target) for action,destination,target in plan)
        if need.kind in ("food", "food_reserve"):
            owned = self.items.count(character.id, "food")
            if owned and need.kind == "food" and character.hunger >= FEEDING.meal_threshold:
                choices.append(Solution("eat", 0))
            if owned >= self.feeding.reserve_target(character):
                return self._evaluate(character, need, choices)
            if "market" in places:
                # A intenção de comprar não conhece remotamente o preço nem o estoque.
                town = self.world.towns[places["market"].map_id]
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
                detail=seen.get('training_details',{}).get(character.training_target,{})
                destination=Location(**detail['location']) if detail.get('location') else character.known_places.get('market')
                choices.append(Solution("train",0,destination))
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
                    detail=seen.get('training_details',{}).get(seen['training_offer'],{})
                    destination=Location(**detail['location']) if detail.get('location') else places.get('market')
                    choices.append(Solution("train",0,destination))
            choices = [c for c in choices if c.action != 'work' or self.professions.compatible_workplace(character)]
        if self.interactions:
            existing={(c.action,c.destination,c.target_id) for c in choices}
            for service in (self.interactions.conflicts,self.interactions.migration):
                for action,destination,target in service.candidates(character,need):
                    if (action,destination,target) not in existing:
                        choices.append(Solution(action,0,destination,target))
                        existing.add((action,destination,target))
        if self.agency:
            choices.extend(Solution(a,0,d,t) for a,d,t in self.agency.travel_candidates(character,need))
        if self.interactions:
            search=self.interactions.investigation.candidates(character,need)
            if search is not None:
                choices=[c for c in choices if c.action not in ('pursue','watch_case','investigate','check_relative','ask_personal_help')]
                choices.extend(Solution(a,0,d,t) for a,d,t in search)
            if (need.kind in ('rest','work','money','recovery','healing') and character.position.map_id!=character.home.map_id
                    and any(c.status=='waiting_for_information' for c in character.commitments.values())):
                choices.append(Solution('return_from_search',0))
        if need.context.get('aspiration_domain')=='competence':
            choices=[c for c in choices if c.action=='train']
        # Enumerar todos os fornecedores antes de converter aquisição em refeição.
        if need.kind == 'food' and self.feeding.immediate_meal_needed(character):
            for action, original in MEALS.items():
                for choice in list(choices):
                    if choice.action == original:
                        if original == 'ask_help' and self.world.characters[choice.target_id].is_player:
                            continue
                        choices.append(Solution(action, 0, choice.destination, choice.target_id))
        if character.combat.detention_until>self.world.turn or character.combat.surrendered_until>self.world.turn:
            choices=[c for c in choices if c.action in ('eat','drink','drink_well','sleep') and
                     (c.destination is None or c.destination==character.position)]
            if need.kind=='rest':choices=[Solution('sleep',0)]
        return self._evaluate(character, need, choices)

    def _evaluate(self, character, need, choices):
        available, rejected = [], []
        observer=self.recorder.observer
        observer.candidates(need,choices)
        for choice in choices:
            action = MEALS.get(choice.action, choice.action)
            reason=self.eligibility(character,choice)
            if reason:
                observer.blocked(need,choice,reason)
                continue
            if action=='work':
                # Estoque verdadeiro só pode bloquear quem está na instalação.
                # Uma oferta antiga/remota não vira radar de emprego.
                if character.position==character.workplace:
                    work_reason=self.professions.work_gate(character)
                    if work_reason:
                        observer.blocked(need,choice,work_reason)
                        continue
            if self.interactions:
                from .action_pressure import STRONG,FORWARD
                if action in STRONG or action in FORWARD or action=='attack':
                    if action=='attack' and self.interactions.lethal_decisions.active(character,choice.target_id):
                        choice.action_audit=self.interactions.lethal_decisions.action_audit(character,choice.target_id,need)
                    else:choice.action_audit=self.interactions.action_pressure.assess(character,need,action,choice.target_id)
                    if not choice.action_audit['eligible']:
                        observer.blocked(need,choice,'NO_CAPABILITY',choice.action_audit.get('major_barriers'))
                        continue
            if (action in ("work_for_food", "temporary_service") and choice.action not in MEALS and
                    self.items.count(character.id, 'food') > self.feeding.reserve_target(character)):
                observer.blocked(need,choice,'EXCESS_RESERVE')
                continue
            if (need.kind == 'family' and action in ACQUISITIONS and
                    self.items.count(character.id, 'food') >= self.feeding.reserve_target(character)+1):
                observer.blocked(need,choice,'EXCESS_RESERVE')
                continue  # Reserva própria mais uma provisão para o familiar.
            travel = distance(character.position, choice.destination) if choice.destination else 0
            terms = self.social.considerations(character, choice.target_id) if action in (
                "ask_help", "ask_personal_help", "seek_company", "denounce", "give_supplies") else {}
            if self.interactions:
                from .conflicts import ACTIONS
                if action in ACTIONS:
                    terms.update(self.interactions.conflicts.terms(character,choice.target_id))
                    terms['culpability']=float(bool(need.context.get('stolen_fact')))
                if action=='migrate':
                    terms.update(financial_pressure=float(need.context.get('reason')=='poverty'),
                                 fear=float(need.context.get('reason') in ('wanted','threat')))
            if action=='policy_work':
                terms['financial_pressure']=min(1,max(0,20-character.money)/20)
            if action == "train":
                terms.update({"local_demand":1.,"financial_pressure":min(1,max(0,20-character.money)/20),
                    "training_cost":max(0,36-character.personality.diligence//5)/36,
                    "current_job_value":0. if self.professions.saturated(character,character.market_observation) else .5,
                    "risk":max(character.hunger,character.thirst)/100})
            if action in ('work', 'train', 'work_for_food', 'temporary_service','policy_work'):
                terms['physical_depletion'] = max(0, (RECOVERY.target_hp-character.health)/RECOVERY.target_hp)
            if action in ('attack', 'threaten', 'pursue'):
                terms['critical_depletion'] = max(0, (RECOVERY.critical_hp-character.health)/RECOVERY.critical_hp)
                if action == 'attack' and terms.get('defensive', 0):
                    terms['critical_depletion'] *= .25
            if need.kind == 'recovery' and action in ('sleep', 'seek_treatment'):
                terms['recovery_pressure'] = max(0, (RECOVERY.target_hp-character.health)/RECOVERY.target_hp)
            if self.interactions and action in ('finish','spare','capture','first_aid','withdraw'):
                target=self.world.characters.get(choice.target_id)
                if target and self.interactions.terminal_combat.opportunity(character,target):
                    terminal=self.interactions.lethal_decisions.terminal(character,target)
                    score=terminal['scores'].get('help' if action=='first_aid' else action,-1000)
                    if score<=-1000:
                        observer.blocked(need,choice,'TERMINAL_UNAVAILABLE')
                        continue
                    # Uma competição terminal. Necessidades vitais continuam
                    # concorrendo antes, na escolha de Need, como anteriormente.
                    choice.score=score;choice.considerations={'terminal_context':score/200,
                        'terminal_winner':terminal['choice']==('help' if action=='first_aid' else action)}
                    available.append(choice)
                    observer.scored(need,choice)
                    continue
            choice.score, choice.considerations = evaluate(action, character, terms, travel)
            if choice.action_audit and action!='attack':
                bonus=choice.action_audit['action_pressure']*.25
                choice.score+=bonus;choice.considerations['action_pressure']=bonus/200
            if need.kind in ("food", "food_reserve"):
                choice.feeding = self.feeding.estimate(character, choice)
                if choice.feeding and not choice.feeding['survival_viable']:
                    rejected.append(choice)
                    observer.blocked(need,choice,'SURVIVAL_NOT_VIABLE')
                    continue
            role=need.context.get('institutional_role')
            if (role=='inquire' and action=='ask_about_person' or role=='watch' and action=='search_area'):
                choice.score+=10;choice.considerations['institutional_assignment']=.05
            if self.agency:
                choice.score = self.agency.adjust(character,need,action,choice.score,choice.considerations)
            if self.interactions:
                mythic=self.interactions.faith.modifier(character,action)
                choice.score+=mythic
                if mythic:choice.considerations['mythic_influence']=mythic/200
            available.append(choice)
            observer.scored(need,choice)
        self.rejected_food[character.id] = rejected
        if need.kind == 'food' and self.feeding.immediate_meal_needed(character):
            immediate = {(MEALS[c.action], c.destination, c.target_id) for c in available if c.action in MEALS}
            available = [c for c in available if (c.action, c.destination, c.target_id) not in immediate]
        available=sorted(available, key=lambda choice: (-choice.score, choice.action, choice.target_id or 0))
        self.evaluated_choices[(character.id,need.id)]=available
        return available

    def choose(self, alternatives):
        if alternatives and all('terminal_winner' in s.considerations for s in alternatives):
            return next((s for s in alternatives if s.considerations['terminal_winner']),alternatives[0])
        near = [s for s in alternatives if alternatives[0].score - s.score <= UTILITY.close_choices]
        if len(near) == 1:
            return near[0]
        return max(near, key=lambda s: s.score + self.rng.uniform(-UTILITY.variation, UTILITY.variation))

    def decide(self, character, elapsed: int = 1) -> None:
        with self.recorder.observer.decision(character,self.feeding.decision_interval(character)):
            self._decide(character,elapsed)

    def _decide(self, character, elapsed: int = 1) -> None:
        self.evaluated_choices.clear()
        self.world.metrics['NPCDecision']=self.world.metrics.get('NPCDecision',0)+1
        self.economy.observe(character)
        character.food_state['food_before_decision'] = self.items.count(character.id, "food")
        character.food_state['last_decision_turn'] = self.world.turn
        active = self.needs.refresh(character)
        # Uma avaliação por decisão real. Consultas/debug não mudam o save.
        for need in active:
            if need.kind not in ('revenge','protection','response','pursuit'):continue
            target_id=need.context.get('threat') if need.kind=='protection' else need.target_id
            if target_id not in self.spatial.at(character.position):continue
            if not any(a=='attack' for a,d,t in self.interactions.conflicts.candidates(character,need)):continue
            target=self.world.characters[target_id]
            assessment=self.interactions.lethality.evaluate(character,target,need,audit=True)
            marker=(target.id,assessment['available'])
            old=character.agency_state.get('lethal_option')
            if assessment['available'] and (not old or tuple(old['marker'])!=marker or self.world.turn-old['turn']>=48):
                self.interactions.agency.event(character,'LethalOptionConsidered',self.agency.current(character,need),
                    lethal_audit=assessment,need_kind=need.kind)
                character.agency_state['lethal_option']={'marker':marker,'turn':self.world.turn}
        if not active:
            self.interactions.audit.selection(character,active,None)
            # Rotina sem pressão: retornar para casa. Não abandona o mundo parado.
            if character.combat.detention_until<=self.world.turn and character.combat.surrendered_until<=self.world.turn:
                if character.position.map_id!=character.home.map_id and any(c.status=='waiting_for_information' for c in character.commitments.values()):
                    self.interactions.investigation.return_home(character)
                else:self.navigation.approach(character, character.home, elapsed)
            character.goal = None
            return
        selected, choice = None, None
        for need in active:
            alternatives = self.plan_solutions(character, need)
            if need.kind in ("food", "food_reserve"):
                self.feeding.rejected(character, need, self.rejected_food.get(character.id, []))
            if alternatives:
                selected, choice = need, self.choose(alternatives)
                break
            if self.agency:self.agency.blocked(character,need)
            need.status = "blocked"
            if not need.context.get("blocked_recorded"):
                self.needs.count("Blocked", need.kind, character)
                need.context["blocked_recorded"] = True
        if selected is None:
            self.interactions.audit.selection(character,active,None)
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
                                   s.destination == paused.destination for s in self.plan_solutions(character, paused_need)):
                current = paused
                current.status = "active"
                character.goal = paused
            character.suspended_goal = None
        meal_interrupt = choice.action == "eat" or (
            choice.action in MEALS and self.feeding.immediate_meal_needed(character))
        recovery_interrupt = (selected.kind == 'recovery' and character.health < RECOVERY.critical_hp
                              and choice.action in ('sleep', 'seek_treatment', 'drink', 'drink_well', 'drink_stream'))
        # Mantém uma viagem em andamento enquanto outra necessidade não é
        # claramente mais urgente. Fome e sede próximas não devem fazer o
        # personagem alternar destinos a cada hora sem concluir nenhuma ação.
        if current and current.status == "active" and not meal_interrupt and not recovery_interrupt and not selected.context.get('emergency'):
            current_need = next((need for need in active if need.id == current.need_id), None)
            if current_need and selected.priority < current_need.priority + 12:
                continuing = next((solution for solution in self.plan_solutions(character, current_need)
                                   if solution.action == current.action and
                                   solution.target_id == current.target_id and
                                   solution.destination == current.destination), None)
                if continuing:
                    selected, choice = current_need, continuing
        for need in active:
            if need.kind not in PERSONAL_KINDS or need.status=='waiting_for_information':
                continue
            if need is selected:
                need.context["selections"] = need.context.get("selections",0)+1
                self.needs.explain(character,need,"Selected")
            elif not self.plan_solutions(character,need):
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
        self.interactions.audit.selection(character,active,selected)
        if self.agency:self.agency.selected(character,active,selected,choice.action)
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
                               for s in self.evaluated_choices.get((character.id,selected.id),())],
                "rejected_food_solutions": [{"action": s.action, "feeding": s.feeding}
                                             for s in self.rejected_food.get(character.id, [])]}
        if not (current and current.status == "active" and current.need_id == selected.id and
                current.action == choice.action and current.target_id == choice.target_id and
                current.destination == choice.destination and current.resource_kind == choice.resource_kind):
            current = Goal(self.world.allocate_id(), selected.id, choice.action, choice.score,
                           self.world.turn, choice.target_id, choice.destination,
                           resource_kind=choice.resource_kind,amount=choice.amount)
            character.goal = current
        self.recorder.observer.selected(selected,choice,current)
        if current.destination and character.position != current.destination:
            # Tempo de viagem é consumido antes da ação; não recebe horas de
            # produção por um intervalo que passou caminhando.
            steps = min(elapsed, distance(character.position, current.destination))
            before = self.agency.snapshot(character,selected) if self.agency else None
            arrived = self.navigation.approach(character, current.destination, steps)
            if self.agency:self.agency.outcome(character,selected,current.action,before,True,steps)
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
                               context={"profession": character.profession, "need_source": selected.source,
                                        "recognized_by":[i for i in self.spatial.at(character.position) if i!=character.id]})
            if selected.context.get('aspiration_domain')=='recognition':
                selected.context['deeds']=selected.context.get('deeds',0)+1
                if selected.context['deeds']>=selected.context.get('deeds_target',3):self.needs.finish(character,selected)
            else:self.needs.finish(character, selected)
        # A necessidade depende do estado, não do sucesso nominal de uma ação.
        if (current.action == "eat" or current.action in MEALS) and character.hunger < FEEDING.meal_threshold:
            self.needs.satisfy(character, "food")
        elif current.action in ("drink", "drink_well", "drink_stream") and character.thirst < 25:
            self.needs.satisfy(character, "water")
        elif current.action == "sleep" and character.fatigue < 25:
            self.needs.satisfy(character, "rest")

    def execute(self, character, goal, hours: int) -> tuple[bool, str]:
        observer=self.recorder.observer
        if observer.current is None:
            with observer.decision(character,0) as trace:
                need=next((n for n in character.needs.values() if n.id==goal.need_id),None)
                if need:observer.selected(need,goal,goal)
                result=self.execute(character,goal,hours)
            return result
        with observer.action(character,goal):
            result=self._execute_attempt(character,goal,hours)
            observer.outcome(result)
            self.interactions.audit.outcome(character,goal,result[0])
            return result

    def _execute_attempt(self, character, goal, hours: int) -> tuple[bool, str]:
        if goal.action in ("work_for_food", "temporary_service"):
            deficit = max(1, self.feeding.reserve_target(character)-self.items.count(character.id, 'food'))
            hours = min(hours, deficit)
        elif goal.action in MEALS:
            hours = 1  # Uma operação explícita de refeição, sem lote retroativo.
        previous_rng = self.rng.getstate()
        need = next((n for n in character.needs.values() if n.id==goal.need_id),None)
        from .action_pressure import STRONG
        if self.interactions and goal.action in STRONG:
            check=self.interactions.action_pressure.assess(character,need,goal.action,goal.target_id)
            if not check['eligible']:return False,'Faltam causa grave, capacidade ou pressão para esta ação.'
        previous_position=character.position
        previous_social_progress=character.social_state.get('meaningful_social_actions',0)
        before = self.agency.snapshot(character,need) if self.agency and need else None
        terminal=None
        if self.interactions and goal.action in ('capture','first_aid','withdraw'):
            target=self.world.characters.get(goal.target_id)
            if target and self.interactions.terminal_combat.opportunity(character,target):
                terminal=self.interactions.lethal_decisions.terminal(character,target)
        result = self._execute(character,goal,hours)
        if terminal is not None:
            self.recorder.emit('TerminalDecision',f'{character.name} escolheu {goal.action} diante da incapacidade.',
                character.id,goal.target_id,previous_position,historical=True,
                context={'decision':'help' if goal.action=='first_aid' else goal.action,
                    'terminal_context':terminal,'executed':result[0],'outcome':result[1]})
        if self.agency and need:self.agency.outcome(character,need,goal.action,before,result[0],hours)
        if self.interactions:self.interactions.action_pressure.outcome(character,need,goal.action,result[0],previous_position,previous_social_progress)
        resolved_rng = self.rng.getstate()
        if result[0] or resolved_rng!=previous_rng:
            self.world.rng_state = resolved_rng
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
        if not character.alive:return False,'Um morto não pode agir.'
        held=character.combat.detention_until>self.world.turn or character.combat.surrendered_until>self.world.turn
        if held and action not in ('eat','drink','drink_well','sleep'):
            return False,'A detenção ou rendição restringe esta ação.'
        need = next((n for n in character.needs.values() if n.id == goal.need_id), None)
        if self.interactions:
            if action=='perform_institutional_task':return self.interactions.tasks.execute(character,goal,need)
            from .geography import TRAVEL_ACTIONS
            from .institutions import ACTIONS as INSTITUTION_ACTIONS
            if action in INSTITUTION_ACTIONS:return self.interactions.institutions.execute(character,goal,need)
            from .access import ACTIONS as ACCESS_ACTIONS
            if action in ACCESS_ACTIONS:return self.interactions.access.execute(character,goal,need)
            if action=='ask_route':return self.interactions.geography.ask(character,goal.target_id)
            if action=='route_travel':
                if character.migration or need and need.kind=='migration':
                    return self.interactions.migration.execute(character, character.migration.destination_id if character.migration else need.target_id, need)
                return self.interactions.geography.travel(character,goal.target_id,need.kind if need else 'individual')
            from .society import SOCIAL_ACTIONS
            from .collective_action import ACTIONS as COLLECTIVE_ACTIONS
            from .faith import FAITH_ACTIONS
            if action in SOCIAL_ACTIONS|COLLECTIVE_ACTIONS:return self.interactions.society.execute(character,goal,need)
            if action in FAITH_ACTIONS:return self.interactions.faith.execute(character,goal,need)
            from .conflicts import ACTIONS
            if action in ACTIONS:return self.interactions.conflicts.execute(character,goal,need)
            from .investigation import SEARCH_ACTIONS
            if action in SEARCH_ACTIONS:return self.interactions.investigation.execute(character,goal,need)
            if action=='return_from_search':return self.interactions.investigation.return_home(character,need)
            if action=='follow_lead':return self.agency.follow_lead(character,goal.target_id,need)
            if action=='migrate':return self.interactions.migration.execute(character,goal.target_id,need)
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
            if character.position.map_id not in self.world.towns:
                return False,'Não há mercado nesta área.'
            if need and need.kind == 'food_reserve':
                return self.economy.buy_reserve(character, self.feeding.reserve_target(character),
                                                bulk=need.priority >= 50)
            return self.economy.buy(character.id, character.position.map_id, "food")
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
            town = self.world.towns.get(character.position.map_id)
            if town:
                if town.wild_food <= 0:
                    return False, "Os alimentos silvestres locais acabaram por hoje."
                town.wild_food -= 1
            point = self.world.points.get(character.position.map_id)
            if point:
                if not self.items.count(point.id,'food'):return False,'Recursos alimentares do local esgotados.'
                self.items.transfer(point.id,character.id,self.items.first(point.id,'food'))
            else:self.items.create(character.id, "food", creator_id=character.id,
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
            town = self.world.towns.get(character.position.map_id)
            if not town:return False,'Nenhum mercado local acessível.'
            item_id = self.items.first(town.id, "food")
            if character.position != town.market or item_id is None:
                return False, "Nenhum alimento acessível."
            moved = self.items.transfer(town.id, character.id, item_id)
            self.recorder.emit("ItemStolen", f"{character.name} roubou comida no mercado de {town.name}.",
                               character.id, town.id, character.position,
                               context={'item_id':moved.id,'item_kind':'food'})
            return True, "Alimento roubado."
        if action == "secure":
            need = character.needs["security"]
            event_id = int(need.source.split(":")[1])
            suspect = self.world.characters.get(goal.target_id)
            record=self.interactions.justice.record_for(character,goal.target_id) if self.interactions else None
            if self.interactions and not record:return False,'Falta evidência institucional conhecida e válida.'
            if record and record.known_severity.get(character.id,1)>1:
                return False,'A gravidade conhecida exige resposta de perseguição/captura.'
            character.failures[f"crime:{event_id}"] = self.world.turn + 24
            self.needs.satisfy(character, "security")
            if suspect and suspect.alive and suspect.position == character.position:
                if record:
                    self.interactions.justice.resolve_known(character,suspect.id,'resolved')
                fine = min(5, suspect.money)
                suspect.money -= fine
                self.world.towns[character.town_id].money += fine
                self.recorder.emit("GuardResponded", f"{character.name} interveio no roubo e cobrou {fine} moedas de {suspect.name}.",
                                   character.id, suspect.id, character.position,
                                   context={'record_id':record.id if record else None,'fine':fine,'source_fact':event_id})
                return True, "Suspeito encontrado; intervenção registrada."
            return True, "O guarda investigou o último local conhecido; o suspeito não estava lá."
        return False, "Ação desconhecida."

    def eligibility(self, person, choice):
        """QUERY: guardas fundamentais compartilhadas por seleção e preparação.

        Estoque remoto só é consultado na observação própria recente; a presença
        permite verificar a fonte material. Nenhuma informação remota é criada.
        """
        from .navigation import passable
        action=MEALS.get(choice.action,choice.action)
        if max(person.failures.get(choice.action,0),person.failures.get(action,0))>self.world.turn:
            return 'ACTION_COOLDOWN'
        if action=='ask_help' and person.failures.get(f'request:{choice.target_id}',0)>self.world.turn:
            return 'ACTION_COOLDOWN'
        destination=choice.destination
        if destination and (destination.map_id!=person.position.map_id or not passable(self.world,destination)):
            return 'NO_KNOWN_ROUTE'
        if action=='fill_water':
            if not destination or destination not in person.known_places.values():return 'NO_KNOWN_TARGET'
            town=self.world.towns.get(destination.map_id)
            _,structures=self.navigation.describe(destination)
            if not town or 'Poço' not in structures:return 'NO_CAPABILITY'
            seen=person.market_observation
            if person.position==destination:
                if not self.items.count(town.id,'water'):return 'NO_STOCK'
            elif (seen.get('town_id')==town.id and self.world.turn-seen.get('turn',-1000)<=24
                  and seen.get('stock',{}).get('water')==0):return 'NO_STOCK'
        if (person.combat.detention_until>self.world.turn or person.combat.surrendered_until>self.world.turn):
            if action not in ('eat','drink','drink_well','sleep') or destination and destination!=person.position:
                return 'NO_CAPABILITY'
        return None

    def preventive_choice(self, person, choice):
        preparation=self._preventive_choice(person,choice)
        return preparation if preparation and not self.eligibility(person,preparation) else None

    def _preventive_choice(self, person, choice):
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
        with self.recorder.observer.decision(town,0):
            return self._collective(town,need,report)

    def _collective(self,town,need,report):
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
        self.recorder.observer.candidates(need,choices)
        for candidate in choices:self.recorder.observer.scored(need,candidate)
        choice=self.choose(choices)
        town.goal=Goal(self.world.allocate_id(),need.id,choice.action,choice.score,self.world.turn)
        need.status='selected'
        self.needs.count('Selected',need.kind,town)
        self.recorder.observer.selected(need,choice,town.goal)
        with self.recorder.observer.action(town,town.goal):
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
            self.recorder.observer.outcome((success,'EXECUTED' if success else 'BLOCKED_MATERIAL'))
