# Fase 3.2 — diagnóstico de reserva, acesso alimentar e bugs sociais

**Data: 8 de outubro de 2026. Escopo: investigação para análise do usuário.** Nesta etapa, não apliquei mudanças de prioridade, salário, preço, estoque ou comportamento social. Criei observadores, reproduções controladas e este relatório. As sugestões ao final ainda não foram implementadas.

## Resultado principal

Os três problemas possuem causas identificáveis, mas não vêm de uma única falha:

1. **A reserva preventiva existe, porém está quase sempre abaixo das outras necessidades na fila.** Sua prioridade máxima é 52, e o motor escolhe a primeira necessidade com alternativas. Nas janelas sem fome significativa, descanso e sede respondem por aproximadamente 79% das primeiras escolhas. O envelhecimento da reserva para de elevar sua prioridade depois de cerca de 54 horas.
2. **O acesso econômico depende de oportunidades executáveis, não só de dinheiro existente no mundo.** Os caixas municipais finais somam 1.460.520 moedas, enquanto os NPCs vivos somam 7.338. Há comida e caixa no mesmo mapa de 411 NPCs que não conseguem pagar uma refeição. Produção saturada, serviços temporários limitados e incompatibilidades de alternativas bloqueiam a circulação para parte das pessoas.
3. **Os dois bugs sociais vêm de pré-condições incompletas.** A denúncia escolhe um guarda observado sem excluir o culpado; a informação considera o assunto, mas não exige novidade ou utilidade para o problema atual. O transmissor também retorna sucesso mesmo quando o conhecimento do destinatário não melhora.

Encontrei **42 denúncias ao próprio culpado entre 337 denúncias**, em três campanhas de 10.000 horas. O caso conhecido de informação velha contém **quatro transmissões do mesmo fato**, no mesmo episódio familiar. Não trato isso como quatro histórias diferentes.

## Evidências utilizadas e limites do método

Analisei o código congelado da correção alimentar, os três saves finais e os registros completos das três campanhas anteriores de 10.000 horas. Além disso, reproduzi **as primeiras 1.000 horas de cada campanha**, com observadores novos de prioridade, escolha inicial, continuidade, trabalho e pagamento.

As três reproduções terminaram com **exatamente o mesmo SHA-256 do checkpoint canônico de 1.000 horas**. Os observadores não alteraram a aleatoriedade, decisões ou estados resultantes. O motor continua com SHA-256 **3ad877c9ff085a0d07009ffcdae917beb9473a012241c0f4e731ea7238ea363b**.

Também executei **cinco microdiagnósticos com verificações por assert**, em mundos descartáveis. Neles, valores iniciais são condições de laboratório para isolar cada mecanismo; nenhum dinheiro, alimento ou personagem dessas condições entrou nas campanhas reais. Não houve nova campanha completa de 10.000 horas nesta investigação, nem repetição desnecessária de toda a suíte de 130 testes, pois as regras permaneceram intactas.

As frequências de decisão e salário abaixo são das **1.000 horas iniciais**, somando eventos de avaliação, não personagens únicos. O censo econômico é do **final das campanhas de 10.000 horas**. As denúncias e pedidos de informação foram procurados nos **logs completos de 10.000 horas**. Esses três recortes não devem ser confundidos.

## 1. Por que a reserva preventiva quase nunca vence

### 1.1 A fórmula cria um teto estrutural baixo

A prioridade da reserva usa:

```text
26 + 8 × (déficit / alvo) + 0,2 × min(fome, 50) + bônus de idade
bônus de idade = min(8, idade da necessidade × 0,15)
```

Não há modificador de personalidade ou relação para `food_reserve`. Logo, com déficit máximo, fome 50 ou mais e idade já saturada, o máximo é **26 + 8 + 10 + 8 = 52**. Com uma ração e alvo de duas, cai para no máximo **48**.

O bônus de idade chega ao teto em aproximadamente **53,3 horas**; depois disso, a reserva pode esperar dias sem crescer mais. Seu valor não expressa quanto tempo resta até a próxima oportunidade de compra/trabalho ou quanto uma ida perdida custará.

Comparação das fórmulas atuais:

| Necessidade | Como cresce | Efeito sobre a reserva |
| --- | --- | --- |
| Reserva | Base, déficit, fome limitada a 50 e idade limitada a 8 | Teto 52; com uma ração normal, teto 48 |
| Descanso | Fadiga + idade | Uma fadiga intermediária já pode ultrapassar a manutenção |
| Água | Sede + idade; bônus em níveis altos; risco vital separado | Supera a reserva com facilidade e exige deslocamento quando não há água carregada |
| Renda | Pressão financeira até 70 + diligência/5 + idade | Pode chegar a 98 com atributos máximos permitidos |
| Trabalho | Base 35 + diligência/5 + idade | Pode chegar a 63, mesmo sem fome emergencial |
| Refeição | Fome + idade; prioridade emergencial 100 | A partir da fome alta, domina a reserva, como deve acontecer em emergência |
| Pessoais | Pressão própria, relação, personalidade e idade | Algumas corretamente vencem; não são o principal concorrente medido na janela preventiva |

