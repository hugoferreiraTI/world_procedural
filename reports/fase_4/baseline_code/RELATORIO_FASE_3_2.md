# Fase 3.2 — Reserva preventiva, acesso econômico e coerência social

Relatório de implementação e auditoria. Data: 08/10/2026. Base: [fase_3_2.md](</home/hugo/Área de trabalho/procedrual/fase_3_2.md>). Versão final: `mvp-4-fase3.2-final`.

## 1. Resumo executivo

Os bugs de denúncia, informação repetida, crédito salarial, segunda ração, oferta esgotada e trabalho em instalação incompatível foram corrigidos. A pressão preventiva agora depende de cobertura, reposição conhecida, oportunidade e espera limitada.

Isso não equivale a ter resolvido a fome nem a diversidade narrativa. Nas campanhas finais, as mortes foram 331 → 335; seleções pessoais 25414 → 19818; satisfações pessoais 11744 → 13462. As tabelas abaixo mostram diferenças por campanha. Esses números são observações conjuntas das correções, não provas isoladas do efeito de cada mudança.

**Resposta à pergunta sobre ataques:** não existe ação de ataque entre NPCs. Hostilidade, crime e vingança produzem respostas sociais, mas não dano físico. Todas as mortes reais registradas nesta etapa continuam sendo privação. Envelhecimento e morte por idade também não estão implementados. O evento `CharacterKilled` pode ser interpretado, mas o motor não possui uma ação real que o produza durante essas campanhas.

## 2. Código e arquitetura preservados

O fluxo continua State/Knowledge → Need → Priority → Solutions → Goal → Action → Consequence → State. Nenhum planejador paralelo, controlador novo de fome ou economia paralela foi criado. A seleção continua no GoalSystem e o Utility AI continua comparando soluções da necessidade escolhida.

Geração, modelos persistentes, itens, navegação, eventos, população, relações, utility, quests, social e sucessão mantiveram seus módulos existentes. Fome +2/h, sede, fadiga, HP, dano por privação e recuperação por descanso não foram facilitados. Os parâmetros de Survival/Feeding anteriores foram preservados. A regra de geração permanece `mvp-4`; os hashes do estado inicial sem história são idênticos nas duas seeds, mascarando somente a identificação de versão.

O código anterior, todos os saves e relatórios anteriores, os 130 testes originais e a política pública do jogador foram preservados. Foram verificados 389 arquivos anteriores. O baseline está em [código baseline](</home/hugo/Área de trabalho/procedrual/reports/fase_3_2/baseline_code>) e as regras finais em [código congelado](</home/hugo/Área de trabalho/procedrual/reports/fase_3_2/codigo_congelado>). Saves anteriores permanecem disponíveis com o seu motor baseline; a nova identificação de regras impede carregá-los silenciosamente com regras diferentes.

## 3. Bugs corrigidos

A denúncia exclui o ator conhecido do crime, culpado, ameaça, alvo acusado e denunciante; a execução revalida essa independência. Informação já conhecida ou inadequada ao episódio não conta como resposta útil. Tentativas inúteis têm memória pequena por necessidade/interlocutor/fato, e informação realmente nova reabre o interlocutor.

A segunda ração continua financiável. Compra parcial e lote limitado conservam itens/dinheiro. Trabalho produtivo pode terminar com crédito fracionário, sem cooldown indevido. Ofertas de distribuição respeitam quota e estoque no instante da observação; a execução respeita o estado efetivo na chegada. A incompatibilidade de instalação bloqueia a intenção profissional.

A auditoria intermediária revelou dois casos adicionais: localização anterior ao episódio era aceita em ajuda material familiar; e aquisição adiada podia empatar com aquisição+refeição emergencial. Ambos foram corrigidos antes das campanhas finais. Os resultados intermediários foram preservados, sem esconder as falhas descobertas.

## 4. Modelo preventivo anterior

A fórmula era `26 + 8 × déficit/alvo + 0,2 × min(fome,50) + idade`, com idade limitada a 8. O teto ficava próximo de 52 sem ração e 48 com uma ração para alvo de duas. A espera saturava depois de cerca de 54h. Descanso, sede e renda podiam vencer repetidamente, mesmo em encontros economicamente favoráveis com o mercado.

