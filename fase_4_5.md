# FASE 4.5 — IMPULSO SOCIAL, AMBIÇÃO E CONSEQUÊNCIA

Base atual: `mvp-5-fase4.1`.

Esta fase deve partir do estado atual do projeto e preservar, tanto quanto tecnicamente possível, tudo que já foi implementado e validado.

O objetivo NÃO é reconstruir:

- Need System;
- personalidade;
- emoções;
- combate;
- fome/sede;
- recuperação;
- conhecimento;
- relações;
- reputação;
- crime;
- guardas;
- perseguição;
- migração;
- família;
- luto;
- vingança;
- população;
- LOD;
- profissões;
- economia;
- sucessão;
- persistência.

Esses sistemas já existem.

A Fase 4.5 deve atuar principalmente como uma camada de **continuidade de intenção, impulso e agência**, conectando melhor sistemas que hoje já existem.

Alterações estruturais em sistemas anteriores só devem acontecer quando for demonstrado que a arquitetura atual impossibilita o comportamento necessário.

Nesse caso:

1. documentar a limitação;
2. fazer a menor alteração arquitetural possível;
3. preservar interfaces e semânticas existentes;
4. criar regressão direcionada;
5. explicar no relatório por que a alteração foi necessária.

---

# 1. VISÃO DA FASE

O problema principal agora não é ausência de sistemas.

O mundo já possui:

- fome;
- pobreza;
- raiva;
- ressentimento;
- humilhação;
- desespero;
- luto;
- vingança;
- crime;
- proteção;
- combate;
- perseguição;
- fuga;
- migração;
- reputação;
- relações familiares;
- conhecimento limitado.

Mesmo assim, muitos personagens ainda se comportam de forma excessivamente passiva ou episódica.

A simulação frequentemente produz:

evento  
→ reação imediata  
→ algumas ações  
→ retorno à rotina.

Queremos permitir:

evento  
→ interpretação pessoal  
→ pressão emocional  
→ necessidade  
→ impulso  
→ compromisso  
→ sequência de ações  
→ reação de outras pessoas  
→ mudança de situação  
→ nova avaliação  
→ continuação, transformação ou abandono do objetivo.

A mudança fundamental é:

**NPCs devem ser capazes de tomar as rédeas da própria situação.**

---

# 2. NÃO SCRIPTAR HISTÓRIAS

Não implementar cadeias específicas.

Não criar regras equivalentes a:

`fome -> roubar`

`assassinato -> familiar perseguir assassino`

`raiva alta -> atacar`

`vingança -> matar`

`ambição alta -> procurar cargo`

`pobreza -> migrar`

Esses comportamentos devem emergir do sistema geral.

A Fase 4.5 deve criar mecanismos abstratos que tornem essas trajetórias POSSÍVEIS.

O motor continua sendo:

State  
→ Perception  
→ Knowledge  
→ Need  
→ Priority  
→ Solutions  
→ Goal  
→ Action  
→ Consequence  
→ Event  
→ New State.

A nova camada deve complementar esse fluxo.

Não substituí-lo.

---

# 3. PROBLEMA CENTRAL: PRIORIDADE NÃO É COMPROMISSO

O sistema atual possui prioridade.

Prioridade responde:

**“O que é mais importante para mim agora?”**

Isso não é suficiente para histórias longas.

Uma pessoa também precisa poder responder:

**“Com o que eu estou comprometido?”**

Um objetivo importante não deve desaparecer simplesmente porque outra necessidade venceu durante algumas horas.

É necessário separar:

- prioridade imediata;
- intenção persistente.

---

# 4. INTRODUZIR O CONCEITO DE COMMITMENT

Criar uma estrutura conceitual equivalente a:

`Commitment`

Ela NÃO é uma segunda Need.

Ela registra que um personagem adotou determinado objetivo como algo que pretende continuar perseguindo ao longo do tempo.

Campos conceituais:

- owner;
- originating_need;
- originating_fact/event;
- target, quando existir;
- motivation;
- intensity;
- created_at;
- last_progress_at;
- last_attempt_at;
- progress;
- setbacks;
- failures;
- investment;
- current_status;
- abandonment_pressure;
- resolution_condition.

Pode haver outros campos necessários.

Evitar excesso.

---

# 5. COMMITMENT NÃO GARANTE EXECUÇÃO CONTÍNUA

Um Commitment não significa:

“o NPC fará isso até morrer.”

Ele pode:

- pausar;
- perder prioridade;
- ser abandonado;
- ser satisfeito;
- ser transformado;
- tornar-se impossível;
- perder importância;
- ser substituído.

Mas ele preserva intenção.

Um personagem pode:

trabalhar  
→ comer  
→ dormir  
→ resolver outra emergência

e depois retornar a um objetivo importante.

---

# 6. NECESSIDADES CONTINUAM CONTROLANDO A AÇÃO

Não permitir que Commitment ignore o Need System.

O fluxo pode ser conceitualmente:

Need ativa  
→ solução importante escolhida  
→ Commitment criado/reforçado  
→ outras necessidades interrompem temporariamente  
→ quando houver espaço, o Commitment volta a oferecer Goals relacionados.

Não criar:

`commitment.execute()`.

Ele deve influenciar a geração/prioridade de Goals através do sistema atual.

---

# 7. PRESERVAR A CAUSA