Fontes: [fórmula da reserva](</home/hugo/Área de trabalho/procedrual/procedural/needs.py:105>), [prioridade e ordenação](</home/hugo/Área de trabalho/procedrual/procedural/needs.py:165>) e [modificadores pessoais](</home/hugo/Área de trabalho/procedrual/procedural/personal.py:228>).

### 1.2 O motor interrompe a análise na primeira necessidade atendível

`GoalSystem.decide` percorre necessidades já ordenadas. Para cada uma, enumera alternativas; ao encontrar uma lista não vazia, escolhe uma ação e sai do laço. Não compara o benefício de todas as ações de todas as necessidades.

Portanto, **aumentar o score de comprar comida dentro de `food_reserve` não faria a reserva superar descanso ou renda**. Esse score só participa depois que a necessidade alcança a etapa de alternativas. O problema principal está antes da utility da ação.

Fonte: [primeira necessidade com alternativas](</home/hugo/Área de trabalho/procedrual/procedural/goals.py:157>).

### 1.3 Medição das perdas reais

Nas reproduções, a reserva estava ativa em **376.485 avaliações**. Foi a necessidade selecionada em **2.018**, ou **0,54%**. A tabela separa o mecanismo imediato da perda:

| Avaliações com reserva ativa | Jogador Dovha | Espectador Dovha | Mundo Mira |
| --- | --- | --- | --- |
| Total | 126.746 | 129.771 | 119.968 |
| Reserva escolhida | 890 | 590 | 538 |
| Outra emergência analisada antes | 68.603 | 71.771 | 65.525 |
| Outra necessidade com prioridade maior | 57.241 | 57.408 | 53.895 |
| Empate de prioridade | 5 | 2 | 6 |
| Reserva era a primeira escolha, mas continuidade vetou | 7 | 0 | 4 |

Essa contagem identifica a necessidade selecionada. Trabalho pago com comida por uma necessidade de renda ou provisão familiar também pode repor inventário, sem contar como seleção de `food_reserve`. Não uso o percentual de 0,54% como medida de toda aquisição preventiva.

As avaliações incluem momentos em que o personagem já está em emergência alimentar. Nesse estado, a refeição vencer a reserva é correto. Para entender a prevenção, é preciso olhar separadamente a janela **fome <50**.

Nessa janela houve **33.319 avaliações com reserva insuficiente**. A reserva venceu em **1.805 — 5,42%**. Em **21.405 avaliações**, ela perdeu mesmo com comida municipal disponível e dinheiro para uma refeição pelo preço corrente observado pelo auditor: **64,24% de todas as avaliações dessa janela**.

Essa última contagem demonstra oportunidade física/financeira existente no instante, mas não garante cotação conhecida, rota curta ou ausência de disputa. O observador não forneceu o preço real remoto ao NPC. Ela permite rejeitar a explicação de que todas as perdas eram simplesmente falta de dinheiro.

| Primeira escolha quando fome <50 e falta reserva | Jogador Dovha | Espectador Dovha | Mundo Mira |
| --- | --- | --- | --- |
| Descanso | 5.554 | 5.401 | 5.043 |
| Água | 3.522 | 3.405 | 3.266 |
| Renda | 1.103 | 1.081 | 1.083 |
| Trabalho | 406 | 140 | 173 |
| Família | 390 | 337 | 303 |
| Reserva | 767 | 491 | 475 |

Somados, descanso e água correspondem a **26.191 das 33.319 primeiras escolhas**, aproximadamente **78,61%**. Família responde por 1.030. Assim, “as necessidades sociais estão tomando todo o tempo da reserva” não explica o padrão observado. Grande parte da concorrência vem das outras necessidades fisiológicas.

Exemplo real: **Mira Luar, ID 12, jogador Dovha, turno 24**. Fome 39, uma ração, 26 moedas; mercado da cidade com 30 rações, preço real 4. A reserva tem prioridade **38,85**; descanso, **44,75**. O motor seleciona descanso e começa a voltar para casa. Há meios de comprar uma ração, mas a prioridade coloca outra necessidade antes. Esse recorte mostra uma escolha normal, não prova que todo descanso nessa situação deveria ser proibido.

### 1.4 A continuidade existe, mas foi secundária na amostra

Um objetivo ativo pode continuar se a nova prioridade não superar a anterior em pelo menos **12 pontos**, com exceções vitais. Isso pode adiar reposição. Contudo, a medição encontrou somente **11 vetos diretos** de uma primeira escolha de reserva. Também encontrou **167 avaliações** nas quais a continuidade preservou uma reserva em andamento apesar de outra primeira escolha.

Logo, não recomendo culpar ou remover genericamente a continuidade: nessa amostra ela preservou mais escolhas de reserva do que vetou. O teto e a ordenação têm evidência quantitativa muito maior.

Exemplo de veto: **Iria Luar, ID 38, turno 221, jogador**. Reserva 33,5; objetivo de ascensão por trabalho 33,4, já em andamento. A reserva ganha inicialmente por 0,1, mas o objetivo continua pela margem de 12. Iria tinha uma ração, 40 moedas e 97 rações municipais.

