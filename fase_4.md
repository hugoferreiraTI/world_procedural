# FASE 4 — INTERAÇÃO, COMBATE E RESPOSTA

Versão-base atual: `mvp-4-fase3.2-final`.

Esta é a primeira grande fase depois da estabilização econômica/social das Fases 3, correção alimentar e 3.2.

O foco agora muda.

Até aqui o mundo já consegue:

- perceber fatos;
- possuir conhecimento individual;
- formar necessidades;
- priorizar necessidades;
- avaliar soluções;
- executar ações;
- produzir consequências;
- manter relações;
- sentir luto;
- buscar familiares;
- investigar crimes;
- denunciar;
- ajudar;
- trabalhar;
- mudar de profissão;
- passar fome;
- sobreviver ou morrer por privação;
- gerar sucessão simples;
- produzir pequenas histórias causais.

Porém, a maior limitação atual é:

**os personagens ainda possuem poucas maneiras de RESPONDER materialmente uns aos outros.**

Um NPC pode ficar com raiva.

Pode querer vingança.

Pode saber quem roubou.

Pode investigar.

Pode denunciar.

Mas não pode:

- ameaçar;
- confrontar;
- atacar;
- defender;
- intervir;
- perseguir;
- render-se;
- capturar;
- ferir;
- matar;
- fugir para outra cidade;
- tornar-se procurado de verdade.

Da mesma forma, pobreza, humilhação, perda, desigualdade, fome e injustiça ainda possuem pouca capacidade de transformar permanentemente o comportamento individual.

A Fase 4 deve corrigir exatamente isso.

---

# 1. OBJETIVO CENTRAL

A Fase 4 se chama:

# INTERAÇÃO, COMBATE E RESPOSTA

O objetivo é ampliar drasticamente o vocabulário de ações e reações possíveis dos NPCs.

O mundo deve começar a produzir cadeias como:

NPC pobre
→ observa uma oportunidade
→ personalidade + conhecimento + necessidade + risco
→ decide roubar
→ vítima percebe
→ vítima reage
→ ladrão responde
→ confronto
→ fuga ou combate
→ ferimento ou morte
→ testemunha percebe
→ informação circula
→ criminoso passa a ser procurado
→ guarda tenta localizá-lo
→ família descobre a morte
→ luto
→ possível vingança
→ novas decisões.

IMPORTANTE:

NÃO implemente essa cadeia como roteiro.

Não exista:

`if poor: steal`
`if steal: victim_attack`
`if victim_dies: guard_chase`

Cada elo deve emergir dos sistemas já existentes.

O fluxo deve continuar:

State / Knowledge
→ Need
→ Priority
→ Solutions
→ Goal
→ Action
→ Consequence
→ Event
→ Perception / Knowledge
→ New Need
→ New decision.

---

# 2. PRINCÍPIO FUNDAMENTAL

A Fase 4 NÃO deve transformar NPCs em máquinas violentas.

Raiva != ataque.

Vingatividade != assassinato.

Pobreza != roubo.

Crime testemunhado != combate obrigatório.

Cada ação depende de:

- necessidade;
- prioridade;
- personalidade;
- estado emocional;
- relação;
- reputação;
- conhecimento;
- risco percebido;
- força percebida;
- recursos;
- presença de aliados;
- autoridade;
- medo;
- coragem;
- consequências esperadas;
- distância;
- oportunidade.

O mesmo fato deve poder produzir respostas diferentes.

Exemplo:

um NPC é roubado.

NPC A:
coragem alta
vingatividade alta
raiva alta
confia na própria força
→ confronta.

NPC B:
coragem baixa
confiança na guarda alta
→ denuncia.

NPC C:
medo alto
relação forte com o ladrão
→ evita confronto.

NPC D:
compaixão alta
percebe que o ladrão está faminto
→ pode não retaliar.

NPC E:
vingatividade alta
não sabe onde o ladrão está
→ procura/investiga.

A Fase 4 deve aumentar possibilidades.

Não diminuir decisões a um único comportamento correto.

---

# 3. NÃO CRIAR UM SEGUNDO SISTEMA DE IA

Preserve integralmente o modelo atual.

Não criar:

- Behaviour Tree paralelo;
- GOAP paralelo;
- CombatAI separado que ignora NeedSystem;
- script de reação automática;
- sistema exclusivo para criminosos;
- sistema exclusivo para guardas.

Combate, fuga, perseguição, ameaça e defesa devem aparecer como:

SOLUTIONS

para necessidades existentes ou novas necessidades coerentes.

Exemplos:

`revenge`
pode produzir:

- investigar;
- denunciar;
- evitar;
- confrontar;
- ameaçar;
- atacar;
- perseguir.

`protection`
pode produzir:

- afastar-se;
- acompanhar;
- avisar;
- denunciar;
- proteger;
- intervir;
- enfrentar agressor.

`food`
ou `money`
podem, em condições extremas e personalidade compatível, permitir:

- pedir;
- trabalhar;
- coletar;
- vender;
- migrar;
- roubar.

Não transforme crime em necessidade independente quando ele é uma solução para outra pressão.

---

# 4. AUMENTO GRANDE DA POPULAÇÃO PERSISTENTE

A Fase 4 deve aumentar consideravelmente o número de NPCs reais/persistentes.

O mundo atual possui poucos personagens persistentes para o objetivo narrativo do projeto.

Mais personagens persistentes significam:

- mais relações;
- mais famílias;
- mais testemunhas;
- mais vítimas;
- mais criminosos;
- mais amigos;
- mais rivais;
- mais profissões;
- mais carreiras;
- mais conflitos;
- mais encontros;
- mais histórias concorrentes.

NÃO aumente:

- quantidade de reinos;
- quantidade de cidades;
- quantidade de vilas;
- tamanho do mapa;
- estrutura geográfica principal.

Mantenha o mesmo número de localidades e reinos.

Aumente a DENSIDADE HUMANA real.

---

# 5. REDUZIR POPULAÇÃO ABSTRATA

Hoje a população abstrata representa uma parcela excessivamente maior que o elenco persistente.

Isso deve mudar.

A população abstrata continua existindo porque é útil para:

- escala demográfica;
- consumo agregado;
- renda agregada;
- materialização eventual;
- representação de pessoas ainda não individualizadas.

Mas não deve representar dezenas de vezes mais pessoas que o elenco real.

Meta inicial de geração:

**para cada NPC persistente, aproximadamente 2 a 3 habitantes abstratos.**

Ou equivalentemente:

`abstract_population ≈ persistent_population × 2..3`

Não precisa ser exatamente igual em todas as cidades.

Capitais podem possuir maior parcela persistente.

Aldeias podem possuir proporção diferente.

Mas a ordem de grandeza deve permanecer próxima.

---

# 6. NÃO INFLAR A POPULAÇÃO TOTAL SEM NECESSIDADE

Preferencialmente, converta uma parcela da população atualmente abstrata em personagens persistentes durante a geração.

Preserve:

`TotalPopulation = PersistentAlive + AbstractPopulation`

sempre que possível.

O objetivo não é criar milhões de pessoas extras.

É individualizar uma parcela muito maior da população que já existe.

Aumente o elenco persistente inicial para pelo menos aproximadamente 3× o atual, se a população total das localidades permitir isso.

Uma faixa inicial desejável para esta geração é algo como:

**1.200–2.000 NPCs persistentes no mundo**

sem alterar quantidade de cidades/reinos.

Não force exatamente esse número se violar o censo existente.

A regra demográfica e a proporção abstrata/persistente são mais importantes que atingir um número artificial.

---

# 7. NOVOS NPCS PERSISTENTES DEVEM TER VIDA SOCIAL

Não gere centenas de NPCs isolados sem relações.

A geração ampliada deve continuar criando:

- famílias;
- casamentos;
- parentescos;
- amizades;
- profissões;
- local de residência;
- relações relevantes.

O grafo deve permanecer esparso e plausível.

Não conecte todos com todos.

O objetivo é aumentar a quantidade de redes locais.

Exemplo:

bairro/cidade:

família A
↔ amigos
↔ colegas
↔ comerciantes
↔ guardas
↔ rivais ocasionais.

Isso multiplica as possibilidades narrativas.

---

# 8. PERFORMANCE — EVITAR O(N²)

Com mais NPCs persistentes, não faça varreduras globais de todos contra todos.

Interações devem partir principalmente de:

- mesma localidade;
- mesma matriz;
- proximidade;
- relação conhecida;
- alvo conhecido;
- evento observado.

Use índices/buckets espaciais já existentes ou crie uma estrutura mínima de consulta local.

Não faça:

para cada NPC:
    verificar todos os NPCs do mundo.

Isso destruirá performance.

---

# 9. LOD DE SIMULAÇÃO PERSISTENTE

Todos os NPCs continuam sendo indivíduos reais.

Não transforme personagens distantes novamente em números abstratos.

Mas frequência de decisão pode variar.

Exemplo conceitual:

### ACTIVE

NPC:

- em combate;
- em perseguição;
- próximo do jogador;
- participando de evento social relevante;
- em crise vital.

Decisão:
aproximadamente 1h.

### LOCAL

NPC ativo na rotina normal.

Decisão:
3–6h conforme regras atuais.

### BACKGROUND PERSISTENT

NPC distante sem evento relevante.

Decisão:
6–12h ou atualização coerente equivalente.

IMPORTANTE:

fisiologia e eventos críticos continuam coerentes.

Um evento relevante deve poder PROMOVER imediatamente o personagem para simulação mais frequente.

Exemplo:

NPC distante recebe informação de que irmão morreu.

Não esperar 12h artificialmente se a arquitetura atual permite reação imediata ao evento.

O LOD reduz trabalho computacional.

Não elimina identidade ou causalidade.

---

# 10. ESTADOS EMOCIONAIS DINÂMICOS

Os 11 traços de personalidade atuais continuam existindo como BASE relativamente estável.

Não transforme personalidade em humor que muda 30 pontos por hora.

Adicione uma camada dinâmica de estado psicológico/social.

No mínimo considere:

- anger / raiva;
- resentment / ressentimento;
- humiliation / humilhação;
- desperation / desespero.

Grief já existe como necessidade/estado causal e deve conversar com essa camada.

---

# 11. PERSONALIDADE BASE VS ESTADO ATUAL

Conceitualmente:

`EffectiveBehavior = PersonalityBaseline + EmotionalState + Context`

Exemplo:

NPC normalmente:

vingatividade = 35.

Depois de:

- ser roubado;
- ser humilhado;
- perder familiar;
- sofrer agressão;

pode possuir:

resentment = 70
anger = 80.

Ele continua sendo uma pessoa com vingatividade-base 35.

Mas temporariamente suas decisões podem ficar muito mais agressivas.

