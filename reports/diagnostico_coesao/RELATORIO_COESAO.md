# Auditoria de coesão — Neravon-Coesao55

Campanha nova, natural, sem jogador, **300h**, regras **mvp-12-fase5.5**, geração **mvp-5.4**. Seed única **Neravon-Coesao55**. O diagnóstico mede a versão entregue e não introduz rebalanceamento ou funcionalidades.

O gargalo principal é continuidade:47 propostas chegaram a16 submissões e três decisões; só uma política recebeu trabalho e nenhuma terminou. Nenhum grupo acumulou quatro reuniões, portanto a formalização nem chegou ao cálculo normal de pressão. Na sobrevivência,13 mortos de sede carregavam água e 94 mortos tiveram repetição de fill_water após falha nos últimos rastros. As seções abaixo separam bloqueios corretos, bugs demonstrados e causas ainda não observáveis; não tratam ausência de evento raro como defeito.

## 1. Proveniência, execução e limites da observação

| Item | Registro |
| --- | --- |
| Código SHA256 | c60349c54564a759147738b10d6c490c44440d53afb2e681b0a8aaa5c82d4a72 |
| SHA256 depois | c60349c54564a759147738b10d6c490c44440d53afb2e681b0a8aaa5c82d4a72 |
| Commit da referência anterior à limpeza | c996d8c095f67479d36b43b9ddcbdf63420f4d39 |
| População persistente inicial/final | 1898 / 1600 |
| População abstrata inicial/final | 4693 / 4693 |
| Duração real de processamento (s) | 2005.77 |
| Verificações estruturais | [{"hour":25,"errors":[]},{"hour":50,"errors":[]},{"hour":75,"errors":[]},{"hour":100,"errors":[]},{"hour":125,"errors":[]},{"hour":150,"errors":[]},{"hour":175,"errors":[]},{"hour":200,"errors":[]},{"hour":225,"errors":[]},{"hour":250,"errors":[]},{"hour":275,"errors":[]},{"hour":300,"errors":[]}] |
| Erros de rota | [] |
| Erros do observador | {} |

Foi usado sys.setprofile externo para ler argumentos, variáveis locais e retornos efetivamente produzidos pelo motor, mais observação de eventos. Não houve substituição de funções de decisão, leitura global para alimentar NPCs, chamadas extras a soluções ou avanço auxiliar do mundo. Debug permaneceu desligado. O controle reduzido de 8h produziu estado e RNG idênticos com e sem observador (manifesto.json, controlled_checks.observer_control). Esse controle não substitui uma comparação controlada de 300h.

Houve dois reinícios com a mesma seed: uma falha do leitor ao receber return(None) durante propagação de exceção e, depois, o crash explícito da visita a POI na hora 26. Não foram reinícios por resultado. Após autorização do usuário, apenas Geography.emit teve o parâmetro kind renomeado para event_kind: duas linhas, preservando context["kind"], conteúdo e regras. O arquivo de patch e os registros de reprodução identificam a exceção. A campanha completa é a tentativa posterior; os prefixos interrompidos não entram nos totais.

28 testes selecionados passaram: suites Fase 5.5 e 5.4 e quatro regressões críticas de letalidade/alimentação. Não foi executada toda a suite histórica. O observador registra amostras iniciais de 48 criações, 80 chamadas de proposta e 40 trabalhos, mais decisões de adesão, decisões políticas e os três últimos registros de decisão de cada morto. Amostras iniciais têm viés temporal; não representam sorteio estatístico.

Unidades: chamadas, eventos, pares NPC–grupo, pessoas únicas e entidades persistentes são diferentes. GroupSearchAttempt limita emissão a 12h; recusas a 24h; ExistingGroupFound só em mudança do grupo escolhido. As contagens desses eventos não são probabilidades puras de conversão. Scores de grupos ao encerrar, calculados pelo auditor, são explicitamente identificados como derivados, não decisões tomadas pelo NPC. Campos pressure são o último cálculo do motor, não uma consulta recalculada ao final.

Evidências: metrics.json agrega estados e contadores; traces.json contém os rastros referenciados; manifesto.json contém hashes e retenção. Os três Markdown de Vaelora-55 foram preservados sem alteração. Não foi carregado o save antigo. O save temporário desta campanha serve apenas à conferência e é removido após a auditoria.

## 2. Painel do encadeamento

| Etapa | Entidades ou eventos observados | Unidade |
| --- | --- | --- |
| Necessidades coletivas distintas | 1866 | pares NPC/Need political_pressure |
| Busca efetiva | 20175 | chamadas search_groups |
| Busca publicada / grupo encontrado publicado | 5884 / 1367 | eventos limitados |
| Adesão tentada / efetivada | 1252 / 1064 | eventos |
| Grupo criado / ativo ao fim | 146 / 128 | grupos |
| Proposta criada / apoiada / apoio entregue / submetida | 47 / 47 / 16 / 16 | propostas únicas |
| Proposta decidida / vinculada a política | 3 / 3 | propostas únicas |
| Política criada / trabalhada / concluída | 3 / 1 / 0 | políticas únicas |
| Facção formalizada / aceita adesão | 0 / 2 | eventos |
| Mortos / privação | 298 / 297 | NPCs únicos |

| Need | chamadas de avaliação | com alternativa viável | seleções finais |
| --- | --- | --- | --- |
| food | 140087 | 138007 | 117733 |
| food_reserve | 13639 | 12911 | 9784 |
| water | 21112 | 14046 | 12982 |
| rest | 115715 | 114136 | 81583 |
| recovery | 169 | 84 | 526 |
| political_pressure | 18111 | 14850 | 13462 |
| organizational_survival | 4975 | 3267 | 2885 |
| affiliation | 7 | 2 | 2 |
| governance | 101 | 101 | 72 |
| institutional_work | 18 | 9 | 7 |
| institutional_response | 0 | 0 | 0 |

A seleção é hierárquica: Needs são ordenadas por prioridade, e a primeira com alternativas viáveis vence; só então se comparam Utilities de suas alternativas. Continuação de Goal, interrupção alimentar e preparação preventiva podem modificar a escolha. Não há uma disputa única entre todos os scores de todas as Needs. Avaliações adicionais de Needs pessoais não equivalem a seleção.

Os contadores de avaliação usam o kind que realmente entrou em _evaluate; recovery pode delegar solutions a uma cópia da Need com kind rest/food/water. Assim, recovery pode ter mais seleções que avaliações marcadas recovery, sem incoerência do funil: parte de suas alternativas foi contada sob outro kind. Essas colunas não são uma coorte única de necessidades.

## 3. Grupos: funil, fragmentação e conhecimento

| Métrica | Resultado |
| --- | --- |
| Avaliações que chegaram à afinidade | 27298 |
| Verificações compatíveis nessa etapa (afinidade ≥25) | 6952 |
| Verificações abaixo de 25 | 20346 |
| Pessoas com ao menos uma recusa por afinidade | 792 |
| Pessoas cujas razões observadas foram apenas baixa afinidade | 504 |
| Pares NPC–líder recusados / repetidos | 2081 / 1947 |
| Eventos de recusa | 4768 |
| Pessoas únicas com adesão | 598 |
| Grupos criados | 146 |
| Adesões por novo grupo | 7.29 |
| Expedições criadas (outro caminho de Group) | 0 |
| Tamanho final declarado de grupos ativos | {"n":128,"min":2,"p25":4.0,"median":7.0,"mean":8.1016,"p75":12.0,"p90":16.0,"max":23} |
| NPCs em múltiplos grupos equivalentes | 273 / 621 participantes (43.96%) |
| Jaccard médio de pares equivalentes ativos | 0.33 |
| Pares equivalentes com ao menos um membro comum | 86 |

| Motivo de GroupJoinRejected | Eventos históricos efetivos |
| --- | --- |
| low_social_affinity | 4243 |
| too_many_commitments | 288 |
| contact_or_capacity | 188 |
| different_objective | 32 |
| leader_unavailable | 17 |

Equivalência diagnóstica = mesma localidade de origem, causa e subject_id. Não pressupõe que os NPCs conheçam esses outros grupos. Tamanho declarado pode conter mortos ainda não podados; vínculo ativo recíproco é mostrado separadamente. Um Jaccard pequeno significa composição diferente; não prova causas diferentes.

| Localidade | causa / subject | grupos ativos | tamanhos | idades (h) | reuniões | propostas distintas |
| --- | --- | --- | --- | --- | --- | --- |
| Karvia #1088 | security / None | 6 | [14,17,12,3,3,3] | [290,278,251,238,218,200] | 3 | 1 |
| Dorria #1023 | security / None | 5 | [21,10,10,2,2] | [275,252,229,211,155] | 1 | 1 |
| Sildor #50 | security / None | 4 | [20,18,14,3] | [280,272,264,257] | 2 | 2 |
| Elimar #479 | security / None | 4 | [17,11,5,2] | [269,259,201,166] | 3 | 2 |
| Kardor #648 | security / None | 4 | [15,18,10,4] | [280,270,231,230] | 3 | 1 |
| Valmar #789 | security / None | 4 | [14,12,8,2] | [274,257,141,121] | 2 | 1 |
| Dordor #3 | security / None | 3 | [7,10,6] | [298,294,294] | 0 | 0 |
| Normar #97 | security / None | 3 | [23,16,8] | [294,279,208] | 2 | 1 |
| Silthon #162 | security / None | 3 | [18,14,13] | [276,264,263] | 3 | 1 |
| Valvia #209 | security / None | 3 | [4,6,6] | [281,253,217] | 2 | 2 |
| Nordor #227 | security / None | 3 | [8,12,5] | [272,258,184] | 3 | 2 |
| Ardor #256 | security / None | 3 | [4,5,4] | [295,291,268] | 2 | 1 |
| Valvia #302 | water_access / None | 3 | [4,13,4] | [255,254,243] | 0 | 0 |
| Arria #331 | security / None | 3 | [7,8,8] | [298,294,271] | 3 | 1 |
| Silvia #378 | security / None | 3 | [8,8,8] | [300,272,254] | 2 | 1 |
| Elivia #461 | security / None | 3 | [6,4,4] | [279,228,135] | 2 | 1 |
| Elilen #583 | security / None | 3 | [12,12,5] | [281,279,262] | 2 | 1 |
| Elilen #695 | security / None | 3 | [16,15,11] | [278,276,272] | 1 | 1 |
| Mormar #724 | security / None | 3 | [6,6,3] | [280,203,128] | 3 | 2 |
| Sildor #911 | security / None | 3 | [15,17,9] | [273,266,180] | 1 | 1 |
| Karlen #976 | security / None | 3 | [12,16,18] | [282,282,280] | 3 | 1 |
| Dordor #3 | water_access / None | 2 | [2,3] | [243,181] | 0 | 0 |
| Dorven #32 | security / None | 2 | [7,7] | [292,271] | 2 | 1 |
| Valven #191 | security / None | 2 | [3,2] | [83,41] | 0 | 0 |
| Norven #349 | security / None | 2 | [16,16] | [271,263] | 2 | 1 |
| Normar #414 | security / None | 2 | [11,7] | [279,209] | 1 | 1 |
| Northon #443 | security / None | 2 | [7,5] | [278,165] | 2 | 1 |
| Morven #508 | security / None | 2 | [6,8] | [298,272] | 2 | 1 |
| Arthon #526 | security / None | 2 | [21,16] | [286,261] | 0 | 0 |
| Elilen #583 | water_access / None | 2 | [6,2] | [254,200] | 1 | 1 |
| Elidor #612 | security / None | 2 | [4,4] | [216,169] | 2 | 1 |
| Arvia #630 | security / None | 2 | [5,4] | [262,139] | 1 | 1 |
| Elilen #677 | security / None | 2 | [7,6] | [288,138] | 1 | 1 |
| Valthon #742 | security / None | 2 | [15,19] | [296,282] | 1 | 1 |
| Dordor #771 | security / None | 2 | [8,8] | [249,208] | 1 | 1 |
| Dorthon #846 | security / None | 2 | [6,3] | [298,282] | 1 | 1 |
| Normir #893 | security / None | 2 | [7,6] | [290,125] | 1 | 1 |
| Norvia #1070 | security / None | 2 | [7,4] | [251,135] | 1 | 1 |
| Normar #79 | security / None | 1 | [6] | [291] | 1 | 1 |
| Silmir #126 | security / None | 1 | [4] | [184] | 1 | 1 |
| Dormar #144 | criminal_cooperation / None | 1 | [2] | [135] | 1 | 1 |
| Ardor #256 | resource_pressure / None | 1 | [2] | [146] | 1 | 1 |
| Valvia #302 | security / None | 1 | [3] | [296] | 0 | 0 |
| Silvia #378 | resource_pressure / None | 1 | [2] | [23] | 0 | 0 |
| Valria #396 | security / None | 1 | [4] | [257] | 0 | 0 |
| Normar #414 | criminal_cooperation / None | 1 | [2] | [11] | 0 | 0 |
| Northon #443 | resource_pressure / None | 1 | [3] | [30] | 0 | 0 |
| Elivia #461 | resource_pressure / None | 1 | [3] | [141] | 0 | 0 |
| Elilen #677 | resource_pressure / None | 1 | [2] | [78] | 0 | 0 |
| Valmar #789 | resource_pressure / None | 1 | [2] | [141] | 0 | 0 |
| Norlen #818 | resource_pressure / None | 1 | [2] | [26] | 0 | 0 |
| Dorthon #846 | water_access / None | 1 | [4] | [254] | 0 | 0 |
| Valmar #875 | resource_pressure / None | 1 | [2] | [54] | 0 | 0 |
| Valmar #875 | security / None | 1 | [9] | [268] | 0 | 0 |
| Armir #940 | resource_pressure / None | 1 | [2] | [38] | 0 | 0 |
| Armir #940 | security / None | 1 | [7] | [281] | 1 | 1 |
| Eliria #1005 | resource_pressure / None | 1 | [2] | [60] | 1 | 1 |
| Eliria #1005 | security / None | 1 | [11] | [287] | 1 | 1 |
| Silria #1117 | resource_pressure / None | 1 | [3] | [84] | 0 | 0 |
| Silria #1117 | security / None | 1 | [8] | [249] | 1 | 1 |

## 3.1 Por que organizar se já existe grupo?

collective_candidates primeiro pesquisa SOMENTE known_groups; se encontra um grupo aceito, retorna join_group e não oferece organize nesse ramo. Quando não encontra, pode oferecer share_problem e organize, com criação exigindo fato ProblemShared recente (≤72h), autor presente, afinidade com esse par ≥35 e capacidade de compromissos. form pesquisa novamente, impedindo criação se houver grupo conhecido aceito. Logo, várias criações não são uma escolha Utility(create)>Utility(join): join muitas vezes nem foi enumerado.

Fórmula base de Utility: base[action] + Σ(valor_normalizado × peso) − min(200, distância × UTILITY.distance_weight), seguida dos ajustes de GoalSystem._evaluate (alimentação, combate e pressão de ação quando aplicáveis). As considerações retidas são normalizadas por 200; multiplicar sua soma por 200 recompõe o score base, antes de outros ajustes. Need.priority não é adicionada a esse score.

| Alternativa | base | pesos reais |
| --- | --- | --- |
| join_group | 45 | {"compassion":20,"independence":-20} |
| organize | 55 | {"ambition":25,"compassion":20,"persistence":20} |
| share_problem | 45 | {"compassion":15,"independence":-15} |
| meet_group | 50 | {"diligence":20,"persistence":20} |
| submit_proposal | 70 | {"ambition":25,"persistence":20} |
| review_proposal | 65 | {"diligence":25,"honesty":15} |

### Criação real: grupo #47914 na hora 18

Iria Vale #4675; HP 100.0, fome 44.0, sede 36.0, fadiga 40.6; moedas 9; comida/água 1/0; posição 846:2,2; Goal organize/active

Personalidade na entrada: {"honesty":36,"compassion":15,"courage":77,"independence":58,"greed":79,"diligence":22,"family_loyalty":32,"persistence":7,"temperament":21,"vengefulness":83,"ambition":92,"sadism":0}.

| Need real na entrada | prioridade | status | alvo |
| --- | --- | --- | --- |
| political_pressure | 74.95 | active | — |
| advancement | 58.90 | selected | — |
| migration | 53.80 | active | 911 |
| food | 46.45 | active | — |
| rest | 42.40 | active | — |
| food_reserve | 40.63 | active | — |
| money | 39.85 | active | — |
| protection | 38.05 | active | 4675 |

| Need avaliada | alternativa | Utility | alvo | considerações normalizadas |
| --- | --- | --- | --- | --- |
| political_pressure | organize | 82.40 | — | {"base":0.275,"ambition":0.115,"compassion":0.015,"persistence":0.007000000000000001,"travel":-0.0} |
| advancement | work | 41.00 | — | {"base":0.25,"diligence":0.055,"physical_depletion":0.0,"travel":-0.1,"no_progress":0.0} |
| protection | ask_personal_help | 35.35 | 4678 | {"base":0.125,"independence":-0.087,"compassion":0.015,"trust":0.11025,"reputation":0.0,"relationship":0.013500000000000002,"travel":-0.0} |

Causa/subject: security/None; conhecidos antes: [21951, 44760]; pesquisa interna retornou []; verificações reais: [{"hour":18,"group":21951,"ok":false,"reason":"low_social_affinity","affinity":{"score":21.799999999999997,"trust":10,"friendship":0,"same_profession":false}},{"hour":18,"group":44760,"ok":false,"reason":"low_social_affinity","affinity":{"score":21.799999999999997,"trust":10,"friendship":0,"same_profession":false}},{"hour":18,"group":21951,"ok":false,"reason":"low_social_affinity","affinity":{"score":21.799999999999997,"trust":10,"friendship":0,"same_profession":false}},{"hour":18,"group":44760,"ok":false,"reason":"low_social_affinity","affinity":{"score":21.799999999999997,"trust":10,"friendship":0,"same_profession":false}}]; resultado: novo grupo #47914.

Utility(join): não calculada nesse registro; não havia alternativa join_group avaliada. A existência global de grupos não concede conhecimento ao NPC.

### Criação real: grupo #51135 na hora 20

Marie Alvor #5247; HP 100.0, fome 24.0, sede 40.0, fadiga 26.0; moedas 15; comida/água 0/0; posição 976:5,9; Goal organize/active

Personalidade na entrada: {"honesty":87,"compassion":33,"courage":84,"independence":84,"greed":85,"diligence":23,"family_loyalty":60,"persistence":88,"temperament":31,"vengefulness":11,"ambition":78,"sadism":9}.

| Need real na entrada | prioridade | status | alvo |
| --- | --- | --- | --- |
| political_pressure | 72.56 | active | — |
| food_reserve | 54.26 | active | — |
| protection | 53.05 | active | 5247 |
| advancement | 52.96 | selected | — |
| migration | 52.00 | active | 846 |
| divine_contact | 50.60 | active | 5850 |
| water | 40.90 | active | — |
| religious_interest | 38.33 | active | 5850 |

| Need avaliada | alternativa | Utility | alvo | considerações normalizadas |
| --- | --- | --- | --- | --- |
| political_pressure | organize | 98.70 | — | {"base":0.275,"ambition":0.0975,"compassion":0.033,"persistence":0.08800000000000001,"travel":-0.0} |
| political_pressure | share_problem | 37.35 | — | {"base":0.225,"compassion":0.02475,"independence":-0.063,"travel":-0.0} |
| protection | denounce | 92.75 | 999 | {"base":0.225,"honesty":0.15225,"vengefulness":0.011000000000000001,"courage":0.063,"trust":0.0125,"travel":-0.0} |
| protection | denounce | 92.75 | 5215 | {"base":0.225,"honesty":0.15225,"vengefulness":0.011000000000000001,"courage":0.063,"trust":0.0125,"travel":-0.0} |
| protection | denounce | 92.75 | 5238 | {"base":0.225,"honesty":0.15225,"vengefulness":0.011000000000000001,"courage":0.063,"trust":0.0125,"travel":-0.0} |
| protection | denounce | 92.75 | 5261 | {"base":0.225,"honesty":0.15225,"vengefulness":0.011000000000000001,"courage":0.063,"trust":0.0125,"travel":-0.0} |
| protection | denounce | 92.75 | 5284 | {"base":0.225,"honesty":0.15225,"vengefulness":0.011000000000000001,"courage":0.063,"trust":0.0125,"travel":-0.0} |
| protection | denounce | 92.75 | 5307 | {"base":0.225,"honesty":0.15225,"vengefulness":0.011000000000000001,"courage":0.063,"trust":0.0125,"travel":-0.0} |
| protection | denounce | 92.75 | 5330 | {"base":0.225,"honesty":0.15225,"vengefulness":0.011000000000000001,"courage":0.063,"trust":0.0125,"travel":-0.0} |
| protection | denounce | 92.75 | 5365 | {"base":0.225,"honesty":0.15225,"vengefulness":0.011000000000000001,"courage":0.063,"trust":0.0125,"travel":-0.0} |
| protection | demand_return | 91.95 | 5198 | {"base":0.2,"honesty":0.10875,"persistence":0.08800000000000001,"courage":0.063,"travel":-0.0} |
| protection | defend | 62.22 | 5198 | {"base":0.2,"risk":0.04807692307692307,"courage":0.063,"defensive":0.0,"injury":-0.0,"travel":-0.0} |
| protection | confront | 56.08 | 5198 | {"base":0.175,"courage":0.126,"anger":0.0,"risk":-0.02884615384615384,"vengefulness":0.00825,"travel":-0.0} |
| protection | apologize | 55.00 | 5198 | {"base":0.125,"honesty":0.10875,"compassion":0.04125,"culpability":0.0,"anger":-0.0,"travel":-0.0} |
| advancement | work | 61.50 | — | {"base":0.25,"diligence":0.0575,"physical_depletion":0.0,"travel":-0.0,"no_progress":0.0} |

Causa/subject: security/None; conhecidos antes: [46771, 46813]; pesquisa interna retornou []; verificações reais: [{"hour":20,"group":46771,"ok":false,"reason":"low_social_affinity","affinity":{"score":23.3,"trust":10,"friendship":0,"same_profession":false}},{"hour":20,"group":46813,"ok":false,"reason":"low_social_affinity","affinity":{"score":23.3,"trust":10,"friendship":0,"same_profession":false}},{"hour":20,"group":46771,"ok":false,"reason":"low_social_affinity","affinity":{"score":23.3,"trust":10,"friendship":0,"same_profession":false}},{"hour":20,"group":46813,"ok":false,"reason":"low_social_affinity","affinity":{"score":23.3,"trust":10,"friendship":0,"same_profession":false}}]; resultado: novo grupo #51135.

