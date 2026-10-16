# Por que a sobrevivência ainda domina as histórias

Análise do MVP de fase 2 — 7 de outubro de 2026.

**Conclusão:** há histórias pessoais funcionando, mas a economia e a rotina dos NPCs ainda não sustentam tempo, recursos e oportunidades suficientes para que elas tenham continuidade. O problema combina conversão de alimentos, acesso à renda, capacidade profissional, deslocamento e alternativas pessoais limitadas. Reposição profissional pode ajudar bastante, mas não resolve sozinha.

Este trabalho analisa código e os saves existentes. Não altera regras, população, profissões ou campanhas e não executa novas campanhas de 10.000 turnos. As mudanças que você pretende fazer na população abstrata continuam pendentes.

## 1. Evidências e limites da análise

Foram examinados os três modos já testados, com 10.000 horas de simulação após a preparação inicial de 24 horas. Esta análise também releu os checkpoints de 1.000 e 5.000 horas de cada campanha: nove saves ao todo.

Fontes reproduzíveis:

- [Relatório das três perspectivas](</home/hugo/Área de trabalho/procedrual/reports/tres_perspectivas_20261007/RELATORIO.md>), com métodos, histórias e limites dos testes.
- [Comparativo das campanhas](</home/hugo/Área de trabalho/procedrual/reports/tres_perspectivas_20261007/comparativo.json>), com seleções de necessidades e eventos.
- [Evidências deste diagnóstico](</home/hugo/Área de trabalho/procedrual/reports/analise_abastecimento/evidencias.json>), com estoques, dinheiro, profissões e preços por cidade nos nove saves.
- [Script de extração](</home/hugo/Área de trabalho/procedrual/experiments/supply_analysis.py>), executável com `python3 experiments/supply_analysis.py` na pasta do projeto.

Neste relatório, **observação** significa algo encontrado nos saves; **mecanismo confirmado** significa uma regra presente no código; **hipótese** significa uma explicação causal que ainda precisa de comparação controlada. Um estoque vazio em um checkpoint não prova que ficou vazio o dia inteiro. Cozinheiro vivo não significa cozinheiro trabalhando, presente na cozinha ou com tempo disponível.

### Resultado ao final das campanhas

| Indicador | Jogador — Dovha | Espectador — Dovha | Mundo — Mira |
| --- | ---: | ---: | ---: |
| NPCs vivos | 317 | 311 | 302 |
| NPCs mortos | 139 | 145 | 138 |
| Cidades e vilas | 79 | 79 | 76 |
| Mercados sem comida pronta | 26 | 31 | 31 |
| Desses mercados: trigo no limite de 240 | 26 | 31 | 30 |
| Desses mercados: cozinheiro vivo | 11 | 17 | 15 |
| Desses mercados: nenhum cozinheiro vivo | 15 | 14 | 16 |
| Localidades com ≥100 rações e algum residente sem dinheiro para comprar uma | 16 | 23 | 18 |
| NPCs vivos com menos de 10 moedas | 171 | 176 | 152 |
| NPCs vivos com fome ou sede ≥70 | 164 | 144 | 174 |
| Seleções de necessidades fisiológicas | 91,63% | 91,80% | 92,48% |

“Fisiológicas” reúne **fome, sede e descanso**. Essas porcentagens são seleções de necessidades pelo motor; não representam porcentagem de histórias sobre comida, ações concluídas ou tempo gasto. NPCs críticos decidem com maior frequência, o que também influencia a distribuição.

Há uma medida mais direta do conteúdo oferecido ao jogador: **43 das 49 quests eram de comida**, aproximadamente 87,8%. Cinco eram familiares e uma de companhia. É um resultado desta campanha e desta política de jogador, não uma taxa garantida para qualquer partida.

Os testes anteriores passaram pelas verificações de invariantes, contabilidade monetária, salvamento e continuação determinística. Isso sustenta a estabilidade técnica observada; não demonstra equilíbrio econômico ou variedade narrativa suficiente.

## 2. O problema não começou somente depois das mortes

