# Histórias reais — Fase 4.6

Seed `Corven-46`, mundo novo, h 0–5000, sem jogador e sem save carregado. Relatos derivados de eventos e compromissos, sem falas ou acontecimentos inventados.

As seleções abaixo mostram trajetórias distintas. O catálogo completo de compromissos está em `global_5000h/arcos.json`; os eventos observados estão em `global_5000h/eventos.jsonl.gz`. Uma sequência longa de tentativas não equivale automaticamente a uma história profunda.

## Cobertura das situações solicitadas

| Situação | Evidência natural |
|---|---:|
| Mudança de intenção para matar | 23 |
| Alternativa letal considerada | 56 |
| Misericórdia após incapacidade letal | 0 |
| Intenção letal abandonada explicitamente | 6 |
| Morte com intenção matar | 0 |
| Intenção letal escolhida — compromissos elegíveis | 14 |
| Opção letal disponível em situação natural — compromissos elegíveis | 34 |
| Pista antiga renovada por consulta real — compromissos elegíveis | 699 |
| Resposta à morte causada por outro — compromissos elegíveis | 12 |
| Reação grave amadurecida — compromissos elegíveis | 8 |
| Busca com várias pistas — compromissos elegíveis | 8394 |
| Busca suspensa e reativada — compromissos elegíveis | 1095 |
| Guarda investigando — compromissos elegíveis | 1190 |
| Vingança com deslocamento entre localidades — compromissos elegíveis | 14 |
| Viagem motivada por saber-se procurado — compromissos elegíveis | 383 |
| Perseguição institucional com viagem — compromissos elegíveis | 5 |
| Busca sem saída — compromissos elegíveis | 1546 |
| Vingança encerrada sem ataque registrado — compromissos elegíveis | 1459 |
| Vingança abandonada — compromissos elegíveis | 14776 |
| Espera com retorno à rotina — compromissos elegíveis | 2597 |
| Autoria inicialmente desconhecida — compromissos elegíveis | 0 |
| Pedido recusado ou sem informação — compromissos elegíveis | 467 |
| Cadeias causais com violência, resposta de terceiro, nova violência e nova resposta | 887 |
| Pista deliberadamente falsa comprovada | Não gerada pelo sistema atual; não confundir com informação atrasada |

## 1. Intenção letal escolhida: Tomas Bruma (NPC 1935)

Compromisso `4347853`, motivação `response`, alvo inicial Iria Bruma (NPC 1927). Nasceu na hora 3982. Fato causal `4340730`.

Personalidade inicial registrada: coragem 88, compaixão 69, vingatividade 66, persistência 66 e lealdade familiar 82 (escala 0–100). Situação no fim da campanha: vivo. Esses valores influenciam escolhas; não comprovam por si sós a razão de um evento.

Causa registrada: Iria Bruma feriu Tomas Bruma em 2 HP. (h 3975, evento 4340730).

| Hora | Transformação real | Evento |
|---:|---|---:|
| 3982 | CommitmentCreated | 4347854 |
| 3982 | Pista de Iria Bruma (NPC 1927) em Karven, (3, 5), observação h 3982, confiança 100%, fonte direct | 4347855 |
| 3984 | Pista de Iria Bruma (NPC 1927) em Karven, (3, 5), observação h 3983, confiança 100%, fonte direct | 4350231 |
| 4000 | Pista de Iria Bruma (NPC 1927) em Karven, (3, 5), observação h 4000, confiança 100%, fonte direct | 4367573 |
| 4001 | Pista de Iria Bruma (NPC 1927) em Karven, (3, 5), observação h 4001, confiança 100%, fonte direct | 4368533 |
| 4003 | Pista de Iria Bruma (NPC 1927) em Karven, (3, 5), observação h 4002, confiança 100%, fonte direct | 4370608 |
| 4007 | Pista de Iria Bruma (NPC 1927) em Karven, (2, 2), observação h 4007, confiança 100%, fonte direct | 4374860 |
| 4013 | Pista de Iria Bruma (NPC 1927) em Karven, (3, 5), observação h 4013, confiança 100%, fonte direct | 4381759 |
| 4355 | Mudança de abordagem: drink → search_area | 4744630 |
| 4373 | Mudança de abordagem: search_area → fill_water | 4763542 |
| 4376 | Pista de Iria Bruma (NPC 1927) em Karven, (2, 2), observação h 4366, confiança 60%, fonte known | 4766934 |
| 4376 | Mudança de abordagem: fill_water → ask_about_person | 4766935 |
| 4394 | Mudança de abordagem: ask_about_person → search_area | 4785878 |
| 4398 | Pista de Iria Bruma (NPC 1927) em Karven, (1, 5), observação h 4394, confiança 60%, fonte known | 4790532 |
| 4398 | Mudança de abordagem: search_area → ask_about_person | 4790533 |
| 4399 | CommitmentAbandoned: no_progress_or_lost_agency | 4791647 |

Primeira execução social registrada: h 4177, `attack`, sucesso `True` — Ataque causou 8 de dano real.. Abordagens registradas: `{'attack': 6, 'defend': 5, 'confront': 1, 'search_area': 6, 'ask_about_person': 3, 'drink': 2, 'fill_water': 2}`; execuções sem sucesso: 0. O log social amostra repetições, então esses números não são o total exato de ações.

Ataques executados com este compromisso: amostra nas horas `[4177, 4182, 4271, 4274, 4276, 4278]`. Isso não demonstra intenção de matar.

Leitura: 5 locais de pista distintos, 24 mudanças de abordagem; encerramento `CommitmentAbandoned`. Pistas descrevem conhecimento recebido, não a posição objetiva atual. Encerrar uma denúncia não comprova captura nem eliminação do adversário.

## 2. Opção letal disponível em situação natural: Nora Bruma (NPC 3367)

Compromisso `1252548`, motivação `response`, alvo inicial Silas Stone (NPC 811). Nasceu na hora 1206. Fato causal `738384`.

Personalidade inicial registrada: coragem 76, compaixão 24, vingatividade 94, persistência 89 e lealdade familiar 38 (escala 0–100). Situação no fim da campanha: vivo. Esses valores influenciam escolhas; não comprovam por si sós a razão de um evento.

Causa registrada: Silas Stone feriu Nora Bruma em 11 HP. (h 754, evento 738384).

