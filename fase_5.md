# FASE 5 — PODER LOCAL, ORGANIZAÇÕES, FÉ, DIVINIZAÇÃO E LENDAS EMERGENTES

## 0. CONTEXTO E PRINCÍPIO CENTRAL

Basear esta fase na versão atual `mvp-7-fase4.6`.

Esta fase NÃO é uma reescrita do motor.

Preserve os sistemas existentes sempre que possível:

- Need;
- prioridade dinâmica;
- Solution;
- Goal;
- Commitment;
- Aspiration;
- personalidade;
- emoção;
- grievance;
- Knowledge;
- rumores;
- investigação;
- relações;
- economia;
- profissões;
- migração;
- combate;
- justiça;
- reputação;
- Event Bus;
- persistência;
- geração procedural;
- sucessão básica;
- instituições já existentes.

O princípio central continua sendo:

**histórias devem emergir de pessoas, necessidades, conhecimento, crenças, relações e consequências reais.**

Não construir um `StoryManager`.

Não criar acontecimentos apenas porque seriam narrativamente interessantes.

Não criar guerras, revoluções ou grandes tragédias para “dar história” ao mundo.

A prioridade desta fase é:

> fazer indivíduos começarem a agir coletivamente, politicamente, religiosamente e miticamente através dos mesmos princípios causais que já regem suas vidas pessoais.

Uma história pequena é válida.

Uma vida comum é válida.

Um objetivo abandonado é válido.

Um grupo que desaparece depois de conseguir o que queria é válido.

Um personagem extraordinário que nunca realiza seu potencial é válido.

Grandes arcos devem surgir raramente.

---

# 1. OBJETIVOS DESTA FASE

Implementar cinco pilares que devem conversar entre si:

1. grupos sociais emergentes;
2. política local;
3. organizações e facções ativas;
4. fé, deuses reais e divinização;
5. fama, indivíduos míticos e itens históricos.

Esses sistemas NÃO devem existir isoladamente.

O objetivo é permitir circuitos como:

```text
Need individual
→ problema compartilhado
→ grupo
→ proposta
→ pressão sobre autoridade
→ decisão política
→ consequência material
→ novas Needs
```

e:

```text
evento sobrenatural real
→ testemunhas
→ interpretação
→ rumor
→ fé
→ grupo religioso
→ pressão social/política
```

e raramente:

```text
indivíduo excepcional
→ feitos
→ fama
→ epíteto
→ seguidores
→ culto
→ confronto com entidade divina
→ possível apoteose
```

---

# 2. FORA DO ESCOPO

NÃO implementar nesta fase:

- guerras entre reinos;
- diplomacia completa entre reinos;
- tratados;
- alianças internacionais;
- cerco;
- conquista territorial;
- anexação;
- ocupação militar;
- batalhas de exércitos;
- guerra civil completa;
- revolução completa;
- sistema estratégico de exército entre mapas;
- caravanas militares;
- destruição de cidades por guerra;
- nascimento/envelhecimento geracional;
- IA generativa controlando regras;
- roteiro principal;
- profecia obrigatória;
- “chosen one” automático;
- alinhamento global GOOD/EVIL;
- sistema automático de herói/vilão.

Podem surgir condições que no futuro levem a guerra, golpe ou revolução.

Não implementar ainda a resolução desses fenômenos em escala nacional.

---

# 3. POLÍTICA LOCAL: ESTRUTURA DE PODER

Adicionar política executável principalmente na escala da cidade.

Cada cidade de reino deve possuir uma autoridade política local:

```text
Mayor / Prefeito
```

O prefeito representa a cidade perante a família real e o reino.

Nesta fase, para um cidadão comum, o maior cargo político formal alcançável é prefeito.

Não implementar ainda ascensão comum direta ao trono.

O prefeito deve ser uma pessoa real existente no mundo.

Deve possuir:

- CharacterID;
- cidade representada;
- início do mandato/ocupação;
- origem da nomeação/ascensão;
- apoio conhecido;
- grupos relevantes;
- decisões tomadas;
- propostas recebidas;
- reputação política;
- relações com autoridades locais;
- relação com família real.

Não transformar prefeito em controlador absoluto da cidade.

Ele é uma autoridade que precisa lidar com pressões concorrentes.

---

# 4. RELAÇÃO ENTRE PREFEITO E FAMÍLIA REAL

A família real continua sendo autoridade superior do reino.

O prefeito:

- representa necessidades da cidade;
- recebe ou transmite decisões;
- pode buscar recursos do reino;
- pode entrar em desacordo com interesses reais;
- pode ganhar ou perder apoio;
- pode ignorar ou atender pressões locais;
- pode ter interesses próprios.

Não implementar ainda uma máquina completa de política nacional.

Nesta fase é suficiente que exista uma relação executável entre:

```text
cidade
↕
prefeito
↕
família real / autoridade central
```

A personalidade do prefeito deve influenciar suas respostas.

Não usar decisões aleatórias independentes de contexto.

---

# 5. GRUPOS POPULARES EMERGENTES

Adicionar `Group` como entidade social distinta de facção.

Um grupo popular deve surgir porque pessoas compartilham algum problema, desejo, crença, interesse ou ameaça.

Exemplos possíveis:

- falta de comida;
- salários ruins;
- insegurança;
- medo de criminosos;
- desejo por mais armamento;
- oposição a alguma decisão;
- demanda religiosa;
- defesa de culto;
- perseguição a culto rival;
- proteção de profissão;
- apoio a determinada figura;
- demanda por justiça;
- reclamação contra tributos;
- defesa de determinada política.

NÃO criar grupos aleatoriamente apenas para povoar o mundo.

O fluxo deve ser aproximadamente:

```text
Needs / crenças / interesses individuais
→ reconhecimento de problema compartilhado
→ contato social
→ percepção de afinidade
→ formação de grupo
```

---

# 6. GRUPO NÃO É FACÇÃO

Separar claramente:

## Grupo

Pode ser:

- temporário;
- informal;
- local;
- sem recursos próprios relevantes;
- criado por um problema específico;
- dissolvido após sucesso, fracasso ou perda de relevância.

## Facção

É uma organização mais persistente.