Com o tempo:

- raiva pode cair;
- ressentimento pode durar mais;
- reconciliação pode diminuir;
- justiça/reparação pode diminuir;
- nova agressão pode aumentar.

---

# 12. ALTERAÇÃO LENTA DA PERSONALIDADE

Experiências repetidas e persistentes PODEM alterar lentamente alguns traços-base.

Mas isso deve acontecer devagar.

Não:

roubo sofrido
→ vingatividade +30.

Pode existir algo como:

meses de:

- humilhação;
- violência;
- privação;
- repetidas traições;

→ pequena alteração acumulada em:

- vingatividade;
- confiança;
- temperamento;
- independência;
- compaixão.

Use limites.

Personalidade deve possuir história.

Não ruído.

---

# 13. RAIVA

Raiva deve ser um estado dinâmico 0–100 ou equivalente.

Pode aumentar por:

- agressão sofrida;
- roubo;
- humilhação;
- perda causada por alguém;
- ameaça;
- repetidas frustrações;
- injustiça percebida;
- privação prolongada;
- dano a familiar;
- traição;
- derrota pública.

Pode diminuir por:

- tempo;
- reparação;
- ajuda;
- reconciliação;
- distância do conflito;
- punição percebida do responsável;
- apoio social.

Raiva NÃO escolhe ação diretamente.

Ela altera:

- prioridade;
- Utility;
- tolerância ao risco;
- valor de confrontar;
- valor de retaliar;
- valor de fugir;
- interpretação social.

---

# 14. HUMILHAÇÃO

Humilhação deve representar principalmente situações sociais.

Exemplos:

- derrota pública;
- ameaça pública;
- ser roubado diante de outros;
- insulto;
- rejeição social grave;
- submissão forçada;
- derrota em confronto;
- punição pública.

Humilhação pode:

- aumentar raiva;
- aumentar ressentimento;
- aumentar necessidade de reconhecimento;
- aumentar desejo de reparação;
- diminuir confiança;
- em algumas personalidades, aumentar fuga/evitação.

Não faça toda humilhação gerar violência.

---

# 15. DESESPERO

Desespero representa pressão persistente sem solução.

Pode aumentar com:

- fome recorrente;
- pobreza longa;
- desemprego;
- perda de família;
- fracassos repetidos;
- ausência de apoio;
- luto prolongado;
- perseguição;
- isolamento.

Pode diminuir com:

- comida;
- renda;
- ajuda;
- companhia;
- mudança de cidade;
- solução do problema;
- recuperação material.

Desespero pode alterar Utility de:

- crime;
- migração;
- pedido de ajuda;
- abandono de objetivo;
- comportamento arriscado.

---

# 16. RESSENTIMENTO COM ALVO

Além de raiva geral, permita ressentimento ligado a um alvo.

Pode ser:

- pessoa;
- grupo;
- autoridade;
- cidade;
- reino.

Mas SOMENTE quando o NPC possui conhecimento para atribuir causa.

Exemplo:

NPC pobre numa cidade rica NÃO deve automaticamente odiar o rei.

Ele precisa:

- conhecer a riqueza;
- perceber sua própria situação;
- atribuir responsabilidade;
- ouvir informação/propaganda;
- observar ação institucional.

Crie a base de:

`Grievance`

ou estrutura equivalente:

- target;
- cause;
- intensity;
- created_at;
- last_reinforced;
- known_fact/source.

NÃO implemente revolução ainda.

Essa estrutura será matéria-prima da Fase 5.

---

# 17. INTERAÇÕES SOCIAIS NOVAS

Amplie o repertório de ações possíveis.

Inclua quando coerente:

- confrontar;
- ameaçar;
- exigir devolução;
- advertir;
- intimidar;
- insultar/provocar;
- pedir desculpas;
- recuar;
- render-se;
- intervir;
- defender;
- pedir ajuda imediata;
- alertar terceiros;
- tentar acalmar;
- perdoar/encerrar conflito quando personalidade/contexto permitirem.

Não transforme diálogo em LLM.

Essas continuam sendo ações estruturadas.

A camada textual apenas descreve.

---

# 18. CRIME COMO AÇÃO EMERGENTE

Roubo já existe.

A Fase 4 deve integrá-lo melhor às necessidades.

Exemplo:

NPC com:

- fome;
- pobreza;
- poucas oportunidades;
- honestidade baixa;
- ganância alta;
- desespero;
- risco percebido baixo;

pode considerar roubo.

NPC rico e ganancioso também pode roubar.

Não faça pobreza ser requisito.

Não faça pobreza automaticamente gerar crime.

Utility deve considerar:

- valor esperado;
- necessidade;
- personalidade;
- risco;
- testemunhas;
- reputação;
- relação com vítima;
- autoridade presente;
- consequência conhecida.

---

# 19. A VÍTIMA PRECISA RESPONDER

Hoje um roubo pode gerar conhecimento/reputação/reparação.

Na Fase 4 a vítima deve possuir mais alternativas.

Ao perceber o roubo:

- ignorar;
- evitar;
- exigir devolução;
- confrontar;
- ameaçar;
- denunciar;
- chamar guarda;
- perseguir;
- atacar;
- pedir ajuda;
- fugir.

A resposta depende da vítima.

Não existe reação universal.

---

# 20. TESTEMUNHAS

Toda agressão, crime ou morte deve gerar percepção SOMENTE para quem realmente pode perceber.

Não use conhecimento global.

