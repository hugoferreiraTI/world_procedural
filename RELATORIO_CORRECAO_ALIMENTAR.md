# Correção alimentar individual — implementação, auditorias e histórias

Etapa anterior à Fase 4. Especificação executada: [correcao_alimentar.md](</home/hugo/Área de trabalho/procedrual/correcao_alimentar.md>). Versão atual: **mvp-4-alimentacao**. Todos os resultados deste relatório pertencem ao mesmo código congelado; não houve alteração de regra durante as campanhas.

## Resumo executivo

Implementei separação entre reserva, refeição e emergência; refeição normal a partir de fome 50; interrupção de objetivos para comer; prazo biológico comum; e variantes explícitas de aquisição com consumo imediato. Permanecem finitos os estoques, salários, dinheiro e tempo. Fisiologia, dano, cura, HP inicial e regras de economia/formação/vida pessoal foram preservados.

Os **105 testes anteriores e 25 regressões novas passaram: 130 testes**. As três auditorias completaram **10.000 horas cada**. A reprodução observacional das três campanhas antigas também completou 10.000 horas e reproduziu exatamente seus saves originais.a

As mortes totais passaram de **690 para 331**. Mortes com fome no limite passaram de **687 para 320**. Mortes por fome carregando alimento passaram de **108 para zero**, incluindo os **107 casos de aquisição na última decisão** e o caso de comida já possuída. Essa mudança, junto das regressões que reproduzem as falhas antigas, comprova correção do bloqueio entre possuir/adquirir e consumir alimento vital.

**A prevenção ainda é pouco efetiva na população.** Apenas 7,43%–10,98% dos NPCs vivos terminam com a reserva-alvo; a fome média no início da procura permanece perto de 76 e no consumo perto de 82. Somente 1,48%–2,54% das procuras começam antes do limiar de refeição. Portanto, não declaro que a alimentação passou a ser amplamente preventiva nem que a pobreza foi resolvida. O mecanismo existe e funciona nos cenários controlados; sua adoção no mundo continua limitada.

O espaço para necessidades pessoais cresceu, mas a seleção fisiológica ainda representa aproximadamente 87%–88% das decisões. Há **12 casos narrativos documentados** adiante: famílias, procura, luto, investigação, sucessão, reconhecimento, carreiras e intervenções do jogador. Também aparecem incoerências sociais reais e repetição. Não iniciei a Fase 4.

## Alterações realizadas

- `feeding.py` calcula cobertura, duração até consumir, margem biológica e diagnóstico; não escolhe objetivos nem executa ações.
- `needs.py` acrescenta manutenção moderada da reserva e distingue risco vital de desempate comum.
- `goals.py` rejeita alternativas alimentares biologicamente lentas, permite refeições explícitas e suspende/retoma objetivos válidos.
- `items.py` informa aquisições, transferências e consumo reais à instrumentação.
- `models.py`, `validation.py` e persistência preservam estado alimentar e objetivo suspenso, com validação.
- `engine.py` instala os serviços e oferece `refeicao`/`refeição`; `ui.py` explica o comando.
- `rules.py` centraliza os parâmetros; as rotinas originais de fisiologia e descanso são estruturalmente idênticas às anteriores.

Também limitei lotes de trabalho pagos com comida ao déficit legítimo da reserva. Na verificação curta anterior às campanhas, a atualização acumulada de trabalho podia entregar um lote excessivo de rações. A correção foi feita **antes** do congelamento e dos três testes longos. A verificação curta foi preservada como diagnóstico, sem entrar nos números finais.

## Arquitetura preservada

O fluxo permanece **State/Knowledge → Need → Priority → Solutions → Goal → Action → Consequence → New State**. O cálculo temporal é metadado da solução existente. Não há GOAP, plano paralelo, roteiro por nome de personagem ou regra para produzir um desfecho predeterminado.

Aquisição continua sendo transferência ou criação por produção legítima; consumo continua removendo uma unidade real e reduzindo fome. Necessidades familiares, profissionais e pessoais disputam as mesmas prioridades. Os módulos `economy.py`, `professions.py` e `personal.py` foram preservados byte a byte; as consequências deles mudam porque os personagens passam a decidir e sobreviver de outra maneira.

Os saves novos usam `mvp-4-alimentacao`; saves antigos `mvp-4` são recusados explicitamente, permanecendo intactos. A geração usa a referência **mvp-4**, separada da versão de regras, para conservar geografia, elenco e relações iniciais antes da simulação histórica. A verificação de Dovha e Mira está em [geracao_inicial_verificada.json](</home/hugo/Área de trabalho/procedrual/reports/correcao_alimentar/geracao_inicial_verificada.json>). As primeiras 24 horas já respondem às novas regras, de modo que o estado no início da auditoria pode diferir.

## Regras de reserva alimentar

O alvo normal é **24 horas de cobertura**, com crescimento de fome 2/h e nutrição 40 por ração: `ceil(24 × 2 / 40) = 2 rações`. O inventário pessoal representa a reserva. Não foi criada uma despensa doméstica.

Para destino conhecido no mesmo mapa, a cobertura considera o maior entre 24 horas e duração conhecida da viagem + **6 horas de margem**, limitada a **6 rações**. Destino em outro mapa sem trajeto conhecido não permite consultar o mapa global para obter uma distância milagrosa.

`food_reserve` usa base 26, peso de déficit 8 e peso de fome 0,2 até o limiar 50, somados aos modificadores comuns de prioridade. É manutenção moderada, não emergência automática. Não obriga um personagem saudável a abandonar uma necessidade pessoal importante. A procura considera compra, coleta, trabalho compatível, serviço temporário, provisão e pedido já existentes, conforme o que é conhecido e disponível.

O alvo limita a busca preventiva; não proíbe transferências legítimas. Um pagamento produtivo ou uma provisão familiar pode deixar uma terceira ração, e presentes externos também podem ultrapassar o alvo. Isso é diferente de incentivar acúmulo ilimitado. Nas três campanhas finais, os inventários observados dos NPCs vivos têm 0–3 rações.

## Regras de refeição

Com fome **≥50**, surge a necessidade de refeição. Com alimento possuído, comer é uma alternativa direta, sem uma nova aquisição. O valor 50 é uma hipótese configurável, não um ótimo definitivo.

Comprar para reserva continua sem reduzir fome. As variantes `buy_meal`, `forage_meal`, `steal_meal`, `ask_meal`, `work_for_meal` e `service_meal` executam a aquisição legítima e depois consomem de fato. São candidatas de emergência quando a margem é curta; pedido pendente ao jogador não se transforma em uma refeição instantânea.

O comando público `refeicao` usa o mesmo serviço de compra e consumo dos NPCs, cobra o preço real e consome uma hora. Falta de produto ou dinheiro não gera alimento. O jogador da auditoria manteve sua política anterior e não foi privilegiado com uso obrigatório desse comando.

Nutrição usada é `min(fome antes de consumir, 40)`. Sua média nova foi **40 em todas as campanhas**; antes já era aproximadamente 39,94–39,97. Não há evidência de que desperdiçar sistematicamente a nutrição da ração fosse o principal problema anterior. O problema comprovado era conseguir chegar ao consumo a tempo.

## Regras de emergência

Fome **≥80**, ou fome ≥50 com margem estimada de sobrevivência ≤6 horas, recebe tratamento emergencial. O intervalo de decisão torna-se uma hora nos estados críticos, inclusive para NPC distante. A fisiologia continua avançando toda hora, como antes.

Risco vital precede desempate por ID. Uma refeição escolhida pode interromper trabalho, treinamento, descanso, viagem e preparação. O objetivo suspenso é armazenado; após estabilização, só é retomado se sua necessidade e solução ainda forem válidas. A continuidade comum dos objetivos permanece.

