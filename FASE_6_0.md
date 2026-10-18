# FASE 6.0 — aprofundamento sistêmico e coerência causal

Base `mvp-13-fase5.5.5` → regras **mvp-14-fase6.0**. Geração **mvp-6.0**; save **formato 2**. Seleção pela primeira Need solucionável preservada. **366 testes passaram**, incluindo os 341 anteriores; controles de neutralidade e continuidade passaram. Campanha **Arvandor-Coerencia60**, nova, do zero, **300h**, quatro reinos, sem jogador, historical_turns=0. Duas falhas nos scripts de exportação/comparação exigiram duas reproduções da mesma seed para recuperar arquivos: três execuções de300h, 900h de simulação ao todo, sem escolha de resultado ou alteração do código do jogo.

## 1. Baseline e hipóteses

Na 5.5.5 houve 274 mortes: 270 por privação, 4 por combate; 388 ataques, 147 grupos, 1.038 adesões, 52 propostas, 10 submissões e 4 políticas concluídas. A suíte inicial tinha 341 testes verdes. O problema da fase não era ausência de sistemas: era a capacidade de completar os ciclos.

O levantamento novo preservado em [reports/fase_6_0/capacidade_base.json](</home/hugo/Área de trabalho/procedrual/reports/fase_6_0/capacidade_base.json>) encontrou capitais com 103 NPCs presentes, demanda hídrica fisiológica de 109,87 unidades/dia e reposição 80. O censo persistente planejado é 104, que exige 110,93/dia. As vilas e cidades comuns não apresentam esse déficit nominal. O controle inicial de 72h na versão antiga não registrou mortes: isso não invalida um déficit acumulativo.

Hipóteses: infraestrutura abaixo do consumo produz emergência estrutural; um trabalho local inviável pode monopolizar Need; afinidade pessoal isolada pode impedir consolidação de grupos; líder exclusivo pode interromper entregas; conhecimento de um guarda em campo não equivale a depósito institucional; raridade religiosa precisa de gates observáveis.

## 2. Mudanças realizadas

- **Água inicial:** dimensionamento depois da densificação, pelo censo final e número real de poços. Demanda = persistentes × 24 × 2/45. Capacidade mínima histórica 80; acima disso, arredondamento por fonte física. Storage = dois dias da capacidade. Estoque inicial continua 80. Sem poços, capacidade projetada zero. Instalação existente é uma fonte passiva; não se inventaram operadores ou bombeamento laboral. O modelo hidrológico anterior continua, sem seca nova ou recurso retirado de outro estoque.
- **Demanda local:** visitantes físicos passam a integrar a demanda alimentar administrativa; seu censo residencial permanece na origem.
- **Emprego:** gate local compartilhado explica NO_PAYER, NO_INPUT, SATURATED e INCOMPATIBLE. Estoque verdadeiro só bloqueia na instalação; oferta remota não é radar. Quem está desempregado pode gerar Need de renda/trabalho quando observou oportunidade real.
- **Carreira:** TrainingOpportunity explicita profissão, instrutor/instituição, progresso, custo, insumo e local. Cozinha mantém formação institucional em taverna; agricultor, mineiro, lenhador, caçador e ferreiro exigem instrutor presente e demanda publicada. A prática produz, usa insumos aplicáveis e remunera do caixa existente. Não há árvore RPG. Materialização continua exigindo déficit persistente, abstrato, reservas e ausência de candidato local; profissional compatível residente fora com rota conhecida também impede materialização precipitada.
- **Organizações:** OrganizationalCompatibility separada de SocialAffinity. Causa, objetivo, estratégia conhecida, localidade, efetividade comunicada, custos, autonomia, adesões e hostilidade compõem a avaliação. Afinidade isolada deixa de ser o gate inteiro. JOIN continua precedendo CREATE; hostilidade, estratégia incompatível, capacidade e desconhecimento ainda permitem grupos distintos.
- **Continuidade:** InstitutionalTask persiste com emissor, instituição, tipo, alvo, local, criação, prioridade, requisitos, papéis autorizados, status, tentativas e barreira. Entrega, resposta, reunião e trabalho de política usam ações humanas existentes. Representantes são autorizados por contato; tarefa precisa ser conhecida, e execução revalida presença/autorização. O estado conhecido da tarefa é individual: conclusão distante só encerra a intenção após notícia ou leitura de comprovante no local. Prefeitura pode designar funcionários presentes para receber documentos; decisão política continua do prefeito. Policy work aceita rotação de trabalhadores habilitados e informados.
- **LOD:** mantém 1/3/6/12 horas conforme o estado original; perseguição conhecida e obrigação urgente promovem temporariamente resolução, sem promoção universal por qualquer Need. Emergência vital já promovia resolução de uma hora e continua com prioridade máxima.
- **Justiça:** conhecimento adquirido em campo só vira registro compartilhável quando o guarda chega ao serviço local; mantém latência e presença para outro guarda aprender. Casos, pistas, atribuições e captura usam o sistema existente. Sem fato conhecido não existe captura autorizada.
- **Violência e religião:** arquitetura letal e critérios de audiência/intervenção preservados. Audiência agora informa separadamente falta de mensagem, presença/acesso, energia e cooldown. Não houve redução de thresholds para produzir mortes ou milagres.
- **Observabilidade V1.1:** métricas privadas por episódio, fluxos de itens, janelas por Town, crescimento fisiológico entre decisões, funis e casos. Metadados mínimos preservam emissões ordinárias descartadas, com kind/turn/ator/alvo/local/pais; não se reconstrói verdade a partir de rumores.

