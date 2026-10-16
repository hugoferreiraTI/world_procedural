# FASE 5.2 — DECISÃO LETAL, CONSEQUÊNCIA DA MORTE, PRESENÇA DIVINA E AFINIDADE COM OS DEUSES

## 0. CONTEXTO

Basear esta fase na entrega atual `mvp-9-fase5.1`.

NÃO reescrever os sistemas existentes.

Preservar:

- Need;
- Priority;
- Solution/Utility;
- Goal;
- Commitment;
- Aspiration;
- WorldPressure;
- ActionPressure;
- ActionCapacity;
- PerceivedCapacity;
- personalidade;
- emoções;
- grievances;
- Knowledge;
- investigação;
- grupos;
- propostas;
- política local;
- facções;
- fé;
- divindades;
- Renown;
- MythicTraits;
- combate;
- justiça;
- Event Bus;
- persistência.

A Fase 5.1 demonstrou que a camada de ação melhorou principalmente a política.

Também demonstrou:

```text
7 mudanças naturais para kill
6 autores
6 autores realmente atacaram com intenção letal
0 ExecutionOpportunity
0 TerminalDecision
```

Portanto, o problema atual NÃO é apenas:

> “NPCs não conseguem querer matar.”

Eles conseguem.

O problema é:

> uma decisão letal ainda é muito difícil de consolidar e continuar até um desfecho.

Ao mesmo tempo:

- facções continuam sem vida natural suficiente;
- deuses não receberam pressão grave conhecida suficiente;
- orações isoladas corretamente não bastaram;
- fé ainda não produz disputa territorial significativa;
- matar alguém ainda produz pouca transformação psicológica/biográfica no próprio matador.

Esta fase deve atacar esses gargalos sem aumentar aleatoriedade arbitrariamente.

---

# 1. BASE CONCEITUAL DE AGRESSÃO

Usar como inspiração conceitual, NÃO como reprodução clínica literal, a estrutura:

```text
INSTIGATION
+
IMPELLANCE
versus
INHIBITION
```

Ou seja:

```text
o mundo produz um gatilho
↓
características/contexto empurram para determinada resposta
↓
barreiras tentam impedir
↓
ação pode ou não atravessar
```

No código atual isso deve conversar com:

```text
WorldPressure
ActionPressure
Personality
Knowledge
Commitment
Barriers
Capacity
```

Não criar outro motor inteiro.

---

# 2. NÃO USAR UMA SOMA LETAL BURRA

Não fazer:

```text
anger + grievance + vengeance > X
→ kill
```

A decisão letal precisa de:

```text
contexto minimamente compatível
+
pressão
+
impulso
-
inibição
+
capacidade percebida
```

MAS:

## IMPORTANTE

A implementação atual está excessivamente conservadora.

Nesta fase, tornar a morte deliberada **mais acessível**.

Não transformar homicídio em evento comum.

Mas também não exigir praticamente uma tragédia perfeita para cada morte.

---

# 3. REDUZIR A BARREIRA CONTEXTUAL DA LETALIDADE

Auditar os requisitos atuais de contexto grave da Fase 5.1.

Reduzir aproximadamente pela metade a intensidade contextual necessária para tornar `kill` elegível.

Isto NÃO significa:

```text
dividir todos os números por 2
```

automaticamente.

Significa:

> situações que antes precisavam estar próximas do extremo para tornar matar plausível devem poder fazê-lo em severidade intermediária quando personalidade, histórico, relação e inibição tornam isso coerente.

Exemplo conceitual:

ANTES:

```text
precisa de X + U + Z + T em níveis quase extremos
```

AGORA:

```text
X/2 + U/2 + Z/2 + T/2
```

podem ser suficientes combinados.

Não exigir perfeição psicológica.

Este é um mundo violento e perigoso.

Morte deve ser rara.

Não ultra-rara.

---

# 4. CONTEXTO AINDA É OBRIGATÓRIO

Apesar da redução:

não permitir homicídio forte surgir apenas de personalidade.

Um NPC extremamente vingativo ainda precisa possuir:

- um alvo;
- alguma causa interpretada;
- alguma oportunidade;
- algum contexto compatível.

O contexto pode ser menos extremo que antes.

Mas não pode ser zero.

---

# 5. TIPOS DE CONTEXTO LETAL

Não criar dezenas de regras especiais.

Agrupar semanticamente contextos gerais como:

```text
reactive_threat
retributive
protective
instrumental
moral_punishment
hedonic / death_seeking
```

Essas categorias servem para interpretação e auditoria.

Elas não devem virar scripts separados.

---

# 6. AMEAÇA REATIVA

Uma ameaça imediata pode produzir decisão letal sem histórico longo.

Considerar:

- dano recebido;
- ameaça percebida;
- repetição;
- possibilidade de fuga;
- capacidade do agressor;
- risco para pessoas próximas;
- medo;
- raiva;
- coragem.

Não exigir múltiplos dias de grievance.

Uma briga grave pode produzir homicídio naquele momento.

---

# 7. VINGANÇA / RETRIBUIÇÃO

Para contexto persistente considerar:

- dano conhecido;
- intenção atribuída;
- perda de pessoa próxima;
- repetição;
- grievance;
- ruminação;
- falha de reparação;
- compromisso;
- humilhação;
- crença de que o alvo merece punição.

Intencionalidade conhecida deve pesar mais do que dano acidental.

Mas percepção pode estar errada.

NPC age segundo o que sabe/acredita.

---

# 8. VIOLÊNCIA MORAL E VIOLÊNCIA INSTRUMENTAL

Separar conceitualmente:

```text
"ele merece sofrer/morrer"
```

de:

```text
"ele precisa morrer para eu obter alguma coisa"
```

Na violência moral/retributiva:

- blame;
- responsabilidade;
- merecimento;
- doutrina;
- justiça percebida;

podem reduzir barreiras.

Na instrumental:

- dehumanização;
- indiferença;
- objetivo;
- ganho;
- baixo vínculo;

podem reduzir barreiras.

Não exigir dehumanização para toda morte.

---

# 9. LETHAL CONSIDERATION

Adicionar ou explicitar estado equivalente a:

```text
LethalConsideration
```

Significa:

> matar entrou nas alternativas plausíveis.

É transitório.

Não significa decisão definitiva.

---

# 10. LETHAL DECISION

Adicionar estado explícito:

```text
LethalDecision
```

ou:

```text
LethalResolution
```

Significa:

> este personagem decidiu que deseja que ESTE alvo morra.

Registrar:

- actor;
- target;
- cause;
- mode;
- supporting facts;
- decision time;
- WorldPressure;
- ActionPressure;
- major impellors;
- major inhibitors;
- confidence;
- related Commitment;
- persistence/intensity.

---

# 11. HISTERESE DA DECISÃO LETAL

Uma vez que `LethalDecision` seja formada:

NÃO recalcular do zero a cada hora.

Fome pode interromper execução.

Sono pode interromper execução.

Viagem pode interromper execução.

Perder o alvo pode interromper execução.

MAS:

```text
eat
```

não significa:

```text
I no longer want target dead
```

A decisão deve persistir.

---

# 12. ENTRAR É DIFÍCIL, SAIR TAMBÉM

Usar histerese conceitual.

A condição necessária para ABANDONAR uma decisão letal deve ser diferente da condição para nunca tê-la tomado.

Pode enfraquecer ou desaparecer quando houver:

- nova informação relevante;
- inocência percebida;
- reconciliação;
- perdão;
- grievance resolvido;
- medo extremo;
- vínculo restaurado;
- intervenção de pessoa importante;
- mudança religiosa/moral;
- queda prolongada da ruminação;
- substituição real do objetivo.

Não usar timeout puro como razão suficiente.

---

# 13. RUMINAÇÃO

Adicionar representação compacta de:

```text
AngryRumination / RevengeRumination
```

Não precisa ser um sistema cognitivo enorme.

Deve representar:

> o quanto aquele personagem continua retornando mentalmente àquela agressão/perda.

Pode crescer por:

- grievance não resolvido;
- repetição;
- humilhação;
- morte de próximo;
- encontro recorrente;
- falhas de reparação.

Pode cair por:

- tempo seguro;
- resolução;
- perdão;
- mudança de interpretação;
- novas prioridades fortes;
- relação reparada.

Ruminação ajuda a sustentar `LethalDecision`.

---

# 14. AÇÃO APÓS DECISÃO LETAL

Com `LethalDecision` ativa, ações compatíveis recebem forte continuidade:

```text
find target
investigate
pursue
confront
attack
prepare
```

Sem criar protagonista obsessivo imortal.

Survival Needs ainda interrompem.

Capacidade ainda importa.

Conhecimento ainda importa.

Distância ainda importa.

---

# 15. NÃO REFAZER O COMBATE

NÃO aumentar dano geral apenas para conseguir cadáveres.

Preservar ataques normais.

O problema observado é continuidade/desfecho, não ausência total de dano.

---

# 16. EXECUTION OPPORTUNITY

Preservar conceito terminal.

Quando:

```text
target incapacitated
AND attacker present
AND attacker capable
AND LethalDecision active
```

criar:

```text
ExecutionOpportunity
```

---

# 17. NOVA AVALIAÇÃO TERMINAL

Quando o alvo é incapacitado, atualizar contexto.

Muito importante:

a ameaça defensiva imediata pode diminuir drasticamente.

Portanto:

```text
defensive instigation
```

deve cair.

Mas:

- revenge;
- moral punishment;
- instrumental objective;
- DeathAffinity;
- sadism;
- divine doctrine;
- persistent grievance;

podem continuar.

---

# 18. TERMINAL DECISION

Na oportunidade terminal competir entre:

```text
finish
spare
capture
help
withdraw
```

Mas NÃO exigir que `finish` atravesse novamente toda a mesma barreira usada para criar `LethalDecision`.

A decisão já foi tomada.

A avaliação terminal pergunta:

> alguma mudança relevante aconteceu para me fazer parar?

Isso é fundamental.

---

# 19. FINISH

Se:

```text
finish
```

vence e o alvo está realmente incapaz de resistir:

```text
CharacterKilled
death_context = deliberate_finish
```

Morte certa dentro da abstração.

Não rolar dano comum novamente.

---

# 20. MORTE DELIBERADA NÃO PRECISA SER EXECUÇÃO

Também permitir:

```text
lethal attack
→ dano físico normal
→ target dies
```

registrando que a intenção era matar.

Separar:

```text
intentional_combat_kill
```

de:

```text
deliberate_finish
```

---

# 21. PÓS-MORTE

Adicionar:

```text
PostKillAppraisal
```

para quem matou alguém.

Não assumir trauma.

Não assumir culpa.

Não assumir prazer.

A reação depende de:

- personalidade;
- fé;
- contexto;
- vínculo;
- intenção;
- vulnerabilidade da vítima;
- justificativa;
- testemunhas;
- reputação;
- grupo;
- valor atribuído à morte.

---

# 22. POSSÍVEIS REAÇÕES PÓS-MORTE

Estados possíveis incluem:

```text
guilt
shame
fear
relief
pride
pleasure
fascination
numbness
grief
moral_conflict
```

Podem coexistir.

Não precisam virar traits.

---

# 23. MORAL INJURY / CONFLITO MORAL

Se o assassinato contradiz fortemente:

- compassion;
- faith;
- personal values;
- attachment;
- prior self-image;

pode produzir estado equivalente a:

```text
moral_conflict
```

com:

- culpa;
- vergonha;
- retirada social;
- desejo de reparação;
- oração;
- confissão futura;
- mudança comportamental.

Não diagnosticar clinicamente.

É uma mecânica narrativa inspirada em conflito moral pós-violência.

---

# 24. SADISMO

Adicionar um traço estável opcional:

```text
sadism
```

0–100.

Distribuição populacional deve ser fortemente concentrada em valores baixos.

Valores muito altos devem ser raros.

Sadismo representa:

> maior potencial de obter satisfação com sofrimento causado.

Não significa homicídio automático.

---

# 25. DEATH AFFINITY

Adicionar estado dinâmico:

```text
DeathAffinity
```

Não confundir com `DivineAffinity`.

Representa:

> associação positiva aprendida com causar morte.

Inicialmente baixa/zero para quase todos.

Pode aumentar quando:

- NPC mata;
- a morte foi intencional;
- `PostKillAppraisal` produz prazer/orgulho/fascinação;
- sadism é alto;
- guilt/harm aversion são baixos;
- a fé ou grupo aprova;
- a morte produz resultado desejado.

---

# 26. DEATH AFFINITY PODE CAIR

Pode diminuir por:

- culpa;
- vergonha;
- consequências ruins;
- punição;
- morte de próximo;
- arrependimento;
- mudança religiosa;
- trauma moral;
- passagem longa sem reforço.

---

# 27. CAMINHO PARA ASSASSINO RECORRENTE

NÃO criar:

```text
first kill
→ serial killer
```

Mas permitir trajetória:

```text
kill
→ positive PostKillAppraisal
→ DeathAffinity rises
→ inhibition decreases
→ violence becomes more attractive
→ another kill
→ reinforcement
```

Eventualmente pode surgir Need/Aspiration equivalente a:

```text
seek_killing
seek_victim
seek_violent_opportunity
```

somente quando o histórico justificar.

---

# 28. HOMICÍDIO HEDÔNICO

Um NPC com:

- sadism alto;
- DeathAffinity alta;
- harm aversion baixa;
- pouca culpa;
- oportunidade;

pode começar a matar sem grievance pessoal intenso.

Ainda precisa de:

- alvo acessível;
- oportunidade;
- capacidade;
- avaliação de risco.

Isso constitui contexto próprio:

```text
hedonic violence
```

e NÃO deve ser confundido com vingança.

---

# 29. ASSASSINO RECORRENTE E KNOWLEDGE

Mortes repetidas devem produzir informação social quando descobertas.

Pode surgir:

```text
"há alguém matando pessoas em X"
```

sem autoria conhecida.

Knowledge preserva:

- mortes;
- padrão;
- região;
- vítimas;
- confiança;
- fonte.

---

# 30. PADRÃO DE HOMICÍDIOS

Adicionar reconhecimento institucional compacto de padrão quando houver:

- múltiplos homicídios;
- proximidade temporal/geográfica;
- assinatura causal compatível;
- autor conhecido ou desconhecido.

Não criar CSI completo.

Apenas permitir:

```text
SerialViolencePattern
```

ou equivalente.

---

# 31. GUARDAS REAGEM A PADRÕES

Um padrão conhecido pode aumentar:

- prioridade do caso;
- compartilhamento institucional;
- investigação;
- busca;
- proteção local;
- vigilância.

Não teleportar conhecimento.

---

# 32. RUMORES SOBRE ASSASSINO

Renown/Knowledge podem produzir:

```text
"o Açougueiro de Karvia"
"o Assassino de Valthon"
```

quando houver conhecimento suficiente.

Epíteto não prova autoria objetiva.

Pode existir acusação errada.

---

# 33. DIVINIZAÇÃO SOCIAL DO ASSASSINO

Em casos extremos, cultura/religião/rumor pode interpretar assassino famoso como:

- escolhido;
- avatar;
- campeão;
- manifestação;
- servo de Deus.

Isto NÃO cria Divinity objetiva.

---

# 34. DEUS DA MORTE E ASSASSINO

Se existir um Deus cujo domínio/valores realmente premiam morte intencional:

adorá-lo NÃO basta para receber grande favor.

O fiel precisa agir segundo os valores desse Deus.

Exemplo:

```text
high devotion
+ zero acts aligned with Death
→ limited DivineAffinity
```

Enquanto:

```text
moderate devotion
+ repeated intentional killing aligned with doctrine
→ potentially high DivineAffinity
```

Isso deve depender da personalidade/doutrina do Deus.

---

# 35. DIVINE AFFINITY

Adicionar relação direcionada:

```text
DivineAffinity(god_id, npc_id)
```

Significa:

> quanto ESTE Deus favorece/valoriza ESTE mortal.

Não confundir com:

```text
Devotion
```

Devotion:

> quanto o mortal ama/acredita/segue o Deus.

DivineAffinity:

> quanto o Deus valoriza aquele mortal.

---

# 36. FONTES DE DIVINE AFFINITY

Pode crescer por:

- ações alinhadas ao domínio;
- cumprir valores;
- defender seguidores;
- realizar ritos;
- sacrifícios;
- espalhar a fé;
- cumprir ordem divina;
- proteger local sagrado;
- destruir inimigo relevante;
- feitos extraordinários coerentes.

Oração e adoração podem contribuir.

Mas não devem ser a principal fonte para deuses orientados à ação.

---

# 37. EXEMPLO: DEUS DA MORTE

Se seu Deus da Morte valoriza assassinato deliberado:

```text
prayer = pequena contribuição
intentional kill = grande contribuição
repeated killing = maior
killing important enemy = ainda maior
```

Mas verificar:

- contexto;
- doutrina;
- autoria conhecida pelo Deus;
- intenção.

Um acidente fatal não deve valer igual a assassinato deliberado.

---

# 38. DIVINE DISAFFINITY

A afinidade pode tornar-se negativa.

Ações opostas ao Deus podem reduzir relação.

Exemplos:

- trair culto;
- proteger alvo condenado;
- destruir templo;
- matar seguidor favorecido;
- agir contra domínio;
- abandonar juramento.

---

# 39. DIVINE BOND

Afinidade extremamente alta pode formar:

```text
DivineBond
```

Não precisa ser outra classe pesada.

Pode ser um estado relacional raro.

Ele permite canal sobrenatural limitado.

O Deus pode receber sinais sobre eventos graves do mortal:

```text
near death
death
major betrayal
major divine-aligned act
```

Isso NÃO significa onisciência geral.

---

# 40. MORTE DE FIEL MUITO FAVORECIDO

Se um mortal com alta `DivineAffinity` é morto:

o Deus pode receber:

```text
DivineBondDeathSignal
```

através do vínculo.

Registrar:

- follower;
- killer se conhecido pelo vínculo/evento;
- location;
- confidence;
- cause.

Isso pode criar:

```text
DivineWorldPressure
```

contra o assassino.

---

# 41. PUNIÇÃO DIVINA

Um Deus pode responder à morte de um favorito com:

- sinal;
- maldição;
- retirada de proteção;
- campeão;
- manifestação;
- punição direta;

conforme:

- afinidade;
- personalidade divina;
- domínio;
- energia;
- conhecimento;
- risco;
- importância do fiel.

Não usar:

```text
favorite killed
→ lightning killer
```

automaticamente.

---

# 42. PROTEÇÃO DIVINA

Alta `DivineAffinity` também deve aumentar Utility para:

- proteger;
- abençoar;
- avisar;
- curar dentro das regras divinas;
- conceder poder;
- intervir contra agressor.

Não garantir intervenção.

---

# 43. PRESENÇA DIVINA REGIONAL

Não criar um mundo físico separado para cada Deus nesta fase.

O chamado “plano divino” deve ser entendido como uma **camada sobrenatural invisível sobreposta às regiões físicas do mundo mortal**.

Usar conceito equivalente a:

```text
DivinePresence
```

Exemplo:

```text
Karvia
├── região física
└── DivinePresence de God_A
```

O Deus está presente naquela região em uma camada não perceptível normalmente pelos mortais.

Não precisa possuir:

- palácio;
- cidade divina;
- mapa próprio;
- população espiritual;
- civilização separada.

Ele simplesmente existe naquela presença sobrenatural regional e pode interferir quando houver causa e capacidade para isso.

---

# 44. LOCALIZAÇÃO DIVINA

Cada Deus deve possuir:

```text
current_region
```

ou conjunto limitado de regiões de presença se isso já for semanticamente coerente com a cosmologia.

A localização importa.

O Deus não deve agir fisicamente do outro lado do mundo sem:

- manifestação apropriada;
- alcance sobrenatural permitido;
- canal coerente;
- ou deslocamento/interferência que respeite as regras existentes.

A presença em uma região NÃO torna o Deus onisciente sobre tudo o que ocorre ali.

Conhecimento continua separado da localização.

---

# 45. INFORMAÇÃO QUE CHEGA AO DEUS

O Deus recebe informações através de canais causais.

Exemplos:

```text
prayer
cult_report
devoted_follower_report
DivineBond
sacred_site_event
direct_manifestation_observation
high_affinity_follower_signal
```

Criar/usar:

```text
DivineMessage
```

contendo:

- source;
- event/fact;
- subject;
- region;
- confidence;
- channel;
- timestamp.

Uma oração continua sendo uma alegação, não verdade objetiva.

---

# 46. DEVOTION E DIVINE AFFINITY

Preservar duas relações distintas:

```text
Devotion(mortal → God)
```

e:

```text
DivineAffinity(God → mortal)
```

Devotion mede:

> quanto o mortal acredita, ama, teme ou segue aquele Deus.

DivineAffinity mede:

> quanto o Deus pessoalmente valoriza aquele mortal.

Alta Devotion NÃO garante alta DivineAffinity.

Um mortal pode amar profundamente um Deus que praticamente não se importa com ele.

Outro pode ser menos devoto, mas realizar repetidamente atos extremamente alinhados ao domínio e tornar-se favorito.

---

# 47. COMO DIVINE AFFINITY CRESCE

A afinidade deve crescer principalmente por comportamento coerente com os valores da divindade.

Exemplo:

um Deus da Morte pode valorizar:

```text
intentional killing
accepted sacrifice
spreading fear
defending the cult
killing significant enemies
```

dependendo de sua doutrina e personalidade.

Portanto:

```text
high devotion
+ no behavior aligned with God
```

pode gerar pouca afinidade.

Enquanto:

```text
moderate devotion
+ repeated meaningful actions aligned with God
```

pode gerar afinidade muito maior.

Oração e adoração podem contribuir, mas não substituir ação quando a própria divindade valoriza atos.

---

# 48. CAMADAS DA COMUNIDADE RELIGIOSA

Não tratar todos os seguidores como equivalentes.

Para cada religião/região, acompanhar ao menos conceitualmente:

```text
Followers
DevotedFollowers
Cultists
Actors
```

## Followers

Pessoas que reconhecem/seguem a fé de forma relevante.

## DevotedFollowers

Fiéis para quem a religião possui grande importância pessoal e comportamental.

## Cultists

Participantes ativos de:

- culto;
- rito;
- propagação;
- organização religiosa;
- manutenção da comunidade.

## Actors

Mortais que realizam ações concretas importantes em favor dos valores ou objetivos do Deus.

Exemplos:

- matar por um Deus da Morte;
- proteger inocentes por uma divindade que valoriza proteção;
- impor julgamento para uma divindade de Justiça;
- conquistar para uma divindade que valoriza conquista;
- defender o culto;
- destruir inimigo religioso relevante.

As categorias podem se sobrepor conforme a implementação permitir.

Não duplicar pessoas artificialmente.

---

# 49. NÃO USAR APENAS CONTAGEM TOTAL

Um Deus com:

```text
Followers = 1000
Devoted = 100
Cultists = 50
Actors = 10
```

não deve considerar equivalente perder:

```text
50 Followers
```

e perder:

```text
5 Actors
```

A perda da camada ativa pode possuir impacto muito maior.

Criar uma análise de:

```text
FaithHealth
```

e não apenas:

```text
FollowerCount
```

---

# 50. FAITH HEALTH

Para cada Deus/região acompanhar tendências compactas como:

```text
follower_count
devoted_count
cultist_count
actor_count

follower_retention
devoted_retention
cultist_retention
actor_retention

new_followers
conversions_out
recent_deaths
recent_growth
recent_losses

rival_growth
regional_share
high_affinity_losses
high_affinity_gains
actor_activity
cult_activity
```

Nem tudo precisa ser campo persistente.

Derivar quando for eficiente.

O objetivo é representar:

> saúde da religião

e não apenas:

> quantidade de pessoas com religion_id.

---

# 51. JANELAS TEMPORAIS

Não reagir a pequenas oscilações de um tick.

Comparar períodos.

Exemplo conceitual:

```text
últimas 100h
versus
100h anteriores
```

ou média móvel equivalente.

Pode manter janelas menores para detectar choques rápidos e maiores para tendência.

Exemplo:

```text
short_term_trend
medium_term_trend
```

Não criar histórico redundante gigante.

---

# 52. PERDA SIMULTÂNEA DE CAMADAS

Uma queda geral é particularmente relevante quando várias camadas deterioram ao mesmo tempo.

Exemplo:

```text
Followers 1000 → 910
Devoted 100 → 78
Cultists 50 → 34
Actors 10 → 5
```

Isso constitui sinal muito mais grave do que:

```text
Followers 1000 → 900
Devoted 100 → 105
Cultists 50 → 53
Actors 10 → 12
```

No segundo caso:

a religião perdeu massa casual, mas seu núcleo ficou mais ativo.

Não interpretar automaticamente como crise.

---

# 53. PERDA DO NÚCLEO

Perdas severas de:

```text
Actors
Cultists
high-DivineAffinity followers
```

podem gerar crise mesmo sem queda expressiva no total de seguidores.

Exemplo:

```text
Followers:
1000 → 940

Actors:
10 → 2
```

pode ser muito mais grave para determinada divindade do que perder 150 seguidores passivos.

---

# 54. PERDA PONDERADA POR DIVINE AFFINITY

A morte, conversão ou abandono de um mortal muito favorecido deve possuir peso especial.

Exemplo:

```text
Follower A DivineAffinity = 15
Follower B DivineAffinity = 30
Follower C DivineAffinity = 94
```

A perda de C pode provocar uma reação muito maior.

Criar conceito derivado equivalente a:

```text
AffinityWeightedLoss
```

Não usar necessariamente soma linear.

Considerar especialmente:

- quantidade de favoritos perdidos;
- afinidade individual;
- papel religioso;
- motivo da perda;
- autoria conhecida;
- importância histórica.

---

# 55. FAITH HEALTH NÃO É UMA SOMA LINEAR GIGANTE

Evitar:

```text
FaithHealth =
Followers*1 +
Devoted*3 +
Cultists*6 +
Actors*12
```

como verdade absoluta.

Pesos podem ajudar internamente, mas decisões importantes devem considerar a composição semanticamente.

Exemplo:

```text
3000 Followers
80 Devoted
10 Cultists
1 Actor
```

pode representar religião numerosa porém pouco ativa.

Enquanto:

```text
180 Followers
70 Devoted
45 Cultists
25 Actors
```

pode representar culto pequeno, porém extremamente intenso.

A divindade deve conseguir distinguir isso.

---

# 56. SAÚDE REGIONAL E GLOBAL

Separar:

```text
RegionalFaithHealth
```

de:

```text
GlobalFaithHealth
```

Um Deus pode estar crescendo globalmente e ainda sofrer crise em uma região específica.

Isso é especialmente importante quando a região é:

- origem histórica da fé;
- grande concentração de seguidores;
- local sagrado;
- região de muitos favoritos;
- centro do culto;
- região disputada com rival.

---

# 57. IMPORTÂNCIA REGIONAL

Adicionar conceito derivado equivalente a:

```text
RegionalReligiousImportance
```

Pode depender de:

- porcentagem dos seguidores globais;
- origem da religião;
- locais sagrados;
- quantidade de cultistas;
- quantidade de Actors;
- favoritos;
- eventos históricos;
- intervenções antigas;
- renown religioso.

Assim:

perder 20% de uma região irrelevante

não precisa ser igual a

perder 20% do berço histórico da religião.

---

# 58. PRESSÃO DE FÉ RIVAL

Crescimento de outra fé importa principalmente quando:

```text
Faith_A decreases
AND
Faith_B increases
```

na mesma região ou população relacionada.

Mas NÃO assumir automaticamente causalidade.

Inicialmente o Deus pode saber apenas:

```text
minha influência está diminuindo
```

sem conhecer a causa.

Relatos, seguidores, cultistas e observação posterior podem revelar:

```text
Faith_B está convertendo meus seguidores
```

---

# 59. EVENTOS RELIGIOSOS DE CHOQUE

Alguns eventos podem alterar `FaithHealth` ou `DivineWorldPressure` muito mais rapidamente do que tendência populacional comum.

Exemplos:

- morte de favorito;
- massacre de cultistas;
- destruição/profanação de local sagrado;
- conversão pública de líder religioso;
- manifestação de Deus rival;
- morte de campeão;
- assassinato repetido de Actors;
- milagre rival observado;
- traição de grande figura religiosa.

Isso não substitui a tendência.

É uma fonte adicional de pressão.

---

# 60. CLASSIFICAÇÃO SEMÂNTICA DA CRISE

Evitar:

```text
FaithScore < 50
→ GodIntervenes
```

Classificar a condição religiosa em estados derivados como:

```text
STABLE
MINOR_DECLINE
CORE_EROSION
REGIONAL_CRISIS
CULT_COLLAPSE
EXISTENTIAL_RELIGIOUS_THREAT
```

A classificação deve considerar:

- magnitude;
- duração;
- quais camadas estão caindo;
- DivineAffinity dos perdidos;
- importância regional;
- crescimento rival;
- atividade do culto;
- perdas de Actors;
- eventos de choque;
- histórico recente.

---

# 61. CRISE NÃO SIGNIFICA INTERVENÇÃO AUTOMÁTICA

`FaithHealth` serve para gerar pressão e oportunidades.

Não fazer:

```text
REGIONAL_CRISIS
→ miracle()
```

Fluxo:

```text
FaithHealth changes objectively
↓
information reaches God
↓
God understands some portion of decline
↓
DivineWorldPressure
↓
DivineActionPressure
↓
candidate interventions
↓
Utility / personality / domain / capacity
↓
action or inaction
```

---

# 62. O DEUS PRECISA SABER

Objetivamente:

```text
Faith_A is collapsing in Karvia
```

não significa:

```text
God_A knows it
```

A informação precisa alcançar a divindade por canal válido.

A presença divina naquela região pode facilitar alguns sinais sobrenaturais/religiosos, mas NÃO concede conhecimento automático de todos os eventos.

---

# 63. PERCEPÇÃO DIVINA AGREGADA

Para evitar exigir uma oração para cada seguidor perdido, permitir que certos canais religiosos produzam informações agregadas.

Exemplo:

um cultista/líder pode reportar:

```text
"nossa congregação perdeu muitos membros em Karvia"
```

O Deus recebe uma informação aproximada.

Não precisa saber instantaneamente:

```text
Follower #1 converted
Follower #2 died
Follower #3 migrated
...
```

Isso mantém causalidade sem transformar conhecimento divino em burocracia impossível.

---

# 64. DIVINE WORLD PRESSURE

Quando a divindade aprende que sua fé está deteriorando:

```text
known FaithHealth decline
↓
DivineWorldPressure
```

A pressão depende de:

- severidade;
- persistência;
- importância da região;
- camada afetada;
- DivineAffinity dos perdidos;
- personalidade do Deus;
- valores;
- domínio;
- rival envolvido;
- choque religioso conhecido.

---

# 65. DIVINE ACTION PRESSURE

Usar arquitetura equivalente à dos demais agentes:

```text
DivineWorldPressure
↓
DivineActionPressure
↓
capacity / energy / presence
↓
candidate interventions
↓
action
```

Não criar IA completamente separada.

---

# 66. QUANDO INTERVIR

Não criar um contador único que determine intervenção automaticamente.

Usar:

```text
known religious decline
+
DivineWorldPressure
+
DivineActionPressure
+
DivineAffinity
+
personality/domain
+
energy/capacity
+
regional importance
+
available interventions
```

para gerar candidatos de ação.

---

# 67. EXEMPLOS DE REAÇÃO DIVINA

Pequena perda de seguidores comuns:

```text
observar
esperar
enviar sinal menor
```

Erosão do núcleo:

```text
favorecer cultista
fortalecer campeão
enviar presságio
```

Perda forte de Actors ou favoritos:

```text
curse
protect
empower
direct warning
```

Colapso regional:

```text
manifestation
major miracle
punishment
direct intervention
```

Isto são possibilidades.

Não sequência fixa.

---

# 68. PERSONALIDADE DIVINA CONTINUA IMPORTANDO

Dois Deuses sofrendo a mesma perda podem reagir de formas completamente diferentes.

Um Deus paciente pode tolerar declínio prolongado.

Um Deus possessivo pode reagir cedo.

Um Deus da Morte pode valorizar mais a perda de assassinos/Actors que a perda de seguidores comuns.

Um Deus da Justiça pode reagir fortemente quando seus seguidores foram perseguidos de forma considerada injusta.

Um Deus orgulhoso pode reagir especialmente à humilhação pública de seu culto.

---

# 69. DIVINE AFFINITY MODIFICA AÇÃO

Quando um Deus avalia intervenção envolvendo mortal específico:

```text
DivineAffinity
```

deve modificar fortemente Utility.

Um favorito pode receber ajuda numa situação que não justificaria intervenção por outro fiel.

Mas ainda deve existir:

- conhecimento;
- energia;
- oportunidade;
- presença/alcance válido.

---

# 70. MORTE DE FAVORITO

Se mortal com `DivineAffinity` muito alta morre:

o Deus pode receber sinal privilegiado quando existir vínculo apropriado.

Isso pode gerar:

```text
FavoredFollowerKilled
↓
DivineWorldPressure
↓
possible punishment / response
```

Não revelar automaticamente autoria se o canal não conhece o assassino.

---

# 71. PROTEÇÃO E PUNIÇÃO DIVINA

Alta afinidade pode aumentar Utility para:

```text
protect
warn
bless
empower
heal within divine rules
curse aggressor
punish killer
```

Não garantir ação.

Punição também depende da personalidade e doutrina da divindade.

---

# 72. CAMPEÕES

Alta `DivineAffinity` + capacidade + trajetória pode produzir estado:

```text
DivineChampionCandidate
```

ou campeão reconhecido.

Não gerar automaticamente.

Um assassino favorecido pelo Deus da Morte pode eventualmente tornar-se campeão.

Um protetor pode tornar-se campeão de uma divindade de Justiça ou Proteção.

---

# 73. DEUS PODE ABANDONAR UM FIEL

Devotion alta não garante reciprocidade.

Se o fiel:

- não age segundo valores;
- trai;
- falha repetidamente;
- age diretamente contra domínio;
- protege inimigos centrais;
- profana algo relevante;

`DivineAffinity` pode cair mesmo que `Devotion` permaneça alta.

---

# 74. RELIGIÃO COMO COMPORTAMENTO

A fé deve diferenciar:

```text
believer
devout believer
cultist
actor
favored believer
champion
socially divinized mortal
actual deity
```

São coisas diferentes.

Uma pessoa pode ocupar mais de uma função.

---

# 75. MORTE + RELIGIÃO + RENOWN

Uma sequência possível, NÃO roteirizada:

```text
NPC mata
↓
DeathAffinity cresce
↓
Deus da Morte aprova
↓
DivineAffinity cresce
↓
rumores dos assassinatos se espalham
↓
epíteto surge
↓
alguns acreditam que ele é campeão/avatar
↓
guardas procuram
↓
culto pode venerá-lo
```

Não criar função que execute essa história inteira.

Cada transição depende dos sistemas existentes.

---

# 76. SERIAL KILLER NÃO É CLASSE

Nunca criar:

```text
npc.type = SERIAL_KILLER
```

Pode existir classificação de auditoria.

Mas no motor deve ser apenas uma pessoa cuja trajetória produziu:

- mortes repetidas;
- DeathAffinity;
- desejo de matar;
- baixa inibição;
- oportunidades;
- evasão de investigação.

---

# 77. FAMA DO ASSASSINO

Renown deve poder refletir:

```text
killing
fear
mystery
cruelty
divine_association
```

Dependendo do conhecimento disponível.

Se autoria for desconhecida:

epíteto pode pertencer à figura social desconhecida/padrão, não ao NPC real.

---

# 78. MEDO SOCIAL

Mortes recorrentes conhecidas numa região podem aumentar estado social/local equivalente a:

```text
fear_of_killer
```

ou pressão de segurança.

Isso pode:

- formar grupos;
- aumentar propostas;
- aumentar demanda por guardas;
- gerar rumores;
- mudar comportamento local.

Não implementar pânico global automático.

---

# 79. GUARDAS MAIS ATIVOS POR HOMICÍDIOS

Homicídio repetido conhecido deve aumentar:

```text
case severity
investigation priority
institutional action pressure
```

Ainda limitado por:

- conhecimento;
- pessoal;
- distância;
- recursos.

---

# 80. HISTÓRIAS EMERGENTES DE MORTE

Queremos agora permitir naturalmente histórias como:

```text
assalto
→ vítima reage
→ decide matar
→ agressor morre
→ vítima sente culpa
→ busca religião
```

ou:

```text
agressão repetida
→ ruminação
→ decisão letal
→ perseguição
→ assassinato
→ família reage
```

ou:

```text
primeiro assassinato
→ prazer/fascinação
→ DeathAffinity
→ nova busca por violência
→ rumor
→ investigação
```

ou:

```text
assassino favorecido por Deus da Morte
→ alta DivineAffinity
→ bênção
→ fama
→ culto interpreta como campeão divino
```

Nenhuma deve ser script.

---

# 81. RELAÇÃO COM PESQUISA

Utilizar apenas como inspiração estrutural:

## I³ Model

```text
instigation
impellance
inhibition
```

Ajuda a separar:

- gatilho;
- forças que empurram;
- forças que seguram.

## Angry Rumination

Usar para persistência de raiva e vingança.

## Moral Disengagement / Moral Justification

Usar para explicar redução de barreira moral em determinados contextos.

## Harm Aversion

Usar para explicar por que vítima incapacitada/sofrendo pode aumentar inibição em alguns NPCs.

## Sadism Research

Usar como inspiração para:

```text
sadism
+
positive affect from violence
→ DeathAffinity
```

## Moral Injury Literature

Usar como inspiração para:

```text
post-kill guilt/shame/conflict
```

quando a morte viola valores do próprio personagem.

NÃO apresentar o simulador como modelo clínico fiel de psicologia humana.

---

# 82. NÃO DEIXAR A PESQUISA TORNAR O MUNDO PACÍFICO DEMAIS

Muito importante.

A literatura deve melhorar a coerência.

Não deve transformar a simulação numa sociedade moderna altamente inibida.

O mundo é perigoso e sombrio.

Portanto:

- gatilhos letais podem ocorrer em severidade moderada;
- inibição pode ser menor;
- armas e violência fazem parte da vida;
- justiça institucional é limitada;
- vingança pode ser culturalmente plausível.

Preservar coerência sem transformar homicídio em evento praticamente impossível.

---

# 83. META QUALITATIVA DE LETALIDADE

NÃO definir:

```text
precisamos de X homicídios
```

Mas em uma população na casa de milhares, com:

- agressões;
- crimes;
- armas;
- grievances;
- vingança;
- guardas;
- cultos;