Commitment precisa manter referência à sua origem.

Não apenas:

`revenge_target = X`.

Mas:

- o que ocorreu;
- o que o NPC sabe;
- confiança;
- quem ele acredita ser responsável;
- por que ainda se importa.

Isso é importante para auditoria e para evitar ações sem causa.

---

# 8. FATOS IMPORTANTES NÃO PODEM SUMIR POR MEMÓRIA CURTA

Se um Commitment ativo depende de um fato importante:

a referência causal necessária deve permanecer disponível enquanto o Commitment for válido.

Isso NÃO significa transformar toda memória em memória eterna.

E NÃO significa reaprender um fato antigo como novo choque emocional.

Separar:

- lembrar da causa;
- receber novamente a notícia.

Relembrar não deve duplicar raiva, grievance ou choque automaticamente.

---

# 9. IMPULSO

Adicionar uma medida conceitual de **Impulse**.

Impulse NÃO é personalidade.

Impulse NÃO é emoção.

Impulse NÃO é Need.

Ele representa:

**quão disposto o personagem está a sair da rotina e agir de maneira significativa para alterar a situação atual.**

Deve ser calculado dinamicamente.

---

# 10. COMPONENTES DO IMPULSO

Conceitualmente:

`Impulse =`

- urgência da Need;
- duração do problema;
- repetição de fracassos;
- frustração;
- pressão emocional;
- personalidade compatível;
- Commitment;
- importância da relação;
- gravidade percebida;
- oportunidade;
- perceived agency;

menos:

- medo;
- risco;
- incapacidade;
- custo;
- obrigações concorrentes;
- distância;
- incerteza;
- consequências percebidas.

Não precisa usar literalmente uma única fórmula.

Mas essas dimensões precisam participar.

---

# 11. IMPULSO NÃO CRIA AÇÃO

Impulse modifica:

- prioridade;
- tolerância a risco;
- soluções consideradas;
- persistência;
- vontade de interromper rotina.

Ele não executa ação diretamente.

Continuar respeitando:

Need  
→ Solutions  
→ Utility  
→ Goal.

---

# 12. PERCEIVED AGENCY

Adicionar explicitamente o conceito:

`perceived_agency`

Ele representa:

**“Eu acredito que consigo fazer alguma coisa sobre isso?”**

Isso é essencial.

Raiva sem agência pode produzir:

- resignação;
- isolamento;
- desespero;
- espera;
- pedido de ajuda.

Raiva com agência percebida pode produzir ação.

---

# 13. COMO CALCULAR PERCEIVED AGENCY

Basear em informações do próprio personagem:

- alternativas conhecidas;
- recursos;
- dinheiro;
- armas;
- força percebida;
- saúde;
- aliados;
- contatos;
- profissão;
- localização;
- experiências anteriores;
- sucesso ou fracasso passado;
- distância;
- conhecimento de rotas;
- presença de autoridade;
- risco percebido.

Nunca consultar possibilidades desconhecidas do personagem.

---

# 14. FRUSTRAÇÃO ACUMULADA

Necessidades repetidamente não resolvidas precisam deixar histórico.

Criar/reaproveitar conceito equivalente a:

`UnresolvedPressure`

ou armazenamento dentro da própria Need/Commitment.

Registrar:

- tempo sem resolução;
- tentativas;
- falhas;
- bloqueios;
- soluções esgotadas;
- ajuda negada;
- oportunidades perdidas.

---

# 15. FRUSTRAÇÃO ALTERA O ESPAÇO DE SOLUÇÕES

Uma necessidade não resolvida repetidamente pode fazer o personagem considerar soluções:

- mais caras;
- mais arriscadas;
- moralmente menos compatíveis;
- socialmente mais agressivas;
- geograficamente mais distantes.

Não adicionar solução automaticamente.

A Utility apenas deixa de tratar determinadas soluções como absurdamente improváveis quando a pressão aumenta.

---

# 16. PERSONALIDADE CONTINUA IMPORTANDO

Personagens diferentes devem responder de forma diferente à mesma pressão.

Traços existentes continuam sendo usados.

Não adicionar dezenas de novos traits.

A Fase 4.5 deve extrair mais comportamento dos onze atuais.

Especialmente:

- courage;
- independence;
- greed;
- diligence;
- family_loyalty;
- persistence;
- temperament;
- vengefulness;
- ambition;
- compassion;
- honesty.

---

# 17. NECESSIDADES EXTREMAS DEVEM PRODUZIR SOLUÇÕES EXTREMAS

Atualmente uma Need vital pode continuar produzindo respostas relativamente conservadoras até o personagem morrer.

A Fase 4.5 deve permitir mudança gradual do envelope de soluções conforme:

- urgência;
- risco de morte;
- fracasso repetido;
- desespero;
- personalidade;
- agência percebida.

Não criar uma lista rígida de estágios.

A ideia é:

**quanto maior a ameaça existencial e quanto menos soluções normais funcionam, maior pode ser a tolerância do personagem a opções que normalmente rejeitaria.**

---

# 18. FOME COMO PRESSÃO SOCIAL, NÃO APENAS FISIOLÓGICA

Preservar integralmente a Fase 4.1.

Não voltar a rebalancear fome sem diagnóstico concreto.

O objetivo agora é permitir que privação persistente gere consequências comportamentais mais fortes.

A fome pode contribuir para:

- desespero;
- frustração;
- raiva;
- humilhação;
- grievance quando existe alvo causal conhecido;
- maior tolerância a risco.

Mas:

fome NÃO cria culpado automaticamente.

---

# 19. SOBREVIVÊNCIA EXTREMA

Quando risco de morte é real e soluções convencionais falharam:

o personagem deve reavaliar opções com tolerância diferente.

Não obrigar crime.

Não obrigar violência.

Não obrigar migração.

Mas evitar situações em que um NPC morre passivamente enquanto possuía soluções conhecidas que seriam plausíveis para aquela personalidade em estado extremo.

---

# 20. DESISTIR TAMBÉM É UMA DECISÃO

A simulação não deve assumir que todo personagem luta até o fim.

Dependendo de:

- personalidade;
- desespero;
- relações;
- percepção de agência;
- perdas;
- apoio;

o personagem pode:

- resignar-se;
- fugir;
- pedir ajuda;
- abandonar objetivo;
- isolar-se;
- assumir comportamento extremamente arriscado.

Resultados autodestrutivos fatais, quando já suportados pelo sistema, devem continuar raros, abstratos e sem representação de método.

Não tornar isso uma solução frequente.

---

# 21. LUTO PRECISA PODER MUDAR TRAJETÓRIAS

Luto não deve ser somente:

estado emocional  
→ conforto  
→ decaimento.

Dependendo de:

- relação;
- personalidade;
- causa conhecida;
- apoio;
- grievance;
- intensidade;
- compromisso;

luto pode alterar:

- rotina;
- objetivos;
- tolerância a risco;
- relações;
- migração;
- busca;
- proteção;
- vingança;
- isolamento.

---

# 22. LUTO NÃO É VINGANÇA

Não fundir.

Um personagem pode:

- sofrer sem procurar culpado;
- investigar;
- fugir;
- proteger outros;
- buscar companhia;
- abandonar responsabilidades;
- buscar vingança.

A resposta depende da pessoa.

---

# 23. VINGANÇA PRECISA SER UM OBJETIVO REAL DE LONGO PRAZO

A Need `revenge` já existe.

Não recriar.

O problema é continuidade.

Quando um personagem adota vingança como objetivo importante:

pode gerar um Commitment.

Esse Commitment deve conseguir sobreviver a:

- fome normal;
- sono;
- trabalho;
- distância;
- perda temporária do alvo.

Sem necessariamente permanecer prioridade número um.

---

# 24. VINGANÇA PRECISA DE PROGRESSO

Uma vingança distante não pode repetir:

`pursue`
→ falha
→ `pursue`
→ falha

por centenas de horas.

O Commitment precisa reconhecer:

- informação nova;
- posição provável;
- perda da pista;
- deslocamento;
- aproximação;
- encontro;
- fracasso;
- impossibilidade;
- resolução.

Uma ação que não altera informação nem posição repetidamente deve perder utilidade.

---

# 25. ALVO DESCONHECIDO

Se autoria de uma morte não é conhecida:

vingança direcionada não pode existir contra o verdadeiro culpado.

Pode existir:

- grief;
- investigação;
- busca de informação;
- suspeita.

Commitment pode inicialmente ter:

`target = unknown`.

Posteriormente pode mudar se informação confiável surgir.

---

# 26. CICLOS DE ÓDIO DEVEM EMERGIR

Não criar:

`RevengeCycle`.

Não criar:

`family_feud = true`.

O ciclo surge naturalmente.

Violência produz:

Event  
→ conhecimento  
→ relações afetadas  
→ grief/grievance  
→ Need  
→ Commitment  
→ resposta.

Se essa resposta causa nova violência:

o mesmo sistema roda novamente para outras pessoas.

---

# 27. CICLO DE ÓDIO PRECISA PODER TERMINAR

Possíveis motivos sistêmicos:

- desconhecimento;
- medo;
- perdão;
- morte;
- distância;
- abandono;
- falta de agência;
- reconciliação;
- captura;
- mudança de prioridades;
- passagem do tempo.

Não fazer vendetta infinita por definição.

---

# 28. VIOLÊNCIA PRECISA TER INTENÇÃO

O sistema atual possui `attack`.

Porém `attack` pode representar motivações muito diferentes.

Adicionar ao contexto do confronto um conceito de:

`violence_intent`

ou equivalente.

Não precisa necessariamente criar novas Actions.

---

# 29. INTENÇÕES DE VIOLÊNCIA

Usar categorias abstratas suficientes para distinguir:

- afastar;
- conter;
- subjugar;
- ferir;
- matar.

Nomes exatos ficam a critério da implementação.

Não criar dezenas de níveis.

---

# 30. INTENÇÃO LETAL NÃO É DANO MAIOR

Não fazer:

`lethal = damage * 2`.

A intenção representa:

**qual resultado o personagem está tentando obter.**

O dano continua usando o sistema físico existente.

---

# 31. INTENÇÃO LETAL DEVE SER RARA MAS REAL

Ela pode ganhar Utility quando existe combinação relevante de:

- Need grave;
- grievance grave;
- vingatividade;
- raiva;
- baixa compaixão;
- histórico de violência;
- ameaça;
- risco percebido;
- importância do alvo;
- Commitment;
- contexto.

Não usar threshold único.

Não usar:

`anger > X -> lethal`.

---