## 3. Mudanças rejeitadas e limites de escopo

Não houve global action utility, redução de fome/sede/dano ou prioridade de sobrevivência, renda gratuita para persistentes, água multiplicada por um fator arbitrário para a capital, polícia telepática, spawn de facção, quota de história ou intervenção divina automática. Não houve banco novo, compressão estrutural do save, demografia ou mudança hora→turno.

Não se acrescentou continuação genérica Acquire→Consume: refeições emergenciais já existem no motor; a presença de recurso ao morrer deve ser examinada por caso e não prova, sozinha, atraso fatal de consumo. Eventos raros não foram forçados. Reunião não substitui a regra canônica de formalização.

## 4. Testes e controles

366 testes PASS; **25 testes causais novos**, nenhum teste removido/ignorado. Os testes antigos de alimentação foram isolados de emergências aleatórias de parentes da nova geração. O teste de pagador ausente foi fortalecido para exigir bloqueio antes da tentativa improdutiva, em vez de exigir uma primeira falha deliberada. As rodadas intermediárias com falhas estão preservadas; não representam o resultado final.

Os 25 controles pequenos cobrem: capital dimensionada e fonte ausente; capacidade sem produção; visitante; emergência ACTIVE/BACKGROUND; promoção por obrigação conhecida; trabalho sem pagador/insumo e com remuneração; ausência de radar remoto; desempregado com oferta; instrutor ausente/presente e mudança profissional; afinidade baixa com causa comum e hostilidade/estratégia contrária; delegado com líder ausente e save/load; tarefa desconhecida, conclusão distante sem recebimento e continuidade do endereço de aprendizagem; formalização 167/200h; crime em campo versus depósito; guarda sem fato versus captura de rendido; deus sem mensagem versus todos os gates válidos; tombstone; Need preterida/solvabilidade desconhecida; crescimento fisiológico e recurso no inventário ao morrer.

Um controle adicional executou o pipeline completo de carreira: oportunidade conhecida, reserva e aspiração de competência; em 16 decisões reais, a Need selecionou train e o desempregado tornou-se cozinheiro. Não se chamou train diretamente. Evidência: [reports/fase_6_0/controle_carreira_pipeline.json](</home/hugo/Área de trabalho/procedrual/reports/fase_6_0/controle_carreira_pipeline.json>).

Neutralidade: OFF/NORMAL/AUDIT, 36h cada, estado de gameplay completo, metadados de Events e RNG idênticos. Continuidade: 100h contínuas = 50h→save/load→50h em todos os campos. Smoke: quatro reinos, 12h, invariantes e geografia válidas.

### A/B causal de infraestrutura

| Medida | Capacidade antiga no motor 6.0 | Capacidade dimensionada no motor 6.0 |
| --- | --- | --- |
| Seed | Controle-Capacidade60 | Controle-Capacidade60 |
| Horas | 144 | 144 |
| Mortes | 32 | 13 |
| Causas | {'thirst': 20, 'hunger': 9, 'both': 3} | {'hunger': 12, 'thirst': 1} |
| Fração de decisões de sobrevivência | 70.61% | 70.71% |
| Furtos de mercado | 868 | 863 |
| Propostas criadas | 38 | 35 |

Os dois braços usam o mesmo mundo inicial 6.0, mesmas pessoas, inventários e RNG. A única alteração é capacidade/armazenamento de água: antiga 80/160 contra dimensionamento inicial. Ambos mantêm as outras correções 6.0. A comparação por identidade registrou estas transições: {'thirst -> not_dead_by_deprivation': 19, 'hunger -> hunger': 8, 'not_dead_by_deprivation -> hunger': 3, 'thirst -> hunger': 1, 'both -> not_dead_by_deprivation': 3, 'hunger -> not_dead_by_deprivation': 1, 'not_dead_by_deprivation -> thirst': 1}. Não houve mortes não relacionadas à privação nem materializações nos dois braços. O saldo é 23 indivíduos vivos em vez de mortos e quatro mortes novas dentro do horizonte de144h; não implica imunidade futura. Esse é um controle isolado da infraestrutura; não é um A/B de toda a versão antiga contra a nova. Mudanças em furto ou política desse par são efeitos observados, sem mecanismo de restauração de taxas.