No checkpoint de 1.000 horas, já havia 19 mercados vazios com cozinheiro vivo na campanha do jogador, 18 no espectador e 19 no mundo. Portanto, a perda de profissionais agrava o problema, mas não explica todo o início dele.

No modo jogador, as mortes acumuladas passaram de 89 em 1.000 horas para 136 em 5.000 e 139 em 10.000. No espectador: 101, 140 e 145. No mundo: 98, 135 e 138. Grande parte da perda do elenco ocorreu cedo; depois, o mundo continuou com menos personagens e com problemas persistentes de abastecimento.

Isso importa para o projeto: testar só o estado final pode esconder a fase em que o sistema perdeu capacidade. Também seria errado afirmar que todo NPC morrerá inevitavelmente: centenas continuaram vivos por 10.000 horas.

## 3. Causas e motivos

### 3.1. A resposta coletiva trata falta de comida como falta de plantio

**Mecanismo confirmado:** quando a população abstrata não compra a quantidade diária de comida, a cidade cria o objetivo `expand_farming`. Sua ação produz trigo, limitada por trabalhadores abstratos, dinheiro e espaço no estoque. O reino, por sua vez, oferece financiamento agrícola. Não existe uma escolha coletiva entre plantar, cozinhar, contratar ou transportar conforme o gargalo.

Veja [economy.py](</home/hugo/Área de trabalho/procedrual/procedural/economy.py:100>).

**Observação:** quase todos os mercados vazios finais têm 240 unidades de trigo. A matéria-prima está presente, mas comida pronta está ausente. Quando o trigo chega ao teto, a resposta agrícola deixa de produzir, e não há outra resposta coletiva para converter o estoque.

**Por que isso importa:** plantar mais não resolve falta de preparo. A cidade pode reconhecer corretamente a escassez e executar uma ação inadequada para sua causa. Isso mantém a mesma pressão voltando sem abrir uma solução diferente.

### 3.2. Profissões podem perder renda mesmo em cidades abastecidas

**Mecanismo confirmado:** agricultores, mineiros, lenhadores, caçadores e ferreiros recebem salário depois de produzir. Se o estoque está cheio ou falta insumo, o trabalho falha antes do pagamento. Guardas e outros prestadores de serviço seguem outra lógica e podem receber por serviço.

Veja [professions.py](</home/hugo/Área de trabalho/procedrual/procedural/professions.py:26>).

**Exemplo atual:** no save do jogador, Dorlen, ID 50, tem 231 rações, 240 unidades de trigo e 3.997 moedas na cidade. Elena Alvor, ID 56, agricultora, tem uma moeda, fome 64 e nenhuma ração; o preço de uma ração é duas moedas.

Ela está numa localidade com comida e dinheiro, mas seu trabalho habitual encontra um estoque de trigo cheio. O snapshot não reconstrói todas as decisões anteriores dela; a regra confirma que produzir mais trigo ali não fornece salário enquanto o estoque permanecer no teto.

**Por que isso importa:** excesso de matéria-prima pode eliminar a renda de quem a produz. O problema passa a ser acesso individual à comida, além da quantidade total disponível. Nos nove checkpoints analisados, nenhuma cidade tinha caixa zerado; isso não exclui falta de caixa em outros momentos, mas impede tratar falência municipal generalizada como explicação desses estados.

### 3.3. Uma alternativa financeira para fome ainda usa um limite fixo

**Mecanismo confirmado:** a viabilidade da compra usa preço observável no mercado. Entretanto, a alternativa de trabalhar para resolver fome só é oferecida a profissionais quando têm **menos de cinco moedas**. O trabalho rural pago em comida só aparece nesse ramo para personagens sem profissão; estudantes também ficam fora dele.

Veja [goals.py](</home/hugo/Área de trabalho/procedrual/procedural/goals.py:32>).

**Exemplo:** Elivia, ID 162, termina a campanha do jogador com zero comida e 240 de trigo. Seu cozinheiro Arthus Solaris, ID 171, está vivo, tem 12 moedas e nenhuma ração. O preço calculado naquele mercado vazio é 14 moedas; não é uma oferta comprável, pois não há estoque. Mesmo assim, 12 moedas já impedem a alternativa financeira de trabalho dentro da necessidade de fome. Trabalho ainda pode aparecer por outra necessidade, mas terá de vencer a competição de prioridades.

