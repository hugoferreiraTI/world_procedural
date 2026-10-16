"""Relatório de34 seções, extraído da única auditoria oficial e seus IDs."""
import gzip, json, re, statistics
from collections import Counter,defaultdict
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'reports/fase_4'
AUDIT=OUT/'auditoria_global_10000h'

def load_rows(name):
 with gzip.open(AUDIT/name,'rt',encoding='utf-8') as f:
  for line in f:yield json.loads(line)
def fmt(value):return f'{value:,}'.replace(',','.') if isinstance(value,int) else str(value)
def link(path,label):return f'[{label}](<{ROOT/path}>)'
def readable(text):
 # Espaçamento do texto corrido; caminhos, hashes, versões e código intactos.
 protected=r"(\[[^\]]*\]\(<[^>]*>\)|`[^`]*`|'[^']*'|\b[0-9a-f]{40,64}\b|mvp-[^\s|;.,]+(?:\.[^\s|;,]+)*|SHA256|\bh\d+\b|\bH\d{2}\b)"
 parts=re.split(protected,text)
 for i in range(0,len(parts),2):
  parts[i]=re.sub(r'([A-Za-zÀ-ÿ])(?=\d)',r'\1 ',parts[i])
  parts[i]=re.sub(r'(?<=\d)([A-Za-zÀ-ÿ])',r' \1',parts[i])
  parts[i]=re.sub(r'([:;])(?=[^\s|])',r'\1 ',parts[i])
  parts[i]=re.sub(r',(?=[^\d\s])',', ',parts[i])
 for i in range(1,len(parts),2):
  if parts[i-1] and not parts[i-1][-1].isspace() and (parts[i].startswith(('`','[')) or parts[i-1][-1] in ':;,'):
   parts[i]=' '+parts[i]
 return ''.join(parts)
