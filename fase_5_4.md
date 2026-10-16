# FASE 5.4 — GEOGRAFIA, ROTAS E ACESSO

## 0. PRINCÍPIO DA FASE

A Fase 5.4 não existe para adicionar mais acontecimentos aleatórios.

Ela existe para tornar o espaço do mundo causalmente relevante.

O mundo possui:

- reinos;
- capitais;
- cidades;
- vilas;
- cavernas;
- castelos abandonados;
- quartéis-generais;
- autoridades;
- grupos;
- facções;
- religiões;
- deuses;
- rumores;
- pessoas procurando pessoas;
- migração;
- comércio;
- investigações.

Porém possuir um destino no estado global do mundo NÃO significa que um agente pode alcançá-lo.

A regra central desta fase é:

```text
EXISTIR
!=
SER CONHECIDO
!=
SABER ONDE FICA
!=
CONHECER UMA ROTA
!=
CONSEGUIR VIAJAR ATÉ LÁ
```

Nenhum personagem deve sair para uma localidade simplesmente porque o motor conhece seu ID ou sua posição.

---

# 1. NOVA ESCALA GEOGRÁFICA

A geração atual está excessivamente pulverizada.

A campanha Thalendor-521 possuía:

```text
6 reinos
29 cidades
48 vilas
77 localidades
```

Nesta fase, reduzir a escala.

Nova geração desejada:

```text
4 reinos
```

Cada reino possui:

```text
1 capital
4 cidades
```

Além disso, possuir algumas vilas subordinadas.

Alvo inicial aproximado:

```text
por reino:

1 capital
4 cidades
6–8 vilas
```

Total aproximado:

```text
4 capitais
16 cidades
24–32 vilas

44–52 localidades
```

Não tratar esses números como obrigação matemática se a geração precisar de pequena variação.

Mas preservar a estrutura:

```text
vilas > cidades
cidades > capitais
```

Uma capital deve ser rara.

---

# 2. DENSIDADE IMPORTA

A redução de localidades NÃO deve reduzir proporcionalmente a população persistente.

O objetivo é aumentar a densidade social.

Queremos mais:

```text
encontros
comércio
rumores
recrutamento
política
crime
investigação
religião
relações
ações coletivas
```

acontecendo em lugares compartilhados.

A geração deve diferenciar claramente:

```text
CAPITAL
CIDADE
VILA
```

não apenas pelo nome administrativo.

---

# 3. CAPITAL

Uma capital deve concentrar mais:

- população;
- comércio;
- autoridade;
- militares;
- culto;
- circulação de informação;
- propostas;
- organizações;
- visitantes.

A capital possui:

```text
governante / corte relevante
prefeito quando aplicável
general
estrutura militar mais forte
mercado maior
maior circulação de visitantes
```

Não criar sistemas de guerra nesta fase.

---

# 4. CIDADE

Cidade é centro regional.

Pode concentrar:

- prefeito;
- guarda;
- mercado;
- oficinas;
- grupos;
- cultos;
- possíveis sedes organizacionais;
- conexões com vilas próximas.

---

# 5. VILA

Vila é menor.

Deve depender mais das cidades para:

- autoridade;
- comércio especializado;
- decisões políticas;
- segurança regional;
- alguns serviços.

Isso deve tornar trajetos vila → cidade socialmente relevantes.

Uma vila não deve possuir automaticamente todas as instituições de uma cidade.

---

# 6. GRAFO DE ROTAS

Criar uma representação explícita da mobilidade entre localidades.

Conceitualmente:

```text
Locality
   │
   ├── Route
   │      ├── destination
   │      ├── distance
   │      ├── travel_time
   │      ├── terrain
   │      ├── danger
   │      ├── condition
   │      └── route_type
   │
   └── Route
```

O mundo forma um grafo.

Exemplo:

```text
Vila A
  |
  | estrada
  |
Cidade B
  |
  +---------- Capital
  |
  +---------- Vila C
```

---

# 7. NÃO EXISTE TELEPORTE GEOGRÁFICO POR CONHECIMENTO GLOBAL

Regra obrigatória:

```text
world knows destination
```

NÃO autoriza:

```text
NPC.travel(destination)
```