| Hora | Transformação real | Evento |
|---:|---|---:|
| 1206 | CommitmentCreated | 1252549 |
| 1206 | Pista de Silas Stone (NPC 811) em Kardor, (2, 2), observação h 1197, confiança 100%, fonte direct | 1252551 |
| 1210 | Mudança de abordagem: search_area → ask_about_person | 1256891 |
| 1212 | Mudança de abordagem: ask_about_person → search_area | 1259076 |
| 1222 | Busca entra em espera: no_remaining_known_source; 4 tentativas nesta pista | 1270220 |
| 1223 | Pista de Silas Stone (NPC 811) em Kardor, (3, 5), observação h 1223, confiança 100%, fonte direct | 1271397 |
| 1223 | Informação útil reativa o objetivo; a ação ainda depende da próxima decisão | 1271398 |
| 1229 | Pista de Silas Stone (NPC 811) em Kardor, (3, 5), observação h 1228, confiança 100%, fonte direct | 1278274 |
| 1473 | Mudança de abordagem: drink → search_area | 1557332 |
| 1494 | Busca entra em espera: no_remaining_known_source; 2 tentativas nesta pista | 1580921 |
| 1517 | Pista de Silas Stone (NPC 811) em Kardor, (2, 2), observação h 1517, confiança 100%, fonte direct | 1606348 |
| 1517 | Informação útil reativa o objetivo; a ação ainda depende da próxima decisão | 1606349 |
| 1517 | Opção letal torna-se plausível: pressão 69.09, causa recurrent_physical_danger, confiança 100%; não comprova escolha de matar | 1606350 |
| 1526 | Mudança de abordagem: search_area → ask_about_person | 1616300 |
| 1527 | Mudança de abordagem: ask_about_person → search_area | 1617422 |
| 1539 | CommitmentAbandoned: no_progress_or_lost_agency | 1630978 |

Primeira execução social registrada: h 1206, `search_area`, sucesso `True` — Área conhecida observada; ausência não revela destino remoto.. Abordagens registradas: `{'search_area': 12, 'ask_about_person': 4, 'attack': 1, 'fill_water': 2, 'drink': 3}`; execuções sem sucesso: 0. O log social amostra repetições, então esses números não são o total exato de ações.

Ataques executados com este compromisso: amostra nas horas `[1251]`. Isso não demonstra intenção de matar.

Enquanto este compromisso estava em espera, entre h 1297 e 1516, ações reais bem-sucedidas: `{'work': 7, 'buy_food': 4, 'eat': 3, 'drink': 5, 'sleep': 2, 'pursue': 5, 'fill_water': 3, 'stay_near': 1}`. Não são etapas de um plano da busca.

Leitura: 3 locais de pista distintos, 17 mudanças de abordagem; encerramento `CommitmentAbandoned`. Pistas descrevem conhecimento recebido, não a posição objetiva atual. Encerrar uma denúncia não comprova captura nem eliminação do adversário.

## 3. Pista antiga renovada por consulta real: Elena Luar (NPC 2259)

Compromisso `3339038`, motivação `family`, alvo inicial Aldren Luar (NPC 2256). Nasceu na hora 3054. Fato causal `3334508`.

Personalidade inicial registrada: coragem 48, compaixão 48, vingatividade 43, persistência 25 e lealdade familiar 27 (escala 0–100). Situação no fim da campanha: vivo. Esses valores influenciam escolhas; não comprovam por si sós a razão de um evento.

Causa registrada: Elena Luar não localiza um familiar há 2748 horas. (h 3050, evento 3334508).

| Hora | Transformação real | Evento |
|---:|---|---:|
| 3054 | CommitmentCreated | 3339039 |
| 3054 | Pista de Aldren Luar (NPC 2256) em Karmar, (3, 5), observação h 302, confiança 100%, fonte direct | 3339040 |
| 3059 | Pista de Aldren Luar (NPC 2256) em Karmir, (1, 5), observação h 3011, confiança 30%, fonte rumor | 3344518 |
| 3059 | Mudança de abordagem: search_area → ask_about_person | 3344519 |
| 3060 | Passo de viagem física para Karmir | 3345636 |
| 3060 | Mudança de abordagem: ask_about_person → follow_lead | 3345637 |
| 3849 | CommitmentExpired: finite_intention_horizon | 4204481 |

Primeira execução social registrada: h 3058, `search_area`, sucesso `True` — Área conhecida observada; ausência não revela destino remoto.. Abordagens registradas: `{'search_area': 1, 'ask_about_person': 1, 'follow_lead': 172}`; execuções sem sucesso: 0. O log social amostra repetições, então esses números não são o total exato de ações.

Leitura: 2 locais de pista distintos, 2 mudanças de abordagem; encerramento `CommitmentExpired`. Pistas descrevem conhecimento recebido, não a posição objetiva atual. Encerrar uma denúncia não comprova captura nem eliminação do adversário.

## 4. Resposta à morte causada por outro: Ruan Bruma (NPC 4264)

Compromisso `664519`, motivação `grief`, alvo inicial Tomas Bruma (NPC 4267). Nasceu na hora 685. Fato causal `558398`.

Personalidade inicial registrada: coragem 68, compaixão 24, vingatividade 67, persistência 83 e lealdade familiar 79 (escala 0–100). Situação no fim da campanha: vivo. Esses valores influenciam escolhas; não comprovam por si sós a razão de um evento.

Causa registrada: Elena Hammer causou a morte de Tomas Bruma em confronto. (h 588, evento 558398).

| Hora | Transformação real | Evento |
|---:|---|---:|
| 685 | CommitmentCreated | 664520 |
| 687 | Mudança de abordagem: fill_water → drink | 666596 |
| 688 | Mudança de abordagem: drink → remember_relative | 667607 |
| 693 | CommitmentCompleted: verified_need_resolution | 672852 |

Primeira execução social registrada: h 686, `fill_water`, sucesso `True` — Reserva de água obtida na fonte local.. Abordagens registradas: `{'fill_water': 1, 'drink': 1, 'remember_relative': 1}`; execuções sem sucesso: 0. O log social amostra repetições, então esses números não são o total exato de ações.

Leitura: 0 locais de pista distintos, 2 mudanças de abordagem; encerramento `CommitmentCompleted`. Pistas descrevem conhecimento recebido, não a posição objetiva atual. Encerrar uma denúncia não comprova captura nem eliminação do adversário.

## 5. Reação grave amadurecida: Aldren Stone (NPC 3726)

Compromisso `4504093`, motivação `response`, alvo inicial Darin Solaris (NPC 790). Nasceu na hora 4128. Fato causal `4257945`.

Personalidade inicial registrada: coragem 78, compaixão 64, vingatividade 87, persistência 83 e lealdade familiar 66 (escala 0–100). Situação no fim da campanha: vivo. Esses valores influenciam escolhas; não comprovam por si sós a razão de um evento.

Causa registrada: Darin Solaris feriu Aldren Stone em 2 HP. (h 3899, evento 4257945).