# 32. INCAPACIDADE E INTENÇÃO

Hoje incapacidade encerra confrontos e ajuda a evitar massacres.

Preservar esse comportamento para conflitos comuns.

Porém, quando o personagem possuía intenção letal real:

a incapacidade do alvo deve causar uma **nova decisão moral/estratégica**, e não necessariamente encerrar tudo automaticamente.

O personagem pode:

- parar;
- poupar;
- abandonar;
- capturar;
- pedir ajuda;
- completar a intenção letal.

A nova decisão continua dependendo de Utility, personalidade, risco, testemunhas e contexto.

---

# 33. NÃO AUMENTAR MORTES SIMPLESMENTE AUMENTANDO DANO

Não rebalancear armas ou dano com objetivo de gerar mais mortes.

Primeiro corrigir:

- intenção;
- persistência;
- escalada;
- continuidade.

Queremos mais mortes que façam sentido.

Não maior DPS.

---

# 34. AGRESSÃO DEVE MUDAR O CONFLITO

Evitar ping-pong prolongado de ataques.

Após acontecimentos importantes:

- ferimento severo;
- rendição;
- incapacidade;
- entrada de terceiro;
- chegada de guarda;
- fuga;
- morte;
- mudança de força;

reavaliar o objetivo.

Não preservar automaticamente o mesmo Goal antigo.

---

# 35. ESCALADA

Conflitos devem conseguir aumentar ou diminuir de gravidade.

A escalada deve depender da história do conflito.

Guardar/reaproveitar informações como:

- gravidade inicial;
- agressões sofridas;
- tentativas de acordo;
- restituição;
- humilhação;
- ferimentos;
- mortes;
- terceiros;
- risco.

Não criar uma ladder roteirizada.

---

# 36. DESESCALADA CONTINUA IMPORTANTE

A Fase 4 já implementou:

- fuga;
- rendição;
- desculpas;
- restituição;
- retirada;
- perdão;
- captura.

Preservar.

A 4.5 não deve transformar o mundo em massacre constante.

---

# 37. CONSEQUÊNCIAS IRREVERSÍVEIS

O mundo precisa produzir com maior frequência decisões que realmente mudem trajetórias.

Não necessariamente morte.

Consequência forte pode alterar:

- localização;
- profissão;
- dinheiro;
- posse;
- relação;
- reputação;
- ferimento;
- liberdade;
- residência;
- objetivo;
- confiança;
- segurança.

O importante é:

uma história deve conseguir modificar o futuro do personagem.

---

# 38. GUARDAS PRECISAM TER AGÊNCIA INSTITUCIONAL

Atualmente guardas podem possuir conhecimento individual de crimes.

Isso deve continuar.

Não criar onisciência.

Porém, quando um delito grave é formalmente conhecido pela autoridade local:

ele deve poder se tornar conhecimento institucional local.

---

# 39. CONHECIMENTO INSTITUCIONAL

Criar/reutilizar um registro local compartilhável de caso.

Ele contém somente informações que realmente chegaram à instituição.

Pode armazenar:

- crime;
- suspeito conhecido ou desconhecido;
- evidência;
- gravidade;
- última localização conhecida;
- estado;
- origem.

Guardas locais podem aprender esse registro por canais institucionais.

---

# 40. NÃO TELEPATIA ENTRE GUARDAS

Um guarda não sabe instantaneamente tudo que outro descobriu.

Precisa existir mecanismo de:

- registro;
- encontro;
- comunicação;
- turno de serviço;
- compartilhamento local.

Pode ser abstraído dentro da instituição desde que tenha custo/latência coerentes.

---

# 41. GRAVIDADE DO CRIME

O sistema precisa distinguir socialmente gravidade.

Não necessariamente criar novo sistema legal completo.

Mas respostas institucionais não devem tratar da mesma forma:

- conflito menor;
- roubo;
- agressão;
- homicídio;
- violência contra autoridade;
- reincidência grave.

A gravidade altera:

- prioridade;
- duração;
- quantidade de guardas envolvidos;
- persistência;
- disposição ao risco.

---

# 42. MAIS DE UM GUARDA PODE RESPONDER

Casos graves podem gerar Commitments institucionais em múltiplos guardas.

Evitar:

1 crime  
→ 50 Goals duplicados.

O caso é único.

Cada guarda pode assumir uma tarefa derivada do caso.

---

# 43. COORDENAÇÃO MÍNIMA

Não criar sistema policial complexo.

O necessário é impedir que todos façam exatamente a mesma coisa.

A instituição pode distribuir implicitamente ações como:

- procurar;
- vigiar;
- obter informação;
- responder quando alvo é encontrado.

Tudo ainda ocorre através de NPCs reais.

---

# 44. GUARDA NÃO É ASSASSINO AUTOMÁTICO

Profissão de guarda aumenta:

- responsabilidade;
- resposta a crime grave;
- persistência institucional;
- disposição a intervir.

Não significa:

`guard -> attack`.

Captura continua preferível quando plausível.

Violência depende de resistência, risco e contexto.

---

# 45. MATAR ALGUÉM PRECISA MUDAR A VIDA DO AUTOR

Quando autoria é conhecida e crime grave é reconhecido:

o autor deve poder sofrer consequências reais.

Pode gerar:

- wanted;
- perseguição;
- perda de segurança;
- mudança de rotina;
- fuga;
- migração;
- isolamento;
- novas relações hostis.

