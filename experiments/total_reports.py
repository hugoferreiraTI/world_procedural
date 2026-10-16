"""Documentação da auditoria; lê fontes/evidências, sem executar decisões."""
import ast
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

from .total_static import ROOT, OUT, Inventory, table, fingerprint, TRAITS

def read(name):
    return json.loads((OUT/name).read_text())

def write(name,text):
    if name.endswith('.md'):
        for report in ('RADIOGRAFIA_TOTAL.md','MAPA_CODIGO.md','DECISOES_REAIS.md','OBSERVABILIDADE.md'):
            text=text.replace(']('+report+')','](<'+str(OUT/report)+'>)')
        if name!='DECISOES_REAIS.md':
            headings=re.findall(r'^## (.+)$',text,re.M)
            def slug(s):return re.sub(r'\s','-',re.sub(r'[^\w\s-]','',s.lower()))
            toc='## Índice\n\n'+'\n'.join('- ['+h+'](#'+slug(h)+')' for h in headings)+'\n\n'
            first=text.find('\n\n')+2
            text=text[:first]+toc+text[first:]
    (OUT/name).write_text(text,encoding='utf-8')

def link(symbol,inv):
    f=next((f for f in inv['functions'] if f['symbol']==symbol),None)
    if not f:return '`'+symbol+'`'
    return f"[{symbol}](<{ROOT}/procedural/{f['module']}.py:{f['line']}>)"

def source(symbol,inv):
    f=next((f for f in inv['functions'] if f['symbol']==symbol),None)
    if not f:return ''
    lines=(ROOT/'procedural'/f"{f['module']}.py").read_text().splitlines()
    return f"### {symbol}\n\nFonte: {link(symbol,inv)}.\n\n```python\n"+'\n'.join(lines[f['line']-1:f['end_line']])+"\n```\n\n"

# A classificação é por capacidade explicativa do registro padrão, não pelo
# número de chamadas, nem pela presença de um teste com o nome do sistema.
SYSTEMS=[
 ('__init__','Versões','A','Completo','Constantes de regras/geração no agregado; não migra formatos anteriores.'),
 ('__main__','Entrada CLI','B','Completo','Argumentos/ações do usuário não formam um histórico completo de comandos no save.'),
 ('access','Acesso, contato, pactos, POIs, adesão','B','Parcial','Estados e eventos de êxito existem; alternativas omitidas e todos os motivos de silêncio não são históricos.'),
 ('action_pressure','Pressão/capacidade para agir','B','Parcial','Últimos registros e transições de faixa; não preserva cada cálculo nem cada recusa.'),
 ('aftermath','Reação do autor à morte','B','Completo no ciclo existente','Appraisal e death_record explicam mortes retidas; feedback e decaimento não têm série completa.'),
 ('agency','Compromissos e aspirações','B','Parcial','Continuidade persistida, limites e diagnósticos; alternativas e estados anteriores exigem observador.'),
 ('collective_action','Agência de grupo/facção/deus','B','Parcial','Pressão e avaliações seletivas; capacidade booleana não equivale a serviço institucional completo.'),
 ('conflicts','Conflito, dano, ajuda e reação','B','Parcial','Eventos de ataques/reação; candidatos, vínculos e risco exatos a cada escolha não ficam todos registrados.'),
 ('divine_relations','Conhecimento e afinidade dos deuses','B','Parcial','Mensagens, fontes e afinidades limitadas; censos objetivos não são o conhecimento do deus.'),
 ('economy','Mercado, tesouros e economia diária','B','Parcial','Saldos e relatórios recentes; não há razão contábil imutável de cada unidade e preço histórico.'),
 ('emotions','Emoções, agravos e adaptação','C','Parcial','Estado atual e fontes compactas; a trajetória completa dos sentimentos e seus insumos históricos foi perdida.'),
 ('engine','Coordenação, comandos e morte','B','Completo no fluxo atual','Ordem e registro da morte existem; decisões anteriores não são integralmente persistidas.'),
 ('events','Bus, Recorder e índice espacial','B','Parcial','Histórico seletivo, buffer de 256 e contexto mutável; ordem completa e proveniência não são garantidas após retenção.'),
 ('faith','Crença, ritos, deuses e ascensão','B','Parcial','Eventos de ritos/efeitos e estado divino; ausência de audiência não fornece todos os gates históricos.'),
 ('feeding','Alimentação, prazo biológico e reserva','B','Parcial','Estimativas/diagnósticos recentes; candidatos descartados e substituição preventiva requerem captura externa.'),
 ('generation','Geração determinística','B','Completo no gerador atual','Seed+versão+config permitem refazer geração, mas config completa não é campo geral do save; auditoria a preserva.'),
 ('geography','Rotas, conhecimento e Journey','B','Parcial','Rota objetiva, conhecimento pessoal, Journey e eventos; todo caminho rejeitado e estado anterior não são retidos.'),
 ('goals','Seleção, Utility e execução','C','Completo no mecanismo atual','Goal final e métricas não explicam o leilão completo; debug e solutions não são consultas universalmente puras.'),
 ('institutions','Propostas, políticas, facções e legalidade','B','Parcial','Scores de decisões, orçamento e histórico limitado; conhecimento dos trabalhadores e candidaturas não são históricos completos.'),
 ('investigation','Busca, pistas e autoria','B','Parcial','Pistas/estado de busca e eventos; ausência de pista e competição de Needs dependem de trace externo.'),
 ('items','Itens, transferência e consumo','B','Parcial','Dono atual, origem e história seletiva; stack ordinário consumido não tem trajetória unitária completa.'),
 ('justice','Crime conhecido, wanted e captura','B','Parcial','Caso/evidência/local/confiança; não se pode inferir conhecimento de todo guarda pela ocorrência objetiva.'),
 ('lethal_decisions','Motivo letal persistente e terminal','B','Completo no ciclo existente','Decisão/cálculos selecionados e eventos; gates não emitidos em todas as consultas precisam do observador.'),
 ('lethality','Pressão letal e compatibilidade','B','Parcial','Retorna avaliação e emite auditorias seletivas; uma chamada sem audit não vira histórico.'),
 ('migration','Mudança física de residência','B','Parcial','Estado e eventos de destino/chegada; trajetórias bloqueadas não são reconstruíveis universalmente.'),
 ('models','Estado tipado','A','Completo como esquema','Campos atuais são inspecionáveis; esquema não representa histórico de cada alteração.'),
 ('navigation','Movimento local e passagem de mapas','C','Parcial','Posição final não reconstrói todo passo nem o caminho bloqueado.'),
 ('needs','Fisiologia, prioridades e lifecycle','C','Completo no mecanismo atual','Estado final é sobrescrito/reutilizado; todas as prioridades de cada hora não são persistidas.'),
 ('knowledge','Percepção, Facts, memória e rumores','B','Parcial','Fonte/confiança e memória limitada; receipts históricos integrais e visão passada exigem observador.'),
 ('personal','Necessidades pessoais e percepção','B','Parcial','Fatos/fontes e observações limitadas; causas esquecidas podem perder o vínculo original.'),
 ('personal_actions','Ajuda, família e reparação','B','Parcial','Resultados e eventos de ação; recusas e alternativas não enumeradas nem sempre emitem evento.'),
 ('politics','Sucessão de reinos','B','Parcial','Eventos e governante final; não equivale a sistema de guerra entre reinos ou política nacional completa.'),
 ('population','Censo de residentes','A','Completo no censo existente','Residentes, abstratos e mortes contabilizadas identificam o total atual; nascimentos naturais não existem.'),
 ('professions','Produção, pagamento e cozinha','B','Parcial','Resultado de trabalho é transitório; produção agregada/saldo não explicam cada salário ou material sem trace.'),
 ('quests','Pedidos e jogador','B','Parcial','Quest/Need e estados persistem; campanha sem jogador não valida naturalmente sua interação.'),
 ('recovery','Ledgers de dano e cura','B','Completo no ciclo existente','Acumulados e último tratamento; série de todo dano/cura por hora exige observador.'),
 ('relationships','Grafo dirigido','B','Parcial','Arestas atuais e alguns fatos causais; alterações sucessivas não têm log geral.'),
 ('religious_health','Censo religioso e relato local','B','Parcial','Snapshots agregados limitados e relatos locais separados; não preserva todo fiel por janela.'),
 ('renown','Renome, epítetos e objetos míticos','B','Parcial','Fontes e marcas limitadas; mito subjetivo não é propriedade física nem divindade objetiva.'),
 ('rules','Parâmetros compartilhados','A','Completo','Regras explícitas e thresholds embutidos estão inventariados; versão não garante compatibilidade comportamental.'),
 ('social','Confiança, ajuda e interpretação','C','Parcial','Retornos/cálculos transitórios e reputações atualizadas; todos os valores de entrada da escolha não ficam no save.'),
 ('society','Grupos, prefeitura e caminhos legados','B','Parcial','Grupos/propostas/planos persistem; há ramo político inacessível e via concorrente de formalização.'),
 ('terminal_combat','Incapacidade e oportunidade final','B','Completo no ciclo existente','Evento terminal explica seleção ocorrida; oportunidades descartadas não são registradas integralmente.'),
 ('ui','Apresentação do terminal','D','Completo no terminal atual','Texto digitado e todas as telas exibidas não são reconstruídos de um save final.'),
 ('utility','Score das alternativas','C','Completo no avaliador atual','Função pura recebe entradas variáveis; score histórico não se recupera sem snapshot das entradas.'),
 ('validation','Validação estrutural','A','Parcial como prova do mundo','Erros estruturais verificáveis; sucesso não prova plausibilidade, observabilidade ou conservação temporal.'),
 ('violence_patterns','Reconhecimento local de violência','B','Parcial','Padrões limitados e fatos fonte; não existe vigilância global da criminalidade.'),
 ('persistence','JSON e save/load','B','Parcial na continuidade geral','Formato e estado podem ser lidos; serialização por valor perde aliases e pode divergir em histórico mutável.')]

PERSISTENCE={
 '__init__':'Constantes não são snapshots; rules_version é gravada no envelope/WorldState.',
 '__main__':'World produzido/carregado é persistível; argumentos completos da CLI não são salvos.',
 'access':'Character.access_state/known_factions/known_sacred_sites; contratos, sacred_sites, POIs e sedes.',
 'action_pressure':'ActionPressure de Character/Group/Faction/Divinity e métricas; cálculo local completo é transitório.',
 'aftermath':'Character.death_state/death_affinity, death_records e eventos históricos.',
 'agency':'Character.commitments/aspirations/agency_state, Needs/context e eventos.',
 'collective_action':'Group/Faction.plan, knowledge, ActionPressure, commitment e ordens; serviço não persistido.',
 'conflicts':'Character.combat/health/emotions/observations, Needs e registros de morte.',
 'divine_relations':'Divinity.messages/affinities/bonds/presence_regions/essence/energy.',
 'economy':'Town.money/abstract_money/demand/stock/relatórios/produção; Kingdom.treasury; créditos nos donos.',
 'emotions':'Character.emotions/grievances e adaptação de personality; série histórica incompleta.',
 'engine':'WorldState.turn/rng_state/death_records/entidades; objetos coordenadores são reconstruídos.',
 'events':'WorldState.events256/history/metrics e Facts retidos; EventBus/SpatialIndex não persistidos.',
 'faith':'Character.religion/devotion/beliefs/mythic; World.divinities e estado de fé.',
 'feeding':'Character.food_state e World.feeding_diagnostics/metrics; margin_cache/listeners não.',
 'generation':'Entidades/seed/rules_version/RNG; config e generation_version não estão no esquema do save.',
 'geography':'World.routes; Character.route_knowledge/place_knowledge/known_towns/Journey; adjacency não.',
 'goals':'Goal/suspended_goal/Needs/failures; Solution/alternativas/debug/caches não são histórico persistente.',
 'institutions':'Policy/Proposal/Group/Faction/Town.office e conhecimentos individuais institucionais.',
 'investigation':'Pistas e busca nos contextos de agência/compromissos, observações/Needs e eventos retidos.',
 'items':'World.items + inventory de cada dono, origem/propriedades/história seletiva; item consumido pode sumir.',
 'justice':'World.wanted_records e Character.combat; índices/heaps de guardas são reconstruídos.',
 'knowledge':'Character.knowledge/memories/applied_facts/reputations/observations; listeners/pins em processamento não.',
 'lethal_decisions':'Character.lethal_decisions/commitments/combat/context e eventos privados retidos.',
 'lethality':'Character.combat.conflict_history, evidência e métricas; retorno evaluate não é histórico integral.',
 'migration':'Character.migration/position/home/workplace/town_id e censo de Town; Journey compartilhada.',
 'models':'Campos alcançáveis de WorldState são codificados por persistence.TYPES.',
 'navigation':'Character.position/known_places e town_id do jogador; path_cache não persistido.',
 'needs':'Needs dos donos, fisiologia, prioridades/status/context atuais e métricas; episódios anteriores sobrescritos.',
 'personal':'Observations/processed_personal_facts/personal_cooldowns/Needs; índice kin do serviço é reconstruído.',
 'personal_actions':'Posse/recursos/relações/Needs/context/quests e eventos; cálculo de candidatura transitório.',
 'politics':'Kingdom.ruler_id/heir_id/political_state e eventos de sucessão.',
 'population':'Town.population/abstract_population/resident_ids/counted_deaths e Character.town_id.',
 'professions':'Profissão/treinamento/wage_credit, estoques/produção/demanda da Town; WorkResult transitório.',
 'quests':'World.quests e Needs/context/recursos associados; sessão de terminal não.',
 'recovery':'HP/recoverable_deprivation_damage/damage_by_origin/recovery_state e métricas.',
 'relationships':'World.relationships dirigido; alterações anteriores sem evento não formam timeline.',
 'religious_health':'World.faith_health, Divinity.essence e Character.social_state.known_congregations.',
 'renown':'Character.renown/item_beliefs/beliefs/social_state; histórias/propriedades de Item.',
 'rules':'Parâmetros ficam no código; o save referencia versão de regras, não uma cópia de todos os valores.',
 'social':'Efeitos em reputação/relacionamentos/Needs; termos de Utility não ficam todos persistidos.',
 'society':'World.groups/factions/proposals; Town.office/mayor/military; vínculos/conhecimento de Character.',
 'terminal_combat':'Combat.pending_judgments e contexto da decisão, morte/Event; oportunidade calculada é transitória.',
 'ui':'Não persiste todas as telas/comandos; só efeitos do núcleo e save solicitado.',
 'utility':'Cálculo puro; último Goal.score pode persistir, concorrentes/terms/draws não universalmente.',
 'validation':'Retorna erros sem persistência própria; manifesto externo guarda resultados da auditoria.',
 'violence_patterns':'Character.social_state.violence_patterns/fear_of_killer, security Need e fontes.',
 'persistence':'Envelope versionado + WorldState tipado/RNG; serviços/caches/identidade de alias não.'}

NEEDS=[
 ('food','needs.refresh','hunger ≥35; pressão por faixas 20–100','eat; buy_food/forage/steal/ask_help/work/work_for_food; sete variantes *_meal; take_site_supplies','hunger<35; execução nominal de compra não satisfaz por si só'),
 ('food_reserve','needs.refresh','déficit da reserva 24h, margem de viagem, alvo ≤6; pressão ≤85','aquisições do food; train/temporary_service se ofertas conhecidas; suprimento de local','cobertura/alvo atingido; não significa comer'),
 ('water','needs.refresh','thirst≥25; emergência≥98','drink; drink_well em mercado/poços conhecidos; drink_stream sem mercado; suprimento em POI','thirst<25'),
 ('rest','needs.refresh','fatigue≥25','sleep em casa; retorno geográfico se aplicável','fatigue<25'),
 ('money','needs.refresh','reserva<10 ou alvo20 após48h; urgência≤70','work; train; temporary_service; work_for_food; sell_surplus; alternativas institucionais devidas','saldo/estabilidade e reavaliação; não há salário automático'),
 ('work','needs.refresh','8≤hora<18; ocupação remunerada ou treino; base35','work; train; temporário conhecido e compatível','fora do horário ou responsabilidade resolvida; produção não é contínua sem ação'),
 ('security','needs.refresh/justice/violence_patterns','guarda, crime conhecido fresco/confiante; base60; padrões violentos têm contexto próprio','secure; pursue; watch_case; follow_lead/search_area/ask_about_person; respostas legais','caso conhecido encerrado/expirado/inacessível; não olha lista global de criminosos'),
 ('family','personal.refresh/on_fact','vínculo e observação de carência/ausência; urgência/contexto no criador','check_relative; give_supplies; ask_personal_help; aquisições de provisão; busca/pista/rota','encontro, ajuda válida ou notícia de morte; duração/cooldown por alvo'),
 ('grief','personal.on_fact','morte conhecida de vínculo≥40; 20+.35*vínculo; duração48+vínculo','remember_relative; seek_company; ajuda pessoal','conforto recebido/lembrança/resolução/expiração; não deriva só da morte objetiva'),
 ('revenge','personal.revenge/lethal_decisions','dano conhecido; base20+.25*vínculo; duração48+2*vengefulness','investigate; denounce; confront; demand_return; threaten; attack; busca; finish só com oportunidade','morte conhecida do responsável, guarda/reparação, compromisso resolvido/expiração'),
 ('protection','personal.on_fact/conflicts','crime/ameaça conhecida; alvo é protegido, context.threat é agressor','stay_near; avoid_threat; denounce; protect/intervene; confront/attack; busca','proteção recebida/ameaça encerrada/expiração'),
 ('status','personal.refresh/agency','ambição/reconhecimento e aspiração; urgência no criador','work; seek_company; train; share_problem; ações sociais condicionais','feito significativo, aspiração/meta ou expiração'),
 ('advancement','personal.refresh/agency','competência/renda persistente; urgência no criador','train; work; sell_surplus; soluções restritas a train no domínio competence','treino/competência e reavaliação; não há carreira geral para toda profissão'),
 ('response','conflicts.refresh','oponente/ameaça percebida, resposta física ou reparação','attack/defend/flee/surrender/confront/withdraw; alert/call_help; apologize/return_stolen/forgive','conflito acaba, trégua, morte/incapacidade ou timeout'),
 ('assistance','conflicts.refresh','necessidade conhecida de socorro','first_aid; call_help; intervenção física compatível','socorro/risco resolvido ou alvo indisponível'),
 ('pursuit','justice.refresh','wanted conhecido, severidade e jurisdição','pursue/follow_lead/watch_case/search_area/ask_about_person/capture; ataque condicionado','detenção/encerramento/expiração ou espera por informação'),
 ('healing','conflicts.refresh','lesão e tratamento necessário','seek_treatment; first_aid/call_help conforme contexto','estabilização e reavaliação'),
 ('recovery','recovery.refresh','HP<80; min95,25+(80−HP)','delegação a food/water para estabilizar; sleep; seek_treatment/call_help com lesão','HP≥80; cura rápida só sobre ledger fisiológico'),
 ('despair','conflicts.refresh','convergência extrema e persistente; não é toda pobreza','apoio/alternativas de sobrevivência; self_harm sob gate raro','pressão/desespero reduzido ou fim do ciclo; não chamar toda morte natural'),
 ('migration','migration.refresh','ameaça, wanted, pobreza e local conhecido viável','migrate; route_travel; ask_route; preparação de provisões','chegada muda residência; viagem isolada não muda censo'),
 ('political_pressure','society.refresh','problema local percebido/compatível; urgência derivada','share_problem; organize; join_group; attend_group; ask_route/route_travel','aderir/encaminhar/resolver/reavaliar a causa; grupos desconhecidos não são opções'),
 ('organizational_survival','society.refresh','grupo ou facção existente; contexto reutilizado','meet_group; submit/support_proposal; report/contribute/assignment/recruit; institucional_supply/purchase/patrol/raid; formalize_organization; representação','objetivo/estado institucional; risco de contextos group_id e faction_id misturados'),
 ('governance','society.refresh/institutions.refresh','prefeito/representante, proposta recebida ou obrigação local','review_proposal; serve_office; issue_local_order; read_response; relay_response; policy_work','resposta/entrega/estado político; sem conhecimento não há julgamento remoto'),
 ('institutional_work','institutions.refresh','política conhecida ativa/stalled e worker elegível; base48 ou63 se money<15, cap75','policy_work; route_travel/ask_route se entrega TRANSPORT','política concluída ou sem oferta válida; aptidão material é revalidada na execução'),
 ('institutional_response','institutions.refresh','membro recebe restrição RESTRICTED/ILLEGAL conhecida; base55','institutional_response','resposta explícita satisfaz; silêncio ou lei desconhecida não inicia a ação'),
 ('military_service','society.refresh','atribuição institucional/militar conhecida','perform_assignment; faction_prepare; faction_raid; defend/protect condicionais','atribuição/ordem e reavaliação'),
 ('recognition','society.refresh','renome/posição aspirada','seek_local_office; ações de responsabilidade/organização conforme contexto','reconhecimento real e limites locais'),
 ('religious_interest','faith.refresh/aftermath','crença, devoção, fatos ou conflito moral','pray; offer_resource; spread_faith; reinterpret; defend_cult; report_congregation (B08); tell_item_history; challenge_divinity/claim_essence condicionais','rito/reinterpretação/estado; repetição de ato não prova contato divino'),
 ('power','faith.refresh','potencial mítico, ambição e conhecimento','train_power; challenge/claim são enumeradas por religious_interest sob seus próprios gates','treino/ascensão/resolução; ambição não gera essência'),
 ('divine_contact','access.refresh','motivo e sítio sagrado conhecido','seek_divine_contact; ask_route/route_travel; oração/rito no destino','audiência/espera/recusa/novo conhecimento; chegar não garante resposta'),
 ('divine_contract','access.refresh','oferta ou pacto pessoal conhecido','accept_contract; refuse_contract; abandon_contract; cumprimento por ações existentes','estado do pacto e obrigação; deus precisa saber da quebra'),
 ('organizational_access','access.refresh','convite recebido/interesse em facção conhecida','answer_invitation; request_membership; invite_person; attend_faction; viagem','aceitação/recusa/adiamento/expiração motivada'),
 ('affiliation','access.refresh','convite recebido base43 ou interesse próprio base36 em organização conhecida','answer_invitation; request_membership; attend_faction; viagem','aceitação/recusa/condicionamento/adiamento; não integração automática'),
 ('organizational_base','access.refresh','base/POI conhecido e interesse organizacional','claim_location; store_supplies; form_expedition; explore_poi; viagem','ocupação/estoque/base ou bloqueio de acesso/capacidade'),
 ('exploration','access.refresh','POI e motivação conhecidos','explore_poi; form_expedition; follow_expedition; viagem','exploração/retorno/expiração conforme contexto'),
 ('return_from_site','access.refresh','retorno de POI/rota concluída','route_travel; ask_route; take_site_supplies se necessário','chegada confirmada'),
 ('spatial_journey','access.refresh','Journey em curso','route_travel; rotina de retomada/pausa/provisões','Journey concluída/abortada; não implica trocar residência'),
 ('professional','economy.daily (Town)','déficit produtivo/ProfessionalDemand; base55','diagnóstico; resposta administrativa usa Goal coletiva ligada ao Need food, com expand_farming/publish_temporary_work/open_training/materialize_worker/improve_utilization','demanda revista; não possui seletor profissional autônomo por seu próprio ID'),
 ('resource_pressure / water_access / security / religious_interest / criminal_cooperation (Group)','society.form, cause dinâmica','causa compartilhada; urgência/priority herdadas da fonte individual','commitment coletivo/plano; execução por membros/representante via organizational_survival, não um NPC Group autônomo','grupo/causa/proposta e lifecycle próprios; expedition cria Group, mas não chama ensure de Need coletiva nesse caminho'),
 ('organizational_survival (Faction)','society.orders','relato conhecido; base45','Goal perform_assignment da facção; ordens para membros presentes; ação depende de cada Character','ordem/capacidade/estado institucional; Goal do agregado não percorre Engine como personagem'),
 ('food (Town/Kingdom)','economy.daily','escassez coletiva e pedidos','política/Quest/administração; não é um estômago coletivo que executa eat','estoque/relatório/encaminhamento reavaliado')]

