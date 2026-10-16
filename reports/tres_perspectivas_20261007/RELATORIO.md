# Três testes: jogador, espectador e observação de todo o mundo

Executados em 07/10/2026, com regras `mvp-3`. **Três campanhas novas de 10.000 turnos cada**, totalizando 30.000 horas simuladas em mundos separados. O motor do jogo não foi alterado para produzir histórias ou melhorar os resultados.

As histórias pessoais funcionaram com e sem jogador. A evidência mais interessante foi reconhecimento por trabalho que circulou até a pessoa admirada por uma NPC. Também houve descoberta autônoma de restos, luto por amizade, denúncias e investigações. Entretanto, a sobrevivência continuou dominando entre **91,63% e 92,48% das seleções de necessidade**. Todos os reinos perderam os governantes nos dois testes sem jogador.

## Como os três testes foram feitos

| Teste | Seed | Perspectiva e interferência |
| --- | --- | --- |
| Jogador | Dovha | Controlador utiliza comandos públicos, cuida de suas necessidades, conversa, entrega itens e responde a pedidos. Informações ocultas do auditor não orientam suas ações. |
| Espectador | Dovha | Mundo gerado sem jogador. Acompanhamento narrativo da capital Vallen e da família Douran, com métricas globais de controle. Nenhum comando, provisão ou alteração de atributos. |
| Todo o mundo | Mira | Outra configuração de mundo, sem jogador. Inspeção das necessidades de todos os 440 NPCs após cada hora; eventos de todas as regiões e quadros das 76 localidades a cada 250 horas. |

No espectador também foram inspecionados os 456 NPCs e as 79 localidades; a diferença é o foco narrativo em Vallen. A observação global amplia a leitura a outras famílias, cidades, amizades, crimes e consequências regionais, em outra seed. Os dois observadores não são personagens do jogo.

Cada campanha começou no turno 24, após a preparação normal do mundo, e terminou no turno 10.024. Preparação não foi somada aos 10.000 turnos. Nenhum NPC foi teleportado ou criado manualmente. Não foram forçadas mortes, perdas, personalidades, estoques ou relações.

A cobertura global inclui NPCs em pontos de interesse, além dos moradores das cidades. Mira possui seis reinos, 76 localidades, oito pontos de interesse e 85 mapas; Dovha possui seis reinos, 79 localidades, oito pontos de interesse e 88 mapas. As decisões mantêm os intervalos normais do motor: observar tudo não faz todos os NPCs passarem a agir a cada hora.

**Limite da comparação:** com jogador, a proximidade acelera atualizações de alguns NPCs; a criação do jogador também participa da inicialização e ele altera recursos, informação e relações. Logo, Dovha com/sem jogador não isola somente a entrega de comida como causa. Mira muda também a seed. São três perspectivas reproduzíveis, não um experimento que atribui toda diferença a uma única variável.

## Resultado quantitativo

| Medida | Jogador: Dovha | Espectador: Dovha | Mundo: Mira |
| --- | ---: | ---: | ---: |
| Turnos executados | 10.000 | 10.000 | 10.000 |
| NPCs vivos no início | 456 | 456 | 440 |
| NPCs vivos no final | 317 | 311 | 302 |
| Mortes no período | 139 | 145 | 138 |
| Mercados sem comida | 26/79 | 31/79 | 31/76 |
| Localidades sem NPCs vivos | 4 | 4 | 1 |
| Reinos sem governante | 5/6 | 6/6 | 6/6 |
| Seleções de necessidade dos NPCs | 930.703 | 915.291 | 861.913 |
| Seleções fisiológicas | 91,6312% | 91,8018% | 92,4762% |
| Quests oferecidas | 49 | 0 | 0 |
| Quests concluídas | 11 | 0 | 0 |
| Erros de invariantes nos checkpoints | 0 | 0 | 0 |
| Diferença máxima no balanço monetário | 0 | 0 | 0 |
| Tempo de execução | 177,58 s | 180,23 s | 168,20 s |

Quests são contratos de envolvimento do jogador no motor atual. **Zero quests num mundo sem jogador é esperado**: os NPCs ainda trocam informação, entregam provisões e agem por conta própria, sem formalizar esses atos como contratos entre NPCs.

“Localidade sem NPCs vivos” não significa população abstrata zero. Os habitantes abstratos continuam separados dos personagens individualizados.

