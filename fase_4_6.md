# FASE 4.6 — ESCALADA FATAL, INVESTIGAÇÃO ATIVA E CONTINUIDADE DE PERSEGUIÇÃO

Base atual: `mvp-6-fase4.5`.

A Fase 4.6 NÃO é a Fase 5.

Não implementar:

- política profunda;
- revoluções;
- novas facções;
- tomada de reinos;
- guerras;
- exércitos;
- diplomacia;
- religião organizada;
- deuses;
- magia;
- cargos políticos avançados;
- novos sistemas coletivos de governo.

Reinos e facções existentes devem permanecer funcionando exatamente como funcionam atualmente.

A Fase 4.6 é uma etapa de refinamento da agência interpessoal introduzida na Fase 4.5.

O objetivo principal é fazer com que:

**Needs + personalidade + emoções + histórico + Commitment + conhecimento + contexto consigam, em casos extremos, gerar consequências irreversíveis entre indivíduos.**

Especialmente:

- perseguições realmente investigativas;
- vinganças persistentes;
- escalada de conflitos;
- intenção deliberadamente letal;
- ciclos de ódio;
- fuga após crimes graves;
- reativação de objetivos quando surgem novas informações.

Tudo deve continuar emergindo do sistema.

Não escrever histórias prontas.

---

# 1. ESTADO ATUAL

A Fase 4.5 comprovou que:

- Commitments persistem;
- objetivos podem sobreviver a interrupções;
- personagens mudam estratégia;
- Ambition influencia iniciativa;
- memória causal funciona;
- perseguições podem atravessar localidades;
- guardas conseguem compartilhar casos localmente;
- violência possui intenção separada do dano.

Porém a campanha revelou um gargalo importante.

Houve aproximadamente:

- 20.655 ataques;
- 10 mortes por combate;
- milhares de Commitments de vingança/reparação;
- muitos casos de perseguição bloqueados por distância ou pista antiga;
- pouquíssimas situações naturais chegando a ataque deliberadamente letal;
- nenhuma continuação natural relevante após incapacidade;
- grande quantidade de intenção, mas pouca transformação fatal.

Portanto:

**a arquitetura já consegue querer, mas ainda encontra dificuldade para perseguir, escalar e concluir.**

---

# 2. OBJETIVO DA FASE

A Fase 4.6 deve responder:

> Quando um NPC acumula motivos extremamente fortes contra outro NPC, ele consegue chegar naturalmente ao ponto de decidir que quer matá-lo?

E:

> Quando um NPC procura alguém e sua pista fica velha, ele consegue investigar ativamente em vez de esperar passivamente uma nova informação cair em sua memória?

E:

> Quando uma busca falha, ela consegue entrar em espera e ser retomada posteriormente sem desaparecer nem repetir buscas inúteis?

---

# 3. PRESERVAÇÃO PRIMEIRO

O princípio técnico desta fase é:

**preservar tudo que já funciona.**

Não reescrever sem necessidade:

- Need System;
- Goal System;
- Utility;
- Commitment;
- Aspiration;
- Impulse;
- personalidade;
- emoções;
- grievances;
- conhecimento;
- relações;
- reputação;
- combate;
- lesões;
- recuperação;
- fome/sede;
- economia;
- profissões;
- migração;
- navegação;
- guardas;
- criminalidade;
- população;
- LOD;
- save/load.

Antes de alterar um componente existente:

1. demonstrar a limitação;
2. verificar se extensão é suficiente;
3. preferir integração sobre substituição;
4. manter compatibilidade conceitual;
5. registrar a alteração.

---

# 4. NÃO REBALANCEAR COMBATE POR MORTALIDADE

Não aumentar:

- dano;
- armas;
- multiplicadores;
- HP;
- chance crítica;
- frequência global de ataques.

O baixo número de mortes não deve ser corrigido aumentando DPS.

A hipótese principal desta fase é:

**falta intenção letal natural e continuidade causal suficiente, não dano.**

---

# 5. INTENÇÃO LETAL

A intenção `kill` ou equivalente já deve existir conceitualmente na camada de violência.

A Fase 4.6 precisa fazer com que ela possa surgir naturalmente no mundo.

Ela deve continuar sendo:

- rara;
- contextual;
- direcionada;
- explicável;
- auditável.

Não transformar violência comum em homicídio.

---

# 6. MATAR NÃO É UM TRAÇO DE PERSONALIDADE

Não criar:

`killer_trait`