BUGS=[
 ('B01','Confirmado — histórico e persistência','events.EventRecorder.emit / knowledge.observe / society.form','Contexto conserva listas vivas de Group.member_ids. Um join posterior reescreve GroupFormed antigo e Facts. Save/load copia por valor e desfaz o alias: mesmo join com RNG igual pode deixar históricos diferentes.','Prova controlada com form→snapshot→loads→join idêntico; membros atuais iguais, contexto antigo divergente; phase51.test_11 também falha.'),
 ('B02','Confirmado — ramo inacessível','society.SocietySystem.react','PolicyDecided delega a Institutions.react_decision e retorna. O ramo posterior que escreveria Group.responsibility_id nunca executa; a delegada não o escreve. Assume_local_office exige esse campo.','Fonte + únicos leitores/escritor + falhas phase5.test_06 e phase51.test_04. Não depende de esperar outra seed.'),
 ('B03','Confirmado — cooldown contornado','goals.GoalSystem.preventive_choice','fill_water é criado depois de _evaluate sem repetir cooldown/checagem de estoque; uma ação bloqueada pode reaparecer como preparação.','Fonte e reprodução natural já preservada em Neravon; esta campanha informa novas ocorrências separadamente.'),
 ('B04','Confirmado — vias divergentes','society.meeting / institutions.formalization / access.execute','Via normal exige score≥65 e três presentes; formalize_organization legado chama found_faction diretamente e pode formalizar com dois/score55.','Prova controlada da auditoria de coesão; nenhuma nova formalização natural é fabricada.'),
 ('B05','Confirmado — candidato e execução divergem','institutions.faction_candidates / execute','Suprimento é oferecido com food OU water; execução escolhe o produto da maior privação e pode falhar mesmo com o outro disponível.','Fonte e controle prévio; ausência de falha natural não remove a inconsistência.'),
 ('B06','Estado ambíguo confirmado; impacto ainda parcial','society.refresh / society.candidates / action_pressure.key','Reutilização de organizational_survival pode manter faction_id antigo quando escreve group_id; ordenação de candidatos consulta facção primeiro e chave de pressão prefere grupo.','Snapshot final de líderes em Neravon; contexto misto é verificável, mas sua parcela causal sobre inatividade não está quantificada.')]

BUGS.extend([
 ('B07','Confirmado — causa textual contraditória','access.explore → engine.finish_death','Causa exploration no registro/contexto recebe descrição genérica de morte autoinfligida.','Reprodução controlada de finish_death com causa exploration, sem hora natural adicional.'),
 ('B08','Confirmado — crash condicional','faith.candidates → utility.evaluate','report_congregation é uma alternativa real de religious_interest, mas não existe em utility.BASE; ao alcançar a avaliação, ocorre KeyError antes do envio do relato.','Reprodução com orações testemunhadas e duas mortes conhecidas, zero horas naturais; nenhuma correção aplicada.')])

TEST_NOTES={
 'test_meal_at_normal_threshold_uses_most_nutrition':'Falha: spread_faith venceu eat na fixture. Competição entre Needs é real; expectativa de comer a35 não equivale a emergência. Revisar intenção do teste antes de chamar bug.',
 'test_15_population_balance_geography_identity':'Falha: literais de densidade/contagem anteriores à geração atual; não prova corrupção populacional.',
 'test_06_recovery_ends_and_material_despair_falls_gradually':'Falha: HP76 em vez de≥80. Interferência de prioridade/descanso na fixture; regressão comportamental possível, causa não isolada nesta auditoria.',
 'test_12_lethal_incapacity_requires_new_moral_decision':'Erro: fixture espera violence_intents[target] legado; decisão atual dirigida está em lethal_decisions. Verificar compatibilidade do cenário.',
 'test_16_interlocal_following_uses_only_known_lead':'Falha: alternativa follow_lead agora aparece; conhecimento de trajeto e pista têm novo caminho. Expectativa legada de lista vazia.',
 'test_02_extreme_convergence_and_evidence_trace':'Erro: teste lê loss_importance, campo que a avaliação atual não retorna. Contrato do teste desatualizado.',
 'test_03_low_confidence_and_unknown_author':'Falha: confiança esperada30, atual0 após filtros de autoria/evidência; fixture/contrato precisa revisão.',
 'test_06_group_response_requires_received_decision':'Falha pertinente a B02: responsibility_id nunca recebe o prefeito por ramo inacessível.',
 'test_10_promotion_not_xp_or_money_only':'Erro: assignments[target] ausente na fixture de membro. Falta robustez para membro sem assignment; ocorrência natural não demonstrada.',
 'test_21_divine_death_is_separate_and_not_automatic_apotheosis':'Falha: gates atuais exigem manifestação/acesso físico; fixture antiga não demonstra esse acesso.',
 'test_22_claimed_essence_transforms_domain':'Falha: acesso físico/essência atuais não satisfeitos no cenário legado; ciclo permanece testável por controles atuais.',
 'test_26_situational_lethality_requires_immediate_extreme_threat':'Falha de nome: situational virou reactive_threat; não é por si uma morte incorreta.',
 'test_28_save_limits_query_purity_and_seeded_continuity':'Falha real da premissa de consulta pura: solutions pode atualizar planos/diagnósticos. Não usar para visualização passiva.',
 'test_29_office_contact_and_known_physical_faction_route':'Falha de acesso/contato em fixture de geração anterior; não provada falha estrutural nova.',
 'test_30_public_reply_is_physical_and_remote_status_is_not_knowledge':'Falha: conhecimento local ficou rejected; fluxo de decisões/localidade mudou. Investigar contrato da fixture; não inferir telepatia só desse resultado.',
 'test_02_grave_known_loss_enables_intention_execution':'Falha: ataque habilitado onde fixture esperava bloqueio. Política letal/pressão atual mudou; não demonstra morte inevitável.',
 'test_03_many_weak_factors_do_not_become_grave_world_pressure':'Falha: disponibilidadeFalse. Avaliação de letalidade foi reformulada; é necessário confrontar a causa grave real da fixture.',
 'test_04_received_group_failures_raise_pressure_without_duplicate':'Falha pertinente a B02: assume_local_office não aparece, pois responsabilidade não é atribuída.',
 'test_07_capable_faction_acts_with_cost_and_ideology_filter':'Falha: institutional_supply sai antes de perform_assignment. Prioridade/exclusividade entre provedores, não ausência total de ação institucional.',
 'test_10_village_representation_travels_and_response_returns':'Falha: represent_travel necessita caminho físico conhecido segundo a geografia atual; fixture legada não o satisfaz.',
 'test_11_pressure_save_queries_and_deterministic_continuation':'Falha pertinente a B01: listas de membros no contexto de eventos são aliases no mundo vivo e cópias no carregado.'}

def test_results():
    if not (OUT/'testes_completos.log').exists():return read('manifesto.json')['test_suite']
    log=(OUT/'testes_completos.log').read_text()
    rows=[]
    for line in log.splitlines():
        m=re.match(r'(FAIL|ERROR): (\w+) \(([^)]+)\)',line)
        if m:rows.append({'result':m[1],'name':m[2],'test':m[3],'assessment':TEST_NOTES.get(m[2],'Analisar traceback preservado no manifesto; sem classificação automática.')})
    return {'total':326,'passed':305,'failed':18,'errors':3,'seconds':161.969,'issues':rows,'log_sha256':hashlib.sha256(log.encode()).hexdigest(),'log':log}

def systems_matrix(inv,metrics):
    available={f['module'] for f in inv['files']}
    catalog={s[0]:s for s in SYSTEMS}
    rows=[]
    for module in sorted(available):
        s=catalog.get(module,(module,module,'C','Parcial','Inspeção estática disponível; ciclo específico no mapa.'))
        fs=[f for f in inv['functions'] if f['module']==module]
        counts={f['symbol']:metrics['calls'].get(f['symbol'],0) for f in fs}
        generation=sum(v for k,v in metrics.get('generation_calls',{}).items() if k.startswith(module+'.'))
        # Assertion inventory is evidence of a fixture, never a natural call.
        tests=[t for t in inv['tests'] if any(module in c or any(f['name'] in c.rsplit('.',1)[-1] for f in fs if f['name'] not in ('__init__','execute','refresh','tick','count','emit','set','learn')) for c in t['calls'])]
        rows.append({'module':module,'system':s[1],'observability':s[2],'completeness':s[3],'limitation':s[4],
                     'implemented':True,'natural_calls':sum(counts.values()),'generation_calls':generation,'methods_observed':sum(v>0 for v in counts.values()),'methods_total':len(fs),'methods':counts,
                     'controlled_test_candidates':[t['file']+'::'+t['class']+'.'+t['name'] for t in tests],
                     'test_mapping':'Conservador por chamadas/nomes; confirmar assertivas no MAPA. Não é medição de branch coverage.',
                     'persistent':PERSISTENCE[module]})
    return rows

def requirements_index():
    request=Path('/home/hugo/.codex/attachments/3a924848-7d24-44b4-bf93-d9b470b9912b/Texto colado.txt')
    if not request.exists():return []
    rows=[]
    for n,title in re.findall(r'^# (\d+)\. (.+)$',request.read_text(),re.M):
        number=int(n)
        target='RADIOGRAFIA_TOTAL.md'
        if number in (3,4,10,14,15,16,30,73,74,75,96):target='MAPA_CODIGO.md'
        if number in (67,68,69,70,71,78,98):target='OBSERVABILIDADE.md'
        if number in (80,81,82,83,97):target='DECISOES_REAIS.md'
        limit='Lacunas por sistema explicitadas; fonte, amostra e agregado são provas distintas.'
        if number in (14,15,70,80,83,84,85,104):limit='Cobertura parcial de causalidade histórica: gates nunca enumerados, snapshots ausentes e coortes de latência não capturadas são lacunas declaradas, sem inferência retrospectiva.'
        if number in (55,56,57,63):limit='Ciclo estático/gates e controles catalogados; ocorrência rara natural não é exigida nem fabricada.'
        rows.append({'requirement':number,'title':title,'primary_report':target,'limit':limit})
    assert len(rows)==104
    return rows