Para iniciar uma viagem voluntária até uma localidade específica, o NPC precisa possuir conhecimento suficiente de rota.

---

# 8. ROUTE KNOWLEDGE

Criar conhecimento de rota separado do simples conhecimento de uma localidade.

Algo conceitualmente como:

```text
RouteKnowledge
{
    actor
    origin
    destination
    route_id
    confidence
    source
    learned_at
    last_used_at
}
```

Um personagem pode saber:

> Karven existe.

sem saber:

> como chegar até Karven.

---

# 9. COMO UMA ROTA É APRENDIDA

Uma rota pode ser aprendida por meios causais.

Exemplos:

```text
nasceu/morou na região
já percorreu a rota
ouviu instruções
recebeu um mapa
seguiu outra pessoa
foi escoltado
viajou em grupo
aprendeu com comerciante
aprendeu com guarda
aprendeu com familiar
recebeu indicação institucional
```

Não criar conhecimento automaticamente só porque duas localidades estão próximas.

---

# 10. CONHECIMENTO LOCAL INICIAL

NPCs podem começar conhecendo algumas rotas coerentes com sua vida.

Exemplo:

```text
morador da vila
→ conhece caminho até cidade responsável pela região
→ conhece vilas vizinhas frequentes
```

Comerciante pode conhecer mais rotas.

Guarda pode conhecer rotas relevantes para sua jurisdição.

Governante pode conhecer importantes conexões do próprio reino.

Isso NÃO significa conhecimento completo do mapa.

---

# 11. ROTAS PODEM SER ENSINADAS

Permitir ação semântica equivalente a:

```text
AskRoute
GiveDirections
ShareRouteKnowledge
```

Exemplo:

```text
NPC A:
"preciso chegar a Karven"

NPC B conhece caminho

↓
RouteKnowledge transmitido
```

Confiança importa.

Uma informação incorreta pode gerar erro.

---

# 12. RUMORES SOBRE LUGARES

Preservar:

```text
ObjectiveTruth != Knowledge
```

Um personagem pode ouvir:

> Existe uma caverna ao norte de Valthon.

Isso pode ser:

- correto;
- parcialmente correto;
- desatualizado;
- falso;
- impreciso.

Rumor sobre um lugar NÃO concede automaticamente rota exata.

---

# 13. ROTAS DESCONHECIDAS

Se o NPC precisa alcançar um lugar mas não conhece rota:

candidate solutions podem incluir:

```text
ask_local
ask_guard
ask_trader
seek_guide
search_map
follow_known_traveler
explore
abandon
wait
```

Não:

```text
pathfind global coordinates
```

---

# 14. PATHFINDING FÍSICO != CONHECIMENTO

Separar claramente:

```text
KNOWLEDGE LAYER
```

de:

```text
PATHFINDING LAYER
```

O pathfinding pode calcular tecnicamente como atravessar uma rota conhecida.

Mas não pode conceder ao NPC conhecimento que ele não possui.

---

# 15. VIAGEM MULTIETAPA

Rotas podem exigir conexões.

Exemplo:

```text
Vila A
→ Cidade B
→ Capital C
→ Cidade D
```

O NPC pode conhecer somente:

```text
A → B
B → C
```

e não saber como continuar até D.

Nesse caso ele pode chegar à capital e precisar procurar informação novamente.

Isso é comportamento válido.

---

# 16. ROUTE PLANNING

Um personagem pode montar uma viagem usando apenas conexões conhecidas.

Conceitualmente:

```text
known_route_graph(actor)
```

e não:

```text
global_world_graph
```

A busca pelo caminho deve ocorrer sobre o grafo conhecido pelo agente.

---

# 17. ROTAS TÊM CUSTO

Considerar:

- distância;
- tempo;
- fome;
- sede;
- descanso;
- risco;
- condição física;
- dinheiro quando aplicável;
- companhia;
- perigo conhecido.

Uma rota conhecida pode ainda ser inviável.

---

# 18. ROTAS TÊM HISTÓRIA

Rotas podem adquirir eventos associados.

Exemplo:

```text
roubos
mortes
desaparecimentos
ataques
migrações
peregrinações
expedições
```

Isso pode produzir reputação social:

> Estrada de Valdor é perigosa.

