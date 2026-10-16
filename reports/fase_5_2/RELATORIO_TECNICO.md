# Relatório técnico — Fase 5.2

Versão **mvp-10-fase5.2**. Base: `mvp-9-fase5.1`. Seed natural **Eryndal-52**, **500 horas**, sem jogador e sem história simulada anterior. População persistente inicial: **1776**; vivos ao final: **1738**. A população abstrata inicial de 4461 habitantes pertence à economia agregada; as histórias e mortes abaixo são de NPCs persistentes.

**Conclusão:** os mecanismos foram implementados e passaram nos testes selecionados, mas a campanha não demonstrou homicídio deliberado natural nem intervenção divina. Houve decisões e ataques letais, com um bug de escolha terminal e um bug de preservação da evidência encontrados após as 500h. Foram corrigidos e validados em testes controlados; os resultados naturais abaixo pertencem à revisão anterior a esses ajustes. A frequência e a emergência natural dessas consequências permanecem sem comprovação nesta entrega.

## O que mudou

A decisão de matar agora é um estado separado da execução. Fatos conhecidos oferecem o gatilho; personalidade, emoção, compromisso, ruminação e experiência com a morte modificam a resposta; compaixão, vínculo, incerteza, medo e autoridade oferecem inibição. Nenhuma personalidade, por si só, produz uma vítima ou causa.

A redução da barreira é contextual: uma agressão conhecida de 8 HP já pode oferecer ameaça moderada imediata, contra 15 HP anteriormente; dano atribuído não resolvido de 10 HP pode oferecer uma base continuada, contra combinações antigas de 20–35 HP e repetição extrema. Isso disponibiliza a consideração: a decisão ainda compete com conter, repelir, subjugar ou ferir. Dano, variação aleatória, defesa e potência das armas foram preservados.

`LethalDecision` guarda autor, alvo, modo, causa, até três fatos, confiança, momento da decisão, compromisso relacionado, pressões, intensidade, fatores de impulso/inibição e ruminação. Os modos são ameaça reativa, retribuição, proteção, objetivo instrumental, punição moral e busca de violência por trajetória reforçada. A última exige experiência positiva repetida, sadismo elevado, afinidade com a morte e oportunidade conhecida.

Fome, descanso, viagem, ausência do alvo e encerramento do episódio físico não apagam a decisão. Sobrevivência e capacidade continuam interrompendo a execução. Perdão explícito, reparação material pertinente, desculpa aceita, nova prova de inocência, vínculo restaurado, perigo percebido novo ou mudança moral podem encerrá-la. Tempo seguro reduz ruminação; a desistência por essa via depende também de baixa ruminação e menor disposição vingativa. Não há simples prazo de expiração.

Diante da incapacidade real, a ameaça defensiva imediata cai. Finalizar, poupar, capturar, ajudar e retirar-se competem pelo contexto atual; não se repete toda a barreira inicial. Finalizar continua exigindo decisão ativa, presença e capacidade; tem morte certa dentro da abstração. A morte por golpe comum com intenção de matar é registrada separadamente da finalização.

Na revisão entregue, as alternativas terminais usam uma única avaliação contextual; não recebem outra barreira genérica de utilidade. Necessidades vitais ainda podem tomar prioridade. Uma decisão defensiva também pode mudar para retribuição diante de nova agressão conhecida: dano acumulado confirmado de pelo menos 20 HP, agravo de pelo menos 40 e vingatividade de pelo menos 60; ou novo homicídio confirmado de pessoa próxima. A atualização exige fato recebido e produz `LethalDecisionUpdated`.

`PostKillAppraisal` combina culpa, vergonha, medo, alívio, orgulho, prazer, fascinação, insensibilidade, luto e conflito moral, conforme intenção, valores, religião percebida, vínculo, vulnerabilidade e testemunhas. Culpa pode criar interesse religioso. `DeathAffinity` começa em zero; cresce apenas com morte deliberada avaliada positivamente e pode cair com culpa, perda, punição conhecida ou ausência prolongada de reforço. Há até quatro avaliações recentes por matador; o histórico causal continua no save. Não foi criada classe de assassino serial.

Mortes violentas aprendidas podem formar uma hipótese de padrão local. Autoria desconhecida permanece desconhecida. Guardas recebem necessidade de vigilância e maior pressão; relatos locais podem alimentar medo e representação por segurança. Epítetos de padrões anônimos ficam separados do renome de pessoas identificadas. A investigação não consulta a posição atual de suspeitos remotos.