def static_narrative(inv):
    text='''## Como ler e verificar

O código é a autoridade. O [MAPA_CODIGO.md](MAPA_CODIGO.md) enumera cada função, campos lidos/escritos, chamadas, emissores, gates, traits, constantes, invariantes e cada teste. As expressões exatas e os trechos de fonte no apêndice delimitam fórmulas e exceções. [DECISOES_REAIS.md](DECISOES_REAIS.md) mostra entradas e resultados realmente capturados; [OBSERVABILIDADE.md](OBSERVABILIDADE.md) identifica o que não se consegue reconstruir. “Não observado” não significa “ausente”, e “implementado” não significa ciclo completo em todas as profissões/setores.

Não houve mecânica, rebalanceamento, ajuste de seed nem correção do núcleo nesta auditoria. Houve inventário antes da simulação, execução da suíte inteira e um único mundo natural de 300h. Controles isolados são identificados como controles. A campanha sem jogador não prova a experiência de comandos ou Quests.

## Dependências reais

```mermaid
flowchart TD
 GEN[Geração / seed / RNG] --> W[WorldState / modelos]
 E[Engine.step] --> L[Feeding: LOD]
 L --> G[GoalSystem.decide]
 G --> N[NeedSystem.refresh]
 P[Fisiologia / recuperação] --> N
 K[Knowledge: Fact / observações] --> N
 R[Relações / personalidade / emoções] --> N
 A[Agency / ActionPressure / compromisso] --> N
 N --> C[Produtores de alternativas / gates]
 C --> U[Utility e ajustes]
 U --> GO[Continuidade / Goal / preparação]
 GO --> X[Execução física]
 X --> EV[EventRecorder / EventBus]
 EV --> K
 X --> W
 E --> P
 EC[Economy / Professions / Items] --> C
 EC --> X
 CJ[Crime / Justice / Investigation / Combat] --> C
 CJ --> X
 SI[Society / Institutions / políticas] --> C
 SI --> X
 F[Faith / DivineRelations / Access] --> C
 F --> X
 GE[Navigation / Geography / Migration] --> C
 GE --> X
 EV --> PO[Population / Politics / aftermath / renome]
 W --> SAVE[Persistência / validação]
```

O grafo de chamadas resolvidas por método está no MAPA; as arestas medidas na campanha ficam em metrics.call_edges. Despacho dinâmico e callbacks são declarados como tal; uma importação não é prova de chamada.

## Uma hora: ordem exata e consequências do relógio

| Ordem | Função/guarda | Entidades e efeito |
| --- | --- | --- |
| 1 | closing_turn = turn+1; IDs em ordem crescente | Ignora mortos e jogador; o menor ID age antes e pode modificar recursos/conhecimento de quem decide depois. |
| 2 | feeding.decision_interval | Atualiza lod; decide se closing_turn % interval == id % interval. elapsed=max(1,closing_turn−last_update). |
| 3 | goals.decide; last_update=closing_turn | Observe mercado, refresh de Needs/serviços, alternativas, gates, Utility, continuidade, preparo, movimento e execução. Eventos reagem sincronicamente durante a ação. Ainda usa o turn anterior ao fechamento. |
| 4 | world.turn=closing_turn | Só agora fecha a hora. |
| 5 | needs.physiology, todos os vivos, inclusive jogador | Fome/sede/fadiga aumentam todo tick, qualquer LOD. Dano e starvation_hours são aplicados. |
| 6 | health≤0 → finish_death('deprivation') | Fecha morte imediatamente; sobrevivente jogador recebe needs.refresh. Mortes em combate podem ter ocorrido antes, dentro da ação. |
| 7 | turn%6==0 → knowledge.gossip | Snapshot impede notícia atravessar cadeia inteira no mesmo gossip. |
| 8 | turn%24==0 → economy.daily | Produção/consumo/relatórios coletivos/mercado e demandas; não equivale a cada NPC trabalhar. |
| 9 | justice.tick | A cada hora expira casos/libera detenção; communicate a cada AGENCY.institutional_latency=6h. |
| 10 | society.tick | Chamado a cada hora, retorna fora de turn%24==0; então substitui cargos, limpa grupos/propostas e membros/lideranças de facções. |
| 11 | institutions.tick | Retorna fora de turn%24==0; verifica ausência de trabalho≥48h/tempo da política≥48h e convites/candidatos mortos, sem substituir trabalhador físico. |
| 12 | faith.tick | Toda hora avalia oportunidades/pressão dos deuses; saúde religiosa a24h, energia +.5 a24h; intervenções têm cooldown168h e consideração emitida≤1/24h. |
| 13 | quests.reconcile | Reconcilia estado material/social dos pedidos. |
| 14 | world.rng_state=rng.getstate() | Snapshot do RNG; execute também sincroniza quando há sucesso ou RNG consumido. Não existe autosave por hora. |

Comer pode impedir dano no fechamento seguinte, mas adquirir, caminhar e consumir são operações diferentes. Um NPC não toma necessariamente uma nova decisão entre duas horas de fisiologia. Uma ação longa usa elapsed, porém caminhada debita suas horas antes de produção. Uma falha pode voltar à fila com cooldown de12h; a preparação de água constitui a exceção problemática B03.

## LOD real

Não há enums HIGH/MEDIUM/LOW. Existem `active`, `local`, `background`. Active decide a cada1h por promoção temporal, combate, migração em curso, HP<30, categoria lendária, fome≥80, sede≥85 ou jogador vivo a distância≤3. Fome≥35 dá local/3h. Comum em casa sem essas condições fica background/12h; demais local/6h ou importante/3h. A ordem é relevante: uma condição anterior prevalece sobre a seguinte.

Fisiologia, gossip periódico e economia global continuam. Percepção/refresh/emoções/alternativas e trabalho dependem da decisão, enquanto aprender um evento dispara listeners imediatamente. LOD muda semanticamente oportunidades de comer/reagir/trabalhar, tamanho do lote elapsed, chegada e competição; não é só uma otimização gráfica. As distribuições observadas aparecem adiante.

## Geração: seed até o mundo

`seed_number` usa SHA256 de `GENERATION_VERSION:seed`, convertido em inteiro para um único random.Random. Uma mesma seed com versão/config diferentes não é comparação isolada. O mapa500×500 usa625 regiões de20×20 e 8% de irregularidade por célula em .FDS. Config valida500×500, reinos1–6, distância mínima1–12, distância de vila maior que a mínima e≤24, pelo menos8 NPCs/cidade e histórico≥0. Centros dos4 reinos são predeterminados; bounds, posições, biomas e escolhas usam RNG. Posição tenta até3000 vezes respeitando Manhattan mínima.

Cada reino tem5 cidades (primeira capital) e1–2 vilas por cidade, distribuídas por sorteio. Mapas locais têm15/11/7 células de lado; mercados/poços/casas/oficinas/área rural são acessos determinados, detalhes variam. População inicial sorteada é depois ajustada na densificação padrão de4 reinos:104 residentes/capital,60/cidade,18/vila, com razão abstrata2.1/2.5/2.7; não há promessa de quantidade fixa de localidades para toda seed. Cada Town recebe dinheiro800–1600 e reservas iniciais40food,80water,40grain,24iron,24wood; a geração é dotação inicial, não dinheiro criado pelo trabalho.

Onze traits iniciais são inteiros5–95; sadism=round(100*random()**6), concentrado em valores baixos. Dinheiro1–28, fome10–60, fadiga0–20, devoção0–100, comida1–2. Profissão segue ciclo de8 ocupações e papéis régios separados; itens/ferramentas/armas dependem da profissão/categoria. Famílias são arestas explícitas, nomes coerentes e trios de pais/filho na densificação; não há demografia reprodutiva autônoma.

O gerador cria8 POIs,2 sedes com líderes e facções iniciais, estoque material e6 locais exploráveis; caverna tem profundidade1–4 e perigo6–35. Cria dados de relações/reinos, densifica depois da geografia, salva RNG, instancia Engine, chama bootstrap de sociedade/fé/geografia/acesso e emite fundações. `historical_turns` normalmente24, explicitamente0 aqui. Jogador, quando solicitado, é criado depois da história inicial com25 moedas,4food,6water. Fórmulas/ranges restantes e todos os sites de RNG estão no MAPA e no apêndice da geração.

## Character: estado completo e proprietários das alterações

Os campos declarados, defaults e tipos estão integralmente no MAPA. Relações familiares não são uma lista oculta do personagem: ficam no grafo do mundo. `faction` legado não substitui organization_ids.

| Grupo | Estado | Leitores / escritores principais |
| --- | --- | --- |
| Identidade | id,name,surname,nickname,category,alive,is_player,origin,faction | Geração/materialização; renome; Engine.finish_death; serviços consultam IDs, não nomes. |
| Corpo | health,hunger,thirst,fatigue,starvation_hours,damage_by_origin,recoverable_deprivation_damage,recovery_state,last_meal,last_drink | Needs/Recovery/Feeding, execução de refeições/sono/tratamento, Conflict e Engine. |
| Economia | money,inventory,wage_credit,financial_since,financial_setbacks | Items/Economy/Professions/Institutions/Access; Needs e Utility leem pressão/renda. |
| Personalidade/emoções | personality,emotions,grievances,death_affinity,death_state | Geração; Emotion adapta lentamente; Aftermath/LethalDecision/ViolencePatterns; prioridade e Utility leem. |
| Trabalho/lugar | position,home,workplace,town_id,profession,training_target/progress/required/started/last_practice,market_observation | Navigation/Geography/Migration/Professions/Economy; conhecimento limita escolhas de trabalho/rotas. |
| Saber/memória | knowledge,memories,reputations,known_places,failures,applied_facts,observations,processed_personal_facts,personal_cooldowns | Knowledge/Personal/Social/Investigation/Geography; informações têm data/fonte, retenção e confiança. |
| Decisão | needs,goal,suspended_goal,last_update,active_until,lod,food_state,commitments,aspirations,agency_state,action_pressures,lethal_decisions | Needs/Goals/Agency/Feeding/ActionPressure/LethalDecision; eventos podem promover LOD, não executar ação diretamente. |
| Instituições | group_ids,organization_ids,social_state,known_groups/proposals/policies/factions | Society/Institutions/Access; conhecer e integrar são estados diferentes. |
| Fé/mito | religion,devotion,beliefs,renown,item_beliefs,mythic_trait,mythic_development,known_sacred_sites | Faith/Renown/DivineRelations/Access; crença e propriedades objetivas separadas. |
| Conflito/viagem | combat,known_towns,migration,route_knowledge,place_knowledge,journey,access_state | Conflict/Justice/TerminalCombat/Geography/Migration/Access; cargo não dá teleportação. |

## Personalidade e emoções

O MAPA contém, para cada um dos12 traits, todas as referências diretas e pesos Utility expandidos, com a expressão exata que mostra sinal, condição e efeito; não se resume cada trait a um adjetivo. Honesty afeta roubo, denúncia, restrição moral e decisão política; compassion afeta ajuda, vínculos, inibição e reação à morte; courage afeta risco/ação/fuga; independence afeta autonomia/ajuda/migração/adesão; greed afeta apropriação/retorno/decisão; diligence afeta prioridade laboral, trabalho/treino e governo; family_loyalty afeta família/proteção/migração; persistence afeta continuidade, busca e organização; temperament afeta hostilidade/protesto; vengefulness afeta investigação/agravo/letais; ambition afeta carreira/status/organização/poder; sadism afeta decisão letal/aftermath, sem peso genérico na Utility-base.

EmotionalState persiste anger, resentment, humiliation, desperation e ledgers/fontes de desespero, perdas/processamento, strain/adaptation e horários. Fear, guilt, shame, relief, pride, pleasure, fascination, numbness, grief e moral_conflict de morte são principalmente avaliações em death_state/appraisals e termos derivados, não onze barras globais com decaimento uniforme. Grief também é Need. Fear de combate deriva de poder/risco percebido.

Fato prejudicial com confiança≥30 e dano pessoal/familiar produz intensidade proporcional ao ganho de confiança: furto18, ataque30, ameaça16, insulto12, morte violenta45, privação8; anger soma intensidade, resentment55%, humiliation50% em contextos específicos/confiança≥70. O mesmo fato não duplica integralmente a emoção. Apoio reduz anger/desespero e parte da humilhação; reparação também reduz grievance/ressentimento. Atualização por elapsed decai anger .3/h, resentment .04/h, humiliation .1/h, grievance .025/h. Pressões de privação/pobreza/luto/violência/perseguição aumentam fontes separadas; estabilidade material≥6h reduz só fontes materiais .25/h, não apaga luto. Adaptação exige strain≥720, intervalo720 e máximo5 mudanças, +1vengefulness/+1independence. O histórico completo anterior não fica retido.

## Need, prioridade e alternativas

Need tem ID, owner, kind,target,base_urgency,priority,created/updated,status,source,reason,expires e context. A chave pode ser kind:alvo, mas `kind=key.split(':')[0]`; chaves distintas não são novos kinds. `ensure` reativa/reutiliza ID, limpa contexto na reativação de encerrado e finaliza compromisso anterior pertinente. `finish` muda status/prioridade, Goal e cooldown pessoal48h; não confundir status da ação com satisfação fisiológica. Alguns produtores usam espera por informação, bloqueio, expiração e resolução de compromissos.

Prioridade comum=min100(base+min8,idade*.15+traço+amizade/10+perigo+emoção), com diligence/5 em money/work e courage/10+20 em security. Food/water base≥80 recebem perigo15; emergência força100. Food_reserve substitui essa prioridade pela fórmula de cobertura. Agency acrescenta até seu teto; ActionPressure pode acrescentar value*.14. Ordenação é rank de emergência, prioridade decrescente, ID crescente. Emergência food/water tem rank2 com nível≥98, rank1 abaixo, demais0.

O motor percorre Needs nessa ordem e para na primeira com solução viável. Utility compara alternativas dessa Need; uma ação de score200 de uma Need inferior não vence globalmente uma ação de score70 da Need superior. Continuidade pode conservar Goal anterior dentro da margem12 respeitando emergências/refeição/recuperação. Objetivos suspensos não são uma fila ilimitada: há um suspended_goal, compromissos têm até4, aspirações até2, pressão até8 registros.

'''
    text+=table(['Kind / dono','Criador','Ativação / base','Alternativas condicionais','Término / bloqueio'],NEEDS)
    text+='''A tabela enumera famílias sem prometer todas simultaneamente. Para cada criador, o MAPA preserva argumentos de urgência/source/reason/target/context; o apêndice transcreve os produtores reais para resolver os gates específicos e a duração. Há Needs coletivas como water_access/resource_pressure e cooperação derivadas das causas/diagnósticos; uma causa de grupo não deve ser contada automaticamente como um Need.kind de Character.

## Gates: antes e depois da Utility

| Etapa | Exemplos reais / efeito |
| --- | --- |
| Produtor | Conhecimento do local/fato/rota, profissão, alvo, grupo conhecido e compatível, cargo/papel, oferta observada fresca, capacidade e recursos locais quando observáveis; pode retornar zero antes de criar Solution. |
| Filtro de soluções | Saturação/treino substitui work; detenção/rendição restringem ações e destino; competência aspirada mantém só train; busca troca alternativas genéricas por pistas. |
| _evaluate antes do score | ActionPressure não elegível; provisão familiar já suficiente; cooldown de ação/base/pedido; destino em outro mapa. Essas soluções não chamam utility.evaluate. |
| Avaliação especializada | Terminal usa tabela própria e não Utility.BASE; valores sentinela≤−1000 eliminam opções. |
| Após Utility-base | Feeding.estimate pode rejeitar prazo inviável; variantes refeição podem remover aquisição equivalente; Agency/Faith modificam scores; estas etapas não são gates pré-Utility. |
| Após escolha | Continuidade de Goal, suspended_goal e preventive_choice podem trocar winner/destino; o preparo de água não repete todas as guardas. |
| Execução | Revalida contato, saldo/estoque, capacidade, evidência, acesso e condições. Um candidato viável anteriormente pode falhar legitimamente depois da caminhada. |

Todos os gates sintáticos de saída/continue/erro estão por método no MAPA, com condições numéricas/compreensões nos trechos de fonte. Um candidato que o produtor nunca criou não aparece como “perdeu por Utility”. O observador só atribui razão quando a entrada/retorno real a sustenta; as demais são lacunas explícitas.

## Utility e Goal

`score = BASE[action] + Σ(values[name] * WEIGHTS[action][name]) − min(200,2*travel)`. Traits passam por normalized; termos sociais podem substituir valores e incluem confiança, reputação, vínculo, risco, autoridade, lesão, privação e pressão de recuperação. Considerations são parcelas divididas por200; comparar o score exige multiplicá-las por200. MEALS usa a base da aquisição original. O catálogo de TODAS as ações e pesos está no MAPA.

ActionPressure acrescenta25% de sua pressão às ações pertinentes, exceto attack no caminho normal. Treino considera demanda, pressão financeira, custo por diligência, valor do emprego e risco. Agency acrescenta compromisso/aspiração; Faith aplica influência mítica. Terminal substitui a competição pelo seu winner real. Fora do terminal, alternativas a até3 pontos da primeira sofrem variação uniforme[−1.5,+1.5] apenas no desempate; draw individual não fica persistido. Scores iguais ordenam ação/target antes da escolha.

Goal persiste ação, Need, score, criação, alvo/destino/status/outcome. Caminhada pode consumir todo elapsed e deixar Goal ativo sem execute. Falha registra outcome e cooldown12h; Need volta ativa. Uma ação concluída não resolve automaticamente todos os seus motivos. Suspensão por refeição e retomada, janela de continuidade, blocked, desistência/espera e progresso dos compromissos estão na fonte transcrita. O abandono usa clamp(idle/8 + failures*8 + setbacks*3 − persistence*.25 − ambition*.1) > 55 + persistence*.3; o horizonte finito é720 + 3*persistence horas, com exceções/continuidade para decisão letal ativa e espera por informação conforme a ordem dos ramos. AGENCY.no_progress_hours=168 não é lido nesse fluxo, portanto não é um timeout fixo de168h. Não existe planejador externo executando fora de Need/Goal.

## WorldPressure, ActionPressure e capacidade

WorldPressure exige causas conhecidas e específicas: perda próxima, ameaça extrema, dano grave repetido, pedido recebido, causa institucional/fé. Soma de traços fracos não cria automaticamente uma causa grave. Disposição=clamp(severidade*(.45+.25*persistence/100+.30*agency/100)*min1.25(1+min6(falhas)*.025+min48(investimento)*.002)*(1−min.8(barreiras))). Emoção pode prolongar pressão grave; falhas/idade têm limites.

Capacidade real normal=clamp(HP*(1−fatigue/150)); percebida=clamp(capacidade*(.6+courage/125)). Finish/attack com decisão ativa usam auditoria letal especializada; challenge_divinity exige causa grave, desenvolvimento mítico≥60 e pressão≥35; assume_local_office exige grupo escalado/responsabilidade e gates próprios; ações fortes não executam com capacidade<12, detenção ou rendição. Não há bônus automático de dano físico por pressão. As fórmulas integrais de agência, capacidade e inibidores estão no apêndice.

## Fome, sede, descanso, dano, cura e morte

Fome cresce2/h; sede2/h ou4 em D; fadiga1.2/h, todas limitadas100. Chegar a100 em fome OU sede causa dano `min6(2+starvation_hours//12)` por hora; o relógio de privação zera quando ambas voltam abaixo100. O dano real limitado ao HP entra em damage_by_origin e, para fome/sede/both, em recoverable_deprivation_damage. Comer reduz40; beber reduz45. Não é um teste simples “há comida na cidade, portanto come”: posse, conhecimento, preço, renda, distância, Need escolhida, intervalo de decisão e etapa de consumo são independentes.

Fome35–40 permite oportunidade de refeição com pressão relativamente baixa;40–60 cresce40+1.5*(fome−40),≥60 cresce70+1.5*(fome−60) até100. Reserva objetiva cobre24h e margem6h, máximo6; pressão inclui cobertura, oportunidade observada pagável, risco, idade e retorno da viagem. O prazo biológico simula até128h e rejeita soluções que não deixam o indivíduo vivo até adquirir/consumir. Estoque remoto não é lido como conhecimento grátis.

Sede≥25 cria Need; drink consome água própria, drink_well busca fonte conhecida em Town, drink_stream é caminho rural sem mercado. Poço consome estoque real da cidade; infraestrutura diária e capacidade de armazenamento não significam água infinita. Daily repõe somente dentro das regras/capacidade. `fill_water` recolhe para carregar, não bebe automaticamente. B03 permite repetição preventiva após falha; salvar água no inventário não garante sobreviver ao fechamento seguinte se o consumo ficou para outra decisão.

Sleep reduz fadiga12*horas e chama recuperação. Cura normal3/h, metade em privação severe,0 critical/starvation. Em casa sem oponentes, ledger de privação pode curar8/h com nível≤50,4/h≤70,1/h≤80,0 acima; o orçamento é max(cura normal,rápida), não soma. Tratamento atende dano físico primeiro; débito do ledger impede curar privação inexistente. Need recovery existe HP<80 e pode delegar estabilização a food/water antes de sleep. Fadiga reduz capacidade/aptidão e prioridades; não há morte de velhice modelada nem dano fatal diretamente por fadiga isolada.

Todas as mortes convergem para finish_death: privação classifica hunger/thirst/both no registro, combate pode carregar killer/weapon/intenção, self_harm usa causa própria abstrata quando elegível; explorar POI pode causar morte exploration, e desafio divino pode causar combat sem killer mortal. Encerra Goals/Needs/commitments e decisões do dono, remove do índice de vivos, mantém corpo/posses. EventBus atualiza censo uma vez, sucessão/relações/emoções/justiça/grupos/fé por seus consumidores; conhecimento não é universal. CharacterKilled ativa Aftermath. Morte de um deus é outra entidade/fluxo, não baixa o censo mortal como se fosse um residente.

## Economia: donos, preço e conservação

Dinheiro tem dono: Character.money, Town.money, Kingdom.treasury, Faction.money, Group.money, Policy.money e Town.abstract_money separado. Kingdom não possui campo money. Cada reino começa com treasury2000; Economy.daily adiciona floor(abstract_population/100) ao saldo abstrato como fonte monetária explícita de trabalho abstrato, registrada em MoneySourceAbstractWork. Não é transferência de um pagador persistente: a fronteira dessa fonte de moeda deve ser declarada, não ocultada sob a palavra salário. Compra transfere moeda Character→Town e item Town→Character; venda faz o inverso, com desconto e saldo real. Salário Town→Character usa wage_credit em sextos (restos não são moedas adicionais). Política reserva Town→Policy, paga Policy→worker, devolve sobra. Contribuição/dues fazem Character→Group/Facção; transporte move carga real. Morte mantém dinheiro/posses no cadáver; não é sumiço de moeda nem distribuição automática.

Preço base e cotação por estoque (inclusive cada unidade de lote) estão em Economy.market_value/buy_price/sell_price/quote. Compra observada só no mercado registra preço/estoque/turno; intenção pode caminhar sem conhecer preço remoto. Sem renda há trabalho, treino/temporário, venda de excedente, coleta, ajuda ou roubo conforme conhecimento/gates e personalidade; nenhuma dessas opções é garantida. Crédito salarial e grain_credit são unidades distintas e não devem ser somados como dinheiro. Relatórios diários e agregados não formam razão contábil histórico completo.

## Profissões, procura de trabalho, produção e carreira

| Ocupação | Local / input → output / limites | Pagamento e destino |
| --- | --- | --- |
| agricultor | workplace rural; trabalho gera grain2/h ou3 na especialização; cap240 | Produto→Town; crédito produzido*(6//rate), Town paga sexto convertido. |
| mineiro | workplace artesanal; iron2/h ou3 especializado; cap120 | Mesmo fluxo material/salarial; ferramenta não é um input consumido por hora. |
| lenhador | workplace artesanal; wood2/h ou3 especializado; cap120 | Produto Town e remuneração Town. |
| caçador | workplace rural; food2/h (a especialização padrão é grain/iron/wood); cap240 | Produto Town; não é comida automaticamente do caçador. |
| cozinheiro | mercado/taverna;2/3grain→1food com grain_credit inteiro em terços;3food/h; cap240 | Produto Town, salário por produção real. |
| ferreiro | workplace;2iron+1wood→1weapon por ação, cap8 | Insumos Town, arma Town; lote elapsed não cria horas retroativas de forja. |
| guarda/soldado | workplace válido, serviço/patrulha | Salário Town por horas; sem item produzido nessa ação. Captura exige conhecimento separado. |
| comerciante | workplace/serviço; transporte institucional é outro caminho | Salário Town; não existe comércio interlocal autônomo geral implementado por esse rótulo. |
| governante/conselheiro | workplace/serviço e administração separada | Salário Town; tesouro/decisão institucional não são dinheiro pessoal. |
| estudante / None | sem work remunerado genérico | None pode usar temporário; treino segue gates. Não existe emprego garantido pelo nome. |

Need work surge no horário8–18, money por baixa reserva; food/reserve pode oferecer work se comida conhecida é impagável. Um NPC não faz busca global de vagas: Economy.observe no mercado oferece dados frescos≤24h de estoque, temporário e treino. Goal.solutions remove work saturado/incompatível, adiciona vagas conhecidas; Utility penaliza distância2/passo e privação, recompensa diligence, e treino considera pressão financeira/custo/demanda. Salário esperado não é uma variável geral aprendida e comparada entre todos os empregos; o mecanismo prioriza alternativas existentes no mercado local. Pode não haver vaga/input/espaço/pagador, e a execução falha com razão explícita; fome/família/ação alternativa competem em decisões seguintes.

Trabalho temporário de preparo consome grão real e distribui o produto entre pagamento em comida e estoque. Distribuir refeições consome duas por unidade: uma paga trabalhador, outra população abstrata. Treinamento só cobre cozinha: aprendiz produz1food/h, ganha2sextos e conclui max12(36−diligence//5−8 se agricultor) unidades; abandono após168h sem prática. Não é árvore de carreira para toda profissão. ProfessionalDemand mede déficit; materializar exige déficit≥72h, cooldown, abstrato, dinheiro/insumos/instalação e ausência de candidato persistente adequado; transforma um residente abstrato em aprendiz, transfere12 do saldo abstrato, provisões da Town e preserva censo. Reposição profissional ampla é PARCIAL.

Produção conserva insumos na cozinha/forja/transporte; agricultura/mineração/caça/água são fontes modeladas por capacidade/ação/tempo e não esgotamento ecológico. Consumo abstrato agregado usa escala de moradores, não um estômago por cidadão invisível. Não interpretar “material finito em estoque” como modelo completo de energia/solo/minérios renováveis.

## Itens e propriedade

ItemService cria com ID/owner/origem/criador/qualidade/raridade e propriedades reais; inventários guardam quantidades. Transferência total altera dono, parcial divide stack; consumo debita/remove item conforme quantidade. Itens nomeados/importantes têm história/posição/uso seletivos; pilhas comuns não mantêm trilha por unidade consumida. Arma altera dano por damage/quality; tool e artefato podem carregar propriedades sem um ciclo universal de desgaste/fabricação. Food/water/grain/iron/wood têm consumo material específico. item_beliefs e lenda atribuída não são actual_properties: alguém acreditar em bônus não o cria.

## Relações, família e epistemologia

Grafo dirigido `(source,target,kind)`; value0–100, diplomacia−100–100; só reciprocal=True escreve duas direções. Espécies literais, valores iniciais e todos os sites de alteração/leitura estão no MAPA: afinidade_divina, amizade, autoridade_local, casamento, confiança, diplomacia, familiaridade, filho_de, lealdade, pai_de, pertence_a, representa_cidade, reside_em e residente_de. A materialização usa residente_de e migração usa reside_em; o censo autoritativo usa town_id/resident_ids, não a fusão desses rótulos. Divinity.relations pode guardar valores negativos enquanto a aresta afinidade_divina é truncada pelo Graph em0, uma diferença de representação que impede usar os dois como escala idêntica. Amizade/confiança podem divergir em direção; parentesco usa casamento/pai_de/filho_de. Siblings não têm ciclo próprio de relações derivadas/nascimentos; família funcional consulta arestas explícitas. Family care/search nasce de observação e notícia; morte objetiva só produz luto em quem aprende com vínculo suficiente. Conhecer alguém não garante confiar, e confiar em emissor para compartilhar não é necessariamente a confiança do receptor para acreditar.

Truth=WorldState e eventos objetivos; Fact=representação recebida, com confiança/fonte/contexto; Observation=estado visto com data; Memory=registro curto; Belief=atribuição religiosa/mítica; Reputation=interpretação subjetiva acumulada por fatos; conhecimento de local e de rota são estruturas distintas. EventRecorder publica; Knowledge observa testemunhas e participantes, learn aplica confiança e dispara listeners de forma síncrona. Não se reavalia o mundo remoto para corrigir automaticamente uma crença.

Conhecimento é limitado64 Facts e32 memórias, com causas protegidas por Agency/processamento em curso; aplicada contribuição/reputação não duplica ao reouvir o mesmo fato com menor confiança. Melhoria de confiança aplica diferença, não a história inteira de novo. Gossip a6h usa snapshot, sorteia contato na célula ou quatro adjacentes e um fato compartilhável; confiança do emissor permite compartilhar, do receptor classifica trusted/known/rumor/untrusted. Teto transmitido=min(confiança anterior,80/60/30/10); direto100. Não há recomposição automática de certeza por retransmissão.

Gossip conserva kind, actor, target, local e turno do Fact: muda fonte/confiança, não sorteia distorção textual nem cria uma autoria falsa. Informação velha é filtrada por idade/Need, local já buscado, observação mais nova e melhoria de confiança, não por um TTL universal de toda crença. Verdade objetiva, relato enfraquecido, informação desatualizada e interpretação/atribuição religiosa equivocada existem em graus diferentes; não há um campo universal truth=True/False nem um ciclo geral de falsas acusações fabricadas. Mentira deliberada geral com NPC escolhendo fabricar uma proposição falsa e manter versões é AUSENTE como ciclo completo; rumor não é automaticamente mentira. Falsa divindade/lenda atribuída é crença subjetiva PARCIAL, sem criar entidade divina objetiva.

## Crime, investigação, justiça e combate

Crimes concretos incluem furto de estoque/indivíduo e violência/ameaças/morte julgadas pelos filtros de justiça; incursão institucional pode ser legal/tolerada/restrita/ilegal conforme jurisdição e evidência conhecida. Furto transfere item real, não spawna recompensa. Greed positiva, honesty fortemente negativa e contexto de fome/estoque/acesso favorecem steal; security precisa conhecer, chegar e vencer a competição de Need antes de prender. Assim milhares de furtos podem coexistir com poucas capturas sem provar falha em EventBus: medir cada fronteira crime→testemunha→Fact→guarda→busca→encontro→captura.

Investigation parte de fatos/pistas conhecidos; pista guarda lugar/data/fonte/confiança/especificidade/direção/related_fact. Search/ask podem avançar, descartar local pesquisado ou deixar compromisso esperando informação. Wanted não é onisciência: record guarda known_by, local, severidade, confiança, evidência e prazo; expiração/detenção/soltura são distintas de inocência. Denunciar ao culpado é filtrado no caminho atual por alvo/fato; não se assume a presença de um bug antigo sem reproduzi-lo.

Conflito enumera confront/warn/threaten/demand_return/insult/apologize/return_stolen/forgive/calm, attack/defend/flee/withdraw/surrender, protect/intervene/call_help/alert, pursue/capture e first_aid/seek_treatment. Alvos precisam estar acessíveis e conhecidos; fuga move, rendição restringe, captura requer autoridade/evidência/oportunidade. Trégua/timeout têm regras próprias. Dano=`(4+min12(weapon.damage*(.5+quality/200)))*(.5+HP/200)*(1−injured/250)` com multiplicador mítico treinado até15%, variação inteira±2, defesa*.45 e mínimo1; coragem influencia decisão, não multiplica dano diretamente.

## Letalidade: querer, buscar, atacar e finalizar

Modos reais são reactive_threat, retributive, protective, instrumental, moral_punishment e hedonic. Cause usa fatos próprios com autoria/confiança, dano confirmado, perdas próximas e objetivo instrumental; humiliation repetida não equivale a qualquer insulto isolado. Death_seeking é trajetória derivada, não sétimo modo: exige afinidade/mortes positivas/sadismo/inibição sob gates próprios. A fórmula integral de todos os modos e limiares consta no apêndice.

Evaluate calcula instigação, vengefulness, emoção dirigida limitada pelo agravo, compromisso, sadismo, afinidade e reparação falha; subtrai compaixão, honestidade, medo, risco, vínculo, autoridade/testemunhas, autoria incerta e alternativas não letais. Pressão<40, falta de causa grave/confiança≥60 e inibidores bloqueiam adoção. Decisão persistente ativa não vira amnésia ao alvo sair da célula; mantém fontes/intensidade/ruminação/compromisso/estado. Capacidade/local limitam execução sem apagar desejo. Buscar requer pista/rota/provisões; atacar requer contato e competição; finalizar requer incapacidade, acesso e decisão ativa.

Terminal compara finish/spare/capture/help/withdraw. Ameaça defensiva removida pela incapacidade reduz muito finish e aumenta spare; motivos não defensivos podem continuar. Captura tem95+honesty*.1 se guarda com caso; ajuda exige food+water; vínculo/compaixão inibem finish; medo favorece retirar. Winner é o max real com desempate por chave, usado diretamente, não uma nova rolagem de moral. Finish válido mata sem nova rolagem de dano. Sem oportunidade/decisão não existe kill arbitrário por Utility-base.

Aftermath usa intenção, justificativa percebida, vulnerabilidade, vínculo, testemunhas, sadismo, crença do autor e afinidade. Registra guilt/shame/fear/relief/pride/pleasure/fascination/numbness/grief/moral_conflict, mortes positivas e antes/depois de afinidade. Feedback conhecido pode reduzi-la; decaimento tem janela. Mesmo gesto não produz o mesmo sentimento em todos. Os appraisals retidos são4 por pessoa, kill_facts8; não equivalem a histórico emocional integral.

## Grupos, propostas e governo

Group é causa compartilhada com membros/leader, conhecimento/atividade/pressão/plano/investimento. Criar, conhecer, ingressar e reunir são etapas diferentes; Institutions.search_groups exige conhecimento/compatibilidade antes de uma alternativa join. Recusa pode resultar de causa, distância, autonomia, confiança ou limite; não se presume que todo grupo mundial seja visível. Churn, líder morto, dissolução e registro de origem persistem de modo limitado. Reunião exige presença física; alto número de membros não prova encontros regulares.

Proposta reúne pessoas/grupos/facções por chave de jurisdição/setor/objetivo, apoio único e fontes; reuso evita duplicatas equivalentes. Apoiar não é entregar; representante precisa chegar ao prefeito/mercado, transmitir e depois receber/devolver resposta. Quadro público mantém respostas limitadas e conhecimento local; prefeito não lê status remoto como notícia. Decisão considera pressão, urgência, apoio vivo, idade, visibilidade e crise local, personalidade e orçamento. Scores approve/partial/reject/defer/ignore são persistidos no resultado; sem orçamento aprovação vira defer. Sucessão preserva o quadro, mas vários fluxos ainda dependem da pessoa escolhida.

B02 interrompe a ligação rejeição conhecida→responsável político→tomada de cargo: o bloco que escreveria responsibility_id está depois de um retorno. B06 pode misturar contexto grupo/facção. A antiga Society.material existe paralela à política material atual; sua acessibilidade precisa ser lida pelo grafo e não inferida de seu nome. O código legado que sai cedo em political_pressure não é uma segunda política ativa.

## Políticas: cada setor

Policy reserva2–16 moedas (parcial até8), exige8 etapas (parcial4), trabalhador apto/conhecedor/local, paga1 por etapa e devolve sobra na conclusão; budget=money+spent+refunded. Falhar pode produzir stalled/barreira, não desaparece o orçamento. A existência de Policy não contrata automaticamente qualquer profissional.

| Setor | Worker/local | Inputs/efeito/limites e conclusão |
| --- | --- | --- |
| WATER | mineiro/lenhador/ferreiro/agricultor no mercado |1wood+1iron/etapa; a cada2 etapas +20/dia,+40armazenamento; não cria água instantânea. |
| FOOD | cozinheiro/agricultor/caçador |prepare até4rações, grão/crédito real, espaço≤240. |
| PROCESSING | cozinheiro |Mesmo caminho de preparo; não é indústria multietapas genérica. |
| EMPLOYMENT | elegível temporário |Mesmo primeiro caminho de preparo: diversidade de emprego PARCIAL. |
| WEAPONS | ferreiro |2iron+1wood→weapon real, pagamento/subsídio separado dos insumos. |
| RAW_MATERIAL | mineiro/lenhador/agricultor no workplace |Chama work existente1h; produção+salário regular exigidos; subsídio1 sai da Policy. |
| SECURITY | guarda/soldado no mercado |Observa/patrulha, paga e fatiga; não garante impedir crimes. |
| TRANSPORT | comerciante |3grain/wood/iron reais; destino conhecido no mesmo reino, rota/provisões; atribuição não paga até certificado de chegada e entrega; carga perdida bloqueia. |
| cult_recognition | objective especial, elegibilidade herdada do setor |Registra culto reconhecido em Town.policies; não cria comida, divindade ou conhecimento universal. |

Barreiras incluem money<1, fatigue≥95/HP<30, recursos/armazenamento, input, rota/carga/provisões, chegada não confirmada/carga perdida e serviço especializado indisponível. Se trabalhador nunca conhece a política ou a Need perde prioridade, policy_work nem é chamado e nenhuma PolicyBlocked precisa aparecer: essa é uma lacuna entre notícia e trabalho.

## Facções, formalização e capacidade institucional

Duas facções iniciais têm líder, sede física, estoque real e dinheiro; novas derivam de grupos/ocupação/contribuições sob limites globais. A via meeting exige investimento≥4, idade≥168h,≥3membros e2presentes com dinheiro>15 antes da função de score. Institutions.formalization calcula idade/falhas/reuniões/presentes/contribuições, score≥65,≥3presentes e fundos≥4; found_faction acrescenta limite mundial/liderança/capacidade. Access.formalize_organization ignora parte desses gates (B04). Portanto eles não são invariantes globais de toda facção.

Ingresso exige conhecimento/contato/termos, custo de autonomia/risco/dues e benefício percebido de comida/água/proteção/renda/companhia/treino. Reconsideração por fadiga≥85 ouHP<45 não é recusa definitiva; independência≥90 pode recusar. Convites podem permanecer condicionados; morte os expira por motivo, não simples prazo. Só existir estoque na HQ não entrega água ao recruta distante.

Capacidades derivam de membros vivos presentes abastecidos (food+water,HP≥30), guardas, HQ e recursos. Patrol/guard/investigate requerem guarda apto; escort exige≥2abastecidos; train≥2guardas; produce requer profissão; trade comerciante e saldo≥2; explore≥2 e mineiro/caçador; occupy≥2 e HQ. Há ações concretas institutional_supply/purchase/patrol/support/raid/response, contribuições, assignment/preparo e recrutamento, mas nem todo booleano possui ciclo independente completo. Treino institucional geral, comércio complexo, contratos remunerados de escolta e custódia multidepósito são PARCIAIS/AUSENTES como ciclos.

Legalidade por cidade deriva de ações/evidências recebidas e valores/ideologia: tolerância, restrição e ilegalidade não mudam automaticamente por toda parte. Resposta institucional depende de líder/membro conhecer o fato, capacidade/material e escolha. Uma ação de suprimento pode preceder assignment e ocultá-lo naquela enumeração; B05 é a divergência de produto. Fontes/Needs concorrentes e sobrevivência da liderança são gargalos concretos.

## Fé, deuses, audiência, contrato, apoteose e mito

Geração cria os deuses definidos em Faith.GODS, crença/devoção local e potencial mítico raro; acreditar num mortal não o insere em world.divinities. Faith, DivineRelations, ReligiousHealth, Renown e Access compõem um fluxo, não uma mente onisciente. Deus conhece mensagens/fatos por oração/atividade/presença/relatos e fontes limitadas; composição religiosa objetiva só vira conhecimento pela cadeia de relatos permitida. Presença regional≠corpo acessível. Alvo e intervenção dependem de informação, domínio/valores, afinidade, energia, cooldown e motivo.

Mortal precisa motivo, lugar sagrado conhecido, rota, provisões, chegada e rito; Access.audience, não DivineRelations.audience, decide a audiência. Exemplos de gates: favor≥30,devoção≥80,honor do deus≥50,energia≥45 e cooldown72; audiência custa10. Manifestação forte exige motivo/favor/energia adicionais (favor≥60,energia≥55, custo25), duração/local; DivineRelations tem também avaliação e manifestação por mensagens, com funções/canais próprios no apêndice. Não unir esses dois caminhos como se compartilhassem todo limiar. Contrato exige condições/oferta (inclui favor≥40 e feitos≥2 no caminho), conhecimento e aceitação; obrigação/mensagem de quebra não é lida globalmente por simples estado objetivo.

Divine death requer deus vivo, acesso físico válido a manifestação e capacidade mítica/circunstância; apoteose é posterior e separada, essência acessível e desenvolvimento/gates, cap12divindades. Não exigir ocorrência natural em300h. Renown usa feitos conhecidos e alcance, pode nomear/epitetar/atribuir lenda a item; mythic_trait é potencial, mythic_development depende de treino; item_beliefs não altera automaticamente o dano real. Saúde religiosa distingue followers/devoted/cultists/actors, snapshots e crises, mantendo censos objetivos e percepção local separados.

## Geografia, rotas, Journey, migração e POIs

World map e mapas locais usam Location(map_id,x,y), Town e Kingdom com limites e posições; Navigation resolve passo local/portais, Geography conexões. Route guarda origem/destino/distância/tempo/terreno/perigo/condição/tipo/toll/uso. Conhecer Town/POI não dá rota; RouteKnowledge tem direção,confiança,fonte,data/custo aprendido. Fontes incluem geração local, viagem, pergunta/relato, encontro e expedição. Plan percorre grafo conhecido, não GPS de todos os lugares; dados objetivos podem bloquear execução.

Journey guarda origem/destino,rotas/nós,motivo,início,modo/guia,leg/offset,pausa/provisões/história. Begin exige caminho/acesso e abastecimento; step consome tempo/provisões/movimento, pode pausar/falhar/retomar; arrival emite certificado. Seguir/escort usa guia/caminho conhecido e continuidade do grupo, sem teleportar por vínculo. Ausência de ocorrência natural de escolta não é bug.

Migração de NPC reutiliza Journey mas confirma mudança de town_id/home/workplace/resident_ids e censos; visitar não muda a residência do NPC. Para o jogador, Navigation.enter atualiza town_id como referência da localidade atual, e ele não compõe o censo de residentes: não interpretar esse campo exatamente como residência de NPC. POI inclui geração, descoberta/rumor/routeknowledge, mapa interno, exploração/perigo/estoque/restos/história, claim/occupation/HQ; o estoque é do ponto/facção, não de todo visitante. Não há exploração de dungeon completa só por existir depth.

## População, jogador e Quests

Persistent_alive+abstract=total_living por Town; mortos continuam personagens/posses, counted_deaths impede dupla baixa. Register retira um abstrato e adiciona um residente; materialização não é nascimento nem expansão grátis do mundo. Não há nascimento/morte individual/sociologia completa dos abstratos; idade biológica e envelhecimento não são campos de Character nem causas naturais de morte implementadas. A escala abstrata de consumo/produção é agregada; não atribuir uma história individual a cada residente invisível.

Engine.execute traduz comandos, usa _finish/_action e os mesmos serviços; ação válida avança hora, consulta/ação inválida em geral não. Contudo diálogo/algumas consultas de candidatos podem ter efeitos informacionais: não anunciar todo método de apresentação como puro. Jogador não é decidido por GoalSystem, mas sofre fisiologia igual. QuestSystem pode criar/listar/aceitar/abandonar/reconciliar pedidos ligados a Need e ajuda material/pessoal; sem jogador esta campanha mede só rotinas chamadas, não teste natural completo de aceitação/entrega. Todas as ramificações de CLI/Quest estão no MAPA e fontes, sem implementação adicional.

## Persistência, validação, limites e desempenho

encode inclui dataclass `$type`, dicionário `$dict`, tupla `$tuple`, listas e primitivos; decode aceita apenas TYPES de models. Envelope exige format_version1 e rules_version atual, world deve ser WorldState compatível, validate e restauração RNG precisam passar. GENERATION_VERSION é constante do código/seed; WorldState e o envelope do save não armazenam generation_version nem GenerationConfig completos. O manifesto desta auditoria preserva ambos. Não há migração automática do esquema. Escrita usa temporário no destino, flush+fsync+os.replace e limpeza; serviços/bus/índice/caches são reconstruídos.

B01 é uma limitação real da continuidade: serialização por valor não preserva identidade compartilhada de contexto/lista. Não afirmar que todo load diverge: o teste básico de continuidade passou, e o controle específico de alias demonstrou quando diverge. Queries Goal.solutions e algumas avaliações podem alterar planos/diagnósticos; visualizador não pode chamá-las como leitura passiva.

Todos os invariantes emitidos pelo validador, thresholds embutidos, caps nomeados, ações e testes estão no MAPA. Cobre referências/IDs/mapas, posse/quantidade/owner, relações, censo, ledgers, políticas/orçamento, conhecimento/rotas/Journey e estados. Não valida toda causalidade histórica nem todos os ciclos econômicos. History seletiva não tem teto geral equivalente ao buffer events256; conflitos/fatos/retornos imediatos podem crescer pressão de memória. Grupos, facções, Needs/diagnósticos, crenças e histórias específicas possuem limites distintos: ler constantes e guardas, não supor limite global único.

O custo medido desta auditoria inclui sys.setprofile, snapshots e amostragem; não é benchmark do motor sem observador. A/B prova neutralidade no cenário curto, não ausência matemática de todo risco de instrumentação. Amostragem/retentores têm limites e não preservam a experiência completa de cada habitante.

'''
    return text

