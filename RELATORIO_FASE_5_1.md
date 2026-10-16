# Fase 5.1 — agência, pressão e continuidade

**Entrega:** `mvp-9-fase5.1`, baseada na entrega da Fase 5. O documento recebido está preservado integralmente em [fase_5_1.md](</home/hugo/Área de trabalho/procedrual/fase_5_1.md>).

O avanço natural mais claro foi a representação política: **134 entregas de propostas e 59 decisões em 1.000 horas**. A agência geral continua limitada: só **6,97% dos compromissos examinados registraram progresso nas ações de continuidade**. Facções e deuses funcionaram nos cenários controlados, mas permaneceram sem ações organizacionais/intervenções naturais. A sobrevivência continua sendo um problema: **182 mortes por fome**.

## O que foi implementado

| Parte | Comportamento entregue | Alcance demonstrado |
|---|---|---|
| WorldPressure | Causa conhecida e gravidade examinadas antes da Utility; personalidade não fabrica uma causa grave | Testes de ausência de causa, danos leves, relatos incertos e perda próxima |
| ActionPressure | Estado contextual por interesse, modificado por persistência, agência percebida, compromisso, falhas relacionadas e barreiras | Máximo de oito registros por NPC, com retenção estável; não é traço permanente |
| Capacidade | Separação entre vontade, capacidade física e capacidade percebida; execução forte revalida incapacidade | Ataque com intenção letal também passa pelo filtro; desejo pode permanecer sem ataque |
| Continuidade de grupos | Encontros planejados, representante, entrega, leitura, retorno físico e reação a resposta recebida | Caminho vila → cidade apareceu naturalmente e passou no teste completo de ida/volta |
| Escalada e resolução | Recusas conhecidas aumentam iniciativa; alívio material e resolução reduzem pressão; resposta antiga não é reaplicada | Protesto natural; escalada e desescalada controladas. Não implementa toda a cadeia boicote → sabotagem → revolução |
| Facções | Recrutamento, preparação com recursos próprios, serviço conhecido e incursão pequena com suprimentos, presença e permissão ideológica | Capacidade e raid provados em condições controladas; zero ocorrência natural |
| Fé e deuses | Difusão cultural com confiança limitada, influência local auditável, percepção por declarações/relatos recebidos e resposta divina custeada | Perda conhecida pode oferecer ação sem nova oração; perda remota desconhecida e oração isolada não bastam |
| Letalidade | Desejo letal preservado; ação exige causa grave atribuída ao alvo atual, disposição e capacidade | Resposta situacional e persistente preservadas nos testes; seis autores atacaram com intenção letal naturalmente |

Não foram acrescentados panteões, frequência maior de MythicTraits, guerras nacionais, conquista, sistema geracional ou um botão de destruir vilas. A incursão implementada envolve roubo limitado ou combate presencial com guardas; não simula cerco nem destruição de estruturas. A influência religiosa é parcial: há crenças locais e conhecimento recebido pelo deus, sem competição territorial completa ou onisciência.

## Campanha e conversão em ação

**Seed Selvaren-51**, mundo novo, observador sem jogador, sem histórico anterior e sem carregar save. Começou com **1.744 NPCs persistentes, 4.387 habitantes abstratos, 75 localidades, duas facções, três deuses e cinco potenciais míticos**. O marco de 200h é o começo da mesma campanha que continuou até 1.000h; não foram 1.200h nem duas seeds. Só existe um save final.

| Medida acumulada | 200h | 1.000h |
|---|---:|---:|
| NPCs vivos | 1.743 | 1.561 |
| Mortes por fome / combate | 1 / 0 | 182 / 1 |
| Compromissos criados nos interesses auditados | 2.112 | 16.418 |
| Compromissos com progresso em ações de continuidade | 176 — 8,33% | 1.144 — 6,97% |
| Execuções bem-sucedidas dessas ações | 3.467 | 14.468 |
| Execuções com consequência registrada | 1.092 | 3.755 |
| Grupos formados / com ação relevante | 259 / 77 | 886 / 128 |
| Propostas criadas / entregas | 179 / 81 | 447 / 134 |
| Entregas por proposta criada | 45,25% | 29,98% |
| Decisões políticas | 38 | 59 |
| Pares resposta–personagem com aprendizado | 57 | 94 |
| Retransmissões presenciais de resposta | 1 | 2 |
| Preparações / ações organizacionais / adesões | 0 / 0 / 0 | 0 / 0 / 0 |
| Orações / avaliações divinas / intervenções | 46 / 372 / 0 | 75 / 931 / 0 |
| Mudanças para intenção de matar / autores | 0 / 0 | 7 / 6 |
| Autores de ataque letal / oportunidades / decisões terminais | 0 / 0 / 0 | 6 / 0 / 0 |