Fonte: [continuidade do objetivo](</home/hugo/Área de trabalho/procedrual/procedural/goals.py:195>).

### 1.5 Uma ração reduz a pressão antes de completar a reserva

Comprar comida normalmente transfere **uma unidade**. O objetivo de compra termina após essa ação, enquanto a necessidade de reserva continua incompleta. Na próxima avaliação, possuir uma ração reduz o peso do déficit de 8 para 4. A segunda ração precisa vencer novamente, com prioridade menor.

Também existe uma lacuna de alternativas: `known_unaffordable` retorna falso assim que o personagem possui qualquer comida. Como esse método condiciona trabalho no ramo `food_reserve`, um NPC pobre com uma ração pode deixar de considerar trabalhar para financiar a segunda. O ramo geral de renda ainda pode oferecer trabalho; não significa que todo trabalho ficou impossível.

O microdiagnóstico isolou isso: dinheiro zero, fome 30, alvo duas rações. Com **zero rações**, alternativas incluem `work`; com **uma**, `work` desaparece desse ramo. Coleta e roubo continuam, e ofertas temporárias podem aparecer se suas condições forem satisfeitas. A compra não se torna acessível só porque há uma ração guardada.

Fontes: [alternativas alimentares](</home/hugo/Área de trabalho/procedrual/procedural/goals.py:40>), [qualquer comida elimina o indicador de impossibilidade de compra](</home/hugo/Área de trabalho/procedrual/procedural/economy.py:185>) e [compra unitária](</home/hugo/Área de trabalho/procedrual/procedural/goals.py:337>).

### 1.6 Tempo e oportunidade ainda não influenciam a pressão preventiva

O alvo usa cobertura temporal, mas a prioridade usa principalmente déficit e fome atuais. A avaliação de prazo biológico é um filtro posterior da solução alimentar; não aumenta a prioridade de uma oportunidade preventiva que está prestes a desaparecer.

NPCs comuns saudáveis podem ter até seis horas entre decisões. Uma compra de uma ração, uma ida para beber e uma volta para descansar podem consumir a pequena janela antes de fome 50. Deslocamento e concorrência precisam entrar na análise de oportunidade, sem promover toda manutenção a emergência.

**Diagnóstico desta frente:** o mecanismo preventivo está subordinado quase permanentemente a um conjunto de necessidades recorrentes. Não falta uma `Need`; falta uma relação eficaz entre cobertura, próxima oportunidade, prioridade e reposição até o alvo.

## 2. Por que ter comida na cidade não garante acesso individual

### 2.1 Dinheiro e comida estão separados da capacidade de obtê-los

O pagamento vem do caixa municipal. A compra transfere dinheiro do NPC para esse mesmo caixa; a produção de vários trabalhadores cria itens no inventário da cidade, enquanto o trabalhador recebe moeda. Se a produção é bloqueada ou a renda não é selecionada/concluída a tempo, o estoque pode existir sem capacidade de compra individual.

Censo final das campanhas de 10.000 horas:

| Condição final | Jogador Dovha | Espectador Dovha | Mundo Mira |
| --- | --- | --- | --- |
| NPCs vivos | 350 | 346 | 324 |
| Dinheiro abaixo de uma refeição | 172 | 158 | 135 |
| Sem comida e sem dinheiro para uma refeição | 127 | 118 | 93 |
| Pobre, com comida e caixa municipal no mesmo mapa | 144 | 144 | 123 |
| Pobre com profissão saturada | 52 | 45 | 36 |
| Pobre inelegível para trabalho temporário pago em produto | 20 | 16 | 13 |
| Dinheiro dos NPCs vivos | 2.797 | 2.309 | 2.232 |
| Dinheiro dos municípios | 506.243 | 516.639 | 437.638 |

Os **411 pobres com comida e caixa no mesmo mapa** são 88,39% dos 465 NPCs abaixo do preço de uma refeição no final. Esses valores são por campanha independente, somados para comparar condições; não existe transferência entre os três mundos.

O censo confirma concentração nos caixas municipais e dificuldade de acesso individual. Não prova que os caixas tinham esse mesmo dinheiro em todos os turnos anteriores nem atribui cada morte exclusivamente à concentração monetária.

Na auditoria alimentar anterior, **209 das 320 mortes com fome** ocorreram sem dinheiro para a cotação recente conhecida. Isso é condição terminal comprovada, não uma reconstrução completa da vida econômica de cada morto.

Fontes: [pagamento](</home/hugo/Área de trabalho/procedrual/procedural/economy.py:98>), [produção e salário](</home/hugo/Área de trabalho/procedrual/procedural/professions.py:80>) e [compra](</home/hugo/Área de trabalho/procedrual/procedural/economy.py:58>).

### 2.2 Produção saturada corta a renda do trabalhador

Agricultores, mineiros, lenhadores, caçadores e cozinheiros produzem para estoque municipal com limite. Se seu produto atinge o limite, a produção paga deixa de existir. O filtro `saturated` também pode remover a alternativa de trabalho a partir da observação conhecida.

