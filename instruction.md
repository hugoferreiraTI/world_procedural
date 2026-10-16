# Visão Geral

A ideia deste projeto é desenvolver um jogo baseado em geração procedural praticamente total. NPCs, itens, facções, reinos, relações, eventos e outros elementos do mundo deverão ser gerados proceduralmente.

O jogo será baseado em turnos e utilizará um sistema de locomoção através de uma matriz. O jogador poderá se movimentar para norte, sul, leste e oeste.

Um dos principais objetivos do projeto é criar um mundo que funcione independentemente do jogador. NPCs possuem suas próprias relações, profissões, rotinas, necessidades e objetivos. Quests não deverão existir apenas como missões previamente programadas, mas também poderão surgir naturalmente como consequência dos acontecimentos da simulação.

# NPCs

O jogador poderá conversar com qualquer NPC existente no mundo. Entretanto, nem todos os NPCs terão o mesmo nível de profundidade narrativa ou importância para a simulação.

Os NPCs serão separados inicialmente nas seguintes categorias:

- Lendário: deuses, entidades ou humanos considerados lendários.
- Importante: políticos, reis, líderes, personagens de alto escalão, humanos extremamente poderosos ou indivíduos relevantes para o mundo.
- Comum: habitantes comuns, trabalhadores, soldados, comerciantes e outros personagens cotidianos.

A classificação poderá determinar o nível de profundidade da geração, dos diálogos, das memórias, dos objetivos e da participação do NPC na simulação.

# Sistema de Família

Durante a geração de um NPC poderá existir uma verificação para determinar se ele possui família.

Caso um personagem chamado John Hammer seja casado e tenha filhos, a geração deverá manter coerência entre os membros da família. Sua esposa e seus filhos poderão compartilhar o sobrenome Hammer de acordo com as regras culturais estabelecidas pelo mundo.

As relações familiares deverão fazer parte do sistema de relacionamentos entre entidades.

# Sistema de Relacionamentos

Os relacionamentos serão representados através de uma estrutura baseada em grafos.

NPCs poderão possuir relações com outros NPCs, facções, entidades religiosas e outros elementos do mundo.

As relações não deverão utilizar nomes como identificadores principais. Cada entidade deverá possuir um identificador único e estável, permitindo que nomes sejam repetidos ou alterados sem quebrar as relações existentes.

Entre NPCs, relações como família, amizade, rivalidade, lealdade, casamento e outras poderão ser representadas através desse sistema.

A lealdade poderá possuir valores entre 0 e 100, representando o grau de fidelidade ou comprometimento de uma entidade em relação a outra.

# Sistema de Necessidades e Quests Emergentes

As quests deverão surgir principalmente através das necessidades dos personagens e das situações criadas pela própria simulação.

Exemplo:

John Hammer possui uma esposa. Todas as manhãs, ela segue sua rotina de ir até uma vila vizinha para comprar comida. Em determinado dia, ela não retorna.

O estado real do mundo pode conter a informação de que algo aconteceu com ela, porém John não deverá automaticamente possuir essa informação.

John apenas percebe que sua esposa deveria ter retornado e ainda está desaparecida.

Essa percepção gera uma necessidade:

`Encontrar esposa`

A necessidade poderá gerar um objetivo:

`Descobrir onde sua esposa está`

Dependendo das relações existentes, da personalidade do personagem e das possibilidades disponíveis, John poderá procurar ajuda.

Caso ele peça ajuda ao jogador, essa necessidade poderá se transformar em uma quest para o jogador.

Portanto, a estrutura conceitual será:

`Estado do mundo -> Percepção do NPC -> Necessidade -> Objetivo -> Ação -> Possível Quest`

Uma quest deverá ser consequência do estado da simulação, e não obrigatoriamente um evento criado isoladamente pelo sistema.

Esse princípio deverá se aplicar também a personagens importantes.

Um líder de facção poderá possuir necessidades como eliminar determinado personagem, recuperar um item, conquistar território, obter recursos, proteger uma cidade ou enfraquecer uma facção rival.

# Conhecimento dos NPCs

O mundo possuirá um estado objetivo, porém os NPCs não deverão possuir conhecimento automático sobre tudo que acontece.

Cada NPC deverá tomar decisões utilizando apenas informações que conhece, percebeu ou recebeu através de outras entidades.

Isso significa que uma informação existente no estado global do mundo não necessariamente estará disponível para todos os personagens.

Esse princípio permitirá futuramente a existência de rumores, mentiras, informações incorretas, investigações, propaganda, conhecimento desatualizado e outros comportamentos emergentes.

# Profissões

Todos os NPCs poderão possuir uma ocupação.

Exemplos iniciais:

- Ferreiro
- Cozinheiro
- Guarda
- Soldado
- Caçador
- Comerciante
- Estudante

NPCs sem profissão formal poderão utilizar uma ocupação nula ou categorias específicas de acordo com sua condição.

O termo `Estudante` poderá ser utilizado principalmente para crianças ou personagens que estejam estudando, mas não deverá representar obrigatoriamente qualquer personagem sem profissão.

As profissões deverão possuir impacto real sobre o mundo.

Um ferreiro deverá poder produzir armas ou armaduras.

Um cozinheiro poderá trabalhar como vendedor, funcionário de uma taverna, cozinheiro particular ou exercer outras funções relacionadas.

Guardas deverão exercer atividades de proteção ou patrulhamento.

Caçadores poderão obter recursos através da caça.

A profissão não deverá existir apenas como informação textual do personagem.

# Fé e Religião

NPCs possuirão um sistema relacionado à religião e à fé.

A religião ou crença deverá representar qual deus, conjunto de deuses ou sistema religioso o personagem segue.

Essa escolha poderá normalmente ser influenciada pelo reino, região, cultura ou família em que o personagem nasceu ou vive.

A intensidade da fé deverá ser separada da religião escolhida.

Exemplo:

`Religião: Culto do Sol`

`Devoção: 15/100`

Esse personagem pertence culturalmente à religião, porém possui pouca devoção.

Outro personagem poderá possuir:

`Religião: Culto do Sol`

`Devoção: 95/100`

Nesse caso, sua religião possui grande influência sobre suas decisões e comportamento.

# Lealdade

NPCs poderão possuir níveis de lealdade em relação a outros NPCs, facções, líderes ou organizações.

A lealdade poderá utilizar inicialmente uma escala de 0 a 100.

Essa informação deverá fazer parte do sistema de relacionamentos e utilizar identificadores únicos das entidades relacionadas.

# Popularidade e Reputação

Popularidade e reputação deverão representar conceitos diferentes.

Popularidade representa o quanto determinado personagem é conhecido.

Reputação representa o motivo pelo qual esse personagem é conhecido e como diferentes grupos interpretam suas ações.

Um personagem conhecido por assassinar pessoas não deverá automaticamente ser tratado como um excelente cozinheiro apenas porque possui alta popularidade.

A reputação deverá manter contexto sobre feitos, comportamentos ou características pelas quais o personagem se tornou conhecido.

Diferentes NPCs ou facções também poderão possuir opiniões diferentes sobre a mesma pessoa.

# Jogador

O jogador possuirá inicialmente os seguintes campos:

```text
name
nickname
faction
health
inventory
```

`name` representa o nome do personagem.

`nickname` representa o apelido ou título pelo qual o personagem é conhecido. Por padrão, o jogador deverá começar como `Desconhecido`. Novos apelidos poderão surgir ao longo da campanha através de suas ações e reputação.

`faction` representa a facção atual do jogador. Por padrão, o jogador não pertence a nenhuma facção.

`health` representa sua vida atual. O valor inicial será 100.

`inventory` será responsável pelos itens carregados pelo jogador e deverá utilizar uma estrutura apropriada para armazenar referências aos itens.

# Princípios de Arquitetura Já Definidos

O mapa será representado através de uma matriz, responsável principalmente pela localização espacial e movimentação das entidades.

Os relacionamentos serão representados através de grafos.

O sistema deverá priorizar modularidade e reutilização.

As entidades deverão utilizar identificadores únicos para permitir referências seguras entre diferentes sistemas.

O código deverá evitar estruturas excessivamente acopladas ou objetos responsáveis por todos os sistemas ao mesmo tempo.

Sistemas como relacionamentos, necessidades, profissões, rotina, reputação e conhecimento deverão permanecer separados sempre que possível.

A lógica principal do jogo não deverá depender diretamente da interface utilizada.

# 1. Sistema de Geração Procedural

O objetivo não é criar um jogo infinito, mas um mundo finito com conteúdo fortemente procedural. Por isso, alguns parâmetros globais serão definidos previamente, enquanto o conteúdo interno será aleatorizado a partir da seed.

O mundo iniciará com até **6 reinos**. Esses reinos serão gerados proceduralmente e funcionarão como facções de grande escala.

Cada reino poderá conter entre **4 e 6 cidades**. Uma dessas cidades será obrigatoriamente a capital do reino e deverá possuir escala, importância e quantidade de estruturas superiores às demais.

As cidades serão representadas por matrizes próprias, separadas da matriz global do mundo.

Uma cidade pode, por exemplo, possuir uma matriz `5x5` apenas para fins demonstrativos. As posições presentes nas extremidades da matriz representam as muralhas da cidade. Dessa forma, a primeira e última linha e a primeira e última coluna constituem o perímetro defensivo da cidade.

Exemplo conceitual:

```text
X X X X X
X . . . X
X . . . X
X . . . X
X X X X X
```

- `X` representa a muralha.
- `.` representa uma posição interna da cidade.

O tamanho real das cidades poderá ser consideravelmente maior. A matriz `5x5` é apenas um exemplo para demonstrar a lógica estrutural.

As posições internas da cidade não representam obrigatoriamente uma única construção física. Uma posição pode representar uma área ou conjunto de estruturas.

Por exemplo, uma posição poderá conter:

```text
Distrito residencial
10 casas
32 NPCs
```

Ou:

```text
Distrito comercial
2 lojas
1 ferreiro
1 taverna
14 NPCs
```

O jogador deverá possuir uma ação `listar`, responsável por mostrar o conteúdo disponível na posição atual.

Exemplo:

```text
Local: Distrito Comercial

Estruturas:
- Ferreiro
- Taverna
- Loja de alimentos

NPCs presentes:
- John Hammer
- Marie Stone
- Arthus Vale
```

Uma cidade poderá conter diferentes tipos de áreas e estruturas, incluindo:

- Casas
- Lojas
- Tavernas
- Ferreiros
- Quartéis
- Igrejas
- Mercados
- Palácios
- Praças
- Distritos residenciais
- Distritos comerciais
- Estruturas administrativas
- Estruturas militares

A quantidade, distribuição e organização dessas estruturas deverão variar proceduralmente.

## Exterior das cidades

Fora das cidades, o mundo será composto por terrenos, biomas e pontos de interesse.

Os biomas iniciais poderão incluir:

- Floresta
- Planície
- Deserto
- Pântano

Novos biomas poderão ser adicionados posteriormente.

O exterior também poderá conter pontos de interesse.

### Vilas

A maioria das vilas deverá estar vinculada a algum reino e, normalmente, localizada nas proximidades de uma cidade.

Uma vila poderá pertencer administrativamente a uma cidade ou diretamente a um reino.

Também poderão existir vilas independentes que não pertencem a nenhum reino.

### Cavernas

Cavernas utilizarão um sistema de interior próprio.

Ao entrar em uma caverna, o jogador poderá acessar uma matriz local separada da matriz global do mundo.

### Castelos abandonados

Castelos abandonados também utilizarão o sistema de interiores e possuirão sua própria estrutura procedural.

### Quartéis-generais de grupos ou facções

Quartéis-generais importantes não deverão ser tratados apenas como interiores simples.

Eles poderão possuir matrizes próprias, de maneira semelhante às cidades, permitindo diferentes áreas internas, estruturas e NPCs.

# 2. Sistema de Seed e Aleatoriedade

O sistema de seed possuirá uma característica narrativa.

Em vez de utilizar apenas um valor numérico apresentado diretamente ao jogador, a seed poderá ser representada pelo nome de um personagem primordial responsável por desencadear acontecimentos importantes da geração inicial do mundo.

Exemplo:

```text
Seed: Dovha
```

Dovha não será apenas um texto utilizado para iniciar o gerador. Ele será um personagem real e persistente dentro do mundo e poderá ser encontrado durante a campanha caso continue vivo e acessível.

A string `Dovha` deverá ser convertida internamente em uma seed determinística utilizada pelo gerador procedural.

Portanto, mundos criados com a mesma seed e mesma versão das regras de geração deverão produzir os mesmos resultados iniciais.

O personagem ligado à seed poderá receber características, relações e eventos iniciais gerados proceduralmente.

Exemplo conceitual:

```text
Dovha
↓
Líder da Facção dos Dragões
↓
Liderou um exército contra um reino rival
↓
O reino rival foi destruído
↓
Suas antigas cidades tornaram-se ruínas
↓
Outros reinos reagiram
↓
Iniciou-se uma guerra em grande escala
```

Esse processo deverá fazer parte da geração da história inicial do mundo.

Portanto, a geração não deverá apenas criar estruturas estáticas. Ela também poderá executar uma quantidade limitada de acontecimentos históricos antes do início da campanha.

Isso significa que um mundo teoricamente configurado para possuir 6 reinos poderá começar a partida com apenas 5 ativos caso um deles tenha sido destruído durante a geração histórica.

O reino destruído poderá continuar existindo no estado do mundo através de:

- Ruínas
- Antigos territórios
- Sobreviventes
- Famílias nobres
- Refugiados
- Facções remanescentes
- Itens históricos
- Relações políticas
- Memórias de personagens

A geração deverá utilizar aleatoriedade controlada pela seed.

Nenhum sistema deverá utilizar geradores aleatórios independentes sem relação com a seed principal quando o resultado fizer parte da geração determinística do mundo.

# 3. Sistema de Mapa e Geração do Mundo

O mundo será representado inicialmente por uma matriz global de:

```text
500 x 500
```

Totalizando **250.000 posições**.

Cada posição representa uma área do mundo e não necessariamente deverá possuir uma construção ou ponto de interesse.

Grande parte das posições poderá representar somente terreno atravessável.

Antes do início da campanha, o gerador deverá criar a estrutura inicial do mundo.

A geração deverá ocorrer em etapas lógicas.

Exemplo conceitual:

```text
Seed
↓
Geração dos biomas
↓
Definição das regiões
↓
Geração dos reinos
↓
Distribuição territorial
↓
Geração das cidades e capitais
↓
Geração das vilas
↓
Geração de facções menores
↓
Geração dos pontos de interesse
↓
Geração dos NPCs principais
↓
Geração das relações iniciais
↓
Simulação histórica inicial
↓
Estado inicial jogável
```

A ordem exata poderá ser refinada durante o desenvolvimento, porém sistemas dependentes não deverão ser gerados antes de suas dependências.

## Territórios

Cada reino deverá possuir uma região territorial dentro do mapa global.

Os territórios não precisam possuir formato perfeitamente quadrado no resultado final, embora blocos possam ser utilizados inicialmente para facilitar a geração.

Somente um reino poderá receber a classificação inicial de `Grande Reino`.

Esse reino poderá possuir uma área máxima aproximada de até:

```text
100 x 100
```

Dentro da matriz global.

Isso não significa que todas essas posições serão ocupadas por cidades.

Grande parte do território deverá continuar sendo composta por:

- Terrenos
- Estradas
- Florestas
- Vilas
- Ruínas
- Recursos
- Acampamentos
- Estruturas menores
- Pontos de interesse

As cidades e a capital ocuparão apenas uma parcela desse território.

