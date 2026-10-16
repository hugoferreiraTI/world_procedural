"""Geração por etapas usando um único RNG e uma versão explícita das regras."""

from dataclasses import dataclass
import hashlib
import random

from . import RULES_VERSION
from .events import EventBus, EventRecorder, SpatialIndex
from .items import ItemService
from .models import (Area, Character, Faction, Grid, Kingdom, Location,
                     Personality, PointOfInterest, Town, WorldState)
from .relationships import RelationshipGraph
from .population import Population

FIRST_NAMES = ("Aldren", "Mira", "Cael", "Tomas", "Elena", "Arthus", "Lyra",
               "John", "Marie", "Nora", "Darin", "Iria", "Silas", "Ruan", "Bela")
FAMILY_NAMES = ("Valerius", "Hammer", "Stone", "Arven", "Vale", "Kars", "Solaris",
                "Ferros", "Alvor", "Montes", "Luar", "Bruma", "Corven", "Douran")
PROFESSIONS = ("agricultor", "cozinheiro", "ferreiro", "mineiro", "lenhador",
               "comerciante", "guarda", "caçador")


@dataclass(frozen=True)
class GenerationConfig:
    width: int = 500
    height: int = 500
    kingdom_count: int = 6
    minimum_distance: int = 5
    maximum_village_distance: int = 18
    npcs_per_city: int = 8
    historical_turns: int = 24

    def validate(self) -> None:
        if self.width != 500 or self.height != 500:
            raise ValueError("Esta versão usa o mapa global 500×500 da especificação.")
        if not 1 <= self.kingdom_count <= 6:
            raise ValueError("A quantidade de reinos deve ficar entre 1 e 6.")
        if not 1 <= self.minimum_distance <= 12:
            raise ValueError("Distância mínima deve ficar entre 1 e 12.")
        if not self.minimum_distance < self.maximum_village_distance <= 24:
            raise ValueError("Distância máxima de vilas deve ser maior que a mínima e até 24.")
        if self.npcs_per_city < 8 or self.historical_turns < 0:
            raise ValueError("Use pelo menos 8 NPCs por cidade e histórico não negativo.")


def seed_number(seed: str) -> int:
    return int.from_bytes(hashlib.sha256(f"{RULES_VERSION}:{seed}".encode()).digest(), "big")


def make_local_grid(entity_id: int, name: str, size: int, outside: Location,
                    capital: bool = False, interior: bool = False, rng=None) -> Grid:
    rows = [["#" if x in (0, size - 1) or y in (0, size - 1) else "."
             for x in range(size)] for y in range(size)]
    center = size // 2
    rows[size - 1][center] = "G"
    areas = {f"{center}:{size - 1}": Area("Portão sul", ["Portão"])}
    if interior:
        for _ in range(size):
            x, y = rng.randint(1, size - 2), rng.randint(1, size - 2)
            # Preserva o corredor central até a entrada.
            if x != center:
                rows[y][x] = "#"
        areas[f"{center}:{center}"] = Area("Salão interno", ["Restos antigos"])
    else:
        rows[size - 2][center] = "M"
        rows[2][2] = "H"
        rows[2][size - 3] = "W"
        rows[1][center] = "P" if capital else "T"
        rows[size - 2][1] = "A"
        areas.update({
            f"{center}:{size - 2}": Area("Distrito comercial", ["Mercado", "Taverna", "Poço"]),
            "2:2": Area("Distrito residencial", ["Casas", "Poço"]),
            f"{size - 3}:2": Area("Distrito artesanal", ["Ferreiro", "Oficinas"]),
            f"{center}:1": Area("Palácio real" if capital else "Praça do templo",
                                  ["Palácio", "Quartel", "Templo"] if capital else ["Templo", "Praça"]),
            f"1:{size - 2}": Area("Área rural", ["Hortas", "Bosque", "Poço"]),
        })
        # Áreas adicionais variam entre cidades, sem alterar os acessos essenciais.
        for y in range(3, size - 3):
            x = rng.choice([1, size - 2])
            areas[f"{x}:{y}"] = Area(rng.choice(["Praça", "Residências", "Quartel"]),
                                       [rng.choice(["Casas", "Jardim", "Posto da guarda"])])
    return Grid(entity_id, name, size, size, ["".join(row) for row in rows], areas, outside)


