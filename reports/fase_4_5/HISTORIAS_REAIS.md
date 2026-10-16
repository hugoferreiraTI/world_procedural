# Histórias reais — Fase 4.5

Seleção de arcos da campanha nova de 5.000 horas, seed Vespera-47. Cada marco abaixo possui ID no registro bruto. “Concluído” significa que a condição da necessidade foi encerrada; não significa necessariamente matar, enriquecer ou encontrar alguém. A duração conta horas desde a adoção do compromisso. Pausas preservam intenção, sem representar trabalho contínuo.

## 1. John Montes — vingança/reparação

Compromisso **#2618083**, h 2224–2839 (615 h). Desfecho: **CommitmentAbandoned**.

Alvo inicialmente conhecido: **John Valerius**, #1476.

Causa conhecida: evento **#2617319**, h 2224: John Valerius roubou comida no mercado de Karlen.

Uma decisão observada: HP 100, fome 44; necessidade `revenge`, ação `pursue`, sucesso=True. Impulso 56.1/100; agência percebida 66.4/100. Esses valores pertencem à amostra registrada, não a toda a trajetória.

Resposta registrada à ação: **Pessoa localizada fisicamente.**. Novo estado medido: HP 100, fome 44; posição {'map_id': 1502, 'x': 2, 'y': 2} → {'map_id': 1502, 'x': 2, 'y': 2}.

Traços iniciais relevantes: ambition=39, persistence=49, vengefulness=73, compassion=11, courage=41. Emotion participa da avaliação do motor, mas não foi amostrada nesta longa; não atribuímos valores ou pensamentos inventados.

Reavaliação posterior observada, h 2635: `pursue`, sucesso=True; resposta: **Busca local sem encontro; não consulta posição remota.**. HP 100 → 100.

| Hora | Evento | Etapa e evidência |
|---|---|---|
| 2224 | #2618084 | objetivo adotado; target=1476 |
| 2224 | #2618085 | intenção pausada; target=1476; competing=food |
| 2292 | #2702499 | intenção retomada; target=1476; competing=revenge |
| 2292 | #2702502 | nova informação; target=1476 |
| 2292 | #2702503 | mudança verificável; changes=['information']; action=pursue; target=1476 |
| 2307 | #2721321 | mudança de estratégia; previous=pursue; next=investigate; target=1476 |
| 2472 | #2926814 | viagem por pista conhecida; target=1476; destination=1502 |
| 2472 | #2926816 | mudança verificável; changes=['approach']; action=follow_lead; target=1476 |
| 2839 | #3385697 | objetivo abandonado; reason=cause_replaced; target=1476 |

Atividade registrada: **24**; episódios de progresso verificável: **20**. Mudanças de estratégia podem ser preparos locais, não transformações profundas de vida.

## 2. Lyra Bruma — perseguição institucional

Compromisso **#4299852**, h 3577–4457 (880 h). Desfecho: **CommitmentAbandoned**.

Alvo inicialmente conhecido: **Arthus Luar**, #4418.

Causa conhecida: evento **#4185950**, h 3484: Arthus Luar roubou comida no mercado de Sildor.

Uma decisão observada: HP 100, fome 44; necessidade `pursuit`, ação `demand_return`, sucesso=True. Impulso 66.2/100; agência percebida 72.5/100. Esses valores pertencem à amostra registrada, não a toda a trajetória.

Resposta registrada à ação: **Interação estruturada registrada: demand_return.**. Novo estado medido: HP 100, fome 44; posição {'map_id': 1192, 'x': 3, 'y': 5} → {'map_id': 1192, 'x': 3, 'y': 5}.

Traços iniciais relevantes: ambition=56, persistence=75, vengefulness=81, compassion=88, courage=36. Emotion participa da avaliação do motor, mas não foi amostrada nesta longa; não atribuímos valores ou pensamentos inventados.

Reavaliação posterior observada, h 3690: `follow_lead`, sucesso=True; resposta: **Viagem física até uma pista conhecida; residência conservada.**. HP 100 → 100.

**Inconsistência confirmada:** este compromisso institucional durou além do prazo da evidência conhecida (h 3652, mesmo usando a gravidade final conhecida pelo guarda). A continuação inclui o bug de reativação/expiração corrigido na entrega; sua duração não deve ser contada como prova de perseguição legitimamente sustentada.