Os demais reinos deverão possuir territórios proporcionalmente menores.

Os territórios deverão respeitar espaço suficiente para exploração entre cidades e pontos importantes.

## Distância entre pontos de interesse

Cidades, vilas, estruturas e outros pontos relevantes não deverão surgir obrigatoriamente em posições adjacentes.

Durante a geração deverá existir uma distância mínima configurável entre determinados tipos de pontos de interesse.

Como valor inicial de desenvolvimento, poderá ser utilizada uma distância mínima aproximada de **5 células**.

Esse valor não deverá ser fixo em todas as situações.

O gerador poderá escolher distâncias maiores dentro de limites configuráveis.

Exemplo:

```text
minimumDistance = 5
maximumDistance = valor configurável
```

Diferentes tipos de estruturas poderão possuir diferentes regras de distância.

## Navegação do jogador

O jogador estará sempre localizado em uma posição da matriz global ou de uma matriz local.

Na matriz global, a movimentação ocorrerá utilizando os quatro pontos cardeais:

- Norte
- Sul
- Leste
- Oeste

Não haverá inicialmente movimentação diagonal.

## Mapa visível ao jogador

Embora o mundo possua uma matriz global de `500x500`, o jogador não visualizará toda a matriz simultaneamente.

A interface deverá apresentar inicialmente uma janela de:

```text
5 x 5
```

Centralizada ou posicionada em relação ao jogador.

Essa matriz `5x5` representa apenas a área atualmente visível da matriz global.

Exemplo:

```text
. . . . .
. F F . .
. F @ R .
. . R C .
. . . . .
```

Onde:

- `@` = jogador
- `F` = floresta
- `R` = estrada
- `C` = cidade
- `.` = terreno comum ou desconhecido

Mover o jogador não significa mover uma matriz `5x5` independente pelo mundo.

O jogador possuirá coordenadas reais dentro da matriz global, e a interface apenas exibirá uma região `5x5` ao redor dessas coordenadas.

## Diferentes escalas de mapa

O sistema deverá distinguir claramente a matriz global das matrizes locais.

### Matriz global

Representa o mundo externo.

```text
500 x 500
```

Pode conter:

- Terrenos
- Biomas
- Cidades
- Vilas
- Ruínas
- Estradas
- Cavernas
- Quartéis-generais
- Outros pontos de interesse

### Matriz de cidade

Representa o interior navegável de uma cidade.

Seu tamanho poderá variar dependendo da cidade.

### Matriz de interior

Representa interiores específicos como:

- Cavernas
- Castelos
- Masmorras
- Estruturas especiais

Essas matrizes serão geradas separadamente e associadas à posição correspondente no mundo global.

O sistema deverá evitar interpretar uma célula da matriz global, uma célula da matriz urbana e uma célula de interior como possuindo obrigatoriamente a mesma escala física.

## 4. Sistema de Biomas e Terrenos
Terreno: Para fins de não exarcebar na complexidade, os terrenos mesmo sendo diferentes. não afetarão a locomoção ou combate.

Biomas: Eles sim, terão grande influencia, um terreno de deserte poderá tirar o status "sede" mais rapidamente, deixar com mais fome, e mais sonolento o player - o foco do jogo será relações e efeitos borboleta, por isso não irei focar muito em terreno e bioma.

## 5. Sistema de Locomoção
O jogador irá se mover por pontos cardiais. Obviamente, caso a posição que ele vá seja por exemplo uma MURALHA de uma cidade e não um portão, ele será barrado de conseguir passar.
## 6. Sistema de Turnos
Extremamente importante:
Os turnos andarão junto no mundo. Como assim? No caso sempre que o jogador andar ou fazer um movimento, o mundo faz junto com ele, como eu disse NPCs e o mundo em si não fica parado, então 1 turno que será equivalente a 1 hora - mesmo sendo, estranho, 1 matriz de posição conterá uma hora sim - jogador faz um movimento - mundo faz junto. O sistema de necessidade irá mover o mundo inteiro.

## 7. Sistema de Tempo
Não terá grande impacto na jogatina os diferentes tempos.

## 8. Sistema de Rotinas dos NPCs
Tudo dependerá do sistema de necessidade. Caso seja por exemplo um vendedor de comida, porém que no momento está passando por um aperto financeiro, ele poderá colocar promoções na suas vendas. Ou então caso sua filha ou algum parente que ele ame muito, suma, ele poderá acordar e tomar a decisão que irá procura-la, ja não mais estando na sua loja. Caso a necessidade do npc esteja estabilziada (nesse caso, sem necessidade), ele terá sua rotina normal, acorda, trabalha, volta pra casa.

## 9. Sistema de Necessidades
## 9. Sistema de Necessidades

O sistema de necessidades é o sistema mais importante de todo o jogo. Ele será responsável por movimentar grande parte do ecossistema e deverá funcionar mesmo sem qualquer interferência do jogador.

A primeira regra fundamental é:

**Necessidade não é ação. Necessidade é um estado que pressiona uma entidade a buscar uma solução.**

Uma necessidade poderá surgir a partir de mudanças no estado do mundo, condições individuais, relações entre personagens, falta de recursos, acontecimentos políticos, conflitos, crenças, objetivos ou outros fatores.

A ação escolhida para resolver essa necessidade dependerá de outros sistemas, principalmente do sistema de personalidade.

De forma conceitual:

```text
Estado do mundo
↓
Necessidade
↓
Personalidade + contexto + conhecimento + recursos disponíveis
↓
Possíveis soluções
↓
Ação escolhida
↓
Consequência
↓
Novo estado do mundo
```

### Necessidades e consequências em cadeia

As necessidades deverão ser capazes de gerar consequências que criam novas necessidades em outras entidades ou sistemas.

Utilizando Dovha como exemplo:

Dovha exterminou um reino durante a geração histórica inicial e provocou uma guerra em grande escala.

A guerra causa redução na produção e problemas comerciais.

```text
Guerra
↓
Menor disponibilidade de alimentos
↓
Preço dos alimentos aumenta
↓
Mais NPCs sentem dificuldade para conseguir comida
```

A partir disso, diferentes consequências poderão surgir.

Alguns NPCs poderão começar a roubar para suprir sua necessidade de alimentação.

```text
Fome
↓
Aumento de roubos
↓
Ruas tornam-se mais perigosas
```

O aumento da criminalidade gera novas necessidades para cidades e governos.

```text
Criminalidade aumenta
↓
Necessidade de segurança aumenta
↓
Mais guardas são contratados
↓
Mais pessoas entram para atividades militares
```

O aumento da atividade militar também afeta outros setores.

```text
Mais soldados
↓
Maior demanda por armas e armaduras
↓
Preço de armas e armaduras aumenta
```

Ao mesmo tempo, parte da população que anteriormente exercia profissões artesanais poderá migrar para atividades militares.

```text
Maior militarização
↓
Menos mão de obra artesanal
↓
Menor produção de determinados produtos
↓
Produtos artesanais ficam mais caros
```

Esse processo poderá continuar afetando outros sistemas.

O objetivo é permitir que uma alteração relevante no mundo possa gerar uma cadeia de consequências emergentes sem a necessidade de acontecimentos previamente roteirizados.

### Necessidade e personalidade

Nem todos os NPCs deverão responder à mesma necessidade da mesma maneira.

O sistema de personalidade será um dos principais responsáveis por determinar qual solução o personagem considera aceitável.

Portanto:

```text
Necessidade + Personalidade + Contexto = Tendência de ação
```

Por exemplo, diferentes NPCs com fome poderão reagir de maneiras diferentes.

Um personagem honesto poderá:

- Procurar trabalho
- Pedir ajuda
- Comprar comida caso possua dinheiro

Um personagem agressivo poderá:

- Ameaçar alguém
- Roubar comida
- Atacar um comerciante

Um personagem independente poderá:

- Caçar
- Pescar
- Procurar alimentos no ambiente

Um personagem extremamente leal à sua comunidade poderá dividir os poucos recursos que possui mesmo estando com fome.

A necessidade é semelhante, mas a resposta deverá variar conforme personalidade, conhecimento, profissão, recursos, relações e contexto.

### Necessidades geradas por relações pessoais

O sistema de relacionamentos deverá possuir forte influência sobre as necessidades.

Exemplo:

O jogador mata um soldado inimigo.

O filho desse soldado possui idade suficiente para compreender o acontecimento e está dentro da área em que consegue presenciar a morte.

Nesse momento, o personagem recebe conhecimento sobre o acontecimento:

```text
Pai morto pelo jogador
```

Esse evento poderá gerar estados emocionais e necessidades relacionadas à perda.

Entretanto, isso não significa que todos os personagens buscarão vingança.

A personalidade deverá influenciar o resultado.

Um personagem com características como:

- Vingativo
- Rancoroso
- Agressivo
- Extremamente leal à família

poderá desenvolver uma necessidade relacionada à vingança.

Exemplo:

```text
Necessidade:
Responder à morte do pai

Possível objetivo:
Matar o jogador
```

Outro personagem poderá possuir personalidade diferente e buscar outras respostas.

Exemplos:

```text
Fugir do jogador
```

```text
Denunciar o jogador
```

```text
Procurar proteção
```

```text
Entrar para uma facção inimiga do jogador
```

```text
Abandonar a região
```

Portanto, a necessidade não deverá determinar diretamente uma única ação.

### Necessidades em escala de reino

O mesmo sistema deverá ser aplicável a entidades maiores, como facções e reinos.

Exemplo:

O Reino X possui grande produção de trigo.

O Reino Y sofre com escassez de alimentos.

Inicialmente, o Reino Y tenta comprar trigo do Reino X.

Entretanto, o Reino X começa a aumentar excessivamente o preço do recurso.

O Reino Y passa a possuir uma necessidade crítica de alimentação para sua população.

```text
Escassez de alimentos
↓
Necessidade de obter trigo
```

O reino deverá avaliar diferentes soluções possíveis.

Exemplos:

```text
Negociar preços
```

```text
Buscar outro fornecedor
```

```text
Expandir produção própria
```

```text
Criar novas rotas comerciais
```

```text
Roubar carregamentos
```

```text
Invadir território produtor
```

Caso fatores políticos, militares, econômicos e de personalidade de seus líderes favoreçam uma solução agressiva, essa necessidade poderá resultar em guerra.

```text
Necessidade alimentar
↓
Falha em soluções diplomáticas ou econômicas
↓
Solução militar considerada viável
↓
Guerra
```

Dessa forma, guerras poderão surgir organicamente através da simulação, sem depender da participação do jogador.

### Necessidades relacionadas ao jogador

O jogador também poderá se tornar alvo direto das necessidades de NPCs, facções e reinos.

Exemplo:

O jogador alcançou um nível lendário de feitos e tornou-se amplamente conhecido.

Ao mesmo tempo, ele é inimigo declarado de determinada facção.

Essa facção poderá possuir a necessidade de neutralizar a ameaça representada pelo jogador.

Uma das possíveis soluções será criar uma recompensa por sua morte ou captura.

```text
Jogador representa ameaça
↓
Facção precisa neutralizar jogador
↓
Recompensa criada
```

Essa recompensa poderá se espalhar através do sistema de rumores e informações.

NPCs compatíveis poderão tomar conhecimento dela.

Mercenários, criminosos, caçadores de recompensa ou pessoas desesperadas poderão decidir perseguir o jogador caso suas personalidades, necessidades e interesses tornem essa ação atraente.

Exemplo:

```text
Mercenário possui dívida
↓
Descobre recompensa pelo jogador
↓
Necessidade de dinheiro + personalidade compatível
↓
Objetivo: localizar jogador
↓
Inicia caçada
```

A localização do jogador não deverá ser automaticamente conhecida.

A perseguição deverá depender do sistema de rumores, informações, avistamentos e conhecimento dos NPCs.

### Regra central

O sistema deverá evitar lógica direta do tipo:

```text
NPC está com fome
→ roubar comida
```

O comportamento esperado deverá seguir uma estrutura semelhante a:

```text
NPC está com fome
↓
Necessidade de conseguir alimento
↓
Sistema avalia possíveis soluções conhecidas
↓
Personalidade e contexto modificam a preferência por cada solução
↓
Uma solução é escolhida
↓
NPC cria um objetivo
↓
O objetivo gera ações
```

Essa separação é obrigatória para evitar que todos os NPCs reajam da mesma maneira aos mesmos acontecimentos.

### Necessidades em diferentes escalas

O sistema de necessidades deverá funcionar em diferentes níveis da simulação.

#### NPCs

Exemplos:

- Fome
- Segurança
- Dinheiro
- Encontrar familiar
- Vingança
- Trabalho
- Proteção
- Fé
- Status
- Poder

#### Famílias

Exemplos:

- Encontrar membro desaparecido
- Conseguir comida
- Proteger residência
- Melhorar condição financeira

#### Facções

Exemplos:

- Obter recursos
- Recrutar membros
- Eliminar rival
- Expandir influência
- Proteger território

#### Reinos

Exemplos:

- Alimentar população
- Defender fronteira
- Conseguir recursos estratégicos
- Resolver crise econômica
- Expandir território
- Neutralizar ameaça externa

A escala muda, mas o princípio deverá permanecer o mesmo:

```text
Problema ou desejo
↓
Necessidade
↓
Avaliação de soluções
↓
Objetivo
↓
Ação
↓
Consequência
```

### Princípio de autonomia do mundo

O sistema de necessidades deverá continuar funcionando mesmo que o jogador permaneça completamente parado.

NPCs continuarão tomando decisões.

Facções continuarão perseguindo seus interesses.

Reinos poderão entrar em conflito.

Recursos poderão ficar escassos.

Preços poderão mudar.

Personagens poderão morrer.

Novas necessidades poderão surgir.

O jogador é uma entidade dentro da simulação, e não o centro obrigatório de todos os acontecimentos.

## Sistema de Prioridade e Conflito de Necessidades
Cada entidade poderá possuir múltiplas necessidades ao mesmo tempo.

Um NPC poderá estar com fome, cansado, com medo, preocupado com um familiar e ainda possuir obrigações profissionais.

O sistema deverá decidir continuamente qual necessidade merece maior atenção.

A existência de uma necessidade não significa que ela será resolvida imediatamente.

Cada necessidade possuirá um valor de prioridade calculado dinamicamente.

Exemplo:

Fome: 45
Sono: 30
Trabalho: 55
Encontrar filho desaparecido: 92
Pagar dívida: 70

Nesse cenário, a necessidade relacionada ao filho desaparecido possui maior prioridade e tende a se transformar no objetivo principal do NPC.

Estrutura básica de uma necessidade

Uma necessidade deverá conter informações suficientes para permitir rastreamento, atualização e tomada de decisão.

Exemplo conceitual:

Need

ID
OwnerID
Type
TargetID
BaseUrgency
CurrentPriority
CreatedAt
UpdatedAt
Status
Source
Reason

OwnerID representa a entidade que possui a necessidade.

Type representa o tipo da necessidade.

TargetID é opcional e representa uma entidade relacionada à necessidade.

BaseUrgency representa a urgência inicial.

CurrentPriority representa a prioridade calculada atualmente.

CreatedAt representa quando a necessidade surgiu.

UpdatedAt representa a última atualização.

Status representa o estado atual da necessidade.

Source representa qual sistema ou acontecimento originou a necessidade.

Reason deverá permitir rastrear o motivo pelo qual ela existe.

Estados de uma necessidade

Uma necessidade poderá possuir diferentes estados.

Inactive
Active
Selected
Blocked
Satisfied
Failed
Expired

