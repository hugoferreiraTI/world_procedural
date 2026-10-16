# Histórias emergentes observadas

Estes relatos são reconstruções auditáveis. Fatos, ações, conhecimentos anteriores e resultados vêm das campanhas finais; a intermediária problemática foi preservada separadamente. “História” aqui inclui episódio social, trajetória profissional e microepisódio econômico. Nenhum deles é apresentado como saga, guerra ou consciência política.

## H01. Investigação de responsável conhecido — Marie Alvor #1759

Campanha: **jogador**.

Participantes: Elena Luar #1753; Elena Bruma #1756; Marie Alvor #1759. Relações: amizade com Elena Bruma #1756: 85. Na primeira execução registrada, profissão caçador, caixa 1 e 1 ração(ões).


Necessidade `revenge`, motivo: Buscar informação ou reparação por dano conhecido; prioridade na primeira execução: 60,74. Fonte `event:1486366`. Antes da ação, conhecia o fato #1486366 do turno 9924 com confiança 60. Conteúdo: Elena Luar roubou comida no mercado de Dorlen.



Turno | Evento | ID | Consequência registrada
--- | --- | --- | ---
9924 | ItemStolen | 1486366 | Elena Luar roubou comida no mercado de Dorlen.
10008 | PersonLocated | 1498286 | Marie Alvor localizou Elena Luar.
10008 | InvestigationPerformed | 1498287 | Marie Alvor verificou o último local conhecido do responsável.
10014 | ThreatReported | 1499204 | Marie Alvor denunciou um acontecimento conhecido a Elena Bruma.


Turno | Ação | Sucesso | Resultado
--- | --- | --- | ---
10008 | investigate | True | Investigou o local conhecido; não houve confronto.
10014 | denounce | True | Denúncia registrada por autoridade que já conhece o fato.

Evento/percepção → conhecimento próprio → necessidade → prioridade → solução executada → consequências nos quadros acima. A duração entre a fonte causal e a última ação é 90h. Elena Bruma #1756 mantém impacto do fato #1486366: tags {'ladrão': 6}, confiança 0, confiança da evidência 0,60; Marie Alvor #1759 mantém impacto do fato #1486366: tags {'ladrão': 13}, confiança 0, confiança da evidência 0,60

Estado final no turno 10024: vivo, profissão caçador, 2 moedas, 1 rações, HP 100, fome 74, sede 68. Esse é o estado ao fim da campanha, não uma informação que os participantes necessariamente possuíam na época do episódio.


**Qualidade e limite:** A motivação de reparação está explícita na necessidade e o responsável na informação conhecida. Investigar e denunciar não equivalem a atacar, prender ou obter punição; nenhuma dessas consequências foi inventada.


## H02. Busca familiar e localização — Lyra Valerius #1458

Campanha: **jogador**.

Participantes: Bela Valerius #1455; Lyra Valerius #1458. Relações: filho_de com Bela Valerius #1455: 100; amizade com Bela Valerius #1455: 39. Na primeira execução registrada, profissão estudante, caixa 1 e 0 ração(ões).


Necessidade `family`, motivo: Ausência percebida após encontros anteriores; prioridade na primeira execução: 77,65. Fonte `event:60792`. Antes da ação, conhecia o fato #60792 do turno 332 com confiança 100. Conteúdo: Lyra Valerius não localiza um familiar há 96 horas.



Turno | Evento | ID | Consequência registrada
--- | --- | --- | ---
332 | AbsenceNoticed | 60792 | Lyra Valerius não localiza um familiar há 96 horas.
398 | FamilySearch | 73131 | Lyra Valerius verificou um local conhecido sem encontrar o familiar.
401 | PersonLocated | 73685 | Lyra Valerius localizou Bela Valerius.


Turno | Ação | Sucesso | Resultado
--- | --- | --- | ---
398 | check_relative | True | A pessoa não foi localizada nesta posição.
401 | check_relative | True | Pessoa localizada; o fato pode ser informado a outro personagem.

Evento/percepção → conhecimento próprio → necessidade → prioridade → solução executada → consequências nos quadros acima. A duração entre a fonte causal e a última ação é 69h. Não foi atribuída promoção nem mudança profissional a esses eventos; o ledger final não conserva um impacto reputacional específico deles.

