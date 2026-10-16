"""Relatório da evidência exportada; não carrega Engine nem simula o save."""
import argparse
import json
from collections import Counter
from pathlib import Path

ROOT=Path('reports/fase_5_2_1')
FOLDER=ROOT/'campanha_1000h'

def table(header,rows):
    return '| '+' | '.join(header)+' |\n| '+' | '.join('---' for _ in header)+' |\n'+''.join('| '+' | '.join(map(str,row))+' |\n' for row in rows)+'\n'

def number(value,decimals=0):
    return f'{value:,.{decimals}f}'.replace(',', '_').replace('.', ',').replace('_', '.')

def link(label,path):
    return f'[{label}](<{Path(path).resolve()}>)'

def read(name):
    return json.loads((FOLDER/name).read_text())

def run():
    d=read('resultado_1000h.json');o=read('oportunidades_terminais.json');lore=read('material_lore.json')
    if d['seed']!='Thalendor-521':
        raise ValueError('Os casos revisados manualmente neste relatório pertencem à seed Thalendor-521.')
    c=d['events'];m=d['metrics'];i=d['initial'];names=lore['names']
    finishes=[ev for ev in d['deliberate_deaths'] if ev['context'].get('death_context')=='deliberate_finish']
    finish_op=[r for r in o['opportunities'] if r['context']['choice']=='finish']
    unexecuted=[r for r in finish_op if not r.get('chosen')]
    unknown=[r for r in d['active_decisions'] if r['target_alive_objectively'] is False and not any(f['confidence']>=60 for f in r['known_death_facts'])]
    death_total=sum(d['deaths_by_cause'].values());hungry=d['deaths_by_cause'].get('hunger',0)
    text='# Relatório — Fase 5.2.1: Thalendor-521\n\n'
    if finishes:
        text+=f"**Campanha concluída: {number(d['hours'])} horas e {len(finishes)} finalizações deliberadas naturais, todas com avaliação pós-morte.** O caminho decisão letal → ataque → oportunidade → escolha de finalizar → morte → PostKill funcionou. Não é necessário recalibrar a letalidade para satisfazer o critério desta fase.\n\n"
    else:
        text+='**Campanha concluída, sem finalização deliberada natural.** As escolhas observadas estão abaixo; não foram provocadas mortes para satisfazer uma meta.\n\n'
    text+=f"Seed **{d['seed']}**, versão `{d['rules']}`. Mundo novo, sem jogador, sem histórico inicial e sem save carregado. A duração de 1.000h substitui as 300h do documento por pedido do usuário. As tentativas com Vaelmir-521 interrompidas em 582h e 650h permanecem arquivadas; o usuário autorizou começar novamente com uma seed nova. O núcleo ficou congelado durante toda esta execução.\n\n"
    text+=table(['Hora','NPCs vivos','Decisões criadas','Ataques letais','Oportunidades','Mortes intencionais'],[(s['hour'],s['alive'],s['decisions'],s['lethal_attacks'],s['opportunities'],s['deliberate_deaths']) for s in d['snapshots'] if s['hour'] in (0,250,500,750,1000)])
    text+='## Correções e testes prévios\n\n'
    text+='A escolha terminal vencedora passou a executar sem o sorteio residual entre alternativas próximas. Captura, ajuda e retirada registram escolha e sucesso; a telemetria separa candidatos, considerações e decisões. Actors religiosos foram diferenciados pelo significado do ato em cada domínio. Dano, HP, armas, frequência de ataque, barreira letal e parâmetros de intervenção divina foram preservados.\n\n'
    text+='As falhas anteriores eram de memória reentrante: um fato podia ser expulso enquanto ainda era processado, ou antes de uma decisão letal fixar sua causa. Referências locais e proteção temporária dos fatos em processamento/criação corrigem esses casos, mantendo o limite de 64 memórias. Listas históricas de auditoria também foram isoladas de alterações posteriores.\n\n'
    text+='**Seis testes focados e quatro regressões passaram**: finalizar/poupar, morte conhecida versus desconhecida, encerramento por ruminação, Actors específicos e sobreposição coerente; anonimato, persistência, recuperação e continuidade determinística. As duas falhas anteriores foram reproduzidas antes das correções. Não foi repetida a suíte completa. Logs: `testes_6_memoria_integridade.log` e `smoke_4_memoria_integridade.log`.\n\n'
    text+='## Funil letal e consequências\n\n'
    rows=[(k,c.get(k,0)) for k in ('LethalCandidateEvaluated','LethalCandidateRejected','LethalConsideration','LethalDecision')]
    rows += [('Decisões que chegaram a ataque',d['decisions_with_lethal_attack']),('LethalAttack',m.get('LethalAttack',0)),('ExecutionOpportunity',c.get('ExecutionOpportunity',0))]
    rows += [('Terminal'+choice.capitalize()+'Chosen',d['terminal_choices'].get(choice,0)) for choice in ('finish','spare','capture','help','withdraw')]
    rows += [(k,m.get(k,0)) for k in ('IntentionalCombatKill','DeliberateFinish')]
    rows += [(k,c.get(k,0)) for k in ('PostKillAppraisal','DeathAffinityIncrease','LethalDecisionResolved','LethalDecisionAbandoned')]
    text+=table(['Etapa','Ocorrências'],rows)
    text+='Candidatos são transições relevantes, decisões são episódios e ataques são ações. Não são contagens de pessoas distintas nem etapas com correspondência obrigatória de um para um.\n\n'
    text+=f"Sucessos terminais: `{d['terminal_successes']}`. Houve seis escolhas de captura e cinco execuções bem-sucedidas. Os **{c.get('PostKillAppraisal',0)} PostKill** incluem as quatro finalizações e seis mortes não intencionais em combate; não são dez homicídios deliberados. Nenhuma DeathAffinity aumentou.\n\n"
    text+=table(['Autor → vítima','Hora','Culpa','Alívio','Orgulho','Prazer / fascinação'],[(names[str(ev['actor_id'])]+' → '+names[str(ev['target_id'])],ev['turn'],number(ev['context']['post_kill_appraisal']['feelings']['guilt'],2),number(ev['context']['post_kill_appraisal']['feelings']['relief'],2),number(ev['context']['post_kill_appraisal']['feelings']['pride'],2),'0 / 0') for ev in finishes])
    text+='Vergonha, medo, insensibilidade, luto e conflito moral estão nas avaliações completas. Nenhuma das quatro finalizações criou afinidade com a morte ou automaticamente um assassino recorrente.\n\n'
    text+='## Decisões antigas e conhecimento\n\n'
    text+=table(['Idade da decisão ativa','Quantidade'],list(d['active_decisions_age'].items()))
    text+=f"Encerramentos: `{d['closure_reasons']}`. O estado final retém `{d['decisions_retained_by_status']}`; decisões encerradas podem sair da memória limitada, mas seus eventos permanecem no histórico. **{len(unknown)} decisões** tinham alvo morto e ausência de notícia confiável da morte. Isso respeita o conhecimento individual.\n\n"
    text+='Silas Corven soube diretamente da morte de Tomas Kars na hora 591 e resolveu a decisão. John Bruma não soube da morte de Cael Luar na hora 509 e ainda tinha decisão aberta na hora 1.000. Houve três encerramentos por vida segura e ruminação reduzida. Entretanto, **73 das 101 decisões ativas têm mais de 168h**: a duração continua merecendo acompanhamento; não foi acrescentado timeout.\n\n'
    text+='## Religião\n\n'
    gods=d['religion_final']['gods'];before=i['religion']['gods']
    text+=table(['Deus','Seguidores início → fim','Devotos finais','Cultistas finais','Actors finais','Actors exclusivos'],[(g['name'],str(before[id]['followers'])+' → '+str(g['followers']),g['devoted'],g['cultists'],g['actors'],g['exclusive_actors']) for id,g in gods.items()])
    pairs=[(g['name']+' + '+gods[other]['name'],count) for id,g in gods.items() for other,count in g['shared_actors'].items() if int(id)<int(other)]
    text+=table(['Domínios compartilhados','Actors'],pairs)
    text+=f"A união contém **{d['religion_final']['unique_actors_total']} pessoas distintas**. Actor representa feitos alinhados nos últimos 200h, inclusive de alguém que não segue aquele deus. Aurion começou sem seguidores porque nenhum reino desta seed recebeu o Culto do Sol; seus Actors não demonstram conversão.\n\n"
    text+=f"Relatos de declínio: **{c.get('ReligiousDeclineReported',0)}**; notícia de crescimento rival: **{c.get('RivalFaithGrowthKnown',0)}**; intervenções: **{c.get('DivineIntervention',0)}**. O canal existente exige duas perdas conhecidas de membros reconhecidos por ritual/declaração, seguidas de um relato religioso. Ele não transportou declínio agregado nesta campanha. **O desaparecimento agregado de Actors não tem canal próprio.** A deterioração objetiva pode continuar desconhecida pelos deuses.\n\n"
    text+='## Incongruências e limites encontrados\n\n'
    text+='**Captura impossível oferecida — confirmado.** Na hora 500, John Bruma escolheu capturar Cael Luar, já detido por Iria Solaris de 491h até 503h. O escore de captura foi 103,50; a execução recusou. O cálculo terminal verifica guarda/caso conhecido, mas omite a condição de detenção do alvo que `Justice.capture` exige. Eventos **553168 e 564020**. É uma inconsistência entre seleção e execução, sem corrupção do save; não foi corrigida durante esta validação.\n\n'
    text+=f"**Fome ainda domina a mortalidade.** Causas finais: `{d['deaths_by_cause']}`. Fome isolada representa **{hungry}/{death_total} = {number(hungry/death_total*100,2)}%**; outras quatro mortes envolveram fome e sede. O rótulo registra a causa final, não todo dano anterior: Cael Luar acumulou 117 HP de danos de combate e nove de fome antes da morte classificada como fome. Esses totais acumulados não equivalem ao saldo de HP, pois houve recuperação.\n\n"
    verification=FOLDER/'verificacao_narrativa.json'
    if verification.exists():
        food=read('verificacao_narrativa.json')['final_food']
        text+=f"Na hora 1.000 havia **{number(food['town_food'])} unidades de comida nos estoques das localidades e {food['npc_food']} nos inventários dos vivos**. Disponibilidade mundial não demonstra acesso individual: esse retrato final não prova comida acessível na localidade e hora de cada morte. O próximo diagnóstico deve verificar acesso, dinheiro, lesões e prioridade das ações por vítima.\n\n"
    repeated=Counter(names.values())
    text+=f"**Identificação narrativa ambígua — confirmado.** {len(names)} NPCs usam {len(repeated)} nomes completos distintos; {sum(n>1 for n in repeated.values())} nomes se repetem. Duas Elena Kars formaram o primeiro grupo. Os IDs continuam distintos, sem colisão de entidades; profissão, localidade e ID foram usados na crônica para evitar confusão.\n\n"
    text+=f"**Oportunidade calculada não garante escolha executada.** Finalizar liderou em {len(finish_op)} retratos de oportunidade; {len(unexecuted)} não tiveram uma escolha terminal associada: horas 580, 838 e 913. Necessidades vitais concorrem antes da escolha terminal, e presença/saúde podem mudar. A evidência exportada não identifica o motivo exato de cada perda; esses casos permanecem uma lacuna de acompanhamento, não prova de sorteio residual. Nas escolhas efetivas houve **zero divergências** entre o vencedor contextual e a ação terminal.\n\n"
    text+='**Linha extrema: somente hipótese.** Ruan Montes finalizou quando finalizar marcou 70,74. Aldren Kars, com ruminação 100 e pressão 75, retirou-se porque o medo elevou essa opção a 75 contra 59,71 de finalizar. Os exemplos não exigem morte automática. Não foi implementada uma faixa irreversível; as oportunidades sem desfecho merecem investigação antes de qualquer nova regra.\n\n'
    text+=f"Validação: **{len(d['integrity_checks'])} verificações estruturais**, **{len(d['structural_errors'])} erros estruturais** e **{len(d['causal_violations'])} alertas causais**. A captura acima foi encontrada na revisão manual; zero alertas não significa ausência de todo bug. A auditoria cobre referências históricas, causa/capacidade dos ataques, escolha terminal, morte conhecida e origem/custo divino.\n\n"
    if d['causal_violations']:text+=f"Alertas: `{d['causal_violations']}`.\n\n"
    text+='## Evidência preservada\n\n'
    text+='A seed nova produziu outras pessoas, localidades, distribuição religiosa e trajetórias. Como houve também correções de memória e maior duração alcançada, a comparação com Vaelmir-521 não isola o efeito de cada mudança. A crônica apresenta seis trajetórias, sem diálogos ou eventos inventados.\n\n'
    text+=f"Tempo total **{number(d['runtime_seconds']/60,2)}min**; pico de memória incluindo exportação **{number(d['memory_peak_mib_including_export'],1)}MiB**. Save único **{number(d['save_bytes']/2**20,2)}MiB**, com **{number(d['history_events'])} eventos históricos**. Núcleo congelado: `{d['core_sha256']}`. O hash do save está em `save_sha256.txt`; não foi duplicado o histórico bruto.\n\n"
    text+=' · '.join([link('Crônica nova',ROOT/'HISTORIAS_REAIS.md'),link('Resultado completo',FOLDER/'resultado_1000h.json'),link('Retratos terminais',FOLDER/'oportunidades_terminais.json'),link('Verificação narrativa',verification),link('Save final',FOLDER/'save_final.json')])+'.\n'
    Path('RELATORIO_5_2_1.md').write_text(text)

