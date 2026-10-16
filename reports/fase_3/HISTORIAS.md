# Histórias observadas na Fase 3

Campanhas espontâneas de 10.000 horas, após as correções de cotação desconhecida e estoque vazio. Turnos são absolutos: as campanhas começam em 24. Os cenários A–G não entram neste arquivo. As linhas citadas pertencem à pasta do modo indicado.

## Jogador — Dovha

### Mudança de profissão de um residente existente: Cael Stone (ID 1411)

Localidade: Silmir (ID 1405). No fim: vivo; profissão cozinheiro.

| Turno absoluto | Registro | Evidência |
|---:|---|---|
| 678 | TrainingStarted | Cael Stone começou a aprender cozinha. (linha 1105) |
| 705 | ProfessionChanged | Cael Stone deixou agricultor e tornou-se cozinheiro. (linha 1162) |

Prática registrada: progresso máximo 20 horas produtivas. O intervalo entre começo e conclusão inclui viagens e outras necessidades.

Contexto local comprovado: antes dessa sequência, o cozinheiro Aldren Stone morreu no turno 585. Não se presume vínculo familiar.

Fotografias locais: no turno 524, alimento 0, trigo 61, cozinheiros 1; no turno 10024, alimento 2, trigo 24, cozinheiros 1. Fotografias não demonstram abastecimento contínuo.

A sequência comprova ações e consequências individuais. Ela não comprova sozinha a recuperação do mercado nem uma relação familiar com o profissional anterior.

### Materialização com continuidade: Iria Bruma (ID 119259)

Localidade: Silvia (ID 1462). No fim: vivo; profissão sem profissão.

| Turno absoluto | Registro | Evidência |
|---:|---|---|
| 720 | WorkerMaterialized | Iria Bruma passou a trabalhar como aprendiz em Silvia. (linha 1190) |
| 720 | TrainingStarted | Iria Bruma iniciou aprendizagem de cozinha. (linha 1191) |
| 920 | TrainingAbandoned | Iria Bruma abandonou a aprendizagem sem prática recente. (linha 1592) |

Prática registrada: progresso máximo 21 horas produtivas. O intervalo entre começo e conclusão inclui viagens e outras necessidades.

Contexto local comprovado: antes dessa sequência, o cozinheiro Lyra Hammer morreu no turno 441. Não se presume vínculo familiar.

Fotografias locais: no turno 524, alimento 0, trigo 108, cozinheiros 0; no turno 10024, alimento 0, trigo 73, cozinheiros 0. Fotografias não demonstram abastecimento contínuo.

A sequência comprova ações e consequências individuais. Ela não comprova sozinha a recuperação do mercado nem uma relação familiar com o profissional anterior.

### Materialização sem sobrevivência garantida: Silas Valerius (ID 98352)

Localidade: Valria (ID 900). No fim: morto; profissão cozinheiro.

| Turno absoluto | Registro | Evidência |
|---:|---|---|
| 576 | WorkerMaterialized | Silas Valerius passou a trabalhar como aprendiz em Valria. (linha 904) |
| 576 | TrainingStarted | Silas Valerius iniciou aprendizagem de cozinha. (linha 905) |
| 629 | ProfessionChanged | Silas Valerius deixou o desemprego e tornou-se cozinheiro. (linha 1003) |

Prática registrada: progresso máximo 28 horas produtivas. O intervalo entre começo e conclusão inclui viagens e outras necessidades.

Morte no turno 1013: condições hunger, fome 100, sede 64; comida/água carregadas 0/1.

Fotografias locais: no turno 524, alimento 2, trigo 106, cozinheiros 1; no turno 10024, alimento 11, trigo 34, cozinheiros 1. Fotografias não demonstram abastecimento contínuo.

A sequência comprova ações e consequências individuais. Ela não comprova sozinha a recuperação do mercado nem uma relação familiar com o profissional anterior.

### Trabalho temporário realizado

Turno 62: Tomas Stone distribuiu 1 refeições locais. Valores físicos: `{"service": "meal_distribution", "paid_food": 1, "served_food": 1}`. Evidência: `economia_eventos.jsonl`, linha 5. Pagamento por alimento é comprovado; não se infere uma motivação pessoal que o evento não registrou.

### Continuidade familiar: Iria Luar e Arthus Luar

Relação registrada: casamento; IDs 38/41. Esta sequência contém 10 pedidos relativos ao mesmo par, não histórias independentes para cada pedido.