Na investigação anterior de 1.000h por modo, a reserva venceu 2.018 de 376.485 avaliações ativas. Na janela preventiva mais relevante, fome <50 com déficit, venceu 1.805 de 33.319: 5,42%. Esses denominadores são avaliações; não significam 376.485 pessoas nem uma taxa medida nas 10.000h anteriores inteiras.

## 5. Novo modelo de cobertura e oportunidade

A cobertura estimada combina o tempo até a próxima refeição normal com 20h equivalentes por ração carregada. O risco compara essa cobertura com o custo conhecido de reposição e a margem de viagem. Uma rota planejada pode ampliar o horizonte e o alvo existente, limitado a seis rações.

A oportunidade presente pesa mais perto de um mercado com preço/estoque observados recentemente e orçamento para pelo menos uma unidade. O bônus máximo desse termo é 8 vezes a fração do déficit. Uma viagem que adia o próximo encontro conhecido com o mercado acrescenta pressão proporcional à lacuna de cobertura, limitada a 12 vezes essa fração. Sem conhecimento do trajeto ou do preço, o NPC não recebe dados globais.

A espera usa `18 × idade/(idade+72) × déficit/alvo`: cresce após 54h, mas converge e diminui quando há uma ração. A pressão final tem teto 85 e não recebe novamente o bônus temporal genérico. Fome/sede vitais continuam acima dela; sono crítico e luto forte continuam podendo vencer. Continuidade global de objetivo foi mantida. Não foi aplicado um aumento fixo de 30 pontos.

Esses valores são parâmetros do modelo contextual, não uma garantia de comportamento ideal. O resultado precisa ser medido; não existe meta de fazer 80% do elenco carregar duas rações.

## 6. Segunda ração

`known_unaffordable` agora avalia o déficit até o alvo solicitado. Para reserva 2, posse 1 e dinheiro 0, o ramo de renda continua disponível quando profissão/local/conhecimento permitem. Para posse 2, não há déficit normal.

No mercado, o custo usa a curva real. Fora dele, uma cotação recente fornece uma estimativa, não um preço remoto perfeito; sem cotação, o mínimo conhecido continua sendo somente um limite inferior. Isso muda a validade de uma solução, não obriga a prioridade a selecionar trabalho. Saturação, falta de profissão executável e outros bloqueios continuam legítimos.

## 7. Compra parcial e lote

A compra limita a quantidade por alvo, déficit, estoque e dinheiro. Cada unidade do lote percorre a curva marginal real de preço; o caixa municipal recebe exatamente o valor debitado do comprador. Há compra parcial quando só uma ração é possível.

Na manutenção de baixa pressão, o executor pode comprar uma unidade. Com pressão pelo menos 50, pode completar o déficit em lote limitado. A compra não reduz fome; somente a refeição consome uma ração e reduz fome. Uma compra para reserva não usa retrospectivamente várias horas de alimentação.
Campanha | Primeira ração comprada | Segunda incluída | Só a segunda | Compras parciais
--- | --- | --- | --- | ---
jogador | 19397 | 16255 | 1032 | 4174
espectador | 19566 | 15479 | 85 | 4172
mundo | 17989 | 14049 | 91 | 4031

## 8. Crédito salarial

O resultado de trabalho distingue pago, creditado, saturado, sem insumo, sem pagador, local incompatível e destino não alcançado. A interface anterior de sucesso/mensagem continua utilizável. `2/6` ou `4/6` legítimos são trabalho produtivo bem-sucedido, mesmo sem moeda inteira naquele instante.

O crédito é o campo persistente já existente. Acumula sextos, transfere moeda real do caixa municipal quando devido e subtrai os sextos pagos. Não é renda universal nem criação monetária. Sem pagador líquido, a atividade salarial pode falhar antes de produzir. Produção inexistente não gera salário. Os testes cobrem crédito, conversão única e save/load.
Campanha | Trabalhos creditados sem moeda inteira | Trabalhos com pagamento | Sem insumo | Saturados
--- | --- | --- | --- | ---
jogador | 3602 | 102513 | 1503 | 6418
espectador | 3194 | 103327 | 1486 | 6162
mundo | 2930 | 88681 | 2013 | 5840

## 9. Profissões saturadas

Os limites de armazenamento e insumos continuam reais. Se a cidade não precisa de mais madeira, ferro ou alimentos, a atividade correspondente pode não produzir nem pagar. A correção não obriga o município a adquirir produção inútil.

