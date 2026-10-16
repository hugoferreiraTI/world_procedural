# Auditoria do jogador — 10.000 turnos

Seed **Dovha**, regras **mvp-2**, executada em 7 de outubro de 2026. Foram
**10.000 ações bem-sucedidas de uma hora**, além de **514 tentativas rejeitadas**
que não avançaram o relógio. Começou no turno mundial 24 e terminou
no turno 10024. Tempo: 75.39 segundos.

A campanha é automatizada, não uma partida humana. O controlador usa comandos
públicos, inventário, consultas, mensagens e locais conhecidos pelo jogador. Leitura
global serve à auditoria, não à escolha de ações. Não houve teleporte, alteração
manual de atributos, concessão de dinheiro ou mudança nas regras do motor durante
os 10.000 turnos. As reproduções isoladas usam fixtures explicitamente configuradas,
em mundos descartáveis, e não fazem parte dessa campanha.

## Resultado da campanha

- Jogador vivo, vida **100**, fome **40**, sede **20**, **0 moedas**.
- Visitou **Karmir**, **Dorven** e o mapa externo; **15 NPCs distintos** encontrados.
- **95 pedidos**: **66 autônomos**, **29 iniciados em conversas**.
- **33 quests concluídas**, **32 resolvidas por outra solução**, **30 recusadas**.
- **499 refeições**, **643 coletas**, **32 trabalhos por alimento**, **70 entregas**,
  **15 compras**, **24 vendas**, **406 conversas** e **995 descansos**.
- **116 NPCs morreram**; restaram **300 vivos**. Houve **25 mortes com fome 100
  e comida no inventário**; parte desses NPCs também estava com sede 100.
- Ao final: **48 de 70 mercados sem comida**, **3 cidades sem NPC local
  vivo** e **6 reinos sem governante**, mantendo a crise sucessória explícita.

A política teve **5.715 horas de espera** e **4.285 ações de outras categorias**.
Explorou bairros e dois mapas urbanos, mas não representa exploração completa dos
seis reinos. A continuidade dependeu de comida e água reais; nenhuma cura de
inanição por descanso ocorreu. Não houve crash, IDs inválidos ou divergência
monetária nos dez checkpoints. O save final foi recarregado e serializado de forma
exatamente igual. A suíte existente continua passando: **43 testes**.

## Bugs confirmados

### B02 — P1: jogador e NPC sofrem a fome em ordens diferentes

**Observado na campanha e confirmado em reprodução isolada.**

No turno mundial **679**, Ruan Luar (ID 633, comerciante) morreu com **fome 100,
sede 74 e uma ração**. Outros casos constam no JSON de mortes. Isso expõe um
problema na ordem de execução, confirmado sem sede crítica:

1. Configurar jogador e NPC com vida 1, fome 100, sede 0, ambos possuindo comida.
2. Jogador executa `comer`.
3. Jogador come antes do tick e sobrevive com vida 1; o NPC recebe dano antes de
   decidir comer, morre e deixa duas rações no inventário.

**Causa:** comandos do jogador executam a ação e depois chamam `step`; NPCs
recebem fisiologia e checagem de morte antes de `goals.decide`.
A fisiologia compartilhada não torna o relógio das ações simétrico.
Código: [procedural/engine.py:66](</home/hugo/Área de trabalho/procedrual/procedural/engine.py:66>) e
[procedural/engine.py:85](</home/hugo/Área de trabalho/procedrual/procedural/engine.py:85>).

**Impacto:** alimento disponível no instante crítico pode salvar o jogador e
não salvar um NPC equivalente. Os 25 registros de morte com comida não provam,
sozinhos, que todos seriam evitados: há sede crítica em parte deles. A reprodução
sem sede comprova a assimetria especificamente.

**Direção de correção:** definir uma ordem comum de decisão, ação, fisiologia e
morte, considerando o custo temporal de adquirir comida e o de consumi-la.

### B04 — P2: possuir 10 moedas impede pedir ajuda mesmo sem poder comprar comida

**Confirmado em reprodução isolada, não contabilizado como ocorrência espontânea
na campanha principal.**

NPC faminto, sem comida, conhecido e próximo do jogador. O mercado possui uma
ração por **14 moedas**, enquanto o NPC tem **10**. A decisão corretamente remove
`buy_food`, considera `ask_help` e pontua o jogador como melhor interlocutor.
Ao executar o pedido, recebe **“Pedido indisponível”**.