**Por que isso importa:** “tem cinco moedas” não significa “tem meios de se alimentar”. Esse limite merece revisão com base no custo conhecido e nas alternativas reais. A solução deve respeitar informação local: um NPC longe do mercado não deve conhecer automaticamente o estoque e o preço atuais.

### 3.4. Capacidade profissional não acompanha a escala da população

**Mecanismo confirmado:** na configuração padrão, cada cidade recebe oito profissionais, um de cada profissão básica; cada vila recebe agricultor, cozinheiro, guarda e caçador. As capitais acrescentam a família governante. A população nominal varia bastante, mas a quantidade inicial desses profissionais não é calculada pela demanda local. Os estoques iniciais de comida e trigo também são iguais entre localidades.

Veja [generation.py](</home/hugo/Área de trabalho/procedrual/procedural/generation.py:138>) e [distribuição dos profissionais](</home/hugo/Área de trabalho/procedrual/procedural/generation.py:199>).

A população abstrata consome diariamente `ceil(população_abstrata / 120)` unidades do mesmo estoque de comida. Existe renda abstrata diária e colheita coletiva de trigo quando falta alimento, mas não uma cadeia abstrata completa de preparo e abastecimento.

**Por que isso importa:** a demanda cresce com a população, enquanto a capacidade concreta depende de poucos personagens e das horas em que conseguem trabalhar. Uma capital pode depender do mesmo número de cozinheiros de uma vila. Produção, consumo e escala precisam representar o mesmo modelo econômico.

A expressão “lotes diários” aparece na economia, mas o consumo retira o mesmo tipo de item que um NPC individual come. É necessário documentar a equivalência agregada antes de recalibrar população e produção. Não seria correto aplicar consumo individual integral a milhares de habitantes mantendo a produção atual.

### 3.5. A morte pode retirar uma função essencial permanentemente

**Ausência confirmada:** não há reposição profissional por demanda a partir da população abstrata. Quando um cozinheiro morre, suas relações e consequências permanecem, mas não surge um novo trabalhador para assumir a função.

**Observação:** entre 14 e 16 mercados vazios finais, conforme o modo, não têm cozinheiro vivo. Isso é um grupo relevante, embora outros mercados estejam vazios com cozinheiro vivo.

**Por que isso importa:** uma morte narrativa também pode virar perda permanente de infraestrutura econômica. Sem recuperação, a cidade continua pressionando os sobreviventes, que passam a ter menos condições de desenvolver outras histórias.

Reposição deve recuperar a função, mantendo a morte do personagem. Não deve copiar nome, família, memórias ou relações do falecido, nem tratar reis, líderes e personagens importantes como vagas comuns intercambiáveis.

### 3.6. Sobreviver exige deslocamento e ações distintas

**Mecanismo confirmado:** fome e sede crescem por hora; deslocamento consome tempo antes de executar a ação. Comprar, comer, beber, trabalhar e descansar competem com procurar um familiar ou investigar uma ameaça. NPCs comuns normalmente decidem em intervalos de seis horas; os críticos passam a decidir a cada hora. A fisiologia continua em todas as horas.

Veja [engine.py](</home/hugo/Área de trabalho/procedrual/procedural/engine.py:65>) e [goals.py](</home/hugo/Área de trabalho/procedrual/procedural/goals.py:156>).

Só a fome cresce 48 pontos por dia; uma ração reduz 40. Em longo prazo, sem desperdício por redução até zero, isso equivale a pelo menos 1,2 rações por dia para um NPC ativo na simulação. Adquirir cada ração e chegar aos recursos adiciona custo ao ato de comer.

**Hipótese a testar:** distância, repetição de tentativas e frequência das decisões podem manter trabalhadores em sobrevivência quase contínua, inclusive onde há recursos. O número de seleções não mede esse custo adequadamente; precisamos de ações concluídas, horas de viagem e produção efetiva.