## 5. Campanha natural e comparação histórica

| Métrica | Vaelora-55 | Neravon-Coesao55 | Thalven-Radiografia55 | Elyndar-Estabilidade555 | Arvandor-Coerencia60 |
| --- | --- | --- | --- | --- | --- |
| Persistentes iniciais | 1880 | 1898 | 1916 | 1862 | 1880 |
| Mortes | 315 | 298 | 342 | 274 | 123 |
| hunger / thirst / both / combat | 175/126/13/1 | 160/127/10/1 | 202/126/14/0 | 132/125/13/4 | 116/3/2/2 |
| NewGroupCreated | 132 | 146 | 144 | 147 | 61 |
| GroupJoined | 998 | 1064 | 1075 | 1038 | 1112 |
| ProposalCreated | 46 | 47 | 46 | 52 | 40 |
| ProposalSubmitted | 16 | 16 | 13 | 10 | 25 |
| PolicyDecided | 2 | 3 | 4 | 4 | 5 |
| PolicyCompleted | 2 | 0 | 2 | 4 | 3 |
| Formalização de facções | 0 | 0 | 0 | 0 | 0 |

Todas as campanhas têm 300h. Seeds, populações, regras e agora geração diferem: a tabela é comparação descritiva, não percentual causal de melhoria. O A/B acima é a evidência da intervenção hídrica isolada. A primeira execução completou300h com invariantes válidas e salvou as métricas, mas o exportador não converteu um Location presente em metadados de pai causal. O problema foi corrigido somente no exportador. A primeira reprodução também completou300h com os mesmos dados JSON; uma comparação direta entre chaves int em memória e str no JSON interrompeu a exportação. Esse erro do exportador foi corrigido com normalização e checkpoint completo anterior à análise. A reprodução final usa as mesmas fontes de jogo/testes e compara todas as métricas finais e os12checkpoints com a primeira execução. Falha e log originais são preservados; nenhum resultado foi escolhido por ser mais interessante.

| Causa | Mortes |
| --- | --- |
| both | 2 |
| combat | 2 |
| hunger | 116 |
| thirst | 3 |

Privação: **121/123** mortes. Fração das seleções por Need de sobrevivência: **82.60%**. Em **85** mortes havia food no mercado municipal local, mas a carteira não cobria uma unidade (49 sem dinheiro; 36 com valor insuficiente). Isso é estado econômico observado no óbito, não prova de que o NPC sabia do estoque ou conseguiria chegar a tempo. A fração de seleções não mede horas de ação e inclui preparo que pode trocar a ação sem trocar a Need selecionada.

As 12 conferências de 25h das três execuções passaram nas invariantes e geografia. O saldo monetário foi explicado pela fonte abstrata existente; residual zero, inclusive com mortos, tesourarias, caixa abstrato, grupos, facções e políticas. Dinheiro inicial 140956, final 141244, fonte explícita 288. A economia não é monetariamente fechada: trabalho abstrato já emite moeda e isso continua declarado.

## 6. Need starvation

