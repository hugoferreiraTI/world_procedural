# FASE 3.2 — Reserva Preventiva, Acesso Econômico e Coerência Social

Antes de iniciar a Fase 4 e aumentar drasticamente a população persistente, estabilize os problemas locais identificados pela investigação da versão `mvp-4-alimentacao`.

Esta etapa ainda NÃO é a Fase 4.

Não aumente população, não implemente migração, não implemente guerra, política ampla, revoluções, religião, deuses, comércio entre cidades ou novos sistemas grandes.

O objetivo desta etapa é corrigir:

1. a baixa efetividade da reserva alimentar preventiva;
2. caminhos de renda existentes, mas semanticamente incorretos ou não executáveis;
3. interpretação incorreta de remuneração parcial;
4. anúncios de trabalho incompatíveis com capacidade real;
5. denúncia ao próprio culpado;
6. informação social velha/repetida sendo considerada útil;
7. alguns casos de intenção profissional incompatível com o local.

Preserve todos os sistemas atuais e trabalhe sobre eles.

---

# 1. PRINCÍPIO FUNDAMENTAL

Não transforme o mundo em uma economia perfeitamente eficiente.

O fato de uma cidade possuir muito dinheiro ou muita comida enquanto alguns habitantes permanecem pobres, frustrados ou insatisfeitos NÃO é necessariamente um erro.

Isso pode ser uma consequência social legítima e futuramente deverá servir de base para:

- insatisfação popular;
- conflito de classes;
- grupos revolucionários;
- grupos anti-Estado;
- revoltas;
- populismo;
- movimentos políticos;
- facções econômicas;
- crime organizado;
- radicalização;
- cultos;
- influência religiosa;
- manipulação por líderes;
- guerras civis.

Portanto:

**não tente fazer todo NPC ter emprego, dinheiro e comida garantidos.**

Também não tente distribuir automaticamente a riqueza municipal.

Desigualdade, desemprego, pobreza, estoque concentrado e saturação econômica podem existir legitimamente.

A tarefa desta fase é eliminar situações em que essas condições existem por causa de:

- interpretação errada de estado;
- oportunidade falsa;
- resultado produtivo considerado fracasso;
- prioridade preventiva estruturalmente incapaz de competir;
- informação semanticamente inútil considerada útil;
- ação social incoerente.

A economia deve poder gerar pobreza real.

Ela não deve gerar pobreza porque `2/6 de moeda == fracasso`.

A cidade pode ter comida enquanto alguns não conseguem comprá-la.

Isso pode ser socialmente interessante.

Mas deve acontecer porque:

- o NPC realmente não tem renda;
- oportunidades são escassas;
- sua profissão está saturada;
- ele não conhece outra oportunidade;
- há desigualdade;
- instituições não ajudam;
- ele tomou decisões ruins;
- relações sociais não ofereceram ajuda;
- mercado e estrutura local não resolveram o problema.

Não porque o motor interpretou incorretamente uma oportunidade real.

---

# 2. ARQUITETURA QUE DEVE SER PRESERVADA

Preserve:

State / Knowledge
→ Need
→ Priority
→ Solutions
→ Goal
→ Action
→ Consequence
→ New State.

Não crie:

- novo Utility AI;
- novo planejador paralelo;
- GOAP adicional;
- sistema econômico paralelo;
- controlador especial para fome;
- sistema social separado;
- dinheiro mágico;
- comida gratuita;
- roteiro para evitar pobreza;
- regra específica por personagem.

Todas as correções devem aproveitar os sistemas existentes.

---

# 3. ESTADO ATUAL CONFIRMADO

A alimentação emergencial foi corrigida na etapa anterior.

As três campanhas de 10.000 horas demonstraram:

- mortes totais: 690 → 331;
- mortes com fome no limite: 687 → 320;
- mortes carregando comida: 108 → 0;
- aquisições fatais na última decisão: 107 → 0;
- aumento de necessidades pessoais selecionadas;
- aumento de necessidades pessoais satisfeitas;
- redução moderada da seleção fisiológica.

Portanto:

NÃO desfaça as regras de emergência alimentar.

Preserve:

- interrupção vital;
- aquisição + refeição emergencial;
- prazo biológico;
- objetivo suspenso;
- prioridade vital acima do desempate por ID;
- distinção entre adquirir e consumir.

As 25 regressões alimentares novas devem permanecer passando.

---

# 4. PROBLEMA 1 — RESERVA PREVENTIVA EXISTE, MAS QUASE NUNCA VENCE

O diagnóstico demonstrou:

Prioridade atual da reserva:

`26 + 8 × déficit/alvo + 0,2 × min(fome,50) + bônus de idade`

O bônus de idade possui teto 8.

Consequência:

- prioridade máxima com reserva vazia ≈ 52;
- com uma ração para alvo de duas ≈ 48;
- o bônus temporal satura por volta de 54 horas.