é esperado que ocasionalmente ocorram:

```text
intentional_combat_kill
deliberate_finish
revenge_homicide
situational_homicide
```

Se continua sempre zero, tratar como possível amortecimento excessivo.

---

# 84. NÃO OTIMIZAR POR CADÁVERES

Ainda assim:

não aumentar dano geral.

não criar chance aleatória de homicídio.

não reduzir todas as barreiras indiscriminadamente.

Queremos:

```text
mais mortes causais
```

e não:

```text
mais mortes estatísticas
```

---

# 85. MÉTRICAS DE LETALIDADE

Registrar:

```text
LethalConsideration
LethalDecision
LethalDecisionAbandoned
LethalAttack
IntentionalCombatKill
ExecutionOpportunity
TerminalDecisionFinish
TerminalDecisionSpare
DeliberateFinish
PostKillAppraisal
DeathAffinityIncrease
ViolenceSeekingCreated
```

---

# 86. MÉTRICAS DIVINAS E RELIGIOSAS

Registrar compactamente:

```text
DivineMessage
DivineAffinityChanged
DivineBondCreated
FavoredFollowerKilled

Followers
DevotedFollowers
Cultists
Actors

RegionalFaithHealthChanged
GlobalFaithHealthChanged
CoreErosionDetected
RegionalReligiousCrisisDetected
CultCollapseDetected

HighAffinityFollowerLost
FaithInfluenceChanged
FaithLossLearnedByGod
RivalFaithGrowthKnown

DivineActionConsidered
DivineIntervention
DivinePunishment
DivineProtection
ChampionCandidate
```

Evitar telemetria explosiva por tick.

Preferir transições significativas.

---

# 87. AUDITORIA DE CAUSA LETAL

Para cada morte deliberada natural, registrar compactamente:

```text
who
target
mode
initial cause
supporting facts
WorldPressure
ActionPressure
LethalDecision time
rumination
inhibition
capacity
terminal context
post-kill reaction
```

---

# 88. AUDITORIA DE ASSASSINO RECORRENTE

Se ocorrer:

registrar trajetória completa, mas compacta:

```text
first kill
PostKillAppraisal
DeathAffinity
second kill
Renown/rumor
guard response
religious reaction
```

Não inventar serial killer caso não ocorra.

---

# 89. AUDITORIA DIVINA

Se Deus intervier naturalmente:

registrar:

```text
God
current region
what God knew
how God learned
RegionalFaithHealth
GlobalFaithHealth
affected layers
high-affinity losses
rival growth if known
DivineAffinity if target-specific
DivineWorldPressure
energy
chosen intervention
effect
witnesses
rumors
```

---

# 90. PERSISTÊNCIA RELIGIOSA COMPACTA

Salvar apenas o necessário para reconstruir:

- seguidores relevantes;
- categorias religiosas;
- afinidades divinas importantes;
- vínculos;
- conhecimento divino;
- tendências necessárias;
- presença regional;
- energia.

Não manter logs ilimitados de oração ou snapshots completos de FaithHealth por hora.

Preferir eventos de mudança.

---

# 91. NÃO CRIAR AFTERLIFE AINDA

A presença divina regional NÃO implica sistema completo de pós-vida.

Não implementar:

- almas de todos os mortos;
- julgamento pós-morte;
- população de mortos;
- economia espiritual.

Pode vir futuramente.

---

# 92. NÃO CRIAR GUERRA DIVINA AINDA

Deuses podem:

- conhecer rivais;
- perder fé;
- ganhar fé;
- reagir;
- favorecer mortais;
- interferir.

Não implementar:

- exército divino;
- guerra completa entre deuses;
- conquista de planos;
- sistema de guerra religiosa nacional.

---

# 93. NÃO REFORMULAR POLÍTICA/FACÇÕES

A Fase 5.1 melhorou claramente política.

Não reescrever sociedade.

Apenas integrar efeitos novos:

- assassinatos;
- medo;
- religião;
- favores divinos;
- rumores;
- investigação;
- conflitos religiosos locais.

---

# 94. TESTES — MANTER PEQUENO

Criar aproximadamente:

```text
8 testes novos
```

Não mais que 10 salvo necessidade real.

Prioridades:

1. decisão letal forma-se com contexto moderado coerente após redução da barreira;
2. personalidade sem causa não forma decisão letal;
3. `LethalDecision` persiste através de fome/sono e só muda com causa relevante;
4. alvo incapacitado produz `finish/spare` coerente;
5. `PostKillAppraisal` gera culpa em um perfil e `DeathAffinity` em outro;
6. `DivineAffinity` cresce muito mais por ato alinhado relevante que por simples oração;
7. perda combinada de Followers/Devoted/Cultists/Actors gera crise adequada, enquanto perda apenas de massa com núcleo crescente não gera falsa crise;
8. Deus só reage à deterioração religiosa depois de recebê-la por canal válido.

Opcional, se realmente necessário:

9. perda de favorito pesa mais que seguidores comuns e pode gerar resposta;
10. rumor de assassino aumenta prioridade institucional sem revelar autor automaticamente.

---

# 95. REGRESSÃO

Não rodar novamente toda suíte antiga de centenas de testes durante desenvolvimento.

Rodar:

```text
novos testes
+
smoke crítico pequeno
```

Smoke:

- conhecimento;
- combate;
- grupo;
- fé;
- save/load.

No máximo aproximadamente 15–20 testes selecionados nesta fase, salvo bug real.

---

# 96. MICROCENÁRIOS

No máximo:

```text
4 microcenários
```

1. autodefesa → kill → incapacitação → spare/finish;
2. assassinato → guilt versus DeathAffinity;
3. fiel do Deus da Morte → atos alinhados → DivineAffinity;
4. deterioração religiosa composta / morte de favorito → informação válida ao Deus → possível intervenção.

Microcenário prova capacidade.

Não conta como lore natural.

---

# 97. CAMPANHA NATURAL

NÃO rodar 5.000h.

NÃO rodar várias seeds procurando história boa.

Rodar:

```text
uma campanha de 500 horas
```

Se houver erro estrutural que invalide a campanha cedo, corrigir e reiniciar uma única vez.

Não trocar seed porque houve poucas mortes, nenhuma intervenção ou nenhuma história épica.

---

# 98. SAVE E CUSTO

Manter:

```text
1 save final
```

Não duplicar código inteiro.

Não exportar histórico bruto gigante separadamente.

Não criar múltiplas cópias de:

```text
baseline_code
final_code
entrega_code
backup_code
```

Usar patch/diff/git quando possível.

---

# 99. RELATÓRIO TÉCNICO

Criar relatório técnico separado do arquivo de histórias.

O relatório deve conter:

- alterações implementadas;
- arquitetura;
- testes;
- métricas;
- conversões;
- mortes por causa;
- mortes deliberadas;
- decisões letais;
- abandonos de decisão;
- ExecutionOpportunity;
- finish/spare;
- PostKillAppraisal;
- DeathAffinity;
- padrões de homicídio;
- resposta institucional;
- DivineAffinity;
- composição religiosa;
- FaithHealth;
- mensagens recebidas pelos deuses;
- intervenções;
- gargalos;
- bugs;
- limitações;
- custo de execução;
- tamanho dos arquivos.

Este arquivo é o lugar para tabelas técnicas, percentuais, contadores e conclusões de engenharia.

---

# 100. HISTORIAS_REAIS.MD NÃO É UM RELATÓRIO

Criar:

```text
reports/fase_5_2/HISTORIAS_REAIS.md
```

Mas NÃO escrevê-lo como segundo relatório técnico.

O objetivo é:

> contar o que aconteceu naquele mundo.

Ele deve ser legível como uma pequena crônica documental da seed.

Continuar absolutamente fiel aos eventos reais.

Não inventar pensamentos.

Não inventar motivações não registradas.

Não transformar hipótese em fato.

Não usar microcenários como lore natural.