| Need | Episódios | Horas ativas | Topo | Solvável observado | Solvabilidade desconhecida | Selecionada | Executada | Sucesso | Preterida | Nunca selecionada | Latência média / máxima (h) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| advancement | 1265 | 293417 | 5615 | 139101 | 151307 | 1995 | 1583 | 1520 | 137142 | 903 | 10.157 / 216 |
| affiliation | 75 | 15710 | 0 | 0 | 15699 | 1 | 1 | 1 | 0 | 74 | 7.0 / 7 |
| assistance | 1 | 14 | 0 | 0 | 14 | 0 | 0 | 0 | 0 | 1 | None / None |
| divine_contact | 177 | 38108 | 874 | 382 | 37691 | 394 | 261 | 259 | 0 | 92 | 14.424 / 147 |
| exploration | 87 | 18133 | 3 | 1 | 18131 | 1 | 1 | 1 | 0 | 86 | 16.0 / 16 |
| family | 8319 | 400333 | 58295 | 184272 | 176831 | 12117 | 9137 | 5529 | 173365 | 4738 | 9.695 / 171 |
| food | 17145 | 407499 | 159586 | 156493 | 249856 | 120063 | 50723 | 45199 | 49377 | 2016 | 11.292 / 26 |
| food_reserve | 6086 | 491124 | 23306 | 10383 | 480350 | 9281 | 5730 | 5080 | 14 | 2187 | 29.275 / 257 |
| governance | 94 | 4404 | 251 | 91 | 4313 | 89 | 45 | 45 | 0 | 61 | 14.667 / 111 |
| grief | 24 | 1074 | 0 | 681 | 393 | 3 | 3 | 3 | 681 | 21 | 14.333 / 41 |
| healing | 51 | 3079 | 0 | 2 | 3040 | 2 | 2 | 2 | 0 | 50 | 74.0 / 74 |
| institutional_task | 225 | 31594 | 29 | 45 | 31519 | 43 | 36 | 34 | 0 | 216 | 121.889 / 228 |
| institutional_work | 38 | 2422 | 16 | 18 | 2387 | 18 | 15 | 14 | 0 | 30 | 30.375 / 44 |
| migration | 3051 | 318598 | 287 | 419 | 317746 | 425 | 283 | 282 | 5 | 2917 | 27.858 / 225 |
| military_service | 325 | 15077 | 694 | 289 | 14673 | 271 | 187 | 167 | 0 | 178 | 8.082 / 106 |
| money | 2222 | 335676 | 16478 | 41914 | 289934 | 7807 | 4831 | 4358 | 34116 | 1087 | 46.942 / 274 |
| organizational_access | 2 | 598 | 0 | 7 | 587 | 7 | 5 | 4 | 0 | 0 | 8.0 / 16 |
| organizational_survival | 1113 | 257231 | 11535 | 4486 | 251092 | 4226 | 3398 | 3363 | 22 | 397 | 35.739 / 261 |
| political_pressure | 2965 | 396977 | 27674 | 12036 | 384084 | 11855 | 10270 | 9725 | 105 | 1398 | 13.414 / 244 |
| power | 14 | 214 | 27 | 5 | 209 | 5 | 5 | 5 | 0 | 12 | 0.0 / 0 |
| protection | 3690 | 306125 | 1927 | 169934 | 131667 | 1968 | 1651 | 1310 | 168476 | 3065 | 40.602 / 267 |
| pursuit | 1586 | 46902 | 290 | 226 | 46424 | 226 | 134 | 134 | 4 | 1554 | 27.406 / 97 |
| recognition | 145 | 41369 | 156 | 54 | 41262 | 54 | 31 | 1 | 0 | 122 | 16.739 / 129 |
| recovery | 853 | 62602 | 162 | 303 | 61943 | 301 | 58 | 53 | 2 | 827 | 69.269 / 131 |
| religious_interest | 5855 | 247965 | 671 | 177 | 247670 | 208 | 192 | 192 | 1 | 5660 | 19.369 / 258 |
| response | 1654 | 92834 | 929 | 531 | 91713 | 619 | 521 | 510 | 10 | 1471 | 9.705 / 189 |
| rest | 3553 | 501551 | 145356 | 83128 | 417004 | 83646 | 31823 | 31808 | 163 | 92 | 27.57 / 265 |
| revenge | 3255 | 72004 | 119 | 48596 | 23225 | 94 | 71 | 64 | 49390 | 3239 | 39.562 / 121 |
| security | 1861 | 13725 | 464 | 603 | 13091 | 1954 | 1477 | 1477 | 38 | 391 | 1.852 / 163 |
| spatial_journey | 104 | 3844 | 313 | 373 | 3460 | 373 | 373 | 373 | 0 | 49 | 16.2 / 222 |
| status | 599 | 85464 | 1558 | 44423 | 39634 | 573 | 445 | 440 | 44011 | 392 | 7.227 / 212 |
| water | 14838 | 433448 | 18188 | 158537 | 274870 | 11617 | 11263 | 11257 | 159576 | 7256 | 21.435 / 143 |
| work | 23963 | 227002 | 7908 | 24390 | 200998 | 2041 | 1596 | 1580 | 22120 | 22817 | 1.455 / 9 |

Horas ativas contam episódios conhecidos pelo motor; o topo é o ranking da última decisão real até a seguinte. Não se executa planejamento COMMAND extra para medir alternativas. Solvabilidade só é afirmada por avaliação real daquela hora ou probe puro de alternativa imediata/local. O restante é **UNKNOWN**, inclusive necessidades inferiores não avaliadas. Portanto zero em solvable_hours não significa impossibilidade; nunca selecionada não significa automaticamente monopolização. Preterida exige alternativa observada e Need superior vencedora. Não se extrapola estoque entre decisões. Reativações, expirações e resolução por episódio estão no JSON.

## 7. Sustentabilidade por Town

Última janela diária completa, h288. Produção nominal é potencial com profissionais/infraestrutura, não garantia de output. Realizado food é a janela anterior; water é reposição efetiva da janela fechada. Estoques são posteriores à reposição/consumo administrativo.

