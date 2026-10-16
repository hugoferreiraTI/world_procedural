# Fase 4.6 — investigação ativa e escalada fatal

Versão `mvp-7-fase4.6`, seed `Corven-46`. Mundo novo em h 0, sem jogador nem save carregado, 1568 NPCs persistentes, 3926 habitantes abstratos e 66 localidades. Uma única campanha longa concluída de 5000 horas. Um início anterior foi interrompido durante o diagnóstico da reação imediata e não integra estas estatísticas. Núcleo congelado: `e3866d29db349cbfc963bc0a7cd0036e65b9577a0f7cb16707a2f4a787b43c96`.

## Resultado e respostas centrais

A investigação funciona naturalmente: 13792 verificações de áreas, 3744 consultas a pessoas, 845 respostas consideradas úteis, 3149 entradas em espera e 1545 reativações. Existem regressões de preservação da causa, retorno à vida diária e reativação sem ação automática.

Intenção letal natural: 23 mudanças para `kill` entre 12 NPCs, 0 mortes com essa intenção e 0 decisões de poupar após incapacidade letal. A capacidade técnica foi demonstrada em regressões controladas. A campanha não demonstrou emergência natural de homicídio deliberado; esse objetivo permanece empiricamente não comprovado nesta seed.

O gargalo demonstrado mudou: a opção letal foi elegível em 287 avaliações e venceu em 57 ataques, mas nenhum desses ataques levou a incapacidade letal. O julgamento após incapacidade não teve oportunidade natural de ocorrer. A próxima análise deve rastrear continuidade dos confrontos, encontros, retiradas, recuperação e interferência de outras Needs, mantendo o dano atual.

Quando a intenção é considerada, a decisão é explicável por autoria conhecida, dano/perda grave atribuída, grievance, compromisso e barreiras pessoais/situacionais. Pressão insuficiente não vira intenção letal por ruído de Utility. Intenção altera o desfecho desejado, mantendo o mesmo cálculo de dano.

Pista velha pode levar a verificação e pergunta; uma resposta conhecida pode produzir pista nova. Falta de informação pode suspender a busca sem esquecer sua origem. Esses dois avanços estão documentados em histórias reais, com IDs e horários.

## O que mudou

- `LethalPressure`: pré-condições semânticas e fatores/barreiras dirigidos a um alvo; episódios e tentativas de resolução compactos, sem contar golpes como conflitos distintos.
- Reações imediatas podem amadurecer em compromisso quando há dano próprio grave conhecido e reincidência/perigo sério. Novos danos atribuídos ao mesmo alvo podem aprofundar sua intensidade, sem contar isso como aproximação física.
- Evidências mistas conservam a confiança no fato grave atribuído; uma agressão certa não confirma um homicídio de autoria duvidosa. Perda pessoal importante comprovada pode justificar gravidade sem ataques anteriores do próprio vingador.
- Informante com conhecimento real de homicídio pode esclarecer autoria desconhecida, retargetando o mesmo compromisso e preservando a origem da vingança.
- Investigação geral para vingança, procura institucional e familiar desaparecido. Até três pistas por compromisso, fontes e áreas limitadas, confiança e idade preservadas, informantes locais sem conhecimento global.
- Dormência, reativação por informação útil, retorno físico à rotina, reconhecimento presencial de pessoa ou restos e prazo finito de intenção.
- Uma pista formal recente por caso; compartilhamento presencial no serviço local após seis horas. Tarefas de busca/vigilância/informação permanecem distintas; gravidade aumenta duração e limite de tentativas.
- Contexto de preparação nas necessidades canônicas e bônus limitado de quatro pontos na alternativa; progresso exige aumento real de provisões frente a déficit conhecido.
- Auditoria de decisões e pistas, sem efeitos de consultas de depuração sobre o save. Nenhuma nova mecânica da Fase 5.

O diagnóstico de cada componente e a justificativa da extensão estão em `reports/fase_4_6/DIAGNOSTICO_E_ALTERACOES.md`. A fórmula de potência e o bloco de dano são idênticos à base. Alimentação, recuperação, economia, profissões, geração, política, migração, navegação e população permanecem byte a byte iguais. Integrações em Needs/Goals/Knowledge/Agency/Justice são preservadas em `preservacao.json` e no código congelado.

## Validação

Foram acrescentadas 18 regressões compostas, totalizando 245 testes únicos. A suíte completa foi executada uma vez quando havia 243 testes: 240 passaram e três detectaram divergências de contadores por consultas/debug. Após o reparo, esses testes passaram. A extensão final de reação persistente foi validada em 59 testes direcionados: as 18 regressões novas, as 18 da Fase 4.5, os 20 de combate da Fase 4 e os três de determinismo. Não há falha pendente. Logs originais e retestes foram conservados.

A curta validada, com o mesmo hash da longa, completou 500 h: {'thirst': 2, 'hunger': 18, 'combat': 3}, 0 erros de integridade, 0 mortes alimentares com comida carregada. Execuções diagnósticas e interrompidas estão separadas; seus resultados não se misturam com esta campanha.