| Hora | Transformação real | Evento |
|---:|---|---:|
| 4128 | CommitmentCreated | 4504094 |
| 4128 | Pista de Darin Solaris (NPC 790) em Vallen, (3, 5), observação h 4108, confiança 100%, fonte direct | 4504095 |
| 4135 | Pista de Darin Solaris (NPC 790) em Vallen, (2, 2), observação h 4135, confiança 100%, fonte direct | 4511397 |
| 4139 | Pista de Darin Solaris (NPC 790) em Vallen, (2, 2), observação h 4136, confiança 100%, fonte direct | 4515520 |
| 4154 | Pista de Darin Solaris (NPC 790) em Vallen, (1, 5), observação h 4148, confiança 60%, fonte known | 4531130 |
| 4154 | Mudança de abordagem: search_area → ask_about_person | 4531132 |
| 4167 | Mudança de abordagem: ask_about_person → search_area | 4544253 |
| 4177 | Busca entra em espera: no_remaining_known_source; 2 tentativas nesta pista | 4554971 |
| 4925 | Pista de Darin Solaris (NPC 790) em Vallen, (3, 5), observação h 4925, confiança 100%, fonte direct | 5363215 |
| 4927 | Pista de Darin Solaris (NPC 790) em Vallen, (3, 4), observação h 4927, confiança 100%, fonte direct | 5365424 |
| 4943 | Pista de Darin Solaris (NPC 790) em Vallen, (2, 2), observação h 4943, confiança 100%, fonte direct | 5382659 |
| 4946 | Pista de Darin Solaris (NPC 790) em Vallen, (2, 2), observação h 4944, confiança 100%, fonte direct | 5385983 |
| 4975 | Pista de Darin Solaris (NPC 790) em Vallen, (2, 2), observação h 4973, confiança 100%, fonte direct | 5416932 |
| 4983 | Pista de Darin Solaris (NPC 790) em Vallen, (3, 5), observação h 4983, confiança 100%, fonte direct | 5425345 |
| 4993 | Pista de Darin Solaris (NPC 790) em Vallen, (3, 5), observação h 4992, confiança 100%, fonte direct | 5436217 |
| 4997 | Pista de Darin Solaris (NPC 790) em Vallen, (2, 2), observação h 4997, confiança 100%, fonte direct | 5440505 |

Primeira execução social registrada: h 4142, `search_area`, sucesso `True` — Área conhecida observada; ausência não revela destino remoto.. Abordagens registradas: `{'search_area': 5, 'ask_about_person': 1}`; execuções sem sucesso: 0. O log social amostra repetições, então esses números não são o total exato de ações.

Enquanto este compromisso estava em espera, entre h 4177 e 4193, ações reais bem-sucedidas: `{'steal': 1, 'eat': 1, 'fill_water': 1, 'drink': 2, 'sleep': 1}`. Não são etapas de um plano da busca.

Leitura: 8 locais de pista distintos, 2 mudanças de abordagem; encerramento `paused`. Pistas descrevem conhecimento recebido, não a posição objetiva atual. Encerrar uma denúncia não comprova captura nem eliminação do adversário.

## 6. Busca com várias pistas: Tomas Douran (NPC 4122)

Compromisso `1173138`, motivação `family`, alvo inicial Arthus Douran (NPC 4125). Nasceu na hora 1136. Fato causal `1173137`.

Personalidade inicial registrada: coragem 64, compaixão 73, vingatividade 32, persistência 27 e lealdade familiar 56 (escala 0–100). Situação no fim da campanha: vivo. Esses valores influenciam escolhas; não comprovam por si sós a razão de um evento.

Causa registrada: Tomas Douran não localiza um familiar há 890 horas. (h 1136, evento 1173137).

| Hora | Transformação real | Evento |
|---:|---|---:|
| 1136 | CommitmentCreated | 1173139 |
| 1136 | Pista de Arthus Douran (NPC 4125) em Vallen, (3, 5), observação h 246, confiança 100%, fonte direct | 1173140 |
| 1142 | Pista de Arthus Douran (NPC 4125) em Normar, (1, 5), observação h 752, confiança 30%, fonte rumor | 1180090 |
| 1142 | Mudança de abordagem: search_area → ask_about_person | 1180091 |
| 1160 | Mudança de abordagem: ask_about_person → forage | 1200468 |
| 1382 | Mudança de abordagem: forage → fill_water | 1454489 |
| 1397 | Mudança de abordagem: fill_water → forage | 1471264 |
| 1422 | Mudança de abordagem: forage → fill_water | 1500172 |
| 1448 | Mudança de abordagem: forage → follow_lead | 1529328 |
| 1456 | Mudança de abordagem: follow_lead → forage | 1538652 |
| 1508 | Mudança de abordagem: forage → fill_water | 1596443 |
| 1509 | Mudança de abordagem: fill_water → follow_lead | 1597431 |
| 1534 | Mudança de abordagem: follow_lead → search_area | 1625122 |
| 1535 | Pista de Arthus Douran (NPC 4125) em Normar, (3, 5), observação h 1535, confiança 100%, fonte direct | 1626243 |
| 1535 | Mudança de abordagem: search_area → check_relative | 1626246 |
| 1535 | CommitmentCompleted: verified_need_resolution | 1626248 |

Primeira execução social registrada: h 1136, `search_area`, sucesso `True` — Área conhecida observada; ausência não revela destino remoto.. Abordagens registradas: `{'search_area': 1, 'ask_about_person': 1, 'forage': 33, 'fill_water': 4, 'follow_lead': 24, 'check_relative': 1}`; execuções sem sucesso: 0. O log social amostra repetições, então esses números não são o total exato de ações.

Leitura: 3 locais de pista distintos, 18 mudanças de abordagem; encerramento `CommitmentCompleted`. Pistas descrevem conhecimento recebido, não a posição objetiva atual. Encerrar uma denúncia não comprova captura nem eliminação do adversário.

## 7. Busca suspensa e reativada: Marie Ferros (NPC 541)

Compromisso `424087`, motivação `pursuit`, alvo inicial John Luar (NPC 3015). Nasceu na hora 461. Fato causal `420265`.

Personalidade inicial registrada: coragem 7, compaixão 87, vingatividade 23, persistência 92 e lealdade familiar 42 (escala 0–100). Situação no fim da campanha: vivo. Esses valores influenciam escolhas; não comprovam por si sós a razão de um evento.

Causa registrada: John Luar feriu Mira Arven em 2 HP. (h 457, evento 420265).

| Hora | Transformação real | Evento |
|---:|---|---:|
| 461 | CommitmentCreated | 424088 |
| 461 | Pista de John Luar (NPC 3015) em Valvia, (2, 2), observação h 461, confiança 100%, fonte direct | 424089 |
| 465 | Pista de John Luar (NPC 3015) em Valvia, (2, 2), observação h 462, confiança 100%, fonte direct | 428199 |
| 482 | Pista de John Luar (NPC 3015) em Valvia, (3, 5), observação h 482, confiança 100%, fonte direct | 445370 |
| 487 | Pista de John Luar (NPC 3015) em Valvia, (3, 5), observação h 486, confiança 100%, fonte direct | 450764 |
| 488 | Mudança de abordagem: search_area → ask_about_person | 451738 |
| 489 | Mudança de abordagem: ask_about_person → search_area | 452742 |
| 492 | Busca entra em espera: no_remaining_known_source; 3 tentativas nesta pista | 455655 |
| 892 | Pista de John Luar (NPC 3015) em Valvia, (3, 5), observação h 891, confiança 100%, fonte direct | 893098 |
| 892 | Mudança de abordagem: surrender → search_area | 893105 |
| 894 | Mudança de abordagem: search_area → ask_about_person | 895525 |
| 903 | Mudança de abordagem: ask_about_person → search_area | 905912 |
| 906 | Busca entra em espera: no_remaining_known_source; 3 tentativas nesta pista | 909345 |
| 941 | Pista de John Luar (NPC 3015) em Valvia, (3, 5), observação h 940, confiança 100%, fonte direct | 949254 |
| 941 | Informação útil reativa o objetivo; a ação ainda depende da próxima decisão | 949255 |
| 947 | CommitmentAbandoned: no_progress_or_lost_agency | 956072 |

