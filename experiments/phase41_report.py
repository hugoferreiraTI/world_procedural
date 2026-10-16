"""Relatório Fase 4.1, derivado das campanhas concluídas; não simula o mundo."""
import gzip,json,re
from collections import Counter,defaultdict
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'reports/fase_4_1'
LONG=BASE/'global_5000h'
OLD=ROOT/'reports/lore_vespera47_5000h'
CAUSES={'hunger':'fome','thirst':'sede','both':'fome e sede','combat':'combate'}

def read(path):return json.loads(path.read_text())
def n(value,digits=0):
    return f'{value:,.{digits}f}'.replace(',','@').replace('.',',').replace('@','.')
def pct(value,total):return n(100*value/max(1,total),2)+'%'
def link(path,label=None):return f'[{label or path.name}](<{path.resolve()}>)'
def table(headers,rows):
    return '\n'.join(['| '+' | '.join(headers)+' |','| '+' | '.join(['---']*len(headers))+' |']+['| '+' | '.join(map(str,row))+' |' for row in rows])
def polish(text):
    protected=r'(\[[^\]]*\]\(<[^>]*>\)|`[^`]*`)'
    parts=re.split(protected,text)
    return ''.join(part if i%2 else polish_prose(part) for i,part in enumerate(parts))
def polish_prose(text):
    for before,after in {
      'HPbaixo':'HP baixo','HPcrítico':'HP crítico','HPpós-refeição':'HP pós-refeição',
      'HPanterior':'HP anterior','HPda primeira':'HP da primeira','Fase4.1':'Fase 4.1',
      'Fase4':'Fase 4','NPCvivo':'NPC vivo','novosNPCs':'novos NPCs',
      'Controlenovo':'Controle novo','Controleantigo':'Controle antigo',
      'NovaFase':'Nova Fase','seisreinos':'seis reinos','Antigo500':'Antigo 500',
      'Nova500':'Nova 500','Nova5.000':'Nova 5.000','subiu{':'subiu {'
      ,'comHP':'com HP','emHP':'em HP','aHP':'a HP','oHP':'o HP','eHP':'e HP',
      'deHP':'de HP','apósHP':'após HP','noHP':'no HP','porID':'por ID',
      'deNPC':'de NPC','oNPC':'o NPC','dosNPCs':'dos NPCs','deLOD':'de LOD','emh':'em h','atéh':'até h'
    }.items():text=text.replace(before,after)
    text=re.sub(r'(\d)(HP|h\b|rações|vezes|pontos|persistentes|abstratos|localidades|privação|combate|dano|cura)',r'\1 \2',text)
    text=re.sub(r'(?<!\w)(HP)(?=\d)',r'\1 ',text)
    text=re.sub(r'(?<=[a-zà-ú])(?=\d)', ' ',text)
    return re.sub(r'(?<=\S) {2,}(?=\S)',' ',text)
def rows_gz(path):
    with gzip.open(path,'rt',encoding='utf-8') as stream:
        for line in stream:yield json.loads(line)
def hunger_deaths(d):return sum(d['death_causes'].get(k,0) for k in ('hunger','both'))
def material_deaths(d):return sum(d['death_causes'].get(k,0) for k in ('hunger','thirst','both'))
def windows(d):
    return table(['Prazo','Observados','Morreu','HP <30','HP 30–50','HP 50–70','HP >70'],[
      [h+'h',n(sum(c.values())),*[n(c.get(k,0)) for k in ('dead','below30','30-50','50-70','above70')]]
      for h,c in d['low_hp_window_counts'].items()])