| Criação | Pedido | Desfecho | Conclusão |
|---:|---|---|---:|
| 6326 | Levar provisões ao familiar de Iria Luar (ID 786055, food) | failed | — |
| 7154 | Levar provisões ao familiar de Iria Luar (ID 881405, water) | failed | — |
| 7263 | Levar provisões ao familiar de Iria Luar (ID 894235, food) | declined | — |
| 7781 | Localizar familiar de Iria Luar e informar (ID 954309, family) | resolved_elsewhere | — |
| 8006 | Levar provisões ao familiar de Iria Luar (ID 980317, food) | resolved_elsewhere | — |
| 8321 | Levar provisões ao familiar de Iria Luar (ID 1016560, food) | declined | — |
| 8515 | Levar provisões ao familiar de Iria Luar (ID 1039052, food) | failed | — |
| 8657 | Levar provisões ao familiar de Iria Luar (ID 1055373, food) | completed | 8682 |
| 8840 | Levar provisões ao familiar de Iria Luar (ID 1076402, food) | declined | — |
| 9907 | Levar provisões ao familiar de Iria Luar (ID 1198673, food) | completed | 9935 |

Evidência: quests persistidas em `save_final.json` e detalhes em `relatorio.json`. A repetição mostra continuidade do vínculo e um limite de variedade narrativa: pedidos de provisão recorrentes ainda concentram o arco em sobrevivência. Conclusões são ajuda efetiva, não prova de estabilidade econômica permanente.

### Consequência pessoal: RemainsLocated

Turno 357: Tomas Montes identificou os restos de Bela Montes. (ator 550, alvo 547). Evidência: `eventos_pessoais.jsonl`, linha 811. Este é um evento pessoal efetivamente executado, não só uma necessidade selecionada.

### Consequência pessoal: ComfortGiven

Turno 209: Tomas Montes ouviu Bela Hammer durante seu luto. (ator 550, alvo 252). Evidência: `eventos_pessoais.jsonl`, linha 532. Este é um evento pessoal efetivamente executado, não só uma necessidade selecionada.

### Consequência pessoal: Remembrance

Turno 494: John Kars dedicou um momento à memória de uma pessoa próxima. (ator 1677, alvo None). Evidência: `eventos_pessoais.jsonl`, linha 1060. Este é um evento pessoal efetivamente executado, não só uma necessidade selecionada.

### Consequência pessoal: PersonLocated

Turno 36: Iria Stone localizou Tomas Stone. (ator 103, alvo 106). Evidência: `eventos_pessoais.jsonl`, linha 38. Este é um evento pessoal efetivamente executado, não só uma necessidade selecionada.

## Espectador — Dovha

### Mudança de profissão de um residente existente: Cael Stone (ID 1411)

Localidade: Silmir (ID 1405). No fim: vivo; profissão cozinheiro.

| Turno absoluto | Registro | Evidência |
|---:|---|---|
| 1019 | TrainingStarted | Cael Stone começou a aprender cozinha. (linha 1713) |
| 1043 | ProfessionChanged | Cael Stone deixou agricultor e tornou-se cozinheiro. (linha 1778) |

Prática registrada: progresso máximo 20 horas produtivas. O intervalo entre começo e conclusão inclui viagens e outras necessidades.

Contexto local comprovado: antes dessa sequência, o cozinheiro Aldren Stone morreu no turno 952. Não se presume vínculo familiar.

Fotografias locais: no turno 774, alimento 25, trigo 45, cozinheiros 1; no turno 10024, alimento 0, trigo 28, cozinheiros 1. Fotografias não demonstram abastecimento contínuo.

A sequência comprova ações e consequências individuais. Ela não comprova sozinha a recuperação do mercado nem uma relação familiar com o profissional anterior.

### Materialização com continuidade: Tomas Montes (ID 165735)

Localidade: Sillen (ID 115). No fim: vivo; profissão sem profissão.

| Turno absoluto | Registro | Evidência |
|---:|---|---|
| 1080 | WorkerMaterialized | Tomas Montes passou a trabalhar como aprendiz em Sillen. (linha 1839) |
| 1080 | TrainingStarted | Tomas Montes iniciou aprendizagem de cozinha. (linha 1840) |
| 1263 | TrainingAbandoned | Tomas Montes abandonou a aprendizagem sem prática recente. (linha 2240) |
| 1700 | TrainingStarted | Tomas Montes começou a aprender cozinha. (linha 3010) |
| 1869 | TrainingAbandoned | Tomas Montes abandonou a aprendizagem sem prática recente. (linha 3301) |

