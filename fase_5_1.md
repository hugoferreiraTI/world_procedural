# FASE 5.1 — AGÊNCIA, PRESSÃO DO MUNDO E CONTINUIDADE DA AÇÃO

## 0. CONTEXTO

Basear esta fase na entrega atual da Fase 5.

A Fase 5 implementou corretamente:

- grupos;
- propostas;
- prefeitos;
- hierarquia militar;
- facções;
- fé;
- deuses objetivos;
- MythicTraits;
- renome;
- epítetos;
- combate terminal;
- intenção letal situacional e persistente.

O problema observado NÃO é ausência desses sistemas.

O principal gargalo atual é:

> os agentes conseguem perceber, querer, organizar, acreditar e formular intenções, mas frequentemente não transformam isso em AÇÃO concreta suficiente para alterar o mundo.

Exemplos observados:

- milhares de problemas compartilhados;
- milhares de grupos;
- poucas reuniões;
- poucas propostas entregues;
- pouquíssimas decisões políticas;
- facções praticamente sem ações naturais;
- centenas de orações e nenhuma intervenção divina natural;
- intenções letais naturais, mas nenhuma conclusão terminal natural.

Portanto esta fase NÃO deve adicionar uma grande quantidade de novos sistemas.

Ela deve fazer os sistemas atuais **AGIREM**.

---

# 1. PRINCÍPIO CENTRAL

Preservar:

```text
Need
→ Priority
→ Solution
→ Goal
→ Commitment
```

Adicionar uma camada explícita entre intenção e execução:

```text
Need / Interest
→ Priority
→ Solution
→ Goal / Intent
→ ACTION PRESSURE
→ CAPACITY / OPPORTUNITY
→ ACTION
→ CONSEQUENCE
→ LEARNING / NEW STATE
```

A nova pergunta é:

> “por que este agente realmente resolveu agir agora?”

---

# 2. NÃO CRIAR UM TRAIT FIXO DE “AÇÃO”

Não adicionar:

```text
action = 80
```

como personalidade permanente.

A disposição para agir deve ser:

- contextual;
- dinâmica;
- acumulável;
- reduzível;
- explicável.

Nome sugerido:

```text
ActionPressure
```

ou equivalente.

---

# 3. ACTION PRESSURE

`ActionPressure` representa:

> quanto a situação atual está pressionando o agente a transformar intenção em ação concreta.

Não deve representar:

- moralidade;
- raiva isoladamente;
- coragem isoladamente;
- Need isoladamente;
- chance aleatória de agir.

Deve derivar de fatores causais reais.

Exemplos:

```text
urgency
severity
repeated failure
continued deprivation
anger
desperation
commitment investment
perceived injustice
social support
opportunity
persistence
courage
perceived agency
```

com barreiras como:

```text
fear
risk
cost
distance
fatigue
uncertainty
lack of resources
internal disagreement
competing survival needs
```

---

# 4. NÃO USAR SOMA PURA

Fundamental.

Não fazer:

```text
anger 30
+ grievance 20
+ courage 20
+ need 30
= 100
→ extreme action
```

Ações graves não podem aparecer porque muitos fatores médios somaram um valor alto.

O motor deve distinguir:

```text
muitos motivos leves
```

de:

```text
um contexto realmente grave
```

---

# 5. PRESSÃO DO MUNDO

Ações fortes precisam de pressão causal forte proveniente do mundo.

Adicionar conceito equivalente a:

```text
WorldPressure
```

Não necessariamente um campo persistente.

Pode ser uma avaliação derivada dos fatos relevantes.

Ela responde:

> “o que REALMENTE aconteceu para justificar considerar uma resposta desta gravidade?”

---

# 6. ELIGIBILITY ANTES DE UTILITY

Antes de uma ação extrema competir por Utility, verificar se existem pré-condições semânticas suficientes.

Fluxo:

```text
context
↓
semantic eligibility
↓
ActionPressure
↓
capacity
↓
utility competition
↓
action
```

Não permitir que ruído estatístico transforme ação absurda em opção válida.

---

# 7. ESCALA DE GRAVIDADE DAS AÇÕES

Ações diferentes exigem níveis diferentes de pressão contextual.

Conceitualmente:

```text
talk / complain
< organize
< proposal
< protest
< threat
< sabotage
< assault
< kill
< destroy settlement
< confront divinity
```

Não implementar como threshold global simples.

Cada tipo de ação deve ter requisitos semanticamente compatíveis.

---

