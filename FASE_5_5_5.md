# FASE 5.5.5 — correção, tratamento, limpeza e observabilidade histórica

**Concluída.** Base: `mvp-12-fase5.5` → atual: `mvp-13-fase5.5.5`. Geração: `mvp-5.4`. Formato de save: **2**.

**341 testes ativos passaram; B01–B08 corrigidos; continuidade e neutralidade passaram; campanha nova de 300h concluída.** Não houve ajuste de produção, dano de privação, prioridade fisiológica, frequência de violência ou thresholds para aumentar eventos raros.

## 1. Estado inicial e escopo

A auditoria anterior registrou 326 testes: **305 PASS, 18 FAIL e 3 ERROR**. Os 21 resultados não verdes foram examinados individualmente. Nenhum teste foi desativado ou marcado como sucesso esperado para esconder uma falha. Foram acrescentados **15 testes**, resultando nos 341 atuais.

O trabalho ficou nas correções confirmadas, eliminação de implementações contraditórias, contratos de consulta e Observabilidade Histórica V1. Não foram implementados nascimentos, idade, gerações, guerra entre reinos, eleições, diálogo geral, novas profissões ou nova fase de balanceamento.

A auditoria de origem continua preservada em [Radiografia anterior](</home/hugo/Área de trabalho/procedrual/reports/auditoria_total/RADIOGRAFIA_TOTAL.md>). Seus diagnósticos de bugs descrevem a versão anterior, não o estado atual.

## 2. B01–B08: causas, correções e prova

| Bug | Causa | Correção | Verificação | Código |
| --- | --- | --- | --- | --- |
| B01 | Contextos compartilhavam listas/dicionários do mundo e entre Facts. Save/load rompia o alias e a história divergia. | Event e Fact fazem deepcopy na construção: a proteção cobre todos os produtores, inclusive coleções aninhadas/conjuntos. O pós-morte não altera mais CharacterKilled; PostKillAppraisal é separado e aponta para a morte. Persistência aceita conjuntos tipados. | Snapshots aninhados; independência entre ouvintes; adesão após load com igualdade integral; pós-morte separado. | [Event](</home/hugo/Área de trabalho/procedrual/procedural/models.py:741>); [Fact](</home/hugo/Área de trabalho/procedrual/procedural/models.py:291>) |
| B02 | Society.react retornava antes de atribuir responsabilidade; a autoridade ativa não fazia essa consequência. | Institutions.react_decision concentra registro, falhas e responsabilidade em recusa conhecida com confiança ≥60. Repetição não duplica; melhoria de confiança pode completar a atribuição. Ramo morto removido. | Decisão não recebida não atribui; recebida atribui; duplicação e confiança melhor testadas; assume_local_office volta a respeitar as pré-condições. | [Institutions.react_decision](</home/hugo/Área de trabalho/procedrual/procedural/institutions.py:336>) |
| B03 | Preparação recriava fill_water depois dos filtros normais, inclusive em cooldown ou fonte sem água conhecida. | GoalSystem.eligibility é usada pela avaliação e pela preparação. Verifica falha/cooldown, mapa/acesso, fonte conhecida, existência do poço e disponibilidade observável. Fonte local pode ser inspecionada; ausência remota só é usada quando conhecida recentemente. | Preparo bloqueado por cooldown, observação remota de falta e fonte local vazia. Sem alterar água produzida, sede ou dano. | [GoalSystem.eligibility](</home/hugo/Área de trabalho/procedrual/procedural/goals.py:679>) |
| B04 | Via de Access/found_faction pulava score e presença exigidos no fluxo de reuniões. | can_formalize reúne liderança, estado, tipo do grupo, idade, membros presentes, investimento, contribuições, score e limites. Todos os entrypoints revalidam a mesma função. A alternativa de Access usa o encontro presente, sem deslocar o ator para longe dos fundadores. | Dois presentes são rejeitados pelas duas vias; estado maduro válido formaliza com débito pessoal real. Fixtures antes aceitas pelo atalho agora satisfazem o score. | [Institutions.can_formalize](</home/hugo/Área de trabalho/procedrual/procedural/institutions.py:522>) |
| B05 | O candidato existia por food OU water; execução podia escolher justamente o recurso ausente. | MaterialCandidate → Solution → Goal transportam resource_kind e quantidade. A alternativa prefere o recurso da maior privação quando disponível, ou o recurso existente; execução respeita a intenção e revalida estoque/presença. | Organização com comida e sem água, membro com mais sede: transfere a comida escolhida, sem fabricar recurso. | [Institutions.faction_candidates](</home/hugo/Área de trabalho/procedrual/procedural/institutions.py:605>) |
| B06 | Need reutilizada guardava group_id e faction_id, e consumidores escolhiam entidades diferentes. | organization_type/organization_id são canônicos. O alias correspondente é mantido para consumidores antigos, sempre exclusivo. bind_organization elimina o oposto; pressão, candidato e execução leem a mesma identidade. Contexto ambíguo é inválido. | Reuso facção→grupo, chave de pressão, inexistência de candidato da facção e recusa de execução sobre organização diferente. | [bind_organization](</home/hugo/Área de trabalho/procedrual/procedural/organization_context.py:13>) |
| B07 | Causas que caíam no fallback, como exploration, eram descritas como autoinfligidas. | Descrições explícitas para privação, combate, self_harm, exploração e divina. Causa desconhecida aparece pelo identificador real, sem inventar semântica. | Exploração e causa desconhecida preservam causa e texto coerentes. | [Engine.finish_death](</home/hugo/Área de trabalho/procedrual/procedural/engine.py:193>) |
| B08 | report_congregation era produzido por Faith, mas não tinha entrada em Utility.BASE. | Base igual à comunicação institucional report_to_faction (45), com dever/diligência (20), devoção (25) e penalidade de viagem já existente. A candidatura continua exigindo perdas conhecidas e cooldown; execução continua exigindo canal ritual físico. | Orações testemunhadas + duas mortes conhecidas → produtor → Utility → Goal → execução; sem KeyError. Não foi apenas acrescentado um número sem semântica. | [evaluate](</home/hugo/Área de trabalho/procedrual/procedural/utility.py:82>) |