**Como ler:** os compromissos são episódios de intenção duradoura, restritos aos interesses da camada nova. Progresso considera eventos `CommitmentProgress` de ações de continuidade, como aproximação física e avanço social; não significa história concluída. Execuções são contadores de ações, podem repetir-se no mesmo episódio e incluem presença/espera. Consequências filtram movimento e progresso observável; não são consequências sociais duradouras necessariamente. A taxa de compromissos com progresso é a comparação de episódios distintos. Não dividir execuções por NPCs nem tratar os números como probabilidades.

Um contador inicial chamado “intenções” registrava **226.985 criações de cache**, incluindo expulsões e recriações. Ele foi renomeado e separado dos compromissos reais, recuperados do histórico do mesmo save. Também havia **63 avaliações letais elegíveis**, que não são 63 intenções: o histórico contém sete mudanças para `kill`. As correções de telemetria não reexecutaram o mundo.

Das decisões políticas, **35 foram parciais, 11 adiadas, 11 recusadas e duas aprovadas**. Seus efeitos somaram duas unidades de comida e 88 unidades de dinheiro, além dos efeitos de políticas/armamento existentes. Portanto, mais entrega não equivale a resolver a fome. Dos grupos, 603 nasceram por pressão de recursos e 283 por segurança.

Na longa anterior da Fase 5 foram seis entregas e quatro decisões em 5.000h. O resultado atual mostra continuidade mais presente, mas **não é uma comparação controlada**: seed, população, duração e implementação diferem. Não foi feita campanha adicional para escolher uma seed melhor.

## Pressão observada e histórias

Faixas: baixa <25; média 25–<55; alta 55–<80; extrema ≥80. Estado final:

| Agente | Baixa | Média | Alta | Extrema |
|---|---:|---:|---:|---:|
| NPC vivo — maior registro individual | 193 | 1.358 | 10 | 0 |
| Grupo ativo | 1 | 88 | 233 | 0 |
| Facção ativa | 2 | 0 | 0 | 0 |
| Deus vivo | 3 | 0 | 0 | 0 |

Durante as atualizações houve pressão alta em NPCs e grupos, mas nenhuma faixa extrema registrada. Os 233 grupos altos no fim, diante de poucas retransmissões, mostram que **pressão suficiente ainda não garante oportunidade e continuidade suficientes**. Ausência de extremos não prova equilíbrio perfeito; a mortalidade por fome continua alta.

[HISTORIAS_REAIS.md](</home/hugo/Área de trabalho/procedrual/reports/fase_5_1/HISTORIAS_REAIS.md>) reúne **sete episódios reais**, incluindo Darin Luar representando Norlen em Dormir, resposta municipal parcial, retorno presencial de informação, protesto, reação letal após dano recente e uma morte física com intenção de subjugar. Não transforma casos controlados em lore nem inventa desfechos ausentes.

Foram feitas **21 verificações de integridade**, de 0 a 1.000h, sem erros. O exame posterior dos 13 ataques registrados com intenção letal não encontrou falta de causa semântica nem valores abaixo dos novos mínimos de disposição/capacidade. Não houve oportunidades terminais, intervenções, apoteoses ou mortes divinas naturais. Não houve morte por privação com comida carregada, mas isso não demonstra acesso econômico adequado à comida.

## Bugs corrigidos e limites

| Problema encontrado | Correção / evidência |
|---|---|
| Vila sem prefeito não tinha caminho prático de representação | Rota pública conhecida para cidade do mesmo reino; viagem física, sem posição remota do prefeito |
| Representante podia perder relevância durante a viagem | Deslocamento efetivo mantém a representação em andamento; retorno conserva residência |
| Resposta individual não chegava ao grupo | Leitura presencial e retransmissão após encontro; conhecimento de cada membro continua separado |
| Novo fluxo escondia serviço do líder e disputa local de cargo | Restauradas as opções anteriores, com os filtros físicos/causais e políticos |
| Ataque comum com intenção letal escapava do filtro de capacidade | Reproduzido: capacidade 1,33 ainda permitia cinco de dano. Agora bloqueia antes de executar e antes da Utility |
| História de dano incerto podia ser classificada como causa grave | Memória de dano atribuído com confiança suficiente separada da suspeita; teste conserva desejo irracional sem permitir ataque |
| Resposta antiga podia reaplicar falha e substituir uma decisão mais recente | Só fontes mais novas avançam o estado; repetição/retrocesso bloqueados, sem esquecer o último resultado |
| Deus conhecia duas perdas, tinha capacidade, mas exigia nova oração | Declaração recebida oferece alvo/local conhecido; custo de 20 de energia, janela temporal, presença e Utility continuam exigidos |
| Região da perda religiosa podia ser confundida com a do mensageiro | Usa o local da fonte recebida; não segue o fiel remotamente |
| Cache de oito pressões expulsava circularmente todos os interesses | Atualiza oito chaves prioritárias estáveis e preserva falhas/continuidade; teste de duas decisões com 12 interesses |
| Métricas confundiam avaliações/cache com novas intenções | Contadores separados; conversão por compromissos reconstruída sem simulação adicional |

