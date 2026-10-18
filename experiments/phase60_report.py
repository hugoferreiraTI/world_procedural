"""Quatro relatórios da Fase 6 derivados dos artefatos, sem simular o mundo."""
from pathlib import Path
import json,re
from collections import Counter
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'reports/fase_6_0'

def read(name):return json.loads((OUT/name).read_text())
def link(name):return f'[{name}](<{ROOT/name}>)'
def table(headers,rows):
    return '\n'.join(['| '+' | '.join(headers)+' |','| '+' | '.join(['---']*len(headers))+' |']+['| '+' | '.join(str(v).replace('|','/') for v in row)+' |' for row in rows])
def metric(w,key):return w.get('world_metrics',{}).get(key,0)
def write(name,content): (ROOT/name).write_text(content.strip()+'\n')

def main():
    c=read('campanha.json');control=read('controles.json');details=read('detalhes_nativos.json');cases=read('casos_reais.json')
    extra=read('analise_nativa.json')
    ab_cases=read('contrafactuais_agua.json')
    career=read('controle_carreira_pipeline.json')
    old=json.loads((ROOT/'reports/fase_5_5_5/campanha.json').read_text())
    log=(OUT/'testes_final.log').read_text();assert log.rstrip().endswith('OK')
    total=int(re.search(r'Ran (\d+) tests',log).group(1));a=control['water_capacity_ab']['before'];b=control['water_capacity_ab']['after']
    counts=c['counts'];death_causes=c['death_causes'];dead=sum(death_causes.values())
    priv=sum(death_causes.get(k,0) for k in ('hunger','thirst','both'))
    for row in c['need_funnel'].values():
        for key in ('never_selected','episodes','active_hours','top_rank_hours','solvable_hours','unknown_solvability_hours','selected_count','executed_count','successful_count','blocked_by_higher_need_count'):
            row.setdefault(key,0)
        row.setdefault('first_selection_max',None)
    needtable=table(['Need','Episódios','Horas ativas','Topo','Solvável observado','Solvabilidade desconhecida','Selecionada','Executada','Sucesso','Preterida','Nunca selecionada','Latência média / máxima (h)'],
        [(k,v['episodes'],v['active_hours'],v['top_rank_hours'],v['solvable_hours'],v['unknown_solvability_hours'],v['selected_count'],v['executed_count'],v['successful_count'],v['blocked_by_higher_need_count'],v['never_selected'],f"{v['first_selection_mean']} / {v['first_selection_max']}") for k,v in sorted(c['need_funnel'].items())])
    gatekeys=[(k.split(':',1)[1],v) for k,v in counts.items() if k.startswith('formalization_gate:')]
    deathtable=table(['Causa','Mortes'],sorted(death_causes.items()))
    factors=Counter(f for row in c['death_funnel'].values() for f in row['factors'])
    factor_table=table(['Fator documentado','Mortes com o fator'],factors.most_common())
    latest={r['town']:r for r in c['town_days']}
    town_table=table(['Local','Tipo','Persistentes presentes','Abstratos','Food / water / grain','Potencial food / water por dia','Realizado food / water na janela','Dias de reserva food / water','Moedas medianas'],
        [(details['town_names'].get(str(id),id),r['kind'],r['persistent_population'],r['abstract_population'],f"{r['food_stock']} / {r['water_stock']} / {r['grain_stock']}",f"{r['potential_food']} / {r['potential_water']}",f"{r['realized_food']} / {r['realized_water']}",f"{r['reserve_days_food']} / {r['reserve_days_water']}",r['median_personal_money']) for id,r in latest.items()])
    comparison=table(['Métrica','Vaelora-55','Neravon-Coesao55','Thalven-Radiografia55','Elyndar-Estabilidade555',c['seed']],
        [('Persistentes iniciais',1880,1898,1916,old['initial_named'],c['initial_named']),
         ('Mortes',315,298,342,sum(old['death_causes'].values()),dead),
         ('hunger / thirst / both / combat','175/126/13/1','160/127/10/1','202/126/14/0','/'.join(str(old['death_causes'].get(k,0)) for k in ('hunger','thirst','both','combat')),'/'.join(str(death_causes.get(k,0)) for k in ('hunger','thirst','both','combat'))),
         ('NewGroupCreated',132,146,144,old['world_metrics'].get('NewGroupCreated',0),metric(c,'NewGroupCreated')),
         ('GroupJoined',998,1064,1075,old['world_metrics'].get('GroupJoined',0),metric(c,'GroupJoined')),
         ('ProposalCreated',46,47,46,old['world_metrics'].get('ProposalCreated',0),metric(c,'ProposalCreated')),
         ('ProposalSubmitted',16,16,13,old['world_metrics'].get('ProposalSubmitted',0),metric(c,'ProposalSubmitted')),
         ('PolicyDecided',2,3,4,old['world_metrics'].get('PolicyDecided',0),metric(c,'PolicyDecided')),
         ('PolicyCompleted',2,0,2,old['world_metrics'].get('PolicyCompleted',0),metric(c,'PolicyCompleted')),
         ('Formalização de facções',0,0,0,old['world_metrics'].get('FactionFormalized',0),metric(c,'FactionFormalized'))])
    ab=table(['Medida','Capacidade antiga no motor 6.0','Capacidade dimensionada no motor 6.0'],
        [('Seed',a['seed'],b['seed']),('Horas',a['hours'],b['hours']),('Mortes',sum(a['death_causes'].values()),sum(b['death_causes'].values())),('Causas',a['death_causes'],b['death_causes']),('Fração de decisões de sobrevivência',f"{a['survival_decision_share']:.2%}",f"{b['survival_decision_share']:.2%}"),('Furtos de mercado',metric(a,'ItemStolen'),metric(b,'ItemStolen')),('Propostas criadas',metric(a,'ProposalCreated'),metric(b,'ProposalCreated'))])
    workkeys=['work_attempts','work_produced','work_paid','work_credit_sixths','training_opportunities_observed','task_delegated']
    worktable=table(['Medida nativa','Valor'],[(k,counts.get(k,0)) for k in workkeys]+[(k,metric(c,k)) for k in ('TrainingStarted','TrainingProgress','ProfessionChanged','WorkerMaterialized','InstitutionalTaskCompleted','InstitutionalCaseFiled','InstitutionalCaseShared','CharacterCaptured')])
    religion_table=table(['Etapa','Contagem de eventos'],[(k,metric(c,k)) for k in ('SacredSiteKnown','PrayerOffered','DivineMessage','DivineAccessAchieved','DivineAudience','DivineIntervention','DivineContractOffered','DivineContractAccepted','DivineContract','Apotheosis')])
    lod_table=table(['LOD','Decisões','Episódios críticos','Mortes por privação','Horas entre decisões: média','Crescimento de fome entre decisões: média','Sede: média','Fadiga: média'],
        [(lod,counts.get('decisions_lod:'+lod,0),counts.get('critical_episodes:'+lod,0),counts.get('deaths_lod:'+lod,0),
          round(counts.get('decision_gap_sum:'+lod,0)/max(1,counts.get('decision_gap_count:'+lod,0)),2),
          *[round(counts.get('physiology_gap:'+lod+':'+k,0)/max(1,counts.get('decision_gap_count:'+lod,0)),2) for k in ('hunger','thirst','fatigue')]) for lod in ('active','local','background')])
    write('FASE_6_0.md',f'''# FASE 6.0 — aprofundamento sistêmico e coerência causal

Base `mvp-13-fase5.5.5` → regras **{c['rules']}**. Geração **{c['generation']}**; save **formato 2**. Seleção pela primeira Need solucionável preservada. **{total} testes passaram**, incluindo os 341 anteriores; controles de neutralidade e continuidade passaram. Campanha **{c['seed']}**, nova, do zero, **300h**, quatro reinos, sem jogador, historical_turns=0. Duas falhas nos scripts de exportação/comparação exigiram duas reproduções da mesma seed para recuperar arquivos: três execuções de300h, 900h de simulação ao todo, sem escolha de resultado ou alteração do código do jogo.

## 1. Baseline e hipóteses

Na 5.5.5 houve 274 mortes: 270 por privação, 4 por combate; 388 ataques, 147 grupos, 1.038 adesões, 52 propostas, 10 submissões e 4 políticas concluídas. A suíte inicial tinha 341 testes verdes. O problema da fase não era ausência de sistemas: era a capacidade de completar os ciclos.

O levantamento novo preservado em {link('reports/fase_6_0/capacidade_base.json')} encontrou capitais com 103 NPCs presentes, demanda hídrica fisiológica de 109,87 unidades/dia e reposição 80. O censo persistente planejado é 104, que exige 110,93/dia. As vilas e cidades comuns não apresentam esse déficit nominal. O controle inicial de 72h na versão antiga não registrou mortes: isso não invalida um déficit acumulativo.

Hipóteses: infraestrutura abaixo do consumo produz emergência estrutural; um trabalho local inviável pode monopolizar Need; afinidade pessoal isolada pode impedir consolidação de grupos; líder exclusivo pode interromper entregas; conhecimento de um guarda em campo não equivale a depósito institucional; raridade religiosa precisa de gates observáveis.

## 2. Mudanças realizadas

- **Água inicial:** dimensionamento depois da densificação, pelo censo final e número real de poços. Demanda = persistentes × 24 × 2/45. Capacidade mínima histórica 80; acima disso, arredondamento por fonte física. Storage = dois dias da capacidade. Estoque inicial continua 80. Sem poços, capacidade projetada zero. Instalação existente é uma fonte passiva; não se inventaram operadores ou bombeamento laboral. O modelo hidrológico anterior continua, sem seca nova ou recurso retirado de outro estoque.
- **Demanda local:** visitantes físicos passam a integrar a demanda alimentar administrativa; seu censo residencial permanece na origem.
- **Emprego:** gate local compartilhado explica NO_PAYER, NO_INPUT, SATURATED e INCOMPATIBLE. Estoque verdadeiro só bloqueia na instalação; oferta remota não é radar. Quem está desempregado pode gerar Need de renda/trabalho quando observou oportunidade real.
- **Carreira:** TrainingOpportunity explicita profissão, instrutor/instituição, progresso, custo, insumo e local. Cozinha mantém formação institucional em taverna; agricultor, mineiro, lenhador, caçador e ferreiro exigem instrutor presente e demanda publicada. A prática produz, usa insumos aplicáveis e remunera do caixa existente. Não há árvore RPG. Materialização continua exigindo déficit persistente, abstrato, reservas e ausência de candidato local; profissional compatível residente fora com rota conhecida também impede materialização precipitada.
- **Organizações:** OrganizationalCompatibility separada de SocialAffinity. Causa, objetivo, estratégia conhecida, localidade, efetividade comunicada, custos, autonomia, adesões e hostilidade compõem a avaliação. Afinidade isolada deixa de ser o gate inteiro. JOIN continua precedendo CREATE; hostilidade, estratégia incompatível, capacidade e desconhecimento ainda permitem grupos distintos.
- **Continuidade:** InstitutionalTask persiste com emissor, instituição, tipo, alvo, local, criação, prioridade, requisitos, papéis autorizados, status, tentativas e barreira. Entrega, resposta, reunião e trabalho de política usam ações humanas existentes. Representantes são autorizados por contato; tarefa precisa ser conhecida, e execução revalida presença/autorização. O estado conhecido da tarefa é individual: conclusão distante só encerra a intenção após notícia ou leitura de comprovante no local. Prefeitura pode designar funcionários presentes para receber documentos; decisão política continua do prefeito. Policy work aceita rotação de trabalhadores habilitados e informados.
- **LOD:** mantém 1/3/6/12 horas conforme o estado original; perseguição conhecida e obrigação urgente promovem temporariamente resolução, sem promoção universal por qualquer Need. Emergência vital já promovia resolução de uma hora e continua com prioridade máxima.
- **Justiça:** conhecimento adquirido em campo só vira registro compartilhável quando o guarda chega ao serviço local; mantém latência e presença para outro guarda aprender. Casos, pistas, atribuições e captura usam o sistema existente. Sem fato conhecido não existe captura autorizada.
- **Violência e religião:** arquitetura letal e critérios de audiência/intervenção preservados. Audiência agora informa separadamente falta de mensagem, presença/acesso, energia e cooldown. Não houve redução de thresholds para produzir mortes ou milagres.
- **Observabilidade V1.1:** métricas privadas por episódio, fluxos de itens, janelas por Town, crescimento fisiológico entre decisões, funis e casos. Metadados mínimos preservam emissões ordinárias descartadas, com kind/turn/ator/alvo/local/pais; não se reconstrói verdade a partir de rumores.

## 3. Mudanças rejeitadas e limites de escopo

Não houve global action utility, redução de fome/sede/dano ou prioridade de sobrevivência, renda gratuita para persistentes, água multiplicada por um fator arbitrário para a capital, polícia telepática, spawn de facção, quota de história ou intervenção divina automática. Não houve banco novo, compressão estrutural do save, demografia ou mudança hora→turno.

Não se acrescentou continuação genérica Acquire→Consume: refeições emergenciais já existem no motor; a presença de recurso ao morrer deve ser examinada por caso e não prova, sozinha, atraso fatal de consumo. Eventos raros não foram forçados. Reunião não substitui a regra canônica de formalização.

## 4. Testes e controles

{total} testes PASS; **25 testes causais novos**, nenhum teste removido/ignorado. Os testes antigos de alimentação foram isolados de emergências aleatórias de parentes da nova geração. O teste de pagador ausente foi fortalecido para exigir bloqueio antes da tentativa improdutiva, em vez de exigir uma primeira falha deliberada. As rodadas intermediárias com falhas estão preservadas; não representam o resultado final.

Os 25 controles pequenos cobrem: capital dimensionada e fonte ausente; capacidade sem produção; visitante; emergência ACTIVE/BACKGROUND; promoção por obrigação conhecida; trabalho sem pagador/insumo e com remuneração; ausência de radar remoto; desempregado com oferta; instrutor ausente/presente e mudança profissional; afinidade baixa com causa comum e hostilidade/estratégia contrária; delegado com líder ausente e save/load; tarefa desconhecida, conclusão distante sem recebimento e continuidade do endereço de aprendizagem; formalização 167/200h; crime em campo versus depósito; guarda sem fato versus captura de rendido; deus sem mensagem versus todos os gates válidos; tombstone; Need preterida/solvabilidade desconhecida; crescimento fisiológico e recurso no inventário ao morrer.

Um controle adicional executou o pipeline completo de carreira: oportunidade conhecida, reserva e aspiração de competência; em {career['hours']} decisões reais, a Need selecionou train e o desempregado tornou-se cozinheiro. Não se chamou train diretamente. Evidência: {link('reports/fase_6_0/controle_carreira_pipeline.json')}.

Neutralidade: OFF/NORMAL/AUDIT, 36h cada, estado de gameplay completo, metadados de Events e RNG idênticos. Continuidade: 100h contínuas = 50h→save/load→50h em todos os campos. Smoke: quatro reinos, 12h, invariantes e geografia válidas.

### A/B causal de infraestrutura

{ab}

Os dois braços usam o mesmo mundo inicial 6.0, mesmas pessoas, inventários e RNG. A única alteração é capacidade/armazenamento de água: antiga 80/160 contra dimensionamento inicial. Ambos mantêm as outras correções 6.0. A comparação por identidade registrou estas transições: {ab_cases['transitions']}. Não houve mortes não relacionadas à privação nem materializações nos dois braços. O saldo é 23 indivíduos vivos em vez de mortos e quatro mortes novas dentro do horizonte de144h; não implica imunidade futura. Esse é um controle isolado da infraestrutura; não é um A/B de toda a versão antiga contra a nova. Mudanças em furto ou política desse par são efeitos observados, sem mecanismo de restauração de taxas.

## 5. Campanha natural e comparação histórica

{comparison}

Todas as campanhas têm 300h. Seeds, populações, regras e agora geração diferem: a tabela é comparação descritiva, não percentual causal de melhoria. O A/B acima é a evidência da intervenção hídrica isolada. A primeira execução completou300h com invariantes válidas e salvou as métricas, mas o exportador não converteu um Location presente em metadados de pai causal. O problema foi corrigido somente no exportador. A primeira reprodução também completou300h com os mesmos dados JSON; uma comparação direta entre chaves int em memória e str no JSON interrompeu a exportação. Esse erro do exportador foi corrigido com normalização e checkpoint completo anterior à análise. A reprodução final usa as mesmas fontes de jogo/testes e compara todas as métricas finais e os12checkpoints com a primeira execução. Falha e log originais são preservados; nenhum resultado foi escolhido por ser mais interessante.

{deathtable}

Privação: **{priv}/{dead}** mortes. Fração das seleções por Need de sobrevivência: **{c['survival_decision_share']:.2%}**. Em **{factors.get('NO_MONEY',0)+factors.get('AFFORDABILITY',0)}** mortes havia food no mercado municipal local, mas a carteira não cobria uma unidade ({factors.get('NO_MONEY',0)} sem dinheiro; {factors.get('AFFORDABILITY',0)} com valor insuficiente). Isso é estado econômico observado no óbito, não prova de que o NPC sabia do estoque ou conseguiria chegar a tempo. A fração de seleções não mede horas de ação e inclui preparo que pode trocar a ação sem trocar a Need selecionada.

As 12 conferências de 25h das três execuções passaram nas invariantes e geografia. O saldo monetário foi explicado pela fonte abstrata existente; residual zero, inclusive com mortos, tesourarias, caixa abstrato, grupos, facções e políticas. Dinheiro inicial {c['initial_money']}, final {c['final_money']}, fonte explícita {c['explicit_currency_source']}. A economia não é monetariamente fechada: trabalho abstrato já emite moeda e isso continua declarado.

## 6. Need starvation

{needtable}

Horas ativas contam episódios conhecidos pelo motor; o topo é o ranking da última decisão real até a seguinte. Não se executa planejamento COMMAND extra para medir alternativas. Solvabilidade só é afirmada por avaliação real daquela hora ou probe puro de alternativa imediata/local. O restante é **UNKNOWN**, inclusive necessidades inferiores não avaliadas. Portanto zero em solvable_hours não significa impossibilidade; nunca selecionada não significa automaticamente monopolização. Preterida exige alternativa observada e Need superior vencedora. Não se extrapola estoque entre decisões. Reativações, expirações e resolução por episódio estão no JSON.

## 7. Sustentabilidade por Town

Última janela diária completa, h288. Produção nominal é potencial com profissionais/infraestrutura, não garantia de output. Realizado food é a janela anterior; water é reposição efetiva da janela fechada. Estoques são posteriores à reposição/consumo administrativo.

{town_table}

Todas as janelas, preços, acessibilidade, consumo e affordability estão no JSON. Contadores de consumo são cumulativos; subtraia linhas adjacentes para obter o fluxo diário. Consumo de água de abstratos é **0 porque não está modelado**, não porque se demonstrou que abstratos não precisam beber. Não se acrescentou fisiologia demográfica nesta fase. Estoque não garante conhecimento, rota, dinheiro, aquisição ou tempo.

### Funil das mortes por privação

{factor_table}

Fatores podem coexistir. WORLD_SHORTAGE exige ausência de item material no mundo; LOCAL_SHORTAGE é estoque comercial municipal local zero; não avalia todo POI, depósito de facção, recurso silvestre ou fonte não comercial. Essa limitação impede tratá-lo sozinho como explicação definitiva de acesso. Material existente pode pertencer a morto ou estar inacessível. RESOURCE_OWNED_AT_DEATH é evidência de posse; não prova que um agente fisicamente capaz tinha ação livre para consumir. PRIORITY_COMPETITION e gates recentes são associações documentadas, não contrafactual automático de evitabilidade. Ausência de evidência permanece OTHER_UNKNOWN. Cada caso conserva níveis, inventário, posição/goal, última decisão e timestamps disponíveis.

## 8. LOD e fisiologia

{lod_table}

Crescimento soma a fisiologia efetivamente aplicada entre oportunidades, com clamp em 100, separado do saldo líquido depois de comer/beber. Decisões são agrupadas pelo LOD da oportunidade; o primeiro intervalo de cada pessoa não compõe a média. Mortes da tabela são as por privação. Contagem de todas as mortes pelo último LOD de decisão conhecido, incluindo combate: **{extra['all_deaths_by_last_decision_lod']}**; sem registro: {len(extra['deaths_without_decision_lod'])}. Esse último LOD não é um novo snapshot físico inventado do instante da morte. Latência por LOD da primeira seleção: {extra['need_latency_by_first_selection_lod']}. Não há experimento que demonstre neutralidade estatística completa de toda vida social por LOD; o controle pequeno demonstra resposta vital equivalente em emergência local.

## 9. Trabalho, carreira e continuidade

{worktable}

Training opportunities observed conta exposições a oportunidades, não vagas únicas. Produção e pagamento de trabalho são contabilizados separadamente; serviços podem pagar sem criar item. O salário sempre sai do pagador. Tentativas de trabalho que falharam fora de uma decisão real não criam efeitos privados persistentes. Tarefas: {c['tasks']}. Conclusões com morte anterior do emissor comprovada por ordem de Events: {extra['tasks_completed_after_issuer_death']}. A métrica geral de delegação compara executor e emissor; sozinha não prova ausência física do emissor. Políticas: {c['policies']}. Não se trata rotação como mudança de dono da política.

## 10. Grupos, facções e formalização

Recusas observadas por causa: {extra['join_rejection_reasons']}.

Grupos finais: {c['groups']}. Facções finais: {c['factions']}. Fragmentação registra grupos conhecidos, score/motivos, distância, lotação, relação e lacuna de conhecimento. Grupo semelhante desconhecido não é deduplicado por varredura global do NPC.

{table(['Gate de formalização','Ocorrências de avaliação'],sorted(gatekeys))}

Requisitos 4 investimentos, 168h, 3 membros, 3 presentes, contribuição real e score 65 preservados. O funil conta avaliações realmente feitas; grupos que não chegaram a uma candidatura não recebem um score fictício. Um mesmo candidato pode falhar vários gates; não somar essa tabela como grupos distintos. A ausência de formalização não foi mascarada com limiar menor.

## 11. Crime, violência e religião

{table(['Etapa','Eventos'],[(k,metric(c,k)) for k in ('ItemStolen','PersonalItemStolen','WantedIssued','InstitutionalCaseFiled','InstitutionalCaseShared','InvestigationClue','PursuitSearch','SuspectLocated','CharacterCaptured','GuardResponded','PursuitEnded','CharacterAttacked','CharacterIncapacitated','ExecutionOpportunity','TerminalDecision','IncapacitatedSpared','FirstAidGiven','CharacterWithdrew','CharacterFled','CharacterSurrendered','ApologyGiven','RestitutionGiven','ConflictForgiven')])}

Motivos refinados dos ataques pelos flags explícitos, mode auditado/parent e Need: **{extra['attack_motives_refined']}**. Dano registrado nos Events de ataque: {extra['attack_damage_recorded']} HP, sem atribuir dano de privação a combate. Latências institucionais: {extra['latencies']}. Crimes e testemunhas, recebimentos pela autoridade e desfechos estão nos contadores nativos. Testemunha aqui significa terceiro além dos participantes registrado no Event. Gravidade e captura não usam posição atual remota como pista. A arquitetura letal permanece motive→decisão→acesso→ataque→incapacidade→desfecho. Os números não são quota de mortes.

{religion_table}

Mensagens recebidas, presença regional, energia, afinidades e gates de audiência usam estado informado da divindade. A classificação nativa de motivos de ataques é uma heurística de contexto; o audit detalhado e seus Facts devem confirmar a motivação, especialmente em response e em casos hedonistas. O controle com todos os gates válidos prova acessibilidade, não frequência natural garantida. Zero em audiência/apoteose é permitido. Não foi introduzido favorecimento automático.

## 12. Retenção e casos reais

{c['history_events']} Events históricos, {c['traces_retained']} traces retidos e {c['tombstones']} metadados mínimos. Pais distintos referenciados: {c['parent_ids']}; payloads completos ausentes no índice: {c['missing_full_payloads']}; IDs ausentes até como metadados: **{len(c['missing_even_metadata'])}**. Tombstone informa identidade/tempo/atores/local/pais; não contém texto/contexto completo, Fact nem razão de decisão inventada.

O arquivo histórico compactado tem {c['archive']['bytes']/1e6:.2f} MB e **não é save completo**. JSON/save não foi substituído ou otimizado. Controle de persistência completo foi feito nos mundos de 100h. {link('DECISOES_6.md')} conserva exemplos naturais com Events, traces, tentativas e recebimentos disponíveis.

## 13. Sistemas ainda desequilibrados e decisões futuras

Sobrevivência continua sendo analisada pelos fatores acima, sem prometer mundo sustentável por decreto. O dimensionamento inicial não garante água futura: consumo extra, transferência, oferenda, acesso e obra afetam a reserva. O potencial alimentar é uma projeção de expediente de10h, não um limite físico demonstrado de ocupação de todas as cozinhas; slots são usados no planejamento/treinamento, sem um calendário de ocupação simultânea de estações. Produção alimentar nominal pode exceder demanda e ainda não se realizar por tempo, emprego, insumos, estoque, renda ou prioridades.

Compatibilidade organizacional ainda usa uma estratégia simples comunicada e custos conhecidos; não implementa ideologia completa. Delegação cobre quatro obrigações concretas, não toda ação possível de facção/prefeitura. A separação individual de status foi implementada para tarefas; livros agregados legados de coordenação organizacional não equivalem a uma auditoria de todo conhecimento institucional. Registro criminal permanece simplificado; morte/resolução administrativa e troca de atribuições ainda merecem exame. Crescimento dos registros privados continua dívida técnica. Solvabilidade UNKNOWN e causas não provadas permanecem explícitas.

Formalização, violência e religião não foram calibradas para cumprir metas. Não há neutralidade estatística total demonstrada para todos os LODs. Demografia, seca dinâmica nova, transporte comercial autônomo completo, diplomacia/guerras e otimização de save ficam para fases próprias.

Evidências: {link('reports/fase_6_0/testes_final.log')}, {link('reports/fase_6_0/controles.json')}, {link('reports/fase_6_0/campanha.json')}, {link('reports/fase_6_0/detalhes_nativos.json')}, {link('reports/fase_6_0/casos_reais.json')}. Implementação: {link('procedural/causal_audit.py')}, {link('procedural/sustainability.py')}, {link('procedural/organizational_compatibility.py')}, {link('procedural/institutional_tasks.py')}, {link('tests/test_phase60.py')}.
''')
    write('COERENCIA.md',f'''# COERÊNCIA — Fase 6.0

Campanha **{c['seed']}**, 300h, seed nova. Controles artificiais e mundo natural são evidências separadas. Coerente em controle não significa que todo ciclo ocorrerá naturalmente.

{table(['Sistema','Função pretendida','Observado / veredito','Gargalo / motivo','Mudança e efeito','Risco restante'],[
('Sobrevivência','Evitar emergência quando há capacidade/acesso',f"Parcial: {priv}/{dead} mortes por privação",'Capitais antes produziam 80 água/dia para consumo fisiológico ~111','Dimensionamento inicial; efeito isolado no A/B','Acesso e produção realizada ainda dependem de pessoas'),
('Economia','Input→trabalho→produto→dono→pagamento',f"{counts.get('work_attempts',0)} tentativas; {counts.get('work_produced',0)} unidades; {counts.get('work_paid',0)} moedas pagas",'Sem pagador/insumo não há salário/produto','Gate físico e registro de fluxos; caixa conservado salvo fonte abstrata declarada','Capacidade nominal não mede tempo produtivo real'),
('LOD','Reduzir detalhe sem condenar por distância','Controle de emergência local equivalente; distribuição natural no relatório','Necessidades urgentes podiam perder oportunidades de decisão','Promoção limitada a pressão conhecida; crescimento fisiológico medido','Neutralidade social estatística não demonstrada'),
('Carreira','Responder à demanda e aprendizagem material',f"{metric(c,'TrainingStarted')} inícios; {metric(c,'ProfessionChanged')} mudanças",'Instrutor, prática, demanda e pagador','Interface comum; controle confirma mudança real sem dinheiro grátis','Cobertura por profissão ainda seletiva'),
('Grupos','Cooperar antes de fragmentar',f"{metric(c,'NewGroupCreated')} criados; {metric(c,'GroupJoined')} adesões",'Afinidade pessoal não respondia adequação à causa','OrganizationalCompatibility separada; JOIN primeiro','Estratégia/custos simples; grupos desconhecidos continuam possíveis'),
('Continuidade','Obrigação sobreviver ao emissor',str(c['tasks']),'Liderança exclusiva e entrega física','Tarefas conhecidas, representantes presenciais e revalidação','Não cobre toda atividade institucional'),
('Prefeitura/policy','Receber, decidir e executar com orçamento',str(c['policies']),'Presença, autoridade e insumos','Recepção delegável; política aceita trabalhador habilitado rotativo','Decisão maior continua do prefeito'),
('Formalização','Institucionalizar continuidade custeada',f"{metric(c,'FactionFormalized')} formalizações",'Gates discriminados, sem quotas','Mesma regra canônica; nenhum limiar relaxado','Frequência pode continuar rara'),
('Justiça','Evidência→caso→pista→contato→resolução',f"{metric(c,'WantedIssued')} procuras; {metric(c,'CharacterCaptured')} capturas",'Saber em campo não equivale a registrar','Depósito físico e aprendizagem local com latência; captura controlada válida','Ciclo administrativo simplificado'),
('Violência','Causa plausível e consequência proporcional',f"{metric(c,'CharacterAttacked')} ataques; {death_causes.get('combat',0)} mortes de combate",'Desfechos precisam competir no contexto terminal','Arquitetura e thresholds preservados; motivos/desfechos medidos','Contagem sozinha não prova qualidade de todos os confrontos'),
('Religião','Acesso e resposta pelo conhecimento divino',str(c['religion']),'Mensagem/presença/afinidade/energia/cooldown','Gates explícitos; controle de acesso válido sem forçar naturalidade','Raridade e conhecimento retido limitado'),
('Observabilidade','Explicar sem alterar decisões',f"OFF/NORMAL/AUDIT iguais; pais sem metadados: {len(c['missing_even_metadata'])}",'Payload descartado e solvabilidade não avaliada','Tombstone e métricas V1.1 privadas; save/load igual','UNKNOWN não é impossível; retenção ainda cresce')])}

{link('FASE_6_0.md')} contém os números completos, intervalos e ressalvas. {link('BALANCEAMENTO.md')} registra parâmetros. Não há afirmação de mundo perfeito ou de causalidade entre campanhas com seeds diferentes.
''')
    decisions=[f'# DECISÕES REAIS — {c["seed"]}', '\n300h naturais. Nenhum caso abaixo é fixture ou reconstrução inventada. IDs de tarefa, organização, alvo e personagem têm contratos diferentes; não se traduz alvo institucional como pessoa sem evidência.\n']
    for case in cases:
        ev=case['event'];tr=case.get('trace');attempt=case.get('attempt')
        decisions += [f"## Event #{ev['id']} — {ev['kind']}, h{ev['turn']}",
            f"Ator: {details['names'].get(str(ev['actor_id']),ev['actor_id'])} (#{ev['actor_id']}); alvo #{ev['target_id']}; pais {ev['parent_event_ids']}.",
            ev['description'],
            f"Decisão {tr['id']} (decisor #{tr['actor_id']}), Need {tr['need_kind']}, episódio {tr['need_episode_id']}, prioridade {tr['need_priority']}, ação {tr['selected_action']}, score {tr['selected_score']}." if tr else 'Trace privado não retido/não associado; nenhuma motivação foi inventada.',
            f"Tentativa {attempt['id']}: {attempt['action']}, sucesso {attempt['success']}, resultado {attempt['outcome']}." if attempt else 'Tentativa individual ausente; emissão pode pertencer a consequência/registro do sistema.',
            f"Contexto real: `{json.dumps(ev['context'],ensure_ascii=False)}`.",
            f"Recebimentos preservados no exemplo: {len(case['receipts'])}. Detalhes, fontes e pais estão no JSON.\n"]
    decisions.append('## Mortes por privação: casos com evidência disponível\n')
    for key,row in list(c['death_funnel'].items())[:16]:
        dr=details['death_records'].get(str(key),{})
        decisions.append(f"- **{details['names'].get(str(key),key)} #{key}**, h{row['turn']}: causa {dr.get('cause')}; fome/sede {row['hunger']}/{row['thirst']}, food/water próprios {dr.get('food')}/{dr.get('water')}; fatores {', '.join(row['factors'])}. Última decisão {row['last_decision']}; ação {row['goal']}. Estoques observados pela auditoria: `{json.dumps(row['stock'],ensure_ascii=False)}`. Isso não significa conhecimento automático do NPC.")
    decisions.append('\n## Trabalho e barreiras religiosas/formalização\n')
    decisions.append('Exemplos de trabalho produtivo registrados no mundo:')
    for row in details['native_samples'].get('work_cases',[])[:10]:decisions.append(f"- h{row['turn']}, {details['names'].get(str(row['actor']),row['actor'])} #{row['actor']}, {row['profession']}: produziu {row['produced']}, recebeu {row['paid']}, status {row['status']}.")
    for row in details['native_samples'].get('religion_gates',[])[:8]:decisions.append(f"- h{row['turn']}, mortal #{row['actor']}, deus #{row['god']}: gates {row['gates']}; mensagem recebida {row['has_message']}, energia {row['energy']}, afinidade {row['affinity']}, devoção {row['devotion']}.")
    decisions.append(f"\nSe treinamento, captura, formalização ou audiência não aparecem, a campanha não demonstrou esse acontecimento. Os controles documentados provaram os caminhos aplicáveis; não foram apresentados como lore. Evidências: {link('reports/fase_6_0/casos_reais.json')} e {link('reports/fase_6_0/detalhes_nativos.json')}.\n")
    write('DECISOES_6.md','\n\n'.join(decisions))
    write('BALANCEAMENTO.md',f'''# BALANCEAMENTO — Fase 6.0

Regra: alteração mínima causal, sem quota de eventos. A campanha não foi usada para escolher seed ou reajustar parâmetros depois de observar resultados.

{table(['Parâmetro/regra','Anterior','Novo','Motivo / evidência','Efeito controlado / natural'],[
('Capacidade hídrica inicial','80/dia para toda localidade','80 mínimo; acima disso ceil((N×48/45)/poços)×poços','Censo persistente final supera capacidade nas capitais; projeto depois da densificação',f"A/B: {a['death_causes']} → {b['death_causes']}; natural {death_causes}"),
('Armazenamento de água','160','2×capacidade projetada','Dois dias da infraestrutura inicial; estoque inicial não cresce','Cidades/vilas pequenas mantêm 160; capital típica 222'),
('Demanda alimentar local','1,2×residentes presentes + ceil(abstratos/120)','1,2×todos os persistentes presentes + ceil(abstratos/120)','Visitante também consome; não muda residência/censo','Controle +1 visitante = +1,2 de demanda; efeito natural incluído nas janelas'),
('Gate de adesão social','Afinidade >=25 como requisito isolado','Adequação organizacional >=50; afinidade componente limitado a15','Causa e utilidade da instituição não se reduzem à amizade','Controle aceita causa comum com afinidade<25; hostilidade/estratégia continuam vetando'),
('Adequação organizacional: componentes','Sem índice separado','causa40, objetivo15, estratégia10, localidade10 ou3, eficácia -20..10, afinidade0..15; autonomia -0,1×independência; dues -3×custo; risco ilegal -0,25×honestidade; adesões -4 cada; hostilidade -0,2×valor','Componentes conhecidos ou observados, sem bônus por existência global da organização',f"Natural {metric(c,'NewGroupCreated')} grupos e {metric(c,'GroupJoined')} adesões; não atribuir tudo ao score"),
('Representantes de grupo','Líder exclusivo para entrega','Até2 representantes presentes autorizados','Eliminar falha por ausência do emissor sem execução automática','Controle de delegado/save-load passa; tarefas naturais no relatório'),
('Tarefa institucional: prioridade/utility','Sem fila persistente','Prioridade55; utility55 + diligence20 + persistence20; execução dentro da Need organizacional ou obrigação conhecida','Continuidade sem furar prioridade vital; pesos análogos a funções existentes',str(c['tasks'])),
('Reunião','Candidatura a cada24h; execução direta não limitava repetição','Mantém24h também na execução, exceto primeiro encontro','Candidato/execução devem representar a mesma cadência','Não foi reduzido intervalo para gerar mais investimento'),
('LOD por pressão','Promoção por fisiologia/combate/migração e janelas ativas','Também perseguição/obrigação conhecida ativa com prioridade>=65','Resolução temporária enquanto existe pressão operacional','Controle com obrigação70 promove 12→1; baixa pressão não promove'),
('Aprendizagem produtiva geral','Cozinha: progresso12..36, salário proporcional','Interface comum; outros caminhos exigem instrutor e déficit, progresso max(12,36-diligence//5), 1 unidade/h salvo arma1/operação; crédito2 sextos/unidade','Mesmo modelo de prática material, sem conversão instantânea ou renda grátis','Controles de produto/pagamento/profissão passam; eventos naturais discriminados'),
('Demanda agrária','Sem déficit publicado geral','ceil(max(0,demanda_food-capacidade_caça)×2/3 /20) agricultores requeridos; publicar somente com déficit e grain baixo','20 = duas unidades/h por dez horas de expediente nominal; não aumenta output real','Instrutor e tempo continuam gates; nominal não é produção realizada'),
('Formalização','168h, investimento4, membros3, presentes3, score65, contribuições/fundos reais','Inalterado','Medir gates antes de rever proxy',f"Natural {metric(c,'FactionFormalized')} formalizações"),
('Fisiologia/dano/recuperação/letalidade/religião','Valores 5.5.5','Inalterados','Sem resolver resultado por limiar arbitrário','Regressões antigas e cenários específicos passam')])}

### A/B de uma variável

{ab}

Mesmo mundo inicial e RNG; os dois braços usam as demais regras 6.0. Alteração de water_daily/storage é um único conjunto de infraestrutura. Não equivale a todas as mudanças 5.5.5→6.0 isoladas. Sem repetição por resultados.

### Efeitos colaterais

Furtos de mercado no A/B: **{metric(a,'ItemStolen')}→{metric(b,'ItemStolen')}**. Propostas **{metric(a,'ProposalCreated')}→{metric(b,'ProposalCreated')}**. Fração vital **{a['survival_decision_share']:.2%}→{b['survival_decision_share']:.2%}**. Nenhuma taxa foi restaurada para fabricar conflito. A campanha final serve à observação integrada, não à atribuição causal de cada mudança numérica.

### Versões

RULES_VERSION passa a mvp-14-fase6.0. GENERATION_VERSION passa a mvp-6.0 porque há nova regra de infraestrutura inicial; essa versão participa do hash da seed, logo nomes iguais não garantem mesmo mundo entre versões. Formato de save continua2: campos novos possuem defaults, sem troca de codec. O carregador mantém a recusa de outra rules_version; saves 5.5.5 não são compatíveis com6.0 e não houve migração silenciosa.
''')
    print(json.dumps({'reports':['FASE_6_0.md','COERENCIA.md','DECISOES_6.md','BALANCEAMENTO.md'],'tests':total,'natural_hours':c['hours']},ensure_ascii=False))

if __name__=='__main__':main()
