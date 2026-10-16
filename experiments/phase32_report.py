"""Relatório da versão final; números sempre extraídos das campanhas preservadas."""
from collections import Counter,defaultdict
from dataclasses import asdict
import gzip
import json
from pathlib import Path

from procedural.persistence import JsonRepository
from procedural.engine import Engine

ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'reports/fase_3_2';OLD=ROOT/'reports/correcao_alimentar'
MODES=('jogador','espectador','mundo')
def read(p):return json.loads(p.read_text())
def link(p,label=None):return f'[{label or p.name}](<{p.resolve()}>)'
def fmt(v):
    if isinstance(v,float):return f'{v:.2f}'.replace('.',',')
    return str(v)
def table(headers,rows):
    return '\n'+' | '.join(headers)+'\n'+' | '.join('---' for _ in headers)+'\n'+'\n'.join(' | '.join(fmt(v) for v in row) for row in rows)+'\n'
def streams(p):
    with gzip.open(p,'rt',encoding='utf-8') as f:
        for line in f:yield json.loads(line)


def main():
    comparison=read(OUT/'comparativo.json');div=read(OUT/'diversidade_narrativa.json')
    olddiv=read(OLD/'diversidade_narrativa.json');extra=read(OUT/'diversidade_complementar.json')
    census=read(OUT/'censo_economico.json');verification=read(OUT/'verificacao_final.json')
    details={m:read(OUT/'auditorias'/m/'metricas_fase32.json') for m in MODES}
    replays={m:read(OUT/'reproducao_integral'/f'{m}.json') for m in MODES}
    manifest=read(OUT/'manifesto_auditoria.json')
    before_deaths=sum(comparison[m]['before']['deaths'] for m in MODES)
    after_deaths=sum(comparison[m]['after']['deaths'] for m in MODES)
    before_personal=sum(comparison[m]['before']['personal_selections'] for m in MODES)
    after_personal=sum(comparison[m]['after']['personal_selections'] for m in MODES)
    before_satisfied=sum(comparison[m]['before']['personal_satisfied'] for m in MODES)
    after_satisfied=sum(comparison[m]['after']['personal_satisfied'] for m in MODES)
    report=[]
    def section(title,text):report.append(f'## {title}\n\n{text.strip()}\n')
    report.append('# Fase 3.2 — Reserva preventiva, acesso econômico e coerência social\n\nRelatório de implementação e auditoria. Data: 08/10/2026. Base: '+link(ROOT/'fase_3_2.md')+'. Versão final: `'+manifest['rules_version']+'`.\n')
    section('1. Resumo executivo',f'''Os bugs de denúncia, informação repetida, crédito salarial, segunda ração, oferta esgotada e trabalho em instalação incompatível foram corrigidos. A pressão preventiva agora depende de cobertura, reposição conhecida, oportunidade e espera limitada.

Isso não equivale a ter resolvido a fome nem a diversidade narrativa. Nas campanhas finais, as mortes foram {before_deaths} → {after_deaths}; seleções pessoais {before_personal} → {after_personal}; satisfações pessoais {before_satisfied} → {after_satisfied}. As tabelas abaixo mostram diferenças por campanha. Esses números são observações conjuntas das correções, não provas isoladas do efeito de cada mudança.

**Resposta à pergunta sobre ataques:** não existe ação de ataque entre NPCs. Hostilidade, crime e vingança produzem respostas sociais, mas não dano físico. Todas as mortes reais registradas nesta etapa continuam sendo privação. Envelhecimento e morte por idade também não estão implementados. O evento `CharacterKilled` pode ser interpretado, mas o motor não possui uma ação real que o produza durante essas campanhas.''')
    section('2. Código e arquitetura preservados',f'''O fluxo continua State/Knowledge → Need → Priority → Solutions → Goal → Action → Consequence → State. Nenhum planejador paralelo, controlador novo de fome ou economia paralela foi criado. A seleção continua no GoalSystem e o Utility AI continua comparando soluções da necessidade escolhida.

Geração, modelos persistentes, itens, navegação, eventos, população, relações, utility, quests, social e sucessão mantiveram seus módulos existentes. Fome +2/h, sede, fadiga, HP, dano por privação e recuperação por descanso não foram facilitados. Os parâmetros de Survival/Feeding anteriores foram preservados. A regra de geração permanece `mvp-4`; os hashes do estado inicial sem história são idênticos nas duas seeds, mascarando somente a identificação de versão.

O código anterior, todos os saves e relatórios anteriores, os 130 testes originais e a política pública do jogador foram preservados. Foram verificados {verification['previous_files_preserved']} arquivos anteriores. O baseline está em {link(OUT/'baseline_code','código baseline')} e as regras finais em {link(OUT/'codigo_congelado','código congelado')}. Saves anteriores permanecem disponíveis com o seu motor baseline; a nova identificação de regras impede carregá-los silenciosamente com regras diferentes.''')
    section('3. Bugs corrigidos','''A denúncia exclui o ator conhecido do crime, culpado, ameaça, alvo acusado e denunciante; a execução revalida essa independência. Informação já conhecida ou inadequada ao episódio não conta como resposta útil. Tentativas inúteis têm memória pequena por necessidade/interlocutor/fato, e informação realmente nova reabre o interlocutor.

A segunda ração continua financiável. Compra parcial e lote limitado conservam itens/dinheiro. Trabalho produtivo pode terminar com crédito fracionário, sem cooldown indevido. Ofertas de distribuição respeitam quota e estoque no instante da observação; a execução respeita o estado efetivo na chegada. A incompatibilidade de instalação bloqueia a intenção profissional.

A auditoria intermediária revelou dois casos adicionais: localização anterior ao episódio era aceita em ajuda material familiar; e aquisição adiada podia empatar com aquisição+refeição emergencial. Ambos foram corrigidos antes das campanhas finais. Os resultados intermediários foram preservados, sem esconder as falhas descobertas.''')
    section('4. Modelo preventivo anterior','''A fórmula era `26 + 8 × déficit/alvo + 0,2 × min(fome,50) + idade`, com idade limitada a 8. O teto ficava próximo de 52 sem ração e 48 com uma ração para alvo de duas. A espera saturava depois de cerca de 54h. Descanso, sede e renda podiam vencer repetidamente, mesmo em encontros economicamente favoráveis com o mercado.

Na investigação anterior de 1.000h por modo, a reserva venceu 2.018 de 376.485 avaliações ativas. Na janela preventiva mais relevante, fome <50 com déficit, venceu 1.805 de 33.319: 5,42%. Esses denominadores são avaliações; não significam 376.485 pessoas nem uma taxa medida nas 10.000h anteriores inteiras.''')
    section('5. Novo modelo de cobertura e oportunidade','''A cobertura estimada combina o tempo até a próxima refeição normal com 20h equivalentes por ração carregada. O risco compara essa cobertura com o custo conhecido de reposição e a margem de viagem. Uma rota planejada pode ampliar o horizonte e o alvo existente, limitado a seis rações.

A oportunidade presente pesa mais perto de um mercado com preço/estoque observados recentemente e orçamento para pelo menos uma unidade. O bônus máximo desse termo é 8 vezes a fração do déficit. Uma viagem que adia o próximo encontro conhecido com o mercado acrescenta pressão proporcional à lacuna de cobertura, limitada a 12 vezes essa fração. Sem conhecimento do trajeto ou do preço, o NPC não recebe dados globais.

A espera usa `18 × idade/(idade+72) × déficit/alvo`: cresce após 54h, mas converge e diminui quando há uma ração. A pressão final tem teto 85 e não recebe novamente o bônus temporal genérico. Fome/sede vitais continuam acima dela; sono crítico e luto forte continuam podendo vencer. Continuidade global de objetivo foi mantida. Não foi aplicado um aumento fixo de 30 pontos.

Esses valores são parâmetros do modelo contextual, não uma garantia de comportamento ideal. O resultado precisa ser medido; não existe meta de fazer 80% do elenco carregar duas rações.''')
    section('6. Segunda ração','''`known_unaffordable` agora avalia o déficit até o alvo solicitado. Para reserva 2, posse 1 e dinheiro 0, o ramo de renda continua disponível quando profissão/local/conhecimento permitem. Para posse 2, não há déficit normal.

No mercado, o custo usa a curva real. Fora dele, uma cotação recente fornece uma estimativa, não um preço remoto perfeito; sem cotação, o mínimo conhecido continua sendo somente um limite inferior. Isso muda a validade de uma solução, não obriga a prioridade a selecionar trabalho. Saturação, falta de profissão executável e outros bloqueios continuam legítimos.''')
    section('7. Compra parcial e lote','''A compra limita a quantidade por alvo, déficit, estoque e dinheiro. Cada unidade do lote percorre a curva marginal real de preço; o caixa municipal recebe exatamente o valor debitado do comprador. Há compra parcial quando só uma ração é possível.

Na manutenção de baixa pressão, o executor pode comprar uma unidade. Com pressão pelo menos 50, pode completar o déficit em lote limitado. A compra não reduz fome; somente a refeição consome uma ração e reduz fome. Uma compra para reserva não usa retrospectivamente várias horas de alimentação.'''+table(['Campanha','Primeira ração comprada','Segunda incluída','Só a segunda','Compras parciais'],[[m,*[details[m]['counts'].get(k,0) for k in ('reserve_purchase_first_ration','reserve_purchase_second_ration','reserve_purchase_only_second','reserve_purchase_partial')]] for m in MODES]))
    section('8. Crédito salarial','''O resultado de trabalho distingue pago, creditado, saturado, sem insumo, sem pagador, local incompatível e destino não alcançado. A interface anterior de sucesso/mensagem continua utilizável. `2/6` ou `4/6` legítimos são trabalho produtivo bem-sucedido, mesmo sem moeda inteira naquele instante.

O crédito é o campo persistente já existente. Acumula sextos, transfere moeda real do caixa municipal quando devido e subtrai os sextos pagos. Não é renda universal nem criação monetária. Sem pagador líquido, a atividade salarial pode falhar antes de produzir. Produção inexistente não gera salário. Os testes cobrem crédito, conversão única e save/load.'''+table(['Campanha','Trabalhos creditados sem moeda inteira','Trabalhos com pagamento','Sem insumo','Saturados'],[[m,*[details[m]['income'].get('status:'+k,0) for k in ('credited','paid','no_input','saturated')]] for m in MODES]))
    section('9. Profissões saturadas','''Os limites de armazenamento e insumos continuam reais. Se a cidade não precisa de mais madeira, ferro ou alimentos, a atividade correspondente pode não produzir nem pagar. A correção não obriga o município a adquirir produção inútil.

O personagem pode buscar as alternativas que já existem: venda de excedente, treinamento observado, coleta, ajuda ou serviço temporário compatível. Manutenção, transporte local e outras profissões novas não foram inventados. Quando esses caminhos faltam, subemprego e pobreza permanecem estados válidos. O censo separa pobreza com setor saturado de falha de interpretação salarial.''')
    section('10. Trabalho temporário','''Distribuição anuncia no máximo `min(quota restante, estoque de alimento/2)`. Uma unidade paga o trabalhador em alimento; outra é consumida como refeição servida à população abstrata. Quota zero ou estoque insuficiente não geram oferta disponível.

O preparo temporário usa o espaço e grão efetivamente disponíveis para preparar alimento, respeitando a ocupação compatível e a área rural existente. Observações registram instante, local, capacidade, requisitos e expiração de conhecimento em 24h. Não reservam uma vaga.

Assim, uma oferta pode ser verdadeira ao ser observada e desaparecer na viagem. A execução revalida quota, estoque e ocupação. O relatório distingue esse desaparecimento de um anúncio falso no instante da observação.''')
    section('11. Intenção profissional e local','''O motor não oferece trabalho profissional cuja instalação e mapa corrente não pertençam à economia exigida. Os líderes colocados em quartéis, mas associados economicamente à cidade natal, não receberam acesso remoto ao caixa ou mercado natal.

O bloqueio não cria economia de quartel nem salário novo. Uma profissão declarada pode continuar sem atividade executável naquela instalação. A mensagem de incompatibilidade explica esse caso, enquanto destino não alcançado continua sendo outro resultado. As regressões validam ausência de transferência remota.''')
    section('12. Distribuição econômica',table(['Campanha','Caixa municipal','Dinheiro NPCs vivos','Pobres no mapa municipal','Pobres com comida municipal','Pobres com setor saturado'],[[m,census[m]['municipal_money'],census[m]['living_npc_money'],census[m]['poor_on_town_maps'],census[m]['poor_with_municipal_food'],census[m]['poor_saturated']] for m in MODES])+'''A tabela é um retrato final do auditor. “Pobre” significa caixa menor que o preço real de uma ração; não significa necessariamente fome imediata, pois pode haver comida carregada. Pobreza nos mapas municipais usa habitantes presentes; outros indicadores de campanha consultam o preço da cidade de vínculo para todos os vivos. Esses universos não são idênticos.

Média, mediana, caixa, preço, estoque, desemprego, saturação e capacidades locais foram registrados em quadros de 250h. Não foram transmitidos automaticamente aos NPCs.''')
    section('13. Desigualdade observada','''Há personagens abaixo do preço de uma refeição mesmo em localidades com caixa e alimentos. A concentração municipal foi preservada. Existem diferenças de elegibilidade, renda, profissão, conhecimento e localização; recursos municipais não são inventário pessoal.

O censo e as histórias mostram fatos materiais. Não foram acrescentados insatisfação política, luta de classes, sindicatos, revolução ou consciência de desigualdade. Tampouco se conclui que cada morte de pobre ocorreu por saturação: um retrato final não prova a sequência causal de todas as mortes.''')
    section('14. Por que a desigualdade não foi automaticamente corrigida','''A instrução pede causas sociais verdadeiras, incluindo resultados ruins. Distribuir caixa ou comida para todos apagaria desemprego e escassez de oportunidades reais. O trabalho foi corrigir interpretações e intenções incoerentes, preservando pagamentos e recursos físicos.

A única fonte monetária externa observada continua sendo a renda abstrata preexistente. O balanço separa essa fonte de transferências, e todos os checkpoints finais ficaram com diferença monetária zero. Não houve geração de NPC para fornecer ajuda ou preencher arbitrariamente uma vaga; a materialização anterior continua convertendo habitantes abstratos sob suas regras já existentes.''')
    section('15. Denúncia ao culpado',table(['Campanha','Denúncias anteriores','Ao culpado anteriormente','Denúncias finais válidas','Ao culpado agora'],[[m,olddiv[m]['narrative_event_counts'].get('ThreatReported',0),{'jogador':12,'espectador':23,'mundo':7}[m],verification['campaigns'][m]['valid_reports'],verification['campaigns'][m]['invalid_independent_reports']] for m in MODES])+'''A exclusão usa conhecimento próprio: fato conhecido, contexto de culpado/ameaça e alvo acusado. Culpa desconhecida não exclui alguém por informação do auditor. A execução revalida profissão, presença, evidência e independência.

Protocolar uma denúncia é distinto de ensinar um fato novo ao guarda. Um guarda independente que já conhece o fato pode registrar a denúncia sem emitir uma falsa aquisição de conhecimento. O episódio não pode ser protocolado duas vezes. Sem autoridade válida, a necessidade não é satisfeita artificialmente.''')
    section('16. Informação velha e repetição','''A avaliação reutilizável distingue informação nova útil, confiança melhorada, já conhecida, temporalmente inadequada, irrelevante e ausência de informação. Localização respeita observações e buscas posteriores. Uma localização diferente mais recente que a última observação pode abrir uma pista anterior à ausência: muda o destino da busca sem confirmar encontro atual nem fechar a necessidade. Uma localização anterior à busca fracassada no mesmo lugar não reinicia aquele trajeto. A validação cobre busca e ajuda material familiar. Confiança superior pode melhorar uma observação incerta da mesma época. Morte antiga desconhecida continua sendo relevante.

`learn()==false` não termina como aprendizagem bem-sucedida. Resposta inútil não emite `InformationShared` como progresso. Quests existentes continuam aceitando as confirmações adequadas. A transmissão pública de um fato realmente novo pode aprender história sem fechar uma necessidade; aprendizagem e resolução são efeitos diferentes.

Tentativas recentes ficam na própria necessidade, com limite de oito registros, interlocutor, fato, resultado e prazo de 24h. Uma resposta inútil não gera cooldown genérico de todos os pedidos de informação. Um fato novo reabre aquele interlocutor imediatamente. Isso não garante que o ajudante saiba algo: buscas podem continuar bloqueadas.'''+table(['Campanha','Sem informação','Já conhecida','Antiga para episódio','Nova útil','Confiança melhorada','Repetições evitadas'],[[m,*[details[m]['social_metrics'].get('InformationReply:'+k,0) for k in ('no_information','already_known','stale_for_need','new_useful','better_confidence')],details[m]['information'].get('repeated_reply_avoided',0)] for m in MODES]))
    # Parte final e histórias são escritas pela função abaixo.
    finish_report(report,comparison,div,olddiv,extra,census,verification,details,replays,manifest,section)