O personagem pode buscar as alternativas que já existem: venda de excedente, treinamento observado, coleta, ajuda ou serviço temporário compatível. Manutenção, transporte local e outras profissões novas não foram inventados. Quando esses caminhos faltam, subemprego e pobreza permanecem estados válidos. O censo separa pobreza com setor saturado de falha de interpretação salarial.

## 10. Trabalho temporário

Distribuição anuncia no máximo `min(quota restante, estoque de alimento/2)`. Uma unidade paga o trabalhador em alimento; outra é consumida como refeição servida à população abstrata. Quota zero ou estoque insuficiente não geram oferta disponível.

O preparo temporário usa o espaço e grão efetivamente disponíveis para preparar alimento, respeitando a ocupação compatível e a área rural existente. Observações registram instante, local, capacidade, requisitos e expiração de conhecimento em 24h. Não reservam uma vaga.

Assim, uma oferta pode ser verdadeira ao ser observada e desaparecer na viagem. A execução revalida quota, estoque e ocupação. O relatório distingue esse desaparecimento de um anúncio falso no instante da observação.

## 11. Intenção profissional e local

O motor não oferece trabalho profissional cuja instalação e mapa corrente não pertençam à economia exigida. Os líderes colocados em quartéis, mas associados economicamente à cidade natal, não receberam acesso remoto ao caixa ou mercado natal.

O bloqueio não cria economia de quartel nem salário novo. Uma profissão declarada pode continuar sem atividade executável naquela instalação. A mensagem de incompatibilidade explica esse caso, enquanto destino não alcançado continua sendo outro resultado. As regressões validam ausência de transferência remota.

## 12. Distribuição econômica

Campanha | Caixa municipal | Dinheiro NPCs vivos | Pobres no mapa municipal | Pobres com comida municipal | Pobres com setor saturado
--- | --- | --- | --- | --- | ---
jogador | 449048 | 2634 | 146 | 113 | 41
espectador | 477875 | 1976 | 156 | 137 | 54
mundo | 425733 | 2026 | 143 | 124 | 42
A tabela é um retrato final do auditor. “Pobre” significa caixa menor que o preço real de uma ração; não significa necessariamente fome imediata, pois pode haver comida carregada. Pobreza nos mapas municipais usa habitantes presentes; outros indicadores de campanha consultam o preço da cidade de vínculo para todos os vivos. Esses universos não são idênticos.

Média, mediana, caixa, preço, estoque, desemprego, saturação e capacidades locais foram registrados em quadros de 250h. Não foram transmitidos automaticamente aos NPCs.

## 13. Desigualdade observada

Há personagens abaixo do preço de uma refeição mesmo em localidades com caixa e alimentos. A concentração municipal foi preservada. Existem diferenças de elegibilidade, renda, profissão, conhecimento e localização; recursos municipais não são inventário pessoal.

O censo e as histórias mostram fatos materiais. Não foram acrescentados insatisfação política, luta de classes, sindicatos, revolução ou consciência de desigualdade. Tampouco se conclui que cada morte de pobre ocorreu por saturação: um retrato final não prova a sequência causal de todas as mortes.

## 14. Por que a desigualdade não foi automaticamente corrigida

A instrução pede causas sociais verdadeiras, incluindo resultados ruins. Distribuir caixa ou comida para todos apagaria desemprego e escassez de oportunidades reais. O trabalho foi corrigir interpretações e intenções incoerentes, preservando pagamentos e recursos físicos.

A única fonte monetária externa observada continua sendo a renda abstrata preexistente. O balanço separa essa fonte de transferências, e todos os checkpoints finais ficaram com diferença monetária zero. Não houve geração de NPC para fornecer ajuda ou preencher arbitrariamente uma vaga; a materialização anterior continua convertendo habitantes abstratos sob suas regras já existentes.

## 15. Denúncia ao culpado

Campanha | Denúncias anteriores | Ao culpado anteriormente | Denúncias finais válidas | Ao culpado agora
--- | --- | --- | --- | ---
jogador | 108 | 12 | 48 | 0
espectador | 135 | 23 | 48 | 0
mundo | 94 | 7 | 47 | 0
A exclusão usa conhecimento próprio: fato conhecido, contexto de culpado/ameaça e alvo acusado. Culpa desconhecida não exclui alguém por informação do auditor. A execução revalida profissão, presença, evidência e independência.