def run_failure():
    failure=read('falha_resumida.json');manifest=read('manifesto.json')
    checkpoint=FOLDER/'checkpoint_resumo.json'
    snapshots=json.loads(checkpoint.read_text())['snapshots'] if checkpoint.exists() else []
    partial_path=FOLDER/'evidencia_parcial_falha.json'
    partial=json.loads(partial_path.read_text()) if partial_path.exists() else {}
    text=f"# Relatório — Fase 5.2.1 interrompida\n\nA campanha com seed **{manifest['seed']}**, iniciada do zero e sem jogador, parou na hora **{failure['hour']}**. As **1.000 horas não foram concluídas**. Falha: `{failure['error']}`.\n\n"
    if snapshots:
        text+=f"Último marco validado: **{snapshots[-1]['hour']}h**.\n\n"
        text+=table(['Hora','Vivos','Decisões','Ataques letais','Oportunidades','Mortes intencionais'],[(r['hour'],r['alive'],r['decisions'],r['lethal_attacks'],r['opportunities'],r['deliberate_deaths']) for r in snapshots])
    if partial:text+=f"Escolhas terminais até a interrupção: `{dict(Counter(r['choice'] for r in partial['terminal']))}`.\n\n"
    text+=f"Erros estruturais: `{failure['structural_errors']}`. Alertas causais: `{failure['causal_violations']}`. Não existe save final concluído desta campanha.\n\n"
    text+=' · '.join([link('Falha',FOLDER/'falha_resumida.json'),link('Evidência parcial',partial_path),link('Crônica',ROOT/'HISTORIAS_REAIS.md')])+'.\n'
    Path('RELATORIO_5_2_1.md').write_text(text)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--folder',type=Path,default=FOLDER)
    FOLDER=parser.parse_args().folder
    if (FOLDER/'falha_resumida.json').exists():run_failure()
    else:run()
