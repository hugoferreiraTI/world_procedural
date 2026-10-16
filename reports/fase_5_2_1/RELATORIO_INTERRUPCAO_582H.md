# Relatório — Fase 5.2.1 interrompida na hora 582
> Registro da primeira execução. Depois deste encerramento, o usuário autorizou um novo teste de 1.000h com a mesma seed. A memória reentrante e a lista mutável de auditoria foram corrigidas antes do reinício. O relatório principal atualizado fica em `RELATORIO_5_2_1.md`, na raiz do projeto.

**A campanha de 1.000 horas parou na hora 582 por `KeyError` na transmissão de informações entre guardas. O usuário escolheu encerrar com este relatório, sem reinício.** A última medição completa preservada é da hora **550**; não são resultados finais da hora 582.

Até 550h houve **115 decisões letais, 527 ataques letais, 31 oportunidades terminais, 16 escolhas de poupar, uma finalização deliberada, uma retirada e uma captura**. Duas mortes intencionais foram contabilizadas: uma em combate e uma por finalização. Isso demonstra que `finish` conseguiu ocorrer naturalmente, com dano e barreira letal preservados. A validação ampla de 1.000h ficou incompleta.

## Campanha e mudanças

Seed **Vaelmir-521**, versão `mvp-10.1-fase5.2.1`, mundo novo, sem jogador, sem histórico inicial e sem save anterior. Abertura: **1.760 NPCs persistentes, 4.424 habitantes abstratos, seis reinos, 30 cidades e 45 vilas**. Houve uma única execução natural, sem troca de seed ou parâmetros. A duração solicitada substituiu as 300h do documento por 1.000h; o encerramento posterior foi decidido pelo usuário após a falha.

Antes da campanha: retirada do sorteio residual entre alternativas terminais próximas; registro terminal de captura/ajuda/retirada; retratos contextuais com cinco escores, valores pessoais e causa; telemetria compacta de candidatos avaliados/rejeitados; classificação de Actors por significado do ato. Dano, armas, HP, frequência de ataque, requisitos letais e custos/chances/limiares divinos não foram alterados. A linha extrema de finalização inevitável permanece somente uma hipótese.

## Evolução preservada

| Hora | Vivos | Decisões criadas | Ataques letais | Oportunidades | Mortes intencionais |
| --- | --- | --- | --- | --- | --- |
| 0 | 1760 | 0 | 0 | 0 | 0 |
| 100 | 1760 | 0 | 0 | 0 | 0 |
| 150 | 1758 | 4 | 16 | 0 | 0 |
| 200 | 1758 | 5 | 31 | 1 | 0 |
| 300 | 1752 | 23 | 95 | 3 | 0 |
| 350 | 1742 | 37 | 160 | 7 | 1 |
| 450 | 1720 | 64 | 289 | 14 | 2 |
| 500 | 1700 | 88 | 407 | 18 | 2 |
| 550 | 1662 | 115 | 527 | 31 | 2 |

A primeira decisão de poupar aparece na medição de 200h; a primeira morte intencional aparece na de 350h; a finalização deliberada, na de 450h. São janelas de observação, não as horas exatas dos eventos. Na hora 550 havia 98 mortos em relação à população persistente inicial, dos quais dois eram mortes intencionais contabilizadas. **As causas das demais mortes não foram exportadas:** não é possível atribuí-las à fome, combate acidental ou outra causa.

## Funil letal — disponível até 550h

| Etapa | Quantidade / disponibilidade |
| --- | --- |
| LethalCandidateEvaluated / Rejected | não exportados |
| LethalConsideration | não exportado |
| LethalDecision | 115 |
| Decisões que chegaram a ataque | não exportadas |
| LethalAttack | 527 |
| ExecutionOpportunity | 31 |
| TerminalFinishChosen | 1 |
| TerminalSpareChosen | 16 |
| TerminalCaptureChosen | 1 |
| TerminalHelpChosen | 0 |
| TerminalWithdrawChosen | 1 |
| IntentionalCombatKill | 1 |
| DeliberateFinish | 1 |
| PostKillAppraisal / DeathAffinityIncrease | contagens não exportadas |
| LethalDecisionResolved / Abandoned | contagens não exportadas |

