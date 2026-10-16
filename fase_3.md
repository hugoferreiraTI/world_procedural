# FASE 3 — ECONOMIA ADAPTATIVA, TRABALHO E RESILIÊNCIA LOCAL

## Objetivo geral

A Fase 2 comprovou que o motor consegue produzir:

- necessidades pessoais;
- relações familiares executáveis;
- busca por familiares;
- luto;
- investigação;
- proteção;
- reconhecimento;
- ascensão financeira;
- quests emergentes;
- histórias independentes do jogador.

Entretanto, as auditorias de 10.000 turnos mostram que aproximadamente 92% das seleções de necessidades dos NPCs continuam sendo fisiológicas.

NÃO interpretar isso automaticamente como um problema de peso da fome.

Os relatórios mostram pressão material real e gargalos econômicos.

Esta fase deverá atacar as CAUSAS materiais que mantêm NPCs em sobrevivência quase permanente.

A meta é transformar o mundo de:

```text
crise
↓
degradação
↓
mais crise
↓
morte
```

em um sistema capaz também de:

```text
crise
↓
diagnóstico
↓
adaptação
↓
recuperação possível
```

Recuperação NÃO deve ser garantida.

Uma cidade ainda poderá colapsar.

A diferença é que ela deverá possuir mecanismos reais para tentar responder.

---

# 1. Documentos obrigatórios antes da implementação

Antes de alterar código, leia integralmente:

- `instruction.md`
- `fase_2.md`
- relatório final da Fase 2;
- relatório das três perspectivas;
- relatório de diagnóstico sobre dominância fisiológica;
- relatório técnico sobre abastecimento/sobrevivência;
- testes existentes;
- código atual de:
  - economia;
  - profissões;
  - necessidades;
  - objetivos;
  - Utility AI;
  - população;
  - geração;
  - engine/tempo;
  - conhecimento;
  - persistência.

Produza antes da implementação um pequeno levantamento contendo:

```text
1. quais sistemas já existem;
2. quais serão reutilizados;
3. quais gargalos são confirmados por código;
4. quais hipóteses ainda precisam ser medidas;
5. quais alterações serão feitas;
6. quais sistemas NÃO serão recriados.
```

Não implementar sistemas paralelos.

---

# 2. Preservar a arquitetura atual

O jogo já possui:

```text
estado do mundo
↓
percepção/conhecimento
↓
necessidade
↓
prioridade
↓
soluções
↓
objetivo
↓
ação
↓
consequência
```

Essa arquitetura deverá continuar sendo o centro da simulação.

NÃO criar:

```text
novo Utility AI
novo NeedSystem
novo GoalSystem
GOAP paralelo
nova economia paralela
novo sistema de profissões isolado
```

A nova lógica econômica deverá alimentar os sistemas existentes.

Exemplo:

```text
cidade detecta baixa capacidade de preparo
↓
necessidade coletiva existente
↓
novas soluções possíveis
↓
Utility avalia
↓
ação escolhida
```

---

# 3. Regra central: não nerfar fome artificialmente

NÃO alterar de início:

```text
crescimento de fome
crescimento de sede
crescimento de cansaço
dano de privação
pesos fisiológicos
```

Não fazer:

```python
hunger_priority *= 0.5
```

Não aumentar comida gratuitamente.

Não adicionar estoques infinitos.

Não alterar percentuais apenas para fazer a auditoria "parecer melhor".

Primeiro deve-se verificar se:

```text
produção
+
renda
+
capacidade
+
acesso
+
trabalho adaptável
```

conseguem reduzir naturalmente a pressão fisiológica.

Somente após uma nova auditoria deverá ser considerado rebalancear fisiologia.

---

# 4. Diagnóstico econômico da localidade

Hoje a cidade tende a interpretar:

```text
falta comida
↓
produzir mais trigo
```

Isso é insuficiente.

Uma necessidade coletiva de alimentação deverá conseguir identificar QUAL PARTE da cadeia está falhando.

Crie uma avaliação reutilizável de gargalo.

Não necessariamente precisa ser um enum exatamente assim, mas conceitualmente precisamos distinguir:

```text
RAW_MATERIAL_SHORTAGE

PROCESSING_CAPACITY_SHORTAGE

LABOR_SHORTAGE

AFFORDABILITY_PROBLEM

LOCAL_ACCESS_PROBLEM

STORAGE_BLOCKAGE

TRANSPORT_SHORTAGE
```

Transporte intermunicipal ainda ficará fora desta fase, mas pode aparecer como diagnóstico sem solução disponível.

## Exemplo 1

```text
food = 0
grain = 10

→ falta matéria-prima
→ agricultura é solução coerente
```

## Exemplo 2

```text
food = 0
grain = 240
cook_count = 0

→ não é falta de trigo
→ falta capacidade profissional
```

## Exemplo 3

```text
food = 0
grain = 240
cook_count = 1
cook_capacity < local_demand

→ existe cozinheiro
→ capacidade insuficiente
```

## Exemplo 4

```text
food = 200
muitos NPCs sem dinheiro

→ disponibilidade não é o problema principal
→ acesso econômico é o gargalo
```

## Exemplo 5

```text
profissional tenta produzir
estoque cheio
produção bloqueada
salário bloqueado

→ STORAGE_BLOCKAGE / WORK_ACCESS
```

A cidade não deverá continuar executando a mesma solução indefinidamente quando os dados mostram que ela não resolve o gargalo.

---

# 5. Capacidade produtiva versus demanda

Deixar de tratar capacidade profissional apenas como:

```text
tem cozinheiro?
sim/não
```

Uma localidade deverá possuir alguma forma de estimar:

```text
demanda prevista
capacidade produtiva
produção realizada
déficit
```

Começar pela cadeia mais importante:

```text
trigo
↓
comida
```

Não implementar uma economia industrial gigantesca nesta fase.

## Exemplo conceitual

```text
FoodDemandPerDay = X
FoodProductionCapacityPerDay = Y

Deficit = X - Y
```

Uma cidade pode possuir cozinheiro e ainda estar subdimensionada.

Exemplo:

```text
população grande
↓
demanda = 30
capacidade culinária = 8

→ déficit estrutural
```

A quantidade de trabalhadores necessários deverá estar ligada a:

```text
população
consumo esperado
estrutura
estoque
demanda
capacidade individual
```

e não somente a uma quantidade fixa inicial.

---

# 6. Não aplicar consumo/população sem definir unidades

Antes de recalibrar consumo ou produção, documentar claramente:

```text
o que significa 1 unidade de food

o que significa 1 unidade de grain

quanto uma unidade abstrata representa

como consumo abstrato e consumo individual convivem

como produção individual e produção abstrata convivem
```

Não aumentar produção/população "até funcionar".

Produção e consumo precisam utilizar um modelo coerente.

---

# 7. Corrigir a alternativa financeira de sobrevivência

Existe uma regra remanescente que considera trabalho como solução de fome apenas abaixo de determinado valor fixo de moedas.

Eliminar essa lógica fixa.

Não usar:

```text
money < 5
```

nem trocar por:

```text
money < 10
money < 20
```

A pergunta correta é:

```text
Com aquilo que esse NPC SABE,
ele consegue obter comida atualmente?
```

Avaliar quando aplicável:

```text
dinheiro atual
preço conhecido
estoque conhecido
distância
mercado conhecido
recursos próprios
possibilidade de coleta
possibilidade de trabalho
```

Exemplo:

```text
NPC possui 12 moedas
comida conhecida custa 14

→ não consegue comprar
→ trabalho continua sendo solução viável
```

Se ele não conhece o preço atual:

NÃO consultar magicamente o estado global.

Use informação observada/conhecida e sua validade.

---

# 8. Trabalho temporário e trabalho avulso

Antes de depender somente de troca formal de profissão, expandir trabalho avulso.

Um NPC cuja profissão atual está bloqueada poderá executar tarefas temporárias úteis.

Exemplo:

```text
agricultor
↓
estoque de trigo cheio
↓
trabalho agrícola não produz valor
↓
cidade possui outra necessidade de mão de obra
↓
NPC considera trabalho temporário
```

Possíveis categorias conceituais:

```text
auxiliar de produção
carregamento
coleta
preparo simples
serviço público
ajuda em estrutura compatível
```

Não permitir que qualquer NPC execute qualquer profissão instantaneamente.

Considerar:

```text
complexidade da tarefa
competência necessária
profissão atual
personalidade
diligência
distância
pagamento
demanda
```

Atividades simples podem exigir pouca preparação.

Atividades especializadas podem exigir treinamento futuro.

---

# 9. Trabalho precisa gerar valor real

Não criar salários mágicos.

Toda remuneração deverá possuir:

```text
pagador real
atividade real
resultado real ou serviço real
```

Dinheiro não deve surgir apenas porque um NPC "tentou trabalhar".

Ao mesmo tempo, evitar situações binárias artificiais.

## Exemplo atual problemático

```text
produção em lote = 3
espaço restante = 2

resultado:
produção = 0
salário = 0
```

Quando tecnicamente possível, permitir:

```text
produção parcial = 2
consumo proporcional de insumos
pagamento proporcional
```

Se determinada profissão não permite produção parcial por alguma razão lógica, documentar.

---

# 10. Estoque cheio não deve condenar trabalhador à pobreza

Um estoque cheio significa:

```text
não precisamos produzir mais desse item agora
```

Não necessariamente:

```text
este trabalhador não possui nenhuma forma de obter renda
```

Quando uma profissão estiver saturada:

```text
WorkNeed
↓
avaliar:
outra atividade da mesma profissão?
trabalho temporário?
venda de excedente?
outra demanda local?
treinamento?
```

Mudança definitiva de profissão virá posteriormente nesta mesma fase.

---

# 11. Definir população antes da materialização

A população abstrata atualmente precisa de uma definição formal.

Antes de criar novos NPCs, definir explicitamente:

```text
TotalPopulation
AbstractPopulation
PersistentAlivePopulation
PersistentDeadPopulation
```

A implementação pode utilizar nomes diferentes.

Mas a semântica precisa ser inequívoca.

Defina invariantes.

Exemplo conceitual:

```text
TotalLivingPopulation =
AbstractPopulation
+
PersistentAlivePopulation
```

Quando um abstrato se materializa:

```text
AbstractPopulation -= 1
PersistentAlivePopulation += 1

TotalLivingPopulation permanece igual
```

Quando um persistente morre:

```text
PersistentAlivePopulation -= 1
TotalLivingPopulation -= 1
```

Adapte se o modelo atual exigir outra estrutura.

O importante é:

- não duplicar população;
- não descontar pessoa duas vezes;
- morto não continuar sendo contado como abstrato vivo;
- residente temporariamente em outro mapa não desaparecer da contagem;
- materialização não criar pessoas do nada.

Criar testes explícitos dessas invariantes.

---

# 12. Demanda profissional

Depois da capacidade produtiva e da população estarem definidas, implementar demanda profissional.

Exemplo:

```text
FoodDemand = 30
CookingCapacity = 8

ProfessionalDemand(Cook) = relevante
```

Não transformar automaticamente:

```text
ProfessionalDemand(Cook)
```

em:

```text
CreateCook()
```

Ela representa uma necessidade do mercado/localidade.

A localidade deverá primeiro verificar soluções disponíveis.

---

# 13. Ordem de resposta à falta profissional

Quando uma função estiver abaixo da capacidade necessária:

## Prioridade 1 — melhorar utilização atual

Verificar:

```text
profissional existente consegue trabalhar?
tem insumo?
tem estrutura?
tem tempo?
está bloqueado por estoque?
recebe pagamento?
está distante?
```

Não contratar trabalhador para um problema de scheduling.

---

## Prioridade 2 — trabalho temporário

Buscar NPCs locais capazes de executar tarefas auxiliares.

---

## Prioridade 3 — mudança/treinamento profissional

Buscar NPC persistente adequado.

Possíveis candidatos:

```text
desempregado
profissão saturada
trabalhador pobre
trabalhador pouco demandado
NPC ambicioso
NPC com necessidade financeira
profissão compatível
```

---

## Prioridade 4 — materialização

Somente quando:

```text
demanda persistente existe
+
não há candidatos adequados
+
população abstrata disponível
+
estrutura existe
+
atividade pode sustentar trabalhador
```

materializar um novo NPC comum.

---

# 14. Mudança de profissão

Profissão não deverá continuar necessariamente imutável.

Crie uma solução relacionada a:

```text
NeedWork
NeedMoney
ambition
ProfessionalDemand
```