### O que os NPCs selecionaram

| Necessidade | Jogador | Espectador | Mundo |
| --- | ---: | ---: | ---: |
| Fome, sede e descanso | 852.814 | 840.254 | 797.064 |
| Trabalho/renda | 62.985 | 60.382 | 52.276 |
| Família | 7.395 | 7.605 | 7.255 |
| Segurança dos guardas | 7.021 | 6.592 | 5.231 |
| Ascensão financeira | 364 | 361 | 15 |
| Proteção pessoal | 101 | 75 | 51 |
| Retaliação/vingança | 15 | 17 | 10 |
| Luto | 8 | 5 | 9 |
| Reconhecimento/status | 0 | 0 | 2 |

São contadores persistentes de seleção do motor, descontada a preparação. Não são quantidade de ações concluídas ou porcentagem de horas do jogador. Deslocamentos, tentativas e frequência maior de decisões sob urgência também entram na seleção.

### Eventos que sustentam histórias

| Evento no período | Jogador | Espectador | Mundo |
| --- | ---: | ---: | ---: |
| Preocupação familiar | 10.032 | 9.926 | 9.502 |
| Ausência percebida | 2.227 | 2.301 | 1.945 |
| Busca em local sem encontrar familiar | 2.369 | 2.465 | 2.260 |
| Pessoa localizada | 520 | 520 | 498 |
| Informação transmitida | 310 | 392 | 390 |
| Denúncia | 58 | 52 | 28 |
| Investigação de responsável | 9 | 10 | 6 |
| Restos identificados | 3 | 4 | 4 |
| Recordação de pessoa perdida | 4 | 4 | 8 |
| Companhia prestada no luto | 1 | 0 | 0 |
| Responsabilidade cumprida por objetivo de status | 0 | 0 | 1 |

Milhares de preocupações familiares não equivalem a milhares de enredos diferentes: grande parte é cuidado ligado à privação. Informação e ação podem compor a mesma história; uma denúncia, por exemplo, também emite transmissão de informação.

### Ciclo de vida de algumas pressões

| Categoria | Jogador: criadas / satisfeitas / expiradas | Espectador: criadas / satisfeitas / expiradas | Mundo: criadas / satisfeitas / expiradas |
| --- | --- | --- | --- |
| Família | 12.259 / 1.262 / 10.946 | 12.227 / 1.276 / 10.899 | 11.447 / 1.275 / 10.116 |
| Luto | 32 / 5 / 27 | 34 / 4 / 30 | 28 / 8 / 20 |
| Proteção | 4.976 / 58 / 4.860 | 4.848 / 55 / 4.734 | 4.111 / 29 / 4.035 |
| Retaliação | 3.610 / 3.342 / 236 | 3.532 / 3.252 / 247 | 2.430 / 2.204 / 209 |
| Status | 19 / 0 / 29 | 19 / 0 / 29 | 13 / 1 / 19 |
| Ascensão | 2.428 / 7 / 2.498 | 2.472 / 5 / 2.542 | 2.243 / 8 / 2.295 |

Contagens representam episódios/transições, inclusive reativação do mesmo ID. Há necessidades anteriores ao turno 24 que terminam no período; portanto expirações podem superar novas criações. Expiração também pode ocorrer quando o dono morre. Retaliações frequentemente fecham por notícia da intervenção de um guarda: satisfação não prova que o dono retaliou pessoalmente.

## Teste 1 — como jogador

O personagem terminou vivo, com vida mínima/final 100 e 28 moedas. Usou coleta, trabalho, compra, venda, conversas e entregas. Visitou Vallen e o mapa externo; não percorreu todas as cidades como personagem.

Das 49 quests: 43 eram de comida, cinco de busca familiar e uma de companhia. Foram concluídas 11, recusadas 15, falharam três e 20 foram resolvidas por outro meio.

### A história de Bela Douran voltou a acontecer

Bela, ID 345, buscava notícias de Dovha, ID 339. O jogador identificou os restos no turno **968**, obtendo o fato **152367**, e informou Bela no turno **975**. Isso concluiu a **quest 146390**, encerrou a busca e gerou luto conhecido.

No turno **976**, Bela pediu companhia pela **quest 153527**. O controlador recusou no turno seguinte. A recusa não apagou a necessidade; foi registrada como interação social.