A afinidade divina é dirigida do deus ao mortal e pode ser negativa; devoção continua pertencendo ao mortal. Orações contribuem pouco e possuem teto; feitos relevantes conhecidos têm contribuição maior. Domínio e valores modulam aprovação: a regra para um deus da morte só recompensa homicídio se a doutrina realmente permitir. A cosmologia inicial mantém Aurion, Neruma e Elar; nenhum deus da morte foi acrescentado artificialmente à campanha.

Afinidade extrema e vários feitos podem criar vínculo raro e candidatura a campeão. A candidatura não reconhece automaticamente um campeão. O vínculo transmite apenas sinais graves; um sinal de morte não identifica automaticamente o assassino. Presença divina ocupa regiões físicas numa camada invisível. Não concede visão de tudo: existem oração, observação na localização divina, relato de feito conhecido, relato de congregação e vínculo. Deslocamento de presença custa 25–45 de energia; intervenção custa mais 20 e preserva o intervalo mínimo.

A composição religiosa distingue seguidores, devotos, participantes de culto e agentes que praticaram atos alinhados. Camadas podem se sobrepor; não devem ser somadas como pessoas diferentes. `FaithHealth` mantém até três pontos de tendência, com atualização a cada 24 horas e comparação aproximada de 100 horas. Considera perda de núcleo, perda de favoritos, importância da região e crescimento rival. Queda de massa com núcleo crescente pode permanecer estável. Censo e crise objetivos não entram diretamente na decisão divina: precisam de mensagem recebida.

## Validação e limites do experimento

**18 testes selecionados passaram:** dez novos e oito regressões críticas de conhecimento, combate, recuperação, grupos, fé e persistência. Os dois testes opcionais do documento foram incluídos porque autoria oculta no vínculo e padrão de homicídio são caminhos novos com risco de vazamento de conhecimento. Foram usadas quatro famílias controladas: defesa/decisão/terminal; pós-morte/reforço/padrão; atos religiosos/afinidade; crise/vínculo/presença/intervenção. São provas de capacidade, não histórias naturais. Não houve saves de microcenários nem repetição da suíte antiga inteira.

A primeira tentativa natural foi interrompida cedo, depois do último marco de 50h, para corrigir um erro de alvo na resposta a quase morte de favorito: a punição poderia atingir o protegido. O teste do vínculo agora verifica esse caminho. Houve somente o reinício permitido, **na mesma seed**. A tentativa interrompida não produziu save e não entra nos resultados. O núcleo permaneceu igual durante toda a campanha concluída.

Foram feitas **11 verificações estruturais**, das horas 0 a 500; erros encontrados: **0**. Violações detectadas pela auditoria durante a execução: **0**. Essa auditoria verificava elegibilidade/capacidade e custo/origem, mas não confrontava a escolha terminal final nem procurava referências alteradas retroativamente. Portanto, zero nesse contador não significa ausência de bugs. O save final contém o estado e o histórico original; não há exportação duplicada do histórico bruto.

## Bugs encontrados e ajustes após a campanha

1. **Dupla competição terminal.** Na hora 67, Silas Kars poupou Ruan Alvor (`TerminalDecision #86661`), embora a avaliação terminal favorecesse finalizar: 65,76 contra 46,20 para poupar. A utilidade genérica e os modificadores de agência voltavam a favorecer alternativas depois da avaliação contextual. A entrega retorna somente alternativas terminais para aquela necessidade quando há oportunidade física e usa seus escores diretamente. O teste 04 agora verifica a seleção automática de finalizar/poupar, além da execução.

2. **Modo inicial congelado.** Novas agressões reforçavam fatos e ruminação, mas uma decisão inicialmente defensiva conservava seu modo para sempre. Isso dificultava distinguir perigo cessado de agravo continuado. A entrega permite a mudança condicionada a novos fatos, dano confirmado, agravo e personalidade; não transforma todo combate em vingança. O teste 03 verifica a mudança e o encerramento por perdão próprio.