### Correções de integração necessárias

A responsabilização ativa revelou uma segunda contradição: aprender a resposta já atualizava o grupo, e o filtro antigo passava a considerar impossível retransmiti-la. A entrega aos demais agora tem confirmação própria (`relayed_responses`, limitada a 12 IDs), exige representante e outro membro presentes e não repete a consequência institucional. Retransmitir concorre com as ações locais já elegíveis; não bloqueia artificialmente a tomada de cargo.

Um ataque que mantém decisão letal ativa também passou a usar na seleção o mesmo `LethalDecisionSystem.action_audit` exigido na execução. Isso evita oferecer um ataque cuja incapacidade física já o torna inexequível; não alterou dano, score letal ou limiar de capacidade.

`Society.promote` trata vínculo/assignment inválido com retorno False. Convite, aceitação e promoção continuam sendo etapas distintas.

## 3. Legado: classificação e remoção

A análise considerou chamadores no código, strings de ação/dispatch, listeners/callbacks, fixtures e chamadas medidas na auditoria anterior. Contagem de um método inteiro não é cobertura de seus ramos. Nenhum uso externo fora do repositório foi presumido.

| Símbolo | Classificação | Evidência | Ação |
| --- | --- | --- | --- |
| Society.react / ramo posterior de PolicyDecided | LEGACY_UNREACHABLE | return incondicional depois de Institutions.react_decision; listeners chamam o wrapper ativo. 1.524.247 chamadas do método na auditoria anterior, sem prova de execução do ramo morto. | Ramo removido; wrapper único preservado. Responsabilidade transferida à implementação ativa. |
| Society.candidates / segundo ramo political_pressure | LEGACY_UNREACHABLE | Primeira linha já retorna Institutions.collective_candidates. Chamadas naturais do método inteiro: 938.155; a impossibilidade do ramo é estática. | Ramo removido; provedor canônico preservado. |
| Society.candidates / fallback de grupo e fallback da liderança de facção | LEGACY_UNREACHABLE | CollectiveAction.candidates retorna antes para grupo ativo e para liderança de facção; estado encerrado não é razão para reativar a regra antiga. | Regras duplicadas removidas; tarefas de membros não líderes continuam no caminho ativo. |
| Society.material | TEST_ONLY | Nenhum chamador produtivo/callback/dispatch no repositório; uma fixture antiga; zero chamadas naturais na auditoria. Substituída por Policy e policy_work. Uso externo fora do repositório não foi alegado. | REMOVED; teste agora exige orçamento, trabalhador conhecido, grão debitado e alimento produzido materialmente. |
| Society.decision_scores | COMPATIBILITY_WRAPPER | Testes locais chamam o símbolo; zero chamadas naturais anteriores. Uma linha delega para Institutions.decision_scores. | Preservado sem segunda fórmula; classificado COMMAND porque pressure atualiza a proposta. |
| Access.membership | COMPATIBILITY_WRAPPER | Usado por Access.execute e fixtures; três chamadas naturais medidas na auditoria anterior. | Preservado como delegação para Institutions.membership. |
| formalize_organization | COMPATIBILITY_WRAPPER | Ação ainda reconhecida por Utility e dispatcher Access. A via antiga pulava score e presença mínima. | Preservada, redirecionada para formalization/can_formalize; FoundFaction revalida a mesma regra. |
| Institutions / CollectiveAction / Society.execute | ACTIVE | Fornecedores e dispatchers chamados pelo motor, testes e decisões medidas; funções distintas para proposta, política material e resposta. | Responsabilidades explicitadas; sem materialização política instantânea paralela. |
| AGENCY.maximum_aspirations / AGENCY.no_progress_hours | DEAD | Campos declarados sem leitores produtivos, callbacks ou acesso dinâmico correspondente. Duração/abandono reais usam outras fórmulas. | Removidos; nenhuma regra foi ligada artificialmente às constantes. |
| SURVIVAL.normal / moderate / severe | ACTIVE | Leitores internos em SurvivalRules.band usam self; ausência de SURVIVAL.campo fora da classe não significa ociosidade. | Preservados. |
| experiments.total_proofs | TEST_ONLY | Reprodutor histórico da auditoria sobre mvp-12-fase5.5; não faz parte da suíte ativa tests. | Preservado como evidência histórica; não deve ser executado sobre a versão corrigida esperando reproduzir os bugs. |

