# FASE 6.0 — APROFUNDAMENTO SISTÊMICO, COERÊNCIA E BALANCEAMENTO CAUSAL

Base:

```text
mvp-13-fase5.5.5
save format 2
generation mvp-5.4
```

Versão alvo sugerida:

```text
mvp-14-fase6.0
```

Alterar `GENERATION_VERSION` somente se regras de geração realmente mudarem.

Alterar formato de save somente se houver incompatibilidade estrutural real.

---

# 1. OBJETIVO DA FASE

A Fase 6.0 NÃO é principalmente uma fase de adicionar novos subsistemas.

É uma fase de aprofundar os sistemas existentes para que o mundo seja:

```text
mais coerente
mais sustentável
mais responsivo
mais institucionalmente contínuo
mais socialmente explicável
mais economicamente causal
mais capaz de completar os ciclos já modelados
```

sem transformar:

```text
emergência → bônus mágico
instituição → telepatia
economia → recurso grátis
justiça → radar global
religião → intervenção automática
facção → spawn por threshold
NPC → agente onisciente
```

A pergunta deixa de ser:

> “o sistema existe?”

e passa a ser:

> “o sistema consegue naturalmente cumprir sua função quando as condições existem?”

---

# 2. FILOSOFIA DA FASE 6

Preservar:

```text
STATE
↓
PERCEPTION / KNOWLEDGE
↓
NEED
↓
PRIORITY
↓
AVAILABLE SOLUTIONS
↓
GATES
↓
UTILITY
↓
GOAL
↓
ACTION
↓
EVENT
↓
KNOWLEDGE / CONSEQUENCE
↓
NEW STATE
```

Não resolver incoerência removendo causalidade.

Não tornar NPCs oniscientes.

Não fazer instituições agirem sem pessoas.

Não criar recursos para corrigir escassez.

Não abaixar thresholds de eventos raros apenas para fazê-los aparecer.

Não buscar taxas “bonitas”.

---

# 3. QUESTÃO CENTRAL DO MOTOR DE DECISÃO

O motor atual NÃO compara globalmente todas as ações possíveis.

Ele:

```text
ordena Needs
↓
procura a primeira Need com solução viável
↓
compara Utility apenas dentro daquela Need
```

Isso é arquitetura intencional e deve ser PRESERVADO inicialmente.

Não substituir por:

```text
GLOBAL ACTION UTILITY
```

sem evidência extremamente forte.

O objetivo da Fase 6 é descobrir:

```text
quando essa arquitetura produz comportamento coerente
```

e:

```text
quando uma Need repetidamente solucionável monopoliza
a capacidade de agir e impede o restante da vida.
```

---

# 4. MEDIR “NEED STARVATION”

Adicionar métricas causais para cada tipo de Need:

```text
active_hours
top_rank_hours
solvable_hours
selected_count
executed_count
successful_count

blocked_by_higher_need_count
time_until_first_selection
time_until_resolution
reactivation_count
expiration_count
```

Especialmente:

```text
food
water
food_reserve
rest
recovery
money
work
family
security
political_pressure
organizational_survival
religious_interest
divine_contact
advancement
migration
```

Queremos distinguir:

```text
Need não aconteceu
```

de:

```text
Need aconteceu mas nunca teve solução
```

de:

```text
Need tinha solução mas outra Need venceu por 150 horas.
```

---

# 5. NÃO REDUZIR PRIORIDADE DE SOBREVIVÊNCIA POR DECRETO

Se alguém está com:

```text
thirst = 100
HP = 12
```

sede DEVE atropelar:

```text
carreira
política
religião
socialização
```

O objetivo NÃO é fazer o NPC ir à reunião enquanto morre.

O objetivo é descobrir:

> por que tantos NPCs chegam continuamente nesse estado?

Portanto atacar:

```text
causa da emergência
```

antes de:

```text
prioridade da emergência
```

---

# PARTE A — SOBREVIVÊNCIA E ECONOMIA

# 6. RADIOGRAFIA DE SUSTENTABILIDADE POR LOCALIDADE

Para cada Town:

calcular a cada janela diária:

```text
persistent_population
abstract_population

food_stock
water_stock

grain_stock

food_production_capacity
water_production_capacity

food_realized
water_realized

abstract_food_consumption
persistent_food_consumption

abstract_water_consumption
persistent_water_consumption

market_price
median_personal_money

food_affordability
water_accessibility

reserve_days_food
reserve_days_water
```

Separar:

```text
capitais
cidades
vilas
```

---

# 7. POTENCIAL ≠ PRODUÇÃO REAL

Distinguir:

```text
potential_capacity
```

de:

```text
realized_production
```

Exemplo:

uma cidade pode possuir capacidade para produzir 200 água/dia, mas produzir apenas 80 porque:

```text
faltou trabalhador
faltou infraestrutura
faltou tempo
faltou material
faltou acesso
```

Não confundir capacidade nominal com output.

---

# 8. FUNIL DA SOBREVIVÊNCIA

Para cada morte por privação, tentar classificar causalmente:

```text
WORLD SHORTAGE
LOCAL SHORTAGE
ACCESS FAILURE
KNOWLEDGE FAILURE
AFFORDABILITY
NO MONEY
NO WORK
TRAVEL TIME
PRIORITY COMPETITION
FAILED ACQUISITION
ACQUIRED_TOO_LATE
FAILED_CONSUMPTION
LOD OPPORTUNITY
OTHER / UNKNOWN
```

Uma morte pode possuir múltiplos fatores.

Não inventar causa quando não houver evidência.

---

# 9. RECURSO EXISTENTE NÃO SIGNIFICA RECURSO ACESSÍVEL

Preservar distinção:

```text
Town has food
≠
NPC knows
≠
NPC can reach
≠
NPC can afford
≠
NPC can acquire
≠
NPC has time to consume
```

Essa cadeia deve permanecer causal.

---

# 10. CAPITAIS

Auditar especificamente a sustentabilidade das capitais.

Verificar se infraestrutura inicial está sendo dimensionada de forma incoerente com população.

Pergunta:

> uma capital começa estruturalmente condenada mesmo quando sua economia funciona normalmente?

Se SIM:

corrigir o modelo de capacidade.

Não simplesmente:

```text
capital_water *= 10
```

Criar capacidade coerente com:

```text
população
tipo de localidade
infraestrutura
trabalhadores
recursos
```

---

# 11. ESCASSEZ CONTINUA SENDO POSSÍVEL

Depois da correção:

```text
seca
falta de trabalhador
colapso econômico
rota interrompida
crise política
violência
```

ainda podem gerar fome.

O mundo não deve ser automaticamente sustentável.

A diferença é:

```text
crise causal
```

versus:

```text
parâmetro inicial matematicamente inviável.
```

---

# 12. AQUISIÇÃO CRÍTICA E CONSUMO

Auditar casos:

```text
NPC obtém food/water
↓
ainda está em condição fatal
↓
hora fecha
↓
morre antes de consumir
```

Não unir aquisição e consumo genericamente.

Mas avaliar se, em emergência extrema, faz sentido existir uma continuação semântica:

```text
AcquireCriticalResource
→ ImmediateConsume
```

somente quando:

```text
recurso acabou de ser adquirido
necessidade é emergencial
NPC está fisicamente capaz
consumo não exige outra atividade incompatível
```

Não adicionar se os dados não justificarem.

---

# PARTE B — LOD E OPORTUNIDADE DE VIDA

# 13. AUDITAR LOD

Comparar:

```text
ACTIVE
LOCAL
BACKGROUND
```

ou estados reais equivalentes.

Para cada nível:

```text
decision_interval
Needs criadas
Needs resolvidas
tempo médio sem decisão
episódios críticos
mortes
trabalho
relações
instituições
crime
religião
viagens
```

---

# 14. FISIOLOGIA VS INTERVALO DE DECISÃO

Fisiologia acontece em escala diferente das decisões em LOD.

Medir especificamente:

```text
quanto hunger/thirst/fatigue aumenta
entre duas oportunidades reais de decisão
```

por LOD.

Pergunta:

> NPC em background possui menos chance estrutural de salvar a própria vida?

Se SIM:

corrigir a discrepância sem transformar LOD em simulação completa.

---

# 15. LOD NÃO DEVE ALTERAR A PERSONALIDADE DO MUNDO

LOD pode alterar:

```text
resolução
frequência de atualização
nível de detalhe
```

mas não deveria produzir sistematicamente:

```text
mais mortes
menos carreira
menos justiça
menos instituições
```

apenas porque o NPC não está perto de uma entidade relevante.

---

# 16. PROMOÇÃO POR PRESSÃO

Avaliar se pressões relevantes devem promover temporariamente LOD:

```text
emergência fisiológica
perseguição
investigação ativa
decisão letal
responsabilidade institucional urgente
Journey crítica
```

Somente se necessário.

Não promover todo NPC por qualquer Need.

---

# PARTE C — EMPREGO, PRODUÇÃO E CARREIRA

# 17. PRESERVAR ECONOMIA MATERIAL

Manter:

```text
worker
→ input
→ work
→ output
→ owner
→ payment
```

Não introduzir renda abstrata para personagens persistentes apenas para reduzir pobreza.

---

# 18. FUNIL DE EMPREGO

Medir:

```text
Need money/work
↓
market observed
↓
opportunity known
↓
candidate generated
↓
Utility
↓
travel
↓
work attempt
↓
production
↓
payment
```

Separar falhas:

```text
NO_PAYER
NO_INPUT
SATURATED
INCOMPATIBLE
NO_KNOWN_JOB
NOT_ARRIVED
PRIORITY_LOST
```

---

# 19. CARREIRA ATUALMENTE É PARCIAL

Aprofundar:

```text
ProfessionalDemand
training
apprenticeship
profession change
worker materialization
```

Não criar uma árvore RPG de profissões.

Carreira deve responder a:

```text
demanda real
oportunidade conhecida
instrutor/capacidade
tempo
personalidade
pressão econômica
aspiração
```

---

# 20. GENERALIZAR TREINAMENTO COM CAUTELA

Hoje o treinamento é muito concentrado em poucos caminhos.

Criar uma interface comum de treinamento para profissões que semanticamente admitem aprendizagem.

Exemplo conceitual:

```text
TrainingOpportunity
profession
teacher/institution
required_progress
cost
input
location
```

Não necessariamente todas as profissões usam exatamente o mesmo método.

---

# 21. NÃO MATERIALIZAR TRABALHADOR SEM CAUSA

`ProfessionalDemand` deve continuar exigindo déficit persistente.

Antes de materializar um abstrato:

procurar:

```text
desempregado persistente
candidato treinável
profissional compatível
migração possível
```

Materialização é último mecanismo de continuidade demográfica atual.

Não é spawn de funcionário.

---

# PARTE D — GRUPOS E COESÃO SOCIAL

# 22. SOCIAL AFFINITY ≠ ORGANIZATIONAL COMPATIBILITY

Criar explicitamente:

```text
OrganizationalCompatibility
```

separado de:

```text
SocialAffinity
```

---

# 23. SOCIAL AFFINITY

Continua representando algo como:

```text
trust
friendship
personal relation
reputation
```

Importante para:

```text
liderança
cooperação
confiança
risco social
```

Mas não deve responder sozinha:

> esta organização serve ao meu problema?

---

# 24. ORGANIZATIONAL COMPATIBILITY

Deve considerar causalmente:

```text
shared cause
objective alignment
known strategy
locality
known effectiveness
reputation
legal risk
dues/cost
autonomy cost
capacity
existing membership
social affinity
hostility
```

Social affinity é UM componente.

Não é o gate inteiro.

---

# 25. JOIN ANTES DE CREATE

Continuar filosofia:

```text
problema coletivo
↓
procura organizações conhecidas/acessíveis
↓
avalia compatibilidade
↓
JOIN quando existe opção aceitável
↓
CREATE somente quando não existe opção suficientemente compatível
```

---

# 26. MÚLTIPLOS GRUPOS CONTINUAM POSSÍVEIS

Não deduplicar grupos globalmente.

Dois grupos de segurança podem coexistir porque:

```text
estratégia diferente
liderança rival
ideologia
hostilidade
geografia
corrupção percebida
capacidade cheia
falta de confiança
objetivo secundário incompatível
```

O importante é conseguir responder:

> por que o segundo grupo precisou existir?

---

# 27. MEDIR FRAGMENTAÇÃO

Para cada criação de grupo quando já existe grupo semelhante:

registrar:

```text
known_existing_groups
compatibility
rejection reason
distance
capacity
relationship
strategy conflict
knowledge gap
```