Utility(join): não calculada nesse registro; não havia alternativa join_group avaliada. A existência global de grupos não concede conhecimento ao NPC.

### Criação real: grupo #27668 na hora 6

Cael Solaris #1231; HP 100.0, fome 35.0, sede 12.0, fadiga 10.2; moedas 4; comida/água 2/0; posição 3:2,2; Goal organize/active

Personalidade na entrada: {"honesty":84,"compassion":17,"courage":68,"independence":94,"greed":63,"diligence":23,"family_loyalty":82,"persistence":19,"temperament":80,"vengefulness":77,"ambition":84,"sadism":16}.

| Need real na entrada | prioridade | status | alvo |
| --- | --- | --- | --- |
| political_pressure | 72.52 | active | — |
| advancement | 52.04 | active | — |
| migration | 52.00 | active | 50 |
| money | 46.60 | active | — |
| protection | 42.00 | active | 1231 |
| food | 20.00 | active | — |

| Need avaliada | alternativa | Utility | alvo | considerações normalizadas |
| --- | --- | --- | --- | --- |
| political_pressure | organize | 83.20 | — | {"base":0.275,"ambition":0.105,"compassion":0.017,"persistence":0.019,"travel":-0.0} |
| political_pressure | share_problem | 33.45 | — | {"base":0.225,"compassion":0.012750000000000001,"independence":-0.0705,"travel":-0.0} |
| advancement | work | 29.50 | — | {"base":0.25,"diligence":0.0575,"physical_depletion":0.0,"travel":-0.16,"no_progress":0.0} |
| protection | ask_personal_help | 17.70 | 1228 | {"base":0.125,"independence":-0.141,"compassion":0.017,"trust":0.07,"reputation":0.0,"relationship":0.0175,"travel":-0.0} |

Causa/subject: security/None; conhecidos antes: [19980]; pesquisa interna retornou []; verificações reais: [{"hour":6,"group":19980,"ok":false,"reason":"low_social_affinity","affinity":{"score":21.0,"trust":10,"friendship":0,"same_profession":false}},{"hour":6,"group":19980,"ok":false,"reason":"low_social_affinity","affinity":{"score":21.0,"trust":10,"friendship":0,"same_profession":false}}]; resultado: novo grupo #27668.

Utility(join): não calculada nesse registro; não havia alternativa join_group avaliada. A existência global de grupos não concede conhecimento ao NPC.

### Criação real: grupo #28103 na hora 6

Marie Bruma #2638; HP 100.0, fome 37.0, sede 12.0, fadiga 16.2; moedas 22; comida/água 1/0; posição 331:2,2; Goal organize/active

Personalidade na entrada: {"honesty":9,"compassion":52,"courage":23,"independence":68,"greed":47,"diligence":45,"family_loyalty":93,"persistence":83,"temperament":27,"vengefulness":75,"ambition":37,"sadism":19}.

| Need real na entrada | prioridade | status | alvo |
| --- | --- | --- | --- |
| political_pressure | 66.46 | active | — |
| migration | 52.00 | active | 302 |
| protection | 47.60 | active | 2638 |
| food_reserve | 37.00 | active | — |
| religious_interest | 30.40 | active | 5848 |
| food | 26.00 | active | — |

| Need avaliada | alternativa | Utility | alvo | considerações normalizadas |
| --- | --- | --- | --- | --- |
| political_pressure | organize | 91.25 | — | {"base":0.275,"ambition":0.04625,"compassion":0.052000000000000005,"persistence":0.08299999999999999,"travel":-0.0} |
| political_pressure | share_problem | 42.60 | — | {"base":0.225,"compassion":0.03900000000000001,"independence":-0.051000000000000004,"travel":-0.0} |
| protection | pursue | 81.40 | 2655 | {"base":0.275,"courage":0.023000000000000003,"diligence":0.03375,"vengefulness":0.075,"critical_depletion":0.0,"travel":-0.0,"action_pressure":0.0,"pressure_risk_tolerance":0.00025546211634397344} |
| protection | ask_personal_help | 30.60 | 2635 | {"base":0.125,"independence":-0.10200000000000001,"compassion":0.052000000000000005,"trust":0.049,"reputation":0.0,"relationship":0.028999999999999998,"travel":-0.0} |
| protection | avoid_threat | 15.60 | — | {"base":0.2,"courage":-0.046000000000000006,"compassion":0.03900000000000001,"vengefulness":-0.075,"travel":-0.04} |

Causa/subject: security/None; conhecidos antes: [20728]; pesquisa interna retornou []; verificações reais: [{"hour":6,"group":20728,"ok":false,"reason":"low_social_affinity","affinity":{"score":20.95,"trust":10,"friendship":0,"same_profession":false}},{"hour":6,"group":20728,"ok":false,"reason":"low_social_affinity","affinity":{"score":20.95,"trust":10,"friendship":0,"same_profession":false}}]; resultado: novo grupo #28103.

Utility(join): não calculada nesse registro; não havia alternativa join_group avaliada. A existência global de grupos não concede conhecimento ao NPC.

### Criação real: grupo #32339 na hora 9

Darin Alvor #2293; HP 100.0, fome 35.0, sede 18.0, fadiga 18.8; moedas 14; comida/água 0/0; posição 256:2,2; Goal organize/active

Personalidade na entrada: {"honesty":10,"compassion":47,"courage":88,"independence":62,"greed":15,"diligence":90,"family_loyalty":10,"persistence":92,"temperament":22,"vengefulness":19,"ambition":70,"sadism":1}.

| Need real na entrada | prioridade | status | alvo |
| --- | --- | --- | --- |
| political_pressure | 71.57 | active | — |
| food_reserve | 61.00 | active | — |
| work | 53.00 | active | — |
| migration | 52.00 | active | 227 |
| divine_contact | 50.90 | active | 5848 |
| religious_interest | 39.81 | active | 5848 |
| advancement | 33.85 | active | — |
| protection | 33.55 | active | 2293 |

| Need avaliada | alternativa | Utility | alvo | considerações normalizadas |
| --- | --- | --- | --- | --- |
| political_pressure | organize | 100.30 | — | {"base":0.275,"ambition":0.0875,"compassion":0.04699999999999999,"persistence":0.09200000000000001,"travel":-0.0} |
| political_pressure | share_problem | 42.75 | — | {"base":0.225,"compassion":0.03525,"independence":-0.04650000000000001,"travel":-0.0} |
| advancement | work | 91.00 | — | {"base":0.25,"diligence":0.225,"physical_depletion":0.0,"travel":-0.02} |
| advancement | steal_person | 67.89 | 2302 | {"base":0.31,"greed":0.03,"honesty":-0.045,"authority":-0.0,"courage":0.044000000000000004,"travel":-0.0,"pressure_moral_tolerance":0.00044481390306122444} |
| protection | demand_return | 74.10 | 2302 | {"base":0.2,"honesty":0.0125,"persistence":0.09200000000000001,"courage":0.066,"travel":-0.0} |
| protection | defend | 62.82 | 2302 | {"base":0.2,"risk":0.04807692307692307,"courage":0.066,"defensive":0.0,"injury":-0.0,"travel":-0.0} |
| protection | confront | 58.48 | 2302 | {"base":0.175,"courage":0.132,"anger":0.0,"risk":-0.02884615384615384,"vengefulness":0.01425,"travel":-0.0} |
| protection | calm | 49.10 | 2302 | {"base":0.175,"compassion":0.0705,"bond":0.0,"anger":-0.0,"travel":-0.0} |
| protection | ask_personal_help | 46.05 | 2290 | {"base":0.125,"independence":-0.09300000000000001,"compassion":0.04699999999999999,"trust":0.11375,"reputation":0.0,"relationship":0.0375,"travel":-0.0} |
| protection | warn | 40.90 | 2302 | {"base":0.15,"compassion":0.04699999999999999,"honesty":0.0075,"travel":-0.0} |
| protection | apologize | 39.25 | 2302 | {"base":0.125,"honesty":0.0125,"compassion":0.05875,"culpability":0.0,"anger":-0.0,"travel":-0.0} |
| protection | withdraw | 38.47 | 2302 | {"base":0.175,"risk":0.04807692307692307,"compassion":0.03525,"courage":-0.066,"defensive":-0.0,"travel":-0.0} |
| protection | forgive | 35.75 | 2302 | {"base":0.125,"compassion":0.08224999999999999,"bond":0.0,"vengefulness":-0.0285,"resentment":-0.0,"travel":-0.0} |
| protection | threaten | 35.37 | 2302 | {"base":0.125,"anger":0.0,"courage":0.08800000000000001,"temperament":0.022000000000000002,"compassion":-0.05875,"authority":-0.0,"critical_depletion":0.0,"travel":-0.0,"pressure_risk_tolerance":0.0006151432135007847} |
| protection | flee | 24.54 | 2302 | {"base":0.175,"fear":0.0,"risk":0.05769230769230768,"courage":-0.11,"low_health":0.0,"injury":-0.0,"authority":0.0,"travel":-0.0} |
| protection | surrender | 12.62 | 2302 | {"base":0.125,"authority":0.0,"risk":0.04807692307692307,"low_health":0.0,"courage":-0.11,"defensive":-0.0,"travel":-0.0} |

Causa/subject: security/None; conhecidos antes: [26469]; pesquisa interna retornou []; verificações reais: [{"hour":9,"group":26469,"ok":false,"reason":"low_social_affinity","affinity":{"score":24.9,"trust":10,"friendship":0,"same_profession":false}},{"hour":9,"group":26469,"ok":false,"reason":"low_social_affinity","affinity":{"score":24.9,"trust":10,"friendship":0,"same_profession":false}}]; resultado: novo grupo #32339.

Utility(join): não calculada nesse registro; não havia alternativa join_group avaliada. A existência global de grupos não concede conhecimento ao NPC.

### Criação real: grupo #35756 na hora 11

Cael Bruma #2580; HP 100.0, fome 29.0, sede 22.0, fadiga 29.2; moedas 5; comida/água 1/0; posição 302:2,2; Goal organize/active

Personalidade na entrada: {"honesty":64,"compassion":56,"courage":15,"independence":88,"greed":36,"diligence":34,"family_loyalty":74,"persistence":68,"temperament":77,"vengefulness":35,"ambition":7,"sadism":5}.

| Need real na entrada | prioridade | status | alvo |
| --- | --- | --- | --- |
| political_pressure | 61.44 | active | — |
| migration | 52.00 | active | 349 |
| money | 48.52 | active | — |
| protection | 47.10 | active | 2580 |
| work | 41.80 | active | — |
| food_reserve | 35.80 | active | — |
| religious_interest | 34.56 | active | 5848 |
| rest | 29.20 | active | — |

| Need avaliada | alternativa | Utility | alvo | considerações normalizadas |
| --- | --- | --- | --- | --- |
| political_pressure | organize | 81.55 | — | {"base":0.275,"ambition":0.00875,"compassion":0.05600000000000001,"persistence":0.068,"travel":-0.0} |
| political_pressure | share_problem | 40.20 | — | {"base":0.225,"compassion":0.042,"independence":-0.066,"travel":-0.0} |
| protection | ask_personal_help | 24.30 | 2577 | {"base":0.125,"independence":-0.132,"compassion":0.05600000000000001,"trust":0.049,"reputation":0.0,"relationship":0.023499999999999997,"travel":-0.0} |
| protection | avoid_threat | 11.40 | — | {"base":0.2,"courage":-0.03,"compassion":0.042,"vengefulness":-0.035,"travel":-0.12} |

Causa/subject: security/None; conhecidos antes: [24876]; pesquisa interna retornou []; verificações reais: [{"hour":11,"group":24876,"ok":false,"reason":"low_social_affinity","affinity":{"score":17.250000000000004,"trust":10,"friendship":0,"same_profession":false}},{"hour":11,"group":24876,"ok":false,"reason":"low_social_affinity","affinity":{"score":17.250000000000004,"trust":10,"friendship":0,"same_profession":false}}]; resultado: novo grupo #35756.

Utility(join): não calculada nesse registro; não havia alternativa join_group avaliada. A existência global de grupos não concede conhecimento ao NPC.

## 3.2 Afinidade social: fórmula e distribuição

```python
def affinity(self,p,q,cause):
    trust=self.e.graph.value(p.id,q.id,'confiança',10)
    bond=self.e.graph.value(p.id,q.id,'amizade')
    return trust*.5+bond*.2+p.personality.compassion*.2+p.personality.ambition*.15+(8 if p.profession==q.profession else 0)
```

Aceite em acceptable_group exige ≥25; recrutamento dos pares da criação exige ≥35. Antes da afinidade existem gates de status/objetivo, grupo fechado/capacidade, três compromissos, líder vivo, confiança≥5, crença compatível, preferência de liderança após fracassos e rota. A variável cause é recebida mas não altera a fórmula. Confiança padrão é 10; amizade padrão 0. Apenas saber que o grupo existe ou observar um membro não concede bônus de familiaridade. Família pode influenciar relações no grafo, mas não recebe termo próprio aqui. Tamanho não altera afinidade; entre grupos aceitos, a pesquisa prefere maior composição e depois maior idade.

| Distribuição realmente calculada | Valores |
| --- | --- |
| Todos os checks que alcançaram affinity | {"n":27298,"min":7.05,"p25":17.75,"median":21.45,"mean":22.0625,"p75":25.2,"p90":31.3,"max":70.25} |

| hora | NPC | líder | confiança | amizade | compaixão | ambição | mesma profissão | score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 2834 | 2851 | 10 | 0 | 62 | 38 | False | 23.10 |
| 1 | 2834 | 2851 | 10 | 0 | 62 | 38 | False | 23.10 |
| 1 | 2837 | 2851 | 10 | 0 | 18 | 74 | False | 19.70 |
| 1 | 2837 | 2851 | 10 | 0 | 18 | 74 | False | 19.70 |
| 2 | 2834 | 2851 | 10 | 0 | 62 | 38 | False | 23.10 |
| 2 | 2837 | 2851 | 10 | 0 | 18 | 74 | False | 19.70 |
| 2 | 4839 | 4658 | 10 | 0 | 44 | 38 | False | 19.50 |
| 3 | 1222 | 1395 | 10 | 0 | 29 | 51 | False | 18.45 |
| 3 | 1222 | 1395 | 10 | 0 | 29 | 51 | False | 18.45 |
| 3 | 1228 | 1395 | 10 | 0 | 32 | 76 | False | 22.80 |
| 3 | 1300 | 1395 | 10 | 0 | 83 | 8 | False | 22.80 |
| 3 | 1300 | 1395 | 10 | 0 | 83 | 8 | False | 22.80 |

“Apenas afinidade” refere-se ao conjunto de motivos observados por pessoa durante a campanha, não à prova contrafactual de que ela ingressaria se o threshold fosse reduzido. Repetição foi medida por par NPC–líder com mais de uma avaliação recusada; nem toda reavaliação é uma tentativa presencial de adesão. Efeito indireto confirmado no código: afinidade abaixo do limiar retira join das alternativas e permite organização separada se outro par cumprir os gates.

## 4. Churn, dissolução e vida social dos grupos

| Métrica | Resultado |
| --- | --- |
| Eventos GroupJoined | 1064 |
| Remoções de membro observadas entre horas | 259 |
| Removido já morto / vivo | 259 / 0 |
| Pessoas únicas nos vínculos removidos | 141 |
| Dissoluções / fusões | 18 / 0 |
| Objetos retirados do mundo | 0 |
| Duração criada→dissolução ou encerramento | {"n":146,"min":11,"p25":190.25,"median":257.0,"mean":226.0068,"p75":278.75,"p90":290.5,"max":300} |
| Sem atividade desde last_relevant, ativos | {"n":128,"min":7,"p25":60.75,"median":130.5,"mean":126.6406,"p75":182.25,"p90":214.1,"max":251} |
| Reuniões acumuladas, ativos | {"n":128,"min":0,"p25":0.0,"median":1.0,"mean":0.5469,"p75":1.0,"p90":1.0,"max":2} |
| Ativos sem proposta / sem reunião | 59 / 59 |

O ledger compara conjuntos de membros a cada hora. Óbito e remoção não são eventos simultâneos: a manutenção periódica pode podar mais tarde. Uma adesão seguida de remoção dentro da mesma hora pode escapar à comparação. Dissolver remove vínculos no Character e pode manter a lista histórica no Group; esse estoque não equivale a associação ativa. Não há evento de saída voluntária separado nessa contagem. Tempo socialmente ativo é aproximação criada→dissolução, com last_relevant e reuniões; não uma leitura psicológica contínua.

| Grupo | local / causa | fundadores | joins | únicos fundadores+joins | removidos mortos/vivos | finais declarados / vivos | links nas pessoas / recíprocos vivos | status | reuniões | última atividade |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 27668 | Dordor #3/security | 2 | 38 | 40 | 30/0 | 10/6 | 40/6 | active | 0 | 52 |
| 27726 | Dordor #3/security | 2 | 35 | 37 | 31/0 | 6/4 | 37/4 | active | 0 | 69 |
| 19980 | Dordor #3/security | 2 | 30 | 32 | 25/0 | 7/5 | 32/5 | active | 0 | 53 |
| 21951 | Dorthon #846/security | 2 | 27 | 29 | 23/0 | 6/4 | 29/4 | active | 1 | 49 |
| 52318 | Elilen #583/security | 2 | 25 | 27 | 15/0 | 12/12 | 27/12 | active | 1 | 55 |
| 30183 | Valvia #302/security | 2 | 23 | 25 | 12/0 | 13/11 | 12/0 | dissolved | 1 | 288 |
| 59875 | Valvia #302/security | 2 | 23 | 25 | 12/0 | 13/11 | 12/0 | dissolved | 1 | 288 |
| 85797 | Valvia #302/water_access | 4 | 23 | 27 | 14/0 | 13/10 | 27/10 | active | 0 | 197 |
| 27898 | Normar #97/security | 2 | 22 | 24 | 1/0 | 23/23 | 24/23 | active | 1 | 254 |
| 49193 | Elilen #583/security | 2 | 20 | 22 | 10/0 | 12/11 | 22/11 | active | 1 | 58 |
| 41293 | Arthon #526/security | 2 | 19 | 21 | 0/0 | 21/21 | 21/21 | active | 0 | 103 |
| 58457 | Dorria #1023/security | 2 | 19 | 21 | 0/0 | 21/21 | 21/21 | active | 0 | 141 |

actor_links é a referência Character.group_ids, incluindo personagens mortos cujo vínculo histórico não foi apagado. Não é vínculo recíproco por si só. A última coluna de links vivos cruza pessoa viva, composição do grupo e status ativo. A fragmentação/sobreposição da seção 3 usa apenas membros vivos; a distribuição de tamanho declarado permanece separada.

Grupo #27726: fundadores [1268, 1406]; 35 joins; remoções reais [hora,NPC,morto] [(168, 1335, True), (168, 1188, True), (168, 1309, True), (168, 1199, True), (192, 1418, True), (192, 1260, True), (192, 1266, True), (192, 1294, True), (216, 9, True), (216, 1211, True), (216, 44, True), (216, 1317, True), (240, 1220, True), (240, 1257, True), (240, 1427, True), (240, 1303, True), (240, 1240, True), (264, 1369, True), (264, 1406, True), (264, 1286, True), (288, 1248, True), (288, 1283, True), (288, 1381, True), (288, 1222, True), (288, 1289, True), (288, 1323, True), (288, 12, True), (288, 1306, True), (288, 1358, True), (288, 1268, True), (288, 1274, True)]; dissolução None (None); lista final [1438, 1412, 292, 1386, 1395, 1182]; vínculos [9, 12, 44, 292, 1182, 1188, 1199, 1211, 1220, 1222, 1240, 1248, 1257, 1260, 1266, 1268, 1274, 1283, 1286, 1289, 1294, 1303, 1306, 1309, 1317, 1323, 1335, 1358, 1369, 1381, 1386, 1395, 1406, 1412, 1418, 1427, 1438].

Grupo #27668: fundadores [1231, 1228]; 38 joins; remoções reais [hora,NPC,morto] [(168, 1188, True), (168, 1309, True), (168, 1335, True), (192, 1418, True), (192, 1260, True), (192, 1294, True), (192, 1234, True), (192, 1266, True), (216, 9, True), (216, 1211, True), (216, 1300, True), (216, 1317, True), (240, 1220, True), (240, 1254, True), (240, 1257, True), (240, 1427, True), (240, 1303, True), (240, 1240, True), (240, 1435, True), (264, 1369, True), (288, 1248, True), (288, 1346, True), (288, 1381, True), (288, 1289, True), (288, 1274, True), (288, 1323, True), (288, 12, True), (288, 1358, True), (288, 1268, True), (288, 1306, True)]; dissolução None (None); lista final [1231, 1228, 292, 1395, 1438, 1412, 1386, 1392, 1182, 1378]; vínculos [9, 12, 292, 1182, 1188, 1211, 1220, 1228, 1231, 1234, 1240, 1248, 1254, 1257, 1260, 1266, 1268, 1274, 1289, 1294, 1300, 1303, 1306, 1309, 1317, 1323, 1335, 1346, 1358, 1369, 1378, 1381, 1386, 1392, 1395, 1412, 1418, 1427, 1435, 1438].

Grupo #19980: fundadores [1395, 1392]; 30 joins; remoções reais [hora,NPC,morto] [(168, 1188, True), (168, 1309, True), (168, 1335, True), (192, 1418, True), (192, 1260, True), (192, 1326, True), (192, 1294, True), (192, 1266, True), (216, 9, True), (216, 1211, True), (216, 1349, True), (216, 1317, True), (240, 1240, True), (240, 1427, True), (240, 1220, True), (240, 1303, True), (264, 1369, True), (288, 1248, True), (288, 1381, True), (288, 1289, True), (288, 1323, True), (288, 12, True), (288, 1358, True), (288, 1268, True), (288, 1372, True)]; dissolução None (None); lista final [1395, 1392, 292, 1438, 1412, 1182, 1386]; vínculos [9, 12, 292, 1182, 1188, 1211, 1220, 1240, 1248, 1260, 1266, 1268, 1289, 1294, 1303, 1309, 1317, 1323, 1326, 1335, 1349, 1358, 1369, 1372, 1381, 1386, 1392, 1395, 1412, 1418, 1427, 1438].

Vaelora registrou um grupo de Dormir com 25 adesões e cinco membros finais, mas seus três Markdown não preservam o ledger completo. Não é possível reconstruir honestamente cada saída daquela campanha. Os casos acima respondem à mesma pergunta nesta campanha com as remoções efetivamente observadas.