A preparação de água e destino não sobrepõe uma refeição imediatamente necessária. Sede já fatal ainda pode preceder fome alta menos urgente. Se duas privações são simultaneamente fatais e uma única ação não resolve ambas, a regra não garante imortalidade.

## Avaliação temporal de sobrevivência

Cada solução alimentar compara **EstimatedTimeUntilFoodConsumed** com **EstimatedSurvivalMargin**. A margem projeta até 128 fechamentos horários, usando HP próprio, fome, sede, privação consecutiva, dano crescente e o bioma atual. O valor é recalculado quando o estado muda.

O tempo da solução inclui deslocamento conhecido, duração de aquisição, renda estimada quando necessária, ida ao mercado, compra e uma oportunidade adicional de comer. Refeição explícita não adiciona uma segunda decisão de consumo. Trabalho de aprendiz considera remuneração diferente do trabalho comum. Em manutenção saudável, a estimativa inclui a espera até o limiar normal de refeição.

Uma alternativa pode permanecer economicamente possível e ser marcada `survival_viable=false`, motivo `SolutionTooSlow`. Ela sai das candidatas alimentares salvadoras. Trabalho continua possível quando há prazo; não foi proibido para todo personagem pobre.

Preço desconhecido usa somente um limite inferior de referência, **2 moedas**, identificado como desconhecido; não vira informação de cotação real. Produto ausente, falta de dinheiro, preço desconhecido, mercado desconhecido, distância e comida já possuída possuem indicadores separados. Nenhum estoque distante é consultado como conhecimento pessoal atual.

É uma estimativa pequena, não uma garantia de rota: distância local pode subestimar desvios, bioma futuro pode mudar a sede e produção/concorrência podem mudar o mercado. O cálculo não prevê todos os eventos futuros nem assegura execução de uma cadeia em ambiente competitivo.

## Testes

Resultado: **130 testes passaram**, incluindo os **105 originais preservados** e **25 novos**. Registro completo: [testes_finais.txt](</home/hugo/Área de trabalho/procedrual/reports/correcao_alimentar/testes_finais.txt>); regressões: [test_feeding.py](</home/hugo/Área de trabalho/procedrual/tests/test_feeding.py>).

As regressões cobrem reserva suficiente sem nova procura; reposição preventiva saudável; prioridade pessoal importante; refeição no limiar; interrupção de trabalho, descanso empatado, viagem e treinamento; preparação de água; sede fatal concorrente; cadeia de renda lenta demais e cadeia ainda válida; refeição com orçamento/estoque finitos; mercado vazio; compra sem consumo; lotes limitados; viagem sem conhecimento global; preço desconhecido; determinismo; fila de aquisições; save/load e retomada; comando público com tempo real e ação inválida sem mutação.

Além disso, os três saves finais passaram por validação, round-trip idêntico e continuação determinística de 24 horas. Não houve erro de validação nem diferença no balanço de moeda. Essas verificações detectam incoerências estruturais; não demonstram, sozinhas, boa qualidade narrativa.

## Auditorias de 10.000 horas

Foram repetidos jogador Dovha, espectador Dovha e observador global Mira. O jogador usa comandos públicos e a política automática anterior; não equivale a um humano que improvisa livremente por 10.000 horas. As outras duas campanhas não possuem intervenção de jogador.

O código congelado tem SHA-256 **3ad877c9ff085a0d07009ffcdae917beb9473a012241c0f4e731ea7238ea363b**. O manifesto, snapshot do código e hashes dos artefatos antigos permitem verificar o congelamento e a preservação. Cada campanha tem checkpoints de 1.000 e 5.000 horas, save final, registros alimentares e narrativos, métricas e estados econômicos amostrados.

Para medir indicadores novos na versão antiga, reproduzi as três campanhas com o código histórico isolado e observadores externos. Os saves finais reproduzem exatamente os SHA-256 originais. Para confirmar conhecimento antes de decisões profissionais e de segurança, reproduzi os primeiros 5.000 turnos novos; os três checkpoints também ficaram idênticos aos originais novos.

Essa comparação controla seed, mecanismo de geração e política de teste, mas avalia **o conjunto da correção**. Não isola o efeito de cada parâmetro; decisões diferentes mudam sorteios, trajetórias, sobreviventes e reposição profissional. As médias são de eventos e NPCs observados, não do mesmo painel fixo de sobreviventes.

Dados: [manifesto_auditoria.json](</home/hugo/Área de trabalho/procedrual/reports/correcao_alimentar/manifesto_auditoria.json>), [verificacao_final.json](</home/hugo/Área de trabalho/procedrual/reports/correcao_alimentar/verificacao_final.json>), [comparativo.json](</home/hugo/Área de trabalho/procedrual/reports/correcao_alimentar/comparativo.json>), [reproduções antigas](</home/hugo/Área de trabalho/procedrual/reports/correcao_alimentar/baseline_medicoes>), [reproduções observacionais de ações](</home/hugo/Área de trabalho/procedrual/reports/correcao_alimentar/replay_acoes>).

## Comparação com a Fase 3 original

Cada célula mostra **antes → depois**. “Mortes com fome” inclui a condição de fome 100 com ou sem sede 100; é a mesma classificação do diagnóstico histórico.

| Indicador | Jogador Dovha | Espectador Dovha | Mundo Mira |
| --- | --- | --- | --- |
| Mortes totais | 221 → 104 | 258 → 103 | 211 → 124 |
| Mortes com fome | 219 → 103 | 258 → 98 | 210 → 119 |
| Mortes com fome carregando alimento | 38 → 0 | 39 → 0 | 31 → 0 |
| Aquisição na última decisão fatal | 38 → 0 | 38 → 0 | 31 → 0 |
| Comida possuída antes da última decisão | 0 → 0 | 1 → 0 | 0 → 0 |
| NPCs vivos no final | 286 → 350 | 278 → 346 | 279 → 324 |
| Fome no início da procura | 77,37 → 76,24 | 78,06 → 76,82 | 78,03 → 76,55 |
| HP no início da procura | 96,12 → 92,15 | 95,65 → 92,53 | 95,73 → 93,21 |
| HP na aquisição | 96,05 → 92,88 | 95,62 → 93,23 | 95,62 → 93,88 |
| Fome na aquisição | 76,72 → 75,71 | 77,78 → 76,29 | 77,86 → 75,90 |
| Fome ao consumir | 82,56 → 82,19 | 83,46 → 82,52 | 83,53 → 82,35 |
| HP ao consumir | 96,20 → 92,88 | 95,77 → 93,24 | 95,76 → 93,88 |
| Procura → aquisição, horas | 2,01 → 2,67 | 2,09 → 2,66 | 2,19 → 2,61 |
| Aquisição → consumo, horas | 43,25 → 6,96 | 31,60 → 6,61 | 28,99 → 6,83 |
| Procura → consumo, horas | 5,17 → 5,16 | 5,20 → 4,83 | 5,14 → 4,82 |

Aquisição → consumo acompanha lotes FIFO: pode incluir comida paga por trabalho e guardada por muito tempo. Sua queda de 29–43 horas para aproximadamente 7 horas reflete também o fim de acúmulos excessivos. Não significa que toda procura ficou dezenas de horas mais rápida: procura → consumo muda pouco e aquisição demora um pouco mais.

As médias temporais usam pares rastreáveis que chegaram à etapa correspondente; aquisições sem consumo não produzem um tempo de consumo completo. Estoque inicial sem carimbo não é atribuído indevidamente a um lote novo. Procura nova inclui manutenção e refeição; a antiga não tinha necessidade separada de reserva. Esses limites importam na leitura das médias.