| Local | Tipo | Persistentes presentes | Abstratos | Food / water / grain | Potencial food / water por dia | Realizado food / water na janela | Dias de reserva food / water | Moedas medianas |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Karlen | capital | 91 | 218 | 0 / 163 / 2 | 320 / 111 | 28 / 111 | 0.0 / 1.679 | 0 |
| Morlen | vila | 18 | 49 | 164 / 160 / 52 | 100 / 80 | 26 / 21 | 7.257 / 8.333 | 2.0 |
| Sildor | cidade | 58 | 150 | 15 / 160 / 164 | 220 / 80 | 50 / 76 | 0.209 / 2.586 | 1.0 |
| Karmar | vila | 16 | 49 | 69 / 160 / 8 | 80 / 80 | 14 / 19 | 3.416 / 9.375 | 4.0 |
| Eliria | vila | 18 | 49 | 46 / 160 / 56 | 100 / 80 | 19 / 17 | 2.035 / 8.333 | 5.0 |
| Sillen | cidade | 55 | 150 | 12 / 160 / 69 | 200 / 80 | 57 / 50 | 0.176 / 2.727 | 0 |
| Norlen | vila | 17 | 49 | 23 / 160 / 103 | 100 / 80 | 33 / 24 | 1.075 / 8.824 | 7 |
| Kardor | vila | 18 | 49 | 28 / 160 / 152 | 100 / 80 | 17 / 17 | 1.239 / 8.333 | 7.0 |
| Sillen | cidade | 58 | 150 | 8 / 160 / 15 | 200 / 80 | 33 / 65 | 0.112 / 2.586 | 1.0 |
| Elithon | vila | 18 | 49 | 63 / 160 / 74 | 100 / 80 | 12 / 17 | 2.788 / 8.333 | 4.0 |
| Elimar | cidade | 57 | 150 | 13 / 160 / 7 | 200 / 80 | 62 / 73 | 0.185 / 2.632 | 1 |
| Armir | vila | 16 | 49 | 29 / 160 / 92 | 100 / 80 | 43 / 15 | 1.436 / 9.375 | 6.0 |
| Normar | capital | 98 | 218 | 8 / 111 / 51 | 300 / 111 | 105 / 111 | 0.067 / 1.062 | 0.0 |
| Dormar | vila | 18 | 49 | 9 / 160 / 132 | 100 / 80 | 24 / 13 | 0.398 / 8.333 | 4.0 |
| Silria | cidade | 57 | 150 | 33 / 160 / 23 | 200 / 80 | 58 / 78 | 0.469 / 2.632 | 1 |
| Ardor | vila | 18 | 49 | 61 / 160 / 24 | 100 / 80 | 23 / 17 | 2.699 / 8.333 | 6.0 |
| Arria | vila | 19 | 49 | 57 / 160 / 12 | 100 / 80 | 30 / 17 | 2.395 / 7.895 | 3 |
| Valthon | cidade | 59 | 150 | 113 / 160 / 12 | 220 / 80 | 101 / 65 | 1.552 / 2.542 | 0 |
| Elidor | vila | 18 | 49 | 129 / 160 / 14 | 100 / 80 | 39 / 12 | 5.708 / 8.333 | 3.5 |
| Karlen | vila | 15 | 49 | 49 / 160 / 50 | 80 / 80 | 15 / 13 | 2.579 / 10.0 | 3 |
| Arvia | cidade | 55 | 150 | 15 / 160 / 240 | 200 / 80 | 61 / 57 | 0.221 / 2.727 | 0 |
| Silthon | vila | 18 | 49 | 15 / 160 / 86 | 100 / 80 | 24 / 6 | 0.664 / 8.333 | 1.0 |
| Elimir | cidade | 59 | 150 | 16 / 160 / 1 | 200 / 80 | 41 / 77 | 0.22 / 2.542 | 0 |
| Karlen | vila | 17 | 49 | 21 / 160 / 61 | 100 / 80 | 25 / 22 | 0.981 / 8.824 | 1 |
| Dorlen | capital | 98 | 218 | 27 / 120 / 58 | 330 / 111 | 120 / 111 | 0.226 / 1.148 | 1.0 |
| Elimar | vila | 15 | 49 | 60 / 160 / 8 | 100 / 80 | 16 / 11 | 3.158 / 10.0 | 3 |
| Ardor | cidade | 53 | 150 | 10 / 160 / 28 | 200 / 80 | 30 / 67 | 0.152 / 2.83 | 1 |
| Karvia | vila | 18 | 49 | 98 / 160 / 0 | 100 / 80 | 12 / 19 | 4.336 / 8.333 | 3.5 |
| Nordor | vila | 19 | 49 | 119 / 160 / 28 | 100 / 80 | 18 / 19 | 5.0 / 7.895 | 5 |
| Valdor | cidade | 60 | 150 | 17 / 160 / 59 | 200 / 80 | 56 / 64 | 0.23 / 2.5 | 1.0 |
| Dorvia | vila | 17 | 49 | 99 / 160 / 31 | 100 / 80 | 18 / 23 | 4.626 / 8.824 | 3 |
| Eliria | cidade | 58 | 150 | 16 / 160 / 75 | 200 / 80 | 63 / 76 | 0.223 / 2.586 | 1.0 |
| Silria | vila | 16 | 49 | 6 / 160 / 93 | 100 / 80 | 12 / 21 | 0.297 / 9.375 | 3.5 |
| Northon | vila | 19 | 49 | 19 / 160 / 0 | 100 / 80 | 18 / 22 | 0.798 / 7.895 | 3 |
| Valthon | cidade | 58 | 150 | 32 / 160 / 47 | 200 / 80 | 52 / 71 | 0.447 / 2.586 | 0.0 |
| Dorvia | vila | 18 | 49 | 25 / 160 / 10 | 100 / 80 | 6 / 15 | 1.106 / 8.333 | 5.0 |
| Dorvia | vila | 19 | 49 | 95 / 160 / 0 | 100 / 80 | 8 / 22 | 3.992 / 7.895 | 6 |
| Valvia | capital | 72 | 218 | 2 / 137 / 2 | 240 / 111 | 61 / 111 | 0.023 / 1.784 | 2.0 |
| Dorlen | vila | 18 | 49 | 57 / 160 / 4 | 100 / 80 | 49 / 20 | 2.522 / 8.333 | 4.5 |
| Valvia | cidade | 57 | 150 | 24 / 160 / 240 | 200 / 80 | 72 / 58 | 0.341 / 2.632 | 1 |
| Arvia | vila | 18 | 49 | 3 / 160 / 82 | 100 / 80 | 21 / 18 | 0.133 / 8.333 | 4.5 |
| Ardor | cidade | 56 | 150 | 31 / 160 / 1 | 200 / 80 | 47 / 71 | 0.448 / 2.679 | 0.0 |
| Eliria | vila | 18 | 49 | 93 / 160 / 26 | 100 / 80 | 51 / 17 | 4.115 / 8.333 | 5.0 |
| Vallen | cidade | 59 | 150 | 5 / 160 / 5 | 200 / 80 | 30 / 54 | 0.069 / 2.542 | 1 |
| Valven | vila | 17 | 49 | 69 / 160 / 119 | 100 / 80 | 15 / 20 | 3.224 / 8.824 | 5 |
| Mormar | cidade | 59 | 150 | 22 / 160 / 52 | 180 / 80 | 74 / 69 | 0.302 / 2.542 | 1 |
| Armar | vila | 18 | 49 | 80 / 160 / 62 | 100 / 80 | 4 / 12 | 3.54 / 8.333 | 5.0 |
| Elimar | vila | 18 | 49 | 19 / 160 / 4 | 120 / 80 | 3 / 25 | 0.841 / 8.333 | 4.5 |