A reputação deve vir de conhecimento transmitido.

---

# 19. PONTOS DE INTERESSE

Transformar Points of Interest em lugares utilizáveis pelo sistema.

Tipos atuais relevantes:

```text
quartel-general
castelo abandonado
caverna
```

Não manter esses locais como decoração procedural.

---

# 20. DESCOBERTA DE POI

POI pode ser:

```text
UNKNOWN
RUMORED
KNOWN
VISITED
EXPLORED
CLAIMED
```

conforme o tipo.

Um NPC não sabe automaticamente que todas as cavernas/castelos existem.

---

# 21. CAVERNAS

Cavernas devem poder possuir:

- profundidade;
- áreas internas abstratas;
- perigo;
- recursos;
- itens;
- restos mortais;
- criaturas futuras quando aplicável;
- eventos históricos;
- rumores;
- caminhos conhecidos/desconhecidos.

Não transformar toda caverna obrigatoriamente em dungeon.

Algumas podem ser:

```text
pequenas
vazias
úteis para abrigo
ricas em recurso
perigosas
historicamente relevantes
```

---

# 22. EXPLORAÇÃO DE CAVERNA

NPC precisa ter motivo para explorar.

Possíveis causas:

```text
rumor de recurso
rumor de artefato
necessidade econômica
procura por pessoa
fuga
missão organizacional futura
curiosidade
ambição
busca religiosa
procura por abrigo
```

Não:

```text
random NPC enters dungeon because dungeon exists
```

---

# 23. ITENS RAROS E HISTÓRICOS

Cavernas podem conter itens incomuns ou artefatos.

Mas separar:

```text
ACTUAL ITEM PROPERTIES
```

de:

```text
BELIEVED ITEM PROPERTIES
```

Uma espada comum pode ser considerada lendária.

Um artefato real pode ser desconhecido.

Um rumor de item lendário pode ser falso.

---

# 24. EXPEDIÇÕES

Uma pessoa pode concluir:

```text
explorar sozinho é arriscado
```

e procurar companhia.

Isso pode gerar:

```text
temporary expedition group
```

usando a infraestrutura de grupos existente quando possível.

Não criar um ExpeditionSystem totalmente separado se os sistemas existentes puderem representar isso.

---

# 25. CASTELOS ABANDONADOS

Castelos abandonados devem possuir utilidade espacial real.

Possíveis usos:

- abrigo;
- esconderijo;
- base;
- fortificação;
- sede de facção;
- culto;
- depósito;
- ponto de encontro;
- posição estratégica.

---

# 26. CLAIM LOCATION

Criar mecanismo semântico de reivindicação/ocupação de POI quando apropriado.

Exemplo:

```text
Faction needs HQ
↓
knows abandoned castle
↓
evaluates route
↓
evaluates danger
↓
travels
↓
occupies
↓
ClaimLocation
↓
FactionHQChanged
```

Não transformar ocupação em propriedade legal automática.

Outros atores podem contestar.

---

# 27. QUARTÉIS-GENERAIS EXISTENTES

As facções iniciais podem continuar com seus HQs.

Mas HQ agora deve participar de:

- recrutamento;
- armazenamento;
- reunião;
- liderança;
- atividades;
- conhecimento organizacional.

Sede não é apenas campo textual.

---

# 28. RECRUTAMENTO DE FACÇÕES

A campanha anterior mostrou duas facções com um único membro durante toda a simulação.

Corrigir esse gargalo de forma causal.

NÃO fazer:

```text
every X hours:
    recruit random NPC
```

---

# 29. COMO ALGUÉM CONHECE UMA FACÇÃO

O indivíduo precisa saber que ela existe.

Pode aprender por:

```text
encontro com membro
rumor
reputação
atividade pública
grupo local
trabalho
familiar
culto
passagem pela sede
convite
```

---

# 30. RECRUITMENT INTEREST

Uma facção pode desenvolver necessidade de pessoas.

Exemplos:

```text
few_members
workload
security
expansion
resource_need
loss_of_member
new_HQ
```

Isso cria pressão organizacional.

---

# 31. CANDIDATOS

Candidato deve possuir alguma coerência com a facção:

- profissão;
- valores;
- relações;
- reputação;
- experiência;
- necessidade;
- ideologia;
- fé quando relevante;
- localização/acesso.