## 5. Formalização: score, gates anteriores e ponto de parada

```python
def formalization(self,p,g,present,execute=False):
    age=self.w.turn-g.created_at;funds=sum(min(2,max(0,q.money-15)) for q in present)
    score=min(100,min(25,age/8)+g.failures*8+g.investment*5+min(15,len(present)*3)+min(15,funds*2))
    g.plan['formalization_pressure']={'value':score,'age':age,'known_failures':g.failures,'meetings':g.investment,'present_members':len(present),'available_contributions':funds}
    if self.w.turn-g.plan.get('last_formalization_audit',-1000)>=24:
        g.plan['last_formalization_audit']=self.w.turn
        self.emit('FormalizationConsidered',p,g.id,group_id=g.id,factors=g.plan['formalization_pressure'])
    if not execute or score<65 or g.investment<4 or age<168 or len(present)<3 or funds<4:return None
    f=self.e.society.found_faction(p,g,present)
    return f
```

No caminho da reunião, a função não é chamada para todo grupo a cada hora. Society.meeting exige líder e ≥2 presentes; atualiza investimento; dissolve se não houver problema compartilhado; só chama formalization após investimento≥4, idade≥168h, ≥3 membros registrados e ≥2 presentes com mais de 15 moedas. Formalization ainda exige ≥3 presentes, contribuição≥4 e score≥65. found_faction acrescenta líder/grupo ativos, capacidade global (<24 facções), limites de vínculos e contribuição real. Pressão alta isolada não aciona nada nesse caminho.

Há também um caminho legado: Access.candidates oferece formalize_organization ao líder com investimento≥4, idade≥168h e três membros registrados; Access.execute chama found_faction diretamente. Ele NÃO passa por Institutions.formalization e NÃO exige seu score 65 nem três presentes. Portanto, o funil de score abaixo cobre a via de reunião, não todas as rotas possíveis de criação. A divergência foi reproduzida com score 55 e dois presentes e está nos bugs confirmados, sem alteração comportamental.

| Etapa real | grupos únicos | chamadas |
| --- | --- | --- |
| Criados | 146 | 146 |
| Reunião chamada | 81 | 86 |
| Passaram gates externos de formalização em reunião | 0 | 0 |
| Função formalization efetivamente chamada | 0 | 0 |
| Score ≥65 dentro da função | 0 | 0 |
| Ação legada formalize_organization: seleções / execuções / falhas | unidades não são grupos únicos | 0 / 0 / 0 |
| Formalizados | 0 | 0 |

| Gate ausente na reunião (categorias sobrepostas) | chamadas |
| --- | --- |
| investimento≥4 | 86 |
| idade≥168 | 82 |
| membros≥3 | 16 |
| ricos presentes≥2 | 47 |

| Grupo / causa | membros | idade | reuniões / fracassos | caixa grupo | pressão problema | presentes / contribuições | score derivado /65 | líder HP/moedas/presente | gates ausentes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 46771/security | 12 | 282 | 2/7 | 0 | 21.27 | 3/0 | 100 | 100/1/False | ["meetings_ge4","rich_present_ge2","funds_ge4","leader_present"] |
| 51135/security | 18 | 280 | 1/7 | 0 | 0.00 | 5/0 | 100 | 100/0/False | ["meetings_ge4","rich_present_ge2","funds_ge4","leader_present"] |
| 63807/security | 16 | 271 | 1/1 | 0 | 0.00 | 3/0 | 47 | 82/0/False | ["meetings_ge4","rich_present_ge2","funds_ge4","score_ge65","leader_present"] |
| 90047/security | 7 | 251 | 1/0 | 0 | 0.00 | 3/4 | 47 | 86/2/False | ["meetings_ge4","score_ge65","leader_present"] |
| 93737/security | 8 | 249 | 1/0 | 0 | 55 | 4/2 | 46 | 100/0/False | ["meetings_ge4","rich_present_ge2","funds_ge4","score_ge65","leader_present"] |
| 20728/security | 7 | 298 | 1/0 | 0 | 55 | 6/0 | 45 | 100/1/True | ["meetings_ge4","rich_present_ge2","funds_ge4","score_ge65"] |
| 28103/security | 8 | 294 | 1/0 | 0 | 55 | 7/0 | 45 | 100/0/True | ["meetings_ge4","rich_present_ge2","funds_ge4","score_ge65"] |
| 53894/security | 16 | 278 | 1/0 | 0 | 14.12 | 7/0 | 45 | 54/0/False | ["meetings_ge4","rich_present_ge2","funds_ge4","score_ge65","leader_present"] |
| 63767/security | 8 | 271 | 1/0 | 0 | 55 | 6/0 | 45 | 100/6/False | ["meetings_ge4","rich_present_ge2","funds_ge4","score_ge65","leader_present"] |
| 74469/security | 16 | 263 | 1/1 | 0 | 0.00 | 2/0 | 44 | 94/0/False | ["meetings_ge4","rich_present_ge2","present_ge3","funds_ge4","score_ge65","leader_present"] |

Top 10 = cálculo diagnóstico na posição do mercado na hora 300. Não é chamada histórica a formalization. O grupo não tem depósito de itens próprio no modelo; money é caixa do grupo, enquanto funds são moedas contribuíveis dos presentes acima de 15, limitadas a duas por pessoa. Problema persistente usa g.pressure/failures; comprovar necessidade individual de todos os ausentes nesse instante exigiria atualização extra e não foi feito.

O primeiro bloqueio natural confirmado foi investimento/reuniões: zero das86 chamadas chegou a quatro reuniões; os grupos ativos terminaram com no máximo duas. Isso bloqueou inclusive a ação legada. Em Society.candidates, líder com proposta pendente conhecida como draft retorna apenas submit_proposal antes de enumerar meet_group. Essa exclusividade ajuda a explicar a continuidade curta de reuniões enquanto há rascunho, sem provar cada hora de escolha dos líderes. Score derivado100 em dois grupos não atravessa esse gate.

## 6. Facções: visibilidade, contato e adesão

| Facção | conhecem existência total/vivos | conhecem HQ total/vivos | observaram membro | contato presencial ao longo da campanha | termos de benefícios / custos conhecidos | elegíveis básicos finais | convidados | status dos registros | membros finais |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Companhia de Ardor | 124/44 | 124/44 | 118 | 118 | 4 / 4 | 43 | 4 | {"expired_for_reason":3,"offered":1} | 1 |
| Irmandade de Elimir | 105/39 | 105/39 | 105 | 105 | 5 / 5 | 38 | 5 | {"accepted":2,"expired_for_reason":2,"offered":1} | 1 |

Conhecer HQ significa place_knowledge contém a sede; não garante saber rota até ela. Contato é co-presença lida em Access.refresh, e observar membro é possuir observação dessa pessoa; não são sinônimos de conversa bem-sucedida. Elegibilidade básica final = vivo, facção conhecida, sem organização e facção ativa; não garante Utility suficiente, equipamento ou capacidade de ingresso. Esses conjuntos em momentos diferentes não compõem uma única coorte monotônica. Benefícios/riscos conhecidos de fato foram contados pelos registros de terms, não atribuídos a todos os conhecedores.

| Etapa | Resultado | Unidade |
| --- | --- | --- |
| Sabem que alguma facção existe | 229 | pessoas no encerramento |
| Tiveram co-presença observada | 223 | pessoas acumuladas |
| Convidados publicados | 9 | eventos |
| Solicitações espontâneas | 0 | eventos |
| Registros de ingresso / com termos | 9 / 9 | pares NPC–facção |
| Avaliações de membership executadas | 2 | chamadas |
| Candidatos avaliados únicos | 2 | pares NPC–facção |
| Aceites / recusas / adiamentos / condições | 2 / 0 / 0 / 0 | eventos |
| Aceites que continuam na lista final | 0 | NPC–facção |
| Deserções publicadas | 0 | eventos |

| Ingressante que morreu | nome | causa | hora |
| --- | --- | --- | --- |
| 325 | Nora Vale | thirst | 216 |
| 2384 | Mira Douran | thirst | 168 |

```python
def membership_scores(self,p,f,record):
    info=record.get('terms',{});b=info.get('benefits',{});c=info.get('costs',{})
    benefit=(min(15,b.get('income',0)*4)*(1 if p.money<15 else .3)+min(20,b.get('food',0)*4)*p.hunger/100+
             min(25,b.get('water',0)*5)*p.thirst/100+b.get('protection',0)*(20 if self.e.society.pressure(p) else 8)+
             min(12,b.get('company',0)*4)+p.personality.ambition*.12+self.e.access.faction_fit(p,f)*.35+
             b.get('training',0)*8)
    cost=c.get('dues',1)*3+p.personality.independence*.2+c.get('risk',.4)*(100-p.personality.courage)*.15
    if f.headquarters_id!=p.position.map_id and not self.e.geography.plan(p,f.headquarters_id):cost+=8
    if self.e.graph.value(p.id,record.get('inviter',f.leader_id),'confiança',10)<5:cost+=30
    return {'perceived_benefit':round(benefit,2),'perceived_cost':round(cost,2)}
```

A fórmula lê termos transmitidos pelo membro, fome/sede atuais, dinheiro pessoal, traços, fit calculado por Access e confiança no convidante. Não lê estoque mundial para oferecer vantagem onisciente. A autonomia declarada nos termos não tem parcela separada no cálculo; independência é o custo efetivo. Independência≥90 pode recusar mesmo com benefício maior. Fadiga≥85 ou HP<45 adiam antes da aceitação. Sem contato a decisão favorável permanece considering; termos ausentes impedem cálculo. Guardas/soldados sem arma sob risco≥0,6 podem condicionar ao equipamento. membership também bloqueia quem já possui qualquer organização.

### Aceites: 2 de 2 pares disponíveis

### NPC #325 / facção #1158 h24

Nora Vale #325; HP 100.0, fome 22.0, sede 48.0, fadiga 30.8; moedas 17; comida/água 1/0; posição 302:7,13; Goal answer_invitation/active

Personalidade na entrada: {"honesty":22,"compassion":66,"courage":29,"independence":76,"greed":74,"diligence":8,"family_loyalty":91,"persistence":84,"temperament":69,"vengefulness":67,"ambition":52,"sadism":0}.

| Need real na entrada | prioridade | status | alvo |
| --- | --- | --- | --- |
| affiliation | 57.60 | active | 1158 |
| water | 49.35 | active | — |
| advancement | 41.18 | selected | — |
| religious_interest | 40.13 | active | 5848 |
| food_reserve | 39.09 | active | — |
| rest | 30.80 | active | — |

| Need avaliada | alternativa | Utility | alvo | considerações normalizadas |
| --- | --- | --- | --- | --- |
| affiliation | answer_invitation | 65.00 | 1158 | {"base":0.325,"travel":-0.0} |
| advancement | work | 54.00 | — | {"base":0.25,"diligence":0.02,"physical_depletion":0.0,"travel":-0.0} |
| advancement | steal_person | 35.63 | 323 | {"base":0.31,"greed":0.14800000000000002,"honesty":-0.099,"authority":-0.2,"courage":0.014499999999999999,"travel":-0.0,"pressure_moral_tolerance":0.004661073209795919} |

Registro real antes {"status":"offered","created_at":23,"inviter":1155,"terms":{"benefits":{"protection":0,"food":12,"water":24,"income":1,"company":1,"training":0},"costs":{"dues":1,"risk":0.83,"autonomy":0.2},"reported_at":23,"source":1155}}; depois {"status":"accepted","created_at":23,"inviter":1155,"terms":{"benefits":{"protection":0,"food":12,"water":24,"income":1,"company":1,"training":0},"costs":{"dues":1,"risk":0.83,"autonomy":0.2},"reported_at":24,"source":1155},"last_contact":24,"evaluation":{"perceived_benefit":46.27,"perceived_cost":35.04},"accepted_at":24}; contatos [1155]; retorno [true,"Ingresso aceito com benefício percebido, custo e contato real."].

### NPC #2384 / facção #1158 h26

Mira Douran #2384; HP 100.0, fome 38.0, sede 7.0, fadiga 35.2; moedas 14; comida/água 2/0; posição 302:7,13; Goal answer_invitation/active

Personalidade na entrada: {"honesty":60,"compassion":70,"courage":49,"independence":9,"greed":66,"diligence":35,"family_loyalty":9,"persistence":91,"temperament":35,"vengefulness":73,"ambition":43,"sadism":0}.

| Need real na entrada | prioridade | status | alvo |
| --- | --- | --- | --- |
| affiliation | 55.60 | active | 1158 |
| religious_interest | 39.10 | active | 5848 |
| advancement | 37.33 | active | — |
| rest | 36.25 | active | — |
| food | 29.15 | active | — |

| Need avaliada | alternativa | Utility | alvo | considerações normalizadas |
| --- | --- | --- | --- | --- |
| affiliation | answer_invitation | 65.00 | 1158 | {"base":0.325,"travel":-0.0} |
| advancement | work | 67.50 | — | {"base":0.25,"diligence":0.0875,"physical_depletion":0.0,"travel":-0.0} |

Registro real antes {"status":"offered","created_at":26,"inviter":1155,"terms":{"benefits":{"protection":0,"food":12,"water":24,"income":1,"company":2,"training":0},"costs":{"dues":1,"risk":0.83,"autonomy":0.2},"reported_at":26,"source":1155}}; depois {"status":"accepted","created_at":26,"inviter":1155,"terms":{"benefits":{"protection":0,"food":12,"water":24,"income":1,"company":2,"training":0},"costs":{"dues":1,"risk":0.83,"autonomy":0.2},"reported_at":26,"source":1155},"last_contact":26,"evaluation":{"perceived_benefit":49.56,"perceived_cost":19.15},"accepted_at":26}; contatos [1155, 325]; retorno [true,"Ingresso aceito com benefício percebido, custo e contato real."].

### Recusas: 0 de 0 pares disponíveis

### Convites sem conclusão: 2 de 2 registros disponíveis

Facção Companhia de Ardor #1150; registro {"status":"offered","created_at":102,"inviter":1147,"terms":{"benefits":{"protection":0,"food":12,"water":24,"income":0,"company":1,"training":0},"costs":{"dues":1,"risk":0.71,"autonomy":0.2},"reported_at":102,"source":1147}}. Estado final: Elena Douran #1383; HP 9.0, fome 84.0, sede 41.0, fadiga 100.0; moedas 0; comida/água 0/1; posição 3:7,8; Goal steal/active. Avaliações efetivas retidas: 0; relação/benefício/custo só existem se constarem no registro, nenhum score hipotético foi calculado.

| Need atual | prioridade | status | fonte |
| --- | --- | --- | --- |
| food | 100 | selected | physiology |
| rest | 100 | active | physiology |
| recovery | 100 | active | own_physiology |
| money | 94.67 | active | economy |
| security | 93.70 | active | event:364915 |
| pursuit | 76.00 | active | event:272795 |
| response | 75.82 | active | event:332553 |

Facção Irmandade de Elimir #1158; registro {"status":"offered","created_at":292,"inviter":1155,"terms":{"benefits":{"protection":0,"food":12,"water":24,"income":0,"company":1,"training":0},"costs":{"dues":1,"risk":0.83,"autonomy":0.2},"reported_at":292,"source":1155}}. Estado final: Lyra Kars #2522; HP 10.0, fome 100.0, sede 41.0, fadiga 100.0; moedas 0; comida/água 0/2; posição 302:7,13; Goal fill_water/completed. Avaliações efetivas retidas: 0; relação/benefício/custo só existem se constarem no registro, nenhum score hipotético foi calculado.

| Need atual | prioridade | status | fonte |
| --- | --- | --- | --- |
| food | 100 | blocked | physiology |
| rest | 100 | selected | physiology |
| recovery | 100 | active | own_physiology |
| security | 95.54 | active | event:364201 |
| family | 92.46 | blocked | event:336904 |
| money | 83.66 | active | economy |
| pursuit | 82.57 | active | event:317972 |

## 7. Capacidade material e ação institucional

| Facção | membros / profissões | moedas | itens reais | HQ | Capabilities finais no mapa do líder | ações enumeradas | execuções / falhas |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Companhia de Ardor | 1 / {"caçador":1} | 0 | {"food":0,"water":0,"weapon":0,"tool":0,"grain":0} | Quartel-general de Mormar #1144 | {"patrol":false,"escort":false,"train":false,"produce":false,"store":true,"guard":false,"investigate":false,"trade":false,"recruit":true,"explore":false,"occupy":false} | {"calls":30,"institutional_supply":1} | {"store_supplies":1,"institutional_supply":1,"route_travel":19,"ask_route":6,"invite_person":4,"faction_prepare":1,"report_to_faction":1,"perform_assignment":1} / {"faction_prepare":1} |
| Irmandade de Elimir | 1 / {"caçador":1} | 0 | {"food":0,"water":0,"weapon":0,"tool":0,"grain":0} | Quartel-general de Silthon #1152 | {"patrol":false,"escort":false,"train":false,"produce":false,"store":true,"guard":false,"investigate":false,"trade":false,"recruit":true,"explore":false,"occupy":false} | {"calls":20,"institutional_support":1} | {"route_travel":1,"faction_prepare":1,"invite_person":5,"answer_invitation":2,"report_to_faction":1,"perform_assignment":1,"institutional_support":1,"attend_group":2} / {} |

| Facção | ActionPressure final e fontes | regra/status local |
| --- | --- | --- |
| Companhia de Ardor | {"value":26.76,"world":35,"failures":0,"last_failure":-1000,"updated_at":298,"source_facts":[],"reason":"purpose_outreach"} | {} |
| Irmandade de Elimir | {"value":20.82,"world":35,"failures":0,"last_failure":-1000,"updated_at":299,"source_facts":[],"reason":"purpose_outreach"} | {} |

| Facção | Estoque real na sede, distinto do inventário Faction |
| --- | --- |
| Companhia de Ardor | {"place":1144,"name":"Quartel-general de Mormar","food":12,"water":24} |
| Irmandade de Elimir | {"place":1152,"name":"Quartel-general de Silthon","food":12,"water":24} |

As duas sedes conservaram 12 comidas e 24 águas no encerramento, enquanto os inventários das facções e seus caixas estavam zerados. Há capacidade material no lugar, mas institutional_supply enumera somente estoque de Faction; retirar itens do ponto exige presença/acesso pelas ações espaciais existentes. As capacidades finais acima pertencem ao mapa do líder e a seus membros abastecidos, não à riqueza de todo o mundo.

| Líder | grupos atuais | Need organizational_survival final e contexto | última ação bem-sucedida |
| --- | --- | --- | --- |
| Aldren Hammer | [101035,169333] | [{"id":13724,"kind":"organizational_survival","priority":60.7321068,"base":50.704,"status":"active","target":1147,"source":"group:101035","reason":"Participar da organização conhecida","context":{"faction_id":1150,"group_id":101035}}] | {"action":"eat","turn":298} |
| John Ferros | [84586] | [{"id":19777,"kind":"organizational_survival","priority":57.022668,"base":48.328,"status":"active","target":2548,"source":"group:84586","reason":"Participar da organização conhecida","context":{"faction_id":1158,"group_id":84586}}] | {"action":"pursue","turn":299} |

Society.refresh reutiliza uma única Need organizational_survival: com grupo ativo, atualiza fonte/alvo e group_id para o primeiro grupo; no ramo elif organization_ids atribui contexto de facção. O ramo de grupo não apaga faction_id anterior. Os dois líderes terminaram com fonte de grupo e ambos os IDs no contexto. Society.candidates consulta faction_candidates antes do caminho coletivo; portanto esse contexto misto pode enumerar ações da facção sob uma Need descrita como participação no grupo. É mistura observada e localização causal no código, mas não se atribui a ela todo período de inatividade. Não há Need faccional independente garantida para cada vínculo. ActionPressure não substitui a enumeração/seleção.

Capabilities é predicado de meios atuais na localidade do avaliador: exige membros vivos, provisões carregadas e profissões específicas para vários serviços. Não é um contador de ações. invitation_info anuncia proteção, comida/água do estoque da facção e relatório de HQ, renda até quatro moedas, companhia e treinamento; renda anunciada não é promessa já paga nem salário automático. Capacidade de treinamento/produção/escolta não cria por si só handler natural equivalente. Estoque final não prova estoque no momento de cada convite; terms/reported_at é a evidência temporal do anúncio.

| hora | facção | NPC | efeito material | ilegal |
| --- | --- | --- | --- | --- |
| 6 | 1150 | 1147 | {"supplied":"food","recipient":1147,"item_id":1148} | False |

As ações institucionais acrescentadas oferecem apoio político, patrulha, compra, suprimento, roubo autorizado pelas normas e resposta à restrição. As contagens candidates_observed medem alternativas enumeradas por faction_candidates, antes da avaliação Utility; action_selected é seleção, action_executed é tentativa de execução, FactionAction é efeito bem-sucedido. Não são etapas intercambiáveis. O retorno antecipado de alternativas institucionais em Society.candidates pode impedir a enumeração das alternativas antigas report_to_faction/recruit_member/contribute nessa mesma chamada; isso é propriedade do código, não prova de que toda ausência de recrutamento tenha essa causa.

| Ação | seleções | tentativas de execução | retornos falhos |
| --- | --- | --- | --- |
| invite_person | 10 | 9 | 0 |
| recruit_member | 0 | 0 | 0 |
| request_membership | 0 | 0 | 0 |
| answer_invitation | 2 | 2 | 0 |
| institutional_support | 1 | 1 | 0 |
| institutional_patrol | 0 | 0 | 0 |
| institutional_purchase | 0 | 0 | 0 |
| institutional_supply | 1 | 1 | 0 |
| institutional_raid | 0 | 0 | 0 |
| institutional_response | 0 | 0 | 0 |
| contribute | 0 | 0 | 0 |
| perform_assignment | 2 | 2 | 0 |

## 8. Propostas: equivalência, apoio real e publicação

| Métrica | Resultado |
| --- | --- |
| Criadas / reutilizações | 47 / 29 |
| Status final | {"draft":31,"submitted":13,"partial":2,"accepted":1} |
| Pessoas únicas apoiadoras / com apoio entregue | 482 / 171 |
| Pares pessoa–proposta apoiados / entregues | 493 / 171 |
| Grupos apoiadores distintos | 75 |
| Eventos de apoio / entrega / submissão | 266 / 28 / 16 |

