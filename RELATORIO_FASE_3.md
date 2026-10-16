# Fase 3 — implementação, auditoria e limites

Especificação: **`fase_3.md`**, preservada integralmente a partir do texto enviado.
Versão: **mvp-4**. Foram mantidos os serviços existentes e acrescentados diagnóstico
econômico, trabalho útil, formação culinária, reposição limitada e observabilidade.
Fome, sede, cansaço, dano, recuperação e duração das necessidades sociais não foram
reduzidos para alterar a distribuição de comportamentos.

**Resultado: a economia passou a reagir à falta de conversão e de profissionais, mas a dominância de sobrevivência não foi resolvida.** Os mercados vazios diminuíram nas três campanhas; pobreza e mortalidade do elenco inicial ficaram maiores. As seleções pessoais e satisfações também diminuíram em números absolutos. Isso impede declarar a fase uma melhora geral na qualidade das histórias. As diferenças de geração entre versões limitam a atribuição causal.

Os resultados completos estão em [comparação](reports/fase_3/COMPARACAO.md),
[histórias observadas](reports/fase_3/HISTORIAS.md) e
[modelo econômico](reports/fase_3/MODELO_ECONOMICO.md). As campanhas finais estão em
`reports/fase_3/auditorias/`, nas pastas `jogador`, `espectador` e `mundo`.

## 1. Estado anterior

O MVP já tinha mercado com estoque e dinheiro, preços regionais, produção, salários,
trabalho rural por alimento, conhecimento individual, relações familiares, eventos,
quests e persistência determinística. A Fase 2 acrescentara necessidades pessoais,
mas as três campanhas anteriores dedicavam 91,63%–92,48% das seleções à fisiologia.
Não existiam demanda profissional adaptativa, formação nem materialização.

O núcleo anterior foi preservado em `reports/fase_3/baseline_code/`. Os documentos
e a leitura anterior à implementação estão registrados no
[levantamento](reports/fase_3/LEVANTAMENTO.md). Os saves históricos continuam intactos.

## 2. Gargalos confirmados antes da mudança

Nas campanhas da Fase 2, 26/31/31 mercados terminaram sem alimento. Respectivamente
26/31/30 desses mercados tinham trigo cheio: uma falta de conversão podia provocar
a mesma resposta coletiva que uma falta de matéria-prima. Estoque cheio interrompia
o trabalho remunerado, sem alternativa suficiente; espaço parcial recusava lotes
inteiros; a alternativa financeira para fome usava o corte fixo de cinco moedas.

Profissões tinham elenco inicial fixo, sem recomposição após mortes. População
nominal não distinguia residentes mortos dos vivos. A instrumentação social não
separava pressão concorrente de falta de solução. Uma reprodução instrumentada do
núcleo antigo, antes de implementar prevenção, registrou em 1.000 horas: 101 mortes,
48 com fome no limite, 20 com sede no limite e 33 com ambas. Esse diagnóstico
está em `reports/fase_3/agua_baseline_1000.json`; não é uma comparação controlada
com a geração da nova versão.

## 3. Sistemas existentes reutilizados

`NeedSystem` continua produzindo pressões, `GoalSystem` alternativas e objetivos,
`utility` avaliação por personalidade. Trabalho e aprendizagem usam
`ProfessionSystem`; preço, diagnóstico e resposta diária usam `Economy`.
Inventários, eventos, conhecimento, grafo, quests, navegação e repositório JSON
continuam compartilhados. O motor conserva a ordem ação → fisiologia → morte.

As ações coletivas usam os mesmos `Solution`, `Goal` e avaliação de utilidade,
com prioridades contextuais para a instituição. Publicar uma oferta não força
um NPC a caminhar ou aceitar a ocupação.

## 4. Sistemas deliberadamente não recriados

