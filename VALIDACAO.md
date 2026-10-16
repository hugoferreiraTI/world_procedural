# Validação do primeiro MVP

Este documento registra a versão **mvp-1**. A validação das correções **mvp-2**
está em [RELATORIO_HARDENING.md](RELATORIO_HARDENING.md); os números abaixo são históricos.

Verificações executadas em 7 de outubro de 2026, usando Python 3.12.3.

```bash
python3 -m unittest discover -s tests -v
python3 -m procedural --seed Dovha --simular 10000
```

Os 18 testes passaram. Cobrem geração reproduzível em processos com diferentes
`PYTHONHASHSEED`, matrizes e famílias, relógio de ações, autonomia dos NPCs,
conservação de dinheiro no comércio, matéria-prima na fabricação, respostas
diferentes à fome, reavaliação de trabalho sem pagamento, conclusão de viagens
com necessidades concorrentes, percepção local, rumores, sigilo, quests ligadas
a necessidades, entrega de itens reais, corrupção de saves e limites de memória.

Uma campanha salva após 80 turnos e continuada por mais 200 produziu exatamente
o mesmo estado da execução contínua, incluindo a aleatoriedade. A interface
também foi exercitada com entrada em cidade, movimento, mercado, inventário,
save em arquivo e load pelo próprio terminal.

## Simulação longa

A seed Dovha gerou seis reinos, 76 cidades e vilas, e 440 NPCs. A simulação
avançou 10.000 horas adicionais às 24 horas de história inicial, em 47,29 segundos
nesta máquina. Terminou com 273 NPCs vivos e 833 itens. Os invariantes de IDs,
relacionamentos, matrizes, inventários, objetivos, necessidades e valores passaram.

Durante a execução ocorreram 10.000 eventos de produção, 14.970 compras,
5.222 roubos, 1.532 intervenções de guardas e 369.770 transferências de rumores.
O histórico contém 185 acontecimentos importantes; o registro cotidiano mantém
até 256 eventos. Memórias individuais e conhecimento têm limites de 32 e 64.

Houve 167 mortes por privação e 12 mudanças de sucessão. Isso confirma que a
simulação pode produzir consequências sem jogador; não demonstra equilíbrio
econômico final. Consumo, produção, salários e prioridades ainda precisam de
balanceamento para uma campanha longa agradável. Estes testes verificam
estabilidade e causalidade do núcleo, não todos os sistemas futuros do documento.

## Correções resultantes

Necessidades concorrentes podiam provocar mudanças constantes de destino.
Objetivos em andamento agora continuam até serem concluídos, exceto quando
outra necessidade se torna claramente mais urgente. Trabalho que não gera
pagamento também deixa de ser repetido como solução para obter alimento ou
dinheiro; o NPC reconsidera outras alternativas.

## Fase 4 — interação, combate e resposta

Foram adicionadas 20 regressões compostas em `tests/test_phase4.py`, cobrindo
causalidade, combate, reação social, morte/censo, captura, migração e persistência.
Passaram novamente após a correção final de denúncias acumuladas.

A suíte anterior de 179 casos foi executada uma vez. Doze casos falharam nessa
passagem; dez foram corrigidos e reavaliados, e duas expectativas da Fase 2 foram
atualizadas porque os comportamentos antes ausentes passam a ser solicitados.
Os logs e os testes originais preservados estão em `reports/fase_4`.

A auditoria curta completou 1.000h. Uma única campanha oficial Mira global
completou 10.000h, com 1.728 persistentes iniciais, 4.338 abstratos e 1.218
persistentes vivos ao final. Houve 510 mortes: 416 fome, 6 sede, 1 fome+sede e
87 combate. Os invariantes estruturais passaram a cada 100 horas.

