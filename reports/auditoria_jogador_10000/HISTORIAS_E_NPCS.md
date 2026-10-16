# Histórias e comportamento dos NPCs — campanha Dovha

**Avaliação:** o save produziu boas situações para histórias, sobretudo Mira Corven, a relação com Marie Arven e a guarda Iria Douran. Os acontecimentos têm causas e consequências reconhecíveis. Entretanto, a maioria dos episódios repete fome, obtenção de comida e descanso. Os personagens apresentam diferenças de comportamento, mas ainda desenvolvem pouco seus vínculos, suas ambições e seus papéis políticos.

Análise do `save_final.json`, no turno **10.024**, após as **10.000 horas de ações do jogador Auditor**, iniciadas no turno 24. Foram usados o save, os checkpoints de 1.000 e 5.000 horas e o diário da auditoria. Nenhum turno adicional foi executado. Os títulos abaixo são editoriais; as sequências descritas vêm dos registros. Interpretações estão identificadas e não acrescentam acontecimentos.

Um ajuste ao relato anterior: o jogador visitou **Karmir, uma capital, e Dorven, uma vila**. Dorven aqui é o mapa 50; existem outros lugares com esse nome.

## 1. Mira Corven: a herdeira que pediu comida antes de assumir o reino

Este é o arco mais completo ligado diretamente ao jogador. Mira começa como uma estudante da família real, procura alimento, recebe ajuda, torna-se governante e morre pouco depois.

| Turno | Acontecimento comprovado |
| --- | --- |
| 80 | Ao conversar, Mira relata fome e busca de alimentos. Também conta ter visto Aldren Kars roubar no mercado de Karmir. |
| 81 | Auditor entrega uma ração; o evento registra urgência 47. |
| 145 | Darin Corven, integrante da família real, morre por privação. |
| 157 | Auditor entrega outra ração, desta vez com urgência social registrada como zero. |
| 247 | Mira pede comida ao jogador por iniciativa própria, criando a quest 36.857. |
| 273 | Auditor entrega comida e conclui o pedido; urgência registrada 71. |
| 309 | Dovha morre por privação. Mira assume o Reino Corven. |
| 373 | Mira morre por privação. A dinastia Corven se extingue. |

A conversa inicial é particularmente boa porque conecta a personagem a um problema local concreto: **“Eu vi: Aldren Kars roubou comida no mercado de Karmir.”** Ela participa do mesmo mundo de escassez e crimes dos habitantes comuns.

No último estado preservado de Mira, a confiança no jogador é **30**, com reputação **prestativo 38** e admiração **38**. O favor deixou uma marca social. A entrega de urgência zero também mostra que nem todo presente recebe o mesmo significado.

**Qualidade da história:** há encontro, necessidade, participação do jogador, mudança de posição e desfecho. A ajuda antecede a sucessão em 36 horas; o governo dura 64 horas. Isso permite uma história pessoal com relevância política, sem precisar inventar uma missão especial para uma princesa.

**Limite:** receber comida não prova que o jogador garantiu sua sobrevivência até a sucessão. A morte acontece com fome 90 e sede 100. Ao assumir o reino, Mira continua cadastrada como `estudante`; a sucessão altera quem governa, mas não gera uma nova rotina de governo. Não há registros de cerimônia, decisões próprias como governante, promessa ao jogador ou reação à morte dos familiares.

Evidências principais: eventos 13.087, 23.486, 40.842, 40.843, 46.124 e 55.470; quest 36.857; personagem 233.

## 2. Marie Arven: o protetor em quem confia, mas que também considera insensível

Marie, agricultor de Dorven, forma a relação mais persistente da campanha com Auditor. Seu perfil tem **compaixão 91** e **independência 5**. O comportamento observado combina com alguém que recorre frequentemente à ajuda, embora posição, contatos e reputação também influenciem as oportunidades.

Dos **85 pedidos** de Marie, **65 surgem por iniciativa própria** e 20 durante conversas. O jogador conclui 32, recusa 28 e outros 25 acabam resolvidos sem uma conclusão pelo jogador. Há **40 entregas de comida** a Marie; entrega e conclusão de quest são contagens diferentes.

| Momento | Dinheiro | Confiança no jogador | Reputação do jogador vista por Marie |
| --- | ---: | ---: | --- |
| Turno 1.024 | 88 | 15 | prestativo 6 |
| Turno 5.024 | 1 | 49 | prestativo 79; insensível 24 |
| Turno 10.024 | 0 | 93 | prestativo 100; insensível 100 |

No turno **3.603**, Marie faz seu primeiro pedido registrado. No **3.688**, uma recusa já registra urgência 65,55 e confiança 29. Muito depois, no **9.803**, outra recusa ocorre quando a confiança era 98. Ao final, ela está em 93: existe consequência social da recusa mesmo depois de muitos favores.