FORMULAS=[
 'engine.Engine.step','justice.JusticeSystem.tick','society.SocietySystem.tick','institutions.Institutions.tick','faith.FaithSystem.tick','generation.GenerationConfig.validate','generation.seed_number','generation.generate_world',
 'society.SocietySystem.bootstrap','faith.FaithSystem.bootstrap','geography.Geography.bootstrap','access.AccessActions.bootstrap','institutions.Institutions.bootstrap',
 'needs.NeedSystem.ensure','needs.NeedSystem.finish','needs.NeedSystem.refresh',
 'personal.PersonalNeeds.on_fact','personal.PersonalNeeds.refresh','personal.PersonalNeeds.priority_modifier',
 'utility.evaluate','goals.GoalSystem.solutions','goals.GoalSystem._evaluate','goals.GoalSystem.choose','goals.GoalSystem.decide','goals.GoalSystem.preventive_choice',
 'feeding.FeedingSystem.decision_interval','feeding.FeedingSystem.reserve_target','feeding.FeedingSystem.reserve_pressure','feeding.FeedingSystem.survival_margin','feeding.FeedingSystem.estimate',
 'recovery.RecoverySystem.recover_hp','economy.Economy.market_value','economy.Economy.buy_price','economy.Economy.sell_price','economy.Economy.quote','economy.Economy.wage','economy.Economy.daily',
 'professions.ProfessionSystem.work','professions.ProfessionSystem.train','professions.ProfessionSystem.can_materialize',
 'agency.AgencySystem.profile','agency.AgencySystem.adopt','agency.AgencySystem.refresh','agency.AgencySystem.adjust',
 'action_pressure.ActionPressureSystem.world_pressure','action_pressure.ActionPressureSystem.disposition','action_pressure.ActionPressureSystem.assess',
 'conflicts.ConflictSystem.terms','conflicts.ConflictSystem.candidates','conflicts.ConflictSystem.execute','conflicts.ConflictSystem.intent_scores',
 'lethal_decisions.LethalDecisionSystem.cause','lethal_decisions.LethalDecisionSystem.evaluate','lethal_decisions.LethalDecisionSystem._consider','lethal_decisions.LethalDecisionSystem.refresh','lethal_decisions.LethalDecisionSystem.action_audit','lethal_decisions.LethalDecisionSystem.terminal',
 'terminal_combat.TerminalCombat.opportunity','terminal_combat.TerminalCombat.execute','aftermath.AftermathSystem.on_kill',
 'justice.JusticeSystem.refresh','justice.JusticeSystem.capture','investigation.InvestigationSystem.candidates',
 'society.SocietySystem.pressure','society.SocietySystem.refresh','society.SocietySystem.candidates','society.SocietySystem.react','society.SocietySystem.meeting','society.SocietySystem.found_faction',
 'institutions.Institutions.collective_candidates','institutions.Institutions.acceptable_group','institutions.Institutions.propose','institutions.Institutions.submit','institutions.Institutions.pressure','institutions.Institutions.decision_scores','institutions.Institutions.policy_work','institutions.Institutions.membership_scores','institutions.Institutions.capabilities','institutions.Institutions.formalization','institutions.Institutions.faction_candidates',
 'faith.FaithSystem.candidates','faith.FaithSystem.divine_assessment','faith.FaithSystem.intervene','faith.FaithSystem.divine_death','faith.FaithSystem.apotheosis',
 'divine_relations.DivineRelations.receive','divine_relations.DivineRelations.assessment','divine_relations.DivineRelations.manifest',
 'access.AccessActions.candidates','access.AccessActions.audience','access.AccessActions.manifest','access.AccessActions.physical_access',
 'geography.Geography.connect','geography.Geography.plan','geography.Geography.begin','geography.Geography.step',
 'migration.MigrationSystem.candidates','emotions.EmotionSystem.update','emotions.EmotionSystem.support','emotions.EmotionSystem.repair','quests.QuestSystem.respond','quests.QuestSystem.reconcile',
 'goals.GoalSystem._execute','faith.FaithSystem.execute','access.AccessActions.execute','institutions.Institutions.execute','society.SocietySystem.execute','engine.Engine.execute']

