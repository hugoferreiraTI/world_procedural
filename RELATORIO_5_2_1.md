# Relatório — Fase 5.2.1: Thalendor-521

**Campanha concluída: 1.000 horas e 4 finalizações deliberadas naturais, todas com avaliação pós-morte.** O caminho decisão letal → ataque → oportunidade → escolha de finalizar → morte → PostKill funcionou. Não é necessário recalibrar a letalidade para satisfazer o critério desta fase.

Seed **Thalendor-521**, versão `mvp-10.1-fase5.2.1`. Mundo novo, sem jogador, sem histórico inicial e sem save carregado. A duração de 1.000h substitui as 300h do documento por pedido do usuário. As tentativas com Vaelmir-521 interrompidas em 582h e 650h permanecem arquivadas; o usuário autorizou começar novamente com uma seed nova. O núcleo ficou congelado durante toda esta execução.

| Hora | NPCs vivos | Decisões criadas | Ataques letais | Oportunidades | Mortes intencionais |
| --- | --- | --- | --- | --- | --- |
| 0 | 1776 | 0 | 0 | 0 | 0 |
| 250 | 1773 | 10 | 42 | 1 | 0 |
| 500 | 1707 | 84 | 362 | 20 | 1 |
| 750 | 1570 | 160 | 809 | 53 | 2 |
| 1000 | 1480 | 206 | 1115 | 78 | 4 |

## Correções e testes prévios

A escolha terminal vencedora passou a executar sem o sorteio residual entre alternativas próximas. Captura, ajuda e retirada registram escolha e sucesso; a telemetria separa candidatos, considerações e decisões. Actors religiosos foram diferenciados pelo significado do ato em cada domínio. Dano, HP, armas, frequência de ataque, barreira letal e parâmetros de intervenção divina foram preservados.

As falhas anteriores eram de memória reentrante: um fato podia ser expulso enquanto ainda era processado, ou antes de uma decisão letal fixar sua causa. Referências locais e proteção temporária dos fatos em processamento/criação corrigem esses casos, mantendo o limite de 64 memórias. Listas históricas de auditoria também foram isoladas de alterações posteriores.

**Seis testes focados e quatro regressões passaram**: finalizar/poupar, morte conhecida versus desconhecida, encerramento por ruminação, Actors específicos e sobreposição coerente; anonimato, persistência, recuperação e continuidade determinística. As duas falhas anteriores foram reproduzidas antes das correções. Não foi repetida a suíte completa. Logs: `testes_6_memoria_integridade.log` e `smoke_4_memoria_integridade.log`.

## Funil letal e consequências

| Etapa | Ocorrências |
| --- | --- |
| LethalCandidateEvaluated | 2165 |
| LethalCandidateRejected | 1941 |
| LethalConsideration | 207 |
| LethalDecision | 206 |
| Decisões que chegaram a ataque | 157 |
| LethalAttack | 1115 |
| ExecutionOpportunity | 78 |
| TerminalFinishChosen | 4 |
| TerminalSpareChosen | 34 |
| TerminalCaptureChosen | 6 |
| TerminalHelpChosen | 0 |
| TerminalWithdrawChosen | 1 |
| IntentionalCombatKill | 0 |
| DeliberateFinish | 4 |
| PostKillAppraisal | 10 |
| DeathAffinityIncrease | 0 |
| LethalDecisionResolved | 11 |
| LethalDecisionAbandoned | 94 |

Candidatos são transições relevantes, decisões são episódios e ataques são ações. Não são contagens de pessoas distintas nem etapas com correspondência obrigatória de um para um.

Sucessos terminais: `{'spare': 34, 'finish': 4, 'capture': 5, 'withdraw': 1}`. Houve seis escolhas de captura e cinco execuções bem-sucedidas. Os **10 PostKill** incluem as quatro finalizações e seis mortes não intencionais em combate; não são dez homicídios deliberados. Nenhuma DeathAffinity aumentou.

| Autor → vítima | Hora | Culpa | Alívio | Orgulho | Prazer / fascinação |
| --- | --- | --- | --- | --- | --- |
| Ruan Montes → Ruan Stone | 421 | 25,38 | 55,00 | 15,64 | 0 / 0 |
| Darin Kars → Bela Alvor | 701 | 51,46 | 55,00 | 0,00 | 0 / 0 |
| Marie Montes → Elena Kars | 799 | 29,72 | 55,00 | 11,70 | 0 / 0 |
| Marie Corven → Iria Vale | 968 | 51,26 | 55,00 | 0,00 | 0 / 0 |

Vergonha, medo, insensibilidade, luto e conflito moral estão nas avaliações completas. Nenhuma das quatro finalizações criou afinidade com a morte ou automaticamente um assassino recorrente.

## Decisões antigas e conhecimento

| Idade da decisão ativa | Quantidade |
| --- | --- |
| <24h | 5 |
| 24–72h | 9 |
| 72–168h | 14 |
| >168h | 73 |

Encerramentos: `{'terminal_spared': 35, 'new_overwhelming_perceived_danger': 16, 'owner_died': 36, 'known_target_death': 11, 'terminal_capture': 4, 'safe_life_and_diminished_rumination': 3}`. O estado final retém `{'active': 101, 'abandoned': 82, 'resolved': 10}`; decisões encerradas podem sair da memória limitada, mas seus eventos permanecem no histórico. **10 decisões** tinham alvo morto e ausência de notícia confiável da morte. Isso respeita o conhecimento individual.

Silas Corven soube diretamente da morte de Tomas Kars na hora 591 e resolveu a decisão. John Bruma não soube da morte de Cael Luar na hora 509 e ainda tinha decisão aberta na hora 1.000. Houve três encerramentos por vida segura e ruminação reduzida. Entretanto, **73 das 101 decisões ativas têm mais de 168h**: a duração continua merecendo acompanhamento; não foi acrescentado timeout.