Considere:

- mesma posição/local;
- proximidade;
- presença;
- visibilidade disponível no modelo;
- evento audível se existir conceito equivalente.

Testemunha pode aprender:

- ator;
- vítima;
- tipo de ação;
- local;
- turno;
- resultado.

Confiança depende da percepção.

---

# 21. TESTEMUNHA TAMBÉM É AGENTE

Testemunha não serve apenas para espalhar rumor.

Ela pode reagir.

Dependendo de:

- profissão;
- coragem;
- relação com vítima;
- relação com agressor;
- lealdade;
- medo;
- personalidade;
- força percebida.

Pode:

- fugir;
- denunciar;
- ajudar vítima;
- intervir;
- atacar agressor;
- seguir agressor;
- prestar primeiros socorros;
- contar para familiar;
- ignorar.

---

# 22. COMBATE LOCAL

Implemente combate entre personagens.

O objetivo desta fase NÃO é criar um sistema tático complexo.

Não implemente ainda:

- membros individuais;
- dezenas de tipos de dano;
- magia;
- exércitos;
- formações;
- cerco;
- guerra.

Crie combate local simples e causal.

---

# 23. AÇÕES DE COMBATE

No mínimo:

- attack;
- defend;
- flee;
- surrender;
- intervene/protect.

Outras podem surgir se já encaixarem na arquitetura.

Cada ação deve consumir tempo.

Combate não ocorre fora do fluxo normal do mundo.

---

# 24. ENTRADA EM COMBATE

Um personagem não entra em combate apenas porque existe hostilidade.

Antes de escolher ataque, considerar:

- necessidade;
- raiva;
- vingatividade;
- coragem;
- medo;
- relação;
- reputação;
- força própria conhecida;
- força do alvo percebida;
- número de aliados;
- número de inimigos;
- saúde;
- arma;
- possibilidade de fuga;
- presença de guarda;
- possíveis consequências.

Um NPC muito vingativo pode ainda decidir:

“ele é forte demais.”

e fugir/denunciar.

---

# 25. FORÇA PERCEBIDA

Mantenha separação:

OBJECTIVE STRENGTH

vs

PERCEIVED STRENGTH.

NPC não deve acessar estatísticas escondidas de outro NPC sem motivo.

Pode inferir por:

- aparência/equipamento observável;
- reputação;
- confronto anterior;
- testemunho;
- estado físico visível.

Isso permite erro.

Um NPC pode subestimar alguém.

---

# 26. RESOLUÇÃO DE COMBATE

Use HP existente.

Implemente fórmula simples, documentada e configurável.

Considere:

- saúde;
- arma carregada/equipada;
- qualidade da arma;
- força base se já houver atributo aplicável;
- estado de ferimento;
- defesa;
- pequena aleatoriedade determinística.

Se não existir atributo físico adequado, não invente um sistema enorme de RPG.

Crie somente o necessário.

Não faça personalidade aumentar dano diretamente.

Coragem influencia decisão.

Não necessariamente força física.

---

# 27. ARMAS

Itens já possuem dados e armas já existem como objetos/base.

Faça armas terem função mínima no combate.

Pode existir:

- unarmed;
- arma simples;
- arma melhor.

Use propriedades existentes quando possível.

Não implemente ainda:

- sistema complexo de equipamentos;
- slots corporais extensos;
- encantamento;
- dezenas de efeitos.

O objetivo é consequência física, não loot-RPG.

---

# 28. FERIMENTOS

Além de HP, adicione um estado simples de ferimento.

Por exemplo:

- light;
- moderate;
- severe.

Ou modelo equivalente.

Ferimento pode afetar:

- movimento;
- trabalho;
- combate;
- prioridade de procurar ajuda;
- capacidade de fugir.

Não implemente sistema anatômico detalhado.

---

# 29. TRATAMENTO

NPC ferido pode gerar necessidade de tratamento.

Soluções possíveis:

- descansar;
- procurar curandeiro;
- pedir ajuda;
- receber tratamento.

Use profissão de healer se já existir.

Não faça cura instantânea gratuita.

Tratamento consome:

- tempo;
- recurso se apropriado;
- disponibilidade.

Não transforme esta fase em sistema completo de medicina.

---

# 30. FUGA

Fugir deve ser uma ação real.

Pode ocorrer:

- antes do combate;
- durante combate;
- depois de testemunhar ameaça.

Sucesso depende de:

- distância;
- estado físico;
- perseguidor;
- contexto local;
- pequena aleatoriedade determinística.

Uma fuga pode encerrar combate sem resolver o conflito social.

---

# 31. RENDIÇÃO

Um personagem pode decidir render-se.

Influências:

- HP baixo;
- coragem;
- diferença de força;
- presença de guarda;
- relação;
- possibilidade percebida de sobreviver.

Rendição não significa morte automática.

Pode permitir:

- captura;
- multa;
- perda de item;
- fim temporário do confronto.

---

# 32. MORTE VIOLENTA

Ataque pode eventualmente causar morte.

Emita evento real.

Exemplo:

`CharacterKilled`

com:

- victim_id;
- killer_id;
- turn;
- location;
- cause;
- weapon/item se relevante;
- event_id.

Não altere cadáver/inventário de forma mágica.

Use sistema existente de morte/população.

---

# 33. MORTE DEVE DISPARAR SISTEMAS EXISTENTES

Quando ocorrer morte violenta:

- população é atualizada;
- relações continuam apontando para o morto;
- família pode entrar em luto quando souber;
- testemunhas aprendem;
- reputação reage;
- vingança pode surgir;
- sucessão pode ocorrer se for governante;
- necessidades em andamento são encerradas corretamente;
- cadáver permanece coerente;
- itens continuam reais.

Não crie um segundo caminho de morte exclusivo do combate.

Reutilize a morte já existente.

---

# 34. LUTO PODE GERAR RESPOSTAS DIFERENTES

Luto atualmente permite companhia/lembrança.

Mantenha isso.

Amplie possibilidades de acordo com contexto.

Se a morte possui responsável conhecido:

luto pode coexistir com:

- vingança;
- medo;
- proteção;
- busca de justiça.

Não transforme todo luto em vingança.

Personalidade e relação importam.

---

# 35. DESESPERO EXTREMO E MORTE AUTOCAUSADA

Permita, de forma rara e abstrata, que estados extremos de:

- luto prolongado;
- isolamento;
- desespero muito alto;
- repetidas perdas;
- ausência de suporte;
- personalidade/contexto compatíveis;

possam produzir uma ação autodestrutiva fatal.

IMPORTANTE:

- deve ser rara;
- nunca ser resposta padrão ao luto;
- não usar detalhes de método;
- não descrever procedimento;
- registrar apenas causa abstrata;
- relações protetoras e apoio devem reduzir fortemente a probabilidade/Utility;
- companhia, ajuda e melhora material devem poder retirar essa solução.

Isso existe como possibilidade narrativa grave, não como punição automática.

Evento final pode usar causa abstrata como `self_harm` ou equivalente.

---

# 36. PERSEGUIÇÃO E STATUS DE PROCURADO

Implemente uma versão inicial de perseguição criminal.

NÃO é ainda sistema judicial completo.

Crie estrutura equivalente a:

`WantedRecord`

com:

- suspect_id;
- jurisdiction/locality;
- originating_fact/event;
- severity;
- evidence/confidence;
- created_at;
- active/resolved;
- last_known_location.

Uma pessoa só se torna procurada se autoridade apropriada obtiver conhecimento/evidência suficiente segundo regras locais.

Auditor saber ≠ guarda saber.

---

# 37. GUARDA COMO AGENTE DE PERSEGUIÇÃO

Guarda que conhece um `WantedRecord` pode gerar necessidade institucional/pessoal de:

- localizar;
- perseguir;
- confrontar;
- capturar.

Não teleporte o guarda.

Não use localização global do criminoso.

Use:

- última localização conhecida;
- informação;
- testemunhas;
- observação.

---

# 38. CAPTURA

Implemente consequência mínima de captura.

Não crie sistema judicial completo.

Possibilidades:

- rendição;
- derrota sem morte;
- detenção temporária;
- aplicação da multa existente;
- perda/retorno de item roubado quando rastreável;
- liberação posterior.

Não implemente ainda:

- tribunal complexo;
- prisão de anos;
- sistema legal completo.

Mas perseguição precisa possuir um desfecho além de apenas “encontrou”.

---

# 39. CRIMINOSO PODE FUGIR DA CIDADE

Implemente MIGRAÇÃO AUTÔNOMA INDIVIDUAL BÁSICA.

Ela é necessária nesta fase porque fugir é uma resposta concreta.

NPC pode considerar mudança de cidade por:

- perseguição;
- pobreza persistente;
- falta de trabalho;
- ameaça;
- violência;
- perda familiar;
- oportunidade conhecida;
- relação em outro local.

Não crie caravanas.

Não crie comércio intermunicipal.

Não crie migração em massa.

É decisão individual.

---

# 40. DESTINO DE MIGRAÇÃO

NPC NÃO conhece todas as cidades magicamente.

Pode escolher entre localidades conhecidas por:

- viagens anteriores;
- informação;
- família;
- profissão;
- rumores confiáveis;
- relações.

Utility do destino pode considerar:

- segurança percebida;
- trabalho conhecido;
- família;
- reputação;
- distância;
- perseguição;
- custo da viagem;
- reserva.

Migração deve usar deslocamento real.

---

# 41. MUDANÇA DE RESIDÊNCIA

Chegar a outra cidade NÃO significa automaticamente mudar residência.

Pode existir:

- visitante;
- refugiado/fugitivo temporário;
- residente novo.

Após permanência ou decisão adequada, pode atualizar `town_id`/residência segundo invariantes populacionais.

A transferência precisa preservar censo:

origem perde residente;
destino ganha residente;

sem criar pessoa nova.

---

# 42. RAIVA, POBREZA E POLÍTICA FUTURA

NÃO implemente revolução nesta fase.

NÃO implemente golpe.

NÃO implemente facção revolucionária completa.

Mas preserve o material necessário.

Exemplo futuro:

cidade possui muita riqueza
+
NPC sofre privação
+
NPC conhece essa concentração
+
atribui responsabilidade ao governo
+
ressentimento alto
+
raiva alta
+
outros compartilham fatos
→ possível pressão política.

Na Fase 5 isso poderá gerar:

- movimento;
- facção;
- protesto;
- apoio a pretendente;
- deposição;
- guerra civil.

Agora apenas:

- estados;
- fatos;
- grievances;
- relações;
- causas.

---

# 43. NÃO ATRIBUIR CULPA POLÍTICA MAGICAMENTE

Um NPC pobre não sabe automaticamente:

“o rei acumula riqueza.”

