"""Apresentação textual: encaminha ações ao motor sem implementar regras."""

import json
import os
import shlex

from .engine import Engine
from .persistence import JsonRepository

STATUS_NAMES = {"active": "ativa", "selected": "priorizada", "blocked": "bloqueada",
                "inactive": "inativa", "satisfied": "satisfeita", "failed": "falhou",
                "expired": "expirada", "offered": "oferecido", "accepted": "aceito",
                "declined": "recusado", "completed": "concluído",
                "resolved_elsewhere": "resolvido pelo mundo"}
NEED_NAMES = {"food": "comida", "water": "água", "rest": "descanso", "money": "dinheiro",
              "food_reserve": "reserva alimentar",
              "work": "trabalho", "security": "segurança", "family": "família", "grief": "luto",
              "revenge": "reparação/vingança", "protection": "proteção", "status": "reconhecimento",
              "advancement": "ascensão", "response":"resposta", "pursuit":"perseguição",
              "healing":"recuperação", "assistance":"auxílio", "migration":"mudança", "despair":"desespero"}
NEED_NAMES['recovery'] = 'recuperação física'
NEED_NAMES.update(political_pressure='pressão política',organizational_survival='organização',
                  governance='governo local',military_service='comando militar',
                  religious_interest='fé pessoal',power='desenvolvimento de poder')

HELP = """Ações (uma hora cada):
  mover norte|sul|leste|oeste       ou digite somente a direção
  entrar / sair                   sair requer estar em um portão G
  esperar [horas]                  de 1 a 1000
  conversar NPC_ID
  aceitar QUEST_ID / recusar QUEST_ID
  entregar NPC_ID ITEM_ID [quantidade]
  comprar comida|agua|trigo|ferro|madeira|arma [quantidade]
  vender ITEM_ID [quantidade]
  comer / beber / descansar
  refeicao                        comprar e consumir uma ração no mercado
  coletar                         na área rural A
  trabalhar                       trabalho avulso em A, pago com comida
  pedir comida NPC_ID              depende de confiança e disposição
  investigar NPC_ID                localizar pessoa/restos presentes e registrar o fato
  informar NPC_ID FACT_ID          transmitir uma informação conhecida
  acompanhar NPC_ID                companhia/proteção solicitada no encontro
  atacar NPC_ID / defender / fugir / render / recuar
  confrontar NPC_ID / ameacar NPC_ID / cobrar NPC_ID / avisar NPC_ID
  insultar NPC_ID / desculpar NPC_ID / acalmar NPC_ID / perdoar NPC_ID
  socorrer NPC_ID                    usa água e provisão reais; ajuda limitada
  capturar NPC_ID                    exige autoridade, prova e rendição/incapacidade
  orar SUJEITO_ID / ofertar SUJEITO_ID
  difundir_fe SUJEITO_ID / reavaliar_fe SUJEITO_ID
  treinar_poder / reivindicar_essencia DEUS_ID
  compartilhar_problema / organizar
  aderir_grupo GRUPO_ID / reunir_grupo GRUPO_ID
  apresentar_proposta PROPOSTA_ID / contar_historia_item ITEM_ID

Consultas: listar, mapa, status, inventario, necessidades, mercado, eventos, fatos, quests
           grupos, organizacoes, crencas, renome, cargos (na administração local)
Campanha: salvar [arquivo.json], carregar [arquivo.json], encerrar
Legenda: @ você, F floresta, D deserto, S pântano, C cidade, V vila, ? interior,
         # muralha, G portão, M mercado, H casas, W oficinas, A área rural.
As consultas não consomem turnos. NPCs presentes são identificados por ID.
"""