Enquanto isso:

- renda pode chegar muito acima;
- trabalho pode passar de 60;
- descanso frequentemente supera;
- sede frequentemente supera;
- necessidades pessoais também podem superar.

Em 376.485 avaliações com reserva ativa, ela foi selecionada apenas 2.018 vezes: aproximadamente 0,54%.

Isso sozinho inclui estados emergenciais em que corretamente outra necessidade domina.

Mais importante:

com fome <50 e reserva insuficiente:

- 33.319 avaliações;
- reserva venceu apenas 1.805 vezes;
- aproximadamente 5,42%.

Descanso e água responderam por aproximadamente 78,61% das primeiras escolhas nessa janela preventiva.

Portanto o problema não é ausência de `food_reserve`.

O problema é que seu modelo de prioridade não representa adequadamente:

- cobertura restante;
- oportunidade atual;
- próxima oportunidade conhecida;
- custo de perder a oportunidade;
- tempo necessário para repor;
- proximidade de uma viagem;
- orçamento disponível;
- quantidade ainda necessária.

---

# 5. NÃO RESOLVER COM UM AUMENTO BRUTO DE PRIORIDADE

Não faça:

`food_reserve += 30`

ou qualquer outro número mágico equivalente.

Não queremos:

“tenho uma ração em vez de duas”
→ abandonar funeral;
→ abandonar busca familiar;
→ abandonar trabalho importante;
→ abandonar proteção;
→ abandonar investigação.

A manutenção de reserva deve continuar sendo preventiva, e não uma emergência permanente.

A prioridade deve crescer de forma contextual.

---

# 6. NOVA LÓGICA DE PRESSÃO PREVENTIVA

Reestruture a pressão de reserva usando conceitos equivalentes a:

- cobertura atual;
- déficit;
- próxima oportunidade conhecida;
- custo temporal da reposição;
- oportunidade presente;
- viagem planejada;
- distância conhecida;
- orçamento;
- idade da necessidade.

Conceitualmente:

`ReservePressure = CoverageRisk + OpportunityRisk + DeficitPressure + MildHunger + WaitingPressure`

Os nomes podem mudar.

Não transforme essa fórmula conceitual em uma implementação artificial apenas para reproduzir exatamente os nomes acima.

## CoverageRisk

Deve representar:

“quanto tempo minha reserva atual cobre?”

Zero rações deve ser mais preocupante que uma.

Uma ração deve continuar sendo considerada abaixo do alvo quando o alvo é duas.

Duas rações normais devem satisfazer a manutenção normal.

Uma viagem longa pode elevar o alvo já existente conforme as regras atuais.

## OpportunityRisk

Considere:

- existe mercado conhecido acessível agora?
- estou atualmente perto dele?
- tenho dinheiro?
- sei aproximadamente o preço?
- minha próxima oportunidade conhecida é distante?
- estou prestes a viajar?
- a reposição exige várias horas?
- a oferta conhecida pode expirar?

Perder uma oportunidade boa deve aumentar moderadamente a importância da reposição.

Isso NÃO significa conhecimento global.

O NPC usa apenas conhecimento próprio.

## WaitingPressure

A necessidade não deve simplesmente parar de crescer depois de ~54 horas.

Também não deve crescer infinitamente até virar emergência automática.

Use uma curva limitada ou contextual.

Uma necessidade antiga de reserva continuamente ignorada deve ganhar algum peso, especialmente quando continua sem cobertura adequada.

---

# 7. A SEGUNDA RAÇÃO É UM BUG CONCRETO

Hoje existe uma lacuna:

- alvo = 2;
- NPC possui 0;
- sem dinheiro;
- trabalho pode aparecer como alternativa para financiar comida.

Após conseguir 1 ração:

- ainda falta 1;
- porém alguns testes econômicos deixam de considerar insuficiência porque o NPC “possui comida”;
- trabalho desaparece do ramo de reserva.

Isso está errado.

A pergunta correta não é:

“Possui alguma comida?”

A pergunta correta é:

“Possui recursos suficientes para alcançar a reserva desejada?”

Exemplo:

ReserveTarget = 2  
Owned = 1  
Deficit = 1  
KnownUnitPrice = 4  
Money = 0

Existe déficit econômico conhecido de 4 moedas.

Isso pode tornar renda uma solução viável.

IMPORTANTE:

não significa que o NPC deve abandonar imediatamente tudo para trabalhar.

Significa apenas que trabalhar continua sendo uma alternativa válida para completar a reserva.

A PRIORIDADE decide se vale agir agora.

A SOLUÇÃO decide como agir caso essa necessidade seja escolhida.

Não misture os dois.

---

# 8. COMPRA DE RESERVA PODE SER PARCIAL

O alvo normal atual é duas rações.

Não exija compra completa de duas para considerar a ação válida.

Exemplos:

Meta: 2  
Possui: 0  
Dinheiro: suficiente para 1

→ comprar 1 é progresso legítimo.

Meta: 2  
Possui: 1  
Dinheiro: suficiente para 1

→ comprar a segunda é progresso legítimo.

Meta: 2  
Possui: 0  
Dinheiro: suficiente para 2  
mercado: suficiente

→ pode adquirir as duas se isso fizer sentido.

Se houver compra em lote, calcule o preço real de cada unidade conforme a economia.

Não faça simplesmente:

`preço_atual × quantidade`

se o preço depende de estoque/demanda e muda após cada unidade.

Cada transferência deve permanecer economicamente real.

Não permita:

- duplicação de item;
- compra sem estoque;
- compra sem dinheiro;
- preço ignorado;
- reserva infinita.

---

# 9. DINHEIRO MUNICIPAL CONCENTRADO NÃO É AUTOMATICAMENTE BUG

O diagnóstico final encontrou aproximadamente:

- dinheiro municipal total: 1.460.520;
- dinheiro dos NPCs vivos: 7.338;
- 411 NPCs pobres mesmo havendo comida e caixa municipal no mesmo mapa.

NÃO tente igualar essa distribuição automaticamente.

Essa desigualdade pode ser um estado social válido.

Uma cidade rica com trabalhadores pobres pode ser uma excelente fonte futura de:

- revolta;
- ressentimento;
- radicalização;
- crime;
- facções;
- greve;
- movimento anti-governo;
- apoio a pretendentes políticos;
- culto religioso;
- separatismo.

Na futura política, os NPCs devem poder perceber algo como:

“a cidade possui recursos”
+
“eu não consigo viver dignamente”
→ insatisfação.

Mas isso NÃO será implementado nesta fase.

Apenas preserve os dados que futuramente permitirão esse comportamento.

Não crie agora:

- satisfação política;
- ideologia;
- revolucionários;
- sindicatos;
- revolução;
- imposto;
- redistribuição.

Mas evite apagar as condições que um dia poderão gerá-los.

---

# 10. PROBLEMA 2 — PROFISSÃO SATURADA PODE GERAR POBREZA

Profissionais de produção dependem de estoque municipal.

Quando o estoque está saturado:

- produção deixa de ocorrer;
- corretamente não existe salário por produção inexistente;
- o trabalhador pode ficar sem renda.

No final das campanhas havia 133 NPCs pobres com profissão saturada.

Isso NÃO deve ser automaticamente eliminado.

É coerente que:

“ninguém precisa de mais madeira”
→ lenhador tenha menos trabalho.

Isso pode gerar:

- pobreza;
- mudança de profissão;
- procura por trabalho alternativo;
- futura migração;
- insatisfação;
- crime;
- futura ação política.

O erro seria o mundo oferecer trabalho que não existe ou interpretar atividade legítima incorretamente.

Portanto:

não obrigue a cidade a comprar produção inútil só para manter emprego.

Não pague salário por produto que não foi produzido.

Não aumente artificialmente limites de estoque para absorver tudo.

Procure tarefas locais compatíveis que representem demanda real.

Exemplos possíveis, apenas se já puderem ser representados de modo coerente:

- distribuição;
- processamento;
- manutenção;
- serviço temporário;
- transporte local;
- trabalho de apoio.

Toda tarefa deve:

- ter demanda;
- consumir tempo;
- possuir fonte real de pagamento;
- respeitar capacidade;
- respeitar recursos;
- poder terminar.

Se não houver trabalho real:

desemprego/subemprego é um estado válido.

---

# 11. BUG CONCRETO — PAGAMENTO FRACIONÁRIO SENDO TRATADO COMO FALHA

O sistema registra salário em sextos de moeda.

Exemplo confirmado:

NPC produz uma ração.

Recebe:

`2/6` de moeda como crédito.

Nenhuma moeda inteira é transferida ainda.

O executor observa:

`money_after == money_before`

e conclui:

“O trabalho não trouxe o pagamento necessário.”

Depois aplica cooldown de falha de 12 horas.

Isso é semanticamente incorreto.

O trabalho:

- aconteceu;
- produziu recurso;
- gerou crédito salarial;
- conservou dinheiro corretamente.

Portanto precisa haver distinção entre:

- trabalho sem produção;
- trabalho produtivo sem remuneração possível;
- trabalho produtivo com crédito parcial;
- trabalho produtivo com pagamento inteiro;
- trabalho realmente fracassado.

Pode usar enum/status/resultado estruturado.

Exemplo conceitual:

`WORK_FAILED_NO_INPUT`
`WORK_BLOCKED_SATURATED`
`WORK_SUCCESS_CREDIT`
`WORK_SUCCESS_PAID`
`WORK_FAILED_NO_PAYER`

Não é obrigatório usar esses nomes.

O importante é não tratar crédito legítimo como zero.

## Requisitos