Possui:

- identidade;
- liderança;
- membros;
- sede ou área de operação;
- recursos;
- objetivos;
- hierarquia;
- continuidade;
- capacidade organizacional.

Um grupo pode eventualmente amadurecer e virar facção.

Isso deve emergir de continuidade, liderança, recursos, identidade e investimento.

Não fazer:

```text
qualquer Group
→ Faction
```

automaticamente.

---

# 7. FORMAÇÃO DE GRUPOS

A formação deve considerar:

- necessidade compartilhada;
- severidade;
- repetição;
- relações sociais;
- proximidade;
- profissão;
- crença;
- reputação;
- confiança;
- personalidade;
- liderança disponível;
- capacidade percebida;
- informação disponível.

Uma pessoa pode concordar com o problema mas não entrar no grupo.

Outra pode entrar e depois abandonar.

Outra pode radicalizar o grupo.

Outra pode tentar moderá-lo.

---

# 8. LIDERANÇA DE GRUPO

Grupos podem possuir liderança formal ou informal.

A liderança deve emergir de fatores como:

- iniciativa;
- reputação;
- reconhecimento;
- ambição;
- persistência;
- coragem;
- competência percebida;
- relações;
- capacidade de mobilização;
- confiança do grupo.

Não escolher líder apenas pelo maior atributo numérico.

Não teleportar autoridade.

A pessoa precisa estar socialmente conectada ao grupo.

---

# 9. OBJETIVOS COLETIVOS

Grupos podem possuir um objetivo coletivo derivado das necessidades de seus membros.

Exemplo:

```text
escassez alimentar
→ membros percebem privação comum
→ grupo se forma
→ objetivo: aumentar acesso a comida
```

Não transformar isso diretamente em uma ação.

Aplicar princípio semelhante ao individual:

```text
Collective Pressure
→ alternatives
→ collective objective
→ chosen strategy
→ action
→ consequence
```

Evitar criar um segundo motor completamente separado se os conceitos atuais puderem ser generalizados/reutilizados.

---

# 10. PROPOSTAS

Nesta fase, propostas políticas formais devem surgir principalmente através de grupos.

Não permitir que qualquer NPC gere propostas políticas arbitrárias sem representação coletiva.

Uma proposta deve conter pelo menos:

- grupo de origem;
- problema causal;
- objetivo;
- alvo político;
- solução proposta;
- urgência;
- apoio conhecido;
- oposição conhecida;
- data;
- status;
- resultado.

Exemplos:

- mais distribuição de comida;
- redução/aumento de determinada cobrança;
- mais investimento em segurança;
- mais armas para militares;
- proteção de determinada profissão;
- reconhecimento de culto;
- restrição de culto;
- aumento de recursos para alguma instituição;
- apoio a determinado grupo.

---

# 11. PROPOSTAS DEVEM ALTERAR O MUNDO REAL

Proposta não pode ser apenas texto.

Se aprovada, deve afetar algum sistema existente.

Exemplo:

```text
mais distribuição alimentar
→ recursos realmente saem de algum estoque/tesouro
```

```text
mais armamento
→ demanda real por armas/materiais
```

```text
mais guardas
→ necessidade real de pessoal, pagamento ou recursos
```

```text
restrição religiosa
→ comportamento institucional/social real
```

Não criar benefícios sem custo.

---

# 12. DECISÃO DO PREFEITO

O prefeito deve avaliar propostas segundo:

- personalidade;
- interesses;
- reputação;
- relações;
- recursos;
- apoio social;
- oposição;
- posição da família real;
- risco;
- necessidade da cidade;
- crenças;
- autoridade disponível.

Não usar:

```text
proposal_support > X
→ approve
```

como única lógica.

A decisão precisa competir com alternativas.

---

# 13. REAÇÃO DOS GRUPOS

Uma proposta pode ser:

- aceita;
- aceita parcialmente;
- recusada;
- adiada;
- ignorada;
- substituída;
- negociada.

O grupo deve reagir ao resultado.

Possíveis respostas:

- aceitar;
- dissolver;
- insistir;
- reorganizar;
- mudar proposta;
- aumentar pressão;
- protestar;
- procurar apoio;
- denunciar;
- ameaçar;
- abandonar;
- radicalizar.

Radicalização não deve ser automática.

---

# 14. PRIVAÇÃO, RAIVA E RADICALIZAÇÃO

Privação extrema pode gerar grupos muito mais perigosos.

Mas NÃO usar:

```text
hunger high + anger high
→ overthrow government
```

Exigir combinação causal.

Possíveis fatores:

- privação coletiva;
- duração;
- raiva;
- ressentimento;
- fracasso de alternativas;
- responsabilidade atribuída;
- baixa confiança institucional;
- percepção de injustiça;
- liderança;
- apoio;
- capacidade percebida;
- repressão;
- crenças.

A responsabilidade percebida é fundamental.

A mesma fome pode gerar interpretações distintas:

```text
"foi a seca"
```

```text
"o prefeito roubou"
```

```text
"os comerciantes esconderam comida"
```

```text
"os deuses estão nos punindo"
```

Essas interpretações devem produzir comportamentos diferentes.

---

# 15. GRUPOS DE DOMÍNIO

Em circunstâncias extremas, alguns grupos podem desenvolver objetivo de tomar controle político local.

Chamar internamente como conceito equivalente a:

```text
domination / seize_local_power
```

Não significa revolução nacional.

Pode ser:

- remover prefeito;
- controlar determinada instituição;
- impor autoridade local;
- ocupar função administrativa.

Não implementar guerra civil completa.

Esses grupos devem ser raros.

---

# 16. CONFLITO ENTRE GRUPOS

Grupos podem possuir objetivos incompatíveis.

Isso pode gerar:

- rivalidade;
- desconfiança;
- propaganda;
- boicote;
- intimidação;
- disputa por apoio;
- denúncias;
- ameaças;
- brigas;
- conspiração;
- assassinato;
- negociação;
- acordo.

NÃO transformar antagonismo em violência automaticamente.

Usar os mesmos princípios sociais já existentes.

---

# 17. GRIEVANCE ENTRE GRUPOS