Isso evita salário por produção inexistente e acúmulo infinito, mas gera uma consequência: **ter abundância de um produto pode tirar o emprego remunerado daquele produtor**. O problema passa de produção total para conversão da capacidade de trabalho em acesso a alimento. No final, **133 NPCs pobres** possuem profissão saturada.

Em 1.000 horas por modo, encontrei **636/643/685 falhas de trabalho** com a mensagem conjunta “Faltam materiais ou o estoque já atende à demanda”. São **1.964 falhas**. A mensagem não distingue falta de insumo de estoque saturado; não atribuo todas à saturação. O censo final e o código comprovam saturação como mecanismo, mas não sua parcela exata nessas falhas.

Trabalho remunerado que depende de insumo precisa considerar oferta realmente executável; saber que existe uma profissão não basta. Fonte: [limites de produção](</home/hugo/Área de trabalho/procedrual/procedural/professions.py:80>) e [remoção de trabalho saturado](</home/hugo/Área de trabalho/procedrual/procedural/goals.py:90>).

### 2.3 O trabalho temporário resolve parte do acesso, mas tem quota e elegibilidade

Há duas saídas existentes: preparar comida com trigo e receber parte da produção; distribuir refeições e receber uma ração. Elas funcionaram frequentemente nas reproduções, com bens reais.

Porém, a distribuição tem limite diário baseado na população abstrata. Cada porção exige **duas rações municipais**: uma remunera o trabalhador e a outra é consumida pela população. Se a quota diária já foi servida, não existe trabalho de distribuição restante, mesmo havendo muito alimento.

A oferta observada `temporary_work` é publicada por escassez ou dificuldade de compra no diagnóstico, mas a enumeração de `temporary_service` não verifica a quota restante. Assim, pode oferecer um serviço que só falhará na execução. Foram **46/32/51 falhas**, **129 no total**, por “Não há refeições para distribuir”.

O microdiagnóstico colocou 100 rações no mercado e quota diária já atendida: a alternativa foi oferecida, mas a execução falhou sem transferir alimento. Portanto, existe um desencontro específico entre **oferta anunciada** e **trabalho disponível**.

Além disso, guardas, soldados, governantes, conselheiros, estudantes e alguns aprendizes não participam automaticamente dessas tarefas de produto. Há **49 pobres finais inelegíveis**. Essa é uma restrição de design, não automaticamente um bug: precisamos de uma fonte de renda compatível, em vez de transformar toda profissão em cozinheiro.

Fontes: [observação das ofertas](</home/hugo/Área de trabalho/procedrual/procedural/economy.py:160>), [enumeração](</home/hugo/Área de trabalho/procedrual/procedural/goals.py:99>), [distribuição e quota](</home/hugo/Área de trabalho/procedrual/procedural/professions.py:37>).

### 2.4 Trabalho produtivo parcial pode ser tratado como falha de renda

Salário é registrado em **sextos de moeda**. Só valores inteiros são transferidos imediatamente. Isso conserva remuneração proporcional, mas o executor de `work`, quando ligado a `food` ou `money`, retorna falha se o dinheiro inteiro do personagem não aumentou naquela ação.

Um cozinheiro que produz uma ração com restos pode ganhar **2/6 de moeda**. Houve produção e crédito legítimos, mas nenhuma moeda inteira entrou ainda. O resultado é “O trabalho não trouxe o pagamento necessário”, e o `decide` aplica **cooldown de 12 horas** à ação que retornou falso.

O microdiagnóstico reproduziu exatamente isso: uma ração produzida, caixa municipal 500, crédito 2/6, dinheiro pago zero, resultado falso, moeda conservada. Na amostra houve **12/13/13 resultados dessa mensagem**, **38 ao todo**. Nenhuma chamada salarial observada teve uma moeda inteira devida e não paga; essa evidência enfraquece a hipótese de inadimplência de caixa como causa dessas falhas iniciais.

O aprendiz também recebe frações, mas usa a ação `train`, que tem tratamento diferente; não atribuo esse mesmo retorno falso a toda hora de treinamento. O problema aqui é confundir **não receber uma moeda inteira agora** com **não ter realizado trabalho remunerado útil**.

Fontes: [crédito salarial](</home/hugo/Área de trabalho/procedrual/procedural/economy.py:98>), [checagem de dinheiro imediato](</home/hugo/Área de trabalho/procedrual/procedural/goals.py:368>) e [cooldown após falha](</home/hugo/Área de trabalho/procedrual/procedural/goals.py:277>).

### 2.5 A hipótese de falta de caixa não foi confirmada nesses recortes

Nas chamadas de salário das 1.000 horas iniciais, não houve pagamento inteiro devido que ficou sem pagamento por falta de caixa. No censo final, nenhum NPC vivo estava vinculado a município com caixa zero, e nenhum pobre carregava crédito salarial de pelo menos uma moeda inteira sem recebimento.

Isso não garante liquidez em todos os turnos de 10.000 horas. Mostra que **não devemos começar a solução imprimindo mais dinheiro nem presumindo salários atrasados em massa**. Há caixa nos recortes medidos; os caminhos que permitem recebê-lo e usar alimento precisam melhorar.