| Hora | Evento | Etapa e evidência |
|---|---|---|
| 3577 | #4299853 | objetivo adotado; target=4418 |
| 3577 | #4299854 | intenção pausada; target=4418; competing=money |
| 3624 | #4358834 | nova informação; target=4418 |
| 3638 | #4375989 | intenção retomada; target=4418; competing=pursuit |
| 3639 | #4377212 | mudança de estratégia; previous=demand_return; next=attack; target=4418 |
| 3681 | #4429111 | viagem por pista conhecida; target=4418; destination=1192 |
| 3681 | #4429113 | mudança verificável; changes=['approach']; action=follow_lead; target=4418 |
| 4457 | #5387037 | objetivo abandonado; reason=no_progress_or_lost_agency; target=4418 |

Atividade registrada: **5**; episódios de progresso verificável: **5**. Mudanças de estratégia podem ser preparos locais, não transformações profundas de vida.

## 3. Iria Montes — ascensão pessoal

Compromisso **#13203**, h 2–512 (510 h). Desfecho: **CommitmentAbandoned**.

Origem registrada na necessidade: `self_assessment:2`; motivo: Acumular uma reserva maior com trabalho e comércio disponíveis.

Uma decisão observada: HP 100, fome 27; necessidade `advancement`, ação `work`, sucesso=True. Impulso 66.2/100; agência percebida 78.3/100. Esses valores pertencem à amostra registrada, não a toda a trajetória.

Resposta registrada à ação: **Produção concluída com pagamento.**. Novo estado medido: HP 100, fome 27; posição {'map_id': 1679, 'x': 3, 'y': 5} → {'map_id': 1679, 'x': 3, 'y': 5}.

Traços iniciais relevantes: ambition=94, persistence=84, vengefulness=76, compassion=50, courage=53. Emotion participa da avaliação do motor, mas não foi amostrada nesta longa; não atribuímos valores ou pensamentos inventados.

Reavaliação posterior observada, h 509: `work`, sucesso=False; resposta: **O estoque já atende à demanda.**. HP 100 → 100.

| Hora | Evento | Etapa e evidência |
|---|---|---|
| 2 | #13204 | objetivo adotado; target=None |
| 2 | #13205 | intenção pausada; target=None; competing=food |
| 5 | #17149 | mudança verificável; changes=['money']; action=work; target=None |
| 50 | #66353 | intenção retomada; target=None; competing=advancement |
| 170 | #180291 | mudança de estratégia; previous=work; next=temporary_service; target=None |
| 512 | #531398 | objetivo abandonado; reason=no_progress_or_lost_agency; target=None |

Atividade registrada: **60**; episódios de progresso verificável: **33**. Mudanças de estratégia podem ser preparos locais, não transformações profundas de vida.

## 4. Iria Montes — cuidado ou busca familiar

Compromisso **#741536**, h 696–1150 (454 h). Desfecho: **CommitmentCompleted**.

Alvo inicialmente conhecido: **Darin Montes**, #2440.

Causa conhecida: evento **#667350**, h 633: Iria Montes não localiza um familiar há 277 horas.

Uma decisão observada: HP 100, fome 55; necessidade `family`, ação `forage`, sucesso=True. Impulso 59.6/100; agência percebida 71.0/100. Esses valores pertencem à amostra registrada, não a toda a trajetória.

Resposta registrada à ação: **Alimento coletado.**. Novo estado medido: HP 100, fome 55; posição {'map_id': 526, 'x': 1, 'y': 5} → {'map_id': 526, 'x': 1, 'y': 5}.

Traços iniciais relevantes: ambition=44, persistence=86, vengefulness=93, compassion=23, courage=25. Emotion participa da avaliação do motor, mas não foi amostrada nesta longa; não atribuímos valores ou pensamentos inventados.

Reavaliação posterior observada, h 1150: `check_relative`, sucesso=True; resposta: **Pessoa localizada; o fato pode ser informado a outro personagem.**. HP 100 → 100.

| Hora | Evento | Etapa e evidência |
|---|---|---|
| 696 | #741537 | objetivo adotado; target=2440 |
| 696 | #741538 | intenção pausada; target=2440; competing=food |
| 705 | #752004 | intenção retomada; target=2440; competing=family |
| 705 | #752006 | mudança verificável; changes=['approach']; action=forage; target=2440 |
| 708 | #755618 | mudança verificável; changes=['provisions', 'resource']; action=forage; target=2440 |
| 711 | #759051 | viagem por pista conhecida; target=2440; destination=284 |
| 711 | #759052 | mudança de estratégia; previous=forage; next=follow_lead; target=2440 |
| 750 | #804463 | mudança verificável; changes=['provisions']; action=fill_water; target=2440 |
| 1150 | #1287328 | nova informação; target=2440 |
| 1150 | #1287330 | mudança verificável; changes=['resolution']; action=check_relative; target=2440 |
| 1150 | #1287331 | objetivo encerrado; reason=verified_need_resolution; target=2440 |

