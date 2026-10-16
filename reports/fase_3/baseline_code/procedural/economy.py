"""Produção, consumo e dinheiro regionais; estoque nunca é infinito."""

import math

from .models import Goal, WorldState
from .items import NAMES

BASE_PRICES = {"food": 3, "water": 1, "grain": 2, "iron": 5, "wood": 2,
               "weapon": 24, "tool": 10}


class Economy:
    def __init__(self, world: WorldState, items, recorder, needs):
        self.world, self.items, self.recorder, self.needs = world, items, recorder, needs

    def market_value(self, town_id: int, kind: str, stock: int | None = None) -> float:
        town = self.world.towns[town_id]
        stock = self.items.count(town_id, kind) if stock is None else stock
        expected = max(8, town.population // 100) if kind in ("food", "grain") else 12
        scarcity = max(.45, min(4, expected / max(1, stock)))
        demand = min(1, town.demand.get(kind, 0) / 20)
        return BASE_PRICES[kind] * (scarcity + demand)

    def buy_price(self, town_id: int, kind: str, stock: int | None = None) -> int:
        return max(2, math.ceil(self.market_value(town_id, kind, stock) * 1.1))

    def sell_price(self, town_id: int, kind: str, stock: int | None = None) -> int:
        # O estoque é o que existirá APÓS receber esta unidade. Assim a curva
        # percorrida na revenda é exatamente a curva inversa da compra.
        stock = self.items.count(town_id, kind) + 1 if stock is None else stock
        return max(1, math.floor(self.market_value(town_id, kind, stock) * .65))

    def price(self, town_id: int, kind: str) -> int:
        return self.buy_price(town_id, kind)

    def can_seek_food(self, character) -> bool:
        """Viabilidade conhecida da intenção; não consulta estoque remoto."""
        market = character.known_places.get("market")
        town = self.world.towns.get(character.town_id)
        if (not town or market != town.market or market.map_id != character.position.map_id
                or character.money < 2):
            return False
        if character.position != market:
            return True  # Pode ir verificar; preço/estoque ainda são desconhecidos.
        return (self.items.count(town.id, "food") > 0 and
                character.money >= self.price(town.id, "food"))

    def quote(self, town_id: int, kind: str, quantity: int, buying: bool = True) -> int:
        stock = self.items.count(town_id, kind)
        if buying:
            return sum(self.buy_price(town_id, kind, stock - unit) for unit in range(quantity))
        return sum(self.sell_price(town_id, kind, stock + unit + 1) for unit in range(quantity))

    def buy(self, buyer_id: int, town_id: int, kind: str, quantity: int = 1) -> tuple[bool, str]:
        buyer, town = self.world.characters[buyer_id], self.world.towns[town_id]
        if buyer.position != town.market:
            return False, "Vá até o mercado (M) para comprar."
        if kind not in BASE_PRICES or quantity <= 0:
            return False, "Produto ou quantidade inválida."
        if self.items.count(town_id, kind) < quantity:
            return False, "O mercado está sem estoque suficiente."
        cost = self.quote(town_id, kind, quantity)
        if buyer.money < cost:
            return False, f"São necessárias {cost} moedas."
        item_id = self.items.first(town_id, kind)
        if not self.world.items[item_id].stackable and quantity != 1:
            return False, "Compre equipamentos individualmente."
        self.items.transfer(town_id, buyer_id, item_id, quantity)
        buyer.money -= cost
        town.money += cost
        self.recorder.emit("ItemBought", f"{buyer.name} comprou {quantity} unidade(s) de {NAMES[kind].lower()} por {cost} moedas.",
                           buyer.id, town.id, town.market)
        return True, f"Compra concluída por {cost} moedas."

    def sell(self, seller_id: int, town_id: int, item_id: int, quantity: int = 1) -> tuple[bool, str]:
        seller, town = self.world.characters[seller_id], self.world.towns[town_id]
        if seller.position != town.market:
            return False, "Vá até o mercado (M) para vender."
        if seller.inventory.get(item_id, 0) < quantity or quantity <= 0:
            return False, "Item ou quantidade indisponível."
        kind = self.world.items[item_id].kind
        if self.items.count(town_id, kind) + quantity > 240:
            return False, "O mercado não precisa de mais unidades deste produto."
        cost = self.quote(town_id, kind, quantity, buying=False)
        if town.money < cost:
            return False, "O mercado não possui dinheiro suficiente."
        self.items.transfer(seller_id, town_id, item_id, quantity)
        seller.money += cost
        town.money -= cost
        self.recorder.emit("ItemSold", f"{seller.name} vendeu mercadorias por {cost} moedas.",
                           seller.id, town.id, town.market)
        return True, f"Venda concluída por {cost} moedas."

    def wage(self, character, hours: int) -> None:
        town = self.world.towns[character.town_id]
        amount = min(town.money, hours)
        town.money -= amount
        character.money += amount

    def daily(self) -> None:
        for town in self.world.towns.values():
            town.wild_food = min(30, town.wild_food + 15)
            water = min(80, max(0, 160 - self.items.count(town.id, "water")))
            if water:
                self.items.create(town.id, "water", water, origin=f"Poço de {town.name}")
            for kind in town.demand:
                town.demand[kind] = max(0, town.demand[kind] - 8)
            population = max(0, town.population - len(town.resident_ids))
            required = max(1, math.ceil(population / 120))
            price = self.price(town.id, "food")
            bought = min(required, self.items.count(town.id, "food"), town.abstract_money // price)
            if bought:
                self.items.consume(town.id, "food", bought)
                town.abstract_money -= bought * price
                town.money += bought * price
            # Renda da população abstrata deriva do trabalho diário de seus
            # habitantes, da mesma forma que a colheita representa recursos renováveis.
            income = population // 100
            town.abstract_money += income
            self.world.metrics["MoneySourceAbstractWork"] = self.world.metrics.get("MoneySourceAbstractWork", 0) + income
            shortage = required - bought
            if shortage:
                was_active = town.needs.get("food") and town.needs["food"].status not in ("satisfied", "expired")
                need = self.needs.ensure(town, "food", min(100, 50 + shortage * 3),
                                         "consumption", f"Faltam {shortage} lotes diários de alimento")
                need.priority = need.base_urgency
                need.status = "selected"
                town.goal = Goal(self.world.allocate_id(), need.id, "expand_farming", 70, self.world.turn)
                # Mobilização rural é uma ação coletiva limitada por mão de obra e tesouro.
                units = min(shortage * 2, population // 100, town.money,
                            max(0, 240 - self.items.count(town.id, "grain")))
                if units:
                    town.money -= units
                    town.abstract_money += units
                    self.items.create(town.id, "grain", units, origin="Colheita de trabalhadores locais")
                    town.goal.status = "completed"
                else:
                    need.status = "blocked"
                    town.goal.status = "failed"
                if not was_active:
                    self.recorder.emit("FoodShortage", f"{town.name} sofre falta de alimentos.",
                                       target_id=town.id, location=town.market)
            else:
                self.needs.satisfy(town, "food")
        for kingdom in self.world.kingdoms.values():
            struggling = [self.world.towns[entity_id] for entity_id in kingdom.city_ids + kingdom.village_ids
                          if self.world.towns[entity_id].needs.get("food") and
                          self.world.towns[entity_id].needs["food"].status not in ("satisfied", "expired")]
            if struggling:
                need = self.needs.ensure(kingdom, "food", min(100, 40 + len(struggling) * 10),
                                         "city_reports", "Escassez relatada pelas cidades")
                need.priority, need.status = need.base_urgency, "selected"
                kingdom.economic_state = "em crise"
                kingdom.goal = Goal(self.world.allocate_id(), need.id, "fund_farming", 70, self.world.turn)
                target = min(struggling, key=lambda town: town.money)
                aid = min(30, kingdom.treasury)
                kingdom.treasury -= aid
                target.money += aid
                kingdom.goal.target_id = target.id
                kingdom.goal.status = "completed" if aid else "failed"
                if not aid:
                    need.status = "blocked"
            else:
                self.needs.satisfy(kingdom, "food")
                kingdom.economic_state = "estável"