O HP médio de aquisição **caiu**, em vez de melhorar. Mais sobreviventes fragilizados e trajetórias diferentes podem contribuir, mas não isolei essa causa. Não apresento essa média como prova de melhora de saúde. O desaparecimento do extremo fatal de aquisição com 1–3 HP é um resultado distinto da média populacional.

## Análise das mortes

Na versão corrigida, as condições terminais são **320 mortes com fome 100** e **11 com sede 100 sem fome 100**; não há a condição conjunta nas novas campanhas. O registro classifica estado terminal, não um laudo completo que atribua cada ponto de dano a fome ou sede ao longo da vida. Nenhum desses mortos carregava comida.

Nas 320 mortes com fome, **308** tinham uma cotação local conhecida recente; **209** não podiam comprar uma ração por essa cotação. **56** tinham dinheiro zero. Essas condições se sobrepõem. Não classifico preço desconhecido como pobreza e não deduzo estoque no turno da morte a partir do estoque final.

| Condição entre mortos com fome | Jogador Dovha | Espectador Dovha | Mundo Mira |
| --- | --- | --- | --- |
| Sem alimento no inventário | 103 | 98 | 119 |
| Cotação conhecida recente | 97 | 95 | 116 |
| Não podia pagar essa cotação | 63 | 70 | 76 |
| Dinheiro zero | 17 | 25 | 14 |
| Rejeição por prazo nos últimos 6 turnos | 103 | 98 | 119 |

Todos os 320 tinham pelo menos uma rejeição recente por prazo insuficiente. Isso comprova que o filtro identificou caminhos lentos no trecho terminal; **não prova que toda morte era inevitável desde horas ou dias antes**, nem que todas tiveram exclusivamente pobreza como causa. É necessário distinguir o problema terminal da prevenção anterior.

Ainda aparecem objetivos finais `sleep` e `work`. Ao contrário do padrão antigo, não havia refeição carregada para interromper e comer. Objetivo registrado também não é sinônimo de última ação bem-sucedida: nos três modos, as últimas ações bem-sucedidas frequentemente são beber. Um caminho alimentar bloqueado pode deixar outro objetivo ou uma tentativa sem sucesso no estado terminal. Não reclassifico automaticamente esses casos como “morreu porque preferiu dormir tendo comida”.

As novas campanhas somaram **33 mortes com `work` como objetivo final**, contra as 318 últimas escolhas alimentares de trabalho do diagnóstico antigo. Esses indicadores têm definições diferentes; não uso a diferença como contagem exata de um único bug corrigido. As regressões controladas demonstram que uma cadeia biologicamente impossível não é aceita como salvação alimentar.

O cenário antigo de Bela Valerius, descanso empatado e preparo de água apesar da ração possuída, está representado em regressões. Na campanha nova, Bela não morre carregando comida. Escassez de acesso e fragilidade continuam podendo matar depois. Detalhes por pessoa: [mortes_remanescentes.json](</home/hugo/Área de trabalho/procedrual/reports/correcao_alimentar/mortes_remanescentes.json>).

## Análise do estoque pessoal e da prevenção

| Indicador | Jogador Dovha | Espectador Dovha | Mundo Mira |
| --- | --- | --- | --- |
| Reserva ≥2 no final, % | 12,94 → 7,43 | 11,15 → 10,98 | 12,90 → 10,49 |
| Reserva, média dos 40 quadros, % | 11,74 → 8,07 | 10,41 → 7,61 | 10,77 → 8,38 |
| Rações por NPC vivo no final | 5,87 → 0,34 | 4,05 → 0,36 | 4,40 → 0,42 |
| Rações, média dos 40 quadros | 3,24 → 0,35 | 2,24 → 0,34 | 2,07 → 0,35 |

| Inventário final dos vivos | Jogador Dovha | Espectador Dovha | Mundo Mira |
| --- | --- | --- | --- |
| 0 ração/rações | 268 | 272 | 235 |
| 1 ração/rações | 56 | 36 | 55 |
| 2 ração/rações | 15 | 24 | 22 |
| 3 ração/rações | 11 | 14 | 12 |

| Início real da procura | Jogador Dovha | Espectador Dovha | Mundo Mira |
| --- | --- | --- | --- |
| Antes de fome 50, % | 2,54 | 1,48 | 1,65 |
| Com fome ≥80, % | 68,10 | 69,33 | 68,38 |
| Com HP ≤3, quantidade | 373 | 414 | 333 |
| Seleções de manutenção da reserva | 5.222 | 2.072 | 2.262 |
| Comida possuída no início, média | 0,015 | 0,009 | 0,009 |
| Alvo registrado no início, média | 2,00 | 2,00 | 2,00 |
| Déficit registrado no início, média | 1,98 | 1,99 | 1,99 |

As reservas antigas eram muito concentradas: a média de 4–6 rações por NPC não significava que a maioria tinha cobertura; só 11%–13% tinham duas ou mais no final. Pagamentos em lotes e acúmulo elevaram essa média. Limitar esses lotes evita esconder a vulnerabilidade por trás de uma média alta.

As médias de quadros usam 40 observações a cada 250 horas, excluindo o quadro inicial; os arquivos contêm 41 quadros com esse inicial incluído. O alvo médio registrado foi 2 rações nas procuras destas campanhas. O alvo ampliado para viagens longas foi exercitado em regressão, sem inventar uma ocorrência frequente nos logs.

Mesmo assim, a correção **não aumentou a proporção mantendo reserva**. A maioria termina com zero ou uma ração. Mais de dois terços das procuras ainda começam com fome ≥80; há **1.120 inícios de procura com HP ≤3**, que são eventos, não 1.120 pessoas distintas ou mortes. Esse achado impede declarar cumprida uma prevenção populacional forte.

Comida de reserva disputa prioridades de renda, fadiga e necessidades pessoais; alguns personagens não conseguem pagar, outros têm caminhos conhecidos limitados ou concorrência por provisões. O alvo configura uma intenção, não entrega automaticamente os recursos para realizá-la. O filtro temporal corrige a aceitação de uma saída impossível, mas não transforma essa saída em viável.

Assim, o ganho principal comprovado está na coerência de refeição e emergência; a rotina preventiva exige diagnóstico adicional de prioridade, continuidade e acesso. Os números não autorizam aumentar arbitrariamente seu peso e passar por cima da vida pessoal.

## Impacto nos mercados e na pobreza

| Indicador | Jogador Dovha | Espectador Dovha | Mundo Mira |
| --- | --- | --- | --- |
| Comida municipal total final | 8.629 → 9.610 | 8.149 → 9.495 | 7.060 → 8.732 |
| Mercados sem comida no final | 12 → 8 | 17 → 5 | 17 → 8 |
| Dinheiro insuficiente para uma refeição local | 124 → 172 | 102 → 158 | 112 → 135 |
| Insuficiente para refeição, % dos vivos | 43,36 → 49,14 | 36,69 → 45,66 | 40,14 → 41,67 |
| NPCs com menos de 10 moedas | 219 → 279 | 189 → 260 | 192 → 255 |
| Déficits profissionais locais finais | 7 → 3 | 7 → 2 | 7 → 5 |

Há mais comida municipal total e menos mercados vazios no final, enquanto a proporção sem dinheiro para uma refeição **aumenta nas três campanhas**. Estoque agregado e acesso individual são problemas diferentes. Uma cidade com alimento não implica que uma pessoa saiba da oferta, tenha dinheiro, chegue lá e consiga consumir antes de morrer.

O estoque municipal não foi aumentado por regra nova: essas quantidades resultam de produção, consumo e transferências existentes sob outras trajetórias. Os quadros de reserva/economia amostram o tempo; um valor final sozinho não descreve cada crise de abastecimento.

