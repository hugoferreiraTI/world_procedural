"""Extrai relatórios e evidência selecionada; não executa a simulação."""
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path

BASE=Path(__file__).resolve().parents[1]
OUT=BASE/'reports/fase_5_5'
DATA=OUT/'campanha_300h'

def table(headers,rows):
    return '\n'.join(['| '+' | '.join(headers)+' |','| '+' | '.join(['---']*len(headers))+' |']+
                     ['| '+' | '.join(str(v).replace('|','/') for v in row)+' |' for row in rows])+'\n\n'

def compact(counter):
    return ', '.join(f'{k}: {v}' for k,v in sorted(counter.items())) or 'nenhum'

def main():
    r=json.loads((DATA/'resumo.json').read_text())
    events=json.loads((DATA/'eventos_para_selecao.json').read_text())
    assert r['completed_hours']==300 and not r['route_errors'] and all(not x['errors'] for x in r['checks'])
    bykind=defaultdict(list)
    for e in events:bykind[e['kind']].append(e)
    selected={};stories=[]
    chars=r['characters'];towns={t['id']:t for t in r['towns']};groups={g['id']:g for g in r['groups']}
    props={p['id']:p for p in r['proposals']};policies={p['id']:p for p in r['policies']};factions={f['id']:f for f in r['factions']}
    places={**{i:t['name'] for i,t in towns.items()},**{p['id']:p['name'] for p in r['points']}}
    labels={'security':'segurança','water_access':'água','resource_pressure':'sustento','criminal_cooperation':'cooperação criminosa',
            'religious_interest':'fé','active':'ativo','faction':'formalizado','dissolved':'dissolvido','completed':'concluída',
            'stalled':'paralisada','accepted':'aceita','partial':'aprovação parcial','submitted':'entregue','draft':'rascunho',
            'deferred':'adiada','ignored':'ignorada','rejected':'recusada','hunters':'caçadores','mercenaries':'mercenários','justice':'justiça'}
    def label(x):return labels.get(x,x)
    def person(id):
        if id is None:return 'cargo vago'
        p=chars.get(str(id));return f"{p['name']} (#{id})"+(' †' if not p['alive'] else '') if p else f'NPC #{id}'
    def place(id):return f'{places.get(id,"Localidade")} (#{id})'
    def group(id):return f"{groups[id]['name']} (#{id})" if id in groups else f'Grupo #{id}'
    def ref(es):
        for e in es:selected[e['id']]=e
        return 'Registros: '+ '; '.join(f"{e['kind']} #{e['id']} — h{e['turn']}" for e in es)+'.'
    def story(title,text,es):
        if not es:return
        stories.append(f'## {len(stories)+1}. {title}\n\n{text}\n\n{ref(es)}\n')
    def match(kind,key,id):return [e for e in bykind[kind] if e['context'].get(key,e['target_id'])==id]

    # Seleção de cadeias reais, sem fabricar finais nem transformar fixtures em lore.
    joins=Counter(e['target_id'] for e in bykind['GroupJoined'])
    if joins:
        gid=joins.most_common(1)[0][0];joined=match('GroupJoined','group_id',gid)
        created=match('NewGroupCreated','group_id',gid)
        found=[e for e in bykind['ExistingGroupFound'] if e['target_id']==gid and e['actor_id']==joined[0]['actor_id']]
        g=groups.get(gid);size=len(g['member_ids']) if g else 'não conservado no registro final'
        text=f"{group(gid)} recebeu {len(joined)} adesões durante a campanha. {person(joined[0]['actor_id'])} entrou na hora {joined[0]['turn']} por contato com um participante: {person(joined[0]['context']['contact'])}."
        if found:text+=' O encontro de um grupo compatível conhecido aparece antes da adesão selecionada.'
        if created:text+=f" O registro de criação traz {len(created[0]['context']['members'])} fundadores."
        text+=f' No encerramento, o número de membros registrados era {size}. Adesões sucessivas deram continuidade à organização existente.'
        story('Uma organização recebe novos participantes',text,created[:1]+found[:1]+[joined[0],joined[-1]])
    shared=[p for p in r['proposals'] if len(p['supporting_group_ids'])>1]
    if shared:
        p=max(shared,key=lambda x:(len(x['supporting_group_ids']),x['support']));pid=p['id']
        es=match('ProposalCreated','proposal_id',pid)[:1]+match('CompatibleProposalFound','proposal_id',pid)[:2]+match('ProposalSupported','proposal_id',pid)[-2:]+match('ProposalSupportDelivered','proposal_id',pid)[-1:]
        text=f"A proposta #{pid}, setor {p['sector']}, concentrou apoio de {len(p['supporting_group_ids'])} grupos: "+'; '.join(group(i) for i in p['supporting_group_ids'])+'. '
        text+=f"Seu registro final possui {p['support']} pessoas únicas; {len(p['delivered_supporter_ids'])} apoios chegaram à administração. Encontrar uma proposta compatível permitiu apoiar a iniciativa existente. Estado final: {label(p['status'])}."
        story('Vários grupos apoiam a mesma proposta',text,es)
    decisions=bykind['PolicyDecided']
    if decisions:
        event=max(decisions,key=lambda e:e['context']['result'].get('political_pressure',0));pid=event['context']['proposal_id'];result=event['context']['result']
        es=match('ProposalSubmitted','proposal_id',pid)[-1:]+[event]+match('PolicyCreated','proposal_id',pid)[:1]
        scores=result.get('scores',{})
        text=f"{person(event['actor_id'])} decidiu a proposta #{pid}, em {place(event['location']['map_id'])}, na hora {event['turn']}. A pressão registrada era {result['political_pressure']:.1f}; a decisão foi {label(result['decision'])}. "
        text+='A avaliação registrada combinou pressão, personalidade e orçamento: '+compact({k:round(v,1) for k,v in scores.items()})+'. '
        if result.get('policy_id'):text+=f"A resposta criou ou vinculou a política #{result['policy_id']}; a execução material é uma etapa posterior."
        else:text+='Essa resposta não criou política material.'
        text+=' O registro não permite afirmar que o prefeito mudaria de opinião em um cenário hipotético sem pressão.'
        story('A administração recebe pressão e decide',text,es)
    effects=bykind['PolicyEffect']
    if effects:
        candidates=[e for e in effects if 'capacity_after' in e['context']['effect']]
        event=candidates[-1] if candidates else effects[0];pid=event['context']['policy_id'];p=policies[pid]
        pe=match('PolicyEffect','policy_id',pid);es=match('PolicyCreated','policy_id',pid)[:1]+pe[:2]+([event] if event not in pe[:2] else [])+match('PolicyCompleted','policy_id',pid)[:1]
        material=Counter()
        for e in pe:material.update(e['context'].get('materials',{}))
        text=f"A política #{pid}, setor {p['sector']}, em {place(p['jurisdiction'])}, financiou {len(pe)} etapas de trabalho, com {len(p['workers'])} trabalhadores registrados. Foram pagos {p['spent']} em salários do orçamento reservado; materiais consumidos: {compact(material)}. "
        if candidates:
            text+=f"Uma etapa elevou a capacidade diária de {event['context']['effect']['capacity_before']} para {event['context']['effect']['capacity_after']} unidades. A obra não criou água instantaneamente; a coleta diária existente passou a poder usar a nova capacidade. "
        else:text+='O efeito registrado na etapa selecionada foi '+json.dumps(event['context']['effect'],ensure_ascii=False)+'. '
        text+=f"Estado ao final: {label(p['status'])}. Isso comprova execução, sem provar que toda escassez local acabou."
        story('Uma aprovação passa à execução',text,es)
    blocked=bykind['PolicyBlocked']
    if blocked:
        unresolved=[e for e in blocked if policies[e['context']['policy_id']]['status']=='stalled']
        event=unresolved[-1] if unresolved else blocked[0];pid=event['context']['policy_id'];p=policies[pid]
        es=match('PolicyCreated','policy_id',pid)[:1]+[event]+match('PolicyEffect','policy_id',pid)[-1:]
        text=f"A política #{pid}, setor {p['sector']}, em {place(p['jurisdiction'])}, encontrou a barreira registrada `{event['context']['reason']}` na hora {event['turn']}. "
        text+=f"No final, constavam {p['work_done']} de {p['work_required']} etapas, {p['money']} de orçamento ainda reservado e estado {label(p['status'])}. "
        text+='A aprovação institucional não garantiu o trabalho. Esse registro não identifica sozinho qual necessidade concorrente venceu para cada trabalhador ausente.'
        complete=match('PolicyCompleted','policy_id',pid)[:1]
        story('Uma política encontra limites' if p['status']!='completed' else 'Um trabalho demora, mas depois é concluído',text,es+complete)
    formal=bykind['FactionFormalized']
    if formal:
        ev=formal[0];fid=ev['target_id'];gid=ev['context']['origin_group_id'];f=factions.get(fid)
        es=match('NewGroupCreated','group_id',gid)[:1]+match('GroupMeeting','group_id',gid)[-2:]+[ev]
        text=f"{group(gid)} formalizou a facção #{fid} na hora {ev['turn']}. Os fundadores registrados foram "+', '.join(person(i) for i in ev['context']['founders'])+'. '
        text+='A avaliação conservada na formalização foi '+json.dumps(ev['context'].get('factors',{}),ensure_ascii=False)+'. '
        if f:text+=f"A organização terminou com {len(f['member_ids'])} membros e {f['money']} em caixa."
        story('Um grupo desenvolve continuidade institucional',text,es)
    accepts=bykind['FactionMembershipAccepted']
    if accepts:
        ev=accepts[0];fid=ev['target_id'];id=ev['actor_id'];f=factions[fid]
        prior=[e for e in bykind['FactionInvite'] if e['target_id']==fid and e['context'].get('candidate')==id]
        prior+= [e for e in bykind['FactionJoinRequest']+bykind['FactionMembershipDeferred']+bykind['FactionMembershipConditioned'] if e['actor_id']==id and e['target_id']==fid and e['turn']<=ev['turn']]
        score=ev['context']['evaluation']
        text=f"{person(id)} entrou em {f['name']} (#{fid}) na hora {ev['turn']}, em contato com {person(ev['context']['contact'])}. O benefício percebido registrado foi {score['perceived_benefit']}, contra custo {score['perceived_cost']}. "
        text+='A adesão teve avaliação individual e contato físico. O ingresso não comprova recebimento automático de salário, comida, treinamento ou equipamento; essas entregas dependem de ações e recursos posteriores.'
        story('Uma pessoa aceita a organização',text,sorted(prior,key=lambda x:x['turn'])[:3]+[ev])
    actions=bykind['FactionAction']
    if actions and len(stories)<9:
        ev=next((e for e in actions if e['context']['action']=='institutional_patrol'),actions[0]);fid=ev['target_id'];f=factions[fid]
        preceding=[e for e in actions if e['target_id']==fid and e['turn']<=ev['turn'] and e['context']['action']=='institutional_purchase'][-1:]
        law=[e for e in bykind['FactionLocalStatusChanged'] if e['target_id']==fid and e['context'].get('source_fact')==ev['id']]
        text=f"{person(ev['actor_id'])}, membro de {f['name']} (#{fid}), executou `{ev['context']['action']}` em {place(ev['location']['map_id'])}, na hora {ev['turn']}. O resultado registrado foi "+json.dumps(ev['context']['effect'],ensure_ascii=False)+'. '
        text+=f"A ação foi classificada como {'ilegal' if ev['context']['illegal'] else 'legal'} no evento. "
        if law:text+=f"Uma autoridade que recebeu o fato mudou o estado local para {law[0]['context']['status']}. "
        else:text+='Não há mudança legal ligada a esse evento na evidência selecionada. '
        text+='A capacidade veio dos membros e mantimentos presentes; a execução não exigiu uma proposta aprovada pelo prefeito.'
        story('A facção age com capacidade própria',text,preceding+[ev]+law[:1])
    deferred=bykind['FactionMembershipDeferred']
    if deferred and len(stories)<9:
        accepted_pairs={(e['actor_id'],e['target_id']) for e in accepts}
        ev=next((e for e in deferred if (e['actor_id'],e['target_id']) not in accepted_pairs),deferred[0])
        later=[e for kind in ('FactionMembershipAccepted','FactionMembershipRejected','FactionMembershipConditioned') for e in bykind[kind]
               if e['actor_id']==ev['actor_id'] and e['target_id']==ev['target_id'] and e['turn']>=ev['turn']]
        text=f"{person(ev['actor_id'])} adiou a decisão sobre a facção #{ev['target_id']} na hora {ev['turn']}, por `{ev['context']['reason']}`. "
        if later:text+=f"O próximo desfecho registrado foi {later[0]['kind']} na hora {later[0]['turn']}."
        else:text+='A cadeia selecionada termina aberta: o adiamento não deve ser narrado como ingresso ou recusa.'
        story('Uma condição interrompe a adesão',text,[ev]+later[:1])
    assert 6<=len(stories)<=10, f'Número de cadeias reais insuficiente: {len(stories)}'
    hist='# HISTÓRIAS REAIS — Vaelora-55\n\n'
    hist+='Campanha natural nova, sem jogador, 300 horas. Estes episódios vêm da execução concluída, após a correção da interrupção estrutural da hora 50. Testes controlados não fazem parte desta lore. † identifica personagens mortos no encerramento, sem presumir quando ou como morreram.\n\n'
    hist+='\n'.join(stories)+'\nEvidência selecionada: [eventos_relevantes.json](campanha_300h/eventos_relevantes.json).\n'

    ec=r['events'];initial=r['initial'];death_total=sum(r['deaths'].values())
    counter=lambda key:ec.get(key,0)
    gs=Counter(g['cause'] for g in r['groups']);ps=Counter(p['sector'] for p in r['policies'])
    propstates=Counter(p['status'] for p in r['proposals']);decstates=Counter(e['context']['result']['decision'] for e in decisions)
    materials=Counter()
    for e in effects:materials.update(e['context'].get('materials',{}))
    invstates=Counter(row['status'] for f in r['factions'] for row in f['norms'].get('invitations',{}).values())
    max_group=max((len(g['member_ids']) for g in r['groups']),default=0)
    water_towns=[t for t in r['towns'] if t['infrastructure']['water_daily']>80]
    metrics={'seed':r['seed'],'hours':300,'restarts':r['restarts'],'initial':initial,'final_named':r['final_named'],
             'final_abstract':r['final_abstract'],'deaths':r['deaths'],'events':ec,'final_group_causes':dict(gs),
             'largest_group':max_group,'final_proposal_states':dict(propstates),'decisions':dict(decstates),
             'policy_sectors':dict(ps),'policy_states':dict(Counter(p['status'] for p in r['policies'])),
             'policy_materials_consumed':dict(materials),'policy_wages':sum(p['spent'] for p in r['policies']),
             'group_join_counts':dict(joins),'people_joined_count':len({e['actor_id'] for e in bykind['GroupJoined']}),
             'group_rejection_reasons':dict(Counter(e['context']['reason'] for e in bykind['GroupJoinRejected'])),
             'invitation_states_retained':dict(invstates),'water_localities_expanded':len(water_towns),
             'selected_story_count':len(stories),'selected_event_count':len(selected),'checks':r['checks'],'route_errors':r['route_errors']}

    mundo=f"# MUNDO — {r['seed']}\n\n300 horas naturais, sem jogador; versão `{r['rules']}`. Catálogo compacto do estado final e dos acontecimentos contados.\n\n"
    mundo+=f"A população começou com **{initial['named']} pessoas persistentes e {initial['abstract']} abstratas** ({initial['named']+initial['abstract']} habitantes). Terminou com **{r['final_named']} persistentes vivos e {r['final_abstract']} abstratos** ({r['final_named']+r['final_abstract']}). Houve {death_total} mortes registradas: {compact(r['deaths'])}.\n\n"
    mundo+='## Reinos e localidades\n\n'
    mundo+=table(['Reino','Capital','Cidades / vilas','Persistentes vivos / abstratos','Governante'],[
        [k['name'],place(k['capital_id']),f"{sum(t['kind']=='cidade' for t in r['towns'] if t['kingdom_id']==k['id'])} / {sum(t['kind']=='vila' for t in r['towns'] if t['kingdom_id']==k['id'])}",
         f"{sum(t['named'] for t in r['towns'] if t['kingdom_id']==k['id'])} / {sum(t['abstract'] for t in r['towns'] if t['kingdom_id']==k['id'])}",person(k['ruler_id'])] for k in r['kingdoms']])
    mundo+=f"São {len(r['towns'])} localidades. Seus mercados possuem, juntos, {sum(t['food'] for t in r['towns'])} rações e {sum(t['water'] for t in r['towns'])} unidades de água; tesouros locais somam {sum(t['money'] for t in r['towns'])}. Estoques pessoais e institucionais são separados.\n\n"
    mundo+=table(['Capital','Persistentes vivos','Água no mercado','Capacidade diária / armazenamento'],[
        [place(t['id']),t['named'],t['water'],f"{t['infrastructure']['water_daily']} / {t['infrastructure']['water_storage']}"] for t in r['towns'] if t['capital']])
    mundo+='## Grupos e propostas\n\n'
    mundo+=f"Foram criados {counter('NewGroupCreated')} grupos e realizadas {counter('GroupJoined')} adesões, por {len({e['actor_id'] for e in bykind['GroupJoined']})} pessoas distintas. O registro final conserva {len(r['groups'])} grupos: {compact(Counter(g['status'] for g in r['groups']))}. Maior grupo: {max_group} membros. Causas registradas: {compact({label(k):v for k,v in gs.items()})}.\n\n"
    mundo+=table(['Grupo','Localidade','Causa','Membros','Liderança','Estado'],[
        [group(g['id']),place(g['town_id']),label(g['cause']),len(g['member_ids']),person(g['leader_id']),label(g['status'])]
        for g in sorted(r['groups'],key=lambda g:len(g['member_ids']),reverse=True)[:8]])
    mundo+=f"Propostas criadas: {counter('ProposalCreated')}; reutilizações: {counter('CompatibleProposalFound')}; registros de apoio: {counter('ProposalSupported')}; entregas presenciais: {counter('ProposalSubmitted')}. Estados finais: {compact({label(k):v for k,v in propstates.items()})}. Decisões ao longo da campanha: {compact({label(k):v for k,v in decstates.items()})}.\n\n"
    mundo+=table(['Proposta','Jurisdição / setor','Pessoas únicas / apoios entregues','Grupos / facções apoiadores','Estado'],[
        [p['id'],f"{place(p['town_id'])} / {p['sector']}",f"{p['support']} / {len(p['delivered_supporter_ids'])}",f"{len(p['supporting_group_ids'])} / {len(p['supporting_faction_ids'])}",label(p['status'])]
        for p in sorted(r['proposals'],key=lambda p:p['support'],reverse=True)[:8]])
    mundo+='## Políticas materiais\n\n'
    mundo+=f"Políticas criadas: {counter('PolicyCreated')}; setores: {compact(ps)}. Etapas efetivamente trabalhadas: {counter('PolicyEffect')}. Salários pagos: {metrics['policy_wages']}; materiais consumidos: {compact(materials)}. Localidades com capacidade hídrica expandida: {len(water_towns)}.\n\n"
    mundo+=table(['Política','Localidade / setor','Etapas','Orçamento / gasto / devolvido / reservado','Estado / último obstáculo'],[
        [p['id'],f"{place(p['jurisdiction'])} / {p['sector']}",f"{p['work_done']} / {p['work_required']}",f"{p['budget']} / {p['spent']} / {p['refunded']} / {p['money']}",f"{label(p['status'])}; {p['barriers'].get('reason','—')}"] for p in r['policies']])
    mundo+='## Facções\n\n'
    mundo+=f"Formalizações durante a campanha: {counter('FactionFormalized')}. Convites: {counter('FactionInvite')}; pedidos de ingresso: {counter('FactionJoinRequest')}; aceites: {counter('FactionMembershipAccepted')}; recusas: {counter('FactionMembershipRejected')}; adiamentos: {counter('FactionMembershipDeferred')}; condições: {counter('FactionMembershipConditioned')}. Respostas repetidas são acontecimentos, não pessoas adicionais. Estados dos registros conservados: {compact(invstates)}.\n\n"
    for f in r['factions']:
        mundo+=f"- **{f['name']} (#{f['id']})**: {label(f['purpose'])}; {label(f['status'])}; sede {place(f['headquarters_id'])}; líder {person(f['leader_id'])}. Membros ({len(f['member_ids'])}): "+', '.join(person(i) for i in f['member_ids'])+'. '
        mundo+=f"Caixa {f['money']}; estoque próprio {compact(f['inventory'])}. Capacidades no contexto local do líder: "+', '.join(k for k,v in f['capabilities'].items() if v)+'. '
        mundo+='Status local conhecido: '+(', '.join(f"{place(int(id))}: {row['status']}" for id,row in f['local_status'].items()) or 'sem registro de classificação local')+'.\n'
    mundo+='\nAções institucionais realizadas: '+compact(Counter(e['context']['action'] for e in actions))+'. Capacidades disponíveis não equivalem a ações realizadas.\n\n'
    mundo+='## Religião, conflitos e caminhos\n\n'
    mundo+=table(['Divindade','Domínio','Viva','Seguidores vivos registrados','Vínculos'],[
        [g['name'],g['domain'],'sim' if g['alive'] else 'não',r['followers'].get(str(g['id']),0),len(g['bonds'])] for g in r['gods']])
    mundo+=f"Intervenções divinas: {counter('DivineIntervention')}; audiências: {counter('DivineAudience')}; apoteoses: {counter('Apotheosis')}; mortes divinas: {counter('DivinityKilled')}. Mortes por combate no registro: {r['deaths'].get('combat',0)}. Ataques: {counter('CharacterAttacked')}; roubos: {counter('ItemStolen')}.\n\n"
    mundo+=f"A malha tem {r['routes']['count']} rotas e {r['routes']['traversals']} travessias acumuladas. Viagens iniciadas: {counter('JourneyStarted')}; chegadas: {counter('JourneyArrived')}. POIs: {compact(Counter(p['kind'] for p in r['points']))}. "
    mundo+='Sedes/locais reclamados: '+('; '.join(f"{p['name']} (#{p['id']}), posse #{p['claimant_id']}" for p in r['points'] if p['claimant_id']) or 'nenhum')+'.\n\n'
    mundo+='O [registro compacto](campanha_300h/resumo.json) contém IDs, localidades e organizações para consultas além destas tabelas. As trajetórias selecionadas estão em [HISTORIAS_REAIS.md](HISTORIAS_REAIS.md).\n'

    tech=f"# RELATÓRIO TÉCNICO — Fase 5.5\n\n## Entrega e alcance\n\nVersão `{r['rules']}`, especificação preservada em `fase_5_5.md`. A fase adapta os serviços existentes para ligar grupo, apoio político, política material, continuidade organizacional e decisão de adesão. Campanha natural **{r['seed']}**, do zero, sem jogador, **300 horas**. Houve um reinício estrutural na mesma seed, documentado abaixo; não houve seleção de seed por resultados interessantes.\n\n"
    tech+='## Arquitetura e implementação\n\nDataclasses, Engine, eventos, conhecimento individual, itens, trabalho, JSON e Need → Utility → Goal → ação continuam sendo a arquitetura. `institutions.py` concentra a integração institucional; não cria um segundo motor de agentes ou economia. A versão de geração continua `mvp-5.4`; regras/saves mudaram. O carregador aplica a incompatibilidade de versão existente. O baseline contém somente fontes anteriores, sem saves/dumps.\n\n'
    tech+=table(['Sistema','Implementado','Limite real'],[
        ['Grupos conhecidos','Conhecimento por encontros/fatos; busca antes da criação; adesão por qualquer membro presente; motivos de incompatibilidade; até 64 participantes','Conhecer a existência não garante encontro. Cooperação por proposta comum; fusão automática não foi criada.'],
        ['Propostas','Busca entre propostas conhecidas/publicadas; equivalência por jurisdição/setor/efeito/sujeito; apoio único por pessoa e diversos grupos/facções','Apoios remotos só chegam com representação física. Grupos desconhecidos podem legitimamente fragmentar.'],
        ['Pressão e prefeito','Apoios vivos entregues, urgência, persistência, visibilidade e crise; avaliação contextual com personalidade e dinheiro','Pressão é simplificada: área afetada fica registrada; legitimidade/reputação não têm modelo político completo.'],
        ['Política genérica','Estado persistente, dinheiro em reserva, trabalho, efeitos, obstáculos e devolução; aprovação não cria bens','Não há contratação administrativa completa nem garantia de trabalhador disponível.'],
        ['WATER','Obra remunerada consome madeira/ferro; cada duas etapas amplia 20/dia e 40 de armazenamento; coleta diária usa a capacidade','Sem obra não há expansão; sem produção/acesso, estoque disponível continua limitado. Não foi aplicado aumento inicial global.'],
        ['FOOD / PROCESSING / EMPLOYMENT','Profissão/trabalho existentes; matéria-prima e crédito fracionário de grão; alimento produzido em estoque real','A execução alimentar é o primeiro caminho material; não representa todos os empregos e produtos possíveis.'],
        ['WEAPONS / RAW_MATERIAL / SECURITY','Encomenda consome ferro/madeira; produção profissional real com subsídio; guardas observam/patrulham','Matéria-prima segue remuneração normal mais subsídio reservado; patrulha não garante queda de crime.'],
        ['TRANSPORT','Comerciante recebe carga real; rota conhecida e mantimentos; Journey existente; salário somente após entrega física','Primeiro serviço de transporte distribui grão/madeira/ferro dentro do mesmo reino. Comércio remunerado generalizado e contratos extensos ficam para depois.'],
        ['Resultados','Fatos percebidos ligam resposta/efeito/frustração ao grupo; alívio depende da necessidade observada; sem dissolução automática por aprovação','Conhecimento de resultado ainda pode ser atrasado; aprovação isolada não significa resolução do problema.'],
        ['Formalização','Pressão derivada de duração, falhas conhecidas, reuniões, participantes e contribuições; origem/fundadores/história preservados','Presença, financiamento e condições anteriores continuam exigidos; tamanho sozinho não formaliza.'],
        ['Adesão','Benefício/custo por necessidade, profissão, confiança, autonomia, ambição e risco; condição de equipamento, adiamento, retomada, canal físico','Termos usam informação comunicada; benefícios anunciados dependem de recursos e execução posteriores.'],
        ['Facções','Capacidades derivadas; compra, suprimento, patrulha, apoio a proposta, resposta a restrição e incursão com recursos próprios','Treinamento especializado, escolta remunerada e contratos CityContract extensos não foram adicionados; alguns caminhos reutilizam ações anteriores.'],
        ['Crime e lei','Crimes próprios/reconhecidos e confiança permitem cooperação genérica; classificação por cidade e fatos conhecidos; reação institucional','Sem classe Bandit ou guerra automática. Multa, banimento, guerra e todos os modos de negociação não ganharam ciclo completo.'],
    ])
    tech+='A pressão usada é `min(100, 2×apoiadores vivos entregues + 0,3×urgência + persistência até 20 + visibilidade (2/10) + crise (0/10))`. Esse valor compete com personalidade e custo: apoio não determina aprovação. Recursos institucionais usam ItemService e dinheiro dos mesmos donos; os setores não mantêm estoques paralelos fictícios.\n\n'
    tech+='## Testes controlados e smoke\n\n**28 verificações passaram**: os 14 métodos da Fase 5.5, dez da Fase 5.4 e quatro regressões críticas de alimentação/letalidade. Não houve repetição da suíte histórica inteira. Os controles novos cobrem busca conhecida/desconhecida, incompatibilidade, grupo de 20 pessoas, proposta reutilizada, contagem única entre grupos/facção, pressão no julgamento, reserva monetária sem geração de bens, água/alimento/entrega por rota, falta material, formalização, capacidades, estados de convite e retomada, infrações sucessivas e organização criminosa genérica. Log: `testes_regressoes.log`.\n\n'
    tech+='Dois smokes pequenos de 48h usaram mundos reduzidos: o natural teve 77 NPCs, cinco grupos e duas propostas; o controlado teve 69 NPCs, três grupos, três propostas e uma política. Ambos passaram integridade, rotas e ida/volta JSON; seus saves temporários foram apagados automaticamente. `smoke.json` e `smoke_politica.json` conservam apenas resultados.\n\n'
    tech+='Esses controles demonstram capacidade sob condições preparadas. Aceite, formalização, ilegalidade, banditismo, produção e transporte controlados não são lore da campanha. A ocorrência natural aparece nas métricas seguintes.\n\n'
    tech+='## Falha encontrada e correções\n\nA primeira execução parou na hora **50**, porque o validador ainda rejeitava grupos acima de **16** pessoas, embora a adesão nova permitisse crescimento. Doze grupos acionaram a invariante antiga. O registro mínimo está em `interrompida_50h/falha.json`, com manifesto e log. Não foi preservado um dump completo. O limite foi alinhado a 64 e um controle foi ampliado para validar 20 membros. A campanha foi reiniciada do zero com **a mesma Vaelora-55**.\n\n'
    tech+=table(['Correção','Razão'],[
        ['Limites de membros e estado ignored no validador','Dados novos precisam ser aceitos pela integridade, preservando os limites de memória anteriores.'],
        ['Avaliação da utilidade de policy_work','O peso financeiro usa a consideração financeira existente, evitando chave ausente no percurso real Need/Goal.'],
        ['Entrega presencial dos apoios','Registrar assinatura num grupo distante não pode elevar instantaneamente a pressão recebida pelo prefeito.'],
        ['Fontes de infrações sucessivas','Uma nova infração deve ser registrada mesmo se RESTRICTED não mudou; a terceira evidência pode levar a ILLEGAL.'],
        ['Proteção de propostas vinculadas a políticas','A limpeza periódica anterior não pode excluir a proposta que uma política ainda referencia.'],
        ['Fundadores presentes','A formalização usa participantes presentes, preservando origens sem transferir pessoas remotas.'],
    ])
    tech+='## Campanha natural concluída\n\n'
    tech+='**Diferença entre código medido e entrega final:** após a campanha, a revisão constatou que a alternativa `ignore` era sempre matematicamente superada por `reject`. A entrega acrescenta contexto de falta de orçamento/exaustão para tornar ignorar uma decisão possível, e reconsideração quando a pressão recebida aumenta. Também conserva o quadro público de propostas na substituição de prefeito. Os controles 4 e 6 verificam esses ajustes. Eles não foram aplicados retroativamente à campanha, que não teve decisões `ignore`. `versoes.json` identifica os hashes; duas fontes auditadas permitem reconstruir o núcleo medido. Não houve nova campanha nem horas extras.\n\n'
    tech+=table(['Indicador','Resultado'],[
        ['Escala inicial',f"{initial['named']} persistentes + {initial['abstract']} abstratos; {initial['kingdoms']} reinos, {initial['localities']} localidades"],
        ['Grupos criados / adesões',f"{counter('NewGroupCreated')} / {counter('GroupJoined')} ({len({e['actor_id'] for e in bykind['GroupJoined']})} pessoas distintas)"],
        ['Buscas / encontros compatíveis / recusas',f"{counter('GroupSearchAttempt')} / {counter('ExistingGroupFound')} / {counter('GroupJoinRejected')}"],
        ['Grupos finais / maior',f"{len(r['groups'])} / {max_group} membros"],
        ['Dissoluções / fusões',f"{counter('GroupDissolved')} / {counter('GroupMerged')}"],
        ['Propostas criadas / reutilizações',f"{counter('ProposalCreated')} / {counter('CompatibleProposalFound')}"],
        ['Apoios / entregas de apoio / submissões',f"{counter('ProposalSupported')} / {counter('ProposalSupportDelivered')} / {counter('ProposalSubmitted')}"],
        ['Decisões',compact(decstates)],
        ['Políticas / etapas pagas',f"{counter('PolicyCreated')} / {counter('PolicyEffect')}"],
        ['Setores / estados',compact(ps)+'; '+compact(Counter(p['status'] for p in r['policies']))],
        ['Materiais consumidos / salários',compact(materials)+f"; {metrics['policy_wages']} moedas"],
        ['Capacidade hídrica ampliada',f'{len(water_towns)} localidades'],
        ['Formalizações naturais',counter('FactionFormalized')],
        ['Convites / pedidos / aceites',f"{counter('FactionInvite')} / {counter('FactionJoinRequest')} / {counter('FactionMembershipAccepted')}"],
        ['Recusas / adiamentos / condições',f"{counter('FactionMembershipRejected')} / {counter('FactionMembershipDeferred')} / {counter('FactionMembershipConditioned')}"],
        ['Ações de facção / mudanças legais',f"{counter('FactionAction')} / {counter('FactionLocalStatusChanged')}"],
        ['Cooperação criminosa registrada',sum(g['cause']=='criminal_cooperation' for g in r['groups'])],
        ['Mortes',str(death_total)+'; '+compact(r['deaths'])],
        ['Integridade / rotas','Zero erros em seis marcos (50–300h); zero erros de rota'],
        ['Tempo da execução',f"{r['runtime_seconds']:.2f}s"],
    ])
    tech+='Apoios são únicos **por proposta**; a mesma pessoa pode apoiar diferentes propostas. Adesões e recusas são contagens de acontecimentos; não representam igual número de pessoas ou grupos redundantes evitados. O registro de apoio entre grupos mostra cooperação. Não houve deduplicação global onisciente nem fusão forçada.\n\n'
    tech+='Motivos registrados para recusa de grupo: '+compact(metrics['group_rejection_reasons'])+'. Alguns acontecimentos são tentativas repetidas; esses números não representam igual número de pessoas incompatíveis.\n\n'
    tech+='## O que os resultados permitem concluir\n\n'
    tech+=f"A integração natural produziu {counter('GroupJoined')} adesões a grupos existentes, {counter('CompatibleProposalFound')} reutilizações de propostas e {counter('FactionMembershipAccepted')} ingressos em facções. Esses resultados distinguem continuidade efetiva de mera criação de objetos. As políticas tiveram {counter('PolicyEffect')} etapas pagas; {sum(p['status']=='completed' for p in r['policies'])} concluídas e {sum(p['status']=='stalled' for p in r['policies'])} paralisadas no encerramento. Aprovação e efeito material permaneceram separados.\n\n"
    tech+='A campanha da Fase 5.4 tinha 179 grupos criados, 87 propostas e nenhum ingresso em facção, em 200h, seed Arandor-54, com 1.826 persistentes iniciais. Esta campanha tem outra seed, elenco e duração: a comparação descritiva sugere continuidade onde existia fragmentação, mas não mede isoladamente um efeito causal ou percentual de melhoria. Não foi feita outra campanha comparativa longa.\n\n'
    tech+='## Limites e gargalos\n\n'
    tech+='**Gargalo observado:** houve 16 grupos de água, mas somente duas propostas WATER, criadas nas horas 94 e 125, ambas ainda em rascunho e sem apoio entregue. Não surgiu política WATER ou FOOD: as duas políticas naturais foram de segurança. Ao final, os representantes de água estavam com fome 90/70 e HP 37/8; um coletava alimento e o outro dormia. Esse retrato final comprova concorrência vital naquele momento, sem reconstituir cada decisão anterior. Das 315 mortes, 314 (99,7%) foram por fome, sede ou ambas.\n\n'
    tech+='Uma leitura do save, sem avançar horas, encontrou 14 propostas entregues ainda sem decisão e 13 convites oferecidos com necessidade de adesão ativa. Os responsáveis e candidatos frequentemente estavam exaustos, sem dinheiro pessoal ou atendendo alimentação/recuperação. Um prefeito citado havia morrido no fechamento, antes da próxima rodada de reposição. `diagnostico_gargalos.json` preserva somente esses estados mínimos; não substitui um histórico de decisões. Tesouro municipal e dinheiro do NPC são donos distintos: atender a administração não paga salário automaticamente no código atual.\n\n'
    tech+='**Próximos ajustes recomendados:** remunerar serviço administrativo com o tesouro real e trabalho efetivo; permitir representação delegada e resposta institucional com continuidade mesmo quando o líder precisa se recuperar; registrar por que cada tarefa institucional perdeu a disputa de prioridades. Esses caminhos devem ser testados com estoques e dinheiro reais, sem rebaixar necessidades vitais ou garantir aprovação. A hipótese é que reduzam a dependência da disponibilidade de uma única pessoa; esta campanha não mede esse efeito futuro.\n\n'
    tech+='- A oferta de trabalho concorre com sede, fome, descanso e compromissos. `no_effective_work` identifica a falta de execução, sem atribuir por si só a culpa a um traço ou NPC específico. Obras dependem de madeira/ferro e de trabalhadores que saibam da política.\n'
    tech+='- A capacidade hídrica pode responder por obras; esta fase não demonstra equilíbrio demográfico/material definitivo. Mortalidade ou mercados vazios não devem ser tratados como resolvidos por existir uma política.\n'
    tech+='- Há limite de 24 propostas por administração, 64 membros por grupo/facção, memórias e históricos curtos. Políticas referenciadas são preservadas; ainda falta arquivamento compacto completo para sucessivos anos de campanhas políticas. A execução de 300h não demonstra estabilidade indefinida de memória.\n'
    tech+='- Fusão negociada, carreira/treinamento institucional completo, todos os contratos administrativos e conflitos territoriais longos continuam fora da implementação mínima. Capacidades declaradas para ações futuras não são prova de execução.\n'
    tech+='- Não há eleições, guerra entre reinos nem economia paralela. Raridades ausentes naturalmente não justificam reiniciar ou manipular a seed.\n\n'
    tech+='## Disco e retenção\n\nOs artefatos regeneráveis foram inventariados antes de qualquer remoção. Foram removidos 377 arquivos grandes de execução, preservando fontes, testes, configuração, baselines de código, documentação, relatórios finais históricos e evidências compactas. O manifesto de limpeza registra caminho, tamanho, tipo e relatório preservado; não foi removida a árvore do projeto.\n\n'
    tech+='<!-- DISK_FINAL -->\n\n'
    tech+='O save completo desta campanha deve ser apagado **somente após** gravar e auditar os três relatórios. `retencao.json` registra hash, tamanho e confirmação da remoção. Os eventos retidos em `eventos_relevantes.json` são os usados nas histórias; métricas e `resumo.json` preservam cadastro mínimo, sem mapas, itens completos, memória individual ou milhões de ações. O dump intermediário de eventos é removido.\n\n'
    tech+='Arquivos principais: [MUNDO.md](MUNDO.md), [HISTORIAS_REAIS.md](HISTORIAS_REAIS.md). Auditoria: `campanha_300h/{manifesto,resumo,metrics,eventos_relevantes}.json`, `testes_regressoes.log`, `limpeza.json` e `auditoria_disco_antes.json`.\n'

    for name,text in [('RELATORIO_TECNICO.md',tech),('MUNDO.md',mundo),('HISTORIAS_REAIS.md',hist)]:
        (OUT/name).write_text(text,encoding='utf-8')
    (DATA/'metrics.json').write_text(json.dumps(metrics,ensure_ascii=False,indent=2))
    (DATA/'eventos_relevantes.json').write_text(json.dumps(sorted(selected.values(),key=lambda e:e['id']),ensure_ascii=False,indent=2))
    print(json.dumps({'stories':len(stories),'selected_events':len(selected),'metrics':{k:v for k,v in metrics.items() if k not in ('events','checks')}}))

if __name__=='__main__':main()