Crédito parcial deve:

- permanecer persistido;
- acumular corretamente;
- converter em moeda inteira quando devido;
- não duplicar salário;
- não criar moeda;
- não ser perdido após save/load.

Cooldown de falha NÃO deve ser aplicado simplesmente porque ainda não houve moeda inteira.

Se houve produção legítima e crédito legítimo:

foi trabalho bem-sucedido.

---

# 12. PROBLEMA 3 — OFERTA TEMPORÁRIA PODE ESTAR ESGOTADA ANTES DE SER OFERECIDA

Atualmente trabalho temporário de distribuição pode ser anunciado mesmo quando a quota diária já foi consumida.

Foi reproduzido:

- 100 rações disponíveis;
- quota diária já atendida;
- solução ainda oferecida;
- execução falha depois.

Nas campanhas houve 129 falhas de “Não há refeições para distribuir”.

Corrija a coerência entre:

- oportunidade observada;
- oportunidade enumerada;
- oportunidade executada.

A observação/oferta deve considerar:

- quota restante naquele instante;
- estoque requerido;
- recursos;
- estrutura;
- capacidade.

Porém:

a oferta NÃO deve garantir execução futura.

Outro NPC pode chegar antes.

A quota pode acabar.

O estoque pode mudar.

Isso é comportamento emergente legítimo.

Portanto diferencie:

“oferta era falsa no momento em que foi observada”

de:

“oferta era verdadeira, mas deixou de existir antes da chegada.”

A segunda situação é válida.

Se possível, oportunidades conhecidas devem registrar:

- observed_at;
- local;
- tipo;
- capacidade restante observada;
- requisitos conhecidos.

Não transforme isso em conhecimento perfeito permanente.

---

# 13. PROFISSÕES INELEGÍVEIS PARA TRABALHO TEMPORÁRIO

Guardas, governantes, estudantes, conselheiros e outros podem não ser elegíveis para determinadas tarefas.

Não simplesmente torne todos elegíveis.

Essas diferenças podem ser socialmente interessantes.

Um governante pobre não precisa virar cozinheiro temporário por padrão.

Um guarda pode ter uma estrutura de remuneração diferente.

Um estudante pode depender de família, trabalho parcial ou outra oportunidade futura.

Nesta etapa:

verifique se cada profissão possui pelo menos caminhos coerentes que podem existir localmente.

Mas NÃO invente emprego apenas para impedir pobreza.

Se não houver oportunidade:

registre corretamente que não existe oportunidade executável.

Isso será informação útil para futuras necessidades de:

- mudança profissional;
- migração;
- crime;
- protesto;
- política.

---

# 14. INTENÇÕES PROFISSIONAIS INCOMPATÍVEIS COM O LOCAL

Foram encontrados líderes/caçadores cujo local de trabalho físico é um quartel, mas cuja profissão produtiva exige também estar no mapa municipal associado.

O sistema pode então:

- selecionar trabalho;
- caminhar até o local;
- estar fisicamente no local correto segundo um campo;
- ainda assim falhar porque economicamente está no mapa errado.

Não habilite acesso remoto ao mercado ou caixa natal para corrigir isso.

Resolva semanticamente.

Antes de oferecer trabalho, determine se:

- a atividade pode realmente ocorrer naquele local;
- há economia/estrutura local correspondente;
- há recursos;
- há pagador;
- há destino válido.

Se não:

não ofereça aquela solução ou explique o bloqueio correto.

Evite mensagem enganosa como:

“o local de trabalho ainda não foi alcançado”

quando o verdadeiro problema é:

“esta instalação não participa da economia produtiva exigida.”

---

# 15. BUG SOCIAL 1 — DENÚNCIA AO PRÓPRIO CULPADO

Isto é confirmado e frequente.

Nas três campanhas:

337 denúncias totais.

42 foram direcionadas ao próprio ator do crime.

12,46%.

Portanto não é um caso isolado.

## Problema atual

A candidatura procura:

“guarda conhecido/presente.”

Mas não exclui:

- culpado;
- ameaça;
- ator do fato;
- alvo da denúncia.

A execução também não revalida isso.

O sistema então:

- transmite a informação ao culpado;
- emite `ThreatReported`;
- marca como denunciado;
- satisfaz a necessidade.

Isso está errado semanticamente.

## Correção

Na candidatura:

um destinatário de denúncia independente NÃO pode ser:

- ator conhecido do crime;
- culpado/culprit conhecido;
- ameaça conhecida associada;
- alvo denunciado;
- o próprio denunciante quando semanticamente incompatível.

Na execução:

repita a validação.

Não confie apenas na candidatura porque conhecimento e estado podem mudar.

## Caso sem autoridade válida

Se o único guarda disponível for o próprio criminoso:

NÃO gere outro guarda.

NÃO escolha o criminoso.

NÃO satisfaça a necessidade.