Atividade registrada: **94**; episódios de progresso verificável: **76**. Mudanças de estratégia podem ser preparos locais, não transformações profundas de vida.

## 5. Bela Ferros — proteção

Compromisso **#1732741**, h 1514–1695 (181 h). Desfecho: **CommitmentCompleted**.

Alvo inicialmente conhecido: **Aldren Ferros**, #3400.

Causa conhecida: evento **#1731494**, h 1513: Cael Douran feriu Aldren Ferros em 3 HP.

Uma decisão observada: HP 100, fome 50; necessidade `protection`, ação `denounce`, sucesso=False. Impulso 59.3/100; agência percebida 54.2/100. Esses valores pertencem à amostra registrada, não a toda a trajetória.

Resposta registrada à ação: **Faltam informante, guarda presente ou evidência conhecida.**. Novo estado medido: HP 100, fome 50; posição {'map_id': 724, 'x': 3, 'y': 5} → {'map_id': 724, 'x': 3, 'y': 5}.

Traços iniciais relevantes: ambition=12, persistence=55, vengefulness=82, compassion=58, courage=5. Emotion participa da avaliação do motor, mas não foi amostrada nesta longa; não atribuímos valores ou pensamentos inventados.

Reavaliação posterior observada, h 1695: `stay_near`, sucesso=True; resposta: **Acompanhou o protegido.**. HP 100 → 100.

| Hora | Evento | Etapa e evidência |
|---|---|---|
| 1514 | #1732742 | objetivo adotado; target=3400 |
| 1515 | #1734149 | nova informação; reason=same_intention_new_stage; target=3400 |
| 1515 | #1734154 | mudança de estratégia; previous=denounce; next=attack; target=3400 |
| 1517 | #1736810 | intenção pausada; target=3400; competing=rest |
| 1536 | #1759711 | intenção retomada; target=3400; competing=protection |
| 1536 | #1759715 | mudança verificável; changes=['approach']; action=pursue; target=3400 |
| 1539 | #1763444 | mudança verificável; changes=['information']; action=pursue; target=3400 |
| 1695 | #1955518 | mudança verificável; changes=['resolution']; action=stay_near; target=3400 |
| 1695 | #1955519 | objetivo encerrado; reason=verified_need_resolution; target=3400 |

Atividade registrada: **26**; episódios de progresso verificável: **15**. Mudanças de estratégia podem ser preparos locais, não transformações profundas de vida.

## 6. Mira Kars — mudança de residência

Compromisso **#520654**, h 503–1076 (573 h). Desfecho: **CommitmentCompleted**.

Destino inicial: localidade #209.

Origem registrada na necessidade: `known_towns`; motivo: Considerar mudança por threat.

Uma decisão observada: HP 100, fome 43; necessidade `migration`, ação `forage`, sucesso=True. Impulso 60.7/100; agência percebida 74.3/100. Esses valores pertencem à amostra registrada, não a toda a trajetória.

Resposta registrada à ação: **Alimento coletado.**. Novo estado medido: HP 100, fome 43; posição {'map_id': 180, 'x': 1, 'y': 5} → {'map_id': 180, 'x': 1, 'y': 5}.

Traços iniciais relevantes: ambition=84, persistence=66, vengefulness=91, compassion=62, courage=33. Emotion participa da avaliação do motor, mas não foi amostrada nesta longa; não atribuímos valores ou pensamentos inventados.

Reavaliação posterior observada, h 1076: `migrate`, sucesso=True; resposta: **Uma etapa física da viagem foi realizada.**. HP 100 → 100.

| Hora | Evento | Etapa e evidência |
|---|---|---|
| 503 | #520655 | objetivo adotado; target=209 |
| 503 | #520657 | intenção pausada; target=209; competing=family |
| 521 | #540650 | intenção retomada; target=209; competing=migration |
| 524 | #544067 | mudança verificável; changes=['provisions']; action=forage; target=209 |
| 571 | #596609 | mudança de estratégia; previous=forage; next=buy_food; target=209 |
| 574 | #600358 | mudança verificável; changes=['journey_started']; action=migrate; target=209 |
| 575 | #601464 | nova informação; reason=same_intention_new_stage; target=209 |
| 575 | #601466 | mudança verificável; changes=['approach']; action=migrate; target=209 |
| 1076 | #1197598 | mudança verificável; changes=['approach', 'resolution']; action=migrate; target=209 |
| 1076 | #1197599 | objetivo encerrado; reason=verified_need_resolution; target=209 |