Todas as janelas, preços, acessibilidade, consumo e affordability estão no JSON. Contadores de consumo são cumulativos; subtraia linhas adjacentes para obter o fluxo diário. Consumo de água de abstratos é **0 porque não está modelado**, não porque se demonstrou que abstratos não precisam beber. Não se acrescentou fisiologia demográfica nesta fase. Estoque não garante conhecimento, rota, dinheiro, aquisição ou tempo.

### Funil das mortes por privação

| Fator documentado | Mortes com o fator |
| --- | --- |
| TRAVEL_TIME | 81 |
| PRIORITY_COMPETITION | 66 |
| NO_MONEY | 49 |
| AFFORDABILITY | 36 |
| LOCAL_SHORTAGE | 29 |
| OTHER_UNKNOWN | 4 |

Fatores podem coexistir. WORLD_SHORTAGE exige ausência de item material no mundo; LOCAL_SHORTAGE é estoque comercial municipal local zero; não avalia todo POI, depósito de facção, recurso silvestre ou fonte não comercial. Essa limitação impede tratá-lo sozinho como explicação definitiva de acesso. Material existente pode pertencer a morto ou estar inacessível. RESOURCE_OWNED_AT_DEATH é evidência de posse; não prova que um agente fisicamente capaz tinha ação livre para consumir. PRIORITY_COMPETITION e gates recentes são associações documentadas, não contrafactual automático de evitabilidade. Ausência de evidência permanece OTHER_UNKNOWN. Cada caso conserva níveis, inventário, posição/goal, última decisão e timestamps disponíveis.

## 8. LOD e fisiologia

| LOD | Decisões | Episódios críticos | Mortes por privação | Horas entre decisões: média | Crescimento de fome entre decisões: média | Sede: média | Fadiga: média |
| --- | --- | --- | --- | --- | --- | --- | --- |
| active | 156640 | 1221 | 121 | 1.08 | 1.9 | 2.16 | 0.79 |
| local | 113512 | 9296 | 0 | 3.27 | 6.54 | 6.54 | 3.56 |
| background | 2392 | 136 | 0 | 5.83 | 11.66 | 11.66 | 7.0 |