## Instrumentação de prazo e interrupção

Os logs registram fome/HP na procura, aquisição e consumo; comida possuída, alvo/déficit; tempos entre etapas; prazo estimado e margem; objetivo interrompido; condições de morte; última ação bem-sucedida e motivos/condições conhecidos das alternativas rejeitadas. O save retém diagnóstico recente limitado a 256 entradas; os arquivos de auditoria preservam o fluxo integral. Essa separação mantém observabilidade sem crescimento ilimitado de memória dentro do mundo.

| Diagnóstico novo | Jogador Dovha | Espectador Dovha | Mundo Mira |
| --- | --- | --- | --- |
| Interrupções emergenciais de objetivos | 1.226 | 1.313 | 1.185 |
| Alternativas rejeitadas por prazo | 8.007 | 7.378 | 7.022 |

Somam **3.724 interrupções emergenciais** e **22.407 rejeições por prazo**. São registros de ocorrência, não pessoas únicas, nem uma contagem automática de vidas salvas. As interrupções incluem trabalho, treino, descanso e buscas aquisitivas anteriores.

Exemplo real de prazo: no jogador, turno **103**, NPC **18**, fome 100 e HP 96, uma alternativa `work` foi rejeitada com **33 horas até consumir** contra **32 horas de margem**, `economically_viable=true`, `survival_viable=false` e condição conhecida `NoMoney`. O filtro pode antecipar o fracasso antes de chegar a HP 1–3.

Nas campanhas, o motivo final de rejeição registrado foi `SolutionTooSlow`; ausência de produto/dinheiro/preço conhecido aparece nos indicadores de condições e na geração de candidatas. Isso não significa que todas essas condições eram presentes em toda rejeição. Mercado/rota desconhecidos têm tratamento separado, mas não apareceram como motivo final nesses logs canônicos. As regressões exercitam conhecimento incompleto.

## Impacto sobre necessidades pessoais e profissões

| Indicador | Jogador Dovha | Espectador Dovha | Mundo Mira |
| --- | --- | --- | --- |
| Seleção fisiológica, % | 88,66 → 87,13 | 89,84 → 87,83 | 90,47 → 87,77 |
| Seleções pessoais | 6.428 → 8.954 | 5.110 → 8.598 | 4.842 → 7.862 |
| Necessidades pessoais satisfeitas | 2.229 → 3.946 | 2.235 → 3.741 | 2.926 → 4.057 |
| Personagens que concluíram formação | 59 → 13 | 88 → 5 | 57 → 23 |
| Reformados entre residentes existentes | 8 → 7 | 13 → 4 | 8 → 10 |
| Trabalhadores materializados | 59 → 6 | 88 → 1 | 58 → 16 |

Seleções pessoais somam **16.380 → 25.414**; satisfações pessoais, **7.390 → 11.744**. A seleção fisiológica perde aproximadamente 1,5–2,7 pontos percentuais, sem deixar de dominar. A reserva aparece separadamente da categoria fisiológica nesta classificação; inclusão dela também usa decisões, não deve ser apresentada como tempo social livre.

“Satisfeita” é uma transição de necessidade registrada pelo motor, não uma prova de que cada uma produziu uma história completa ou uma ação social bem-sucedida. Algumas necessidades mudam/encerram por atualização de contexto. A leitura de histórias usa ações e eventos, além desses totais.

Concluintes de formação somam **204 → 41** e materializações **205 → 23**. Não disfarço isso como melhora automática da carreira: menos mortes reduzem parte das vagas, mas não isolei quanto da queda vem disso e quanto vem da concorrência com outras ações. Residentes existentes reformados somam **29 → 21**. A longa sequência de Mira, abaixo, demonstra perda e retomada de progresso, não formação contínua garantida.

Durante as campanhas novas, **281 necessidades pessoais ativas** foram encerradas pela morte de seus donos: 75/95/111 nos três modos. Isso conta necessidades, não 281 sagas interrompidas. Há 82 necessidades familiares nessa condição. A morte ainda limita continuidade.

Na comparação dos eventos sociais, não há melhora uniforme:

| Evento social | Jogador Dovha | Espectador Dovha | Mundo Mira |
| --- | --- | --- | --- |
| Procura familiar | 1.130 → 1.946 | 1.321 → 2.204 | 959 → 2.076 |
| Pessoa localizada | 275 → 564 | 231 → 502 | 321 → 458 |
| Investigação | 24 → 48 | 14 → 57 | 67 → 30 |
| Lembrança de perda | 6 → 2 | 3 → 3 | 3 → 1 |
| Reconhecimento por feito | 3 → 3 | 2 → 2 | 3 → 0 |
| Proteção prestada | 0 → 0 | 0 → 2 | 0 → 0 |
| Conforto prestado | 2 → 0 | 2 → 0 | 0 → 0 |

Há mais buscas e encontros, mas luto, reconhecimento e conforto não cresceram conjuntamente. Esses mecanismos já existiam; a correção cria mais oportunidades para alguns deles, sem acrescentar novos temas por decreto.

# Histórias emergentes observadas

Leitura das três campanhas corrigidas, com 10.000 horas cada. Os turnos abaixo são os turnos absolutos do mundo: a auditoria começou no turno 24. IDs identificam pessoas dentro da campanha indicada; resultados de campanhas diferentes não devem ser misturados.

As evidências selecionadas estão em [historias_evidencias.json](</home/hugo/Área de trabalho/procedrual/reports/correcao_alimentar/historias_evidencias.json>). O catálogo contém eventos originais, conhecimento antes da ação, necessidades, resultados, relações e estados finais. Relações de confiança ali são valores finais; os valores de parentesco citados também aparecem no contexto das necessidades durante os episódios. “Sucesso” de uma ação significa execução aceita pelo motor: uma procura que não encontrou ninguém também pode ter sido executada com sucesso.

## S01 — Marie tenta ajudar Lyra, denuncia seus crimes e acaba encontrando os restos

**Campanha jogador.** Marie Luar **77**, cozinheiro; Lyra Luar **74**, agricultor; John Montes **91**, guarda. Marie e Lyra têm casamento de valor **94**. O jogador não intervém nesta cadeia registrada.

No turno **46**, Marie percebe a privação de Lyra: `FamilyConcern 10487`, necessidade familiar de cuidado, recurso comida. Marie conhece diretamente esse fato, confiança 100. A primeira tentativa de pedir ajuda falha porque o interlocutor não conhece informação útil. Portanto, o cuidado existe como intenção, mas não há provisão comprovada nessa tentativa.

Lyra rouba recursos da cidade. Marie conserva conhecimento de crimes e desenvolve proteção pessoal. Uma denúncia no turno **106**, ligada ao crime **14464**, falha. Outra, no turno **118**, transmite o crime **21346**, ocorrido no turno 115, ao guarda John: `InformationShared 21822` e `ThreatReported 21823`. A evidência estava conhecida antes da decisão, confiança 100. O guarda responde a Lyra no turno **120**, evento **22173**. A resposta local está registrada; o catálogo não demonstra que esse evento específico foi causado exclusivamente pela denúncia de Marie.

No turno **155**, surge outro cuidado familiar, evento **28609**. Marie coleta alimento no **160** e procura Lyra no **166**. O encontro **30885** confirma Lyra com fome 100, sede 62 e HP 96. Coletar para o objetivo familiar não comprova que a ração foi entregue: não há `HelpGiven` nessa sequência selecionada.

