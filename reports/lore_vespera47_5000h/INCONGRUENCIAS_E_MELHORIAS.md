# Incongruências, hipóteses e prioridades

## 9. Crime e motivação financeira

Roubos bem-sucedidos por necessidade (ações raiz, sem contar duas vezes uma execução interna): {'successful_theft_need:food_reserve': 7012, 'successful_theft_need:money': 10048, 'financial_thefts': 10053, 'financial_no_direct_money_gain': 10053, 'financial_already_two_food': 2826, 'successful_theft_need:advancement': 5, 'successful_theft_need:food': 39330}. O dinheiro ficou igual imediatamente após 10053 dos 10053 roubos sob objetivo money/advancement; 2826 começaram com pelo menos duas unidades de alimento. Foram identificadas 515 pessoas com pelo menos três roubos bem-sucedidos ligados à mesma necessidade financeira amostrada.

**Limite confirmado:** o roubo financeiro transfere alimento, e muitas dessas ações deixam o dinheiro igual. Isso pode economizar uma compra, mas não constitui ganho monetário direto; a necessidade de dinheiro pode continuar alimentando a mesma escolha. Sem uma sequência de revenda ou outro benefício financeiro avaliado, cria-se repetição. Prioridade antes da próxima fase: restringir essa solução à finalidade que ela realmente atende, ou implementar uma estratégia financeira completa com transferência/pagador reais e retorno de progresso. Não criar moedas ao concluir um roubo.

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