A necessidade pode:

- permanecer ativa;
- ficar bloqueada;
- buscar informação;
- buscar outra autoridade conhecida;
- evitar o suspeito;
- expirar conforme regras existentes.

Futuramente isso poderá gerar:

- corrupção percebida;
- fuga;
- vigilantes;
- revolta;
- autoridade externa;
- facções.

Mas NÃO implemente essas consequências agora.

Se quiser futuramente existir:

“confrontar o próprio acusado”

isso deve ser uma Action semanticamente diferente de `denounce`.

---

# 16. BUG SOCIAL 2 — INFORMAÇÃO VELHA CONSIDERADA ÚTIL

Caso confirmado:

Arthus procura Iria.

Última observação mais recente: turno 364.

Nova ausência percebida: turno 400.

Marie transmite repetidamente fato de localização do turno 328.

Arthus já conhecia esse fato com confiança 100.

Mesmo assim:

- `InformationShared` é emitido;
- ação retorna sucesso;
- necessidade não avança;
- mesma informação pode ser pedida novamente.

## Problemas diferentes

Há três falhas aqui:

1. seleção da resposta não avalia utilidade contextual;
2. `KnowledgeSystem.learn()` retorna falso quando nada é aprendido;
3. `inform()` ignora isso e ainda retorna sucesso.

---

# 17. CRIAR AVALIAÇÃO PEQUENA E REUTILIZÁVEL DE UTILIDADE DA INFORMAÇÃO

Não crie um sistema gigantesco.

Crie uma pequena avaliação semântica compartilhada.

Conceitualmente:

`evaluate_information_utility(receiver, fact, context/need)`

Ela pode retornar categorias como:

- NEW_USEFUL_INFORMATION;
- BETTER_CONFIDENCE;
- ALREADY_KNOWN;
- STALE_FOR_CURRENT_NEED;
- IRRELEVANT;
- NO_INFORMATION.

Os nomes podem variar.

## Para busca por desaparecido

Uma informação de localização deve ser considerada útil se, por exemplo:

- é posterior à última observação relevante;
- ou é posterior ao início do episódio;
- ou fornece localização diferente e relevante;
- ou aumenta confiança de algo ainda incerto;
- ou altera concretamente a busca.

Um fato anterior à última vez em que o solicitante viu a pessoa normalmente não ajuda a localizar alguém que desapareceu depois disso.

## Cuidado

Não aplique uma regra genérica do tipo:

“fato antigo = inútil.”

Exemplo:

uma pessoa pode descobrir hoje que seu pai morreu meses atrás.

Isso continua sendo informação nova e relevante.

A utilidade depende do contexto da necessidade.

---

# 18. TRANSMISSÃO PRECISA TER RESULTADO HONESTO

Hoje:

`learn() == false`

pode terminar como:

“Informação transmitida.”

Isso deve ser corrigido.

Diferencie:

- informação aprendida;
- confiança aumentada;
- informação já conhecida;
- informação velha para aquela busca;
- informação irrelevante;
- interlocutor não sabe nada útil.

`InformationShared` pode continuar existindo como evento de comunicação, se semanticamente realmente houve conversa.

Mas isso NÃO deve automaticamente significar:

`NeedProgress = true`

ou:

`ActionSuccess = meaningful_success`.

Uma conversa pode acontecer e não ajudar.

Isso é válido.

---

# 19. EVITAR LOOP DE PERGUNTA INÚTIL

Se:

NPC A pergunta a B sobre C.

B responde fato X.

A já conhece X.

X não ajuda.

Então A não deveria perguntar novamente uma hora depois exatamente a mesma coisa esperando resultado diferente.

Guarde pequena memória de tentativas recentes associada a:

- necessidade;
- interlocutor;
- fato;
- resultado.

Ou mecanismo equivalente.

Não crie memória infinita.

Uma novidade real deve reabrir a oportunidade.

Exemplo:

turno 100:
Marie sabe somente fato antigo.
→ resposta inútil.

turno 120:
Marie vê Iria.
→ novo PersonLocated.

turno 121:
Arthus pode perguntar novamente.
→ agora existe informação útil.

---

# 20. ORDEM DE IMPLEMENTAÇÃO

Implemente nesta ordem:

## Etapa A — bugs sociais locais

1. destinatário válido de denúncia;
2. validação também na execução;
3. utilidade/novidade da informação;
4. retorno honesto de aprendizado;
5. prevenção de repetição inútil.

Motivo:

são bugs claros, locais e não dependem de rebalanceamento.

## Etapa B — semântica econômica

6. corrigir déficit da segunda ração;
7. compra parcial/lote limitado até alvo;
8. distinguir crédito salarial fracionário de falha;
9. remover cooldown incorreto após trabalho produtivo com crédito;
10. oferta temporária deve refletir quota/recursos atuais;
11. revalidar oferta na execução;
12. bloquear trabalho estruturalmente incompatível com o local.