Protocolar uma denúncia é distinto de ensinar um fato novo ao guarda. Um guarda independente que já conhece o fato pode registrar a denúncia sem emitir uma falsa aquisição de conhecimento. O episódio não pode ser protocolado duas vezes. Sem autoridade válida, a necessidade não é satisfeita artificialmente.

## 16. Informação velha e repetição

A avaliação reutilizável distingue informação nova útil, confiança melhorada, já conhecida, temporalmente inadequada, irrelevante e ausência de informação. Localização respeita observações e buscas posteriores. Uma localização diferente mais recente que a última observação pode abrir uma pista anterior à ausência: muda o destino da busca sem confirmar encontro atual nem fechar a necessidade. Uma localização anterior à busca fracassada no mesmo lugar não reinicia aquele trajeto. A validação cobre busca e ajuda material familiar. Confiança superior pode melhorar uma observação incerta da mesma época. Morte antiga desconhecida continua sendo relevante.

`learn()==false` não termina como aprendizagem bem-sucedida. Resposta inútil não emite `InformationShared` como progresso. Quests existentes continuam aceitando as confirmações adequadas. A transmissão pública de um fato realmente novo pode aprender história sem fechar uma necessidade; aprendizagem e resolução são efeitos diferentes.

Tentativas recentes ficam na própria necessidade, com limite de oito registros, interlocutor, fato, resultado e prazo de 24h. Uma resposta inútil não gera cooldown genérico de todos os pedidos de informação. Um fato novo reabre aquele interlocutor imediatamente. Isso não garante que o ajudante saiba algo: buscas podem continuar bloqueadas.
Campanha | Sem informação | Já conhecida | Antiga para episódio | Nova útil | Confiança melhorada | Repetições evitadas
--- | --- | --- | --- | --- | --- | ---
jogador | 1500 | 0 | 156 | 0 | 0 | 3404
espectador | 1517 | 0 | 119 | 0 | 0 | 3471
mundo | 1471 | 0 | 117 | 0 | 0 | 3259

## 17. Testes

Passaram 179 testes: os 130 anteriores sem edição, entre eles as 25 regressões alimentares existentes, mais 49 novos. O arquivo de saída é [testes_finais.txt](</home/hugo/Área de trabalho/procedrual/reports/fase_3_2/testes_finais.txt>); as regressões novas estão em [test_phase32.py](</home/hugo/Área de trabalho/procedrual/tests/test_phase32.py>).

Foram cobertos destinatários culpados/independentes/desconhecidos, revalidação e save/load de denúncia; novidade, confiança, localização antiga, morte antiga, memória de respostas, reabertura e quests; financiamento de 0/1/2 rações, preço marginal, compra parcial, conservação e limite de estoque; crédito em sextos, conversão única, persistência e ausência de cooldown incorreto; quota, concorrência, estoque perdido, pagamento físico, oferta expirada e instalação incompatível.

Os cenários preventivos cobrem mercado próximo, segunda ração, luto forte, viagem longa conhecida, reposição distante, ausência real de caminho, sono e sede críticos. A regressão emergencial nova reproduz HP 5, fome 100 e sede 96: coletar+comer evita o adiamento que deixou o NPC sem uma ação isolada capaz de resgatá-lo na hora seguinte.

## 18. Auditoria curta

Campanha | Antes: reserva com fome <50 (%) | Final: mesma janela (%) | Reserva selecionada | Reserva ativa
--- | --- | --- | --- | ---
jogador | 6,80 | 15,08 | 7652 | 118709
espectador | 4,64 | 14,02 | 7390 | 118419
mundo | 4,65 | 14,88 | 7272 | 108643
São 1.000h por modo, comparadas à investigação anterior de 1.000h, sem extrapolar a taxa antiga como se ela cobrisse 10.000h. As rodadas curtas foram preservadas: `curta_v1`, `curta_v2`, `curta_v3` e `curta_final`. A última corresponde às regras finais.

As campanhas intermediárias foram preservadas em [intermediária v1](</home/hugo/Área de trabalho/procedrual/reports/fase_3_2/intermediaria_v1>) e [intermediária v2](</home/hugo/Área de trabalho/procedrual/reports/fase_3_2/intermediaria_v2>). A primeira encontrou informação familiar antiga aceita e aquisição adiada em emergência. A segunda confirmou as correções; a revisão semântica posterior acrescentou pistas de localização diferente sem confirmação falsa de encontro. Essas observações e casos controlados causaram regressões e correções; nenhum resultado foi apagado. Depois disso, o código foi congelado novamente.

