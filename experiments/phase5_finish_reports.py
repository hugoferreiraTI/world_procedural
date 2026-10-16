"""Consolida somente dados encerrados; não simula, modifica ou recarrega o mundo."""
import hashlib
import json
from pathlib import Path


ROOT=Path(__file__).resolve().parents[1]
FOLDER=ROOT/'reports/fase_5'


def read(path):return json.loads(path.read_text())


def metrics(summary):
    p=summary['phase5'];events=p['events']
    return {'seed':summary['seed'],'hours':summary['hours'],'rules':summary['rules'],
        'core_sha256':summary['core_sha256'],'initial':summary['initial'],'alive':summary['alive'],
        'deaths':sum(summary['death_causes'].values()),'death_causes':summary['death_causes'],
        'deprivation_deaths_with_food':len(summary['food_carried_deaths']),
        'invariant_errors':summary['invariants']+summary['final_invariants'],
        'scheduled_invariant_checks':summary['hours']//100,'final_check':True,
        'runtime_seconds_simulation':summary['runtime_seconds'],'save_seconds':summary['save_seconds'],
        'save_mib':summary['save_mib'],'memory_peak_including_export_mib':summary['memory_peak_mib'],
        'history_events':summary['history_events'],'meals':summary['meals'],
        'phase5_events':{name:events.get(name,0) for name in sorted(__import__('experiments.phase5_audit',fromlist=['NEW']).NEW)},
        'groups_final':p['groups_final'],'proposal_status_final':p['proposal_status_final'],
        'factions_final':p['factions_final'],'lethal_modes':p['lethal_modes'],
        'mythic_total':p['mythic_total'],'mythic_alive':p['mythic_alive'],
        'actual_gods':p['actual_gods'],'confirmed_gods':p['gods_with_confirmed_knowers'],
        'social_veneration_observer_updates':summary['metrics'].get('Renown:mortal_venerated',0),
        'believed_divine_mortals_final':p['believed_divine_mortals'],
        'actual_divine_mortals_final':p['actual_divine_mortals'],
        'epithet_subjects_final':p['epithet_subjects'],'reach_distribution_final':p['reach_distribution'],
        'historical_items_final':p['historical_items'],'divine_contact_items_final':p['items_with_divine_contact'],
        'new_entity_maxima_sampled_every_50h':p['maxima']}