## Etapa C — prevenção alimentar

13. substituir prioridade puramente estática por cobertura + oportunidade;
14. não remover continuidade global;
15. não transformar reserva em emergência permanente;
16. observar comportamento.

---

# 21. TESTES SOCIAIS OBRIGATÓRIOS

Preserve todos os 130 testes atuais.

Adicione regressões para:

### Denúncia

- culpado é guarda presente → não pode ser destinatário;
- existe outro guarda válido → outro pode receber denúncia;
- só existe guarda culpado → necessidade não é satisfeita artificialmente;
- culpa desconhecida → não excluir pessoa por informação que NPC não possui;
- culpa descoberta depois da candidatura → execução revalida;
- denúncia válida continua funcionando;
- save/load mantém estado corretamente.

### Informação

- fato já conhecido com mesma confiança → não conta como nova informação;
- fato com maior confiança → pode melhorar conhecimento;
- localização anterior à última observação → inútil para nova ausência;
- localização posterior à ausência → útil;
- morte antiga ainda desconhecida → pode continuar útil;
- resposta inútil não fecha necessidade;
- mesma resposta inútil não gera loop contínuo;
- nova informação posterior reabre interlocutor;
- eventos e reputação não são duplicados por repetição;
- quests existentes continuam funcionando.

---

# 22. TESTES ECONÔMICOS OBRIGATÓRIOS

### Reserva

- alvo 2, possui 0, sem dinheiro → trabalho pode financiar reserva;
- alvo 2, possui 1, sem dinheiro → trabalho ainda pode financiar segunda;
- alvo 2, possui 2 → não há déficit normal;
- dinheiro para apenas 1 → compra parcial legítima;
- dinheiro para 2 → pode completar alvo;
- compra respeita curva real de preço;
- estoque insuficiente limita quantidade;
- não há duplicação monetária ou de itens.

### Crédito salarial

- produção legítima gera 2/6 → trabalho é sucesso;
- nenhuma moeda inteira transferida → crédito permanece;
- seis sextos acumulados → uma moeda real transferida;
- crédito não duplica;
- save/load preserva crédito;
- trabalho realmente sem produção continua falhando;
- trabalho bloqueado por estoque distingue saturação.

### Trabalho temporário

- quota zero no momento da observação → não oferecer como disponível;
- quota positiva → oferta pode existir;
- outro NPC consome quota antes → execução pode falhar honestamente;
- estoque desaparece antes → execução falha sem inventar item;
- remuneração usa estoque/dinheiro reais;
- oferta expirada não permanece conhecimento perfeito.

### Local profissional

- local físico correto mas economia incompatível → não oferecer ação impossível;
- local/economia válidos → trabalho funciona;
- sem acesso remoto a caixa/mercado natal.

---

# 23. TESTES DA NOVA PRIORIDADE PREVENTIVA

Crie cenários controlados.

### Caso 1

fome 20  
0 rações  
mercado ao lado  
dinheiro suficiente  
nenhuma emergência

Resultado desejado:

reserva possui pressão relevante e pode ser escolhida.

Não precisa obrigatoriamente vencer toda necessidade pessoal.

### Caso 2

fome 20  
1 ração  
alvo 2  
mercado ao lado  
dinheiro suficiente

Resultado:

segunda ração é uma oportunidade preventiva legítima.

### Caso 3

fome 20  
1 ração  
funeral/luto de alta prioridade

Resultado:

a manutenção preventiva NÃO deve necessariamente destruir o objetivo social.

### Caso 4

fome 25  
0 rações  
viagem conhecida longa prestes a iniciar

Resultado:

cobertura/oportunidade elevam fortemente a reserva.

### Caso 5

fome 25  
0 rações  
mercado disponível agora  
próxima oportunidade conhecida muito distante

Resultado:

reserva ganha pressão adicional.

### Caso 6

fome 25  
0 rações  
sem dinheiro e sem trabalho real

Resultado:

não fingir que existe solução.

### Caso 7

fome 25  
reserva insuficiente  
sono crítico

Resultado:

sono ainda pode vencer quando biologicamente necessário.

### Caso 8

sede crítica

Resultado:

sede pode corretamente superar manutenção alimentar.

---

# 24. NÃO ALTERAR NESTA ETAPA

Não:

- aumentar população;
- reduzir população abstrata;
- implementar LOD;
- implementar migração;
- implementar cidade falida;
- implementar caravanas;
- criar revoltas;
- criar movimentos anti-Estado;
- implementar política;
- implementar ideologia;
- implementar guerra;
- implementar deuses;
- implementar religião;
- implementar impostos;
- redistribuir riqueza automaticamente;
- criar renda universal;
- criar comida grátis;
- reduzir fome;
- reduzir dano;
- aumentar HP;
- aumentar estoque artificialmente;
- forçar profissão;
- gerar NPC para preencher emprego;
- alterar nascimento/envelhecimento.