Não foi criado outro planejador, Utility AI, economia, sistema profissional,
gerenciador de eventos, grafo, persistência ou sistema financeiro pessoal.
`Population` é um auxiliar de contabilidade censitária, não uma segunda IA.
Diagnóstico e auditoria descrevem decisões; não geram uma história roteirizada.

Guerra, exércitos, combate, equipamento, intervenção divina, religião organizada,
política complexa, caravanas, nascimento, envelhecimento e herança continuam fora
do escopo solicitado.

## 5. Novo diagnóstico econômico

| Motivo | O que o diagnóstico consegue identificar |
|---|---|
| `RAW_MATERIAL_SHORTAGE` | Reserva de trigo insuficiente frente ao fluxo alimentar. |
| `PROCESSING_CAPACITY_SHORTAGE` | Cozinha ausente ou capacidade nominal abaixo da demanda. |
| `LABOR_SHORTAGE` | Cozinha existente sem cozinheiro local vivo. |
| `AFFORDABILITY_PROBLEM` | Alimento existente e residentes locais sem caixa para comprá-lo nem ração própria. |
| `LOCAL_ACCESS_PROBLEM` | Capacidade nominal suficiente, mas produção recente insuficiente. |
| `STORAGE_BLOCKAGE` | Trabalho de um produtor local bloqueado por estoque cheio. |
| `TRANSPORT_SHORTAGE` | Relatório regional recente aponta excedente externo, sem transporte implementado. |

Motivos coexistem. `LOCAL_ACCESS_PROBLEM` é um sinal de subutilização, não uma prova
isolada da causa. O relatório administrativo não vira conhecimento automático do
NPC: observações locais e cotações têm validade de 24 horas.

## 6. Alterações no trabalho

Trabalhadores compatíveis podem preparar alimento em tarefa avulsa rural, usando
trigo real, espaço e tempo. Parte do produto paga o trabalhador; o restante fica
na cidade. Distribuição no mercado transfere uma ração ao trabalhador e serve
outra à população abstrata, respeitando o limite diário.

Produção agrícola, extração, caça e cozinha aceitam a quantidade realmente
possível. Pagamento material acompanha a produção. Guarda, comércio e administração
mantêm os serviços remunerados. A alteração não concede ocupação especializada
instantânea a um auxiliar nem transforma estoque cheio em salário fictício.

## 7. Remoção de thresholds fixos

Foi removido `money < 5` da alternativa de trabalho para fome. Uma cotação válida
é comparada ao caixa do NPC; cinco, dez ou doze moedas ainda podem ser insuficientes.
Sem cotação, um NPC com o piso conhecido de compra pode ir verificar o mercado.
Os alvos de reserva da necessidade financeira já existente continuam: a mudança
trata a viabilidade de obter comida, não apaga todo parâmetro econômico.

As primeiras auditorias revelaram duas confusões que foram corrigidas: preço
desconhecido era tratado como falta de dinheiro; estoque vazio também era tratado
como insuficiência de caixa. Ambas podiam manter alguém trabalhando por comida
mesmo com muitas moedas. Agora falta de informação, falta de produto e falta de
renda têm consequências distintas. Foram acrescentados testes de regressão.
As campanhas anteriores às correções estão preservadas em
`reports/fase_3/auditorias_pre_correcao/` e
`reports/fase_3/auditorias_pre_correcao_estoque/`.

## 8. Produção parcial

Uma cozinha com espaço para duas rações produz duas, em vez de recusar um lote
de três. Cada ração consome exatamente dois terços de trigo; o resto é conservado
em `grain_credit`. Salário parcial acumula `wage_credit` em sextos de moeda e
só se converte em caixa por transferência real da cidade.

O teste com estoque 238 → 240 comprova consumo de quatro terços de trigo e
crédito de dois terços de moeda, sem criação monetária. Armas continuam
indivisíveis; uma operação produz uma arma, com seus materiais e pagamento.

## 9. Modelo de capacidade produtiva

