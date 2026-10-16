"""Consolida os replays de fome em evidências e relatório legível."""
from collections import Counter
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'reports/diagnostico_fome'
MODES = ('jogador', 'espectador', 'mundo')


def main():
    summaries = {m: json.loads((OUT/m/'resumo.json').read_text()) for m in MODES}
    cases = [(m, json.loads(line)) for m in MODES
             for line in (OUT/m/'casos.jsonl').read_text().splitlines()]
    hungry = [(m, c) for m, c in cases if c['record']['cause'] in ('hunger', 'both')]
    partition = Counter('inventario_com_comida' if c['record']['food'] else
                        'sem_comida_propria_mercado_com_comida' if c['at_death']['town_food'] else
                        'sem_comida_propria_mercado_vazio' for m, c in hungry)
    before_partition = Counter(
        'inventario_com_comida' if (s := c['last_decision']['before'])['food'] else
        'mercado_vazio' if not s['town_food'] else
        'dinheiro_insuficiente' if s['money'] < s['town_price'] else
        'fora_do_mercado' if s['distance_market'] else
        'mercado_com_comida_e_dinheiro_suficiente' for m, c in hungry)
    accessible = [(m, c) for m, c in hungry
                  if (s := c['last_decision']['before'])['food'] == 0
                  and s['town_food'] > 0 and s['money'] >= s['town_price']
                  and s['distance_market'] == 0]
    work = [c for m, c in hungry if c['last_decision']['selected'] == 'work']
    counters = Counter()
    for s in summaries.values():
        counters.update(s['counters'])
    core_hash = hashlib.sha256(b''.join(p.read_bytes() for p in sorted((ROOT/'procedural').glob('*.py')))).hexdigest()
    manifest = json.loads((ROOT/'reports/fase_3/manifesto_auditoria.json').read_text())
    assert core_hash == manifest['core_sha256'], 'O motor mudou desde as campanhas auditadas.'
    assert all(s['replay_identical'] for s in summaries.values())
    assert len(cases) == 690 and len(hungry) == 687
    assert partition == {'inventario_com_comida': 108,
                         'sem_comida_propria_mercado_com_comida': 319,
                         'sem_comida_propria_mercado_vazio': 260}
    assert all(c['last_decision']['need'] == 'food' for c in work)
    aggregate = {
        'scope': '3 campanhas canônicas da Fase 3, 10000 turnos cada; apenas mortes de NPCs',
        'deaths': len(cases), 'hunger_or_both': len(hungry),
        'causes': dict(Counter(c['record']['cause'] for m, c in cases)),
        'death_partition': dict(partition), 'last_decision_before_partition': dict(before_partition),
        'food_in_home_market_at_death': sum(s['hunger_with_food_in_home_market'] for s in summaries.values()),
        'food_acquired_in_final_decision': sum(s['food_acquired_in_final_decision'] for s in summaries.values()),
        'food_already_present_before_final_decision': sum(s['food_already_present_before_final_decision'] for s in summaries.values()),
        'fresh_acquisition_actions': dict(Counter(c['last_decision']['selected'] for m, c in hungry
                                                if c['record']['food'] and not c['last_decision']['before']['food'])),
        'terminal_choices': dict(Counter(c['last_decision']['selected'] for m, c in hungry)),
        'work_terminal_need': dict(Counter(c['last_decision']['need'] for c in work)),
        'work_terminal_execution': dict(Counter('travel' if not c['last_decision'].get('execution') else
                                               'success' if c['last_decision']['execution']['success'] else 'failure'
                                               for c in work)),
        'accessible_before_terminal_choices': dict(Counter(c['last_decision']['selected'] for m, c in accessible)),
        'critical_decisions_with_food': counters['critical_decisions_with_food'],
        'critical_decisions_with_food_selected_eat': counters['critical_with_food_selected:eat'],
        'critical_decisions_with_food_eat_percent': 100*counters['critical_with_food_selected:eat']/counters['critical_decisions_with_food'],
        'core_sha256': core_hash, 'core_unchanged': True,
        'replays': {m: {'identical': s['replay_identical'], 'save_sha256': s['save_sha256']} for m, s in summaries.items()},
    }
    (OUT/'RESUMO_GERAL.json').write_text(json.dumps(aggregate, ensure_ascii=False, indent=2)+'\n')
    selected_ids = {('mundo', 573), ('espectador', 1455), ('jogador', 260), ('jogador', 912), ('jogador', 127)}
    examples = [{'mode': m, **c} for m, c in cases if (m, c['id']) in selected_ids]
    (OUT/'EXEMPLOS_REAIS.json').write_text(json.dumps(examples, ensure_ascii=False, indent=2)+'\n')
    report = REPORT.replace('{{ROOT}}', str(ROOT))
    (ROOT/'RELATORIO_FOME_E_MORTES.md').write_text(report, encoding='utf-8')
    print(json.dumps({'report': str(ROOT/'RELATORIO_FOME_E_MORTES.md'),
                      'deaths': len(cases), 'core_unchanged': True,
                      'replays_identical': True}, ensure_ascii=False))