A comparação de continuidade original depois do save final divergiu.
Um microcenário reproduziu remoção indevida de caso criminal do índice ativo.
A correção posterior agrupa casos por suspeito e gravidade conhecida, bloqueia
multa leve para caso grave e conserva os demais casos ativos no índice.
O motor corrigido passou na continuação 10.000→10.024h contra uma recarga em
10.012h: estado exato igual, índice consistente a cada hora, invariantes válidos.
Não houve segunda campanha de 10.000h. Essas etapas e hashes estão separados no
relatório; a verificação curta não é apresentada como nova auditoria longa.

O relatório final tem 34 seções em `RELATORIO_FASE_4.md`; histórias e decisões
causais estão em `reports/fase_4/HISTORIAS_EMERGENTES.md`. Fome ainda predomina
nas mortes, e histórico/save volumosos continuam sendo limites medidos.

## Fase 4.1 — recuperação fisiológica

Em 8 de outubro de 2026, os 209 testes passaram, incluindo dez regressões
compostas novas: roubo pessoal com consumo vital, compra real sem cura,
refeição antecipada, ausência de refeição precoce, dano real por privação,
recuperação e desespero gradual, dano de combate separado, dano misto sem
cura duplicada, save/load determinístico e promoção de LOD com interrupção.

As expectativas antigas de alimentação foram ajustadas ao limiar 35.
Um cenário da Fase 3.2 que verificava ausência de alternativas agora mantém
outros NPCs fora do encontro para não permitir ajuda local real.
Essas alterações e as tentativas iniciais estão registradas em
`reports/fase_4_1/testes_primeira_execucao.txt`; o resultado final está em
`reports/fase_4_1/testes_completos.txt`.

A comparação curta gera dois mundos Vespera-47 novos, sem jogador ou história
prévia, com 1.776 NPCs persistentes, 4.461 abstratos, 75 localidades e seis reinos.
Os dois completaram 500h. A versão anterior teve 50 mortes (41 por fome ou
fome+sede); a nova teve 23 (22 por fome, uma por sede). Nenhuma dessas duas
campanhas morreu de fome carregando comida. Consumo: 1,1429 → 1,1641 rações
por dia de NPC persistente vivo. Os invariantes passaram a cada 100h.

O observador curto inicializava o máximo de HP pós-refeição com o HP anterior à
refeição. O indicador derivado `crises_with_meal_and_hp_improvement` dessas duas
campanhas não deve ser usado. `correcao_observador.json` registra a limitação e
uma contagem válida de episódios com cura efetivamente medida após refeição.
O observador foi corrigido antes da campanha longa; nenhuma decisão do motor
ou métrica de mortes, refeições e janelas de HP é afetada por essa correção.

A única campanha longa Fase 4.1 terminou em 5.000h, com 1.521 vivos e 255 mortos:
243 por fome, três por sede e nove por combate. Nenhuma morte por fome carregava
ração. Consumo normalizado: 1,1846 anterior → 1,1867 atual, diferença de 0,18%.
Os invariantes passaram nas 50 verificações e o núcleo manteve o SHA congelado
`3206658685c769d82049bc62720e755b4a89c53840b26bc86c10342a459d32a6`.

O balanço global de HP fechou exatamente: 267.477 de dano menos 233.630 de cura
resultam em 33.847 HP ausentes no elenco, incluindo mortos. A privação também
fechou: 177.644 perdidos − 148.801 recuperados = 28.843 restantes no registro.
O save exportado foi recarregado somente para verificação, sem simular horas
adicionais; formato, versão, invariantes e total de dano restante passaram.

A melhora de sobrevivência é parcial: 49 trajetórias com refeição em HP <30
atingiram HP ≥80 em até 168h, mas nenhum episódio crítico apresentou HP >70 nas
janelas de 24/48/72h. Foram registradas 224 mortes por fome após refeição crítica.
Não interpretar menos mortes ou maior HP médio dos sobreviventes como resolução
completa do ciclo. A falha antiga de bloqueio entre `forage_meal` e `forage`
permanece documentada com evidência em `reports/fase_4_1/BUGS_REMANESCENTES.md`.