Evidências pesquisáveis: [legado.json](</home/hugo/Área de trabalho/procedrual/reports/fase_5_5_5/legado.json>) e [referencias_legado.json](</home/hugo/Área de trabalho/procedrual/reports/fase_5_5_5/referencias_legado.json>).

As duas constantes removidas não foram ligadas a regras novas. O abandono de compromissos continua usando a fórmula existente de pressão/falhas/persistência e sua duração máxima. `SURVIVAL.normal/moderate/severe` foram mantidas: têm leitores internos em `band`, embora não apareçam como acessos externos `SURVIVAL.campo`.

## 4. Os 21 testes antigos não verdes

“Depois: PASS” significa execução na suíte completa final. A causa foi classificada antes de atualizar a expectativa ou a fixture.

| Teste | Antes | Classificação / causa | Ação tomada | Depois |
| --- | --- | --- | --- | --- |
| test_phase45.Phase45Tests.test_12_lethal_incapacity_requires_new_moral_decision | ERROR | OUTDATED_FIXTURE: A perda referida não possuía vínculo próximo suficiente no cenário; o ataque não formava decisão letal persistente. | Vínculo próximo explícito; mantém a comparação entre poupar e desfecho fatal real. | PASS |
| test_phase46.Phase46Tests.test_02_extreme_convergence_and_evidence_trace | ERROR | OUTDATED_TEST: loss_importance deixou de integrar o retorno da avaliação moderna. | Verifica known_close_loss, world_pressure e os fatos conhecidos que sustentam a decisão. | PASS |
| test_phase5.Phase5Tests.test_10_promotion_not_xp_or_money_only | ERROR | OUTDATED_FIXTURE: Recrutar agora comunica convite; não registra aceitação do convidado. | Executa contato/avaliação/aceitação antes da promoção; promote também retorna False para vínculo/assignment ausente (robustez). | PASS |
| test_feeding.FeedingTests.test_meal_at_normal_threshold_uses_most_nutrition | FAIL | INVALID_EXPECTATION: Fome 35 é oportunidade normal; fé pode ganhar a competição entre Needs. | Testa escolha/execução de eat dentro da Need food e mantém os testes globais de emergência; não elevou prioridade da fome. | PASS |
| test_phase4.Phase4Tests.test_15_population_balance_geography_identity | FAIL | OUTDATED_TEST: 1728 NPCs / 73 localidades eram números anteriores à geração 5.4. | Confere faixa atual, 104/60/18 residentes por tipo, proporção abstrata e identidade da geografia entre densidades. | PASS |
| test_phase41.Phase41Tests.test_06_recovery_ends_and_material_despair_falls_gradually | FAIL | OUTDATED_FIXTURE: Faltava reserva alimentar: aos 76 HP a reserva e o expediente venciam a recuperação de baixa prioridade. | Adiciona provisões reais à fixture de estabilização; mantém 12h, HP≥80, redução de desespero material e preservação do luto. Prioridades do mundo não foram ajustadas. | PASS |
| test_phase45.Phase45Tests.test_16_interlocal_following_uses_only_known_lead | FAIL | OUTDATED_FIXTURE: Local conhecido podia ser a própria cidade; lugar conhecido não concede rota. follow_lead é compatibilidade para Geography.travel. | Ensina uma conexão real entre localidades diferentes, fornece provisões e verifica route_travel/Journey; limpa lugar/rota para validar desconhecimento. | PASS |
| test_phase46.Phase46Tests.test_03_low_confidence_and_unknown_author | FAIL | OUTDATED_TEST: A causa letal atual filtra evidência abaixo de 60; a certeza de uma causa admissível passa a zero. | Exige confiança zero, low_confidence e indisponibilidade, mantendo o controle sem autor conhecido. | PASS |
| test_phase5.Phase5Tests.test_06_group_response_requires_received_decision | FAIL | CONFIRMED_BUG: B02: ramo que atribuía responsabilidade era inalcançável. | Institutions.react_decision é a única autoridade; a expectativa original passa sem afrouxamento. | PASS |
| test_phase5.Phase5Tests.test_21_divine_death_is_separate_and_not_automatic_apotheosis | FAIL | OUTDATED_FIXTURE: Posição espiritual do deus não garante acesso físico desde 5.4. | Constrói manifestação física controlada antes de testar morte/essência; preserva separação de apoteose. | PASS |
| test_phase5.Phase5Tests.test_22_claimed_essence_transforms_domain | FAIL | OUTDATED_FIXTURE: Não havia manifestação física, portanto não era liberada a essência. | Satisfaz o acesso físico na fixture; preserva testes do domínio transformado, crença, singularidade e persistência. | PASS |
| test_phase5.Phase5Tests.test_26_situational_lethality_requires_immediate_extreme_threat | FAIL | OUTDATED_TEST: O modelo moderno distingue reactive_threat e a lesão atribuída persistente que pode continuar como retributive. | Verifica os modos e a causa persistente corretos; não obriga o motor a apagar lesão depois de quatro horas. | PASS |
| test_phase5.Phase5Tests.test_28_save_limits_query_purity_and_seeded_continuity | FAIL | CONFIRMED_BUG: solutions modificava planos/diagnósticos na consulta. | QUERY em cópia isolada; o ciclo executável usa plan_solutions. Mantida igualdade integral do save e consultas de interface. | PASS |
| test_phase5.Phase5Tests.test_29_office_contact_and_known_physical_faction_route | FAIL | OUTDATED_FIXTURE: Relatório organizacional era tratado como teleporte entre mapa global e cidade. | Exige rejeição sem percurso, confirma posição e depois testa o relatório em presença real; restante da sucessão/residência é preservado. | PASS |
| test_phase5.Phase5Tests.test_30_public_reply_is_physical_and_remote_status_is_not_knowledge | FAIL | OUTDATED_FIXTURE: Outros membros presentes na administração aprendiam a resposta legitimamente. | Afasta todos os membros para testar ausência de notícia, depois retorna o representante ao quadro público. | PASS |
| test_phase51.Phase51Tests.test_02_grave_known_loss_enables_intention_execution | FAIL | REAL_REGRESSION: O candidato attack podia ignorar incapacidade exigida pela execução de uma decisão letal ativa; a fixture também permitia contenção por vínculo ao alvo. | Constitui decisão persistente explícita, sem vínculo protetor; _evaluate usa o mesmo action_audit letal da execução. Mantém desejo persistente, bloqueio físico, RNG e desfecho real. | PASS |
| test_phase51.Phase51Tests.test_03_many_weak_factors_do_not_become_grave_world_pressure | FAIL | INVALID_EXPECTATION: Relatos abaixo da confiança mínima já não produzem intenção letal válida. | Exige bloqueio letal e ausência de intenção kill; não obriga o retorno do desejo irracional que foi substituído pelo modelo atual. | PASS |
| test_phase51.Phase51Tests.test_04_received_group_failures_raise_pressure_without_duplicate | FAIL | CONFIRMED_BUG: B02 bloqueava responsabilidade e assume_local_office. | Mantém todas as expectativas originais: três falhas conhecidas, sem duplicação, cargo disponível e restrição para guarda. | PASS |
| test_phase51.Phase51Tests.test_07_capable_faction_acts_with_cost_and_ideology_filter | FAIL | INVALID_EXPECTATION: Abastecimento existente tem precedência sobre serviço no provedor institucional; a ordem não desapareceu. | Transfere estoque real antes de testar a etapa de ordem; conserva custo, ideologia, patrulha/roubo e pagamento. Não altera prioridade dos provedores. | PASS |
| test_phase51.Phase51Tests.test_10_village_representation_travels_and_response_returns | FAIL | OUTDATED_FIXTURE: Faltavam rota/provisões e a antiga velocidade de um passo não representa a estrada atual. Também havia bloqueio real de retransmissão após conhecimento do líder. | Ensina rota/provisões e confere velocidade do próprio trajeto; corrige respostas ainda não retransmitidas sem duplicar responsabilização e mantém encontro físico. | PASS |
| test_phase51.Phase51Tests.test_11_pressure_save_queries_and_deterministic_continuation | FAIL | CONFIRMED_BUG: B01: contexto de fundação compartilhava lista de membros. | Snapshots profundos e consulta pura; igualdade integral permanece exigida. | PASS |

