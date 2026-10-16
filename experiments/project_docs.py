"""Documentação do código existente; extrai símbolos, campos e fórmulas por AST."""
import ast
import dataclasses
import re
from pathlib import Path
from procedural import RULES_VERSION,GENERATION_VERSION,rules,utility

BASE=Path(__file__).resolve().parents[1]
SOURCES={p.name:p.read_text() for p in (BASE/'procedural').glob('*.py')}
TREES={name:ast.parse(text) for name,text in SOURCES.items()}

def table(headers,rows):
    return '\n'.join(['| '+' | '.join(headers)+' |','| '+' | '.join(['---']*len(headers))+' |']+
                     ['| '+' | '.join(str(v).replace('|','/') for v in row)+' |' for row in rows])+'\n\n'
def symbol(file,name):
    body=TREES[file].body;node=None
    for part in name.split('.'):
        node=next(n for n in body if isinstance(n,(ast.ClassDef,ast.FunctionDef)) and n.name==part)
        body=node.body
    return node
def excerpt(file,name,start=None):
    text=ast.get_source_segment(SOURCES[file],symbol(file,name))
    if start:text=text[text.index(start):]
    return f'Fonte: `procedural/{file} :: {name}`.\n\n```python\n{text}\n```\n\n'

def main():
    text=f'''# PROJECT — simulador procedural de mundo

Documentação do estado atual, sem reconstrução narrativa das fases anteriores.

| Campo | Valor |
| --- | --- |
| Objetivo | Mundo finito com NPCs persistentes, conhecimento subjetivo e consequências materiais |
| Regras/save | `{RULES_VERSION}` |
| Geração | `{GENERATION_VERSION}` |
| Linguagem | Python 3.11+; somente biblioteca padrão |
| Arquitetura | Dataclasses + serviços coordenados por Engine; Need → alternativas → Utility → Goal → ação |
| Entrada | `procedural/__main__.py :: main` |
| Interface | Terminal em português; simulação sem jogador disponível |
| Persistência | JSON tipado, versionado, escrita atômica; estado do RNG incluído |

## Executar, salvar e testar

```bash
python3 -m procedural --seed Dovha --nome Viajante
python3 -m procedural --seed MinhaSeed --simular 100 --salvar campanha.json
python3 -m procedural --carregar campanha.json --simular 24 --salvar campanha.json
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=tests python3 -m unittest test_phase55 test_phase54
python3 -m unittest discover -s tests -v
```

O último comando enumera a suíte completa; a auditoria de coesão executa somente
28 controles selecionados, não apresenta o restante como aprovado. `--simular`
mede horas adicionais; `GenerationConfig.historical_turns` vale 24 por padrão.
A campanha diagnóstica usa explicitamente zero horas de história inicial e 300
horas observadas. Não confundir o turno absoluto do CLI com o tempo solicitado.
Não há dependências externas, instalação de pacote, banco de dados ou serviço de IA.

No jogo, `ajuda` mostra os comandos. Consultas e ações inválidas não avançam o
relógio; ações válidas usam `Engine.execute` e o mesmo núcleo dos NPCs. As famílias
de comandos incluem movimento/entrada/saída, comida/água/trabalho, conversa/fatos,
investigação, combate, grupos/propostas/organizações, rotas/viagens e ritos.

## Árvore relevante

```text
procedural/                  núcleo e interface atuais
tests/                       testes existentes, preservados
experiments/
    cohesion_audit.py         observador externo da campanha de 300h
    cohesion_reports.py       análise dos dados compactos e relatório de coesão
    project_docs.py           este catálogo gerado a partir de fontes/AST
reports/
    fase_5_5/                somente os três Markdown históricos de Vaelora-55
    diagnostico_coesao/       relatório, métricas, traces e manifesto atuais
PROJECT.md                   referência técnica atual
README.md                    operação resumida
LIMPEZA.md                   inventário resumido e retenção
instruction.md               especificação original de referência
fase_5_5.md                  especificação institucional de referência
.git/                        histórico local de fontes/documentos
```

Os documentos de especificação descrevem intenções e não substituem esta descrição
do código. Recursos marcados como PARCIAL abaixo não devem ser anunciados como um
ciclo completo. Ferramentas de auditoria ficam fora de `procedural/` e não modificam
o comportamento do motor.

## Entradas e objetos coordenadores

'''
    text+=table(['Símbolo','Responsabilidade'],[
        ['`__main__.main()`','Interpreta CLI, gera/carrega WorldState, instancia Engine, executa simulação ou terminal e salva quando solicitado.'],
        ['`generation.generate_world(seed, player_name, with_player, config)`','Gera a verdade inicial e o histórico inicial configurado.'],
        ['`engine.Engine(world)`','Restaura RNG, instancia serviços, liga eventos/listeners e inicializa campos institucionais.'],
        ['`engine.Engine.step()`','Uma hora de decisões, fechamento fisiológico e rotinas globais.'],
        ['`engine.Engine.execute(text)`','Traduz comando de jogador em operação validada do núcleo.'],
        ['`ui.run_terminal(engine, repository)`','Laço de apresentação e entrada; não define regras do mundo.'],
        ['`persistence.JsonRepository.save/load`','Adaptador de disco; valida dados e versão.'],
        ['`unittest` + `tests/test_*.py`','Entrada de testes controlados; não é evidência de ocorrência natural.']])
    text+='''## Uma hora real de simulação

`Engine.step` calcula `closing_turn = world.turn + 1`. Na ordem atual:

1. Percorre personagens em ordem crescente de ID; ignora mortos e jogador.
2. `FeedingSystem.decision_interval` define LOD; o módulo da hora/ID seleciona quem
   decide. `elapsed` mede desde a última atualização. `GoalSystem.decide` observa o
   mercado, atualiza necessidades, escolhe e movimenta/executa ações antes do
   fechamento da hora. Caminhada consome o tempo disponível da ação.
3. Atribui `world.turn = closing_turn`.
4. Aplica `NeedSystem.physiology` a todos os vivos, independentemente do LOD;
   `finish_death` resolve HP zerado. Atualiza necessidades do jogador sobrevivente.
5. A cada 6h, `KnowledgeSystem.gossip`.
6. A cada 24h, `Economy.daily`.
7. `JusticeSystem.tick`, `SocietySystem.tick`, `Institutions.tick`, `FaithSystem.tick`,
   nesta ordem; cada serviço possui suas próprias guardas de periodicidade.
8. `QuestSystem.reconcile`; grava o estado corrente do RNG em `world.rng_state`.

Salvar não é uma operação automática a cada hora. Atualização de decisão e
fisiologia têm frequências diferentes. Comer ocorre antes do dano daquela hora,
mas comprar/coletar, caminhar e consumir podem constituir etapas distintas.

## Modelos persistentes

`models.py` contém dataclasses sem as regras dos serviços. O serializador genérico
persiste todos os campos dessas dataclasses, inclusive dicionários com chaves
inteiras, tuplas e estruturas aninhadas. Índice espacial, caches, assinaturas de
eventos e objetos de serviço são reconstruídos pelo Engine, não serializados.

'''
    descriptions={'WorldState':'Agregado persistente: entidades, relações, relógio, RNG, métricas, histórico e registros de morte.',
      'Character':'Agente persistente; não é uma classe de profissão ou de bandido.',
      'Need':'Pressão com origem, alvo, prioridade, contexto e estado.',
      'Goal':'Intenção operacional escolhida: ação, alvo, destino, estado e resultado.',
      'Commitment':'Continuidade de intenção com investimento, progresso e condição de resolução.',
      'Aspiration':'Objetivo pessoal mais duradouro; não executa ação sozinho.',
      'Personality':'Traços numéricos; emoções e necessidades são estruturas separadas.',
      'Fact':'Conhecimento de um acontecimento, com fonte/confiança/contexto.',
      'Event':'Registro publicado pelo motor; não implica conhecimento universal.',
      'Observation':'Sinais e localização observados, com data; não rastreia remotamente.',
      'Town':'Localidade real usada para cidade, capital e vila; mercado, residentes, tesouro e infraestrutura.',
      'Kingdom':'Reino, localidades subordinadas, governante e estados institucionais.',
      'Route':'Conexão objetiva, percurso, custo, condição e uso.',
      'RouteKnowledge':'Conhecimento pessoal de uma conexão, com origem e confiança.',
      'Journey':'Viagem física em etapas, baseada no que se sabia na partida.',
      'PointOfInterest':'POI com mapa, estoque, posse e história.',
      'Group':'Organização por causa compartilhada, membros, liderança e memória.',
      'Proposal':'Demanda política e apoio por pessoas, grupos e facções.',
      'Policy':'Orçamento reservado, setor, trabalho, efeito, barreira e conclusão.',
      'Faction':'Organização persistente com patrimônio, membros, sede e funções.',
      'Divinity':'Deus objetivo; separado da crença em um mortal ou num nome.',
      'DivineContract':'Condições e estados de um pacto específico.',
      'LethalDecision':'Decisão letal dirigida, persistente e distinta de oportunidade física.',
      'ActionPressure':'Pressão contextual e fontes; não aumenta dano.',
      'Item':'Bem possuído e transferível; quantidades ficam nos inventários dos donos.',
      'Relationship':'Aresta dirigida tipada entre IDs.',
      'CombatState':'Oponentes, lesões, rendição, detenção, memória e julgamentos.'}
    models=[n for n in TREES['models.py'].body if isinstance(n,ast.ClassDef)]
    rows=[]
    for c in models:
        fields=[n.target.id for n in c.body if isinstance(n,ast.AnnAssign)]
        rows.append([c.name,descriptions.get(c.name,ast.get_docstring(c) or 'Estrutura auxiliar persistente.'),', '.join(f'`{x}`' for x in fields[:10])+(' …' if len(fields)>10 else '')])
    text+=table(['Dataclass em models.py','Responsabilidade','Campos de entrada'],rows)
    text+='''`Interest`, `Priority`, `Alternative` e `Result` não são quatro novas classes
persistentes: interesse é expresso por Need/Aspiration/Commitment; prioridade é o
campo `Need.priority`; alternativa é `goals.Solution`; o resultado de execução é
normalmente `(success, outcome)` e é refletido no Goal. `professions.WorkResult`
detalha trabalho/pagamento/produção. A localidade chama-se `Town`, o deus chama-se
`Divinity`; localização conhecida é principalmente dicionário, não uma entidade
Locality ou God adicional.

### Character: mapa completo de campos

'''
    cats=[('Identidade','id name surname nickname category alive is_player origin faction'),
      ('Corpo e recursos','health money hunger thirst fatigue starvation_hours recoverable_deprivation_damage damage_by_origin recovery_state inventory wage_credit last_meal last_drink last_successful_action'),
      ('Personalidade e emoção','personality emotions grievances death_affinity death_state'),
      ('Lugar e trabalho','position home workplace town_id profession financial_since financial_setbacks training_target training_progress training_required training_started training_last_practice market_observation'),
      ('Conhecimento e memória','knowledge memories reputations known_places failures applied_facts observations processed_personal_facts personal_cooldowns'),
      ('Decisão e continuidade','needs goal suspended_goal last_update active_until lod food_state commitments aspirations agency_state action_pressures lethal_decisions'),
      ('Vida institucional','group_ids organization_ids social_state known_groups known_proposals known_policies known_factions'),
      ('Fé e renome','religion devotion beliefs renown item_beliefs mythic_trait mythic_development known_sacred_sites'),
      ('Combate e viagem','combat known_towns migration route_knowledge place_knowledge journey access_state')]
    actual={n.target.id for n in symbol('models.py','Character').body if isinstance(n,ast.AnnAssign)}
    documented=set(' '.join(s for _,s in cats).split());assert actual==documented,(actual-documented,documented-actual)
    text+=table(['Grupo','Campos existentes'],[(name,', '.join(f'`{x}`' for x in fields.split())) for name,fields in cats])
    text+='Relações familiares não são `family_ids` em Character: ficam no grafo dirigido de WorldState (`pai_de`, `filho_de`, `casamento`, etc.). `faction` é um vínculo legado de geração; `organization_ids` representa participação institucional atual. Consultar um sem o outro pode produzir interpretação incorreta.\n\n'
    text+='''## Motor de decisão e fórmulas

`NeedSystem.ensure` cria/reativa pressões por chave; `finish` encerra estados e a
intenção associada. `refresh` combina corpo, trabalho e serviços pessoais/sociais.
A prioridade e a utilidade possuem escalas e papéis distintos. `decide` percorre
as necessidades ordenadas e para na primeira com alternativa viável; não coloca
todos os trabalhos de todas as necessidades num único leilão global de scores.
Uma intenção ativa ainda pode continuar quando a nova pressão não supera a
anterior por 12 pontos, respeitadas exceções de emergência/refeição/recuperação.

### Prioridade e ordem

'''
    text+=excerpt('needs.py','NeedSystem.refresh','active = []')
    text+='### Utilidade de alternativas\n\nTraços entram normalizados por `social.normalized`. O termo de viagem usa distância da alternativa no mesmo mapa; viagens remotas seguem a enumeração de Geography, não uma distância global adivinhada. Agência, influência mítica, pressão de ação e contexto terminal podem ajustar ou substituir a avaliação base no GoalSystem.\n\n'
    text+=excerpt('utility.py','evaluate')+excerpt('goals.py','GoalSystem.choose')
    important=['eat','drink','drink_well','sleep','buy_food','forage','steal','work','work_for_food','organize','join_group','share_problem','meet_group','submit_proposal','support_proposal','review_proposal','policy_work','answer_invitation','request_membership','institutional_patrol','institutional_purchase','institutional_supply','institutional_raid','institutional_support','route_travel','ask_route','attack','defend','flee','surrender','capture','spare','finish','seek_divine_contact','accept_contract']
    text+=table(['Ação','Base atual','Pesos adicionais de Utility'],[(a,utility.BASE[a],', '.join(f'{k}={v:g}' for k,v in utility.WEIGHTS.get(a,{}).items()) or 'nenhum') for a in important])
    text+='### Fisiologia, refeição e recuperação\n\nFome e sede acumulam por hora. Aquisição/posse/consumo são etapas distintas. Comer reduz fome; não repõe HP. Descanso seguro pode recuperar dano de privação registrado, com orçamento que impede somar duas curas completas. O LOD antecipa decisão por fome/baixa vida, sem reduzir a fisiologia de NPCs distantes.\n\n'
    text+=excerpt('needs.py','NeedSystem.physiology')+excerpt('feeding.py','FeedingSystem.meal_pressure')+excerpt('recovery.py','RecoverySystem.recover_hp')
    text+='### Personalidade: onde cada traço entra\n\n'
    traits=[n.target.id for n in symbol('models.py','Personality').body if isinstance(n,ast.AnnAssign)]
    traitrows=[]
    def walk_usage(nodes,file,prefix=''):
        found=[]
        for node in nodes:
            if isinstance(node,ast.ClassDef):found.extend(walk_usage(node.body,file,node.name+'.'))
            elif isinstance(node,ast.FunctionDef):
                attrs={n.attr for n in ast.walk(node) if isinstance(n,ast.Attribute)}
                found.append((attrs,file+' :: '+prefix+node.name))
        return found
    usages=[]
    for file,t in TREES.items():usages.extend(walk_usage(t.body,file))
    purposes={'honesty':'Restrição moral, compra/roubo, resposta legal e decisão política.','compassion':'Ajuda, moderação de agressão, afinidade social, aprovações e pertencimento.',
      'courage':'Disposição a conflito, fuga, risco e atividades organizacionais.','independence':'Autonomia, pedir ajuda, adesão/recusa e exploração.',
      'greed':'Obtenção de recursos, roubo, custo político e contribuição.','diligence':'Trabalho, recuperação de renda, atendimento e avaliações administrativas.',
      'family_loyalty':'Necessidades e assistência a pessoas próximas.','persistence':'Continuidade, reuniões, busca e custo de abandono.',
      'temperament':'Humilhação/insulto/ameaça e protesto.','vengefulness':'Agravo dirigido, perseguição e inibidores de perdão.',
      'ambition':'Formação/liderança, adesão, carreira, exploração e contato.','sadism':'Decisão letal e reforço posterior; não altera força física.'}
    for trait in traits:
        symbols=[name for attrs,name in usages if trait in attrs]
        traitrows.append([trait,purposes[trait],'; '.join(f'`{s}`' for s in symbols[:7])+ (f'; +{len(symbols)-7} usos localizáveis' if len(symbols)>7 else '')])
    text+=table(['Traço real','Efeito','Funções que o consultam diretamente'],traitrows)
    text+='Alguns usos passam por dicionários de pesos em `utility.WEIGHTS`, portanto não aparecem como acesso de atributo na tabela AST. Raiva, ressentimento, humilhação, desespero e devoção não são nomes alternativos dos doze traços: são estados separados.\n\n'
    text+='''## Conhecimento, relações e percepção

`WorldState` contém verdade objetiva. `EventRecorder.emit` publica um fato real,
mas `KnowledgeSystem` filtra testemunhas/observação e propaga conhecimento por
fontes e rumores. `Fact` carrega evento, data, confiança e origem. Um NPC não
consulta toda a história objetiva para decidir. `Observation` expira como pista
remota: não segue automaticamente a posição atual do outro personagem.

`known_places`, `known_towns` e `place_knowledge` registram existência/local;
`route_knowledge` registra conexões, direção, confiança e data. Conhecer destino
não concede trajeto. `beliefs` são interpretações do personagem; `Divinity` é
existência objetiva. Rumor pode produzir crença sem tornar sua interpretação real.
`applied_facts` e registros de processamento evitam reaplicar indefinidamente o
mesmo efeito. Memórias e dicionários possuem limites diferentes.

`RelationshipGraph` usa chaves `source:target:kind`; relações são dirigidas e só
são recíprocas quando solicitado. Confiança, amizade, casamento, filiação,
lealdade, representação municipal e diplomacia não são um único escore.
Reputação, renome e crença também permanecem separados.

## Geografia, geração e viagem

`generation.seed_number` transforma SHA-256 de `GENERATION_VERSION:seed` em
semente do RNG. A fonte aleatória é persistida e restaurada; regras de execução
não são chamadas a serviços externos. Geração padrão: mapa externo 500×500,
quatro reinos, cada um com capital, quatro outras cidades e seis a oito vilas.
`GenerationConfig` permite 1–6 reinos, distâncias e densidade. A configuração
escolhe a escala de NPCs persistentes; população abstrata não equivale a pessoas
individualmente simuladas. Famílias, relações, profissões, deuses, facções, POIs
e rotas são criados nas funções de geração/bootstrap correspondentes.

`Geography.plan` busca no grafo pessoal; `candidates` pode procurar instruções ou
mantimentos; `ask` transmite apenas conexões conhecidas pelo interlocutor.
`begin` exige condição física, rota válida, provisões e pedágios conhecidos.
`Journey` conserva os trechos conhecidos na partida. `step` caminha até o portão,
percorre o mapa externo, entra nas localidades e completa conexões. `visit` não
troca automaticamente residência. Migração é outro estado e possui estabilização.
Seguir/escoltar exige guia presente com viagem válida; não cria conhecimento por
nome de destino. `Geography.audit` valida coerência de viagens e conexões.

POIs têm interior, estoque finito e posse; exploração/ocupação reutilizam
`AccessActions` e itens. **PARCIAL:** exploração interna é resumida, sem uma
simulação de todas as câmaras; disputa territorial e contratos longos de sede
não constituem um sistema completo de propriedade legal.

## Economia e sobrevivência material

Cada dono mantém `inventory: item_id → quantidade`; o item possui um único
`owner_id`. `ItemService.transfer` movimenta/soma pilhas sem duplicar quantidade.
Consume elimina quantidade real. Dinheiro pertence a Character/Town/Kingdom/
Faction/Group/Policy; tesouro municipal não é saldo pessoal do prefeito.
`Kingdom.treasury` guarda o tesouro real (inicialmente 2000/reino), enquanto
`Town.abstract_money` pertence ao conjunto abstrato local. `Economy.daily` cria
`abstract_population // 100` moedas por localidade/dia nessa conta, registrando
`MoneySourceAbstractWork`; é uma fonte monetária explícita, sem débito de outro
pagador. Os demais salários materiais seguem transferências de saldos existentes.

`Economy.observe` registra cotação/estoque e sua data; `known_unaffordable` usa
observação, enquanto compra executada verifica preço, saldo e estoque reais.
Conhecer uma cotação não garante que o bem permaneça disponível ao chegar.
`ProfessionSystem.work`, trabalho avulso, temporário e treinamento usam profissão,
local de trabalho e materiais. `prepare` converte grão em alimento usando crédito
fracionário, preservando balanço; pagamentos são transferências entre donos.
`Population` mantém a contabilidade entre abstratos e residentes persistentes.
Reposição/formação profissional é **PARCIAL**, não substitui qualquer governante
ou qualquer carreira de forma genérica.

Água diária usa a capacidade de `Town.infrastructure`, com base 80/dia e 160 de
armazenamento. A rotina diária coleta/renova água segundo a fonte existente;
aprovar uma obra não cria água imediatamente. Preços, reservas e salários têm
regras no próprio Economy/ProfessionSystem, não um orçamento mágico institucional.

## Grupos: descoberta, criação e continuidade

`Society.pressure` reconhece problema pessoal; `Institutions.own_pressure` acrescenta
escassez observada de água e cooperação criminosa conhecida. `Institutions.refresh`
descobre grupos por encontros/fatos. `search_groups` percorre grupos conhecidos,
não todos os grupos do mundo; `acceptable_group` aplica compatibilidade e acesso.
`collective_candidates` retorna adesão antes de oferecer criação quando há grupo
compatível. Portanto join/create frequentemente são caminhos mutuamente excluídos
na enumeração, não dois scores competindo juntos.

'''
    text+=excerpt('society.py','SocietySystem.affinity')+excerpt('institutions.py','Institutions.acceptable_group')
    text+='A criação exige um problema compartilhado confiável, interlocutor presente e afinidade com pares. `Society.form` seleciona até sete pares e um líder por conexão/traços, não por sorteio de facção. Novos membros podem entrar por qualquer membro presente; o teto é 64. Um NPC pode ter até três grupos. Reunião exige líder e pelo menos dois presentes, atualiza investimento e pode propor demanda. O grupo não desaparece só porque uma proposta foi aprovada.\n\n'
    text+=excerpt('society.py','SocietySystem.form')
    text+='`Society.tick` remove mortos da lista a cada 24h, escolhe sucessor do líder quando possível e dissolve grupos sem membros/relevância suficiente. Grupo dissolvido pode conservar lista histórica de membros até a retirada posterior do objeto; ela não equivale a vínculo ativo em Character. Expedições têm prazo próprio. A auditoria deve distinguir lista histórica, pessoas vivas e vínculo recíproco atual.\n\n'
    text+='''## Propostas, pressão e decisão

`Institutions.propose` procura proposta conhecida na jurisdição da autoridade
derivada por `CollectiveActionSystem.authority`. Reuso compara setor, efeito,
sujeito e estado relevante, inclusive política ainda ativa/paralisada. A consulta
à publicação só ocorre quando o representante está no mercado administrativo.
Dois grupos podem legitimamente desconhecer propostas equivalentes em rascunho.

`support` registra presentes e pessoas únicas; `support_by_group` conserva
assinaturas; `deliver_support` leva apoio à jurisdição. `submit` exige representante
e prefeito juntos no mercado. `delivered_supporter_ids` não é igual a todos os
apoiadores conhecidos pelo grupo. Facção pode apoiar por representante e pessoas
presentes; não recebe bônus automático por ser facção.

'''
    text+=excerpt('institutions.py','Institutions.pressure')+excerpt('institutions.py','Institutions.decision_scores')
    text+='`resolve` escolhe o maior score, verifica capacidade financeira para reservar orçamento e grava motivo/scores. Aprovação sem orçamento suficiente vira adiamento. Administração considera demandas recebidas; ignoradas podem voltar se a pressão aumentar após 24h. O quadro público é conservado na troca de prefeito. Liderança, entrega e julgamento continuam dependendo de pessoas específicas; não existe substituição genérica por qualquer integrante.\n\n'
    text+='''## Políticas: reserva, trabalho e efeito

`create_policy` cria/reutiliza Policy por jurisdição/setor/objetivo. Reserva
dinheiro de Town para Policy: até 16 na aprovação ou 8 na parcial, mínimo 2.
Cada etapa bem executada paga 1 ao trabalhador e aumenta `spent`; conclusão
devolve a sobra, conservando `money + spent + refunded = budget`. `work_required`
é 8 ou 4. `policy_work` exige conhecimento, estado ativo/paralisado, profissão,
posição correta e aptidão física. `PolicyBlocked` não é uma prova de falha
definitiva: a política pode retomar e concluir.

'''
    text+=table(['Setor','Profissional/caminho','Material e efeito'],[
      ['WATER','Mineiro, lenhador, ferreiro ou agricultor no mercado','Uma madeira + um ferro/etapa; a cada duas etapas aumenta 20/dia e 40 de armazenamento. Zero água instantânea.'],
      ['FOOD','Cozinheiro, agricultor ou caçador','prepare usa grão/crédito; até quatro rações por etapa, teto de estoque 240.'],
      ['PROCESSING','Cozinheiro','Mesmo primeiro caminho material de processamento alimentar.'],
      ['EMPLOYMENT','Elegibilidade temporária existente','Primeiro caminho usa processamento alimentar; PARCIAL para diversidade de empregos.'],
      ['WEAPONS','Ferreiro','Duas unidades de ferro + uma madeira criam uma arma real.'],
      ['RAW_MATERIAL','Mineiro, lenhador ou agricultor no workplace','Executa work existente; salário normal mais subsídio de 1 vêm de saldos reais.'],
      ['SECURITY','Guarda ou soldado','Observação/patrulha real, custo e fadiga; não garante evitar crimes.'],
      ['TRANSPORT','Comerciante, rota conhecida e provisões','Carga real de três grãos/madeira/ferro, Journey no mesmo reino e entrega confirmada antes do salário.'],
      ['cult_recognition','Objetivo especial de política','Reconhecimento administrativo de culto usa Town.policies, sem criar alimento.']])
    text+='Barreiras emitidas incluem orçamento esgotado, trabalhador inapto, falta de madeira/ferro/grão/armazenamento, rota/carga/provisões ausentes, chegada não confirmada, carga perdida e falta de trabalho efetivo. Nem toda causa de não seleção vira barreira: uma Need que nunca foi escolhida pode não chegar a policy_work. `known_policies` é informação individual; a existência de uma política não contrata todos os profissionais automaticamente.\n\n'
    text+='## Formalização, facções e adesão\n\nO chamado de formalização em `Society.meeting` tem guardas anteriores: investimento ≥4, idade ≥168h, pelo menos três membros e dois presentes com dinheiro >15. Passar por elas ainda não garante formalizar. `Institutions.formalization` deriva pressão, presença e contribuições; `Society.found_faction` verifica limite mundial, liderança e capacidade organizacional.\n\n'
    text+='Existe também uma via legada em `AccessActions.candidates/execute`: `formalize_organization` chama `Society.found_faction` diretamente. Ela exige idade/investimento/membros e contribuições, mas não passa pelo score ≥65 nem pelo mínimo de três presentes de `Institutions.formalization`. A auditoria reproduziu a divergência com score 55 e dois fundadores; não foi corrigida nesta limpeza. Portanto, os gates da função de pressão não são invariantes de todas as vias.\n\n'
    text+=excerpt('institutions.py','Institutions.formalization')
    text+='A facção guarda `origin_group_id`, fundadores, causa, história e hora da formalização. Contribuições saem de dinheiro pessoal real; apenas fundadores presentes entram. O modelo preserva o grupo de origem como registro. Cooperação criminosa reutiliza o mesmo Group/Faction, derivada de fatos próprios, conhecimento de crime e confiança; não há BanditNPC.\n\n'
    text+='`AccessActions` descobre organizações por encontro/fato. Convite precisa de oferta comunicada; pedido espontâneo usa interesse conhecido. `Institutions.membership` avalia termos recebidos e custos. Fadiga ≥85 ou HP <45 adiam com reconsideração; independência ≥90 pode recusar. Guarda/soldado pode condicionar ingresso a arma em risco alto. Contato com um membro basta para registrar; não há adesão telepática. O ingresso comum exige ausência de organização prévia, embora o modelo comporte até três por outros caminhos.\n\n'
    text+=excerpt('institutions.py','Institutions.membership_scores')
    text+=excerpt('access.py','AccessActions.faction_fit')+excerpt('institutions.py','Institutions.invitation_info')
    text+='Convites conservam offered/considering/conditioned/deferred/accepted/rejected/expired_for_reason; morte é motivo de expiração, não um simples relógio. Retomada depende de refresh, prioridade, aptidão e contato. Termos podem citar relatório do estoque de HQ e recursos da organização, sem prometer recebimento automático.\n\n'
    text+=excerpt('institutions.py','Institutions.capabilities')
    text+='`faction_candidates` permite compra, suprimento, patrulha, apoio político ou incursão conforme causa/capacidade. As ações existentes também incluem contribuições, relatórios, ordens e preparação. Capacidade booleana não prova que exista uma ação autônoma completa para cada rótulo: treinamento especializado, comércio geral, escolta remunerada e contratos CityContract são **PARCIAIS/ausentes como ciclo completo**. Estoque de Faction é agregado; não existe um sistema completo de depósitos e custódia por região.\n\n'
    text+='Inconsistências atuais documentadas na auditoria, sem correção comportamental: `faction_candidates` oferece suprimento se houver comida OU água, enquanto `execute` exige o tipo da maior privação; `GoalSystem.preventive_choice` pode recriar `fill_water` após `_evaluate`, contornando o bloqueio de falha e sem verificar estoque. `Society.refresh` também pode preservar `faction_id` ao reutilizar organizational_survival para um grupo; é preciso ler fonte/alvo/contexto juntos, pois não há uma Need independente para cada instituição.\n\n'
    text+='''## Crime, lei, investigação e combate

Roubo transfere bem real e emite ItemStolen; autoria conhecida é separada de
suspeita e de existência objetiva do crime. `KnowledgeSystem`, `JusticeSystem`
e `InvestigationSystem` conservam fontes, confiança, pista/local e idade. Guardas
recebem casos conhecidos por canais locais e latência; não percorrem uma lista
global de culpados. Pista ausente pode deixar compromisso esperando informação.

`Institutions.authority_response` classifica ação conhecida de facção por
jurisdição. Serviço legal pode ser tolerado; evidências ilegais levam a restrição
e reincidência conhecida a ilegalidade. A classificação pode variar por cidade.
Reagir a uma restrição exige que o membro tenha recebido o fato. **PARCIAL:**
todos os estados possíveis de lei, contratos, multas e dissolução institucional
não possuem cadeia completa; não há guerra civil ou entre reinos automática.

`ConflictSystem` separa confrontar/ameaçar, atacar, defender, fugir, render e
socorrer. Arma, HP, lesão, defesa e variação física alteram dano; coragem altera
escolha. Dano pode causar incapacidade antes da morte. Captura exige autoridade,
evidência e oportunidade. Socorro consome recursos reais.

`LethalDecisionSystem` separa motivo, inibidores, decisão persistente, acesso ao
alvo e oportunidade terminal. `TerminalCombat.opportunity` exige alvo alcançável,
incapacidade e decisão letal ativa. Finalizar válido encerra a vida sem repetir
rolagem de dano; poupar/ajudar/retirar continuam alternativas no contexto terminal.

'''
    text+=excerpt('lethal_decisions.py','LethalDecisionSystem.evaluate')
    text+=excerpt('conflicts.py','ConflictSystem.power')
    text+='A execução adiciona `rng.randint(-INTERACTION.damage_variation, INTERACTION.damage_variation)`, arredonda e aplica dano mínimo 1. Defesa multiplica pelo `defense_multiplier`; contextos específicos podem ajustar o resultado. O trecho operacional está em `ConflictSystem.execute`, e morte converge para `Engine.finish_death`.\n\n'
    text+='''## Religião, deuses, afinidade e contatos

`FaithSystem` interpreta fatos conhecidos, oração, difusão e reavaliação.
Devoção é um campo do personagem; crença não cria divindade. `DivineRelations`
recebe informação por canais válidos e avalia domínio/alinhamento/favor.
`ReligiousHealth` resume fé por região a partir dos canais existentes; não obriga
intervenção. `RenownSystem` separa renome contextual de fama ou adoração.

`AccessActions` pode gerar necessidade seek_divine_contact por fé, perda e
ambição; exige lugar e caminho conhecidos. Rito e chegada não obrigam audiência.
Pactos podem ser oferecidos, aceitos, recusados, abandonados ou quebrados com
conhecimento do descumprimento. Manifestação tem custo/duração; um deus invisível
não fica fisicamente atacável por alguém saber seu nome. Morte divina exige
acesso físico válido; apropriação de essência/apoteose é outro passo com condições.
O potencial mítico raro não garante destino nem ascensão.

'''
    text+=excerpt('divine_relations.py','DivineRelations.adjust')
    text+=excerpt('access.py','AccessActions.audience')+excerpt('divine_relations.py','DivineRelations.assessment')
    text+='## Pressão de ação e dependências\n\nPressão contextual limita motivo, disposição e capacidade; não converte traços médios em causa grave. As fórmulas abaixo são consultas do código atual. Mudanças em pressão não executam ações por si mesmas.\n\n'
    text+=excerpt('action_pressure.py','ActionPressureSystem.disposition')
    text+=excerpt('action_pressure.py','ActionPressureSystem.assess')
    text+='''```mermaid
flowchart LR
    Physiology --> Need
    Knowledge --> Need
    Need --> GoalSystem
    GoalSystem --> Utility
    Utility --> Goal
    Goal --> Services
    Services --> Events
    Events --> Knowledge
    Society --> Groups
    Groups --> Proposals
    Proposals --> Institutions
    Institutions --> Policies
    Policies --> Professions
    Policies --> Items
    Groups --> Formalization
    Formalization --> Factions
    Knowledge --> Geography
    Geography --> Navigation
```

O Engine coordena esses serviços. As setas representam dados/chamadas existentes,
não processos concorrentes independentes. O motor não usa um modelo de linguagem
para inventar decisões ou histórias; relatórios são leitura posterior dos registros.

## Eventos principais e seus consumidores

'''
    text+=table(['Evento/família','Emissor principal','Dados e consumidores','Uso em auditoria'],[
      ['CharacterDied / CharacterKilled','Engine.finish_death / combate terminal','Pessoa, causa, lugar e fonte; Population, Knowledge, aftermath/justiça/fé','Morte única e consequências.'],
      ['ItemStolen','Ações econômicas/conflito/facção','Bem, autor, vítima, lugar; Knowledge, Justice, Society/Institutions','Distinguir roubo objetivo de autoria percebida.'],
      ['GroupSearchAttempt / ExistingGroupFound / GroupJoinRejected','Institutions.search_groups/join','Causa, grupo, origem ou motivo; conhecimento local e auditoria','Eventos têm throttling; não equivalem a todas as avaliações.'],
      ['NewGroupCreated / GroupJoined / GroupMeeting / GroupDissolved','Society + Institutions','Grupo, participantes, causa, fontes; conhecimento e continuidade','Criação, coesão, churn e atividade.'],
      ['ProposalCreated / CompatibleProposalFound / ProposalSupported','Institutions.propose/support','Setor, proposta, pessoas únicas, grupos; conhecimento','Funil de reuso/apoio.'],
      ['ProposalSupportDelivered / ProposalSubmitted','Institutions.deliver_support/submit','Apoio recebido e representante; administração','Entrega física distinta de assinatura remota.'],
      ['PolicyDecided / PolicyDecision','Institutions.resolve','Scores, motivo, pressão e política; Society/Knowledge','Decisão contextual verificável.'],
      ['PolicyCreated / PolicyEffect / PolicyBlocked / PolicyCompleted','Institutions','Orçamento, materiais, trabalho, efeito e obstáculo; percepção dos participantes','Aprovação ≠ efeito e bloqueio ≠ fracasso final.'],
      ['FactionInvite / FactionMembership*','Access + Institutions','Pessoa, termos, avaliação e estado; necessidades/conhecimento','Oferta, resposta, continuidade e ingresso.'],
      ['FormalizationConsidered / FactionFormalized','Institutions.formalization/registered_faction','Fatores, origem, fundadores; conhecimento social','Formalização considerada versus obtida.'],
      ['FactionAction / FactionLocalStatusChanged','Institutions','Ação, capacidade, legalidade, fontes e jurisdição','can_do separado de did_do; autoridade deve conhecer.'],
      ['JourneyStarted / JourneyArrived / RouteKnowledgeShared','Geography','Rotas conhecidas na partida, fonte, provisões e duração','Acesso físico, latência e aprendizado.'],
      ['DivineMessage / DivineIntervention / DivineManifestation','Fé e relações divinas','Canal, região, custo, alvo e efeito; Knowledge/Access','Resposta divina sem onisciência do NPC.']])
    text+='''Os listeners concretos são ligados em `Engine.__init__` e nos construtores dos
serviços. `EventRecorder` atualiza métricas/história e publica no EventBus;
consumidores específicos e observadores recebem o evento. Emitir um evento não
significa que todos os personagens se tornaram testemunhas ou concordaram.

## Persistência e compatibilidade

`persistence.encode/decode` usa tags `$type`, `$dict`, `$tuple`; tipos permitidos
vêm das dataclasses conhecidas. JSON não executa código. `loads` verifica versão
de formato e regras, valida WorldState e testa restauração do RNG.
`JsonRepository.save` valida, escreve arquivo temporário, fsync e substitui
atomicamente o destino. As regras atuais não migram automaticamente saves de
outra versão. Auditorias antigas não são saves necessários ao runtime.

O contexto de Event/Fact pode conservar listas mutáveis do estado vivo. Por
exemplo, adesões posteriores podem alterar a lista de membros de um evento de
fundação antigo. A serialização por valor não preserva esses aliases: continuar
após load pode produzir histórico diferente do mundo original mesmo com RNG e
membros atuais iguais. Continuidade determinística básica funciona em cenários
cobertos, mas não é garantia universal enquanto esse caso existir.

## Invariantes verificadas e limites operacionais

`validation.validate_world/assert_valid` verifica IDs, donos, inventários,
quantidades, locais passáveis, relações, entidades referenciadas, compromissos,
viagens, limites de estruturas e recursos. Orçamento de Policy conserva saldo,
gasto e devolução; apoio por pessoa não duplica dentro da mesma proposta.
`Geography.audit` complementa a coerência entre viagem e rotas.

Invariantes de regras também são demonstradas por controles: conhecer destino
sem rota não autoriza viagem; aprovação não cria recursos; desconhecer fato não
autoriza reação institucional; deus não manifestado não pode ser morto por acesso
físico inexistente. Essas regras não significam que todo NPC conseguirá comer,
viajar, formalizar ou sobreviver.

### Parâmetros declarados

'''
    paramrows=[]
    for name in ('SURVIVAL','FEEDING','UTILITY','RECOVERY','INTERACTION'):
        obj=getattr(rules,name)
        for field in dataclasses.fields(obj):paramrows.append([name,field.name,getattr(obj,field.name),'procedural/rules.py'])
    text+=table(['Conjunto','Parâmetro','Valor atual','Local'],paramrows)
    text+=table(['Limite/condição adicional','Valor','Fonte'],[
      ['Membros de Group / Faction','64 / 64','Institutions.acceptable_group/join/membership; validation'],
      ['Grupos / organizações por personagem','3 / 3 no modelo; ingresso comum exige nenhuma organização','Society.form/found_faction; Institutions.membership'],
      ['Grupos locais / facções mundiais para criação','32 / 24','Society.form/found_faction'],
      ['Propostas na administração / em grupo','24 / 6','Institutions.propose/support; Society.tick'],
      ['Conhecimento/memória de grupo/facção','24 / 16','Society.remember; validation'],
      ['Livros institucionais pessoais','64','Institutions.remember'],
      ['Histórico de política','24','Institutions.policy_work/policy_barrier'],
      ['Convites terminais conservados','16 por facção','Institutions.tick'],
      ['Formalização','168h, investimento 4, score 65, presentes 3 e contribuição 4, entre outras guardas','Society.meeting/found_faction; Institutions.formalization'],
      ['Troca de boatos / economia diária','6h / 24h','Engine.step'],
      ['Limpeza/reposição social','24h','Society.tick'],
      ['Água inicial: capacidade/armazenamento','80/dia / 160','Institutions.bootstrap; Economy.daily']])
    text+='## Mapa dos arquivos atuais\n\nA tabela é obtida da AST atual: símbolos e imports são do código existente. Import não implica chamada a cada tick. O papel resume a responsabilidade principal, sem apresentar todos os métodos como ações autônomas.\n\n'
    maprows=[]
    deps_by_file={name:sorted({n.module for n in ast.walk(tree) if isinstance(n,ast.ImportFrom) and n.level and n.module}) for name,tree in TREES.items()}
    for name,tree in sorted(TREES.items()):
        classes=[n.name for n in tree.body if isinstance(n,ast.ClassDef)]
        funcs=[n.name for n in tree.body if isinstance(n,ast.FunctionDef)]
        dependencies=deps_by_file[name]
        consumers=sorted(Path(other).stem for other,deps in deps_by_file.items() if Path(name).stem in deps)
        doc=(ast.get_docstring(tree) or '').split('\n')[0]
        maprows.append([f'`procedural/{name}`',doc,', '.join(classes+funcs) or 'constantes',', '.join(dependencies) or '—',', '.join(consumers) or '—'])
    text+=table(['Arquivo','Responsabilidade','Classes/funções de módulo','Imports relativos','Importado por (dependência estática)'],maprows)
    text+='### Métodos centrais: entradas, saídas e efeitos\n\n'
    central=[('engine.py','Engine.step','Estado do mundo e RNG','None','Avança hora, executa ações/fisiologia/eventos e rotinas.'),
      ('needs.py','NeedSystem.refresh','Character','Lista ordenada de Need','Cria/reativa/encerra pressões e atualiza prioridades.'),
      ('goals.py','GoalSystem.solutions','Character e Need','Lista ordenada de Solution','Enumera e pontua caminhos; alguns produtores mantêm diagnósticos/estado de acesso, portanto não usar debug como prova de ausência de efeitos.'),
      ('goals.py','GoalSystem.decide','Character e elapsed','None','Escolhe necessidade, mantém/interrompe Goal e anda/executa.'),
      ('goals.py','GoalSystem.execute','Character, Goal, horas','(bool, texto)','Valida, despacha serviço, registra resultado/estado.'),
      ('institutions.py','Institutions.search_groups','Pessoa, causa, sujeito, audit','Lista de Group','Busca conhecimento pessoal; pode emitir diagnóstico throttled.'),
      ('institutions.py','Institutions.propose','Pessoa e grupo','Proposal ou None','Reutiliza/cria proposta e registra apoio.'),
      ('institutions.py','Institutions.resolve','Prefeito e proposta','(bool, texto)','Decide, reserva orçamento e publica resposta.'),
      ('institutions.py','Institutions.policy_work','Pessoa e política','(bool, texto)','Consome materiais/carga, paga trabalho e registra efeito.'),
      ('institutions.py','Institutions.membership','Pessoa, facção, request','(bool, texto)','Avalia termos, muda estado do convite e pode registrar ingresso.'),
      ('geography.py','Geography.begin','Pessoa, destino, motivo, modo, guia','(bool, texto)','Valida provisões/rota, cobra pedágio, cria Journey.'),
      ('geography.py','Geography.step','Pessoa viajando','(bool, texto)','Move fisicamente e registra travessia/chegada.'),
      ('knowledge.py','KnowledgeSystem.learn','Pessoa e Fact','Retorno do método','Filtra/aplica conhecimento e informa listeners.'),
      ('professions.py','ProfessionSystem.work','Pessoa e horas','WorkResult','Consome/produz bens, transfere salário e registra produção.'),
      ('engine.py','Engine.finish_death','Pessoa, causa e contexto','bool','Fecha vida/intenções, preserva corpo/posses e publica morte única.')]
    text+=table(['Símbolo / assinatura atual','Entrada','Saída','Efeitos'],[
        [f"`{file} :: {name}({ast.unparse(symbol(file,name).args)})`",i,o,e] for file,name,i,o,e in central])
    text+='## Testes existentes e o que demonstram\n\n'
    testrows=[]
    for p in sorted((BASE/'tests').glob('test_*.py')):
        tree=ast.parse(p.read_text());names=[n.name for n in ast.walk(tree) if isinstance(n,ast.FunctionDef) and n.name.startswith('test_')]
        doc=(ast.get_docstring(tree) or '').split('\n')[0]
        examples='; '.join(n.removeprefix('test_') for n in names[:4])
        testrows.append([p.name,len(names),doc or examples, 'capacidade/regressão controlada'])
    text+=table(['Arquivo','Métodos','Escopo declarado ou exemplos reais','Tipo de evidência'],testrows)
    text+='Testes controlados preparam circunstâncias e comprovam capacidade/regressão. Emergência natural exige campanha sem manipulação de personagens/estoques/traits. `reports/diagnostico_coesao/RELATORIO_COESAO.md` faz essa distinção e compara o novo resultado com os três Markdown de Vaelora-55, sem inventar métricas históricas ausentes.\n\n'
    text+='''## Fluxos de ponta a ponta

**Sobrevivência:** fisiologia/estado → Need de fome/sede/recuperação → conhecimento
de fonte/preço → soluções conhecidas → viabilidade alimentar/Utility → Goal →
caminhar/adquirir → possuir → consumir → reavaliar; dano e morte ficam no fechamento.

**Política:** problema pessoal → compartilhamento/conhecimento → adesão/criação →
reunião → proposta conhecida equivalente ou nova → assinaturas → entrega presencial
à jurisdição → prefeito disponível → julgamento → dinheiro reservado → trabalhador
informado/apto → material e trabalho → efeito conhecido → continuidade do grupo.

**Facção:** encontro/fato → conhecimento → convite/pedido → termos → benefício/custo
e barreiras → resposta/retomada → registro físico → membros/recursos → capacidade
contextual → necessidade e escolha de ação → compra/serviço/suprimento/resultado.

**Viagem:** saber que local existe → conhecer conexões → obter mantimentos → iniciar
Journey → sair pelo portão → estrada → conexão/entrada → chegada → observação e
atualização da rota. Chegar não é mudar residência nem obter audiência divina.

## Limitações atuais

- `FaithSystem.candidates` pode enumerar `report_congregation`, mas essa ação
  não existe em `utility.BASE`; avaliar a alternativa provoca KeyError antes do
  envio do relato religioso. Há reprodução controlada, sem correção aplicada.
- `Society.react` retorna após delegar PolicyDecided antes do ramo que atribui
  `Group.responsibility_id`; a consequência de responsabilização/tomada de cargo
  não completa esse caminho. A delegada atual não preenche o campo.
- `GoalSystem.solutions` pode atualizar planos/diagnósticos durante a enumeração;
  não é uma API universalmente pura para um visualizador consultar passivamente.
- Morte por exploração registra a causa `exploration`, mas a descrição genérica
  de `finish_death` pode descrevê-la como autoinfligida. O contexto guarda a causa
  específica; a frase não é uma fonte confiável para classificá-la.
- Decisões institucionais competem com fisiologia, deslocamento e compromissos;
  não há garantia de atendimento por prefeito, representante ou candidato.
- A busca social usa afinidade dirigida ao líder; familiaridade, confiança e
  conhecimento de existência são estados diferentes. Isso pode sustentar fragmentação.
- Um booleano de capacidade não implementa treinamento, comércio, escolta ou
  contratos completos. Estoques de organizações ainda são agregados.
- Conhecimento de falha/êxito depende de circulação; aprovação não é efeito e
  efeito não demonstra que o problema de todos foi resolvido.
- Há limites de memória e de propostas; políticas referenciadas permanecem.
  Arquivamento de muitos anos institucionais não é um ciclo completo.
- Produção, cargos, sucessões e população abstrata têm tratamentos específicos;
  não existe substituição profissional/demográfica universal.
- Mortalidade, estabilidade econômica e eventos raros não ficam comprovados por
  uma única campanha de 300h. Frequência baixa não demonstra por si só um bug.
- Registros existentes não retêm todos os descartes de alternativas, ruídos de
  desempate e razões de cada movimento. A auditoria externa observa parte desses
  dados sem adicionar persistência ou instrumentação nova ao núcleo.
'''
    (BASE/'PROJECT.md').write_text(text,encoding='utf-8')
    readme='''# Simulador procedural — estado atual 5.5

Jogo de terminal em português, Python 3.11+, somente biblioteca padrão.
Regras e saves: `mvp-12-fase5.5`; geração: `mvp-5.4`.

```bash
python3 -m procedural --seed Dovha --nome Viajante
python3 -m procedural --seed MinhaSeed --simular 100 --salvar campanha.json
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=tests python3 -m unittest test_phase55 test_phase54
```

No terminal, `ajuda` lista os comandos. Movimento/ações válidas consomem horas;
consultas e ações inválidas não avançam o mundo. Salvar/carregar inclui RNG e estado tipado; versões incompatíveis são recusadas.
Há uma limitação de continuidade com contextos mutáveis, documentada em PROJECT.md.

- [PROJECT.md](PROJECT.md): arquitetura, modelos, fórmulas, sistemas, arquivos e testes.
- [Radiografia total](reports/auditoria_total/RADIOGRAFIA_TOTAL.md): auditoria integral, decisões reais e observabilidade.
- [Relatório de coesão](reports/diagnostico_coesao/RELATORIO_COESAO.md): campanha diagnóstica nova de 300h.
- [LIMPEZA.md](LIMPEZA.md): o que foi retirado e preservado.
- Referência anterior Vaelora-55: [técnico](reports/fase_5_5/RELATORIO_TECNICO.md),
  [mundo](reports/fase_5_5/MUNDO.md), [histórias](reports/fase_5_5/HISTORIAS_REAIS.md).

A Limpeza Intuitiva não é uma nova fase e não rebalanceia o jogo. A única mudança
no núcleo foi a correção de crash em `Geography.emit`, autorizada pelo usuário e
registrada no relatório e manifesto. O histórico de fontes/documentos retirados da árvore está no
Git local. Relatórios antigos podem citar evidências e saves já removidos pela
retenção; os três Markdown de Vaelora-55 são a baseline documental preservada.
'''
    (BASE/'README.md').write_text(readme,encoding='utf-8')
    print(f'PROJECT.md: {len(text.splitlines())} linhas; {len(text.encode())} bytes')

if __name__=='__main__':main()