## 19. Auditorias finais de 10.000h

Campanha | Seed | Horas | Erros de invariantes | Diferença monetária | Reprodução integral | Continuação +24h
--- | --- | --- | --- | --- | --- | ---
jogador | Dovha | 10000 | 0 | 0 | True | True
espectador | Dovha | 10000 | 0 | 0 | True | True
mundo | Mira | 10000 | 0 | 0 | True | True
Dovha jogador mantém exatamente o controlador anterior, usando comandos públicos e informações do próprio jogador. Os trajetos concretos podem divergir porque os encontros e oportunidades mudam. Dovha espectador e Mira mundo não possuem jogador guiando ações. O modo “mundo” acrescenta observação do auditor; não oferece visão global aos NPCs.

Cada campanha tem checkpoints, save final, alimentação, ações pessoais, contexto econômico, narrativa, desigualdade e episódios. A reprodução integral usa os comandos já registrados ou 10.000 passos canônicos e exige SHA idêntico ao save final. O checkpoint de 1.000h é idêntico ao teste curto final; save/load e continuação de 24h também foram validados. Verificação: [verificacao_final.json](</home/hugo/Área de trabalho/procedrual/reports/fase_3_2/verificacao_final.json>). Motor congelado: `0fc25d6ab2d71f3f24c4100bc9712a48a2f45109ac35b12b09cbc29b4fe8276e`.

## 20. Comparação antes/depois

Campanha | Mortes | Alvo completo final (%) | Rações médias finais | Seleções pessoais | Satisfações pessoais
--- | --- | --- | --- | --- | ---
jogador | 104 → 113 | 7,43 → 14,78 | 0,34 → 0,53 | 8954 → 7674 | 3946 → 4323
espectador | 103 → 103 | 10,98 → 17,48 | 0,36 → 0,60 | 8598 → 5926 | 3741 → 4347
mundo | 124 → 119 | 10,49 → 15,62 | 0,42 → 0,58 | 7862 → 6218 | 4057 → 4792
Os resultados não permitem declarar melhora geral por um único indicador. Reserva mais frequente, linguagem econômica correta e eliminação de denúncias incoerentes são resultados distintos de menos mortes, mais histórias ou distribuição mais eficiente. Nenhuma queda ou subida é atribuída isoladamente ao novo termo de prioridade sem um experimento de ablação.

“Satisfeita” é uma transição de necessidade, não uma saga. Muitas necessidades também fecham ao reencontrar alguém ou receber conhecimento sem que o NPC execute uma ação pessoal. Por isso, a análise narrativa abaixo usa episódios com ações e fatos registrados.

## 21. Mortalidade

Campanha | Antes: total | Final: total | Fome no limite | Sede no limite | Mortes com comida
--- | --- | --- | --- | --- | ---
jogador | 104 | 113 | 111 | 2 | 0
espectador | 103 | 103 | 99 | 4 | 0
mundo | 124 | 119 | 117 | 3 | 0
Fome e sede no limite se sobrepõem quando a causa é `both`; somá-las pode contar a mesma morte duas vezes. Todas as mortes reais são privação, não assassinato, combate ou velhice. Os registros de `CharacterKilled` dos testes controlados não foram misturados às campanhas.

Na intermediária v1, Lyra Hammer #520 morreu no turno 8311 com uma ração: na última decisão tinha HP 2, fome 100 e sede 98. Os contrafactuais controlados confirmam que comer sozinho ou beber sozinho já causariam morte na hora seguinte. Porém, na hora 8309 havia uma solução real de coletar+comer que teria evitado o conflito. A aquisição adiada foi escolhida por empate entre alternativas. Essa lacuna foi corrigida na seleção existente, sem aumentar HP, reduzir dano ou juntar arbitrariamente duas ações no último instante.

O caso permanece documentado na reprodução intermediária e em `terminal_intermediario_micro.json`. O número final na tabela não é uma promessa de imunidade futura: duas necessidades vitais simultâneas com recursos insuficientes ainda podem gerar mortes legítimas.

## 22. Reservas