Não criar todas obrigatoriamente.

Mas matar alguém e continuar rotina normal apesar de autoridade informada deve ser raro quando existe capacidade institucional de resposta.

---

# 46. FUGA PRECISA SER UMA RESPOSTA ESTRATÉGICA

Um personagem procurado deve avaliar:

- gravidade;
- conhecimento da guarda;
- capacidade local;
- recursos;
- rotas conhecidas;
- relações;
- segurança;
- probabilidade de captura.

Migração existente deve ser reutilizada.

Não criar sistema de teleport/flee especial.

---

# 47. PERSEGUIÇÃO INTERLOCAL

Não criar conhecimento global.

Mas um Commitment pode continuar além da cidade quando:

- destino provável é conhecido;
- informação nova foi recebida;
- existe rota conhecida;
- perseguidor consegue viajar.

Isso pode valer para:

- perseguição pessoal;
- vingança;
- busca;
- investigação.

Guardas também podem continuar somente quando possuem base institucional e informação compatível.

---

# 48. LONGA DISTÂNCIA NÃO É LOCALIZAÇÃO EXATA

Conhecer que alguém foi para outra região/localidade não significa conhecer a célula atual.

Ao chegar:

o perseguidor precisa:

- buscar;
- perguntar;
- observar;
- obter notícia.

Reutilizar conhecimento/percepção atuais.

---

# 49. RELAÇÕES PRECISAM MODIFICAR COMPROMISSO

Strength/importance da relação deve alterar:

- grief;
- protection;
- revenge;
- forgiveness;
- willingness to risk.

Uma relação superficial e uma relação familiar forte não devem possuir o mesmo peso.

Reutilizar estrutura relacional atual.

---

# 50. IMPACTO EM TERCEIROS

Quando dois NPCs entram em conflito:

as consequências não devem ficar restritas ao par.

Terceiros que realmente:

- conhecem os envolvidos;
- testemunham;
- recebem informação;

podem gerar respostas próprias.

Isso já existe parcialmente.

A 4.5 deve permitir maior continuidade dessas respostas.

---

# 51. NÃO CRIAR PROPAGAÇÃO EXPONENCIAL

Todo fato não deve ativar todos os conhecidos.

Use:

- força da relação;
- gravidade;
- confiança;
- distância;
- relevância;
- personalidade.

Monitorar explosão de Needs/Commitments.

---

# 52. AMBIÇÃO — USAR O TRAÇO QUE JÁ EXISTE

O projeto já possui `ambition`.

NÃO criar:

`ambition2`.

O traço atual representa:

**quanto o personagem tende a perseguir ascensão e objetivos maiores.**

A Fase 4.5 deve finalmente dar a esse traço objetivos concretos de longo prazo.

---

# 53. INTRODUZIR ASPIRATIONS

Criar estrutura equivalente a:

`Aspiration`.

Aspiration representa:

**algo que o personagem gostaria de alcançar ao longo de sua vida.**

Não é Need urgente.

Não é Action.

Não é cargo.

Não é quest.

---

# 54. ASPIRAÇÃO MAIOR E MENOR

Cada personagem pode possuir:

- uma aspiração principal;
- poucas aspirações secundárias.

Não criar dezenas.

A aspiração principal deve ser relativamente estável.

As secundárias podem mudar mais facilmente.

---

# 55. ASPIRAÇÕES DEVEM NASCER DO PERSONAGEM

Derivar de:

- personalidade;
- profissão;
- relações;
- riqueza;
- posição social;
- habilidades;
- experiências;
- reputação;
- oportunidades conhecidas;
- história.

Não escolher apenas RNG.

RNG determinístico pode desempatar possibilidades igualmente coerentes.

---

# 56. ASPIRAÇÃO NÃO É ROTEIRO

Não armazenar:

“executar A, depois B, depois C”.

Aspiration oferece direção.

O Need/Goal System decide passos locais.

---

# 57. AMBITION MODIFICA ASPIRATION

Traço ambition pode alterar:

- intensidade;
- persistência;
- tolerância ao fracasso;
- investimento de tempo;
- risco aceito;
- frequência de retorno ao objetivo.

Ambição baixa pode permitir que aspiração exista sem dominar a vida.

Ambição alta pode criar forte Commitment.

---

# 58. ASPIRAÇÕES NESTA FASE DEVEM SER PESSOAIS/SOCIAIS

NÃO implementar agora:

- golpe de Estado;
- tomada de reino;
- facção política;
- revolução;
- guerra;
- comando de exército;
- política estatal.

Aspirações desta fase devem operar sobre capacidades já existentes.

Podem envolver abstratamente:

- riqueza;
- competência;
- prestígio;
- reconhecimento;
- profissão;
- segurança;
- família;
- reputação;
- posição social já existente.

Não criar sistemas novos de governo.

---

# 59. CARGOS FUTUROS

A arquitetura de Aspiration deve permitir que no futuro seja possível adicionar novos destinos.

Mas NÃO implementar agora a lógica política.

Fase 5 poderá fornecer novos Goals possíveis para o mesmo sistema.

Não antecipar essa implementação.

---

# 60. ASPIRATION PODE GERAR NEEDS DE AUTO-INICIATIVA

Hoje muitas Needs surgem porque algo aconteceu.

