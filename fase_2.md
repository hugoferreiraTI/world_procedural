# FASE 2 — VIDA E CONTINUIDADE

## Escopo desta etapa

Esta etapa possui APENAS três objetivos principais:

1. Corrigir os quatro bugs confirmados restantes.
2. Completar o sistema de personalidade já existente.
3. Implementar necessidades pessoais não fisiológicas.

Não implemente ainda:

- Guerra
- Exércitos
- Combate
- Equipamentos completos
- Deuses
- Religião organizada
- Diplomacia completa
- Reposição profissional
- Mudança de profissão
- Nascimento/envelhecimento
- Hereditariedade
- Caravanas
- Viagens autônomas entre cidades
- IA generativa
- Um novo sistema de quests
- Um novo sistema de decisão
- Um novo planner/GOAP

Esses sistemas pertencem a etapas posteriores.

Leia integralmente antes de modificar código:

- `instruction.md`
- relatório comparativo mais recente
- relatório de hardening
- auditoria dos 10.000 turnos
- relatório de histórias/NPCs
- código atual
- testes existentes

Antes de implementar qualquer coisa, faça um levantamento do que já existe.

Não crie sistemas paralelos para funcionalidades que já existem parcialmente.

# 1. Princípio arquitetural obrigatório

O motor atual já possui:

```text
Estado do mundo
↓
Percepção / Conhecimento
↓
Necessidade
↓
Prioridade
↓
Soluções possíveis
↓
Objetivo
↓
Ação
↓
Consequência
↓
Novo estado do mundo
```

PRESERVE esse fluxo.

O objetivo desta fase é adicionar novos tipos de pressão, personalidade e soluções ao sistema atual.

Não substitua o motor existente por:

```text
Behavior Tree
GOAP separado
FSM global
novo Utility Engine
novo Quest Engine
```

Se o sistema atual já possui abstração para `Need`, `Goal`, candidatos de ação, utility/score ou prioridade, reutilize-a.

A regra conceitual continua sendo:

```text
Necessidade
+
Personalidade
+
Contexto
+
Conhecimento
+
Relacionamentos
=
Preferência entre soluções possíveis
```

Personalidade NÃO executa ação.

Necessidade NÃO executa ação.

Ambas modificam a escolha realizada pelo sistema já existente.

# 2. Não rebalancear fome artificialmente nesta fase

A auditoria mostrou forte predominância de fome, comida, sede e descanso.

Entretanto, não conclua automaticamente que fome possui peso excessivo.

Atualmente existem muito mais soluções executáveis de sobrevivência do que necessidades sociais/pessoais executáveis.

Primeiro amplie o espaço comportamental.

Não faça correções como:

```python
hunger_priority *= 0.3
```

apenas para produzir artificialmente maior variedade.

A fome continua sendo uma necessidade real e poderá continuar vencendo outras necessidades quando estiver crítica.

Após a implementação das novas necessidades, uma nova auditoria deverá medir se a predominância fisiológica diminuiu naturalmente.

Somente depois disso deverá ser considerado rebalanceamento significativo.

# 3. Corrigir os quatro bugs confirmados

Antes de ampliar comportamento, corrija os quatro bugs conhecidos e crie testes de regressão para cada um.

## 3.1 Ordem temporal diferente entre jogador e NPC

Hoje existe assimetria:

```text
Jogador
→ executa comer
→ tempo avança
→ fisiologia

NPC
→ fisiologia
→ possível morte
→ decisão
→ comer
```

Isso permite que duas entidades equivalentes tenham resultados diferentes.

Defina uma semântica temporal comum.

Não crie exceção específica para NPC.

A regra deve ser válida para qualquer entidade submetida ao mesmo relógio.

O sistema precisa definir claramente quando acontecem:

```text
decisão
ação
passagem do tempo
fisiologia
verificação de morte
```

Crie teste com jogador e NPC em condições equivalentes:

```text
vida crítica
fome crítica
sede não crítica
comida disponível
```

O resultado deverá obedecer à mesma regra temporal.

## 3.2 Pedido de ajuda bloqueado por valor fixo de moedas

Atualmente um NPC pode possuir:

```text
10 moedas
comida custando 14
```

O sistema de objetivos corretamente conclui:

```text
não consegue comprar
→ pedir ajuda é solução possível
```

mas o sistema de quest posteriormente bloqueia porque:

```text
money >= 10
```

Não mantenha duas definições diferentes de:

```text
"NPC consegue resolver sua necessidade sozinho"
```

Extraia ou reutilize uma avaliação única de viabilidade.

Ela deverá considerar, quando conhecido:

```text
dinheiro
preço
estoque
local acessível
item necessário
```

O mesmo resultado utilizado para pontuar `buy_food` deverá ser respeitado pelo sistema que oferece ajuda.

## 3.3 Ação inválida produz efeitos persistentes

Uma ação rejeitada atualmente pode criar necessidade e consumir ID mesmo sem avançar o turno.

Corrigir.

Fluxo esperado:

```text
intenção
↓
validação de precondições
↓
ação válida?
   não → nenhum efeito persistente
   sim → execução
↓
efeitos persistentes
```

Uma ação rejeitada NÃO poderá:

```text
criar Need
criar Goal
consumir EntityID sem necessidade
criar evento
criar memória
mudar reputação
alterar inventário
```

a menos que a própria tentativa seja um acontecimento observável definido explicitamente pelo design.

## 3.4 Evidência melhor para fato já conhecido

Atualmente:

```text
FactID = 500
confidence = 30
```

pode impedir uma transmissão posterior:

```text
FactID = 500
confidence = 95
```

apenas porque o ID já é conhecido.

Corrigir sem quebrar idempotência.

Separar conceitualmente:

```text
Fato
Crença no fato
Fontes conhecidas
Confiança
Interpretação
Efeito social já aplicado
```

Receber evidência melhor pode aumentar a certeza.

Não deverá reaplicar automaticamente reputação como se fosse um segundo acontecimento.

Exemplo:

```text
Rumor:
FactID 500
confidence 30

↓ posteriormente

Testemunha confiável:
FactID 500
confidence 90

Resultado:
confidence aumenta

NÃO:
reputação aplicada novamente
```

# 4. Completar personalidade sem criar sistema paralelo

O projeto já possui traços de personalidade.

Antes de adicionar qualquer campo:

1. Liste todos os traços atuais.
2. Localize onde são gerados.
3. Localize onde alteram decisões.
4. Localize como são serializados.
5. Identifique quais novos conceitos já podem ser representados pelos traços atuais.

Não adicione dois traços que representam praticamente a mesma dimensão psicológica.

## 4.1 Personalidade estável versus estado emocional

Separe conceitualmente:

```text
Personalidade
```

de:

```text
Estado emocional momentâneo
```

Exemplo:

```text
Irascibilidade = traço relativamente estável

Raiva atual = resposta temporária a um acontecimento
```

Nesta fase NÃO é necessário construir um sistema emocional completo.

Caso seja necessário representar ira dentro da personalidade, prefira um conceito estável equivalente a:

```text
temperamento / irascibilidade
```

A morte de um familiar pode produzir uma necessidade ou pressão emocional.

Não transforme:

```text
Raiva = 200
```

em um valor permanente apenas porque um acontecimento irritou o personagem.

## 4.2 Traços a analisar

A especificação prevê comportamento relacionado a conceitos como:

```text
ira / temperamento
rancor / vingatividade
ambição
cinismo / falsidade
lealdade familiar
```

Adicione somente aquilo que representa informação nova.

### Honestidade versus falsidade

Se `honesty` já representa disposição para mentir, trapacear ou agir desonestamente:

```text
Falsehood = 100 - Honesty
```

não justifica necessariamente outro campo persistente.

Não crie:

```text
honesty
falsehood
```

como dois valores independentes se representam o mesmo eixo.

`Cynicism` só deverá existir separadamente caso represente algo diferente, por exemplo:

```text
desconfiança sobre as intenções dos outros
tendência a esperar comportamento egoísta
```

### Persistência versus rancor

Persistência existente pode significar:

```text
continuar perseguindo um objetivo
```

Rancor/vingatividade significa algo diferente:

```text
manter pressão por retaliação após dano pessoal
```

Se essas funções forem realmente diferentes no motor, `vengefulness` ou equivalente pode existir como traço separado.

### Lealdade familiar

O grafo já possui relações e lealdades entre entidades.