### 3.7. Sede também precisa entrar no diagnóstico

Os saves finais têm 25 mortos carregando comida no jogador, 25 no espectador e 16 no mundo. Nenhum morto carrega água. Isso não identifica a causa individual de cada morte, pois a privação pode ser por fome ou sede e comer exige uma ação.

Os NPCs já podem beber em poços conhecidos; não está faltando toda a funcionalidade de água. Mas as alternativas autônomas de sede não incluem compra e preparação de uma reserva de água para viagem. Há cidades com estoque de água e indivíduos com sede alta.

**Por que isso importa:** melhorar comida pode deixar o segundo gargalo intacto. Devemos rastrear a condição no momento da morte e o caminho até a fonte, evitando atribuir toda privação à fome.

### 3.8. As histórias pessoais ainda têm poucas formas de prosseguir

A fase 2 já produz busca familiar, comunicação, luto, proteção e investigação. Há uma sequência verificável em que Bela recebe notícias dos restos do pai e depois pede companhia. No modo mundo, Lyra Ferros cumpre uma responsabilidade para buscar reconhecimento; o acontecimento é depois conhecido por outros NPCs.

Mas milhares de preocupações familiares não equivalem a milhares de histórias independentes: muitas respondem à mesma privação recorrente. Status depende de encontro com uma referência reconhecida, e ascensão atualmente busca aumentar a reserva financeira. Não existem carreiras completas, disputas políticas executáveis, religião organizada ou guerras com exércitos.

**Por que isso importa:** estabilizar a sobrevivência pode abrir espaço para as histórias existentes, mas não acrescenta automaticamente caminhos que ainda faltam. A variedade também depende de gatilhos, oportunidades conhecidas, alternativas executáveis e continuidade depois de cada ação.

## 4. O que já existe e o que falta

| Funcionalidade | Estado atual | Impacto esperado de completar |
| --- | --- | --- |
| Trabalho avulso por alimento | Existe na área rural; converte trigo e paga uma ração física. A escolha autônoma é restrita. | Ampliar elegibilidade pode aproveitar trabalhadores ociosos e reduzir barreira monetária. |
| Produção e consumo abstratos | Parciais: consumo, renda e mobilização de trigo. | Cadeia produtiva coerente pode sustentar a demanda sem depender de um único NPC materializado. |
| Reposição profissional | Ausente. | Recuperar funções essenciais após perda de trabalhador. |
| Trabalho conforme demanda | Parcial; estoque limita produção, mas não há rede ampla de tarefas alternativas remuneradas. | Evitar que estoque cheio prenda alguém sem renda quando outra tarefa é necessária. |
| Diagnóstico coletivo do gargalo | Parcial; falta de comida leva à expansão agrícola. | Escolher preparo, contratação, plantio ou importação conforme a causa conhecida. |
| Transporte comercial entre cidades | Ausente. | Levar excedentes a déficits, com custo, prazo e capacidade reais. |
| Sobrevivência preventiva | Há locais conhecidos e poços; preparação autônoma de reservas é limitada. | Reduzir idas e tentativas repetidas, sobretudo em viagens pessoais. |
| Objetivos pessoais | Implementados na fase 2, com alternativas ainda limitadas. | Criar continuidade além de cuidado por privação e acumulação financeira. |

Os impactos são expectativas fundamentadas nos mecanismos encontrados. Ainda não foram medidos por testes comparativos com essas funcionalidades implementadas.

## 5. Sugestões de solução e por que adotá-las

### A. Definir a contabilidade da população antes de ampliar produção

Na revisão que você pretende fazer, definir explicitamente população total viva, abstrata e materializada; como mortes alteram esses números; e o que significa uma unidade agregada de consumo e produção.

Hoje a fórmula subtrai `len(resident_ids)`, que inclui mortos e pode incluir residentes atualmente em outro mapa. Não é um registro independente de população abstrata viva. Materializar um trabalhador deve transferir uma pessoa e sua capacidade entre representações, evitando contar sua produção duas vezes.