REPORT = """# Relatório — fome e mortes na Fase 3

Data: 7 de outubro de 2026. Versão analisada: `mvp-4`, após as correções registradas na auditoria canônica da Fase 3.

## 1. Resposta direta à suspeita

**O sistema verifica a fome, sim. A quantidade de comida guardada não substitui essa verificação.** A fome cria a necessidade de alimentação; o inventário determina se o personagem pode comer imediatamente ou precisa obter alimento primeiro.

O problema está na passagem entre **sentir fome → conseguir comida → efetivamente comer**. Comprar, coletar, receber comida como pagamento e comer são ações separadas. A fisiologia continua retirando vida entre elas. O planejamento também pode preservar uma viagem, resolver um empate em favor do descanso ou preparar água sem considerar que a fome matará antes.

A reprodução das três campanhas mostrou:

- **687 das 690 mortes de NPCs ocorreram com fome no limite**, incluindo sete com sede também no limite.
- **402 dessas 687 mortes aconteceram com comida no estoque da própria cidade.** Portanto, a impressão de que existe alimento enquanto pessoas morrem tem fundamento.
- **108 mortos carregavam comida. Em 107 deles, ela entrou no inventário na última decisão; o NPC morreu no fechamento daquela hora, antes de poder escolher comer.** Apenas um já carregava comida antes da decisão fatal.
- Nas **273.082 decisões com fome ≥ 85 e comida já no inventário**, o motor escolheu `eat` **273.042 vezes: 99,985%**. Isso mede decisões, não pessoas ou mortes.

O diagnóstico central é uma combinação de **acesso ao alimento, aquisição tardia e decisões sem avaliação suficiente do risco imediato de morte**. Uma simples verificação adicional de estoque não resolveria esses três problemas.

## 2. O que foi analisado e como conferir

Reproduzi as três campanhas originais de 10.000 turnos cada: jogador, espectador e mundo. Mantive as sementes e, no modo jogador, executei novamente os mesmos comandos registrados. Acrescentei observação de vida, fome, inventário, dinheiro, estoque local, ação escolhida e resultado, antes e depois das decisões e da fisiologia.

**Os três estados finais reproduzidos possuem exatamente o mesmo SHA-256 dos saves originais. Os registros de morte também coincidem integralmente.** A observação não mudou os resultados. Os 690 casos são ocorrências somadas entre campanhas; não representam 690 personagens distintos de um único mundo.

O código do motor permanece idêntico ao manifesto da Fase 3. Foram acrescentados somente scripts e arquivos de diagnóstico. Cinco verificações controladas complementam os casos reais e estão identificadas como cenários preparados, sem entrar nas estatísticas das campanhas.

Arquivos para conferência:

- [Resumo numérico consolidado](<{{ROOT}}/reports/diagnostico_fome/RESUMO_GERAL.json>).
- [Histórico dos cinco exemplos reais citados](<{{ROOT}}/reports/diagnostico_fome/EXEMPLOS_REAIS.json>).
- [Resultados das verificações controladas](<{{ROOT}}/reports/diagnostico_fome/microverificacoes.json>).
- [Casos completos: jogador](<{{ROOT}}/reports/diagnostico_fome/jogador/casos.jsonl>), [espectador](<{{ROOT}}/reports/diagnostico_fome/espectador/casos.jsonl>) e [mundo](<{{ROOT}}/reports/diagnostico_fome/mundo/casos.jsonl>). Cada linha é um caso, com até 64 registros recentes.
- [Script da reprodução](<{{ROOT}}/experiments/hunger_diagnosis.py>), [verificações controladas](<{{ROOT}}/experiments/hunger_microchecks.py>) e [consolidação deste relatório](<{{ROOT}}/experiments/hunger_report.py>).

## 3. Quanto a fome representa nas mortes

| Campanha | Mortes totais | Fome sem sede no limite | Fome e sede no limite | Sede sem fome no limite | Mortos com comida própria |
|---|---:|---:|---:|---:|---:|
| Jogador | 221 | 216 | 3 | 2 | 38 |
| Espectador | 258 | 257 | 1 | 0 | 39 |
| Mundo | 211 | 207 | 3 | 1 | 31 |
| **Total** | **690** | **680** | **7** | **3** | **108** |

Nestes testes, são **98,55% de mortes classificadas como fome sem sede no limite**, ou **99,57% contando os casos mistos**. A proporção é maior que os 90% mencionados na pergunta.

Os aproximadamente 89–90% apresentados anteriormente como seleção fisiológica mediam escolhas de **comida, água e descanso somadas**. Essa métrica não é a porcentagem de mortes por fome.

Há um limite na classificação: o registro usa fome e sede no momento da morte. Ele não reconstrói qual delas causou cada ponto de dano ao longo de toda a vida. Assim, “fome” significa fome em 100 na morte e sede abaixo de 100; não garante ausência de dano anterior por sede. A regra está em [classificação das mortes](<{{ROOT}}/procedural/engine.py:119>).

## 4. Como a fome e o consumo funcionam

Um turno corresponde a uma hora. A ordem relevante é:

1. O NPC que tem uma decisão agendada observa o ambiente e atualiza suas necessidades.
2. Fome **≥ 25** cria ou mantém a necessidade `food`.
3. O motor escolhe uma necessidade, depois uma solução para ela.
4. O personagem caminha ou executa a ação escolhida.
5. A hora fecha: a fome aumenta **2 pontos**, a sede aumenta e o cansaço também.
6. Se fome ou sede chegou a **100**, há dano. Se a vida chegou a zero, a morte é registrada.

Veja a [criação da necessidade de fome](<{{ROOT}}/procedural/needs.py:104>) e a [ordem das decisões e da fisiologia](<{{ROOT}}/procedural/engine.py:73>).

Quando `food` é a necessidade avaliada, possuir uma ração inclui `eat` entre as soluções. Essa ação tem pontuação base **200**, superior às bases de comprar, coletar e trabalhar. Comer consome uma ração e reduz a fome em **40 pontos**, mas não recupera vida. Com fome 100, uma refeição leva a 60; no fechamento da hora, a fome fica em 62. A execução está em [consumo de comida](<{{ROOT}}/procedural/goals.py:259>).

**Comprar não reduz a fome. Coletar não reduz a fome. Receber uma ração não reduz a fome.** Essas ações colocam um item no inventário; só `eat` o transforma em redução da necessidade. Uma ação de aquisição bem-sucedida pode, portanto, ser seguida de morte.

Os NPCs comuns normalmente decidem a cada seis horas; importantes a cada três; lendários e personagens próximos ao jogador a cada hora. Contudo, **fome ou sede ≥ 85 força decisões de hora em hora**. Não encontrei evidência de que as mortes com fome 100 sejam causadas por continuar esperando seis horas para pensar.

## 5. Por que conseguir comida pode não salvar

O dano começa quando fome ou sede alcança 100. Ele aumenta conforme o contador de horas consecutivas nessa condição:

| Horas consecutivas no limite | Dano por hora |
|---|---:|
| 1 a 11 | 2 |
| 12 a 23 | 3 |
| 24 a 35 | 4 |
| 36 a 47 | 5 |
| 48 em diante | 6 |

O contador é compartilhado pela privação de comida/água. Descansar não recupera vida quando o maior valor entre fome e sede está acima de 80. Comer elimina o dano daquela fome imediata se a sede também estiver abaixo do limite, mas deixa o personagem com a vida já perdida. Fontes: [fisiologia e descanso](<{{ROOT}}/procedural/needs.py:73>) e [parâmetros de sobrevivência](<{{ROOT}}/procedural/rules.py:7>).

Nos **107 casos de aquisição na última decisão**, os personagens tinham apenas **1 a 3 pontos de vida**: 37 tinham 1; 60 tinham 2; dez tinham 3. Eles conseguiram alimento, mas não consumiram antes do próximo dano.

As aquisições fatais foram: **52 compras, 33 coletas, dez trabalhos pagos em comida, sete roubos e cinco serviços temporários pagos em comida**. Não se trata somente de um erro da compra: a separação entre adquirir e consumir aparece em diferentes caminhos.

### Caso real: Arthus Arven, caçador, modo mundo

NPC 573, morto no turno **163**. Já estava tentando chegar ao mercado, com fome 100 e 14 moedas.

| Momento | O que aconteceu | Vida | Fome | Comida própria |
|---|---|---:|---:|---:|
| Decisão 159 | Continua o deslocamento para comprar | 10 | 100 | 0 |
| Fechamento 160 | Sofre dano | 8 | 100 | 0 |
| Fechamento 161 | Sofre dano | 5 | 100 | 0 |
| Fechamento 162 | Sofre dano | 2 | 100 | 0 |
| Decisão 162 | Compra uma ração por 14 moedas; havia seis no mercado | 2 | 100 | 1 |
| Fechamento 163 | Sofre três pontos de dano e morre | 0 | 100 | 1 |

O motor reconheceu a fome e a compra funcionou. **Faltou tempo para a ação seguinte de comer.** A comida encontrada no cadáver não estava sendo ignorada havia muitos turnos: tinha acabado de ser comprada.

Outro exemplo: **Marie Ferros**, NPC 912, modo jogador, recebeu uma ração por trabalho no turno 173, com vida 2 e fome 100. Morreu no fechamento 174, sem conseguir consumi-la.

## 6. Onde estava a comida quando eles morreram

“Tem comida” pode significar estoque de outra cidade, estoque da cidade local ou item pertencente ao NPC. Esses estados têm consequências diferentes.

Entre as **687 mortes com fome**, a divisão sem sobreposição no instante da morte é:

| Situação | Casos | Parcela |
|---|---:|---:|
| NPC carregava comida | 108 | 15,72% |
| NPC não carregava comida, mas sua cidade tinha rações | 319 | 46,43% |
| NPC não carregava comida e sua cidade estava sem rações | 260 | 37,85% |
| **Total** | **687** | **100%** |

Contando também os mortos com alimento próprio, **402 mortes tinham rações disponíveis no estoque da cidade: 58,52%**. Essa contagem se sobrepõe à primeira linha e não deve ser somada à tabela.

Em todos os 687 casos havia rações em pelo menos alguma cidade do mundo. Isso confirma existência global, mas não demonstra acesso local a tempo. O NPC não recebe automaticamente alimentos de uma cidade distante.

Estoque municipal não é inventário pessoal. Comprar exige estar no mercado, haver estoque e ter dinheiro suficiente. Fora do mercado, o personagem usa conhecimento local e informações de preço com validade; não consulta automaticamente o estoque de todo o mundo. Roubar, pedir ajuda e coletar são caminhos próprios, com deslocamento, disposição social, personalidade e possíveis falhas. Consulte [viabilidade e execução de compra](<{{ROOT}}/procedural/economy.py:36>) e [soluções para a fome](<{{ROOT}}/procedural/goals.py:33>).

Grãos e reservas silvestres também não equivalem a uma refeição já disponível no bolso. Grãos precisam virar comida por produção; coleta precisa ocorrer no local conhecido. Encontrar grãos no estoque ao morrer não demonstra que o NPC poderia consumi-los diretamente.

### O estado anterior à última decisão esclarece mais

Antes da decisão final, e não depois de comprar ou receber salário, os 687 casos se distribuíam assim:

| Condição antes da decisão fatal | Casos |
|---|---:|
| Já possuía comida | 1 |
| Sem comida própria e mercado local vazio | 317 |
| Mercado tinha comida, mas dinheiro abaixo do preço atual | 237 |
| Mercado tinha comida e havia dinheiro, mas NPC estava fora dele | 76 |
| Estava no mercado, sem comida própria, com estoque e dinheiro suficiente | 56 |

Dos últimos **56**, **52 compraram** na própria decisão fatal. Dois fizeram serviço temporário, um treinou e um roubou. Ou seja: mesmo quando compra era imediatamente acessível, a aquisição ainda precisava ser seguida de consumo.

O estoque pode mudar entre essas medições, inclusive porque a última ação produz comida. Por isso, dizer “a cidade tinha comida na morte” não prova que ela tinha a mesma quantidade ao iniciar a decisão, nem durante toda a viagem anterior.

## 7. Por que trabalham quando estão morrendo de fome

**318 das 687 mortes com fome tiveram `work` como última escolha. Em todas as 318, a necessidade selecionada era `food`.** O NPC estava trabalhando como caminho para conseguir dinheiro e comprar alimento. Isso confirma detecção da fome, mas expõe um planejamento incompleto.

Em 234 desses casos, o trabalho foi executado com sucesso; em 83, o personagem ainda estava em deslocamento para trabalhar; em um, a execução falhou. Ganhar dinheiro sem obter e consumir alimento a tempo não impede o dano.

A disponibilidade de trabalho como solução considera insuficiência financeira conhecida. Sua pontuação favorece diligência e desconta distância, mas não calcula se há vida suficiente para **trabalhar → acumular dinheiro → comprar → comer**. Algumas alternativas avaliam risco, como treinamento, porém não existe um limite de sobrevivência comum a toda essa cadeia. Fontes: [trabalho como solução da fome](<{{ROOT}}/procedural/goals.py:54>), [insuficiência financeira conhecida](<{{ROOT}}/procedural/economy.py:185>) e [pontuação das ações](<{{ROOT}}/procedural/utility.py:6>).

### Caso real: Tomas Ferros, guarda, modo jogador

NPC 260, morto no turno **344**. Na decisão 343:

- Estava no mercado, que tinha **15 rações**; uma custava **7 moedas**.
- Tinha **5 moedas**, **vida 1**, **fome 100** e nenhuma ração própria.
- O motor selecionou a necessidade de comida, mas escolheu trabalhar: pontuação **97,5**, contra **73,1** para uma alternativa de pedir ajuda.
- Trabalhou, passou a ter seis moedas, continuou com fome 100 e morreu no fechamento da hora.

Havia alimento próximo, mas ele não podia comprar. **A solução escolhida nunca chegaria à refeição antes do dano fatal.** O caso não prova que um pedido de ajuda teria sido aceito; prova que o plano de trabalho escolhido não podia salvá-lo naquele prazo.

## 8. O caso em que já havia comida e o NPC não comeu

**Bela Valerius**, NPC 1455, conselheira no modo espectador, é o único dos 108 mortos com comida que já possuía uma ração antes da decisão fatal.

| Momento | O que aconteceu | Vida | Fome | Comida própria |
|---|---|---:|---:|---:|
| Decisão 240 | Coleta uma ração | 5 | 100 | 1 |
| Fechamento 241 | Sofre quatro pontos de dano | 1 | 100 | 1 |
| Decisão 241 | Descanso vence empate; preparação escolhe buscar água | 1 | 100 | 1 |
| Fechamento 242 | Morre com a ração e duas unidades de água | 0 | 100 | 1 |

A causa da escolha foi uma sequência específica:

1. Fome e descanso estavam com prioridade **100**, o teto comum às necessidades.
2. O desempate usa o menor identificador da necessidade. O descanso, ID 3155, era mais antigo que a fome, ID 3668, e venceu.
3. A solução de descanso levaria Bela para casa, a oito passos de distância.
4. A preparação da viagem verifica água antes de comida. Com sede 77 e uma fonte no local, escolheu `fill_water`.
5. Essa preparação não verificou se vida 1 e fome 100 tornavam fatal adiar a refeição.

**Aqui existe uma falha observada de prioridade e prevenção:** ela podia comer imediatamente, mas o motor executou outra ação. Comer teria reduzido a fome para 60 antes do dano; a sede também estava abaixo de 100 naquele fechamento.

A pontuação 200 de comer não corrigiu o empate porque as ações são comparadas **dentro da necessidade selecionada**. Primeiro venceu descanso; as soluções de comida ficaram fora daquela comparação. Fontes: [teto e desempate de prioridades](<{{ROOT}}/procedural/needs.py:159>), [seleção de necessidade](<{{ROOT}}/procedural/goals.py:134>) e [preparação com água antes de comida](<{{ROOT}}/procedural/goals.py:360>).

## 9. Continuidade de objetivos pode manter uma escolha pior

O motor preserva um objetivo ativo quando outra necessidade não supera sua prioridade por 12 pontos. Isso evita abandonar viagens a toda hora. Porém, pode manter uma ação antiga mesmo quando aparece uma solução mais rápida dentro da própria necessidade.

Nas campanhas, **Iria Stone**, NPC 127, modo jogador, tinha vida 2, fome 100, oito moedas e estava num mercado com cinco rações a seis moedas. Comprar tinha pontuação **85,6**, mas ela continuou o serviço temporário anterior, cuja pontuação atual era **63,85**. Recebeu uma ração como pagamento e morreu no fechamento 226, antes de comer. Esse é um caso real de continuidade mantendo uma alternativa inferior; tanto comprar quanto receber a ração ainda exigiriam resolver a etapa do consumo.

Uma verificação controlada demonstrou uma falha mais direta: um NPC com comida própria, fome 100 e vida 2 manteve a viagem para comprar, embora `eat` tivesse pontuação 200. Caminhou e morreu com a ração. **Esse segundo cenário foi preparado para testar a regra; não apareceu como causa das mortes com comida já presente nas três campanhas.** Não deve ser contado como frequência espontânea.

O risco está na [preservação do objetivo ativo](<{{ROOT}}/procedural/goals.py:154>). Além disso, chegar ao destino consumindo a última hora de deslocamento adia a execução para a próxima decisão, criando mais uma etapa que o plano precisa considerar.

## 10. Verificações controladas realizadas

Preparei cinco estados pequenos e executei o motor atual, sem modificar suas regras. Todos passaram pelas verificações esperadas e pela validação do mundo.

| Cenário preparado | Resultado |
|---|---|
| Fome 0, uma ração guardada | Não come; estoque sozinho não cria fome |
| Fome 100, vida 2, uma ração, sem conflitos | Come, termina com fome 62 e sobrevive |
| Fome 100, vida 2, dinheiro e mercado abastecido, sem ração própria | Compra e morre antes de comer |
| Fome 100, vida 2, uma ração, descanso mais antigo também com prioridade 100 | Descansa, não recupera vida em privação crítica e morre com comida |
| Fome 100, vida 2, uma ração, viagem de compra ativa | Continua a viagem e morre com comida |

Os cenários confirmam mecanismos do código. Os números das mortes vêm exclusivamente dos replays, sem acrescentar essas mortes artificiais.

Há ainda uma sutileza no registro: a morte marca o objetivo atual como `failed`, mesmo se a aquisição acabara de ser bem-sucedida. Para avaliar esses casos, usei o resultado da execução antes da morte; o estado final do objetivo, sozinho, poderia sugerir incorretamente que a compra falhou.

## 11. O que precisa ser corrigido primeiro

As propostas abaixo são recomendações para uma implementação posterior. **Este trabalho não alterou as regras do jogo.**

| Prioridade | Mudança sugerida | Motivo e efeito esperado |
|---|---|---|
| 1 | Comparar ameaça imediata à vida ao desempatar necessidades e preparar viagens | Evita descanso ou busca preventiva de água vencerem uma refeição necessária para sobreviver à próxima hora; caso Bela confirma a necessidade |
| 1 | Permitir interromper objetivo ativo para consumir uma reserva que evita morte imediata | Mantém continuidade em situações normais e elimina o risco demonstrado de continuar comprando com comida no bolso |
| 1 | Planejar aquisição e consumo com tempo explícito | As 107 aquisições fatais mostram que obter uma ração não é concluir alimentação; o plano deve reservar tempo para comer ou definir uma refeição imediata no local |
| 2 | Avaliar prazo da cadeia de renda, compra e consumo | Impede escolher horas de trabalho incompatíveis com a vida restante; ajuda a separar plano possível de plano economicamente correto, porém tarde demais |
| 2 | Planejar reposição de reserva pessoal antes da emergência | Comprar uma unidade somente após surgir fome deixa pouco espaço para viagem, mudança de preço ou falta temporária de estoque |
| 2 | Reavaliar alternativas locais de ajuda, pagamento em refeição e acesso de emergência | Comida municipal existente não é acesso pessoal garantido; precisa haver uma ação viável e disponível para quem não pode pagar |
| 3 | Medir a demanda real por refeições antes de ajustar produção e população abstrata | Mais produção pode aliviar estoques vazios, mas não resolve sozinha os erros de tempo, consumo e prioridade |

Para o terceiro ponto, há uma escolha de desenho: manter aquisição e consumo como ações separadas com planejamento antecipado, ou introduzir uma ação explícita de comprar/receber **uma refeição consumida no local**. A segunda opção deve debitar uma ração real e respeitar tempo e disponibilidade. Não basta reduzir fome ao comprar qualquer reserva, porque comprar para guardar também é um comportamento válido.

Uma hipótese adicional merece medição: o diagnóstico econômico estima **1,2 ração por NPC por dia**, compatível com 40 pontos por ração e aumento de 48 pontos de fome por dia. Entretanto, comer logo em 26 reduz para zero e usa somente 26 dos 40 pontos possíveis. Num cenário ideal de decisões a cada hora, comida abundante e consumo sempre nesse limiar, isso equivale a aproximadamente **1,85 ração/dia**. É uma divergência potencial de dimensionamento, não uma medição da média destas campanhas nem uma causa já quantificada para as 687 mortes. Deve-se medir consumo efetivo antes de recalibrar demanda ou mudar o limiar. A estimativa administrativa está em [diagnóstico alimentar](<{{ROOT}}/procedural/economy.py:111>).

Para validar futuras correções, os indicadores úteis são: mortes com alimento adquirido na última decisão, mortes com alimento já presente e não consumido, escolhas que não cabem no tempo de vida restante, duração entre aquisição e refeição e sobrevivência durante falta temporária de estoque. O objetivo deve ser reduzir mortes evitáveis preservando consequências reais de pobreza e escassez.

## 12. Limites desta análise

Os resultados mostram o comportamento destas três campanhas e cinco verificações controladas; não são uma estimativa universal para qualquer semente. Os estados locais de estoque são observados pelo diagnóstico, não concedidos como conhecimento automático ao personagem. Dinheiro e estoque na morte podem ter mudado desde a última escolha. As pontuações registradas são alternativas da necessidade selecionada, não de todas as necessidades comparadas juntas.

Não atribuí todas as 687 mortes a um único defeito. **107 casos demonstram aquisição tardia sem tempo para consumo; um demonstra desvio fatal apesar de comida já disponível no inventário; muitos outros mostram ausência de estoque próprio, barreiras financeiras e deslocamento.** As campanhas não foram rerrodadas com correções, portanto ainda não há uma porcentagem comprovada de mortes que cada mudança eliminaria.
"""


if __name__ == '__main__':
    main()