Essa sequência foi reproduzida numa campanha nova, sem reutilizar o save anterior. O save final tem exatamente o mesmo hash da campanha de fase 2 anterior. Isso confirma a reprodução das ações e consequências sob a mesma seed, regras e política do jogador; não representa uma história inédita independente.

Também houve companhia autônoma: Marie Stone, ID 485, procurou Mira Stone, ID 491, no turno **1.978**, ao lidar com a morte do cônjuge ID 488. Seu luto superou a fome na seleção daquele momento.

**Qualidade observada:** existe um encadeamento que chega ao jogador e muda de objetivo após a descoberta. A maior parte das interações posteriores ainda retorna a alimento e sobrevivência. O controlador recusou a única quest de companhia; esta campanha não demonstra a conclusão desse contrato pelo jogador.

## Teste 2 — como espectador

### Vallen teve um destino diferente

Na campanha sem jogador:

1. **Turno 228:** Bela Douran morreu por privação.
2. **Turno 252:** Dovha morreu; Lyra Douran, ID 342, assumiu o Reino Douran.
3. Lyra conheceu a morte de Dovha e teve luto, mas não chegou a realizar uma ação de luto antes de morrer.
4. **Turno 275:** Lyra morreu; a família real disponível se extinguiu e o reino entrou em crise sucessória.

A cadeia de busca do pai e pedido de companhia de Bela não pôde acontecer, pois ela morreu antes dele. É uma diferença concreta de trajetória. A campanha com jogador terminou com Bela viva e o Reino Douran com governante; isso não autoriza atribuir o contraste apenas a uma entrega específica, pelos limites metodológicos já descritos.

Até o turno **499**, os seis reinos desta campanha já estavam sem governante. Os territórios e os sobreviventes continuaram existindo; não ocorreu desaparecimento mágico do mundo.

### Iria Alvor percebeu a morte do cônjuge e agiu

Em Eliven, **Arthus Alvor, ID 675**, morreu no turno **322**. Iria Alvor, ID 672, estava entre as testemunhas; o vínculo conjugal era 90. Ela gerou luto a partir da morte conhecida e realizou uma recordação no turno **323** — evento **54602**, ligado ao fato **54357**.

Seu perfil inclui independência 89, lealdade familiar 89 e persistência 72. A ação aconteceu por iniciativa dela, sem um jogador solicitar ou executar uma quest. O episódio foi satisfeito.

### Luto também surgiu por amizade

Em Silmir, **Silas Luar, ID 1480**, morreu no turno **2.506**. A guarda **Iria Valerius, ID 1482**, conheceu a morte por presenciá-la. O contexto de luto registra vínculo 69 e `family: false`: não era parentesco.

Ela foi recordar a pessoa perdida no turno **2.561**, evento **364145**. Isso mostra que as reações não ficaram restritas aos primeiros colapsos dinásticos nem apenas à família real.

### Uma descoberta autônoma mudou a busca em luto

Em Mormar, **Nora Douran, ID 204**, morreu no turno **5.050**. Sua cônjuge **Lyra Douran, ID 207** — outra personagem, diferente da rainha ID 342 — identificou os restos no turno **5.138**.

A identificação **686216** gerou luto conhecido. Lyra realizou recordação no turno **5.186**, evento **692154**. Houve 88 horas entre a morte e a descoberta, e a reação dependeu da descoberta. Essa é uma sequência familiar executada inteiramente pelos NPCs.

### Crimes produziram alternativas, sem ataque automático

Em Arvia, **Marie Douran, ID 710**, denunciou a um guarda um roubo de Tomas Douran, ID 704, no turno **5.245**. Em Mormir, **Darin Arven, ID 517**, investigou o último local conhecido de Tomas Arven, ID 514, no turno **1.350**.

Marie tem vingatividade 95 e coragem 15; Darin tem vingatividade 89 e independência 95. São respostas distintas ao tipo de pressão criminal, em situações diferentes. Ambas podem fechar depois por conhecimento de intervenção do guarda. Não houve duelo, execução ou captura inventada na narrativa.

## Teste 3 — observação de todo o mundo

Todos os 440 NPCs da seed Mira foram inspecionados após cada hora, incluindo os dois personagens em mapas de pontos de interesse. Foram guardados **41 quadros**, do início ao final, cobrindo as 76 localidades e os seis reinos. A crônica retém também acontecimentos que o buffer curto do jogo já teria descartado.