3. **Evidência histórica mutável.** A decisão e algumas avaliações emitidas compartilhavam a mesma lista de fatos. Reforços posteriores alteravam os registros antigos. A leitura posterior encontrou **467 registros** com referências posteriores ao próprio evento: {'LethalConsideration': 78, 'CharacterAttacked': 389}. Por exemplo, o ataque `#71941` da hora 52 passou a citar agressões das horas 65, 66 e 149. Isso corrompia a documentação histórica; não comprova que o NPC conhecia o futuro quando agiu. Agora decisão, consideração, avaliação de ataque e encerramento preservam listas independentes. O teste 03 verifica que novos fatos modificam a decisão sem modificar as evidências emitidas antes. O auditor também passou a verificar referências futuras.

Esses três ajustes ocorreram **depois** da única campanha concluída. Os 18 testes selecionados foram repetidos após as correções e passaram; não houve segunda campanha, troca de seed, reconstrução de acontecimentos nem edição do save para alterar o resultado. Eventos, causas principais, identidades, horas e decisões iniciais preservadas como valores permitem reconstruir as trajetórias; listas contaminadas da auditoria antiga não são usadas como prova da informação disponível no passado.

A entrega final também registra mudança regional de influência em transições relevantes de saúde religiosa. O relato de congregação pode transportar conversões observadas de membros para uma fé rival; somente a recepção desse relato emite conhecimento divino do crescimento rival. O teste 07 foi ampliado para verificar que o crescimento não é aprendido antes do relato. Essa integração é posterior à campanha, que não teve conversões nem relatos de declínio.

Na revisão final, foi corrigida ainda a trégua ao encerrar um confronto com vários adversários: a decisão do último adversário percorrido podia ser reutilizada para todos os pares. Agora cada par usa sua própria decisão. O teste 03 cobre o encerramento simultâneo com um adversário sem decisão e outro com decisão ativa. É correção de continuidade encontrada na revisão do código, sem contagem retrospectiva de efeitos na campanha.

## Resultados naturais de letalidade

| Indicador | Resultado |
|---|---:|
| Considerações letais registradas | 148 |
| Decisões letais criadas | 147 |
| Decisões com ataque letal | 107 |
| Conversão decisão → ataque | 72.8% |
| Execuções de ataques letais | 632 |
| Oportunidades terminais | 30 |
| Finalizações escolhidas | 0 |
| Decisões explícitas de poupar | 15 |
| Mortes por golpe intencional | 0 |
| Mortes por finalização deliberada | 0 |
| Decisões abandonadas | 30 |
| Decisões resolvidas | 0 |
| Avaliações após matar | 0 |
| Aumentos de afinidade com a morte | 0 |
| Busca de violência criada | 0 |
| Hipóteses de padrão comunicadas | 0 |
| Guardas com necessidade de investigar padrão | 0 |
| Vigilâncias de padrão registradas | 0 |

Consideração aqui é um episódio elegível que venceu a comparação inicial de intenções, não toda consulta rejeitada. Ataques são execuções e podem se repetir pelo mesmo autor/alvo; decisões e pessoas são unidades diferentes. As decisões retidas no estado final podem ser menos numerosas que as criadas porque a memória é limitada.

Foram criadas 147 decisões, das quais 107 levaram a ataque. As 30 oportunidades são registros de episódios, não 30 decisões terminais executadas; apenas 15 terminaram em escolha explícita, todas de poupar. Não se deve atribuir as 15 exclusivamente à compaixão: pelo menos uma foi afetada pelo bug acima. Houve sete capturas no sistema existente, sem demonstrar captura como desfecho da nova competição terminal.

Causas de morte: **{'both': 1, 'hunger': 36, 'thirst': 1}**. Contextos registrados: **{'both': 1, 'hunger': 36, 'thirst': 1}**. Mortes por fome com comida no próprio inventário: **0**. Modos das decisões retidas: `{'reactive_threat': 85, 'retributive': 1, 'protective': 56, 'instrumental': 2}`; estados retidos: `{'active': 117, 'abandoned': 27}`.

## Fé, afinidade e atuação divina

| Indicador | Resultado |
|---|---:|
| DivineMessage | 112 |
| DivineAffinityChanged | 11 |
| DivineBondCreated | 0 |
| FavoredFollowerKilled | 0 |
| ChampionCandidate | 0 |
| ReligiousDeclineReported | 0 |
| DivinePresenceChanged | 0 |
| DivineActionConsidered | 27 |
| DivineIntervention | 0 |