Estado final no turno 10024: vivo, profissão estudante, 1 moedas, 0 rações, HP 100, fome 38, sede 31. Esse é o estado ao fim da campanha, não uma informação que os participantes necessariamente possuíam na época do episódio.


**Qualidade e limite:** A busca deriva de ausência percebida, não de um mapa global. Verificar sem encontrar e depois localizar são mudanças reais de situação. O conhecimento e a cronologia distinguem o encontro de retransmitir uma localização velha.


## H03. Luto e lembrança — Mira Hammer #1200

Campanha: **jogador**.

Participantes: Marie Ferros #912; Mira Hammer #1200; Silas Hammer #1203. Relações: casamento com Silas Hammer #1203: 90; amizade com Silas Hammer #1203: 71. Na primeira execução registrada, profissão governante, caixa 14 e 0 ração(ões).


Necessidade `grief`, motivo: Morte conhecida de Silas Hammer; prioridade na primeira execução: 81,50. Fonte `event:40567`. Antes da ação, conhecia o fato #40567 do turno 227 com confiança 30. Conteúdo: Silas Hammer morreu por privação.



Turno | Evento | ID | Consequência registrada
--- | --- | --- | ---
227 | CharacterDied | 40567 | Silas Hammer morreu por privação.
365 | ComfortGiven | 67042 | Marie Ferros ouviu Mira Hammer durante seu luto.


Turno | Ação | Sucesso | Resultado
--- | --- | --- | ---
362 | drink | True | Sede reduzida.
365 | seek_company | True | Buscou companhia para lidar com a perda.

Evento/percepção → conhecimento próprio → necessidade → prioridade → solução executada → consequências nos quadros acima. A duração entre a fonte causal e a última ação é 138h. Mira Hammer #1200 mantém impacto do fato #67042: tags {'prestativo': 6}, confiança 4, confiança da evidência 1,00

Estado final no turno 10024: morto, profissão governante, 0 moedas, 0 rações, HP 0, fome 100, sede 30. Esse é o estado ao fim da campanha, não uma informação que os participantes necessariamente possuíam na época do episódio.


**Qualidade e limite:** O luto e a lembrança são necessidades/ações registradas. A relação conhecida sustenta o episódio. Não foi acrescentada uma emoção específica nem se presume que todo familiar soube imediatamente da morte.


## H04. Ajuda familiar material — Lyra Luar #74

Campanha: **jogador**.

Participantes: Lyra Luar #74; Marie Luar #77. Relações: casamento com Marie Luar #77: 94; amizade com Marie Luar #77: 36. Na primeira execução registrada, profissão agricultor, caixa 8 e 1 ração(ões).


Necessidade `family`, motivo: Privação de familiar percebida em encontro; prioridade na primeira execução: 79,60. Fonte `event:222284`. Antes da ação, conhecia o fato #222284 do turno 1301 com confiança 100. Conteúdo: Lyra Luar percebeu a privação de Marie Luar.



Turno | Evento | ID | Consequência registrada
--- | --- | --- | ---
1301 | FamilyConcern | 222284 | Lyra Luar percebeu a privação de Marie Luar.
1333 | FamilySearch | 227170 | Lyra Luar verificou um local conhecido sem encontrar o familiar.
1345 | HelpGiven | 229022 | Lyra Luar entregou provisões a Marie Luar.


Turno | Ação | Sucesso | Resultado
--- | --- | --- | ---
1309 | ask_personal_help | False | Resposta sem avanço: no_information.
1333 | check_relative | True | A pessoa não foi localizada nesta posição.
1345 | give_supplies | True | Ajuda material prestada.

Evento/percepção → conhecimento próprio → necessidade → prioridade → solução executada → consequências nos quadros acima. A duração entre a fonte causal e a última ação é 44h. Marie Luar #77 mantém impacto do fato #229022: tags {'prestativo': 5}, confiança 4, confiança da evidência 1,00

Estado final no turno 10024: vivo, profissão agricultor, 9 moedas, 1 rações, HP 100, fome 60, sede 53. Esse é o estado ao fim da campanha, não uma informação que os participantes necessariamente possuíam na época do episódio.