**Motivo:** sem essa definição, uma correção pode tanto duplicar trabalhadores quanto criar demanda impossível. A produção abstrata deverá consumir tempo, insumos e capacidade de estruturas; não ser uma reposição gratuita de comida.

### B. Fazer a cidade responder ao gargalo correto

Manter necessidade, objetivos e ações do motor existente, acrescentando alternativas: plantar quando falta trigo, preparar quando há trigo e falta comida, contratar quando falta capacidade, e buscar abastecimento externo quando há fonte conhecida e transporte disponível.

**Motivo:** é a ligação mais direta entre o diagnóstico observado e uma ação útil. O estoque cheio de trigo deixa de bloquear a única resposta disponível. É possível começar com respostas locais, antes de implementar caravanas.

### C. Ampliar trabalho temporário e remuneração por necessidade real

Aproveitar o trabalho avulso já existente para permitir tarefas compatíveis a profissionais temporariamente ociosos. Um agricultor com estoque cheio poderia ajudar no preparo, recebendo pagamento real em dinheiro ou comida. Competência, local, duração e capacidade devem limitar a tarefa; estudantes não precisam virar automaticamente profissionais de qualquer ofício.

Rever também a condição fixa de cinco moedas: o NPC deve considerar se consegue obter alimento pelas opções que conhece. Não basta aumentar esse número para outro limite arbitrário.

**Motivo:** atende aos dois lados do problema: matéria-prima sem conversão e indivíduo sem acesso. Salário deve sair de um pagador e produção deve consumir insumos; pagar infinitamente por produzir bens sem demanda apenas deslocaria o desequilíbrio.

### D. Implementar reposição profissional seletiva

Quando existir estrutura, vaga, demanda persistente e população abstrata disponível, contratar ou materializar um novo trabalhador comum após um prazo. Exigir condições mínimas de sobrevivência e meios de pagamento. Usar demanda e capacidade para determinar vagas, em vez de fixar o mesmo elenco em toda cidade.

**Motivo:** evita que uma morte encerre permanentemente o preparo de alimentos. O limite é importante: contratar outro cozinheiro numa cidade onde os cozinheiros vivos não conseguem trabalhar pode repetir a falha. Demanda persistente não autoriza criação infinita de NPCs.

### E. Planejar sobrevivência com informação local

Avaliar reserva de comida e água antes de uma viagem conhecida; manter memória de preço, estoque e fonte com validade; escolher trajetos e abastecimento possíveis antes de alcançar o estado crítico. Compartilhamento familiar e refeições coletivas podem ampliar o cuidado existente, usando itens reais e decisões dos participantes.

**Motivo:** reduz o custo repetitivo de sobrevivência e permite concluir uma busca pessoal. Não exige tornar a fome inofensiva nem dar conhecimento global aos NPCs. A frequência de decisão deve ser verificada para garantir que o intervalo não faça o personagem perder oportunidades de agir.

### F. Dimensionar reservas por cobertura e capacidade

Medir quantos dias o estoque atende à demanda prevista e quanto os trabalhadores realmente conseguem produzir. Reservas e estruturas podem variar por tamanho e função da localidade, conforme o modelo de população escolhido.

**Motivo:** um teto igual de 240 unidades não descreve a mesma cobertura para vila e capital. Aumentar o teto, sozinho, apenas permite guardar mais; não produz, distribui ou paga alimento.

### G. Acrescentar transporte depois de existir uma economia local coerente

Criar comércio com oferta conhecida, contrato, estoque reservado, transportador, carga e tempo de viagem. O destino só recebe quando a carga chega. Dinheiro muda de dono; não aparece automaticamente pela operação.

**Motivo:** os saves têm localidades com excedente ao lado de um mundo com mercados vazios. Transporte pode conectar esses estados e gerar histórias de cooperação e conflito. Mas exige mais sistemas e não resolve pobreza individual nem falta de preparo no destino.

### H. Ampliar oportunidades pessoais após medir a folga criada