# 8. NPC INDIVIDUAL

Para NPC, ActionPressure deve considerar:

- Need atual;
- urgência;
- histórico de falhas;
- Commitment;
- perdas;
- ameaça;
- raiva;
- ressentimento;
- medo;
- personalidade;
- perceived_agency;
- oportunidade;
- risco;
- energia;
- distância;
- recursos.

Um NPC pode querer algo e mesmo assim não agir.

Isso é válido.

---

# 9. NÃO AGIR NÃO SIGNIFICA ESQUECER

Se uma pessoa não age agora:

```text
Goal / Commitment
```

pode permanecer.

Pressão pode:

- aumentar;
- diminuir;
- estabilizar.

Não reiniciar a história a cada ciclo.

---

# 10. FRUSTRAÇÃO ACUMULADA

Tentativas relevantes que falham podem aumentar pressão futura.

Exemplos:

```text
pedido ignorado
proposta recusada
tentativa bloqueada
perseguição fracassada
privação continuada
agressão repetida
oração sem resposta
```

Mas evitar:

```text
qualquer falha += raiva
```

Somente falhas relacionadas ao objetivo e conhecidas pelo agente.

---

# 11. PRESSÃO PODE CAIR

ActionPressure não é monotônica.

Pode diminuir quando:

- problema é parcialmente resolvido;
- ameaça desaparece;
- comida chega;
- grupo perde interesse;
- relação melhora;
- agente conclui que não consegue;
- risco aumenta;
- evidência muda;
- tempo reduz relevância.

---

# 12. PERSONALIDADE MODIFICA RESPOSTA, NÃO CRIA CAUSA

Um personagem vingativo não mata porque possui `vengefulness` alto.

Ele pode, quando sofre algo grave:

- manter intenção por mais tempo;
- tolerar mais risco;
- abandonar menos facilmente alternativas violentas.

Da mesma forma:

- courage;
- compassion;
- persistence;
- ambition;
- temperament;
- independence;

modificam a resposta a fatos reais.

---

# 13. ACTION CAPACITY

Separar:

```text
ActionPressure
```

de:

```text
ActionCapacity
```

Perguntas diferentes:

```text
ActionPressure:
"quanto quero agir?"
```

```text
ActionCapacity:
"quanto realmente consigo agir?"
```

---

# 14. PERCEIVED CAPACITY

Quando útil, separar também:

```text
PerceivedCapacity
```

do poder real.

Isso permite erro.

Exemplo:

```text
real capacity = 30
perceived capacity = 80
```

Uma facção pode atacar algo muito forte e ser destruída.

Ou:

```text
real capacity = 90
perceived capacity = 25
```

e permanecer passiva.

---

# 15. COMMITMENT DE RECURSOS

Ação forte deve consumir algo real.

NPC:

- tempo;
- energia;
- dinheiro;
- risco físico.

Grupo:

- coesão;
- membros;
- recursos;
- reputação.

Facção:

- combatentes;
- armas;
- suprimentos;
- dinheiro;
- liderança.

Deus:

- energia divina;
- influência;
- exposição.

Autoridade:

- tesouro;
- recursos;
- legitimidade.

Não criar ação transformadora sem custo quando o contexto exige custo.

---

# 16. GRUPOS POPULARES

Aplicar a mesma lógica aos grupos.

Um grupo não deve existir apenas como:

```text
shared_need
```

Ele precisa poder desenvolver:

```text
CollectiveActionPressure
```

derivado de:

- problema compartilhado;
- continuidade;
- gravidade;
- coesão;
- liderança;
- apoio;
- indignação;
- respostas anteriores;
- confiança institucional;
- perceived capacity.

---

# 17. GRUPO NÃO AGE AUTOMATICAMENTE

Um grupo pode existir durante muito tempo e:

- conversar;
- esperar;
- perder membros;
- dissolver.

Tudo válido.

Mas grupos com alta pressão e capacidade precisam ter maior persistência para tentar ações plausíveis.

---

# 18. CONTINUIDADE POLÍTICA

Corrigir o funil:

```text
problema
→ grupo
→ representante
→ proposta
→ autoridade
→ resposta
→ grupo aprende resposta
→ grupo reage
```

Evitar que a maior parte das histórias morra apenas por falta de propagação prática.

---

# 19. VILAS → CIDADES

Implementar caminho conhecido de representação das vilas.

Uma vila sem prefeito deve saber, quando apropriado, qual cidade/autoridade representa aquela área.

Fluxo físico:

```text
grupo da vila
→ escolhe representante
→ representante viaja
→ entrega proposta
→ resposta é produzida
→ representante ou membro aprende
→ informação retorna ao grupo
```

Sem conhecimento remoto automático.

---

# 20. AÇÃO COLETIVA ESCALONADA

Quando propostas e métodos leves falham, novas ações podem entrar no conjunto elegível.

Exemplo:

```text
complain
→ organize
→ proposal
→ protest
→ boycott
→ threat
→ sabotage
→ violence
```

Não exigir essa ordem rigidamente.

Mas ações mais graves devem normalmente possuir histórico compatível.

---

# 21. RADICALIZAÇÃO

Radicalização deve exigir combinação causal forte.

Fatores:

- privação;
- duração;
- repetidos fracassos;
- repressão;
- membros feridos/mortos;
- responsabilidade atribuída;
- baixa confiança institucional;
- ideologia;
- liderança;
- capacidade.

Não fazer:

```text
anger high
→ radicalize
```

---

# 22. FACÇÕES

Facções precisam possuir cálculo real de ação organizacional.

Conceito sugerido:

```text
OrganizationalActionPressure
```

Derivado de:

- propósito;
- ideologia;
- necessidades;
- recursos;
- ameaças;
- grievances;
- liderança;
- fracassos;
- oportunidades;
- apoio;
- capacidade.

---

# 23. IDEOLOGIA COMO FILTRO DE AÇÃO

Ideologia não deve ser apenas texto.

Ela deve modificar quais soluções são consideradas aceitáveis.

Exemplo:

uma facção pode aceitar:

```text
steal supplies
```

e rejeitar:

```text
harm civilians
```

Outra pode considerar ambos aceitáveis.

Não usar GOOD/EVIL universal.

---

# 24. FACÇÃO PODE ESCALAR AÇÕES

Exemplos possíveis:

```text
recruit
train
negotiate
threaten
steal
raid
sabotage
kidnap
attack
destroy
```

Não criar tudo obrigatoriamente agora.

Priorizar um conjunto pequeno, mas REALMENTE executável.

---

# 25. ROUBAR / ATACAR / DESTRUIR LOCALIDADE

Ações extremamente fortes contra uma vila/cidade devem exigir contexto forte.

Exemplo de elegibilidade:

```text
strong motive
AND
known target
AND
organizational hostility/justification
AND
capacity
AND
resources
AND
acceptable risk
```

e normalmente também:

```text
lower-intensity alternatives failed
OR
ideology strongly permits immediate violence
OR
extreme emergency
```

---

# 26. DESTRUIR UMA VILA NÃO É UM BOTÃO

Se uma facção decide atacar uma vila, a ação deve produzir consequências físicas reais.

Pode envolver:

- viagem;
- membros presentes;
- combate;
- roubo;
- morte;
- perda de recursos;
- estruturas afetadas;
- fuga;
- resposta militar;
- reputação.

Nesta fase não é necessário criar guerra nacional.

---

# 27. NÃO CRIAR “RAID RANDOM”

Facção não invade localidade aleatoriamente para produzir história.

Registrar sempre:

```text
why_this_target
why_now
why_this_action
why_lower_options_failed_or_were_rejected
```

---

# 28. DEUSES

Aplicar a mesma arquitetura.

Deus também é agente.

Não basta possuir:

- domínio;
- energia;
- seguidores;
- oração recebida.

Precisa existir:

```text
DivineActionPressure
```

---

# 29. PRESSÃO DIVINA

Pode considerar:

- perda de fiéis;
- rival religioso crescendo;
- perda de território religioso;
- profanação;
- morte de seguidores importantes;
- pedidos;
- ameaça a domínio;
- rivalidade divina;
- desafio de mortal;
- personalidade;
- valores;
- energia disponível.

---

# 30. FÉ TERRITORIAL

Começar a acompanhar de forma compacta influência religiosa por região/localidade.

Não significa que todos possuem mesma crença.

Registrar algo equivalente a:

```text
local faith influence
```

derivado de seguidores reais/conhecimento.

---

# 31. PERDA DE FÉ

Um Deus deve conseguir perceber, se tiver meios de conhecimento adequados, que:

- seguidores estão diminuindo;
- culto rival cresce;
- locais sagrados perdem influência.

Isso pode aumentar pressão para agir.

Não dar onisciência automática.

---

# 32. INTERVENÇÃO DIVINA COMO ESCALADA

Possíveis níveis de ação:

Pressão menor:

```text
sign
dream
minor blessing
```

Pressão intermediária:

```text
visible miracle
curse
champion support
protection
```

Pressão extrema:

```text
manifestation
direct punishment
major intervention
```

Não transformar isso em tabela rígida.

---

# 33. ZERO INTERVENÇÕES É DIAGNÓSTICO

Na Fase 5 houve oração natural, mas nenhuma intervenção natural.

Investigar:

- Utility nunca vence?
- Deus não conhece situação?
- custo energético é alto demais?
- condições são raras demais?
- Goal é interrompido?
- não existe continuidade?
- nenhuma pressão real chega ao Deus?

NÃO simplesmente aumentar probabilidade de intervenção.

---

# 34. FÉ COMPETINDO POR REGIÃO

Permitir que crenças naturalmente se espalhem e alterem influência local.

Isso pode gerar:

```text
Faith A loses followers
↓
DivineActionPressure(A) rises
```

enquanto:

```text
Faith B grows
↓
confidence / organization / political influence rises
```

Sem guerra religiosa automática.

---

# 35. INTENÇÃO LETAL

Preservar a separação:

```text
LethalPressure
```

responde:

> “quero essa pessoa morta?”

enquanto:

```text
ActionPressure
```

responde:

> “vou realmente fazer algo para isso acontecer?”

---

# 36. MATAR EXIGE PRESSÃO REAL

Não permitir que vários fatores pequenos produzam homicídio.

`kill` precisa de pelo menos uma base semântica grave.

Possíveis exemplos:

- ameaça letal imediata;
- dano físico grave/repetido;
- morte conhecida de pessoa próxima;
- perseguição extrema;
- grievance realmente severo;
- conflito persistente e escalado.

---

# 37. LETALIDADE SITUACIONAL

Preservar o comportamento observado na Fase 5.

Uma ameaça imediata realmente grave pode permitir decisão letal sem arco longo.

Exemplo:

```text
robbery
→ repeated attack
→ victim nearly incapacitated
→ situational lethal response
```

---

# 38. AÇÕES EXTREMAS PRECISAM SER EXPLICÁVEIS

Para ações como:

```text
kill
destroy settlement
assassinate leader
attack temple
confront god
```

registrar auditoria compacta:

```text
eligibility causes
world pressure
action pressure
capacity
major barriers
selected alternative
```

---

# 39. MYTHIC TRAITS

Não aumentar frequência.

A raridade atual está adequada.

MythicTrait deve aumentar capacidade e comportamento em contextos compatíveis, mas não fornecer ActionPressure artificial sem causa.

Justice não deve gerar:

```text
attack unjust god
```

sem que exista:

- conhecimento;
- interpretação;
- grievance;
- capacidade;
- trajetória.

---

# 40. APOTEOSE E MORTE DIVINA

Não calibrar esta fase para fazê-las aparecer.

Zero ocorrências em campanha curta é aceitável.

Apenas garantir que, se existirem todas as condições reais, ActionPressure e continuidade não impeçam artificialmente a ação.

---

# 41. MENOS INTENÇÃO, MAIS CONSEQUÊNCIA

Objetivo desta fase NÃO é aumentar quantidade de:

```text
Needs
Commitments
Groups
Rumors
```

Idealmente podemos até terminar com menos microeventos.

O que queremos aumentar é a razão:

```text
meaningful actions / meaningful intentions
```

---

# 42. NÃO CRIAR HIPERATIVIDADE

Muito importante.

Não queremos transformar todos os agentes em pessoas impulsivas.

Muitas pessoas devem:

- reclamar e não agir;
- querer e desistir;
- participar pouco;
- aceitar situação;
- falhar;
- abandonar.

Ações transformadoras continuam raras.

---

# 43. GRANDES AÇÕES DEVEM TER HISTÓRIAS PESADAS

Quando auditor encontrar:

```text
CharacterKilled
VillageDestroyed
DivineManifestation
LeaderAssassinated
```

o contexto anterior deve normalmente fazer o leitor pensar:

> “caralho, faz sentido isso ter chegado aqui.”

Não:

> “uma soma passou de 70.”

---

# 44. NÃO AUMENTAR ALEATORIEDADE PARA PRODUZIR EVENTOS

Não fazer:

```text
chance_to_act += X
chance_to_intervene += X
chance_to_raid += X
```

como solução principal.

RNG continua apenas para desempates/variação entre opções próximas.

A ação deve nascer da causalidade.

---

# 45. TESTES — REDUZIR DRASTICAMENTE