---

# 101. ABERTURA DO HISTORIAS_REAIS.MD

Começar apresentando o mundo daquela seed.

Exemplo de estrutura:

```text
# Histórias reais — Fase 5.2

Seed: X
Duração: 500 horas
População inicial: X
População final: Y
Localidades: X
Reinos: X
Facções existentes: X
Deuses: X
```

Depois descrever em prosa os elementos do mundo.

---

# 102. PROFISSÕES DO MUNDO

O arquivo deve dizer quais profissões existiram e sua distribuição relevante.

Exemplo:

> Selvaren iniciou a campanha com 1.742 habitantes persistentes. Entre as profissões registradas havia padeiros, agricultores, guardas, comerciantes, ferreiros...

Se houver muitas profissões:

não listar centenas individualmente.

Apresentar:

- quantidade de profissões distintas;
- profissões mais comuns;
- profissões raras interessantes;
- profissões de NPCs que participarem das histórias selecionadas.

Exemplo:

```text
Foram observadas 18 profissões distintas.
As mais frequentes foram X, Y e Z.
```

Isso é descrição do mundo, não avaliação técnica.

---

# 103. RELIGIÕES E DEUSES NO HISTORIAS_REAIS.MD

Apresentar os Deuses PELO NOME.

Não escrever apenas:

```text
God #1
God #2
```

Informar, quando existente:

- nome;
- domínio;
- valores principais;
- regiões de maior influência;
- quantidade aproximada de seguidores;
- Devoted;
- Cultists;
- Actors;
- favoritos relevantes;
- intervenções ocorridas.

Exemplo de estilo:

> O culto de **Nharos, Deus da Morte**, tinha 843 seguidores no início da campanha, dos quais 71 eram devotos, 26 participavam ativamente do culto e cinco haviam praticado atos reconhecidos como alinhados à divindade.

Usar apenas dados existentes.

---

# 104. EVENTO INICIAL

Identificar, quando a seed possuir um primeiro evento relevante registrado:

```text
qual foi o primeiro acontecimento social significativo?
```

Pode ser:

- primeiro conflito;
- primeiro grupo;
- primeira morte;
- primeira conversão;
- primeiro crime;
- primeira intervenção;
- primeiro acontecimento político;
- primeiro evento excepcional.

Não precisa chamar qualquer tick trivial de “evento inicial”.

O objetivo é dar um ponto de partida narrativo à crônica.

Exemplo:

> A primeira mudança social relevante aconteceu na hora 6, quando...

---

# 105. O MUNDO ANTES DAS HISTÓRIAS

Dar um pequeno retrato factual da campanha:

- população;
- cidades/vilas;
- profissões;
- religiões;
- governantes relevantes;
- facções;
- personagens míticos se existirem;
- situação alimentar;
- violência geral;
- alguma característica incomum da seed.

Sem transformar isso em relatório estatístico longo.

A intenção é permitir que quem leia entenda:

> “que mundo era esse?”

antes dos arcos individuais.

---

# 106. HISTÓRIAS DE NPCs

Selecionar no máximo aproximadamente 8–10 trajetórias realmente interessantes.

Cada história deve acompanhar pessoas pelo nome.

Não apresentar apenas eventos soltos.

Exemplo:

```text
## Cael Luar e Bela Solaris
```

E então reconstruir cronologicamente:

- quem eram;
- profissão se conhecida;
- onde viviam;
- fé se relevante;
- relações relevantes;
- evento inicial;
- acontecimentos intermediários;
- decisões;
- deslocamentos;
- confrontos;
- consequência;
- estado ao final da campanha.

---

# 107. NÃO INVENTAR INTERIORIDADE

Pode escrever:

> Cael passou a perseguir Bela depois de...

se houver eventos que comprovem perseguição/Goal/Commitment.

Não escrever:

> Cael percebeu que sua alma estava consumida pelo ódio.

a menos que haja sistema/evento objetivo equivalente.

Preferir:

> A partir dali, os registros mostram...

ou:

> O sistema registrou `LethalDecision`...

quando necessário.

---

# 108. HISTÓRIAS PODEM SER PEQUENAS

Não priorizar só épicos.

Uma história válida pode ser:

- padeiro que mudou de fé;
- representante de vila;
- amigo que procurou outro;
- cultista que ganhou favor;
- guarda que investigou assassinato;
- grupo que protestou;
- personagem que matou e se arrependeu;
- pessoa que quase matou e desistiu;
- religião que perdeu seu núcleo;
- Deus que ignorou uma crise;
- NPC mítico que morreu sem realizar nada especial.

Vida pequena continua sendo lore.

---

# 109. HISTÓRIAS INCOMPLETAS SÃO VÁLIDAS

Se a campanha terminar no meio de uma trajetória:

dizer claramente.

Exemplo:

> Na hora 500, Darin ainda procurava X. A campanha terminou antes que ele descobrisse onde a pessoa estava.

Não criar resolução falsa.

---

# 110. RELIGIÃO COMO HISTÓRIA

Se houver mudança religiosa interessante, narrá-la como fenômeno social.

Exemplo:

> A fé em X perdeu seguidores em Karvia, mas seu núcleo ativo cresceu...

ou:

> embora centenas ainda professassem a fé, seus Actors caíram de dez para três...

ou:

> a morte de Y removeu um dos mortais mais favorecidos por X...

Se o Deus soube:

explicar como a informação chegou.

Se não soube:

dizer que a crise permaneceu objetivamente real, mas desconhecida pela divindade.

---

# 111. HISTÓRIA DE INTERVENÇÃO DIVINA

Se houver intervenção natural, contar:

1. situação anterior;
2. estado da religião;
3. o que o Deus sabia;
4. como soube;
5. relação com os mortais envolvidos;
6. intervenção;
7. testemunhas;
8. interpretação posterior;
9. consequência social/religiosa.

Não chamar cenário controlado de história.

---

# 112. HISTÓRIA DE ASSASSINATO

Se houver homicídio deliberado natural, reconstruir:

- agressões/eventos anteriores;
- conhecimento do assassino;
- `LethalConsideration`;
- `LethalDecision`;
- perseguição/confronto;
- morte;
- reação pós-morte;
- testemunhas;
- família;
- guardas;
- rumor;
- Renown;
- reação religiosa.

Apenas os componentes que realmente existirem.

---

# 113. ASSASSINO RECORRENTE

Se surgir naturalmente alguém com mortes repetidas:

não escrever simplesmente:

> “surgiu um serial killer.”

Contar como a trajetória apareceu.

Exemplo:

```text
primeira morte
↓
reação positiva
↓
DeathAffinity
↓
segunda morte
↓
rumores
↓
investigação
```

Mostrar quando a sociedade ainda não sabia quem era.

Se ganhou epíteto, apresentar quando e por quem se tornou conhecido.

---

# 114. ESTADO FINAL DO MUNDO

No fim do `HISTORIAS_REAIS.md`, escrever uma seção narrativa curta:

```text
## Quando a campanha terminou
```

Descrever:

- quantos estavam vivos;
- principais mudanças políticas;
- condição religiosa;
- conflitos não resolvidos;
- personagens importantes ainda ativos;
- decisões letais abertas;
- investigações abertas;
- grupos/facções ainda em atividade;
- deuses sob pressão;
- histórias claramente inacabadas.

Não transformar em tabela de métricas.

---

# 115. DADOS GERAIS NO HISTORIAS_REAIS.MD

O arquivo pode usar números para ajudar a contar o mundo.

Exemplos adequados:

> Ao longo das 500 horas, 23 profissões estiveram representadas.

> Três Deuses possuíam seguidores ativos.

> Quatro NPCs chegaram a uma decisão letal.

> A maior religião possuía 1.021 seguidores, mas apenas sete Actors.

Mas evitar blocos enormes como:

```text
metric_a = 342
metric_b = 812
metric_c = 54
...
```

Isso pertence ao relatório técnico.

---

