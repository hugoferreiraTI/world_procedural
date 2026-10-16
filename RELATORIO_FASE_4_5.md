# Fase 4.5 — impulso social, ambição e consequência

Versão **mvp-6-fase4.5**, seed **Vespera-47**, mundo novo em h 0, sem jogador e sem carregar save. 1.776 personagens persistentes, 75 localidades e 6 reinos. SHA-256 da campanha: `ad79243a9a9a1aea2158a81abb000b4719335ace9c5e04581bc1d0f4132d9dbc`. SHA-256 da entrega: `20b26d3def72979fc3c03938856c8d8301ee39336089fb6088970a9cfe656442`. A longa preserva o código congelado; correções encontradas durante a revisão foram validadas depois em regressões e na curta de entrega.

## Resultado

A camada nova preserva intenções através de interrupções e permite iniciativas baseadas em aspirações. A campanha registrou **91.913 compromissos**, **21.213 encerrados por resolução**, **65.035 abandonados** e **2.257 expirados**. 24.757 tiveram progresso verificável e 21.908 mudaram de estratégia. Esses números contam compromissos, não pessoas nem histórias profundas.

O avanço narrativo é parcial: persistência e mudanças de abordagem existem, mas cuidado por privação e delitos leves ainda dominam. A sobrevivência piorou nesta campanha congelada: **365 mortes**, contra **255** na Fase 4.1. As correções finais passaram na curta de 500 h; não foi rodada outra longa para afirmar que essa diferença desapareceu.

## Implementação e alterações necessárias

- **Commitment:** guarda dono, necessidade, fato causal, alvo, motivação, intensidade, investimento, tentativas, progresso, fracassos e encerramento. Até quatro por NPC; mantém a mesma Need e passa novamente pelo Goal/Utility. Pausa, retomada e abandono são registrados.
- **Memória causal:** fatos usados por compromissos ativos e até três evidências complementares ficam protegidos dentro do limite de 64 fatos. Lembrar não chama novamente o processamento emocional.
- **Impulso/agência:** considera urgência, tempo sem resolução, fracassos, emoções, traços, relação, gravidade conhecida, recursos, saúde, risco e pistas. Não executa ações. Pressão extrema pode aliviar parcialmente custos morais/de risco e tornar roubo pessoal uma alternativa; não força crime.
- **Aspiration:** direção principal derivada de personalidade e situação, com riqueza, competência, reconhecimento ou família. Só oferece passos apoiados por oportunidades conhecidas. Competência usa aprendizagem real; dinheiro ganho não conta como progresso de competência. Reconhecimento exige responsabilidade pública observada; família acompanha resolução de cuidados.
- **Violência:** afastar, conter, subjugar, ferir e matar são intenções de resultado. Fórmula, armas e multiplicador de defesa permaneceram iguais. Incapacidade comum encerra combate; intenção letal sustentada abre uma nova escolha entre continuar, poupar, retirar-se, pedir ajuda ou capturar quando válido. A regressão comprova tanto poupar quanto causar fatalidade.
- **Guarda:** usa o mesmo caso local. Informação formal circula no serviço do mercado após latência de seis horas; até três tarefas por caso: busca, vigilância e informação. Gravidade modifica prioridade e duração. Guarda remoto não aprende por telepatia.
- **Pistas interlocalidades:** viagens passam por portão, estrada e entrada conhecidos, com provisões reais; preservam residência. Ao chegar, usa a última pista e encontros, sem consultar posição global do perseguido.

Foi necessário integrar manutenção de compromissos ao refresh de Needs, proteger causas da remoção FIFO e permitir julgamento após incapacidade. Também foi corrigida uma falha anterior: `CharacterKilled` saía do processamento da justiça antes de registrar o crime do autor. A correção mantém a resolução de casos contra a vítima e permite registrar o homicídio conhecido. As curtas revelaram uma ligação fraca de aspirações com necessidades antigas; a revisão liga a aspiração ao objetivo compatível e separa competência de riqueza. A transição interna de motivo durante viagem também passou a preservar o compromisso, mantendo sua causa original. Um cenário controlado identificou impulso insuficiente para auto-iniciativa; a direção da aspiração agora participa do impulso e da urgência da necessidade correspondente.