**Qualidade e limite:** A ajuda é por water, conforme a necessidade, e usa transferência física. Uma doação não prova que a morte era certa nem que resolveu toda a pobreza do destinatário.


## H05. Denúncia a autoridade independente — Marie Alvor #1759

Campanha: **espectador**.

Participantes: Elena Luar #1753; Elena Bruma #1756; Marie Alvor #1759. Relações: amizade com Elena Bruma #1756: 85. Na primeira execução registrada, profissão caçador, caixa 2 e 1 ração(ões).


Necessidade `revenge`, motivo: Buscar informação ou reparação por dano conhecido; prioridade na primeira execução: 60,74. Fonte `event:1048608`. Antes da ação, conhecia o fato #1048608 do turno 6857 com confiança 100. Conteúdo: Elena Luar roubou comida no mercado de Dorlen.



Turno | Evento | ID | Consequência registrada
--- | --- | --- | ---
6857 | ItemStolen | 1048608 | Elena Luar roubou comida no mercado de Dorlen.
6948 | PersonLocated | 1061905 | Marie Alvor localizou Elena Luar.
6948 | InvestigationPerformed | 1061906 | Marie Alvor verificou o último local conhecido do responsável.
6954 | InformationShared | 1062872 | Marie Alvor informou Elena Bruma: Elena Luar roubou comida no mercado de Dorlen.
6954 | ThreatReported | 1062873 | Marie Alvor denunciou um acontecimento conhecido a Elena Bruma.


Turno | Ação | Sucesso | Resultado
--- | --- | --- | ---
6948 | investigate | True | Investigou o local conhecido; não houve confronto.
6954 | denounce | True | Informação transmitida.

Evento/percepção → conhecimento próprio → necessidade → prioridade → solução executada → consequências nos quadros acima. A duração entre a fonte causal e a última ação é 97h. Elena Bruma #1756 mantém impacto do fato #1048608: tags {'ladrão': 6}, confiança 0, confiança da evidência 0,60; Marie Alvor #1759 mantém impacto do fato #1048608: tags {'ladrão': 21}, confiança 0, confiança da evidência 1,00

Estado final no turno 10024: vivo, profissão caçador, 2 moedas, 2 rações, HP 100, fome 74, sede 68. Esse é o estado ao fim da campanha, não uma informação que os participantes necessariamente possuíam na época do episódio.


**Qualidade e limite:** A motivação de reparação está explícita na necessidade e o responsável na informação conhecida. Investigar e denunciar não equivalem a atacar, prender ou obter punição; nenhuma dessas consequências foi inventada.


## H06. Ajuda familiar material — Elena Corven #1097

Campanha: **espectador**.

Participantes: Cael Corven #1094; Elena Corven #1097. Relações: casamento com Cael Corven #1094: 95; amizade com Cael Corven #1094: 63. Na primeira execução registrada, profissão cozinheiro, caixa 8 e 1 ração(ões).


Necessidade `family`, motivo: Privação de familiar percebida em encontro; prioridade na primeira execução: 68,70. Fonte `event:11397`. Antes da ação, conhecia o fato #11397 do turno 52 com confiança 100. Conteúdo: Elena Corven percebeu a privação de Cael Corven.



Turno | Evento | ID | Consequência registrada
--- | --- | --- | ---
52 | FamilyConcern | 11397 | Elena Corven percebeu a privação de Cael Corven.
70 | FamilySearch | 13808 | Elena Corven verificou um local conhecido sem encontrar o familiar.
94 | HelpGiven | 17202 | Elena Corven entregou provisões a Cael Corven.


Turno | Ação | Sucesso | Resultado
--- | --- | --- | ---
52 | ask_personal_help | False | Resposta sem avanço: no_information.
70 | check_relative | True | A pessoa não foi localizada nesta posição.
94 | give_supplies | True | Ajuda material prestada.

Evento/percepção → conhecimento próprio → necessidade → prioridade → solução executada → consequências nos quadros acima. A duração entre a fonte causal e a última ação é 42h. Cael Corven #1094 mantém impacto do fato #17202: tags {'prestativo': 6}, confiança 5, confiança da evidência 1,00