### Lyra Ferros buscou reconhecimento, trabalhou e a notícia circulou

**Lyra Ferros, ID 489**, trabalha com madeira em Dorria, ID 471. Sua ambição é 61. Um encontro com **Tomas Corven, ID 807**, importante, havia criado uma necessidade de reconhecimento no turno **2**, durante a preparação.

Na campanha observada, ela selecionou status e cumpriu uma responsabilidade no turno **44**, evento **9221**, executando trabalho real. Esse é um objetivo anterior ao início que foi realizado durante o teste — não uma necessidade criada depois do turno 24.

Inicialmente, somente Lyra testemunhou o feito. No save final, o registro persistente desse evento aparece interpretado por:

- **Tomas Ferros, ID 497:** contribuição `responsável: 1`.
- **Tomas Corven, ID 807:** contribuição `responsável: 1`, justamente a pessoa que motivou a busca de reconhecimento.

Isso prova circulação e efeito social específico, sem atribuir uma hora de chegada que não foi registrada pelo auditor. A necessidade não concedeu fama instantaneamente: o efeito foi mediado pelo feito e pelo conhecimento. Evidência adicional: [reconhecimento.json](</home/hugo/Área de trabalho/procedrual/reports/tres_perspectivas_20261007/mundo/reconhecimento.json>).

Foi um dos melhores resultados narrativos dos testes. Também foi raro: somente duas seleções de status e uma responsabilidade cumprida em toda a campanha Mira. Um episódio posterior de status da mesma personagem expirou.

### Elena Alvor descobriu o familiar morto e reagiu

Em Karria, **Cael Alvor, ID 1743**, morreu no turno **256**. **Elena Alvor, ID 1746**, estudante e filha de Cael, identificou os restos no turno **332**, evento **53179**. Seu luto nasceu dessa informação; ela realizou recordação no turno **335**, evento **53616**.

O vínculo familiar era 100. Elena tem compaixão 10 e lealdade familiar 36, mas independência 83. A relação concreta e a morte conhecida foram suficientes para gerar reação; compaixão baixa não tornou o comportamento automaticamente indiferente.

### A informação demorou a chegar a Ruan Kars

Em Dorlen, **Silas Kars, ID 311**, morreu no turno **568**. **Ruan Kars, ID 308**, gerou luto somente no turno **636**, com confiança 30 na notícia e vínculo 97. Ele realizou recordação no turno **673**.

A diferença de 68 horas entre morte e luto mostra o limite de conhecimento individual. O mundo sabia que Silas estava morto; Ruan reagiu quando recebeu a informação.

### Investigar não garantiu resolver

Em Arvia, **John Corven, ID 1127**, conheceu o roubo de Tomas Bruma, ID 1112, no turno **2.638**. John verificou o último local conhecido no turno **2.788**, evento **371760**, mas o episódio de retaliação terminou expirado no turno observado **2.831**.

Houve tentativa concreta, sem resultado garantido. Isso dá consequência à indisponibilidade de informação/solução, embora o texto ainda seja curto e mecânico.

### Colapso dinástico coexistiu com sobrevivência local

Mira morreu no turno **142** e Marie Vale assumiu o Reino Vale. John Vale morreu no turno **253**; Marie morreu no **260**, encerrando a linha sucessória disponível. O último dos seis reinos perdeu seu governante no turno **981**.

Mesmo assim, 302 NPCs estavam vivos ao final. Os dois caçadores em mapas de pontos de interesse também sobreviveram com vida 100. Colapso das famílias governantes e desaparecimento de todos os NPCs são fenômenos diferentes; o primeiro foi recorrente, o segundo não aconteceu.

## Como ficou a qualidade das histórias

