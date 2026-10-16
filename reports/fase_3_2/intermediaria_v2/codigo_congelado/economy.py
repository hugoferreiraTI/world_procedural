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
            observed = character.market_observation
            if (observed.get("town_id") == town.id and
                    self.world.turn-observed.get("price_turn",-1000) <= 24):
                return observed.get("stock",{}).get("food",0) > 0 and character.money >= observed["price"]
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

    def buy_reserve(self, person, target, bulk=False):
        """Lote limitado ao déficit, estoque e curva marginal de preço real."""
        town = self.world.towns[person.town_id]
        deficit = max(0, target-self.items.count(person.id, 'food'))
        limit = min(deficit, self.items.count(town.id, 'food'), target if bulk else 1)
        quantity = 0
        for amount in range(1, limit+1):
            if self.quote(town.id, 'food', amount) > person.money:
                break
            quantity = amount
        if quantity == 0:
            return False, 'Não há compra possível para o déficit atual.'
        success, message = self.buy(person.id, town.id, 'food', quantity)
        if success:
            for name, count in (('ReservePurchaseUnits', quantity), ('ReservePurchasePartial', quantity < deficit),
                                ('ReservePurchaseSecondRation', self.items.count(person.id, 'food') >= 2)):
                self.world.metrics[name] = self.world.metrics.get(name, 0)+count
        return success, message

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

    def wage(self, character, hours: int, sixths=False) -> int:
        town = self.world.towns[character.town_id]
        character.wage_credit += hours if sixths else hours * 6
        amount = min(town.money, character.wage_credit // 6)
        town.money -= amount
        character.money += amount
        character.wage_credit -= amount * 6
        return amount

    def has_kitchen(self, town):
        area = self.world.maps[town.id].areas.get(f"{town.market.x}:{town.market.y}")
        return bool(area and 'Taverna' in area.structures and town.cooking_slots > 0)

    def food_diagnosis(self, town):
        """Relatório administrativo local; não é conhecimento automático de NPC."""
        people = [self.world.characters[i] for i in town.resident_ids]
        local = [c for c in people if c.alive and c.position.map_id == town.id]
        stock = {k:self.items.count(town.id,k) for k in ('food','grain','water','iron','wood')}
        abstract = town.abstract_population or 0
        demand = (math.ceil(abstract/120) if abstract else 0) + 1.2 * len(local)
        cooks = sum(c.profession=='cozinheiro' for c in local)
        hunters = sum(c.profession=='caçador' for c in local)
        kitchen = self.has_kitchen(town)
        capacity = min(cooks,town.cooking_slots)*30 if kitchen else 0
        hunting_capacity = hunters*20
        required = max(1 if stock['food']<demand else 0, math.ceil(max(0,demand-hunting_capacity)/30))
        trainees = sum(c.training_target=='cozinheiro' for c in local)
        deficit = max(0,required-cooks) if kitchen else 0
        projected_deficit = max(0,deficit-trainees)
        tags = []
        insufficient = stock['food'] < demand
        raw_required = math.ceil(max(12,demand)*2/3)*2
        if insufficient and stock['grain']+town.grain_credit/3 < raw_required:
            tags.append('RAW_MATERIAL_SHORTAGE')
        if insufficient and (not kitchen or cooks==0 or capacity+hunting_capacity<demand):
            tags.append('PROCESSING_CAPACITY_SHORTAGE')
        if insufficient and cooks==0 and kitchen:
            tags.append('LABOR_SHORTAGE')
        price = self.price(town.id,'food')
        poor = sum(c.money<price and not self.items.count(c.id,'food') for c in local)
        if stock['food']>0 and poor:
            tags.append('AFFORDABILITY_PROBLEM')
        if any(self.professions.saturated(c,{'stock':stock}) for c in local):
            tags.append('STORAGE_BLOCKAGE')
        realized = town.production_previous.get('food',0)
        if insufficient and cooks and capacity+hunting_capacity>=demand and realized<demand:
            tags.append('LOCAL_ACCESS_PROBLEM')
        external = [other.id for other in self.world.towns.values() if other.id!=town.id and
                    other.kingdom_id==town.kingdom_id and other.economic_report and
                    self.world.turn-other.economic_report.get('turn',-1000)<=24 and
                    other.economic_report['stock']['food']>other.economic_report['expected_demand']*2]
        if insufficient and external:
            tags.append('TRANSPORT_SHORTAGE')
        return {'turn':self.world.turn,'stock':stock,'expected_demand':round(demand,2),
                'processing_capacity':capacity,'hunting_capacity':hunting_capacity,
                'production_capacity':capacity+hunting_capacity,'actual_production':realized,
                'capacity_deficit':max(0,round(demand-capacity-hunting_capacity,2)),
                'cook_count':cooks,'required_cooks':required,'professional_deficit':deficit,
                'projected_professional_deficit':projected_deficit,
                'raw_required':raw_required,'poor_residents':poor,'bottlenecks':tags,
                'external_supply_reports':external,'transport_available':False}

    def observe(self, person):
        town = self.world.towns.get(person.position.map_id)
        if not town or person.town_id!=town.id:
            return
        visible_places = [person.known_places.get(k) for k in ('market','work','forage')]
        if person.position not in visible_places:
            return
        # Quadro local: só quem chegou ao mercado observa o preço atual.
        old = person.market_observation
        stock = {k:self.items.count(town.id,k) for k in ('food','grain','water','iron','wood')}
        report = town.economic_report
        offers = bool(report and (report['stock']['food']<report['expected_demand']*2 or
                                  'AFFORDABILITY_PROBLEM' in report['bottlenecks']))
        opportunities = self.professions.temporary_capacity(town) if offers else {}
        observation = {'turn':self.world.turn,'town_id':town.id,'stock':stock,
                       'temporary_work':bool(opportunities), 'temporary_offers':opportunities,
                       'offers_observed_at':self.world.turn, 'offers_expire_at':self.world.turn+24,
                       'training_offer':None}
        if person.position == town.market:
            observation.update({'price':self.price(town.id,'food'),'price_turn':self.world.turn})
            vacancy = town.professional_demand.get('cozinheiro',{})
            if vacancy.get('projected_deficit',vacancy.get('deficit')) and self.world.turn-vacancy.get('since',self.world.turn)>=48:
                observation['training_offer']='cozinheiro'
        elif old.get('town_id')==town.id:
            for key in ('price','price_turn','training_offer'):
                if key in old: observation[key]=old[key]
        person.market_observation=observation

    def known_unaffordable(self, person, target=1):
        deficit = max(0, target-self.items.count(person.id,'food'))
        if not deficit:
            return False
        town = self.world.towns.get(person.town_id)
        if town and person.position==town.market:
            stock = self.items.count(town.id, 'food')
            return person.money < self.quote(town.id, 'food', min(deficit, max(1, stock)))
        seen = person.market_observation
        if (seen.get('town_id')==person.town_id and self.world.turn-seen.get('price_turn',-1000)<=24):
            return person.money < deficit*seen['price']
        # Sem cotação, falta de informação não prova falta de dinheiro.
        # Quem tem o mínimo conhecido pode ir verificar o mercado; manter
        # trabalho como solução de fome aqui prendia NPCs ricos na produção.
        return person.money < deficit*2

    def daily(self) -> None:
        for town in self.world.towns.values():
            town.production_previous, town.production_today = town.production_today, {}
            town.wild_food = min(30,town.wild_food+15)
            water = min(80,max(0,160-self.items.count(town.id,'water')))
            if water: self.items.create(town.id,'water',water,origin=f'Poço de {town.name}')
            for kind in town.demand: town.demand[kind]=max(0,town.demand[kind]-8)
            population = town.abstract_population or 0
            required = max(0,(math.ceil(population/120) if population else 0)-town.meals_served_today)
            town.meals_served_today = 0
            price = self.price(town.id,'food')
            bought = min(required,self.items.count(town.id,'food'),town.abstract_money//price)
            if bought:
                self.items.consume(town.id,'food',bought)
                town.abstract_money-=bought*price; town.money+=bought*price
            income=population//100
            town.abstract_money+=income
            self.world.metrics['MoneySourceAbstractWork']=self.world.metrics.get('MoneySourceAbstractWork',0)+income
            report=self.food_diagnosis(town)
            town.economic_report=report
            deficit=report['professional_deficit']
            previous=town.professional_demand.get('cozinheiro',{})
            if deficit:
                town.professional_demand['cozinheiro']={'deficit':deficit,'required':report['required_cooks'],
                    'projected_deficit':report['projected_professional_deficit'],
                    'since':previous.get('since',self.world.turn),'stage':previous.get('stage','utilization')}
                need=self.needs.ensure(town,'professional',55,'capacity','Capacidade culinária abaixo da demanda')
                need.context.update(town.professional_demand['cozinheiro'])
            else:
                if previous:
                    self.world.metrics['VacancyClosed']=self.world.metrics.get('VacancyClosed',0)+1
                    self.world.metrics['VacancyHours']=self.world.metrics.get('VacancyHours',0)+self.world.turn-previous['since']
                town.professional_demand.pop('cozinheiro',None)
                self.needs.satisfy(town,'professional')
            pressure = required>bought or bool(report['bottlenecks'])
            if pressure:
                current=town.needs.get('food')
                was_active=bool(current and current.status not in ('satisfied','expired'))
                need=self.needs.ensure(town,'food',min(100,50+max(0,required-bought)*3),
                    'local_report','Diagnóstico da cadeia local de alimentos')
                need.context.update(report)
                need.priority=need.base_urgency
                self.goals.collective(town,need,report)
                if required>bought and not was_active:
                    self.recorder.emit('FoodShortage',f'{town.name} sofre falta de alimentos.',target_id=town.id,location=town.market)
            else:
                self.needs.satisfy(town,'food')
        for kingdom in self.world.kingdoms.values():
            struggling=[self.world.towns[i] for i in kingdom.city_ids+kingdom.village_ids
                if self.world.towns[i].economic_report.get('stock',{}).get('food',0)<
                   self.world.towns[i].economic_report.get('expected_demand',0)]
            if struggling:
                need=self.needs.ensure(kingdom,'food',min(100,40+len(struggling)*10),'city_reports','Escassez relatada pelas cidades')
                need.priority,need.status=need.base_urgency,'selected'; kingdom.economic_state='em crise'
                kingdom.goal=Goal(self.world.allocate_id(),need.id,'fund_local_response',70,self.world.turn)
                target=min(struggling,key=lambda town:town.money); aid=min(30,kingdom.treasury)
                kingdom.treasury-=aid; target.money+=aid
                kingdom.goal.target_id=target.id; kingdom.goal.status='completed' if aid else 'failed'
                if not aid: need.status='blocked'
            else:
                self.needs.satisfy(kingdom,'food'); kingdom.economic_state='estável'