Demanda diária de diagnóstico = `ceil(abstratos / 120) + 1,2 × persistentes vivos
presentes`. Capacidade culinária nominal = cozinheiros locais, limitados pelos
postos da taverna, vezes 30 rações/dia. Caçadores acrescentam 20 rações/dia.
Demanda, capacidade e produção realizada são registradas separadamente.

As dez horas nominais de trabalho são uma referência de planejamento, não uma
garantia de utilização. Caminhada, privação, descanso, decisão e insumos afetam
a produção real. Auxiliares e aprendizes entram na realização, não na capacidade
nominal de profissionais formados. Mais detalhes e limites estão no modelo econômico.

## 10. Modelo populacional final

`Town.population` é o total vivo administrativo; `abstract_population` é o
conjunto vivo ainda não individualizado. `resident_ids` permite derivar
persistentes vivos e mortos. Residentes viajando continuam pertencendo ao censo
de origem. O jogador é visitante e fica fora dessa conta.

O consumo abstrato conserva a escala agregada do MVP: um fluxo amostral do mercado
detalhado, não a fisiologia de milhares de pessoas. Não se afirma que uma ração
alimentaria fisicamente 120 pessoas. Não foram implementados natalidade,
envelhecimento ou mortalidade individual abstrata.

## 11. Invariantes populacionais

**Total vivo = abstratos vivos + residentes persistentes vivos.** Materialização
reduz abstratos em um e aumenta persistentes vivos em um, sem mudar o total.
Morte persistente reduz o total uma única vez; o ID permanece como morto.
Treinamento e deslocamento não alteram o censo.

Validação e testes cobrem registro duplicado, morte repetida, abstratos esgotados,
viagem, nova identidade e persistência. As campanhas verificam essas invariantes
nos dez checkpoints de cada modo e novamente nos saves finais.

## 12. Demanda profissional

Cada vaga culinária registra necessidade efetiva, necessidade projetada
descontando aprendizes, início e etapa da resposta. Falta de trigo favorece
colheita limitada; falta de conversão favorece utilização, trabalho temporário,
oferta de formação e, quando elegível, materialização.

Capacidade acompanha demanda e postos locais; o número inicial de NPCs por
localidade ainda pertence à geração do MVP. Não foi feita uma remodelagem de
todas as profissões. Uma vaga pode encerrar por formação ou desaparecimento da
necessidade, diferença importante para interpretar a duração média.

## 13. Mudança/treinamento profissional

Formação de cozinheiro exige candidato comum compatível, oferta conhecida,
cozinha/posto, trigo, espaço e caixa. Diligência, ambição, pressão financeira,
custo, ocupação atual, risco e distância entram na avaliação da alternativa.
O aprendiz produz uma ração/hora, com salário reduzido; requer de 12 a 36 horas
produtivas. A ocupação anterior só muda ao completar o requisito.

Materializados requerem 24 horas produtivas. Tempo sem prática por mais de
168 horas encerra a aprendizagem. Ter um candidato adequado no censo não garante
que ele descubra ou aceite a oferta: a escolha individual permanece autônoma.

| Campanha | Inícios de formação | Residentes anteriores formados | Conclusões totais | Abandonos |
|---|---:|---:|---:|---:|
| jogador | 82 | 8 | 59 | 14 |
| espectador | 112 | 13 | 88 | 19 |
| mundo | 80 | 8 | 57 | 13 |

Conclusões totais incluem aprendizes materializados. Inícios podem incluir uma nova tentativa da mesma pessoa após abandono; não são todos personagens distintos.

## 14. Materializações realizadas

Uma falta precisa persistir por pelo menos 72 horas, sem candidato existente
adequado nem aprendizes suficientes. Abstratos, caixa, trigo, água, cozinha e
postos limitam a materialização, com intervalo mínimo de 72 horas por cidade.
O novo residente é um aprendiz comum, com identidade e personalidade próprias,
origem, relações mínimas, memórias e necessidades persistidas.