O título **“Protetor de Dorven”** resulta da regra de completar três pedidos de moradores da localidade. Neste caso, as três primeiras conclusões em Dorven são todas de Marie, nos turnos **3.742, 3.890 e 4.150**. Portanto, o título representa uma sequência de ajuda local concentrada nesse personagem.

**Qualidade da história:** o jogador não é apenas um visitante que recebe uma missão e desaparece. Marie volta a procurá-lo, reconhece os favores e reage às recusas. Há continuidade e uma relação ambivalente sustentada por acontecimentos reais.

**Limite:** os pedidos são sempre de alimento. Os dois rótulos chegam ao teto 100; a função que resume reputação subtrai o maior negativo do maior positivo, produzindo **saldo zero**, apesar da confiança 93. São marcas acumuladas de ajuda e recusa, mas isso ainda não demonstra sentimentos complexos. O diálogo também não expressa essa ambivalência: no turno 10.016, Marie diz apenas **“Sou Marie Arven, agricultor. Agora estou tentando trabalhar.”**

Evidências: personagem 56; quests e reações individuais em `evidencias_historias.json`; recusas 475.101 e 1.206.905.

## 3. Marie e Iria: a mesma casa, duas relações diferentes com o jogador

Marie e Iria Arven têm vínculo de **casamento 78**, amizade 61 e confiança mútua 64. Iria é cozinheiro, com **independência 81** e **compaixão 19**, valores bem diferentes dos de Marie.

Iria faz somente **nove pedidos**, todos durante conversas. Sete são resolvidos por outra via e dois recusados; nenhum consta como concluído pelo jogador. Auditor entrega comida a Iria sete vezes ao longo da campanha, mas isso não implica sete quests concluídas nem sete favores considerados relevantes.

No final, Iria atribui ao jogador **prestativo 64**, **insensível 13** e confiança **6**. Marie, na mesma casa, tem confiança 93. Iria também conhece ajuda prestada a Marie: no turno **9.890**, diz **“Ouvi dizer: Auditor entregou ração a Marie Arven.”**

**Qualidade da história:** os habitantes próximos não têm uma opinião uniforme sobre o jogador. A notícia de um favor chega ao cônjuge, mas a relação de confiança continua diferente. Isso dá identidade social aos NPCs e mostra informação circulando localmente.

**Limite:** o casamento cadastrado não se transforma aqui em um arco de decisões familiares. Não há evidência preservada de discussão sobre o jogador, plano conjunto para conseguir comida ou mudança do vínculo conjugal. A diferença entre os dois é compatível com personalidade e experiências distintas, mas esta campanha não isola quanto cada fator contribuiu.

## 4. Dorven: comida abundante, moradores sem dinheiro

O estado final da vila fornece o contexto mais forte para os pedidos de Marie e Iria:

| Pessoa ou recurso | Situação no turno 10.024 |
| --- | --- |
| Mercado | 239 unidades de comida e 240 de trigo; comida custa 2 moedas por unidade |
| Marie Arven, agricultor | 0 moedas |
| Iria Arven, cozinheiro | 1 moeda |
| Lyra Vale, guarda | 1.901 moedas |
| Ruan Alvor, caçador | 893 moedas |

**Interpretação:** existe uma história de acesso desigual à comida. No momento final, o alimento está disponível, mas Marie e Iria não conseguem pagar uma unidade com suas reservas. O problema não é somente produzir mais.

O código ajuda a explicar a situação: o agricultor recebe salário apenas quando consegue produzir, e o trigo já está no limite de 240. O cozinheiro precisa de espaço para um lote de três rações; com estoque 239, não consegue produzir esse lote. A guarda pode receber por serviço sem depender desse espaço no estoque. Esses mecanismos favorecem rotinas econômicas diferentes.

**Qualidade da história:** o cenário permite compreender por que um trabalhador pede comida enquanto outros acumulam dinheiro na mesma vila. É um contraste concreto, que liga profissão, mercado e comportamento.

**Limite:** não é uma desigualdade social deliberadamente elaborada pelos personagens. Parte dela resulta de bloqueios artificiais da produção. A fotografia final também não prova que o mercado estivesse cheio durante todos os pedidos anteriores. O save não registra revolta, negociação salarial, organização dos moradores ou mudança de profissão como resposta.

## 5. Iria Douran: a guarda que rouba e depois multa outro ladrão

Em **Elivia, vila do mapa 706**, Iria Douran é guarda e Arthus Ferros é caçador. São personagens diferentes de Iria Arven, de Dorven.

| Turno | Registro preservado |
| --- | --- |
| 9.994 | Iria Douran rouba comida no mercado de Elivia. |
| 9.997 | Arthus Ferros rouba comida no mesmo mercado. |
| 10.000 | Iria intervém no roubo e cobra 5 moedas de Arthus. |
| 10.021 | Arthus volta a roubar comida. |
| 10.024 | Iria intervém novamente, cobrando outras 5 moedas. |