Na longa: 0 erros nas 50 verificações de estado; 1274 NPCs vivos ao final; causas de morte `{'thirst': 6, 'hunger': 260, 'combat': 17, 'both': 11}`. Mortes alimentares carregando comida: 0. O quadro de fome continua relevante e a fase não comprova sua resolução.

## Avaliação letal

| Contador | Ocorrências |
|---|---:|
| `Lethal:abandoned` | 10 |
| `Lethal:available` | 287 |
| `Lethal:blocked:authority_or_witnesses` | 50 |
| `Lethal:blocked:compassion` | 184440 |
| `Lethal:blocked:fear` | 57798 |
| `Lethal:blocked:insufficient_commitment` | 843734 |
| `Lethal:blocked:insufficient_pressure` | 948992 |
| `Lethal:blocked:low_confidence` | 801439 |
| `Lethal:blocked:nonlethal_better` | 187 |
| `Lethal:death` | 0 |
| `Lethal:evaluated` | 978266 |
| `Lethal:incapacity` | 0 |
| `Lethal:mercy` | 0 |
| `Lethal:precondition_failed` | 977979 |
| `Lethal:won` | 57 |

A categoria `low_confidence` inclui avaliações sem fato grave atribuído conhecido; não significa que todos esses NPCs acreditavam em um rumor de homicídio. `insufficient_pressure` também inclui ausência de causa grave semanticamente elegível.

O registro narrativo contém 56 eventos `LethalOptionConsidered`: ele evita repetir a mesma opção/alvo antes de 48 horas. Isso não equivale às 287 avaliações elegíveis. `won` conta ataques com intenção matar, não mudanças de intenção; as 23 mudanças envolveram 12 NPCs. As dez ocorrências de `abandoned` incluem seis encerramentos explícitos e quatro reavaliações para outra intenção.

Os contadores são avaliações e ações, não pessoas independentes. Uma decisão pode avaliar mais de uma Need; fatores de bloqueio podem coexistir. Avaliar em cada decisão e na execução permite reexaminar incapacidade, autoridade e novas informações sem efeitos de consultas/debug.

## Investigação e vida durante a espera

| Contador | Ocorrências |
|---|---:|
| `Investigation:area_searched` | 13792 |
| `Investigation:asked` | 3744 |
| `Investigation:dormant` | 3149 |
| `Investigation:found` | 503 |
| `Investigation:known_clue` | 156943 |
| `Investigation:new_clue` | 157165 |
| `Investigation:reactivated` | 1545 |
| `Investigation:remains_found` | 50 |
| `Investigation:rumor` | 222 |
| `Investigation:stale_clue` | 5961 |
| `Investigation:useful` | 845 |
| `Investigation:useless` | 2899 |

Pistas avaliadas: 157165; idade média 28.1 h, confiança média 99.7%. O auditor encontrou 1408 pistas cujo alvo já estava em outro mapa e 37263 com alvo em outra célula do mesmo mapa. Isso mede desatualização, sem provar mentira. A amostra detalhada contém as primeiras 4.096 pistas; os totais incluem todas.

Fontes das pistas: `{'direct': 156027, 'known': 907, 'rumor': 222, 'trusted': 9}`. Observações diretas de pessoas presentes também entram neste total; a confiança média de todas as pistas não mede apenas a qualidade das respostas de informantes. A categoria narrativa de renovação por consulta exige uma pista anterior com pelo menos 12 horas e uma informação mais recente fornecida por uma fonte real.

Pistas formalmente depositadas: 2386; retransmissões institucionais: 11327. Cada retransmissão depende da presença e da latência do canal, não é um comunicado global.

Ações reais bem-sucedidas enquanto havia compromisso em espera: `{'eat': 44849, 'sleep': 47390, 'drink_well': 10424, 'pursue': 3231, 'work': 28188, 'buy_food': 14184, 'steal': 7993, 'secure': 2176, 'drink': 30098, 'check_relative': 1454, 'fill_water': 15165, 'confront': 162, 'demand_return': 253, 'defend': 928, 'forage': 16611, 'denounce': 1400, 'stay_near': 253, 'migrate': 18318, 'flee': 652, 'steal_person': 1322, 'return_from_search': 3597, 'search_area': 1673, 'temporary_service': 2284, 'sell_surplus': 635, 'give_supplies': 577, 'work_for_food': 3339, 'calm': 27, 'apologize': 41, 'investigate': 196, 'ask_about_person': 422, 'avoid_threat': 202, 'attack': 2169, 'surrender': 120, 'forgive': 2, 'follow_lead': 3664, 'ask_personal_help': 151, 'withdraw': 43, 'ask_help': 125, 'threaten': 118, 'protect': 128, 'intervene': 23, 'watch_case': 77, 'alert': 1, 'insult': 72, 'warn': 14, 'buy_meal': 3, 'work_for_meal': 1, 'call_help': 9, 'seek_treatment': 153, 'remember_relative': 9, 'capture': 9, 'steal_meal': 12, 'forage_meal': 16, 'first_aid': 5, 'return_stolen': 1}`. Compromissos dormentes no fim: 215. Casos institucionais com mais de um guarda: 1226; máximo de guardas por caso: 3.