def stories(long,people,initial):
    """Escolhe trajetórias existentes e guarda cada linha citada como evidência."""
    traces=defaultdict(list)
    for row in rows_gz(LONG/'decisoes.jsonl.gz'):
        traces[str(row['actor'])].append(row)
    events=defaultdict(list)
    for event in rows_gz(LONG/'eventos.jsonl.gz'):
        for pid in {event['actor_id'],event['target_id']}:
            if pid is not None:events[str(pid)].append(event)
    candidates=[]
    for pid,rows in traces.items():
        meals=[r for r in rows if r['success'] and r['before']['hp']<30 and r['after']['hunger']<r['before']['hunger']]
        for meal in meals:
            healed=[r for r in rows if meal['turn']<=r['turn']<=meal['turn']+168 and r['after']['hp']>r['before']['hp']]
            restored=next((r for r in healed if r['after']['hp']>=80),None)
            if restored:
                return_to=next((r for r in rows if restored['turn']<r['turn']<=restored['turn']+72 and r['success'] and r['action'] in ('work','train','work_for_food','temporary_service','migrate','give_supplies')),None)
                candidates.append((bool(return_to),people[pid]['alive'],pid,meal,healed,restored,return_to))
                break
    candidates.sort(key=lambda c:(not c[0],not c[1],c[3]['before']['hp'],c[3]['turn']))
    chosen=[];used=set()
    for c in candidates:
        if c[2] not in used:
            chosen.append(c);used.add(c[2])
        if len(chosen)==5:break
    texts=['# Histórias reais — Fase 4.1','',
      'Seed Vespera-47; mundo novo sem jogador; 5.000 horas. São reconstruções de eventos e ações reais, não narrativas geradas. '
      'HP e recursos nos quadros são valores antes/depois da ação; fisiologia continua no fechamento da hora. '
      'A agenda antiga de LOD pode agrupar várias horas de descanso em uma execução; um salto maior que 8 HP numa linha não significa cura de uma única hora. '
      'Sobrevivente ao final não significa imunidade futura.','']
    evidence=[]
    def action_table(rows):
        return table(['Hora','Ação','Necessidade','HP','Fome','Sede','Dano de privação','Resultado'],[
          [n(r['turn']),r['action'],(r['need'] or {}).get('kind','—'),f"{r['before']['hp']} → {r['after']['hp']}",
           f"{n(r['before']['hunger'])} → {n(r['after']['hunger'])}",f"{n(r['before']['thirst'])} → {n(r['after']['thirst'])}",
           f"{r['before']['deprivation']} → {r['after']['deprivation']}",'sucesso' if r['success'] else 'falhou'] for r in rows])
    for i,c in enumerate(chosen,1):
        returned,alive,pid,meal,healed,restored,return_to=c
        sample=[meal]
        sample+=healed[:2]
        if restored not in sample:sample.append(restored)
        if return_to:sample.append(return_to)
        sample.sort(key=lambda r:r['turn'])
        person=people[pid]
        texts+= [f'## {i}. {person["name"]} #{pid}: refeição, recuperação e continuidade','',
          f"Na hora {n(meal['turn'])}, tinha {meal['before']['hp']} HP e fome {n(meal['before']['hunger'])}. "
          f"A ação `{meal['action']}` reduziu a fome sem restaurar HP. Depois, descanso/tratamento registrado elevou HP até "
          f"{restored['after']['hp']} na hora {n(restored['turn'])}. "
          +(f"Na hora {n(return_to['turn'])}, executou `{return_to['action']}` após essa recuperação. " if return_to else 'Não foi encontrada atividade de retorno no intervalo observado de 72h. ')
          +f"Estado em 5.000h: {'vivo' if alive else 'morto'}, HP {person['state']['hp']}. "
          +'A melhora demonstrada é corporal e temporal; ela não garante estabilidade econômica permanente.','',action_table(sample),'']
        nearby=[e for e in events[pid] if meal['turn']-12<=e['turn']<=restored['turn']+24 and e['kind'] in ('HelpGiven','FirstAidGiven','ProtectionGiven','MigrationStarted','MigrationArrived')][:3]
        for e in nearby:
            texts +=[f"- h{n(e['turn'])}, evento #{e['id']}: {e['description']}"]
        if nearby:texts.append('')
        evidence.append({'kind':'recovery_trajectory','person':pid,'actions':sample,'events':nearby})
    personal=sorted(((pid,r) for pid,rows in traces.items() for r in rows
                     if r['action']=='person_meal' and r['success'] and r['before']['hp']<=5),
                    key=lambda c:(c[1]['before']['hp'],c[1]['turn']))
    texts+=['## Roubo pessoal vital: transferência e consumo na mesma cadeia','']
    if personal:
        pid,r=personal[0];related=[e for e in events[pid] if e['id'] in r['event_ids']]
        death=long['death_records'].get(pid)
        texts +=[f"{people[pid]['name']} #{pid}, h{n(r['turn'])}: `{r['action']}` baixou a fome "
          f"{n(r['before']['hunger'])}→{n(r['after']['hunger'])}, mantendo HP {r['after']['hp']}. "
          'A transferência produziu evento de roubo e o consumo produziu evento de refeição. '
          +(f"A pessoa morreu mais tarde emh{n(death['turn'])}, por {CAUSES[death['cause']]}, com {death['food']} rações. " if death else 'A pessoa permaneceu viva atéh5.000. ')
          +'Isso demonstra a correção da aquisição alimentar imediata; não promete proteção contra futuras crises.','',action_table([r]),'']
        for e in related:texts +=[f"- Evento #{e['id']}: {e['description']}"]
        texts.append('');evidence.append({'kind':'personal_meal','person':pid,'action':r,'events':related,'death':death})
    else:texts+=['A regressão controlada comprova a cadeia vital; não houve recorte de roubo pessoal bem-sucedido comHP≤5 nesta campanha.','']
    # Ajuda de familiar só é afirmada quando o vínculo inicial está documentado.
    family_case=None
    for pid,rows in traces.items():
        kin=set(map(str,initial.get(pid,{}).get('family',[])))
        for e in events[pid]:
            if str(e['target_id'])==pid and str(e['actor_id']) in kin and e['kind'] in ('HelpGiven','FirstAidGiven'):
                nearby=[r for r in rows if abs(r['turn']-e['turn'])<=24 and r['before']['hp']<80]
                if nearby:family_case=(pid,e,nearby[:3]);break
        if family_case:break
    texts+=['## Ajuda e vínculos familiares','']
    if family_case:
        pid,e,nearby=family_case
        texts +=[f"h{n(e['turn'])}, evento #{e['id']}: {e['description']} O vínculo familiar entre os IDs "
          f"{e['actor_id']} e {e['target_id']} consta do elenco inicial da mesma seed. As ações próximas mostram a condição do destinatário; "
          'o registro não demonstra enfermagem contínua ou planejamento médico. Nomes iguais pertencem a IDs diferentes; '
          'o texto do evento permite ambiguidade visual porque não apresenta esses IDs.','',action_table(nearby),'']
        evidence.append({'kind':'family_help','person':pid,'event':e,'actions':nearby})
    else:texts+=['Não foi encontrada, nos recortes disponíveis, combinação verificável de familiar ajudando destinatário com HP baixo. '
        'Ajuda geral não foi renomeada como cuidado familiar.','']
    mixed=next(((pid,r) for pid,rows in traces.items() for r in rows if r['before']['deprivation']
                and 100-r['before']['hp']>r['before']['deprivation'] and r['after']['hp']>r['before']['hp']),None)
    texts+=['## Dano misto: privação e ferimento não são a mesma cura','']
    if mixed:
        pid,r=mixed;heal=r['after']['hp']-r['before']['hp'];depriv=r['before']['deprivation']-r['after']['deprivation']
        texts +=[f"{people[pid]['name']} #{pid}, h{n(r['turn'])}: faltavam {100-r['before']['hp']} HP; "
          f"a parcela de privação era de {r['before']['deprivation']} HP. A ação `{r['action']}` restaurou {heal} HP: "
          f"{depriv} debitados desse registro e {heal-depriv} de cura física normal/tratamento. "
          'Não houve cura física rápida causada pela refeição.','',action_table([r]),'']
        evidence.append({'kind':'mixed_damage','person':pid,'action':r})
    else:texts+=['Nenhum recorte clínico misto foi localizado; o caso controlado de 30 HP de fome +20 de combate está no teste 08.','']
    failed=[]
    for pid,death in long['death_records'].items():
        if death['cause'] not in ('hunger','both'):continue
        meal=[r for r in traces[pid] if r['success'] and r['before']['hp']<30 and r['after']['hunger']<r['before']['hunger'] and r['turn']<death['turn']]
        if meal:failed.append((pid,death,meal[-1]))
    texts+=['## Contraponto: uma refeição ainda pode apenas adiar o desfecho','']
    for pid,death,meal in failed[:3]:
        later=[r for r in traces[pid] if meal['turn']<r['turn']<death['turn']]
        rows=[meal]+later[-4:]
        texts +=[f"{death['name']} #{pid} comeu com HP {meal['before']['hp']} em h{n(meal['turn'])}, "
          f"mas morreu por {CAUSES[death['cause']]} em h{n(death['turn'])}, carregando {death['food']} rações. "
          'A cadeia rompeu após o consumo; a morte não prova que a cura disponível foi recusada deliberadamente. '
          'Os registros abaixo mostram as ações realizadas e as condições materiais.','',action_table(rows),'']
        for r in rows:
            if not r['success']:texts +=[f"- h{n(r['turn'])}, `{r['action']}`: {r['outcome']}"]
        texts.append('')
        evidence.append({'kind':'failed_recovery','person':pid,'death':death,'actions':rows})
    if not failed:texts+=['Nenhuma morte por fome foi ligada a uma refeição crítica anterior no recorte registrado. Isso é ausência no recorte, não prova de impossibilidade.','']
    # Comparação por ID não é contrafactual causal: escolhas divergem após a atualização.
    old_deaths=read(OLD/'resumo.json')['death_records']
    survivors=[(pid,d) for pid,d in old_deaths.items() if people.get(pid,{}).get('alive')]
    texts+=['## Personagens que morreram na versão anterior e continuaram nesta campanha','']
    for pid,d in survivors[:5]:
        texts +=[f"- {d['name']} #{pid}: morreu por {CAUSES[d['cause']]} em h{n(d['turn'])} na campanha anterior; "
                 f"na campanha nova está vivo em h5.000 com {people[pid]['state']['hp']} HP."]
    texts+=['','A geração inicial foi preservada, mas as escolhas e a aleatoriedade subsequente divergem. '
       'Esses casos são comparação de trajetórias, não prova de que a mesma sequência antiga foi salva apenas pela cura.','',
       '## Fontes e alcance','',
       f"Ações: {link(LONG/'decisoes.jsonl.gz')}. Eventos: {link(LONG/'eventos.jsonl.gz')}. "
       f"Vínculos iniciais: {link(OLD/'personagens_iniciais.json')}. "
       f"Trechos citados: {link(BASE/'evidencias_historias.json')}. "
       'Ações normais após recuperação são amostradas a cada 24h durante 72h; ações com HP <30 são registradas sem esse intervalo. '
       'O catálogo não representa todas as histórias do mundo.']
    (BASE/'HISTORIAS_REAIS.md').write_text(polish('\n'.join(texts))+'\n')
    (BASE/'evidencias_historias.json').write_text(json.dumps(evidence,ensure_ascii=False,indent=2))
    return {'full_recovery_trajectories_found':len(candidates),'featured':len(chosen),'family_help_found':bool(family_case),
      'featured_search_recoveries_within72':sum(c[5]['turn']-c[3]['turn']<=72 for c in candidates),
      'shortest_recorded_full_recovery_hours':min((c[5]['turn']-c[3]['turn'] for c in candidates),default=None),
      'failed_recovery_deaths_found':len(failed),'old_dead_new_alive':len(survivors)}