Não duplique:

```text
relationship loyalty
```

com outro valor idêntico dentro de personalidade.

Caso seja necessário um traço de personalidade, ele deve representar uma predisposição geral:

```text
family_orientation
```

ou equivalente:

> Quanto este personagem tende a priorizar parentes em comparação com outras relações.

A força concreta da relação continua vindo do grafo.

Portanto:

```text
prioridade familiar =
força da relação específica
+
tipo de relação
+
predisposição familiar
+
contexto
```

### Ambição

Ambição deverá representar predisposição para desejar ascensão.

Ela NÃO é, sozinha, um objetivo.

```text
Ambition = personalidade

ImproveStatus / GainInfluence / ImproveWealth
= necessidades ou objetivos concretos
```

Um NPC com ambição alta deverá ter maior probabilidade de desenvolver e manter necessidades relacionadas a crescimento pessoal.

## 4.3 Personality ≠ deterministic action

Nunca faça:

```python
if npc.vengefulness > 70:
    npc.attack(killer)
```

O comportamento esperado é:

```text
acontecimento
↓
necessidade surge
↓
possíveis respostas
↓
personalidade modifica scores
↓
ação/contexto disponível decide
```

Exemplo:

```text
Pai morreu.

Possíveis respostas:

Lamentar
Denunciar responsável
Evitar responsável
Investigar
Buscar proteção
Buscar vingança
Pedir ajuda
```

Um personagem vingativo pode aumentar `SeekRevenge`.

Um personagem medroso pode aumentar `AvoidThreat`.

Um personagem compassivo pode reduzir soluções extremamente violentas.

Um personagem independente pode favorecer agir sozinho.

Isso deverá utilizar a infraestrutura de scoring já existente.

# 5. Determinismo da personalidade

A geração dos novos traços deverá continuar utilizando o RNG determinístico existente.

Mesma:

```text
seed
versão das regras
estado
```

deve produzir os mesmos personagens.

Não utilize RNG global independente.

Se o sistema atual trabalha em escala diferente de `0-100` ou `0-200`, preserve a escala atual.

Os números presentes em `instruction.md` são conceituais.

Não faça migração de todos os traços apenas porque o documento possui exemplos como:

```text
raiva = 200
compaixão = 100
```

# 6. Necessidades pessoais além da sobrevivência

O sistema atual já possui necessidades como:

```text
fome
sede
descanso
dinheiro
trabalho
segurança
```

NÃO recrie essas necessidades.

Implemente novas necessidades usando a infraestrutura existente.

Nesta fase, o foco é:

```text
família
luto
vingança
proteção
renda/estabilidade financeira
status
ambição/ascensão
```

Cada nova necessidade só poderá ser considerada funcional se possuir:

```text
gatilho real
Source
Reason
TargetID quando aplicável
prioridade
condição de satisfação
condição de expiração
pelo menos uma solução executável
integração com personalidade
integração com conhecimento
```

Não adicione `NeedType` que nunca consegue produzir comportamento.

# 7. Necessidades familiares

Não implementar ainda nascimento, descendência ou hereditariedade.

Utilize o grafo familiar existente.

Novas necessidades podem surgir de relações que já existem.

Exemplos:

```text
HelpFamilyMember
CheckFamilyMember
FindFamilyMember
ProtectFamilyMember
```

Não necessariamente precisam ser quatro classes diferentes.

Escolha a modelagem que melhor se encaixar na arquitetura atual.

## 7.1 Conhecimento obrigatório

Um NPC não pode procurar um familiar porque o motor global sabe que ele desapareceu.

Ele precisa perceber alguma anomalia.

Exemplo:

```text
esposa possui rotina conhecida
↓
deveria ter retornado
↓
não está presente
↓
NPC percebe ausência
↓
Need: FindFamilyMember
```

Se a infraestrutura atual ainda não consegue representar expectativa de retorno, implemente a versão mínima coerente possível sem criar viagens entre cidades.

Por exemplo:

```text
familiar conhecido normalmente presente
familiar deixou de ser localizado por período relevante
```

O motivo deverá permanecer rastreável.

## 7.2 Relação modifica prioridade

Exemplo:

```text
Conhecido desapareceu
relation = 15

Irmão desapareceu
relation = 80

Filho desapareceu
relation = 98
```