Inactive significa que a necessidade existe, porém ainda não atingiu relevância suficiente.

Active significa que a necessidade está sendo considerada pelo sistema.

Selected significa que ela originou o objetivo atualmente priorizado pela entidade.

Blocked significa que a entidade gostaria de resolver a necessidade, mas atualmente não possui uma solução acessível.

Satisfied significa que a necessidade foi resolvida.

Failed significa que a tentativa de resolução falhou de maneira definitiva.

Expired significa que a necessidade deixou de fazer sentido.

Crescimento de necessidades

Algumas necessidades deverão aumentar com o tempo.

Exemplo:

Fome

Turno 100: 20
Turno 110: 35
Turno 120: 52
Turno 130: 71
Turno 140: 90

Quanto mais tempo determinado problema permanece sem solução, maior poderá se tornar sua urgência.

Entretanto, nem toda necessidade deverá possuir crescimento linear.

Exemplo:

A fome poderá crescer gradualmente.

Uma ameaça imediata poderá surgir diretamente com prioridade extremamente alta.

Incêndio na residência
Prioridade inicial: 98

Uma dívida que vence em vinte dias poderá começar com prioridade baixa e aumentar conforme o prazo se aproxima.

Redução de necessidades

Necessidades também poderão diminuir.

Exemplo:

Um NPC está com fome.

Fome: 80

Ele consegue comer parcialmente.

Fome: 35

A necessidade ainda existe, porém perdeu prioridade.

O mesmo poderá acontecer com necessidades abstratas.

Exemplo:

Um personagem procura sua irmã desaparecida.

Inicialmente:

Prioridade: 95

Após meses sem nenhuma pista, dependendo da personalidade do personagem, essa prioridade poderá diminuir.

Um personagem extremamente persistente poderá continuar com prioridade elevada.

Outro poderá aceitar a perda e reduzir gradualmente a necessidade.

Resolução completa

Quando a condição responsável pela necessidade deixa de existir, a necessidade deverá ser marcada como satisfeita.

Exemplo:

Necessidade:
Encontrar esposa desaparecida

A esposa retorna para casa.

Resultado:

Status: Satisfied

A necessidade deverá deixar de participar da seleção de objetivos.

Expiração

Algumas necessidades poderão deixar de fazer sentido mesmo sem serem satisfeitas.

Exemplo:

Comprar espada específica

O ferreiro que produzia a espada morreu e o item foi destruído.

Dependendo do contexto, a necessidade poderá:

Expired

ou gerar outra necessidade:

Encontrar uma arma equivalente

Outro exemplo:

Encontrar personagem X

Se o NPC descobrir que X morreu, a necessidade de encontrá-lo deverá ser encerrada.

Isso poderá gerar novas necessidades, como:

Descobrir quem matou X

ou:

Vingar X

Prioridade

A prioridade de uma necessidade não deverá depender de apenas um valor fixo.

Ela poderá ser formada através de diferentes fatores.

Exemplo conceitual:

Prioridade =
Urgência Base
+ Modificador de Tempo
+ Modificador de Personalidade
+ Modificador de Relacionamento
+ Modificador de Perigo
+ Modificador de Responsabilidade
+ Modificador de Contexto

Essa fórmula não precisa obrigatoriamente ser uma soma simples na implementação final, mas deverá representar esses fatores.

Urgência base

Cada tipo de necessidade poderá possuir uma urgência inicial.

Exemplo:

Fome leve: 20
Fome severa: 80

Encontrar objeto perdido: 30

Fugir de ataque: 100

Modificador de tempo

Algumas necessidades ganham importância com o tempo.

Exemplo:

Pagamento de dívida

10 dias restantes: +5
5 dias restantes: +20
1 dia restante: +50

Modificador de personalidade

A personalidade influencia a importância atribuída à necessidade.

Exemplo:

Um NPC vingativo presencia a morte de seu pai.

Necessidade:
Responder à morte do pai

Urgência base: 50
Vingativo: +25
Rancoroso: +15

Prioridade parcial: 90

Outro personagem:

Pacífico: -20
Medroso: -25

Poderá possuir a mesma necessidade, porém com prioridade muito menor.

Modificador de relacionamento

Quanto maior a importância da entidade relacionada, maior poderá ser o impacto da necessidade.

Exemplo:

Pessoa desconhecida desapareceu
Relacionamento: 0

Prioridade adicional: 0

Amigo desapareceu
Relacionamento: 60

Prioridade adicional: +20

Filho desapareceu
Relacionamento: 100

Prioridade adicional: +50

Modificador de perigo

Situações que ameaçam diretamente a sobrevivência deverão receber forte aumento de prioridade.

Exemplo:

Fome: 60
Trabalho: 55
Fugir de incêndio: 100

A entidade deverá interromper atividades menos importantes para lidar com o perigo imediato.

Modificador de responsabilidade

Profissão, posição social e obrigações poderão alterar prioridades.

Exemplo:

Um guarda presencia um crime.

Necessidade:
Interromper crime

Urgência base: 45
Responsabilidade profissional: +35

Um civil presencia o mesmo crime.

Urgência base: 45
Responsabilidade profissional: 0

Ambos podem reagir de maneiras diferentes.

Modificador de contexto

O estado atual do mundo poderá alterar a prioridade.

Exemplo:

Um NPC possui necessidade de comprar comida.

Normalmente:

Prioridade: 55

Durante uma guerra:

Escassez de alimentos
Preço aumentando
Mercado fechando em breve

A prioridade poderá aumentar.

Necessidades concorrentes

Quando múltiplas necessidades estão ativas, o sistema deverá comparar suas prioridades.

Exemplo:

Fome: 65
Sono: 55
Trabalho: 40
Proteger filho durante ataque: 100

A necessidade de proteger o filho deverá dominar temporariamente as demais.

Após a ameaça desaparecer:

Proteger filho: Satisfied

O sistema deverá recalcular as prioridades restantes.

Necessidades interrompíveis

Alguns objetivos poderão ser interrompidos.

Exemplo:

NPC está trabalhando.

Objetivo atual:
Produzir espada

Então surge:

Casa pegando fogo
Prioridade: 100

O trabalho deverá ser interrompido.

Depois da emergência, o NPC poderá retornar ao objetivo anterior caso ele continue válido.

Necessidades não interrompíveis

Algumas ações específicas poderão não permitir interrupção imediata.

Exemplo:

NPC está no meio de uma luta

Uma necessidade secundária de comer não deverá interromper instantaneamente a ação atual.

O sistema deverá considerar se o objetivo atual pode ou não ser interrompido com segurança.

Necessidades bloqueadas

Uma entidade poderá possuir uma necessidade sem possuir uma solução conhecida.

Exemplo:

Necessidade:
Encontrar irmão desaparecido

O NPC não conhece:

Localização
Pistas
Testemunhas

Nesse caso:

Status: Blocked

A necessidade continua existindo.

O sistema poderá então gerar objetivos auxiliares.

Exemplo:

Perguntar aos vizinhos

Visitar último local conhecido

Contratar alguém

Esperar por informações

Objetivos derivados

Uma necessidade poderá gerar um ou vários objetivos possíveis.

Exemplo:

Necessidade:
Conseguir comida

Possíveis objetivos:

Comprar comida
Caçar
Pescar
Pedir comida
Roubar comida
Trabalhar por comida
Cozinhar item existente

O sistema deverá avaliar quais objetivos são possíveis.

Avaliação de solução

Cada solução deverá receber uma pontuação de adequação.

Exemplo conceitual:

SolutionScore =
Personalidade
+ Recursos disponíveis
+ Conhecimento
+ Distância
+ Risco
+ Custo
+ Relações
+ Profissão
+ Experiências anteriores

Exemplo:

NPC com fome.

Possíveis soluções:

Comprar comida: 82
Caçar: 30
Roubar: 12
Pedir ajuda: 50

Resultado:

Objetivo escolhido:
Comprar comida

Para outro NPC:

Comprar comida: 10
Caçar: 75
Roubar: 68
Pedir ajuda: 5

O mesmo problema produz comportamento diferente.

Falha de objetivo

Um objetivo poderá falhar.

Exemplo:

Necessidade:
Conseguir comida

Objetivo:
Comprar comida

O NPC chega ao mercado e descobre que não possui dinheiro suficiente.

Resultado:

Goal Failed
Need still Active

O sistema deverá selecionar outra solução.

Próxima solução:
Pedir comida

Caso também falhe:

Próxima solução:
Roubar comida

A personalidade continuará influenciando se determinada solução é aceitável.

Aprendizado por resultado

NPCs poderão registrar resultados de tentativas anteriores.

Exemplo:

Tentativa:
Roubar mercado

Resultado:
Foi preso

Isso poderá reduzir a atratividade dessa solução no futuro.

Outro NPC poderá interpretar a experiência de maneira diferente dependendo da personalidade.

Um personagem cauteloso:

Roubar novamente: -50

Um personagem extremamente agressivo:

Roubar novamente: -5

Necessidades persistentes

Algumas necessidades são temporárias.

Exemplo:

Fome
Sono
Segurança

Outras podem permanecer durante anos.

Exemplo:

Vingança
Tornar-se rei
Destruir determinada facção
Encontrar familiar desaparecido
Ficar rico

Essas necessidades de longo prazo não deverão necessariamente dominar cada turno.

Elas poderão permanecer ativas com prioridade variável.

Necessidades fundamentais e desejos

O sistema deverá diferenciar necessidades fundamentais de desejos.

Necessidades fundamentais estão relacionadas a condições importantes para sobrevivência ou funcionamento da entidade.

Exemplo:

Comer
Dormir
Segurança
Tratamento médico

Desejos representam objetivos que não possuem urgência biológica imediata.

Exemplo:

Ficar rico
Obter título
Casar
Conquistar território
Vingança
Tornar-se famoso

Ambos utilizarão o mesmo sistema geral de avaliação, mas poderão possuir regras de crescimento diferentes.

Necessidades coletivas

Facções e reinos também poderão possuir múltiplas necessidades simultaneamente.

Exemplo:

Reino X

Fome da população: 85
Defesa da fronteira: 92
Falta de ferro: 60
Desejo de expansão: 30
Crise política: 75

O reino deverá priorizar seus recursos de acordo com essas necessidades.

Isso poderá gerar decisões como:

Aumentar recrutamento

Comprar alimentos

Criar novos impostos

Negociar com outro reino

Invadir território

Conflito interno de necessidades coletivas

Entidades coletivas não precisam agir como se possuíssem uma única mente.

Um reino poderá ter:

População querendo paz

enquanto:

Rei quer expansão

e:

Militares querem guerra

O resultado deverá depender dos sistemas políticos, de poder e de influência.

A necessidade do reino representa o estado coletivo, mas decisões específicas poderão ser influenciadas pelos personagens que possuem autoridade.

Frequência de avaliação

Nem todas as necessidades precisam ser recalculadas a cada pequeno passo do jogo.

Necessidades críticas poderão ser avaliadas imediatamente.

Exemplo:

Ataque
Incêndio
Ferimento grave

Necessidades comuns poderão ser atualizadas em intervalos maiores.

Exemplo:

Fome
Sono
Trabalho

Necessidades estratégicas poderão ser avaliadas ainda menos frequentemente.

Exemplo:

Política de reino
Diplomacia
Expansão territorial
Economia

Esse sistema deverá evitar processamentos desnecessários.

Exemplo completo

John Hammer possui:

Fome: 50
Trabalho: 45
Dívida: 65
Encontrar esposa desaparecida: 90

Sua personalidade possui:

Leal à família: alto
Responsável: alto
Ganancioso: baixo
Covarde: médio

O relacionamento com sua esposa é:

95/100

A necessidade de encontrá-la recebe:

Urgência base: 60
Relacionamento: +25
Personalidade: +15
Tempo desaparecida: +10

Resultado:

Prioridade: 110

O sistema poderá limitar valores finais a uma escala definida, como 0-100.

John passa a priorizar essa necessidade.

Possíveis soluções:

Perguntar aos vizinhos
Procurar na estrada
Ir até a vila vizinha
Contratar alguém
Pedir ajuda ao jogador
Avisar os guardas

John conhece o jogador e possui relação positiva com ele.

O sistema avalia:

Perguntar aos vizinhos: 75
Procurar sozinho: 60
Pedir ajuda ao jogador: 84
Avisar guardas: 50

John decide pedir ajuda ao jogador.

Nesse momento, a necessidade interna de um NPC gera uma oportunidade externa para o jogador.

Necessidade
↓
Objetivo
↓
Interação
↓
Quest emergente

Caso o jogador recuse, a necessidade não desaparece.

John poderá escolher outra solução.

Caso o jogador aceite e encontre sua esposa, a necessidade será marcada como satisfeita.

Caso descubra que ela morreu, a necessidade original será encerrada, mas o evento poderá gerar novas necessidades dependendo da personalidade de John.

Exemplo:

Luto
Vingança
Proteger filhos
Descobrir responsável
Abandonar região

Regra central do sistema

Nenhuma entidade deverá possuir apenas uma sequência fixa de comportamentos para cada necessidade.

O sistema deverá funcionar através de:

Necessidade
↓
Prioridade
↓
Soluções possíveis
↓
Filtros de contexto
↓
Influência da personalidade
↓
Escolha de objetivo
↓
Execução de ações
↓
Resultado
↓
Reavaliação

Esse ciclo deverá ser uma das principais estruturas responsáveis pela autonomia e comportamento emergente do mundo.

## 10. Sistema de Objetivos
O jogo não conterá objetivos claros, como uma ihstória principal, apenas quest pelo sistema de necessidade.

## 11. Sistema de Memória dos NPCs
Os jogadores, desde sua criação irão conter um sistema de memória. Será um slice de FEITOS - se o jogador roubo e foi visto - o npc que sabe disso terá guardado essa informação e pode espalhar ela de forma natural.

As memórias influenciam na tomada de decisão dos npcs, um npc fraco não irá lutar contra um npc lendário se ele es lembrar de quem é.

## 12. Sistema de Personalidade
Sistema de personalidade - muitíssimo importante.

O npc, para realizar uma ação, qualquer ação, será a soma da necessidade e personalidade que culminará naquela ação específica.

O sistema de personaldiade na verdade será uma luta entre as personalidades. exem:
raiva - 200
compaixão - 100
coragem - 100
falsidade - 100

o npc que conter essa linha (terá mais, esses são só apra exemplo) irá ter mais facilidade em agir de forma explosiva e impulsiva em uma situação. Enquanto uma pessoa com falsidade (ou cinismo) poderia agir de uma forma mais obscura, esperando o momento certo.

Tudo dependerá da personaldiade de cada npc.

Npcs agem com base na personalidade. toda ação será personalidade + necessidade = ação
## 13. Sistema de Conhecimento e Percepção
Não teremos testes de percepção. Todo equipamento do player será comprado ou achado.

## 14. Sistema de Rumores e Propagação de Informação
Extrema importancia.

Todo npc terá um slice de conheciment, Esse conhecimento será propagado de uma forma natural. Um npc propagará com o tempo o conhecimento para as posições de matrizes próximas. Então um que está no 12x5 não terá a informação da posição 45x90 pois são muitos distante. Mas caso um npc que tenha esse conhecimento vá para essa outra posição, então o conhecimento vai começar a ser propagado por la.

Para o NPC contar algo para o jogador, ele terá que ter confiança ao jogador, cada conhecimento vai depender de x confiança, algo secreto muita confiança, confiança se ganha tendo popularidade de bom moço ou fazendo favores ao npc.

