# Unidades e contratos da Fase 3

Este documento descreve as regras executadas em `mvp-4`. A especificação de entrada
é `fase_3.md`; o levantamento anterior ao código está em `LEVANTAMENTO.md`.

## Tempo, bens e moeda

Um turno é uma hora; um dia contém 24 turnos. Os inventários guardam quantidades
inteiras. `food` representa uma ração: consumi-la reduz fome em 40, como na Fase 2.
`water` reduz sede em 45. A fisiologia, o dano por privação e a cura por descanso
permanecem iguais. Não há consumo individual aplicado a cada habitante abstrato.

Preparar uma ração custa exatamente dois terços de uma unidade de trigo. O campo
`grain_credit` conserva de zero a dois terços já retirados do inventário: material
disponível para preparo = `3 × trigo inteiro + grain_credit`, em terços.
Cada ração retira dois desses terços. Isso permite produção parcial sem arredondar
repetidamente insumos para cima nem criar alimento sem consumir matéria-prima.
O saldo fracionário é material de processamento, não um item negociável.

Moedas são inteiras. `wage_credit` guarda salário conquistado, ainda não pago, em sextos
de moeda. Produção completa recebe uma moeda por hora equivalente; produção
parcial acumula a fração correspondente. O pagamento transfere somente moedas
existentes da cidade. Crédito salarial não é dinheiro disponível para compras.
Guarda, comércio e administração continuam prestando serviços remunerados.
A renda abstrata diária é a fonte explícita de moeda já existente, registrada em
`MoneySourceAbstractWork`; não é salário novo criado por trabalho avulso.

## População

`Town.population` é o total de habitantes vivos, não o número de personagens no mapa.
`abstract_population` conta habitantes vivos não individualizados. Residentes
persistentes vivos são os IDs vivos de `resident_ids`, inclusive quando viajam.
Os mortos persistentes permanecem registrados, sem compor o total vivo.
O jogador é visitante e não integra esse censo.

Invariante: **total vivo = abstratos vivos + residentes persistentes vivos**.
Materializar move exatamente uma pessoa do conjunto abstrato para o persistente;
não muda o total vivo. Uma morte persistente diminui o total uma única vez,
registrada em `counted_deaths`. Viajar não reduz a população da cidade de origem.
Não há nascimento, envelhecimento ou mortalidade individual de abstratos.

## Demanda e capacidade

A demanda abstrata diária é `ceil(abstratos / 120)` rações, ou zero sem abstratos.
Ela preserva a agregação econômica do MVP; não equivale ao consumo fisiológico
de todos os habitantes. Refeições realmente distribuídas durante o dia são
deduzidas dessa compra, evitando cobrar o mesmo consumo duas vezes.

Para diagnóstico, somam-se 1,2 rações por residente persistente vivo presente no
mapa local. A estimativa de capacidade de um cozinheiro é 30 rações/dia, usando
três por hora e dez horas nominais; a de um caçador é 20. Uma cozinha existente
e seus postos limitam a capacidade culinária. Os postos iniciais acompanham a
escala populacional; não fornecem insumos, salários ou produção gratuita.

Capacidade nominal, demanda esperada e produção realizada são campos separados.
As dez horas são uma referência de planejamento, não uma garantia de execução:
viagens, descanso, privação, informação e remuneração reduzem a utilização.
Produção avulsa e de aprendizes entra na produção realizada, mas não na capacidade
nominal de profissionais formados. Trabalho emergencial pode ocorrer fora do
horário da rotina. Essa aproximação precisa ser lida junto dos dados reais.

## Diagnóstico e informação

`Economy.food_diagnosis` é um relatório administrativo local. Identifica falta de
matéria-prima, capacidade de processamento, mão de obra, poder de compra, acesso
local, bloqueio por estoque e transporte. Mais de um motivo pode coexistir.
`LOCAL_ACCESS_PROBLEM` é um sinal de baixa realização apesar da capacidade nominal;
não prova sozinho se a causa foi trajeto, decisão, insumo ou renda.

