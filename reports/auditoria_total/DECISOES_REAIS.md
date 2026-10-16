# DECISÕES REAIS — por que fez, não fez ou falhou

Dados da campanha única **Thalven-Radiografia55**,300h,sem jogador,histórico inicial0. São decisões capturadas enquanto o motor executava, sem reconsultar solutions nem recalcular Utility. A amostragem privilegia diversidade técnica; sua proporção não estima frequência no mundo. Horas são world.turn durante a decisão, antes do fechamento fisiológico. “Sem execução” pode significar que a caminhada consumiu o elapsed.

O estado de entrada precede refresh/percepção; a lista de Needs já é posterior ao refresh real. Fonte conhecida é amostra dos fatos ligados aos contextos. Relações e known_target coletados ao final são marcados como posteriores. Coleções emocionais que tiveram cópia rasa foram removidas, preservando só escalares. “ND” ou “LACUNA” significa que o observador não reteve o dado, sem preenchimento retrospectivo.

## Cobertura da amostragem

| Categoria | Retidas | Apresentadas |
| --- | --- | --- |
| blocked | 5 | 3 |
| career | 4 | 3 |
| combat | 3 | 3 |
| crime | 4 | 3 |
| faction | 4 | 3 |
| family | 4 | 3 |
| food | 4 | 3 |
| group | 4 | 2 |
| investigation | 4 | 2 |
| justice | 4 | 2 |
| lethal | 1 | 1 |
| migration | 4 | 2 |
| money | 4 | 2 |
| policy | 4 | 2 |
| proposal | 4 | 2 |
| recovery | 4 | 2 |
| religion | 4 | 2 |
| rest | 4 | 2 |
| social | 4 | 2 |
| travel | 4 | 2 |
| water | 4 | 2 |
| work | 4 | 2 |

Categorias sem trace de decisão retido: nenhuma. Conferir contadores de chamadas/eventos antes de concluir ausência: o mapeamento de categoria pode classificar o mesmo fenômeno em mais de uma fronteira, mas retém uma categoria por decisão.

A categoria lethal inclui uma avaliação letal real reclassificada editorialmente de combat. A ação final foi attack; não houve finish. Agency.adjust pode consultar terminal() ainda com alvo acima de12HP e só aplicar o bônus terminal abaixo do limiar. Portanto uma tabela com choice=spare não prova que o NPC poupou um incapacitado naquela hora; verificar HP, função chamadora e evento de execução.

## Por que fez / por que não fez / por que falhou

### 01. blocked — Bela Hammer #1165, h155: sem seleção

**Sem seleção viável** no retorno de decide. Isso não demonstra ausência de todas as pressões: examinar Needs e avaliações abaixo.

**Entrada:** {"id":1165,"name":"Bela Hammer","hour":155,"alive":true,"profession":"caçador","lod":"active","position":{"map_id":3,"x":7,"y":13},"residence":3,"hp":100,"hunger":78,"thirst":85,"fatigue":22.00000000000001,"money":1,"food":0,"water":0,"local_food":0,"local_water":0,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{"drink_well":157}}.

**Personalidade:** {"honesty":78,"compassion":32,"courage":5,"independence":8,"greed":58,"diligence":53,"family_loyalty":95,"persistence":50,"temperament":61,"vengefulness":43,"ambition":34,"sadism":0}. **Emoções escalares de entrada:** {"anger":100.0,"resentment":100.0,"humiliation":100.0,"desperation":5.150000000000001,"last_updated":154,"last_support":-10000,"strain":10.075500000000003,"adaptation":0,"last_adapted":0,"stable_material_hours":0,"nested_collections":"LACUNA: cópia rasa; histórico não utilizado"}.

**Conhecimento/locais de entrada:** {"known_places":{"home":{"map_id":1162,"x":5,"y":5},"work":{"map_id":1162,"x":5,"y":5},"forage":{"map_id":3,"x":1,"y":13},"sacred":{"map_id":1162,"x":5,"y":1},"market":{"map_id":3,"x":7,"y":13},"well_rural":{"map_id":3,"x":1,"y":13}},"known_towns":[3,32],"route_knowledge_count":4,"knowledge_ids_before":[202683,202692,202699,202711,202714,202717,202723,203798,203815,203837,203839,203844,203848,203857,198567,198604,204985,204987,204996,205005,205012,205018,205025,205034,205041,206003,206009,206011,206018,206025,206026,206027,206028,206034,206047,206051,206228,206840,206968,206970,206982,207000,207001,207004,207009,207013,207016,207020,207821,207988,207990,207991,208018,208034,208041,208047,208049,208989,208991,209005,209009,209029,209034,209204],"market_observation":{"turn":154,"town_id":3,"stock":{"food":1,"grain":94,"water":0,"iron":114,"wood":82},"temporary_work":true,"offers_expire_at":178,"training_offer":null,"price":14,"price_turn":154}}.

**Fatos-fonte retidos após percepção:** [{"event_id":209005,"kind":"ItemStolen","actor_id":1308,"target_id":3,"location":{"map_id":3,"x":7,"y":13},"turn":154,"description":"Bela Luar roubou comida no mercado de Dorria.","confidence":100,"required_trust":0,"source_id":null,"source_kind":"direct","context":{"item_id":201453,"item_kind":"food"}}].

| Need | ID/alvo | Base→prioridade | Estado/fonte |
| --- | --- | --- | --- |
| food | 13985/None | 97.0→100 | active / physiology |
| water | 39351/None | 85→100 | active / physiology |
| political_pressure | 109659/None | 80→94.2325 | active / own_shared_problem |
| protection | 124993/1165 | 45→92.10502602484472 | active / event:209005 |
| money | 116857/None | 51.333333333333336→70.37733333333334 | active / economy |
| food_reserve | 83311/None | 41.0→69.87912087912088 | active / food_reserve |
| organizational_access | 13990/1168 | 53→61.0 | active / organization |
| migration | 126074/32 | 52→60.444 | active / known_towns |
| organizational_survival | 13988/1165 | 48.744→59.2248 | active / faction:1168 |
| work | 30736/None | 35→46.050000000000004 | active / profession |
| advancement | 13987/None | 21.0684→38.7295304 | blocked / aspiration:wealth |

**Alternativas/gates realmente vistos:**

Need #13985 (`food`): 0 Solutions entraram em _evaluate; 0 saíram disponíveis. Entrada: ``.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |

Need #39351 (`water`): 1 Solutions entraram em _evaluate; 0 saíram disponíveis. Entrada: `drink_well`.

| Opção | Alvo | Etapa | Motivo observado | Auditoria/feeding |
| --- | --- | --- | --- | --- |
| drink_well | None | before_Utility_or_unresolved | cooldown_after_failure | {"pressure":null,"feeding":null} |

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |

Need #109659 (`political_pressure`): 0 Solutions entraram em _evaluate; 0 saíram disponíveis. Entrada: ``.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |

Need #124993 (`protection`): 0 Solutions entraram em _evaluate; 0 saíram disponíveis. Entrada: ``.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |

Need #116857 (`money`): 0 Solutions entraram em _evaluate; 0 saíram disponíveis. Entrada: ``.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |

Need #83311 (`food_reserve`): 0 Solutions entraram em _evaluate; 0 saíram disponíveis. Entrada: ``.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |

Need #13990 (`organizational_access`): 0 Solutions entraram em _evaluate; 0 saíram disponíveis. Entrada: ``.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |

Need #126074 (`migration`): 0 Solutions entraram em _evaluate; 0 saíram disponíveis. Entrada: ``.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |

Need #13988 (`organizational_survival`): 0 Solutions entraram em _evaluate; 0 saíram disponíveis. Entrada: ``.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |

Need #30736 (`work`): 0 Solutions entraram em _evaluate; 0 saíram disponíveis. Entrada: ``.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |

Need #13987 (`advancement`): 0 Solutions entraram em _evaluate; 0 saíram disponíveis. Entrada: ``.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |

**Escolhas intermediárias:** [].

**Preparação/substituição posterior:** [].

**Winner final / Goal:** {"winner":{},"goal":null,"suspended_before":null,"suspended_after":null}.

**Execução:** execute não foi chamado neste trace. A Goal pode ter iniciado/continuado deslocamento; o snapshot e a posição posterior delimitam essa conclusão.

**Cálculos especializados reais:** [{"system":"lethal_decision","function":"lethal_decisions.LethalDecisionSystem.evaluate","result":{"available":false,"pressure":-51.68,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":209986,"motive":"protection","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":7.3100000000000005,"directed_emotion":7.8705000000000025,"commitment":7.165650559006211,"sadism":0.0,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":17.6,"moral_restraint":9.36,"fear":0.0,"risk":2.062111801242236,"bond":0.0,"authority_or_witnesses":15,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":59.7137546583851,"commitment_intensity":59.7137546583851},"inputs":{"pressure":-51.68,"cause":{"severity":0,"grave":false,"causes":[],"facts":[],"confidence":0,"mode":"retributive","confirmed_injury":0}}},{"system":"lethal_decision","function":"lethal_decisions.LethalDecisionSystem.evaluate","result":{"available":false,"pressure":-51.68,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":209986,"motive":"protection","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":7.3100000000000005,"directed_emotion":7.8705000000000025,"commitment":7.165650559006211,"sadism":0.0,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":17.6,"moral_restraint":9.36,"fear":0.0,"risk":2.062111801242236,"bond":0.0,"authority_or_witnesses":15,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":59.7137546583851,"commitment_intensity":59.7137546583851},"inputs":{"pressure":-51.68,"cause":{"severity":0,"grave":false,"causes":[],"facts":[],"confidence":0,"mode":"retributive","confirmed_injury":0}}},{"system":"lethal_pressure","function":"lethality.LethalPressure.evaluate","result":{"available":false,"pressure":-51.68,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":209986,"motive":"protection","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":7.3100000000000005,"directed_emotion":7.8705000000000025,"commitment":7.165650559006211,"sadism":0.0,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":17.6,"moral_restraint":9.36,"fear":0.0,"risk":2.062111801242236,"bond":0.0,"authority_or_witnesses":15,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":59.7137546583851,"commitment_intensity":59.7137546583851},"inputs":{}}].

| Evento/hora | Actor→target | Emissor | Testemunhas | Contexto |
| --- | --- | --- | --- | --- |
| 209985 / 155 / CommitmentAbandoned | 1165→None | ["agency.AgencySystem.event","agency.AgencySystem.close","agency.AgencySystem.refresh"] | [1165] | {"reason":"cause_replaced","duration":1,"activity":0,"meaningful_progress":0,"strategy_changes":0,"commitment_id":208990,"need_id":124993,"origin":"protection","source_fact":208047,"target":1165,"progress":0} |
| 209987 / 155 / CommitmentCreated | 1165→None | ["agency.AgencySystem.event","agency.AgencySystem.adopt","agency.AgencySystem.refresh"] | [1165] | {"impulse":59.7137546583851,"agency":0.555631469979296,"commitment_id":209986,"need_id":124993,"origin":"protection","source_fact":209005,"target":1165,"progress":0} |

**Aprendizado aceito durante a decisão (amostra):** [{"npc":1165,"event":209985,"kind":"CommitmentAbandoned","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":1165,"event":209987,"kind":"CommitmentCreated","source":null,"firsthand":true,"confidence":100,"latency":0}].

**Recibos posteriores ligados ao mesmo event_id:** [{"event":209985,"kind":"CommitmentAbandoned","learned":{"count":1,"first":155,"last":155,"first_people":[1165]}},{"event":209987,"kind":"CommitmentCreated","learned":{"count":1,"first":155,"last":155,"first_people":[1165]}}]. Contagem é operações de aprendizado aceitas, não indivíduos únicos.

**Consequência imediata:** {"id":1165,"name":"Bela Hammer","hour":155,"alive":true,"profession":"caçador","lod":"active","position":{"map_id":3,"x":7,"y":13},"residence":3,"hp":100,"hunger":78,"thirst":85,"fatigue":22.00000000000001,"money":1,"food":0,"water":0,"local_food":0,"local_water":0,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{"drink_well":157}}. **Observação/relações com o alvo ao final:** {"observation_end":null,"relations_end":[]}. Não usar esse estado posterior como entrada antiga nem atribuir consequências futuras sem vínculo causal.

### 02. career — Bela Solaris #5844, h194: work

**Pressão escolhida:** `advancement` #27568, prioridade 48.338, base 15, fonte `self_assessment:5`, alvo None. Motivo: Acumular uma reserva maior com trabalho e comércio disponíveis.

**Contexto preservado:** {"diagnostic":{"reason":"Selected","competing":null,"turn":194}}.

**Entrada:** {"id":5844,"name":"Bela Solaris","hour":194,"alive":true,"profession":"guarda","lod":"local","position":{"map_id":1135,"x":2,"y":2},"residence":1135,"hp":100,"hunger":40,"thirst":28,"fatigue":39.60000000000005,"money":37,"food":1,"water":0,"local_food":94,"local_water":158,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{}}.

**Personalidade:** {"honesty":78,"compassion":48,"courage":45,"independence":45,"greed":61,"diligence":60,"family_loyalty":51,"persistence":51,"temperament":69,"vengefulness":67,"ambition":94,"sadism":5}. **Emoções escalares de entrada:** {"anger":0.0,"resentment":0.0,"humiliation":0.0,"desperation":0.0,"last_updated":191,"last_support":-10000,"strain":0,"adaptation":0,"last_adapted":0,"stable_material_hours":0,"nested_collections":"LACUNA: cópia rasa; histórico não utilizado"}.

**Conhecimento/locais de entrada:** {"known_places":{"market":{"map_id":1135,"x":3,"y":5},"home":{"map_id":1135,"x":2,"y":2},"work":{"map_id":1135,"x":3,"y":5},"forage":{"map_id":1135,"x":1,"y":5},"well_home":{"map_id":1135,"x":2,"y":2},"well_rural":{"map_id":1135,"x":1,"y":5},"sacred":{"map_id":1135,"x":3,"y":1}},"known_towns":[1135,1088,864],"route_knowledge_count":2,"knowledge_ids_before":[207796,208856,208857,210967,210970,210972,116682,212140,214188,214191,214193,215284,217483,193897,217739,217742,219860,219861,219862,219863,221071,221075,221079,221273,221274,222407,222405,222412,222414,222601,223682,223685,223688,225013,175594,225091,228977,232224,232228,232230,232231,212141,233259,233261,235270,235272,235274,238417,238607,238608,238610,241892,245143,245144,136612,248800,248802,248804,248810,248814,248816,249033,250115,254117],"market_observation":{"turn":170,"town_id":1135,"stock":{"food":100,"grain":88,"water":157,"iron":64,"wood":120},"temporary_work":false,"offers_expire_at":194,"training_offer":null,"price":2,"price_turn":170}}.

**Fatos-fonte retidos após percepção:** [].

| Need | ID/alvo | Base→prioridade | Estado/fonte |
| --- | --- | --- | --- |
| advancement | 27568/None | 15→48.338 | selected / self_assessment:5 |
| rest | 42789/None | 39.60000000000005→40.050000000000054 | active / physiology |
| food | 42787/None | 40.0→40.0 | active / physiology |
| food_reserve | 27567/None | 37.0→38.693333333333335 | active / food_reserve |
| water | 42788/None | 28→28.0 | active / physiology |

**Alternativas/gates realmente vistos:**

Need #27568 (`advancement`): 1 Solutions entraram em _evaluate; 1 saíram disponíveis. Entrada: `work`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| work | {"target":null,"destination":{"map_id":1135,"x":3,"y":5}} | 72.0 | {"base":0.25,"diligence":0.15,"physical_depletion":0.0,"travel":-0.04} | {"feeding":null,"action_pressure":null} |

**Escolhas intermediárias:** [{"chosen":{"action":"work","score":72.0,"target":null,"destination":{"map_id":1135,"x":3,"y":5},"terms":{"base":0.25,"diligence":0.15,"physical_depletion":0.0,"travel":-0.04},"feeding":null,"action_pressure":null},"near_scores":[72.0],"variation_draws":"não capturados; RNG não consultado pelo observador"}].

**Preparação/substituição posterior:** [].

**Winner final / Goal:** {"winner":{"action":"work","score":72.0,"target":null,"destination":{"map_id":1135,"x":3,"y":5},"terms":{"base":0.25,"diligence":0.15,"physical_depletion":0.0,"travel":-0.04},"feeding":null,"action_pressure":null},"goal":{"id":256341,"need_id":27568,"action":"work","score":72.0,"created_at":194,"target_id":null,"destination":{"map_id":1135,"x":3,"y":5},"status":"active","outcome":""},"suspended_before":null,"suspended_after":null}.

**Por que outras Needs não foram executadas:** a fila prioriza emergência/priority/ID e para na primeira solucionável, sujeita à continuidade/preparo. Outras pressões retidas: rest#42789(40.050000000000054), food#42787(40.0), food_reserve#27567(38.693333333333335), water#42788(28.0). Não atribuir score global entre Needs.

**Execução:** execute não foi chamado neste trace. A Goal pode ter iniciado/continuado deslocamento; o snapshot e a posição posterior delimitam essa conclusão.

**Cálculos especializados reais:** [].

**Evento:** nenhum evento retido durante esta decisão. Isso pode significar movimento/efeito sem evento; não implica falha.

**Aprendizado aceito durante a decisão (amostra):** [].

**Recibos posteriores ligados ao mesmo event_id:** []. Contagem é operações de aprendizado aceitas, não indivíduos únicos.

**Consequência imediata:** {"id":5844,"name":"Bela Solaris","hour":194,"alive":true,"profession":"guarda","lod":"local","position":{"map_id":1135,"x":2,"y":5},"residence":1135,"hp":100,"hunger":40,"thirst":28,"fatigue":39.60000000000005,"money":37,"food":1,"water":0,"local_food":94,"local_water":158,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{}}. **Observação/relações com o alvo ao final:** {"observation_end":null,"relations_end":[]}. Não usar esse estado posterior como entrada antiga nem atribuir consequências futuras sem vínculo causal.

### 03. combat — Mira Hammer #4302, h233: denounce

**Pressão escolhida:** `protection` #15665, prioridade 0, base 45, fonte `event:290332`, alvo 4302. Motivo: Crime conhecido ameaça segurança pessoal/familiar.

**Contexto preservado:** {"source_event":290332,"threat":4426,"known_location":{"map_id":760,"x":5,"y":9},"diagnostic":{"reason":"Satisfied","competing":null,"turn":233}}.

**Entrada:** {"id":4302,"name":"Mira Hammer","hour":233,"alive":true,"profession":"cozinheiro","lod":"local","position":{"map_id":760,"x":1,"y":9},"residence":760,"hp":100,"hunger":60,"thirst":61,"fatigue":74.8000000000002,"money":2,"food":0,"water":0,"local_food":8,"local_water":119,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{}}.

**Personalidade:** {"honesty":83,"compassion":11,"courage":46,"independence":56,"greed":18,"diligence":8,"family_loyalty":75,"persistence":79,"temperament":78,"vengefulness":81,"ambition":87,"sadism":0}. **Emoções escalares de entrada:** {"anger":98.92000000000004,"resentment":81.86000000000006,"humiliation":62.89999999999998,"desperation":7.3000000000000025,"last_updated":231,"last_support":47,"strain":10.5695,"adaptation":0,"last_adapted":0,"stable_material_hours":0,"nested_collections":"LACUNA: cópia rasa; histórico não utilizado"}.

**Conhecimento/locais de entrada:** {"known_places":{"market":{"map_id":760,"x":5,"y":9},"home":{"map_id":760,"x":2,"y":2},"work":{"map_id":760,"x":5,"y":9},"forage":{"map_id":760,"x":1,"y":9},"well_home":{"map_id":760,"x":2,"y":2},"well_rural":{"map_id":760,"x":1,"y":9},"sacred":{"map_id":760,"x":5,"y":1}},"known_towns":[760,601,3],"route_knowledge_count":2,"knowledge_ids_before":[252903,253738,253742,253748,253751,253761,254234,255011,255014,255023,256027,256029,256033,256035,256047,256053,257122,257125,257127,257137,257149,257154,257522,258128,258130,258131,258132,258133,246085,223389,268718,268719,268720,268721,268723,268744,268747,258146,275847,275849,279431,188252,189567,282812,290306,290315,290320,290323,290324,290325,290332,291351,291352,291353,294321,294327,294334,294699,295327,295338,295714,296347,297434,297879],"market_observation":{"turn":231,"town_id":760,"stock":{"food":9,"grain":64,"water":129,"iron":120,"wood":120},"temporary_work":true,"offers_expire_at":255,"training_offer":null,"price":6,"price_turn":226}}.

**Fatos-fonte retidos após percepção:** [{"event_id":290332,"kind":"ItemStolen","actor_id":4426,"target_id":760,"location":{"map_id":760,"x":5,"y":9},"turn":225,"description":"Iria Solaris roubou comida no mercado de Dormar.","confidence":100,"required_trust":0,"source_id":null,"source_kind":"direct","context":{"item_id":290331,"item_kind":"food"}}].

| Need | ID/alvo | Base→prioridade | Estado/fonte |
| --- | --- | --- | --- |
| protection | 15665/4302 | 45→84.00797056603776 | active / event:290332 |
| rest | 37008/None | 74.8000000000002→82.8000000000002 | active / physiology |
| revenge | 93364/4426 | 30.0→76.81779272237199 | active / event:290332 |
| food | 21928/None | 70.0→74.5 | active / physiology |
| food_reserve | 21927/None | 41.0→72.72277227722772 | active / food_reserve |
| family | 79080/4305 | 46.0→70.5968 | active / event:252220 |
| water | 42297/None | 61→69 | active / physiology |
| status | 21932/None | 26.885999999999996→68.70513759999999 | active / aspiration:recognition |
| political_pressure | 21936/None | 51.425→64.5770019047619 | active / own_shared_problem |
| migration | 21930/601 | 52→61.9856 | active / known_towns |
| money | 207517/None | 49.375→59.583 | active / economy |
| organizational_survival | 47016/4371 | 41.831→52.985462000000005 | active / group:21992 |
| recognition | 21937/760 | 39.400000000000006→48.07200000000001 | active / political_aspiration |
| advancement | 21929/None | 15→45.0476 | active / self_assessment:2 |
| work | 31893/None | 35→37.95 | active / profession |
| religious_interest | 21935/5908 | 29.75→31.1458 | active / own_faith |

**Alternativas/gates realmente vistos:**

Need #15665 (`protection`): 8 Solutions entraram em _evaluate; 8 saíram disponíveis. Entrada: `denounce, denounce, denounce, denounce, denounce, denounce, avoid_threat, pursue`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| denounce | {"target":783,"destination":{"map_id":760,"x":1,"y":9}} | 99.65 | {"base":0.225,"honesty":0.14525,"vengefulness":0.08100000000000002,"courage":0.0345,"trust":0.0125,"travel":-0.0,"no_progress":0.0} | {"feeding":null,"action_pressure":null} |
| denounce | {"target":4385,"destination":{"map_id":760,"x":1,"y":9}} | 99.65 | {"base":0.225,"honesty":0.14525,"vengefulness":0.08100000000000002,"courage":0.0345,"trust":0.0125,"travel":-0.0,"no_progress":0.0} | {"feeding":null,"action_pressure":null} |
| denounce | {"target":4431,"destination":{"map_id":760,"x":1,"y":9}} | 99.65 | {"base":0.225,"honesty":0.14525,"vengefulness":0.08100000000000002,"courage":0.0345,"trust":0.0125,"travel":-0.0,"no_progress":0.0} | {"feeding":null,"action_pressure":null} |
| denounce | {"target":4339,"destination":{"map_id":760,"x":5,"y":9}} | 91.64999999999999 | {"base":0.225,"honesty":0.14525,"vengefulness":0.08100000000000002,"courage":0.0345,"trust":0.0125,"travel":-0.04,"no_progress":0.0} | {"feeding":null,"action_pressure":null} |
| denounce | {"target":4362,"destination":{"map_id":760,"x":5,"y":9}} | 91.64999999999999 | {"base":0.225,"honesty":0.14525,"vengefulness":0.08100000000000002,"courage":0.0345,"trust":0.0125,"travel":-0.04,"no_progress":0.0} | {"feeding":null,"action_pressure":null} |
| denounce | {"target":4408,"destination":{"map_id":760,"x":2,"y":2}} | 83.65 | {"base":0.225,"honesty":0.14525,"vengefulness":0.08100000000000002,"courage":0.0345,"trust":0.0125,"travel":-0.08,"no_progress":0.0} | {"feeding":null,"action_pressure":null} |
| pursue | {"target":4426,"destination":{"map_id":760,"x":5,"y":9}} | 80.93395026189155 | {"base":0.275,"courage":0.046000000000000006,"diligence":0.006,"vengefulness":0.08100000000000002,"critical_depletion":0.0,"travel":-0.04,"action_pressure":0.0,"no_progress":0.0,"pressure_risk_tolerance":0.036669751309457696} | {"feeding":null,"action_pressure":{"eligible":true,"world_pressure":0,"action_pressure":0.0,"eligibility_causes":[],"source_facts":[],"capacity":50.13,"perceived_capacity":48.53,"major_barriers":[],"selected_alternative":"pursue"}} |
| avoid_threat | {"target":null,"destination":{"map_id":760,"x":2,"y":2}} | -8.950000000000005 | {"base":0.2,"courage":-0.09200000000000001,"compassion":0.00825,"vengefulness":-0.08100000000000002,"travel":-0.08,"no_progress":0.0} | {"feeding":null,"action_pressure":null} |

Need #93364 (`revenge`): 9 Solutions entraram em _evaluate; 9 saíram disponíveis. Entrada: `investigate, denounce, denounce, denounce, denounce, denounce, denounce, avoid_threat, pursue`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| investigate | {"target":4426,"destination":{"map_id":760,"x":5,"y":9}} | 111.30000000000003 | {"base":0.225,"vengefulness":0.16200000000000003,"courage":0.09200000000000001,"independence":0.084,"compassion":-0.0055000000000000005,"temperament":0.03900000000000001,"travel":-0.04} | {"feeding":null,"action_pressure":null} |
| denounce | {"target":783,"destination":{"map_id":760,"x":1,"y":9}} | 99.65 | {"base":0.225,"honesty":0.14525,"vengefulness":0.08100000000000002,"courage":0.0345,"trust":0.0125,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| denounce | {"target":4385,"destination":{"map_id":760,"x":1,"y":9}} | 99.65 | {"base":0.225,"honesty":0.14525,"vengefulness":0.08100000000000002,"courage":0.0345,"trust":0.0125,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| denounce | {"target":4431,"destination":{"map_id":760,"x":1,"y":9}} | 99.65 | {"base":0.225,"honesty":0.14525,"vengefulness":0.08100000000000002,"courage":0.0345,"trust":0.0125,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| denounce | {"target":4339,"destination":{"map_id":760,"x":5,"y":9}} | 91.64999999999999 | {"base":0.225,"honesty":0.14525,"vengefulness":0.08100000000000002,"courage":0.0345,"trust":0.0125,"travel":-0.04} | {"feeding":null,"action_pressure":null} |
| denounce | {"target":4362,"destination":{"map_id":760,"x":5,"y":9}} | 91.64999999999999 | {"base":0.225,"honesty":0.14525,"vengefulness":0.08100000000000002,"courage":0.0345,"trust":0.0125,"travel":-0.04} | {"feeding":null,"action_pressure":null} |
| denounce | {"target":4408,"destination":{"map_id":760,"x":2,"y":2}} | 83.65 | {"base":0.225,"honesty":0.14525,"vengefulness":0.08100000000000002,"courage":0.0345,"trust":0.0125,"travel":-0.08} | {"feeding":null,"action_pressure":null} |
| pursue | {"target":4426,"destination":{"map_id":760,"x":5,"y":9}} | 77.37298442399779 | {"base":0.275,"courage":0.046000000000000006,"diligence":0.006,"vengefulness":0.08100000000000002,"critical_depletion":0.0,"travel":-0.04,"action_pressure":0.0,"pressure_risk_tolerance":0.018864922119988883} | {"feeding":null,"action_pressure":{"eligible":true,"world_pressure":0,"action_pressure":0.0,"eligibility_causes":[],"source_facts":[],"capacity":50.13,"perceived_capacity":48.53,"major_barriers":[],"selected_alternative":"pursue"}} |
| avoid_threat | {"target":null,"destination":{"map_id":760,"x":2,"y":2}} | -8.950000000000005 | {"base":0.2,"courage":-0.09200000000000001,"compassion":0.00825,"vengefulness":-0.08100000000000002,"travel":-0.08} | {"feeding":null,"action_pressure":null} |

Need #79080 (`family`): 1 Solutions entraram em _evaluate; 1 saíram disponíveis. Entrada: `check_relative`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| check_relative | {"target":4305,"destination":{"map_id":760,"x":5,"y":9}} | 79.75000000000001 | {"base":0.275,"independence":0.07,"family_loyalty":0.09375,"travel":-0.04} | {"feeding":null,"action_pressure":null} |

Need #21932 (`status`): 2 Solutions entraram em _evaluate; 2 saíram disponíveis. Entrada: `work, work_for_food`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| work_for_food | {"target":null,"destination":{"map_id":760,"x":1,"y":9}} | 47.0 | {"base":0.225,"diligence":0.01,"physical_depletion":0.0,"travel":-0.0,"no_progress":0.0} | {"feeding":null,"action_pressure":null} |
| work | {"target":null,"destination":{"map_id":760,"x":5,"y":9}} | 46.0 | {"base":0.25,"diligence":0.02,"physical_depletion":0.0,"travel":-0.04,"no_progress":0.0} | {"feeding":null,"action_pressure":null} |

Need #21929 (`advancement`): 2 Solutions entraram em _evaluate; 2 saíram disponíveis. Entrada: `work, work_for_food`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| work_for_food | {"target":null,"destination":{"map_id":760,"x":1,"y":9}} | 47.0 | {"base":0.225,"diligence":0.01,"physical_depletion":0.0,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| work | {"target":null,"destination":{"map_id":760,"x":5,"y":9}} | 46.0 | {"base":0.25,"diligence":0.02,"physical_depletion":0.0,"travel":-0.04} | {"feeding":null,"action_pressure":null} |

**Escolhas intermediárias:** [{"chosen":{"action":"denounce","score":99.65,"target":4431,"destination":{"map_id":760,"x":1,"y":9},"terms":{"base":0.225,"honesty":0.14525,"vengefulness":0.08100000000000002,"courage":0.0345,"trust":0.0125,"travel":-0.0,"no_progress":0.0},"feeding":null,"action_pressure":null},"near_scores":[99.65,99.65,99.65,91.64999999999999,91.64999999999999,83.65,80.93395026189155,-8.950000000000005],"variation_draws":"não capturados; RNG não consultado pelo observador"}].

**Preparação/substituição posterior:** [].

**Winner final / Goal:** {"winner":{"action":"denounce","score":99.65,"target":4431,"destination":{"map_id":760,"x":1,"y":9},"terms":{"base":0.225,"honesty":0.14525,"vengefulness":0.08100000000000002,"courage":0.0345,"trust":0.0125,"travel":-0.0,"no_progress":0.0},"feeding":null,"action_pressure":null},"goal":{"id":298571,"need_id":15665,"action":"denounce","score":99.65,"created_at":233,"target_id":4431,"destination":{"map_id":760,"x":1,"y":9},"status":"completed","outcome":"Informação transmitida."},"suspended_before":null,"suspended_after":null}.

**Por que outras Needs não foram executadas:** a fila prioriza emergência/priority/ID e para na primeira solucionável, sujeita à continuidade/preparo. Outras pressões retidas: rest#37008(82.8000000000002), revenge#93364(76.81779272237199), food#21928(74.5), food_reserve#21927(72.72277227722772), family#79080(70.5968), water#42297(69), status#21932(68.70513759999999), political_pressure#21936(64.5770019047619), migration#21930(61.9856), money#207517(59.583), organizational_survival#47016(52.985462000000005), recognition#21937(48.07200000000001), advancement#21929(45.0476), work#31893(37.95), religious_interest#21935(31.1458). Não atribuir score global entre Needs.

**Execução:** {"success":true,"result":[true,"Informação transmitida."],"goal_at_entry":{"id":298571,"need_id":15665,"action":"denounce","score":99.65,"created_at":233,"target_id":4431,"destination":{"map_id":760,"x":1,"y":9},"status":"active","outcome":""},"before":{"id":4302,"name":"Mira Hammer","hour":233,"alive":true,"profession":"cozinheiro","lod":"local","position":{"map_id":760,"x":1,"y":9},"residence":760,"hp":100,"hunger":60,"thirst":61,"fatigue":74.8000000000002,"money":2,"food":0,"water":0,"local_food":8,"local_water":119,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{}},"after":{"id":4302,"name":"Mira Hammer","hour":233,"alive":true,"profession":"cozinheiro","lod":"local","position":{"map_id":760,"x":1,"y":9},"residence":760,"hp":100,"hunger":60,"thirst":61,"fatigue":74.8000000000002,"money":2,"food":0,"water":0,"local_food":8,"local_water":119,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{}}}.

**Cálculos especializados reais:** [{"system":"lethal_decision","function":"lethal_decisions.LethalDecisionSystem.evaluate","result":{"available":false,"pressure":-41.34,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":291350,"motive":"protection","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":13.770000000000001,"directed_emotion":3.9160000000000017,"commitment":6.4416384905660395,"sadism":0.0,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":6.050000000000001,"moral_restraint":9.959999999999999,"fear":0.0,"risk":4.452830188679245,"bond":0.0,"authority_or_witnesses":15,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":53.680320754716995,"commitment_intensity":53.680320754716995},"inputs":{"pressure":-41.34,"cause":{"severity":0,"grave":false,"causes":[],"facts":[],"confidence":0,"mode":"retributive","confirmed_injury":0}}},{"system":"lethal_decision","function":"lethal_decisions.LethalDecisionSystem.evaluate","result":{"available":false,"pressure":-41.34,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":291350,"motive":"protection","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":13.770000000000001,"directed_emotion":3.9160000000000017,"commitment":6.4416384905660395,"sadism":0.0,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":6.050000000000001,"moral_restraint":9.959999999999999,"fear":0.0,"risk":4.452830188679245,"bond":0.0,"authority_or_witnesses":15,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":53.680320754716995,"commitment_intensity":53.680320754716995},"inputs":{"pressure":-41.34,"cause":{"severity":0,"grave":false,"causes":[],"facts":[],"confidence":0,"mode":"retributive","confirmed_injury":0}}},{"system":"lethal_pressure","function":"lethality.LethalPressure.evaluate","result":{"available":false,"pressure":-41.34,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":291350,"motive":"protection","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":13.770000000000001,"directed_emotion":3.9160000000000017,"commitment":6.4416384905660395,"sadism":0.0,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":6.050000000000001,"moral_restraint":9.959999999999999,"fear":0.0,"risk":4.452830188679245,"bond":0.0,"authority_or_witnesses":15,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":53.680320754716995,"commitment_intensity":53.680320754716995},"inputs":{}},{"system":"lethal_decision","function":"lethal_decisions.LethalDecisionSystem.evaluate","result":{"available":false,"pressure":-47.78,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"revenge","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":13.770000000000001,"directed_emotion":3.9160000000000017,"commitment":0.0,"sadism":0.0,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":6.050000000000001,"moral_restraint":9.959999999999999,"fear":0.0,"risk":4.452830188679245,"bond":0.0,"authority_or_witnesses":15,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{"pressure":-47.78,"cause":{"severity":0,"grave":false,"causes":[],"facts":[],"confidence":0,"mode":"retributive","confirmed_injury":0}}},{"system":"lethal_decision","function":"lethal_decisions.LethalDecisionSystem.evaluate","result":{"available":false,"pressure":-47.78,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"revenge","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":13.770000000000001,"directed_emotion":3.9160000000000017,"commitment":0.0,"sadism":0.0,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":6.050000000000001,"moral_restraint":9.959999999999999,"fear":0.0,"risk":4.452830188679245,"bond":0.0,"authority_or_witnesses":15,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{"pressure":-47.78,"cause":{"severity":0,"grave":false,"causes":[],"facts":[],"confidence":0,"mode":"retributive","confirmed_injury":0}}},{"system":"lethal_pressure","function":"lethality.LethalPressure.evaluate","result":{"available":false,"pressure":-47.78,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"revenge","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":13.770000000000001,"directed_emotion":3.9160000000000017,"commitment":0.0,"sadism":0.0,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":6.050000000000001,"moral_restraint":9.959999999999999,"fear":0.0,"risk":4.452830188679245,"bond":0.0,"authority_or_witnesses":15,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{}},{"system":"capacity","function":"action_pressure.ActionPressureSystem.assess","result":{"eligible":true,"world_pressure":0,"action_pressure":0.0,"eligibility_causes":[],"source_facts":[],"capacity":50.13,"perceived_capacity":48.53,"major_barriers":[],"selected_alternative":"pursue"},"inputs":{}},{"system":"capacity","function":"action_pressure.ActionPressureSystem.assess","result":{"eligible":true,"world_pressure":0,"action_pressure":0.0,"eligibility_causes":[],"source_facts":[],"capacity":50.13,"perceived_capacity":48.53,"major_barriers":[],"selected_alternative":"pursue"},"inputs":{}}].

| Evento/hora | Actor→target | Emissor | Testemunhas | Contexto |
| --- | --- | --- | --- | --- |
| 298570 / 233 / CommitmentResumed | 4302→None | ["agency.AgencySystem.event","agency.AgencySystem.selected","goals.GoalSystem.decide"] | [4302] | {"competing":"protection","commitment_id":291350,"need_id":15665,"origin":"protection","source_fact":290332,"target":4302,"progress":0} |
| 298572 / 233 / InformationShared | 4302→4431 | ["personal_actions.PersonalActions.inform","personal_actions.PersonalActions.execute","goals.GoalSystem._execute"] | [766,772,783,4302,4331,4365,4385,4388,4423,4431] | {"fact_id":290332,"utility":"new_useful"} |
| 298573 / 233 / ThreatReported | 4302→4431 | ["personal_actions.PersonalActions.execute","goals.GoalSystem._execute","goals.GoalSystem.execute"] | [766,772,783,4302,4331,4365,4385,4388,4423,4431] | {"fact_id":290332} |
| 298574 / 233 / CommitmentProgress | 4302→None | ["agency.AgencySystem.event","agency.AgencySystem.outcome","goals.GoalSystem.execute"] | [4302] | {"changes":["report","resolution"],"action":"denounce","commitment_id":291350,"need_id":15665,"origin":"protection","source_fact":290332,"target":4302,"progress":1} |
| 298575 / 233 / CommitmentCompleted | 4302→None | ["agency.AgencySystem.event","agency.AgencySystem.close","agency.AgencySystem.outcome"] | [4302] | {"reason":"verified_need_resolution","duration":7,"activity":1,"meaningful_progress":1,"strategy_changes":0,"commitment_id":291350,"need_id":15665,"origin":"protection","source_fact":290332,"target":4302,"progress":1} |

**Aprendizado aceito durante a decisão (amostra):** [{"npc":4302,"event":298570,"kind":"CommitmentResumed","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":4431,"event":290332,"kind":"ItemStolen","source":4302,"firsthand":false,"confidence":30,"latency":8},{"npc":766,"event":298572,"kind":"InformationShared","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":772,"event":298572,"kind":"InformationShared","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":783,"event":298572,"kind":"InformationShared","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":4302,"event":298572,"kind":"InformationShared","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":4331,"event":298572,"kind":"InformationShared","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":4365,"event":298572,"kind":"InformationShared","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":4385,"event":298572,"kind":"InformationShared","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":4388,"event":298572,"kind":"InformationShared","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":4423,"event":298572,"kind":"InformationShared","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":4431,"event":298572,"kind":"InformationShared","source":null,"firsthand":true,"confidence":100,"latency":0}].

**Recibos posteriores ligados ao mesmo event_id:** [{"event":298570,"kind":"CommitmentResumed","learned":{"count":1,"first":233,"last":233,"first_people":[4302]}},{"event":298572,"kind":"InformationShared","learned":{"count":13,"first":233,"last":300,"first_people":[766,772,783,4302,4331,4365]}},{"event":298573,"kind":"ThreatReported","learned":{"count":10,"first":233,"last":233,"first_people":[766,772,783,4302,4331,4365]}},{"event":298574,"kind":"CommitmentProgress","learned":{"count":1,"first":233,"last":233,"first_people":[4302]}},{"event":298575,"kind":"CommitmentCompleted","learned":{"count":1,"first":233,"last":233,"first_people":[4302]}}]. Contagem é operações de aprendizado aceitas, não indivíduos únicos.

**Consequência imediata:** {"id":4302,"name":"Mira Hammer","hour":233,"alive":true,"profession":"cozinheiro","lod":"local","position":{"map_id":760,"x":1,"y":9},"residence":760,"hp":100,"hunger":60,"thirst":61,"fatigue":74.8000000000002,"money":2,"food":0,"water":0,"local_food":8,"local_water":119,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{}}. **Observação/relações com o alvo ao final:** {"observation_end":{"turn":233,"position":{"map_id":760,"x":1,"y":9},"hunger":62,"thirst":16,"health":100,"alive":true,"profession":"guarda","weapon_power":10,"injured":0},"relations_end":[]}. Não usar esse estado posterior como entrada antiga nem atribuir consequências futuras sem vínculo causal.

### 04. crime — Cael Hammer #497, h259: steal_person

**Pressão escolhida:** `food` #16704, prioridade 100, base 100, fonte `physiology`, alvo None. Motivo: Fome.

**Contexto preservado:** {"emergency":true}.

**Entrada:** {"id":497,"name":"Cael Hammer","hour":259,"alive":true,"profession":"lenhador","lod":"active","position":{"map_id":479,"x":2,"y":2},"residence":479,"hp":100,"hunger":81,"thirst":68,"fatigue":70.00000000000021,"money":0,"food":0,"water":0,"local_food":21,"local_water":107,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{}}.

**Personalidade:** {"honesty":32,"compassion":78,"courage":78,"independence":92,"greed":56,"diligence":10,"family_loyalty":56,"persistence":44,"temperament":12,"vengefulness":48,"ambition":36,"sadism":0}. **Emoções escalares de entrada:** {"anger":0.0,"resentment":0.0,"humiliation":0.0,"desperation":45.30000000000008,"last_updated":256,"last_support":-10000,"strain":108.62799999999999,"adaptation":0,"last_adapted":0,"stable_material_hours":0,"nested_collections":"LACUNA: cópia rasa; histórico não utilizado"}.

**Conhecimento/locais de entrada:** {"known_places":{"market":{"map_id":479,"x":5,"y":9},"home":{"map_id":479,"x":2,"y":2},"work":{"map_id":479,"x":8,"y":2},"forage":{"map_id":479,"x":1,"y":9},"well_home":{"map_id":479,"x":2,"y":2},"well_rural":{"map_id":479,"x":1,"y":9},"sacred":{"map_id":479,"x":5,"y":1}},"known_towns":[479,302],"route_knowledge_count":2,"knowledge_ids_before":[234759,235765,167324,234372,247121,247122,242315,252730,260512,260962,261475,263026,263027,263634,263635,256920,275530,276817,276840,276865,276866,276867,278075,278076,278086,278105,278116,279170,279177,279230,267512,228425,254205,280501,280536,249538,254765,286909,287506,287981,288591,288994,288997,290070,300724,302923,303513,308758,309245,309806,309809,310251,310256,310257,310809,311249,311279,284807,312434,286904,265138,322798,322800,285839],"market_observation":{"turn":247,"town_id":479,"stock":{"food":18,"grain":32,"water":153,"iron":120,"wood":120},"temporary_work":true,"offers_expire_at":271,"training_offer":null,"price":2,"price_turn":61}}.

**Fatos-fonte retidos após percepção:** [].

| Need | ID/alvo | Base→prioridade | Estado/fonte |
| --- | --- | --- | --- |
| food | 16704/None | 100→100 | active / physiology |
| rest | 44683/None | 70.00000000000021→78.00000000000021 | active / physiology |
| money | 16705/None | 63.75→77.47000000000001 | active / economy |
| water | 44682/None | 68→76 | active / physiology |
| political_pressure | 34297/None | 57.15→73.29286761904763 | active / own_shared_problem |
| food_reserve | 16703/None | 41.0→73.07272727272728 | active / food_reserve |
| organizational_survival | 44684/3237 | 41.3305→54.66038851428572 | active / group:27751 |
| migration | 34296/302 | 35→47.39237142857144 | active / known_towns |
| advancement | 16707/None | 21.252→42.177203199999994 | active / aspiration:wealth |

**Alternativas/gates realmente vistos:**

Need #16704 (`food`): 4 Solutions entraram em _evaluate; 4 saíram disponíveis. Entrada: `steal, forage, work_for_food, steal_person`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| steal_person | {"target":3212,"destination":null} | 74.82791159183674 | {"base":0.31,"greed":0.11200000000000002,"honesty":-0.14400000000000002,"authority":-0.0,"courage":0.03900000000000001,"travel":-0.0,"pressure_moral_tolerance":0.0571395579591837} | {"feeding":{"EstimatedTimeUntilFoodConsumed":2,"EstimatedSurvivalMargin":43,"economically_viable":true,"survival_viable":true,"reason":null,"known_conditions":["UnknownPrice","DistantProduct"]},"action_pressure":null} |
| forage | {"target":null,"destination":{"map_id":479,"x":1,"y":9}} | 65.0 | {"base":0.175,"independence":0.23,"hunter":0.0,"travel":-0.08} | {"feeding":{"EstimatedTimeUntilFoodConsumed":10,"EstimatedSurvivalMargin":43,"economically_viable":true,"survival_viable":true,"reason":null,"known_conditions":["UnknownPrice","DistantProduct"]},"action_pressure":null} |
| steal | {"target":null,"destination":{"map_id":479,"x":5,"y":9}} | 55.89457825850341 | {"base":0.35,"greed":0.09333333333333335,"honesty":-0.16,"courage":0.03900000000000001,"travel":-0.1,"pressure_moral_tolerance":0.0571395579591837} | {"feeding":{"EstimatedTimeUntilFoodConsumed":12,"EstimatedSurvivalMargin":43,"economically_viable":true,"survival_viable":true,"reason":null,"known_conditions":["UnknownPrice","DistantProduct"]},"action_pressure":null} |
| work_for_food | {"target":null,"destination":{"map_id":479,"x":1,"y":9}} | 31.5 | {"base":0.225,"diligence":0.0125,"physical_depletion":0.0,"travel":-0.08} | {"feeding":{"EstimatedTimeUntilFoodConsumed":10,"EstimatedSurvivalMargin":43,"economically_viable":true,"survival_viable":true,"reason":null,"known_conditions":["UnknownPrice","DistantProduct"]},"action_pressure":null} |

Need #16707 (`advancement`): 2 Solutions entraram em _evaluate; 2 saíram disponíveis. Entrada: `work_for_food, steal_person`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| steal_person | {"target":3212,"destination":null} | 75.802211328 | {"base":0.31,"greed":0.11200000000000002,"honesty":-0.14400000000000002,"authority":-0.0,"courage":0.03900000000000001,"travel":-0.0,"no_progress":0.0,"pressure_moral_tolerance":0.062011056640000006} | {"feeding":null,"action_pressure":null} |
| work_for_food | {"target":null,"destination":{"map_id":479,"x":1,"y":9}} | 31.5 | {"base":0.225,"diligence":0.0125,"physical_depletion":0.0,"travel":-0.08,"no_progress":0.0} | {"feeding":null,"action_pressure":null} |

**Escolhas intermediárias:** [{"chosen":{"action":"steal_person","score":74.82791159183674,"target":3212,"destination":null,"terms":{"base":0.31,"greed":0.11200000000000002,"honesty":-0.14400000000000002,"authority":-0.0,"courage":0.03900000000000001,"travel":-0.0,"pressure_moral_tolerance":0.0571395579591837},"feeding":{"EstimatedTimeUntilFoodConsumed":2,"EstimatedSurvivalMargin":43,"economically_viable":true,"survival_viable":true,"reason":null,"known_conditions":["UnknownPrice","DistantProduct"]},"action_pressure":null},"near_scores":[74.82791159183674,65.0,55.89457825850341,31.5],"variation_draws":"não capturados; RNG não consultado pelo observador"}].

**Preparação/substituição posterior:** [].

**Winner final / Goal:** {"winner":{"action":"steal_person","score":74.82791159183674,"target":3212,"destination":null,"terms":{"base":0.31,"greed":0.11200000000000002,"honesty":-0.14400000000000002,"authority":-0.0,"courage":0.03900000000000001,"travel":-0.0,"pressure_moral_tolerance":0.0571395579591837},"feeding":{"EstimatedTimeUntilFoodConsumed":2,"EstimatedSurvivalMargin":43,"economically_viable":true,"survival_viable":true,"reason":null,"known_conditions":["UnknownPrice","DistantProduct"]},"action_pressure":null},"goal":{"id":325298,"need_id":16704,"action":"steal_person","score":74.82791159183674,"created_at":259,"target_id":3212,"destination":null,"status":"failed","outcome":"Não havia provisão acessível no alvo."},"suspended_before":null,"suspended_after":null}.

**Por que outras Needs não foram executadas:** a fila prioriza emergência/priority/ID e para na primeira solucionável, sujeita à continuidade/preparo. Outras pressões retidas: rest#44683(78.00000000000021), money#16705(77.47000000000001), water#44682(76), political_pressure#34297(73.29286761904763), food_reserve#16703(73.07272727272728), organizational_survival#44684(54.66038851428572), migration#34296(47.39237142857144), advancement#16707(42.177203199999994). Não atribuir score global entre Needs.

**Execução:** {"success":false,"result":[false,"Não havia provisão acessível no alvo."],"goal_at_entry":{"id":325298,"need_id":16704,"action":"steal_person","score":74.82791159183674,"created_at":259,"target_id":3212,"destination":null,"status":"active","outcome":""},"before":{"id":497,"name":"Cael Hammer","hour":259,"alive":true,"profession":"lenhador","lod":"active","position":{"map_id":479,"x":2,"y":2},"residence":479,"hp":100,"hunger":81,"thirst":68,"fatigue":70.00000000000021,"money":0,"food":0,"water":0,"local_food":21,"local_water":107,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{}},"after":{"id":497,"name":"Cael Hammer","hour":259,"alive":true,"profession":"lenhador","lod":"active","position":{"map_id":479,"x":2,"y":2},"residence":479,"hp":100,"hunger":81,"thirst":68,"fatigue":70.00000000000021,"money":0,"food":0,"water":0,"local_food":21,"local_water":107,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{}}}.

**Cálculos especializados reais:** [].

**Evento:** nenhum evento retido durante esta decisão. Isso pode significar movimento/efeito sem evento; não implica falha.

**Aprendizado aceito durante a decisão (amostra):** [].

**Recibos posteriores ligados ao mesmo event_id:** []. Contagem é operações de aprendizado aceitas, não indivíduos únicos.

**Consequência imediata:** {"id":497,"name":"Cael Hammer","hour":259,"alive":true,"profession":"lenhador","lod":"active","position":{"map_id":479,"x":2,"y":2},"residence":479,"hp":100,"hunger":81,"thirst":68,"fatigue":70.00000000000021,"money":0,"food":0,"water":0,"local_food":21,"local_water":107,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{"steal_person":271}}. **Observação/relações com o alvo ao final:** {"observation_end":{"turn":259,"position":{"map_id":479,"x":2,"y":2},"hunger":84,"thirst":68,"health":62,"alive":true,"profession":"comerciante","weapon_power":4,"injured":0},"relations_end":[]}. Não usar esse estado posterior como entrada antiga nem atribuir consequências futuras sem vínculo causal.

### 05. faction — Aldren Hammer #1173, h128: invite_person

**Pressão escolhida:** `organizational_access` #20146, prioridade 62.0066, base 53, fonte `organization`, alvo 1176. Motivo: Procurar pessoas e recursos para a organização.

**Contexto preservado:** {"faction_id":1176}.

**Entrada:** {"id":1173,"name":"Aldren Hammer","hour":128,"alive":true,"profession":"caçador","lod":"local","position":{"map_id":396,"x":3,"y":5},"residence":302,"hp":100,"hunger":47,"thirst":31,"fatigue":100,"money":1,"food":1,"water":0,"local_food":50,"local_water":150,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{"denounce":131,"steal_person":137}}.

**Personalidade:** {"honesty":12,"compassion":81,"courage":11,"independence":30,"greed":77,"diligence":61,"family_loyalty":64,"persistence":89,"temperament":72,"vengefulness":23,"ambition":49,"sadism":0}. **Emoções escalares de entrada:** {"anger":0.0,"resentment":0.0,"humiliation":0.0,"desperation":11.249999999999996,"last_updated":125,"last_support":40,"strain":26.8875,"adaptation":0,"last_adapted":0,"stable_material_hours":0,"nested_collections":"LACUNA: cópia rasa; histórico não utilizado"}.

**Conhecimento/locais de entrada:** {"known_places":{"home":{"map_id":1170,"x":5,"y":5},"work":{"map_id":1170,"x":5,"y":5},"forage":{"map_id":396,"x":1,"y":5},"sacred":{"map_id":1170,"x":5,"y":1},"market":{"map_id":396,"x":3,"y":5},"well_rural":{"map_id":396,"x":1,"y":5}},"known_towns":[302,396,367],"route_knowledge_count":6,"knowledge_ids_before":[146269,146357,146358,148103,150130,150211,151665,153278,153378,128006,148100,154746,156333,156420,156732,156734,157762,157764,159533,159536,159968,159973,159976,159981,94672,160653,161104,161108,161109,161111,161112,161113,161114,161119,163041,163043,163045,163127,163518,163520,164752,164755,164758,166753,167252,167258,168806,171441,171446,172781,172785,174552,174553,174555,174556,174557,175030,168801,141520,138088,176208,176218,177807,177809],"market_observation":{"turn":125,"town_id":396,"stock":{"food":51,"grain":70,"water":153,"iron":32,"wood":72},"temporary_work":false,"offers_expire_at":149,"training_offer":null,"price":2,"price_turn":125}}.

**Fatos-fonte retidos após percepção:** [{"event_id":159973,"kind":"ItemStolen","actor_id":2910,"target_id":396,"location":{"map_id":396,"x":3,"y":5},"turn":113,"description":"Cael Bruma roubou comida no mercado de Morvia.","confidence":100,"required_trust":0,"source_id":null,"source_kind":"direct","context":{"item_id":159972,"item_kind":"food"}}].

| Need | ID/alvo | Base→prioridade | Estado/fonte |
| --- | --- | --- | --- |
| rest | 44830/None | 100→100 | active / physiology |
| money | 20140/None | 53.25→74.386 | active / economy |
| protection | 63328/1173 | 45→64.5 | blocked / event:159973 |
| organizational_access | 20146/1176 | 53→62.0066 | active / organization |
| migration | 63430/367 | 52→56.986 | active / known_towns |
| organizational_survival | 20144/1173 | 45→53.0 | active / faction:1176 |
| food | 20139/None | 50.5→51.4 | active / physiology |
| advancement | 20142/None | 23.1798→47.35878853714286 | blocked / aspiration:wealth |
| work | 30738/None | 35→47.2 | active / profession |
| religious_interest | 20143/5909 | 32.75→41.8462 | active / own_faith |
| food_reserve | 166839/None | 37.0→38.0 | active / food_reserve |
| water | 39353/None | 31→31.45 | active / physiology |

**Alternativas/gates realmente vistos:**

Need #44830 (`rest`): 1 Solutions entraram em _evaluate; 0 saíram disponíveis. Entrada: `sleep`.

| Opção | Alvo | Etapa | Motivo observado | Auditoria/feeding |
| --- | --- | --- | --- | --- |
| sleep | None | before_Utility_or_unresolved | destination_other_map | {"pressure":null,"feeding":null} |

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |

Need #20140 (`money`): 2 Solutions entraram em _evaluate; 0 saíram disponíveis. Entrada: `steal_person, steal_person`.

| Opção | Alvo | Etapa | Motivo observado | Auditoria/feeding |
| --- | --- | --- | --- | --- |
| steal_person | 2896 | before_Utility_or_unresolved | cooldown_after_failure | {"pressure":null,"feeding":null} |
| steal_person | 2919 | before_Utility_or_unresolved | cooldown_after_failure | {"pressure":null,"feeding":null} |

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |

Need #63328 (`protection`): 4 Solutions entraram em _evaluate; 0 saíram disponíveis. Entrada: `denounce, denounce, denounce, avoid_threat`.

| Opção | Alvo | Etapa | Motivo observado | Auditoria/feeding |
| --- | --- | --- | --- | --- |
| denounce | 408 | before_Utility_or_unresolved | cooldown_after_failure | {"pressure":null,"feeding":null} |
| denounce | 2898 | before_Utility_or_unresolved | cooldown_after_failure | {"pressure":null,"feeding":null} |
| denounce | 2794 | before_Utility_or_unresolved | cooldown_after_failure | {"pressure":null,"feeding":null} |
| avoid_threat | None | before_Utility_or_unresolved | destination_other_map | {"pressure":null,"feeding":null} |

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |

Need #20146 (`organizational_access`): 1 Solutions entraram em _evaluate; 1 saíram disponíveis. Entrada: `invite_person`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| invite_person | {"target":1176,"destination":null} | 55.00000000000001 | {"base":0.275,"travel":-0.0} | {"feeding":null,"action_pressure":null} |

Need #63328 (`protection`): 4 Solutions entraram em _evaluate; 0 saíram disponíveis. Entrada: `denounce, denounce, denounce, avoid_threat`.

| Opção | Alvo | Etapa | Motivo observado | Auditoria/feeding |
| --- | --- | --- | --- | --- |
| denounce | 408 | before_Utility_or_unresolved | cooldown_after_failure | {"pressure":null,"feeding":null} |
| denounce | 2898 | before_Utility_or_unresolved | cooldown_after_failure | {"pressure":null,"feeding":null} |
| denounce | 2794 | before_Utility_or_unresolved | cooldown_after_failure | {"pressure":null,"feeding":null} |
| avoid_threat | None | before_Utility_or_unresolved | destination_other_map | {"pressure":null,"feeding":null} |

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |

Need #20142 (`advancement`): 2 Solutions entraram em _evaluate; 0 saíram disponíveis. Entrada: `steal_person, steal_person`.

| Opção | Alvo | Etapa | Motivo observado | Auditoria/feeding |
| --- | --- | --- | --- | --- |
| steal_person | 2896 | before_Utility_or_unresolved | cooldown_after_failure | {"pressure":null,"feeding":null} |
| steal_person | 2919 | before_Utility_or_unresolved | cooldown_after_failure | {"pressure":null,"feeding":null} |

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |

**Escolhas intermediárias:** [{"chosen":{"action":"invite_person","score":55.00000000000001,"target":1176,"destination":null,"terms":{"base":0.275,"travel":-0.0},"feeding":null,"action_pressure":null},"near_scores":[55.00000000000001],"variation_draws":"não capturados; RNG não consultado pelo observador"}].

**Preparação/substituição posterior:** [].

**Winner final / Goal:** {"winner":{"action":"invite_person","score":55.00000000000001,"target":1176,"destination":null,"terms":{"base":0.275,"travel":-0.0},"feeding":null,"action_pressure":null},"goal":{"id":177892,"need_id":20146,"action":"invite_person","score":55.00000000000001,"created_at":128,"target_id":1176,"destination":null,"status":"failed","outcome":"Nenhum candidato local disponível e coerente."},"suspended_before":null,"suspended_after":null}.

**Por que outras Needs não foram executadas:** a fila prioriza emergência/priority/ID e para na primeira solucionável, sujeita à continuidade/preparo. Outras pressões retidas: rest#44830(100), money#20140(74.386), protection#63328(64.5), migration#63430(56.986), organizational_survival#20144(53.0), food#20139(51.4), advancement#20142(47.35878853714286), work#30738(47.2), religious_interest#20143(41.8462), food_reserve#166839(38.0), water#39353(31.45). Não atribuir score global entre Needs.

**Execução:** {"success":false,"result":[false,"Nenhum candidato local disponível e coerente."],"goal_at_entry":{"id":177892,"need_id":20146,"action":"invite_person","score":55.00000000000001,"created_at":128,"target_id":1176,"destination":null,"status":"active","outcome":""},"before":{"id":1173,"name":"Aldren Hammer","hour":128,"alive":true,"profession":"caçador","lod":"local","position":{"map_id":396,"x":3,"y":5},"residence":302,"hp":100,"hunger":47,"thirst":31,"fatigue":100,"money":1,"food":1,"water":0,"local_food":50,"local_water":150,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{"denounce":131,"steal_person":137}},"after":{"id":1173,"name":"Aldren Hammer","hour":128,"alive":true,"profession":"caçador","lod":"local","position":{"map_id":396,"x":3,"y":5},"residence":302,"hp":100,"hunger":47,"thirst":31,"fatigue":100,"money":1,"food":1,"water":0,"local_food":50,"local_water":150,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{"denounce":131,"steal_person":137}}}.

**Cálculos especializados reais:** [{"system":"lethal_decision","function":"lethal_decisions.LethalDecisionSystem.evaluate","result":{"available":false,"pressure":-74.48,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"protection","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":3.91,"directed_emotion":0.0,"commitment":0.0,"sadism":0.0,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":44.550000000000004,"moral_restraint":1.44,"fear":0.0,"risk":2.4000000000000004,"bond":0.0,"authority_or_witnesses":0.0,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{"pressure":-74.48,"cause":{"severity":0,"grave":false,"causes":[],"facts":[],"confidence":0,"mode":"retributive","confirmed_injury":0}}},{"system":"lethal_decision","function":"lethal_decisions.LethalDecisionSystem.evaluate","result":{"available":false,"pressure":-74.48,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"protection","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":3.91,"directed_emotion":0.0,"commitment":0.0,"sadism":0.0,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":44.550000000000004,"moral_restraint":1.44,"fear":0.0,"risk":2.4000000000000004,"bond":0.0,"authority_or_witnesses":0.0,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{"pressure":-74.48,"cause":{"severity":0,"grave":false,"causes":[],"facts":[],"confidence":0,"mode":"retributive","confirmed_injury":0}}},{"system":"lethal_pressure","function":"lethality.LethalPressure.evaluate","result":{"available":false,"pressure":-74.48,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"protection","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":3.91,"directed_emotion":0.0,"commitment":0.0,"sadism":0.0,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":44.550000000000004,"moral_restraint":1.44,"fear":0.0,"risk":2.4000000000000004,"bond":0.0,"authority_or_witnesses":0.0,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{}}].

**Evento:** nenhum evento retido durante esta decisão. Isso pode significar movimento/efeito sem evento; não implica falha.

**Aprendizado aceito durante a decisão (amostra):** [].

**Recibos posteriores ligados ao mesmo event_id:** []. Contagem é operações de aprendizado aceitas, não indivíduos únicos.

**Consequência imediata:** {"id":1173,"name":"Aldren Hammer","hour":128,"alive":true,"profession":"caçador","lod":"local","position":{"map_id":396,"x":3,"y":5},"residence":302,"hp":100,"hunger":47,"thirst":31,"fatigue":100,"money":1,"food":1,"water":0,"local_food":50,"local_water":150,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{"denounce":131,"steal_person":137,"invite_person":140}}. **Observação/relações com o alvo ao final:** {"observation_end":null,"relations_end":[{"source_id":1173,"target_id":1176,"kind":"lealdade","value":100}]}. Não usar esse estado posterior como entrada antiga nem atribuir consequências futuras sem vínculo causal.

### 06. family — John Montes #4380, h134: check_relative

**Pressão escolhida:** `family` #64335, prioridade 79.5944, base 61.3, fonte `event:149751`, alvo 4383. Motivo: Privação de familiar percebida em encontro.

**Contexto preservado:** {"mode":"care","source_event":149751,"known_location":{"map_id":760,"x":5,"y":9},"diagnostic":{"reason":"Selected","competing":null,"turn":134}}.

**Entrada:** {"id":4380,"name":"John Montes","hour":134,"alive":true,"profession":"lenhador","lod":"local","position":{"map_id":760,"x":2,"y":2},"residence":760,"hp":100,"hunger":64,"thirst":43,"fatigue":43.80000000000028,"money":0,"food":0,"water":1,"local_food":0,"local_water":124,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{}}.

**Personalidade:** {"honesty":9,"compassion":77,"courage":31,"independence":33,"greed":9,"diligence":44,"family_loyalty":12,"persistence":10,"temperament":11,"vengefulness":44,"ambition":22,"sadism":1}. **Emoções escalares de entrada:** {"anger":12.599999999999994,"resentment":16.56000000000002,"humiliation":7.200000000000004,"desperation":0.0,"last_updated":131,"last_support":53,"strain":0,"adaptation":0,"last_adapted":0,"stable_material_hours":0,"nested_collections":"LACUNA: cópia rasa; histórico não utilizado"}.

**Conhecimento/locais de entrada:** {"known_places":{"market":{"map_id":760,"x":5,"y":9},"home":{"map_id":760,"x":2,"y":2},"work":{"map_id":760,"x":8,"y":2},"forage":{"map_id":760,"x":1,"y":9},"well_home":{"map_id":760,"x":2,"y":2},"well_rural":{"map_id":760,"x":1,"y":9},"sacred":{"map_id":760,"x":5,"y":1}},"known_towns":[760,601,3],"route_knowledge_count":2,"knowledge_ids_before":[150890,151943,151946,152980,153906,145835,154995,156032,156033,156034,156036,156974,156981,156985,156987,158042,158043,158044,160222,160226,160229,160233,160235,160240,160241,161374,161377,161381,161384,162681,162684,162687,162691,162695,162697,162714,163076,163080,163844,163847,163850,163855,163862,163868,163871,163876,164306,164310,165116,165118,165120,165122,165135,165136,165137,165139,165143,165154,165559,166374,166376,166378,166387,179554],"market_observation":{"turn":118,"town_id":760,"stock":{"food":3,"grain":68,"water":85,"iron":98,"wood":88},"temporary_work":true,"offers_expire_at":142,"training_offer":null,"price":9,"price_turn":118}}.

**Fatos-fonte retidos após percepção:** [{"event_id":165120,"kind":"ItemStolen","actor_id":4328,"target_id":760,"location":{"map_id":760,"x":5,"y":9},"turn":117,"description":"Arthus Bruma roubou comida no mercado de Dormar.","confidence":100,"required_trust":0,"source_id":null,"source_kind":"direct","context":{"item_id":162680,"item_kind":"food"}}].

| Need | ID/alvo | Base→prioridade | Estado/fonte |
| --- | --- | --- | --- |
| family | 64335/4383 | 61.3→79.5944 | active / event:149751 |
| food | 22045/None | 76.0→78.1 | active / physiology |
| political_pressure | 22049/None | 58.3→70.8976 | active / own_shared_problem |
| food_reserve | 37027/None | 41.0→68.41721854304636 | active / food_reserve |
| family | 90290/4377 | 52.699999999999996→66.7054 | active / event:149750 |
| money | 151944/None | 52.208333333333336→65.35833333333333 | active / economy |
| protection | 15685/4380 | 45→63.092 | active / event:165120 |
| migration | 22046/601 | 52→60.0 | active / known_towns |
| rest | 51803/None | 43.80000000000028→51.80000000000028 | active / physiology |
| work | 31931/None | 35→44.7 | active / profession |
| water | 47043/None | 43→44.35 | active / physiology |
| religious_interest | 22048/5908 | 34.0→39.452799999999996 | active / own_faith |

**Alternativas/gates realmente vistos:**

Need #64335 (`family`): 1 Solutions entraram em _evaluate; 1 saíram disponíveis. Entrada: `check_relative`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| check_relative | {"target":4383,"destination":{"map_id":760,"x":5,"y":9}} | 46.25 | {"base":0.275,"independence":0.04125,"family_loyalty":0.015,"travel":-0.1} | {"feeding":null,"action_pressure":null} |

Need #90290 (`family`): 1 Solutions entraram em _evaluate; 1 saíram disponíveis. Entrada: `check_relative`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| check_relative | {"target":4377,"destination":{"map_id":760,"x":5,"y":9}} | 46.25 | {"base":0.275,"independence":0.04125,"family_loyalty":0.015,"travel":-0.1} | {"feeding":null,"action_pressure":null} |

Need #15685 (`protection`): 8 Solutions entraram em _evaluate; 8 saíram disponíveis. Entrada: `denounce, denounce, denounce, denounce, denounce, denounce, avoid_threat, pursue`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| pursue | {"target":4328,"destination":{"map_id":760,"x":5,"y":4}} | 69.01866786865915 | {"base":0.275,"courage":0.031,"diligence":0.033,"vengefulness":0.044000000000000004,"critical_depletion":0.0,"travel":-0.05,"action_pressure":0.0,"pressure_risk_tolerance":0.012093339343295704} | {"feeding":null,"action_pressure":{"eligible":true,"world_pressure":0,"action_pressure":0.0,"eligibility_causes":[],"source_facts":[],"capacity":70.8,"perceived_capacity":60.04,"major_barriers":[],"selected_alternative":"pursue"}} |
| denounce | {"target":4385,"destination":{"map_id":760,"x":2,"y":2}} | 64.1 | {"base":0.225,"honesty":0.01575,"vengefulness":0.044000000000000004,"courage":0.023250000000000003,"trust":0.0125,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| denounce | {"target":4408,"destination":{"map_id":760,"x":2,"y":2}} | 64.1 | {"base":0.225,"honesty":0.01575,"vengefulness":0.044000000000000004,"courage":0.023250000000000003,"trust":0.0125,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| denounce | {"target":4431,"destination":{"map_id":760,"x":2,"y":8}} | 52.1 | {"base":0.225,"honesty":0.01575,"vengefulness":0.044000000000000004,"courage":0.023250000000000003,"trust":0.0125,"travel":-0.06} | {"feeding":null,"action_pressure":null} |
| denounce | {"target":783,"destination":{"map_id":760,"x":5,"y":9}} | 44.1 | {"base":0.225,"honesty":0.01575,"vengefulness":0.044000000000000004,"courage":0.023250000000000003,"trust":0.0125,"travel":-0.1} | {"feeding":null,"action_pressure":null} |
| denounce | {"target":4339,"destination":{"map_id":760,"x":5,"y":9}} | 44.1 | {"base":0.225,"honesty":0.01575,"vengefulness":0.044000000000000004,"courage":0.023250000000000003,"trust":0.0125,"travel":-0.1} | {"feeding":null,"action_pressure":null} |
| denounce | {"target":4362,"destination":{"map_id":760,"x":5,"y":9}} | 44.1 | {"base":0.225,"honesty":0.01575,"vengefulness":0.044000000000000004,"courage":0.023250000000000003,"trust":0.0125,"travel":-0.1} | {"feeding":null,"action_pressure":null} |
| avoid_threat | {"target":null,"destination":{"map_id":760,"x":2,"y":2}} | 30.349999999999998 | {"base":0.2,"courage":-0.062,"compassion":0.05775,"vengefulness":-0.044000000000000004,"travel":-0.0} | {"feeding":null,"action_pressure":null} |

**Escolhas intermediárias:** [{"chosen":{"action":"check_relative","score":46.25,"target":4383,"destination":{"map_id":760,"x":5,"y":9},"terms":{"base":0.275,"independence":0.04125,"family_loyalty":0.015,"travel":-0.1},"feeding":null,"action_pressure":null},"near_scores":[46.25],"variation_draws":"não capturados; RNG não consultado pelo observador"}].

**Preparação/substituição posterior:** [].

**Winner final / Goal:** {"winner":{"action":"check_relative","score":46.25,"target":4383,"destination":{"map_id":760,"x":5,"y":9},"terms":{"base":0.275,"independence":0.04125,"family_loyalty":0.015,"travel":-0.1},"feeding":null,"action_pressure":null},"goal":{"id":184892,"need_id":64335,"action":"check_relative","score":46.25,"created_at":134,"target_id":4383,"destination":{"map_id":760,"x":5,"y":9},"status":"active","outcome":""},"suspended_before":null,"suspended_after":null}.

**Por que outras Needs não foram executadas:** a fila prioriza emergência/priority/ID e para na primeira solucionável, sujeita à continuidade/preparo. Outras pressões retidas: food#22045(78.1), political_pressure#22049(70.8976), food_reserve#37027(68.41721854304636), family#90290(66.7054), money#151944(65.35833333333333), protection#15685(63.092), migration#22046(60.0), rest#51803(51.80000000000028), work#31931(44.7), water#47043(44.35), religious_interest#22048(39.452799999999996). Não atribuir score global entre Needs.

**Execução:** execute não foi chamado neste trace. A Goal pode ter iniciado/continuado deslocamento; o snapshot e a posição posterior delimitam essa conclusão.

**Cálculos especializados reais:** [{"system":"lethal_decision","function":"lethal_decisions.LethalDecisionSystem.evaluate","result":{"available":false,"pressure":-86.7,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"protection","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":7.48,"directed_emotion":0.0,"commitment":0.0,"sadism":0.13,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":42.35,"moral_restraint":1.08,"fear":0.0,"risk":5.877551020408163,"bond":0.0,"authority_or_witnesses":15,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{"pressure":-86.7,"cause":{"severity":0,"grave":false,"causes":[],"facts":[],"confidence":0,"mode":"retributive","confirmed_injury":0}}},{"system":"lethal_decision","function":"lethal_decisions.LethalDecisionSystem.evaluate","result":{"available":false,"pressure":-86.7,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"protection","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":7.48,"directed_emotion":0.0,"commitment":0.0,"sadism":0.13,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":42.35,"moral_restraint":1.08,"fear":0.0,"risk":5.877551020408163,"bond":0.0,"authority_or_witnesses":15,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{"pressure":-86.7,"cause":{"severity":0,"grave":false,"causes":[],"facts":[],"confidence":0,"mode":"retributive","confirmed_injury":0}}},{"system":"lethal_pressure","function":"lethality.LethalPressure.evaluate","result":{"available":false,"pressure":-86.7,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"protection","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":7.48,"directed_emotion":0.0,"commitment":0.0,"sadism":0.13,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":42.35,"moral_restraint":1.08,"fear":0.0,"risk":5.877551020408163,"bond":0.0,"authority_or_witnesses":15,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{}},{"system":"capacity","function":"action_pressure.ActionPressureSystem.assess","result":{"eligible":true,"world_pressure":0,"action_pressure":0.0,"eligibility_causes":[],"source_facts":[],"capacity":70.8,"perceived_capacity":60.04,"major_barriers":[],"selected_alternative":"pursue"},"inputs":{}}].

**Evento:** nenhum evento retido durante esta decisão. Isso pode significar movimento/efeito sem evento; não implica falha.

**Aprendizado aceito durante a decisão (amostra):** [].

**Recibos posteriores ligados ao mesmo event_id:** []. Contagem é operações de aprendizado aceitas, não indivíduos únicos.

**Consequência imediata:** {"id":4380,"name":"John Montes","hour":134,"alive":true,"profession":"lenhador","lod":"local","position":{"map_id":760,"x":2,"y":5},"residence":760,"hp":100,"hunger":64,"thirst":43,"fatigue":43.80000000000028,"money":0,"food":0,"water":1,"local_food":0,"local_water":124,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{}}. **Observação/relações com o alvo ao final:** {"observation_end":{"turn":110,"position":{"map_id":760,"x":5,"y":9},"hunger":42,"thirst":40,"health":100,"alive":true,"profession":"comerciante","weapon_power":4,"injured":0},"relations_end":[{"source_id":4380,"target_id":4383,"kind":"pai_de","value":100},{"source_id":4380,"target_id":4383,"kind":"amizade","value":73},{"source_id":4380,"target_id":4383,"kind":"confiança","value":61}]}. Não usar esse estado posterior como entrada antiga nem atribuir consequências futuras sem vínculo causal.

### 07. food — Darin Vale #4935, h86: forage

**Pressão escolhida:** `food` #37182, prioridade 100, base 100, fonte `physiology`, alvo None. Motivo: Fome.

**Contexto preservado:** {"emergency":true}.

**Entrada:** {"id":4935,"name":"Darin Vale","hour":86,"alive":true,"profession":"cozinheiro","lod":"active","position":{"map_id":864,"x":2,"y":13},"residence":864,"hp":90,"hunger":100,"thirst":82,"fatigue":86.20000000000017,"money":1,"food":0,"water":0,"local_food":88,"local_water":0,"recoverable_deprivation":10,"starvation_hours":5,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{"ask_help":86}}.

**Personalidade:** {"honesty":86,"compassion":6,"courage":77,"independence":26,"greed":74,"diligence":6,"family_loyalty":14,"persistence":76,"temperament":38,"vengefulness":65,"ambition":5,"sadism":1}. **Emoções escalares de entrada:** {"anger":0.12,"resentment":0.0,"humiliation":0.0,"desperation":8.750000000000002,"last_updated":85,"last_support":-10000,"strain":11.738999999999999,"adaptation":0,"last_adapted":0,"stable_material_hours":0,"nested_collections":"LACUNA: cópia rasa; histórico não utilizado"}.

**Conhecimento/locais de entrada:** {"known_places":{"market":{"map_id":864,"x":7,"y":13},"home":{"map_id":864,"x":2,"y":2},"work":{"map_id":864,"x":7,"y":13},"forage":{"map_id":864,"x":1,"y":13},"well_home":{"map_id":864,"x":2,"y":2},"well_rural":{"map_id":864,"x":1,"y":13},"sacred":{"map_id":864,"x":7,"y":1}},"known_towns":[864,911],"route_knowledge_count":2,"knowledge_ids_before":[97992,97991,97990,97994,97995,97997,97999,98004,98006,93021,90406,99349,90412,86422,95782,112888,112889,112887,112886,112885,112884,112883,112882,112881,112880,112879,112878,112877,112876,112875,112874,112895,112894,112893,112892,112891,114113,114114,114115,114117,114127,114126,114125,114450,114449,114451,115294,116443,116444,116442,116441,116440,116439,116438,116437,117576,117575,117581,117580,117579,117578,117577,114466,125920],"market_observation":{"turn":56,"town_id":864,"stock":{"food":141,"grain":58,"water":0,"iron":68,"wood":120},"temporary_work":true,"offers_expire_at":80,"training_offer":null,"price":2,"price_turn":56}}.

**Fatos-fonte retidos após percepção:** [].

| Need | ID/alvo | Base→prioridade | Estado/fonte |
| --- | --- | --- | --- |
| food | 37182/None | 100→100 | active / physiology |
| water | 42491/None | 82→100 | active / physiology |
| rest | 47160/None | 86.20000000000017→94.20000000000017 | active / physiology |
| food_reserve | 22385/None | 41.0→72.6923076923077 | active / food_reserve |
| money | 22386/None | 52.5→62.432 | active / economy |
| migration | 60516/911 | 52→60.732 | active / known_towns |
| protection | 54879/4935 | 45→56.712 | blocked / event:76824 |
| political_pressure | 60517/None | 41.25→51.8008 | active / own_shared_problem |
| work | 32102/None | 35→37.1 | active / profession |
| advancement | 22388/None | 18.1254→27.3754 | active / aspiration:wealth |

**Alternativas/gates realmente vistos:**

Need #37182 (`food`): 3 Solutions entraram em _evaluate; 3 saíram disponíveis. Entrada: `steal, forage, work`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| forage | {"target":null,"destination":{"map_id":864,"x":1,"y":13}} | 46.0 | {"base":0.175,"independence":0.065,"hunter":0.0,"travel":-0.01} | {"feeding":{"EstimatedTimeUntilFoodConsumed":3,"EstimatedSurvivalMargin":29,"economically_viable":true,"survival_viable":true,"reason":null,"known_conditions":["UnknownPrice","DistantProduct"]},"action_pressure":null} |
| work | {"target":null,"destination":{"map_id":864,"x":7,"y":13}} | 43.0 | {"base":0.25,"diligence":0.015,"physical_depletion":0.0,"travel":-0.05} | {"feeding":{"EstimatedTimeUntilFoodConsumed":8,"EstimatedSurvivalMargin":29,"economically_viable":true,"survival_viable":true,"reason":null,"known_conditions":["UnknownPrice","DistantProduct"]},"action_pressure":null} |
| steal | {"target":null,"destination":{"map_id":864,"x":7,"y":13}} | 15.846031091411563 | {"base":0.35,"greed":0.12333333333333334,"honesty":-0.43,"courage":0.0385,"travel":-0.05,"pressure_moral_tolerance":0.047396822123724494} | {"feeding":{"EstimatedTimeUntilFoodConsumed":7,"EstimatedSurvivalMargin":29,"economically_viable":true,"survival_viable":true,"reason":null,"known_conditions":["UnknownPrice","DistantProduct"]},"action_pressure":null} |

Need #54879 (`protection`): 0 Solutions entraram em _evaluate; 0 saíram disponíveis. Entrada: ``.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |

Need #22388 (`advancement`): 1 Solutions entraram em _evaluate; 1 saíram disponíveis. Entrada: `work`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| work | {"target":null,"destination":{"map_id":864,"x":7,"y":13}} | 43.0 | {"base":0.25,"diligence":0.015,"physical_depletion":0.0,"travel":-0.05} | {"feeding":null,"action_pressure":null} |

**Escolhas intermediárias:** [{"chosen":{"action":"forage","score":46.0,"target":null,"destination":{"map_id":864,"x":1,"y":13},"terms":{"base":0.175,"independence":0.065,"hunter":0.0,"travel":-0.01},"feeding":{"EstimatedTimeUntilFoodConsumed":3,"EstimatedSurvivalMargin":29,"economically_viable":true,"survival_viable":true,"reason":null,"known_conditions":["UnknownPrice","DistantProduct"]},"action_pressure":null},"near_scores":[46.0,43.0,15.846031091411563],"variation_draws":"não capturados; RNG não consultado pelo observador"}].

**Preparação/substituição posterior:** [].

**Winner final / Goal:** {"winner":{"action":"forage","score":46.0,"target":null,"destination":{"map_id":864,"x":1,"y":13},"terms":{"base":0.175,"independence":0.065,"hunter":0.0,"travel":-0.01},"feeding":{"EstimatedTimeUntilFoodConsumed":3,"EstimatedSurvivalMargin":29,"economically_viable":true,"survival_viable":true,"reason":null,"known_conditions":["UnknownPrice","DistantProduct"]},"action_pressure":null},"goal":{"id":117589,"need_id":37182,"action":"forage","score":24.0,"created_at":75,"target_id":null,"destination":{"map_id":864,"x":1,"y":13},"status":"active","outcome":""},"suspended_before":null,"suspended_after":null}.

**Por que outras Needs não foram executadas:** a fila prioriza emergência/priority/ID e para na primeira solucionável, sujeita à continuidade/preparo. Outras pressões retidas: water#42491(100), rest#47160(94.20000000000017), food_reserve#22385(72.6923076923077), money#22386(62.432), migration#60516(60.732), protection#54879(56.712), political_pressure#60517(51.8008), work#32102(37.1), advancement#22388(27.3754). Não atribuir score global entre Needs.

**Execução:** execute não foi chamado neste trace. A Goal pode ter iniciado/continuado deslocamento; o snapshot e a posição posterior delimitam essa conclusão.

**Cálculos especializados reais:** [{"system":"lethal_decision","function":"lethal_decisions.LethalDecisionSystem.evaluate","result":{"available":false,"pressure":-40.09,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"protection","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":11.05,"directed_emotion":0.0,"commitment":0.0,"sadism":0.13,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":3.3000000000000003,"moral_restraint":10.32,"fear":1.49736842105263,"risk":6.153846153846155,"bond":0.0,"authority_or_witnesses":0.0,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{"pressure":-40.09,"cause":{"severity":0,"grave":false,"causes":[],"facts":[],"confidence":0,"mode":"retributive","confirmed_injury":0}}},{"system":"lethal_decision","function":"lethal_decisions.LethalDecisionSystem.evaluate","result":{"available":false,"pressure":-40.09,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"protection","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":11.05,"directed_emotion":0.0,"commitment":0.0,"sadism":0.13,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":3.3000000000000003,"moral_restraint":10.32,"fear":1.49736842105263,"risk":6.153846153846155,"bond":0.0,"authority_or_witnesses":0.0,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{"pressure":-40.09,"cause":{"severity":0,"grave":false,"causes":[],"facts":[],"confidence":0,"mode":"retributive","confirmed_injury":0}}},{"system":"lethal_pressure","function":"lethality.LethalPressure.evaluate","result":{"available":false,"pressure":-40.09,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"protection","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":11.05,"directed_emotion":0.0,"commitment":0.0,"sadism":0.13,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":3.3000000000000003,"moral_restraint":10.32,"fear":1.49736842105263,"risk":6.153846153846155,"bond":0.0,"authority_or_witnesses":0.0,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{}}].

**Evento:** nenhum evento retido durante esta decisão. Isso pode significar movimento/efeito sem evento; não implica falha.

**Aprendizado aceito durante a decisão (amostra):** [].

**Recibos posteriores ligados ao mesmo event_id:** []. Contagem é operações de aprendizado aceitas, não indivíduos únicos.

**Consequência imediata:** {"id":4935,"name":"Darin Vale","hour":86,"alive":true,"profession":"cozinheiro","lod":"active","position":{"map_id":864,"x":1,"y":13},"residence":864,"hp":90,"hunger":100,"thirst":82,"fatigue":86.20000000000017,"money":1,"food":0,"water":0,"local_food":88,"local_water":0,"recoverable_deprivation":10,"starvation_hours":5,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{}}. **Observação/relações com o alvo ao final:** {"observation_end":null,"relations_end":[]}. Não usar esse estado posterior como entrada antiga nem atribuir consequências futuras sem vínculo causal.

### 08. group — Nora Valerius #2806, h149: share_problem

**Pressão escolhida:** `political_pressure` #92540, prioridade 81.90537142857143, base 68.65, fonte `own_shared_problem`, alvo None. Motivo: Buscar representação para problema pessoal.

**Contexto preservado:** {}.

**Entrada:** {"id":2806,"name":"Nora Valerius","hour":149,"alive":true,"profession":"ferreiro","lod":"active","position":{"map_id":367,"x":5,"y":9},"residence":367,"hp":100,"hunger":60,"thirst":73,"fatigue":67.60000000000007,"money":5,"food":0,"water":0,"local_food":8,"local_water":139,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{}}.

**Personalidade:** {"honesty":88,"compassion":87,"courage":81,"independence":64,"greed":85,"diligence":47,"family_loyalty":53,"persistence":92,"temperament":9,"vengefulness":89,"ambition":91,"sadism":0}. **Emoções escalares de entrada:** {"anger":36.41999999999999,"resentment":35.72000000000002,"humiliation":20.900000000000006,"desperation":1.2,"last_updated":148,"last_support":87,"strain":0.28400000000000003,"adaptation":0,"last_adapted":0,"stable_material_hours":0,"nested_collections":"LACUNA: cópia rasa; histórico não utilizado"}.

**Conhecimento/locais de entrada:** {"known_places":{"market":{"map_id":367,"x":5,"y":9},"home":{"map_id":367,"x":2,"y":2},"work":{"map_id":367,"x":8,"y":2},"forage":{"map_id":367,"x":1,"y":9},"well_home":{"map_id":367,"x":2,"y":2},"well_rural":{"map_id":367,"x":1,"y":9},"sacred":{"map_id":367,"x":5,"y":1}},"known_towns":[367,302],"route_knowledge_count":2,"knowledge_ids_before":[181866,181867,168750,182422,182423,182425,184471,194549,194552,194554,195353,195891,195893,195911,195915,196903,197503,197501,197509,197521,197529,197531,197535,197536,197537,197538,197540,198436,198434,198470,198998,199001,199014,199016,199019,199025,199028,199038,199836,199838,199880,200406,200408,200411,200420,200422,201246,201252,201733,201737,201740,201747,202549,203025,203027,203034,203035,203037,203048,203702,204090,204103,204101,204111],"market_observation":{"turn":148,"town_id":367,"stock":{"food":7,"grain":163,"water":144,"iron":70,"wood":108},"temporary_work":true,"offers_expire_at":172,"training_offer":null,"price":4,"price_turn":148}}.

**Fatos-fonte retidos após percepção:** [{"event_id":195891,"kind":"FamilyConcern","actor_id":2806,"target_id":2803,"location":{"map_id":367,"x":5,"y":9},"turn":143,"description":"Nora Valerius percebeu a privação de Ruan Valerius.","confidence":100,"required_trust":0,"source_id":null,"source_kind":"direct","context":{"observed_need":61}},{"event_id":204101,"kind":"ItemStolen","actor_id":2769,"target_id":367,"location":{"map_id":367,"x":5,"y":9},"turn":149,"description":"Ruan Arven roubou comida no mercado de Valria.","confidence":100,"required_trust":0,"source_id":null,"source_kind":"direct","context":{"item_id":204100,"item_kind":"food"}}].

| Need | ID/alvo | Base→prioridade | Estado/fonte |
| --- | --- | --- | --- |
| political_pressure | 92540/None | 68.65→81.90537142857143 | active / own_shared_problem |
| food_reserve | 33278/None | 41.0→78.88679245283019 | active / food_reserve |
| water | 43660/None | 73→76.45 | active / physiology |
| family | 76427/2803 | 58.3→76.14059999999999 | active / event:195891 |
| rest | 52945/None | 67.60000000000007→75.60000000000007 | active / physiology |
| food | 14838/None | 70.0→74.8 | active / physiology |
| organizational_survival | 95224/2746 | 56.301500000000004→68.63429828571428 | active / group:52882 |
| advancement | 14839/None | 27.7554→65.72607264 | blocked / self_assessment:0 |
| protection | 91187/2806 | 45→65.596 | active / event:204101 |
| migration | 92539/302 | 52→60.072 | active / known_towns |
| status | 92538/None | 20→52.414 | active / encounter:597:52 |
| money | 197519/None | 40.208333333333336→50.43033333333334 | active / economy |
| recognition | 14844/367 | 40.2→48.456657142857146 | active / political_aspiration |
| revenge | 91188/2769 | 30.0→46.996 | active / event:204101 |
| religious_interest | 14843/5909 | 27.5→29.675 | active / own_faith |

**Alternativas/gates realmente vistos:**

Need #92540 (`political_pressure`): 1 Solutions entraram em _evaluate; 1 saíram disponíveis. Entrada: `share_problem`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| share_problem | {"target":null,"destination":{"map_id":367,"x":5,"y":9}} | 48.45 | {"base":0.225,"compassion":0.06525,"independence":-0.048,"travel":-0.0} | {"feeding":null,"action_pressure":null} |

Need #76427 (`family`): 1 Solutions entraram em _evaluate; 1 saíram disponíveis. Entrada: `check_relative`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| check_relative | {"target":2803,"destination":{"map_id":367,"x":5,"y":9}} | 84.25 | {"base":0.275,"independence":0.08,"family_loyalty":0.06625,"travel":-0.0} | {"feeding":null,"action_pressure":null} |

Need #14839 (`advancement`): 3 Solutions entraram em _evaluate; 3 saíram disponíveis. Entrada: `work, work_for_food, temporary_service`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| temporary_service | {"target":null,"destination":{"map_id":367,"x":5,"y":9}} | 65.45 | {"base":0.225,"diligence":0.05875,"compassion":0.0435,"physical_depletion":0.0,"travel":-0.0,"no_progress":0.0} | {"feeding":null,"action_pressure":null} |
| work_for_food | {"target":null,"destination":{"map_id":367,"x":1,"y":9}} | 48.75 | {"base":0.225,"diligence":0.05875,"physical_depletion":0.0,"travel":-0.04,"no_progress":0.0} | {"feeding":null,"action_pressure":null} |
| work | {"target":null,"destination":{"map_id":367,"x":8,"y":2}} | -0.5000000000000071 | {"base":0.25,"diligence":0.1175,"physical_depletion":0.0,"travel":-0.1,"no_progress":-0.27} | {"feeding":null,"action_pressure":null} |

Need #91187 (`protection`): 22 Solutions entraram em _evaluate; 22 saíram disponíveis. Entrada: `denounce, denounce, denounce, denounce, denounce, denounce, denounce, denounce, confront, threaten, demand_return, warn, insult, call_help, calm, withdraw, flee, defend, forgive, apologize, surrender, attack`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| denounce | {"target":2748,"destination":{"map_id":367,"x":5,"y":9}} | 108.25 | {"base":0.225,"honesty":0.154,"vengefulness":0.08900000000000001,"courage":0.06075,"trust":0.0125,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| denounce | {"target":2771,"destination":{"map_id":367,"x":5,"y":9}} | 108.25 | {"base":0.225,"honesty":0.154,"vengefulness":0.08900000000000001,"courage":0.06075,"trust":0.0125,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| denounce | {"target":2794,"destination":{"map_id":367,"x":5,"y":9}} | 108.25 | {"base":0.225,"honesty":0.154,"vengefulness":0.08900000000000001,"courage":0.06075,"trust":0.0125,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| denounce | {"target":2840,"destination":{"map_id":367,"x":5,"y":9}} | 108.25 | {"base":0.225,"honesty":0.154,"vengefulness":0.08900000000000001,"courage":0.06075,"trust":0.0125,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| denounce | {"target":2863,"destination":{"map_id":367,"x":4,"y":9}} | 106.25 | {"base":0.225,"honesty":0.154,"vengefulness":0.08900000000000001,"courage":0.06075,"trust":0.0125,"travel":-0.01} | {"feeding":null,"action_pressure":null} |
| denounce | {"target":390,"destination":{"map_id":367,"x":5,"y":5}} | 100.25 | {"base":0.225,"honesty":0.154,"vengefulness":0.08900000000000001,"courage":0.06075,"trust":0.0125,"travel":-0.04} | {"feeding":null,"action_pressure":null} |
| demand_return | {"target":2769,"destination":null} | 92.55 | {"base":0.2,"honesty":0.11,"persistence":0.09200000000000001,"courage":0.06075,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| denounce | {"target":2403,"destination":{"map_id":367,"x":2,"y":2}} | 88.25 | {"base":0.225,"honesty":0.154,"vengefulness":0.08900000000000001,"courage":0.06075,"trust":0.0125,"travel":-0.1} | {"feeding":null,"action_pressure":null} |
| denounce | {"target":2817,"destination":{"map_id":367,"x":2,"y":2}} | 88.25 | {"base":0.225,"honesty":0.154,"vengefulness":0.08900000000000001,"courage":0.06075,"trust":0.0125,"travel":-0.1} | {"feeding":null,"action_pressure":null} |
| confront | {"target":2769,"destination":null} | 70.568 | {"base":0.175,"courage":0.1215,"anger":0.027089999999999993,"risk":-0.0375,"vengefulness":0.06675,"travel":-0.0} | {"feeding":null,"action_pressure":null} |

Need #92538 (`status`): 3 Solutions entraram em _evaluate; 3 saíram disponíveis. Entrada: `work, work_for_food, temporary_service`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| temporary_service | {"target":null,"destination":{"map_id":367,"x":5,"y":9}} | 65.45 | {"base":0.225,"diligence":0.05875,"compassion":0.0435,"physical_depletion":0.0,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| work | {"target":null,"destination":{"map_id":367,"x":8,"y":2}} | 53.49999999999999 | {"base":0.25,"diligence":0.1175,"physical_depletion":0.0,"travel":-0.1} | {"feeding":null,"action_pressure":null} |
| work_for_food | {"target":null,"destination":{"map_id":367,"x":1,"y":9}} | 48.75 | {"base":0.225,"diligence":0.05875,"physical_depletion":0.0,"travel":-0.04} | {"feeding":null,"action_pressure":null} |

Need #91188 (`revenge`): 23 Solutions entraram em _evaluate; 23 saíram disponíveis. Entrada: `investigate, denounce, denounce, denounce, denounce, denounce, denounce, denounce, denounce, confront, threaten, demand_return, warn, insult, call_help, calm, withdraw, flee, defend, forgive, apologize, surrender, attack`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| investigate | {"target":2769,"destination":{"map_id":367,"x":5,"y":9}} | 124.40000000000002 | {"base":0.225,"vengefulness":0.17800000000000002,"courage":0.16200000000000003,"independence":0.096,"compassion":-0.0435,"temperament":0.0045,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| denounce | {"target":2748,"destination":{"map_id":367,"x":5,"y":9}} | 108.25 | {"base":0.225,"honesty":0.154,"vengefulness":0.08900000000000001,"courage":0.06075,"trust":0.0125,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| denounce | {"target":2771,"destination":{"map_id":367,"x":5,"y":9}} | 108.25 | {"base":0.225,"honesty":0.154,"vengefulness":0.08900000000000001,"courage":0.06075,"trust":0.0125,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| denounce | {"target":2794,"destination":{"map_id":367,"x":5,"y":9}} | 108.25 | {"base":0.225,"honesty":0.154,"vengefulness":0.08900000000000001,"courage":0.06075,"trust":0.0125,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| denounce | {"target":2840,"destination":{"map_id":367,"x":5,"y":9}} | 108.25 | {"base":0.225,"honesty":0.154,"vengefulness":0.08900000000000001,"courage":0.06075,"trust":0.0125,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| denounce | {"target":2863,"destination":{"map_id":367,"x":4,"y":9}} | 106.25 | {"base":0.225,"honesty":0.154,"vengefulness":0.08900000000000001,"courage":0.06075,"trust":0.0125,"travel":-0.01} | {"feeding":null,"action_pressure":null} |
| denounce | {"target":390,"destination":{"map_id":367,"x":5,"y":5}} | 100.25 | {"base":0.225,"honesty":0.154,"vengefulness":0.08900000000000001,"courage":0.06075,"trust":0.0125,"travel":-0.04} | {"feeding":null,"action_pressure":null} |
| demand_return | {"target":2769,"destination":null} | 92.55 | {"base":0.2,"honesty":0.11,"persistence":0.09200000000000001,"courage":0.06075,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| denounce | {"target":2403,"destination":{"map_id":367,"x":2,"y":2}} | 88.25 | {"base":0.225,"honesty":0.154,"vengefulness":0.08900000000000001,"courage":0.06075,"trust":0.0125,"travel":-0.1} | {"feeding":null,"action_pressure":null} |
| denounce | {"target":2817,"destination":{"map_id":367,"x":2,"y":2}} | 88.25 | {"base":0.225,"honesty":0.154,"vengefulness":0.08900000000000001,"courage":0.06075,"trust":0.0125,"travel":-0.1} | {"feeding":null,"action_pressure":null} |

**Escolhas intermediárias:** [{"chosen":{"action":"share_problem","score":48.45,"target":null,"destination":{"map_id":367,"x":5,"y":9},"terms":{"base":0.225,"compassion":0.06525,"independence":-0.048,"travel":-0.0},"feeding":null,"action_pressure":null},"near_scores":[48.45],"variation_draws":"não capturados; RNG não consultado pelo observador"}].

**Preparação/substituição posterior:** [].

**Winner final / Goal:** {"winner":{"action":"share_problem","score":48.45,"target":null,"destination":{"map_id":367,"x":5,"y":9},"terms":{"base":0.225,"compassion":0.06525,"independence":-0.048,"travel":-0.0},"feeding":null,"action_pressure":null},"goal":{"id":204115,"need_id":92540,"action":"share_problem","score":48.45,"created_at":149,"target_id":null,"destination":{"map_id":367,"x":5,"y":9},"status":"completed","outcome":"Problema próprio comunicado presencialmente."},"suspended_before":null,"suspended_after":null}.

**Por que outras Needs não foram executadas:** a fila prioriza emergência/priority/ID e para na primeira solucionável, sujeita à continuidade/preparo. Outras pressões retidas: food_reserve#33278(78.88679245283019), water#43660(76.45), family#76427(76.14059999999999), rest#52945(75.60000000000007), food#14838(74.8), organizational_survival#95224(68.63429828571428), advancement#14839(65.72607264), protection#91187(65.596), migration#92539(60.072), status#92538(52.414), money#197519(50.43033333333334), recognition#14844(48.456657142857146), revenge#91188(46.996), religious_interest#14843(29.675). Não atribuir score global entre Needs.

**Execução:** {"success":true,"result":[true,"Problema próprio comunicado presencialmente."],"goal_at_entry":{"id":204115,"need_id":92540,"action":"share_problem","score":48.45,"created_at":149,"target_id":null,"destination":{"map_id":367,"x":5,"y":9},"status":"active","outcome":""},"before":{"id":2806,"name":"Nora Valerius","hour":149,"alive":true,"profession":"ferreiro","lod":"active","position":{"map_id":367,"x":5,"y":9},"residence":367,"hp":100,"hunger":60,"thirst":73,"fatigue":67.60000000000007,"money":5,"food":0,"water":0,"local_food":8,"local_water":139,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{}},"after":{"id":2806,"name":"Nora Valerius","hour":149,"alive":true,"profession":"ferreiro","lod":"active","position":{"map_id":367,"x":5,"y":9},"residence":367,"hp":100,"hunger":60,"thirst":73,"fatigue":67.60000000000007,"money":5,"food":0,"water":0,"local_food":8,"local_water":139,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{}}}.

**Cálculos especializados reais:** [{"system":"lethal_decision","function":"lethal_decisions.LethalDecisionSystem.evaluate","result":{"available":false,"pressure":-86.7,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"protection","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":15.13,"directed_emotion":7.579000000000009,"commitment":0.0,"sadism":0.0,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":47.85,"moral_restraint":10.559999999999999,"fear":0.0,"risk":6.0,"bond":0.0,"authority_or_witnesses":15,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{"pressure":-86.7,"cause":{"severity":0,"grave":false,"causes":[],"facts":[],"confidence":0,"mode":"retributive","confirmed_injury":0}}},{"system":"lethal_decision","function":"lethal_decisions.LethalDecisionSystem.evaluate","result":{"available":false,"pressure":-86.7,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"protection","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":15.13,"directed_emotion":7.579000000000009,"commitment":0.0,"sadism":0.0,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":47.85,"moral_restraint":10.559999999999999,"fear":0.0,"risk":6.0,"bond":0.0,"authority_or_witnesses":15,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{"pressure":-86.7,"cause":{"severity":0,"grave":false,"causes":[],"facts":[],"confidence":0,"mode":"retributive","confirmed_injury":0}}},{"system":"lethal_pressure","function":"lethality.LethalPressure.evaluate","result":{"available":false,"pressure":-86.7,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"protection","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":15.13,"directed_emotion":7.579000000000009,"commitment":0.0,"sadism":0.0,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":47.85,"moral_restraint":10.559999999999999,"fear":0.0,"risk":6.0,"bond":0.0,"authority_or_witnesses":15,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{}},{"system":"lethal_decision","function":"lethal_decisions.LethalDecisionSystem.evaluate","result":{"available":false,"pressure":-86.7,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"revenge","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":15.13,"directed_emotion":7.579000000000009,"commitment":0.0,"sadism":0.0,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":47.85,"moral_restraint":10.559999999999999,"fear":0.0,"risk":6.0,"bond":0.0,"authority_or_witnesses":15,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{"pressure":-86.7,"cause":{"severity":0,"grave":false,"causes":[],"facts":[],"confidence":0,"mode":"retributive","confirmed_injury":0}}},{"system":"lethal_decision","function":"lethal_decisions.LethalDecisionSystem.evaluate","result":{"available":false,"pressure":-86.7,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"revenge","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":15.13,"directed_emotion":7.579000000000009,"commitment":0.0,"sadism":0.0,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":47.85,"moral_restraint":10.559999999999999,"fear":0.0,"risk":6.0,"bond":0.0,"authority_or_witnesses":15,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{"pressure":-86.7,"cause":{"severity":0,"grave":false,"causes":[],"facts":[],"confidence":0,"mode":"retributive","confirmed_injury":0}}},{"system":"lethal_pressure","function":"lethality.LethalPressure.evaluate","result":{"available":false,"pressure":-86.7,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"revenge","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":15.13,"directed_emotion":7.579000000000009,"commitment":0.0,"sadism":0.0,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":47.85,"moral_restraint":10.559999999999999,"fear":0.0,"risk":6.0,"bond":0.0,"authority_or_witnesses":15,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{}},{"system":"lethal_decision","function":"lethal_decisions.LethalDecisionSystem.evaluate","result":{"available":false,"pressure":-86.7,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"protection","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":15.13,"directed_emotion":7.579000000000009,"commitment":0.0,"sadism":0.0,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":47.85,"moral_restraint":10.559999999999999,"fear":0.0,"risk":6.0,"bond":0.0,"authority_or_witnesses":15,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{"pressure":-86.7,"cause":{"severity":0,"grave":false,"causes":[],"facts":[],"confidence":0,"mode":"retributive","confirmed_injury":0}}},{"system":"lethal_pressure","function":"lethality.LethalPressure.evaluate","result":{"available":false,"pressure":-86.7,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"protection","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":15.13,"directed_emotion":7.579000000000009,"commitment":0.0,"sadism":0.0,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":47.85,"moral_restraint":10.559999999999999,"fear":0.0,"risk":6.0,"bond":0.0,"authority_or_witnesses":15,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{"reason":"inhibition"}},{"system":"lethal_decision","function":"lethal_decisions.LethalDecisionSystem.evaluate","result":{"available":false,"pressure":-86.7,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"revenge","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":15.13,"directed_emotion":7.579000000000009,"commitment":0.0,"sadism":0.0,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":47.85,"moral_restraint":10.559999999999999,"fear":0.0,"risk":6.0,"bond":0.0,"authority_or_witnesses":15,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{"pressure":-86.7,"cause":{"severity":0,"grave":false,"causes":[],"facts":[],"confidence":0,"mode":"retributive","confirmed_injury":0}}},{"system":"lethal_pressure","function":"lethality.LethalPressure.evaluate","result":{"available":false,"pressure":-86.7,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"revenge","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":15.13,"directed_emotion":7.579000000000009,"commitment":0.0,"sadism":0.0,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":47.85,"moral_restraint":10.559999999999999,"fear":0.0,"risk":6.0,"bond":0.0,"authority_or_witnesses":15,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{"reason":"inhibition"}},{"system":"lethal_decision","function":"lethal_decisions.LethalDecisionSystem.evaluate","result":{"available":false,"pressure":-86.7,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"protection","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":15.13,"directed_emotion":7.579000000000009,"commitment":0.0,"sadism":0.0,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":47.85,"moral_restraint":10.559999999999999,"fear":0.0,"risk":6.0,"bond":0.0,"authority_or_witnesses":15,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{"pressure":-86.7,"cause":{"severity":0,"grave":false,"causes":[],"facts":[],"confidence":0,"mode":"retributive","confirmed_injury":0}}},{"system":"lethal_pressure","function":"lethality.LethalPressure.evaluate","result":{"available":false,"pressure":-86.7,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"protection","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":15.13,"directed_emotion":7.579000000000009,"commitment":0.0,"sadism":0.0,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":47.85,"moral_restraint":10.559999999999999,"fear":0.0,"risk":6.0,"bond":0.0,"authority_or_witnesses":15,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{}},{"system":"capacity","function":"action_pressure.ActionPressureSystem.assess","result":{"eligible":true,"world_pressure":0,"action_pressure":0.0,"eligibility_causes":[],"source_facts":[],"capacity":54.93,"perceived_capacity":68.55,"major_barriers":[],"selected_alternative":"attack"},"inputs":{"scores":{"repel":47.400000000000006,"contain":51.25,"subdue":28.8,"hurt":22.62399999999999,"kill":-1000}}},{"system":"lethal_decision","function":"lethal_decisions.LethalDecisionSystem.evaluate","result":{"available":false,"pressure":-86.7,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"revenge","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":15.13,"directed_emotion":7.579000000000009,"commitment":0.0,"sadism":0.0,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":47.85,"moral_restraint":10.559999999999999,"fear":0.0,"risk":6.0,"bond":0.0,"authority_or_witnesses":15,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{"pressure":-86.7,"cause":{"severity":0,"grave":false,"causes":[],"facts":[],"confidence":0,"mode":"retributive","confirmed_injury":0}}},{"system":"lethal_pressure","function":"lethality.LethalPressure.evaluate","result":{"available":false,"pressure":-86.7,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"revenge","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":15.13,"directed_emotion":7.579000000000009,"commitment":0.0,"sadism":0.0,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":47.85,"moral_restraint":10.559999999999999,"fear":0.0,"risk":6.0,"bond":0.0,"authority_or_witnesses":15,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{}},{"system":"capacity","function":"action_pressure.ActionPressureSystem.assess","result":{"eligible":true,"world_pressure":0,"action_pressure":0.0,"eligibility_causes":[],"source_facts":[],"capacity":54.93,"perceived_capacity":68.55,"major_barriers":[],"selected_alternative":"attack"},"inputs":{"scores":{"repel":47.400000000000006,"contain":51.25,"subdue":28.8,"hurt":22.62399999999999,"kill":-1000}}}].

| Evento/hora | Actor→target | Emissor | Testemunhas | Contexto |
| --- | --- | --- | --- | --- |
| 204116 / 149 / ProblemShared | 2806→None | ["society.SocietySystem.emit","society.SocietySystem.execute","goals.GoalSystem._execute"] | [382,388,597,2734,2740,2746,2769,2771,2794,2806,2835,2838,2840,2849] | {"cause":"security","subject":null,"severity":55,"source_fact":null} |

**Aprendizado aceito durante a decisão (amostra):** [{"npc":382,"event":204116,"kind":"ProblemShared","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":388,"event":204116,"kind":"ProblemShared","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":597,"event":204116,"kind":"ProblemShared","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":2734,"event":204116,"kind":"ProblemShared","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":2740,"event":204116,"kind":"ProblemShared","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":2746,"event":204116,"kind":"ProblemShared","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":2769,"event":204116,"kind":"ProblemShared","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":2771,"event":204116,"kind":"ProblemShared","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":2794,"event":204116,"kind":"ProblemShared","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":2806,"event":204116,"kind":"ProblemShared","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":2835,"event":204116,"kind":"ProblemShared","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":2838,"event":204116,"kind":"ProblemShared","source":null,"firsthand":true,"confidence":100,"latency":0}].

**Recibos posteriores ligados ao mesmo event_id:** [{"event":204116,"kind":"ProblemShared","learned":{"count":15,"first":149,"last":180,"first_people":[382,388,597,2734,2740,2746]}}]. Contagem é operações de aprendizado aceitas, não indivíduos únicos.

**Consequência imediata:** {"id":2806,"name":"Nora Valerius","hour":149,"alive":true,"profession":"ferreiro","lod":"active","position":{"map_id":367,"x":5,"y":9},"residence":367,"hp":100,"hunger":60,"thirst":73,"fatigue":67.60000000000007,"money":5,"food":0,"water":0,"local_food":8,"local_water":139,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{}}. **Observação/relações com o alvo ao final:** {"observation_end":null,"relations_end":[]}. Não usar esse estado posterior como entrada antiga nem atribuir consequências futuras sem vínculo causal.

### 09. investigation — Lyra Alvor #3421, h168: pursue

**Pressão escolhida:** `pursuit` #123482, prioridade 76.25530758017493, base 68, fonte `event:125355`, alvo 3410. Motivo: Localizar pessoa procurada com evidência conhecida.

**Contexto preservado:** {"institutional_role":"search","known_location":{"map_id":544,"x":3,"y":9},"source_event":125355}.

**Entrada:** {"id":3421,"name":"Lyra Alvor","hour":168,"alive":true,"profession":"guarda","lod":"active","position":{"map_id":544,"x":3,"y":9},"residence":544,"hp":100,"hunger":60,"thirst":67,"fatigue":60.40000000000008,"money":0,"food":2,"water":0,"local_food":25,"local_water":158,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{}}.

**Personalidade:** {"honesty":67,"compassion":28,"courage":40,"independence":79,"greed":5,"diligence":45,"family_loyalty":45,"persistence":80,"temperament":86,"vengefulness":31,"ambition":79,"sadism":40}. **Emoções escalares de entrada:** {"anger":16.74,"resentment":16.320000000000025,"humiliation":9.300000000000011,"desperation":19.899999999999977,"last_updated":167,"last_support":-10000,"strain":40.3485,"adaptation":0,"last_adapted":0,"stable_material_hours":0,"nested_collections":"LACUNA: cópia rasa; histórico não utilizado"}.

**Conhecimento/locais de entrada:** {"known_places":{"market":{"map_id":544,"x":5,"y":9},"home":{"map_id":544,"x":2,"y":2},"work":{"map_id":544,"x":5,"y":9},"forage":{"map_id":544,"x":1,"y":9},"well_home":{"map_id":544,"x":2,"y":2},"well_rural":{"map_id":544,"x":1,"y":9},"sacred":{"map_id":544,"x":5,"y":1}},"known_towns":[544,302,573],"route_knowledge_count":4,"knowledge_ids_before":[184123,181983,189304,191898,193306,194663,194675,196035,197670,197692,197693,197700,197701,197702,197703,197704,197706,200556,200578,201266,201891,204228,183085,205438,206434,206441,180411,215874,216952,183091,149571,217648,217652,218189,218197,218202,218204,218214,219307,219309,219315,219317,219322,219325,219336,219341,220528,220530,220538,220540,220541,220542,220543,220546,220553,221185,221860,221876,221878,221879,221891,223139,223147,223149],"market_observation":{"turn":166,"town_id":544,"stock":{"food":16,"grain":94,"water":108,"iron":94,"wood":80},"temporary_work":true,"offers_expire_at":190,"training_offer":null,"price":2,"price_turn":166}}.

**Fatos-fonte retidos após percepção:** [{"event_id":189304,"kind":"AbsenceNoticed","actor_id":3421,"target_id":null,"location":{"map_id":544,"x":5,"y":5},"turn":138,"description":"Lyra Alvor não localiza um familiar há 39 horas.","confidence":100,"required_trust":0,"source_id":null,"source_kind":"direct","context":{"last_seen":99,"relative_id":3419}},{"event_id":219309,"kind":"WantedIssued","actor_id":3421,"target_id":544,"location":{"map_id":544,"x":5,"y":9},"turn":163,"description":"Lyra Alvor registrou procura por Tomas Montes.","confidence":100,"required_trust":0,"source_id":null,"source_kind":"direct","context":{"record_id":219308,"suspect_id":3413,"source_fact":219307,"severity":1,"confidence":100,"last_known_location":{"map_id":544,"x":5,"y":9}}}].

| Need | ID/alvo | Base→prioridade | Estado/fonte |
| --- | --- | --- | --- |
| family | 171551/3416 | 59.2→79.3924142857143 | blocked / event:171550 |
| pursuit | 123482/3410 | 68→76.25530758017493 | active / event:125355 |
| water | 48571/None | 67→75 | active / physiology |
| money | 51567/None | 56.166666666666664→74.77066666666666 | active / economy |
| food | 15119/None | 70.0→74.5 | active / physiology |
| rest | 48572/None | 60.40000000000008→68.40000000000008 | active / physiology |
| political_pressure | 110039/None | 53.016666666666666→65.61219523809524 | active / own_shared_problem |
| family | 62622/3419 | 46.5→63.248157142857146 | active / event:189304 |
| status | 15122/None | 26.0274→60.42773926857143 | active / aspiration:recognition |
| military_service | 51568/544 | 55→60.258 | active / known_local_case |
| advancement | 15120/None | 15→43.4585 | selected / self_assessment:0 |

**Alternativas/gates realmente vistos:**

Need #171551 (`family`): 0 Solutions entraram em _evaluate; 0 saíram disponíveis. Entrada: ``.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |

Need #123482 (`pursuit`): 1 Solutions entraram em _evaluate; 1 saíram disponíveis. Entrada: `pursue`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| pursue | {"target":3410,"destination":{"map_id":544,"x":3,"y":9}} | 79.0270053042344 | {"base":0.275,"courage":0.04,"diligence":0.03375,"vengefulness":0.031,"critical_depletion":0.0,"travel":-0.0,"action_pressure":0.0,"pressure_risk_tolerance":0.015385026521171965} | {"feeding":null,"action_pressure":{"eligible":true,"world_pressure":0,"action_pressure":0.0,"eligibility_causes":[],"source_facts":[],"capacity":59.73,"perceived_capacity":54.95,"major_barriers":[],"selected_alternative":"pursue"}} |

Need #123482 (`pursuit`): 1 Solutions entraram em _evaluate; 1 saíram disponíveis. Entrada: `pursue`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| pursue | {"target":3410,"destination":{"map_id":544,"x":3,"y":9}} | 79.0270053042344 | {"base":0.275,"courage":0.04,"diligence":0.03375,"vengefulness":0.031,"critical_depletion":0.0,"travel":-0.0,"action_pressure":0.0,"pressure_risk_tolerance":0.015385026521171965} | {"feeding":null,"action_pressure":{"eligible":true,"world_pressure":0,"action_pressure":0.0,"eligibility_causes":[],"source_facts":[],"capacity":59.73,"perceived_capacity":54.95,"major_barriers":[],"selected_alternative":"pursue"}} |

Need #171551 (`family`): 0 Solutions entraram em _evaluate; 0 saíram disponíveis. Entrada: ``.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |

Need #62622 (`family`): 1 Solutions entraram em _evaluate; 1 saíram disponíveis. Entrada: `check_relative`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| check_relative | {"target":3419,"destination":{"map_id":544,"x":5,"y":9}} | 82.0 | {"base":0.275,"independence":0.09875,"family_loyalty":0.05625,"travel":-0.02} | {"feeding":null,"action_pressure":null} |

Need #15122 (`status`): 1 Solutions entraram em _evaluate; 1 saíram disponíveis. Entrada: `work`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| work | {"target":null,"destination":{"map_id":544,"x":5,"y":9}} | 68.5 | {"base":0.25,"diligence":0.1125,"physical_depletion":0.0,"travel":-0.02,"no_progress":0.0} | {"feeding":null,"action_pressure":null} |

Need #15120 (`advancement`): 1 Solutions entraram em _evaluate; 1 saíram disponíveis. Entrada: `work`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| work | {"target":null,"destination":{"map_id":544,"x":5,"y":9}} | 68.5 | {"base":0.25,"diligence":0.1125,"physical_depletion":0.0,"travel":-0.02} | {"feeding":null,"action_pressure":null} |

**Escolhas intermediárias:** [{"chosen":{"action":"pursue","score":79.0270053042344,"target":3410,"destination":{"map_id":544,"x":3,"y":9},"terms":{"base":0.275,"courage":0.04,"diligence":0.03375,"vengefulness":0.031,"critical_depletion":0.0,"travel":-0.0,"action_pressure":0.0,"pressure_risk_tolerance":0.015385026521171965},"feeding":null,"action_pressure":{"eligible":true,"world_pressure":0,"action_pressure":0.0,"eligibility_causes":[],"source_facts":[],"capacity":59.73,"perceived_capacity":54.95,"major_barriers":[],"selected_alternative":"pursue"}},"near_scores":[79.0270053042344],"variation_draws":"não capturados; RNG não consultado pelo observador"}].

**Preparação/substituição posterior:** [].

**Winner final / Goal:** {"winner":{"action":"pursue","score":79.0270053042344,"target":3410,"destination":{"map_id":544,"x":3,"y":9},"terms":{"base":0.275,"courage":0.04,"diligence":0.03375,"vengefulness":0.031,"critical_depletion":0.0,"travel":-0.0,"action_pressure":0.0,"pressure_risk_tolerance":0.015385026521171965},"feeding":null,"action_pressure":{"eligible":true,"world_pressure":0,"action_pressure":0.0,"eligibility_causes":[],"source_facts":[],"capacity":59.73,"perceived_capacity":54.95,"major_barriers":[],"selected_alternative":"pursue"}},"goal":{"id":223150,"need_id":123482,"action":"pursue","score":74.78202359063155,"created_at":166,"target_id":3410,"destination":{"map_id":544,"x":3,"y":9},"status":"completed","outcome":"Busca local sem encontro; não consulta posição remota."},"suspended_before":null,"suspended_after":null}.

**Por que outras Needs não foram executadas:** a fila prioriza emergência/priority/ID e para na primeira solucionável, sujeita à continuidade/preparo. Outras pressões retidas: family#171551(79.3924142857143), water#48571(75), money#51567(74.77066666666666), food#15119(74.5), rest#48572(68.40000000000008), political_pressure#110039(65.61219523809524), family#62622(63.248157142857146), status#15122(60.42773926857143), military_service#51568(60.258), advancement#15120(43.4585). Não atribuir score global entre Needs.

**Execução:** {"success":true,"result":[true,"Busca local sem encontro; não consulta posição remota."],"goal_at_entry":{"id":223150,"need_id":123482,"action":"pursue","score":74.78202359063155,"created_at":166,"target_id":3410,"destination":{"map_id":544,"x":3,"y":9},"status":"active","outcome":""},"before":{"id":3421,"name":"Lyra Alvor","hour":168,"alive":true,"profession":"guarda","lod":"active","position":{"map_id":544,"x":3,"y":9},"residence":544,"hp":100,"hunger":60,"thirst":67,"fatigue":60.40000000000008,"money":0,"food":2,"water":0,"local_food":25,"local_water":158,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{}},"after":{"id":3421,"name":"Lyra Alvor","hour":168,"alive":true,"profession":"guarda","lod":"active","position":{"map_id":544,"x":3,"y":9},"residence":544,"hp":100,"hunger":60,"thirst":67,"fatigue":60.40000000000008,"money":0,"food":2,"water":0,"local_food":25,"local_water":158,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{}}}.

**Cálculos especializados reais:** [{"system":"lethal_decision","function":"lethal_decisions.LethalDecisionSystem.evaluate","result":{"available":false,"pressure":-42.99,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"pursuit","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":5.2700000000000005,"directed_emotion":3.47600000000001,"commitment":0.0,"sadism":5.2,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":15.400000000000002,"moral_restraint":8.04,"fear":0.0,"risk":3.498542274052478,"bond":0.0,"authority_or_witnesses":0.0,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{"pressure":-42.99,"cause":{"severity":0,"grave":false,"causes":[],"facts":[],"confidence":0,"mode":"retributive","confirmed_injury":0}}},{"system":"lethal_decision","function":"lethal_decisions.LethalDecisionSystem.evaluate","result":{"available":false,"pressure":-42.99,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"pursuit","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":5.2700000000000005,"directed_emotion":3.47600000000001,"commitment":0.0,"sadism":5.2,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":15.400000000000002,"moral_restraint":8.04,"fear":0.0,"risk":3.498542274052478,"bond":0.0,"authority_or_witnesses":0.0,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{"pressure":-42.99,"cause":{"severity":0,"grave":false,"causes":[],"facts":[],"confidence":0,"mode":"retributive","confirmed_injury":0}}},{"system":"lethal_pressure","function":"lethality.LethalPressure.evaluate","result":{"available":false,"pressure":-42.99,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"pursuit","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":5.2700000000000005,"directed_emotion":3.47600000000001,"commitment":0.0,"sadism":5.2,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":15.400000000000002,"moral_restraint":8.04,"fear":0.0,"risk":3.498542274052478,"bond":0.0,"authority_or_witnesses":0.0,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{}},{"system":"capacity","function":"action_pressure.ActionPressureSystem.assess","result":{"eligible":true,"world_pressure":0,"action_pressure":0.0,"eligibility_causes":[],"source_facts":[],"capacity":59.73,"perceived_capacity":54.95,"major_barriers":[],"selected_alternative":"pursue"},"inputs":{}},{"system":"capacity","function":"action_pressure.ActionPressureSystem.assess","result":{"eligible":true,"world_pressure":0,"action_pressure":0.0,"eligibility_causes":[],"source_facts":[],"capacity":59.73,"perceived_capacity":54.95,"major_barriers":[],"selected_alternative":"pursue"},"inputs":{}}].

| Evento/hora | Actor→target | Emissor | Testemunhas | Contexto |
| --- | --- | --- | --- | --- |
| 225971 / 168 / PursuitSearch | 3421→None | ["conflicts.ConflictSystem.execute","goals.GoalSystem._execute","goals.GoalSystem.execute"] | [3421] | {"target_id":3410,"source_fact":125355,"attempt":1} |

**Aprendizado aceito durante a decisão (amostra):** [{"npc":3421,"event":225971,"kind":"PursuitSearch","source":null,"firsthand":true,"confidence":100,"latency":0}].

**Recibos posteriores ligados ao mesmo event_id:** [{"event":225971,"kind":"PursuitSearch","learned":{"count":1,"first":168,"last":168,"first_people":[3421]}}]. Contagem é operações de aprendizado aceitas, não indivíduos únicos.

**Consequência imediata:** {"id":3421,"name":"Lyra Alvor","hour":168,"alive":true,"profession":"guarda","lod":"active","position":{"map_id":544,"x":3,"y":9},"residence":544,"hp":100,"hunger":60,"thirst":67,"fatigue":60.40000000000008,"money":0,"food":2,"water":0,"local_food":25,"local_water":158,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{}}. **Observação/relações com o alvo ao final:** {"observation_end":{"turn":159,"position":{"map_id":544,"x":3,"y":9},"hunger":85,"thirst":48,"health":100,"alive":true,"profession":"ferreiro","weapon_power":4,"injured":0},"relations_end":[]}. Não usar esse estado posterior como entrada antiga nem atribuir consequências futuras sem vínculo causal.

### 10. justice — Arthus Douran #1799, h160: secure

**Pressão escolhida:** `security` #31027, prioridade 0, base 60, fonte `event:214510`, alvo 1840. Motivo: Cael Solaris roubou comida no mercado de Normar..

**Contexto preservado:** {}.

**Entrada:** {"id":1799,"name":"Arthus Douran","hour":160,"alive":true,"profession":"guarda","lod":"active","position":{"map_id":115,"x":5,"y":9},"residence":115,"hp":100,"hunger":60,"thirst":50,"fatigue":62.00000000000028,"money":2,"food":1,"water":0,"local_food":7,"local_water":113,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{"crime:201186":171,"crime:208876":178,"crime:209114":179,"crime:210136":180,"crime:211331":181,"crime:212411":182}}.

**Personalidade:** {"honesty":88,"compassion":31,"courage":61,"independence":26,"greed":72,"diligence":44,"family_loyalty":5,"persistence":14,"temperament":44,"vengefulness":15,"ambition":52,"sadism":58}. **Emoções escalares de entrada:** {"anger":30.89999999999999,"resentment":25.060000000000024,"humiliation":16.300000000000004,"desperation":1.4999999999999998,"last_updated":159,"last_support":47,"strain":3.0839999999999996,"adaptation":0,"last_adapted":0,"stable_material_hours":0,"nested_collections":"LACUNA: cópia rasa; histórico não utilizado"}.

**Conhecimento/locais de entrada:** {"known_places":{"market":{"map_id":115,"x":5,"y":9},"home":{"map_id":115,"x":2,"y":2},"work":{"map_id":115,"x":5,"y":9},"forage":{"map_id":115,"x":1,"y":9},"well_home":{"map_id":115,"x":2,"y":2},"well_rural":{"map_id":115,"x":1,"y":9},"sacred":{"map_id":115,"x":5,"y":1}},"known_towns":[115,3,144],"route_knowledge_count":4,"knowledge_ids_before":[203908,208094,208097,208106,208120,208878,208876,209087,209092,209095,209098,209111,209109,209116,209114,209119,209867,209869,210104,210112,210118,210122,210124,210126,210132,210138,210136,211042,211285,211288,211297,211300,211306,211321,211328,211333,211331,211359,212390,212396,212399,212403,212411,212413,212419,212432,212434,213217,213446,213452,213455,213464,214213,214479,214481,214485,214497,214506,214510,214512,214515,215305,215556,215558],"market_observation":{"turn":159,"town_id":115,"stock":{"food":6,"grain":69,"water":117,"iron":120,"wood":120},"temporary_work":true,"offers_expire_at":183,"training_offer":null,"price":5,"price_turn":159}}.

**Fatos-fonte retidos após percepção:** [{"event_id":214512,"kind":"WantedIssued","actor_id":1799,"target_id":115,"location":{"map_id":115,"x":5,"y":9},"turn":159,"description":"Arthus Douran registrou procura por Cael Solaris.","confidence":100,"required_trust":0,"source_id":null,"source_kind":"direct","context":{"record_id":214511,"suspect_id":1840,"source_fact":214510,"severity":1,"confidence":100,"last_known_location":{"map_id":115,"x":5,"y":9}}},{"event_id":214510,"kind":"ItemStolen","actor_id":1840,"target_id":115,"location":{"map_id":115,"x":5,"y":9},"turn":159,"description":"Cael Solaris roubou comida no mercado de Normar.","confidence":100,"required_trust":0,"source_id":null,"source_kind":"direct","context":{"item_id":214509,"item_kind":"food"}}].

| Need | ID/alvo | Base→prioridade | Estado/fonte |
| --- | --- | --- | --- |
| security | 31027/1840 | 60→90.0116 | active / event:214510 |
| food | 17433/None | 70.0→71.8 | active / physiology |
| pursuit | 215562/1840 | 68→68.0 | active / event:214510 |
| rest | 34667/None | 62.00000000000028→66.50000000000028 | active / physiology |
| money | 146522/None | 48.458333333333336→65.39033333333334 | active / economy |
| military_service | 31030/115 | 55→64.8854 | active / known_local_case |
| family | 17435/1802 | 46.0→60.1988 | active / event:190198 |
| family | 89670/1797 | 43.900000000000006→58.71160000000001 | active / event:180101 |
| water | 39549/None | 50→51.8 | active / physiology |
| political_pressure | 31029/None | 45.25833333333333→49.34993333333333 | active / own_shared_problem |
| advancement | 17437/None | 23.052→48.386606057142856 | selected / aspiration:wealth |
| work | 31026/None | 35→45.0 | active / profession |
| food_reserve | 31025/None | 37.0→41.5 | active / food_reserve |
| religious_interest | 17438/5908 | 28.25→33.6034 | active / own_faith |

**Alternativas/gates realmente vistos:**

Need #31027 (`security`): 1 Solutions entraram em _evaluate; 1 saíram disponíveis. Entrada: `secure`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| secure | {"target":1840,"destination":{"map_id":115,"x":5,"y":9}} | 90.33333333333333 | {"base":0.35,"courage":0.10166666666666668,"travel":-0.0} | {"feeding":null,"action_pressure":null} |

Need #17435 (`family`): 1 Solutions entraram em _evaluate; 1 saíram disponíveis. Entrada: `check_relative`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| check_relative | {"target":1802,"destination":{"map_id":115,"x":5,"y":9}} | 62.75000000000001 | {"base":0.275,"independence":0.0325,"family_loyalty":0.00625,"travel":-0.0} | {"feeding":null,"action_pressure":null} |

Need #89670 (`family`): 1 Solutions entraram em _evaluate; 1 saíram disponíveis. Entrada: `check_relative`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| check_relative | {"target":1797,"destination":{"map_id":115,"x":2,"y":8}} | 54.75000000000001 | {"base":0.275,"independence":0.0325,"family_loyalty":0.00625,"travel":-0.04} | {"feeding":null,"action_pressure":null} |

Need #17437 (`advancement`): 1 Solutions entraram em _evaluate; 1 saíram disponíveis. Entrada: `work`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| work | {"target":null,"destination":{"map_id":115,"x":5,"y":9}} | 72.0 | {"base":0.25,"diligence":0.11,"physical_depletion":0.0,"travel":-0.0,"no_progress":0.0} | {"feeding":null,"action_pressure":null} |

**Escolhas intermediárias:** [{"chosen":{"action":"secure","score":90.33333333333333,"target":1840,"destination":{"map_id":115,"x":5,"y":9},"terms":{"base":0.35,"courage":0.10166666666666668,"travel":-0.0},"feeding":null,"action_pressure":null},"near_scores":[90.33333333333333],"variation_draws":"não capturados; RNG não consultado pelo observador"}].

**Preparação/substituição posterior:** [].

**Winner final / Goal:** {"winner":{"action":"secure","score":90.33333333333333,"target":1840,"destination":{"map_id":115,"x":5,"y":9},"terms":{"base":0.35,"courage":0.10166666666666668,"travel":-0.0},"feeding":null,"action_pressure":null},"goal":{"id":215563,"need_id":31027,"action":"secure","score":90.33333333333333,"created_at":160,"target_id":1840,"destination":{"map_id":115,"x":5,"y":9},"status":"completed","outcome":"Suspeito encontrado; intervenção registrada."},"suspended_before":null,"suspended_after":null}.

**Por que outras Needs não foram executadas:** a fila prioriza emergência/priority/ID e para na primeira solucionável, sujeita à continuidade/preparo. Outras pressões retidas: food#17433(71.8), pursuit#215562(68.0), rest#34667(66.50000000000028), money#146522(65.39033333333334), military_service#31030(64.8854), family#17435(60.1988), family#89670(58.71160000000001), water#39549(51.8), political_pressure#31029(49.34993333333333), advancement#17437(48.386606057142856), work#31026(45.0), food_reserve#31025(41.5), religious_interest#17438(33.6034). Não atribuir score global entre Needs.

**Execução:** {"success":true,"result":[true,"Suspeito encontrado; intervenção registrada."],"goal_at_entry":{"id":215563,"need_id":31027,"action":"secure","score":90.33333333333333,"created_at":160,"target_id":1840,"destination":{"map_id":115,"x":5,"y":9},"status":"active","outcome":""},"before":{"id":1799,"name":"Arthus Douran","hour":160,"alive":true,"profession":"guarda","lod":"active","position":{"map_id":115,"x":5,"y":9},"residence":115,"hp":100,"hunger":60,"thirst":50,"fatigue":62.00000000000028,"money":2,"food":1,"water":0,"local_food":7,"local_water":113,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{"crime:201186":171,"crime:208876":178,"crime:209114":179,"crime:210136":180,"crime:211331":181,"crime:212411":182}},"after":{"id":1799,"name":"Arthus Douran","hour":160,"alive":true,"profession":"guarda","lod":"active","position":{"map_id":115,"x":5,"y":9},"residence":115,"hp":100,"hunger":60,"thirst":50,"fatigue":62.00000000000028,"money":2,"food":1,"water":0,"local_food":7,"local_water":113,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{"crime:201186":171,"crime:208876":178,"crime:209114":179,"crime:210136":180,"crime:211331":181,"crime:212411":182,"crime:214510":184}}}.

**Cálculos especializados reais:** [{"system":"lethal_decision","function":"lethal_decisions.LethalDecisionSystem.evaluate","result":{"available":false,"pressure":-61.64,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"pursuit","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":2.5500000000000003,"directed_emotion":3.9545000000000003,"commitment":0.0,"sadism":7.54,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":17.05,"moral_restraint":10.559999999999999,"fear":0.0,"risk":3.0769230769230775,"bond":0.0,"authority_or_witnesses":15,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{"pressure":-61.64,"cause":{"severity":0,"grave":false,"causes":[],"facts":[],"confidence":0,"mode":"retributive","confirmed_injury":0}}},{"system":"lethal_decision","function":"lethal_decisions.LethalDecisionSystem.evaluate","result":{"available":false,"pressure":-61.64,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"pursuit","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":2.5500000000000003,"directed_emotion":3.9545000000000003,"commitment":0.0,"sadism":7.54,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":17.05,"moral_restraint":10.559999999999999,"fear":0.0,"risk":3.0769230769230775,"bond":0.0,"authority_or_witnesses":15,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{"pressure":-61.64,"cause":{"severity":0,"grave":false,"causes":[],"facts":[],"confidence":0,"mode":"retributive","confirmed_injury":0}}},{"system":"lethal_pressure","function":"lethality.LethalPressure.evaluate","result":{"available":false,"pressure":-61.64,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"pursuit","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":2.5500000000000003,"directed_emotion":3.9545000000000003,"commitment":0.0,"sadism":7.54,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":17.05,"moral_restraint":10.559999999999999,"fear":0.0,"risk":3.0769230769230775,"bond":0.0,"authority_or_witnesses":15,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{}}].

| Evento/hora | Actor→target | Emissor | Testemunhas | Contexto |
| --- | --- | --- | --- | --- |
| 215564 / 160 / GuardResponded | 1799→1840 | ["goals.GoalSystem._execute","goals.GoalSystem.execute","goals.GoalSystem.decide"] | [124,1739,1745,1748,1791,1799,1834,1837,1840,1843,1845,1857,1868] | {"record_id":214511,"fine":5,"source_fact":214510} |

**Aprendizado aceito durante a decisão (amostra):** [{"npc":124,"event":215564,"kind":"GuardResponded","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":1739,"event":215564,"kind":"GuardResponded","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":1745,"event":215564,"kind":"GuardResponded","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":1748,"event":215564,"kind":"GuardResponded","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":1791,"event":215564,"kind":"GuardResponded","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":1799,"event":215564,"kind":"GuardResponded","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":1834,"event":215564,"kind":"GuardResponded","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":1837,"event":215564,"kind":"GuardResponded","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":1840,"event":215564,"kind":"GuardResponded","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":1843,"event":215564,"kind":"GuardResponded","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":1845,"event":215564,"kind":"GuardResponded","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":1857,"event":215564,"kind":"GuardResponded","source":null,"firsthand":true,"confidence":100,"latency":0}].

**Recibos posteriores ligados ao mesmo event_id:** [{"event":215564,"kind":"GuardResponded","learned":{"count":14,"first":160,"last":168,"first_people":[124,1739,1745,1748,1791,1799]}}]. Contagem é operações de aprendizado aceitas, não indivíduos únicos.

**Consequência imediata:** {"id":1799,"name":"Arthus Douran","hour":160,"alive":true,"profession":"guarda","lod":"active","position":{"map_id":115,"x":5,"y":9},"residence":115,"hp":100,"hunger":60,"thirst":50,"fatigue":62.00000000000028,"money":2,"food":1,"water":0,"local_food":7,"local_water":113,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{"crime:201186":171,"crime:208876":178,"crime:209114":179,"crime:210136":180,"crime:211331":181,"crime:212411":182,"crime:214510":184}}. **Observação/relações com o alvo ao final:** {"observation_end":{"turn":160,"position":{"map_id":115,"x":5,"y":9},"hunger":59,"thirst":50,"health":100,"alive":true,"profession":"lenhador","weapon_power":4,"injured":0},"relations_end":[]}. Não usar esse estado posterior como entrada antiga nem atribuir consequências futuras sem vínculo causal.

### 11. lethal — Aldren Alvor #3851, h249: attack

**Classificação:** Reclassificação editorial de cálculo letal realmente capturado; não é execução de finish nem uma oportunidade terminal comprovada. Categoria original do observador: combat.

**Pressão escolhida:** `protection` #63374, prioridade 100, base 66.70400000000001, fonte `event:282721`, alvo 3854. Motivo: Proteger pessoa diante de conflito conhecido.

**Contexto preservado:** {"source_event":282721,"threat":3877,"victim":3854,"known_location":{"map_id":630,"x":3,"y":5},"diagnostic":{"reason":"Selected","competing":null,"turn":249}}.

**Entrada:** {"id":3851,"name":"Aldren Alvor","hour":249,"alive":true,"profession":"lenhador","lod":"active","position":{"map_id":630,"x":3,"y":5},"residence":630,"hp":84,"hunger":34,"thirst":48,"fatigue":70.80000000000008,"money":9,"food":0,"water":1,"local_food":66,"local_water":152,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{}}.

**Personalidade:** {"honesty":71,"compassion":26,"courage":34,"independence":38,"greed":53,"diligence":89,"family_loyalty":71,"persistence":11,"temperament":82,"vengefulness":42,"ambition":6,"sadism":0}. **Emoções escalares de entrada:** {"anger":97.30000000000005,"resentment":99.79999999999997,"humiliation":8.500000000000002,"desperation":2.6499999999999995,"last_updated":248,"last_support":232,"strain":9.447999999999997,"adaptation":0,"last_adapted":0,"stable_material_hours":0,"nested_collections":"LACUNA: cópia rasa; histórico não utilizado"}.

**Conhecimento/locais de entrada:** {"known_places":{"market":{"map_id":630,"x":3,"y":5},"home":{"map_id":630,"x":2,"y":2},"work":{"map_id":630,"x":4,"y":2},"forage":{"map_id":630,"x":1,"y":5},"well_home":{"map_id":630,"x":2,"y":2},"well_rural":{"map_id":630,"x":1,"y":5},"sacred":{"map_id":630,"x":3,"y":1}},"known_towns":[630,601,3],"route_knowledge_count":2,"knowledge_ids_before":[275698,277007,292261,293268,294227,297323,297324,297331,297846,297848,297850,298469,298473,299641,299645,299659,300846,300849,300851,300857,301941,301943,301945,301951,303043,303047,303057,303062,304106,304112,304114,304545,305063,305064,305070,305709,305711,306340,306342,306832,307397,307822,309336,309343,309341,309346,309347,309349,309817,310369,310374,310830,310833,311387,311959,312547,313083,313618,313622,314110,314602,315134,315132,315136],"market_observation":{"turn":248,"town_id":630,"stock":{"food":67,"grain":30,"water":152,"iron":84,"wood":118},"temporary_work":true,"offers_expire_at":272,"training_offer":null,"price":2,"price_turn":248}}.

**Fatos-fonte retidos após percepção:** [{"event_id":310833,"kind":"CharacterConfronted","actor_id":642,"target_id":3851,"location":{"map_id":630,"x":3,"y":5},"turn":245,"description":"Cael Alvor: confront diante de Aldren Alvor.","confidence":100,"required_trust":0,"source_id":null,"source_kind":"direct","context":{"source_fact":305063,"record_id":277026,"lawful":true}},{"event_id":294227,"kind":"CharacterAttacked","actor_id":3877,"target_id":3851,"location":{"map_id":630,"x":3,"y":5},"turn":229,"description":"Iria Hammer feriu Aldren Alvor em 2 HP.","confidence":100,"required_trust":0,"source_id":null,"source_kind":"direct","context":{"damage":2,"weapon_id":null,"intended_target":3851,"source_fact":294218,"lawful":false,"self_defense":true,"violence_intent":"contain","post_incapacity":false,"victim_profession":"lenhador","actor_groups":[73273],"action_audit":{"eligible":true,"world_pressure":45,"action_pressure":23.23,"eligibility_causes":["unresolved_attributed_injury"],"source_facts":[285952,287017,288094],"capacity":44.87,"perceived_capacity":28.72,"major_barriers":[],"selected_alternative":"attack"}}},{"event_id":315132,"kind":"ItemStolen","actor_id":636,"target_id":630,"location":{"map_id":630,"x":3,"y":5},"turn":249,"description":"Silas Bruma roubou comida no mercado de Karria.","confidence":100,"required_trust":0,"source_id":null,"source_kind":"direct","context":{"item_id":315131,"item_kind":"food"}}].

| Need | ID/alvo | Base→prioridade | Estado/fonte |
| --- | --- | --- | --- |
| protection | 63374/3854 | 66.70400000000001→100 | selected / event:282721 |
| response | 289115/3877 | 75→98.29944632025048 | active / event:294227 |
| family | 92801/3848 | 56.4→83.10914285714286 | blocked / event:272032 |
| rest | 35391/None | 70.80000000000008→76.50000000000009 | active / physiology |
| protection | 203739/3851 | 45→74.28800000000001 | active / event:315132 |
| food_reserve | 35389/None | 40.8→73.62115594329333 | active / food_reserve |
| response | 277028/642 | 50→70.08800000000001 | active / event:310833 |
| political_pressure | 64112/None | 55.9→67.7652 | active / own_shared_problem |
| migration | 64111/601 | 52→60.224 | active / known_towns |
| water | 40320/None | 48→56 | active / physiology |
| work | 35392/None | 35→52.95 | active / profession |
| healing | 291237/3851 | 48.0→51.45 | active / injury |
| money | 312545/None | 32.125→50.599 | active / economy |

**Alternativas/gates realmente vistos:**

Need #63374 (`protection`): 17 Solutions entraram em _evaluate; 17 saíram disponíveis. Entrada: `avoid_threat, stay_near, threaten, warn, insult, call_help, calm, withdraw, flee, defend, forgive, apologize, surrender, attack, intervene, protect, alert`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| attack | {"target":3877,"destination":null} | 153.20526457728576 | {"base":0.14,"anger":0.21825000000000014,"resentment":0.14963999999999994,"vengefulness":0.063,"courage":0.0425,"risk":-0.09951720849440575,"compassion":-0.03900000000000001,"authority":-0.0625,"low_health":0.0,"defensive":0.125,"bond":-0.0,"critical_depletion":-0.0,"travel":-0.0,"pressure_risk_tolerance":0.014053531380834428,"known_reputation":-0.03,"lethal_continuity":0.2446} | {"feeding":null,"action_pressure":{"eligible":true,"world_pressure":55,"action_pressure":22.44,"eligibility_causes":["immediate_physical_threat"],"source_facts":[292261,293268,294227],"capacity":44.35,"perceived_capacity":44.35,"major_barriers":[],"decision_id":285945,"selected_alternative":"attack"}} |
| defend | {"target":3877,"destination":null} | 82.54701895403689 | {"base":0.2,"risk":0.045235094770184434,"courage":0.025500000000000002,"defensive":0.15,"injury":-0.008,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| stay_near | {"target":3854,"destination":null} | 68.35 | {"base":0.175,"family_loyalty":0.12424999999999999,"courage":0.0425,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| protect | {"target":3877,"destination":null} | 62.21238483677048 | {"base":0.175,"family_loyalty":0.08875,"compassion":0.0325,"courage":0.051000000000000004,"bond":0.0,"risk":-0.03618807581614755,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| threaten | {"target":3877,"destination":null} | 61.1107062761669 | {"base":0.125,"anger":0.14550000000000007,"courage":0.034,"temperament":0.08199999999999999,"compassion":-0.0325,"authority":-0.0625,"critical_depletion":0.0,"travel":-0.0,"pressure_risk_tolerance":0.014053531380834428} | {"feeding":null,"action_pressure":null} |
| apologize | {"target":3877,"destination":null} | 59.999999999999986 | {"base":0.125,"honesty":0.08875,"compassion":0.0325,"culpability":0.175,"anger":-0.12125000000000007,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| alert | {"target":3877,"destination":null} | 56.697018954036885 | {"base":0.175,"honesty":0.08875,"risk":0.045235094770184434,"courage":-0.025500000000000002,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| flee | {"target":3877,"destination":null} | 54.05642274484426 | {"base":0.175,"fear":0.032,"risk":0.05428211372422132,"courage":-0.0425,"low_health":0.0,"injury":-0.016,"authority":0.0375,"travel":-0.0,"known_reputation":0.03} | {"feeding":null,"action_pressure":null} |
| insult | {"target":3877,"destination":null} | 48.98000000000001 | {"base":0.075,"anger":0.14550000000000007,"humiliation":0.008400000000000001,"temperament":0.06149999999999999,"compassion":-0.0455,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| warn | {"target":3877,"destination":null} | 45.849999999999994 | {"base":0.15,"compassion":0.026000000000000002,"honesty":0.05324999999999999,"travel":-0.0} | {"feeding":null,"action_pressure":null} |

Need #92801 (`family`): 1 Solutions entraram em _evaluate; 1 saíram disponíveis. Entrada: `check_relative`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| check_relative | {"target":3848,"destination":{"map_id":630,"x":3,"y":5}} | 82.25 | {"base":0.275,"independence":0.0475,"family_loyalty":0.08875,"travel":-0.0} | {"feeding":null,"action_pressure":null} |

Need #203739 (`protection`): 15 Solutions entraram em _evaluate; 15 saíram disponíveis. Entrada: `denounce, avoid_threat, confront, threaten, demand_return, warn, insult, call_help, calm, withdraw, flee, defend, forgive, apologize, surrender`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| denounce | {"target":642,"destination":{"map_id":630,"x":3,"y":5}} | 86.85000000000001 | {"base":0.225,"honesty":0.12424999999999999,"vengefulness":0.042,"courage":0.025500000000000002,"trust":0.0175,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| defend | {"target":636,"destination":null} | 85.06807581254165 | {"base":0.2,"risk":0.057840379062708246,"courage":0.025500000000000002,"defensive":0.15,"injury":-0.008,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| flee | {"target":636,"destination":null} | 71.46816440500167 | {"base":0.175,"fear":0.1339323671497585,"risk":0.06940845487524988,"courage":-0.0425,"low_health":0.0,"injury":-0.016,"authority":0.0375,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| demand_return | {"target":636,"destination":null} | 65.05 | {"base":0.2,"honesty":0.08875,"persistence":0.011000000000000001,"courage":0.025500000000000002,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| confront | {"target":636,"destination":null} | 59.109154512475016 | {"base":0.175,"courage":0.051000000000000004,"anger":0.07275000000000004,"risk":-0.03470422743762494,"vengefulness":0.0315,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| threaten | {"target":636,"destination":null} | 58.4234744222006 | {"base":0.125,"anger":0.14550000000000007,"courage":0.034,"temperament":0.08199999999999999,"compassion":-0.0325,"authority":-0.0625,"critical_depletion":0.0,"travel":-0.0,"pressure_risk_tolerance":0.0006173721110029006} | {"feeding":null,"action_pressure":null} |
| insult | {"target":636,"destination":null} | 48.98000000000001 | {"base":0.075,"anger":0.14550000000000007,"humiliation":0.008400000000000001,"temperament":0.06149999999999999,"compassion":-0.0455,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| warn | {"target":636,"destination":null} | 45.849999999999994 | {"base":0.15,"compassion":0.026000000000000002,"honesty":0.05324999999999999,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| surrender | {"target":636,"destination":null} | 38.06807581254164 | {"base":0.125,"authority":0.1,"risk":0.057840379062708246,"low_health":0.0,"courage":-0.0425,"defensive":-0.05,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| call_help | {"target":636,"destination":null} | 37.34154589371981 | {"base":0.125,"fear":0.08370772946859907,"independence":-0.038,"injury":0.016,"travel":-0.0} | {"feeding":null,"action_pressure":null} |

**Escolhas intermediárias:** [{"chosen":{"action":"attack","score":153.20526457728576,"target":3877,"destination":null,"terms":{"base":0.14,"anger":0.21825000000000014,"resentment":0.14963999999999994,"vengefulness":0.063,"courage":0.0425,"risk":-0.09951720849440575,"compassion":-0.03900000000000001,"authority":-0.0625,"low_health":0.0,"defensive":0.125,"bond":-0.0,"critical_depletion":-0.0,"travel":-0.0,"pressure_risk_tolerance":0.014053531380834428,"known_reputation":-0.03,"lethal_continuity":0.2446},"feeding":null,"action_pressure":{"eligible":true,"world_pressure":55,"action_pressure":22.44,"eligibility_causes":["immediate_physical_threat"],"source_facts":[292261,293268,294227],"capacity":44.35,"perceived_capacity":44.35,"major_barriers":[],"decision_id":285945,"selected_alternative":"attack"}},"near_scores":[153.20526457728576,82.54701895403689,68.35,62.21238483677048,61.1107062761669,59.999999999999986,56.697018954036885,54.05642274484426],"variation_draws":"não capturados; RNG não consultado pelo observador"}].

**Preparação/substituição posterior:** [].

**Winner final / Goal:** {"winner":{"action":"attack","score":153.20526457728576,"target":3877,"destination":null,"terms":{"base":0.14,"anger":0.21825000000000014,"resentment":0.14963999999999994,"vengefulness":0.063,"courage":0.0425,"risk":-0.09951720849440575,"compassion":-0.03900000000000001,"authority":-0.0625,"low_health":0.0,"defensive":0.125,"bond":-0.0,"critical_depletion":-0.0,"travel":-0.0,"pressure_risk_tolerance":0.014053531380834428,"known_reputation":-0.03,"lethal_continuity":0.2446},"feeding":null,"action_pressure":{"eligible":true,"world_pressure":55,"action_pressure":22.44,"eligibility_causes":["immediate_physical_threat"],"source_facts":[292261,293268,294227],"capacity":44.35,"perceived_capacity":44.35,"major_barriers":[],"decision_id":285945,"selected_alternative":"attack"}},"goal":{"id":315655,"need_id":63374,"action":"attack","score":153.20526457728576,"created_at":249,"target_id":3877,"destination":null,"status":"completed","outcome":"Ataque causou 3 de dano real."},"suspended_before":null,"suspended_after":null}.

**Por que outras Needs não foram executadas:** a fila prioriza emergência/priority/ID e para na primeira solucionável, sujeita à continuidade/preparo. Outras pressões retidas: response#289115(98.29944632025048), family#92801(83.10914285714286), rest#35391(76.50000000000009), protection#203739(74.28800000000001), food_reserve#35389(73.62115594329333), response#277028(70.08800000000001), political_pressure#64112(67.7652), migration#64111(60.224), water#40320(56), work#35392(52.95), healing#291237(51.45), money#312545(50.599). Não atribuir score global entre Needs.

**Execução:** {"success":true,"result":[true,"Ataque causou 3 de dano real."],"goal_at_entry":{"id":315655,"need_id":63374,"action":"attack","score":153.20526457728576,"created_at":249,"target_id":3877,"destination":null,"status":"active","outcome":""},"before":{"id":3851,"name":"Aldren Alvor","hour":249,"alive":true,"profession":"lenhador","lod":"active","position":{"map_id":630,"x":3,"y":5},"residence":630,"hp":84,"hunger":34,"thirst":48,"fatigue":70.80000000000008,"money":9,"food":0,"water":1,"local_food":66,"local_water":152,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{}},"after":{"id":3851,"name":"Aldren Alvor","hour":249,"alive":true,"profession":"lenhador","lod":"active","position":{"map_id":630,"x":3,"y":5},"residence":630,"hp":84,"hunger":34,"thirst":48,"fatigue":70.80000000000008,"money":9,"food":0,"water":1,"local_food":66,"local_water":152,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{}}}.

**Cálculos especializados reais:** [{"system":"lethal_decision","function":"lethal_decisions.LethalDecisionSystem.evaluate","result":{"available":false,"pressure":-74.74,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"protection","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":7.140000000000001,"directed_emotion":7.364500000000017,"commitment":0.0,"sadism":0.0,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":14.3,"moral_restraint":8.52,"fear":23.37119806763286,"risk":5.552676390019991,"bond":0.0,"authority_or_witnesses":7.5,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{"pressure":-74.74,"cause":{"severity":0,"grave":false,"causes":[],"facts":[],"confidence":0,"mode":"retributive","confirmed_injury":0}}},{"system":"lethal_decision","function":"lethal_decisions.LethalDecisionSystem.evaluate","result":{"available":false,"pressure":-74.74,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"protection","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":7.140000000000001,"directed_emotion":7.364500000000017,"commitment":0.0,"sadism":0.0,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":14.3,"moral_restraint":8.52,"fear":23.37119806763286,"risk":5.552676390019991,"bond":0.0,"authority_or_witnesses":7.5,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{"pressure":-74.74,"cause":{"severity":0,"grave":false,"causes":[],"facts":[],"confidence":0,"mode":"retributive","confirmed_injury":0}}},{"system":"lethal_pressure","function":"lethality.LethalPressure.evaluate","result":{"available":false,"pressure":-74.74,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"protection","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":7.140000000000001,"directed_emotion":7.364500000000017,"commitment":0.0,"sadism":0.0,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":14.3,"moral_restraint":8.52,"fear":23.37119806763286,"risk":5.552676390019991,"bond":0.0,"authority_or_witnesses":7.5,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{}},{"system":"lethal_decision","function":"lethal_decisions.LethalDecisionSystem.evaluate","result":{"available":false,"pressure":-88.67,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"response","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":7.140000000000001,"directed_emotion":6.704500000000008,"commitment":0.0,"sadism":0.0,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":14.3,"moral_restraint":8.52,"fear":34.9,"risk":7.2972815193913085,"bond":0.0,"authority_or_witnesses":7.5,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{"pressure":-88.67,"cause":{"severity":0,"grave":false,"causes":[],"facts":[],"confidence":0,"mode":"retributive","confirmed_injury":0}}},{"system":"lethal_decision","function":"lethal_decisions.LethalDecisionSystem.evaluate","result":{"available":false,"pressure":-88.67,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"response","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":7.140000000000001,"directed_emotion":6.704500000000008,"commitment":0.0,"sadism":0.0,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":14.3,"moral_restraint":8.52,"fear":34.9,"risk":7.2972815193913085,"bond":0.0,"authority_or_witnesses":7.5,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{"pressure":-88.67,"cause":{"severity":0,"grave":false,"causes":[],"facts":[],"confidence":0,"mode":"retributive","confirmed_injury":0}}},{"system":"lethal_pressure","function":"lethality.LethalPressure.evaluate","result":{"available":false,"pressure":-88.67,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"response","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":7.140000000000001,"directed_emotion":6.704500000000008,"commitment":0.0,"sadism":0.0,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":14.3,"moral_restraint":8.52,"fear":34.9,"risk":7.2972815193913085,"bond":0.0,"authority_or_witnesses":7.5,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{}},{"system":"lethal_decision","function":"lethal_decisions.LethalDecisionSystem.evaluate","result":{"available":true,"pressure":83.92,"mode":"protective","confidence":100,"known_facts":[292261,293268,294227],"source_fact":294227,"commitment_id":null,"motive":"protection","world_pressure":55,"grave_basis":"immediate_physical_threat","blocking":[],"positive_factors":{"instigation":22.5,"vengefulness":7.140000000000001,"directed_emotion":21.643600000000003,"commitment":0.0,"sadism":0.0,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":14.3,"moral_restraint":8.52,"fear":5.584,"risk":4.342569097937705,"bond":0.0,"authority_or_witnesses":7.5,"uncertain_authorship":0.0,"available_nonlethal_alternative":10},"decision_id":285945,"rumination":100,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{"pressure":83.92,"cause":{"severity":55,"facts":[292261,293268,294227],"confidence":100,"mode":"protective","causes":["immediate_physical_threat"]}}},{"system":"lethal_pressure","function":"lethality.LethalPressure.evaluate","result":{"available":true,"pressure":83.92,"mode":"protective","confidence":100,"known_facts":[292261,293268,294227],"source_fact":294227,"commitment_id":null,"motive":"protection","world_pressure":55,"grave_basis":"immediate_physical_threat","blocking":[],"positive_factors":{"instigation":22.5,"vengefulness":7.140000000000001,"directed_emotion":21.643600000000003,"commitment":0.0,"sadism":0.0,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":14.3,"moral_restraint":8.52,"fear":5.584,"risk":4.342569097937705,"bond":0.0,"authority_or_witnesses":7.5,"uncertain_authorship":0.0,"available_nonlethal_alternative":10},"decision_id":285945,"rumination":100,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{}},{"system":"lethal_decision","function":"lethal_decisions.LethalDecisionSystem.evaluate","result":{"available":true,"pressure":83.92,"mode":"protective","confidence":100,"known_facts":[292261,293268,294227],"source_fact":294227,"commitment_id":null,"motive":"response","world_pressure":55,"grave_basis":"immediate_physical_threat","blocking":[],"positive_factors":{"instigation":22.5,"vengefulness":7.140000000000001,"directed_emotion":21.643600000000003,"commitment":0.0,"sadism":0.0,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":14.3,"moral_restraint":8.52,"fear":5.584,"risk":4.342569097937705,"bond":0.0,"authority_or_witnesses":7.5,"uncertain_authorship":0.0,"available_nonlethal_alternative":10},"decision_id":285945,"rumination":100,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{"pressure":83.92,"cause":{"severity":55,"facts":[292261,293268,294227],"confidence":100,"mode":"protective","causes":["immediate_physical_threat"]}}},{"system":"lethal_pressure","function":"lethality.LethalPressure.evaluate","result":{"available":true,"pressure":83.92,"mode":"protective","confidence":100,"known_facts":[292261,293268,294227],"source_fact":294227,"commitment_id":null,"motive":"response","world_pressure":55,"grave_basis":"immediate_physical_threat","blocking":[],"positive_factors":{"instigation":22.5,"vengefulness":7.140000000000001,"directed_emotion":21.643600000000003,"commitment":0.0,"sadism":0.0,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":14.3,"moral_restraint":8.52,"fear":5.584,"risk":4.342569097937705,"bond":0.0,"authority_or_witnesses":7.5,"uncertain_authorship":0.0,"available_nonlethal_alternative":10},"decision_id":285945,"rumination":100,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{}},{"system":"terminal","function":"lethal_decisions.LethalDecisionSystem.terminal","result":{"choice":"spare","scores":{"finish":-9.76,"spare":80.4,"capture":-1000,"help":-1000,"withdraw":33.0},"reason":"incapacity_removed_immediate_threat","decision_id":285945,"defensive_threat":0,"inhibition":14.3,"mode":"protective","actor":3851,"target":3877,"cause":"immediate_physical_threat","source_facts":[292261,293268,294227],"intensity":55.68,"world_pressure":55,"action_pressure":36.99,"rumination":100,"retribution":false,"continued_motive":false,"compassion":26,"fear":0.16,"attachment":0,"death_affinity":0,"sadism":0,"religious_influence":{"help":0,"withdraw":0},"actor_health":84,"target_health":53,"actor_fatigue":70.80000000000008},"inputs":{"scores":{"finish":-9.755999999999986,"spare":80.4,"capture":-1000,"help":-1000,"withdraw":33.0}}},{"system":"lethal_decision","function":"lethal_decisions.LethalDecisionSystem.evaluate","result":{"available":true,"pressure":83.92,"mode":"protective","confidence":100,"known_facts":[292261,293268,294227],"source_fact":294227,"commitment_id":null,"motive":"protection","world_pressure":55,"grave_basis":"immediate_physical_threat","blocking":[],"positive_factors":{"instigation":22.5,"vengefulness":7.140000000000001,"directed_emotion":21.643600000000003,"commitment":0.0,"sadism":0.0,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":14.3,"moral_restraint":8.52,"fear":5.584,"risk":4.342569097937705,"bond":0.0,"authority_or_witnesses":7.5,"uncertain_authorship":0.0,"available_nonlethal_alternative":10},"decision_id":285945,"rumination":100,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{"pressure":83.92,"cause":{"severity":55,"facts":[292261,293268,294227],"confidence":100,"mode":"protective","causes":["immediate_physical_threat"]}}},{"system":"capacity","function":"action_pressure.ActionPressureSystem.assess","result":{"eligible":true,"world_pressure":55,"action_pressure":22.44,"eligibility_causes":["immediate_physical_threat"],"source_facts":[292261,293268,294227],"capacity":44.35,"perceived_capacity":44.35,"major_barriers":[],"decision_id":285945,"selected_alternative":"attack"},"inputs":{}},{"system":"lethal_decision","function":"lethal_decisions.LethalDecisionSystem.evaluate","result":{"available":true,"pressure":83.92,"mode":"protective","confidence":100,"known_facts":[292261,293268,294227],"source_fact":294227,"commitment_id":null,"motive":"protection","world_pressure":55,"grave_basis":"immediate_physical_threat","blocking":[],"positive_factors":{"instigation":22.5,"vengefulness":7.140000000000001,"directed_emotion":21.643600000000003,"commitment":0.0,"sadism":0.0,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":14.3,"moral_restraint":8.52,"fear":5.584,"risk":4.342569097937705,"bond":0.0,"authority_or_witnesses":7.5,"uncertain_authorship":0.0,"available_nonlethal_alternative":10},"decision_id":285945,"rumination":100,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{"pressure":83.92,"cause":{"severity":55,"facts":[292261,293268,294227],"confidence":100,"mode":"protective","causes":["immediate_physical_threat"]}}},{"system":"lethal_pressure","function":"lethality.LethalPressure.evaluate","result":{"available":true,"pressure":83.92,"mode":"protective","confidence":100,"known_facts":[292261,293268,294227],"source_fact":294227,"commitment_id":null,"motive":"protection","world_pressure":55,"grave_basis":"immediate_physical_threat","blocking":[],"positive_factors":{"instigation":22.5,"vengefulness":7.140000000000001,"directed_emotion":21.643600000000003,"commitment":0.0,"sadism":0.0,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":14.3,"moral_restraint":8.52,"fear":5.584,"risk":4.342569097937705,"bond":0.0,"authority_or_witnesses":7.5,"uncertain_authorship":0.0,"available_nonlethal_alternative":10},"decision_id":285945,"rumination":100,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{}},{"system":"lethal_decision","function":"lethal_decisions.LethalDecisionSystem.evaluate","result":{"available":true,"pressure":83.92,"mode":"protective","confidence":100,"known_facts":[292261,293268,294227],"source_fact":294227,"commitment_id":null,"motive":"protection","world_pressure":55,"grave_basis":"immediate_physical_threat","blocking":[],"positive_factors":{"instigation":22.5,"vengefulness":7.140000000000001,"directed_emotion":21.643600000000003,"commitment":0.0,"sadism":0.0,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":14.3,"moral_restraint":8.52,"fear":5.584,"risk":4.342569097937705,"bond":0.0,"authority_or_witnesses":7.5,"uncertain_authorship":0.0,"available_nonlethal_alternative":10},"decision_id":285945,"rumination":100,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{"pressure":83.92,"cause":{"severity":55,"facts":[292261,293268,294227],"confidence":100,"mode":"protective","causes":["immediate_physical_threat"]}}},{"system":"lethal_pressure","function":"lethality.LethalPressure.evaluate","result":{"available":true,"pressure":83.92,"mode":"protective","confidence":100,"known_facts":[292261,293268,294227],"source_fact":294227,"commitment_id":null,"motive":"protection","world_pressure":55,"grave_basis":"immediate_physical_threat","blocking":[],"positive_factors":{"instigation":22.5,"vengefulness":7.140000000000001,"directed_emotion":21.643600000000003,"commitment":0.0,"sadism":0.0,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":14.3,"moral_restraint":8.52,"fear":5.584,"risk":4.342569097937705,"bond":0.0,"authority_or_witnesses":7.5,"uncertain_authorship":0.0,"available_nonlethal_alternative":10},"decision_id":285945,"rumination":100,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{}},{"system":"lethal_decision","function":"lethal_decisions.LethalDecisionSystem.evaluate","result":{"available":true,"pressure":83.92,"mode":"protective","confidence":100,"known_facts":[292261,293268,294227],"source_fact":294227,"commitment_id":null,"motive":"protection","world_pressure":55,"grave_basis":"immediate_physical_threat","blocking":[],"positive_factors":{"instigation":22.5,"vengefulness":7.140000000000001,"directed_emotion":21.643600000000003,"commitment":0.0,"sadism":0.0,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":14.3,"moral_restraint":8.52,"fear":5.584,"risk":4.342569097937705,"bond":0.0,"authority_or_witnesses":7.5,"uncertain_authorship":0.0,"available_nonlethal_alternative":10},"decision_id":285945,"rumination":100,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{"pressure":83.92,"cause":{"severity":55,"facts":[292261,293268,294227],"confidence":100,"mode":"protective","causes":["immediate_physical_threat"]}}},{"system":"lethal_decision","function":"lethal_decisions.LethalDecisionSystem.evaluate","result":{"available":true,"pressure":83.92,"mode":"protective","confidence":100,"known_facts":[292261,293268,294227],"source_fact":294227,"commitment_id":null,"motive":"protection","world_pressure":55,"grave_basis":"immediate_physical_threat","blocking":[],"positive_factors":{"instigation":22.5,"vengefulness":7.140000000000001,"directed_emotion":21.643600000000003,"commitment":0.0,"sadism":0.0,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":14.3,"moral_restraint":8.52,"fear":5.584,"risk":4.342569097937705,"bond":0.0,"authority_or_witnesses":7.5,"uncertain_authorship":0.0,"available_nonlethal_alternative":10},"decision_id":285945,"rumination":100,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{"pressure":83.92,"cause":{"severity":55,"facts":[292261,293268,294227],"confidence":100,"mode":"protective","causes":["immediate_physical_threat"]}}},{"system":"lethal_pressure","function":"lethality.LethalPressure.evaluate","result":{"available":true,"pressure":83.92,"mode":"protective","confidence":100,"known_facts":[292261,293268,294227],"source_fact":294227,"commitment_id":null,"motive":"protection","world_pressure":55,"grave_basis":"immediate_physical_threat","blocking":[],"positive_factors":{"instigation":22.5,"vengefulness":7.140000000000001,"directed_emotion":21.643600000000003,"commitment":0.0,"sadism":0.0,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":14.3,"moral_restraint":8.52,"fear":5.584,"risk":4.342569097937705,"bond":0.0,"authority_or_witnesses":7.5,"uncertain_authorship":0.0,"available_nonlethal_alternative":10},"decision_id":285945,"rumination":100,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{}}].

| Evento/hora | Actor→target | Emissor | Testemunhas | Contexto |
| --- | --- | --- | --- | --- |
| 315656 / 249 / CharacterAttacked | 3851→3877 | ["conflicts.ConflictSystem.execute","goals.GoalSystem._execute","goals.GoalSystem.execute"] | [636,642,3851,3854,3877] | {"damage":3,"weapon_id":null,"intended_target":3877,"source_fact":282721,"lawful":false,"self_defense":false,"violence_intent":"kill","post_incapacity":false,"victim_profession":"comerciante","actor_groups":[],"action_audit":{"eligible":true,"world_pressure":55,"action_pressure":22.44,"eligibility_causes":["immediate_physical_threat"],"source_facts":[292261,293268,294227],"capacity":44.35,"perceived_capacity":44.35,"major_barriers":[],"decision_id":285945,"selected_alternative":"attack"},"lethal_audit":{"available":true,"pressure":83.92,"mode":"protective","confidence":100,"known_facts":[292261,293268,294227],"source_fact":294227,"commitment_id":null,"motive":"protection","world_pressure":55,"grave_basis":"immediate_physical_threat","blocking":[],"positive_factors":{"instigation":22.5,"vengefulness":7.140000000000001,"directed_emotion":21.643600000000003,"commitment":0.0,"sadism":0.0,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":14.3,"moral_restraint":8.52,"fear":5.584,"risk":4.342569097937705,"bond":0.0,"authority_or_witnesses":7.5,"uncertain_authorship":0.0,"available_nonlethal_alternative":10},"decision_id":285945,"rumination":100,"current_commitment_strength":0,"commitment_intensity":0}} |

**Aprendizado aceito durante a decisão (amostra):** [{"npc":636,"event":315656,"kind":"CharacterAttacked","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":642,"event":315656,"kind":"CharacterAttacked","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":3851,"event":315656,"kind":"CharacterAttacked","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":3854,"event":315656,"kind":"CharacterAttacked","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":3877,"event":315656,"kind":"CharacterAttacked","source":null,"firsthand":true,"confidence":100,"latency":0}].

**Recibos posteriores ligados ao mesmo event_id:** [{"event":315656,"kind":"CharacterAttacked","learned":{"count":5,"first":249,"last":249,"first_people":[636,642,3851,3854,3877]}}]. Contagem é operações de aprendizado aceitas, não indivíduos únicos.

**Consequência imediata:** {"id":3851,"name":"Aldren Alvor","hour":249,"alive":true,"profession":"lenhador","lod":"active","position":{"map_id":630,"x":3,"y":5},"residence":630,"hp":84,"hunger":34,"thirst":48,"fatigue":70.80000000000008,"money":9,"food":0,"water":1,"local_food":66,"local_water":152,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{}}. **Observação/relações com o alvo ao final:** {"observation_end":{"turn":249,"position":{"map_id":630,"x":3,"y":5},"hunger":60,"thirst":57,"health":53,"alive":true,"profession":"comerciante","weapon_power":4,"injured":48},"relations_end":[]}. Não usar esse estado posterior como entrada antiga nem atribuir consequências futuras sem vínculo causal.

### 12. migration — Iria Alvor #3177, h26: buy_food

**Pressão escolhida:** `migration` #31498, prioridade 54.7, base 52, fonte `known_towns`, alvo 302. Motivo: Considerar mudança por threat.

**Contexto preservado:** {"reason":"threat"}.

**Entrada:** {"id":3177,"name":"Iria Alvor","hour":26,"alive":true,"profession":"cozinheiro","lod":"local","position":{"map_id":479,"x":5,"y":9},"residence":479,"hp":100,"hunger":19,"thirst":52,"fatigue":50.20000000000004,"money":15,"food":1,"water":0,"local_food":152,"local_water":144,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{"organize":32}}.

**Personalidade:** {"honesty":77,"compassion":8,"courage":76,"independence":75,"greed":26,"diligence":49,"family_loyalty":40,"persistence":56,"temperament":77,"vengefulness":21,"ambition":44,"sadism":3}. **Emoções escalares de entrada:** {"anger":0.0,"resentment":0.0,"humiliation":0.0,"desperation":0.0,"last_updated":23,"last_support":-10000,"strain":0,"adaptation":0,"last_adapted":0,"stable_material_hours":0,"nested_collections":"LACUNA: cópia rasa; histórico não utilizado"}.

**Conhecimento/locais de entrada:** {"known_places":{"market":{"map_id":479,"x":5,"y":9},"home":{"map_id":479,"x":2,"y":2},"work":{"map_id":479,"x":5,"y":9},"forage":{"map_id":479,"x":1,"y":9},"well_home":{"map_id":479,"x":2,"y":2},"well_rural":{"map_id":479,"x":1,"y":9},"sacred":{"map_id":479,"x":5,"y":1}},"known_towns":[479,302],"route_knowledge_count":2,"knowledge_ids_before":[50824,51495,51496,51504,51506,51510,51517,52300,52302,52303,52304,52305,52306,53061,53063,53064,53068,53077,53082,53807,53808,53810,53811,53812,53813,53814,53816,53817,53823,53825,54443,54448,54450,54452,54453,54454,54455,54456,54463,54465,54469,54470,54472,54473,54474,55185,55854,55856,55862,55866,43816,56767,56894,57508,58176,58178,58181,58183,58185,58828,58830,58832,58835,60081],"market_observation":{"turn":23,"town_id":479,"stock":{"food":157,"grain":89,"water":74,"iron":120,"wood":86},"temporary_work":false,"offers_expire_at":47,"training_offer":null,"price":2,"price_turn":23}}.

**Fatos-fonte retidos após percepção:** [].

| Need | ID/alvo | Base→prioridade | Estado/fonte |
| --- | --- | --- | --- |
| political_pressure | 31499/None | 61.6→70.00351428571427 | active / own_shared_problem |
| migration | 31498/302 | 52→54.7 | active / known_towns |
| protection | 26781/3177 | 45→54.55 | blocked / event:31514 |
| water | 41918/None | 52→53.8 | active / physiology |
| rest | 31496/None | 50.20000000000004→52.90000000000004 | active / physiology |
| food_reserve | 21280/None | 33.8→37.8 | active / food_reserve |

**Alternativas/gates realmente vistos:**

Need #31499 (`political_pressure`): 1 Solutions entraram em _evaluate; 0 saíram disponíveis. Entrada: `organize`.

| Opção | Alvo | Etapa | Motivo observado | Auditoria/feeding |
| --- | --- | --- | --- | --- |
| organize | None | before_Utility_or_unresolved | cooldown_after_failure | {"pressure":null,"feeding":null} |

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |

Need #31498 (`migration`): 1 Solutions entraram em _evaluate; 1 saíram disponíveis. Entrada: `buy_food`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| buy_food | {"target":null,"destination":{"map_id":479,"x":5,"y":9}} | 90.4 | {"base":0.375,"honesty":0.077,"travel":-0.0} | {"feeding":null,"action_pressure":null} |

Need #26781 (`protection`): 2 Solutions entraram em _evaluate; 2 saíram disponíveis. Entrada: `ask_personal_help, ask_personal_help`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| ask_personal_help | {"target":3174,"destination":null} | 27.999999999999996 | {"base":0.125,"independence":-0.1125,"compassion":0.008,"trust":0.105,"reputation":0.0,"relationship":0.014499999999999999,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| ask_personal_help | {"target":3180,"destination":null} | 24.3 | {"base":0.125,"independence":-0.1125,"compassion":0.008,"trust":0.0805,"reputation":0.0,"relationship":0.020499999999999997,"travel":-0.0} | {"feeding":null,"action_pressure":null} |

**Escolhas intermediárias:** [{"chosen":{"action":"buy_food","score":90.4,"target":null,"destination":{"map_id":479,"x":5,"y":9},"terms":{"base":0.375,"honesty":0.077,"travel":-0.0},"feeding":null,"action_pressure":null},"near_scores":[90.4],"variation_draws":"não capturados; RNG não consultado pelo observador"}].

**Preparação/substituição posterior:** [].

**Winner final / Goal:** {"winner":{"action":"buy_food","score":90.4,"target":null,"destination":{"map_id":479,"x":5,"y":9},"terms":{"base":0.375,"honesty":0.077,"travel":-0.0},"feeding":null,"action_pressure":null},"goal":{"id":60082,"need_id":31498,"action":"buy_food","score":90.4,"created_at":26,"target_id":null,"destination":{"map_id":479,"x":5,"y":9},"status":"completed","outcome":"Compra concluída por 2 moedas."},"suspended_before":null,"suspended_after":null}.

**Por que outras Needs não foram executadas:** a fila prioriza emergência/priority/ID e para na primeira solucionável, sujeita à continuidade/preparo. Outras pressões retidas: political_pressure#31499(70.00351428571427), protection#26781(54.55), water#41918(53.8), rest#31496(52.90000000000004), food_reserve#21280(37.8). Não atribuir score global entre Needs.

**Execução:** {"success":true,"result":[true,"Compra concluída por 2 moedas."],"goal_at_entry":{"id":60082,"need_id":31498,"action":"buy_food","score":90.4,"created_at":26,"target_id":null,"destination":{"map_id":479,"x":5,"y":9},"status":"active","outcome":""},"before":{"id":3177,"name":"Iria Alvor","hour":26,"alive":true,"profession":"cozinheiro","lod":"local","position":{"map_id":479,"x":5,"y":9},"residence":479,"hp":100,"hunger":19,"thirst":52,"fatigue":50.20000000000004,"money":15,"food":1,"water":0,"local_food":152,"local_water":144,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{"organize":32}},"after":{"id":3177,"name":"Iria Alvor","hour":26,"alive":true,"profession":"cozinheiro","lod":"local","position":{"map_id":479,"x":5,"y":9},"residence":479,"hp":100,"hunger":19,"thirst":52,"fatigue":50.20000000000004,"money":13,"food":2,"water":0,"local_food":151,"local_water":144,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{"organize":32}}}.

**Cálculos especializados reais:** [{"system":"lethal_decision","function":"lethal_decisions.LethalDecisionSystem.evaluate","result":{"available":false,"pressure":-59.3,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"protection","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":3.5700000000000003,"directed_emotion":0.0,"commitment":0.0,"sadism":0.39,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":4.4,"moral_restraint":9.24,"fear":0.0,"risk":4.615384615384615,"bond":0.0,"authority_or_witnesses":15,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{"pressure":-59.3,"cause":{"severity":0,"grave":false,"causes":[],"facts":[],"confidence":0,"mode":"retributive","confirmed_injury":0}}},{"system":"lethal_decision","function":"lethal_decisions.LethalDecisionSystem.evaluate","result":{"available":false,"pressure":-59.3,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"protection","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":3.5700000000000003,"directed_emotion":0.0,"commitment":0.0,"sadism":0.39,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":4.4,"moral_restraint":9.24,"fear":0.0,"risk":4.615384615384615,"bond":0.0,"authority_or_witnesses":15,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{"pressure":-59.3,"cause":{"severity":0,"grave":false,"causes":[],"facts":[],"confidence":0,"mode":"retributive","confirmed_injury":0}}},{"system":"lethal_pressure","function":"lethality.LethalPressure.evaluate","result":{"available":false,"pressure":-59.3,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"protection","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":3.5700000000000003,"directed_emotion":0.0,"commitment":0.0,"sadism":0.39,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":4.4,"moral_restraint":9.24,"fear":0.0,"risk":4.615384615384615,"bond":0.0,"authority_or_witnesses":15,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{}}].

| Evento/hora | Actor→target | Emissor | Testemunhas | Contexto |
| --- | --- | --- | --- | --- |
| 60084 / 26 / ItemBought | 3177→479 | ["economy.Economy.buy","goals.GoalSystem._execute","goals.GoalSystem.execute"] | [485,488,497,500,502,505,3166,3171,3174,3177,3180,3186,3189,3197,3200,3206,3212,3217,3220,3223,3235,3237,3246,3249,3260,3269,3272,3281,3298] | {} |

**Aprendizado aceito durante a decisão (amostra):** [{"npc":485,"event":60084,"kind":"ItemBought","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":488,"event":60084,"kind":"ItemBought","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":497,"event":60084,"kind":"ItemBought","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":500,"event":60084,"kind":"ItemBought","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":502,"event":60084,"kind":"ItemBought","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":505,"event":60084,"kind":"ItemBought","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":3166,"event":60084,"kind":"ItemBought","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":3171,"event":60084,"kind":"ItemBought","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":3174,"event":60084,"kind":"ItemBought","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":3177,"event":60084,"kind":"ItemBought","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":3180,"event":60084,"kind":"ItemBought","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":3186,"event":60084,"kind":"ItemBought","source":null,"firsthand":true,"confidence":100,"latency":0}].

**Recibos posteriores ligados ao mesmo event_id:** [{"event":60084,"kind":"ItemBought","learned":{"count":30,"first":26,"last":54,"first_people":[485,488,497,500,502,505]}}]. Contagem é operações de aprendizado aceitas, não indivíduos únicos.

**Consequência imediata:** {"id":3177,"name":"Iria Alvor","hour":26,"alive":true,"profession":"cozinheiro","lod":"local","position":{"map_id":479,"x":5,"y":9},"residence":479,"hp":100,"hunger":19,"thirst":52,"fatigue":50.20000000000004,"money":13,"food":2,"water":0,"local_food":151,"local_water":144,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{"organize":32}}. **Observação/relações com o alvo ao final:** {"observation_end":null,"relations_end":[]}. Não usar esse estado posterior como entrada antiga nem atribuir consequências futuras sem vínculo causal.

### 13. money — Mira Arven #295, h28: work

**Pressão escolhida:** `money` #13541, prioridade 64.56666666666666, base 49.166666666666664, fonte `economy`, alvo None. Motivo: Reservas financeiras baixas.

**Contexto preservado:** {}.

**Entrada:** {"id":295,"name":"Mira Arven","hour":28,"alive":true,"profession":"conselheiro","lod":"active","position":{"map_id":3,"x":7,"y":13},"residence":3,"hp":100,"hunger":29,"thirst":56,"fatigue":47.60000000000002,"money":1,"food":2,"water":0,"local_food":78,"local_water":118,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{"organize":39}}.

**Personalidade:** {"honesty":79,"compassion":21,"courage":77,"independence":37,"greed":45,"diligence":56,"family_loyalty":55,"persistence":80,"temperament":93,"vengefulness":62,"ambition":11,"sadism":1}. **Emoções escalares de entrada:** {"anger":2.099999999999998,"resentment":9.780000000000001,"humiliation":1.200000000000001,"desperation":0.0,"last_updated":27,"last_support":27,"strain":0,"adaptation":0,"last_adapted":0,"stable_material_hours":0,"nested_collections":"LACUNA: cópia rasa; histórico não utilizado"}.

**Conhecimento/locais de entrada:** {"known_places":{"market":{"map_id":3,"x":7,"y":13},"home":{"map_id":3,"x":2,"y":2},"work":{"map_id":3,"x":7,"y":13},"forage":{"map_id":3,"x":1,"y":13},"well_home":{"map_id":3,"x":2,"y":2},"well_rural":{"map_id":3,"x":1,"y":13},"sacred":{"map_id":3,"x":7,"y":1}},"known_towns":[3,50,115,162,227],"route_knowledge_count":8,"knowledge_ids_before":[58329,58330,58332,58336,58337,58338,58340,58341,58342,58346,58347,58348,58349,58350,58351,58352,58354,58355,58358,59406,59409,59417,59445,59578,59585,59590,59593,59599,59600,59601,59604,59607,59611,59614,59627,59633,59635,59637,59642,59646,59647,59648,59650,60749,60753,60884,60885,60887,60888,60891,60901,60903,60908,60909,60910,60911,60919,60932,60936,60937,60938,60940,60941,61885],"market_observation":{"turn":27,"town_id":3,"stock":{"food":74,"grain":88,"water":127,"iron":92,"wood":34},"temporary_work":true,"offers_expire_at":51,"training_offer":null,"price":2,"price_turn":27}}.

**Fatos-fonte retidos após percepção:** [{"event_id":59406,"kind":"ItemStolen","actor_id":9,"target_id":3,"location":{"map_id":3,"x":7,"y":13},"turn":26,"description":"Elena Solaris roubou comida no mercado de Dorria.","confidence":100,"required_trust":0,"source_id":null,"source_kind":"direct","context":{"item_id":59405,"item_kind":"food"}}].

| Need | ID/alvo | Base→prioridade | Estado/fonte |
| --- | --- | --- | --- |
| political_pressure | 32470/None | 56.65→64.7696 | active / own_shared_problem |
| money | 13541/None | 49.166666666666664→64.56666666666666 | active / economy |
| water | 42894/None | 56→57.95 | active / physiology |
| migration | 32469/115 | 52→54.85 | active / known_towns |
| rest | 37622/None | 47.60000000000002→50.00000000000002 | active / physiology |
| protection | 30367/295 | 30→41.467 | active / event:59406 |

**Alternativas/gates realmente vistos:**

Need #32470 (`political_pressure`): 1 Solutions entraram em _evaluate; 0 saíram disponíveis. Entrada: `organize`.

| Opção | Alvo | Etapa | Motivo observado | Auditoria/feeding |
| --- | --- | --- | --- | --- |
| organize | None | before_Utility_or_unresolved | cooldown_after_failure | {"pressure":null,"feeding":null} |

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |

Need #13541 (`money`): 1 Solutions entraram em _evaluate; 1 saíram disponíveis. Entrada: `work`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| work | {"target":null,"destination":{"map_id":3,"x":7,"y":13}} | 78.0 | {"base":0.25,"diligence":0.14,"physical_depletion":0.0,"travel":-0.0} | {"feeding":null,"action_pressure":null} |

Need #30367 (`protection`): 27 Solutions entraram em _evaluate; 27 saíram disponíveis. Entrada: `denounce, denounce, denounce, denounce, denounce, denounce, denounce, denounce, denounce, denounce, denounce, denounce, ask_personal_help, ask_personal_help, confront, threaten, demand_return, warn, insult, call_help, calm, withdraw, flee, defend, forgive, apologize, surrender`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| denounce | {"target":26,"destination":{"map_id":3,"x":7,"y":13}} | 99.1 | {"base":0.225,"honesty":0.13825,"vengefulness":0.062,"courage":0.05775,"trust":0.0125,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| denounce | {"target":1218,"destination":{"map_id":3,"x":7,"y":13}} | 99.1 | {"base":0.225,"honesty":0.13825,"vengefulness":0.062,"courage":0.05775,"trust":0.0125,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| denounce | {"target":1241,"destination":{"map_id":3,"x":7,"y":13}} | 99.1 | {"base":0.225,"honesty":0.13825,"vengefulness":0.062,"courage":0.05775,"trust":0.0125,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| denounce | {"target":1264,"destination":{"map_id":3,"x":7,"y":13}} | 99.1 | {"base":0.225,"honesty":0.13825,"vengefulness":0.062,"courage":0.05775,"trust":0.0125,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| denounce | {"target":1287,"destination":{"map_id":3,"x":7,"y":13}} | 99.1 | {"base":0.225,"honesty":0.13825,"vengefulness":0.062,"courage":0.05775,"trust":0.0125,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| denounce | {"target":1310,"destination":{"map_id":3,"x":7,"y":13}} | 99.1 | {"base":0.225,"honesty":0.13825,"vengefulness":0.062,"courage":0.05775,"trust":0.0125,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| denounce | {"target":1333,"destination":{"map_id":3,"x":7,"y":13}} | 99.1 | {"base":0.225,"honesty":0.13825,"vengefulness":0.062,"courage":0.05775,"trust":0.0125,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| denounce | {"target":1356,"destination":{"map_id":3,"x":7,"y":13}} | 99.1 | {"base":0.225,"honesty":0.13825,"vengefulness":0.062,"courage":0.05775,"trust":0.0125,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| denounce | {"target":1379,"destination":{"map_id":3,"x":7,"y":13}} | 99.1 | {"base":0.225,"honesty":0.13825,"vengefulness":0.062,"courage":0.05775,"trust":0.0125,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| denounce | {"target":1402,"destination":{"map_id":3,"x":7,"y":13}} | 99.1 | {"base":0.225,"honesty":0.13825,"vengefulness":0.062,"courage":0.05775,"trust":0.0125,"travel":-0.0} | {"feeding":null,"action_pressure":null} |

**Escolhas intermediárias:** [{"chosen":{"action":"work","score":78.0,"target":null,"destination":{"map_id":3,"x":7,"y":13},"terms":{"base":0.25,"diligence":0.14,"physical_depletion":0.0,"travel":-0.0},"feeding":null,"action_pressure":null},"near_scores":[78.0],"variation_draws":"não capturados; RNG não consultado pelo observador"}].

**Preparação/substituição posterior:** [].

**Winner final / Goal:** {"winner":{"action":"work","score":78.0,"target":null,"destination":{"map_id":3,"x":7,"y":13},"terms":{"base":0.25,"diligence":0.14,"physical_depletion":0.0,"travel":-0.0},"feeding":null,"action_pressure":null},"goal":{"id":61886,"need_id":13541,"action":"work","score":78.0,"created_at":28,"target_id":null,"destination":{"map_id":3,"x":7,"y":13},"status":"completed","outcome":"Serviço realizado."},"suspended_before":null,"suspended_after":null}.

**Por que outras Needs não foram executadas:** a fila prioriza emergência/priority/ID e para na primeira solucionável, sujeita à continuidade/preparo. Outras pressões retidas: political_pressure#32470(64.7696), water#42894(57.95), migration#32469(54.85), rest#37622(50.00000000000002), protection#30367(41.467). Não atribuir score global entre Needs.

**Execução:** {"success":true,"result":[true,"Serviço realizado."],"goal_at_entry":{"id":61886,"need_id":13541,"action":"work","score":78.0,"created_at":28,"target_id":null,"destination":{"map_id":3,"x":7,"y":13},"status":"active","outcome":""},"before":{"id":295,"name":"Mira Arven","hour":28,"alive":true,"profession":"conselheiro","lod":"active","position":{"map_id":3,"x":7,"y":13},"residence":3,"hp":100,"hunger":29,"thirst":56,"fatigue":47.60000000000002,"money":1,"food":2,"water":0,"local_food":78,"local_water":118,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{"organize":39}},"after":{"id":295,"name":"Mira Arven","hour":28,"alive":true,"profession":"conselheiro","lod":"active","position":{"map_id":3,"x":7,"y":13},"residence":3,"hp":100,"hunger":29,"thirst":56,"fatigue":47.60000000000002,"money":2,"food":2,"water":0,"local_food":78,"local_water":118,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{"organize":39}}}.

**Cálculos especializados reais:** [{"system":"lethal_decision","function":"lethal_decisions.LethalDecisionSystem.evaluate","result":{"available":false,"pressure":-56.06,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"protection","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":10.540000000000001,"directed_emotion":1.2693999999999999,"commitment":0.0,"sadism":0.13,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":11.55,"moral_restraint":9.48,"fear":0.0,"risk":1.9718599157851497,"bond":0.0,"authority_or_witnesses":15,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{"pressure":-56.06,"cause":{"severity":0,"grave":false,"causes":[],"facts":[],"confidence":0,"mode":"retributive","confirmed_injury":0}}},{"system":"lethal_decision","function":"lethal_decisions.LethalDecisionSystem.evaluate","result":{"available":false,"pressure":-56.06,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"protection","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":10.540000000000001,"directed_emotion":1.2693999999999999,"commitment":0.0,"sadism":0.13,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":11.55,"moral_restraint":9.48,"fear":0.0,"risk":1.9718599157851497,"bond":0.0,"authority_or_witnesses":15,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{"pressure":-56.06,"cause":{"severity":0,"grave":false,"causes":[],"facts":[],"confidence":0,"mode":"retributive","confirmed_injury":0}}},{"system":"lethal_pressure","function":"lethality.LethalPressure.evaluate","result":{"available":false,"pressure":-56.06,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"protection","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":10.540000000000001,"directed_emotion":1.2693999999999999,"commitment":0.0,"sadism":0.13,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":11.55,"moral_restraint":9.48,"fear":0.0,"risk":1.9718599157851497,"bond":0.0,"authority_or_witnesses":15,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{}},{"system":"work","actual":{"actor":295,"town":3,"money_before":1,"treasury_before":1490,"inputs_before":{"food":78,"grain":84,"iron":92,"wood":34},"result":{"status":"paid","message":"Serviço realizado.","produced":0,"paid":1,"credit_added":6}}}].

**Evento:** nenhum evento retido durante esta decisão. Isso pode significar movimento/efeito sem evento; não implica falha.

**Aprendizado aceito durante a decisão (amostra):** [].

**Recibos posteriores ligados ao mesmo event_id:** []. Contagem é operações de aprendizado aceitas, não indivíduos únicos.

**Consequência imediata:** {"id":295,"name":"Mira Arven","hour":28,"alive":true,"profession":"conselheiro","lod":"active","position":{"map_id":3,"x":7,"y":13},"residence":3,"hp":100,"hunger":29,"thirst":56,"fatigue":47.60000000000002,"money":2,"food":2,"water":0,"local_food":78,"local_water":118,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{"organize":39}}. **Observação/relações com o alvo ao final:** {"observation_end":null,"relations_end":[]}. Não usar esse estado posterior como entrada antiga nem atribuir consequências futuras sem vínculo causal.

### 14. policy — Lyra Alvor #887, h28: policy_work

**Pressão escolhida:** `institutional_work` #61964, prioridade 48.0, base 48, fonte `known_policy`, alvo 61662. Motivo: Cumprir trabalho financiado conhecido.

**Contexto preservado:** {}.

**Entrada:** {"id":887,"name":"Lyra Alvor","hour":28,"alive":true,"profession":"guarda","lod":"active","position":{"map_id":864,"x":7,"y":13},"residence":864,"hp":100,"hunger":30,"thirst":16,"fatigue":34.599999999999994,"money":32,"food":2,"water":0,"local_food":219,"local_water":129,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{}}.

**Personalidade:** {"honesty":18,"compassion":66,"courage":38,"independence":26,"greed":62,"diligence":79,"family_loyalty":76,"persistence":15,"temperament":67,"vengefulness":35,"ambition":79,"sadism":0}. **Emoções escalares de entrada:** {"anger":0.0,"resentment":0.0,"humiliation":0.0,"desperation":0.0,"last_updated":27,"last_support":-10000,"strain":0,"adaptation":0,"last_adapted":0,"stable_material_hours":0,"nested_collections":"LACUNA: cópia rasa; histórico não utilizado"}.

**Conhecimento/locais de entrada:** {"known_places":{"market":{"map_id":864,"x":7,"y":13},"home":{"map_id":864,"x":2,"y":2},"work":{"map_id":864,"x":7,"y":13},"forage":{"map_id":864,"x":1,"y":13},"well_home":{"map_id":864,"x":2,"y":2},"well_rural":{"map_id":864,"x":1,"y":13},"sacred":{"map_id":864,"x":7,"y":1}},"known_towns":[864,911,976,1023],"route_knowledge_count":6,"knowledge_ids_before":[57887,57889,57894,57895,57897,57898,57899,57900,57903,59179,59181,59185,59186,59187,59188,59192,59194,59195,59196,59204,59210,59212,59214,59216,59218,59220,59227,59230,59539,59541,60482,60483,60486,60489,60490,60492,60493,60494,60495,60496,60498,60500,60501,60502,60504,60505,60506,60508,60510,60511,60520,60880,61632,61634,61639,61640,61645,61648,61658,61663,61664,61665,61670,61963],"market_observation":{"turn":27,"town_id":864,"stock":{"food":215,"grain":52,"water":139,"iron":68,"wood":120},"temporary_work":true,"offers_expire_at":51,"training_offer":null,"price":2,"price_turn":27}}.

**Fatos-fonte retidos após percepção:** [].

| Need | ID/alvo | Base→prioridade | Estado/fonte |
| --- | --- | --- | --- |
| institutional_work | 61964/61662 | 48→48.0 | active / known_policy |
| advancement | 16861/None | 15→38.8 | selected / self_assessment:1 |
| rest | 52371/None | 34.599999999999994→35.64999999999999 | active / physiology |

**Alternativas/gates realmente vistos:**

Need #61964 (`institutional_work`): 1 Solutions entraram em _evaluate; 1 saíram disponíveis. Entrada: `policy_work`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| policy_work | {"target":61662,"destination":{"map_id":864,"x":7,"y":13}} | 84.75 | {"base":0.325,"diligence":0.09875,"financial_pressure":0.0,"travel":-0.0} | {"feeding":null,"action_pressure":null} |

Need #16861 (`advancement`): 2 Solutions entraram em _evaluate; 2 saíram disponíveis. Entrada: `work, steal_person`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| work | {"target":null,"destination":{"map_id":864,"x":7,"y":13}} | 89.5 | {"base":0.25,"diligence":0.1975,"physical_depletion":0.0,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| steal_person | {"target":885,"destination":null} | 35.00748429591837 | {"base":0.31,"greed":0.124,"honesty":-0.081,"authority":-0.2,"courage":0.019,"travel":-0.0,"pressure_moral_tolerance":0.0030374214795918374} | {"feeding":null,"action_pressure":null} |

**Escolhas intermediárias:** [{"chosen":{"action":"policy_work","score":84.75,"target":61662,"destination":{"map_id":864,"x":7,"y":13},"terms":{"base":0.325,"diligence":0.09875,"financial_pressure":0.0,"travel":-0.0},"feeding":null,"action_pressure":null},"near_scores":[84.75],"variation_draws":"não capturados; RNG não consultado pelo observador"}].

**Preparação/substituição posterior:** [].

**Winner final / Goal:** {"winner":{"action":"policy_work","score":84.75,"target":61662,"destination":{"map_id":864,"x":7,"y":13},"terms":{"base":0.325,"diligence":0.09875,"financial_pressure":0.0,"travel":-0.0},"feeding":null,"action_pressure":null},"goal":{"id":61965,"need_id":61964,"action":"policy_work","score":84.75,"created_at":28,"target_id":61662,"destination":{"map_id":864,"x":7,"y":13},"status":"completed","outcome":"Trabalho real e salário do orçamento reservado."},"suspended_before":null,"suspended_after":null}.

**Por que outras Needs não foram executadas:** a fila prioriza emergência/priority/ID e para na primeira solucionável, sujeita à continuidade/preparo. Outras pressões retidas: advancement#16861(38.8), rest#52371(35.64999999999999). Não atribuir score global entre Needs.

**Execução:** {"success":true,"result":[true,"Trabalho real e salário do orçamento reservado."],"goal_at_entry":{"id":61965,"need_id":61964,"action":"policy_work","score":84.75,"created_at":28,"target_id":61662,"destination":{"map_id":864,"x":7,"y":13},"status":"active","outcome":""},"before":{"id":887,"name":"Lyra Alvor","hour":28,"alive":true,"profession":"guarda","lod":"active","position":{"map_id":864,"x":7,"y":13},"residence":864,"hp":100,"hunger":30,"thirst":16,"fatigue":34.599999999999994,"money":32,"food":2,"water":0,"local_food":219,"local_water":129,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{}},"after":{"id":887,"name":"Lyra Alvor","hour":28,"alive":true,"profession":"guarda","lod":"active","position":{"map_id":864,"x":7,"y":13},"residence":864,"hp":100,"hunger":30,"thirst":16,"fatigue":36.599999999999994,"money":33,"food":2,"water":0,"local_food":219,"local_water":129,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{}}}.

**Cálculos especializados reais:** [].

| Evento/hora | Actor→target | Emissor | Testemunhas | Contexto |
| --- | --- | --- | --- | --- |
| 61966 / 28 / PolicyEffect | 887→61662 | ["institutions.Institutions.emit","institutions.Institutions.policy_work","institutions.Institutions.execute"] | [873,885,887,1153,1156,1159,4679,4688,4691,4694,4705,4717,4740,4742,4757,4765,4774,4786,4788,4791,4794,4797,4803,4806,4809,4811,4820,4823,4826,4829,4832,4843,4855,4857,4863,4866,4875,4878,4880,4892,4895,4901,4906,4909,4912,4921,4924,4926,4935] | {"policy_id":61662,"proposal_id":57845,"sector":"SECURITY","effect":{"patrol":887,"observed_place":{"map_id":864,"x":7,"y":13}},"materials":{},"wage":1,"remaining_budget":6,"work_done":2} |

**Aprendizado aceito durante a decisão (amostra):** [{"npc":873,"event":61966,"kind":"PolicyEffect","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":885,"event":61966,"kind":"PolicyEffect","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":887,"event":61966,"kind":"PolicyEffect","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":1153,"event":61966,"kind":"PolicyEffect","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":1156,"event":61966,"kind":"PolicyEffect","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":1159,"event":61966,"kind":"PolicyEffect","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":4679,"event":61966,"kind":"PolicyEffect","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":4688,"event":61966,"kind":"PolicyEffect","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":4691,"event":61966,"kind":"PolicyEffect","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":4694,"event":61966,"kind":"PolicyEffect","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":4705,"event":61966,"kind":"PolicyEffect","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":4717,"event":61966,"kind":"PolicyEffect","source":null,"firsthand":true,"confidence":100,"latency":0}].

**Recibos posteriores ligados ao mesmo event_id:** [{"event":61966,"kind":"PolicyEffect","learned":{"count":50,"first":28,"last":54,"first_people":[873,885,887,1153,1156,1159]}}]. Contagem é operações de aprendizado aceitas, não indivíduos únicos.

**Consequência imediata:** {"id":887,"name":"Lyra Alvor","hour":28,"alive":true,"profession":"guarda","lod":"active","position":{"map_id":864,"x":7,"y":13},"residence":864,"hp":100,"hunger":30,"thirst":16,"fatigue":36.599999999999994,"money":33,"food":2,"water":0,"local_food":219,"local_water":129,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{}}. **Observação/relações com o alvo ao final:** {"observation_end":null,"relations_end":[]}. Não usar esse estado posterior como entrada antiga nem atribuir consequências futuras sem vínculo causal.

### 15. proposal — Iria Alvor #4213, h114: submit_proposal

**Pressão escolhida:** `organizational_survival` #61517, prioridade 66.140304, base 53.496500000000005, fonte `group:57703`, alvo 4213. Motivo: Participar da organização conhecida.

**Contexto preservado:** {"group_id":57703,"known_location":{"map_id":695,"x":5,"y":9}}.

**Entrada:** {"id":4213,"name":"Iria Alvor","hour":114,"alive":true,"profession":"ferreiro","lod":"local","position":{"map_id":695,"x":5,"y":9},"residence":695,"hp":100,"hunger":54,"thirst":48,"fatigue":60.8000000000002,"money":2,"food":2,"water":0,"local_food":40,"local_water":104,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{}}.

**Personalidade:** {"honesty":34,"compassion":52,"courage":6,"independence":29,"greed":43,"diligence":53,"family_loyalty":39,"persistence":26,"temperament":9,"vengefulness":38,"ambition":20,"sadism":46}. **Emoções escalares de entrada:** {"anger":26.999999999999993,"resentment":18.60000000000001,"humiliation":14.999999999999996,"desperation":0.0,"last_updated":111,"last_support":-10000,"strain":0,"adaptation":0,"last_adapted":0,"stable_material_hours":0,"nested_collections":"LACUNA: cópia rasa; histórico não utilizado"}.

**Conhecimento/locais de entrada:** {"known_places":{"market":{"map_id":695,"x":5,"y":9},"home":{"map_id":695,"x":2,"y":2},"work":{"map_id":695,"x":8,"y":2},"forage":{"map_id":695,"x":1,"y":9},"well_home":{"map_id":695,"x":2,"y":2},"well_rural":{"map_id":695,"x":1,"y":9},"sacred":{"map_id":695,"x":5,"y":1}},"known_towns":[695,601,3],"route_knowledge_count":2,"knowledge_ids_before":[149703,149708,149720,150162,150840,150849,151293,151297,151299,151302,151881,151883,151884,151886,151887,151888,151891,151897,151900,151903,151909,152314,152316,152943,152945,152950,153303,153873,153885,106096,148418,154369,154371,154949,154951,154955,154959,154961,154965,155371,156366,156943,156950,156955,157364,157989,157993,157991,158002,158440,158452,159190,159195,159204,159209,159211,159570,160187,160190,160696,160702,161334,161336,161339],"market_observation":{"turn":111,"town_id":695,"stock":{"food":46,"grain":125,"water":105,"iron":92,"wood":114},"temporary_work":true,"offers_expire_at":135,"training_offer":null,"price":2,"price_turn":111}}.

**Fatos-fonte retidos após percepção:** [{"event_id":157991,"kind":"ItemStolen","actor_id":4204,"target_id":695,"location":{"map_id":695,"x":5,"y":9},"turn":111,"description":"Elena Corven roubou comida no mercado de Silven.","confidence":100,"required_trust":0,"source_id":null,"source_kind":"direct","context":{"item_id":157990,"item_kind":"food"}}].

| Need | ID/alvo | Base→prioridade | Estado/fonte |
| --- | --- | --- | --- |
| organizational_survival | 61517/4213 | 53.496500000000005→66.140304 | active / group:57703 |
| rest | 28556/None | 60.8000000000002→65.1500000000002 | active / physiology |
| protection | 53252/4213 | 45→63.184000000000005 | active / event:157991 |
| political_pressure | 57699/None | 58.0→63.1174 | active / own_shared_problem |
| money | 125508/None | 47.291666666666664→62.541666666666664 | active / economy |
| food | 28555/None | 61.0→62.35 | active / physiology |
| migration | 57698/601 | 52→53.35 | active / known_towns |
| water | 48832/None | 48→49.35 | active / physiology |
| advancement | 15525/None | 19.1568→32.156800000000004 | active / aspiration:wealth |
| religious_interest | 15526/5908 | 22.5→31.8692 | active / own_faith |

**Alternativas/gates realmente vistos:**

Need #61517 (`organizational_survival`): 1 Solutions entraram em _evaluate; 1 saíram disponíveis. Entrada: `submit_proposal`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| submit_proposal | {"target":61519,"destination":{"map_id":695,"x":5,"y":9}} | 87.22749999999999 | {"base":0.35,"ambition":0.025,"persistence":0.026000000000000002,"travel":-0.0,"action_pressure":0.0351375} | {"feeding":null,"action_pressure":{"eligible":true,"world_pressure":55,"action_pressure":28.11,"eligibility_causes":["shared_problem"],"source_facts":[60826,61481,61506],"capacity":59.47,"perceived_capacity":38.54,"major_barriers":[],"selected_alternative":"submit_proposal"}} |

Need #53252 (`protection`): 11 Solutions entraram em _evaluate; 11 saíram disponíveis. Entrada: `denounce, denounce, denounce, denounce, denounce, denounce, denounce, denounce, denounce, avoid_threat, pursue`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| pursue | {"target":4204,"destination":{"map_id":695,"x":5,"y":9}} | 71.80502087717639 | {"base":0.275,"courage":0.006,"diligence":0.03975,"vengefulness":0.038,"critical_depletion":0.0,"travel":-0.0,"action_pressure":0.0,"pressure_risk_tolerance":0.00027510438588193554} | {"feeding":null,"action_pressure":{"eligible":true,"world_pressure":0,"action_pressure":0.0,"eligibility_causes":[],"source_facts":[],"capacity":59.47,"perceived_capacity":38.54,"major_barriers":[],"selected_alternative":"pursue"}} |
| denounce | {"target":624,"destination":{"map_id":695,"x":5,"y":9}} | 67.9 | {"base":0.225,"honesty":0.059500000000000004,"vengefulness":0.038,"courage":0.0045,"trust":0.0125,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| denounce | {"target":718,"destination":{"map_id":695,"x":5,"y":9}} | 67.9 | {"base":0.225,"honesty":0.059500000000000004,"vengefulness":0.038,"courage":0.0045,"trust":0.0125,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| denounce | {"target":4086,"destination":{"map_id":695,"x":5,"y":9}} | 67.9 | {"base":0.225,"honesty":0.059500000000000004,"vengefulness":0.038,"courage":0.0045,"trust":0.0125,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| denounce | {"target":4109,"destination":{"map_id":695,"x":5,"y":9}} | 67.9 | {"base":0.225,"honesty":0.059500000000000004,"vengefulness":0.038,"courage":0.0045,"trust":0.0125,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| denounce | {"target":4132,"destination":{"map_id":695,"x":5,"y":9}} | 67.9 | {"base":0.225,"honesty":0.059500000000000004,"vengefulness":0.038,"courage":0.0045,"trust":0.0125,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| denounce | {"target":4155,"destination":{"map_id":695,"x":5,"y":9}} | 67.9 | {"base":0.225,"honesty":0.059500000000000004,"vengefulness":0.038,"courage":0.0045,"trust":0.0125,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| denounce | {"target":4178,"destination":{"map_id":695,"x":5,"y":9}} | 67.9 | {"base":0.225,"honesty":0.059500000000000004,"vengefulness":0.038,"courage":0.0045,"trust":0.0125,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| denounce | {"target":4201,"destination":{"map_id":695,"x":5,"y":9}} | 67.9 | {"base":0.225,"honesty":0.059500000000000004,"vengefulness":0.038,"courage":0.0045,"trust":0.0125,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| denounce | {"target":4236,"destination":{"map_id":695,"x":5,"y":9}} | 67.9 | {"base":0.225,"honesty":0.059500000000000004,"vengefulness":0.038,"courage":0.0045,"trust":0.0125,"travel":-0.0} | {"feeding":null,"action_pressure":null} |

Need #15525 (`advancement`): 4 Solutions entraram em _evaluate; 4 saíram disponíveis. Entrada: `work, work_for_food, temporary_service, steal_person`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| temporary_service | {"target":null,"destination":{"map_id":695,"x":5,"y":9}} | 63.45 | {"base":0.225,"diligence":0.06625,"compassion":0.026000000000000002,"physical_depletion":0.0,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| work | {"target":null,"destination":{"map_id":695,"x":8,"y":2}} | 56.49999999999999 | {"base":0.25,"diligence":0.1325,"physical_depletion":0.0,"travel":-0.1} | {"feeding":null,"action_pressure":null} |
| work_for_food | {"target":null,"destination":{"map_id":695,"x":1,"y":9}} | 50.25000000000001 | {"base":0.225,"diligence":0.06625,"physical_depletion":0.0,"travel":-0.04} | {"feeding":null,"action_pressure":null} |
| steal_person | {"target":716,"destination":null} | 15.026740807510201 | {"base":0.31,"greed":0.086,"honesty":-0.153,"authority":-0.2,"courage":0.003,"travel":-0.0,"pressure_moral_tolerance":0.029133704037551018} | {"feeding":null,"action_pressure":null} |

**Escolhas intermediárias:** [{"chosen":{"action":"submit_proposal","score":87.22749999999999,"target":61519,"destination":{"map_id":695,"x":5,"y":9},"terms":{"base":0.35,"ambition":0.025,"persistence":0.026000000000000002,"travel":-0.0,"action_pressure":0.0351375},"feeding":null,"action_pressure":{"eligible":true,"world_pressure":55,"action_pressure":28.11,"eligibility_causes":["shared_problem"],"source_facts":[60826,61481,61506],"capacity":59.47,"perceived_capacity":38.54,"major_barriers":[],"selected_alternative":"submit_proposal"}},"near_scores":[87.22749999999999],"variation_draws":"não capturados; RNG não consultado pelo observador"}].

**Preparação/substituição posterior:** [].

**Winner final / Goal:** {"winner":{"action":"submit_proposal","score":87.22749999999999,"target":61519,"destination":{"map_id":695,"x":5,"y":9},"terms":{"base":0.35,"ambition":0.025,"persistence":0.026000000000000002,"travel":-0.0,"action_pressure":0.0351375},"feeding":null,"action_pressure":{"eligible":true,"world_pressure":55,"action_pressure":28.11,"eligibility_causes":["shared_problem"],"source_facts":[60826,61481,61506],"capacity":59.47,"perceived_capacity":38.54,"major_barriers":[],"selected_alternative":"submit_proposal"}},"goal":{"id":161342,"need_id":61517,"action":"submit_proposal","score":87.22749999999999,"created_at":114,"target_id":61519,"destination":{"map_id":695,"x":5,"y":9},"status":"completed","outcome":"Proposta e apoio recebidos presencialmente."},"suspended_before":null,"suspended_after":null}.

**Por que outras Needs não foram executadas:** a fila prioriza emergência/priority/ID e para na primeira solucionável, sujeita à continuidade/preparo. Outras pressões retidas: rest#28556(65.1500000000002), protection#53252(63.184000000000005), political_pressure#57699(63.1174), money#125508(62.541666666666664), food#28555(62.35), migration#57698(53.35), water#48832(49.35), advancement#15525(32.156800000000004), religious_interest#15526(31.8692). Não atribuir score global entre Needs.

**Execução:** {"success":true,"result":[true,"Proposta e apoio recebidos presencialmente."],"goal_at_entry":{"id":161342,"need_id":61517,"action":"submit_proposal","score":87.22749999999999,"created_at":114,"target_id":61519,"destination":{"map_id":695,"x":5,"y":9},"status":"active","outcome":""},"before":{"id":4213,"name":"Iria Alvor","hour":114,"alive":true,"profession":"ferreiro","lod":"local","position":{"map_id":695,"x":5,"y":9},"residence":695,"hp":100,"hunger":54,"thirst":48,"fatigue":60.8000000000002,"money":2,"food":2,"water":0,"local_food":40,"local_water":104,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{}},"after":{"id":4213,"name":"Iria Alvor","hour":114,"alive":true,"profession":"ferreiro","lod":"local","position":{"map_id":695,"x":5,"y":9},"residence":695,"hp":100,"hunger":54,"thirst":48,"fatigue":60.8000000000002,"money":2,"food":2,"water":0,"local_food":40,"local_water":104,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{}}}.

**Cálculos especializados reais:** [{"system":"lethal_decision","function":"lethal_decisions.LethalDecisionSystem.evaluate","result":{"available":false,"pressure":-112.68,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"protection","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","fear","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":6.460000000000001,"directed_emotion":0.0,"commitment":0.0,"sadism":5.98,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":28.6,"moral_restraint":4.08,"fear":39.1,"risk":8.33587786259542,"bond":0.0,"authority_or_witnesses":15,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{"pressure":-112.68,"cause":{"severity":0,"grave":false,"causes":[],"facts":[],"confidence":0,"mode":"retributive","confirmed_injury":0}}},{"system":"lethal_decision","function":"lethal_decisions.LethalDecisionSystem.evaluate","result":{"available":false,"pressure":-112.68,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"protection","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","fear","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":6.460000000000001,"directed_emotion":0.0,"commitment":0.0,"sadism":5.98,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":28.6,"moral_restraint":4.08,"fear":39.1,"risk":8.33587786259542,"bond":0.0,"authority_or_witnesses":15,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{"pressure":-112.68,"cause":{"severity":0,"grave":false,"causes":[],"facts":[],"confidence":0,"mode":"retributive","confirmed_injury":0}}},{"system":"lethal_pressure","function":"lethality.LethalPressure.evaluate","result":{"available":false,"pressure":-112.68,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"protection","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","fear","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":6.460000000000001,"directed_emotion":0.0,"commitment":0.0,"sadism":5.98,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":28.6,"moral_restraint":4.08,"fear":39.1,"risk":8.33587786259542,"bond":0.0,"authority_or_witnesses":15,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{}},{"system":"capacity","function":"action_pressure.ActionPressureSystem.assess","result":{"eligible":true,"world_pressure":55,"action_pressure":28.11,"eligibility_causes":["shared_problem"],"source_facts":[60826,61481,61506],"capacity":59.47,"perceived_capacity":38.54,"major_barriers":[],"selected_alternative":"submit_proposal"},"inputs":{}},{"system":"capacity","function":"action_pressure.ActionPressureSystem.assess","result":{"eligible":true,"world_pressure":0,"action_pressure":0.0,"eligibility_causes":[],"source_facts":[],"capacity":59.47,"perceived_capacity":38.54,"major_barriers":[],"selected_alternative":"pursue"},"inputs":{}}].

| Evento/hora | Actor→target | Emissor | Testemunhas | Contexto |
| --- | --- | --- | --- | --- |
| 161343 / 114 / PoliticalPressureChanged | 4213→61519 | ["institutions.Institutions.emit","institutions.Institutions.pressure","institutions.Institutions.deliver_support"] | [624,716,718,4109,4141,4150,4164,4170,4173,4178,4207,4213] | {"proposal_id":61519,"previous":31.5,"pressure":87.0,"factors":{"unique_support":23,"severity":55.0,"persistence":14.5,"visibility":10,"local_crisis":0,"affected_localities":[695]}} |
| 161344 / 114 / ProposalSupportDelivered | 4213→61519 | ["institutions.Institutions.emit","institutions.Institutions.deliver_support","institutions.Institutions.submit"] | [624,716,718,4109,4141,4150,4164,4170,4173,4178,4207,4213] | {"proposal_id":61519,"group_id":57703,"supporter_ids":[701,707,713,716,4069,4075,4081,4092,4098,4101,4104,4118,4130,4141,4144,4147,4150,4155,4187,4196,4210,4213,4216],"source_fact":54683} |
| 161345 / 114 / ProposalSubmitted | 4213→4173 | ["institutions.Institutions.emit","institutions.Institutions.submit","society.SocietySystem.execute"] | [624,716,718,4109,4141,4150,4164,4170,4173,4178,4207,4213] | {"proposal_id":61519,"group_id":57703,"supporter_ids":[701,707,713,716,4069,4075,4081,4092,4098,4101,4104,4118,4130,4141,4144,4147,4150,4155,4187,4196,4210,4213,4216],"source_fact":54683} |

**Aprendizado aceito durante a decisão (amostra):** [{"npc":624,"event":161343,"kind":"PoliticalPressureChanged","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":716,"event":161343,"kind":"PoliticalPressureChanged","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":718,"event":161343,"kind":"PoliticalPressureChanged","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":4109,"event":161343,"kind":"PoliticalPressureChanged","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":4141,"event":161343,"kind":"PoliticalPressureChanged","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":4150,"event":161343,"kind":"PoliticalPressureChanged","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":4164,"event":161343,"kind":"PoliticalPressureChanged","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":4170,"event":161343,"kind":"PoliticalPressureChanged","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":4173,"event":161343,"kind":"PoliticalPressureChanged","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":4178,"event":161343,"kind":"PoliticalPressureChanged","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":4207,"event":161343,"kind":"PoliticalPressureChanged","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":4213,"event":161343,"kind":"PoliticalPressureChanged","source":null,"firsthand":true,"confidence":100,"latency":0}].

**Recibos posteriores ligados ao mesmo event_id:** [{"event":161343,"kind":"PoliticalPressureChanged","learned":{"count":13,"first":114,"last":132,"first_people":[624,716,718,4109,4141,4150]}},{"event":161344,"kind":"ProposalSupportDelivered","learned":{"count":12,"first":114,"last":114,"first_people":[624,716,718,4109,4141,4150]}},{"event":161345,"kind":"ProposalSubmitted","learned":{"count":12,"first":114,"last":114,"first_people":[624,716,718,4109,4141,4150]}}]. Contagem é operações de aprendizado aceitas, não indivíduos únicos.

**Consequência imediata:** {"id":4213,"name":"Iria Alvor","hour":114,"alive":true,"profession":"ferreiro","lod":"local","position":{"map_id":695,"x":5,"y":9},"residence":695,"hp":100,"hunger":54,"thirst":48,"fatigue":60.8000000000002,"money":2,"food":2,"water":0,"local_food":40,"local_water":104,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{}}. **Observação/relações com o alvo ao final:** {"observation_end":null,"relations_end":[]}. Não usar esse estado posterior como entrada antiga nem atribuir consequências futuras sem vínculo causal.

### 16. recovery — Marie Solaris #1322, h213: forage

**Pressão escolhida:** `recovery` #177913, prioridade 100, base 95, fonte `own_physiology`, alvo 1322. Motivo: Recuperar condição física após dano.

**Contexto preservado:** {}.

**Entrada:** {"id":1322,"name":"Marie Solaris","hour":213,"alive":true,"profession":"ferreiro","lod":"active","position":{"map_id":3,"x":2,"y":3},"residence":3,"hp":8,"hunger":68,"thirst":50,"fatigue":90.4,"money":1,"food":0,"water":0,"local_food":21,"local_water":0,"recoverable_deprivation":92,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{}}.

**Personalidade:** {"honesty":74,"compassion":62,"courage":90,"independence":74,"greed":94,"diligence":82,"family_loyalty":82,"persistence":12,"temperament":25,"vengefulness":36,"ambition":28,"sadism":48}. **Emoções escalares de entrada:** {"anger":93.10000000000007,"resentment":99.07999999999986,"humiliation":97.70000000000013,"desperation":44.20000000000004,"last_updated":212,"last_support":-10000,"strain":84.19299999999998,"adaptation":0,"last_adapted":0,"stable_material_hours":0,"nested_collections":"LACUNA: cópia rasa; histórico não utilizado"}.

**Conhecimento/locais de entrada:** {"known_places":{"market":{"map_id":3,"x":7,"y":13},"home":{"map_id":3,"x":2,"y":2},"work":{"map_id":3,"x":12,"y":2},"forage":{"map_id":3,"x":1,"y":13},"well_home":{"map_id":3,"x":2,"y":2},"well_rural":{"map_id":3,"x":1,"y":13},"sacred":{"map_id":3,"x":7,"y":1}},"known_towns":[3,50],"route_knowledge_count":2,"knowledge_ids_before":[249093,249094,249098,249100,249109,250315,250316,250321,250329,250339,250342,250343,250360,250361,250368,250376,250602,251342,251507,251516,251526,251529,251536,251548,251546,251550,251553,251554,251558,251567,251568,252584,252740,252745,252756,252975,252979,252984,252988,253008,253010,253021,253061,253062,254124,254131,254133,254316,254322,254326,254362,254583,255433,255439,255444,255470,256374,256421,256564,256569,256573,249082,249048,260608],"market_observation":{"turn":195,"town_id":3,"stock":{"food":20,"grain":35,"water":0,"iron":114,"wood":88},"temporary_work":true,"offers_expire_at":219,"training_offer":null,"price":2,"price_turn":195}}.

**Fatos-fonte retidos após percepção:** [{"event_id":260608,"kind":"AbsenceNoticed","actor_id":1322,"target_id":null,"location":{"map_id":3,"x":7,"y":9},"turn":199,"description":"Marie Solaris não localiza um familiar há 36 horas.","confidence":100,"required_trust":0,"source_id":null,"source_kind":"direct","context":{"last_seen":163,"relative_id":1325}},{"event_id":254583,"kind":"ItemStolen","actor_id":2381,"target_id":3,"location":{"map_id":3,"x":7,"y":13},"turn":193,"description":"Elena Kars roubou comida no mercado de Dorria.","confidence":100,"required_trust":0,"source_id":null,"source_kind":"direct","context":{"item_id":254582,"item_kind":"food"}}].

| Need | ID/alvo | Base→prioridade | Estado/fonte |
| --- | --- | --- | --- |
| recovery | 177913/1322 | 95→100 | active / own_physiology |
| food | 29177/None | 82.0→99.4 | active / physiology |
| rest | 34513/None | 90.4→98.4 | active / physiology |
| money | 17071/None | 58.833333333333336→86.78133333333335 | active / economy |
| food_reserve | 49659/None | 41.0→81.12781954887218 | active / food_reserve |
| political_pressure | 88240/None | 66.7→78.62878571428571 | active / own_shared_problem |
| response | 226849/1241 | 55→75.832 | active / event:226848 |
| protection | 163194/1322 | 45→72.332 | active / event:254583 |
| migration | 164399/50 | 52→62.148 | active / known_towns |
| family | 96181/1325 | 40.6→59.6556 | active / event:260608 |
| water | 39379/None | 50→51.8 | active / physiology |
| advancement | 17073/None | 21.165599999999998→36.3825736 | active / aspiration:wealth |

**Alternativas/gates realmente vistos:**

Need #177913 (`food`): 5 Solutions entraram em _evaluate; 4 saíram disponíveis. Entrada: `steal, forage, work, work_for_food, temporary_service`.

| Opção | Alvo | Etapa | Motivo observado | Auditoria/feeding |
| --- | --- | --- | --- | --- |
| work | None | after_Utility | feeding.survival_viable_false | {"pressure":null,"feeding":{"EstimatedTimeUntilFoodConsumed":30,"EstimatedSurvivalMargin":19,"economically_viable":true,"survival_viable":false,"reason":"SolutionTooSlow","known_conditions":["NoMoney","DistantProduct"]}} |

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| forage | {"target":null,"destination":{"map_id":3,"x":1,"y":13}} | 50.0 | {"base":0.175,"independence":0.185,"hunter":0.0,"travel":-0.11} | {"feeding":{"EstimatedTimeUntilFoodConsumed":13,"EstimatedSurvivalMargin":19,"economically_viable":true,"survival_viable":true,"reason":null,"known_conditions":["NoMoney","DistantProduct"]},"action_pressure":null} |
| steal | {"target":null,"destination":{"map_id":3,"x":7,"y":13}} | 19.258260406037408 | {"base":0.35,"greed":0.15666666666666665,"honesty":-0.37,"courage":0.045,"travel":-0.15,"pressure_moral_tolerance":0.06462463536352042} | {"feeding":{"EstimatedTimeUntilFoodConsumed":17,"EstimatedSurvivalMargin":19,"economically_viable":true,"survival_viable":true,"reason":null,"known_conditions":["NoMoney","DistantProduct"]},"action_pressure":null} |
| work_for_food | {"target":null,"destination":{"map_id":3,"x":1,"y":13}} | 12.0 | {"base":0.225,"diligence":0.1025,"physical_depletion":-0.1575,"travel":-0.11} | {"feeding":{"EstimatedTimeUntilFoodConsumed":13,"EstimatedSurvivalMargin":19,"economically_viable":true,"survival_viable":true,"reason":null,"known_conditions":["NoMoney","DistantProduct"]},"action_pressure":null} |
| temporary_service | {"target":null,"destination":{"map_id":3,"x":7,"y":13}} | 10.200000000000001 | {"base":0.225,"diligence":0.1025,"compassion":0.031,"physical_depletion":-0.1575,"travel":-0.15} | {"feeding":{"EstimatedTimeUntilFoodConsumed":17,"EstimatedSurvivalMargin":19,"economically_viable":true,"survival_viable":true,"reason":null,"known_conditions":["NoMoney","DistantProduct"]},"action_pressure":null} |

Need #177913 (`food`): 5 Solutions entraram em _evaluate; 4 saíram disponíveis. Entrada: `steal, forage, work, work_for_food, temporary_service`.

| Opção | Alvo | Etapa | Motivo observado | Auditoria/feeding |
| --- | --- | --- | --- | --- |
| work | None | after_Utility | feeding.survival_viable_false | {"pressure":null,"feeding":{"EstimatedTimeUntilFoodConsumed":30,"EstimatedSurvivalMargin":19,"economically_viable":true,"survival_viable":false,"reason":"SolutionTooSlow","known_conditions":["NoMoney","DistantProduct"]}} |

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| forage | {"target":null,"destination":{"map_id":3,"x":1,"y":13}} | 50.0 | {"base":0.175,"independence":0.185,"hunter":0.0,"travel":-0.11} | {"feeding":{"EstimatedTimeUntilFoodConsumed":13,"EstimatedSurvivalMargin":19,"economically_viable":true,"survival_viable":true,"reason":null,"known_conditions":["NoMoney","DistantProduct"]},"action_pressure":null} |
| steal | {"target":null,"destination":{"map_id":3,"x":7,"y":13}} | 19.258260406037408 | {"base":0.35,"greed":0.15666666666666665,"honesty":-0.37,"courage":0.045,"travel":-0.15,"pressure_moral_tolerance":0.06462463536352042} | {"feeding":{"EstimatedTimeUntilFoodConsumed":17,"EstimatedSurvivalMargin":19,"economically_viable":true,"survival_viable":true,"reason":null,"known_conditions":["NoMoney","DistantProduct"]},"action_pressure":null} |
| work_for_food | {"target":null,"destination":{"map_id":3,"x":1,"y":13}} | 12.0 | {"base":0.225,"diligence":0.1025,"physical_depletion":-0.1575,"travel":-0.11} | {"feeding":{"EstimatedTimeUntilFoodConsumed":13,"EstimatedSurvivalMargin":19,"economically_viable":true,"survival_viable":true,"reason":null,"known_conditions":["NoMoney","DistantProduct"]},"action_pressure":null} |
| temporary_service | {"target":null,"destination":{"map_id":3,"x":7,"y":13}} | 10.200000000000001 | {"base":0.225,"diligence":0.1025,"compassion":0.031,"physical_depletion":-0.1575,"travel":-0.15} | {"feeding":{"EstimatedTimeUntilFoodConsumed":17,"EstimatedSurvivalMargin":19,"economically_viable":true,"survival_viable":true,"reason":null,"known_conditions":["NoMoney","DistantProduct"]},"action_pressure":null} |

Need #163194 (`protection`): 10 Solutions entraram em _evaluate; 10 saíram disponíveis. Entrada: `denounce, denounce, denounce, denounce, denounce, denounce, denounce, denounce, denounce, pursue`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| denounce | {"target":1287,"destination":{"map_id":3,"x":2,"y":2}} | 92.10000000000001 | {"base":0.225,"honesty":0.1295,"vengefulness":0.036,"courage":0.0675,"trust":0.0125,"travel":-0.01} | {"feeding":null,"action_pressure":null} |
| denounce | {"target":1379,"destination":{"map_id":3,"x":2,"y":2}} | 92.10000000000001 | {"base":0.225,"honesty":0.1295,"vengefulness":0.036,"courage":0.0675,"trust":0.0125,"travel":-0.01} | {"feeding":null,"action_pressure":null} |
| denounce | {"target":1402,"destination":{"map_id":3,"x":2,"y":2}} | 92.10000000000001 | {"base":0.225,"honesty":0.1295,"vengefulness":0.036,"courage":0.0675,"trust":0.0125,"travel":-0.01} | {"feeding":null,"action_pressure":null} |
| denounce | {"target":1264,"destination":{"map_id":3,"x":7,"y":9}} | 72.1 | {"base":0.225,"honesty":0.1295,"vengefulness":0.036,"courage":0.0675,"trust":0.0125,"travel":-0.11} | {"feeding":null,"action_pressure":null} |
| denounce | {"target":44,"destination":{"map_id":3,"x":7,"y":13}} | 64.1 | {"base":0.225,"honesty":0.1295,"vengefulness":0.036,"courage":0.0675,"trust":0.0125,"travel":-0.15} | {"feeding":null,"action_pressure":null} |
| denounce | {"target":73,"destination":{"map_id":3,"x":7,"y":13}} | 64.1 | {"base":0.225,"honesty":0.1295,"vengefulness":0.036,"courage":0.0675,"trust":0.0125,"travel":-0.15} | {"feeding":null,"action_pressure":null} |
| denounce | {"target":1310,"destination":{"map_id":3,"x":7,"y":13}} | 64.1 | {"base":0.225,"honesty":0.1295,"vengefulness":0.036,"courage":0.0675,"trust":0.0125,"travel":-0.15} | {"feeding":null,"action_pressure":null} |
| denounce | {"target":1448,"destination":{"map_id":3,"x":7,"y":13}} | 64.1 | {"base":0.225,"honesty":0.1295,"vengefulness":0.036,"courage":0.0675,"trust":0.0125,"travel":-0.15} | {"feeding":null,"action_pressure":null} |
| denounce | {"target":2265,"destination":{"map_id":3,"x":7,"y":13}} | 64.1 | {"base":0.225,"honesty":0.1295,"vengefulness":0.036,"courage":0.0675,"trust":0.0125,"travel":-0.15} | {"feeding":null,"action_pressure":null} |
| pursue | {"target":2381,"destination":{"map_id":3,"x":7,"y":13}} | 35.64633426785714 | {"base":0.275,"courage":0.09,"diligence":0.06149999999999999,"vengefulness":0.036,"critical_depletion":-0.135,"travel":-0.15,"action_pressure":0.0,"pressure_risk_tolerance":0.0007316713392857139} | {"feeding":null,"action_pressure":{"eligible":true,"world_pressure":0,"action_pressure":0.0,"eligibility_causes":[],"source_facts":[],"capacity":3.18,"perceived_capacity":4.2,"major_barriers":[],"selected_alternative":"pursue"}} |

Need #96181 (`family`): 1 Solutions entraram em _evaluate; 1 saíram disponíveis. Entrada: `check_relative`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| check_relative | {"target":1325,"destination":{"map_id":3,"x":1,"y":13}} | 72.0 | {"base":0.275,"independence":0.0925,"family_loyalty":0.1025,"travel":-0.11} | {"feeding":null,"action_pressure":null} |

Need #17073 (`advancement`): 3 Solutions entraram em _evaluate; 3 saíram disponíveis. Entrada: `work, work_for_food, temporary_service`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| work | {"target":null,"destination":{"map_id":3,"x":12,"y":2}} | 37.5 | {"base":0.25,"diligence":0.205,"physical_depletion":-0.1575,"travel":-0.11} | {"feeding":null,"action_pressure":null} |
| work_for_food | {"target":null,"destination":{"map_id":3,"x":1,"y":13}} | 12.0 | {"base":0.225,"diligence":0.1025,"physical_depletion":-0.1575,"travel":-0.11} | {"feeding":null,"action_pressure":null} |
| temporary_service | {"target":null,"destination":{"map_id":3,"x":7,"y":13}} | 10.200000000000001 | {"base":0.225,"diligence":0.1025,"compassion":0.031,"physical_depletion":-0.1575,"travel":-0.15} | {"feeding":null,"action_pressure":null} |

**Escolhas intermediárias:** [{"chosen":{"action":"forage","score":50.0,"target":null,"destination":{"map_id":3,"x":1,"y":13},"terms":{"base":0.175,"independence":0.185,"hunter":0.0,"travel":-0.11},"feeding":{"EstimatedTimeUntilFoodConsumed":13,"EstimatedSurvivalMargin":19,"economically_viable":true,"survival_viable":true,"reason":null,"known_conditions":["NoMoney","DistantProduct"]},"action_pressure":null},"near_scores":[50.0,19.258260406037408,12.0,10.200000000000001],"variation_draws":"não capturados; RNG não consultado pelo observador"}].

**Preparação/substituição posterior:** [].

**Winner final / Goal:** {"winner":{"action":"forage","score":50.0,"target":null,"destination":{"map_id":3,"x":1,"y":13},"terms":{"base":0.175,"independence":0.185,"hunter":0.0,"travel":-0.11},"feeding":{"EstimatedTimeUntilFoodConsumed":13,"EstimatedSurvivalMargin":19,"economically_viable":true,"survival_viable":true,"reason":null,"known_conditions":["NoMoney","DistantProduct"]},"action_pressure":null},"goal":{"id":275147,"need_id":177913,"action":"forage","score":48.0,"created_at":212,"target_id":null,"destination":{"map_id":3,"x":1,"y":13},"status":"active","outcome":""},"suspended_before":null,"suspended_after":null}.

**Por que outras Needs não foram executadas:** a fila prioriza emergência/priority/ID e para na primeira solucionável, sujeita à continuidade/preparo. Outras pressões retidas: food#29177(99.4), rest#34513(98.4), money#17071(86.78133333333335), food_reserve#49659(81.12781954887218), political_pressure#88240(78.62878571428571), response#226849(75.832), protection#163194(72.332), migration#164399(62.148), family#96181(59.6556), water#39379(51.8), advancement#17073(36.3825736). Não atribuir score global entre Needs.

**Execução:** execute não foi chamado neste trace. A Goal pode ter iniciado/continuado deslocamento; o snapshot e a posição posterior delimitam essa conclusão.

**Cálculos especializados reais:** [{"system":"lethal_decision","function":"lethal_decisions.LethalDecisionSystem.evaluate","result":{"available":false,"pressure":-85.79,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"protection","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":6.12,"directed_emotion":0.0,"commitment":0.0,"sadism":6.24,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":34.1,"moral_restraint":8.879999999999999,"fear":17.666666666666664,"risk":7.5,"bond":0.0,"authority_or_witnesses":0.0,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{"pressure":-85.79,"cause":{"severity":0,"grave":false,"causes":[],"facts":[],"confidence":0,"mode":"retributive","confirmed_injury":0}}},{"system":"lethal_decision","function":"lethal_decisions.LethalDecisionSystem.evaluate","result":{"available":false,"pressure":-85.79,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"protection","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":6.12,"directed_emotion":0.0,"commitment":0.0,"sadism":6.24,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":34.1,"moral_restraint":8.879999999999999,"fear":17.666666666666664,"risk":7.5,"bond":0.0,"authority_or_witnesses":0.0,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{"pressure":-85.79,"cause":{"severity":0,"grave":false,"causes":[],"facts":[],"confidence":0,"mode":"retributive","confirmed_injury":0}}},{"system":"lethal_pressure","function":"lethality.LethalPressure.evaluate","result":{"available":false,"pressure":-85.79,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"protection","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":6.12,"directed_emotion":0.0,"commitment":0.0,"sadism":6.24,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":34.1,"moral_restraint":8.879999999999999,"fear":17.666666666666664,"risk":7.5,"bond":0.0,"authority_or_witnesses":0.0,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{}},{"system":"lethal_decision","function":"lethal_decisions.LethalDecisionSystem.evaluate","result":{"available":false,"pressure":-96.57,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"response","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":6.12,"directed_emotion":0.0,"commitment":0.0,"sadism":6.24,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":34.1,"moral_restraint":8.879999999999999,"fear":26.5,"risk":9.448818897637794,"bond":0.0,"authority_or_witnesses":0.0,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{"pressure":-96.57,"cause":{"severity":0,"grave":false,"causes":[],"facts":[],"confidence":0,"mode":"retributive","confirmed_injury":0}}},{"system":"lethal_decision","function":"lethal_decisions.LethalDecisionSystem.evaluate","result":{"available":false,"pressure":-96.57,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"response","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":6.12,"directed_emotion":0.0,"commitment":0.0,"sadism":6.24,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":34.1,"moral_restraint":8.879999999999999,"fear":26.5,"risk":9.448818897637794,"bond":0.0,"authority_or_witnesses":0.0,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{"pressure":-96.57,"cause":{"severity":0,"grave":false,"causes":[],"facts":[],"confidence":0,"mode":"retributive","confirmed_injury":0}}},{"system":"lethal_pressure","function":"lethality.LethalPressure.evaluate","result":{"available":false,"pressure":-96.57,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"response","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":6.12,"directed_emotion":0.0,"commitment":0.0,"sadism":6.24,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":34.1,"moral_restraint":8.879999999999999,"fear":26.5,"risk":9.448818897637794,"bond":0.0,"authority_or_witnesses":0.0,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{}},{"system":"capacity","function":"action_pressure.ActionPressureSystem.assess","result":{"eligible":true,"world_pressure":0,"action_pressure":0.0,"eligibility_causes":[],"source_facts":[],"capacity":3.18,"perceived_capacity":4.2,"major_barriers":[],"selected_alternative":"pursue"},"inputs":{}}].

**Evento:** nenhum evento retido durante esta decisão. Isso pode significar movimento/efeito sem evento; não implica falha.

**Aprendizado aceito durante a decisão (amostra):** [].

**Recibos posteriores ligados ao mesmo event_id:** []. Contagem é operações de aprendizado aceitas, não indivíduos únicos.

**Consequência imediata:** {"id":1322,"name":"Marie Solaris","hour":213,"alive":true,"profession":"ferreiro","lod":"active","position":{"map_id":3,"x":2,"y":4},"residence":3,"hp":8,"hunger":68,"thirst":50,"fatigue":90.4,"money":1,"food":0,"water":0,"local_food":21,"local_water":0,"recoverable_deprivation":92,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{}}. **Observação/relações com o alvo ao final:** {"observation_end":null,"relations_end":[]}. Não usar esse estado posterior como entrada antiga nem atribuir consequências futuras sem vínculo causal.

### 17. religion — Nora Arven #3376, h167: fill_water

**Pressão escolhida:** `divine_contact` #23841, prioridade 55.6, base 47.6, fonte `personal_faith`, alvo 5909. Motivo: Buscar contato por devoção, ambição ou perda.

**Contexto preservado:** {"source_fact":null}.

**Entrada:** {"id":3376,"name":"Nora Arven","hour":167,"alive":true,"profession":"lenhador","lod":"active","position":{"map_id":302,"x":7,"y":13},"residence":526,"hp":14,"hunger":41,"thirst":100,"fatigue":100,"money":9,"food":0,"water":0,"local_food":0,"local_water":0,"recoverable_deprivation":86,"starvation_hours":30,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{"fill_water":178,"drink_well":177}}.

**Personalidade:** {"honesty":90,"compassion":17,"courage":27,"independence":76,"greed":76,"diligence":19,"family_loyalty":58,"persistence":67,"temperament":77,"vengefulness":58,"ambition":65,"sadism":0}. **Emoções escalares de entrada:** {"anger":0.0,"resentment":0.0,"humiliation":0.0,"desperation":20.499999999999957,"last_updated":166,"last_support":-10000,"strain":26.833999999999993,"adaptation":0,"last_adapted":0,"stable_material_hours":0,"nested_collections":"LACUNA: cópia rasa; histórico não utilizado"}.

**Conhecimento/locais de entrada:** {"known_places":{"market":{"map_id":302,"x":7,"y":13},"home":{"map_id":526,"x":2,"y":2},"work":{"map_id":526,"x":4,"y":2},"forage":{"map_id":302,"x":1,"y":13},"well_home":{"map_id":526,"x":2,"y":2},"well_rural":{"map_id":302,"x":1,"y":13},"sacred":{"map_id":526,"x":3,"y":1}},"known_towns":[526,479,302],"route_knowledge_count":4,"knowledge_ids_before":[191705,191706,193079,194460,194461,195796,195804,195805,195837,195838,195839,182372,197476,197477,198906,198907,198916,198917,198918,198940,198975,198976,200316,200323,200336,200371,200372,201166,201712,201713,202498,202542,202936,202952,203165,203642,204036,204222,205197,205215,205427,205891,206236,206254,206263,206428,206429,207184,207185,207188,207213,207219,207240,207336,208900,209885,210262,212568,213616,205227,174955,221080,223136,223689],"market_observation":{"turn":166,"town_id":302,"stock":{"food":0,"grain":0,"water":0,"iron":64,"wood":120},"temporary_work":false,"offers_expire_at":190,"training_offer":null,"price":14,"price_turn":166}}.

**Fatos-fonte retidos após percepção:** [].

| Need | ID/alvo | Base→prioridade | Estado/fonte |
| --- | --- | --- | --- |
| water | 43857/None | 100→100 | active / physiology |
| food | 28377/None | 41.5→100 | active / physiology |
| rest | 38442/None | 100→100 | active / physiology |
| recovery | 203162/3376 | 91→93.85 | active / own_physiology |
| food_reserve | 68192/None | 41.0→67.93706293706293 | active / food_reserve |
| divine_contact | 23841/5909 | 47.6→55.6 | active / personal_faith |
| advancement | 23838/None | 24.9726→51.702080731428566 | blocked / self_assessment:3 |
| money | 87493/None | 36.958333333333336→50.43033333333333 | active / economy |
| status | 220517/None | 20→36.7 | blocked / encounter:591:164 |

**Alternativas/gates realmente vistos:**

Need #43857 (`water`): 3 Solutions entraram em _evaluate; 0 saíram disponíveis. Entrada: `drink_well, drink_well, drink_well`.

| Opção | Alvo | Etapa | Motivo observado | Auditoria/feeding |
| --- | --- | --- | --- | --- |
| drink_well | None | before_Utility_or_unresolved | cooldown_after_failure | {"pressure":null,"feeding":null} |
| drink_well | None | before_Utility_or_unresolved | cooldown_after_failure | {"pressure":null,"feeding":null} |
| drink_well | None | before_Utility_or_unresolved | cooldown_after_failure | {"pressure":null,"feeding":null} |

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |

Need #28377 (`food`): 2 Solutions entraram em _evaluate; 0 saíram disponíveis. Entrada: `forage, forage_meal`.

| Opção | Alvo | Etapa | Motivo observado | Auditoria/feeding |
| --- | --- | --- | --- | --- |
| forage | None | after_Utility | feeding.survival_viable_false | {"pressure":null,"feeding":{"EstimatedTimeUntilFoodConsumed":8,"EstimatedSurvivalMargin":4,"economically_viable":true,"survival_viable":false,"reason":"SolutionTooSlow","known_conditions":["NoMoney"]}} |
| forage_meal | None | after_Utility | feeding.survival_viable_false | {"pressure":null,"feeding":{"EstimatedTimeUntilFoodConsumed":7,"EstimatedSurvivalMargin":4,"economically_viable":true,"survival_viable":false,"reason":"SolutionTooSlow","known_conditions":["NoMoney"]}} |

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |

Need #38442 (`rest`): 1 Solutions entraram em _evaluate; 0 saíram disponíveis. Entrada: `sleep`.

| Opção | Alvo | Etapa | Motivo observado | Auditoria/feeding |
| --- | --- | --- | --- | --- |
| sleep | None | before_Utility_or_unresolved | destination_other_map | {"pressure":null,"feeding":null} |

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |

Need #203162 (`water`): 3 Solutions entraram em _evaluate; 0 saíram disponíveis. Entrada: `drink_well, drink_well, drink_well`.

| Opção | Alvo | Etapa | Motivo observado | Auditoria/feeding |
| --- | --- | --- | --- | --- |
| drink_well | None | before_Utility_or_unresolved | cooldown_after_failure | {"pressure":null,"feeding":null} |
| drink_well | None | before_Utility_or_unresolved | cooldown_after_failure | {"pressure":null,"feeding":null} |
| drink_well | None | before_Utility_or_unresolved | cooldown_after_failure | {"pressure":null,"feeding":null} |

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |

Need #68192 (`food_reserve`): 1 Solutions entraram em _evaluate; 0 saíram disponíveis. Entrada: `forage`.

| Opção | Alvo | Etapa | Motivo observado | Auditoria/feeding |
| --- | --- | --- | --- | --- |
| forage | None | after_Utility | feeding.survival_viable_false | {"pressure":null,"feeding":{"EstimatedTimeUntilFoodConsumed":8,"EstimatedSurvivalMargin":4,"economically_viable":true,"survival_viable":false,"reason":"SolutionTooSlow","known_conditions":["NoMoney"]}} |

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |

Need #23841 (`divine_contact`): 1 Solutions entraram em _evaluate; 1 saíram disponíveis. Entrada: `seek_divine_contact`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| seek_divine_contact | {"target":5909,"destination":{"map_id":302,"x":7,"y":1}} | 61.75000000000001 | {"base":0.275,"devotion":0.105,"ambition":0.04875,"travel":-0.12} | {"feeding":null,"action_pressure":null} |

Need #23838 (`advancement`): 0 Solutions entraram em _evaluate; 0 saíram disponíveis. Entrada: ``.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |

Need #220517 (`status`): 0 Solutions entraram em _evaluate; 0 saíram disponíveis. Entrada: ``.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |

**Escolhas intermediárias:** [{"chosen":{"action":"seek_divine_contact","score":61.75000000000001,"target":5909,"destination":{"map_id":302,"x":7,"y":1},"terms":{"base":0.275,"devotion":0.105,"ambition":0.04875,"travel":-0.12},"feeding":null,"action_pressure":null},"near_scores":[61.75000000000001],"variation_draws":"não capturados; RNG não consultado pelo observador"}].

**Preparação/substituição posterior:** [{"input":{"action":"seek_divine_contact","score":61.75000000000001,"target":5909,"destination":{"map_id":302,"x":7,"y":1},"terms":{"base":0.275,"devotion":0.105,"ambition":0.04875,"travel":-0.12},"feeding":null,"action_pressure":null},"replacement":{"action":"fill_water","score":100,"target":null,"destination":{"map_id":302,"x":7,"y":13},"terms":{},"feeding":null,"action_pressure":null},"travel":12,"horizon":18}].

**Winner final / Goal:** {"winner":{"action":"fill_water","score":100,"target":null,"destination":{"map_id":302,"x":7,"y":13},"terms":{},"feeding":null,"action_pressure":null},"goal":{"id":224436,"need_id":23841,"action":"fill_water","score":100,"created_at":167,"target_id":null,"destination":{"map_id":302,"x":7,"y":13},"status":"failed","outcome":"Não há água para levar nesta fonte."},"suspended_before":null,"suspended_after":null}.

**Por que outras Needs não foram executadas:** a fila prioriza emergência/priority/ID e para na primeira solucionável, sujeita à continuidade/preparo. Outras pressões retidas: water#43857(100), food#28377(100), rest#38442(100), recovery#203162(93.85), food_reserve#68192(67.93706293706293), advancement#23838(51.702080731428566), money#87493(50.43033333333333), status#220517(36.7). Não atribuir score global entre Needs.

**Execução:** {"success":false,"result":[false,"Não há água para levar nesta fonte."],"goal_at_entry":{"id":224436,"need_id":23841,"action":"fill_water","score":100,"created_at":167,"target_id":null,"destination":{"map_id":302,"x":7,"y":13},"status":"active","outcome":""},"before":{"id":3376,"name":"Nora Arven","hour":167,"alive":true,"profession":"lenhador","lod":"active","position":{"map_id":302,"x":7,"y":13},"residence":526,"hp":14,"hunger":41,"thirst":100,"fatigue":100,"money":9,"food":0,"water":0,"local_food":0,"local_water":0,"recoverable_deprivation":86,"starvation_hours":30,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{"fill_water":178,"drink_well":177}},"after":{"id":3376,"name":"Nora Arven","hour":167,"alive":true,"profession":"lenhador","lod":"active","position":{"map_id":302,"x":7,"y":13},"residence":526,"hp":14,"hunger":41,"thirst":100,"fatigue":100,"money":9,"food":0,"water":0,"local_food":0,"local_water":0,"recoverable_deprivation":86,"starvation_hours":30,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{"fill_water":178,"drink_well":177}}}.

**Cálculos especializados reais:** [].

| Evento/hora | Actor→target | Emissor | Testemunhas | Contexto |
| --- | --- | --- | --- | --- |
| 224434 / 167 / AgencyDiagnostic | 3376→None | ["agency.AgencySystem.event","agency.AgencySystem.diagnostic","agency.AgencySystem.blocked"] | [3376] | {"need_id":43857,"category":"vital","reason":"no_viable_known_solution","competing":null,"profile":{"impulse":59.76099999999999,"perceived_agency":0.43700000000000006,"unresolved_pressure":1,"risk":0.0,"uncertainty":0.1,"opportunity":1.0,"aspiration_drive":0}} |
| 224435 / 167 / AgencyDiagnostic | 3376→None | ["agency.AgencySystem.event","agency.AgencySystem.diagnostic","agency.AgencySystem.blocked"] | [3376] | {"need_id":28377,"category":"vital","reason":"no_viable_known_solution","competing":null,"profile":{"impulse":28.852428571428565,"perceived_agency":0.48700000000000004,"unresolved_pressure":0.14285714285714285,"risk":0.0,"uncertainty":0.1,"opportunity":1.0,"aspiration_drive":0}} |

**Aprendizado aceito durante a decisão (amostra):** [{"npc":3376,"event":224434,"kind":"AgencyDiagnostic","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":3376,"event":224435,"kind":"AgencyDiagnostic","source":null,"firsthand":true,"confidence":100,"latency":0}].

**Recibos posteriores ligados ao mesmo event_id:** [{"event":224434,"kind":"AgencyDiagnostic","learned":{"count":1,"first":167,"last":167,"first_people":[3376]}},{"event":224435,"kind":"AgencyDiagnostic","learned":{"count":1,"first":167,"last":167,"first_people":[3376]}}]. Contagem é operações de aprendizado aceitas, não indivíduos únicos.

**Consequência imediata:** {"id":3376,"name":"Nora Arven","hour":167,"alive":true,"profession":"lenhador","lod":"active","position":{"map_id":302,"x":7,"y":13},"residence":526,"hp":14,"hunger":41,"thirst":100,"fatigue":100,"money":9,"food":0,"water":0,"local_food":0,"local_water":0,"recoverable_deprivation":86,"starvation_hours":30,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{"fill_water":179,"drink_well":177}}. **Observação/relações com o alvo ao final:** {"observation_end":null,"relations_end":[]}. Não usar esse estado posterior como entrada antiga nem atribuir consequências futuras sem vínculo causal.

### 18. rest — Elena Alvor #2927, h201: sleep

**Pressão escolhida:** `rest` #35086, prioridade 100, base 100, fonte `physiology`, alvo None. Motivo: Cansaço.

**Contexto preservado:** {}.

**Entrada:** {"id":2927,"name":"Elena Alvor","hour":201,"alive":true,"profession":"ferreiro","lod":"active","position":{"map_id":414,"x":5,"y":6},"residence":414,"hp":30,"hunger":68,"thirst":42,"fatigue":100,"money":0,"food":0,"water":0,"local_food":4,"local_water":140,"recoverable_deprivation":70,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{"ask_help":207}}.

**Personalidade:** {"honesty":53,"compassion":77,"courage":79,"independence":20,"greed":72,"diligence":95,"family_loyalty":35,"persistence":47,"temperament":8,"vengefulness":89,"ambition":71,"sadism":0}. **Emoções escalares de entrada:** {"anger":99.10000000000001,"resentment":72.32000000000005,"humiliation":53.599999999999966,"desperation":27.999999999999925,"last_updated":200,"last_support":103,"strain":60.75849999999996,"adaptation":0,"last_adapted":0,"stable_material_hours":0,"nested_collections":"LACUNA: cópia rasa; histórico não utilizado"}.

**Conhecimento/locais de entrada:** {"known_places":{"market":{"map_id":414,"x":5,"y":9},"home":{"map_id":414,"x":2,"y":2},"work":{"map_id":414,"x":8,"y":2},"forage":{"map_id":414,"x":1,"y":9},"well_home":{"map_id":414,"x":2,"y":2},"well_rural":{"map_id":414,"x":1,"y":9},"sacred":{"map_id":414,"x":5,"y":1}},"known_towns":[414,302],"route_knowledge_count":2,"knowledge_ids_before":[225852,225853,225855,225857,225862,225874,225877,225880,225882,225887,225898,226674,227202,227203,227205,227206,227208,227214,227218,227222,227870,228329,228334,228336,228340,228347,228351,228356,228362,229076,229531,229539,229541,229550,230205,230628,223777,220444,255768,255783,255792,256440,256442,256883,256881,256890,256895,256902,257482,257484,257487,257885,257883,257888,257892,257895,257908,258821,258831,258844,258855,258853,258861,259498],"market_observation":{"turn":198,"town_id":414,"stock":{"food":8,"grain":114,"water":142,"iron":120,"wood":100},"temporary_work":true,"offers_expire_at":222,"training_offer":null,"price":4,"price_turn":198}}.

**Fatos-fonte retidos após percepção:** [{"event_id":225857,"kind":"WantedIssued","actor_id":2938,"target_id":414,"location":{"map_id":414,"x":5,"y":9},"turn":168,"description":"Elena Vale registrou procura por Elena Alvor.","confidence":100,"required_trust":0,"source_id":null,"source_kind":"direct","context":{"record_id":225856,"suspect_id":2927,"source_fact":225855,"severity":1,"confidence":100,"last_known_location":{"map_id":414,"x":5,"y":9}}},{"event_id":258853,"kind":"ItemStolen","actor_id":3048,"target_id":414,"location":{"map_id":414,"x":5,"y":9},"turn":197,"description":"Aldren Douran roubou comida no mercado de Elithon.","confidence":100,"required_trust":0,"source_id":null,"source_kind":"direct","context":{"item_id":258852,"item_kind":"food"}},{"event_id":257885,"kind":"WantedIssued","actor_id":437,"target_id":414,"location":{"map_id":414,"x":5,"y":9},"turn":196,"description":"Mira Alvor registrou procura por Elena Alvor.","confidence":100,"required_trust":0,"source_id":null,"source_kind":"direct","context":{"record_id":257884,"suspect_id":2927,"source_fact":257883,"severity":1,"confidence":100,"last_known_location":{"map_id":414,"x":5,"y":9}}}].

| Need | ID/alvo | Base→prioridade | Estado/fonte |
| --- | --- | --- | --- |
| food | 18153/None | 82.0→100 | active / physiology |
| rest | 35086/None | 100→100 | active / physiology |
| money | 18154/None | 64.33333333333334→93.58533333333334 | active / economy |
| recovery | 214713/2927 | 75→81.3 | active / own_physiology |
| food_reserve | 18152/None | 41.0→80.29074889867842 | active / food_reserve |
| political_pressure | 66950/None | 65.98333333333333→76.50193333333334 | active / own_shared_problem |
| response | 225858/2938 | 55→73.444 | active / event:225857 |
| response | 257886/437 | 55→69.244 | active / event:257885 |
| migration | 66949/302 | 62→69.05199999999999 | active / known_towns |
| protection | 65500/2927 | 45→69.04400000000001 | active / event:258853 |
| organizational_survival | 70589/2982 | 54.30500000000001→64.7928 | active / group:46649 |
| work | 35087/None | 35→54.15 | active / profession |
| water | 45310/None | 42→43.2 | active / physiology |

**Alternativas/gates realmente vistos:**

Need #18153 (`food`): 7 Solutions entraram em _evaluate; 6 saíram disponíveis. Entrada: `steal, forage, ask_help, work, work_for_food, temporary_service, steal_person`.

| Opção | Alvo | Etapa | Motivo observado | Auditoria/feeding |
| --- | --- | --- | --- | --- |
| ask_help | 2930 | before_Utility_or_unresolved | cooldown_after_failure | {"pressure":null,"feeding":null} |

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| steal_person | {"target":435,"destination":null} | 67.90444274999999 | {"base":0.31,"greed":0.144,"honesty":-0.23850000000000002,"authority":-0.0,"courage":0.0395,"travel":-0.0,"pressure_moral_tolerance":0.08452221374999999} | {"feeding":{"EstimatedTimeUntilFoodConsumed":2,"EstimatedSurvivalMargin":29,"economically_viable":true,"survival_viable":true,"reason":null,"known_conditions":["NoMoney","DistantProduct"]},"action_pressure":null} |
| work | {"target":null,"destination":{"map_id":414,"x":8,"y":2}} | 61.625 | {"base":0.25,"diligence":0.2375,"physical_depletion":-0.109375,"travel":-0.07} | {"feeding":{"EstimatedTimeUntilFoodConsumed":23,"EstimatedSurvivalMargin":29,"economically_viable":true,"survival_viable":true,"reason":null,"known_conditions":["NoMoney","DistantProduct"]},"action_pressure":null} |
| steal | {"target":null,"destination":{"map_id":414,"x":5,"y":9}} | 59.80444274999999 | {"base":0.35,"greed":0.12,"honesty":-0.265,"courage":0.0395,"travel":-0.03,"pressure_moral_tolerance":0.08452221374999999} | {"feeding":{"EstimatedTimeUntilFoodConsumed":5,"EstimatedSurvivalMargin":29,"economically_viable":true,"survival_viable":true,"reason":null,"known_conditions":["NoMoney","DistantProduct"]},"action_pressure":null} |
| temporary_service | {"target":null,"destination":{"map_id":414,"x":5,"y":9}} | 48.575 | {"base":0.225,"diligence":0.11875,"compassion":0.0385,"physical_depletion":-0.109375,"travel":-0.03} | {"feeding":{"EstimatedTimeUntilFoodConsumed":5,"EstimatedSurvivalMargin":29,"economically_viable":true,"survival_viable":true,"reason":null,"known_conditions":["NoMoney","DistantProduct"]},"action_pressure":null} |
| work_for_food | {"target":null,"destination":{"map_id":414,"x":1,"y":9}} | 32.875 | {"base":0.225,"diligence":0.11875,"physical_depletion":-0.109375,"travel":-0.07} | {"feeding":{"EstimatedTimeUntilFoodConsumed":9,"EstimatedSurvivalMargin":29,"economically_viable":true,"survival_viable":true,"reason":null,"known_conditions":["NoMoney","DistantProduct"]},"action_pressure":null} |
| forage | {"target":null,"destination":{"map_id":414,"x":1,"y":9}} | 30.999999999999993 | {"base":0.175,"independence":0.05,"hunter":0.0,"travel":-0.07} | {"feeding":{"EstimatedTimeUntilFoodConsumed":9,"EstimatedSurvivalMargin":29,"economically_viable":true,"survival_viable":true,"reason":null,"known_conditions":["NoMoney","DistantProduct"]},"action_pressure":null} |

Need #35086 (`rest`): 1 Solutions entraram em _evaluate; 1 saíram disponíveis. Entrada: `sleep`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| sleep | {"target":null,"destination":{"map_id":414,"x":2,"y":2}} | 86.0 | {"base":0.5,"recovery_pressure":0.0,"travel":-0.07} | {"feeding":null,"action_pressure":null} |

Need #65500 (`protection`): 9 Solutions entraram em _evaluate; 9 saíram disponíveis. Entrada: `denounce, denounce, denounce, denounce, denounce, denounce, denounce, ask_personal_help, pursue`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| pursue | {"target":3048,"destination":{"map_id":414,"x":5,"y":9}} | 97.13362082414456 | {"base":0.275,"courage":0.079,"diligence":0.07125,"vengefulness":0.08900000000000001,"critical_depletion":0.0,"travel":-0.03,"action_pressure":0.0,"pressure_risk_tolerance":0.0014181041207227236} | {"feeding":null,"action_pressure":{"eligible":true,"world_pressure":0,"action_pressure":0.0,"eligibility_causes":[],"source_facts":[],"capacity":10.0,"perceived_capacity":12.32,"major_barriers":[],"selected_alternative":"pursue"}} |
| denounce | {"target":2984,"destination":{"map_id":414,"x":5,"y":8}} | 91.7 | {"base":0.225,"honesty":0.09275,"vengefulness":0.08900000000000001,"courage":0.059250000000000004,"trust":0.0125,"travel":-0.02} | {"feeding":null,"action_pressure":null} |
| denounce | {"target":437,"destination":{"map_id":414,"x":5,"y":9}} | 89.7 | {"base":0.225,"honesty":0.09275,"vengefulness":0.08900000000000001,"courage":0.059250000000000004,"trust":0.0125,"travel":-0.03} | {"feeding":null,"action_pressure":null} |
| denounce | {"target":2961,"destination":{"map_id":414,"x":5,"y":9}} | 89.7 | {"base":0.225,"honesty":0.09275,"vengefulness":0.08900000000000001,"courage":0.059250000000000004,"trust":0.0125,"travel":-0.03} | {"feeding":null,"action_pressure":null} |
| denounce | {"target":3007,"destination":{"map_id":414,"x":5,"y":9}} | 89.7 | {"base":0.225,"honesty":0.09275,"vengefulness":0.08900000000000001,"courage":0.059250000000000004,"trust":0.0125,"travel":-0.03} | {"feeding":null,"action_pressure":null} |
| denounce | {"target":3030,"destination":{"map_id":414,"x":5,"y":9}} | 89.7 | {"base":0.225,"honesty":0.09275,"vengefulness":0.08900000000000001,"courage":0.059250000000000004,"trust":0.0125,"travel":-0.03} | {"feeding":null,"action_pressure":null} |
| denounce | {"target":3053,"destination":{"map_id":414,"x":5,"y":9}} | 89.7 | {"base":0.225,"honesty":0.09275,"vengefulness":0.08900000000000001,"courage":0.059250000000000004,"trust":0.0125,"travel":-0.03} | {"feeding":null,"action_pressure":null} |
| denounce | {"target":2938,"destination":{"map_id":414,"x":5,"y":2}} | 87.7 | {"base":0.225,"honesty":0.09275,"vengefulness":0.08900000000000001,"courage":0.059250000000000004,"trust":0.0125,"travel":-0.04} | {"feeding":null,"action_pressure":null} |
| ask_personal_help | {"target":2930,"destination":null} | 50.9 | {"base":0.125,"independence":-0.03,"compassion":0.077,"trust":0.049,"reputation":0.0,"relationship":0.0335,"travel":-0.0} | {"feeding":null,"action_pressure":null} |

**Escolhas intermediárias:** [{"chosen":{"action":"steal_person","score":67.90444274999999,"target":435,"destination":null,"terms":{"base":0.31,"greed":0.144,"honesty":-0.23850000000000002,"authority":-0.0,"courage":0.0395,"travel":-0.0,"pressure_moral_tolerance":0.08452221374999999},"feeding":{"EstimatedTimeUntilFoodConsumed":2,"EstimatedSurvivalMargin":29,"economically_viable":true,"survival_viable":true,"reason":null,"known_conditions":["NoMoney","DistantProduct"]},"action_pressure":null},"near_scores":[67.90444274999999,61.625,59.80444274999999,48.575,32.875,30.999999999999993],"variation_draws":"não capturados; RNG não consultado pelo observador"}].

**Preparação/substituição posterior:** [].

**Winner final / Goal:** {"winner":{"action":"sleep","score":86.0,"target":null,"destination":{"map_id":414,"x":2,"y":2},"terms":{"base":0.5,"recovery_pressure":0.0,"travel":-0.07},"feeding":null,"action_pressure":null},"goal":{"id":259893,"need_id":35086,"action":"sleep","score":80.0,"created_at":198,"target_id":null,"destination":{"map_id":414,"x":2,"y":2},"status":"active","outcome":""},"suspended_before":null,"suspended_after":null}.

**Por que outras Needs não foram executadas:** a fila prioriza emergência/priority/ID e para na primeira solucionável, sujeita à continuidade/preparo. Outras pressões retidas: food#18153(100), money#18154(93.58533333333334), recovery#214713(81.3), food_reserve#18152(80.29074889867842), political_pressure#66950(76.50193333333334), response#225858(73.444), response#257886(69.244), migration#66949(69.05199999999999), protection#65500(69.04400000000001), organizational_survival#70589(64.7928), work#35087(54.15), water#45310(43.2). Não atribuir score global entre Needs.

**Execução:** execute não foi chamado neste trace. A Goal pode ter iniciado/continuado deslocamento; o snapshot e a posição posterior delimitam essa conclusão.

**Cálculos especializados reais:** [{"system":"lethal_decision","function":"lethal_decisions.LethalDecisionSystem.evaluate","result":{"available":false,"pressure":-75.11,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"protection","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":15.13,"directed_emotion":7.397500000000019,"commitment":0.0,"sadism":0.0,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":42.35,"moral_restraint":6.359999999999999,"fear":13.42538461538461,"risk":5.504061156235068,"bond":0.0,"authority_or_witnesses":0.0,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{"pressure":-75.11,"cause":{"severity":0,"grave":false,"causes":[],"facts":[],"confidence":0,"mode":"retributive","confirmed_injury":0}}},{"system":"lethal_decision","function":"lethal_decisions.LethalDecisionSystem.evaluate","result":{"available":false,"pressure":-75.11,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"protection","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":15.13,"directed_emotion":7.397500000000019,"commitment":0.0,"sadism":0.0,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":42.35,"moral_restraint":6.359999999999999,"fear":13.42538461538461,"risk":5.504061156235068,"bond":0.0,"authority_or_witnesses":0.0,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{"pressure":-75.11,"cause":{"severity":0,"grave":false,"causes":[],"facts":[],"confidence":0,"mode":"retributive","confirmed_injury":0}}},{"system":"lethal_pressure","function":"lethality.LethalPressure.evaluate","result":{"available":false,"pressure":-75.11,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"protection","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":15.13,"directed_emotion":7.397500000000019,"commitment":0.0,"sadism":0.0,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":42.35,"moral_restraint":6.359999999999999,"fear":13.42538461538461,"risk":5.504061156235068,"bond":0.0,"authority_or_witnesses":0.0,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{}},{"system":"lethal_decision","function":"lethal_decisions.LethalDecisionSystem.evaluate","result":{"available":false,"pressure":-99.06,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"response","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":15.13,"directed_emotion":0.0,"commitment":0.0,"sadism":0.0,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":42.35,"moral_restraint":6.359999999999999,"fear":28.15,"risk":7.326007326007325,"bond":0.0,"authority_or_witnesses":0.0,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{"pressure":-99.06,"cause":{"severity":0,"grave":false,"causes":[],"facts":[],"confidence":0,"mode":"retributive","confirmed_injury":0}}},{"system":"lethal_decision","function":"lethal_decisions.LethalDecisionSystem.evaluate","result":{"available":false,"pressure":-99.06,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"response","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":15.13,"directed_emotion":0.0,"commitment":0.0,"sadism":0.0,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":42.35,"moral_restraint":6.359999999999999,"fear":28.15,"risk":7.326007326007325,"bond":0.0,"authority_or_witnesses":0.0,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{"pressure":-99.06,"cause":{"severity":0,"grave":false,"causes":[],"facts":[],"confidence":0,"mode":"retributive","confirmed_injury":0}}},{"system":"lethal_pressure","function":"lethality.LethalPressure.evaluate","result":{"available":false,"pressure":-99.06,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"response","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":15.13,"directed_emotion":0.0,"commitment":0.0,"sadism":0.0,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":42.35,"moral_restraint":6.359999999999999,"fear":28.15,"risk":7.326007326007325,"bond":0.0,"authority_or_witnesses":0.0,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{}},{"system":"lethal_decision","function":"lethal_decisions.LethalDecisionSystem.evaluate","result":{"available":false,"pressure":-99.06,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"response","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":15.13,"directed_emotion":0.0,"commitment":0.0,"sadism":0.0,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":42.35,"moral_restraint":6.359999999999999,"fear":28.15,"risk":7.326007326007325,"bond":0.0,"authority_or_witnesses":0.0,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{"pressure":-99.06,"cause":{"severity":0,"grave":false,"causes":[],"facts":[],"confidence":0,"mode":"retributive","confirmed_injury":0}}},{"system":"lethal_decision","function":"lethal_decisions.LethalDecisionSystem.evaluate","result":{"available":false,"pressure":-99.06,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"response","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":15.13,"directed_emotion":0.0,"commitment":0.0,"sadism":0.0,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":42.35,"moral_restraint":6.359999999999999,"fear":28.15,"risk":7.326007326007325,"bond":0.0,"authority_or_witnesses":0.0,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{"pressure":-99.06,"cause":{"severity":0,"grave":false,"causes":[],"facts":[],"confidence":0,"mode":"retributive","confirmed_injury":0}}},{"system":"lethal_pressure","function":"lethality.LethalPressure.evaluate","result":{"available":false,"pressure":-99.06,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"response","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":15.13,"directed_emotion":0.0,"commitment":0.0,"sadism":0.0,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":42.35,"moral_restraint":6.359999999999999,"fear":28.15,"risk":7.326007326007325,"bond":0.0,"authority_or_witnesses":0.0,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{}},{"system":"capacity","function":"action_pressure.ActionPressureSystem.assess","result":{"eligible":true,"world_pressure":0,"action_pressure":0.0,"eligibility_causes":[],"source_facts":[],"capacity":10.0,"perceived_capacity":12.32,"major_barriers":[],"selected_alternative":"pursue"},"inputs":{}}].

**Evento:** nenhum evento retido durante esta decisão. Isso pode significar movimento/efeito sem evento; não implica falha.

**Aprendizado aceito durante a decisão (amostra):** [].

**Recibos posteriores ligados ao mesmo event_id:** []. Contagem é operações de aprendizado aceitas, não indivíduos únicos.

**Consequência imediata:** {"id":2927,"name":"Elena Alvor","hour":201,"alive":true,"profession":"ferreiro","lod":"active","position":{"map_id":414,"x":5,"y":5},"residence":414,"hp":30,"hunger":68,"thirst":42,"fatigue":100,"money":0,"food":0,"water":0,"local_food":4,"local_water":140,"recoverable_deprivation":70,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{"ask_help":207}}. **Observação/relações com o alvo ao final:** {"observation_end":null,"relations_end":[]}. Não usar esse estado posterior como entrada antiga nem atribuir consequências futuras sem vínculo causal.

### 19. social — Mira Alvor #437, h28: issue_local_order

**Pressão escolhida:** `military_service` #19880, prioridade 59.2868, base 55, fonte `known_local_case`, alvo 414. Motivo: Orientar segurança local por caso recebido.

**Contexto preservado:** {"source_event":50033}.

**Entrada:** {"id":437,"name":"Mira Alvor","hour":28,"alive":true,"profession":"guarda","lod":"local","position":{"map_id":414,"x":5,"y":5},"residence":414,"hp":100,"hunger":27,"thirst":18,"fatigue":44.600000000000016,"money":27,"food":2,"water":0,"local_food":210,"local_water":142,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{"crime:19847":26}}.

**Personalidade:** {"honesty":42,"compassion":56,"courage":20,"independence":28,"greed":24,"diligence":77,"family_loyalty":33,"persistence":14,"temperament":6,"vengefulness":88,"ambition":14,"sadism":0}. **Emoções escalares de entrada:** {"anger":0.0,"resentment":0.0,"humiliation":0.0,"desperation":0.0,"last_updated":24,"last_support":-10000,"strain":0,"adaptation":0,"last_adapted":0,"stable_material_hours":0,"nested_collections":"LACUNA: cópia rasa; histórico não utilizado"}.

**Conhecimento/locais de entrada:** {"known_places":{"market":{"map_id":414,"x":5,"y":9},"home":{"map_id":414,"x":2,"y":2},"work":{"map_id":414,"x":5,"y":9},"forage":{"map_id":414,"x":1,"y":9},"well_home":{"map_id":414,"x":2,"y":2},"well_rural":{"map_id":414,"x":1,"y":9},"sacred":{"map_id":414,"x":5,"y":1}},"known_towns":[414,302,443,461],"route_knowledge_count":6,"knowledge_ids_before":[46667,46668,46669,46670,46671,46672,46673,46674,46675,46676,46677,46678,46679,46680,46653,46652,46681,46686,46689,46690,46705,46707,26718,47744,48439,48440,48448,48450,48453,48463,50015,50031,50033,50052,50053,50055,50056,50058,50064,50065,50067,50068,50072,50073,50805,50806,50814,50815,50817,50818,50821,51452,51457,51458,51460,51461,51462,51469,51475,51476,51480,54414,43747,56714],"market_observation":{"turn":21,"town_id":414,"stock":{"food":207,"grain":128,"water":77,"iron":112,"wood":54},"temporary_work":false,"offers_expire_at":45,"training_offer":null,"price":2,"price_turn":21}}.

**Fatos-fonte retidos após percepção:** [{"event_id":50033,"kind":"WantedIssued","actor_id":437,"target_id":414,"location":{"map_id":414,"x":5,"y":9},"turn":19,"description":"Mira Alvor registrou procura por Nora Stone.","confidence":100,"required_trust":0,"source_id":null,"source_kind":"direct","context":{"record_id":50032,"suspect_id":2993,"source_fact":50031,"severity":1,"confidence":100,"last_known_location":{"map_id":414,"x":5,"y":9}}}].

| Need | ID/alvo | Base→prioridade | Estado/fonte |
| --- | --- | --- | --- |
| military_service | 19880/414 | 55→59.2868 | active / known_local_case |
| rest | 39146/None | 44.600000000000016→46.850000000000016 | active / physiology |

**Alternativas/gates realmente vistos:**

Need #19880 (`military_service`): 1 Solutions entraram em _evaluate; 1 saíram disponíveis. Entrada: `issue_local_order`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| issue_local_order | {"target":414,"destination":{"map_id":414,"x":5,"y":9}} | 52.0 | {"base":0.3,"travel":-0.04} | {"feeding":null,"action_pressure":null} |

**Escolhas intermediárias:** [{"chosen":{"action":"issue_local_order","score":52.0,"target":414,"destination":{"map_id":414,"x":5,"y":9},"terms":{"base":0.3,"travel":-0.04},"feeding":null,"action_pressure":null},"near_scores":[52.0],"variation_draws":"não capturados; RNG não consultado pelo observador"}].

**Preparação/substituição posterior:** [].

**Winner final / Goal:** {"winner":{"action":"issue_local_order","score":52.0,"target":414,"destination":{"map_id":414,"x":5,"y":9},"terms":{"base":0.3,"travel":-0.04},"feeding":null,"action_pressure":null},"goal":{"id":61900,"need_id":19880,"action":"issue_local_order","score":52.0,"created_at":28,"target_id":414,"destination":{"map_id":414,"x":5,"y":9},"status":"active","outcome":""},"suspended_before":null,"suspended_after":null}.

**Por que outras Needs não foram executadas:** a fila prioriza emergência/priority/ID e para na primeira solucionável, sujeita à continuidade/preparo. Outras pressões retidas: rest#39146(46.850000000000016). Não atribuir score global entre Needs.

**Execução:** execute não foi chamado neste trace. A Goal pode ter iniciado/continuado deslocamento; o snapshot e a posição posterior delimitam essa conclusão.

**Cálculos especializados reais:** [].

**Evento:** nenhum evento retido durante esta decisão. Isso pode significar movimento/efeito sem evento; não implica falha.

**Aprendizado aceito durante a decisão (amostra):** [].

**Recibos posteriores ligados ao mesmo event_id:** []. Contagem é operações de aprendizado aceitas, não indivíduos únicos.

**Consequência imediata:** {"id":437,"name":"Mira Alvor","hour":28,"alive":true,"profession":"guarda","lod":"local","position":{"map_id":414,"x":5,"y":9},"residence":414,"hp":100,"hunger":27,"thirst":18,"fatigue":44.600000000000016,"money":27,"food":2,"water":0,"local_food":210,"local_water":142,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{}}. **Observação/relações com o alvo ao final:** {"observation_end":null,"relations_end":[]}. Não usar esse estado posterior como entrada antiga nem atribuir consequências futuras sem vínculo causal.

### 20. travel — Nora Arven #3376, h21: route_travel

**Pressão escolhida:** `divine_contact` #23841, prioridade 50.300000000000004, base 47.6, fonte `personal_faith`, alvo 5909. Motivo: Buscar contato por devoção, ambição ou perda.

**Contexto preservado:** {"source_fact":null}.

**Entrada:** {"id":3376,"name":"Nora Arven","hour":21,"alive":true,"profession":"lenhador","lod":"local","position":{"map_id":526,"x":3,"y":5},"residence":526,"hp":100,"hunger":29,"thirst":42,"fatigue":36.199999999999996,"money":15,"food":2,"water":2,"local_food":125,"local_water":73,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{}}.

**Personalidade:** {"honesty":90,"compassion":17,"courage":27,"independence":76,"greed":76,"diligence":19,"family_loyalty":58,"persistence":67,"temperament":77,"vengefulness":58,"ambition":65,"sadism":0}. **Emoções escalares de entrada:** {"anger":0.0,"resentment":0.0,"humiliation":0.0,"desperation":0.0,"last_updated":15,"last_support":-10000,"strain":0,"adaptation":0,"last_adapted":0,"stable_material_hours":0,"nested_collections":"LACUNA: cópia rasa; histórico não utilizado"}.

**Conhecimento/locais de entrada:** {"known_places":{"market":{"map_id":526,"x":3,"y":5},"home":{"map_id":526,"x":2,"y":2},"work":{"map_id":526,"x":4,"y":2},"forage":{"map_id":526,"x":1,"y":5},"well_home":{"map_id":526,"x":2,"y":2},"well_rural":{"map_id":526,"x":1,"y":5},"sacred":{"map_id":526,"x":3,"y":1}},"known_towns":[526,479,302],"route_knowledge_count":2,"knowledge_ids_before":[9029,9030,9047,9048,12673,12672,18376,18377,23839,23842,23843,23845,25333,25334,25338,12671,28376,33443,35214,35227,9040,11781,37689,38425,38434,38435,38444,40148,40162,43012,43019,43847,45428,45430,9026,47765,47767,47770,48558,48563,48567,50145,50150],"market_observation":{"turn":15,"town_id":526,"stock":{"food":132,"grain":36,"water":80,"iron":84,"wood":41},"temporary_work":false,"offers_expire_at":39,"training_offer":null,"price":2,"price_turn":15}}.

**Fatos-fonte retidos após percepção:** [].

| Need | ID/alvo | Base→prioridade | Estado/fonte |
| --- | --- | --- | --- |
| divine_contact | 23841/5909 | 47.6→50.300000000000004 | active / personal_faith |
| advancement | 23838/None | 24.9726→45.93817988571429 | active / self_assessment:3 |
| water | 43857/None | 42→42.9 | active / physiology |
| religious_interest | 23840/5909 | 33.0→37.639 | active / own_faith |
| rest | 38442/None | 36.199999999999996→37.55 | active / physiology |

**Alternativas/gates realmente vistos:**

Need #23841 (`divine_contact`): 1 Solutions entraram em _evaluate; 1 saíram disponíveis. Entrada: `route_travel`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| route_travel | {"target":479,"destination":null} | 71.39999999999999 | {"base":0.29,"persistence":0.067,"risk":0.0,"travel":-0.0} | {"feeding":null,"action_pressure":null} |

Need #23838 (`advancement`): 1 Solutions entraram em _evaluate; 1 saíram disponíveis. Entrada: `work`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| work | {"target":null,"destination":{"map_id":526,"x":4,"y":2}} | 51.5 | {"base":0.25,"diligence":0.0475,"physical_depletion":0.0,"travel":-0.04} | {"feeding":null,"action_pressure":null} |

**Escolhas intermediárias:** [{"chosen":{"action":"route_travel","score":71.39999999999999,"target":479,"destination":null,"terms":{"base":0.29,"persistence":0.067,"risk":0.0,"travel":-0.0},"feeding":null,"action_pressure":null},"near_scores":[71.39999999999999],"variation_draws":"não capturados; RNG não consultado pelo observador"}].

**Preparação/substituição posterior:** [].

**Winner final / Goal:** {"winner":{"action":"route_travel","score":71.39999999999999,"target":479,"destination":null,"terms":{"base":0.29,"persistence":0.067,"risk":0.0,"travel":-0.0},"feeding":null,"action_pressure":null},"goal":{"id":53100,"need_id":23841,"action":"route_travel","score":71.39999999999999,"created_at":21,"target_id":479,"destination":null,"status":"completed","outcome":"Caminhada até a saída da localidade."},"suspended_before":null,"suspended_after":null}.

**Por que outras Needs não foram executadas:** a fila prioriza emergência/priority/ID e para na primeira solucionável, sujeita à continuidade/preparo. Outras pressões retidas: advancement#23838(45.93817988571429), water#43857(42.9), religious_interest#23840(37.639), rest#38442(37.55). Não atribuir score global entre Needs.

**Execução:** {"success":true,"result":[true,"Caminhada até a saída da localidade."],"goal_at_entry":{"id":53100,"need_id":23841,"action":"route_travel","score":71.39999999999999,"created_at":21,"target_id":479,"destination":null,"status":"active","outcome":""},"before":{"id":3376,"name":"Nora Arven","hour":21,"alive":true,"profession":"lenhador","lod":"local","position":{"map_id":526,"x":3,"y":5},"residence":526,"hp":100,"hunger":29,"thirst":42,"fatigue":36.199999999999996,"money":15,"food":2,"water":2,"local_food":125,"local_water":73,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{}},"after":{"id":3376,"name":"Nora Arven","hour":21,"alive":true,"profession":"lenhador","lod":"local","position":{"map_id":526,"x":3,"y":6},"residence":526,"hp":100,"hunger":29,"thirst":42,"fatigue":36.199999999999996,"money":15,"food":2,"water":2,"local_food":125,"local_water":73,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":{"origin":526,"destination":479,"route_ids":[5932],"nodes":[526,479],"reason":"divine_contact","started_at":21,"mode":"known_route","guide_id":null,"leg":0,"offset":0,"last_step":21,"entering":false,"known_at_start":[{"actor":3376,"origin":526,"destination":479,"route_id":5932,"confidence":100,"source":"initial_local_life","learned_at":0,"last_used_at":-1,"source_id":null,"travel_time":4,"danger":4,"condition":"open"}]},"failures":{}}}.

**Cálculos especializados reais:** [{"system":"journey_begin","function":"geography.Geography.begin","result":[true,"Viagem planejada exclusivamente pelas conexões conhecidas."],"inputs":{"mode":"known_route","reason":"divine_contact"}},{"system":"journey_step","function":"geography.Geography.step","result":[true,"Caminhada até a saída da localidade."],"inputs":{}}].

| Evento/hora | Actor→target | Emissor | Testemunhas | Contexto |
| --- | --- | --- | --- | --- |
| 53101 / 21 / JourneyStarted | 3376→479 | ["geography.Geography.emit","geography.Geography.begin","geography.Geography.travel"] | [535,538,541,3341,3344,3350,3356,3358,3361,3367,3376,3379] | {"origin":526,"reason":"divine_contact","mode":"known_route","guide_id":null,"route_ids":[5932],"nodes":[526,479],"known_at_start":[{"actor":3376,"origin":526,"destination":479,"route_id":5932,"confidence":100,"source":"initial_local_life","learned_at":0,"last_used_at":-1,"source_id":null,"travel_time":4,"danger":4,"condition":"open"}],"food_owned":2,"water_owned":2,"required_food":2,"required_water":1,"estimated_hours":14,"toll":0} |
| 53102 / 21 / SacredJourney | 3376→479 | ["geography.Geography.emit","geography.Geography.begin","geography.Geography.travel"] | [535,538,541,3341,3344,3350,3356,3358,3361,3367,3376,3379] | {"route_ids":[5932]} |

**Aprendizado aceito durante a decisão (amostra):** [{"npc":535,"event":53101,"kind":"JourneyStarted","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":538,"event":53101,"kind":"JourneyStarted","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":541,"event":53101,"kind":"JourneyStarted","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":3341,"event":53101,"kind":"JourneyStarted","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":3344,"event":53101,"kind":"JourneyStarted","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":3350,"event":53101,"kind":"JourneyStarted","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":3356,"event":53101,"kind":"JourneyStarted","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":3358,"event":53101,"kind":"JourneyStarted","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":3361,"event":53101,"kind":"JourneyStarted","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":3367,"event":53101,"kind":"JourneyStarted","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":3376,"event":53101,"kind":"JourneyStarted","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":3379,"event":53101,"kind":"JourneyStarted","source":null,"firsthand":true,"confidence":100,"latency":0}].

**Recibos posteriores ligados ao mesmo event_id:** [{"event":53101,"kind":"JourneyStarted","learned":{"count":13,"first":21,"last":72,"first_people":[535,538,541,3341,3344,3350]}},{"event":53102,"kind":"SacredJourney","learned":{"count":14,"first":21,"last":78,"first_people":[535,538,541,3341,3344,3350]}}]. Contagem é operações de aprendizado aceitas, não indivíduos únicos.

**Consequência imediata:** {"id":3376,"name":"Nora Arven","hour":21,"alive":true,"profession":"lenhador","lod":"local","position":{"map_id":526,"x":3,"y":6},"residence":526,"hp":100,"hunger":29,"thirst":42,"fatigue":36.199999999999996,"money":15,"food":2,"water":2,"local_food":125,"local_water":73,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":{"origin":526,"destination":479,"route_ids":[5932],"nodes":[526,479],"reason":"divine_contact","started_at":21,"mode":"known_route","guide_id":null,"leg":0,"offset":0,"last_step":21,"entering":false,"known_at_start":[{"actor":3376,"origin":526,"destination":479,"route_id":5932,"confidence":100,"source":"initial_local_life","learned_at":0,"last_used_at":-1,"source_id":null,"travel_time":4,"danger":4,"condition":"open"}]},"failures":{}}. **Observação/relações com o alvo ao final:** {"observation_end":null,"relations_end":[]}. Não usar esse estado posterior como entrada antiga nem atribuir consequências futuras sem vínculo causal.

### 21. water — Tomas Vale #5856, h260: drink

**Pressão escolhida:** `water` #42802, prioridade 73.15, base 70, fonte `physiology`, alvo None. Motivo: Sede.

**Contexto preservado:** {"emergency":false}.

**Entrada:** {"id":5856,"name":"Tomas Vale","hour":260,"alive":true,"profession":"ferreiro","lod":"local","position":{"map_id":1135,"x":2,"y":2},"residence":1135,"hp":100,"hunger":51,"thirst":70,"fatigue":45.60000000000044,"money":0,"food":0,"water":2,"local_food":100,"local_water":147,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{"work":263,"steal_person":269}}.

**Personalidade:** {"honesty":54,"compassion":29,"courage":16,"independence":34,"greed":49,"diligence":16,"family_loyalty":55,"persistence":31,"temperament":41,"vengefulness":80,"ambition":47,"sadism":0}. **Emoções escalares de entrada:** {"anger":7.199999999999996,"resentment":8.46000000000001,"humiliation":5.400000000000002,"desperation":10.35,"last_updated":257,"last_support":-10000,"strain":24.4485,"adaptation":0,"last_adapted":0,"stable_material_hours":0,"nested_collections":"LACUNA: cópia rasa; histórico não utilizado"}.

**Conhecimento/locais de entrada:** {"known_places":{"market":{"map_id":1135,"x":3,"y":5},"home":{"map_id":1135,"x":2,"y":2},"work":{"map_id":1135,"x":4,"y":2},"forage":{"map_id":1135,"x":1,"y":5},"well_home":{"map_id":1135,"x":2,"y":2},"well_rural":{"map_id":1135,"x":1,"y":5},"sacred":{"map_id":1135,"x":3,"y":1}},"known_towns":[1135,1088,864],"route_knowledge_count":2,"knowledge_ids_before":[235274,238417,238421,222397,201152,238607,238608,238610,245142,245147,208857,245340,246454,246461,248806,248808,248813,250119,252577,252578,254114,254122,256347,256351,257421,259396,160764,262637,263543,265685,265688,269048,272453,272455,242854,273750,276159,279728,228987,286344,286348,286350,287414,287417,288527,289558,289570,289572,289575,290630,290633,290640,290642,303419,305411,308865,311833,181820,298886,239530,312982,315019,308862,299110],"market_observation":{"turn":254,"town_id":1135,"stock":{"food":100,"grain":66,"water":156,"iron":112,"wood":120},"temporary_work":true,"offers_expire_at":278,"training_offer":null,"price":2,"price_turn":226}}.

**Fatos-fonte retidos após percepção:** [{"event_id":289558,"kind":"ItemStolen","actor_id":5836,"target_id":1135,"location":{"map_id":1135,"x":3,"y":5},"turn":224,"description":"Darin Vale roubou comida no mercado de Dorria.","confidence":100,"required_trust":0,"source_id":null,"source_kind":"direct","context":{"item_id":289557,"item_kind":"food"}}].

| Need | ID/alvo | Base→prioridade | Estado/fonte |
| --- | --- | --- | --- |
| water | 42802/None | 70→73.15 | active / physiology |
| money | 192481/None | 57.0→69.06400000000001 | active / economy |
| food_reserve | 56585/None | 41.0→64.77358490566037 | active / food_reserve |
| political_pressure | 217485/None | 51.05→62.295199999999994 | active / own_shared_problem |
| migration | 217484/1088 | 52→58.263999999999996 | active / known_towns |
| food | 42801/None | 56.5→57.4 | active / physiology |
| revenge | 289559/5836 | 30.0→54.427 | active / event:289558 |
| protection | 215277/5856 | 30→50.346999999999994 | active / event:289558 |
| rest | 47430/None | 45.60000000000044→47.85000000000044 | active / physiology |
| advancement | 37474/None | 22.3482→45.84182054857143 | blocked / aspiration:wealth |
| religious_interest | 37475/5907 | 36.0→45.4546 | active / own_faith |

**Alternativas/gates realmente vistos:**

Need #42802 (`water`): 4 Solutions entraram em _evaluate; 4 saíram disponíveis. Entrada: `drink, drink_well, drink_well, drink_well`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| drink | {"target":null,"destination":null} | 200.0 | {"base":1.0,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| drink_well | {"target":null,"destination":{"map_id":1135,"x":2,"y":2}} | 100.0 | {"base":0.5,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| drink_well | {"target":null,"destination":{"map_id":1135,"x":3,"y":5}} | 92.0 | {"base":0.5,"travel":-0.04} | {"feeding":null,"action_pressure":null} |
| drink_well | {"target":null,"destination":{"map_id":1135,"x":1,"y":5}} | 92.0 | {"base":0.5,"travel":-0.04} | {"feeding":null,"action_pressure":null} |

Need #289559 (`revenge`): 5 Solutions entraram em _evaluate; 5 saíram disponíveis. Entrada: `investigate, denounce, denounce, avoid_threat, pursue`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| investigate | {"target":5836,"destination":{"map_id":1135,"x":3,"y":5}} | 86.8 | {"base":0.225,"vengefulness":0.16,"courage":0.032,"independence":0.051000000000000004,"compassion":-0.014499999999999999,"temperament":0.020499999999999997,"travel":-0.04} | {"feeding":null,"action_pressure":null} |
| denounce | {"target":1147,"destination":{"map_id":1135,"x":2,"y":2}} | 84.80000000000001 | {"base":0.225,"honesty":0.09450000000000001,"vengefulness":0.08,"courage":0.012,"trust":0.0125,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| denounce | {"target":5844,"destination":{"map_id":1135,"x":2,"y":2}} | 84.80000000000001 | {"base":0.225,"honesty":0.09450000000000001,"vengefulness":0.08,"courage":0.012,"trust":0.0125,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| pursue | {"target":5836,"destination":{"map_id":1135,"x":2,"y":2}} | 77.22672554285714 | {"base":0.275,"courage":0.016,"diligence":0.012,"vengefulness":0.08,"critical_depletion":0.0,"travel":-0.0,"action_pressure":0.0,"pressure_risk_tolerance":0.003133627714285714} | {"feeding":null,"action_pressure":{"eligible":true,"world_pressure":0,"action_pressure":0.0,"eligibility_causes":[],"source_facts":[],"capacity":69.6,"perceived_capacity":50.67,"major_barriers":[],"selected_alternative":"pursue"}} |
| avoid_threat | {"target":null,"destination":{"map_id":1135,"x":2,"y":2}} | 21.950000000000003 | {"base":0.2,"courage":-0.032,"compassion":0.02175,"vengefulness":-0.08,"travel":-0.0} | {"feeding":null,"action_pressure":null} |

Need #215277 (`protection`): 4 Solutions entraram em _evaluate; 4 saíram disponíveis. Entrada: `denounce, denounce, avoid_threat, pursue`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| denounce | {"target":1147,"destination":{"map_id":1135,"x":2,"y":2}} | 84.80000000000001 | {"base":0.225,"honesty":0.09450000000000001,"vengefulness":0.08,"courage":0.012,"trust":0.0125,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| denounce | {"target":5844,"destination":{"map_id":1135,"x":2,"y":2}} | 84.80000000000001 | {"base":0.225,"honesty":0.09450000000000001,"vengefulness":0.08,"courage":0.012,"trust":0.0125,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| pursue | {"target":5836,"destination":{"map_id":1135,"x":2,"y":2}} | 77.03952554285713 | {"base":0.275,"courage":0.016,"diligence":0.012,"vengefulness":0.08,"critical_depletion":0.0,"travel":-0.0,"action_pressure":0.0,"pressure_risk_tolerance":0.002197627714285713} | {"feeding":null,"action_pressure":{"eligible":true,"world_pressure":0,"action_pressure":0.0,"eligibility_causes":[],"source_facts":[],"capacity":69.6,"perceived_capacity":50.67,"major_barriers":[],"selected_alternative":"pursue"}} |
| avoid_threat | {"target":null,"destination":{"map_id":1135,"x":2,"y":2}} | 21.950000000000003 | {"base":0.2,"courage":-0.032,"compassion":0.02175,"vengefulness":-0.08,"travel":-0.0} | {"feeding":null,"action_pressure":null} |

Need #37474 (`advancement`): 2 Solutions entraram em _evaluate; 1 saíram disponíveis. Entrada: `work, work_for_food`.

| Opção | Alvo | Etapa | Motivo observado | Auditoria/feeding |
| --- | --- | --- | --- | --- |
| work | None | before_Utility_or_unresolved | cooldown_after_failure | {"pressure":null,"feeding":null} |

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| work_for_food | {"target":null,"destination":{"map_id":1135,"x":1,"y":5}} | 41.0 | {"base":0.225,"diligence":0.02,"physical_depletion":0.0,"travel":-0.04,"no_progress":0.0} | {"feeding":null,"action_pressure":null} |

**Escolhas intermediárias:** [{"chosen":{"action":"drink","score":200.0,"target":null,"destination":null,"terms":{"base":1.0,"travel":-0.0},"feeding":null,"action_pressure":null},"near_scores":[200.0,100.0,92.0,92.0],"variation_draws":"não capturados; RNG não consultado pelo observador"}].

**Preparação/substituição posterior:** [].

**Winner final / Goal:** {"winner":{"action":"drink","score":200.0,"target":null,"destination":null,"terms":{"base":1.0,"travel":-0.0},"feeding":null,"action_pressure":null},"goal":{"id":326995,"need_id":42802,"action":"drink","score":200.0,"created_at":260,"target_id":null,"destination":null,"status":"completed","outcome":"Sede reduzida."},"suspended_before":null,"suspended_after":null}.

**Por que outras Needs não foram executadas:** a fila prioriza emergência/priority/ID e para na primeira solucionável, sujeita à continuidade/preparo. Outras pressões retidas: money#192481(69.06400000000001), food_reserve#56585(64.77358490566037), political_pressure#217485(62.295199999999994), migration#217484(58.263999999999996), food#42801(57.4), revenge#289559(54.427), protection#215277(50.346999999999994), rest#47430(47.85000000000044), advancement#37474(45.84182054857143), religious_interest#37475(45.4546). Não atribuir score global entre Needs.

**Execução:** {"success":true,"result":[true,"Sede reduzida."],"goal_at_entry":{"id":326995,"need_id":42802,"action":"drink","score":200.0,"created_at":260,"target_id":null,"destination":null,"status":"active","outcome":""},"before":{"id":5856,"name":"Tomas Vale","hour":260,"alive":true,"profession":"ferreiro","lod":"local","position":{"map_id":1135,"x":2,"y":2},"residence":1135,"hp":100,"hunger":51,"thirst":70,"fatigue":45.60000000000044,"money":0,"food":0,"water":2,"local_food":100,"local_water":147,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{"work":263,"steal_person":269}},"after":{"id":5856,"name":"Tomas Vale","hour":260,"alive":true,"profession":"ferreiro","lod":"local","position":{"map_id":1135,"x":2,"y":2},"residence":1135,"hp":100,"hunger":51,"thirst":25,"fatigue":45.60000000000044,"money":0,"food":0,"water":1,"local_food":100,"local_water":147,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{"work":263,"steal_person":269}}}.

**Cálculos especializados reais:** [{"system":"lethal_decision","function":"lethal_decisions.LethalDecisionSystem.evaluate","result":{"available":false,"pressure":-43.22,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"protection","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":13.600000000000001,"directed_emotion":1.6104000000000007,"commitment":0.0,"sadism":0.0,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":15.950000000000001,"moral_restraint":6.4799999999999995,"fear":0.0,"risk":6.0,"bond":0.0,"authority_or_witnesses":0.0,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{"pressure":-43.22,"cause":{"severity":0,"grave":false,"causes":[],"facts":[],"confidence":0,"mode":"retributive","confirmed_injury":0}}},{"system":"lethal_decision","function":"lethal_decisions.LethalDecisionSystem.evaluate","result":{"available":false,"pressure":-43.22,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"protection","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":13.600000000000001,"directed_emotion":1.6104000000000007,"commitment":0.0,"sadism":0.0,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":15.950000000000001,"moral_restraint":6.4799999999999995,"fear":0.0,"risk":6.0,"bond":0.0,"authority_or_witnesses":0.0,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{"pressure":-43.22,"cause":{"severity":0,"grave":false,"causes":[],"facts":[],"confidence":0,"mode":"retributive","confirmed_injury":0}}},{"system":"lethal_pressure","function":"lethality.LethalPressure.evaluate","result":{"available":false,"pressure":-43.22,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"protection","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":13.600000000000001,"directed_emotion":1.6104000000000007,"commitment":0.0,"sadism":0.0,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":15.950000000000001,"moral_restraint":6.4799999999999995,"fear":0.0,"risk":6.0,"bond":0.0,"authority_or_witnesses":0.0,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{}},{"system":"lethal_decision","function":"lethal_decisions.LethalDecisionSystem.evaluate","result":{"available":false,"pressure":-43.22,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"revenge","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":13.600000000000001,"directed_emotion":1.6104000000000007,"commitment":0.0,"sadism":0.0,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":15.950000000000001,"moral_restraint":6.4799999999999995,"fear":0.0,"risk":6.0,"bond":0.0,"authority_or_witnesses":0.0,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{"pressure":-43.22,"cause":{"severity":0,"grave":false,"causes":[],"facts":[],"confidence":0,"mode":"retributive","confirmed_injury":0}}},{"system":"lethal_decision","function":"lethal_decisions.LethalDecisionSystem.evaluate","result":{"available":false,"pressure":-43.22,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"revenge","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":13.600000000000001,"directed_emotion":1.6104000000000007,"commitment":0.0,"sadism":0.0,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":15.950000000000001,"moral_restraint":6.4799999999999995,"fear":0.0,"risk":6.0,"bond":0.0,"authority_or_witnesses":0.0,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{"pressure":-43.22,"cause":{"severity":0,"grave":false,"causes":[],"facts":[],"confidence":0,"mode":"retributive","confirmed_injury":0}}},{"system":"lethal_pressure","function":"lethality.LethalPressure.evaluate","result":{"available":false,"pressure":-43.22,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"revenge","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":13.600000000000001,"directed_emotion":1.6104000000000007,"commitment":0.0,"sadism":0.0,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":15.950000000000001,"moral_restraint":6.4799999999999995,"fear":0.0,"risk":6.0,"bond":0.0,"authority_or_witnesses":0.0,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{}},{"system":"capacity","function":"action_pressure.ActionPressureSystem.assess","result":{"eligible":true,"world_pressure":0,"action_pressure":0.0,"eligibility_causes":[],"source_facts":[],"capacity":69.6,"perceived_capacity":50.67,"major_barriers":[],"selected_alternative":"pursue"},"inputs":{}},{"system":"capacity","function":"action_pressure.ActionPressureSystem.assess","result":{"eligible":true,"world_pressure":0,"action_pressure":0.0,"eligibility_causes":[],"source_facts":[],"capacity":69.6,"perceived_capacity":50.67,"major_barriers":[],"selected_alternative":"pursue"},"inputs":{}}].

**Evento:** nenhum evento retido durante esta decisão. Isso pode significar movimento/efeito sem evento; não implica falha.

**Aprendizado aceito durante a decisão (amostra):** [].

**Recibos posteriores ligados ao mesmo event_id:** []. Contagem é operações de aprendizado aceitas, não indivíduos únicos.

**Consequência imediata:** {"id":5856,"name":"Tomas Vale","hour":260,"alive":true,"profession":"ferreiro","lod":"local","position":{"map_id":1135,"x":2,"y":2},"residence":1135,"hp":100,"hunger":51,"thirst":25,"fatigue":45.60000000000044,"money":0,"food":0,"water":1,"local_food":100,"local_water":147,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{"work":263,"steal_person":269}}. **Observação/relações com o alvo ao final:** {"observation_end":null,"relations_end":[]}. Não usar esse estado posterior como entrada antiga nem atribuir consequências futuras sem vínculo causal.

### 22. work — Cael Hammer #4155, h11: work

**Pressão escolhida:** `work` #31852, prioridade 44.050000000000004, base 35, fonte `profession`, alvo None. Motivo: Responsabilidade profissional.

**Contexto preservado:** {}.

**Entrada:** {"id":4155,"name":"Cael Hammer","hour":11,"alive":true,"profession":"guarda","lod":"active","position":{"map_id":695,"x":5,"y":9},"residence":695,"hp":100,"hunger":15,"thirst":22,"fatigue":13.199999999999998,"money":10,"food":1,"water":0,"local_food":119,"local_water":80,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{}}.

**Personalidade:** {"honesty":85,"compassion":65,"courage":91,"independence":57,"greed":35,"diligence":43,"family_loyalty":47,"persistence":72,"temperament":53,"vengefulness":28,"ambition":53,"sadism":23}. **Emoções escalares de entrada:** {"anger":0.0,"resentment":0.0,"humiliation":0.0,"desperation":0.0,"last_updated":10,"last_support":-10000,"strain":0,"adaptation":0,"last_adapted":0,"stable_material_hours":0,"nested_collections":"LACUNA: cópia rasa; histórico não utilizado"}.

**Conhecimento/locais de entrada:** {"known_places":{"market":{"map_id":695,"x":5,"y":9},"home":{"map_id":695,"x":2,"y":2},"work":{"map_id":695,"x":5,"y":9},"forage":{"map_id":695,"x":1,"y":9},"well_home":{"map_id":695,"x":2,"y":2},"well_rural":{"map_id":695,"x":1,"y":9},"sacred":{"map_id":695,"x":5,"y":1}},"known_towns":[695,601,724,742,3],"route_knowledge_count":6,"knowledge_ids_before":[9849,9850,9879,9880,9881,9882,9883,9884,9893,9894,9929,9930,9931,9932,9933,9934,11859,11860,11861,11862,11858,11857,11856,11855,11854,11853,11852,11851,11850,11849,16785,16800,16808,16815,18810,21835,21856,21865,23181,24724,25607,27174,27187,23178,27802,29071,29077,29075,29082,29089,29998,30013,30016,30633,30636,31847,31855,32579,33670,34341,34344,35513,35522,36079],"market_observation":{"turn":10,"town_id":695,"stock":{"food":102,"grain":55,"water":80,"iron":52,"wood":37},"temporary_work":false,"offers_expire_at":34,"training_offer":null,"price":2,"price_turn":10}}.

**Fatos-fonte retidos após percepção:** [].

| Need | ID/alvo | Base→prioridade | Estado/fonte |
| --- | --- | --- | --- |
| work | 31852/None | 35→44.050000000000004 | active / profession |
| status | 21857/None | 22.8198→38.460765942857144 | active / aspiration:recognition |
| food_reserve | 21853/None | 33.0→38.0 | active / food_reserve |

**Alternativas/gates realmente vistos:**

Need #31852 (`work`): 1 Solutions entraram em _evaluate; 1 saíram disponíveis. Entrada: `work`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| work | {"target":null,"destination":{"map_id":695,"x":5,"y":9}} | 71.5 | {"base":0.25,"diligence":0.1075,"physical_depletion":0.0,"travel":-0.0} | {"feeding":null,"action_pressure":null} |

Need #21857 (`status`): 1 Solutions entraram em _evaluate; 1 saíram disponíveis. Entrada: `work`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| work | {"target":null,"destination":{"map_id":695,"x":5,"y":9}} | 71.5 | {"base":0.25,"diligence":0.1075,"physical_depletion":0.0,"travel":-0.0} | {"feeding":null,"action_pressure":null} |

**Escolhas intermediárias:** [{"chosen":{"action":"work","score":71.5,"target":null,"destination":{"map_id":695,"x":5,"y":9},"terms":{"base":0.25,"diligence":0.1075,"physical_depletion":0.0,"travel":-0.0},"feeding":null,"action_pressure":null},"near_scores":[71.5],"variation_draws":"não capturados; RNG não consultado pelo observador"}].

**Preparação/substituição posterior:** [].

**Winner final / Goal:** {"winner":{"action":"work","score":71.5,"target":null,"destination":{"map_id":695,"x":5,"y":9},"terms":{"base":0.25,"diligence":0.1075,"physical_depletion":0.0,"travel":-0.0},"feeding":null,"action_pressure":null},"goal":{"id":36969,"need_id":31852,"action":"work","score":71.5,"created_at":11,"target_id":null,"destination":{"map_id":695,"x":5,"y":9},"status":"completed","outcome":"Serviço realizado."},"suspended_before":null,"suspended_after":null}.

**Por que outras Needs não foram executadas:** a fila prioriza emergência/priority/ID e para na primeira solucionável, sujeita à continuidade/preparo. Outras pressões retidas: status#21857(38.460765942857144), food_reserve#21853(38.0). Não atribuir score global entre Needs.

**Execução:** {"success":true,"result":[true,"Serviço realizado."],"goal_at_entry":{"id":36969,"need_id":31852,"action":"work","score":71.5,"created_at":11,"target_id":null,"destination":{"map_id":695,"x":5,"y":9},"status":"active","outcome":""},"before":{"id":4155,"name":"Cael Hammer","hour":11,"alive":true,"profession":"guarda","lod":"active","position":{"map_id":695,"x":5,"y":9},"residence":695,"hp":100,"hunger":15,"thirst":22,"fatigue":13.199999999999998,"money":10,"food":1,"water":0,"local_food":119,"local_water":80,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{}},"after":{"id":4155,"name":"Cael Hammer","hour":11,"alive":true,"profession":"guarda","lod":"active","position":{"map_id":695,"x":5,"y":9},"residence":695,"hp":100,"hunger":15,"thirst":22,"fatigue":13.199999999999998,"money":11,"food":1,"water":0,"local_food":119,"local_water":80,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{}}}.

**Cálculos especializados reais:** [{"system":"work","actual":{"actor":4155,"town":695,"money_before":10,"treasury_before":1397,"inputs_before":{"food":119,"grain":58,"iron":58,"wood":55},"result":{"status":"paid","message":"Serviço realizado.","produced":0,"paid":1,"credit_added":6}}}].

**Evento:** nenhum evento retido durante esta decisão. Isso pode significar movimento/efeito sem evento; não implica falha.

**Aprendizado aceito durante a decisão (amostra):** [].

**Recibos posteriores ligados ao mesmo event_id:** []. Contagem é operações de aprendizado aceitas, não indivíduos únicos.

**Consequência imediata:** {"id":4155,"name":"Cael Hammer","hour":11,"alive":true,"profession":"guarda","lod":"active","position":{"map_id":695,"x":5,"y":9},"residence":695,"hp":100,"hunger":15,"thirst":22,"fatigue":13.199999999999998,"money":11,"food":1,"water":0,"local_food":119,"local_water":80,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{}}. **Observação/relações com o alvo ao final:** {"observation_end":null,"relations_end":[]}. Não usar esse estado posterior como entrada antiga nem atribuir consequências futuras sem vínculo causal.

### 23. blocked — Marie Stone #4385, h7: sem seleção

**Sem seleção viável** no retorno de decide. Isso não demonstra ausência de todas as pressões: examinar Needs e avaliações abaixo.

**Entrada:** {"id":4385,"name":"Marie Stone","hour":7,"alive":true,"profession":"guarda","lod":"active","position":{"map_id":760,"x":5,"y":7},"residence":760,"hp":100,"hunger":34,"thirst":14,"fatigue":11.399999999999999,"money":12,"food":2,"water":0,"local_food":52,"local_water":80,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{"crime:25633":28}}.

**Personalidade:** {"honesty":55,"compassion":35,"courage":87,"independence":78,"greed":8,"diligence":23,"family_loyalty":86,"persistence":70,"temperament":28,"vengefulness":18,"ambition":37,"sadism":0}. **Emoções escalares de entrada:** {"anger":0.0,"resentment":0.0,"humiliation":0.0,"desperation":0.0,"last_updated":6,"last_support":5,"strain":0,"adaptation":0,"last_adapted":0,"stable_material_hours":0,"nested_collections":"LACUNA: cópia rasa; histórico não utilizado"}.

**Conhecimento/locais de entrada:** {"known_places":{"market":{"map_id":760,"x":5,"y":9},"home":{"map_id":760,"x":2,"y":2},"work":{"map_id":760,"x":5,"y":9},"forage":{"map_id":760,"x":1,"y":9},"well_home":{"map_id":760,"x":2,"y":2},"well_rural":{"map_id":760,"x":1,"y":9},"sacred":{"map_id":760,"x":5,"y":1}},"known_towns":[760,601,789,3],"route_knowledge_count":4,"knowledge_ids_before":[10036,10065,10066,10067,10068,10091,10092,10093,10094,10101,10102,10131,10132,10133,10134,11885,11886,11887,11888,11884,11883,11882,11881,11880,11879,11878,11877,11876,11875,13829,13837,13843,13853,13861,15645,18855,18881,18918,18916,20007,20013,20015,21962,22063,22069,23209,23211,23219,23226,23228,24113,24116,24727,25633,25642,25650,25671,25677,26189,27230,27232,27245,24118,28612],"market_observation":{"turn":5,"town_id":760,"stock":{"food":47,"grain":50,"water":80,"iron":40,"wood":23},"temporary_work":false,"offers_expire_at":29,"training_offer":null,"price":2,"price_turn":5}}.

**Fatos-fonte retidos após percepção:** [].

| Need | ID/alvo | Base→prioridade | Estado/fonte |
| --- | --- | --- | --- |

**Alternativas/gates realmente vistos:**

**Escolhas intermediárias:** [].

**Preparação/substituição posterior:** [].

**Winner final / Goal:** {"winner":{},"goal":null,"suspended_before":null,"suspended_after":null}.

**Execução:** execute não foi chamado neste trace. A Goal pode ter iniciado/continuado deslocamento; o snapshot e a posição posterior delimitam essa conclusão.

**Cálculos especializados reais:** [].

**Evento:** nenhum evento retido durante esta decisão. Isso pode significar movimento/efeito sem evento; não implica falha.

**Aprendizado aceito durante a decisão (amostra):** [].

**Recibos posteriores ligados ao mesmo event_id:** []. Contagem é operações de aprendizado aceitas, não indivíduos únicos.

**Consequência imediata:** {"id":4385,"name":"Marie Stone","hour":7,"alive":true,"profession":"guarda","lod":"active","position":{"map_id":760,"x":5,"y":6},"residence":760,"hp":100,"hunger":34,"thirst":14,"fatigue":11.399999999999999,"money":12,"food":2,"water":0,"local_food":52,"local_water":80,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{"crime:25633":28}}. **Observação/relações com o alvo ao final:** {"observation_end":null,"relations_end":[]}. Não usar esse estado posterior como entrada antiga nem atribuir consequências futuras sem vínculo causal.

### 24. career — Tomas Valerius #4029, h50: work

**Pressão escolhida:** `advancement` #21778, prioridade 64.90804886857143, base 28.1334, fonte `self_assessment:2`, alvo None. Motivo: Acumular uma reserva maior com trabalho e comércio disponíveis.

**Contexto preservado:** {"diagnostic":{"reason":"Selected","competing":null,"turn":50}}.

**Entrada:** {"id":4029,"name":"Tomas Valerius","hour":50,"alive":true,"profession":"agricultor","lod":"local","position":{"map_id":677,"x":2,"y":2},"residence":677,"hp":100,"hunger":39,"thirst":55,"fatigue":50.000000000000085,"money":58,"food":0,"water":0,"local_food":108,"local_water":159,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{}}.

**Personalidade:** {"honesty":13,"compassion":81,"courage":73,"independence":77,"greed":92,"diligence":43,"family_loyalty":13,"persistence":50,"temperament":93,"vengefulness":65,"ambition":93,"sadism":0}. **Emoções escalares de entrada:** {"anger":0.0,"resentment":0.0,"humiliation":0.0,"desperation":0.0,"last_updated":44,"last_support":-10000,"strain":0,"adaptation":0,"last_adapted":0,"stable_material_hours":0,"nested_collections":"LACUNA: cópia rasa; histórico não utilizado"}.

**Conhecimento/locais de entrada:** {"known_places":{"market":{"map_id":677,"x":3,"y":5},"home":{"map_id":677,"x":2,"y":2},"work":{"map_id":677,"x":1,"y":5},"forage":{"map_id":677,"x":1,"y":5},"well_home":{"map_id":677,"x":2,"y":2},"well_rural":{"map_id":677,"x":1,"y":5},"sacred":{"map_id":677,"x":3,"y":1}},"known_towns":[677,648,3],"route_knowledge_count":2,"knowledge_ids_before":[9751,9752,21779,21781,21784,21785,24704,24713,6468,29060,29066,31825,31826,34322,34329,36940,36941,39215,39217,42202,42203,46950,46952,6466,49538,51718,51719,53846,11844,58201,60313,60314,64210,64211,46954,68397,70077,71901,71902,75473,75475,80785,11843,88134,88135,88133,88132],"market_observation":{"turn":44,"town_id":677,"stock":{"food":112,"grain":76,"water":140,"iron":70,"wood":51},"temporary_work":false,"offers_expire_at":68,"training_offer":null}}.

**Fatos-fonte retidos após percepção:** [{"event_id":90185,"kind":"FamilyConcern","actor_id":4029,"target_id":4032,"location":{"map_id":677,"x":2,"y":2},"turn":50,"description":"Tomas Valerius percebeu a privação de Tomas Valerius.","confidence":100,"required_trust":0,"source_id":null,"source_kind":"direct","context":{"observed_need":55}}].

| Need | ID/alvo | Base→prioridade | Estado/fonte |
| --- | --- | --- | --- |
| advancement | 21778/None | 28.1334→64.90804886857143 | selected / self_assessment:2 |
| food_reserve | 51716/None | 41.0→64.29411764705883 | active / food_reserve |
| family | 90186/4032 | 52.7→63.35800000000001 | active / event:90185 |
| water | 42200/None | 55→57.25 | active / physiology |
| rest | 36938/None | 50.000000000000085→55.85000000000009 | active / physiology |
| religious_interest | 21782/5908 | 25.0→33.9108 | active / own_faith |
| food | 31822/None | 32→32.0 | active / physiology |

**Alternativas/gates realmente vistos:**

Need #21778 (`advancement`): 3 Solutions entraram em _evaluate; 3 saíram disponíveis. Entrada: `work, steal_person, steal_person`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| work | {"target":null,"destination":{"map_id":677,"x":1,"y":5}} | 63.5 | {"base":0.25,"diligence":0.1075,"physical_depletion":0.0,"travel":-0.04,"no_progress":0.0} | {"feeding":null,"action_pressure":null} |
| steal_person | {"target":4044,"destination":null} | 56.129189756277555 | {"base":0.31,"greed":0.18400000000000002,"honesty":-0.0585,"authority":-0.2,"courage":0.0365,"travel":-0.0,"no_progress":0.0,"pressure_moral_tolerance":0.008645948781387757} | {"feeding":null,"action_pressure":null} |
| steal_person | {"target":4067,"destination":null} | 56.129189756277555 | {"base":0.31,"greed":0.18400000000000002,"honesty":-0.0585,"authority":-0.2,"courage":0.0365,"travel":-0.0,"no_progress":0.0,"pressure_moral_tolerance":0.008645948781387757} | {"feeding":null,"action_pressure":null} |

Need #90186 (`family`): 1 Solutions entraram em _evaluate; 1 saíram disponíveis. Entrada: `ask_personal_help`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| ask_personal_help | {"target":4032,"destination":null} | 36.300000000000004 | {"base":0.125,"independence":-0.1155,"compassion":0.08100000000000002,"trust":0.07,"reputation":0.0,"relationship":0.021,"travel":-0.0,"known_reputation":-0.0} | {"feeding":null,"action_pressure":null} |

**Escolhas intermediárias:** [{"chosen":{"action":"work","score":63.5,"target":null,"destination":{"map_id":677,"x":1,"y":5},"terms":{"base":0.25,"diligence":0.1075,"physical_depletion":0.0,"travel":-0.04,"no_progress":0.0},"feeding":null,"action_pressure":null},"near_scores":[63.5,56.129189756277555,56.129189756277555],"variation_draws":"não capturados; RNG não consultado pelo observador"}].

**Preparação/substituição posterior:** [].

**Winner final / Goal:** {"winner":{"action":"work","score":63.5,"target":null,"destination":{"map_id":677,"x":1,"y":5},"terms":{"base":0.25,"diligence":0.1075,"physical_depletion":0.0,"travel":-0.04,"no_progress":0.0},"feeding":null,"action_pressure":null},"goal":{"id":90191,"need_id":21778,"action":"work","score":63.5,"created_at":50,"target_id":null,"destination":{"map_id":677,"x":1,"y":5},"status":"completed","outcome":"Produção concluída com pagamento."},"suspended_before":null,"suspended_after":null}.

**Por que outras Needs não foram executadas:** a fila prioriza emergência/priority/ID e para na primeira solucionável, sujeita à continuidade/preparo. Outras pressões retidas: food_reserve#51716(64.29411764705883), family#90186(63.35800000000001), water#42200(57.25), rest#36938(55.85000000000009), religious_interest#21782(33.9108), food#31822(32.0). Não atribuir score global entre Needs.

**Execução:** {"success":true,"result":[true,"Produção concluída com pagamento."],"goal_at_entry":{"id":90191,"need_id":21778,"action":"work","score":63.5,"created_at":50,"target_id":null,"destination":{"map_id":677,"x":1,"y":5},"status":"active","outcome":""},"before":{"id":4029,"name":"Tomas Valerius","hour":50,"alive":true,"profession":"agricultor","lod":"local","position":{"map_id":677,"x":1,"y":5},"residence":677,"hp":100,"hunger":39,"thirst":55,"fatigue":50.000000000000085,"money":58,"food":0,"water":0,"local_food":108,"local_water":159,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{}},"after":{"id":4029,"name":"Tomas Valerius","hour":50,"alive":true,"profession":"agricultor","lod":"local","position":{"map_id":677,"x":1,"y":5},"residence":677,"hp":100,"hunger":39,"thirst":55,"fatigue":50.000000000000085,"money":60,"food":0,"water":0,"local_food":108,"local_water":159,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{}}}.

**Cálculos especializados reais:** [{"system":"work","actual":{"actor":4029,"town":677,"money_before":58,"treasury_before":1122,"inputs_before":{"food":108,"grain":76,"iron":88,"wood":51},"result":{"status":"paid","message":"Produção concluída com pagamento.","produced":4,"paid":2,"credit_added":12}}}].

| Evento/hora | Actor→target | Emissor | Testemunhas | Contexto |
| --- | --- | --- | --- | --- |
| 90185 / 50 / FamilyConcern | 4029→4032 | ["personal.PersonalNeeds.refresh","needs.NeedSystem.refresh","goals.GoalSystem.decide"] | [4029,4032] | {"observed_need":55} |
| 90188 / 50 / GroupKnown | 683→64214 | ["institutions.Institutions.emit","institutions.Institutions.know_group","institutions.Institutions.on_fact"] | [683,689,4029,4032,4044,4046,4058,4067] | {"group_id":64214,"source":"received_fact","source_fact":90187} |
| 90187 / 50 / GroupKnown | 4029→64214 | ["institutions.Institutions.emit","institutions.Institutions.know_group","institutions.Institutions.refresh"] | [683,689,4029,4032,4044,4046,4058,4067] | {"group_id":64214,"source":"member_encounter","source_fact":null} |
| 90189 / 50 / GroupKnown | 4029→29955 | ["institutions.Institutions.emit","institutions.Institutions.know_group","institutions.Institutions.refresh"] | [683,689,4029,4032,4044,4046,4058,4067] | {"group_id":29955,"source":"member_encounter","source_fact":null} |
| 90190 / 50 / CommitmentResumed | 4029→None | ["agency.AgencySystem.event","agency.AgencySystem.selected","goals.GoalSystem.decide"] | [4029] | {"competing":"advancement","commitment_id":21780,"need_id":21778,"origin":"advancement","source_fact":null,"target":null,"progress":8} |
| 90192 / 50 / ItemCreated | 4029→677 | ["professions.ProfessionSystem.work","goals.GoalSystem._execute","goals.GoalSystem.execute"] | [692,4029] | {} |
| 90193 / 50 / CommitmentProgress | 4029→None | ["agency.AgencySystem.event","agency.AgencySystem.outcome","goals.GoalSystem.execute"] | [4029] | {"changes":["money"],"action":"work","commitment_id":21780,"need_id":21778,"origin":"advancement","source_fact":null,"target":null,"progress":9} |

**Aprendizado aceito durante a decisão (amostra):** [{"npc":4029,"event":90185,"kind":"FamilyConcern","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":4032,"event":90185,"kind":"FamilyConcern","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":683,"event":90188,"kind":"GroupKnown","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":689,"event":90188,"kind":"GroupKnown","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":4029,"event":90188,"kind":"GroupKnown","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":4032,"event":90188,"kind":"GroupKnown","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":4044,"event":90188,"kind":"GroupKnown","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":4046,"event":90188,"kind":"GroupKnown","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":4058,"event":90188,"kind":"GroupKnown","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":4067,"event":90188,"kind":"GroupKnown","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":683,"event":90187,"kind":"GroupKnown","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":689,"event":90187,"kind":"GroupKnown","source":null,"firsthand":true,"confidence":100,"latency":0}].

**Recibos posteriores ligados ao mesmo event_id:** [{"event":90185,"kind":"FamilyConcern","learned":{"count":2,"first":50,"last":50,"first_people":[4029,4032]}},{"event":90188,"kind":"GroupKnown","learned":{"count":9,"first":50,"last":60,"first_people":[683,689,4029,4032,4044,4046]}},{"event":90187,"kind":"GroupKnown","learned":{"count":9,"first":50,"last":54,"first_people":[683,689,4029,4032,4044,4046]}},{"event":90189,"kind":"GroupKnown","learned":{"count":11,"first":50,"last":102,"first_people":[683,689,4029,4032,4044,4046]}},{"event":90190,"kind":"CommitmentResumed","learned":{"count":1,"first":50,"last":50,"first_people":[4029]}},{"event":90192,"kind":"ItemCreated","learned":{"count":2,"first":50,"last":50,"first_people":[692,4029]}},{"event":90193,"kind":"CommitmentProgress","learned":{"count":3,"first":50,"last":108,"first_people":[4029,4064,4032]}}]. Contagem é operações de aprendizado aceitas, não indivíduos únicos.

**Consequência imediata:** {"id":4029,"name":"Tomas Valerius","hour":50,"alive":true,"profession":"agricultor","lod":"local","position":{"map_id":677,"x":1,"y":5},"residence":677,"hp":100,"hunger":39,"thirst":55,"fatigue":50.000000000000085,"money":60,"food":0,"water":0,"local_food":108,"local_water":159,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{}}. **Observação/relações com o alvo ao final:** {"observation_end":null,"relations_end":[]}. Não usar esse estado posterior como entrada antiga nem atribuir consequências futuras sem vínculo causal.

### 25. combat — Ruan Ferros #5255, h110: defend

**Pressão escolhida:** `protection` #102988, prioridade 66.06700000000001, base 45, fonte `event:152118`, alvo 5255. Motivo: Crime conhecido ameaça segurança pessoal/familiar.

**Contexto preservado:** {"source_event":152118,"threat":5263,"known_location":{"map_id":976,"x":2,"y":2},"diagnostic":{"reason":"Selected","competing":null,"turn":110}}.

**Entrada:** {"id":5255,"name":"Ruan Ferros","hour":110,"alive":true,"profession":"comerciante","lod":"active","position":{"map_id":976,"x":2,"y":2},"residence":976,"hp":100,"hunger":48,"thirst":41,"fatigue":52.00000000000017,"money":3,"food":0,"water":0,"local_food":101,"local_water":114,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{"denounce":120}}.

**Personalidade:** {"honesty":52,"compassion":63,"courage":38,"independence":24,"greed":70,"diligence":30,"family_loyalty":22,"persistence":36,"temperament":34,"vengefulness":23,"ambition":7,"sadism":0}. **Emoções escalares de entrada:** {"anger":39.60000000000004,"resentment":27.780000000000012,"humiliation":22.19999999999998,"desperation":5.850000000000001,"last_updated":109,"last_support":-10000,"strain":12.946499999999997,"adaptation":0,"last_adapted":0,"stable_material_hours":0,"nested_collections":"LACUNA: cópia rasa; histórico não utilizado"}.

**Conhecimento/locais de entrada:** {"known_places":{"market":{"map_id":976,"x":5,"y":9},"home":{"map_id":976,"x":2,"y":2},"work":{"map_id":976,"x":5,"y":9},"forage":{"map_id":976,"x":1,"y":9},"well_home":{"map_id":976,"x":2,"y":2},"well_rural":{"map_id":976,"x":1,"y":9},"sacred":{"map_id":976,"x":5,"y":1}},"known_towns":[976,864,1005],"route_knowledge_count":4,"knowledge_ids_before":[121771,121774,121785,122775,122784,122787,122792,122798,122800,122805,123040,123831,123837,123844,124766,124768,125659,125667,125677,125680,125684,94746,79537,126825,126831,126835,126837,127819,127825,127829,127832,127841,128779,128781,128786,128792,128794,128796,129047,129048,129775,129777,129779,113178,131902,137891,142110,142397,143720,146085,146089,146094,116575,147433,148801,149978,151076,152118,131907,154425,154427,155173,156209,156212],"market_observation":{"turn":88,"town_id":976,"stock":{"food":165,"grain":58,"water":106,"iron":50,"wood":120},"temporary_work":true,"offers_expire_at":112,"training_offer":null,"price":2,"price_turn":88}}.

**Fatos-fonte retidos após percepção:** [{"event_id":127825,"kind":"AbsenceNoticed","actor_id":5255,"target_id":null,"location":{"map_id":976,"x":5,"y":9},"turn":85,"description":"Ruan Ferros não localiza um familiar há 36 horas.","confidence":100,"required_trust":0,"source_id":null,"source_kind":"direct","context":{"last_seen":49,"relative_id":5252}},{"event_id":137891,"kind":"AbsenceNoticed","actor_id":5255,"target_id":null,"location":{"map_id":976,"x":5,"y":3},"turn":94,"description":"Ruan Ferros não localiza um familiar há 45 horas.","confidence":100,"required_trust":0,"source_id":null,"source_kind":"direct","context":{"last_seen":49,"relative_id":5257}},{"event_id":152118,"kind":"ItemStolen","actor_id":5263,"target_id":5255,"location":{"map_id":976,"x":2,"y":2},"turn":105,"description":"Iria Bruma roubou provisão de Ruan Ferros.","confidence":100,"required_trust":0,"source_id":null,"source_kind":"direct","context":{"item_id":124765,"item_kind":"food"}}].

| Need | ID/alvo | Base→prioridade | Estado/fonte |
| --- | --- | --- | --- |
| protection | 102988/5255 | 45→66.06700000000001 | selected / event:152118 |
| family | 78125/5257 | 47.5→62.422399999999996 | active / event:137891 |
| money | 54987/None | 47.666666666666664→62.14666666666666 | active / economy |
| food_reserve | 25895/None | 41.0→59.94736842105263 | active / food_reserve |
| rest | 35809/None | 52.00000000000017→59.80000000000017 | active / physiology |
| migration | 103797/1005 | 52→59.68 | active / known_towns |
| family | 127826/5252 | 40.0→52.7166 | active / event:127825 |
| food | 25896/None | 52.0→52.6 | active / physiology |
| political_pressure | 103798/None | 39.71666666666666→49.783866666666654 | active / own_shared_problem |
| water | 45921/None | 41→45.2 | active / physiology |
| revenge | 102989/5263 | 30.0→44.147000000000006 | active / event:152118 |
| work | 35810/None | 35→41.6 | active / profession |
| religious_interest | 25899/5907 | 25.75→34.282599999999995 | active / own_faith |
| advancement | 25898/None | 18.2658→28.0158 | active / aspiration:wealth |

**Alternativas/gates realmente vistos:**

Need #102988 (`protection`): 20 Solutions entraram em _evaluate; 13 saíram disponíveis. Entrada: `denounce, denounce, denounce, denounce, denounce, denounce, denounce, avoid_threat, confront, threaten, warn, insult, call_help, calm, withdraw, flee, defend, forgive, apologize, surrender`.

| Opção | Alvo | Etapa | Motivo observado | Auditoria/feeding |
| --- | --- | --- | --- | --- |
| denounce | 5257 | before_Utility_or_unresolved | cooldown_after_failure | {"pressure":null,"feeding":null} |
| denounce | 5280 | before_Utility_or_unresolved | cooldown_after_failure | {"pressure":null,"feeding":null} |
| denounce | 999 | before_Utility_or_unresolved | cooldown_after_failure | {"pressure":null,"feeding":null} |
| denounce | 5234 | before_Utility_or_unresolved | cooldown_after_failure | {"pressure":null,"feeding":null} |
| denounce | 5303 | before_Utility_or_unresolved | cooldown_after_failure | {"pressure":null,"feeding":null} |
| denounce | 5326 | before_Utility_or_unresolved | cooldown_after_failure | {"pressure":null,"feeding":null} |
| denounce | 5349 | before_Utility_or_unresolved | cooldown_after_failure | {"pressure":null,"feeding":null} |

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| defend | {"target":5263,"destination":null} | 58.20000000000001 | {"base":0.2,"risk":0.0625,"courage":0.0285,"defensive":0.0,"injury":-0.0,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| withdraw | {"target":5263,"destination":null} | 51.24999999999999 | {"base":0.175,"risk":0.0625,"compassion":0.04724999999999999,"courage":-0.0285,"defensive":-0.0,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| warn | {"target":5263,"destination":null} | 50.4 | {"base":0.15,"compassion":0.063,"honesty":0.03900000000000001,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| confront | {"target":5263,"destination":null} | 48.245000000000005 | {"base":0.175,"courage":0.057,"anger":0.02947500000000003,"risk":-0.0375,"vengefulness":0.01725,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| calm | {"target":5263,"destination":null} | 48.00499999999999 | {"base":0.175,"compassion":0.09449999999999999,"bond":0.0,"anger":-0.02947500000000003,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| apologize | {"target":5263,"destination":null} | 43.92499999999999 | {"base":0.125,"honesty":0.065,"compassion":0.07875,"culpability":0.0,"anger":-0.04912500000000005,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| flee | {"target":5263,"destination":null} | 40.5 | {"base":0.175,"fear":0.0,"risk":0.075,"courage":-0.0475,"low_health":0.0,"injury":-0.0,"authority":0.0,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| threaten | {"target":5263,"destination":null} | 37.276591900000014 | {"base":0.125,"anger":0.05895000000000006,"courage":0.038,"temperament":0.034,"compassion":-0.07875,"authority":-0.0,"critical_depletion":0.0,"travel":-0.0,"pressure_risk_tolerance":0.0091829595} | {"feeding":null,"action_pressure":null} |
| forgive | {"target":5263,"destination":null} | 34.602 | {"base":0.125,"compassion":0.11025,"bond":0.0,"vengefulness":-0.0345,"resentment":-0.027740000000000015,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| surrender | {"target":5263,"destination":null} | 28.000000000000004 | {"base":0.125,"authority":0.0,"risk":0.0625,"low_health":0.0,"courage":-0.0475,"defensive":-0.0,"travel":-0.0} | {"feeding":null,"action_pressure":null} |

Need #78125 (`family`): 1 Solutions entraram em _evaluate; 1 saíram disponíveis. Entrada: `check_relative`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| check_relative | {"target":5257,"destination":{"map_id":976,"x":2,"y":2}} | 66.5 | {"base":0.275,"independence":0.03,"family_loyalty":0.0275,"travel":-0.0} | {"feeding":null,"action_pressure":null} |

Need #127826 (`family`): 1 Solutions entraram em _evaluate; 1 saíram disponíveis. Entrada: `check_relative`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| check_relative | {"target":5252,"destination":{"map_id":976,"x":2,"y":2}} | 66.5 | {"base":0.275,"independence":0.03,"family_loyalty":0.0275,"travel":-0.0} | {"feeding":null,"action_pressure":null} |

Need #102989 (`revenge`): 22 Solutions entraram em _evaluate; 15 saíram disponíveis. Entrada: `investigate, denounce, denounce, denounce, denounce, denounce, denounce, denounce, avoid_threat, confront, threaten, demand_return, warn, insult, call_help, calm, withdraw, flee, defend, forgive, apologize, surrender`.

| Opção | Alvo | Etapa | Motivo observado | Auditoria/feeding |
| --- | --- | --- | --- | --- |
| denounce | 5257 | before_Utility_or_unresolved | cooldown_after_failure | {"pressure":null,"feeding":null} |
| denounce | 5280 | before_Utility_or_unresolved | cooldown_after_failure | {"pressure":null,"feeding":null} |
| denounce | 999 | before_Utility_or_unresolved | cooldown_after_failure | {"pressure":null,"feeding":null} |
| denounce | 5234 | before_Utility_or_unresolved | cooldown_after_failure | {"pressure":null,"feeding":null} |
| denounce | 5303 | before_Utility_or_unresolved | cooldown_after_failure | {"pressure":null,"feeding":null} |
| denounce | 5326 | before_Utility_or_unresolved | cooldown_after_failure | {"pressure":null,"feeding":null} |
| denounce | 5349 | before_Utility_or_unresolved | cooldown_after_failure | {"pressure":null,"feeding":null} |

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| investigate | {"target":5263,"destination":{"map_id":976,"x":2,"y":2}} | 73.7 | {"base":0.225,"vengefulness":0.046000000000000006,"courage":0.076,"independence":0.036,"compassion":-0.0315,"temperament":0.017,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| demand_return | {"target":5263,"destination":null} | 65.9 | {"base":0.2,"honesty":0.065,"persistence":0.036,"courage":0.0285,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| defend | {"target":5263,"destination":null} | 58.20000000000001 | {"base":0.2,"risk":0.0625,"courage":0.0285,"defensive":0.0,"injury":-0.0,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| withdraw | {"target":5263,"destination":null} | 52.089999999999996 | {"base":0.175,"risk":0.0625,"compassion":0.04724999999999999,"courage":-0.0285,"defensive":-0.0,"travel":-0.0,"known_reputation":0.004200000000000001} | {"feeding":null,"action_pressure":null} |
| warn | {"target":5263,"destination":null} | 50.4 | {"base":0.15,"compassion":0.063,"honesty":0.03900000000000001,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| confront | {"target":5263,"destination":null} | 48.245000000000005 | {"base":0.175,"courage":0.057,"anger":0.02947500000000003,"risk":-0.0375,"vengefulness":0.01725,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| calm | {"target":5263,"destination":null} | 48.00499999999999 | {"base":0.175,"compassion":0.09449999999999999,"bond":0.0,"anger":-0.02947500000000003,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| apologize | {"target":5263,"destination":null} | 43.92499999999999 | {"base":0.125,"honesty":0.065,"compassion":0.07875,"culpability":0.0,"anger":-0.04912500000000005,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| flee | {"target":5263,"destination":null} | 41.34 | {"base":0.175,"fear":0.0,"risk":0.075,"courage":-0.0475,"low_health":0.0,"injury":-0.0,"authority":0.0,"travel":-0.0,"known_reputation":0.004200000000000001} | {"feeding":null,"action_pressure":null} |
| threaten | {"target":5263,"destination":null} | 36.33414710000001 | {"base":0.125,"anger":0.05895000000000006,"courage":0.038,"temperament":0.034,"compassion":-0.07875,"authority":-0.0,"critical_depletion":0.0,"travel":-0.0,"pressure_risk_tolerance":0.0044707355000000015} | {"feeding":null,"action_pressure":null} |

Need #25898 (`advancement`): 2 Solutions entraram em _evaluate; 2 saíram disponíveis. Entrada: `work, work_for_food`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| work | {"target":null,"destination":{"map_id":976,"x":5,"y":9}} | 44.99999999999999 | {"base":0.25,"diligence":0.075,"physical_depletion":0.0,"travel":-0.1} | {"feeding":null,"action_pressure":null} |
| work_for_food | {"target":null,"destination":{"map_id":976,"x":1,"y":9}} | 36.5 | {"base":0.225,"diligence":0.0375,"physical_depletion":0.0,"travel":-0.08} | {"feeding":null,"action_pressure":null} |

**Escolhas intermediárias:** [{"chosen":{"action":"defend","score":58.20000000000001,"target":5263,"destination":null,"terms":{"base":0.2,"risk":0.0625,"courage":0.0285,"defensive":0.0,"injury":-0.0,"travel":-0.0},"feeding":null,"action_pressure":null},"near_scores":[58.20000000000001,51.24999999999999,50.4,48.245000000000005,48.00499999999999,43.92499999999999,40.5,37.276591900000014],"variation_draws":"não capturados; RNG não consultado pelo observador"}].

**Preparação/substituição posterior:** [].

**Winner final / Goal:** {"winner":{"action":"defend","score":58.20000000000001,"target":5263,"destination":null,"terms":{"base":0.2,"risk":0.0625,"courage":0.0285,"defensive":0.0,"injury":-0.0,"travel":-0.0},"feeding":null,"action_pressure":null},"goal":{"id":157162,"need_id":102988,"action":"defend","score":58.20000000000001,"created_at":110,"target_id":5263,"destination":null,"status":"completed","outcome":"Defesa temporária adotada."},"suspended_before":null,"suspended_after":null}.

**Por que outras Needs não foram executadas:** a fila prioriza emergência/priority/ID e para na primeira solucionável, sujeita à continuidade/preparo. Outras pressões retidas: family#78125(62.422399999999996), money#54987(62.14666666666666), food_reserve#25895(59.94736842105263), rest#35809(59.80000000000017), migration#103797(59.68), family#127826(52.7166), food#25896(52.6), political_pressure#103798(49.783866666666654), water#45921(45.2), revenge#102989(44.147000000000006), work#35810(41.6), religious_interest#25899(34.282599999999995), advancement#25898(28.0158). Não atribuir score global entre Needs.

**Execução:** {"success":true,"result":[true,"Defesa temporária adotada."],"goal_at_entry":{"id":157162,"need_id":102988,"action":"defend","score":58.20000000000001,"created_at":110,"target_id":5263,"destination":null,"status":"active","outcome":""},"before":{"id":5255,"name":"Ruan Ferros","hour":110,"alive":true,"profession":"comerciante","lod":"active","position":{"map_id":976,"x":2,"y":2},"residence":976,"hp":100,"hunger":48,"thirst":41,"fatigue":52.00000000000017,"money":3,"food":0,"water":0,"local_food":101,"local_water":114,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{"denounce":120}},"after":{"id":5255,"name":"Ruan Ferros","hour":110,"alive":true,"profession":"comerciante","lod":"active","position":{"map_id":976,"x":2,"y":2},"residence":976,"hp":100,"hunger":48,"thirst":41,"fatigue":52.00000000000017,"money":3,"food":0,"water":0,"local_food":101,"local_water":114,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{"denounce":120}}}.

**Cálculos especializados reais:** [{"system":"lethal_decision","function":"lethal_decisions.LethalDecisionSystem.evaluate","result":{"available":false,"pressure":-69.08,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"protection","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":3.91,"directed_emotion":3.9050000000000016,"commitment":0.0,"sadism":0.0,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":34.650000000000006,"moral_restraint":6.24,"fear":0.0,"risk":6.0,"bond":0.0,"authority_or_witnesses":0.0,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{"pressure":-69.08,"cause":{"severity":0,"grave":false,"causes":[],"facts":[],"confidence":0,"mode":"retributive","confirmed_injury":0}}},{"system":"lethal_decision","function":"lethal_decisions.LethalDecisionSystem.evaluate","result":{"available":false,"pressure":-69.08,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"protection","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":3.91,"directed_emotion":3.9050000000000016,"commitment":0.0,"sadism":0.0,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":34.650000000000006,"moral_restraint":6.24,"fear":0.0,"risk":6.0,"bond":0.0,"authority_or_witnesses":0.0,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{"pressure":-69.08,"cause":{"severity":0,"grave":false,"causes":[],"facts":[],"confidence":0,"mode":"retributive","confirmed_injury":0}}},{"system":"lethal_pressure","function":"lethality.LethalPressure.evaluate","result":{"available":false,"pressure":-69.08,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"protection","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":3.91,"directed_emotion":3.9050000000000016,"commitment":0.0,"sadism":0.0,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":34.650000000000006,"moral_restraint":6.24,"fear":0.0,"risk":6.0,"bond":0.0,"authority_or_witnesses":0.0,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{}},{"system":"lethal_decision","function":"lethal_decisions.LethalDecisionSystem.evaluate","result":{"available":false,"pressure":-69.08,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"revenge","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":3.91,"directed_emotion":3.9050000000000016,"commitment":0.0,"sadism":0.0,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":34.650000000000006,"moral_restraint":6.24,"fear":0.0,"risk":6.0,"bond":0.0,"authority_or_witnesses":0.0,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{"pressure":-69.08,"cause":{"severity":0,"grave":false,"causes":[],"facts":[],"confidence":0,"mode":"retributive","confirmed_injury":0}}},{"system":"lethal_decision","function":"lethal_decisions.LethalDecisionSystem.evaluate","result":{"available":false,"pressure":-69.08,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"revenge","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":3.91,"directed_emotion":3.9050000000000016,"commitment":0.0,"sadism":0.0,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":34.650000000000006,"moral_restraint":6.24,"fear":0.0,"risk":6.0,"bond":0.0,"authority_or_witnesses":0.0,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{"pressure":-69.08,"cause":{"severity":0,"grave":false,"causes":[],"facts":[],"confidence":0,"mode":"retributive","confirmed_injury":0}}},{"system":"lethal_pressure","function":"lethality.LethalPressure.evaluate","result":{"available":false,"pressure":-69.08,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"revenge","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":3.91,"directed_emotion":3.9050000000000016,"commitment":0.0,"sadism":0.0,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":34.650000000000006,"moral_restraint":6.24,"fear":0.0,"risk":6.0,"bond":0.0,"authority_or_witnesses":0.0,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{}}].

| Evento/hora | Actor→target | Emissor | Testemunhas | Contexto |
| --- | --- | --- | --- | --- |
| 157163 / 110 / CharacterDefended | 5255→None | ["conflicts.ConflictSystem.execute","goals.GoalSystem._execute","goals.GoalSystem.execute"] | [985,5226,5255,5263,5269,5306,5318,5329,5335] | {} |

**Aprendizado aceito durante a decisão (amostra):** [{"npc":985,"event":157163,"kind":"CharacterDefended","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":5226,"event":157163,"kind":"CharacterDefended","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":5255,"event":157163,"kind":"CharacterDefended","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":5263,"event":157163,"kind":"CharacterDefended","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":5269,"event":157163,"kind":"CharacterDefended","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":5306,"event":157163,"kind":"CharacterDefended","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":5318,"event":157163,"kind":"CharacterDefended","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":5329,"event":157163,"kind":"CharacterDefended","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":5335,"event":157163,"kind":"CharacterDefended","source":null,"firsthand":true,"confidence":100,"latency":0}].

**Recibos posteriores ligados ao mesmo event_id:** [{"event":157163,"kind":"CharacterDefended","learned":{"count":9,"first":110,"last":110,"first_people":[985,5226,5255,5263,5269,5306]}}]. Contagem é operações de aprendizado aceitas, não indivíduos únicos.

**Consequência imediata:** {"id":5255,"name":"Ruan Ferros","hour":110,"alive":true,"profession":"comerciante","lod":"active","position":{"map_id":976,"x":2,"y":2},"residence":976,"hp":100,"hunger":48,"thirst":41,"fatigue":52.00000000000017,"money":3,"food":0,"water":0,"local_food":101,"local_water":114,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{"denounce":120}}. **Observação/relações com o alvo ao final:** {"observation_end":{"turn":110,"position":{"map_id":976,"x":2,"y":2},"hunger":17,"thirst":40,"health":100,"alive":true,"profession":"agricultor","weapon_power":4,"injured":0},"relations_end":[{"source_id":5255,"target_id":5263,"kind":"confiança","value":4}]}. Não usar esse estado posterior como entrada antiga nem atribuir consequências futuras sem vínculo causal.

### 26. crime — Cael Valerius #2458, h182: steal

**Pressão escolhida:** `food` #14659, prioridade 100, base 100, fonte `physiology`, alvo None. Motivo: Fome.

**Contexto preservado:** {"emergency":true}.

**Entrada:** {"id":2458,"name":"Cael Valerius","hour":182,"alive":true,"profession":"cozinheiro","lod":"active","position":{"map_id":302,"x":7,"y":11},"residence":302,"hp":38,"hunger":86,"thirst":49,"fatigue":100,"money":2,"food":0,"water":1,"local_food":0,"local_water":0,"recoverable_deprivation":62,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{}}.

**Personalidade:** {"honesty":62,"compassion":85,"courage":15,"independence":60,"greed":92,"diligence":65,"family_loyalty":86,"persistence":85,"temperament":88,"vengefulness":61,"ambition":29,"sadism":0}. **Emoções escalares de entrada:** {"anger":96.70000000000003,"resentment":99.47999999999995,"humiliation":98.70000000000005,"desperation":36.199999999999946,"last_updated":181,"last_support":-10000,"strain":61.514999999999986,"adaptation":0,"last_adapted":0,"stable_material_hours":0,"nested_collections":"LACUNA: cópia rasa; histórico não utilizado"}.

**Conhecimento/locais de entrada:** {"known_places":{"market":{"map_id":302,"x":7,"y":13},"home":{"map_id":302,"x":2,"y":2},"work":{"map_id":302,"x":7,"y":13},"forage":{"map_id":302,"x":1,"y":13},"well_home":{"map_id":302,"x":2,"y":2},"well_rural":{"map_id":302,"x":1,"y":13},"sacred":{"map_id":302,"x":7,"y":1}},"known_towns":[302,367],"route_knowledge_count":2,"knowledge_ids_before":[161025,197431,197438,197443,197465,197472,197490,198374,198892,198896,198900,198913,198928,198943,198948,198963,198969,198972,198979,199833,199878,200285,200294,200296,200304,200307,200310,200319,200327,200338,200354,200355,200364,200377,201163,201220,201222,201276,201636,201639,201650,201656,201659,201661,202977,215717,215745,215747,215752,215755,216439,216838,217622,168603,225722,225720,225741,225742,225964,225965,227106,228996,212599,213581],"market_observation":{"turn":172,"town_id":302,"stock":{"food":0,"grain":0,"water":0,"iron":64,"wood":120},"temporary_work":false,"offers_expire_at":196,"training_offer":null,"price":14,"price_turn":172}}.

**Fatos-fonte retidos após percepção:** [{"event_id":225741,"kind":"ItemStolen","actor_id":2513,"target_id":302,"location":{"map_id":302,"x":7,"y":13},"turn":168,"description":"Elena Solaris roubou comida no mercado de Norria.","confidence":100,"required_trust":0,"source_id":null,"source_kind":"direct","context":{"item_id":225703,"item_kind":"food"}},{"event_id":161025,"kind":"AbsenceNoticed","actor_id":2458,"target_id":null,"location":{"map_id":302,"x":7,"y":2},"turn":114,"description":"Cael Valerius não localiza um familiar há 38 horas.","confidence":100,"required_trust":0,"source_id":null,"source_kind":"direct","context":{"last_seen":76,"relative_id":2461}},{"event_id":225722,"kind":"WantedIssued","actor_id":2426,"target_id":302,"location":{"map_id":302,"x":7,"y":13},"turn":168,"description":"Ruan Vale registrou procura por Cael Valerius.","confidence":100,"required_trust":0,"source_id":null,"source_kind":"direct","context":{"record_id":225721,"suspect_id":2458,"source_fact":225720,"severity":1,"confidence":100,"last_known_location":{"map_id":302,"x":7,"y":13}}},{"event_id":213581,"kind":"ItemStolen","actor_id":2516,"target_id":302,"location":{"map_id":302,"x":7,"y":13},"turn":158,"description":"Iria Corven roubou comida no mercado de Norria.","confidence":30,"required_trust":0,"source_id":2625,"source_kind":"rumor","context":{"item_id":213580,"item_kind":"food"}}].

| Need | ID/alvo | Base→prioridade | Estado/fonte |
| --- | --- | --- | --- |
| food | 14659/None | 100→100 | active / physiology |
| rest | 52779/None | 100→100 | active / physiology |
| money | 14660/None | 57.583333333333336→81.51133333333334 | active / economy |
| protection | 29553/2458 | 45→80.024 | active / event:213581 |
| family | 83562/2461 | 46.333333333333336→79.46618952380952 | active / event:161025 |
| recovery | 185624/2458 | 67→74.05 | active / own_physiology |
| response | 225723/2426 | 55→71.724 | active / event:225722 |
| food_reserve | 33106/None | 41.0→71.71020408163265 | active / food_reserve |
| migration | 33108/367 | 62→68.078 | active / known_towns |
| political_pressure | 33109/None | 54.93333333333334→65.53033333333333 | active / own_shared_problem |
| revenge | 104193/2513 | 30.0→59.884 | active / event:225741 |
| water | 43576/None | 49→54.1 | active / physiology |
| work | 33107/None | 35→48.75 | active / profession |

**Alternativas/gates realmente vistos:**

Need #14659 (`food`): 3 Solutions entraram em _evaluate; 3 saíram disponíveis. Entrada: `steal, forage, work`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| steal | {"target":null,"destination":{"map_id":302,"x":7,"y":13}} | 61.41058666666666 | {"base":0.35,"greed":0.15333333333333335,"honesty":-0.31,"courage":0.0075,"travel":-0.02,"pressure_moral_tolerance":0.1262196} | {"feeding":{"EstimatedTimeUntilFoodConsumed":4,"EstimatedSurvivalMargin":23,"economically_viable":true,"survival_viable":true,"reason":null,"known_conditions":["NoProduct","NoMoney","DistantProduct"]},"action_pressure":null} |
| work | {"target":null,"destination":{"map_id":302,"x":7,"y":13}} | 60.12500000000001 | {"base":0.25,"diligence":0.1625,"physical_depletion":-0.091875,"travel":-0.02} | {"feeding":{"EstimatedTimeUntilFoodConsumed":16,"EstimatedSurvivalMargin":23,"economically_viable":true,"survival_viable":true,"reason":null,"known_conditions":["NoProduct","NoMoney","DistantProduct"]},"action_pressure":null} |
| forage | {"target":null,"destination":{"map_id":302,"x":1,"y":13}} | 49.0 | {"base":0.175,"independence":0.15,"hunter":0.0,"travel":-0.08} | {"feeding":{"EstimatedTimeUntilFoodConsumed":10,"EstimatedSurvivalMargin":23,"economically_viable":true,"survival_viable":true,"reason":null,"known_conditions":["NoProduct","NoMoney","DistantProduct"]},"action_pressure":null} |

Need #29553 (`protection`): 7 Solutions entraram em _evaluate; 7 saíram disponíveis. Entrada: `denounce, denounce, denounce, denounce, denounce, avoid_threat, pursue`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| denounce | {"target":361,"destination":{"map_id":302,"x":7,"y":13}} | 79.65 | {"base":0.225,"honesty":0.1085,"vengefulness":0.061,"courage":0.01125,"trust":0.0125,"travel":-0.02} | {"feeding":null,"action_pressure":null} |
| denounce | {"target":2426,"destination":{"map_id":302,"x":7,"y":13}} | 79.65 | {"base":0.225,"honesty":0.1085,"vengefulness":0.061,"courage":0.01125,"trust":0.0125,"travel":-0.02} | {"feeding":null,"action_pressure":null} |
| denounce | {"target":2495,"destination":{"map_id":302,"x":7,"y":13}} | 79.65 | {"base":0.225,"honesty":0.1085,"vengefulness":0.061,"courage":0.01125,"trust":0.0125,"travel":-0.02} | {"feeding":null,"action_pressure":null} |
| denounce | {"target":2610,"destination":{"map_id":302,"x":7,"y":13}} | 79.65 | {"base":0.225,"honesty":0.1085,"vengefulness":0.061,"courage":0.01125,"trust":0.0125,"travel":-0.02} | {"feeding":null,"action_pressure":null} |
| denounce | {"target":2518,"destination":{"map_id":302,"x":7,"y":8}} | 77.64999999999999 | {"base":0.225,"honesty":0.1085,"vengefulness":0.061,"courage":0.01125,"trust":0.0125,"travel":-0.03} | {"feeding":null,"action_pressure":null} |
| pursue | {"target":2516,"destination":{"map_id":302,"x":7,"y":13}} | 76.17641859321476 | {"base":0.275,"courage":0.015,"diligence":0.04875,"vengefulness":0.061,"critical_depletion":0.0,"travel":-0.02,"action_pressure":0.0,"pressure_risk_tolerance":0.0011320929660737812} | {"feeding":null,"action_pressure":{"eligible":true,"world_pressure":0,"action_pressure":0.0,"eligibility_causes":[],"source_facts":[],"capacity":12.67,"perceived_capacity":9.12,"major_barriers":[],"selected_alternative":"pursue"}} |
| avoid_threat | {"target":null,"destination":{"map_id":302,"x":2,"y":2}} | 6.550000000000001 | {"base":0.2,"courage":-0.03,"compassion":0.06375,"vengefulness":-0.061,"travel":-0.14} | {"feeding":null,"action_pressure":null} |

Need #83562 (`family`): 2 Solutions entraram em _evaluate; 2 saíram disponíveis. Entrada: `search_area, search_area`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| search_area | {"target":2461,"destination":{"map_id":302,"x":7,"y":13}} | 78.675 | {"base":0.275,"persistence":0.10625,"courage":0.01125,"travel":-0.02,"action_pressure":0.020874999999999998,"no_progress":0.0} | {"feeding":null,"action_pressure":{"eligible":true,"world_pressure":46.333333333333336,"action_pressure":16.7,"eligibility_causes":["event:161025"],"source_facts":[161025],"capacity":12.67,"perceived_capacity":9.12,"major_barriers":[],"selected_alternative":"search_area"}} |
| search_area | {"target":2461,"destination":{"map_id":302,"x":1,"y":13}} | 66.675 | {"base":0.275,"persistence":0.10625,"courage":0.01125,"travel":-0.08,"action_pressure":0.020874999999999998,"no_progress":0.0} | {"feeding":null,"action_pressure":{"eligible":true,"world_pressure":46.333333333333336,"action_pressure":16.7,"eligibility_causes":["event:161025"],"source_facts":[161025],"capacity":12.67,"perceived_capacity":9.12,"major_barriers":[],"selected_alternative":"search_area"}} |

Need #104193 (`revenge`): 8 Solutions entraram em _evaluate; 8 saíram disponíveis. Entrada: `investigate, denounce, denounce, denounce, denounce, denounce, avoid_threat, pursue`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| investigate | {"target":2513,"destination":{"map_id":302,"x":7,"y":13}} | 89.7 | {"base":0.225,"vengefulness":0.122,"courage":0.03,"independence":0.09,"compassion":-0.0425,"temperament":0.044000000000000004,"travel":-0.02} | {"feeding":null,"action_pressure":null} |
| denounce | {"target":361,"destination":{"map_id":302,"x":7,"y":13}} | 79.65 | {"base":0.225,"honesty":0.1085,"vengefulness":0.061,"courage":0.01125,"trust":0.0125,"travel":-0.02} | {"feeding":null,"action_pressure":null} |
| denounce | {"target":2426,"destination":{"map_id":302,"x":7,"y":13}} | 79.65 | {"base":0.225,"honesty":0.1085,"vengefulness":0.061,"courage":0.01125,"trust":0.0125,"travel":-0.02} | {"feeding":null,"action_pressure":null} |
| denounce | {"target":2495,"destination":{"map_id":302,"x":7,"y":13}} | 79.65 | {"base":0.225,"honesty":0.1085,"vengefulness":0.061,"courage":0.01125,"trust":0.0125,"travel":-0.02} | {"feeding":null,"action_pressure":null} |
| denounce | {"target":2610,"destination":{"map_id":302,"x":7,"y":13}} | 79.65 | {"base":0.225,"honesty":0.1085,"vengefulness":0.061,"courage":0.01125,"trust":0.0125,"travel":-0.02} | {"feeding":null,"action_pressure":null} |
| denounce | {"target":2518,"destination":{"map_id":302,"x":7,"y":8}} | 77.64999999999999 | {"base":0.225,"honesty":0.1085,"vengefulness":0.061,"courage":0.01125,"trust":0.0125,"travel":-0.03} | {"feeding":null,"action_pressure":null} |
| pursue | {"target":2513,"destination":{"map_id":302,"x":7,"y":7}} | 72.20759183076903 | {"base":0.275,"courage":0.015,"diligence":0.04875,"vengefulness":0.061,"critical_depletion":0.0,"travel":-0.04,"action_pressure":0.0,"pressure_risk_tolerance":0.0012879591538451321} | {"feeding":null,"action_pressure":{"eligible":true,"world_pressure":0,"action_pressure":0.0,"eligibility_causes":[],"source_facts":[],"capacity":12.67,"perceived_capacity":9.12,"major_barriers":[],"selected_alternative":"pursue"}} |
| avoid_threat | {"target":null,"destination":{"map_id":302,"x":2,"y":2}} | 6.550000000000001 | {"base":0.2,"courage":-0.03,"compassion":0.06375,"vengefulness":-0.061,"travel":-0.14} | {"feeding":null,"action_pressure":null} |

**Escolhas intermediárias:** [{"chosen":{"action":"steal","score":61.41058666666666,"target":null,"destination":{"map_id":302,"x":7,"y":13},"terms":{"base":0.35,"greed":0.15333333333333335,"honesty":-0.31,"courage":0.0075,"travel":-0.02,"pressure_moral_tolerance":0.1262196},"feeding":{"EstimatedTimeUntilFoodConsumed":4,"EstimatedSurvivalMargin":23,"economically_viable":true,"survival_viable":true,"reason":null,"known_conditions":["NoProduct","NoMoney","DistantProduct"]},"action_pressure":null},"near_scores":[61.41058666666666,60.12500000000001,49.0],"variation_draws":"não capturados; RNG não consultado pelo observador"}].

**Preparação/substituição posterior:** [].

**Winner final / Goal:** {"winner":{"action":"steal","score":61.41058666666666,"target":null,"destination":{"map_id":302,"x":7,"y":13},"terms":{"base":0.35,"greed":0.15333333333333335,"honesty":-0.31,"courage":0.0075,"travel":-0.02,"pressure_moral_tolerance":0.1262196},"feeding":{"EstimatedTimeUntilFoodConsumed":4,"EstimatedSurvivalMargin":23,"economically_viable":true,"survival_viable":true,"reason":null,"known_conditions":["NoProduct","NoMoney","DistantProduct"]},"action_pressure":null},"goal":{"id":241048,"need_id":14659,"action":"steal","score":61.41058666666666,"created_at":182,"target_id":null,"destination":{"map_id":302,"x":7,"y":13},"status":"active","outcome":""},"suspended_before":null,"suspended_after":null}.

**Por que outras Needs não foram executadas:** a fila prioriza emergência/priority/ID e para na primeira solucionável, sujeita à continuidade/preparo. Outras pressões retidas: rest#52779(100), money#14660(81.51133333333334), protection#29553(80.024), family#83562(79.46618952380952), recovery#185624(74.05), response#225723(71.724), food_reserve#33106(71.71020408163265), migration#33108(68.078), political_pressure#33109(65.53033333333333), revenge#104193(59.884), water#43576(54.1), work#33107(48.75). Não atribuir score global entre Needs.

**Execução:** execute não foi chamado neste trace. A Goal pode ter iniciado/continuado deslocamento; o snapshot e a posição posterior delimitam essa conclusão.

**Cálculos especializados reais:** [{"system":"lethal_decision","function":"lethal_decisions.LethalDecisionSystem.evaluate","result":{"available":false,"pressure":-95.57,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"protection","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":10.370000000000001,"directed_emotion":0.0,"commitment":0.0,"sadism":0.0,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":46.75000000000001,"moral_restraint":7.4399999999999995,"fear":14.771739130434781,"risk":6.9818181818181815,"bond":0.0,"authority_or_witnesses":0.0,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{"pressure":-95.57,"cause":{"severity":0,"grave":false,"causes":[],"facts":[],"confidence":0,"mode":"retributive","confirmed_injury":0}}},{"system":"lethal_decision","function":"lethal_decisions.LethalDecisionSystem.evaluate","result":{"available":false,"pressure":-95.57,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"protection","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":10.370000000000001,"directed_emotion":0.0,"commitment":0.0,"sadism":0.0,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":46.75000000000001,"moral_restraint":7.4399999999999995,"fear":14.771739130434781,"risk":6.9818181818181815,"bond":0.0,"authority_or_witnesses":0.0,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{"pressure":-95.57,"cause":{"severity":0,"grave":false,"causes":[],"facts":[],"confidence":0,"mode":"retributive","confirmed_injury":0}}},{"system":"lethal_pressure","function":"lethality.LethalPressure.evaluate","result":{"available":false,"pressure":-95.57,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"protection","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":10.370000000000001,"directed_emotion":0.0,"commitment":0.0,"sadism":0.0,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":46.75000000000001,"moral_restraint":7.4399999999999995,"fear":14.771739130434781,"risk":6.9818181818181815,"bond":0.0,"authority_or_witnesses":0.0,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{}},{"system":"lethal_decision","function":"lethal_decisions.LethalDecisionSystem.evaluate","result":{"available":false,"pressure":-75.47,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"revenge","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":10.370000000000001,"directed_emotion":3.8830000000000027,"commitment":0.0,"sadism":0.0,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":46.75000000000001,"moral_restraint":7.4399999999999995,"fear":0.0,"risk":5.53125,"bond":0.0,"authority_or_witnesses":0.0,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{"pressure":-75.47,"cause":{"severity":0,"grave":false,"causes":[],"facts":[],"confidence":0,"mode":"retributive","confirmed_injury":0}}},{"system":"lethal_decision","function":"lethal_decisions.LethalDecisionSystem.evaluate","result":{"available":false,"pressure":-75.47,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"revenge","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":10.370000000000001,"directed_emotion":3.8830000000000027,"commitment":0.0,"sadism":0.0,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":46.75000000000001,"moral_restraint":7.4399999999999995,"fear":0.0,"risk":5.53125,"bond":0.0,"authority_or_witnesses":0.0,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{"pressure":-75.47,"cause":{"severity":0,"grave":false,"causes":[],"facts":[],"confidence":0,"mode":"retributive","confirmed_injury":0}}},{"system":"lethal_pressure","function":"lethality.LethalPressure.evaluate","result":{"available":false,"pressure":-75.47,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"revenge","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":10.370000000000001,"directed_emotion":3.8830000000000027,"commitment":0.0,"sadism":0.0,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":46.75000000000001,"moral_restraint":7.4399999999999995,"fear":0.0,"risk":5.53125,"bond":0.0,"authority_or_witnesses":0.0,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{}},{"system":"lethal_decision","function":"lethal_decisions.LethalDecisionSystem.evaluate","result":{"available":false,"pressure":-120.49,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"response","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","fear","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":10.370000000000001,"directed_emotion":0.0,"commitment":0.0,"sadism":0.0,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":46.75000000000001,"moral_restraint":7.4399999999999995,"fear":37.75,"risk":8.921933085501859,"bond":0.0,"authority_or_witnesses":0.0,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{"pressure":-120.49,"cause":{"severity":0,"grave":false,"causes":[],"facts":[],"confidence":0,"mode":"retributive","confirmed_injury":0}}},{"system":"lethal_decision","function":"lethal_decisions.LethalDecisionSystem.evaluate","result":{"available":false,"pressure":-120.49,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"response","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","fear","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":10.370000000000001,"directed_emotion":0.0,"commitment":0.0,"sadism":0.0,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":46.75000000000001,"moral_restraint":7.4399999999999995,"fear":37.75,"risk":8.921933085501859,"bond":0.0,"authority_or_witnesses":0.0,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{"pressure":-120.49,"cause":{"severity":0,"grave":false,"causes":[],"facts":[],"confidence":0,"mode":"retributive","confirmed_injury":0}}},{"system":"lethal_pressure","function":"lethality.LethalPressure.evaluate","result":{"available":false,"pressure":-120.49,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"response","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","fear","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":10.370000000000001,"directed_emotion":0.0,"commitment":0.0,"sadism":0.0,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":46.75000000000001,"moral_restraint":7.4399999999999995,"fear":37.75,"risk":8.921933085501859,"bond":0.0,"authority_or_witnesses":0.0,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{}},{"system":"capacity","function":"action_pressure.ActionPressureSystem.assess","result":{"eligible":true,"world_pressure":0,"action_pressure":0.0,"eligibility_causes":[],"source_facts":[],"capacity":12.67,"perceived_capacity":9.12,"major_barriers":[],"selected_alternative":"pursue"},"inputs":{}},{"system":"capacity","function":"action_pressure.ActionPressureSystem.assess","result":{"eligible":true,"world_pressure":46.333333333333336,"action_pressure":16.7,"eligibility_causes":["event:161025"],"source_facts":[161025],"capacity":12.67,"perceived_capacity":9.12,"major_barriers":[],"selected_alternative":"search_area"},"inputs":{}},{"system":"capacity","function":"action_pressure.ActionPressureSystem.assess","result":{"eligible":true,"world_pressure":46.333333333333336,"action_pressure":16.7,"eligibility_causes":["event:161025"],"source_facts":[161025],"capacity":12.67,"perceived_capacity":9.12,"major_barriers":[],"selected_alternative":"search_area"},"inputs":{}},{"system":"capacity","function":"action_pressure.ActionPressureSystem.assess","result":{"eligible":true,"world_pressure":0,"action_pressure":0.0,"eligibility_causes":[],"source_facts":[],"capacity":12.67,"perceived_capacity":9.12,"major_barriers":[],"selected_alternative":"pursue"},"inputs":{}}].

**Evento:** nenhum evento retido durante esta decisão. Isso pode significar movimento/efeito sem evento; não implica falha.

**Aprendizado aceito durante a decisão (amostra):** [].

**Recibos posteriores ligados ao mesmo event_id:** []. Contagem é operações de aprendizado aceitas, não indivíduos únicos.

**Consequência imediata:** {"id":2458,"name":"Cael Valerius","hour":182,"alive":true,"profession":"cozinheiro","lod":"active","position":{"map_id":302,"x":7,"y":12},"residence":302,"hp":38,"hunger":86,"thirst":49,"fatigue":100,"money":2,"food":0,"water":1,"local_food":0,"local_water":0,"recoverable_deprivation":62,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{}}. **Observação/relações com o alvo ao final:** {"observation_end":null,"relations_end":[]}. Não usar esse estado posterior como entrada antiga nem atribuir consequências futuras sem vínculo causal.

### 27. faction — Aldren Hammer #1173, h2: store_supplies

**Pressão escolhida:** `organizational_access` #20146, prioridade 53.0, base 53, fonte `organization`, alvo 1176. Motivo: Procurar pessoas e recursos para a organização.

**Contexto preservado:** {"faction_id":1176}.

**Entrada:** {"id":1173,"name":"Aldren Hammer","hour":2,"alive":true,"profession":"caçador","lod":"local","position":{"map_id":1170,"x":5,"y":5},"residence":302,"hp":100,"hunger":35,"thirst":4,"fatigue":9.399999999999999,"money":5,"food":4,"water":5,"local_food":null,"local_water":null,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{}}.

**Personalidade:** {"honesty":12,"compassion":81,"courage":11,"independence":30,"greed":77,"diligence":61,"family_loyalty":64,"persistence":89,"temperament":72,"vengefulness":23,"ambition":49,"sadism":0}. **Emoções escalares de entrada:** {"anger":0,"resentment":0,"humiliation":0,"desperation":0,"last_updated":0,"last_support":-10000,"strain":0,"adaptation":0,"last_adapted":0,"stable_material_hours":0,"nested_collections":"LACUNA: cópia rasa; histórico não utilizado"}.

**Conhecimento/locais de entrada:** {"known_places":{"home":{"map_id":1170,"x":5,"y":5},"work":{"map_id":1170,"x":5,"y":5},"forage":{"map_id":1170,"x":5,"y":5},"sacred":{"map_id":1170,"x":5,"y":1}},"known_towns":[302,396],"route_knowledge_count":2,"knowledge_ids_before":[6813,6814,12024,12025],"market_observation":{}}.

**Fatos-fonte retidos após percepção:** [].

| Need | ID/alvo | Base→prioridade | Estado/fonte |
| --- | --- | --- | --- |
| organizational_survival | 20144/1173 | 50.696→54.4032 | active / faction:1176 |
| organizational_access | 20146/1176 | 53→53.0 | active / organization |
| money | 20140/None | 40.0→52.2 | active / economy |
| advancement | 20142/None | 23.1798→36.0500688 | active / aspiration:wealth |
| religious_interest | 20143/5909 | 32.75→34.9774 | active / own_faith |
| food | 20139/None | 20→20.0 | active / physiology |

**Alternativas/gates realmente vistos:**

Need #20144 (`organizational_survival`): 0 Solutions entraram em _evaluate; 0 saíram disponíveis. Entrada: ``.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |

Need #20146 (`organizational_access`): 1 Solutions entraram em _evaluate; 1 saíram disponíveis. Entrada: `store_supplies`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| store_supplies | {"target":1176,"destination":null} | 40.0 | {"base":0.2,"travel":-0.0} | {"feeding":null,"action_pressure":null} |

Need #20142 (`advancement`): 0 Solutions entraram em _evaluate; 0 saíram disponíveis. Entrada: ``.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |

**Escolhas intermediárias:** [{"chosen":{"action":"store_supplies","score":40.0,"target":1176,"destination":null,"terms":{"base":0.2,"travel":-0.0},"feeding":null,"action_pressure":null},"near_scores":[40.0],"variation_draws":"não capturados; RNG não consultado pelo observador"}].

**Preparação/substituição posterior:** [].

**Winner final / Goal:** {"winner":{"action":"store_supplies","score":40.0,"target":1176,"destination":null,"terms":{"base":0.2,"travel":-0.0},"feeding":null,"action_pressure":null},"goal":{"id":20148,"need_id":20146,"action":"store_supplies","score":40.0,"created_at":2,"target_id":1176,"destination":null,"status":"completed","outcome":"Contribuição de recursos existentes."},"suspended_before":null,"suspended_after":null}.

**Por que outras Needs não foram executadas:** a fila prioriza emergência/priority/ID e para na primeira solucionável, sujeita à continuidade/preparo. Outras pressões retidas: organizational_survival#20144(54.4032), money#20140(52.2), advancement#20142(36.0500688), religious_interest#20143(34.9774), food#20139(20.0). Não atribuir score global entre Needs.

**Execução:** {"success":true,"result":[true,"Contribuição de recursos existentes."],"goal_at_entry":{"id":20148,"need_id":20146,"action":"store_supplies","score":40.0,"created_at":2,"target_id":1176,"destination":null,"status":"active","outcome":""},"before":{"id":1173,"name":"Aldren Hammer","hour":2,"alive":true,"profession":"caçador","lod":"local","position":{"map_id":1170,"x":5,"y":5},"residence":302,"hp":100,"hunger":35,"thirst":4,"fatigue":9.399999999999999,"money":5,"food":4,"water":5,"local_food":null,"local_water":null,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{}},"after":{"id":1173,"name":"Aldren Hammer","hour":2,"alive":true,"profession":"caçador","lod":"local","position":{"map_id":1170,"x":5,"y":5},"residence":302,"hp":100,"hunger":35,"thirst":4,"fatigue":9.399999999999999,"money":5,"food":3,"water":5,"local_food":null,"local_water":null,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{}}}.

**Cálculos especializados reais:** [].

| Evento/hora | Actor→target | Emissor | Testemunhas | Contexto |
| --- | --- | --- | --- | --- |
| 20141 / 2 / AspirationAdopted | 1173→None | ["agency.AgencySystem.event","agency.AgencySystem.aspirations","agency.AgencySystem.refresh"] | [1173] | {"domain":"wealth","intensity":62.11} |
| 20145 / 2 / FactionRecruitmentInterest | 1173→1176 | ["access.AccessActions.emit","access.AccessActions.refresh","needs.NeedSystem.refresh"] | [1173] | {"reason":"few_members","members":1} |
| 20147 / 2 / RouteUnknownBlockedTravel | 1173→302 | ["geography.Geography.emit","geography.Geography.block","geography.Geography.candidates"] | [1173] | {"reason":"route_unknown","origin":1170,"place_known":true} |
| 20150 / 2 / FactionContribution | 1173→1176 | ["access.AccessActions.emit","access.AccessActions.execute","goals.GoalSystem._execute"] | [1173] | {"transfers":1} |

**Aprendizado aceito durante a decisão (amostra):** [{"npc":1173,"event":20141,"kind":"AspirationAdopted","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":1173,"event":20145,"kind":"FactionRecruitmentInterest","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":1173,"event":20147,"kind":"RouteUnknownBlockedTravel","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":1173,"event":20150,"kind":"FactionContribution","source":null,"firsthand":true,"confidence":100,"latency":0}].

**Recibos posteriores ligados ao mesmo event_id:** [{"event":20141,"kind":"AspirationAdopted","learned":{"count":1,"first":2,"last":2,"first_people":[1173]}},{"event":20145,"kind":"FactionRecruitmentInterest","learned":{"count":1,"first":2,"last":2,"first_people":[1173]}},{"event":20147,"kind":"RouteUnknownBlockedTravel","learned":{"count":1,"first":2,"last":2,"first_people":[1173]}},{"event":20150,"kind":"FactionContribution","learned":{"count":1,"first":2,"last":2,"first_people":[1173]}}]. Contagem é operações de aprendizado aceitas, não indivíduos únicos.

**Consequência imediata:** {"id":1173,"name":"Aldren Hammer","hour":2,"alive":true,"profession":"caçador","lod":"local","position":{"map_id":1170,"x":5,"y":5},"residence":302,"hp":100,"hunger":35,"thirst":4,"fatigue":9.399999999999999,"money":5,"food":3,"water":5,"local_food":null,"local_water":null,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{}}. **Observação/relações com o alvo ao final:** {"observation_end":null,"relations_end":[{"source_id":1173,"target_id":1176,"kind":"lealdade","value":100}]}. Não usar esse estado posterior como entrada antiga nem atribuir consequências futuras sem vínculo causal.

### 28. family — Nora Hammer #1989, h220: check_relative

**Pressão escolhida:** `family` #82204, prioridade 71.72957142857142, base 46.5, fonte `event:237632`, alvo 1992. Motivo: Ausência percebida após encontros anteriores.

**Contexto preservado:** {"mode":"missing","source_event":237632,"known_location":{"map_id":162,"x":2,"y":2},"diagnostic":{"reason":"Selected","competing":null,"turn":220}}.

**Entrada:** {"id":1989,"name":"Nora Hammer","hour":220,"alive":true,"profession":"guarda","lod":"active","position":{"map_id":162,"x":5,"y":6},"residence":162,"hp":100,"hunger":22,"thirst":38,"fatigue":44.00000000000041,"money":5,"food":0,"water":0,"local_food":14,"local_water":149,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{"crime:270502":232,"crime:276561":237}}.

**Personalidade:** {"honesty":31,"compassion":30,"courage":92,"independence":25,"greed":94,"diligence":82,"family_loyalty":62,"persistence":39,"temperament":55,"vengefulness":72,"ambition":45,"sadism":0}. **Emoções escalares de entrada:** {"anger":13.199999999999989,"resentment":9.260000000000012,"humiliation":7.400000000000006,"desperation":9.150000000000006,"last_updated":219,"last_support":-10000,"strain":21.225000000000005,"adaptation":0,"last_adapted":0,"stable_material_hours":0,"nested_collections":"LACUNA: cópia rasa; histórico não utilizado"}.

**Conhecimento/locais de entrada:** {"known_places":{"market":{"map_id":162,"x":5,"y":9},"home":{"map_id":162,"x":2,"y":2},"work":{"map_id":162,"x":5,"y":9},"forage":{"map_id":162,"x":1,"y":9},"well_home":{"map_id":162,"x":2,"y":2},"well_rural":{"map_id":162,"x":1,"y":9},"sacred":{"map_id":162,"x":5,"y":1}},"known_towns":[162,3,191,209],"route_knowledge_count":6,"knowledge_ids_before":[269401,269406,270199,270502,270507,270526,270531,270529,270534,270536,271356,271359,271638,271640,271647,271649,271651,260753,272571,272922,272923,272925,272935,272942,272948,273778,274143,274148,274969,275286,275288,275297,276563,276561,276571,276575,276582,277826,277827,277828,277829,277830,277831,277837,278657,278954,278958,278960,278966,278971,278969,278975,278977,251371,236578,195652,279945,280273,280280,280282,280284,280291,281339,281342],"market_observation":{"turn":217,"town_id":162,"stock":{"food":11,"grain":27,"water":156,"iron":120,"wood":94},"temporary_work":true,"offers_expire_at":241,"training_offer":null,"price":3,"price_turn":217}}.

**Fatos-fonte retidos após percepção:** [{"event_id":278971,"kind":"WantedIssued","actor_id":185,"target_id":162,"location":{"map_id":162,"x":5,"y":9},"turn":215,"description":"Cael Douran registrou procura por Elena Corven.","confidence":100,"required_trust":0,"source_id":null,"source_kind":"direct","context":{"record_id":278970,"suspect_id":2024,"source_fact":278969,"severity":1,"confidence":100,"last_known_location":{"map_id":162,"x":5,"y":9}}}].

| Need | ID/alvo | Base→prioridade | Estado/fonte |
| --- | --- | --- | --- |
| family | 82204/1992 | 46.5→71.72957142857142 | selected / event:237632 |
| food_reserve | 51225/None | 38.4→69.74558823529412 | active / food_reserve |
| money | 159775/None | 44.458333333333336→69.60233333333333 | active / economy |
| military_service | 51227/162 | 55→67.4884 | active / known_local_case |
| family | 251712/1987 | 41.4→65.63282857142858 | active / event:251711 |
| response | 269384/185 | 55→58.701 | active / event:269383 |
| political_pressure | 209154/None | 46.208333333333336→57.428333333333335 | active / own_shared_problem |
| migration | 270505/191 | 52→54.544 | active / known_towns |
| advancement | 31078/None | 23.093400000000003→47.35646772571429 | selected / aspiration:wealth |
| rest | 51226/None | 44.00000000000041→46.25000000000041 | active / physiology |
| religious_interest | 31079/5908 | 36.5→46.1324 | active / own_faith |
| water | 41520/None | 38→38.9 | active / physiology |

**Alternativas/gates realmente vistos:**

Need #82204 (`family`): 1 Solutions entraram em _evaluate; 1 saíram disponíveis. Entrada: `check_relative`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| check_relative | {"target":1992,"destination":{"map_id":162,"x":2,"y":2}} | 62.75000000000001 | {"base":0.275,"independence":0.03125,"family_loyalty":0.0775,"travel":-0.07} | {"feeding":null,"action_pressure":null} |

Need #82204 (`family`): 1 Solutions entraram em _evaluate; 1 saíram disponíveis. Entrada: `check_relative`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| check_relative | {"target":1992,"destination":{"map_id":162,"x":2,"y":2}} | 62.75000000000001 | {"base":0.275,"independence":0.03125,"family_loyalty":0.0775,"travel":-0.07} | {"feeding":null,"action_pressure":null} |

Need #251712 (`family`): 1 Solutions entraram em _evaluate; 1 saíram disponíveis. Entrada: `check_relative`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| check_relative | {"target":1987,"destination":{"map_id":162,"x":5,"y":9}} | 70.75 | {"base":0.275,"independence":0.03125,"family_loyalty":0.0775,"travel":-0.03} | {"feeding":null,"action_pressure":null} |

Need #31078 (`advancement`): 1 Solutions entraram em _evaluate; 1 saíram disponíveis. Entrada: `work`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| work | {"target":null,"destination":{"map_id":162,"x":5,"y":9}} | 85.0 | {"base":0.25,"diligence":0.205,"physical_depletion":0.0,"travel":-0.03,"no_progress":0.0} | {"feeding":null,"action_pressure":null} |

**Escolhas intermediárias:** [{"chosen":{"action":"check_relative","score":62.75000000000001,"target":1992,"destination":{"map_id":162,"x":2,"y":2},"terms":{"base":0.275,"independence":0.03125,"family_loyalty":0.0775,"travel":-0.07},"feeding":null,"action_pressure":null},"near_scores":[62.75000000000001],"variation_draws":"não capturados; RNG não consultado pelo observador"}].

**Preparação/substituição posterior:** [].

**Winner final / Goal:** {"winner":{"action":"check_relative","score":62.75000000000001,"target":1992,"destination":{"map_id":162,"x":2,"y":2},"terms":{"base":0.275,"independence":0.03125,"family_loyalty":0.0775,"travel":-0.07},"feeding":null,"action_pressure":null},"goal":{"id":281343,"need_id":82204,"action":"check_relative","score":56.75,"created_at":217,"target_id":1992,"destination":{"map_id":162,"x":2,"y":2},"status":"active","outcome":""},"suspended_before":null,"suspended_after":null}.

**Por que outras Needs não foram executadas:** a fila prioriza emergência/priority/ID e para na primeira solucionável, sujeita à continuidade/preparo. Outras pressões retidas: food_reserve#51225(69.74558823529412), money#159775(69.60233333333333), military_service#51227(67.4884), family#251712(65.63282857142858), response#269384(58.701), political_pressure#209154(57.428333333333335), migration#270505(54.544), advancement#31078(47.35646772571429), rest#51226(46.25000000000041), religious_interest#31079(46.1324), water#41520(38.9). Não atribuir score global entre Needs.

**Execução:** execute não foi chamado neste trace. A Goal pode ter iniciado/continuado deslocamento; o snapshot e a posição posterior delimitam essa conclusão.

**Cálculos especializados reais:** [{"system":"lethal_decision","function":"lethal_decisions.LethalDecisionSystem.evaluate","result":{"available":false,"pressure":-43.26,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"response","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":12.24,"directed_emotion":0.0,"commitment":0.0,"sadism":0.0,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":16.5,"moral_restraint":3.7199999999999998,"fear":0.0,"risk":5.275884809848319,"bond":0.0,"authority_or_witnesses":0.0,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{"pressure":-43.26,"cause":{"severity":0,"grave":false,"causes":[],"facts":[],"confidence":0,"mode":"retributive","confirmed_injury":0}}},{"system":"lethal_decision","function":"lethal_decisions.LethalDecisionSystem.evaluate","result":{"available":false,"pressure":-43.26,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"response","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":12.24,"directed_emotion":0.0,"commitment":0.0,"sadism":0.0,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":16.5,"moral_restraint":3.7199999999999998,"fear":0.0,"risk":5.275884809848319,"bond":0.0,"authority_or_witnesses":0.0,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{"pressure":-43.26,"cause":{"severity":0,"grave":false,"causes":[],"facts":[],"confidence":0,"mode":"retributive","confirmed_injury":0}}},{"system":"lethal_pressure","function":"lethality.LethalPressure.evaluate","result":{"available":false,"pressure":-43.26,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"response","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":12.24,"directed_emotion":0.0,"commitment":0.0,"sadism":0.0,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":16.5,"moral_restraint":3.7199999999999998,"fear":0.0,"risk":5.275884809848319,"bond":0.0,"authority_or_witnesses":0.0,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{}}].

**Evento:** nenhum evento retido durante esta decisão. Isso pode significar movimento/efeito sem evento; não implica falha.

**Aprendizado aceito durante a decisão (amostra):** [].

**Recibos posteriores ligados ao mesmo event_id:** []. Contagem é operações de aprendizado aceitas, não indivíduos únicos.

**Consequência imediata:** {"id":1989,"name":"Nora Hammer","hour":220,"alive":true,"profession":"guarda","lod":"active","position":{"map_id":162,"x":5,"y":5},"residence":162,"hp":100,"hunger":22,"thirst":38,"fatigue":44.00000000000041,"money":5,"food":0,"water":0,"local_food":14,"local_water":149,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{"crime:270502":232,"crime:276561":237}}. **Observação/relações com o alvo ao final:** {"observation_end":{"turn":182,"position":{"map_id":162,"x":2,"y":2},"hunger":64,"thirst":49,"health":100,"alive":true,"profession":"caçador","weapon_power":10,"injured":0},"relations_end":[{"source_id":1989,"target_id":1992,"kind":"pai_de","value":100},{"source_id":1989,"target_id":1992,"kind":"amizade","value":48},{"source_id":1989,"target_id":1992,"kind":"confiança","value":62}]}. Não usar esse estado posterior como entrada antiga nem atribuir consequências futuras sem vínculo causal.

### 29. food — Ruan Hammer #5361, h241: fill_water

**Pressão escolhida:** `food` #22637, prioridade 100, base 100, fonte `physiology`, alvo None. Motivo: Fome.

**Contexto preservado:** {"emergency":true}.

**Entrada:** {"id":5361,"name":"Ruan Hammer","hour":241,"alive":true,"profession":"ferreiro","lod":"active","position":{"map_id":976,"x":3,"y":8},"residence":976,"hp":100,"hunger":99,"thirst":77,"fatigue":59.200000000000514,"money":0,"food":0,"water":0,"local_food":4,"local_water":158,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{}}.

**Personalidade:** {"honesty":39,"compassion":37,"courage":44,"independence":51,"greed":62,"diligence":22,"family_loyalty":27,"persistence":71,"temperament":60,"vengefulness":6,"ambition":9,"sadism":0}. **Emoções escalares de entrada:** {"anger":1.5000000000000142,"resentment":34.04000000000008,"humiliation":7.099999999999983,"desperation":13.74999999999999,"last_updated":240,"last_support":167,"strain":39.16700000000001,"adaptation":0,"last_adapted":0,"stable_material_hours":0,"nested_collections":"LACUNA: cópia rasa; histórico não utilizado"}.

**Conhecimento/locais de entrada:** {"known_places":{"market":{"map_id":976,"x":5,"y":9},"home":{"map_id":976,"x":2,"y":2},"work":{"map_id":976,"x":8,"y":2},"forage":{"map_id":976,"x":1,"y":9},"well_home":{"map_id":976,"x":2,"y":2},"well_rural":{"map_id":976,"x":1,"y":9},"sacred":{"map_id":976,"x":5,"y":1}},"known_towns":[976,864],"route_knowledge_count":2,"knowledge_ids_before":[219759,219762,220004,220954,220957,220972,221248,221254,222280,222283,223558,223561,223572,223576,223860,224881,224884,224888,224899,224904,192342,225330,226499,227714,227719,227944,228881,228883,228891,228900,229155,231077,231083,231301,232101,232104,232106,214072,242710,243828,245008,245010,209968,247558,248673,248680,248682,248692,248696,252432,241588,255410,259318,81992,265570,235444,263414,276032,286361,286360,295490,298775,289407,302255],"market_observation":{"turn":230,"town_id":976,"stock":{"food":6,"grain":63,"water":134,"iron":120,"wood":120},"temporary_work":true,"offers_expire_at":254,"training_offer":null,"price":3,"price_turn":173}}.

**Fatos-fonte retidos após percepção:** [{"event_id":295490,"kind":"AbsenceNoticed","actor_id":5361,"target_id":null,"location":{"map_id":976,"x":8,"y":2},"turn":230,"description":"Ruan Hammer não localiza um familiar há 36 horas.","confidence":100,"required_trust":0,"source_id":null,"source_kind":"direct","context":{"last_seen":194,"relative_id":5358}},{"event_id":302255,"kind":"AbsenceNoticed","actor_id":5361,"target_id":null,"location":{"map_id":976,"x":3,"y":3},"turn":236,"description":"Ruan Hammer não localiza um familiar há 39 horas.","confidence":100,"required_trust":0,"source_id":null,"source_kind":"direct","context":{"last_seen":197,"relative_id":5355}}].

| Need | ID/alvo | Base→prioridade | Estado/fonte |
| --- | --- | --- | --- |
| food | 22637/None | 100→100 | active / physiology |
| water | 42621/None | 77→85 | active / physiology |
| money | 122801/None | 58.708333333333336→72.24033333333335 | active / economy |
| rest | 42622/None | 59.200000000000514→67.20000000000051 | active / physiology |
| food_reserve | 32243/None | 41.0→66.632 | active / food_reserve |
| family | 109375/5358 | 46.0→62.20739999999999 | active / event:295490 |
| political_pressure | 148809/None | 47.05833333333334→58.26573333333334 | active / own_shared_problem |
| family | 64544/5355 | 46.5→54.5424 | active / event:302255 |
| advancement | 22639/None | 18.3198→28.5698 | active / aspiration:wealth |

**Alternativas/gates realmente vistos:**

Need #22637 (`food`): 4 Solutions entraram em _evaluate; 4 saíram disponíveis. Entrada: `steal, forage, work, work_for_food`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| forage | {"target":null,"destination":{"map_id":976,"x":1,"y":9}} | 54.49999999999999 | {"base":0.175,"independence":0.1275,"hunter":0.0,"travel":-0.03} | {"feeding":{"EstimatedTimeUntilFoodConsumed":5,"EstimatedSurvivalMargin":34,"economically_viable":true,"survival_viable":true,"reason":null,"known_conditions":["UnknownPrice","DistantProduct"]},"action_pressure":null} |
| steal | {"target":null,"destination":{"map_id":976,"x":5,"y":9}} | 54.470637343324825 | {"base":0.35,"greed":0.10333333333333333,"honesty":-0.195,"courage":0.022000000000000002,"travel":-0.03,"pressure_moral_tolerance":0.022019853383290818} | {"feeding":{"EstimatedTimeUntilFoodConsumed":5,"EstimatedSurvivalMargin":34,"economically_viable":true,"survival_viable":true,"reason":null,"known_conditions":["UnknownPrice","DistantProduct"]},"action_pressure":null} |
| work_for_food | {"target":null,"destination":{"map_id":976,"x":1,"y":9}} | 44.5 | {"base":0.225,"diligence":0.0275,"physical_depletion":0.0,"travel":-0.03} | {"feeding":{"EstimatedTimeUntilFoodConsumed":5,"EstimatedSurvivalMargin":34,"economically_viable":true,"survival_viable":true,"reason":null,"known_conditions":["UnknownPrice","DistantProduct"]},"action_pressure":null} |
| work | {"target":null,"destination":{"map_id":976,"x":8,"y":2}} | 39.0 | {"base":0.25,"diligence":0.055,"physical_depletion":0.0,"travel":-0.11} | {"feeding":{"EstimatedTimeUntilFoodConsumed":25,"EstimatedSurvivalMargin":34,"economically_viable":true,"survival_viable":true,"reason":null,"known_conditions":["UnknownPrice","DistantProduct"]},"action_pressure":null} |

Need #109375 (`family`): 1 Solutions entraram em _evaluate; 1 saíram disponíveis. Entrada: `check_relative`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| check_relative | {"target":5358,"destination":{"map_id":976,"x":2,"y":2}} | 60.5 | {"base":0.275,"independence":0.06375,"family_loyalty":0.03375,"travel":-0.07} | {"feeding":null,"action_pressure":null} |

Need #64544 (`family`): 1 Solutions entraram em _evaluate; 1 saíram disponíveis. Entrada: `check_relative`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| check_relative | {"target":5355,"destination":{"map_id":976,"x":2,"y":2}} | 60.5 | {"base":0.275,"independence":0.06375,"family_loyalty":0.03375,"travel":-0.07} | {"feeding":null,"action_pressure":null} |

Need #22639 (`advancement`): 2 Solutions entraram em _evaluate; 2 saíram disponíveis. Entrada: `work, work_for_food`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| work_for_food | {"target":null,"destination":{"map_id":976,"x":1,"y":9}} | 44.5 | {"base":0.225,"diligence":0.0275,"physical_depletion":0.0,"travel":-0.03} | {"feeding":null,"action_pressure":null} |
| work | {"target":null,"destination":{"map_id":976,"x":8,"y":2}} | 39.0 | {"base":0.25,"diligence":0.055,"physical_depletion":0.0,"travel":-0.11} | {"feeding":null,"action_pressure":null} |

**Escolhas intermediárias:** [{"chosen":{"action":"steal","score":54.470637343324825,"target":null,"destination":{"map_id":976,"x":5,"y":9},"terms":{"base":0.35,"greed":0.10333333333333333,"honesty":-0.195,"courage":0.022000000000000002,"travel":-0.03,"pressure_moral_tolerance":0.022019853383290818},"feeding":{"EstimatedTimeUntilFoodConsumed":5,"EstimatedSurvivalMargin":34,"economically_viable":true,"survival_viable":true,"reason":null,"known_conditions":["UnknownPrice","DistantProduct"]},"action_pressure":null},"near_scores":[54.49999999999999,54.470637343324825,44.5,39.0],"variation_draws":"não capturados; RNG não consultado pelo observador"}].

**Preparação/substituição posterior:** [{"input":{"action":"steal","score":54.470637343324825,"target":null,"destination":{"map_id":976,"x":5,"y":9},"terms":{"base":0.35,"greed":0.10333333333333333,"honesty":-0.195,"courage":0.022000000000000002,"travel":-0.03,"pressure_moral_tolerance":0.022019853383290818},"feeding":{"EstimatedTimeUntilFoodConsumed":5,"EstimatedSurvivalMargin":34,"economically_viable":true,"survival_viable":true,"reason":null,"known_conditions":["UnknownPrice","DistantProduct"]},"action_pressure":null},"replacement":{"action":"fill_water","score":100,"target":null,"destination":{"map_id":976,"x":5,"y":9},"terms":{},"feeding":null,"action_pressure":null},"travel":3,"horizon":9}].

**Winner final / Goal:** {"winner":{"action":"fill_water","score":100,"target":null,"destination":{"map_id":976,"x":5,"y":9},"terms":{},"feeding":null,"action_pressure":null},"goal":{"id":306655,"need_id":22637,"action":"fill_water","score":100,"created_at":240,"target_id":null,"destination":{"map_id":976,"x":5,"y":9},"status":"active","outcome":""},"suspended_before":null,"suspended_after":null}.

**Por que outras Needs não foram executadas:** a fila prioriza emergência/priority/ID e para na primeira solucionável, sujeita à continuidade/preparo. Outras pressões retidas: water#42621(85), money#122801(72.24033333333335), rest#42622(67.20000000000051), food_reserve#32243(66.632), family#109375(62.20739999999999), political_pressure#148809(58.26573333333334), family#64544(54.5424), advancement#22639(28.5698). Não atribuir score global entre Needs.

**Execução:** execute não foi chamado neste trace. A Goal pode ter iniciado/continuado deslocamento; o snapshot e a posição posterior delimitam essa conclusão.

**Cálculos especializados reais:** [].

**Evento:** nenhum evento retido durante esta decisão. Isso pode significar movimento/efeito sem evento; não implica falha.

**Aprendizado aceito durante a decisão (amostra):** [].

**Recibos posteriores ligados ao mesmo event_id:** []. Contagem é operações de aprendizado aceitas, não indivíduos únicos.

**Consequência imediata:** {"id":5361,"name":"Ruan Hammer","hour":241,"alive":true,"profession":"ferreiro","lod":"active","position":{"map_id":976,"x":3,"y":9},"residence":976,"hp":100,"hunger":99,"thirst":77,"fatigue":59.200000000000514,"money":0,"food":0,"water":0,"local_food":4,"local_water":158,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{}}. **Observação/relações com o alvo ao final:** {"observation_end":null,"relations_end":[]}. Não usar esse estado posterior como entrada antiga nem atribuir consequências futuras sem vínculo causal.

### 30. group — Aldren Vale #2789, h91: share_problem

**Pressão escolhida:** `political_pressure` #115998, prioridade 75.16999999999999, base 67.3, fonte `own_shared_problem`, alvo None. Motivo: Buscar representação para problema pessoal.

**Contexto preservado:** {}.

**Entrada:** {"id":2789,"name":"Aldren Vale","hour":91,"alive":true,"profession":"lenhador","lod":"active","position":{"map_id":367,"x":5,"y":9},"residence":367,"hp":100,"hunger":60,"thirst":47,"fatigue":36.0,"money":6,"food":2,"water":0,"local_food":116,"local_water":114,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{}}.

**Personalidade:** {"honesty":83,"compassion":13,"courage":91,"independence":68,"greed":85,"diligence":7,"family_loyalty":23,"persistence":80,"temperament":93,"vengefulness":23,"ambition":82,"sadism":2}. **Emoções escalares de entrada:** {"anger":30.89999999999999,"resentment":19.12000000000001,"humiliation":16.3,"desperation":0.0,"last_updated":90,"last_support":31,"strain":0,"adaptation":0,"last_adapted":0,"stable_material_hours":0,"nested_collections":"LACUNA: cópia rasa; histórico não utilizado"}.

**Conhecimento/locais de entrada:** {"known_places":{"market":{"map_id":367,"x":5,"y":9},"home":{"map_id":367,"x":2,"y":2},"work":{"map_id":367,"x":8,"y":2},"forage":{"map_id":367,"x":1,"y":9},"well_home":{"map_id":367,"x":2,"y":2},"well_rural":{"map_id":367,"x":1,"y":9},"sacred":{"map_id":367,"x":5,"y":1}},"known_towns":[367,302],"route_knowledge_count":2,"knowledge_ids_before":[121334,121352,121885,122258,122264,122271,122970,123350,124353,124875,124880,125218,125226,99652,125975,125977,126330,126333,126336,126342,127407,127413,128309,128312,128322,128972,128973,128975,129344,129350,129356,129360,129365,130338,130336,130345,130347,130349,130357,130359,130361,130365,130368,130371,130984,131370,131376,131385,131392,131396,115987,132169,132568,132578,132576,132585,132587,132588,132600,132602,132604,133253,133701,133704],"market_observation":{"turn":90,"town_id":367,"stock":{"food":117,"grain":112,"water":114,"iron":70,"wood":90},"temporary_work":true,"offers_expire_at":114,"training_offer":null,"price":2,"price_turn":90}}.

**Fatos-fonte retidos após percepção:** [{"event_id":132576,"kind":"ItemStolen","actor_id":2769,"target_id":367,"location":{"map_id":367,"x":5,"y":9},"turn":90,"description":"Ruan Arven roubou comida no mercado de Valria.","confidence":100,"required_trust":0,"source_id":null,"source_kind":"direct","context":{"item_id":132575,"item_kind":"food"}}].

| Need | ID/alvo | Base→prioridade | Estado/fonte |
| --- | --- | --- | --- |
| political_pressure | 115998/None | 67.3→75.16999999999999 | active / own_shared_problem |
| food | 18090/None | 70.0→71.8 | active / physiology |
| organizational_survival | 119278/2786 | 53.425→68.12259999999999 | active / group:88611 |
| family | 62507/2786 | 46.0→63.431 | active / event:118248 |
| advancement | 18091/None | 27.0948→61.312931108571426 | selected / self_assessment:1 |
| protection | 115588/2789 | 45→54.763999999999996 | active / event:132576 |
| migration | 115997/302 | 52→54.55 | active / known_towns |
| water | 45274/None | 47→51.5 | active / physiology |
| status | 77579/None | 20→49.446 | active / encounter:597:40 |
| money | 124342/None | 38.375→41.125 | active / economy |
| rest | 35057/None | 36.0→37.35 | active / physiology |
| religious_interest | 18095/5909 | 24.75→34.6764 | active / own_faith |

**Alternativas/gates realmente vistos:**

Need #115998 (`political_pressure`): 1 Solutions entraram em _evaluate; 1 saíram disponíveis. Entrada: `share_problem`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| share_problem | {"target":null,"destination":{"map_id":367,"x":5,"y":9}} | 36.75 | {"base":0.225,"compassion":0.009750000000000002,"independence":-0.051000000000000004,"travel":-0.0} | {"feeding":null,"action_pressure":null} |

Need #62507 (`family`): 1 Solutions entraram em _evaluate; 1 saíram disponíveis. Entrada: `check_relative`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| check_relative | {"target":2786,"destination":{"map_id":367,"x":5,"y":9}} | 77.75000000000001 | {"base":0.275,"independence":0.085,"family_loyalty":0.02875,"travel":-0.0} | {"feeding":null,"action_pressure":null} |

Need #18091 (`advancement`): 2 Solutions entraram em _evaluate; 2 saíram disponíveis. Entrada: `work, work_for_food`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| work_for_food | {"target":null,"destination":{"map_id":367,"x":1,"y":9}} | 38.75 | {"base":0.225,"diligence":0.00875,"physical_depletion":0.0,"travel":-0.04,"no_progress":0.0} | {"feeding":null,"action_pressure":null} |
| work | {"target":null,"destination":{"map_id":367,"x":8,"y":2}} | 33.5 | {"base":0.25,"diligence":0.0175,"physical_depletion":0.0,"travel":-0.1,"no_progress":0.0} | {"feeding":null,"action_pressure":null} |

Need #115588 (`protection`): 21 Solutions entraram em _evaluate; 21 saíram disponíveis. Entrada: `denounce, denounce, denounce, denounce, denounce, denounce, denounce, denounce, confront, threaten, demand_return, warn, insult, call_help, calm, withdraw, flee, defend, forgive, apologize, surrender`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| denounce | {"target":390,"destination":{"map_id":367,"x":5,"y":9}} | 94.8 | {"base":0.225,"honesty":0.14525,"vengefulness":0.023000000000000003,"courage":0.06825,"trust":0.0125,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| denounce | {"target":2748,"destination":{"map_id":367,"x":5,"y":9}} | 94.8 | {"base":0.225,"honesty":0.14525,"vengefulness":0.023000000000000003,"courage":0.06825,"trust":0.0125,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| denounce | {"target":2794,"destination":{"map_id":367,"x":5,"y":9}} | 94.8 | {"base":0.225,"honesty":0.14525,"vengefulness":0.023000000000000003,"courage":0.06825,"trust":0.0125,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| denounce | {"target":2817,"destination":{"map_id":367,"x":5,"y":9}} | 94.8 | {"base":0.225,"honesty":0.14525,"vengefulness":0.023000000000000003,"courage":0.06825,"trust":0.0125,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| denounce | {"target":2840,"destination":{"map_id":367,"x":5,"y":9}} | 94.8 | {"base":0.225,"honesty":0.14525,"vengefulness":0.023000000000000003,"courage":0.06825,"trust":0.0125,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| denounce | {"target":2863,"destination":{"map_id":367,"x":5,"y":9}} | 94.8 | {"base":0.225,"honesty":0.14525,"vengefulness":0.023000000000000003,"courage":0.06825,"trust":0.0125,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| demand_return | {"target":2769,"destination":null} | 90.4 | {"base":0.2,"honesty":0.10375,"persistence":0.08,"courage":0.06825,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| denounce | {"target":2403,"destination":{"map_id":367,"x":2,"y":2}} | 74.8 | {"base":0.225,"honesty":0.14525,"vengefulness":0.023000000000000003,"courage":0.06825,"trust":0.0125,"travel":-0.1} | {"feeding":null,"action_pressure":null} |
| denounce | {"target":2771,"destination":{"map_id":367,"x":2,"y":2}} | 74.8 | {"base":0.225,"honesty":0.14525,"vengefulness":0.023000000000000003,"courage":0.06825,"trust":0.0125,"travel":-0.1} | {"feeding":null,"action_pressure":null} |
| defend | {"target":2769,"destination":null} | 66.14999999999999 | {"base":0.2,"risk":0.0625,"courage":0.06825,"defensive":0.0,"injury":-0.0,"travel":-0.0} | {"feeding":null,"action_pressure":null} |

Need #77579 (`status`): 5 Solutions entraram em _evaluate; 5 saíram disponíveis. Entrada: `give_supplies, give_supplies, give_supplies, work, work_for_food`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| give_supplies | {"target":376,"destination":null} | 64.15 | {"base":0.275,"compassion":0.02275,"family_loyalty":0.023000000000000003,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| give_supplies | {"target":2743,"destination":null} | 64.15 | {"base":0.275,"compassion":0.02275,"family_loyalty":0.023000000000000003,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| give_supplies | {"target":2849,"destination":null} | 64.15 | {"base":0.275,"compassion":0.02275,"family_loyalty":0.023000000000000003,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| work_for_food | {"target":null,"destination":{"map_id":367,"x":1,"y":9}} | 38.75 | {"base":0.225,"diligence":0.00875,"physical_depletion":0.0,"travel":-0.04} | {"feeding":null,"action_pressure":null} |
| work | {"target":null,"destination":{"map_id":367,"x":8,"y":2}} | 33.5 | {"base":0.25,"diligence":0.0175,"physical_depletion":0.0,"travel":-0.1} | {"feeding":null,"action_pressure":null} |

**Escolhas intermediárias:** [{"chosen":{"action":"share_problem","score":36.75,"target":null,"destination":{"map_id":367,"x":5,"y":9},"terms":{"base":0.225,"compassion":0.009750000000000002,"independence":-0.051000000000000004,"travel":-0.0},"feeding":null,"action_pressure":null},"near_scores":[36.75],"variation_draws":"não capturados; RNG não consultado pelo observador"}].

**Preparação/substituição posterior:** [].

**Winner final / Goal:** {"winner":{"action":"share_problem","score":36.75,"target":null,"destination":{"map_id":367,"x":5,"y":9},"terms":{"base":0.225,"compassion":0.009750000000000002,"independence":-0.051000000000000004,"travel":-0.0},"feeding":null,"action_pressure":null},"goal":{"id":133710,"need_id":115998,"action":"share_problem","score":36.75,"created_at":91,"target_id":null,"destination":{"map_id":367,"x":5,"y":9},"status":"completed","outcome":"Problema próprio comunicado presencialmente."},"suspended_before":null,"suspended_after":null}.

**Por que outras Needs não foram executadas:** a fila prioriza emergência/priority/ID e para na primeira solucionável, sujeita à continuidade/preparo. Outras pressões retidas: food#18090(71.8), organizational_survival#119278(68.12259999999999), family#62507(63.431), advancement#18091(61.312931108571426), protection#115588(54.763999999999996), migration#115997(54.55), water#45274(51.5), status#77579(49.446), money#124342(41.125), rest#35057(37.35), religious_interest#18095(34.6764). Não atribuir score global entre Needs.

**Execução:** {"success":true,"result":[true,"Problema próprio comunicado presencialmente."],"goal_at_entry":{"id":133710,"need_id":115998,"action":"share_problem","score":36.75,"created_at":91,"target_id":null,"destination":{"map_id":367,"x":5,"y":9},"status":"active","outcome":""},"before":{"id":2789,"name":"Aldren Vale","hour":91,"alive":true,"profession":"lenhador","lod":"active","position":{"map_id":367,"x":5,"y":9},"residence":367,"hp":100,"hunger":60,"thirst":47,"fatigue":36.0,"money":6,"food":2,"water":0,"local_food":116,"local_water":114,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{}},"after":{"id":2789,"name":"Aldren Vale","hour":91,"alive":true,"profession":"lenhador","lod":"active","position":{"map_id":367,"x":5,"y":9},"residence":367,"hp":100,"hunger":60,"thirst":47,"fatigue":36.0,"money":6,"food":2,"water":0,"local_food":116,"local_water":114,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{}}}.

**Cálculos especializados reais:** [{"system":"lethal_decision","function":"lethal_decisions.LethalDecisionSystem.evaluate","result":{"available":false,"pressure":-60.0,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"protection","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":3.91,"directed_emotion":3.9435000000000002,"commitment":0.0,"sadism":0.26,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":7.15,"moral_restraint":9.959999999999999,"fear":0.0,"risk":6.0,"bond":0.0,"authority_or_witnesses":15,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{"pressure":-60.0,"cause":{"severity":0,"grave":false,"causes":[],"facts":[],"confidence":0,"mode":"retributive","confirmed_injury":0}}},{"system":"lethal_decision","function":"lethal_decisions.LethalDecisionSystem.evaluate","result":{"available":false,"pressure":-60.0,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"protection","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":3.91,"directed_emotion":3.9435000000000002,"commitment":0.0,"sadism":0.26,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":7.15,"moral_restraint":9.959999999999999,"fear":0.0,"risk":6.0,"bond":0.0,"authority_or_witnesses":15,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{"pressure":-60.0,"cause":{"severity":0,"grave":false,"causes":[],"facts":[],"confidence":0,"mode":"retributive","confirmed_injury":0}}},{"system":"lethal_pressure","function":"lethality.LethalPressure.evaluate","result":{"available":false,"pressure":-60.0,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"protection","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":3.91,"directed_emotion":3.9435000000000002,"commitment":0.0,"sadism":0.26,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":7.15,"moral_restraint":9.959999999999999,"fear":0.0,"risk":6.0,"bond":0.0,"authority_or_witnesses":15,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{}}].

| Evento/hora | Actor→target | Emissor | Testemunhas | Contexto |
| --- | --- | --- | --- | --- |
| 133711 / 91 / ProblemShared | 2789→None | ["society.SocietySystem.emit","society.SocietySystem.execute","goals.GoalSystem._execute"] | [376,393,2731,2743,2748,2754,2769,2789,2794,2835,2840,2849,2866] | {"cause":"security","subject":null,"severity":55,"source_fact":null} |

**Aprendizado aceito durante a decisão (amostra):** [{"npc":376,"event":133711,"kind":"ProblemShared","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":393,"event":133711,"kind":"ProblemShared","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":2731,"event":133711,"kind":"ProblemShared","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":2743,"event":133711,"kind":"ProblemShared","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":2748,"event":133711,"kind":"ProblemShared","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":2754,"event":133711,"kind":"ProblemShared","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":2769,"event":133711,"kind":"ProblemShared","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":2789,"event":133711,"kind":"ProblemShared","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":2794,"event":133711,"kind":"ProblemShared","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":2835,"event":133711,"kind":"ProblemShared","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":2840,"event":133711,"kind":"ProblemShared","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":2849,"event":133711,"kind":"ProblemShared","source":null,"firsthand":true,"confidence":100,"latency":0}].

**Recibos posteriores ligados ao mesmo event_id:** [{"event":133711,"kind":"ProblemShared","learned":{"count":13,"first":91,"last":91,"first_people":[376,393,2731,2743,2748,2754]}}]. Contagem é operações de aprendizado aceitas, não indivíduos únicos.

**Consequência imediata:** {"id":2789,"name":"Aldren Vale","hour":91,"alive":true,"profession":"lenhador","lod":"active","position":{"map_id":367,"x":5,"y":9},"residence":367,"hp":100,"hunger":60,"thirst":47,"fatigue":36.0,"money":6,"food":2,"water":0,"local_food":116,"local_water":114,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{}}. **Observação/relações com o alvo ao final:** {"observation_end":null,"relations_end":[]}. Não usar esse estado posterior como entrada antiga nem atribuir consequências futuras sem vínculo causal.

### 31. investigation — Tomas Corven #1903, h234: pursue

**Pressão escolhida:** `pursuit` #133535, prioridade 74.6, base 68, fonte `event:250490`, alvo 1892. Motivo: Localizar pessoa procurada com evidência conhecida.

**Contexto preservado:** {"institutional_role":"search","known_location":{"map_id":144,"x":2,"y":2},"source_event":250490}.

**Entrada:** {"id":1903,"name":"Tomas Corven","hour":234,"alive":true,"profession":"guarda","lod":"local","position":{"map_id":144,"x":2,"y":2},"residence":144,"hp":100,"hunger":49,"thirst":63,"fatigue":59.20000000000002,"money":1,"food":0,"water":1,"local_food":6,"local_water":146,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{}}.

**Personalidade:** {"honesty":89,"compassion":56,"courage":35,"independence":34,"greed":85,"diligence":38,"family_loyalty":93,"persistence":48,"temperament":84,"vengefulness":42,"ambition":57,"sadism":0}. **Emoções escalares de entrada:** {"anger":15.299999999999995,"resentment":23.820000000000032,"humiliation":8.100000000000001,"desperation":12.549999999999976,"last_updated":231,"last_support":211,"strain":60.83149999999996,"adaptation":0,"last_adapted":0,"stable_material_hours":0,"nested_collections":"LACUNA: cópia rasa; histórico não utilizado"}.

**Conhecimento/locais de entrada:** {"known_places":{"market":{"map_id":144,"x":3,"y":5},"home":{"map_id":144,"x":2,"y":2},"work":{"map_id":144,"x":3,"y":5},"forage":{"map_id":144,"x":1,"y":5},"well_home":{"map_id":144,"x":2,"y":2},"well_rural":{"map_id":144,"x":1,"y":5},"sacred":{"map_id":144,"x":3,"y":1}},"known_towns":[144,115,3],"route_knowledge_count":2,"knowledge_ids_before":[139844,258431,258432,258434,223723,239853,221122,239847,267207,267213,267215,268015,268018,268265,268268,269362,270480,270485,271348,271350,271624,271627,272911,272914,272917,272919,274117,274124,274127,274953,274956,276546,276554,277815,278649,278951,243969,222792,279754,280259,280266,281331,282356,282358,283460,283469,284554,285307,215591,286717,286720,287743,287747,287745,287749,287753,288554,288788,292914,293855,293858,285308,240649,267211],"market_observation":{"turn":224,"town_id":144,"stock":{"food":8,"grain":0,"water":150,"iron":49,"wood":67},"temporary_work":false,"offers_expire_at":248,"training_offer":null,"price":4,"price_turn":224}}.

**Fatos-fonte retidos após percepção:** [{"event_id":139844,"kind":"FamilyConcern","actor_id":1903,"target_id":1909,"location":{"map_id":144,"x":2,"y":2},"turn":96,"description":"Tomas Corven percebeu a privação de John Corven.","confidence":100,"required_trust":0,"source_id":null,"source_kind":"direct","context":{"observed_need":77}}].

| Need | ID/alvo | Base→prioridade | Estado/fonte |
| --- | --- | --- | --- |
| family | 65248/1909 | 63.099999999999994→96.11940285714286 | blocked / event:139844 |
| pursuit | 133535/1892 | 68→74.6 | active / event:250490 |
| money | 72861/None | 56.25→72.88999999999999 | active / economy |
| organizational_survival | 65249/1906 | 54.459→72.08314800000001 | active / group:38045 |
| food_reserve | 14334/None | 41.0→70.45454545454545 | active / food_reserve |
| water | 39626/None | 63→69.15 | active / physiology |
| rest | 41506/None | 59.20000000000002→67.20000000000002 | active / physiology |
| political_pressure | 39629/None | 51.8→63.644999999999996 | active / own_shared_problem |
| food | 32925/None | 53.5→54.55 | active / physiology |
| advancement | 14336/None | 24.2598→51.61774939428571 | selected / aspiration:wealth |
| migration | 266074/115 | 35→40.54 | active / known_towns |
| religious_interest | 14337/5908 | 24.5→27.599 | active / own_faith |

**Alternativas/gates realmente vistos:**

Need #65248 (`family`): 0 Solutions entraram em _evaluate; 0 saíram disponíveis. Entrada: ``.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |

Need #133535 (`pursuit`): 1 Solutions entraram em _evaluate; 1 saíram disponíveis. Entrada: `pursue`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| pursue | {"target":1892,"destination":{"map_id":144,"x":2,"y":2}} | 77.15530669072936 | {"base":0.275,"courage":0.035,"diligence":0.0285,"vengefulness":0.042,"critical_depletion":0.0,"travel":-0.0,"action_pressure":0.0,"pressure_risk_tolerance":0.005276533453646827} | {"feeding":null,"action_pressure":{"eligible":true,"world_pressure":0,"action_pressure":0.0,"eligibility_causes":[],"source_facts":[],"capacity":60.53,"perceived_capacity":53.27,"major_barriers":[],"selected_alternative":"pursue"}} |

Need #65248 (`family`): 0 Solutions entraram em _evaluate; 0 saíram disponíveis. Entrada: ``.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |

Need #14336 (`advancement`): 1 Solutions entraram em _evaluate; 1 saíram disponíveis. Entrada: `work`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| work | {"target":null,"destination":{"map_id":144,"x":3,"y":5}} | 61.0 | {"base":0.25,"diligence":0.095,"physical_depletion":0.0,"travel":-0.04,"no_progress":0.0} | {"feeding":null,"action_pressure":null} |

**Escolhas intermediárias:** [{"chosen":{"action":"pursue","score":77.15530669072936,"target":1892,"destination":{"map_id":144,"x":2,"y":2},"terms":{"base":0.275,"courage":0.035,"diligence":0.0285,"vengefulness":0.042,"critical_depletion":0.0,"travel":-0.0,"action_pressure":0.0,"pressure_risk_tolerance":0.005276533453646827},"feeding":null,"action_pressure":{"eligible":true,"world_pressure":0,"action_pressure":0.0,"eligibility_causes":[],"source_facts":[],"capacity":60.53,"perceived_capacity":53.27,"major_barriers":[],"selected_alternative":"pursue"}},"near_scores":[77.15530669072936],"variation_draws":"não capturados; RNG não consultado pelo observador"}].

**Preparação/substituição posterior:** [].

**Winner final / Goal:** {"winner":{"action":"pursue","score":77.15530669072936,"target":1892,"destination":{"map_id":144,"x":2,"y":2},"terms":{"base":0.275,"courage":0.035,"diligence":0.0285,"vengefulness":0.042,"critical_depletion":0.0,"travel":-0.0,"action_pressure":0.0,"pressure_risk_tolerance":0.005276533453646827},"feeding":null,"action_pressure":{"eligible":true,"world_pressure":0,"action_pressure":0.0,"eligibility_causes":[],"source_facts":[],"capacity":60.53,"perceived_capacity":53.27,"major_barriers":[],"selected_alternative":"pursue"}},"goal":{"id":299249,"need_id":133535,"action":"pursue","score":77.15530669072936,"created_at":234,"target_id":1892,"destination":{"map_id":144,"x":2,"y":2},"status":"completed","outcome":"Busca local sem encontro; não consulta posição remota."},"suspended_before":null,"suspended_after":null}.

**Por que outras Needs não foram executadas:** a fila prioriza emergência/priority/ID e para na primeira solucionável, sujeita à continuidade/preparo. Outras pressões retidas: family#65248(96.11940285714286), money#72861(72.88999999999999), organizational_survival#65249(72.08314800000001), food_reserve#14334(70.45454545454545), water#39626(69.15), rest#41506(67.20000000000002), political_pressure#39629(63.644999999999996), food#32925(54.55), advancement#14336(51.61774939428571), migration#266074(40.54), religious_interest#14337(27.599). Não atribuir score global entre Needs.

**Execução:** {"success":true,"result":[true,"Busca local sem encontro; não consulta posição remota."],"goal_at_entry":{"id":299249,"need_id":133535,"action":"pursue","score":77.15530669072936,"created_at":234,"target_id":1892,"destination":{"map_id":144,"x":2,"y":2},"status":"active","outcome":""},"before":{"id":1903,"name":"Tomas Corven","hour":234,"alive":true,"profession":"guarda","lod":"local","position":{"map_id":144,"x":2,"y":2},"residence":144,"hp":100,"hunger":49,"thirst":63,"fatigue":59.20000000000002,"money":1,"food":0,"water":1,"local_food":6,"local_water":146,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{}},"after":{"id":1903,"name":"Tomas Corven","hour":234,"alive":true,"profession":"guarda","lod":"local","position":{"map_id":144,"x":2,"y":2},"residence":144,"hp":100,"hunger":49,"thirst":63,"fatigue":59.20000000000002,"money":1,"food":0,"water":1,"local_food":6,"local_water":146,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{}}}.

**Cálculos especializados reais:** [{"system":"lethal_decision","function":"lethal_decisions.LethalDecisionSystem.evaluate","result":{"available":false,"pressure":-64.13,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"pursuit","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":7.140000000000001,"directed_emotion":3.7125000000000057,"commitment":0.0,"sadism":0.0,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":30.800000000000004,"moral_restraint":10.68,"fear":0.0,"risk":3.498542274052478,"bond":0.0,"authority_or_witnesses":0.0,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{"pressure":-64.13,"cause":{"severity":0,"grave":false,"causes":[],"facts":[],"confidence":0,"mode":"retributive","confirmed_injury":0}}},{"system":"lethal_decision","function":"lethal_decisions.LethalDecisionSystem.evaluate","result":{"available":false,"pressure":-64.13,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"pursuit","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":7.140000000000001,"directed_emotion":3.7125000000000057,"commitment":0.0,"sadism":0.0,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":30.800000000000004,"moral_restraint":10.68,"fear":0.0,"risk":3.498542274052478,"bond":0.0,"authority_or_witnesses":0.0,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{"pressure":-64.13,"cause":{"severity":0,"grave":false,"causes":[],"facts":[],"confidence":0,"mode":"retributive","confirmed_injury":0}}},{"system":"lethal_pressure","function":"lethality.LethalPressure.evaluate","result":{"available":false,"pressure":-64.13,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"pursuit","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":7.140000000000001,"directed_emotion":3.7125000000000057,"commitment":0.0,"sadism":0.0,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":30.800000000000004,"moral_restraint":10.68,"fear":0.0,"risk":3.498542274052478,"bond":0.0,"authority_or_witnesses":0.0,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{}},{"system":"capacity","function":"action_pressure.ActionPressureSystem.assess","result":{"eligible":true,"world_pressure":0,"action_pressure":0.0,"eligibility_causes":[],"source_facts":[],"capacity":60.53,"perceived_capacity":53.27,"major_barriers":[],"selected_alternative":"pursue"},"inputs":{}}].

| Evento/hora | Actor→target | Emissor | Testemunhas | Contexto |
| --- | --- | --- | --- | --- |
| 299250 / 234 / PursuitSearch | 1903→None | ["conflicts.ConflictSystem.execute","goals.GoalSystem._execute","goals.GoalSystem.execute"] | [1903] | {"target_id":1892,"source_fact":250490,"attempt":1} |

**Aprendizado aceito durante a decisão (amostra):** [{"npc":1903,"event":299250,"kind":"PursuitSearch","source":null,"firsthand":true,"confidence":100,"latency":0}].

**Recibos posteriores ligados ao mesmo event_id:** [{"event":299250,"kind":"PursuitSearch","learned":{"count":1,"first":234,"last":234,"first_people":[1903]}}]. Contagem é operações de aprendizado aceitas, não indivíduos únicos.

**Consequência imediata:** {"id":1903,"name":"Tomas Corven","hour":234,"alive":true,"profession":"guarda","lod":"local","position":{"map_id":144,"x":2,"y":2},"residence":144,"hp":100,"hunger":49,"thirst":63,"fatigue":59.20000000000002,"money":1,"food":0,"water":1,"local_food":6,"local_water":146,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{}}. **Observação/relações com o alvo ao final:** {"observation_end":{"turn":231,"position":{"map_id":144,"x":2,"y":2},"hunger":40,"thirst":57,"health":100,"alive":true,"profession":"ferreiro","weapon_power":4,"injured":0},"relations_end":[]}. Não usar esse estado posterior como entrada antiga nem atribuir consequências futuras sem vínculo causal.

### 32. justice — John Solaris #109, h157: secure

**Pressão escolhida:** `security` #114346, prioridade 0, base 60, fonte `event:211269`, alvo 1696. Motivo: Bela Solaris roubou comida no mercado de Elimir..

**Contexto preservado:** {}.

**Entrada:** {"id":109,"name":"John Solaris","hour":157,"alive":true,"profession":"guarda","lod":"active","position":{"map_id":97,"x":3,"y":5},"residence":97,"hp":100,"hunger":46,"thirst":48,"fatigue":29.99999999999999,"money":38,"food":2,"water":0,"local_food":106,"local_water":144,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{}}.

**Personalidade:** {"honesty":86,"compassion":61,"courage":69,"independence":10,"greed":45,"diligence":63,"family_loyalty":66,"persistence":8,"temperament":48,"vengefulness":91,"ambition":79,"sadism":0}. **Emoções escalares de entrada:** {"anger":0.0,"resentment":0.0,"humiliation":0.0,"desperation":0.0,"last_updated":156,"last_support":-10000,"strain":0,"adaptation":0,"last_adapted":0,"stable_material_hours":0,"nested_collections":"LACUNA: cópia rasa; histórico não utilizado"}.

**Conhecimento/locais de entrada:** {"known_places":{"market":{"map_id":97,"x":3,"y":5},"home":{"map_id":97,"x":2,"y":2},"work":{"map_id":97,"x":3,"y":5},"forage":{"map_id":97,"x":1,"y":5},"well_home":{"map_id":97,"x":2,"y":2},"well_rural":{"map_id":97,"x":1,"y":5},"sacred":{"map_id":97,"x":3,"y":1}},"known_towns":[97,50,3],"route_knowledge_count":2,"knowledge_ids_before":[156512,157283,157287,157522,157524,158660,158662,158664,159509,159725,90938,160585,160588,160589,160874,161765,161768,162102,162986,174786,131180,175986,177982,178766,181065,172482,184328,185473,187654,187663,188529,188530,188531,188528,188527,188598,188599,188602,188603,188604,188911,195590,196817,200117,200119,201181,201508,185470,204824,204827,205080,205082,207061,207064,207069,207073,208090,208093,210098,210101,211269,211271,211275,211277],"market_observation":{"turn":156,"town_id":97,"stock":{"food":107,"grain":2,"water":144,"iron":76,"wood":120},"temporary_work":false,"offers_expire_at":180,"training_offer":null,"price":2,"price_turn":156}}.

**Fatos-fonte retidos após percepção:** [{"event_id":211269,"kind":"ItemStolen","actor_id":1696,"target_id":97,"location":{"map_id":97,"x":3,"y":5},"turn":156,"description":"Bela Solaris roubou comida no mercado de Elimir.","confidence":100,"required_trust":0,"source_id":null,"source_kind":"direct","context":{"item_id":211268,"item_kind":"food"}}].

| Need | ID/alvo | Base→prioridade | Estado/fonte |
| --- | --- | --- | --- |
| security | 114346/1696 | 60→91.9204 | active / event:211269 |
| political_pressure | 114348/None | 66.85→71.45179999999999 | active / own_shared_problem |
| pursuit | 212153/1696 | 68→68.0 | active / event:211269 |
| food | 42846/None | 49.0→49.6 | active / physiology |
| water | 42847/None | 48→49.05 | active / physiology |
| work | 30426/None | 35→48.2 | active / profession |
| advancement | 13452/None | 15→42.75 | active / self_assessment:93 |
| rest | 42848/None | 29.99999999999999→30.59999999999999 | active / physiology |

**Alternativas/gates realmente vistos:**

Need #114346 (`security`): 1 Solutions entraram em _evaluate; 1 saíram disponíveis. Entrada: `secure`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| secure | {"target":1696,"destination":{"map_id":97,"x":3,"y":5}} | 93.0 | {"base":0.35,"courage":0.115,"travel":-0.0} | {"feeding":null,"action_pressure":null} |

Need #13452 (`advancement`): 1 Solutions entraram em _evaluate; 1 saíram disponíveis. Entrada: `work`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| work | {"target":null,"destination":{"map_id":97,"x":3,"y":5}} | 81.5 | {"base":0.25,"diligence":0.1575,"physical_depletion":0.0,"travel":-0.0} | {"feeding":null,"action_pressure":null} |

**Escolhas intermediárias:** [{"chosen":{"action":"secure","score":93.0,"target":1696,"destination":{"map_id":97,"x":3,"y":5},"terms":{"base":0.35,"courage":0.115,"travel":-0.0},"feeding":null,"action_pressure":null},"near_scores":[93.0],"variation_draws":"não capturados; RNG não consultado pelo observador"}].

**Preparação/substituição posterior:** [].

**Winner final / Goal:** {"winner":{"action":"secure","score":93.0,"target":1696,"destination":{"map_id":97,"x":3,"y":5},"terms":{"base":0.35,"courage":0.115,"travel":-0.0},"feeding":null,"action_pressure":null},"goal":{"id":212154,"need_id":114346,"action":"secure","score":93.0,"created_at":157,"target_id":1696,"destination":{"map_id":97,"x":3,"y":5},"status":"completed","outcome":"Suspeito encontrado; intervenção registrada."},"suspended_before":null,"suspended_after":null}.

**Por que outras Needs não foram executadas:** a fila prioriza emergência/priority/ID e para na primeira solucionável, sujeita à continuidade/preparo. Outras pressões retidas: political_pressure#114348(71.45179999999999), pursuit#212153(68.0), food#42846(49.6), water#42847(49.05), work#30426(48.2), advancement#13452(42.75), rest#42848(30.59999999999999). Não atribuir score global entre Needs.

**Execução:** {"success":true,"result":[true,"Suspeito encontrado; intervenção registrada."],"goal_at_entry":{"id":212154,"need_id":114346,"action":"secure","score":93.0,"created_at":157,"target_id":1696,"destination":{"map_id":97,"x":3,"y":5},"status":"active","outcome":""},"before":{"id":109,"name":"John Solaris","hour":157,"alive":true,"profession":"guarda","lod":"active","position":{"map_id":97,"x":3,"y":5},"residence":97,"hp":100,"hunger":46,"thirst":48,"fatigue":29.99999999999999,"money":38,"food":2,"water":0,"local_food":106,"local_water":144,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{}},"after":{"id":109,"name":"John Solaris","hour":157,"alive":true,"profession":"guarda","lod":"active","position":{"map_id":97,"x":3,"y":5},"residence":97,"hp":100,"hunger":46,"thirst":48,"fatigue":29.99999999999999,"money":38,"food":2,"water":0,"local_food":106,"local_water":144,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{"crime:211269":181}}}.

**Cálculos especializados reais:** [{"system":"lethal_decision","function":"lethal_decisions.LethalDecisionSystem.evaluate","result":{"available":false,"pressure":-61.3,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"pursuit","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":15.47,"directed_emotion":0.0,"commitment":0.0,"sadism":0.0,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":33.550000000000004,"moral_restraint":10.32,"fear":0.0,"risk":2.8950542822677927,"bond":0.0,"authority_or_witnesses":0.0,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{"pressure":-61.3,"cause":{"severity":0,"grave":false,"causes":[],"facts":[],"confidence":0,"mode":"retributive","confirmed_injury":0}}},{"system":"lethal_decision","function":"lethal_decisions.LethalDecisionSystem.evaluate","result":{"available":false,"pressure":-61.3,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"pursuit","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":15.47,"directed_emotion":0.0,"commitment":0.0,"sadism":0.0,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":33.550000000000004,"moral_restraint":10.32,"fear":0.0,"risk":2.8950542822677927,"bond":0.0,"authority_or_witnesses":0.0,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{"pressure":-61.3,"cause":{"severity":0,"grave":false,"causes":[],"facts":[],"confidence":0,"mode":"retributive","confirmed_injury":0}}},{"system":"lethal_pressure","function":"lethality.LethalPressure.evaluate","result":{"available":false,"pressure":-61.3,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"pursuit","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":15.47,"directed_emotion":0.0,"commitment":0.0,"sadism":0.0,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":33.550000000000004,"moral_restraint":10.32,"fear":0.0,"risk":2.8950542822677927,"bond":0.0,"authority_or_witnesses":0.0,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{}}].

| Evento/hora | Actor→target | Emissor | Testemunhas | Contexto |
| --- | --- | --- | --- | --- |
| 212155 / 157 / GuardResponded | 109→1696 | ["goals.GoalSystem._execute","goals.GoalSystem.execute","goals.GoalSystem.decide"] | [109,1696,1699,1702,1731] | {"record_id":211270,"fine":5,"source_fact":211269} |

**Aprendizado aceito durante a decisão (amostra):** [{"npc":109,"event":212155,"kind":"GuardResponded","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":1696,"event":212155,"kind":"GuardResponded","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":1699,"event":212155,"kind":"GuardResponded","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":1702,"event":212155,"kind":"GuardResponded","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":1731,"event":212155,"kind":"GuardResponded","source":null,"firsthand":true,"confidence":100,"latency":0}].

**Recibos posteriores ligados ao mesmo event_id:** [{"event":212155,"kind":"GuardResponded","learned":{"count":6,"first":157,"last":174,"first_people":[109,1696,1699,1702,1731,103]}}]. Contagem é operações de aprendizado aceitas, não indivíduos únicos.

**Consequência imediata:** {"id":109,"name":"John Solaris","hour":157,"alive":true,"profession":"guarda","lod":"active","position":{"map_id":97,"x":3,"y":5},"residence":97,"hp":100,"hunger":46,"thirst":48,"fatigue":29.99999999999999,"money":38,"food":2,"water":0,"local_food":106,"local_water":144,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{"crime:211269":181}}. **Observação/relações com o alvo ao final:** {"observation_end":{"turn":157,"position":{"map_id":97,"x":3,"y":5},"hunger":59,"thirst":44,"health":100,"alive":true,"profession":"agricultor","weapon_power":4,"injured":0},"relations_end":[]}. Não usar esse estado posterior como entrada antiga nem atribuir consequências futuras sem vínculo causal.

### 33. migration — Arthus Kars #2553, h26: buy_food

**Pressão escolhida:** `migration` #31312, prioridade 54.7, base 52, fonte `known_towns`, alvo 367. Motivo: Considerar mudança por threat.

**Contexto preservado:** {"reason":"threat"}.

**Entrada:** {"id":2553,"name":"Arthus Kars","hour":26,"alive":true,"profession":"ferreiro","lod":"local","position":{"map_id":302,"x":2,"y":5},"residence":302,"hp":100,"hunger":26,"thirst":52,"fatigue":41.20000000000001,"money":14,"food":0,"water":0,"local_food":67,"local_water":118,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{"organize":23}}.

**Personalidade:** {"honesty":28,"compassion":48,"courage":42,"independence":75,"greed":55,"diligence":78,"family_loyalty":83,"persistence":16,"temperament":75,"vengefulness":91,"ambition":9,"sadism":9}. **Emoções escalares de entrada:** {"anger":0.0,"resentment":0.0,"humiliation":0.0,"desperation":0.0,"last_updated":20,"last_support":5,"strain":0,"adaptation":0,"last_adapted":0,"stable_material_hours":0,"nested_collections":"LACUNA: cópia rasa; histórico não utilizado"}.

**Conhecimento/locais de entrada:** {"known_places":{"market":{"map_id":302,"x":7,"y":13},"home":{"map_id":302,"x":2,"y":2},"work":{"map_id":302,"x":12,"y":2},"forage":{"map_id":302,"x":1,"y":13},"well_home":{"map_id":302,"x":2,"y":2},"well_rural":{"map_id":302,"x":1,"y":13},"sacred":{"map_id":302,"x":7,"y":1}},"known_towns":[302,367],"route_knowledge_count":2,"knowledge_ids_before":[36555,36564,36565,36568,36569,36576,36577,36579,36581,36583,36592,36594,33145,38170,38171,38175,38177,38191,38192,38200,39820,39821,39823,39826,39835,39836,39860,39861,39876,41677,41679,41704,41705,41720,41727,41728,41736,41739,41741,43568,43577,43579,43586,43597,43604,45174,45180,45205,45206,45216,45234,45236,46497,46501,46514,20919,51309,51344,52804,55660,55664,33144,57359,59896],"market_observation":{}}.

**Fatos-fonte retidos após percepção:** [].

| Need | ID/alvo | Base→prioridade | Estado/fonte |
| --- | --- | --- | --- |
| political_pressure | 31313/None | 56.35→63.42291428571429 | active / own_shared_problem |
| food_reserve | 20970/None | 39.2→56.25344827586208 | active / food_reserve |
| migration | 31312/367 | 52→54.7 | active / known_towns |
| water | 41733/None | 52→53.8 | active / physiology |
| protection | 29565/2553 | 30→46.95 | active / event:29538 |
| rest | 41734/None | 41.20000000000001→43.00000000000001 | active / physiology |
| religious_interest | 20977/5909 | 33.0→38.138600000000004 | active / own_faith |

**Alternativas/gates realmente vistos:**

Need #31313 (`political_pressure`): 1 Solutions entraram em _evaluate; 1 saíram disponíveis. Entrada: `organize`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| organize | {"target":null,"destination":null} | 70.05 | {"base":0.275,"ambition":0.01125,"compassion":0.048,"persistence":0.016,"travel":-0.0} | {"feeding":null,"action_pressure":null} |

Need #31312 (`migration`): 1 Solutions entraram em _evaluate; 1 saíram disponíveis. Entrada: `buy_food`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| buy_food | {"target":null,"destination":{"map_id":302,"x":7,"y":13}} | 54.6 | {"base":0.375,"honesty":0.028000000000000004,"travel":-0.13} | {"feeding":null,"action_pressure":null} |

Need #31312 (`migration`): 1 Solutions entraram em _evaluate; 1 saíram disponíveis. Entrada: `buy_food`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| buy_food | {"target":null,"destination":{"map_id":302,"x":7,"y":13}} | 54.6 | {"base":0.375,"honesty":0.028000000000000004,"travel":-0.13} | {"feeding":null,"action_pressure":null} |

Need #29565 (`protection`): 1 Solutions entraram em _evaluate; 1 saíram disponíveis. Entrada: `avoid_threat`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| avoid_threat | {"target":null,"destination":{"map_id":302,"x":1,"y":13}} | -5.799999999999998 | {"base":0.2,"courage":-0.084,"compassion":0.036,"vengefulness":-0.091,"travel":-0.09} | {"feeding":null,"action_pressure":null} |

**Escolhas intermediárias:** [{"chosen":{"action":"organize","score":70.05,"target":null,"destination":null,"terms":{"base":0.275,"ambition":0.01125,"compassion":0.048,"persistence":0.016,"travel":-0.0},"feeding":null,"action_pressure":null},"near_scores":[70.05],"variation_draws":"não capturados; RNG não consultado pelo observador"}].

**Preparação/substituição posterior:** [].

**Winner final / Goal:** {"winner":{"action":"buy_food","score":54.6,"target":null,"destination":{"map_id":302,"x":7,"y":13},"terms":{"base":0.375,"honesty":0.028000000000000004,"travel":-0.13},"feeding":null,"action_pressure":null},"goal":{"id":46517,"need_id":31312,"action":"buy_food","score":48.6,"created_at":17,"target_id":null,"destination":{"map_id":302,"x":7,"y":13},"status":"active","outcome":""},"suspended_before":{"id":46517,"need_id":31312,"action":"buy_food","score":48.6,"created_at":17,"target_id":null,"destination":{"map_id":302,"x":7,"y":13},"status":"suspended","outcome":""},"suspended_after":null}.

**Por que outras Needs não foram executadas:** a fila prioriza emergência/priority/ID e para na primeira solucionável, sujeita à continuidade/preparo. Outras pressões retidas: political_pressure#31313(63.42291428571429), food_reserve#20970(56.25344827586208), water#41733(53.8), protection#29565(46.95), rest#41734(43.00000000000001), religious_interest#20977(38.138600000000004). Não atribuir score global entre Needs.

**Execução:** execute não foi chamado neste trace. A Goal pode ter iniciado/continuado deslocamento; o snapshot e a posição posterior delimitam essa conclusão.

**Cálculos especializados reais:** [{"system":"lethal_decision","function":"lethal_decisions.LethalDecisionSystem.evaluate","result":{"available":false,"pressure":-49.12,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"protection","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":15.47,"directed_emotion":0.0,"commitment":0.0,"sadism":1.17,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":26.400000000000002,"moral_restraint":3.36,"fear":0.0,"risk":6.0,"bond":0.0,"authority_or_witnesses":0.0,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{"pressure":-49.12,"cause":{"severity":0,"grave":false,"causes":[],"facts":[],"confidence":0,"mode":"retributive","confirmed_injury":0}}},{"system":"lethal_decision","function":"lethal_decisions.LethalDecisionSystem.evaluate","result":{"available":false,"pressure":-49.12,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"protection","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":15.47,"directed_emotion":0.0,"commitment":0.0,"sadism":1.17,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":26.400000000000002,"moral_restraint":3.36,"fear":0.0,"risk":6.0,"bond":0.0,"authority_or_witnesses":0.0,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{"pressure":-49.12,"cause":{"severity":0,"grave":false,"causes":[],"facts":[],"confidence":0,"mode":"retributive","confirmed_injury":0}}},{"system":"lethal_pressure","function":"lethality.LethalPressure.evaluate","result":{"available":false,"pressure":-49.12,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"protection","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":15.47,"directed_emotion":0.0,"commitment":0.0,"sadism":1.17,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":26.400000000000002,"moral_restraint":3.36,"fear":0.0,"risk":6.0,"bond":0.0,"authority_or_witnesses":0.0,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{}}].

| Evento/hora | Actor→target | Emissor | Testemunhas | Contexto |
| --- | --- | --- | --- | --- |
| 59932 / 26 / GroupSearchAttempt | 2553→None | ["institutions.Institutions.emit","institutions.Institutions.search_groups","institutions.Institutions.collective_candidates"] | [2493,2530,2553] | {"cause":"security","subject":null,"known":1} |

**Aprendizado aceito durante a decisão (amostra):** [{"npc":2493,"event":59932,"kind":"GroupSearchAttempt","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":2530,"event":59932,"kind":"GroupSearchAttempt","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":2553,"event":59932,"kind":"GroupSearchAttempt","source":null,"firsthand":true,"confidence":100,"latency":0}].

**Recibos posteriores ligados ao mesmo event_id:** [{"event":59932,"kind":"GroupSearchAttempt","learned":{"count":5,"first":26,"last":30,"first_people":[2493,2530,2553,2513,2544]}}]. Contagem é operações de aprendizado aceitas, não indivíduos únicos.

**Consequência imediata:** {"id":2553,"name":"Arthus Kars","hour":26,"alive":true,"profession":"ferreiro","lod":"local","position":{"map_id":302,"x":2,"y":11},"residence":302,"hp":100,"hunger":26,"thirst":52,"fatigue":41.20000000000001,"money":14,"food":0,"water":0,"local_food":67,"local_water":118,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{}}. **Observação/relações com o alvo ao final:** {"observation_end":null,"relations_end":[]}. Não usar esse estado posterior como entrada antiga nem atribuir consequências futuras sem vínculo causal.

### 34. money — Nora Douran #3313, h261: temporary_service

**Pressão escolhida:** `money` #43839, prioridade 70.626, base 56.25, fonte `economy`, alvo None. Motivo: Estabilizar renda baixa persistente.

**Contexto preservado:** {}.

**Entrada:** {"id":3313,"name":"Nora Douran","hour":261,"alive":true,"profession":"lenhador","lod":"local","position":{"map_id":508,"x":2,"y":2},"residence":508,"hp":100,"hunger":57,"thirst":27,"fatigue":10.799999999999999,"money":2,"food":1,"water":1,"local_food":72,"local_water":145,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{}}.

**Personalidade:** {"honesty":89,"compassion":40,"courage":19,"independence":70,"greed":94,"diligence":20,"family_loyalty":37,"persistence":90,"temperament":64,"vengefulness":80,"ambition":14,"sadism":0}. **Emoções escalares de entrada:** {"anger":0.0,"resentment":0.0,"humiliation":0.0,"desperation":29.24999999999998,"last_updated":258,"last_support":-10000,"strain":87.60599999999998,"adaptation":0,"last_adapted":0,"stable_material_hours":0,"nested_collections":"LACUNA: cópia rasa; histórico não utilizado"}.

**Conhecimento/locais de entrada:** {"known_places":{"market":{"map_id":508,"x":3,"y":5},"home":{"map_id":508,"x":2,"y":2},"work":{"map_id":508,"x":4,"y":2},"forage":{"map_id":508,"x":1,"y":5},"well_home":{"map_id":508,"x":2,"y":2},"well_rural":{"map_id":508,"x":1,"y":5},"sacred":{"map_id":508,"x":3,"y":1}},"known_towns":[508,479,302],"route_knowledge_count":2,"knowledge_ids_before":[241203,242326,242328,244523,244526,244528,104320,184632,248917,168919,237902,239001,204216,259970,261930,261937,263055,265158,266327,268517,268520,270819,271912,271916,271919,245842,182504,275579,275581,276876,279236,238526,251977,286932,290094,292147,252637,299008,299531,299532,301837,301839,304958,191889,306232,306233,245846,269693,269137,311938,311942,312471,312473,315586,83744,256941,275582,237904,318647,320726,321787,323780,327079,327521],"market_observation":{"turn":240,"town_id":508,"stock":{"food":87,"grain":160,"water":160,"iron":108,"wood":120},"temporary_work":true,"offers_expire_at":264,"training_offer":null,"price":2,"price_turn":216}}.

**Fatos-fonte retidos após percepção:** [{"event_id":321787,"kind":"FamilyConcern","actor_id":3313,"target_id":3310,"location":{"map_id":508,"x":2,"y":2},"turn":255,"description":"Nora Douran percebeu a privação de Arthus Douran.","confidence":100,"required_trust":0,"source_id":null,"source_kind":"direct","context":{"observed_need":60}}].

| Need | ID/alvo | Base→prioridade | Estado/fonte |
| --- | --- | --- | --- |
| money | 43839/None | 56.25→70.626 | active / economy |
| food | 15100/None | 65.5→66.85 | active / physiology |
| family | 65568/3310 | 49.2→63.570800000000006 | active / event:321787 |
| political_pressure | 104326/None | 47.35→63.13985 | active / own_shared_problem |
| migration | 113727/479 | 35→45.376 | active / known_towns |
| food_reserve | 15099/None | 37.0→38.0 | active / food_reserve |
| water | 43838/None | 27→27.0 | active / physiology |
| advancement | 15102/None | 19.578→26.227999999999998 | active / aspiration:wealth |

**Alternativas/gates realmente vistos:**

Need #43839 (`money`): 2 Solutions entraram em _evaluate; 2 saíram disponíveis. Entrada: `work_for_food, temporary_service`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| temporary_service | {"target":null,"destination":{"map_id":508,"x":3,"y":5}} | 46.0 | {"base":0.225,"diligence":0.025,"compassion":0.02,"physical_depletion":0.0,"travel":-0.04} | {"feeding":null,"action_pressure":null} |
| work_for_food | {"target":null,"destination":{"map_id":508,"x":1,"y":5}} | 42.00000000000001 | {"base":0.225,"diligence":0.025,"physical_depletion":0.0,"travel":-0.04} | {"feeding":null,"action_pressure":null} |

Need #65568 (`family`): 2 Solutions entraram em _evaluate; 2 saíram disponíveis. Entrada: `give_supplies, ask_personal_help`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| give_supplies | {"target":3310,"destination":null} | 76.4 | {"base":0.275,"compassion":0.07,"family_loyalty":0.037000000000000005,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| ask_personal_help | {"target":3310,"destination":null} | 34.800000000000004 | {"base":0.125,"independence":-0.105,"compassion":0.04,"trust":0.098,"reputation":0.0,"relationship":0.016,"travel":-0.0,"known_reputation":-0.0} | {"feeding":null,"action_pressure":null} |

Need #15102 (`advancement`): 2 Solutions entraram em _evaluate; 2 saíram disponíveis. Entrada: `work_for_food, temporary_service`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| temporary_service | {"target":null,"destination":{"map_id":508,"x":3,"y":5}} | 46.0 | {"base":0.225,"diligence":0.025,"compassion":0.02,"physical_depletion":0.0,"travel":-0.04} | {"feeding":null,"action_pressure":null} |
| work_for_food | {"target":null,"destination":{"map_id":508,"x":1,"y":5}} | 42.00000000000001 | {"base":0.225,"diligence":0.025,"physical_depletion":0.0,"travel":-0.04} | {"feeding":null,"action_pressure":null} |

**Escolhas intermediárias:** [{"chosen":{"action":"temporary_service","score":46.0,"target":null,"destination":{"map_id":508,"x":3,"y":5},"terms":{"base":0.225,"diligence":0.025,"compassion":0.02,"physical_depletion":0.0,"travel":-0.04},"feeding":null,"action_pressure":null},"near_scores":[46.0,42.00000000000001],"variation_draws":"não capturados; RNG não consultado pelo observador"}].

**Preparação/substituição posterior:** [].

**Winner final / Goal:** {"winner":{"action":"temporary_service","score":46.0,"target":null,"destination":{"map_id":508,"x":3,"y":5},"terms":{"base":0.225,"diligence":0.025,"compassion":0.02,"physical_depletion":0.0,"travel":-0.04},"feeding":null,"action_pressure":null},"goal":{"id":327522,"need_id":43839,"action":"temporary_service","score":46.0,"created_at":261,"target_id":null,"destination":{"map_id":508,"x":3,"y":5},"status":"active","outcome":""},"suspended_before":null,"suspended_after":null}.

**Por que outras Needs não foram executadas:** a fila prioriza emergência/priority/ID e para na primeira solucionável, sujeita à continuidade/preparo. Outras pressões retidas: food#15100(66.85), family#65568(63.570800000000006), political_pressure#104326(63.13985), migration#113727(45.376), food_reserve#15099(38.0), water#43838(27.0), advancement#15102(26.227999999999998). Não atribuir score global entre Needs.

**Execução:** execute não foi chamado neste trace. A Goal pode ter iniciado/continuado deslocamento; o snapshot e a posição posterior delimitam essa conclusão.

**Cálculos especializados reais:** [].

**Evento:** nenhum evento retido durante esta decisão. Isso pode significar movimento/efeito sem evento; não implica falha.

**Aprendizado aceito durante a decisão (amostra):** [].

**Recibos posteriores ligados ao mesmo event_id:** []. Contagem é operações de aprendizado aceitas, não indivíduos únicos.

**Consequência imediata:** {"id":3313,"name":"Nora Douran","hour":261,"alive":true,"profession":"lenhador","lod":"local","position":{"map_id":508,"x":2,"y":5},"residence":508,"hp":100,"hunger":57,"thirst":27,"fatigue":10.799999999999999,"money":2,"food":1,"water":1,"local_food":72,"local_water":145,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{}}. **Observação/relações com o alvo ao final:** {"observation_end":null,"relations_end":[]}. Não usar esse estado posterior como entrada antiga nem atribuir consequências futuras sem vínculo causal.

### 35. policy — Iria Luar #4926, h27: policy_work

**Pressão escolhida:** `institutional_work` #61668, prioridade 63.0, base 63, fonte `known_policy`, alvo 61662. Motivo: Cumprir trabalho financiado conhecido.

**Contexto preservado:** {}.

**Entrada:** {"id":4926,"name":"Iria Luar","hour":27,"alive":true,"profession":"guarda","lod":"active","position":{"map_id":864,"x":7,"y":13},"residence":864,"hp":100,"hunger":16,"thirst":54,"fatigue":52.40000000000004,"money":4,"food":0,"water":0,"local_food":219,"local_water":129,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{}}.

**Personalidade:** {"honesty":60,"compassion":28,"courage":84,"independence":80,"greed":11,"diligence":47,"family_loyalty":51,"persistence":77,"temperament":86,"vengefulness":32,"ambition":90,"sadism":1}. **Emoções escalares de entrada:** {"anger":0.0,"resentment":0.0,"humiliation":0.0,"desperation":0.0,"last_updated":26,"last_support":-10000,"strain":0,"adaptation":0,"last_adapted":0,"stable_material_hours":0,"nested_collections":"LACUNA: cópia rasa; histórico não utilizado"}.

**Conhecimento/locais de entrada:** {"known_places":{"market":{"map_id":864,"x":7,"y":13},"home":{"map_id":864,"x":2,"y":2},"work":{"map_id":864,"x":7,"y":13},"forage":{"map_id":864,"x":1,"y":13},"well_home":{"map_id":864,"x":2,"y":2},"well_rural":{"map_id":864,"x":1,"y":13},"sacred":{"map_id":864,"x":7,"y":1}},"known_towns":[864,911,976,1023],"route_knowledge_count":6,"knowledge_ids_before":[57889,57894,57895,57897,57899,57898,57900,57903,57904,57905,57906,59179,59181,59185,59187,59186,59188,59192,59194,59195,59196,59204,59210,59212,59214,59216,59218,59220,59227,59230,59539,59541,60482,60483,60486,60489,60490,60492,60495,60494,60493,60496,60498,60500,60501,60502,60504,60505,60506,60508,60510,60511,60520,60880,61632,61634,61639,61640,61645,61648,61658,61663,61664,61665],"market_observation":{"turn":26,"town_id":864,"stock":{"food":216,"grain":52,"water":139,"iron":68,"wood":120},"temporary_work":true,"offers_expire_at":50,"training_offer":null,"price":2,"price_turn":26}}.

**Fatos-fonte retidos após percepção:** [].

| Need | ID/alvo | Base→prioridade | Estado/fonte |
| --- | --- | --- | --- |
| institutional_work | 61668/61662 | 63→63.0 | active / known_policy |
| money | 22370/None | 43.041666666666664→56.19166666666666 | active / economy |
| rest | 27353/None | 52.40000000000004→55.70000000000004 | active / physiology |
| water | 47156/None | 54→55.5 | active / physiology |
| food_reserve | 22368/None | 37.2→45.68648648648649 | active / food_reserve |
| religious_interest | 22375/5907 | 24.25→29.7122 | active / own_faith |

**Alternativas/gates realmente vistos:**

Need #61668 (`institutional_work`): 1 Solutions entraram em _evaluate; 1 saíram disponíveis. Entrada: `policy_work`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| policy_work | {"target":61662,"destination":{"map_id":864,"x":7,"y":13}} | 96.75 | {"base":0.325,"diligence":0.05875,"financial_pressure":0.1,"travel":-0.0} | {"feeding":null,"action_pressure":null} |

**Escolhas intermediárias:** [{"chosen":{"action":"policy_work","score":96.75,"target":61662,"destination":{"map_id":864,"x":7,"y":13},"terms":{"base":0.325,"diligence":0.05875,"financial_pressure":0.1,"travel":-0.0},"feeding":null,"action_pressure":null},"near_scores":[96.75],"variation_draws":"não capturados; RNG não consultado pelo observador"}].

**Preparação/substituição posterior:** [].

**Winner final / Goal:** {"winner":{"action":"policy_work","score":96.75,"target":61662,"destination":{"map_id":864,"x":7,"y":13},"terms":{"base":0.325,"diligence":0.05875,"financial_pressure":0.1,"travel":-0.0},"feeding":null,"action_pressure":null},"goal":{"id":61669,"need_id":61668,"action":"policy_work","score":96.75,"created_at":27,"target_id":61662,"destination":{"map_id":864,"x":7,"y":13},"status":"completed","outcome":"Trabalho real e salário do orçamento reservado."},"suspended_before":null,"suspended_after":null}.

**Por que outras Needs não foram executadas:** a fila prioriza emergência/priority/ID e para na primeira solucionável, sujeita à continuidade/preparo. Outras pressões retidas: money#22370(56.19166666666666), rest#27353(55.70000000000004), water#47156(55.5), food_reserve#22368(45.68648648648649), religious_interest#22375(29.7122). Não atribuir score global entre Needs.

**Execução:** {"success":true,"result":[true,"Trabalho real e salário do orçamento reservado."],"goal_at_entry":{"id":61669,"need_id":61668,"action":"policy_work","score":96.75,"created_at":27,"target_id":61662,"destination":{"map_id":864,"x":7,"y":13},"status":"active","outcome":""},"before":{"id":4926,"name":"Iria Luar","hour":27,"alive":true,"profession":"guarda","lod":"active","position":{"map_id":864,"x":7,"y":13},"residence":864,"hp":100,"hunger":16,"thirst":54,"fatigue":52.40000000000004,"money":4,"food":0,"water":0,"local_food":219,"local_water":129,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{}},"after":{"id":4926,"name":"Iria Luar","hour":27,"alive":true,"profession":"guarda","lod":"active","position":{"map_id":864,"x":7,"y":13},"residence":864,"hp":100,"hunger":16,"thirst":54,"fatigue":54.40000000000004,"money":5,"food":0,"water":0,"local_food":219,"local_water":129,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{}}}.

**Cálculos especializados reais:** [].

| Evento/hora | Actor→target | Emissor | Testemunhas | Contexto |
| --- | --- | --- | --- | --- |
| 61670 / 27 / PolicyEffect | 4926→61662 | ["institutions.Institutions.emit","institutions.Institutions.policy_work","institutions.Institutions.execute"] | [873,885,887,1153,1156,1159,4679,4688,4691,4694,4705,4717,4740,4742,4757,4765,4774,4786,4788,4791,4794,4797,4803,4806,4809,4811,4820,4823,4826,4829,4832,4843,4855,4857,4863,4866,4875,4878,4880,4892,4895,4901,4906,4909,4912,4921,4924,4926,4935] | {"policy_id":61662,"proposal_id":57845,"sector":"SECURITY","effect":{"patrol":4926,"observed_place":{"map_id":864,"x":7,"y":13}},"materials":{},"wage":1,"remaining_budget":7,"work_done":1} |

**Aprendizado aceito durante a decisão (amostra):** [{"npc":873,"event":61670,"kind":"PolicyEffect","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":885,"event":61670,"kind":"PolicyEffect","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":887,"event":61670,"kind":"PolicyEffect","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":1153,"event":61670,"kind":"PolicyEffect","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":1156,"event":61670,"kind":"PolicyEffect","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":1159,"event":61670,"kind":"PolicyEffect","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":4679,"event":61670,"kind":"PolicyEffect","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":4688,"event":61670,"kind":"PolicyEffect","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":4691,"event":61670,"kind":"PolicyEffect","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":4694,"event":61670,"kind":"PolicyEffect","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":4705,"event":61670,"kind":"PolicyEffect","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":4717,"event":61670,"kind":"PolicyEffect","source":null,"firsthand":true,"confidence":100,"latency":0}].

**Recibos posteriores ligados ao mesmo event_id:** [{"event":61670,"kind":"PolicyEffect","learned":{"count":49,"first":27,"last":27,"first_people":[873,885,887,1153,1156,1159]}}]. Contagem é operações de aprendizado aceitas, não indivíduos únicos.

**Consequência imediata:** {"id":4926,"name":"Iria Luar","hour":27,"alive":true,"profession":"guarda","lod":"active","position":{"map_id":864,"x":7,"y":13},"residence":864,"hp":100,"hunger":16,"thirst":54,"fatigue":54.40000000000004,"money":5,"food":0,"water":0,"local_food":219,"local_water":129,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{}}. **Observação/relações com o alvo ao final:** {"observation_end":null,"relations_end":[]}. Não usar esse estado posterior como entrada antiga nem atribuir consequências futuras sem vínculo causal.

### 36. proposal — John Corven #4173, h8: serve_office

**Pressão escolhida:** `governance` #21876, prioridade 64.3958, base 60, fonte `own_office_duty`, alvo 4173. Motivo: Atender moradores na administração local.

**Contexto preservado:** {"mode":"office_hours"}.

**Entrada:** {"id":4173,"name":"John Corven","hour":8,"alive":true,"profession":"lenhador","lod":"local","position":{"map_id":695,"x":8,"y":2},"residence":695,"hp":100,"hunger":20,"thirst":16,"fatigue":15.599999999999996,"money":28,"food":0,"water":0,"local_food":102,"local_water":80,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{}}.

**Personalidade:** {"honesty":77,"compassion":31,"courage":9,"independence":23,"greed":31,"diligence":86,"family_loyalty":72,"persistence":91,"temperament":93,"vengefulness":77,"ambition":84,"sadism":0}. **Emoções escalares de entrada:** {"anger":0.0,"resentment":0.0,"humiliation":0.0,"desperation":0.0,"last_updated":2,"last_support":-10000,"strain":0,"adaptation":0,"last_adapted":0,"stable_material_hours":0,"nested_collections":"LACUNA: cópia rasa; histórico não utilizado"}.

**Conhecimento/locais de entrada:** {"known_places":{"market":{"map_id":695,"x":5,"y":9},"home":{"map_id":695,"x":2,"y":2},"work":{"map_id":695,"x":8,"y":2},"forage":{"map_id":695,"x":1,"y":9},"well_home":{"map_id":695,"x":2,"y":2},"well_rural":{"map_id":695,"x":1,"y":9},"administration":{"map_id":695,"x":5,"y":9},"sacred":{"map_id":695,"x":5,"y":1}},"known_towns":[695,601,3],"route_knowledge_count":2,"knowledge_ids_before":[5891,9785,9786,9815,9816,9839,9840,9869,9870,9899,9900,9923,9924,9953,9954,12923,12924,12925,12926,12922,12921,12920,15442,15444,15486,18805,21847,21875,21878,24017,24043,27170,27171,12898,25595,28541,28542,28544,30007,30008,30021,30022,31849,31850,31862],"market_observation":{"turn":2,"town_id":695,"stock":{"food":50,"grain":39,"water":80,"iron":26,"wood":24},"temporary_work":false,"offers_expire_at":26,"training_offer":null}}.

**Fatos-fonte retidos após percepção:** [].

| Need | ID/alvo | Base→prioridade | Estado/fonte |
| --- | --- | --- | --- |
| governance | 21876/4173 | 60→64.3958 | active / own_office_duty |
| work | 31863/None | 35→52.2 | active / profession |
| food_reserve | 21872/None | 38.0→49.443438914027155 | active / food_reserve |
| advancement | 21874/None | 15→36.9 | active / self_assessment:2 |

**Alternativas/gates realmente vistos:**

Need #21876 (`governance`): 1 Solutions entraram em _evaluate; 1 saíram disponíveis. Entrada: `serve_office`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| serve_office | {"target":4173,"destination":{"map_id":695,"x":5,"y":9}} | 35.0 | {"base":0.275,"travel":-0.1} | {"feeding":null,"action_pressure":null} |

Need #21874 (`advancement`): 1 Solutions entraram em _evaluate; 1 saíram disponíveis. Entrada: `work`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| work | {"target":null,"destination":{"map_id":695,"x":8,"y":2}} | 93.0 | {"base":0.25,"diligence":0.215,"physical_depletion":0.0,"travel":-0.0} | {"feeding":null,"action_pressure":null} |

**Escolhas intermediárias:** [{"chosen":{"action":"serve_office","score":35.0,"target":4173,"destination":{"map_id":695,"x":5,"y":9},"terms":{"base":0.275,"travel":-0.1},"feeding":null,"action_pressure":null},"near_scores":[35.0],"variation_draws":"não capturados; RNG não consultado pelo observador"}].

**Preparação/substituição posterior:** [].

**Winner final / Goal:** {"winner":{"action":"serve_office","score":35.0,"target":4173,"destination":{"map_id":695,"x":5,"y":9},"terms":{"base":0.275,"travel":-0.1},"feeding":null,"action_pressure":null},"goal":{"id":31864,"need_id":21876,"action":"serve_office","score":35.0,"created_at":8,"target_id":4173,"destination":{"map_id":695,"x":5,"y":9},"status":"active","outcome":""},"suspended_before":null,"suspended_after":null}.

**Por que outras Needs não foram executadas:** a fila prioriza emergência/priority/ID e para na primeira solucionável, sujeita à continuidade/preparo. Outras pressões retidas: work#31863(52.2), food_reserve#21872(49.443438914027155), advancement#21874(36.9). Não atribuir score global entre Needs.

**Execução:** execute não foi chamado neste trace. A Goal pode ter iniciado/continuado deslocamento; o snapshot e a posição posterior delimitam essa conclusão.

**Cálculos especializados reais:** [].

**Evento:** nenhum evento retido durante esta decisão. Isso pode significar movimento/efeito sem evento; não implica falha.

**Aprendizado aceito durante a decisão (amostra):** [].

**Recibos posteriores ligados ao mesmo event_id:** []. Contagem é operações de aprendizado aceitas, não indivíduos únicos.

**Consequência imediata:** {"id":4173,"name":"John Corven","hour":8,"alive":true,"profession":"lenhador","lod":"local","position":{"map_id":695,"x":8,"y":8},"residence":695,"hp":100,"hunger":20,"thirst":16,"fatigue":15.599999999999996,"money":28,"food":0,"water":0,"local_food":102,"local_water":80,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{}}. **Observação/relações com o alvo ao final:** {"observation_end":null,"relations_end":[]}. Não usar esse estado posterior como entrada antiga nem atribuir consequências futuras sem vínculo causal.

### 37. recovery — Arthus Arven #5511, h284: buy_food

**Pressão escolhida:** `recovery` #241629, prioridade 91.0, base 83, fonte `own_physiology`, alvo 5511. Motivo: Recuperar condição física após dano.

**Contexto preservado:** {}.

**Entrada:** {"id":5511,"name":"Arthus Arven","hour":284,"alive":true,"profession":"lenhador","lod":"active","position":{"map_id":1023,"x":2,"y":7},"residence":1023,"hp":22,"hunger":64,"thirst":28,"fatigue":85.60000000000002,"money":2,"food":0,"water":0,"local_food":5,"local_water":107,"recoverable_deprivation":78,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{}}.

**Personalidade:** {"honesty":53,"compassion":68,"courage":63,"independence":31,"greed":56,"diligence":59,"family_loyalty":74,"persistence":11,"temperament":46,"vengefulness":88,"ambition":53,"sadism":0}. **Emoções escalares de entrada:** {"anger":59.88000000000021,"resentment":59.86000000000014,"humiliation":35.19999999999982,"desperation":34.54999999999998,"last_updated":283,"last_support":80,"strain":61.654499999999864,"adaptation":0,"last_adapted":0,"stable_material_hours":0,"nested_collections":"LACUNA: cópia rasa; histórico não utilizado"}.

**Conhecimento/locais de entrada:** {"known_places":{"market":{"map_id":1023,"x":5,"y":9},"home":{"map_id":1023,"x":2,"y":2},"work":{"map_id":1023,"x":8,"y":2},"forage":{"map_id":1023,"x":1,"y":9},"well_home":{"map_id":1023,"x":2,"y":2},"well_rural":{"map_id":1023,"x":1,"y":9},"sacred":{"map_id":1023,"x":5,"y":1}},"known_towns":[1023,864],"route_knowledge_count":2,"knowledge_ids_before":[90575,310683,310687,310692,310699,310701,310704,311725,311727,311736,311742,311747,311751,312845,312846,312847,312848,312849,312850,312851,312844,312843,312842,312841,312840,312839,312838,312837,312836,312835,312853,312860,312866,312864,312869,312871,312872,312874,312877,312883,312886,324116,262397,324217,324218,324219,324220,324216,324215,324214,324213,332700,332710,333716,333720,333723,333961,335786,271260,345758,345759,345760,345762,324408],"market_observation":{"turn":268,"town_id":1023,"stock":{"food":5,"grain":14,"water":153,"iron":120,"wood":120},"temporary_work":true,"offers_expire_at":292,"training_offer":null,"price":3,"price_turn":246}}.

**Fatos-fonte retidos após percepção:** [{"event_id":312874,"kind":"ItemStolen","actor_id":5462,"target_id":1023,"location":{"map_id":1023,"x":5,"y":9},"turn":246,"description":"Elena Montes roubou comida no mercado de Elithon.","confidence":100,"required_trust":0,"source_id":null,"source_kind":"direct","context":{"item_id":312873,"item_kind":"food"}},{"event_id":262397,"kind":"WantedIssued","actor_id":5447,"target_id":1023,"location":{"map_id":1023,"x":5,"y":9},"turn":200,"description":"John Valerius registrou procura por Arthus Arven.","confidence":30,"required_trust":0,"source_id":5482,"source_kind":"rumor","context":{"record_id":262396,"suspect_id":5511,"source_fact":262395,"severity":1,"confidence":100,"last_known_location":{"map_id":1023,"x":5,"y":9}}},{"event_id":90575,"kind":"FamilyConcern","actor_id":5511,"target_id":5516,"location":{"map_id":1023,"x":5,"y":9},"turn":50,"description":"Arthus Arven percebeu a privação de Arthus Arven.","confidence":100,"required_trust":0,"source_id":null,"source_kind":"direct","context":{"observed_need":58}}].

| Need | ID/alvo | Base→prioridade | Estado/fonte |
| --- | --- | --- | --- |
| rest | 52079/None | 85.60000000000002→93.60000000000002 | active / physiology |
| recovery | 241629/5511 | 83→91.0 | active / own_physiology |
| family | 90576/5516 | 57.4→87.09241428571428 | blocked / event:90575 |
| food | 22757/None | 76.0→78.1 | active / physiology |
| money | 183981/None | 53.291666666666664→75.86766666666666 | active / economy |
| protection | 89243/5511 | 45→73.04900000000002 | active / event:312874 |
| migration | 89249/864 | 62→72.776 | active / known_towns |
| food_reserve | 22756/None | 41.0→72.70860927152317 | active / food_reserve |
| response | 262398/5447 | 55→71.94900000000003 | active / event:262397 |
| revenge | 89244/5447 | 30.0→63.18900000000002 | active / event:309646 |
| political_pressure | 89250/None | 51.24166666666666→61.267466666666664 | active / own_shared_problem |
| organizational_survival | 146123/5479 | 45.0→53.0 | active / group:49191 |
| water | 42682/None | 28→28.15 | active / physiology |

**Alternativas/gates realmente vistos:**

Need #52079 (`rest`): 1 Solutions entraram em _evaluate; 1 saíram disponíveis. Entrada: `sleep`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| sleep | {"target":null,"destination":{"map_id":1023,"x":2,"y":2}} | 90.0 | {"base":0.5,"recovery_pressure":0.0,"travel":-0.05} | {"feeding":null,"action_pressure":null} |

Need #241629 (`food`): 5 Solutions entraram em _evaluate; 5 saíram disponíveis. Entrada: `buy_food, steal, forage, work_for_food, temporary_service`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| buy_food | {"target":null,"destination":{"map_id":1023,"x":5,"y":9}} | 75.6 | {"base":0.375,"honesty":0.053000000000000005,"travel":-0.05} | {"feeding":{"EstimatedTimeUntilFoodConsumed":7,"EstimatedSurvivalMargin":28,"economically_viable":true,"survival_viable":true,"reason":null,"known_conditions":["UnknownPrice","DistantProduct"]},"action_pressure":null} |
| forage | {"target":null,"destination":{"map_id":1023,"x":1,"y":9}} | 44.49999999999999 | {"base":0.175,"independence":0.0775,"hunter":0.0,"travel":-0.03} | {"feeding":{"EstimatedTimeUntilFoodConsumed":5,"EstimatedSurvivalMargin":28,"economically_viable":true,"survival_viable":true,"reason":null,"known_conditions":["UnknownPrice","DistantProduct"]},"action_pressure":null} |
| steal | {"target":null,"destination":{"map_id":1023,"x":5,"y":9}} | 41.35329156207483 | {"base":0.35,"greed":0.09333333333333335,"honesty":-0.265,"courage":0.0315,"travel":-0.05,"pressure_moral_tolerance":0.04693312447704082} | {"feeding":{"EstimatedTimeUntilFoodConsumed":7,"EstimatedSurvivalMargin":28,"economically_viable":true,"survival_viable":true,"reason":null,"known_conditions":["UnknownPrice","DistantProduct"]},"action_pressure":null} |
| temporary_service | {"target":null,"destination":{"map_id":1023,"x":5,"y":9}} | 31.175000000000004 | {"base":0.225,"diligence":0.07375,"compassion":0.034,"physical_depletion":-0.126875,"travel":-0.05} | {"feeding":{"EstimatedTimeUntilFoodConsumed":7,"EstimatedSurvivalMargin":28,"economically_viable":true,"survival_viable":true,"reason":null,"known_conditions":["UnknownPrice","DistantProduct"]},"action_pressure":null} |
| work_for_food | {"target":null,"destination":{"map_id":1023,"x":1,"y":9}} | 28.375000000000007 | {"base":0.225,"diligence":0.07375,"physical_depletion":-0.126875,"travel":-0.03} | {"feeding":{"EstimatedTimeUntilFoodConsumed":5,"EstimatedSurvivalMargin":28,"economically_viable":true,"survival_viable":true,"reason":null,"known_conditions":["UnknownPrice","DistantProduct"]},"action_pressure":null} |

Need #90576 (`family`): 0 Solutions entraram em _evaluate; 0 saíram disponíveis. Entrada: ``.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |

Need #89243 (`protection`): 9 Solutions entraram em _evaluate; 9 saíram disponíveis. Entrada: `denounce, denounce, denounce, denounce, denounce, denounce, denounce, avoid_threat, pursue`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| pursue | {"target":5462,"destination":{"map_id":1023,"x":2,"y":2}} | 84.74326317482357 | {"base":0.275,"courage":0.063,"diligence":0.04425,"vengefulness":0.08800000000000001,"critical_depletion":0.0,"travel":-0.05,"action_pressure":0.0,"pressure_risk_tolerance":0.00346631587411783} | {"feeding":null,"action_pressure":{"eligible":true,"world_pressure":0,"action_pressure":0.0,"eligibility_causes":[],"source_facts":[],"capacity":9.45,"perceived_capacity":10.43,"major_barriers":[],"selected_alternative":"pursue"}} |
| denounce | {"target":5424,"destination":{"map_id":1023,"x":2,"y":2}} | 83.1 | {"base":0.225,"honesty":0.09275,"vengefulness":0.08800000000000001,"courage":0.04724999999999999,"trust":0.0125,"travel":-0.05} | {"feeding":null,"action_pressure":null} |
| denounce | {"target":5447,"destination":{"map_id":1023,"x":5,"y":9}} | 83.1 | {"base":0.225,"honesty":0.09275,"vengefulness":0.08800000000000001,"courage":0.04724999999999999,"trust":0.0125,"travel":-0.05} | {"feeding":null,"action_pressure":null} |
| denounce | {"target":5470,"destination":{"map_id":1023,"x":5,"y":9}} | 83.1 | {"base":0.225,"honesty":0.09275,"vengefulness":0.08800000000000001,"courage":0.04724999999999999,"trust":0.0125,"travel":-0.05} | {"feeding":null,"action_pressure":null} |
| denounce | {"target":5516,"destination":{"map_id":1023,"x":5,"y":9}} | 83.1 | {"base":0.225,"honesty":0.09275,"vengefulness":0.08800000000000001,"courage":0.04724999999999999,"trust":0.0125,"travel":-0.05} | {"feeding":null,"action_pressure":null} |
| denounce | {"target":5539,"destination":{"map_id":1023,"x":2,"y":2}} | 83.1 | {"base":0.225,"honesty":0.09275,"vengefulness":0.08800000000000001,"courage":0.04724999999999999,"trust":0.0125,"travel":-0.05} | {"feeding":null,"action_pressure":null} |
| denounce | {"target":5614,"destination":{"map_id":1023,"x":5,"y":9}} | 83.1 | {"base":0.225,"honesty":0.09275,"vengefulness":0.08800000000000001,"courage":0.04724999999999999,"trust":0.0125,"travel":-0.05} | {"feeding":null,"action_pressure":null} |
| denounce | {"target":5493,"destination":{"map_id":1023,"x":5,"y":2}} | 77.10000000000001 | {"base":0.225,"honesty":0.09275,"vengefulness":0.08800000000000001,"courage":0.04724999999999999,"trust":0.0125,"travel":-0.08} | {"feeding":null,"action_pressure":null} |
| avoid_threat | {"target":null,"destination":{"map_id":1023,"x":2,"y":2}} | -2.5999999999999996 | {"base":0.2,"courage":-0.126,"compassion":0.051000000000000004,"vengefulness":-0.08800000000000001,"travel":-0.05} | {"feeding":null,"action_pressure":null} |

Need #89244 (`revenge`): 2 Solutions entraram em _evaluate; 2 saíram disponíveis. Entrada: `investigate, avoid_threat`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| investigate | {"target":5447,"destination":{"map_id":1023,"x":5,"y":9}} | 102.50000000000001 | {"base":0.225,"vengefulness":0.17600000000000002,"courage":0.126,"independence":0.04650000000000001,"compassion":-0.034,"temperament":0.023000000000000003,"travel":-0.05} | {"feeding":null,"action_pressure":null} |
| avoid_threat | {"target":null,"destination":{"map_id":1023,"x":2,"y":2}} | -2.5999999999999996 | {"base":0.2,"courage":-0.126,"compassion":0.051000000000000004,"vengefulness":-0.08800000000000001,"travel":-0.05} | {"feeding":null,"action_pressure":null} |

**Escolhas intermediárias:** [{"chosen":{"action":"sleep","score":90.0,"target":null,"destination":{"map_id":1023,"x":2,"y":2},"terms":{"base":0.5,"recovery_pressure":0.0,"travel":-0.05},"feeding":null,"action_pressure":null},"near_scores":[90.0],"variation_draws":"não capturados; RNG não consultado pelo observador"}].

**Preparação/substituição posterior:** [].

**Winner final / Goal:** {"winner":{"action":"buy_food","score":75.6,"target":null,"destination":{"map_id":1023,"x":5,"y":9},"terms":{"base":0.375,"honesty":0.053000000000000005,"travel":-0.05},"feeding":{"EstimatedTimeUntilFoodConsumed":7,"EstimatedSurvivalMargin":28,"economically_viable":true,"survival_viable":true,"reason":null,"known_conditions":["UnknownPrice","DistantProduct"]},"action_pressure":null},"goal":{"id":345785,"need_id":241629,"action":"buy_food","score":65.60000000000001,"created_at":279,"target_id":null,"destination":{"map_id":1023,"x":5,"y":9},"status":"active","outcome":""},"suspended_before":null,"suspended_after":null}.

**Por que outras Needs não foram executadas:** a fila prioriza emergência/priority/ID e para na primeira solucionável, sujeita à continuidade/preparo. Outras pressões retidas: rest#52079(93.60000000000002), family#90576(87.09241428571428), food#22757(78.1), money#183981(75.86766666666666), protection#89243(73.04900000000002), migration#89249(72.776), food_reserve#22756(72.70860927152317), response#262398(71.94900000000003), revenge#89244(63.18900000000002), political_pressure#89250(61.267466666666664), organizational_survival#146123(53.0), water#42682(28.15). Não atribuir score global entre Needs.

**Execução:** execute não foi chamado neste trace. A Goal pode ter iniciado/continuado deslocamento; o snapshot e a posição posterior delimitam essa conclusão.

**Cálculos especializados reais:** [{"system":"lethal_decision","function":"lethal_decisions.LethalDecisionSystem.evaluate","result":{"available":false,"pressure":-85.79,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"protection","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":14.96,"directed_emotion":0.0,"commitment":0.0,"sadism":0.0,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":37.400000000000006,"moral_restraint":6.359999999999999,"fear":19.531967213114754,"risk":7.453416149068323,"bond":0.0,"authority_or_witnesses":0.0,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{"pressure":-85.79,"cause":{"severity":0,"grave":false,"causes":[],"facts":[],"confidence":0,"mode":"retributive","confirmed_injury":0}}},{"system":"lethal_decision","function":"lethal_decisions.LethalDecisionSystem.evaluate","result":{"available":false,"pressure":-85.79,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"protection","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":14.96,"directed_emotion":0.0,"commitment":0.0,"sadism":0.0,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":37.400000000000006,"moral_restraint":6.359999999999999,"fear":19.531967213114754,"risk":7.453416149068323,"bond":0.0,"authority_or_witnesses":0.0,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{"pressure":-85.79,"cause":{"severity":0,"grave":false,"causes":[],"facts":[],"confidence":0,"mode":"retributive","confirmed_injury":0}}},{"system":"lethal_pressure","function":"lethality.LethalPressure.evaluate","result":{"available":false,"pressure":-85.79,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"protection","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":14.96,"directed_emotion":0.0,"commitment":0.0,"sadism":0.0,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":37.400000000000006,"moral_restraint":6.359999999999999,"fear":19.531967213114754,"risk":7.453416149068323,"bond":0.0,"authority_or_witnesses":0.0,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{}},{"system":"lethal_decision","function":"lethal_decisions.LethalDecisionSystem.evaluate","result":{"available":false,"pressure":-94.89,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"revenge","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":14.96,"directed_emotion":3.729000000000013,"commitment":0.0,"sadism":0.0,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":37.400000000000006,"moral_restraint":6.359999999999999,"fear":30.55,"risk":9.273743016759777,"bond":0.0,"authority_or_witnesses":0.0,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{"pressure":-94.89,"cause":{"severity":0,"grave":false,"causes":[],"facts":[],"confidence":0,"mode":"retributive","confirmed_injury":0}}},{"system":"lethal_decision","function":"lethal_decisions.LethalDecisionSystem.evaluate","result":{"available":false,"pressure":-94.89,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"revenge","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":14.96,"directed_emotion":3.729000000000013,"commitment":0.0,"sadism":0.0,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":37.400000000000006,"moral_restraint":6.359999999999999,"fear":30.55,"risk":9.273743016759777,"bond":0.0,"authority_or_witnesses":0.0,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{"pressure":-94.89,"cause":{"severity":0,"grave":false,"causes":[],"facts":[],"confidence":0,"mode":"retributive","confirmed_injury":0}}},{"system":"lethal_pressure","function":"lethality.LethalPressure.evaluate","result":{"available":false,"pressure":-94.89,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"revenge","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":14.96,"directed_emotion":3.729000000000013,"commitment":0.0,"sadism":0.0,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":37.400000000000006,"moral_restraint":6.359999999999999,"fear":30.55,"risk":9.273743016759777,"bond":0.0,"authority_or_witnesses":0.0,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{}},{"system":"lethal_decision","function":"lethal_decisions.LethalDecisionSystem.evaluate","result":{"available":false,"pressure":-94.89,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"response","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":14.96,"directed_emotion":3.729000000000013,"commitment":0.0,"sadism":0.0,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":37.400000000000006,"moral_restraint":6.359999999999999,"fear":30.55,"risk":9.273743016759777,"bond":0.0,"authority_or_witnesses":0.0,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{"pressure":-94.89,"cause":{"severity":0,"grave":false,"causes":[],"facts":[],"confidence":0,"mode":"retributive","confirmed_injury":0}}},{"system":"lethal_decision","function":"lethal_decisions.LethalDecisionSystem.evaluate","result":{"available":false,"pressure":-94.89,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"response","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":14.96,"directed_emotion":3.729000000000013,"commitment":0.0,"sadism":0.0,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":37.400000000000006,"moral_restraint":6.359999999999999,"fear":30.55,"risk":9.273743016759777,"bond":0.0,"authority_or_witnesses":0.0,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{"pressure":-94.89,"cause":{"severity":0,"grave":false,"causes":[],"facts":[],"confidence":0,"mode":"retributive","confirmed_injury":0}}},{"system":"lethal_pressure","function":"lethality.LethalPressure.evaluate","result":{"available":false,"pressure":-94.89,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"response","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":14.96,"directed_emotion":3.729000000000013,"commitment":0.0,"sadism":0.0,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":37.400000000000006,"moral_restraint":6.359999999999999,"fear":30.55,"risk":9.273743016759777,"bond":0.0,"authority_or_witnesses":0.0,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{}},{"system":"capacity","function":"action_pressure.ActionPressureSystem.assess","result":{"eligible":true,"world_pressure":0,"action_pressure":0.0,"eligibility_causes":[],"source_facts":[],"capacity":9.45,"perceived_capacity":10.43,"major_barriers":[],"selected_alternative":"pursue"},"inputs":{}}].

**Evento:** nenhum evento retido durante esta decisão. Isso pode significar movimento/efeito sem evento; não implica falha.

**Aprendizado aceito durante a decisão (amostra):** [].

**Recibos posteriores ligados ao mesmo event_id:** []. Contagem é operações de aprendizado aceitas, não indivíduos únicos.

**Consequência imediata:** {"id":5511,"name":"Arthus Arven","hour":284,"alive":true,"profession":"lenhador","lod":"active","position":{"map_id":1023,"x":2,"y":8},"residence":1023,"hp":22,"hunger":64,"thirst":28,"fatigue":85.60000000000002,"money":2,"food":0,"water":0,"local_food":5,"local_water":107,"recoverable_deprivation":78,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{}}. **Observação/relações com o alvo ao final:** {"observation_end":null,"relations_end":[]}. Não usar esse estado posterior como entrada antiga nem atribuir consequências futuras sem vínculo causal.

### 38. religion — Aldren Bruma #2887, h6: buy_food

**Pressão escolhida:** `divine_contact` #14896, prioridade 48.05, base 47.15, fonte `personal_faith`, alvo 5909. Motivo: Buscar contato por devoção, ambição ou perda.

**Contexto preservado:** {"source_fact":null}.

**Entrada:** {"id":2887,"name":"Aldren Bruma","hour":6,"alive":true,"profession":"ferreiro","lod":"background","position":{"map_id":396,"x":2,"y":2},"residence":396,"hp":100,"hunger":15,"thirst":12,"fatigue":8.200000000000001,"money":21,"food":1,"water":0,"local_food":46,"local_water":80,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{}}.

**Personalidade:** {"honesty":61,"compassion":30,"courage":9,"independence":75,"greed":53,"diligence":26,"family_loyalty":47,"persistence":68,"temperament":5,"vengefulness":91,"ambition":65,"sadism":28}. **Emoções escalares de entrada:** {"anger":0.0,"resentment":0.0,"humiliation":0.0,"desperation":0.0,"last_updated":3,"last_support":-10000,"strain":0,"adaptation":0,"last_adapted":0,"stable_material_hours":0,"nested_collections":"LACUNA: cópia rasa; histórico não utilizado"}.

**Conhecimento/locais de entrada:** {"known_places":{"market":{"map_id":396,"x":3,"y":5},"home":{"map_id":396,"x":2,"y":2},"work":{"map_id":396,"x":4,"y":2},"forage":{"map_id":396,"x":1,"y":5},"well_home":{"map_id":396,"x":2,"y":2},"well_rural":{"map_id":396,"x":1,"y":5},"sacred":{"map_id":396,"x":3,"y":1}},"known_towns":[396,367,302],"route_knowledge_count":2,"knowledge_ids_before":[8561,8562,8563,8564,8567,8568,8569,8570,8573,8574,8575,8576,8579,8580,8581,8582,8585,8586,12522,12523,12524,12525,12526,12527,12528,12529,12521,14891,14894,14897,14898,14900,14913,14918,21171,21182,23704,23709,21161],"market_observation":{}}.

**Fatos-fonte retidos após percepção:** [].

| Need | ID/alvo | Base→prioridade | Estado/fonte |
| --- | --- | --- | --- |
| divine_contact | 14896/5909 | 47.15→48.05 | active / personal_faith |
| advancement | 14893/None | 24.1158→43.20185622857143 | active / self_assessment:0 |
| religious_interest | 14895/5909 | 32.25→35.4082 | active / own_faith |
| food_reserve | 28257/None | 33.0→33.0 | active / food_reserve |

**Alternativas/gates realmente vistos:**

Need #14896 (`divine_contact`): 1 Solutions entraram em _evaluate; 1 saíram disponíveis. Entrada: `buy_food`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| buy_food | {"target":null,"destination":{"map_id":396,"x":3,"y":5}} | 79.2 | {"base":0.375,"honesty":0.061,"travel":-0.04} | {"feeding":null,"action_pressure":null} |

Need #14893 (`advancement`): 1 Solutions entraram em _evaluate; 1 saíram disponíveis. Entrada: `work`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| work | {"target":null,"destination":{"map_id":396,"x":4,"y":2}} | 59.0 | {"base":0.25,"diligence":0.065,"physical_depletion":0.0,"travel":-0.02} | {"feeding":null,"action_pressure":null} |

**Escolhas intermediárias:** [{"chosen":{"action":"buy_food","score":79.2,"target":null,"destination":{"map_id":396,"x":3,"y":5},"terms":{"base":0.375,"honesty":0.061,"travel":-0.04},"feeding":null,"action_pressure":null},"near_scores":[79.2],"variation_draws":"não capturados; RNG não consultado pelo observador"}].

**Preparação/substituição posterior:** [].

**Winner final / Goal:** {"winner":{"action":"buy_food","score":79.2,"target":null,"destination":{"map_id":396,"x":3,"y":5},"terms":{"base":0.375,"honesty":0.061,"travel":-0.04},"feeding":null,"action_pressure":null},"goal":{"id":28258,"need_id":14896,"action":"buy_food","score":79.2,"created_at":6,"target_id":null,"destination":{"map_id":396,"x":3,"y":5},"status":"active","outcome":""},"suspended_before":null,"suspended_after":null}.

**Por que outras Needs não foram executadas:** a fila prioriza emergência/priority/ID e para na primeira solucionável, sujeita à continuidade/preparo. Outras pressões retidas: advancement#14893(43.20185622857143), religious_interest#14895(35.4082), food_reserve#28257(33.0). Não atribuir score global entre Needs.

**Execução:** execute não foi chamado neste trace. A Goal pode ter iniciado/continuado deslocamento; o snapshot e a posição posterior delimitam essa conclusão.

**Cálculos especializados reais:** [].

**Evento:** nenhum evento retido durante esta decisão. Isso pode significar movimento/efeito sem evento; não implica falha.

**Aprendizado aceito durante a decisão (amostra):** [].

**Recibos posteriores ligados ao mesmo event_id:** []. Contagem é operações de aprendizado aceitas, não indivíduos únicos.

**Consequência imediata:** {"id":2887,"name":"Aldren Bruma","hour":6,"alive":true,"profession":"ferreiro","lod":"background","position":{"map_id":396,"x":2,"y":5},"residence":396,"hp":100,"hunger":15,"thirst":12,"fatigue":8.200000000000001,"money":21,"food":1,"water":0,"local_food":46,"local_water":80,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{}}. **Observação/relações com o alvo ao final:** {"observation_end":null,"relations_end":[]}. Não usar esse estado posterior como entrada antiga nem atribuir consequências futuras sem vínculo causal.

### 39. rest — Elena Douran #5637, h68: sleep

**Pressão escolhida:** `rest` #60666, prioridade 87.9000000000001, base 81.60000000000011, fonte `physiology`, alvo None. Motivo: Cansaço.

**Contexto preservado:** {}.

**Entrada:** {"id":5637,"name":"Elena Douran","hour":68,"alive":true,"profession":"agricultor","lod":"local","position":{"map_id":1088,"x":5,"y":9},"residence":1088,"hp":100,"hunger":35,"thirst":46,"fatigue":81.60000000000011,"money":53,"food":1,"water":0,"local_food":87,"local_water":77,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{}}.

**Personalidade:** {"honesty":51,"compassion":73,"courage":51,"independence":24,"greed":83,"diligence":17,"family_loyalty":32,"persistence":90,"temperament":53,"vengefulness":44,"ambition":92,"sadism":0}. **Emoções escalares de entrada:** {"anger":0.0,"resentment":0.0,"humiliation":0.0,"desperation":0.0,"last_updated":62,"last_support":-10000,"strain":0,"adaptation":0,"last_adapted":0,"stable_material_hours":0,"nested_collections":"LACUNA: cópia rasa; histórico não utilizado"}.

**Conhecimento/locais de entrada:** {"known_places":{"market":{"map_id":1088,"x":5,"y":9},"home":{"map_id":1088,"x":2,"y":2},"work":{"map_id":1088,"x":1,"y":9},"forage":{"map_id":1088,"x":1,"y":9},"well_home":{"map_id":1088,"x":2,"y":2},"well_rural":{"map_id":1088,"x":1,"y":9},"sacred":{"map_id":1088,"x":5,"y":1}},"known_towns":[1088,864],"route_knowledge_count":2,"knowledge_ids_before":[101105,101110,101116,101118,101120,101119,101418,101419,102176,102183,102185,102193,103054,103057,103061,103064,103857,103862,103864,103867,104004,104006,104641,104645,104647,104672,104670,104787,104788,104789,104790,104792,105456,105473,105475,105491,105494,105625,106339,106349,106357,106355,106654,107517,107518,107521,107522,107523,107525,107531,107664,107662,107670,108452,108473,108470,108481,108485,108487,108611,108612,108613,108614,108616],"market_observation":{"turn":62,"town_id":1088,"stock":{"food":100,"grain":122,"water":80,"iron":120,"wood":74},"temporary_work":true,"offers_expire_at":86,"training_offer":null,"price":2,"price_turn":62}}.

**Fatos-fonte retidos após percepção:** [{"event_id":108470,"kind":"ItemStolen","actor_id":5735,"target_id":1088,"location":{"map_id":1088,"x":5,"y":9},"turn":67,"description":"Elena Bruma roubou comida no mercado de Arria.","confidence":100,"required_trust":0,"source_id":null,"source_kind":"direct","context":{"item_id":108469,"item_kind":"food"}}].

| Need | ID/alvo | Base→prioridade | Estado/fonte |
| --- | --- | --- | --- |
| rest | 60666/None | 81.60000000000011→87.9000000000001 | active / physiology |
| political_pressure | 98142/None | 68.8→74.56899999999999 | active / own_shared_problem |
| family | 94497/5643 | 58.3→70.55122857142857 | blocked / event:94496 |
| family | 94495/5640 | 51.099999999999994→65.62359999999998 | active / event:94494 |
| organizational_survival | 101071/5686 | 52.5285→57.832100000000004 | active / group:53614 |
| protection | 95995/5637 | 45→55.2 | active / event:108470 |
| migration | 98141/864 | 52→53.8 | active / known_towns |
| water | 42706/None | 46→50.95 | active / physiology |
| recognition | 22818/1088 | 40.400000000000006→48.400000000000006 | active / political_aspiration |
| food_reserve | 52110/None | 37.0→41.0 | active / food_reserve |
| food | 32310/None | 20→20.0 | active / physiology |

**Alternativas/gates realmente vistos:**

Need #60666 (`rest`): 1 Solutions entraram em _evaluate; 1 saíram disponíveis. Entrada: `sleep`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| sleep | {"target":null,"destination":{"map_id":1088,"x":2,"y":2}} | 80.0 | {"base":0.5,"recovery_pressure":0.0,"travel":-0.1} | {"feeding":null,"action_pressure":null} |

Need #94497 (`family`): 1 Solutions entraram em _evaluate; 1 saíram disponíveis. Entrada: `check_relative`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| check_relative | {"target":5643,"destination":{"map_id":1088,"x":5,"y":9}} | 69.0 | {"base":0.275,"independence":0.03,"family_loyalty":0.04,"travel":-0.0} | {"feeding":null,"action_pressure":null} |

Need #94495 (`family`): 1 Solutions entraram em _evaluate; 1 saíram disponíveis. Entrada: `check_relative`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| check_relative | {"target":5640,"destination":{"map_id":1088,"x":5,"y":9}} | 69.0 | {"base":0.275,"independence":0.03,"family_loyalty":0.04,"travel":-0.0} | {"feeding":null,"action_pressure":null} |

Need #95995 (`protection`): 20 Solutions entraram em _evaluate; 20 saíram disponíveis. Entrada: `denounce, denounce, denounce, denounce, denounce, denounce, avoid_threat, confront, threaten, demand_return, warn, insult, call_help, calm, withdraw, flee, defend, forgive, apologize, surrender`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| denounce | {"target":1111,"destination":{"map_id":1088,"x":5,"y":9}} | 81.80000000000001 | {"base":0.225,"honesty":0.08925000000000001,"vengefulness":0.044000000000000004,"courage":0.03825,"trust":0.0125,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| denounce | {"target":5654,"destination":{"map_id":1088,"x":5,"y":9}} | 81.80000000000001 | {"base":0.225,"honesty":0.08925000000000001,"vengefulness":0.044000000000000004,"courage":0.03825,"trust":0.0125,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| denounce | {"target":5677,"destination":{"map_id":1088,"x":5,"y":9}} | 81.80000000000001 | {"base":0.225,"honesty":0.08925000000000001,"vengefulness":0.044000000000000004,"courage":0.03825,"trust":0.0125,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| denounce | {"target":5700,"destination":{"map_id":1088,"x":5,"y":9}} | 81.80000000000001 | {"base":0.225,"honesty":0.08925000000000001,"vengefulness":0.044000000000000004,"courage":0.03825,"trust":0.0125,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| denounce | {"target":5723,"destination":{"map_id":1088,"x":5,"y":9}} | 81.80000000000001 | {"base":0.225,"honesty":0.08925000000000001,"vengefulness":0.044000000000000004,"courage":0.03825,"trust":0.0125,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| denounce | {"target":5769,"destination":{"map_id":1088,"x":5,"y":9}} | 81.80000000000001 | {"base":0.225,"honesty":0.08925000000000001,"vengefulness":0.044000000000000004,"courage":0.03825,"trust":0.0125,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| demand_return | {"target":5735,"destination":null} | 78.4 | {"base":0.2,"honesty":0.06375,"persistence":0.09,"courage":0.03825,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| surrender | {"target":5735,"destination":null} | 64.75 | {"base":0.125,"authority":0.2,"risk":0.0625,"low_health":0.0,"courage":-0.06375,"defensive":-0.0,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| defend | {"target":5735,"destination":null} | 60.150000000000006 | {"base":0.2,"risk":0.0625,"courage":0.03825,"defensive":0.0,"injury":-0.0,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| calm | {"target":5735,"destination":null} | 56.89999999999999 | {"base":0.175,"compassion":0.10949999999999999,"bond":0.0,"anger":-0.0,"travel":-0.0} | {"feeding":null,"action_pressure":null} |

**Escolhas intermediárias:** [{"chosen":{"action":"sleep","score":80.0,"target":null,"destination":{"map_id":1088,"x":2,"y":2},"terms":{"base":0.5,"recovery_pressure":0.0,"travel":-0.1},"feeding":null,"action_pressure":null},"near_scores":[80.0],"variation_draws":"não capturados; RNG não consultado pelo observador"}].

**Preparação/substituição posterior:** [].

**Winner final / Goal:** {"winner":{"action":"sleep","score":80.0,"target":null,"destination":{"map_id":1088,"x":2,"y":2},"terms":{"base":0.5,"recovery_pressure":0.0,"travel":-0.1},"feeding":null,"action_pressure":null},"goal":{"id":109413,"need_id":60666,"action":"sleep","score":80.0,"created_at":68,"target_id":null,"destination":{"map_id":1088,"x":2,"y":2},"status":"active","outcome":""},"suspended_before":null,"suspended_after":null}.

**Por que outras Needs não foram executadas:** a fila prioriza emergência/priority/ID e para na primeira solucionável, sujeita à continuidade/preparo. Outras pressões retidas: political_pressure#98142(74.56899999999999), family#94497(70.55122857142857), family#94495(65.62359999999998), organizational_survival#101071(57.832100000000004), protection#95995(55.2), migration#98141(53.8), water#42706(50.95), recognition#22818(48.400000000000006), food_reserve#52110(41.0), food#32310(20.0). Não atribuir score global entre Needs.

**Execução:** execute não foi chamado neste trace. A Goal pode ter iniciado/continuado deslocamento; o snapshot e a posição posterior delimitam essa conclusão.

**Cálculos especializados reais:** [{"system":"lethal_decision","function":"lethal_decisions.LethalDecisionSystem.evaluate","result":{"available":false,"pressure":-89.79,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"protection","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":7.48,"directed_emotion":0.0,"commitment":0.0,"sadism":0.0,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":40.150000000000006,"moral_restraint":6.12,"fear":0.0,"risk":6.0,"bond":0.0,"authority_or_witnesses":15,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{"pressure":-89.79,"cause":{"severity":0,"grave":false,"causes":[],"facts":[],"confidence":0,"mode":"retributive","confirmed_injury":0}}},{"system":"lethal_decision","function":"lethal_decisions.LethalDecisionSystem.evaluate","result":{"available":false,"pressure":-89.79,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"protection","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":7.48,"directed_emotion":0.0,"commitment":0.0,"sadism":0.0,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":40.150000000000006,"moral_restraint":6.12,"fear":0.0,"risk":6.0,"bond":0.0,"authority_or_witnesses":15,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{"pressure":-89.79,"cause":{"severity":0,"grave":false,"causes":[],"facts":[],"confidence":0,"mode":"retributive","confirmed_injury":0}}},{"system":"lethal_pressure","function":"lethality.LethalPressure.evaluate","result":{"available":false,"pressure":-89.79,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"protection","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":7.48,"directed_emotion":0.0,"commitment":0.0,"sadism":0.0,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":40.150000000000006,"moral_restraint":6.12,"fear":0.0,"risk":6.0,"bond":0.0,"authority_or_witnesses":15,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{}}].

**Evento:** nenhum evento retido durante esta decisão. Isso pode significar movimento/efeito sem evento; não implica falha.

**Aprendizado aceito durante a decisão (amostra):** [].

**Recibos posteriores ligados ao mesmo event_id:** []. Contagem é operações de aprendizado aceitas, não indivíduos únicos.

**Consequência imediata:** {"id":5637,"name":"Elena Douran","hour":68,"alive":true,"profession":"agricultor","lod":"local","position":{"map_id":1088,"x":5,"y":3},"residence":1088,"hp":100,"hunger":35,"thirst":46,"fatigue":81.60000000000011,"money":53,"food":1,"water":0,"local_food":87,"local_water":77,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{}}. **Observação/relações com o alvo ao final:** {"observation_end":null,"relations_end":[]}. Não usar esse estado posterior como entrada antiga nem atribuir consequências futuras sem vínculo causal.

### 40. social — Aldren Valerius #3456, h86: work

**Pressão escolhida:** `status` #21436, prioridade 65.96393408, base 28.0038, fonte `aspiration:recognition`, alvo None. Motivo: Melhorar condição pessoal por oportunidade conhecida.

**Contexto preservado:** {"diagnostic":{"reason":"Selected","competing":null,"turn":86}}.

**Entrada:** {"id":3456,"name":"Aldren Valerius","hour":86,"alive":true,"profession":"ferreiro","lod":"local","position":{"map_id":544,"x":5,"y":2},"residence":544,"hp":100,"hunger":56,"thirst":37,"fatigue":48.20000000000016,"money":21,"food":0,"water":0,"local_food":149,"local_water":116,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{}}.

**Personalidade:** {"honesty":52,"compassion":36,"courage":44,"independence":88,"greed":67,"diligence":50,"family_loyalty":64,"persistence":21,"temperament":76,"vengefulness":44,"ambition":95,"sadism":0}. **Emoções escalares de entrada:** {"anger":0.0,"resentment":0.0,"humiliation":0.0,"desperation":0.0,"last_updated":83,"last_support":53,"strain":0,"adaptation":0,"last_adapted":0,"stable_material_hours":0,"nested_collections":"LACUNA: cópia rasa; histórico não utilizado"}.

**Conhecimento/locais de entrada:** {"known_places":{"market":{"map_id":544,"x":5,"y":9},"home":{"map_id":544,"x":2,"y":2},"work":{"map_id":544,"x":8,"y":2},"forage":{"map_id":544,"x":1,"y":9},"well_home":{"map_id":544,"x":2,"y":2},"well_rural":{"map_id":544,"x":1,"y":9},"sacred":{"map_id":544,"x":5,"y":1}},"known_towns":[544,302],"route_knowledge_count":2,"knowledge_ids_before":[93316,93948,93957,93961,93966,93981,80232,94847,95455,96577,96581,96594,97657,97661,97662,97660,97664,97683,97686,98311,98797,98802,98806,98811,99769,99781,100713,100715,100723,100725,100729,101367,101806,101807,101808,101810,101816,102686,102690,103490,103503,103506,103953,104352,104355,104358,105131,105134,105995,106000,46779,119419,119421,119404,116170,120473,120489,121436,122386,122398,122413,123492,125365,106013],"market_observation":{"turn":65,"town_id":544,"stock":{"food":187,"grain":111,"water":82,"iron":74,"wood":82},"temporary_work":false,"offers_expire_at":89,"training_offer":null,"price":2,"price_turn":65}}.

**Fatos-fonte retidos após percepção:** [].

| Need | ID/alvo | Base→prioridade | Estado/fonte |
| --- | --- | --- | --- |
| food_reserve | 21432/None | 41.0→71.65714285714286 | active / food_reserve |
| status | 21436/None | 28.0038→65.96393408 | selected / aspiration:recognition |
| food | 21433/None | 64.0→65.35 | active / physiology |
| organizational_survival | 75322/3522 | 49.267→59.6814 | active / group:55922 |
| rest | 46793/None | 48.20000000000016→56.20000000000016 | active / physiology |
| recognition | 21439/544 | 41.0→49.2124 | active / political_aspiration |
| advancement | 21434/None | 15→46.75 | active / self_assessment:2 |
| work | 36800/None | 35→45.9 | active / profession |
| water | 46792/None | 37→45 | active / physiology |

**Alternativas/gates realmente vistos:**

Need #21432 (`food_reserve`): 3 Solutions entraram em _evaluate; 3 saíram disponíveis. Entrada: `buy_food, steal, forage`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| buy_food | {"target":null,"destination":{"map_id":544,"x":5,"y":9}} | 71.39999999999999 | {"base":0.375,"honesty":0.052000000000000005,"travel":-0.07} | {"feeding":{"EstimatedTimeUntilFoodConsumed":11,"EstimatedSurvivalMargin":55,"economically_viable":true,"survival_viable":true,"reason":null,"known_conditions":["DistantProduct"]},"action_pressure":null} |
| forage | {"target":null,"destination":{"map_id":544,"x":1,"y":9}} | 56.99999999999999 | {"base":0.175,"independence":0.22,"hunter":0.0,"travel":-0.11} | {"feeding":{"EstimatedTimeUntilFoodConsumed":15,"EstimatedSurvivalMargin":55,"economically_viable":true,"survival_viable":true,"reason":null,"known_conditions":["DistantProduct"]},"action_pressure":null} |
| steal | {"target":null,"destination":{"map_id":544,"x":5,"y":9}} | 33.09676729251701 | {"base":0.35,"greed":0.11166666666666668,"honesty":-0.26,"courage":0.022000000000000002,"travel":-0.07,"pressure_moral_tolerance":0.01181716979591837} | {"feeding":{"EstimatedTimeUntilFoodConsumed":11,"EstimatedSurvivalMargin":55,"economically_viable":true,"survival_viable":true,"reason":null,"known_conditions":["DistantProduct"]},"action_pressure":null} |

Need #21436 (`status`): 1 Solutions entraram em _evaluate; 1 saíram disponíveis. Entrada: `work`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| work | {"target":null,"destination":{"map_id":544,"x":8,"y":2}} | -3.0 | {"base":0.25,"diligence":0.125,"physical_depletion":0.0,"travel":-0.03,"no_progress":-0.36} | {"feeding":null,"action_pressure":null} |

Need #21434 (`advancement`): 2 Solutions entraram em _evaluate; 2 saíram disponíveis. Entrada: `work, steal_person`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| work | {"target":null,"destination":{"map_id":544,"x":8,"y":2}} | 69.0 | {"base":0.25,"diligence":0.125,"physical_depletion":0.0,"travel":-0.03} | {"feeding":null,"action_pressure":null} |
| steal_person | {"target":3442,"destination":null} | 32.298438 | {"base":0.31,"greed":0.134,"honesty":-0.234,"authority":-0.1,"courage":0.022000000000000002,"travel":-0.0,"pressure_moral_tolerance":0.029492189999999998} | {"feeding":null,"action_pressure":null} |

**Escolhas intermediárias:** [{"chosen":{"action":"buy_food","score":71.39999999999999,"target":null,"destination":{"map_id":544,"x":5,"y":9},"terms":{"base":0.375,"honesty":0.052000000000000005,"travel":-0.07},"feeding":{"EstimatedTimeUntilFoodConsumed":11,"EstimatedSurvivalMargin":55,"economically_viable":true,"survival_viable":true,"reason":null,"known_conditions":["DistantProduct"]},"action_pressure":null},"near_scores":[71.39999999999999,56.99999999999999,33.09676729251701],"variation_draws":"não capturados; RNG não consultado pelo observador"}].

**Preparação/substituição posterior:** [].

**Winner final / Goal:** {"winner":{"action":"work","score":-3.0,"target":null,"destination":{"map_id":544,"x":8,"y":2},"terms":{"base":0.25,"diligence":0.125,"physical_depletion":0.0,"travel":-0.03,"no_progress":-0.36},"feeding":null,"action_pressure":null},"goal":{"id":125366,"need_id":21436,"action":"work","score":9.0,"created_at":83,"target_id":null,"destination":{"map_id":544,"x":8,"y":2},"status":"active","outcome":""},"suspended_before":null,"suspended_after":null}.

**Por que outras Needs não foram executadas:** a fila prioriza emergência/priority/ID e para na primeira solucionável, sujeita à continuidade/preparo. Outras pressões retidas: food_reserve#21432(71.65714285714286), food#21433(65.35), organizational_survival#75322(59.6814), rest#46793(56.20000000000016), recognition#21439(49.2124), advancement#21434(46.75), work#36800(45.9), water#46792(45). Não atribuir score global entre Needs.

**Execução:** execute não foi chamado neste trace. A Goal pode ter iniciado/continuado deslocamento; o snapshot e a posição posterior delimitam essa conclusão.

**Cálculos especializados reais:** [].

**Evento:** nenhum evento retido durante esta decisão. Isso pode significar movimento/efeito sem evento; não implica falha.

**Aprendizado aceito durante a decisão (amostra):** [].

**Recibos posteriores ligados ao mesmo event_id:** []. Contagem é operações de aprendizado aceitas, não indivíduos únicos.

**Consequência imediata:** {"id":3456,"name":"Aldren Valerius","hour":86,"alive":true,"profession":"ferreiro","lod":"local","position":{"map_id":544,"x":8,"y":2},"residence":544,"hp":100,"hunger":56,"thirst":37,"fatigue":48.20000000000016,"money":21,"food":0,"water":0,"local_food":149,"local_water":116,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{}}. **Observação/relações com o alvo ao final:** {"observation_end":null,"relations_end":[]}. Não usar esse estado posterior como entrada antiga nem atribuir consequências futuras sem vínculo causal.

### 41. travel — Nora Arven #3376, h22: route_travel

**Pressão escolhida:** `spatial_journey` #54487, prioridade 58.0, base 58, fonte `journey`, alvo 479. Motivo: Prosseguir viagem já iniciada.

**Contexto preservado:** {}.

**Entrada:** {"id":3376,"name":"Nora Arven","hour":22,"alive":true,"profession":"lenhador","lod":"active","position":{"map_id":526,"x":3,"y":6},"residence":526,"hp":100,"hunger":31,"thirst":44,"fatigue":37.4,"money":15,"food":2,"water":2,"local_food":123,"local_water":70,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":{"origin":526,"destination":479,"route_ids":[5932],"nodes":[526,479],"reason":"divine_contact","started_at":21,"mode":"known_route","guide_id":null,"leg":0,"offset":0,"last_step":21,"entering":false,"known_at_start":[{"actor":3376,"origin":526,"destination":479,"route_id":5932,"confidence":100,"source":"initial_local_life","learned_at":0,"last_used_at":-1,"source_id":null,"travel_time":4,"danger":4,"condition":"open"}]},"failures":{}}.

**Personalidade:** {"honesty":90,"compassion":17,"courage":27,"independence":76,"greed":76,"diligence":19,"family_loyalty":58,"persistence":67,"temperament":77,"vengefulness":58,"ambition":65,"sadism":0}. **Emoções escalares de entrada:** {"anger":0.0,"resentment":0.0,"humiliation":0.0,"desperation":0.0,"last_updated":21,"last_support":-10000,"strain":0,"adaptation":0,"last_adapted":0,"stable_material_hours":0,"nested_collections":"LACUNA: cópia rasa; histórico não utilizado"}.

**Conhecimento/locais de entrada:** {"known_places":{"market":{"map_id":526,"x":3,"y":5},"home":{"map_id":526,"x":2,"y":2},"work":{"map_id":526,"x":4,"y":2},"forage":{"map_id":526,"x":1,"y":5},"well_home":{"map_id":526,"x":2,"y":2},"well_rural":{"map_id":526,"x":1,"y":5},"sacred":{"map_id":526,"x":3,"y":1}},"known_towns":[526,479,302],"route_knowledge_count":2,"knowledge_ids_before":[9029,9030,9047,9048,12673,12672,18376,18377,23839,23842,23843,23845,25333,25334,25338,12671,28376,33443,35214,35227,9040,11781,37689,38425,38434,38435,38444,40148,40162,43012,43019,43847,45428,45430,9026,47765,47767,47770,48558,48563,48567,50145,50150,53101,53102],"market_observation":{"turn":21,"town_id":526,"stock":{"food":125,"grain":36,"water":73,"iron":80,"wood":39},"temporary_work":false,"offers_expire_at":45,"training_offer":null,"price":2,"price_turn":21}}.

**Fatos-fonte retidos após percepção:** [].

| Need | ID/alvo | Base→prioridade | Estado/fonte |
| --- | --- | --- | --- |
| spatial_journey | 54487/479 | 58→58.0 | active / journey |
| divine_contact | 23841/5909 | 47.6→50.45 | active / personal_faith |
| advancement | 23838/None | 24.9726→46.06160845714286 | active / self_assessment:3 |
| water | 43857/None | 44→45.05 | active / physiology |
| rest | 38442/None | 37.4→38.9 | active / physiology |
| religious_interest | 23840/5909 | 33.0→37.7736 | active / own_faith |

**Alternativas/gates realmente vistos:**

Need #54487 (`spatial_journey`): 1 Solutions entraram em _evaluate; 1 saíram disponíveis. Entrada: `route_travel`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| route_travel | {"target":479,"destination":null} | 71.39999999999999 | {"base":0.29,"persistence":0.067,"risk":0.0,"travel":-0.0} | {"feeding":null,"action_pressure":null} |

Need #23838 (`advancement`): 1 Solutions entraram em _evaluate; 1 saíram disponíveis. Entrada: `work`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| work | {"target":null,"destination":{"map_id":526,"x":4,"y":2}} | 49.5 | {"base":0.25,"diligence":0.0475,"physical_depletion":0.0,"travel":-0.05} | {"feeding":null,"action_pressure":null} |

**Escolhas intermediárias:** [{"chosen":{"action":"route_travel","score":71.39999999999999,"target":479,"destination":null,"terms":{"base":0.29,"persistence":0.067,"risk":0.0,"travel":-0.0},"feeding":null,"action_pressure":null},"near_scores":[71.39999999999999],"variation_draws":"não capturados; RNG não consultado pelo observador"}].

**Preparação/substituição posterior:** [].

**Winner final / Goal:** {"winner":{"action":"route_travel","score":71.39999999999999,"target":479,"destination":null,"terms":{"base":0.29,"persistence":0.067,"risk":0.0,"travel":-0.0},"feeding":null,"action_pressure":null},"goal":{"id":54488,"need_id":54487,"action":"route_travel","score":71.39999999999999,"created_at":22,"target_id":479,"destination":null,"status":"completed","outcome":"Caminhada até a saída da localidade."},"suspended_before":null,"suspended_after":null}.

**Por que outras Needs não foram executadas:** a fila prioriza emergência/priority/ID e para na primeira solucionável, sujeita à continuidade/preparo. Outras pressões retidas: divine_contact#23841(50.45), advancement#23838(46.06160845714286), water#43857(45.05), rest#38442(38.9), religious_interest#23840(37.7736). Não atribuir score global entre Needs.

**Execução:** {"success":true,"result":[true,"Caminhada até a saída da localidade."],"goal_at_entry":{"id":54488,"need_id":54487,"action":"route_travel","score":71.39999999999999,"created_at":22,"target_id":479,"destination":null,"status":"active","outcome":""},"before":{"id":3376,"name":"Nora Arven","hour":22,"alive":true,"profession":"lenhador","lod":"active","position":{"map_id":526,"x":3,"y":6},"residence":526,"hp":100,"hunger":31,"thirst":44,"fatigue":37.4,"money":15,"food":2,"water":2,"local_food":123,"local_water":70,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":{"origin":526,"destination":479,"route_ids":[5932],"nodes":[526,479],"reason":"divine_contact","started_at":21,"mode":"known_route","guide_id":null,"leg":0,"offset":0,"last_step":21,"entering":false,"known_at_start":[{"actor":3376,"origin":526,"destination":479,"route_id":5932,"confidence":100,"source":"initial_local_life","learned_at":0,"last_used_at":-1,"source_id":null,"travel_time":4,"danger":4,"condition":"open"}]},"failures":{}},"after":{"id":3376,"name":"Nora Arven","hour":22,"alive":true,"profession":"lenhador","lod":"active","position":{"map_id":1,"x":393,"y":125},"residence":526,"hp":100,"hunger":31,"thirst":44,"fatigue":37.4,"money":15,"food":2,"water":2,"local_food":null,"local_water":null,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":{"origin":526,"destination":479,"route_ids":[5932],"nodes":[526,479],"reason":"divine_contact","started_at":21,"mode":"known_route","guide_id":null,"leg":0,"offset":0,"last_step":22,"entering":false,"known_at_start":[{"actor":3376,"origin":526,"destination":479,"route_id":5932,"confidence":100,"source":"initial_local_life","learned_at":0,"last_used_at":-1,"source_id":null,"travel_time":4,"danger":4,"condition":"open"}]},"failures":{}}}.

**Cálculos especializados reais:** [{"system":"journey_step","function":"geography.Geography.step","result":[true,"Caminhada até a saída da localidade."],"inputs":{}}].

**Evento:** nenhum evento retido durante esta decisão. Isso pode significar movimento/efeito sem evento; não implica falha.

**Aprendizado aceito durante a decisão (amostra):** [].

**Recibos posteriores ligados ao mesmo event_id:** []. Contagem é operações de aprendizado aceitas, não indivíduos únicos.

**Consequência imediata:** {"id":3376,"name":"Nora Arven","hour":22,"alive":true,"profession":"lenhador","lod":"active","position":{"map_id":1,"x":393,"y":125},"residence":526,"hp":100,"hunger":31,"thirst":44,"fatigue":37.4,"money":15,"food":2,"water":2,"local_food":null,"local_water":null,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":{"origin":526,"destination":479,"route_ids":[5932],"nodes":[526,479],"reason":"divine_contact","started_at":21,"mode":"known_route","guide_id":null,"leg":0,"offset":0,"last_step":22,"entering":false,"known_at_start":[{"actor":3376,"origin":526,"destination":479,"route_id":5932,"confidence":100,"source":"initial_local_life","learned_at":0,"last_used_at":-1,"source_id":null,"travel_time":4,"danger":4,"condition":"open"}]},"failures":{}}. **Observação/relações com o alvo ao final:** {"observation_end":null,"relations_end":[]}. Não usar esse estado posterior como entrada antiga nem atribuir consequências futuras sem vínculo causal.

### 42. water — Darin Valerius #1391, h163: drink_well

**Pressão escolhida:** `water` #39395, prioridade 100, base 100, fonte `physiology`, alvo None. Motivo: Sede.

**Contexto preservado:** {"emergency":true}.

**Entrada:** {"id":1391,"name":"Darin Valerius","hour":163,"alive":true,"profession":"ferreiro","lod":"active","position":{"map_id":3,"x":7,"y":13},"residence":3,"hp":90,"hunger":66,"thirst":100,"fatigue":94.00000000000021,"money":4,"food":0,"water":0,"local_food":4,"local_water":0,"recoverable_deprivation":10,"starvation_hours":5,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{"drink_well":163,"fill_water":174}}.

**Personalidade:** {"honesty":55,"compassion":54,"courage":68,"independence":9,"greed":62,"diligence":49,"family_loyalty":77,"persistence":87,"temperament":84,"vengefulness":19,"ambition":24,"sadism":0}. **Emoções escalares de entrada:** {"anger":100.0,"resentment":100.0,"humiliation":100.0,"desperation":38.79999999999994,"last_updated":162,"last_support":-10000,"strain":35.906499999999994,"adaptation":0,"last_adapted":0,"stable_material_hours":0,"nested_collections":"LACUNA: cópia rasa; histórico não utilizado"}.

**Conhecimento/locais de entrada:** {"known_places":{"market":{"map_id":3,"x":7,"y":13},"home":{"map_id":3,"x":2,"y":2},"work":{"map_id":3,"x":12,"y":2},"forage":{"map_id":3,"x":1,"y":13},"well_home":{"map_id":3,"x":2,"y":2},"well_rural":{"map_id":3,"x":1,"y":13},"sacred":{"map_id":3,"x":7,"y":1}},"known_towns":[3,50],"route_knowledge_count":2,"knowledge_ids_before":[117928,203815,202669,94911,201438,202699,205022,205025,205034,205041,206003,206009,206011,206018,206027,206028,206026,206025,206034,206047,206051,206228,206840,206982,208034,208041,208049,208047,209005,209009,213202,213343,213355,213357,213358,213378,213381,213393,214377,214394,214396,214417,214434,215489,215487,215499,215497,216578,216586,209029,212304,217763,217779,217777,217784,218695,218693,218697,218888,218895,218902,218907,218914,218915],"market_observation":{"turn":162,"town_id":3,"stock":{"food":1,"grain":104,"water":0,"iron":114,"wood":82},"temporary_work":true,"offers_expire_at":186,"training_offer":null,"price":14,"price_turn":162}}.

**Fatos-fonte retidos após percepção:** [{"event_id":218693,"kind":"ItemStolen","actor_id":21,"target_id":3,"location":{"map_id":3,"x":7,"y":13},"turn":163,"description":"Lyra Luar roubou comida no mercado de Dorria.","confidence":100,"required_trust":0,"source_id":null,"source_kind":"direct","context":{"item_id":217762,"item_kind":"food"}},{"event_id":117928,"kind":"AbsenceNoticed","actor_id":1391,"target_id":null,"location":{"map_id":3,"x":7,"y":13},"turn":76,"description":"Darin Valerius não localiza um familiar há 39 horas.","confidence":100,"required_trust":0,"source_id":null,"source_kind":"direct","context":{"last_seen":37,"relative_id":1394}},{"event_id":213202,"kind":"CharacterDied","actor_id":null,"target_id":1397,"location":{"map_id":3,"x":7,"y":13},"turn":158,"description":"Lyra Valerius morreu por privação.","confidence":100,"required_trust":0,"source_id":null,"source_kind":"direct","context":{"cause":"deprivation","weapon_id":null,"victim_faction":2}}].

| Need | ID/alvo | Base→prioridade | Estado/fonte |
| --- | --- | --- | --- |
| water | 39395/None | 100→100 | active / physiology |
| rest | 49669/None | 94.00000000000021→100 | active / physiology |
| political_pressure | 51066/None | 80→92.8104 | active / own_shared_problem |
| organizational_survival | 149129/1388 | 65.1235→81.4197 | active / group:149113 |
| food | 17112/None | 79.0→81.25 | active / physiology |
| protection | 51021/1391 | 45→75.818 | active / event:218693 |
| response | 182126/1218 | 55→74.618 | active / event:182125 |
| family | 62025/1394 | 42.3→74.44628571428572 | selected / event:117928 |
| money | 57068/None | 50.791666666666664→71.72766666666666 | active / economy |
| response | 182142/1414 | 50→69.618 | active / event:182137 |
| grief | 213203/1397 | 55.0→69.41194285714285 | active / event:213202 |
| food_reserve | 17111/None | 41.0→68.84905660377359 | active / food_reserve |
| migration | 51065/50 | 52→59.93599999999999 | active / known_towns |

**Alternativas/gates realmente vistos:**

Need #39395 (`water`): 3 Solutions entraram em _evaluate; 3 saíram disponíveis. Entrada: `drink_well, drink_well, drink_well`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| drink_well | {"target":null,"destination":{"map_id":3,"x":7,"y":13}} | 100.0 | {"base":0.5,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| drink_well | {"target":null,"destination":{"map_id":3,"x":1,"y":13}} | 88.0 | {"base":0.5,"travel":-0.06} | {"feeding":null,"action_pressure":null} |
| drink_well | {"target":null,"destination":{"map_id":3,"x":2,"y":2}} | 68.0 | {"base":0.5,"travel":-0.16} | {"feeding":null,"action_pressure":null} |

Need #51021 (`protection`): 25 Solutions entraram em _evaluate; 25 saíram disponíveis. Entrada: `denounce, denounce, denounce, denounce, denounce, denounce, denounce, denounce, denounce, denounce, denounce, denounce, confront, threaten, demand_return, warn, insult, call_help, calm, withdraw, flee, defend, forgive, apologize, surrender`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| demand_return | {"target":21,"destination":null} | 81.35 | {"base":0.2,"honesty":0.06875,"persistence":0.087,"courage":0.051000000000000004,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| denounce | {"target":73,"destination":{"map_id":3,"x":7,"y":13}} | 80.75 | {"base":0.225,"honesty":0.09625,"vengefulness":0.019,"courage":0.051000000000000004,"trust":0.0125,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| denounce | {"target":1218,"destination":{"map_id":3,"x":7,"y":13}} | 80.75 | {"base":0.225,"honesty":0.09625,"vengefulness":0.019,"courage":0.051000000000000004,"trust":0.0125,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| denounce | {"target":1241,"destination":{"map_id":3,"x":7,"y":13}} | 80.75 | {"base":0.225,"honesty":0.09625,"vengefulness":0.019,"courage":0.051000000000000004,"trust":0.0125,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| denounce | {"target":1264,"destination":{"map_id":3,"x":7,"y":13}} | 80.75 | {"base":0.225,"honesty":0.09625,"vengefulness":0.019,"courage":0.051000000000000004,"trust":0.0125,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| denounce | {"target":1287,"destination":{"map_id":3,"x":7,"y":13}} | 80.75 | {"base":0.225,"honesty":0.09625,"vengefulness":0.019,"courage":0.051000000000000004,"trust":0.0125,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| denounce | {"target":1310,"destination":{"map_id":3,"x":7,"y":13}} | 80.75 | {"base":0.225,"honesty":0.09625,"vengefulness":0.019,"courage":0.051000000000000004,"trust":0.0125,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| denounce | {"target":1333,"destination":{"map_id":3,"x":7,"y":13}} | 80.75 | {"base":0.225,"honesty":0.09625,"vengefulness":0.019,"courage":0.051000000000000004,"trust":0.0125,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| denounce | {"target":1356,"destination":{"map_id":3,"x":7,"y":13}} | 80.75 | {"base":0.225,"honesty":0.09625,"vengefulness":0.019,"courage":0.051000000000000004,"trust":0.0125,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| denounce | {"target":1379,"destination":{"map_id":3,"x":7,"y":13}} | 80.75 | {"base":0.225,"honesty":0.09625,"vengefulness":0.019,"courage":0.051000000000000004,"trust":0.0125,"travel":-0.0} | {"feeding":null,"action_pressure":null} |

Need #62025 (`family`): 1 Solutions entraram em _evaluate; 1 saíram disponíveis. Entrada: `check_relative`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| check_relative | {"target":1394,"destination":null} | 76.5 | {"base":0.275,"independence":0.01125,"family_loyalty":0.09625,"travel":-0.0,"no_progress":0.0} | {"feeding":null,"action_pressure":null} |

Need #213203 (`grief`): 29 Solutions entraram em _evaluate; 29 saíram disponíveis. Entrada: `seek_company, seek_company, seek_company, seek_company, seek_company, seek_company, seek_company, seek_company, seek_company, seek_company, seek_company, seek_company, seek_company, seek_company, seek_company, seek_company, seek_company, seek_company, seek_company, seek_company, seek_company, seek_company, seek_company, seek_company, seek_company, seek_company, seek_company, seek_company, remember_relative`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| seek_company | {"target":1394,"destination":null} | 84.8 | {"base":0.225,"compassion":0.054000000000000006,"independence":-0.01575,"trust":0.11375,"relationship":0.04699999999999999,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| seek_company | {"target":1388,"destination":null} | 76.15 | {"base":0.225,"compassion":0.054000000000000006,"independence":-0.01575,"trust":0.0875,"relationship":0.03,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| remember_relative | {"target":1397,"destination":{"map_id":3,"x":7,"y":13}} | 59.650000000000006 | {"base":0.2,"independence":0.01125,"persistence":0.087,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| seek_company | {"target":21,"destination":null} | 56.15 | {"base":0.225,"compassion":0.054000000000000006,"independence":-0.01575,"trust":0.0175,"relationship":0.0,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| seek_company | {"target":24,"destination":null} | 56.15 | {"base":0.225,"compassion":0.054000000000000006,"independence":-0.01575,"trust":0.0175,"relationship":0.0,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| seek_company | {"target":1207,"destination":null} | 56.15 | {"base":0.225,"compassion":0.054000000000000006,"independence":-0.01575,"trust":0.0175,"relationship":0.0,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| seek_company | {"target":1210,"destination":null} | 56.15 | {"base":0.225,"compassion":0.054000000000000006,"independence":-0.01575,"trust":0.0175,"relationship":0.0,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| seek_company | {"target":1241,"destination":null} | 56.15 | {"base":0.225,"compassion":0.054000000000000006,"independence":-0.01575,"trust":0.0175,"relationship":0.0,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| seek_company | {"target":1250,"destination":null} | 56.15 | {"base":0.225,"compassion":0.054000000000000006,"independence":-0.01575,"trust":0.0175,"relationship":0.0,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| seek_company | {"target":1256,"destination":null} | 56.15 | {"base":0.225,"compassion":0.054000000000000006,"independence":-0.01575,"trust":0.0175,"relationship":0.0,"travel":-0.0} | {"feeding":null,"action_pressure":null} |

**Escolhas intermediárias:** [{"chosen":{"action":"drink_well","score":100.0,"target":null,"destination":{"map_id":3,"x":7,"y":13},"terms":{"base":0.5,"travel":-0.0},"feeding":null,"action_pressure":null},"near_scores":[100.0,88.0,68.0],"variation_draws":"não capturados; RNG não consultado pelo observador"}].

**Preparação/substituição posterior:** [].

**Winner final / Goal:** {"winner":{"action":"drink_well","score":100.0,"target":null,"destination":{"map_id":3,"x":7,"y":13},"terms":{"base":0.5,"travel":-0.0},"feeding":null,"action_pressure":null},"goal":{"id":218916,"need_id":39395,"action":"drink_well","score":100.0,"created_at":163,"target_id":null,"destination":{"map_id":3,"x":7,"y":13},"status":"failed","outcome":"Não há água disponível."},"suspended_before":null,"suspended_after":null}.

**Por que outras Needs não foram executadas:** a fila prioriza emergência/priority/ID e para na primeira solucionável, sujeita à continuidade/preparo. Outras pressões retidas: rest#49669(100), political_pressure#51066(92.8104), organizational_survival#149129(81.4197), food#17112(81.25), protection#51021(75.818), response#182126(74.618), family#62025(74.44628571428572), money#57068(71.72766666666666), response#182142(69.618), grief#213203(69.41194285714285), food_reserve#17111(68.84905660377359), migration#51065(59.93599999999999). Não atribuir score global entre Needs.

**Execução:** {"success":false,"result":[false,"Não há água disponível."],"goal_at_entry":{"id":218916,"need_id":39395,"action":"drink_well","score":100.0,"created_at":163,"target_id":null,"destination":{"map_id":3,"x":7,"y":13},"status":"active","outcome":""},"before":{"id":1391,"name":"Darin Valerius","hour":163,"alive":true,"profession":"ferreiro","lod":"active","position":{"map_id":3,"x":7,"y":13},"residence":3,"hp":90,"hunger":66,"thirst":100,"fatigue":94.00000000000021,"money":4,"food":0,"water":0,"local_food":4,"local_water":0,"recoverable_deprivation":10,"starvation_hours":5,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{"fill_water":174}},"after":{"id":1391,"name":"Darin Valerius","hour":163,"alive":true,"profession":"ferreiro","lod":"active","position":{"map_id":3,"x":7,"y":13},"residence":3,"hp":90,"hunger":66,"thirst":100,"fatigue":94.00000000000021,"money":4,"food":0,"water":0,"local_food":4,"local_water":0,"recoverable_deprivation":10,"starvation_hours":5,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{"fill_water":174}}}.

**Cálculos especializados reais:** [{"system":"lethal_decision","function":"lethal_decisions.LethalDecisionSystem.evaluate","result":{"available":false,"pressure":-77.54,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"protection","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":3.2300000000000004,"directed_emotion":3.9545000000000003,"commitment":0.0,"sadism":0.0,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":29.700000000000003,"moral_restraint":6.6,"fear":0.0,"risk":3.423331635252165,"bond":0.0,"authority_or_witnesses":15,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{"pressure":-77.54,"cause":{"severity":0,"grave":false,"causes":[],"facts":[],"confidence":0,"mode":"retributive","confirmed_injury":0}}},{"system":"lethal_decision","function":"lethal_decisions.LethalDecisionSystem.evaluate","result":{"available":false,"pressure":-77.54,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"protection","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":3.2300000000000004,"directed_emotion":3.9545000000000003,"commitment":0.0,"sadism":0.0,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":29.700000000000003,"moral_restraint":6.6,"fear":0.0,"risk":3.423331635252165,"bond":0.0,"authority_or_witnesses":15,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{"pressure":-77.54,"cause":{"severity":0,"grave":false,"causes":[],"facts":[],"confidence":0,"mode":"retributive","confirmed_injury":0}}},{"system":"lethal_pressure","function":"lethality.LethalPressure.evaluate","result":{"available":false,"pressure":-77.54,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"protection","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":3.2300000000000004,"directed_emotion":3.9545000000000003,"commitment":0.0,"sadism":0.0,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":29.700000000000003,"moral_restraint":6.6,"fear":0.0,"risk":3.423331635252165,"bond":0.0,"authority_or_witnesses":15,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{}},{"system":"lethal_decision","function":"lethal_decisions.LethalDecisionSystem.evaluate","result":{"available":false,"pressure":-114.4,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"response","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":3.2300000000000004,"directed_emotion":0.0,"commitment":0.0,"sadism":0.0,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":29.700000000000003,"moral_restraint":6.6,"fear":29.8,"risk":6.5325443786982245,"bond":0.0,"authority_or_witnesses":15,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{"pressure":-114.4,"cause":{"severity":0,"grave":false,"causes":[],"facts":[],"confidence":0,"mode":"retributive","confirmed_injury":0}}},{"system":"lethal_decision","function":"lethal_decisions.LethalDecisionSystem.evaluate","result":{"available":false,"pressure":-114.4,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"response","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":3.2300000000000004,"directed_emotion":0.0,"commitment":0.0,"sadism":0.0,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":29.700000000000003,"moral_restraint":6.6,"fear":29.8,"risk":6.5325443786982245,"bond":0.0,"authority_or_witnesses":15,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{"pressure":-114.4,"cause":{"severity":0,"grave":false,"causes":[],"facts":[],"confidence":0,"mode":"retributive","confirmed_injury":0}}},{"system":"lethal_pressure","function":"lethality.LethalPressure.evaluate","result":{"available":false,"pressure":-114.4,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"response","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":3.2300000000000004,"directed_emotion":0.0,"commitment":0.0,"sadism":0.0,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":29.700000000000003,"moral_restraint":6.6,"fear":29.8,"risk":6.5325443786982245,"bond":0.0,"authority_or_witnesses":15,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{}},{"system":"lethal_decision","function":"lethal_decisions.LethalDecisionSystem.evaluate","result":{"available":false,"pressure":-82.66,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"response","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":3.2300000000000004,"directed_emotion":0.0,"commitment":0.0,"sadism":0.0,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":29.700000000000003,"moral_restraint":6.6,"fear":0.0,"risk":4.590964590964591,"bond":0.0,"authority_or_witnesses":15,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{"pressure":-82.66,"cause":{"severity":0,"grave":false,"causes":[],"facts":[],"confidence":0,"mode":"retributive","confirmed_injury":0}}},{"system":"lethal_decision","function":"lethal_decisions.LethalDecisionSystem.evaluate","result":{"available":false,"pressure":-82.66,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"response","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":3.2300000000000004,"directed_emotion":0.0,"commitment":0.0,"sadism":0.0,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":29.700000000000003,"moral_restraint":6.6,"fear":0.0,"risk":4.590964590964591,"bond":0.0,"authority_or_witnesses":15,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{"pressure":-82.66,"cause":{"severity":0,"grave":false,"causes":[],"facts":[],"confidence":0,"mode":"retributive","confirmed_injury":0}}},{"system":"lethal_pressure","function":"lethality.LethalPressure.evaluate","result":{"available":false,"pressure":-82.66,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"response","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":3.2300000000000004,"directed_emotion":0.0,"commitment":0.0,"sadism":0.0,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":29.700000000000003,"moral_restraint":6.6,"fear":0.0,"risk":4.590964590964591,"bond":0.0,"authority_or_witnesses":15,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{}}].

**Evento:** nenhum evento retido durante esta decisão. Isso pode significar movimento/efeito sem evento; não implica falha.

**Aprendizado aceito durante a decisão (amostra):** [].

**Recibos posteriores ligados ao mesmo event_id:** []. Contagem é operações de aprendizado aceitas, não indivíduos únicos.

**Consequência imediata:** {"id":1391,"name":"Darin Valerius","hour":163,"alive":true,"profession":"ferreiro","lod":"active","position":{"map_id":3,"x":7,"y":13},"residence":3,"hp":90,"hunger":66,"thirst":100,"fatigue":94.00000000000021,"money":4,"food":0,"water":0,"local_food":4,"local_water":0,"recoverable_deprivation":10,"starvation_hours":5,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{"fill_water":174,"drink_well":175}}. **Observação/relações com o alvo ao final:** {"observation_end":null,"relations_end":[]}. Não usar esse estado posterior como entrada antiga nem atribuir consequências futuras sem vínculo causal.

### 43. work — Elena Solaris #1699, h12: work

**Pressão escolhida:** `work` #30956, prioridade 52.2, base 35, fonte `profession`, alvo None. Motivo: Responsabilidade profissional.

**Contexto preservado:** {}.

**Entrada:** {"id":1699,"name":"Elena Solaris","hour":12,"alive":true,"profession":"cozinheiro","lod":"local","position":{"map_id":97,"x":3,"y":5},"residence":97,"hp":100,"hunger":30,"thirst":24,"fatigue":26.39999999999999,"money":22,"food":2,"water":0,"local_food":101,"local_water":80,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{}}.

**Personalidade:** {"honesty":11,"compassion":15,"courage":62,"independence":60,"greed":85,"diligence":83,"family_loyalty":32,"persistence":32,"temperament":40,"vengefulness":60,"ambition":20,"sadism":1}. **Emoções escalares de entrada:** {"anger":0.0,"resentment":0.0,"humiliation":0.0,"desperation":0.0,"last_updated":11,"last_support":-10000,"strain":0,"adaptation":0,"last_adapted":0,"stable_material_hours":0,"nested_collections":"LACUNA: cópia rasa; histórico não utilizado"}.

**Conhecimento/locais de entrada:** {"known_places":{"market":{"map_id":97,"x":3,"y":5},"home":{"map_id":97,"x":2,"y":2},"work":{"map_id":97,"x":3,"y":5},"forage":{"map_id":97,"x":1,"y":5},"well_home":{"map_id":97,"x":2,"y":2},"well_rural":{"map_id":97,"x":1,"y":5},"sacred":{"map_id":97,"x":3,"y":1}},"known_towns":[97,50,3],"route_knowledge_count":2,"knowledge_ids_before":[7377,7378,7379,7380,7383,7384,7385,7386,7389,7390,7391,7392,7395,7396,7397,7398,7401,7402,12181,12182,12183,12184,12185,12186,12187,12188,12189,14233,14236,14252,20504,20525,23473,20516,28056,28054,28063,28951,29303,30958,30959,32866,34645,36294,36298,36302],"market_observation":{"turn":11,"town_id":97,"stock":{"food":75,"grain":36,"water":80,"iron":30,"wood":50},"temporary_work":false,"offers_expire_at":35,"training_offer":null,"price":2,"price_turn":11}}.

**Fatos-fonte retidos após percepção:** [].

| Need | ID/alvo | Base→prioridade | Estado/fonte |
| --- | --- | --- | --- |
| work | 30956/None | 35→52.2 | active / profession |
| rest | 36292/None | 26.39999999999999→26.54999999999999 | active / physiology |
| advancement | 14234/None | 19.704→26.504 | active / aspiration:wealth |

**Alternativas/gates realmente vistos:**

Need #30956 (`work`): 1 Solutions entraram em _evaluate; 1 saíram disponíveis. Entrada: `work`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| work | {"target":null,"destination":{"map_id":97,"x":3,"y":5}} | 91.5 | {"base":0.25,"diligence":0.2075,"physical_depletion":0.0,"travel":-0.0} | {"feeding":null,"action_pressure":null} |

Need #14234 (`advancement`): 2 Solutions entraram em _evaluate; 2 saíram disponíveis. Entrada: `work, steal_person`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| work | {"target":null,"destination":{"map_id":97,"x":3,"y":5}} | 91.5 | {"base":0.25,"diligence":0.2075,"physical_depletion":0.0,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| steal_person | {"target":1711,"destination":null} | 52.476190475102044 | {"base":0.31,"greed":0.17,"honesty":-0.0495,"authority":-0.2,"courage":0.031,"travel":-0.0,"pressure_moral_tolerance":0.0008809523755102042} | {"feeding":null,"action_pressure":null} |

**Escolhas intermediárias:** [{"chosen":{"action":"work","score":91.5,"target":null,"destination":{"map_id":97,"x":3,"y":5},"terms":{"base":0.25,"diligence":0.2075,"physical_depletion":0.0,"travel":-0.0},"feeding":null,"action_pressure":null},"near_scores":[91.5],"variation_draws":"não capturados; RNG não consultado pelo observador"}].

**Preparação/substituição posterior:** [].

**Winner final / Goal:** {"winner":{"action":"work","score":91.5,"target":null,"destination":{"map_id":97,"x":3,"y":5},"terms":{"base":0.25,"diligence":0.2075,"physical_depletion":0.0,"travel":-0.0},"feeding":null,"action_pressure":null},"goal":{"id":37957,"need_id":30956,"action":"work","score":91.5,"created_at":12,"target_id":null,"destination":{"map_id":97,"x":3,"y":5},"status":"completed","outcome":"Produção concluída com pagamento."},"suspended_before":null,"suspended_after":null}.

**Por que outras Needs não foram executadas:** a fila prioriza emergência/priority/ID e para na primeira solucionável, sujeita à continuidade/preparo. Outras pressões retidas: rest#36292(26.54999999999999), advancement#14234(26.504). Não atribuir score global entre Needs.

**Execução:** {"success":true,"result":[true,"Produção concluída com pagamento."],"goal_at_entry":{"id":37957,"need_id":30956,"action":"work","score":91.5,"created_at":12,"target_id":null,"destination":{"map_id":97,"x":3,"y":5},"status":"active","outcome":""},"before":{"id":1699,"name":"Elena Solaris","hour":12,"alive":true,"profession":"cozinheiro","lod":"local","position":{"map_id":97,"x":3,"y":5},"residence":97,"hp":100,"hunger":30,"thirst":24,"fatigue":26.39999999999999,"money":22,"food":2,"water":0,"local_food":101,"local_water":80,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{}},"after":{"id":1699,"name":"Elena Solaris","hour":12,"alive":true,"profession":"cozinheiro","lod":"local","position":{"map_id":97,"x":3,"y":5},"residence":97,"hp":100,"hunger":30,"thirst":24,"fatigue":26.39999999999999,"money":23,"food":2,"water":0,"local_food":104,"local_water":80,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{}}}.

**Cálculos especializados reais:** [{"system":"work","actual":{"actor":1699,"town":97,"money_before":22,"treasury_before":819,"inputs_before":{"food":101,"grain":28,"iron":44,"wood":59},"result":{"status":"paid","message":"Produção concluída com pagamento.","produced":3,"paid":1,"credit_added":6}}}].

| Evento/hora | Actor→target | Emissor | Testemunhas | Contexto |
| --- | --- | --- | --- | --- |
| 37958 / 12 / ItemCreated | 1699→97 | ["professions.ProfessionSystem.work","goals.GoalSystem._execute","goals.GoalSystem.execute"] | [106,109,1699,1708,1711,1713,1716,1722,1734] | {} |

**Aprendizado aceito durante a decisão (amostra):** [{"npc":106,"event":37958,"kind":"ItemCreated","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":109,"event":37958,"kind":"ItemCreated","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":1699,"event":37958,"kind":"ItemCreated","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":1708,"event":37958,"kind":"ItemCreated","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":1711,"event":37958,"kind":"ItemCreated","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":1713,"event":37958,"kind":"ItemCreated","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":1716,"event":37958,"kind":"ItemCreated","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":1722,"event":37958,"kind":"ItemCreated","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":1734,"event":37958,"kind":"ItemCreated","source":null,"firsthand":true,"confidence":100,"latency":0}].

**Recibos posteriores ligados ao mesmo event_id:** [{"event":37958,"kind":"ItemCreated","learned":{"count":9,"first":12,"last":12,"first_people":[106,109,1699,1708,1711,1713]}}]. Contagem é operações de aprendizado aceitas, não indivíduos únicos.

**Consequência imediata:** {"id":1699,"name":"Elena Solaris","hour":12,"alive":true,"profession":"cozinheiro","lod":"local","position":{"map_id":97,"x":3,"y":5},"residence":97,"hp":100,"hunger":30,"thirst":24,"fatigue":26.39999999999999,"money":23,"food":2,"water":0,"local_food":104,"local_water":80,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{}}. **Observação/relações com o alvo ao final:** {"observation_end":null,"relations_end":[]}. Não usar esse estado posterior como entrada antiga nem atribuir consequências futuras sem vínculo causal.

### 44. blocked — Arthus Alvor #3237, h11: sem seleção

**Sem seleção viável** no retorno de decide. Isso não demonstra ausência de todas as pressões: examinar Needs e avaliações abaixo.

**Entrada:** {"id":3237,"name":"Arthus Alvor","hour":11,"alive":true,"profession":"guarda","lod":"active","position":{"map_id":479,"x":5,"y":9},"residence":479,"hp":100,"hunger":10,"thirst":22,"fatigue":20.199999999999992,"money":24,"food":1,"water":0,"local_food":81,"local_water":80,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{"organize":14}}.

**Personalidade:** {"honesty":46,"compassion":8,"courage":5,"independence":93,"greed":64,"diligence":29,"family_loyalty":76,"persistence":87,"temperament":65,"vengefulness":23,"ambition":69,"sadism":0}. **Emoções escalares de entrada:** {"anger":0.0,"resentment":0.0,"humiliation":0.0,"desperation":0.0,"last_updated":10,"last_support":-10000,"strain":0,"adaptation":0,"last_adapted":0,"stable_material_hours":0,"nested_collections":"LACUNA: cópia rasa; histórico não utilizado"}.

**Conhecimento/locais de entrada:** {"known_places":{"market":{"map_id":479,"x":5,"y":9},"home":{"map_id":479,"x":2,"y":2},"work":{"map_id":479,"x":5,"y":9},"forage":{"map_id":479,"x":1,"y":9},"well_home":{"map_id":479,"x":2,"y":2},"well_rural":{"map_id":479,"x":1,"y":9},"sacred":{"map_id":479,"x":5,"y":1}},"known_towns":[479,302,508,526],"route_knowledge_count":6,"knowledge_ids_before":[27747,27749,27764,27765,27766,27767,27763,27762,27761,27760,27759,27758,27757,27756,27755,27754,27768,28299,28319,28334,28338,29031,29032,29034,29036,29035,29739,29755,29756,29759,29760,29763,30537,30538,31500,31501,31511,31516,31514,32532,33385,33386,33400,34285,34286,34288,34291,34292,34290,34289,34298,34299,34301,34302,34305,34307,34309,35181,35183,35191,35193,35204,35205,36725],"market_observation":{"turn":10,"town_id":479,"stock":{"food":58,"grain":56,"water":80,"iron":52,"wood":34},"temporary_work":false,"offers_expire_at":34,"training_offer":null,"price":2,"price_turn":10}}.

**Fatos-fonte retidos após percepção:** [].

| Need | ID/alvo | Base→prioridade | Estado/fonte |
| --- | --- | --- | --- |
| organizational_survival | 28332/3237 | 67.9515→77.13812685714285 | active / group:27751 |
| political_pressure | 21313/None | 65.35→77.10417428571428 | active / own_shared_problem |
| protection | 19893/502 | 50→68.45 | blocked / event:19889 |
| migration | 21312/508 | 52→54.990857142857145 | active / known_towns |
| advancement | 15053/None | 24.807000000000002→48.554725485714286 | blocked / self_assessment:0 |
| work | 31509/None | 35→41.25 | active / profession |
| food_reserve | 29761/None | 32.0→36.473684210526315 | active / food_reserve |
| religious_interest | 15055/5909 | 27.5→31.721314285714286 | active / own_faith |

**Alternativas/gates realmente vistos:**

Need #28332 (`organizational_survival`): 0 Solutions entraram em _evaluate; 0 saíram disponíveis. Entrada: ``.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |

Need #21313 (`political_pressure`): 0 Solutions entraram em _evaluate; 0 saíram disponíveis. Entrada: ``.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |

Need #19893 (`protection`): 0 Solutions entraram em _evaluate; 0 saíram disponíveis. Entrada: ``.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |

Need #21312 (`migration`): 0 Solutions entraram em _evaluate; 0 saíram disponíveis. Entrada: ``.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |

Need #15053 (`advancement`): 0 Solutions entraram em _evaluate; 0 saíram disponíveis. Entrada: ``.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |

Need #31509 (`work`): 0 Solutions entraram em _evaluate; 0 saíram disponíveis. Entrada: ``.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |

Need #29761 (`food_reserve`): 0 Solutions entraram em _evaluate; 0 saíram disponíveis. Entrada: ``.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |

Need #15055 (`religious_interest`): 0 Solutions entraram em _evaluate; 0 saíram disponíveis. Entrada: ``.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |

**Escolhas intermediárias:** [].

**Preparação/substituição posterior:** [].

**Winner final / Goal:** {"winner":{},"goal":null,"suspended_before":null,"suspended_after":null}.

**Execução:** execute não foi chamado neste trace. A Goal pode ter iniciado/continuado deslocamento; o snapshot e a posição posterior delimitam essa conclusão.

**Cálculos especializados reais:** [{"system":"lethal_decision","function":"lethal_decisions.LethalDecisionSystem.evaluate","result":{"available":false,"pressure":-55.26,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"protection","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":3.91,"directed_emotion":0.0,"commitment":0.0,"sadism":0.0,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":4.4,"moral_restraint":5.52,"fear":0.0,"risk":4.253810705423609,"bond":0.0,"authority_or_witnesses":15,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{"pressure":-55.26,"cause":{"severity":0,"grave":false,"causes":[],"facts":[],"confidence":0,"mode":"retributive","confirmed_injury":0}}},{"system":"lethal_decision","function":"lethal_decisions.LethalDecisionSystem.evaluate","result":{"available":false,"pressure":-55.26,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"protection","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":3.91,"directed_emotion":0.0,"commitment":0.0,"sadism":0.0,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":4.4,"moral_restraint":5.52,"fear":0.0,"risk":4.253810705423609,"bond":0.0,"authority_or_witnesses":15,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{"pressure":-55.26,"cause":{"severity":0,"grave":false,"causes":[],"facts":[],"confidence":0,"mode":"retributive","confirmed_injury":0}}},{"system":"lethal_pressure","function":"lethality.LethalPressure.evaluate","result":{"available":false,"pressure":-55.26,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"protection","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":3.91,"directed_emotion":0.0,"commitment":0.0,"sadism":0.0,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":4.4,"moral_restraint":5.52,"fear":0.0,"risk":4.253810705423609,"bond":0.0,"authority_or_witnesses":15,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{}}].

**Evento:** nenhum evento retido durante esta decisão. Isso pode significar movimento/efeito sem evento; não implica falha.

**Aprendizado aceito durante a decisão (amostra):** [].

**Recibos posteriores ligados ao mesmo event_id:** []. Contagem é operações de aprendizado aceitas, não indivíduos únicos.

**Consequência imediata:** {"id":3237,"name":"Arthus Alvor","hour":11,"alive":true,"profession":"guarda","lod":"active","position":{"map_id":479,"x":5,"y":9},"residence":479,"hp":100,"hunger":10,"thirst":22,"fatigue":20.199999999999992,"money":24,"food":1,"water":0,"local_food":81,"local_water":80,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{"organize":14}}. **Observação/relações com o alvo ao final:** {"observation_end":null,"relations_end":[]}. Não usar esse estado posterior como entrada antiga nem atribuir consequências futuras sem vínculo causal.

### 45. career — Tomas Hammer #1633, h12: work

**Pressão escolhida:** `advancement` #14221, prioridade 48.40500130285715, base 25.242600000000003, fonte `self_assessment:0`, alvo None. Motivo: Acumular uma reserva maior com trabalho e comércio disponíveis.

**Contexto preservado:** {"diagnostic":{"reason":"Selected","competing":null,"turn":12}}.

**Entrada:** {"id":1633,"name":"Tomas Hammer","hour":12,"alive":true,"profession":"lenhador","lod":"local","position":{"map_id":50,"x":8,"y":2},"residence":50,"hp":100,"hunger":15,"thirst":24,"fatigue":19.399999999999995,"money":13,"food":1,"water":0,"local_food":78,"local_water":78,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{}}.

**Personalidade:** {"honesty":13,"compassion":9,"courage":58,"independence":65,"greed":57,"diligence":24,"family_loyalty":18,"persistence":95,"temperament":24,"vengefulness":34,"ambition":71,"sadism":0}. **Emoções escalares de entrada:** {"anger":0.0,"resentment":0.0,"humiliation":0.0,"desperation":0.0,"last_updated":9,"last_support":-10000,"strain":0,"adaptation":0,"last_adapted":0,"stable_material_hours":0,"nested_collections":"LACUNA: cópia rasa; histórico não utilizado"}.

**Conhecimento/locais de entrada:** {"known_places":{"market":{"map_id":50,"x":5,"y":9},"home":{"map_id":50,"x":2,"y":2},"work":{"map_id":50,"x":8,"y":2},"forage":{"map_id":50,"x":1,"y":9},"well_home":{"map_id":50,"x":2,"y":2},"well_rural":{"map_id":50,"x":1,"y":9},"sacred":{"map_id":50,"x":5,"y":1}},"known_towns":[50,3],"route_knowledge_count":2,"knowledge_ids_before":[12150,12151,12152,12153,12154,12155,12149,12148,12147,12146,12145,12144,12143,12142,12141,12140,12139,12138,12137,12136,12135,12134,12133,12132,12131,12130,12129,12128,12127,12126,12125,12124,12123,12122,14190,14196,14198,14213,14222,20377,17376,28047,29250,30906,30932,30947,30948,32820,32824,32848,34159,34160,34583,34588,34589,36228,36247,36250,7231,23435,26368,37919,37928,37949],"market_observation":{"turn":9,"town_id":50,"stock":{"food":76,"grain":69,"water":78,"iron":58,"wood":43},"temporary_work":false,"offers_expire_at":33,"training_offer":null}}.

**Fatos-fonte retidos após percepção:** [].

| Need | ID/alvo | Base→prioridade | Estado/fonte |
| --- | --- | --- | --- |
| advancement | 14221/None | 25.242600000000003→48.40500130285715 | selected / self_assessment:0 |
| work | 32846/None | 35→40.25 | active / profession |
| food_reserve | 37951/None | 33.0→33.0 | active / food_reserve |

**Alternativas/gates realmente vistos:**

Need #14221 (`advancement`): 1 Solutions entraram em _evaluate; 1 saíram disponíveis. Entrada: `work`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| work | {"target":null,"destination":{"map_id":50,"x":8,"y":2}} | 62.0 | {"base":0.25,"diligence":0.06,"physical_depletion":0.0,"travel":-0.0,"no_progress":0.0} | {"feeding":null,"action_pressure":null} |

**Escolhas intermediárias:** [{"chosen":{"action":"work","score":62.0,"target":null,"destination":{"map_id":50,"x":8,"y":2},"terms":{"base":0.25,"diligence":0.06,"physical_depletion":0.0,"travel":-0.0,"no_progress":0.0},"feeding":null,"action_pressure":null},"near_scores":[62.0],"variation_draws":"não capturados; RNG não consultado pelo observador"}].

**Preparação/substituição posterior:** [].

**Winner final / Goal:** {"winner":{"action":"work","score":62.0,"target":null,"destination":{"map_id":50,"x":8,"y":2},"terms":{"base":0.25,"diligence":0.06,"physical_depletion":0.0,"travel":-0.0,"no_progress":0.0},"feeding":null,"action_pressure":null},"goal":{"id":37954,"need_id":14221,"action":"work","score":62.0,"created_at":12,"target_id":null,"destination":{"map_id":50,"x":8,"y":2},"status":"completed","outcome":"Produção concluída com pagamento."},"suspended_before":null,"suspended_after":null}.

**Por que outras Needs não foram executadas:** a fila prioriza emergência/priority/ID e para na primeira solucionável, sujeita à continuidade/preparo. Outras pressões retidas: work#32846(40.25), food_reserve#37951(33.0). Não atribuir score global entre Needs.

**Execução:** {"success":true,"result":[true,"Produção concluída com pagamento."],"goal_at_entry":{"id":37954,"need_id":14221,"action":"work","score":62.0,"created_at":12,"target_id":null,"destination":{"map_id":50,"x":8,"y":2},"status":"active","outcome":""},"before":{"id":1633,"name":"Tomas Hammer","hour":12,"alive":true,"profession":"lenhador","lod":"local","position":{"map_id":50,"x":8,"y":2},"residence":50,"hp":100,"hunger":15,"thirst":24,"fatigue":19.399999999999995,"money":13,"food":1,"water":0,"local_food":78,"local_water":78,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{}},"after":{"id":1633,"name":"Tomas Hammer","hour":12,"alive":true,"profession":"lenhador","lod":"local","position":{"map_id":50,"x":8,"y":2},"residence":50,"hp":100,"hunger":15,"thirst":24,"fatigue":19.399999999999995,"money":16,"food":1,"water":0,"local_food":78,"local_water":78,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{}}}.

**Cálculos especializados reais:** [{"system":"work","actual":{"actor":1633,"town":50,"money_before":13,"treasury_before":1324,"inputs_before":{"food":78,"grain":96,"iron":80,"wood":65},"result":{"status":"paid","message":"Produção concluída com pagamento.","produced":6,"paid":3,"credit_added":18}}}].

| Evento/hora | Actor→target | Emissor | Testemunhas | Contexto |
| --- | --- | --- | --- | --- |
| 37953 / 12 / CommitmentCreated | 1633→None | ["agency.AgencySystem.event","agency.AgencySystem.adopt","agency.AgencySystem.refresh"] | [1633] | {"impulse":52.783642285714286,"agency":0.8155,"commitment_id":37952,"need_id":14221,"origin":"advancement","source_fact":null,"target":null,"progress":0} |
| 37955 / 12 / ItemCreated | 1633→50 | ["professions.ProfessionSystem.work","goals.GoalSystem._execute","goals.GoalSystem.execute"] | [65,1515,1538,1541,1558,1564,1581,1584,1587,1627,1633,1653] | {} |
| 37956 / 12 / CommitmentProgress | 1633→None | ["agency.AgencySystem.event","agency.AgencySystem.outcome","goals.GoalSystem.execute"] | [1633] | {"changes":["money"],"action":"work","commitment_id":37952,"need_id":14221,"origin":"advancement","source_fact":null,"target":null,"progress":1} |

**Aprendizado aceito durante a decisão (amostra):** [{"npc":1633,"event":37953,"kind":"CommitmentCreated","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":65,"event":37955,"kind":"ItemCreated","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":1515,"event":37955,"kind":"ItemCreated","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":1538,"event":37955,"kind":"ItemCreated","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":1541,"event":37955,"kind":"ItemCreated","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":1558,"event":37955,"kind":"ItemCreated","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":1564,"event":37955,"kind":"ItemCreated","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":1581,"event":37955,"kind":"ItemCreated","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":1584,"event":37955,"kind":"ItemCreated","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":1587,"event":37955,"kind":"ItemCreated","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":1627,"event":37955,"kind":"ItemCreated","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":1633,"event":37955,"kind":"ItemCreated","source":null,"firsthand":true,"confidence":100,"latency":0}].

**Recibos posteriores ligados ao mesmo event_id:** [{"event":37953,"kind":"CommitmentCreated","learned":{"count":2,"first":12,"last":24,"first_people":[1633,1558]}},{"event":37955,"kind":"ItemCreated","learned":{"count":12,"first":12,"last":12,"first_people":[65,1515,1538,1541,1558,1564]}},{"event":37956,"kind":"CommitmentProgress","learned":{"count":1,"first":12,"last":12,"first_people":[1633]}}]. Contagem é operações de aprendizado aceitas, não indivíduos únicos.

**Consequência imediata:** {"id":1633,"name":"Tomas Hammer","hour":12,"alive":true,"profession":"lenhador","lod":"local","position":{"map_id":50,"x":8,"y":2},"residence":50,"hp":100,"hunger":15,"thirst":24,"fatigue":19.399999999999995,"money":16,"food":1,"water":0,"local_food":78,"local_water":78,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{}}. **Observação/relações com o alvo ao final:** {"observation_end":null,"relations_end":[]}. Não usar esse estado posterior como entrada antiga nem atribuir consequências futuras sem vínculo causal.

### 46. combat — Bela Luar #5612, h149: demand_return

**Pressão escolhida:** `protection` #30298, prioridade 68.425, base 45, fonte `event:202428`, alvo 5612. Motivo: Crime conhecido ameaça segurança pessoal/familiar.

**Contexto preservado:** {"source_event":202428,"threat":5614,"known_location":{"map_id":1070,"x":3,"y":5},"diagnostic":{"reason":"Selected","competing":null,"turn":149}}.

**Entrada:** {"id":5612,"name":"Bela Luar","hour":149,"alive":true,"profession":"comerciante","lod":"active","position":{"map_id":1070,"x":3,"y":5},"residence":1070,"hp":100,"hunger":48,"thirst":28,"fatigue":56.80000000000035,"money":17,"food":0,"water":0,"local_food":48,"local_water":151,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{"organize":158}}.

**Personalidade:** {"honesty":87,"compassion":35,"courage":85,"independence":34,"greed":83,"diligence":38,"family_loyalty":85,"persistence":87,"temperament":43,"vengefulness":41,"ambition":71,"sadism":0}. **Emoções escalares de entrada:** {"anger":31.38,"resentment":46.38000000000001,"humiliation":16.8,"desperation":0.2999999999999999,"last_updated":148,"last_support":145,"strain":0,"adaptation":0,"last_adapted":0,"stable_material_hours":0,"nested_collections":"LACUNA: cópia rasa; histórico não utilizado"}.

**Conhecimento/locais de entrada:** {"known_places":{"market":{"map_id":1070,"x":3,"y":5},"home":{"map_id":1070,"x":2,"y":2},"work":{"map_id":1070,"x":3,"y":5},"forage":{"map_id":1070,"x":1,"y":5},"well_home":{"map_id":1070,"x":2,"y":2},"well_rural":{"map_id":1070,"x":1,"y":5},"sacred":{"map_id":1070,"x":3,"y":1}},"known_towns":[1070,1023,864],"route_knowledge_count":2,"knowledge_ids_before":[175531,175533,175535,175846,176717,176719,176720,176721,176722,176727,178693,179778,179968,180784,186250,186251,186252,186259,186260,186261,186262,186263,186264,186265,186258,186257,186266,186456,186457,179965,190029,190030,190032,190037,191117,193820,195180,195181,195179,195185,198306,198313,198320,198538,198545,199727,199729,199732,199735,199948,201065,201066,201067,201068,201071,201073,201347,202424,202426,202428,202436,202640,203786,203788],"market_observation":{"turn":148,"town_id":1070,"stock":{"food":48,"grain":92,"water":151,"iron":55,"wood":70},"temporary_work":false,"offers_expire_at":172,"training_offer":null,"price":2,"price_turn":148}}.

**Fatos-fonte retidos após percepção:** [{"event_id":202428,"kind":"ItemStolen","actor_id":5614,"target_id":5612,"location":{"map_id":1070,"x":3,"y":5},"turn":147,"description":"Arthus Kars roubou provisão de Bela Luar.","confidence":100,"required_trust":0,"source_id":null,"source_kind":"direct","context":{"item_id":5615,"item_kind":"food"}}].

| Need | ID/alvo | Base→prioridade | Estado/fonte |
| --- | --- | --- | --- |
| political_pressure | 35904/None | 65.65→78.89777142857143 | active / own_shared_problem |
| protection | 30298/5612 | 45→68.425 | active / event:202428 |
| food_reserve | 105451/None | 41.0→67.72 | active / food_reserve |
| rest | 40957/None | 56.80000000000035→64.80000000000035 | active / physiology |
| migration | 35903/1023 | 52→60.0 | active / known_towns |
| food | 25985/None | 52.0→58.9 | active / physiology |
| advancement | 25986/None | 25.4442→57.177645577142854 | selected / self_assessment:4 |
| revenge | 114256/5614 | 30.0→53.985 | active / event:202428 |
| water | 40956/None | 28→36 | active / physiology |
| religious_interest | 25990/5907 | 24.75→26.9388 | active / own_faith |

**Alternativas/gates realmente vistos:**

Need #35904 (`political_pressure`): 1 Solutions entraram em _evaluate; 0 saíram disponíveis. Entrada: `organize`.

| Opção | Alvo | Etapa | Motivo observado | Auditoria/feeding |
| --- | --- | --- | --- | --- |
| organize | None | before_Utility_or_unresolved | cooldown_after_failure | {"pressure":null,"feeding":null} |

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |

Need #30298 (`protection`): 14 Solutions entraram em _evaluate; 14 saíram disponíveis. Entrada: `denounce, confront, threaten, demand_return, warn, insult, call_help, calm, withdraw, flee, defend, forgive, apologize, surrender`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| demand_return | {"target":5614,"destination":null} | 91.9 | {"base":0.2,"honesty":0.10875,"persistence":0.087,"courage":0.06375,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| denounce | {"target":1082,"destination":{"map_id":1070,"x":2,"y":2}} | 90.9 | {"base":0.225,"honesty":0.15225,"vengefulness":0.040999999999999995,"courage":0.06375,"trust":0.0125,"travel":-0.04} | {"feeding":null,"action_pressure":null} |
| flee | {"target":5614,"destination":null} | 82.67857142857143 | {"base":0.175,"fear":0.2,"risk":0.10714285714285715,"courage":-0.10625,"low_health":0.0,"injury":-0.0,"authority":0.0375,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| defend | {"target":5614,"destination":null} | 70.60714285714286 | {"base":0.2,"risk":0.08928571428571429,"courage":0.06375,"defensive":0.0,"injury":-0.0,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| confront | {"target":5614,"destination":null} | 60.597714285714275 | {"base":0.175,"courage":0.1275,"anger":0.023309999999999994,"risk":-0.053571428571428575,"vengefulness":0.030749999999999996,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| warn | {"target":5614,"destination":null} | 50.05 | {"base":0.15,"compassion":0.035,"honesty":0.06525,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| apologize | {"target":5614,"destination":null} | 47.73 | {"base":0.125,"honesty":0.10875,"compassion":0.04375,"culpability":0.0,"anger":-0.038849999999999996,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| withdraw | {"target":5614,"destination":null} | 45.357142857142854 | {"base":0.175,"risk":0.08928571428571429,"compassion":0.02625,"courage":-0.06375,"defensive":-0.0,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| calm | {"target":5614,"destination":null} | 44.838 | {"base":0.175,"compassion":0.0525,"bond":0.02,"anger":-0.023309999999999994,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| call_help | {"target":5614,"destination":null} | 43.2 | {"base":0.125,"fear":0.125,"independence":-0.034,"injury":0.0,"travel":-0.0} | {"feeding":null,"action_pressure":null} |

Need #25986 (`advancement`): 1 Solutions entraram em _evaluate; 1 saíram disponíveis. Entrada: `work`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| work | {"target":null,"destination":{"map_id":1070,"x":3,"y":5}} | 69.0 | {"base":0.25,"diligence":0.095,"physical_depletion":0.0,"travel":-0.0,"no_progress":0.0} | {"feeding":null,"action_pressure":null} |

Need #114256 (`revenge`): 15 Solutions entraram em _evaluate; 15 saíram disponíveis. Entrada: `investigate, denounce, confront, threaten, demand_return, warn, insult, call_help, calm, withdraw, flee, defend, forgive, apologize, surrender`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| investigate | {"target":5614,"destination":{"map_id":1070,"x":3,"y":5}} | 106.4 | {"base":0.225,"vengefulness":0.08199999999999999,"courage":0.17,"independence":0.051000000000000004,"compassion":-0.0175,"temperament":0.0215,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| demand_return | {"target":5614,"destination":null} | 91.9 | {"base":0.2,"honesty":0.10875,"persistence":0.087,"courage":0.06375,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| denounce | {"target":1082,"destination":{"map_id":1070,"x":2,"y":2}} | 90.9 | {"base":0.225,"honesty":0.15225,"vengefulness":0.040999999999999995,"courage":0.06375,"trust":0.0125,"travel":-0.04} | {"feeding":null,"action_pressure":null} |
| flee | {"target":5614,"destination":null} | 88.67857142857143 | {"base":0.175,"fear":0.2,"risk":0.10714285714285715,"courage":-0.10625,"low_health":0.0,"injury":-0.0,"authority":0.0375,"travel":-0.0,"known_reputation":0.03} | {"feeding":null,"action_pressure":null} |
| defend | {"target":5614,"destination":null} | 70.60714285714286 | {"base":0.2,"risk":0.08928571428571429,"courage":0.06375,"defensive":0.0,"injury":-0.0,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| confront | {"target":5614,"destination":null} | 60.597714285714275 | {"base":0.175,"courage":0.1275,"anger":0.023309999999999994,"risk":-0.053571428571428575,"vengefulness":0.030749999999999996,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| withdraw | {"target":5614,"destination":null} | 51.357142857142854 | {"base":0.175,"risk":0.08928571428571429,"compassion":0.02625,"courage":-0.06375,"defensive":-0.0,"travel":-0.0,"known_reputation":0.03} | {"feeding":null,"action_pressure":null} |
| warn | {"target":5614,"destination":null} | 50.05 | {"base":0.15,"compassion":0.035,"honesty":0.06525,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| apologize | {"target":5614,"destination":null} | 47.73 | {"base":0.125,"honesty":0.10875,"compassion":0.04375,"culpability":0.0,"anger":-0.038849999999999996,"travel":-0.0} | {"feeding":null,"action_pressure":null} |
| calm | {"target":5614,"destination":null} | 44.838 | {"base":0.175,"compassion":0.0525,"bond":0.02,"anger":-0.023309999999999994,"travel":-0.0} | {"feeding":null,"action_pressure":null} |

**Escolhas intermediárias:** [{"chosen":{"action":"demand_return","score":91.9,"target":5614,"destination":null,"terms":{"base":0.2,"honesty":0.10875,"persistence":0.087,"courage":0.06375,"travel":-0.0},"feeding":null,"action_pressure":null},"near_scores":[91.9,90.9,82.67857142857143,70.60714285714286,60.597714285714275,50.05,47.73,45.357142857142854],"variation_draws":"não capturados; RNG não consultado pelo observador"}].

**Preparação/substituição posterior:** [].

**Winner final / Goal:** {"winner":{"action":"demand_return","score":91.9,"target":5614,"destination":null,"terms":{"base":0.2,"honesty":0.10875,"persistence":0.087,"courage":0.06375,"travel":-0.0},"feeding":null,"action_pressure":null},"goal":{"id":204705,"need_id":30298,"action":"demand_return","score":91.9,"created_at":149,"target_id":5614,"destination":null,"status":"completed","outcome":"Interação estruturada registrada: demand_return."},"suspended_before":null,"suspended_after":null}.

**Por que outras Needs não foram executadas:** a fila prioriza emergência/priority/ID e para na primeira solucionável, sujeita à continuidade/preparo. Outras pressões retidas: political_pressure#35904(78.89777142857143), food_reserve#105451(67.72), rest#40957(64.80000000000035), migration#35903(60.0), food#25985(58.9), advancement#25986(57.177645577142854), revenge#114256(53.985), water#40956(36), religious_interest#25990(26.9388). Não atribuir score global entre Needs.

**Execução:** {"success":true,"result":[true,"Interação estruturada registrada: demand_return."],"goal_at_entry":{"id":204705,"need_id":30298,"action":"demand_return","score":91.9,"created_at":149,"target_id":5614,"destination":null,"status":"active","outcome":""},"before":{"id":5612,"name":"Bela Luar","hour":149,"alive":true,"profession":"comerciante","lod":"active","position":{"map_id":1070,"x":3,"y":5},"residence":1070,"hp":100,"hunger":48,"thirst":28,"fatigue":56.80000000000035,"money":17,"food":0,"water":0,"local_food":48,"local_water":151,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{"organize":158}},"after":{"id":5612,"name":"Bela Luar","hour":149,"alive":true,"profession":"comerciante","lod":"active","position":{"map_id":1070,"x":3,"y":5},"residence":1070,"hp":100,"hunger":48,"thirst":28,"fatigue":56.80000000000035,"money":17,"food":0,"water":0,"local_food":48,"local_water":151,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{"organize":158}}}.

**Cálculos especializados reais:** [{"system":"lethal_decision","function":"lethal_decisions.LethalDecisionSystem.evaluate","result":{"available":false,"pressure":-97.13,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"protection","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":6.970000000000001,"directed_emotion":8.516200000000001,"commitment":0.0,"sadism":0.0,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":19.25,"moral_restraint":10.44,"fear":27.25,"risk":8.571428571428571,"bond":9.6,"authority_or_witnesses":7.5,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{"pressure":-97.13,"cause":{"severity":0,"grave":false,"causes":[],"facts":[],"confidence":0,"mode":"retributive","confirmed_injury":0}}},{"system":"lethal_decision","function":"lethal_decisions.LethalDecisionSystem.evaluate","result":{"available":false,"pressure":-97.13,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"protection","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":6.970000000000001,"directed_emotion":8.516200000000001,"commitment":0.0,"sadism":0.0,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":19.25,"moral_restraint":10.44,"fear":27.25,"risk":8.571428571428571,"bond":9.6,"authority_or_witnesses":7.5,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{"pressure":-97.13,"cause":{"severity":0,"grave":false,"causes":[],"facts":[],"confidence":0,"mode":"retributive","confirmed_injury":0}}},{"system":"lethal_pressure","function":"lethality.LethalPressure.evaluate","result":{"available":false,"pressure":-97.13,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"protection","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":6.970000000000001,"directed_emotion":8.516200000000001,"commitment":0.0,"sadism":0.0,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":19.25,"moral_restraint":10.44,"fear":27.25,"risk":8.571428571428571,"bond":9.6,"authority_or_witnesses":7.5,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{}},{"system":"lethal_decision","function":"lethal_decisions.LethalDecisionSystem.evaluate","result":{"available":false,"pressure":-97.13,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"revenge","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":6.970000000000001,"directed_emotion":8.516200000000001,"commitment":0.0,"sadism":0.0,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":19.25,"moral_restraint":10.44,"fear":27.25,"risk":8.571428571428571,"bond":9.6,"authority_or_witnesses":7.5,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{"pressure":-97.13,"cause":{"severity":0,"grave":false,"causes":[],"facts":[],"confidence":0,"mode":"retributive","confirmed_injury":0}}},{"system":"lethal_decision","function":"lethal_decisions.LethalDecisionSystem.evaluate","result":{"available":false,"pressure":-97.13,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"revenge","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":6.970000000000001,"directed_emotion":8.516200000000001,"commitment":0.0,"sadism":0.0,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":19.25,"moral_restraint":10.44,"fear":27.25,"risk":8.571428571428571,"bond":9.6,"authority_or_witnesses":7.5,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{"pressure":-97.13,"cause":{"severity":0,"grave":false,"causes":[],"facts":[],"confidence":0,"mode":"retributive","confirmed_injury":0}}},{"system":"lethal_pressure","function":"lethality.LethalPressure.evaluate","result":{"available":false,"pressure":-97.13,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"revenge","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":6.970000000000001,"directed_emotion":8.516200000000001,"commitment":0.0,"sadism":0.0,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":19.25,"moral_restraint":10.44,"fear":27.25,"risk":8.571428571428571,"bond":9.6,"authority_or_witnesses":7.5,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{}}].

| Evento/hora | Actor→target | Emissor | Testemunhas | Contexto |
| --- | --- | --- | --- | --- |
| 204706 / 149 / RestitutionDemanded | 5612→5614 | ["conflicts.ConflictSystem.execute","goals.GoalSystem._execute","goals.GoalSystem.execute"] | [1076,1079,5603,5612,5614,5626,5635] | {"source_fact":202428} |

**Aprendizado aceito durante a decisão (amostra):** [{"npc":1076,"event":204706,"kind":"RestitutionDemanded","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":1079,"event":204706,"kind":"RestitutionDemanded","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":5603,"event":204706,"kind":"RestitutionDemanded","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":5612,"event":204706,"kind":"RestitutionDemanded","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":5614,"event":204706,"kind":"RestitutionDemanded","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":5626,"event":204706,"kind":"RestitutionDemanded","source":null,"firsthand":true,"confidence":100,"latency":0},{"npc":5635,"event":204706,"kind":"RestitutionDemanded","source":null,"firsthand":true,"confidence":100,"latency":0}].

**Recibos posteriores ligados ao mesmo event_id:** [{"event":204706,"kind":"RestitutionDemanded","learned":{"count":7,"first":149,"last":149,"first_people":[1076,1079,5603,5612,5614,5626]}}]. Contagem é operações de aprendizado aceitas, não indivíduos únicos.

**Consequência imediata:** {"id":5612,"name":"Bela Luar","hour":149,"alive":true,"profession":"comerciante","lod":"active","position":{"map_id":1070,"x":3,"y":5},"residence":1070,"hp":100,"hunger":48,"thirst":28,"fatigue":56.80000000000035,"money":17,"food":0,"water":0,"local_food":48,"local_water":151,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{"organize":158}}. **Observação/relações com o alvo ao final:** {"observation_end":{"turn":149,"position":{"map_id":1070,"x":3,"y":5},"hunger":30,"thirst":31,"health":100,"alive":true,"profession":"guarda","weapon_power":10,"injured":0},"relations_end":[{"source_id":5612,"target_id":5614,"kind":"amizade","value":16},{"source_id":5612,"target_id":5614,"kind":"confiança","value":14}]}. Não usar esse estado posterior como entrada antiga nem atribuir consequências futuras sem vínculo causal.

### 47. crime — Cael Vale #3721, h220: steal

**Pressão escolhida:** `food` #15256, prioridade 100, base 100, fonte `physiology`, alvo None. Motivo: Fome.

**Contexto preservado:** {"emergency":true}.

**Entrada:** {"id":3721,"name":"Cael Vale","hour":220,"alive":true,"profession":"lenhador","lod":"active","position":{"map_id":601,"x":1,"y":13},"residence":601,"hp":50,"hunger":100,"thirst":16,"fatigue":100,"money":17,"food":0,"water":0,"local_food":0,"local_water":12,"recoverable_deprivation":50,"starvation_hours":7,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{"fill_water":227,"drink_well":225,"forage":226,"steal_person":231}}.

**Personalidade:** {"honesty":6,"compassion":87,"courage":90,"independence":94,"greed":29,"diligence":41,"family_loyalty":83,"persistence":26,"temperament":51,"vengefulness":27,"ambition":32,"sadism":17}. **Emoções escalares de entrada:** {"anger":0.12,"resentment":0.0,"humiliation":0.0,"desperation":22.199999999999992,"last_updated":219,"last_support":117,"strain":25.164000000000005,"adaptation":0,"last_adapted":0,"stable_material_hours":0,"nested_collections":"LACUNA: cópia rasa; histórico não utilizado"}.

**Conhecimento/locais de entrada:** {"known_places":{"market":{"map_id":601,"x":7,"y":13},"home":{"map_id":601,"x":2,"y":2},"work":{"map_id":601,"x":12,"y":2},"forage":{"map_id":601,"x":1,"y":13},"well_home":{"map_id":601,"x":2,"y":2},"well_rural":{"map_id":601,"x":1,"y":13},"sacred":{"map_id":601,"x":7,"y":1}},"known_towns":[601,648,3],"route_knowledge_count":2,"knowledge_ids_before":[261995,262009,262010,262018,262021,263115,263122,263123,263130,264207,264210,264211,264226,264227,264697,264698,265236,265244,252073,265859,267757,268097,268096,270264,271332,272465,272467,244021,274930,274931,276167,277043,279313,280614,280620,280621,280622,281050,281643,281645,281658,281683,281684,281827,281829,282660,282662,283134,283749,283751,283752,283754,283756,283769,283775,283785,284334,284872,284875,284882,284885,284890,284892,284894],"market_observation":{"turn":219,"town_id":601,"stock":{"food":0,"grain":0,"water":18,"iron":120,"wood":120},"temporary_work":false,"offers_expire_at":243,"training_offer":null,"price":2,"price_turn":72}}.

**Fatos-fonte retidos após percepção:** [{"event_id":283775,"kind":"FamilyConcern","actor_id":3721,"target_id":3718,"location":{"map_id":601,"x":1,"y":13},"turn":219,"description":"Cael Vale percebeu a privação de Bela Vale.","confidence":100,"required_trust":0,"source_id":null,"source_kind":"direct","context":{"observed_need":100}}].

| Need | ID/alvo | Base→prioridade | Estado/fonte |
| --- | --- | --- | --- |
| food | 15256/None | 100→100 | active / physiology |
| rest | 38496/None | 100→100 | active / physiology |
| family | 91413/3718 | 67.6→97.6078 | blocked / event:283775 |
| food_reserve | 15255/None | 41.0→72.56164383561644 | active / food_reserve |
| recovery | 171637/3721 | 55→63.0 | active / own_physiology |

**Alternativas/gates realmente vistos:**

Need #15256 (`food`): 5 Solutions entraram em _evaluate; 2 saíram disponíveis. Entrada: `buy_food, steal, forage, steal_person, steal_person`.

| Opção | Alvo | Etapa | Motivo observado | Auditoria/feeding |
| --- | --- | --- | --- | --- |
| forage | None | before_Utility_or_unresolved | cooldown_after_failure | {"pressure":null,"feeding":null} |
| steal_person | 3586 | before_Utility_or_unresolved | cooldown_after_failure | {"pressure":null,"feeding":null} |
| steal_person | 3609 | before_Utility_or_unresolved | cooldown_after_failure | {"pressure":null,"feeding":null} |

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| steal | {"target":null,"destination":{"map_id":601,"x":7,"y":13}} | 73.36039666666667 | {"base":0.35,"greed":0.04833333333333333,"honesty":-0.03,"courage":0.045,"travel":-0.06,"pressure_moral_tolerance":0.013468650000000002} | {"feeding":{"EstimatedTimeUntilFoodConsumed":8,"EstimatedSurvivalMargin":18,"economically_viable":true,"survival_viable":true,"reason":null,"known_conditions":["UnknownPrice","DistantProduct"]},"action_pressure":null} |
| buy_food | {"target":null,"destination":{"map_id":601,"x":7,"y":13}} | 64.2 | {"base":0.375,"honesty":0.006,"travel":-0.06} | {"feeding":{"EstimatedTimeUntilFoodConsumed":8,"EstimatedSurvivalMargin":18,"economically_viable":true,"survival_viable":true,"reason":null,"known_conditions":["UnknownPrice","DistantProduct"]},"action_pressure":null} |

Need #91413 (`family`): 0 Solutions entraram em _evaluate; 0 saíram disponíveis. Entrada: ``.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |

**Escolhas intermediárias:** [{"chosen":{"action":"steal","score":73.36039666666667,"target":null,"destination":{"map_id":601,"x":7,"y":13},"terms":{"base":0.35,"greed":0.04833333333333333,"honesty":-0.03,"courage":0.045,"travel":-0.06,"pressure_moral_tolerance":0.013468650000000002},"feeding":{"EstimatedTimeUntilFoodConsumed":8,"EstimatedSurvivalMargin":18,"economically_viable":true,"survival_viable":true,"reason":null,"known_conditions":["UnknownPrice","DistantProduct"]},"action_pressure":null},"near_scores":[73.36039666666667,64.2],"variation_draws":"não capturados; RNG não consultado pelo observador"}].

**Preparação/substituição posterior:** [].

**Winner final / Goal:** {"winner":{"action":"steal","score":73.36039666666667,"target":null,"destination":{"map_id":601,"x":7,"y":13},"terms":{"base":0.35,"greed":0.04833333333333333,"honesty":-0.03,"courage":0.045,"travel":-0.06,"pressure_moral_tolerance":0.013468650000000002},"feeding":{"EstimatedTimeUntilFoodConsumed":8,"EstimatedSurvivalMargin":18,"economically_viable":true,"survival_viable":true,"reason":null,"known_conditions":["UnknownPrice","DistantProduct"]},"action_pressure":null},"goal":{"id":284895,"need_id":15256,"action":"steal","score":73.36039666666667,"created_at":220,"target_id":null,"destination":{"map_id":601,"x":7,"y":13},"status":"active","outcome":""},"suspended_before":null,"suspended_after":null}.

**Por que outras Needs não foram executadas:** a fila prioriza emergência/priority/ID e para na primeira solucionável, sujeita à continuidade/preparo. Outras pressões retidas: rest#38496(100), family#91413(97.6078), food_reserve#15255(72.56164383561644), recovery#171637(63.0). Não atribuir score global entre Needs.

**Execução:** execute não foi chamado neste trace. A Goal pode ter iniciado/continuado deslocamento; o snapshot e a posição posterior delimitam essa conclusão.

**Cálculos especializados reais:** [].

**Evento:** nenhum evento retido durante esta decisão. Isso pode significar movimento/efeito sem evento; não implica falha.

**Aprendizado aceito durante a decisão (amostra):** [].

**Recibos posteriores ligados ao mesmo event_id:** []. Contagem é operações de aprendizado aceitas, não indivíduos únicos.

**Consequência imediata:** {"id":3721,"name":"Cael Vale","hour":220,"alive":true,"profession":"lenhador","lod":"active","position":{"map_id":601,"x":2,"y":13},"residence":601,"hp":50,"hunger":100,"thirst":16,"fatigue":100,"money":17,"food":0,"water":0,"local_food":0,"local_water":12,"recoverable_deprivation":50,"starvation_hours":7,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{"fill_water":227,"drink_well":225,"forage":226,"steal_person":231}}. **Observação/relações com o alvo ao final:** {"observation_end":null,"relations_end":[]}. Não usar esse estado posterior como entrada antiga nem atribuir consequências futuras sem vínculo causal.

### 48. faction — Aldren Hammer #1173, h140: invite_person

**Pressão escolhida:** `organizational_access` #20146, prioridade 61.8236, base 53, fonte `organization`, alvo 1176. Motivo: Procurar pessoas e recursos para a organização.

**Contexto preservado:** {"faction_id":1176}.

**Entrada:** {"id":1173,"name":"Aldren Hammer","hour":140,"alive":true,"profession":"caçador","lod":"local","position":{"map_id":396,"x":1,"y":5},"residence":302,"hp":100,"hunger":31,"thirst":55,"fatigue":100,"money":1,"food":1,"water":0,"local_food":50,"local_water":144,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{"invite_person":140,"denounce":143}}.

**Personalidade:** {"honesty":12,"compassion":81,"courage":11,"independence":30,"greed":77,"diligence":61,"family_loyalty":64,"persistence":89,"temperament":72,"vengefulness":23,"ambition":49,"sadism":0}. **Emoções escalares de entrada:** {"anger":0.0,"resentment":0.0,"humiliation":0.0,"desperation":13.049999999999994,"last_updated":137,"last_support":40,"strain":31.972499999999997,"adaptation":0,"last_adapted":0,"stable_material_hours":0,"nested_collections":"LACUNA: cópia rasa; histórico não utilizado"}.

**Conhecimento/locais de entrada:** {"known_places":{"home":{"map_id":1170,"x":5,"y":5},"work":{"map_id":1170,"x":5,"y":5},"forage":{"map_id":396,"x":1,"y":5},"sacred":{"map_id":1170,"x":5,"y":1},"market":{"map_id":396,"x":3,"y":5},"well_rural":{"map_id":396,"x":1,"y":5}},"known_towns":[302,396,367],"route_knowledge_count":6,"knowledge_ids_before":[159981,94672,160653,161104,161108,161109,161111,161112,161113,161114,161119,163041,163043,163045,163127,163518,163520,164752,164755,164758,166753,167252,167258,168806,171441,171446,172781,172785,174552,174553,174555,174556,174557,175030,168801,141520,138088,176208,176218,177807,177809,178208,178210,179288,179298,180868,181294,181296,181300,164749,182441,184096,184101,184102,184103,184104,184212,184551,184558,187438,187440,187528,187868,85528],"market_observation":{"turn":137,"town_id":396,"stock":{"food":51,"grain":67,"water":146,"iron":32,"wood":72},"temporary_work":false,"offers_expire_at":161,"training_offer":null,"price":2,"price_turn":137}}.

**Fatos-fonte retidos após percepção:** [].

| Need | ID/alvo | Base→prioridade | Estado/fonte |
| --- | --- | --- | --- |
| rest | 44830/None | 100→100 | active / physiology |
| money | 20140/None | 53.75→75.03 | active / economy |
| protection | 63328/1173 | 45→66.3 | blocked / event:159973 |
| organizational_access | 20146/1176 | 53→61.8236 | active / organization |
| migration | 63430/367 | 52→58.93 | active / known_towns |
| water | 39353/None | 55→57.25 | active / physiology |
| organizational_survival | 20144/1173 | 45→53.0 | active / faction:1176 |
| advancement | 20142/None | 23.1798→47.47793139428571 | blocked / aspiration:wealth |
| religious_interest | 20143/5909 | 32.75→41.8462 | active / own_faith |
| food_reserve | 166839/None | 36.2→38.23225806451613 | active / food_reserve |

**Alternativas/gates realmente vistos:**

Need #44830 (`rest`): 1 Solutions entraram em _evaluate; 0 saíram disponíveis. Entrada: `sleep`.

| Opção | Alvo | Etapa | Motivo observado | Auditoria/feeding |
| --- | --- | --- | --- | --- |
| sleep | None | before_Utility_or_unresolved | destination_other_map | {"pressure":null,"feeding":null} |

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |

Need #20140 (`money`): 0 Solutions entraram em _evaluate; 0 saíram disponíveis. Entrada: ``.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |

Need #63328 (`protection`): 1 Solutions entraram em _evaluate; 0 saíram disponíveis. Entrada: `avoid_threat`.

| Opção | Alvo | Etapa | Motivo observado | Auditoria/feeding |
| --- | --- | --- | --- | --- |
| avoid_threat | None | before_Utility_or_unresolved | destination_other_map | {"pressure":null,"feeding":null} |

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |

Need #20146 (`organizational_access`): 1 Solutions entraram em _evaluate; 1 saíram disponíveis. Entrada: `invite_person`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| invite_person | {"target":1176,"destination":{"map_id":396,"x":3,"y":5}} | 51.0 | {"base":0.275,"travel":-0.02} | {"feeding":null,"action_pressure":null} |

Need #63328 (`protection`): 1 Solutions entraram em _evaluate; 0 saíram disponíveis. Entrada: `avoid_threat`.

| Opção | Alvo | Etapa | Motivo observado | Auditoria/feeding |
| --- | --- | --- | --- | --- |
| avoid_threat | None | before_Utility_or_unresolved | destination_other_map | {"pressure":null,"feeding":null} |

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |

Need #20142 (`advancement`): 0 Solutions entraram em _evaluate; 0 saíram disponíveis. Entrada: ``.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |

**Escolhas intermediárias:** [{"chosen":{"action":"invite_person","score":51.0,"target":1176,"destination":{"map_id":396,"x":3,"y":5},"terms":{"base":0.275,"travel":-0.02},"feeding":null,"action_pressure":null},"near_scores":[51.0],"variation_draws":"não capturados; RNG não consultado pelo observador"}].

**Preparação/substituição posterior:** [].

**Winner final / Goal:** {"winner":{"action":"invite_person","score":51.0,"target":1176,"destination":{"map_id":396,"x":3,"y":5},"terms":{"base":0.275,"travel":-0.02},"feeding":null,"action_pressure":null},"goal":{"id":191350,"need_id":20146,"action":"invite_person","score":51.0,"created_at":140,"target_id":1176,"destination":{"map_id":396,"x":3,"y":5},"status":"failed","outcome":"Nenhum candidato local disponível e coerente."},"suspended_before":null,"suspended_after":null}.

**Por que outras Needs não foram executadas:** a fila prioriza emergência/priority/ID e para na primeira solucionável, sujeita à continuidade/preparo. Outras pressões retidas: rest#44830(100), money#20140(75.03), protection#63328(66.3), migration#63430(58.93), water#39353(57.25), organizational_survival#20144(53.0), advancement#20142(47.47793139428571), religious_interest#20143(41.8462), food_reserve#166839(38.23225806451613). Não atribuir score global entre Needs.

**Execução:** {"success":false,"result":[false,"Nenhum candidato local disponível e coerente."],"goal_at_entry":{"id":191350,"need_id":20146,"action":"invite_person","score":51.0,"created_at":140,"target_id":1176,"destination":{"map_id":396,"x":3,"y":5},"status":"active","outcome":""},"before":{"id":1173,"name":"Aldren Hammer","hour":140,"alive":true,"profession":"caçador","lod":"local","position":{"map_id":396,"x":3,"y":5},"residence":302,"hp":100,"hunger":31,"thirst":55,"fatigue":100,"money":1,"food":1,"water":0,"local_food":50,"local_water":144,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{"denounce":143}},"after":{"id":1173,"name":"Aldren Hammer","hour":140,"alive":true,"profession":"caçador","lod":"local","position":{"map_id":396,"x":3,"y":5},"residence":302,"hp":100,"hunger":31,"thirst":55,"fatigue":100,"money":1,"food":1,"water":0,"local_food":50,"local_water":144,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{"denounce":143}}}.

**Cálculos especializados reais:** [{"system":"lethal_decision","function":"lethal_decisions.LethalDecisionSystem.evaluate","result":{"available":false,"pressure":-74.48,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"protection","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":3.91,"directed_emotion":0.0,"commitment":0.0,"sadism":0.0,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":44.550000000000004,"moral_restraint":1.44,"fear":0.0,"risk":2.4000000000000004,"bond":0.0,"authority_or_witnesses":0.0,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{"pressure":-74.48,"cause":{"severity":0,"grave":false,"causes":[],"facts":[],"confidence":0,"mode":"retributive","confirmed_injury":0}}},{"system":"lethal_decision","function":"lethal_decisions.LethalDecisionSystem.evaluate","result":{"available":false,"pressure":-74.48,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"protection","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":3.91,"directed_emotion":0.0,"commitment":0.0,"sadism":0.0,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":44.550000000000004,"moral_restraint":1.44,"fear":0.0,"risk":2.4000000000000004,"bond":0.0,"authority_or_witnesses":0.0,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{"pressure":-74.48,"cause":{"severity":0,"grave":false,"causes":[],"facts":[],"confidence":0,"mode":"retributive","confirmed_injury":0}}},{"system":"lethal_pressure","function":"lethality.LethalPressure.evaluate","result":{"available":false,"pressure":-74.48,"mode":"retributive","confidence":0,"known_facts":[],"source_fact":null,"commitment_id":null,"motive":"protection","world_pressure":0,"grave_basis":"none","blocking":["insufficient_pressure","low_confidence","inhibition"],"positive_factors":{"instigation":0.0,"vengefulness":3.91,"directed_emotion":0.0,"commitment":0.0,"sadism":0.0,"death_affinity":0.0,"failed_repair":0},"barriers":{"harm_aversion":44.550000000000004,"moral_restraint":1.44,"fear":0.0,"risk":2.4000000000000004,"bond":0.0,"authority_or_witnesses":0.0,"uncertain_authorship":50.0,"available_nonlethal_alternative":10},"decision_id":null,"rumination":0,"current_commitment_strength":0,"commitment_intensity":0},"inputs":{}}].

**Evento:** nenhum evento retido durante esta decisão. Isso pode significar movimento/efeito sem evento; não implica falha.

**Aprendizado aceito durante a decisão (amostra):** [].

**Recibos posteriores ligados ao mesmo event_id:** []. Contagem é operações de aprendizado aceitas, não indivíduos únicos.

**Consequência imediata:** {"id":1173,"name":"Aldren Hammer","hour":140,"alive":true,"profession":"caçador","lod":"local","position":{"map_id":396,"x":3,"y":5},"residence":302,"hp":100,"hunger":31,"thirst":55,"fatigue":100,"money":1,"food":1,"water":0,"local_food":50,"local_water":144,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{"denounce":143,"invite_person":152}}. **Observação/relações com o alvo ao final:** {"observation_end":null,"relations_end":[{"source_id":1173,"target_id":1176,"kind":"lealdade","value":100}]}. Não usar esse estado posterior como entrada antiga nem atribuir consequências futuras sem vínculo causal.

### 49. family — Bela Arven #5206, h75: check_relative

**Pressão escolhida:** `family` #95846, prioridade 74.70599999999999, base 57.099999999999994, fonte `event:95845`, alvo 5209. Motivo: Privação de familiar percebida em encontro.

**Contexto preservado:** {"mode":"care","source_event":95845,"known_location":{"map_id":958,"x":2,"y":2},"diagnostic":{"reason":"Selected","competing":null,"turn":75}}.

**Entrada:** {"id":5206,"name":"Bela Arven","hour":75,"alive":true,"profession":"ferreiro","lod":"local","position":{"map_id":958,"x":2,"y":5},"residence":958,"hp":100,"hunger":44,"thirst":60,"fatigue":39.00000000000014,"money":8,"food":0,"water":0,"local_food":128,"local_water":153,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{}}.

**Personalidade:** {"honesty":21,"compassion":6,"courage":34,"independence":26,"greed":60,"diligence":41,"family_loyalty":52,"persistence":9,"temperament":15,"vengefulness":7,"ambition":75,"sadism":0}. **Emoções escalares de entrada:** {"anger":0.0,"resentment":0.0,"humiliation":0.0,"desperation":2.25,"last_updated":72,"last_support":-10000,"strain":4.702500000000001,"adaptation":0,"last_adapted":0,"stable_material_hours":0,"nested_collections":"LACUNA: cópia rasa; histórico não utilizado"}.

**Conhecimento/locais de entrada:** {"known_places":{"market":{"map_id":958,"x":3,"y":5},"home":{"map_id":958,"x":2,"y":2},"work":{"map_id":958,"x":4,"y":2},"forage":{"map_id":958,"x":1,"y":5},"well_home":{"map_id":958,"x":2,"y":2},"well_rural":{"map_id":958,"x":1,"y":5},"sacred":{"map_id":958,"x":3,"y":1}},"known_towns":[958,911,864],"route_knowledge_count":2,"knowledge_ids_before":[10933,10934,13218,13219,13220,13221,13217,13216,13215,13214,13213,16106,19361,30209,33964,33968,33971,33976,35801,38878,38880,40806,44364,45890,45891,25875,24406,49090,53507,53513,53514,54972,44366,57968,59295,59300,45899,47887,16121,69887,69889,69890,69893,71045,68966,19346,74626,47891,68962,27615,80574,80583,84258,84261,84263,91772,95845,99122,19343,104573,84265,28805,107439,111490],"market_observation":{"turn":51,"town_id":958,"stock":{"food":130,"grain":95,"water":156,"iron":64,"wood":54},"temporary_work":false,"offers_expire_at":75,"training_offer":null,"price":2,"price_turn":36}}.

**Fatos-fonte retidos após percepção:** [{"event_id":95845,"kind":"FamilyConcern","actor_id":5206,"target_id":5209,"location":{"map_id":958,"x":2,"y":2},"turn":54,"description":"Bela Arven percebeu a privação de Silas Arven.","confidence":100,"required_trust":0,"source_id":null,"source_kind":"direct","context":{"observed_need":57}}].

| Need | ID/alvo | Base→prioridade | Estado/fonte |
| --- | --- | --- | --- |
| family | 95846/5209 | 57.099999999999994→74.70599999999999 | selected / event:95845 |
| food_reserve | 33961/None | 41.0→64.29411764705883 | active / food_reserve |
| water | 44360/None | 60→62.25 | active / physiology |
| advancement | 33965/None | 25.761→57.01633188571428 | blocked / aspiration:wealth |
| political_pressure | 99119/None | 49.0→54.4468 | active / own_shared_problem |
| money | 33962/None | 36.75→51.016 | active / economy |
| rest | 44361/None | 39.00000000000014→47.00000000000014 | active / physiology |
| food | 38875/None | 46.0→46.45 | active / physiology |

**Alternativas/gates realmente vistos:**

Need #95846 (`family`): 1 Solutions entraram em _evaluate; 1 saíram disponíveis. Entrada: `check_relative`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| check_relative | {"target":5209,"destination":{"map_id":958,"x":2,"y":2}} | 68.5 | {"base":0.275,"independence":0.0325,"family_loyalty":0.065,"travel":-0.03} | {"feeding":null,"action_pressure":null} |

Need #95846 (`family`): 1 Solutions entraram em _evaluate; 1 saíram disponíveis. Entrada: `check_relative`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| check_relative | {"target":5209,"destination":{"map_id":958,"x":2,"y":2}} | 68.5 | {"base":0.275,"independence":0.0325,"family_loyalty":0.065,"travel":-0.03} | {"feeding":null,"action_pressure":null} |

Need #33965 (`advancement`): 1 Solutions entraram em _evaluate; 1 saíram disponíveis. Entrada: `work`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| work | {"target":null,"destination":{"map_id":958,"x":4,"y":2}} | 24.5 | {"base":0.25,"diligence":0.1025,"physical_depletion":0.0,"travel":-0.05,"no_progress":-0.18} | {"feeding":null,"action_pressure":null} |

**Escolhas intermediárias:** [{"chosen":{"action":"check_relative","score":68.5,"target":5209,"destination":{"map_id":958,"x":2,"y":2},"terms":{"base":0.275,"independence":0.0325,"family_loyalty":0.065,"travel":-0.03},"feeding":null,"action_pressure":null},"near_scores":[68.5],"variation_draws":"não capturados; RNG não consultado pelo observador"}].

**Preparação/substituição posterior:** [].

**Winner final / Goal:** {"winner":{"action":"check_relative","score":68.5,"target":5209,"destination":{"map_id":958,"x":2,"y":2},"terms":{"base":0.275,"independence":0.0325,"family_loyalty":0.065,"travel":-0.03},"feeding":null,"action_pressure":null},"goal":{"id":117654,"need_id":95846,"action":"check_relative","score":68.5,"created_at":75,"target_id":5209,"destination":{"map_id":958,"x":2,"y":2},"status":"active","outcome":""},"suspended_before":null,"suspended_after":null}.

**Por que outras Needs não foram executadas:** a fila prioriza emergência/priority/ID e para na primeira solucionável, sujeita à continuidade/preparo. Outras pressões retidas: food_reserve#33961(64.29411764705883), water#44360(62.25), advancement#33965(57.01633188571428), political_pressure#99119(54.4468), money#33962(51.016), rest#44361(47.00000000000014), food#38875(46.45). Não atribuir score global entre Needs.

**Execução:** execute não foi chamado neste trace. A Goal pode ter iniciado/continuado deslocamento; o snapshot e a posição posterior delimitam essa conclusão.

**Cálculos especializados reais:** [].

**Evento:** nenhum evento retido durante esta decisão. Isso pode significar movimento/efeito sem evento; não implica falha.

**Aprendizado aceito durante a decisão (amostra):** [].

**Recibos posteriores ligados ao mesmo event_id:** []. Contagem é operações de aprendizado aceitas, não indivíduos únicos.

**Consequência imediata:** {"id":5206,"name":"Bela Arven","hour":75,"alive":true,"profession":"ferreiro","lod":"local","position":{"map_id":958,"x":2,"y":2},"residence":958,"hp":100,"hunger":44,"thirst":60,"fatigue":39.00000000000014,"money":8,"food":0,"water":0,"local_food":128,"local_water":153,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{}}. **Observação/relações com o alvo ao final:** {"observation_end":{"turn":72,"position":{"map_id":958,"x":2,"y":2},"hunger":53,"thirst":54,"health":100,"alive":true,"profession":"mineiro","weapon_power":4,"injured":0},"relations_end":[{"source_id":5206,"target_id":5209,"kind":"pai_de","value":100},{"source_id":5206,"target_id":5209,"kind":"amizade","value":22},{"source_id":5206,"target_id":5209,"kind":"confiança","value":70}]}. Não usar esse estado posterior como entrada antiga nem atribuir consequências futuras sem vínculo causal.

### 50. food — Darin Vale #2944, h214: buy_food

**Pressão escolhida:** `food` #38303, prioridade 100, base 100, fonte `physiology`, alvo None. Motivo: Fome.

**Contexto preservado:** {"emergency":true}.

**Entrada:** {"id":2944,"name":"Darin Vale","hour":214,"alive":true,"profession":"agricultor","lod":"active","position":{"map_id":414,"x":2,"y":8},"residence":414,"hp":100,"hunger":80,"thirst":71,"fatigue":85.20000000000043,"money":4,"food":0,"water":2,"local_food":11,"local_water":89,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{}}.

**Personalidade:** {"honesty":63,"compassion":31,"courage":67,"independence":14,"greed":17,"diligence":33,"family_loyalty":81,"persistence":94,"temperament":40,"vengefulness":6,"ambition":54,"sadism":1}. **Emoções escalares de entrada:** {"anger":15.300000000000045,"resentment":23.699999999999992,"humiliation":11.099999999999977,"desperation":3.6000000000000005,"last_updated":213,"last_support":144,"strain":7.686000000000001,"adaptation":0,"last_adapted":0,"stable_material_hours":0,"nested_collections":"LACUNA: cópia rasa; histórico não utilizado"}.

**Conhecimento/locais de entrada:** {"known_places":{"market":{"map_id":414,"x":5,"y":9},"home":{"map_id":414,"x":2,"y":2},"work":{"map_id":414,"x":1,"y":9},"forage":{"map_id":414,"x":1,"y":9},"well_home":{"map_id":414,"x":2,"y":2},"well_rural":{"map_id":414,"x":1,"y":9},"sacred":{"map_id":414,"x":5,"y":1}},"known_towns":[414,302],"route_knowledge_count":2,"knowledge_ids_before":[172788,223029,223765,225866,225891,225893,227210,227220,231638,231646,231647,231648,231649,231650,203064,212637,238934,238936,240087,240684,242262,242264,242265,242266,243409,184114,245735,245736,245738,247043,249456,249457,249459,249460,250754,251399,170950,207285,253429,253431,253432,254194,254722,255769,255774,255775,255780,255789,256885,256897,256900,256904,257489,257904,257906,258829,258833,258847,184563,195327,259897,269620,269621,250764],"market_observation":{"turn":198,"town_id":414,"stock":{"food":8,"grain":114,"water":142,"iron":120,"wood":100},"temporary_work":true,"offers_expire_at":222,"training_offer":null,"price":3,"price_turn":148}}.

**Fatos-fonte retidos após percepção:** [{"event_id":172788,"kind":"AbsenceNoticed","actor_id":2944,"target_id":null,"location":{"map_id":414,"x":2,"y":2},"turn":123,"description":"Darin Vale não localiza um familiar há 42 horas.","confidence":100,"required_trust":0,"source_id":null,"source_kind":"direct","context":{"last_seen":81,"relative_id":2938}},{"event_id":253431,"kind":"FamilyConcern","actor_id":2944,"target_id":2941,"location":{"map_id":414,"x":1,"y":9},"turn":192,"description":"Darin Vale percebeu a privação de Marie Vale.","confidence":100,"required_trust":0,"source_id":null,"source_kind":"direct","context":{"observed_need":69}}].

| Need | ID/alvo | Base→prioridade | Estado/fonte |
| --- | --- | --- | --- |
| food | 38303/None | 100→100 | active / physiology |
| rest | 52988/None | 85.20000000000043→93.20000000000043 | active / physiology |
| family | 101723/2941 | 60.7→88.73382857142857 | selected / event:253431 |
| water | 43712/None | 71→79 | active / physiology |
| family | 98692/2938 | 47.0→76.80272000000001 | selected / event:172788 |
| organizational_survival | 107965/3013 | 55.93300000000001→67.61640000000001 | active / group:95295 |
| food_reserve | 52987/None | 41.0→65.7304347826087 | active / food_reserve |
| money | 193165/None | 45.041666666666664→59.961666666666666 | active / economy |
| political_pressure | 105909/None | 46.141666666666666→56.67706666666667 | active / own_shared_problem |

**Alternativas/gates realmente vistos:**

Need #38303 (`food`): 5 Solutions entraram em _evaluate; 5 saíram disponíveis. Entrada: `buy_food, steal, forage, work_for_food, temporary_service`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| buy_food | {"target":null,"destination":{"map_id":414,"x":5,"y":9}} | 79.60000000000001 | {"base":0.375,"honesty":0.063,"travel":-0.04} | {"feeding":{"EstimatedTimeUntilFoodConsumed":6,"EstimatedSurvivalMargin":43,"economically_viable":true,"survival_viable":true,"reason":null,"known_conditions":["UnknownPrice","DistantProduct"]},"action_pressure":null} |
| work_for_food | {"target":null,"destination":{"map_id":414,"x":1,"y":9}} | 49.25 | {"base":0.225,"diligence":0.04125,"physical_depletion":0.0,"travel":-0.02} | {"feeding":{"EstimatedTimeUntilFoodConsumed":4,"EstimatedSurvivalMargin":43,"economically_viable":true,"survival_viable":true,"reason":null,"known_conditions":["UnknownPrice","DistantProduct"]},"action_pressure":null} |
| temporary_service | {"target":null,"destination":{"map_id":414,"x":5,"y":9}} | 48.35 | {"base":0.225,"diligence":0.04125,"compassion":0.0155,"physical_depletion":0.0,"travel":-0.04} | {"feeding":{"EstimatedTimeUntilFoodConsumed":6,"EstimatedSurvivalMargin":43,"economically_viable":true,"survival_viable":true,"reason":null,"known_conditions":["UnknownPrice","DistantProduct"]},"action_pressure":null} |
| forage | {"target":null,"destination":{"map_id":414,"x":1,"y":9}} | 38.0 | {"base":0.175,"independence":0.035,"hunter":0.0,"travel":-0.02} | {"feeding":{"EstimatedTimeUntilFoodConsumed":4,"EstimatedSurvivalMargin":43,"economically_viable":true,"survival_viable":true,"reason":null,"known_conditions":["UnknownPrice","DistantProduct"]},"action_pressure":null} |
| steal | {"target":null,"destination":{"map_id":414,"x":5,"y":9}} | 13.79604770238095 | {"base":0.35,"greed":0.02833333333333334,"honesty":-0.315,"courage":0.0335,"travel":-0.04,"pressure_moral_tolerance":0.01214690517857143} | {"feeding":{"EstimatedTimeUntilFoodConsumed":6,"EstimatedSurvivalMargin":43,"economically_viable":true,"survival_viable":true,"reason":null,"known_conditions":["UnknownPrice","DistantProduct"]},"action_pressure":null} |

Need #101723 (`family`): 1 Solutions entraram em _evaluate; 1 saíram disponíveis. Entrada: `check_relative`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| check_relative | {"target":2941,"destination":{"map_id":414,"x":1,"y":9}} | 74.75 | {"base":0.275,"independence":0.0175,"family_loyalty":0.10125,"travel":-0.02} | {"feeding":null,"action_pressure":null} |

Need #98692 (`family`): 1 Solutions entraram em _evaluate; 1 saíram disponíveis. Entrada: `search_area`.

Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.

| Ação | Alvo/destino | Score | Terms reais | Estimação/capacidade |
| --- | --- | --- | --- | --- |
| search_area | {"target":2938,"destination":{"map_id":414,"x":5,"y":9}} | 68.2025 | {"base":0.275,"persistence":0.1175,"courage":0.05025,"travel":-0.04,"action_pressure":0.0282625,"no_progress":-0.09} | {"feeding":null,"action_pressure":{"eligible":true,"world_pressure":47.0,"action_pressure":22.61,"eligibility_causes":["event:172788"],"source_facts":[172788],"capacity":43.2,"perceived_capacity":49.08,"major_barriers":[],"selected_alternative":"search_area"}} |

**Escolhas intermediárias:** [{"chosen":{"action":"buy_food","score":79.60000000000001,"target":null,"destination":{"map_id":414,"x":5,"y":9},"terms":{"base":0.375,"honesty":0.063,"travel":-0.04},"feeding":{"EstimatedTimeUntilFoodConsumed":6,"EstimatedSurvivalMargin":43,"economically_viable":true,"survival_viable":true,"reason":null,"known_conditions":["UnknownPrice","DistantProduct"]},"action_pressure":null},"near_scores":[79.60000000000001,49.25,48.35,38.0,13.79604770238095],"variation_draws":"não capturados; RNG não consultado pelo observador"}].

**Preparação/substituição posterior:** [].

**Winner final / Goal:** {"winner":{"action":"buy_food","score":79.60000000000001,"target":null,"destination":{"map_id":414,"x":5,"y":9},"terms":{"base":0.375,"honesty":0.063,"travel":-0.04},"feeding":{"EstimatedTimeUntilFoodConsumed":6,"EstimatedSurvivalMargin":43,"economically_viable":true,"survival_viable":true,"reason":null,"known_conditions":["UnknownPrice","DistantProduct"]},"action_pressure":null},"goal":{"id":273118,"need_id":38303,"action":"buy_food","score":67.6,"created_at":210,"target_id":null,"destination":{"map_id":414,"x":5,"y":9},"status":"active","outcome":""},"suspended_before":null,"suspended_after":null}.

**Por que outras Needs não foram executadas:** a fila prioriza emergência/priority/ID e para na primeira solucionável, sujeita à continuidade/preparo. Outras pressões retidas: rest#52988(93.20000000000043), family#101723(88.73382857142857), water#43712(79), family#98692(76.80272000000001), organizational_survival#107965(67.61640000000001), food_reserve#52987(65.7304347826087), money#193165(59.961666666666666), political_pressure#105909(56.67706666666667). Não atribuir score global entre Needs.

**Execução:** execute não foi chamado neste trace. A Goal pode ter iniciado/continuado deslocamento; o snapshot e a posição posterior delimitam essa conclusão.

**Cálculos especializados reais:** [{"system":"capacity","function":"action_pressure.ActionPressureSystem.assess","result":{"eligible":true,"world_pressure":47.0,"action_pressure":22.61,"eligibility_causes":["event:172788"],"source_facts":[172788],"capacity":43.2,"perceived_capacity":49.08,"major_barriers":[],"selected_alternative":"search_area"},"inputs":{}}].

**Evento:** nenhum evento retido durante esta decisão. Isso pode significar movimento/efeito sem evento; não implica falha.

**Aprendizado aceito durante a decisão (amostra):** [].

**Recibos posteriores ligados ao mesmo event_id:** []. Contagem é operações de aprendizado aceitas, não indivíduos únicos.

**Consequência imediata:** {"id":2944,"name":"Darin Vale","hour":214,"alive":true,"profession":"agricultor","lod":"active","position":{"map_id":414,"x":2,"y":9},"residence":414,"hp":100,"hunger":80,"thirst":71,"fatigue":85.20000000000043,"money":4,"food":0,"water":2,"local_food":11,"local_water":89,"recoverable_deprivation":0,"starvation_hours":0,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{}}. **Observação/relações com o alvo ao final:** {"observation_end":null,"relations_end":[]}. Não usar esse estado posterior como entrada antiga nem atribuir consequências futuras sem vínculo causal.

## Mortes: registros e limites da reconstrução

Cada morte tem registro final e duas decisões recentes retidas; estas são precedência temporal, não prova de que só essas decisões causaram a morte. O conjunto completo está em traces.death_cases, com estado/posses/recursos locais no instante.

### Caso hunger: NPC #4803, h139

Registro: {"turn":139,"name":"Silas Kars","profession":"mineiro","town_id":864,"cause":"hunger","health":0,"hunger":100,"thirst":91,"fatigue":100,"food":0,"water":1,"last_meal":71,"last_drink":121,"recoverable_deprivation_damage":100,"damage_by_origin":{"hunger":88,"both":12},"last_successful_action":{"action":"drink","turn":121},"goal":"ask_meal","destination":null,"known_water_sources":[{"map_id":864,"x":7,"y":13},{"map_id":864,"x":2,"y":2},{"map_id":864,"x":1,"y":13}],"distance_to_water":0,"event_id":189882}.

Estado pré-fechamento de morte: {"id":4803,"name":"Silas Kars","hour":139,"alive":true,"profession":"mineiro","lod":"active","position":{"map_id":864,"x":1,"y":13},"residence":864,"hp":0,"hunger":100,"thirst":91,"fatigue":100,"money":3,"food":0,"water":1,"local_food":5,"local_water":0,"recoverable_deprivation":100,"starvation_hours":34,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{"forage_meal":147,"person_meal":148,"steal_person":149,"ask_meal":150}}.

Decisão recente: {"hour":137,"actor":4803,"selected_need":{"id":22299,"kind":"food","target":null,"base":100,"priority":100,"status":"active","source":"physiology","reason":"Fome","created":74,"expires":null,"context":{"emergency":true}},"winner":{"action":"steal_person","score":73.88950225,"target":4694,"destination":null,"terms":{"base":0.31,"greed":0.15600000000000003,"honesty":-0.0585,"authority":-0.1,"courage":0.038,"travel":-0.0,"pressure_moral_tolerance":0.023947511249999994},"feeding":{"EstimatedTimeUntilFoodConsumed":2,"EstimatedSurvivalMargin":2,"economically_viable":true,"survival_viable":true,"reason":null,"known_conditions":["UnknownPrice","DistantProduct"]},"action_pressure":null},"preparations":[],"execution":{"goal_at_entry":{"id":188341,"need_id":22299,"action":"steal_person","score":73.88950225,"created_at":137,"target_id":4694,"destination":null,"status":"active","outcome":""},"state_before":{"id":4803,"name":"Silas Kars","hour":137,"alive":true,"profession":"mineiro","category":"comum","lod":"active","position":{"map_id":864,"x":1,"y":13},"home":{"map_id":864,"x":2,"y":2},"workplace":{"map_id":864,"x":12,"y":2},"residence":864,"hp":6,"hunger":100,"thirst":87,"fatigue":100,"money":3,"food":0,"water":1,"recoverable_deprivation":94,"starvation_hours":32,"local_food":5,"local_water":0,"personality":{"honesty":13,"compassion":39,"courage":76,"independence":65,"greed":78,"diligence":58,"family_loyalty":81,"persistence":12,"temperament":37,"vengefulness":78,"ambition":71,"sadism":0},"emotions":{"anger":0.12,"resentment":6.180000000000012,"humiliation":0.0,"desperation":23.549999999999947,"last_updated":137,"last_support":47,"strain":34.16699999999999,"adaptation":0,"last_adapted":0,"stable_material_hours":0,"nested_collections":"LACUNA: cópia rasa; histórico não utilizado"},"failures":{"forage_meal":147,"person_meal":148},"known_places":{"market":{"map_id":864,"x":7,"y":13},"home":{"map_id":864,"x":2,"y":2},"work":{"map_id":864,"x":12,"y":2},"forage":{"map_id":864,"x":1,"y":13},"well_home":{"map_id":864,"x":2,"y":2},"well_rural":{"map_id":864,"x":1,"y":13},"sacred":{"map_id":864,"x":7,"y":1}},"market_observation":{"turn":137,"town_id":864,"stock":{"food":5,"grain":28,"water":0,"iron":76,"wood":120},"temporary_work":true,"offers_expire_at":161,"training_offer":null,"price":2,"price_turn":53},"groups":[],"factions":[],"known_groups":[56255,72074,86400,110613,102867,113139,132984],"known_factions":[],"route_knowledge_count":2,"known_towns":[864,911],"journey":null,"training":{"target":null,"progress":0,"required":0},"devotion":94,"religion":"Culto do Sol","goal":{"id":188341,"need_id":22299,"action":"steal_person","score":73.88950225,"created_at":137,"target_id":4694,"destination":null,"status":"active","outcome":""},"suspended_goal":{"id":173197,"need_id":22299,"action":"forage","score":43.5,"created_at":123,"target_id":null,"destination":{"map_id":864,"x":1,"y":13},"status":"suspended","outcome":""}},"success":false,"result":[false,"Não havia provisão acessível no alvo."],"state_after":{"id":4803,"name":"Silas Kars","hour":137,"alive":true,"profession":"mineiro","category":"comum","lod":"active","position":{"map_id":864,"x":1,"y":13},"home":{"map_id":864,"x":2,"y":2},"workplace":{"map_id":864,"x":12,"y":2},"residence":864,"hp":6,"hunger":100,"thirst":87,"fatigue":100,"money":3,"food":0,"water":1,"recoverable_deprivation":94,"starvation_hours":32,"local_food":5,"local_water":0,"personality":{"honesty":13,"compassion":39,"courage":76,"independence":65,"greed":78,"diligence":58,"family_loyalty":81,"persistence":12,"temperament":37,"vengefulness":78,"ambition":71,"sadism":0},"emotions":{"anger":0.12,"resentment":6.180000000000012,"humiliation":0.0,"desperation":23.549999999999947,"last_updated":137,"last_support":47,"strain":34.16699999999999,"adaptation":0,"last_adapted":0,"stable_material_hours":0,"nested_collections":"LACUNA: cópia rasa; histórico não utilizado"},"failures":{"forage_meal":147,"person_meal":148},"known_places":{"market":{"map_id":864,"x":7,"y":13},"home":{"map_id":864,"x":2,"y":2},"work":{"map_id":864,"x":12,"y":2},"forage":{"map_id":864,"x":1,"y":13},"well_home":{"map_id":864,"x":2,"y":2},"well_rural":{"map_id":864,"x":1,"y":13},"sacred":{"map_id":864,"x":7,"y":1}},"market_observation":{"turn":137,"town_id":864,"stock":{"food":5,"grain":28,"water":0,"iron":76,"wood":120},"temporary_work":true,"offers_expire_at":161,"training_offer":null,"price":2,"price_turn":53},"groups":[],"factions":[],"known_groups":[56255,72074,86400,110613,102867,113139,132984],"known_factions":[],"route_knowledge_count":2,"known_towns":[864,911],"journey":null,"training":{"target":null,"progress":0,"required":0},"devotion":94,"religion":"Culto do Sol","goal":{"id":188341,"need_id":22299,"action":"steal_person","score":73.88950225,"created_at":137,"target_id":4694,"destination":null,"status":"active","outcome":""},"suspended_goal":{"id":173197,"need_id":22299,"action":"forage","score":43.5,"created_at":123,"target_id":null,"destination":{"map_id":864,"x":1,"y":13},"status":"suspended","outcome":""}}},"state_before":{"id":4803,"name":"Silas Kars","hour":137,"alive":true,"profession":"mineiro","lod":"active","position":{"map_id":864,"x":1,"y":13},"residence":864,"hp":6,"hunger":100,"thirst":87,"fatigue":100,"money":3,"food":0,"water":1,"local_food":5,"local_water":0,"recoverable_deprivation":94,"starvation_hours":32,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{"forage_meal":147,"person_meal":148}},"state_after":{"id":4803,"name":"Silas Kars","hour":137,"alive":true,"profession":"mineiro","lod":"active","position":{"map_id":864,"x":1,"y":13},"residence":864,"hp":6,"hunger":100,"thirst":87,"fatigue":100,"money":3,"food":0,"water":1,"local_food":5,"local_water":0,"recoverable_deprivation":94,"starvation_hours":32,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{"forage_meal":147,"person_meal":148,"steal_person":149}}}.

Decisão recente: {"hour":138,"actor":4803,"selected_need":{"id":22299,"kind":"food","target":null,"base":100,"priority":100,"status":"active","source":"physiology","reason":"Fome","created":74,"expires":null,"context":{"emergency":true}},"winner":{"action":"ask_meal","score":67.1,"target":4800,"destination":null,"terms":{"base":0.125,"compassion":0.0975,"trust":0.10149999999999998,"reputation":0.0,"relationship":0.011500000000000002,"travel":-0.0},"feeding":{"EstimatedTimeUntilFoodConsumed":1,"EstimatedSurvivalMargin":1,"economically_viable":true,"survival_viable":true,"reason":null,"known_conditions":["UnknownPrice","DistantProduct"]},"action_pressure":null},"preparations":[],"execution":{"goal_at_entry":{"id":189651,"need_id":22299,"action":"ask_meal","score":67.1,"created_at":138,"target_id":4800,"destination":null,"status":"active","outcome":""},"state_before":{"id":4803,"name":"Silas Kars","hour":138,"alive":true,"profession":"mineiro","category":"comum","lod":"active","position":{"map_id":864,"x":1,"y":13},"home":{"map_id":864,"x":2,"y":2},"workplace":{"map_id":864,"x":12,"y":2},"residence":864,"hp":2,"hunger":100,"thirst":89,"fatigue":100,"money":3,"food":0,"water":1,"recoverable_deprivation":98,"starvation_hours":33,"local_food":4,"local_water":0,"personality":{"honesty":13,"compassion":39,"courage":76,"independence":65,"greed":78,"diligence":58,"family_loyalty":81,"persistence":12,"temperament":37,"vengefulness":78,"ambition":71,"sadism":0},"emotions":{"anger":0.12,"resentment":6.140000000000012,"humiliation":0.0,"desperation":23.949999999999946,"last_updated":138,"last_support":47,"strain":34.706499999999984,"adaptation":0,"last_adapted":0,"stable_material_hours":0,"nested_collections":"LACUNA: cópia rasa; histórico não utilizado"},"failures":{"forage_meal":147,"person_meal":148,"steal_person":149},"known_places":{"market":{"map_id":864,"x":7,"y":13},"home":{"map_id":864,"x":2,"y":2},"work":{"map_id":864,"x":12,"y":2},"forage":{"map_id":864,"x":1,"y":13},"well_home":{"map_id":864,"x":2,"y":2},"well_rural":{"map_id":864,"x":1,"y":13},"sacred":{"map_id":864,"x":7,"y":1}},"market_observation":{"turn":138,"town_id":864,"stock":{"food":4,"grain":30,"water":0,"iron":76,"wood":120},"temporary_work":true,"offers_expire_at":162,"training_offer":null,"price":2,"price_turn":53},"groups":[],"factions":[],"known_groups":[56255,72074,86400,110613,102867,113139,132984],"known_factions":[],"route_knowledge_count":2,"known_towns":[864,911],"journey":null,"training":{"target":null,"progress":0,"required":0},"devotion":94,"religion":"Culto do Sol","goal":{"id":189651,"need_id":22299,"action":"ask_meal","score":67.1,"created_at":138,"target_id":4800,"destination":null,"status":"active","outcome":""},"suspended_goal":{"id":173197,"need_id":22299,"action":"forage","score":43.5,"created_at":123,"target_id":null,"destination":{"map_id":864,"x":1,"y":13},"status":"suspended","outcome":""}},"success":false,"result":[false,"Não foi possível obter ajuda."],"state_after":{"id":4803,"name":"Silas Kars","hour":138,"alive":true,"profession":"mineiro","category":"comum","lod":"active","position":{"map_id":864,"x":1,"y":13},"home":{"map_id":864,"x":2,"y":2},"workplace":{"map_id":864,"x":12,"y":2},"residence":864,"hp":2,"hunger":100,"thirst":89,"fatigue":100,"money":3,"food":0,"water":1,"recoverable_deprivation":98,"starvation_hours":33,"local_food":4,"local_water":0,"personality":{"honesty":13,"compassion":39,"courage":76,"independence":65,"greed":78,"diligence":58,"family_loyalty":81,"persistence":12,"temperament":37,"vengefulness":78,"ambition":71,"sadism":0},"emotions":{"anger":0.12,"resentment":6.140000000000012,"humiliation":0.0,"desperation":23.949999999999946,"last_updated":138,"last_support":47,"strain":34.706499999999984,"adaptation":0,"last_adapted":0,"stable_material_hours":0,"nested_collections":"LACUNA: cópia rasa; histórico não utilizado"},"failures":{"forage_meal":147,"person_meal":148,"steal_person":149},"known_places":{"market":{"map_id":864,"x":7,"y":13},"home":{"map_id":864,"x":2,"y":2},"work":{"map_id":864,"x":12,"y":2},"forage":{"map_id":864,"x":1,"y":13},"well_home":{"map_id":864,"x":2,"y":2},"well_rural":{"map_id":864,"x":1,"y":13},"sacred":{"map_id":864,"x":7,"y":1}},"market_observation":{"turn":138,"town_id":864,"stock":{"food":4,"grain":30,"water":0,"iron":76,"wood":120},"temporary_work":true,"offers_expire_at":162,"training_offer":null,"price":2,"price_turn":53},"groups":[],"factions":[],"known_groups":[56255,72074,86400,110613,102867,113139,132984],"known_factions":[],"route_knowledge_count":2,"known_towns":[864,911],"journey":null,"training":{"target":null,"progress":0,"required":0},"devotion":94,"religion":"Culto do Sol","goal":{"id":189651,"need_id":22299,"action":"ask_meal","score":67.1,"created_at":138,"target_id":4800,"destination":null,"status":"active","outcome":""},"suspended_goal":{"id":173197,"need_id":22299,"action":"forage","score":43.5,"created_at":123,"target_id":null,"destination":{"map_id":864,"x":1,"y":13},"status":"suspended","outcome":""}}},"state_before":{"id":4803,"name":"Silas Kars","hour":138,"alive":true,"profession":"mineiro","lod":"active","position":{"map_id":864,"x":1,"y":13},"residence":864,"hp":2,"hunger":100,"thirst":89,"fatigue":100,"money":3,"food":0,"water":1,"local_food":4,"local_water":0,"recoverable_deprivation":98,"starvation_hours":33,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{"forage_meal":147,"person_meal":148,"steal_person":149}},"state_after":{"id":4803,"name":"Silas Kars","hour":138,"alive":true,"profession":"mineiro","lod":"active","position":{"map_id":864,"x":1,"y":13},"residence":864,"hp":2,"hunger":100,"thirst":89,"fatigue":100,"money":3,"food":0,"water":1,"local_food":4,"local_water":0,"recoverable_deprivation":98,"starvation_hours":33,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{"forage_meal":147,"person_meal":148,"steal_person":149,"ask_meal":150}}}.

LACUNA: estoque local não prova que era conhecido, pagável, alcançável e consumível a tempo; o trace explica as últimas escolhas, mas não simula um contrafactual de sobrevivência.

### Caso thirst: NPC #2464, h128

Registro: {"turn":128,"name":"Cael Valerius","profession":"mineiro","town_id":302,"cause":"thirst","health":0,"hunger":62,"thirst":100,"fatigue":100,"food":0,"water":0,"last_meal":127,"last_drink":63,"recoverable_deprivation_damage":100,"damage_by_origin":{"hunger":43,"both":55,"thirst":2},"last_successful_action":{"action":"steal_meal","turn":127},"goal":"steal_meal","destination":{"map_id":302,"x":7,"y":13},"known_water_sources":[{"map_id":302,"x":7,"y":13},{"map_id":302,"x":2,"y":2},{"map_id":302,"x":1,"y":13}],"distance_to_water":0,"event_id":177760}.

Estado pré-fechamento de morte: {"id":2464,"name":"Cael Valerius","hour":128,"alive":true,"profession":"mineiro","lod":"active","position":{"map_id":302,"x":7,"y":13},"residence":302,"hp":0,"hunger":62,"thirst":100,"fatigue":100,"money":2,"food":0,"water":0,"local_food":7,"local_water":0,"recoverable_deprivation":100,"starvation_hours":34,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{}}.

Decisão recente: {"hour":126,"actor":2464,"selected_need":{"id":23621,"kind":"food","target":null,"base":100,"priority":100,"status":"selected","source":"physiology","reason":"Fome","created":63,"expires":null,"context":{"emergency":true}},"winner":{"action":"steal_meal","score":84.45149358333333,"target":null,"destination":{"map_id":302,"x":7,"y":13},"terms":{"base":0.35,"greed":0.11166666666666668,"honesty":-0.105,"courage":0.036,"travel":-0.01,"pressure_moral_tolerance":0.03959080125000001},"feeding":{"EstimatedTimeUntilFoodConsumed":2,"EstimatedSurvivalMargin":2,"economically_viable":true,"survival_viable":true,"reason":null,"known_conditions":["UnknownPrice","DistantProduct"]},"action_pressure":null},"preparations":[],"execution":null,"state_before":{"id":2464,"name":"Cael Valerius","hour":126,"alive":true,"profession":"mineiro","lod":"active","position":{"map_id":302,"x":6,"y":13},"residence":302,"hp":6,"hunger":100,"thirst":100,"fatigue":100,"money":2,"food":0,"water":0,"local_food":9,"local_water":0,"recoverable_deprivation":94,"starvation_hours":32,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{}},"state_after":{"id":2464,"name":"Cael Valerius","hour":126,"alive":true,"profession":"mineiro","lod":"active","position":{"map_id":302,"x":7,"y":13},"residence":302,"hp":6,"hunger":100,"thirst":100,"fatigue":100,"money":2,"food":0,"water":0,"local_food":9,"local_water":0,"recoverable_deprivation":94,"starvation_hours":32,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{}}}.

Decisão recente: {"hour":127,"actor":2464,"selected_need":{"id":23621,"kind":"food","target":null,"base":100,"priority":100,"status":"selected","source":"physiology","reason":"Fome","created":63,"expires":null,"context":{"emergency":true}},"winner":{"action":"steal_meal","score":86.38051358333333,"target":null,"destination":{"map_id":302,"x":7,"y":13},"terms":{"base":0.35,"greed":0.11166666666666668,"honesty":-0.105,"courage":0.036,"travel":-0.0,"pressure_moral_tolerance":0.03923590124999999},"feeding":{"EstimatedTimeUntilFoodConsumed":1,"EstimatedSurvivalMargin":1,"economically_viable":true,"survival_viable":true,"reason":null,"known_conditions":["NoMoney"]},"action_pressure":null},"preparations":[],"execution":{"goal_at_entry":{"id":171335,"need_id":23621,"action":"steal_meal","score":76.73541358333333,"created_at":122,"target_id":null,"destination":{"map_id":302,"x":7,"y":13},"status":"active","outcome":""},"state_before":{"id":2464,"name":"Cael Valerius","hour":127,"alive":true,"profession":"mineiro","category":"comum","lod":"active","position":{"map_id":302,"x":7,"y":13},"home":{"map_id":302,"x":2,"y":2},"workplace":{"map_id":302,"x":12,"y":2},"residence":302,"hp":2,"hunger":100,"thirst":100,"fatigue":100,"money":2,"food":0,"water":0,"recoverable_deprivation":98,"starvation_hours":33,"local_food":5,"local_water":0,"personality":{"honesty":21,"compassion":56,"courage":72,"independence":76,"greed":67,"diligence":21,"family_loyalty":73,"persistence":41,"temperament":10,"vengefulness":35,"ambition":43,"sadism":12},"emotions":{"anger":17.94,"resentment":9.860000000000001,"humiliation":8.9,"desperation":22.149999999999956,"last_updated":127,"last_support":27,"strain":29.61699999999999,"adaptation":0,"last_adapted":0,"stable_material_hours":0,"nested_collections":"LACUNA: cópia rasa; histórico não utilizado"},"failures":{},"known_places":{"market":{"map_id":302,"x":7,"y":13},"home":{"map_id":302,"x":2,"y":2},"work":{"map_id":302,"x":12,"y":2},"forage":{"map_id":302,"x":1,"y":13},"well_home":{"map_id":302,"x":2,"y":2},"well_rural":{"map_id":302,"x":1,"y":13},"sacred":{"map_id":302,"x":7,"y":1}},"market_observation":{"turn":127,"town_id":302,"stock":{"food":5,"grain":94,"water":0,"iron":64,"wood":120},"temporary_work":true,"offers_expire_at":151,"training_offer":null,"price":6,"price_turn":127},"groups":[],"factions":[],"known_groups":[31271,50846,33120,84785],"known_factions":[],"route_knowledge_count":2,"known_towns":[302,367],"journey":null,"training":{"target":null,"progress":0,"required":0},"devotion":71,"religion":"Culto da Aurora","goal":{"id":171335,"need_id":23621,"action":"steal_meal","score":76.73541358333333,"created_at":122,"target_id":null,"destination":{"map_id":302,"x":7,"y":13},"status":"active","outcome":""},"suspended_goal":{"id":157665,"need_id":23621,"action":"forage","score":49.0,"created_at":111,"target_id":null,"destination":{"map_id":302,"x":1,"y":13},"status":"suspended","outcome":""}},"success":true,"result":[true,"Alimento roubado. Fome reduzida."],"state_after":{"id":2464,"name":"Cael Valerius","hour":127,"alive":true,"profession":"mineiro","category":"comum","lod":"active","position":{"map_id":302,"x":7,"y":13},"home":{"map_id":302,"x":2,"y":2},"workplace":{"map_id":302,"x":12,"y":2},"residence":302,"hp":2,"hunger":60,"thirst":100,"fatigue":100,"money":2,"food":0,"water":0,"recoverable_deprivation":98,"starvation_hours":33,"local_food":4,"local_water":0,"personality":{"honesty":21,"compassion":56,"courage":72,"independence":76,"greed":67,"diligence":21,"family_loyalty":73,"persistence":41,"temperament":10,"vengefulness":35,"ambition":43,"sadism":12},"emotions":{"anger":17.94,"resentment":9.860000000000001,"humiliation":8.9,"desperation":22.149999999999956,"last_updated":127,"last_support":27,"strain":29.61699999999999,"adaptation":0,"last_adapted":0,"stable_material_hours":0,"nested_collections":"LACUNA: cópia rasa; histórico não utilizado"},"failures":{},"known_places":{"market":{"map_id":302,"x":7,"y":13},"home":{"map_id":302,"x":2,"y":2},"work":{"map_id":302,"x":12,"y":2},"forage":{"map_id":302,"x":1,"y":13},"well_home":{"map_id":302,"x":2,"y":2},"well_rural":{"map_id":302,"x":1,"y":13},"sacred":{"map_id":302,"x":7,"y":1}},"market_observation":{"turn":127,"town_id":302,"stock":{"food":5,"grain":94,"water":0,"iron":64,"wood":120},"temporary_work":true,"offers_expire_at":151,"training_offer":null,"price":6,"price_turn":127},"groups":[],"factions":[],"known_groups":[31271,50846,33120,84785],"known_factions":[],"route_knowledge_count":2,"known_towns":[302,367],"journey":null,"training":{"target":null,"progress":0,"required":0},"devotion":71,"religion":"Culto da Aurora","goal":{"id":171335,"need_id":23621,"action":"steal_meal","score":76.73541358333333,"created_at":122,"target_id":null,"destination":{"map_id":302,"x":7,"y":13},"status":"active","outcome":""},"suspended_goal":{"id":157665,"need_id":23621,"action":"forage","score":49.0,"created_at":111,"target_id":null,"destination":{"map_id":302,"x":1,"y":13},"status":"suspended","outcome":""}}},"state_before":{"id":2464,"name":"Cael Valerius","hour":127,"alive":true,"profession":"mineiro","lod":"active","position":{"map_id":302,"x":7,"y":13},"residence":302,"hp":2,"hunger":100,"thirst":100,"fatigue":100,"money":2,"food":0,"water":0,"local_food":5,"local_water":0,"recoverable_deprivation":98,"starvation_hours":33,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{}},"state_after":{"id":2464,"name":"Cael Valerius","hour":127,"alive":true,"profession":"mineiro","lod":"active","position":{"map_id":302,"x":7,"y":13},"residence":302,"hp":2,"hunger":60,"thirst":100,"fatigue":100,"money":2,"food":0,"water":0,"local_food":4,"local_water":0,"recoverable_deprivation":98,"starvation_hours":33,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{}}}.

LACUNA: estoque local não prova que era conhecido, pagável, alcançável e consumível a tempo; o trace explica as últimas escolhas, mas não simula um contrafactual de sobrevivência.

### Caso both: NPC #1299, h166

Registro: {"turn":166,"name":"Arthus Kars","profession":"ferreiro","town_id":3,"cause":"both","health":0,"hunger":100,"thirst":100,"fatigue":79.60000000000004,"food":0,"water":0,"last_meal":109,"last_drink":125,"recoverable_deprivation_damage":100,"damage_by_origin":{"hunger":88,"both":11,"thirst":2},"last_successful_action":{"action":"sleep","turn":160},"goal":"ask_meal","destination":null,"known_water_sources":[{"map_id":3,"x":7,"y":13},{"map_id":3,"x":2,"y":2},{"map_id":3,"x":1,"y":13}],"distance_to_water":0,"event_id":222415}.

Estado pré-fechamento de morte: {"id":1299,"name":"Arthus Kars","hour":166,"alive":true,"profession":"ferreiro","lod":"active","position":{"map_id":3,"x":2,"y":2},"residence":3,"hp":0,"hunger":100,"thirst":100,"fatigue":79.60000000000004,"money":0,"food":0,"water":0,"local_food":7,"local_water":0,"recoverable_deprivation":100,"starvation_hours":32,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{"fill_water":176,"steal_person":166,"drink_well":167,"ask_meal":177}}.

Decisão recente: {"hour":164,"actor":1299,"selected_need":{"id":20217,"kind":"political_pressure","target":null,"base":80,"priority":91.9984,"status":"active","source":"own_shared_problem","reason":"Buscar representação para problema pessoal","created":51,"expires":null,"context":{}},"winner":{"action":"fill_water","score":100,"target":null,"destination":{"map_id":3,"x":2,"y":2},"terms":{},"feeding":null,"action_pressure":null},"preparations":[{"input":{"action":"share_problem","score":15.7,"target":null,"destination":{"map_id":3,"x":7,"y":13},"terms":{"base":0.225,"compassion":0.023250000000000003,"independence":-0.009750000000000002,"travel":-0.16},"feeding":null,"action_pressure":null},"replacement":{"action":"fill_water","score":100,"target":null,"destination":{"map_id":3,"x":2,"y":2},"terms":{},"feeding":null,"action_pressure":null},"travel":16,"horizon":22}],"execution":{"goal_at_entry":{"id":220055,"need_id":20217,"action":"fill_water","score":100,"created_at":164,"target_id":null,"destination":{"map_id":3,"x":2,"y":2},"status":"active","outcome":""},"state_before":{"id":1299,"name":"Arthus Kars","hour":164,"alive":true,"profession":"ferreiro","category":"comum","lod":"active","position":{"map_id":3,"x":2,"y":2},"home":{"map_id":3,"x":2,"y":2},"workplace":{"map_id":3,"x":12,"y":2},"residence":3,"hp":5,"hunger":100,"thirst":100,"fatigue":77.20000000000003,"money":0,"food":0,"water":0,"recoverable_deprivation":95,"starvation_hours":30,"local_food":8,"local_water":0,"personality":{"honesty":78,"compassion":31,"courage":54,"independence":13,"greed":61,"diligence":64,"family_loyalty":15,"persistence":22,"temperament":59,"vengefulness":45,"ambition":48,"sadism":1},"emotions":{"anger":45.24000000000002,"resentment":35.04000000000008,"humiliation":24.599999999999937,"desperation":28.34999999999994,"last_updated":164,"last_support":-10000,"strain":36.63749999999999,"adaptation":0,"last_adapted":0,"stable_material_hours":0,"nested_collections":"LACUNA: cópia rasa; histórico não utilizado"},"failures":{"fill_water":175,"steal_person":166,"drink_well":167},"known_places":{"market":{"map_id":3,"x":7,"y":13},"home":{"map_id":3,"x":2,"y":2},"work":{"map_id":3,"x":12,"y":2},"forage":{"map_id":3,"x":1,"y":13},"well_home":{"map_id":3,"x":2,"y":2},"well_rural":{"map_id":3,"x":1,"y":13},"sacred":{"map_id":3,"x":7,"y":1}},"market_observation":{"turn":139,"town_id":3,"stock":{"food":11,"grain":99,"water":0,"iron":100,"wood":72},"temporary_work":true,"offers_expire_at":163,"training_offer":null,"price":14,"price_turn":102},"groups":[],"factions":[],"known_groups":[17206,30771,43245,30390,129111,146187,149113,161707],"known_factions":[1168],"route_knowledge_count":2,"known_towns":[3,50],"journey":null,"training":{"target":null,"progress":0,"required":0},"devotion":81,"religion":"Ordem da Maré","goal":{"id":220055,"need_id":20217,"action":"fill_water","score":100,"created_at":164,"target_id":null,"destination":{"map_id":3,"x":2,"y":2},"status":"active","outcome":""},"suspended_goal":null},"success":false,"result":[false,"Não há água para levar nesta fonte."],"state_after":{"id":1299,"name":"Arthus Kars","hour":164,"alive":true,"profession":"ferreiro","category":"comum","lod":"active","position":{"map_id":3,"x":2,"y":2},"home":{"map_id":3,"x":2,"y":2},"workplace":{"map_id":3,"x":12,"y":2},"residence":3,"hp":5,"hunger":100,"thirst":100,"fatigue":77.20000000000003,"money":0,"food":0,"water":0,"recoverable_deprivation":95,"starvation_hours":30,"local_food":8,"local_water":0,"personality":{"honesty":78,"compassion":31,"courage":54,"independence":13,"greed":61,"diligence":64,"family_loyalty":15,"persistence":22,"temperament":59,"vengefulness":45,"ambition":48,"sadism":1},"emotions":{"anger":45.24000000000002,"resentment":35.04000000000008,"humiliation":24.599999999999937,"desperation":28.34999999999994,"last_updated":164,"last_support":-10000,"strain":36.63749999999999,"adaptation":0,"last_adapted":0,"stable_material_hours":0,"nested_collections":"LACUNA: cópia rasa; histórico não utilizado"},"failures":{"fill_water":175,"steal_person":166,"drink_well":167},"known_places":{"market":{"map_id":3,"x":7,"y":13},"home":{"map_id":3,"x":2,"y":2},"work":{"map_id":3,"x":12,"y":2},"forage":{"map_id":3,"x":1,"y":13},"well_home":{"map_id":3,"x":2,"y":2},"well_rural":{"map_id":3,"x":1,"y":13},"sacred":{"map_id":3,"x":7,"y":1}},"market_observation":{"turn":139,"town_id":3,"stock":{"food":11,"grain":99,"water":0,"iron":100,"wood":72},"temporary_work":true,"offers_expire_at":163,"training_offer":null,"price":14,"price_turn":102},"groups":[],"factions":[],"known_groups":[17206,30771,43245,30390,129111,146187,149113,161707],"known_factions":[1168],"route_knowledge_count":2,"known_towns":[3,50],"journey":null,"training":{"target":null,"progress":0,"required":0},"devotion":81,"religion":"Ordem da Maré","goal":{"id":220055,"need_id":20217,"action":"fill_water","score":100,"created_at":164,"target_id":null,"destination":{"map_id":3,"x":2,"y":2},"status":"active","outcome":""},"suspended_goal":null}},"state_before":{"id":1299,"name":"Arthus Kars","hour":164,"alive":true,"profession":"ferreiro","lod":"active","position":{"map_id":3,"x":2,"y":2},"residence":3,"hp":5,"hunger":100,"thirst":100,"fatigue":77.20000000000003,"money":0,"food":0,"water":0,"local_food":8,"local_water":0,"recoverable_deprivation":95,"starvation_hours":30,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{"fill_water":175,"steal_person":166,"drink_well":167}},"state_after":{"id":1299,"name":"Arthus Kars","hour":164,"alive":true,"profession":"ferreiro","lod":"active","position":{"map_id":3,"x":2,"y":2},"residence":3,"hp":5,"hunger":100,"thirst":100,"fatigue":77.20000000000003,"money":0,"food":0,"water":0,"local_food":8,"local_water":0,"recoverable_deprivation":95,"starvation_hours":30,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{"fill_water":176,"steal_person":166,"drink_well":167}}}.

Decisão recente: {"hour":165,"actor":1299,"selected_need":{"id":20212,"kind":"food","target":null,"base":100,"priority":100,"status":"active","source":"physiology","reason":"Fome","created":62,"expires":null,"context":{"emergency":true}},"winner":{"action":"ask_meal","score":69.19999999999999,"target":1302,"destination":null,"terms":{"base":0.125,"compassion":0.0775,"trust":0.1085,"reputation":0.0,"relationship":0.035,"travel":-0.0},"feeding":{"EstimatedTimeUntilFoodConsumed":1,"EstimatedSurvivalMargin":1,"economically_viable":true,"survival_viable":true,"reason":null,"known_conditions":["UnknownPrice","DistantProduct"]},"action_pressure":null},"preparations":[],"execution":{"goal_at_entry":{"id":221317,"need_id":20212,"action":"ask_meal","score":69.19999999999999,"created_at":165,"target_id":1302,"destination":null,"status":"active","outcome":""},"state_before":{"id":1299,"name":"Arthus Kars","hour":165,"alive":true,"profession":"ferreiro","category":"comum","lod":"active","position":{"map_id":3,"x":2,"y":2},"home":{"map_id":3,"x":2,"y":2},"workplace":{"map_id":3,"x":12,"y":2},"residence":3,"hp":1,"hunger":100,"thirst":100,"fatigue":78.40000000000003,"money":0,"food":0,"water":0,"recoverable_deprivation":99,"starvation_hours":31,"local_food":9,"local_water":0,"personality":{"honesty":78,"compassion":31,"courage":54,"independence":13,"greed":61,"diligence":64,"family_loyalty":15,"persistence":22,"temperament":59,"vengefulness":45,"ambition":48,"sadism":1},"emotions":{"anger":45.060000000000024,"resentment":35.00000000000008,"humiliation":24.499999999999936,"desperation":28.74999999999994,"last_updated":165,"last_support":-10000,"strain":37.22499999999999,"adaptation":0,"last_adapted":0,"stable_material_hours":0,"nested_collections":"LACUNA: cópia rasa; histórico não utilizado"},"failures":{"fill_water":176,"steal_person":166,"drink_well":167},"known_places":{"market":{"map_id":3,"x":7,"y":13},"home":{"map_id":3,"x":2,"y":2},"work":{"map_id":3,"x":12,"y":2},"forage":{"map_id":3,"x":1,"y":13},"well_home":{"map_id":3,"x":2,"y":2},"well_rural":{"map_id":3,"x":1,"y":13},"sacred":{"map_id":3,"x":7,"y":1}},"market_observation":{"turn":139,"town_id":3,"stock":{"food":11,"grain":99,"water":0,"iron":100,"wood":72},"temporary_work":true,"offers_expire_at":163,"training_offer":null,"price":14,"price_turn":102},"groups":[],"factions":[],"known_groups":[17206,30771,43245,30390,129111,146187,149113,161707],"known_factions":[1168],"route_knowledge_count":2,"known_towns":[3,50],"journey":null,"training":{"target":null,"progress":0,"required":0},"devotion":81,"religion":"Ordem da Maré","goal":{"id":221317,"need_id":20212,"action":"ask_meal","score":69.19999999999999,"created_at":165,"target_id":1302,"destination":null,"status":"active","outcome":""},"suspended_goal":null},"success":false,"result":[false,"Não foi possível obter ajuda."],"state_after":{"id":1299,"name":"Arthus Kars","hour":165,"alive":true,"profession":"ferreiro","category":"comum","lod":"active","position":{"map_id":3,"x":2,"y":2},"home":{"map_id":3,"x":2,"y":2},"workplace":{"map_id":3,"x":12,"y":2},"residence":3,"hp":1,"hunger":100,"thirst":100,"fatigue":78.40000000000003,"money":0,"food":0,"water":0,"recoverable_deprivation":99,"starvation_hours":31,"local_food":9,"local_water":0,"personality":{"honesty":78,"compassion":31,"courage":54,"independence":13,"greed":61,"diligence":64,"family_loyalty":15,"persistence":22,"temperament":59,"vengefulness":45,"ambition":48,"sadism":1},"emotions":{"anger":45.060000000000024,"resentment":35.00000000000008,"humiliation":24.499999999999936,"desperation":28.74999999999994,"last_updated":165,"last_support":-10000,"strain":37.22499999999999,"adaptation":0,"last_adapted":0,"stable_material_hours":0,"nested_collections":"LACUNA: cópia rasa; histórico não utilizado"},"failures":{"fill_water":176,"steal_person":166,"drink_well":167},"known_places":{"market":{"map_id":3,"x":7,"y":13},"home":{"map_id":3,"x":2,"y":2},"work":{"map_id":3,"x":12,"y":2},"forage":{"map_id":3,"x":1,"y":13},"well_home":{"map_id":3,"x":2,"y":2},"well_rural":{"map_id":3,"x":1,"y":13},"sacred":{"map_id":3,"x":7,"y":1}},"market_observation":{"turn":139,"town_id":3,"stock":{"food":11,"grain":99,"water":0,"iron":100,"wood":72},"temporary_work":true,"offers_expire_at":163,"training_offer":null,"price":14,"price_turn":102},"groups":[],"factions":[],"known_groups":[17206,30771,43245,30390,129111,146187,149113,161707],"known_factions":[1168],"route_knowledge_count":2,"known_towns":[3,50],"journey":null,"training":{"target":null,"progress":0,"required":0},"devotion":81,"religion":"Ordem da Maré","goal":{"id":221317,"need_id":20212,"action":"ask_meal","score":69.19999999999999,"created_at":165,"target_id":1302,"destination":null,"status":"active","outcome":""},"suspended_goal":null}},"state_before":{"id":1299,"name":"Arthus Kars","hour":165,"alive":true,"profession":"ferreiro","lod":"active","position":{"map_id":3,"x":2,"y":2},"residence":3,"hp":1,"hunger":100,"thirst":100,"fatigue":78.40000000000003,"money":0,"food":0,"water":0,"local_food":9,"local_water":0,"recoverable_deprivation":99,"starvation_hours":31,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{"fill_water":176,"steal_person":166,"drink_well":167}},"state_after":{"id":1299,"name":"Arthus Kars","hour":165,"alive":true,"profession":"ferreiro","lod":"active","position":{"map_id":3,"x":2,"y":2},"residence":3,"hp":1,"hunger":100,"thirst":100,"fatigue":78.40000000000003,"money":0,"food":0,"water":0,"local_food":9,"local_water":0,"recoverable_deprivation":99,"starvation_hours":31,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{"fill_water":176,"steal_person":166,"drink_well":167,"ask_meal":177}}}.

LACUNA: estoque local não prova que era conhecido, pagável, alcançável e consumível a tempo; o trace explica as últimas escolhas, mas não simula um contrafactual de sobrevivência.

**combat:** nenhum caso que satisfaça o filtro na campanha.

### Caso with_owned_food: NPC #1046, h207

Registro: {"turn":207,"name":"Bela Luar","profession":"guarda","town_id":1023,"cause":"thirst","health":0,"hunger":18,"thirst":100,"fatigue":100,"food":3,"water":0,"last_meal":201,"last_drink":147,"recoverable_deprivation_damage":100,"damage_by_origin":{"thirst":100},"last_successful_action":{"action":"forage","turn":203},"goal":"fill_water","destination":{"map_id":864,"x":7,"y":13},"known_water_sources":[{"map_id":864,"x":7,"y":13},{"map_id":1023,"x":2,"y":2},{"map_id":864,"x":1,"y":13}],"distance_to_water":3,"event_id":269053}.

Estado pré-fechamento de morte: {"id":1046,"name":"Bela Luar","hour":207,"alive":true,"profession":"guarda","lod":"active","position":{"map_id":864,"x":4,"y":13},"residence":1023,"hp":0,"hunger":18,"thirst":100,"fatigue":100,"money":17,"food":3,"water":0,"local_food":0,"local_water":0,"recoverable_deprivation":100,"starvation_hours":17,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{"drink_well":210}}.

Decisão recente: {"hour":205,"actor":1046,"selected_need":{"id":107646,"kind":"migration","target":1052,"base":52,"priority":61.388,"status":"selected","source":"known_towns","reason":"Considerar mudança por threat","created":144,"expires":null,"context":{"reason":"threat"}},"winner":{"action":"fill_water","score":95.39999999999999,"target":null,"destination":{"map_id":864,"x":7,"y":13},"terms":{"base":0.5,"diligence":0.027000000000000003,"travel":-0.05},"feeding":null,"action_pressure":null},"preparations":[],"execution":null,"state_before":{"id":1046,"name":"Bela Luar","hour":205,"alive":true,"profession":"guarda","lod":"active","position":{"map_id":864,"x":2,"y":13},"residence":1023,"hp":4,"hunger":14,"thirst":100,"fatigue":100,"money":17,"food":3,"water":0,"local_food":0,"local_water":0,"recoverable_deprivation":96,"starvation_hours":15,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{"drink_well":210}},"state_after":{"id":1046,"name":"Bela Luar","hour":205,"alive":true,"profession":"guarda","lod":"active","position":{"map_id":864,"x":3,"y":13},"residence":1023,"hp":4,"hunger":14,"thirst":100,"fatigue":100,"money":17,"food":3,"water":0,"local_food":0,"local_water":0,"recoverable_deprivation":96,"starvation_hours":15,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{"drink_well":210}}}.

Decisão recente: {"hour":206,"actor":1046,"selected_need":{"id":107646,"kind":"migration","target":1052,"base":52,"priority":61.42,"status":"selected","source":"known_towns","reason":"Considerar mudança por threat","created":144,"expires":null,"context":{"reason":"threat"}},"winner":{"action":"fill_water","score":97.39999999999999,"target":null,"destination":{"map_id":864,"x":7,"y":13},"terms":{"base":0.5,"diligence":0.027000000000000003,"travel":-0.04},"feeding":null,"action_pressure":null},"preparations":[],"execution":null,"state_before":{"id":1046,"name":"Bela Luar","hour":206,"alive":true,"profession":"guarda","lod":"active","position":{"map_id":864,"x":3,"y":13},"residence":1023,"hp":1,"hunger":16,"thirst":100,"fatigue":100,"money":17,"food":3,"water":0,"local_food":0,"local_water":0,"recoverable_deprivation":99,"starvation_hours":16,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{"drink_well":210}},"state_after":{"id":1046,"name":"Bela Luar","hour":206,"alive":true,"profession":"guarda","lod":"active","position":{"map_id":864,"x":4,"y":13},"residence":1023,"hp":1,"hunger":16,"thirst":100,"fatigue":100,"money":17,"food":3,"water":0,"local_food":0,"local_water":0,"recoverable_deprivation":99,"starvation_hours":16,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{"drink_well":210}}}.

LACUNA: estoque local não prova que era conhecido, pagável, alcançável e consumível a tempo; o trace explica as últimas escolhas, mas não simula um contrafactual de sobrevivência.

### Caso with_local_food: NPC #2464, h128

Registro: {"turn":128,"name":"Cael Valerius","profession":"mineiro","town_id":302,"cause":"thirst","health":0,"hunger":62,"thirst":100,"fatigue":100,"food":0,"water":0,"last_meal":127,"last_drink":63,"recoverable_deprivation_damage":100,"damage_by_origin":{"hunger":43,"both":55,"thirst":2},"last_successful_action":{"action":"steal_meal","turn":127},"goal":"steal_meal","destination":{"map_id":302,"x":7,"y":13},"known_water_sources":[{"map_id":302,"x":7,"y":13},{"map_id":302,"x":2,"y":2},{"map_id":302,"x":1,"y":13}],"distance_to_water":0,"event_id":177760}.

Estado pré-fechamento de morte: {"id":2464,"name":"Cael Valerius","hour":128,"alive":true,"profession":"mineiro","lod":"active","position":{"map_id":302,"x":7,"y":13},"residence":302,"hp":0,"hunger":62,"thirst":100,"fatigue":100,"money":2,"food":0,"water":0,"local_food":7,"local_water":0,"recoverable_deprivation":100,"starvation_hours":34,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{}}.

Decisão recente: {"hour":126,"actor":2464,"selected_need":{"id":23621,"kind":"food","target":null,"base":100,"priority":100,"status":"selected","source":"physiology","reason":"Fome","created":63,"expires":null,"context":{"emergency":true}},"winner":{"action":"steal_meal","score":84.45149358333333,"target":null,"destination":{"map_id":302,"x":7,"y":13},"terms":{"base":0.35,"greed":0.11166666666666668,"honesty":-0.105,"courage":0.036,"travel":-0.01,"pressure_moral_tolerance":0.03959080125000001},"feeding":{"EstimatedTimeUntilFoodConsumed":2,"EstimatedSurvivalMargin":2,"economically_viable":true,"survival_viable":true,"reason":null,"known_conditions":["UnknownPrice","DistantProduct"]},"action_pressure":null},"preparations":[],"execution":null,"state_before":{"id":2464,"name":"Cael Valerius","hour":126,"alive":true,"profession":"mineiro","lod":"active","position":{"map_id":302,"x":6,"y":13},"residence":302,"hp":6,"hunger":100,"thirst":100,"fatigue":100,"money":2,"food":0,"water":0,"local_food":9,"local_water":0,"recoverable_deprivation":94,"starvation_hours":32,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{}},"state_after":{"id":2464,"name":"Cael Valerius","hour":126,"alive":true,"profession":"mineiro","lod":"active","position":{"map_id":302,"x":7,"y":13},"residence":302,"hp":6,"hunger":100,"thirst":100,"fatigue":100,"money":2,"food":0,"water":0,"local_food":9,"local_water":0,"recoverable_deprivation":94,"starvation_hours":32,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{}}}.

Decisão recente: {"hour":127,"actor":2464,"selected_need":{"id":23621,"kind":"food","target":null,"base":100,"priority":100,"status":"selected","source":"physiology","reason":"Fome","created":63,"expires":null,"context":{"emergency":true}},"winner":{"action":"steal_meal","score":86.38051358333333,"target":null,"destination":{"map_id":302,"x":7,"y":13},"terms":{"base":0.35,"greed":0.11166666666666668,"honesty":-0.105,"courage":0.036,"travel":-0.0,"pressure_moral_tolerance":0.03923590124999999},"feeding":{"EstimatedTimeUntilFoodConsumed":1,"EstimatedSurvivalMargin":1,"economically_viable":true,"survival_viable":true,"reason":null,"known_conditions":["NoMoney"]},"action_pressure":null},"preparations":[],"execution":{"goal_at_entry":{"id":171335,"need_id":23621,"action":"steal_meal","score":76.73541358333333,"created_at":122,"target_id":null,"destination":{"map_id":302,"x":7,"y":13},"status":"active","outcome":""},"state_before":{"id":2464,"name":"Cael Valerius","hour":127,"alive":true,"profession":"mineiro","category":"comum","lod":"active","position":{"map_id":302,"x":7,"y":13},"home":{"map_id":302,"x":2,"y":2},"workplace":{"map_id":302,"x":12,"y":2},"residence":302,"hp":2,"hunger":100,"thirst":100,"fatigue":100,"money":2,"food":0,"water":0,"recoverable_deprivation":98,"starvation_hours":33,"local_food":5,"local_water":0,"personality":{"honesty":21,"compassion":56,"courage":72,"independence":76,"greed":67,"diligence":21,"family_loyalty":73,"persistence":41,"temperament":10,"vengefulness":35,"ambition":43,"sadism":12},"emotions":{"anger":17.94,"resentment":9.860000000000001,"humiliation":8.9,"desperation":22.149999999999956,"last_updated":127,"last_support":27,"strain":29.61699999999999,"adaptation":0,"last_adapted":0,"stable_material_hours":0,"nested_collections":"LACUNA: cópia rasa; histórico não utilizado"},"failures":{},"known_places":{"market":{"map_id":302,"x":7,"y":13},"home":{"map_id":302,"x":2,"y":2},"work":{"map_id":302,"x":12,"y":2},"forage":{"map_id":302,"x":1,"y":13},"well_home":{"map_id":302,"x":2,"y":2},"well_rural":{"map_id":302,"x":1,"y":13},"sacred":{"map_id":302,"x":7,"y":1}},"market_observation":{"turn":127,"town_id":302,"stock":{"food":5,"grain":94,"water":0,"iron":64,"wood":120},"temporary_work":true,"offers_expire_at":151,"training_offer":null,"price":6,"price_turn":127},"groups":[],"factions":[],"known_groups":[31271,50846,33120,84785],"known_factions":[],"route_knowledge_count":2,"known_towns":[302,367],"journey":null,"training":{"target":null,"progress":0,"required":0},"devotion":71,"religion":"Culto da Aurora","goal":{"id":171335,"need_id":23621,"action":"steal_meal","score":76.73541358333333,"created_at":122,"target_id":null,"destination":{"map_id":302,"x":7,"y":13},"status":"active","outcome":""},"suspended_goal":{"id":157665,"need_id":23621,"action":"forage","score":49.0,"created_at":111,"target_id":null,"destination":{"map_id":302,"x":1,"y":13},"status":"suspended","outcome":""}},"success":true,"result":[true,"Alimento roubado. Fome reduzida."],"state_after":{"id":2464,"name":"Cael Valerius","hour":127,"alive":true,"profession":"mineiro","category":"comum","lod":"active","position":{"map_id":302,"x":7,"y":13},"home":{"map_id":302,"x":2,"y":2},"workplace":{"map_id":302,"x":12,"y":2},"residence":302,"hp":2,"hunger":60,"thirst":100,"fatigue":100,"money":2,"food":0,"water":0,"recoverable_deprivation":98,"starvation_hours":33,"local_food":4,"local_water":0,"personality":{"honesty":21,"compassion":56,"courage":72,"independence":76,"greed":67,"diligence":21,"family_loyalty":73,"persistence":41,"temperament":10,"vengefulness":35,"ambition":43,"sadism":12},"emotions":{"anger":17.94,"resentment":9.860000000000001,"humiliation":8.9,"desperation":22.149999999999956,"last_updated":127,"last_support":27,"strain":29.61699999999999,"adaptation":0,"last_adapted":0,"stable_material_hours":0,"nested_collections":"LACUNA: cópia rasa; histórico não utilizado"},"failures":{},"known_places":{"market":{"map_id":302,"x":7,"y":13},"home":{"map_id":302,"x":2,"y":2},"work":{"map_id":302,"x":12,"y":2},"forage":{"map_id":302,"x":1,"y":13},"well_home":{"map_id":302,"x":2,"y":2},"well_rural":{"map_id":302,"x":1,"y":13},"sacred":{"map_id":302,"x":7,"y":1}},"market_observation":{"turn":127,"town_id":302,"stock":{"food":5,"grain":94,"water":0,"iron":64,"wood":120},"temporary_work":true,"offers_expire_at":151,"training_offer":null,"price":6,"price_turn":127},"groups":[],"factions":[],"known_groups":[31271,50846,33120,84785],"known_factions":[],"route_knowledge_count":2,"known_towns":[302,367],"journey":null,"training":{"target":null,"progress":0,"required":0},"devotion":71,"religion":"Culto da Aurora","goal":{"id":171335,"need_id":23621,"action":"steal_meal","score":76.73541358333333,"created_at":122,"target_id":null,"destination":{"map_id":302,"x":7,"y":13},"status":"active","outcome":""},"suspended_goal":{"id":157665,"need_id":23621,"action":"forage","score":49.0,"created_at":111,"target_id":null,"destination":{"map_id":302,"x":1,"y":13},"status":"suspended","outcome":""}}},"state_before":{"id":2464,"name":"Cael Valerius","hour":127,"alive":true,"profession":"mineiro","lod":"active","position":{"map_id":302,"x":7,"y":13},"residence":302,"hp":2,"hunger":100,"thirst":100,"fatigue":100,"money":2,"food":0,"water":0,"local_food":5,"local_water":0,"recoverable_deprivation":98,"starvation_hours":33,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{}},"state_after":{"id":2464,"name":"Cael Valerius","hour":127,"alive":true,"profession":"mineiro","lod":"active","position":{"map_id":302,"x":7,"y":13},"residence":302,"hp":2,"hunger":60,"thirst":100,"fatigue":100,"money":2,"food":0,"water":0,"local_food":4,"local_water":0,"recoverable_deprivation":98,"starvation_hours":33,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{}}}.

LACUNA: estoque local não prova que era conhecido, pagável, alcançável e consumível a tempo; o trace explica as últimas escolhas, mas não simula um contrafactual de sobrevivência.

### Caso with_owned_water: NPC #4803, h139

Registro: {"turn":139,"name":"Silas Kars","profession":"mineiro","town_id":864,"cause":"hunger","health":0,"hunger":100,"thirst":91,"fatigue":100,"food":0,"water":1,"last_meal":71,"last_drink":121,"recoverable_deprivation_damage":100,"damage_by_origin":{"hunger":88,"both":12},"last_successful_action":{"action":"drink","turn":121},"goal":"ask_meal","destination":null,"known_water_sources":[{"map_id":864,"x":7,"y":13},{"map_id":864,"x":2,"y":2},{"map_id":864,"x":1,"y":13}],"distance_to_water":0,"event_id":189882}.

Estado pré-fechamento de morte: {"id":4803,"name":"Silas Kars","hour":139,"alive":true,"profession":"mineiro","lod":"active","position":{"map_id":864,"x":1,"y":13},"residence":864,"hp":0,"hunger":100,"thirst":91,"fatigue":100,"money":3,"food":0,"water":1,"local_food":5,"local_water":0,"recoverable_deprivation":100,"starvation_hours":34,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{"forage_meal":147,"person_meal":148,"steal_person":149,"ask_meal":150}}.

Decisão recente: {"hour":137,"actor":4803,"selected_need":{"id":22299,"kind":"food","target":null,"base":100,"priority":100,"status":"active","source":"physiology","reason":"Fome","created":74,"expires":null,"context":{"emergency":true}},"winner":{"action":"steal_person","score":73.88950225,"target":4694,"destination":null,"terms":{"base":0.31,"greed":0.15600000000000003,"honesty":-0.0585,"authority":-0.1,"courage":0.038,"travel":-0.0,"pressure_moral_tolerance":0.023947511249999994},"feeding":{"EstimatedTimeUntilFoodConsumed":2,"EstimatedSurvivalMargin":2,"economically_viable":true,"survival_viable":true,"reason":null,"known_conditions":["UnknownPrice","DistantProduct"]},"action_pressure":null},"preparations":[],"execution":{"goal_at_entry":{"id":188341,"need_id":22299,"action":"steal_person","score":73.88950225,"created_at":137,"target_id":4694,"destination":null,"status":"active","outcome":""},"state_before":{"id":4803,"name":"Silas Kars","hour":137,"alive":true,"profession":"mineiro","category":"comum","lod":"active","position":{"map_id":864,"x":1,"y":13},"home":{"map_id":864,"x":2,"y":2},"workplace":{"map_id":864,"x":12,"y":2},"residence":864,"hp":6,"hunger":100,"thirst":87,"fatigue":100,"money":3,"food":0,"water":1,"recoverable_deprivation":94,"starvation_hours":32,"local_food":5,"local_water":0,"personality":{"honesty":13,"compassion":39,"courage":76,"independence":65,"greed":78,"diligence":58,"family_loyalty":81,"persistence":12,"temperament":37,"vengefulness":78,"ambition":71,"sadism":0},"emotions":{"anger":0.12,"resentment":6.180000000000012,"humiliation":0.0,"desperation":23.549999999999947,"last_updated":137,"last_support":47,"strain":34.16699999999999,"adaptation":0,"last_adapted":0,"stable_material_hours":0,"nested_collections":"LACUNA: cópia rasa; histórico não utilizado"},"failures":{"forage_meal":147,"person_meal":148},"known_places":{"market":{"map_id":864,"x":7,"y":13},"home":{"map_id":864,"x":2,"y":2},"work":{"map_id":864,"x":12,"y":2},"forage":{"map_id":864,"x":1,"y":13},"well_home":{"map_id":864,"x":2,"y":2},"well_rural":{"map_id":864,"x":1,"y":13},"sacred":{"map_id":864,"x":7,"y":1}},"market_observation":{"turn":137,"town_id":864,"stock":{"food":5,"grain":28,"water":0,"iron":76,"wood":120},"temporary_work":true,"offers_expire_at":161,"training_offer":null,"price":2,"price_turn":53},"groups":[],"factions":[],"known_groups":[56255,72074,86400,110613,102867,113139,132984],"known_factions":[],"route_knowledge_count":2,"known_towns":[864,911],"journey":null,"training":{"target":null,"progress":0,"required":0},"devotion":94,"religion":"Culto do Sol","goal":{"id":188341,"need_id":22299,"action":"steal_person","score":73.88950225,"created_at":137,"target_id":4694,"destination":null,"status":"active","outcome":""},"suspended_goal":{"id":173197,"need_id":22299,"action":"forage","score":43.5,"created_at":123,"target_id":null,"destination":{"map_id":864,"x":1,"y":13},"status":"suspended","outcome":""}},"success":false,"result":[false,"Não havia provisão acessível no alvo."],"state_after":{"id":4803,"name":"Silas Kars","hour":137,"alive":true,"profession":"mineiro","category":"comum","lod":"active","position":{"map_id":864,"x":1,"y":13},"home":{"map_id":864,"x":2,"y":2},"workplace":{"map_id":864,"x":12,"y":2},"residence":864,"hp":6,"hunger":100,"thirst":87,"fatigue":100,"money":3,"food":0,"water":1,"recoverable_deprivation":94,"starvation_hours":32,"local_food":5,"local_water":0,"personality":{"honesty":13,"compassion":39,"courage":76,"independence":65,"greed":78,"diligence":58,"family_loyalty":81,"persistence":12,"temperament":37,"vengefulness":78,"ambition":71,"sadism":0},"emotions":{"anger":0.12,"resentment":6.180000000000012,"humiliation":0.0,"desperation":23.549999999999947,"last_updated":137,"last_support":47,"strain":34.16699999999999,"adaptation":0,"last_adapted":0,"stable_material_hours":0,"nested_collections":"LACUNA: cópia rasa; histórico não utilizado"},"failures":{"forage_meal":147,"person_meal":148},"known_places":{"market":{"map_id":864,"x":7,"y":13},"home":{"map_id":864,"x":2,"y":2},"work":{"map_id":864,"x":12,"y":2},"forage":{"map_id":864,"x":1,"y":13},"well_home":{"map_id":864,"x":2,"y":2},"well_rural":{"map_id":864,"x":1,"y":13},"sacred":{"map_id":864,"x":7,"y":1}},"market_observation":{"turn":137,"town_id":864,"stock":{"food":5,"grain":28,"water":0,"iron":76,"wood":120},"temporary_work":true,"offers_expire_at":161,"training_offer":null,"price":2,"price_turn":53},"groups":[],"factions":[],"known_groups":[56255,72074,86400,110613,102867,113139,132984],"known_factions":[],"route_knowledge_count":2,"known_towns":[864,911],"journey":null,"training":{"target":null,"progress":0,"required":0},"devotion":94,"religion":"Culto do Sol","goal":{"id":188341,"need_id":22299,"action":"steal_person","score":73.88950225,"created_at":137,"target_id":4694,"destination":null,"status":"active","outcome":""},"suspended_goal":{"id":173197,"need_id":22299,"action":"forage","score":43.5,"created_at":123,"target_id":null,"destination":{"map_id":864,"x":1,"y":13},"status":"suspended","outcome":""}}},"state_before":{"id":4803,"name":"Silas Kars","hour":137,"alive":true,"profession":"mineiro","lod":"active","position":{"map_id":864,"x":1,"y":13},"residence":864,"hp":6,"hunger":100,"thirst":87,"fatigue":100,"money":3,"food":0,"water":1,"local_food":5,"local_water":0,"recoverable_deprivation":94,"starvation_hours":32,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{"forage_meal":147,"person_meal":148}},"state_after":{"id":4803,"name":"Silas Kars","hour":137,"alive":true,"profession":"mineiro","lod":"active","position":{"map_id":864,"x":1,"y":13},"residence":864,"hp":6,"hunger":100,"thirst":87,"fatigue":100,"money":3,"food":0,"water":1,"local_food":5,"local_water":0,"recoverable_deprivation":94,"starvation_hours":32,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{"forage_meal":147,"person_meal":148,"steal_person":149}}}.

Decisão recente: {"hour":138,"actor":4803,"selected_need":{"id":22299,"kind":"food","target":null,"base":100,"priority":100,"status":"active","source":"physiology","reason":"Fome","created":74,"expires":null,"context":{"emergency":true}},"winner":{"action":"ask_meal","score":67.1,"target":4800,"destination":null,"terms":{"base":0.125,"compassion":0.0975,"trust":0.10149999999999998,"reputation":0.0,"relationship":0.011500000000000002,"travel":-0.0},"feeding":{"EstimatedTimeUntilFoodConsumed":1,"EstimatedSurvivalMargin":1,"economically_viable":true,"survival_viable":true,"reason":null,"known_conditions":["UnknownPrice","DistantProduct"]},"action_pressure":null},"preparations":[],"execution":{"goal_at_entry":{"id":189651,"need_id":22299,"action":"ask_meal","score":67.1,"created_at":138,"target_id":4800,"destination":null,"status":"active","outcome":""},"state_before":{"id":4803,"name":"Silas Kars","hour":138,"alive":true,"profession":"mineiro","category":"comum","lod":"active","position":{"map_id":864,"x":1,"y":13},"home":{"map_id":864,"x":2,"y":2},"workplace":{"map_id":864,"x":12,"y":2},"residence":864,"hp":2,"hunger":100,"thirst":89,"fatigue":100,"money":3,"food":0,"water":1,"recoverable_deprivation":98,"starvation_hours":33,"local_food":4,"local_water":0,"personality":{"honesty":13,"compassion":39,"courage":76,"independence":65,"greed":78,"diligence":58,"family_loyalty":81,"persistence":12,"temperament":37,"vengefulness":78,"ambition":71,"sadism":0},"emotions":{"anger":0.12,"resentment":6.140000000000012,"humiliation":0.0,"desperation":23.949999999999946,"last_updated":138,"last_support":47,"strain":34.706499999999984,"adaptation":0,"last_adapted":0,"stable_material_hours":0,"nested_collections":"LACUNA: cópia rasa; histórico não utilizado"},"failures":{"forage_meal":147,"person_meal":148,"steal_person":149},"known_places":{"market":{"map_id":864,"x":7,"y":13},"home":{"map_id":864,"x":2,"y":2},"work":{"map_id":864,"x":12,"y":2},"forage":{"map_id":864,"x":1,"y":13},"well_home":{"map_id":864,"x":2,"y":2},"well_rural":{"map_id":864,"x":1,"y":13},"sacred":{"map_id":864,"x":7,"y":1}},"market_observation":{"turn":138,"town_id":864,"stock":{"food":4,"grain":30,"water":0,"iron":76,"wood":120},"temporary_work":true,"offers_expire_at":162,"training_offer":null,"price":2,"price_turn":53},"groups":[],"factions":[],"known_groups":[56255,72074,86400,110613,102867,113139,132984],"known_factions":[],"route_knowledge_count":2,"known_towns":[864,911],"journey":null,"training":{"target":null,"progress":0,"required":0},"devotion":94,"religion":"Culto do Sol","goal":{"id":189651,"need_id":22299,"action":"ask_meal","score":67.1,"created_at":138,"target_id":4800,"destination":null,"status":"active","outcome":""},"suspended_goal":{"id":173197,"need_id":22299,"action":"forage","score":43.5,"created_at":123,"target_id":null,"destination":{"map_id":864,"x":1,"y":13},"status":"suspended","outcome":""}},"success":false,"result":[false,"Não foi possível obter ajuda."],"state_after":{"id":4803,"name":"Silas Kars","hour":138,"alive":true,"profession":"mineiro","category":"comum","lod":"active","position":{"map_id":864,"x":1,"y":13},"home":{"map_id":864,"x":2,"y":2},"workplace":{"map_id":864,"x":12,"y":2},"residence":864,"hp":2,"hunger":100,"thirst":89,"fatigue":100,"money":3,"food":0,"water":1,"recoverable_deprivation":98,"starvation_hours":33,"local_food":4,"local_water":0,"personality":{"honesty":13,"compassion":39,"courage":76,"independence":65,"greed":78,"diligence":58,"family_loyalty":81,"persistence":12,"temperament":37,"vengefulness":78,"ambition":71,"sadism":0},"emotions":{"anger":0.12,"resentment":6.140000000000012,"humiliation":0.0,"desperation":23.949999999999946,"last_updated":138,"last_support":47,"strain":34.706499999999984,"adaptation":0,"last_adapted":0,"stable_material_hours":0,"nested_collections":"LACUNA: cópia rasa; histórico não utilizado"},"failures":{"forage_meal":147,"person_meal":148,"steal_person":149},"known_places":{"market":{"map_id":864,"x":7,"y":13},"home":{"map_id":864,"x":2,"y":2},"work":{"map_id":864,"x":12,"y":2},"forage":{"map_id":864,"x":1,"y":13},"well_home":{"map_id":864,"x":2,"y":2},"well_rural":{"map_id":864,"x":1,"y":13},"sacred":{"map_id":864,"x":7,"y":1}},"market_observation":{"turn":138,"town_id":864,"stock":{"food":4,"grain":30,"water":0,"iron":76,"wood":120},"temporary_work":true,"offers_expire_at":162,"training_offer":null,"price":2,"price_turn":53},"groups":[],"factions":[],"known_groups":[56255,72074,86400,110613,102867,113139,132984],"known_factions":[],"route_knowledge_count":2,"known_towns":[864,911],"journey":null,"training":{"target":null,"progress":0,"required":0},"devotion":94,"religion":"Culto do Sol","goal":{"id":189651,"need_id":22299,"action":"ask_meal","score":67.1,"created_at":138,"target_id":4800,"destination":null,"status":"active","outcome":""},"suspended_goal":{"id":173197,"need_id":22299,"action":"forage","score":43.5,"created_at":123,"target_id":null,"destination":{"map_id":864,"x":1,"y":13},"status":"suspended","outcome":""}}},"state_before":{"id":4803,"name":"Silas Kars","hour":138,"alive":true,"profession":"mineiro","lod":"active","position":{"map_id":864,"x":1,"y":13},"residence":864,"hp":2,"hunger":100,"thirst":89,"fatigue":100,"money":3,"food":0,"water":1,"local_food":4,"local_water":0,"recoverable_deprivation":98,"starvation_hours":33,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{"forage_meal":147,"person_meal":148,"steal_person":149}},"state_after":{"id":4803,"name":"Silas Kars","hour":138,"alive":true,"profession":"mineiro","lod":"active","position":{"map_id":864,"x":1,"y":13},"residence":864,"hp":2,"hunger":100,"thirst":89,"fatigue":100,"money":3,"food":0,"water":1,"local_food":4,"local_water":0,"recoverable_deprivation":98,"starvation_hours":33,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{"forage_meal":147,"person_meal":148,"steal_person":149,"ask_meal":150}}}.

LACUNA: estoque local não prova que era conhecido, pagável, alcançável e consumível a tempo; o trace explica as últimas escolhas, mas não simula um contrafactual de sobrevivência.

### Caso no_money: NPC #3695, h144

Registro: {"turn":144,"name":"Cael Vale","profession":"mineiro","town_id":601,"cause":"thirst","health":0,"hunger":12,"thirst":100,"fatigue":100,"food":0,"water":0,"last_meal":138,"last_drink":64,"recoverable_deprivation_damage":100,"damage_by_origin":{"hunger":12,"thirst":88},"last_successful_action":{"action":"work_for_meal","turn":138},"goal":"fill_water","destination":{"map_id":601,"x":1,"y":13},"known_water_sources":[{"map_id":601,"x":7,"y":13},{"map_id":601,"x":2,"y":2},{"map_id":601,"x":1,"y":13}],"distance_to_water":0,"event_id":196655}.

Estado pré-fechamento de morte: {"id":3695,"name":"Cael Vale","hour":144,"alive":true,"profession":"mineiro","lod":"active","position":{"map_id":601,"x":1,"y":13},"residence":601,"hp":0,"hunger":12,"thirst":100,"fatigue":100,"money":0,"food":0,"water":0,"local_food":2,"local_water":0,"recoverable_deprivation":100,"starvation_hours":31,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{"fill_water":155,"forage":144,"drink_well":149}}.

Decisão recente: {"hour":142,"actor":3695,"selected_need":{"id":35327,"kind":"rest","target":null,"base":100,"priority":100,"status":"active","source":"physiology","reason":"Cansaço","created":10,"expires":null,"context":{}},"winner":{"action":"fill_water","score":100,"target":null,"destination":{"map_id":601,"x":1,"y":13},"terms":{},"feeding":null,"action_pressure":null},"preparations":[{"input":{"action":"sleep","score":76.0,"target":null,"destination":{"map_id":601,"x":2,"y":2},"terms":{"base":0.5,"recovery_pressure":0.0,"travel":-0.12},"feeding":null,"action_pressure":null},"replacement":{"action":"fill_water","score":100,"target":null,"destination":{"map_id":601,"x":1,"y":13},"terms":{},"feeding":null,"action_pressure":null},"travel":12,"horizon":18}],"execution":{"goal_at_entry":{"id":194744,"need_id":35327,"action":"fill_water","score":100,"created_at":142,"target_id":null,"destination":{"map_id":601,"x":1,"y":13},"status":"active","outcome":""},"state_before":{"id":3695,"name":"Cael Vale","hour":142,"alive":true,"profession":"mineiro","category":"comum","lod":"active","position":{"map_id":601,"x":1,"y":13},"home":{"map_id":601,"x":2,"y":2},"workplace":{"map_id":601,"x":12,"y":2},"residence":601,"hp":6,"hunger":8,"thirst":100,"fatigue":100,"money":0,"food":0,"water":0,"recoverable_deprivation":94,"starvation_hours":29,"local_food":2,"local_water":0,"personality":{"honesty":62,"compassion":60,"courage":19,"independence":58,"greed":41,"diligence":79,"family_loyalty":17,"persistence":12,"temperament":15,"vengefulness":28,"ambition":45,"sadism":0},"emotions":{"anger":92.08000000000013,"resentment":57.76000000000003,"humiliation":49.89999999999995,"desperation":20.399999999999995,"last_updated":142,"last_support":-10000,"strain":20.608000000000008,"adaptation":0,"last_adapted":0,"stable_material_hours":0,"nested_collections":"LACUNA: cópia rasa; histórico não utilizado"},"failures":{"fill_water":153,"forage":144,"drink_well":149},"known_places":{"market":{"map_id":601,"x":7,"y":13},"home":{"map_id":601,"x":2,"y":2},"work":{"map_id":601,"x":12,"y":2},"forage":{"map_id":601,"x":1,"y":13},"well_home":{"map_id":601,"x":2,"y":2},"well_rural":{"map_id":601,"x":1,"y":13},"sacred":{"map_id":601,"x":7,"y":1}},"market_observation":{"turn":142,"town_id":601,"stock":{"food":2,"grain":60,"water":0,"iron":104,"wood":119},"temporary_work":true,"offers_expire_at":166,"training_offer":null,"price":14,"price_turn":118},"groups":[],"factions":[],"known_groups":[27001,33508,26942,54578,83895,84474,85578,126499,162537,159069],"known_factions":[],"route_knowledge_count":2,"known_towns":[601,648,3],"journey":null,"training":{"target":null,"progress":0,"required":0},"devotion":55,"religion":"Ordem da Maré","goal":{"id":194744,"need_id":35327,"action":"fill_water","score":100,"created_at":142,"target_id":null,"destination":{"map_id":601,"x":1,"y":13},"status":"active","outcome":""},"suspended_goal":null},"success":false,"result":[false,"Não há água para levar nesta fonte."],"state_after":{"id":3695,"name":"Cael Vale","hour":142,"alive":true,"profession":"mineiro","category":"comum","lod":"active","position":{"map_id":601,"x":1,"y":13},"home":{"map_id":601,"x":2,"y":2},"workplace":{"map_id":601,"x":12,"y":2},"residence":601,"hp":6,"hunger":8,"thirst":100,"fatigue":100,"money":0,"food":0,"water":0,"recoverable_deprivation":94,"starvation_hours":29,"local_food":2,"local_water":0,"personality":{"honesty":62,"compassion":60,"courage":19,"independence":58,"greed":41,"diligence":79,"family_loyalty":17,"persistence":12,"temperament":15,"vengefulness":28,"ambition":45,"sadism":0},"emotions":{"anger":92.08000000000013,"resentment":57.76000000000003,"humiliation":49.89999999999995,"desperation":20.399999999999995,"last_updated":142,"last_support":-10000,"strain":20.608000000000008,"adaptation":0,"last_adapted":0,"stable_material_hours":0,"nested_collections":"LACUNA: cópia rasa; histórico não utilizado"},"failures":{"fill_water":153,"forage":144,"drink_well":149},"known_places":{"market":{"map_id":601,"x":7,"y":13},"home":{"map_id":601,"x":2,"y":2},"work":{"map_id":601,"x":12,"y":2},"forage":{"map_id":601,"x":1,"y":13},"well_home":{"map_id":601,"x":2,"y":2},"well_rural":{"map_id":601,"x":1,"y":13},"sacred":{"map_id":601,"x":7,"y":1}},"market_observation":{"turn":142,"town_id":601,"stock":{"food":2,"grain":60,"water":0,"iron":104,"wood":119},"temporary_work":true,"offers_expire_at":166,"training_offer":null,"price":14,"price_turn":118},"groups":[],"factions":[],"known_groups":[27001,33508,26942,54578,83895,84474,85578,126499,162537,159069],"known_factions":[],"route_knowledge_count":2,"known_towns":[601,648,3],"journey":null,"training":{"target":null,"progress":0,"required":0},"devotion":55,"religion":"Ordem da Maré","goal":{"id":194744,"need_id":35327,"action":"fill_water","score":100,"created_at":142,"target_id":null,"destination":{"map_id":601,"x":1,"y":13},"status":"active","outcome":""},"suspended_goal":null}},"state_before":{"id":3695,"name":"Cael Vale","hour":142,"alive":true,"profession":"mineiro","lod":"active","position":{"map_id":601,"x":1,"y":13},"residence":601,"hp":6,"hunger":8,"thirst":100,"fatigue":100,"money":0,"food":0,"water":0,"local_food":2,"local_water":0,"recoverable_deprivation":94,"starvation_hours":29,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{"fill_water":153,"forage":144,"drink_well":149}},"state_after":{"id":3695,"name":"Cael Vale","hour":142,"alive":true,"profession":"mineiro","lod":"active","position":{"map_id":601,"x":1,"y":13},"residence":601,"hp":6,"hunger":8,"thirst":100,"fatigue":100,"money":0,"food":0,"water":0,"local_food":2,"local_water":0,"recoverable_deprivation":94,"starvation_hours":29,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{"fill_water":154,"forage":144,"drink_well":149}}}.

Decisão recente: {"hour":143,"actor":3695,"selected_need":{"id":35327,"kind":"rest","target":null,"base":100,"priority":100,"status":"active","source":"physiology","reason":"Cansaço","created":10,"expires":null,"context":{}},"winner":{"action":"fill_water","score":100,"target":null,"destination":{"map_id":601,"x":1,"y":13},"terms":{},"feeding":null,"action_pressure":null},"preparations":[{"input":{"action":"sleep","score":76.0,"target":null,"destination":{"map_id":601,"x":2,"y":2},"terms":{"base":0.5,"recovery_pressure":0.0,"travel":-0.12},"feeding":null,"action_pressure":null},"replacement":{"action":"fill_water","score":100,"target":null,"destination":{"map_id":601,"x":1,"y":13},"terms":{},"feeding":null,"action_pressure":null},"travel":12,"horizon":18}],"execution":{"goal_at_entry":{"id":196127,"need_id":35327,"action":"fill_water","score":100,"created_at":143,"target_id":null,"destination":{"map_id":601,"x":1,"y":13},"status":"active","outcome":""},"state_before":{"id":3695,"name":"Cael Vale","hour":143,"alive":true,"profession":"mineiro","category":"comum","lod":"active","position":{"map_id":601,"x":1,"y":13},"home":{"map_id":601,"x":2,"y":2},"workplace":{"map_id":601,"x":12,"y":2},"residence":601,"hp":2,"hunger":10,"thirst":100,"fatigue":100,"money":0,"food":0,"water":0,"recoverable_deprivation":98,"starvation_hours":30,"local_food":0,"local_water":0,"personality":{"honesty":62,"compassion":60,"courage":19,"independence":58,"greed":41,"diligence":79,"family_loyalty":17,"persistence":12,"temperament":15,"vengefulness":28,"ambition":45,"sadism":0},"emotions":{"anger":91.78000000000013,"resentment":57.720000000000034,"humiliation":49.79999999999995,"desperation":20.799999999999994,"last_updated":143,"last_support":-10000,"strain":21.116000000000007,"adaptation":0,"last_adapted":0,"stable_material_hours":0,"nested_collections":"LACUNA: cópia rasa; histórico não utilizado"},"failures":{"fill_water":154,"forage":144,"drink_well":149},"known_places":{"market":{"map_id":601,"x":7,"y":13},"home":{"map_id":601,"x":2,"y":2},"work":{"map_id":601,"x":12,"y":2},"forage":{"map_id":601,"x":1,"y":13},"well_home":{"map_id":601,"x":2,"y":2},"well_rural":{"map_id":601,"x":1,"y":13},"sacred":{"map_id":601,"x":7,"y":1}},"market_observation":{"turn":143,"town_id":601,"stock":{"food":0,"grain":60,"water":0,"iron":104,"wood":119},"temporary_work":true,"offers_expire_at":167,"training_offer":null,"price":14,"price_turn":118},"groups":[],"factions":[],"known_groups":[27001,33508,26942,54578,83895,84474,85578,126499,162537,159069],"known_factions":[],"route_knowledge_count":2,"known_towns":[601,648,3],"journey":null,"training":{"target":null,"progress":0,"required":0},"devotion":55,"religion":"Ordem da Maré","goal":{"id":196127,"need_id":35327,"action":"fill_water","score":100,"created_at":143,"target_id":null,"destination":{"map_id":601,"x":1,"y":13},"status":"active","outcome":""},"suspended_goal":null},"success":false,"result":[false,"Não há água para levar nesta fonte."],"state_after":{"id":3695,"name":"Cael Vale","hour":143,"alive":true,"profession":"mineiro","category":"comum","lod":"active","position":{"map_id":601,"x":1,"y":13},"home":{"map_id":601,"x":2,"y":2},"workplace":{"map_id":601,"x":12,"y":2},"residence":601,"hp":2,"hunger":10,"thirst":100,"fatigue":100,"money":0,"food":0,"water":0,"recoverable_deprivation":98,"starvation_hours":30,"local_food":0,"local_water":0,"personality":{"honesty":62,"compassion":60,"courage":19,"independence":58,"greed":41,"diligence":79,"family_loyalty":17,"persistence":12,"temperament":15,"vengefulness":28,"ambition":45,"sadism":0},"emotions":{"anger":91.78000000000013,"resentment":57.720000000000034,"humiliation":49.79999999999995,"desperation":20.799999999999994,"last_updated":143,"last_support":-10000,"strain":21.116000000000007,"adaptation":0,"last_adapted":0,"stable_material_hours":0,"nested_collections":"LACUNA: cópia rasa; histórico não utilizado"},"failures":{"fill_water":154,"forage":144,"drink_well":149},"known_places":{"market":{"map_id":601,"x":7,"y":13},"home":{"map_id":601,"x":2,"y":2},"work":{"map_id":601,"x":12,"y":2},"forage":{"map_id":601,"x":1,"y":13},"well_home":{"map_id":601,"x":2,"y":2},"well_rural":{"map_id":601,"x":1,"y":13},"sacred":{"map_id":601,"x":7,"y":1}},"market_observation":{"turn":143,"town_id":601,"stock":{"food":0,"grain":60,"water":0,"iron":104,"wood":119},"temporary_work":true,"offers_expire_at":167,"training_offer":null,"price":14,"price_turn":118},"groups":[],"factions":[],"known_groups":[27001,33508,26942,54578,83895,84474,85578,126499,162537,159069],"known_factions":[],"route_knowledge_count":2,"known_towns":[601,648,3],"journey":null,"training":{"target":null,"progress":0,"required":0},"devotion":55,"religion":"Ordem da Maré","goal":{"id":196127,"need_id":35327,"action":"fill_water","score":100,"created_at":143,"target_id":null,"destination":{"map_id":601,"x":1,"y":13},"status":"active","outcome":""},"suspended_goal":null}},"state_before":{"id":3695,"name":"Cael Vale","hour":143,"alive":true,"profession":"mineiro","lod":"active","position":{"map_id":601,"x":1,"y":13},"residence":601,"hp":2,"hunger":10,"thirst":100,"fatigue":100,"money":0,"food":0,"water":0,"local_food":0,"local_water":0,"recoverable_deprivation":98,"starvation_hours":30,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{"fill_water":154,"forage":144,"drink_well":149}},"state_after":{"id":3695,"name":"Cael Vale","hour":143,"alive":true,"profession":"mineiro","lod":"active","position":{"map_id":601,"x":1,"y":13},"residence":601,"hp":2,"hunger":10,"thirst":100,"fatigue":100,"money":0,"food":0,"water":0,"local_food":0,"local_water":0,"recoverable_deprivation":98,"starvation_hours":30,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{"fill_water":155,"forage":144,"drink_well":149}}}.

LACUNA: estoque local não prova que era conhecido, pagável, alcançável e consumível a tempo; o trace explica as últimas escolhas, mas não simula um contrafactual de sobrevivência.

### Caso with_money: NPC #2464, h128

Registro: {"turn":128,"name":"Cael Valerius","profession":"mineiro","town_id":302,"cause":"thirst","health":0,"hunger":62,"thirst":100,"fatigue":100,"food":0,"water":0,"last_meal":127,"last_drink":63,"recoverable_deprivation_damage":100,"damage_by_origin":{"hunger":43,"both":55,"thirst":2},"last_successful_action":{"action":"steal_meal","turn":127},"goal":"steal_meal","destination":{"map_id":302,"x":7,"y":13},"known_water_sources":[{"map_id":302,"x":7,"y":13},{"map_id":302,"x":2,"y":2},{"map_id":302,"x":1,"y":13}],"distance_to_water":0,"event_id":177760}.

Estado pré-fechamento de morte: {"id":2464,"name":"Cael Valerius","hour":128,"alive":true,"profession":"mineiro","lod":"active","position":{"map_id":302,"x":7,"y":13},"residence":302,"hp":0,"hunger":62,"thirst":100,"fatigue":100,"money":2,"food":0,"water":0,"local_food":7,"local_water":0,"recoverable_deprivation":100,"starvation_hours":34,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{}}.

Decisão recente: {"hour":126,"actor":2464,"selected_need":{"id":23621,"kind":"food","target":null,"base":100,"priority":100,"status":"selected","source":"physiology","reason":"Fome","created":63,"expires":null,"context":{"emergency":true}},"winner":{"action":"steal_meal","score":84.45149358333333,"target":null,"destination":{"map_id":302,"x":7,"y":13},"terms":{"base":0.35,"greed":0.11166666666666668,"honesty":-0.105,"courage":0.036,"travel":-0.01,"pressure_moral_tolerance":0.03959080125000001},"feeding":{"EstimatedTimeUntilFoodConsumed":2,"EstimatedSurvivalMargin":2,"economically_viable":true,"survival_viable":true,"reason":null,"known_conditions":["UnknownPrice","DistantProduct"]},"action_pressure":null},"preparations":[],"execution":null,"state_before":{"id":2464,"name":"Cael Valerius","hour":126,"alive":true,"profession":"mineiro","lod":"active","position":{"map_id":302,"x":6,"y":13},"residence":302,"hp":6,"hunger":100,"thirst":100,"fatigue":100,"money":2,"food":0,"water":0,"local_food":9,"local_water":0,"recoverable_deprivation":94,"starvation_hours":32,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{}},"state_after":{"id":2464,"name":"Cael Valerius","hour":126,"alive":true,"profession":"mineiro","lod":"active","position":{"map_id":302,"x":7,"y":13},"residence":302,"hp":6,"hunger":100,"thirst":100,"fatigue":100,"money":2,"food":0,"water":0,"local_food":9,"local_water":0,"recoverable_deprivation":94,"starvation_hours":32,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{}}}.

Decisão recente: {"hour":127,"actor":2464,"selected_need":{"id":23621,"kind":"food","target":null,"base":100,"priority":100,"status":"selected","source":"physiology","reason":"Fome","created":63,"expires":null,"context":{"emergency":true}},"winner":{"action":"steal_meal","score":86.38051358333333,"target":null,"destination":{"map_id":302,"x":7,"y":13},"terms":{"base":0.35,"greed":0.11166666666666668,"honesty":-0.105,"courage":0.036,"travel":-0.0,"pressure_moral_tolerance":0.03923590124999999},"feeding":{"EstimatedTimeUntilFoodConsumed":1,"EstimatedSurvivalMargin":1,"economically_viable":true,"survival_viable":true,"reason":null,"known_conditions":["NoMoney"]},"action_pressure":null},"preparations":[],"execution":{"goal_at_entry":{"id":171335,"need_id":23621,"action":"steal_meal","score":76.73541358333333,"created_at":122,"target_id":null,"destination":{"map_id":302,"x":7,"y":13},"status":"active","outcome":""},"state_before":{"id":2464,"name":"Cael Valerius","hour":127,"alive":true,"profession":"mineiro","category":"comum","lod":"active","position":{"map_id":302,"x":7,"y":13},"home":{"map_id":302,"x":2,"y":2},"workplace":{"map_id":302,"x":12,"y":2},"residence":302,"hp":2,"hunger":100,"thirst":100,"fatigue":100,"money":2,"food":0,"water":0,"recoverable_deprivation":98,"starvation_hours":33,"local_food":5,"local_water":0,"personality":{"honesty":21,"compassion":56,"courage":72,"independence":76,"greed":67,"diligence":21,"family_loyalty":73,"persistence":41,"temperament":10,"vengefulness":35,"ambition":43,"sadism":12},"emotions":{"anger":17.94,"resentment":9.860000000000001,"humiliation":8.9,"desperation":22.149999999999956,"last_updated":127,"last_support":27,"strain":29.61699999999999,"adaptation":0,"last_adapted":0,"stable_material_hours":0,"nested_collections":"LACUNA: cópia rasa; histórico não utilizado"},"failures":{},"known_places":{"market":{"map_id":302,"x":7,"y":13},"home":{"map_id":302,"x":2,"y":2},"work":{"map_id":302,"x":12,"y":2},"forage":{"map_id":302,"x":1,"y":13},"well_home":{"map_id":302,"x":2,"y":2},"well_rural":{"map_id":302,"x":1,"y":13},"sacred":{"map_id":302,"x":7,"y":1}},"market_observation":{"turn":127,"town_id":302,"stock":{"food":5,"grain":94,"water":0,"iron":64,"wood":120},"temporary_work":true,"offers_expire_at":151,"training_offer":null,"price":6,"price_turn":127},"groups":[],"factions":[],"known_groups":[31271,50846,33120,84785],"known_factions":[],"route_knowledge_count":2,"known_towns":[302,367],"journey":null,"training":{"target":null,"progress":0,"required":0},"devotion":71,"religion":"Culto da Aurora","goal":{"id":171335,"need_id":23621,"action":"steal_meal","score":76.73541358333333,"created_at":122,"target_id":null,"destination":{"map_id":302,"x":7,"y":13},"status":"active","outcome":""},"suspended_goal":{"id":157665,"need_id":23621,"action":"forage","score":49.0,"created_at":111,"target_id":null,"destination":{"map_id":302,"x":1,"y":13},"status":"suspended","outcome":""}},"success":true,"result":[true,"Alimento roubado. Fome reduzida."],"state_after":{"id":2464,"name":"Cael Valerius","hour":127,"alive":true,"profession":"mineiro","category":"comum","lod":"active","position":{"map_id":302,"x":7,"y":13},"home":{"map_id":302,"x":2,"y":2},"workplace":{"map_id":302,"x":12,"y":2},"residence":302,"hp":2,"hunger":60,"thirst":100,"fatigue":100,"money":2,"food":0,"water":0,"recoverable_deprivation":98,"starvation_hours":33,"local_food":4,"local_water":0,"personality":{"honesty":21,"compassion":56,"courage":72,"independence":76,"greed":67,"diligence":21,"family_loyalty":73,"persistence":41,"temperament":10,"vengefulness":35,"ambition":43,"sadism":12},"emotions":{"anger":17.94,"resentment":9.860000000000001,"humiliation":8.9,"desperation":22.149999999999956,"last_updated":127,"last_support":27,"strain":29.61699999999999,"adaptation":0,"last_adapted":0,"stable_material_hours":0,"nested_collections":"LACUNA: cópia rasa; histórico não utilizado"},"failures":{},"known_places":{"market":{"map_id":302,"x":7,"y":13},"home":{"map_id":302,"x":2,"y":2},"work":{"map_id":302,"x":12,"y":2},"forage":{"map_id":302,"x":1,"y":13},"well_home":{"map_id":302,"x":2,"y":2},"well_rural":{"map_id":302,"x":1,"y":13},"sacred":{"map_id":302,"x":7,"y":1}},"market_observation":{"turn":127,"town_id":302,"stock":{"food":5,"grain":94,"water":0,"iron":64,"wood":120},"temporary_work":true,"offers_expire_at":151,"training_offer":null,"price":6,"price_turn":127},"groups":[],"factions":[],"known_groups":[31271,50846,33120,84785],"known_factions":[],"route_knowledge_count":2,"known_towns":[302,367],"journey":null,"training":{"target":null,"progress":0,"required":0},"devotion":71,"religion":"Culto da Aurora","goal":{"id":171335,"need_id":23621,"action":"steal_meal","score":76.73541358333333,"created_at":122,"target_id":null,"destination":{"map_id":302,"x":7,"y":13},"status":"active","outcome":""},"suspended_goal":{"id":157665,"need_id":23621,"action":"forage","score":49.0,"created_at":111,"target_id":null,"destination":{"map_id":302,"x":1,"y":13},"status":"suspended","outcome":""}}},"state_before":{"id":2464,"name":"Cael Valerius","hour":127,"alive":true,"profession":"mineiro","lod":"active","position":{"map_id":302,"x":7,"y":13},"residence":302,"hp":2,"hunger":100,"thirst":100,"fatigue":100,"money":2,"food":0,"water":0,"local_food":5,"local_water":0,"recoverable_deprivation":98,"starvation_hours":33,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{}},"state_after":{"id":2464,"name":"Cael Valerius","hour":127,"alive":true,"profession":"mineiro","lod":"active","position":{"map_id":302,"x":7,"y":13},"residence":302,"hp":2,"hunger":60,"thirst":100,"fatigue":100,"money":2,"food":0,"water":0,"local_food":4,"local_water":0,"recoverable_deprivation":98,"starvation_hours":33,"training":{"target":null,"progress":0,"required":0},"journey":null,"failures":{}}}.

LACUNA: estoque local não prova que era conhecido, pagável, alcançável e consumível a tempo; o trace explica as últimas escolhas, mas não simula um contrafactual de sobrevivência.

## Perguntas sem resposta completa

“Por que não tentou uma alternativa que o produtor nunca enumerou?” exige gate/entrada que nem sempre foi retido. “O que sabia horas antes?” exige snapshot histórico de Facts/observações, não só IDs. “Era inevitável morrer?” não pode ser demonstrado apenas pela sequência observada, pois precisaria comparar alternativas com as mesmas restrições/tempo/RNG. “Por que um deus não respondeu?” exige registrar cada gate da avaliação naquele instante. Estas são LACUNAS DE OBSERVABILIDADE e estão detalhadas no relatório correspondente; nenhum silêncio foi preenchido como intenção narrativa.
