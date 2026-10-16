"""Relatório derivado de uma campanha já encerrada; nunca avança o mundo."""
import inspect
import itertools
import json
import re
import statistics
import textwrap
from collections import Counter, defaultdict, deque
from pathlib import Path

from .cohesion_audit import distribution
from procedural.persistence import loads
from procedural.institutions import Institutions
from procedural.society import SocietySystem
from procedural.utility import BASE as ACTION_BASE, WEIGHTS

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'reports/diagnostico_coesao'
ND='não disponível na baseline'

def read(name):return json.loads((OUT/name).read_text())
def cell(v):
    if v is None:return '—'
    if isinstance(v,float):return f'{v:.2f}'
    if isinstance(v,(dict,list,tuple)):v=json.dumps(v,ensure_ascii=False,separators=(',',':'))
    return str(v).replace('|',' / ').replace('\n',' ')
def dist(v):return cell(distribution(list(v)))
def pos(s):
    p=(s or {}).get('position') or {}
    return f"{p.get('map_id')}:{p.get('x')},{p.get('y')}"
def vital(s):
    if not s:return 'estado não retido'
    return f"{s['name']} #{s['id']}; HP {s['hp']:.1f}, fome {s['hunger']:.1f}, sede {s['thirst']:.1f}, fadiga {s['fatigue']:.1f}; moedas {s['money']}; comida/água {s['food']}/{s['water']}; posição {pos(s)}; Goal {s['goal']}/{s['goal_status']}"
def alt_rows(case):
    result=[]
    byid={str(n['id']):n for n in case.get('ordered_needs',[])}
    for nid,choices in case.get('evaluations',{}).items():
        for a in choices:result.append((byid.get(str(nid),{}).get('kind',nid),a['action'],a['score'],a.get('target'),a.get('terms')))
    return result
def path_steps(world,a,b):
    if not a or not b or a.get('map_id')!=b.get('map_id'):return None
    grid=world.maps.get(a['map_id'])
    if not grid:return None
    start=(a['x'],a['y']);end=(b['x'],b['y'])
    queue=deque([(start,0)]);seen={start}
    while queue:
        (x,y),n=queue.popleft()
        if (x,y)==end:return n
        for dx,dy in ((0,1),(0,-1),(1,0),(-1,0)):
            nx,ny=x+dx,y+dy
            if 0<=nx<grid.width and 0<=ny<grid.height and grid.rows[ny][nx]!='#' and (nx,ny) not in seen:
                seen.add((nx,ny));queue.append(((nx,ny),n+1))
    return None

