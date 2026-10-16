"""Relatório filtrado do único save; não carrega nem continua a simulação."""
import json
from collections import Counter
from dataclasses import asdict
from pathlib import Path
from procedural.persistence import decode
from experiments.phase5_extract_history import stream_array
from procedural.action_pressure import KINDS,FORWARD

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'reports/fase_5_1'
CAMP=OUT/'campanha'

def write_json(path,value):
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')

def extract():
    """Corrige o rótulo do contador letal e audita ataques além das finalizações."""
    kills=Counter();violations=[];capacity_violations=[];ordinary_lethal_attacks=0;scanned=0
    decisions=Counter();group_causes=Counter();relayed=set()
    commitments={200:set(),1000:set()};progress={200:set(),1000:set()};group_actions={200:set(),1000:set()}
    last_intent={};selected=None
    for raw in stream_array(CAMP/'save_final.json',b'"history":['):
        fields=raw['fields'];kind=fields['kind'];scanned+=1
        if kind not in ('ViolenceIntentChanged','CharacterAttacked','CharacterKilled','CommitmentCreated','CommitmentProgress',
                        'PolicyDecided','GroupFormed','ResponseRelayed','ProposalSubmitted','GroupProtested'):continue
        event=decode(raw);c=event.context
        if kind in ('CommitmentCreated','CommitmentProgress') and c.get('origin') in KINDS:
            for hours in (200,1000):
                if event.turn>hours:continue
                if kind=='CommitmentCreated':commitments[hours].add(c['commitment_id'])
                elif c.get('action') in FORWARD:progress[hours].add(c['commitment_id'])
        if kind in ('ProposalSubmitted','GroupProtested','ResponseRelayed'):
            gid=event.target_id if kind=='ResponseRelayed' else c['group_id']
            for hours in (200,1000):
                if event.turn<=hours:group_actions[hours].add(gid)
        if kind=='ViolenceIntentChanged' and c.get('intent')=='kill':
            kills['1000']+=1
            if event.turn<=200:kills['200']+=1
            last_intent[(event.actor_id,event.target_id)]=asdict(event)
        if kind in ('CharacterAttacked','CharacterKilled') and c.get('violence_intent')=='kill':
            ordinary_lethal_attacks+=1;a=c.get('action_audit',{})
            if not a.get('eligibility_causes') or a.get('world_pressure',0)<60:
                if len(violations)<5:violations.append({'event':event.id,'turn':event.turn,'audit':a})
            if a.get('capacity',0)<12 or a.get('action_pressure',0)<35:
                if len(capacity_violations)<5:capacity_violations.append({'event':event.id,'turn':event.turn,'audit':a})
            if selected is None:selected={'event':asdict(event),'intent_event':last_intent.get((event.actor_id,event.target_id)),'sources':[]}
        if kind=='PolicyDecided':decisions[c.get('result',{}).get('decision','unknown')]+=1
        if kind=='GroupFormed':group_causes[c.get('cause','unknown')]+=1
        if kind=='ResponseRelayed':relayed.update(c.get('source_facts',[]))
    for hours in (200,1000):
        path=CAMP/('curta_200h.json' if hours==200 else 'principal_1000h.json')
        summary=json.loads(path.read_text());lethal=summary['conversions']['lethal']
        if 'lethal_option_evaluations_available' not in lethal:
            lethal['lethal_option_evaluations_available']=lethal.pop('intent_changes')
        lethal['intent_changes']=kills[str(hours)]
        npc=summary['conversions']['npc']
        if 'intention_episodes' in npc:npc['pressure_record_creations']=npc.pop('intention_episodes')
        if 'actions_per_episode' in npc:npc['actions_per_pressure_record_creation']=npc.pop('actions_per_episode')
        npc.update(commitment_episodes_created=len(commitments[hours]),
            commitments_with_forward_progress=len(commitments[hours]&progress[hours]),
            forward_progress_fraction=round(len(commitments[hours]&progress[hours])/len(commitments[hours]),4) if commitments[hours] else None)
        group=summary['conversions']['group'];group['with_meaningful_action']=len(group_actions[hours])
        group['groups_with_action_fraction']=round(len(group_actions[hours])/group['formed'],4) if group['formed'] else None
        summary['telemetry_correction']='Lethal:available mede avaliações, não intenções. Criações de cache de pressão não são episódios de intenção. Compromissos criados e com progresso foram contados no histórico do mesmo save; sem reexecução.'
        write_json(path,summary)
    if selected:
        ids=set(selected['event']['context'].get('action_audit',{}).get('source_facts',[]))
        origin=selected['event']['context'].get('source_fact')
        if origin:ids.add(origin)
        for raw in stream_array(CAMP/'save_final.json',b'"history":['):
            if raw['fields']['id'] in ids:selected['sources'].append(asdict(decode(raw)))
        path=CAMP/'exemplos_filtrados.json';cases=json.loads(path.read_text())
        cases['lethal_attack_without_terminal']=selected;write_json(path,cases)
    evidence={'history_events_scanned':scanned,'kill_intent_changes':dict(kills),
        'ordinary_lethal_attacks_or_deaths':ordinary_lethal_attacks,
        'ordinary_lethal_semantic_violations_first_five':violations,
        'pre_final_capacity_or_disposition_violations_first_five':capacity_violations,
        'commitment_funnel':{str(h):{'created':len(commitments[h]),'with_forward_progress':len(commitments[h]&progress[h])} for h in (200,1000)},
        'policy_decisions':dict(decisions),'group_causes':dict(group_causes),
        'distinct_response_facts_relayed':len(relayed),
        'method':'Leitura sequencial do histórico do único save final. Nenhum motor carregado; nenhuma história bruta duplicada.'}
    write_json(OUT/'extracao_compacta.json',evidence)
    return evidence