Esses sistemas pertencem a fases futuras.

---

# 25. PRESERVAR DESIGUALDADE COMO INFORMAÇÃO FUTURA

Adicione instrumentação suficiente para futuramente sistemas políticos poderem observar desigualdade.

NÃO implemente reação política ainda.

Se já houver métricas adequadas, apenas preserve.

Seria útil poder obter futuramente por localidade:

- riqueza municipal;
- riqueza média/mediana dos residentes;
- quantidade sem poder comprar alimento;
- desemprego/subemprego observável;
- profissões saturadas;
- oportunidades existentes;
- estoque alimentar;
- preço;
- concentração aproximada;
- mortes por privação;
- população persistentemente pobre.

Não transforme isso em `RevolutionScore` agora.

Isso será decidido quando política/facções forem implementadas.

A fase atual só deve garantir que esses estados resultem de economia real e sejam observáveis.

---

# 26. AUDITORIA CURTA ANTES DAS CAMPANHAS LONGAS

Antes de gastar três vezes 10.000 horas, rode auditoria intermediária de aproximadamente 1.000 horas nos três modos.

Compare:

- reserva ativa;
- reserva selecionada;
- fome <50 + déficit;
- oportunidade disponível;
- necessidade que venceu;
- cobertura;
- próxima oportunidade;
- compra parcial;
- segunda ração;
- trabalho com crédito fracionário;
- trabalho saturado;
- oferta temporária esgotada;
- denúncias inválidas;
- comunicação sem aprendizado.

Se aparecer bug estrutural claro:

corrija antes da auditoria final.

Preserve os resultados intermediários.

---

# 27. AUDITORIAS FINAIS

Depois de congelar as regras:

- Dovha jogador: 10.000 horas;
- Dovha espectador: 10.000 horas;
- Mira mundo: 10.000 horas.

Preserve completamente:

- saves anteriores;
- relatórios anteriores;
- código baseline;
- seeds;
- política automatizada anterior onde comparação exige.

Valide:

- invariantes;
- dinheiro;
- população;
- save/load;
- determinismo;
- continuação +24h.

---

# 28. MÉTRICAS DE RESERVA

Compare com a versão anterior:

- % de NPCs com alvo completo;
- média de rações;
- buscas iniciadas com fome <50;
- buscas iniciadas com fome ≥80;
- buscas iniciadas com HP ≤3;
- cobertura média;
- reserva ativa vs selecionada;
- o que venceu a reserva;
- oportunidades preventivas perdidas apesar de mercado/dinheiro;
- compras da primeira ração;
- compras da segunda;
- compras parciais;
- tempo até completar alvo;
- viagens iniciadas sem cobertura suficiente.

Não estabeleça meta arbitrária como:

“80% precisam possuir duas rações.”

Queremos descobrir o comportamento.

---

# 29. MÉTRICAS ECONÔMICAS

Registrar:

- dinheiro municipal;
- dinheiro dos NPCs;
- distribuição aproximada;
- NPCs abaixo de preço de uma refeição;
- pobres com comida municipal disponível;
- pobres em profissão saturada;
- pobres sem oportunidade local executável;
- salário integral;
- crédito salarial parcial;
- trabalhos com crédito parcial;
- trabalhos verdadeiramente fracassados;
- falhas por insumo;
- falhas por saturação;
- falhas por quota;
- falhas por contexto/local;
- serviços temporários observados;
- serviços realmente executados;
- ofertas que expiraram antes da chegada;
- produção;
- estoque.

Não interprete desigualdade automaticamente como bug.

---

# 30. MÉTRICAS SOCIAIS

Registrar:

- denúncias totais;
- denúncias ao próprio culpado;
- denúncias válidas;
- denúncias bloqueadas por falta de autoridade independente;
- pedidos de informação;
- fatos úteis transmitidos;
- confiança melhorada;
- fatos já conhecidos;
- fatos temporalmente inúteis;
- repetição evitada;
- necessidades fechadas por informação realmente útil;
- buscas familiares que avançaram;
- buscas familiares que permaneceram bloqueadas.

Resultado desejado:

zero denúncias tratadas como independentes quando destinatário é o próprio culpado.

Resultado desejado:

informação velha/repetida NÃO deve aparecer como avanço real.

---

# 31. AUDITORIA NARRATIVA CONTINUA OBRIGATÓRIA

Assim como no relatório anterior, não produza somente estatísticas econômicas.

Crie novamente:

# Histórias emergentes observadas

Procure ativamente histórias reais em:

- família;
- ausência;
- busca;
- reencontro;
- crime;
- denúncia;
- investigação;
- reparação;
- proteção;
- morte;
- descoberta de restos;
- luto;
- lembrança;
- amizade;
- reputação;
- reconhecimento;
- trabalho;
- desemprego;
- pobreza;
- mudança de profissão;
- treinamento;
- abandono;
- retomada;
- ambição;
- sucessão;
- quests;
- intervenção do jogador.

