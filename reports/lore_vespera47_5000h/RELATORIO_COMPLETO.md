# Relatório completo de lore — Vespera-47, 5000h

## 1. Resultado e alcance

Seed **Vespera-47**, versão **mvp-5-fase4**, mundo novo a partir de geração em h0, sem jogador e sem carregar saves. Observação de **5000 horas**. Elenco inicial: 1776 persistentes e 4461 abstratos; 75 localidades e 6 reinos. Final: 1387 vivos; 389 mortes. Há crime, combate, apoio, reparação, fuga e mudança de residência reais. A diversidade deve ser lida nas histórias, sem transformar contagem de eventos em qualidade literária.

## 2. Onde ler tudo

[Histórias detalhadas](</home/hugo/Área de trabalho/procedrual/reports/lore_vespera47_5000h/HISTORIAS_DETALHADAS.md>); [catálogo de todos os personagens](</home/hugo/Área de trabalho/procedrual/reports/lore_vespera47_5000h/CATALOGO_POR_PERSONAGEM.md>); [catálogo por localidade](</home/hugo/Área de trabalho/procedrual/reports/lore_vespera47_5000h/CATALOGO_POR_LOCALIDADE.md>); [cronologia dos reinos](</home/hugo/Área de trabalho/procedrual/reports/lore_vespera47_5000h/CRONOLOGIA_DOS_REINOS.md>); [catálogo integral de arcos, em JSONL compactado](</home/hugo/Área de trabalho/procedrual/reports/lore_vespera47_5000h/CATALOGO_COMPLETO_DE_ARCOS.jsonl.gz>); [eventos integrais selecionados](</home/hugo/Área de trabalho/procedrual/reports/lore_vespera47_5000h/eventos.jsonl.gz>); [decisões amostradas](</home/hugo/Área de trabalho/procedrual/reports/lore_vespera47_5000h/decisoes.jsonl.gz>); [recepção de notícias e necessidades](</home/hugo/Área de trabalho/procedrual/reports/lore_vespera47_5000h/reacoes.jsonl.gz>); [métricas](</home/hugo/Área de trabalho/procedrual/reports/lore_vespera47_5000h/resumo.json>); [análise quantitativa](</home/hugo/Área de trabalho/procedrual/reports/lore_vespera47_5000h/analise_lore.json>).

O catálogo cobre 369.531 eventos narrativos em 155.947 arcos/lotes. Componentes ligados por fontes são causais; eventos de rotina isolados são agrupados por par/semana e marcados como lote, sem inventar uma trama. 36 recortes recebem leitura detalhada. Consumo e trabalho comuns ficam nas métricas, não são apresentados como histórias épicas.

## 3. Método e evidência

Hash do núcleo congelado: `74dee84cf3997e30f5b81840cf0c60f4edda6d053122e2300ca6bbf3c6b4da4e`. A instrumentação só observa avaliações feitas pelo motor e os resultados; não recalcula utility, não escolhe ações nem muda RNG. Dois mundos novos menores, simulados por 48h com/sem observador, produziram estado exato igual. Campos objetivos do auditor são separados da percepção do NPC. Na campanha, invariantes e índice criminal foram conferidos a cada 100h. Esses validadores cobrem estrutura e alguns índices; não certificam coerência de todo efeito social ou vínculo residencial. Receber um fato/ter uma necessidade não prova que o NPC a executou. As decisões incluem resultado real, dinheiro/comida antes e depois, fontes e alternativas disponíveis.

O save final foi somente exportado; não foi carregado. Microcenários diagnósticos também nasceram de geração nova, em mundos separados. Recursos e relógio controlados nesses cenários são fixtures de reprodução, não fatos da campanha.

## 4. Evolução do mundo

