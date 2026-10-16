# FASE 5.5 — FACÇÕES, GRUPOS, PROPOSTAS E AÇÃO INSTITUCIONAL

## 0. OBJETIVO DA FASE

A Fase 5.5 deve transformar pressão social em estruturas institucionais coerentes.

O mundo já possui:

- necessidades individuais;
- grupos;
- propostas;
- autoridades;
- facções;
- recursos;
- produção;
- profissões;
- cidades e vilas;
- rotas;
- conhecimento subjetivo;
- crime;
- religião;
- relações;
- ações coletivas.

O problema atual é que esses sistemas ainda não formam um ciclo institucional completo.

Na campanha anterior surgiram muitos grupos semelhantes tratando do mesmo problema, enquanto facções continuaram com poucos ou nenhum membro.

Esta fase deve resolver isso sem criar adesões artificiais, facções aleatórias ou políticas que alterem números magicamente.

Princípio central:

```text
INDIVÍDUOS SENTEM PROBLEMAS
↓
PROCURAM ORGANIZAÇÕES EXISTENTES
↓
ENTRAM EM GRUPOS OU CRIAM NOVOS
↓
GRUPOS CONCENTRAM APOIO
↓
PROPOSTAS PRESSIONAM AUTORIDADES
↓
POLÍTICAS TENTAM ALTERAR O MUNDO REAL
↓
SE O ESTADO NÃO RESOLVE
↓
GRUPOS PODEM DESENVOLVER CAPACIDADE PRÓPRIA
↓
FACÇÕES
↓
AÇÃO INSTITUCIONAL INDEPENDENTE
```

---

# 1. PRINCÍPIO FUNDAMENTAL

Separar claramente:

```text
GRUPO
```

de:

```text
FACÇÃO
```

Um grupo representa principalmente:

```text
pessoas organizadas em torno de uma necessidade,
causa,
problema,
interesse ou objetivo compartilhado.
```

Uma facção representa:

```text
uma organização persistente,
com recursos,
membros,
liderança,
capacidade própria de ação
e continuidade além de um único problema imediato.
```

---

# 2. GRUPO NÃO DEVE SER CRIADO SE JÁ EXISTE UM COMPATÍVEL

Antes de criar um novo grupo, um NPC deve procurar grupos relevantes que:

- ele conhece;
- estejam acessíveis;
- atuem na mesma localidade ou região adequada;
- tratem de causa suficientemente compatível;
- aceitem novos participantes;
- não sejam incompatíveis socialmente com ele.

Fluxo:

```text
StrongNeed
↓
NeedCollectiveAction
↓
SearchKnownCompatibleGroups
```

Se houver grupo adequado:

```text
JoinGroup
```

deve competir como solução preferível a:

```text
CreateGroup
```

Criar um novo grupo somente quando houver motivo real.

---

# 3. NÃO USAR CONHECIMENTO GLOBAL

Um grupo existir na cidade NÃO significa que todo NPC sabe que ele existe.

Preservar:

```text
ObjectiveExistence != NPCKnowledge
```

O NPC pode descobrir grupos por:

- conhecidos;
- familiares;
- rumores;
- reuniões;
- ações públicas;
- propostas públicas;
- participantes;
- autoridade;
- presença física;
- trabalho;
- religião;
- facções relacionadas.

---

# 4. MOTIVOS PARA NÃO ENTRAR EM GRUPO EXISTENTE

Mesmo conhecendo um grupo compatível, o NPC pode preferir criar outro se houver causa suficiente.

Exemplos:

- hostilidade ao líder;
- baixa confiança;
- rivalidade;
- religião incompatível;
- valores incompatíveis;
- objetivo parcialmente diferente;
- grupo considerado ineficaz;
- grupo fechado;
- experiências ruins anteriores;
- distância;
- grupo ligado a inimigo;
- excesso de compromisso;
- desejo de liderança próprio.

Não criar fragmentação aleatória.

---

# 5. CONSOLIDAÇÃO DE GRUPOS

Evitar dezenas de grupos praticamente idênticos na mesma região.

Grupos com:

```text
mesma causa
mesma localidade/região
objetivos compatíveis
membros socialmente compatíveis
```

podem:

- receber novos membros;
- cooperar;
- apoiar mesma proposta;
- eventualmente se fundir.

Não forçar fusão automática.

---

# 6. GRUPOS PODEM CRESCER

Um grupo deve possuir continuidade suficiente para:

```text
2 pessoas
→ 4
→ 8
→ 20
```

sem precisar criar novos grupos paralelos.

Registrar:

- membros;
- liderança;
- causa;
- objetivos;
- apoio;
- recursos;
- idade;
- reuniões;
- histórico;
- propostas apoiadas;
- ações coletivas.