# 116. TOM DO HISTORIAS_REAIS.MD

Escrever como:

> crônica factual de um mundo simulado.

Não como:

> relatório de QA.

Pode possuir títulos narrativos como:

```text
## O representante que saiu de Norlen
## A primeira morte de Cael
## O culto que começou a desaparecer
## O favorito de Nharos
```

desde que o título não invente interpretação.

---

# 117. EVIDÊNCIA

Cada história deve citar internamente os principais IDs/eventos/horas necessários para auditoria.

Mas sem destruir a leitura.

Exemplo:

> Na hora 328, Cael atacou Bela com intenção `kill` (`CharacterAttacked #349027`).

Não despejar dezenas de IDs se quatro eventos centrais bastarem.

---

# 118. AUSÊNCIAS IMPORTANTES

No final do arquivo, pode haver uma seção curta:

```text
## Coisas que não aconteceram
```

Apenas para fenômenos narrativamente relevantes.

Exemplos:

- nenhum Deus interveio;
- nenhuma execução deliberada ocorreu;
- nenhum assassino recorrente surgiu;
- nenhuma apoteose aconteceu.

Sem transformar isso em análise de falha.

A explicação técnica fica no relatório.

---

# 119. SUCESSO DA FASE

A Fase 5.2 é bem-sucedida se demonstrar que:

- matar ficou menos impossível sem virar ação aleatória;
- decisões letais têm causa;
- decisão letal persiste;
- finish/spare respondem ao novo contexto;
- mortes deliberadas podem ocorrer naturalmente;
- matar muda alguns personagens;
- alguns sentem culpa;
- outros podem desenvolver afinidade positiva com a morte;
- trajetória de assassino recorrente é possível sem classe pré-programada;
- guardas e rumores conseguem reagir;
- deuses possuem presença regional sobrenatural;
- localização divina não significa onisciência;
- DivineAffinity é diferente de Devotion;
- agir segundo o Deus importa mais que apenas adorá-lo;
- seguidores possuem importância religiosa diferente;
- FaithHealth distingue massa religiosa de núcleo ativo;
- queda simultânea de Followers/Devoted/Cultists/Actors pode acender crise;
- perda de Actors ou favoritos pode importar desproporcionalmente;
- um Deus pode proteger favorito;
- um Deus pode reagir à morte de favorito;
- fé pode ganhar/perder influência regional;
- Deus precisa conhecer a perda para reagir;
- intervenções divinas podem finalmente surgir por causa real;
- o arquivo de histórias consegue retratar o mundo, seus habitantes e acontecimentos sem virar um relatório técnico.

---

# 120. PRINCÍPIOS QUE NÃO PODEM SER QUEBRADOS

1. World truth != NPC knowledge.

2. World truth != divine knowledge.

3. Devotion != DivineAffinity.

4. Worship != Divinity.

5. Sadism != murderer.

6. DeathAffinity != guaranteed killing.

7. LethalDecision != immediate death.

8. Kill intent != damage buff.

9. Incapacitation changes context.

10. Defensive threat should fall when threat truly ends.

11. Persistent revenge may remain after threat ends.

12. Personality modifies response; it does not create cause from nothing.

13. Gods are not globally or regionally omniscient.

14. DivinePresence != automatic knowledge.

15. High DivineAffinity creates preference, not automatic miracles.

16. Serial killer is an emergent trajectory, not a class.

17. Rumor does not reveal objective killer automatically.

18. Homicide should be uncommon, not virtually nonexistent.

19. Do not calibrate toward a target death count.

20. Do not use random probability as substitute for causal action.

21. Preserve existing systems instead of rewriting them.

22. Follower count alone does not determine religious health.

23. Loss of core followers may matter more than loss of passive followers.

24. Religious decline must be known before a God can act on it.

25. HISTORIAS_REAIS.md is a chronicle of the world, not a duplicate technical report.

---

# 121. RESULTADO DESEJADO

Depois desta fase, quero que uma história POSSA emergir assim:

```text
homem pacífico é atacado repetidamente
↓
WorldPressure cresce
↓
LethalConsideration
↓
barreiras cedem
↓
LethalDecision
↓
ele procura o agressor
↓
confronto
↓
mata
↓
PostKillAppraisal
↓
culpa
↓
aproxima-se da religião
```

Outro personagem:

```text
mata
↓
sente prazer/fascinação
↓
DeathAffinity cresce
↓
repete
↓
rumores surgem
↓
guardas conectam mortes
↓
cidade sente medo
```

Outro:

```text
devoto do Deus da Morte
↓
oração gera pouco favor
↓
começa a agir segundo a doutrina
↓
mata repetidamente
↓
DivineAffinity cresce
↓
torna-se favorito
↓
é atacado e quase morto
↓
Deus considera intervir
```

Outro:

```text
favorito de Deus é assassinado
↓
DivineBond envia sinal
↓
Deus aprende a morte
↓
DivineWorldPressure cresce
↓
punição/proteção torna-se opção
↓
Deus age ou decide não agir
```

E regionalmente:

```text
Faith B cresce em região de Faith A
↓
Followers de A começam a cair
↓
Devoted também diminuem
↓
Cultists abandonam
↓
Actors desaparecem
↓
FaithHealth entra em CORE_EROSION / REGIONAL_CRISIS
↓
seguidores relatam situação
↓
God A aprende perda
↓
DivineWorldPressure cresce
↓
intervenção torna-se plausível
↓
testemunhas
↓
rumor
↓
nova mudança religiosa
```

Nenhuma dessas histórias deve existir como função roteirizada.

Os sistemas fornecem:

```text
causa
conhecimento
pressão
personalidade
fé
afinidade
capacidade
ação
consequência
```

A história surge depois.

---

# 122. FILOSOFIA FINAL

A Fase 5.1 ensinou o mundo a agir.

A Fase 5.2 deve ensinar o mundo que:

> algumas ações mudam permanentemente quem as realizou.

Matar não é apenas:

```text
CharacterKilled
```

É um evento capaz de modificar:

- o matador;
- a vítima;
- a família;
- os guardas;
- a reputação;
- a religião;
- um Deus;
- uma cidade inteira.

Da mesma forma, fé não é apenas:

```text
religion_id
devotion
```

É um ecossistema social.

Uma religião pode possuir milhares de seguidores e estar morrendo internamente.

Outra pode possuir poucas centenas de pessoas, mas dezenas de devotos, cultistas e Actors extremamente ativos.

O Deus precisa perceber essa diferença.

E religião também é uma relação de mão dupla.

O mortal pode amar um Deus que não liga para ele.

Um mortal pouco devoto pode tornar-se favorito porque vive exatamente segundo os valores da divindade.

Um assassino pode virar campeão do Deus da Morte.

Outro pode matar uma vez, se arrepender e nunca mais conseguir atravessar aquela barreira.

Um Deus pode observar sua religião desaparecer de uma região e permanecer quieto porque ainda não sabe.

Pode receber relatos algumas horas depois e começar a agir.

Pode perder um favorito e reagir violentamente.

Pode escolher não reagir.

Pode favorecer um mortal que todos os outros seguidores desprezam.

Um humano pode ser chamado de Deus sem possuir Divinity.

E algum dia um deles pode realmente matar uma divindade e ocupar seu lugar.

Não tentar fazer essas histórias acontecerem.

Fazer com que o mundo tenha condições de produzi-las.

E, ao final da campanha, não quero apenas saber:

> quantas vezes cada sistema foi chamado.

Quero conseguir abrir `HISTORIAS_REAIS.md` e descobrir:

> quem vivia naquele mundo,  
> no que trabalhavam,  
> quais Deuses adoravam,  
> quais Deuses existiam,  
> qual acontecimento colocou aquela história em movimento,  
> quem amou, odiou, matou, protegeu, protestou, mudou de fé, ganhou favor ou morreu,  
> e quais histórias ainda estavam acontecendo quando o relógio da simulação parou.