Atividade registrada: **127**; episódios de progresso verificável: **123**. Mudanças de estratégia podem ser preparos locais, não transformações profundas de vida.

## 7. Tomas Bruma — reconhecimento

Compromisso **#64074**, h 48–181 (133 h). Desfecho: **CommitmentCompleted**.

Origem registrada na necessidade: `aspiration:recognition`; motivo: Melhorar condição pessoal por oportunidade conhecida.

Uma decisão observada: HP 100, fome 32; necessidade `status`, ação `drink`, sucesso=True. Impulso 67.6/100; agência percebida 77.6/100. Esses valores pertencem à amostra registrada, não a toda a trajetória.

Resposta registrada à ação: **Sede reduzida.**. Novo estado medido: HP 100, fome 32; posição {'map_id': 461, 'x': 2, 'y': 2} → {'map_id': 461, 'x': 2, 'y': 2}.

Traços iniciais relevantes: ambition=95, persistence=53, vengefulness=70, compassion=92, courage=51. Emotion participa da avaliação do motor, mas não foi amostrada nesta longa; não atribuímos valores ou pensamentos inventados.

Reavaliação posterior observada, h 181: `give_supplies`, sucesso=True; resposta: **Ajuda material prestada.**. HP 100 → 100.

| Hora | Evento | Etapa e evidência |
|---|---|---|
| 48 | #64075 | objetivo adotado; target=None |
| 48 | #64076 | intenção pausada; target=None; competing=advancement |
| 96 | #110471 | intenção retomada; target=None; competing=status |
| 99 | #113430 | mudança de estratégia; previous=drink; next=work; target=None |
| 168 | #177938 | mudança verificável; changes=['public_recognition']; action=work; target=None |
| 181 | #189855 | mudança verificável; changes=['resolution']; action=give_supplies; target=None |
| 181 | #189856 | objetivo encerrado; reason=verified_need_resolution; target=None |

Atividade registrada: **14**; episódios de progresso verificável: **2**. Mudanças de estratégia podem ser preparos locais, não transformações profundas de vida.

## 8. Mira Ferros — luto

Compromisso **#2594388**, h 2205–2268 (63 h). Desfecho: **CommitmentCompleted**.

Alvo inicialmente conhecido: **Bela Ferros**, #4675.

Causa conhecida: evento **#2593278**, h 2204: Marie Montes causou a morte de Bela Ferros em confronto.

Uma decisão observada: HP 100, fome 46; necessidade `grief`, ação `drink`, sucesso=True. Impulso 82.2/100; agência percebida 72.1/100. Esses valores pertencem à amostra registrada, não a toda a trajetória.

Resposta registrada à ação: **Sede reduzida.**. Novo estado medido: HP 100, fome 46; posição {'map_id': 1304, 'x': 2, 'y': 2} → {'map_id': 1304, 'x': 2, 'y': 2}.

Traços iniciais relevantes: ambition=79, persistence=93, vengefulness=62, compassion=12, courage=81. Emotion participa da avaliação do motor, mas não foi amostrada nesta longa; não atribuímos valores ou pensamentos inventados.

Reavaliação posterior observada, h 2268: `remember_relative`, sucesso=True; resposta: **Visitou um local relacionado à perda.**. HP 100 → 100.

| Hora | Evento | Etapa e evidência |
|---|---|---|
| 2205 | #2594389 | objetivo adotado; target=4675 |
| 2205 | #2594390 | intenção pausada; target=4675; competing=food |
| 2263 | #2666575 | intenção retomada; target=4675; competing=grief |
| 2264 | #2667879 | mudança de estratégia; previous=drink; next=remember_relative; target=4675 |
| 2264 | #2667880 | mudança verificável; changes=['approach']; action=remember_relative; target=4675 |
| 2268 | #2672683 | mudança verificável; changes=['resolution']; action=remember_relative; target=4675 |
| 2268 | #2672684 | objetivo encerrado; reason=verified_need_resolution; target=4675 |

Atividade registrada: **6**; episódios de progresso verificável: **5**. Mudanças de estratégia podem ser preparos locais, não transformações profundas de vida.

## 9. Lyra Valerius — cuidado ou busca familiar

Compromisso **#4692355**, h 3892–4330 (438 h). Desfecho: **CommitmentAbandoned**.

Alvo inicialmente conhecido: **Lyra Valerius**, #5427.