---

# 7. PROPOSTAS SEM DUPLICAÇÃO

Antes de criar uma proposta nova:

```text
SearchCompatibleExistingProposal
```

na jurisdição relevante.

Uma proposta semelhante deve ser reutilizada quando:

- problema é equivalente;
- setor é equivalente;
- efeito desejado é compatível;
- área afetada é compatível;
- proposta ainda está ativa/relevante.

Nesse caso:

```text
SupportProposal
```

em vez de:

```text
CreateProposal
```

---

# 8. PROPOSTA DEVE ACUMULAR APOIO

Uma proposta deve possuir apoio real.

Exemplo conceitual:

```text
Proposal
{
    supporters_people
    supporting_groups
    affected_population
    created_at
    persistence
    urgency
    locality
    sector
    desired_effect
}
```

Evitar duplicar contagem de uma mesma pessoa através de vários grupos.

---

# 9. PRESSÃO POLÍTICA

Criar uma pressão política derivada.

Não fazer:

```text
100 supporters = automatic approval
```

A pressão deve considerar fatores contextuais.

Conceitualmente:

```text
PoliticalPressure =
    support
    × severity
    × persistence
    × visibility
    × legitimacy
    × affected_population
    × local_crisis
```

A fórmula exata pode seguir o padrão de utilidades existente.

Não precisa ser multiplicação literal.

---

# 10. PREFEITO SENTE PRESSÃO

A autoridade deve avaliar a pressão coletiva.

A pressão pode tornar o prefeito:

```text
mais disposto a reconsiderar
mais disposto a ceder
mais disposto a aprovar parcialmente
mais disposto a gastar recursos
mais disposto a priorizar o problema
```

Não substituir personalidade ou julgamento do prefeito.

---

# 11. PRESSÃO NÃO SIGNIFICA CONCORDÂNCIA

Um prefeito pode aceitar uma proposta por:

- convicção;
- compaixão;
- pragmatismo;
- medo;
- pressão;
- preservação da ordem;
- reputação;
- relações;
- necessidade econômica;
- ameaça de escalada.

Preservar a causa registrada.

---

# 12. PRESSÃO PODE SER IGNORADA

Prefeito pode:

```text
approve
partial_approve
reject
defer
ignore
```

desde que haja decisão contextual coerente.

Alta pressão não cria aprovação obrigatória.

---

# 13. PROPOSTAS DEVEM GERAR POLÍTICAS REAIS

Uma proposta aprovada NÃO deve apenas conceder um bônus abstrato.

Ela deve criar:

```text
Policy
```

ou estado institucional equivalente.

A política deve alterar incentivos e ações possíveis.

---

# 14. POLÍTICAS ECONÔMICAS GENÉRICAS

Criar sistema genérico, evitando um sistema separado para cada recurso.

Exemplo:

```text
Policy
{
    jurisdiction
    sector
    objective
    intensity
    budget
    start_time
    status
}
```

Setores iniciais relevantes:

```text
FOOD
WATER
SECURITY
WEAPONS
RAW_MATERIAL
PROCESSING
EMPLOYMENT
TRANSPORT
```

Outros podem ser adicionados futuramente.

---

# 15. AÇÕES DE POLÍTICA

Uma política pode permitir/priorizar ações como:

```text
subsidize
hire
purchase
distribute
ration
train
protect
increase_capacity
prioritize_production
store_reserve
commission_work
```

Usar sistemas econômicos já existentes.

---

# 16. POLÍTICA NÃO CRIA RECURSOS DO NADA

Regra obrigatória:

```text
PolicyApproved
!=
ResourceCreated
```

Exemplo:

Uma política de aumentar comida pode:

```text
aumentar demanda por trabalhadores
aumentar prioridade de produção
oferecer pagamento
financiar ferramenta
comprar produção
aumentar reservas
```

Mas a comida ainda precisa ser:

```text
produzida
coletada
processada
transportada
comprada
armazenada
```

---

# 17. POLÍTICA PODE FALHAR

Exemplo:

```text
IncreaseFoodProduction
↓
mais trabalhadores são procurados
↓
faltam matérias-primas
↓
produção não cresce
```

Resultado:

```text
PolicyEffectiveness = low
```

Isso pode alimentar nova pressão social.

Não transformar aprovação em sucesso garantido.

---

# 18. ÁGUA E COMIDA

A campanha anterior revelou mortalidade urbana elevada por sede.

Usar esta fase para permitir resposta institucional material.

Exemplo:

```text
grupo percebe escassez
↓
apoia proposta de água
↓
prefeito aprova
↓
política aumenta capacidade/produção/distribuição
↓
trabalhadores e recursos são mobilizados
```

Não aumentar água magicamente.

---

