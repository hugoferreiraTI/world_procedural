"""Relatórios derivados da auditoria. Não executa nem altera decisões do mundo."""
import argparse,gzip,json
from collections import Counter,defaultdict
from pathlib import Path

LABELS=['grupo formado por privação','grupo que conseguiu proposta e se dissolveu',
 'proposta recusada que aumentou tensão','grupos antagonistas','grupo que amadureceu em facção',
 'prefeito reagindo a pressões diferentes','general/militares pressionando autoridade','promoção em facção',
 'fé atravessando região','rumor espiritual','intervenção conhecida de formas diferentes',
 'mortal divinizado socialmente sem ser Deus','personagem ganhando epíteto',
 'epítetos diferentes em regiões distintas','MythicTrait produzindo trajetória',
 'MythicTrait sem grande arco','item ganhando importância histórica','intenção letal situacional',
 'execução deliberada','misericórdia após oportunidade de execução','morte alterando a vida do autor',
 'caso político/religioso inacabado']

def read(path):return json.loads(path.read_text())

def generate(folder,output):
    folder=Path(folder);output=Path(output)
    s=read(folder/'resumo.json');p5=s['phase5'];people=read(folder/'personagens_fase5.json')
    initial=read(folder/'personagens_iniciais.json');cities=read(folder/'cidades.json')
    institutions=read(folder/'instituicoes.json');arcs=read(folder/'arcos_grupos.json')
    with gzip.open(folder/'eventos.jsonl.gz','rt',encoding='utf-8') as f:events=[json.loads(line) for line in f]
    extra=folder/'eventos_adicionais.json'
    if extra.exists():events.extend(read(extra))
    events=list({e['id']:e for e in events}.values());events.sort(key=lambda e:(e['turn'],e['id']))
    byid={e['id']:e for e in events};kinds=defaultdict(list)
    for e in events:kinds[e['kind']].append(e)
    names={int(i):p['name'] for i,p in people.items()}
    names.update({int(i):v['name'] for i,v in institutions['divinities'].items()})
    names.update({int(i):v['name'] for i,v in institutions['factions'].items()})
    names.update({int(i):v['name'] for i,v in institutions['groups'].items()})
    names.update({int(i):v['name'] for i,v in cities.items()})
    solutions={'arms_funding':'armamento da guarda','food_distribution':'distribuição de comida',
        'security_funding':'financiamento da segurança','temporary_work':'trabalho temporário',
        'recognize_cult':'reconhecimento de culto','restrict_cult':'restrição de culto'}
    for e in kinds['PolicyDecided']:
        names[e['target_id']]='Proposta de '+solutions.get(e['context']['solution'],e['context']['solution'])
    def who(id):return '—' if id is None else f"{names.get(id,'Entidade')} (#{id})"
    def source(events):
        events=list({e['id']:e for e in events}.values())
        rows=['','| Hora | Acontecimento | Autor | Alvo | ID do fato |','|---:|---|---|---|---:|']
        for e in events[:8]:rows.append(f"| {e['turn']} | {e['kind']} | {who(e['actor_id'])} | {who(e['target_id'])} | {e['id']} |")
        return '\n'.join(rows)
    cases={};evidence={};notes={}
    def add(n,text,seq=()):
        seq=list({e['id']:e for e in seq}.values())
        cases[n]=text+source(seq) if seq else text
        evidence[n]=[e['id'] for e in seq]
    formed=kinds['GroupFormed'];economical=[e for e in formed if e['context']['cause']=='resource_pressure']
    if economical:
        e=max(economical,key=lambda e:len(arcs.get(str(e['target_id']),{}).get('events',[])))
        root=byid.get(e['context']['source_fact']);gid=e['target_id']
        town=cities.get(str(e['location']['map_id']),{})
        chain=[r for r in events if r['context'].get('group_id')==gid or r['target_id']==gid]
        add(1,f"{who(e['actor_id'])} liderou um grupo que começou com {len(e['context']['members'])} participantes, em {town.get('name')} ({town.get('kind')}). A origem registrada foi pressão econômica comunicada. Fonte da iniciativa: fato #{e['context']['source_fact']}; necessidade #{e['context']['originating_need']}. Adesões posteriores e a existência do grupo não demonstram solução da privação.",([root] if root else [])+[e]+chain[:5])
    accepted=[e for e in kinds['GroupDissolved'] if e['context'].get('reason')=='proposal_accepted']
    if accepted:
        e=accepted[0];gid=e['target_id'];chain=[r for r in events if r['context'].get('group_id')==gid]
        add(2,'O grupo encerrou sua finalidade depois de receber uma aprovação. Dissolução é consequência registrada; não prova que todos os problemas econômicos dos membros desapareceram.',chain[-5:]+[e])
    rejected=[e for e in kinds['PolicyDecided'] if e['context']['result']['decision']=='reject']
    for e in rejected:
        readers=[r for r in kinds['PolicyRead'] if e['id'] in r['context'].get('source_facts',[])]
        protests=[r for r in kinds['GroupProtested'] if r['context'].get('group_id')==e['context']['group_id'] and r['turn']>=e['turn']]
        if readers or protests:
            add(3,'Uma recusa ficou pública e foi consultada pelo representante, ou foi seguida por protesto do grupo. A pressão depende de receber a resposta; a decisão remota sozinha não informa os membros.',[e]+readers[:2]+protests[:2]);break
    hostile=[(i,g) for i,g in institutions['groups'].items() if g['grievances']]
    if hostile:
        id,g=hostile[0];seq=[byid[v['source_fact']] for v in g['grievances'].values() if v['source_fact'] in byid]
        others=[(i,institutions['groups'][i]) for i in g['grievances'] if i in institutions['groups']]
        detail=' '.join(f"O grupo #{i}, liderado por {who(other['leader_id'])}, conservava {len(other['member_ids'])} membros e {'também registrava agravo contra o primeiro' if str(id) in other['grievances'] else 'era alvo do agravo'}; seu status final era `{other['status']}`." for i,other in others)
        add(4,f"**{g['name']}** (#{id}), liderado por {who(g['leader_id'])}, terminou com {len(g['grievances'])} agravamentos contra outros grupos e status `{g['status']}`. Os agrupamentos interpretaram agressões conhecidas contra seus membros. {detail} São interpretações de fatos conhecidos; não demonstram guerra entre grupos nem ataque comandado pela organização.",seq)
    elif s['metrics'].get('Society:group_antagonism',0):
        add(4,f"O contador registrou {s['metrics']['Society:group_antagonism']} interpretações de antagonismo. O recorte final não conserva um par completo de grupos; isso não será apresentado como guerra ou saga reconstruída.")
    if kinds['FactionFounded']:
        e=kinds['FactionFounded'][0];gid=e['context']['group_id'];g=next((r for r in formed if r['target_id']==gid),None)
        add(5,f"Uma organização foi fundada por {who(e['actor_id'])}, a partir do grupo #{gid}. O evento registra propósito `{e['context']['purpose']}`, {len(e['context']['members'])} membros e contribuição real de {e['context']['cost']} moedas.",([g] if g else [])+[e])
    decisions=defaultdict(list)
    for e in kinds['PolicyDecided']:decisions[e['actor_id']].append(e)
    for id,seq in decisions.items():
        if len({r['context']['solution'] for r in seq})>=2:
            choices=[];seen=set()
            for e in seq:
                if e['context']['solution'] not in seen:seen.add(e['context']['solution']);choices.append(e)
            outcomes=[]
            for e in choices:
                result=e['context']['result'];material=result['material']
                recipients=', '.join(who(i) for i in material.get('recipients',[])) or 'nenhum'
                outcomes.append(f"Na hora {e['turn']}, respondeu `{result['decision']}` ao pedido de {solutions.get(e['context']['solution'],e['context']['solution'])}: {material.get('food',0)} comida, {material.get('money',0)} moedas, destinatários {recipients}"+(f", arma #{material['weapon_id']}" if material.get('weapon_id') else '')+'.')
            add(6,f"{who(id)} respondeu a pressões diferentes. "+' '.join(outcomes)+" Os destinatários são os realmente atendidos; se a autoridade aparece nessa lista, a transferência não será descrita como ajuda a outro morador. Cada decisão conserva suas pontuações contextuais e custos.",choices);break
    for e in kinds['ProposalSubmitted']:
        g=next((r for r in formed if r['target_id']==e['context']['group_id']),None)
        if g and any(initial.get(str(i),{}).get('profession') in ('guarda','soldado') for i in g['context']['members']):
            add(7,'Um grupo com participação militar apresentou demanda à autoridade civil. Isso demonstra interesse local e representação; não é mobilização de exército nem golpe nacional.',[g,e]);break
    if kinds['FactionPromoted']:add(8,'O membro recebeu promoção formal. As regras exigem serviço relevante, relação com liderança, permanência e vaga; dinheiro ou XP isolado não bastam.',kinds['FactionPromoted'][:3])
    roots=defaultdict(list)
    for e in kinds['SpiritualReport']:roots[e['context'].get('source_fact')].append(e)
    for id,seq in roots.items():
        if len({r['location']['map_id'] for r in seq if r['location']})>=2:
            add(9,f"A interpretação do mesmo fato #{id} foi expressa em mais de uma localidade. Isso registra circulação do relato; não prova conversão de toda uma região.",seq[:4]);break
    if kinds['SpiritualReport']:
        e=kinds['SpiritualReport'][0];root=byid.get(e['context'].get('source_fact'))
        add(10,f"{who(e['actor_id'])} transmitiu uma interpretação `{e['context'].get('interpretation')}`. A alegação refere-se ao sujeito #{e['context'].get('believed_subject')}; confiança declarada {e['context'].get('confidence')}. O receptor continua sujeito ao limite de rumor de 30%, e a ontologia divina não muda.",([root] if root else [])+[e])
    for row in p5['interpretations']:
        beliefs=[r for r in row['observers'] if r['belief']]
        if len({r['belief']['interpretation'] for r in beliefs})>=2:
            detail='; '.join(f"{r['name']} (#{r['observer']}, devoção {r['devotion']}): {r['belief']['interpretation']}" for r in beliefs[:6])
            add(11,f"Um mesmo acontecimento produziu classificações diferentes: {detail}. São campos de crença registrados, não pensamentos inventados.",[row['event']]);break
    if p5['believed_divine_mortals']:
        id=p5['believed_divine_mortals'][0]
        followers=[(i,p['beliefs'].get(str(id))) for i,p in people.items() if p['beliefs'].get(str(id),{}).get('believed_divine')]
        details='; '.join(f"{people[i]['name']} (#{i}): interpretação {b.get('interpretation')}, confiança {b.get('confidence')}, fato #{b.get('source_fact')}" for i,b in followers[:5])
        seq=[byid[b['source_fact']] for _,b in followers if b.get('source_fact') in byid]
        add(12,f"{who(id)} era considerado divino por {len(followers)} observadores registrados. Divindade objetiva do mortal: {'sim' if id in p5['actual_divine_mortals'] else 'não'}. Crenças retidas: {details}. A veneração permanece subjetiva, sem transformação automática.",seq[:3])
    elif s['metrics'].get('Renown:mortal_venerated',0):
        add(12,f"O contador registrou {s['metrics']['Renown:mortal_venerated']} atualizações de veneração mortal, mas nenhuma crença correspondente permaneceu no recorte final. A identidade e o arco não podem ser reconstruídos com segurança a partir desse contador. Houve sinal do mecanismo natural, sem exemplo narrativo completo.")
    for observer,p in people.items():
        record=next(((int(i),r) for i,r in p['renown'].items() if r['epithet']),None)
        if record:
            id,r=record;seq=[byid[int(i)] for i in r['facts'] if int(i) in byid]
            add(13,f"Para {p['name']} (#{observer}), {who(id)} ficou conhecido como **{r['epithet']}**. Domínios registrados: {r['domains']}. IDs dos fatos conservados no renome: {list(r['facts'])}. Alguns fatos já não estão no recorte de eventos/conhecimento final. O título é avaliação social, sem concessão automática de habilidade ou divindade.",seq[:4]);break
    for id,p in people.items():
        titles=p['social_state'].get('regional_epithets',{})
        if len({v.split(' de ')[0] for v in titles.values()})>=2:
            add(14,f"{p['name']} (#{id}) recebeu caracterizações de naturezas diferentes conforme os observadores regionais: {titles}. Esta diferença vem de feitos conhecidos, não de um título global imposto.");break
    mythic=sorted(((i,p) for i,p in people.items() if p['mythic']),key=lambda row:row[1]['development'],reverse=True)
    for id,p in mythic:
        seq=[e for e in kinds['PowerTrained'] if e['actor_id']==int(id)]
        if seq:
            selected=seq[:2]+seq[-1:]
            aspiration=[{'status':a['status'],'progress':a['progress']} for a in p['aspirations'] if a['domain']=='become_stronger']
            add(15,f"{p['name']} (#{id}), com potencial **{p['mythic']}**, desenvolveu a capacidade até {p['development']}/100. O treino consome fome e cansaço; sobrevivência final: `{p['alive']}`, HP {p['state']['hp']}, dinheiro {p['state']['money']}. Aspiração de poder ao fim: {aspiration}. Isso é uma trajetória de desenvolvimento, sem presumir heroísmo, saga ou ascensão.",selected);break
    exceptional={'FactionFounded','DivinityKilled','Apotheosis','TerminalDecision'}
    for id,p in mythic:
        feats=[e for e in events if e['actor_id']==int(id) and e['kind'] in exceptional]
        if not feats and p['development']==0:
            add(16,f"{p['name']} (#{id}) tinha potencial **{p['mythic']}**, mas terminou com desenvolvimento zero e nenhum dos feitos excepcionais examinados. Sobrevivência final: `{p['alive']}`. Ausência de saga não é, por si, bug.");break
    for id,item in institutions['items'].items():
        important=[byid[i] for i in item['important_events'] if i in byid]
        if important:
            add(17,f"O item #{id}, **{item['name']}**, ganhou o título histórico `{item['historical_title']}`. Qualidade {item['quality']}, proprietário #{item['owner_id']}, donos anteriores {item['previous_owners']}, propriedades físicas {item['actual_properties']}. A relevância histórica não cria efeito mágico automaticamente.",important[:4]);break
    situational=[e for e in kinds['ViolenceIntentChanged'] if e['context'].get('intent')=='kill' and e['context'].get('lethal_audit',{}).get('mode')=='situational']
    if situational:
        e=situational[0];a=e['context']['lethal_audit'];seq=[byid[i] for i in a['known_facts'] if i in byid]
        add(18,f"{who(e['actor_id'])} passou a intenção situacional de matar diante de ameaça recente. Pressão calculada {a['pressure']}; barreiras {a['barriers']}. Intenção não equivale a execução.",seq+[e])
    fatal=[e for e in kinds['CharacterKilled'] if e['context'].get('death_context')=='deliberate_finish']
    if fatal:
        e=fatal[0];seq=[r for r in events if r['actor_id']==e['actor_id'] and r['target_id']==e['target_id'] and r['turn']<=e['turn'] and r['kind'] in ('CharacterAttacked','ExecutionOpportunity','TerminalDecision')]
        add(19,f"{who(e['actor_id'])} concluiu a finalização deliberada de {who(e['target_id'])}. A decisão terminal validou presença, incapacidade e intenção; o desfecho foi fatal sem repetir dano aleatório.",seq[-5:]+[e])
    for e in kinds['IncapacitatedSpared']:
        opportunity=next((r for r in reversed(kinds['ExecutionOpportunity']) if r['actor_id']==e['actor_id'] and r['target_id']==e['target_id'] and r['turn']<=e['turn']),None)
        if opportunity and opportunity['context'].get('expires_at',opportunity['turn']+6)>e['turn']:
            add(20,f"{who(e['actor_id'])} poupou {who(e['target_id'])} durante a oportunidade terminal. A vida foi preservada; grievance e consequências anteriores não são apagadas por essa decisão.",[opportunity,e]);break
    for e in kinds['CharacterKilled']:
        consequences=[r for r in kinds['WantedIssued'] if r['context'].get('source_fact')==e['id']]
        if consequences:
            add(21,f"A morte causada por {who(e['actor_id'])} originou procura institucional vinculada ao fato. Isso é uma alteração documentada da vida do autor; não será presumida culpa psicológica sem registro próprio.",[e]+consequences[:3]);break
    wanted_path=folder/'procura_final.json'
    if 21 not in cases and wanted_path.exists():
        records=read(wanted_path)
        for e in kinds['CharacterKilled']:
            linked=[r for r in records if r['suspect_id']==e['actor_id'] and
                    (r['originating_fact']==e['id'] or (r['institutional_fact'] or {}).get('event_id')==e['id'])]
            if linked:
                r=linked[0]
                informed=[int(i) for i,fact_id in r['known_facts'].items() if fact_id==e['id']]
                add(21,f"{who(e['actor_id'])} ({people[str(e['actor_id'])]['profession']}) matou {who(e['target_id'])} ({people[str(e['target_id'])]['profession']}). Intenção registrada: `{e['context'].get('violence_intent')}`; dano final {e['context'].get('damage')}. A morte foi incorporada ao registro institucional #{r['id']}, aberto na hora {r['created_at']} e encerrado como `{r['status']}` na hora {r['resolved_at']}; gravidade final {r['severity']}. Guardas que tinham este homicídio como fato conhecido do caso: {[who(i) for i in informed]}. A lista geral de pessoas cientes {r['known_by']} também pode incluir suspeito e vítima, e não equivale à lista de investigadores. O registro começou com outro fato e foi agravado pela morte. Expiração não prova absolvição, e não será presumida culpa psicológica.",[e]);break
    pending=[(i,g) for i,g in institutions['groups'].items() if g['status']=='active' and g['proposal_ids']]
    if pending:
        id,g=pending[0];states={i:g['proposal_knowledge'].get(str(i),{}) for i in g['proposal_ids']}
        add(22,f"O grupo **{g['name']}** (#{id}) continuava ativo, sob liderança de {who(g['leader_id'])}. Conhecimento sobre suas propostas: {states}. Caso aberto não receberá final inventado.")
    abandoned=[(i,p) for i,p in institutions['proposals'].items() if p['status']=='draft' and institutions['groups'].get(str(p['group_id']),{}).get('status')!='active']
    if 22 not in cases and abandoned:
        id,p=abandoned[0];g=institutions['groups'].get(str(p['group_id']),{})
        notes[22]=f"Não ficou um caso ativo com representação suficiente para esta categoria. O rascunho #{id}, `{p['solution']}`, criado na hora {p['created_at']}, continuava armazenado, mas o grupo **{g.get('name')}** já estava `{g.get('status')}`. É um encaminhamento interrompido e uma ambiguidade de status até a limpeza dos registros encerrados; não será apresentado como política em andamento."
    lines=[f"# Histórias reais — Fase 5 — {s['hours']:,} horas".replace(',','.'),
        f"\nSeed **{s['seed']}**; regras `{s['rules']}`; mundo iniciado em zero, sem jogador, sem save anterior e sem história de aquecimento. Código: `{s['core_sha256']}`.",
        '\nEste relatório seleciona evidências das 22 categorias solicitadas. Eventos repetidos não são tratados como sagas. Os microcenários controlados estão em arquivo separado e não entram nestes exemplos.',
        f"\nForam documentadas {len(cases)}/22 categorias com alguma evidência natural. Algumas demonstram apenas uma transformação pequena ou evidência incompleta, como explicado em cada caso.",
        '\n## Cobertura\n\n| Categoria | Evidência selecionada |\n|---|---|']
    delivery_path=folder.parent/'ENTREGA_FINAL.json'
    if delivery_path.exists() and read(delivery_path)['core_sha256']!=s['core_sha256']:
        technical=Path(__file__).resolve().parents[1]/'RELATORIO_FASE_5.md'
        lines.insert(2,f'\nEsta é a campanha preservada anterior aos ajustes finais de entrega. Os resultados pertencem ao código acima. As correções posteriores e sua validação separada estão no [relatório técnico](<{technical}>).')
    for n,title in enumerate(LABELS,1):lines.append(f"| {n}. {title} | {'Registrada — ler limites do caso' if n in cases else 'Não ocorreu naturalmente com evidência suficiente'} |")
    for n,title in enumerate(LABELS,1):lines+=['',f'## {n}. {title}','',cases.get(n,notes.get(n,'Não ocorreu naturalmente com evidência suficiente nesta campanha. O cenário controlado, quando existente, comprova apenas capacidade técnica e não substitui uma história natural.'))]
    cause_counts=Counter(e['context']['cause'] for e in formed)
    town_kinds=Counter(cities.get(str(e['location']['map_id']),{}).get('kind','desconhecido') for e in formed)
    dissolution=Counter(e['context'].get('reason') for e in kinds['GroupDissolved'])
    lines+=['','## Qualidade e limites narrativos','',
      f"Houve {len(formed)} formações de grupo, distribuídas por causa: {dict(cause_counts)}. Encerramentos registrados: {dict(dissolution)}. A quantidade de grupos não corresponde à mesma quantidade de histórias completas.",
      '\nPressão econômica predominante indica que muitas iniciativas ainda nasceram da sobrevivência. Segurança também pode ser consequência de roubo de comida; a categoria da pressão sozinha não identifica toda a causa da história.',
      f"\nFormações por tipo de localidade: {dict(town_kinds)}. Vilas não têm prefeito neste modelo, e a representação de suas demandas numa cidade não está implementada. Isso é uma limitação funcional relevante para a continuidade política.",
      f"\nAs propostas produziram {len(kinds['PolicyDecided'])} decisões e {len(kinds['PolicyRead'])} consultas presenciais. Cada leitura pode conter resposta já conhecida; não é uma nova mudança política.",
      f"\nA mortalidade foi {s['death_causes']}. Mortes com comida carregada: {len(s['food_carried_deaths'])}. A Fase 5 ampliou possibilidades sociais, mas este dado não demonstra equilíbrio econômico nem resolve automaticamente a predominância de privação.",
      '\nUma história forte precisa de transformação verificável: informação útil, mudança de objetivo, transferência material, alteração de cargo, relação, crença, lugar ou vida. Muitos episódios aqui são pequenos, interrompidos ou encerrados por perda de relevância.',
      '\nO alcance de fama é uma classificação do auditor baseada nos observadores e evidências; não deve ser confundido com conhecimento universal. Epíteto tampouco comprova capacidade física.',
      '\nA extração complementar usa o histórico do save e, para fatos que não entraram nele, apenas conhecimento direto retido com confiança de pelo menos 60%. Sua origem está identificada em `eventos_adicionais.json`. Rumores não são promovidos a acontecimentos objetivos.',
      f"\nDados: [{folder.name}/resumo.json](<{(folder/'resumo.json').resolve()}>) e [eventos rastreáveis](<{(folder/'eventos.jsonl.gz').resolve()}>). Os IDs nas tabelas permitem conferir o relato."]
    output.parent.mkdir(parents=True,exist_ok=True);output.write_text('\n'.join(lines)+'\n')
    (output.parent/'COBERTURA_HISTORIAS.json').write_text(json.dumps({'seed':s['seed'],'hours':s['hours'],'core_sha256':s['core_sha256'],
        'covered':len(cases),'categories':{n:{'name':t,'evidence_selected':n in cases,'event_ids':evidence.get(n,[])} for n,t in enumerate(LABELS,1)},
        'group_causes':dict(cause_counts),'group_dissolutions':dict(dissolution),'groups_by_town_kind':dict(town_kinds)},ensure_ascii=False,indent=2))
    print(json.dumps({'stories_file':str(output),'documented_categories':len(cases),'group_causes':dict(cause_counts)},ensure_ascii=False))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--folder',required=True);p.add_argument('--output',required=True)
    a=p.parse_args();generate(a.folder,a.output)