def render(engine: Engine) -> str:
    view = engine.view()
    if "map" not in view:
        return f"Seed {view['seed']} | Turno {view['turn']}"
    x, y = view["position"]
    left = [f"{view['name']} — {view['nickname']}",
            f"Vida {view['health']}/100 | Moedas {view['money']}",
            f"Fome {view['hunger']} | Sede {view['thirst']} | Cansaço {view['fatigue']}",
            f"Dia {view['day']} | {view['hour']:02d}:00 | Turno {view['turn']}",
            f"{view['map_name']} | ({x}, {y})", view["place"]]
    right = ["MAPA 5×5"] + [" ".join(row) for row in view["map"]]
    width = 58
    lines = ["┌" + "─" * width + "┬" + "─" * 15 + "┐"]
    for info, row in zip(left, right):
        lines.append("│ " + info[:width - 2].ljust(width - 2) + " │ " + row.ljust(13) + " │")
    lines.append("├" + "─" * width + "┴" + "─" * 15 + "┤")
    details = []
    if view["structures"]:
        details.append("Estruturas: " + ", ".join(view["structures"]))
    details.extend(f"NPC #{npc['id']}: {npc['name']} ({npc['profession'] or 'sem profissão'})" for npc in view["npcs"])
    details.extend(f"Restos #{body['id']}: {body['name']} — investigar ID" for body in view.get("bodies", []))
    if not view["npcs"]:
        details.append("Nenhum NPC nesta posição.")
    details.extend(view["events"][-2:])
    if not view["alive"]:
        details.append("PERSONAGEM MORTO — carregar campanha.json ou encerrar")
    for detail in details:
        # Quebra apenas texto de apresentação; não determina estado do mundo.
        for offset in range(0, len(detail), 72):
            lines.append("│ " + detail[offset:offset + 72].ljust(72) + " │")
    lines.append("├" + "─" * 74 + "┤")
    lines.append("│ mover · entrar · listar · conversar ID · inventario · ajuda".ljust(75) + "│")
    lines.append("└" + "─" * 74 + "┘")
    return "\n".join(lines)


def run_terminal(engine: Engine, repository=None) -> None:
    repository = repository or JsonRepository()
    print("MUNDO PROCEDURAL | Seed: " + engine.world.seed)
    print("Digite ajuda para conhecer os comandos.")
    while True:
        print(render(engine))
        try:
            line = input("> ")
        except (EOFError, KeyboardInterrupt):
            print("\nCampanha encerrada.")
            return
        try:
            tokens = shlex.split(line)
            if not tokens:
                continue
            command = tokens[0].lower()
            if command in ("encerrar", "exit", "quit"):
                return
            if command == "ajuda":
                print(HELP)
                continue
            if command in ("salvar", "carregar"):
                if len(tokens) > 2:
                    print("Coloque caminhos com espaços entre aspas.")
                    continue
                path = tokens[1] if len(tokens) == 2 else "campanha.json"
                if command == "salvar":
                    engine.world.rng_state = engine.rng.getstate()
                    repository.save(engine.world, path)
                    print(f"Campanha salva em {os.path.abspath(path)}")
                else:
                    loaded = repository.load(path)
                    engine = Engine(loaded)
                    print("Campanha carregada.")
                continue
            result = engine.execute(line)
            print(result.message)
            if result.data is not None and command not in ("listar", "status", "mapa"):
                if isinstance(result.data, list):
                    for entry in result.data:
                        if isinstance(entry, str):
                            print(entry)
                        elif command in ("inventario", "inventário"):
                            print(f"#{entry['id']} {entry['name']} ×{entry['quantity']} | {entry['rarity']} | qualidade {entry['quality']}")
                        elif command == "mercado":
                            print(f"{entry['product']}: {entry['quantity']} disponível(is) | compra {entry['price']} / venda {entry['sell_price']} moedas; lotes variam com estoque")
                        elif command == "quests":
                            print(f"#{entry['id']} {entry['title']} | {STATUS_NAMES.get(entry['status'], entry['status'])}")
                        elif command == "necessidades":
                            print(f"{NEED_NAMES.get(entry['type'],entry['type'])} | prioridade {entry['priority']} | {STATUS_NAMES.get(entry['status'],entry['status'])} | {entry['reason']}")
                        else:
                            print(" | ".join(f"{key}: {value}" for key, value in entry.items()))
                    if not result.data:
                        print("Nenhum registro.")
                else:
                    print(json.dumps(result.data, ensure_ascii=False, indent=2))
        except (OSError, ValueError) as error:
            print(f"Não foi possível concluir: {error}")