# 19. INFRAESTRUTURA E POPULAÇÃO

Permitir que capacidade material relevante possa responder à dimensão da cidade.

Capital não deve possuir necessariamente a mesma infraestrutura máxima de uma vila.

Quando uma política de expansão de capacidade for aceita:

```text
budget + workers + materials
→ capacity improvement
```

Preservar conservação material.

---

# 20. RESULTADO DA POLÍTICA DEVE ALTERAR O MUNDO

Uma política pode afetar:

- produção;
- estoque;
- emprego;
- segurança;
- preços;
- disponibilidade;
- capacidade;
- patrulhas;
- treinamento;
- comércio.

Essas consequências devem surgir dos sistemas existentes.

---

# 21. POPULAÇÃO PRECISA PERCEBER RESULTADOS

Quando possível, grupos devem obter conhecimento causal do resultado.

Exemplo:

```text
ProposalAccepted
↓
PolicyCreated
↓
water availability rises
```

ou:

```text
PolicyCreated
↓
nothing improves
```

Isso deve influenciar:

- satisfação;
- confiança;
- novas propostas;
- pressão;
- continuidade do grupo;
- formalização futura.

---

# 22. PROPOSTA BEM-SUCEDIDA PODE REDUZIR PRESSÃO

Se o problema diminui materialmente:

```text
NeedSeverity ↓
PoliticalPressure ↓
GroupActionPressure ↓
```

O grupo pode:

- continuar;
- perder atividade;
- dissolver;
- mudar de objetivo.

Não dissolver automaticamente.

---

# 23. PROPOSTA FRACASSADA PODE AUMENTAR PRESSÃO

Se:

```text
proposal rejected
```

ou:

```text
approved but ineffective
```

e o problema continua:

```text
Frustration ↑
SelfActionPressure ↑
InstitutionalizationPressure ↑
```

desde que os membros saibam do fracasso.

---

# 24. FACÇÃO COMO EVOLUÇÃO DE GRUPO

Uma facção deve poder nascer de um grupo.

Não por tamanho isolado.

Não fazer:

```text
if members >= 10:
    become_faction()
```

---

# 25. FORMALIZATION PRESSURE

Criar pressão de formalização derivada.

Possíveis fatores:

- problema persistente;
- propostas fracassadas;
- repetidas ações coletivas;
- necessidade de coordenação duradoura;
- necessidade de treinamento;
- necessidade de patrimônio;
- necessidade de sede;
- necessidade de hierarquia;
- necessidade de funções especializadas;
- necessidade de agir sem autoridade;
- recursos acumulados;
- identidade compartilhada;
- liderança estável.

---

# 26. GRUPO PODE DECIDIR AGIR POR CONTA PRÓPRIA

Exemplo:

```text
roubos em estrada
↓
grupo pede segurança
↓
autoridade não resolve
↓
problema continua
↓
grupo começa a organizar patrulha
```

Isso pode gerar necessidade de:

- armas;
- turnos;
- treinamento;
- estoque;
- liderança;
- sede;
- financiamento.

Então:

```text
FormalizeFaction
```

pode se tornar solução.

---

# 27. FACÇÃO NÃO É BRAÇO DO PREFEITO

Uma facção possui:

```text
OwnMembers
OwnResources
OwnLeadership
OwnGoals
OwnActions
OwnKnowledge
OwnHQ
```

Ela pode agir sem pedir autorização política para cada ação.

---

# 28. FACÇÃO TEM CAPACIDADES REAIS

Criar capacidades derivadas do que a organização realmente possui.

Exemplo:

```text
FactionCapabilities
```

podem incluir:

```text
patrol
escort
train
produce
store
guard
investigate
trade
recruit
explore
occupy
```

Não conceder automaticamente.

---

# 29. CAPACIDADE DEPENDE DE MEMBROS

Exemplo:

Facção com:

```text
guards
```

pode patrulhar melhor.

Com:

```text
smith
```

pode produzir/manter certos equipamentos.

Com:

```text
hunter
```

pode obter recursos específicos.

Com:

```text
merchant
```

pode melhorar ações comerciais.

Usar profissão real dos membros.

---

# 30. CAPACIDADE DEPENDE DE RECURSOS

Uma organização sem:

```text
money
food
water
tools
weapons
```

não deve conseguir executar ações que dependem deles.

Não gerar recursos institucionais artificialmente.

---

# 31. CAPACIDADE DEPENDE DE INFRAESTRUTURA

HQ pode oferecer:

- armazenamento;
- reunião;
- descanso;
- recrutamento;
- treinamento;
- coordenação.

Castelos/POIs poderão futuramente virar sedes conforme sistema já existente.

---

# 32. VALOR DE ENTRAR EM FACÇÃO

