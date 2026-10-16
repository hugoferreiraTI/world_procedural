"""Navegação cardinal em mapas independentes; muralhas são intransponíveis."""

from collections import deque

from .models import Character, Location, WorldState

DIRECTIONS = {"norte": (0, -1), "sul": (0, 1), "leste": (1, 0), "oeste": (-1, 0)}
SYMBOLS = {".": "Planície", "F": "Floresta", "D": "Deserto", "S": "Pântano",
           "#": "Muralha", "G": "Portão", "M": "Mercado", "H": "Residências",
           "W": "Oficinas", "P": "Palácio", "T": "Templo", "A": "Área rural",
           "R": "Estrada"}


def distance(a: Location, b: Location) -> int:
    if a.map_id != b.map_id:
        return 1000
    return abs(a.x - b.x) + abs(a.y - b.y)


def passable(world: WorldState, position: Location) -> bool:
    grid = world.maps.get(position.map_id)
    return bool(grid and 0 <= position.x < grid.width and
                0 <= position.y < grid.height and grid.rows[position.y][position.x] != "#")


class Navigation:
    def __init__(self, world: WorldState, spatial):
        self.world, self.spatial = world, spatial
        self.path_cache: dict[tuple[Location, Location], Location | None] = {}

    def relocate(self, character: Character, position: Location) -> None:
        old = character.position
        character.position = position
        self.spatial.move(character.id, old, position)

    def point_at(self, position: Location):
        if position.map_id != self.world.world_map_id:
            return None
        return next((point for point in (*self.world.towns.values(), *self.world.points.values())
                     if point.position == position), None)

    def enter(self, character: Character) -> tuple[bool, str]:
        point = self.point_at(character.position)
        if point is None:
            return False, "Não há entrada nesta posição."
        grid = self.world.maps[point.id]
        self.relocate(character, Location(grid.id, grid.width // 2, grid.height - 1))
        if point.id in self.world.towns:
            town = self.world.towns[point.id]
            if character.is_player:
                character.town_id = town.id
            character.known_places.update({"market": town.market,
                                          "forage": Location(town.id, 1, grid.height - 2),
                                          "well_rural": Location(town.id, 1, grid.height - 2)})
        return True, f"Você entrou em {point.name}."

    def leave(self, character: Character) -> tuple[bool, str]:
        grid = self.world.maps[character.position.map_id]
        symbol = grid.rows[character.position.y][character.position.x]
        if grid.exit_to is None or symbol != "G":
            return False, "Para sair, vá até um portão (G)."
        self.relocate(character, grid.exit_to)
        return True, "Você voltou ao mapa externo."

    def move(self, character: Character, direction: str) -> tuple[bool, str]:
        if direction not in DIRECTIONS:
            return False, "Use norte, sul, leste ou oeste."
        dx, dy = DIRECTIONS[direction]
        current = character.position
        new = Location(current.map_id, current.x + dx, current.y + dy)
        grid = self.world.maps[current.map_id]
        if not (0 <= new.x < grid.width and 0 <= new.y < grid.height):
            if grid.exit_to is not None and grid.rows[current.y][current.x] == "G":
                return self.leave(character)
            return False, "Você alcançou o limite do mapa."
        if not passable(self.world, new):
            return False, "Uma muralha bloqueia a passagem. Procure um portão."
        self.relocate(character, new)
        return True, f"Você se moveu para {direction}."

    def approach(self, character: Character, destination: Location, steps: int = 1) -> bool:
        if character.position.map_id != destination.map_id:
            return False
        if character.combat.detention_until>self.world.turn or character.combat.surrendered_until>self.world.turn:
            return character.position==destination
        if character.combat.injured>=20:steps=max(1,int(steps*(1-character.combat.injured/150)))
        for _ in range(steps):
            start = character.position
            if start == destination:
                return True
            key = (start, destination)
            if start.map_id==self.world.world_map_id:
                dx=1 if destination.x>start.x else -1 if destination.x<start.x else 0
                dy=0 if dx else 1 if destination.y>start.y else -1
                self.relocate(character,Location(start.map_id,start.x+dx,start.y+dy))
                continue
            if key not in self.path_cache:
                previous: dict[Location, Location | None] = {start: None}
                queue = deque([start])
                while queue and destination not in previous:
                    current = queue.popleft()
                    for dx, dy in DIRECTIONS.values():
                        point = Location(start.map_id, current.x + dx, current.y + dy)
                        if point not in previous and passable(self.world, point):
                            previous[point] = current
                            queue.append(point)
                step = destination if destination in previous else None
                while step is not None and previous[step] not in (None, start):
                    step = previous[step]
                if len(self.path_cache) >= 4096:
                    self.path_cache.clear()
                self.path_cache[key] = step
            step = self.path_cache[key]
            if step is None:
                return False
            self.relocate(character, step)
        return character.position == destination

    def visible(self, position: Location) -> list[list[str]]:
        grid = self.world.maps[position.map_id]
        result = []
        for y in range(position.y - 2, position.y + 3):
            row = []
            for x in range(position.x - 2, position.x + 3):
                point = Location(grid.id, x, y)
                if point == position:
                    symbol = "@"
                elif not (0 <= x < grid.width and 0 <= y < grid.height):
                    symbol = " "
                else:
                    poi = self.point_at(point)
                    symbol = ("C" if poi.kind == "cidade" else "V" if poi.kind == "vila"
                              else "?" if poi else grid.rows[y][x]) if poi else grid.rows[y][x]
                row.append(symbol)
            result.append(row)
        return result

    def describe(self, position: Location) -> tuple[str, list[str]]:
        grid = self.world.maps[position.map_id]
        area = grid.areas.get(f"{position.x}:{position.y}")
        poi = self.point_at(position)
        if poi:
            return poi.name, ["Entrada: use entrar"]
        if area:
            return area.name, list(area.structures)
        return SYMBOLS.get(grid.rows[position.y][position.x], "Área interna"), []