Não transforme simplesmente:

```text
family = prioridade 100
```

Considere:

```text
relationship strength
relationship type
family orientation
personality
time missing
danger known
```

# 8. Luto

A morte de personagem relacionado deverá poder gerar uma necessidade/estado de luto.

Pré-condições:

```text
CharacterDied existe
NPC conhece/acredita na morte
possui relação relevante com morto
```

Não utilize conhecimento global.

O NPC não pode sofrer luto por uma morte que desconhece.

A intensidade deverá considerar:

```text
tipo de relação
força da relação
personalidade
importância do falecido
circunstâncias conhecidas
```

Luto NÃO deverá significar apenas:

```text
ficar parado
```

Ele poderá modificar temporariamente preferência por:

```text
trabalho
socialização
descanso
buscar companhia
visitar local relacionado
vingança
```

Implemente apenas comportamentos que o motor atual consegue executar.

Não construa nesta fase um sistema emocional completo.

# 9. Vingança

A especificação já prevê vingança como consequência possível de dano pessoal.

Implemente como necessidade derivada de acontecimento real.

Exemplo:

```text
CharacterKilled
↓
NPC conhece o fato
↓
vítima possui relação relevante
↓
interpretação pessoal
↓
Need: Revenge
```

A existência da necessidade NÃO significa:

```text
NPC automaticamente tenta matar o responsável.
```

Nesta fase o jogo ainda não possui combate completo.

Portanto, não implemente combate apenas para satisfazer vingança.

Soluções atualmente possíveis podem incluir, conforme infraestrutura disponível:

```text
investigar responsável
buscar informação
denunciar
espalhar informação
evitar responsável
pedir ajuda
buscar proteção
acompanhar/localizar responsável
```

Se uma solução exige um sistema ainda ausente:

```text
assassinar
duelar
contratar assassino
viajar para outro reino
```

ela deverá permanecer indisponível ou bloqueada.

Não crie o sistema ausente nesta fase.

## 9.1 Personalidade

Exemplo de modificadores:

```text
vingatividade alta
→ aumenta interesse em retaliação

rancor alto
→ reduz decay da necessidade

coragem baixa
→ reduz confronto direto

independência baixa
→ aumenta busca por ajuda

compaixão alta
→ pode reduzir soluções violentas

honestidade alta
→ pode aumentar denúncia formal

cinismo alto, se existir
→ pode favorecer manipulação ou desconfiança
```

Esses são exemplos de intenção.

Adapte ao sistema real de scoring.

# 10. Proteção

Diferencie pelo menos conceitualmente:

```text
SelfProtection
ProtectOther
ProtectHome
```

Não necessariamente precisam ser três tipos persistentes diferentes.

A necessidade pode surgir quando o personagem conhece:

```text
ameaça próxima
crime recorrente
ameaça contra familiar
inimigo conhecido
perigo em sua residência
```

Possíveis respostas dentro do escopo atual:

```text
evitar local
procurar guarda
pedir ajuda
permanecer próximo do protegido
avisar outro personagem
```

Não criar combate novo nesta fase.

# 11. Dinheiro e renda

O relatório afirma que dinheiro e trabalho JÁ existem.

Portanto:

NÃO criar:

```text
NeedMoney2
NeedIncome
FinancialNeed
```

se eles duplicarem as pressões atuais.

Amplie o sistema já existente para diferenciar:

```text
preciso de dinheiro imediatamente
```

de:

```text
minha situação financeira está ruim e preciso melhorar renda
```

A segunda é uma pressão de médio prazo.

Ela pode aumentar com:

```text
dinheiro persistentemente baixo
incapacidade recorrente de comprar necessidades
baixa renda profissional
dívidas futuras se existirem
dependência frequente de ajuda
```

Nesta fase NÃO implemente mudança de profissão.

Utilize soluções que já existem:

```text
trabalhar
vender recurso
realizar atividade profissional
buscar trabalho disponível já suportado
```

Se determinada solução requer mudança profissional, marque como indisponível para esta etapa.

# 12. Status

Implemente uma pressão relacionada à posição social.

Ela deve utilizar sistemas já existentes:

```text
reputação
popularidade
profissão
categoria do personagem
relações
```