As 12 moedas iniciais saem do caixa abstrato. Comida e água iniciais saem do
estoque da cidade. Não se copiam família, memória, inventário ou reputação de
um morto. Materialização não aumenta o total vivo e não garante sobrevivência.

| Campanha | Materializados | Vivos no fim | Mortos no período |
|---|---:|---:|---:|
| jogador | 59 | 8 | 51 |
| espectador | 88 | 9 | 79 |
| mundo | 58 | 6 | 52 |

O número de novos residentes não deve ser confundido com postos estabilizados. Entre 86% e 90% dos materializados morreram durante estas campanhas; mecanismos de reposição existem, mas seu resultado de sobrevivência é fraco.

## 15. Reposição profissional

A sequência prioriza utilização e tarefa temporária, depois residente existente
em formação, e só então materialização elegível. Não há clone de morto nem
formação instantânea. Reposição nesta fase significa recompor a capacidade
culinária; não repõe automaticamente reis, guardas ou qualquer profissional.

| Campanha | Fechamentos de vaga | Média dos fechamentos (horas) | Déficit profissional final | Maior duração ainda aberta |
|---|---:|---:|---:|---:|
| jogador | 60 | 240.40 | 7 | 9808 |
| espectador | 79 | 378.23 | 7 | 9016 |
| mundo | 51 | 552.47 | 7 | 9688 |

A média inclui encerramento por desaparecimento da demanda, não apenas contratação; vagas abertas não entram na média. No jogador, Silvia mantém uma falta de dois cozinheiros por 9.808 horas, na etapa `open_training`. Há candidatos nominais, mas publicar oferta não garantiu formação efetiva.

Como medida observável de reposição após morte local, 58/86/56 identidades
concluíram formação em cidades onde um cozinheiro já havia morrido; eram zero
na Fase 2. Não existe associação de cada novo trabalhador a um morto específico.
Esses números medem formação após perda local, não estabilidade permanente do posto.

## 16. Diagnóstico de água

O registro de morte guarda última refeição, última bebida, última ação bem-sucedida,
objetivo, destino, reservas, fontes conhecidas, distância e condições fisiológicas.
Prevenção de viagem pode consumir reserva, buscar água em poço conhecido ou
obter comida a preço/estoque recentemente observados. Não consulta fontes globais.

| Campanha | Mortes: fome | Mortes: sede | Mortes: ambas | Carregando água |
|---|---:|---:|---:|---:|
| jogador | 216 | 2 | 3 | 113 |
| espectador | 257 | 0 | 1 | 126 |
| mundo | 207 | 1 | 3 | 107 |

Nenhum sobrevivente terminou com sede ≥85. As mortes em condição de sede total foram raras nesta rodada, enquanto a fome concentrou as mortes. Levar água passou a ser comum: 113/126/107 vítimas carregavam água, o que não significa que ela causou suas mortes. Todos os mortos tinham ao menos uma fonte conhecida; 144/167/138 estavam a distância zero de uma delas. O próximo gargalo não pode ser explicado apenas como desconhecimento de poços. Foram registradas 117899/115508/114983 seleções de preparação; elas incluem beber, comer ou buscar reserva.

`hunger`, `thirst` e `both` são categorias exclusivas da condição no instante da
morte. Água carregada não prova morte por sede. O contador `WaterTravelHours`
inclui tempo desde a criação do objetivo até beber, inclusive espera: não permite
uma afirmação precisa sobre horas somente de caminhada. Fontes lembradas também
não garantem estoque disponível na chegada.

## 17. Necessidades pessoais perdidas por prioridade

O motor agora registra a necessidade concorrente quando uma necessidade pessoal
viável perde. Distingue prioridade maior, desempate e continuação de objetivo.
Uma seleção não equivale a ação social concluída: beber ou comer para preparar
uma viagem pode ocorrer sob um objetivo pessoal.