Exemplo conceitual:

```text
JobChangeScore =
ExpectedIncome
+ LocalDemand
+ Ambition
+ Diligence
+ FinancialPressure
- TrainingCost
- Risk
- Distance
- CurrentJobValue
```

Não use necessariamente essa fórmula literal.

Integre ao sistema atual de Utility AI.

---

# 15. Treinamento

Uma profissão especializada não deve surgir instantaneamente.

Adicionar conceito simples de treinamento.

Exemplo:

```text
profession_target = cook
training_progress = 0
training_required = X
```

Durante treinamento:

```text
produtividade reduzida
renda possivelmente reduzida
possibilidade de desistência
```

Tempo necessário pode variar conforme:

```text
profissão anterior
similaridade
diligência
complexidade
```

Não criar sistema gigantesco de skills nesta fase.

---

# 16. Materialização profissional

Quando necessário, um habitante abstrato pode se tornar NPC persistente.

Esse NPC deverá ser um indivíduo novo.

Gerar:

```text
EntityID
nome
personalidade
profissão ou treinamento
posição
inventário inicial coerente
relações mínimas quando aplicável
origem/localidade
```

Não copiar:

```text
nome
memórias
família
relações
reputação
```

do trabalhador morto.

A vaga foi substituída.

A pessoa NÃO foi substituída.

---

# 17. Limitar reposição

Reposição NÃO deverá ser infinita.

Considerar:

```text
população abstrata disponível
tempo
demanda
estrutura
capacidade econômica
cooldown
```

Exemplo:

```text
cozinheiro morre

hora 1:
vaga detectada

hora 6:
candidatos avaliados

dias seguintes:
treinamento/materialização

posteriormente:
produção recuperada
```

Não:

```text
cozinheiro morre
1 turno depois:
cozinheiro perfeito aparece
```

---

# 18. Sobrevivência preventiva

Hoje os NPCs frequentemente agem quando a necessidade já está alta.

Adicionar capacidade limitada de preparação.

Antes de:

```text
viagem
busca familiar
investigação
trabalho distante
```

o NPC pode avaliar:

```text
comida disponível
água disponível
distância
tempo estimado
fontes conhecidas
```

E considerar:

```text
comer antes de sair
beber antes de sair
levar comida
obter água
```

Não permitir conhecimento mágico.

O NPC trabalha com:

```text
memória
local conhecido
informação conhecida
```

---

# 19. Água precisa de diagnóstico separado

Adicionar instrumentação específica de sede.

Registrar para cada morte por privação:

```text
health
hunger
thirst
fatigue

food carried
water carried

last meal
last drink

current goal
last successful action
destination

known water source
distance to known water
```

Também medir:

```text
NPCs com sede crítica
NPCs conhecendo poço
NPCs chegando ao poço
tempo gasto para chegar
```

Não implementar solução antes de identificar se o problema é:

```text
falta de água
conhecimento
distância
scheduling
prioridade
frequência de decisão
```

---

# 20. Instrumentação de necessidades pessoais

A Fase 2 mostrou muitas necessidades pessoais criadas e poucas executadas.

Precisamos separar motivos.

Para cada Need que não conseguiu produzir comportamento, registrar quando aplicável:

```text
LostToHigherPriority
NoViableSolution
ExpiredBeforeSelection
OwnerDied
TargetUnavailable
UnknownRequiredInformation
Selected
Satisfied
```

Exemplo:

```text
Need: Mourning
priority = 70

Hunger = 85

result:
LostToHigherPriority(Hunger)
```

versus:

```text
Need: Protection
priority = 85

solutions = 0

result:
NoViableSolution
```

Esses dois casos NÃO devem ser misturados.

---

# 21. NÃO alterar duração social sem evidência

Não aumentar arbitrariamente:

```text
luto
proteção
vingança
status
```

apenas para gerar mais histórias.

Primeiro use a instrumentação para descobrir:

```text
não foi selecionada?

ou

foi selecionada mas não tinha solução?
```

Somente depois ajuste:

```text
priority
decay
expiration
solution availability
```

se os dados justificarem.

---

# 22. Sistemas fora do escopo desta fase

NÃO implementar agora:

```text
guerra
exércitos
combate completo
equipamentos completos
deuses
religião organizada
rituais
diplomacia avançada
caravanas completas
comércio intermunicipal completo
nascimento
envelhecimento
hereditariedade
IA generativa
política complexa
```

A continuidade política continua sendo problema conhecido.

Mas não será usada agora para resolver a dominância fisiológica.

Ela deverá entrar em etapa posterior ou subfase específica.

---

# 23. Transporte entre cidades

Não implementar sistema completo agora.

Entretanto, o diagnóstico econômico deverá conseguir identificar:

```text
LOCAL_SUPPLY_INSUFFICIENT
EXTERNAL_SUPPLY_EXISTS
NO_TRANSPORT_AVAILABLE
```

Isso prepara o sistema para futura expansão.

Não faça teleporte de recurso entre mercados.

---

# 24. Testes obrigatórios

Preservar todos os testes existentes.

Adicionar testes equivalentes a:

```text
test_food_shortage_with_low_grain_prefers_farming

test_food_shortage_with_full_grain_does_not_expand_farming

test_food_shortage_without_cook_creates_professional_demand

test_cook_alive_but_insufficient_capacity_detects_capacity_deficit

test_food_available_but_population_poor_detects_affordability_problem

test_work_for_food_does_not_use_fixed_five_coin_threshold

test_known_unaffordable_food_keeps_work_as_valid_solution

test_unknown_market_price_does_not_use_global_omniscience

test_full_stock_can_allow_alternative_work

test_partial_stock_space_allows_partial_production

test_partial_production_pays_proportionally

test_professional_capacity_scales_with_local_demand

test_materialization_preserves_total_population

test_death_reduces_living_population_once

test_materialization_never_duplicates_population

test_professional_demand_does_not_instantly_spawn_worker

test_existing_candidate_preferred_before_materialization

test_training_requires_time

test_materialized_worker_has_new_identity

test_materialized_worker_does_not_copy_dead_workers_memories

test_replacement_is_limited_by_abstract_population

test_preventive_survival_uses_known_information_only

test_personal_need_records_higher_priority_loss

test_personal_need_records_no_viable_solution

test_determinism_after_phase3_changes

test_save_load_preserves_population_and_professional_state
```

Adapte nomes à convenção do projeto.

---

# 25. Testes dirigidos obrigatórios

Além dos testes unitários, criar cenários reproduzíveis.

## Cenário A

```text
grain = 240
food = 0
cook alive
```

Pergunta:

Por que não existe comida?

Diagnosticar capacidade/execução.

---

## Cenário B

```text
grain = 240
food = 0
cook dead
```

Esperado:

```text
professional demand
```

e não:

```text
expand farming
```

---

## Cenário C

```text
food = 200
NPC money = 1
food price = 2
```

Esperado:

diagnóstico de acesso/renda.

---

## Cenário D

```text
farmer
grain stock full
money = 1
```

O NPC precisa possuir alternativa além de tentar plantar indefinidamente.

---

## Cenário E

```text
NPC money = 12
food price = 14
```

Trabalho continua sendo alternativa válida.

---

## Cenário F

```text
city demand requires 3 cooks
only 1 cook alive
```

Deve existir déficit de capacidade mesmo com profissão presente.

---

## Cenário G

```text
cook dies
abstract population exists
```

O sistema tenta:

```text
current workers
temporary workers
training
materialization
```

conforme regras.

---

# 26. Auditoria longa após implementação

Executar novamente pelo menos:

```text
10.000 turnos
```

Preferencialmente repetir:

```text
jogador
espectador
mundo
```

com metodologia equivalente às campanhas anteriores.

Não altere os dados durante auditoria.

---

# 27. Métricas econômicas obrigatórias

Registrar:

```text
mercados sem comida
mercados sem comida + trigo cheio
mercados sem comida + cozinheiro vivo
mercados sem comida + nenhum cozinheiro

food produced per locality
grain produced per locality

expected demand
production capacity
actual production

professional deficits

professionals dead
professionals retrained
workers materialized

average vacancy duration

NPCs with < cost of one meal

NPCs with hunger >= 70
NPCs with thirst >= 70

deaths by starvation
deaths by thirst
deaths by exhaustion if applicable

deaths carrying food
deaths carrying water
```

---

# 28. Métricas comportamentais

Registrar novamente:

```text
fisiológicas
trabalho/renda
família
luto
proteção
vingança
status
ascensão
```

Mas NÃO definir uma porcentagem desejada.

Comparar naturalmente com o baseline da Fase 2:

```text
~91,6% a ~92,5% fisiológicas
```

---

# 29. Critério de interpretação

Se após:

```text
economia local adaptativa
capacidade produtiva coerente
renda melhor
reposição profissional
água diagnosticada
```

a fisiologia cair significativamente sem alterar seus pesos:

Conclusão provável:

```text
pressão material era a causa principal
```

Se:

```text
mercados saudáveis
renda saudável
água acessível
capacidade adequada
```

mas fisiologia continuar próxima de 92%:

então investigar numa fase posterior:

```text
hunger growth
thirst growth
fatigue growth
meal satiation
decision frequency
goal interruption
preventive maintenance
```

Somente nesse cenário alterar fisiologia.

---

# 30. Histórias emergentes que esta fase pode criar

Não programe estas histórias.

Elas são exemplos do que pode surgir.

## Exemplo

```text
cozinheiro morre
↓
comida começa a faltar
↓
cidade detecta déficit
↓
agricultor está sem trabalho porque trigo está cheio
↓
aceita trabalho temporário
↓
ganha renda
↓
cidade recupera parte da produção
```

## Outro

```text
cidade perde trabalhadores
↓
vaga permanece aberta
↓
NPC ambicioso percebe oportunidade
↓
começa treinamento
↓
muda de profissão
↓
torna-se importante para a cidade
```

## Outro

```text
não existem candidatos
↓
habitante abstrato é materializado
↓
ganha identidade própria
↓
entra na sociedade
↓
cria relações
↓
futuramente gera suas próprias histórias
```

Não roteirize esses resultados.

Eles devem surgir dos mesmos sistemas existentes.

---

# 31. Relatório final obrigatório

Ao concluir a Fase 3, gerar relatório contendo:

```text
1. Estado anterior

2. Gargalos confirmados antes da mudança

3. Sistemas existentes reutilizados

4. Sistemas deliberadamente não recriados

5. Novo diagnóstico econômico

6. Alterações no trabalho

7. Remoção de thresholds fixos

8. Produção parcial

9. Modelo de capacidade produtiva

10. Modelo populacional final

11. Invariantes populacionais

12. Demanda profissional

13. Mudança/treinamento profissional

14. Materializações realizadas

15. Reposição profissional

16. Diagnóstico de água

17. Necessidades pessoais perdidas por prioridade

18. Necessidades pessoais sem solução

19. Testes antigos e novos

20. Auditoria de 10.000 turnos

21. Comparação quantitativa com Fase 2

22. Histórias emergentes observadas

23. Problemas ainda existentes

24. Recomendações para próxima etapa
```

---

# 32. Comparação obrigatória com baseline

Comparar explicitamente:

```text
Fase 2
vs
Fase 3
```

Utilizando pelo menos:

```text
fisiologia selecionada

mercados sem comida

mercados sem comida + trigo cheio

NPCs pobres

NPCs com fome crítica

NPCs com sede crítica

mortes

mortes com comida

mortes com água

localidades funcionalmente vazias

necessidades pessoais selecionadas

necessidades pessoais expiradas

trabalhadores substituídos

trabalhadores treinados

materializações
```

Não atribua causalidade sem evidência.

Exemplo:

```text
"mercados vazios caíram após mudança"
```

é observação.

```text
"caíram exclusivamente devido à reposição"
```

exige comparação controlada.

---

# 33. Filosofia final da fase

Não estamos tentando criar um mundo eternamente equilibrado.

Estamos tentando criar um mundo capaz de reagir.

Uma cidade pode falhar.

Um mercado pode ficar vazio.

Um profissional pode morrer.

Uma fome pode acontecer.

Mas o mundo deve conseguir tentar:

```text
entender o problema
↓
buscar alternativas
↓
redistribuir trabalho
↓
criar oportunidade
↓
treinar pessoas
↓
recuperar capacidade
```

O objetivo não é estabilidade.

O objetivo é **resiliência sistêmica**.

Não esconda a crise.

Faça o mundo responder à crise.

E somente depois avalie se a fisiologia realmente precisa ser rebalanceada.