Os três primeiros episódios sobrevivem como fatos conhecidos por NPCs, com confiança 100. Os dois últimos também estão na lista recente de eventos do mundo.

Iria tem **honestidade 41, compaixão 14, coragem 93 e ganância 80**. Arthus tem **honestidade 16, compaixão 87 e ganância 92**. A compaixão alta de Arthus não impede roubo; honestidade e necessidade também entram na escolha. O perfil não funciona como um único rótulo de “bom” ou “mau”.

No turno final, Iria tem fome 76, sede 68 e zero moedas. Arthus tem fome 84, sede 74 e zero moedas. Ambos carregam uma unidade de comida. O mercado conserva **211 unidades de comida**.

**Qualidade da história:** este é o melhor contraste entre profissão e necessidade. A guarda participa do mesmo ciclo de sobrevivência e crime que deveria fiscalizar. A aplicação da multa e o novo roubo de Arthus dão consequências e continuidade à sequência.

**Limite:** chamar isso de corrupção organizada seria inventar uma trama. O motor permite que a guarda roube e procure crimes cometidos por outros; os próprios roubos não entram na sua necessidade de segurança. A resposta registrada transfere até cinco moedas ao mercado, sem confiscar a comida ou prender o suspeito. A reincidência mostra que essa resposta não encerra o ciclo. Não há prova de remorso, perseguição pessoal ou plano consciente de exploração.

Evidências: personagens 718 e 721; fatos/eventos 1.229.400, 1.229.747, 1.230.151, 1.232.566 e 1.232.931.

## 6. Karmir e o fim das dinastias

Em Karmir, John Valerius, agricultor, e Ruan Valerius, cozinheiro, têm casamento 95, amizade 41 e confiança 57. Registros preservados atribuem roubos de comida a Ruan nos turnos **61 e 281**. John morre por privação no turno **481**; Ruan morre no **504**, 23 horas depois.

No save final, os **11 NPCs que estão fisicamente no mapa de Karmir estão mortos**. O mercado tem zero comida, 240 de trigo e 160 de água. Dois outros personagens vinculados à localidade permanecem vivos em mapas de sedes; portanto, não morreram todos os personagens associados à cidade.

**Interpretação:** o casal e a capital fornecem uma história de colapso da sobrevivência e da produção. Porém, os vínculos fortes do casal não geram um episódio registrado de cuidado ou luto. A população abstrata ainda aparece como 2.994 habitantes: ela não pode ser confundida com 2.994 personagens que observamos agir.

O mesmo padrão de privação atinge as seis famílias reais:

| Reino | Sucessão registrada | Turno da extinção da dinastia |
| --- | --- | ---: |
| Vale | Elena Vale → Nora Vale | 194 |
| Stone | Darin Stone → Aldren Stone | 256 |
| Solaris | Darin Solaris → Lyra Solaris | 288 |
| Kars | Tomas Kars morre sem familiar vivo para sucedê-lo | 339 |
| Corven | Dovha → Mira Corven | 373 |
| Luar | Tomas Luar → Ruan Luar, o herdeiro de ID 467 | 1.573 |

Ruan Luar, o herdeiro, permanece governante por **1.411 horas**, desde o turno 162. Há outro Ruan Luar na família, ID 464, que morre no turno 171; os dois não são a mesma pessoa.

Depois do turno **1.573**, passam **8.451 horas** até o save final sem governante em nenhum dos seis reinos. Todos continuam em crise sucessória e com estado militar `paz`.

**Qualidade da história:** a morte de governantes muda efetivamente a liderança, e a história política permanece registrada. O contraste entre o governo curtíssimo de Mira e a sobrevivência mais longa de Ruan dá alguma variedade.

**Limite:** todos os arcos dinásticos terminam em privação. Depois da extinção, não aparecem novos pretendentes, recomposição das famílias ou disputa pelo poder. A história política perde continuidade cedo. Problemas de sobrevivência identificados na auditoria, incluindo NPCs que morrem carregando comida, também reduzem a credibilidade desses desfechos; não se deve explicar toda morte como uma escolha plausível do personagem.

## Como os NPCs estão agindo

Os NPCs tomam decisões sem esperar por uma conversa com o jogador: trabalham, procuram alimento, compram, roubam, pedem ajuda e respondem a crimes. Marie iniciou 65 pedidos sozinha; Mira também fez um pedido espontâneo. O comportamento difere entre indivíduos e profissões.

Os registros do mundo contabilizam **5.144 roubos**, **1.301 respostas de guardas**, **120.502 coletas de alimento** e **395.518 transmissões de rumores**. Essas métricas incluem as 24 horas iniciais do mundo. Um rumor transmitido não representa uma história nova: muitas transmissões difundem os mesmos fatos.