| Aspecto | Avaliação sustentada pelos testes |
| --- | --- |
| Causa e consequência | Boa nos exemplos documentados: ausência, descoberta, notícia, luto e mudança de objetivo têm ligação verificável. |
| Autonomia | Confirmada: luto por família/amizade, descoberta de restos, denúncias, investigação e reconhecimento aconteceram sem jogador. |
| Conhecimento individual | Visível: morte e reação ocorreram em horas distintas; informação circulou e produziu efeito social. |
| Personalidade | Há alternativas plausíveis e testes anteriores isolando traços. As campanhas misturam posição, recursos, relações e personalidade; não isolam um traço como causa exclusiva. |
| Continuidade | Existe em arcos individuais, inclusive depois de 5.000 horas. Ainda é limitada para famílias e governos, pois não há reposição. |
| Variedade cotidiana | Fraca: sobrevivência ocupa mais de 91% das seleções; cuidado material, roubo e crise de sucessão se repetem. |
| Texto e identidade | Funcional, mas simples. Muitos nomes completos repetidos dificultam reconhecer quem fez o quê sem IDs. |
| Histórias de grande escala | Sucessão e crise existem. Guerras, deuses, combate e sistemas religiosos executáveis continuam fora desta etapa e não surgiram nestes testes. |

O auditor voltou a encontrar **zero casos do critério estrito de dois NPCs escolhendo ações diferentes diante do mesmo evento-fonte**, nas categorias de luto, vingança e proteção que ele acompanha. Há diferenças diante do mesmo tipo de pressão, em eventos e condições diferentes. Não apresento isso como prova de diferenciação completa diante de um único acontecimento compartilhado.

## Bugs e inconsistências observados

### Integridade: nenhuma nova falha grave detectada no percurso

As três campanhas terminaram. Os 30 checkpoints passaram nas invariantes e no balanço monetário. Todos os saves finais carregaram e serializaram novamente de modo idêntico; duas cópias de cada save continuaram mais 24 horas de forma determinística.

A campanha de jogador não registrou ação inválida com mutação persistente. Não foi detectado crash, corrupção de save ou quebra de referência no percurso executado. Isso não substitui testar todas as combinações de ações e cenários.

### Problemas de comportamento e narrativa confirmados

| Problema | Evidência | Impacto |
| --- | --- | --- |
| Fisiologia domina em todas as perspectivas | 91,63%, 91,80% e 92,48% das seleções. | O jogador e o espectador recebem poucas histórias pessoais em comparação ao ciclo de sobrevivência. |
| Famílias governantes colapsam repetidamente | Todos os seis reinos sem governante até 499 em Dovha espectador e 981 em Mira. | Narrativa política tende ao mesmo destino; faltam continuidade material e sucessória além do mecanismo atual. |
| Pressões pessoais expiram sem ação | Luto: 30/34 expirados no espectador e 20/28 no global. Proteção: 4.734 e 4.035 episódios expirados. | Muitos acontecimentos geram necessidade, mas não ganham uma resposta visível. Expiração inclui morte do dono. |
| Reconhecimento executa raramente | Dovha: zero seleções; Mira: duas seleções e um feito. | O arco de Lyra é válido, mas não representa um sistema frequentemente ativo. |
| Ascensão após o início quase não se concretiza | Os cinco episódios satisfeitos do espectador e os oito de Mira encontrados na extração foram criados na preparação. | As novas metas posteriores competem mal ou não alcançam reserva suficiente; não há promoção de profissão/categoria. |
| Recursos locais e continuidade profissional seguem restritos | 31 mercados sem comida nos dois testes sem jogador. | Fome, roubo, mortes e sucessão continuam alimentados pelo mesmo problema material; repor profissionais ainda não foi implementado. |
| Nomes completos repetidos | 456 NPCs e 192 nomes distintos em Dovha; 440 NPCs e 183 nomes distintos em Mira. | Duas pessoas podem ter o mesmo nome, inclusive cônjuges. Identidade técnica por ID permanece correta, mas o relato fica confuso. |
| Satisfação não equivale sempre a ação própria | Retaliações frequentemente encerradas por notícia de guarda; compra/coleta pode ser apenas uma etapa familiar. | Contar fechamentos como aventuras completas ou vinganças realizadas exageraria as histórias. |
| Busca e informação desatualizada podem repetir pressão | Mais de 2.200 buscas sem localizar em cada mundo sem jogador. | Existem tentativas coerentes, mas falta variedade de pistas e continuidade das investigações. |
| Companhia teve pouca evidência nesta rodada | Uma entre NPCs na campanha com jogador; zero nos dois mundos sem jogador. | Esta rodada não mostrou diversidade consistente nas formas de lidar com luto. |

Os problemas acima são limitações de eficácia, continuidade ou apresentação. Não foram convertidos em correções de regras durante a auditoria. O diagnóstico não exige concluir que baixar o peso da fome seria a solução: economia, acesso, encontros, frequência de decisão e alternativas pessoais continuam combinados.

