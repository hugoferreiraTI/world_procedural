"""Inventários referenciam itens únicos; transferências dividem pilhas."""

from .models import Item, WorldState

NAMES = {"food": "Ração", "water": "Água", "grain": "Trigo", "iron": "Ferro",
         "wood": "Madeira", "weapon": "Espada de ferro", "tool": "Ferramentas"}
STACKABLE = {"food", "water", "grain", "iron", "wood"}


class ItemService:
    def __init__(self, world: WorldState, rng):
        self.world, self.rng = world, rng
        self.listeners = []

    def notify(self, kind, owner_id, product, quantity):
        for listener in self.listeners:
            listener(kind, owner_id, product, quantity)

    def owner(self, owner_id: int):
        return self.world.characters.get(owner_id) or self.world.towns.get(owner_id)

    def count(self, owner_id: int, kind: str) -> int:
        owner = self.owner(owner_id)
        return sum(quantity for item_id, quantity in owner.inventory.items()
                   if self.world.items[item_id].kind == kind)

    def first(self, owner_id: int, kind: str) -> int | None:
        return next((item_id for item_id in self.owner(owner_id).inventory
                     if self.world.items[item_id].kind == kind), None)

    def create(self, owner_id: int, kind: str, quantity: int = 1,
               creator_id: int | None = None, origin: str = "Geração inicial",
               category: str = "comum") -> Item:
        if quantity <= 0:
            raise ValueError("Quantidade deve ser positiva.")
        owner = self.owner(owner_id)
        if kind in STACKABLE:
            item_id = self.first(owner_id, kind)
            if item_id is not None:
                owner.inventory[item_id] += quantity
                self.notify("acquired", owner_id, kind, quantity)
                return self.world.items[item_id]
        quality = self.rng.randint(35, 65) + {"comum": 0, "importante": 20,
                                             "lendário": 35}.get(category, 0)
        rarity = "comum" if quality < 70 else "incomum" if quality < 90 else "raro"
        item = Item(self.world.allocate_id(), NAMES[kind], kind, owner_id,
                    min(100, quality), rarity, creator_id, self.world.turn, origin,
                    kind in STACKABLE, max(1, quality // 5) if kind == "weapon" else 0)
        self.world.items[item.id] = item
        owner.inventory[item.id] = quantity
        self.notify("acquired", owner_id, kind, quantity)
        return item

    def consume(self, owner_id: int, kind: str, quantity: int = 1) -> bool:
        if quantity <= 0 or self.count(owner_id, kind) < quantity:
            return False
        consumed = quantity
        inventory = self.owner(owner_id).inventory
        for item_id in list(inventory):
            if self.world.items[item_id].kind != kind:
                continue
            amount = min(inventory[item_id], quantity)
            inventory[item_id] -= amount
            quantity -= amount
            if inventory[item_id] == 0:
                del inventory[item_id]
                del self.world.items[item_id]
            if quantity == 0:
                self.notify("consumed", owner_id, kind, consumed)
                return True
        return False

    def transfer(self, source_id: int, target_id: int, item_id: int,
                 quantity: int = 1) -> Item:
        if source_id == target_id:
            raise ValueError("Origem e destino devem ser diferentes.")
        source, target = self.owner(source_id), self.owner(target_id)
        if quantity <= 0 or source.inventory.get(item_id, 0) < quantity:
            raise ValueError("Item ou quantidade indisponível.")
        item = self.world.items[item_id]
        product = item.kind
        source.inventory[item_id] -= quantity
        # Uma entidade física possui apenas um dono em cada instante.
        if source.inventory[item_id] == 0:
            del source.inventory[item_id]
            moved = item
            moved.owner_id = target_id
        else:
            moved = Item(self.world.allocate_id(), item.name, item.kind, target_id,
                         item.quality, item.rarity, item.creator_id, item.created_at,
                         item.origin, item.stackable, item.damage)
            self.world.items[moved.id] = moved
        if moved.stackable:
            existing = self.first(target_id, moved.kind)
            if existing is not None:
                target.inventory[existing] += quantity
                del self.world.items[moved.id]
                self.notify("transferred", source_id, product, quantity)
                self.notify("acquired", target_id, product, quantity)
                return self.world.items[existing]
        target.inventory[moved.id] = quantity
        self.notify("transferred", source_id, product, quantity)
        self.notify("acquired", target_id, product, quantity)
        return moved