| Hora | Vivos | Mortos | Raiva média | Desespero médio | Lesionados |
|---:|---:|---:|---:|---:|---:|
| 500 | 1726 | 50 | 48.88 | 70.0 | 156 |
| 1000 | 1622 | 154 | 53.3 | 90.19 | 219 |
| 1500 | 1566 | 210 | 54.06 | 90.92 | 174 |
| 2000 | 1522 | 254 | 52.13 | 91.34 | 190 |
| 2500 | 1486 | 290 | 49.58 | 91.39 | 204 |
| 3000 | 1460 | 316 | 47.91 | 91.19 | 195 |
| 3500 | 1434 | 342 | 45.29 | 91.05 | 193 |
| 4000 | 1417 | 359 | 44.38 | 91.39 | 185 |
| 4500 | 1405 | 371 | 43.67 | 92.04 | 154 |
| 5000 | 1387 | 389 | 43.51 | 91.68 | 155 |

## 5. Comparação com Mira

| Indicador | Mira em 5.000h | Vespera-47 em 5.000h |
|---|---:|---:|
| Persistentes iniciais | 1728 | 1776 |
| Abstratos iniciais | 4338 | 4461 |
| Vivos | 1340 | 1387 |
| Mortos | 388 | 389 |
| Mortos/persistentes iniciais | 22.45% | 21.90% |
| Ataques | 33121 | 27623 |
| Mudanças de residência | 595 | 490 |

A comparação usa janelas iguais. A geografia/elenco novos resultam de outra seed. As diferenças de dinâmica não isolam exclusivamente a seed: Mira foi observada antes da correção posterior de casos criminais. Também há população inicial diferente e instrumentação mais completa. Não foi carregado nem reexecutado o save de Mira; só foram consultadas suas métricas já preservadas. Mudança de frequência não é automaticamente melhora de qualidade.

## 6. Inventário de acontecimentos

| Fato/ação | Quantidade |
|---|---:|
| AbsenceNoticed | 61.568 |
| ApologyGiven | 273 |
| CalmingAttempted | 136 |
| CharacterAttacked | 27.573 |
| CharacterCaptured | 341 |
| CharacterConfronted | 1.779 |
| CharacterDefended | 10.610 |
| CharacterDied | 339 |
| CharacterFled | 5.648 |
| CharacterInsulted | 722 |
| CharacterKilled | 50 |
| CharacterReleased | 304 |
| CharacterSurrendered | 1.545 |
| CharacterThreatened | 716 |
| CharacterWarned | 167 |
| CharacterWithdrew | 207 |
| ComfortGiven | 18 |
| ConflictEnded | 10.572 |
| ConflictStarted | 4.947 |
| FamilyConcern | 40.726 |
| FamilySearch | 16.654 |
| FirstAidGiven | 50 |
| GuardResponded | 26.507 |
| HelpGiven | 2.102 |
| ImmediateHelpRequested | 271 |
| InformationShared | 4.297 |
| InvestigationPerformed | 773 |
| ItemStolen | 56.395 |
| LocalEconomicResponse | 323 |
| MigrationArrived | 491 |
| MigrationStarted | 511 |
| PersonLocated | 2.138 |
| PersonalityAdapted | 7.169 |
| ProtectionGiven | 7.723 |
| PursuitEnded | 2.762 |
| PursuitSearch | 26.749 |
| RemainsLocated | 57 |
| Remembrance | 32 |
| ResidentMoved | 490 |
| ResponsibilityFulfilled | 92 |
| RestitutionDemanded | 2.226 |
| RestitutionGiven | 23 |
| SuccessionChanged | 4 |
| SuspectLocated | 750 |
| ThirdPartyAlerted | 65 |
| ThreatAvoided | 1.111 |
| ThreatReported | 11.885 |
| WantedIssued | 29.640 |

Rumores: 1.216.179; informação estruturada: 4.297. Ativações de família/luto/vingança: 102294 / 173 / 34639. São ativações, não pessoas únicas nem missões concluídas.

## 7. Qualidade das histórias

Minha avaliação: a causalidade local e a consequência material são o ponto mais forte. Roubo gera respostas; proteção traz terceiros; combate pode terminar em fuga, rendição, captura ou morte; mudança de cidade altera o censo. Reparação e socorro mostram alternativas concretas.