A adesão precisa responder à pergunta:

> Por que este NPC entraria?

Possíveis benefícios reais:

- proteção;
- renda;
- trabalho;
- equipamento;
- treinamento;
- comida/água;
- abrigo;
- status;
- influência;
- companhia;
- identidade;
- acesso a expedições;
- acesso a conhecimento;
- rede social;
- possibilidade de carreira;
- acesso a HQ.

---

# 33. CUSTOS DA FACÇÃO

Adesão também possui custos:

- deveres;
- risco;
- contribuição;
- trabalho;
- possível perda de autonomia;
- obrigações;
- inimigos institucionais;
- distância;
- possível ilegalidade;
- lealdade esperada.

---

# 34. DECISÃO DE ADESÃO

Não usar chance arbitrária.

Avaliar:

```text
perceived_benefit
vs
perceived_cost
```

modificado por:

- personalidade;
- necessidade;
- relações;
- profissão;
- reputação;
- ambição;
- independência;
- coragem;
- confiança;
- recursos;
- situação atual.

---

# 35. CONVITE PRECISA TER CONTINUIDADE

Atualmente convites podem ficar oferecidos sem resolução.

Criar continuidade.

Estados possíveis:

```text
OFFERED
CONSIDERING
CONDITIONED
DEFERRED
ACCEPTED
REJECTED
EXPIRED_FOR_REASON
```

Não expirar apenas por timeout simples se continuar relevante.

---

# 36. CONDIÇÃO DE ENTRADA

Uma pessoa pode responder:

```text
"aceito se..."
```

semanticamente.

Exemplos:

- pagamento;
- equipamento;
- segurança;
- recuperação física;
- retorno para casa;
- conversa posterior;
- conclusão de obrigação existente.

Não exige diálogo textual.

---

# 37. RETOMADA

Convite adiado deve poder ser retomado.

Exemplo:

```text
fatigued
→ defer
→ rest
→ reconsider
```

Sem precisar reencontrar arbitrariamente o líder se houver canal institucional válido.

Mas contato físico continua necessário quando semanticamente exigido.

---

# 38. PEDIDO ESPONTÂNEO DE ADESÃO

Preservar:

```text
Person → RequestMembership
```

A facção pode:

```text
accept
reject
defer
set_condition
```

---

# 39. BANDITISMO NÃO É CLASSE

Não criar:

```text
BanditNPC
```

como tipo arbitrário.

Comportamento bandido deve emergir de:

```text
necessidade
+
personalidade
+
oportunidade
+
baixo custo percebido
+
crime repetido
```

---

# 40. BANDIDOS PODEM SE ENCONTRAR

Pessoas envolvidas em crimes compatíveis podem:

```text
cooperate
share information
share targets
share loot
protect one another
```

se houver conhecimento e confiança suficientes.

---

# 41. GRUPO DE BANDIDOS

Se cooperação criminosa persistir:

```text
individual criminals
↓
criminal group
```

O grupo ainda usa a mesma infraestrutura de Group.

Não criar outro motor separado.

---

# 42. FACÇÃO CRIMINOSA

Se o grupo criminoso desenvolve:

- membros estáveis;
- liderança;
- recursos;
- esconderijo/sede;
- coordenação;
- objetivos persistentes;
- capacidade operacional;

pode formalizar-se como facção.

---

# 43. FACÇÃO NÃO PRECISA SER LEGAL

Facções podem ser:

- cívicas;
- mercenárias;
- comerciais;
- criminosas;
- religiosas;
- protetoras;
- profissionais;
- exploratórias;
- políticas.

Não usar categorias rígidas para determinar comportamento.

A identidade deve emergir das atividades predominantes.

---

# 44. LEI LOCAL

Ações de facções devem ser avaliadas segundo a lei/jurisdição local.

Não fazer:

```text
FactionAction = illegal
```

por padrão.

---

# 45. STATUS LOCAL DA FACÇÃO

Criar algo conceitualmente como:

```text
FactionLocalStatus
```

Possíveis estados:

```text
RECOGNIZED
CONTRACTED
TOLERATED
NEUTRAL
RESTRICTED
ILLEGAL
HOSTILE
```

O status pode variar por cidade/reino.

---

# 46. LEGALIDADE DEPENDE DA AÇÃO

Exemplo:

```text
patrulhar voluntariamente
```

pode ser legal.

```text
proteger comerciante
```

pode ser legal.

```text
vender mercadoria
```

pode ser legal.

```text
cobrar pedágio sem autorização
```

pode ser ilegal.

```text
sequestrar suspeito
```

pode ser ilegal.

```text
roubar viajantes
```

deve ser tratado como crime conforme sistema existente.

---

# 47. PREFEITO PODE REAGIR A FACÇÕES