Crescimento soma a fisiologia efetivamente aplicada entre oportunidades, com clamp em 100, separado do saldo líquido depois de comer/beber. Decisões são agrupadas pelo LOD da oportunidade; o primeiro intervalo de cada pessoa não compõe a média. Mortes da tabela são as por privação. Contagem de todas as mortes pelo último LOD de decisão conhecido, incluindo combate: **{'active': 123}**; sem registro: 0. Esse último LOD não é um novo snapshot físico inventado do instante da morte. Latência por LOD da primeira seleção: {'local': {'observations': 31648, 'mean': 17.085882204246715, 'maximum': 267}, 'active': {'observations': 8701, 'mean': 19.831743477761176, 'maximum': 274}, 'background': {'observations': 1487, 'mean': 11.72763954270343, 'maximum': 258}}. Não há experimento que demonstre neutralidade estatística completa de toda vida social por LOD; o controle pequeno demonstra resposta vital equivalente em emergência local.

## 9. Trabalho, carreira e continuidade

| Medida nativa | Valor |
| --- | --- |
| work_attempts | 14629 |
| work_produced | 36036 |
| work_paid | 24437 |
| work_credit_sixths | 146750 |
| training_opportunities_observed | 0 |
| task_delegated | 55 |
| TrainingStarted | 0 |
| TrainingProgress | 0 |
| ProfessionChanged | 0 |
| WorkerMaterialized | 0 |
| InstitutionalTaskCompleted | 53 |
| InstitutionalCaseFiled | 1778 |
| InstitutionalCaseShared | 1014 |
| CharacterCaptured | 3 |

Training opportunities observed conta exposições a oportunidades, não vagas únicas. Produção e pagamento de trabalho são contabilizados separadamente; serviços podem pagar sem criar item. O salário sempre sai do pagador. Tentativas de trabalho que falharam fora de uma decisão real não criam efeitos privados persistentes. Tarefas: {'total': 168, 'statuses': {'pending': 75, 'completed': 88, 'blocked': 5}, 'kinds': {'hold_meeting': 118, 'deliver_proposal': 40, 'work_policy': 5, 'return_response': 5}, 'delegated_successes': 42}. Conclusões com morte anterior do emissor comprovada por ordem de Events: []. A métrica geral de delegação compara executor e emissor; sozinha não prova ausência física do emissor. Políticas: {'total': 5, 'statuses': {'completed': 3, 'stalled': 1, 'active': 1}, 'worker_rotation': 2}. Não se trata rotação como mudança de dono da política.

## 10. Grupos, facções e formalização

Recusas observadas por causa: {'contact_or_capacity': 86, 'hostility_or_distrust': 2, 'inactive': 14}.

Grupos finais: {'objects': 61, 'statuses': {'active': 58, 'dissolved': 3}, 'memberships': 1191}. Facções finais: 2. Fragmentação registra grupos conhecidos, score/motivos, distância, lotação, relação e lacuna de conhecimento. Grupo semelhante desconhecido não é deduplicado por varredura global do NPC.

| Gate de formalização | Ocorrências de avaliação |
| --- | --- |
| INSUFFICIENT_FUNDS | 24 |
| LOW_INVESTMENT | 56 |
| LOW_SCORE | 57 |
| NO_CONTRIBUTIONS | 24 |
| NO_LEADER | 32 |
| NO_PRESENT_MEMBERS | 7 |
| TOO_FEW_MEMBERS | 3 |
| TOO_YOUNG | 48 |

Requisitos 4 investimentos, 168h, 3 membros, 3 presentes, contribuição real e score 65 preservados. O funil conta avaliações realmente feitas; grupos que não chegaram a uma candidatura não recebem um score fictício. Um mesmo candidato pode falhar vários gates; não somar essa tabela como grupos distintos. A ausência de formalização não foi mascarada com limiar menor.

## 11. Crime, violência e religião

| Etapa | Eventos |
| --- | --- |
| ItemStolen | 3359 |
| PersonalItemStolen | 0 |
| WantedIssued | 1780 |
| InstitutionalCaseFiled | 1778 |
| InstitutionalCaseShared | 1014 |
| InvestigationClue | 1575 |
| PursuitSearch | 440 |
| SuspectLocated | 14 |
| CharacterCaptured | 3 |
| GuardResponded | 1302 |
| PursuitEnded | 33 |
| CharacterAttacked | 311 |
| CharacterIncapacitated | 8 |
| ExecutionOpportunity | 6 |
| TerminalDecision | 5 |
| IncapacitatedSpared | 4 |
| FirstAidGiven | 1 |
| CharacterWithdrew | 11 |
| CharacterFled | 150 |
| CharacterSurrendered | 68 |
| ApologyGiven | 17 |
| RestitutionGiven | 0 |
| ConflictForgiven | 2 |