Não precisa ser perfeito.

---

# 32. CONVITE E PEDIDO DE ADESÃO

Permitir os dois sentidos:

```text
Faction → InvitePerson
```

e:

```text
Person → RequestMembership
```

O outro lado pode:

```text
accept
reject
delay
request_condition
```

Não exigir diálogo textual nesta fase.

Usar ações semânticas.

---

# 33. GRUPO → FACÇÃO

Grupos locais duradouros podem se formalizar.

Não automaticamente.

Considerar fatores como:

```text
continuidade
membros
identidade compartilhada
objetivo persistente
liderança
recursos
necessidade organizacional
```

Quando esses elementos existirem, disponibilizar solução:

```text
FormalizeOrganization
```

Isso pode criar nova facção.

---

# 34. FACÇÕES PRECISAM DE RECURSOS

Facção com:

```text
0 moedas
0 estoque
1 membro
```

deve ter dificuldade real de agir.

Mas deve também conseguir tentar resolver isso.

Candidate actions:

```text
member contribution
paid work
trade
request support
recruit
claim resource site
explore
store supplies
```

Sem gerar dinheiro artificial.

---

# 35. FACÇÃO PODE BUSCAR NOVA SEDE

Se não possui HQ adequado:

```text
Need: organizational_base
```

Candidate solutions:

```text
use existing property
rent/buy future
construct future
claim abandoned castle
use cave temporarily
request space
```

Nesta fase priorizar reutilização dos POIs existentes.

---

# 36. GEOGRAFIA E FACÇÕES DEVEM CONVERSAR

Uma facção só pode recrutar alguém distante se houver caminho causal de contato.

Não:

```text
faction knows every NPC
```

Ela precisa:

```text
member travels
candidate visits
rumor/reputation spreads
institutional contact
```

---

# 37. ACESSO AOS DEUSES

A campanha anterior demonstrou:

```text
favor divino existe
```

mas contato forte continua extremamente raro.

Nesta fase, abrir rotas causais para que mortais possam BUSCAR contato divino.

Não aumentar simplesmente chance de intervenção.

---

# 38. SEEK DIVINE CONTACT

Permitir Goal/Commitment equivalente a:

```text
seek_divine_contact
```

quando existir causa suficiente.

Possíveis causas:

- devoção;
- desespero;
- ambição;
- curiosidade;
- perda importante;
- busca de poder;
- desejo de salvar alguém;
- vingança;
- interesse religioso;
- desejo de desafiar uma divindade;
- desejo de matar uma divindade quando histórico extremo justificar.

Nenhuma dessas causas deve automaticamente produzir o Goal.

---

# 39. COMO BUSCAR CONTATO DIVINO

Candidate solutions podem incluir:

```text
pray
seek_cultist
seek_devoted_follower
seek_favored_person
travel_to_sacred_region
seek_sacred_site
seek_relic
perform_known_ritual
follow_manifestation_rumor
```

Todas dependem de conhecimento.

---

# 40. LOCAL SAGRADO

Permitir que determinadas regiões/POIs adquiram significado religioso.

Não criar dezenas automaticamente.

Pode surgir por:

- presença divina histórica;
- ritual;
- manifestação;
- objeto associado;
- evento importante;
- tradição religiosa.

A pessoa precisa conhecer o local e uma rota até ele.

---

# 41. DIVINE ACCESS != DIVINE RESPONSE

Chegar a um lugar sagrado ou executar ritual não obriga Deus a responder.

Separar:

```text
access achieved
```

de:

```text
God chooses to respond
```

---

# 42. DIVINE AUDIENCE

Quando condições raras permitirem, criar:

```text
DivineAudience
```

como estado/evento semântico.

Pode acontecer por:

- manifestação;
- sinal direto;
- presença reconhecida;
- vínculo;
- ritual;
- convite do próprio Deus.

Não exige diálogo textual nesta fase.

---

# 43. CONTRATOS DIVINOS

Permitir estrutura genérica de pacto/contrato.

Algo como:

```text
DivineContract
{
    god
    mortal
    god_obligation
    mortal_obligation
    conditions
    status
    created_at
}
```

Exemplos:

```text
proteção ↔ serviço
poder ↔ dever religioso
conhecimento ↔ tarefa
favor ↔ proteção de seguidores
```

Não gerar contratos aleatoriamente.

---

# 44. CONTRATO NÃO SIGNIFICA OBEDIÊNCIA

Mortais podem:

```text
cumprir
falhar
recusar
abandonar
trair
```

Deus precisa aprender descumprimentos por canais válidos, salvo quando o próprio contrato estabelecer conhecimento direto dessa condição.

---

# 45. MANIFESTAÇÃO DIVINA

Preservar a cosmologia atual:

Deus possui presença regional invisível.

Para interação física direta, deve ocorrer manifestação.

```text
DivinePresence
→ Manifestation
→ physical interaction possible
```

Manifestar possui custo e risco.

---

# 46. DEUS FISICAMENTE VULNERÁVEL

Um mortal NÃO pode atacar uma divindade simplesmente usando seu ID.

Para confronto físico:

```text
God must be manifested / bound / physically accessible
```

Somente então ações físicas podem ser consideradas.

---

# 47. BUSCAR MATAR UM DEUS

Não criar:

```text
KillGodQuest
```

automática.

Esse objetivo só pode emergir de histórico extraordinário.

Possíveis bases:

- perda causada pelo Deus;
- conflito religioso extremo;
- pacto rompido conhecido;
- ambição excepcional;
- crença de que Deus deve morrer;
- busca de poder;
- vingança;
- contexto mítico.

Ainda precisa:

```text
knowledge
capacity
route
means
access
```

---

# 48. FORÇAR MANIFESTAÇÃO

Pode existir futuramente conhecimento/ritual capaz de:

```text
bind divine presence
```

ou exigir manifestação.

Nesta fase, implementar apenas se puder reutilizar arquitetura atual sem criar um sistema enorme.

Caso contrário:

documentar como extensão futura.

Não inflar escopo.

---

# 49. MORTE DIVINA E APOTEOSE

Preservar regra já existente:

```text
kill god
!=
become god
```

Após morte divina:

```text
released divine essence / seat
```

pode existir.

Mortal só se torna divino se:

```text
legitimately claims / appropriates essence
```

pelos requisitos existentes.

Não facilitar isso artificialmente apenas para produzir exemplo.

---

# 50. GEOGRAFIA DIVINA

A localização/presença divina precisa participar das rotas de acesso.

Se uma pessoa acredita que Neruma pode ser encontrada numa região distante:

ela ainda precisa:

```text
conhecer região
conhecer rota
sobreviver à viagem
chegar
realizar meio de contato
```

Divindade não remove geografia.

---

# 51. INFORMAÇÃO SOBRE POIS

Rumores podem envolver:

```text
cavernas
castelos
quartéis
artefatos
locais sagrados
manifestações
facções
```

Preservar:

```text
Fact
Claim
Knowledge
Belief
Rumor
```

---

# 52. EXPEDIÇÃO PODE PRODUZIR HISTÓRIA

Exemplo desejável, NÃO roteirizado:

```text
rumor de espada em uma caverna
↓
NPC acredita
↓
não conhece rota
↓
pergunta a comerciante
↓
aprende caminho
↓
recruta dois conhecidos
↓
viajam
↓
exploram
↓
um morre
↓
sobrevivente retorna
↓
rumor muda
↓
item ganha história
```

Não criar função que execute essa saga inteira.

Cada etapa deve usar sistemas normais.

---

# 53. CASTELO PODE PRODUZIR HISTÓRIA

Exemplo desejável:

```text
grupo cresce
↓
formaliza facção
↓
precisa de sede
↓
conhece castelo abandonado
↓
viaja
↓
ocupa
↓
estabelece HQ
```

Depois pode:

```text
armazenar recursos
receber candidatos
ser visitado
ser contestado
```

---

# 54. NÃO IMPLEMENTAR GUERRA

Mesmo com castelos e território:

NÃO adicionar nesta fase:

- guerra entre reinos;
- conquista territorial;
- exércitos nacionais completos;
- diplomacia internacional ampla.

Conflitos locais por POI podem ocorrer usando sistemas existentes.

---

# 55. NÃO IMPLEMENTAR DUNGEON CRAWLER COMPLETO