| Deus | Seguidores início → fim | Devotos início → fim | Cultistas finais | Actors finais | Maior afinidade | Energia final |
|---|---:|---:|---:|---:|---:|---:|
| Aurion | 520 → 508 | 189 → 187 | 4 | 404 | 5.04 | 100.0 |
| Neruma | 868 → 848 | 300 → 295 | 8 | 404 | 14.40 | 100.0 |
| Elar | 388 → 382 | 150 → 147 | 3 | 404 | 2.40 | 100.0 |

A tabela de composição usa a hora 500. A última amostragem de saúde religiosa ocorreu na hora 480. Os Actors incluem pessoas que agiram segundo os valores do deus mesmo sem adotarem seu culto.

Os 404 Actors de cada deus são as mesmas pessoas nesta seed: a regra ampla de ajuda e valores compassivos alinha o ato aos três. Isso não representa 1.212 agentes diferentes, nem três núcleos doutrinários distintos. É uma limitação de diferenciação religiosa. Os participantes recentes de culto foram poucos (4/8/3), e ninguém alcançou favorito, vínculo ou candidatura a campeão.

**Aurion**: estado global `CORE_EROSION`; estados regionais retidos `{'CORE_EROSION': 39, 'STABLE': 24, 'MINOR_DECLINE': 12}`. Memória divina final: `{'prayer': 11, 'devoted_report': 5}`; vínculos 0; candidatos a campeão 0. Pressão conhecida final 0.00; disposição para agir 0.00. Esses canais finais descrevem a memória limitada de 16 mensagens, não o total histórico.

**Neruma**: estado global `MINOR_DECLINE`; estados regionais retidos `{'CORE_EROSION': 36, 'MINOR_DECLINE': 20, 'STABLE': 19}`. Memória divina final: `{'devoted_report': 10, 'prayer': 6}`; vínculos 0; candidatos a campeão 0. Pressão conhecida final 0.00; disposição para agir 0.00. Esses canais finais descrevem a memória limitada de 16 mensagens, não o total histórico.

**Elar**: estado global `CORE_EROSION`; estados regionais retidos `{'CORE_EROSION': 40, 'STABLE': 26, 'MINOR_DECLINE': 9}`. Memória divina final: `{'prayer': 6, 'devoted_report': 10}`; vínculos 0; candidatos a campeão 0. Pressão conhecida final 0.00; disposição para agir 0.00. Esses canais finais descrevem a memória limitada de 16 mensagens, não o total histórico.

## Gargalos e alcance da entrega

