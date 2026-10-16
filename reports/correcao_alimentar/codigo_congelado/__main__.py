"""python3 -m procedural: terminal jogável ou simulação sem jogador."""

import argparse
import json
import time

from .engine import Engine
from .generation import generate_world
from .persistence import JsonRepository
from .ui import run_terminal
from .validation import assert_valid


def main():
    parser = argparse.ArgumentParser(description="Mundo procedural por turnos, em português.")
    parser.add_argument("--seed", default="Dovha", help="Nome do personagem primordial")
    parser.add_argument("--nome", default="Viajante", help="Nome do jogador")
    parser.add_argument("--simular", type=int, metavar="TURNOS", help="Rodar sem jogador")
    parser.add_argument("--carregar", metavar="ARQUIVO", help="Carregar campanha JSON")
    parser.add_argument("--salvar", metavar="ARQUIVO", help="Salvar ao final de uma simulação")
    args = parser.parse_args()
    if args.simular is not None and args.simular < 0:
        parser.error("O número de turnos não pode ser negativo.")
    repository = JsonRepository()
    started = time.monotonic()
    try:
        world = (repository.load(args.carregar) if args.carregar else
                 generate_world(args.seed, args.nome, with_player=args.simular is None))
        engine = Engine(world)
        if args.simular is not None:
            engine.simulate(args.simular)
            assert_valid(world)
            if args.salvar:
                repository.save(world, args.salvar)
            print(json.dumps({"seed": world.seed, "turno": world.turn,
                              "turnos_simulados": args.simular,
                              "reinos": len(world.kingdoms), "cidades_e_vilas": len(world.towns),
                              "npcs": len(world.characters),
                              "npcs_vivos": sum(character.alive for character in world.characters.values()),
                              "itens": len(world.items), "acontecimentos_historicos": len(world.history),
                              "eventos": world.metrics, "invariantes": "válidas",
                              "tempo_segundos": round(time.monotonic() - started, 2)},
                             ensure_ascii=False, indent=2))
        else:
            run_terminal(engine, repository)
    except (ValueError, OSError) as error:
        parser.exit(1, f"Erro: {error}\n")


if __name__ == "__main__":
    main()