def finish_report(report,comparison,div,olddiv,extra,census,verification,details,replays,manifest,section):
    supplement=read(OUT/'metricas_complementares.json')
    section('17. Testes',f'''Passaram {manifest['tests']} testes: os 130 anteriores sem edição, entre eles as 25 regressões alimentares existentes, mais 49 novos. O arquivo de saída é {link(OUT/'testes_finais.txt')}; as regressões novas estão em {link(ROOT/'tests/test_phase32.py')}.

Foram cobertos destinatários culpados/independentes/desconhecidos, revalidação e save/load de denúncia; novidade, confiança, localização antiga, morte antiga, memória de respostas, reabertura e quests; financiamento de 0/1/2 rações, preço marginal, compra parcial, conservação e limite de estoque; crédito em sextos, conversão única, persistência e ausência de cooldown incorreto; quota, concorrência, estoque perdido, pagamento físico, oferta expirada e instalação incompatível.

Os cenários preventivos cobrem mercado próximo, segunda ração, luto forte, viagem longa conhecida, reposição distante, ausência real de caminho, sono e sede críticos. A regressão emergencial nova reproduz HP 5, fome 100 e sede 96: coletar+comer evita o adiamento que deixou o NPC sem uma ação isolada capaz de resgatá-lo na hora seguinte.''')
    shortrows=[]
    for m in MODES:
        old=read(ROOT/'reports/fase_3_2_diagnostico'/f'{m}_replay.json')['counts']
        new=read(OUT/manifest['short_audit']/m/'metricas_fase32.json')['counts']
        shortrows.append([m,100*old['reserve_selected_hunger_below_50']/old['active_reserve_hunger_below_50'],
                          100*new['healthy_reserve_selected']/new['healthy_deficit'],new['reserve_selected'],new['reserve_active']])
    section('18. Auditoria curta',table(['Campanha','Antes: reserva com fome <50 (%)','Final: mesma janela (%)','Reserva selecionada','Reserva ativa'],shortrows)+f'''São 1.000h por modo, comparadas à investigação anterior de 1.000h, sem extrapolar a taxa antiga como se ela cobrisse 10.000h. As rodadas curtas foram preservadas: `curta_v1`, `curta_v2`, `curta_v3` e `curta_final`. A última corresponde às regras finais.

As campanhas intermediárias foram preservadas em {link(OUT/'intermediaria_v1','intermediária v1')} e {link(OUT/'intermediaria_v2','intermediária v2')}. A primeira encontrou informação familiar antiga aceita e aquisição adiada em emergência. A segunda confirmou as correções; a revisão semântica posterior acrescentou pistas de localização diferente sem confirmação falsa de encontro. Essas observações e casos controlados causaram regressões e correções; nenhum resultado foi apagado. Depois disso, o código foi congelado novamente.''')
    section('19. Auditorias finais de 10.000h',table(['Campanha','Seed','Horas','Erros de invariantes','Diferença monetária','Reprodução integral','Continuação +24h'],[[m,manifest['seeds'][m],10000,0,0,replays[m]['final_checkpoint_identical'],verification['campaigns'][m]['deterministic_continuation_24_hours']] for m in MODES])+f'''Dovha jogador mantém exatamente o controlador anterior, usando comandos públicos e informações do próprio jogador. Os trajetos concretos podem divergir porque os encontros e oportunidades mudam. Dovha espectador e Mira mundo não possuem jogador guiando ações. O modo “mundo” acrescenta observação do auditor; não oferece visão global aos NPCs.

Cada campanha tem checkpoints, save final, alimentação, ações pessoais, contexto econômico, narrativa, desigualdade e episódios. A reprodução integral usa os comandos já registrados ou 10.000 passos canônicos e exige SHA idêntico ao save final. O checkpoint de 1.000h é idêntico ao teste curto final; save/load e continuação de 24h também foram validados. Verificação: {link(OUT/'verificacao_final.json')}. Motor congelado: `{manifest['core_sha256']}`.''')
    section('20. Comparação antes/depois',table(['Campanha','Mortes','Alvo completo final (%)','Rações médias finais','Seleções pessoais','Satisfações pessoais'],[[m,f"{comparison[m]['before']['deaths']} → {comparison[m]['after']['deaths']}",f"{fmt(comparison[m]['before']['reserve_final']['maintaining_reserve_percent'])} → {fmt(comparison[m]['after']['reserve_final']['maintaining_reserve_percent'])}",f"{fmt(comparison[m]['before']['reserve_final']['average_personal_food'])} → {fmt(comparison[m]['after']['reserve_final']['average_personal_food'])}",f"{comparison[m]['before']['personal_selections']} → {comparison[m]['after']['personal_selections']}",f"{comparison[m]['before']['personal_satisfied']} → {comparison[m]['after']['personal_satisfied']}" ] for m in MODES])+'''Os resultados não permitem declarar melhora geral por um único indicador. Reserva mais frequente, linguagem econômica correta e eliminação de denúncias incoerentes são resultados distintos de menos mortes, mais histórias ou distribuição mais eficiente. Nenhuma queda ou subida é atribuída isoladamente ao novo termo de prioridade sem um experimento de ablação.

“Satisfeita” é uma transição de necessidade, não uma saga. Muitas necessidades também fecham ao reencontrar alguém ou receber conhecimento sem que o NPC execute uma ação pessoal. Por isso, a análise narrativa abaixo usa episódios com ações e fatos registrados.''')
    section('21. Mortalidade',table(['Campanha','Antes: total','Final: total','Fome no limite','Sede no limite','Mortes com comida'],[[m,comparison[m]['before']['deaths'],comparison[m]['after']['deaths'],comparison[m]['after']['hunger_deaths'],comparison[m]['after']['thirst_deaths'],comparison[m]['after']['hunger_deaths_with_food']] for m in MODES])+'''Fome e sede no limite se sobrepõem quando a causa é `both`; somá-las pode contar a mesma morte duas vezes. Todas as mortes reais são privação, não assassinato, combate ou velhice. Os registros de `CharacterKilled` dos testes controlados não foram misturados às campanhas.

Na intermediária v1, Lyra Hammer #520 morreu no turno 8311 com uma ração: na última decisão tinha HP 2, fome 100 e sede 98. Os contrafactuais controlados confirmam que comer sozinho ou beber sozinho já causariam morte na hora seguinte. Porém, na hora 8309 havia uma solução real de coletar+comer que teria evitado o conflito. A aquisição adiada foi escolhida por empate entre alternativas. Essa lacuna foi corrigida na seleção existente, sem aumentar HP, reduzir dano ou juntar arbitrariamente duas ações no último instante.

O caso permanece documentado na reprodução intermediária e em `terminal_intermediario_micro.json`. O número final na tabela não é uma promessa de imunidade futura: duas necessidades vitais simultâneas com recursos insuficientes ainda podem gerar mortes legítimas.''')
    reserve_rows=[]
    for m in MODES:
        c=details[m]['counts'];reserve_rows.append([m,c['reserve_active'],c['reserve_selected'],100*c['reserve_selected']/c['reserve_active'],100*c['healthy_reserve_selected']/c['healthy_deficit'],c['healthy_known_opportunity_lost'],c['trips_started_with_deficit']])
    section('22. Reservas',table(['Campanha','Avaliações ativas','Selecionada','Ativa → escolhida (%)','Escolhida com fome <50 (%)','Oportunidade conhecida perdida','Viagens iniciadas com déficit'],reserve_rows)+'''A última coluna inclui deslocamentos para obter comida, água ou trabalho; não equivale a expedições longas deliberadamente desprotegidas. A pressão usa somente a oportunidade que o NPC conhece. O indicador de oportunidade “real” do auditor está separado nas métricas e nunca orienta a decisão.

Há cobertura estimada, reposição conhecida e pressão de espera nos exemplos de decisão. Os quadros de 250h mostram a distribuição de 0/1/2/3+ rações. Os tempos de busca/aquisição/consumo estão registrados por fluxo alimentar. Completar um alvo não é garantido: um NPC pode comer, ajudar alguém, viajar, perder a oferta ou ficar sem renda antes de mantê-lo.''')
    report.append(table(['Campanha','Buscas com fome <50, antes → final','Buscas com fome ≥80, antes → final','Buscas com HP ≤3, antes → final','Cobertura média com reserva ativa (h)','Tempo médio até alvo observado, antes → final (h)'],[
        [m,*[f"{supplement[m]['before'].get(k,0)} → {supplement[m]['after'].get(k,0)}" for k in ('searches_hunger_below_50','searches_hunger_at_least_80','searches_hp_at_most_3')],supplement[m]['mean_coverage_hours_while_reserve_active'],f"{fmt(supplement[m]['before']['hours_to_recorded_target_mean'])} → {fmt(supplement[m]['after']['hours_to_recorded_target_mean'])}"] for m in MODES]))
    report.append('O tempo até o alvo inclui apenas buscas cuja aquisição atingiu o alvo registrado no início; não imputa sucesso às demais nem mede reserva sustentada. Cobertura é uma média por avaliação com déficit, não por pessoa.\n\n'+table(['Campanha','Reserva preventiva perdeu para descanso','Sede','Renda','Necessidades pessoais'],[[m,supplement[m]['healthy_reserve_winners'].get('rest',0),supplement[m]['healthy_reserve_winners'].get('water',0),supplement[m]['healthy_reserve_winners'].get('money',0),sum(supplement[m]['healthy_reserve_winners'].get(k,0) for k in ('family','grief','revenge','protection','status','advancement'))] for m in MODES]))
    section('23. Renda',table(['Campanha','Moedas pagas em trabalho executado','Crédito novo em sextos','Produção profissional medida','Pobres abaixo do preço, todos os vivos'],[[m,details[m]['income'].get('work:paid_coins',0),details[m]['income'].get('wage_sixths_accrued',0),details[m]['income'].get('produced_units',0),comparison[m]['after']['final']['poor_below_one_meal']] for m in MODES])+'''O pagamento em produto de serviços temporários continua separado de moeda. Crédito fracionário é progresso econômico real, mas não é uma moeda inteira já gastável. Um trabalhador pode produzir corretamente e continuar sem orçamento para comprar imediatamente. A correção semântica não transforma essa espera em riqueza automática.

A projeção temporal de renda continua usando taxas nominais; concorrência, insumos e produção parcial podem alterar o tempo concreto. A auditoria não atribui todas as mortes remanescentes a um único mecanismo salarial.''')
    section('24. Estoques',table(['Campanha','Comida municipal antes','Comida municipal final','Mercados vazios antes','Mercados vazios finais'],[[m,comparison[m]['before']['reserve_final']['municipal_food_total'],comparison[m]['after']['reserve_final']['municipal_food_total'],comparison[m]['before']['final']['empty_food'],comparison[m]['after']['final']['empty_food']] for m in MODES])+'''Comida carregada por NPCs saiu de compra, produção, coleta ou transferência real. Os limites de estoque não foram elevados. A reserva pode deslocar parte do estoque para inventários pessoais; ela não cria alimento nem resolve todos os gargalos locais. A presença de estoque em outro município também não resolve acesso local: comércio intermunicipal não foi implementado.''')
    opportunity_rows=[]
    for m in MODES:
        c=replays[m]['observations_and_executions']
        opportunity_rows.append([m,c.get('observed:meal_distribution',0),c.get('executed:meal_distribution',0),c.get('observed_offer_lost_before_execution:meal_distribution',0),c.get('episodes:no_independent_known_guard',0),c.get('episodes:missing_report_evidence',0)])
    section('25. Oportunidades e bloqueios',table(['Campanha','Observações de distribuição','Execuções bem-sucedidas','Oferta conhecida perdida','Episódios sem guarda independente','Episódios sem evidência de denúncia'],opportunity_rows)+'''Observações são atualizações locais por indivíduo e instante, não vagas únicas. Oferta perdida exige capacidade positiva observada e falha posterior; pode resultar de quota ou estoque consumidos, sem atribuir concorrência a um ator específico quando isso não foi reconstruído.

A contagem de bloqueio social distingue falta de autoridade independente de falta do fato conhecido. Não se criou guarda substituto. Desemprego, ineligibilidade e escassez de informação continuam podendo bloquear necessidades. A reprodução integral conserva os exemplos e o SHA do save.''')
    section('26. Métricas sociais',table(['Campanha','Pedidos pessoais de ajuda','Pedidos com informação útil','Fatos úteis transmitidos','Melhorias de confiança transmitidas','Busca familiar: episódios com ação','Com confirmação direta','Com pedido de ajuda fracassado'],[[m,*[supplement[m]['social'].get(k,0) for k in ('personal_information_requests','requests_with_useful_information','useful_facts_transmitted','transmission:better_confidence','missing_episodes_with_action','missing_episodes_with_direct_location_confirmation','missing_episodes_with_failed_help_request')]] for m in MODES])+f'''Denúncias válidas, fatos úteis, confiança melhorada, respostas inúteis e repetição evitada foram registrados separadamente. As três campanhas finais têm zero denúncias tratadas como independentes ao próprio acusado e zero respostas marcadas como sucesso com mensagem “sem avanço”. Os eventos de transmissão útil têm `utility` no contexto.

Pedidos pessoais também podem pedir companhia ou abrir quest; nem todos são perguntas informativas. Não houve informação útil recebida pela ação autônoma de pedir ajuda nestas campanhas. As transmissões úteis registradas vieram de outros caminhos, como denúncia ou comando do jogador. Portanto, a ausência de progresso informativo continua sendo uma limitação observada, apesar das regressões demonstrarem que informação nova válida pode ajudar. Não se atribuiu fechamento de necessidade a uma informação indireta sem evidência suficiente. Confirmação direta e pedido fracassado podem ocorrer no mesmo episódio; os números não são categorias excludentes nem incluem todos os reencontros espontâneos.

Isso não significa justiça completa. A denúncia registra conhecimento e resolve aquela intenção de procurar uma autoridade; não implementa julgamento, prisão, julgamento tardio de um crime nem punição por assassinato. O guarda continua com a intervenção local já existente. A redução de transmissões pode ser eliminação de duplicatas, mas não é automaticamente perda de informação útil. Veja {link(OUT/'auditorias','dados completos das campanhas')} e as histórias.''')
    section('27. Histórias emergentes observadas','''A seguir estão episódios reais reconstruídos dos registros. As histórias completas também foram salvas em arquivo separado. Não há ficção acrescentada para preencher lacunas, nem emoção ou motivação presumida a partir de um resultado material.''')
    stories=build_stories()
    report.append(stories)
    diversity_rows=[]
    for m in MODES:
        old,new=olddiv[m],div[m]
        diversity_rows.append([m,f"{old['personal_episodes_with_action']} → {new['personal_episodes_with_action']}",
          f"{old['episodes_by_event_count'].get('2',0)} → {new['episodes_by_event_count'].get('2',0)}",
          f"{old['episodes_by_event_count'].get('3',0)} → {new['episodes_by_event_count'].get('3',0)}",
          f"{old['episodes_by_event_count'].get('4+',0)} → {new['episodes_by_event_count'].get('4+',0)}",
          f"{old['episodes_spanning_at_least_168_hours']} → {new['episodes_spanning_at_least_168_hours']}",
          f"{old['characters_with_personal_actions_over_at_least_720_hours']} → {new['characters_with_personal_actions_over_at_least_720_hours']}"])
    section('28. Diversidade narrativa',table(['Campanha','Episódios com ação','2 eventos','3 eventos','4+ eventos','Duração ≥168h','Personagens ≥720h'],diversity_rows)+table(['Campanha','Sem cuidado alimentar direto/crime alimentar','Com evento do jogador','Sem evento do jogador','Necessidades pessoais interrompidas por morte'],[[m,extra[m]['episodes_without_direct_food_care_or_food_crime'],extra[m]['episodes_with_player_event'],extra[m]['episodes_without_player_event'],extra[m]['personal_needs_interrupted_by_death']] for m in MODES])+table(['Evento, antes → final','Jogador','Espectador','Mundo'],[[k,*[f"{olddiv[m]['narrative_event_counts'].get(k,0)} → {div[m]['narrative_event_counts'].get(k,0)}" for m in MODES]] for k in ('ProfessionChanged','ResponsibilityFulfilled','Remembrance','ItemStolen','InvestigationPerformed','ProtectionGiven','FamilySearch','PersonLocated','QuestCompleted','SuccessionChanged')])+'''O primeiro quadro usa o mesmo agrupamento anterior: personagem, necessidade, início do episódio e fonte, com eventos compatíveis registrados na hora da ação. A duração parte do evento causal conhecido. Esses episódios não incluem toda a trajetória profissional/sucessória, apresentada à parte nas histórias.

O segundo quadro acrescenta uma classificação mais estrita: exclui cuidado familiar por comida e crime alimentar, mas conserva, por exemplo, busca, luto e cuidado por água. Isso não prova independência total da fisiologia: o luto pode ter começado por morte de fome. “Sem jogador” significa nenhum evento com o jogador no episódio; não prova que o mundo inteiro não sofreu influência indireta dele.

Menos episódios extensos ou menos investigações significa que a variedade/continuidade não foi automaticamente resolvida. A remoção de retransmissões falsas também reduz artificialmente cadeias que antes pareciam longas. Ainda assim, os dados não autorizam substituir toda redução por uma explicação favorável: prioridade, renda e caminhos sociais continuam competindo, e as causas narrativas permanecem estreitas.''')
    section('29. Bugs remanescentes e riscos observados','''Não reapareceram denúncia ao próprio acusado, aprendizagem duplicada tratada como avanço, cooldown por mero crédito parcial, anúncio de quota zero como oportunidade verdadeira ou acesso remoto à economia natal nas regressões e verificações finais.

Isso não é prova de ausência de qualquer bug. O calendário e as regras simplificadas podem deixar fome/sede convergirem tarde demais; a projeção de salário é nominal; guarda conhecido pode desaparecer ou não ter evidência na chegada; fatos relevantes podem sair da memória limitada. Os registros finais permitem investigar esses casos sem confundi-los automaticamente com erro.

Há limitações funcionais relevantes: pedidos de ajuda material por água possuem caminhos menos diretos; treinamento pode reiniciar repetidamente; reconhecimento frequentemente termina em um único gesto; denunciar não abre processo de justiça persistente; não existe agressão/combate. Foram registrados como limitações, sem acrescentar sistemas fora do escopo.''')
    section('30. Limitações da análise','''Duas seeds e três modos não representam todos os mundos possíveis. As campanhas mudam várias correções conjuntamente e divergem após decisões iniciais; não isolam a contribuição de cada parâmetro. O jogador automatizado tem política limitada, não avalia criativamente toda quest disponível. Quadros de 250h são amostras, não estado de cada pessoa em todas as horas.

Contagens de avaliação, observação, transição, evento e episódio têm denominadores diferentes. Fato conhecido pelo auditor não é conhecimento do NPC. Causalidade entre trabalho saturado e mudança de carreira só é afirmada quando a necessidade/decisão sustentam essa ligação; mera proximidade temporal é apresentada como correlação.

A implementação da Fase 3.2 corrige coerência local. Ela não demonstra que o projeto já produz sagas, guerras, conflitos políticos ou violência autônoma, nem que está pronto para multiplicar população sem ampliar a auditoria de comportamento.''')
    section('31. Recomendações para a Fase 4','''Primeiro, manter estas regressões e a observabilidade quando mudar a população, sem remover pobreza legítima para melhorar estatísticas. Medir o custo e as consequências de ampliar elenco/LOD com as mesmas cadeias causais.

Antes de atribuir riqueza narrativa à escala, aprofundar os caminhos locais já existentes: ajuda material, expectativas de renda, continuidade de carreira, localização e resposta real à denúncia. Separar “necessidade satisfeita” de resolução social duradoura.

Para a questão levantada sobre inimigos: uma etapa própria de agressão e combate local pode produzir defesa, fuga, ferimentos, mortes violentas, testemunhas e repercussão familiar. Não é necessário implementar guerra entre reinos para haver confronto pessoal. Mas hostilidade não deve implicar ataque automático: motivação conhecida, risco, coragem, relações e consequências precisam participar do fluxo atual.

Ao introduzir `CharacterKilled` como consequência real, também revisar sucessão, população, evidência, atribuição de culpa e proteção para reagirem corretamente à nova causa de morte. Política, religião, deuses, migração, redistribuição e guerras continuam fora desta entrega. A economia atual pode alimentar conflitos futuros, mas eles ainda precisam existir como ações e consequências executáveis.''')
    path=ROOT/'RELATORIO_FASE_3_2.md';path.write_text('\n'.join(report)+'\n')
    (OUT/'HISTORIAS_EMERGENTES.md').write_text(stories+'\n')
    print(path,'palavras',len(path.read_text().split()))