| Antiga / nova | jurisdição | setor / efeito / subject | nova h | antiga conhecida na criação? |
| --- | --- | --- | --- | --- |
| 54809 / 76724 | Silthon #162 | SECURITY / patrol / None | 39 | False |
| 54809 / 88878 | Silthon #162 | SECURITY / patrol / None | 48 | False |
| 56304 / 83099 | Sildor #50 | SECURITY / patrol / None | 44 | False |
| 56353 / 66690 | Normar #97 | SECURITY / patrol / None | 31 | False |
| 56353 / 273062 | Normar #97 | SECURITY / patrol / None | 206 | False |
| 56680 / 57354 | Normar #414 | SECURITY / patrol / None | 25 | False |
| 56680 / 116338 | Normar #414 | SECURITY / patrol / None | 72 | False |
| 56790 / 79497 | Elilen #583 | SECURITY / patrol / None | 41 | False |
| 56790 / 130344 | Elilen #583 | SECURITY / patrol / None | 85 | False |
| 57354 / 116338 | Normar #414 | SECURITY / patrol / None | 72 | False |
| 59140 / 64820 | Valvia #302 | SECURITY / patrol / None | 30 | False |
| 59274 / 151233 | Elimar #479 | SECURITY / patrol / None | 102 | False |
| 62703 / 161707 | Dorthon #846 | SECURITY / patrol / None | 112 | False |
| 62966 / 94322 | Dorria #1023 | SECURITY / patrol / None | 52 | False |
| 65434 / 121061 | Norven #349 | SECURITY / patrol / None | 76 | False |
| 66690 / 273062 | Normar #97 | SECURITY / patrol / None | 206 | False |
| 69431 / 209179 | Nordor #227 | SECURITY / patrol / None | 152 | False |
| 69431 / 221908 | Nordor #227 | SECURITY / patrol / None | 163 | False |
| 69800 / 147657 | Kardor #648 | SECURITY / patrol / None | 99 | False |
| 71157 / 83775 | Valmar #789 | SECURITY / patrol / None | 44 | False |
| 76724 / 88878 | Silthon #162 | SECURITY / patrol / None | 48 | False |
| 79497 / 130344 | Elilen #583 | SECURITY / patrol / None | 85 | False |
| 80192 / 244196 | Karlen #976 | SECURITY / patrol / None | 181 | False |
| 92654 / 98361 | Karvia #1088 | SECURITY / patrol / None | 54 | False |
| 95269 / 141147 | Valthon #742 | SECURITY / patrol / None | 95 | False |
| 123567 / 180530 | Elilen #695 | SECURITY / patrol / None | 128 | False |
| 123567 / 237203 | Elilen #695 | SECURITY / patrol / None | 175 | False |
| 180530 / 237203 | Elilen #695 | SECURITY / patrol / None | 175 | False |
| 188472 / 270472 | Sildor #911 | SECURITY / patrol / None | 203 | False |
| 209179 / 221908 | Nordor #227 | SECURITY / patrol / None | 163 | False |

Pares equivalentes que coexistiram sem conclusão/rejeição prévia conhecida: 30. O teste usa tempos de criação, decisões e conclusão observados; não chama propose novamente. Quando a amostra de criação mostra antiga ausente de known_after, o bloqueio de reutilização é conhecimento: o código somente reutiliza propostas conhecidas. Se a política antiga já acabou, uma nova proposta é um ciclo novo e foi excluída dessa contagem. Casos fora da amostra não permitem atribuir motivo individual exato. Rascunho não é automaticamente público: public_proposals só aprende a lista publicada no mercado, após submissão.

| Proposta | local / setor | criação | status | apoio / entregue | grupos | pública / recebida | política | última pressão |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 70260 | Dordor #3/SECURITY | 34 | draft | 9/0 | [30030,63401] | False/False | — | 35.33 |
| 56304 | Sildor #50/SECURITY | 24 | submitted | 9/4 | [32162,72901] | True/True | — | 54.50 |
| 83099 | Sildor #50/SECURITY | 44 | submitted | 3/2 | [81598] | True/True | — | 32.33 |
| 56353 | Normar #97/SECURITY | 24 | draft | 27/0 | [51756,27898] | False/False | — | 38.50 |
| 66690 | Normar #97/SECURITY | 31 | draft | 12/0 | [26364,37226] | False/False | — | 19.83 |
| 273062 | Normar #97/SECURITY | 206 | draft | 3/0 | [165742] | False/False | — | 18.50 |
| 287454 | Normar #97/SECURITY | 218 | draft | 2/0 | [224162] | False/False | — | 21.50 |
| 54809 | Silthon #162/SECURITY | 23 | draft | 4/0 | [48866] | False/False | — | 38.50 |
| 76724 | Silthon #162/SECURITY | 39 | submitted | 23/15 | [73023,74274,56421] | True/True | — | 76.50 |
| 88878 | Silthon #162/SECURITY | 48 | submitted | 6/6 | [87181] | True/True | — | 58.50 |
| 69431 | Nordor #227/SECURITY | 33 | draft | 7/0 | [32339,68203] | False/False | — | 38.50 |
| 209179 | Nordor #227/SECURITY | 152 | draft | 7/0 | [61884,165815] | False/False | — | 28.33 |
| 221908 | Nordor #227/SECURITY | 163 | draft | 2/0 | [80463] | False/False | — | 18.50 |
| 274255 | Nordor #227/FOOD | 207 | draft | 2/0 | [211333] | False/False | — | 15.07 |
| 59140 | Valvia #302/SECURITY | 26 | draft | 11/0 | [20728,63767,28103] | False/False | — | 29.17 |
| 64820 | Valvia #302/SECURITY | 30 | draft | 29/2 | [59875,30183] | False/False | — | 25.33 |
| 65434 | Norven #349/SECURITY | 30 | partial | 20/7 | [63807,74469] | True/True | 306439 | 60.50 |
| 121061 | Norven #349/SECURITY | 76 | draft | 9/0 | [85970,14598] | False/False | — | 24.50 |
| 56680 | Normar #414/SECURITY | 24 | draft | 11/0 | [52140] | False/False | — | 34.67 |
| 57354 | Normar #414/SECURITY | 25 | draft | 9/0 | [53048,187742] | False/False | — | 38.50 |
| 116338 | Normar #414/SECURITY | 72 | draft | 9/0 | [52198,224807] | False/False | — | 38.50 |
| 59274 | Elimar #479/SECURITY | 26 | submitted | 13/6 | [21102,62320,67003] | True/True | — | 58.50 |
| 151233 | Elimar #479/SECURITY | 102 | submitted | 7/2 | [147394,186701] | True/True | — | 43.17 |
| 56790 | Elilen #583/SECURITY | 24 | submitted | 31/30 | [52318,49193] | True/True | — | 92.17 |
| 79497 | Elilen #583/SECURITY | 41 | submitted | 6/5 | [75900] | True/True | — | 54.50 |
| 130344 | Elilen #583/SECURITY | 85 | draft | 6/0 | [129403,182894] | False/False | — | 38.50 |
| 310263 | Elilen #583/WATER | 238 | draft | 6/0 | [86186] | False/False | — | 34.99 |
| 69800 | Kardor #648/SECURITY | 33 | draft | 21/0 | [65742,112883,50815] | False/False | — | 38.50 |
| 147657 | Kardor #648/SECURITY | 99 | draft | 3/0 | [37842] | False/False | — | 18.50 |
| 123567 | Elilen #695/SECURITY | 78 | submitted | 12/4 | [53894] | True/True | — | 54.50 |
| 180530 | Elilen #695/SECURITY | 128 | draft | 6/0 | [50877] | False/False | — | 20.50 |
| 237203 | Elilen #695/SECURITY | 175 | draft | 6/0 | [144830,234257] | False/False | — | 23.50 |
| 95269 | Valthon #742/SECURITY | 52 | draft | 8/0 | [93737] | False/False | — | 38.50 |
| 141147 | Valthon #742/SECURITY | 95 | draft | 15/0 | [46686] | False/False | — | 38.50 |
| 71157 | Valmar #789/SECURITY | 34 | draft | 5/0 | [34735] | False/False | — | 18.50 |
| 83775 | Valmar #789/SECURITY | 44 | partial | 15/11 | [82405,217420] | True/True | 138300 | 68.50 |
| 62703 | Dorthon #846/SECURITY | 28 | submitted | 29/29 | [21951] | True/True | — | 88.33 |
| 161707 | Dorthon #846/SECURITY | 112 | draft | 7/0 | [34847] | False/False | — | 38.50 |
| 188472 | Sildor #911/SECURITY | 136 | draft | 11/0 | [70389] | False/False | — | 19.83 |
| 270472 | Sildor #911/SECURITY | 203 | draft | 4/0 | [49616] | False/False | — | 18.50 |
| 80192 | Karlen #976/SECURITY | 42 | accepted | 19/18 | [46771,51135] | True/True | 146540 | 73.17 |
| 244196 | Karlen #976/SECURITY | 181 | draft | 6/0 | [40134] | False/False | — | 18.50 |
| 364780 | Karlen #976/FOOD | 288 | draft | 2/0 | [313168] | False/False | — | 16.38 |
| 62966 | Dorria #1023/SECURITY | 28 | draft | 4/0 | [54259] | False/False | — | 18.67 |
| 94322 | Dorria #1023/SECURITY | 52 | submitted | 9/7 | [90047,201892] | True/True | — | 56.17 |
| 92654 | Karvia #1088/SECURITY | 50 | submitted | 20/15 | [91163,106926,33677] | True/True | — | 76.50 |
| 98361 | Karvia #1088/SECURITY | 54 | submitted | 8/8 | [94121] | True/True | — | 62.50 |

## 9. Funil político por entidades e tempos entre etapas

| Etapa | entidades únicas | eventos |
| --- | --- | --- |
| ProposalCreated | 47 | 47 |
| Support | 47 | 266 |
| SupportDelivered | 16 | 28 |
| Submitted | 16 | 16 |
| Decision | 3 | 3 |
| PolicyCreated | 3 | 3 |
| Work/Effect | 1 | 3 |
| Completion | 0 | 0 |

| Intervalo (h) | n | média | mediana | p90 (n≥10) | máximo |
| --- | --- | --- | --- | --- | --- |
| criação → primeiro apoio | 47 | 0 | 0.00 | 0.00 | 0 |
| criação → primeira entrega | 16 | 56.56 | 19.50 | 149.00 | 195 |
| primeira entrega → primeira decisão | 3 | 101.33 | 53.00 | amostra pequena | 204 |
| primeira decisão → política vinculada | 3 | 0 | 0.00 | amostra pequena | 0 |
| política → primeiro trabalho | 1 | 92 | 92.00 | amostra pequena | 92 |
| primeiro trabalho → conclusão | 0 | — | — | amostra pequena | — |

Apoio pode ser registrado no próprio propose, gerando intervalo zero legítimo. Essas distribuições incluem apenas etapas concluídas; rascunhos/políticas pendentes têm duração censurada na hora 300 e não foram convertidos em latências concluídas. Uma política pode ser reutilizada por mais de uma proposta; identificadores foram deduplicados no funil de políticas.

## 9.1 Rascunhos e representantes

Proposta #54809 (Silthon #162, SECURITY), criada h23, idade 277h, apoio 4, entregue 0, recebida=False. Representante: Silas Alvor #2135; HP 100.0, fome 45.0, sede 17.0, fadiga 51.0; moedas 0; comida/água 0/0; posição 162:5,9; Goal drink/completed. Mercado: caminho local de 0 passos (None = outro mapa/sem caminho/dado ausente, não prova de rota interlocal impossível). Prefeito: Elena Alvor #2022; HP 12.0, fome 56.0, sede 15.0, fadiga 91.6; moedas 1; comida/água 0/0; posição 162:2,3; Goal work/active.

Needs atuais [{"id":50380,"kind":"organizational_survival","priority":72.35035399999998,"base":57.165,"status":"blocked","target":2135,"source":"group:48866","reason":"Participar da organização conhecida","context":{"group_id":48866}},{"id":152144,"kind":"money","priority":71.381,"base":58.125,"status":"blocked","target":null,"source":"economy","reason":"Estabilizar renda baixa persistente","context":{}},{"id":45481,"kind":"protection","priority":70.55700000000002,"base":45,"status":"blocked","target":2135,"source":"event:371159","reason":"Crime conhecido ameaça segurança pessoal/familiar","context":{"diagnostic":{"reason":"NoViableSolution","competing":null,"turn":298}}},{"id":314776,"kind":"response","priority":69.05700000000002,"base":55,"status":"blocked","target":26,"source":"event:336833","reason":"Responder à procura institucional conhecida","context":{}},{"id":17347,"kind":"food_reserve","priority":69.0,"base":41.0,"status":"blocked","target":null,"source":"food_reserve","reason":"Manter cobertura alimentar pessoal","context":{}},{"id":48862,"kind":"migration","priority":61.656,"base":52,"status":"blocked","target":3,"source":"known_towns","reason":"Considerar mudança por threat","context":{}}]; grupos [48866, 87181, 128121]; compromissos [{"id":105386,"status":"paused","target":null,"reason":null},{"id":311044,"status":"paused","target":2135,"reason":null}]; viagem —; última ação bem-sucedida {"action":"drink","turn":298}.

Proposta #56353 (Normar #97, SECURITY), criada h24, idade 276h, apoio 27, entregue 0, recebida=False. Representante: Ruan Douran #1789; HP 92.0, fome 72.0, sede 15.0, fadiga 100.0; moedas 0; comida/água 0/0; posição 97:5,5; Goal sleep/active. Mercado: caminho local de 4 passos (None = outro mapa/sem caminho/dado ausente, não prova de rota interlocal impossível). Prefeito: Arthus Corven #1686; HP 100.0, fome 60.0, sede 60.0, fadiga 58.0; moedas 12; comida/água 0/2; posição 97:1,9; Goal fill_water/completed.

Needs atuais [{"id":13983,"kind":"food","priority":100,"base":85.0,"status":"active","target":null,"source":"physiology","reason":"Fome","context":{"emergency":false}},{"id":37189,"kind":"rest","priority":100,"base":100,"status":"selected","target":null,"source":"physiology","reason":"Cansaço","context":{}},{"id":13982,"kind":"food_reserve","priority":81.35483870967742,"base":41.0,"status":"active","target":null,"source":"food_reserve","reason":"Manter cobertura alimentar pessoal","context":{}},{"id":300562,"kind":"response","priority":77.89911710106229,"base":55,"status":"active","target":120,"source":"event:300561","reason":"Responder à procura institucional conhecida","context":{}},{"id":322902,"kind":"response","priority":77.34,"base":55,"status":"active","target":1717,"source":"event:322901","reason":"Responder à procura institucional conhecida","context":{}},{"id":47072,"kind":"protection","priority":73.14,"base":45,"status":"active","target":1789,"source":"event:372297","reason":"Crime conhecido ameaça segurança pessoal/familiar","context":{"diagnostic":{"reason":"LostToHigherPriority","competing":"rest","turn":299}}}]; grupos [51756]; compromissos [{"id":147041,"status":"paused","target":null,"reason":null}]; viagem —; última ação bem-sucedida {"action":"drink","turn":295}.

Proposta #56680 (Normar #414, SECURITY), criada h24, idade 276h, apoio 11, entregue 0, recebida=False. Representante: Arthus Douran #3043; HP 54.0, fome 76.0, sede 60.0, fadiga 92.8; moedas 0; comida/água 0/1; posição 414:5,3; Goal sleep/active. Mercado: caminho local de 6 passos (None = outro mapa/sem caminho/dado ausente, não prova de rota interlocal impossível). Prefeito: Iria Douran #429; HP 100.0, fome 46.0, sede 15.0, fadiga 91.6; moedas 0; comida/água 2/1; posição 414:1,9; Goal drink/completed.

Needs atuais [{"id":14715,"kind":"food","priority":100,"base":88.0,"status":"active","target":null,"source":"physiology","reason":"Fome","context":{"emergency":false}},{"id":37580,"kind":"rest","priority":98.40000000000006,"base":90.40000000000006,"status":"selected","target":null,"source":"physiology","reason":"Cansaço","context":{}},{"id":14716,"kind":"money","priority":88.864,"base":69,"status":"active","target":null,"source":"economy","reason":"Estabilizar renda baixa persistente","context":{}},{"id":52137,"kind":"political_pressure","priority":85.55366666666666,"base":72.51666666666667,"status":"active","target":null,"source":"own_shared_problem","reason":"Buscar representação para problema pessoal","context":{"cause":"resource_pressure"}},{"id":14714,"kind":"food_reserve","priority":80.81935483870967,"base":41.0,"status":"active","target":null,"source":"food_reserve","reason":"Manter cobertura alimentar pessoal","context":{}},{"id":52132,"kind":"protection","priority":78.208,"base":45,"status":"active","target":3043,"source":"event:366531","reason":"Crime conhecido ameaça segurança pessoal/familiar","context":{"diagnostic":{"reason":"LostToHigherPriority","competing":"rest","turn":298}}}]; grupos [52140]; compromissos [{"id":80689,"status":"paused","target":null,"reason":null}]; viagem —; última ação bem-sucedida {"action":"eat","turn":292}.

Proposta #57354 (Normar #414, SECURITY), criada h25, idade 275h, apoio 9, entregue 0, recebida=False. Representante: Ruan Solaris #452; HP 100.0, fome 32.0, sede 60.0, fadiga 100.0; moedas 1; comida/água 0/0; posição 414:5,9; Goal denounce/failed. Mercado: caminho local de 0 passos (None = outro mapa/sem caminho/dado ausente, não prova de rota interlocal impossível). Prefeito: Iria Douran #429; HP 100.0, fome 46.0, sede 15.0, fadiga 91.6; moedas 0; comida/água 2/1; posição 414:1,9; Goal drink/completed.

Needs atuais [{"id":28847,"kind":"rest","priority":100,"base":100,"status":"blocked","target":null,"source":"physiology","reason":"Cansaço","context":{}},{"id":38441,"kind":"money","priority":77.61,"base":59.75,"status":"blocked","target":null,"source":"economy","reason":"Estabilizar renda baixa persistente","context":{}},{"id":38443,"kind":"migration","priority":65.37371,"base":52,"status":"blocked","target":414,"source":"known_towns","reason":"Considerar mudança por threat","context":{}},{"id":28855,"kind":"protection","priority":61.7,"base":45,"status":"active","target":452,"source":"event:373239","reason":"Crime conhecido ameaça segurança pessoal/familiar","context":{"diagnostic":{"reason":"Selected","competing":null,"turn":295}}},{"id":61318,"kind":"family","priority":61.062000000000005,"base":38.0,"status":"blocked","target":449,"source":"event:323754","reason":"Ausência percebida após encontros anteriores","context":{"mode":"missing","diagnostic":{"reason":"LostToHigherPriority","competing":"protection","turn":295}}},{"id":346729,"kind":"response","priority":58.6,"base":55,"status":"active","target":2988,"source":"event:346728","reason":"Responder à procura institucional conhecida","context":{}}]; grupos [53048]; compromissos [{"id":310753,"status":"paused","target":452,"reason":null},{"id":315650,"status":"paused","target":414,"reason":null}]; viagem —; última ação bem-sucedida {"action":"eat","turn":292}.

Proposta #59140 (Valvia #302, SECURITY), criada h26, idade 274h, apoio 11, entregue 0, recebida=False. Representante: Darin Hammer #2664; HP 100.0, fome 75.0, sede 60.0, fadiga 73.2; moedas 1; comida/água 1/0; posição 331:3,5; Goal buy_food/completed. Mercado: caminho local de None passos (None = outro mapa/sem caminho/dado ausente, não prova de rota interlocal impossível). Prefeito: Nora Arven #2485; HP 0.0, fome 100.0, sede 15.0, fadiga 100.0; moedas 4; comida/água 0/1; posição 302:7,11; Goal sleep/failed.

Needs atuais [{"id":20720,"kind":"food","priority":100,"base":89.5,"status":"selected","target":null,"source":"physiology","reason":"Fome","context":{"emergency":false}},{"id":30857,"kind":"rest","priority":80.00000000000041,"base":72.00000000000041,"status":"active","target":null,"source":"physiology","reason":"Cansaço","context":{}},{"id":45605,"kind":"food_reserve","priority":76.91666666666667,"base":41.0,"status":"active","target":null,"source":"food_reserve","reason":"Manter cobertura alimentar pessoal","context":{}},{"id":20721,"kind":"money","priority":75.908,"base":56,"status":"active","target":null,"source":"economy","reason":"Estabilizar renda baixa persistente","context":{}},{"id":20725,"kind":"political_pressure","priority":72.10594,"base":58.175,"status":"active","target":null,"source":"own_shared_problem","reason":"Buscar representação para problema pessoal","context":{"cause":"resource_pressure"}},{"id":26642,"kind":"organizational_survival","priority":68.4068,"base":56.813,"status":"active","target":2664,"source":"group:20728","reason":"Participar da organização conhecida","context":{"group_id":20728}}]; grupos [20728]; compromissos [{"id":83371,"status":"paused","target":null,"reason":null},{"id":294414,"status":"paused","target":null,"reason":null}]; viagem —; última ação bem-sucedida {"action":"buy_food","turn":299}.

Proposta #62966 (Dorria #1023, SECURITY), criada h28, idade 272h, apoio 4, entregue 0, recebida=False. Representante: Lyra Arven #5567; HP 100.0, fome 78.0, sede 60.0, fadiga 74.0; moedas 1; comida/água 1/1; posição 1052:1,5; Goal forage/completed. Mercado: caminho local de None passos (None = outro mapa/sem caminho/dado ausente, não prova de rota interlocal impossível). Prefeito: Elena Valerius #1041; HP 61.0, fome 72.0, sede 65.0, fadiga 82.0; moedas 0; comida/água 2/2; posição 1023:1,9; Goal work_for_food/completed.

Needs atuais [{"id":19120,"kind":"food","priority":100,"base":91.0,"status":"selected","target":null,"source":"physiology","reason":"Fome","context":{"emergency":false}},{"id":67615,"kind":"family","priority":96.23044571428571,"base":64.0,"status":"blocked","target":5570,"source":"event:327886","reason":"Privação de familiar percebida em encontro","context":{"mode":"care","diagnostic":{"reason":"NoViableSolution","competing":null,"turn":298}}},{"id":35038,"kind":"political_pressure","priority":81.47989571428573,"base":65.4,"status":"active","target":null,"source":"own_shared_problem","reason":"Buscar representação para problema pessoal","context":{"cause":"resource_pressure"}},{"id":35035,"kind":"rest","priority":79.6000000000007,"base":71.6000000000007,"status":"active","target":null,"source":"physiology","reason":"Cansaço","context":{}},{"id":78605,"kind":"money","priority":78.77,"base":64.75,"status":"active","target":null,"source":"economy","reason":"Estabilizar renda baixa persistente","context":{}},{"id":99631,"kind":"family","priority":75.07538571428572,"base":52.599999999999994,"status":"active","target":5564,"source":"event:327885","reason":"Privação de familiar percebida em encontro","context":{"mode":"care","diagnostic":{"reason":"LostToHigherPriority","competing":"food","turn":298}}}]; grupos []; compromissos [{"id":317847,"status":"paused","target":null,"reason":null},{"id":327887,"status":"paused","target":5570,"reason":null}]; viagem —; última ação bem-sucedida {"action":"forage","turn":298}.