---

# PARTE E — CONTINUIDADE INSTITUCIONAL

# 28. INSTITUIÇÃO NÃO É UMA PESSOA

Preservar:

```text
pessoas executam ações
```

mas criar:

```text
InstitutionalTask / Obligation
```

ou estrutura equivalente.

A instituição possui a obrigação.

Uma pessoa autorizada executa.

---

# 29. TASK QUEUE INSTITUCIONAL

Exemplos:

```text
deliver_proposal
return_response
hold_meeting
work_policy
respond_case
purchase_resource
perform_assignment
recruit
report
```

Task deve possuir:

```text
issuer
institution
kind
target
location
created
priority
requirements
authorized_roles
status
attempts
block_reason
```

---

# 30. DELEGAÇÃO

Criar papéis/autorização suficientes para evitar single point of failure.

Exemplos:

```text
leader
deputy
representative
authorized_member
mayor
municipal_representative
```

Não criar burocracia gigantesca.

---

# 31. TAREFA SOBREVIVE AO TITULAR

Se o líder:

```text
dorme
viaja
está ferido
morre
fica sem provisões
```

a obrigação institucional não precisa desaparecer.

Outro agente autorizado pode assumir.

Isso NÃO significa execução automática.

Ainda exige:

```text
conhecimento
presença
rota
tempo
recursos
capacidade
```

---

# 32. PREFEITURA

Criar continuidade administrativa mínima.

O prefeito continua responsável por decisões de maior autoridade.

Mas tarefas como:

```text
receber documento
publicar resposta
transmitir informação
administrar trabalho já aprovado
```

podem ser delegáveis quando semanticamente adequado.

---

# 33. POLICY WORK

Permitir rotação de trabalhador quando apropriado.

A Policy pertence à cidade.

Não ao primeiro trabalhador que começou.

---

# PARTE F — GRUPO → FACÇÃO

# 34. NÃO REDUZIR FORMALIZATION SCORE AINDA

A formalização agora possui regra única e confiável.

Primeiro medir o novo funil:

```text
eligible groups
↓
age
↓
membership
↓
meetings/presence
↓
investment
↓
contributions
↓
formalization score
↓
funds
↓
formalization
```

---

# 35. CONTAR O GATE QUE MATOU CADA CANDIDATURA

Para cada grupo potencial:

```text
TOO_YOUNG
TOO_FEW_MEMBERS
NO_PRESENT_MEMBERS
LOW_INVESTMENT
NO_CONTRIBUTIONS
LOW_SCORE
INSUFFICIENT_FUNDS
NO_LEADER
WORLD_LIMIT
```

ou códigos equivalentes.

---

# 36. REVISAR REQUISITOS SOMENTE DEPOIS

Se os dados mostrarem que um gate específico impede praticamente todos os grupos independentemente de comportamento:

avaliar sua coerência.

Pergunta:

> esse gate representa realmente institucionalização?

Exemplo:

quatro reuniões podem ser proxy para:

```text
continuidade
```

mas talvez a continuidade real seja melhor medida por:

```text
ações coletivas
investimento
tempo
propostas
recursos compartilhados
participação recorrente
```

Não mudar sem evidência.

---

# PARTE G — CRIME → JUSTIÇA

# 37. FUNIL COMPLETO

Instrumentar e medir:

```text
Crime
↓
Witness
↓
Fact
↓
Authority learns
↓
Wanted / case
↓
Investigation
↓
Lead
↓
Pursuit
↓
Contact
↓
Confrontation
↓
Capture / detention / resolution
```

---

# 38. ZERO CAPTURA PRECISA TER EXPLICAÇÃO

Não exigir taxa arbitrária de captura.

Mas se:

```text
wanted existe
guarda sabe
suspeito é conhecido
ambos estão acessíveis
guarda possui autoridade
```

e ainda assim não existe caminho operacional até captura:

há gargalo.

---

# 39. CASO PODE SER RESPONSABILIDADE INSTITUCIONAL

Avaliar integrar justiça ao modelo de continuidade.

Um caso não deve desaparecer porque:

```text
o único guarda que sabia dele dormiu
```

O conhecimento NÃO pode virar universal.

Mas autoridade pode possuir registros institucionais conhecidos por agentes autorizados.

---

