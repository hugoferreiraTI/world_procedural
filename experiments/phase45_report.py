"""Relatório derivado de eventos e transições reais, sem gerar lore fictícia."""
import gzip,json
from collections import Counter,defaultdict
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
FOLDER=ROOT/'reports/fase_4_5'
LABELS={'family':'cuidado ou busca familiar','revenge':'vingança/reparação','pursuit':'perseguição institucional',
        'migration':'mudança de residência','protection':'proteção','advancement':'ascensão pessoal',
        'status':'reconhecimento','grief':'luto'}
STAGES={'CommitmentCreated':'objetivo adotado','CommitmentProgress':'mudança verificável',
        'CommitmentStrategyChanged':'mudança de estratégia','CommitmentInformation':'nova informação',
        'CommitmentRetargeted':'alvo revisto por evidência','CommitmentTravel':'viagem por pista conhecida',
        'CommitmentPaused':'intenção pausada','CommitmentResumed':'intenção retomada',
        'CommitmentCompleted':'objetivo encerrado','CommitmentAbandoned':'objetivo abandonado',
        'CommitmentExpired':'intenção expirada'}

def read(p):return json.loads(p.read_text())
def number(n):return f'{n:,}'.replace(',','.')

def run():
    global_dir=FOLDER/'global_5000h';d=read(global_dir/'resumo.json');short=read(FOLDER/'curta_entrega_500h/resumo.json')
    release=read(FOLDER/'preservacao.json');controlled=read(FOLDER/'comparacao_ambicao_entrega.json')
    before=read(ROOT/'reports/fase_4_1/global_5000h/resumo.json');people=read(global_dir/'personagens.json')
    arcs=read(global_dir/'arcos.json');cases=read(global_dir/'casos_institucionais.json')
    by_origin=defaultdict(list)
    for cid,a in arcs.items():by_origin[a['origin']].append((cid,a))
    def score(pair):
        a=pair[1];distinct=len({t['kind'] for t in a['transitions']})
        return distinct*100+min(60,a.get('ended_at',5000)-a['created_at'])+min(100,len(a['transitions']))
    selected=[];chosen=set()
    for origin in ('revenge','pursuit','advancement','family','protection','migration','status','grief'):
        options=sorted(by_origin[origin],key=score,reverse=True)
        if options:
            item=options[0];selected.append(item);chosen.add(item[0])
    failures=sorted(((cid,a) for cid,a in arcs.items() if cid not in chosen and a.get('ending')=='CommitmentAbandoned'),key=score,reverse=True)
    if failures:selected.append(failures[0])
    unresolved=sorted(((cid,a) for cid,a in arcs.items() if cid not in chosen and not a.get('ending')),key=score,reverse=True)
    if unresolved:selected.append(unresolved[0])
    chosen.update(cid for cid,a in selected)
    for origin in ('revenge','pursuit','advancement'):
        options=sorted(((cid,a) for cid,a in arcs.items() if cid not in chosen and a['origin']==origin
                        and a.get('ending')=='CommitmentAbandoned'),key=score,reverse=True)
        if options:selected.append(options[0]);chosen.add(options[0][0])
    deaths_without_goal=sorted(((cid,a) for cid,a in arcs.items() if cid not in chosen and
        any(t['context'].get('reason')=='owner_died' for t in a['transitions'])),key=score,reverse=True)
    if deaths_without_goal:selected.append(deaths_without_goal[0])
    wanted_ids={t['id'] for _,a in selected for t in a['transitions']}
    wanted_ids.update(i for _,a in selected for i in a['event_ids'])
    wanted_ids.update(a.get('source_fact') for _,a in selected)
    events={};fatalities=[];event_count=0
    with gzip.open(global_dir/'eventos.jsonl.gz','rt') as f:
        for line in f:
            e=json.loads(line);event_count+=1
            if e['id'] in wanted_ids:events[e['id']]=e
            if e['kind']=='CharacterKilled':fatalities.append(e)
    names=lambda pid:people.get(str(pid),{}).get('name',f'NPC #{pid}')
    evidence=[];text=['# Histórias reais — Fase 4.5\n',
      'Seleção de arcos da campanha nova de 5.000 horas, seed Vespera-47. Cada marco abaixo possui ID no registro bruto. '
      '“Concluído” significa que a condição da necessidade foi encerrada; não significa necessariamente matar, enriquecer ou encontrar alguém. '
      'A duração conta horas desde a adoção do compromisso. Pausas preservam intenção, sem representar trabalho contínuo.\n']
    traces_needed={cid for cid,a in selected};traces={};last_traces={}
    with gzip.open(global_dir/'decisoes_sociais.jsonl.gz','rt') as f:
        for line in f:
            row=json.loads(line);c=row.get('commitment')
            if c and str(c['id']) in traces_needed:
                traces.setdefault(str(c['id']),row);last_traces[str(c['id'])]=row
    for i,(cid,a) in enumerate(selected,1):
        owner=names(a['owner']);end=a.get('ended_at',5000);source=events.get(a.get('source_fact'))
        row=traces.get(cid);transitions=list(a['transitions'])
        # Marcos diversos; evita chamar cada golpe/compra de capítulo.
        first={};last=[]
        for t in transitions:
            key=t['kind']
            if key=='CommitmentProgress':key+=':'+','.join(t['context'].get('changes',[]))
            first.setdefault(key,t)
        milestones=sorted(first.values(),key=lambda t:(t['turn'],t['id']))[:9]
        if transitions and transitions[-1] not in milestones:milestones.append(transitions[-1])
        for kind in ('CommitmentPaused','CommitmentResumed'):
            e=next((events[j] for j in a['event_ids'] if j in events and events[j]['kind']==kind),None)
            if e:milestones.append({'id':e['id'],'turn':e['turn'],'kind':kind,'context':e['context']})
        milestones=sorted(milestones,key=lambda t:(t['turn'],t['id']))
        text += [f'## {i}. {owner} — {LABELS.get(a["origin"],a["origin"])}\n',
          f'Compromisso **#{cid}**, h {a["created_at"]}–{end} ({end-a["created_at"]} h). '
          f'Desfecho: **{a.get("ending","ainda sem encerramento")}**.\n']
        target=a.get('target')
        if target is not None:
            text.append(f'Destino inicial: localidade #{target}.\n' if a['origin']=='migration' else
                        f'Alvo inicialmente conhecido: **{names(target)}**, #{target}.\n')
        if source:
            text.append(f'Causa conhecida: evento **#{source["id"]}**, h {source["turn"]}: {source["description"]}\n')
        elif row:
            text.append(f'Origem registrada na necessidade: `{row["need"]["source"]}`; motivo: {row["need"]["reason"]}.\n')
        else:text.append('A origem está referenciada no arco; o evento causal não aparece no recorte bruto selecionado. Não reconstruído por suposição.\n')
        if row:
            impulse=row.get('impulse',{})
            text.append(f'Uma decisão observada: HP {row["before"]["hp"]}, fome {row["before"]["hunger"]:.0f}; '
                f'necessidade `{row["need"]["kind"]}`, ação `{row["action"]}`, sucesso={row["success"]}. '
                f'Impulso {impulse.get("impulse",0):.1f}/100; agência percebida {impulse.get("perceived_agency",0)*100:.1f}/100. '
                'Esses valores pertencem à amostra registrada, não a toda a trajetória.\n')
            text.append(f'Resposta registrada à ação: **{row["outcome"]}**. '
                        f'Novo estado medido: HP {row["after"]["hp"]}, fome {row["after"]["hunger"]:.0f}; '
                        f'posição {row["before"]["position"]} → {row["after"]["position"]}.\n')
            traits=people.get(str(a['owner']),{}).get('initial_personality',{})
            text.append('Traços iniciais relevantes: '+', '.join(f'{k}={traits[k]}' for k in
                ('ambition','persistence','vengefulness','compassion','courage') if k in traits)+'. '
                'Emotion participa da avaliação do motor, mas não foi amostrada nesta longa; não atribuímos valores ou pensamentos inventados.\n')
            last=last_traces.get(cid)
            if last and last['turn']!=row['turn']:
                text.append(f'Reavaliação posterior observada, h {last["turn"]}: `{last["action"]}`, '
                    f'sucesso={last["success"]}; resposta: **{last["outcome"]}**. '
                    f'HP {last["before"]["hp"]} → {last["after"]["hp"]}.\n')
            if a['origin']=='pursuit':
                case=cases.get(str(row['need']['context'].get('record_id')))
                if case:
                    severity=case['known_severity'].get(str(a['owner']),1)
                    deadline=case['created_at']+168*(1+severity//2)
                    if end>deadline:
                        text.append(f'**Inconsistência confirmada:** este compromisso institucional durou além do prazo '
                            f'da evidência conhecida (h {deadline}, mesmo usando a gravidade final conhecida pelo guarda). '
                            'A continuação inclui o bug de reativação/expiração corrigido na entrega; sua duração não deve '
                            'ser contada como prova de perseguição legitimamente sustentada.\n')
        text.append('| Hora | Evento | Etapa e evidência |\n|---|---|---|')
        for t in milestones:
            c=t['context'];details=[]
            for k in ('changes','action','previous','next','reason','old_target','target','destination','competing'):
                if k in c:details.append(f'{k}={c[k]}')
            text.append(f'| {t["turn"]} | #{t["id"]} | {STAGES.get(t["kind"],t["kind"])}; {"; ".join(details)} |')
        ending=transitions[-1]['context'] if transitions else {}
        activity=ending.get('activity',a.get('final',{}).get('activity_count'))
        meaningful=ending.get('meaningful_progress',a.get('final',{}).get('meaningful_progress'))
        text.append(f'\nAtividade registrada: **{activity if activity is not None else "não fechada"}**; '
                    f'episódios de progresso verificável: **{meaningful if meaningful is not None else "não fechado"}**. '
                    'Mudanças de estratégia podem ser preparos locais, não transformações profundas de vida.\n')
        evidence.append({'commitment':cid,'arc':a,'cause':source,'decision_sample':row,
                         'later_decision':last_traces.get(cid),'milestones':milestones})
    text.append('## Fatalidades e repercussões\n')
    if fatalities:
        for e in fatalities:
            related=[cid for cid,a in arcs.items() if a.get('source_fact')==e['id']]
            text.append(f'- h {e["turn"]}, evento #{e["id"]}: {e["description"]} '
                f'Intenção registrada: `{e["context"].get("violence_intent","não informada")}`. '
                f'Compromissos diretamente ligados à notícia: {", ".join("#"+x for x in related[:8]) or "nenhum registrado"}.')
    else:text.append('Nenhuma morte interpessoal ocorreu nesta campanha. A capacidade letal foi validada em regressão controlada; não há exemplo natural a inventar.\n')
    fatal_intents=Counter(e['context'].get('violence_intent','unknown') for e in fatalities)
    post_incapacity=sum(bool(e['context'].get('post_incapacity')) for e in fatalities)
    text.append(f'\nIntenções nas fatalidades reais: `{dict(fatal_intents)}`; '
                f'ataques fatais após incapacidade: **{post_incapacity}**. '
                'Ferir/subjugar ainda pode matar por dano físico, especialmente quando a vítima já tem pouco HP. '
                'Uma fatalidade sozinha não comprova execução deliberada de vingança.\n')
    text.append('## Passividade observada\n')
    examples=d['agency'].get('strong_revenge_examples',[])
    for sample in examples[:3]:
        text.append(f'- h {sample["turn"]}: {names(sample["owner"])} contra {names(sample["target"])}; '
                    f'compromisso #{sample["commitment"]}, grievance={sample["grievance"]:.1f}, '
                    f'ação atual={sample["goal"]}, diagnóstico=`{sample["reason"]}`. '
                    'O diagnóstico descreve essa amostra diária, sem concluir que o NPC permaneceu assim todo o tempo.')
    if not examples:text.append('Nenhuma amostra atingiu todos os critérios simultâneos de vingança forte definidos pelo observador.\n')
    # A longa começou antes destes campos observacionais: nunca completar
    # sua emoção por inferência. A curta da entrega fornece cadeias medidas.
    short_chains={}
    with gzip.open(FOLDER/'curta_entrega_500h/decisoes_sociais.jsonl.gz','rt') as f:
        for line in f:
            row=json.loads(line);kind=row['need']['kind']
            if (kind in ('advancement','family','pursuit') and kind not in short_chains
                    and row.get('need_before') and row.get('commitment') and row['success']):
                short_chains[kind]=row
    short_facts={};source_ids={row['commitment']['originating_fact'] for row in short_chains.values()}
    with gzip.open(FOLDER/'curta_entrega_500h/eventos.jsonl.gz','rt') as f:
        for line in f:
            event=json.loads(line)
            if event['id'] in source_ids:short_facts[event['id']]=event
    text.append('\n## Complemento: cadeias medidas na curta da entrega\n')
    text.append('Os próximos casos pertencem à execução independente de 500 h do código corrigido. '
                'IDs de eventos são locais a essa execução; não ligá-los aos IDs da longa. '
                'A curta amostrou emoções antes/depois, prioridade antes da ação e score da solução escolhida.\n')
    for kind,row in short_chains.items():
        pre=row['before'];post=row['after'];emotion=row['emotions_before'];need=row['need_before'];c=row['commitment']
        source=short_facts.get(c['originating_fact'])
        cause=source['description'] if source else 'avaliação pessoal/oportunidade registrada em '+need['source']
        cause_id=f'fato #{c["originating_fact"]}' if c['originating_fact'] is not None else 'avaliação própria'
        text.append(f'### {row["name"]} — h {row["turn"]}, {LABELS[kind]}\n')
        text.append(f'**State:** HP {pre["hp"]}, fome {pre["hunger"]}, dinheiro {pre["money"]}. '
            f'**Knowledge:** {cause}; {cause_id}, confiança registrada {c["context"]["confidence"]}. '
            f'**Emotion:** raiva {emotion["anger"]:.1f}, ressentimento {emotion["resentment"]:.1f}, '
            f'desespero {emotion["desperation"]:.1f}. '
            f'**Need:** {kind}, prioridade {need["priority"]:.1f}. '
            f'**Impulse:** {row["impulse"].get("impulse",0):.1f}; **Commitment:** #{c["id"]}. '
            f'**Solution/Action:** `{row["action"]}`, score {row["solution_score"]:.1f}. '
            f'**Response:** {row["outcome"]}. '
            f'**Consequence/New State:** HP {post["hp"]}, fome {post["hunger"]}, dinheiro {post["money"]}; '
            f'progresso verificável acumulado no compromisso {c["meaningful_progress"]}.\n')
    (FOLDER/'cadeias_curta.json').write_text(json.dumps(short_chains,ensure_ascii=False,indent=2))
    text += ['\n## Limite desta seleção\n',
      'Os registros permitem conferir fatos, decisões e transições; não reconstruímos pensamentos ou valores emocionais que não foram amostrados. '
      'Um arco longo pode continuar pobre em transformações. O JSON de arcos preserva os demais casos, inclusive falhas e objetivos pendentes.\n']
    (FOLDER/'HISTORIAS_REAIS.md').write_text('\n'.join(text))
    (FOLDER/'evidencias_historias.json').write_text(json.dumps(evidence,ensure_ascii=False,indent=2))
    agency=d['agency'];m=d['metrics']
    case_severity=Counter(c['severity'] for c in cases.values())
    case_states=Counter(c['status'] for c in cases.values())
    own=defaultdict(Counter)
    for cid,a in arcs.items():
        if a['origin'] in ('advancement','status'):
            own[a['owner']]['created']+=1
            own[a['owner']]['progress']+=sum(t['kind']=='CommitmentProgress' for t in a['transitions'])
    bins={}
    for label,minimum,maximum in (('ambição <40',0,39),('ambição 40–69',40,69),('ambição ≥70',70,100)):
        members=[(int(pid),p) for pid,p in people.items() if p.get('initial_personality') and minimum<=p['initial_personality']['ambition']<=maximum]
        bins[label]={'people':len(members),'commitments':sum(own[pid]['created'] for pid,p in members),
                     'progress':sum(own[pid]['progress'] for pid,p in members)}
    causal_depth=Counter();origins_progress=Counter()
    for a in arcs.values():
        kinds={t['kind'] for t in a['transitions']}-{'CommitmentCreated'}
        causal_depth[len(kinds)]+=1
        origins_progress[a['origin']]+=sum(t['kind']=='CommitmentProgress' for t in a['transitions'])
    report=[f'# Fase 4.5 — impulso social, ambição e consequência\n',
      f'Versão **{d["rules"]}**, seed **{d["seed"]}**, mundo novo em h 0, sem jogador e sem carregar save. '
      f'{number(d["initial"]["persistent"])} personagens persistentes, {d["initial"]["towns"]} localidades e {d["initial"]["kingdoms"]} reinos. '
      f'SHA-256 da campanha: `{d["core_sha256"]}`. '
      f'SHA-256 da entrega: `{release["final_core_sha256"]}`. '
      'A longa preserva o código congelado; correções encontradas durante a revisão foram validadas depois em regressões e na curta de entrega.\n',
      '## Resultado\n',
      f'A camada nova preserva intenções através de interrupções e permite iniciativas baseadas em aspirações. '
      f'A campanha registrou **{number(agency["commitments_total"])} compromissos**, '
      f'**{number(agency["completed"])} encerrados por resolução**, **{number(agency["abandoned"])} abandonados** '
      f'e **{number(agency["expired"])} expirados**. '
      f'{number(agency["arcs_with_progress"])} tiveram progresso verificável e '
      f'{number(agency["arcs_with_strategy_change"])} mudaram de estratégia. '
      'Esses números contam compromissos, não pessoas nem histórias profundas.\n',
      f'O avanço narrativo é parcial: persistência e mudanças de abordagem existem, mas cuidado por privação e delitos leves ainda dominam. '
      f'A sobrevivência piorou nesta campanha congelada: **{sum(d["death_causes"].values())} mortes**, '
      f'contra **{sum(before["death_causes"].values())}** na Fase 4.1. '
      'As correções finais passaram na curta de 500 h; não foi rodada outra longa para afirmar que essa diferença desapareceu.\n',
      '## Implementação e alterações necessárias\n',
      '- **Commitment:** guarda dono, necessidade, fato causal, alvo, motivação, intensidade, investimento, tentativas, progresso, fracassos e encerramento. Até quatro por NPC; mantém a mesma Need e passa novamente pelo Goal/Utility. Pausa, retomada e abandono são registrados.\n'
      '- **Memória causal:** fatos usados por compromissos ativos e até três evidências complementares ficam protegidos dentro do limite de 64 fatos. Lembrar não chama novamente o processamento emocional.\n'
      '- **Impulso/agência:** considera urgência, tempo sem resolução, fracassos, emoções, traços, relação, gravidade conhecida, recursos, saúde, risco e pistas. Não executa ações. Pressão extrema pode aliviar parcialmente custos morais/de risco e tornar roubo pessoal uma alternativa; não força crime.\n'
      '- **Aspiration:** direção principal derivada de personalidade e situação, com riqueza, competência, reconhecimento ou família. Só oferece passos apoiados por oportunidades conhecidas. Competência usa aprendizagem real; dinheiro ganho não conta como progresso de competência. Reconhecimento exige responsabilidade pública observada; família acompanha resolução de cuidados.\n'
      '- **Violência:** afastar, conter, subjugar, ferir e matar são intenções de resultado. Fórmula, armas e multiplicador de defesa permaneceram iguais. Incapacidade comum encerra combate; intenção letal sustentada abre uma nova escolha entre continuar, poupar, retirar-se, pedir ajuda ou capturar quando válido. A regressão comprova tanto poupar quanto causar fatalidade.\n'
      '- **Guarda:** usa o mesmo caso local. Informação formal circula no serviço do mercado após latência de seis horas; até três tarefas por caso: busca, vigilância e informação. Gravidade modifica prioridade e duração. Guarda remoto não aprende por telepatia.\n'
      '- **Pistas interlocalidades:** viagens passam por portão, estrada e entrada conhecidos, com provisões reais; preservam residência. Ao chegar, usa a última pista e encontros, sem consultar posição global do perseguido.\n',
      'Foi necessário integrar manutenção de compromissos ao refresh de Needs, proteger causas da remoção FIFO e permitir julgamento após incapacidade. '
      'Também foi corrigida uma falha anterior: `CharacterKilled` saía do processamento da justiça antes de registrar o crime do autor. '
      'A correção mantém a resolução de casos contra a vítima e permite registrar o homicídio conhecido. '
      'As curtas revelaram uma ligação fraca de aspirações com necessidades antigas; a revisão liga a aspiração ao objetivo compatível e separa competência de riqueza. A transição interna de motivo durante viagem também passou a preservar o compromisso, mantendo sua causa original. Um cenário controlado identificou impulso insuficiente para auto-iniciativa; a direção da aspiração agora participa do impulso e da urgência da necessidade correspondente.\n',
      'Na revisão da longa, cinco casos adicionais foram reproduzidos e corrigidos na entrega: '
      '(1) uma perseguição encerrada pelo conhecimento do próprio guarda podia ser reativada pelo compromisso; '
      '(2) a certeza da morte bloqueava identificação posterior do autor com confiança menor, mas suficiente; '
      '(3) o compromisso registrava confiança 100 por padrão mesmo com notícia 60; '
      '(4) seguir pista distante não mantinha o LOD horário usado na estimativa de viagem; '
      '(5) reutilizar uma Need resolvida podia apagar o encerramento da intenção anterior. '
      'As falhas anteriores e os testes posteriores foram preservados. Os resultados da longa incluem esses problemas; não foram recalculados ou apresentados como uma longa do código corrigido.\n',
      '## Validação e preservação\n',
      '**227 testes passaram**, incluindo 18 regressões novas e as dez de recuperação. '
      'Cobrem pausa/retomada, causa sem choque duplicado, abandono, agência sem informação remota, autoria desconhecida, evidência posterior, intenção sem bônus de dano, incapacidade, fatalidade/mercy, guardas, aspiração, save/load e determinismo.\n',
      f'As curtas de diagnóstico foram preservadas, incluindo as revisões de aspiração e continuidade. A curta da entrega passou por 500 horas em `curta_entrega_500h`, '
      f'com {sum(short["death_causes"].values())} mortes e zero violações estruturais. Uma execução inicial foi interrompida após o checkpoint de 600 h para corrigir abandono falso de viagem; os dados estão em `diagnostico_interrompido` e não entram nos resultados oficiais. Uma campanha longa foi concluída: {d["hours"]} horas. '
      f'A longa passou por {d["hours"]//100} verificações de integridade. Nenhum resultado anterior foi sobrescrito.\n',
      'Os arquivos de alimentação, recuperação, economia, profissões, geração, migração, população, política e itens são idênticos à base preservada. '
      'A fórmula `power` também é idêntica. O registro dessa comparação está em `preservacao.json`. '
      'Nova versão de save; campanhas antigas continuam acessíveis com sua versão correspondente preservada.\n',
      '## Comparação física com a Fase 4.1\n',
      '| Indicador em 5.000 h | Fase 4.1 | Fase 4.5 |\n|---|---:|---:|',
      f'| Vivos | {before["alive"]} | {d["alive"]} |',
      f'| Mortes por fome/fome+sede | {before["death_causes"].get("hunger",0)+before["death_causes"].get("both",0)} | {d["death_causes"].get("hunger",0)+d["death_causes"].get("both",0)} |',
      f'| Mortes por sede | {before["death_causes"].get("thirst",0)} | {d["death_causes"].get("thirst",0)} |',
      f'| Mortes por combate | {before["death_causes"].get("combat",0)} | {d["death_causes"].get("combat",0)} |',
      f'| Ataques individuais | {before["metrics"].get("AttackExecuted",0)} | {m.get("AttackExecuted",0)} |',
      f'| Rações por dia de NPC vivo | {before["rations_per_persistent_npc_day"]:.4f} | {d["rations_per_persistent_npc_day"]:.4f} |',
      f'| Mortes alimentares carregando comida | {len(before["food_carried_deaths"])} | {len(d["food_carried_deaths"])} |\n',
      'Mesma seed e geração inicial; as decisões e o fluxo aleatório divergem depois. A comparação é descritiva, não isola o efeito de cada mecanismo. '
      'Não houve meta de mortalidade ou aumento de dano/produção para obter estes resultados.\n',
      f'Variação observada de mortes totais: {sum(before["death_causes"].values())} → {sum(d["death_causes"].values())}. '
      'Se a mortalidade aumenta, isso é uma regressão de sobrevivência observada, mesmo com módulos fisiológicos iguais; '
      'mudanças nas escolhas, deslocamentos e acesso podem alterar o resultado. A curta posterior não prova recuperação dessa diferença no horizonte de 5.000 h.\n',
      '## Continuidade, violência e instituição\n',
      f'Duração média dos compromissos: **{agency["duration_mean"]:.1f} h**, incluindo os ainda ativos, portanto com censura no fim da campanha. '
      f'{number(agency["arcs_with_three_distinct_causal_transitions"])} arcos tiveram pelo menos três tipos de transição além da adoção. '
      'Isso mede diversidade de marcos; preparar comida/água e trocar abordagem também conta, sem equivaler a uma grande saga.\n',
      '| Origem | Compromissos adotados | Episódios de progresso |\n|---|---:|---:|']
    for origin,total in agency['commitments_by_origin'].items():report.append(f'| {LABELS.get(origin,origin)} | {number(total)} | {number(origins_progress[origin])} |')
    report += [f'\nTransições de intenção: `{agency["violence_intent_transitions"]}`. '
      f'Incapacidades: {m.get("CharacterIncapacitated",0)}; poupados: {m.get("IncapacitatedSpared",0)}; '
      f'fugas: {m.get("CharacterFled",0)}; rendições: {m.get("CharacterSurrendered",0)}; capturas: {m.get("CharacterCaptured",0)}. '
      'São ocorrências, não indivíduos ou conflitos únicos.\n',
      f'Fatalidades por intenção: `{dict(fatal_intents)}`; continuadas após incapacidade: {post_incapacity}. '
      'A capacidade de julgamento letal em cenário controlado não prova sua frequência natural nem comprova que as mortes registradas foram vinganças executadas.\n',
      f'Casos institucionais: {number(agency["institutional_cases"])}; '
      f'casos com mais de uma tarefa de guarda: {number(agency["multi_guard_cases"])}. '
      f'Máximos observados: {agency["maximum_commitments_per_character"]} compromissos por personagem e '
      f'{agency["maximum_case_assignments"]} guardas atribuídos por caso. A maioria dos registros é de delitos leves.\n',
      f'Gravidade dos casos: `{dict(sorted(case_severity.items()))}`. '
      f'Estados institucionais finais: `{dict(case_states)}`; cada guarda continua limitado ao estado que pessoalmente conhece.\n',
      f'Amostras diárias de vingança forte/agressividade compatível: `{agency.get("strong_revenge_daily_samples",{})}`. '
      'As categorias distinguem pista desconhecida, distância, incapacidade, trégua, outra necessidade e Utility/risco; '
      'as amostras não são pessoas independentes. O perfil e os exemplos estão no resumo JSON.\n',
      '## Ambição\n',
      '| Ambição inicial | NPCs | Compromissos de ascensão/reconhecimento | Episódios de progresso |\n|---|---:|---:|---:|']
    for label,b in bins.items():report.append(f'| {label} | {b["people"]} | {b["commitments"]} | {b["progress"]} |')
    report.append('\nControle de 120 h, seed Ambicao-45, mesmo mundo e mesmo agricultor; somente ambição inicial foi alterada:\n\n'
                  '| Ambição | Compromissos adotados | Ações de ascensão | Dinheiro final |\n|---|---:|---:|---:|')
    for trait,result in controlled['results'].items():
        count=sum(v for k,v in result['actions'].items() if k.startswith('advancement:'))
        report.append(f'| {trait} | {len(result["commitments_created"])} | {count} | {result["money"]} |')
    report += ['\nA regressão controla a direção do efeito: maior ambição aumenta intensidade/prioridade, sem criar ação automática. '
      'As faixas da campanha misturam profissão, riqueza, sobrevivência e oportunidade; não provam causalidade isolada. '
      'Ascensão profissional ainda depende das oportunidades de aprendizagem já existentes, sobretudo cozinha.\n',
      '## Histórias e limites\n',
      f'[Leia as histórias e suas evidências](<{FOLDER / "HISTORIAS_REAIS.md"}>). '
      'A seleção inclui cuidado, perseguição, vingança/reparação, ascensão, proteção, viagem, fracasso e intenção ainda aberta. '
      'Os arcos completos permanecem em `global_5000h/arcos.json`; não contamos golpes repetidos como capítulos. '
      'O complemento da curta corrigida registra a cadeia completa com emoções e prioridade medidas; a longa não tinha esses campos, e sua ausência foi explicitada.\n',
      '- A fisiologia permanece com as limitações documentadas na Fase 4.1. Esta fase não encerra o problema de fome/recuperação.\n'
      '- Progresso local e preparo são reais, mas nem sempre produzem transformação narrativa profunda; continuidade não garante uma boa história.\n'
      '- Aspirações dependem das capacidades disponíveis; reconhecimento e competência têm repertório limitado.\n'
      '- Agência percebida é uma estimativa simples de recursos, saúde, risco e lugares/pessoas conhecidos. Conhecer uma oportunidade não garante acesso; caminhos inviáveis ainda podem gerar otimismo e tentativas frustradas.\n'
      '- Comunicação institucional exige serviço local e tem alcance limitado; guardas podem perder pistas, abandonar ou não conseguir capturar.\n'
      '- Intenção letal é possibilidade, não obrigação. Separar sua capacidade controlada da frequência natural registrada.\n'
      '- Vingança pode encerrar por denúncia, reconciliação, morte conhecida ou abandono; não chamar isso automaticamente de vingança executada.\n'
      '- A falha anterior de bloqueio entre `forage_meal` e `forage` continua fora desta fase.\n'
      '- Uma seed, uma longa; resultados não representam todos os mundos.\n',
      'Prioridades antes de ampliar conteúdo: conferir perseguições que trocam casos sem avanço, viagens com acesso precário a água/comida e '
      'aspirações com muitas tentativas e nenhuma conquista. As cinco correções finais resolvem casos específicos; o aumento de mortes e a pouca profundidade de alguns arcos continuam limitações abertas.\n',
      'Não foram adicionados política, guerras, revoluções, facções novas, deuses ou religião organizada. '
      'Antes de expandir, revisar os arcos com muita atividade e pouco progresso e os diagnósticos de prioridade/pistas. '
      'A evolução central é manter intenção, reavaliar meios e registrar consequências através dos sistemas existentes.\n',
      '## Arquivos\n',
      '`fase_4_5.md`: especificação; `tests/test_phase45.py`: regressões; '
      '`reports/fase_4_5/global_5000h/`: campanha, save, resumo, personagens, casos, arcos e logs comprimidos; '
      '`reports/fase_4_5/evidencias_historias.json`: seleção causal verificável.\n']
    report.append(f'\nCusto observado da longa: {d["runtime_seconds"]/60:.1f} minutos até apurar o resumo '
        '(exclui exportação final do save); histórico com '+number(d['history_events'])+' eventos. '
        'Estados ativos têm limites, mas o histórico persistente cresce com a campanha; pausa/retomada pode produzir bastante volume. '
        f'O save exportado ocupa {(global_dir/"save_final.json").stat().st_size/1024**2:.1f} MiB.\n')
    (ROOT/'RELATORIO_FASE_4_5.md').write_text('\n'.join(report))
    (FOLDER/'RELATORIO_FASE_4_5.md').write_text('\n'.join(report))
    (FOLDER/'analise_narrativa.json').write_text(json.dumps({'depth_distribution':dict(causal_depth),
        'ambition_bins':bins,'progress_by_origin':dict(origins_progress),'selected_arcs':[c for c,a in selected],
        'event_rows':event_count},ensure_ascii=False,indent=2))
    print(json.dumps({'report':'RELATORIO_FASE_4_5.md','stories':len(selected),'events':event_count},ensure_ascii=False))

if __name__=='__main__':run()