Estado final no turno 10024: vivo, profissão cozinheiro, 4 moedas, 0 rações, HP 100, fome 72, sede 69. Esse é o estado ao fim da campanha, não uma informação que os participantes necessariamente possuíam na época do episódio.


**Qualidade e limite:** A ajuda é por water, conforme a necessidade, e usa transferência física. Uma doação não prova que a morte era certa nem que resolveu toda a pobreza do destinatário.


## H07. Reconhecimento — Tomas Montes #1219

Campanha: **espectador**.

Participantes: Tomas Montes #1219. Relações: nenhum vínculo familiar/amical relevante identificado entre esses participantes. Na primeira execução registrada, profissão cozinheiro, caixa 10 e 1 ração(ões).


Necessidade `status`, motivo: Buscar reconhecimento após encontrar Silas Valerius; prioridade na primeira execução: 44,00. Fonte `encounter:1452:0`. O fato-fonte não estava na memória limitada da primeira execução capturada. A necessidade/contexto conservavam a percepção anterior; o relatório não trata o registro global como conhecimento novo do NPC.



Turno | Evento | ID | Consequência registrada
--- | --- | --- | ---
30 | ResponsibilityFulfilled | 8605 | Tomas Montes cumpriu uma responsabilidade local.


Turno | Ação | Sucesso | Resultado
--- | --- | --- | ---
30 | work | True | Produção concluída com pagamento.

Evento/percepção → conhecimento próprio → necessidade → prioridade → solução executada → consequências nos quadros acima. A duração entre a fonte causal e a última ação é 30h. Não foi atribuída promoção nem mudança profissional a esses eventos; o ledger final não conserva um impacto reputacional específico deles.

Estado final no turno 10024: morto, profissão cozinheiro, 0 moedas, 0 rações, HP 0, fome 100, sede 48. Esse é o estado ao fim da campanha, não uma informação que os participantes necessariamente possuíam na época do episódio.


**Qualidade e limite:** Buscar reconhecimento está sustentado pela necessidade criada após encontro relevante. Um gesto concreto de ajuda/trabalho não significa receber título, cargo ou prestígio coletivo duradouro.


## H08. Proteção concreta — Silas Bruma #47

Campanha: **mundo**.

Participantes: Ruan Ferros #44; Silas Bruma #47. Relações: amizade com Ruan Ferros #44: 20. Na primeira execução registrada, profissão caçador, caixa 1 e 1 ração(ões).


Necessidade `protection`, motivo: Crime conhecido ameaça segurança pessoal/familiar; prioridade na primeira execução: 64,60. Fonte `event:433982`. Antes da ação, conhecia o fato #433982 do turno 2953 com confiança 60. Conteúdo: Ruan Ferros roubou comida no mercado de Dordor.



Turno | Evento | ID | Consequência registrada
--- | --- | --- | ---
2953 | ItemStolen | 433982 | Ruan Ferros roubou comida no mercado de Dordor.
3022 | ThreatAvoided | 443428 | Silas Bruma buscou um local seguro conhecido.


Turno | Ação | Sucesso | Resultado
--- | --- | --- | ---
3022 | avoid_threat | True | Afastou-se do local da ameaça.

Evento/percepção → conhecimento próprio → necessidade → prioridade → solução executada → consequências nos quadros acima. A duração entre a fonte causal e a última ação é 69h. Silas Bruma #47 mantém impacto do fato #433982: tags {'ladrão': 7}, confiança 0, confiança da evidência 0,60

Estado final no turno 10024: vivo, profissão caçador, 1 moedas, 0 rações, HP 100, fome 60, sede 68. Esse é o estado ao fim da campanha, não uma informação que os participantes necessariamente possuíam na época do episódio.


**Qualidade e limite:** O afastamento/proteção é ação social concreta. Não foi presumido um confronto, crime adicional, ferimento ou reação política.


## H09. Luto e lembrança — Elena Bruma #889

Campanha: **mundo**.

Participantes: Elena Bruma #889; Aldren Bruma #892. Relações: casamento com Aldren Bruma #892: 66; amizade com Aldren Bruma #892: 71. Na primeira execução registrada, profissão agricultor, caixa 28 e 0 ração(ões).