def generate_world(seed: str = "Dovha", player_name: str = "Viajante",
                   with_player: bool = True,
                   config: GenerationConfig | None = None) -> WorldState:
    config = config or GenerationConfig()
    config.validate()
    seed = seed.strip()
    if not seed:
        raise ValueError("A seed precisa conter um nome.")
    rng = random.Random(seed_number(seed))
    world = WorldState(seed, RULES_VERSION, 1)
    graph, items = RelationshipGraph(world), ItemService(world, rng)

    # Regiões de bioma contínuas, com pequenas irregularidades por célula.
    regions = [[rng.choice(".FDS") for _ in range(25)] for _ in range(25)]
    rows = []
    for y in range(config.height):
        rows.append("".join(regions[y // 20][x // 20] if rng.random() > .08
                            else rng.choice(".FDS") for x in range(config.width)))
    world.maps[1] = Grid(1, "Mundo", config.width, config.height, rows)
    used_positions: list[Location] = []

    def free(position: Location) -> bool:
        return all(abs(position.x - other.x) + abs(position.y - other.y) >=
                   config.minimum_distance for other in used_positions)

    def choose_position(bounds, near: Location | None = None) -> Location:
        x0, y0, x1, y1 = bounds
        for _ in range(3000):
            if near:
                radius = config.maximum_village_distance
                x = rng.randint(max(x0 + 2, near.x - radius), min(x1 - 3, near.x + radius))
                y = rng.randint(max(y0 + 2, near.y - radius), min(y1 - 3, near.y + radius))
            else:
                x, y = rng.randint(x0 + 8, x1 - 9), rng.randint(y0 + 8, y1 - 9)
            position = Location(1, x, y)
            if near and abs(x - near.x) + abs(y - near.y) > config.maximum_village_distance:
                continue
            if free(position):
                used_positions.append(position)
                return position
        raise ValueError("Não foi possível distribuir pontos com estas distâncias.")

    def town_name() -> str:
        return rng.choice(("Ar", "Val", "Nor", "Kar", "Eli", "Mor", "Sil", "Dor")) + rng.choice(
            ("ven", "dor", "mar", "len", "ria", "thon", "mir", "via"))

    def add_town(kingdom: Kingdom | None, position: Location, kind: str,
                 capital: bool = False) -> Town:
        entity_id = world.allocate_id()
        name = town_name()
        size = 11 if capital else rng.choice([7, 9]) if kind == "cidade" else 7
        grid = make_local_grid(entity_id, name, size, position, capital, rng=rng)
        world.maps[entity_id] = grid
        population = rng.randint(2400, 4500) if capital else rng.randint(600, 1800) if kind == "cidade" else rng.randint(120, 450)
        town = Town(entity_id, name, kingdom.id if kingdom else None, position,
                    Location(entity_id, size // 2, size - 2), kind, capital,
                    population, rng.choice(["grain", "iron", "wood"]),
                    rng.randint(800, 1600), population * 10)
        world.towns[entity_id] = town
        town.abstract_population = population
        town.cooking_slots = max(1, (population // 120 + 30) // 30 + 1)
        for resource, amount in (("food", 40), ("water", 80), ("grain", 40), ("iron", 24), ("wood", 24)):
            items.create(town.id, resource, amount, origin=f"Reservas de {name}")
        if kingdom:
            (kingdom.city_ids if kind == "cidade" else kingdom.village_ids).append(entity_id)
            graph.set(entity_id, kingdom.id, "pertence_a", 100)
            if capital:
                kingdom.capital_id = entity_id
        return town

    def add_character(town: Town, profession: str | None, surname: str | None = None,
                      name: str | None = None, category: str = "comum") -> Character:
        grid = world.maps[town.id]
        home = Location(town.id, 2, 2)
        work = (Location(town.id, grid.width - 3, 2) if profession in ("ferreiro", "mineiro", "lenhador")
                else Location(town.id, 1, grid.height - 2) if profession in ("agricultor", "caçador")
                else town.market)
        family = surname or rng.choice(FAMILY_NAMES)
        personality = Personality(*(rng.randint(5, 95) for _ in range(11)))
        kingdom = world.kingdoms.get(town.kingdom_id)
        character = Character(world.allocate_id(), name or f"{rng.choice(FIRST_NAMES)} {family}",
                              family, town.market, home, work, town.id, profession, personality,
                              category=category, faction=town.kingdom_id,
                              religion=kingdom.religion if kingdom else "Culto da Aurora",
                              devotion=rng.randint(0, 100), money=rng.randint(1, 28),
                              hunger=rng.randint(10, 60), fatigue=rng.randint(0, 20))
        character.known_places = {"market": town.market, "home": home, "work": work,
                                  "forage": Location(town.id, 1, grid.height - 2),
                                  "well_home": home,
                                  "well_rural": Location(town.id, 1, grid.height - 2)}
        world.characters[character.id] = character
        Population(world).register(town, character)
        items.create(character.id, "food", rng.randint(1, 2), origin="Mantimentos pessoais")
        if profession in ("ferreiro", "agricultor", "mineiro", "lenhador", "cozinheiro"):
            items.create(character.id, "tool", creator_id=None)
        if profession in ("guarda", "caçador") or category != "comum":
            items.create(character.id, "weapon", category=category)
        if character.faction:
            graph.set(character.id, character.faction, "lealdade", rng.randint(15, 95))
        return character

    centers = [(85, 85), (250, 85), (415, 85), (85, 340), (250, 340), (415, 340)]
    surnames = rng.sample(FAMILY_NAMES, config.kingdom_count)
    for index in range(config.kingdom_count):
        cx, cy = centers[index]
        span = 100 if index == 0 else rng.randint(60, 85)
        bounds = (cx - span // 2, cy - span // 2, cx + span // 2, cy + span // 2)
        kingdom = Kingdom(world.allocate_id(), f"Reino {surnames[index]}", surnames[index],
                          bounds, index == 0, rng.choice(["agrária", "artesanal", "militar"]),
                          rng.choice(["Culto do Sol", "Ordem da Maré", "Culto da Aurora"]))
        world.kingdoms[kingdom.id] = kingdom
        for city_index in range(rng.randint(4, 6)):
            town = add_town(kingdom, choose_position(bounds), "cidade", city_index == 0)
            for npc_index in range(config.npcs_per_city):
                add_character(town, PROFESSIONS[npc_index % len(PROFESSIONS)])
            for _ in range(rng.randint(1, 2)):
                village = add_town(kingdom, choose_position(bounds, town.position), "vila")
                for profession in ("agricultor", "cozinheiro", "guarda", "caçador"):
                    add_character(village, profession)
        capital = world.towns[kingdom.capital_id]
        ruler = add_character(capital, "governante", kingdom.family_name,
                              seed if index == 0 else None, "lendário" if index == 0 else "importante")
        consort = add_character(capital, "conselheiro", kingdom.family_name, category="importante")
        heir = add_character(capital, "estudante", kingdom.family_name, category="importante")
        kingdom.ruler_id, kingdom.heir_id = ruler.id, heir.id
        kingdom.royal_family = [ruler.id, consort.id, heir.id]
        graph.set(ruler.id, consort.id, "casamento", 90, reciprocal=True)
        for parent in (ruler, consort):
            graph.set(parent.id, heir.id, "pai_de", 100)
            graph.set(heir.id, parent.id, "filho_de", 100)
        if index == 0:
            world.primordial_id = ruler.id

    for town in world.towns.values():
        residents = town.resident_ids
        # Famílias comuns permanecem personagens reais com sobrenome coerente.
        if len(residents) >= 4:
            a, b = world.characters[residents[0]], world.characters[residents[1]]
            b.name = b.name.rsplit(" ", 1)[0] + " " + a.surname
            b.surname = a.surname
            graph.set(a.id, b.id, "casamento", rng.randint(60, 100), reciprocal=True)
        for a, b in zip(residents, residents[1:]):
            graph.set(a, b, "amizade", rng.randint(10, 90), reciprocal=True)
            graph.set(a, b, "confiança", rng.randint(20, 70), reciprocal=True)
    kingdom_ids = list(world.kingdoms)
    for index, a in enumerate(kingdom_ids):
        for b in kingdom_ids[index + 1:]:
            graph.set(a, b, "diplomacia", rng.randint(-45, 65), reciprocal=True)

    for index in range(8):
        point_id = world.allocate_id()
        kind = "quartel-general" if index < 2 else rng.choice(["caverna", "castelo abandonado"])
        point = PointOfInterest(point_id, f"{kind.capitalize()} de {town_name()}", kind,
                                choose_position((0, 0, 500, 500)))
        world.points[point.id] = point
        world.maps[point.id] = make_local_grid(point.id, point.name, 11 if index < 2 else 9,
                                              point.position, interior=index >= 2, rng=rng)
        if index < 2:
            town = next(iter(world.towns.values()))
            leader = add_character(town, "caçador", category="importante")
            faction_id = world.allocate_id()
            leader.faction = faction_id
            headquarters = Location(point.id, 5, 5)
            leader.position = leader.home = leader.workplace = headquarters
            # Líder mantém conhecimento da cidade natal, mas não acessa seus
            # recursos remotamente; sobrevivência ocorre no próprio quartel.
            leader.known_places = {"home": headquarters, "work": headquarters,
                                  "forage": headquarters}
            faction = Faction(faction_id, rng.choice(["Companhia", "Irmandade"]) + " de " + town_name(),
                              leader.id, point.id, "caçadores" if index == 0 else "mercenários")
            world.factions[faction.id] = faction
            graph.set(leader.id, faction.id, "lealdade", 100)

    world.rng_state = rng.getstate()
    # Importação tardia mantém a geração independente da apresentação.
    from .engine import Engine
    engine = Engine(world)
    for kingdom in world.kingdoms.values():
        engine.recorder.emit("KingdomFounded", f"{kingdom.name} foi fundado sob a família {kingdom.family_name}.",
                             kingdom.ruler_id, kingdom.id,
                             world.characters[kingdom.ruler_id].position, historical=True)
    engine.simulate(config.historical_turns)
    if with_player:
        first_capital = world.towns[next(iter(world.kingdoms.values())).capital_id]
        position = first_capital.position
        player = Character(world.allocate_id(), player_name.strip() or "Viajante", "", position,
                           position, position, first_capital.id, None, Personality(),
                           is_player=True, money=25, last_update=world.turn)
        world.characters[player.id] = player
        world.player_id = player.id
        for kind, quantity in (("food", 4), ("water", 6)):
            engine.items.create(player.id, kind, quantity, origin="Mantimentos da viagem")
        engine.spatial.rebuild()
    world.rng_state = engine.rng.getstate()
    return world