Adicionar uma representação compacta de agravos coletivos quando necessária.

Não copiar toda emoção humana para organizações.

Registrar apenas o suficiente para explicar:

- por que determinado grupo considera outro uma ameaça;
- qual fato originou isso;
- severidade;
- continuidade;
- resolução ou abandono.

Evitar crescimento ilimitado de pares.

---

# 18. FACÇÕES ATIVAS

Transformar facção de estrutura majoritariamente passiva em organização executável.

Uma facção deve possuir:

- líder;
- membros;
- propósito;
- recursos;
- sede;
- hierarquia;
- regras;
- interesses;
- objetivos;
- relações;
- memória organizacional compacta.

O comportamento da facção deve ser fortemente influenciado pelo propósito de sua existência.

---

# 19. PROPÓSITO DA FACÇÃO

Exemplos:

- caçadores de recompensa;
- mercadores;
- ordem religiosa;
- proteção local;
- grupo de justiça;
- associação profissional;
- exploradores;
- criminosos;
- estudiosos;
- culto;
- organização militar privada.

Não restringir a esses exemplos.

O propósito deve alterar:

- recrutamento;
- hierarquia;
- ações plausíveis;
- necessidades coletivas;
- uso de recursos;
- reputação.

---

# 20. LIDERANÇA DE FACÇÃO

O líder deve ser personagem real.

Sua personalidade deve influenciar:

- prioridades;
- tolerância a risco;
- recrutamento;
- punição;
- expansão;
- negociação;
- relação com autoridade;
- interpretação do propósito.

A facção NÃO deve ser simplesmente a personalidade do líder.

Ela também possui:

- membros;
- história;
- interesses;
- recursos;
- normas.

Mas o líder deve exercer influência forte.

---

# 21. PATENTES DE FACÇÃO

Facções devem possuir hierarquias coerentes com seu propósito.

Os nomes podem ser definidos durante criação/fundação segundo contexto da organização.

Exemplo:

```text
Guilda de Caçadores
Novato
Caçador
Veterano
Mestre
```

Outra facção pode usar títulos totalmente diferentes.

Evitar depender de IA generativa.

Utilizar repertórios/configurações e composição procedural controlada.

---

# 22. PROMOÇÃO EM FACÇÕES

Promoção deve depender de:

- feitos relevantes;
- confiança;
- tempo;
- competência;
- lealdade;
- reputação interna;
- vagas;
- decisão de liderança;
- necessidade organizacional.

Não usar apenas XP.

---

# 23. ESTRUTURA MILITAR LOCAL

Adicionar hierarquia militar das cidades do reino:

```text
General
Captain
Lieutenant
Sergeant
Soldier
```

Regras iniciais:

- exatamente um General ativo por cidade quando estrutura militar existir;
- múltiplos capitães;
- múltiplos tenentes;
- múltiplos sargentos;
- soldados.

Cada patente deve possuir autoridade real compatível.

---

# 24. GENERAL DA CIDADE

O General é a maior autoridade militar local.

Ele não substitui o prefeito.

Prefeito:

```text
autoridade política local
```

General:

```text
autoridade militar local
```

Pode existir tensão entre os dois.

---

# 25. MILITARES COMO GRUPO SOCIAL

Soldados não são apenas unidades de combate.

Eles são NPCs.

Podem:

- possuir necessidades;
- criar relações;
- formar grupos;
- apoiar propostas;
- rejeitar propostas;
- pressionar prefeito;
- apoiar general;
- entrar em conflito interno;
- possuir religião;
- espalhar rumores;
- venerar figuras.

Isso prepara futuros golpes e guerras sem implementá-los agora.

---

# 26. PRESSÃO MILITAR

Militares podem formar grupos em torno de interesses como:

- pagamento;
- equipamento;
- comida;
- segurança;
- prestígio;
- liderança;
- religião;
- tratamento recebido.

Esses grupos podem produzir propostas.

Não permitir golpe automático nesta fase.

---

# 27. FÉ OBJETIVAMENTE REAL

A cosmologia deste mundo deve assumir:

**deuses existem objetivamente.**

Isso não é ambíguo para o motor.

Mas a percepção das pessoas continua imperfeita.

Separar:

```text
Objective Divinity
Faith
Knowledge
Worship
Interpretation
```

---

# 28. DEUS REAL ≠ SER ADORADO

Um Deus pode:

- existir e ser adorado;
- existir e ser desconhecido;
- existir e ser interpretado incorretamente.

Um mortal pode:

- ser adorado;
- ser considerado divino;
- possuir culto;
- NÃO ser um Deus real.

Não usar adoração como prova ontológica.

---

# 29. ENTIDADE DIVINA

Criar estrutura de entidade divina com pelo menos:

- ID;
- nome;
- domínio atual;
- personalidade/valores próprios;
- poder;
- seguidores conhecidos;
- áreas de influência;
- relações;
- memória divina compacta;
- intervenções;
- estado vivo/morto;
- origem;
- possíveis vínculos com objetos/locais.

Não transformar Deus em apenas NPC com HP enorme.

Pode compartilhar conceitos com Character, mas deve possuir semântica divina própria.

---

# 30. DOMÍNIO DIVINO

Cada Deus possui domínio ou conjunto limitado de conceitos associados.

Exemplos:

- amor;
- justiça;
- guerra;
- morte;
- conhecimento;
- caça;
- fome;
- tempestade;
- proteção;
- vingança.

O domínio deve afetar:

- comportamento;
- tipos de intervenção;
- valores;
- relação com seguidores;
- culto.

---

# 31. DEVOÇÃO

A devoção individual deve continuar variável.

Não assumir que todo religioso é fanático.

A devoção deve influenciar:

- prioridade religiosa;
- interpretação;
- ritual;
- disposição a obedecer doutrina;
- participação em grupo religioso;
- reação a blasfêmia;
- disposição a defender culto;
- impacto de sinais divinos.

---

# 32. FÉ COMO COMPORTAMENTO

Transformar fé de simples campo em sistema executável.

Um NPC pode:

- rezar;
- buscar templo/local sagrado;
- oferecer recurso;
- pedir intervenção;
- espalhar crença;
- defender fé;
- abandonar fé;
- mudar fé;
- formar culto;
- denunciar heresia percebida;
- reinterpretar evento.