Necessidade `grief`, motivo: Morte conhecida de Aldren Bruma; prioridade na primeira execução: 72,95. Fonte `event:1306271`. Antes da ação, conhecia o fato #1306271 do turno 9450 com confiança 100. Conteúdo: Elena Bruma identificou os restos de Aldren Bruma.



Turno | Evento | ID | Consequência registrada
--- | --- | --- | ---
9450 | RemainsLocated | 1306271 | Elena Bruma identificou os restos de Aldren Bruma.
9564 | Remembrance | 1321356 | Elena Bruma dedicou um momento à memória de uma pessoa próxima.


Turno | Ação | Sucesso | Resultado
--- | --- | --- | ---
9564 | remember_relative | True | Visitou um local relacionado à perda.

Evento/percepção → conhecimento próprio → necessidade → prioridade → solução executada → consequências nos quadros acima. A duração entre a fonte causal e a última ação é 114h. Não foi atribuída promoção nem mudança profissional a esses eventos; o ledger final não conserva um impacto reputacional específico deles.

Estado final no turno 10024: vivo, profissão agricultor, 28 moedas, 0 rações, HP 100, fome 56, sede 71. Esse é o estado ao fim da campanha, não uma informação que os participantes necessariamente possuíam na época do episódio.


**Qualidade e limite:** O luto e a lembrança são necessidades/ações registradas. A relação conhecida sustenta o episódio. Não foi acrescentada uma emoção específica nem se presume que todo familiar soube imediatamente da morte.


## H10. Carreira interrompida e retomada — Darin Valerius #1477

Campanha: **jogador**.

Darin Valerius #1477 iniciou treinamento no turno 1284 e mudou de mineiro para cozinheiro no turno 4841. Duração da trajetória selecionada: 3557h. Houve 5 abandono(s) por falta de prática recente. A primeira prática capturada veio da necessidade `money` (Estabilizar renda baixa persistente), prioridade 83,60, caixa 2 e crédito 0/6.



Turno | ID | Evento | Descrição
--- | --- | --- | ---
1284 | 219858 | TrainingStarted | Darin Valerius começou a aprender cozinha.
1459 | 246294 | TrainingAbandoned | Darin Valerius abandonou a aprendizagem sem prática recente.
1554 | 260695 | TrainingStarted | Darin Valerius começou a aprender cozinha.
1728 | 286685 | TrainingAbandoned | Darin Valerius abandonou a aprendizagem sem prática recente.
1890 | 310624 | TrainingStarted | Darin Valerius começou a aprender cozinha.
2064 | 336449 | TrainingAbandoned | Darin Valerius abandonou a aprendizagem sem prática recente.
2076 | 338257 | TrainingStarted | Darin Valerius começou a aprender cozinha.
2250 | 363964 | TrainingAbandoned | Darin Valerius abandonou a aprendizagem sem prática recente.
2550 | 408890 | TrainingStarted | Darin Valerius começou a aprender cozinha.
2723 | 434671 | TrainingAbandoned | Darin Valerius abandonou a aprendizagem sem prática recente.
4625 | 716867 | TrainingStarted | Darin Valerius começou a aprender cozinha.
4841 | 749046 | ProfessionChanged | Darin Valerius deixou mineiro e tornou-se cozinheiro.

A cadeia comprovada é oportunidade conhecida → necessidade selecionada → prática com insumo e remuneração reais → pausa/abandono → nova prática → mudança profissional. As falhas anteriores de trabalho, quando capturadas, são correlação material; não provam por si mesmas que a saturação foi a motivação única. Não houve profissão forçada nem promoção instantânea.

Estado final no turno 10024: morto, profissão cozinheiro, 3 moedas, 0 rações, HP 0, fome 100, sede 12. Esse é o estado ao fim da campanha, não uma informação que os participantes necessariamente possuíam na época do episódio.

**Qualidade e limite:** existe continuidade e consequência profissional persistente. Recomeços também mostram repetição e uma aprendizagem frágil; não foram reescritos como uma aventura deliberada.


## H11. Carreira interrompida e retomada — Mira Stone #1142

Campanha: **mundo**.

