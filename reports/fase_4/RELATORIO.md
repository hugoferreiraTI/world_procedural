# Relatório final — Fase 4: interação, combate e resposta

Base recebida em `fase_4.md`; decisão demográfica do usuário: equilíbrio. Código e evidências anteriores preservados. Este relatório usa a auditoria oficial congelada, sem misturar resultados da curta.

Arquivos: [histórias e decisões reais](</home/hugo/Área de trabalho/procedrual/reports/fase_4/HISTORIAS_EMERGENTES.md>); [métricas oficiais](</home/hugo/Área de trabalho/procedrual/reports/fase_4/auditoria_global_10000h/resumo.json>); [save final](</home/hugo/Área de trabalho/procedrual/reports/fase_4/auditoria_global_10000h/save_final.json>); [20 regressões](</home/hugo/Área de trabalho/procedrual/reports/fase_4/testes_direcionados.txt>); [registro de correções](</home/hugo/Área de trabalho/procedrual/reports/fase_4/PLANO_E_REGISTRO.md>)

## 1. Resumo executivo

Fase 4 implementada como `mvp-5-fase4`. Mira começou com 1.728 NPCs persistentes e 4.338 abstratos, seis reinos e 73 localidades. Em 10.000 h ocorreram 53.280 ataques,87 mortes em combate,547 capturas e 918 mudanças de residência (509 indivíduos). Mortes totais: 510; fome/privação continua relevante ({'hunger': 416, 'combat': 87, 'thirst': 6, 'both': 1}). Qualidade deve ser avaliada pelas cadeias causais em [histórias e decisões reais](</home/hugo/Área de trabalho/procedrual/reports/fase_4/HISTORIAS_EMERGENTES.md>), não só pelo número de eventos.

## 2. Comparação com mvp-4-fase3.2-final

| Sistema | Antes | Fase 4 |
|---|---|---|
| NPCs Mira |432 |1.728 inicialmente |
| Abstratos Mira |59.350 |4.338 inicialmente |
| Geografia |6 reinos/73 localidades |Idêntica |
| Combate NPC/jogador |Ausente |Ataque, defesa, fuga, rendição e proteção física |
| Ferimentos |Ausente |HP+lesão com efeitos e recuperação gradual |
| Guarda |Investiga/multa roubo conhecido |Casos, evidência própria, procura e captura mínima |
| Migração autônoma |Ausente |Viagem física, visita, transferência de residência |
| Emoções |Traços/pressões pessoais |Estado dinâmico causal e adaptação lenta |
| Política/religião ampla |Ausente |Segue fora do escopo |

A comparação demográfica redimensiona o total por decisão do usuário; não preserva 59.782 habitantes. A campanha anterior de Mira teve 119 mortes/432 em 10.000 h, mas esse número não é um experimento controlado contra o novo elenco e economia. O núcleo anterior está preservado em baseline_code.

## 3. Sistemas reaproveitados

Need/Goal/Utility continuam escolhendo todas as ações. Reutilizados fisiologia, alimentação preventiva, renda/crédito, produção, inventário e transferências, navegação, percepção/gossip, relações, quests, população, morte e sucessão. Novos serviços enumeram/executam alternativas e consequências; não há CombatAI paralelo nem ataque acionado diretamente por callback. Estado emocional é modificador; crime/ataque/fuga são soluções/ações; perseguição e mudança são pressões/objetivos executáveis.

## 4. População persistente nova

Multiplicador 4 aplicado após toda a geografia e personagens originais. Adiciona famílias de três, relações próximas esparsas e distribuição profissional, preservando identidades antigas. O total original seria incompatível com 2–3 abstratos por persistente sem criar 15–20 mil NPCs; o usuário pediu equilíbrio. Configurações reduzidas mantêm o elenco anterior por padrão; densidade pode ser explícita. Nenhuma pessoa nova é criada por migrar.

## 5. Relação persistente/abstrata

Mira inicial: 4.338/1.728=2.510 abstratos por persistente. Capitais 2,1; cidades 2,5; vilas 2,7 aproximadamente, com arredondamento. Total inicial 6.066. A proporção local inicial é verificada nos testes. Migração e mortes podem mudar a proporção posterior; não há reposição mágica para conservar o índice. Abstratos finais: 4.338; continuam consumidores/trabalhadores agregados.