Lyra morre no turno **198** por **sede**, com fome 62 e sem comida. O registro da morte informa última refeição no turno 197. Marie investiga no **202** um crime anterior, **24539**, cometido por Lyra no turno 133. A necessidade selecionada é **vingança/reparação pelo crime contra a cidade**, não busca de familiar desaparecido. Durante a investigação, encontra os restos: **38086**, seguido de `InvestigationPerformed 38088`.

Essa descoberta cria luto familiar. No turno **208**, Marie executa `remember_relative`: `Remembrance 39312`, fonte explícita **38086**, parentesco 94, conhecimento direto 100. Marie permanece viva ao final, HP 98, fome 44.

**Cadeia comprovada:** privação conhecida → cuidado; crime conhecido → proteção/denúncia e investigação; descoberta dos restos durante a investigação → conhecimento da perda → luto → visita de lembrança. É o melhor exemplo de objetivos familiares e sociais coexistindo. O sistema não possui uma emoção completa de “conflito de lealdades”, mas as decisões efetivamente envolvem ajudar e denunciar a mesma pessoa.

## S02 — Lyra Valerius assume o reino e continua procurando Bela

**Campanha espectador, autônoma.** Silas Valerius **1452**, governante; Bela Valerius **1455**, conselheiro; Lyra Valerius **1458**, estudante. Silas e Bela têm casamento 90; ambos possuem relação parental 100 com Lyra. Os dados usam `pai_de`/`filho_de` sem um campo suficiente para deduzir o gênero dos personagens.

Silas morre por fome no turno **430**, evento **83444**. A sucessão **83445**, no mesmo turno, coloca Lyra na referência de governante do reino **1209**. Sua profissão registrada continua estudante: posição política e profissão são campos diferentes. Isso é sucessão simples, já existente, sem uma disputa dinástica nova.

Lyra percebe a ausência de Bela no turno **485**, evento **94161**, usando a última observação de **329**. Procura no **491**, `FamilySearch 95157`, sem localizar Bela. No **548**, encontra Bela com fome 60, sede 63 e **1 HP**: evento **105966**. A necessidade é familiar, modo `missing`; não há consulta à localização global da pessoa.

No **1097**, outra ausência é percebida, **201247**, última observação **1061**. A busca **209637**, no **1148**, ainda não encontra Bela. O encontro **211206**, no **1157**, confirma fome 100, sede 66 e HP 4. Bela finalmente morre por fome no **1689**, evento **299125**, sem comida. Lyra está viva ao final, HP 100, fome 78.

**Cadeia:** morte do governante → sucessão; observações familiares envelhecidas → ausência percebida → buscas → encontros que confirmam fragilidade. A morte final de Bela é conhecida pelo auditor; não atribuo a Lyra conhecimento dessa morte sem um fato correspondente. Na campanha antiga, Bela morreu no turno 242 carregando comida. Agora vive até 1689 e morre sem alimento. Essa diferença pertence ao conjunto da correção e de suas consequências, não a um experimento que isole uma única regra.

## S03 — Uma ausência real produz 54 horas de procura

**Campanha mundo, autônoma.** Lyra Douran **254**, agricultor, e Marie Douran **257**, cozinheiro, casamento **100**.

No turno **469**, Lyra percebe que não vê Marie desde **433**: `AbsenceNoticed 87191`. Isso cria uma necessidade familiar de busca com localização previamente conhecida. Lyra procura no **517**, evento **95738**, mas não encontra Marie. No **523**, encontra a pessoa: **96790**, HP 100, fome 76, sede 57. O fato da ausência estava conhecido com confiança 100 antes das duas ações.

**Cadeia:** ausência baseada em observação → necessidade de localizar familiar → busca sem resultado → reencontro confirmado. Dura **54 horas** desde a percepção até o encontro. Não existe evidência de sequestro, fuga deliberada ou aventura fora da cidade.

Marie segue viva no final, HP 100, fome 82. Lyra morre muito depois, no turno **7603**, por sede. Essa morte posterior encerra sua trajetória, mas não apaga o desfecho bem-sucedido da busca anterior nem prova que Marie soube da perda. É uma história pequena, independente de uma tarefa de obter comida, embora continue vivendo num mundo sujeito à privação.

## S04 — Duas pessoas reagem de maneira diferente ao mesmo crime

**Campanha espectador, autônoma.** Aldren Douran **1597**, guarda, rouba a cidade **1574** no turno **84**, `ItemStolen 16126`. Elena Vale **1595**, comerciante, e John Vale **1592**, lenhador, desenvolvem necessidades de vingança/reparação referentes ao mesmo crime. Elena e John possuem amizade registrada; as relações de confiança mudam ao longo da campanha.

Elena investiga no turno **154**. Conhece o crime diretamente, confiança **100**, e procura no local conhecido. `PersonLocated 28377` encontra Aldren; `InvestigationPerformed 28378` registra investigação sem confronto. No **160**, Elena tenta pedir mais informação e falha. Nesse segundo momento, o fato original já não aparece em seu conhecimento capturado, embora a necessidade ainda o referencie.

John tenta denunciar no turno **175**, com o fato original conhecido por rumor, confiança **30**. A tentativa falha com a mensagem “Faltam informante, guarda presente ou evidência conhecida”. Esse resultado não permite escolher uma dessas condições como causa exclusiva. No **181**, pedir ajuda também falha por falta de informação útil.

**Cadeia:** mesmo crime → conhecimentos com qualidade diferente → investigação bem-sucedida de Elena e denúncia malsucedida de John. Coragem/vingatividade também diferem: Elena 40/85, John 62/81. Isso comprova reações diferentes, mas não prova que a personalidade sozinha causou a diferença; conhecimento, posição e momento também participam. Os três seguem vivos no final. Não houve vingança física nem punição final demonstrada nesse recorte.

## S05 — Uma denúncia chega ao próprio guarda suspeito

**Campanha jogador, episódio autônomo.** Elena **1595** e o guarda Aldren **1597** reaparecem nesta campanha, com outros acontecimentos.

No turno **5406**, Aldren comete o crime **879781** contra a cidade 1574. Elena conhece o fato diretamente, confiança 100, e seleciona `denounce` por necessidade de vingança. No **5428**, **883259** transmite o crime e **883260** registra a denúncia. O destinatário de ambos é **1597**, o próprio Aldren.

**Cadeia:** crime conhecido → reparação → escolha de guarda presente → denúncia ao suspeito. A ação funciona tecnicamente, mas o alvo social é incoerente para uma denúncia que deveria procurar investigação independente. Os dois permanecem vivos. Não há resultado que demonstre punição.

Este é um **bug social remanescente**, não uma história de justiça bem-sucedida. A escolha de autoridade não exclui adequadamente o próprio culpado. Não alterei esse sistema durante a correção alimentar.

## S06 — O interlocutor repete informação anterior à própria ausência

**Campanha jogador, episódio autônomo.** Arthus Luar **41**, cozinheiro; Iria Luar **38**, agricultor, casamento 94; Marie Stone **44**, guarda, interlocutor conhecido.

Arthus já havia localizado Iria no turno **328**, evento **63306**. No **400**, percebe uma nova ausência, **77503**, pois a última observação é do **364**. A busca no **405**, **78420**, não encontra Iria.

Arthus pede informação a Marie. Nos turnos **406**, **407**, **418** e **419**, ocorrem **78608**, **78815**, **80984** e **81150**. Todos transmitem o mesmo fato **63306**, do turno 328, anterior tanto à última observação quanto à ausência atual. As ações retornam “Informação transmitida”, mas o registro da necessidade no turno 419 continua sendo busca, com `searched=True` e bloqueio por falta de solução já observado.