Não implementar tudo obrigatoriamente de uma vez se algumas ações exigirem sistemas inexistentes.

Priorizar um núcleo funcional e auditável.

---

# 33. EXPANSÃO DE FÉ

Fé pode se espalhar para fora de sua região original.

Usar:

- contato;
- relações;
- migração;
- testemunho;
- reputação;
- rumor;
- intervenção percebida;
- grupos;
- líderes religiosos.

Não converter automaticamente por proximidade.

---

# 34. EVENTO SOBRENATURAL: VERDADE E INTERPRETAÇÃO

O motor deve preservar a verdade objetiva.

Exemplo:

```text
God 17 caused DivineIntervention 991
```

Personagens podem interpretar como:

```text
milagre
maldição
coincidência
ação de outro Deus
ação de um mortal
evento incompreendido
```

Não sobrescrever verdade com interpretação.

---

# 35. RUMOR ESPIRITUAL

Knowledge deve poder transmitir rumores religiosos e sobrenaturais.

Rumor não precisa ser informação operacional imediata.

Pode ser:

- relato de milagre;
- suposta aparição;
- feito extraordinário;
- bênção;
- maldição;
- profecia percebida;
- fama de indivíduo;
- reputação de objeto.

Preservar:

- fonte;
- confiança;
- idade;
- cadeia de transmissão quando relevante.

---

# 36. DEUSES PODEM INTERVIR

Adicionar intervenções divinas executáveis.

Não torná-las frequentes.

Possíveis categorias iniciais:

- bênção;
- maldição;
- sinal;
- proteção;
- aumento temporário;
- punição;
- manifestação;
- influência sobre item.

Cada intervenção deve possuir:

- causa;
- Deus;
- alvo;
- custo/regra;
- consequência;
- testemunhas;
- conhecimento produzido.

---

# 37. NÃO USAR INTERVENÇÃO COMO ROTEIRO

Deus não intervém porque “seria épico”.

Deve existir motivação.

Exemplos:

- seguidor relevante;
- afronta;
- pedido;
- ameaça;
- domínio;
- relacionamento;
- rivalidade;
- interesse.

---

# 38. RELAÇÃO ENTRE DEUSES

Pode existir relação básica entre deuses nesta fase.

Não implementar guerra divina completa.

Permitir apenas estados suficientes para:

- afinidade;
- hostilidade;
- rivalidade;
- interesse.

---

# 39. MORTE DE UM DEUS

Deuses podem morrer.

Isso deve ser extremamente raro.

Não simplificar para:

```text
HP <= 0
→ ordinary death
```

Pode utilizar combate, mas a morte divina deve produzir consequências especiais.

Registrar:

- autor;
- causa;
- testemunhas;
- local;
- domínio;
- seguidores afetados;
- essência/divindade liberada;
- repercussão.

---

# 40. APOTEOSE REAL

Um mortal pode se tornar Deus REAL caso consiga:

1. matar um Deus;
2. sobreviver;
3. possuir acesso legítimo à essência/posição divina;
4. conseguir assumir essa divindade segundo as regras implementadas.

Não fazer automaticamente:

```text
kill God
→ isGod = true
```

Deve existir uma etapa de apropriação/assunção.

---

# 41. DOMÍNIO NÃO É HERDADO AUTOMATICAMENTE

Se um mortal mata o Deus do Amor, ele não precisa virar Deus do Amor.

O novo domínio pode ser influenciado por:

- personalidade;
- MythicTrait;
- trajetória;
- crenças;
- feitos;
- aspirações;
- reputação;
- circunstância da ascensão.

Exemplo:

```text
Deus do Amor morre
↓
mortal da Justiça assume essência
↓
novo Deus do Julgamento
```

A sucessão divina deve permitir transformação religiosa real.

---

# 42. USURPAÇÃO DIVINA

Seguidores do Deus morto podem:

- aceitar;
- rejeitar;
- considerar novo Deus usurpador;
- manter culto antigo;
- migrar para outra fé;
- formar grupos;
- perseguir seguidores rivais.

Não implementar guerra religiosa nacional automaticamente.

---

# 43. DIVINIZAÇÃO SOCIAL

Separar apoteose real de divinização social.

Um mortal pode ser considerado Deus sem possuir Divinity.

Exemplo:

```text
General vence dezenas de batalhas/duelos locais
↓
soldados espalham histórias
↓
ganha epíteto
↓
alguns passam a considerá-lo divino
↓
culto pode surgir
```

Motor:

```text
actual_divinity = false
```

Sociedade:

```text
believed_divine = true para certos grupos/personagens
```

---

# 44. FAMA / RENOWN

Expandir conhecimento social para incluir:

```text
Renown
```

Renown responde:

> pelo que essa pessoa é conhecida?

Não substituir fatos individuais.

Agregar reputação derivada de feitos conhecidos.

Possíveis áreas:

- swordsmanship;
- cooking;
- hunting;
- leadership;
- justice;
- cruelty;
- generosity;
- divine association;
- survival;
- craftsmanship;
- military success.

---

# 45. FATO, FAMA E EPÍTETO

Separar:

```text
Fact
Renown
Epithet
```

Fact:

```text
Daemon derrotou NPC X em duelo.
```

Renown:

```text
Daemon é conhecido por habilidade com espada.
```

Epithet:

```text
Daemon, o Espadachim.
```

---

# 46. FAMA DEPENDE DE CONHECIMENTO

Feito desconhecido não gera fama automática.

Se alguém mata 100 inimigos sem testemunhas, sobreviventes, evidência ou propagação:

```text
Renown não cresce automaticamente.
```

O EventLog sabe.

A sociedade não necessariamente sabe.

---

# 47. ALCANCE DA FAMA

Renown deve possuir alcance.

Possíveis escalas:

- círculo pessoal;
- local;
- cidade;
- regional;
- reino;
- continental.

Não usar thresholds rígidos isolados.

Considerar:

- quantidade de pessoas que conhecem;
- alcance geográfico;
- repetição;
- importância dos feitos;
- credibilidade;
- testemunhas;
- rumores.