**Causa:** `QuestSystem.offer` rejeita qualquer NPC com `money >= 10`,
independentemente do preço e da disponibilidade real do alimento.
Código: [procedural/quests.py:18](</home/hugo/Área de trabalho/procedrual/procedural/quests.py:18>).

**Impacto:** candidato considerado viável por um sistema é recusado por outro,
com perda de tempo e bloqueio temporário da ação em uma necessidade urgente.
**Direção de correção:** compartilhar a mesma avaliação de capacidade de resolver
a fome, usando preço/estoque somente quando forem observáveis ou conhecidos.

### B01 — P2: ação inválida cria necessidades e altera o contador de IDs

**Observado na própria campanha e confirmado em reprodução isolada.**

Na posição externa inicial, sem necessidade de comida ativa:

- `coletar` falha: “Vá até uma área conhecida de coleta”.
- O turno permanece igual, mas surge uma necessidade `food` com urgência zero.
- `next_id` cresce em 1. `trabalhar` fora da área rural também cria `work` antes
  de verificar se o trabalho é possível.

Na campanha isso ocorreu antes da entrada em Karmir. Não é perda de dinheiro
nem avanço do relógio, mas um estado alterado por ação rejeitada.
**Causa:** `_action` chama `needs.ensure` antes de validar a execução.
Código: [procedural/engine.py:144](</home/hugo/Área de trabalho/procedrual/procedural/engine.py:144>).

**Direção de correção:** validar precondições antes de persistir pressão/objetivo,
ou usar intenção temporária e só consolidar efeitos após sucesso.

### B05 — P2: rumor mais confiável não atualiza um fato já conhecido

**Confirmado em reprodução isolada. A campanha não mede quantas oportunidades de
reforço foram perdidas; não há contagem inventada desse problema.**

O jogador conhece um favor por rumor com confiança **30**. Um NPC próximo viu
esse favor diretamente (confiança **100**) e o jogador confia nele em **95**.
A rodada de rumores deixa o fato em **30**. Conversar com o mesmo NPC eleva a
certeza para **80**, mostrando que o mecanismo de atualização existe.

**Causa:** `gossip` exclui qualquer fato cujo ID já esteja no conhecimento do
ouvinte, antes de verificar se a fonte pode oferecer evidência melhor.
Código: [procedural/knowledge.py:87](</home/hugo/Área de trabalho/procedrual/procedural/knowledge.py:87>).

**Impacto:** atualização de crença depende do canal. Uma notícia corrigida/reforçada
pela rede social fica bloqueada enquanto a versão fraca permanecer na memória.
**Direção de correção:** permitir reforços factuais por diferença de confiança,
preservando a idempotência da contribuição de reputação.

## Inconsistências e decisões de design

### B03 — Consequência de B02: entrega concluída seguida de morte

Em fixture isolada, aceitar um pedido e entregar comida a um NPC com vida 1 e
fome 100 produz `HelpGiven` e `QuestCompleted`; no tick seguinte do mesmo comando,
o NPC morre antes de comer. A quest permanece `completed` e ele deixa a ração.

**Não apareceu nas 70 entregas da campanha principal** e não é contado como
um quinto bug independente. A morte antes de agir deriva de B02. Além disso,
“conseguir alimento” pode ter apenas a entrega como objetivo; exigir sobrevivência
é uma decisão sobre o contrato da quest. Convém definir esse critério e distinguir
entrega material de socorro efetivo. Código: [procedural/quests.py:54](</home/hugo/Área de trabalho/procedrual/procedural/quests.py:54>).

### B06 — Comunicação instantânea de resposta entre mapas

Em reprodução, o jogador sai do mapa da cidade por comandos normais e recusa um
pedido. O NPC, ainda no mapa urbano, conhece a recusa imediatamente; sua confiança
cai de **60 para 47**. O evento ocorre no mapa externo, mas ambos são registrados
como participantes que sabem do fato.

Não existe carta, mensageiro ou comunicação à distância nessa sequência.
A interface permite responder de qualquer lugar. É uma inconsistência com a
localidade da informação, salvo se respostas remotas forem uma convenção explícita
pretendida pelo jogo. Código: [procedural/quests.py:35](</home/hugo/Área de trabalho/procedrual/procedural/quests.py:35>).

## Limitações e balanceamento que permanecem

### L01 — População e trabalho: pendente pela orientação anterior do usuário

Cidades com população contábil elevada continuam sem NPC local vivo:

| Cidade | ID | População contábil | NPCs locais vivos |
|---|---:|---:|---:|
| Karmir | 3 | 2.994 | 0 |
| Morvia | 471 | 4.321 | 0 |
| Valvia | 1109 | 3.867 | 0 |