# 40. SEM POLÍCIA TELEPÁTICA

Registrar caso na instituição requer transmissão física/informacional legítima.

Depois disso, agentes autorizados podem aprender através do canal institucional.

---

# 41. CRIME E SOBREVIVÊNCIA ESTÃO LIGADOS

Não balancear furto antes de estabilizar sobrevivência.

Parte dos crimes pode ser consequência causal de:

```text
fome
pobreza
falta de acesso
```

A melhora econômica pode alterar criminalidade naturalmente.

Medir antes/depois.

---

# PARTE H — VIOLÊNCIA E LETALIDADE

# 42. NÃO REESCREVER O SISTEMA LETAL

A arquitetura:

```text
motive
→ LethalDecision
→ pursuit/access
→ attack
→ incapacitation
→ terminal
→ finish/spare/capture/help/withdraw
```

deve permanecer.

---

# 43. MEDIR COERÊNCIA DA VIOLÊNCIA

Classificar ataques por:

```text
self defense
protective
retributive
law enforcement
property conflict
theft response
instrumental
hedonic
other
```

E medir:

```text
attack
→ injury
→ incapacitation
→ terminal
→ death
```

---

# 44. FREQUÊNCIA NÃO POSSUI META ARBITRÁRIA

388 ataques e 4 mortes podem ser coerentes ou não.

A pergunta é:

> os ataques possuem causas plausíveis e consequências proporcionais?

Não:

> quero 20 mortes.

---

# 45. PÓS-CONFLITO

Verificar se conflitos conseguem realmente terminar por:

```text
withdraw
flee
surrender
capture
repair
apology
return_stolen
forgive
truce
```

Se `attack` domina porque outros encerramentos não conseguem competir/executar, aprofundar esses ciclos.

---

# PARTE I — RELIGIÃO

# 46. FUNIL RELIGIOSO

Medir:

```text
belief
↓
religious_interest
↓
prayer / ritual
↓
seek_divine_contact
↓
sacred site known
↓
route known
↓
journey
↓
rite
↓
DivineAccess
↓
god receives/knows
↓
audience/intervention
↓
contract
```

---

# 47. RARIDADE ≠ SISTEMA INACESSÍVEL

Zero audiência em 300h pode ser perfeitamente válido.

Mas distinguir:

```text
ninguém chegou aos gates
```

de:

```text
milhares chegaram e um único threshold sempre bloqueou todos.
```

---

# 48. AUDITAR DEUSES PELO QUE ELES SABEM

Não usar:

```text
WorldState truth
```

como conhecimento divino.

Medir:

```text
messages received
facts known
regional presence
affinity
energy
cooldown
domain relevance
```

---

# 49. INTERVENÇÃO DEVE CONTINUAR RARA

Não transformar deus em sistema de suporte aos NPCs.

Intervenção deve continuar depender de:

```text
acesso
conhecimento
afinidade
motivo
energia
valores
```

---

# PARTE J — OBSERVABILIDADE V1.1 DURANTE A FASE

# 50. USAR O SISTEMA NATIVO

A auditoria da Fase 6 deve usar:

```text
DecisionTrace
ActionAttempt
LearningReceipt
parent_event_ids
Need episodes
EventIndex
```

Não voltar a depender prioritariamente de `sys.setprofile`.

---

# 51. APROFUNDAR GATES NOS SISTEMAS ALTERADOS

Quando V1 retornar:

```text
NO_GENERATED_ACTION
```

em um funil central alterado nesta fase:

tentar substituir por razão específica.

Não instrumentar o projeto inteiro novamente.

Somente os sistemas tocados pela 6.0.

---

# 52. LINKS CAUSAIS SEM PAYLOAD

Não transformar Observability V1.1 num projeto paralelo grande.

Mas avaliar um:

```text
HistoricalEventTombstone
```

mínimo para pais causais persistentes cujo payload completo seria descartado.

Algo como:

```text
event_id
kind
turn
actor
target
location
parent_ids
```

Somente se puder ser implementado sem explodir escopo.

Caso contrário registrar para fase posterior.

---

# PARTE K — METODOLOGIA DE BALANCEAMENTO

# 53. NÃO ALTERAR DEZ VARIÁVEIS AO MESMO TEMPO

Para cada problema:

```text
hipótese
↓
métrica
↓
controle
↓
alteração mínima
↓
mesma seed controlada
↓
comparação
```

Só depois integrar.

---

# 54. BALANCEAMENTO CAUSAL

Exemplo ruim:

```text
muita fome
→ hunger_per_hour 2 → 1
```

Exemplo melhor:

```text
muita fome
↓
capitais não conseguem produzir o consumo teórico
↓
infraestrutura inicial incompatível com população
↓
corrigir relação população↔capacidade
```

---

# 55. NÃO BALANCEAR PARA UMA SEED

Usar:

```text
fixtures controladas
seeds fixas para A/B
campanha natural final com seed nova
```

Não seed-shopping.

---

# 56. ORDEM DAS INTERVENÇÕES

Seguir preferencialmente:

```text
1. sobrevivência / sustentabilidade
2. LOD
3. emprego / carreira
4. grupos / compatibilidade
5. continuidade institucional
6. formalização
7. crime / justiça
8. violência
9. religião
```

Essa ordem importa porque os sistemas são causais.

Exemplo:

```text
sobrevivência
↓
crime
↓
justiça
```

Não calibrar crime antes da sobrevivência.

---

# 57. TESTES

Manter os 341 testes verdes.

Toda nova regra relevante precisa de teste causal pequeno.

Não remover teste da 5.5.5 para facilitar balanceamento.

---

# 58. REGRESSÕES 5.5.5

Garantir durante toda a fase:

```text
B01 não volta
B02 não volta
B03 não volta
B04 não volta
B05 não volta
B06 não volta
B07 não volta
B08 não volta
```

---

# 59. NEUTRALIDADE DA OBSERVABILIDADE

Se Observability for expandida:

repetir OFF/NORMAL/AUDIT.

Gameplay/RNG devem continuar equivalentes.

---

# 60. CONTROLLED RUNS

Criar cenários pequenos específicos para:

```text
capital sustentável
capital estruturalmente insuficiente

NPC em ACTIVE vs BACKGROUND

worker sem emprego
worker com vaga
training opportunity

dois grupos compatíveis
dois grupos incompatíveis

líder ausente com delegado disponível

grupo quase formalizável

crime conhecido pela guarda

crime sem conhecimento da guarda

deus com acesso insuficiente
deus com todos os gates válidos
```

Não transformar esses controles em história natural.

---

# 61. CAMPANHA NATURAL FINAL

Após integração:

```text
300 horas
4 reinos
sem jogador
historical_turns = 0
seed nova
sem seed-shopping
```

Preservar comparabilidade com:

```text
Vaelora-55
Neravon-Coesao55
Thalven-Radiografia55
Elyndar-Estabilidade555
```

---

# 62. MÉTRICAS OBRIGATÓRIAS DA CAMPANHA

### Sobrevivência

```text
mortes por causa
survival decision share
critical episodes
resource-at-death
avoidability classification
produção/consumo por Town
reserve days
```

### LOD

```text
decisions por nível
critical episodes por nível
mortes por nível
Need latency por nível
```

### Trabalho

```text
work attempts
produção
pagamento
training opportunities
training starts
profession changes
materializations
```

### Grupos

```text
created
joins
join refusals por causa
duplicate-cause creation
OrganizationalCompatibility distribution
meetings
contributions
```

### Facções

```text
formalization candidates
gate funnel
formalizations
membership
actions
task delegation
```

### Política

```text
proposals
support
delivery
decision
policy
policy work
completion
latencies
delegation
```

### Crime/justiça

```text
crimes
witnessed
authority learned
wanted
investigation
lead
pursuit
contact
capture
resolution
```

### Violência

```text
attacks por motivo
incapacitations
terminal opportunities
finish
spare
capture
help
withdraw
combat deaths
```

### Religião

```text
prayer
seek contact
access
rite
audience
intervention
contract
gate failures
```

---

# 63. NÃO DEFINIR QUOTAS DE HISTÓRIA

Não exigir:

```text
>= 1 apoteose
>= 3 facções
>= 20 capturas
```

Um mundo pode legitimamente não produzir isso em 300h.

O critério é:

> quando existem condições suficientes, o ciclo consegue avançar?

E, quando não avança:

> conseguimos explicar exatamente por quê?

---