Campanha | Avaliações ativas | Selecionada | Ativa → escolhida (%) | Escolhida com fome <50 (%) | Oportunidade conhecida perdida | Viagens iniciadas com déficit
--- | --- | --- | --- | --- | --- | ---
jogador | 934352 | 50250 | 5,38 | 10,41 | 46476 | 205482
espectador | 943475 | 47612 | 5,05 | 8,34 | 43737 | 207082
mundo | 861300 | 46855 | 5,44 | 9,27 | 38809 | 191712
A última coluna inclui deslocamentos para obter comida, água ou trabalho; não equivale a expedições longas deliberadamente desprotegidas. A pressão usa somente a oportunidade que o NPC conhece. O indicador de oportunidade “real” do auditor está separado nas métricas e nunca orienta a decisão.

Há cobertura estimada, reposição conhecida e pressão de espera nos exemplos de decisão. Os quadros de 250h mostram a distribuição de 0/1/2/3+ rações. Os tempos de busca/aquisição/consumo estão registrados por fluxo alimentar. Completar um alvo não é garantido: um NPC pode comer, ajudar alguém, viajar, perder a oferta ou ficar sem renda antes de mantê-lo.


Campanha | Buscas com fome <50, antes → final | Buscas com fome ≥80, antes → final | Buscas com HP ≤3, antes → final | Cobertura média com reserva ativa (h) | Tempo médio até alvo observado, antes → final (h)
--- | --- | --- | --- | --- | ---
jogador | 3128 → 9126 | 83724 → 67541 | 373 → 248 | 5,48 | 1,02 → 0,69
espectador | 1822 → 7964 | 85072 → 68628 | 414 → 332 | 5,27 | 0,44 → 0,63
mundo | 1897 → 8423 | 78753 → 61719 | 333 → 204 | 5,31 | 0,43 → 0,58

O tempo até o alvo inclui apenas buscas cuja aquisição atingiu o alvo registrado no início; não imputa sucesso às demais nem mede reserva sustentada. Cobertura é uma média por avaliação com déficit, não por pessoa.


Campanha | Reserva preventiva perdeu para descanso | Sede | Renda | Necessidades pessoais
--- | --- | --- | --- | ---
jogador | 49410 | 23551 | 19402 | 2145
espectador | 49514 | 23089 | 18733 | 1286
mundo | 44492 | 21720 | 16544 | 1280

## 23. Renda

Campanha | Moedas pagas em trabalho executado | Crédito novo em sextos | Produção profissional medida | Pobres abaixo do preço, todos os vivos
--- | --- | --- | --- | ---
jogador | 239994 | 1440182 | 368595 | 147
espectador | 244937 | 1469831 | 384607 | 157
mundo | 213825 | 1283124 | 337530 | 143
O pagamento em produto de serviços temporários continua separado de moeda. Crédito fracionário é progresso econômico real, mas não é uma moeda inteira já gastável. Um trabalhador pode produzir corretamente e continuar sem orçamento para comprar imediatamente. A correção semântica não transforma essa espera em riqueza automática.

A projeção temporal de renda continua usando taxas nominais; concorrência, insumos e produção parcial podem alterar o tempo concreto. A auditoria não atribui todas as mortes remanescentes a um único mecanismo salarial.

## 24. Estoques

Campanha | Comida municipal antes | Comida municipal final | Mercados vazios antes | Mercados vazios finais
--- | --- | --- | --- | ---
jogador | 9610 | 9209 | 8 | 10
espectador | 9495 | 9129 | 5 | 7
mundo | 8732 | 8250 | 8 | 10
Comida carregada por NPCs saiu de compra, produção, coleta ou transferência real. Os limites de estoque não foram elevados. A reserva pode deslocar parte do estoque para inventários pessoais; ela não cria alimento nem resolve todos os gargalos locais. A presença de estoque em outro município também não resolve acesso local: comércio intermunicipal não foi implementado.

## 25. Oportunidades e bloqueios

Campanha | Observações de distribuição | Execuções bem-sucedidas | Oferta conhecida perdida | Episódios sem guarda independente | Episódios sem evidência de denúncia
--- | --- | --- | --- | --- | ---
jogador | 437064 | 23520 | 376 | 3040 | 504
espectador | 452505 | 24479 | 357 | 3215 | 543
mundo | 402236 | 20816 | 301 | 1891 | 445
Observações são atualizações locais por indivíduo e instante, não vagas únicas. Oferta perdida exige capacidade positiva observada e falha posterior; pode resultar de quota ou estoque consumidos, sem atribuir concorrência a um ator específico quando isso não foi reconstruído.