## 9.2 Recebidas e ainda sem decisão conclusiva

Proposta #56304, submitted, recebida=True, última pressão 54.50; prefeito: Elena Corven #1608; HP 21.0, fome 82.0, sede 15.0, fadiga 90.4; moedas 0; comida/água 0/0; posição 50:2,2; Goal drink/completed; caminho local ao mercado 10; representante 1666. Needs do prefeito [{"id":40699,"kind":"food","priority":100,"base":100,"status":"selected","target":null,"source":"physiology","reason":"Fome","context":{"emergency":true}},{"id":50217,"kind":"rest","priority":97.2,"base":89.2,"status":"active","target":null,"source":"physiology","reason":"Cansaço","context":{}},{"id":149603,"kind":"money","priority":94.726,"base":64.25,"status":"active","target":null,"source":"economy","reason":"Estabilizar renda baixa persistente","context":{}},{"id":186370,"kind":"recovery","priority":92.0,"base":84,"status":"active","target":1608,"source":"own_physiology","reason":"Recuperar condição física após dano","context":{}},{"id":63456,"kind":"political_pressure","priority":78.63296666666668,"base":67.25,"status":"active","target":null,"source":"own_shared_problem","reason":"Buscar representação para problema pessoal","context":{"cause":"resource_pressure"}},{"id":308693,"kind":"response","priority":77.04400000000001,"base":55,"status":"active","target":91,"source":"event:308692","reason":"Responder à procura institucional conhecida","context":{}}]; viagem —; compromissos []; última ação {"action":"drink","turn":299}.

Proposta #56790, submitted, recebida=True, última pressão 92.17; prefeito: Ruan Vale #3590; HP 10.0, fome 98.0, sede 80.0, fadiga 100.0; moedas 3; comida/água 0/1; posição 583:4,13; Goal buy_meal/active; caminho local ao mercado 3; representante 3538. Needs do prefeito [{"id":18085,"kind":"food","priority":100,"base":100,"status":"selected","target":null,"source":"physiology","reason":"Fome","context":{"emergency":true}},{"id":44508,"kind":"rest","priority":100,"base":100,"status":"active","target":null,"source":"physiology","reason":"Cansaço","context":{}},{"id":171275,"kind":"recovery","priority":100,"base":95,"status":"active","target":3590,"source":"own_physiology","reason":"Recuperar condição física após dano","context":{}},{"id":58046,"kind":"political_pressure","priority":93.1802,"base":80,"status":"active","target":null,"source":"own_shared_problem","reason":"Buscar representação para problema pessoal","context":{"cause":"water_access"}},{"id":39489,"kind":"water","priority":85.35,"base":78,"status":"active","target":null,"source":"physiology","reason":"Sede","context":{"emergency":false}},{"id":178403,"kind":"money","priority":76.76833333333333,"base":51.208333333333336,"status":"active","target":null,"source":"economy","reason":"Estabilizar renda baixa persistente","context":{}}]; viagem —; compromissos []; última ação {"action":"sleep","turn":286}.

Proposta #59274, submitted, recebida=True, última pressão 58.50; prefeito: Ruan Alvor #488; HP 90.0, fome 66.0, sede 15.0, fadiga 80.8; moedas 3; comida/água 0/0; posição 479:5,8; Goal sleep/active; caminho local ao mercado 1; representante 3297. Needs do prefeito [{"id":48406,"kind":"rest","priority":87.60000000000021,"base":79.60000000000021,"status":"selected","target":null,"source":"physiology","reason":"Cansaço","context":{}},{"id":16437,"kind":"food","priority":81.55,"base":76.0,"status":"active","target":null,"source":"physiology","reason":"Fome","context":{"emergency":false}},{"id":60635,"kind":"protection","priority":78.18910510037982,"base":45,"status":"active","target":488,"source":"event:375886","reason":"Crime conhecido ameaça segurança pessoal/familiar","context":{"diagnostic":{"reason":"LostToHigherPriority","competing":"rest","turn":299}}},{"id":61328,"kind":"political_pressure","priority":77.62732952380954,"base":62.45,"status":"active","target":null,"source":"own_shared_problem","reason":"Buscar representação para problema pessoal","context":{"cause":"resource_pressure"}},{"id":16444,"kind":"governance","priority":76.0829142857143,"base":62.0,"status":"active","target":488,"source":"received_proposals","reason":"Responder a proposta formal recebida","context":{"mode":"received_proposal","proposal_id":59274}},{"id":283890,"kind":"money","priority":75.444,"base":52.5,"status":"active","target":null,"source":"economy","reason":"Estabilizar renda baixa persistente","context":{}}]; viagem —; compromissos [{"id":146769,"status":"paused","target":null,"reason":null},{"id":214379,"status":"paused","target":3236,"reason":null},{"id":239642,"status":"paused","target":302,"reason":null}]; última ação {"action":"drink","turn":298}.

Proposta #62703, submitted, recebida=True, última pressão 88.33; prefeito: Lyra Arven #4770; HP 26.0, fome 74.0, sede 46.0, fadiga 100.0; moedas 1; comida/água 0/1; posição 846:1,8; Goal sleep/active; caminho local ao mercado 11; representante 4681. Needs do prefeito [{"id":22016,"kind":"food","priority":100,"base":88.0,"status":"active","target":null,"source":"physiology","reason":"Fome","context":{"emergency":false}},{"id":36425,"kind":"rest","priority":100,"base":100,"status":"selected","target":null,"source":"physiology","reason":"Cansaço","context":{}},{"id":134650,"kind":"money","priority":87.76599999999999,"base":56.75,"status":"active","target":null,"source":"economy","reason":"Estabilizar renda baixa persistente","context":{}},{"id":200287,"kind":"recovery","priority":87.0,"base":79,"status":"active","target":4770,"source":"own_physiology","reason":"Recuperar condição física após dano","context":{}},{"id":22015,"kind":"food_reserve","priority":85,"base":41.0,"status":"active","target":null,"source":"food_reserve","reason":"Manter cobertura alimentar pessoal","context":{}},{"id":258742,"kind":"grief","priority":75.69102857142856,"base":55.0,"status":"active","target":4773,"source":"event:258741","reason":"Morte conhecida de Bela Arven","context":{"diagnostic":{"reason":"LostToHigherPriority","competing":"rest","turn":299}}}]; viagem —; compromissos [{"id":93839,"status":"paused","target":null,"reason":null}]; última ação {"action":"drink","turn":294}.

Proposta #76724, submitted, recebida=True, última pressão 76.50; prefeito: Elena Alvor #2022; HP 12.0, fome 56.0, sede 15.0, fadiga 91.6; moedas 1; comida/água 0/0; posição 162:2,3; Goal work/active; caminho local ao mercado 9; representante 1999. Needs do prefeito [{"id":182105,"kind":"recovery","priority":100,"base":93,"status":"selected","target":2022,"source":"own_physiology","reason":"Recuperar condição física após dano","context":{}},{"id":35614,"kind":"rest","priority":98.4,"base":90.4,"status":"active","target":null,"source":"physiology","reason":"Cansaço","context":{}},{"id":26396,"kind":"money","priority":93.32400000000001,"base":63,"status":"active","target":null,"source":"economy","reason":"Estabilizar renda baixa persistente","context":{}},{"id":47160,"kind":"political_pressure","priority":78.27516666666666,"base":66.3,"status":"active","target":null,"source":"own_shared_problem","reason":"Buscar representação para problema pessoal","context":{"cause":"resource_pressure"}},{"id":47126,"kind":"protection","priority":76.52,"base":45,"status":"active","target":2022,"source":"event:362821","reason":"Crime conhecido ameaça segurança pessoal/familiar","context":{"diagnostic":{"reason":"LostToHigherPriority","competing":"recovery","turn":299}}},{"id":26399,"kind":"governance","priority":73.535,"base":62.0,"status":"active","target":2022,"source":"received_proposals","reason":"Responder a proposta formal recebida","context":{"proposal_id":76724,"mode":"received_proposal"}}]; viagem —; compromissos []; última ação {"action":"drink","turn":298}.

Proposta #79497, submitted, recebida=True, última pressão 54.50; prefeito: Ruan Vale #3590; HP 10.0, fome 98.0, sede 80.0, fadiga 100.0; moedas 3; comida/água 0/1; posição 583:4,13; Goal buy_meal/active; caminho local ao mercado 3; representante 3840. Needs do prefeito [{"id":18085,"kind":"food","priority":100,"base":100,"status":"selected","target":null,"source":"physiology","reason":"Fome","context":{"emergency":true}},{"id":44508,"kind":"rest","priority":100,"base":100,"status":"active","target":null,"source":"physiology","reason":"Cansaço","context":{}},{"id":171275,"kind":"recovery","priority":100,"base":95,"status":"active","target":3590,"source":"own_physiology","reason":"Recuperar condição física após dano","context":{}},{"id":58046,"kind":"political_pressure","priority":93.1802,"base":80,"status":"active","target":null,"source":"own_shared_problem","reason":"Buscar representação para problema pessoal","context":{"cause":"water_access"}},{"id":39489,"kind":"water","priority":85.35,"base":78,"status":"active","target":null,"source":"physiology","reason":"Sede","context":{"emergency":false}},{"id":178403,"kind":"money","priority":76.76833333333333,"base":51.208333333333336,"status":"active","target":null,"source":"economy","reason":"Estabilizar renda baixa persistente","context":{}}]; viagem —; compromissos []; última ação {"action":"sleep","turn":286}.

Estados finais explicam indisponibilidade naquele instante; não bastam para provar cada hora de espera anterior. O código exige encontro entre líder de grupo apoiador e prefeito no mercado para submit; resolve exige prefeito no mercado e proposta recebida. Não existe decisão automática só porque a pressão chegou a 100.

## 10. Pressão política e decisão da autoridade

```python
def pressure(self,prop,p=None):
    t=self.w.towns[prop.town_id]
    age=min(20,(self.w.turn-prop.created_at)/6)
    visibility=10 if prop.id in t.office.get('known_proposals',[]) else 2
    crisis=10 if t.economic_report.get('deficit',0) or prop.urgency>=70 else 0
    living=sum(self.w.characters[i].alive for i in prop.delivered_supporter_ids)
    value=min(100,living*2+prop.urgency*.3+age+visibility+crisis)
    previous=prop.pressure;prop.pressure=value
    prop.pressure_state={'unique_support':living,'severity':prop.urgency,'persistence':age,'visibility':visibility,'local_crisis':crisis,'affected_localities':list(prop.affected_locality_ids)}
    if p and abs(previous-value)>=2:self.emit('PoliticalPressureChanged',p,prop.id,proposal_id=prop.id,previous=previous,pressure=value,factors=prop.pressure_state)
    return value
```

living conta somente apoiadores ENTREGUES e ainda vivos. affected_localities é armazenado, mas não acrescenta bônus numérico na fórmula. Severidade vem de urgency, que acumula o máximo registrado. A visibilidade é dois antes do recebimento e dez depois. Pressão não equivale a consentimento global e pode cair quando apoiadores morrem.

| Conjunto | distribuição da última pressão armazenada |
| --- | --- |
| Com apoio entregue | {"n":16,"min":32.33333333333333,"p25":54.5,"median":59.5,"mean":63.1458,"p75":74.0,"p90":82.4167,"max":92.16666666666667} |
| Entregues e decididas | {"n":3,"min":60.5,"p25":64.5,"median":68.5,"mean":67.3889,"p75":70.8333,"p90":72.2333,"max":73.16666666666666} |
| Entregues e nunca decididas | {"n":13,"min":32.33333333333333,"p25":54.5,"median":58.5,"mean":62.1667,"p75":76.5,"p90":85.9667,"max":92.16666666666667} |

São valores finais armazenados de propostas entregues, não necessariamente pressão no instante da primeira entrega. O rastreio de PoliticalPressureChanged só registra variações ≥2; não conserva todo cálculo intermediário. A distribuição de decisão abaixo usa valores efetivamente calculados no ato, sem essa ambiguidade.

```python
def decision_scores(self,p,prop):
    t=self.w.towns[prop.town_id];pressure=self.pressure(prop)
    cost=25 if t.money<8 else 5
    # Sem capacidade material ou sob exaustão, uma demanda de baixa pressão
    # pode ser deixada sem encaminhamento. A alternativa não é dominada
    # matematicamente pela recusa em todos os contextos.
    avoid=(25 if t.money<2 and pressure<45 else 0)+(30 if p.fatigue>=85 and pressure<45 else 0)
    return {'approve':pressure*.55+p.personality.compassion*.3+p.personality.diligence*.15-cost-p.personality.greed*.15,
            'partial':22+pressure*.35+p.personality.diligence*.25-cost*.4,
            'reject':18+p.personality.greed*.45+p.personality.independence*.1-pressure*.15,
            'defer':25+p.personality.persistence*.2+cost*.6-pressure*.2,
            'ignore':p.personality.independence*.25+p.personality.greed*.25-pressure*.35+avoid}
```

Decisão calculada h92, proposta #83775: Ruan Ferros #4522; HP 100.0, fome 46.0, sede 49.0, fadiga 31.4; moedas 19; comida/água 0/1; posição 789:5,9; Goal review_proposal/active. Personalidade {"honesty":67,"compassion":7,"courage":60,"independence":83,"greed":70,"diligence":90,"family_loyalty":33,"persistence":73,"temperament":85,"vengefulness":67,"ambition":93,"sadism":92}; crise/fatores {"unique_support":7,"severity":55.0,"persistence":8.0,"visibility":10,"local_crisis":0,"affected_localities":[789]}; pressão 48.5; tesouro 1265; cost=5; avoid=0; scores {"approve":26.775000000000006,"partial":59.474999999999994,"reject":50.525,"defer":32.9,"ignore":21.275000000000002}; máximo=partial. Resultado do evento da mesma hora: {"decision":"partial","scores":{"approve":26.775000000000006,"partial":59.474999999999994,"reject":50.525,"defer":32.9,"ignore":21.275000000000002},"reason":"pressure_personality_and_material_budget","political_pressure":48.5,"policy_id":138300,"material":{"food":0,"money":0,"recipients":[]}}.

Decisão calculada h98, proposta #80192: Marie Alvor #5299; HP 100.0, fome 49.0, sede 61.0, fadiga 57.6; moedas 6; comida/água 0/1; posição 976:5,9; Goal review_proposal/active. Personalidade {"honesty":83,"compassion":74,"courage":29,"independence":17,"greed":6,"diligence":84,"family_loyalty":65,"persistence":52,"temperament":91,"vengefulness":33,"ambition":56,"sadism":0}; crise/fatores {"unique_support":18,"severity":55.0,"persistence":9.333333333333334,"visibility":10,"local_crisis":0,"affected_localities":[976]}; pressão 71.83333333333334; tesouro 1913; cost=5; avoid=0; scores {"approve":68.40833333333333,"partial":66.14166666666667,"reject":11.624999999999998,"defer":24.03333333333333,"ignore":-19.39166666666667}; máximo=approve. Resultado do evento da mesma hora: {"decision":"approve","scores":{"approve":68.40833333333333,"partial":66.14166666666667,"reject":11.624999999999998,"defer":24.03333333333333,"ignore":-19.39166666666667},"reason":"pressure_personality_and_material_budget","political_pressure":71.83333333333334,"policy_id":146540,"material":{"food":0,"money":0,"recipients":[]}}.

Decisão calculada h235, proposta #65434: Lyra Corven #2747; HP 78.0, fome 66.0, sede 65.0, fadiga 56.8; moedas 6; comida/água 0/0; posição 349:5,9; Goal review_proposal/active. Personalidade {"honesty":90,"compassion":53,"courage":28,"independence":23,"greed":13,"diligence":90,"family_loyalty":35,"persistence":67,"temperament":33,"vengefulness":41,"ambition":85,"sadism":0}; crise/fatores {"unique_support":7,"severity":55.0,"persistence":20,"visibility":10,"local_crisis":0,"affected_localities":[349]}; pressão 60.5; tesouro 1959; cost=5; avoid=0; scores {"approve":55.725,"partial":63.675,"reject":17.075000000000003,"defer":29.299999999999997,"ignore":-12.174999999999997}; máximo=partial. Resultado do evento da mesma hora: {"decision":"partial","scores":{"approve":55.725,"partial":63.675,"reject":17.075000000000003,"defer":29.299999999999997,"ignore":-12.174999999999997},"reason":"pressure_personality_and_material_budget","political_pressure":60.5,"policy_id":306439,"material":{"food":0,"money":0,"recipients":[]}}.

approve/partial com orçamento insuficiente para create_policy viram defer na execução. Assim, máximo matemático e resultado material podem diferir por gate explícito; os rastros e o result persistido permitem distinguir.

## 11. Política: conhecer, poder trabalhar, selecionar e produzir

| Política / setor | estado | conhecedores vivos observados (acumulado) | elegíveis conhecidos observados | trabalhadores efetivos | trabalho | orçamento/spent/refund/saldo | efeitos / barreiras |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 138300/SECURITY | stalled | 42 | 6 | [4562] | 3/4 | 8/3/0/5 | {"patrol":4562} / {"reason":"no_effective_work","at":288} |
| 146540/SECURITY | stalled | 46 | 5 | [] | 0/8 | 16/0/0/16 | {} / {"reason":"no_effective_work","at":288} |
| 306439/SECURITY | stalled | 21 | 4 | [] | 0/4 | 8/0/0/8 | {} / {"reason":"no_effective_work","at":288} |

| Etapa | Resultado |
| --- | --- |
| Need institutional_work avaliada / viável / escolhida | 18 / 9 / 7 |
| policy_work selecionada / executada / falha | 7 / 3 / 0 |
| Efeitos / conclusão / bloqueios publicados | 3 / 0 / 10 |
| Motivos de PolicyBlocked | {"no_effective_work":10} |
| Materiais efetivamente consumidos | {} |
| Salários / reservado / devolvido | 3 / 32 / 0 |

Awareness é conjunto de pessoas que conheciam a política enquanto vivas em algum checkpoint; disponibilidade institucional observada exige worker_eligible realmente consultado e conhecimento presente. Não é um censo de todos os trabalhadores potenciais do mundo. Recursos são consumidos na execução; orçamento é reservado em create_policy; não há reserva prévia de madeira/ferro por simples aprovação. SECURITY financia observação/patrulha, sem produção física de água/comida. WATER consome madeira+ferro, aumenta capacidade a cada dois passos; não cria água diretamente. Ver os oito handlers e as profissões exatas em PROJECT.md.

Blockers reais: budget_exhausted, worker_unfit, missing_wood_or_iron, missing_grain_or_storage, missing_iron_or_wood, missing_known_route_or_cargo, transport_supplies_missing, physical_arrival_unconfirmed, cargo_lost e specialized_assignment_unavailable; RAW_MATERIAL propaga status do trabalho. Institutions.tick também registra no_effective_work depois de pelo menos 48h sem trabalho e de idade da política; esse rótulo identifica ausência de execução, não a causa específica. Falta de conhecimento, prioridade ou caminho antes de policy_work pode impedir que haja PolicyBlocked. A ausência desse evento não prova disponibilidade material; um motivo não registrado é “não observável com instrumentação atual”.

### Trabalho real da política #138300 h184

Elena Hammer #4562; HP 100.0, fome 62.0, sede 53.0, fadiga 50.8; moedas 9; comida/água 0/0; posição 789:5,9; Goal policy_work/active

Personalidade na entrada: {"honesty":84,"compassion":29,"courage":67,"independence":72,"greed":26,"diligence":37,"family_loyalty":64,"persistence":32,"temperament":91,"vengefulness":88,"ambition":48,"sadism":0}.

| Need real na entrada | prioridade | status | alvo |
| --- | --- | --- | --- |
| family | 95.99 | blocked | 4565 |
| food | 74.80 | active | — |
| institutional_work | 65.25 | active | 138300 |
| food_reserve | 64.66 | active | — |
| water | 61 | active | — |
| rest | 58.80 | active | — |
| money | 46.30 | active | — |
| religious_interest | 44.96 | active | 5850 |

| Need avaliada | alternativa | Utility | alvo | considerações normalizadas |
| --- | --- | --- | --- | --- |
| food | buy_food | 89.80 | — | {"base":0.375,"honesty":0.084,"travel":-0.01} |
| food | forage | 65.00 | — | {"base":0.175,"independence":0.18,"hunter":0.0,"travel":-0.03} |
| food | steal | 1.15 | — | {"base":0.35,"greed":0.04333333333333334,"honesty":-0.42,"courage":0.0335,"travel":-0.01,"pressure_moral_tolerance":0.008931334285714285} |
| institutional_work | policy_work | 86.00 | 138300 | {"base":0.325,"diligence":0.04625,"financial_pressure":0.06875,"travel":-0.01} |

Antes: {"id":138300,"jurisdiction":789,"proposal_id":83775,"sector":"SECURITY","objective":"patrol","intensity":48.5,"budget":8,"money":8,"start_time":92,"status":"stalled","spent":0,"refunded":0,"work_done":0,"work_required":4,"last_work":-1,"workers":[],"effects":{},"barriers":{"reason":"no_effective_work","at":168},"history":[138301,199096,228472],"source_fact":73559}; retorno: [true,"Trabalho real e salário do orçamento reservado."].

### Trabalho real da política #138300 h188

Elena Hammer #4562; HP 100.0, fome 30.0, sede 16.0, fadiga 57.6; moedas 1; comida/água 0/0; posição 789:5,9; Goal policy_work/active

Personalidade na entrada: {"honesty":84,"compassion":29,"courage":67,"independence":72,"greed":26,"diligence":37,"family_loyalty":64,"persistence":32,"temperament":91,"vengefulness":88,"ambition":48,"sadism":0}.

| Need real na entrada | prioridade | status | alvo |
| --- | --- | --- | --- |
| family | 96.22 | blocked | 4565 |
| institutional_work | 65.85 | active | 138300 |
| rest | 65.60 | active | — |
| food_reserve | 57.68 | active | — |
| money | 57.37 | active | — |
| religious_interest | 45.46 | active | 5850 |