Desta vez, também procure histórias economicamente interessantes como:

- profissional que perde renda porque seu setor saturou;
- personagem que muda trajetória por falta de trabalho;
- personagem pobre numa cidade rica;
- ajuda familiar causada por desigualdade;
- crime associado a dificuldade econômica;
- carreira retomada;
- oferta perdida para concorrente;
- personagem que consegue se estabilizar;
- personagem que não consegue e permanece insatisfeito.

NÃO chame automaticamente isso de:

- luta de classes;
- consciência política;
- revolução;
- anti-Estado.

Esses conceitos ainda não existem no motor.

Apenas registre os fatos materiais.

Isso poderá ser usado no futuro para criar tais comportamentos.

---

# 32. FORMATO DAS HISTÓRIAS

Para cada história relevante:

- título;
- campanha;
- personagens + IDs;
- relações;
- profissão;
- situação econômica relevante;
- necessidades;
- conhecimento anterior;
- evento causal;
- decisões;
- consequências;
- mudança de relação/reputação/profissão;
- estado final;
- duração.

Mostrar quando possível:

evento
→ conhecimento
→ necessidade
→ prioridade
→ solução
→ ação
→ consequência
→ nova situação.

Distinguir explicitamente:

- causa comprovada;
- correlação;
- interpretação provável;
- informação que o auditor sabe mas o personagem não sabe.

Não inventar emoção.

Não inventar motivação que não esteja suportada.

---

# 33. DIVERSIDADE NARRATIVA

Registrar novamente:

- episódios pessoais com ação;
- episódios com 2 eventos;
- com 3;
- com 4+;
- duração ≥168h;
- personagens acompanhados por ≥720h;
- histórias sem núcleo alimentar;
- histórias autônomas;
- histórias com jogador;
- histórias interrompidas por morte;
- mudanças profissionais;
- reconhecimento;
- luto;
- crime;
- investigação;
- proteção;
- busca familiar.

Comparar com o relatório anterior.

Objetivo:

descobrir se melhorar prevenção e coerência econômica:

- aumenta oportunidades sociais;
- diminui repetição;
- aumenta continuidade;
- ou apenas mantém mais pessoas vivas.

Não presumir o resultado.

---

# 34. RELATÓRIO FINAL

Produza relatório detalhado com:

1. Resumo executivo.
2. Código/arquitetura preservados.
3. Bugs corrigidos.
4. Modelo de prioridade preventiva anterior.
5. Novo modelo de cobertura/oportunidade.
6. Segunda ração.
7. Compra parcial.
8. Crédito salarial.
9. Profissões saturadas.
10. Trabalho temporário.
11. Intenções incompatíveis com local.
12. Distribuição econômica.
13. Desigualdade observada.
14. Por que desigualdade NÃO foi automaticamente corrigida.
15. Denúncia ao culpado.
16. Informação velha.
17. Testes.
18. Auditoria curta.
19. Auditorias de 10.000 horas.
20. Comparação antes/depois.
21. Mortalidade.
22. Reservas.
23. Renda.
24. Estoques.
25. Oportunidades.
26. Métricas sociais.
27. Histórias emergentes observadas.
28. Diversidade narrativa.
29. Bugs remanescentes.
30. Limitações.
31. Recomendações para a Fase 4.

---

# 35. CRITÉRIO DE SUCESSO

Não considere sucesso simplesmente porque:

- mortes caíram;
- todos possuem comida;
- dinheiro ficou igualmente distribuído;
- pobreza desapareceu;
- reserva sempre vence.

Isso poderia inclusive piorar o projeto.

Considere sucesso se:

- reserva preventiva tem oportunidade real de acontecer;
- prioridade responde a cobertura/oportunidade;
- segunda ração continua financiável;
- crédito parcial não é chamado de falha;
- oportunidade temporária anunciada é realmente executável naquele momento;
- concorrência ainda pode fazer oportunidade desaparecer;
- profissão saturada pode legitimamente gerar pobreza;
- desigualdade continua possível;
- transferências permanecem reais;
- denúncia não vai ao próprio acusado;
- informação velha não é registrada como progresso;
- histórias continuam surgindo;
- sistemas preservam determinismo e invariantes.

O objetivo é produzir **causas sociais verdadeiras**, inclusive causas ruins.

Um personagem pobre numa cidade rica pode ser um resultado excelente.

Um personagem pobre porque `2/6` foi interpretado como zero é um bug.

Uma cidade com grande estoque e trabalhadores insatisfeitos pode futuramente gerar conflitos políticos extremamente interessantes.

Não elimine essa possibilidade.

Garanta apenas que, quando ela acontecer, tenha surgido do mundo — e não de uma interpretação incorreta do código.