Na revisão da longa, cinco casos adicionais foram reproduzidos e corrigidos na entrega: (1) uma perseguição encerrada pelo conhecimento do próprio guarda podia ser reativada pelo compromisso; (2) a certeza da morte bloqueava identificação posterior do autor com confiança menor, mas suficiente; (3) o compromisso registrava confiança 100 por padrão mesmo com notícia 60; (4) seguir pista distante não mantinha o LOD horário usado na estimativa de viagem; (5) reutilizar uma Need resolvida podia apagar o encerramento da intenção anterior. As falhas anteriores e os testes posteriores foram preservados. Os resultados da longa incluem esses problemas; não foram recalculados ou apresentados como uma longa do código corrigido.

## Validação e preservação

**227 testes passaram**, incluindo 18 regressões novas e as dez de recuperação. Cobrem pausa/retomada, causa sem choque duplicado, abandono, agência sem informação remota, autoria desconhecida, evidência posterior, intenção sem bônus de dano, incapacidade, fatalidade/mercy, guardas, aspiração, save/load e determinismo.

As curtas de diagnóstico foram preservadas, incluindo as revisões de aspiração e continuidade. A curta da entrega passou por 500 horas em `curta_entrega_500h`, com 15 mortes e zero violações estruturais. Uma execução inicial foi interrompida após o checkpoint de 600 h para corrigir abandono falso de viagem; os dados estão em `diagnostico_interrompido` e não entram nos resultados oficiais. Uma campanha longa foi concluída: 5000 horas. A longa passou por 50 verificações de integridade. Nenhum resultado anterior foi sobrescrito.

Os arquivos de alimentação, recuperação, economia, profissões, geração, migração, população, política e itens são idênticos à base preservada. A fórmula `power` também é idêntica. O registro dessa comparação está em `preservacao.json`. Nova versão de save; campanhas antigas continuam acessíveis com sua versão correspondente preservada.

## Comparação física com a Fase 4.1

| Indicador em 5.000 h | Fase 4.1 | Fase 4.5 |
|---|---:|---:|
| Vivos | 1521 | 1411 |
| Mortes por fome/fome+sede | 243 | 341 |
| Mortes por sede | 3 | 14 |
| Mortes por combate | 9 | 10 |
| Ataques individuais | 17168 | 20655 |
| Rações por dia de NPC vivo | 1.1867 | 1.1872 |
| Mortes alimentares carregando comida | 0 | 0 |

Mesma seed e geração inicial; as decisões e o fluxo aleatório divergem depois. A comparação é descritiva, não isola o efeito de cada mecanismo. Não houve meta de mortalidade ou aumento de dano/produção para obter estes resultados.

Variação observada de mortes totais: 255 → 365. Se a mortalidade aumenta, isso é uma regressão de sobrevivência observada, mesmo com módulos fisiológicos iguais; mudanças nas escolhas, deslocamentos e acesso podem alterar o resultado. A curta posterior não prova recuperação dessa diferença no horizonte de 5.000 h.

## Continuidade, violência e instituição

Duração média dos compromissos: **174.6 h**, incluindo os ainda ativos, portanto com censura no fim da campanha. 19.155 arcos tiveram pelo menos três tipos de transição além da adoção. Isso mede diversidade de marcos; preparar comida/água e trocar abordagem também conta, sem equivaler a uma grande saga.

| Origem | Compromissos adotados | Episódios de progresso |
|---|---:|---:|
| reconhecimento | 2.353 | 645 |
| ascensão pessoal | 3.432 | 3.180 |
| cuidado ou busca familiar | 27.612 | 55.750 |
| mudança de residência | 7.480 | 40.886 |
| perseguição institucional | 3.738 | 4.693 |
| proteção | 32.114 | 5.753 |
| vingança/reparação | 15.138 | 2.423 |
| luto | 46 | 60 |

Transições de intenção: `{'hurt': 2636, 'contain': 1226, 'repel': 1621, 'subdue': 1574}`. Incapacidades: 199; poupados: 0; fugas: 5261; rendições: 1352; capturas: 115. São ocorrências, não indivíduos ou conflitos únicos.

Fatalidades por intenção: `{'hurt': 4, 'subdue': 5, 'contain': 1}`; continuadas após incapacidade: 0. A capacidade de julgamento letal em cenário controlado não prova sua frequência natural nem comprova que as mortes registradas foram vinganças executadas.

Casos institucionais: 21.939; casos com mais de uma tarefa de guarda: 1.012. Máximos observados: 4 compromissos por personagem e 3 guardas atribuídos por caso. A maioria dos registros é de delitos leves.

Gravidade dos casos: `{1: 20730, 2: 62, 3: 886, 4: 258, 5: 3}`. Estados institucionais finais: `{'resolved': 14413, 'expired': 7054, 'captured': 115, 'active': 357}`; cada guarda continua limitado ao estado que pessoalmente conhece.