def histories():
    cases=json.loads((CAMP/'exemplos_filtrados.json').read_text())
    names=json.loads((CAMP/'nomes.json').read_text())
    result=json.loads((CAMP/'principal_1000h.json').read_text())
    def person(i):return f"{names['characters'][str(i)]} (NPC #{i})" if str(i) in names['characters'] else f'NPC #{i}'
    def town(i):return names['towns'].get(str(i),f'local #{i}')
    titles={'local_representation':'Uma proposta chegou à autoridade local',
        'village_representation':'Representação de uma vila na cidade',
        'material_policy':'Resposta da autoridade e efeito material',
        'physical_response_return':'A informação voltou presencialmente ao grupo',
        'received_failure_and_protest':'Falhas recebidas chegaram ao protesto',
        'faction_capacity_preparation':'Preparação real de uma facção',
        'faction_action':'Ação organizacional com custo',
        'divine_action':'Intervenção divina',
        'combat_death':'Morte em combate',
        'lethal_attack_without_terminal':'A intenção letal chegou ao ataque, sem finalização',
        'deliberate_finish':'Finalização deliberada'}
    order=['local_representation','village_representation','material_policy','physical_response_return',
           'received_failure_and_protest','faction_capacity_preparation','faction_action',
           'divine_action','lethal_attack_without_terminal','deliberate_finish','combat_death']
    lines=['# Histórias reais — Fase 5.1','',
        'Seed **Selvaren-51**, mundo novo, sem jogador; 1.000 horas totais, incluindo o marco de 200h.',
        'A seleção abaixo contém fatos da campanha, anterior aos ajustes finais de integração. Microcenários não entram como lore natural.',
        'São episódios representativos; alguns pertencem ao mesmo arco. Os eventos não registram pensamentos privados dos personagens.','']
    chosen=[k for k in order if k in cases][:8]
    for num,key in enumerate(chosen,1):
        case=cases[key];ev=case['event'];c=ev['context'];origin=case.get('origin')
        lines.extend([f'## {num}. {titles[key]}',''])
        if origin:
            lines.append(f"O grupo **{origin['name']}**, de **{town(origin['town'])}**, surgiu na hora {origin['turn']} por `{origin['cause']}`. O representante registrado na formação era {person(origin['leader'])}.")
        if ev['kind']=='PolicyDecided':
            response=c.get('result',{});material=response.get('material',{})
            lines.append(f"Na hora {ev['turn']}, {person(ev['actor_id'])} produziu a resposta **{response.get('decision','não indicada')}** à proposta #{ev['target_id']}. Efeito material registrado: `{json.dumps(material,ensure_ascii=False)}`. Isso demonstra resposta institucional; não prova que todos os membros foram atendidos.")
        elif ev['kind']=='ResponseRelayed':
            recipients=', '.join(person(i) for i in c.get('recipients',[]))
            lines.append(f"Na hora {ev['turn']}, {person(ev['actor_id'])} retransmitiu presencialmente as respostas {c.get('source_facts',[])} a {recipients}. A existência da decisão na cidade, sozinha, não havia informado esses membros.")
        elif ev['kind']=='ProposalSubmitted':
            place=town(ev['location']['map_id'])
            lines.append(f"Na hora {ev['turn']}, {person(ev['actor_id'])} entregou a proposta #{c['proposal_id']} a {person(ev['target_id'])}, em **{place}**. A entrega ocorreu no encontro físico; o evento não equivale a aprovação nem a solução completa do problema.")
        elif ev['kind']=='GroupProtested':
            lines.append(f"Na hora {ev['turn']}, {person(ev['actor_id'])} protestou após {c.get('failures',0)} falhas registradas; fonte recebida #{c.get('source_fact')}. Houve reação política, sem violência coletiva automática.")
        elif ev['kind']=='CharacterKilled':
            lines.append(f"Na hora {ev['turn']}, {person(ev['actor_id'])} matou {person(ev['target_id'])}. Intenção registrada: `{c.get('violence_intent','não indicada')}`; contexto: `{c.get('death_context','ataque físico')}`. Uma morte física com intenção não letal não constitui finalização deliberada.")
        elif ev['kind']=='CharacterAttacked':
            lines.append(f"Na hora {ev['turn']}, {person(ev['actor_id'])} atacou {person(ev['target_id'])} com intenção **kill**, causando {c['damage']} de dano. As fontes registram dano anterior conhecido; a campanha não chegou a uma oportunidade terminal desse confronto.")
            previous=case.get('intent_event')
            if previous:lines.append(f"Mudança de intenção documentada: ViolenceIntentChanged #{previous['id']}, hora {previous['turn']}.")
        else:lines.append(ev['description'])
        chain=case.get('chain',[])
        if chain:lines.append('Encadeamento retido: '+ ' → '.join(f"{x['kind']} #{x['id']} (h{x['turn']})" for x in chain)+'.')
        lines.append(f"Evidência central: **{ev['kind']} #{ev['id']}**, hora **{ev['turn']}**.")
        audit=c.get('action_audit')
        if audit:lines.append(f"Auditoria da ação: WorldPressure={audit.get('world_pressure')}; ActionPressure={audit.get('action_pressure')}; capacidade={audit.get('capacity')}; barreiras={audit.get('major_barriers')}; fontes={audit.get('source_facts')}; alternativa={audit.get('selected_alternative')}.")
        sources=case.get('sources',[])
        if sources:lines.append('Fontes anteriores: '+'; '.join(f"{x['description']} (#{x.get('id',x.get('event_id'))}, h{x['turn']})" for x in sources[:4])+'.')
        lines.append('')
    lines.extend(['## Ausências e histórias que não avançaram',''])
    group=result['conversions']['group'];f=result['conversions']['faction'];g=result['conversions']['god'];lethal=result['conversions']['lethal']
    lines.append(f"Dos {group['formed']} grupos formados, {group['with_meaningful_action']} chegaram a entrega, protesto ou retransmissão. Há muito mais articulação que mudança concluída; formar grupo continua sem garantir ação.")
    lines.append(f"Facções: {f['organizational_actions']} ações, {f['preparation_attempts']} preparações e {f['joined']} adesões. As sedes naturais continuaram limitando a saída e a capacidade; o êxito do raid controlado não é uma invasão desta seed.")
    lines.append(f"Deuses: {g['prayers']} orações, {g['action_considered']} avaliações e {g['interventions']} intervenções. A causa conhecida não ultrapassou o filtro semântico; oração isolada não bastou. O cenário controlado de perda de fiéis não ocorreu aqui como arco confirmado.")
    lines.append(f"Intenções de matar: {lethal['intent_changes']} mudanças, {lethal['actors_with_kill_intent']} autores; {lethal['terminal_opportunities']} oportunidades e {lethal['terminal_decisions']} decisões terminais. Destruição de localidades, apoteose e morte divina não foram produzidas para preencher categorias.")
    lines.extend(['','Não há base para afirmar que esta fase já produz guerras ou grandes sagas com regularidade. A evidência mais forte é a continuidade política; facções e divindades permanecem gargalos naturais.',
        '', f'[Evidência filtrada](<{CAMP}/exemplos_filtrados.json>) · [Métricas da campanha](<{CAMP}/principal_1000h.json>) · [Único save final](<{CAMP}/save_final.json>)',''])
    (OUT/'HISTORIAS_REAIS.md').write_text('\n'.join(lines))