def finish():
    short=read(FOLDER/'curta_validada_500h/resumo.json');long=read(FOLDER/'longa_5000h/resumo.json')
    coverage=read(FOLDER/'COBERTURA_HISTORIAS.json')
    delivery=read(FOLDER/'ENTREGA_FINAL.json')
    delivery_short=read(FOLDER/'curta_entrega_500h/resumo.json')
    assert long['hours']==5000 and long['core_sha256']==short['core_sha256']
    assert not long['invariants'] and not long['final_invariants']
    assert delivery['suite_status']=='passed' and delivery['directed_status']=='passed'
    assert delivery_short['hours']==500 and delivery_short['core_sha256']==delivery['core_sha256']
    assert not delivery_short['invariants'] and not delivery_short['final_invariants']
    institutions=read(FOLDER/'longa_5000h/instituicoes.json')
    cost=read(FOLDER/'longa_5000h/custo_campos_novos.json')
    overlaps=[{'town':i,'person':t['mayor']} for i,t in institutions['offices'].items()
              if t['mayor'] is not None and t['mayor']==t['general']]
    package={'rules':long['rules'],'delivery_core_sha256':delivery['core_sha256'],
        'campaign_core_sha256':long['core_sha256'],'short':metrics(short),'long':metrics(long),
        'delivery_short':metrics(delivery_short),
        'narrative_coverage':coverage,'final_mayor_general_overlap':overlaps,
        'new_model_fields_cost':cost,
        'scope':'Campanhas naturais independentes. Contadores de ações/epítetos não são contagem de personagens ou sagas.'}
    (FOLDER/'METRICAS_FASE_5.json').write_text(json.dumps(package,ensure_ascii=False,indent=2))
    registry=read(FOLDER/'EXECUCOES.json')
    registry['long_campaigns_completed']=1
    for entry in registry['executions']:
        if entry['folder'].endswith('longa_5000h'):
            entry.update(status='concluida_final',last_confirmed_hour=5000,final_summary_exists=True,
                         reason='Única longa, encerrada em 5000h, mesmo núcleo da curta validada anterior aos ajustes de entrega, save e validação concluídos.')
        if entry['folder'].endswith('curta_validada_500h'):
            entry['status']='concluida_pre_ajustes_entrega'
            entry['reason']='500h completas no núcleo da longa, anteriores aos ajustes finais de fé, residência e adesão.'
        if entry['folder'].endswith('curta_parcial_antes_correcoes'):
            entry['reason']='Interrompida após ponto confirmado em 150h para corrigir regressões antigas.'
        if entry['folder'].endswith('curta_parcial_renome_200h'):
            entry['reason']='Falhou na validação em 200h por renome excedendo limite; último checkpoint registrado em 150h.'
    if not any(e['folder'].endswith('curta_entrega_500h') for e in registry['executions']):
        registry['executions'].append({'folder':'reports/fase_5/curta_entrega_500h',
            'seed':delivery_short['seed'],'rules':delivery_short['rules'],
            'core_sha256':delivery_short['core_sha256'],'hours_requested':500,
            'last_confirmed_hour':500,'status':'concluida_entrega_final',
            'reason':'Código de entrega após ajustes finais; zero erros de integridade, save e exportação concluídos.',
            'final_summary_exists':True})
    (FOLDER/'EXECUCOES.json').write_text(json.dumps(registry,ensure_ascii=False,indent=2))
    rows=[('Seed','seed'),('Horas','hours'),('NPCs persistentes iniciais',lambda s:s['initial']['persistent']),
          ('População abstrata inicial',lambda s:s['initial']['abstract']),('Localidades',lambda s:s['initial']['towns']),
          ('NPCs vivos finais','alive'),('Mortes',lambda s:sum(s['death_causes'].values())),
          ('Causas das mortes','death_causes'),('Mortes alimentares com comida',lambda s:len(s['food_carried_deaths'])),
          ('Erros de integridade',lambda s:len(s['invariants'])+len(s['final_invariants'])),
          ('Histórico de eventos','history_events'),('Save (MiB)',lambda s:round(s['save_mib'],2)),
          ('Pico de memória do processo, incluindo exportação (MiB)',lambda s:round(s['memory_peak_mib'],2)),
          ('Simulação (min)',lambda s:round(s['runtime_seconds']/60,2)),('Exportação do save (s)',lambda s:round(s['save_seconds'],2))]
    lines=['## Auditoria natural e custo','',
        f"A curta validada **Serevan-5**, de 500h, e a única longa **Nhalven-5**, de 5.000h, usaram o mesmo núcleo SHA-256 `{long['core_sha256']}`, anterior aos ajustes finais explicitados abaixo. A longa começou com {long['initial']['persistent']} NPCs persistentes, {long['initial']['abstract']} habitantes abstratos, {long['initial']['towns']} localidades, {long['initial']['kingdoms']} reinos, {long['initial']['mayors']} prefeitos, {long['initial']['generals']} generais, {long['initial']['factions']} facções nativas e {long['initial']['divinities']} deuses.",
        '', '| Métrica | Curta do núcleo da longa | Longa | Curta de entrega |','|---|---|---|---|']
    for name,key in rows:
        get=(lambda s:s[key]) if isinstance(key,str) else key
        lines.append(f'| {name} | {get(short)} | {get(long)} | {get(delivery_short)} |')
    lines+=['',f"Na longa passaram **50 verificações periódicas**, além da validação inicial e final. Na curta passaram cinco periódicas, além da inicial e final. Não foi carregado save antigo. O núcleo não foi alterado durante a longa. As repetições curtas de diagnóstico estão identificadas em [EXECUCOES.json](<{FOLDER/'EXECUCOES.json'}>); houve somente uma campanha longa iniciada nesta fase.",
        '', f"**Ajustes posteriores explicitados:** a entrega usa SHA-256 `{delivery['core_sha256']}`. Depois da longa, foram corrigidos: hipótese recebida sobre o sucessor após apoteose; oração dirigida ao mortal realmente ascendido; prefeito que continuava no cargo após mudar de residência; oferta de adesão para quem já tinha três grupos; preservação de demandas formais e respostas públicas na sucessão municipal. O código da campanha permanece em `reports/fase_5/final_code`; o da entrega está em `reports/fase_5/entrega_code`. São hashes diferentes e não devem ser confundidos.",
        '', f"A suíte completa de **275 testes** passou novamente no código de entrega. Uma nova curta de **500h**, seed {delivery_short['seed']}, validou esse mesmo núcleo, com {sum(delivery_short['death_causes'].values())} mortes e zero erros de integridade. Os microcenários ampliados verificaram as condições raras e save/load. A campanha longa registrou {long['phase5']['events'].get('Apotheosis',0)} apoteoses, portanto não validou frequência natural dos caminhos divinos corrigidos. Não houve segunda longa. Registro: [ENTREGA_FINAL.json](<{FOLDER/'ENTREGA_FINAL.json'}>); curta: [resumo.json](<{FOLDER/'curta_entrega_500h/resumo.json'}>).",
        '', f"**A sobrevivência não melhorou na curta de entrega:** com a mesma seed, as mortes passaram de {sum(short['death_causes'].values())} para {sum(delivery_short['death_causes'].values())}, causas finais {delivery_short['death_causes']}. Houve {len(delivery_short['food_carried_deaths'])} mortes alimentares com comida carregada nessa execução. Mudanças nas escolhas sociais alteram a sequência de ações e a trajetória do RNG; essa comparação não isola qual ajuste contribuiu para cada morte. A piora observada permanece um limite da entrega, sem extrapolar a frequência da curta para 5.000h nem substituir a longa anterior.",
        '', '### Política, organizações e fé observadas','',
        '| Acontecimento | Curta do núcleo da longa | Longa | Curta de entrega |','|---|---:|---:|---:|']
    for kind in ('ProblemShared','GroupFormed','GroupJoined','GroupMeeting','GroupDissolved','ProposalCreated',
                 'ProposalSubmitted','PolicyDecided','PolicyRead','GroupProtested','MayorAppointed','RoyalAidDecided',
                 'FactionFounded','FactionJoined','FactionPromoted','FactionReport','OrganizationalAction','MilitaryOrder',
                 'PrayerOffered','DivineIntervention','SpiritualReport','FaithReinterpreted','DivinityKilled','Apotheosis',
                 'PowerTrained','ExecutionOpportunity','TerminalDecision','IncapacitatedSpared','ItemLegendReported'):
        lines.append(f"| {kind} | {short['phase5']['events'].get(kind,0)} | {long['phase5']['events'].get(kind,0)} | {delivery_short['phase5']['events'].get(kind,0)} |")
    p=long['phase5'];events=p['events']
    lines+=['',f"Causas dos grupos formados na longa: **{coverage['group_causes']}**. Encerramentos: {coverage['group_dissolutions']}. Estado final dos grupos: {p['groups_final']}; propostas ainda conservadas: {p['proposal_status_final']}; facções: {p['factions_final']}. Os objetos encerrados são removidos após o prazo; portanto, quantidade final é diferente da quantidade histórica.",
        '',f"Formações por tipo de localidade: {coverage['groups_by_town_kind']}. Grupos de vila não têm encaminhamento para uma autoridade urbana; esse limite se soma à dificuldade de contato entre prefeito e representante.",
        '',f"Houve {long['metrics'].get('Society:material_food',0)} unidades de comida e {long['metrics'].get('Society:material_money',0)} moedas contabilizadas nos efeitos políticos. Uma decisão pode ser parcial, adiada ou não encontrar beneficiário presente. Decisões e ações militares sem destinatários úteis não equivalem a mudança efetiva de vida.",
        '',f"Potenciais míticos: {p['mythic_total']} gerados, distribuição {p['mythic_distribution']}, {p['mythic_alive']} vivos ao fim. Mudanças para intenção matar por modo: {p['lethal_modes']}. Os modos representam escolhas registradas; não são mortes.",
        '',f"Divindades objetivas no fim: {p['actual_gods']}; divindades com conhecimento ontológico confirmado: {p['gods_with_confirmed_knowers']}. Mortais venerados ainda registrados: {p['believed_divine_mortals']}; mortais com apoteose objetiva: {p['actual_divine_mortals']}. O contador de veneração registrou {long['metrics'].get('Renown:mortal_venerated',0)} atualizações de observadores e não deve ser confundido com esse número de mortais.",
        '',f"Personagens com epíteto retido por algum observador: {p['epithet_subjects']}. Alcance final calculado: {p['reach_distribution']}. Itens históricos: {p['historical_items']}; com contato divino: {p['items_with_divine_contact']}; com crença registrada: {p['items_with_beliefs']}. Epítetos associados a ofício/proteção podem predominar sobre figuras épicas.",
        '', f"Sobreposição prefeito/General no estado final: {overlaps if overlaps else 'nenhuma observada'}. Isso não elimina a limitação potencial da via de usurpação apontada acima.",
        '', '### Qualidade das histórias e ausências','',
        f"A seleção documentou **{coverage['covered']}/22 categorias** com alguma evidência natural. Isso inclui transformações pequenas ou incompletas; não significa {coverage['covered']} sagas grandes. O arquivo [HISTORIAS_REAIS.md](<{FOLDER/'HISTORIAS_REAIS.md'}>) explica cada caso com fatos, estados e limites, sem inventar pensamentos.",
        '', 'Categorias sem exemplo natural suficiente nesta campanha:']
    for entry in coverage['categories'].values():
        if not entry['evidence_selected']:lines.append('- '+entry['name']+'.')
    lines+=['', 'A ausência de um arco raro não prova um bug. Porém, a persistência de poucos encontros, propostas entregues e serviços concluídos, diante de muitas tentativas, aponta um gargalo de continuidade. A próxima melhoria útil é transformar comunicação e participação em transições reais, preservando custos e conhecimento individual.',
        '', '### Custo e comparação com a base','',
        f"O save da longa ocupa **{long['save_mib']:.2f} MiB**. O processo alcançou **{long['memory_peak_mib']:.2f} MiB**, incluindo a serialização/exportação. A simulação levou {long['runtime_seconds']/60:.2f} minutos e a escrita do save {long['save_seconds']:.2f} segundos. Essas medidas dependem desta máquina e incluem o custo da auditoria. Não medem apenas a Fase 5.",
        '', f"Entre as duas campanhas independentes, o save cresceu {long['save_mib']/short['save_mib']:.2f} vezes. Não é uma medida da taxa exata de crescimento da mesma seed. O histórico final tem {long['history_events']} acontecimentos, e existem fatos, memória aplicada e registros anteriores que crescem além dos novos campos limitados.",
        '', f"Os valores compactos dos campos de modelo acrescentados ocupam aproximadamente **{cost['added_model_value_mib']:.2f} MiB**, sem nomes de campos e wrappers. A medida inclui os campos novos de fama, grupos, divindades, cargos, facções e itens, mas não isola os eventos/fatos/necessidades que eles geram nos campos anteriores. Não é medida de RAM nem custo total da Fase 5. A decomposição está em [custo_campos_novos.json](<{FOLDER/'longa_5000h/custo_campos_novos.json'}>).",
        '', 'A longa histórica da Fase 4.6, seed Corven-46, terminou com 1.274 vivos e 294 mortos de 1.568 NPCs iniciais: 260 por fome, 11 por fome+sede, seis por sede e 17 em combate. Seu save tinha 1.101,64 MiB. A seed, população e RNG diferem; não é possível atribuir a diferença inteira à Fase 5. O pico de memória antigo foi medido antes da exportação e não é diretamente comparável ao pico atual.',
        '', '### Prioridades justificadas para continuidade','',
        '1. Melhorar representação e contato útil entre membros e autoridade: incluir encaminhamento conhecido de demandas das vilas às cidades e passagem de respostas de um membro ao representante, sem leitura remota de estado. Isso pode concluir arcos existentes, em vez de criar novas pressões sem resposta.',
        '2. Reduzir tentativas previsivelmente inviáveis de organização/adesão com o conhecimento do NPC. Limites locais e ausência de interlocutor não deveriam produzir ação repetida sem progresso indefinidamente.',
        '3. Tornar a sobrevivência e a saída física das sedes das facções possíveis por abastecimento real, descoberta e vínculos. Criar membros ou suprimentos por script apagaria o problema em vez de resolvê-lo.',
        '4. Registrar mudanças de crença, título e consequências materiais de forma compacta e rastreável. Um contador agregado pode perder a identidade de quem mudou e a transformação concreta.',
        '5. Separar causalidade contribuinte da causa final das mortes e reduzir o custo de persistência. Isso melhora diagnóstico e permite campanhas maiores sem confundir dano acumulado, fome e combate.',
        '', f"Dados completos: [métricas consolidadas](<{FOLDER/'METRICAS_FASE_5.json'}>), [resumo da longa](<{FOLDER/'longa_5000h/resumo.json'}>), [save final](<{FOLDER/'longa_5000h/save_final.json'}>) e [preservação da geração](<{FOLDER/'PRESERVACAO_GERACAO.json'}>)."]
    report=ROOT/'RELATORIO_FASE_5.md';prefix=report.read_text().split('## Auditoria natural e custo')[0]
    report.write_text(prefix+'\n'.join(lines)+'\n')
    print(json.dumps({'report':str(report),'core':long['core_sha256'],'categories':coverage['covered'],
                      'long_hours':long['hours'],'overlaps':overlaps},ensure_ascii=False))


if __name__=='__main__':finish()