def event_catalog(inv,metrics):
    text='## Catálogo integral de emissões e consumidores\n\n'
    text+='Cada site de emissão está abaixo; expressões dinâmicas são mantidas como código, não renomeadas como eventos observados. Actor/target/context são os argumentos da chamada. Quando há wrapper, seguir sua política e a chamada final. Um mesmo kind pode ter vários contextos/historical/testemunhas: não existe um único esquema uniforme por nome.\n\n'
    text+=table(['Emissor / linha','Kind(s) / template','Chamada completa'],[(x['symbol']+':'+str(x['line']),x['kinds'] or x['kind_expression'],x['call']) for x in inv['events']])
    text+='### Esquema efetivo por site: actor, target, contexto, retenção e conhecimento\n\n'
    text+='O histórico de rotina retém256 eventos; historical=True também vai a history sem esse cap. Todo evento publicado pode gerar Fact para testemunhas/participantes vivos pelo mesmo Knowledge.observe. Throttle não é propriedade uniforme do kind: guardas abaixo são locais ao emissor; condições de chamadores e retorno anterior precisam da cadeia de fonte. Consumidores listados são compatíveis com o nome/filtro estático, não prova de efeito em cada testemunha.\n\n'
    rows=[]
    trees={}
    for item in inv['files']:
        tree=ast.parse((ROOT/item['path']).read_text())
        parents={c:p for p in ast.walk(tree) for c in ast.iter_child_nodes(p)}
        trees[item['module']]=(tree,parents)
    for site in inv['events']:
        fn=next(f for f in inv['functions'] if f['symbol']==site['symbol'])
        node=ast.parse(site['call'],mode='eval').body
        args=[ast.unparse(a) for a in node.args];kwargs={k.arg:ast.unparse(k.value) for k in node.keywords}
        def value(key,index,default='None'):
            return kwargs.get(key,args[index] if len(args)>index else default)
        receiver=site['receiver'];wrapped=receiver=='self.emit' and fn['module'] in ('society','institutions','access','geography')
        agency=receiver.endswith('.event');lethal=receiver=='self.emit' and fn['module']=='lethal_decisions'
        if wrapped:
            actor=(args[1] if len(args)>1 else 'p')+'.id';target=value('target',2)
            context=kwargs;historical='True';witnesses='presentes em '+(args[1] if len(args)>1 else 'p')+'.position + participantes'
        elif agency or lethal:
            actor=(args[0] if args else 'p')+'.id';target='None (target dirigido fica no context)' if lethal else 'None'
            context=kwargs;historical='True';witnesses='somente autor + participantes mortais se houver; evento privado ao ator'
        else:
            actor=value('actor_id',2);target=value('target_id',3);historical=value('historical',5,'False')
            context=value('context',7,'{}');witnesses=value('witnesses',6,'presentes em location (ou nenhum se None)')+'; soma actor/target mortais'
        tree,parents=trees[fn['module']]
        original=next((n for n in ast.walk(tree) if isinstance(n,ast.Call) and n.lineno==site['line'] and ast.unparse(n)==site['call']),None)
        guards=[];child=original;parent=parents.get(original)
        while parent is not None:
            if isinstance(parent,ast.If):
                side='else' if child in parent.orelse else 'if'
                guards.append(side+' '+ast.unparse(parent.test))
            if isinstance(parent,(ast.FunctionDef,ast.AsyncFunctionDef)):break
            child=parent;parent=parents.get(parent)
        kinds=site['kinds'];consumers=['knowledge.KnowledgeSystem.observe (*)']
        for sub in inv['consumers']:
            if '*' in sub['kinds'] or set(kinds)&set(sub['kinds']):consumers.append(sub['handler'])
        for f in inv['functions']:
            if any(set(kinds)&set(x['values']) for x in f['event_checks']):consumers.append(f['symbol'])
        rows.append((site['symbol']+':'+str(site['line']),kinds or site['kind_expression'],actor,target,context,
                     historical+'; events256'+(' + history quando True' if historical!='False' else ''),list(reversed(guards)),witnesses,sorted(set(consumers))))
    text+=table(['Site','Kind/template','Actor','Target','Contexto','Persistência/historical','Guardas de emissão / throttle local','Quem pode receber Fact','Consumidores estáticos compatíveis'],rows)
    text+='### Políticas dos wrappers (fonte integral)\n\n'
    wrappers=sorted({x['symbol'] for x in inv['events'] if x['symbol'].endswith(('.emit','.event'))})
    for symbol in ['events.EventRecorder.emit','knowledge.KnowledgeSystem.observe',*wrappers]:text+=source(symbol,inv)
    text+='### Inscrições diretas de EventBus\n\n'+table(['Arquivo/função / linha','Handler e filtro'],[(x['symbol']+':'+str(x['line']),x['call']) for x in inv['consumers']])
    text+='### Filtros adicionais de consumidores de Event/Fact\n\n'+table(['Consumidor','Linha','Condição'],[(f['symbol'],c['line'],c['expression']) for f in inv['functions'] for c in f['event_checks']])
    text+='### Kinds efetivamente emitidos nas 300h\n\n'
    text+=table(['Kind','Emissões','Cadeias reais de origem'],[(k,n,metrics['event_sources'].get(k,{})) for k,n in sorted(metrics['events'].items())])
    return text

def observability(inv,metrics,manifest,systems):
    text='''# OBSERVABILIDADE — registros atuais e causalidade perdida

Esta é uma especificação de dados para inspeção futura; não implementa frontend nem instrumentação permanente no núcleo. A=explicável integralmente no escopo indicado pelo registro padrão; B=parcial; C=exige observador durante a ocorrência; D=informação já perdida após a ocorrência. A/B/C/D não são notas de qualidade do comportamento nem garantias de que todo evento do módulo foi observado.

## Matriz por sistema

'''
    text+=table(['Arquivo / sistema','Classe','Completude','Limitação'],[(s['module']+' / '+s['system'],s['observability'],s['completeness'],s['limitation']) for s in systems])
    text+='''## Onde a cadeia causal se rompe

| Fronteira | Registro existente | Informação ausente / consequência |
| --- | --- | --- |
| STATE→percepção | Estado atual, algumas observações datadas | Snapshot de posição/estoque/HP/dinheiro e versão de conhecimento em cada decisão. Estado final não prova insumo anterior. |
| Fact→Need | source/context em vários Needs | Referência tipada uniforme ao fato, confiança usada e regra de criação; ID de Need reutilizado não identifica episódio. |
| Need→prioridade | priority atual e diagnósticos limitados | Lista completa de todas as Needs, modificadores, ranks e status antes de cada seleção. |
| Produção de alternativas→gates | Código e alguns motivos/diagnósticos | Todas as opções consideradas/omitidas e razão por gate; lista vazia não diz qual pré-condição faltou. |
| Utility→winner | Goal.score e debug opcional | Scores/terms de todas as alternativas, ordem, variação sorteada e substituições por continuidade/preparação. |
| Goal→execução | Goal/outcome atual e eventos parciais | ID único de tentativa/ação, origem da Need/Goal, horas caminhadas/produzidas, versão do mundo e condição revalidada. |
| Execução→evento | kind/actor/target/location/context | parent_event, need_episode_id, goal_id, action_attempt_id, política de mutabilidade e esquema de cada contexto. |
| Evento→saber | witnesses e Facts ainda retidos | Recibo de aprendizado imutável por receptor, hora/confiança/canal/quem contou; witnesses não garante todas as reações. |
| Saber→consequência | Fontes em vários subsistemas | Deltas de estado, evento causal e contribuição diferencial; eventos correlacionados não provam causa. |
| Histórico→save | history seletiva e buffer events256 | Evento cotidiano expulso, memória32/knowledge64, alias de contexto mutável B01; timelines completas não se recuperam. |

## EventBus e EventRecorder: o que fica

EventBus é síncrono, em memória; subscriptions/handlers e índice espacial são reconstruídos. Recorder aloca ID/turn, acrescenta actor/target mortais como observadores, usa witnesses explícitas ou presentes no local, grava events (últimos256), history se historical=True, incrementa métrica e publica. Histórico não implica Fact universal: quem não testemunhou precisa de canal posterior. Evento com witnesses=[] ainda inclui actor/target mortais, se fornecidos; eventos de censo só objetivos podem não ter observador mortal.

Não existe throttling universal no Recorder: módulos aplicam cooldown/limite de exemplos antes de emitir. Métricas como NPCDecision, PersonalOutcome, NeedCreated, pressão/produção/cura podem existir sem Event. Descrição textual não substitui contexto tipado. B01 mostra que contexto pode conter referências mutáveis: nem history nem Fact são snapshots garantidamente imutáveis. Aftermath inclusive adiciona appraisal ao evento de morte durante publicação. O observador captura o contexto depois de emit retornar (após listeners), não antes da publicação; esse momento é declarado.

## Controle A/B e método externo

'''
    text+=table(['Controle','Resultado'],[(k,v) for k,v in manifest['control'].items()])
    text+='''sys.setprofile acompanha chamadas/retornos reais, sem substituir função do motor, sem RNG do mundo, sem novas ações/fatos e sem recomputar solutions/Utility para explicar. A amostragem bottom-k usa SHA256 de categoria/NPC/hora/ação; rings guardam duas decisões recentes por NPC para mortes e agregados contam o restante. O teste de8h em cada lado confirmou igualdade serializada de mundo, RNG, history e events no cenário de controle. Os 300h foram um único mundo novo, sem jogador, seed fixa declarada e histórico inicial0.

Limitações verificadas do observador:

- Não cobre cada valor local temporário de todo gate nos produtores. Quando razão individual não é observável, o trace a marca; não preenche com hipótese.
- Campos escalares de emoções são snapshots; coleções aninhadas rasas em state.emotions foram excluídas dos relatos históricos porque poderiam refletir alteração posterior. Não se usa esse dado para justificar a decisão antiga.
- Relações com alvo e known_target obtidos no fim da decisão são explicitamente estado posterior, não os vínculos de entrada. IDs de conhecimento iniciais não são cópia integral de todos os Facts.
- terms de Utility e retornos especializados são os calculados; o draw de desempate não é copiado. Reproduzir a seed não substitui preservar aquele draw/versionamento no futuro.
- Audiência é AccessActions.audience; o tag especializado antigo apontava para DivineRelations.audience, que não existe. Chamadas reais/eventos gerais de audiência são contados, mas não há captura especializada completa de todos os seus locais internos.
- Contagem de aprendizagem é operações learn aceitas, podendo incluir melhor confiança para o mesmo receptor; não significa pessoas únicas. first_people é amostra≤6.
- Os eventos são capturados no retorno de emit, após listeners. Cascatas aninhadas podem retornar antes do evento pai; ordem da lista de captura não é necessariamente a ordem de alocação. IDs/turn/emitter_stack estão preservados, mas faltam parent_event_ids uniformes.
- O contador monetário bruto omitiu Kingdom.treasury ao procurar money; a análise final reconcilia saldos reais com a fonte explícita MoneySourceAbstractWork. Tesouros intermediários não foram preservados e não foram preenchidos por inferência.
- Disponibilidade/eligibilidade de trabalhador no fim não é conhecimento histórico de todos os candidatos. Relatório não atribui a posteriori esse conhecimento ao passado.
- Amostras têm limite por categoria, por evento e por cálculo raro; pools não formam amostra estatística representativa para estimar prevalência. Frequências usam os agregados, não a proporção dos traces.

## O QUE PRECISA SER REGISTRADO PARA O VISUALIZADOR

Usar observação imutável no momento de ocorrência, sem chamar produtores mutáveis de candidatos. Contrato mínimo sugerido de um registro de decisão:

```text
run_id, code/rules/generation_version, seed, generation_config
decision_id, actor_id, started_turn, closing_turn, lod, elapsed
state_version_before, own_state_before, perceived_state_before
knowledge_version, fact_ids + confidence/source used, observed_at
need_episode_id, need_id, kind/source/target/context, priority_terms/rank
alternatives_generated, alternatives_omitted + gate_id/reason/evidence
utility_inputs, terms, scores, random_tie_draws, raw_winner
continuity/preparation/substitution, final_winner, goal_id/status
action_attempt_id, destination/route, travel_hours, execution_hours
validation_gates_at_execution, success, failure_code, material_deltas
emitted_event_ids, event_parent_ids, state_version_after
learning_receipts(receiver, turn, channel, source_id, confidence_before/after)
```

| Tela futura | Dados necessários além do registro padrão |
| --- | --- |
| Timeline NPC | Identidade estável, residência/posição, episódios de Need, decisões/Goal, fontes conhecidas, emoções/compromissos e deltas de HP/posses. |
| Timeline cidade | Censo persistente/abstrato, estoques/fluxos com donos, preço/oferta por instante, prefeito/quadro/políticas, rotas e eventos locais. |
| Timeline grupo | Fundação com lista copiada, ingresso/saída/motivo, líder/sucessão, reuniões/presentes/investimento, conhecimento de proposta/resposta e pressão. |
| Timeline facção | Origem/formalização e gates aplicados, membros/sede/bens/dinheiro, capacidades com insumos, convites/termos recebidos, ordens/ação/legalidade por jurisdição. |
| Timeline item | ID e genealogia split/merge, criação/consumo/transferência, quantidade/proprietário/posição, uso real separado de lenda/crença. |
| Timeline religião | Belief individual e fonte, devoção/rito, conhecimento divino e afinidade, presença/manifestação/energia, audiência/pacto/obrigação e censo objetivo separado. |
| Cadeia causal | parent_event, source_fact, source_need_episode, goal/action IDs, regra/versionamento, contribuição de cada deliberação/efeito. |
| World According To NPC | Snapshot versionado do saber naquele instante, confiança, fonte/idade, observação distinta de truth, lugares/rotas/pessoas conhecidas e incerteza. |

Não inferir o que o NPC sabia de um save final nem mostrar censo objetivo como sua visão. Retenção pode manter snapshots espaçados + deltas/eventos compactos e índices por entidade, com caps declarados e links para evidências. É necessário corrigir futuramente a mutabilidade histórica antes de usar Event como verdade imutável; esta tarefa só registra o requisito. Dados privados ao ator (pensamentos/avaliações) não devem virar Facts públicos por exigência do visualizador.

'''
    text+=event_catalog(inv,metrics)
    write('OBSERVABILIDADE.md',text)

def clean_emotions(value):
    """Remove apenas dados históricos do observador cuja cópia era rasa."""
    if isinstance(value,dict):
        for key,item in value.items():
            if key=='emotions' and isinstance(item,dict):
                value[key]={k:v for k,v in item.items() if v is None or isinstance(v,(int,float,str,bool))}
                value[key]['nested_collections']='LACUNA: cópia rasa; histórico não utilizado'
            else:clean_emotions(item)
    elif isinstance(value,list):
        for item in value:clean_emotions(item)

def compact_json(value):
    return json.dumps(value,ensure_ascii=False,separators=(',',':'))