### 2.6 Existem tentativas de renda estruturalmente incompatíveis com o lugar

Nos exemplos de falha “O local de trabalho ainda não foi alcançado”, dois líderes caçadores ilustram outro bloqueio. **Iria Solaris 1772** e **Cael Arven 1777**, em Dovha, vivem e têm local de trabalho nos quartéis **1771/1776**, mas conservam `town_id=3`. A profissão de produção exige também estar no mapa da cidade vinculada.

Assim, podem estar exatamente no local de trabalho do quartel e ainda falhar porque ele não é o mapa municipal. A geração retirou corretamente o acesso remoto ao mercado natal, mas o sistema de renda continuou enumerando trabalho naquele quartel sem uma economia remuneradora local correspondente.

Esse caso não explica a pobreza da maioria dos NPCs urbanos. É um exemplo confirmado de intenção de renda incompatível com seu contexto, e a mensagem de erro sugere deslocamento ainda incompleto quando o problema é o vínculo econômico/mapa.

Fontes: [origem e local de trabalho dos líderes](</home/hugo/Área de trabalho/procedrual/procedural/generation.py:243>) e [restrição da profissão](</home/hugo/Área de trabalho/procedrual/procedural/professions.py:80>). Não proponho habilitar produção ou recursos remotos para corrigir isso.

### 2.7 O filtro de sobrevivência chega depois do fracasso preventivo

O salário pleno nominal é de aproximadamente uma moeda por hora produtiva; o aprendiz recebe um terço. O preço mínimo de alimento é duas moedas e cresce com escassez e demanda. Crescimento de fome 2/h e nutrição 40 exigem aproximadamente **1,2 ração por dia**, no balanço fisiológico ideal, além do tempo de obter recursos e deslocar-se.

Se a renda não se realiza antes da fome alta, a sequência trabalho → salário → mercado → compra → consumo pode ultrapassar a margem biológica. O filtro corretamente rejeita essa sequência tardia. Ele não cria uma oportunidade de trabalho que não existe e não devolve o tempo já perdido.

O campo `economically_viable` da estimativa alimentar também é limitado: ele pressupõe rendimento nominal e não certifica, por si só, insumos, caixa futuro e execução da profissão. Filtros de candidatura e checagens de execução complementam a estimativa. Não deve ser apresentado como prova de que um emprego garantido estava disponível.

**Diagnóstico desta frente:** dinheiro agregado e comida agregada não se convertem automaticamente em direito de compra. O foco deve ser oportunidade local verificável, circulação por trabalho compatível e pagamento proporcional corretamente tratado, com reserva buscada antes de a cadeia ficar longa demais.

## 3. Bug social: denunciar o culpado para ele mesmo

### 3.1 A candidatura verifica profissão, não independência

Para `revenge`/`protection`, o código percorre observações pessoais e adiciona `denounce` para qualquer guarda observado vivo, quando existe evidência conhecida e ainda não houve denúncia. **Não compara esse guarda com `culprit`, `threat`, o ator do crime ou a pessoa denunciada.**

O score social pode favorecer alguém conhecido e confiável, mesmo que a evidência atual diga que essa mesma pessoa praticou o crime. Reputação negativa reduz preferência em alguns contextos, mas não substitui uma pré-condição de destinatário adequado.

Fonte: [candidatos a denúncia](</home/hugo/Área de trabalho/procedrual/procedural/personal_actions.py:51>).

### 3.2 A execução repete a lacuna e fecha o problema

O executor verifica se o destinatário está presente e se o denunciante conhece o fato. Transmite a informação, marca `reported=True`, emite `ThreatReported` e satisfaz a necessidade. Não impede transmitir a acusação ao próprio suspeito como se fosse denúncia independente bem-sucedida.

Portanto, não é só uma escolha ruim de personagem: **o sistema aceita e encerra a necessidade usando essa escolha**. Se a ação fosse uma confrontação ao acusado, precisaria ter significado e consequências próprios; hoje é registrada como denúncia a autoridade.

Fonte: [execução e satisfação](</home/hugo/Área de trabalho/procedrual/procedural/personal_actions.py:162>).

### 3.3 Frequência e exemplo confirmado

| Denúncias nos logs de 10.000h | Jogador Dovha | Espectador Dovha | Mundo Mira |
| --- | --- | --- | --- |
| Total | 108 | 135 | 94 |
| Destinatário igual ao ator do crime | 12 | 23 | 7 |
| Fonte recuperada do conhecimento antes da ação | 2 | 3 | 3 |
| Fonte ainda não identificada | 0 | 0 | 0 |

São **42/337 = 12,46%** das denúncias. Oito fatos de origem não estavam no fluxo narrativo iniciado no turno 24; recuperei todos nas capturas de conhecimento antes das ações. Não restou fonte desconhecida nessa classificação.

Exemplo: **Elena Vale 1595**, jogador, conhece o crime **879781**, cometido pelo guarda **Aldren Douran 1597** no turno **5406**. No **5428**, `InformationShared 883259` e `ThreatReported 883260` têm destinatário **1597**. A necessidade é de vingança/reparação e a evidência estava conhecida com confiança 100. A microreprodução confirmou candidatura, execução aceita e necessidade satisfeita na mesma configuração causal.