**Cadeia:** nova ausência → procura → pedidos de informação → repetição de fato antigo sem avanço demonstrado. A troca é real; a utilidade para essa procura é insuficiente. O registro persistente de reputação impede reaplicar indefinidamente o mesmo favor, mas não impede o diálogo repetitivo. Arthus e Iria estão vivos ao final. Não afirmo que a ausência ficou sem solução durante os 10.000 turnos: o problema demonstrado está nesse episódio.

## S07 — Cael quer reconhecimento e seu trabalho muda a reputação

**Campanha jogador, episódio autônomo.** Cael Hammer **687**, comerciante; Bela Douran **684**, lenhador, referência da necessidade de reconhecimento. Não há evidência para chamar Bela de monarca ou conceder a Cael um título político.

Um encontro no turno **4508** é a fonte `encounter:684:4508` da necessidade `status`. O contexto pede **um feito**, `deeds_target=1`. Após concorrência com outras prioridades, Cael trabalha no turno **4652**, 144 horas depois: `ResponsibilityFulfilled 762383`.

Elena Luar **675**, Lyra Kars **678**, Bela e Cael conhecem o evento diretamente, confiança 100. O estado persistente de Bela contém o impacto do fato sobre Cael: etiqueta **responsável +4**, confiança adicional **0**. Elena recebe contribuição +2; Lyra, +4. A ação fecha a necessidade de reconhecimento.

**Cadeia:** encontro → desejo de reconhecimento → trabalho observado → fato compartilhado pelos presentes → reputação contextual registrada. É um efeito social comprovado, sem promoção, poder ou mudança de profissão inventados. Cael continua vivo no final, HP 44, fome 68. O desfecho do episódio é reconhecimento local; a fragilidade posterior também permanece visível.

## S08 — Ruan Kars troca de carreira para estabilizar renda

**Campanha espectador, autônoma.** Ruan Kars **1480**, inicialmente lenhador, aprende a cozinhar na cidade **1462**.

A primeira ação de formação capturada no turno **1263** seleciona necessidade **money**, motivo “Estabilizar renda baixa persistente”, meta 20 moedas e 1.200 horas de renda baixa. Não é uma personalidade recém-inventada nem uma ordem do jogador. A oferta local de formação passa pelas regras existentes de observação e disponibilidade.

`TrainingStarted 228807`, no **1263**, exige **34 horas de prática**. Há 14 registros de progresso, que podem contabilizar mais de uma hora de prática por atualização. No **1599**, `ProfessionChanged 284503` altera a profissão de lenhador para cozinheiro; a ação desse turno ainda está ligada à necessidade de renda.

**Cadeia:** dificuldade persistente de renda + oportunidade local → formação produtiva → prática distribuída → mudança de carreira. Foram **336 horas de calendário**, não 336 horas contínuas de aula. Não houve intervenção do jogador. Ruan segue vivo ao final, cozinheiro, HP 100, fome 74. A aquisição de profissão não comprova que deixou de ser pobre definitivamente.

## S09 — Mira Montes abandona dez formações antes de concluir a décima primeira

**Campanha espectador, autônoma.** Mira Montes **915**, mineiro, aprende a ser cozinheiro na cidade **900**.

O primeiro `TrainingStarted`, **130575**, acontece no turno **685**, com requisito **35 horas de prática**. A ação inicial está ligada a **food**, fome 92: a formação também podia ser um caminho legítimo de obtenção de recursos. No turno 4478, outra retomada está ligada a **money**. A trajetória não preserva uma única motivação imutável.

Os inícios são **685, 1107, 1801, 2186, 2522, 2719, 3044, 3578, 4028, 4478 e 5180**. Os abandonos são **1100, 1368, 2132, 2360, 2696, 2966, 3524, 3915, 4404 e 4917**. O catálogo conserva os 108 eventos do recorte: 11 inícios, 10 abandonos, 86 registros de progresso e a mudança de profissão.

No turno **5719**, `ProfessionChanged 924221` finalmente registra cozinheiro. Da primeira tentativa à conclusão passam **5.034 horas**, aproximadamente **210 dias**. A regra antiga encerra formação após mais de 168 horas sem prática, perdendo o progresso daquela tentativa. O log prova as interrupções; não prova que cada abandono teve exatamente a fome como causa.

**Cadeia:** oportunidade → prática → lacuna → abandono → nova tentativa, repetida dez vezes → conclusão. Existe continuidade longa do mesmo personagem, mas o conteúdo é bastante repetitivo. Mira termina viva, HP 92, fome 100. O sistema produziu uma trajetória identificável; ainda não produziu uma biografia rica em decisões profissionais variadas.

## S10 — Bela Solaris sai da população abstrata e se torna cozinheiro

**Campanha mundo, autônoma.** Bela Solaris **152312**, origem registrada “Habitante abstrato de Valria”, cidade **342**. Não possui parentesco gerado nesta materialização.

No turno **864**, `WorkerMaterialized 152314` registra conversão de um habitante abstrato em personagem persistente, após **72 horas de vaga**; o contingente abstrato restante é **414**. `TrainingStarted 152315`, no mesmo turno, exige **24 horas de prática**. É o mecanismo limitado da Fase 3, preservado nesta correção, com condições locais de recursos e contratação.

No **865**, a ação capturada seleciona **advancement**, domínio riqueza, meta 29 moedas. Já no **961**, a ação final de treinamento está ligada a **food**. O objetivo econômico e a sobrevivência podem utilizar a mesma atividade produtiva. `ProfessionChanged 167776`, no **961**, registra a conclusão após **97 horas de calendário**.

**Cadeia:** falta profissional persistente → conversão de residente existente → aprendizagem produtiva → profissão permanente. Não é nascimento, imigração nem cópia de um personagem morto. Bela permanece viva ao final, cozinheiro, HP 100, fome 80. É um exemplo de recuperação de capacidade local limitada, sem garantir recuperação econômica completa da cidade.

## S11 — O jogador aceita uma missão de água e não a conclui

**Campanha jogador.** Iria Luar **38**, agricultor; Arthus Luar **41**, cozinheiro, casamento 94; jogador Auditor **7676**.

Iria percebe privação de Arthus no turno **9512**, evento **1507116**. Na conversa do turno **9514**, cria pedido ao jogador: `HelpRequested 1507428`, quest **1507427**, tipo `family_care`, recurso exigido **water**, destinatário **41**, localização conhecida no contexto.

O comando `conversar 38` avança **9514→9515** e oferece o pedido. `aceitar 1507427` avança **9515→9516**. Depois o controlador automático do jogador continua com outras ações. Não há comando de entrega durante o intervalo ativo. `esperar 1`, de **9560→9561**, registra a quest como **failed**.

**Cadeia:** observação familiar → cuidado → pedido por conversa → aceitação do jogador → ausência de entrega → expiração. Iria e Arthus continuam vivos ao final, HP 100. Portanto, não há “família salva pela quest”. Há mudança real causada pela aceitação e pelo não cumprimento, com consequência formal de falha.

A política de teste foi preservada para comparação; ela reage melhor a pedidos simples de comida do que a essa tarefa familiar de água. Isso limita a qualidade da atuação do jogador automático. Não é um bug do jogo a missão exigir água e expirar sem entrega.

## S12 — Uma ração entregue pelo jogador é consumida na hora seguinte

**Campanha jogador.** Auditor **7676** entrega comida ao comerciante Arthus Valerius **24** no turno **100**: `HelpGiven 18732`, urgência 62.

A instrumentação registra `FoodAcquired` no mesmo turno, HP **90**, fome **62**, inventário após entrega **1 ração**. No **101**, `FoodConsumed` registra a mesma aquisição, `acquired_turn=100`, fome antes de comer **64**, HP 90, inventário após consumo **0**. Assim, o item recebido foi de fato utilizado: receber alimento e comer são consequências distintas.