Amostras diárias de vingança forte: `{'distance_or_stale_lead': 3072, 'truce': 46, 'other_need': 796, 'utility_or_known_risk': 22, 'incapacity': 2, 'attack_selected': 1, 'solution_absent': 1}`. Amostras de reação grave persistente: `{'waiting_for_information': 23, 'distance_or_lead': 138, 'other_need': 12, 'attack_selected': 2, 'truce': 13, 'utility_or_semantic_barrier': 2}`. Uma amostra bloqueada por distância ou por outra Need não comprova falta de intenção. Ações durante a espera podem atender outros compromissos; um objetivo dormente não monopoliza a vida do NPC.

Cadeias causais estritas detectadas: 887. Exigem violência inicial, resposta de terceiro, nova violência e nova resposta por referências de fatos usados. Repetição de eventos ou mera proximidade temporal não basta.

## Qualidade narrativa e comparação

Foram adotados 91167 compromissos; 22579 tiveram progresso e 19154 mudaram de estratégia. Não são números de grandes sagas. Transformação de pista, suspensão, retomada, presença e consequência são critérios mais fortes que extensão do EventLog.

A longa anterior da Fase 4.5 teve 1776 NPCs, 365 mortes e nenhuma mudança natural para matar; esta teve 1568 NPCs e 294 mortes. Seeds e populações diferentes impedem atribuir a diferença numérica à versão. A longa da Fase 4.5 também usou um núcleo anterior aos cinco ajustes finais daquela entrega; esses reparos já integram a base preservada da Fase 4.6. O avanço verificável desta entrega é a investigação/dormência, sustentado também por regressões controladas.

## Estado, save e custo

Save da curta: 128.5 MiB; da longa: 1101.6 MiB. O volume cresceu 8.57× para horizonte 10× maior. Histórico: 1619772 eventos. O agregado de conflito e compromissos investigativos, incluindo campos preexistentes, ocupa aproximadamente 2.74 MiB serializado. Os limites de pares, pistas e fontes evitam crescimento sem limite por personagem; o histórico global continua volumoso.

Tempo de simulação/auditoria registrado: 67.1 min; pico de memória anterior à exportação do save: 2478.6 MiB. A exportação pode ter pico adicional e não está incluída nesse indicador. Save/load da própria versão e continuidade determinística passaram nas regressões. Saves de versões anteriores continuam sujeitos à checagem de versão já existente.

## Problemas e limites restantes

- Informação falsa deliberada não é produzida nesta fase; há rumor e informação antiga, que não devem ser rotulados como mentira comprovada.
- Novas observações rotineiras podem gerar muitas transições de pista e inflar a leitura de progresso. O relatório separa estas transições das consultas que renovaram uma informação antiga.
- Uma pista remota não fornece uma rota desconhecida. Falta de rota, recursos, oportunidade ou coragem pode impedir a viagem.
- O registro institucional depende de conhecimento, presença e canais locais. Homicídio conhecido aumenta gravidade, sem garantir captura.
- A intensidade de muitos conflitos permanece insuficiente para homicídio. Denúncias e afastamentos podem encerrar necessidades antigas antes de uma escalada mais profunda; são desfechos válidos, mas limitam sagas violentas.
- Mortes por combate com intenção de ferir/repelir podem atingir pessoas já muito debilitadas por privação. São consequências físicas fatais, sem prova de decisão deliberada de matar.
- Fome, cuidado familiar por privação e despesas individuais ainda dominam parte das histórias. Preservar o módulo alimentar não garante os mesmos resultados quando outros objetivos disputam tempo.
- O save conserva a grande crônica preexistente. Esta entrega mede o custo e limita dados novos, mas não resolve toda a retenção histórica.

Antes de ampliar a fase seguinte, a leitura principal é `reports/fase_4_6/HISTORIAS_REAIS.md`: ela separa trajetórias demonstradas, falhas reais e categorias sem exemplo natural. Categorias sem exemplo natural devem motivar diagnóstico causal, sem meta de mortalidade.

## Arquivos para leitura

- [Histórias reais e todas as fatalidades](</home/hugo/Área de trabalho/procedrual/reports/fase_4_6/HISTORIAS_REAIS.md>)
- [Diagnóstico das alterações](</home/hugo/Área de trabalho/procedrual/reports/fase_4_6/DIAGNOSTICO_E_ALTERACOES.md>)
- [Índice de execuções](</home/hugo/Área de trabalho/procedrual/reports/fase_4_6/EXECUCOES.json>)
- [Validação e logs](</home/hugo/Área de trabalho/procedrual/reports/fase_4_6/validacao_testes.json>)
- [Especificação da fase](</home/hugo/Área de trabalho/procedrual/fase_4_6.md>)