## 15. Sistema de Facções
As facções serão de grande importancia, elas serão dividas em dois tipos de facções
Reinos - são as facções que contém território oficialmente, reinos, vilas e uma capital. Serão geridas por 1 rei e sua família real - os reinos terão o nome da família, logo para um reino acabaar TODA a família tem que ser morta. Desde o pai (rei) ao filho (principe-herdeiro) - dentro do território dessa facção todos, sem execção tem que responder a família real - a família real também contem uma fé e cultura, irei falar mais sobre o sistam de reinos.

Facções - facções que não saõ reinos, contém uma estrutura não nobre (podendo dser bandidos, mercenários, cçadores e afins) quem está no topo da hierarquia ira ditar o que tem que ser feito e como ser feito. A facção não carrega o nome do lider e sim o nome desginado por ele, facções estão muito ligadas a ideologia do lider. Sendo ele o grande representante, essas facções podem ser ultra violentas como passivas. Tudo irá depender do randomziador.


## 16. Sistema de Reinos
## 16. Sistema de Reinos

Os reinos serão facções territoriais de grande escala. Diferente das facções comuns, um reino possui território oficial, cidades, vilas, população, estrutura política, economia, cultura, religião predominante e uma família real.

Cada reino deverá possuir uma identidade própria gerada proceduralmente.

Essa identidade poderá ser influenciada por:

- Nome da família real
- Cultura predominante
- Religião predominante
- Região geográfica
- Biomas presentes
- Recursos disponíveis
- História inicial
- Personalidade da família real
- Relações com outros reinos
- Situação econômica
- Situação militar

### Estrutura básica de um reino

Cada reino deverá possuir pelo menos os seguintes elementos:

```text
Reino

ID
Nome
Família Real
Rei Atual
Herdeiro Atual
Capital
Cidades
Vilas
Território
População
Cultura
Religião Predominante
Recursos
Economia
Força Militar
Relações Diplomáticas
Necessidades
Histórico
Status
```

O reino deverá utilizar um identificador único e não depender apenas de seu nome.

### Nome do reino

Por padrão, o reino deverá possuir forte relação com o nome da família real.

Exemplo:

```text
Família Real:
Valerius

Reino:
Reino Valerius
```

Entretanto, a implementação deverá permitir futuramente nomes históricos ou culturais diferentes do sobrenome da família.

### Família real

A família real representa a linhagem governante do reino.

Ela poderá conter:

- Rei
- Rainha ou consorte
- Príncipe herdeiro
- Princesas
- Outros filhos
- Irmãos do rei
- Tios
- Primos
- Outros parentes relevantes

As relações familiares deverão utilizar o mesmo sistema de grafos utilizado pelos demais NPCs.

Exemplo:

```text
Rei Aldren
├── married_to → Rainha Mira
├── father_of → Cael
└── brother_of → Tomas
```

A família real não deverá existir apenas como dado político. Seus integrantes serão NPCs reais dentro do mundo e poderão:

- Morrer
- Ser assassinados
- Desaparecer
- Casar
- Ter filhos
- Criar rivalidades
- Participar de guerras
- Tornar-se populares ou odiados
- Ser capturados
- Trair o próprio reino
- Criar necessidades próprias

### Sucessão

Quando o rei morrer, o sistema deverá procurar um sucessor válido.

Inicialmente, a sucessão poderá seguir uma estrutura simples baseada na linhagem da família real.

Exemplo conceitual:

```text
Rei morre
↓
Existe herdeiro válido?
↓
Sim
↓
Herdeiro assume o trono
```

Caso não exista herdeiro direto, o sistema poderá procurar outros membros da família real.

Exemplo:

```text
Filho
↓
Irmão
↓
Outro descendente
↓
Parente elegível
```

As regras exatas de sucessão poderão variar posteriormente de acordo com cultura e sistema político.

### Extinção da família real

Um reino não deverá desaparecer automaticamente apenas porque seu rei morreu.

Para a linhagem governante original ser considerada extinta, não poderá existir nenhum membro válido da família real capaz de reivindicar o trono.

Mesmo nesse caso, o território não deverá simplesmente desaparecer.

A extinção da família poderá gerar diferentes consequências:

```text
Família real extinta
↓
Crise sucessória
```

Essa crise poderá resultar em:

- Guerra civil
- Formação de nova dinastia
- Divisão territorial
- Conquista por outro reino
- Ascensão de líder militar
- Ascensão de facção religiosa
- Criação de república ou outra forma política futura
- Colapso do reino

Portanto, a morte de toda a família real representa o fim da dinastia, não obrigatoriamente o desaparecimento imediato de toda a estrutura territorial.

### Território

Cada reino deverá possuir território definido dentro da matriz global.

O território poderá conter:

- Capital
- Cidades
- Vilas
- Estradas
- Recursos naturais
- Florestas
- Montanhas
- Fazendas
- Ruínas
- Fortificações
- Pontos de interesse

Nem toda posição territorial deverá possuir construções.

O reino deverá possuir controle territorial sobre suas células.

Exemplo conceitual:

```text
Tile (120, 87)

Owner:
Reino Valerius
```

Esse controle poderá mudar durante guerras, revoltas ou eventos políticos.

### Capital

Todo reino deverá possuir uma capital.

A capital será sua cidade mais importante e poderá concentrar:

- Palácio real
- Família real
- Administração
- Quartéis militares
- Comércio
- Instituições religiosas
- Mercados
- NPCs importantes

A capital deverá possuir maior importância econômica, política e militar que a maioria das cidades do mesmo reino.

### Cidades

Cada reino deverá possuir inicialmente entre 4 e 6 cidades, salvo alterações causadas pela geração histórica.

Cada cidade deverá possuir relação direta com o reino ao qual pertence.

Exemplo:

```text
Cidade de Arven
↓
belongs_to
↓
Reino Valerius
```

Cidades deverão gerar e consumir recursos e poderão possuir especializações próprias.

Exemplo:

```text
Cidade A
Produção principal:
Ferro

Cidade B
Produção principal:
Trigo

Cidade C
Produção principal:
Armas
```

Essas diferenças deverão influenciar economia e necessidades do reino.

### Vilas

Vilas vinculadas ao reino deverão normalmente existir nos arredores de suas cidades.

Elas poderão possuir funções como:

- Produção agrícola
- Mineração
- Pesca
- Criação de animais
- Extração de madeira
- Pequeno comércio

As vilas deverão alimentar economicamente cidades próximas ou o próprio reino.

### População

O reino deverá possuir uma população total.

Essa população poderá ser dividida entre:

- Capital
- Cidades
- Vilas
- Zonas rurais
- População militar
- População abstrata

Nem todos os habitantes precisam necessariamente existir como NPCs totalmente simulados.

NPCs importantes poderão ser persistentes e individuais.

Parte da população poderá existir de maneira abstrata para reduzir custo de simulação.

### Controle sobre a população

Por padrão, habitantes dentro do território reconhecem formalmente a autoridade da família real.

Entretanto, isso não significa obediência absoluta.

NPCs poderão:

- Apoiar a família real
- Ser indiferentes
- Odiar a família real
- Desobedecer
- Desertar
- Apoiar rebeliões
- Trabalhar para facções inimigas
- Espionar
- Tentar assassinar membros da realeza

Portanto, pertencer ao território e ser leal ao reino são conceitos diferentes.

### Lealdade ao reino

O reino poderá possuir um valor médio de estabilidade ou lealdade populacional.

Entretanto, NPCs individuais deverão manter suas próprias relações.

Exemplo:

```text
Reino:
Estabilidade geral = 70
```

NPC específico:

```text
Lealdade à coroa = 15
```

Isso permite revoltas e dissidência mesmo em reinos aparentemente estáveis.

### Cultura

Cada reino deverá possuir uma cultura predominante.

A cultura poderá influenciar:

- Nomes
- Vestimentas
- Arquitetura
- Religião
- Profissões
- Leis
- Comportamentos sociais
- Estrutura familiar
- Preferências militares
- Relação com estrangeiros

Nem todos os NPCs precisam seguir perfeitamente a cultura predominante.

### Religião predominante

Cada reino poderá possuir uma religião predominante.

Essa religião poderá estar associada:

- À família real
- À cultura
- À história do reino
- A um deus específico
- A um conjunto de divindades

O reino poderá apoiar oficialmente determinada religião sem obrigatoriamente proibir outras.

Essa relação dependerá futuramente dos sistemas político, cultural e religioso.

### Economia

Cada reino deverá possuir necessidades econômicas próprias.

Exemplos:

```text
Trigo
Madeira
Ferro
Armas
Animais
Ouro
```

A disponibilidade desses recursos deverá depender de suas cidades, vilas, território e comércio.

O reino poderá possuir excesso de determinado recurso e falta de outro.

Exemplo:

```text
Produção de trigo:
Alta

Produção de ferro:
Baixa
```

Isso poderá gerar necessidade de importar ferro.

Caso essa necessidade não seja atendida, outras soluções poderão surgir:

- Comércio
- Expansão
- Aliança
- Roubo
- Conquista

### Tesouro

O reino deverá possuir recursos financeiros próprios.

O tesouro poderá ser utilizado para:

- Manter exército
- Comprar recursos
- Construir estruturas
- Contratar mercenários
- Financiar guerras
- Pagar recompensas
- Realizar obras públicas

Uma crise financeira deverá limitar as possíveis ações do reino.

### Sistema militar

Cada reino deverá possuir uma força militar.

Ela poderá incluir:

- Guardas
- Soldados
- Oficiais
- Generais
- Tropas especiais
- Milícias
- Mercenários contratados

A força militar deverá depender de:

- População
- Economia
- Recursos
- Produção de armas
- Cultura
- Necessidades
- Situação política

Durante guerras ou crises, o reino poderá aumentar o recrutamento.

Isso deverá afetar outros sistemas, principalmente mão de obra e economia.

### Liderança

O rei será uma entidade individual e sua personalidade deverá influenciar as decisões do reino.

Exemplo:

```text
Rei agressivo
↓
Maior tendência a escolher soluções militares
```

```text
Rei diplomático
↓
Maior tendência a negociar
```

```text
Rei ganancioso
↓
Maior preocupação com riqueza e tributos
```

Entretanto, o rei não deverá controlar tudo sozinho obrigatoriamente.

Outros personagens importantes poderão influenciar decisões futuras.

Exemplos:

- Rainha
- Herdeiro
- General
- Conselheiro
- Sacerdote
- Governador
- Nobre poderoso

### Necessidades do reino

Os reinos utilizarão o mesmo conceito de necessidades utilizado pelos NPCs.

Exemplos:

```text
Necessidade:
Alimentar população
```

```text
Necessidade:
Defender fronteira
```

```text
Necessidade:
Obter ferro
```

```text
Necessidade:
Eliminar ameaça interna
```

```text
Necessidade:
Resolver crise econômica
```

Essas necessidades deverão gerar possíveis objetivos e ações.

Exemplo:

```text
Necessidade:
Falta de alimentos
↓
Objetivos possíveis:
Comprar trigo
Aumentar produção
Buscar novo parceiro comercial
Tomar território fértil
```

A personalidade dos líderes, situação econômica, relações diplomáticas e força militar deverão influenciar a decisão final.

### Relações entre reinos

Todo reino poderá possuir relações com outros reinos.

Essas relações deverão utilizar o sistema de grafos.

Exemplo:

```text
Reino A
↓ allied_with
Reino B
```

```text
Reino A
↓ hostile_to
Reino C
```

As relações poderão ser influenciadas por:

- Comércio
- Guerra
- Casamentos
- Assassinatos
- Disputas territoriais
- Religião
- Cultura
- Recursos
- Eventos históricos
- Ações do jogador

### História do reino

Cada reino deverá possuir histórico próprio.

O histórico poderá registrar acontecimentos relevantes como:

- Fundação
- Mudança de rei
- Guerra
- Conquista
- Derrota
- Rebelião
- Fome
- Epidemia
- Casamento real
- Assassinato
- Mudança territorial
- Destruição de cidade
- Ascensão de nova dinastia

Esses acontecimentos poderão alimentar memória, reputação, cultura e relações diplomáticas.

### Status do reino

Um reino poderá possuir diferentes estados.

Exemplos:

```text
Estável
```

```text
Em guerra
```

```text
Em crise
```

```text
Guerra civil
```

```text
Colapsando
```

```text
Ocupado
```

```text
Extinto
```

O status deverá ser consequência do estado real da simulação e não apenas uma classificação aleatória.

### Colapso de um reino

Um reino poderá deixar de existir.

Isso poderá acontecer por fatores como:

- Família real extinta
- Território completamente conquistado
- Guerra civil
- Destruição econômica
- Rebelião
- Fusão com outro reino
- Fragmentação territorial

Quando um reino deixar de existir, seus elementos históricos deverão permanecer no mundo.

Exemplo:

```text
Reino destruído
↓
Ruínas
↓
Refugiados
↓
Ex-soldados
↓
Nobres sobreviventes
↓
Reivindicações territoriais
↓
Ódio contra conquistadores
```

O desaparecimento político de um reino não deve apagar suas consequências.

### Regra central

Um reino não deverá funcionar como uma entidade isolada ou estática.

Ele deverá ser resultado da interação entre:

```text
Família real
+
População
+
Território
+
Economia
+
Cultura
+
Religião
+
Exército
+
Necessidades
+
Relações diplomáticas
+
História
```

Esses sistemas deverão influenciar uns aos outros continuamente.


## 17. Sistema Político

O sistema político será simples e terá como função principal definir quem governa cada reino e como decisões importantes podem surgir da simulação.

Cada reino possuirá um governante principal, normalmente o rei, além de uma linha de sucessão ligada à família real.

A personalidade do governante deverá influenciar decisões do reino.

Exemplo:

```text
Rei agressivo
→ maior chance de escolher soluções militares

Rei diplomático
→ maior chance de negociar

Rei ganancioso
→ maior chance de aumentar impostos ou priorizar riqueza
```

Personagens importantes como generais, membros da família real ou líderes religiosos poderão exercer influência, mas o sistema não precisa simular política em nível excessivamente detalhado.

O principal objetivo é permitir acontecimentos como:

- Mudança de rei
- Crise de sucessão
- Rebelião
- Golpe
- Conflito interno
- Mudança de decisões devido à personalidade do governante

O sistema político deverá funcionar principalmente como apoio aos sistemas de necessidade, reino, guerra e narrativa.

## 18. Sistema de Diplomacia

A diplomacia representará a relação entre reinos e facções.

Essas relações deverão utilizar o sistema de grafos e poderão possuir valores positivos ou negativos.

Exemplo:

```text
Reino A → Reino B
Relação: 75
```

```text
Reino A → Reino C
Relação: -80
```

As relações poderão mudar de acordo com acontecimentos do mundo.

Exemplos:

- Comércio melhora relações
- Ajuda militar melhora relações
- Ataques pioram relações
- Disputas territoriais pioram relações
- Assassinatos pioram relações
- Inimigos em comum podem aproximar facções
- Guerras anteriores influenciam relações futuras

A diplomacia também poderá ser utilizada como uma possível solução para necessidades.

Exemplo:

```text
Reino precisa de trigo
↓
Outro reino possui trigo
↓
Tenta negociar
```

Caso a negociação falhe, outras soluções poderão ser consideradas, incluindo guerra.

O sistema diplomático não será o foco principal do jogo. Ele existirá principalmente para gerar consequências, conflitos, alianças e situações interessantes para o RPG.

## 19. Sistema de Guerra

Em caso de geurra declarada. O rei ou facção irá move um exército, esse exército é parte da força militar, a soma da frça militar dessa parte ira criar o "poder", caso o pode seja maior que o poder do exército do inimigo, ele ganha. A guerra só acaba mediante a objetivo cumprida ou negociação.

