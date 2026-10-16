"""Relatório da 5.5.5 a partir das evidências medidas; não simula nem altera regras."""
import ast
from dataclasses import asdict
import gzip
import hashlib
import json
from pathlib import Path
import re
import subprocess

from procedural import RULES_VERSION
from procedural.persistence import decode
from .phase555_validation import sources

ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'reports/fase_5_5_5'


def read(name):return json.loads((OUT/name).read_text())
def link(path,label=None):return f'[{label or Path(path).name}](<{ROOT/path}>)'
def table(headers,rows):
    esc=lambda value:str(value).replace('|','\\|').replace('\n',' ')
    return '\n'.join(['| '+' | '.join(headers)+' |','| '+' | '.join(['---']*len(headers))+' |']+
                      ['| '+' | '.join(esc(v) for v in row)+' |' for row in rows])+'\n\n'
def source(file,symbol):
    tree=ast.parse((ROOT/'procedural'/file).read_text());body=tree.body;node=None
    for part in symbol.split('.'):
        node=next(n for n in body if isinstance(n,(ast.ClassDef,ast.FunctionDef)) and n.name==part);body=node.body
    return f'[{symbol}](<{ROOT/"procedural"/file}:{node.lineno}>)'
def mb(value):return f'{value/1_000_000:.2f} MB'