NÃO repetir uma bateria enorme.

Não criar 30 novos testes compostos.

Criar apenas aproximadamente:

```text
8–12 testes direcionados novos
```

focados EXCLUSIVAMENTE na Fase 5.1.

Prioridades:

1. ActionPressure baixo não gera ação forte.
2. WorldPressure grave torna ação forte elegível.
3. muitos fatores fracos não equivalem a contexto extremo.
4. grupo aumenta ação após falhas reais.
5. grupo reduz pressão após problema resolvido.
6. facção incapaz busca aumentar capacidade.
7. facção com pressão + capacidade executa ação organizacional.
8. Deus reage a perda relevante de influência em cenário controlado.
9. Deus não reage por simples oração isolada.
10. homicídio exige base semântica grave.
11. representação vila → cidade funciona fisicamente.
12. save/load de ActionPressure apenas se novo estado persistente exigir.

Não é obrigatório possuir exatamente 12.

Usar o mínimo necessário.

---

# 46. REGRESSÃO ANTIGA — NÃO RODAR TUDO TODA HORA

Não executar os 275 testes antigos repetidamente durante desenvolvimento.

Durante implementação:

```text
rodar somente testes da Fase 5.1
+
um pequeno smoke set de sistemas críticos
```

Smoke regressions:

- alimentação;
- recuperação;
- conhecimento;
- combate;
- grupos;
- fé.

No máximo alguns testes representativos.

Somente se mudança tocar diretamente um sistema antigo, rodar o subconjunto relacionado.

Uma execução integral final é OPCIONAL.

Se os 275 testes consumirem tempo/espaço excessivo e as mudanças forem bem isoladas, registrar explicitamente que a suíte inteira não foi repetida.

Não fingir que foi.

---

# 47. CAMPANHA CONTROLADA MUITO CURTA

Usar microcenários apenas para provar mecanismos raros.

Não criar dezenas.

Aproximadamente:

```text
4–6 microcenários
```

suficientes.

Exemplos:

- grupo escalando após recusas;
- facção escolhendo raid;
- facção sem capacidade buscando recursos;
- Deus reagindo à perda de fé;
- ação extrema bloqueada sem WorldPressure;
- intenção letal + ActionPressure.

---

# 48. CAMPANHA NATURAL CURTA

NÃO rodar 5000 horas.

Rodar inicialmente:

```text
200 horas
```

para verificar:

- loops;
- explosão de ActionPressure;
- agentes hiperativos;
- grupos violentos demais;
- deuses intervindo demais;
- regressões.

---

# 49. CAMPANHA NATURAL PRINCIPAL

Se 200h estiver estável, rodar apenas UMA campanha principal de:

```text
1000 horas
```

Não 5000.

1000h é suficiente nesta fase porque estamos medindo:

- transição intenção → ação;
- continuidade;
- escalada;
- intervenção;
- ações organizacionais.

Não estamos auditando gerações históricas.

---

# 50. NÃO RODAR SEGUNDA LONGA SÓ PARA OBTER HISTÓRIA MELHOR

Usar a primeira campanha válida.

Mesmo se:

- nenhum Deus intervier;
- nenhuma vila for destruída;
- ninguém executar outro NPC.

Registrar ausência.

Não procurar seed conveniente.

---

# 51. ECONOMIA DE TOKENS

Relatórios devem ser compactos.

Não despejar:

- milhares de eventos;
- logs completos;
- dumps extensos;
- listas gigantes de tentativas.

Priorizar:

```text
métrica agregada
+
alguns exemplos reais representativos
```

---

# 52. ECONOMIA DE DISCO

O projeto já está excessivamente grande.

NÃO duplicar código inteiro da base em várias pastas.

NÃO criar:

```text
baseline_code/
final_code/
entrega_code/
backup_code/
```

para cada tentativa.

Git já deve ser tratado como fonte de histórico quando disponível.

---

# 53. SAVES

Não salvar dezenas de estados intermediários gigantes.

Manter preferencialmente:

```text
1 save final da campanha principal
```

e, se necessário:

```text
1 save curto para diagnóstico
```

Microcenários não precisam necessariamente preservar save completo.

---

# 54. LOGS

Não preservar logs repetitivos de execuções fracassadas, exceto quando necessários para depuração imediata.

Após corrigir bug:

- manter resumo;
- erro;
- correção;
- teste que cobre.

Não guardar centenas de MB de log textual.

---

# 55. EVENTOS