| Need avaliada | alternativa | Utility | alvo | considerações normalizadas |
| --- | --- | --- | --- | --- |
| institutional_work | policy_work | 98.00 | 138300 | {"base":0.325,"diligence":0.04625,"financial_pressure":0.11875,"travel":-0.0} |

Antes: {"id":138300,"jurisdiction":789,"proposal_id":83775,"sector":"SECURITY","objective":"patrol","intensity":48.5,"budget":8,"money":7,"start_time":92,"status":"active","spent":1,"refunded":0,"work_done":1,"work_required":4,"last_work":184,"workers":[4562],"effects":{"patrol":4562},"barriers":{},"history":[138301,199096,228472,247796],"source_fact":73559}; retorno: [true,"Trabalho real e salário do orçamento reservado."].

### Trabalho real da política #138300 h220

Elena Hammer #4562; HP 100.0, fome 54.0, sede 35.0, fadiga 50.0; moedas 2; comida/água 0/0; posição 789:5,9; Goal policy_work/active

Personalidade na entrada: {"honesty":84,"compassion":29,"courage":67,"independence":72,"greed":26,"diligence":37,"family_loyalty":64,"persistence":32,"temperament":91,"vengefulness":88,"ambition":48,"sadism":0}.

| Need real na entrada | prioridade | status | alvo |
| --- | --- | --- | --- |
| family | 96.14 | blocked | 4565 |
| institutional_work | 70.79 | active | 138300 |
| food_reserve | 67.81 | active | — |
| food | 65.05 | active | — |
| money | 61.83 | active | — |
| rest | 58.00 | active | — |
| political_pressure | 51.65 | active | — |
| religious_interest | 38.65 | active | 5850 |

| Need avaliada | alternativa | Utility | alvo | considerações normalizadas |
| --- | --- | --- | --- | --- |
| institutional_work | policy_work | 94.75 | 138300 | {"base":0.325,"diligence":0.04625,"financial_pressure":0.1125,"travel":-0.01} |

Antes: {"id":138300,"jurisdiction":789,"proposal_id":83775,"sector":"SECURITY","objective":"patrol","intensity":48.5,"budget":8,"money":6,"start_time":92,"status":"active","spent":2,"refunded":0,"work_done":2,"work_required":4,"last_work":188,"workers":[4562],"effects":{"patrol":4562},"barriers":{},"history":[138301,199096,228472,247796,253007],"source_fact":73559}; retorno: [true,"Trabalho real e salário do orçamento reservado."].

## 12. Mortalidade: causa, tempo e lugar

| Causa | Mortos |
| --- | --- |
| both | 10 |
| combat | 1 |
| hunger | 160 |
| thirst | 127 |

| Recuperação/dano registrado no mundo | Valor / unidade |
| --- | --- |
| Recovery:Damage:hunger | 51581 |
| Recovery:Damage:thirst | 14682 |
| Recovery:Damage:both | 3858 |
| Recovery:DeprivationHealed | 11159 |
| Recovery:PhysicalHealed | 373 |
| Recovery:DeprivationFullyRecovered | 500 |

Houve298 mortes em1.898 persistentes iniciais (15,70%);297/298 foram por privação (99,66%). A recuperação existe e foi usada:11.159 pontos de dano de privação foram curados e houve500 registros de recuperação completa desse ledger, não500 pessoas únicas. Logo, o diagnóstico atual não é ausência absoluta de cura. O problema envolve manter acesso, consumo e recuperação antes de esgotar HP; os rastros seguintes comprovam falhas de continuidade em parte das mortes. Não há contrafactual que atribua todas as298 a um único gate.

| Bloco horário | hunger | thirst | both | combat | other | total |
| --- | --- | --- | --- | --- | --- | --- |
| 1–25 | 0 | 0 | 0 | 0 | 0 | 0 |
| 26–50 | 0 | 0 | 0 | 0 | 0 | 0 |
| 51–75 | 0 | 0 | 0 | 0 | 0 | 0 |
| 76–100 | 0 | 1 | 0 | 0 | 0 | 1 |
| 101–125 | 4 | 4 | 0 | 0 | 0 | 8 |
| 126–150 | 3 | 14 | 2 | 0 | 0 | 19 |
| 151–175 | 6 | 33 | 2 | 0 | 0 | 41 |
| 176–200 | 4 | 33 | 1 | 0 | 0 | 38 |
| 201–225 | 4 | 28 | 1 | 0 | 0 | 33 |
| 226–250 | 31 | 12 | 4 | 1 | 0 | 48 |
| 251–275 | 58 | 2 | 0 | 0 | 0 | 60 |
| 276–300 | 50 | 0 | 0 | 0 | 0 | 50 |

| Tipo de local da morte | Mortos |
| --- | --- |
| capital | 286 |
| cidade | 12 |

| Localidade | tipo | residentes vivos finais / abstratos | mortes no mapa | estoque comida/água/grão | water_daily/storage | tesouro | economia final |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Dorthon #846 | capital | 19/218 | 84 | 0/78/1 | 80/160 | 2420 | {"turn":288,"stock":{"food":0,"grain":1,"water":95,"iron":120,"wood":94},"expected_demand":30.8,"processing_capacity":90,"hunting_capacity":40,"production_capacity":130,"actual_production":10,"capacity_deficit":0,"cook_count":3,"required_cooks":1,"professional_deficit":0,"projected_professional_deficit":0,"raw_required":42,"poor_residents":21,"bottlenecks":["RAW_MATERIAL_SHORTAGE","STORAGE_BLOCKAGE","LOCAL_ACCESS_PROBLEM","TRANSPORT_SHORTAGE"],"external_supply_reports":[875,958],"transport_available":false} |
| Dordor #3 | capital | 23/218 | 80 | 0/66/0 | 80/160 | 2456 | {"turn":288,"stock":{"food":0,"grain":2,"water":84,"iron":120,"wood":82},"expected_demand":39.2,"processing_capacity":90,"hunting_capacity":100,"production_capacity":190,"actual_production":3,"capacity_deficit":0,"cook_count":4,"required_cooks":1,"professional_deficit":0,"projected_professional_deficit":0,"raw_required":54,"poor_residents":27,"bottlenecks":["RAW_MATERIAL_SHORTAGE","STORAGE_BLOCKAGE","LOCAL_ACCESS_PROBLEM","TRANSPORT_SHORTAGE"],"external_supply_reports":[79,126,144,209,274],"transport_available":false} |
| Valvia #302 | capital | 39/218 | 66 | 0/48/0 | 80/160 | 2605 | {"turn":288,"stock":{"food":0,"grain":0,"water":80,"iron":120,"wood":120},"expected_demand":59.6,"processing_capacity":60,"hunting_capacity":80,"production_capacity":140,"actual_production":45,"capacity_deficit":0,"cook_count":8,"required_cooks":1,"professional_deficit":0,"projected_professional_deficit":0,"raw_required":80,"poor_residents":46,"bottlenecks":["RAW_MATERIAL_SHORTAGE","STORAGE_BLOCKAGE","LOCAL_ACCESS_PROBLEM","TRANSPORT_SHORTAGE"],"external_supply_reports":[331,378],"transport_available":false} |
| Elilen #583 | capital | 51/218 | 56 | 2/32/17 | 80/160 | 2769 | {"turn":288,"stock":{"food":4,"grain":23,"water":80,"iron":118,"wood":120},"expected_demand":65.6,"processing_capacity":60,"hunting_capacity":80,"production_capacity":140,"actual_production":36,"capacity_deficit":0,"cook_count":12,"required_cooks":1,"professional_deficit":0,"projected_professional_deficit":0,"raw_required":88,"poor_residents":51,"bottlenecks":["RAW_MATERIAL_SHORTAGE","AFFORDABILITY_PROBLEM","STORAGE_BLOCKAGE","LOCAL_ACCESS_PROBLEM","TRANSPORT_SHORTAGE"],"external_supply_reports":[630,677,724,771],"transport_available":false} |
| Karlen #976 | cidade | 57/150 | 4 | 8/130/123 | 80/160 | 2361 | {"turn":288,"stock":{"food":0,"grain":136,"water":160,"iron":120,"wood":102},"expected_demand":71.6,"processing_capacity":60,"hunting_capacity":140,"production_capacity":200,"actual_production":32,"capacity_deficit":0,"cook_count":8,"required_cooks":1,"professional_deficit":0,"projected_professional_deficit":0,"raw_required":96,"poor_residents":53,"bottlenecks":["STORAGE_BLOCKAGE","LOCAL_ACCESS_PROBLEM","TRANSPORT_SHORTAGE"],"external_supply_reports":[875,958],"transport_available":false} |
| Elilen #695 | cidade | 57/150 | 2 | 6/123/0 | 80/160 | 1726 | {"turn":288,"stock":{"food":4,"grain":12,"water":160,"iron":120,"wood":120},"expected_demand":70.4,"processing_capacity":60,"hunting_capacity":140,"production_capacity":200,"actual_production":28,"capacity_deficit":0,"cook_count":7,"required_cooks":1,"professional_deficit":0,"projected_professional_deficit":0,"raw_required":94,"poor_residents":43,"bottlenecks":["RAW_MATERIAL_SHORTAGE","AFFORDABILITY_PROBLEM","STORAGE_BLOCKAGE","LOCAL_ACCESS_PROBLEM","TRANSPORT_SHORTAGE"],"external_supply_reports":[630,724,771],"transport_available":false} |
| Valthon #742 | cidade | 59/150 | 2 | 21/128/42 | 80/160 | 1810 | {"turn":288,"stock":{"food":1,"grain":53,"water":160,"iron":120,"wood":120},"expected_demand":72.8,"processing_capacity":60,"hunting_capacity":140,"production_capacity":200,"actual_production":12,"capacity_deficit":0,"cook_count":8,"required_cooks":1,"professional_deficit":0,"projected_professional_deficit":0,"raw_required":98,"poor_residents":51,"bottlenecks":["RAW_MATERIAL_SHORTAGE","AFFORDABILITY_PROBLEM","STORAGE_BLOCKAGE","LOCAL_ACCESS_PROBLEM","TRANSPORT_SHORTAGE"],"external_supply_reports":[630,724,771],"transport_available":false} |
| Normar #97 | cidade | 60/150 | 1 | 6/122/189 | 80/160 | 2222 | {"turn":288,"stock":{"food":2,"grain":201,"water":160,"iron":120,"wood":120},"expected_demand":74.0,"processing_capacity":60,"hunting_capacity":140,"production_capacity":200,"actual_production":38,"capacity_deficit":0,"cook_count":8,"required_cooks":1,"professional_deficit":0,"projected_professional_deficit":0,"raw_required":100,"poor_residents":57,"bottlenecks":["AFFORDABILITY_PROBLEM","STORAGE_BLOCKAGE","LOCAL_ACCESS_PROBLEM","TRANSPORT_SHORTAGE"],"external_supply_reports":[79,126,144,209,274],"transport_available":false} |
| Norven #349 | cidade | 60/150 | 1 | 18/129/204 | 80/160 | 2141 | {"turn":288,"stock":{"food":14,"grain":210,"water":160,"iron":120,"wood":120},"expected_demand":74.0,"processing_capacity":60,"hunting_capacity":140,"production_capacity":200,"actual_production":57,"capacity_deficit":0,"cook_count":9,"required_cooks":1,"professional_deficit":0,"projected_professional_deficit":0,"raw_required":100,"poor_residents":38,"bottlenecks":["AFFORDABILITY_PROBLEM","STORAGE_BLOCKAGE","LOCAL_ACCESS_PROBLEM","TRANSPORT_SHORTAGE"],"external_supply_reports":[331,378],"transport_available":false} |
| Sildor #911 | cidade | 60/150 | 1 | 6/138/84 | 80/160 | 1968 | {"turn":288,"stock":{"food":11,"grain":77,"water":160,"iron":120,"wood":120},"expected_demand":74.0,"processing_capacity":60,"hunting_capacity":160,"production_capacity":220,"actual_production":35,"capacity_deficit":0,"cook_count":8,"required_cooks":1,"professional_deficit":0,"projected_professional_deficit":0,"raw_required":100,"poor_residents":46,"bottlenecks":["RAW_MATERIAL_SHORTAGE","AFFORDABILITY_PROBLEM","STORAGE_BLOCKAGE","LOCAL_ACCESS_PROBLEM","TRANSPORT_SHORTAGE"],"external_supply_reports":[875,958],"transport_available":false} |
| Dorria #1023 | cidade | 61/150 | 1 | 1/136/0 | 80/160 | 1634 | {"turn":288,"stock":{"food":1,"grain":0,"water":160,"iron":120,"wood":120},"expected_demand":75.2,"processing_capacity":60,"hunting_capacity":140,"production_capacity":200,"actual_production":54,"capacity_deficit":0,"cook_count":8,"required_cooks":1,"professional_deficit":0,"projected_professional_deficit":0,"raw_required":102,"poor_residents":58,"bottlenecks":["RAW_MATERIAL_SHORTAGE","AFFORDABILITY_PROBLEM","STORAGE_BLOCKAGE","LOCAL_ACCESS_PROBLEM","TRANSPORT_SHORTAGE"],"external_supply_reports":[875,958],"transport_available":false} |

Estoque e capacidade nessa tabela são do encerramento; estoque na morte está no rastro individual. Mortes foram localizadas por posição real, não residência. “Residentes vivos finais” conta o cadastro de residentes; viagens podem deslocar a presença física. water_daily/storage são limites de infraestrutura, não volume garantido entregue a cada NPC. economic_report conserva o último relatório econômico, não uma série diária inteira.

## 12.1 Posse, conhecimento, dinheiro e alcance

| Condição ao chamar finish_death (privação) | Pessoas |
| --- | --- |
| Carregava comida | 1 |
| Carregava água | 79 |
| Tinha moedas >0 / ≥2 | 216 / 162 |
| Comida local >0 / água local >0 | 136 / 120 |
| Conhecia mercado / algum poço | 297 / 297 |
| Fome fatal e comida carregada | 0 |
| Sede fatal e água carregada | 13 |

| Acesso econômico conhecido (privação) | Pessoas |
| --- | --- |
| Cotação de comida conhecida com até 24h e mesmo mapa | 220 |
| Desses: dinheiro suficiente para uma unidade ao preço conhecido | 29 |
| Desses: dinheiro insuficiente | 191 |
| Demais: sem cotação recente local suficiente para concluir affordability | 77 |

Recurso local não equivale a recurso do NPC. Comida pode exigir compra, matéria-prima não é refeição e água do Town abastece mercado/poço sob regras distintas. Uma cotação conhecida antiga não prova preço atual. Dinheiro≥2 é faixa descritiva, não certificado de affordability. O motor aplica dano fisiológico antes da próxima decisão: estar com HP zero na entrada de finish_death não oferece uma rodada extra para comer. Ver fórmulas exatas de dano/recuperação em PROJECT.md.

| Último registro | Distribuição |
| --- | --- |
| Need da última decisão real | {"rest":202,"food":45,"water":22,"security":1,"political_pressure":2,"money":19,"divine_contact":1,"migration":1,"family":4} |
| Ação escolhida naquela decisão | {"fill_water":114,"sleep":81,"person_meal":14,"ask_meal":4,"drink_well":19,"drink":15,"secure":1,"forage_meal":10,"forage":3,"eat":2,"steal_meal":7,"buy_meal":1,"service_meal":1,"work_for_meal":6,"work":17,"check_relative":2} |
| Goal armazenado ao morrer | {"fill_water":114,"sleep":81,"person_meal":14,"ask_meal":4,"drink_well":19,"drink":15,"secure":1,"forage_meal":10,"forage":3,"eat":2,"steal_meal":7,"buy_meal":1,"service_meal":1,"work_for_meal":6,"work":17,"check_relative":2} |

Achado específico: 94 mortos têm, dentro dos últimos três registros, fill_water escolhido novamente menos de 12h depois de sua falha. O preparador cria uma Solution depois de _evaluate e não reaplica o filtro failures[action]>turn. No total, 114 mortos terminaram com fill_water escolhido; 13 morreram de sede/both com água carregada. No caso John Solaris #1245, h166/h167 falharam, h168 obteve duas águas com HP 2 e sede 100, e o fechamento h169 matou antes do consumo seguinte. Isso prova quebra de continuidade observada, não que corrigir somente esse ponto salvaria todos os mortos.

O caminho foi conferido por BFS somente leitura sobre o mapa, sem atualizar conhecimento ou chamar decisões. É distância física local a uma fonte conhecida (primeiro poço registrado ou mercado), não garantia de água remanescente, sobrevivência durante a caminhada, custo ou acesso em outra localidade. Necessidades institucionais foram mantidas com as prioridades originais.

### Morte #1245 — thirst h169

John Solaris #1245; HP 0.0, fome 30.0, sede 100.0, fadiga 100.0; moedas 0; comida/água 0/2; posição 3:7,13; Goal fill_water/completed

Primeira Need vital observada ≥50: {"water":50,"food":53}; conhecido mercado {"map_id":3,"x":7,"y":13}, poços [{"map_id":3,"x":2,"y":2},{"map_id":3,"x":1,"y":13}]; observação econômica {"turn":168,"town_id":3,"stock":{"food":17,"grain":24,"water":61,"iron":120,"wood":78},"temporary_work":true,"temporary_offers":{"meal_distribution":{"capacity":1,"local":{"map_id":3,"x":7,"y":13},"required_food_per_unit":2},"food_preparation":{"capacity":12,"local":{"map_id":3,"x":1,"y":13},"required_grain_thirds":6,"paid_food_per_unit":1}},"offers_observed_at":168,"offers_expire_at":192,"training_offer":null,"price":2,"price_turn":168}; comida/água local 17/0; passos à primeira fonte conhecida 16.

h166: Need rest prioridade 100.00; escolhido fill_water score 100.00; estado após: John Solaris #1245; HP 10.0, fome 24.0, sede 100.0, fadiga 100.0; moedas 0; comida/água 0/0; posição 3:7,13; Goal fill_water/failed; execução=True, retorno=[false,"Não há água para levar nesta fonte."].

| Alternativa realmente avaliada | score | alvo | termos | estimativa alimentar calculada |
| --- | --- | --- | --- | --- |
| sleep | 68.00 | — | {"base":0.5,"recovery_pressure":0.0,"travel":-0.16} | — |

h167: Need rest prioridade 100.00; escolhido fill_water score 100.00; estado após: John Solaris #1245; HP 6.0, fome 26.0, sede 100.0, fadiga 100.0; moedas 0; comida/água 0/0; posição 3:7,13; Goal fill_water/failed; execução=True, retorno=[false,"Não há água para levar nesta fonte."].

| Alternativa realmente avaliada | score | alvo | termos | estimativa alimentar calculada |
| --- | --- | --- | --- | --- |
| sleep | 68.00 | — | {"base":0.5,"recovery_pressure":0.0,"travel":-0.16} | — |

h168: Need rest prioridade 100.00; escolhido fill_water score 100.00; estado após: John Solaris #1245; HP 2.0, fome 28.0, sede 100.0, fadiga 100.0; moedas 0; comida/água 0/2; posição 3:7,13; Goal fill_water/completed; execução=True, retorno=[true,"Reserva de água obtida na fonte local."].

| Alternativa realmente avaliada | score | alvo | termos | estimativa alimentar calculada |
| --- | --- | --- | --- | --- |
| sleep | 68.00 | — | {"base":0.5,"recovery_pressure":0.0,"travel":-0.16} | — |

Registro causal do motor: {"turn":169,"name":"John Solaris","profession":"guarda","town_id":3,"cause":"thirst","health":0,"hunger":30,"thirst":100,"fatigue":100,"food":0,"water":2,"last_meal":164,"last_drink":98,"recoverable_deprivation_damage":100,"damage_by_origin":{"thirst":88,"hunger":12,"both":6},"last_successful_action":{"action":"fill_water","turn":168},"goal":"fill_water","destination":{"map_id":3,"x":7,"y":13},"known_water_sources":[{"map_id":3,"x":7,"y":13},{"map_id":3,"x":2,"y":2},{"map_id":3,"x":1,"y":13}],"distance_to_water":0,"event_id":229958}. Não se conclui que o NPC poderia consumir estoque remoto apenas porque o Town tinha unidades.

### Morte #1263 — thirst h169

Marie Montes #1263; HP 0.0, fome 28.0, sede 100.0, fadiga 100.0; moedas 3; comida/água 0/2; posição 3:1,13; Goal fill_water/completed

Primeira Need vital observada ≥50: {"food":2,"water":26}; conhecido mercado {"map_id":3,"x":7,"y":13}, poços [{"map_id":3,"x":2,"y":2},{"map_id":3,"x":1,"y":13}]; observação econômica {"turn":168,"town_id":3,"stock":{"food":17,"grain":22,"water":57,"iron":120,"wood":78},"temporary_work":true,"temporary_offers":{"food_preparation":{"capacity":11,"local":{"map_id":3,"x":1,"y":13},"required_grain_thirds":6,"paid_food_per_unit":1}},"offers_observed_at":168,"offers_expire_at":192,"training_offer":null,"price":9,"price_turn":152}; comida/água local 17/0; passos à primeira fonte conhecida 12.

h166: Need rest prioridade 100.00; escolhido fill_water score 100.00; estado após: Marie Montes #1263; HP 10.0, fome 22.0, sede 100.0, fadiga 100.0; moedas 3; comida/água 0/0; posição 3:1,13; Goal fill_water/failed; execução=True, retorno=[false,"Não há água para levar nesta fonte."].

| Alternativa realmente avaliada | score | alvo | termos | estimativa alimentar calculada |
| --- | --- | --- | --- | --- |
| sleep | 76.00 | — | {"base":0.5,"recovery_pressure":0.0,"travel":-0.12} | — |

h167: Need rest prioridade 100.00; escolhido fill_water score 100.00; estado após: Marie Montes #1263; HP 6.0, fome 24.0, sede 100.0, fadiga 100.0; moedas 3; comida/água 0/0; posição 3:1,13; Goal fill_water/failed; execução=True, retorno=[false,"Não há água para levar nesta fonte."].

| Alternativa realmente avaliada | score | alvo | termos | estimativa alimentar calculada |
| --- | --- | --- | --- | --- |
| sleep | 76.00 | — | {"base":0.5,"recovery_pressure":0.0,"travel":-0.12} | — |

h168: Need rest prioridade 100.00; escolhido fill_water score 100.00; estado após: Marie Montes #1263; HP 2.0, fome 26.0, sede 100.0, fadiga 100.0; moedas 3; comida/água 0/2; posição 3:1,13; Goal fill_water/completed; execução=True, retorno=[true,"Reserva de água obtida na fonte local."].