Causa conhecida: evento **#4692354**, h 3892: Lyra Valerius não localiza um familiar há 414 horas.

Uma decisão observada: HP 25, fome 2; necessidade `family`, ação `check_relative`, sucesso=True. Impulso 66.9/100; agência percebida 56.5/100. Esses valores pertencem à amostra registrada, não a toda a trajetória.

Resposta registrada à ação: **A pessoa não foi localizada nesta posição.**. Novo estado medido: HP 25, fome 2; posição {'map_id': 1643, 'x': 3, 'y': 5} → {'map_id': 1643, 'x': 3, 'y': 5}.

Traços iniciais relevantes: ambition=47, persistence=5, vengefulness=24, compassion=10, courage=73. Emotion participa da avaliação do motor, mas não foi amostrada nesta longa; não atribuímos valores ou pensamentos inventados.

Reavaliação posterior observada, h 4329: `follow_lead`, sucesso=True; resposta: **Você entrou em Dormir.**. HP 100 → 100.

| Hora | Evento | Etapa e evidência |
|---|---|---|
| 3892 | #4692356 | objetivo adotado; target=5427 |
| 3893 | #4693589 | intenção pausada; target=5427; competing=food_reserve |
| 3941 | #4753298 | intenção retomada; target=5427; competing=family |
| 3941 | #4753300 | nova informação; target=5427 |
| 3941 | #4753302 | mudança de estratégia; previous=check_relative; next=ask_personal_help; target=5427 |
| 3941 | #4753303 | mudança verificável; changes=['information']; action=ask_personal_help; target=5427 |
| 3942 | #4754703 | viagem por pista conhecida; target=5427; destination=1661 |
| 3942 | #4754705 | mudança verificável; changes=['approach']; action=follow_lead; target=5427 |
| 4330 | #5232369 | objetivo abandonado; reason=no_progress_or_lost_agency; target=5427 |

Atividade registrada: **22**; episódios de progresso verificável: **17**. Mudanças de estratégia podem ser preparos locais, não transformações profundas de vida.

## 10. Iria Montes — cuidado ou busca familiar

Compromisso **#5171590**, h 4281–5000 (719 h). Desfecho: **ainda sem encerramento**.

Alvo inicialmente conhecido: **Lyra Montes**, #3559.

Causa conhecida: evento **#5171589**, h 4281: Iria Montes não localiza um familiar há 2020 horas.

Uma decisão observada: HP 100, fome 40; necessidade `family`, ação `forage`, sucesso=True. Impulso 63.8/100; agência percebida 63.3/100. Esses valores pertencem à amostra registrada, não a toda a trajetória.

Resposta registrada à ação: **Alimento coletado.**. Novo estado medido: HP 100, fome 40; posição {'map_id': 630, 'x': 1, 'y': 7} → {'map_id': 630, 'x': 1, 'y': 7}.

Traços iniciais relevantes: ambition=61, persistence=39, vengefulness=10, compassion=71, courage=48. Emotion participa da avaliação do motor, mas não foi amostrada nesta longa; não atribuímos valores ou pensamentos inventados.

Reavaliação posterior observada, h 4979: `follow_lead`, sucesso=True; resposta: **Viagem física até uma pista conhecida; residência conservada.**. HP 100 → 100.

| Hora | Evento | Etapa e evidência |
|---|---|---|
| 4281 | #5171591 | objetivo adotado; target=3559 |
| 4281 | #5171593 | intenção pausada; target=3559; competing=family |
| 4323 | #5223101 | intenção retomada; target=3559; competing=family |
| 4323 | #5223104 | mudança verificável; changes=['provisions', 'resource']; action=forage; target=3559 |
| 4326 | #5226795 | mudança de estratégia; previous=forage; next=fill_water; target=3559 |
| 4326 | #5226796 | mudança verificável; changes=['provisions']; action=fill_water; target=3559 |
| 4329 | #5230613 | viagem por pista conhecida; target=3559; destination=789 |
| 4329 | #5230615 | mudança verificável; changes=['approach']; action=follow_lead; target=3559 |
| 4995 | #6028953 | mudança verificável; changes=['approach']; action=forage; target=3559 |

Atividade registrada: **106**; episódios de progresso verificável: **101**. Mudanças de estratégia podem ser preparos locais, não transformações profundas de vida.

## 11. John Valerius — vingança/reparação

Compromisso **#871948**, h 807–1315 (508 h). Desfecho: **CommitmentAbandoned**.

Alvo inicialmente conhecido: **Elena Valerius**, #4993.