O relatório de 27 seções está em `RELATORIO_FASE_4_1.md`; histórias e trechos
causais estão em `reports/fase_4_1/HISTORIAS_REAIS.md` e `evidencias_historias.json`.

## Fase 4.5 — impulso, compromissos e aspirações

A suíte passou por 227 testes, incluindo 18 regressões direcionadas em
`tests/test_phase45.py`. Os dez testes de alimentação/recuperação da Fase 4.1
continuam passando. `reports/fase_4_5/preservacao.json` compara os módulos
materiais e a fórmula física de combate com a base preservada.

A entrega usa o núcleo SHA-256
`20b26d3def72979fc3c03938856c8d8301ee39336089fb6088970a9cfe656442`.
As 227 regressões passaram em `testes_completos_entrega.txt`; após aplicar
os mesmos arquivos ao projeto, as 28 regressões das Fases 4.1/4.5 passaram
novamente em `regressoes_projeto_entrega.txt`.

A curta de entrega foi realizada em mundo novo, seed Vespera-47, por 500h:
15 mortes (12 por fome, duas por fome+sede e uma em combate), zero erros de
integridade e nenhuma morte alimentar carregando comida. Está em
`reports/fase_4_5/curta_entrega_500h`. As curtas de diagnóstico foram preservadas.

Uma campanha longa foi concluída em 5.000h: 1.411 vivos e 365 mortos, sendo
308 por fome, 33 por fome+sede, 14 por sede e dez em combate. As 50 verificações
de integridade passaram; nenhuma morte alimentar carregava comida. A longa
usa o núcleo congelado
`ad79243a9a9a1aea2158a81abb000b4719335ace9c5e04581bc1d0f4132d9dbc`,
preservado em `reports/fase_4_5/campaign_code`. Cinco problemas reproduzidos
durante a revisão foram corrigidos na entrega e validados na curta posterior;
os resultados da longa incluem o comportamento anterior a essas correções.
Não interpretar a curta como prova de que a piora de sobrevivência desapareceu
no horizonte longo. `ajustes_finais.json` registra essa distinção.

A campanha, seu save e a seleção narrativa ficam em
`reports/fase_4_5/global_5000h`, `reports/fase_4_5/HISTORIAS_REAIS.md` e no
`RELATORIO_FASE_4_5.md`; métricas de progresso não equivalem a ações realizadas
nem a histórias profundas. A versão nova do save é `mvp-6-fase4.5`.


## Fase 4.6 — investigação e escalada fatal

A entrega usa `mvp-7-fase4.6`, núcleo SHA-256 `e3866d29db349cbfc963bc0a7cd0036e65b9577a0f7cb16707a2f4a787b43c96`.
Foram acrescentadas 18 regressões compostas, totalizando 245 testes únicos.
A suíte completa inicial foi executada uma vez: 240 de 243 passaram e três
detectaram contadores alterados por consultas de depuração. O reparo passou nos
três testes; a validação final passou em 59 testes dirigidos (18 novos, 18 da
Fase 4.5, 20 de combate e três de determinismo). A suíte completa não foi repetida.
Logs iniciais e retestes estão preservados em `reports/fase_4_6`.

O mesmo código congelado foi observado em mundo novo, sem jogador nem histórico
prévio, seed Corven-46: curta de 500h e uma longa concluída de 5.000h. Um início
longo anterior foi interrompido no diagnóstico, com último ponto confirmado em
800h, e não entra nas estatísticas finais. `EXECUCOES.json` distingue cada execução.

Na longa, as 50 verificações de integridade passaram: 1274 vivos e
294 mortos; causas `{'thirst': 6, 'hunger': 260, 'combat': 17, 'both': 11}`. Nenhuma morte alimentar carregava comida.
Houve 23 mudanças para intenção matar e 57 ataques com essa intenção; nenhum
homicídio deliberado nem julgamento letal após incapacidade nesta campanha.
Esses desfechos foram demonstrados em regressões controladas, sem preencher
a seleção de histórias naturais com fatos artificiais.