---

# 48. EPÍTETOS

Personagens podem receber apelidos/títulos emergentes baseados em sua fama.

Exemplos:

```text
Daemon, o Espadachim
```

```text
Arthus, o Caçador Feroz
```

```text
Iria, a Cozinheira dos Deuses
```

```text
Daemon, o Deus Espadachim
```

O epíteto deve refletir:

- pelo que é conhecido;
- intensidade;
- alcance;
- cultura;
- crença social.

---

# 49. "DEUS" EM EPÍTETO NÃO SIGNIFICA DIVINDADE

Fundamental:

```text
epithet contains "God"
≠
actual_divinity
```

Um homem chamado “Deus Espadachim” pode continuar mortal.

Isso pode inclusive contribuir para culto futuro.

---

# 50. EPÍTETO PODE VARIAR POR REGIÃO

Não exigir título global único.

Uma pessoa pode ser conhecida de formas diferentes em lugares diferentes.

Exemplo:

```text
cidade A:
Daemon, o Protetor
```

```text
cidade B:
Daemon, o Açougueiro
```

Mesma pessoa.

Diferentes histórias/conhecimento.

---

# 51. PERSONAGENS MÍTICOS RAROS

Adicionar uma característica excepcional raríssima ao nascimento de alguns personagens.

Nome estrutural sugerido:

```text
MythicTrait
```

Não confundir com personality normal.

---

# 52. EXEMPLOS DE MYTHIC TRAITS

Exemplos iniciais:

- Heroism;
- Justice;
- Coldness.

Pode haver outros futuramente.

Não transformar isso em GOOD / EVIL.

---

# 53. RARIDADE

Pouquíssimos NPCs devem possuir MythicTrait.

Não gerar dezenas de figuras especiais em cada cidade.

Esses indivíduos representam potencial histórico extraordinário.

A maioria da população deve continuar comum.

---

# 54. MYTHIC TRAIT COMO FORÇA DE PERSONALIDADE

O MythicTrait deve exercer influência muito forte sobre:

- Utility;
- Aspirations;
- Commitment;
- percepção moral;
- risco;
- busca de poder;
- escolha de aliados;
- escolha de grupos;
- resposta a eventos.

Exemplo:

```text
Justice
```

não significa:

```text
always morally correct
```

Significa:

> forte impulso para agir segundo aquilo que o personagem acredita ser justo.

---

# 55. JUSTIÇA É SUBJETIVA AO PERSONAGEM

Dois personagens com Justice podem divergir.

Um pode acreditar:

```text
todo acusado merece julgamento.
```

Outro:

```text
criminosos perigosos merecem morte.
```

Usar:

- personalidade;
- fé;
- cultura;
- conhecimento;
- experiências.

---

# 56. HEROISM

Heroism pode aumentar tendência a:

- enfrentar perigo;
- proteger;
- aceitar custo pessoal;
- buscar feitos;
- responder a ameaças.

Não significa comportamento sempre bom.

Um personagem pode buscar heroísmo por fama ou orgulho.

---

# 57. COLDNESS

Coldness pode influenciar:

- tolerância emocional;
- cálculo de risco;
- baixa hesitação;
- decisões duras;
- resistência a certas barreiras emocionais.

Não transformar automaticamente em psicopatia ou maldade.

---

# 58. PODER FÍSICO EXCEPCIONAL

MythicTrait pode fornecer potencial físico acima do humano comum.

Permitir bônus limitados e explícitos em:

- HP máximo;
- dano;
- resistência;
- crescimento;
- capacidade futura.

Mas evitar:

```text
bebê mítico
→ força absurda imediata
```

Preferir:

```text
potencial elevado
→ desenvolvimento através da vida
```

---

# 59. BUSCA POR PODER

Personagens míticos podem desenvolver Aspiration relacionada a:

```text
become_stronger
```

quando coerente com:

- MythicTrait;
- personalidade;
- experiências;
- ameaças;
- crenças;
- objetivos.

Não executar automaticamente.

---

# 60. EXEMPLO: JUSTICE

Um personagem com Justice forte pode:

```text
perceber injustiça
→ formar Commitment
→ treinar/buscar força
→ entrar em grupo
→ criar grupo
→ defender vítimas
→ confrontar instituição
```

Raramente:

```text
considerar Deus injusto
→ buscar força
→ formar aliados
→ tentar confrontá-lo
```

Nada disso deve ser roteirizado.

---

# 61. PERSONAGEM MÍTICO PODE FRACASSAR

Fundamental.

Pode:

- morrer jovem;
- nunca encontrar oportunidade;
- abandonar objetivo;
- ser desconhecido;
- escolher vida comum;
- ser derrotado;
- nunca virar lenda.

MythicTrait é potencial e influência, não destino.

---

# 62. GRANDES ARCOS DEVEM SER RAROS

Não calibrar o sistema para que todo MythicTrait vire uma saga.

Distribuição desejada conceitualmente:

```text
maioria:
vidas ordinárias
```

```text
alguns:
acontecimentos marcantes
```

```text
poucos:
trajetórias históricas
```

```text
raríssimos:
figuras míticas / divinas
```

---

# 63. ITENS HISTÓRICOS

Expandir Item.

Já existe procedência básica.

Adicionar possibilidade de histórico relevante.

Campos/conceitos possíveis:

- previous_owners;
- important_events;
- famous_kills;
- divine_contact;
- religious_association;
- creator;
- creation_location;
- creation_time;
- renown;
- epithet/title;
- believed_properties;
- actual_properties.

---

# 64. ITEM PODE SE TORNAR LENDÁRIO

Não gerar todo item lendário como lendário desde o início.

Uma espada comum pode adquirir importância por:

- dono famoso;
- matar figura importante;
- matar Deus;
- participação em evento conhecido;
- associação religiosa;
- sucessivas transmissões.

---

# 65. PROPRIEDADE REAL ≠ PROPRIEDADE ACREDITADA

Separar:

```text
actual_item_effects
```

de:

```text
beliefs_about_item
```

Uma espada pode ser considerada amaldiçoada sem ser.

Um artefato realmente divino pode ser tratado como comum.