## Religião

| Deus | Seguidores início → fim | Devotos finais | Cultistas finais | Actors finais | Actors exclusivos |
| --- | --- | --- | --- | --- | --- |
| Aurion | 0 → 0 | 0 | 0 | 204 | 177 |
| Neruma | 1240 → 1044 | 406 | 12 | 44 | 30 |
| Elar | 536 → 436 | 161 | 7 | 36 | 20 |

| Domínios compartilhados | Actors |
| --- | --- |
| Aurion + Neruma | 14 |
| Aurion + Elar | 16 |
| Neruma + Elar | 3 |

A união contém **254 pessoas distintas**. Actor representa feitos alinhados nos últimos 200h, inclusive de alguém que não segue aquele deus. Aurion começou sem seguidores porque nenhum reino desta seed recebeu o Culto do Sol; seus Actors não demonstram conversão.

Relatos de declínio: **0**; notícia de crescimento rival: **0**; intervenções: **0**. O canal existente exige duas perdas conhecidas de membros reconhecidos por ritual/declaração, seguidas de um relato religioso. Ele não transportou declínio agregado nesta campanha. **O desaparecimento agregado de Actors não tem canal próprio.** A deterioração objetiva pode continuar desconhecida pelos deuses.

## Incongruências e limites encontrados

**Captura impossível oferecida — confirmado.** Na hora 500, John Bruma escolheu capturar Cael Luar, já detido por Iria Solaris de 491h até 503h. O escore de captura foi 103,50; a execução recusou. O cálculo terminal verifica guarda/caso conhecido, mas omite a condição de detenção do alvo que `Justice.capture` exige. Eventos **553168 e 564020**. É uma inconsistência entre seleção e execução, sem corrupção do save; não foi corrigida durante esta validação.

**Fome ainda domina a mortalidade.** Causas finais: `{'both': 4, 'hunger': 281, 'combat': 10, 'thirst': 1}`. Fome isolada representa **281/296 = 94,93%**; outras quatro mortes envolveram fome e sede. O rótulo registra a causa final, não todo dano anterior: Cael Luar acumulou 117 HP de danos de combate e nove de fome antes da morte classificada como fome. Esses totais acumulados não equivalem ao saldo de HP, pois houve recuperação.

Na hora 1.000 havia **11.081 unidades de comida nos estoques das localidades e 392 nos inventários dos vivos**. Disponibilidade mundial não demonstra acesso individual: esse retrato final não prova comida acessível na localidade e hora de cada morte. O próximo diagnóstico deve verificar acesso, dinheiro, lesões e prioridade das ações por vítima.

**Identificação narrativa ambígua — confirmado.** 1776 NPCs usam 211 nomes completos distintos; 210 nomes se repetem. Duas Elena Kars formaram o primeiro grupo. Os IDs continuam distintos, sem colisão de entidades; profissão, localidade e ID foram usados na crônica para evitar confusão.

**Oportunidade calculada não garante escolha executada.** Finalizar liderou em 6 retratos de oportunidade; 3 não tiveram uma escolha terminal associada: horas 580, 838 e 913. Necessidades vitais concorrem antes da escolha terminal, e presença/saúde podem mudar. A evidência exportada não identifica o motivo exato de cada perda; esses casos permanecem uma lacuna de acompanhamento, não prova de sorteio residual. Nas escolhas efetivas houve **zero divergências** entre o vencedor contextual e a ação terminal.

**Linha extrema: somente hipótese.** Ruan Montes finalizou quando finalizar marcou 70,74. Aldren Kars, com ruminação 100 e pressão 75, retirou-se porque o medo elevou essa opção a 75 contra 59,71 de finalizar. Os exemplos não exigem morte automática. Não foi implementada uma faixa irreversível; as oportunidades sem desfecho merecem investigação antes de qualquer nova regra.

Validação: **21 verificações estruturais**, **0 erros estruturais** e **0 alertas causais**. A captura acima foi encontrada na revisão manual; zero alertas não significa ausência de todo bug. A auditoria cobre referências históricas, causa/capacidade dos ataques, escolha terminal, morte conhecida e origem/custo divino.

## Evidência preservada

A seed nova produziu outras pessoas, localidades, distribuição religiosa e trajetórias. Como houve também correções de memória e maior duração alcançada, a comparação com Vaelmir-521 não isola o efeito de cada mudança. A crônica apresenta seis trajetórias, sem diálogos ou eventos inventados.

Tempo total **19,49min**; pico de memória incluindo exportação **2.512,8MiB**. Save único **299,71MiB**, com **257.756 eventos históricos**. Núcleo congelado: `b989f75933e3ed5a4fe59a5b2aeb22d5941d37798211d6ab2e3f870f20bd04f7`. O hash do save está em `save_sha256.txt`; não foi duplicado o histórico bruto.

[Crônica nova](</home/hugo/Área de trabalho/procedrual/reports/fase_5_2_1/HISTORIAS_REAIS.md>) · [Resultado completo](</home/hugo/Área de trabalho/procedrual/reports/fase_5_2_1/campanha_1000h_thalendor/resultado_1000h.json>) · [Retratos terminais](</home/hugo/Área de trabalho/procedrual/reports/fase_5_2_1/campanha_1000h_thalendor/oportunidades_terminais.json>) · [Verificação narrativa](</home/hugo/Área de trabalho/procedrual/reports/fase_5_2_1/campanha_1000h_thalendor/verificacao_narrativa.json>) · [Save final](</home/hugo/Área de trabalho/procedrual/reports/fase_5_2_1/campanha_1000h_thalendor/save_final.json>).