def state_brief(state):
    keys=('id','name','hour','alive','profession','lod','position','residence','hp','hunger','thirst','fatigue','money','food','water','local_food','local_water','recoverable_deprivation','starvation_hours','training','journey','failures')
    return {k:state.get(k) for k in keys if k in state}

def trace_report(traces,metrics):
    allrows=traces['decisions'];by=defaultdict(list)
    lethal_example=next((r for r in allrows if any(c['system']=='terminal' for c in r.get('calculations',[])) and any(c['system']=='lethal_decision' and isinstance(c.get('result'),dict) and c['result'].get('available') for c in r.get('calculations',[]))),None)
    for row in allrows:
        if row is lethal_example:
            by['lethal'].append({**row,'category':'lethal','observer_category':row['category'],
                 'curation_note':'Reclassificação editorial de cálculo letal realmente capturado; não é execução de finish nem uma oportunidade terminal comprovada.'})
        else:by[row['category']].append(row)
    selected=[];used=set()
    # Garante diversidade antes de preencher 50 posições com amostras restantes.
    for i in range(5):
        for category,rows in sorted(by.items()):
            if i>=len(rows):continue
            row=rows[i];key=(row['actor'],row['hour'])
            if key not in used and len(selected)<50:used.add(key);selected.append(row)
    text='''# DECISÕES REAIS — por que fez, não fez ou falhou

Dados da campanha única **Thalven-Radiografia55**,300h,sem jogador,histórico inicial0. São decisões capturadas enquanto o motor executava, sem reconsultar solutions nem recalcular Utility. A amostragem privilegia diversidade técnica; sua proporção não estima frequência no mundo. Horas são world.turn durante a decisão, antes do fechamento fisiológico. “Sem execução” pode significar que a caminhada consumiu o elapsed.

O estado de entrada precede refresh/percepção; a lista de Needs já é posterior ao refresh real. Fonte conhecida é amostra dos fatos ligados aos contextos. Relações e known_target coletados ao final são marcados como posteriores. Coleções emocionais que tiveram cópia rasa foram removidas, preservando só escalares. “ND” ou “LACUNA” significa que o observador não reteve o dado, sem preenchimento retrospectivo.

## Cobertura da amostragem

'''
    text+=table(['Categoria','Retidas','Apresentadas'],[(k,len(v),sum(r['category']==k for r in selected)) for k,v in sorted(by.items())])
    requested=['food','water','rest','money','work','career','family','social','crime','investigation','combat','lethal','religion','travel','migration','group','proposal','policy','faction']
    absent=[k for k in requested if k not in by]
    text+='Categorias sem trace de decisão retido: '+(', '.join(absent) if absent else 'nenhuma')+'. Conferir contadores de chamadas/eventos antes de concluir ausência: o mapeamento de categoria pode classificar o mesmo fenômeno em mais de uma fronteira, mas retém uma categoria por decisão.\n\n'
    text+='A categoria lethal inclui uma avaliação letal real reclassificada editorialmente de combat. A ação final foi attack; não houve finish. Agency.adjust pode consultar terminal() ainda com alvo acima de12HP e só aplicar o bônus terminal abaixo do limiar. Portanto uma tabela com choice=spare não prova que o NPC poupou um incapacitado naquela hora; verificar HP, função chamadora e evento de execução.\n\n'
    text+='## Por que fez / por que não fez / por que falhou\n\n'
    index=[]
    for i,row in enumerate(selected,1):
        before=row.get('state_before',{});after=row.get('state_after',{});winner=row.get('winner',{});need=row.get('selected_need',{})
        title=f"{i:02d}. {row['category']} — {before.get('name','NPC')} #{row['actor']}, h{row['hour']}: {row.get('action','sem seleção')}"
        index.append({'number':i,'actor':row['actor'],'hour':row['hour'],'category':row['category'],'action':row.get('action'),'success':row.get('execution',{}).get('success')})
        text+='### '+title+'\n\n'
        if row.get('curation_note'):text+='**Classificação:** '+row['curation_note']+' Categoria original do observador: '+row['observer_category']+'.\n\n'
        if need:
            text+=f"**Pressão escolhida:** `{need['kind']}` #{need['id']}, prioridade {need['priority']}, base {need['base']}, fonte `{need['source']}`, alvo {need.get('target')}. Motivo: {need.get('reason','ND')}.\n\n"
            text+='**Contexto preservado:** '+compact_json(need.get('context',{}))+'.\n\n'
        else:text+='**Sem seleção viável** no retorno de decide. Isso não demonstra ausência de todas as pressões: examinar Needs e avaliações abaixo.\n\n'
        text+='**Entrada:** '+compact_json(state_brief(before))+'.\n\n'
        text+='**Personalidade:** '+compact_json(before.get('personality',{}))+'. **Emoções escalares de entrada:** '+compact_json(before.get('emotions',{}))+'.\n\n'
        text+='**Conhecimento/locais de entrada:** '+compact_json({'known_places':before.get('known_places',{}),'known_towns':before.get('known_towns',[]),'route_knowledge_count':before.get('route_knowledge_count'),'knowledge_ids_before':row.get('knowledge_before',[]),'market_observation':before.get('market_observation',{})})+'.\n\n'
        text+='**Fatos-fonte retidos após percepção:** '+compact_json(row.get('known_source_facts',[]))+'.\n\n'
        text+=table(['Need','ID/alvo','Base→prioridade','Estado/fonte'],[(n['kind'],str(n['id'])+'/'+str(n.get('target')),str(n['base'])+'→'+str(n['priority']),str(n['status'])+' / '+str(n['source'])) for n in row.get('needs',[])])
        text+='**Alternativas/gates realmente vistos:**\n\n'
        for evaluation in row.get('evaluations',[]):
            text+=f"Need #{evaluation['need_id']} (`{evaluation['kind_at_evaluation']}`): {evaluation['input_count']} Solutions entraram em _evaluate; {evaluation['available_count']} saíram disponíveis. Entrada: `{', '.join(evaluation['input_actions'])}`.\n\n"
            if evaluation['discarded']:
                text+=table(['Opção','Alvo','Etapa','Motivo observado','Auditoria/feeding'],[(g['action'],g.get('target'),g['stage'],g['reason'],{'pressure':g.get('action_pressure'),'feeding':g.get('feeding')}) for g in evaluation['discarded']])
            else:text+='Nenhum descarte individual retido nesta avaliação. Opções nunca enumeradas não aparecem nesta tabela.\n\n'
            text+=table(['Ação','Alvo/destino','Score','Terms reais','Estimação/capacidade'],[(s['action'],{'target':s.get('target'),'destination':s.get('destination')},s['score'],s.get('terms'),{'feeding':s.get('feeding'),'action_pressure':s.get('action_pressure')}) for s in evaluation['available']])
        text+='**Escolhas intermediárias:** '+compact_json(row.get('choices',[]))+'.\n\n'
        text+='**Preparação/substituição posterior:** '+compact_json(row.get('preparations',[]))+'.\n\n'
        text+='**Winner final / Goal:** '+compact_json({'winner':winner,'goal':row.get('goal_after'),'suspended_before':before.get('suspended_goal'),'suspended_after':after.get('suspended_goal')})+'.\n\n'
        if need:
            unequal=[n for n in row.get('needs',[]) if n['id']!=need['id']]
            text+='**Por que outras Needs não foram executadas:** a fila prioriza emergência/priority/ID e para na primeira solucionável, sujeita à continuidade/preparo. Outras pressões retidas: '+', '.join(f"{n['kind']}#{n['id']}({n['priority']})" for n in unequal)+'. Não atribuir score global entre Needs.\n\n'
        ex=row.get('execution')
        if ex:
            text+='**Execução:** '+compact_json({'success':ex.get('success'),'result':ex.get('result'),'goal_at_entry':ex.get('goal_at_entry'),'before':state_brief(ex.get('state_before',{})),'after':state_brief(ex.get('state_after',{}))})+'.\n\n'
        else:text+='**Execução:** execute não foi chamado neste trace. A Goal pode ter iniciado/continuado deslocamento; o snapshot e a posição posterior delimitam essa conclusão.\n\n'
        text+='**Cálculos especializados reais:** '+compact_json(row.get('calculations',[]))+'.\n\n'
        events=row.get('events',[])
        if events:text+=table(['Evento/hora','Actor→target','Emissor','Testemunhas','Contexto'],[(str(e['id'])+' / '+str(e['hour'])+' / '+e['kind'],str(e.get('actor'))+'→'+str(e.get('target')),e.get('emitter_stack'),e['witnesses'],e['context']) for e in events])
        else:text+='**Evento:** nenhum evento retido durante esta decisão. Isso pode significar movimento/efeito sem evento; não implica falha.\n\n'
        text+='**Aprendizado aceito durante a decisão (amostra):** '+compact_json(row.get('learning_during_decision',[]))+'.\n\n'
        retained_ids={e['id'] for e in events}
        receipts=[{'event':e['id'],'kind':e['kind'],'learned':e.get('learned')} for e in traces['important_events'] if e['id'] in retained_ids]
        text+='**Recibos posteriores ligados ao mesmo event_id:** '+compact_json(receipts)+'. Contagem é operações de aprendizado aceitas, não indivíduos únicos.\n\n'
        text+='**Consequência imediata:** '+compact_json(state_brief(after))+'. **Observação/relações com o alvo ao final:** '+compact_json({'observation_end':row.get('known_target'),'relations_end':row.get('relations_to_target',[])})+'. Não usar esse estado posterior como entrada antiga nem atribuir consequências futuras sem vínculo causal.\n\n'
    text+='## Mortes: registros e limites da reconstrução\n\n'
    cases=traces.get('death_cases',[])
    text+='Cada morte tem registro final e duas decisões recentes retidas; estas são precedência temporal, não prova de que só essas decisões causaram a morte. O conjunto completo está em traces.death_cases, com estado/posses/recursos locais no instante.\n\n'
    chosen=[]
    categories=[('hunger',lambda d:d['record'].get('cause')=='hunger'),('thirst',lambda d:d['record'].get('cause')=='thirst'),('both',lambda d:d['record'].get('cause')=='both'),('combat',lambda d:d['record'].get('cause')=='combat'),('with_owned_food',lambda d:d['state'].get('food',0)>0),('with_local_food',lambda d:(d['state'].get('local_food') or 0)>0),('with_owned_water',lambda d:d['state'].get('water',0)>0),('no_money',lambda d:d['state'].get('money')==0),('with_money',lambda d:d['state'].get('money',0)>=2)]
    for label,predicate in categories:
        sample=next((d for d in cases if d.get('record') and predicate(d)),None)
        if not sample:text+=f"**{label}:** nenhum caso que satisfaça o filtro na campanha.\n\n";continue
        text+=f"### Caso {label}: NPC #{sample['actor']}, h{sample['hour']}\n\n"
        text+='Registro: '+compact_json(sample['record'])+'.\n\nEstado pré-fechamento de morte: '+compact_json(state_brief(sample['state']))+'.\n\n'
        for d in sample['last_decisions']:
            text+='Decisão recente: '+compact_json({'hour':d['hour'],'actor':d['actor'],'selected_need':d.get('selected_need'),'winner':d.get('winner'),'preparations':d.get('preparations'),'execution':d.get('execution'),'state_before':state_brief(d.get('state_before',{})),'state_after':state_brief(d.get('state_after',{}))})+'.\n\n'
        text+='LACUNA: estoque local não prova que era conhecido, pagável, alcançável e consumível a tempo; o trace explica as últimas escolhas, mas não simula um contrafactual de sobrevivência.\n\n'
        chosen.append({'label':label,'actor':sample['actor'],'hour':sample['hour']})
    text+='## Perguntas sem resposta completa\n\n“Por que não tentou uma alternativa que o produtor nunca enumerou?” exige gate/entrada que nem sempre foi retido. “O que sabia horas antes?” exige snapshot histórico de Facts/observações, não só IDs. “Era inevitável morrer?” não pode ser demonstrado apenas pela sequência observada, pois precisaria comparar alternativas com as mesmas restrições/tempo/RNG. “Por que um deus não respondeu?” exige registrar cada gate da avaliação naquele instante. Estas são LACUNAS DE OBSERVABILIDADE e estão detalhadas no relatório correspondente; nenhum silêncio foi preenchido como intenção narrativa.\n'
    write('DECISOES_REAIS.md',text)
    return {'traces_presented':len(selected),'trace_index':index,'death_examples':chosen,'category_raw_observer':dict(Counter(r['category'] for r in allrows)),
            'category_editorial_available':{k:len(v) for k,v in by.items()},'category_presented':dict(Counter(r['category'] for r in selected)),
            'categories_without_retained_trace':absent,'lethal_editorial_note':'A real captured combat/decision assessment was presented under lethal; no finish occurrence was invented.'}

def runtime_narrative(m,manifest,traces,analysis):
    events=m['events'];wm=m['world_metrics'];deaths=Counter(x['cause'] for x in m['deaths'].values())
    text='## Campanha natural e comportamento medido\n\n'
    text+=table(['Campo','Resultado'],[('Seed',m['seed']),('Horas / jogador / história prévia',str(m['hours'])+' / sem jogador / 0'),('Persistentes iniciais',manifest['campaign']['initial_named']),('Abstratos iniciais',manifest['campaign']['initial_abstract']),('População final',m['population']),('Mortes por causa',dict(deaths)),('Eventos emitidos',sum(events.values())),('Reinícios',manifest['campaign']['restarts']),('Erros do observador',m['observer_errors']),('Validações estruturais',m['checks']),('RNG/estado/events A/B',manifest['control']['world_rng_events_equal']),('Tempo instrumentado em segundos',manifest['campaign']['runtime_seconds'])])
    text+='### Evolução a cada25h\n\n'+table(['Hora','Vivos','Mortes','Grupos','Propostas','Policies','Moeda capturada sem treasury*'],[(r['hour'],r['alive'],r['deaths'],r['groups'],r['proposals'],r['policies'],r['money']['total']) for r in m['temporal']])
    text+='*O contador inicial do observador leu money para Kingdom, mas o campo real é treasury. Esses marcos brutos não são o total monetário global. A correção contábil abaixo usa treasury real do save final e a dotação inicial explícita2000/reino; sem inventar snapshots intermediários de tesouro. Essa correção de medição não modifica o mundo nem refaz a campanha.\n\n'
    account=m['money_accounting'];initial,final=account['initial_complete'],account['final_complete']
    text+='### Moeda por proprietário (contagem completa)\n\n'+table(['Dono','Inicial','Final','Delta'],[(k,initial.get(k,0),v,v-initial.get(k,0)) for k,v in final.items()])
    text+=table(['Reconciliação','Valor'],[('Fonte explícita MoneySourceAbstractWork',account['abstract_work_source']),('Delta total',final['total']-initial['total']),('Resíduo após fonte explícita',account['residual_after_explicit_source'])])
    text+='Inclui dinheiro de vivos e mortos, Town/abstratos, tesouros Kingdom, organizações e Policy. Economy.daily acrescenta floor(abstract_population/100) por Town ao saldo abstrato e registra MoneySourceAbstractWork: há uma fonte monetária explícita modelada, não pagamento de um dono rico oculto. Conferir delta contra essa fonte, em vez de exigir total constante. Resíduo0 demonstra reconciliação agregada nesta campanha, sem provar justiça de cada salário nem excluir fluxos compensatórios. WorkResult real com saldo do trabalhador/pagador está nos traces laborais.\n\n'
    text+='### Funil universal por Need\n\n'
    selected=Counter()
    for key,value in m['selected'].items():selected[key.split(':',1)[0]]+=value
    kinds=sorted(set(m['need_seen'])|set(m['evaluate_calls'])|set(selected))
    text+=table(['Need','Aparições refresh','Chamadas _evaluate','Solutions entrada','Disponíveis saída','Seleções finais','_evaluate sem entrada'],[(k,m['need_seen'].get(k,0),m['evaluate_calls'].get(k,0),m['raw_candidates'].get(k,0),m['available'].get(k,0),selected[k],m['no_candidates_at_evaluate'].get(k,0)) for k in kinds])
    text+='Denominadores diferem: aparições repetem a mesma Need em decisões diferentes; _evaluate pode ocorrer mais de uma vez por decisão, inclusive diagnóstico de Need pessoal perdedora e delegação recovery→food/water. “Disponível” é depois de gates, não equivale a número de chamadas Utility; “selecionado” pode ser preparo posterior e não chegar a execute por caminhada. Não tratar colunas como coorte estritamente decrescente.\n\n'
    text+='### Ações: Utility, seleção, execução e resultado\n\n'
    action_selected=Counter()
    for key,value in m['selected'].items():action_selected[key.split(':',1)[1]]+=value
    actions=sorted(set(m['utility_calls'])|set(m['executed'])|set(action_selected))
    text+=table(['Ação','Utility-base chamada','Selecionada final','execute chamado','Sucesso nominal','Falha'],[(a,m['utility_calls'].get(a,0),action_selected[a],m['executed'].get(a,0),m['success'].get(a,0),m['failure'].get(a,0)) for a in actions])
    text+='Utility-base da variante *_meal é contabilizada pelo nome da aquisição original. Terminal usa scores especializados. Sucesso nominal pode ser atribuição/etapa, não resolução final do motivo; esses casos estão na fonte de cada ação.\n\n'
    text+='### Gates/fracassos realmente observados\n\n'+table(['Need / razão (pré ou pós)','Contagem'],sorted(m['pre_utility_and_post_gates'].items()))
    text+=table(['Ação / outcome de falha','Contagem'],sorted(m['failed_reasons'].items(),key=lambda x:-x[1]))
    text+='### LOD observado\n\n'+table(['Estado / intervalo em horas','Medições'],sorted(m['lod_calls'].items()))
    text+='### Latências com distribuição\n\n'
    text+=table(['Métrica','n','min','p25','median','mean','p75','p90','max'],[(k,*[r['distribution'].get(x,'ND') for x in ('n','min','p25','median','mean','p75','p90','max')]) for k,r in sorted(m['latencies'].items())])
    text+='Latências são em horas de world.turn. event_to_knowledge conta operações aceitas, inclusive reforço posterior; need_lifetime_when_finish_called inclui chamadas repetidas de finish de estados já encerrados, portanto não é tempo de resolução único por episódio. group_to_first_or_repeated_meeting mede cada reunião desde criação, não só a primeira. submission_to_decision usa primeira submissão e pode incluir reconsideração. Invitation→response/Journey→arrival só são medidas quando IDs e fases casam; n0 não é latência0. Crime→primeira investigação e Need→primeira ação não têm coorte universal retida: LACUNA, não média inventada.\n\n'
    text+='### Grupos, propostas, políticas e facções\n\n'
    text+=table(['Transição','Ocorrências'],[(k,events.get(k,0)) for k in ('NewGroupCreated','GroupJoined','GroupJoinRejected','GroupMeeting','GroupDissolved','ProposalCreated','ProposalReused','ProposalSupported','ProposalSubmitted','PolicyDecided','PolicyCreated','PolicyEffect','PolicyCompleted','FactionInvite','FactionMembershipAccepted','FactionMembershipRejected','FactionMembershipDeferred','FactionFormalized','GroupFormalized','FactionAction')])
    text+=table(['Grupos atuais','Contagem'],[('Total',len(m['groups'])),('Status',dict(Counter(g['status'] for g in m['groups']))),('Investimento/reuniões',dict(Counter(g['investment'] for g in m['groups']))),('Membros finais vivos',sum(len(g['living_members']) for g in m['groups']))])
    text+=table(['Proposta','Grupo / município / setor','Status / decisão','Representante final: HP/fome/sede/lugar','Prefeito final'],[(p['id'],{'group':p['group_id'],'town':p['town_id'],'sector':p.get('sector')},[p['status'],p.get('result',{})],state_brief(p['representative']) if p.get('representative') else None,state_brief(p['mayor']) if p.get('mayor') else None) for p in m['proposals']])
    text+=table(['Policy','Setor / status','Orçamento / gasto / devolvido / saldo','Etapas','Trabalhadores / barreiras'],[(p['id'],[p['sector'],p['status']],[p['budget'],p['spent'],p['refunded'],p['money']],[p['work_done'],p['work_required']],[p['workers'],p['barriers']]) for p in m['policies']])
    text+=table(['Facção','Membros / status','Líder final','Estoque / sede','Capacidades finais'],[(f['name']+' #'+str(f['id']),[f['member_ids'],f['status']],state_brief(f['leader_state']),[f['inventory_quantities'],f['hq_inventory']],f['capabilities']) for f in m['factions']])
    text+='Estado final de representante/líder/trabalhador não é seu estado quando a proposta foi criada. Pressões de sobrevivência podem concorrer com reunião/entrega; só atribuir causa concreta quando o trace da hora mostra a substituição. A análise complementar de gates finais e pessoas conhecedoras está em metrics.final_audit.\n\n'
    text+='### Crime, justiça, violência, religião, trabalho e viagens: eventos por estágios\n\n'
    stages={
     'crime→justiça':['ItemStolen','CharacterAttacked','CharacterKilled','WantedIssued','InvestigationClue','InvestigationSearched','InvestigationReply','SearchClueShared','GuardResponded','CharacterCaptured'],
     'escalada→morte':['LethalOptionConsidered','LethalCandidateEvaluated','LethalCandidateRejected','LethalDecision','LethalDecisionUpdated','CharacterAttacked','CharacterIncapacitated','ExecutionOpportunity','TerminalDecision','CharacterKilled','PostKillAppraisal'],
     'fé→acesso':['PrayerOffered','SpiritualReport','SeekDivineContact','DivineAccessAchieved','DivineAudience','DivineContractOffered','DivineContractAccepted','DivineManifestation','DivinityKilled','Apotheosis'],
     'trabalho→carreira':['ItemCreated','TemporaryWorkPerformed','TrainingStarted','TrainingProgress','ProfessionChanged','WorkerMaterialized'],
     'rota→viagem':['RouteKnowledgeCreated','AskRoute','RouteKnowledgeShared','JourneyStarted','JourneyArrived','MigrationStarted','MigrationArrived','ResidentMoved','FollowJourney','EscortJourney','POIExplored','POIClaimed']}
    for group,names in stages.items():
        text+='**'+group+'** (nomes exatos ausentes têm0; catálogo completo evita confundir variações de nome):\n\n'+table(['Evento','Contagem','Aprendizados aceitos'],[(k,events.get(k,0),sum(v for label,v in m['learned'].items() if label.startswith(k+':'))) for k in names])
    text+='As tabelas são frequências por etapa, não conversão causal individual: um crime pode ter várias testemunhas, reforços, buscas e reações; um ataque pode ser não letal. Quem soube de um evento retido é ligado pelo mesmo event_id em traces.important_events. Eventos de nome não existente no catálogo são marcados0 apenas como expectativa investigada, não como feature implementada.\n\n'
    text+='### Estado final dos deuses e dos vínculos religiosos\n\n'
    text+=table(['Deus / domínio','Vida / energia / lugar / presença','Mensagens / seguidores conhecidos / vínculos','Afinidades / pressão','Intervenções retidas'],[(str(g['id'])+' / '+g['name']+' / '+g['domain'],[g['alive'],g['energy'],g['location'],g['presence_regions']],[len(g['messages']),len(g['known_followers']),g['bonds']],[g['affinities'],g['action_pressure']],g['interventions']) for g in m['divinities']])
    text+='Esses são estados finais do deus; mensagens e memórias têm retenção limitada. Não atribuir esse saber retrospectivamente a cada oração. Contratos preservados: '+compact_json(m['contracts'])+'.\n\n'
    text+='Censo religioso/renome final e efeitos por tipo (quando retidos historicamente): '+compact_json(m.get('final_audit',{}).get('religious_outcomes',{}))+'. Não somar veneraçāo social com apoteose objetiva.\n\n'
    text+='### Sobrevivência: mortes com recursos e últimas decisões\n\n'
    deathcases=traces['death_cases']
    filters=[('comida própria',lambda x:x['state'].get('food',0)>0),('água própria',lambda x:x['state'].get('water',0)>0),('comida local',lambda x:(x['state'].get('local_food') or 0)>0),('água local',lambda x:(x['state'].get('local_water') or 0)>0),('sem moeda',lambda x:x['state'].get('money',0)==0),('≥2 moedas',lambda x:x['state'].get('money',0)>=2)]
    text+=table(['No instante de finish_death','Mortes','IDs'],[(label,len(xs:=[x for x in deathcases if test(x)]),[x['actor'] for x in xs]) for label,test in filters])
    text+='Esses conjuntos se sobrepõem e incluem todas as causas; comida/água na Town não prova acesso individual. Os casos de fome/sede/posse/local e as duas decisões anteriores foram incluídos em DECISOES_REAIS. A reserva e recovery existem; a tese antiga de ausência total de cura não descreve o código atual. Falhas de tempo, renda, acesso e decisão continuam possíveis mesmo com esse ciclo.\n\n'
    text+='### Orçamento hídrico: capacidade e demanda mínima\n\n'
    text+='Uma pessoa ganha48 pontos de sede/dia em mapa local e cada unidade reduz no máximo45; o limite ideal é48/45≈1.067 unidades/dia por pessoa, antes de desperdício por beber cedo. Uma capital com104 pessoas presentes precisaria≈110.9/dia, acima do water_daily inicial80. Inventário inicial e estoque amortecem por algum tempo; essa desigualdade não é corrigida por escolher melhor a mesma água. A hipótese assume presença contínua, nenhum canal alternativo e nenhuma obra: viagens, suprimentos, mortes e políticas mudam o balanço. Não é uma nova simulação nem prova de causa individual de toda morte.\n\n'
    text+=table(['Capital','Vivos residentes finais','Água final','Capacidade/dia','Demanda mínima ideal dos residentes*'],[(t['name']+' #'+str(t['id']),t['alive_residents'],t['inventory']['water'],t['infrastructure'].get('water_daily',80),round(t['alive_residents']*48/45,2)) for t in m['towns'] if t['capital']])
    text+='*Residentes podem estar viajando; usar presença física e uma série de consumo para o orçamento efetivo. Mortes por município/causa e recursos no instante estão em metrics.final_audit.\n\n'
    text+='### Cobertura de execução, custos e lacunas\n\n'
    text+=table(['Item','Resultado'],[('Métodos diferentes chamados',len(m['calls'])),('Tempo/hora instrumentada, segundos',m['step_seconds']),('Caps de amostra atingidos',m['sample_caps_reached']),('Traces apresentados',analysis['traces_presented']),('Categorias sem trace retido',analysis['categories_without_retained_trace'])])
    return text