### Duas correções na medição, sem alterar o jogo

O observador foi verificado por 48 horas: mundos com e sem instrumentação terminaram com estado e RNG idênticos. As seleções oficiais vêm de `NPCNeedSelected`, não da repetição de amostras de debug.

Na conferência do mapa, somar apenas moradores dos mapas de cidades omitia os dois NPCs dos pontos de interesse. O total global da visualização foi corrigido usando o elenco inicial e as mortes canônicas; os contadores do motor, relatórios e saves já estavam corretos. Os números locais continuam representando somente a localidade selecionada.

A extração também preserva necessidades criadas durante a preparação e realizadas depois, identificadas como `carried_from_preparation`. Assim, o trabalho de reconhecimento no turno 44 não é escondido nem descrito incorretamente como uma necessidade criada durante a campanha.

## Evidências, saves e reprodução

- [Comparativo estruturado](</home/hugo/Área de trabalho/procedrual/reports/tres_perspectivas_20261007/comparativo.json>) e [verificação final](</home/hugo/Área de trabalho/procedrual/reports/tres_perspectivas_20261007/verificacao_final.json>).
- Jogador: [métricas](</home/hugo/Área de trabalho/procedrual/reports/tres_perspectivas_20261007/jogador/metricas_fase2.json>), [ações](</home/hugo/Área de trabalho/procedrual/reports/tres_perspectivas_20261007/jogador/acoes.jsonl>) e [save](</home/hugo/Área de trabalho/procedrual/reports/tres_perspectivas_20261007/jogador/save_final.json>).
- Espectador: [histórias com fontes e ações](</home/hugo/Área de trabalho/procedrual/reports/tres_perspectivas_20261007/espectador/historias.json>), [crônica](</home/hugo/Área de trabalho/procedrual/reports/tres_perspectivas_20261007/espectador/cronica.jsonl>) e [save](</home/hugo/Área de trabalho/procedrual/reports/tres_perspectivas_20261007/espectador/save_final.json>).
- Mundo: [histórias com fontes e ações](</home/hugo/Área de trabalho/procedrual/reports/tres_perspectivas_20261007/mundo/historias.json>), [crônica](</home/hugo/Área de trabalho/procedrual/reports/tres_perspectivas_20261007/mundo/cronica.jsonl>), [quadros do mundo](</home/hugo/Área de trabalho/procedrual/reports/tres_perspectivas_20261007/mundo/quadros_mundo.json>) e [save](</home/hugo/Área de trabalho/procedrual/reports/tres_perspectivas_20261007/mundo/save_final.json>).
- [Verificação de observação sem interferência](</home/hugo/Área de trabalho/procedrual/reports/tres_perspectivas_20261007/verificacao_observador.json>).

Cada pasta dos observadores contém também `elenco.json`, `cobertura.json`, `necessidades_pessoais.jsonl`, `metricas_fase2.json`, `relatorio.json` e saves nas horas 1.000 e 5.000. Necessidades são observadas no fechamento da hora; estados intermediários instantâneos podem escapar dessa amostra. As métricas persistentes permanecem a contagem oficial. Eventos do barramento podem ser aninhados; para uma ordem temporal estável, use turno e ID.

A visualização é uma reprodução dos quadros medidos a cada 250 horas, com as posições reais das localidades, limites dos reinos e pontos de interesse gerados. Não é um mundo novo sendo simulado dentro do mapa e não inventa estados entre os quadros. Os eventos destacados são acontecimentos reais; sua presença no mapa do auditor não significa que todo NPC os conhecia.

Para reproduzir, use novas pastas de saída:

```bash
python3 -m experiments.phase2_audit --seed Dovha --turnos 10000 --output reports/nova_rodada/jogador
python3 -m experiments.perspective_audit --mode espectador --seed Dovha --turnos 10000 --output reports/nova_rodada/espectador
python3 -m experiments.perspective_audit --mode mundo --seed Mira --turnos 10000 --output reports/nova_rodada/mundo
```

Foi adicionado somente código de auditoria/extração e os artefatos dos testes. SHA-256 do núcleo `procedural/*.py` permanece `984cefd941906afb9e35f70a1fb01f82322290b6fc132dcf9576d3b102b9de0c`.

Saves e relatórios anteriores foram preservados. Os três novos saves usam `mvp-3`.