| Motivo por avaliação | Jogador | Espectador | Mundo |
|---|---:|---:|---:|
| Perdeu para prioridade maior | 385006 | 405298 | 438950 |
| Busca familiar perdeu para prioridade maior | 124556 | 125487 | 126691 |

Nos exemplos recentes salvos, comida, descanso, água e renda aparecem como concorrentes. Essa amostra limitada não mede a distribuição histórica inteira de causas; os contadores acima medem todas as avaliações.

Esses números contam avaliações, não necessidades únicas ou histórias diferentes.
Uma busca familiar pode aparecer repetidamente. Diagnósticos recentes ficam
limitados a 256 exemplos no mundo; contadores agregados e episódios ficam salvos.

## 18. Necessidades pessoais sem solução

Ausência de alternativa é registrada separadamente de perder por prioridade.
Informação desconhecida e alvo observado indisponível podem complementar o motivo.
Fechamentos distinguem satisfação, expiração antes de selecionar, expiração depois
de selecionar e morte do dono. Não foram ampliados prazos sociais para reduzir
expirações artificialmente.

| Motivo | Jogador | Espectador | Mundo |
|---|---:|---:|---:|
| Avaliações sem solução viável | 15071 | 13577 | 8854 |
| Busca familiar sem solução viável | 9392 | 11398 | 7281 |
| Episódios expirados antes de seleção | 13088 | 13360 | 13901 |
| Episódios expirados após seleção | 2243 | 2530 | 2278 |
| Episódios encerrados pela morte do dono | 142 | 148 | 165 |

Nas duas últimas linhas, seleção pode ter sido apenas preparação de viagem. Expiração sem seleção não comprova desinteresse: a necessidade pode nunca ter vencido uma pressão material.

Informação útil, alvo alcançável e continuidade de encontro continuam podendo
faltar. A instrumentação permite investigar; não afirma que todo bloqueio foi
resolvido pela Fase 3.

## 19. Testes antigos e novos

**105 testes passaram: 73 anteriores preservados e 32 novos.** Os 26 contratos
obrigatórios têm testes correspondentes em `tests/test_phase3.py`. Os adicionais
cobrem distribuição real, residente viajando, diagnóstico de água e regressões
da confusão entre cotação, estoque e renda. Resultado: `reports/fase_3/testes.txt`.

Fisiologia e descanso foram comparados por árvore sintática com o núcleo anterior;
`rules.py` e `personal.py` permaneceram idênticos. Observar o mesmo mundo por
48 horas manteve estado e RNG idênticos ao controle sem observador.

| Cenário dirigido | Resultado verificado |
|---|---|
| A: trigo cheio, comida ausente, cozinheiro vivo | Sinaliza utilização/acesso; não responde com mais trigo. |
| B: cozinheiro morto | Sinaliza processamento/mão de obra e registra demanda profissional. |
| C: comida existente, residente pobre | Sinaliza poder de compra e permite tarefa útil. |
| D: produtor pobre com estoque cheio | Oferece trabalho avulso por alimento. |
| E: doze moedas diante de ração de quatorze | A renda continua alternativa; estoque cheio pode substituir o emprego bloqueado por tarefa avulsa. |
| F: capacidade abaixo da demanda | Calcula necessidade superior de cozinheiros. |
| G: morte profissional e reação ao longo do tempo | Registro detalhado de 240 horas, sem impor formação ou recuperação. |

No cenário G, o novo aprendiz foi materializado no turno 144 e completou a formação no 205. No turno 240 existia um cozinheiro, sem déficit nominal, mas o mercado continuava sem comida e a produção recente era 15 rações contra demanda de 36,2. A fixture demonstra reposição e também a diferença entre ter capacidade nominal e realmente utilizá-la.

As fixtures A–G constam em `reports/fase_3/cenarios_dirigidos.json`; são testes
dirigidos e não são apresentados como histórias espontâneas das campanhas.

## 20. Auditoria de 10.000 turnos