Não criar:

`murder_chance`

Não criar:

`random_kill_probability`.

Um personagem decide matar porque uma combinação extrema de circunstâncias tornou essa opção aceitável para ELE contra AQUELE alvo.

---

# 7. PRESSÃO LETAL DIRECIONADA

Criar uma avaliação conceitual equivalente a:

`LethalPressure(actor, target, context)`

Ela representa:

**quanto o personagem ultrapassou suas barreiras normais contra matar aquele alvo específico.**

Não deve existir como emoção global.

É relacional.

---

# 8. FONTES POSSÍVEIS DE PRESSÃO LETAL

A avaliação pode considerar:

- grievance contra o alvo;
- raiva direcionada;
- ressentimento direcionado;
- humilhações conhecidas;
- perdas atribuídas ao alvo;
- ferimentos causados pelo alvo;
- ameaça contínua;
- assassinato de pessoa importante;
- vingança ativa;
- desespero;
- repetição do conflito;
- fracasso de respostas anteriores;
- Commitment;
- intensidade relacional;
- percepção de perigo futuro;
- percepção de que o problema continuará enquanto o alvo estiver livre.

Essas variáveis não devem ser simplesmente somadas sem semântica.

---

# 9. BARREIRAS À INTENÇÃO LETAL

Também considerar:

- compaixão;
- honestidade quando relevante;
- medo;
- baixa coragem;
- vínculo afetivo com o alvo;
- culpa provável;
- risco de morrer;
- testemunhas;
- autoridade presente;
- consequências criminais conhecidas;
- reputação;
- incerteza sobre autoria;
- alternativas não letais ainda plausíveis.

A intenção letal precisa vencer essas barreiras.

---

# 10. LIMIAR ALTO

A intenção de matar deve exigir uma convergência incomum.

Não utilizar regra simples:

`LethalPressure > 80`.

Pode existir threshold interno, mas o cálculo precisa exigir condições semanticamente coerentes.

Exemplo conceitual de princípio:

uma emoção extrema isolada não basta.

Várias pressões compatíveis e direcionadas precisam convergir.

---

# 11. ESGOTAMENTO INTERPESSOAL

Introduzir/reaproveitar um conceito equivalente a:

`relationship_conflict_exhaustion`

Ele representa:

**quanto um conflito específico entre duas pessoas já consumiu alternativas menos extremas.**

Pode considerar:

- quantidade de episódios relevantes;
- duração;
- novas agressões;
- promessas quebradas;
- reparações fracassadas;
- ameaças recorrentes;
- tentativas de afastamento;
- reencontros hostis;
- novas perdas.

Não confundir simplesmente com número de ataques.

---

# 12. ESGOTAMENTO NÃO É CONTADOR DE GOLPES

Não fazer:

`5 ataques -> matar`.

Uma sequência de ataques dentro de um único confronto deve ter peso limitado.

O sistema deve distinguir:

**repetição mecânica dentro do mesmo episódio**

de:

**histórico de conflito entre episódios diferentes.**

---

# 13. ALTERNATIVAS NÃO LETAIS ESGOTADAS

Registrar semanticamente quando soluções relevantes contra o mesmo problema:

- falharam;
- foram recusadas;
- foram quebradas;
- não alteraram a situação;
- tornaram-se inviáveis.

Isso pode aumentar a disposição a considerar soluções mais extremas.

Não exigir uma sequência específica.

---

# 14. NÃO OBRIGAR ESCALADA

Mesmo em situação grave:

o NPC pode continuar escolhendo:

- fugir;
- denunciar;
- capturar;
- ameaçar;
- evitar;
- perdoar;
- abandonar;
- negociar.

A intenção letal apenas entra no conjunto de soluções plausíveis.

---

# 15. INTENÇÃO LETAL DEVE SER UM OBJETIVO

Quando `kill` vence:

o personagem passa a ter um objetivo explícito:

**causar a morte daquele alvo.**

Não é:

“atacar mais forte.”

É uma finalidade diferente.

---

# 16. DANO CONTINUA IGUAL

Uma pessoa tentando matar continua usando:

- mesma arma;
- mesmo poder;
- mesma defesa;
- mesma lesão;
- mesmo HP;
- mesmo RNG.

Não adicionar bônus de dano pela intenção.

---

# 17. INTENÇÃO PODE MUDAR DURANTE CONFLITO

Um confronto pode começar com intenção não letal.

Eventos durante o conflito podem alterar a avaliação.

