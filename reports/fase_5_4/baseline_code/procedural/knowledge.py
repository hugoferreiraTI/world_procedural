"""Percepção local, memórias e propagação de informação por contato."""

from dataclasses import replace
from contextlib import contextmanager

from .models import Character, Event, Fact, FactImpact, Memory, Reputation, WorldState
from .rules import SOURCE_RELIABILITY

KNOWLEDGE_LIMIT = 64
MEMORY_LIMIT = 32


class KnowledgeSystem:
    def __init__(self, world: WorldState, bus, spatial, graph, rng, social):
        self.world, self.spatial, self.graph, self.rng = world, spatial, graph, rng
        self.social = social
        self.listeners = []
        self.agency = None
        self.processing = {}
        bus.subscribe("*", self.observe)

    def learn(self, character: Character, fact: Fact, firsthand: bool) -> bool:
        confidence = min(fact.confidence / 100, SOURCE_RELIABILITY["direct"] if firsthand else
                         SOURCE_RELIABILITY.get(fact.source_kind, .3))
        old = character.knowledge.get(fact.event_id)
        previous = character.applied_facts.get(fact.event_id)
        if old and confidence <= old.confidence / 100:
            return False
        # Armazena confiança efetiva; retransmissão nunca restaura certeza perdida.
        learned_fact = replace(fact, confidence=round(confidence * 100),
                               source_kind="direct" if firsthand else fact.source_kind)
        with self.protect(character, (fact.event_id,)):
            return self._accept(character, fact, firsthand, confidence, previous, learned_fact)

    @contextmanager
    def protect(self, character, facts):
        """Mantém causas próprias enquanto uma reação síncrona está em curso."""
        refs = set(facts)
        if not refs:
            yield
            return
        processing = self.processing.setdefault(character.id, {})
        for event_id in refs:
            processing[event_id] = processing.get(event_id, 0) + 1
        try:
            yield
        finally:
            for event_id in refs:
                processing[event_id] -= 1
                if not processing[event_id]:
                    del processing[event_id]
            if not processing:
                del self.processing[character.id]

    def _accept(self, character, fact, firsthand, confidence, previous, learned_fact):
        character.knowledge[fact.event_id] = learned_fact
        while len(character.knowledge) > KNOWLEDGE_LIMIT:
            pinned = self.agency.pinned(character) if self.agency else set()
            pinned.update(self.processing.get(character.id, {}))
            removable = next(i for i in character.knowledge if i not in pinned)
            del character.knowledge[removable]
        character.memories.append(Memory(fact.event_id, self.world.turn,
                                         fact.description, firsthand))
        del character.memories[:-MEMORY_LIMIT]
        if fact.actor_id is not None and fact.actor_id != character.id:
            reputation = character.reputations.setdefault(fact.actor_id, Reputation())
            tags, trust = self.social.interpret(character, fact)
            if (tags or trust) and (not previous or confidence > previous.confidence):
                weighted = {tag: round(amount * confidence) for tag, amount in tags.items()}
                weighted_trust = round(trust * confidence)
                for tag, amount in weighted.items():
                    delta = amount - (previous.tags.get(tag, 0) if previous else 0)
                    reputation.tags[tag] = max(0, min(100, reputation.tags.get(tag, 0) + delta))
                    reputation.popularity = min(100, reputation.popularity + max(0, delta) // 2)
                    if tag in ("prestativo", "leal", "responsável"):
                        reputation.admiration = max(0, min(100, reputation.admiration + delta))
                    else:
                        reputation.fear = max(0, min(100, reputation.fear + delta // 2))
                if weighted_trust or previous and previous.trust:
                    key = self.graph.key(character.id, fact.actor_id, "confiança")
                    if key not in self.world.relationships:
                        self.graph.set(character.id, fact.actor_id, "confiança", 10)
                    self.graph.adjust(character.id, fact.actor_id, "confiança",
                                      weighted_trust - (previous.trust if previous else 0))
                character.applied_facts[fact.event_id] = FactImpact(
                    fact.actor_id, confidence, weighted, weighted_trust,
                    previous.emotion_confidence if previous else 0, previous.renown_confidence if previous else 0)
            if tags and fact.event_id not in reputation.sources:
                reputation.sources.append(fact.event_id)
                del reputation.sources[:-32]
        for listener in self.listeners:
            # Uma reação pode aprender outros fatos e expulsar esta memória.
            # Todos os observadores recebem o fato aceito nesta operação.
            listener(character, learned_fact)
        return True

    def observe(self, event: Event) -> None:
        fact = Fact(event.id, event.kind, event.actor_id, event.target_id, event.location,
                    event.turn, event.description,
                    required_trust=20 if event.kind == "HelpRequested" else 0,
                    source_kind="direct", context=event.context)
        if event.kind=='SearchClueShared':
            fact=replace(fact,confidence=event.context['confidence'],source_id=event.actor_id,
                         source_kind=event.context['clue_source_kind'])
        if event.kind in ('SpiritualReport','ItemLegendReported'):
            fact=replace(fact,confidence=event.context.get('confidence',30),source_id=event.actor_id,source_kind='rumor')
        for entity_id in event.witnesses:
            character = self.world.characters.get(entity_id)
            if character and character.alive:
                self.learn(character, fact, event.kind not in ('SearchClueShared','SpiritualReport','ItemLegendReported'))

    def gossip(self) -> None:
        # Snapshot impede que a mesma notícia atravesse vários contatos em um turno.
        snapshot = {entity_id: tuple(character.knowledge.values())
                    for entity_id, character in self.world.characters.items()
                    if character.alive and not character.is_player and character.knowledge}
        transfers = []
        for entity_id, facts in snapshot.items():
            source = self.world.characters[entity_id]
            p = source.position
            listeners = []
            for dx, dy in ((0, 0), (0, 1), (0, -1), (1, 0), (-1, 0)):
                listeners.extend(self.spatial.at(type(p)(p.map_id, p.x + dx, p.y + dy)))
            listeners = sorted(set(listeners) - {entity_id})
            if not listeners:
                continue
            target = self.world.characters[self.rng.choice(listeners)]
            trust = self.graph.value(source.id, target.id, "confiança", 10)
            shareable = [fact for fact in facts if fact.required_trust <= trust and
                         (fact.event_id not in target.knowledge or
                          self.transmitted(fact, source, target).confidence >
                          target.knowledge[fact.event_id].confidence)]
            if shareable:
                fact = self.rng.choice(shareable)
                transfers.append((target, self.transmitted(fact, source, target)))
        for target, fact in transfers:
            if self.learn(target, fact, False):
                self.world.metrics["RumorShared"] = self.world.metrics.get("RumorShared", 0) + 1

    def transmitted(self, fact, source, target):
        trust = self.graph.value(target.id, source.id, "confiança", 10)
        kind = ("trusted" if trust >= 70 else "known" if trust >= 30 else
                "untrusted" if trust < 5 else "rumor")
        return replace(fact, source_id=source.id, source_kind=kind,
                       confidence=min(fact.confidence, round(SOURCE_RELIABILITY[kind] * 100)))

    def information_utility(self, receiver, fact, need=None):
        """Utilidade da resposta recebida, sem aprender nem consultar o mundo remoto."""
        if fact is None:
            return "no_information"
        if need and need.kind in ("family", "revenge", "protection"):
            query = need.target_id if need.kind == "family" else need.context.get("victim")
            if query is None or fact.target_id != query or fact.kind not in (
                    "PersonLocated", "CharacterDied", "CharacterKilled", "RemainsLocated"):
                return "irrelevant"
            if fact.kind == "PersonLocated" and need.kind == 'family':
                observation = receiver.observations.get(query)
                last_seen = max(need.context.get("last_seen", -1), observation.turn if observation else -1)
                old = receiver.knowledge.get(fact.event_id)
                improvement = bool(old and fact.confidence > old.confidence)
                known_location = need.context.get('known_location')
                changed_location = bool(fact.location and observation and fact.location != observation.position
                                        and fact.turn > last_seen)
                searched_same = bool(known_location and fact.location and
                                     known_location == vars(fact.location) and
                                     need.context.get('searched_at', -1) >= fact.turn)
                if (fact.location is None or searched_same or fact.turn < last_seen or
                        fact.turn == last_seen and not improvement or
                        fact.turn < need.created_at and not changed_location and not improvement):
                    return "stale_for_need"
        old = receiver.knowledge.get(fact.event_id)
        if old and old.confidence >= fact.confidence:
            return "already_known"
        return "better_confidence" if old else "new_useful"

    def dialogue(self, character: Character, listener: Character) -> str:
        trust = self.graph.value(character.id, listener.id, "confiança", 10)
        profession = character.profession or "viajante"
        messages = [f"Sou {character.name}, {profession}."]
        if character.training_target:
            messages.append(f"Estou aprendendo a trabalhar como {character.training_target}.")
        if character.hunger >= 55:
            messages.append("Estou com fome e preciso encontrar comida.")
        if character.goal:
            action = {"work": "trabalhar", "train": "aprender uma nova profissão",
                      "temporary_service": "distribuir refeições", "work_for_food": "preparar alimento por pagamento",
                      "fill_water": "levar água para o caminho", "buy_food": "comprar comida", "forage": "buscar alimentos",
                      "sleep": "descansar", "ask_help": "procurar ajuda", "secure": "investigar um roubo",
                      "check_relative": "localizar um familiar", "give_supplies": "ajudar alguém",
                      "seek_company": "buscar companhia", "remember_relative": "lidar com uma perda",
                      "denounce": "procurar um guarda", "investigate": "buscar informação sobre um responsável",
                      "avoid_threat": "evitar uma ameaça", "stay_near": "acompanhar um familiar",
                      "ask_personal_help": "pedir ajuda para um problema pessoal", "sell_surplus": "vender excedentes"}.get(
                          character.goal.action)
            if action:
                messages.append(f"Agora estou tentando {action}.")
        personal = sorted((n for n in character.needs.values() if n.kind in
                           ("family", "grief", "revenge", "protection", "status", "advancement") and
                           n.status not in ("satisfied", "expired", "failed", "inactive")), key=lambda n: -n.priority)
        if personal and trust >= 20:
            messages.append(personal[0].reason + ".")
        reputation = character.reputations.get(listener.id)
        if reputation and reputation.tags.get("ladrão", 0) >= 30:
            messages.append("Ouvi relatos dos seus roubos. Tenho receio de você.")
        facts = [fact for fact in character.knowledge.values()
                 if fact.required_trust <= trust and fact.kind in
                 ("KingdomFounded", "ItemStolen", "CharacterKilled", "FoodShortage", "HelpGiven")]
        if facts:
            fact = facts[-1]
            messages.append(("Eu vi: " if fact.confidence == 100 else "Ouvi dizer: ") + fact.description)
            self.learn(listener, self.transmitted(fact, character, listener), False)
        elif trust < 20:
            messages.append("Ainda nos conhecemos pouco.")
        return " ".join(messages)