| Alternativa realmente avaliada | score | alvo | termos | estimativa alimentar calculada |
| --- | --- | --- | --- | --- |
| sleep | 76.00 | — | {"base":0.5,"recovery_pressure":0.0,"travel":-0.12} | — |

Registro causal do motor: {"turn":169,"name":"Marie Montes","profession":"lenhador","town_id":3,"cause":"thirst","health":0,"hunger":28,"thirst":100,"fatigue":100,"food":0,"water":2,"last_meal":163,"last_drink":86,"recoverable_deprivation_damage":100,"damage_by_origin":{"thirst":86,"both":14},"last_successful_action":{"action":"fill_water","turn":168},"goal":"fill_water","destination":{"map_id":3,"x":1,"y":13},"known_water_sources":[{"map_id":3,"x":7,"y":13},{"map_id":3,"x":2,"y":2},{"map_id":3,"x":1,"y":13}],"distance_to_water":0,"event_id":229959}. Não se conclui que o NPC poderia consumir estoque remoto apenas porque o Town tinha unidades.

### Morte #5043 — hunger h127

Tomas Montes #5043; HP 0.0, fome 100.0, sede 29.0, fadiga 82.0; moedas 1; comida/água 0/0; posição 911:2,2; Goal ask_meal/failed

Primeira Need vital observada ≥50: {"food":11,"water":26}; conhecido mercado {"map_id":911,"x":5,"y":9}, poços [{"map_id":911,"x":2,"y":2},{"map_id":911,"x":1,"y":9}]; observação econômica {"turn":116,"town_id":911,"stock":{"food":76,"grain":100,"water":94,"iron":116,"wood":86},"temporary_work":true,"temporary_offers":{"meal_distribution":{"capacity":2,"local":{"map_id":911,"x":5,"y":9},"required_food_per_unit":2},"food_preparation":{"capacity":50,"local":{"map_id":911,"x":1,"y":9},"required_grain_thirds":6,"paid_food_per_unit":1}},"offers_observed_at":116,"offers_expire_at":140,"training_offer":null,"price":2,"price_turn":103}; comida/água local 57/141; passos à primeira fonte conhecida 0.

h124: Need food prioridade 100.00; escolhido person_meal score 8.67; estado após: Tomas Montes #5043; HP 10.0, fome 100.0, sede 23.0, fadiga 78.4; moedas 1; comida/água 0/0; posição 911:2,2; Goal person_meal/failed; execução=True, retorno=[false,"Não havia provisão acessível no alvo."].

| Alternativa realmente avaliada | score | alvo | termos | estimativa alimentar calculada |
| --- | --- | --- | --- | --- |
| person_meal | 8.67 | 5006 | {"base":0.31,"greed":0.14800000000000002,"honesty":-0.414,"authority":-0.2,"courage":0.028499999999999998,"travel":-0.0,"pressure_moral_tolerance":0.17087401500000002} | {"EstimatedTimeUntilFoodConsumed":1,"EstimatedSurvivalMargin":3,"economically_viable":true,"survival_viable":true,"reason":null,"known_conditions":["NoMoney","DistantProduct"]} |

h125: Need food prioridade 100.00; escolhido steal_person score 8.23; estado após: Tomas Montes #5043; HP 6.0, fome 100.0, sede 25.0, fadiga 79.6; moedas 1; comida/água 0/0; posição 911:2,2; Goal steal_person/failed; execução=True, retorno=[false,"Não havia provisão acessível no alvo."].

| Alternativa realmente avaliada | score | alvo | termos | estimativa alimentar calculada |
| --- | --- | --- | --- | --- |
| steal_person | 8.23 | 5006 | {"base":0.31,"greed":0.14800000000000002,"honesty":-0.414,"authority":-0.2,"courage":0.028499999999999998,"travel":-0.0,"pressure_moral_tolerance":0.16864646500000002} | {"EstimatedTimeUntilFoodConsumed":2,"EstimatedSurvivalMargin":2,"economically_viable":true,"survival_viable":true,"reason":null,"known_conditions":["NoMoney","DistantProduct"]} |

h126: Need food prioridade 100.00; escolhido ask_meal score 82.35; estado após: Tomas Montes #5043; HP 2.0, fome 100.0, sede 27.0, fadiga 80.8; moedas 1; comida/água 0/0; posição 911:2,2; Goal ask_meal/failed; execução=True, retorno=[false,"Não foi possível obter ajuda."].

| Alternativa realmente avaliada | score | alvo | termos | estimativa alimentar calculada |
| --- | --- | --- | --- | --- |
| ask_meal | 82.35 | 5040 | {"base":0.125,"compassion":0.1775,"trust":0.07525,"reputation":0.0,"relationship":0.034,"travel":-0.0} | {"EstimatedTimeUntilFoodConsumed":1,"EstimatedSurvivalMargin":1,"economically_viable":true,"survival_viable":true,"reason":null,"known_conditions":["NoMoney","DistantProduct"]} |

Registro causal do motor: {"turn":127,"name":"Tomas Montes","profession":"ferreiro","town_id":911,"cause":"hunger","health":0,"hunger":100,"thirst":29,"fatigue":82.00000000000001,"food":0,"water":0,"last_meal":56,"last_drink":115,"recoverable_deprivation_damage":100,"damage_by_origin":{"hunger":100},"last_successful_action":{"action":"sleep","turn":123},"goal":"ask_meal","destination":null,"known_water_sources":[{"map_id":911,"x":5,"y":9},{"map_id":911,"x":2,"y":2},{"map_id":911,"x":1,"y":9}],"distance_to_water":0,"event_id":178849}. Não se conclui que o NPC poderia consumir estoque remoto apenas porque o Town tinha unidades.

### Morte #328 — hunger h192

Iria Ferros #328; HP 0.0, fome 100.0, sede 62.0, fadiga 89.2; moedas 2; comida/água 0/0; posição 302:2,2; Goal sleep/completed

Primeira Need vital observada ≥50: {"food":12,"water":27}; conhecido mercado {"map_id":302,"x":7,"y":13}, poços [{"map_id":302,"x":2,"y":2},{"map_id":302,"x":1,"y":13}]; observação econômica {"turn":173,"town_id":302,"stock":{"food":0,"grain":0,"water":0,"iron":106,"wood":120},"temporary_work":false,"temporary_offers":{},"offers_observed_at":173,"offers_expire_at":197,"training_offer":null,"price":14,"price_turn":173}; comida/água local 35/0; passos à primeira fonte conhecida 0.

h189: Need food prioridade 100.00; escolhido person_meal score -16.42; estado após: Iria Ferros #328; HP 2.0, fome 94.0, sede 56.0, fadiga 100.0; moedas 2; comida/água 0/0; posição 302:2,2; Goal person_meal/failed; execução=True, retorno=[false,"Não havia provisão acessível no alvo."].

| Alternativa realmente avaliada | score | alvo | termos | estimativa alimentar calculada |
| --- | --- | --- | --- | --- |
| person_meal | -16.42 | 2520 | {"base":0.31,"greed":0.036,"honesty":-0.396,"authority":-0.2,"courage":0.0245,"travel":-0.0,"pressure_moral_tolerance":0.14340612} | {"EstimatedTimeUntilFoodConsumed":1,"EstimatedSurvivalMargin":3,"economically_viable":true,"survival_viable":true,"reason":null,"known_conditions":["NoProduct","NoMoney","DistantProduct"]} |

h190: Need food prioridade 100.00; escolhido steal_person score -16.51; estado após: Iria Ferros #328; HP 2.0, fome 96.0, sede 58.0, fadiga 100.0; moedas 2; comida/água 0/0; posição 302:2,2; Goal steal_person/failed; execução=True, retorno=[false,"Não havia provisão acessível no alvo."].

| Alternativa realmente avaliada | score | alvo | termos | estimativa alimentar calculada |
| --- | --- | --- | --- | --- |
| steal_person | -16.51 | 2520 | {"base":0.31,"greed":0.036,"honesty":-0.396,"authority":-0.2,"courage":0.0245,"travel":-0.0,"pressure_moral_tolerance":0.14293422000000003} | {"EstimatedTimeUntilFoodConsumed":2,"EstimatedSurvivalMargin":2,"economically_viable":true,"survival_viable":true,"reason":null,"known_conditions":["NoProduct","NoMoney","DistantProduct"]} |

h191: Need rest prioridade 100.00; escolhido sleep score 100.00; estado após: Iria Ferros #328; HP 2.0, fome 98.0, sede 60.0, fadiga 88.0; moedas 2; comida/água 0/0; posição 302:2,2; Goal sleep/completed; execução=True, retorno=[true,"Descanso realizado."].

| Alternativa realmente avaliada | score | alvo | termos | estimativa alimentar calculada |
| --- | --- | --- | --- | --- |
| sleep | 100.00 | — | {"base":0.5,"recovery_pressure":0.0,"travel":-0.0} | — |

Registro causal do motor: {"turn":192,"name":"Iria Ferros","profession":"caçador","town_id":302,"cause":"hunger","health":0,"hunger":100,"thirst":62,"fatigue":89.2,"food":0,"water":0,"last_meal":172,"last_drink":167,"recoverable_deprivation_damage":100,"damage_by_origin":{"hunger":94,"thirst":8},"last_successful_action":{"action":"sleep","turn":191},"goal":"sleep","destination":{"map_id":302,"x":2,"y":2},"known_water_sources":[{"map_id":302,"x":7,"y":13},{"map_id":302,"x":2,"y":2},{"map_id":302,"x":1,"y":13}],"distance_to_water":0,"event_id":257233}. Não se conclui que o NPC poderia consumir estoque remoto apenas porque o Town tinha unidades.

### Morte #2589 — thirst h266

Bela Valerius #2589; HP 0.0, fome 24.0, sede 100.0, fadiga 100.0; moedas 2; comida/água 0/0; posição 302:1,13; Goal work_for_meal/completed

Primeira Need vital observada ≥50: {"food":14,"water":26}; conhecido mercado {"map_id":302,"x":7,"y":13}, poços [{"map_id":302,"x":2,"y":2},{"map_id":302,"x":1,"y":13}]; observação econômica {"turn":265,"town_id":302,"stock":{"food":0,"grain":4,"water":61,"iron":120,"wood":120},"temporary_work":true,"temporary_offers":{"food_preparation":{"capacity":2,"local":{"map_id":302,"x":1,"y":13},"required_grain_thirds":6,"paid_food_per_unit":1}},"offers_observed_at":265,"offers_expire_at":289,"training_offer":null,"price":14,"price_turn":249}; comida/água local 4/59; passos à primeira fonte conhecida 12.

h263: Need rest prioridade 100.00; escolhido fill_water score 100.00; estado após: Bela Valerius #2589; HP 12.0, fome 100.0, sede 100.0, fadiga 100.0; moedas 2; comida/água 0/0; posição 302:1,13; Goal fill_water/failed; execução=True, retorno=[false,"Não há água para levar nesta fonte."].

| Alternativa realmente avaliada | score | alvo | termos | estimativa alimentar calculada |
| --- | --- | --- | --- | --- |
| sleep | 76.00 | — | {"base":0.5,"recovery_pressure":0.0,"travel":-0.12} | — |

h264: Need food prioridade 100.00; escolhido work_for_meal score 16.50; estado após: Bela Valerius #2589; HP 8.0, fome 60.0, sede 100.0, fadiga 100.0; moedas 2; comida/água 0/0; posição 302:1,13; Goal work_for_meal/completed; execução=True, retorno=[true,"Trabalho realizado com pagamento do produto ou proporcional. Fome reduzida."].

| Alternativa realmente avaliada | score | alvo | termos | estimativa alimentar calculada |
| --- | --- | --- | --- | --- |
| work_for_meal | 16.50 | — | {"base":0.225,"diligence":0.015,"physical_depletion":-0.1575,"travel":-0.0} | {"EstimatedTimeUntilFoodConsumed":1,"EstimatedSurvivalMargin":2,"economically_viable":true,"survival_viable":true,"reason":null,"known_conditions":["NoProduct","NoMoney","DistantProduct"]} |

h265: Need food prioridade 100.00; escolhido work_for_meal score 14.75; estado após: Bela Valerius #2589; HP 4.0, fome 22.0, sede 100.0, fadiga 100.0; moedas 2; comida/água 0/0; posição 302:1,13; Goal work_for_meal/completed; execução=True, retorno=[true,"Trabalho realizado com pagamento do produto ou proporcional. Fome reduzida."].

| Alternativa realmente avaliada | score | alvo | termos | estimativa alimentar calculada |
| --- | --- | --- | --- | --- |
| work_for_meal | 14.75 | — | {"base":0.225,"diligence":0.015,"physical_depletion":-0.16625,"travel":-0.0} | {"EstimatedTimeUntilFoodConsumed":1,"EstimatedSurvivalMargin":1,"economically_viable":true,"survival_viable":true,"reason":null,"known_conditions":["NoProduct","NoMoney","DistantProduct"]} |

Registro causal do motor: {"turn":266,"name":"Bela Valerius","profession":"comerciante","town_id":302,"cause":"thirst","health":0,"hunger":24,"thirst":100,"fatigue":100,"food":0,"water":0,"last_meal":265,"last_drink":218,"recoverable_deprivation_damage":100,"damage_by_origin":{"thirst":32,"hunger":62,"both":12},"last_successful_action":{"action":"work_for_meal","turn":265},"goal":"work_for_meal","destination":{"map_id":302,"x":1,"y":13},"known_water_sources":[{"map_id":302,"x":7,"y":13},{"map_id":302,"x":2,"y":2},{"map_id":302,"x":1,"y":13}],"distance_to_water":0,"event_id":340856}. Não se conclui que o NPC poderia consumir estoque remoto apenas porque o Town tinha unidades.

### Morte #2612 — thirst h241

Cael Ferros #2612; HP 0.0, fome 10.0, sede 100.0, fadiga 100.0; moedas 1; comida/água 0/2; posição 302:1,13; Goal fill_water/completed

Primeira Need vital observada ≥50: {"water":25,"food":52}; conhecido mercado {"map_id":302,"x":7,"y":13}, poços [{"map_id":302,"x":2,"y":2},{"map_id":302,"x":1,"y":13}]; observação econômica {"turn":240,"town_id":302,"stock":{"food":7,"grain":2,"water":53,"iron":120,"wood":120},"temporary_work":true,"temporary_offers":{"meal_distribution":{"capacity":2,"local":{"map_id":302,"x":7,"y":13},"required_food_per_unit":2},"food_preparation":{"capacity":1,"local":{"map_id":302,"x":1,"y":13},"required_grain_thirds":6,"paid_food_per_unit":1}},"offers_observed_at":240,"offers_expire_at":264,"training_offer":null,"price":7,"price_turn":151}; comida/água local 7/49; passos à primeira fonte conhecida 12.

h238: Need water prioridade 100.00; escolhido drink_well score 100.00; estado após: Cael Ferros #2612; HP 5.0, fome 4.0, sede 98.0, fadiga 100.0; moedas 1; comida/água 0/0; posição 302:1,13; Goal drink_well/failed; execução=True, retorno=[false,"Não há água disponível."].

| Alternativa realmente avaliada | score | alvo | termos | estimativa alimentar calculada |
| --- | --- | --- | --- | --- |
| drink_well | 100.00 | — | {"base":0.5,"travel":-0.0} | — |
| drink_well | 88.00 | — | {"base":0.5,"travel":-0.06} | — |
| drink_well | 76.00 | — | {"base":0.5,"travel":-0.12} | — |

h239: Need rest prioridade 100.00; escolhido fill_water score 100.00; estado após: Cael Ferros #2612; HP 3.0, fome 6.0, sede 100.0, fadiga 100.0; moedas 1; comida/água 0/0; posição 302:1,13; Goal fill_water/failed; execução=True, retorno=[false,"Não há água para levar nesta fonte."].

| Alternativa realmente avaliada | score | alvo | termos | estimativa alimentar calculada |
| --- | --- | --- | --- | --- |
| sleep | 76.00 | — | {"base":0.5,"recovery_pressure":0.0,"travel":-0.12} | — |

h240: Need rest prioridade 100.00; escolhido fill_water score 100.00; estado após: Cael Ferros #2612; HP 1.0, fome 8.0, sede 100.0, fadiga 100.0; moedas 1; comida/água 0/2; posição 302:1,13; Goal fill_water/completed; execução=True, retorno=[true,"Reserva de água obtida na fonte local."].

| Alternativa realmente avaliada | score | alvo | termos | estimativa alimentar calculada |
| --- | --- | --- | --- | --- |
| sleep | 76.00 | — | {"base":0.5,"recovery_pressure":0.0,"travel":-0.12} | — |

Registro causal do motor: {"turn":241,"name":"Cael Ferros","profession":"comerciante","town_id":302,"cause":"thirst","health":0,"hunger":10,"thirst":100,"fatigue":100,"food":0,"water":2,"last_meal":236,"last_drink":195,"recoverable_deprivation_damage":100,"damage_by_origin":{"hunger":78,"thirst":27},"last_successful_action":{"action":"fill_water","turn":240},"goal":"fill_water","destination":{"map_id":302,"x":1,"y":13},"known_water_sources":[{"map_id":302,"x":7,"y":13},{"map_id":302,"x":2,"y":2},{"map_id":302,"x":1,"y":13}],"distance_to_water":0,"event_id":313296}. Não se conclui que o NPC poderia consumir estoque remoto apenas porque o Town tinha unidades.

### Morte #4819 — hunger h122

Cael Arven #4819; HP 0.0, fome 100.0, sede 57.0, fadiga 100.0; moedas 38; comida/água 0/1; posição 846:7,13; Goal drink/completed

Primeira Need vital observada ≥50: {"food":45,"water":48}; conhecido mercado {"map_id":846,"x":7,"y":13}, poços [{"map_id":846,"x":2,"y":2},{"map_id":846,"x":1,"y":13}]; observação econômica {"turn":121,"town_id":846,"stock":{"food":0,"grain":0,"water":40,"iron":114,"wood":72},"temporary_work":false,"temporary_offers":{},"offers_observed_at":121,"offers_expire_at":145,"training_offer":null,"price":14,"price_turn":121}; comida/água local 0/40; passos à primeira fonte conhecida 16.

h119: Need rest prioridade 100.00; escolhido fill_water score 100.00; estado após: Cael Arven #4819; HP 10.0, fome 100.0, sede 100.0, fadiga 100.0; moedas 38; comida/água 0/0; posição 846:7,13; Goal fill_water/failed; execução=True, retorno=[false,"Não há água para levar nesta fonte."].

| Alternativa realmente avaliada | score | alvo | termos | estimativa alimentar calculada |
| --- | --- | --- | --- | --- |
| sleep | 68.00 | — | {"base":0.5,"recovery_pressure":0.0,"travel":-0.16} | — |

h120: Need rest prioridade 100.00; escolhido fill_water score 100.00; estado após: Cael Arven #4819; HP 6.0, fome 100.0, sede 100.0, fadiga 100.0; moedas 38; comida/água 0/2; posição 846:7,13; Goal fill_water/completed; execução=True, retorno=[true,"Reserva de água obtida na fonte local."].

| Alternativa realmente avaliada | score | alvo | termos | estimativa alimentar calculada |
| --- | --- | --- | --- | --- |
| sleep | 68.00 | — | {"base":0.5,"recovery_pressure":0.0,"travel":-0.16} | — |

h121: Need water prioridade 100.00; escolhido drink score 200.00; estado após: Cael Arven #4819; HP 2.0, fome 100.0, sede 55.0, fadiga 100.0; moedas 38; comida/água 0/1; posição 846:7,13; Goal drink/completed; execução=True, retorno=[true,"Sede reduzida."].

| Alternativa realmente avaliada | score | alvo | termos | estimativa alimentar calculada |
| --- | --- | --- | --- | --- |
| drink | 200.00 | — | {"base":1.0,"travel":-0.0} | — |

Registro causal do motor: {"turn":122,"name":"Cael Arven","profession":"comerciante","town_id":846,"cause":"hunger","health":0,"hunger":100,"thirst":57,"fatigue":100,"food":0,"water":1,"last_meal":49,"last_drink":121,"recoverable_deprivation_damage":100,"damage_by_origin":{"hunger":84,"both":16},"last_successful_action":{"action":"drink","turn":121},"goal":"drink","destination":null,"known_water_sources":[{"map_id":846,"x":7,"y":13},{"map_id":846,"x":2,"y":2},{"map_id":846,"x":1,"y":13}],"distance_to_water":0,"event_id":173193}. Não se conclui que o NPC poderia consumir estoque remoto apenas porque o Town tinha unidades.

### Morte #4689 — thirst h151

Lyra Valerius #4689; HP 0.0, fome 4.0, sede 100.0, fadiga 100.0; moedas 25; comida/água 0/0; posição 846:1,13; Goal forage_meal/completed

Primeira Need vital observada ≥50: {"water":50,"food":59}; conhecido mercado {"map_id":846,"x":7,"y":13}, poços [{"map_id":846,"x":2,"y":2},{"map_id":846,"x":1,"y":13}]; observação econômica {"turn":150,"town_id":846,"stock":{"food":2,"grain":1,"water":0,"iron":118,"wood":72},"temporary_work":false,"temporary_offers":{},"offers_observed_at":150,"offers_expire_at":174,"training_offer":null,"price":14,"price_turn":143}; comida/água local 3/0; passos à primeira fonte conhecida 12.

h148: Need food prioridade 100.00; escolhido forage_meal score 55.00; estado após: Lyra Valerius #4689; HP 10.0, fome 78.0, sede 100.0, fadiga 100.0; moedas 25; comida/água 0/0; posição 846:1,13; Goal forage_meal/active; execução=False, retorno=—.

| Alternativa realmente avaliada | score | alvo | termos | estimativa alimentar calculada |
| --- | --- | --- | --- | --- |
| forage_meal | 55.00 | — | {"base":0.175,"independence":0.11,"hunter":0.0,"travel":-0.01} | {"EstimatedTimeUntilFoodConsumed":2,"EstimatedSurvivalMargin":3,"economically_viable":true,"survival_viable":true,"reason":null,"known_conditions":["NoProduct","DistantProduct"]} |
| work_for_meal | 29.12 | — | {"base":0.225,"diligence":0.08375,"physical_depletion":-0.153125,"travel":-0.01} | {"EstimatedTimeUntilFoodConsumed":2,"EstimatedSurvivalMargin":3,"economically_viable":true,"survival_viable":true,"reason":null,"known_conditions":["NoProduct","DistantProduct"]} |

