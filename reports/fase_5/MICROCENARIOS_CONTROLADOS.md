# Capacidade técnica — cenários controlados da Fase 5

Estes cenários **não são histórias da campanha natural**. Eles criam condições raras ou isolam causas para testar regras. Os nomes, recursos, vínculos e lugares são do mundo gerado; danos, tempo e traços podem ser ajustados explicitamente pelo teste.

Fonte: `tests/test_phase5.py`. São 30 regressões compostas.

| Casos | Regra verificada |
|---|---|
| 01–02 | Problema comunicado, encontro e afinidade são necessários; não formar repetidamente o mesmo grupo para a mesma pessoa; não oferecer adesão quando o NPC já ocupa as três vagas de grupo. |
| 03–06 | Proposta precisa chegar à autoridade; personalidade/recursos mudam a resposta; comida aprovada sai de estoque existente; grupo reage apenas à decisão recebida. |
| 07 | Restrição conhecida pode gerar antagonismo coletivo sem ataque automático. |
| 08 | Grupo precisa de continuidade, membros, investimento e recursos para virar facção. O dinheiro é transferido. |
| 09–11 | General único, substituição com sobrevivente disponível, patente conservada durante patrulha; promoção exige feitos/vínculo/tempo/vaga; instituição não conhece ocorrência antes de receber relatório. |
| 12–15 | Deus real é separado de crença; mortal adorado permanece mortal; rumor conserva fonte/confiança; intervenção custa energia, tem intervalo e testemunhas locais. |
| 16–18 | Feito desconhecido não gera fama; repetição do mesmo fato não inflaciona nem ultrapassa o limite; epíteto e alcance dependem de evidência e circulação. |
| 19–20 | Potencial excepcional não dá força imediata; treino custa esforço; aspiração produz intenção persistente; Justiça continua subjetiva. |
| 21–22 | Matar um deus não concede apoteose; apropriação legítima é outra ação; domínio novo depende do mortal. Receber o fato pode produzir hipótese sobre o sucessor, sem certeza ou conversão automática. Oração ao mortal ascendido alcança sua divindade real; veneração comum não cria esse acesso. Save/load conserva os estados. |
| 23–26 | Oportunidade exige presença/capacidade/intenção; `finish` válido é fatal sem nova rolagem; misericórdia conserva vida e grievance; perigo situacional precisa de dano/ameaça grave recente. |
| 27–28 | Item ganha história objetiva sem buff automático; transferência conserva a identidade; save/load conserva regras, consultas são puras e continuação mantém o RNG. |
| 29 | Prefeito vai ao atendimento sem saber de proposta remota; entrega continua presencial; líder de facção atravessa entrada real por rota conhecida e conserva residência. Viagem temporária conserva o prefeito; migração de residência abre sucessão e transfere demandas já recebidas ao novo titular. |
| 30 | Recusa remota não altera o conhecimento do grupo; representante precisa consultar resposta pública no mercado; reaprender a mesma resposta não repete aumento de pressão. |

A suíte anterior também foi preservada. Falhas encontradas durante desenvolvimento e campanhas curtas são documentadas no relatório técnico e mantidas nos logs. Nenhum resultado controlado será contado como morte divina, apoteose, execução ou culto natural nas 5.000 horas.

Os casos 02, 22 e 29 foram ampliados depois da longa para conferir os ajustes finais. A quantidade permanece em 30 regressões compostas; seus novos resultados pertencem ao código de entrega.