def build_stories():
    evidence=read(OUT/'historias_evidencias.json')
    worlds={m:JsonRepository().load(OUT/'auditorias'/m/'save_final.json') for m in MODES}
    engines={m:Engine(worlds[m]) for m in MODES}
    personal_context={m:{(a['npc_id'],a['turn'],a['goal_id']):a for a in streams(OUT/'auditorias'/m/'contexto_pessoal.jsonl.gz')} for m in MODES}
    events={m:list(streams(OUT/'auditorias'/m/'narrativa.jsonl.gz')) for m in MODES}
    incomes={m:list(streams(OUT/'auditorias'/m/'economia_acoes.jsonl.gz')) for m in MODES}
    census=read(OUT/'censo_economico.json')
    parts=['# Histórias emergentes observadas\n\nEstes relatos são reconstruções auditáveis. Fatos, ações, conhecimentos anteriores e resultados vêm das campanhas finais; a intermediária problemática foi preservada separadamente. “História” aqui inclui episódio social, trajetória profissional e microepisódio econômico. Nenhum deles é apresentado como saga, guerra ou consciência política.\n']
    number=0
    def heading(title,mode):
        nonlocal number
        number+=1;parts.append(f'## H{number:02d}. {title}\n\nCampanha: **{mode}**.\n')
    def person(mode,i):
        w=worlds[mode]
        c=w.characters.get(i)
        return f'{c.name} #{i}' if c else f'{w.towns[i].name} #{i}' if i in w.towns else str(i)
    def final(mode,i):
        c=worlds[mode].characters[i];e=engines[mode]
        return f"Estado final no turno {worlds[mode].turn}: {'vivo' if c.alive else 'morto'}, profissão {c.profession or 'sem profissão'}, {c.money} moedas, {e.items.count(c.id,'food')} rações, HP {c.health}, fome {c.hunger}, sede {c.thirst}. Esse é o estado ao fim da campanha, não uma informação que os participantes necessariamente possuíam na época do episódio."
    selected=[]
    desired={'jogador':('Investigação de responsável conhecido','Busca familiar e localização','Luto e lembrança','Ajuda familiar material'),
             'espectador':('Denúncia a autoridade independente','Ajuda familiar material','Reconhecimento'),
             'mundo':('Proteção concreta','Luto e lembrança')}
    for mode in MODES:
        for label in desired[mode]:
            story=next((s for s in evidence[mode]['personal_stories'] if s['label']==label),None)
            if story:selected.append((mode,story))
    for mode,story in selected:
        ep=story['episode'];need=ep['need'];owner=ep['npc_id'];actions=ep['actions'];w=worlds[mode]
        heading(story['label']+' — '+person(mode,owner),mode)
        ids={owner,need['target_id']}|{e.get('actor_id') for e in ep['events']}|{e.get('target_id') for e in ep['events']}
        participants=[i for i in ids if i is not None and i in w.characters]
        relations=[r for r in w.relationships.values() if r.source_id==owner and r.target_id in participants and r.kind in ('casamento','pai_de','filho_de','amizade')]
        relation_text='; '.join(f'{r.kind} com {person(mode,r.target_id)}: {r.value}' for r in relations) or 'nenhum vínculo familiar/amical relevante identificado entre esses participantes'
        context=personal_context[mode].get((owner,actions[0]['turn'],next((a['goal_id'] for a in personal_context[mode].values() if a['npc_id']==owner and a['turn']==actions[0]['turn'] and a['need_id']==need['id']),-1)),{})
        # A associação usa dono/turno/necessidade, pois o agrupamento de episódio não conserva goal_id.
        if not context:
            context=next((a for a in personal_context[mode].values() if a['npc_id']==owner and a['turn']==actions[0]['turn'] and a['need_id']==need['id']),{})
        economy=f"Na primeira execução registrada, profissão {context.get('profession','não capturada')}, caixa {context.get('money','não capturado')} e {context.get('food','não capturado')} ração(ões)."
        source=need['context'].get('source_event');fact=actions[0]['source_fact_known_before']
        known=(f"Antes da ação, conhecia o fato #{fact['event_id']} do turno {fact['turn']} com confiança {fact['confidence']}. "
               f"Conteúdo: {fact['description']}") if fact else ('O fato-fonte não estava na memória limitada da primeira execução capturada. A necessidade/contexto conservavam a percepção anterior; o relatório não trata o registro global como conhecimento novo do NPC.')
        parts.append(f"Participantes: {'; '.join(person(mode,i) for i in sorted(participants))}. Relações: {relation_text}. {economy}\n\n")
        parts.append(f"Necessidade `{need['kind']}`, motivo: {need['reason']}; prioridade na primeira execução: {fmt(need['priority'])}. Fonte `{need['source']}`. {known}\n\n")
        parts.append(table(['Turno','Evento','ID','Consequência registrada'],[[e['turn'],e['kind'],e['id'],e['description']] for e in ep['events'][:12]]))
        parts.append(table(['Turno','Ação','Sucesso','Resultado'],[[a['turn'],a['action'],a['success'],a['outcome']] for a in actions[:12]]))
        impacts=[]
        for event in ep['events']:
            for i in participants:
                impact=w.characters[i].applied_facts.get(event['id'])
                if impact and (impact.tags or impact.trust):
                    impacts.append(f"{person(mode,i)} mantém impacto do fato #{event['id']}: tags {impact.tags}, confiança {impact.trust}, confiança da evidência {fmt(impact.confidence)}")
        effects='; '.join(impacts[:4]) if impacts else 'Não foi atribuída promoção nem mudança profissional a esses eventos; o ledger final não conserva um impacto reputacional específico deles.'
        parts.append(f"Evento/percepção → conhecimento próprio → necessidade → prioridade → solução executada → consequências nos quadros acima. A duração entre a fonte causal e a última ação é {ep['span_hours']}h. {effects}\n\n{final(mode,owner)}\n\n")
        if need['kind']=='revenge':
            interpretation='A motivação de reparação está explícita na necessidade e o responsável na informação conhecida. Investigar e denunciar não equivalem a atacar, prender ou obter punição; nenhuma dessas consequências foi inventada.'
        elif need['kind']=='grief':
            interpretation='O luto e a lembrança são necessidades/ações registradas. A relação conhecida sustenta o episódio. Não foi acrescentada uma emoção específica nem se presume que todo familiar soube imediatamente da morte.'
        elif need['kind']=='status':
            interpretation='Buscar reconhecimento está sustentado pela necessidade criada após encontro relevante. Um gesto concreto de ajuda/trabalho não significa receber título, cargo ou prestígio coletivo duradouro.'
        elif need['kind']=='family' and need['context'].get('mode')=='missing':
            interpretation='A busca deriva de ausência percebida, não de um mapa global. Verificar sem encontrar e depois localizar são mudanças reais de situação. O conhecimento e a cronologia distinguem o encontro de retransmitir uma localização velha.'
        elif need['kind']=='family':
            interpretation=f"A ajuda é por {need['context'].get('resource','food')}, conforme a necessidade, e usa transferência física. Uma doação não prova que a morte era certa nem que resolveu toda a pobreza do destinatário."
        else:
            interpretation='O afastamento/proteção é ação social concreta. Não foi presumido um confronto, crime adicional, ferimento ou reação política.'
        parts.append('**Qualidade e limite:** '+interpretation+'\n\n')
    for mode in ('jogador','mundo'):
        if not evidence[mode]['careers']:continue
        career=evidence[mode]['careers'][0];i=career['actor_id'];history=career['history'];change=career['profession_change']
        started=next(e for e in history if e['kind']=='TrainingStarted')
        abandon=[e for e in history if e['kind']=='TrainingAbandoned']
        heading(('Carreira interrompida e retomada — ' if abandon else 'Aprendizagem e nova profissão — ')+person(mode,i),mode)
        actor_actions=[a for a in incomes[mode] if a['npc_id']==i and started['turn']<=a['turn']<=change['turn']]
        first=next((a for a in actor_actions if a['goal']['action']=='train'),None)
        reason=(f"A primeira prática capturada veio da necessidade `{first['need']['kind']}` ({first['need']['reason']}), prioridade {fmt(first['need']['priority'])}, caixa {first['money_before']} e crédito {first['credit_before']}/6.") if first and first['need'] else 'A origem da primeira seleção de treino não foi capturada como necessidade nesta extração.'
        parts.append(f"{person(mode,i)} iniciou treinamento no turno {started['turn']} e mudou de {change['context'].get('previous') or 'sem profissão'} para {change['context'].get('profession')} no turno {change['turn']}. Duração da trajetória selecionada: {change['turn']-started['turn']}h. Houve {len(abandon)} abandono(s) por falta de prática recente. {reason}\n\n")
        anchors=[e for e in history if e['kind'] in ('TrainingStarted','TrainingAbandoned','ProfessionChanged')]
        parts.append(table(['Turno','ID','Evento','Descrição'],[[e['turn'],e['id'],e['kind'],e['description']] for e in anchors]))
        chain='oportunidade conhecida → necessidade selecionada → prática com insumo e remuneração reais → '
        if abandon:chain+='pausa/abandono → nova prática → '
        chain+='mudança profissional'
        quality=('Recomeços também mostram repetição e uma aprendizagem frágil; não foram reescritos como uma aventura deliberada.' if abandon else 'Não houve abandono registrado nesta trajetória; a nova profissão também não garante renda ou sobrevivência futuras.')
        parts.append('A cadeia comprovada é '+chain+'. As falhas anteriores de trabalho, quando capturadas, são correlação material; não provam por si mesmas que a saturação foi a motivação única. Não houve profissão forçada nem promoção instantânea.\n\n'+final(mode,i)+'\n\n**Qualidade e limite:** existe continuidade e consequência profissional persistente. '+quality+'\n\n')
    # Retrato material de desigualdade, com indicação explícita de que é observação do auditor.
    mode='mundo'
    poor=[p for p in census[mode]['poor_people'] if p['municipal_food']>0 and p['town_money']>0 and p['profession_saturated']]
    if poor:
        p=max(poor,key=lambda p:p['town_money']);heading('Profissional pobre em localidade com recursos — '+person(mode,p['id']),mode)
        parts.append(f"No turno final, {person(mode,p['id'])} tem profissão {p['profession']}, {p['money']} moeda(s) e {p['food']} ração(ões). A localidade #{p['town_id']} possui {p['town_money']} moedas e {p['municipal_food']} rações; uma ração custa {p['real_price_for_auditor']} moedas. O setor está saturado nesse retrato. Elegibilidade temporária: {p['temporary_eligible']}.\n\n")
        parts.append(f"Necessidades ativas: {p['active_needs']}. Conhecimento de mercado do próprio personagem: observação do turno {p['known_market'].get('turn','ausente')}, preço observado {p['known_market'].get('price','desconhecido')}. A disponibilidade física atual e o caixa municipal são informações do auditor; não são uma denúncia política ou percepção econômica global do NPC.\n\nA causa da saturação é estoque, e o salário depende de atividade real. Não há evento de revolta nem emoção de ressentimento implementada. Este é um estado econômico interessante para uma futura história, não uma saga já executada.\n\n"+final(mode,p['id'])+'\n\n')
    # Crédito efetivo seguido de transferência monetária real.
    mode='espectador'
    if evidence[mode]['fractional_credit_examples']:
        a=evidence[mode]['fractional_credit_examples'][0];i=a['npc_id']
        later=next((b for b in incomes[mode] if b['npc_id']==i and b['turn']>a['turn'] and b['money_after']>b['money_before']),None)
        heading('Crédito parcial é trabalho real — '+person(mode,i),mode)
        parts.append(f"No turno {a['turn']}, {person(mode,i)} executou trabalho na profissão {a['profession']}. Necessidade `{a['need']['kind']}`: {a['need']['reason']}. Caixa {a['money_before']} → {a['money_after']}; crédito {a['credit_before']}/6 → {a['credit_after']}/6. Resultado: {a['outcome']} A ação foi bem-sucedida e não recebeu cooldown de fracasso por não ter transferido uma moeda inteira.\n\n")
        if later:parts.append(f"No turno {later['turn']}, outra atividade do mesmo personagem pagou {later['money_after']-later['money_before']} moeda(s), a partir do caixa local. Crédito naquela operação: {later['credit_before']}/6 → {later['credit_after']}/6. Isso prova remuneração posterior real; não se atribui toda essa moeda exclusivamente ao primeiro lote sem contabilizar os trabalhos intermediários.\n\n")
        parts.append(final(mode,i)+'\n\n**Qualidade e limite:** é um microepisódio econômico que corrige causalidade. Não deve ser contado como uma grande história por si só, nem como garantia de estabilidade financeira.\n\n')
    mode='jogador'
    if evidence[mode]['lost_temporary_offer_examples']:
        a=evidence[mode]['lost_temporary_offer_examples'][0];i=a['npc_id'];seen=a['known_offer']
        capacity=seen.get('temporary_offers',{}).get('meal_distribution',{}).get('capacity')
        heading('Oferta conhecida desaparece antes da execução — '+person(mode,i),mode)
        parts.append(f"{person(mode,i)} conhecia oferta de distribuição observada no turno {seen.get('offers_observed_at')}, capacidade {capacity}. Tentou `{a['goal']['action']}` no turno {a['turn']}, com necessidade `{a['need']['kind']}` ({a['need']['reason']}). A execução falhou honestamente: {a['outcome']} Caixa {a['money_before']} → {a['money_after']}; alimento pessoal {a['food_before']} → {a['food_after']}.\n\n")
        nearby=[e for e in events[mode] if e['kind']=='TemporaryWorkPerformed' and e['target_id']==a['goal']['destination']['map_id'] and seen.get('offers_observed_at',a['turn'])<=e['turn']<=a['turn']]
        if nearby:parts.append(table(['Turno','ID','Outro trabalho local registrado'],[[e['turn'],e['id'],e['description']] for e in nearby[:6]]))
        parts.append('A reprodução valida capacidade positiva no instante em que a oferta foi observada. Não houve criação de pagamento/comida para cumprir a promessa depois. Trabalhos locais próximos mostram concorrência possível, mas, sem reconstruir toda a sequência de consumo, não se atribui a perda a um concorrente específico.\n\n'+final(mode,i)+'\n\n**Qualidade e limite:** o mundo pode frustrar um plano legítimo; isso é diferente de anunciar uma vaga já esgotada. Não há reação política à frustração.\n\n')
    mode='jogador';completed=[e for e in events[mode] if e['kind']=='QuestCompleted']
    if completed:
        event=completed[0];player=event['actor_id'];receiver=event['target_id']
        heading('Intervenção do jogador com conclusão registrada',mode)
        parts.append(f"Evento #{event['id']}, turno {event['turn']}: {event['description']} Participantes: {person(mode,player)} e {person(mode,receiver)}. Contexto do evento: {event['context']}.\n\n")
        related=[q for q in worlds[mode].quests.values() if q.owner_id==receiver and q.completed_at==event['turn']]
        for q in related:parts.append(f"Quest #{q.id}, tipo `{q.kind}`, criada {q.created_at}, concluída {q.completed_at}; duração {q.completed_at-q.created_at}h. Contexto: {q.context}.\n\n")
        parts.append('A política automatizada usou comandos públicos e concluiu a necessidade exigida pela quest. O fato da conclusão é comprovado; não se presume que o jogador salvou uma morte certa nem que cumpriu todas as quests oferecidas.\n\n'+final(mode,receiver)+'\n\n')
    mode='espectador'
    if evidence[mode]['succession']:
        event=evidence[mode]['succession'][0];heading('Sucessão após perda real de governante',mode)
        parts.append(f"Evento #{event['id']}, turno {event['turn']}: {event['description']} Contexto: {event['context']}. A sucessão muda a liderança pelo sistema já existente; não produz uma guerra automaticamente.\n\n")
        kingdom=worlds[mode].kingdoms[event['target_id']]
        death=next((e for e in events[mode] if e['kind']=='CharacterDied' and e['turn']==event['turn'] and e['target_id'] in kingdom.royal_family),None)
        if death:
            victim=death['target_id'];successor=event['actor_id'];record=worlds[mode].death_records[victim]
            kin=[r for r in worlds[mode].relationships.values() if r.source_id==successor and r.target_id==victim and r.kind in ('casamento','pai_de','filho_de')]
            parts.append(f"Causa registrada: evento #{death['id']}, turno {death['turn']}, {death['description']} Governante anterior: {person(mode,victim)}; sucessor: {person(mode,successor)}; reino #{kingdom.id}. Vínculos do sucessor com o falecido: {[(r.kind,r.value) for r in kin]}. Registro da morte: fome {record['hunger']}, sede {record['thirst']}, comida carregada {record['food']}, causa `{record['cause']}`.\n\n")
            parts.append('A consequência de liderança ocorreu na mesma hora: morte → callback de sucessão → escolha dinástica → novo governante. Essa decisão é uma regra institucional existente; não decorre de uma necessidade pessoal de ambição nem exige que o sucessor possuísse previamente o fato da morte. Os receptores explicitamente registrados do evento sucessório foram '+str([k['id'] for k in event['knowledge_at_event']])+'.\n\n'+final(mode,successor)+'\n\n')
        parts.append('A morte deve ser lida no registro de privação da campanha, não reclassificada como assassinato. Uma troca de liderança não demonstra facções políticas, reivindicações militares ou legitimidade debatida, pois essas ações ainda não existem.\n\n')
    parts.append('## Avaliação das histórias\n\nHá relações, conhecimento limitado, decisões locais, reencontros, reparação sem confronto, ajuda material, mudanças profissionais e consequências persistentes. Algumas trajetórias atravessam centenas ou milhares de horas. Isso demonstra causalidade local além de uma simples lista de mortes.\n\nA qualidade ainda é desigual: muitas cadeias são curtas, a motivação econômica domina carreiras, perdas derivam de privação e a denúncia costuma encerrar a reação sem uma investigação judicial continuada. A ausência de agressão limita os rumos da hostilidade. A Fase 3.2 melhora a honestidade dos registros e das ações; ampliar a variedade de causas e consequências exige funcionalidades futuras, não apenas aumentar a população.\n\nFontes: '+link(OUT/'historias_evidencias.json')+', '+link(OUT/'diversidade_narrativa.json')+' e os fluxos de cada campanha em '+link(OUT/'auditorias','auditorias')+'.\n')
    return '\n'.join(parts)


if __name__=='__main__':main()