As 31 oportunidades e 19 escolhas não representam a mesma unidade: uma oportunidade pode não chegar imediatamente à escolha. Os retratos individuais não foram escritos antes da falha; portanto, os 12 casos restantes não podem ser classificados causalmente neste relatório. Captura e retirada são escolhas registradas; o sucesso dessas duas execuções também não ficou exportado.

O código prevê avaliação pós-morte para homicídios e os testes verificaram sua execução, mas a contagem e os sentimentos naturais não ficaram gravados. Não atribuí culpa, prazer ou aumento de DeathAffinity aos dois matadores sem esses registros. Não houve alerta de divergência entre vencedor contextual e escolha terminal no arquivo de falha preservado; isso não substitui a inspeção dos escores individuais.

## Decisões abertas

| Idade da decisão ativa na hora 550 | Quantidade |
| --- | --- |
| <24h | 11 |
| 24–72h | 25 |
| 72–168h | 24 |
| >168h | 23 |

Havia **83 decisões ativas**. Os motivos de encerramento, mortes conhecidas/desconhecidas dos alvos e ruminação individual não ficaram exportados. Assim, as 23 decisões com mais de 168h não demonstram, por si, memória eterna nem persistência plausível. Os testes demonstram que morte confiável encerra a decisão, rumor fraco não encerra e vida segura com redução de ruminação pode encerrá-la sem prazo arbitrário; a distribuição natural desses motivos permanece sem medição.

## Falha confirmada e correção posterior

**P1 — memória expulsa durante processamento de um fato.** Na hora 582, `justice.communicate()` enviou um fato a um guarda. `KnowledgeSystem.learn()` chamou os ouvintes consultando repetidamente `character.knowledge[fact.event_id]`. Uma reação reentrante pode aprender outros fatos, atingir o limite de 64 memórias e expulsar o fato que os ouvintes seguintes ainda precisam processar. O próximo acesso lançou **`KeyError: 582633`** e encerrou a execução. A cadeia do traceback está no log.

A correção posterior guarda uma referência local ao fato aceito e entrega essa referência aos ouvintes. Também foi retirado um acesso equivalente à memória no processamento de conflitos entre grupos. O limite de memória continua 64; ninguém ganha informação nova ou confiança maior. **A correção não participou desta campanha**, nem foi validada por outra campanha natural. Foi reproduzido o mesmo `KeyError` em teste usando a implementação anterior, e o caso passou com a correção.

**P2 — 37 alertas de referência a fatos futuros em auditorias históricas.** O primeiro conjunto já existia na hora 250. O arquivo de falha conserva 37 IDs únicos, todos com motivo `future_fact_in_history`; exemplos: **229447, 230588, 253318, 323893, 432448 e 546196**. Não há alertas de outra categoria nesse arquivo. Isso compromete a leitura causal do histórico e não deve ser confundido com 37 homicídios ou 37 personagens afetados.

Foi confirmado em uma sondagem controlada que uma auditoria genérica de ataque pode compartilhar `source_facts` com uma decisão relativa a outro alvo, via `ActionPressure.known_harm()`: reforçar essa decisão muda a lista já devolvida ao auditor. Esse é um caminho real de mutabilidade residual e **uma explicação possível** para os alertas. Sem os contextos completos dos 37 eventos, não foi estabelecido que todos vieram desse caminho. Essa mutabilidade não foi corrigida nesta entrega; exige isolamento dos dados históricos e verificação específica numa próxima correção.