Arthus conhece diretamente a ajuda. Seu registro persistente do fato atribui ao jogador **prestativo +6** e confiança **+5**. Arthus continua vivo ao final, HP 88, fome 62.

**Cadeia:** decisão pública de entregar → transferência real → posse → consumo posterior → efeito social persistente. É uma intervenção comprovada do jogador. Não podemos dizer que ela evitou uma morte certa: Arthus tinha 90 HP. O resultado interessante é a coerência entre ajuda, consumo e reputação, sem necessidade de criar uma catástrofe artificial.

## Avaliação da qualidade deste material

Os casos S01–S10 mostram decisões de NPCs sem intervenção direta do jogador nos encadeamentos apresentados; quatro deles vêm da campanha espectador e dois do mundo sem jogador. S11 e S12 têm intervenção pública registrada. S02 e S03 permitem acompanhar personagens por longos intervalos; S09 possui a trajetória profissional mais longa selecionada. S01 encadeia necessidades diferentes com fontes identificadas.

Busca familiar, reconhecimento e parte das mudanças profissionais possuem objetivos próprios além da sobrevivência. Entretanto, crimes, cuidado, perdas e formação frequentemente continuam ligados à comida ou à renda. Não classifico qualquer necessidade social como uma história economicamente independente.

Há material suficiente para estes **12 casos**, incluindo dois casos de incoerência social e uma quest fracassada. O conjunto não justifica afirmar que já existem grandes guerras, aventuras épicas, religião ativa ou relações emocionais profundas. O melhor resultado é continuidade causal local; as principais limitações são repetição, pouca transformação das relações e conclusões sociais curtas.

## Diversidade narrativa

Utilizo **10 famílias temáticas explícitas**, agrupadas manualmente: cuidado/provisão familiar; ausência e procura; crime/denúncia/investigação/reparação; proteção/evitação; descoberta de morte e luto; troca de informação; reconhecimento/reputação; profissão/formação/abandono; ambição econômica; sucessão. Quests são um meio de intervenção dentro desses temas, não automaticamente um tema adicional. Afinidades e amizade existem no grafo, mas não encontrei uma cadeia robusta de conforto/amparo entre amigos nestes testes novos.

O extrator automático agrupa ações pelo NPC, necessidade e fonte causal atual. Ele liga o fato de origem e os eventos compatíveis emitidos nas ações. Os números abaixo são **episódios de reação local**, não romances completos. Não incluem formação/sucessão nessa contagem, podem incluir repetição de informação e não equivalem a uma medida de originalidade.

| Episódios e continuidade | Jogador Dovha | Espectador Dovha | Mundo Mira |
| --- | --- | --- | --- |
| Episódios pessoais com ação | 4.615 | 4.864 | 4.429 |
| Com exatamente 2 eventos registrados | 2.612 | 2.784 | 2.604 |
| Com exatamente 3 eventos registrados | 218 | 232 | 173 |
| Com 4 ou mais eventos registrados | 29 | 19 | 18 |
| Duração ≥168 horas desde o fato atual | 27 | 14 | 8 |
| NPCs com ações pessoais separadas por ≥720h | 165 | 165 | 147 |
| Episódios cujo núcleo não é cuidado alimentar | 1.046 | 1.200 | 1.259 |

As cadeias de 2/3/4+ eventos estão vinculadas à mesma necessidade/fonte e às ações registradas; não assumo que todos os pares de eventos sucessivos causaram um ao outro. A validação manual dos 12 casos distingue encadeamento comprovado, acontecimentos paralelos e tentativa que não avançou. Exemplo: a resposta do guarda em S01 não foi tratada como efeito exclusivo comprovado da denúncia; a descoberta dos restos é fonte explícita do luto seguinte.

Contagens com duração longa usam o turno do **fato causal atual**, pois um crime novo pode atualizar uma necessidade antiga sem trocar seu `created_at`. Usar apenas a idade da necessidade inflaria duração de histórias. A trajetória de um NPC por 720 horas também pode ser uma sucessão de rotinas pequenas, sem uma saga contínua.

Os modos espectador/mundo são totalmente autônomos. Nos casos selecionados, S01–S10 têm cadeias sem intervenção direta do jogador; S11/S12 têm participação comprovada. O jogador fez 27 entregas de comida na campanha, uma quest foi aceita e falhou. Entregas não equivalem a 27 vidas salvas nem a 27 histórias distintas.

O mundo continua produzindo histórias além de obter comida. A variedade já existe em alguns objetivos, mas continua estreita: há **zero ComfortGiven**, somente **2 ProtectionGiven**, **6 Remembrance** e **5 ResponsibilityFulfilled** entre as três campanhas novas. Muitas origens continuam sendo roubo de alimento, cuidado de privação e morte. Há mais oportunidade social; não há evidência suficiente para dizer que o mundo já saiu da predominância de sobrevivência.

Dados e método: [diversidade_narrativa.json](</home/hugo/Área de trabalho/procedrual/reports/correcao_alimentar/diversidade_narrativa.json>), [episódios jogador](</home/hugo/Área de trabalho/procedrual/reports/correcao_alimentar/auditorias/jogador/episodios_narrativos.json>), [episódios espectador](</home/hugo/Área de trabalho/procedrual/reports/correcao_alimentar/auditorias/espectador/episodios_narrativos.json>), [episódios mundo](</home/hugo/Área de trabalho/procedrual/reports/correcao_alimentar/auditorias/mundo/episodios_narrativos.json>).

## Limitações

- São duas seeds e três campanhas, sem pretensão de representar todas as populações possíveis. Há regressões causais específicas, mas não uma garantia matemática de ausência de bugs em todo mundo gerado.
- A reserva tem alvo e ações legítimas, porém baixa cobertura real; as buscas e refeições ainda são tardias na maioria dos eventos observados. A prevenção não deve ser anunciada como resolvida em escala populacional.
- Não há reconstrução completa das causas econômicas de cada morte remanescente. A análise terminal diferencia falta de dinheiro conhecido, estado e caminho rejeitado; não inventa estoque no instante exato.
- A estimativa temporal é local e pequena; não conhece todos os desvios de navegação, mudanças de bioma, ações de terceiros e cotações futuras.
- Um objetivo suspenso é guardado por personagem; não há uma pilha ilimitada de interrupções. A retomada exige validade, sem recuperar automaticamente um objetivo expirado.
- Médias temporais dependem de lotes consumidos e da composição de sobreviventes. A fila de carimbos tem limite, coalescendo lotes se ultrapassar 16 entradas; essa marca fica registrada. Não trate uma fila coalescida como datas individuais exatas.
- Logs narrativos preservam fatos e ações; o sistema atual não modela emoções profundas ou uma intenção contínua de décadas. Uma descrição literária mais rica não seria evidência de simulação mais rica.

## Bugs e inconsistências ainda existentes

**Denúncia dirigida ao culpado que também é guarda.** Confirmada em S05. A solução encontra autoridade pela profissão/presença sem excluir adequadamente o suspeito. Deve distinguir investigação independente e conflito de interesse; não está corrigida nesta etapa alimentar.

**Informação velha repetida sem utilidade para a necessidade atual.** Confirmada em S06. A ação retorna sucesso de comunicação, mas repassa fato anterior à última observação, sem fechar a busca. Deve avaliar novidade temporal, utilidade e tentativas repetidas.

**Necessidade persistente e evidência podem perder sincronia.** Em S04, Elena ainda tem a necessidade relacionada ao crime no turno 160, mas o fato original já não aparece no conhecimento capturado. A execução respeita conhecimento e pode falhar; a escolha deveria reconhecer melhor quando precisa recuperar a evidência. O fracasso de John no 175 não foi atribuído indevidamente a esquecimento: ele ainda conhecia rumor do crime.