def main():
    m,t,manifest=read('metrics.json'),read('traces.json'),read('manifesto.json')
    assert m['hours']==300
    save=OUT/'save_temporario.json'
    w=loads(save.read_text()) if save.exists() else None
    retained=read('analise.json') if (OUT/'analise.json').exists() else {}
    place_names={str(i):p.name for i,p in w.points.items()} if w else retained.get('place_names',{})
    hq_truth=retained.get('hq_truth',{})
    if w:
        for f in w.factions.values():
            place=w.points.get(f.headquarters_id) or w.towns.get(f.headquarters_id)
            if place:hq_truth[str(f.id)]={'place':place.id,'name':place.name,'food':sum(n for i,n in place.inventory.items() if w.items[i].kind=='food'),'water':sum(n for i,n in place.inventory.items() if w.items[i].kind=='water')}
    rejection_reasons=Counter(x.context.get('reason') for x in w.history if x.kind=='GroupJoinRejected') if w else Counter(retained.get('group_rejection_events',{}))
    distance_cache=retained.get('local_path_steps',{})
    def steps(s,destination):
        if not s:return None
        key=f"{s['id']}@{s['hour']}:{cell(s['position'])}->{cell(destination)}"
        if w:distance_cache[key]=path_steps(w,s['position'],destination)
        return distance_cache.get(key)
    events=t['events'];ev=defaultdict(list)
    for x in events:ev[x['kind']].append(x)
    count=lambda k:m['events'].get(k,0)
    town={x['id']:x for x in m['towns']}
    townname=lambda i:f"{town.get(i,{}).get('name',place_names.get(str(i),'local'))} #{i}"
    groups=m['groups'];allgroups={x['id']:x for x in m['retired_groups']+groups}
    proposals={p['id']:p for p in m['proposals']};policies={p['id']:p for p in m['policies']}
    deaths={x['state']['id']:x for x in t['deaths'] if x.get('record')}
    living_members=lambda g:set(g.get('final_members',g.get('members',[])))-set(deaths)
    def byproposal(kind):
        d=defaultdict(list)
        for x in ev[kind]:d[x['context'].get('proposal_id',x['target'])].append(x)
        return d
    def bypolicy(kind):
        d=defaultdict(list)
        for x in ev[kind]:d[x['context'].get('policy_id',x['target'])].append(x)
        return d
    support,delivery,submitted,decisions=[byproposal(k) for k in ('ProposalSupported','ProposalSupportDelivered','ProposalSubmitted','PolicyDecided')]
    work,effects,completion=[bypolicy(k) for k in ('PolicyEffect','PolicyEffect','PolicyCompleted')]
    joiners={j['person'] for g in allgroups.values() for j in g.get('joins',[])}
    active=[g for g in groups if g['status']=='active']
    buckets=defaultdict(list)
    for g in active:buckets[(g['town'],g['cause'],g['subject'])].append(g)
    overlaps=[];equivalent_members=defaultdict(set);pair_details=[]
    for key,gs in buckets.items():
        for g in gs:
            for p in living_members(g):equivalent_members[(p,key)].add(g['id'])
        for a,b in itertools.combinations(gs,2):
            aa,bb=living_members(a),living_members(b);union=aa|bb
            j=len(aa&bb)/len(union) if union else 0
            overlaps.append(j);pair_details.append({'a':a['id'],'b':b['id'],'shared':sorted(aa&bb),'jaccard':j})
    multi={p for (p,k),ids in equivalent_members.items() if len(ids)>1}
    group_people={p for g in active for p in living_members(g)}
    deprivation=[d for d in deaths.values() if d['record'].get('cause') in ('hunger','thirst','both')]
    def deathplace(d):
        loc=town.get(d['state']['position']['map_id'])
        return 'capital' if loc and loc['capital'] else loc['kind'] if loc else 'rota/mapa externo/POI'
    def dtime(d):return d['record'].get('turn',d['state']['hour'])
    lines=[]
    def p(s=''):
        if not s.startswith('```'):s=re.sub(r'\b(e|de|contra|observados|os|foram|foi|seção|seções|até|menos|conservaram|score|idade|sede|HP)(?=\d)',r'\1 ',s)
        lines.extend([s,''])
    def heading(s):p('## '+s)
    def table(headers,rows):
        p('| '+' | '.join(headers)+' |\n| '+' | '.join('---' for _ in headers)+' |\n'+'\n'.join('| '+' | '.join(cell(v) for v in row)+' |' for row in rows))
    def source(fn):p('```python\n'+textwrap.dedent(inspect.getsource(fn)).rstrip()+'\n```')
    def trace(case,label):
        p('### '+label)
        p(vital(case['state']))
        p('Personalidade na entrada: '+cell(case['state'].get('personality'))+'.')
        ns=case.get('ordered_needs',case['state'].get('needs',[]))
        table(['Need real na entrada','prioridade','status','alvo'],[(n['kind'],n['priority'],n.get('status'),n.get('target')) for n in ns[:8]])
        rows=alt_rows(case)
        if rows:table(['Need avaliada','alternativa','Utility','alvo','considerações normalizadas'],rows)
        else:p('Alternativas/scores não calculados ou não retidos nesse ponto; nenhum score foi reconstruído ficticiamente.')

    p('# Auditoria de coesão — Neravon-Coesao55')
    p(f"Campanha nova, natural, sem jogador, **{m['hours']}h**, regras **{m['rules']}**, geração **{m['generation']}**. Seed única **{m['seed']}**. O diagnóstico mede a versão entregue e não introduz rebalanceamento ou funcionalidades.")
    p('O gargalo principal é continuidade:47 propostas chegaram a16 submissões e três decisões; só uma política recebeu trabalho e nenhuma terminou. Nenhum grupo acumulou quatro reuniões, portanto a formalização nem chegou ao cálculo normal de pressão. Na sobrevivência,13 mortos de sede carregavam água e94 mortos tiveram repetição de fill_water após falha nos últimos rastros. As seções abaixo separam bloqueios corretos, bugs demonstrados e causas ainda não observáveis; não tratam ausência de evento raro como defeito.')
    heading('1. Proveniência, execução e limites da observação')
    c=manifest['campaign']
    table(['Item','Registro'],[
        ('Código SHA256',c['code_sha256']),('SHA256 depois',c['code_sha256_after']),
        ('Commit da referência anterior à limpeza',manifest.get('git_reference_commit',manifest.get('reference_commit','ver manifesto.json'))),
        ('População persistente inicial/final',f"{c['initial_named']} / {m['named_alive']}"),
        ('População abstrata inicial/final',f"{c['initial_abstract']} / {m['abstract']}"),
        ('Duração real de processamento (s)',c['runtime_seconds']),('Verificações estruturais',m['checks']),
        ('Erros de rota',c['route_errors']),('Erros do observador',m['observer_errors'])])
    p('Foi usado sys.setprofile externo para ler argumentos, variáveis locais e retornos efetivamente produzidos pelo motor, mais observação de eventos. Não houve substituição de funções de decisão, leitura global para alimentar NPCs, chamadas extras a soluções ou avanço auxiliar do mundo. Debug permaneceu desligado. O controle reduzido de8h produziu estado e RNG idênticos com e sem observador (manifesto.json, controlled_checks.observer_control). Esse controle não substitui uma comparação controlada de300h.')
    p('Houve dois reinícios com a mesma seed: uma falha do leitor ao receber return(None) durante propagação de exceção e, depois, o crash explícito da visita a POI na hora 26. Não foram reinícios por resultado. Após autorização do usuário, apenas Geography.emit teve o parâmetro kind renomeado para event_kind: duas linhas, preservando context["kind"], conteúdo e regras. O arquivo de patch e os registros de reprodução identificam a exceção. A campanha completa é a tentativa posterior; os prefixos interrompidos não entram nos totais.')
    p('28 testes selecionados passaram: suites Fase 5.5 e 5.4 e quatro regressões críticas de letalidade/alimentação. Não foi executada toda a suite histórica. O observador registra amostras iniciais de 48 criações, 80 chamadas de proposta e 40 trabalhos, mais decisões de adesão, decisões políticas e os três últimos registros de decisão de cada morto. Amostras iniciais têm viés temporal; não representam sorteio estatístico.')
    p('Unidades: chamadas, eventos, pares NPC–grupo, pessoas únicas e entidades persistentes são diferentes. GroupSearchAttempt limita emissão a 12h; recusas a 24h; ExistingGroupFound só em mudança do grupo escolhido. As contagens desses eventos não são probabilidades puras de conversão. Scores de grupos ao encerrar, calculados pelo auditor, são explicitamente identificados como derivados, não decisões tomadas pelo NPC. Campos pressure são o último cálculo do motor, não uma consulta recalculada ao final.')
    p('Evidências: metrics.json agrega estados e contadores; traces.json contém os rastros referenciados; manifesto.json contém hashes e retenção. Os três Markdown de Vaelora-55 foram preservados sem alteração. Não foi carregado o save antigo. O save temporário desta campanha serve apenas à conferência e é removido após a auditoria.')

    heading('2. Painel do encadeamento')
    table(['Etapa','Entidades ou eventos observados','Unidade'],[
        ('Necessidades coletivas distintas',m['unique_collective_needs'],'pares NPC/Need political_pressure'),
        ('Busca efetiva',m['calls'].get('search',0),'chamadas search_groups'),
        ('Busca publicada / grupo encontrado publicado',f"{count('GroupSearchAttempt')} / {count('ExistingGroupFound')}",'eventos limitados'),
        ('Adesão tentada / efetivada',f"{count('GroupJoinAttempt')} / {count('GroupJoined')}",'eventos'),
        ('Grupo criado / ativo ao fim',f"{count('NewGroupCreated')} / {len(active)}",'grupos'),
        ('Proposta criada / apoiada / apoio entregue / submetida',f"{count('ProposalCreated')} / {len(support)} / {len(delivery)} / {len(submitted)}",'propostas únicas'),
        ('Proposta decidida / vinculada a política',f"{len(decisions)} / {sum(p['policy_id'] is not None for p in proposals.values())}",'propostas únicas'),
        ('Política criada / trabalhada / concluída',f"{len(policies)} / {len(work)} / {len(completion)}",'políticas únicas'),
        ('Facção formalizada / aceita adesão',f"{count('FactionFormalized')} / {count('FactionMembershipAccepted')}",'eventos'),
        ('Mortos / privação',f"{len(deaths)} / {len(deprivation)}",'NPCs únicos')])
    table(['Need','chamadas de avaliação','com alternativa viável','seleções finais'],[(k,m['candidate_calls'].get(k,0),m['candidate_viable'].get(k,0),m['need_selected'].get(k,0)) for k in ('food','food_reserve','water','rest','recovery','political_pressure','organizational_survival','affiliation','governance','institutional_work','institutional_response')])
    p('A seleção é hierárquica: Needs são ordenadas por prioridade, e a primeira com alternativas viáveis vence; só então se comparam Utilities de suas alternativas. Continuação de Goal, interrupção alimentar e preparação preventiva podem modificar a escolha. Não há uma disputa única entre todos os scores de todas as Needs. Avaliações adicionais de Needs pessoais não equivalem a seleção.')
    p('Os contadores de avaliação usam o kind que realmente entrou em _evaluate; recovery pode delegar solutions a uma cópia da Need com kind rest/food/water. Assim, recovery pode ter mais seleções que avaliações marcadas recovery, sem incoerência do funil: parte de suas alternativas foi contada sob outro kind. Essas colunas não são uma coorte única de necessidades.')

    heading('3. Grupos: funil, fragmentação e conhecimento')
    a=m['affinity'];ad=a['distribution']
    table(['Métrica','Resultado'],[
        ('Avaliações que chegaram à afinidade',ad['n']),('Verificações compatíveis nessa etapa (afinidade ≥25)',ad['n']-a['low_attempts']),
        ('Verificações abaixo de 25',a['low_attempts']),('Pessoas com ao menos uma recusa por afinidade',a['rejected_people']),
        ('Pessoas cujas razões observadas foram apenas baixa afinidade',a['only_affinity_people']),
        ('Pares NPC–líder recusados / repetidos',f"{a['low_pairs']} / {a['repeated_pairs']}"),
        ('Eventos de recusa',count('GroupJoinRejected')),('Pessoas únicas com adesão',len(joiners)),
        ('Grupos criados',count('NewGroupCreated')),('Adesões por novo grupo',count('GroupJoined')/max(1,count('NewGroupCreated'))),
        ('Expedições criadas (outro caminho de Group)',count('ExpeditionFormed')),
        ('Tamanho final declarado de grupos ativos',dist(len(g['final_members']) for g in active)),
        ('NPCs em múltiplos grupos equivalentes',f"{len(multi)} / {len(group_people)} participantes ({100*len(multi)/max(1,len(group_people)):.2f}%)"),
        ('Jaccard médio de pares equivalentes ativos',statistics.mean(overlaps) if overlaps else None),
        ('Pares equivalentes com ao menos um membro comum',sum(bool(x['shared']) for x in pair_details))])
    table(['Motivo de GroupJoinRejected','Eventos históricos efetivos'],rejection_reasons.most_common())
    p('Equivalência diagnóstica = mesma localidade de origem, causa e subject_id. Não pressupõe que os NPCs conheçam esses outros grupos. Tamanho declarado pode conter mortos ainda não podados; vínculo ativo recíproco é mostrado separadamente. Um Jaccard pequeno significa composição diferente; não prova causas diferentes.')
    table(['Localidade','causa / subject','grupos ativos','tamanhos','idades (h)','reuniões','propostas distintas'],[(townname(key[0]),f'{key[1]} / {key[2]}',len(gs),[len(g['final_members']) for g in gs],[300-g['created_at'] for g in gs],sum(g['meetings'] for g in gs),len({p for g in gs for p in g['proposals']})) for key,gs in sorted(buckets.items(),key=lambda kv:(-len(kv[1]),kv[0][0],kv[0][1]))])
    heading('3.1 Por que organizar se já existe grupo?')
    p('collective_candidates primeiro pesquisa SOMENTE known_groups; se encontra um grupo aceito, retorna join_group e não oferece organize nesse ramo. Quando não encontra, pode oferecer share_problem e organize, com criação exigindo fato ProblemShared recente (≤72h), autor presente, afinidade com esse par ≥35 e capacidade de compromissos. form pesquisa novamente, impedindo criação se houver grupo conhecido aceito. Logo, várias criações não são uma escolha Utility(create)>Utility(join): join muitas vezes nem foi enumerado.')
    p('Fórmula base de Utility: base[action] + Σ(valor_normalizado × peso) − min(200, distância × UTILITY.distance_weight), seguida dos ajustes de GoalSystem._evaluate (alimentação, combate e pressão de ação quando aplicáveis). As considerações retidas são normalizadas por 200; multiplicar sua soma por 200 recompõe o score base, antes de outros ajustes. Need.priority não é adicionada a esse score.')
    table(['Alternativa','base','pesos reais'],[(k,ACTION_BASE[k],WEIGHTS.get(k,{})) for k in ('join_group','organize','share_problem','meet_group','submit_proposal','review_proposal')])
    cases=t['group_creation']
    chosen=[]
    for row in sorted(cases,key=lambda r:(-len(r.get('known_groups',[])),r['state']['hour'])):
        if len(chosen)>=6:break
        if row not in chosen:chosen.append(row)
    for row in chosen:
        trace(row,f"Criação real: grupo #{row['group']} na hora {row['state']['hour']}")
        p(f"Causa/subject: {row['cause']}/{row['subject']}; conhecidos antes: {[g['id'] for g in row['known_groups']]}; pesquisa interna retornou {row.get('search_found',[])}; verificações reais: {cell(row.get('group_checks',[]))}; resultado: novo grupo #{row['result']}.")
        if not any(x[1]=='join_group' for x in alt_rows(row)):p('Utility(join): não calculada nesse registro; não havia alternativa join_group avaliada. A existência global de grupos não concede conhecimento ao NPC.')
    heading('3.2 Afinidade social: fórmula e distribuição')
    source(SocietySystem.affinity)
    p('Aceite em acceptable_group exige ≥25; recrutamento dos pares da criação exige ≥35. Antes da afinidade existem gates de status/objetivo, grupo fechado/capacidade, três compromissos, líder vivo, confiança≥5, crença compatível, preferência de liderança após fracassos e rota. A variável cause é recebida mas não altera a fórmula. Confiança padrão é 10; amizade padrão 0. Apenas saber que o grupo existe ou observar um membro não concede bônus de familiaridade. Família pode influenciar relações no grafo, mas não recebe termo próprio aqui. Tamanho não altera afinidade; entre grupos aceitos, a pesquisa prefere maior composição e depois maior idade.')
    table(['Distribuição realmente calculada','Valores'],[('Todos os checks que alcançaram affinity',ad)])
    table(['hora','NPC','líder','confiança','amizade','compaixão','ambição','mesma profissão','score'],[(x['hour'],x['person'],x['leader'],x['trust'],x['friendship'],x['compassion'],x['ambition'],x['same_profession'],x['score']) for x in a['examples']])
    p('“Apenas afinidade” refere-se ao conjunto de motivos observados por pessoa durante a campanha, não à prova contrafactual de que ela ingressaria se o threshold fosse reduzido. Repetição foi medida por par NPC–líder com mais de uma avaliação recusada; nem toda reavaliação é uma tentativa presencial de adesão. Efeito indireto confirmado no código: afinidade abaixo do limiar retira join das alternativas e permite organização separada se outro par cumprir os gates.')

    heading('4. Churn, dissolução e vida social dos grupos')
    allrows=list(allgroups.values())
    removals=[(g,r) for g in allrows for r in g.get('removals',[])]
    table(['Métrica','Resultado'],[
        ('Eventos GroupJoined',count('GroupJoined')),('Remoções de membro observadas entre horas',len(removals)),
        ('Removido já morto / vivo',f"{sum(r['dead'] for g,r in removals)} / {sum(not r['dead'] for g,r in removals)}"),
        ('Pessoas únicas nos vínculos removidos',len({r['person'] for g,r in removals})),
        ('Dissoluções / fusões',f"{count('GroupDissolved')} / {count('GroupMerged')}"),
        ('Objetos retirados do mundo',len(m['retired_groups'])),
        ('Duração criada→dissolução ou encerramento',dist((g.get('dissolved_at') or 300)-g['created_at'] for g in allrows)),
        ('Sem atividade desde last_relevant, ativos',dist(300-g['last_relevant'] for g in active)),
        ('Reuniões acumuladas, ativos',dist(g['meetings'] for g in active)),
        ('Ativos sem proposta / sem reunião',f"{sum(not g['proposals'] for g in active)} / {sum(g['meetings']==0 for g in active)}")])
    p('O ledger compara conjuntos de membros a cada hora. Óbito e remoção não são eventos simultâneos: a manutenção periódica pode podar mais tarde. Uma adesão seguida de remoção dentro da mesma hora pode escapar à comparação. Dissolver remove vínculos no Character e pode manter a lista histórica no Group; esse estoque não equivale a associação ativa. Não há evento de saída voluntária separado nessa contagem. Tempo socialmente ativo é aproximação criada→dissolução, com last_relevant e reuniões; não uma leitura psicológica contínua.')
    table(['Grupo','local / causa','fundadores','joins','únicos fundadores+joins','removidos mortos/vivos','finais declarados / vivos','links nas pessoas / recíprocos vivos','status','reuniões','última atividade'],[(g['id'],f"{townname(g['town'])}/{g['cause']}",len(g.get('founders',[])),len(g.get('joins',[])),len(set(g.get('founders',[]))|{j['person'] for j in g.get('joins',[])}),f"{sum(r['dead'] for r in g.get('removals',[]))}/{sum(not r['dead'] for r in g.get('removals',[]))}",f"{len(g.get('final_members',g.get('members',[])))}/{len(living_members(g))}",f"{len(g.get('actor_links',[]))}/{len(set(g.get('actor_links',[]))&living_members(g)) if g['status']=='active' else 0}",g['status'],g['meetings'],g['last_relevant']) for g in sorted(allrows,key=lambda g:-len(g.get('joins',[])))[:12]])
    p('actor_links é a referência Character.group_ids, incluindo personagens mortos cujo vínculo histórico não foi apagado. Não é vínculo recíproco por si só. A última coluna de links vivos cruza pessoa viva, composição do grupo e status ativo. A fragmentação/sobreposição da seção3 usa apenas membros vivos; a distribuição de tamanho declarado permanece separada.')
    for g in sorted(allrows,key=lambda g:-(len(g.get('joins',[]))-len(g.get('final_members',g.get('members',[])))))[:3]:
        lost=g.get('removals',[])
        p(f"Grupo #{g['id']}: fundadores {g.get('founders',[])}; {len(g.get('joins',[]))} joins; remoções reais [hora,NPC,morto] {[(r['hour'],r['person'],r['dead']) for r in lost]}; dissolução {g.get('dissolved_at')} ({g.get('dissolution_reason')}); lista final {g.get('final_members',g.get('members',[]))}; vínculos {g.get('actor_links',[])}.")
    p('Vaelora registrou um grupo de Dormir com 25 adesões e cinco membros finais, mas seus três Markdown não preservam o ledger completo. Não é possível reconstruir honestamente cada saída daquela campanha. Os casos acima respondem à mesma pergunta nesta campanha com as remoções efetivamente observadas.')

    heading('5. Formalização: score, gates anteriores e ponto de parada')
    source(Institutions.formalization)
    p('No caminho da reunião, a função não é chamada para todo grupo a cada hora. Society.meeting exige líder e ≥2 presentes; atualiza investimento; dissolve se não houver problema compartilhado; só chama formalization após investimento≥4, idade≥168h, ≥3 membros registrados e ≥2 presentes com mais de 15 moedas. Formalization ainda exige ≥3 presentes, contribuição≥4 e score≥65. found_faction acrescenta líder/grupo ativos, capacidade global (<24 facções), limites de vínculos e contribuição real. Pressão alta isolada não aciona nada nesse caminho.')
    p('Há também um caminho legado: Access.candidates oferece formalize_organization ao líder com investimento≥4, idade≥168h e três membros registrados; Access.execute chama found_faction diretamente. Ele NÃO passa por Institutions.formalization e NÃO exige seu score65 nem três presentes. Portanto, o funil de score abaixo cobre a via de reunião, não todas as rotas possíveis de criação. A divergência foi reproduzida com score55 e dois presentes e está nos bugs confirmados, sem alteração comportamental.')
    meeting=m['meeting_gates'];formal=m['formalization_evaluations']
    table(['Etapa real','grupos únicos','chamadas'],[
        ('Criados',count('NewGroupCreated'),count('NewGroupCreated')),
        ('Reunião chamada',len({r['group'] for r in meeting}),len(meeting)),
        ('Passaram gates externos de formalização em reunião',len({r['group'] for r in meeting if r['success'] and r['status']=='active' and r['meetings']>=4 and r['age']>=168 and r['members']>=3 and r['rich_present']>=2}),sum(r['success'] and r['status']=='active' and r['meetings']>=4 and r['age']>=168 and r['members']>=3 and r['rich_present']>=2 for r in meeting)),
        ('Função formalization efetivamente chamada',len({r['group'] for r in formal}),len(formal)),
        ('Score ≥65 dentro da função',len({r['group'] for r in formal if r['score']>=65}),sum(r['score']>=65 for r in formal)),
        ('Ação legada formalize_organization: seleções / execuções / falhas','unidades não são grupos únicos',f"{m['action_selected'].get('formalize_organization',0)} / {m['action_executed'].get('formalize_organization',0)} / {m['action_failed'].get('formalize_organization',0)}"),
        ('Formalizados',count('FactionFormalized'),count('FactionFormalized'))])
    table(['Gate ausente na reunião (categorias sobrepostas)','chamadas'],[(name,sum(not test(r) for r in meeting)) for name,test in [('investimento≥4',lambda r:r['meetings']>=4),('idade≥168',lambda r:r['age']>=168),('membros≥3',lambda r:r['members']>=3),('ricos presentes≥2',lambda r:r['rich_present']>=2)]])
    ranked=sorted(active,key=lambda g:(-g['formalization_at_market']['score'],-g['meetings'],g['created_at']))[:10]
    table(['Grupo / causa','membros','idade','reuniões / fracassos','caixa grupo','pressão problema','presentes / contribuições','score derivado /65','líder HP/moedas/presente','gates ausentes'],[(f"{g['id']}/{g['cause']}",len(g['final_members']),300-g['created_at'],f"{g['meetings']}/{g['failures']}",g['money'],g['pressure'],f"{g['formalization_at_market']['present']}/{g['formalization_at_market']['funds']}",g['formalization_at_market']['score'],f"{g['leader_state']['hp']:.0f}/{g['leader_state']['money']}/{g['formalization_at_market']['gates']['leader_present']}",[k for k,v in g['formalization_at_market']['gates'].items() if not v]) for g in ranked])
    p('Top 10 = cálculo diagnóstico na posição do mercado na hora 300. Não é chamada histórica a formalization. O grupo não tem depósito de itens próprio no modelo; money é caixa do grupo, enquanto funds são moedas contribuíveis dos presentes acima de 15, limitadas a duas por pessoa. Problema persistente usa g.pressure/failures; comprovar necessidade individual de todos os ausentes nesse instante exigiria atualização extra e não foi feito.')
    p('O primeiro bloqueio natural confirmado foi investimento/reuniões: zero das86 chamadas chegou a quatro reuniões; os grupos ativos terminaram com no máximo duas. Isso bloqueou inclusive a ação legada. Em Society.candidates, líder com proposta pendente conhecida como draft retorna apenas submit_proposal antes de enumerar meet_group. Essa exclusividade ajuda a explicar a continuidade curta de reuniões enquanto há rascunho, sem provar cada hora de escolha dos líderes. Score derivado100 em dois grupos não atravessa esse gate.')
    if formal:table(['hora','grupo','score','idade','funds','presentes','execute','resultado'],[(r['hour'],r['group'],r['score'],r['age'],r['funds'],r['present'],r['execute'],r['result']) for r in formal[:15]])

    heading('6. Facções: visibilidade, contato e adesão')
    table(['Facção','conhecem existência total/vivos','conhecem HQ total/vivos','observaram membro','contato presencial ao longo da campanha','termos de benefícios / custos conhecidos','elegíveis básicos finais','convidados','status dos registros','membros finais'],[(f['name'],f"{len(f['knowers'])}/{len(set(f['knowers'])-set(deaths))}",f"{len(f['location_knowers'])}/{len(set(f['location_knowers'])-set(deaths))}",len(f['member_observation_people']),len(f['contact_people']),f"{sum(bool(r.get('terms',{}).get('benefits')) for r in f['invitations'].values())} / {sum(bool(r.get('terms',{}).get('costs')) for r in f['invitations'].values())}",len(f['basic_eligible']),len(f['invitations']),dict(Counter(r['status'] for r in f['invitations'].values())),len(f['members'])) for f in m['factions']])
    p('Conhecer HQ significa place_knowledge contém a sede; não garante saber rota até ela. Contato é co-presença lida em Access.refresh, e observar membro é possuir observação dessa pessoa; não são sinônimos de conversa bem-sucedida. Elegibilidade básica final = vivo, facção conhecida, sem organização e facção ativa; não garante Utility suficiente, equipamento ou capacidade de ingresso. Esses conjuntos em momentos diferentes não compõem uma única coorte monotônica. Benefícios/riscos conhecidos de fato foram contados pelos registros de terms, não atribuídos a todos os conhecedores.')
    samples=t['membership']
    invitations=[(f,pid,r) for f in m['factions'] for pid,r in f['invitations'].items()]
    table(['Etapa','Resultado','Unidade'],[
        ('Sabem que alguma facção existe',len({p for f in m['factions'] for p in f['knowers']}),'pessoas no encerramento'),
        ('Tiveram co-presença observada',len({p for f in m['factions'] for p in f['contact_people']}),'pessoas acumuladas'),
        ('Convidados publicados',count('FactionInvite'),'eventos'),('Solicitações espontâneas',count('FactionJoinRequest'),'eventos'),
        ('Registros de ingresso / com termos',f"{len(invitations)} / {sum(bool(r.get('terms')) for f,pid,r in invitations)}",'pares NPC–facção'),
        ('Avaliações de membership executadas',len(samples),'chamadas'),('Candidatos avaliados únicos',len({(r['state']['id'],r['faction']) for r in samples}),'pares NPC–facção'),
        ('Aceites / recusas / adiamentos / condições',f"{count('FactionMembershipAccepted')} / {count('FactionMembershipRejected')} / {count('FactionMembershipDeferred')} / {count('FactionMembershipConditioned')}",'eventos'),
        ('Aceites que continuam na lista final',sum(int(pid) in f['members'] for f,pid,r in invitations if r['status']=='accepted'),'NPC–facção'),
        ('Deserções publicadas',count('FactionDeserted'),'eventos')])
    accepted_dead=[(int(pid),deaths[int(pid)]['state']['name'],deaths[int(pid)]['record']['cause'],dtime(deaths[int(pid)])) for f,pid,r in invitations if r['status']=='accepted' and int(pid) in deaths]
    if accepted_dead:table(['Ingressante que morreu','nome','causa','hora'],accepted_dead)
    source(Institutions.membership_scores)
    p('A fórmula lê termos transmitidos pelo membro, fome/sede atuais, dinheiro pessoal, traços, fit calculado por Access e confiança no convidante. Não lê estoque mundial para oferecer vantagem onisciente. A autonomia declarada nos termos não tem parcela separada no cálculo; independência é o custo efetivo. Independência≥90 pode recusar mesmo com benefício maior. Fadiga≥85 ou HP<45 adiam antes da aceitação. Sem contato a decisão favorável permanece considering; termos ausentes impedem cálculo. Guardas/soldados sem arma sob risco≥0,6 podem condicionar ao equipamento. membership também bloqueia quem já possui qualquer organização.')
    for status,title in [('accepted','Aceites'),('rejected','Recusas')]:
        rows=[r for r in samples if (r.get('record_after') or {}).get('status')==status]
        dedup={}
        for r in rows:dedup.setdefault((r['state']['id'],r['faction']),r)
        p(f'### {title}: {min(5,len(dedup))} de {len(dedup)} pares disponíveis')
        for r in list(dedup.values())[:5]:
            trace(r,f"NPC #{r['state']['id']} / facção #{r['faction']} h{r['state']['hour']}")
            p(f"Registro real antes {cell(r.get('record_before'))}; depois {cell(r.get('record_after'))}; contatos {r['actual_contacts']}; retorno {cell(r['result'])}.")
    unanswered=[(f,pid,r) for f,pid,r in invitations if r['status'] in ('offered','considering','deferred','conditioned','delayed','conditional')]
    p(f'### Convites sem conclusão: {min(5,len(unanswered))} de {len(unanswered)} registros disponíveis')
    for f,pid,r in unanswered[:5]:
        s=f['invited_states'][pid]
        seen=[x for x in samples if x['state']['id']==int(pid) and x['faction']==f['id']]
        p(f"Facção {f['name']} #{f['id']}; registro {cell(r)}. Estado final: {vital(s)}. Avaliações efetivas retidas: {len(seen)}; relação/benefício/custo só existem se constarem no registro, nenhum score hipotético foi calculado.")
        table(['Need atual','prioridade','status','fonte'],[(n['kind'],n['priority'],n['status'],n['source']) for n in sorted(s['needs'],key=lambda n:-n['priority'])[:7]])

    heading('7. Capacidade material e ação institucional')
    table(['Facção','membros / profissões','moedas','itens reais','HQ','Capabilities finais no mapa do líder','ações enumeradas','execuções / falhas'],[(f['name'],f"{len(f['members'])} / {cell(f['professions'])}",f['money'],f['inventory'],townname(f['hq']),f['capabilities'],f['candidates_observed'],f"{cell(f['executions'])} / {cell(f['execution_failures'])}") for f in m['factions']])
    table(['Facção','ActionPressure final e fontes','regra/status local'],[(f['name'],f['pressure'],f['local_status']) for f in m['factions']])
    table(['Facção','Estoque real na sede, distinto do inventário Faction'],[(f['name'],hq_truth.get(str(f['id']),'não retido')) for f in m['factions']])
    p('As duas sedes conservaram12 comidas e24 águas no encerramento, enquanto os inventários das facções e seus caixas estavam zerados. Há capacidade material no lugar, mas institutional_supply enumera somente estoque de Faction; retirar itens do ponto exige presença/acesso pelas ações espaciais existentes. As capacidades finais acima pertencem ao mapa do líder e a seus membros abastecidos, não à riqueza de todo o mundo.')
    table(['Líder','grupos atuais','Need organizational_survival final e contexto','última ação bem-sucedida'],[(f['leader_state']['name'],f['leader_state']['groups'],[n for n in f['leader_state']['needs'] if n['kind']=='organizational_survival'],f['leader_state']['last_successful_action']) for f in m['factions']])
    p('Society.refresh reutiliza uma única Need organizational_survival: com grupo ativo, atualiza fonte/alvo e group_id para o primeiro grupo; no ramo elif organization_ids atribui contexto de facção. O ramo de grupo não apaga faction_id anterior. Os dois líderes terminaram com fonte de grupo e ambos os IDs no contexto. Society.candidates consulta faction_candidates antes do caminho coletivo; portanto esse contexto misto pode enumerar ações da facção sob uma Need descrita como participação no grupo. É mistura observada e localização causal no código, mas não se atribui a ela todo período de inatividade. Não há Need faccional independente garantida para cada vínculo. ActionPressure não substitui a enumeração/seleção.')
    p('Capabilities é predicado de meios atuais na localidade do avaliador: exige membros vivos, provisões carregadas e profissões específicas para vários serviços. Não é um contador de ações. invitation_info anuncia proteção, comida/água do estoque da facção e relatório de HQ, renda até quatro moedas, companhia e treinamento; renda anunciada não é promessa já paga nem salário automático. Capacidade de treinamento/produção/escolta não cria por si só handler natural equivalente. Estoque final não prova estoque no momento de cada convite; terms/reported_at é a evidência temporal do anúncio.')
    faction_actions=ev['FactionAction']
    table(['hora','facção','NPC','efeito material','ilegal'],[(x['hour'],x['context'].get('faction_id',x['target']),x['actor'],x['context'].get('effect',x['context']),x['context'].get('illegal')) for x in faction_actions[:30]])
    p('As ações institucionais acrescentadas oferecem apoio político, patrulha, compra, suprimento, roubo autorizado pelas normas e resposta à restrição. As contagens candidates_observed medem alternativas enumeradas por faction_candidates, antes da avaliação Utility; action_selected é seleção, action_executed é tentativa de execução, FactionAction é efeito bem-sucedido. Não são etapas intercambiáveis. O retorno antecipado de alternativas institucionais em Society.candidates pode impedir a enumeração das alternativas antigas report_to_faction/recruit_member/contribute nessa mesma chamada; isso é propriedade do código, não prova de que toda ausência de recrutamento tenha essa causa.')
    table(['Ação','seleções','tentativas de execução','retornos falhos'],[(a,m['action_selected'].get(a,0),m['action_executed'].get(a,0),m['action_failed'].get(a,0)) for a in ('invite_person','recruit_member','request_membership','answer_invitation','institutional_support','institutional_patrol','institutional_purchase','institutional_supply','institutional_raid','institutional_response','contribute','perform_assignment')])

    heading('8. Propostas: equivalência, apoio real e publicação')
    table(['Métrica','Resultado'],[
        ('Criadas / reutilizações',f"{count('ProposalCreated')} / {count('CompatibleProposalFound')}"),
        ('Status final',dict(Counter(p['status'] for p in proposals.values()))),
        ('Pessoas únicas apoiadoras / com apoio entregue',f"{len({i for p in proposals.values() for i in p['supporter_ids']})} / {len({i for p in proposals.values() for i in p['delivered_supporter_ids']})}"),
        ('Pares pessoa–proposta apoiados / entregues',f"{sum(len(p['supporter_ids']) for p in proposals.values())} / {sum(len(p['delivered_supporter_ids']) for p in proposals.values())}"),
        ('Grupos apoiadores distintos',len({i for p in proposals.values() for i in p['supporting_group_ids']})),
        ('Eventos de apoio / entrega / submissão',f"{count('ProposalSupported')} / {count('ProposalSupportDelivered')} / {count('ProposalSubmitted')}")])
    duplicate_rows=[]
    for a,b in itertools.combinations(proposals.values(),2):
        if (a['town_id'],a['sector'],a['desired_effect'],a['subject_id'])!=(b['town_id'],b['sector'],b['desired_effect'],b['subject_id']):continue
        older,newer=sorted([a,b],key=lambda x:x['created_at'])
        pol=policies.get(older['policy_id']);end=min((x['hour'] for x in completion.get(pol['id'],[])),default=301) if pol else 301
        if end<=newer['created_at'] or older['status']=='rejected' and older.get('decided_at',301)<=newer['created_at']:continue
        creation=next((r for r in t['proposal_creation'] if r.get('result')==newer['id'] and r['state']['hour']==newer['created_at']),None)
        known=older['id'] in creation['known_after'] if creation else None
        duplicate_rows.append({'older':older['id'],'newer':newer['id'],'town':townname(a['town_id']),'sector':a['sector'],'effect':a['desired_effect'],'subject':a['subject_id'],'known':known,'new_hour':newer['created_at']})
    table(['Antiga / nova','jurisdição','setor / efeito / subject','nova h','antiga conhecida na criação?'],[(f"{r['older']} / {r['newer']}",r['town'],f"{r['sector']} / {r['effect']} / {r['subject']}",r['new_hour'],r['known']) for r in duplicate_rows[:30]])
    p(f"Pares equivalentes que coexistiram sem conclusão/rejeição prévia conhecida: {len(duplicate_rows)}. O teste usa tempos de criação, decisões e conclusão observados; não chama propose novamente. Quando a amostra de criação mostra antiga ausente de known_after, o bloqueio de reutilização é conhecimento: o código somente reutiliza propostas conhecidas. Se a política antiga já acabou, uma nova proposta é um ciclo novo e foi excluída dessa contagem. Casos fora da amostra não permitem atribuir motivo individual exato. Rascunho não é automaticamente público: public_proposals só aprende a lista publicada no mercado, após submissão.")
    table(['Proposta','local / setor','criação','status','apoio / entregue','grupos','pública / recebida','política','última pressão'],[(p['id'],f"{townname(p['town_id'])}/{p['sector']}",p['created_at'],p['status'],f"{len(p['supporter_ids'])}/{len(p['delivered_supporter_ids'])}",p['supporting_group_ids'],f"{p['public']}/{p['in_received_office']}",p['policy_id'],p['pressure']) for p in sorted(proposals.values(),key=lambda p:(p['town_id'],p['created_at']))])

    heading('9. Funil político por entidades e tempos entre etapas')
    table(['Etapa','entidades únicas','eventos'],[
        ('ProposalCreated',count('ProposalCreated'),count('ProposalCreated')),('Support',len(support),count('ProposalSupported')),
        ('SupportDelivered',len(delivery),count('ProposalSupportDelivered')),('Submitted',len(submitted),count('ProposalSubmitted')),
        ('Decision',len(decisions),count('PolicyDecided')),('PolicyCreated',len(policies),count('PolicyCreated')),
        ('Work/Effect',len(effects),count('PolicyEffect')),('Completion',len(completion),count('PolicyCompleted'))])
    times=defaultdict(list)
    for pid,p0 in proposals.items():
        if support[pid]:times['criação → primeiro apoio'].append(min(e['hour'] for e in support[pid])-p0['created_at'])
        if delivery[pid]:times['criação → primeira entrega'].append(min(e['hour'] for e in delivery[pid])-p0['created_at'])
        if delivery[pid] and decisions[pid]:times['primeira entrega → primeira decisão'].append(min(e['hour'] for e in decisions[pid])-min(e['hour'] for e in delivery[pid]))
        if decisions[pid] and p0['policy_id'] in policies:times['primeira decisão → política vinculada'].append(policies[p0['policy_id']]['start_time']-min(e['hour'] for e in decisions[pid]))
    for pid,pol in policies.items():
        if work[pid]:times['política → primeiro trabalho'].append(min(e['hour'] for e in work[pid])-pol['start_time'])
        if completion[pid] and work[pid]:times['primeiro trabalho → conclusão'].append(min(e['hour'] for e in completion[pid])-min(e['hour'] for e in work[pid]))
    table(['Intervalo (h)','n','média','mediana','p90 (n≥10)','máximo'],[(k,d['n'],d.get('mean'),d.get('median'),d.get('p90') if d['n']>=10 else 'amostra pequena',d.get('max')) for k in ('criação → primeiro apoio','criação → primeira entrega','primeira entrega → primeira decisão','primeira decisão → política vinculada','política → primeiro trabalho','primeiro trabalho → conclusão') for d in [distribution(times[k])]])
    p('Apoio pode ser registrado no próprio propose, gerando intervalo zero legítimo. Essas distribuições incluem apenas etapas concluídas; rascunhos/políticas pendentes têm duração censurada na hora 300 e não foram convertidos em latências concluídas. Uma política pode ser reutilizada por mais de uma proposta; identificadores foram deduplicados no funil de políticas.')
    heading('9.1 Rascunhos e representantes')
    for q in sorted((p for p in proposals.values() if p['status']=='draft'),key=lambda p:p['created_at'])[:6]:
        r=q['representative'];may=q['mayor']
        distance=steps(r,town[q['town_id']]['market'])
        p(f"Proposta #{q['id']} ({townname(q['town_id'])}, {q['sector']}), criada h{q['created_at']}, idade {300-q['created_at']}h, apoio {q['support']}, entregue {len(q['delivered_supporter_ids'])}, recebida={q['in_received_office']}. Representante: {vital(r)}. Mercado: caminho local de {distance} passos (None = outro mapa/sem caminho/dado ausente, não prova de rota interlocal impossível). Prefeito: {vital(may)}.")
        if r:p(f"Needs atuais {cell(sorted(r['needs'],key=lambda n:-n['priority'])[:6])}; grupos {r['groups']}; compromissos {cell(r['commitments'])}; viagem {cell(r['journey'])}; última ação bem-sucedida {cell(r['last_successful_action'])}.")
    heading('9.2 Recebidas e ainda sem decisão conclusiva')
    pending=[p for p in proposals.values() if p['status'] in ('submitted','deferred','ignored')]
    for q in sorted(pending,key=lambda p:p['created_at'])[:6]:
        mayor=q['mayor'];r=q['representative']
        route_steps=steps(mayor,town[q['town_id']]['market'])
        p(f"Proposta #{q['id']}, {q['status']}, recebida={q['in_received_office']}, última pressão {q['pressure']:.2f}; prefeito: {vital(mayor)}; caminho local ao mercado {route_steps}; representante {r['id'] if r else 'ausente'}. Needs do prefeito {cell(sorted(mayor['needs'],key=lambda n:-n['priority'])[:6]) if mayor else 'ausente'}; viagem {cell(mayor['journey']) if mayor else '—'}; compromissos {cell(mayor['commitments']) if mayor else '—'}; última ação {cell(mayor['last_successful_action']) if mayor else '—'}.")
    p('Estados finais explicam indisponibilidade naquele instante; não bastam para provar cada hora de espera anterior. O código exige encontro entre líder de grupo apoiador e prefeito no mercado para submit; resolve exige prefeito no mercado e proposta recebida. Não existe decisão automática só porque a pressão chegou a 100.')

    heading('10. Pressão política e decisão da autoridade')
    source(Institutions.pressure)
    p('living conta somente apoiadores ENTREGUES e ainda vivos. affected_localities é armazenado, mas não acrescenta bônus numérico na fórmula. Severidade vem de urgency, que acumula o máximo registrado. A visibilidade é dois antes do recebimento e dez depois. Pressão não equivale a consentimento global e pode cair quando apoiadores morrem.')
    delivered_ids=set(x for x,rows in delivery.items() if rows)
    decided_ids=set(x for x,rows in decisions.items() if rows)
    table(['Conjunto','distribuição da última pressão armazenada'],[(name,dist(p['pressure'] for p in proposals.values() if test(p))) for name,test in [('Com apoio entregue',lambda p:p['id'] in delivered_ids),('Entregues e decididas',lambda p:p['id'] in delivered_ids&decided_ids),('Entregues e nunca decididas',lambda p:p['id'] in delivered_ids-decided_ids)]])
    p('São valores finais armazenados de propostas entregues, não necessariamente pressão no instante da primeira entrega. O rastreio de PoliticalPressureChanged só registra variações ≥2; não conserva todo cálculo intermediário. A distribuição de decisão abaixo usa valores efetivamente calculados no ato, sem essa ambiguidade.')
    source(Institutions.decision_scores)
    for r in t['political'][:10]:
        decision_event=next((x for x in decisions[r['proposal']] if x['hour']==r['hour']),None)
        result=decision_event['context'].get('result') if decision_event else 'não observado no evento dessa hora'
        p(f"Decisão calculada h{r['hour']}, proposta #{r['proposal']}: {vital(r['mayor'])}. Personalidade {cell(r['mayor']['personality'])}; crise/fatores {cell(r['pressure_state'])}; pressão {r['pressure']}; tesouro {r['town_money']}; cost={r['cost']}; avoid={r['avoid']}; scores {cell(r['scores'])}; máximo={max(r['scores'],key=r['scores'].get)}. Resultado do evento da mesma hora: {cell(result)}.")
    if not t['political']:p('Não houve chamada efetiva a decision_scores nesta campanha; portanto não existem cinco decisões reais para exemplificar e nenhum score hipotético foi criado.')
    p('approve/partial com orçamento insuficiente para create_policy viram defer na execução. Assim, máximo matemático e resultado material podem diferir por gate explícito; os rastros e o result persistido permitem distinguir.')

    heading('11. Política: conhecer, poder trabalhar, selecionar e produzir')
    table(['Política / setor','estado','conhecedores vivos observados (acumulado)','elegíveis conhecidos observados','trabalhadores efetivos','trabalho','orçamento/spent/refund/saldo','efeitos / barreiras'],[(f"{q['id']}/{q['sector']}",q['status'],m['policy_awareness'].get(str(q['id']),0),m['policy_eligible_aware'].get(str(q['id']),0),q['workers'],f"{q['work_done']}/{q['work_required']}",f"{q['budget']}/{q['spent']}/{q['refunded']}/{q['money']}",f"{cell(q['effects'])} / {cell(q['barriers'])}") for q in policies.values()])
    table(['Etapa','Resultado'],[
        ('Need institutional_work avaliada / viável / escolhida',f"{m['candidate_calls'].get('institutional_work',0)} / {m['candidate_viable'].get('institutional_work',0)} / {m['need_selected'].get('institutional_work',0)}"),
        ('policy_work selecionada / executada / falha',f"{m['action_selected'].get('policy_work',0)} / {m['action_executed'].get('policy_work',0)} / {m['action_failed'].get('policy_work',0)}"),
        ('Efeitos / conclusão / bloqueios publicados',f"{count('PolicyEffect')} / {count('PolicyCompleted')} / {count('PolicyBlocked')}"),
        ('Motivos de PolicyBlocked',dict(Counter(e['context'].get('reason') for e in ev['PolicyBlocked']))),
        ('Materiais efetivamente consumidos',dict(sum((Counter(e['context'].get('materials',{})) for e in ev['PolicyEffect']),Counter()))),
        ('Salários / reservado / devolvido',f"{sum(e['context'].get('wage',0) for e in ev['PolicyEffect'])} / {sum(p['budget'] for p in policies.values())} / {sum(p['refunded'] for p in policies.values())}")])
    p('Awareness é conjunto de pessoas que conheciam a política enquanto vivas em algum checkpoint; disponibilidade institucional observada exige worker_eligible realmente consultado e conhecimento presente. Não é um censo de todos os trabalhadores potenciais do mundo. Recursos são consumidos na execução; orçamento é reservado em create_policy; não há reserva prévia de madeira/ferro por simples aprovação. SECURITY financia observação/patrulha, sem produção física de água/comida. WATER consome madeira+ferro, aumenta capacidade a cada dois passos; não cria água diretamente. Ver os oito handlers e as profissões exatas em PROJECT.md.')
    p('Blockers reais: budget_exhausted, worker_unfit, missing_wood_or_iron, missing_grain_or_storage, missing_iron_or_wood, missing_known_route_or_cargo, transport_supplies_missing, physical_arrival_unconfirmed, cargo_lost e specialized_assignment_unavailable; RAW_MATERIAL propaga status do trabalho. Institutions.tick também registra no_effective_work depois de pelo menos48h sem trabalho e de idade da política; esse rótulo identifica ausência de execução, não a causa específica. Falta de conhecimento, prioridade ou caminho antes de policy_work pode impedir que haja PolicyBlocked. A ausência desse evento não prova disponibilidade material; um motivo não registrado é “não observável com instrumentação atual”.')
    for r in t['policy_work'][:3]:
        trace(r,f"Trabalho real da política #{r['policy']} h{r['state']['hour']}")
        p(f"Antes: {cell(r['policy_before'])}; retorno: {cell(r['result'])}.")

    heading('12. Mortalidade: causa, tempo e lugar')
    table(['Causa','Mortos'],sorted(m['deaths'].items()))
    table(['Recuperação/dano registrado no mundo','Valor / unidade'],[(key,m['world_metrics'].get(key,0)) for key in ('Recovery:Damage:hunger','Recovery:Damage:thirst','Recovery:Damage:both','Recovery:DeprivationHealed','Recovery:PhysicalHealed','Recovery:DeprivationFullyRecovered')])
    p('Houve298 mortes em1.898 persistentes iniciais (15,70%);297/298 foram por privação (99,66%). A recuperação existe e foi usada:11.159 pontos de dano de privação foram curados e houve500 registros de recuperação completa desse ledger, não500 pessoas únicas. Logo, o diagnóstico atual não é ausência absoluta de cura. O problema envolve manter acesso, consumo e recuperação antes de esgotar HP; os rastros seguintes comprovam falhas de continuidade em parte das mortes. Não há contrafactual que atribua todas as298 a um único gate.')
    table(['Bloco horário','hunger','thirst','both','combat','other','total'],[(f'{start+1}–{start+25}',*[sum(start<dtime(d)<=start+25 and d['record'].get('cause')==cause for d in deaths.values()) for cause in ('hunger','thirst','both','combat')],sum(start<dtime(d)<=start+25 and d['record'].get('cause') not in ('hunger','thirst','both','combat') for d in deaths.values()),sum(start<dtime(d)<=start+25 for d in deaths.values())) for start in range(0,300,25)])
    table(['Tipo de local da morte','Mortos'],Counter(deathplace(d) for d in deaths.values()).most_common())
    deathbytown=Counter(d['state']['position']['map_id'] for d in deaths.values())
    table(['Localidade','tipo','residentes vivos finais / abstratos','mortes no mapa','estoque comida/água/grão','water_daily/storage','tesouro','economia final'],[(townname(x['id']),'capital' if x['capital'] else x['kind'],f"{x['named_alive']}/{x['abstract']}",deathbytown[x['id']],f"{x['inventory']['food']}/{x['inventory']['water']}/{x['inventory']['grain']}",f"{x['infrastructure'].get('water_daily')}/{x['infrastructure'].get('water_storage')}",x['money'],x['economy']) for x in sorted(m['towns'],key=lambda x:-deathbytown[x['id']]) if deathbytown[x['id']] or x['capital']])
    p('Estoque e capacidade nessa tabela são do encerramento; estoque na morte está no rastro individual. Mortes foram localizadas por posição real, não residência. “Residentes vivos finais” conta o cadastro de residentes; viagens podem deslocar a presença física. water_daily/storage são limites de infraestrutura, não volume garantido entregue a cada NPC. economic_report conserva o último relatório econômico, não uma série diária inteira.')

    heading('12.1 Posse, conhecimento, dinheiro e alcance')
    table(['Condição ao chamar finish_death (privação)','Pessoas'],[
        ('Carregava comida',sum(d['state']['food']>0 for d in deprivation)),('Carregava água',sum(d['state']['water']>0 for d in deprivation)),
        ('Tinha moedas >0 / ≥2',f"{sum(d['state']['money']>0 for d in deprivation)} / {sum(d['state']['money']>=2 for d in deprivation)}"),
        ('Comida local >0 / água local >0',f"{sum((d['state']['local_food'] or 0)>0 for d in deprivation)} / {sum((d['state']['local_water'] or 0)>0 for d in deprivation)}"),
        ('Conhecia mercado / algum poço',f"{sum(bool(d['state']['known_market']) for d in deprivation)} / {sum(bool(d['state']['known_wells']) for d in deprivation)}"),
        ('Fome fatal e comida carregada',sum(d['record']['cause'] in ('hunger','both') and d['state']['food']>0 for d in deprivation)),
        ('Sede fatal e água carregada',sum(d['record']['cause'] in ('thirst','both') and d['state']['water']>0 for d in deprivation))])
    quoted=[d for d in deprivation if d['state']['market_observation'].get('price') is not None and d['state']['hour']-d['state']['market_observation'].get('price_turn',-1000)<=24 and d['state']['market_observation'].get('town_id')==d['state']['position']['map_id']]
    table(['Acesso econômico conhecido (privação)','Pessoas'],[
        ('Cotação de comida conhecida com até24h e mesmo mapa',len(quoted)),
        ('Desses: dinheiro suficiente para uma unidade ao preço conhecido',sum(d['state']['money']>=d['state']['market_observation']['price'] for d in quoted)),
        ('Desses: dinheiro insuficiente',sum(d['state']['money']<d['state']['market_observation']['price'] for d in quoted)),
        ('Demais: sem cotação recente local suficiente para concluir affordability',len(deprivation)-len(quoted))])
    p('Recurso local não equivale a recurso do NPC. Comida pode exigir compra, matéria-prima não é refeição e água do Town abastece mercado/poço sob regras distintas. Uma cotação conhecida antiga não prova preço atual. Dinheiro≥2 é faixa descritiva, não certificado de affordability. O motor aplica dano fisiológico antes da próxima decisão: estar com HP zero na entrada de finish_death não oferece uma rodada extra para comer. Ver fórmulas exatas de dano/recuperação em PROJECT.md.')
    lastneed=Counter();lastaction=Counter();lastgoal=Counter()
    access=[]
    for d in deprivation:
        s=d['state'];hist=d['last_decisions'];last=hist[-1] if hist else None
        lastneed[last['need'] if last else 'não observado']+=1;lastaction[last['action'] if last else 'não observado']+=1;lastgoal[s['goal']]+=1
        source=s['known_wells'][0] if s['known_wells'] else s.get('known_market')
        source_steps=steps(s,source)
        access.append({'person':s['id'],'hour':dtime(d),'cause':d['record']['cause'],'food':s['food'],'water':s['water'],'money':s['money'],'local_food':s['local_food'],'local_water':s['local_water'],'known_market':bool(s['known_market']),'known_well':bool(s['known_wells']),'steps_to_first_known_well_or_market':source_steps,'last_need':last['need'] if last else None,'last_action':last['action'] if last else None})
    table(['Último registro','Distribuição'],[('Need da última decisão real',dict(lastneed)),('Ação escolhida naquela decisão',dict(lastaction)),('Goal armazenado ao morrer',dict(lastgoal))])
    repeated_prep=[]
    for d in deprivation:
        for aa,bb in zip(d['last_decisions'],d['last_decisions'][1:]):
            if aa['action']==bb['action']=='fill_water' and aa.get('execution') and not aa['execution']['result'][0] and bb['hour']-aa['hour']<12:
                repeated_prep.append(d['state']['id']);break
    p(f"Achado específico: {len(repeated_prep)} mortos têm, dentro dos últimos três registros, fill_water escolhido novamente menos de12h depois de sua falha. O preparador cria uma Solution depois de _evaluate e não reaplica o filtro failures[action]>turn. No total, {lastaction['fill_water']} mortos terminaram com fill_water escolhido; {sum(d['record']['cause'] in ('thirst','both') and d['state']['water']>0 for d in deprivation)} morreram de sede/both com água carregada. No caso John Solaris #1245, h166/h167 falharam, h168 obteve duas águas com HP2 e sede100, e o fechamento h169 matou antes do consumo seguinte. Isso prova quebra de continuidade observada, não que corrigir somente esse ponto salvaria todos os mortos.")
    p('O caminho foi conferido por BFS somente leitura sobre o mapa, sem atualizar conhecimento ou chamar decisões. É distância física local a uma fonte conhecida (primeiro poço registrado ou mercado), não garantia de água remanescente, sobrevivência durante a caminhada, custo ou acesso em outra localidade. Necessidades institucionais foram mantidas com as prioridades originais.')
    examples=[]
    example_sets=([
        d for d in deprivation if (d['record']['cause'] in ('hunger','both') and d['state']['food']) or (d['record']['cause'] in ('thirst','both') and d['state']['water'])],
        sorted((d for d in deprivation if d['record']['cause'] in ('hunger','both')),key=lambda d:-(d['state']['local_food'] or 0)),
        sorted((d for d in deprivation if d['record']['cause'] in ('thirst','both')),key=lambda d:-(d['state']['local_water'] or 0)),
        sorted(deprivation,key=lambda d:-d['state']['money']),
        [d for d in deprivation if d['last_decisions'] and d['last_decisions'][-1]['need'] not in ('food','water','recovery','rest')],
        deprivation)
    for group in example_sets:
        added=0
        for d in group:
            if d not in examples:examples.append(d);added+=1
            if len(examples)>=8 or added>=2:break
        if len(examples)>=8:break
    for d in examples:
        s=d['state'];ar=next(a for a in access if a['person']==s['id'])
        p('### Morte #'+str(s['id'])+' — '+str(d['record']['cause'])+' h'+str(dtime(d)))
        p(vital(s))
        p(f"Primeira Need vital observada ≥50: {cell(d['first_vital'])}; conhecido mercado {cell(s['known_market'])}, poços {cell(s['known_wells'])}; observação econômica {cell(s['market_observation'])}; comida/água local {s['local_food']}/{s['local_water']}; passos à primeira fonte conhecida {ar['steps_to_first_known_well_or_market']}.")
        for r in d['last_decisions']:
            p(f"h{r['hour']}: Need {r['need']} prioridade {r['priority']:.2f}; escolhido {r['action']} score {r['score']:.2f}; estado após: {vital(r['state_after'])}; execução={r['executed']}, retorno={cell(r.get('execution',{}).get('result') if r.get('execution') else None)}.")
            table(['Alternativa realmente avaliada','score','alvo','termos','estimativa alimentar calculada'],[(z['action'],z['score'],z['target'],z.get('terms'),z.get('feeding')) for z in r['alternatives']])
        p('Registro causal do motor: '+cell(d['record'])+'. Não se conclui que o NPC poderia consumir estoque remoto apenas porque o Town tinha unidades.')
    heading('13. Competição de prioridade e dependências pessoais')
    competition=defaultdict(Counter)
    for key,n in m['institutional_competition'].items():
        origin,target=key.split(' -> ',1);competition[origin][target]+=n
    table(['Need que perdeu','episódios observados','principais vencedoras e estágio de avaliação'],[(kind,sum(competition[kind].values()),competition[kind].most_common(5)) for kind in ('political_pressure','organizational_survival','affiliation','governance','institutional_work','institutional_response')])
    table(['Need institucional → Need vencedora','ocorrências'],Counter(m['institutional_competition']).most_common(24))
    p('not_evaluated indica que a iteração normal parou antes desse Need; evaluated_but_not_selected significa que alguma avaliação foi observada, sem garantir que participou da competição final. O contador não substitui um replay completo de escolhas em todos os instantes. Não houve redução da prioridade da sobrevivência para produzir ação política.')
    table(['Processo','Dependência provada pelo código','Medida do efeito nesta campanha'],[
        ('Entrega e submissão de grupo','Institutions.deliver_support: p.id==g.leader_id; submit: líder de grupo apoiador + prefeito + mercado',f"{sum(p['status']=='draft' for p in proposals.values())} rascunhos; {sum(p['status']=='draft' and p['representative'] and not p['representative']['alive'] for p in proposals.values())} com representante final morto"),
        ('Decisão política','Institutions.resolve: t.mayor_id==p.id e mercado; Society.refresh cria governance só no prefeito',f"{len(pending)} pendentes recebidas/deferred/ignored; {sum(p['mayor'] and not p['mayor']['alive'] for p in pending)} com prefeito final morto"),
        ('Reunião e formalização','Society.meeting: líder presente e pares; found_faction mantém liderança',f"{sum(not g['leader_state']['alive'] for g in active)} grupos ativos com líder morto ao encerrar"),
        ('Compra institucional','Institutions.execute institutional_purchase: p.id==f.leader_id e mercado',f"{count('FactionAction')} efeitos institucionais totais; falhas por facção na seção 7"),
        ('Convite e admissão','Access.execute invite_person e membership exigem canal/membro presente; não necessariamente só líder para responder','não é um SPOF absoluto do líder: qualquer membro presente pode fornecer contato em membership'),
        ('Trabalho de política','Institutions.worker_eligible aceita profissões; policy_work exige trabalhador apto presente','não há trabalhador único obrigatório em WATER/FOOD/SECURITY; transporte guarda job por pessoa')])
    p('Indisponibilidade estrutural é demonstrada pelas condições; número exato de horas perdidas por cada pessoa indisponível não foi registrado continuamente. Não se atribuem todos os rascunhos ou esperas exclusivamente à morte do líder. Troca de prefeito preserva quadro recebido/publicado; não preserva automaticamente o ritmo de atendimento.')

    heading('14. Geografia e coesão')
    table(['Indicador','Resultado'],[('Localidades / reinos',f"{len(m['towns'])} / {len({x['kingdom'] for x in m['towns']})}"),('Rotas / travessias',f"{m['routes']['count']} / {m['routes']['traversals']}"),('JourneyStarted / Arrived',f"{count('JourneyStarted')} / {count('JourneyArrived')}"),('Auditoria de rotas',c['route_errors'])])
    p('Conhecer lugar e conhecer rota são registros diferentes. search_groups restringe inicialmente à cidade de residência; acceptable_group ainda pode exigir plano para quem está fora. Um grupo globalmente compatível não gera adesão remota. Proposal usa jurisdição determinada por Collective.authority; entrega e trabalho político exigem presença no mercado. Facções podem ter HQ em POI; suprimento exige depósito ou responsável presente, não teletransporte do estoque. Caminho local, viagem por rotas, preparação de provisões e encontro com autoridade são custos distintos. A campanha verifica que as rotas usadas são válidas, mas não registra uma decomposição causal exaustiva do tempo de viagem de cada cadeia institucional.')

    heading('15. Comparação com Vaelora-55')
    p('Fonte exclusiva da baseline: ../fase_5_5/RELATORIO_TECNICO.md, MUNDO.md e HISTORIAS_REAIS.md. Seeds e populações diferem. Além da correção autorizada do crash, Vaelora foi medida antes dos últimos ajustes 5.5 de contexto de ignore e preservação do quadro público citados no próprio relatório técnico anterior. Logo, são padrões repetidos/não repetidos e diferenças observadas, sem percentual causal atribuído à implementação.')
    maxsize=max((len(g['final_members']) for g in groups),default=0)
    table(['Métrica','Vaelora-55','Neravon-Coesao55'],[
        ('Horas',300,300),('Persistentes iniciais',1880,c['initial_named']),('Abstratos',4644,m['abstract']),('Persistentes vivos finais',1565,m['named_alive']),
        ('Mortos',315,len(deaths)),('hunger / thirst / both / combat','175 / 126 / 13 / 1',' / '.join(str(m['deaths'].get(k,0)) for k in ('hunger','thirst','both','combat'))),
        ('Grupos criados',132,count('NewGroupCreated')),('Ativos / dissolvidos','114 / 18',f"{len(active)} / {count('GroupDissolved')}"),('Adesões',998,count('GroupJoined')),('Pessoas únicas com adesão',555,len(joiners)),
        ('Maior grupo relatado (baseline) / maior lista final (nova)',24,maxsize),('Causas de criação','security:109; water:16; resource:7',dict(Counter(g['cause'] for g in allrows))),
        ('GroupSearchAttempt',5325,count('GroupSearchAttempt')),('ExistingGroupFound',1230,count('ExistingGroupFound')),('GroupJoinRejected',4273,count('GroupJoinRejected')),
        ('Low affinity eventos',3631,rejection_reasons.get('low_social_affinity',0)),
        ('Formalizações',0,count('FactionFormalized')),('Propostas criadas',46,count('ProposalCreated')),('Reutilizações',22,count('CompatibleProposalFound')),
        ('Eventos de apoio',261,count('ProposalSupported')),('Entregas de apoio',33,count('ProposalSupportDelivered')),('Submissões',16,count('ProposalSubmitted')),
        ('Decisões',2,count('PolicyDecided')),('Políticas',2,len(policies)),('Trabalhos com efeito',8,count('PolicyEffect')),('Políticas concluídas',2,count('PolicyCompleted')),
        ('Convites',19,count('FactionInvite')),('Pedidos espontâneos',0,count('FactionJoinRequest')),('Aceites / recusas','4 / 1',f"{count('FactionMembershipAccepted')} / {count('FactionMembershipRejected')}"),
        ('Membros finais das duas facções','3 / 3',[len(f['members']) for f in m['factions']]),('FactionAction',3,count('FactionAction')),('Status legal mudou',0,count('FactionLocalStatusChanged')),
        ('Viagens iniciadas / concluídas','76 / 64',f"{count('JourneyStarted')} / {count('JourneyArrived')}"),('Rotas / travessias','55 / 65',f"{m['routes']['count']} / {m['routes']['traversals']}"),
        ('Ataques',417,count('CharacterAttacked')),('Furtos',3190,count('ItemStolen')),('Estoque final comida/água','2045 / 6718',f"{sum(x['inventory']['food'] for x in m['towns'])} / {sum(x['inventory']['water'] for x in m['towns'])}"),
        ('Afinidade: distribuição de calls',ND,ad),('Pressões/latências distribuídas',ND,'seções9–10'),('Ledger exato de churn',ND,'seção4'),('Elegibilidade conhecida por política',ND,m['policy_eligible_aware'])])
    table(['Razão entre eventos (não taxa individual)','Vaelora','Nova'],[(name,old0/max(1,old1),count(n0)/max(1,count(n1))) for name,old0,old1,n0,n1 in [('found/search',1230,5325,'ExistingGroupFound','GroupSearchAttempt'),('joins/search',998,5325,'GroupJoined','GroupSearchAttempt'),('newgroups/search',132,5325,'NewGroupCreated','GroupSearchAttempt'),('reuses/creates',22,46,'CompatibleProposalFound','ProposalCreated'),('submitted/created',16,46,'ProposalSubmitted','ProposalCreated'),('decisions/submissions',2,16,'PolicyDecided','ProposalSubmitted'),('accepts/invites',4,19,'FactionMembershipAccepted','FactionInvite')]])
    p(f"As razões permitem comparar intensidade relativa de eventos sob os mesmos limites de emissão, não uma coorte individual. Uma proposta pode ser submetida ou decidida mais de uma vez. O maior grupo relatado em Vaelora foi24; o novo valor é lista final, sem série completa do pico de cada mutação. A mortalidade observada foi {len(deaths)} contra315, e {len(deprivation)}/{len(deaths)} mortes novas tiveram causa de privação. Isso descreve diferença entre campanhas, não efeito isolado de uma alteração. O padrão de predominância de privação deve ser avaliado junto das causas e dos rastros, não do estoque final agregado.")

    heading('16. GARGALOS CONFIRMADOS')
    table(['Sistema / sintoma','Evidência','Código','Efeito / confiança'],[
        ('Adesão a grupos','Checks abaixo do limiar e repetições na seção3','Society.affinity + Institutions.acceptable_group','Gate de afinidade retira join e permite alternativa separada; alta para gate, não contrafactual de balanceamento'),
        ('Formalização','Funil de reuniões/gates e top10 seção5','Society.meeting → Institutions.formalization','Score suficiente sozinho não basta; idade, co-presença e contribuições filtram antes; alta'),
        ('Propostas em espera','Rascunhos, entrega, recepção, representantes/prefeitos nas seções8–10','Institutions.submit/resolve + Society.candidates','Continuidade depende de presença e Need do representante/autoridade; alta para condições, parcial para horas de atraso'),
        ('Recrutamento','Termos, convites, chamadas e respostas seção6','Institutions.refresh/membership','Conhecimento/convite não equivale a decisão materializada; alta nos casos rastreados'),
        ('Execução institucional','Candidatos, tentativas e efeitos seção7','Institutions.faction_candidates/execute','Capacidade declarada pode ficar sem execução ou falhar em gate; alta onde retorno observado'),
        ('Sobrevivência','Mortes individuais com estoque local e últimos Goals seção12','GoalSystem.decide + alimentação/água/recuperação','Recursos agregados não garantem posse/consumo a tempo; alta para fatos, causas individuais detalhadas nos rastros')])
    p('Gargalo confirmado adicional de alta confiança: preparo hídrico. Houve94 mortos com repetição de fill_water depois de falha em intervalo menor que12h;13 morreram de sede carregando água. GoalSystem.preventive_choice cria o preparo depois do filtro de _evaluate. O efeito observado é gastar rodadas em fonte vazia ou adquirir sem consumir antes do fechamento; a fixture na seção19 comprova o desvio do bloqueio, sem estimar quantas mortes uma correção evitaria.')
    heading('17. HIPÓTESES')
    p('1. Consolidar contatos e confiança entre membros de grupos equivalentes poderia reduzir fragmentação; não foi feito experimento contrafactual e não há prova de limiar ideal. 2. Delegação de representação poderia aumentar entrega; não foi testada, pois alteraria gameplay. 3. Aumentar autonomia do trabalho institucional pode mudar execução, mas medir só oferta de capacidade não identifica impacto. 4. Uma campanha de 300h não caracteriza frequência estacionária de formalização, guerra, divindades ou colapso. 5. Estoque final positivo com mortes não prova o mesmo estoque, preço e acesso em todas as horas anteriores.')
    heading('18. COMPORTAMENTO CORRETO MAS INDESEJADO')
    p('Fragmentar por desconhecimento/baixa afinidade cumpre a epistemologia atual; pode produzir organizações redundantes no nível mundial. Recusar ou adiar ingresso por autonomia, risco, estado físico ou custo é decisão válida. Dar prioridade à sobrevivência e exigir recursos reais para política é correto, ainda que reduza ação institucional. Formalização rara sob várias condições simultâneas não é bug por ausência de evento. Dinheiro público/faccional não é renda pessoal do prefeito/membro; um cargo rico não sustenta automaticamente seu ocupante. O projeto precisa decidir futuramente quais desses resultados deseja mudar, preservando causalidade e limites materiais.')
    heading('19. BUGS CONFIRMADOS')
    p('**Crash em visita a POI — corrigido exclusivamente com autorização.** Geography.visit passava o nome do evento por posição e kind=point.kind como contexto, mas Geography.emit também chamava o primeiro parâmetro de kind. Resultado reproduzido: TypeError de argumento duplicado na hora26. Renomear o parâmetro para event_kind mantém o payload. A reprodução isolada e a passagem natural pela mesma hora validam a correção; o manifesto e patch preservam a alteração exata. Não foi mudada a versão conceitual.')
    def proof(filename,key):
        file=OUT/filename
        return json.loads(file.read_text()) if file.exists() else manifest.get('controlled_checks',{}).get(key)
    repro=proof('reproducao_suprimento.json','supply_reproduction')
    if repro:p('**Enumeração/execução de suprimento institucional — não corrigido.** '+cell(repro)+'. faction_candidates usa comida OU água para oferecer institutional_supply; execute escolhe somente o tipo da maior privação e exige esse tipo. Logo, um estoque de comida pode oferecer solução que vai falhar pedindo água. A reprodução é fixture isolada, não uma segunda campanha; sua frequência natural deve ser lida nos retornos falhos da seção7 e não inferida da fixture.')
    repro_form=proof('reproducao_formalizacao.json','formalization_reproduction')
    if repro_form:p('**Critérios de formalização divergentes — não corrigido.** '+cell(repro_form)+'. Access.execute(formalize_organization) chama Society.found_faction diretamente e contorna o gate de score≥65/presentes≥3 de Institutions.formalization. Na fixture de idade168 e quatro reuniões, a via nova recusou; a antiga aceitou score55 e dois fundadores. É inconsistência concreta entre caminhos da mesma funcionalidade; não prova frequência natural. A seção5 informa as seleções/execuções reais da ação legada.')
    repro_prep=proof('reproducao_preparo.json','preventive_reproduction')
    if repro_prep:p('**Preparo preventivo contorna bloqueio de ação falha — não corrigido.** '+cell(repro_prep)+'. GoalSystem._evaluate elimina fill_water durante o bloqueio de12h; preventive_choice o recria depois da avaliação, sem respeitar failures e sem verificar estoque da fonte. A fixture produziu zero alternativas pelo caminho normal, mas uma tentativa preventiva da mesma ação, que falhou por fonte vazia. Foram observados94 mortos com repetição desse padrão nos três últimos registros. Aquisição também é separada de beber: os13 mortos com água mostram que chegar a possuir recurso na última hora não assegura consumo antes do fechamento fisiológico.')
    p('Nenhum outro comportamento foi promovido a bug só por parecer pouco interessante. Falha do observador inicial foi corrigida no experimento externo; o tratamento registra erros e não encobre exceções do motor. Resultado sem dado suficiente fica nas hipóteses/lacunas.')
    heading('20. LACUNAS DE OBSERVABILIDADE')
    p('Faltam para cobertura exaustiva: retorno não-vazio de cada search e motivo individual de todos os gates; leituras/atualizações temporais completas de confiança; pico histórico de tamanho por grupo a cada mutação; exclusões voluntárias com identidade causal; pressão exata em toda entrega; último histórico de decisões de todo representante/prefeito vivo; distinção de candidatos descartados antes de _evaluate; preço/alcance/estoque de cada fonte conhecida a cada hora; horas de impedimento atribuídas exclusivamente a cada dependência; conhecimento individual explícito de todos os custos de facção. O perfil coleta apenas dados realmente existentes ou contadores de observação, sem preenchimento ficcional.')
    p('Os três últimos registros de cada morto permitem rastrear trechos finais, não reconstituir todas as 300h de Need→Goal→acesso→consumo por pessoa. O primeiro limiar vital≥50 não significa fome/sede contínua desde então. Eventos e contadores têm limites diferentes. Gates não alcançados não possuem Utility. As amostras de criação são iniciais, não aleatórias. Esses limites devem acompanhar qualquer conclusão futura baseada neste diagnóstico.')
    heading('21. Recomendações priorizadas — não implementadas')
    table(['Prioridade','Proposta de trabalho futuro','Por quê / como validar'],[
        ('P0','Manter regressão para o crash de POI e harmonizar assinatura/payload de eventos equivalentes','Evita interrupção estrutural; reprodução isolada já documentada, regras preservadas'),
        ('P0','Fazer preparo preventivo respeitar falhas e adequação fisiológica da ação','Há repetição natural de fill_water sem estoque apesar do bloqueio; consumo crítico precisa de continuidade verificável antes do próximo dano, sem criar água'),
        ('P1','Alinhar disponibilidade específica e localização de institutional_supply na enumeração e execução','Remove alternativa materialmente impossível; bug reproduzido isoladamente, sem falha natural dessa ação nesta seed'),
        ('P1','Unificar critérios entre a ação legada de formalização e a via de reunião','Evita critérios contraditórios; reproduzido isoladamente, sem formalização natural nesta seed'),
        ('P1','Instrumentar gates e retomadas com motivos por etapa e identidade de entidade','Separa conhecimento, prioridade, presença, dinheiro e material; medir funis por coorte antes de rebalancear'),
        ('P1','Rever continuidade de representação e atendimento quando titular está indisponível','Processos existentes dependem de indivíduos; avaliar delegação/sucessão com contato real, sem entrega automática'),
        ('P1','Estudar consolidação baseada em contato e objetivo compartilhado','Reduz duplicação artificial sem conceder conhecimento global ou forçar simpatia; comparar seeds controladas'),
        ('P1','Validar acesso individual a comida/água e previsão de margem fisiológica nos casos da seção12','Ataque causal às mortes, preservando moeda, estoque e prioridade vital; repetir casos identificados com novos testes curtos'),
        ('P2','Reavaliar gates conjuntos de formalização após observar mais coortes maduras','A ausência em300h não exige baixar thresholds; medir reuniões, renda e co-presença'),
        ('P2','Alinhar benefícios anunciados e serviços executáveis de facção','Distinguir capacidade, compromisso e entrega, sem fabricar ação para produzir lore'),
        ('P2','Revisar retenção de propostas ligadas a políticas concluídas','O limite24 com objetos protegidos é risco de longo prazo; não extrapolar para falha natural não observada')])
    p('Nenhuma recomendação comportamental foi aplicada. PROJECT.md descreve o código atual; LIMPEZA.md registra o corte de artefatos. Este relatório é diagnóstico, não nova fase, campanha de lore ou especificação já implementada.')
    (OUT/'RELATORIO_COESAO.md').write_text('\n'.join(lines),encoding='utf-8')
    derived={'group_overlap_pairs':pair_details,'proposal_equivalent_coexisting':duplicate_rows,'death_access':access,'timing':{k:distribution(v) for k,v in times.items()},'last_death_need':dict(lastneed),'last_death_action':dict(lastaction),'death_place_type':dict(Counter(deathplace(d) for d in deaths.values())),'group_rejection_events':dict(rejection_reasons),'local_path_steps':distance_cache,'place_names':place_names,'deaths_with_repeated_preventive_fill':repeated_prep,'hq_truth':hq_truth}
    (OUT/'analise.json').write_text(json.dumps(derived,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'report_lines':len(lines),'groups':len(groups),'proposals':len(proposals),'deaths':len(deaths),'overlap_pairs':len(pair_details),'duplicate_proposal_pairs':len(duplicate_rows)},ensure_ascii=False))

if __name__=='__main__':main()