Foram executadas **três campanhas finais de 10.000 horas cada**, de turno 24 a
10.024: jogador automatizado com comandos públicos em Dovha, espectador sem
jogador em Dovha e observador global sem jogador em Mira. As duas perspectivas
sem jogador usam o mesmo motor; a perspectiva muda a leitura, não as regras.
O jogador usa a política anterior de sobrevivência, movimento, conversa e pedidos.

São dez checkpoints por campanha, contabilidade monetária, censo, estoques,
fisiologia, produção, vagas e comportamento. As perspectivas sem jogador
inspecionam todo o elenco, inclusive novos personagens, e todas as localidades;
amostras econômicas são feitas a cada 250 horas. Não se aceleram decisões de NPCs
distantes para aumentar histórias.

Saves em 1.000, 5.000 e 10.000 horas, registros econômicos, pessoais e diagnóstico
de mortes estão nas pastas dos modos. O motor e RNG continuaram idênticos em
duas cópias carregadas por mais 24 horas. Verificação final:
`reports/fase_3/verificacao_final.json`.

| Campanha | Produção de alimento | Produção de trigo | Tarefas temporárias | Erros / diferença monetária |
|---|---:|---:|---:|---:|
| jogador | 247957 | 135630 | 13082 | 0 / 0 |
| espectador | 239826 | 131044 | 11655 | 0 / 0 |
| mundo | 224612 | 125855 | 12495 | 0 / 0 |

Produção é acumulada no período; não é estoque final. No modo jogador, o auditor sobreviveu às 10.000 horas com saúde 100. Surgiram dez quests: nove de cuidado familiar e uma busca; duas concluídas, três recusadas, três falharam e duas foram resolvidas de outra maneira. Todas envolvem o mesmo casal, um limite de diversidade.

## 21. Comparação quantitativa com Fase 2

| Indicador | Jogador F2 → F3 | Espectador F2 → F3 | Mundo F2 → F3 |
|---|---:|---:|---:|
| NPCs vivos iniciais | 456 → 448 | 456 → 448 | 440 → 432 |
| Localidades | 79 → 76 | 79 → 76 | 76 → 73 |
| NPCs vivos finais | 317 → 286 | 311 → 278 | 302 → 279 |
| Mortes durante a campanha | 139 → 221 | 145 → 258 | 138 → 211 |
| Mortalidade do elenco inicial (%) | 30.48 → 37.95 | 31.80 → 39.96 | 31.36 → 36.81 |
| Seleções fisiológicas (%) | 91.63 → 88.66 | 91.80 → 89.84 | 92.48 → 90.47 |
| Mercados sem comida | 26 → 12 | 31 → 17 | 31 → 17 |
| Sem comida e trigo cheio | 26 → 0 | 31 → 0 | 30 → 1 |
| Dinheiro abaixo de uma ração | 81 → 124 | 78 → 102 | 65 → 112 |
| Dinheiro abaixo de dez moedas | 171 → 219 | 176 → 189 | 152 → 192 |
| Fome ≥70 | 149 → 120 | 120 → 97 | 146 → 102 |
| Sede ≥70 | 59 → 48 | 52 → 55 | 74 → 46 |
| Fome ≥85 | 44 → 29 | 32 → 20 | 32 → 24 |
| Sede ≥85 | 11 → 0 | 8 → 0 | 7 → 0 |
| Mortes carregando comida | 25 → 38 | 25 → 39 | 16 → 31 |
| Mortes carregando água | 0 → 113 | 0 → 126 | 0 → 107 |
| Localidades sem NPC vivo presente | 4 → 0 | 4 → 0 | 1 → 0 |
| Seleções pessoais | 7883 → 6428 | 8063 → 5110 | 7342 → 4842 |
| Episódios pessoais expirados | 18596 → 15473 | 18481 → 16038 | 16694 → 16344 |
| Episódios pessoais satisfeitos | 4674 → 2229 | 4592 → 2235 | 3525 → 2926 |
| Residentes existentes formados | 0 → 8 | 0 → 13 | 0 → 8 |
| Conclusões de formação (todos) | 0 → 59 | 0 → 88 | 0 → 57 |
| Formados após morte de cozinheiro local | 0 → 58 | 0 → 86 | 0 → 56 |
| Habitantes materializados | 0 → 59 | 0 → 88 | 0 → 58 |