Obs: em geurras de calamidade, como um reino quase perdendo, o rei pode determianr alistamento forçado, fazendo com que NPCs não militares, sejam obrigado a ir para a guerra. 

isso pode resultar em uma economia mais ferrada, cara e escassa também. Dependedo do nível da guerra, vilas inteiras serõa povoadas apenas por mulheres e crianças.

## 20. Sistema de Cultura
A cultura de um povo é a soma da cultura da família real + necessidade + bioma (roupas) + histórico.

O histórico é o histórico daquele reino, se o reino passa por muitas guerras, a tendencia é ter um histórico mais militar, logo ua cultura mais militar, caso não, será um povo de mais colhieta e menos militarismo.

Obs: a cultura pode influenciar na personalidade dos NPCs
# Tópicos que Ainda Precisam ser Definidos
## 21. Sistema de Religiões
Importante!
Nesse mundo, religiões são sempre puxadas para o fanatismo, sem meio termo, cada reino vai ter uma religião oficial que se´ra seguida a risca. No topo tera o padre, lider da religião e porta voz do Dues da religião. Abaixo penitentes e o clero (use a divisão do catolicismo).

Penitentes: e´uma sub facção que sempre irá existir, eles serão os caçadores de hereges de toda a religião.

## 22. Sistema de Deuses
Deuses existem, podem aparecer ou serem invocados.

É o suprassumo do poder em um mundo.

O ritual de invocação normalmente será sacríficio do padre da religiao + pedaço ou item do Deus + sangue do player + contrato com o Deus - ritual é um contrato de poder.

Os deuses possuirão personalidade própria, desejos, valores e formas diferentes de interpretar o mundo.

Diferente dos NPCs comuns, a personalidade dos deuses poderá representar conceitos extremos e influenciar diretamente religiões, culturas, seguidores, milagres e conflitos.

Cada deus deverá possuir um conjunto de características com valores numéricos.

Exemplo:

Ira: 180
Compaixão: 40
Orgulho: 160
Paciência: 20
Honra: 130
Crueldade: 90
Curiosidade: 30

Os valores dos deuses poderão ultrapassar os limites normais utilizados por humanos, representando personalidades muito mais intensas.

A personalidade deverá influenciar como o deus reage aos acontecimentos e como interpreta as ações de seus seguidores.

Domínios

Além da personalidade, cada deus deverá possuir um ou mais domínios.

Exemplos:

Guerra

Fogo

Morte

Natureza

Conhecimento

Mar

Justiça

Engano

Caça

Amor

Tempestade

Os domínios não representam necessariamente personalidade.

Um deus da guerra pode ser honrado e disciplinado, enquanto outro pode ser cruel e caótico.

Exemplo:

Deus A

Domínio:
Guerra

Personalidade:
Honra: 190
Disciplina: 170
Crueldade: 20

Deus B

Domínio:
Guerra

Personalidade:
Crueldade: 190
Ira: 180
Honra: 15

Ambos representam guerra, mas possuem comportamentos completamente diferentes.

Valores fundamentais

Cada deus poderá possuir valores considerados sagrados.

Exemplo:

Valoriza:
Coragem
Sacrifício
Lealdade

Despreza:
Covardia
Traição
Deserção

Esses valores deverão influenciar a religião criada em torno da divindade.

Seguidores poderão receber aprovação ou desaprovação conforme suas ações.

Desejos divinos

Deuses também poderão possuir necessidades ou desejos.

Entretanto, essas necessidades não precisam ser biológicas.

Exemplos:

Aumentar número de seguidores

Destruir uma religião rival

Recuperar artefato perdido

Punir determinada linhagem

Proteger determinado povo

Ser lembrado

Expandir seu domínio

Libertar-se de alguma prisão

Encontrar um campeão

Destruir outro deus

Esses desejos utilizarão o sistema geral de necessidades.

Desejo divino
+
Personalidade
+
Estado do mundo
=
Possível ação divina

Relação com seguidores

Cada deus poderá possuir relações diferentes com seus seguidores.

Alguns poderão ser protetores.

Outros poderão considerar seus seguidores apenas ferramentas.

Exemplo:

Compaixão alta
→ maior chance de ajudar seguidores

Orgulho alto
→ exige demonstrações de devoção

Crueldade alta
→ aceita sacrifícios extremos

Ciúme alto
→ reage mal à adoração de outros deuses

A devoção dos seguidores também deverá influenciar a atenção recebida.

Intervenção divina

Deuses não deverão agir constantemente.

Intervenções diretas precisam ser acontecimentos relevantes.

Possíveis ações:

Enviar visão

Criar sonho

Conceder bênção

Aplicar maldição

Escolher campeão

Criar artefato

Alterar acontecimento

Enviar criatura

Manifestar-se diretamente

A personalidade deverá influenciar a forma da intervenção.

Um deus paciente poderá enviar sinais durante anos antes de agir.

Um deus impulsivo poderá reagir imediatamente a uma provocação.

Memória divina

Deuses deverão possuir memória muito mais persistente que NPCs comuns.

Acontecimentos importantes poderão permanecer durante períodos extremamente longos.

Exemplo:

Rei destruiu templo
↓
Deus registra acontecimento
↓
Ódio contra rei
↓
Ódio pode continuar para seus descendentes

Isso poderá gerar maldições familiares, rivalidades religiosas ou acontecimentos futuros.

Relações entre deuses

Deuses também utilizarão o sistema de grafos.

Exemplos:

Deus do Sol
→ aliado
→ Deusa da Justiça

Deus do Fogo
→ rival
→ Deus do Mar

Essas relações poderão gerar:

Guerras religiosas

Alianças entre cultos

Profecias

Campeões rivais

Artefatos

Conflitos entre seguidores

Contradições de personalidade

Um deus poderá possuir características conflitantes.

Exemplo:

Compaixão: 150
Ira: 170

Isso não deverá ser considerado erro.

O deus poderá amar profundamente seus seguidores e, ao mesmo tempo, reagir com violência extrema contra quem os ameaça.

Essas contradições ajudam a criar divindades menos previsíveis.

Personalidade e religião

A religião deverá refletir parcialmente a personalidade do deus.

Um deus extremamente disciplinado poderá gerar uma religião rígida.

Um deus ligado à liberdade poderá gerar cultos menos hierárquicos.

Entretanto, seguidores poderão interpretar o deus de maneira incorreta.

A religião criada pelos humanos não precisa representar perfeitamente a personalidade real da divindade.

Isso permite situações como:

Deus real:
Compaixão alta

Religião criada em seu nome:
Extremamente violenta

O próprio deus poderá aprovar, ignorar ou tentar corrigir essa interpretação.

Regra central

Deuses não deverão ser apenas personagens com números maiores.

Eles deverão funcionar como entidades capazes de influenciar grandes partes do mundo através de:

Personalidade
+
Domínios
+
Valores
+
Desejos
+
Memória
+
Seguidores
+
Relações
=
Comportamento divino

A personalidade deverá definir como cada deus reage ao mundo e impedir que todas as divindades atuem da mesma forma.

## 23. Sistema de Itens

Os itens serão gerados proceduralmente e deverão possuir qualidade, raridade, função e origem.

A qualidade dos itens encontrados estará diretamente relacionada ao contexto em que foram obtidos e à importância da entidade que os possuía.

NPCs comuns terão maior chance de possuir itens comuns.

NPCs importantes poderão possuir itens incomuns ou raros.

NPCs lendários terão maior chance de possuir equipamentos únicos ou extremamente raros.

Deuses poderão possuir itens divinos ou lendários ligados diretamente à sua identidade.

Exemplo:

```text
NPC comum
↓
Espada de Ferro

NPC importante
↓
Espada de Aço de Arven

NPC lendário
↓
Lâmina de Kars, Quebra-Escudos

Deus
↓
Aurora, Espada do Fogo Eterno
```

A raridade inicial poderá seguir categorias como:

```text
Comum
Incomum
Raro
Épico
Lendário
Divino
```

A raridade não deverá ser escolhida apenas aleatoriamente. Ela deverá considerar fatores como:

- Importância do antigo proprietário
- Qualidade do material
- História do item
- Eventos associados
- Criador
- Tempo de existência
- Feitos realizados com ele
- Origem divina ou sobrenatural

Itens também poderão ganhar importância ao longo da simulação.

Uma espada comum utilizada por um personagem para matar um rei, por exemplo, poderá ganhar valor histórico e reputação mesmo que originalmente fosse apenas uma arma comum.

Itens especiais poderão possuir peculiaridades.

Exemplo:

```text
Nome:
Lâmina de Kars

Peculiaridade:
Quebra-Escudos
```

Essas peculiaridades poderão alterar comportamento, atributos ou simplesmente representar características históricas importantes.

Ao morrer, um NPC poderá deixar disponíveis os itens físicos que carregava ou utilizava.

O jogador poderá, dependendo da situação, pegar múltiplos itens do corpo e não apenas um único item sorteado.

Itens que não fazem sentido físico não deverão aparecer como loot apenas por aleatoriedade.

## 24. Sistema de Equipamentos

Equipamentos são itens que podem ser utilizados diretamente por personagens.

As principais categorias iniciais serão:

- Armas
- Armaduras
- Capacetes
- Escudos
- Acessórios

O personagem deverá possuir espaços próprios para equipamentos.

Exemplo:

```text
Arma principal
Arma secundária
Cabeça
Torso
Mãos
Pernas
Acessório
```

A estrutura poderá ser expandida posteriormente.

Equipamentos deverão possuir atributos próprios.

Exemplo:

```text
Espada de Ferro

Dano: 12
Durabilidade: 85
Peso: 4
Raridade: Comum
```

Armaduras poderão possuir características como:

```text
Defesa
Peso
Durabilidade
Resistências
```

Equipamentos especiais poderão possuir modificadores únicos.

Exemplo:

```text
Aurora, Espada do Fogo Eterno

Raridade: Divina
Dano: muito alto
Peculiaridade: Fogo Eterno
Antigo proprietário: Deus do Fogo
```

A origem do equipamento deverá permanecer registrada quando relevante.

Isso permitirá que NPCs reconheçam determinados itens.

Exemplo:

```text
Jogador equipa a espada de um deus morto
↓
NPC religioso reconhece a arma
↓
Reação depende de fé, conhecimento e personalidade
```

Portanto, equipamentos poderão possuir importância não apenas em combate, mas também social, religiosa e histórica.

## 25. Sistema de Inventário

Jogadores e NPCs poderão possuir inventários.

O inventário será responsável por armazenar referências aos itens atualmente carregados pela entidade.

Exemplo conceitual:

```text
Inventory

- ItemID 102
- ItemID 340
- ItemID 422
```

Itens deverão possuir identificadores únicos.

O inventário não deverá copiar todas as informações do item diretamente. Ele deverá manter referência ao item existente no mundo.

Itens empilháveis poderão utilizar quantidade.

Exemplo:

```text
Pão x4
Flecha x20
Moeda x135
```

Itens únicos deverão permanecer individualizados.

Exemplo:

```text
Aurora, Espada do Fogo Eterno
```

O sistema deverá permitir ações como:

- Adicionar item
- Remover item
- Equipar item
- Desequipar item
- Transferir item
- Comprar item
- Vender item
- Abandonar item
- Pegar item de corpo
- Entregar item

O inventário também deverá respeitar o contexto da entidade.

NPCs deverão carregar itens compatíveis com profissão, riqueza, função e situação.

Exemplo:

```text
Ferreiro
↓
Ferramentas
Materiais
Algum dinheiro
Possível arma

Soldado
↓
Arma
Armadura
Comida
Itens militares
```

A geração de inventário deverá utilizar o sistema procedural, mas sempre respeitando lógica e contexto.

## 28. Sistema Econômico

O sistema econômico deverá funcionar principalmente através de produção, consumo, disponibilidade e necessidade.

Os preços não deverão permanecer completamente fixos.

Cada região poderá produzir determinados recursos e depender de outros.

Exemplo:

```text
Cidade A:
Alta produção de trigo

Cidade B:
Alta produção de ferro
```

Essas diferenças deverão gerar comércio natural.

O valor de um item deverá ser influenciado por fatores como:

```text
Preço base
+
Disponibilidade
+
Demanda
+
Escassez
+
Situação regional
+
Eventos do mundo
```

Exemplo:

Uma guerra aumenta o recrutamento militar.

```text
Mais soldados
↓
Maior procura por armas
↓
Maior procura por ferro
↓
Preço do ferro aumenta
↓
Preço de armas aumenta
```

Ao mesmo tempo, a guerra pode retirar trabalhadores de outras profissões.

```text
Mais pessoas no exército
↓
Menos artesãos
↓
Menor produção artesanal
↓
Preço de produtos artesanais aumenta
```

O mesmo deverá acontecer com alimentos.

```text
Guerra
↓
Produção agrícola diminui
↓
Alimentos ficam escassos
↓
Preços aumentam
↓
População possui dificuldade para comprar
↓
Novas necessidades surgem
```

Portanto, a economia deverá estar diretamente ligada ao sistema de necessidades.

NPCs também deverão possuir dinheiro ou recursos compatíveis com sua situação econômica.

Um NPC pobre não deverá conseguir comprar continuamente equipamentos caros.

Um comerciante rico poderá possuir maior quantidade de dinheiro e mercadorias.

Cidades e reinos também poderão possuir recursos econômicos próprios.

A economia deverá permitir acontecimentos como:

- Escassez
- Inflação local
- Produtos baratos devido à abundância
- Crises alimentares
- Falta de matéria-prima
- Crescimento comercial
- Rotas comerciais
- Mercados afetados por guerra
- Saques
- Bloqueios econômicos

Os preços poderão variar entre regiões.

Exemplo:

```text
Cidade produtora de trigo:
Pão = 3 moedas

Cidade distante sofrendo fome:
Pão = 14 moedas
```

Isso poderá criar oportunidades para comerciantes, jogadores e facções.

NPCs deverão reagir aos preços de acordo com suas necessidades e condições financeiras.

Um NPC incapaz de comprar comida poderá:

```text
Buscar trabalho
↓
Pedir ajuda
↓
Procurar alimento em outro local
↓
Roubar
```

dependendo de personalidade e contexto.

O sistema econômico não deverá funcionar isoladamente.

Ele deverá alimentar diretamente:

```text
Necessidades
Profissões
Comércio
Facções
Reinos
Criminalidade
Guerras
Quests emergentes
```

A regra central será:

```text
Produção
+
Consumo
+
Disponibilidade
+
Necessidade
=
Economia dinâmica
```

O objetivo não é criar uma simulação econômica extremamente complexa, mas fazer com que acontecimentos do mundo tenham consequências perceptíveis nos preços, recursos e comportamento das entidades.

## 29. Sistema de Comércio

O sistema de comércio será responsável pela circulação de itens, recursos e dinheiro entre NPCs, cidades, vilas, facções e reinos.

O comércio deverá responder ao sistema econômico.

Se determinado recurso estiver abundante em uma região, seu preço tende a ser menor. Se estiver escasso, seu preço tende a aumentar.

Exemplo:

```text
Cidade A:
Muito trigo
Pouco ferro

Cidade B:
Muito ferro
Pouco trigo
```

Isso cria uma relação comercial natural entre as duas cidades.

Comerciantes poderão comprar produtos onde são baratos e vender onde possuem maior valor.

NPCs poderão atuar como:

- Comerciantes
- Vendedores
- Mercadores itinerantes
- Donos de lojas
- Artesãos que vendem a própria produção
- Intermediários entre cidades