Prática registrada: progresso máximo 15 horas produtivas. O intervalo entre começo e conclusão inclui viagens e outras necessidades.

Contexto local comprovado: antes dessa sequência, o cozinheiro Darin Douran morreu no turno 987. Não se presume vínculo familiar.

Fotografias locais: no turno 1024, alimento 0, trigo 20, cozinheiros 0; no turno 10024, alimento 0, trigo 24, cozinheiros 0. Fotografias não demonstram abastecimento contínuo.

A sequência comprova ações e consequências individuais. Ela não comprova sozinha a recuperação do mercado nem uma relação familiar com o profissional anterior.

### Materialização sem sobrevivência garantida: Bela Valerius (ID 104357)

Localidade: Norlen (ID 3). No fim: morto; profissão cozinheiro.

| Turno absoluto | Registro | Evidência |
|---:|---|---|
| 624 | WorkerMaterialized | Bela Valerius passou a trabalhar como aprendiz em Norlen. (linha 1003) |
| 624 | TrainingStarted | Bela Valerius iniciou aprendizagem de cozinha. (linha 1004) |
| 676 | ProfessionChanged | Bela Valerius deixou o desemprego e tornou-se cozinheiro. (linha 1107) |

Prática registrada: progresso máximo 25 horas produtivas. O intervalo entre começo e conclusão inclui viagens e outras necessidades.

Morte no turno 1169: condições hunger, fome 100, sede 55; comida/água carregadas 0/1.

Contexto local comprovado: antes dessa sequência, o cozinheiro Nora Luar morreu no turno 538. Não se presume vínculo familiar.

Fotografias locais: no turno 524, alimento 12, trigo 36, cozinheiros 1; no turno 10024, alimento 0, trigo 55, cozinheiros 0. Fotografias não demonstram abastecimento contínuo.

A sequência comprova ações e consequências individuais. Ela não comprova sozinha a recuperação do mercado nem uma relação familiar com o profissional anterior.

### Trabalho temporário realizado

Turno 65: Bela Hammer preparou 3 rações em trabalho temporário. Valores físicos: `{"food": 3, "paid_food": 1}`. Evidência: `economia_eventos.jsonl`, linha 4. Pagamento por alimento é comprovado; não se infere uma motivação pessoal que o evento não registrou.

### Consequência pessoal: RemainsLocated

Turno 336: Tomas Montes identificou os restos de Bela Montes. (ator 550, alvo 547). Evidência: `eventos_pessoais.jsonl`, linha 768. Este é um evento pessoal efetivamente executado, não só uma necessidade selecionada.

### Consequência pessoal: ComfortGiven

Turno 209: Tomas Montes ouviu Bela Hammer durante seu luto. (ator 550, alvo 252). Evidência: `eventos_pessoais.jsonl`, linha 527. Este é um evento pessoal efetivamente executado, não só uma necessidade selecionada.

### Consequência pessoal: Remembrance

Turno 652: Ruan Valerius dedicou um momento à memória de uma pessoa próxima. (ator 563, alvo None). Evidência: `eventos_pessoais.jsonl`, linha 1282. Este é um evento pessoal efetivamente executado, não só uma necessidade selecionada.

### Consequência pessoal: PersonLocated

Turno 36: Iria Stone localizou Tomas Stone. (ator 103, alvo 106). Evidência: `eventos_pessoais.jsonl`, linha 38. Este é um evento pessoal efetivamente executado, não só uma necessidade selecionada.

## Mundo — Mira

### Mudança de profissão de um residente existente: Aldren Valerius (ID 115)

Localidade: Northon (ID 97). No fim: vivo; profissão cozinheiro.

| Turno absoluto | Registro | Evidência |
|---:|---|---|
| 1138 | TrainingStarted | Aldren Valerius começou a aprender cozinha. (linha 1817) |
| 1308 | TrainingAbandoned | Aldren Valerius abandonou a aprendizagem sem prática recente. (linha 2162) |
| 1382 | TrainingStarted | Aldren Valerius começou a aprender cozinha. (linha 2280) |
| 1471 | ProfessionChanged | Aldren Valerius deixou lenhador e tornou-se cozinheiro. (linha 2441) |