Da mesma forma:

uma intenção letal pode diminuir.

Reavaliar após acontecimentos significativos.

---

# 18. EVENTOS QUE JUSTIFICAM REAVALIAÇÃO

Sem criar callbacks automáticos de ação, considerar nova avaliação quando houver:

- ferimento severo;
- incapacidade;
- rendição;
- intervenção;
- descoberta de informação;
- morte de terceiro;
- retirada;
- chegada de guarda;
- mudança brusca de vantagem;
- nova agressão grave.

---

# 19. INCAPACIDADE

Preservar a regra existente de incapacidade.

Conflitos comuns continuam terminando normalmente quando um personagem fica incapaz.

Porém:

se o agressor possuía intenção letal sustentada,

a incapacidade do alvo deve abrir uma nova decisão.

---

# 20. JULGAMENTO APÓS INCAPACIDADE

As opções podem incluir semanticamente:

- interromper;
- retirar-se;
- poupar;
- capturar;
- pedir auxílio;
- concluir a intenção letal.

Não obrigar morte.

A nova decisão usa novamente:

- personalidade;
- emoção;
- Commitment;
- risco;
- testemunhas;
- consequências;
- contexto.

---

# 21. POUPAR PRECISA SER REAL

Se alguém entrou com intenção letal e depois decide não matar:

registrar essa mudança.

Isso pode alterar:

- emoção;
- relação;
- grievance;
- reputação;
- Commitment.

Não precisa necessariamente significar perdão.

---

# 22. MORTE DELIBERADA DEVE SER AUDITÁVEL

Quando houver homicídio intencional, registrar:

- motivação;
- Commitment;
- fato causal;
- intensidade;
- pressão letal;
- principais fatores positivos;
- principais barreiras;
- decisão final;
- conhecimento disponível.

O auditor precisa conseguir explicar:

**por que este NPC decidiu matar este outro NPC.**

---

# 23. EVITAR “MURDER BY UTILITY NOISE”

Não permitir que pequenas diferenças aleatórias façam `kill` aparecer em situações triviais.

A própria solução letal só deve existir quando pré-condições fortes forem satisfeitas.

RNG pode desempatar escolhas plausíveis.

Não deve transformar opção absurda em plausível.

---

# 24. CONSEQUÊNCIA DA MORTE

Preservar `CharacterKilled`.

Depois da morte:

- conhecimento continua local;
- testemunhas sabem conforme percepção;
- autoria pode ser desconhecida;
- família remota não aprende automaticamente;
- justiça depende de informação;
- luto depende de conhecimento;
- vingança precisa de autoria conhecida ou investigação.

---

# 25. CICLO DE ÓDIO

Não implementar sistema chamado “vendetta”.

O ciclo deve resultar da repetição do motor.

Morte:

→ fato.

Familiar aprende:

→ interpretação.

Relação + personalidade + emoções:

→ Need/Commitment.

Nova ação:

→ possível nova violência.

Se houver nova morte:

o processo pode surgir novamente em outro grupo.

---

# 26. CICLOS DEVEM SER FINITOS NATURALMENTE

Podem terminar por:

- ignorância;
- distância;
- morte;
- medo;
- falta de recursos;
- reconciliação;
- desistência;
- captura;
- mudança emocional;
- ausência de novas pistas.

Não criar ciclo automático.

---

# 27. INVESTIGAÇÃO ATIVA

O segundo grande foco da Fase 4.6 é:

**pistas devem ser procuradas.**

Não depender apenas de receber informação espontaneamente.

---

# 28. PISTA NÃO É O ALVO

Uma pista representa conhecimento sobre:

- onde alguém esteve;
- quando esteve;
- quem pode ter visto;
- para onde talvez tenha ido.

Não representa a localização atual.

---

# 29. ESTRUTURA DE PISTA

Criar/reaproveitar estrutura conceitual com:

- subject;
- location;
- timestamp;
- source;
- confidence;
- specificity;
- direction, quando existir;
- related_fact;
- status.

Não exagerar em complexidade.

---

# 30. PISTAS SÃO CONHECIMENTO

Nunca armazenar informação objetiva que o personagem não possui.

O auditor pode saber a verdade.

O NPC continua agindo somente sobre sua percepção.

---

# 31. SEGUIR PISTA

Quando um Commitment de busca/perseguição possui pista utilizável:

o NPC pode decidir viajar até a área conhecida.

Reutilizar:

- navegação;
- rotas;
- reserva;
- migração/viagem existentes.

Não teleportar.

---

# 32. CHEGAR À PISTA NÃO ENCERRA A BUSCA

Quando chega ao local de uma pista antiga:

o NPC deve poder iniciar ações de investigação.

Isso é o ponto central.

---

# 33. INVESTIGAÇÃO COMO GERAÇÃO DE CONHECIMENTO

A busca deve tentar transformar:

informação antiga

em:

informação mais recente, específica ou confiável.

---

# 34. AÇÕES ABSTRATAS DE INVESTIGAÇÃO

Adicionar/reutilizar soluções equivalentes a:

- procurar sinais locais;
- perguntar;
- consultar contato conhecido;
- verificar local relevante;
- observar;
- investigar pessoas relacionadas;
- seguir informação direcional.

Não transformar isso em roteiro.

---

# 35. PERGUNTAR A PESSOAS

Uma pessoa só pode fornecer informação que realmente:

- viu;
- sabe;
- recebeu;
- acredita.

Não gerar resposta procedural onisciente.

---

# 36. DISPOSIÇÃO PARA INFORMAR

O informante pode:

- responder;
- recusar;
- omitir;
- mentir se o sistema suportar;
- fornecer informação incompleta;
- fornecer rumor.

Depender de:

- relação;
- medo;
- honestidade;
- lealdade;
- reputação;
- relação com o procurado;
- contexto.

Não obrigar todo mundo a colaborar.

---

# 37. INFORMAÇÃO PODE ESTAR ERRADA

Rumores continuam possíveis.

Uma nova pista pode:

- ser correta;
- estar atrasada;
- ser vaga;
- ser incorreta dentro da semântica existente.

Não permitir ao perseguidor distinguir automaticamente.

---

# 38. PISTA MAIS NOVA

Ao obter informação relevante:

avaliar se ela melhora a busca.

Pode melhorar:

- tempo;
- local;
- direção;
- confiança;
- especificidade.

Não substituir pista boa por pista claramente inferior sem motivo.

---

# 39. INVESTIGAÇÃO LOCAL LIMITADA

Não permitir infinitas perguntas.

A investigação deve possuir:

- tentativas;
- oportunidades;
- fontes disponíveis;
- tempo;
- progresso.

Quando uma área foi razoavelmente esgotada:

o NPC precisa reavaliar.

---

# 40. SEM PISTA NOVA

Se não existe avanço:

o Commitment NÃO precisa ser abandonado.

Pode passar para estado dormente.

---

# 41. COMMITMENT DORMANT

Adicionar um estado equivalente a:

`waiting_for_information`.

Ele significa:

**o personagem ainda se importa, mas não possui ação útil neste momento.**

---

# 42. DORMÊNCIA NÃO É FRACASSO

Enquanto dormente:

- não repetir buscas inúteis;
- não gerar Goal toda hora;
- não consumir processamento indevidamente;
- não perder automaticamente a causa;
- não reaplicar emoção como fato novo.

---

# 43. VOLTAR À VIDA

Um NPC sem pista deve:

- retornar para casa ou local coerente;
- continuar profissão;
- comer;
- dormir;
- manter relações;
- seguir outros objetivos.

Ele não deve ficar parado esperando.

---

# 44. REATIVAÇÃO

Quando uma nova informação relevante chegar:

o Commitment pode sair automaticamente de dormência.

Mas:

reativar Commitment NÃO executa uma Action.

Ele apenas volta a competir no Need/Goal System.

---

# 45. REATIVAÇÃO DEVE VALIDAR A PISTA

A nova informação precisa:

- referir-se ao alvo;
- possuir alguma relevância;
- ser suficientemente nova/útil;
- ser conhecida pelo NPC.

Não acordar perseguições por qualquer rumor irrelevante.

---

# 46. INVESTIGAÇÃO E VINGANÇA SÃO SEPARADAS

Um Commitment de vingança pode usar investigação.

Mas investigar não significa vingança.

Um guarda também pode investigar.

Um familiar procurando desaparecido também.

A funcionalidade deve ser reutilizável.

---

# 47. INVESTIGAÇÃO COMO CAPACIDADE GERAL

A arquitetura deve suportar:

`buscar pessoa/informação`

sem estar amarrada exclusivamente ao crime.

Porém não expandir o escopo desta fase para novos sistemas narrativos.

---

# 48. GUARDA E INVESTIGAÇÃO