Mira Stone #1142 iniciou treinamento no turno 1195 e mudou de mineiro para cozinheiro no turno 1705. Duração da trajetória selecionada: 510h. Houve 1 abandono(s) por falta de prática recente. A primeira prática capturada veio da necessidade `money` (Estabilizar renda baixa persistente), prioridade 83,60, caixa 1 e crédito 2/6.



Turno | ID | Evento | Descrição
--- | --- | --- | ---
1195 | 190729 | TrainingStarted | Mira Stone começou a aprender cozinha.
1561 | 241959 | TrainingAbandoned | Mira Stone abandonou a aprendizagem sem prática recente.
1639 | 252596 | TrainingStarted | Mira Stone começou a aprender cozinha.
1705 | 261836 | ProfessionChanged | Mira Stone deixou mineiro e tornou-se cozinheiro.

A cadeia comprovada é oportunidade conhecida → necessidade selecionada → prática com insumo e remuneração reais → pausa/abandono → nova prática → mudança profissional. As falhas anteriores de trabalho, quando capturadas, são correlação material; não provam por si mesmas que a saturação foi a motivação única. Não houve profissão forçada nem promoção instantânea.

Estado final no turno 10024: morto, profissão cozinheiro, 3 moedas, 0 rações, HP 0, fome 100, sede 10. Esse é o estado ao fim da campanha, não uma informação que os participantes necessariamente possuíam na época do episódio.

**Qualidade e limite:** existe continuidade e consequência profissional persistente. Recomeços também mostram repetição e uma aprendizagem frágil; não foram reescritos como uma aventura deliberada.


## H12. Profissional pobre em localidade com recursos — Cael Ferros #159

Campanha: **mundo**.

No turno final, Cael Ferros #159 tem profissão mineiro, 0 moeda(s) e 2 ração(ões). A localidade #144 possui 16708 moedas e 3 rações; uma ração custa 14 moedas. O setor está saturado nesse retrato. Elegibilidade temporária: True.


Necessidades ativas: [{'kind': 'money', 'priority': 92.8, 'status': 'selected'}, {'kind': 'rest', 'priority': 66.1000000000001, 'status': 'active'}, {'kind': 'work', 'priority': 50.7, 'status': 'active'}, {'kind': 'food_reserve', 'priority': 39.8, 'status': 'active'}, {'kind': 'water', 'priority': 72, 'status': 'active'}]. Conhecimento de mercado do próprio personagem: observação do turno 10022, preço observado 12. A disponibilidade física atual e o caixa municipal são informações do auditor; não são uma denúncia política ou percepção econômica global do NPC.

A causa da saturação é estoque, e o salário depende de atividade real. Não há evento de revolta nem emoção de ressentimento implementada. Este é um estado econômico interessante para uma futura história, não uma saga já executada.

Estado final no turno 10024: vivo, profissão mineiro, 0 moedas, 2 rações, HP 100, fome 53, sede 68. Esse é o estado ao fim da campanha, não uma informação que os participantes necessariamente possuíam na época do episódio.


## H13. Crédito parcial é trabalho real — Bela Douran #684

Campanha: **espectador**.

No turno 243, Bela Douran #684 executou trabalho na profissão lenhador. Necessidade `food`: Fome. Caixa 2 → 2; crédito 0/6 → 4/6. Resultado: Produção concluída com crédito salarial parcial. A ação foi bem-sucedida e não recebeu cooldown de fracasso por não ter transferido uma moeda inteira.


Estado final no turno 10024: vivo, profissão lenhador, 1 moedas, 0 rações, HP 100, fome 42, sede 68. Esse é o estado ao fim da campanha, não uma informação que os participantes necessariamente possuíam na época do episódio.

**Qualidade e limite:** é um microepisódio econômico que corrige causalidade. Não deve ser contado como uma grande história por si só, nem como garantia de estabilidade financeira.


## H14. Oferta conhecida desaparece antes da execução — Nora Valerius #1636

Campanha: **jogador**.

Nora Valerius #1636 conhecia oferta de distribuição observada no turno 387, capacidade 1. Tentou `temporary_service` no turno 405, com necessidade `money` (Estabilizar renda baixa persistente). A execução falhou honestamente: Não há refeições para distribuir. Caixa 6 → 6; alimento pessoal 0 → 0.