Primeira execução social registrada: h 487, `search_area`, sucesso `True` — Área conhecida observada; ausência não revela destino remoto.. Abordagens registradas: `{'search_area': 14, 'ask_about_person': 7, 'surrender': 3, 'fill_water': 1}`; execuções sem sucesso: 0. O log social amostra repetições, então esses números não são o total exato de ações.

Enquanto este compromisso estava em espera, entre h 495 e 939, ações reais bem-sucedidas: `{'eat': 7, 'secure': 5, 'pursue': 4, 'drink_well': 9, 'protect': 1, 'surrender': 3, 'sleep': 15, 'forage': 2, 'avoid_threat': 1, 'work': 7, 'steal': 5, 'fill_water': 1, 'drink': 2, 'search_area': 5, 'ask_about_person': 1, 'denounce': 1}`. Não são etapas de um plano da busca.

Leitura: 4 locais de pista distintos, 19 mudanças de abordagem; encerramento `CommitmentAbandoned`. Pistas descrevem conhecimento recebido, não a posição objetiva atual. Encerrar uma denúncia não comprova captura nem eliminação do adversário.

## 8. Guarda investigando: Bela Luar (NPC 4669)

Compromisso `801157`, motivação `pursuit`, alvo inicial Darin Solaris (NPC 4681). Nasceu na hora 810. Fato causal `796679`.

Personalidade inicial registrada: coragem 19, compaixão 10, vingatividade 33, persistência 90 e lealdade familiar 15 (escala 0–100). Situação no fim da campanha: vivo. Esses valores influenciam escolhas; não comprovam por si sós a razão de um evento.

Causa registrada: Darin Solaris feriu Ruan Bruma em 2 HP. (h 806, evento 796679).

| Hora | Transformação real | Evento |
|---:|---|---:|
| 810 | CommitmentCreated | 801158 |
| 810 | Pista de Darin Solaris (NPC 4681) em Elidor, (2, 2), observação h 810, confiança 100%, fonte direct | 801159 |
| 816 | Pista de Darin Solaris (NPC 4681) em Elidor, (2, 2), observação h 813, confiança 100%, fonte direct | 807804 |
| 828 | Pista de Darin Solaris (NPC 4681) em Elidor, (2, 2), observação h 827, confiança 100%, fonte direct | 821529 |
| 829 | Mudança de abordagem: search_area → attack | 822568 |
| 832 | Pista de Darin Solaris (NPC 4681) em Elidor, (2, 2), observação h 831, confiança 100%, fonte direct | 825893 |
| 837 | Mudança de abordagem: attack → search_area | 831321 |
| 841 | Mudança de abordagem: search_area → ask_about_person | 836064 |
| 1254 | Pista de Darin Solaris (NPC 4681) em Elidor, (2, 2), observação h 1253, confiança 100%, fonte direct | 1307094 |
| 1258 | Pista de Darin Solaris (NPC 4681) em Elidor, (3, 5), observação h 1258, confiança 100%, fonte direct | 1311779 |
| 1261 | Pista de Darin Solaris (NPC 4681) em Elidor, (3, 5), observação h 1260, confiança 100%, fonte direct | 1315180 |
| 1267 | Pista de Darin Solaris (NPC 4681) em Elidor, (2, 2), observação h 1267, confiança 100%, fonte direct | 1322023 |
| 1273 | Pista de Darin Solaris (NPC 4681) em Elidor, (2, 2), observação h 1272, confiança 100%, fonte direct | 1329189 |
| 1278 | Pista de Darin Solaris (NPC 4681) em Elidor, (3, 5), observação h 1278, confiança 100%, fonte direct | 1334735 |
| 1280 | Pista de Darin Solaris (NPC 4681) em Elidor, (3, 5), observação h 1279, confiança 100%, fonte direct | 1336962 |
| 1290 | CommitmentExpired: known_evidence_expired | 1348173 |

Primeira execução social registrada: h 829, `attack`, sucesso `True` — Ataque causou 11 de dano real.. Abordagens registradas: `{'attack': 2, 'search_area': 6, 'ask_about_person': 4, 'fill_water': 1, 'drink': 2}`; execuções sem sucesso: 0. O log social amostra repetições, então esses números não são o total exato de ações.

Ataques executados com este compromisso: amostra nas horas `[829, 1107]`. Isso não demonstra intenção de matar.

Enquanto este compromisso estava em espera, entre h 1096 e 1101, ações reais bem-sucedidas: `{'work': 1, 'attack': 1, 'drink': 1, 'denounce': 2, 'ask_personal_help': 1}`. Não são etapas de um plano da busca.

Leitura: 8 locais de pista distintos, 14 mudanças de abordagem; encerramento `CommitmentExpired`. Pistas descrevem conhecimento recebido, não a posição objetiva atual. Encerrar uma denúncia não comprova captura nem eliminação do adversário.

## 9. Vingança com deslocamento entre localidades: John Hammer (NPC 2873)

Compromisso `1352355`, motivação `revenge`, alvo inicial Darin Corven (NPC 618). Nasceu na hora 1294. Fato causal `1345989`.

Personalidade inicial registrada: coragem 62, compaixão 37, vingatividade 66, persistência 35 e lealdade familiar 10 (escala 0–100). Situação no fim da campanha: vivo. Esses valores influenciam escolhas; não comprovam por si sós a razão de um evento.

Causa registrada: Darin Corven roubou comida no mercado de Arlen. (h 1289, evento 1345989).

| Hora | Transformação real | Evento |
|---:|---|---:|
| 1294 | CommitmentCreated | 1352356 |
| 1294 | Pista de Darin Corven (NPC 618) em Arlen, (3, 5), observação h 1289, confiança 100%, fonte direct | 1352357 |
| 1321 | Pista de Darin Corven (NPC 618) em Arlen, (1, 5), observação h 1321, confiança 100%, fonte direct | 1383606 |
| 1342 | Pista de Darin Corven (NPC 618) em Arlen, (2, 2), observação h 1342, confiança 100%, fonte direct | 1407867 |
| 1345 | Mudança de abordagem: investigate → denounce | 1411263 |
| 1360 | Pista de Darin Corven (NPC 618) em Arlen, (2, 2), observação h 1348, confiança 100%, fonte direct | 1428411 |
| 1387 | Pista de Darin Corven (NPC 618) em Arlen, (2, 2), observação h 1384, confiança 100%, fonte direct | 1460046 |
| 1402 | Pista de Darin Corven (NPC 618) em Arlen, (2, 5), observação h 1402, confiança 100%, fonte direct | 1476533 |
| 1819 | Mudança de abordagem: investigate → denounce | 1942518 |
| 1822 | Passo de viagem física para Arlen | 1945653 |
| 1822 | Mudança de abordagem: denounce → follow_lead | 1945654 |
| 1906 | Mudança de abordagem: follow_lead → denounce | 2038940 |
| 1912 | Mudança de abordagem: denounce → forage | 2045460 |
| 1936 | Mudança de abordagem: forage → buy_food | 2072207 |
| 1942 | Mudança de abordagem: buy_food → denounce | 2078714 |
| 1942 | CommitmentCompleted: verified_need_resolution | 2078716 |