Causa conhecida: evento **#868756**, h 804: Elena Valerius roubou comida no mercado de Ardor.

Uma decisão observada: HP 100, fome 51; necessidade `revenge`, ação `denounce`, sucesso=False. Impulso 42.5/100; agência percebida 51.3/100. Esses valores pertencem à amostra registrada, não a toda a trajetória.

Resposta registrada à ação: **Faltam informante, guarda presente ou evidência conhecida.**. Novo estado medido: HP 100, fome 51; posição {'map_id': 1549, 'x': 2, 'y': 2} → {'map_id': 1549, 'x': 2, 'y': 2}.

Traços iniciais relevantes: ambition=76, persistence=7, vengefulness=88, compassion=23, courage=59. Emotion participa da avaliação do motor, mas não foi amostrada nesta longa; não atribuímos valores ou pensamentos inventados.

Reavaliação posterior observada, h 1223: `follow_lead`, sucesso=True; resposta: **Você entrou em Ardor.**. HP 26 → 26.

| Hora | Evento | Etapa e evidência |
|---|---|---|
| 807 | #871949 | objetivo adotado; target=4993 |
| 807 | #871950 | intenção pausada; target=4993; competing=family |
| 874 | #952395 | intenção retomada; target=4993; competing=revenge |
| 877 | #956114 | mudança verificável; changes=['approach']; action=denounce; target=4993 |
| 994 | #1098177 | mudança de estratégia; previous=denounce; next=fill_water; target=4993 |
| 994 | #1098178 | mudança verificável; changes=['provisions']; action=fill_water; target=4993 |
| 997 | #1101789 | viagem por pista conhecida; target=4993; destination=1726 |
| 1315 | #1489463 | objetivo abandonado; reason=no_progress_or_lost_agency; target=4993 |

Atividade registrada: **60**; episódios de progresso verificável: **47**. Mudanças de estratégia podem ser preparos locais, não transformações profundas de vida.

## 12. John Douran — perseguição institucional

Compromisso **#5433243**, h 4494–4819 (325 h). Desfecho: **CommitmentAbandoned**.

Alvo inicialmente conhecido: **Darin Ferros**, #3955.

Causa conhecida: evento **#5335260**, h 4414: Darin Ferros feriu John Douran em 9 HP.

Uma decisão observada: HP 100, fome 53; necessidade `pursuit`, ação `watch_case`, sucesso=True. Impulso 63.9/100; agência percebida 58.6/100. Esses valores pertencem à amostra registrada, não a toda a trajetória.

Resposta registrada à ação: **Vigilância local realizada sem consultar localização remota.**. Novo estado medido: HP 100, fome 53; posição {'map_id': 976, 'x': 2, 'y': 2} → {'map_id': 976, 'x': 2, 'y': 2}.

Traços iniciais relevantes: ambition=15, persistence=86, vengefulness=52, compassion=7, courage=17. Emotion participa da avaliação do motor, mas não foi amostrada nesta longa; não atribuímos valores ou pensamentos inventados.

Reavaliação posterior observada, h 4818: `surrender`, sucesso=True; resposta: **Rendição registrada; não implica morte.**. HP 100 → 100.

| Hora | Evento | Etapa e evidência |
|---|---|---|
| 4494 | #5433244 | objetivo adotado; target=3955 |
| 4494 | #5433245 | intenção pausada; target=3955; competing=rest |
| 4522 | #5467017 | intenção retomada; target=3955; competing=pursuit |
| 4522 | #5467020 | mudança verificável; changes=['approach']; action=watch_case; target=3955 |
| 4559 | #5511328 | mudança de estratégia; previous=watch_case; next=fill_water; target=3955 |
| 4559 | #5511329 | mudança verificável; changes=['provisions']; action=fill_water; target=3955 |
| 4594 | #5553872 | nova informação; target=3955 |
| 4594 | #5553873 | mudança verificável; changes=['information']; action=watch_case; target=3955 |
| 4819 | #5823579 | objetivo abandonado; reason=no_progress_or_lost_agency; target=3955 |

Atividade registrada: **68**; episódios de progresso verificável: **38**. Mudanças de estratégia podem ser preparos locais, não transformações profundas de vida.

## 13. Ruan Stone — ascensão pessoal

Compromisso **#9548**, h 1–730 (729 h). Desfecho: **CommitmentAbandoned**.

Origem registrada na necessidade: `self_assessment:1`; motivo: Acumular uma reserva maior com trabalho e comércio disponíveis.