A reposição profissional não foi implementada nesta etapa. A capital inicial
Karmir ficou sem habitantes locais simulados vivos, enquanto o jogador continuou
em Dorven. Terreiros, mercado e população abstrata não repõem os vínculos perdidos.

### L02 — Economia e dinastias continuam frágeis

Ao final, 48 mercados estavam sem alimento e os seis reinos sem governante.
O estado político permaneceu coerente; isso não significa que o mundo esteja
balanceado. Mudança do modelo populacional, demanda, produção e logística deve
considerar esses números, sem compensar o problema por cura artificial.

As **24 vendas e 15 compras** não populam `Town.demand`: o campo estava vazio em
todas as cidades ao final. A curva reage ao estoque, mas o componente separado
de demanda está inativo. Não é lucro artificial nem moeda criada: todo aumento
de moeda global correspondeu à fonte abstrata registrada.

### L03 — Cansaço 100 é pressão sem penalidade física para o jogador

Em teste separado de **201 turnos**, mantendo alimentação e água por comandos
públicos e sem descansar, o jogador chegou a **cansaço 100**, continuou com vida
100 e ainda pôde mover-se normalmente. É uma limitação atual da fisiologia;
exaustão, velocidade ou penalidade de trabalho não têm regra implementada.
Na campanha principal o controlador descansou e o cansaço máximo foi 78.

## Checkpoints

| Horas de campanha | Vida jogador | NPCs vivos | Mercados sem comida | Cidades sem NPC local vivo | Diferença no balanço de moeda |
|---:|---:|---:|---:|---:|---:|
| 1.000 | 100 | 334 | 37 | 3 | 0 |
| 2.000 | 100 | 313 | 42 | 3 | 0 |
| 3.000 | 100 | 308 | 45 | 3 | 0 |
| 4.000 | 100 | 306 | 43 | 3 | 0 |
| 5.000 | 100 | 305 | 45 | 3 | 0 |
| 6.000 | 100 | 305 | 45 | 3 | 0 |
| 7.000 | 100 | 303 | 45 | 3 | 0 |
| 8.000 | 100 | 303 | 47 | 3 | 0 |
| 9.000 | 100 | 300 | 48 | 3 | 0 |
| 10.000 | 100 | 300 | 48 | 3 | 0 |

Os números mundiais servem ao diagnóstico: o jogador não os consultou para
escolher aonde ir. “Sem NPC local vivo” considera personagem vivo fisicamente no
mapa da cidade, não líderes associados à cidade que vivem em outro interior.

## Registro das ações

| Comando | Horas avançadas |
|---|---:|
| `entrar` | 2 |
| `norte` | 242 |
| `oeste` | 294 |
| `coletar` | 643 |
| `trabalhar` | 32 |
| `leste` | 293 |
| `conversar` | 406 |
| `beber` | 444 |
| `comer` | 499 |
| `sul` | 233 |
| `descansar` | 995 |
| `entregar` | 70 |
| `esperar` | 5.715 |
| `aceitar` | 62 |
| `comprar` | 15 |
| `sair` | 1 |
| `vender` | 24 |
| `recusar` | 30 |

Tentativas rejeitadas incluem pedir comida a alguém indisposto, beber longe de
poço sem água carregada, vender para mercado saturado e trabalhar sem capacidade
de produção. Rejeição correta de uma ação não é classificada como bug.

## Evidências e reprodução

- [Relatório JSON](relatorio.json): ações, quests, mortes com inventário, reações e checkpoints.
- [Transcrição integral](acoes.jsonl): cada tentativa, resposta, estado e mudanças de quest.
- [Reproduções isoladas](reproducoes.json): valores antes/depois dos sete cenários examinados.
- [Resumo auditável](auditoria.json): classificações, integridade e hash das regras.
- [43 testes existentes](testes.txt): todos passaram; os quatro bugs mostram lacunas nessa cobertura.
- [Save de 1.000 turnos](save_1000.json), [save de 5.000](save_5000.json), [save final](save_final.json).

```bash
python3 -m experiments.player_audit --seed Dovha --turnos 10000
python3 -m experiments.audit_reproductions
python3 -m unittest discover -s tests -v
```

Criados apenas os controladores/diagnósticos e os arquivos de evidência desta
auditoria. As regras do jogo foram mantidas para testar a versão existente.
Prioridade recomendada: corrigir a ordem temporal B02; depois unificar viabilidade
do pedido B04, rejeição sem efeitos B01 e atualização de informação B05.