Primeira execução social registrada: h 1342, `investigate`, sucesso `True` — Investigou o local conhecido; não houve confronto.. Abordagens registradas: `{'investigate': 2, 'denounce': 5, 'follow_lead': 5, 'forage': 1, 'buy_food': 1}`; execuções sem sucesso: 4. O log social amostra repetições, então esses números não são o total exato de ações.

Leitura: 4 locais de pista distintos, 8 mudanças de abordagem; encerramento `CommitmentCompleted`. Pistas descrevem conhecimento recebido, não a posição objetiva atual. Encerrar uma denúncia não comprova captura nem eliminação do adversário.

## 10. Viagem motivada por saber-se procurado: Aldren Stone (NPC 2919)

Compromisso `837980`, motivação `migration`, alvo inicial Arria (localidade 565). Nasceu na hora 843. Fato causal `None`.

Personalidade inicial registrada: coragem 76, compaixão 34, vingatividade 71, persistência 71 e lealdade familiar 44 (escala 0–100). Situação no fim da campanha: vivo. Esses valores influenciam escolhas; não comprovam por si sós a razão de um evento.

| Hora | Transformação real | Evento |
|---:|---|---:|
| 843 | CommitmentCreated | 837981 |
| 1776 | CommitmentExpired: finite_intention_horizon | 1895255 |

Primeira execução social registrada: h 843, `migrate`, sucesso `True` — Uma etapa física da viagem foi realizada.. Abordagens registradas: `{'migrate': 263}`; execuções sem sucesso: 0. O log social amostra repetições, então esses números não são o total exato de ações.

Leitura: 0 locais de pista distintos, 0 mudanças de abordagem; encerramento `CommitmentExpired`. Pistas descrevem conhecimento recebido, não a posição objetiva atual. Encerrar uma denúncia não comprova captura nem eliminação do adversário.

## 11. Perseguição institucional com viagem: Cael Arven (NPC 3749)

Compromisso `2070190`, motivação `pursuit`, alvo inicial Aldren Stone (NPC 3726). Nasceu na hora 1934. Fato causal `2032361`.

Personalidade inicial registrada: coragem 21, compaixão 7, vingatividade 52, persistência 36 e lealdade familiar 48 (escala 0–100). Situação no fim da campanha: vivo. Esses valores influenciam escolhas; não comprovam por si sós a razão de um evento.

Causa registrada: Aldren Stone causou a morte de John Douran em confronto. (h 1900, evento 2032361).

| Hora | Transformação real | Evento |
|---:|---|---:|
| 1934 | CommitmentCreated | 2070191 |
| 1934 | Pista de Aldren Stone (NPC 3726) em Vallen, (3, 5), observação h 1910, confiança 100%, fonte direct | 2070192 |
| 1942 | Pista de Aldren Stone (NPC 3726) em Vallen, (2, 2), observação h 1942, confiança 100%, fonte direct | 2078930 |
| 1945 | Pista de Aldren Stone (NPC 3726) em Vallen, (2, 2), observação h 1944, confiança 100%, fonte direct | 2082607 |
| 1948 | Pista de Aldren Stone (NPC 3726) em Vallen, (2, 5), observação h 1948, confiança 100%, fonte direct | 2086038 |
| 1980 | Pista de Aldren Stone (NPC 3726) em Vallen, (2, 2), observação h 1980, confiança 100%, fonte direct | 2121175 |
| 1981 | Pista de Aldren Stone (NPC 3726) em Vallen, (2, 2), observação h 1981, confiança 100%, fonte direct | 2122202 |
| 1982 | Pista de Aldren Stone (NPC 3726) em Vallen, (2, 2), observação h 1982, confiança 100%, fonte direct | 2123270 |
| 2297 | Mudança de abordagem: search_area → demand_return | 2483237 |
| 2301 | Pista de Aldren Stone (NPC 3726) em Vallen, (3, 4), observação h 2301, confiança 100%, fonte direct | 2487618 |
| 2362 | Pista de Aldren Stone (NPC 3726) em Vallen, (2, 2), observação h 2362, confiança 100%, fonte direct | 2557855 |
| 2363 | Mudança de abordagem: demand_return → flee | 2559017 |
| 2364 | Pista de Aldren Stone (NPC 3726) em Vallen, (2, 2), observação h 2363, confiança 100%, fonte direct | 2560236 |
| 2364 | Mudança de abordagem: flee → search_area | 2560239 |
| 2365 | Mudança de abordagem: search_area → fill_water | 2561374 |
| 2366 | CommitmentExpired: known_evidence_expired | 2562474 |

Primeira execução social registrada: h 2024, `search_area`, sucesso `True` — Área conhecida observada; ausência não revela destino remoto.. Abordagens registradas: `{'search_area': 5, 'forage': 2, 'follow_lead': 20, 'fill_water': 2, 'demand_return': 1, 'flee': 1}`; execuções sem sucesso: 0. O log social amostra repetições, então esses números não são o total exato de ações.

Leitura: 4 locais de pista distintos, 10 mudanças de abordagem; encerramento `CommitmentExpired`. Pistas descrevem conhecimento recebido, não a posição objetiva atual. Encerrar uma denúncia não comprova captura nem eliminação do adversário.

## 12. Busca sem saída: Aldren Douran (NPC 4941)

Compromisso `1888232`, motivação `family`, alvo inicial Elena Douran (NPC 4944). Nasceu na hora 1769. Fato causal `1838557`.

Personalidade inicial registrada: coragem 7, compaixão 87, vingatividade 86, persistência 95 e lealdade familiar 41 (escala 0–100). Situação no fim da campanha: vivo. Esses valores influenciam escolhas; não comprovam por si sós a razão de um evento.

Causa registrada: Aldren Douran não localiza um familiar há 597 horas. (h 1724, evento 1838557).