As lojas deverão possuir estoque real.

Um ferreiro não deverá vender infinitas espadas se não possuir materiais ou produção suficiente.

Exemplo:

```text
Ferreiro possui:
20 unidades de ferro

Produz:
2 espadas

Estoque:
2 espadas
```

Caso o ferro acabe, a produção deverá parar até que novos materiais sejam obtidos.

O preço final poderá considerar:

```text
Preço base
+
Escassez
+
Demanda
+
Distância
+
Situação regional
+
Margem do vendedor
```

A personalidade do vendedor também poderá influenciar negociações.

Um comerciante ganancioso poderá cobrar mais.

Um comerciante amigável ao jogador poderá oferecer melhores preços.

Um NPC desesperado poderá vender um item abaixo do valor normal.

O jogador poderá:

- Comprar
- Vender
- Trocar
- Negociar quando permitido
- Comprar recursos
- Comprar equipamentos
- Vender itens encontrados
- Explorar diferenças de preço entre regiões

Rotas comerciais também poderão existir entre cidades e reinos.

Guerras, bandidos ou bloqueios poderão interromper essas rotas.

Exemplo:

```text
Estrada comercial bloqueada
↓
Menos trigo chega à cidade
↓
Estoque diminui
↓
Preço aumenta
```

O comércio deverá funcionar como ponte entre:

```text
Produção
↓
Transporte
↓
Disponibilidade
↓
Preço
↓
Necessidade
```

## 30. Sistema de Profissões

Todos os NPCs poderão possuir uma profissão, ocupação ou função social.

A profissão deverá possuir impacto real na simulação.

Exemplos iniciais:

- Ferreiro
- Agricultor
- Caçador
- Pescador
- Cozinheiro
- Comerciante
- Guarda
- Soldado
- Mineiro
- Lenhador
- Curandeiro
- Sacerdote
- Artesão
- Estudante
- Sem profissão

Cada profissão deverá possuir atividades próprias.

Exemplo:

```text
Ferreiro
↓
Obtém materiais
↓
Produz armas ou armaduras
↓
Vende ou entrega equipamentos
```

```text
Agricultor
↓
Produz alimentos
↓
Abastece vila, cidade ou mercado
```

```text
Guarda
↓
Patrulha
↓
Responde a crimes
↓
Protege áreas determinadas
```

```text
Caçador
↓
Sai para áreas externas
↓
Caça animais
↓
Retorna com carne ou outros recursos
```

A profissão deverá influenciar:

- Rotina
- Local de trabalho
- Conhecimento
- Inventário
- Renda
- Necessidades
- Relações
- Possíveis ações

Um NPC não deverá exercer perfeitamente qualquer profissão sem possuir relação com ela.

Um ferreiro poderá saber produzir armas, enquanto um agricultor comum provavelmente não terá esse conhecimento.

Profissões também deverão responder às necessidades do mundo.

Exemplo:

```text
Guerra começa
↓
Necessidade militar aumenta
↓
Mais NPCs podem se tornar soldados
```

Isso reduz mão de obra em outras áreas.

```text
Menos agricultores
↓
Menor produção de alimentos
```

Também poderão existir mudanças de profissão.

Exemplo:

```text
Agricultor
↓
Perde fazenda durante guerra
↓
Precisa de dinheiro
↓
Entra para grupo mercenário
```

A personalidade também poderá influenciar essa decisão.

Profissões poderão possuir níveis diferentes de experiência ou habilidade futuramente, mas isso não precisa fazer parte do primeiro sistema.

A regra central será:

```text
Profissão
+
Necessidades
+
Personalidade
+
Situação do mundo
=
Comportamento profissional
```

A profissão não deverá existir apenas como um campo textual. Ela deverá gerar ações concretas e consequências para o mundo.

## 31. Sistema de Combate
O combate do jogo será divido por partes. Como TODO ser que da pra combater é humanoide, podemos atiginri cada parte do corpo. As únicas que zerada MATAM é o torax e a abeça, no demais apenas gera um efeito negativo, como deixar a arma cair, ficar bambo e etc.

Dano: dano é o dano da arma + atributos dos equopamentos (como auemtnar a porcentagem de dano da arma e por ai vai)

## 33. Sistema de Ferimentos e Condições
Para a gameplay, o jogo tera apenas ferimetnos localizados em combate, saindo do combate vc ficara apenas com a vida restante, mas os membros terão voltado ao normal
## 34. Sistema de Morte
a morte é permanente.
## 35. Sistema de Família e Hereditariedade
Irá ser simples. Em caso de morte do pai o filho herdeiro irá heradr tudo, desde items a locais;
## 36. Sistema de Nascimento e Envelhecimento
Sincerametne duvido que passarão anos no jogo ent
## 37. Sistema de Reputação
## 37. Sistema de Reputação

O sistema de reputação será responsável por representar como personagens, grupos, cidades, facções e reinos enxergam uma entidade.

Tanto o jogador quanto NPCs poderão possuir reputação.

Reputação não será um único valor global.

Uma pessoa poderá ser considerada herói em uma cidade e assassino em outra.

Também deverá existir diferença entre:

```text
Popularidade
```

e:

```text
Reputação
```

Popularidade representa o quanto uma entidade é conhecida.

Reputação representa pelo que ela é conhecida.

Exemplo:

```text
Jogador

Popularidade: 92

Reputações conhecidas:
Matador de Dragões: 95
Assassino: 65
Protetor de Aldeões: 40
Inimigo do Reino Valerius: 100
```

Um personagem extremamente conhecido não necessariamente será amado.

## Feitos

A reputação será construída principalmente através de feitos.

Um feito representa um acontecimento relevante associado a uma entidade.

Exemplos:

```text
Matou um rei
Salvou uma vila
Matou um deus
Venceu uma guerra
Assassinou um comerciante
Derrotou um personagem lendário
Traiu uma facção
Defendeu uma cidade
Roubou um artefato
Destruiu uma vila
```

Cada feito deverá possuir informações como:

```text
Autor
Tipo do feito
Alvo
Local
Turno/Data
Importância
Testemunhas
Conhecimento público
Facções afetadas
```

A reputação deverá ser consequência desses feitos.

## Reputação contextual

Um mesmo feito poderá gerar reputações completamente diferentes dependendo de quem o observa.

Exemplo:

O jogador mata o rei do Reino A.

Para habitantes leais ao Reino A:

```text
Regicida
Criminoso
Inimigo
```

Para uma facção rebelde:

```text
Libertador
Herói
Aliado
```

Para outro reino:

```text
Pessoa perigosa
Possível aliado
Ameaça política
```

Portanto:

```text
Feito
+
Valores do observador
+
Relações
+
Conhecimento
=
Reputação
```

## Reputação por entidade

Cada entidade poderá possuir sua própria opinião sobre outra.

Exemplo:

```text
NPC John
→ Jogador

Confiança: 80
Reputação percebida:
Herói: 70
Violento: 40
Confiável: 90
```

Outro NPC poderá enxergar o mesmo jogador como:

```text
NPC Marcus
→ Jogador

Confiança: 10
Reputação percebida:
Assassino: 80
Perigoso: 95
```

Não deverá existir obrigação de todos compartilharem a mesma visão.

## Reputação coletiva

Além da opinião individual, grupos poderão possuir uma visão coletiva.

Exemplo:

```text
Cidade de Arven
→ Jogador

Herói local: 85
Criminoso: 5
```

```text
Facção dos Corvos
→ Jogador

Inimigo: 90
Perigoso: 95
```

```text
Reino Valerius
→ Jogador

Procurado: 100
Regicida: 100
```

Essas reputações poderão influenciar NPCs pertencentes a esses grupos.

Entretanto, a opinião individual ainda poderá sobrescrever parcialmente a coletiva.

Exemplo:

Um guarda pertence ao Reino Valerius e recebe ordem para prender o jogador.

Porém:

```text
Jogador salvou sua filha
↓
Lealdade ao jogador: alta
↓
Lealdade ao reino: média
```

Esse conflito poderá afetar sua decisão.

## Tags de reputação

A reputação deverá utilizar conceitos ou tags associados aos feitos.

Exemplos:

```text
Herói
Assassino
Ladrão
Traidor
Libertador
Covarde
Mercenário
Caçador de monstros
Matador de dragões
Matador de deuses
Protetor
Cruel
Confiável
Desonrado
Santo
Herege
Rebelde
Conquistador
```

Essas tags poderão possuir intensidades.

Exemplo:

```text
Assassino: 35
Herói: 80
Confiável: 65
```

Os valores representam o quanto aquela reputação está associada ao personagem para determinada entidade ou grupo.

## Reputação específica por feito

Além de tags genéricas, acontecimentos extremamente importantes poderão possuir reputação própria.

Exemplo:

```text
"Matador de Dovha"
```

ou:

```text
"Responsável pela Queda de Arven"
```

Isso permitirá que acontecimentos procedurais criem identidades únicas.

O jogo não deverá depender apenas de títulos previamente programados.

## Origem da reputação

Toda reputação deverá possuir uma origem rastreável.

Exemplo:

```text
Reputação:
Assassino: +25

Origem:
Jogador matou Marcus na Praça de Arven.

Testemunhas:
12 NPCs
```

Isso será importante para evitar reputações surgindo sem explicação.

## Testemunhas

Um feito não deverá automaticamente se tornar conhecimento global.

Se o jogador matar alguém sem nenhuma testemunha e nenhuma evidência posterior:

```text
Mundo sabe:
Não

Jogador sabe:
Sim
```

A reputação não deverá ser alterada automaticamente para todos.

Caso alguém testemunhe:

```text
NPC testemunha assassinato
↓
Memória criada
↓
Conhecimento adquirido
↓
Possível propagação
↓
Reputação começa a se espalhar
```

O sistema de reputação deverá depender diretamente dos sistemas de memória e rumores.

## Rumores e reputação

Informações poderão se espalhar de forma imperfeita.

Exemplo real:

```text
Jogador matou 3 bandidos.
```

Primeiro rumor:

```text
"Um viajante matou três homens na estrada."
```

Depois:

```text
"Um guerreiro sozinho matou dez homens."
```

Mais tarde:

```text
"Dizem que ele matou vinte homens sem ser ferido."
```

A reputação poderá crescer mesmo com informações exageradas.

Isso permite reputação baseada tanto em fatos quanto em rumores.

## Reputação falsa

O mundo também poderá atribuir feitos incorretamente.

Exemplo:

Um NPC mata determinado personagem, mas espalha que foi o jogador.

Caso o rumor seja aceito:

```text
Jogador
→ reputação de assassino
```

mesmo sendo inocente.

Isso permitirá:

- Acusações falsas
- Manipulação
- Propaganda
- Difamação
- Falsos heróis
- Falsas lendas

Uma reputação não precisa representar a verdade objetiva do mundo.

Ela representa aquilo que as pessoas acreditam.

## Alcance da reputação

A reputação deverá possuir alcance geográfico.

Um jogador poderá ser extremamente conhecido em determinado reino e praticamente desconhecido em outro continente.

Exemplo:

```text
Reino A:
Popularidade 95

Reino B:
Popularidade 40

Região distante:
Popularidade 5
```

Rumores, comerciantes, viajantes, soldados e outros personagens poderão carregar histórias para novas regiões.

## Velocidade de propagação

A velocidade de propagação poderá depender da importância do feito.

Exemplo:

```text
Jogador roubou pão
→ propagação local

Jogador matou um guarda
→ cidade

Jogador matou um rei
→ reino e regiões próximas

Jogador matou um deus
→ possível propagação continental
```

Quanto maior o acontecimento, maior a chance de ele viajar grandes distâncias.

## Popularidade

Popularidade representará apenas o nível de reconhecimento do personagem.

Exemplo:

```text
0-10:
Praticamente desconhecido

11-30:
Conhecido localmente

31-60:
Conhecido regionalmente

61-80:
Muito conhecido

81-99:
Famoso

100:
Figura mundialmente conhecida
```

Essa escala deverá ser apenas referência e poderá ser ajustada.

Popularidade poderá aumentar por feitos positivos ou negativos.

Um criminoso extremamente perigoso poderá possuir popularidade máxima.

## Reconhecimento

NPCs não deverão reconhecer automaticamente alguém apenas porque sua popularidade é alta.

O reconhecimento poderá depender de fatores como:

- Região
- Conhecimento do NPC
- Descrição física
- Armadura
- Equipamento famoso
- Apelido
- Rumores
- Encontros anteriores

Exemplo:

O jogador possui:

```text
Popularidade: 90
Apelido: Matador do Sol
```

Mas está em uma região distante onde sua aparência não é conhecida.

Um NPC poderá saber:

```text
"Existe alguém chamado Matador do Sol."
```

sem perceber que a pessoa na sua frente é ele.

## Equipamentos e reputação

Itens famosos também poderão revelar identidade.

Exemplo:

```text
Jogador possui:
Aurora, Espada do Fogo Eterno
```

Um sacerdote conhece a arma.

```text
Sacerdote reconhece Aurora
↓
Associa arma ao jogador
↓
Percebe que está diante do Matador do Deus do Fogo
```

Portanto, equipamentos poderão carregar reputação.

## Títulos e apelidos

A reputação poderá gerar apelidos automaticamente.

O jogador deverá iniciar como:

```text
Desconhecido
```

Conforme acumula feitos, poderá receber títulos.

Exemplos:

```text
Hugo, o Matador de Lobos

Hugo, o Regicida

Hugo, Quebra-Coroas

Hugo, Carrasco dos Deuses
```

Os títulos deverão surgir a partir dos feitos realmente realizados durante aquela campanha.

Diferentes regiões poderão inclusive utilizar apelidos diferentes para a mesma pessoa.

Exemplo:

```text
Reino A:
"O Libertador"

Reino B:
"O Açougueiro"
```

## Reputação de NPCs

NPCs utilizarão exatamente o mesmo sistema.

Um NPC poderá começar como personagem comum e tornar-se famoso através da simulação.

Exemplo:

```text
Soldado desconhecido
↓
Mata general inimigo
↓
Sobrevive a três batalhas
↓
Torna-se conhecido
↓
Recebe promoção
↓
Torna-se comandante
↓
Torna-se personagem importante
```

Isso significa que as categorias:

```text
Comum
Importante
Lendário
```

não precisam ser completamente permanentes.

Um NPC poderá subir de importância conforme seus feitos.

## NPCs lendários emergentes

Um personagem não precisa nascer lendário.

A própria simulação poderá criar uma lenda.

Exemplo:

```text
Ferreiro comum
↓
Cidade atacada
↓
Defende moradores usando martelo
↓
Mata líder inimigo
↓
Sobrevive
↓
História se espalha
↓
"Martelo de Arven"
```

Esse NPC poderá posteriormente tornar-se uma figura importante.

## Reputação e medo

Reputação positiva e medo deverão ser conceitos diferentes.

Exemplo:

```text
Admiração: 10
Medo: 95
```

Um personagem pode ser odiado e ainda assim possuir enorme influência.

Outro poderá possuir:

```text
Admiração: 90
Medo: 5
```

Esses valores poderão afetar interações diferentes.

## Reputação e confiança

Reputação também não deverá ser confundida com confiança.

Um NPC pode reconhecer o jogador como grande herói:

```text
Reputação positiva: 90
```

mas ainda não confiar pessoalmente nele:

```text
Confiança: 20
```

Confiança deverá ser construída principalmente através de relações diretas.

## Reputação e comportamento

A reputação deverá modificar o comportamento do mundo.

Exemplos:

### Jogador conhecido como herói

NPCs poderão:

- Pedir ajuda
- Oferecer descontos
- Procurar proteção
- Contar informações
- Tentar acompanhá-lo

### Jogador conhecido como criminoso

NPCs poderão:

- Fugir
- Alertar guardas
- Recusar comércio
- Tentar capturá-lo
- Mentir por medo

### Jogador conhecido como guerreiro lendário

NPCs fracos poderão evitar confrontos.

```text
NPC considera atacar jogador
↓
Memória/conhecimento:
Jogador matou personagem lendário
↓
Personalidade:
Covarde
↓
Desiste do confronto
```

Um NPC extremamente corajoso ou vingativo poderá atacar mesmo assim.

## Reputação com facções

Cada facção deverá possuir reputação própria em relação ao jogador e outros personagens.

Exemplo:

```text
Mercenários:
+60

Reino Valerius:
-100

Culto Solar:
-80

Caçadores:
+25
```

A reputação poderá afetar:

- Hostilidade
- Comércio
- Contratos
- Acesso a locais
- Ajuda
- Informações
- Recrutamento
- Recompensas

## Crimes e recompensas

Crimes conhecidos poderão gerar recompensas.

Exemplo:

```text
Jogador mata nobre importante
↓
Crime se torna conhecido
↓
Reino identifica jogador
↓
Recompensa criada
```

O valor poderá depender de:

- Importância da vítima
- Quantidade de crimes
- Periculosidade do jogador
- Recursos da facção
- Reputação anterior

Isso poderá alimentar diretamente o sistema de necessidades.

```text
Mercenário precisa de dinheiro
+
Jogador possui recompensa
+
Mercenário acredita conseguir vencê-lo
=
Possível caça ao jogador
```

## Decaimento da reputação

Nem todos os acontecimentos precisam ser lembrados para sempre.

Pequenos feitos poderão perder importância com o tempo.

Exemplo:

```text
Briga de taverna
↓
meses passam
↓
reputação relacionada diminui
```

Acontecimentos históricos poderão permanecer praticamente para sempre.

Exemplo:

```text
Matou um deus
```

ou:

```text
Destruiu um reino
```

Esses feitos poderão continuar sendo lembrados durante gerações.

## Herança de reputação

Algumas reputações poderão afetar familiares ou associados.

Exemplo:

```text
Pai:
Traidor do reino

Filho:
Pode sofrer desconfiança por associação
```

Isso dependerá da cultura, facção e importância do acontecimento.

O filho não receberá automaticamente os mesmos valores, mas poderá carregar consequências sociais do nome da família.

## Reputação histórica

Personagens mortos deverão continuar possuindo reputação.

Um antigo rei, herói ou criminoso poderá continuar sendo lembrado.

```text
NPC morreu há 80 anos
↓
Ainda possui feitos históricos
↓
Histórias continuam circulando
```

Isso permitirá que o mundo desenvolva figuras históricas organicamente.

## Regra central

O sistema deverá funcionar através de:

```text
Acontecimento real
↓
Testemunhas
↓
Memórias
↓
Propagação de informação
↓
Interpretação individual ou coletiva
↓
Reputação
↓
Mudança de comportamento
```

A reputação nunca deverá representar simplesmente:

```text
bom ou mau
```

Ela deverá representar:

```text
quem conhece você
+
o que acredita que você fez
+
como interpreta esses feitos
+
o quanto esses acontecimentos são importantes
```

Dessa forma, o mesmo personagem poderá ser simultaneamente herói, assassino, libertador, herege e lenda dependendo de quem estiver contando sua história.
## 38. Sistema de Popularidade
## 37. Sistema de Reputação

O sistema de reputação será responsável por representar como personagens, grupos, cidades, facções e reinos enxergam uma entidade.

Tanto o jogador quanto NPCs poderão possuir reputação.

Reputação não será um único valor global.

Uma pessoa poderá ser considerada herói em uma cidade e assassino em outra.

Também deverá existir diferença entre:

```text
Popularidade
```

e:

```text
Reputação
```

Popularidade representa o quanto uma entidade é conhecida.

Reputação representa pelo que ela é conhecida.

Exemplo:

```text
Jogador

Popularidade: 92

Reputações conhecidas:
Matador de Dragões: 95
Assassino: 65
Protetor de Aldeões: 40
Inimigo do Reino Valerius: 100
```

Um personagem extremamente conhecido não necessariamente será amado.

## Feitos

A reputação será construída principalmente através de feitos.

Um feito representa um acontecimento relevante associado a uma entidade.

Exemplos:

```text
Matou um rei
Salvou uma vila
Matou um deus
Venceu uma guerra
Assassinou um comerciante
Derrotou um personagem lendário
Traiu uma facção
Defendeu uma cidade
Roubou um artefato
Destruiu uma vila
```

Cada feito deverá possuir informações como:

```text
Autor
Tipo do feito
Alvo
Local
Turno/Data
Importância
Testemunhas
Conhecimento público
Facções afetadas
```

A reputação deverá ser consequência desses feitos.

## Reputação contextual

Um mesmo feito poderá gerar reputações completamente diferentes dependendo de quem o observa.

Exemplo:

O jogador mata o rei do Reino A.

Para habitantes leais ao Reino A:

```text
Regicida
Criminoso
Inimigo
```

Para uma facção rebelde:

```text
Libertador
Herói
Aliado
```

Para outro reino:

```text
Pessoa perigosa
Possível aliado
Ameaça política
```

Portanto:

```text
Feito
+
Valores do observador
+
Relações
+
Conhecimento
=
Reputação
```

## Reputação por entidade

Cada entidade poderá possuir sua própria opinião sobre outra.

Exemplo:

```text
NPC John
→ Jogador

Confiança: 80
Reputação percebida:
Herói: 70
Violento: 40
Confiável: 90
```

Outro NPC poderá enxergar o mesmo jogador como:

```text
NPC Marcus
→ Jogador

Confiança: 10
Reputação percebida:
Assassino: 80
Perigoso: 95
```

Não deverá existir obrigação de todos compartilharem a mesma visão.

## Reputação coletiva

Além da opinião individual, grupos poderão possuir uma visão coletiva.

Exemplo:

```text
Cidade de Arven
→ Jogador

Herói local: 85
Criminoso: 5
```

```text
Facção dos Corvos
→ Jogador

Inimigo: 90
Perigoso: 95
```

```text
Reino Valerius
→ Jogador

Procurado: 100
Regicida: 100
```

Essas reputações poderão influenciar NPCs pertencentes a esses grupos.

Entretanto, a opinião individual ainda poderá sobrescrever parcialmente a coletiva.

Exemplo:

Um guarda pertence ao Reino Valerius e recebe ordem para prender o jogador.

Porém:

```text
Jogador salvou sua filha
↓
Lealdade ao jogador: alta
↓
Lealdade ao reino: média
```

Esse conflito poderá afetar sua decisão.

## Tags de reputação

A reputação deverá utilizar conceitos ou tags associados aos feitos.

Exemplos:

```text
Herói
Assassino
Ladrão
Traidor
Libertador
Covarde
Mercenário
Caçador de monstros
Matador de dragões
Matador de deuses
Protetor
Cruel
Confiável
Desonrado
Santo
Herege
Rebelde
Conquistador
```

Essas tags poderão possuir intensidades.

Exemplo:

```text
Assassino: 35
Herói: 80
Confiável: 65
```

Os valores representam o quanto aquela reputação está associada ao personagem para determinada entidade ou grupo.

## Reputação específica por feito

Além de tags genéricas, acontecimentos extremamente importantes poderão possuir reputação própria.

Exemplo:

```text
"Matador de Dovha"
```

ou:

```text
"Responsável pela Queda de Arven"
```

Isso permitirá que acontecimentos procedurais criem identidades únicas.

O jogo não deverá depender apenas de títulos previamente programados.

## Origem da reputação

Toda reputação deverá possuir uma origem rastreável.

Exemplo:

```text
Reputação:
Assassino: +25

Origem:
Jogador matou Marcus na Praça de Arven.

Testemunhas:
12 NPCs
```

Isso será importante para evitar reputações surgindo sem explicação.

## Testemunhas

Um feito não deverá automaticamente se tornar conhecimento global.

Se o jogador matar alguém sem nenhuma testemunha e nenhuma evidência posterior:

```text
Mundo sabe:
Não

Jogador sabe:
Sim
```

A reputação não deverá ser alterada automaticamente para todos.

Caso alguém testemunhe:

```text
NPC testemunha assassinato
↓
Memória criada
↓
Conhecimento adquirido
↓
Possível propagação
↓
Reputação começa a se espalhar
```

O sistema de reputação deverá depender diretamente dos sistemas de memória e rumores.

## Rumores e reputação

Informações poderão se espalhar de forma imperfeita.

Exemplo real:

```text
Jogador matou 3 bandidos.
```

Primeiro rumor:

```text
"Um viajante matou três homens na estrada."
```

Depois:

```text
"Um guerreiro sozinho matou dez homens."
```

Mais tarde:

```text
"Dizem que ele matou vinte homens sem ser ferido."
```

A reputação poderá crescer mesmo com informações exageradas.

Isso permite reputação baseada tanto em fatos quanto em rumores.

## Reputação falsa

O mundo também poderá atribuir feitos incorretamente.

Exemplo:

Um NPC mata determinado personagem, mas espalha que foi o jogador.

Caso o rumor seja aceito:

```text
Jogador
→ reputação de assassino
```

mesmo sendo inocente.

Isso permitirá:

- Acusações falsas
- Manipulação
- Propaganda
- Difamação
- Falsos heróis
- Falsas lendas

Uma reputação não precisa representar a verdade objetiva do mundo.

Ela representa aquilo que as pessoas acreditam.

## Alcance da reputação

A reputação deverá possuir alcance geográfico.

Um jogador poderá ser extremamente conhecido em determinado reino e praticamente desconhecido em outro continente.

Exemplo:

```text
Reino A:
Popularidade 95

Reino B:
Popularidade 40

Região distante:
Popularidade 5
```

Rumores, comerciantes, viajantes, soldados e outros personagens poderão carregar histórias para novas regiões.

## Velocidade de propagação

A velocidade de propagação poderá depender da importância do feito.

Exemplo:

```text
Jogador roubou pão
→ propagação local

Jogador matou um guarda
→ cidade

Jogador matou um rei
→ reino e regiões próximas

Jogador matou um deus
→ possível propagação continental
```

Quanto maior o acontecimento, maior a chance de ele viajar grandes distâncias.

## Popularidade

Popularidade representará apenas o nível de reconhecimento do personagem.

Exemplo:

```text
0-10:
Praticamente desconhecido

11-30:
Conhecido localmente

31-60:
Conhecido regionalmente

61-80:
Muito conhecido

81-99:
Famoso

100:
Figura mundialmente conhecida
```

Essa escala deverá ser apenas referência e poderá ser ajustada.

Popularidade poderá aumentar por feitos positivos ou negativos.

Um criminoso extremamente perigoso poderá possuir popularidade máxima.

## Reconhecimento

NPCs não deverão reconhecer automaticamente alguém apenas porque sua popularidade é alta.

O reconhecimento poderá depender de fatores como:

- Região
- Conhecimento do NPC
- Descrição física
- Armadura
- Equipamento famoso
- Apelido
- Rumores
- Encontros anteriores

Exemplo:

O jogador possui:

```text
Popularidade: 90
Apelido: Matador do Sol
```

Mas está em uma região distante onde sua aparência não é conhecida.

Um NPC poderá saber:

```text
"Existe alguém chamado Matador do Sol."
```

sem perceber que a pessoa na sua frente é ele.

## Equipamentos e reputação

Itens famosos também poderão revelar identidade.

Exemplo:

```text
Jogador possui:
Aurora, Espada do Fogo Eterno
```

Um sacerdote conhece a arma.

```text
Sacerdote reconhece Aurora
↓
Associa arma ao jogador
↓
Percebe que está diante do Matador do Deus do Fogo
```

Portanto, equipamentos poderão carregar reputação.

## Títulos e apelidos

A reputação poderá gerar apelidos automaticamente.

O jogador deverá iniciar como:

```text
Desconhecido
```

Conforme acumula feitos, poderá receber títulos.

Exemplos:

```text
Hugo, o Matador de Lobos

Hugo, o Regicida

Hugo, Quebra-Coroas

Hugo, Carrasco dos Deuses
```

Os títulos deverão surgir a partir dos feitos realmente realizados durante aquela campanha.

Diferentes regiões poderão inclusive utilizar apelidos diferentes para a mesma pessoa.

Exemplo:

```text
Reino A:
"O Libertador"

Reino B:
"O Açougueiro"
```

## Reputação de NPCs

NPCs utilizarão exatamente o mesmo sistema.

Um NPC poderá começar como personagem comum e tornar-se famoso através da simulação.

Exemplo:

```text
Soldado desconhecido
↓
Mata general inimigo
↓
Sobrevive a três batalhas
↓
Torna-se conhecido
↓
Recebe promoção
↓
Torna-se comandante
↓
Torna-se personagem importante
```

Isso significa que as categorias:

```text
Comum
Importante
Lendário
```

não precisam ser completamente permanentes.

Um NPC poderá subir de importância conforme seus feitos.

## NPCs lendários emergentes

Um personagem não precisa nascer lendário.

A própria simulação poderá criar uma lenda.

Exemplo:

```text
Ferreiro comum
↓
Cidade atacada
↓
Defende moradores usando martelo
↓
Mata líder inimigo
↓
Sobrevive
↓
História se espalha
↓
"Martelo de Arven"
```

Esse NPC poderá posteriormente tornar-se uma figura importante.

## Reputação e medo

Reputação positiva e medo deverão ser conceitos diferentes.

Exemplo:

```text
Admiração: 10
Medo: 95
```

Um personagem pode ser odiado e ainda assim possuir enorme influência.

Outro poderá possuir:

```text
Admiração: 90
Medo: 5
```

Esses valores poderão afetar interações diferentes.

## Reputação e confiança

Reputação também não deverá ser confundida com confiança.

Um NPC pode reconhecer o jogador como grande herói:

```text
Reputação positiva: 90
```

mas ainda não confiar pessoalmente nele:

```text
Confiança: 20
```

Confiança deverá ser construída principalmente através de relações diretas.

## Reputação e comportamento

A reputação deverá modificar o comportamento do mundo.

Exemplos:

### Jogador conhecido como herói

NPCs poderão:

- Pedir ajuda
- Oferecer descontos
- Procurar proteção
- Contar informações
- Tentar acompanhá-lo

### Jogador conhecido como criminoso

NPCs poderão:

- Fugir
- Alertar guardas
- Recusar comércio
- Tentar capturá-lo
- Mentir por medo

### Jogador conhecido como guerreiro lendário

NPCs fracos poderão evitar confrontos.

```text
NPC considera atacar jogador
↓
Memória/conhecimento:
Jogador matou personagem lendário
↓
Personalidade:
Covarde
↓
Desiste do confronto
```

Um NPC extremamente corajoso ou vingativo poderá atacar mesmo assim.

## Reputação com facções

Cada facção deverá possuir reputação própria em relação ao jogador e outros personagens.

Exemplo:

```text
Mercenários:
+60

Reino Valerius:
-100

Culto Solar:
-80

Caçadores:
+25
```

A reputação poderá afetar:

- Hostilidade
- Comércio
- Contratos
- Acesso a locais
- Ajuda
- Informações
- Recrutamento
- Recompensas

## Crimes e recompensas

Crimes conhecidos poderão gerar recompensas.

Exemplo:

```text
Jogador mata nobre importante
↓
Crime se torna conhecido
↓
Reino identifica jogador
↓
Recompensa criada
```