## 6. Performance

5.673.800 decisões; 430.393 eventos relevantes preservados no arquivo causal. Tempo real total: 3575.816 s; 357.582 s/1.000 h, incluindo registro de auditoria. Memória máxima aproximada na simulação: 764.55 MiB; após persistência: 3801.03 MiB. Save: 336.75 MiB; serialização: 27.682 s; carga: 19.011 s. Medidas vêm de perf_counter e ru_maxrss em Linux; não são benchmark universal. Índices espaciais/censo local, casos ativos e fila de expiração evitam pesquisa de todos os NPCs por encontro. Histórico factual e casos arquivados continuam aumentando o save. Trabalho pago/creditado/sem insumo/saturado: {'WorkOutcome:paid': 361134, 'WorkOutcome:no_input': 8538, 'WorkOutcome:saturated': 43698, 'WorkOutcome:credited': 61018}.

Serialização/carga medidas novamente no checkpoint 10000 h; tempos originais não foram gravados antes da falha. Memória após persistência foi medida no processo de recuperação; o pico original dessa etapa não foi preservado. O save de cerca de 337 MiB e a carga custosa são limites relevantes do protótipo.

## 7. LOD

Fisiologia fecha toda hora para todos. Decisões: ativo 1 h por conflito/pressão vital/evento/jogador próximo/viagem; local 3 h para importantes,6 h comuns; fundo 12 h em casa. Distribuição final: {'active': 336, 'local': 621, 'background': 261}. Promoção muda quando será tomada a decisão, sem disparar ação automática. Combate executa uma operação física por decisão, sem converter seis horas de LOD em seis ataques simultâneos.

## 8. Estados emocionais

Raiva, ressentimento, humilhação e desespero são separados dos onze traços. Agressões, roubo, humilhação e perdas precisam ser conhecidos; precariedade e privação próprias também contribuem. Governante rico não vira culpado sem evidência.

| Estado | Média dos vivos | Vivos com valor≥50 | Máximo |
|---|---:|---:|---:|
| Raiva | 34.67 | 442 | 100.0 |
| Ressentimento | 65.66 | 821 | 100.0 |
| Humilhação | 41.19 | 517 | 100.0 |
| Desespero | 91.08 | 1118 | 100.0 |

Contribuições factuais acumuladas por personagem: {'ItemStolen': 305833, 'CharacterThreatened': 1895, 'CharacterAttacked': 64250, 'CharacterInsulted': 1802, 'CharacterDied': 85, 'CharacterKilled': 16}. São interpretações, não crimes únicos: o mesmo fato pode afetar testemunhas diferentes. Apoio/reparação e decaimento reduzem pressão. A contribuição persistida evita reaprender a mesma notícia como novo choque. O desespero médio alto é um sinal de desequilíbrio, não uma medida de qualidade narrativa.

## 9. Alteração lenta de personalidade

7097 adaptações. Acúmulo de pressão e intervalo mínimo 720 h dão+1 em vingatividade e independência por adaptação, máximo cinco. Uma ofensa não substitui personalidade-base. O modelo é mínimo e não representa desenvolvimento psicológico completo; estados causais e mudanças são persistidos.

## 10. Grievances

44963 grievances criadas; 14561 mantidas pelos vivos no final. Cada registro possui alvo, causa, intensidade, fonte e tempos. Só há atribuição direcionada ao ator de um fato conhecido. Lista pessoal limitada 16; intensidade decai. Perda sem autoria conhecida pode gerar luto, sem apontar automaticamente o assassino verdadeiro.

## 11. Novas ações sociais

11.094 eventos sociais estruturados registrados. Confrontar, ameaçar, cobrar, avisar, insultar, desculpar, retirar-se, pedir auxílio, alertar, acalmar e perdoar competem com fuga/denúncia/ataque. Abordagens repetidas no mesmo episódio têm controle. Cobrança gera pressão; devolver é escolha do autor e transfere um bem real. Exemplos: [histórias e decisões reais](</home/hugo/Área de trabalho/procedrual/reports/fase_4/HISTORIAS_EMERGENTES.md>).