A contagem de bloqueio social distingue falta de autoridade independente de falta do fato conhecido. Não se criou guarda substituto. Desemprego, ineligibilidade e escassez de informação continuam podendo bloquear necessidades. A reprodução integral conserva os exemplos e o SHA do save.

## 26. Métricas sociais

Campanha | Pedidos pessoais de ajuda | Pedidos com informação útil | Fatos úteis transmitidos | Melhorias de confiança transmitidas | Busca familiar: episódios com ação | Com confirmação direta | Com pedido de ajuda fracassado
--- | --- | --- | --- | --- | --- | --- | ---
jogador | 1662 | 0 | 15 | 1 | 1018 | 86 | 80
espectador | 1639 | 0 | 19 | 0 | 792 | 88 | 78
mundo | 1589 | 0 | 5 | 0 | 945 | 88 | 208
Denúncias válidas, fatos úteis, confiança melhorada, respostas inúteis e repetição evitada foram registrados separadamente. As três campanhas finais têm zero denúncias tratadas como independentes ao próprio acusado e zero respostas marcadas como sucesso com mensagem “sem avanço”. Os eventos de transmissão útil têm `utility` no contexto.

Pedidos pessoais também podem pedir companhia ou abrir quest; nem todos são perguntas informativas. Não houve informação útil recebida pela ação autônoma de pedir ajuda nestas campanhas. As transmissões úteis registradas vieram de outros caminhos, como denúncia ou comando do jogador. Portanto, a ausência de progresso informativo continua sendo uma limitação observada, apesar das regressões demonstrarem que informação nova válida pode ajudar. Não se atribuiu fechamento de necessidade a uma informação indireta sem evidência suficiente. Confirmação direta e pedido fracassado podem ocorrer no mesmo episódio; os números não são categorias excludentes nem incluem todos os reencontros espontâneos.

Isso não significa justiça completa. A denúncia registra conhecimento e resolve aquela intenção de procurar uma autoridade; não implementa julgamento, prisão, julgamento tardio de um crime nem punição por assassinato. O guarda continua com a intervenção local já existente. A redução de transmissões pode ser eliminação de duplicatas, mas não é automaticamente perda de informação útil. Veja [dados completos das campanhas](</home/hugo/Área de trabalho/procedrual/reports/fase_3_2/auditorias>) e as histórias.

## 27. Histórias emergentes observadas

A seguir estão episódios reais reconstruídos dos registros. As histórias completas também foram salvas em arquivo separado. Não há ficção acrescentada para preencher lacunas, nem emoção ou motivação presumida a partir de um resultado material.

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

## 28. Diversidade narrativa

Campanha | Episódios com ação | 2 eventos | 3 eventos | 4+ eventos | Duração ≥168h | Personagens ≥720h
--- | --- | --- | --- | --- | --- | ---
jogador | 4615 → 3790 | 2612 → 2581 | 218 → 60 | 29 → 3 | 27 → 28 | 165 → 154
espectador | 4864 → 3357 | 2784 → 2230 | 232 → 56 | 19 → 2 | 14 → 8 | 165 → 156
mundo | 4429 → 3284 | 2604 → 2223 | 173 → 35 | 18 → 1 | 8 → 7 | 147 → 128

Campanha | Sem cuidado alimentar direto/crime alimentar | Com evento do jogador | Sem evento do jogador | Necessidades pessoais interrompidas por morte
--- | --- | --- | --- | ---
jogador | 1937 | 2 | 3788 | 99
espectador | 1588 | 0 | 3357 | 93
mundo | 1660 | 0 | 3284 | 109

Evento, antes → final | Jogador | Espectador | Mundo
--- | --- | --- | ---
ProfessionChanged | 13 → 11 | 5 → 5 | 23 → 10
ResponsibilityFulfilled | 3 → 2 | 2 → 2 | 0 → 0
Remembrance | 2 → 1 | 3 → 2 | 1 → 4
ItemStolen | 9154 → 9976 | 9680 → 9579 | 9473 → 9850
InvestigationPerformed | 48 → 21 | 57 → 21 | 30 → 19
ProtectionGiven | 0 → 3 | 2 → 3 | 0 → 1
FamilySearch | 1946 → 1936 | 2204 → 1653 | 2076 → 1664
PersonLocated | 564 → 534 | 502 → 493 | 458 → 456
QuestCompleted | 0 → 1 | 0 → 0 | 0 → 0
SuccessionChanged | 9 → 11 | 10 → 11 | 8 → 7
O primeiro quadro usa o mesmo agrupamento anterior: personagem, necessidade, início do episódio e fonte, com eventos compatíveis registrados na hora da ação. A duração parte do evento causal conhecido. Esses episódios não incluem toda a trajetória profissional/sucessória, apresentada à parte nas histórias.