def main():
    c=read('campanha.json');controls=read('controles.json');old=read('testes_antigos.json');legacy=read('legado.json');example=read('cadeia_real.json')
    assert c['status']=='completed' and c['hours']==300
    assert sources()==c['sources']==controls['sources']
    log=(OUT/'testes_final.log').read_text();match=re.search(r'Ran (\d+) tests in ([\d.]+)s',log)
    assert log.rstrip().endswith('OK') and match and int(match[1])==341
    for row in old:assert f"({row['test']}) ... ok" in log,row['test']
    with gzip.open(OUT/'historico_nativo.json.gz','rt',encoding='utf-8') as stream:archive=decode(json.load(stream))
    people=archive['characters'];o=archive['observability'];m=c['world_metrics']
    who=lambda id:people.get(id,{}).get('name',f'#{id}')
    # Corrige somente o nome do contador no relatório; não modifica campanha,
    # observação, save, eventos ou a execução natural já registrada.
    religious_reports=m.get('ReligiousDeclineReported',0)
    events=dict(archive['events']);events.update(o.event_archive)
    unavailable_persisted=sorted({i for event in events.values() for i in event.parent_event_ids if i not in events})
    new_tests=[n.name for n in ast.walk(ast.parse((ROOT/'tests/test_phase555.py').read_text()))
               if isinstance(n,ast.FunctionDef) and n.name.startswith('test_')]
    text=f'''# FASE 5.5.5 — correção, tratamento, limpeza e observabilidade histórica

**Concluída.** Base: `mvp-12-fase5.5` → atual: `{RULES_VERSION}`. Geração: `mvp-5.4`. Formato de save: **2**.

**341 testes ativos passaram; B01–B08 corrigidos; continuidade e neutralidade passaram; campanha nova de 300h concluída.** Não houve ajuste de produção, dano de privação, prioridade fisiológica, frequência de violência ou thresholds para aumentar eventos raros.

## 1. Estado inicial e escopo

A auditoria anterior registrou 326 testes: **305 PASS, 18 FAIL e 3 ERROR**. Os 21 resultados não verdes foram examinados individualmente. Nenhum teste foi desativado ou marcado como sucesso esperado para esconder uma falha. Foram acrescentados **{len(new_tests)} testes**, resultando nos 341 atuais.

O trabalho ficou nas correções confirmadas, eliminação de implementações contraditórias, contratos de consulta e Observabilidade Histórica V1. Não foram implementados nascimentos, idade, gerações, guerra entre reinos, eleições, diálogo geral, novas profissões ou nova fase de balanceamento.

A auditoria de origem continua preservada em {link('reports/auditoria_total/RADIOGRAFIA_TOTAL.md','Radiografia anterior')}. Seus diagnósticos de bugs descrevem a versão anterior, não o estado atual.

## 2. B01–B08: causas, correções e prova

'''
    bugs=[
        ('B01','Contextos compartilhavam listas/dicionários do mundo e entre Facts. Save/load rompia o alias e a história divergia.',
         'Event e Fact fazem deepcopy na construção: a proteção cobre todos os produtores, inclusive coleções aninhadas/conjuntos. O pós-morte não altera mais CharacterKilled; PostKillAppraisal é separado e aponta para a morte. Persistência aceita conjuntos tipados.',
         'Snapshots aninhados; independência entre ouvintes; adesão após load com igualdade integral; pós-morte separado.',source('models.py','Event')+'; '+source('models.py','Fact')),
        ('B02','Society.react retornava antes de atribuir responsabilidade; a autoridade ativa não fazia essa consequência.',
         'Institutions.react_decision concentra registro, falhas e responsabilidade em recusa conhecida com confiança ≥60. Repetição não duplica; melhoria de confiança pode completar a atribuição. Ramo morto removido.',
         'Decisão não recebida não atribui; recebida atribui; duplicação e confiança melhor testadas; assume_local_office volta a respeitar as pré-condições.',source('institutions.py','Institutions.react_decision')),
        ('B03','Preparação recriava fill_water depois dos filtros normais, inclusive em cooldown ou fonte sem água conhecida.',
         'GoalSystem.eligibility é usada pela avaliação e pela preparação. Verifica falha/cooldown, mapa/acesso, fonte conhecida, existência do poço e disponibilidade observável. Fonte local pode ser inspecionada; ausência remota só é usada quando conhecida recentemente.',
         'Preparo bloqueado por cooldown, observação remota de falta e fonte local vazia. Sem alterar água produzida, sede ou dano.',source('goals.py','GoalSystem.eligibility')),
        ('B04','Via de Access/found_faction pulava score e presença exigidos no fluxo de reuniões.',
         'can_formalize reúne liderança, estado, tipo do grupo, idade, membros presentes, investimento, contribuições, score e limites. Todos os entrypoints revalidam a mesma função. A alternativa de Access usa o encontro presente, sem deslocar o ator para longe dos fundadores.',
         'Dois presentes são rejeitados pelas duas vias; estado maduro válido formaliza com débito pessoal real. Fixtures antes aceitas pelo atalho agora satisfazem o score.',source('institutions.py','Institutions.can_formalize')),
        ('B05','O candidato existia por food OU water; execução podia escolher justamente o recurso ausente.',
         'MaterialCandidate → Solution → Goal transportam resource_kind e quantidade. A alternativa prefere o recurso da maior privação quando disponível, ou o recurso existente; execução respeita a intenção e revalida estoque/presença.',
         'Organização com comida e sem água, membro com mais sede: transfere a comida escolhida, sem fabricar recurso.',source('institutions.py','Institutions.faction_candidates')),
        ('B06','Need reutilizada guardava group_id e faction_id, e consumidores escolhiam entidades diferentes.',
         'organization_type/organization_id são canônicos. O alias correspondente é mantido para consumidores antigos, sempre exclusivo. bind_organization elimina o oposto; pressão, candidato e execução leem a mesma identidade. Contexto ambíguo é inválido.',
         'Reuso facção→grupo, chave de pressão, inexistência de candidato da facção e recusa de execução sobre organização diferente.',source('organization_context.py','bind_organization')),
        ('B07','Causas que caíam no fallback, como exploration, eram descritas como autoinfligidas.',
         'Descrições explícitas para privação, combate, self_harm, exploração e divina. Causa desconhecida aparece pelo identificador real, sem inventar semântica.',
         'Exploração e causa desconhecida preservam causa e texto coerentes.',source('engine.py','Engine.finish_death')),
        ('B08','report_congregation era produzido por Faith, mas não tinha entrada em Utility.BASE.',
         'Base igual à comunicação institucional report_to_faction (45), com dever/diligência (20), devoção (25) e penalidade de viagem já existente. A candidatura continua exigindo perdas conhecidas e cooldown; execução continua exigindo canal ritual físico.',
         'Orações testemunhadas + duas mortes conhecidas → produtor → Utility → Goal → execução; sem KeyError. Não foi apenas acrescentado um número sem semântica.',source('utility.py','evaluate')),
    ]
    text+=table(['Bug','Causa','Correção','Verificação','Código'],bugs)
    text+='''### Correções de integração necessárias

A responsabilização ativa revelou uma segunda contradição: aprender a resposta já atualizava o grupo, e o filtro antigo passava a considerar impossível retransmiti-la. A entrega aos demais agora tem confirmação própria (`relayed_responses`, limitada a 12 IDs), exige representante e outro membro presentes e não repete a consequência institucional. Retransmitir concorre com as ações locais já elegíveis; não bloqueia artificialmente a tomada de cargo.

Um ataque que mantém decisão letal ativa também passou a usar na seleção o mesmo `LethalDecisionSystem.action_audit` exigido na execução. Isso evita oferecer um ataque cuja incapacidade física já o torna inexequível; não alterou dano, score letal ou limiar de capacidade.

`Society.promote` trata vínculo/assignment inválido com retorno False. Convite, aceitação e promoção continuam sendo etapas distintas.

## 3. Legado: classificação e remoção

A análise considerou chamadores no código, strings de ação/dispatch, listeners/callbacks, fixtures e chamadas medidas na auditoria anterior. Contagem de um método inteiro não é cobertura de seus ramos. Nenhum uso externo fora do repositório foi presumido.

'''
    text+=table(['Símbolo','Classificação','Evidência','Ação'],[(x['symbol'],x['classification'],x['evidence'],x['action']) for x in legacy])
    text+=f'''Evidências pesquisáveis: {link('reports/fase_5_5_5/legado.json')} e {link('reports/fase_5_5_5/referencias_legado.json')}.

As duas constantes removidas não foram ligadas a regras novas. O abandono de compromissos continua usando a fórmula existente de pressão/falhas/persistência e sua duração máxima. `SURVIVAL.normal/moderate/severe` foram mantidas: têm leitores internos em `band`, embora não apareçam como acessos externos `SURVIVAL.campo`.

## 4. Os 21 testes antigos não verdes

“Depois: PASS” significa execução na suíte completa final. A causa foi classificada antes de atualizar a expectativa ou a fixture.

'''
    text+=table(['Teste','Antes','Classificação / causa','Ação tomada','Depois'],[(x['test'],x['before'],x['classification']+': '+x['cause'],x['action'],x['after']) for x in old])
    text+=f'''Tabela estruturada: {link('reports/fase_5_5_5/testes_antigos.json')}.

### Outros testes afetados pela limpeza

- A antiga fixture `Society.material` obrigava materialização política instantânea. O teste agora percorre a política financiada, trabalhador que a conhece e consumo de grão para produzir alimento. A função duplicada foi removida.
- Duas fixtures de formalização anteriormente verdes dependiam do atalho B04. Foram atualizadas para presença e score realmente válidos, sem reduzir os requisitos do motor.
- O teste de cadeia alimentar inviável inspeciona diagnósticos do planejamento e passou a chamar explicitamente `plan_solutions` (COMMAND), em vez de esperar que a consulta pública modificasse o motor.
- O debug deixou de repetir o planejamento: usa as alternativas já avaliadas na decisão real. A primeira instrumentação fazia suas contagens divergirem; a regressão foi corrigida.
- Entradas inválidas do jogador sem evento/tempo transcorrido não deixam traces nem consomem IDs privados. Os testes que exigem save inalterado continuam passando.
- A classificação dos recebimentos usa o tipo do Fact aceito, sem depender de um evento ainda estar no cache transitório. Isso corrigiu divergência observacional após load em fixtures que limpam o histórico.

Rodada intermediária preservada em {link('reports/fase_5_5_5/rodada_intermediaria.log')}; ela documenta erros de desenvolvimento, não testes ativos pendentes.

## 5. Testes novos e suíte final

'''
    text+=table(['Teste novo'],[(name,) for name in new_tests])
    text+=f'''Comando:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
```

**Resultado final: {match[1]} testes, 0 falhas, 0 erros, 0 desativações; {match[2]} segundos.** Log completo: {link('reports/fase_5_5_5/testes_final.log')}.

Uma suíte verde valida contratos e cenários cobertos; não demonstra que uma formalização, apoteose ou audiência necessariamente ocorrerá naturalmente.

## 6. Observabilidade Histórica Nativa V1

'''
    text+=table(['Estrutura','O que representa','Campos/contrato'],[
        ('Event','Acontecimento do mundo','ID de entidade/evento existente, turno, ator/alvo/local, testemunhas, historical, snapshot do contexto, schema_version, parent_event_ids, decision_id/action_attempt_id disponíveis.'),
        ('Need episode','Uma ativação específica da necessidade','Need.id permanece; episode incrementa ao reativar depois do encerramento; identificador n<ID>:<geração>, sem consumir IDs do jogo.'),
        ('DecisionTrace','Registro privado da decisão','Ator, turno, LOD, episódio/kind/prioridade, fatos fonte, alternativas geradas/bloqueadas, scores, escolha/score/alvo/recurso, Goal, tentativa, resultado e emissões.'),
        ('ActionAttempt','Tentativa concreta','ID privado, ator, turno, Goal, ação/alvo, success/outcome e IDs emitidos. Caminhada ainda sem execução pode ter Goal e não ter tentativa.'),
        ('LearningReceipt','Aprendizagem, não evento público','Receptor, evento/Fact, turno aprendido, canal, fonte e confiança anterior/posterior; melhorias de confiança são registradas.'),
        ('HistoricalObservability','Estado persistente de observação','Nível, sequência privada, traces/tentativas, anéis recentes, última decisão por ator, recebimentos e arquivo de eventos promovidos.'),
        ('EventIndex','Índices reconstruíveis','Actor, target, location, kind e turn; dados históricos e arquivados, mais cache operacional recente.'),
    ])
    text+=f'''Implementação: {source('observability.py','HistoricalObserver')}, {source('observability.py','EventIndex')} e modelos em {source('models.py','DecisionTrace')}.

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

'''
    text+=table(['API','Classificação','Contrato'],[
        ('GoalSystem.solutions','QUERY','Avalia em cópia isolada do mundo/RNG. Não altera original, cooldown, planos, Facts ou eventos. É mais cara que consultar um índice.'),
        ('GoalSystem.plan_solutions / decide / execute / collective','COMMAND','Planejamento/execução podem manter estado e produzir consequências. Debug usa os resultados já calculados.'),
        ('Institutions.can_formalize / Geography.plan','QUERY','Leitura de requisitos e conexões.'),
        ('Institutions.pressure / decision_scores; Society.decision_scores','COMMAND','Atualizam pressão/diagnóstico da proposta; o nome legado de pontuação não implica pureza.'),
        ('HistoricalObserver.event_details','QUERY','Retorna evento, IDs/causas disponíveis, trace/tentativa, referências de Facts e recebimentos; objetos amigáveis actor/target cobrem Characters. Outros tipos são resolvidos nas coleções do World pelos IDs.'),
        ('EventIndex','QUERY_WITH_CACHE','Índices reconstruídos no load e alimentados por emissões; cache não é estado de gameplay.'),
    ])
    text+='''Exemplo de navegação, sem tomar decisões nem avançar o mundo:

```python
details = engine.observability.event_details(event_id)
by_actor = engine.observability.index.query('actor', actor_id)
by_kind = engine.observability.index.query('kind', 'CharacterKilled')
# details['parent_event_ids'], ['decision'], ['attempt'], ['learning_receipts']
```

## 8. Save e reprodutibilidade

Saves de formato 1 / regras anteriores são **recusados com mensagem de incompatibilidade**. Não existe migração implícita. O formato 2 preserva novos modelos, snapshots, geração/configuração e sequência de IDs privados. Índices são reconstruídos; não há duplicação persistente de cinco índices.

`generation_version` e `generation_config` ficam no World/save, incluindo configuração de geração, presença/nome do jogador. Seed sozinha não é tratada como garantia de reprodução entre versões de regras.

'''
    text+=f'''O save final temporário teve **{mb(c['save']['bytes'])}** e foi carregado com igualdade de todos os campos. SHA-256: `{c['save']['sha256']}`. Foi removido depois da verificação, preservando métricas, hashes e evidência compacta.

**Limite importante:** o JSON completo ainda é grande. A coleção nativa representa {mb(c['observability_bytes'])}, cerca de {100*c['observability_bytes']/c['save']['bytes']:.1f}% do JSON final; o restante inclui o estado do mundo, conhecimento e história já existentes. Não se está chamando 254 MB de save pequeno. Compressão/deduplicação futura deve preservar os registros relevantes, sem apagar causalidade para baixar o número.

O arquivo {link('reports/fase_5_5_5/historico_nativo.json.gz')} tem **{mb(c['historical_archive']['bytes'])}**, com história/observação e identificação mínima de personagens. **É evidência histórica, não um save completo carregável no jogo.** Não contém snapshots completos de Character.

## 9. Neutralidade OFF / NORMAL / AUDIT

Seed fixa: `{controls['neutrality']['seed']}`; **24 horas por modo**. Foram comparados todos os campos do World exceto a coleção privada `observability`, **incluindo metadados de Events**, geração/configuração, estado material, economia, relações, NPCs, métricas, IDs de gameplay e RNG.

Resultado: **igualdade exata nos três níveis**. Hash do estado comparado: `{controls['neutrality']['sha256']}`. OFF reteve {controls['neutrality']['off_decisions_retained']} traces; NORMAL reteve {controls['neutrality']['on_decisions_retained']}.

Não é uma prova matemática de toda campanha futura; é o controle solicitado, complementado pela separação de RNG/IDs e pelos testes de debug/consulta.

## 10. Continuidade e smoke

Seed `{controls['continuity']['seed']}`:

```text
Run A: 100h contínuas
Run B: 50h → serializar → carregar → 50h
```

**Todos os campos persistentes foram iguais**, incluindo RNG, história causal, recebimentos, traces e IDs produzidos depois do load. Próximos IDs: gameplay `{controls['continuity']['next_gameplay_id']}`, privado `{controls['continuity']['next_private_id']}`. Hash: `{controls['continuity']['sha256']}`.

Smoke posterior: `{controls['smoke']['seed']}`, **12h, quatro reinos, {controls['smoke']['npcs']} NPCs**, invariantes e auditoria geográfica válidas. Evidência: {link('reports/fase_5_5_5/controles.json')}.

## 11. Campanha natural final — regressão

Seed única nova: **`{c['seed']}`**. Quatro reinos, sem jogador, `historical_turns=0`, **300 horas**, sem busca de seeds ou aquecimento histórico. Os acontecimentos de geração/fundação em h0 não são horas simuladas anteriores.

'''
    text+=table(['Medida','Resultado'],[
        ('NPCs nomeados inicial/final',f"{c['initial_named']} / {c['final_named']}"),('População abstrata inicial/final',f"{c['initial_abstract']} / {c['final_abstract']}"),
        ('Vivos / mortos',f"{c['final_alive']} / {sum(c['death_causes'].values())}"),('Mortes por fome / sede / ambas / combate',f"{c['death_causes'].get('hunger',0)} / {c['death_causes'].get('thirst',0)} / {c['death_causes'].get('both',0)} / {c['death_causes'].get('combat',0)}"),
        ('Grupos criados / adesões',f"{m.get('NewGroupCreated',0)} / {m.get('GroupJoined',0)}"),('Propostas criadas / entregues',f"{m.get('ProposalCreated',0)} / {m.get('ProposalSubmitted',0)}"),
        ('Políticas criadas / concluídas',f"{m.get('PolicyCreated',0)} / {m.get('PolicyCompleted',0)}"),('Ataques / decisões letais / mortes em combate',f"{m.get('CharacterAttacked',0)} / {m.get('LethalDecision',0)} / {m.get('CharacterKilled',0)}"),
        ('Viagens iniciadas / chegadas',f"{m.get('JourneyStarted',0)} / {m.get('JourneyArrived',0)}"),('Adesões a facção / formalizações',f"{m.get('FactionJoined',0)} / {m.get('FactionFormalized',0)}"),
        ('Intervenções / audiências / apoteoses',f"{m.get('DivineIntervention',0)} / {m.get('DivineAudience',0)} / {m.get('Apotheosis',0)}"),('ReligiousDeclineReported natural',religious_reports),
        ('Eventos históricos / pais causais em links',f"{len(archive['events'])} / {c['causal_links']}"),('Checkpoints válidos',f"{len(c['checkpoints'])}, a cada 25h"),
        ('Exceções estruturais / reescrita do histórico','0 / 0'),('Tempo com observação nativa e verificações',f"{c['seconds']:.1f}s; inclui validação e exportação, não benchmark puro"),
    ])
    text+=f'''O saldo total passou de **{c['initial_money']} para {c['final_money']}**. A diferença **{c['explicit_money_source']}** é exatamente a fonte monetária já prevista `MoneySourceAbstractWork`. O residual foi **zero em todos os checkpoints**. A economia não é monetariamente fechada: trabalho abstrato emite moeda por regra existente. Transferências continuam debitando saldos; produção/consumo de água, alimento e materiais obedecem suas fontes/regras e aos testes materiais da suíte, não a uma hipótese de quantidade global fixa de comida.

Grupos/propostas/políticas, viagens, combate e religião continuaram operando. As quatro mortes em combate ocorreram naturalmente. Zero audiência, apoteose ou formalização não foi “corrigido” com novos thresholds. B08 possui prova controlada ponta a ponta; a quantidade natural de relatos acima não é usada para declarar que esse caminho foi exercitado quando não foi.

### Crescimento da observação

'''
    text+=table(['Hora','Traces importantes','Traces ordinários','Recebimentos permanentes','Anel de recebimentos'],[(r['hour'],r['important_decisions'],r['ordinary_decisions'],r['permanent_receipts'],r['recent_receipts']) for r in c['checkpoints']])
    text+=f'''Foram contabilizadas **{o.counters['decisions']} decisões** (NPCs e rotina coletiva). Retidas: **{len(o.decisions)} ({100*len(o.decisions)/o.counters['decisions']:.2f}%)**, sendo {sum(t.important for t in o.decisions.values())} importantes. Não se gravaram todos os cálculos dos NPCs para sempre. Dos {o.counters['learning_receipts']} recebimentos aceitos, {len(o.learning)} foram preservados como estruturais e {len(o.recent_learning)} ficaram no anel ordinário.

**Lacunas medidas:** {len(c['unavailable_parent_ids'])} IDs parentais únicos já não tinham payload no índice de runtime ao final. No conjunto persistente exportado, são {len(unavailable_persisted)}. São lacunas de payload nas referências; eventos efêmeros podem envelhecer fora da retenção. Não foi atribuída uma causa individual a cada lacuna nem convertido um Fact em evento verdadeiro inventado para preenchê-la. A V1 é uma fundação causal parcial, não um gravador integral de tudo. Um histórico importante com fontes disponíveis pode ser navegado; a ausência do payload é uma lacuna explícita.

O cache transitório de até 4.096 eventos pode ter mais eventos cotidianos que o buffer de 256 salvo. A reconstrução garante os índices da história/arquivo persistentes; não promete perpetuar todos os acertos desse cache.

Evidência completa: {link('reports/fase_5_5_5/campanha.json')} e {link('reports/fase_5_5_5/campanha.log')}.

## 12. Cadeia real completa da campanha

'''
    assert example
    ev=example['source_event'];lr=example['source_learning_receipt'];d=example['decision'];a=example['action_attempt'];result=example['result_event'];last=example['result_learning_receipt']
    text+=table(['Elo','Registro real'],[
        ('Source Event',f"#{ev['id']}, {ev['kind']}, h{ev['turn']}; ator {who(ev['actor_id'])} #{ev['actor_id']}, alvo #{ev['target_id']}"),
        ('Fact aprendido',f"{who(lr['receiver_id'])} #{lr['receiver_id']} recebeu o fato #{lr['event_id']} em h{lr['turn']}, canal {lr['channel']}, confiança {lr['confidence_before']}→{lr['confidence_after']}"),
        ('Need episode',f"{example['need_episode_id']}, {d['need_kind']}, prioridade {d['need_priority']}"),
        ('Decision',f"{d['id']}, ator {who(d['actor_id'])} #{d['actor_id']}, h{d['turn']}; selecionou {d['selected_action']}, score {d['selected_score']}"),
        ('Goal',f"#{example['goal_id']}"),('ActionAttempt',f"{a['id']}, {a['action']}, sucesso {a['success']}"),
        ('Result Event',f"#{result['id']}, {result['kind']}, h{result['turn']}; pais {result['parent_event_ids']}; decision_id={result['decision_id']}, action_attempt_id={result['action_attempt_id']}"),
        ('LearningReceipt do resultado',f"NPC #{last['receiver_id']} aprendeu #{last['event_id']} em h{last['turn']}, canal {last['channel']}, confiança {last['confidence_before']}→{last['confidence_after']}"),
    ])
    text+=f'''Ação e evento podem ter alvos semânticos diferentes: a necessidade responde a uma pessoa, enquanto a chegada descreve uma localidade. O relatório reproduz os IDs efetivos e não converte isso automaticamente em uma narrativa de perseguição bem-sucedida.

Dados completos desse caso, sem reexecutar a decisão: {link('reports/fase_5_5_5/cadeia_real.json')}.

## 13. Problemas e limites que permanecem

- **Sobrevivência domina as mortes:** {sum(c['death_causes'].get(k,0) for k in ('hunger','thirst','both'))}/{sum(c['death_causes'].values())} mortes por privação. Corrigir o atalho de água não resolveu capacidade econômica, deslocamento, competição de prioridades ou sustentabilidade global. Não se usou esta seed para rebalancear nada.
- Há propostas sem entrega e organizações sem formalização. Os caminhos não são garantidos por estar implementados; frequência e gargalos continuam para análise de coerência.
- O save JSON continua volumoso. Retenção ordinária é limitada, mas conhecimento, história e registros importantes crescem. Há espaço para compressão/deduplicação sem apagar a evidência estrutural.
- V1 não grava todos os gates internos de cada fornecedor, todos os desempates de RNG, todos os fatos cotidianos antigos nem a história completa de cada mudança de belief. Ausência é indicada, não preenchida por inferência.
- Identificadores de alvos ainda seguem os contratos dos sistemas existentes; tipos semânticos explícitos para todos eles e resolução genérica de entidades seriam melhorias da API de leitura futura.
- A confirmação natural não substitui testes controlados de eventos raros; estes resultados não autorizam alterar limiares para forçá-los.

## 14. Entrega à Fase 6.0 e evidências

B01–B08 estão corrigidos, a suíte ativa está verde, o legado relevante foi classificado, as regras duplicadas identificadas foram removidas/redirecionadas e a observação nativa passou pelos controles. O histórico não compartilha os payloads mutáveis que causavam B01.

Ficam explicitamente para a 6.0: coerência e balanceamento de sobrevivência, capacidade das capitais, oportunidades afetadas por LOD, fluxo crime→justiça, fragmentação de grupos, compatibilidade organizacional, delegação institucional, carreira, frequência de violência e religião. Nenhuma dessas perguntas foi resolvida mudando taxas nesta fase.

Arquivos principais:

- {link('reports/fase_5_5_5/testes_final.log','Suíte completa final')}
- {link('reports/fase_5_5_5/testes_antigos.json','21 falhas antigas classificadas')}
- {link('reports/fase_5_5_5/legado.json','Código legado')}
- {link('reports/fase_5_5_5/controles.json','Neutralidade, continuidade e smoke')}
- {link('reports/fase_5_5_5/campanha.json','Métricas da campanha')}
- {link('reports/fase_5_5_5/cadeia_real.json','Exemplo causal natural')}
- {link('reports/fase_5_5_5/historico_nativo.json.gz','História nativa compactada, sem save completo')}

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
'''
    (ROOT/'FASE_5_5_5.md').write_text(text)
    report_metrics={'suite_total':341,'new_tests':len(new_tests),'old_issues_classified':len(old),
        'all_sources_match_controls_and_campaign':True,'natural_hours':300,'complete_natural_chain':True,
        'religious_decline_reports':religious_reports,'unavailable_parent_ids_persisted':unavailable_persisted,
        'report_bytes':len(text.encode()),'report_sha256':hashlib.sha256(text.encode()).hexdigest()}
    (OUT/'relatorio_validacao.json').write_text(json.dumps(report_metrics,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report_metrics.items() if k!='unavailable_parent_ids_persisted'},ensure_ascii=False))

if __name__=='__main__':main()