Guardas com caso grave podem:

- seguir pista;
- procurar testemunhas;
- pedir informação;
- investigar área.

Tudo precisa respeitar:

- conhecimento institucional;
- jurisdição;
- rota;
- recursos;
- informação disponível.

---

# 49. VÁRIOS GUARDAS

Preservar tarefas institucionais da Fase 4.5.

Em casos graves:

múltiplos guardas podem trabalhar sobre o mesmo caso.

Mas não repetir todos a mesma investigação automaticamente.

---

# 50. COMPARTILHAMENTO DE NOVA PISTA

Quando um guarda aprende nova informação e ela entra formalmente no caso:

outros guardas locais podem aprender posteriormente pelos mecanismos institucionais existentes.

Não instantaneamente.

---

# 51. GRAVIDADE PRECISA AFETAR PERSISTÊNCIA

Casos muito graves devem:

- demorar mais para expirar;
- sustentar mais investigação;
- receber maior prioridade;
- justificar mais recursos institucionais.

Delitos leves continuam podendo ser abandonados rapidamente.

---

# 52. HOMICÍDIO CONHECIDO

Um homicídio cuja autoria é suficientemente conhecida precisa ser tratado como evento institucional grave.

Não obrigar captura.

Mas gerar resposta coerente quando existe guarda funcional.

---

# 53. MATAR PRECISA ALTERAR A ROTINA DO AUTOR

Um autor que sabe ou acredita que:

- foi visto;
- foi identificado;
- é procurado;

deve considerar as consequências.

Isso pode alterar Utility de:

- permanecer;
- esconder-se;
- fugir;
- migrar;
- evitar área;
- procurar apoio.

Não obrigar fuga.

---

# 54. FUGA APÓS CRIME

Reutilizar viagem/migração.

Não criar `escape_teleport`.

Se fugir:

- precisa de rota;
- tempo;
- recurso;
- deslocamento real.

---

# 55. PERSEGUIÇÃO ATRAVÉS DE LOCALIDADES

Um perseguidor pode atravessar localidades somente quando:

- possui pista;
- conhece rota;
- consegue viajar;
- Commitment é forte o suficiente.

Ao chegar:

não conhece automaticamente a posição final.

Investiga novamente.

---

# 56. PISTA PODE FORMAR CADEIA

Conceitualmente:

pista A  
→ investigação  
→ pista B  
→ deslocamento  
→ investigação  
→ pista C.

Mas não armazenar isso como plano obrigatório.

Cada transição é consequência de ação real.

---

# 57. NECESSIDADES SECUNDÁRIAS E COMMITMENT

A Fase 4.5 permitiu Commitments persistentes.

Nesta fase é permitido que o Commitment forneça contexto para outras Needs.

Com extremo cuidado.

---

# 58. COMMITMENT NÃO POSSUI A VIDA DO NPC

Não transformar cada NPC em protagonista de uma história única.

Um Commitment deve ser UMA influência.

O personagem continua possuindo:

- fome;
- sede;
- sono;
- profissão;
- família;
- relações;
- outras necessidades.

---

# 59. NEED CONTINUA SENDO NEED

Não criar:

`revenge_food`

`revenge_sleep`

`revenge_money`.

Food continua `food`.

Rest continua `rest`.

Money continua `money`.

---

# 60. CONTEXTO DE PREPARAÇÃO

Uma Need pode receber contexto indicando que sua satisfação também ajuda um Commitment.

Exemplo abstrato:

um recurso necessário para uma viagem planejada pode ganhar algum valor adicional.

Mas o recurso continua existindo por sua semântica original.

---

# 61. NÃO CRIAR PLANNER

Não gerar lista:

1. trabalhar;
2. comprar comida;
3. viajar;
4. perguntar;
5. matar.

Isso destruiria a emergência.

Cada decisão continua local.

Commitment apenas fornece direção persistente.

---

# 62. PREPARAÇÃO NÃO DEVE DOMINAR

O modificador derivado do Commitment deve ser limitado.

Uma necessidade secundária não pode esmagar:

- sobrevivência;
- ameaça imediata;
- outra Need genuinamente mais importante.

---

# 63. PROGRESSO DERIVADO

Se satisfazer uma Need secundária realmente aproximou o Commitment:

registrar progresso.

Se não aproximou:

não marcar artificialmente.

---

# 64. RECURSOS PARA OBJETIVO LONGO

Commitments podem considerar recursos necessários conhecidos.