Se possível, para auditoria desta fase exportar somente os eventos relevantes:

```text
ActionPressureChanged
OrganizationalAction
Proposal...
DivineIntervention
ViolenceIntentChanged
Execution...
```

ou gerar relatório filtrado.

Não exportar histórico bruto duplicado se o save já o contém.

---

# 56. HISTÓRIAS REAIS

Gerar relatório compacto:

```text
reports/fase_5_1/HISTORIAS_REAIS.md
```

Selecionar no máximo:

```text
8–10 histórias
```

Não tentar preencher categorias obrigatórias.

Preferir exemplos de:

- intenção que virou ação;
- intenção forte que NÃO virou ação por falta de capacidade;
- grupo escalando;
- grupo desescalando;
- facção agindo;
- facção preparando capacidade;
- Deus reagindo ou não reagindo a perda religiosa;
- homicídio/ação extrema se ocorrer naturalmente.

Se não ocorreu:

dizer explicitamente.

---

# 57. MÉTRICAS MAIS IMPORTANTES

Registrar razão de conversão:

```text
Intentions
→ Actions
→ Consequences
```

Para:

- NPCs;
- grupos;
- facções;
- deuses.

Especialmente:

```text
groups formed
groups with meaningful action
proposals created
proposals submitted
responses learned
organizational actions
prayers
divine action considered
divine interventions
lethal intents
actual pursuit/attack
terminal opportunities
```

---

# 58. AUDITAR ACTION PRESSURE

Coletar distribuição compacta:

```text
low
medium
high
extreme
```

por tipo de agente.

Verificar se:

- quase ninguém chega alto;
- todo mundo chega alto;
- extremos correspondem a contextos realmente graves.

---

# 59. AUDITAR AÇÕES EXTREMAS

Para cada ação extrema natural, selecionar apenas alguns casos e reconstruir:

```text
causa inicial
eventos acumulados
WorldPressure
ActionPressure
capacity
barriers
action selected
consequence
```

---

# 60. CRITÉRIO DE SUCESSO

Esta fase é bem-sucedida se demonstrar que:

- intenção não implica ação automaticamente;
- ações graves exigem contexto grave;
- muitos fatores leves não produzem atrocidade;
- falhas acumuladas podem aumentar iniciativa;
- resolução reduz pressão;
- grupos conseguem atravessar representação e produzir consequência;
- facções conseguem agir quando possuem motivo e capacidade;
- facções sem capacidade tentam adquirir capacidade;
- deuses conseguem responder a ameaças reais à fé/domínio;
- personagens continuam podendo ser passivos;
- ações extremas permanecem raras;
- quando acontecem, são causalmente explicáveis.

---

# 61. FORA DO ESCOPO

Não adicionar:

- guerra entre reinos;
- diplomacia completa;
- conquista territorial;
- sistema nacional de revolução;
- novos panteões;
- novos MythicTraits em massa;
- novas dezenas de políticas;
- sistema geracional;
- exércitos estratégicos completos.

---

# 62. FILOSOFIA FINAL

Até agora o mundo sabe:

```text
perceber
querer
lembrar
acreditar
organizar
```

Esta fase deve fazê-lo aprender a:

```text
AGIR
```

Mas ação não significa hiperatividade.

A ação deve acontecer quando:

```text
o mundo pressionou o agente
+
o agente interpretou essa pressão
+
ele acredita que pode agir
+
possui ou busca capacidade
+
uma solução concreta vence
```

Para ações extremas:

> a personalidade nunca deve ser suficiente.

O mundo precisa ter colocado peso real sobre aquele agente.

Uma morte, destruição, intervenção divina ou ataque político deve carregar história antes de carregar consequência.

Não otimizar para quantidade de acontecimentos.

O objetivo continua sendo:

**coerência causal.**

---

# 63. ENTREGA

Entregar apenas:

- código alterado;
- 8–12 testes novos direcionados;
- poucos microcenários;
- uma curta de aproximadamente 200h;
- uma campanha principal de aproximadamente 1000h;
- métricas compactas;
- HISTORIAS_REAIS.md curto;
- lista de bugs/limitações;
- tamanho final dos novos arquivos gerados.

Não duplicar o código do projeto.

Não gerar dezenas de saves.

Não preservar logs enormes.

Não repetir campanhas simplesmente para obter eventos raros.

Não gastar recursos tentando provar que toda funcionalidade rara apareceu naturalmente.

Esta fase deve ser **menor, mais cirúrgica e mais barata** que a Fase 5.