"""Comparação observacional e extração de histórias; não modifica campanhas."""
from collections import Counter, defaultdict
import hashlib
import json
import math
from pathlib import Path
from procedural.persistence import JsonRepository, decode

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'reports/fase_3'
OLD = ROOT / 'reports/tres_perspectivas_20261007'
MODES = ('jogador', 'espectador', 'mundo')
PERSONAL = ('family', 'grief', 'revenge', 'protection', 'status', 'advancement')


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def write(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')


def stock(world, owner, kind):
    return sum(q for i, q in owner.inventory.items() if world.items[i].kind == kind)


def old_summary(world, report, official):
    people = [c for c in world.characters.values() if not c.is_player]
    alive = [c for c in people if c.alive]
    empty = [t for t in world.towns.values() if not stock(world, t, 'food')]
    def price(t):
        expected = max(8, t.population//100)
        scarcity = max(.45, min(4, expected/max(1, stock(world, t, 'food'))))
        return max(2, math.ceil(3*(scarcity+min(1, t.demand.get('food', 0)/20))*1.1))
    cooks = lambda t: sum(c.alive and c.town_id == t.id and c.position.map_id == t.id
                          and c.profession == 'cozinheiro' for c in people)
    deaths = report['deaths']
    return {'initial_alive':len(people), 'alive':len(alive), 'dead':len(deaths),
            'towns':len(world.towns), 'empty_food':len(empty),
            'empty_food_full_grain':sum(stock(world,t,'grain')>=240 for t in empty),
            'empty_food_live_cook':sum(cooks(t)>0 for t in empty),
            'empty_food_no_cook':sum(cooks(t)==0 for t in empty),
            'poor_below_one_meal':sum(c.money<price(world.towns[c.town_id]) for c in alive),
            'poor_below_10':sum(c.money<10 for c in alive),
            'hunger_70':sum(c.hunger>=70 for c in alive), 'thirst_70':sum(c.thirst>=70 for c in alive),
            'hunger_85':sum(c.hunger>=85 for c in alive), 'thirst_85':sum(c.thirst>=85 for c in alive),
            'localities_functionally_empty':sum(not any(c.alive and c.position.map_id==t.id for c in people)
                                                for t in world.towns.values()),
            'kingdoms_without_ruler':sum(k.ruler_id is None for k in world.kingdoms.values()),
            'deaths_carrying_food':sum(d['food_carried']>0 for d in deaths),
            'deaths_carrying_water':sum(d['water_carried']>0 for d in deaths),
            'workers_retrained':0, 'workers_materialized':0, 'workers_trained':0,
            'workers_formed_after_local_cook_death':0,
            'death_conditions':dict(Counter('both' if d['hunger']>=100 and d['thirst']>=100 else
                              'thirst' if d['thirst']>=100 else 'hunger' if d['hunger']>=100 else 'other'
                              for d in deaths))}


def behavior(summary, official):
    selected = official['selected_distribution']
    summary['selected_distribution'] = selected
    summary['physiological_percent'] = selected['physiological']/sum(selected.values())*100
    summary['personal_selected'] = sum(selected.get(k,0) for k in PERSONAL)
    summary['personal_expired'] = sum(sum(official['lifecycle']['Expired'].get(k,{}).values()) for k in PERSONAL)
    summary['personal_satisfied'] = sum(sum(official['lifecycle']['Satisfied'].get(k,{}).values()) for k in PERSONAL)
    summary['quest_types'] = official['quest_types']
    summary['personal_events'] = official['personal_event_counts']


def numbered_events(path):
    with path.open(encoding='utf-8') as stream:
        for number,line in enumerate(stream,1):
            yield number,json.loads(line)


def stories(mode, world):
    directory = OUT/'auditorias'/mode
    frames = read(directory/'quadros_economicos.json')
    entries = list(numbered_events(directory/'economia_eventos.jsonl'))
    chains = defaultdict(list)
    for line,e in entries:
        if e['kind'] in ('TrainingStarted','TrainingProgress','ProfessionChanged','TrainingAbandoned','WorkerMaterialized'):
            chains[e['actor_id']].append((line,e))
    materialized = {e['actor_id'] for _,e in entries if e['kind']=='WorkerMaterialized'}
    changed = [(line,e) for line,e in entries if e['kind']=='ProfessionChanged' and e['actor_id'] not in materialized]
    selected = []
    if changed:
        # Um formado que sobrevive, se houver; depois o primeiro caso registrado.
        chosen = next((e['actor_id'] for _,e in changed if world.characters[e['actor_id']].alive),changed[0][1]['actor_id'])
        selected.append(('Mudança de profissão de um residente existente',chosen))
    new_ids = sorted(materialized,key=lambda i:chains[i][0][1]['turn'])
    for alive,title in ((True,'Materialização com continuidade'),(False,'Materialização sem sobrevivência garantida')):
        chosen = next((i for i in new_ids if world.characters[i].alive == alive),None)
        if chosen is not None: selected.append((title,chosen))
    sections=[]; records=[]
    for title,identity in selected:
        person=world.characters[identity]
        chain=chains[identity]
        important=[(n,e) for n,e in chain if e['kind']!='TrainingProgress']
        progresses=[e['context']['progress'] for _,e in chain if e['kind']=='TrainingProgress']
        text=[f'### {title}: {person.name} (ID {identity})',
              f'Localidade: {world.towns[person.town_id].name} (ID {person.town_id}). '
              f'No fim: {"vivo" if person.alive else "morto"}; profissão {person.profession or "sem profissão"}.',
              '| Turno absoluto | Registro | Evidência |','|---:|---|---|']
        for number,event in important:
            text.append(f'| {event["turn"]} | {event["kind"]} | {event["description"]} (linha {number}) |')
        text.append('')
        if progresses:text.append(f'Prática registrada: progresso máximo {max(progresses)} horas produtivas. '
                                  'O intervalo entre começo e conclusão inclui viagens e outras necessidades.')
        death=world.death_records.get(identity)
        if death:text.append(f'Morte no turno {death["turn"]}: condições {death["cause"]}, '
                              f'fome {death["hunger"]}, sede {death["thirst"]}; '
                              f'comida/água carregadas {death["food"]}/{death["water"]}.')
        previous = [d for d in world.death_records.values() if d['town_id']==person.town_id and
                    d['profession']=='cozinheiro' and d['turn']<chain[0][1]['turn']]
        if previous:
            latest=max(previous,key=lambda d:d['turn'])
            text.append(f'Contexto local comprovado: antes dessa sequência, o cozinheiro '
                        f'{latest["name"]} morreu no turno {latest["turn"]}. Não se presume vínculo familiar.')
        before=next((f for f in reversed(frames) if f['turn']<=chain[0][1]['turn']),frames[0])
        local_before=next(t for t in before['towns'] if t['id']==person.town_id)
        local_end=next(t for t in frames[-1]['towns'] if t['id']==person.town_id)
        text.append(f'Fotografias locais: no turno {before["turn"]}, alimento '
                    f'{local_before["report"]["stock"]["food"]}, trigo '
                    f'{local_before["report"]["stock"]["grain"]}, cozinheiros '
                    f'{local_before["report"]["cook_count"]}; no turno {frames[-1]["turn"]}, alimento '
                    f'{local_end["report"]["stock"]["food"]}, trigo '
                    f'{local_end["report"]["stock"]["grain"]}, cozinheiros '
                    f'{local_end["report"]["cook_count"]}. Fotografias não demonstram abastecimento contínuo.')
        text.append('A sequência comprova ações e consequências individuais. Ela não comprova sozinha '
                    'a recuperação do mercado nem uma relação familiar com o profissional anterior.')
        table_end=text.index('')
        sections.append('\n\n'.join(text[:2])+'\n\n'+'\n'.join(text[2:table_end])+
                        '\n\n'+'\n\n'.join(text[table_end+1:]))
        records.append({'mode':mode,'npc_id':identity,'title':title,'events':important,'death':death})
    temporary=next(((n,e) for n,e in entries if e['kind']=='TemporaryWorkPerformed' and
                   not world.characters[e['actor_id']].is_player),None)
    if temporary:
        n,e=temporary
        sections.append(f'### Trabalho temporário realizado\n\nTurno {e["turn"]}: {e["description"]} '
                        f'Valores físicos: `{json.dumps(e["context"],ensure_ascii=False)}`. '
                        f'Evidência: `economia_eventos.jsonl`, linha {n}. Pagamento por alimento é '
                        'comprovado; não se infere uma motivação pessoal que o evento não registrou.')
    family_quests=defaultdict(list)
    for q in world.quests.values():
        if q.kind in ('family','family_care'):
            family_quests[q.owner_id,q.target_id].append(q)
    if family_quests:
        (owner_id,target_id),quests=max(family_quests.items(),key=lambda pair:len(pair[1]))
        owner,target=world.characters[owner_id],world.characters[target_id]
        relationship=next((r.kind for r in world.relationships.values() if r.source_id==owner_id and
                           r.target_id==target_id and r.kind in ('casamento','pai_de','filho_de')), 'familiar')
        lines=[f'### Continuidade familiar: {owner.name} e {target.name}',
               f'Relação registrada: {relationship}; IDs {owner_id}/{target_id}. '
               f'Esta sequência contém {len(quests)} pedidos relativos ao mesmo par, '
               'não histórias independentes para cada pedido.',
               '| Criação | Pedido | Desfecho | Conclusão |','|---:|---|---|---:|']
        for q in sorted(quests,key=lambda q:q.created_at):
            lines.append(f'| {q.created_at} | {q.title} (ID {q.id}, {q.context.get("resource",q.kind)}) '
                         f'| {q.status} | {q.completed_at if q.completed_at is not None else "—"} |')
        sections.append('\n\n'.join(lines[:2])+'\n\n'+'\n'.join(lines[2:])+
                        '\n\nEvidência: quests persistidas em `save_final.json` e detalhes em '
                        '`relatorio.json`. A repetição mostra continuidade do vínculo e um limite '
                        'de variedade narrativa: pedidos de provisão recorrentes ainda concentram '
                        'o arco em sobrevivência. Conclusões são ajuda efetiva, não prova de '
                        'estabilidade econômica permanente.')
    personal=list(numbered_events(directory/'eventos_pessoais.jsonl'))
    for kind in ('RemainsLocated','ComfortGiven','Remembrance','PersonLocated'):
        example=next(((n,e) for n,e in personal if e['kind']==kind),None)
        if example:
            n,e=example
            sections.append(f'### Consequência pessoal: {kind}\n\nTurno {e["turn"]}: {e["description"]} '
                            f'(ator {e["actor_id"]}, alvo {e["target_id"]}). '
                            f'Evidência: `eventos_pessoais.jsonl`, linha {n}. '
                            'Este é um evento pessoal efetivamente executado, não só uma necessidade selecionada.')
    return '\n\n'.join(sections),records


def main():
    comparisons=[]; narrative=['# Histórias observadas na Fase 3',
        'Campanhas espontâneas de 10.000 horas, após as correções de cotação desconhecida e estoque vazio. '
        'Turnos são absolutos: as campanhas começam em 24. Os cenários A–G não entram '
        'neste arquivo. As linhas citadas pertencem à pasta do modo indicado.']
    examples=[]
    for mode in MODES:
        directory=OUT/'auditorias'/mode
        metrics=read(directory/'metricas_fase3.json');official=read(directory/'metricas_fase2.json')
        world=JsonRepository().load(directory/'save_final.json')
        # Decodificação somente para leitura; não carrega nem migra o mundo antigo no motor.
        old_world=decode(read(OLD/mode/'save_final.json')['world'])
        old=old_summary(old_world,read(OLD/mode/'relatorio.json'),read(OLD/mode/'metricas_fase2.json'))
        behavior(old,read(OLD/mode/'metricas_fase2.json'))
        current=dict(metrics['final']['summary']);behavior(current,official)
        frames=read(directory/'quadros_economicos.json')
        current.update({k:metrics[k] for k in ('deaths_carrying_food','deaths_carrying_water','workers_retrained',
                                              'workers_trained','workers_materialized','death_conditions')})
        current['initial_alive']=frames[0]['summary']['alive'];current['towns']=len(world.towns)
        current['materialized_alive']=sum(c.alive for c in world.characters.values() if c.origin.startswith('Habitante abstrato de '))
        current['materialized_dead']=current['workers_materialized']-current['materialized_alive']
        current['original_dead']=current['dead']-current['materialized_dead']
        current['original_mortality_percent']=current['original_dead']/current['initial_alive']*100
        current['workers_formed_after_local_cook_death']=len({e['actor_id'] for _,e in
            numbered_events(directory/'economia_eventos.jsonl') if e['kind']=='ProfessionChanged' and
            any(d['profession']=='cozinheiro' and d['town_id']==e['target_id'] and d['turn']<e['turn']
                for d in world.death_records.values())})
        old['original_mortality_percent']=old['dead']/old['initial_alive']*100
        current['production_total']={k:sum(p.get(k,0) for p in metrics['production_by_locality'].values()) for k in ('food','grain')}
        current['vacancies_open']=[{'town_id':t.id,'name':t.name,'hours':world.turn-v['since'],**v}
                                  for t in world.towns.values() for v in t.professional_demand.values()]
        comparisons.append({'mode':mode,'seed':world.seed,'phase2':old,'phase3':current})
        story,record=stories(mode,world);examples.extend(record)
        narrative.append(f'## {mode.capitalize()} — {world.seed}\n\n'+story)
    write(OUT/'comparativo.json',comparisons);write(OUT/'historias_evidencias.json',examples)
    (OUT/'HISTORIAS.md').write_text('\n\n'.join(narrative)+'\n',encoding='utf-8')
    labels={'initial_alive':'NPCs vivos iniciais','towns':'Localidades','alive':'NPCs vivos finais','dead':'Mortes durante a campanha',
        'original_mortality_percent':'Mortalidade do elenco inicial (%)','physiological_percent':'Seleções fisiológicas (%)',
        'empty_food':'Mercados sem comida','empty_food_full_grain':'Sem comida e trigo cheio','poor_below_one_meal':'Dinheiro abaixo de uma ração',
        'poor_below_10':'Dinheiro abaixo de dez moedas','hunger_70':'Fome ≥70','thirst_70':'Sede ≥70','hunger_85':'Fome ≥85','thirst_85':'Sede ≥85',
        'deaths_carrying_food':'Mortes carregando comida','deaths_carrying_water':'Mortes carregando água',
        'localities_functionally_empty':'Localidades sem NPC vivo presente','personal_selected':'Seleções pessoais',
        'personal_expired':'Episódios pessoais expirados','personal_satisfied':'Episódios pessoais satisfeitos',
        'workers_retrained':'Residentes existentes formados','workers_trained':'Conclusões de formação (todos)',
        'workers_formed_after_local_cook_death':'Formados após morte de cozinheiro local',
        'workers_materialized':'Habitantes materializados'}
    table=['| Indicador | Jogador F2 → F3 | Espectador F2 → F3 | Mundo F2 → F3 |','|---|---:|---:|---:|']
    def fmt(value):return f'{value:.2f}' if isinstance(value,float) else str(value)
    for key,label in labels.items():
        table.append('| '+label+' | '+' | '.join(f'{fmt(c["phase2"][key])} → {fmt(c["phase3"][key])}' for c in comparisons)+' |')
    (OUT/'COMPARACAO.md').write_text('# Comparação observacional entre versões\n\n'+ '\n'.join(table)+
        '\n\nA versão participa da seed: geografia, elenco inicial e número de localidades mudam. '
        'Os novos materializados também podem morrer. A mortalidade do elenco inicial exclui essas novas identidades. '
        'Não é um experimento que isola o efeito de cada mecanismo. Pobreza mede caixa versus preço local, '
        'inclusive para quem já carrega alimento; contagens ≥70/≥85 são fotografias finais dos sobreviventes. '
        'Seleção pessoal pode incluir preparação fisiológica; expiração inclui encerramento por morte. '
        'Formados após morte local mede identidades que concluíram formação numa cidade com morte culinária '
        'anterior; não associa cada formado a um morto específico nem comprova estabilização do posto.\n',encoding='utf-8')
    for c in comparisons:
        n=c['phase3'];print(c['mode'], {k:n[k] for k in ('alive','dead','original_dead','materialized_dead','physiological_percent','personal_selected','workers_trained')})


if __name__=='__main__':main()