Mas não criar recursos novos.

Tudo precisa vir da economia real.

---

# 65. COMPROMISSOS PROFUNDOS

Não é necessário criar outra classe.

Mas Commitment já possui intensidade/investimento.

Usar esses campos para distinguir:

- intenção fraca;
- intenção importante;
- intenção profundamente transformadora.

---

# 66. COMPROMISSO PROFUNDO ALTERA ROTINA, NÃO AS REGRAS DO MUNDO

Quanto maior:

- intensity;
- investment;
- emotional relevance;
- persistence;

maior a chance de o personagem:

- voltar ao objetivo;
- gastar tempo;
- viajar;
- procurar informação;
- aceitar risco;
- preparar recursos.

Mas ele continua submetido às mesmas regras.

---

# 67. MORTE DE PESSOA IMPORTANTE

Quando uma perda conhecida envolve relação forte:

ela pode produzir Commitment profundo.

Não obrigatoriamente vingança.

Pode produzir:

- busca;
- luto;
- proteção;
- investigação;
- retirada;
- vingança.

---

# 68. GRAVIDADE RELACIONAL

A importância de um evento deve considerar:

- força da relação;
- tipo de relação;
- história recente;
- personality;
- family_loyalty;
- compassion;
- vengefulness.

Não usar parentesco nominal apenas.

---

# 69. MORTE SEM AUTORIA

Se alguém sabe que um familiar morreu mas não sabe quem matou:

não gerar pressão letal contra culpado verdadeiro.

Pode gerar:

- investigação;
- suspeita;
- luto.

---

# 70. SUSPEITA

Se o sistema já suporta confiança:

suspeita pode direcionar investigação.

Mas intenção letal baseada em evidência fraca deve sofrer barreira forte.

Não proibir absolutamente.

A pessoa pode ser irracional.

Mas isso precisa ser explicado pela personalidade/contexto.

---

# 71. RAIVA NÃO É SUFICIENTE

Preservar este princípio:

**anger ≠ violence**

e adicionar:

**anger ≠ murder.**

Raiva participa da avaliação.

Não determina resultado.

---

# 72. DESESPERO NÃO É SUFICIENTE

Desespero alto pode reduzir aversão ao risco.

Mas não cria homicídio sem alvo/causa.

---

# 73. VINGATIVIDADE NÃO É SUFICIENTE

Vengefulness aumenta:

- duração;
- persistência;
- resistência ao perdão;
- consideração de retaliação.

Não significa automaticamente matar.

---

# 74. COMPASSION COMO BARREIRA REAL

Compaixão precisa conseguir impedir morte mesmo com conflito grave.

Especialmente no julgamento após incapacidade.

---

# 75. CORAGEM E MEDO

Coragem deve afetar disposição a:

- procurar;
- viajar;
- confrontar;
- persistir;
- entrar em situação perigosa.

Medo deve poder interromper isso.

---

# 76. HISTÓRICO ENTRE DUAS PESSOAS

Criar/reutilizar uma visão compacta de histórico relevante entre ator e alvo.

Não duplicar todo EventLog.

Apenas fornecer ao cálculo relacional informações relevantes já existentes.

---

# 77. NÃO CRESCER ESTADO SEM LIMITE

A Fase 4.5 já produziu grande volume histórico.

Evitar novos registros redundantes.

Preferir:

- agregados;
- referências;
- compactação;
- limites.

---

# 78. SAVE

Não tentar resolver completamente o save de 1,2 GB nesta fase.

Mas não piorar exponencialmente.

Medir impacto dos novos registros.

---

# 79. AUDITORIA DE INTENÇÃO LETAL

Instrumentar:

- vezes em que foi avaliada;
- vezes em que pré-condição falhou;
- vezes em que ficou disponível;
- vezes em que venceu;
- vezes em que foi abandonada;
- vezes em que alvo ficou incapaz;
- vezes em que houve misericórdia;
- vezes em que houve morte.

---

# 80. MOTIVOS DE BLOQUEIO LETAL

Registrar categorias:

- pressão insuficiente;
- compaixão;
- medo;
- risco;
- baixa confiança;
- alternativa não letal melhor;
- alvo ausente;
- incapacidade do ator;
- autoridade/testemunhas;
- Commitment insuficiente.

Isso é mais importante que simplesmente contar assassinatos.

---

# 81. AUDITORIA DE INVESTIGAÇÃO

Registrar:

- pistas conhecidas;
- pistas seguidas;
- áreas investigadas;
- pessoas perguntadas;
- informação útil;
- informação inútil;
- rumor;
- pista desatualizada;
- nova pista;
- busca encerrada;
- dormência;
- reativação.

---

# 82. QUALIDADE DA PISTA

Medir:

- idade;
- confiança;
- especificidade;
- distância até alvo real apenas no auditor;
- se levou a progresso.

O NPC não recebe a distância objetiva.

---

# 83. TAXA DE BUSCAS SEM PROGRESSO

Monitorar repetição.

Não queremos:

pista velha  
→ busca  
→ busca  
→ busca  
→ busca.

Após tentativas coerentes sem avanço:

entrar em espera/reavaliar.

---

# 84. AUDITORIA DE VINGANÇA

Para Commitments fortes:

medir:

- nascimento;
- causa;
- alvo;
- confiança;
- primeira ação;
- pistas obtidas;
- deslocamentos;
- períodos dormentes;
- reativações;
- encontro;
- confronto;
- mudança de intenção;
- resolução.

---

# 85. AUDITORIA DE CICLOS

Identificar automaticamente cadeias onde:

uma violência relevante

gera uma resposta de terceiro

que gera outra violência relevante

que gera nova resposta.

Não rotular automaticamente como feud.

Apenas detectar cadeia causal.

---

# 86. HISTÓRIA LONGA

Uma história boa nesta fase deve ser medida por:

- transformações;
- mudanças de estratégia;
- mudanças de local;
- nova informação;
- novos participantes;
- decisões irreversíveis.

Não por número de Events.

---

# 87. TESTES NOVOS

Adicionar aproximadamente:

**12–18 regressões direcionadas.**

Não criar bateria enorme.

---

# 88. TESTES ESSENCIAIS — LETALIDADE

Cobrir pelo menos:

- raiva isolada não libera intenção letal;
- convergência extrema pode liberar;
- baixa confiança reduz intenção;
- compaixão pode impedir;
- intenção letal não aumenta dano;
- conflito comum termina por incapacidade;
- intenção letal permite julgamento pós-incapacidade;
- julgamento pode resultar em poupar;
- julgamento pode resultar em matar;
- morte registra causa/Commitment corretamente.

---

# 89. TESTES ESSENCIAIS — INVESTIGAÇÃO

Cobrir:

- pista antiga leva a investigação;
- investigação pode produzir pista nova;
- informante sem conhecimento não inventa pista;
- rumor preserva confiança;
- ausência de pista coloca Commitment em espera;
- espera não abandona Commitment;
- informação nova reativa;
- reativação não executa ação automaticamente;
- viagem não consulta posição real;
- guarda compartilha pista somente pelo canal institucional existente.

Alguns podem ser unidos.

---

# 90. TESTES DE PRESERVAÇÃO

Rodar toda suíte existente uma vez ao final.

Preservar especialmente:

- Fase 4;
- Fase 4.1;
- Fase 4.5;
- alimentação;
- recuperação;
- save/load;
- determinismo.

---

# 91. AUDITORIA CURTA

Rodar primeiro:

500 horas.

Objetivos:

- detectar massacre;
- verificar se `kill` aparece naturalmente;
- impedir `kill` trivial;
- testar investigação;
- impedir loops;
- validar dormência;
- validar reativação;
- observar uso institucional.

Corrigir bugs antes da longa.

---

# 92. AUDITORIA LONGA

Rodar apenas:

**uma campanha de 5.000 horas.**

Não rodar 10.000.

Não rodar três seeds longas.

No estágio atual, 5.000 horas são suficientes para avaliação de lore.

---

# 93. OBJETIVO ATUAL DO PROJETO

O projeto deve ser tratado neste momento como:

**simulador/criador procedural de lore.**

Não otimizar decisões pensando em gameplay futuro.

Gameplay virá muito depois.

O foco atual é:

- coerência causal;
- histórias;
- impacto;
- continuidade;
- diversidade de trajetórias.

---

# 94. NÃO EXIGIR DÉCADAS SIMULADAS

Nesta fase não existem ainda sistemas que exigem várias gerações.

5.000 horas são suficientes para avaliar:

- conflitos;
- perseguições;
- vinganças;
- mortes;
- crimes;
- migrações;
- ambições;
- famílias;
- recuperação.

---

# 95. HISTÓRIAS DO RELATÓRIO

Selecionar casos reais de:

- intenção letal que surgiu;
- intenção letal que não venceu;
- misericórdia;
- assassinato deliberado;
- perseguição com várias pistas;
- pista falsa;
- perseguição suspensa;
- perseguição reativada;
- alvo perdido;
- guarda investigando;
- vingança que atravessou localidades;
- ciclo de retaliação;
- Commitment que terminou sem violência.

Não inventar casos ausentes.

---

# 96. RELATÓRIO NÃO DEVE PROCURAR SOMENTE SUCESSOS

Mostrar também falhas.

Especialmente:

- busca sem pista;
- vingança abandonada;
- assassino que escapou;
- guarda que perdeu o alvo;
- NPC que decidiu não matar;
- NPC que não teve coragem;
- investigação baseada em informação errada.

Esses casos são importantes.

---

# 97. PERGUNTA CENTRAL SOBRE LETALIDADE

O relatório deve responder:

> **Quando um NPC finalmente decide matar outro, conseguimos explicar por que a barreira foi ultrapassada?**

Se a resposta for somente:

“Utility maior”

o sistema ainda não está auditável o suficiente.

---

# 98. PERGUNTA CENTRAL SOBRE PERSEGUIÇÃO

Responder:

> **Um personagem consegue transformar uma pista velha em investigação ativa e eventualmente gerar uma pista nova?**

---

# 99. PERGUNTA CENTRAL SOBRE CONTINUIDADE

Responder:

> **Quando a pista acaba, o personagem consegue parar de procurar sem esquecer por que estava procurando, e retomar quando surge informação nova?**

---

# 100. CRITÉRIO DE SUCESSO

A Fase 4.6 é bem-sucedida se:

- homicídio deliberado puder emergir;
- continuar raro;
- possuir causas rastreáveis;
- não depender de aumento de dano;
- incapacidade continuar protegendo conflitos comuns;
- perseguições produzirem investigação;
- pistas puderem evoluir;
- buscas puderem entrar em dormência;
- nova informação puder reativá-las;
- guardas puderem investigar ativamente;
- Commitments continuarem respeitando Needs;
- preparação não virar roteiro;
- as histórias apresentarem mais transformações e menos repetição.

---

# 101. NÃO USAR CONTAGEM DE MORTES COMO OBJETIVO

Não calibrar para:

“50 mortes”.

Não existe taxa ideal nesta fase.

A pergunta é:

**as mortes que acontecem possuem significado sistêmico?**

---

# 102. DARK FANTASY NÃO É MASSACRE ALEATÓRIO

O mundo deve poder ser:

- cruel;
- pobre;
- violento;
- vingativo;
- perigoso.

Mas isso precisa surgir de:

- condições;
- pessoas;
- escolhas;
- história.

Não de multiplicadores globais.

---

# 103. RESULTADO DESEJADO

Queremos personagens capazes de chegar a estados como:

**“eu não aceito mais isso.”**

E, dependendo de quem eles são:

- fugir;
- resistir;
- procurar;
- investigar;
- confrontar;
- ferir;
- perdoar;
- capturar;
- matar.

---

# 104. PRINCÍPIO DE PERSEGUIÇÃO

Uma pista não deve responder:

**“onde está o alvo?”**

Ela deve responder:

**“onde faz sentido procurar a próxima informação?”**

---

# 105. PRINCÍPIO DE INTENÇÃO LETAL

Matar não deve ser:

**uma versão mais forte de atacar.**

Matar deve ser:

**uma decisão sobre o desfecho desejado.**

---

# 106. PRINCÍPIO DE CONTINUIDADE

Não encontrar alguém hoje não significa esquecer.

Também não significa procurar para sempre.

Significa:

**“não consigo avançar agora.”**

---

# 107. PRINCÍPIO FINAL

A Fase 4.5 ensinou os NPCs a manter intenções.

A Fase 4.6 deve ensiná-los a:

**levar essas intenções até consequências reais.**

O ciclo desejado não é um roteiro, mas uma possibilidade emergente:

State  
→ Perception  
→ Knowledge  
→ Emotion  
→ Need  
→ Impulse  
→ Commitment  
→ Search/Action  
→ New Information  
→ Reassessment  
→ Escalation or De-escalation  
→ Consequence  
→ New State.

E, em situações raras e extremas:

**o NPC deve ser capaz de concluir que a morte de outro personagem é o resultado que ele deseja produzir.**

Quando isso acontecer, precisamos saber exatamente:

**por quê.**