O NPC precisa:

- ver;
- ouvir;
- aprender;
- inferir por regra permitida.

Fatos possíveis:

- tesouro conhecido;
- imposto conhecido;
- ajuda recusada;
- riqueza pública visível;
- propaganda futura;
- testemunho.

Sem conhecimento:

não existe ressentimento direcionado ao rei.

Pode existir raiva geral/desespero.

---

# 44. FUTURA TOMADA DE PODER

Prepare a arquitetura para uma futura necessidade coletiva/individual semelhante a:

`change_ruler`
`seek_power`
`challenge_rule`

mas NÃO execute golpe nesta fase.

Ambição + ressentimento + legitimidade + apoio serão usados depois.

Não crie agora:

`if anger > 90: overthrow king`.

Isso seria exatamente o tipo de regra especial que este projeto evita.

---

# 45. INTERAÇÕES DEVEM GERAR NOVAS INTERAÇÕES

A principal métrica qualitativa desta fase é:

**uma ação gerar novas possibilidades reais para terceiros.**

Exemplo:

roubo
→ vítima reage
→ testemunha reage
→ confronto
→ ferimento
→ healer entra
→ guarda aprende
→ perseguição
→ fuga
→ familiar procura
→ rumor
→ reputação.

Não precisa acontecer tudo.

Mas o sistema precisa permitir que consequências abram novos ramos.

---

# 46. INTERVENÇÃO DE TERCEIROS

Se dois NPCs entram em conflito e terceiros estão presentes:

eles não devem ser decoração.

Podem avaliar:

- ajudar amigo;
- ajudar vítima;
- ajudar agressor;
- fugir;
- chamar guarda;
- tentar interromper;
- observar.

Isso depende de:

- relação;
- coragem;
- lealdade;
- reputação;
- conhecimento;
- medo.

---

# 47. COMBATE EM GRUPO PEQUENO

Permita múltiplos participantes locais.

Não implemente exército.

Mas situações como:

2 amigos defendendo 1 pessoa contra agressor

devem ser possíveis.

Evite resolver tudo como duelo isolado se existem participantes reais.

---

# 48. REPUTAÇÃO DE VIOLÊNCIA

Eventos físicos devem alimentar reputação existente.

Exemplos de tags/conceitos:

- violento;
- perigoso;
- assassino;
- covarde;
- protetor;
- corajoso;
- ladrão.

Use sistema contextual existente.

Não crie um número global universal.

Uma pessoa pode ser:

“protetor”

para uma família,

e:

“assassino”

para outra.

---

# 49. CONHECIMENTO DA CULPA

Uma morte violenta não significa que todos sabem quem matou.

Pode existir:

- testemunha direta;
- corpo encontrado sem culpado conhecido;
- rumor;
- acusação errada futura;
- suspeito conhecido.

Isso é extremamente importante.

Use FactID/EventID existentes.

---

# 50. NECESSIDADE DE VINGANÇA DEVE CONSIDERAR CULPA CONHECIDA

Se familiar encontra corpo sem saber autor:

não pode imediatamente atacar o assassino verdadeiro.

Pode:

- investigar;
- perguntar;
- procurar testemunha;
- buscar autoridade.

Somente depois de adquirir informação pode direcionar vingança.

---

# 51. NÃO IMPLEMENTAR PROPAGAÇÃO GLOBAL INSTANTÂNEA

Crime em cidade A não vira automaticamente conhecimento de cidade B.

Se criminoso migra:

pode escapar temporariamente da perseguição.

Futuramente informação poderá viajar por:

- pessoas;
- autoridades;
- caravanas;
- política.

Nesta fase use somente caminhos existentes/locais e migração individual.

---

# 52. NECESSIDADES E AÇÕES NOVAS

Revise quais comportamentos são:

NEED

vs

SOLUTION

vs

ACTION

vs

CONSEQUENCE.

Não transforme toda ação nova em nova Need.

Exemplo:

`attack`

é ACTION/SOLUTION.

Não necessariamente Need.

`anger`

é STATE/MODIFIER.

Não Need por si só.

`revenge`

já é Need.

`wanted`

é STATUS/KNOWLEDGE institucional.

`pursuit` pode ser Need/Goal institucional ou resposta de proteção/reparação.

Documente essa classificação.

---

# 53. TESTES — NOVA FILOSOFIA

A partir desta fase, REDUZA o tempo gasto criando baterias enormes de testes.

O projeto possui 179 testes acumulados.

Não quero outra fase com dezenas e dezenas de testes triviais que consomem mais tempo que implementação e observação do mundo.

Durante desenvolvimento:

rode SOMENTE testes diretamente relacionados ao módulo alterado.

Ao final:

rode a suíte anterior completa uma vez.

Adicione somente regressões de alto valor.

Meta aproximada:

**10–20 novos testes direcionados**, não 40–60.

Se algum bug real aparecer na auditoria:

adicione regressão específica.

Não crie teste para cada combinação teórica possível.

---

# 54. TESTES ESSENCIAIS DE COMBATE

Cubra apenas invariantes essenciais:

1. ataque causa dano real;
2. morte reutiliza sistema existente;
3. morto não age;
4. testemunha aprende somente se puder perceber;
5. NPC sem conhecimento não conhece assassino;
6. fuga pode terminar confronto;
7. rendição pode impedir continuação do ataque;
8. defensor/interveniente pode entrar no conflito;
9. save/load preserva combate/status;
10. mesma seed/estado produz mesma resolução.