def generate():
 summary=json.loads((AUDIT/'resumo.json').read_text());m=summary['metrics'];samples=summary['samples']
 continuation=json.loads((OUT/'verificacao_continuidade_pos_auditoria.json').read_text())
 initial=json.loads((AUDIT/'personagens_iniciais.json').read_text())
 towns=json.loads((AUDIT/'mapa_inicial.json').read_text())
 events=sorted(load_rows('eventos.jsonl.gz'),key=lambda e:(e['turn'],e['id']))
 by_id={e['id']:e for e in events};by_actor=defaultdict(list);counts=Counter()
 for e in events:
  counts[e['kind']]+=1
  ids={e['actor_id'],e['target_id']}
  if e['kind']=='WantedIssued':ids.add(e['context'].get('suspect_id'))
  for i in ids:
   if i is not None:by_actor[i].append(e)
 def name(i):return initial.get(str(i),{}).get('name',f'entidade#{i}')
 def count(key):return m.get(key,0)
 by_decision=defaultdict(list)
 def dnear(e,actions=None):
  candidates=[d for d in by_decision.get(e['actor_id'],[]) if d['turn']==e['turn'] and
              (not actions or d['action'] in actions)]
  return candidates[-1] if candidates else None
 def causal(e,depth=8):
  chain=[e];seen={e['id']}
  for _ in range(depth):
   current=chain[-1]
   source=current['context'].get('source_fact') or current['context'].get('fact_id')
   if source not in by_id or source in seen:break
   parent=by_id[source]
   if parent['turn']>current['turn']:break
   chain.append(parent);seen.add(source)
  return list(reversed(chain))
 def event_text(e):
  return f"h{e['turn']} · evento#{e['id']} · **{e['kind']}** · ator#{e['actor_id']}/alvo#{e['target_id']}: {e['description']}"
 def decision_text(d):
  if not d:return 'Não há amostra de utility deste ponto; o evento é comprovado pelo registro, mas o motivo interno completo não foi amostrado.'
  n=d['need'];emotion=d['emotions'];source=d['known_source']
  rival=next((c for c in sorted(d['candidates'],key=lambda c:-c['score']) if c['action']!=d['action']),None)
  alternative=f"; alternativa `{rival['action']}`={rival['score']:.2f}" if rival else ''
  knowledge=f"fato#{source['event_id']} conhecido com confiança{source['confidence']}%" if source else 'fonte ausente da memória curta na amostra; consultar a referência causal/caso institucional'
  return (f"Escolha de {name(d['actor'])}: necessidade`{n['kind'] if n else 'manual'}`; "
    f"prioridade{n['priority']:.2f}; fonte`{n['source']}`; {knowledge}. "
    f"HP{d['health']}, fome{d['hunger']:.1f}, dinheiro{d['money']}, "
    f"raiva{emotion['anger']:.1f}, ressentimento{emotion['resentment']:.1f}. "
    f"Ação`{d['action']}`={d['score']:.2f}{alternative}. "
    'Alternativas foram amostradas na execução; o objetivo pode continuar de uma decisão anterior. Diferenças de até3 pontos admitem desempate pelo RNG determinístico.')
 chosen=[];used=set()
 def add(title,chain,note):
  chain=sorted({e['id']:e for e in chain}.values(),key=lambda e:(e['turn'],e['id']))
  if not chain:return
  key=tuple(e['id'] for e in chain)
  if key in used:return
  used.add(key);chosen.append({'title':title,'events':chain,'note':note})
 # Longest explicit links, never infer relationships merely from surname.
 for e in sorted((e for e in events if e['kind']=='CharacterKilled'),key=lambda e:-len(causal(e)))[:3]:
  chain=causal(e)
  for later in events:
   if later['turn']<e['turn'] or later['turn']>e['turn']+168:continue
   source=later['context'].get('source_fact') or later['context'].get('fact_id')
   victim=initial.get(str(e['target_id']),{})
   same_kingdom=towns.get(str(victim.get('town_id')),{}).get('kingdom_id')==later['target_id']
   succession=(later['kind']=='SuccessionChanged' and later['turn']==e['turn'] and same_kingdom
               and victim.get('profession') in ('governante','conselheiro','estudante'))
   if source==e['id'] or succession:chain.append(later)
  add('Uma morte violenta e suas respostas conhecidas',chain,
      'Autoria da morte consta do evento; somente testemunhas e personagens que receberam informação podem reagir. Eventos posteriores entram com vínculo explícito; uma sucessão só pode entrar na mesma hora e no reino de uma vítima da família real.')
 # Actual migration chain with same actor, named starting reason, visitor/census distinction.
 starts=[e for e in events if e['kind']=='MigrationStarted']
 for reason in ('wanted','poverty','threat','family'):
  for e in starts:
   if e['context'].get('reason')!=reason:continue
   later=[x for x in by_actor[e['actor_id']] if e['turn']<=x['turn']<=e['turn']+240 and
          x['actor_id']==e['actor_id'] and x['kind'] in ('MigrationArrived','ResidentMoved','TrainingStarted','ProfessionChanged')]
   if not any(x['kind']=='ResidentMoved' for x in later):continue
   prior=[x for x in by_actor[e['actor_id']] if 0<=e['turn']-x['turn']<=72 and
          (x['kind'] in ('ItemStolen','CharacterAttacked','CharacterThreatened','WantedIssued','CharacterCaptured'))]
   prior=prior[-3:]
   add(f'Mudança de residência por {reason}: {name(e["actor_id"])}',prior+[e]+later,
       'A razão de partir vem do estado/decisão registrada. Eventos anteriores do mesmo personagem são contexto temporal; não representam causalidade comprovada quando não existe source_fact. Chegada é visita; ResidentMoved altera o censo posteriormente.')
   break
 # Representative actual endpoints and competing nonviolent decisions.
 for kind,title in [('RestitutionGiven','Devolução material real'),('ApologyGiven','Pedido de desculpas'),
                    ('CharacterCaptured','Procura, rendição/incapacidade e captura'),
                    ('FirstAidGiven','Socorro com recursos reais'),('ProtectionGiven','Intervenção de terceiro'),
                    ('CharacterFled','Fuga com deslocamento físico'),('CharacterSurrendered','Rendição interrompendo confronto'),
                    ('CharacterWithdrew','Retirada sem ataque'),('ConflictForgiven','Perdão'),
                    ('CharacterInsulted','Humilhação e pressão social'),('SuccessionChanged','Morte alterando sucessão')]:
  matches=[e for e in events if e['kind']==kind and (kind!='ProtectionGiven' or e['context'].get('physical'))]
  if not matches:continue
  best=max(matches[:10000],key=lambda e:(len(causal(e)),-e['id']))
  chain=causal(best)
  if kind=='SuccessionChanged':
   # Identify royal victim via initial profession/town and kingdom, not just hour.
   related=[x for x in events if x['turn']==best['turn'] and x['kind'] in ('CharacterDied','CharacterKilled')
            and initial.get(str(x['target_id']),{}).get('profession') in ('governante','conselheiro','estudante')
            and towns.get(str(initial.get(str(x['target_id']),{}).get('town_id')),{}).get('kingdom_id')==best['target_id']]
   chain=related+chain
  if kind in ('CharacterCaptured','CharacterSurrendered','CharacterFled','CharacterWithdrew'):
   before=[x for x in by_actor[best['target_id'] or best['actor_id']] if 0<=best['turn']-x['turn']<=24
           and x['kind'] in ('CharacterAttacked','CharacterSurrendered','WantedIssued','CharacterConfronted')]
   chain=before[-2:]+chain
  add(title,chain,'Sequência retirada de eventos reais; não se presume reconciliação duradoura, redenção ou êxito posterior além do que os registros comprovam.')
 # An explicitly linked social chain that crosses several actions.
 chains=sorted((causal(e,12) for e in events if e['kind'] in ('CharacterAttacked','RestitutionGiven','ApologyGiven','CharacterThreatened')),
               key=lambda c:-len(c))
 for chain in chains:
  if len(chain)>=5:
   add('Cadeia social longa com fontes explícitas',chain,'Cada elo aponta para o source_fact do próximo; a sequência não foi inventada a partir de nomes ou proximidade.')
   if sum(s['title'].startswith('Cadeia social longa') for s in chosen)>=2:break
 rich_crime=None
 rich_decision=None
 economic_crime_attempts=Counter()
 wanted_decisions={(e['actor_id'],e['turn']) for story in chosen for e in story['events'] if e['actor_id'] is not None}
 for d in load_rows('decisoes.jsonl.gz'):
  if (d['actor'],d['turn']) in wanted_decisions:by_decision[d['actor']].append(d)
  if d['action']=='steal_person':
   economic_crime_attempts[d['need']['kind']]+=1
   if rich_crime is None and d['money']>=20 and d['need']['kind']=='advancement':
    match=next((e for e in by_actor[d['actor']] if e['kind']=='ItemStolen' and e['actor_id']==d['actor']
                and e['turn']==d['turn'] and e['target_id']==d['target']),None)
    if match:rich_crime,rich_decision=match,d
 if rich_crime:
  add('Roubo associado a avanço financeiro, com reserva monetária', [rich_crime],
      'A necessidade amostrada é avanço financeiro e o ator possuía ao menos20 moedas. O bem roubado foi provisão; não se presume ganho em dinheiro nem necessidade imediata de comer.')
  by_decision[rich_decision['actor']].append(rich_decision)
 for story in chosen:
  # A notícia que o ator conhecia na execução também é evidência causal,
  # mesmo quando o evento final referencia a origem do delito diretamente.
  extra=[]
  for e in story['events']:
   d=dnear(e)
   if d and d['known_source']:
    source=by_id.get(d['known_source']['event_id'])
    if source and source['turn']<=e['turn']:extra.append(source)
  story['events']=sorted({e['id']:e for e in story['events']+extra}.values(),key=lambda e:(e['turn'],e['id']))
 def reading(story):
  chain=story['events'];kinds={e['kind'] for e in chain}
  people={i for e in chain for i in (e['actor_id'],e['target_id']) if str(i) in initial}
  span=chain[-1]['turn']-chain[0]['turn']
  if 'MigrationStarted' in kinds:
   start=next(e for e in chain if e['kind']=='MigrationStarted')
   reason={'wanted':'procura criminal conhecida','poverty':'pobreza persistente','threat':'ameaça conhecida'}.get(start['context']['reason'],start['context']['reason'])
   origin=towns[str(start['context']['origin'])]['name'];destination=towns[str(start['context']['destination'])]['name']
   return f"{name(start['actor_id'])} saiu de {origin} para {destination} por {reason}. A partida, a chegada e a fixação constam do registro, com{span}h entre os primeiros e últimos elos exibidos. A viagem muda o contexto material do personagem; não comprova melhora financeira posterior."
  if 'CharacterKilled' in kinds:
   death=next(e for e in chain if e['kind']=='CharacterKilled')
   return f"A disputa exibida durou{span}h e envolveu{len(people)} pessoas, terminando com {name(death['actor_id'])} matando {name(death['target_id'])}. Há respostas apoiadas em agressões conhecidas; a origem mais antiga pode estar fora do recorte. A consequência física é real, mas repetição de golpes reduz a variedade dentro do arco."
  if 'RestitutionGiven' in kinds:return 'O autor devolveu um bem rastreável após conhecer a cobrança. Este é um desfecho material de reparação: a resposta social produziu outra decisão, sem restituição automática.'
  if 'FirstAidGiven' in kinds:return 'A pressão de proteção foi resolvida por auxílio físico usando recursos do ajudante. É uma alternativa concreta à escalada violenta; o evento não comprova cura completa ou segurança duradoura.'
  if 'CharacterCaptured' in kinds:return 'A sequência chegou a uma consequência institucional com detenção e multa. O guarda decidiu com fontes próprias; os limites e a correção posterior dos casos acumulados estão no relatório final.'
  if 'SuccessionChanged' in kinds:return 'A morte do governante mudou a chefia ou encerrou a linhagem disponível. A causa exibida determina a interpretação; uma morte por privação não é descrita como assassinato.'
  if rich_crime and rich_crime['id'] in {e['id'] for e in chain}:return 'Este caso confirma que pressão de avanço financeiro também pode escolher crime com fome moderada e dinheiro disponível. A transferência foi de alimento: não houve ganho monetário comprovado neste elo.'
  return f"O recorte reúne{len(chain)} fatos ao longo de{span}h, com{len(people)} pessoas identificadas. A variação de resposta está documentada; continuidade futura ou reconciliação permanente exigiriam outros fatos."
 story_lines=['# Histórias reais da Fase4','',
 'Campanha única Mira global,10.000h. Horas contadas desde o mundo gerado, sem histórico econômico prévio. Nomes não identificam pessoas: os IDs dos eventos/atores fazem a ligação. Uma sequência temporal é indicada separadamente de causalidade explícita.','',
 'Os registros compactados contêm todos os eventos selecionados e as decisões amostradas. Ataques, capturas, fugas, rendições e viagens têm amostragem completa de execução; ações repetidas sem nova fonte são amostradas a cada24h.','',
 '## Avaliação da qualidade','',
 'A melhora mais concreta é a existência de consequências entre pessoas: uma cobrança pode produzir devolução; agressões podem provocar proteção de terceiros; a procura pode levar à fuga e a uma residência nova. H07 mostra reparação material, H10 mostra auxílio com recursos e H20 mostra crime associado a avanço financeiro com dinheiro disponível. As decisões amostradas permitem distinguir esses casos.','',
 'As cadeias violentas também repetem muitos golpes e respostas de proteção. Isso cria continuidade causal, mas não garante variedade dramática. Migração por pobreza apareceu pouco, e migração por família não foi comprovada. Fome, dinheiro curto e alta pressão emocional ainda limitam o repertório. Os exemplos são recortes: eventos intermediários não exibidos podem existir, e um source_fact explica a referência da decisão, sem representar sozinho toda a história do personagem.','']
 evidence=[]
 for index,story in enumerate(chosen,1):
  story_lines += [f'## H{index:02d} — {story["title"]}','',reading(story),'',story['note'],'']
  for e in story['events']:
   story_lines.append('- '+event_text(e))
   d=dnear(e)
   if d:
    story_lines += ['','  '+decision_text(d),'']
   evidence.append({'story':index,'event':e,'decision':d})
  story_lines+=['']
 # Clearly list requested chains absent from actual evidence.
 story_lines += ['## O que não foi comprovado','',
 'Ter combate implementado não prova todas as histórias desejadas. Não se presume guerra, vingança concluída, ajuda a inimigo, mudança de carreira causada por crime, familiar migrando ou facção política. A tabela de eventos e os exemplos acima delimitam o que ocorreu. Morte natural seguida de luto é válida, mas não vira assassinato no relatório.','']
 (OUT/'HISTORIAS_EMERGENTES.md').write_text(readable('\n'.join(story_lines)),encoding='utf-8')
 (OUT/'evidencias_historias.json').write_text(json.dumps(evidence,ensure_ascii=False,indent=2),encoding='utf-8')
 migration_reasons=Counter(e['context'].get('reason') for e in starts)
 ends=Counter(e['context'].get('reason') for e in events if e['kind']=='ConflictEnded')
 unique_migrants=len({e['actor_id'] for e in events if e['kind']=='ResidentMoved'})
 migration_routes=Counter((e['context'].get('origin'),e['context'].get('destination')) for e in starts)
 route_lines=['| Origem | Destino | Partidas |','|---|---|---:|']
 for (origin,destination),amount in migration_routes.most_common(10):
  route_lines.append(f"| {towns.get(str(origin),{}).get('name',origin)} (#{origin}) | {towns.get(str(destination),{}).get('name',destination)} (#{destination}) | {amount} |")
 deaths=summary['death_causes'];total=sum(deaths.values())
 violent=deaths.get('combat',0);hunger=deaths.get('hunger',0)+deaths.get('both',0)
 attacks_per_actor=Counter(e['actor_id'] for e in events if e['kind'] in ('CharacterAttacked','CharacterKilled'))
 crimes_witnessed=sum(bool(set(e['witnesses'])-{e['actor_id']}) for e in events if e['kind']=='ItemStolen')
 food_carried_deaths=sum(r.get('food',0)>0 for r in summary['death_records'].values() if r['cause'] in ('hunger','thirst','both'))
 deprivation_after_attack=[]
 for victim,r in summary['death_records'].items():
  if r['cause'] not in ('hunger','thirst','both'):continue
  attacks=[e for e in by_actor[int(victim)] if e['kind']=='CharacterAttacked' and e['target_id']==int(victim)
           and 0<=r['turn']-e['turn']<=48]
  if attacks:deprivation_after_attack.append({'victim':int(victim),'death':r,'recent_attack':attacks[-1]})
 witness_counts=[len(e['witnesses']) for e in events if e['kind'] in ('ItemStolen','CharacterAttacked','CharacterKilled')]
 social_events={'CharacterConfronted','CharacterThreatened','RestitutionDemanded','RestitutionGiven','CharacterWarned',
                'CharacterInsulted','ApologyGiven','ImmediateHelpRequested','ThirdPartyAlerted','CalmingAttempted','ConflictForgiven'}
 emotion=samples[-1]['emotions']
 metrics_rows=['| Evento/ação | Quantidade |','|---|---:|']+[f'| {k} | {fmt(v)} |' for k,v in sorted(counts.items())]
 population_rows=['| Hora | Vivos | Mortos | Lesionados | Raiva média | Desespero médio | Tempo acumulado(s) |','|---:|---:|---:|---:|---:|---:|---:|']
 for s in samples:
  emotion_at=s.get('emotions',{})
  population_rows.append(f"| {s['turn']} | {s['alive']} | {s['dead']} | {s.get('injured','não preservado')} | {emotion_at.get('anger',{}).get('mean','não preservado')} | {emotion_at.get('desperation',{}).get('mean','não preservado')} | {s['seconds']} |")
 histories=link('reports/fase_4/HISTORIAS_EMERGENTES.md','histórias e decisões reais')
 secs=summary['seconds_per_1000h'];size=summary['save_bytes']/1048576
 sections=[]
 def section(title,text):sections.append(f'## {len(sections)+1}. {title}\n\n{text}\n')
 section('Resumo executivo',f"Fase4 implementada como`mvp-5-fase4`. Mira começou com1.728 NPCs persistentes e4.338 abstratos, seis reinos e73 localidades. Em10.000h ocorreram{fmt(count('AttackExecuted'))} ataques,{violent} mortes em combate,{fmt(count('CharacterCaptured'))} capturas e{fmt(count('ResidentMoved'))} mudanças de residência ({unique_migrants} indivíduos). Mortes totais:{total}; fome/privação continua relevante ({dict(deaths)}). Qualidade deve ser avaliada pelas cadeias causais em {histories}, não só pelo número de eventos.")
 section('Comparação com mvp-4-fase3.2-final',"| Sistema | Antes | Fase4 |\n|---|---|---|\n| NPCs Mira |432 |1.728 inicialmente |\n| Abstratos Mira |59.350 |4.338 inicialmente |\n| Geografia |6 reinos/73 localidades |Idêntica |\n| Combate NPC/jogador |Ausente |Ataque, defesa, fuga, rendição e proteção física |\n| Ferimentos |Ausente |HP+lesão com efeitos e recuperação gradual |\n| Guarda |Investiga/multa roubo conhecido |Casos, evidência própria, procura e captura mínima |\n| Migração autônoma |Ausente |Viagem física, visita, transferência de residência |\n| Emoções |Traços/pressões pessoais |Estado dinâmico causal e adaptação lenta |\n| Política/religião ampla |Ausente |Segue fora do escopo |\n\nA comparação demográfica redimensiona o total por decisão do usuário; não preserva59.782 habitantes. A campanha anterior de Mira teve119 mortes/432 em10.000h, mas esse número não é um experimento controlado contra o novo elenco e economia. O núcleo anterior está preservado em baseline_code.")
 section('Sistemas reaproveitados','Need/Goal/Utility continuam escolhendo todas as ações. Reutilizados fisiologia, alimentação preventiva, renda/crédito, produção, inventário e transferências, navegação, percepção/gossip, relações, quests, população, morte e sucessão. Novos serviços enumeram/executam alternativas e consequências; não há CombatAI paralelo nem ataque acionado diretamente por callback. Estado emocional é modificador; crime/ataque/fuga são soluções/ações; perseguição e mudança são pressões/objetivos executáveis.')
 section('População persistente nova','Multiplicador4 aplicado após toda a geografia e personagens originais. Adiciona famílias de três, relações próximas esparsas e distribuição profissional, preservando identidades antigas. O total original seria incompatível com2–3 abstratos por persistente sem criar15–20 mil NPCs; o usuário pediu equilíbrio. Configurações reduzidas mantêm o elenco anterior por padrão; densidade pode ser explícita. Nenhuma pessoa nova é criada por migrar.')
 section('Relação persistente/abstrata',f"Mira inicial:4.338/1.728={4338/1728:.3f} abstratos por persistente. Capitais2,1; cidades2,5; vilas2,7 aproximadamente, com arredondamento. Total inicial6.066. A proporção local inicial é verificada nos testes. Migração e mortes podem mudar a proporção posterior; não há reposição mágica para conservar o índice. Abstratos finais:{fmt(samples[-1]['abstract'])}; continuam consumidores/trabalhadores agregados.")
 section('Performance',f"{fmt(count('NPCDecision'))} decisões;{fmt(sum(v for k,v in counts.items()))} eventos relevantes preservados no arquivo causal. Tempo real total:{summary['runtime_seconds']}s;{secs:.3f}s/1.000h, incluindo registro de auditoria. Memória máxima aproximada na simulação:{samples[-1]['memory_peak_mib']}MiB; após persistência:{summary.get('peak_after_persistence_mib')}MiB. Save:{size:.2f}MiB; serialização:{summary['save_seconds']}s; carga:{summary['load_seconds']}s. Medidas vêm de perf_counter e ru_maxrss em Linux; não são benchmark universal. Índices espaciais/censo local, casos ativos e fila de expiração evitam pesquisa de todos os NPCs por encontro. Histórico factual e casos arquivados continuam aumentando o save. Trabalho pago/creditado/sem insumo/saturado: {dict((k,v) for k,v in m.items() if k.startswith('WorkOutcome:'))}.")
 section('LOD',f"Fisiologia fecha toda hora para todos. Decisões:ativo1h por conflito/pressão vital/evento/jogador próximo/viagem; local3h para importantes,6h comuns; fundo12h em casa. Distribuição final:{samples[-1]['lod']}. Promoção muda quando será tomada a decisão, sem disparar ação automática. Combate executa uma operação física por decisão, sem converter seis horas de LOD em seis ataques simultâneos.")
 section('Estados emocionais',f"Raiva, ressentimento, humilhação e desespero são separados dos onze traços. Fontes são agressão/roubo/humilhação conhecidos, perdas familiares, privação e precariedade própria; autoridade rica não é culpada sem evidência. Estado final:{emotion}. Causas factuais acumuladas:{summary.get('emotion_causes')}. Decaimento/apoio/reparação reduzem pressão; uma contribuição factual persistida impede aumento repetido ao reaprender a mesma notícia.")
 section('Alteração lenta de personalidade',f"{count('PersonalityAdapted')} adaptações. Acúmulo de pressão e intervalo mínimo720h dão+1 em vingatividade e independência por adaptação, máximo cinco. Uma ofensa não substitui personalidade-base. O modelo é mínimo e não representa desenvolvimento psicológico completo; estados causais e mudanças são persistidos.")
 section('Grievances',f"{count('GrievanceCreated')} grievances criadas;{samples[-1]['grievances']} mantidas pelos vivos no final. Cada registro possui alvo, causa, intensidade, fonte e tempos. Só há atribuição direcionada ao ator de um fato conhecido. Lista pessoal limitada16; intensidade decai. Perda sem autoria conhecida pode gerar luto, sem apontar automaticamente o assassino verdadeiro.")
 section('Novas ações sociais',f"{fmt(sum(counts[k] for k in social_events))} eventos sociais estruturados registrados. Confrontar, ameaçar, cobrar, avisar, insultar, desculpar, retirar-se, pedir auxílio, alertar, acalmar e perdoar competem com fuga/denúncia/ataque. Abordagens repetidas no mesmo episódio têm controle. Cobrança gera pressão; devolver é escolha do autor e transfere um bem real. Exemplos:{histories}.")
 section('Crime',f"Roubos:{fmt(count('ItemStolen'))}; roubos com outro participante/testemunha além do autor:{fmt(crimes_witnessed)}; denúncias:{fmt(count('ThreatReported'))}; procuras emitidas:{fmt(count('WantedIssued'))}. Roubo serve comida, dinheiro ou avanço; não depende de profissão/crimeNeed. Mercador presente é oportunidade observável, sem consulta remota do inventário. Riqueza/ganância podem gerar crime, mas o relatório não atribui esse motivo só porque ocorreu roubo: consulte a necessidade amostrada. Crime e briga ainda podem ter raízes alimentares. Tentativas amostradas de roubo pessoal por necessidade:{dict(economic_crime_attempts)}; tentativa não equivale a roubo concluído.")
 section('Reação da vítima',f"Pressão própria por agressão/ofensa/procura institucional pode produzir confronto, denúncia, devolução, desculpa, defesa, fuga, rendição ou ataque. Foram criadas{count('NeedCreated:response')} necessidades de resposta. A ameaça conhecida e a força percebida participam da utility; raiva não executa violência. Ataque requer alternativa viável, alvo vivo presente e ausência de rendição/detenção/trégua.")
 section('Testemunhas',f"Crimes/ataques/mortes observados tiveram média{statistics.mean(witness_counts):.2f} participantes/testemunhas por evento, contando os envolvidos. Acesso é célula local e participantes; gossip percorre contatos com confiabilidade própria. Avisos de procurado usam a cidade como alvo para evitar ensinar suspeito remoto. Guards têm fontes/gravidade/status/localização individuais, mesmo quando compartilham registro institucional.")
 section('Combate',f"Ataques:{fmt(count('AttackExecuted'))}; conflitos físicos iniciados:{fmt(count('ConflictStarted'))}; defesas:{fmt(count('CharacterDefended'))}. Dano=(4+bônus arma)×(0,5+HP/200)×(1−lesão/250), bônus até12, variação−2..+2, defesa×0,45, mínimo1. Arma própria/qualidade são objetivas; força alheia usa aparência aproximada/sinais visíveis. Encerramentos:{dict(ends)}. ConflictEnded também registra encerramento social, portanto não deve ser dividido cegamente por ConflictStarted. Maior número de ataques por um ator:{max(attacks_per_actor.values(),default=0)}; repetição merece avaliação nos exemplos.")
 section('Ferimentos',f"Lesão0–100 além do HP. Lesão≥20 reduz passos por lote e horas produtivas do lote, além de poder de combate e fuga; mínimo de uma operação permanece. Lesão≥6 cria pressão para recuperar. Feridos vivos no final:{samples[-1]['injured']}. Um defensor pode interceptar dano; não pode interceptar o próprio ataque nem atuar rendido/detido. Não há anatomia, sangramento ou sistema de membros.")
 section('Tratamento',f"Socorros iniciais:{fmt(count('FirstAidGiven'))}. Exigem paciente vivo presente, lesão≥6, uma provisão e uma água do ajudante; aliviam6 de lesão e2HP. Descanso elegível recupera lentamente2 de lesão/hora. Sem profissão de curandeiro/hospital, seek_treatment significa procurar local seguro e descansar. Auxílio solicitado cria uma necessidade para outro NPC; não obriga uma cura automática.")
 section('Fuga/rendição',f"Fugas físicas:{fmt(count('CharacterFled'))}; retiradas:{fmt(count('CharacterWithdrew'))}; rendições:{fmt(count('CharacterSurrendered'))}; tentativas fracassadas:{fmt(count('EscapeFailed'))}. Fuga move uma etapa física se possível; tentativa fracassada consome a hora. Rendição impede continuar o ataque e permite captura. Incapacidade≤12HP também encerra confronto. Trégua48h reduz reataque imediato; o conflito social pode continuar depois.")
 section('Mortes violentas',f"Mortes em combate:{violent} de{total} ({violent/max(1,total)*100:.2f}%); causas completas:{deaths}. Mortes por privação com comida carregada:{food_carried_deaths}. Mortes por privação com ataque nas48h anteriores:{len(deprivation_after_attack)}; esta é associação temporal, não prova de causalidade nem contagem adicional de assassinatos. O mesmo finish_death mantém corpo/posses, encerra ações, emite fato, reduz censo uma vez e aciona sucessão. Morto não decide/ataca. Causa autoinfligida abstrata:{deaths.get('self_harm',0)}; condição rara exige desespero extremo prolongado, múltiplas perdas conhecidas e isolamento, com apoio impedindo elegibilidade. Nenhuma descrição de método é implementada.")
 section('Perseguição',f"Buscas locais:{fmt(count('PursuitSearch'))}; localizações:{fmt(count('SuspectLocated'))}; procuras expiradas:{fmt(count('PursuitEnded'))}. Destino é a última posição conhecida por aquele guarda, atualizada por observação/fato novo; não há consulta à posição remota atual do suspeito. Até três buscas sem avanço e janela168h limitam o episódio. A busca de perseguidores é local; ela não atravessa automaticamente mapas atrás de fugitivos. Cada suspeito reutiliza o objetivo do guarda; mudança de pista permite nova busca.")
 section('Procurados',f"Registros institucionais:{len(summary['wanted'])}; estados finais:{dict(Counter(r['status'] for r in summary['wanted'].values()))}. Fonte, jurisdição, suspeito, gravidade, confiança e tempo são persistidos. Autorização exige guarda local/confiança≥60. Força legal/autodefesa contextual não cria delito automaticamente. Resolução remota não vira conhecimento instantâneo dos outros guardas; conhecimento próprio ou prazo encerram a procura.")
 section('Captura',f"Capturas:{fmt(count('CharacterCaptured'))}; liberações:{fmt(count('CharacterReleased'))}; intervenções com multa:{fmt(count('GuardResponded'))}. Capturar exige presença e rendição/incapacidade. Multa usa até5 moedas existentes, transferidas ao caixa local; detenção12h é temporária, sem teleporte. Caso multado encerra quando a resolução é conhecida; não autoriza multas repetidas pelo mesmo fato. O sistema não é tribunal, investigação probatória completa ou prisão simulada.")
 section('Migração',f"Partidas:{fmt(count('MigrationStarted'))}; chegadas como visitante:{fmt(count('MigrationArrived'))}; mudanças de residência:{fmt(count('ResidentMoved'))}; indivíduos:{unique_migrants}; motivos das partidas:{dict(migration_reasons)}. Rota conhecida, provisões, portão, caminho externo, entrada e24h de visita precedem o censo. Origem perde1, destino ganha1; abstratos não viram novos migrantes. Trabalho usa residência/instalação compatíveis; visitante pode comprar/coletar no local físico. Após fixação336h de adaptação restringem nova mudança.")
 section('Impacto em família/luto/vingança',f"Luto criado:{fmt(count('NeedCreated:grief'))}; vingança/reparação criada:{fmt(count('NeedCreated:revenge'))}; proteção criada:{fmt(count('NeedCreated:protection'))}. São contagens de ativações, não pessoas distintas nem vinganças concluídas. Famílias esparsas ampliam a rede afetada; informação ainda precisa alcançar cada membro. Assassinato não revela autoria a familiar remoto. Memória curta/gossip e expiração de necessidades limitam continuidade; esse limite aparece nas histórias interrompidas.")
 section('Impacto em reputação',f"Roubo, agressão ilegal, ameaça, auxílio, proteção e reparação mudam reputação segundo confiança/contexto. Interpretação de morte continua contextual à relação/lealdade; força legítima não é marcada automaticamente como crime. Eventos de ajuda:{fmt(count('HelpGiven'))}; proteção física e companhia:{fmt(count('ProtectionGiven'))}; desculpas:{fmt(count('ApologyGiven'))}; restituições:{fmt(count('RestitutionGiven'))}. Não há reputação universal, propaganda ou julgamento objetivo atribuído a todo o mundo.")
 section('Testes direcionados','Vinte regressões compostas passaram: dano/arma/defesa/intercepção; morte/censo/corpo/sucessão; testemunha/culpado desconhecido; fuga/rendição; escolha violenta e denúncia; guarda informado versus remoto; captura/detenção/liberação; devolução material; emoções/dedup/adaptação; socorro; pedido de ajuda; rota/visita/residência; comércio de visitante; densidade/geografia; save/load determinístico; LOD/fisiologia; desespero/apoio; caso encerrado/objetivo reutilizado; auto-intercepção. A suíte anterior179 foi executada uma vez:12 falhas,10 corrigidas e reavaliadas,2 expectativas antigas atualizadas e reavaliadas. Os logs preservam todas as etapas; não houve segunda execução completa.')
 section('Auditoria curta','Primeira tentativa interrompida pelo validador em500h: auto-intercepção do protetor4058, eventos423845/423846 em495h. Arquivos preservados. Corrigidos também repetição de multas e migração circular. Auditoria corrigida1000h:1.604 vivos,124 mortes (110fome/14combate),8.062 ataques,90capturas,290mudanças;417,383s. Instrumentação falhou somente na continuação após escrever o checkpoint1000h, por callback ligado a arquivo fechado. Resumo/continuação24h recuperados do checkpoint, sem repetir campanha. Depois foram corrigidos limites dos objetivos/índices e regressões antes de congelar a oficial.')
 section('Auditoria global de10.000h',f"UMA campanha Mira global sem jogador, geração inicial com histórico0h e código congelado antes da execução. SHA256 auditado:{summary['core_sha256']}. Invariantes verificados a cada100h; último estado:{samples[-1]['invariants']}. O save10000h foi escrito e carrega; a comparação original de24h divergiu ({summary['continuation_24h_equal']}). Depois da campanha foi corrigido o tratamento de múltiplos casos conhecidos e a remoção indevida do índice institucional. A verificação curta posterior compara o motor contínuo10000→10024 com uma recarga em10012: igualdade exata={continuation['exact_equal']}; índice ativo consistente a cada hora={continuation['justice_active_index_equal_to_world_each_hour']}. SHA256 entregue:{continuation['core_sha256']}. Esta verificação não substitui nem repete a campanha oficial.\n\nO resumo foi recuperado dos arquivos já escritos; os valores de vivos/mortos/tempo intermediários vêm do log. Emoções/lesões intermediárias não foram preservadas após a falha e estão identificadas como ausentes. Não houve três longas nem replay integral10.000h.\n\n"+'\n'.join(population_rows))
 section('Métricas de interação','Contagens de eventos; ativação de necessidade não equivale a história resolvida. IDs e decisões estão nos arquivos causais.\n\n'+'\n'.join(metrics_rows))
 section('Histórias emergentes',f"Foram selecionados{len(chosen)} exemplos reais, com IDs, conhecimento amostrado, necessidade, prioridade, estado emocional, alternativa escolhida e comparação de utility. Leia {histories}. Os exemplos incluem finais cotidianos, fuga, reparação, proteção e captura quando presentes; os desejos de história não viram eventos fictícios no relatório.")
 section('Histórias longas','O arquivo de histórias distingue vínculos explícitos source_fact de antecedentes temporais do mesmo NPC. Migração pode cruzar crime/procura, deslocamento, chegada e residência; mortes podem cruzar autoria, testemunha, luto/reparação e consequência institucional. Só se inclui carreira posterior quando houve evento real; apenas estar na mesma cidade/sobrenome não prova relação familiar ou causalidade. Nem toda cadeia terminou: prazo, perda de informação, necessidade vital e afastamento interrompem arcos.')
 section('Bugs descobertos','1. RNG após ataque não sincronizado antes de salvar: corrigido em Goal.execute sem mutar ação inválida.\n2. Protetor interceptava próprio ataque ou interceptava rendido: filtro corrigido.\n3. Caso resolvido autorizava multa/procura repetidas: resolução e fonte/status próprios corrigidos.\n4. Migração repetida sem adaptação:336h e reavaliação econômica local.\n5. Objetivo novo por caso e varredura crescente de arquivados: objetivo por suspeito, índice ativo/fila de prazo.\n6. Compra de refeição em mapa sem cidade gerava KeyError: retorna recusa sem avanço.\n7. Reaprender notícia fora da memória curta podia repetir emoção: contribuição factual persistida.\n8. Fuga fracassada do jogador não consumia hora: tentativa válida corrigida.\n9. Instrumentação mantinha callback após fechar arquivo: desligado antes da verificação pós-save.\n10. Densificação afetou cenários reduzidos usados pelas regressões econômicas: configuração explícita/escala anterior preservada.\n\nOs originais dos testes e código anteriores permanecem no baseline. A campanha oficial foi executada somente após essas correções e congelamento.')
 section('Limitações','Combate é local e simples; não há anatomia, hospital/curandeiro, julgamento completo, perseguição universal ou recrutamento tático. Migração usa poucas rotas públicas conhecidas, exige reservas e usa24h para residência, sem empregos garantidos. Apoio limitado não assegura cura. Abstratos seguem agregados. Perseguição não atravessa mapas automaticamente e não procura todas as cidades. A amostragem detalhada não inclui a ação antiga de roubo do mercado: nesses elos, o evento/fonte são comprovados, mas o estado/utility original do ladrão não foi amostrado. Metadados de destino para família/trabalho ainda não são alimentados completamente, limitando esses motivos de migração. Texto dos eventos sociais ainda é simples e em alguns casos mostra o nome interno da ação. Memórias/gossip/necessidades com prazo ainda encurtam algumas histórias; registros históricos/factuais ampliam saves. A frequência de ataques não é sinônimo de profundidade e comida pode continuar origem de muitos conflitos. Duas antigas expectativas de teste foram alteradas porque proibiam comportamentos agora solicitados. Saves da Fase3.2 não carregam nesta versão: núcleo/saves antigos estão preservados.')
 section('Preparação para Fase5','Prontos para reutilizar: estados emocionais causais, fontes/culpados conhecidos, grievances, violência/ferimentos, defesa/fuga/rendição, testemunhas, reputação, casos locais, migração, perdas familiares, morte/sucessão e registros persistidos. Ainda NÃO implementados: guerras, exércitos, cerco, diplomacia completa, revoluções, facções políticas completas, disputa formal do trono, deuses/religião ativa, nascimento, envelhecimento, herança, caravanas e destruição de cidades. São etapas futuras; esta campanha não comprova sua emergência.')
 # Evidência da versão entregue é separada da campanha congelada.
 sections[5]+='\n'+summary['persistence_timing_scope']+' Memória após persistência foi medida no processo de recuperação; o pico original dessa etapa não foi preservado. O save de cerca de337MiB e a carga custosa são limites relevantes do protótipo.\n'
 sections[22]+='\nRotas com mais partidas; contagens de viagens, não de moradores finais:\n\n'+'\n'.join(route_lines)+'\n'
 sections[24]+=f"\nRumores/informação: {fmt(count('RumorShared'))} / {fmt(count('InformationShared'))}. O relatório registra fatos que mudam reputação e as fontes das histórias; não preservou uma série temporal de cada reputação individual, portanto não apresenta uma contagem inventada de opiniões alteradas.\n"
 sections[25]+='\nOs20 casos passaram novamente após a correção de casos acumulados. O caso19 foi ampliado com dois guardas, resolução desconhecida, nova agressão, bloqueio de multa insuficiente e reconstrução do índice a partir de um checkpoint com casos sobrepostos. Log: '+link('reports/fase_4/testes_pos_auditoria.txt','regressões posteriores')+'.\n'
 sections[25]+='\nCinco regressões antigas diretamente relacionadas a denúncia e continuidade também passaram após a correção, incluindo continuidade80+200h com recarga. Log: '+link('reports/fase_4/regressoes_legadas_relacionadas.txt','regressões legadas relacionadas')+'.\n'
 sections[31]=sections[31].replace('A campanha oficial foi executada somente após essas correções e congelamento.',
  'A campanha oficial foi executada após os dez itens acima e o congelamento.\n\n11. Inspeção final e verificação pós-save descobriram incoerência entre caso selecionado, caso executado e índice institucional: corrigida DEPOIS da campanha. Um guarda podia escolher agressão grave, executar caso antigo de roubo e apagar um caso novo do índice. A recarga reconstruía esse caso e alterava a execução. A escolha agora agrupa casos por suspeito e gravidade conhecida; a execução usa a mesma escolha; multas pequenas não resolvem casos graves; fechamento mantém outros casos ativos, inclusive desconhecidos pelo guarda. Microcenário no código congelado reproduziu a divergência. A primeira correção teve continuidade exata, mas o verificador detectou um índice incompleto diante de casos antigos sobrepostos: o índice passou a manter todos os casos ativos por suspeito. As duas evidências anteriores foram preservadas.\n\nA correção posterior não participou dos10.000h oficiais. Foi validada por regressões e pela continuação curta documentada na seção28; não houve segunda campanha longa.')
 sections[32]+='\nLimites medidos: fome ou fome+sede representam '+f'{hunger/max(1,total)*100:.2f}%'+f' das mortes; desespero médio final {emotion["desperation"]["mean"]}. O repertório social aumentou, mas essas pressões e o save volumoso ainda precisam de equilíbrio e contenção de histórico. A campanha original também teve falha de continuidade, corrigida e verificada em escopo curto posterior.\n'
 emotional_rows=['| Estado | Média dos vivos | Vivos com valor≥50 | Máximo |','|---|---:|---:|---:|']
 for key,label in [('anger','Raiva'),('resentment','Ressentimento'),('humiliation','Humilhação'),('desperation','Desespero')]:
  v=emotion[key];emotional_rows.append(f"| {label} | {v['mean']} | {v['over50']} | {v['maximum']} |")
 sections[7]='## 8. Estados emocionais\n\nRaiva, ressentimento, humilhação e desespero são separados dos onze traços. Agressões, roubo, humilhação e perdas precisam ser conhecidos; precariedade e privação próprias também contribuem. Governante rico não vira culpado sem evidência.\n\n'+'\n'.join(emotional_rows)+f"\n\nContribuições factuais acumuladas por personagem: {summary['emotion_causes']}. São interpretações, não crimes únicos: o mesmo fato pode afetar testemunhas diferentes. Apoio/reparação e decaimento reduzem pressão. A contribuição persistida evita reaprender a mesma notícia como novo choque. O desespero médio alto é um sinal de desequilíbrio, não uma medida de qualidade narrativa.\n"
 sections[11]+='\nO crime financeiro mínimo ainda transfere provisões: a necessidade amostrada de dinheiro/avanço explica a escolha, mas não comprova ganho em moedas. Não há cadeia autônoma específica de revenda do bem roubado; esse limite pode favorecer repetição de soluções financeiras sem desfecho monetário direto.\n'
 sections[29]+='\nAvaliação: reparação material, auxílio, proteção, captura e mudança de cidade aumentam as consequências possíveis. As cadeias de agressão ainda repetem golpes e a fome segue dominante. H07, H10 e H20 documentam respostas distintas; os arcos violentos e a raridade de mudança por pobreza mostram onde a variedade ainda é limitada.\n'
 assert len(sections)==34
 intro=['# Relatório final — Fase4: interação, combate e resposta','',
 'Base recebida em `fase_4.md`; decisão demográfica do usuário: equilíbrio. Código e evidências anteriores preservados. Este relatório usa a auditoria oficial congelada, sem misturar resultados da curta.','',
 f"Arquivos: {histories}; {link('reports/fase_4/auditoria_global_10000h/resumo.json','métricas oficiais')}; {link('reports/fase_4/auditoria_global_10000h/save_final.json','save final')}; {link('reports/fase_4/testes_direcionados.txt','20 regressões')}; {link('reports/fase_4/PLANO_E_REGISTRO.md','registro de correções')}",'']
 report=readable('\n'.join(intro+sections))
 (ROOT/'RELATORIO_FASE_4.md').write_text(report,encoding='utf-8');(OUT/'RELATORIO.md').write_text(report,encoding='utf-8')
 (OUT/'analise_quantitativa.json').write_text(json.dumps({'event_counts':counts,'migration_reasons':migration_reasons,
  'conflict_end_reasons':ends,'unique_migrants':unique_migrants,'story_count':len(chosen),
  'attack_actor_top10':attacks_per_actor.most_common(10),'witness_mean':statistics.mean(witness_counts),'deprivation_after_recent_attack':deprivation_after_attack,
  'food_carried_deaths':food_carried_deaths,'economic_crime_attempts':economic_crime_attempts,
  'migration_routes':[{'origin':a,'destination':b,'departures':n} for (a,b),n in migration_routes.most_common()]},ensure_ascii=False,indent=2),encoding='utf-8')
 print('Relatório34 seções, histórias:',len(chosen),flush=True)

if __name__=='__main__':generate()