# 64. CRITÉRIO DE COERÊNCIA

Um comportamento pode ser raro e coerente.

Pode ser frequente e coerente.

Pode ser frequente e incoerente.

Pode ser raro porque o modelo está quebrado.

A Fase 6 deve distinguir esses quatro casos.

---

# 65. NÃO OTIMIZAR SAVE AGORA

O save grande permanece dívida técnica conhecida.

Não trocar JSON, implementar banco ou compressão estrutural nesta fase, salvo necessidade bloqueante.

Coerência primeiro.

---

# 66. FORA DO ESCOPO DEMOGRÁFICO

Continuam fora:

```text
gravidez
filhos
nascimento
infância
crescimento
envelhecimento
morte natural por idade
dinastias
gerações
```

Esses sistemas serão tratados quando houver a mudança futura:

```text
hora → turno
```

Não antecipar.

---

# 67. RESULTADOS ESPERADOS DA FASE

Não esperamos um mundo “perfeito”.

Esperamos:

```text
menos emergência estrutural sem causa
menos single points of failure
mais continuidade de processos existentes
grupos mais explicáveis
facções com funil compreensível
carreira funcional quando há demanda
justiça capaz de completar casos reais
LOD semanticamente neutro
religião rara por gates reais
economia sustentável quando possui capacidade
escassez real quando não possui
```

---

# 68. RELATÓRIO FINAL

Criar:

```text
FASE_6_0.md
```

com:

1. baseline da 5.5.5;
2. hipóteses testadas;
3. mudanças realizadas;
4. mudanças rejeitadas;
5. métricas antes/depois;
6. controlled runs;
7. campanha natural;
8. regressões;
9. funis;
10. casos causais reais;
11. efeitos emergentes inesperados;
12. sistemas ainda desequilibrados;
13. decisões deixadas para fase posterior.

---

# 69. COERENCIA.md

Criar relatório específico:

```text
COERENCIA.md
```

Para cada grande sistema:

```text
função pretendida
comportamento observado
coerente?
por quê?
gargalo
mudança
efeito
risco restante
```

---

# 70. DECISOES_6.md

Preservar casos reais especialmente úteis.

Exemplos:

```text
NPC evitou morrer por acesso melhor
NPC morreu apesar de recurso existir — explicar por quê

NPC escolheu trabalho
NPC iniciou treinamento

NPC entrou em grupo existente
NPC criou outro grupo e explicar divergência

representante assumiu tarefa do líder

guarda recebeu caso institucionalmente e capturou
ou explicar por que não conseguiu

grupo chegou perto da formalização e falhou em gate X

mortal buscou divindade e parou em gate Y
```

Não inventar histórias.

---

# 71. BALANCEAMENTO.md

Registrar alterações numéricas de forma explícita:

```text
valor anterior
valor novo
motivo causal
evidência
efeito controlado
efeito natural
```

Qualquer threshold alterado deve aparecer aqui.

---

# 72. NÃO ESCONDER EFEITOS COLATERAIS

Exemplo:

se reduzir privação também reduzir furto em 60%:

registrar.

Não tentar restaurar crime imediatamente só porque caiu.

Primeiro perguntar:

> o crime anterior era parcialmente consequência da fome?

---

# 73. SUCESSO DA FASE 6.0

A fase não termina porque:

```text
mortes diminuíram
```

Ela termina quando conseguirmos explicar:

```text
por que diminuíram
```

E também explicar:

```text
por que as mortes restantes ocorreram.
```

O mesmo vale para:

```text
emprego
crime
captura
grupo
facção
política
violência
religião
```

---

# PRINCÍPIO FINAL

A Fase 5.5.5 tornou o simulador confiável.

A Fase 6.0 deve tornar o mundo coerente.

Não procurar números bonitos.

Procurar cadeias causais que façam sentido.

O objetivo é que:

```text
RESULTADO
↑
AÇÃO
↑
DECISÃO
↑
UTILITY
↑
GATES
↑
NEED / PRESSÃO
↑
CONHECIMENTO
↑
ESTADO DO MUNDO
```

continue sendo verdadeiro,

mas que o próprio estado do mundo e a interação entre sistemas deixem espaço para uma vida além de:

```text
comer
beber
dormir
não morrer
```

quando as condições materiais realmente permitem isso.