A autoridade pode:

```text
recognize
ignore
negotiate
contract
fund
restrict
fine
ban
order_dissolution
investigate
arrest_members
```

Somente quando possuir conhecimento suficiente.

---

# 48. FACÇÃO PODE REAGIR À AUTORIDADE

Pode:

```text
comply
negotiate
ignore
move
hide
reduce_activity
resist
retaliate
```

Não criar guerra civil automática.

---

# 49. CONTRATO ENTRE CIDADE E FACÇÃO

Permitir relação institucional futura ou simples nesta fase:

```text
CityContract
```

Exemplo:

```text
cidade paga
↔
facção patrulha estrada
```

Usar recursos reais.

Não precisa ser sistema econômico enorme.

---

# 50. FACÇÃO PODE SUPRIR FALHA DO ESTADO

Exemplo desejado:

```text
alto crime em estrada
↓
grupos pedem segurança
↓
propostas falham
↓
grupo treina membros
↓
faz patrulha própria
↓
formaliza
↓
facção de proteção
```

Isso não deve ser roteirizado.

Cada etapa emerge dos sistemas gerais.

---

# 51. PODER PARALELO

Se uma facção começa a executar funções que o Estado não consegue:

- segurança;
- distribuição;
- comércio;
- treinamento;
- proteção;

pode aumentar:

```text
reputation
public_dependence
local_influence
```

Não criar uma variável abstrata de "poder político" sem evidência.

Derivar de ações, relações, recursos e apoio.

---

# 52. CONFLITO ENTRE FACÇÕES

Não criar guerras de facção aleatórias.

Conflito pode surgir quando objetivos entram em choque:

```text
mesmo recurso
mesma área
alvos incompatíveis
proteção versus roubo
religião rival
disputa por membros
disputa por HQ
```

Usar relações e ações já existentes.

---

# 53. GRUPOS PODEM APOIAR FACÇÕES

Grupo pode:

- pedir ajuda;
- compartilhar objetivo;
- apoiar ação;
- fornecer membros;
- contratar;
- eventualmente integrar-se.

Não fazer integração automática.

---

# 54. FACÇÕES PODEM RECRUTAR GRUPOS

Uma facção pode identificar grupo compatível.

Pode:

```text
invite_group_leader
invite_members
offer_affiliation
offer_support
```

Sem absorção mágica.

---

# 55. PROPOSTAS E FACÇÕES DEVEM CONVERSAR

Facção também pode apoiar proposta.

Mas ela não precisa depender dela.

Fluxo possível:

```text
facção apoia reforma legal
↓
prefeito rejeita
↓
facção decide atuar sozinha dentro dos limites de capacidade
```

---

# 56. PRESSÃO POLÍTICA DE FACÇÕES

Facções podem gerar pressão maior por:

- membros;
- recursos;
- reputação;
- capacidade;
- apoio popular;
- presença local.

Mas não simplesmente:

```text
Faction = huge pressure bonus
```

---

# 57. GRUPOS NÃO SOMEM APÓS FORMALIZAÇÃO SEM HISTÓRICO

Quando Group vira Faction:

registrar transição.

Preservar:

```text
origin_group_id
founders
cause
history
formalized_at
```

Isso é importante para Chronicle futura.

---

# 58. NÃO CRIAR SISTEMAS ESPECÍFICOS DEMAIS

Evitar:

```text
GuildSystem
MilitiaSystem
BanditFactionSystem
MerchantFactionSystem
CultFactionSystem
```

Preferir:

```text
Group
Institutionalization
Faction
Capabilities
Goals
Resources
Actions
LegalStatus
```

---

# 59. NÃO IMPLEMENTAR GUERRA ENTRE REINOS

Fora do escopo.

Não adicionar:

- conquista territorial;
- diplomacia internacional completa;
- exércitos nacionais novos;
- guerra formal.

---

# 60. NÃO IMPLEMENTAR ELEIÇÕES

Fora do escopo atual.

Pressão política age sobre autoridades existentes.

---

# 61. NÃO IMPLEMENTAR ECONOMIA NOVA PARALELA

Reutilizar:

- produção;
- estoque;
- trabalho;
- dinheiro;
- compra;
- venda;
- itens.

Não criar recursos falsos para facções.

---

# 62. AUDITORIA DE GRUPOS

Registrar:

```text
GroupSearchAttempt
ExistingGroupFound
GroupJoinAttempt
GroupJoined
GroupJoinRejected
NewGroupCreated
GroupMerged
```

quando semanticamente aplicável.

Objetivo:

medir se a criação duplicada realmente caiu.

---

# 63. AUDITORIA DE PROPOSTAS

Registrar:

```text
CompatibleProposalFound
ProposalSupported
ProposalCreated
PoliticalPressureChanged
PolicyDecision
PolicyCreated
PolicyEffect
```

Não gerar evento apenas para preencher contador.

---

# 64. AUDITORIA DE FACÇÕES

Registrar:

```text
FormalizationConsidered
FactionFormalized
FactionRecruitmentNeed
FactionInvite
FactionJoinRequest
FactionMembershipAccepted
FactionMembershipRejected
FactionMembershipDeferred
FactionMembershipConditioned
FactionAction
FactionLocalStatusChanged
```

---

# 65. AUDITORIA DE POLÍTICA

Para cada política relevante, permitir reconstruir:

```text
qual problema existia?
quem pressionou?
qual proposta recebeu apoio?
quem decidiu?
por quê?
qual política surgiu?
quais recursos foram mobilizados?
o setor respondeu?
o problema melhorou?
```

---

# 66. TESTES PEQUENOS

Não executar campanhas gigantes para validar regras controláveis.

Criar aproximadamente:

```text
10–14 testes direcionados
```

Pequenos.

Não rodar milhares de horas dentro de teste unitário.

---

# 67. TESTES MÍNIMOS

Cobrir pelo menos:

1. NPC encontra grupo compatível conhecido e tenta entrar antes de criar novo;
2. NPC desconhece grupo existente e pode formar outro;
3. incompatibilidade legítima permite grupo separado;
4. proposta semelhante existente recebe apoio em vez de duplicação;
5. múltiplos grupos aumentam pressão da mesma proposta sem duplicar pessoas;
6. prefeito responde diferentemente com maior pressão;
7. proposta aprovada cria política e não recursos mágicos;
8. política de água/food altera incentivos/capacidade por caminhos materiais;
9. política pode falhar por falta de recursos;
10. grupo persistente pode formalizar facção sob condições controladas;
11. facção possui capacidade apenas quando membros/recursos permitem;
12. convite pode ser aceito, recusado, adiado e retomado;
13. ação ilegal de facção provoca resposta institucional;
14. banditismo coletivo pode formar grupo/facção sem classe Bandit.

---

# 68. SMOKE TEST

Executar um smoke pequeno após os testes.

Objetivo:

- carregamento;
- geração;
- serialização;
- grupos;
- proposta;
- política;
- facção;
- rota.

Não usar campanha longa como smoke.

---

# 69. CAMPANHA NATURAL

Executar:

```text
300 horas
```

apenas.

Uma campanha.

Sem jogador.

Começada do zero.

---

# 70. SEED

A campanha natural deve usar:

```text
UMA SEED NOVA
```

Nunca reutilizar Arandor-54, Thalendor-521 ou outra campanha antiga para selecionar resultados.

Gerar uma nova seed conforme mecanismo normal do projeto.

Registrar seed no relatório.

---

# 71. SEM SEED-SHOPPING

Não reiniciar porque:

- não surgiu facção;
- nenhum grupo formalizou;
- prefeito não aprovou;
- eventos ficaram pouco interessantes.

Só reiniciar se houver:

```text
bug estrutural
crash
corrupção de save
invariante violado
```

Preservar no relatório qualquer reinício necessário.

---

# 72. O QUE OBSERVAR EM 300H

Grupos:

- criados;
- adesões;
- tamanho;
- grupos duplicados evitados;
- grupos incompatíveis legítimos;
- fusões;
- dissoluções.

Propostas:

- criadas;
- propostas reutilizadas;
- apoios;
- grupos apoiadores;
- pessoas apoiadoras únicas;
- pressão;
- decisões.

Políticas:

- criadas;
- setores;
- recursos mobilizados;
- efeitos materiais;
- políticas eficazes;
- políticas ineficazes.

Facções:

- convites;
- respostas;
- membros;
- formalizações;
- capacidades;
- ações;
- recursos;
- sedes;
- relação com autoridades.

Crime organizado:

- criminosos cooperando;
- grupos criminosos;
- formalização se ocorrer.

Não exigir que eventos raros aconteçam.

---

# 73. CAMPANHA NÃO É TESTE DE CHECKLIST

Não manipular a seed para produzir:

```text
new faction
criminal faction
illegal faction
city conflict
```

Os testes controlados provam capacidade.

A campanha natural prova integração e emergência.

---

# 74. RELATÓRIOS OBRIGATÓRIOS

Após a campanha, gerar exatamente estes três relatórios principais:

```text
RELATORIO_TECNICO.md
MUNDO.md
HISTORIAS_REAIS.md
```

---

# 75. RELATORIO_TECNICO.md

Deve conter:

- implementação realizada;
- arquitetura preservada;
- testes;
- bugs encontrados;
- correções;
- limites;
- campanha de 300h;
- métricas;
- gargalos;
- conclusão honesta.