Caverna deve ser funcional, mas esta fase não precisa criar:

- dezenas de tipos de monstros;
- loot procedural gigantesco;
- classes;
- bosses;
- árvore de combate nova.

O foco é:

```text
acesso
descoberta
exploração
risco
história
```

---

# 56. NÃO IMPLEMENTAR DIÁLOGOS TEXTUAIS

Route sharing, recruitment, pactos e pedidos podem usar ações semânticas.

Diálogo textual continua fase futura.

---

# 57. AUDITORIA DE ROTAS

Para qualquer viagem relevante, deve ser possível responder:

```text
Quem viajou?
De onde?
Para onde?
Por quê?
Qual rota conhecia?
Como aprendeu a rota?
A rota era direta ou multietapa?
Havia recursos para viajar?
```

---

# 58. INVARIANTE PRINCIPAL DE VIAGEM

Criar auditoria:

```text
NPC iniciou viagem específica para localidade desconhecida
```

deve ser erro.

Também erro:

```text
NPC usou conexão ausente do seu grafo conhecido
```

Exceto ações explicitamente classificadas como:

```text
exploration
follow_person
escort
```

que possuam semântica própria.

---

# 59. FOLLOW / ESCORT

NPC pode chegar a lugar cuja rota pessoal não conhecia se:

```text
segue alguém que conhece
```

ou:

```text
é escoltado
```

Ao concluir viagem, pode aprender a rota percorrida conforme memória/cognição.

Isso NÃO é conhecimento prévio.

---

# 60. MIGRAÇÃO

Migração deve obedecer às mesmas regras.

```text
quero morar em X
```

não concede rota.

Migrante pode:

```text
buscar informação
seguir familiar
contratar/seguir guia
viajar por trechos conhecidos
```

---

# 61. BUSCAS E INVESTIGAÇÕES

Busca por pessoa também deve respeitar geografia.

Se investigador aprende:

> alvo foi para Karven

mas não conhece rota para Karven:

o próximo problema pode ser justamente:

```text
obtain_route_to(Karven)
```

Não teleportar investigação.

---

# 62. PROPOSTAS POLÍTICAS

Representantes de vilas continuam precisando viajar fisicamente para levar propostas.

Agora isso depende de rota conhecida.

Isso deve tornar:

```text
local access to authority
```

uma propriedade geográfica real.

---

# 63. ROTAS E ECONOMIA

Comércio deve respeitar conectividade.

Uma vila isolada pode ter:

```text
produção
```

mas acesso ruim ao mercado.

Uma cidade conectada pode receber:

```text
mais visitantes
mais comércio
mais rumores
```

Não reescrever economia inteira nesta fase.

Apenas fazer geografia participar onde já houver integração clara.

---

# 64. ROTAS E RUMORES

Rumores devem se espalhar principalmente por contato.

Rotas conectando locais criam corredores naturais de informação.

Não criar:

```text
rumor teleports between cities
```

---

# 65. DENSIDADE E METRÓPOLES

Após reduzir o número de localidades, verificar se as capitais/cidades realmente concentram mais:

- pessoas;
- conflitos;
- propostas;
- comércio;
- rumores;
- autoridades;
- cultos;
- recrutamento.

Não forçar número de eventos.

A concentração deve surgir do fluxo populacional e institucional.

---

# 66. TESTES

Manter validação barata.

Aproximadamente:

```text
8–10 testes novos
```

Prioridades:

1. NPC conhece localidade, mas não rota → não viaja diretamente;
2. NPC aprende rota com outro → pode viajar;
3. viagem multietapa usa apenas conexões conhecidas;
4. follow/escort permite viagem sem conhecimento prévio e pode ensinar caminho;
5. rumor de POI não equivale a rota;
6. facção consegue recrutar candidato conhecido/local;
7. grupo duradouro consegue formalizar facção em cenário controlado;
8. castelo abandonado pode tornar-se HQ;
9. mortal pode buscar contato divino usando rota/local conhecido;
10. Deus não é fisicamente atacável sem manifestação/acesso válido.

Rodar apenas smoke crítico adicional.

Não rodar suíte completa sem necessidade.

---

# 67. CAMPANHA NATURAL