**Causa direta confirmada:** ausência da exclusão do suspeito na candidatura e ausência de validação independente na execução. A escassez de autoridades alternativas pode tornar a denúncia impossível após a correção; isso deve aparecer como bloqueio legítimo, não ser escondido com NPC novo ou autoridade automática.

## 4. Bug social: informação velha e inútil

### 4.1 O pedido filtra o assunto, mas não a utilidade temporal

O executor de `ask_personal_help` procura no conhecimento do interlocutor fatos sobre a pessoa-alvo, em alguns tipos, e escolhe o maior par `(turno, confiança)`. **Ser o mais recente do interlocutor não significa ser mais recente que o conhecimento do solicitante.**

Não verifica se o fato ocorreu depois da última observação, depois da ausência atual, se já é conhecido com confiança igual/melhor ou se pode alterar a localização considerada na busca.

Fonte: [seleção da informação](</home/hugo/Área de trabalho/procedrual/procedural/personal_actions.py:188>).

### 4.2 Transmissão é marcada como sucesso mesmo sem aprendizado

`KnowledgeSystem.learn` retorna falso quando o destinatário já conhece o fato com confiança igual ou maior. O método `inform` ignora esse retorno: ainda emite `InformationShared`, chama o tratamento de quests e retorna “Informação transmitida”.

O laço de decisão não vê falha, então não aplica o cooldown que ocorreria após uma tentativa inválida. O NPC pode escolher novamente pedir ajuda ao mesmo interlocutor. O registro persistente de reputação evita reaplicar o mesmo favor, mas não impede tempo gasto e narrativa repetida.

Fontes: [retorno falso de aprendizado repetido](</home/hugo/Área de trabalho/procedrual/procedural/knowledge.py:19>), [retorno da transmissão](</home/hugo/Área de trabalho/procedrual/procedural/personal_actions.py:76>) e [tentativas de pedir ajuda](</home/hugo/Área de trabalho/procedrual/procedural/personal_actions.py:70>).

### 4.3 O encerramento da busca exige evidência que a transmissão não exige

O consumidor de fatos familiares só usa `PersonLocated` para atualizar uma busca se o evento tem localização e turno igual ou posterior ao `created_at` da necessidade. A seleção da resposta não aplica essa mesma condição.

Consequentemente, a mensagem é entregue com sucesso, mas não possui condição para fechar a busca. No caso confirmado, já conhecer o fato impede até novo callback de aprendizado. Há uma inconsistência entre **seleção**, **resultado da comunicação** e **efeito na necessidade**.

As quests de informação já têm uma checagem temporal para `PersonLocated`; o pedido autônomo pessoal não compartilha uma avaliação equivalente de utilidade. Isso indica uma regra local reutilizável, não necessidade de novo planejador.

Fontes: [consumo de localização pela necessidade familiar](</home/hugo/Área de trabalho/procedrual/procedural/personal.py:94>) e [checagem temporal em quest](</home/hugo/Área de trabalho/procedrual/procedural/quests.py:89>).

### 4.4 O caso Arthus–Iria–Marie

**Arthus Luar 41**, cozinheiro; **Iria Luar 38**, agricultor; casamento 94. **Marie Stone 44**, guarda, é o interlocutor.

Arthus localizou Iria no turno **328**, fato **63306**. A última observação seguinte é **364**. No **400**, percebe nova ausência, evento **77503**. Busca no **405**, evento **78420**, sem encontrar Iria.

Nos turnos **406, 407, 418 e 419**, Marie transmite quatro vezes o fato **63306**. A informação é anterior à última observação e à ausência. Arthus já conhece esse fato com confiança 100 antes dos pedidos, portanto a retransmissão limitada pela confiabilidade da fonte não melhora esse conhecimento. As quatro ações retornam sucesso, mas a busca ainda está ativa no registro do turno 419.

Na varredura completa, houve **22/87/234 pedidos de informação** no contexto específico de busca familiar. Somente quatro tiveram execução bem-sucedida com transmissão de localização: justamente essas quatro repetições, na campanha jogador. Não encontrei outra transmissão de localização bem-sucedida desse tipo nos outros dois modos. Isso limita a frequência comprovada do bug; não significa que todas as informações compartilhadas do jogo sejam inúteis.

A microreprodução confirmou: fato do turno 30, última observação 70, necessidade criada no 100, fato já conhecido. O aprendizado retorna falso; a execução retorna sucesso; a necessidade permanece ativa.

**Causa direta confirmada:** falta de filtro de relevância temporal/novidade, retorno de aprendizado ignorado e ausência de prevenção de repetição bem-sucedida nominalmente. Não é simplesmente “memória curta”, nem exige aumentar o limite de memória para resolver.

## 5. Correções possíveis, motivos e efeitos esperados

As propostas abaixo são para sua análise. Nenhuma foi aplicada nesta investigação. “Efeito esperado” é hipótese de projeto; precisará de novas regressões e campanhas após implementação.