---

# 55. TESTES ESSENCIAIS DE RESPOSTA

Adicionar regressões para:

- roubo percebido cria opções de reação;
- vítima pode denunciar sem atacar;
- vítima agressiva pode confrontar;
- guarda com informação válida persegue;
- guarda sem informação não sabe magicamente;
- criminoso pode fugir;
- morte conhecida gera luto;
- morte com culpado conhecido pode gerar vingança;
- morte sem culpado conhecido não aponta para assassino real.

Não testar todas as personalidades.

Use alguns cenários representativos.

---

# 56. TESTES ESSENCIAIS EMOCIONAIS

Testar:

- agressão aumenta raiva;
- reparação reduz parte da pressão;
- raiva decai;
- humilhação não modifica instantaneamente personalidade-base em dezenas de pontos;
- experiências prolongadas podem produzir pequena alteração persistente;
- grievance mantém alvo/fonte causal;
- NPC não cria grievance direcionado sem conhecimento da causa.

---

# 57. TESTE DE POPULAÇÃO

Verificar:

- proporção persistente/abstrata;
- invariantes;
- mesma quantidade de cidades/reinos;
- nenhuma duplicação de residente;
- morte reduz total corretamente;
- migração transfere residência sem criar pessoa;
- população abstrata não fica negativa.

Não precisa criar dezenas de testes.

Um conjunto pequeno basta.

---

# 58. UMA ÚNICA AUDITORIA LONGA PRINCIPAL

NÃO execute novamente três campanhas completas de 10.000 horas.

Nesta fase quero mais tempo gasto:

- implementando;
- observando;
- jogando;
- corrigindo comportamento real.

Faça:

### Desenvolvimento

microcenários direcionados.

### Depois

uma auditoria curta de aproximadamente 500–1.000 horas para verificar:

- performance;
- crashes;
- violência absurda;
- loops;
- genocídio acidental;
- NPCs atacando todos;
- perseguição infinita.

Corrija bugs estruturais.

### Final

UMA campanha principal:

**modo mundo / espectador global**
**10.000 horas**

Escolha uma seed canônica já utilizada, preferencialmente Mira.

Essa será a auditoria longa oficial da Fase 4.

---

# 59. PERFIL DE PERFORMANCE

Como a população persistente aumentará muito, execute um benchmark simples.

Registrar:

- NPCs persistentes iniciais;
- abstratos;
- decisões processadas;
- eventos;
- tempo real por 1.000 horas;
- memória aproximada;
- tamanho do save;
- tempo de save/load.

Não transforme isso num projeto de benchmark.

Um relatório simples basta.

Se houver O(N²) evidente:

corrija.

---

# 60. MÉTRICAS DA CAMPANHA DE 10.000H

Registrar:

### População

- persistentes iniciais;
- abstratos;
- vivos;
- mortos;
- migrados;
- cidades;
- reinos.

### Emoções

- raiva média;
- NPCs com raiva alta;
- grievances;
- humilhações;
- desespero;
- causas principais.

Não use média isolada como qualidade.

### Crime

- roubos;
- crimes testemunhados;
- confrontos;
- denúncias;
- procurados;
- perseguições;
- capturas;
- fugitivos.

### Combate

- confrontos iniciados;
- confrontos encerrados por fuga;
- por rendição;
- por incapacidade;
- mortes;
- feridos;
- intervenções de terceiros;
- vítimas protegidas.

### Social

- luto;
- vingança;
- ajuda;
- proteção;
- investigações;
- rumores/informação;
- mudanças de reputação.

### Migração

- migrações;
- motivo;
- origem;
- destino;
- criminosos fugindo;
- pobres procurando oportunidade;
- familiares mudando.

---

# 61. EVITAR MASSACRE SISTÊMICO

Após adicionar combate, observe cuidadosamente:

- taxa de morte;
- taxa de ataque;
- conflitos por NPC;
- duração;
- repetição entre mesmas pessoas.

Se metade da população morrer por brigas em poucos meses:

isso provavelmente é problema de Utility/prioridade.

Não “resolva” diminuindo dano imediatamente.

Primeiro descubra:

- por que tantos atacam;
- por que não fogem;
- por que não se rendem;
- por que terceiros não intervêm;
- por que conflito não se encerra.

---

# 62. EVITAR PACIFISMO SISTÊMICO

O inverso também importa.

Se 10.000 horas produzem:

- milhares de roubos;
- centenas de vinganças;
- zero ataques;

a nova ação existe, mas não participa realmente das escolhas.

Investigue:

- Utility;
- risco;
- personalidade;
- conhecimento;
- prioridade;
- oportunidades.

Não force ataques por quota.

---

# 63. HISTÓRIAS EMERGENTES — FOCO PRINCIPAL DO RELATÓRIO

O relatório final deve dar MUITO espaço para histórias.

Procure ativamente cadeias reais como:

- roubo → reação → combate;
- combate → testemunha → denúncia;
- assassinato → luto → vingança;
- perseguição → fuga → migração;
- pobreza → crime;
- pobreza → migração;
- humilhação → ressentimento → confronto;
- amizade → intervenção;
- família → proteção;
- criminoso morto pela vítima;
- vítima morta pelo ladrão;
- guarda perseguindo criminoso;
- testemunha salvando alguém;
- agressor arrependendo/recuando;
- NPC rendendo-se;
- inimigos evitando confronto por medo;
- pessoa ajudando inimigo ferido;
- carreira interrompida por conflito;
- morte alterando sucessão;
- crime não resolvido;
- acusação sem culpado conhecido.