Tabela estruturada: [testes_antigos.json](</home/hugo/Área de trabalho/procedrual/reports/fase_5_5_5/testes_antigos.json>).

### Outros testes afetados pela limpeza

- A antiga fixture `Society.material` obrigava materialização política instantânea. O teste agora percorre a política financiada, trabalhador que a conhece e consumo de grão para produzir alimento. A função duplicada foi removida.
- Duas fixtures de formalização anteriormente verdes dependiam do atalho B04. Foram atualizadas para presença e score realmente válidos, sem reduzir os requisitos do motor.
- O teste de cadeia alimentar inviável inspeciona diagnósticos do planejamento e passou a chamar explicitamente `plan_solutions` (COMMAND), em vez de esperar que a consulta pública modificasse o motor.
- O debug deixou de repetir o planejamento: usa as alternativas já avaliadas na decisão real. A primeira instrumentação fazia suas contagens divergirem; a regressão foi corrigida.
- Entradas inválidas do jogador sem evento/tempo transcorrido não deixam traces nem consomem IDs privados. Os testes que exigem save inalterado continuam passando.
- A classificação dos recebimentos usa o tipo do Fact aceito, sem depender de um evento ainda estar no cache transitório. Isso corrigiu divergência observacional após load em fixtures que limpam o histórico.