### Reserva: relacionar prioridade à cobertura e à próxima oportunidade

Priorizar pelo tempo de cobertura disponível e pelo tempo da próxima reposição viável, com limite moderado enquanto não houver risco imediato. Isso atacaria a janela preventiva perdida; um aumento constante de peso poderia só deslocar o problema para descanso, família ou trabalho.

Considerar reposição em lote pequeno **até o déficit e o orçamento real**, especialmente quando já há mercado acessível. O preço do lote precisa percorrer a curva real de unidades; não multiplicar cegamente a cotação unitária. Se só há dinheiro para uma ração, uma continua sendo resultado legítimo.

Separar “não precisa comer agora” de “precisa financiar a segunda ração”. O trabalho para reserva deveria avaliar déficit e custo de reposição, preservando renda normal, profissão compatível, conhecimento e prazo. Isso corrige a lacuna reproduzida sem tornar toda pessoa com uma ração automaticamente prioritária.

Manter a continuidade de objetivos, mas avaliar sua interação com cobertura baixa e oportunidade curta. Os 11 vetos medidos não justificam remover a margem de continuidade de todos os objetivos. Primeiro corrigir prioridade, reposição parcial e alternativas.

### Acesso econômico: tornar executável a oportunidade local

Refletir quota restante e condições reais na oferta local de trabalho temporário. Revalidar no instante da execução, porque outros trabalhadores podem esgotar a demanda. A observação conhecida deve carregar a idade do anúncio, evitando conhecimento global perfeito.

Tratar separadamente trabalho sem produção, trabalho produtivo com crédito parcial e pagamento efetivamente impossível. Crédito fracionário legítimo deve participar da projeção de renda; um saldo ainda abaixo de uma moeda não deveria automaticamente punir a ação como trabalho inútil. Não pagar uma moeda inteira antecipada sem fonte nem duplicar crédito e dinheiro.

Para produtores saturados, aproveitar tarefas compatíveis já existentes que consumam recursos locais ou prestem serviço real. Se for preciso remunerar em alimento, debitar estoque real e registrar a produção/pagamento corretamente. A tarefa deve ter demanda/custo e limite, sem virar salário ou comida ilimitados.

Manter limites para estudantes, governantes e guardas, mas verificar se há renda remunerada compatível e alcançável. Não usar formação compulsória ou migração como solução imediata. Nos quartéis, bloquear melhor intenção incompatível e registrar ausência de economia local, preservando a proibição de acesso remoto ao caixa da cidade natal.

Se após corrigir as oportunidades ainda faltar acesso, avaliar políticas locais de compra/serviço com orçamento explícito do município. O caixa já existente pode financiar trabalho ou uma ajuda definida por regra, mas a mudança teria custos, critérios e registro de transferência. Este diagnóstico não demonstra qual política é a melhor nem autoriza inventar demanda fictícia apenas para pagar pessoas.

### Denúncia: destinatário adequado nas duas etapas

Excluir, na candidatura, o ator acusado na evidência conhecida, a ameaça/culpado da necessidade e o próprio denunciante quando incompatível. Repetir a validação na execução; observações podem estar antigas e o alvo pode mudar de estado.

Quando só existe o guarda suspeito, conservar a necessidade bloqueada e permitir outras alternativas legítimas de informação/evitação. Uma conversa com o suspeito pode ser futura ação distinta, mas não deve fechar “denúncia independente” só por transmitir a acusação a ele.

### Informação: utilidade antes de resposta e efeito após aprendizado

Definir uma pequena avaliação compartilhada de relevância: assunto correto, localização aplicável, novidade, confiança e efeito possível sobre a necessidade atual. Para localização em ausência, comparar com última observação e início do episódio atual; não aplicar indiscriminadamente esse corte a uma morte antiga que a pessoa ainda desconhece.

O interlocutor deve selecionar resposta útil a partir do próprio conhecimento, após receber a pergunta/contexto necessário. A escolha de quem perguntar não deve consultar magicamente a memória privada de todos os NPCs.

Separar resultados como **informação nova útil**, **confiança melhorada**, **fato já conhecido**, **fato antigo sem avanço** e **nenhuma informação**. Só os resultados úteis deveriam ser tratados como progresso daquela busca. Repetir comunicação pode continuar permitido em contextos apropriados, com mensagem honesta e sem loop automático de sucesso.

Guardar tentativas recentes por necessidade/interlocutor/fato ou aplicar espera quando não houver novidade. O limite deve ser pequeno e persistente; não gerar uma memória infinita. Atualização genuína de notícia ou confiança deve poder reabrir a oportunidade.

## 6. Ordem de trabalho sugerida e como verificar