Aspiration deve permitir Needs que surgem porque:

**o personagem quer mudar sua condição.**

Isso é um dos principais objetivos da Fase 4.5.

---

# 61. AUTO-INICIATIVA

O NPC deve poder gerar objetivos sem:

- estar morrendo;
- ser atacado;
- ser roubado;
- receber ordem.

Ele pode simplesmente decidir investir tempo em melhorar sua situação quando existe oportunidade conhecida.

---

# 62. PROGRESSO PRECISA SER REAL

Uma ação ligada a Aspiration ou Commitment precisa possuir progresso verificável.

Não repetir atividade que não aproxima o objetivo apenas porque possui nome compatível.

Registrar:

- progresso;
- nenhum progresso;
- regressão;
- bloqueio.

---

# 63. NÃO CONFUNDIR ATIVIDADE COM PROGRESSO

Executar 100 ações relacionadas não significa que um objetivo avançou.

A auditoria deve distinguir:

activity_count

de:

meaningful_progress.

---

# 64. ABANDONO DE OBJETIVOS

Commitments/Aspirations podem ser abandonados quando:

- tornam-se impossíveis;
- custo aumenta demais;
- motivação cai;
- relação muda;
- evidência muda;
- objetivo deixa de fazer sentido;
- sucessivos fracassos reduzem agência percebida;
- outra prioridade de vida passa a dominar.

Registrar motivo.

---

# 65. PERSISTÊNCIA NÃO SIGNIFICA TEIMOSIA INFINITA

`persistence` aumenta tolerância a fracasso.

Não torna NPC incapaz de desistir.

Falha repetida sem informação ou progresso precisa alterar estratégia ou reduzir Utility.

---

# 66. MUDANÇA DE ESTRATÉGIA

Commitment deve permitir trocar solução mantendo objetivo.

Não:

falhou `pursue`
→ `pursue`
→ `pursue`.

Mas:

falhou solução atual  
→ atualizar conhecimento  
→ reavaliar candidatos.

Tudo dentro da arquitetura existente.

---

# 67. NÃO IMPLEMENTAR UM PLANNER GIGANTE

Não criar GOAP completo.

Não criar árvore de planos globais.

Não criar LLM planner.

Objetivos longos devem emergir de:

- Commitment persistente;
- Need;
- conhecimento;
- solução local.

Cada decisão continua sendo local.

---

# 68. RELAÇÕES DEVEM MUDAR COM A HISTÓRIA

Usar sistemas atuais para permitir consequências duradouras de:

- ajuda;
- abandono;
- agressão;
- proteção;
- traição;
- vingança;
- perdão;
- reparação.

Não criar RelationshipSystem novo sem necessidade.

Mas garantir que esses fatos realmente alteram decisões futuras.

---

# 69. REPUTAÇÃO DEVE TER EFEITO FUTURO

Se reputação já registra violência, ajuda, medo etc.:

as avaliações futuras precisam consultar esses dados de forma coerente.

Não implementar reputação universal.

Cada NPC continua possuindo sua própria interpretação.

---

# 70. IMPACTO SOCIAL

O critério mais importante desta fase é:

**uma ação de um NPC deve conseguir alterar as possibilidades e decisões futuras de outros NPCs.**

O mundo deve possuir propagação de consequência.

---

# 71. MORTALIDADE

Não estabelecer meta artificial de mortes.

Não exigir:

X homicídios por mil habitantes.

Mas medir se situações com alto potencial letal continuam terminando quase sempre sem possibilidade real de fatalidade.

---

# 72. DIAGNOSTICAR PASSIVIDADE LETAL

Instrumentar casos em que:

- grievance muito forte;
- Commitment ativo;
- alvo conhecido/presente;
- personalidade agressiva compatível;
- intenção letal possível;
- recurso físico disponível;

mas nunca ocorre escalada.

Registrar por que:

- Utility;
- risco;
- medo;
- incapacidade;
- solução ausente;
- Goal antigo;
- trégua;
- distância;
- outro Need.

Não aumentar dano antes desse diagnóstico.

---

# 73. DIAGNOSTICAR PASSIVIDADE VITAL

Também registrar casos em que:

- sobrevivência está crítica;
- soluções conhecidas existem;
- soluções conservadoras falharam;
- personagem morre sem ampliar seu repertório de decisões.

Queremos saber se ele realmente não tinha alternativa ou se o sistema continuou excessivamente conservador.

---

# 74. MÉTRICAS DE COMMITMENT

Registrar:

- criados;
- concluídos;
- abandonados;
- expirados;
- pausados;
- retomados;
- duração;
- mudanças de estratégia;
- progresso médio;
- tempo sem progresso.

Separar por origem.

---

# 75. MÉTRICAS DE LONGAS HISTÓRIAS

Criar métricas melhores que apenas tamanho do arco.

Uma história longa deve possuir:

- múltiplos acontecimentos significativos;
- mudança de estado;
- mudança de objetivo ou estratégia;
- consequências;
- mais de uma fase causal.

Não contar 100 golpes repetidos como 100 capítulos.

---

# 76. SEGMENTAÇÃO DE ARCOS

Para auditoria, identificar transições como:

- objetivo adotado;
- nova informação;
- mudança de estratégia;
- deslocamento;
- confronto;
- consequência grave;
- novo participante;
- resolução;
- abandono.