Os NPCs observam estoques/quadro de ofertas ao chegar a mercado, trabalho ou
coleta conhecidos. Só no mercado observam a cotação corrente. A informação tem
validade de 24 horas. O diagnóstico administrativo não concede automaticamente
conhecimento a cada personagem. Relatórios regionais podem indicar excedentes,
mas não transportam bens nem geram rotas conhecidas para NPCs.

Sem cotação válida, o NPC com duas moedas pode verificar o mercado: duas é o piso
conhecido da regra de preços, não o antigo corte arbitrário de cinco moedas.
Uma cotação válida acima do caixa permite buscar renda mesmo com cinco, dez ou
doze moedas. Cotação expirada não prova pobreza; estoque vazio também não prova
insuficiência de caixa. Essas distinções corrigiram ciclos de trabalho encontrados
nas primeiras auditorias desta fase.

## Trabalho e formação

Trabalho avulso rural prepara até três rações por hora com trigo e espaço reais.
Uma ração por hora equivalente paga o trabalhador e o restante fica na cidade.
Se só for possível produzir uma fração do lote, o salário proporcional é em moeda.
Distribuição no mercado transfere uma ração como pagamento e consome outra como
refeição efetivamente servida. O limite diário acompanha a demanda abstrata.
Estoque cheio deixa de ser tratado como produção remunerada fictícia e pode
abrir uma alternativa útil para trabalhadores compatíveis.

A cadeia adaptativa implementada é trigo → alimento; a formação é para cozinheiro.
Um residente comum compatível pode escolher aprender após conhecer a oferta.
A prática produz uma ração/hora e recebe um terço da remuneração plena. Insumos,
espaço, posto e caixa são necessários. A formação exige de 12 a 36 horas produtivas,
conforme diligência e experiência agrícola. O relógio da campanha sozinho não
forma ninguém; falta de prática por mais de 168 horas encerra a aprendizagem.
A profissão anterior só é trocada ao completar o requisito.

## Reposição limitada

A vaga registra início, necessidade efetiva e necessidade projetada descontando
aprendizes. A cidade primeiro publica utilização/trabalho temporário; uma falta
persistente pode abrir formação após 48 horas. Materialização só é elegível após
72 horas de falta e ausência de candidato persistente adequado, com abstratos,
cozinha, postos, trigo, água e caixa. Há intervalo mínimo de 72 horas por cidade.

O materializado é uma nova identidade comum e um aprendiz, não um cozinheiro
instantâneo. Recebe 12 moedas transferidas do caixa abstrato e até duas rações
e duas águas transferidas do estoque real. Sua prática exige 24 horas produtivas.
Origem, residência, lealdade, personalidade, memória e necessidade própria são
persistidas. Não herda família, bens, reputação ou memória de quem morreu.
A reposição não é infinita: diminui o conjunto abstrato, usa reservas e demora.

Uma vaga pode continuar aberta se há candidato formalmente adequado que nunca
conhece ou aceita a oferta. Isso é um limite atual da utilização/informação, não
justificativa para materialização automática. Não há reposição de reis nem
cadeias adaptativas completas para todas as profissões.

## Prevenção e métricas

Antes de uma viagem conhecida de pelo menos três passos, a decisão considera
fome/sede previstas para o trajeto mais seis horas. Pode consumir reserva, levar
água de um poço conhecido ou obter comida a preço/estoque recentemente observados.
A chegada ainda pode falhar. Não há busca onisciente por uma fonte qualquer.

`PersonalOutcome` conta avaliações e fechamentos, não histórias distintas: uma
mesma necessidade pode perder várias vezes. Episódios de criação, satisfação e
expiração continuam nos contadores `NPCNeed`. Preparação pode acontecer sob uma
necessidade pessoal selecionada: selecionar luto e beber água não é concluir luto.
`WaterTravelHours` mede o tempo desde a criação do objetivo até beber, incluindo
espera; não mede exclusivamente caminhada. Fechamento de vaga inclui fim da demanda,
e sua média não inclui vagas ainda abertas. Mortes `hunger`, `thirst` e `both`
descrevem as condições no instante da morte; não são uma autópsia causal completa.

Transporte entre cidades, guerra, deuses, religião organizada, política nova,
nascimento e dinastias completas continuam fora desta fase.