| Ordem | Alteração possível | Por que vem antes | Evidência a exigir depois |
| --- | --- | --- | --- |
| 1 | Validar destinatário da denúncia na candidatura e execução | Bug local confirmado, efeito social falso imediato | Zero denúncias ao próprio suspeito; necessidade permanece bloqueada se não houver autoridade válida |
| 2 | Avaliar utilidade/novidade da informação e resultado do aprendizado | Bug local confirmado, repetição sem avanço | Fato velho já conhecido não fecha busca nem gera loop; notícia nova ou confiança melhorada ainda funciona |
| 3 | Corrigir lacuna da segunda ração e resultado do pagamento fracionário | Dois mecanismos reproduzidos sem depender de rebalanceamento amplo | Trabalho possível com uma ração e déficit; crédito proporcional conservado; nenhuma remuneração duplicada |
| 4 | Tornar ofertas temporárias compatíveis com quota e recursos | Oferta pode anunciar execução impossível | Concorrência pode esgotar oferta; falha distingue quota, insumo e estoque; transferências continuam reais |
| 5 | Ajustar prevenção por cobertura/oportunidade e completar reposição limitada | Principal causa quantitativa da baixa prevenção | Mais reposição antes de fome alta, sem eliminar descanso, renda ou vida pessoal; nada de estoque infinito |
| 6 | Reavaliar renda local para ocupações sem trabalho executável | Restrição econômica exige decisões de design | Recursos e dinheiro conservados; trabalho real compatível; nenhum acesso remoto ou formação forçada |

Depois dessas mudanças, repetir as mesmas três campanhas de 10.000 horas com regras congeladas por rodada, preservando estes resultados como diagnóstico anterior. Comparar dinheiro/produção/estoque, cobertura, início de busca, horários de oportunidade, mortalidade e variedade de histórias.

Os critérios principais não devem ser uma meta artificial de mortes ou toda reserva sempre vencer. Devem ser: **não perder repetidamente uma reposição viável por desenho de prioridade; não tratar trabalho remunerado parcial como inútil; não oferecer sistematicamente serviço já esgotado; não satisfazer denúncia por destinatário inadequado; não chamar informação repetida de avanço narrativo**.

## 7. O que está confirmado e o que ainda exige decisão

**Confirmado:** teto da prioridade; predomínio de descanso/sede nas janelas preventivas; perda com recursos disponíveis em muitos instantes; lacuna de alternativas com uma ração; saturação e quota como restrições de renda; fração salarial tratada como falha; dois bugs sociais, suas origens no código e exemplos reproduzidos.

**Não confirmado como causa predominante:** continuidade dos objetivos, inadimplência de caixa ou necessidade de gerar mais moeda. Os dados medidos dão peso menor a essas hipóteses. Não atribuí todas as falhas de produção a saturação nem todas as mortes a uma causa econômica única.

**Ainda exige projeto e experimento:** melhor curva de prioridade preventiva, tamanho e duração de compra em lote, amplitude de tarefas remuneradas, tratamento de crédito parcial, critérios locais de assistência e equilíbrio com histórias pessoais. Não tenho evidência para recomendar um número mágico de prioridade ou salário.

Minha avaliação é que vale realizar essa etapa antes de uma fase ampla: há correções locais claras, e o diagnóstico da reserva revela um problema de ordenação/oportunidade que sistemas maiores poderiam esconder. O acesso econômico deve melhorar por caminhos reais para recursos existentes; a evidência não justifica simplesmente criar mais comida ou dinheiro.

## Arquivos e reprodução

- [Relatório anterior da correção alimentar](</home/hugo/Área de trabalho/procedrual/RELATORIO_CORRECAO_ALIMENTAR.md>).
- [Censo econômico e social, com exemplos](</home/hugo/Área de trabalho/procedrual/reports/fase_3_2_diagnostico/censo_economico_e_social.json>).
- [Cinco microdiagnósticos](</home/hugo/Área de trabalho/procedrual/reports/fase_3_2_diagnostico/microdiagnosticos.json>).
- [Dados de decisão jogador](</home/hugo/Área de trabalho/procedrual/reports/fase_3_2_diagnostico/jogador_replay.json>), [espectador](</home/hugo/Área de trabalho/procedrual/reports/fase_3_2_diagnostico/espectador_replay.json>) e [mundo](</home/hugo/Área de trabalho/procedrual/reports/fase_3_2_diagnostico/mundo_replay.json>).
- [Exemplos completos jogador](</home/hugo/Área de trabalho/procedrual/reports/fase_3_2_diagnostico/jogador_amostras.jsonl.gz>), [espectador](</home/hugo/Área de trabalho/procedrual/reports/fase_3_2_diagnostico/espectador_amostras.jsonl.gz>) e [mundo](</home/hugo/Área de trabalho/procedrual/reports/fase_3_2_diagnostico/mundo_amostras.jsonl.gz>).

Scripts de observação e laboratório:

```bash
python3 -m experiments.phase32_diagnostic_replay --mode jogador
python3 -m experiments.phase32_diagnostic_replay --mode espectador
python3 -m experiments.phase32_diagnostic_replay --mode mundo
python3 -m experiments.phase32_static_diagnosis
python3 -m experiments.phase32_micro_diagnosis
python3 -m experiments.phase32_diagnostic_report
```

Esses scripts geram os artefatos de diagnóstico desta etapa. Os saves canônicos, regras e relatórios de campanhas anteriores ficam preservados. A reprodução recusa motor diferente do manifesto usado; os checkpoints comprovam que a instrumentação não alterou a campanha.