def final_analysis(metrics):
    """Só leitura de WorldState; não instancia Engine nem chama decisões."""
    cached=metrics.get('final_audit',{})
    if cached.get('at_hour')==300 and all(k in cached for k in ('storage_shape','lethal_creation_cohort','group_joins_historical','kingdom_treasuries')):
        return cached
    path=OUT/'save_temporario.json'
    if not path.exists():return metrics.get('final_audit',{})
    from procedural.persistence import JsonRepository
    from procedural.institutions import Institutions
    from procedural.professions import ProfessionSystem
    from types import SimpleNamespace
    w=JsonRepository().load(path)
    # O predicado constrói um dict com todos os setores, logo consulta
    # temporary_eligible mesmo para SECURITY. Serviços de leitura, sem Engine,
    # callbacks, itens, RNG, bootstrap ou operação produtiva.
    reader=Institutions(SimpleNamespace(world=w,professions=ProfessionSystem(w,None,None,None,None)))
    data={'at_hour':w.turn,'read_only':True,'policies':[],'formalization_gates':[],'wanted':{},'divine':{},'deprivation_cases':{}}
    data['kingdom_treasuries']={str(k.id):k.treasury for k in w.kingdoms.values()}
    people=list(w.characters.values())
    data['storage_shape']={'temporary_save_bytes':path.stat().st_size,'history_events':len(w.history),'retained_events':len(w.events),'characters':len(people),'items':len(w.items),'relationships':len(w.relationships),
        'knowledge_total':sum(len(p.knowledge) for p in people),'knowledge_max':max((len(p.knowledge) for p in people),default=0),
        'memories_total':sum(len(p.memories) for p in people),'applied_facts_total':sum(len(p.applied_facts) for p in people),'applied_facts_max':max((len(p.applied_facts) for p in people),default=0),
        'processed_personal_facts_total':sum(len(p.processed_personal_facts) for p in people),'needs_total':sum(len(p.needs) for p in people)}
    joins=[e for e in w.history if e.kind=='GroupJoined']
    data['group_joins_historical']={'events':len(joins),'unique_people':len({e.actor_id for e in joins}),'scope':'Inclui grupos removidos do estado final; GroupJoined é historical=True.'}
    interventions=[e for e in w.history if e.kind=='DivineIntervention']
    venerations=[(p.id,id) for p in people for id,b in p.beliefs.items() if id in w.characters and b.get('believed_divine')]
    data['religious_outcomes']={'intervention_effects':dict(Counter(e.context.get('effect') for e in interventions)),
        'intervention_unique_mortals':len({e.target_id for e in interventions}), 'social_veneration_belief_pairs':len(venerations),'socially_venerated_mortals':sorted({id for p,id in venerations}),
        'mythic_people':[{'id':p.id,'trait':p.mythic_trait,'development':p.mythic_development,'alive':p.alive} for p in people if p.mythic_trait]}
    created=[e for e in w.history if e.kind=='LethalDecision']
    data['lethal_creation_cohort']={'count':len(created),'modes':dict(Counter(e.context.get('decision',{}).get('mode') for e in created)),
        'events':[{'event':e.id,'actor':e.actor_id,'turn':e.turn,'decision':e.context.get('decision')} for e in created],
        'source':'Eventos históricos do próprio save final, sem reconstruir inputs ausentes nem criar novos fatos.'}
    data['census_by_town']=[{'id':t.id,'total_living':t.population,'abstract':t.abstract_population,'persistent_alive':sum(w.characters[i].alive for i in t.resident_ids)} for t in w.towns.values()]
    data['mixed_organizational_contexts']=[{'npc':p.id,'source':n.source,'status':n.status,'context':dict(n.context)} for p in w.characters.values() for n in p.needs.values() if n.kind=='organizational_survival' and n.context.get('group_id') and n.context.get('faction_id')]
    data['deaths_by_residence_and_cause']={str(t.id):dict(Counter(d['cause'] for d in w.death_records.values() if d.get('town_id')==t.id)) for t in w.towns.values() if any(d.get('town_id')==t.id for d in w.death_records.values())}
    for p in w.institutional_policies.values():
        people=[c for c in w.characters.values() if c.alive and c.position.map_id==p.jurisdiction]
        knows=[c for c in people if p.id in c.known_policies]
        eligible=[c for c in knows if reader.worker_eligible(c,p)]
        fit=[c for c in eligible if c.health>=30 and c.fatigue<95]
        data['policies'].append({'id':p.id,'sector':p.sector,'status':p.status,'local_alive':len(people),'knowing':len(knows),'knowing_eligible':len(eligible),'knowing_eligible_fit':len(fit),'fit_ids':[c.id for c in fit],'interpretation':'Snapshot final; não é disponibilidade histórica nem prova de seleção'})
    for g in w.groups.values():
        leader=w.characters.get(g.leader_id)
        place=leader.position if leader else None
        present=[w.characters[i] for i in g.member_ids if w.characters[i].alive and w.characters[i].position==place]
        funds=sum(min(2,max(0,c.money-15)) for c in present)
        score=min(100,min(25,(w.turn-g.created_at)/8)+g.failures*8+g.investment*5+min(15,len(present)*3)+min(15,funds*2))
        data['formalization_gates'].append({'id':g.id,'status':g.status,'age':w.turn-g.created_at,'investment':g.investment,'members':len(g.member_ids),'present_at_leader':len(present),'rich_present':sum(c.money>15 for c in present),'funds':funds,'derived_score_not_called':score,
             'outer_meeting_gates_pass_final':g.investment>=4 and w.turn-g.created_at>=168 and len(g.member_ids)>=3 and sum(c.money>15 for c in present)>=2,
             'responsibility_id':g.responsibility_id,'context_notes':'Posição final do líder é referência; não reconstrói reunião passada.'})
    data['wanted']={'total':len(w.wanted_records),'statuses':dict(Counter(r.status for r in w.wanted_records.values())),'known_by_total':sum(len(r.known_by) for r in w.wanted_records.values())}
    data['divine']={'gods':len(w.divinities),'alive':sum(g.alive for g in w.divinities.values()),'contracts':len(w.divine_contracts),'contracts_by_state':dict(Counter(c.status for c in w.divine_contracts.values())),'mythic_people':sum(bool(c.mythic_trait) for c in w.characters.values()),'death_affinity_positive':sum(c.death_affinity>0 for c in w.characters.values())}
    data['survivors']=[{'id':c.id,'name':c.name,'hp':c.health,'recoverable':c.recoverable_deprivation_damage,'damage':c.damage_by_origin,'last_healed':c.recovery_state.get('last_healed_at'),'food':sum(q for i,q in c.inventory.items() if w.items[i].kind=='food'),'water':sum(q for i,q in c.inventory.items() if w.items[i].kind=='water')} for c in w.characters.values() if c.alive and c.damage_by_origin][:12]
    return data

def campaign_conclusions(m,traces):
    deaths=Counter(d['cause'] for d in m['deaths'].values());total=sum(deaths.values())
    material=sum(deaths[k] for k in ('hunger','thirst','both'))
    selections=sum(m['selected'].values());vital=sum(v for k,v in m['selected'].items() if k.split(':',1)[0] in ('food','food_reserve','water','rest','recovery','healing'))
    text='## Leitura integrada dos resultados desta seed\n\n'
    text+=f"Das {total} mortes, {material} foram classificadas como hunger/thirst/both ({material/max(1,total)*100:.1f}%). As Needs de fome/reserva/água/descanso/recuperação/cura responderam por {vital} de {selections} seleções finais ({vital/max(1,selections)*100:.1f}%). Essa fração mede seleção por kind, não horas gastas: preparo pode trocar a ação de uma Need social por comer ou recolher água.\n\n"
    evidence=[];cooldown_deaths=[]
    for case in traces['death_cases']:
        bad=[]
        for row in case['last_decisions']:
            if any(p['replacement']['action']=='fill_water' for p in row.get('preparations',[])) and row['state_before'].get('failures',{}).get('fill_water',0)>row['hour']:
                bad.append({'hour':row['hour'],'cooldown_until':row['state_before']['failures']['fill_water'],'execution':row.get('execution',{}).get('result')})
        if bad:cooldown_deaths.append({'npc':case['actor'],'death_hour':case['hour'],'cause':case['record']['cause'],'attempts':bad})
    evidence.append(('Mortos com preparo fill_water durante cooldown nas duas últimas decisões',len(cooldown_deaths)))
    for cause,kind in [('hunger','food'),('thirst','water')]:
        cases=[x for x in traces['death_cases'] if x['record']['cause'] in (cause,'both')]
        evidence.append((cause+' / both com '+kind+' próprio ao morrer',sum(x['state'].get(kind,0)>0 for x in cases)))
        evidence.append((cause+' / both com '+kind+' no estoque local ao morrer',sum((x['state'].get('local_'+kind) or 0)>0 for x in cases)))
    text+=table(['Evidência de sobrevivência (conjuntos sobrepostos)','Casos'],evidence)
    text+='A presença de recurso reforça a necessidade de examinar acesso, consumo e fechamento da hora; não é prova isolada de morte evitável. O preparo durante cooldown, quando presente, é uma violação específica de continuidade do bloqueio B03, com horas e outcomes preservados abaixo. A amostra são as duas últimas decisões dos mortos, portanto é um limite inferior de incidência e não taxa do mundo inteiro.\n\n'
    text+=table(['NPC','Morte/causa','Tentativas com cooldown ativo'],[(r['npc'],[r['death_hour'],r['cause']],r['attempts']) for r in cooldown_deaths])
    props=m['proposals'];submitted={e['context'].get('proposal_id',e['target']) for e in traces['important_events'] if e['kind']=='ProposalSubmitted'}
    decided={p['id'] for p in props if p['decided_at'] is not None}
    text+=f"A cadeia coletiva tem {len(m['groups'])} grupos no estado final, {len(props)} propostas preservadas, {len(submitted)} propostas com submissão identificada por ID e {len(decided)} com decisão registrada. Existem {len(m['policies'])} políticas, {sum(p['work_done']>0 for p in m['policies'])} com trabalho e {sum(p['status']=='completed' for p in m['policies'])} concluídas. Essa diferença localiza perdas entre organização, entrega, julgamento e trabalho; os estados finais dos responsáveis e traces explicam apenas os trechos documentados, sem transformar todo atraso em bug.\n\n"
    text+=f"Os eventos registraram {m['events'].get('ItemStolen',0)} furtos, {m['events'].get('CharacterAttacked',0)} ataques e {m['events'].get('CharacterCaptured',0)} capturas. Esses números não são uma taxa de impunidade: cada caso tem autoria/confiança/guarda/pista e oportunidade, e múltiplos crimes podem se referir ao mesmo suspeito. As transições de conhecimento estão nos funis e recibos retidos.\n\n"
    cohort=m['final_audit'].get('lethal_creation_cohort',{})
    text+=f"Houve {m['events'].get('LethalDecision',0)} criações de decisão letal, modos {compact_json(cohort.get('modes',{}))}, {m['events'].get('CharacterIncapacitated',0)} incapacitações, {m['events'].get('ExecutionOpportunity',0)} oportunidades terminais emitidas e {m['calls'].get('terminal_combat.TerminalCombat.execute',0)} chamadas de finish. Ter intenção não foi equivalente a conseguir matar. As {m['calls'].get('lethal_decisions.LethalDecisionSystem.terminal',0)} consultas a terminal() vieram de Agency.adjust na campanha; podem ser avaliações prospectivas, não desfechos. O trace lethal mostra ataque com alvo53HP e uma comparação terminal que favoreceria spare se pertinente; não registra uma execução de spare.\n\n"
    text+=f"Carreira produziu {m['events'].get('TrainingStarted',0)} inícios de treino, {m['events'].get('ProfessionChanged',0)} mudanças de profissão e {m['events'].get('WorkerMaterialized',0)} materializações. Religião registrou {m['events'].get('PrayerOffered',0)} orações, {m['events'].get('DivineIntervention',0)} intervenções e {m['events'].get('DivineAudience',0)} audiências. Viagem teve {m['events'].get('JourneyStarted',0)} partidas e {m['events'].get('JourneyArrived',0)} chegadas. Ausência em um estágio raro não justifica criar oportunidade artificial nem reiniciar a seed.\n\n"
    m['final_audit']['cooldown_preparation_death_evidence']=cooldown_deaths
    return text