Amostras diárias de vingança forte/agressividade compatível: `{'distance_or_stale_lead': 3603, 'other_need': 959, 'truce': 53, 'utility_or_known_risk': 16, 'attack_selected': 5, 'solution_absent': 1, 'incapacity': 2}`. As categorias distinguem pista desconhecida, distância, incapacidade, trégua, outra necessidade e Utility/risco; as amostras não são pessoas independentes. O perfil e os exemplos estão no resumo JSON.

## Ambição

| Ambição inicial | NPCs | Compromissos de ascensão/reconhecimento | Episódios de progresso |
|---|---:|---:|---:|
| ambição <40 | 690 | 1248 | 97 |
| ambição 40–69 | 593 | 1882 | 745 |
| ambição ≥70 | 493 | 2655 | 2983 |

Controle de 120 h, seed Ambicao-45, mesmo mundo e mesmo agricultor; somente ambição inicial foi alterada:

| Ambição | Compromissos adotados | Ações de ascensão | Dinheiro final |
|---|---:|---:|---:|
| 15 | 0 | 0 | 44 |
| 85 | 1 | 5 | 50 |

A regressão controla a direção do efeito: maior ambição aumenta intensidade/prioridade, sem criar ação automática. As faixas da campanha misturam profissão, riqueza, sobrevivência e oportunidade; não provam causalidade isolada. Ascensão profissional ainda depende das oportunidades de aprendizagem já existentes, sobretudo cozinha.

## Histórias e limites

[Leia as histórias e suas evidências](</home/hugo/Área de trabalho/procedrual/reports/fase_4_5/HISTORIAS_REAIS.md>). A seleção inclui cuidado, perseguição, vingança/reparação, ascensão, proteção, viagem, fracasso e intenção ainda aberta. Os arcos completos permanecem em `global_5000h/arcos.json`; não contamos golpes repetidos como capítulos. O complemento da curta corrigida registra a cadeia completa com emoções e prioridade medidas; a longa não tinha esses campos, e sua ausência foi explicitada.

- A fisiologia permanece com as limitações documentadas na Fase 4.1. Esta fase não encerra o problema de fome/recuperação.
- Progresso local e preparo são reais, mas nem sempre produzem transformação narrativa profunda; continuidade não garante uma boa história.
- Aspirações dependem das capacidades disponíveis; reconhecimento e competência têm repertório limitado.
- Agência percebida é uma estimativa simples de recursos, saúde, risco e lugares/pessoas conhecidos. Conhecer uma oportunidade não garante acesso; caminhos inviáveis ainda podem gerar otimismo e tentativas frustradas.
- Comunicação institucional exige serviço local e tem alcance limitado; guardas podem perder pistas, abandonar ou não conseguir capturar.
- Intenção letal é possibilidade, não obrigação. Separar sua capacidade controlada da frequência natural registrada.
- Vingança pode encerrar por denúncia, reconciliação, morte conhecida ou abandono; não chamar isso automaticamente de vingança executada.
- A falha anterior de bloqueio entre `forage_meal` e `forage` continua fora desta fase.
- Uma seed, uma longa; resultados não representam todos os mundos.

Prioridades antes de ampliar conteúdo: conferir perseguições que trocam casos sem avanço, viagens com acesso precário a água/comida e aspirações com muitas tentativas e nenhuma conquista. As cinco correções finais resolvem casos específicos; o aumento de mortes e a pouca profundidade de alguns arcos continuam limitações abertas.

Não foram adicionados política, guerras, revoluções, facções novas, deuses ou religião organizada. Antes de expandir, revisar os arcos com muita atividade e pouco progresso e os diagnósticos de prioridade/pistas. A evolução central é manter intenção, reavaliar meios e registrar consequências através dos sistemas existentes.

## Arquivos

`fase_4_5.md`: especificação; `tests/test_phase45.py`: regressões; `reports/fase_4_5/global_5000h/`: campanha, save, resumo, personagens, casos, arcos e logs comprimidos; `reports/fase_4_5/evidencias_historias.json`: seleção causal verificável.


Custo observado da longa: 63.7 minutos até apurar o resumo (exclui exportação final do save); histórico com 1.854.488 eventos. Estados ativos têm limites, mas o histórico persistente cresce com a campanha; pausa/retomada pode produzir bastante volume. O save exportado ocupa 1209.1 MiB.
