# Fase 4 — registro de desenvolvimento

Especificação completa lida: `fase_4.md` (2230 linhas).
Baseline intacto em baseline_code, versão mvp-4-fase3.2-final. Regras atuais em desenvolvimento mvp-5-fase4; geração-base mvp-4 permanece para geografia.

Usuário resolveu conflito demográfico: equilíbrio, sem elenco pequeno nem imenso. Implementar multiplicador inicial aproximadamente 4 (Mira432→1728), redimensionar total local para 2–3 abstratos por persistente, preservar 73 localidades/6 reinos/mapa e geografia. Inserir expansão DEPOIS de toda geração antiga para não consumir RNG antes das cidades/reinos. Redes esparsas de famílias3 e amizades; novos guardas/mercadores/conversores proporcionais. Não repor legado do morto.

Implementação planejada:
- modelos: EmotionalState, Grievance, CombatState, WantedRecord, MigrationState (já adicionados); versão e regras Interactions (já).
- emotions.py criado: estados, apoio/reparação, atribuição apenas fatos próprios, modificação lenta+1/mês até5, nunca decisões em callback. Revisar perdas por morte sem violência também.
- Engine.finish_death único caminho para privação/combate/self_harm, corpse items retained, population counted once, politics also CharacterKilled. Existing physiology/rest unchanged except wound rehabilitation via execution.
- conflicts.py: enumeração integrada Goal.solutions, utility contextual, execução local attack/defend/flee/surrender/intervene/protect/capture + threat/confront/demand_return/insult/apologize/withdraw/warn/call_help/calm/forgive/first_aid. Morto/detido/truce não atacado indevidamente. Arma própria objetiva vs arma alheia observada aproximada. Lesão simples reduz trabalho/movimento; tratamento tempo+água/comida reais.
- justice.py: guards learn facts threshold60 ownjurisdiction; WantedRecord authority membership/known_by persistent, no access global suspect position, capped pursuit168h/search exhaustion. Wanted notices only local witnesses (targetTown, suspect incontext, avoid default remote participant disclosure). Capture surrendered/incapacitated, fine existing, detention12h/release, no teleport.
- migration.py: one/two known towns from public local route/signpost generation plus facts; real gate→external cardinalsteps→destinationgate→visitor24h→residence transfer. Supplies/known distance, alternate economy reads physical town for visitor. Keep cTown old until residence transfer; no duplicating census. Individual relocation only.
- emotion extreme fatal possibility abstract only, >720h,≥3 known losses, desperation98+, zero support, deterministic veryrare eligibility; no methods, no default grief.
- LOD active1h for conflict/pursuit/migration/critical event, normal3–6, background6–12; physiology hourly. Critical fact active_until promoted. Clamp combat elapsed1.
- spatial/census/bounded candidates and profession loops remove world global scans. No all-to-all. Current gossip uses spatial already.

Validação autorizada: 10–20 regressões essenciais combinadas (tests/test_phase4.py), somente módulos relacionados durante implementação. Suíte anterior179 completa UMA VEZ final; depois somente casos falhos. Microcenários→curta500–1000h→UMA longa Mira global10000h. Não fazer3 longas nem replayintegral10k desnecessário. Relatório34seções, evidência de histórias bastante ampla. Benchmark tempo/memória/save/load/decisões/events, distribuiçãoemoções e crimes/combates/migração, nada de metas artificiais de ataques.

Ainda não alterar docs anteriores/saves/testes originais. Nenhuma guerra, magia, religião atuante, revolução, exércitos, nascimento/idade/herança/caravanas.

## Integração e bugs observados

Implementados os quatro serviços dentro de Need/Goal existentes, persistência de status/estados, população Mira1728/4338 e geografia idêntica. Vinte regressões compostas; duas últimas justificadas por comportamentos observados.

A primeira auditoria curta foi INTERROMPIDA pelo validador em500h: NPC4058 interceptou seu próprio ataque ao atingir alguém protegido anteriormente. Evento423845/423846 em495h registra ator=alvo4058. Arquivos completos preservados em auditoria_curta_v1_falha_500h. Corrigido filtro de interceptação própria e de defensor rendido/detido.

Também observado: um caso podia continuar perseguido após GuardResponded/multa. Casos agora encerram por fato conhecido; cada guarda possui status, gravidade, fonte e localização individuais. Multa não se repete sem novo delito. Mudança de residência possui336h de adaptação e reinicia avaliação financeira local para reduzir deslocamentos circulares. Cobrar devolução só participa das alternativas com evidência de roubo.