| Hora | Transformação real | Evento |
|---:|---|---:|
| 1769 | CommitmentCreated | 1888233 |
| 1769 | Pista de Elena Douran (NPC 4944) em Dorlen, (3, 5), observação h 1127, confiança 100%, fonte direct | 1888234 |
| 1775 | Mudança de abordagem: forage → fill_water | 1894472 |
| 1778 | Passo de viagem física para Dorlen | 1897967 |
| 1778 | Mudança de abordagem: fill_water → follow_lead | 1897968 |
| 1811 | Mudança de abordagem: follow_lead → forage | 1934268 |
| 1889 | Mudança de abordagem: forage → fill_water | 2019914 |
| 1913 | Mudança de abordagem: fill_water → forage | 2046934 |
| 2453 | Mudança de abordagem: fill_water → forage | 2662082 |
| 2468 | Mudança de abordagem: forage → fill_water | 2679045 |
| 2471 | Mudança de abordagem: fill_water → follow_lead | 2682154 |
| 2486 | Mudança de abordagem: follow_lead → forage | 2699794 |
| 2495 | Mudança de abordagem: forage → follow_lead | 2709800 |
| 2511 | Mudança de abordagem: follow_lead → search_area | 2728256 |
| 2513 | Busca entra em espera: local_sources_exhausted; 1 tentativas nesta pista | 2730405 |
| 2774 | CommitmentExpired: finite_intention_horizon | 3026896 |

Primeira execução social registrada: h 1769, `forage`, sucesso `True` — Alimento coletado.. Abordagens registradas: `{'forage': 38, 'fill_water': 11, 'follow_lead': 59, 'search_area': 1}`; execuções sem sucesso: 1. O log social amostra repetições, então esses números não são o total exato de ações.

Enquanto este compromisso estava em espera, entre h 2513 e 2768, ações reais bem-sucedidas: `{'return_from_search': 24, 'eat': 13, 'drink': 12, 'fill_water': 6, 'sleep': 9, 'forage': 10, 'steal_person': 2, 'follow_lead': 28, 'drink_well': 1}`. Não são etapas de um plano da busca.

Leitura: 1 locais de pista distintos, 38 mudanças de abordagem; encerramento `CommitmentExpired`. Pistas descrevem conhecimento recebido, não a posição objetiva atual. Encerrar uma denúncia não comprova captura nem eliminação do adversário.

## 13. Vingança encerrada sem ataque registrado: John Luar (NPC 3017)

Compromisso `2325280`, motivação `revenge`, alvo inicial Cael Corven (NPC 538). Nasceu na hora 2159. Fato causal `2315825`.

Personalidade inicial registrada: coragem 24, compaixão 90, vingatividade 7, persistência 70 e lealdade familiar 62 (escala 0–100). Situação no fim da campanha: vivo. Esses valores influenciam escolhas; não comprovam por si sós a razão de um evento.

Causa registrada: Cael Corven roubou provisão de John Luar. (h 2151, evento 2315825).

| Hora | Transformação real | Evento |
|---:|---|---:|
| 2159 | CommitmentCreated | 2325281 |
| 2159 | Pista de Cael Corven (NPC 538) em Valvia, (2, 2), observação h 2140, confiança 100%, fonte direct | 2325282 |
| 2161 | Pista de Cael Corven (NPC 538) em Valvia, (2, 2), observação h 2160, confiança 100%, fonte direct | 2327712 |
| 2173 | Pista de Cael Corven (NPC 538) em Valvia, (2, 2), observação h 2171, confiança 100%, fonte direct | 2341625 |
| 2201 | Pista de Cael Corven (NPC 538) em Valvia, (3, 4), observação h 2201, confiança 100%, fonte direct | 2372885 |
| 2202 | Pista de Cael Corven (NPC 538) em Valvia, (3, 5), observação h 2202, confiança 100%, fonte direct | 2374600 |
| 2206 | Pista de Cael Corven (NPC 538) em Valvia, (3, 5), observação h 2205, confiança 100%, fonte direct | 2379022 |
| 2236 | Pista de Cael Corven (NPC 538) em Valvia, (2, 2), observação h 2236, confiança 100%, fonte direct | 2413249 |
| 2845 | Pista de Cael Corven (NPC 538) em Valvia, (2, 3), observação h 2843, confiança 100%, fonte direct | 3105765 |
| 2853 | Pista de Cael Corven (NPC 538) em Valvia, (3, 5), observação h 2853, confiança 100%, fonte direct | 3114579 |
| 2855 | Pista de Cael Corven (NPC 538) em Valvia, (3, 5), observação h 2854, confiança 100%, fonte direct | 3116714 |
| 2866 | Pista de Cael Corven (NPC 538) em Valvia, (3, 5), observação h 2865, confiança 100%, fonte direct | 3129224 |
| 2877 | Pista de Cael Corven (NPC 538) em Valvia, (2, 2), observação h 2877, confiança 100%, fonte direct | 3141429 |
| 2880 | Pista de Cael Corven (NPC 538) em Valvia, (2, 2), observação h 2879, confiança 100%, fonte direct | 3144814 |
| 2905 | Pista de Cael Corven (NPC 538) em Valvia, (2, 2), observação h 2902, confiança 100%, fonte direct | 3173016 |
| 2912 | CommitmentCompleted: Intervenção conhecida do guarda | 3180628 |

Leitura: 7 locais de pista distintos, 0 mudanças de abordagem; encerramento `CommitmentCompleted`. Pistas descrevem conhecimento recebido, não a posição objetiva atual. Encerrar uma denúncia não comprova captura nem eliminação do adversário.

## 14. Vingança abandonada: Aldren Hammer (NPC 3744)

Compromisso `1936336`, motivação `revenge`, alvo inicial Iria Arven (NPC 3755). Nasceu na hora 1813. Fato causal `1935230`.

Personalidade inicial registrada: coragem 45, compaixão 76, vingatividade 36, persistência 25 e lealdade familiar 67 (escala 0–100). Situação no fim da campanha: vivo. Esses valores influenciam escolhas; não comprovam por si sós a razão de um evento.

Causa registrada: Iria Arven roubou provisão de Ruan Hammer. (h 1812, evento 1935230).

| Hora | Transformação real | Evento |
|---:|---|---:|
| 1813 | CommitmentCreated | 1936337 |
| 1813 | Pista de Iria Arven (NPC 3755) em Karmar, (3, 5), observação h 1813, confiança 100%, fonte direct | 1936338 |
| 1814 | Pista de Iria Arven (NPC 3755) em Karmar, (2, 5), observação h 1814, confiança 100%, fonte direct | 1937393 |
| 1815 | Pista de Iria Arven (NPC 3755) em Karmar, (1, 5), observação h 1815, confiança 100%, fonte direct | 1938458 |
| 1817 | Pista de Iria Arven (NPC 3755) em Karmar, (1, 5), observação h 1816, confiança 100%, fonte direct | 1940493 |
| 1832 | Pista de Iria Arven (NPC 3755) em Karmar, (2, 2), observação h 1832, confiança 100%, fonte direct | 1957082 |
| 1837 | Pista de Iria Arven (NPC 3755) em Karmar, (2, 2), observação h 1836, confiança 100%, fonte direct | 1962642 |
| 1844 | Pista de Iria Arven (NPC 3755) em Karmar, (2, 2), observação h 1844, confiança 100%, fonte direct | 1969791 |
| 2400 | Pista de Iria Arven (NPC 3755) em Karmar, (3, 5), observação h 2399, confiança 100%, fonte direct | 2601782 |
| 2422 | Pista de Iria Arven (NPC 3755) em Karmar, (2, 2), observação h 2422, confiança 100%, fonte direct | 2627354 |
| 2424 | Pista de Iria Arven (NPC 3755) em Karmar, (2, 2), observação h 2423, confiança 100%, fonte direct | 2629725 |
| 2441 | Pista de Iria Arven (NPC 3755) em Karmar, (2, 2), observação h 2440, confiança 100%, fonte direct | 2648323 |
| 2463 | Pista de Iria Arven (NPC 3755) em Karmar, (1, 5), observação h 2463, confiança 100%, fonte direct | 2673262 |
| 2465 | Pista de Iria Arven (NPC 3755) em Karmar, (1, 5), observação h 2464, confiança 100%, fonte direct | 2675500 |
| 2477 | Pista de Iria Arven (NPC 3755) em Karmar, (2, 5), observação h 2477, confiança 100%, fonte direct | 2688965 |
| 2478 | CommitmentAbandoned: cause_replaced | 2690208 |