## 12. Crime

Roubos: 102.149; roubos com outro participante/testemunha além do autor: 101.233; denúncias: 18.684; procuras emitidas: 50.562. Roubo serve comida, dinheiro ou avanço; não depende de profissão/crimeNeed. Mercador presente é oportunidade observável, sem consulta remota do inventário. Riqueza/ganância podem gerar crime, mas o relatório não atribui esse motivo só porque ocorreu roubo: consulte a necessidade amostrada. Crime e briga ainda podem ter raízes alimentares. Tentativas amostradas de roubo pessoal por necessidade: {'money': 45153, 'advancement': 21, 'food': 13413}; tentativa não equivale a roubo concluído.

O crime financeiro mínimo ainda transfere provisões: a necessidade amostrada de dinheiro/avanço explica a escolha, mas não comprova ganho em moedas. Não há cadeia autônoma específica de revenda do bem roubado; esse limite pode favorecer repetição de soluções financeiras sem desfecho monetário direto.

## 13. Reação da vítima

Pressão própria por agressão/ofensa/procura institucional pode produzir confronto, denúncia, devolução, desculpa, defesa, fuga, rendição ou ataque. Foram criadas 49365 necessidades de resposta. A ameaça conhecida e a força percebida participam da utility; raiva não executa violência. Ataque requer alternativa viável, alvo vivo presente e ausência de rendição/detenção/trégua.

## 14. Testemunhas

Crimes/ataques/mortes observados tiveram média 6.21 participantes/testemunhas por evento, contando os envolvidos. Acesso é célula local e participantes; gossip percorre contatos com confiabilidade própria. Avisos de procurado usam a cidade como alvo para evitar ensinar suspeito remoto. Guards têm fontes/gravidade/status/localização individuais, mesmo quando compartilham registro institucional.

## 15. Combate

Ataques: 53.280; conflitos físicos iniciados: 9.370; defesas: 16.269. Dano=(4+bônus arma)×(0,5+HP/200)×(1−lesão/250), bônus até 12, variação−2..+2, defesa× 0,45, mínimo 1. Arma própria/qualidade são objetivas; força alheia usa aparência aproximada/sinais visíveis. Encerramentos: {'flee': 9588, 'apologize': 299, 'restitution': 25, 'surrender': 2091, 'withdraw': 277, 'timeout': 3025, 'incapacity': 1399, 'capture': 547, 'forgive': 1, 'death': 87, 'departure': 113}. ConflictEnded também registra encerramento social, portanto não deve ser dividido cegamente por ConflictStarted. Maior número de ataques por um ator: 473; repetição merece avaliação nos exemplos.

## 16. Ferimentos

Lesão 0–100 além do HP. Lesão≥20 reduz passos por lote e horas produtivas do lote, além de poder de combate e fuga; mínimo de uma operação permanece. Lesão≥6 cria pressão para recuperar. Feridos vivos no final: 140. Um defensor pode interceptar dano; não pode interceptar o próprio ataque nem atuar rendido/detido. Não há anatomia, sangramento ou sistema de membros.

## 17. Tratamento

Socorros iniciais: 91. Exigem paciente vivo presente, lesão≥6, uma provisão e uma água do ajudante; aliviam 6 de lesão e 2 HP. Descanso elegível recupera lentamente 2 de lesão/hora. Sem profissão de curandeiro/hospital, seek_treatment significa procurar local seguro e descansar. Auxílio solicitado cria uma necessidade para outro NPC; não obriga uma cura automática.

## 18. Fuga/rendição

Fugas físicas: 9.588; retiradas: 277; rendições: 2.091; tentativas fracassadas: 6.145. Fuga move uma etapa física se possível; tentativa fracassada consome a hora. Rendição impede continuar o ataque e permite captura. Incapacidade≤12 HP também encerra confronto. Trégua 48 h reduz reataque imediato; o conflito social pode continuar depois.

## 19. Mortes violentas