Não invente nenhuma dessas.

Só mostre se acontecer.

---

# 64. HISTÓRIAS LONGAS

Dê prioridade especial para histórias que cruzam sistemas.

Exemplo:

pobreza
→ roubo
→ testemunha
→ perseguição
→ migração
→ nova cidade
→ nova profissão.

Ou:

roubo
→ confronto
→ morte
→ família aprende
→ luto
→ vingança
→ perseguição.

Ou:

humilhação
→ ressentimento
→ ameaça
→ intervenção de amigo
→ reputação.

Essas são mais importantes que contabilizar 1.000 roubos isolados.

---

# 65. NÃO FORÇAR FINAL FELIZ

História pode acabar:

- sem resolução;
- criminoso escapando;
- vítima morrendo;
- guarda desistindo;
- família nunca descobrindo culpado;
- vingança expirando;
- personagem migrando.

Isso é válido.

---

# 66. NÃO FORÇAR DRAMA

Também registre histórias cotidianas.

Nem tudo precisa ser assassinato.

Exemplos:

- briga evitada;
- pedido de desculpas;
- amigo intervém;
- ladrão devolve;
- vítima perdoa;
- NPC foge;
- disputa termina sem violência.

O contraste deixa a violência mais significativa.

---

# 67. RELATÓRIO FINAL — ESTRUTURA

Produza:

1. Resumo executivo.
2. Comparação com `mvp-4-fase3.2-final`.
3. Sistemas reaproveitados.
4. População persistente nova.
5. Relação persistente/abstrata.
6. Performance.
7. LOD.
8. Estados emocionais.
9. Alteração lenta de personalidade.
10. Grievances.
11. Novas ações sociais.
12. Crime.
13. Reação da vítima.
14. Testemunhas.
15. Combate.
16. Ferimentos.
17. Tratamento.
18. Fuga/rendição.
19. Mortes violentas.
20. Perseguição.
21. Procurados.
22. Captura.
23. Migração.
24. Impacto em família/luto/vingança.
25. Impacto em reputação.
26. Testes direcionados.
27. Auditoria curta.
28. Auditoria global de 10.000h.
29. Métricas de interação.
30. Histórias emergentes.
31. Histórias longas.
32. Bugs descobertos.
33. Limitações.
34. Preparação para Fase 5.

---

# 68. COMPARAR DIRETAMENTE COM O RELATÓRIO ATUAL

O relatório atual informa que:

- combate NPC×NPC está ausente;
- combate do jogador está ausente;
- ferimentos estão ausentes;
- perseguição organizada está ausente;
- migração autônoma está ausente;
- facções ativas estão ausentes;
- política ampla está ausente;
- guerra está ausente;
- religião/deuses estão ausentes;
- população abstrata ainda possui papel grande;
- níveis de simulação ainda são simples;
- vingança existe sem violência;
- proteção existe sem defesa física;
- crime termina frequentemente em investigação/denúncia;
- sucessão existe, mas é simples.

A Fase 4 deve mudar especificamente:

### De ausente para implementado/parcial

- agressão local;
- combate local;
- ferimentos;
- defesa;
- fuga;
- perseguição;
- procurado;
- captura mínima;
- migração individual;
- reação de testemunhas;
- resposta física de proteção.

### Expandir

- personalidade/estado emocional;
- luto;
- vingança;
- reputação;
- criminalidade;
- conhecimento;
- interação.

### Não implementar ainda

- guerra;
- exércitos;
- cerco;
- diplomacia completa;
- revoluções;
- facções políticas completas;
- disputa formal pelo trono;
- deuses;
- religião completa;
- nascimento;
- envelhecimento;
- herança;
- caravanas;
- destruição de cidades.

Isso pertence à Fase 5 ou posteriores.

---

# 69. PREPARAÇÃO PARA FASE 5

A Fase 4 precisa deixar prontos os blocos causais que a Fase 5 poderá usar.

Especialmente:

- raiva;
- ressentimento;
- humilhação;
- grievances;
- violência;
- reputação;
- criminosos;
- perseguição;
- migração;
- desigualdade conhecida;
- mortes violentas;
- testemunhas;
- famílias afetadas;
- sucessões afetadas;
- concentração de riqueza observável.

Depois isso poderá alimentar:

- política;
- tomada de poder;
- facções;
- revoluções;
- guerra;
- religião;
- deuses;
- culto;
- propaganda;
- heróis;
- tiranos;
- rebeldes.

NÃO implemente essas consequências coletivas agora.

Apenas garanta que os fatos necessários existam e sejam persistidos.

---

# 70. CRITÉRIO FINAL DE QUALIDADE

A Fase 4 não será considerada boa porque:

- há muitos ataques;
- há muitas mortes;
- há muitos NPCs;
- há muitos eventos.

Será boa se o relatório conseguir responder:

“Por que isso aconteceu?”

E a resposta puder ser reconstruída como:

estado
→ percepção
→ conhecimento
→ necessidade
→ personalidade/emoção
→ prioridade
→ solução
→ ação
→ resposta de outro agente
→ consequência
→ nova necessidade.

O objetivo final é que NPCs deixem de apenas coexistir.

Eles devem começar a:

**afetar uns aos outros, responder uns aos outros e mudar por causa uns dos outros.**

Essa é a Fase 4.