Motivos refinados dos ataques pelos flags explícitos, mode auditado/parent e Need: **{'protective': 119, 'self_defense': 157, 'other_or_unknown': 7, 'law_enforcement': 25, 'retributive': 3}**. Dano registrado nos Events de ataque: 1506 HP, sem atribuir dano de privação a combate. Latências institucionais: {'proposal_to_first_decision': {'observations': 5, 'mean': 126.0, 'maximum': 169}, 'policy_to_completion': {'observations': 3, 'mean': 44.0, 'maximum': 75}, 'proposal_to_first_submission': {'observations': 25, 'mean': 66.2, 'maximum': 248}}. Crimes e testemunhas, recebimentos pela autoridade e desfechos estão nos contadores nativos. Testemunha aqui significa terceiro além dos participantes registrado no Event. Gravidade e captura não usam posição atual remota como pista. A arquitetura letal permanece motive→decisão→acesso→ataque→incapacidade→desfecho. Os números não são quota de mortes.

| Etapa | Contagem de eventos |
| --- | --- |
| SacredSiteKnown | 1834 |
| PrayerOffered | 45 |
| DivineMessage | 74 |
| DivineAccessAchieved | 13 |
| DivineAudience | 0 |
| DivineIntervention | 0 |
| DivineContractOffered | 0 |
| DivineContractAccepted | 0 |
| DivineContract | 0 |
| Apotheosis | 0 |

Mensagens recebidas, presença regional, energia, afinidades e gates de audiência usam estado informado da divindade. A classificação nativa de motivos de ataques é uma heurística de contexto; o audit detalhado e seus Facts devem confirmar a motivação, especialmente em response e em casos hedonistas. O controle com todos os gates válidos prova acessibilidade, não frequência natural garantida. Zero em audiência/apoteose é permitido. Não foi introduzido favorecimento automático.

## 12. Retenção e casos reais

61679 Events históricos, 7173 traces retidos e 65524 metadados mínimos. Pais distintos referenciados: 9510; payloads completos ausentes no índice: 1588; IDs ausentes até como metadados: **0**. Tombstone informa identidade/tempo/atores/local/pais; não contém texto/contexto completo, Fact nem razão de decisão inventada.

O arquivo histórico compactado tem 9.42 MB e **não é save completo**. JSON/save não foi substituído ou otimizado. Controle de persistência completo foi feito nos mundos de 100h. [DECISOES_6.md](</home/hugo/Área de trabalho/procedrual/DECISOES_6.md>) conserva exemplos naturais com Events, traces, tentativas e recebimentos disponíveis.

## 13. Sistemas ainda desequilibrados e decisões futuras

Sobrevivência continua sendo analisada pelos fatores acima, sem prometer mundo sustentável por decreto. O dimensionamento inicial não garante água futura: consumo extra, transferência, oferenda, acesso e obra afetam a reserva. O potencial alimentar é uma projeção de expediente de10h, não um limite físico demonstrado de ocupação de todas as cozinhas; slots são usados no planejamento/treinamento, sem um calendário de ocupação simultânea de estações. Produção alimentar nominal pode exceder demanda e ainda não se realizar por tempo, emprego, insumos, estoque, renda ou prioridades.

Compatibilidade organizacional ainda usa uma estratégia simples comunicada e custos conhecidos; não implementa ideologia completa. Delegação cobre quatro obrigações concretas, não toda ação possível de facção/prefeitura. A separação individual de status foi implementada para tarefas; livros agregados legados de coordenação organizacional não equivalem a uma auditoria de todo conhecimento institucional. Registro criminal permanece simplificado; morte/resolução administrativa e troca de atribuições ainda merecem exame. Crescimento dos registros privados continua dívida técnica. Solvabilidade UNKNOWN e causas não provadas permanecem explícitas.

Formalização, violência e religião não foram calibradas para cumprir metas. Não há neutralidade estatística total demonstrada para todos os LODs. Demografia, seca dinâmica nova, transporte comercial autônomo completo, diplomacia/guerras e otimização de save ficam para fases próprias.

Evidências: [reports/fase_6_0/testes_final.log](</home/hugo/Área de trabalho/procedrual/reports/fase_6_0/testes_final.log>), [reports/fase_6_0/controles.json](</home/hugo/Área de trabalho/procedrual/reports/fase_6_0/controles.json>), [reports/fase_6_0/campanha.json](</home/hugo/Área de trabalho/procedrual/reports/fase_6_0/campanha.json>), [reports/fase_6_0/detalhes_nativos.json](</home/hugo/Área de trabalho/procedrual/reports/fase_6_0/detalhes_nativos.json>), [reports/fase_6_0/casos_reais.json](</home/hugo/Área de trabalho/procedrual/reports/fase_6_0/casos_reais.json>). Implementação: [procedural/causal_audit.py](</home/hugo/Área de trabalho/procedrual/procedural/causal_audit.py>), [procedural/sustainability.py](</home/hugo/Área de trabalho/procedrual/procedural/sustainability.py>), [procedural/organizational_compatibility.py](</home/hugo/Área de trabalho/procedrual/procedural/organizational_compatibility.py>), [procedural/institutional_tasks.py](</home/hugo/Área de trabalho/procedrual/procedural/institutional_tasks.py>), [tests/test_phase60.py](</home/hugo/Área de trabalho/procedrual/tests/test_phase60.py>).