Os coeficientes são regras de um jogo sombrio, não medições clínicas de pessoas. A implementação usa como inspiração a separação de gatilho/impulso/inibição do [I³ de Finkel e Hall](https://www.sciencedirect.com/science/article/abs/pii/S2352250X17300635), a associação entre sadismo e gratificação agressiva estudada por [Buckels, Jones e Paulhus](https://pubmed.ncbi.nlm.nih.gov/24022650/), e conflitos de valores após causar dano discutidos por [Litz e colaboradores](https://pubmed.ncbi.nlm.nih.gov/19683376/). Os números de dano, culpa e afinidade são decisões de simulação.

A religião ainda tem três domínios iniciais e dogmas compactos; organização completa de cultos, ordens religiosas nacionais, guerra divina e pós-vida estão fora desta fase. A presença é regional para alcance de ação, mas a observação direta ainda usa a localização exata do deus. Para fatos distantes são necessários relatos ou vínculos. O censo cobre NPCs persistentes; não inventa devoção, culto ou biografia para população abstrata.

Padrões anônimos podem ser construídos de relatos de homicídio com autoria desconhecida. A descoberta genérica de restos do sistema anterior ainda confirma morte sem produzir perícia de homicídio ou assinatura forense; não se pode inferir assassinato de todo cadáver. Epítetos anônimos são hipóteses locais. Renome nominal e veneração continuam exigindo conhecimento e transições próprias; não há função que execute uma saga inteira.

Os critérios de retribuição e moralização são compactos. A intenção inicial não equivale a compromisso ininterrupto de atacar: fome, sede, recuperação, distância, rendição e detenção competem de verdade. Estado religioso deteriorado não é motivo suficiente para milagre quando o deus não foi informado. A campanha única avalia possibilidade e coerência; não estima frequência confiável de homicídio, campeão ou vínculo raro.

O combate comum encaminha alvos incapacitados para julgamento terminal antes de simplesmente repetir golpes até zero HP. Assim, muitos ataques com intenção de matar podem terminar em incapacidade, afastamento ou rendição. Das 144 decisões retidas, 141 eram reativas ou protetoras; só uma era retributiva e duas instrumentais. Essa composição, o modo inicial congelado e a dupla utilidade terminal ajudam a explicar a ausência de mortes deliberadas. A única divergência terminal demonstrada é a de Silas; não se pode atribuir todos os desfechos ao mesmo bug nem calcular o resultado de uma campanha corrigida sem executá-la.

Grupos, propostas, autoridades e facções preservaram a arquitetura anterior. Nesta fase receberam integração local do medo de homicídios; a baixa agência natural de facções continua dependendo de recursos, membros, ideologia e informação. Não foram adicionados membros, salários ou provisões artificiais para fazê-las agir.

Na seed, as duas facções terminaram com um membro cada e nenhuma ação organizacional nova registrada. Houve 87 submissões de propostas e 66 decisões políticas, mas apenas dois repasses de resposta à comunidade. O grupo de Nora Corven ainda desconhecia no final a resposta parcial à segunda proposta, apesar de a autoridade já tê-la decidido: comunicação incompleta, sem ciência instantânea do grupo.

O governante Eryndal-52 conservou o trono e terminou com objetivo de roubar alimento e apenas duas moedas próprias. A renda individual de autoridades ainda não representa o acesso ao tesouro ou abastecimento institucional. Esse desencaixe anterior à Fase 5.2 merece atenção: autoridade política e acesso econômico pessoal continuam pouco ligados. As 38 mortes foram por privação (36 por fome, uma por sede e uma por ambas); ausência de alimento no inventário não esclarece sozinha todo o acesso físico/econômico disponível no mundo.

Para avaliar o critério de sucesso do documento: persistência, escolha contextual, aprendizagem pós-morte, trajetória reforçada, reação dos guardas, vínculo, crise conhecida e custos divinos foram demonstrados nos testes controlados. Na campanha natural foram demonstradas decisões fundamentadas, continuidade, combate, favor por feitos e diferenciação entre crise objetiva e informação divina. **Homicídio deliberado natural, consequências sociais desse homicídio, trajetória recorrente e intervenção divina natural não foram demonstrados.** O ajuste final remove um bloqueio real, mas não permite afirmar que a mortalidade natural já foi calibrada.

## Custo e rastreabilidade

Inventário da entrega: **30 arquivos novos**, cerca de **186.34MiB**, dos quais 184,51MiB são o único save. São oito fontes novas (cinco módulos, testes e dois auxiliares) e 15 fontes existentes alteradas; as alterações estão no patch. O inventário lista o tamanho individual de cada arquivo e inclui os próprios relatórios, logs, patches e metadados.

Tempo total da campanha concluída, incluindo geração e exportação: **500.23s** (8.34min). Exportação: **16.08s**. Pico de memória incluindo serialização: **1576.46MiB**. Save: **193,476,682 bytes** (184.51MiB); histórico interno: 90,808 eventos. A tentativa interrompida e os testes têm custo adicional e não estão incluídos nesse tempo.

SHA-256 do núcleo da campanha: `093296adf05b5c4c06a5289306f6370866f53e2ad259c7083662ff88c94a6635`. SHA-256 do núcleo entregue e validado pelos 18 testes: `2807d4adfb1157ae0fdb8fb2210671b28f9a3d4b688de665e3f9c49843750cbe`. O save pertence à primeira revisão; seu esquema permanece compatível, e uma continuação usa as regras corrigidas, sem apagar os defeitos históricos já gravados. O hash do save está em `campanha_500h/save_sha256.txt`. `ALTERACOES.patch` compara a entrega inteira com a base; `AJUSTES_APOS_CAMPANHA.patch` isola os ajustes finais do motor e testes. Os patches foram verificados com aplicação reversa em modo seco. Não foram criadas cópias completas da base/entrega. O inventário final de arquivos e tamanhos fica em `tamanho_arquivos.json`.

Arquivos centrais: `procedural/lethal_decisions.py`, `aftermath.py`, `divine_relations.py`, `religious_health.py`, `violence_patterns.py`, com integração em modelos, necessidades, agência, pressão, combate, fé, sociedade, motor e validação. Execução de uma campanha com as regras entregues: `python3 -m experiments.phase52_audit --seed Eryndal-52 --folder PASTA_VAZIA`. É instrução para execução futura: para reproduzir exatamente a revisão da campanha registrada, é necessário também reverter os ajustes posteriores numa cópia adequada; a entrega executou uma campanha concluída.