As buscas realizaram 13.792 verificações de áreas e 3.744 consultas: 3.149
entradas em espera, 1.545 reativações e 845 respostas úteis. O save final está
em `reports/fase_4_6/global_5000h/save_final.json` e ocupa 1.101,6 MiB. Dados novos
agregados de conflito e compromissos investigativos ocupam cerca de 2,74 MiB.
A fórmula de potência e o bloco físico de dano continuam idênticos à base.

Leitura: `RELATORIO_FASE_4_6.md` e `reports/fase_4_6/HISTORIAS_REAIS.md`.

## Fase 5 — poder local, organizações, fé e lendas

Entrega `mvp-8-fase5`, núcleo SHA-256 `cb972af78af4063d25173d1165355617317f6f702ffccc4b888ad087f15977de`.
A suíte completa passou em **275 testes**, preservando os 245 anteriores e
acrescentando 30 regressões compostas. Log: `reports/fase_5/testes_275_entrega_social_final.txt`.
A conferência dirigida passou nos 30 casos, incluindo limites de adesão,
sucessão após migração e preservação de demandas recebidas, hipótese sobre
sucessor divino e encaminhamento de oração ao mortal ascendido. Save/load e
continuidade do RNG foram verificados em cenários pequenos; o save longo não
foi inteiramente recarregado para declarar esse resultado.

A curta posterior aos ajustes terminou em mundo novo, sem jogador nem história
prévia, seed **Serevan-5**, por **500h**: 1590 vivos, 26 mortos
(23 fome, duas combate, uma sede), zero erros de integridade em cinco verificações
periódicas, além da inicial e final; nenhuma morte alimentar carregava comida.
O save ocupa 150.37 MiB; pico de memória do processo incluindo exportação
1311.34 MiB; simulação 5.15 minutos.
Dados: `reports/fase_5/curta_entrega_500h`. A curta anterior da mesma seed teve
19 mortes; a entrega não demonstra melhora de sobrevivência.

A **única longa desta fase** terminou em **5.000h**, seed **Nhalven-5**:
1.339 vivos, 293 mortos (287 fome, uma fome+sede, cinco combate).
Passaram 50 verificações periódicas, além da inicial e final. Nenhuma morte
alimentar carregava comida. Ela usa o núcleo preservado
`2a2ede5c51058e8e5ee849dc04a08f7002dd8d7da8db8278312f2460e6e4d8e1`, em `reports/fase_5/final_code`,
anterior aos cinco ajustes finais. O núcleo atual está em
`reports/fase_5/entrega_code`; não houve segunda longa para substituir o resultado.
`ENTREGA_FINAL.json` e `EXECUCOES.json` explicitam versões, execuções e falhas.

A longa registrou 4.332 formações de grupo, seis entregas de proposta, quatro
decisões, 227 orações e 29 treinos. Sete mortais ainda eram venerados no fim;
nenhum deles era divindade objetiva. Não houve apoteose, morte divina,
intervenção, fundação/adesão/promoção de facção, execução deliberada ou
misericórdia terminal. Os microcenários comprovam capacidade dessas regras,
sem serem contados como histórias naturais. A seleção conserva 10 de 22
categorias com alguma evidência; muitas são pequenas ou incompletas.

O save longo ocupa 1039.82 MiB, com pico do processo incluindo exportação
8437.92 MiB. Valores compactos dos campos novos de modelo somam
cerca de 8,50 MiB; isso não isola o histórico/conhecimento derivados nem mede RAM.
A geração física da seed de preservação permaneceu idêntica nos quatro conjuntos
comparados. O documento recebido permanece byte a byte em `fase_5.md`.

Leitura: `RELATORIO_FASE_5.md`, `reports/fase_5/HISTORIAS_REAIS.md`,
`reports/fase_5/METRICAS_FASE_5.json` e `reports/fase_5/MICROCENARIOS_CONTROLADOS.md`.