h149: Need food prioridade 100.00; escolhido forage_meal score 57.00; estado após: Lyra Valerius #4689; HP 6.0, fome 40.0, sede 100.0, fadiga 100.0; moedas 25; comida/água 0/0; posição 846:1,13; Goal forage_meal/completed; execução=True, retorno=[true,"Alimento coletado. Fome reduzida."].

| Alternativa realmente avaliada | score | alvo | termos | estimativa alimentar calculada |
| --- | --- | --- | --- | --- |
| forage_meal | 57.00 | — | {"base":0.175,"independence":0.11,"hunter":0.0,"travel":-0.0} | {"EstimatedTimeUntilFoodConsumed":1,"EstimatedSurvivalMargin":2,"economically_viable":true,"survival_viable":true,"reason":null,"known_conditions":["DistantProduct"]} |
| work_for_meal | 29.38 | — | {"base":0.225,"diligence":0.08375,"physical_depletion":-0.161875,"travel":-0.0} | {"EstimatedTimeUntilFoodConsumed":1,"EstimatedSurvivalMargin":2,"economically_viable":true,"survival_viable":true,"reason":null,"known_conditions":["DistantProduct"]} |

h150: Need food prioridade 100.00; escolhido forage_meal score 57.00; estado após: Lyra Valerius #4689; HP 2.0, fome 2.0, sede 100.0, fadiga 100.0; moedas 25; comida/água 0/0; posição 846:1,13; Goal forage_meal/completed; execução=True, retorno=[true,"Alimento coletado. Fome reduzida."].

| Alternativa realmente avaliada | score | alvo | termos | estimativa alimentar calculada |
| --- | --- | --- | --- | --- |
| forage_meal | 57.00 | — | {"base":0.175,"independence":0.11,"hunter":0.0,"travel":-0.0} | {"EstimatedTimeUntilFoodConsumed":1,"EstimatedSurvivalMargin":1,"economically_viable":true,"survival_viable":true,"reason":null,"known_conditions":["DistantProduct"]} |

Registro causal do motor: {"turn":151,"name":"Lyra Valerius","profession":"agricultor","town_id":846,"cause":"thirst","health":0,"hunger":4,"thirst":100,"fatigue":100,"food":0,"water":0,"last_meal":150,"last_drink":74,"recoverable_deprivation_damage":100,"damage_by_origin":{"thirst":65,"both":43},"last_successful_action":{"action":"forage_meal","turn":150},"goal":"forage_meal","destination":{"map_id":846,"x":1,"y":13},"known_water_sources":[{"map_id":846,"x":7,"y":13},{"map_id":846,"x":2,"y":2},{"map_id":846,"x":1,"y":13}],"distance_to_water":0,"event_id":207809}. Não se conclui que o NPC poderia consumir estoque remoto apenas porque o Town tinha unidades.

## 13. Competição de prioridade e dependências pessoais

| Need que perdeu | episódios observados | principais vencedoras e estágio de avaliação |
| --- | --- | --- |
| political_pressure | 211909 | [["food (not_evaluated)",104740],["rest (not_evaluated)",70860],["water (not_evaluated)",8157],["family (not_evaluated)",7592],["money (not_evaluated)",5880]] |
| organizational_survival | 100051 | [["food (not_evaluated)",47990],["rest (not_evaluated)",33034],["political_pressure (not_evaluated)",6485],["water (not_evaluated)",3551],["family (not_evaluated)",2881]] |
| affiliation | 10786 | [["food (not_evaluated)",5645],["rest (not_evaluated)",3873],["water (not_evaluated)",393],["political_pressure (not_evaluated)",336],["family (not_evaluated)",136]] |
| governance | 1859 | [["food (not_evaluated)",768],["rest (not_evaluated)",729],["money (not_evaluated)",131],["political_pressure (not_evaluated)",92],["family (not_evaluated)",43]] |
| institutional_work | 1147 | [["food (not_evaluated)",625],["rest (not_evaluated)",399],["protection (not_evaluated)",60],["security (not_evaluated)",19],["water (not_evaluated)",14]] |
| institutional_response | 0 | [] |

| Need institucional → Need vencedora | ocorrências |
| --- | --- |
| political_pressure -> food (not_evaluated) | 104740 |
| political_pressure -> rest (not_evaluated) | 70860 |
| organizational_survival -> food (not_evaluated) | 47990 |
| organizational_survival -> rest (not_evaluated) | 33034 |
| political_pressure -> water (not_evaluated) | 8157 |
| political_pressure -> family (not_evaluated) | 7592 |
| organizational_survival -> political_pressure (not_evaluated) | 6485 |
| political_pressure -> money (not_evaluated) | 5880 |
| affiliation -> food (not_evaluated) | 5645 |
| affiliation -> rest (not_evaluated) | 3873 |
| political_pressure -> food_reserve (not_evaluated) | 3560 |
| organizational_survival -> water (not_evaluated) | 3551 |
| organizational_survival -> family (not_evaluated) | 2881 |
| political_pressure -> protection (not_evaluated) | 2601 |
| political_pressure -> organizational_survival (not_evaluated) | 2319 |
| organizational_survival -> money (not_evaluated) | 1592 |
| political_pressure -> security (not_evaluated) | 1426 |
| organizational_survival -> protection (not_evaluated) | 1070 |
| political_pressure -> rest (evaluated_but_not_selected) | 1058 |
| organizational_survival -> food_reserve (not_evaluated) | 1026 |
| governance -> food (not_evaluated) | 768 |
| governance -> rest (not_evaluated) | 729 |
| institutional_work -> food (not_evaluated) | 625 |
| political_pressure -> recovery (not_evaluated) | 517 |

not_evaluated indica que a iteração normal parou antes desse Need; evaluated_but_not_selected significa que alguma avaliação foi observada, sem garantir que participou da competição final. O contador não substitui um replay completo de escolhas em todos os instantes. Não houve redução da prioridade da sobrevivência para produzir ação política.

| Processo | Dependência provada pelo código | Medida do efeito nesta campanha |
| --- | --- | --- |
| Entrega e submissão de grupo | Institutions.deliver_support: p.id==g.leader_id; submit: líder de grupo apoiador + prefeito + mercado | 31 rascunhos; 0 com representante final morto |
| Decisão política | Institutions.resolve: t.mayor_id==p.id e mercado; Society.refresh cria governance só no prefeito | 13 pendentes recebidas/deferred/ignored; 0 com prefeito final morto |
| Reunião e formalização | Society.meeting: líder presente e pares; found_faction mantém liderança | 1 grupos ativos com líder morto ao encerrar |
| Compra institucional | Institutions.execute institutional_purchase: p.id==f.leader_id e mercado | 1 efeitos institucionais totais; falhas por facção na seção 7 |
| Convite e admissão | Access.execute invite_person e membership exigem canal/membro presente; não necessariamente só líder para responder | não é um SPOF absoluto do líder: qualquer membro presente pode fornecer contato em membership |
| Trabalho de política | Institutions.worker_eligible aceita profissões; policy_work exige trabalhador apto presente | não há trabalhador único obrigatório em WATER/FOOD/SECURITY; transporte guarda job por pessoa |

Indisponibilidade estrutural é demonstrada pelas condições; número exato de horas perdidas por cada pessoa indisponível não foi registrado continuamente. Não se atribuem todos os rascunhos ou esperas exclusivamente à morte do líder. Troca de prefeito preserva quadro recebido/publicado; não preserva automaticamente o ritmo de atendimento.

## 14. Geografia e coesão

| Indicador | Resultado |
| --- | --- |
| Localidades / reinos | 49 / 4 |
| Rotas / travessias | 56 / 78 |
| JourneyStarted / Arrived | 83 / 76 |
| Auditoria de rotas | [] |

Conhecer lugar e conhecer rota são registros diferentes. search_groups restringe inicialmente à cidade de residência; acceptable_group ainda pode exigir plano para quem está fora. Um grupo globalmente compatível não gera adesão remota. Proposal usa jurisdição determinada por Collective.authority; entrega e trabalho político exigem presença no mercado. Facções podem ter HQ em POI; suprimento exige depósito ou responsável presente, não teletransporte do estoque. Caminho local, viagem por rotas, preparação de provisões e encontro com autoridade são custos distintos. A campanha verifica que as rotas usadas são válidas, mas não registra uma decomposição causal exaustiva do tempo de viagem de cada cadeia institucional.

## 15. Comparação com Vaelora-55

Fonte exclusiva da baseline: ../fase_5_5/RELATORIO_TECNICO.md, MUNDO.md e HISTORIAS_REAIS.md. Seeds e populações diferem. Além da correção autorizada do crash, Vaelora foi medida antes dos últimos ajustes 5.5 de contexto de ignore e preservação do quadro público citados no próprio relatório técnico anterior. Logo, são padrões repetidos/não repetidos e diferenças observadas, sem percentual causal atribuído à implementação.

| Métrica | Vaelora-55 | Neravon-Coesao55 |
| --- | --- | --- |
| Horas | 300 | 300 |
| Persistentes iniciais | 1880 | 1898 |
| Abstratos | 4644 | 4693 |
| Persistentes vivos finais | 1565 | 1600 |
| Mortos | 315 | 298 |
| hunger / thirst / both / combat | 175 / 126 / 13 / 1 | 160 / 127 / 10 / 1 |
| Grupos criados | 132 | 146 |
| Ativos / dissolvidos | 114 / 18 | 128 / 18 |
| Adesões | 998 | 1064 |
| Pessoas únicas com adesão | 555 | 598 |
| Maior grupo relatado (baseline) / maior lista final (nova) | 24 | 23 |
| Causas de criação | security:109; water:16; resource:7 | {"security":123,"water_access":10,"resource_pressure":11,"criminal_cooperation":2} |
| GroupSearchAttempt | 5325 | 5884 |
| ExistingGroupFound | 1230 | 1367 |
| GroupJoinRejected | 4273 | 4768 |
| Low affinity eventos | 3631 | 4243 |
| Formalizações | 0 | 0 |
| Propostas criadas | 46 | 47 |
| Reutilizações | 22 | 29 |
| Eventos de apoio | 261 | 266 |
| Entregas de apoio | 33 | 28 |
| Submissões | 16 | 16 |
| Decisões | 2 | 3 |
| Políticas | 2 | 3 |
| Trabalhos com efeito | 8 | 3 |
| Políticas concluídas | 2 | 0 |
| Convites | 19 | 9 |
| Pedidos espontâneos | 0 | 0 |
| Aceites / recusas | 4 / 1 | 2 / 0 |
| Membros finais das duas facções | 3 / 3 | [1,1] |
| FactionAction | 3 | 1 |
| Status legal mudou | 0 | 0 |
| Viagens iniciadas / concluídas | 76 / 64 | 83 / 76 |
| Rotas / travessias | 55 / 65 | 56 / 78 |
| Ataques | 417 | 462 |
| Furtos | 3190 | 3815 |
| Estoque final comida/água | 2045 / 6718 | 1505 / 6849 |
| Afinidade: distribuição de calls | não disponível na baseline | {"n":27298,"min":7.05,"p25":17.75,"median":21.45,"mean":22.0625,"p75":25.2,"p90":31.3,"max":70.25} |
| Pressões/latências distribuídas | não disponível na baseline | seções 9–10 |
| Ledger exato de churn | não disponível na baseline | seção 4 |
| Elegibilidade conhecida por política | não disponível na baseline | {"138300":6,"146540":5,"306439":4} |

| Razão entre eventos (não taxa individual) | Vaelora | Nova |
| --- | --- | --- |
| found/search | 0.23 | 0.23 |
| joins/search | 0.19 | 0.18 |
| newgroups/search | 0.02 | 0.02 |
| reuses/creates | 0.48 | 0.62 |
| submitted/created | 0.35 | 0.34 |
| decisions/submissions | 0.12 | 0.19 |
| accepts/invites | 0.21 | 0.22 |

As razões permitem comparar intensidade relativa de eventos sob os mesmos limites de emissão, não uma coorte individual. Uma proposta pode ser submetida ou decidida mais de uma vez. O maior grupo relatado em Vaelora foi 24; o novo valor é lista final, sem série completa do pico de cada mutação. A mortalidade observada foi 298 contra 315, e 297/298 mortes novas tiveram causa de privação. Isso descreve diferença entre campanhas, não efeito isolado de uma alteração. O padrão de predominância de privação deve ser avaliado junto das causas e dos rastros, não do estoque final agregado.

## 16. GARGALOS CONFIRMADOS

| Sistema / sintoma | Evidência | Código | Efeito / confiança |
| --- | --- | --- | --- |
| Adesão a grupos | Checks abaixo do limiar e repetições na seção 3 | Society.affinity + Institutions.acceptable_group | Gate de afinidade retira join e permite alternativa separada; alta para gate, não contrafactual de balanceamento |
| Formalização | Funil de reuniões/gates e top10 seção 5 | Society.meeting → Institutions.formalization | Score suficiente sozinho não basta; idade, co-presença e contribuições filtram antes; alta |
| Propostas em espera | Rascunhos, entrega, recepção, representantes/prefeitos nas seções 8–10 | Institutions.submit/resolve + Society.candidates | Continuidade depende de presença e Need do representante/autoridade; alta para condições, parcial para horas de atraso |
| Recrutamento | Termos, convites, chamadas e respostas seção 6 | Institutions.refresh/membership | Conhecimento/convite não equivale a decisão materializada; alta nos casos rastreados |
| Execução institucional | Candidatos, tentativas e efeitos seção 7 | Institutions.faction_candidates/execute | Capacidade declarada pode ficar sem execução ou falhar em gate; alta onde retorno observado |
| Sobrevivência | Mortes individuais com estoque local e últimos Goals seção 12 | GoalSystem.decide + alimentação/água/recuperação | Recursos agregados não garantem posse/consumo a tempo; alta para fatos, causas individuais detalhadas nos rastros |

Gargalo confirmado adicional de alta confiança: preparo hídrico. Houve94 mortos com repetição de fill_water depois de falha em intervalo menor que12h;13 morreram de sede carregando água. GoalSystem.preventive_choice cria o preparo depois do filtro de _evaluate. O efeito observado é gastar rodadas em fonte vazia ou adquirir sem consumir antes do fechamento; a fixture na seção 19 comprova o desvio do bloqueio, sem estimar quantas mortes uma correção evitaria.

## 17. HIPÓTESES

1. Consolidar contatos e confiança entre membros de grupos equivalentes poderia reduzir fragmentação; não foi feito experimento contrafactual e não há prova de limiar ideal. 2. Delegação de representação poderia aumentar entrega; não foi testada, pois alteraria gameplay. 3. Aumentar autonomia do trabalho institucional pode mudar execução, mas medir só oferta de capacidade não identifica impacto. 4. Uma campanha de 300h não caracteriza frequência estacionária de formalização, guerra, divindades ou colapso. 5. Estoque final positivo com mortes não prova o mesmo estoque, preço e acesso em todas as horas anteriores.

## 18. COMPORTAMENTO CORRETO MAS INDESEJADO

Fragmentar por desconhecimento/baixa afinidade cumpre a epistemologia atual; pode produzir organizações redundantes no nível mundial. Recusar ou adiar ingresso por autonomia, risco, estado físico ou custo é decisão válida. Dar prioridade à sobrevivência e exigir recursos reais para política é correto, ainda que reduza ação institucional. Formalização rara sob várias condições simultâneas não é bug por ausência de evento. Dinheiro público/faccional não é renda pessoal do prefeito/membro; um cargo rico não sustenta automaticamente seu ocupante. O projeto precisa decidir futuramente quais desses resultados deseja mudar, preservando causalidade e limites materiais.

## 19. BUGS CONFIRMADOS

**Crash em visita a POI — corrigido exclusivamente com autorização.** Geography.visit passava o nome do evento por posição e kind=point.kind como contexto, mas Geography.emit também chamava o primeiro parâmetro de kind. Resultado reproduzido: TypeError de argumento duplicado na hora26. Renomear o parâmetro para event_kind mantém o payload. A reprodução isolada e a passagem natural pela mesma hora validam a correção; o manifesto e patch preservam a alteração exata. Não foi mudada a versão conceitual.

**Enumeração/execução de suprimento institucional — não corrigido.** {"seed_fixture":"Repro-Suprimento-55","hours_simulated":0,"setup":{"faction_food":1,"faction_water":0,"hunger":40,"thirst":80,"at_headquarters":true,"is_leader":true},"enumerated_supply":true,"result":[false,"A organização não possui este recurso."],"food_remaining":1,"water_remaining":0,"main_code_changed":false,"natural_occurrence_not_inferred":true}. faction_candidates usa comida OU água para oferecer institutional_supply; execute escolhe somente o tipo da maior privação e exige esse tipo. Logo, um estoque de comida pode oferecer solução que vai falhar pedindo água. A reprodução é fixture isolada, não uma segunda campanha; sua frequência natural deve ser lida nos retornos falhos da seção 7 e não inferida da fixture.

**Critérios de formalização divergentes — não corrigido.** {"seed_fixture":"Repro-Formalizacao-55","natural_hours_simulated":0,"setup_age":168,"meetings":4,"group_members":3,"present_members":2,"contributions":4,"pressure_score":55.0,"required_pressure":65,"canonical_path_created_faction":false,"legacy_candidate_offered":true,"legacy_execution_result":[true,"Formalização custeada por membros presentes."],"factions_created":1,"founder_count":2,"main_code_changed":false,"natural_frequency_not_inferred":true}. Access.execute(formalize_organization) chama Society.found_faction diretamente e contorna o gate de score≥65/presentes≥3 de Institutions.formalization. Na fixture de idade 168 e quatro reuniões, a via nova recusou; a antiga aceitou score 55 e dois fundadores. É inconsistência concreta entre caminhos da mesma funcionalidade; não prova frequência natural. A seção 5 informa as seleções/execuções reais da ação legada.

**Preparo preventivo contorna bloqueio de ação falha — não corrigido.** {"seed_fixture":"Repro-Preparo-Agua-55","natural_hours_simulated":0,"failure_cooldown_until":12,"turn":0,"regular_evaluation_choices":0,"preventive_action":"fill_water","preventive_destination":{"map_id":3,"x":7,"y":13},"actual_execution_result":[false,"Não há água para levar nesta fonte."],"town_water":0,"main_code_changed":false}. GoalSystem._evaluate elimina fill_water durante o bloqueio de 12h; preventive_choice o recria depois da avaliação, sem respeitar failures e sem verificar estoque da fonte. A fixture produziu zero alternativas pelo caminho normal, mas uma tentativa preventiva da mesma ação, que falhou por fonte vazia. Foram observados 94 mortos com repetição desse padrão nos três últimos registros. Aquisição também é separada de beber: os 13 mortos com água mostram que chegar a possuir recurso na última hora não assegura consumo antes do fechamento fisiológico.

Nenhum outro comportamento foi promovido a bug só por parecer pouco interessante. Falha do observador inicial foi corrigida no experimento externo; o tratamento registra erros e não encobre exceções do motor. Resultado sem dado suficiente fica nas hipóteses/lacunas.

## 20. LACUNAS DE OBSERVABILIDADE

Faltam para cobertura exaustiva: retorno não-vazio de cada search e motivo individual de todos os gates; leituras/atualizações temporais completas de confiança; pico histórico de tamanho por grupo a cada mutação; exclusões voluntárias com identidade causal; pressão exata em toda entrega; último histórico de decisões de todo representante/prefeito vivo; distinção de candidatos descartados antes de _evaluate; preço/alcance/estoque de cada fonte conhecida a cada hora; horas de impedimento atribuídas exclusivamente a cada dependência; conhecimento individual explícito de todos os custos de facção. O perfil coleta apenas dados realmente existentes ou contadores de observação, sem preenchimento ficcional.

Os três últimos registros de cada morto permitem rastrear trechos finais, não reconstituir todas as 300h de Need→Goal→acesso→consumo por pessoa. O primeiro limiar vital≥50 não significa fome/sede contínua desde então. Eventos e contadores têm limites diferentes. Gates não alcançados não possuem Utility. As amostras de criação são iniciais, não aleatórias. Esses limites devem acompanhar qualquer conclusão futura baseada neste diagnóstico.

## 21. Recomendações priorizadas — não implementadas

| Prioridade | Proposta de trabalho futuro | Por quê / como validar |
| --- | --- | --- |
| P0 | Manter regressão para o crash de POI e harmonizar assinatura/payload de eventos equivalentes | Evita interrupção estrutural; reprodução isolada já documentada, regras preservadas |
| P0 | Fazer preparo preventivo respeitar falhas e adequação fisiológica da ação | Há repetição natural de fill_water sem estoque apesar do bloqueio; consumo crítico precisa de continuidade verificável antes do próximo dano, sem criar água |
| P1 | Alinhar disponibilidade específica e localização de institutional_supply na enumeração e execução | Remove alternativa materialmente impossível; bug reproduzido isoladamente, sem falha natural dessa ação nesta seed |
| P1 | Unificar critérios entre a ação legada de formalização e a via de reunião | Evita critérios contraditórios; reproduzido isoladamente, sem formalização natural nesta seed |
| P1 | Instrumentar gates e retomadas com motivos por etapa e identidade de entidade | Separa conhecimento, prioridade, presença, dinheiro e material; medir funis por coorte antes de rebalancear |
| P1 | Rever continuidade de representação e atendimento quando titular está indisponível | Processos existentes dependem de indivíduos; avaliar delegação/sucessão com contato real, sem entrega automática |
| P1 | Estudar consolidação baseada em contato e objetivo compartilhado | Reduz duplicação artificial sem conceder conhecimento global ou forçar simpatia; comparar seeds controladas |
| P1 | Validar acesso individual a comida/água e previsão de margem fisiológica nos casos da seção 12 | Ataque causal às mortes, preservando moeda, estoque e prioridade vital; repetir casos identificados com novos testes curtos |
| P2 | Reavaliar gates conjuntos de formalização após observar mais coortes maduras | A ausência em300h não exige baixar thresholds; medir reuniões, renda e co-presença |
| P2 | Alinhar benefícios anunciados e serviços executáveis de facção | Distinguir capacidade, compromisso e entrega, sem fabricar ação para produzir lore |
| P2 | Revisar retenção de propostas ligadas a políticas concluídas | O limite24 com objetos protegidos é risco de longo prazo; não extrapolar para falha natural não observada |

Nenhuma recomendação comportamental foi aplicada. PROJECT.md descreve o código atual; LIMPEZA.md registra o corte de artefatos. Este relatório é diagnóstico, não nova fase, campanha de lore ou especificação já implementada.