---

# 66. RUMORES SOBRE ITENS

Knowledge/Renown deve permitir rumores como:

```text
"esta espada matou um rei"
```

```text
"esta lâmina foi tocada por Deus X"
```

A verdade objetiva continua separada.

---

# 67. POLÍTICA + RELIGIÃO

Permitir interação.

Exemplo:

```text
culto cresce
→ grupo religioso
→ proposta ao prefeito
```

ou:

```text
prefeito restringe culto
→ grievance religioso
→ grupo reage
```

ou:

```text
General é divinizado pelos soldados
→ grupo militar-religioso
→ pressão política
```

Não roteirizar esses casos.

---

# 68. FACÇÃO + RELIGIÃO

Uma facção pode possuir religião predominante ou tornar-se religiosa.

Não criar automaticamente uma facção para cada fé.

Cultos/grupos podem amadurecer em facção conforme continuidade.

---

# 69. MILITAR + RELIGIÃO

Militares podem:

- seguir Deus;
- formar culto;
- idolatrar general;
- interpretar vitórias como sinais;
- pressionar autoridade religiosa/política.

Isso deve usar comportamento social normal.

---

# 70. DEUS + POLÍTICA

Deus pode influenciar política através de:

- seguidores;
- intervenções;
- líderes;
- grupos religiosos.

Evitar:

```text
God directly sets city policy
```

a menos que exista ação causal real e autoridade suficiente.

---

# 71. FINALIZAÇÃO LETAL / EXECUTION OPPORTUNITY

Incorporar também o refinamento pendente da Fase 4.6.

A Fase 4.6 demonstrou intenção natural de matar, mas não homicídio deliberado concluído.

Não aumentar dano apenas para produzir mortes.

Adicionar conceito equivalente a:

```text
ExecutionOpportunity
```

quando:

```text
target incapacitated
AND attacker present
AND attacker capable
AND lethal intent active
```

---

# 72. DECISÃO TERMINAL

Ao surgir oportunidade de conclusão, reavaliar:

- finish;
- spare;
- capture;
- withdraw;
- help;
- outra resposta plausível.

Não executar morte automaticamente apenas porque intenção anterior era `kill`.

---

# 73. FINISH

Se:

```text
finish
```

for escolhido e realmente executado em alvo incapaz de resistir, tratar como desfecho fatal certo dentro da abstração.

Não retornar à rolagem normal de dano.

Registrar:

```text
CharacterKilled
death_context = deliberate_finish
```

ou equivalente.

---

# 74. MATAR NO CALOR DO MOMENTO

Intenção letal NÃO precisa vir apenas de compromisso longo.

Permitir letalidade situacional.

Exemplo:

```text
assalto
→ defesa
→ ameaça extrema
→ medo / raiva / personalidade / risco
→ resposta letal torna-se plausível
```

A pessoa pode matar sem possuir histórico de ódio.

Isso não torna automaticamente o personagem mau.

---

# 75. LETALIDADE CONSTRUÍDA VS SITUACIONAL

Distinguir conceitualmente:

```text
Persistent Lethal Intent
```

de:

```text
Situational Lethal Intent
```

Persistente:

- grievance;
- histórico;
- compromisso;
- perseguição.

Situacional:

- perigo imediato;
- defesa;
- emoção intensa;
- oportunidade;
- personalidade.

Ambas usam barreiras e contexto.

---

# 76. CONSEQUÊNCIA DE MATAR

Matar deve afetar a vida do autor.

Possíveis consequências:

- culpa;
- medo;
- reputação;
- investigação;
- perseguição;
- fuga;
- reação da família;
- reação religiosa;
- fama;
- epíteto;
- mudança pessoal.

Não criar trauma obrigatório.

A reação depende do personagem.

---

# 77. MEMÓRIA DE FEITOS IMPORTANTES

Eventos excepcionais devem possuir maior capacidade de persistência histórica do que fatos cotidianos.

Exemplos:

- matar prefeito;
- matar general;
- matar Deus;
- salvar cidade;
- fundar facção;
- ascender divinamente;
- causar massacre;
- derrotar figura famosa.

Não manter EventLog infinito adicional por entidade.

Usar resumos/identificadores compactos quando possível.

---

# 78. NÃO EXPLODIR SAVE

A Fase 4.6 já mostrou histórico global volumoso.

Esta fase não precisa resolver toda retenção histórica.

Mas NÃO adicionar estruturas sem limites.

Aplicar limites para:

- grupos antigos;
- agravos;
- pistas;
- rumores;
- memória organizacional;
- eventos de fama;
- histórico de item.

Preservar eventos importantes por referência compacta.

---

# 79. NECESSIDADES COLETIVAS

Não criar dezenas de Needs coletivas específicas.

Reutilizar categorias gerais quando possível.

Exemplo:

```text
resource_pressure
security
recognition
religious_interest
political_pressure
organizational_survival
```

Manter semântica limpa.

---

# 80. COMMITMENT COLETIVO

Se necessário, generalizar conceito de Commitment para organizações/grupos.

Não duplicar motor inteiro.

Um compromisso coletivo deve possuir:

- origem;
- objetivo;
- intensidade;
- progresso;
- falhas;
- investimento;
- status;
- resolução.

Mas deve continuar diferente de Need.

---

# 81. KNOWLEDGE COLETIVO

Organização não deve saber tudo que seus membros sabem.

Criar conhecimento institucional somente quando houver mecanismo de transmissão.

Exemplos:

- reunião;
- relatório;
- testemunho;
- líder informado;
- canal institucional.

Sem telepatia organizacional.

---

# 82. REPRESENTAÇÃO

Um prefeito não deve automaticamente conhecer todas as necessidades da cidade.

Grupos, informantes, instituições e eventos precisam transmitir problemas.

Isso mantém informação imperfeita na política.

---

# 83. FACÇÃO NÃO É MENTE COLETIVA

A facção age através de pessoas, liderança e estrutura.

Evitar:

```text
Faction thinks X
```

sem fonte.

Pode existir estado organizacional agregado, mas precisa derivar de seus agentes.

---

# 84. PERSONALIDADE DO LÍDER

Liderança importa muito.