Primeira execução social registrada: h 1843, `search_area`, sucesso `True` — Área conhecida observada; ausência não revela destino remoto.. Abordagens registradas: `{'search_area': 1, 'investigate': 1, 'demand_return': 1, 'denounce': 1}`; execuções sem sucesso: 1. O log social amostra repetições, então esses números não são o total exato de ações.

Leitura: 7 locais de pista distintos, 3 mudanças de abordagem; encerramento `CommitmentAbandoned`. Pistas descrevem conhecimento recebido, não a posição objetiva atual. Encerrar uma denúncia não comprova captura nem eliminação do adversário.

## 15. Espera com retorno à rotina: Silas Solaris (NPC 3301)

Compromisso `780390`, motivação `family`, alvo inicial Iria Solaris (NPC 3304). Nasceu na hora 792. Fato causal `780389`.

Personalidade inicial registrada: coragem 27, compaixão 25, vingatividade 60, persistência 87 e lealdade familiar 90 (escala 0–100). Situação no fim da campanha: vivo. Esses valores influenciam escolhas; não comprovam por si sós a razão de um evento.

Causa registrada: Silas Solaris não localiza um familiar há 585 horas. (h 792, evento 780389).

| Hora | Transformação real | Evento |
|---:|---|---:|
| 792 | CommitmentCreated | 780391 |
| 792 | Pista de Iria Solaris (NPC 3304) em Valmar, (3, 5), observação h 207, confiança 100%, fonte direct | 780392 |
| 799 | Busca entra em espera: no_remaining_known_source; 2 tentativas nesta pista | 788812 |
| 1773 | CommitmentExpired: finite_intention_horizon | 1891950 |

Primeira execução social registrada: h 794, `search_area`, sucesso `True` — Área conhecida observada; ausência não revela destino remoto.. Abordagens registradas: `{'search_area': 1}`; execuções sem sucesso: 0. O log social amostra repetições, então esses números não são o total exato de ações.

Enquanto este compromisso estava em espera, entre h 799 e 1772, ações reais bem-sucedidas: `{'search_area': 7, 'drink': 25, 'migrate': 225, 'return_from_search': 23, 'eat': 48, 'drink_well': 20, 'sleep': 96, 'check_relative': 6, 'fill_water': 13, 'work_for_food': 39, 'give_supplies': 2, 'sell_surplus': 10, 'temporary_service': 11, 'buy_food': 4, 'forage': 4, 'denounce': 3, 'demand_return': 2, 'surrender': 1, 'pursue': 6, 'avoid_threat': 2, 'attack': 2}`. Não são etapas de um plano da busca.

Leitura: 1 locais de pista distintos, 0 mudanças de abordagem; encerramento `CommitmentExpired`. Pistas descrevem conhecimento recebido, não a posição objetiva atual. Encerrar uma denúncia não comprova captura nem eliminação do adversário.

## 16. Pedido recusado ou sem informação: Ruan Valerius (NPC 1529)

Compromisso `4624389`, motivação `response`, alvo inicial Tomas Luar (NPC 4932). Nasceu na hora 4243. Fato causal `4624090`.

Personalidade inicial registrada: coragem 17, compaixão 72, vingatividade 90, persistência 79 e lealdade familiar 34 (escala 0–100). Situação no fim da campanha: vivo. Esses valores influenciam escolhas; não comprovam por si sós a razão de um evento.

Causa registrada: Tomas Luar feriu Ruan Valerius em 3 HP. (h 4242, evento 4624090).

| Hora | Transformação real | Evento |
|---:|---|---:|
| 4243 | CommitmentCreated | 4624390 |
| 4243 | Pista de Tomas Luar (NPC 4932) em Dorlen, (2, 2), observação h 4243, confiança 100%, fonte direct | 4624391 |
| 4244 | Mudança de abordagem: attack → defend | 4625363 |
| 4244 | Pista de Tomas Luar (NPC 4932) em Dorlen, (2, 2), observação h 4244, confiança 100%, fonte direct | 4626071 |
| 4245 | Pista de Tomas Luar (NPC 4932) em Dorlen, (2, 2), observação h 4245, confiança 100%, fonte direct | 4627019 |
| 4248 | Pista de Tomas Luar (NPC 4932) em Dorlen, (2, 3), observação h 4248, confiança 100%, fonte direct | 4629439 |
| 4249 | Pista de Tomas Luar (NPC 4932) em Dorlen, (2, 4), observação h 4249, confiança 100%, fonte direct | 4630493 |
| 4250 | Pista de Tomas Luar (NPC 4932) em Dorlen, (2, 5), observação h 4250, confiança 100%, fonte direct | 4631489 |
| 4612 | Pista de Tomas Luar (NPC 4932) em Dorlen, (3, 5), observação h 4609, confiança 100%, fonte direct | 5026879 |
| 4615 | Pista de Tomas Luar (NPC 4932) em Dorlen, (2, 2), observação h 4615, confiança 100%, fonte direct | 5030118 |
| 4621 | Pista de Tomas Luar (NPC 4932) em Dorlen, (2, 2), observação h 4618, confiança 100%, fonte direct | 5036389 |
| 4621 | Mudança de abordagem: ask_about_person → search_area | 5036393 |
| 4624 | Mudança de abordagem: search_area → ask_about_person | 5039591 |
| 4637 | Pista de Tomas Luar (NPC 4932) em Dorlen, (3, 5), observação h 4637, confiança 100%, fonte direct | 5054052 |
| 4639 | Mudança de abordagem: ask_about_person → surrender | 5056291 |
| 4646 | CommitmentAbandoned: no_progress_or_lost_agency | 5064081 |

Primeira execução social registrada: h 4243, `attack`, sucesso `True` — Ataque causou 4 de dano real.. Abordagens registradas: `{'attack': 4, 'defend': 1, 'search_area': 10, 'ask_about_person': 7, 'surrender': 1}`; execuções sem sucesso: 0. O log social amostra repetições, então esses números não são o total exato de ações.

Ataques executados com este compromisso: amostra nas horas `[4243, 4324, 4402, 4564]`. Isso não demonstra intenção de matar.