Distinguir explicitamente:

```text
comprovado em teste controlado
```

de:

```text
observado naturalmente na campanha
```

---

# 76. MUNDO.md

Gerar catálogo compacto do mundo final.

Incluir:

- seed;
- população;
- reinos;
- localidades;
- grupos;
- tamanho dos grupos;
- propostas;
- apoio;
- políticas;
- setores afetados;
- facções;
- membros;
- recursos;
- ações;
- status legal;
- religião;
- conflitos relevantes;
- mortes;
- economia;
- rotas se relevante;
- POIs relevantes.

Não despejar centenas de linhas desnecessárias se puder resumir e apontar contadores importantes.

---

# 77. HISTORIAS_REAIS.md

Selecionar aproximadamente:

```text
6–10 histórias
```

reais.

Priorizar cadeias como:

- NPC procura grupo e entra em um existente;
- grupo acumula apoio;
- mesma proposta recebe apoio de vários grupos;
- pressão altera decisão de prefeito;
- política muda produção;
- política falha;
- grupo decide agir por conta própria;
- grupo vira facção;
- pessoa entra em facção por benefício concreto;
- facção patrulha;
- ação ilegal provoca resposta da autoridade;
- criminosos se organizam.

Somente se realmente acontecer.

---

# 78. NÃO INVENTAR HISTÓRIAS

Proibido:

- inventar diálogo;
- inventar pensamento;
- inventar motivação não registrada;
- inventar causalidade;
- completar trajetória aberta;
- transformar teste controlado em lore da campanha.

---

# 79. LIMPEZA DA PASTA DO PROJETO — ANTES DE COMEÇAR

A pasta do projeto está ocupando aproximadamente 14 GB.

Antes da implementação da Fase 5.5:

```text
AUDITAR USO DE DISCO
```

Identificar quais diretórios/arquivos são responsáveis pelo crescimento.

Especial atenção a:

- saves de campanhas antigas;
- snapshots gigantes;
- JSONs completos de estado;
- logs;
- artefatos de testes;
- diretórios temporários;
- caches;
- campanhas interrompidas;
- outputs duplicados;
- relatórios intermediários;
- dumps.

---

# 80. LIMPEZA SEGURA

NÃO apagar:

- código-fonte;
- testes;
- configuração;
- documentação importante;
- relatórios finais históricos;
- baseline necessário;
- assets;
- arquivos de projeto;
- dados permanentes necessários para reprodução estrutural.

Apagar apenas arquivos regeneráveis ou grandes artefatos de execução que não precisam mais ser preservados.

---

# 81. NÃO APAGAR ÀS CEGAS

Antes de remover diretórios:

1. medir tamanho;
2. identificar conteúdo;
3. confirmar que é artefato regenerável;
4. preservar relatórios pequenos/importantes;
5. remover arquivos pesados desnecessários.

Não executar:

```text
rm -rf project/
```

nem comandos equivalentes amplos.

---

# 82. SAVES ANTIGOS

Se relatórios finais já preservam suficientemente campanhas antigas:

remover saves gigantes antigos que não sejam mais necessários.

Se existir dúvida sobre algum save:

preservar até verificar.

---

# 83. POLÍTICA DE RETENÇÃO A PARTIR DA FASE 5.5

Após cada campanha natural:

1. rodar campanha;
2. extrair métricas;
3. gerar os três relatórios;
4. gerar pequenos manifestos/evidências necessárias;
5. confirmar que relatórios foram gravados;
6. apagar o save completo pesado da campanha.

---

# 84. SAVE FINAL NÃO É ARQUIVO PERMANENTE

Após:

```text
RELATORIO_TECNICO.md
MUNDO.md
HISTORIAS_REAIS.md
```

estarem concluídos e auditados:

```text
DELETE LARGE FINAL SAVE
```

Não manter save gigante apenas por hábito.

---

# 85. O QUE PODE SER PRESERVADO

Preservar arquivos pequenos como:

```text
manifesto.json
metrics.json
seed.txt
test_results.log
eventos_relevantes.json
hashes.json
```

se úteis para auditoria.

Mas evitar duplicar o mundo completo nesses arquivos.

---

# 86. EVENTOS RELEVANTES

Se HISTORIAS_REAIS depender de evidência:

antes de apagar o save completo, extrair apenas:

```text
eventos utilizados nas histórias
IDs necessários
métricas agregadas
estado mínimo das entidades citadas
```

Não preservar milhões de eventos desnecessários.

---

# 87. TESTES NÃO DEVEM GERAR SAVES PERMANENTES

Testes devem usar:

- diretório temporário;
- fixture temporária;
- cleanup automático.

Ao terminar:

```text
temporary save deleted
```

---

# 88. CAMPANHA INTERROMPIDA

Se uma campanha quebrar por bug:

preservar somente evidência mínima necessária para reproduzir o erro.

Após corrigido e documentado:

remover dumps gigantes que não possuem mais utilidade.

---

# 89. CONTROLE DE TAMANHO

Ao final da Fase 5.5, reportar:

```text
project_size_before
project_size_after_cleanup
reports_size
largest_remaining_directories
```

Isso deve aparecer no relatório técnico.

---

# 90. NÃO CRIAR BACKUPS GIGANTES AUTOMÁTICOS

Evitar duplicar toda a árvore do projeto em cada fase.

Se houver baseline versionado pelo Git:

preferir Git.

Não copiar gigabytes de saves e outputs para:

```text
baseline_code/
backup/
old/
phase_previous/
```

sem necessidade real.

---

# 91. CÓDIGO ANTERIOR

Preservar histórico por controle de versão sempre que possível.

Não criar cópia integral do projeto para cada fase.

Se precisar de snapshot específico:

preservar somente código/configuração, excluindo:

- saves;
- cache;
- outputs;
- logs;
- relatórios grandes;
- artefatos temporários.

---

# 92. NOVA SEED SEMPRE PARA CAMPANHA NATURAL

Cada nova campanha natural de fase deve começar do zero com seed nova.

Não carregar save anterior.

Não continuar campanha antiga.

Fluxo:

```text
new generation
→ new seed
→ run
→ reports
→ delete heavy save
```

---

# 93. TESTES PODEM SER DETERMINÍSTICOS

Testes controlados podem usar seeds fixas pequenas para reprodutibilidade.

A exigência de seed nova vale principalmente para:

```text
natural campaign
```

Não prejudicar testes unitários por aleatoriedade desnecessária.

---

# 94. PERFORMANCE E TAMANHO

Durante a implementação, verificar se algum novo sistema cresce sem limite:

- histórico de propostas;
- apoio;
- grupos;
- eventos;
- conhecimento;
- políticas;
- convites;
- logs.

Usar poda/compactação quando semanticamente seguro.

Não apagar conhecimento vivo só para reduzir arquivo sem avaliar consequências.

---

# 95. INVARIANTES IMPORTANTES

### Grupos

```text
NPC não cria grupo redundante se conhece e aceita grupo compatível.
```

### Propostas

```text
proposta compatível ativa recebe apoio em vez de duplicação.
```

### Política

```text
aprovação não cria recursos do nada.
```

### Facção

```text
facção só executa ação que possui capacidade material/social para executar.
```

### Conhecimento

```text
ator não reage a organização/política/evento desconhecido.
```

### Lei

```text
autoridade não reage a ação da qual não possui conhecimento suficiente.
```

---

# 96. CRITÉRIO DE SUCESSO DA FASE

A fase é bem-sucedida se demonstrar estruturalmente:

```text
PRESSÃO SOCIAL
→ CONSOLIDAÇÃO
→ PROPOSTA
→ PRESSÃO POLÍTICA
→ POLÍTICA MATERIAL
```

e:

```text
PROBLEMA PERSISTENTE
→ GRUPO
→ CAPACIDADE PRÓPRIA
→ FORMALIZAÇÃO
→ FACÇÃO
→ AÇÃO AUTÔNOMA
```

sem scripts específicos.

---

# 97. NÃO EXIGIR FACÇÃO NATURAL EM 300H

Se nenhuma nova facção surgir naturalmente:

isso NÃO invalida a fase.

Os testes devem demonstrar que a transição é possível.

A campanha deve demonstrar que:

- grupos consolidam melhor;
- propostas deixam de duplicar excessivamente;
- apoio se concentra;
- autoridades sentem pressão;
- políticas têm efeitos reais;
- facções existentes conseguem oferecer valor e agir.

---

# 98. PRINCÍPIO FINAL

O objetivo não é produzir mais organizações.

O objetivo é permitir que organizações tenham razão para existir.

```text
GRUPO
= "nós temos um problema"

PROPOSTA
= "queremos que a autoridade faça algo"

POLÍTICA
= "a autoridade decidiu tentar alterar o mundo"

FACÇÃO
= "nós mesmos adquirimos capacidade permanente para agir"
```

E uma facção deve poder cooperar com o Estado, substituí-lo parcialmente, competir com ele ou entrar em conflito com ele dependendo do que realmente fizer.

Nenhuma dessas relações deve ser pré-escrita.

Elas devem emergir de:

```text
necessidade
+
conhecimento
+
membros
+
recursos
+
personalidade
+
história
+
pressão
+
capacidade
+
lei
+
consequência
```

Essa é a Fase 5.5.