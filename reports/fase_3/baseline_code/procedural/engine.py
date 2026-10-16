"""Coordenação do motor. Nenhum input, print ou acesso a arquivos de save."""

from dataclasses import dataclass
import random
import shlex

from .economy import Economy
from .events import EventBus, EventRecorder, SpatialIndex
from .goals import GoalSystem
from .items import ItemService
from .knowledge import KnowledgeSystem
from .navigation import DIRECTIONS, Navigation, distance
from .needs import NeedSystem
from .politics import Politics
from .professions import ProfessionSystem
from .quests import QuestSystem
from .relationships import RelationshipGraph
from .social import SocialSystem
from .models import Goal
from .personal import PersonalNeeds
from .personal_actions import PersonalActions

PRODUCTS = {"comida": "food", "água": "water", "agua": "water", "trigo": "grain",
            "ferro": "iron", "madeira": "wood", "arma": "weapon", "ferramentas": "tool"}


@dataclass
class CommandResult:
    success: bool
    message: str
    data: object = None


class Engine:
    def __init__(self, world):
        self.world = world
        self.rng = random.Random(0)
        if world.rng_state:
            self.rng.setstate(world.rng_state)
        self.bus = EventBus()
        self.spatial = SpatialIndex(world)
        self.recorder = EventRecorder(world, self.bus, self.spatial)
        self.graph = RelationshipGraph(world)
        self.items = ItemService(world, self.rng)
        self.navigation = Navigation(world, self.spatial)
        self.social = SocialSystem(world, self.graph, self.items)
        self.knowledge = KnowledgeSystem(world, self.bus, self.spatial, self.graph, self.rng, self.social)
        self.needs = NeedSystem(world, self.graph, self.recorder)
        self.economy = Economy(world, self.items, self.recorder, self.needs)
        self.professions = ProfessionSystem(world, self.items, self.economy, self.recorder, self.rng)
        self.quests = QuestSystem(world, self.graph, self.recorder, self.needs, self.items,
                                  self.social, self.economy)
        self.goals = GoalSystem(world, self.needs, self.items, self.economy, self.professions,
                                self.navigation, self.graph, self.spatial, self.recorder,
                                self.social, self.rng, self.quests)
        self.politics = Politics(world, self.bus, self.recorder)
        self.needs.personal = PersonalNeeds(world, self.needs, self.graph, self.spatial,
                                            self.items, self.recorder)
        self.knowledge.listeners.append(self.needs.personal.on_fact)
        self.personal_actions = PersonalActions(self)
        self.goals.personal_actions = self.personal_actions

    @property
    def player(self):
        return self.world.characters.get(self.world.player_id)

    def step(self) -> None:
        # Ações de todas as entidades pertencem à hora que está transcorrendo.
        # Comandos do jogador e decisões dos NPCs precedem o fechamento dessa
        # hora, quando fisiologia e morte são aplicadas a todos pela mesma regra.
        closing_turn = self.world.turn + 1
        player = self.player
        for entity_id in sorted(self.world.characters):
            character = self.world.characters[entity_id]
            if not character.alive:
                continue
            if character.is_player:
                continue
            interval = (1 if character.category == "lendário" or
                        player and player.alive and distance(character.position, player.position) <= 3
                        else 3 if character.category == "importante" else 6)
            if character.hunger >= 85 or character.thirst >= 85:
                interval = 1
            if closing_turn % interval == character.id % interval:
                elapsed = max(1, closing_turn - character.last_update)
                self.goals.decide(character, elapsed)
                character.last_update = closing_turn
        self.world.turn = closing_turn
        for entity_id in sorted(self.world.characters):
            character = self.world.characters[entity_id]
            if not character.alive:
                continue
            self.needs.physiology(character)
            if character.health <= 0:
                character.alive = False
                self.spatial.positions.get(character.position, set()).discard(character.id)
                self.recorder.emit("CharacterDied", f"{character.name} morreu por privação.",
                                   target_id=character.id, location=character.position, historical=True)
                if character.goal:
                    character.goal.status = "failed"
                for need in character.needs.values():
                    self.needs.finish(character, need, "expired")
            elif character.is_player:
                self.needs.refresh(character)
        if self.world.turn % 6 == 0:
            self.knowledge.gossip()
        if self.world.turn % 24 == 0:
            self.economy.daily()
        self.quests.reconcile()
        self.world.rng_state = self.rng.getstate()

    def simulate(self, turns: int) -> None:
        if not isinstance(turns, int) or turns < 0:
            raise ValueError("Quantidade de turnos deve ser um inteiro não negativo.")
        for _ in range(turns):
            self.step()

    def nearby(self):
        if not self.player:
            return []
        return [self.world.characters[entity_id] for entity_id in self.spatial.at(self.player.position)
                if entity_id != self.player.id]

    def inventory(self, owner_id: int) -> list[dict]:
        owner = self.items.owner(owner_id)
        return [{"id": item_id, "name": self.world.items[item_id].name,
                 "kind": self.world.items[item_id].kind, "quantity": quantity,
                 "rarity": self.world.items[item_id].rarity,
                 "quality": self.world.items[item_id].quality}
                for item_id, quantity in owner.inventory.items()]

    def view(self) -> dict:
        player = self.player
        if not player:
            return {"turn": self.world.turn, "seed": self.world.seed}
        name, structures = self.navigation.describe(player.position)
        grid = self.world.maps[player.position.map_id]
        return {"turn": self.world.turn, "hour": self.world.turn % 24,
                "day": self.world.turn // 24 + 1, "seed": self.world.seed,
                "name": player.name, "nickname": player.nickname, "health": player.health,
                "alive": player.alive, "hunger": round(player.hunger), "thirst": round(player.thirst),
                "fatigue": round(player.fatigue), "money": player.money, "map_name": grid.name,
                "position": (player.position.x, player.position.y), "place": name,
                "structures": structures, "map": self.navigation.visible(player.position),
                "npcs": [{"id": npc.id, "name": npc.name, "profession": npc.profession,
                          "category": npc.category} for npc in self.nearby()],
                "bodies": [{"id": c.id, "name": c.name} for c in self.world.characters.values()
                           if not c.alive and c.position == player.position],
                "events": [fact.description for fact in player.knowledge.values()][-4:]}

    def _finish(self, success: bool, message: str, data=None) -> CommandResult:
        if success:
            self.step()
        return CommandResult(success, message, data)

    def _npc(self, entity_id: int):
        character = self.world.characters.get(entity_id)
        if character and character.alive and not character.is_player and character.position == self.player.position:
            return character
        return None

    def _action(self, action: str, need_kind="food", target_id=None):
        """Comandos reutilizam a execução que já atende aos NPCs."""
        player = self.player
        need = player.needs.get(need_kind)
        # Uma intenção temporária não aloca IDs nem cria pressão persistente.
        # O estado resultante da ação válida será percebido no tick normal.
        goal = Goal(0, need.id if need else 0, action, 0, self.world.turn, target_id=target_id)
        return self._finish(*self.goals.execute(player, goal, 1))

    def execute(self, text: str) -> CommandResult:
        try:
            tokens = shlex.split(text)
            if not tokens:
                return CommandResult(False, "Digite uma ação; ajuda lista os comandos.")
            command, args = tokens[0].lower(), tokens[1:]
            player = self.player
            if not player:
                return CommandResult(False, "Esta simulação não possui jogador.")
            if command in ("listar", "status", "mapa") and not args:
                return CommandResult(True, "Posição atual.", self.view())
            if command in ("inventário", "inventario") and not args:
                return CommandResult(True, "Inventário.", self.inventory(player.id))
            if command in ("necessidades",) and not args:
                return CommandResult(True, "Necessidades do jogador.",
                                     [{"type": need.kind, "priority": round(need.priority), "status": need.status,
                                       "reason": need.reason} for need in player.needs.values()])
            if command == "quests" and not args:
                return CommandResult(True, "Pedidos.", [{"id": quest.id, "title": quest.title,
                                                         "status": quest.status, "kind": quest.kind,
                                                         "owner_id": quest.owner_id, "target_id": quest.target_id,
                                                         "created_at": quest.created_at, "context": dict(quest.context)}
                                                        for quest in self.world.quests.values()])
            if command == "eventos" and not args:
                return CommandResult(True, "Acontecimentos conhecidos.",
                                     [fact.description for fact in player.knowledge.values()][-12:])
            if command == "fatos" and not args:
                return CommandResult(True, "Informações conhecidas.",
                                     [{"id": f.event_id, "kind": f.kind, "confidence": f.confidence,
                                       "description": f.description, "target_id": f.target_id, "turn": f.turn}
                                      for f in player.knowledge.values()])
            if not player.alive:
                return CommandResult(False, "Seu personagem morreu. Você pode carregar uma campanha ou sair.")
            if command in DIRECTIONS and not args:
                return self._finish(*self.navigation.move(player, command))
            if command == "mover" and len(args) == 1:
                return self._finish(*self.navigation.move(player, args[0].lower()))
            if command == "entrar" and not args:
                return self._finish(*self.navigation.enter(player))
            if command == "sair" and not args:
                return self._finish(*self.navigation.leave(player))
            if command == "esperar" and len(args) <= 1:
                turns = int(args[0]) if args else 1
                if not 1 <= turns <= 1000:
                    return CommandResult(False, "Use entre 1 e 1000 horas de espera.")
                self.simulate(turns)
                return CommandResult(True, f"O mundo avançou {turns} hora(s).")
            if command == "conversar" and len(args) == 1:
                npc = self._npc(int(args[0]))
                if not npc:
                    return CommandResult(False, "Esse NPC não está nesta posição.")
                self.graph.adjust(npc.id, player.id, "familiaridade", 2)
                message = self.knowledge.dialogue(npc, player)
                quest = self.quests.offer(npc, player)
                if quest:
                    message += f" Pedido #{quest.id}: {quest.title}. Use aceitar {quest.id} ou recusar {quest.id}."
                return self._finish(True, message)
            if command in ("aceitar", "recusar") and len(args) == 1:
                return self._finish(*self.quests.respond(int(args[0]), command == "aceitar"))
            if command == "investigar" and len(args) == 1:
                return self._finish(*self.personal_actions.locate(player, int(args[0])))
            if command == "informar" and len(args) == 2:
                npc, fact = self._npc(int(args[0])), player.knowledge.get(int(args[1]))
                if not npc or not fact:
                    return CommandResult(False, "Faltam interlocutor presente ou informação conhecida.")
                return self._finish(*self.personal_actions.inform(player, npc, fact))
            if command == "acompanhar" and len(args) == 1:
                npc = self._npc(int(args[0]))
                if not npc:
                    return CommandResult(False, "Esse NPC não está nesta posição.")
                return self._finish(*self.personal_actions.accompany(player, npc))
            if command == "entregar" and len(args) in (2, 3):
                npc = self._npc(int(args[0]))
                item_id = int(args[1])
                quantity = int(args[2]) if len(args) == 3 else 1
                if not npc:
                    return CommandResult(False, "Esse NPC não está nesta posição.")
                if quantity <= 0 or player.inventory.get(item_id, 0) < quantity:
                    return CommandResult(False, "Item ou quantidade indisponível.")
                kind = self.world.items[item_id].kind
                # Valor social exige carência real; mais presentes antes de
                # consumir o anterior não repetem o mesmo favor.
                urgency = (npc.hunger if kind == "food" and not self.items.count(npc.id, "food") else
                           npc.thirst if kind == "water" and not self.items.count(npc.id, "water") else 0)
                self.items.transfer(player.id, npc.id, item_id, quantity)
                self.quests.delivered(player, npc, kind, urgency)
                return self._finish(True, f"Item entregue a {npc.name}.")
            if command in ("comer", "beber") and not args:
                if command == "comer":
                    return self._action("eat")
                action = "drink" if self.items.count(player.id, "water") else "drink_well"
                town = self.world.towns.get(player.position.map_id)
                if action == "drink_well" and not town:
                    return CommandResult(False, "Não há água acessível aqui.")
                return self._action(action, "water")
            if command == "descansar" and not args:
                return self._action("sleep", "rest")
            if command == "coletar" and not args:
                return self._action("forage")
            if command == "trabalhar" and not args:
                return self._action("work" if player.profession else "work_for_food", "work")
            if command == "pedir" and len(args) == 2 and args[0] == "comida":
                npc = self._npc(int(args[1]))
                if not npc:
                    return CommandResult(False, "Esse NPC não está nesta posição.")
                return self._action("ask_help", target_id=npc.id)
            if command == "mercado" and not args:
                town = self.world.towns.get(player.position.map_id)
                if not town or player.position != town.market:
                    return CommandResult(False, "Vá até o mercado (M).")
                products = [{"product": label, "quantity": self.items.count(town.id, kind),
                             "price": self.economy.price(town.id, kind),
                             "sell_price": self.economy.sell_price(town.id, kind)}
                            for label, kind in PRODUCTS.items() if label != "água"]
                return CommandResult(True, f"Mercado de {town.name}.", products)
            if command == "comprar" and len(args) in (1, 2):
                town = self.world.towns.get(player.position.map_id)
                kind = PRODUCTS.get(args[0].lower(), args[0].lower())
                if not town:
                    return CommandResult(False, "Não há mercado nesta área.")
                return self._finish(*self.economy.buy(player.id, town.id, kind,
                                                     int(args[1]) if len(args) == 2 else 1))
            if command == "vender" and len(args) in (1, 2):
                town = self.world.towns.get(player.position.map_id)
                if not town:
                    return CommandResult(False, "Não há mercado nesta área.")
                return self._finish(*self.economy.sell(player.id, town.id, int(args[0]),
                                                      int(args[1]) if len(args) == 2 else 1))
            return CommandResult(False, "Comando ou argumentos inválidos. Use ajuda.")
        except (ValueError, IndexError) as error:
            return CommandResult(False, f"Não foi possível executar: {error}")