Mas não apagar divergências internas.

Um líder extremamente agressivo pode tentar conduzir facção para confronto.

Membros podem:

- apoiar;
- resistir;
- abandonar;
- conspirar;
- criar subgrupo.

Não implementar golpe interno completo se extrapolar escopo.

---

# 85. NOMES DE GRUPOS E FACÇÕES

Nomes devem refletir:

- origem;
- profissão;
- lugar;
- causa;
- figura fundadora;
- religião;
- objetivo.

Não exigir LLM.

Gerar proceduralmente por regras controladas.

---

# 86. NOMES DE PATENTES

Facções podem receber repertório de patentes coerente com seu tipo.

O líder/fundador pode influenciar escolha do repertório.

Registrar a hierarquia explicitamente.

---

# 87. GOVERNANÇA SEM ELEIÇÃO COMPLEXA

Não é necessário implementar sistema eleitoral completo nesta fase.

O prefeito pode chegar ao cargo através de mecanismo inicial simplificado, desde que:

- seja pessoa real;
- exista causa;
- exista registro;
- possa ser substituído;
- suporte futura expansão.

Evitar fixar arquitetura que impeça eleições futuras.

---

# 88. SUBSTITUIÇÃO DO PREFEITO

Prefeito pode deixar cargo por:

- morte;
- perda de autoridade;
- decisão superior;
- crise;
- substituição.

Não implementar golpes/revolução completos.

Garantir continuidade institucional mínima.

---

# 89. RELAÇÃO PREFEITO–GENERAL

Manter separação institucional.

Registrar relação.

Ela pode afetar:

- apoio;
- confiança;
- propostas;
- segurança;
- resposta a grupos.

Não implementar conflito militar automaticamente.

---

# 90. RELAÇÃO PREFEITO–FACÇÕES

Prefeito pode:

- reconhecer;
- ignorar;
- negociar;
- rejeitar;
- tentar restringir.

Facção reage segundo seus interesses.

---

# 91. REPUTAÇÃO INSTITUCIONAL

Expandir reputação de forma limitada para permitir opinião sobre:

- prefeito;
- general;
- facção;
- grupo;
- culto.

Não criar matriz completa de todos contra todos sem limites.

---

# 92. AUDITORIA: POLÍTICA

Registrar métricas como:

- grupos formados;
- grupos dissolvidos;
- grupos convertidos em facção;
- propostas criadas;
- propostas aceitas;
- parcialmente aceitas;
- recusadas;
- abandonadas;
- pressão aumentada;
- grupos antagonistas;
- conflitos entre grupos;
- mudanças materiais causadas por proposta.

---

# 93. AUDITORIA: FACÇÕES

Registrar:

- facções ativas;
- novos membros;
- promoções;
- deserções;
- recursos;
- objetivos;
- ações organizacionais;
- liderança;
- mudanças de propósito, se houver.

---

# 94. AUDITORIA: MILITARES

Registrar:

- distribuição por patente;
- substituições;
- grupos militares;
- propostas militares;
- tensões com autoridade civil;
- ações realizadas por cadeia de comando.

---

# 95. AUDITORIA: RELIGIÃO

Registrar:

- seguidores por fé;
- conversões;
- abandono;
- grupos religiosos;
- cultos;
- propagação entre localidades;
- intervenções;
- rumores espirituais;
- divergências de interpretação.

---

# 96. AUDITORIA: DIVINIZAÇÃO

Registrar separadamente:

```text
believed_divine
actual_divine
```

Medir:

- mortais divinizados socialmente;
- cultos de mortais;
- deuses reais desconhecidos;
- deuses reais conhecidos;
- morte divina;
- tentativa de apoteose;
- apoteose bem-sucedida.

Não exigir que alguma apoteose aconteça naturalmente em uma única seed.

---

# 97. AUDITORIA: MYTHIC TRAITS

Registrar:

- quantidade total;
- distribuição;
- sobrevivência;
- aspirations;
- Commitments;
- busca de poder;
- grupos fundados;
- feitos importantes;
- fama;
- morte.

Não considerar ausência de grande feito como bug.

---

# 98. AUDITORIA: FAMA

Registrar:

- criação de Renown;
- alcance;
- mudança de alcance;
- epítetos;
- variação regional;
- fama sem conhecimento real;
- cultos derivados de fama.

---

# 99. AUDITORIA: ITENS

Registrar:

- itens que ganharam eventos históricos;
- itens conhecidos regionalmente;
- itens associados a figuras importantes;
- itens ligados a Deus;
- diferença entre propriedade real e rumor.

---

# 100. HISTÓRIAS REAIS

Gerar novamente:

```text
reports/fase_5/HISTORIAS_REAIS.md
```

Sem inventar pensamentos.

Selecionar exemplos reais, se existirem, de:

1. grupo formado por privação;
2. grupo que conseguiu proposta e se dissolveu;
3. proposta recusada que aumentou tensão;
4. grupos antagonistas;
5. grupo que amadureceu em facção;
6. prefeito reagindo a pressões diferentes;
7. general/militares pressionando autoridade;
8. promoção em facção;
9. fé atravessando região;
10. rumor espiritual;
11. intervenção divina conhecida de formas diferentes;
12. mortal divinizado socialmente sem ser Deus;
13. personagem ganhando epíteto;
14. epítetos diferentes em regiões distintas;
15. MythicTrait produzindo trajetória;
16. MythicTrait sem grande arco;
17. item ganhando importância histórica;
18. intenção letal situacional;
19. execução deliberada;
20. misericórdia após oportunidade de execução;
21. morte alterando vida do autor;
22. caso político/religioso inacabado no fim da campanha.

Se determinada categoria não ocorrer naturalmente:

**dizer explicitamente que não ocorreu.**

Não criar exemplo artificial.

---

# 101. EVITAR FALSA PROFUNDIDADE

Não considerar:

```text
100 ações repetidas
```

uma grande história.

Preferir transformações:

- mudança de objetivo;
- mudança de relação;
- mudança institucional;
- mudança de crença;
- mudança geográfica;
- mudança de reputação;
- mudança de cargo;
- criação/dissolução de grupo;
- consequência material;
- descoberta importante;
- intervenção;
- morte;
- ascensão.