**P2 — perda de evidência detalhada na interrupção.** O auditor escrevia retratos, narrativas, métricas completas e save somente ao final. A exceção escreveu apenas hora, erro e alertas; o mundo em memória foi perdido quando o processo terminou. Não há save final, nomes dos matadores, cinco escores naturais, avaliações pós-morte, composição religiosa final ou histórias individuais recuperáveis. Os IDs preservados não permitem reconstruir esses dados. Não executei o mundo novamente para recriá-los. Um próximo auditor deve preservar um resumo suficiente ao falhar, antes de propagar a exceção.

As **12 verificações estruturais**, da hora zero à 550 em intervalos de 50h, passaram. Isso não significa ausência de bugs: a falha fatal ocorreu fora desses verificadores.

## Religião: capacidade testada, resultado natural indisponível

| Deus / domínio | Seguidores iniciais | Devotos iniciais | Actors iniciais | Actors / overlap finais |
| --- | --- | --- | --- | --- |
| Aurion / justice | 552 | 180 | 0 | não exportados |
| Neruma / protection | 600 | 242 | 0 | não exportados |
| Elar / knowledge | 608 | 213 | 0 | não exportados |

Não havia cultistas recentes na abertura. Os testes passaram: ajuda emergencial gera Actor de proteção, ajuda genérica não gera Actors de todos os domínios e informação confiável sobre crime a um guarda pode alinhar justiça e conhecimento ao mesmo tempo. **A divergência de comunidades naturais e a sobreposição final não puderam ser medidas.** A classificação de Actor foi separada do favor divino: um ato alinhado não informa automaticamente o deus.

Os canais existentes permitem relatar duas ou mais perdas conhecidas numa congregação observada e conversões conhecidas para uma fé rival. Perdas agregadas de Actors ainda não têm canal próprio. O deus pode continuar desconhecendo uma deterioração objetiva; não foi adicionada telepatia nem aumentada a intervenção divina. A frequência natural desses relatos também não ficou exportada.

## Testes e conclusão

Os **seis testes focados e quatro testes de regressão passaram antes da campanha**. Depois da falha, o teste de morte conhecida foi ampliado para forçar expulsão reentrante da memória; os mesmos seis testes e quatro regressões passaram novamente. O teste com código anterior falhou exatamente com `KeyError`, confirmando a regressão corrigida. Não foi repetida a suíte completa.

Houve finalização e poupança naturais, sem recalibrar violência. Isso é evidência positiva do desfecho terminal. Entretanto, a interrupção, os 37 alertas e a ausência dos retratos pós-morte impedem declarar concluída a validação ampla ou fechar a análise individual da letalidade. Não há base nesta campanha interrompida para implementar a linha extrema de morte garantida.

Evidências: [Crônica parcial](</home/hugo/Área de trabalho/procedrual/reports/fase_5_2_1/HISTORIAS_REAIS.md>) · [Métricas preservadas](</home/hugo/Área de trabalho/procedrual/reports/fase_5_2_1/RESULTADO_PARCIAL_550H.json>) · [Falha](</home/hugo/Área de trabalho/procedrual/reports/fase_5_2_1/campanha_1000h/falha_resumida.json>) · [Log da campanha](</home/hugo/Área de trabalho/procedrual/reports/fase_5_2_1/execucao_1000h.log>) · [Reprodução do erro](</home/hugo/Área de trabalho/procedrual/reports/fase_5_2_1/reproducao_falha_memoria.log>) · [Testes após correção](</home/hugo/Área de trabalho/procedrual/reports/fase_5_2_1/testes_6_pos_falha.log>) · [Regressões após correção](</home/hugo/Área de trabalho/procedrual/reports/fase_5_2_1/smoke_4_pos_falha.log>).

Núcleo executado: `ea63f9f21b03908fe124f44695c53b8f0f3b37fed8138b66880e21e2d396cd3d`. O hash do núcleo corrigido entregue fica em `reports/fase_5_2_1/ENTREGA_FINAL.json`; as diferenças estão em `alteracoes_codigo.patch`. O arquivo `fase_5_2_1.md` preserva o documento recebido.