Uma decisão observada: HP 100, fome 41; necessidade `advancement`, ação `work`, sucesso=True. Impulso 60.4/100; agência percebida 90.9/100. Esses valores pertencem à amostra registrada, não a toda a trajetória.

Resposta registrada à ação: **Serviço realizado.**. Novo estado medido: HP 100, fome 41; posição {'map_id': 854, 'x': 3, 'y': 5} → {'map_id': 854, 'x': 3, 'y': 5}.

Traços iniciais relevantes: ambition=80, persistence=6, vengefulness=74, compassion=95, courage=79. Emotion participa da avaliação do motor, mas não foi amostrada nesta longa; não atribuímos valores ou pensamentos inventados.

Reavaliação posterior observada, h 343: `work`, sucesso=True; resposta: **Serviço realizado.**. HP 100 → 100.

| Hora | Evento | Etapa e evidência |
|---|---|---|
| 1 | #9549 | objetivo adotado; target=None |
| 1 | #9551 | mudança verificável; changes=['money']; action=work; target=None |
| 4 | #15312 | intenção pausada; target=None; competing=food |
| 10 | #23687 | intenção retomada; target=None; competing=advancement |
| 19 | #37777 | mudança de estratégia; previous=work; next=steal_person; target=None |
| 730 | #781680 | objetivo abandonado; reason=no_progress_or_lost_agency; target=None |

Atividade registrada: **44**; episódios de progresso verificável: **38**. Mudanças de estratégia podem ser preparos locais, não transformações profundas de vida.

## 14. Elena Vale — cuidado ou busca familiar

Compromisso **#2575578**, h 2190–2706 (516 h). Desfecho: **CommitmentExpired**.

Alvo inicialmente conhecido: **Mira Vale**, #4652.

Causa conhecida: evento **#2561813**, h 2179: Elena Vale percebeu a privação de Mira Vale.

Uma decisão observada: HP 100, fome 47; necessidade `family`, ação `check_relative`, sucesso=True. Impulso 58.6/100; agência percebida 70.8/100. Esses valores pertencem à amostra registrada, não a toda a trajetória.

Resposta registrada à ação: **A pessoa não foi localizada nesta posição.**. Novo estado medido: HP 100, fome 47; posição {'map_id': 1286, 'x': 2, 'y': 2} → {'map_id': 1286, 'x': 2, 'y': 2}.

Traços iniciais relevantes: ambition=45, persistence=70, vengefulness=86, compassion=5, courage=73. Emotion participa da avaliação do motor, mas não foi amostrada nesta longa; não atribuímos valores ou pensamentos inventados.

Reavaliação posterior observada, h 2694: `ask_personal_help`, sucesso=False; resposta: **Resposta sem avanço: no_information.**. HP 50 → 50.

| Hora | Evento | Etapa e evidência |
|---|---|---|
| 2190 | #2575579 | objetivo adotado; target=4652 |
| 2190 | #2575580 | intenção pausada; target=4652; competing=revenge |
| 2209 | #2599241 | intenção retomada; target=4652; competing=family |
| 2247 | #2646534 | mudança de estratégia; previous=check_relative; next=forage; target=4652 |
| 2358 | #2784226 | nova informação; target=4652 |
| 2426 | #2868582 | mudança verificável; changes=['approach']; action=forage; target=4652 |
| 2706 | #3219603 | intenção expirada; reason=owner_died; target=4652 |

Atividade registrada: **14**; episódios de progresso verificável: **5**. Mudanças de estratégia podem ser preparos locais, não transformações profundas de vida.

## Fatalidades e repercussões

- h 554, evento #578027: Arthus Solaris causou a morte de Mira Ferros em confronto. Intenção registrada: `hurt`. Compromissos diretamente ligados à notícia: #595651, #649335.
- h 2004, evento #2344209: Iria Corven causou a morte de Nora Stone em confronto. Intenção registrada: `subdue`. Compromissos diretamente ligados à notícia: #2345400, #2345402.
- h 2204, evento #2593278: Marie Montes causou a morte de Bela Ferros em confronto. Intenção registrada: `hurt`. Compromissos diretamente ligados à notícia: #2594388, #2611316.
- h 2246, evento #2644776: Iria Alvor causou a morte de Iria Montes em confronto. Intenção registrada: `hurt`. Compromissos diretamente ligados à notícia: nenhum registrado.
- h 2624, evento #3117598: Bela Stone causou a morte de John Arven em confronto. Intenção registrada: `hurt`. Compromissos diretamente ligados à notícia: nenhum registrado.
- h 2706, evento #3219604: Aldren Arven causou a morte de Elena Vale em confronto. Intenção registrada: `subdue`. Compromissos diretamente ligados à notícia: nenhum registrado.
- h 2742, evento #3263937: Lyra Bruma causou a morte de Arthus Hammer em confronto. Intenção registrada: `subdue`. Compromissos diretamente ligados à notícia: #3264618.
- h 3923, evento #4730815: Iria Montes causou a morte de Lyra Kars em confronto. Intenção registrada: `contain`. Compromissos diretamente ligados à notícia: #4730823, #4730825.
- h 4539, evento #5486689: Nora Ferros causou a morte de Darin Arven em confronto. Intenção registrada: `subdue`. Compromissos diretamente ligados à notícia: nenhum registrado.
- h 4730, evento #5717566: Tomas Bruma causou a morte de Iria Corven em confronto. Intenção registrada: `subdue`. Compromissos diretamente ligados à notícia: nenhum registrado.