Com sobrevivência mais estável, avaliar se as necessidades pessoais passam a executar e concluir mais ações. Depois, acrescentar compromissos e consequências: ajuda entre familiares, dívida social, responsabilidade pública, disputa por função, proteção concreta e prática religiosa local, conforme o próximo escopo autorizado.

**Motivo:** essas ações podem gerar causas próprias, sem depender sempre de comida. Não basta subir a prioridade de ambição: sem uma ação realizável ou um encontro conhecido, a necessidade continua abstrata.

## 6. Ordem recomendada

1. **Fechar seu desenho de população abstrata e das unidades econômicas.** É a base das capacidades e da reposição.
2. **Corrigir respostas locais e acesso ao trabalho.** Diferenciar trigo de comida pronta e renda de estoque; aproveitar o trabalho avulso existente.
3. **Implementar capacidade e reposição profissional por demanda.** Preservar identidade, mortes e limites populacionais.
4. **Medir deslocamento, água e preparação para viagens.** Ajustar alternativas onde houver falhas concretas, preservando perigo e conhecimento local.
5. **Adicionar transporte e novas oportunidades pessoais.** Ampliar alcance e continuidade sobre uma economia capaz de sustentá-los.

Durante todas as etapas, manter a cadeia necessidade → objetivo → alternativas → ação → consequência. Não é necessário criar um motor paralelo para contar histórias.

## 7. Como verificar se resolveu

Comparar cada mudança com a versão anterior partindo do **mesmo estado inicial e estado aleatório**, com uma política de jogador definida, e repetir em outras seeds, com e sem jogador. A versão das regras participa da geração: comparar apenas o mesmo nome de seed entre versões pode comparar mundos diferentes. Se uma mudança exigir migração, o procedimento de comparação precisa documentar essa diferença.

Medir, além da porcentagem de seleção:

- Horas sem comida pronta, cobertura de estoque e quantidade produzida por profissão.
- Vagas essenciais, prazo de reposição e consumo/produção antes e depois da materialização.
- NPCs sem acesso à comida por preço, estoque, distância ou falta de alternativa de renda.
- Mortes com estado fisiológico, inventário, destino e últimas tentativas registrados.
- Horas de viagem, tentativas repetidas e ações realmente concluídas.
- Necessidades pessoais criadas, executadas, concluídas e expiradas; separar cuidado por privação de outros motivos.
- Cadeias de acontecimentos com consequência posterior, participantes e informação transmitida; evitar contar cada evento como uma história independente.

Casos dirigidos úteis: trigo cheio/comida vazia; estoque cheio/trabalhador pobre; cozinheiro morto; cozinheiro vivo sem tempo para produzir; cidade com demanda alta; NPC com dinheiro insuficiente acima do limite de cinco; água disponível com acesso difícil; família capaz de viajar e concluir uma busca.

Continuar verificando itens, dinheiro, população, IDs, persistência e determinismo. Sucesso econômico não deve vir de recursos duplicados, salários sem pagador ou substituição de personagens importantes.

**Critério de melhora:** menos privações evitáveis e mais ações pessoais viáveis e encadeadas, mantendo escassez, escolhas difíceis e consequências. Não há evidência para prometer que uma única funcionalidade atingirá uma porcentagem específica de histórias pessoais. Também não é desejável impor uma quota artificial de ações para esconder o problema.

## 8. Avaliação final

O MVP já serve para testar a cadeia de comportamento e revela consequências pessoais reais. As campanhas mostram, porém, que a sustentabilidade econômica e a continuidade narrativa ainda precisam avançar.

Minha recomendação é combinar **população coerente, diagnóstico do gargalo, trabalho temporário e recuperação das funções essenciais**. Essa combinação responde a causas distintas comprovadas no código e presentes nos saves. Reposição isolada, mais plantio isolado ou redução artificial da fome deixariam partes importantes do problema abertas.

Depois disso, verificar a mudança no comportamento antes de expandir conteúdo. A expectativa é que sobreviver consuma menos tentativas improdutivas e que os personagens possam agir mais sobre relações e projetos próprios. O tamanho dessa melhora permanece uma hipótese até os testes comparativos.