No estado final existem **300 NPCs vivos e 116 mortos**. As últimas metas armazenadas dos vivos são:

| Última meta | Quantidade |
| --- | ---: |
| Descansar | 81 |
| Comer | 65 |
| Beber no poço | 45 |
| Coletar alimento | 39 |
| Comprar comida | 38 |
| Pedir ajuda | 11 |
| Trabalhar | 11 |
| Roubar | 7 |
| Investigar um roubo | 1 |
| Sem meta armazenada | 2 |

**268 de 300** têm uma última meta diretamente ligada a comer, beber, descansar ou conseguir comida por compra/coleta. É uma fotografia das metas armazenadas, não uma medição de tempo gasto: 210 metas estão concluídas, 47 ativas e 41 falharam.

Das 95 quests da campanha, **94 pertencem ao casal Marie e Iria** e uma a Mira. Todas pedem alimento. Há repetição de episódios, mais do que variedade de arcos.

As **406 conversas** geram 133 textos completos distintos, mas usam a mesma estrutura: apresentação, fome, ação atual e um fato conhecido. Mudar nome ou rumor aumenta essa contagem sem criar uma voz própria. O jogador consegue perceber a rotina e notícias locais; percebe muito menos gratidão, ressentimento, luto ou mudança de ambição pela fala.

## Avaliação da qualidade

| Aspecto | Avaliação deste save |
| --- | --- |
| Causas e consequências locais | Boa base: necessidades levam a ações; favores, recusas e crimes deixam efeitos. |
| Diferenças entre NPCs | Visíveis nos pedidos, relações de confiança, profissões e escolhas. Ainda pouco expressas no diálogo. |
| Participação do jogador | Concreta em Mira e Marie, mas concentrada na entrega de comida. |
| Variedade das histórias | Baixa: fome domina moradores, criminosos e famílias reais. |
| Relações familiares | Existem como dados, mas pouco se desenvolvem em ações e acontecimentos neste save. |
| Política ao longo do tempo | A sucessão funciona; a continuidade após extinção é fraca. |
| Histórias épicas ou religiosas | Não há registro de guerras, intervenções divinas ou acontecimentos religiosos com consequências próprias. |
| Credibilidade dos desfechos | Prejudicada pelos problemas de sobrevivência e economia encontrados na auditoria. |

O mundo possui religiões como Culto do Sol, Ordem da Maré e Culto da Aurora, além de devoção dos personagens. Neste save, isso fornece identidade de cenário, sem produzir uma história de deuses agindo. A cultura militar de um reino também não produziu guerra.

Minha leitura é que **há material emergente interessante, mas a variedade e a continuidade ainda são limitadas**. Mira já oferece uma história pessoal com começo, mudança e fim. Marie oferece uma relação que se acumula no tempo. Iria Douran oferece um conflito entre papel social e necessidade. Para histórias maiores, faltam consequências que abram objetivos novos; atualmente, a maioria retorna à obtenção de comida ou termina em morte por privação.

## Evidências e limites da reconstrução

O histórico persistente contém **133 eventos: 116 mortes, 11 mudanças de sucessão e seis fundações de reino**. As mudanças de sucessão incluem cinco nomeações e seis extinções. Os acontecimentos cotidianos usam uma lista curta de 256 eventos recentes. Reunindo os conhecimentos ainda preservados pelos personagens, há **13.344 fatos distintos**, mas esse conjunto não recupera tudo que aconteceu.

Por isso, as contagens globais vêm das métricas; as sequências individuais vêm do histórico, diário do jogador e fatos preservados. Ausência de uma ocorrência na memória curta não demonstra que ela nunca aconteceu. Para avaliar sistemas como luto, governo e diálogo, a leitura dos registros foi complementada pela inspeção das regras atuais.

- [Evidências extraídas: personagens, relações, cronologias, falas e eventos](</home/hugo/Área de trabalho/procedrual/reports/auditoria_jogador_10000/evidencias_historias.json>)
- [Save analisado](</home/hugo/Área de trabalho/procedrual/reports/auditoria_jogador_10000/save_final.json>)
- [Diário das ações do jogador](</home/hugo/Área de trabalho/procedrual/reports/auditoria_jogador_10000/acoes.jsonl>)
- [Relatório da auditoria de bugs](</home/hugo/Área de trabalho/procedrual/reports/auditoria_jogador_10000/RELATORIO.md>)
- Extrator reproduzível: `python3 -m experiments.story_report`, a partir da raiz do projeto.

SHA-256 do save, conferido antes e depois da extração: `9e7c83ae32df3898c52705ac0f1d7094119e84662204c28b851ad5bb678b7ed7`.