**Prevenção alimentar pouco efetiva e procura repetidamente tardia.** Confirmada pela distribuição e cobertura, apesar de regressões de manutenção funcionando. É uma limitação comportamental observada que merece análise de prioridades/continuidade por pessoa. Não há prova de que simplesmente aumentar prioridade seja suficiente ou que toda ocorrência seja erro, pois acesso real pode impedir a reserva.

**Formação perde todo o progresso após lacuna e pode repetir muitos inícios.** Confirmada em S09, consequência da regra existente. É uma fragilidade de continuidade profissional, não um novo defeito de consumo. Onze tentativas para a mesma profissão produzem extensão temporal sem diversidade equivalente.

**Métricas agregadas de sucesso podem esconder ausência de transformação.** Ação de procurar pode ser aceita sem achar pessoa; informação pode ser transmitida sem ajudar; necessidade pode ser satisfeita sem uma saga concluída. O relatório distingue essas situações, mas uma interface que mostre só “sucesso” pode induzir leitura exagerada.

**Controlador de jogador não atende bem a quest familiar de água.** S11 comprova a falha da política de auditoria; não considero a expiração sem entrega um bug de quest. Testes futuros devem incluir uma política que execute o recurso/destinatário corretos e preserve uma comparação separada com a política antiga.

Não encontrei nos três testes longos a recorrência dos cinco bloqueios alimentares principais: trabalhar tendo refeição vital, descanso vencendo por ID, preparo sobrepondo alimento vital, viagem mantendo bloqueio vital, ou adquirir ração e morrer esperando outra decisão. Os cenários controlados também exercitam essas situações. Isso não elimina os limites de prevenção e economia descritos acima.

## Recomendações para a próxima fase

1. **Tratar o bloqueio aquisição→consumo e a interrupção vital como base testada.** Manter as 25 regressões novas como proteção ao acrescentar outros sistemas.
2. **Revisar a prevenção com evidência por trajetória antes de declarar prontidão populacional.** Separar dinheiro insuficiente, oportunidade que existia mas perdeu prioridade, objetivo persistente que adiou reposição e rota longa. Testar mudanças pequenas, sem colocar toda manutenção acima da família e sem criar comida/dinheiro.
3. **Projetar acesso econômico usando a comida que existe.** A necessidade seguinte é fazer renda, estoque local, preço e distribuição produzirem caminhos reais para pobres. Mais produção agregada por si só não resolve as 209 mortes sem dinheiro para a cotação conhecida. Essa frase é uma recomendação de escopo futuro, não implementação de economia ampla agora.
4. **Corrigir as duas incoerências sociais confirmadas.** Seleção de autoridade e utilidade temporal da informação são alterações locais que podem melhorar narrativas sem inventar novos sistemas grandes.
5. **Reavaliar continuidade de formação separadamente.** Perder todo o progresso após uma lacuna pode manter uma pessoa em ciclos repetidos. Qualquer nova regra deve conservar custos, prática real e condições locais, comparando consequências.
6. **Avaliar a próxima etapa por qualidade causal e diversidade, além de mortalidade.** Medir reserva efetiva, busca antes da fome alta, famílias reencontradas, fatos úteis, reputação transformada, carreiras concluídas e proporção de cadeias cuja origem não é privação.

A correção alimentar executada oferece uma base de consumo e emergência mais coerente e auditável. **Ainda não considero resolvida a meta de alimentação amplamente preventiva nem o predomínio de sobrevivência nas histórias.** A Fase 4 não foi iniciada; esses limites estão registrados para decidir seu escopo a partir dos resultados reais.

## Arquivos para leitura e reprodução

- [Jogador Dovha — save final](</home/hugo/Área de trabalho/procedrual/reports/correcao_alimentar/auditorias/jogador/save_final.json>); [relatório bruto](</home/hugo/Área de trabalho/procedrual/reports/correcao_alimentar/auditorias/jogador/relatorio.json>); [alimentação](</home/hugo/Área de trabalho/procedrual/reports/correcao_alimentar/auditorias/jogador/metricas_alimentacao.json>); [eventos narrativos](</home/hugo/Área de trabalho/procedrual/reports/correcao_alimentar/auditorias/jogador/narrativa.jsonl.gz>); [decisões e conhecimento](</home/hugo/Área de trabalho/procedrual/reports/correcao_alimentar/auditorias/jogador/acoes_pessoais.jsonl.gz>). 
- [Espectador Dovha — save final](</home/hugo/Área de trabalho/procedrual/reports/correcao_alimentar/auditorias/espectador/save_final.json>); [relatório bruto](</home/hugo/Área de trabalho/procedrual/reports/correcao_alimentar/auditorias/espectador/relatorio.json>); [alimentação](</home/hugo/Área de trabalho/procedrual/reports/correcao_alimentar/auditorias/espectador/metricas_alimentacao.json>); [eventos narrativos](</home/hugo/Área de trabalho/procedrual/reports/correcao_alimentar/auditorias/espectador/narrativa.jsonl.gz>); [decisões e conhecimento](</home/hugo/Área de trabalho/procedrual/reports/correcao_alimentar/auditorias/espectador/acoes_pessoais.jsonl.gz>). 
- [Mundo Mira — save final](</home/hugo/Área de trabalho/procedrual/reports/correcao_alimentar/auditorias/mundo/save_final.json>); [relatório bruto](</home/hugo/Área de trabalho/procedrual/reports/correcao_alimentar/auditorias/mundo/relatorio.json>); [alimentação](</home/hugo/Área de trabalho/procedrual/reports/correcao_alimentar/auditorias/mundo/metricas_alimentacao.json>); [eventos narrativos](</home/hugo/Área de trabalho/procedrual/reports/correcao_alimentar/auditorias/mundo/narrativa.jsonl.gz>); [decisões e conhecimento](</home/hugo/Área de trabalho/procedrual/reports/correcao_alimentar/auditorias/mundo/acoes_pessoais.jsonl.gz>).

- [12 histórias em arquivo separado](</home/hugo/Área de trabalho/procedrual/reports/correcao_alimentar/HISTORIAS_EMERGENTES.md>) e [catálogo de evidências](</home/hugo/Área de trabalho/procedrual/reports/correcao_alimentar/historias_evidencias.json>).
- [distribuição de procura, rejeição e interrupção](</home/hugo/Área de trabalho/procedrual/reports/correcao_alimentar/distribuicao_diagnosticos.json>).
- [diagnóstico histórico anterior](</home/hugo/Área de trabalho/procedrual/RELATORIO_FOME_E_MORTES.md>) e [campanhas originais preservadas](</home/hugo/Área de trabalho/procedrual/reports/fase_3/auditorias>).

Para gerar novas campanhas com as regras congeladas, use um diretório vazio; o auditor recusa sobrescrever resultados:

```bash
python3 -m unittest discover -s tests -v
python3 -m experiments.feeding_audit --mode jogador --turnos 10000 --output reports/correcao_alimentar/nova_jogador
python3 -m experiments.feeding_audit --mode espectador --turnos 10000 --output reports/correcao_alimentar/nova_espectador
python3 -m experiments.feeding_audit --mode mundo --turnos 10000 --output reports/correcao_alimentar/nova_mundo
```

Os scripts `feeding_baseline`, `feeding_comparison`, `feeding_narratives`, `feeding_story_evidence`, `feeding_remaining_deaths`, `feeding_verify` e `feeding_report` preservam o método usado. A reprodução antiga usa o snapshot histórico isolado; scripts diagnósticos antigos que exigem a assinatura do motor anterior devem ser executados com esse código, não com o motor novo esperando o mesmo hash.
