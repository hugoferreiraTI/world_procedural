"""Catálogo integral de eventos narrativos e relatório crítico de uma seed nova."""
import argparse,gzip,json
from collections import Counter,defaultdict
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
TERMINAL={'CharacterKilled','CharacterDied','CharacterCaptured','RestitutionGiven','ApologyGiven',
 'ConflictForgiven','FirstAidGiven','ResidentMoved','SuccessionChanged','ComfortGiven'}
SOCIAL={'CharacterConfronted','CharacterThreatened','CharacterInsulted','CharacterWarned',
 'ApologyGiven','RestitutionDemanded','RestitutionGiven','CalmingAttempted','ConflictForgiven'}
TRANSLATE={'hunger':'fome','thirst':'sede','both':'fome e sede','combat':'combate',
 'wanted':'procura criminal conhecida','threat':'ameaça conhecida','poverty':'pobreza persistente',
 'family':'relação familiar','self_harm':'causa autoinfligida abstrata'}
def rows(folder,name):
    with gzip.open(folder/name,'rt',encoding='utf-8') as f:
        for line in f:yield json.loads(line)
def pretty(n):return f'{n:,}'.replace(',','.')
def link(path,label):return f'[{label}](<{path}>)'

def build(folder):
    folder=Path(folder).resolve();summary=json.loads((folder/'resumo.json').read_text())
    initial=json.loads((folder/'personagens_iniciais.json').read_text());final=json.loads((folder/'personagens_finais.json').read_text())
    people={**initial,**{i:{**initial.get(i,{}),**p} for i,p in final.items()}}
    towns=json.loads((folder/'cidades_iniciais.json').read_text());townfinal=json.loads((folder/'cidades_finais.json').read_text())
    kingdoms=json.loads((folder/'reinos_iniciais.json').read_text());kingfinal=json.loads((folder/'reinos_finais.json').read_text())
    micro=json.loads((ROOT/'reports/lore_microchecks.json').read_text())
    def name(i):return 'sem personagem identificado' if i is None else f"{people[str(i)]['name']} (#{i})" if str(i) in people else f"{towns[str(i)]['name']} (cidade#{i})" if str(i) in towns else f"{kingdoms[str(i)]['name']} (reino#{i})" if str(i) in kingdoms else f'entidade#{i}'
    def townname(i):return towns.get(str(i),{}).get('name',f'local#{i}')
    events=sorted(rows(folder,'eventos.jsonl.gz'),key=lambda e:(e['turn'],e['id']))
    byid={e['id']:e for e in events};byactor=defaultdict(list);personcounts=defaultdict(Counter);witnesses=Counter();eventcounts=Counter()
    parent={i:i for i in byid};direct_parent={};edge_type={}
    def root(i):
        path=[]
        while parent[i]!=i:path.append(i);i=parent[i]
        for x in path:parent[x]=i
        return i
    def edge(child,source,kind):
        if source in byid and source<child and byid[source]['turn']<=byid[child]['turn']:
            a,b=root(child),root(source)
            if a!=b:parent[a]=b
            if child not in direct_parent:direct_parent[child]=source;edge_type[child]=kind
    rulers={int(i):k['ruler_id'] for i,k in kingdoms.items()};royaldeaths={}
    wanted_origins={};closed_origins=set();closed_cases=set();reopened=[];old_warrants=[];false_adapt=[];repeat_case_fines=[]
    moves=defaultdict(list);realmcounts=defaultdict(Counter);royal_successions=[]
    for e in events:
        eventcounts[e['kind']]+=1
        source=e['context'].get('source_fact') or e['context'].get('fact_id')
        if source is None and str(e['context'].get('source','')).startswith('event:'):
            try:source=int(e['context']['source'].split(':')[1])
            except ValueError:pass
        edge(e['id'],source,'event_context')
        ids={e['actor_id'],e['target_id']}
        if e['kind']=='WantedIssued':ids.add(e['context'].get('suspect_id'))
        for i in ids:
            if str(i) in people:
                byactor[i].append(e);personcounts[i][e['kind']]+=1
        for i in e['witnesses']:
            if str(i) in people:witnesses[i]+=1
        town=towns.get(str((e['location'] or {}).get('map_id')))
        if town:realmcounts[town['kingdom_id']][e['kind']]+=1
        if e['kind'] in ('CharacterKilled','CharacterDied'):
            for k,ruler in rulers.items():
                if ruler==e['target_id']:royaldeaths[k]=e
        if e['kind']=='SuccessionChanged':
            old=royaldeaths.get(e['target_id'])
            if old and old['turn']==e['turn']:edge(e['id'],old['id'],'royal_death_same_ruler')
            royal_successions.append({'event':e,'death':old});rulers[e['target_id']]=e['actor_id']
        if e['kind']=='WantedIssued':
            source=e['context']['source_fact'];wanted_origins[e['context']['record_id']]=source
            if (e['actor_id'],source) in closed_origins:reopened.append(e)
            if source in byid and e['turn']-byid[source]['turn']>168:old_warrants.append(e)
        if e['kind'] in ('GuardResponded','CharacterCaptured'):
            source=wanted_origins.get(e['context'].get('record_id')) or e['context'].get('source_fact')
            if source:closed_origins.add((e['actor_id'],source))
            case=(e['actor_id'],e['context'].get('record_id'))
            if case[1] is not None:
                if case in closed_cases and e['context'].get('fine',0)>0:repeat_case_fines.append(e)
                closed_cases.add(case)
        if e['kind']=='ResidentMoved':moves[e['actor_id']].append(e)
        if e['kind']=='PersonalityAdapted' and str(e['actor_id']) in initial:
            months=e['context']['months'];p=initial[str(e['actor_id'])]['personality']
            saturated=[key for key in e['context']['changes'] if p[key]+months-1>=100]
            if saturated:false_adapt.append({'event_id':e['id'],'actor':e['actor_id'],'fields_at_cap':saturated})
    financial=Counter();financial_examples=[];financial_repeats=defaultdict(list);rich=[];vengeance=[];outcomes=Counter()
    root_decisions=0
    for d in rows(folder,'decisoes.jsonl.gz'):
        if d['depth']!=0:continue
        root_decisions+=1;outcomes[d['action']+':'+str(d['success'])]+=1
        source=d['source_event_id']
        for i in d['event_ids']:
            if i in byid and byid[i]['actor_id']==d['actor'] and i not in direct_parent:
                edge(i,source,'executed_need_source')
        if d['success'] and d['action'] in ('steal','steal_meal','steal_person'):
            need=d['need']['kind'] if d['need'] else 'unknown'
            financial['successful_theft_need:'+need]+=1
            if need in ('money','advancement'):
                financial['financial_thefts']+=1
                if d['after']['money']==d['before']['money']:financial['financial_no_direct_money_gain']+=1
                if d['before']['food']>=2:financial['financial_already_two_food']+=1
                financial_repeats[d['actor'],d['need']['id']].append((d['turn'],d['before']['money'],d['after']['money'],d['event_ids']))
                if len(financial_examples)<12:financial_examples.append(d)
            if need=='advancement' and d['before']['money']>=20 and d['event_ids']:rich.append(d['event_ids'][0])
        if d['success'] and d['action']=='attack' and d['need'] and d['need']['kind']=='revenge':
            known=d['known_source']
            if known and known['kind']=='CharacterKilled':vengeance+=d['event_ids']
    components=defaultdict(list)
    for e in events:components[root(e['id'])].append(e)
    # Agrega somente eventos isolados de rotina por par/semana. As listas de
    # IDs continuam integrais; esses lotes não são apresentados como um arco causal.
    repetitive={'FamilyConcern','AbsenceNoticed','FamilySearch','Remembrance','PersonalityAdapted'}
    episodes=[];routine=defaultdict(list)
    for r,chain in components.items():
        if len(chain)==1 and chain[0]['kind'] in repetitive:
            e=chain[0];routine[e['kind'],e['actor_id'],e['target_id'],e['turn']//168].append(e)
        else:episodes.append({'root':r,'type':'causal_or_single','events':chain})
    for key,chain in routine.items():episodes.append({'root':min(e['id'] for e in chain),'type':'routine_batch','events':chain})
    episodes.sort(key=lambda x:(x['events'][0]['turn'],x['root']))
    lookup={e['id']:ep for ep in episodes for e in ep['events']}
    with gzip.open(folder/'CATALOGO_COMPLETO_DE_ARCOS.jsonl.gz','wt',encoding='utf-8') as f:
        for n,ep in enumerate(episodes,1):
            chain=ep['events'];types=Counter(e['kind'] for e in chain)
            ep['id']=n;ep['kinds']=types
            f.write(json.dumps({'arc_id':n,'root_event':ep['root'],'classification':ep['type'],
              'start':chain[0]['turn'],'end':chain[-1]['turn'],'event_count':len(chain),
              'event_counts':dict(types),'event_ids':[e['id'] for e in chain],
              'people':sorted({i for e in chain for i in (e['actor_id'],e['target_id']) if str(i) in people})},ensure_ascii=False)+'\n')
    chosen=[];used=set()
    def choose(title,ep,context=None):
        if ep['id'] in used:return
        used.add(ep['id']);chosen.append({'title':title,'episode':ep,'context':context or []})
    ranked=sorted((ep for ep in episodes if ep['type']!='routine_batch'),
                  key=lambda ep:(-(ep['events'][-1]['turn']-ep['events'][0]['turn']),-len(ep['events'])))
    for ep in ranked:
        if ep['kinds']['CharacterKilled']:
            choose('Conflito com morte violenta e continuidade causal',ep)
            if sum('morte violenta' in s['title'] for s in chosen)>=5:break
    for kind,title in [('RestitutionGiven','Cobrança e devolução de um bem real'),('ApologyGiven','Desculpas em uma disputa'),
       ('CharacterCaptured','Autoridade, confronto e captura'),('FirstAidGiven','Ferimento e auxílio com recursos'),
       ('ProtectionGiven','Proteção e intervenção de terceiros'),('ConflictForgiven','Perdão observado'),
       ('CalmingAttempted','Tentativa de aliviar tensão'),('CharacterSurrendered','Rendição'),
       ('CharacterFled','Fuga física'),('CharacterWithdrew','Retirada'),('ComfortGiven','Apoio após perda'),
       ('SuccessionChanged','Morte e sucessão política'),('RemainsLocated','Descoberta de restos e conhecimento tardio')]:
        for ep in ranked:
            if ep['kinds'][kind] and ep['id'] not in used:
                choose(title,ep)
                if sum(s['title']==title for s in chosen)>=2:break
    for eventid in rich[:3]+vengeance[:3]:
        if eventid in lookup:choose('Crime por avanço financeiro' if eventid in rich else 'Resposta de vingança após morte conhecida',lookup[eventid])
    for reason in ('wanted','poverty','threat','family'):
        for e in events:
            if e['kind']=='MigrationStarted' and e['context']['reason']==reason:
                later=[x for x in byactor[e['actor_id']] if x['actor_id']==e['actor_id'] and
                  e['turn']<=x['turn']<=e['turn']+250 and x['kind'] in ('MigrationArrived','ResidentMoved','CharacterDied','CharacterKilled')]
                if not later:continue
                context=[x for x in byactor[e['actor_id']] if 0<=e['turn']-x['turn']<=72 and x['id']!=e['id']
                         and x['kind'] in ('WantedIssued','ItemStolen','CharacterAttacked','CharacterThreatened')][-3:]
                choose('Migração por '+TRANSLATE.get(reason,reason),{'id':f'migration:{e["id"]}','root':e['id'],
                  'type':'temporal_migration','events':[e]+later,'kinds':Counter(x['kind'] for x in [e]+later)},context)
                break
    for pid,record in summary['death_records'].items():
        if record['cause'] not in ('hunger','both') or record.get('food',0)<=0:continue
        death=byid.get(record.get('event_id'))
        previous=[e for e in byactor[int(pid)] if e['actor_id']==int(pid) and
          e['kind']=='ItemStolen' and 0<=record['turn']-e['turn']<=1]
        if death and previous:
            chain=previous[-1:]+[death]
            choose('Ração obtida, mas morte antes da refeição',{'id':f'survival:{pid}',
              'root':chain[0]['id'],'type':'temporal_survival','events':chain,
              'kinds':Counter(e['kind'] for e in chain)})
    selected_ids=set()
    for s in chosen:
        chain=s['episode']['events']
        # Exibe marcos e amostra de agressões; catálogo conserva o restante.
        keyevents=[e for e in chain if e['kind'] in TERMINAL or e['kind']=='MigrationStarted']
        sample=chain[:3]+keyevents[:12]+[e for e in chain if e['kind']=='CharacterAttacked'][:4]+chain[-4:]+s['context']
        s['shown']=sorted({e['id']:e for e in sample}.values(),key=lambda e:(e['turn'],e['id']))[:30]
        selected_ids.update(e['id'] for e in s['shown'])
    traces={}
    for d in rows(folder,'decisoes.jsonl.gz'):
        if d['depth']!=0:continue
        for i in d['event_ids']:
            if i in selected_ids and byid[i]['actor_id']==d['actor']:traces[i]=d
    reactions_by_death=defaultdict(list);kin_loss_recipients=set();reaction_kinds=Counter();reaction_total=0
    for r in rows(folder,'reacoes.jsonl.gz'):
        reaction_total+=1;reaction_kinds[r['fact']['kind']]+=1
        if r['kin_of_victim'] and r['fact']['kind'] in ('CharacterKilled','CharacterDied','RemainsLocated'):
            kin_loss_recipients.add((r['person'],r['fact']['target_id']))
            if len(reactions_by_death[r['fact']['target_id']])<8:reactions_by_death[r['fact']['target_id']].append(r)
    story_lines=[f'# Histórias detalhadas — {summary["seed"]}','',
      'Mundo novo, sem jogador, 5.000 horas. Os títulos interpretam registros reais. Há ligações explícitas por fonte e sequências apenas temporais, identificadas separadamente. IDs distinguem nomes repetidos.','',
      f'Catálogo integral: {link(folder/"CATALOGO_COMPLETO_DE_ARCOS.jsonl.gz","todos os arcos/lotes e IDs")}. Biografias: {link(folder/"CATALOGO_POR_PERSONAGEM.md","todos os personagens")}.','']
    evidence=[]
    for n,s in enumerate(chosen,1):
        ep=s['episode'];chain=ep['events'];ids={i for e in chain for i in (e['actor_id'],e['target_id']) if str(i) in people}
        protagonist=next((e['actor_id'] for e in chain if str(e['actor_id']) in people),None)
        headline=s['title']+(f' — {name(protagonist)}' if protagonist is not None else '')
        story_lines += [f'## L{n:02d} — {s["title"]}','',
          f"Arco **{ep['id']}**; h{chain[0]['turn']}→h{chain[-1]['turn']}; {len(chain)} fatos; {len(ids)} participantes diretos. Tipo: `{ep['type']}`.",'']
        story_lines[-4]=f'## L{n:02d} — {headline}'
        s['headline']=headline
        opening=chain[0]
        place=(opening.get('location') or {}).get('map_id')
        story_lines += [f"**Leitura da história:** em h{opening['turn']}, {townname(place)}, o primeiro registro deste recorte diz: {opening['description']}",'']
        violent=[e for e in chain if e['kind']=='CharacterKilled']
        if violent:
            deaths_text='; '.join(f"{name(e['actor_id'])} matou {name(e['target_id'])} em h{e['turn']}" for e in violent[:4])
            story_lines += [deaths_text+'.'+(f' Há mais {len(violent)-4} mortes violentas no catálogo deste arco.' if len(violent)>4 else ''),'']
        endings=[e for e in chain if e['kind'] in TERMINAL]
        if endings:
            story_lines += ['Entre as consequências registradas: '+' '.join(e['description'] for e in endings[-3:])+f" O último fato disponível neste recorte ocorreu em h{chain[-1]['turn']}; isso não implica que a disputa tenha terminado definitivamente.",'']
        else:
            story_lines += ['Este recorte não contém morte, captura, reparação, socorro, consolo ou fixação residencial. A tensão/ação registrada não deve receber um encerramento inventado.','']
        if ep['type']=='temporal_survival':story_lines+=['A ação e a morte estão ligadas por personagem e fechamento da mesma hora: o estado após obter a ração conserva fome no máximo, e o registro da morte ainda contém esse alimento. É uma sequência temporal auditada, não um elo inventado por fonte.','']
        elif ep['type']=='temporal_migration':story_lines+=['Partida, chegada e fixação pertencem à mesma viagem por ator/tempo. Antecedentes são contexto; não se presume que um crime específico seja a causa sem referência na decisão.','']
        else:story_lines+=['Os elos se conectam por fonte de evento/necessidade executada; o registro da fonte demonstra a referência causal do agente, sem garantir que aquela informação seja completa ou que toda a vida esteja neste arco.','']
        kinds=ep['kinds']
        story_lines += ['Desfechos presentes: '+(', '.join(f'{k}: {v}' for k,v in kinds.items() if k in TERMINAL) or 'nenhum desfecho terminal registrado')+'.','']
        if kinds['CharacterAttacked']>15:story_lines+=['**Limite de qualidade:** o arco contém muita repetição de agressões. Continuidade causal aparece, mas a frequência de golpes não equivale a novos objetivos ou capítulos distintos.','']
        for e in s['shown']:
            story_lines.append(f"- **h{e['turn']} · evento#{e['id']} · {e['kind']}**: {e['description']} [ator {name(e['actor_id'])}; alvo {name(e['target_id'])}]")
            d=traces.get(e['id'])
            if d:
                nd=d['need'];known=d['known_source'];alternative=next((x for x in d['candidates'] if x['action']!=d['action']),None)
                source=(f"fato#{known['event_id']}, confiança {known['confidence']}%, origem {known['source_kind']}" if known else
                  f"origem interna `{nd['source'] if nd else 'manual'}`, sem fato externo de referência" if d['source_event_id'] is None else
                  f"fato#{d['source_event_id']} fora da memória curta amostrada; necessidade/caso pode conservar referência própria")
                rival=f"; alternativa `{alternative['action']}`={alternative['score']:.2f}" if alternative else ''
                story_lines+=['',f"  Necessidade `{nd['kind'] if nd else 'manual'}`; prioridade {nd['priority'] if nd else '—'}; {source}. Ação `{d['action']}`, score do objetivo {d['goal_score']:.2f}{rival}. Avaliação das alternativas em h{d['candidate_evaluation_turn']}; objetivo criado em h{d['goal_created_at']}. Resultado: {d['outcome'].rstrip('.') }.",
                 f"  Antes: HP {d['before']['health']}, fome {d['before']['hunger']}, dinheiro {d['before']['money']}, comida {d['before']['food']}; raiva {d['emotions']['anger']:.1f}, ressentimento {d['emotions']['resentment']:.1f}, desespero {d['emotions']['desperation']:.1f}. Depois: HP {d['after']['health']}, dinheiro {d['after']['money']}, comida {d['after']['food']}.",'']
            if e['kind'] in ('CharacterKilled','CharacterDied'):
                for r in reactions_by_death[e['target_id']][:3]:
                    nd=[x for x in r['needs'] if x['kind'] in ('grief','revenge')]
                    story_lines += [f"  Conhecimento familiar: {name(r['person'])} recebeu {r['fact']['kind']} em h{r['learned_at']}, confiança {r['fact']['confidence']}%; pressões registradas: {[(x['kind'],x['status']) for x in nd]}. Isso registra recepção/estado, não uma vingança concluída.",'']
            evidence.append({'story':n,'arc':ep['id'],'event_id':e['id'],'decision':d})
        omitted=len(chain)-len([e for e in s['shown'] if e['id'] in {x['id'] for x in chain}])
        story_lines += [f'Fatos do arco não exibidos neste recorte: {max(0,omitted)}. IDs integrais no catálogo.','']
    (folder/'HISTORIAS_DETALHADAS.md').write_text('\n'.join(story_lines))
    (folder/'evidencias_historias.json').write_text(json.dumps(evidence,ensure_ascii=False,indent=2))
    # Biografia compacta de todos os indivíduos, inclusive os sem arco forte.
    profiles=['# Catálogo por personagem','',
      'Todos os personagens da sessão. Contagens de fatos não são contagens de histórias concluídas. Família é a relação registrada, nunca inferida só pelo sobrenome. Trabalho e consumo rotineiros não entram no inventário de lore abaixo.','']
    for i,p in sorted(people.items(),key=lambda x:int(x[0])):
        pid=int(i);start=initial.get(i,{});end=final[i];counts=personcounts[pid]
        profiles += [f'## #{i} — {p["name"]}','',
          f"Profissão inicial/final: {start.get('profession','introduzido durante a sessão')} / {end['profession']}. Residência inicial/final: {townname(start.get('town_id'))} / {townname(end['town_id'])}. Estado: {'vivo' if end['alive'] else 'morto'}. Família inicial registrada: {', '.join(name(x) for x in start.get('family',[])) or 'nenhuma relação próxima registrada'}.",
          f"Participação em fatos: {dict(counts)}. Presenças como testemunha/participante: {witnesses[pid]}."]
        relevant=[e for e in byactor[pid] if e['kind'] not in repetitive]
        for e in (relevant[:2]+relevant[-2:] if len(relevant)>4 else relevant):
            profiles.append(f"- h{e['turn']}, evento#{e['id']}: {e['description']}")
        if moves[pid]:profiles.append('Residências adotadas: '+' → '.join(townname(e['context']['town_id']) for e in moves[pid])+'.')
        death=summary['death_records'].get(i)
        if death:profiles.append(f"Morte em h{death['turn']}: {TRANSLATE.get(death['cause'],death['cause'])}; evento#{death.get('event_id')}.")
        if not relevant:profiles.append('Sem ação narrativa principal registrada; isso não significa que o personagem ficou sem rotina ou necessidades.')
        profiles+=['']
    (folder/'CATALOGO_POR_PERSONAGEM.md').write_text('\n'.join(profiles))
    local_events=defaultdict(list)
    for event in events:
        place=(event['location'] or {}).get('map_id')
        if str(place) in towns:local_events[place].append(event)
    locations=['# Histórias e situação por localidade','',
      'Todas as localidades geradas. O agrupamento usa o local físico do fato; um visitante pode agir em outra cidade. Valores finais não reconstituem o estoque no instante de mortes anteriores. O catálogo integral conserva os fatos omitidos no recorte.','']
    for tid,t in towns.items():
        end=townfinal[tid];chain=local_events[int(tid)];counts=Counter(e['kind'] for e in chain)
        population_alive=sum(people[str(i)]['alive'] for i in end['resident_ids'] if str(i) in people)
        locations += [f"## {t['name']} (#{tid}) — {kingdoms[str(t['kingdom_id'])]['name']}",'',
          f"Especialização: {t['specialization']}. Abstratos inicial/final: {t['abstract_population']}/{end['abstract_population']}. Persistentes vivos residentes ao final: {population_alive}. Caixa municipal inicial/final: {t['money']}/{end['money']}. Dinheiro dos abstratos inicial/final: {t['abstract_money']}/{end['abstract_money']}.",'',
          f'Fatos locais: {dict(counts)}.','']
        landmarks=[e for e in chain if e['kind'] in TERMINAL]
        local_sample=landmarks[:3]+landmarks[-3:]
        if not landmarks:local_sample=chain[:2]+chain[-2:]
        for event in sorted({e['id']:e for e in local_sample}.values(),key=lambda e:(e['turn'],e['id'])):
            locations.append(f"- h{event['turn']}, evento#{event['id']}: {event['description']} [{name(event['actor_id'])}; {name(event['target_id'])}]")
        locations+=['']
    (folder/'CATALOGO_POR_LOCALIDADE.md').write_text('\n'.join(locations))
    repeated=[{'actor':a,'need_id':n,'successes':len(v),'start':v[0][0],'end':v[-1][0],
              'first':v[0],'last':v[-1]} for (a,n),v in financial_repeats.items() if len(v)>=3]
    migration_reasons=Counter(e['context']['reason'] for e in events if e['kind']=='MigrationStarted')
    multi_residence=[{'person':p,'moves':len(v),'towns':sorted({e['context']['town_id'] for e in v}),
                     'evidence':[e['id'] for e in v[:3]]} for p,v in moves.items() if len({e['context']['town_id'] for e in v})>1]
    names=Counter(p['name'] for p in people.values());duplicate_groups={k:v for k,v in names.items() if v>1}
    food_deaths=[{'person_id':int(i),**r} for i,r in summary['death_records'].items() if r['cause'] in ('hunger','both') and r.get('food',0)>0]
    traveling_deaths=[e for e in events if e['kind']=='CharacterDied' and e['location'] and e['location']['map_id']==1]
    corpse_without_food=[e for e in traveling_deaths if summary['death_records'].get(str(e['target_id']),{}).get('cause') in ('thirst','both')]
    data={'episodes':len(episodes),'covered_events':sum(len(ep['events']) for ep in episodes),'stories':len(chosen),
      'financial_theft':dict(financial),'financial_repeat_people':len({x['actor'] for x in repeated}),
      'financial_repeat_examples':sorted(repeated,key=lambda x:-x['successes'])[:20],
      'same_guard_reopened_closed_source_count':len(reopened),'same_guard_reopen_events':[e['id'] for e in reopened[:30]],
      'same_guard_same_record_repeat_fines_count':len(repeat_case_fines),
      'same_record_repeat_fine_events':[e['id'] for e in repeat_case_fines[:30]],
      'warrants_origin_older_than_168h':len(old_warrants),'old_warrant_events':[e['id'] for e in old_warrants[:20]],
      'multiple_residence_graph_candidates':multi_residence,'adaptation_false_delta_count':len(false_adapt),
      'adaptation_false_delta_examples':false_adapt[:20],'duplicate_name_groups':duplicate_groups,
      'family_loss_recipients':len(kin_loss_recipients),'reaction_records':reaction_total,
      'reaction_fact_kinds':dict(reaction_kinds),'food_carried_deaths':food_deaths,
      'deaths_on_external_map':[e['id'] for e in traveling_deaths],
      'external_thirst_deaths':[e['id'] for e in corpse_without_food],
      'royal_successions':royal_successions,'root_action_outcomes':dict(outcomes),
      'root_decision_records':root_decisions,'event_counts':dict(eventcounts)}
    (folder/'analise_lore.json').write_text(json.dumps(data,ensure_ascii=False,indent=2))
    write_report(folder,summary,data,people,towns,kingdoms,kingfinal,realmcounts,micro,name,chosen)
    print(json.dumps({'stories':len(chosen),'episodes':len(episodes),'covered_events':data['covered_events'],
      'same_guard_reopened':len(reopened),'multiple_residence_people':len(multi_residence)},ensure_ascii=False))

def write_report(folder,s,a,people,towns,kingdoms,kingfinal,realmcounts,micro,name,chosen):
    """Seções analíticas escritas após fechar os catálogos integrais."""
    deaths=s['death_causes'];total=sum(deaths.values());famine=deaths.get('hunger',0)+deaths.get('both',0)
    metric=s['metrics'];parts=[]
    def section(title,body):parts.append(f'## {len(parts)+1}. {title}\n\n{body}\n')
    def file(label,name):return link(folder/name,label)
    section('Resultado e alcance',f"Seed **{s['seed']}**, versão **{s['rules']}**, mundo novo a partir de geração em h0, sem jogador e sem carregar saves. Observação de **{s['hours']} horas**. Elenco inicial: {s['initial']['alive']} persistentes e {s['initial']['abstract']} abstratos; {s['towns']} localidades e {s['kingdoms']} reinos. Final: {s['final']['alive']} vivos; {total} mortes. Há crime, combate, apoio, reparação, fuga e mudança de residência reais. A diversidade deve ser lida nas histórias, sem transformar contagem de eventos em qualidade literária.")
    section('Onde ler tudo',f"{file('Histórias detalhadas','HISTORIAS_DETALHADAS.md')}; {file('catálogo de todos os personagens','CATALOGO_POR_PERSONAGEM.md')}; {file('catálogo por localidade','CATALOGO_POR_LOCALIDADE.md')}; {file('cronologia dos reinos','CRONOLOGIA_DOS_REINOS.md')}; {file('catálogo integral de arcos, em JSONL compactado','CATALOGO_COMPLETO_DE_ARCOS.jsonl.gz')}; {file('eventos integrais selecionados','eventos.jsonl.gz')}; {file('decisões amostradas','decisoes.jsonl.gz')}; {file('recepção de notícias e necessidades','reacoes.jsonl.gz')}; {file('métricas','resumo.json')}; {file('análise quantitativa','analise_lore.json')}.\n\nO catálogo cobre {pretty(a['covered_events'])} eventos narrativos em {pretty(a['episodes'])} arcos/lotes. Componentes ligados por fontes são causais; eventos de rotina isolados são agrupados por par/semana e marcados como lote, sem inventar uma trama. {a['stories']} recortes recebem leitura detalhada. Consumo e trabalho comuns ficam nas métricas, não são apresentados como histórias épicas.")
    section('Método e evidência',f"Hash do núcleo congelado: `{s['core_sha256']}`. A instrumentação só observa avaliações feitas pelo motor e os resultados; não recalcula utility, não escolhe ações nem muda RNG. Dois mundos novos menores, simulados por 48h com/sem observador, produziram estado exato igual. Campos objetivos do auditor são separados da percepção do NPC. Na campanha, invariantes e índice criminal foram conferidos a cada 100h. Esses validadores cobrem estrutura e alguns índices; não certificam coerência de todo efeito social ou vínculo residencial. Receber um fato/ter uma necessidade não prova que o NPC a executou. As decisões incluem resultado real, dinheiro/comida antes e depois, fontes e alternativas disponíveis.\n\nO save final foi somente exportado; não foi carregado. Microcenários diagnósticos também nasceram de geração nova, em mundos separados. Recursos e relógio controlados nesses cenários são fixtures de reprodução, não fatos da campanha.")
    table=['| Hora | Vivos | Mortos | Raiva média | Desespero médio | Lesionados |','|---:|---:|---:|---:|---:|---:|']
    for x in s['samples']:table.append(f"| {x['turn']} | {x['alive']} | {x['dead']} | {x['emotions']['anger']['mean']} | {x['emotions']['desperation']['mean']} | {x['injured']} |")
    section('Evolução do mundo','\n'.join(table))
    section('Comparação com Mira',comparison(s))
    counts=['| Fato/ação | Quantidade |','|---|---:|']+[f'| {k} | {pretty(v)} |' for k,v in sorted(s['events'].items())]
    section('Inventário de acontecimentos','\n'.join(counts)+f"\n\nRumores: {pretty(metric.get('RumorShared',0))}; informação estruturada: {pretty(metric.get('InformationShared',0))}. Ativações de família/luto/vingança: {metric.get('NeedCreated:family',0)} / {metric.get('NeedCreated:grief',0)} / {metric.get('NeedCreated:revenge',0)}. São ativações, não pessoas únicas nem missões concluídas.")
    section('Qualidade das histórias',f"Minha avaliação: a causalidade local e a consequência material são o ponto mais forte. Roubo gera respostas; proteção traz terceiros; combate pode terminar em fuga, rendição, captura ou morte; mudança de cidade altera o censo. Reparação e socorro mostram alternativas concretas.\n\nA variedade ainda é desigual: muitas sequências repetem agressões e proteção, e pressões financeiras alimentam crimes sobre provisões. Arcos extensos podem ser o prolongamento de uma disputa, sem capítulos com novos objetivos. O catálogo detalhado explicita duração, repetição e desfechos, evitando tratar toda sequência longa como história boa.\n\nLeitura narrativa crítica dos casos mais relevantes: {file('análise das melhores histórias e seus limites','LEITURA_CRITICA_DAS_HISTORIAS.md')}.")
    section('As histórias detalhadas','\n'.join(f'- L{i:02d}: {x["headline"]}, arco {x["episode"]["id"]}.' for i,x in enumerate(chosen,1)))
    section('Crime e motivação financeira',f"Roubos bem-sucedidos por necessidade (ações raiz, sem contar duas vezes uma execução interna): {a['financial_theft']}. O dinheiro ficou igual imediatamente após {a['financial_theft'].get('financial_no_direct_money_gain',0)} dos {a['financial_theft'].get('financial_thefts',0)} roubos sob objetivo money/advancement; {a['financial_theft'].get('financial_already_two_food',0)} começaram com pelo menos duas unidades de alimento. Foram identificadas {a['financial_repeat_people']} pessoas com pelo menos três roubos bem-sucedidos ligados à mesma necessidade financeira amostrada.\n\n**Limite confirmado:** o roubo financeiro transfere alimento, e muitas dessas ações deixam o dinheiro igual. Isso pode economizar uma compra, mas não constitui ganho monetário direto; a necessidade de dinheiro pode continuar alimentando a mesma escolha. Sem uma sequência de revenda ou outro benefício financeiro avaliado, cria-se repetição. Prioridade antes da próxima fase: restringir essa solução à finalidade que ela realmente atende, ou implementar uma estratégia financeira completa com transferência/pagador reais e retorno de progresso. Não criar moedas ao concluir um roubo.")
    section('Combate, proteção e encerramentos',f"Ataques: {metric.get('AttackExecuted',0)}; mortes em combate: {deaths.get('combat',0)}; proteção: {metric.get('ProtectionGiven',0)}; socorros: {metric.get('FirstAidGiven',0)}; fugas: {metric.get('CharacterFled',0)}; rendições: {metric.get('CharacterSurrendered',0)}; capturas: {metric.get('CharacterCaptured',0)}. Uma intervenção pode desviar dano para o protetor. Informação indireta com confiança baixa pode sustentar reação pessoal, mas não equivale à evidência mais forte exigida de um guarda.\n\nViolência não está limitada a mortes naturais. Porém frequência alta, sozinha, não comprova boas relações, vingança concluída ou estratégia. Golpes sucessivos sobre fontes antigas podem dominar a história quando outras respostas têm utility baixa.")
    section('Família, luto e conhecimento',f"{a['family_loss_recipients']} pares familiar/perda foram identificados nos registros de recepção. As histórias indicam quando a notícia chegou, com qual confiança e quais pressões apareciam. Uma morte não informa familiares remotos instantaneamente. Encontrar restos sem autoria pode gerar luto e não permite atribuir automaticamente culpa ao assassino que só o auditor conhece.\n\nContagem de necessidade de vingança não é vingança realizada. Os exemplos só recebem esse título quando uma ação executada de revenge referencia uma morte conhecida. Memória curta e prazos ainda interrompem continuidade; é desejável manter fatos relevantes de uma perda/objetivo sem promover toda notícia antiga a novo choque.")
    section('Migração e seus motivos',f"Motivos de partida: {migration_text(folder)}. Mudanças de residência: {metric.get('ResidentMoved',0)}. A partida exige reserva e rota conhecida; chegada precede fixação. {len(a['multiple_residence_graph_candidates'])} pessoas adotaram pelo menos dois destinos diferentes, situação que expõe o bug de vínculos residenciais persistentes descrito abaixo.\n\nMigração por família/trabalho depende de metadados de destino que ainda não são alimentados completamente. A pobreza compete com comida, renda e proteção; não deve ser interpretada como ausência de vontade de migrar apenas porque houve poucas partidas. O destino próximo conhecido pode ser escolhido sem prova de emprego melhor, favorecendo deslocamentos pouco transformadores.")
    carried='\n\n'.join(f"**Caso observado com alimento carregado:** {name(r['person_id'])}, evento#{r['event_id']}, morreu em h{r['turn']} com fome {r['hunger']}, comida {r['food']} e última ação `{r.get('last_successful_action',{}).get('action')}` em h{r.get('last_successful_action',{}).get('turn')}." for r in a['food_carried_deaths'])
    section('Morte, fome e sobrevivência',f"Causas: {deaths}. Fome ou fome+sede: {famine}/{total}, {100*famine/max(1,total):.2f}%. Mortes por fome/fome+sede com alimento carregado: {len(a['food_carried_deaths'])}. Mortes no mapa externo: {len(a['deaths_on_external_map'])}; por sede/fome+sede nesse mapa: {len(a['external_thirst_deaths'])}.\n\n{carried}\n\n**Falha de integração confirmada na campanha:** Bela Douran (#3139) executou steal_person em h582 com HP=1, fome=100 e comida=0. Depois estava com comida=1, mas a fome continuava 100. No fechamento em h583, a fisiologia matou o personagem antes de uma próxima refeição. O roubo pessoal da Fase 4 não está nas aquisições reconhecidas por FeedingSystem. Ele entra depois da conversão para ações de refeição, estimate retorna None e a solução passa sem verificar se a comida será consumida a tempo. steal_meal apareceu como alternativa com score 59,03, enquanto steal_person venceu com 61,10. Prioridade P1: integrar essa aquisição ao cálculo de sobrevivência e, quando aplicável, à operação de refeição; não criar alimento nem apagar fome sem consumo real. História L36 e decisão do evento#498585 conservam os estados completos.\n\nComida na cidade não significa posse, renda ou acesso do indivíduo. Este relatório não mede o estoque municipal no instante de toda morte e não usa estoque final como prova retrospectiva. Esse caso isolado não explica automaticamente as outras 331 mortes por fome/fome+sede. Ferimento, detenção, viagem e disputa por prioridade podem afetar a sobrevivência. Associação com ataques não deve ser contada como assassinato adicional. Para resolver dúvidas alimentares restantes, registrar uma janela de decisões vitais e oportunidades reais por vítima.")
    section('Viagens e reserva de água',f"Mortes por sede no mapa externo exigem conferir roteiro, duração real, terreno e reservas antes da partida. O planejamento mínimo estima sede a 2/h, enquanto a fisiologia no deserto usa 4/h. Isso é uma **limitação confirmada da estimativa**; não prova, por si só, que causou cada morte. Nesta sessão ocorreram {len(a['external_thirst_deaths'])} mortes por sede/fome+sede fora das cidades.\n\nMelhoria: estimar o caminho que o NPC conhece, usar margem para trechos incertos, reconhecer fontes visitadas e reconsiderar partida/abastecimento quando a cobertura não basta. Não consultar poços desconhecidos nem reabastecer automaticamente o viajante.")
    section('Emoções e equilíbrio',f"Estado final dos vivos: {s['final']['emotions']}. Causas factuais: {s['emotion_fact_causes']}. Pobreza persistente, fome, luto e combate sustentam desespero. Uma média alta pode indicar pressão contínua; não mede profundidade.\n\nMelhoria: diferenciar baixa liquidez, privação real e perda grave; avaliar recuperação quando há alimento, renda/apoio e segurança suficientes. Não apagar consequências de perdas para criar final feliz. Na campanha houve {a['adaptation_false_delta_count']} eventos de adaptação anunciando incremento em traço que já estava no teto, conforme valor inicial e sequência de mudanças: o estado continua limitado, mas o texto/contexto da mudança precisa usar o delta efetivo.")
    section('Reputação e reparação',f"Microcenário novo confirmou: desculpa cria tag reparador=8, medo=4 e admiração=0, com score reputacional social inalterado. A interpretação genérica trata tags fora de prestativo/leal/responsável como medo, incluindo reparação. Isso é incoerência semântica de estado, mesmo que confiança/emoção também melhorem.\n\nCorreção indicada: classificar efeitos positivos, negativos e neutros explicitamente; uma desculpa deve alterar medo somente quando houver motivo contextual. Medir reputação antes/depois de reparação com dano prévio, sem presumir perdão total. As opiniões continuam individuais; o auditor não deve impor uma reputação universal.")
    section('Autoridade e punição repetida',f"**Bug confirmado por reprodução:** houve somente um roubo; o guarda encerrou seu caso, perdeu a lembrança curta e reaprendeu o mesmo fato antigo. Surgiu novo caso com a mesma origem e uma segunda captura cobrou outra multa. Dinheiro do suspeito: 12→7→2. O caso encerrado estava persistido, mas on_fact não deduplicou a origem já encerrada pelo próprio guarda. Uma segunda reprodução confirmou que reaprender o próprio WantedIssued dentro de 168h pode reativar o mesmo registro já conhecido como encerrado: a segunda captura retirou mais 5 moedas (11→6).\n\nNa campanha, o catálogo identificou {a['same_guard_reopened_closed_source_count']} novos WantedIssued com a mesma origem já encerrada pelo mesmo guarda. Essa contagem marca reabertura, não prova multa duplicada em todos. Também há {a['same_guard_same_record_repeat_fines_count']} cobranças posteriores por mesmo guarda/record_id já encerrado; eventos: {a['same_record_repeat_fine_events']}. São sinais concretos para inspeção por caso; não confundem novos delitos com reaprendizado do antigo. Evidências: {a['same_guard_reopen_events']}. {a['warrants_origin_older_than_168h']} procuras tinham origem conhecida de mais de 168h; isso deve ser revisado com a política de validade, sem confundir falta de notícia sobre resolução com onisciência.\n\nCorreção prioritária: manter identidade/resultado do caso por origem/jurisdição e conhecimento próprio; reaprender o mesmo delito encerrado não é delito novo. Outro guarda que ignora a resolução pode investigar, mas deve poder obter a informação institucional local. Não bloquear usando automaticamente um encerramento remoto desconhecido.")
    section('Residência e consistência do grafo',f"**Bug confirmado:** duas mudanças reais deixam reside_em=100 nos dois destinos. O censo e town_id mantêm só a residência atual; o grafo conserva a anterior com o mesmo significado de atual. A reprodução separada terminou com censo apenas na cidade 50 e vínculos ativos nas cidades 32 e 50. Na campanha, {len(a['multiple_residence_graph_candidates'])} pessoas passaram por dois ou mais destinos distintos.\n\nCorrigir a relação atual ao transferir residência; conservar trajetória em evento/registro histórico próprio. Também revisar filiação e lealdades quando a mudança cruza reinos: morar em outro lugar não deve, sem decisão explícita, apagar identidade familiar ou política.")
    section('Identidade e apresentação',f"{len(a['duplicate_name_groups'])} nomes completos aparecem em mais de um personagem. IDs preservam identidade no código, mas texto sem cidade/profissão/ID pode sugerir que uma pessoa fez atos de outra. É um problema de legibilidade e continuidade, não prova de personagens fundidos.\n\nMelhoria: identificação estável em diário/interface, com local, ocupação e alcunha quando cabível. Traduzir os verbos internos dos eventos e distinguir protegido, agressor, cobrador e dono do bem devolvido. Não renomear pessoas retroativamente nem deduzir parentesco pelo sobrenome.")
    royallines=['| Reino | Situação final | Governante final | Profissão | Sucessões nesta sessão |','|---|---|---|---|---:|']
    for k,realm in kingdoms.items():
        end=kingfinal[k];r=end['ruler_id'];p=people.get(str(r),{})
        count=sum(x['event']['target_id']==int(k) for x in a['royal_successions'])
        royallines.append(f"| {realm['name']} | {end['political_state']} | {name(r) if r else 'sem governante'} | {p.get('profession','—')} | {count} |")
    section('Reinos, sucessão e limites políticos','\n'.join(royallines)+'\n\nA sucessão mínima troca ruler_id e não atualiza necessariamente profissão/rotina do herdeiro. Quando o governante final permanece estudante/conselheiro, isso é uma lacuna de integração a revisar; não equivale a disputa formal pelo trono. Religiões, títulos e templos gerados não representam deuses agindo. Não foram implementadas guerras, revoluções ou exércitos nesta fase; conflitos individuais não são descritos como guerra.')
    realm_lines=['# Cronologia e material narrativo dos reinos','']
    for k,realm in kingdoms.items():
        realm_lines += [f'## {realm["name"]} (#{k})','',
          'Contagens em mapas locais das cidades deste reino: '+str(dict(realmcounts[int(k)]))+'.','']
        for succession in a['royal_successions']:
            if succession['event']['target_id']==int(k):
                e=succession['event'];death=succession['death']
                realm_lines.append(f"- h{e['turn']}, evento#{e['id']}: {e['description']} Morte associada: evento#{death['id'] if death else 'não identificada'}. Causa: {(death or {}).get('context',{}).get('cause','não registrada')}.")
    (folder/'CRONOLOGIA_DOS_REINOS.md').write_text('\n'.join(realm_lines))
    section('O que não constitui bug por si só','NPC fugir, mentir, abandonar proteção, agir por rumor, não ajudar ou fracassar pode ser coerente com personalidade, informação, risco e recursos. Um arco interrompido por morte/afastamento também é válido. A crítica deve verificar objetivo, alternativas, percepção e resultado, sem exigir comportamento ideal. Gravidade de um assassinato tampouco obriga toda a cidade a saber instantaneamente.')
    section('Suspeitas que precisam de diagnóstico adicional','1. Reserva insuficiente em viagens pelo deserto: cruzar rota, água e relógio por vítima.\n2. Proteção perpetuando agressões: conferir vínculo com vítima/agressor e scores ao longo do arco.\n3. Desespero quase permanente apesar de recursos: separar renda baixa, estoque individual, perdas e perigo.\n4. Restituição resolvendo emoção do cobrador, mas não do dono: comparar target_id/owner_id e respostas do proprietário.\n5. Papel/rotina após sucessão ou mudança de reino: confirmar autoridade, renda e compromisso próprios.\n\nEssas hipóteses não são automaticamente contadas como bugs de toda a campanha; as reproduções confirmadas estão separadas acima.')
    section('Prioridades antes de novas fases','| Prioridade | Ação | Por que | Como verificar |\n|---|---|---|---|\n| P1 | Integrar roubo pessoal à refeição/sobrevivência | Obter alimento sem tempo para consumi-lo foi tratado como solução viável | HP=1, fome100, alvo local com ração: transferência, consumo e fechamento da hora |\n| P1 | Deduplicar caso encerrado ao reaprender origem/aviso | Evitar nova perseguição/multa pelo mesmo delito | Evicção da memória, notícia velha, mesmo guarda/caso |\n| P1 | Dar progresso real a soluções financeiras | Evitar roubo de alimento repetido sob necessidade de dinheiro | Transferências, renda/estoque antes/depois, repetições do mesmo objetivo |\n| P2 | Conferir sobrevivência em viagens | Corrigir estimativa de água; não houve morte em viagem nesta campanha | Rotas/terreno conhecidos, reservas e decisões durante viagem |\n| P2 | Atualizar grafo de residência e separar histórico | Evitar dupla residência atual e conflitos futuros de filiação | Duas mudanças, censo e relações |\n| P2 | Corrigir semântica de reputação reparadora | Evitar desculpa aumentando medo sem causa | Tags, confiança, medo e admiração antes/depois |\n| P2 | Alimentar destinos conhecidos por família/trabalho | Criar motivos concretos além de ameaça/crime | Informação obtida, vaga/familiar real, deslocamento e resultado |\n| P2 | Melhorar continuidade dos objetivos pessoais | Dar passos intermediários a luto/proteção/ambição | Fontes relevantes, prazo, resolução observada |\n| P3 | Usar deltas reais nas mudanças de personalidade | Prevenção: sem ocorrência no teto nesta sessão | Valores anterior/final e evento emitido |\n| P2 | Desambiguar personagens e traduzir diário | Tornar lore legível | Mesmo nome em pessoas diferentes e sequência por ID |\n| P3 | Conter histórico e melhorar performance | Permitir expansão sem ampliar custo indefinidamente | Memória, tamanho de save e registros acumulados |')
    perf=s['final']
    section('Performance e crescimento de registros',f"Tempo observado: {s['runtime_seconds']:.1f}s; decisões totais: {pretty(metric.get('NPCDecision',0))}; decisões narrativas raiz registradas: {pretty(a['root_decision_records'])}. Memória máxima aproximada na simulação (inclui observador; não é benchmark puro do motor): {perf['memory_peak_mib']}MiB. Save exportado: {s['save_bytes']/1048576:.2f}MiB; serialização: {s['save_seconds']}s. Não houve teste por carregamento de save nesta solicitação.\n\nFactImpact acumulados: {pretty(perf['applied_fact_entries'])}; opiniões registradas: {pretty(perf['reputation_entries'])}; casos criminais arquivados/ativos: {pretty(perf['wanted_records'])}. Guardar toda contribuição ajuda deduplicação, mas cresce mesmo com memórias curtas. Separar resumo histórico e fatos ativos pode conter custo, preservando a identidade das origens para não reintroduzir punição/emoção duplicadas.")
    section('Conclusão para a próxima fase','O mundo produz histórias individuais com consequências e já permite observar variação entre ambientes. A próxima expansão deve reaproveitar esse material, mas é melhor corrigir primeiro as inconsistências demonstradas e o progresso de objetivos econômicos. A prioridade é melhorar a coerência e o desfecho dos sistemas existentes. Mais guerras, deuses ou política ampla sobre casos duplicados, papéis residenciais conflitantes e forte pressão alimentar ampliariam problemas já visíveis.')
    text=f'# Relatório completo de lore — {s["seed"]}, {s["hours"]}h\n\n'+'\n'.join(parts)
    (folder/'RELATORIO_COMPLETO.md').write_text(text)
    (ROOT/'RELATORIO_LORES_VESPERA_47.md').write_text(text)
    selected=[parts[i] for i in (8,11,12,13,14,15,16,17,18,19,20,21,22)]
    (folder/'INCONGRUENCIAS_E_MELHORIAS.md').write_text('# Incongruências, hipóteses e prioridades\n\n'+'\n'.join(selected))
    (folder/'reproducoes_micro.json').write_text(json.dumps(micro,ensure_ascii=False,indent=2))

def migration_text(folder):
    return str(dict(Counter(e['context']['reason'] for e in rows(folder,'eventos.jsonl.gz') if e['kind']=='MigrationStarted')))

def comparison(summary):
    baseline=json.loads((ROOT/'reports/fase_4/auditoria_global_10000h/resumo.json').read_text())
    at=next(s for s in baseline['samples'] if s['turn']==5000)
    initial=baseline['initial'];now=summary['final']
    return (f"| Indicador | Mira em 5.000h | {summary['seed']} em 5.000h |\n|---|---:|---:|\n"
      f"| Persistentes iniciais | {initial['alive']} | {summary['initial']['alive']} |\n"
      f"| Abstratos iniciais | {initial['abstract']} | {summary['initial']['abstract']} |\n"
      f"| Vivos | {at['alive']} | {now['alive']} |\n| Mortos | {at['dead']} | {now['dead']} |\n"
      f"| Mortos/persistentes iniciais | {100*at['dead']/initial['alive']:.2f}% | {100*now['dead']/summary['initial']['alive']:.2f}% |\n"
      f"| Ataques | {at.get('attacks','não preservado')} | {summary['metrics'].get('AttackExecuted',0)} |\n"
      f"| Mudanças de residência | {at.get('migrations','não preservado')} | {summary['metrics'].get('ResidentMoved',0)} |\n\n"
      "A comparação usa janelas iguais. A geografia/elenco novos resultam de outra seed. As diferenças de dinâmica não isolam exclusivamente a seed: Mira foi observada antes da correção posterior de casos criminais. Também há população inicial diferente e instrumentação mais completa. Não foi carregado nem reexecutado o save de Mira; só foram consultadas suas métricas já preservadas. Mudança de frequência não é automaticamente melhora de qualidade.")

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('folder');a=p.parse_args();build(a.folder)