Intenções nas fatalidades reais: `{'hurt': 4, 'subdue': 5, 'contain': 1}`; ataques fatais após incapacidade: **0**. Ferir/subjugar ainda pode matar por dano físico, especialmente quando a vítima já tem pouco HP. Uma fatalidade sozinha não comprova execução deliberada de vingança.

## Passividade observada

- h 408: Tomas Kars contra Mira Arven; compromisso #410571, grievance=69.2, ação atual=sleep, diagnóstico=`distance_or_stale_lead`. O diagnóstico descreve essa amostra diária, sem concluir que o NPC permaneceu assim todo o tempo.
- h 408: Ruan Vale contra Cael Hammer; compromisso #412464, grievance=79.9, ação atual=sleep, diagnóstico=`distance_or_stale_lead`. O diagnóstico descreve essa amostra diária, sem concluir que o NPC permaneceu assim todo o tempo.
- h 432: Ruan Vale contra Cael Hammer; compromisso #412464, grievance=79.3, ação atual=eat, diagnóstico=`distance_or_stale_lead`. O diagnóstico descreve essa amostra diária, sem concluir que o NPC permaneceu assim todo o tempo.

## Complemento: cadeias medidas na curta da entrega

Os próximos casos pertencem à execução independente de 500 h do código corrigido. IDs de eventos são locais a essa execução; não ligá-los aos IDs da longa. A curta amostrou emoções antes/depois, prioridade antes da ação e score da solução escolhida.

### Arthus Luar — h 0, ascensão pessoal

**State:** HP 100, fome 19, dinheiro 16. **Knowledge:** avaliação pessoal/oportunidade registrada em self_assessment:0; avaliação própria, confiança registrada 100. **Emotion:** raiva 0.0, ressentimento 0.0, desespero 0.0. **Need:** advancement, prioridade 51.8. **Impulse:** 61.7; **Commitment:** #5676. **Solution/Action:** `work`, score 57.0. **Response:** Serviço realizado.. **Consequence/New State:** HP 100, fome 19, dinheiro 17; progresso verificável acumulado no compromisso 1.

### Aldren Montes — h 0, cuidado ou busca familiar

**State:** HP 100, fome 42, dinheiro 8. **Knowledge:** Aldren Montes percebeu a privação de Nora Montes.; fato #5995, confiança registrada 100. **Emotion:** raiva 0.0, ressentimento 0.0, desespero 0.0. **Need:** family, prioridade 80.0. **Impulse:** 68.4; **Commitment:** #5998. **Solution/Action:** `buy_food`, score 85.0. **Response:** Compra concluída por 2 moedas.. **Consequence/New State:** HP 100, fome 42, dinheiro 6; progresso verificável acumulado no compromisso 1.

### Cael Vale — h 142, perseguição institucional

**State:** HP 100, fome 54, dinheiro 21. **Knowledge:** Lyra Arven roubou comida no mercado de Norria.; fato #62532, confiança registrada 60. **Emotion:** raiva 0.0, ressentimento 0.0, desespero 0.0. **Need:** pursuit, prioridade 79.5. **Impulse:** 57.4; **Commitment:** #125929. **Solution/Action:** `defend`, score 58.2. **Response:** Defesa temporária adotada.. **Consequence/New State:** HP 100, fome 54, dinheiro 21; progresso verificável acumulado no compromisso 0.


## Limite desta seleção

Os registros permitem conferir fatos, decisões e transições; não reconstruímos pensamentos ou valores emocionais que não foram amostrados. Um arco longo pode continuar pobre em transformações. O JSON de arcos preserva os demais casos, inclusive falhas e objetivos pendentes.