**Limitações materiais:** as duas facções naturais permaneceram com um membro nas sedes. A preparação de viagem não encontra fonte de água transportável ali; `fill_water` exige poço e estoque reais em uma localidade. Não receberam suprimentos ou membros por script. Além disso, faltou motivo coletivo grave conhecido; a facção mercenária tinha risco aceitável configurado em 0,45, abaixo do filtro de raid de 0,50. Preparação, recrutamento e incursões naturais continuam por demonstrar.

Os três deuses terminaram com energia 100 e nenhuma perda conhecida registrada. As 931 avaliações foram bloqueadas no filtro de causa/capacidade, antes da competição de Utility. Assim, **energia e uma Utility derrotada não explicam a ausência nesta seed**; o problema dominante foi pressão grave conhecida não chegando ao deus. O ajuste de resposta sem oração passou apenas no controle.

Viagens dependem de provisões, rotas e encontros; a volta da informação ainda é rara. Respostas parciais podem atender poucos indivíduos e deixar o grupo insatisfeito. A causa final da morte também não descreve toda a trajetória. O histórico e registros antigos continuam crescendo; limitar ActionPressure não limita o save inteiro. Esses pontos merecem diagnóstico posterior, não aumento arbitrário de probabilidades.

## Validação e identificação da entrega

Passaram **11 testes novos**, oito verificações antigas representativas e oito regressões antigas diretamente ligadas à letalidade: **27 testes selecionados**. A bateria antiga de 275 não foi repetida. Os controles cobrem seis famílias: causa/capacidade letal; escalada/resolução de grupo; preparação/raid; perda de fé/oração isolada; representação física; persistência, consultas puras e cache estável. Não criaram saves extras.

A campanha usou núcleo SHA-256 `ad07db0a7e9070905e0ea214c211a1bb8502be6faf177da89e51f9d1d1d24548`.
A entrega usa `5eb4237b2c987f96da62e71712e97200eb31573d4fc561019996d0cddf9088a2`.

**Os hashes diferem:** os últimos ajustes de integração, resposta divina sem oração, memória causal, repetição de respostas e retenção de pressão foram feitos após terminar a única campanha. Eles passaram nos testes direcionados; **não houve outra campanha natural**. O save e as histórias preservam a execução anterior a esses ajustes. O teste antigo de letalidade teve sua condição controlada de perda próxima explicitada, para comparar dano entre dois ataques realmente elegíveis.

Registro e evidências: [ENTREGA_FINAL.json](</home/hugo/Área de trabalho/procedrual/reports/fase_5_1/ENTREGA_FINAL.json>), [curta 200h](</home/hugo/Área de trabalho/procedrual/reports/fase_5_1/campanha/curta_200h.json>), [principal 1.000h](</home/hugo/Área de trabalho/procedrual/reports/fase_5_1/campanha/principal_1000h.json>), [testes novos](</home/hugo/Área de trabalho/procedrual/reports/fase_5_1/testes_direcionados.txt>), [smoke](</home/hugo/Área de trabalho/procedrual/reports/fase_5_1/smoke_critico.txt>) e [regressão letal](</home/hugo/Área de trabalho/procedrual/reports/fase_5_1/regressao_letal.txt>).

## Custo e arquivos

O único [save final](</home/hugo/Área de trabalho/procedrual/reports/fase_5_1/campanha/save_final.json>) ocupa **282,28 MiB**. Execução, geração, auditoria e exportação levaram **16,82 minutos**, dos quais 25,49 segundos foram de escrita do save. Pico do processo, incluindo exportação: **2.360,97 MiB**. Os valores compactos dos registros de pressão somaram **1,58 MiB**; essa medida exclui nomes, estruturas de serialização e eventos/conhecimento derivados.

Os novos arquivos somam aproximadamente **282,60 MiB**; seus tamanhos exatos e total estão em [tamanho_arquivos.json](</home/hugo/Área de trabalho/procedrual/reports/fase_5_1/tamanho_arquivos.json>). Não há código inteiro duplicado nem histórico bruto separado. [ALTERACOES.patch](</home/hugo/Área de trabalho/procedrual/reports/fase_5_1/ALTERACOES.patch>) registra a diferença do núcleo contra a cópia da entrega da Fase 5 já existente; [AJUSTES_APOS_CAMPANHA.patch](</home/hugo/Área de trabalho/procedrual/reports/fase_5_1/AJUSTES_APOS_CAMPANHA.patch>) distingue campanha e entrega. Arquivos e campanhas das fases anteriores foram preservados.
