"""Grafo dirigido: nomes nunca são usados como chaves."""

from .models import Relationship, WorldState


class RelationshipGraph:
    def __init__(self, world: WorldState):
        self.world = world

    @staticmethod
    def key(source: int, target: int, kind: str) -> str:
        return f"{source}:{target}:{kind}"

    def set(self, source: int, target: int, kind: str, value: int,
            reciprocal: bool = False) -> None:
        minimum = -100 if kind == "diplomacia" else 0
        value = max(minimum, min(100, value))
        self.world.relationships[self.key(source, target, kind)] = Relationship(
            source, target, kind, value)
        if reciprocal:
            self.set(target, source, kind, value)

    def value(self, source: int, target: int, kind: str, default: int = 0) -> int:
        relation = self.world.relationships.get(self.key(source, target, kind))
        return relation.value if relation else default

    def adjust(self, source: int, target: int, kind: str, amount: int) -> None:
        self.set(source, target, kind, self.value(source, target, kind) + amount)