A versão participa da seed: geografia, elenco e número de localidades mudam.
Essa comparação é histórica, não isola o efeito da reposição ou de outra regra.
Mortes incluem novos materializados; a mortalidade do elenco inicial os exclui.
Percentuais de decisão não são percentuais de tempo nem ações concluídas.

Pobreza mede caixa versus preço do mercado de origem, inclusive para quem carrega
comida. Fome/sede finais descrevem sobreviventes: menos casos críticos ao fim
podem coexistir com mais mortes antes. Expiração pessoal inclui morte do dono
e precisa ser lida junto de criações, seleções e satisfação.

## 22. Histórias emergentes observadas

1. **Cael Stone, agricultor de Silmir, tornou-se cozinheiro.** No jogador, começou no turno 678 e concluiu no 705, depois da morte de um cozinheiro local no 585. Ficou vivo até o final. O mercado terminou com apenas duas rações: a trajetória profissional é concreta, mas não prova abastecimento estável.
2. **Aldren Valerius abandonou e retomou a formação.** Em Mira, iniciou no 1.138, abandonou no 1.308, voltou no 1.382 e tornou-se cozinheiro no 1.471. A profissão anterior era lenhador. Há continuidade do mesmo personagem, com tentativa, interrupção e conclusão.
3. **Iria Bruma sobreviveu, mas abandonou a aprendizagem.** Materializada em Silvia no 720, parou no 920 após alcançar 21 horas de prática. O mercado ainda estava sem comida no fim. Nova pessoa não equivale a recuperação funcional.
4. **Silas Valerius foi formado e depois morreu de fome.** Entrou como aprendiz em Valria no 576, formou-se no 629 e morreu no 1.013, com sede 64 e uma água carregada. A reposição tem consequências e não produz trabalhador imortal.
5. **Iria Luar procurou ajuda para Arthus Luar repetidamente.** O grafo registra casamento. Entre 6.326 e 9.935 houve pedidos de provisões e busca, com falhas, recusas e resolução alternativa; duas entregas terminaram nos turnos 8.682 e 9.935. Ambos sobreviveram. É um vínculo com continuidade, mas a repetição de provisões mantém o arco preso à sobrevivência.
6. **Luto e descobertas ocorreram de fato.** Tomas Montes ouviu Bela Hammer no turno 209 e identificou restos de Bela Montes no 357. São ações pessoais executadas, com registros próprios, não inferências feitas a partir da porcentagem de seleção.

As sequências completas, com IDs, turnos, linhas dos registros e desfechos,
estão em [HISTORIAS.md](reports/fase_3/HISTORIAS.md). Não foram inventadas causas,
parentescos, recuperação de mercado ou conclusão de objetivos que os registros
não demonstram. Formação e substituição acrescentam continuidade econômica;
guerra e intervenção divina não fazem parte destas histórias.

## 23. Problemas ainda existentes

O abastecimento agregado melhorou em fotografias finais, mas **o acesso individual não acompanhou**: residentes com dinheiro abaixo de uma ração passaram de 81/78/65 para 124/102/112. A mortalidade do elenco original subiu de 30,48%/31,80%/31,36% para 37,95%/39,96%/36,81%. Esses resultados continuam ruins mesmo excluindo as mortes de materializados.

As 38/39/31 mortes carregando comida precisam de investigação temporal: muitas últimas ações bem-sucedidas foram aquisição de alimento, possivelmente tarde demais para comê-lo antes do dano. Isso é hipótese apoiada pela sequência, não uma causa comprovada para todas.

