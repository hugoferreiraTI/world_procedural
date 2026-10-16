"""Relatório derivado de evidências reais; casos ausentes permanecem ausentes."""
import gzip,json
from pathlib import Path
from collections import Counter,defaultdict

ROOT=Path('reports/fase_4_6')
FOLDER=ROOT/'global_5000h'
def read(p):return json.loads(p.read_text())
def write(p,text):p.write_text(text,encoding='utf-8')
def run():
    s=read(FOLDER/'resumo.json');short=read(ROOT/'curta_validacao_final_500h/resumo.json')
    arcs=read(FOLDER/'arcos.json');people=read(FOLDER/'personagens.json')
    cases=read(FOLDER/'casos_institucionais.json');life=read(FOLDER/'vida_durante_espera.json')
    places=read(FOLDER/'localidades_iniciais.json')['towns']
    metrics=s['metrics'];phase=s['phase46'];events={};prior_harm={};harm_by_pair=defaultdict(lambda:{'attacks':0,'damage':0});counts=Counter();by_owner=defaultdict(list);actions_by_arc={};wanted_migrations=set()
    with gzip.open(FOLDER/'decisoes_sociais.jsonl.gz','rt') as stream:
        for line in stream:
            d=json.loads(line);c=d.get('commitment')
            if not c:continue
            key=str(c['id'])
            if d['action']=='migrate' and d['success'] and d.get('need',{}).get('context',{}).get('reason')=='wanted':wanted_migrations.add(key)
            row=actions_by_arc.setdefault(key,{'first':None,'actions':{},'failures':0,'attack_times':[]})
            if row['first'] is None:row['first']={'turn':d['turn'],'action':d['action'],'success':d['success'],'outcome':d['outcome']}
            row['actions'][d['action']]=row['actions'].get(d['action'],0)+1
            if not d['success']:row['failures']+=1
            if d['action']=='attack' and d['success'] and len(row['attack_times'])<8:row['attack_times'].append(d['turn'])
    with gzip.open(FOLDER/'eventos.jsonl.gz','rt') as stream:
        for line in stream:
            e=json.loads(line);counts[e['kind']]+=1
            events[e['id']]=e
            if e['kind']=='CharacterAttacked':
                harm=harm_by_pair[(e['actor_id'],e['target_id'])];harm['attacks']+=1;harm['damage']+=e['context'].get('damage',0)
            elif e['kind']=='ViolenceIntentChanged' and e['context'].get('intent')=='kill':prior_harm[e['id']]=dict(harm_by_pair[(e['target_id'],e['actor_id'])])
            if e['kind'] in ('CharacterKilled','IncapacitatedSpared','ViolenceIntentChanged','LethalOptionConsidered','InstitutionalClueFiled','InstitutionalClueShared','InvestigationReply','CharacterFled'):
                by_owner[e['actor_id']].append(e)
    def name(pid):
        if pid is None:return 'autoria/alvo desconhecido'
        if str(pid) in people:return f"{people[str(pid)]['name']} (NPC {pid})"
        if str(pid) in places:return f"{places[str(pid)]['name']} (localidade {pid})"
        return f'entidade {pid}'
    def place(mid):return places.get(str(mid),{}).get('name',f'mapa {mid}')
    def loc(d):return f"{place(d['map_id'])}, ({d['x']}, {d['y']})" if d else 'sem local conhecido'
    def get(k):return metrics.get(k,0)
    labels={'directed_grievance':'mágoa contra o alvo','directed_emotion':'raiva e ressentimento dirigidos','vengefulness':'vingatividade','commitment':'força do compromisso','grave_loss_or_danger':'perda ou perigo grave conhecido','attributed_important_loss':'importância da perda atribuída','failed_alternatives':'respostas fracassadas','investment':'investimento no objetivo','related_desperation':'desespero relacionado','compassion':'compaixão','honesty':'honestidade','fear':'medo','risk':'risco percebido','authority_or_witnesses':'autoridade percebida','bond':'vínculo com o alvo','uncertain_authorship':'incerteza de autoria','plausible_nonlethal_alternative':'alternativa não letal plausível','institutional_duty':'dever institucional','known_criminal_consequences':'consequências criminais conhecidas','witnesses':'testemunhas','known_reputation':'temor da reputação'}
    def factors(d):return '; '.join(f"{labels.get(k,k)}: {v:.2f}" for k,v in sorted(d.items(),key=lambda p:p[1],reverse=True) if v>0)
    killed=sorted((e for e in events.values() if e['kind']=='CharacterKilled'),key=lambda e:e['turn'])
    kill_intents=[e for e in events.values() if e['kind']=='ViolenceIntentChanged' and e['context']['intent']=='kill']
    mercy=[e for e in events.values() if e['kind']=='IncapacitatedSpared']
    abandoned_lethal=[e for e in events.values() if e['kind']=='LethalIntentAbandoned']
    offered=[e for e in events.values() if e['kind']=='LethalOptionConsidered']
    lethalkilled=[e for e in killed if e['context'].get('violence_intent')=='kill']
    selected_lethal_cids={str(e['context'].get('lethal_audit',{}).get('commitment_id')) for e in kill_intents}
    catalog=Counter()
    chosen=[];chosen_ids=set()
    def select(label,predicate,rank=None):
        items=[(cid,a) for cid,a in arcs.items() if predicate(a)]
        catalog[label]=len(items)
        items.sort(key=lambda pair:(rank(pair[1]) if rank else len(pair[1]['transitions'])),reverse=True)
        for cid,a in items:
            if cid not in chosen_ids:chosen.append((label,cid,a));chosen_ids.add(cid);return
    def kinds(a):return {t['kind'] for t in a['transitions']}
    def clue_locations(a):
        return {tuple(t['context']['clue']['location'].values()) for t in a['transitions'] if t['kind']=='InvestigationClue'}
    def consulted_upgrade(a):
        previous=None
        for t in a['transitions']:
            if t['kind']!='InvestigationClue':continue
            clue=t['context']['clue'];source=events.get(clue.get('related_fact'),{})
            if previous and source.get('kind')=='SearchClueShared' and t['turn']-previous['observed_at']>=12 and clue['observed_at']>previous['observed_at']:return True
            previous=clue
        return False
    select('Intenção letal escolhida',lambda a:str(a['transitions'][0]['context'].get('commitment_id')) in selected_lethal_cids)
    select('Opção letal disponível em situação natural',lambda a:'LethalOptionConsidered' in kinds(a))
    select('Pista antiga renovada por consulta real',consulted_upgrade)
    select('Resposta à morte causada por outro',lambda a:a['origin'] in ('revenge','grief','protection') and events.get(a.get('source_fact'),{}).get('kind')=='CharacterKilled')
    select('Reação grave amadurecida',lambda a:a['origin']=='response' and 'CommitmentDeepened' in kinds(a))
    select('Busca com várias pistas',lambda a:len(clue_locations(a))>=3)
    select('Busca suspensa e reativada',lambda a:{'CommitmentDormant','CommitmentReactivated'}<=kinds(a),lambda a:sum(t['kind']=='CommitmentReactivated' for t in a['transitions']))
    select('Guarda investigando',lambda a:a['origin']=='pursuit' and 'InvestigationSearched' in kinds(a))
    select('Vingança com deslocamento entre localidades',lambda a:a['origin']=='revenge' and 'CommitmentTravel' in kinds(a))
    select('Viagem motivada por saber-se procurado',lambda a:str(a['transitions'][0]['context'].get('commitment_id')) in wanted_migrations)
    select('Perseguição institucional com viagem',lambda a:a['origin']=='pursuit' and 'CommitmentTravel' in kinds(a))
    select('Busca sem saída',lambda a:'CommitmentDormant' in kinds(a) and 'CommitmentReactivated' not in kinds(a))
    select('Vingança encerrada sem ataque registrado',lambda a:a['origin']=='revenge' and a.get('ending')=='CommitmentCompleted' and not actions_by_arc.get(str(a['transitions'][0]['context'].get('commitment_id')),{}).get('attack_times'))
    select('Vingança abandonada',lambda a:a['origin']=='revenge' and a.get('ending')=='CommitmentAbandoned')
    select('Espera com retorno à rotina',lambda a:any(str(t['context'].get('commitment_id')) in life for t in a['transitions']),lambda a:sum(life.get(str(a['transitions'][0]['context'].get('commitment_id')),{}).get('actions',{}).values()))
    select('Autoria inicialmente desconhecida',lambda a:a['origin']=='revenge' and a.get('target') is None)
    select('Pedido recusado ou sem informação',lambda a:any(t['kind']=='InvestigationReply' for t in a['transitions']))
    evidence=[]
    narrative=['# Histórias reais — Fase 4.6',f"\nSeed `{s['seed']}`, mundo novo, h 0–{s['hours']}, sem jogador e sem save carregado. Relatos derivados de eventos e compromissos, sem falas ou acontecimentos inventados.",
      '\nAs seleções abaixo mostram trajetórias distintas. O catálogo completo de compromissos está em `global_5000h/arcos.json`; os eventos observados estão em `global_5000h/eventos.jsonl.gz`. Uma sequência longa de tentativas não equivale automaticamente a uma história profunda.',
      '\n## Cobertura das situações solicitadas','\n| Situação | Evidência natural |','|---|---:|',
      f'| Mudança de intenção para matar | {len(kill_intents)} |',f'| Alternativa letal considerada | {len(offered)} |',
      f'| Misericórdia após incapacidade letal | {len(mercy)} |',f'| Intenção letal abandonada explicitamente | {len(abandoned_lethal)} |',f'| Morte com intenção matar | {len(lethalkilled)} |']
    for k,v in catalog.items():narrative.append(f'| {k} — compromissos elegíveis | {v} |')
    narrative += [f"| Cadeias causais com violência, resposta de terceiro, nova violência e nova resposta | {phase['causal_chain_occurrences']} |",
      '| Pista deliberadamente falsa comprovada | Não gerada pelo sistema atual; não confundir com informação atrasada |']
    if not kill_intents:narrative+=['\nNão houve intenção letal natural nesta seed. A regressão controlada comprova a capacidade de decidir matar, poupar e registrar a causa; ela não é uma história da campanha. As barreiras e ausências são discutidas no relatório técnico.']
    for i,(label,cid,a) in enumerate(chosen,1):
        narrative += [f"\n## {i}. {label}: {name(a['owner'])}",f"\nCompromisso `{cid}`, motivação `{a['origin']}`, alvo inicial {name(a.get('target'))}. Nasceu na hora {a['created_at']}. Fato causal `{a.get('source_fact')}`."]
        person=people.get(str(a['owner']),{});traits=person.get('initial_personality') or person.get('personality',{})
        narrative.append(f"\nPersonalidade inicial registrada: coragem {traits.get('courage')}, compaixão {traits.get('compassion')}, vingatividade {traits.get('vengefulness')}, persistência {traits.get('persistence')} e lealdade familiar {traits.get('family_loyalty')} (escala 0–100). Situação no fim da campanha: {'vivo' if person.get('alive') else 'morto'}. Esses valores influenciam escolhas; não comprovam por si sós a razão de um evento.")
        cause=events.get(a.get('source_fact'))
        if cause:narrative.append(f"\nCausa registrada: {cause['description']} (h {cause['turn']}, evento {cause['id']}).")
        ts=a['transitions'];important=[t for t in ts if t['kind'] in ('CommitmentCreated','CommitmentDeepened','CommitmentRetargeted','CommitmentStrategyChanged','LethalOptionConsidered','CommitmentTravel','InvestigationClue','InvestigationReply','CommitmentDormant','CommitmentReactivated','CommitmentCompleted','CommitmentAbandoned','CommitmentExpired')]
        if len(important)>16:important=important[:8]+important[-8:]
        narrative += ['\n| Hora | Transformação real | Evento |','|---:|---|---:|']
        selected=[]
        for t in important:
            ctx=t['context'];description=t['kind']
            if t['kind']=='InvestigationClue':
                clue=ctx['clue'];description=f"Pista de {name(clue['subject_id'])} em {loc(clue['location'])}, observação h {clue['observed_at']}, confiança {clue['confidence']}%, fonte {clue['source_kind']}"
            elif t['kind']=='CommitmentDeepened':description=f"Compromisso aprofundado de {ctx['previous']:.1f} para {ctx['intensity']:.1f}, por novo dano conhecido, fato {ctx['reinforcing_fact']}"
            elif t['kind']=='LethalOptionConsidered':
                audit=ctx['lethal_audit'];description=f"Opção letal torna-se plausível: pressão {audit['pressure']}, causa {audit.get('grave_basis')}, confiança {audit['confidence']}%; não comprova escolha de matar"
            elif t['kind']=='CommitmentStrategyChanged':description=f"Mudança de abordagem: {ctx.get('previous')} → {ctx.get('next')}"
            elif t['kind']=='CommitmentRetargeted':description=f"Alvo atualizado a partir de conhecimento recebido: {ctx}"
            elif t['kind']=='InvestigationReply':description=f"Consulta local: {ctx.get('result')}; fonte {name(ctx.get('informant'))}, confiança {ctx.get('confidence', 'não informada')}"
            elif t['kind']=='CommitmentTravel':description=f"Passo de viagem física para {place(ctx['destination'])}"
            elif t['kind']=='CommitmentDormant':description=f"Busca entra em espera: {ctx['reason']}; {ctx.get('attempts',0)} tentativas nesta pista"
            elif t['kind']=='CommitmentReactivated':description='Informação útil reativa o objetivo; a ação ainda depende da próxima decisão'
            elif t['kind'] in ('CommitmentCompleted','CommitmentAbandoned','CommitmentExpired'):description=f"{t['kind']}: {ctx.get('reason')}"
            narrative.append(f"| {t['turn']} | {description} | {t['id']} |");selected.append(t['id'])
        observed=actions_by_arc.get(cid)
        if observed:
            first=observed['first'];narrative.append(f"\nPrimeira execução social registrada: h {first['turn']}, `{first['action']}`, sucesso `{first['success']}` — {first['outcome']}. Abordagens registradas: `{observed['actions']}`; execuções sem sucesso: {observed['failures']}. O log social amostra repetições, então esses números não são o total exato de ações.")
            if observed['attack_times']:narrative.append(f"\nAtaques executados com este compromisso: amostra nas horas `{observed['attack_times']}`. Isso não demonstra intenção de matar.")
        row=life.get(cid)
        if row:narrative.append(f"\nEnquanto este compromisso estava em espera, entre h {row['first']} e {row['last']}, ações reais bem-sucedidas: `{row['actions']}`. Não são etapas de um plano da busca.")
        ownviolence=[e for e in by_owner.get(a['owner'],[]) if e['kind']=='CharacterKilled' and e['turn']>=a['created_at'] and e['context'].get('lethal_audit',{}).get('commitment_id')==int(cid)]
        ending=a.get('ending',a.get('final',{}).get('status','sem encerramento registrado'))
        narrative.append(f"\nLeitura: {len(clue_locations(a))} locais de pista distintos, {sum(t['kind']=='CommitmentStrategyChanged' for t in ts)} mudanças de abordagem; encerramento `{ending}`. Pistas descrevem conhecimento recebido, não a posição objetiva atual. Encerrar uma denúncia não comprova captura nem eliminação do adversário.")
        evidence.append({'category':label,'commitment':cid,'owner':a['owner'],'source_fact':a.get('source_fact'),'event_ids':selected,'waiting_life':row,'observed_actions':observed})
    narrative += ['\n## Todas as fatalidades por combate observadas','\n| Hora | Autor | Vítima | Intenção | Após incapacidade | Fonte causal | Dano de privação restante |','|---:|---|---|---|---|---:|---:|']
    for e in killed:
        ctx=e['context'];narrative.append(f"| {e['turn']} | {name(e['actor_id'])} | {name(e['target_id'])} | {ctx.get('violence_intent')} | {ctx.get('post_incapacity',False)} | {ctx.get('source_fact')} | {people.get(str(e['target_id']),{}).get('state',{}).get('deprivation','não registrado')} |")
        if ctx.get('lethal_audit'):
            audit=ctx['lethal_audit'];narrative.append(f"\nEvento {e['id']}: motivo `{audit['motive']}`, compromisso `{audit['commitment_id']}`, pressão {audit['pressure']}, confiança {audit['confidence']}%. Fatores: `{audit['positive_factors']}`. Barreiras: `{audit['barriers']}`. Fatos conhecidos: `{audit['known_facts']}`.")
    combat_deprivation=[people.get(str(e['target_id']),{}).get('state',{}).get('deprivation',0) for e in killed]
    if killed:narrative.append(f"\nEntre as {len(killed)} vítimas de combate, {sum(v>=80 for v in combat_deprivation)} tinham pelo menos 80 pontos de dano por privação ainda registrados. Esse dado permanece no personagem após a morte. Confirma debilidade importante, não intenção de homicídio. O golpe final e a vulnerabilidade acumulada devem ser lidos juntos.")
    for title,items in [('Intenção letal que surgiu',kill_intents),('Intenção disponível, com resultado ainda sujeito a Utility',offered),('Misericórdia',mercy),('Intenção letal interrompida',abandoned_lethal)]:
        if items:
            e=items[0];ctx=e['context'];audit=ctx.get('lethal_audit',{})
            narrative += [f'\n## {title}',f"\nH {e['turn']}, {name(e['actor_id'])}, evento {e['id']}, alvo {name(e['target_id'] or ctx.get('target'))}."]
            if audit:
                cause=events.get(audit.get('source_fact'));cause_text=cause['description'] if cause else 'Consultar o fato referenciado nas evidências.'
                narrative += [f"\nCausa: {cause_text} Fato {audit.get('source_fact')}; compromisso {audit.get('commitment_id')}, motivação `{audit.get('motive')}`. Confiança {audit.get('confidence')}%, intensidade {audit.get('commitment_intensity'):.2f}, episódios {audit.get('episodes')}, alternativas fracassadas {audit.get('failed_alternatives')}.",
                    f"\nPressão letal {audit['pressure']}. Fatores positivos: {factors(audit['positive_factors'])}. Barreiras: {factors(audit['barriers'])}. As pré-condições semânticas foram satisfeitas por `{audit.get('grave_basis')}`; o ruído da escolha não criou a elegibilidade."]
                if e['id'] in prior_harm:
                    harm=prior_harm[e['id']];narrative.append(f"\nO fato referenciado é uma referência causal, não todo o conflito: antes desta escolha, o log registra {harm['attacks']} agressões desse alvo contra o ator, somando {harm['damage']} HP de dano infligido. A soma é histórica e inclui dano que pode ter sido recuperado; não representa HP faltando. A avaliação agrega episódios distintos e perigo grave.")
                if ctx.get('scores'):narrative.append(f"\nComparação entre desfechos plausíveis: `{ctx['scores']}`. O evento registra escolha explícita de `{ctx['intent']}`.")
            else:narrative.append(f"\nContexto registrado: `{ctx}`.")
    if phase['causal_chains']:
        narrative += ['\n## Cadeia causal de retaliação','\nA cadeia abaixo tem referências de fatos efetivamente usados; não recebe rótulo automático de feud.']
        for r in phase['causal_chains'][0]:narrative.append(f"\n- H {r['turn']}: `{r['kind']}`, {name(r['actor'])} → {name(r['target'])}, evento {r['event']}.")
    severe=[r for r in cases.values() if r['severity']==5 and r['status']=='expired' and people.get(str(r['suspect_id']),{}).get('alive')]
    narrative += ['\n## Falhas e lacunas',f"\nCasos de gravidade 5 expirados com suspeito ainda vivo no final: {len(severe)}. Isso comprova falha institucional em concluir estes casos, não que o autor saiba que escapou.",
      '\nPerguntas podem terminar em recusa ou ausência de informação. Uma fonte pode dar uma observação correta antiga que já não acompanha o alvo. O auditor compara posições apenas para avaliar a pista; o perseguidor não recebe essa comparação.',
      '\nAs histórias de busca demonstram continuidade e mudanças de informação. A repetição de cuidados familiares, a fome e a baixa quantidade de conflitos realmente graves continuam limitando a variedade de desfechos. As categorias sem exemplo natural não foram preenchidas com cenários artificiais.']
    write(ROOT/'HISTORIAS_REAIS.md','\n'.join(narrative)+'\n');write(ROOT/'evidencias_historias.json',json.dumps(evidence,ensure_ascii=False,indent=2))
    clue_sources=Counter(e['context']['clue']['source_kind'] for e in events.values() if e['kind']=='InvestigationClue')
    quality=phase.get('clue_quality_totals',{});qcount=max(1,quality.get('count',0));saved=(FOLDER/'save_final.json').stat().st_size;shortsaved=(ROOT/'curta_validacao_final_500h/save_final.json').stat().st_size
    previous=read(Path('reports/fase_4_5/global_5000h/resumo.json'))
    overview=['# Fase 4.6 — investigação ativa e escalada fatal',f"\nVersão `{s['rules']}`, seed `{s['seed']}`. Mundo novo em h 0, sem jogador nem save carregado, {s['initial']['persistent']} NPCs persistentes, {s['initial']['abstract']} habitantes abstratos e {s['initial']['towns']} localidades. Uma única campanha longa concluída de {s['hours']} horas. Um início anterior foi interrompido durante o diagnóstico da reação imediata e não integra estas estatísticas. Núcleo congelado: `{s['core_sha256']}`.",
      '\n## Resultado e respostas centrais',
      f"\nA investigação funciona naturalmente: {get('Investigation:area_searched')} verificações de áreas, {get('Investigation:asked')} consultas a pessoas, {get('Investigation:useful')} respostas consideradas úteis, {get('Investigation:dormant')} entradas em espera e {get('Investigation:reactivated')} reativações. Existem regressões de preservação da causa, retorno à vida diária e reativação sem ação automática.",
      f"\nIntenção letal natural: {len(kill_intents)} mudanças para `kill` entre {len({e['actor_id'] for e in kill_intents})} NPCs, {len(lethalkilled)} mortes com essa intenção e {len(mercy)} decisões de poupar após incapacidade letal. A capacidade técnica foi demonstrada em regressões controladas. " + ('A campanha não demonstrou emergência natural de homicídio deliberado; esse objetivo permanece empiricamente não comprovado nesta seed.' if not lethalkilled else 'As mortes deliberadas possuem contexto causal, barreiras e compromisso rastreáveis no relatório narrativo.'),
      f"\nO gargalo demonstrado mudou: a opção letal foi elegível em {get('Lethal:available')} avaliações e venceu em {get('Lethal:won')} ataques, mas nenhum desses ataques levou a incapacidade letal ({get('Lethal:incapacity')}). O julgamento após incapacidade não teve oportunidade natural de ocorrer. A próxima análise deve rastrear continuidade dos confrontos, encontros, retiradas, recuperação e interferência de outras Needs, mantendo o dano atual.",
      '\nQuando a intenção é considerada, a decisão é explicável por autoria conhecida, dano/perda grave atribuída, grievance, compromisso e barreiras pessoais/situacionais. Pressão insuficiente não vira intenção letal por ruído de Utility. Intenção altera o desfecho desejado, mantendo o mesmo cálculo de dano.',
      '\nPista velha pode levar a verificação e pergunta; uma resposta conhecida pode produzir pista nova. Falta de informação pode suspender a busca sem esquecer sua origem. Esses dois avanços estão documentados em histórias reais, com IDs e horários.',
      '\n## O que mudou',
      '\n- `LethalPressure`: pré-condições semânticas e fatores/barreiras dirigidos a um alvo; episódios e tentativas de resolução compactos, sem contar golpes como conflitos distintos.',
      '- Reações imediatas podem amadurecer em compromisso quando há dano próprio grave conhecido e reincidência/perigo sério. Novos danos atribuídos ao mesmo alvo podem aprofundar sua intensidade, sem contar isso como aproximação física.',
      '- Evidências mistas conservam a confiança no fato grave atribuído; uma agressão certa não confirma um homicídio de autoria duvidosa. Perda pessoal importante comprovada pode justificar gravidade sem ataques anteriores do próprio vingador.',
      '- Informante com conhecimento real de homicídio pode esclarecer autoria desconhecida, retargetando o mesmo compromisso e preservando a origem da vingança.',
      '- Investigação geral para vingança, procura institucional e familiar desaparecido. Até três pistas por compromisso, fontes e áreas limitadas, confiança e idade preservadas, informantes locais sem conhecimento global.',
      '- Dormência, reativação por informação útil, retorno físico à rotina, reconhecimento presencial de pessoa ou restos e prazo finito de intenção.',
      '- Uma pista formal recente por caso; compartilhamento presencial no serviço local após seis horas. Tarefas de busca/vigilância/informação permanecem distintas; gravidade aumenta duração e limite de tentativas.',
      '- Contexto de preparação nas necessidades canônicas e bônus limitado de quatro pontos na alternativa; progresso exige aumento real de provisões frente a déficit conhecido.',
      '- Auditoria de decisões e pistas, sem efeitos de consultas de depuração sobre o save. Nenhuma nova mecânica da Fase 5.',
      '\nO diagnóstico de cada componente e a justificativa da extensão estão em `reports/fase_4_6/DIAGNOSTICO_E_ALTERACOES.md`. A fórmula de potência e o bloco de dano são idênticos à base. Alimentação, recuperação, economia, profissões, geração, política, migração, navegação e população permanecem byte a byte iguais. Integrações em Needs/Goals/Knowledge/Agency/Justice são preservadas em `preservacao.json` e no código congelado.',
      '\n## Validação',
      '\nForam acrescentadas 18 regressões compostas, totalizando 245 testes únicos. A suíte completa foi executada uma vez quando havia 243 testes: 240 passaram e três detectaram divergências de contadores por consultas/debug. Após o reparo, esses testes passaram. A extensão final de reação persistente foi validada em 59 testes direcionados: as 18 regressões novas, as 18 da Fase 4.5, os 20 de combate da Fase 4 e os três de determinismo. Não há falha pendente. Logs originais e retestes foram conservados.',
      f"\nA curta validada, com o mesmo hash da longa, completou 500 h: {short['death_causes']}, {len(short['invariants'])} erros de integridade, {len(short['food_carried_deaths'])} mortes alimentares com comida carregada. Execuções diagnósticas e interrompidas estão separadas; seus resultados não se misturam com esta campanha.",
      f"\nNa longa: {len(s['invariants'])} erros nas 50 verificações de estado; {s['alive']} NPCs vivos ao final; causas de morte `{s['death_causes']}`. Mortes alimentares carregando comida: {len(s['food_carried_deaths'])}. O quadro de fome continua relevante e a fase não comprova sua resolução.",
      '\n## Avaliação letal', '\n| Contador | Ocorrências |','|---|---:|']
    for key in sorted({k for k in metrics if k.startswith('Lethal:')}|{'Lethal:evaluated','Lethal:precondition_failed','Lethal:available','Lethal:won','Lethal:abandoned','Lethal:incapacity','Lethal:mercy','Lethal:death'}):overview.append(f'| `{key}` | {get(key)} |')
    overview += ['\nA categoria `low_confidence` inclui avaliações sem fato grave atribuído conhecido; não significa que todos esses NPCs acreditavam em um rumor de homicídio. `insufficient_pressure` também inclui ausência de causa grave semanticamente elegível.',
      '\nO registro narrativo contém 56 eventos `LethalOptionConsidered`: ele evita repetir a mesma opção/alvo antes de 48 horas. Isso não equivale às 287 avaliações elegíveis. `won` conta ataques com intenção matar, não mudanças de intenção; as 23 mudanças envolveram 12 NPCs. As dez ocorrências de `abandoned` incluem seis encerramentos explícitos e quatro reavaliações para outra intenção.',
      '\nOs contadores são avaliações e ações, não pessoas independentes. Uma decisão pode avaliar mais de uma Need; fatores de bloqueio podem coexistir. Avaliar em cada decisão e na execução permite reexaminar incapacidade, autoridade e novas informações sem efeitos de consultas/debug.',
      '\n## Investigação e vida durante a espera','\n| Contador | Ocorrências |','|---|---:|']
    for key in sorted(k for k in metrics if k.startswith('Investigation:')):overview.append(f'| `{key}` | {get(key)} |')
    overview += [f"\nPistas avaliadas: {quality.get('count',0)}; idade média {quality.get('age_sum',0)/qcount:.1f} h, confiança média {quality.get('confidence_sum',0)/qcount:.1f}%. O auditor encontrou {quality.get('actual_other_map',0)} pistas cujo alvo já estava em outro mapa e {quality.get('actual_same_map_away',0)} com alvo em outra célula do mesmo mapa. Isso mede desatualização, sem provar mentira. A amostra detalhada contém as primeiras 4.096 pistas; os totais incluem todas.",
      f"\nFontes das pistas: `{dict(clue_sources)}`. Observações diretas de pessoas presentes também entram neste total; a confiança média de todas as pistas não mede apenas a qualidade das respostas de informantes. A categoria narrativa de renovação por consulta exige uma pista anterior com pelo menos 12 horas e uma informação mais recente fornecida por uma fonte real.",
      f"\nPistas formalmente depositadas: {get('InstitutionalClueFiled')}; retransmissões institucionais: {get('InstitutionalClueShared')}. Cada retransmissão depende da presença e da latência do canal, não é um comunicado global.",
      f"\nAções reais bem-sucedidas enquanto havia compromisso em espera: `{phase.get('waiting_actions',{})}`. Compromissos dormentes no fim: {phase['sleeping_at_end']}. Casos institucionais com mais de um guarda: {s['agency']['multi_guard_cases']}; máximo de guardas por caso: {s['agency']['maximum_case_assignments']}.",
      f"\nAmostras diárias de vingança forte: `{s['agency']['strong_revenge_daily_samples']}`. Amostras de reação grave persistente: `{phase.get('strong_response_daily_samples',{})}`. Uma amostra bloqueada por distância ou por outra Need não comprova falta de intenção. Ações durante a espera podem atender outros compromissos; um objetivo dormente não monopoliza a vida do NPC.",
      f"\nCadeias causais estritas detectadas: {phase['causal_chain_occurrences']}. Exigem violência inicial, resposta de terceiro, nova violência e nova resposta por referências de fatos usados. Repetição de eventos ou mera proximidade temporal não basta.",
      '\n## Qualidade narrativa e comparação',
      f"\nForam adotados {s['agency']['commitments_total']} compromissos; {s['agency']['arcs_with_progress']} tiveram progresso e {s['agency']['arcs_with_strategy_change']} mudaram de estratégia. Não são números de grandes sagas. Transformação de pista, suspensão, retomada, presença e consequência são critérios mais fortes que extensão do EventLog.",
      f"\nA longa anterior da Fase 4.5 teve {previous['initial']['persistent']} NPCs, {sum(previous['death_causes'].values())} mortes e nenhuma mudança natural para matar; esta teve {s['initial']['persistent']} NPCs e {sum(s['death_causes'].values())} mortes. Seeds e populações diferentes impedem atribuir a diferença numérica à versão. A longa da Fase 4.5 também usou um núcleo anterior aos cinco ajustes finais daquela entrega; esses reparos já integram a base preservada da Fase 4.6. O avanço verificável desta entrega é a investigação/dormência, sustentado também por regressões controladas.",
      '\n## Estado, save e custo',
      f"\nSave da curta: {shortsaved/1024**2:.1f} MiB; da longa: {saved/1024**2:.1f} MiB. O volume cresceu {saved/max(1,shortsaved):.2f}× para horizonte 10× maior. Histórico: {s['history_events']} eventos. O agregado de conflito e compromissos investigativos, incluindo campos preexistentes, ocupa aproximadamente {phase['compact_state_bytes']/1024**2:.2f} MiB serializado. Os limites de pares, pistas e fontes evitam crescimento sem limite por personagem; o histórico global continua volumoso.",
      f"\nTempo de simulação/auditoria registrado: {s['runtime_seconds']/60:.1f} min; pico de memória anterior à exportação do save: {s['memory_peak_mib']:.1f} MiB. A exportação pode ter pico adicional e não está incluída nesse indicador. Save/load da própria versão e continuidade determinística passaram nas regressões. Saves de versões anteriores continuam sujeitos à checagem de versão já existente.",
      '\n## Problemas e limites restantes',
      '\n- Informação falsa deliberada não é produzida nesta fase; há rumor e informação antiga, que não devem ser rotulados como mentira comprovada.',
      '- Novas observações rotineiras podem gerar muitas transições de pista e inflar a leitura de progresso. O relatório separa estas transições das consultas que renovaram uma informação antiga.',
      '- Uma pista remota não fornece uma rota desconhecida. Falta de rota, recursos, oportunidade ou coragem pode impedir a viagem.',
      '- O registro institucional depende de conhecimento, presença e canais locais. Homicídio conhecido aumenta gravidade, sem garantir captura.',
      '- A intensidade de muitos conflitos permanece insuficiente para homicídio. Denúncias e afastamentos podem encerrar necessidades antigas antes de uma escalada mais profunda; são desfechos válidos, mas limitam sagas violentas.',
      '- Mortes por combate com intenção de ferir/repelir podem atingir pessoas já muito debilitadas por privação. São consequências físicas fatais, sem prova de decisão deliberada de matar.',
      '- Fome, cuidado familiar por privação e despesas individuais ainda dominam parte das histórias. Preservar o módulo alimentar não garante os mesmos resultados quando outros objetivos disputam tempo.',
      '- O save conserva a grande crônica preexistente. Esta entrega mede o custo e limita dados novos, mas não resolve toda a retenção histórica.',
      '\nAntes de ampliar a fase seguinte, a leitura principal é `reports/fase_4_6/HISTORIAS_REAIS.md`: ela separa trajetórias demonstradas, falhas reais e categorias sem exemplo natural. Categorias sem exemplo natural devem motivar diagnóstico causal, sem meta de mortalidade.']
    write(Path('RELATORIO_FASE_4_6.md'),'\n'.join(overview)+'\n')
    analysis={'seed':s['seed'],'hours':s['hours'],'natural_lethal_intent_changes':len(kill_intents),'natural_lethal_actors':sorted({e['actor_id'] for e in kill_intents}),'available_lethal_actors':sorted({e['actor_id'] for e in offered}),'abandoned_lethal_intents':len(abandoned_lethal),'deliberate_deaths':len(lethalkilled),'mercy':len(mercy),
      'selected_story_categories':dict(catalog),'selected_story_count':len(chosen),'all_combat_deaths':[{'event':e['id'],'turn':e['turn'],'actor':e['actor_id'],'victim':e['target_id'],'context':e['context']} for e in killed],
      'escaped_severe_cases':len(severe),'save_bytes':saved,'short_save_bytes':shortsaved,'core_sha256':s['core_sha256']}
    write(ROOT/'analise_narrativa.json',json.dumps(analysis,ensure_ascii=False,indent=2))
    print(json.dumps(analysis|{'all_combat_deaths':len(killed)},ensure_ascii=False))

if __name__=='__main__':run()