def findings(metrics,manifest,tests):
    text='## Problemas confirmados, gargalos e limites\n\n'
    text+=table(['ID','Classificação','Fronteira','Regra / inconsistência','Evidência'],BUGS)
    text+='### Reprodução mínima e evidência controlada\n\n'
    text+='As provas abaixo não avançam nenhuma hora natural nem alteram fontes: reutilizam a fixture institucional e executam chamadas diretas declaradas. Comando reproduzível: `PYTHONDONTWRITEBYTECODE=1 python3 -m experiments.total_proofs`. A prova de alias sincroniza RNG antes do snapshot para não confundir um RNG antigo da fixture com divergência de persistência.\n\n'
    text+=table(['Prova','Dados preservados'],[(k,v) for k,v in manifest.get('controlled_proofs',{}).items() if isinstance(v,dict)])
    text+='''B01 afeta principalmente a confiança no histórico/continuidade: o grupo atual pode estar correto enquanto o passado foi reescrito. B02 remove um elo de consequência política mesmo quando notícia e frustração chegam. B03 liga preparação de viagem e privação, contornando um bloqueio do seletor. B04/B05 têm caminhos incompatíveis, não são apenas resultados raros. B06 é contexto ambíguo confirmado, com impacto causal ainda parcial; não prova sozinho que nenhuma facção age.

**B07 — causa textual de morte exploratória incorreta:** Access.explore pode chamar finish_death(...,'exploration'), mas o ternário de descrição de Engine.finish_death usa o texto de causa autoinfligida para toda causa sem killer que não seja deprivation/combat. O registro/contexto conserva exploration; a frase do evento descreve outra causa. Contradição verificável entre duas partes do próprio evento, mesmo sem uma morte natural exploratória nesta campanha. Não houve correção.

### Código inacessível, legado e duplicação

- Society.react: segundo bloco PolicyDecided é inacessível pelo retorno anterior. Seu único writer de responsibility_id sustenta B02; não é classificação baseada só em zero chamadas.
- Society.candidates: segundo bloco political_pressure é inacessível pelo primeiro retorno ao novo produtor institucional. Regras nele não descrevem o comportamento ativo.
- Society.material e Society.decision_scores não possuem chamadores internos resolvidos e a busca textual no núcleo só encontra suas definições; são rotinas legadas sem entrada pelo fluxo produtivo atual. Chamadas externas/testes ainda podem acessá-las. O mecanismo atual usa Institutions; não somar os dois resultados como duas políticas.
- Access.membership e Society.resolve/decision_scores contêm delegações/caminhos herdados; duplicação de nomes não implica que ambos executam em cada hora. Formalização é o caso comprovado em que caminhos ativos realmente divergem.
- Faith.influence é consulta de diagnóstico objetivo sem chamadores do núcleo atual; não é o censo passado à decisão divina. Isso é uma entrada opcional ociosa, não uma promessa de efeito quebrada.
- AGENCY.maximum_aspirations e AGENCY.no_progress_hours estão declarados, mas não possuem leitores atuais no núcleo. O limite prático de aspirações e abandono usa outros ramos/literais/fórmulas; mudar essas constantes não garante mudar o comportamento. SURVIVAL.normal/moderate/severe são lidos por self dentro de band, portanto não foram classificados como ociosos por uma busca superficial.
- Método com0chamadas naturais continua apenas não observado, salvo prova de inacessibilidade. Matriz por método distingue essas situações.

### Comportamento correto pelas regras, mas potencialmente indesejado

Epistemologia local fragmenta cooperação: desconhecer grupo/rota/política impede opção antes de Utility; não é telepatia faltando por bug. Compra e consumo separados podem deixar alguém com alimento sem comer naquela hora. Administração não paga remuneração pessoal automaticamente, cargo e salário de profissão são distintos. Grupo com muitos integrantes pode ter poucas reuniões físicas; apoio e proposta criada não equivalem a apoio entregue, decisão ou efeito. Capacidade declarada não obriga facção a agir, e sobrevivência de seus membros concorre com trabalho coletivo. Esses comportamentos precisam ser avaliados pelo propósito do jogo; esta tarefa não os rebalanceou.

### Features parciais e ausentes como ciclo completo

Treinamento/reposição geral só cozinha; carreira institucional, comércio amplo, contratos administrativos complexos, escolta remunerada, depósitos regionais, demografia individual abstrata/nascimentos, eleições, guerras nacionais automáticas e mentira deliberada geral não estão completos. O catálogo não confunde modelo/booleano/ação isolada com ciclo natural. Fé objetiva, mito e apoteose têm caminhos próprios; raridade não prova código morto nem exige manipular população/seed.

### Pontos únicos de falha e fronteiras

| Fronteira | Dependência ou gargalo | Como distinguir de bug |
| --- | --- | --- |
| Need↔Goal | Primeira Need solucionável, continuidade e preparação podem impedir o motivo duradouro | Trace da mesma hora mostra prioridade, opções e substituição; outcome final sozinho não basta. |
| Knowledge↔Action | Fato/rota/política/grupo precisa ser aprendido e retido | Identificar recibo/source/confiança; existência objetiva não prova conhecimento. |
| Economy↔Survival | Stock de Town, moeda individual, preço marginal e tempo de chegada | Comparar donos e snapshots; comida no mapa não é comida acessível. |
| Employment↔Production | Pagador, profissão, input, estoque/espaço e tempo efetivo | WorkResult identifica no_payer/no_input/saturated/incompatible/not_arrived; não confundir presença de profissão com produção. |
| Crime↔Justice | Fonte, autoria, guarda conhecedor, jurisdição/pista/tempo | Muitas vítimas/testemunhas não equivalem a autoridade informada ou captura possível. |
| LethalDecision↔Combat | Desejo dirigido pode persistir sem pista/capacidade/acesso | Decision ativa não garante perseguir, atacar ou finish; opportunity é separada. |
| Group↔Proposal | Liderança, presença e representante específico | Sem delegação genérica, morte/carência/ausência pode travar entrega; status final não conta todas as tentativas. |
| Policy↔Worker | Profissional apto precisa saber da oferta e vencer prioridades | PolicyBlocked só aparece após tentativa; zero work pode ser zero conhecimento ou seleção. |
| Faction↔Capability | Líder/membros presentes, provisões reais, dinheiro e ordem conhecida | B05 é inconsistência de tipo; mera falta de recurso/conhecimento é gate normal. |
| Faith↔Access | Deus precisa receber mensagem e mortal precisa chegar/realizar rito | Silêncio pode ser gate normal; sem trace histórico completo, motivo exato é lacuna. |
| RouteKnowledge↔Journey | Caminho conhecido, condição objetiva, provisões e guia | Conhecer destino não prova rota; Journey pausada pode ser comportamento permitido. |
| Event↔Knowledge | Testemunha/participante/canal e confiança | Métrica de evento não conta receptores únicos; retenção/rumor alteram certeza. |
| Event↔história | Buffer limitado, contexto mutável, ausência de parent IDs | B01 reescreve passado; descartes de retenção e falta de input são lacunas de observabilidade. |

Prefeito, representante do grupo, líder da facção, guia de expedição e fonte de pista são pessoas específicas. Há sucessão em alguns casos, mas não substituição universal da tarefa pendente. Uma perda pode interromper a cadeia mesmo com outros NPCs vivos; isso é um limite de resiliência, salvo quando há regra explícita prometendo retomada violada.

**Retorno doméstico interlocal é parcial:** sleep aponta para home, mas _evaluate descarta destino de outro mapa e Navigation.approach só resolve movimento no mesmo mapa. É necessário outro caminho semântico de viagem/retorno; não há um retorno universal automático por toda Need de descanso/recuperação. O trace de Bela Hammer #1165,h155 mostra casa na HQ1162, posição na cidade3 e necessidade bloqueada apesar de conexões conhecidas. Isso delimita uma fronteira entre rotina doméstica e Journey; não prova que todo caminho de volta era impossível nem converte o estoque da HQ em acesso imediato.

'''
    final=metrics.get('final_audit',{})
    if final:
        text+='### Verificações finais sem avançar a simulação\n\n'
        text+=table(['Policy','Setor/estado','Locais vivos','Sabem','Sabem e elegíveis','Sabem, elegíveis e aptos'],[(p['id'],[p['sector'],p['status']],p['local_alive'],p['knowing'],p['knowing_eligible'],p['knowing_eligible_fit']) for p in final['policies']])
        gs=final['formalization_gates']
        text+=table(['Gate final de formalização (grupos; não reuniões passadas)','Passam'],[('investment≥4',sum(g['investment']>=4 for g in gs)),('age≥168',sum(g['age']>=168 for g in gs)),('members≥3',sum(g['members']>=3 for g in gs)),('dois presentes com moeda>15',sum(g['rich_present']>=2 for g in gs)),('gates externos juntos',sum(g['outer_meeting_gates_pass_final'] for g in gs)),('responsibility_id preenchido',sum(g['responsibility_id'] is not None for g in gs))])
        text+='A pontuação derivada do snapshot final não chama nem modifica Institutions.formalization; consta em metrics.final_audit e não é apresentada como avaliação histórica executada.\n\n'
        text+='Contextos organizacionais finais contendo group_id e faction_id simultaneamente: '+str(len(final.get('mixed_organizational_contexts',[])))+'. Detalhes por NPC em metrics.final_audit.mixed_organizational_contexts.\n\n'
        text+='### Memória e volume real do estado final\n\n'+table(['Coleção / medida','Quantidade'],final.get('storage_shape',{}).items())
        text+='knowledge64 e memories32 não limitam todo o personagem: applied_facts e processed_personal_facts não possuem poda geral no núcleo atual, e history seletiva também não tem teto global. Esses registros evitam reaplicar efeitos antigos, mas podem crescer com novos fatos. O volume do save tipado pode repetir conteúdo compartilhado em memória. A medição de tempo inclui observador e serialização; não é custo puro do motor nem garantia de estabilidade por anos.\n\n'
    text+='## Suíte inteira e capacidade de prova\n\n'
    text+=f"Foram executados {tests['total']} testes em {tests['seconds']}s: **{tests['passed']} passaram, {tests['failed']} falharam, {tests['errors']} deram erro**. Fontes e testes ficaram intocados. Todos os métodos/assertivas/chamadas estão no MAPA; log integral e hash no manifesto. Testes atuais de Fase5.4/5.5 e estabilidade básica podem passar enquanto fixtures antigas falham por contratos mudados; não declarar a suíte toda verde.\n\n"
    text+=table(['Resultado','Teste','Interpretação e limite'],[(x['result'],x['test'],x['assessment']) for x in tests['issues']])
    text+='“Fixture desatualizada” nos casos ainda não isolados é interpretação sustentada por mudanças de gates/contratos e pela fonte, não uma correção executada nem dispensa do teste. Falhas de recuperação/prioridade e respostas locais continuam pendências de investigação específica. Os testes não foram adaptados para esconder falhas.\n\n'
    return text

def comparison(metrics):
    ev=metrics['events'];g=metrics['groups']
    deaths=Counter(x['cause'] for x in metrics['deaths'].values())
    text='## Comparação compatível com auditorias anteriores\n\n'
    text+='Cada campanha tem300h, seed/população diferentes. Vaelora mediu um núcleo anterior a ajustes finais de ignore/quadro; Neravon e Thalven usam o núcleo atual com a correção de crash Geography já existente. Diferenças abaixo são descritivas; não atribuem causalidade à seed nem medem melhoria isolada de código. Fontes: relatórios preservados em fase_5_5 e diagnostico_coesao.\n\n'
    joins=[j['npc'] for row in g for j in row.get('joins',[])]
    text+=table(['Métrica','Vaelora-55','Neravon-Coesao55','Thalven-Radiografia55'],[
      ('Persistentes iniciais',1880,1898,1916),('Abstratos iniciais',4644,4693,4742),('Mortes',315,298,len(metrics['deaths'])),
      ('hunger/thirst/both/combat',[175,126,13,1],[160,127,10,1],[deaths.get(k,0) for k in ('hunger','thirst','both','combat')]),
      ('Grupos comuns criados (NewGroupCreated)',132,146,ev.get('NewGroupCreated',0)),('Adesões / pessoas distintas',[998,555],[1064,598],[ev.get('GroupJoined',0),metrics['final_audit']['group_joins_historical']['unique_people']]),
      ('Propostas criadas',46,47,ev.get('ProposalCreated',0)),('Submissões',16,16,ev.get('ProposalSubmitted',0)),('Decisões',2,3,ev.get('PolicyDecided',0)),
      ('Políticas / etapas / concluídas',[2,8,2],[3,1,0],[len(metrics['policies']),sum(p['work_done'] for p in metrics['policies']),sum(p['status']=='completed' for p in metrics['policies'])]),
      ('Formalizações naturais (facções originadas de grupo)',0,0,sum(bool(f.get('origin_group_id') or f.get('norms',{}).get('origin_group')) for f in metrics['factions'])),('Aceites de facção',4,2,ev.get('FactionMembershipAccepted',0))])
    text+='Adesões contadas por evento não incluem fundadores; pessoas distintas derivam dos IDs de joins preservados. Eventos de formalização podem ser duas notificações do mesmo fluxo; a comparação usa facções com origem em grupo para evitar dupla contagem. Métrica ausente na evidência anterior não foi estimada por aproximação. Os padrões de fragmentação, sobrevivência e dificuldade de entrega institucional devem ser examinados por seus funis, não por uma única contagem de “histórias”.\n\n'
    return text

def main():
    metrics=read('metrics.json');traces=read('traces.json');manifest=read('manifesto.json')
    assert manifest['campaign']['hours_completed']==300 and metrics['hours']==300
    assert fingerprint()==manifest['code_sha256']
    clean_emotions(traces)
    metrics['final_audit']=final_analysis(metrics)
    initial=dict(manifest['campaign']['initial_money']);final=dict(metrics['money_final'])
    initial['kingdoms']=2000*manifest['campaign']['config']['kingdom_count']
    final['kingdoms']=sum(metrics['final_audit']['kingdom_treasuries'].values())
    for money in (initial,final):money['total']=sum(v for k,v in money.items() if k!='total')
    source_money=metrics['world_metrics'].get('MoneySourceAbstractWork',0)
    metrics['money_accounting']={'initial_complete':initial,'final_complete':final,'abstract_work_source':source_money,'residual_after_explicit_source':final['total']-initial['total']-source_money,'correction':'Raw observer money uses nonexistent Kingdom.money=0; treasury counted read-only after campaign; initial treasury=2000 per generated kingdom with historical_turns0.'}
    # Aprofundamento de aliases/estados depois da campanha, sem apagar a prova
    # de inventário inicial nem reclassificar retrospectivamente sua ordem.
    inv=Inventory().scan().data()
    from .total_static import render
    holder=type('InventorySnapshot',(),inv)()
    render(holder)
    systems=systems_matrix(inv,metrics);tests=test_results()
    manifest['test_suite']=tests
    import platform,sys,os
    manifest['runtime_environment']={'python':sys.version,'platform':platform.platform(),'pythonhashseed_env':os.environ.get('PYTHONHASHSEED'),'note':'Ambiente do executor da auditoria; A/B foi no mesmo processo. Não é prova universal de equivalência entre versões de Python.'}
    request_path=Path('/home/hugo/.codex/attachments/3a924848-7d24-44b4-bf93-d9b470b9912b/Texto colado.txt')
    if request_path.exists():manifest['request_source']={'path':str(request_path),'sha256':hashlib.sha256(request_path.read_bytes()).hexdigest(),'numbered_sections':104}
    proofs=Path('/tmp/procedural_total_proofs.json')
    if proofs.exists():manifest.setdefault('controlled_proofs',{}).update(json.loads(proofs.read_text()))
    manifest['observer_limits']=['No tie RNG draws','Nested shallow emotion collections removed from traces','target relations and observation are end-of-decision','Audience special tag missed; general call/event counts retained','Learning counts operations, not unique receivers','No universal per-option gate trace in candidate producers','Final worker awareness is a snapshot, not historical cohort','Raw money counters omit Kingdom.treasury; final complete accounting corrected from save and explicit initial endowment; intermediate treasury snapshots missing']
    analysis=trace_report(traces,metrics)
    coverage={'static':inv,'systems':systems,'request_requirements':requirements_index(),'natural':{'seed':metrics['seed'],'hours':metrics['hours'],'methods':{f['symbol']:metrics['calls'].get(f['symbol'],0) for f in inv['functions']},'traces':analysis,'not_branch_coverage':True}}
    header='# RADIOGRAFIA TOTAL — simulador atual\n\n'
    header+=f"Regras **{manifest['rules']}**, geração **{manifest['generation']}**. Referência SHA256 `{manifest['code_sha256']}`. **48 arquivos,501 funções/métodos,49 dataclasses,233 sites de emissão,326 testes**. Auditoria estática antes da simulação; campanha única **Thalven-Radiografia55,300h**.\n\n"
    header+='O mundo tem ciclos materiais, sociais e religiosos ativos, mas sua causalidade é apenas parcialmente registrada. Foram confirmados problemas de histórico/persistência, consequência política e caminhos divergentes, além de gargalos entre sobrevivência, acesso e ação coletiva. A auditoria documenta esses limites sem alterar o comportamento.\n\n'
    body=header+static_narrative(inv)+runtime_narrative(metrics,manifest,traces,analysis)+campaign_conclusions(metrics,traces)+findings(metrics,manifest,tests)+comparison(metrics)
    body+='## Matriz de cobertura conceitual de todo o núcleo\n\n'
    body+=table(['Sistema / módulo','Implementado / completo?','Testes candidatos*','Chamadas naturais / métodos vistos','Observabilidade','Persistência'],[(s['system']+' / '+s['module'],s['completeness'],len(s['controlled_test_candidates']),str(s['natural_calls'])+' / '+str(s['methods_observed'])+'/'+str(s['methods_total']),s['observability'],s['persistent']) for s in systems])
    body+='*Mapa de testes conservador por nomes/chamadas, não cobertura de branches; assertivas reais e resultado da suíte estão no MAPA/manifesto. Uma chamada natural pode apenas retornar cedo: comprovação de efeito exige evento/delta/trace. Geração e métodos de jogador não chamados em campanha sem jogador são discriminados em coverage_matrix.\n\n'
    body+='## Evidências e retenção\n\nmetrics.json preserva agregados/histogramas/estados institucionais finais; traces.json mantém amostras/recibos/casos de morte; coverage_matrix.json relaciona todo o inventário com chamadas naturais e testes; manifesto.json guarda hashes, configuração, controles, provas, log da suíte e validação. O save completo é temporário para a leitura final e removido somente após validar os quatro relatórios. A análise não promete reconstruir informação que não foi retida. Observação de esquema: towns.population no contador bruto contém abstract_population; census_by_town em final_audit distingue total_living/abstract/persistent_alive explicitamente.\n\n'
    body+='## Apêndice — fórmulas, geradores de alternativas e guardas exatas\n\nOs trechos são copiados das fontes auditadas, sem pseudocódigo. Complementam as tabelas semânticas com cada limiar e ramo. A referência integral por método e os demais invariantes/testes estão no MAPA.\n\n'
    # Inclui todos os criadores de Need e todos os produtores candidates,
    # mesmo quando não fazem parte da lista editorial de fórmulas centrais.
    symbols=list(FORMULAS)
    symbols.extend(x['symbol'] for x in inv['needs'])
    symbols.extend(f['symbol'] for f in inv['functions'] if f['name'] in ('candidates','on_fact','priority_modifier') and f['module'] in ('personal_actions','faith','migration','investigation','collective_action','access','institutions','personal','emotions'))
    symbols.extend(['social.normalized','social.SocialSystem.considerations','items.ItemService.create','items.ItemService.transfer','items.ItemService.consume','religious_health.ReligiousHealth.classify','renown.RenownSystem.learn','engine.Engine.finish_death'])
    for symbol in dict.fromkeys(symbols):body+=source(symbol,inv)
    write('RADIOGRAFIA_TOTAL.md',body)
    observability(inv,metrics,manifest,systems)
    manifest['documentation']={'files':['RADIOGRAFIA_TOTAL.md','MAPA_CODIGO.md','DECISOES_REAIS.md','OBSERVABILIDADE.md'],'trace_summary':analysis,'static_refinement':{'traits_references_including_aliases':len(inv['traits']),'state_assignments_including_tuple_and_dictionary_targets':len(inv['states']),'numeric_literals_with_context':len(inv['numeric_literals']),'relationship_sites':len(inv['relationships'])},'main_code_changed':False,'tests_changed':False}
    for name,data in [('metrics.json',metrics),('traces.json',traces),('coverage_matrix.json',coverage),('manifesto.json',manifest)]:write(name,compact_json(data))
    print(compact_json({'reports':{p.name:p.stat().st_size for p in OUT.glob('*.md')},'traces':analysis['traces_presented'],'systems':len(systems)}))

if __name__=='__main__':main()