def report():
    a=read(BASE/'curta_base/resumo.json');b=read(BASE/'curta_nova/resumo.json');d=read(LONG/'resumo.json')
    old=read(OLD/'resumo.json');old_people=read(OLD/'personagens_finais.json')
    people=read(LONG/'personagens.json');initial=read(OLD/'personagens_iniciais.json')
    clinical=read(LONG/'janelas_recuperacao.json');crises=read(LONG/'crises_por_npc.json')
    story_stats=stories(d,people,initial);m=d['metrics'];last=d['samples'][-1]
    total_damage=sum(m.get('Recovery:Damage:'+k,0) for k in ('hunger','thirst','both','combat'))
    total_healed=m.get('Recovery:DeprivationHealed',0)+m.get('Recovery:PhysicalHealed',0)
    missing_hp=sum(100-p['state']['hp'] for p in people.values())
    deprivation_damage=sum(m.get('Recovery:Damage:'+k,0) for k in ('hunger','thirst','both'))
    remaining_ledger=sum(p['state']['deprivation'] for p in people.values())
    balances={'all_hp':{'damage':total_damage,'healed':total_healed,'missing_hp':missing_hp,
                        'valid':total_damage-total_healed==missing_hp},
              'deprivation':{'damage':deprivation_damage,'healed':m.get('Recovery:DeprivationHealed',0),
                            'remaining':remaining_ledger,'valid':deprivation_damage-m.get('Recovery:DeprivationHealed',0)==remaining_ledger}}
    if not all(v['valid'] for v in balances.values()):raise RuntimeError('Balanço global de HP divergiu: '+str(balances))
    (BASE/'BALANCO_GLOBAL_HP.json').write_text(json.dumps(balances,ensure_ascii=False,indent=2))
    old_metrics=old['metrics'];old_hours=1776*5000-sum(5000-r['turn'] for r in old['death_records'].values())
    old_rations=old_metrics['FoodEaten']/(old_hours/24)
    old_mean_hp=sum(p['health'] for p in old_people.values() if p['alive'])/old['final']['alive']
    old_low=sum(p['alive'] and p['health']<30 for p in old_people.values())
    old_hunger=old_metrics['Feeding:HungerAtConsumption:sum']/old_metrics['Feeding:HungerAtConsumption:count']
    old_meal_hp=old_metrics['Feeding:HPAtConsumption:sum']/old_metrics['Feeding:HPAtConsumption:count']
    new_ratio=d['rations_per_persistent_npc_day']/old_rations
    old_food_deaths=sum(old['death_causes'].get(k,0) for k in ('hunger','both'))
    all_episodes=[e for v in crises.values() for e in v]
    crisis_meals=sum('first_meal' in e for e in all_episodes)
    recurrence_gaps=[e['recurrence_at']-e['start'] for e in all_episodes if 'recurrence_at' in e]
    multi_dead=sum(len(v)>1 and not people[pid]['alive'] for pid,v in crises.items() if v)
    recovered_people={e['person'] for e in clinical if any(w['category']=='above70' for w in e['windows'].values())}
    recovered_dead=sum(not people[str(pid)]['alive'] for pid in recovered_people)
    mixed_people=sum(p['damage_by_origin'].get('combat',0)>0 and any(p['damage_by_origin'].get(k,0)>0 for k in ('hunger','thirst','both')) for p in people.values())
    hunger_dead_people=[people[pid] for pid,r in d['death_records'].items() if r['cause'] in ('hunger','both')]
    hunger_dead_physical=sum(p['state']['deprivation']<100 for p in hunger_dead_people)
    econ=d['economy'];old_towns=read(OLD/'cidades_finais.json')
    alive_people=[p for p in people.values() if p['alive']]
    source_rows=[[source,n(sum(p['despair_sources'].get(source,0)>1e-6 for p in alive_people)),
                  n(sum(p['despair_sources'].get(source,0) for p in alive_people)/max(1,len(alive_people)),2)]
                 for source in ('poverty','deprivation','grief','violence','pursuit','unclassified')]
    old_production=sum(t['production_total'].get('food',0) for t in old_towns.values())
    sections=[]
    def sec(title,body):sections.append('## '+title+'\n\n'+body.strip()+'\n')
    title='# Fase 4.1 — recuperação fisiológica e sobrevivência sustentável\n\n'
    intro=(f"Implementação e auditoria em 8 de outubro de 2026. Especificação: {link(ROOT/'fase_4_1.md')}. "
      f"Versão `{d['rules']}`, SHA-256 `{d['core_sha256']}`. Base preservada: `{a['rules']}`, "
      f"SHA-256 `{a['core_sha256']}`. Todas as campanhas novas começaram em h0, sem jogador e sem carregar save. "
      'A geração manteve `GENERATION_VERSION=mvp-4`, a mesma seed, elenco, geografia e população inicial. '
      'Após a primeira decisão diferente, os fluxos aleatórios e as histórias podem divergir.\n\n')
    sec('1. Resumo executivo',f"""
A versão implementa a sequência adquirir → consumir → estabilizar → descansar → recuperar. Comer continua reduzindo fome, sem curar HP. Dano de privação passou a ser recuperável de forma distinta do dano físico, e HP baixo agora participa das decisões mesmo sem lesão.

Os 209 testes passaram, incluindo dez novos. A comparação controlada de 500h precedeu uma única campanha nova de 5.000h. No teste longo, houve {n(sum(d['death_causes'].values()))} mortes, das quais {n(hunger_deaths(d))} por fome ou fome+sede; antes eram 389 e 332, respectivamente. Consumo por dia de NPC vivo: {n(old_rations,4)} → {n(d['rations_per_persistent_npc_day'],4)} ({n((new_ratio-1)*100,2)}%).

**Resposta central:** há recuperação corporal real: {n(story_stats['full_recovery_trajectories_found'])} trajetórias registradas de refeição comHP<30 chegaram aHP≥80 em até168h. Nas janelas mais curtas, {n(len(recovered_people))} personagens que entraram em HP <30 apareceram com HP >70 em pelo menos um prazo de24/48/72h. Há também fracassos e reincidência: {n(multi_dead)} personagens com crises alimentares repetidas terminaram mortos. Portanto, o motor consegue recuperar um NPC; uma refeição isolada ainda pode apenas adiar a morte se a estabilidade não se sustentar. **A melhora é real, mas a recuperação rápida e duradoura ainda tem resultado parcial.**

Os invariantes estruturais passaram em todas as 50 verificações da campanha longa. Isso verifica integridade, não equilíbrio definitivo. Os resultados representam uma seed e uma execução, sem estimativa estatística de outros mundos.
""")
    sec('2. Diagnóstico anterior',"""
A suspeita do acúmulo de dano tinha base: havia descanso de até 3 HP/h, reduzido ou bloqueado por privação, mas faltava pressão específica de recuperação quando o HP baixo vinha de fome e não de lesões. O NPC podia obter comida, consumir, voltar à rotina e atravessar outra crise com a reserva de HP já reduzida. A necessidade alimentar normal começava em fome 50; decisões de background podiam demorar 12h.

O caso confirmado de integração era Bela Douran #3139: em h582, HP1/fome100, `steal_person` transferiu uma ração, mas a fome permaneceu100; morreu em h583 carregando-a. O relatório Vespera anterior registrou 329 mortes por fome, três por fome+sede, sete por sede e 50 por combate. Essa mortalidade não demonstra falta global de alimentos: distribuição, renda, conhecimento, tempo de deslocamento e fisiologia individual interferem no acesso.
""")
    sec('3. `steal_person`',f"""
Roubo pessoal agora é fornecedor alimentar reconhecido pelo estimador comum. Em emergência fatal, a alternativa `person_meal` executa o roubo real e só consome se a transferência tiver sucesso. Quando há uma alternativa composta viável, a aquisição isolada equivalente não compete como se já fosse consumo. Se o alvo não possui ração ou o roubo não funciona, a cadeia falha sem criar alimento.

O teste 01 confirma HP1/fome100, perda de uma ração pelo alvo, consumo pelo ator, fome100→60 e HP1 preservado no fechamento seguinte. HP não aumenta com a refeição. Na campanha longa, houve {n(m.get('FoodEaten',0))} refeições e {n(len(d['food_carried_deaths']))} mortes por fome/fome+sede carregando ração. Essa última contagem é observação global; o teste controla especificamente o roubo pessoal vital.
""")
    sec('4. Pipeline comum de aquisição alimentar',"""
`ACQUISITIONS` informa quais ações fornecem comida: compra, coleta, roubo municipal/pessoal, pedido de ajuda, trabalho por comida e serviço temporário. `MEALS` mapeia as cadeias reais de aquisição e refeição. Todas as alternativas são enumeradas, inclusive as da Fase 4, antes de montar e avaliar essas cadeias. O estimador inclui rota, tempo de aquisição, intervalo até consumir e margem de sobrevivência.

Toda transferência real passa pelo serviço de itens e pelo observador de inventário: ajuda, pagamento e restituição não geram comida adicional. Restituição recebida e presentes são entradas passivas; não recebem uma ação inventada de “pedir restituição para curar”. A ração recebida torna-se comida possuída e pode ser consumida na próxima decisão. Ajuda solicitada ao jogador não é tratada como transferência garantida.

Aquisição fora de emergência continua separada da refeição. Comprar reserva não obriga o NPC a comer imediatamente. Comer só remove a ração que existe no inventário e aplica a redução normal de fome.
""")
    sec('5. Novo limiar de refeição',f"""
O limiar centralizado caiu de 50 para 35. Em fome36 existe a opção `eat`, mas ela pode perder para uma necessidade mais urgente. Em fome15 não é criada necessidade de refeição. A refeição reduz até40 pontos de fome; o ganho útil depende da fome presente.

A antecipação não significa que todas as refeições aconteçam em35: a média longa foi {n(d['mean_meal_hunger'],2)}, contra aproximadamente {n(old_hunger,2)} antes. A curva, a atividade atual, a água, a reserva, a rota e outras necessidades continuam competindo. A média antiga vem do diagnóstico de consumo, que inclui 50 usos de comida em socorro; a nova média conta `FoodEaten` diretamente. A comparação curta usa o mesmo observador nas duas versões.
""")
    sec('6. Curva de prioridade alimentar',"""
Pressão base configurada: fome35→20; fome40→40; fome60→70; fome80→100. Entre os pontos há progressão linear. Idade da necessidade e modificadores existentes continuam atuando. Abaixo de35 não há pressão de refeição normal. A faixa35–40 permite aproveitar oportunidade; 40–60 é necessidade normal; 60–80 é alta; 80+ ou margem vital curta ativa emergência.

O limiar normal não foi transformado em prioridade100. Reserva conserva sua avaliação de cobertura, déficit, preço observado, oportunidade presente e próxima reposição conhecida. Nenhuma mudança foi feita no crescimento da fome/sede ou no tamanho da redução por refeição.
""")
    sec('7. Need de recuperação',f"""
`recovery` surge abaixo de80HP independentemente da lesão. A pressão base é `min(95,25+80−HP)`: aproximadamente45 emHP60,65 emHP40,85 emHP20 e95 no estado mais grave. O contexto registra HP, dano recuperável e dano físico restante. Ao atingir80, a necessidade pode ser satisfeita; não exige hospitalização até100.

Se alimentação ou água ainda não estiverem suficientemente controladas, a necessidade reutiliza as soluções alimentares/hídricas existentes. Sem adversário ativo, pode voltar à própria casa e descansar; lesão relevante permite buscar tratamento e pedir socorro local. Com adversários, respostas defensivas continuam no sistema de conflitos. HP<20 pode interromper trabalho e objetivos não vitais para descanso/tratamento/água, sem apagar a necessidade de comida ou a defesa.

Na campanha longa: {n(m.get('NeedSelected:recovery',0))} seleções de recuperação, {n(m.get('NeedSatisfied:recovery',0))} satisfações e {n(m.get('Recovery:DeprivationFullyRecovered',0))} esgotamentos do registro de dano por privação. São ocorrências, não necessariamente pessoas únicas. Descanso causado por cansaço também pode recuperar HP; essas contagens não abrangem toda cura.
""")
    sec('8. Origem do dano',table(['Origem','HP realmente perdido na campanha'],[
      ['Fome',n(m.get('Recovery:Damage:hunger',0))],['Sede',n(m.get('Recovery:Damage:thirst',0))],
      ['Fome e sede simultâneas',n(m.get('Recovery:Damage:both',0))],['Combate',n(m.get('Recovery:Damage:combat',0))]])
      +f"\n\nA perda simultânea é contabilizada uma vez em `both`, sem duplicar fome+sede. O dano de combate registra a perda efetiva, limitada ao HP existente; a fórmula e a variação do ataque permaneceram as mesmas. {n(mixed_people)} personagens sofreram tanto privação quanto combate em algum momento; essa contagem de trajetórias mistas não soma um quinto tipo de dano.")
    sec('9. Dano recuperável por privação',f"""
`recoverable_deprivation_damage` acumula somente a perda real causada por fome, sede ou ambas. Um golpe fisiológico nominal de5 em alguém comHP1 registra1. O registro nunca ultrapassa o HP ausente e é persistido no save. A barra de vida permanece única.

Cura fisiológica debita esse registro e aumenta HP na mesma quantidade. Na campanha foram recuperados {n(m.get('Recovery:DeprivationHealed',0))} HP de privação. A contagem pode superar o HP máximo de um NPC ao longo de meses porque novas crises voltam a causar dano; ela não significa excesso de HP em uma ação.

O balanço global fechou exatamente: {n(deprivation_damage)}HP perdidos por privação − {n(m.get('Recovery:DeprivationHealed',0))} recuperados = {n(remaining_ledger)} ainda registrados em vivos e mortos. Também fechou para todo oHP: {n(total_damage)}dano − {n(total_healed)}cura = {n(missing_hp)}HP ausentes no elenco completo. Fonte: {link(BASE/'BALANCO_GLOBAL_HP.json')}.
""")
    sec('10. Dano físico',f"""
Combate não aumenta o registro de privação. O dano físico ainda depende da cura normal de descanso/tratamento, sob as restrições antigas de fome/sede e ferimentos. Socorro continua limitado e consome provisão e água reais. Alimentar-se não cura espada.

Foram recuperados {n(m.get('Recovery:PhysicalHealed',0))} HP físicos ao todo; {n(d['rest_healing_observed'].get('physical',0))} foram observados em descanso. A diferença corresponde ao socorro registrado pela função comum; não deve ser apresentada como cura fisiológica rápida. O teste misto30 de fome+20 de combate confirma que a parcela rápida se limita aos30, enquanto os outros20 usam a recuperação física normal.
""")
    sec('11. Recuperação por descanso',table(['Condição da maior fome/sede','Cura rápida de privação em local seguro'],[
      ['Até50','8HP/h'],['51–70','4HP/h'],['71–80','1HP/h'],['Acima80','0HP/h de cura rápida']])+"""

O local seguro inicial é a própria casa, sem adversários ativos. Chegar lá exige deslocamento real; não há teleporte. A cura física normal continua sendo até3HP/h, com as reduções antigas. `recover_hp` usa um único orçamento, `max(cura_normal,cura_fisiológica)`, e divide esse orçamento entre as parcelas; não soma8+3 indevidamente. A cura rápida não ultrapassa o dano de privação registrado. A cura normal pode também reparar privação quando as condições antigas permitem, inclusive fora da condição de cura rápida.

A recuperação ocorre no descanso executado, sem regeneração passiva universal. Ela pode parar para beber/comer e recomeçar depois. Tratamento limitado segue a mesma função para manter a consistência entre HP ausente e registro recuperável.

O motor conserva a agregação existente de atividade pelo intervalo de LOD. Uma execução de descanso pode representar várias horas acumuladas, portanto uma linha pode mostrar +24HP sob taxa de8HP/h; isso não é uma segunda função de cura. A condição usada é a observada na execução, sem reconstituir as condições de cada hora intermediária. Essa aproximação temporal foi preservada e precisa ser lembrada ao interpretar os quadros clínicos.
""")
    sec('12. Integração com fome/sede',"""
Com fome/sede acima50, o plano de recuperação procura primeiro estabilizar recursos; se a sede é dominante, prioriza água. Aquisição real e consumo permanecem separados. Necessidades vitais críticas conservam a prioridade e o desempate anteriores, e comida possuída em emergência mantém a opção de consumo.

Aumentos por hora e dano progressivo da privação não foram reduzidos. A promoção de LOD antecipa decisões, mas a fisiologia continua passando uma vez por hora. Um NPC pode morrer quando não existe solução conhecida e viável a tempo, inclusive diante de duas necessidades vitais simultâneas. Isso é diferente de curar HP simplesmente porque uma compra aconteceu.
""")
    sec('13. Integração com combate',table(['Evento/ação','Fase4 anterior,5.000h','Fase4.1,5.000h'],[
      ['Ataques executados',n(old_metrics.get('AttackExecuted',0)),n(m.get('AttackExecuted',0))],
      ['Fugas bem-sucedidas (eventos)',n(old_metrics.get('CharacterFled',0)),n(m.get('CharacterFled',0))],
      ['Rendições',n(old_metrics.get('CharacterSurrendered',0)),n(m.get('CharacterSurrendered',0))],
      ['Mortes por combate',n(old['death_causes'].get('combat',0)),n(d['death_causes'].get('combat',0))]])
      +f"\n\nHP crítico adiciona penalidade à Utility de ataque voluntário, ameaça e perseguição. Defesa recebe penalidade menor; fuga e rendição já consideravam HP. Foram observados {n(d['critical_attacks'].get('actor_hp_below20',0))} ataques iniciados comHP<20, de {n(d['critical_attacks'].get('all',0))}. Não há medição equivalente no longo antigo: no controle de500h foram dois antes e zero depois. Essas diferenças também refletem fome, emoções, encontros e trajetórias divergentes; não atribuem toda mudança à cura. Não houve rebalanceamento de dano/armas/defesa.")
    sec('14. Integração com LOD',"""
Personagens comuns em casa podiam decidir a cada12h. Ao cruzar fome35, passam a decidir no máximo a cada3h; fome alta mantém decisões horárias como antes. HP<30 também força o intervalo de1h. Quando saem dessas condições, a mesma agenda retoma o LOD correspondente à categoria/local/contexto.

A promoção altera o intervalo da agenda existente; não executa uma segunda decisão por callback. O teste10 verifica promoção, interrupção de trabalho por recuperação crítica e avanço normal. O save/load determinístico inclui estado da agenda e campos novos. No mundo longo, cada hora de vida entra apenas uma vez no denominador do consumo.
""")
    sec('15. Desespero',f"""
O valor continua limitado a0–100, mas contribuições agora distinguem privação, pobreza, luto, violência e perseguição conhecida. Valores sem fonte específica ficam em `unclassified`; suporte social e decaimento antigo mantêm as parcelas compatíveis com o total. Humilhação e isolamento não receberam decomposição completa nesta fase: seus estados/fatos continuam no sistema anterior.

Condição material estável exige fome/sede≤50, HP≥60 ou melhora recente, casa segura, ausência de perseguição conhecida e ao menos uma ração e água possuídas. Depois de seis horas observadas nessa condição, as parcelas de pobreza/privação podem cair gradualmente a0,25 por hora cada. Uma refeição não dá queda fixa de30. Luto ativo e grievances não são apagados pela melhora material.

A média de desespero entre vivos foi {n(old['final']['emotions']['desperation']['mean'],2)} antes e {n(last['mean_desperation'],2)} depois. Houve {n(m.get('Emotion:MaterialDesperationRecovered',0),2)} pontos de redução material específica somados em toda a população. A média também recebe suporte, perdas e decaimento anteriores; não mede apenas essa nova regra. O tempo estável usa os intervalos observados pelo LOD, sem reconstituir cada hora intermediária de apoio/segurança subjetiva.

{table(['Fonte registrada','Vivos com parcela positiva','Parcela média entre todos os vivos'],source_rows)}

O requisito material usa recursos possuídos e segurança local, portanto existir comida no município ou ter acabado de comer não assegura várias horas estáveis com comida e água em reserva. Pressões persistentes podem continuar acrescentando desespero. A tabela é o estado final das parcelas remanescentes, depois de reduções, e não o total histórico de todas as causas. A contagem de parcelas positivas ignora resíduos numéricos menores que0,000001.
""")
    tests=[('01','Roubo pessoal vital','Transfere e consome ração real antes de fisiologia fatal; não cura HP'),
      ('02','Compra+refeição','Dinheiro/estoque reais; consumo salva sem restaurar HP'),
      ('03','Fome36','Eat válido, prioridade normal e sem emergência artificial'),
      ('04','Fome15','Não cria refeição; reserva continua separada'),
      ('05','Perda por privação','Registra só HP realmente perdido, inclusive sobre-dano nominal'),
      ('06','Recuperação e desespero','Descanso retira estado grave, Need termina e melhora material gradual preserva luto'),
      ('07','Dano de combate','Não entra no registro rápido; descanso breve segue cura física'),
      ('08','Dano misto','30privação+20combate; parcela rápida limitada e sem orçamento duplicado'),
      ('09','Persistência','Campos novos e Need sobrevivem ao save/load com continuação exata'),
      ('10','LOD/interrupção','Antecipação e recuperação crítica usam a agenda existente')]
    sec('16. Testes direcionados',table(['Teste','Cenário','Verificação'],tests)+f"""

Todos os dez passaram. A suíte completa de209 testes passou em61,79s. Os quatro cenários antigos que inicialmente falharam tinham pressupostos afetados pela refeição antecipada e pelas alternativas reais de ajuda. Foram ajustados o limiar, o valor útil da refeição, o indicador de autonomia em vez de um estoque específico e a ausência de ajudantes no cenário sem rota conhecida. Não foram suprimidas falhas do motor.

Logs: {link(BASE/'testes_direcionados.txt')}, {link(BASE/'testes_completos.txt')}, {link(BASE/'testes_primeira_execucao.txt')}. A quantidade de regressões novas permaneceu dentro dos8–12 solicitados. Save/load e conservação material são cobertos pela suíte; não houve nova bateria de dezenas de testes para esta etapa.
""")
    short_rows=[['Mortes totais',n(sum(a['death_causes'].values())),n(sum(b['death_causes'].values()))],
      ['Fome ou fome+sede',n(hunger_deaths(a)),n(hunger_deaths(b))],['Sede isolada',n(a['death_causes'].get('thirst',0)),n(b['death_causes'].get('thirst',0))],
      ['Combate',n(a['death_causes'].get('combat',0)),n(b['death_causes'].get('combat',0))],
      ['Mortes de fome com ração',n(len(a['food_carried_deaths'])),n(len(b['food_carried_deaths']))],
      ['Fome média ao comer',n(a['mean_meal_hunger'],2),n(b['mean_meal_hunger'],2)],
      ['HP médio ao comer',n(a['mean_meal_hp'],2),n(b['mean_meal_hp'],2)],
      ['HP médio dos vivos em500h',n(a['samples'][-1]['mean_hp'],2),n(b['samples'][-1]['mean_hp'],2)],
      ['Vivos comHP<30 em500h',n(a['samples'][-1]['hp_below30']),n(b['samples'][-1]['hp_below30'])],
      ['Desespero médio dos vivos',n(a['samples'][-1]['mean_desperation'],2),n(b['samples'][-1]['mean_desperation'],2)],
      ['Raç./dia deNPC vivo',n(a['rations_per_persistent_npc_day'],4),n(b['rations_per_persistent_npc_day'],4)]]
    sec('17. Auditoria curta',table(['Indicador em500h','Anterior','Nova'],short_rows)+f"""

Mesma seed Vespera-47, perfil completo, sem história prévia:1.776persistentes,4.461abstratos,75localidades,seisreinos. Os núcleos foram executados separadamente com o mesmo observador passivo. A comparação curta terminou antes de iniciar a longa. Consumo subiu{n((b['rations_per_persistent_npc_day']/a['rations_per_persistent_npc_day']-1)*100,2)}%; não dobrou. Mercado vazio na última amostra diária: {a['economy'][-1]['empty_markets']}→{b['economy'][-1]['empty_markets']}. Não houve aumento artificial de produção para compensar antecipação.

A nova campanha curta restaurou8.294HP de privação, selecionou recuperação271vezes e registrou327 esgotamentos do registro recuperável. As janelas de72h ainda tinham47 episódios emHP<30,13 mortes,21 em30–50 e quatro em50–70; nenhum acima70. Isso motivou acompanhamento longo, sem calibrar parâmetros para uma taxa desejada de mortes.

Fontes: {link(BASE/'curta_base/resumo.json')}, {link(BASE/'curta_nova/resumo.json')}. O contador antigo de máximo de HP após refeição teve erro no observador; não é usado para decidir sucesso. A correção e a contagem válida de cura medida estão nos arquivos `correcao_observador.json` de ambas as pastas.
""")
    long_rows=[['Duração','5.000h','5.000h'],['NPCs vivos',n(old['final']['alive']),n(d['alive'])],
      ['Mortes totais',n(sum(old['death_causes'].values())),n(sum(d['death_causes'].values()))],
      ['Fome ou fome+sede',n(old_food_deaths),n(hunger_deaths(d))],
      ['Fome média ao consumir',n(old_hunger,2),n(d['mean_meal_hunger'],2)],
      ['HP médio ao consumir',n(old_meal_hp,2),n(d['mean_meal_hp'],2)],
      ['HP médio dos vivos',n(old_mean_hp,2),n(last['mean_hp'],2)],
      ['Vivos comHP<30',n(old_low),n(last['hp_below30'])],
      ['Desespero médio',n(old['final']['emotions']['desperation']['mean'],2),n(last['mean_desperation'],2)]]
    sec('18. Auditoria longa',table(['Indicador','Vespera antiga','NovaFase4.1'],long_rows)+f"""

Uma campanha global nova de5.000h, após o controle de500h e a suíte aprovados. Não carregou o save Vespera antigo. Núcleo congelado antes de iniciar; o SHA foi conferido novamente ao terminar. As primeiras500h repetiram os indicadores do teste curto, mostrando que a ampliação passiva dos registros não mudou a trajetória do motor.

Tempo de simulação: {n(d['runtime_seconds'],2)}s, sem contar a gravação do save ao final; pico de memória registrado até a medição anterior à gravação:{n(d['memory_peak_mib'],2)}MiB. A exportação e a recarga de validação não estão incluídas nesse pico. Amostras fisiológicas a cada100h e economia a cada24h. Eventos e decisões clínicas foram exportados sem executar decisões adicionais. Manifesto: {link(LONG/'manifesto.json')}; resumo:{link(LONG/'resumo.json')}; save:{link(LONG/'save_final.json')}.

Depois da campanha, o save exportado foi recarregado somente para verificar formato, versão, invariantes e total do registro de dano; nenhuma hora adicional foi simulada nessa conferência. Resultado: {link(BASE/'save_verificado.json')}. A campanha foi gerada do zero e os resultados históricos não foram carregados para iniciá-la.

A longa anterior não coletou as novas parcelas de cura nem as janelas24/48/72h. Essas colunas não foram preenchidas por estimativa. O controle de500h fornece a comparação equivalente das janelas. A comparação longa é descritiva: mesma população inicial, regras diferentes, sequência de escolhas subsequentes divergente.
""")
    bands=['below30','30-40','40-60','60-80','80+']
    sec('19. Consumo alimentar',table(['Fome na refeição','Anterior500h','Nova500h','Nova5.000h'],[
      [k,n(a['meal_bands'].get(k,0)),n(b['meal_bands'].get(k,0)),f"{n(d['meal_bands'].get(k,0))} ({pct(d['meal_bands'].get(k,0),d['meals'])})"] for k in bands])
      +f"""

A campanha nova consumiu {n(d['meals'])} rações em refeições de personagens persistentes, distribuídas em {n(d['alive_hours'])} horas de vida. Fórmula: `FoodEaten/(soma_das_horas_vivas/24)` = {n(d['rations_per_persistent_npc_day'],4)}. A antiga tinha {n(old_metrics['FoodEaten'])} refeições e {n(old_hours)} horas de vida, obtidas a partir do elenco inicial e horários de morte, dando {n(old_rations,4)}. Não houve materialização de novosNPCs no denominador antigo; se existisse nascimento/materialização, seria necessário incorporar o horário de entrada.

Contar apenas população inicial×duração subestimaria consumo por sobrevivente, porque parte do elenco morre. Alimentos abstratos e provisões gastas no socorro não contam como `FoodEaten`; são outros usos físicos de comida. O diagnóstico de nutrição antiga também registrava socorro, motivo da pequena diferença entre médias históricas e refeições.

Variação normalizada:{n((new_ratio-1)*100,2)}%. Refeições abaixo40 constituem {pct(sum(d['meal_bands'].get(k,0) for k in ('below30','30-40')),d['meals'])}. Não se alterou produção para esconder eventual desperdício. A refeição em35 pode desperdiçar até5 dos40pontos de capacidade; as contagens e o consumo permitem acompanhar esse custo.
""")
    sec('20. Economia',table(['Indicador','Controleantigo500h','Controlenovo500h','Nova5.000h'],[
      ['Produção acumulada de comida na última amostra diária',n(a['economy'][-1]['food_produced_cumulative']),n(b['economy'][-1]['food_produced_cumulative']),n(econ[-1]['food_produced_cumulative'])],
      ['Estoque municipal nessa amostra',n(a['economy'][-1]['food_stock']),n(b['economy'][-1]['food_stock']),n(econ[-1]['food_stock'])],
      ['Mercados vazios nessa amostra',n(a['economy'][-1]['empty_markets']),n(b['economy'][-1]['empty_markets']),n(econ[-1]['empty_markets'])],
      ['Preço médio de uma ração',n(a['economy'][-1]['mean_price'],2),n(b['economy'][-1]['mean_price'],2),n(econ[-1]['mean_price'],2)],
      ['Compras de comida (transações)',n(a['metrics'].get('ItemBought',0)),n(b['metrics'].get('ItemBought',0)),n(m.get('ItemBought',0))],
      ['Unidades compradas para reserva',n(a['metrics'].get('ReservePurchaseUnits',0)),n(b['metrics'].get('ReservePurchaseUnits',0)),n(m.get('ReservePurchaseUnits',0))],
      ['Compras que deixaram segunda ração',n(a['metrics'].get('ReservePurchaseSecondRation',0)),n(b['metrics'].get('ReservePurchaseSecondRation',0)),n(m.get('ReservePurchaseSecondRation',0))]])
      +f"""

As últimas amostras diárias são h480 nos testes curtos e h{econ[-1]['turn']} na longa; não são exatamente o estoque de h500/h5.000. Na longa houve {n(sum(e['empty_markets'] for e in econ))} observações de município sem comida em {n(len(econ)*75)} observações município/dia. Produção antiga emh5.000:{n(old_production)}rações; sua amostragem não é idêntica à nova diária.

Compra/transferência, matéria-prima, preparo e remoção por consumo continuam nos serviços antigos. Reserva normal permanece duas rações; até seis somente conforme a avaliação existente de viagem conhecida. Nesta auditoria sem jogador, as chamadas de compra dosNPCs usam somente comida, portanto `ItemBought` conta transações alimentares. Não equivale ao total de unidades: compras de reserva podem ser em lote. `ReservePurchaseUnits` mede unidades reais desse caminho específico e não inclui todas as compras individuais nem doações, coleta ou pagamento. O total de unidades de todas as compras não foi exportado separadamente.

Preservar estoque global não garante acesso econômico de cadaNPC. Uma localidade pode terminar abastecida enquanto alguém distante, pobre ou sem alternativa conhecida morre. Esse limite continua sendo material e decisório, e deve ser investigado por trajetórias, sem corrigir com dinheiro/comida gratuitos.
""")
    sec('21. Mortalidade',table(['Causa','Anterior5.000h','Nova5.000h'],[
      [k,n(old['death_causes'].get(k,0)),n(d['death_causes'].get(k,0))] for k in ('hunger','thirst','both','combat')])
      +f"""

Fome/fome+sede respondem por {pct(hunger_deaths(d),sum(d['death_causes'].values()))} das mortes novas; privação incluindo sede por {pct(material_deaths(d),sum(d['death_causes'].values()))}. Esses percentuais mudam também quando há mais/menos mortes violentas. A predominância alimentar por si só não mostra que a cura falhou nem que o acesso foi resolvido.

Mortes por fome carregando ração: {n(len(d['food_carried_deaths']))}. O arquivo de resumo registra ID, hora, HP, fome/sede, objetivo final, recursos e dano por origem nas mortes fisiológicas. Quando não há alimento possuído, deve-se investigar alternativas disponíveis a tempo; o agregado não prova ausência de alimento na região nem impossibilidade de ajuda.

A causa registrada identifica o dano que encerrou a vida; não descreve sozinha todo o dano anterior. Das{n(hunger_deaths(d))} mortes por fome/fome+sede,{n(hunger_dead_physical)} ainda tinham parcela física ausente noHPno momento da morte. Nas demais, oHPausente era integralmente registrado como privação. Essa separação evita chamar de exclusivamente alimentar uma trajetória que também acumulou dano de combate não recuperado.
""")
    sec('22. Reincidência de crises',f"""
Crise é uma entrada observada em fome≥90 após estar abaixo90. A refeição é ligada à crise mais recente; uma nova entrada fecha a sequência anterior. Foram observadas {n(d['crisis_count'])} crises em {n(d['crisis_people'])} personagens; {n(d['repeat_crisis_people'])} tiveram mais de uma. {n(crisis_meals)} episódios tiveram refeição posterior registrada; {n(d['crises_with_meal_and_recorded_healing'])} tiveram cura de descanso medida após essa refeição, e {n(d['crises_with_meal_and_hp_improvement'])} tiveram HP posterior maior que o da primeira refeição.

Entre as entradas recorrentes, o intervalo médio foi {n(sum(recurrence_gaps)/max(1,len(recurrence_gaps)),2)}h. {n(multi_dead)} personagens com crises repetidas terminaram mortos. O número de crises mede também a amplitude do período e a população que sobrevive para repetir; não deve ser interpretado como uma taxa independente da exposição.

Uma recuperação curta não impede retorno à fome90. O critério clínico útil é observar se a vida realmente sobe entre crises e se a pessoa permanece viva/ativa depois. Cura medida é diferente de melhora líquida: se houver novos danos após comer, o NPC pode recuperar alguns pontos e ainda ficar abaixo do HP de partida. Dados porID: {link(LONG/'crises_por_npc.json')}.
""")
    sec('23. Recuperação de HP',windows(d)+f"""

Cada linha acompanha entradas emHP<30. Uma pessoa pode entrar várias vezes; portanto são episódios, não indivíduos independentes. Os prazos que ultrapassaramh5.000 ficaram censurados ({n(d['censored_windows'])} janelas) e não foram contados como mortes nem recuperações. Os limites são <30,30≤HP<50,50≤HP≤70 eHP>70.

Pessoas únicas com pelo menos uma janela>70:{n(len(recovered_people))}. Janelas incluem todas as causas de HPbaixo; a história clínica e o registro por origem ajudam a distinguir privação e combate. No controle de500h, a versão anterior não teve nenhuma janela>70 em72h; a nova também não, embora tivesse menos episódios graves. **Na longa também não houve HP acima70 nas observações de24/48/72h.** São fotografias nos prazos, não acompanhamento de todos os picos intermediários. A cura disponível e o resultado corporal geral melhoraram, mas a saída rápida do colapso ainda não foi demonstrada por essas janelas.

Fontes: {link(LONG/'janelas_recuperacao.json')}. A cura não acontece só ao abrir `recovery`: descanso por cansaço e tratamento também podem recuperar. Não foi criado um teto de mortalidade para calibrar esses resultados.

Na busca das{n(story_stats['full_recovery_trajectories_found'])} trajetórias completas, o menor intervalo registrado entre uma refeição emHP<30 e uma ação de cura que levou aHP≥80 foi {story_stats['shortest_recorded_full_recovery_hours']}h. A busca encontrou {story_stats['featured_search_recoveries_within72']} dessas trajetórias completas dentro de72h. Essa medição parte da refeição, enquanto as janelas acima partem da entrada emHP<30; os denominadores são diferentes.
""")
    sec('24. Histórias reais',f"""
Foram encontrados {n(story_stats['full_recovery_trajectories_found'])} personagens com refeição emHP<30 e ação de cura levando aHP≥80 em até168h; {story_stats['featured']} trajetórias foram detalhadas. O catálogo contém valores antes/depois, ações reais, horários e eventos de ajuda/migração quando próximos. Há {n(story_stats['failed_recovery_deaths_found'])} mortes por fome ligadas a refeição crítica anterior no recorte; três exemplos são usados como contraponto.

{n(story_stats['old_dead_new_alive'])} IDs que morreram na campanha antiga estão vivos nesta. É evidência de trajetórias diferentes com o mesmo elenco inicial, sem afirmar que cada resultado foi causado exclusivamente pela cura. Vínculo familiar só é afirmado quando consta do elenco inicial. A busca {'encontrou' if story_stats['family_help_found'] else 'não encontrou'} um caso verificável de familiar ajudando um destinatário comHPbaixo no recorte disponível.

Leitura: {link(BASE/'HISTORIAS_REAIS.md')}. Evidências: {link(BASE/'evidencias_historias.json')}. Combate, proteção, rendição, ajuda, migração e sucessão continuam produzindo eventos; isso não implica que todos os arcos já tenham qualidade narrativa completa.

{table(['Consequência social','Eventos na campanha nova'],[[k,n(m.get(k,0))] for k in ('HelpGiven','FirstAidGiven','ProtectionGiven','MigrationStarted','MigrationArrived','ResidentMoved','SuccessionChanged')])}
""")
    sec('25. Limitações',"""
- Uma seed longa não demonstra robustez para todos os mundos ou todos os perfis de jogador. Não houve novo ensaio como jogador nesta etapa; o núcleo compartilhado e os cenários controlados cobrem a integração, e a auditoria longa é global sem jogador.
- Segurança inicial significa própria casa sem adversário ativo. Não há avaliação nova de abrigo coletivo, enfermaria ou ameaça distante desconhecida; oNPC não recebe conhecimento onisciente.
- HP≥80 pode satisfazer recuperação mesmo com pequena parcela recuperável restante. Esse limite evita descanso prioritário eterno; não garante retorno imediato a100.
- Desespero por humilhação/isolamento não tem decomposição completa. Estabilidade material é observada nos intervalos deLOD, e não uma prova de segurança constante em cada hora intermediária.
- Socorro ainda exige lesão; não foi acrescentado sistema médico para desnutrição nem cuidador com tratamento contínuo. Pedidos existentes, comida/água e descanso resolvem parte desse caminho.
- Estoque regional, acesso individual e continuidade de renda são problemas diferentes. A fase não criou crédito/dinheiro/comida para remover dificuldades materiais.
- Contagens de crises/janelas repetem pessoas; resultados censurados e sobreviventes finais têm exposição diferente. Não calcular intervalos estatísticos fingindo independência.
- Observador clínico registra todas as ações comHP<30, recuperação selecionada e recortes de retorno72h apósHP80; outras ações normais são amostradas. Ausência de uma história no catálogo não prova ausência no mundo.
- Relatórios/saves históricos foram preservados. O carregador recusa versões anteriores; não houve migração automática de saves sem a origem antiga de dano.
""")
    food_warning=(f"**Morte com comida permanece observada:** {n(len(d['food_carried_deaths']))} casos na campanha longa; não declarar esse critério integralmente resolvido sem analisar os registros individuais." if d['food_carried_deaths'] else
      'Não foi observada morte por fome carregando comida nesta campanha; isso reforça a regressão corrigida, sem garantir ausência em todas as condições futuras.')
    sec('26. Bugs encontrados',f"""
1. **Corrigido: aquisição pessoal fora da semântica alimentar.** `steal_person` podia vencer consumo viável e deixar fome100 com a ração recém-adquirida; passou a participar do pipeline e da cadeia vital.
2. **Corrigido: falta de necessidade para HPbaixo sem lesão.** Dano fisiológico acumulado não recebia pressão própria suficiente; `recovery` independe de ferimento.
3. **Corrigido: ausência de registro separado da privação.** A cura forte precisava distinguir a parcela recuperável do combate; origem real e debitação agora são persistidas e verificadas.
4. **Corrigido: decisões tardias na faixa normal eHPcrítico.** A agenda existente promove refeições e recuperação; não há callback executando ação duplicada.
5. **Corrigido no observador, antes da longa:** máximo deHPpós-refeição do teste curto iniciava comHPanterior. O erro afetava um indicador derivado, sem mudar o motor. Os registros curtos originais foram mantidos e anotados; a longa inicializa o máximo noHPda primeira refeição.

{food_warning}

**Permanece uma falha de integração pré-existente:** `forage_meal` que falha bloqueia esse nome, mas `forage` pode tentar o mesmo fornecedor na hora seguinte. Mira Bruma #1922 falhou por coleta esgotada emh306 e repetiu emh307; morreu emh310 sem comida. Evitar a repetição não prova que existia alimento alternativo capaz de salvá-la. O núcleo foi conservado durante a longa; a proposta limitada é compartilhar o bloqueio quando a falha ocorreu na aquisição, distinguindo-a de falha de consumo. Evidência e causa: {link(BASE/'BUGS_REMANESCENTES.md')}, {link(BASE/'evidencia_falha_alias.json')}.

Reincidência, pobreza, desespero elevado e história social repetitiva são limitações medidas, não automaticamente bugs com causa única demonstrada. Problemas sociais já listados na auditoria anterior — duplicação de casos após resolução, interpretação de medo na reputação e residência associada à chegada — não foram reabertos como expansão desta fase. Não foram declarados corrigidos por terem ocorrido menos vezes.
""")
    sec('27. Recomendação para próxima fase',f"""
A recuperação fisiológica existe, diferencia origem, compete por ações e aparece em trajetórias reais. O limiar alimentar antecipado passou pelas regressões, e o consumo mudou{n((new_ratio-1)*100,2)}% por dia deNPCvivo. A implementação passou pelos testes; o resultado de sobrevivência sustentável é **parcial**, porque nenhuma janela crítica apresentavaHP>70 nos prazos de24/48/72h e{n(story_stats['failed_recovery_deaths_found'])} mortes por fome tinham refeição crítica anterior registrada. Não recomendo tratar o ciclo de colapso como encerrado nem avançar com base somente na redução de mortes.

Antes de expandir conteúdo social, usar os episódios que comeram emHPbaixo e morreram depois para localizar a próxima quebra concreta: impossibilidade econômica, trajeto, bloqueio por necessidades concorrentes ou ausência de descanso materialmente viável. A evidência desta campanha deve orientar mudanças pequenas, não novos sistemas amplos para mascarar o ciclo.

Uma hipótese específica a verificar é a competição de renda/reserva com recuperação depois que oHPpassa de20–30. A necessidade de renda pode atingir prioridades altas por idade, diligência, desespero e reveses; reduzir aUtility do trabalho não muda a ordem das necessidades. O motor escolhe a primeira necessidade prioritária com solução viável. Isso pode deixar recuperação esperando mesmo com uma alternativa de descanso disponível. É uma inferência do fluxo de decisão, não prova de que explica todos os224 desfechos.

A próxima correção limitada recomendada é unificar o bloqueio de tentativas equivalentes após falha real do fornecedor alimentar. Ela deve ser validada separadamente; a campanha presente mede o núcleo congelado anterior a essa melhoria proposta.

Se a próxima fase mexer em sobrevivência/economia, preservar o conjunto de dez regressões e comparar consumo, reincidência e janelas deHP novamente. Revisar os problemas sociais conhecidos separadamente e acrescentar cuidados/abrigo somente com objetivos e recursos reais. O teste já responde à pergunta central: **oNPC pode sair do colapso e continuar sua vida, mas só obter uma refeição não garante recuperação sustentável.**
""")
    body=polish(title+intro+'\n'.join(sections))
    (ROOT/'RELATORIO_FASE_4_1.md').write_text(body)
    (BASE/'RELATORIO_FASE_4_1.md').write_text(body)
    verdict={'rules':d['rules'],'hash':d['core_sha256'],'tests':209,'new_tests':10,'short_hours':500,'long_hours':5000,
      'new_hunger_deaths':hunger_deaths(d),'old_hunger_deaths':old_food_deaths,
      'food_carried_deaths':len(d['food_carried_deaths']),'rations_ratio':new_ratio,
      'people_recovered_above70':len(recovered_people),'recovered_later_dead':recovered_dead,
      'story_stats':story_stats,'report_sections':len(sections),'invariants':d['invariants'],'hp_balances':balances}
    (BASE/'VERIFICACAO_RELATORIO.json').write_text(json.dumps(verdict,ensure_ascii=False,indent=2))
    print(json.dumps(verdict,ensure_ascii=False,indent=2))

if __name__=='__main__':report()