A variedade ainda é desigual: muitas sequências repetem agressões e proteção, e pressões financeiras alimentam crimes sobre provisões. Arcos extensos podem ser o prolongamento de uma disputa, sem capítulos com novos objetivos. O catálogo detalhado explicita duração, repetição e desfechos, evitando tratar toda sequência longa como história boa.

Leitura narrativa crítica dos casos mais relevantes: [análise das melhores histórias e seus limites](</home/hugo/Área de trabalho/procedrual/reports/lore_vespera47_5000h/LEITURA_CRITICA_DAS_HISTORIAS.md>).

## 8. As histórias detalhadas

- L01: Conflito com morte violenta e continuidade causal — Bela Alvor (#4586), arco 58239.
- L02: Conflito com morte violenta e continuidade causal — Mira Solaris (#798), arco 93800.
- L03: Conflito com morte violenta e continuidade causal — Bela Vale (#1266), arco 38361.
- L04: Conflito com morte violenta e continuidade causal — Marie Stone (#1136), arco 33441.
- L05: Conflito com morte violenta e continuidade causal — Lyra Arven (#4684), arco 108333.
- L06: Cobrança e devolução de um bem real — Arthus Kars (#843), arco 15410.
- L07: Cobrança e devolução de um bem real — Lyra Alvor (#5123), arco 129281.
- L08: Desculpas em uma disputa — Marie Corven (#4279), arco 113068.
- L09: Desculpas em uma disputa — Bela Kars (#686), arco 133951.
- L10: Autoridade, confronto e captura — Elena Arven (#2266), arco 101317.
- L11: Autoridade, confronto e captura — John Luar (#4742), arco 10666.
- L12: Ferimento e auxílio com recursos — Bela Kars (#686), arco 108077.
- L13: Ferimento e auxílio com recursos — Nora Valerius (#621), arco 15998.
- L14: Proteção e intervenção de terceiros — Marie Stone (#5080), arco 62859.
- L15: Proteção e intervenção de terceiros — Lyra Ferros (#2964), arco 55890.
- L16: Tentativa de aliviar tensão — Cael Corven (#171), arco 71954.
- L17: Tentativa de aliviar tensão — Lyra Luar (#3429), arco 68530.
- L18: Rendição — Marie Ferros (#2064), arco 34090.
- L19: Rendição — Cael Bruma (#2697), arco 62336.
- L20: Fuga física — Ruan Kars (#917), arco 97245.
- L21: Fuga física — Silas Montes (#2538), arco 99382.
- L22: Retirada — Silas Arven (#1620), arco 130638.
- L23: Retirada — Silas Solaris (#5462), arco 24582.
- L24: Apoio após perda — Bela Douran (#3139), arco 6101.
- L25: Apoio após perda — Nora Douran (#3088), arco 20463.
- L26: Morte e sucessão política — Nora Arven (#1091), arco 23468.
- L27: Morte e sucessão política, arco 24621.
- L28: Descoberta de restos e conhecimento tardio — Tomas Kars (#4693), arco 59361.
- L29: Descoberta de restos e conhecimento tardio — Lyra Ferros (#2961), arco 134267.
- L30: Crime por avanço financeiro — Cael Hammer (#5331), arco 59.
- L31: Crime por avanço financeiro — Cael Hammer (#5331), arco 589.
- L32: Resposta de vingança após morte conhecida — Darin Vale (#4733), arco 78026.
- L33: Migração por procura criminal conhecida — Lyra Arven (#2807), arco migration:53522.
- L34: Migração por pobreza persistente — Silas Ferros (#579), arco migration:533024.
- L35: Migração por ameaça conhecida — Tomas Luar (#891), arco migration:8805.
- L36: Ração obtida, mas morte antes da refeição — Bela Douran (#3139), arco survival:3139.

## 9. Crime e motivação financeira

Roubos bem-sucedidos por necessidade (ações raiz, sem contar duas vezes uma execução interna): {'successful_theft_need:food_reserve': 7012, 'successful_theft_need:money': 10048, 'financial_thefts': 10053, 'financial_no_direct_money_gain': 10053, 'financial_already_two_food': 2826, 'successful_theft_need:advancement': 5, 'successful_theft_need:food': 39330}. O dinheiro ficou igual imediatamente após 10053 dos 10053 roubos sob objetivo money/advancement; 2826 começaram com pelo menos duas unidades de alimento. Foram identificadas 515 pessoas com pelo menos três roubos bem-sucedidos ligados à mesma necessidade financeira amostrada.

**Limite confirmado:** o roubo financeiro transfere alimento, e muitas dessas ações deixam o dinheiro igual. Isso pode economizar uma compra, mas não constitui ganho monetário direto; a necessidade de dinheiro pode continuar alimentando a mesma escolha. Sem uma sequência de revenda ou outro benefício financeiro avaliado, cria-se repetição. Prioridade antes da próxima fase: restringir essa solução à finalidade que ela realmente atende, ou implementar uma estratégia financeira completa com transferência/pagador reais e retorno de progresso. Não criar moedas ao concluir um roubo.

## 10. Combate, proteção e encerramentos

Ataques: 27623; mortes em combate: 50; proteção: 7723; socorros: 50; fugas: 5648; rendições: 1545; capturas: 341. Uma intervenção pode desviar dano para o protetor. Informação indireta com confiança baixa pode sustentar reação pessoal, mas não equivale à evidência mais forte exigida de um guarda.

Violência não está limitada a mortes naturais. Porém frequência alta, sozinha, não comprova boas relações, vingança concluída ou estratégia. Golpes sucessivos sobre fontes antigas podem dominar a história quando outras respostas têm utility baixa.

## 11. Família, luto e conhecimento

144 pares familiar/perda foram identificados nos registros de recepção. As histórias indicam quando a notícia chegou, com qual confiança e quais pressões apareciam. Uma morte não informa familiares remotos instantaneamente. Encontrar restos sem autoria pode gerar luto e não permite atribuir automaticamente culpa ao assassino que só o auditor conhece.

Contagem de necessidade de vingança não é vingança realizada. Os exemplos só recebem esse título quando uma ação executada de revenge referencia uma morte conhecida. Memória curta e prazos ainda interrompem continuidade; é desejável manter fatos relevantes de uma perda/objetivo sem promover toda notícia antiga a novo choque.

## 12. Migração e seus motivos

Motivos de partida: {'threat': 209, 'wanted': 286, 'poverty': 16}. Mudanças de residência: 490. A partida exige reserva e rota conhecida; chegada precede fixação. 89 pessoas adotaram pelo menos dois destinos diferentes, situação que expõe o bug de vínculos residenciais persistentes descrito abaixo.

Migração por família/trabalho depende de metadados de destino que ainda não são alimentados completamente. A pobreza compete com comida, renda e proteção; não deve ser interpretada como ausência de vontade de migrar apenas porque houve poucas partidas. O destino próximo conhecido pode ser escolhido sem prova de emprego melhor, favorecendo deslocamentos pouco transformadores.

## 13. Morte, fome e sobrevivência

Causas: {'hunger': 329, 'combat': 50, 'both': 3, 'thirst': 7}. Fome ou fome+sede: 332/389, 85.35%. Mortes por fome/fome+sede com alimento carregado: 1. Mortes no mapa externo: 0; por sede/fome+sede nesse mapa: 0.

**Caso observado com alimento carregado:** Bela Douran (#3139), evento#498991, morreu em h583 com fome 100, comida 1 e última ação `steal_person` em h582.

**Falha de integração confirmada na campanha:** Bela Douran (#3139) executou steal_person em h582 com HP=1, fome=100 e comida=0. Depois estava com comida=1, mas a fome continuava 100. No fechamento em h583, a fisiologia matou o personagem antes de uma próxima refeição. O roubo pessoal da Fase 4 não está nas aquisições reconhecidas por FeedingSystem. Ele entra depois da conversão para ações de refeição, estimate retorna None e a solução passa sem verificar se a comida será consumida a tempo. steal_meal apareceu como alternativa com score 59,03, enquanto steal_person venceu com 61,10. Prioridade P1: integrar essa aquisição ao cálculo de sobrevivência e, quando aplicável, à operação de refeição; não criar alimento nem apagar fome sem consumo real. História L36 e decisão do evento#498585 conservam os estados completos.

Comida na cidade não significa posse, renda ou acesso do indivíduo. Este relatório não mede o estoque municipal no instante de toda morte e não usa estoque final como prova retrospectiva. Esse caso isolado não explica automaticamente as outras 331 mortes por fome/fome+sede. Ferimento, detenção, viagem e disputa por prioridade podem afetar a sobrevivência. Associação com ataques não deve ser contada como assassinato adicional. Para resolver dúvidas alimentares restantes, registrar uma janela de decisões vitais e oportunidades reais por vítima.

## 14. Viagens e reserva de água

Mortes por sede no mapa externo exigem conferir roteiro, duração real, terreno e reservas antes da partida. O planejamento mínimo estima sede a 2/h, enquanto a fisiologia no deserto usa 4/h. Isso é uma **limitação confirmada da estimativa**; não prova, por si só, que causou cada morte. Nesta sessão ocorreram 0 mortes por sede/fome+sede fora das cidades.

Melhoria: estimar o caminho que o NPC conhece, usar margem para trechos incertos, reconhecer fontes visitadas e reconsiderar partida/abastecimento quando a cobertura não basta. Não consultar poços desconhecidos nem reabastecer automaticamente o viajante.

## 15. Emoções e equilíbrio

Estado final dos vivos: {'anger': {'mean': 43.51, 'over50': 629, 'maximum': 100.0}, 'resentment': {'mean': 74.08, 'over50': 1050, 'maximum': 100.0}, 'humiliation': {'mean': 49.57, 'over50': 701, 'maximum': 100.0}, 'desperation': {'mean': 91.68, 'over50': 1281, 'maximum': 100.0}}. Causas factuais: {'ItemStolen': 172761, 'CharacterAttacked': 34390, 'CharacterThreatened': 855, 'CharacterInsulted': 888, 'CharacterDied': 73, 'CharacterKilled': 14}. Pobreza persistente, fome, luto e combate sustentam desespero. Uma média alta pode indicar pressão contínua; não mede profundidade.

Melhoria: diferenciar baixa liquidez, privação real e perda grave; avaliar recuperação quando há alimento, renda/apoio e segurança suficientes. Não apagar consequências de perdas para criar final feliz. Na campanha houve 0 eventos de adaptação anunciando incremento em traço que já estava no teto, conforme valor inicial e sequência de mudanças: o estado continua limitado, mas o texto/contexto da mudança precisa usar o delta efetivo.

## 16. Reputação e reparação

Microcenário novo confirmou: desculpa cria tag reparador=8, medo=4 e admiração=0, com score reputacional social inalterado. A interpretação genérica trata tags fora de prestativo/leal/responsável como medo, incluindo reparação. Isso é incoerência semântica de estado, mesmo que confiança/emoção também melhorem.

Correção indicada: classificar efeitos positivos, negativos e neutros explicitamente; uma desculpa deve alterar medo somente quando houver motivo contextual. Medir reputação antes/depois de reparação com dano prévio, sem presumir perdão total. As opiniões continuam individuais; o auditor não deve impor uma reputação universal.

## 17. Autoridade e punição repetida

**Bug confirmado por reprodução:** houve somente um roubo; o guarda encerrou seu caso, perdeu a lembrança curta e reaprendeu o mesmo fato antigo. Surgiu novo caso com a mesma origem e uma segunda captura cobrou outra multa. Dinheiro do suspeito: 12→7→2. O caso encerrado estava persistido, mas on_fact não deduplicou a origem já encerrada pelo próprio guarda. Uma segunda reprodução confirmou que reaprender o próprio WantedIssued dentro de 168h pode reativar o mesmo registro já conhecido como encerrado: a segunda captura retirou mais 5 moedas (11→6).

Na campanha, o catálogo identificou 33 novos WantedIssued com a mesma origem já encerrada pelo mesmo guarda. Essa contagem marca reabertura, não prova multa duplicada em todos. Também há 0 cobranças posteriores por mesmo guarda/record_id já encerrado; eventos: []. São sinais concretos para inspeção por caso; não confundem novos delitos com reaprendizado do antigo. Evidências: [234659, 275894, 303547, 318729, 367477, 425195, 723710, 927203, 1113451, 1186702, 1295691, 1364179, 1516565, 1540683, 1550403, 1707554, 1849853, 1868535, 1876429, 2153825, 2158574, 2199750, 2222107, 2240028, 2370500, 2383144, 2667435, 2872041, 3346981, 3401922]. 0 procuras tinham origem conhecida de mais de 168h; isso deve ser revisado com a política de validade, sem confundir falta de notícia sobre resolução com onisciência.

Correção prioritária: manter identidade/resultado do caso por origem/jurisdição e conhecimento próprio; reaprender o mesmo delito encerrado não é delito novo. Outro guarda que ignora a resolução pode investigar, mas deve poder obter a informação institucional local. Não bloquear usando automaticamente um encerramento remoto desconhecido.

## 18. Residência e consistência do grafo

**Bug confirmado:** duas mudanças reais deixam reside_em=100 nos dois destinos. O censo e town_id mantêm só a residência atual; o grafo conserva a anterior com o mesmo significado de atual. A reprodução separada terminou com censo apenas na cidade 50 e vínculos ativos nas cidades 32 e 50. Na campanha, 89 pessoas passaram por dois ou mais destinos distintos.

Corrigir a relação atual ao transferir residência; conservar trajetória em evento/registro histórico próprio. Também revisar filiação e lealdades quando a mudança cruza reinos: morar em outro lugar não deve, sem decisão explícita, apagar identidade familiar ou política.

## 19. Identidade e apresentação

209 nomes completos aparecem em mais de um personagem. IDs preservam identidade no código, mas texto sem cidade/profissão/ID pode sugerir que uma pessoa fez atos de outra. É um problema de legibilidade e continuidade, não prova de personagens fundidos.

Melhoria: identificação estável em diário/interface, com local, ocupação e alcunha quando cabível. Traduzir os verbos internos dos eventos e distinguir protegido, agressor, cobrador e dono do bem devolvido. Não renomear pessoas retroativamente nem deduzir parentesco pelo sobrenome.

## 20. Reinos, sucessão e limites políticos

| Reino | Situação final | Governante final | Profissão | Sucessões nesta sessão |
|---|---|---|---|---:|
| Reino Stone | estável | Vespera-47 (#245) | governante | 0 |
| Reino Ferros | estável | Silas Ferros (#579) | estudante | 1 |
| Reino Montes | estável | Bela Montes (#872) | governante | 0 |
| Reino Arven | crise sucessória | sem governante | — | 2 |
| Reino Kars | estável | Aldren Kars (#1398) | governante | 0 |
| Reino Vale | estável | Nora Vale (#1750) | estudante | 1 |

A sucessão mínima troca ruler_id e não atualiza necessariamente profissão/rotina do herdeiro. Quando o governante final permanece estudante/conselheiro, isso é uma lacuna de integração a revisar; não equivale a disputa formal pelo trono. Religiões, títulos e templos gerados não representam deuses agindo. Não foram implementadas guerras, revoluções ou exércitos nesta fase; conflitos individuais não são descritos como guerra.

## 21. O que não constitui bug por si só

NPC fugir, mentir, abandonar proteção, agir por rumor, não ajudar ou fracassar pode ser coerente com personalidade, informação, risco e recursos. Um arco interrompido por morte/afastamento também é válido. A crítica deve verificar objetivo, alternativas, percepção e resultado, sem exigir comportamento ideal. Gravidade de um assassinato tampouco obriga toda a cidade a saber instantaneamente.

## 22. Suspeitas que precisam de diagnóstico adicional

1. Reserva insuficiente em viagens pelo deserto: cruzar rota, água e relógio por vítima.
2. Proteção perpetuando agressões: conferir vínculo com vítima/agressor e scores ao longo do arco.
3. Desespero quase permanente apesar de recursos: separar renda baixa, estoque individual, perdas e perigo.
4. Restituição resolvendo emoção do cobrador, mas não do dono: comparar target_id/owner_id e respostas do proprietário.
5. Papel/rotina após sucessão ou mudança de reino: confirmar autoridade, renda e compromisso próprios.

Essas hipóteses não são automaticamente contadas como bugs de toda a campanha; as reproduções confirmadas estão separadas acima.

## 23. Prioridades antes de novas fases

| Prioridade | Ação | Por que | Como verificar |
|---|---|---|---|
| P1 | Integrar roubo pessoal à refeição/sobrevivência | Obter alimento sem tempo para consumi-lo foi tratado como solução viável | HP=1, fome100, alvo local com ração: transferência, consumo e fechamento da hora |
| P1 | Deduplicar caso encerrado ao reaprender origem/aviso | Evitar nova perseguição/multa pelo mesmo delito | Evicção da memória, notícia velha, mesmo guarda/caso |
| P1 | Dar progresso real a soluções financeiras | Evitar roubo de alimento repetido sob necessidade de dinheiro | Transferências, renda/estoque antes/depois, repetições do mesmo objetivo |
| P2 | Conferir sobrevivência em viagens | Corrigir estimativa de água; não houve morte em viagem nesta campanha | Rotas/terreno conhecidos, reservas e decisões durante viagem |
| P2 | Atualizar grafo de residência e separar histórico | Evitar dupla residência atual e conflitos futuros de filiação | Duas mudanças, censo e relações |
| P2 | Corrigir semântica de reputação reparadora | Evitar desculpa aumentando medo sem causa | Tags, confiança, medo e admiração antes/depois |
| P2 | Alimentar destinos conhecidos por família/trabalho | Criar motivos concretos além de ameaça/crime | Informação obtida, vaga/familiar real, deslocamento e resultado |
| P2 | Melhorar continuidade dos objetivos pessoais | Dar passos intermediários a luto/proteção/ambição | Fontes relevantes, prazo, resolução observada |
| P3 | Usar deltas reais nas mudanças de personalidade | Prevenção: sem ocorrência no teto nesta sessão | Valores anterior/final e evento emitido |
| P2 | Desambiguar personagens e traduzir diário | Tornar lore legível | Mesmo nome em pessoas diferentes e sequência por ID |
| P3 | Conter histórico e melhorar performance | Permitir expansão sem ampliar custo indefinidamente | Memória, tamanho de save e registros acumulados |

## 24. Performance e crescimento de registros

Tempo observado: 2100.2s; decisões totais: 3.171.116; decisões narrativas raiz registradas: 267.321. Memória máxima aproximada na simulação (inclui observador; não é benchmark puro do motor): 511.82MiB. Save exportado: 231.98MiB; serialização: 20.725s. Não houve teste por carregamento de save nesta solicitação.

FactImpact acumulados: 595.377; opiniões registradas: 64.439; casos criminais arquivados/ativos: 29.640. Guardar toda contribuição ajuda deduplicação, mas cresce mesmo com memórias curtas. Separar resumo histórico e fatos ativos pode conter custo, preservando a identidade das origens para não reintroduzir punição/emoção duplicadas.

## 25. Conclusão para a próxima fase

O mundo produz histórias individuais com consequências e já permite observar variação entre ambientes. A próxima expansão deve reaproveitar esse material, mas é melhor corrigir primeiro as inconsistências demonstradas e o progresso de objetivos econômicos. A prioridade é melhorar a coerência e o desfecho dos sistemas existentes. Mais guerras, deuses ou política ampla sobre casos duplicados, papéis residenciais conflitantes e forte pressão alimentar ampliariam problemas já visíveis.