Não se observou expansão quantitativa de histórias pessoais: seleções e satisfações diminuíram. A fração fisiológica caiu um pouco, mas ainda ocupa 88,66%/89,84%/90,47%. Um elenco menor e novos residentes sem vínculos familiares herdados também limitam a comparação. Materializados têm relações mínimas, sem criação completa de novas famílias. Nenhuma localidade ficou sem NPC vivo presente ao fim, mas isso não significa que a população abstrata ou a economia estejam plenamente saudáveis. Os seis reinos terminaram sem governante; continuidade política não foi resolvida nesta fase.

| Sistema ou aspecto | Situação final |
|---|---|
| Diagnóstico local, trabalho avulso, produção parcial, pagamento proporcional | Implementados. |
| Censo, morte única e materialização limitada | Implementados. |
| Formação profissional e reposição | Implementadas para cozinha; demais carreiras adaptativas pendentes. |
| Prevenção de viagem e diagnóstico de mortes | Implementados, com limites de informação e medição. |
| Utilização da capacidade e acesso individual ao alimento | Parcial: diagnóstico/oferta não garantem entrega ou adesão. |
| Capacidade nominal versus jornada real | Aproximação explícita; demanda usa uma escala econômica agregada. |
| Transporte entre localidades | Ausente; excedente regional pode ser apenas diagnosticado. |
| Continuidade familiar, luto, proteção e reconhecimento | Sistemas anteriores preservados; bloqueios e expirações ainda existem. |
| Reposição de governantes, dinastias completas, guerra, deuses | Fora do escopo; permanecem pendentes. |

As rotinas de decisão por categoria e urgência foram preservadas. Preparação
desvia uma ação para obter reserva, mas não garante a conclusão do objetivo
original. Uma vaga pode durar milhares de horas se um candidato é formalmente
adequado e nunca aceita a formação. Esse caso exige melhorar informação e
utilização; materializar automaticamente por contagem seria esconder o problema.

As trajetórias profissionais ganharam começo, interrupção e conclusão, mas a
história pessoal continua fragmentada e repetitiva. O instrumento que compara
respostas diferentes ao mesmo fato capturou zero NPCs no jogador, dois no
espectador e dois no mundo. É uma amostra pequena de diversidade observada,
não uma avaliação completa da personalidade de todos os personagens.

Saves `mvp-3` são recusados pelo motor `mvp-4`; foram preservados e somente
decodificados para leitura no comparativo. Não há migração automática improvisada.

## 24. Recomendações para próxima etapa

1. Investigar mortes com uma reprodução da decisão imediatamente anterior,
   distinguindo falta de renda, alimento, tempo de acesso e ação interrompida.
   Comparar com o mesmo estado inicial em experimento controlado, sem mudar dano.
2. Medir adesão às ofertas: quem conhece a vaga, quem aceita, quanto tempo leva,
   por que abandona e quanto de capacidade se realiza. Candidato nominal não
   significa trabalhador disponível. Resolver essa passagem evita vagas eternas.
3. Avaliar pagamento físico e entrega local onde o salário monetário não compra
   a própria produção a tempo. Qualquer ajuste deve transferir bens reais e ser
   testado contra exploração, consumo duplicado e esvaziamento do mercado.
4. Expandir demanda/formação para outras cadeias apenas após estabilizar cozinha,
   renda e acesso. Transporte mínimo é a etapa para conectar excedente e falta,
   com custo e tempo reais, em vez de teletransportar estoque.
5. Reavaliar histórias usando episódios concluídos, eventos e continuidade dos
   mesmos personagens. Só considerar prazos sociais depois de separar pressão,
   ausência de informação, inviabilidade de encontro e morte do dono.

Para reproduzir: comandos em `README.md`; comparação e histórias são geradas por
`python3 -m experiments.phase3_report`, e integridade por
`python3 -m experiments.phase3_verify`. Relatórios de fases anteriores mantêm
o diagnóstico histórico da versão em que foram escritos.