O valor poderá depender de:

- Importância da vítima
- Quantidade de crimes
- Periculosidade do jogador
- Recursos da facção
- Reputação anterior

Isso poderá alimentar diretamente o sistema de necessidades.

```text
Mercenário precisa de dinheiro
+
Jogador possui recompensa
+
Mercenário acredita conseguir vencê-lo
=
Possível caça ao jogador
```

## Decaimento da reputação

Nem todos os acontecimentos precisam ser lembrados para sempre.

Pequenos feitos poderão perder importância com o tempo.

Exemplo:

```text
Briga de taverna
↓
meses passam
↓
reputação relacionada diminui
```

Acontecimentos históricos poderão permanecer praticamente para sempre.

Exemplo:

```text
Matou um deus
```

ou:

```text
Destruiu um reino
```

Esses feitos poderão continuar sendo lembrados durante gerações.

## Herança de reputação

Algumas reputações poderão afetar familiares ou associados.

Exemplo:

```text
Pai:
Traidor do reino

Filho:
Pode sofrer desconfiança por associação
```

Isso dependerá da cultura, facção e importância do acontecimento.

O filho não receberá automaticamente os mesmos valores, mas poderá carregar consequências sociais do nome da família.

## Reputação histórica

Personagens mortos deverão continuar possuindo reputação.

Um antigo rei, herói ou criminoso poderá continuar sendo lembrado.

```text
NPC morreu há 80 anos
↓
Ainda possui feitos históricos
↓
Histórias continuam circulando
```

Isso permitirá que o mundo desenvolva figuras históricas organicamente.

## Regra central

O sistema deverá funcionar através de:

```text
Acontecimento real
↓
Testemunhas
↓
Memórias
↓
Propagação de informação
↓
Interpretação individual ou coletiva
↓
Reputação
↓
Mudança de comportamento
```

A reputação nunca deverá representar simplesmente:

```text
bom ou mau
```

Ela deverá representar:

```text
quem conhece você
+
o que acredita que você fez
+
como interpreta esses feitos
+
o quanto esses acontecimentos são importantes
```

Dessa forma, o mesmo personagem poderá ser simultaneamente herói, assassino, libertador, herege e lenda dependendo de quem estiver contando sua história.
## 39. Sistema de Títulos e Apelidos

Títulos e apelidos deverão surgir organicamente através da reputação, popularidade e feitos de uma entidade.

O jogador começará inicialmente como:

```text
Desconhecido
```

Conforme seus feitos forem conhecidos, novos nomes poderão surgir.

Exemplos:

```text
Matador de Reis
Protetor de Arven
Carrasco dos Dragões
O Regicida
O Sem-Rosto
Quebra-Coroas
```

Os títulos deverão estar relacionados a acontecimentos reais da campanha.

Diferentes regiões poderão utilizar títulos diferentes para a mesma pessoa.

NPCs também poderão receber títulos através do mesmo sistema.

## 40. Sistema de Quests Emergentes

Não existirão quests tradicionais geradas arbitrariamente pelo jogo.

As quests surgirão principalmente através do sistema de necessidades.

Fluxo básico:

```text
Necessidade
↓
Prioridade
↓
Personalidade
↓
Objetivo
↓
Ação
↓
Possível interação com o jogador
↓
Quest emergente
```

Exemplo:

```text
NPC perdeu a esposa
↓
Necessidade de encontrá-la
↓
Decide procurar ajuda
↓
Conhece/confia no jogador
↓
Pede ajuda
↓
Quest criada
```

Caso o jogador recuse, a necessidade continuará existindo e o NPC poderá procurar outra solução.

Uma quest, portanto, representa apenas uma necessidade do mundo na qual o jogador decidiu se envolver.

## 41. Sistema de Eventos Mundiais e História Procedural

O jogo não possuirá uma história principal fixa.

A história do mundo será formada pelos acontecimentos produzidos pela própria simulação.

Exemplos:

- Guerras
- Assassinatos
- Mortes de reis
- Mudanças de liderança
- Destruição de cidades
- Crises econômicas
- Rebeliões
- Surgimento de personagens lendários
- Morte de deuses
- Colapso de facções
- Descoberta de itens importantes
- Mudanças territoriais

Eventos importantes deverão ser registrados no histórico do mundo.

Exemplo:

```text
Ano 17

O Reino Valerius declarou guerra ao Reino Arven.

Ano 19

A cidade de Kars foi destruída.

Ano 21

O rei Aldren morreu em batalha.

Ano 22

Começou a Guerra de Sucessão Valeriana.
```

Não deverá existir obrigação de o jogador participar desses acontecimentos.

O mundo continuará produzindo sua própria história independentemente dele.

Eventos relevantes também poderão gerar novas necessidades, alterar reputações, criar rumores e modificar relações entre entidades.

## 43. Sistema de Personagens Lendários

Personagens lendários representam entidades extremamente importantes ou poderosas.

Poderão incluir:

- Grandes guerreiros
- Heróis
- Vilões históricos
- Líderes extremamente influentes
- Criaturas únicas
- Campeões de deuses
- Outros indivíduos excepcionais

Esses personagens deverão possuir maior profundidade de simulação.

Poderão possuir:

- Personalidade detalhada
- Memórias persistentes
- Objetivos de longo prazo
- Equipamentos únicos
- Alta popularidade
- Reputação própria
- Relações importantes
- Influência sobre o mundo

Um personagem não precisa necessariamente nascer lendário.

NPCs comuns ou importantes poderão atingir esse nível através de feitos realizados durante a simulação.

## 44. Sistema de Personagens Importantes

Personagens importantes ocupam posições relevantes no mundo sem necessariamente serem lendários.

Exemplos:

- Reis
- Príncipes
- Generais
- Líderes de facção
- Nobres
- Sacerdotes importantes
- Comerciantes poderosos
- Governadores

Eles deverão possuir simulação mais detalhada que NPCs comuns.

Suas ações poderão afetar cidades, facções e reinos inteiros.

Personagens importantes também poderão subir para o nível lendário ou perder importância durante a campanha.

## 45. Sistema de NPCs Comuns

NPCs comuns representam a maior parte dos personagens individualmente simulados.

Exemplos:

- Agricultores
- Guardas
- Comerciantes
- Ferreiros
- Caçadores
- Civis
- Soldados
- Estudantes

Eles utilizarão os mesmos sistemas fundamentais dos demais personagens:

```text
Necessidades
Personalidade
Profissão
Memória
Conhecimento
Relacionamentos
Inventário
Reputação
```

Entretanto, poderão possuir menor profundidade de processamento para evitar custo desnecessário.

NPCs comuns poderão se tornar importantes caso seus feitos justifiquem isso.

## 46. Sistema de População Abstrata

Nem todo habitante do mundo precisará existir como um NPC completamente simulado.

Cidades, vilas e reinos poderão possuir população abstrata.

Exemplo:

```text
Cidade de Arven

População:
3.420

NPCs individualmente simulados:
186
```

O restante da população poderá ser utilizado para cálculos de:

- Economia
- Produção
- Consumo
- Mortalidade
- Recrutamento
- Criminalidade
- Crescimento populacional

Quando necessário, um indivíduo abstrato poderá ser transformado em NPC persistente.

Exemplo:

```text
Jogador procura um ferreiro
↓
Sistema necessita de novo NPC
↓
Habitante abstrato é materializado
↓
NPC passa a existir permanentemente
```

## 47. Sistema de Níveis de Simulação dos NPCs

NPCs não deverão possuir o mesmo nível de processamento o tempo inteiro.

O nível de simulação dependerá principalmente de importância e proximidade do jogador.

### Simulação Alta

Utilizada para:

- NPCs próximos do jogador
- Personagens lendários
- Personagens diretamente envolvidos em acontecimentos importantes

Poderá processar:

```text
Movimentação
Necessidades
Memória
Objetivos
Interações
Combate
Rotina
```

### Simulação Média

Utilizada para personagens importantes distantes.

Poderá atualizar seus estados em intervalos maiores.

### Simulação Baixa

Utilizada para NPCs comuns distantes do jogador.

Suas atividades poderão ser resumidas.

Exemplo:

```text
Ferreiro trabalhou durante o dia
↓
Produziu 3 itens
```

em vez de simular individualmente cada ação realizada.

Esse sistema será importante para permitir grandes populações sem processar todos os NPCs detalhadamente a cada turno.

## 49. Sistema de Diálogo

O jogador poderá conversar com qualquer NPC individual existente.

O diálogo deverá considerar informações reais da entidade.

Exemplos:

- Personalidade
- Memórias
- Conhecimento
- Relação com o jogador
- Profissão
- Reputação do jogador
- Necessidades atuais
- Situação do mundo

NPCs comuns não precisam possuir diálogos escritos manualmente.

A IA poderá gerar respostas utilizando exclusivamente o contexto disponibilizado pelo jogo.

A IA não deverá alterar diretamente o estado do mundo.

Exemplo:

```text
NPC possui necessidade:
Encontrar filha

NPC conhece:
Jogador possui boa reputação

NPC confia no jogador:
75
```

Essas informações poderão ser enviadas para a IA gerar naturalmente um pedido de ajuda.

As decisões reais continuarão pertencendo ao motor do jogo.

## 53. Sistema de Eventos e Event Bus

Os sistemas deverão se comunicar preferencialmente através de eventos quando apropriado.

Exemplo:

```text
CharacterKilled
```

poderá ser recebido por:

```text
Sistema de memória
Sistema de reputação
Sistema de necessidade
Sistema de família
Sistema de rumores
Sistema de história
```

Isso evita que o sistema de combate precise conhecer diretamente todos os sistemas que serão afetados pela morte.

Exemplos de eventos:

```text
CharacterKilled
ItemCreated
ItemStolen
KingDied
WarStarted
CityCaptured
FactionDestroyed
RelationshipChanged
QuestCreated
```

O Event Bus será interno ao jogo e não deverá depender de sistemas externos de mensageria.

## 54. Sistema de Persistência

O estado importante do mundo deverá ser persistido.

Isso inclui principalmente:

- Seed
- Mundo
- Entidades
- NPCs
- Relações
- Itens
- Inventários
- Facções
- Reinos
- Eventos históricos
- Memórias relevantes
- Estado econômico
- Posição do jogador

O sistema de persistência deverá permanecer separado da lógica principal do jogo.

O motor não deverá depender diretamente de uma implementação específica de armazenamento.

## 55. Sistema de Save e Load

O jogador poderá salvar e carregar campanhas.

O save deverá armazenar informações suficientes para reconstruir exatamente o estado atual do mundo.

Exemplo:

```text
Seed
Turno atual
Estado do jogador
Estado das entidades
Mapa
Relações
Eventos
Economia
```

Ao carregar:

```text
Save
↓
Reconstrução do World State
↓
Continuação da simulação
```

A seed sozinha não será suficiente depois que a campanha já tiver sofrido alterações.

## 56. Estrutura de Dados e Entity IDs

Todas as entidades relevantes deverão utilizar identificadores únicos.

Exemplo:

```text
EntityID: 18592
```

Isso poderá ser utilizado para:

- NPCs
- Jogador
- Facções
- Reinos
- Cidades
- Itens
- Deuses
- Outros objetos persistentes

Nomes nunca deverão ser utilizados como identificadores principais.

Exemplo:

```text
John Hammer
ID: 8291
```

Dessa forma, poderão existir personagens com nomes iguais sem causar conflitos.

O grafo também deverá utilizar `EntityID` para criar relações.

## 57. Arquitetura Modular

O projeto deverá possuir arquitetura modular.

Os principais sistemas deverão permanecer separados.

Exemplo:

```text
world
character
needs
personality
memory
knowledge
faction
kingdom
economy
items
combat
reputation
events
ai
persistence
ui
```

Um sistema não deverá assumir responsabilidades pertencentes a outro.

Sempre que possível, sistemas deverão se comunicar através de interfaces, eventos ou estruturas bem definidas.

A lógica do jogo deverá permanecer independente da interface.

O objetivo é permitir que sistemas sejam alterados ou expandidos sem exigir reescrever o projeto inteiro.

## 58. Interface Inicial do Jogo

A interface inicial deverá ser simples e focada em texto.

Ela deverá permanecer completamente separada do motor do jogo.

O mapa visível será uma matriz `5x5`.

A disposição inicial poderá seguir aproximadamente:

```text
┌────────────────────────────────────────────────────┐
│ Informações / Local                │   MAPA 5x5     │
│                                    │               │
│                                    │   . . . . .   │
│                                    │   . . F . .   │
│                                    │   . . @ . .   │
│                                    │   . C . . .   │
│                                    │   . . . . .   │
├────────────────────────────────────────────────────┤
│                                                    │
│ Eventos / descrição / diálogo                     │
│                                                    │
├────────────────────────────────────────────────────┤
│ Ações disponíveis                                 │
│ > mover                                           │
│ > listar                                          │
│ > conversar                                       │
│ > inventário                                      │
└────────────────────────────────────────────────────┘
```

O mapa deverá permanecer no canto superior direito.

Outras áreas poderão mostrar:

- Informações da posição atual
- NPCs presentes
- Eventos recentes
- Diálogos
- Vida
- Equipamentos
- Ações disponíveis

A interface não deverá conter regras do jogo.

Ela apenas envia comandos ao motor e apresenta os resultados.

## 59. Testes de Simulação

O jogo deverá possuir testes focados principalmente na estabilidade da simulação.

Deverá ser possível rodar o mundo sem jogador durante grandes quantidades de turnos.

Exemplo:

```text
SimulateWorld(
    turns = 10000
)
```

Os testes deverão procurar problemas como:

- Crashes
- Relações inválidas
- Entidades inexistentes
- Economia quebrada
- Loops infinitos de necessidades
- NPCs presos
- Reinos impossíveis
- Valores fora dos limites
- Crescimento descontrolado de memória

Seeds conhecidas poderão ser utilizadas para reproduzir bugs.

Exemplo:

```text
Seed: Dovha
Turno: 8421

Erro:
NPC tentou interagir com personagem morto.
```

Utilizando a mesma seed e estado correspondente, o erro deverá poder ser investigado novamente.

## 60. Escopo do Primeiro MVP

O primeiro MVP não deverá tentar implementar todos os sistemas descritos no documento.

O objetivo inicial será provar que o núcleo da simulação funciona.

O MVP deverá possuir:

```text
Seed determinística
Mapa procedural
Movimentação em matriz
NPCs
Entity IDs
Personalidade
Necessidades
Prioridades
Objetivos
Profissões básicas
Relacionamentos
Memória básica
Conhecimento
Itens
Inventário
Economia básica
Facções simples
Reinos simples
Event Bus
Save e Load
Interface textual
```

A primeira versão deverá permitir uma situação semelhante a:

```text
Mundo é gerado
↓
NPCs recebem profissões e personalidades
↓
NPCs possuem necessidades
↓
Necessidades produzem objetivos
↓
NPCs realizam ações
↓
Ações modificam o mundo
↓
Mudanças criam novas necessidades
↓
Simulação continua
```

A IA generativa não deverá ser responsável pelo funcionamento do MVP.

O motor deverá funcionar completamente sem ela.

Quando o núcleo estiver funcional, a IA poderá ser integrada principalmente para:

```text
Diálogos
Descrições
Lore
Interpretação narrativa dos acontecimentos
```

A IA deverá trabalhar sobre o estado produzido pela simulação, sem substituir os sistemas responsáveis pelas regras do mundo.

A prioridade do primeiro MVP é provar que o mundo consegue funcionar e produzir acontecimentos interessantes sozinho