Leitura: 9 locais de pista distintos, 22 mudanças de abordagem; encerramento `CommitmentAbandoned`. Pistas descrevem conhecimento recebido, não a posição objetiva atual. Encerrar uma denúncia não comprova captura nem eliminação do adversário.

## Todas as fatalidades por combate observadas

| Hora | Autor | Vítima | Intenção | Após incapacidade | Fonte causal | Dano de privação restante |
|---:|---|---|---|---|---:|---:|
| 338 | Tomas Alvor (NPC 3562) | Cael Hammer (NPC 3530) | hurt | False | 307225 | 99 |
| 404 | Bela Ferros (NPC 698) | Mira Ferros (NPC 2575) | hurt | False | 368096 | 99 |
| 405 | Ruan Solaris (NPC 1887) | Tomas Douran (NPC 1901) | repel | False | 368914 | 86 |
| 588 | Elena Hammer (NPC 1233) | Tomas Bruma (NPC 4267) | subdue | False | 556979 | 0 |
| 606 | Ruan Douran (NPC 3932) | Elena Kars (NPC 3963) | contain | False | 577430 | 98 |
| 716 | Bela Stone (NPC 29) | Lyra Montes (NPC 1690) | hurt | False | 695949 | 90 |
| 973 | Cael Arven (NPC 3040) | Marie Valerius (NPC 2989) | subdue | False | 905314 | 0 |
| 1535 | Elena Douran (NPC 3332) | Bela Vale (NPC 3330) | contain | False | 1495428 | 0 |
| 1900 | Aldren Stone (NPC 3726) | John Douran (NPC 3703) | repel | False | 2028895 | 0 |
| 1968 | Darin Douran (NPC 1124) | Aldren Stone (NPC 4064) | contain | False | 2085011 | 0 |
| 2055 | Tomas Vale (NPC 1035) | Bela Luar (NPC 3836) | subdue | False | 2155388 | 0 |
| 2576 | Elena Douran (NPC 3332) | Lyra Vale (NPC 3324) | subdue | False | 2788795 | 0 |
| 3087 | Elena Montes (NPC 2470) | Lyra Vale (NPC 2479) | subdue | False | 3149208 | 0 |
| 3632 | Cael Stone (NPC 4773) | Marie Arven (NPC 4782) | subdue | False | 3960536 | 0 |
| 3876 | Aldren Bruma (NPC 4261) | Darin Hammer (NPC 4279) | subdue | False | 4127092 | 0 |
| 4934 | Elena Stone (NPC 212) | Cael Kars (NPC 1802) | contain | False | 5368136 | 0 |
| 4969 | Aldren Vale (NPC 2924) | Ruan Arven (NPC 2933) | subdue | False | 5087856 | 0 |

Entre as 17 vítimas de combate, 5 tinham pelo menos 80 pontos de dano por privação ainda registrados. Esse dado permanece no personagem após a morte. Confirma debilidade importante, não intenção de homicídio. O golpe final e a vulnerabilidade acumulada devem ser lidos juntos.

## Intenção letal que surgiu

H 1764, Tomas Solaris (NPC 1113), evento 1881774, alvo Aldren Hammer (NPC 4036).

Causa: Aldren Hammer feriu Tomas Solaris em 1 HP. Fato 1791757; compromisso 1824347, motivação `response`. Confiança 100%, intensidade 99.95, episódios 4, alternativas fracassadas 0.

Pressão letal 49.71. Fatores positivos: perda ou perigo grave conhecido: 40.00; mágoa contra o alvo: 34.53; força do compromisso: 19.99; raiva e ressentimento dirigidos: 19.56; vingatividade: 8.55; desespero relacionado: 2.18; investimento no objetivo: 1.33. Barreiras: alternativa não letal plausível: 25.00; compaixão: 12.00; testemunhas: 12.00; temor da reputação: 12.00; medo: 6.00; risco percebido: 5.68; honestidade: 3.75. As pré-condições semânticas foram satisfeitas por `recurrent_physical_danger`; o ruído da escolha não criou a elegibilidade.

O fato referenciado é uma referência causal, não todo o conflito: antes desta escolha, o log registra 10 agressões desse alvo contra o ator, somando 34 HP de dano infligido. A soma é histórica e inclui dano que pode ter sido recuperado; não representa HP faltando. A avaliação agrega episódios distintos e perigo grave.

Comparação entre desfechos plausíveis: `{'repel': 30.57225967310001, 'contain': 31.0, 'subdue': 22.5, 'hurt': 42.620000000000005, 'kill': 49.71}`. O evento registra escolha explícita de `kill`.

## Intenção disponível, com resultado ainda sujeito a Utility

H 897, Ruan Bruma (NPC 4664), evento 899997, alvo Darin Solaris (NPC 4681).

Causa: Darin Solaris feriu Ruan Bruma em 1 HP. Fato 797667; compromisso 807800, motivação `response`. Confiança 100%, intensidade 99.77, episódios 2, alternativas fracassadas 0.

Pressão letal 46.17. Fatores positivos: perda ou perigo grave conhecido: 40.00; mágoa contra o alvo: 34.21; força do compromisso: 19.95; raiva e ressentimento dirigidos: 19.32; vingatividade: 9.60; investimento no objetivo: 1.42; desespero relacionado: 0.93. Barreiras: alternativa não letal plausível: 25.00; compaixão: 24.80; temor da reputação: 12.00; risco percebido: 6.51; medo: 4.51; honestidade: 3.45; testemunhas: 3.00. As pré-condições semânticas foram satisfeitas por `recurrent_physical_danger`; o ruído da escolha não criou a elegibilidade.

## Intenção letal interrompida

H 1778, Tomas Solaris (NPC 1113), evento 1897099, alvo Aldren Hammer (NPC 4036).

Contexto registrado: `{'target': 4036, 'reason': 'timeout'}`.

## Cadeia causal de retaliação

A cadeia abaixo tem referências de fatos efetivamente usados; não recebe rótulo automático de feud.

- H 57: `CharacterAttacked`, Marie Stone (NPC 1771) → Cael Kars (NPC 1802), evento 64332.

- H 57: `CharacterAttacked`, Nora Montes (NPC 1805) → Marie Stone (NPC 1771), evento 64347.

- H 58: `CharacterAttacked`, Marie Stone (NPC 1771) → Nora Montes (NPC 1805), evento 65100.

- H 58: `ProtectionGiven`, Bela Montes (NPC 1808) → Nora Montes (NPC 1805), evento 65114.

## Falhas e lacunas

Casos de gravidade 5 expirados com suspeito ainda vivo no final: 4. Isso comprova falha institucional em concluir estes casos, não que o autor saiba que escapou.

Perguntas podem terminar em recusa ou ausência de informação. Uma fonte pode dar uma observação correta antiga que já não acompanha o alvo. O auditor compara posições apenas para avaliar a pista; o perseguidor não recebe essa comparação.

As histórias de busca demonstram continuidade e mudanças de informação. A repetição de cuidados familiares, a fome e a baixa quantidade de conflitos realmente graves continuam limitando a variedade de desfechos. As categorias sem exemplo natural não foram preenchidas com cenários artificiais.
