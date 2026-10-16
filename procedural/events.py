"""Event Bus interno e registro limitado de eventos cotidianos."""

from collections import defaultdict
from collections.abc import Callable

from .models import Event, Location, WorldState


class EventBus:
    def __init__(self):
        self.handlers: dict[str, list[Callable[[Event], None]]] = defaultdict(list)

    def subscribe(self, kind: str, handler: Callable[[Event], None]) -> None:
        self.handlers[kind].append(handler)

    def publish(self, event: Event) -> None:
        for handler in (*self.handlers.get(event.kind, ()), *self.handlers.get("*", ())):
            handler(event)


class SpatialIndex:
    def __init__(self, world: WorldState):
        self.world = world
        self.positions: dict[Location, set[int]] = defaultdict(set)
        self.rebuild()

    def rebuild(self) -> None:
        self.positions.clear()
        for character in self.world.characters.values():
            if character.alive:
                self.positions[character.position].add(character.id)

    def move(self, entity_id: int, old: Location, new: Location) -> None:
        group = self.positions.get(old)
        if group is not None:
            group.discard(entity_id)
            if not group:
                self.positions.pop(old, None)
        self.positions[new].add(entity_id)

    def at(self, location: Location) -> list[int]:
        return sorted(self.positions.get(location, ()))


class EventRecorder:
    def __init__(self, world: WorldState, bus: EventBus, spatial: SpatialIndex):
        self.world, self.bus, self.spatial = world, bus, spatial
        from .observability import HistoricalObserver
        self.observer=HistoricalObserver(world)

    def emit(self, kind: str, description: str, actor_id: int | None = None,
             target_id: int | None = None, location: Location | None = None,
             historical: bool = False, witnesses: list[int] | None = None,
             context: dict | None = None, parent_event_ids=()) -> Event:
        observers = set(witnesses if witnesses is not None else
                        self.spatial.at(location) if location else ())
        # Participantes conhecem a própria ação. A posse de uma facção não
        # dá aos seus membros conhecimento automático sobre um evento.
        for entity_id in (actor_id, target_id):
            if entity_id in self.world.characters:
                observers.add(entity_id)
        event = Event(self.world.allocate_id(), kind, self.world.turn, description,
                      actor_id, target_id, location, sorted(observers), historical, context or {})
        self.world.events.append(event)
        del self.world.events[:-256]
        if historical:
            self.world.history.append(event)
        self.world.metrics[kind] = self.world.metrics.get(kind, 0) + 1
        self.observer.on_event(event,parent_event_ids)
        self.bus.publish(event)
        return event