O segundo quadro acrescenta uma classificação mais estrita: exclui cuidado familiar por comida e crime alimentar, mas conserva, por exemplo, busca, luto e cuidado por água. Isso não prova independência total da fisiologia: o luto pode ter começado por morte de fome. “Sem jogador” significa nenhum evento com o jogador no episódio; não prova que o mundo inteiro não sofreu influência indireta dele.

Menos episódios extensos ou menos investigações significa que a variedade/continuidade não foi automaticamente resolvida. A remoção de retransmissões falsas também reduz artificialmente cadeias que antes pareciam longas. Ainda assim, os dados não autorizam substituir toda redução por uma explicação favorável: prioridade, renda e caminhos sociais continuam competindo, e as causas narrativas permanecem estreitas.

## 29. Bugs remanescentes e riscos observados

Não reapareceram denúncia ao próprio acusado, aprendizagem duplicada tratada como avanço, cooldown por mero crédito parcial, anúncio de quota zero como oportunidade verdadeira ou acesso remoto à economia natal nas regressões e verificações finais.

Isso não é prova de ausência de qualquer bug. O calendário e as regras simplificadas podem deixar fome/sede convergirem tarde demais; a projeção de salário é nominal; guarda conhecido pode desaparecer ou não ter evidência na chegada; fatos relevantes podem sair da memória limitada. Os registros finais permitem investigar esses casos sem confundi-los automaticamente com erro.

Há limitações funcionais relevantes: pedidos de ajuda material por água possuem caminhos menos diretos; treinamento pode reiniciar repetidamente; reconhecimento frequentemente termina em um único gesto; denunciar não abre processo de justiça persistente; não existe agressão/combate. Foram registrados como limitações, sem acrescentar sistemas fora do escopo.

## 30. Limitações da análise

Duas seeds e três modos não representam todos os mundos possíveis. As campanhas mudam várias correções conjuntamente e divergem após decisões iniciais; não isolam a contribuição de cada parâmetro. O jogador automatizado tem política limitada, não avalia criativamente toda quest disponível. Quadros de 250h são amostras, não estado de cada pessoa em todas as horas.

Contagens de avaliação, observação, transição, evento e episódio têm denominadores diferentes. Fato conhecido pelo auditor não é conhecimento do NPC. Causalidade entre trabalho saturado e mudança de carreira só é afirmada quando a necessidade/decisão sustentam essa ligação; mera proximidade temporal é apresentada como correlação.

A implementação da Fase 3.2 corrige coerência local. Ela não demonstra que o projeto já produz sagas, guerras, conflitos políticos ou violência autônoma, nem que está pronto para multiplicar população sem ampliar a auditoria de comportamento.

## 31. Recomendações para a Fase 4

Primeiro, manter estas regressões e a observabilidade quando mudar a população, sem remover pobreza legítima para melhorar estatísticas. Medir o custo e as consequências de ampliar elenco/LOD com as mesmas cadeias causais.

Antes de atribuir riqueza narrativa à escala, aprofundar os caminhos locais já existentes: ajuda material, expectativas de renda, continuidade de carreira, localização e resposta real à denúncia. Separar “necessidade satisfeita” de resolução social duradoura.

Para a questão levantada sobre inimigos: uma etapa própria de agressão e combate local pode produzir defesa, fuga, ferimentos, mortes violentas, testemunhas e repercussão familiar. Não é necessário implementar guerra entre reinos para haver confronto pessoal. Mas hostilidade não deve implicar ataque automático: motivação conhecida, risco, coragem, relações e consequências precisam participar do fluxo atual.

Ao introduzir `CharacterKilled` como consequência real, também revisar sucessão, população, evidência, atribuição de culpa e proteção para reagirem corretamente à nova causa de morte. Política, religião, deuses, migração, redistribuição e guerras continuam fora desta entrega. A economia atual pode alimentar conflitos futuros, mas eles ainda precisam existir como ações e consequências executáveis.