def inventory():
    roots=[ROOT/'fase_5_1.md',ROOT/'RELATORIO_FASE_5_1.md',ROOT/'tests/test_phase51.py',
           ROOT/'experiments/phase51_audit.py',ROOT/'experiments/phase51_report.py']
    files=[p for p in OUT.rglob('*') if p.is_file() and p.name!='tamanho_arquivos.json']
    # Módulos novos; alterações de módulos existentes aparecem no patch, sem copiar a base.
    files+=roots+[ROOT/'procedural/action_pressure.py',ROOT/'procedural/collective_action.py']
    entries={str(p.relative_to(ROOT)):p.stat().st_size for p in files if p.exists()}
    data={'new_file_bytes_excluding_this_manifest':sum(entries.values()),'files':entries,
        'method':'Tamanho real dos novos arquivos listados. Não inclui arquivos antigos modificados, caches Python nem campanhas anteriores. Não há cópia nova do núcleo.'}
    data['manifest_bytes']=0;data['total_new_file_bytes']=sum(entries.values())
    for _ in range(4):
        size=len((json.dumps(data,ensure_ascii=False,indent=2)+'\n').encode())
        data['manifest_bytes']=size;data['total_new_file_bytes']=sum(entries.values())+size
    write_json(OUT/'tamanho_arquivos.json',data)
    return data

if __name__=='__main__':
    print(json.dumps(extract(),ensure_ascii=False));histories();inventory()