Prática registrada: progresso máximo 25 horas produtivas. O intervalo entre começo e conclusão inclui viagens e outras necessidades.

Contexto local comprovado: antes dessa sequência, o cozinheiro Bela Solaris morreu no turno 802. Não se presume vínculo familiar.

Fotografias locais: no turno 1024, alimento 0, trigo 18, cozinheiros 0; no turno 10024, alimento 4, trigo 0, cozinheiros 1. Fotografias não demonstram abastecimento contínuo.

A sequência comprova ações e consequências individuais. Ela não comprova sozinha a recuperação do mercado nem uma relação familiar com o profissional anterior.

### Materialização com continuidade: Darin Corven (ID 152129)

Localidade: Morthon (ID 612). No fim: vivo; profissão sem profissão.

| Turno absoluto | Registro | Evidência |
|---:|---|---|
| 1008 | WorkerMaterialized | Darin Corven passou a trabalhar como aprendiz em Morthon. (linha 1594) |
| 1008 | TrainingStarted | Darin Corven iniciou aprendizagem de cozinha. (linha 1595) |
| 1193 | TrainingAbandoned | Darin Corven abandonou a aprendizagem sem prática recente. (linha 1914) |

Prática registrada: progresso máximo 7 horas produtivas. O intervalo entre começo e conclusão inclui viagens e outras necessidades.

Contexto local comprovado: antes dessa sequência, o cozinheiro Silas Alvor morreu no turno 919. Não se presume vínculo familiar.

Fotografias locais: no turno 774, alimento 8, trigo 11, cozinheiros 1; no turno 10024, alimento 0, trigo 20, cozinheiros 0. Fotografias não demonstram abastecimento contínuo.

A sequência comprova ações e consequências individuais. Ela não comprova sozinha a recuperação do mercado nem uma relação familiar com o profissional anterior.

### Materialização sem sobrevivência garantida: Elena Ferros (ID 76955)

Localidade: Valmar (ID 911). No fim: morto; profissão sem profissão.

| Turno absoluto | Registro | Evidência |
|---:|---|---|
| 456 | WorkerMaterialized | Elena Ferros passou a trabalhar como aprendiz em Valmar. (linha 658) |
| 456 | TrainingStarted | Elena Ferros iniciou aprendizagem de cozinha. (linha 659) |
| 641 | TrainingAbandoned | Elena Ferros abandonou a aprendizagem sem prática recente. (linha 982) |

Prática registrada: progresso máximo 17 horas produtivas. O intervalo entre começo e conclusão inclui viagens e outras necessidades.

Morte no turno 788: condições hunger, fome 100, sede 34; comida/água carregadas 0/1.

Contexto local comprovado: antes dessa sequência, o cozinheiro Nora Valerius morreu no turno 229. Não se presume vínculo familiar.

Fotografias locais: no turno 274, alimento 0, trigo 62, cozinheiros 0; no turno 10024, alimento 0, trigo 56, cozinheiros 0. Fotografias não demonstram abastecimento contínuo.

A sequência comprova ações e consequências individuais. Ela não comprova sozinha a recuperação do mercado nem uma relação familiar com o profissional anterior.

### Trabalho temporário realizado

Turno 50: Lyra Alvor distribuiu 2 refeições locais. Valores físicos: `{"service": "meal_distribution", "paid_food": 2, "served_food": 2}`. Evidência: `economia_eventos.jsonl`, linha 6. Pagamento por alimento é comprovado; não se infere uma motivação pessoal que o evento não registrou.

### Consequência pessoal: RemainsLocated

Turno 1597: Cael Ferros identificou os restos de John Ferros. (ator 1076, alvo 1079). Evidência: `eventos_pessoais.jsonl`, linha 2468. Este é um evento pessoal efetivamente executado, não só uma necessidade selecionada.

### Consequência pessoal: Remembrance

Turno 304: Marie Ferros dedicou um momento à memória de uma pessoa próxima. (ator 59, alvo None). Evidência: `eventos_pessoais.jsonl`, linha 728. Este é um evento pessoal efetivamente executado, não só uma necessidade selecionada.

### Consequência pessoal: PersonLocated

Turno 36: Elena Bruma localizou Mira Bruma. (ator 85, alvo 88). Evidência: `eventos_pessoais.jsonl`, linha 22. Este é um evento pessoal efetivamente executado, não só uma necessidade selecionada.