Falha em teste de continuação após ataque: RNG era salvo apenas no fechamento de hora. Goal.execute agora sincroniza estado aleatório após resolução de qualquer ação, incluindo tentativa de fuga fracassada.

Nenhum valor vital de fome/sede/dano por privação, limiar de refeição ou preço mínimo foi alterado. Ferimento reduz eficiência do lote de trabalho/movimento e se recupera com descanso apto.

## Congelamento oficial

SHA256 do núcleo:1ed1227dae6b8e7a31e9b262489e0d73b2f240d06fbd94ca507d337891871b2e. Cópia em codigo_congelado/procedural. Auditoria oficial Mira global10000h iniciada após vinte regressões passarem. Instrumentação verificada48h com361 observações de decisões: estado final idêntico ao motor sem observador.

Suíte anterior179 executada UMA vez. Doze casos falharam nessa passagem: dez regressões se resolveram ao preservar a escala dos mundos reduzidos e validar mercado inexistente/RNG/índice institucional; somente esses casos foram retestados. Duas expectativas da Fase2 foram atualizadas de maneira explícita: ataque passa a existir após autoria conhecida; cenário sem solução usa estudante honesto, porque estudante desonesto pode considerar crime. Ambos retestados e aprovados. Originais históricos preservados em baseline_code/tests.

Auditoria curta corrigida atingiu1000h com124 mortos (110fome/14combate),90capturas,290mudanças de residência; invariantes verificados a cada100h. Falha posterior de instrumentação ao usar callback ligado a arquivo fechado não alterou o checkpoint1000h. Resumo recuperado do save já existente, com comparação de continuação24h sem repetir campanha.

A inspeção de memória levou a reutilizar pursuit por suspeito, evitando acumular objetivos novos a cada delito. Índice de casos ativos e fila de expiração substituem varredura de casos encerrados. Emoções usam contribuição factual persistente para impedir aumento repetido ao reaprender um rumor cuja memória curta expirou. Mudança de personalidade exige ao menos720h entre adaptações. Uma tentativa de fuga fracassada consome a hora da ação.

## Resultado oficial e correção posterior

A única campanha oficial completou 10.000 horas: 1.218 vivos, 510 mortos,
53.280 ataques, 547 capturas e 918 mudanças de residência. Causas: 416 fome,
6 sede, 1 fome+sede e 87 combate. Tempo de simulação: 3.575,816 segundos.
Os invariantes foram verificados a cada 100 horas e o save final foi escrito.
A continuidade original versus o save carregado divergiu nas 24 horas seguintes.

O resumo foi recuperado do checkpoint e dos arquivos causais/log, sem nova
campanha. Emoções e lesões intermediárias não sobreviveram ao encerramento do
processo; estão marcadas como ausentes, sem números estimados. Tempos de
serialização/carga foram medidos novamente e identificados como recuperação.

Microcenário reproduziu um bug: o guarda conhecia um caso antigo cujo
encerramento não havia visto, além de uma nova agressão. A necessidade escolhia
o caso grave, enquanto a execução escolhia o antigo; fechar esse caso podia
apagar o índice de outro caso ativo. O motor carregado reconstruía o índice e
passava a se comportar de modo diferente. Evidência preservada em
reproducao_divergencia_codigo_congelado.json.

A correção posterior agrupa a pressão por suspeito e escolhe a maior gravidade
conhecida; execução e necessidade usam o mesmo caso. Multas por roubo não
encerram acusações mais graves. Resolução fecha casos conhecidos pelo guarda,
mantendo outros casos ativos no índice e a privacidade da informação. A primeira
verificação posterior teve igualdade exata, mas detectou índice incompleto
diante de casos sobrepostos herdados do checkpoint: foi preservada como
verificacao_pos_auditoria_v1_indice_falho.json, e o índice passou a manter
todos os casos ativos por suspeito.

Os 20 testes direcionados foram reexecutados após a correção, incluindo o
microcenário no caso 19. A continuação posterior de 24 horas compara o motor
contínuo com recarga no meio, em 10.012h. Seu resultado e hash do núcleo entregue
estão em verificacao_continuidade_pos_auditoria.json. O código congelado que
produziu a campanha continua intacto; a correção posterior não é apresentada
como tendo passado por uma segunda campanha de 10.000 horas.