Isso permite medir profundidade narrativa.

---

# 77. MÉTRICA DE IMPACTO

Para ações relevantes, medir quantos novos estados causais foram produzidos.

Exemplos de categorias abstratas:

- relação alterada;
- novo conhecimento;
- nova Need;
- novo Commitment;
- ferimento;
- morte;
- migração;
- reputação;
- captura;
- mudança econômica.

Não usar essa métrica diretamente como Utility.

É auditoria.

---

# 78. MÉTRICAS DE VIOLÊNCIA

Registrar:

- conflitos;
- intenção de contenção;
- intenção de ferir;
- intenção letal;
- mudança de intenção durante conflito;
- incapacidade;
- poupado após incapacidade;
- morte;
- fuga;
- rendição;
- captura;
- autor procurado;
- retaliação futura.

---

# 79. MÉTRICAS DE VINGANÇA

Registrar:

- vinganças ativadas;
- Commitments de vingança;
- alvo conhecido/desconhecido;
- alvo localizado;
- viagens motivadas;
- ataques executados;
- desistências;
- resolução;
- mortes decorrentes;
- nova retaliação causada.

Não chamar ativação de vingança concluída.

---

# 80. MÉTRICAS DE GUARDA

Registrar:

- crimes graves conhecidos pela instituição;
- guardas que aprenderam cada caso;
- guardas que receberam Commitment;
- busca;
- encontro;
- captura;
- fuga do suspeito;
- suspeito que deixou a cidade;
- caso abandonado;
- caso resolvido.

---

# 81. MÉTRICAS DE AMBIÇÃO

Registrar:

- Aspiration principal;
- intensidade;
- Commitments derivados;
- progresso;
- mudança de profissão;
- riqueza;
- reconhecimento;
- status já existente;
- abandono;
- satisfação.

Não avaliar sucesso somente pelo número de ações.

---

# 82. TESTES — POUCOS E ESTRUTURAIS

Não criar dezenas de novos testes.

Adicionar aproximadamente:

**12–20 regressões de alto valor.**

---

# 83. TESTES ESSENCIAIS

Cobrir pelo menos:

1. Commitment persiste após interrupção fisiológica.
2. Fato causal permanece referenciado sem duplicar choque.
3. Falha repetida pode trocar estratégia.
4. Commitment pode ser abandonado.
5. Impulse não executa Action diretamente.
6. Perceived agency usa somente conhecimento real.
7. Necessidade extrema amplia soluções sem obrigar crime.
8. Vingança contra autor desconhecido não aponta culpado real.
9. Knowledge posterior pode preencher target.
10. Violência possui intenção separada do dano.
11. Incapacidade em conflito não letal encerra normalmente.
12. Intenção letal permite nova decisão após incapacidade.
13. Morte conhecida pode gerar novo Commitment em relação válida.
14. Crime grave conhecido institucionalmente pode chegar a mais de um guarda.
15. Guarda sem informação continua sem saber.
16. Perseguição distante usa informação conhecida, sem posição global.
17. Aspiration deriva do estado/personagem e persiste.
18. Ambition modifica persistência/intensidade, não cria Action automática.
19. Save/load preserva novos estados.
20. Determinismo continua válido.

Não é obrigatório implementar vinte se alguns forem cobertos pela suíte existente.

---

# 84. AUDITORIA CURTA

Antes da longa:

500–1.000 horas.

Objetivos:

- detectar loops;
- Commitments eternos;
- explosão de memória;
- perseguição infinita;
- violência sistêmica;
- passividade sistêmica;
- guardas duplicando casos;
- objetivos sem progresso.

Corrigir apenas problemas concretos.

---

# 85. AUDITORIA LONGA

Depois:

uma campanha global nova de aproximadamente 5.000–10.000 horas.

Não rodar três campanhas enormes.

O foco da longa deve ser:

**qualidade e continuidade das histórias.**

---

# 86. AUDITORIA NARRATIVA É O PRINCIPAL RESULTADO

Selecionar histórias reais com preferência para:

- múltiplos participantes;
- duração longa;
- mudanças de objetivo;
- mudanças de cidade;
- consequências familiares;
- perseguições;
- vingança;
- violência;
- reparação;
- ambição;
- ascensão pessoal;
- abandono;
- fatalidade;
- histórias não resolvidas.

Não inventar.

---

# 87. NÃO ESCOLHER APENAS HISTÓRIAS BEM-SUCEDIDAS

Mostrar também:

- Commitment que falhou;
- vingança abandonada;
- perseguição que perdeu pista;
- ambição frustrada;
- NPC que permaneceu passivo por razão coerente;
- NPC que tomou decisão ruim;
- personagem que morreu sem alcançar objetivo.

---

# 88. ANALISAR HISTÓRIA COMO CADEIA

Para cada caso relevante:

State  
→ Knowledge  
→ Emotion  
→ Need  
→ Impulse  
→ Commitment  
→ Solution  
→ Action  
→ Response  
→ Consequence  
→ New State.

Se houver continuação:

→ New Knowledge  
→ Reassessment  
→ Strategy Change  
→ Next Action.

---

# 89. NÃO IMPLEMENTAR NESTA FASE

NÃO implementar:

- revolução;
- golpe;
- facções políticas;
- ideologias;
- política coletiva;
- tomada de reino;
- mudanças de regime;
- legislação;
- novas políticas de governo;
- guerra;
- exércitos;
- cerco;
- conquista territorial;
- diplomacia;
- religião organizada;
- deuses;
- milagres;
- magia divina;
- hierarquia política profunda;
- novo sistema de cargos estatais.

Reinos e facções existentes devem continuar funcionando como atualmente.

Não expandi-los.

---

# 90. NÃO USAR RAIVA PARA CRIAR POLÍTICA AINDA

Raiva, grievance, pobreza e desigualdade continuam sendo armazenadas.

Elas terão importância posteriormente.

Nesta fase servem apenas para comportamento individual/interpessoal.

Não criar movimento coletivo.

---

# 91. NÃO ALTERAR A FASE 4.1 SEM NECESSIDADE

Preservar:

- alimentação antecipada;
- recovery;
- origem de dano;
- cura fisiológica;
- consumo;
- economia;
- LOD vital.

Não tentar novamente “resolver fome” nesta fase.

Apenas integrar a pressão vital ao novo modelo de impulso.

---

# 92. NÃO ALTERAR COMBATE SEM NECESSIDADE

Preservar:

- fórmula de dano;
- armas;
- defesa;
- lesão;
- fuga;
- rendição;
- recuperação.

A principal expansão deve ser:

**intenção e continuidade.**

Não letalidade artificial via dano.

---

# 93. NÃO CRIAR NPCs MAIS VIOLENTOS POR CONSTANTE GLOBAL

Não adicionar:

`AGGRESSION_MULTIPLIER = 2`.

O objetivo não é aumentar ataques.

O objetivo é:

personagens corretos  
+ situações corretas  
+ motivações corretas

produzirem consequências mais fortes.

---

# 94. NÃO CRIAR NPCs MAIS AMBICIOSOS GLOBALMENTE

Não aumentar artificialmente todos os valores de ambition.

Usar distribuição atual.

A diferença deve vir de dar significado ao traço.

---

# 95. NÃO GARANTIR HISTÓRIAS

O motor pode produzir histórias monótonas.

Isso não é automaticamente bug.

Mas deve possuir capacidade de produzir trajetórias longas quando condições causais sustentam isso.

---

# 96. CRITÉRIO DE SUCESSO — AGÊNCIA

Um NPC não deve apenas responder:

**“O que faço nesta hora?”**

Ele deve também conseguir manter:

**“O que estou tentando mudar na minha vida?”**

---

# 97. CRITÉRIO DE SUCESSO — IMPACTO

Uma ação importante deve conseguir alterar:

- a própria trajetória;
- trajetória de outro personagem;
- relações;
- conhecimento;
- segurança;
- localização;
- reputação;
- objetivos futuros.

---

# 98. CRITÉRIO DE SUCESSO — HISTÓRIA LONGA

Precisamos encontrar histórias onde o mesmo motivo sobreviva a várias decisões e gere diferentes etapas.

Não medir duração somente em horas.

Medir:

**transformações causais.**

---

# 99. CRITÉRIO DE SUCESSO — FATALIDADE

Mortes interpessoais devem continuar minoritárias.

Porém:

quando existe contexto extremo, intenção letal, oportunidade e capacidade,

a simulação deve realmente permitir um resultado fatal.

Não encerrar artificialmente toda violência antes disso.

---

# 100. CRITÉRIO DE SUCESSO — GUARDA

Um crime grave conhecido não deve depender eternamente da iniciativa de um único guarda.

A instituição local precisa ser capaz de produzir resposta através de múltiplos indivíduos reais.

Sem conhecimento global.

---

# 101. CRITÉRIO DE SUCESSO — VINGANÇA

Uma vingança importante precisa conseguir:

- permanecer ativa;
- sobreviver a interrupções;
- procurar informação;
- viajar;
- mudar estratégia;
- encontrar ou perder o alvo;
- terminar ou ser abandonada.

Sem roteiro.

---

# 102. CRITÉRIO DE SUCESSO — AMBIÇÃO

Personagens ambiciosos precisam demonstrar mais comportamento de auto-iniciativa e continuidade em objetivos de ascensão pessoal do que personagens semelhantes com baixa ambição.

Não precisam necessariamente alcançar sucesso.

---

# 103. PRINCÍPIO CENTRAL

A Fase 4 construiu:

**ação e resposta.**

A Fase 4.1 melhorou:

**sobrevivência e recuperação.**

A Fase 4.5 deve construir:

**iniciativa e continuidade.**

O personagem não deve existir apenas como alguém para quem coisas acontecem.

Ele deve conseguir decidir:

**“isso precisa mudar.”**

E então continuar tentando alterar sua realidade enquanto ainda existirem:

- motivação;
- conhecimento;
- possibilidade;
- personalidade compatível.

---

# 104. PRINCÍPIO FINAL

Não queremos escrever histórias.

Queremos construir agentes que consigam sustentar intenções por tempo suficiente para que histórias apareçam.

O ciclo desejado é:

acontecimento  
→ interpretação  
→ emoção  
→ necessidade  
→ impulso  
→ compromisso  
→ ação  
→ reação social  
→ consequência  
→ reavaliação  
→ nova ação.

Quando isso funciona, eventos deixam de ser episódios isolados.

Eles passam a alterar vidas.

E quando vidas alteram outras vidas repetidamente:

**o mundo começa a produzir história.**