Um NPC pode desejar maior reconhecimento quando:

```text
personalidade favorece isso
posição atual é baixa
observa personagens prestigiados
possui feitos próprios
```

Não aumente popularidade magicamente.

`NeedStatus` deverá produzir comportamento capaz de gerar acontecimentos que, por consequência, podem aumentar reputação/popularidade.

Exemplos dentro de sistemas existentes:

```text
ajudar alguém importante
trabalhar diligentemente
assumir responsabilidade local
participar de acontecimento público disponível
```

Não faça:

```text
NeedStatus
→ Popularity += 10
```

# 13. Ambição e ascensão

Não duplique o traço `Ambition` com uma necessidade de mesmo significado sem distinção.

Definição:

```text
Ambition trait:
Quanto o personagem deseja crescer.

Advancement need:
Qual crescimento concreto ele deseja agora.
```

Exemplos de objetivos futuros possíveis:

```text
melhorar riqueza
aumentar status
aumentar influência
conquistar posição profissional melhor
tornar-se figura importante
```

Nesta fase, não implemente ainda mudança de profissão nem promoção `Comum → Importante → Lendário`.

Entretanto, prepare a necessidade de ascensão para que essas futuras ações possam utilizá-la.

Enquanto essas ações não existirem, utilize apenas soluções executáveis atuais ou mantenha a necessidade como `Blocked`.

Isso é comportamento válido.

Uma necessidade pode existir sem solução atual.

O sistema já prevê estado `Blocked`.

# 14. Prioridade das novas necessidades

NÃO criar um segundo sistema de prioridade.

Use o atual.

Novas necessidades devem aproveitar os modificadores já previstos:

```text
BaseUrgency
Time
Personality
Relationship
Danger
Responsibility
Context
```

Para necessidades de longo prazo, evite que ocupem prioridade máxima continuamente.

Exemplo:

```text
Ambição = pressão persistente
```

não significa:

```text
Abandonar comida crítica porque quero ser famoso.
```

Da mesma forma:

```text
Hunger = 25
```

não deve automaticamente vencer:

```text
Filho desaparecido = 90
```

O objetivo desta expansão é permitir competição verdadeira entre necessidades.

# 15. Utility scoring e personalidade

A infraestrutura atual de candidatos deve continuar sendo utilizada.

Cada solução poderá possuir considerações independentes.

Exemplo conceitual:

```text
Action: AskForHelp

Need urgency
Relationship
Trust
Independence
Pride
Distance
Knowledge
Expected success
```

Outra:

```text
Action: InvestigateAlone

Need urgency
Courage
Independence
Danger
Knowledge
Distance
```

Não faça uma função gigantesca como:

```python
decide_everything_about_npc()
```

Mantenha considerações pequenas e modulares.

Quando soluções possuírem scores muito próximos, preserve o mecanismo determinístico atual de desempate.

Se for usado weighted random, ele DEVE utilizar o RNG baseado na seed.

# 16. Não introduzir GOAP nesta fase

Planejamento por ações pode ser útil futuramente para objetivos complexos.

Entretanto, o jogo já possui:

```text
Need
Goal
Solution
Action
```

Não adicione uma biblioteca/framework GOAP apenas porque algumas necessidades agora possuem múltiplos passos.

Primeiro evolua as abstrações existentes.

Somente documente limitações caso um objetivo realmente prove que a arquitetura atual não consegue representar planejamento necessário.

# 17. Quests emergentes: integrar, não reescrever

O sistema de quests já existe e pedidos de ajuda já podem surgir autonomamente.

NÃO reescreva o QuestSystem.

Novas necessidades devem conseguir utilizá-lo quando a solução escolhida for:

```text
pedir ajuda ao jogador
```

Fluxo obrigatório:

```text
acontecimento real
↓
NPC percebe/conhece
↓
Need
↓
prioridade
↓
soluções avaliadas
↓
AskPlayer é escolhida
↓
Quest emergente
```

Nunca:

```text
GenerateRandomQuest()
```

Exemplos possíveis nesta fase:

```text
ajudar a localizar familiar
obter informação
buscar proteção
ajudar com problema pessoal executável
```

Não gere quest impossível de concluir com as ações atuais do jogador.

Se nenhuma interação compatível existir:

```text
Need continua
Goal pode ficar Blocked
```

# 18. Conhecimento continua limitando comportamento

Essa regra é absoluta:

```text
Estado verdadeiro do mundo
!=
Conhecimento do NPC
```

Nenhuma nova necessidade deve permitir acesso mágico ao WorldState.

Exemplo:

```text
Assassino real = NPC 500
```

não significa que o filho da vítima saiba disso.

Ele pode saber apenas:

```text
Meu pai morreu.
```

Então:

```text
Need: DiscoverResponsible
```

pode surgir antes:

```text
Need: RevengeAgainst(500)
```

A vingança contra um alvo específico só deverá surgir quando o NPC acredita possuir informação suficiente para identificar o responsável.

# 19. Eventos e idempotência

Use o Event Bus existente.

Não crie um segundo sistema de eventos.

Eventos relevantes desta fase poderão alimentar necessidades.

Exemplo:

```text
CharacterDied
→ grief evaluation
→ revenge evaluation
```

```text
PersonMissing / absence detected
→ family concern
```

```text
ThreatKnown
→ protection
```

Um mesmo evento não deverá criar indefinidamente necessidades duplicadas.

Utilize:

```text
Source EventID / FactID
```

ou mecanismo equivalente.

Exemplo:

```text
CharacterDied #900
```

não poderá criar:

```text
Mourning #1
Mourning #2
Mourning #3
```

para o mesmo NPC apenas porque recebeu o mesmo fato novamente via rumor.

# 20. Testes obrigatórios

Primeiro preserve todos os testes existentes.

Depois crie testes comportamentais.

No mínimo cubra equivalentes a:

```text
test_player_and_npc_follow_same_survival_timing

test_food_help_uses_real_affordability

test_invalid_action_has_no_persistent_effect

test_stronger_evidence_updates_existing_fact

test_evidence_upgrade_does_not_duplicate_reputation

test_personality_generation_is_seed_deterministic

test_new_traits_survive_save_load

test_low_honesty_does_not_require_duplicate_falsehood_trait

test_family_relationship_can_generate_family_need

test_unknown_death_does_not_generate_grief

test_known_close_relative_death_can_generate_grief

test_same_death_does_not_duplicate_grief_need

test_vengefulness_changes_revenge_utility

test_cowardice_or_low_courage_reduces_direct_confrontation_preference

test_revenge_requires_known_or_believed_target

test_protection_need_uses_known_threat

test_financial_pressure_reuses_existing_money_work_system

test_status_need_does_not_directly_increase_popularity

test_ambition_trait_can_strengthen_advancement_pressure

test_nonphysiological_need_can_beat_mild_hunger

test_critical_survival_need_can_beat_low_priority_ambition

test_new_need_can_create_existing_emergent_quest_flow

test_unresolvable_need_can_become_blocked

test_same_seed_produces_same_decisions
```

Adapte nomes à convenção do projeto.

# 21. Auditoria após implementação

Após testes unitários, execute novamente simulação longa.

Utilize pelo menos uma campanha de:

```text
10.000 turnos
```

com seed reproduzível.

Não altere silenciosamente os pesos para conseguir resultados desejados.

Registre distribuição das necessidades selecionadas.

Separar pelo menos:

```text
fisiológicas
trabalho/renda
família
luto
vingança
proteção
status
ambição/ascensão
```

Também registrar:

```text
quantidade de Needs criadas por categoria
quantidade satisfeita
quantidade expirada
quantidade bloqueada
quantidade que gerou quest
quantidade de quests por tipo
quantidade de eventos familiares relevantes
quantidade de NPCs que demonstraram comportamento diferente diante do mesmo tipo de acontecimento
```

Não estabeleça meta artificial como:

```text
"só 20% das ações podem envolver comida"
```

Queremos observar comportamento emergente.

Se fome continuar dominando, descubra POR QUÊ.

Possibilidades:

```text
fome realmente excessiva
economia ruim
poucas soluções para outras necessidades
novas necessidades não recebem gatilhos
novas ações são inviáveis
prioridade está mal calibrada
```

Relate a causa antes de simplesmente mudar pesos.

# 22. Auditoria qualitativa de personalidade

Além das métricas, procure situações comparáveis.

Exemplo:

Dois NPCs perdem pessoa próxima.

Verifique se:

```text
NPC A
vingativo + corajoso
→ busca retaliação/investigação

NPC B
compassivo + pouco vingativo
→ luto/proteção/família

NPC C
medroso
→ evita responsável ou procura proteção
```

Não force esses resultados.

Procure casos realmente produzidos pela simulação.

Se todos reagirem praticamente igual, considere isso uma limitação.

# 23. Debug obrigatório

Amplie o debug atual para permitir explicar decisões.

Exemplo:

```text
NPC: John Hammer

Active Needs:

Hunger
Priority: 24

FindFamily
Priority: 82
Target: Mary Hammer
Source: absence perceived at turn 850

ImproveIncome
Priority: 41

Candidate solutions for FindFamily:

AskNeighbor: 65
SearchKnownLocation: 78
AskPlayer: 54

Personality modifiers:

FamilyOrientation: +18
Independence: +10 SearchKnownLocation
Courage: +4 SearchKnownLocation

Selected:
SearchKnownLocation
```

Para vingança:

```text
Need:
Revenge

Base: 45
Relationship modifier: +25
Vengefulness: +22
Courage: -8
Compassion: -10

Selected Goal:
InvestigateResponsible
```

O objetivo é entender por que o comportamento emergiu.

# 24. Compatibilidade e persistência

Novos campos de personalidade e necessidades deverão ser corretamente persistidos.

Não faça migração improvisada de saves antigos.

Se o formato de save mudar significativamente:

```text
incrementar versão
```

e documentar incompatibilidade ou implementar migração consciente.

RNG deve continuar persistido corretamente.

# 25. Critérios de conclusão da fase

Esta fase será considerada concluída quando:

```text
os quatro bugs estiverem corrigidos

a personalidade possuir dimensões suficientes para diferenciar respostas relevantes

não houver traços redundantes óbvios

necessidades familiares forem executáveis

luto puder surgir de conhecimento real de morte

vingança puder surgir sem significar ataque automático

proteção puder influenciar decisão

pressão financeira reutilizar o sistema econômico atual

status produzir objetivos e não pontos mágicos

ambição influenciar objetivos de longo prazo

novas necessidades competirem no sistema atual

novas necessidades puderem gerar quests através do sistema existente

fome continuar funcional e perigosa sem ser artificialmente nerfada

save/load permanecer determinístico

a simulação de 10.000 turnos não apresentar regressões graves
```

# 26. Relatório final obrigatório

Ao terminar, produza um relatório contendo:

```text
1. Estado anterior encontrado
2. Sistemas reutilizados
3. Sistemas que deliberadamente NÃO foram recriados
4. Causa e correção dos quatro bugs
5. Traços existentes antes da mudança
6. Traços adicionados
7. Traços que foram deliberadamente NÃO adicionados por redundância
8. Novas necessidades
9. Gatilhos de cada necessidade
10. Soluções executáveis de cada necessidade
11. Integração com personalidade
12. Integração com conhecimento
13. Integração com relacionamentos
14. Integração com quests existentes
15. Testes antigos e novos
16. Resultado da auditoria de 10.000 turnos
17. Distribuição de necessidades
18. Exemplos reais de comportamentos emergentes
19. Bugs ou limitações restantes
20. Recomendações para a próxima etapa
```

Diferencie claramente:

```text
IMPLEMENTADO
PARCIAL
APENAS BASE/DADOS
AUSENTE
```

Não marque como implementado algo que possui apenas novo campo ou enum.

# PRINCÍPIO FINAL

A intenção desta fase não é fazer o NPC parecer inteligente adicionando scripts.

A intenção é ampliar aquilo que ele pode querer.

Antes:

```text
NPC:
"Preciso sobreviver."
```

Depois:

```text
NPC:
"Preciso sobreviver,
mas também tenho pessoas importantes,
medos,
ressentimentos,
responsabilidades,
situação financeira,
posição social
e coisas que quero conquistar."
```

O comportamento final deverá continuar emergindo do mesmo motor:

```text
Necessidade
+
Personalidade
+
Conhecimento
+
Relacionamentos
+
Contexto
→
Escolha entre soluções possíveis
```

Não escreva a história.

Crie condições para que a história aconteça.