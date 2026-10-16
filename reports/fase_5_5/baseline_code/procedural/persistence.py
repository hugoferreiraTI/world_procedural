"""Adaptador JSON versionado, com escrita atômica e sem execução de código."""

from dataclasses import fields, is_dataclass
import json
import os
from pathlib import Path
import tempfile
from typing import Protocol

from . import RULES_VERSION, models
from .validation import assert_valid

FORMAT_VERSION = 1
TYPES = {name: value for name, value in vars(models).items()
         if isinstance(value, type) and is_dataclass(value)}


def encode(value):
    if is_dataclass(value):
        return {"$type": type(value).__name__,
                "fields": {field.name: encode(getattr(value, field.name)) for field in fields(value)}}
    if isinstance(value, dict):
        return {"$dict": [[encode(key), encode(item)] for key, item in value.items()]}
    if isinstance(value, tuple):
        return {"$tuple": [encode(item) for item in value]}
    if isinstance(value, list):
        return [encode(item) for item in value]
    return value


def decode(value):
    if isinstance(value, list):
        return [decode(item) for item in value]
    if isinstance(value, dict):
        if "$type" in value:
            kind = TYPES.get(value["$type"])
            if kind is None:
                raise ValueError("Tipo desconhecido no save.")
            return kind(**{key: decode(item) for key, item in value["fields"].items()})
        if "$dict" in value:
            return {decode(key): decode(item) for key, item in value["$dict"]}
        if "$tuple" in value:
            return tuple(decode(item) for item in value["$tuple"])
        raise ValueError("Estrutura desconhecida no save.")
    return value


def dumps(world: models.WorldState) -> str:
    return json.dumps({"format_version": FORMAT_VERSION, "rules_version": RULES_VERSION,
                       "world": encode(world)}, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False)


def loads(text: str) -> models.WorldState:
    try:
        document = json.loads(text)
        if document["format_version"] != FORMAT_VERSION or document["rules_version"] != RULES_VERSION:
            raise ValueError("Save incompatível com esta versão do motor.")
        world = decode(document["world"])
        if not isinstance(world, models.WorldState) or world.rules_version != RULES_VERSION:
            raise ValueError("Save não contém um mundo compatível.")
        assert_valid(world)
        # Valida também a restauração da aleatoriedade antes de substituir a campanha.
        import random
        random.Random(0).setstate(world.rng_state)
        return world
    except (KeyError, TypeError, AttributeError, IndexError, OverflowError, RecursionError) as error:
        raise ValueError("Save contém dados inválidos.") from error


class WorldRepository(Protocol):
    def save(self, world: models.WorldState, path: str | Path) -> None: ...
    def load(self, path: str | Path) -> models.WorldState: ...


class JsonRepository:
    def save(self, world: models.WorldState, path: str | Path) -> None:
        assert_valid(world)
        destination = Path(path).expanduser().resolve()
        temporary = None
        try:
            with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=destination.parent,
                                             suffix=".tmp", delete=False) as stream:
                temporary = stream.name
                stream.write(dumps(world))
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(temporary, destination)
        finally:
            if temporary and os.path.exists(temporary):
                os.unlink(temporary)

    def load(self, path: str | Path) -> models.WorldState:
        return loads(Path(path).expanduser().read_text(encoding="utf-8"))