Mortes em combate: 87 de 510 (17.06%); causas completas: {'hunger': 416, 'combat': 87, 'thirst': 6, 'both': 1}. Mortes por privação com comida carregada: 1. Mortes por privação com ataque nas 48 h anteriores: 67; esta é associação temporal, não prova de causalidade nem contagem adicional de assassinatos. O mesmo finish_death mantém corpo/posses, encerra ações, emite fato, reduz censo uma vez e aciona sucessão. Morto não decide/ataca. Causa autoinfligida abstrata: 0; condição rara exige desespero extremo prolongado, múltiplas perdas conhecidas e isolamento, com apoio impedindo elegibilidade. Nenhuma descrição de método é implementada.

## 20. Perseguição

Buscas locais: 45.354; localizações: 1.202; procuras expiradas: 6.918. Destino é a última posição conhecida por aquele guarda, atualizada por observação/fato novo; não há consulta à posição remota atual do suspeito. Até três buscas sem avanço e janela 168 h limitam o episódio. A busca de perseguidores é local; ela não atravessa automaticamente mapas atrás de fugitivos. Cada suspeito reutiliza o objetivo do guarda; mudança de pista permite nova busca.

## 21. Procurados

Registros institucionais: 50562; estados finais: {'resolved': 43014, 'expired': 6918, 'captured': 521, 'active': 109}. Fonte, jurisdição, suspeito, gravidade, confiança e tempo são persistidos. Autorização exige guarda local/confiança≥60. Força legal/autodefesa contextual não cria delito automaticamente. Resolução remota não vira conhecimento instantâneo dos outros guardas; conhecimento próprio ou prazo encerram a procura.

## 22. Captura

Capturas: 547; liberações: 485; intervenções com multa: 44.850. Capturar exige presença e rendição/incapacidade. Multa usa até 5 moedas existentes, transferidas ao caixa local; detenção 12 h é temporária, sem teleporte. Caso multado encerra quando a resolução é conhecida; não autoriza multas repetidas pelo mesmo fato. O sistema não é tribunal, investigação probatória completa ou prisão simulada.

## 23. Migração

Partidas: 939; chegadas como visitante: 921; mudanças de residência: 918; indivíduos: 509; motivos das partidas: {'threat': 384, 'wanted': 548, 'poverty': 7}. Rota conhecida, provisões, portão, caminho externo, entrada e 24 h de visita precedem o censo. Origem perde 1, destino ganha 1; abstratos não viram novos migrantes. Trabalho usa residência/instalação compatíveis; visitante pode comprar/coletar no local físico. Após fixação 336 h de adaptação restringem nova mudança.

Rotas com mais partidas; contagens de viagens, não de moradores finais:

| Origem | Destino | Partidas |
|---|---|---:|
| Karven (#425) | Dormar (#490) | 46 |
| Dormar (#490) | Karven (#425) | 40 |
| Karmir (#1398) | Armar (#1239) | 27 |
| Karvia (#677) | Kardor (#706) | 26 |
| Armar (#1239) | Karmir (#1398) | 24 |
| Mormir (#1650) | Valthon (#1679) | 23 |
| Morven (#1203) | Karthon (#1315) | 23 |
| Elithon (#1614) | Dorthon (#1567) | 22 |
| Karthon (#1315) | Morven (#1203) | 21 |
| Dorthon (#1567) | Elithon (#1614) | 20 |

## 24. Impacto em família/luto/vingança

Luto criado: 216; vingança/reparação criada: 59.793; proteção criada: 100.486. São contagens de ativações, não pessoas distintas nem vinganças concluídas. Famílias esparsas ampliam a rede afetada; informação ainda precisa alcançar cada membro. Assassinato não revela autoria a familiar remoto. Memória curta/gossip e expiração de necessidades limitam continuidade; esse limite aparece nas histórias interrompidas.

## 25. Impacto em reputação

Roubo, agressão ilegal, ameaça, auxílio, proteção e reparação mudam reputação segundo confiança/contexto. Interpretação de morte continua contextual à relação/lealdade; força legítima não é marcada automaticamente como crime. Eventos de ajuda: 2.650; proteção física e companhia: 13.046; desculpas: 299; restituições: 25. Não há reputação universal, propaganda ou julgamento objetivo atribuído a todo o mundo.

Rumores/informação: 2.202.078 / 6.964. O relatório registra fatos que mudam reputação e as fontes das histórias; não preservou uma série temporal de cada reputação individual, portanto não apresenta uma contagem inventada de opiniões alteradas.

## 26. Testes direcionados

Vinte regressões compostas passaram: dano/arma/defesa/intercepção; morte/censo/corpo/sucessão; testemunha/culpado desconhecido; fuga/rendição; escolha violenta e denúncia; guarda informado versus remoto; captura/detenção/liberação; devolução material; emoções/dedup/adaptação; socorro; pedido de ajuda; rota/visita/residência; comércio de visitante; densidade/geografia; save/load determinístico; LOD/fisiologia; desespero/apoio; caso encerrado/objetivo reutilizado; auto-intercepção. A suíte anterior 179 foi executada uma vez: 12 falhas,10 corrigidas e reavaliadas,2 expectativas antigas atualizadas e reavaliadas. Os logs preservam todas as etapas; não houve segunda execução completa.

Os 20 casos passaram novamente após a correção de casos acumulados. O caso 19 foi ampliado com dois guardas, resolução desconhecida, nova agressão, bloqueio de multa insuficiente e reconstrução do índice a partir de um checkpoint com casos sobrepostos. Log: [regressões posteriores](</home/hugo/Área de trabalho/procedrual/reports/fase_4/testes_pos_auditoria.txt>).

Cinco regressões antigas diretamente relacionadas a denúncia e continuidade também passaram após a correção, incluindo continuidade 80+200 h com recarga. Log: [regressões legadas relacionadas](</home/hugo/Área de trabalho/procedrual/reports/fase_4/regressoes_legadas_relacionadas.txt>).

## 27. Auditoria curta

Primeira tentativa interrompida pelo validador em 500 h: auto-intercepção do protetor 4058, eventos 423845/423846 em 495 h. Arquivos preservados. Corrigidos também repetição de multas e migração circular. Auditoria corrigida 1000 h: 1.604 vivos,124 mortes (110 fome/14 combate),8.062 ataques,90 capturas,290 mudanças; 417,383 s. Instrumentação falhou somente na continuação após escrever o checkpoint 1000 h, por callback ligado a arquivo fechado. Resumo/continuação 24 h recuperados do checkpoint, sem repetir campanha. Depois foram corrigidos limites dos objetivos/índices e regressões antes de congelar a oficial.

## 28. Auditoria global de 10.000 h

UMA campanha Mira global sem jogador, geração inicial com histórico 0 h e código congelado antes da execução. SHA256 auditado: 1ed1227dae6b8e7a31e9b262489e0d73b2f240d06fbd94ca507d337891871b2e. Invariantes verificados a cada 100 h; último estado: []. O save 10000 h foi escrito e carrega; a comparação original de 24 h divergiu (False). Depois da campanha foi corrigido o tratamento de múltiplos casos conhecidos e a remoção indevida do índice institucional. A verificação curta posterior compara o motor contínuo 10000→10024 com uma recarga em 10012: igualdade exata=True; índice ativo consistente a cada hora=True. SHA256 entregue: 74dee84cf3997e30f5b81840cf0c60f4edda6d053122e2300ca6bbf3c6b4da4e. Esta verificação não substitui nem repete a campanha oficial.

O resumo foi recuperado dos arquivos já escritos; os valores de vivos/mortos/tempo intermediários vêm do log. Emoções/lesões intermediárias não foram preservadas após a falha e estão identificadas como ausentes. Não houve três longas nem replay integral 10.000 h.

| Hora | Vivos | Mortos | Lesionados | Raiva média | Desespero médio | Tempo acumulado(s) |
|---:|---:|---:|---:|---:|---:|---:|
| 1000 | 1583 | 145 | não preservado | não preservado | não preservado | 422.2 |
| 2000 | 1480 | 248 | não preservado | não preservado | não preservado | 843.9 |
| 3000 | 1422 | 306 | não preservado | não preservado | não preservado | 1243.6 |
| 4000 | 1376 | 352 | não preservado | não preservado | não preservado | 1621.0 |
| 5000 | 1340 | 388 | não preservado | não preservado | não preservado | 1973.4 |
| 6000 | 1312 | 416 | não preservado | não preservado | não preservado | 2313.0 |
| 7000 | 1295 | 433 | não preservado | não preservado | não preservado | 2642.6 |
| 8000 | 1260 | 468 | não preservado | não preservado | não preservado | 2965.2 |
| 9000 | 1239 | 489 | não preservado | não preservado | não preservado | 3275.7 |
| 10000 | 1218 | 510 | 140 | 34.67 | 91.08 | 3575.816 |

## 29. Métricas de interação

Contagens de eventos; ativação de necessidade não equivale a história resolvida. IDs e decisões estão nos arquivos causais.

| Evento/ação | Quantidade |
|---|---:|
| ApologyGiven | 299 |
| CalmingAttempted | 149 |
| CharacterAttacked | 53.193 |
| CharacterCaptured | 547 |
| CharacterConfronted | 3.070 |
| CharacterDefended | 16.269 |
| CharacterDied | 423 |
| CharacterFled | 9.588 |
| CharacterInsulted | 1.529 |
| CharacterKilled | 87 |
| CharacterReleased | 485 |
| CharacterSurrendered | 2.091 |
| CharacterThreatened | 1.611 |
| CharacterWarned | 255 |
| CharacterWithdrew | 277 |
| ComfortGiven | 24 |
| ConflictEnded | 17.452 |
| ConflictForgiven | 1 |
| ConflictStarted | 9.370 |
| FirstAidGiven | 91 |
| GuardResponded | 44.850 |
| HelpGiven | 2.650 |
| ImmediateHelpRequested | 489 |
| InformationShared | 6.964 |
| InvestigationPerformed | 1.524 |
| ItemStolen | 102.149 |
| MigrationArrived | 921 |
| MigrationStarted | 939 |
| PersonLocated | 3.266 |
| PersonalityAdapted | 7.097 |
| ProfessionChanged | 7 |
| ProtectionGiven | 13.046 |
| PursuitEnded | 6.918 |
| PursuitSearch | 45.354 |
| ResidentMoved | 918 |
| ResponsibilityFulfilled | 152 |
| RestitutionDemanded | 3.546 |
| RestitutionGiven | 25 |
| SuccessionChanged | 6 |
| SuspectLocated | 1.202 |
| ThirdPartyAlerted | 120 |
| ThreatAvoided | 2.184 |
| ThreatReported | 18.684 |
| TrainingAbandoned | 1 |
| TrainingStarted | 8 |
| WantedIssued | 50.562 |

## 30. Histórias emergentes

Foram selecionados 20 exemplos reais, com IDs, conhecimento amostrado, necessidade, prioridade, estado emocional, alternativa escolhida e comparação de utility. Leia [histórias e decisões reais](</home/hugo/Área de trabalho/procedrual/reports/fase_4/HISTORIAS_EMERGENTES.md>). Os exemplos incluem finais cotidianos, fuga, reparação, proteção e captura quando presentes; os desejos de história não viram eventos fictícios no relatório.

Avaliação: reparação material, auxílio, proteção, captura e mudança de cidade aumentam as consequências possíveis. As cadeias de agressão ainda repetem golpes e a fome segue dominante. H07, H10 e H20 documentam respostas distintas; os arcos violentos e a raridade de mudança por pobreza mostram onde a variedade ainda é limitada.

## 31. Histórias longas

O arquivo de histórias distingue vínculos explícitos source_fact de antecedentes temporais do mesmo NPC. Migração pode cruzar crime/procura, deslocamento, chegada e residência; mortes podem cruzar autoria, testemunha, luto/reparação e consequência institucional. Só se inclui carreira posterior quando houve evento real; apenas estar na mesma cidade/sobrenome não prova relação familiar ou causalidade. Nem toda cadeia terminou: prazo, perda de informação, necessidade vital e afastamento interrompem arcos.

## 32. Bugs descobertos

1. RNG após ataque não sincronizado antes de salvar: corrigido em Goal.execute sem mutar ação inválida.
2. Protetor interceptava próprio ataque ou interceptava rendido: filtro corrigido.
3. Caso resolvido autorizava multa/procura repetidas: resolução e fonte/status próprios corrigidos.
4. Migração repetida sem adaptação: 336 h e reavaliação econômica local.
5. Objetivo novo por caso e varredura crescente de arquivados: objetivo por suspeito, índice ativo/fila de prazo.
6. Compra de refeição em mapa sem cidade gerava KeyError: retorna recusa sem avanço.
7. Reaprender notícia fora da memória curta podia repetir emoção: contribuição factual persistida.
8. Fuga fracassada do jogador não consumia hora: tentativa válida corrigida.
9. Instrumentação mantinha callback após fechar arquivo: desligado antes da verificação pós-save.
10. Densificação afetou cenários reduzidos usados pelas regressões econômicas: configuração explícita/escala anterior preservada.

Os originais dos testes e código anteriores permanecem no baseline. A campanha oficial foi executada após os dez itens acima e o congelamento.

11. Inspeção final e verificação pós-save descobriram incoerência entre caso selecionado, caso executado e índice institucional: corrigida DEPOIS da campanha. Um guarda podia escolher agressão grave, executar caso antigo de roubo e apagar um caso novo do índice. A recarga reconstruía esse caso e alterava a execução. A escolha agora agrupa casos por suspeito e gravidade conhecida; a execução usa a mesma escolha; multas pequenas não resolvem casos graves; fechamento mantém outros casos ativos, inclusive desconhecidos pelo guarda. Microcenário no código congelado reproduziu a divergência. A primeira correção teve continuidade exata, mas o verificador detectou um índice incompleto diante de casos antigos sobrepostos: o índice passou a manter todos os casos ativos por suspeito. As duas evidências anteriores foram preservadas.

A correção posterior não participou dos 10.000 h oficiais. Foi validada por regressões e pela continuação curta documentada na seção 28; não houve segunda campanha longa.

## 33. Limitações

Combate é local e simples; não há anatomia, hospital/curandeiro, julgamento completo, perseguição universal ou recrutamento tático. Migração usa poucas rotas públicas conhecidas, exige reservas e usa 24 h para residência, sem empregos garantidos. Apoio limitado não assegura cura. Abstratos seguem agregados. Perseguição não atravessa mapas automaticamente e não procura todas as cidades. A amostragem detalhada não inclui a ação antiga de roubo do mercado: nesses elos, o evento/fonte são comprovados, mas o estado/utility original do ladrão não foi amostrado. Metadados de destino para família/trabalho ainda não são alimentados completamente, limitando esses motivos de migração. Texto dos eventos sociais ainda é simples e em alguns casos mostra o nome interno da ação. Memórias/gossip/necessidades com prazo ainda encurtam algumas histórias; registros históricos/factuais ampliam saves. A frequência de ataques não é sinônimo de profundidade e comida pode continuar origem de muitos conflitos. Duas antigas expectativas de teste foram alteradas porque proibiam comportamentos agora solicitados. Saves da Fase 3.2 não carregam nesta versão: núcleo/saves antigos estão preservados.

Limites medidos: fome ou fome+sede representam 81.76% das mortes; desespero médio final 91.08. O repertório social aumentou, mas essas pressões e o save volumoso ainda precisam de equilíbrio e contenção de histórico. A campanha original também teve falha de continuidade, corrigida e verificada em escopo curto posterior.

## 34. Preparação para Fase 5

Prontos para reutilizar: estados emocionais causais, fontes/culpados conhecidos, grievances, violência/ferimentos, defesa/fuga/rendição, testemunhas, reputação, casos locais, migração, perdas familiares, morte/sucessão e registros persistidos. Ainda NÃO implementados: guerras, exércitos, cerco, diplomacia completa, revoluções, facções políticas completas, disputa formal do trono, deuses/religião ativa, nascimento, envelhecimento, herança, caravanas e destruição de cidades. São etapas futuras; esta campanha não comprova sua emergência.