NÃO repetir campanha de 1.000h como padrão.

Executar uma campanha natural de aproximadamente:

```text
300–400 horas
```

Preferência:

```text
350h
```

Uma seed.

Sem seed-shopping.

Sem alterar parâmetros durante execução.

Reiniciar apenas se houver falha estrutural que invalide a campanha.

---

# 68. O QUE OBSERVAR NA CAMPANHA

Não exigir evento raro.

Observar:

### Geografia

- população por capital/cidade/vila;
- viagens;
- rotas aprendidas;
- viagens multietapa;
- falhas por falta de rota;
- migração;
- concentração urbana.

### POIs

- descobertas;
- visitas;
- explorações;
- rumores;
- claims;
- mudança de HQ.

### Facções

- conhecimento da organização;
- recruitment interest;
- convites;
- pedidos de adesão;
- novos membros;
- promoções se existentes;
- formalização de novos grupos.

### Divino

- Goals de buscar contato;
- jornadas religiosas;
- acesso a local sagrado;
- audiências;
- contratos;
- manifestações;
- confrontos se naturalmente ocorrerem.

---

# 69. NÃO EXIGIR APOTEOSE

Uma campanha sem:

```text
god killed
new god
divine contract
manifestation
```

pode ser perfeitamente válida.

Esses eventos devem continuar raros.

O critério é comprovar que existem caminhos causais para chegar até eles.

---

# 70. MÉTRICAS DE ACESSO

Adicionar relatório compacto:

```text
RouteKnowledgeCreated
RouteKnowledgeShared
RouteUnknownBlockedTravel
MultiHopJourney
FollowJourney
EscortJourney
POIDiscovered
POIVisited
POIExplored
POIClaimed
FactionRecruitmentInterest
FactionInvite
FactionJoinRequest
FactionMemberJoined
GroupFormalized
SeekDivineContact
SacredJourney
DivineAudience
DivineContract
DivineManifestation
```

Somente registrar o que realmente existir.

Não gerar eventos vazios só para telemetria.

---

# 71. HISTÓRIAS REAIS

O `HISTORIAS_REAIS.md` desta fase deve procurar histórias espaciais.

Selecionar aproximadamente 6–8 trajetórias interessantes.

Priorizar exemplos como:

- alguém que queria ir a um lugar mas primeiro precisou aprender a rota;
- migração multietapa;
- perseguição limitada por conhecimento geográfico;
- exploração de caverna;
- rumor de artefato;
- grupo que ocupou castelo;
- recrutamento de facção;
- alguém viajando para buscar uma divindade;
- contrato ou manifestação, se ocorrer naturalmente.

Não inventar caso ausente.

---

# 72. RELATÓRIO DO MUNDO

Preservar o formato `MUNDO.md`.

Incluir especialmente:

```text
4 reinos
capitais
cidades
vilas
POIs
rotas
densidade populacional
rotas mais utilizadas
localidades mais conectadas
localidades mais isoladas
facções e sedes
explorações
religião
```

O relatório deve permitir enxergar se a nova geografia realmente produziu centros sociais distintos.

---

# 73. CRITÉRIO DE SUCESSO

A fase terá cumprido seu objetivo quando o mundo demonstrar:

```text
PERSON KNOWS PLACE
but
DOES NOT KNOW ROUTE
→ cannot simply travel there
```

e depois:

```text
learns route
→ can plan journey
→ travels physically
→ potentially learns new places/routes
```

Além disso, deve haver evidência de que POIs e organizações agora participam das decisões dos agentes.

---

# 74. PRINCÍPIO FINAL

Não queremos um mapa que existe apenas para o motor.

Queremos um mundo em que:

```text
onde você está
o que você conhece
quem você conhece
que caminhos conhece
quanto custa chegar
o que acredita existir lá
```

mudem o que você é capaz de fazer.

Uma caverna desconhecida não existe socialmente para aquela pessoa.

Um Deus distante não é acessível porque seu ID existe.

Uma facção não recruta alguém que nunca encontrou ou ouviu falar dela.

Uma autoridade não recebe uma proposta que ninguém conseguiu levar.

Um assassino não persegue alguém através de um mapa que ele não conhece.

**Geografia deve limitar, conectar e criar história.**