---

# 102. TESTES

Criar aproximadamente 20–30 regressões direcionadas cobrindo pelo menos:

- formação de grupo;
- grupo sem formação quando afinidade insuficiente;
- proposta;
- reação do prefeito;
- efeito material;
- oposição entre grupos;
- conversão de grupo em facção;
- patente militar;
- promoção de facção;
- Knowledge institucional não onisciente;
- Deus real separado de fé;
- mortal adorado sem Divinity;
- rumor espiritual;
- intervenção;
- Renown;
- epíteto;
- alcance regional;
- MythicTrait;
- busca de poder;
- morte divina controlada;
- apoteose controlada;
- ExecutionOpportunity;
- finish;
- spare;
- letalidade situacional.

Preservar testes anteriores.

---

# 103. VALIDAÇÃO CONTROLADA

Antes da campanha longa, utilizar microcenários para comportamentos raros:

- mortal divinizado;
- Deus morto;
- apoteose;
- execução;
- misericórdia;
- grupo radical;
- oposição política;
- item tornando-se famoso.

Esses cenários comprovam capacidade técnica.

NÃO usar esses resultados como frequência natural.

---

# 104. CAMPANHA CURTA

Rodar aproximadamente:

```text
500 h
```

para verificar:

- integridade;
- explosão de entidades;
- crescimento de save;
- loops;
- grupos excessivos;
- política excessivamente ativa;
- religiões convertendo todos;
- MythicTraits dominando população;
- intervenção divina excessiva.

Corrigir apenas bugs/erros conceituais claros.

---

# 105. CAMPANHA LONGA

Depois executar:

```text
uma única campanha nova de 5000 horas
```

Não executar 10k/50k nesta fase.

5000 horas são suficientes para auditoria atual.

Registrar seed e versão.

---

# 106. NÃO OTIMIZAR PARA RESULTADOS ÉPICOS

Não definir metas como:

```text
precisamos de 3 deuses mortos
precisamos de 10 revoltas
precisamos de 20 personagens lendários
```

O objetivo é verificar se os mecanismos existem e interagem.

Zero mortes divinas pode ser resultado válido.

Zero apoteoses pode ser válido.

Poucos personagens míticos com grandes feitos é desejável.

---

# 107. CRITÉRIO DE SUCESSO

A fase é bem-sucedida se demonstrar que:

- necessidades individuais podem produzir organização coletiva;
- grupos conseguem produzir propostas;
- autoridades respondem segundo contexto;
- decisões políticas alteram sistemas reais;
- grupos podem entrar em conflito sem violência obrigatória;
- facções agem através de estrutura real;
- militares possuem hierarquia e interesses;
- fé produz comportamento;
- deuses existem objetivamente;
- crença continua subjetiva;
- rumor espiritual funciona;
- mortais podem ser divinizados socialmente;
- fama nasce de conhecimento real;
- epítetos refletem fama;
- indivíduos excepcionais influenciam suas próprias vidas sem roteiro;
- itens acumulam história;
- política, religião e indivíduos conseguem afetar uns aos outros;
- grandes histórias permanecem raras.

---

# 108. PRINCÍPIOS QUE NÃO PODEM SER QUEBRADOS

1. Need não é Action.

2. Conhecimento não é verdade objetiva.

3. Informação nova não executa ação automaticamente.

4. Grupo não é mente coletiva onisciente.

5. Facção não é apenas o líder.

6. Fé não prova divindade.

7. Adoração não cria automaticamente um Deus real.

8. Epíteto não prova habilidade real.

9. Feito desconhecido não gera fama social.

10. MythicTrait não garante destino.

11. Justiça não significa moralidade objetiva.

12. Poder não obriga heroísmo ou maldade.

13. Privação não gera revolta automaticamente.

14. Antagonismo não gera violência automaticamente.

15. `kill intent` não mata automaticamente.

16. `finish` só é fatal quando existe oportunidade terminal válida e a decisão foi tomada.

17. Deus morto não transfere automaticamente seu antigo domínio.

18. Política deve alterar estado real do mundo.

19. Grandes acontecimentos devem ser consequência, não objetivo da simulação.

20. Não maximizar quantidade de histórias.

Maximizar:

**coerência causal.**

---

# 109. RESULTADO ESPERADO

Ao final da Fase 5, quero que o mundo possa produzir naturalmente situações como:

```text
escassez
→ trabalhadores se organizam
→ exigem distribuição
→ prefeito recusa
→ militares recebem prioridade
→ ressentimento cresce
→ grupo se radicaliza
```

ou:

```text
general vence repetidamente
→ soldados contam feitos
→ fama cresce
→ recebe epíteto
→ parte dos soldados passa a tratá-lo como divino
→ culto informal surge
→ prefeito/religião local precisa reagir
```

ou:

```text
Deus intervém
→ poucas pessoas testemunham
→ versões diferentes circulam
→ fé se espalha
→ grupo religioso aparece
```

ou, extremamente raramente:

```text
mortal excepcional
→ trajetória de poder
→ conflito com Deus
→ vence
→ reivindica essência divina
→ torna-se Deus real
→ antigo culto precisa decidir como reagir
```

Nenhuma dessas sequências deve existir como script.

O motor fornece pessoas, conhecimento, necessidades, crenças, poder, organizações e consequências.

A história deve aparecer depois.

---

# 110. ENTREGA FINAL

Entregar:

- código;
- testes;
- relatório técnico;
- métricas;
- preservação das fases anteriores;
- `HISTORIAS_REAIS.md`;
- lista explícita de comportamentos não observados naturalmente;
- bugs/limitações;
- análise de custo de save/memória;
- separação entre capacidade comprovada em teste e emergência observada na campanha.

Não esconder regressões.

Não preencher lacunas com histórias inventadas.

Não chamar um comportamento de emergente se ele apareceu apenas em teste controlado.

Se algo não acontecer em 5000 horas:

**registrar isso como evidência.**

O objetivo desta fase não é provar que o mundo é épico.

O objetivo é provar que ele agora consegue formar:

**sociedade, poder, fé, mito e figuras históricas através de causalidade.**