Turno | ID | Outro trabalho local registrado
--- | --- | ---
390 | 71713 | Ruan Ferros distribuiu 1 refeições locais.

A reprodução valida capacidade positiva no instante em que a oferta foi observada. Não houve criação de pagamento/comida para cumprir a promessa depois. Trabalhos locais próximos mostram concorrência possível, mas, sem reconstruir toda a sequência de consumo, não se atribui a perda a um concorrente específico.

Estado final no turno 10024: vivo, profissão mineiro, 4 moedas, 1 rações, HP 100, fome 68, sede 21. Esse é o estado ao fim da campanha, não uma informação que os participantes necessariamente possuíam na época do episódio.

**Qualidade e limite:** o mundo pode frustrar um plano legítimo; isso é diferente de anunciar uma vaga já esgotada. Não há reação política à frustração.


## H15. Intervenção do jogador com conclusão registrada

Campanha: **jogador**.

Evento #1399953, turno 9328: Auditor cumpriu o pedido de Iria Luar: Conseguir alimento para Iria Luar. Participantes: Auditor #7788 e Iria Luar #38. Contexto do evento: {'kind': 'food'}.


Quest #1399704, tipo `food`, criada 9326, concluída 9328; duração 2h. Contexto: {'source': 'physiology'}.


A política automatizada usou comandos públicos e concluiu a necessidade exigida pela quest. O fato da conclusão é comprovado; não se presume que o jogador salvou uma morte certa nem que cumpriu todas as quests oferecidas.

Estado final no turno 10024: vivo, profissão agricultor, 4 moedas, 1 rações, HP 100, fome 62, sede 24. Esse é o estado ao fim da campanha, não uma informação que os participantes necessariamente possuíam na época do episódio.


## H16. Sucessão após perda real de governante

Campanha: **espectador**.

Evento #67577, turno 367: Lyra Valerius assumiu Reino Valerius. Contexto: {}. A sucessão muda a liderança pelo sistema já existente; não produz uma guerra automaticamente.


Causa registrada: evento #67576, turno 367, Silas Valerius morreu por privação. Governante anterior: Silas Valerius #1452; sucessor: Lyra Valerius #1458; reino #1209. Vínculos do sucessor com o falecido: [('filho_de', 100)]. Registro da morte: fome 100, sede 33, comida carregada 0, causa `hunger`.


A consequência de liderança ocorreu na mesma hora: morte → callback de sucessão → escolha dinástica → novo governante. Essa decisão é uma regra institucional existente; não decorre de uma necessidade pessoal de ambição nem exige que o sucessor possuísse previamente o fato da morte. Os receptores explicitamente registrados do evento sucessório foram [1455, 1458].

Estado final no turno 10024: vivo, profissão estudante, 1 moedas, 0 rações, HP 100, fome 38, sede 25. Esse é o estado ao fim da campanha, não uma informação que os participantes necessariamente possuíam na época do episódio.


A morte deve ser lida no registro de privação da campanha, não reclassificada como assassinato. Uma troca de liderança não demonstra facções políticas, reivindicações militares ou legitimidade debatida, pois essas ações ainda não existem.


## Avaliação das histórias

Há relações, conhecimento limitado, decisões locais, reencontros, reparação sem confronto, ajuda material, mudanças profissionais e consequências persistentes. Algumas trajetórias atravessam centenas ou milhares de horas. Isso demonstra causalidade local além de uma simples lista de mortes.

A qualidade ainda é desigual: muitas cadeias são curtas, a motivação econômica domina carreiras, perdas derivam de privação e a denúncia costuma encerrar a reação sem uma investigação judicial continuada. A ausência de agressão limita os rumos da hostilidade. A Fase 3.2 melhora a honestidade dos registros e das ações; ampliar a variedade de causas e consequências exige funcionalidades futuras, não apenas aumentar a população.

Fontes: [historias_evidencias.json](</home/hugo/Área de trabalho/procedrual/reports/fase_3_2/historias_evidencias.json>), [diversidade_narrativa.json](</home/hugo/Área de trabalho/procedrual/reports/fase_3_2/diversidade_narrativa.json>) e os fluxos de cada campanha em [auditorias](</home/hugo/Área de trabalho/procedrual/reports/fase_3_2/auditorias>).