Rodada intermediária preservada em [rodada_intermediaria.log](</home/hugo/Área de trabalho/procedrual/reports/fase_5_5_5/rodada_intermediaria.log>); ela documenta erros de desenvolvimento, não testes ativos pendentes.

## 5. Testes novos e suíte final

| Teste novo |
| --- |
| test_b01_nested_snapshots_and_fact_independence |
| test_b01_group_join_same_after_load |
| test_b02_received_rejection_records_responsibility_once |
| test_b02_better_confidence_does_not_duplicate_failure |
| test_b03_preparation_respects_cooldown_and_known_empty_source |
| test_b04_all_entrypoints_share_formalization_requirements |
| test_b05_supply_commits_to_available_resource |
| test_b06_reused_need_has_single_typed_identity |
| test_b07_exploration_and_unknown_death_have_truthful_text |
| test_b08_religious_report_producer_utility_goal_execution |
| test_query_is_pure_and_need_episode_changes_on_reactivation |
| test_native_causal_receipts_and_indices_survive_load |
| test_ordinary_observability_has_bounded_retention |
| test_death_keeps_private_appraisal_separate_from_original_event |
| test_old_save_is_rejected_explicitly |

Comando:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
```

**Resultado final: 341 testes, 0 falhas, 0 erros, 0 desativações; 186.943 segundos.** Log completo: [testes_final.log](</home/hugo/Área de trabalho/procedrual/reports/fase_5_5_5/testes_final.log>).

Uma suíte verde valida contratos e cenários cobertos; não demonstra que uma formalização, apoteose ou audiência necessariamente ocorrerá naturalmente.

## 6. Observabilidade Histórica Nativa V1

| Estrutura | O que representa | Campos/contrato |
| --- | --- | --- |
| Event | Acontecimento do mundo | ID de entidade/evento existente, turno, ator/alvo/local, testemunhas, historical, snapshot do contexto, schema_version, parent_event_ids, decision_id/action_attempt_id disponíveis. |
| Need episode | Uma ativação específica da necessidade | Need.id permanece; episode incrementa ao reativar depois do encerramento; identificador n<ID>:<geração>, sem consumir IDs do jogo. |
| DecisionTrace | Registro privado da decisão | Ator, turno, LOD, episódio/kind/prioridade, fatos fonte, alternativas geradas/bloqueadas, scores, escolha/score/alvo/recurso, Goal, tentativa, resultado e emissões. |
| ActionAttempt | Tentativa concreta | ID privado, ator, turno, Goal, ação/alvo, success/outcome e IDs emitidos. Caminhada ainda sem execução pode ter Goal e não ter tentativa. |
| LearningReceipt | Aprendizagem, não evento público | Receptor, evento/Fact, turno aprendido, canal, fonte e confiança anterior/posterior; melhorias de confiança são registradas. |
| HistoricalObservability | Estado persistente de observação | Nível, sequência privada, traces/tentativas, anéis recentes, última decisão por ator, recebimentos e arquivo de eventos promovidos. |
| EventIndex | Índices reconstruíveis | Actor, target, location, kind e turn; dados históricos e arquivados, mais cache operacional recente. |

Implementação: [HistoricalObserver](</home/hugo/Área de trabalho/procedrual/procedural/observability.py:90>), [EventIndex](</home/hugo/Área de trabalho/procedrual/procedural/observability.py:45>) e modelos em [DecisionTrace](</home/hugo/Área de trabalho/procedrual/procedural/models.py:779>).

Não há frontend, narrador LLM ou banco externo. Decisões de NPC e planejamento econômico coletivo são observados no próprio fluxo executável. A observação não cria Facts sobre Need/Utility e não publica pensamentos para outros NPCs.

### Causalidade e relações temporais

`parent_event_ids` guarda causas identificadas por contratos explícitos: source_fact/source_event, fatos de avaliações letais, origem da proposta, entrega, criação de política, trabalho/conclusão, decisão terminal e avaliação pós-morte. Não se infere uma causa só porque dois eventos ocorreram perto.

Na morte, a última decisão da vítima pode ser promovida e ligada por **related_decision_ids**; isso é contexto temporal, separado dos pais causais. Uma fome fatal no fechamento da hora não passa a ser falsamente “causada” pelo último ato do NPC.

`World.events` continua limitado a 256. `World.history` permanece separado; eventos relevantes não históricos e causas disponíveis podem ser promovidos para `event_archive` sem mudar seu historical flag.

### Gates e retenção

Códigos estáveis incluem NO_KNOWN_ROUTE, NO_KNOWN_TARGET, ACTION_COOLDOWN, NO_STOCK, NO_CAPABILITY, NO_INPUT, NO_WORKER, INSUFFICIENT_MONEY, SURVIVAL_NOT_VIABLE, EXCESS_RESERVE e NO_GENERATED_ACTION. Detalhes humanos não são a identidade do gate.

Nem toda ausência de candidato já tem explicação específica: nesses pontos V1 usa **NO_GENERATED_ACTION**, sem fingir saber qual gate interno decidiu. Os fornecedores de rota, avaliação/eligibility e barreiras de trabalho possuem registros mais específicos.

- **OFF:** sem retenção de traces/recebimentos; mantém metadados/IDs causais necessários para não alterar os Events entre modos.
- **NORMAL:** até 12 entradas por lista de alternativas/scores/bloqueios; anel global de 256 decisões ordinárias e 1 última decisão por ator; 1.024 recebimentos ordinários recentes.
- **AUDIT:** até 128 entradas por lista, termos de Utility e anéis de 1.024 decisões / 4.096 recebimentos.
- Traces importantes e recebimentos de fatos estruturais são preservados. Não há snapshot completo de Character por decisão.
- Cortes são explícitos em `truncated`; a escolha final e seu score/alvo/recurso permanecem fora do corte.

A história estrutural cresce com acontecimentos relevantes. O que fica limitado é a retenção dos cálculos/decisões ordinários, não a duração do mundo.

## 7. Consultas e comandos

| API | Classificação | Contrato |
| --- | --- | --- |
| GoalSystem.solutions | QUERY | Avalia em cópia isolada do mundo/RNG. Não altera original, cooldown, planos, Facts ou eventos. É mais cara que consultar um índice. |
| GoalSystem.plan_solutions / decide / execute / collective | COMMAND | Planejamento/execução podem manter estado e produzir consequências. Debug usa os resultados já calculados. |
| Institutions.can_formalize / Geography.plan | QUERY | Leitura de requisitos e conexões. |
| Institutions.pressure / decision_scores; Society.decision_scores | COMMAND | Atualizam pressão/diagnóstico da proposta; o nome legado de pontuação não implica pureza. |
| HistoricalObserver.event_details | QUERY | Retorna evento, IDs/causas disponíveis, trace/tentativa, referências de Facts e recebimentos; objetos amigáveis actor/target cobrem Characters. Outros tipos são resolvidos nas coleções do World pelos IDs. |
| EventIndex | QUERY_WITH_CACHE | Índices reconstruídos no load e alimentados por emissões; cache não é estado de gameplay. |

Exemplo de navegação, sem tomar decisões nem avançar o mundo:

```python
details = engine.observability.event_details(event_id)
by_actor = engine.observability.index.query('actor', actor_id)
by_kind = engine.observability.index.query('kind', 'CharacterKilled')
# details['parent_event_ids'], ['decision'], ['attempt'], ['learning_receipts']
```

## 8. Save e reprodutibilidade

Saves de formato 1 / regras anteriores são **recusados com mensagem de incompatibilidade**. Não existe migração implícita. O formato 2 preserva novos modelos, snapshots, geração/configuração e sequência de IDs privados. Índices são reconstruídos; não há duplicação persistente de cinco índices.

`generation_version` e `generation_config` ficam no World/save, incluindo configuração de geração, presença/nome do jogador. Seed sozinha não é tratada como garantia de reprodução entre versões de regras.

O save final temporário teve **254.12 MB** e foi carregado com igualdade de todos os campos. SHA-256: `4c9cbdb0d0c59127d84bc1411467ff4fd6c62182cca271e77c288225a9ef8ed0`. Foi removido depois da verificação, preservando métricas, hashes e evidência compacta.

**Limite importante:** o JSON completo ainda é grande. A coleção nativa representa 49.46 MB, cerca de 19.5% do JSON final; o restante inclui o estado do mundo, conhecimento e história já existentes. Não se está chamando 254 MB de save pequeno. Compressão/deduplicação futura deve preservar os registros relevantes, sem apagar causalidade para baixar o número.

O arquivo [historico_nativo.json.gz](</home/hugo/Área de trabalho/procedrual/reports/fase_5_5_5/historico_nativo.json.gz>) tem **6.31 MB**, com história/observação e identificação mínima de personagens. **É evidência histórica, não um save completo carregável no jogo.** Não contém snapshots completos de Character.

## 9. Neutralidade OFF / NORMAL / AUDIT

Seed fixa: `Controle-Neutralidade555`; **24 horas por modo**. Foram comparados todos os campos do World exceto a coleção privada `observability`, **incluindo metadados de Events**, geração/configuração, estado material, economia, relações, NPCs, métricas, IDs de gameplay e RNG.

Resultado: **igualdade exata nos três níveis**. Hash do estado comparado: `c1d03fe67966f0de3c604e8320882eb9b540483e46318c056eed996164f1b19f`. OFF reteve 0 traces; NORMAL reteve 278.

Não é uma prova matemática de toda campanha futura; é o controle solicitado, complementado pela separação de RNG/IDs e pelos testes de debug/consulta.

## 10. Continuidade e smoke

Seed `Controle-Continuidade555`:

```text
Run A: 100h contínuas
Run B: 50h → serializar → carregar → 50h
```

**Todos os campos persistentes foram iguais**, incluindo RNG, história causal, recebimentos, traces e IDs produzidos depois do load. Próximos IDs: gameplay `4715`, privado `3875`. Hash: `3040c884ceea0ef4806829e32a04bae7f936609628d5781b82b2ccd3aa2b3e1c`.

Smoke posterior: `Controle-Smoke555`, **12h, quatro reinos, 1844 NPCs**, invariantes e auditoria geográfica válidas. Evidência: [controles.json](</home/hugo/Área de trabalho/procedrual/reports/fase_5_5_5/controles.json>).

## 11. Campanha natural final — regressão

Seed única nova: **`Elyndar-Estabilidade555`**. Quatro reinos, sem jogador, `historical_turns=0`, **300 horas**, sem busca de seeds ou aquecimento histórico. Os acontecimentos de geração/fundação em h0 não são horas simuladas anteriores.

| Medida | Resultado |
| --- | --- |
| NPCs nomeados inicial/final | 1862 / 1862 |
| População abstrata inicial/final | 4595 / 4595 |
| Vivos / mortos | 1588 / 274 |
| Mortes por fome / sede / ambas / combate | 132 / 125 / 13 / 4 |
| Grupos criados / adesões | 147 / 1038 |
| Propostas criadas / entregues | 52 / 10 |
| Políticas criadas / concluídas | 4 / 4 |
| Ataques / decisões letais / mortes em combate | 388 / 30 / 4 |
| Viagens iniciadas / chegadas | 86 / 76 |
| Adesões a facção / formalizações | 1 / 0 |
| Intervenções / audiências / apoteoses | 1 / 0 / 0 |
| ReligiousDeclineReported natural | 0 |
| Eventos históricos / pais causais em links | 70667 / 30007 |
| Checkpoints válidos | 12, a cada 25h |
| Exceções estruturais / reescrita do histórico | 0 / 0 |
| Tempo com observação nativa e verificações | 561.6s; inclui validação e exportação, não benchmark puro |

O saldo total passou de **137384 para 137672**. A diferença **288** é exatamente a fonte monetária já prevista `MoneySourceAbstractWork`. O residual foi **zero em todos os checkpoints**. A economia não é monetariamente fechada: trabalho abstrato emite moeda por regra existente. Transferências continuam debitando saldos; produção/consumo de água, alimento e materiais obedecem suas fontes/regras e aos testes materiais da suíte, não a uma hipótese de quantidade global fixa de comida.

Grupos/propostas/políticas, viagens, combate e religião continuaram operando. As quatro mortes em combate ocorreram naturalmente. Zero audiência, apoteose ou formalização não foi “corrigido” com novos thresholds. B08 possui prova controlada ponta a ponta; a quantidade natural de relatos acima não é usada para declarar que esse caminho foi exercitado quando não foi.

### Crescimento da observação

| Hora | Traces importantes | Traces ordinários | Recebimentos permanentes | Anel de recebimentos |
| --- | --- | --- | --- | --- |
| 25 | 453 | 1787 | 13960 | 1024 |
| 50 | 1137 | 1838 | 38514 | 1024 |
| 75 | 1423 | 1865 | 45634 | 1024 |
| 100 | 1721 | 1878 | 52904 | 1024 |
| 125 | 2085 | 1880 | 61521 | 1024 |
| 150 | 2527 | 1851 | 71511 | 1024 |
| 175 | 3009 | 1805 | 81486 | 1024 |
| 200 | 3505 | 1749 | 90842 | 1024 |
| 225 | 4065 | 1695 | 99977 | 1024 |
| 250 | 4625 | 1671 | 109033 | 1024 |
| 275 | 5273 | 1647 | 118779 | 1024 |
| 300 | 5816 | 1610 | 126858 | 1024 |

Foram contabilizadas **263247 decisões** (NPCs e rotina coletiva). Retidas: **7426 (2.82%)**, sendo 5816 importantes. Não se gravaram todos os cálculos dos NPCs para sempre. Dos 1660335 recebimentos aceitos, 126858 foram preservados como estruturais e 1024 ficaram no anel ordinário.

**Lacunas medidas:** 1442 IDs parentais únicos já não tinham payload no índice de runtime ao final. No conjunto persistente exportado, são 1453. São lacunas de payload nas referências; eventos efêmeros podem envelhecer fora da retenção. Não foi atribuída uma causa individual a cada lacuna nem convertido um Fact em evento verdadeiro inventado para preenchê-la. A V1 é uma fundação causal parcial, não um gravador integral de tudo. Um histórico importante com fontes disponíveis pode ser navegado; a ausência do payload é uma lacuna explícita.

O cache transitório de até 4.096 eventos pode ter mais eventos cotidianos que o buffer de 256 salvo. A reconstrução garante os índices da história/arquivo persistentes; não promete perpetuar todos os acertos desse cache.

Evidência completa: [campanha.json](</home/hugo/Área de trabalho/procedrual/reports/fase_5_5_5/campanha.json>) e [campanha.log](</home/hugo/Área de trabalho/procedrual/reports/fase_5_5_5/campanha.log>).

## 12. Cadeia real completa da campanha

| Elo | Registro real |
| --- | --- |
| Source Event | #27515, WantedIssued, h6; ator Elena Corven #718, alvo #706 |
| Fact aprendido | Nora Vale #4141 recebeu o fato #27515 em h6, canal direct, confiança 0→100 |
| Need episode | n27516:1, response, prioridade 59.35 |
| Decision | d34171, ator Nora Vale #4141, h35; selecionou route_travel, score 74.4 |
| Goal | #71009 |
| ActionAttempt | a34172, route_travel, sucesso True |
| Result Event | #71010, MigrationArrived, h35; pais [27515]; decision_id=d34171, action_attempt_id=a34172 |
| LearningReceipt do resultado | NPC #686 aprendeu #71010 em h35, canal direct, confiança 0→100 |

Ação e evento podem ter alvos semânticos diferentes: a necessidade responde a uma pessoa, enquanto a chegada descreve uma localidade. O relatório reproduz os IDs efetivos e não converte isso automaticamente em uma narrativa de perseguição bem-sucedida.

Dados completos desse caso, sem reexecutar a decisão: [cadeia_real.json](</home/hugo/Área de trabalho/procedrual/reports/fase_5_5_5/cadeia_real.json>).

## 13. Problemas e limites que permanecem

- **Sobrevivência domina as mortes:** 270/274 mortes por privação. Corrigir o atalho de água não resolveu capacidade econômica, deslocamento, competição de prioridades ou sustentabilidade global. Não se usou esta seed para rebalancear nada.
- Há propostas sem entrega e organizações sem formalização. Os caminhos não são garantidos por estar implementados; frequência e gargalos continuam para análise de coerência.
- O save JSON continua volumoso. Retenção ordinária é limitada, mas conhecimento, história e registros importantes crescem. Há espaço para compressão/deduplicação sem apagar a evidência estrutural.
- V1 não grava todos os gates internos de cada fornecedor, todos os desempates de RNG, todos os fatos cotidianos antigos nem a história completa de cada mudança de belief. Ausência é indicada, não preenchida por inferência.
- Identificadores de alvos ainda seguem os contratos dos sistemas existentes; tipos semânticos explícitos para todos eles e resolução genérica de entidades seriam melhorias da API de leitura futura.
- A confirmação natural não substitui testes controlados de eventos raros; estes resultados não autorizam alterar limiares para forçá-los.

## 14. Entrega à Fase 6.0 e evidências

B01–B08 estão corrigidos, a suíte ativa está verde, o legado relevante foi classificado, as regras duplicadas identificadas foram removidas/redirecionadas e a observação nativa passou pelos controles. O histórico não compartilha os payloads mutáveis que causavam B01.

Ficam explicitamente para a 6.0: coerência e balanceamento de sobrevivência, capacidade das capitais, oportunidades afetadas por LOD, fluxo crime→justiça, fragmentação de grupos, compatibilidade organizacional, delegação institucional, carreira, frequência de violência e religião. Nenhuma dessas perguntas foi resolvida mudando taxas nesta fase.

Arquivos principais:

- [Suíte completa final](</home/hugo/Área de trabalho/procedrual/reports/fase_5_5_5/testes_final.log>)
- [21 falhas antigas classificadas](</home/hugo/Área de trabalho/procedrual/reports/fase_5_5_5/testes_antigos.json>)
- [Código legado](</home/hugo/Área de trabalho/procedrual/reports/fase_5_5_5/legado.json>)
- [Neutralidade, continuidade e smoke](</home/hugo/Área de trabalho/procedrual/reports/fase_5_5_5/controles.json>)
- [Métricas da campanha](</home/hugo/Área de trabalho/procedrual/reports/fase_5_5_5/campanha.json>)
- [Exemplo causal natural](</home/hugo/Área de trabalho/procedrual/reports/fase_5_5_5/cadeia_real.json>)
- [História nativa compactada, sem save completo](</home/hugo/Área de trabalho/procedrual/reports/fase_5_5_5/historico_nativo.json.gz>)

Reprodução da campanha, com o mesmo código/versão:

```python
from procedural.generation import generate_world, GenerationConfig
from procedural.engine import Engine
world = generate_world('Elyndar-Estabilidade555', with_player=False,
                       config=GenerationConfig(kingdom_count=4, historical_turns=0))
engine = Engine(world)
engine.simulate(300)
```

A variante com verificações e exportação é `python3 -m experiments.phase555_validation campaign`; ela recusa sobrescrever uma campanha registrada ou trocar seed silenciosamente.
