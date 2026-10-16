"""Produz relatório legível a partir de métricas e evidências já verificadas."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'reports/correcao_alimentar'
MODES = ('jogador', 'espectador', 'mundo')
NAMES = {'jogador': 'Jogador Dovha', 'espectador': 'Espectador Dovha', 'mundo': 'Mundo Mira'}


def read(path):
    return json.loads(path.read_text())


def link(path, label=None):
    return f'[{label or path.name}](<{path}>)'


def fmt(value, decimals=0):
    if value is None:
        return '—'
    return f'{value:,.{decimals}f}'.replace(',', '_').replace('.', ',').replace('_', '.')


def table(headers, rows):
    return '\n'.join(['| '+' | '.join(headers)+' |', '| '+' | '.join(['---']*len(headers))+' |']+
                      ['| '+' | '.join(map(str, row))+' |' for row in rows])


def main():
    data = read(OUT/'comparativo.json')
    narratives = read(OUT/'diversidade_narrativa.json')
    deaths = read(OUT/'mortes_remanescentes.json')
    distribution = read(OUT/'distribuicao_diagnosticos.json')
    parts = []
    def add(value):
        parts.append(value.strip())
    def comparison(label, getter, decimals=0):
        return [label]+[f"{fmt(getter(data[m]['before']), decimals)} → {fmt(getter(data[m]['after']), decimals)}" for m in MODES]

    add(f'''# Correção alimentar individual — implementação, auditorias e histórias

Etapa anterior à Fase 4. Especificação executada: {link(ROOT/'correcao_alimentar.md')}. Versão atual: **mvp-4-alimentacao**. Todos os resultados deste relatório pertencem ao mesmo código congelado; não houve alteração de regra durante as campanhas.

## Resumo executivo

Implementei separação entre reserva, refeição e emergência; refeição normal a partir de fome 50; interrupção de objetivos para comer; prazo biológico comum; e variantes explícitas de aquisição com consumo imediato. Permanecem finitos os estoques, salários, dinheiro e tempo. Fisiologia, dano, cura, HP inicial e regras de economia/formação/vida pessoal foram preservados.

Os **105 testes anteriores e 25 regressões novas passaram: 130 testes**. As três auditorias completaram **10.000 horas cada**. A reprodução observacional das três campanhas antigas também completou 10.000 horas e reproduziu exatamente seus saves originais.

As mortes totais passaram de **690 para 331**. Mortes com fome no limite passaram de **687 para 320**. Mortes por fome carregando alimento passaram de **108 para zero**, incluindo os **107 casos de aquisição na última decisão** e o caso de comida já possuída. Essa mudança, junto das regressões que reproduzem as falhas antigas, comprova correção do bloqueio entre possuir/adquirir e consumir alimento vital.

**A prevenção ainda é pouco efetiva na população.** Apenas 7,43%–10,98% dos NPCs vivos terminam com a reserva-alvo; a fome média no início da procura permanece perto de 76 e no consumo perto de 82. Somente 1,48%–2,54% das procuras começam antes do limiar de refeição. Portanto, não declaro que a alimentação passou a ser amplamente preventiva nem que a pobreza foi resolvida. O mecanismo existe e funciona nos cenários controlados; sua adoção no mundo continua limitada.

O espaço para necessidades pessoais cresceu, mas a seleção fisiológica ainda representa aproximadamente 87%–88% das decisões. Há **12 casos narrativos documentados** adiante: famílias, procura, luto, investigação, sucessão, reconhecimento, carreiras e intervenções do jogador. Também aparecem incoerências sociais reais e repetição. Não iniciei a Fase 4.

## Alterações realizadas

- `feeding.py` calcula cobertura, duração até consumir, margem biológica e diagnóstico; não escolhe objetivos nem executa ações.
- `needs.py` acrescenta manutenção moderada da reserva e distingue risco vital de desempate comum.
- `goals.py` rejeita alternativas alimentares biologicamente lentas, permite refeições explícitas e suspende/retoma objetivos válidos.
- `items.py` informa aquisições, transferências e consumo reais à instrumentação.
- `models.py`, `validation.py` e persistência preservam estado alimentar e objetivo suspenso, com validação.
- `engine.py` instala os serviços e oferece `refeicao`/`refeição`; `ui.py` explica o comando.
- `rules.py` centraliza os parâmetros; as rotinas originais de fisiologia e descanso são estruturalmente idênticas às anteriores.

Também limitei lotes de trabalho pagos com comida ao déficit legítimo da reserva. Na verificação curta anterior às campanhas, a atualização acumulada de trabalho podia entregar um lote excessivo de rações. A correção foi feita **antes** do congelamento e dos três testes longos. A verificação curta foi preservada como diagnóstico, sem entrar nos números finais.

## Arquitetura preservada

O fluxo permanece **State/Knowledge → Need → Priority → Solutions → Goal → Action → Consequence → New State**. O cálculo temporal é metadado da solução existente. Não há GOAP, plano paralelo, roteiro por nome de personagem ou regra para produzir um desfecho predeterminado.

Aquisição continua sendo transferência ou criação por produção legítima; consumo continua removendo uma unidade real e reduzindo fome. Necessidades familiares, profissionais e pessoais disputam as mesmas prioridades. Os módulos `economy.py`, `professions.py` e `personal.py` foram preservados byte a byte; as consequências deles mudam porque os personagens passam a decidir e sobreviver de outra maneira.

Os saves novos usam `mvp-4-alimentacao`; saves antigos `mvp-4` são recusados explicitamente, permanecendo intactos. A geração usa a referência **mvp-4**, separada da versão de regras, para conservar geografia, elenco e relações iniciais antes da simulação histórica. A verificação de Dovha e Mira está em {link(OUT/'geracao_inicial_verificada.json')}. As primeiras 24 horas já respondem às novas regras, de modo que o estado no início da auditoria pode diferir.

## Regras de reserva alimentar

O alvo normal é **24 horas de cobertura**, com crescimento de fome 2/h e nutrição 40 por ração: `ceil(24 × 2 / 40) = 2 rações`. O inventário pessoal representa a reserva. Não foi criada uma despensa doméstica.

Para destino conhecido no mesmo mapa, a cobertura considera o maior entre 24 horas e duração conhecida da viagem + **6 horas de margem**, limitada a **6 rações**. Destino em outro mapa sem trajeto conhecido não permite consultar o mapa global para obter uma distância milagrosa.

`food_reserve` usa base 26, peso de déficit 8 e peso de fome 0,2 até o limiar 50, somados aos modificadores comuns de prioridade. É manutenção moderada, não emergência automática. Não obriga um personagem saudável a abandonar uma necessidade pessoal importante. A procura considera compra, coleta, trabalho compatível, serviço temporário, provisão e pedido já existentes, conforme o que é conhecido e disponível.

O alvo limita a busca preventiva; não proíbe transferências legítimas. Um pagamento produtivo ou uma provisão familiar pode deixar uma terceira ração, e presentes externos também podem ultrapassar o alvo. Isso é diferente de incentivar acúmulo ilimitado. Nas três campanhas finais, os inventários observados dos NPCs vivos têm 0–3 rações.

## Regras de refeição

Com fome **≥50**, surge a necessidade de refeição. Com alimento possuído, comer é uma alternativa direta, sem uma nova aquisição. O valor 50 é uma hipótese configurável, não um ótimo definitivo.

Comprar para reserva continua sem reduzir fome. As variantes `buy_meal`, `forage_meal`, `steal_meal`, `ask_meal`, `work_for_meal` e `service_meal` executam a aquisição legítima e depois consomem de fato. São candidatas de emergência quando a margem é curta; pedido pendente ao jogador não se transforma em uma refeição instantânea.

O comando público `refeicao` usa o mesmo serviço de compra e consumo dos NPCs, cobra o preço real e consome uma hora. Falta de produto ou dinheiro não gera alimento. O jogador da auditoria manteve sua política anterior e não foi privilegiado com uso obrigatório desse comando.

Nutrição usada é `min(fome antes de consumir, 40)`. Sua média nova foi **40 em todas as campanhas**; antes já era aproximadamente 39,94–39,97. Não há evidência de que desperdiçar sistematicamente a nutrição da ração fosse o principal problema anterior. O problema comprovado era conseguir chegar ao consumo a tempo.

## Regras de emergência

Fome **≥80**, ou fome ≥50 com margem estimada de sobrevivência ≤6 horas, recebe tratamento emergencial. O intervalo de decisão torna-se uma hora nos estados críticos, inclusive para NPC distante. A fisiologia continua avançando toda hora, como antes.

Risco vital precede desempate por ID. Uma refeição escolhida pode interromper trabalho, treinamento, descanso, viagem e preparação. O objetivo suspenso é armazenado; após estabilização, só é retomado se sua necessidade e solução ainda forem válidas. A continuidade comum dos objetivos permanece.

A preparação de água e destino não sobrepõe uma refeição imediatamente necessária. Sede já fatal ainda pode preceder fome alta menos urgente. Se duas privações são simultaneamente fatais e uma única ação não resolve ambas, a regra não garante imortalidade.

## Avaliação temporal de sobrevivência

Cada solução alimentar compara **EstimatedTimeUntilFoodConsumed** com **EstimatedSurvivalMargin**. A margem projeta até 128 fechamentos horários, usando HP próprio, fome, sede, privação consecutiva, dano crescente e o bioma atual. O valor é recalculado quando o estado muda.

O tempo da solução inclui deslocamento conhecido, duração de aquisição, renda estimada quando necessária, ida ao mercado, compra e uma oportunidade adicional de comer. Refeição explícita não adiciona uma segunda decisão de consumo. Trabalho de aprendiz considera remuneração diferente do trabalho comum. Em manutenção saudável, a estimativa inclui a espera até o limiar normal de refeição.

Uma alternativa pode permanecer economicamente possível e ser marcada `survival_viable=false`, motivo `SolutionTooSlow`. Ela sai das candidatas alimentares salvadoras. Trabalho continua possível quando há prazo; não foi proibido para todo personagem pobre.

Preço desconhecido usa somente um limite inferior de referência, **2 moedas**, identificado como desconhecido; não vira informação de cotação real. Produto ausente, falta de dinheiro, preço desconhecido, mercado desconhecido, distância e comida já possuída possuem indicadores separados. Nenhum estoque distante é consultado como conhecimento pessoal atual.

É uma estimativa pequena, não uma garantia de rota: distância local pode subestimar desvios, bioma futuro pode mudar a sede e produção/concorrência podem mudar o mercado. O cálculo não prevê todos os eventos futuros nem assegura execução de uma cadeia em ambiente competitivo.

## Testes

Resultado: **130 testes passaram**, incluindo os **105 originais preservados** e **25 novos**. Registro completo: {link(OUT/'testes_finais.txt')}; regressões: {link(ROOT/'tests/test_feeding.py')}.

As regressões cobrem reserva suficiente sem nova procura; reposição preventiva saudável; prioridade pessoal importante; refeição no limiar; interrupção de trabalho, descanso empatado, viagem e treinamento; preparação de água; sede fatal concorrente; cadeia de renda lenta demais e cadeia ainda válida; refeição com orçamento/estoque finitos; mercado vazio; compra sem consumo; lotes limitados; viagem sem conhecimento global; preço desconhecido; determinismo; fila de aquisições; save/load e retomada; comando público com tempo real e ação inválida sem mutação.

Além disso, os três saves finais passaram por validação, round-trip idêntico e continuação determinística de 24 horas. Não houve erro de validação nem diferença no balanço de moeda. Essas verificações detectam incoerências estruturais; não demonstram, sozinhas, boa qualidade narrativa.

## Auditorias de 10.000 horas

Foram repetidos jogador Dovha, espectador Dovha e observador global Mira. O jogador usa comandos públicos e a política automática anterior; não equivale a um humano que improvisa livremente por 10.000 horas. As outras duas campanhas não possuem intervenção de jogador.

O código congelado tem SHA-256 **3ad877c9ff085a0d07009ffcdae917beb9473a012241c0f4e731ea7238ea363b**. O manifesto, snapshot do código e hashes dos artefatos antigos permitem verificar o congelamento e a preservação. Cada campanha tem checkpoints de 1.000 e 5.000 horas, save final, registros alimentares e narrativos, métricas e estados econômicos amostrados.

Para medir indicadores novos na versão antiga, reproduzi as três campanhas com o código histórico isolado e observadores externos. Os saves finais reproduzem exatamente os SHA-256 originais. Para confirmar conhecimento antes de decisões profissionais e de segurança, reproduzi os primeiros 5.000 turnos novos; os três checkpoints também ficaram idênticos aos originais novos.

Essa comparação controla seed, mecanismo de geração e política de teste, mas avalia **o conjunto da correção**. Não isola o efeito de cada parâmetro; decisões diferentes mudam sorteios, trajetórias, sobreviventes e reposição profissional. As médias são de eventos e NPCs observados, não do mesmo painel fixo de sobreviventes.

Dados: {link(OUT/'manifesto_auditoria.json')}, {link(OUT/'verificacao_final.json')}, {link(OUT/'comparativo.json')}, {link(OUT/'baseline_medicoes', 'reproduções antigas')}, {link(OUT/'replay_acoes', 'reproduções observacionais de ações')}.

## Comparação com a Fase 3 original

Cada célula mostra **antes → depois**. “Mortes com fome” inclui a condição de fome 100 com ou sem sede 100; é a mesma classificação do diagnóstico histórico.''')

    add(table(['Indicador']+[NAMES[m] for m in MODES], [
        comparison('Mortes totais', lambda d:d['deaths']),
        comparison('Mortes com fome',lambda d:d['hunger_deaths']),
        comparison('Mortes com fome carregando alimento',lambda d:d['hunger_deaths_with_food']),
        comparison('Aquisição na última decisão fatal',lambda d:d['hunger_deaths_fresh_acquisition']),
        comparison('Comida possuída antes da última decisão',lambda d:d['hunger_deaths_prior_food']),
        comparison('NPCs vivos no final',lambda d:d['final']['alive']),
        comparison('Fome no início da procura',lambda d:d['means']['HungerAtFoodSearchStart'],2),
        comparison('HP no início da procura',lambda d:d['means']['HPAtFoodSearchStart'],2),
        comparison('HP na aquisição',lambda d:d['means']['HPAtAcquisition'],2),
        comparison('Fome na aquisição',lambda d:d['means']['HungerAtAcquisition'],2),
        comparison('Fome ao consumir',lambda d:d['means']['HungerAtConsumption'],2),
        comparison('HP ao consumir',lambda d:d['means']['HPAtConsumption'],2),
        comparison('Procura → aquisição, horas',lambda d:d['means']['TimeFromSearchToAcquisition'],2),
        comparison('Aquisição → consumo, horas',lambda d:d['means']['TimeFromAcquisitionToConsumption'],2),
        comparison('Procura → consumo, horas',lambda d:d['means']['TimeFromSearchToConsumption'],2),
    ]))

    add('''Aquisição → consumo acompanha lotes FIFO: pode incluir comida paga por trabalho e guardada por muito tempo. Sua queda de 29–43 horas para aproximadamente 7 horas reflete também o fim de acúmulos excessivos. Não significa que toda procura ficou dezenas de horas mais rápida: procura → consumo muda pouco e aquisição demora um pouco mais.

As médias temporais usam pares rastreáveis que chegaram à etapa correspondente; aquisições sem consumo não produzem um tempo de consumo completo. Estoque inicial sem carimbo não é atribuído indevidamente a um lote novo. Procura nova inclui manutenção e refeição; a antiga não tinha necessidade separada de reserva. Esses limites importam na leitura das médias.

O HP médio de aquisição **caiu**, em vez de melhorar. Mais sobreviventes fragilizados e trajetórias diferentes podem contribuir, mas não isolei essa causa. Não apresento essa média como prova de melhora de saúde. O desaparecimento do extremo fatal de aquisição com 1–3 HP é um resultado distinto da média populacional.

## Análise das mortes

Na versão corrigida, as condições terminais são **320 mortes com fome 100** e **11 com sede 100 sem fome 100**; não há a condição conjunta nas novas campanhas. O registro classifica estado terminal, não um laudo completo que atribua cada ponto de dano a fome ou sede ao longo da vida. Nenhum desses mortos carregava comida.

Nas 320 mortes com fome, **308** tinham uma cotação local conhecida recente; **209** não podiam comprar uma ração por essa cotação. **56** tinham dinheiro zero. Essas condições se sobrepõem. Não classifico preço desconhecido como pobreza e não deduzo estoque no turno da morte a partir do estoque final.''')

    add(table(['Condição entre mortos com fome']+[NAMES[m] for m in MODES], [
        [label]+[fmt(deaths[m]['summary'][key]) for m in MODES]
        for label,key in [('Sem alimento no inventário','hunger_deaths'),
                          ('Cotação conhecida recente','hunger_deaths_fresh_known_quote'),
                          ('Não podia pagar essa cotação','hunger_deaths_cannot_afford_fresh_known_quote'),
                          ('Dinheiro zero','hunger_deaths_zero_money'),
                          ('Rejeição por prazo nos últimos 6 turnos','hunger_deaths_with_recent_slow_rejection')]]))

    add('''Todos os 320 tinham pelo menos uma rejeição recente por prazo insuficiente. Isso comprova que o filtro identificou caminhos lentos no trecho terminal; **não prova que toda morte era inevitável desde horas ou dias antes**, nem que todas tiveram exclusivamente pobreza como causa. É necessário distinguir o problema terminal da prevenção anterior.

Ainda aparecem objetivos finais `sleep` e `work`. Ao contrário do padrão antigo, não havia refeição carregada para interromper e comer. Objetivo registrado também não é sinônimo de última ação bem-sucedida: nos três modos, as últimas ações bem-sucedidas frequentemente são beber. Um caminho alimentar bloqueado pode deixar outro objetivo ou uma tentativa sem sucesso no estado terminal. Não reclassifico automaticamente esses casos como “morreu porque preferiu dormir tendo comida”.

As novas campanhas somaram **33 mortes com `work` como objetivo final**, contra as 318 últimas escolhas alimentares de trabalho do diagnóstico antigo. Esses indicadores têm definições diferentes; não uso a diferença como contagem exata de um único bug corrigido. As regressões controladas demonstram que uma cadeia biologicamente impossível não é aceita como salvação alimentar.

O cenário antigo de Bela Valerius, descanso empatado e preparo de água apesar da ração possuída, está representado em regressões. Na campanha nova, Bela não morre carregando comida. Escassez de acesso e fragilidade continuam podendo matar depois. Detalhes por pessoa: [mortes_remanescentes.json](</home/hugo/Área de trabalho/procedrual/reports/correcao_alimentar/mortes_remanescentes.json>).

## Análise do estoque pessoal e da prevenção''')

    add(table(['Indicador']+[NAMES[m] for m in MODES], [
        comparison('Reserva ≥2 no final, %',lambda d:d['reserve_final']['maintaining_reserve_percent'],2),
        comparison('Reserva, média dos 40 quadros, %',lambda d:d['average_snapshot_reserve_percent'],2),
        comparison('Rações por NPC vivo no final',lambda d:d['reserve_final']['average_personal_food'],2),
        comparison('Rações, média dos 40 quadros',lambda d:d['average_snapshot_personal_food'],2),
    ]))
    add(table(['Inventário final dos vivos']+[NAMES[m] for m in MODES], [
        [f'{q} ração/rações']+[fmt(data[m]['after']['reserve_final']['reserve_histogram'].get(str(q),0)) for m in MODES]
        for q in range(4)]))
    add(table(['Início real da procura']+[NAMES[m] for m in MODES], [
        ['Antes de fome 50, %']+[fmt(100*distribution[m]['search_distribution']['before_meal_threshold']/distribution[m]['search_distribution']['total'],2) for m in MODES],
        ['Com fome ≥80, %']+[fmt(100*distribution[m]['search_distribution']['high_hunger']/distribution[m]['search_distribution']['total'],2) for m in MODES],
        ['Com HP ≤3, quantidade']+[fmt(distribution[m]['search_distribution']['hp_at_most_three']) for m in MODES],
        ['Seleções de manutenção da reserva']+[fmt(data[m]['after']['reserve_selections']) for m in MODES],
        ['Comida possuída no início, média']+[fmt(data[m]['after']['means']['FoodOwnedAtSearchStart'],3) for m in MODES],
        ['Alvo registrado no início, média']+[fmt(data[m]['after']['means']['ReserveTarget'],2) for m in MODES],
        ['Déficit registrado no início, média']+[fmt(data[m]['after']['means']['ReserveDeficit'],2) for m in MODES],
    ]))
    add('''As reservas antigas eram muito concentradas: a média de 4–6 rações por NPC não significava que a maioria tinha cobertura; só 11%–13% tinham duas ou mais no final. Pagamentos em lotes e acúmulo elevaram essa média. Limitar esses lotes evita esconder a vulnerabilidade por trás de uma média alta.

As médias de quadros usam 40 observações a cada 250 horas, excluindo o quadro inicial; os arquivos contêm 41 quadros com esse inicial incluído. O alvo médio registrado foi 2 rações nas procuras destas campanhas. O alvo ampliado para viagens longas foi exercitado em regressão, sem inventar uma ocorrência frequente nos logs.

Mesmo assim, a correção **não aumentou a proporção mantendo reserva**. A maioria termina com zero ou uma ração. Mais de dois terços das procuras ainda começam com fome ≥80; há **1.120 inícios de procura com HP ≤3**, que são eventos, não 1.120 pessoas distintas ou mortes. Esse achado impede declarar cumprida uma prevenção populacional forte.

Comida de reserva disputa prioridades de renda, fadiga e necessidades pessoais; alguns personagens não conseguem pagar, outros têm caminhos conhecidos limitados ou concorrência por provisões. O alvo configura uma intenção, não entrega automaticamente os recursos para realizá-la. O filtro temporal corrige a aceitação de uma saída impossível, mas não transforma essa saída em viável.

Assim, o ganho principal comprovado está na coerência de refeição e emergência; a rotina preventiva exige diagnóstico adicional de prioridade, continuidade e acesso. Os números não autorizam aumentar arbitrariamente seu peso e passar por cima da vida pessoal.

## Impacto nos mercados e na pobreza''')
    add(table(['Indicador']+[NAMES[m] for m in MODES], [
        comparison('Comida municipal total final',lambda d:d['municipal_food_final']),
        comparison('Mercados sem comida no final',lambda d:d['final']['empty_food']),
        comparison('Dinheiro insuficiente para uma refeição local',lambda d:d['final']['poor_below_one_meal']),
        comparison('Insuficiente para refeição, % dos vivos',lambda d:100*d['final']['poor_below_one_meal']/d['final']['alive'],2),
        comparison('NPCs com menos de 10 moedas',lambda d:d['final']['poor_below_10']),
        comparison('Déficits profissionais locais finais',lambda d:d['final']['professional_deficits']),
    ]))
    add('''Há mais comida municipal total e menos mercados vazios no final, enquanto a proporção sem dinheiro para uma refeição **aumenta nas três campanhas**. Estoque agregado e acesso individual são problemas diferentes. Uma cidade com alimento não implica que uma pessoa saiba da oferta, tenha dinheiro, chegue lá e consiga consumir antes de morrer.

O estoque municipal não foi aumentado por regra nova: essas quantidades resultam de produção, consumo e transferências existentes sob outras trajetórias. Os quadros de reserva/economia amostram o tempo; um valor final sozinho não descreve cada crise de abastecimento.

## Instrumentação de prazo e interrupção

Os logs registram fome/HP na procura, aquisição e consumo; comida possuída, alvo/déficit; tempos entre etapas; prazo estimado e margem; objetivo interrompido; condições de morte; última ação bem-sucedida e motivos/condições conhecidos das alternativas rejeitadas. O save retém diagnóstico recente limitado a 256 entradas; os arquivos de auditoria preservam o fluxo integral. Essa separação mantém observabilidade sem crescimento ilimitado de memória dentro do mundo.''')
    add(table(['Diagnóstico novo']+[NAMES[m] for m in MODES], [
        ['Interrupções emergenciais de objetivos']+[fmt(data[m]['after']['emergency_interruptions']) for m in MODES],
        ['Alternativas rejeitadas por prazo']+[fmt(data[m]['after']['slow_rejections']) for m in MODES],
    ]))
    add('''Somam **3.724 interrupções emergenciais** e **22.407 rejeições por prazo**. São registros de ocorrência, não pessoas únicas, nem uma contagem automática de vidas salvas. As interrupções incluem trabalho, treino, descanso e buscas aquisitivas anteriores.

Exemplo real de prazo: no jogador, turno **103**, NPC **18**, fome 100 e HP 96, uma alternativa `work` foi rejeitada com **33 horas até consumir** contra **32 horas de margem**, `economically_viable=true`, `survival_viable=false` e condição conhecida `NoMoney`. O filtro pode antecipar o fracasso antes de chegar a HP 1–3.

Nas campanhas, o motivo final de rejeição registrado foi `SolutionTooSlow`; ausência de produto/dinheiro/preço conhecido aparece nos indicadores de condições e na geração de candidatas. Isso não significa que todas essas condições eram presentes em toda rejeição. Mercado/rota desconhecidos têm tratamento separado, mas não apareceram como motivo final nesses logs canônicos. As regressões exercitam conhecimento incompleto.

## Impacto sobre necessidades pessoais e profissões''')
    add(table(['Indicador']+[NAMES[m] for m in MODES], [
        comparison('Seleção fisiológica, %',lambda d:d['physiological_percent'],2),
        comparison('Seleções pessoais',lambda d:d['personal_selections']),
        comparison('Necessidades pessoais satisfeitas',lambda d:d['personal_satisfied']),
        comparison('Personagens que concluíram formação',lambda d:d['trained']),
        comparison('Reformados entre residentes existentes',lambda d:d['retrained_existing']),
        comparison('Trabalhadores materializados',lambda d:d['materialized']),
    ]))
    add('''Seleções pessoais somam **16.380 → 25.414**; satisfações pessoais, **7.390 → 11.744**. A seleção fisiológica perde aproximadamente 1,5–2,7 pontos percentuais, sem deixar de dominar. A reserva aparece separadamente da categoria fisiológica nesta classificação; inclusão dela também usa decisões, não deve ser apresentada como tempo social livre.

“Satisfeita” é uma transição de necessidade registrada pelo motor, não uma prova de que cada uma produziu uma história completa ou uma ação social bem-sucedida. Algumas necessidades mudam/encerram por atualização de contexto. A leitura de histórias usa ações e eventos, além desses totais.

Concluintes de formação somam **204 → 41** e materializações **205 → 23**. Não disfarço isso como melhora automática da carreira: menos mortes reduzem parte das vagas, mas não isolei quanto da queda vem disso e quanto vem da concorrência com outras ações. Residentes existentes reformados somam **29 → 21**. A longa sequência de Mira, abaixo, demonstra perda e retomada de progresso, não formação contínua garantida.

Durante as campanhas novas, **281 necessidades pessoais ativas** foram encerradas pela morte de seus donos: 75/95/111 nos três modos. Isso conta necessidades, não 281 sagas interrompidas. Há 82 necessidades familiares nessa condição. A morte ainda limita continuidade.

Na comparação dos eventos sociais, não há melhora uniforme:''')
    event_rows=[]
    for label, key in [('Procura familiar','FamilySearch'),('Pessoa localizada','PersonLocated'),('Investigação','InvestigationPerformed'),('Lembrança de perda','Remembrance'),('Reconhecimento por feito','ResponsibilityFulfilled'),('Proteção prestada','ProtectionGiven'),('Conforto prestado','ComfortGiven')]:
        cells=[]
        for m in MODES:
            old=read(ROOT/'reports/fase_3/auditorias'/m/'metricas_fase2.json')['personal_event_counts'].get(key,0)
            new=narratives[m]['narrative_event_counts'].get(key,0)
            cells.append(f'{fmt(old)} → {fmt(new)}')
        event_rows.append([label]+cells)
    add(table(['Evento social']+[NAMES[m] for m in MODES],event_rows))
    add('''Há mais buscas e encontros, mas luto, reconhecimento e conforto não cresceram conjuntamente. Esses mecanismos já existiam; a correção cria mais oportunidades para alguns deles, sem acrescentar novos temas por decreto.''')

    add((OUT/'HISTORIAS_EMERGENTES.md').read_text())

    add('''## Diversidade narrativa

Utilizo **10 famílias temáticas explícitas**, agrupadas manualmente: cuidado/provisão familiar; ausência e procura; crime/denúncia/investigação/reparação; proteção/evitação; descoberta de morte e luto; troca de informação; reconhecimento/reputação; profissão/formação/abandono; ambição econômica; sucessão. Quests são um meio de intervenção dentro desses temas, não automaticamente um tema adicional. Afinidades e amizade existem no grafo, mas não encontrei uma cadeia robusta de conforto/amparo entre amigos nestes testes novos.

O extrator automático agrupa ações pelo NPC, necessidade e fonte causal atual. Ele liga o fato de origem e os eventos compatíveis emitidos nas ações. Os números abaixo são **episódios de reação local**, não romances completos. Não incluem formação/sucessão nessa contagem, podem incluir repetição de informação e não equivalem a uma medida de originalidade.''')
    add(table(['Episódios e continuidade']+[NAMES[m] for m in MODES], [
        ['Episódios pessoais com ação']+[fmt(narratives[m]['personal_episodes_with_action']) for m in MODES],
        ['Com exatamente 2 eventos registrados']+[fmt(narratives[m]['episodes_by_event_count'].get('2',0)) for m in MODES],
        ['Com exatamente 3 eventos registrados']+[fmt(narratives[m]['episodes_by_event_count'].get('3',0)) for m in MODES],
        ['Com 4 ou mais eventos registrados']+[fmt(narratives[m]['episodes_by_event_count'].get('4+',0)) for m in MODES],
        ['Duração ≥168 horas desde o fato atual']+[fmt(narratives[m]['episodes_spanning_at_least_168_hours']) for m in MODES],
        ['NPCs com ações pessoais separadas por ≥720h']+[fmt(narratives[m]['characters_with_personal_actions_over_at_least_720_hours']) for m in MODES],
        ['Episódios cujo núcleo não é cuidado alimentar']+[fmt(narratives[m]['episodes_whose_core_is_not_food_care']) for m in MODES],
    ]))
    add('''As cadeias de 2/3/4+ eventos estão vinculadas à mesma necessidade/fonte e às ações registradas; não assumo que todos os pares de eventos sucessivos causaram um ao outro. A validação manual dos 12 casos distingue encadeamento comprovado, acontecimentos paralelos e tentativa que não avançou. Exemplo: a resposta do guarda em S01 não foi tratada como efeito exclusivo comprovado da denúncia; a descoberta dos restos é fonte explícita do luto seguinte.

Contagens com duração longa usam o turno do **fato causal atual**, pois um crime novo pode atualizar uma necessidade antiga sem trocar seu `created_at`. Usar apenas a idade da necessidade inflaria duração de histórias. A trajetória de um NPC por 720 horas também pode ser uma sucessão de rotinas pequenas, sem uma saga contínua.

Os modos espectador/mundo são totalmente autônomos. Nos casos selecionados, S01–S10 têm cadeias sem intervenção direta do jogador; S11/S12 têm participação comprovada. O jogador fez 27 entregas de comida na campanha, uma quest foi aceita e falhou. Entregas não equivalem a 27 vidas salvas nem a 27 histórias distintas.

O mundo continua produzindo histórias além de obter comida. A variedade já existe em alguns objetivos, mas continua estreita: há **zero ComfortGiven**, somente **2 ProtectionGiven**, **6 Remembrance** e **5 ResponsibilityFulfilled** entre as três campanhas novas. Muitas origens continuam sendo roubo de alimento, cuidado de privação e morte. Há mais oportunidade social; não há evidência suficiente para dizer que o mundo já saiu da predominância de sobrevivência.

Dados e método: [diversidade_narrativa.json](</home/hugo/Área de trabalho/procedrual/reports/correcao_alimentar/diversidade_narrativa.json>), [episódios jogador](</home/hugo/Área de trabalho/procedrual/reports/correcao_alimentar/auditorias/jogador/episodios_narrativos.json>), [episódios espectador](</home/hugo/Área de trabalho/procedrual/reports/correcao_alimentar/auditorias/espectador/episodios_narrativos.json>), [episódios mundo](</home/hugo/Área de trabalho/procedrual/reports/correcao_alimentar/auditorias/mundo/episodios_narrativos.json>).

## Limitações

- São duas seeds e três campanhas, sem pretensão de representar todas as populações possíveis. Há regressões causais específicas, mas não uma garantia matemática de ausência de bugs em todo mundo gerado.
- A reserva tem alvo e ações legítimas, porém baixa cobertura real; as buscas e refeições ainda são tardias na maioria dos eventos observados. A prevenção não deve ser anunciada como resolvida em escala populacional.
- Não há reconstrução completa das causas econômicas de cada morte remanescente. A análise terminal diferencia falta de dinheiro conhecido, estado e caminho rejeitado; não inventa estoque no instante exato.
- A estimativa temporal é local e pequena; não conhece todos os desvios de navegação, mudanças de bioma, ações de terceiros e cotações futuras.
- Um objetivo suspenso é guardado por personagem; não há uma pilha ilimitada de interrupções. A retomada exige validade, sem recuperar automaticamente um objetivo expirado.
- Médias temporais dependem de lotes consumidos e da composição de sobreviventes. A fila de carimbos tem limite, coalescendo lotes se ultrapassar 16 entradas; essa marca fica registrada. Não trate uma fila coalescida como datas individuais exatas.
- Logs narrativos preservam fatos e ações; o sistema atual não modela emoções profundas ou uma intenção contínua de décadas. Uma descrição literária mais rica não seria evidência de simulação mais rica.

## Bugs e inconsistências ainda existentes

**Denúncia dirigida ao culpado que também é guarda.** Confirmada em S05. A solução encontra autoridade pela profissão/presença sem excluir adequadamente o suspeito. Deve distinguir investigação independente e conflito de interesse; não está corrigida nesta etapa alimentar.

**Informação velha repetida sem utilidade para a necessidade atual.** Confirmada em S06. A ação retorna sucesso de comunicação, mas repassa fato anterior à última observação, sem fechar a busca. Deve avaliar novidade temporal, utilidade e tentativas repetidas.

**Necessidade persistente e evidência podem perder sincronia.** Em S04, Elena ainda tem a necessidade relacionada ao crime no turno 160, mas o fato original já não aparece no conhecimento capturado. A execução respeita conhecimento e pode falhar; a escolha deveria reconhecer melhor quando precisa recuperar a evidência. O fracasso de John no 175 não foi atribuído indevidamente a esquecimento: ele ainda conhecia rumor do crime.

**Prevenção alimentar pouco efetiva e procura repetidamente tardia.** Confirmada pela distribuição e cobertura, apesar de regressões de manutenção funcionando. É uma limitação comportamental observada que merece análise de prioridades/continuidade por pessoa. Não há prova de que simplesmente aumentar prioridade seja suficiente ou que toda ocorrência seja erro, pois acesso real pode impedir a reserva.

**Formação perde todo o progresso após lacuna e pode repetir muitos inícios.** Confirmada em S09, consequência da regra existente. É uma fragilidade de continuidade profissional, não um novo defeito de consumo. Onze tentativas para a mesma profissão produzem extensão temporal sem diversidade equivalente.

**Métricas agregadas de sucesso podem esconder ausência de transformação.** Ação de procurar pode ser aceita sem achar pessoa; informação pode ser transmitida sem ajudar; necessidade pode ser satisfeita sem uma saga concluída. O relatório distingue essas situações, mas uma interface que mostre só “sucesso” pode induzir leitura exagerada.

**Controlador de jogador não atende bem a quest familiar de água.** S11 comprova a falha da política de auditoria; não considero a expiração sem entrega um bug de quest. Testes futuros devem incluir uma política que execute o recurso/destinatário corretos e preserve uma comparação separada com a política antiga.

Não encontrei nos três testes longos a recorrência dos cinco bloqueios alimentares principais: trabalhar tendo refeição vital, descanso vencendo por ID, preparo sobrepondo alimento vital, viagem mantendo bloqueio vital, ou adquirir ração e morrer esperando outra decisão. Os cenários controlados também exercitam essas situações. Isso não elimina os limites de prevenção e economia descritos acima.

## Recomendações para a próxima fase

1. **Tratar o bloqueio aquisição→consumo e a interrupção vital como base testada.** Manter as 25 regressões novas como proteção ao acrescentar outros sistemas.
2. **Revisar a prevenção com evidência por trajetória antes de declarar prontidão populacional.** Separar dinheiro insuficiente, oportunidade que existia mas perdeu prioridade, objetivo persistente que adiou reposição e rota longa. Testar mudanças pequenas, sem colocar toda manutenção acima da família e sem criar comida/dinheiro.
3. **Projetar acesso econômico usando a comida que existe.** A necessidade seguinte é fazer renda, estoque local, preço e distribuição produzirem caminhos reais para pobres. Mais produção agregada por si só não resolve as 209 mortes sem dinheiro para a cotação conhecida. Essa frase é uma recomendação de escopo futuro, não implementação de economia ampla agora.
4. **Corrigir as duas incoerências sociais confirmadas.** Seleção de autoridade e utilidade temporal da informação são alterações locais que podem melhorar narrativas sem inventar novos sistemas grandes.
5. **Reavaliar continuidade de formação separadamente.** Perder todo o progresso após uma lacuna pode manter uma pessoa em ciclos repetidos. Qualquer nova regra deve conservar custos, prática real e condições locais, comparando consequências.
6. **Avaliar a próxima etapa por qualidade causal e diversidade, além de mortalidade.** Medir reserva efetiva, busca antes da fome alta, famílias reencontradas, fatos úteis, reputação transformada, carreiras concluídas e proporção de cadeias cuja origem não é privação.

A correção alimentar executada oferece uma base de consumo e emergência mais coerente e auditável. **Ainda não considero resolvida a meta de alimentação amplamente preventiva nem o predomínio de sobrevivência nas histórias.** A Fase 4 não foi iniciada; esses limites estão registrados para decidir seu escopo a partir dos resultados reais.

## Arquivos para leitura e reprodução''')
    add('\n'.join(f'- {link(OUT/"auditorias"/m/"save_final.json", NAMES[m]+" — save final")}; '+
                  f'{link(OUT/"auditorias"/m/"relatorio.json", "relatório bruto")}; '+
                  f'{link(OUT/"auditorias"/m/"metricas_alimentacao.json", "alimentação")}; '+
                  f'{link(OUT/"auditorias"/m/"narrativa.jsonl.gz", "eventos narrativos")}; '+
                  f'{link(OUT/"auditorias"/m/"acoes_pessoais.jsonl.gz", "decisões e conhecimento")}. ' for m in MODES))
    add(f'''- {link(OUT/'HISTORIAS_EMERGENTES.md', '12 histórias em arquivo separado')} e {link(OUT/'historias_evidencias.json', 'catálogo de evidências')}.
- {link(OUT/'distribuicao_diagnosticos.json', 'distribuição de procura, rejeição e interrupção')}.
- {link(ROOT/'RELATORIO_FOME_E_MORTES.md', 'diagnóstico histórico anterior')} e {link(ROOT/'reports/fase_3/auditorias', 'campanhas originais preservadas')}.

Para gerar novas campanhas com as regras congeladas, use um diretório vazio; o auditor recusa sobrescrever resultados:

```bash
python3 -m unittest discover -s tests -v
python3 -m experiments.feeding_audit --mode jogador --turnos 10000 --output reports/correcao_alimentar/nova_jogador
python3 -m experiments.feeding_audit --mode espectador --turnos 10000 --output reports/correcao_alimentar/nova_espectador
python3 -m experiments.feeding_audit --mode mundo --turnos 10000 --output reports/correcao_alimentar/nova_mundo
```

Os scripts `feeding_baseline`, `feeding_comparison`, `feeding_narratives`, `feeding_story_evidence`, `feeding_remaining_deaths`, `feeding_verify` e `feeding_report` preservam o método usado. A reprodução antiga usa o snapshot histórico isolado; scripts diagnósticos antigos que exigem a assinatura do motor anterior devem ser executados com esse código, não com o motor novo esperando o mesmo hash.''')
    report='\n\n'.join(parts)+'\n'
    (ROOT/'RELATORIO_CORRECAO_ALIMENTAR.md').write_text(report)
    print(json.dumps({'report':str(ROOT/'RELATORIO_CORRECAO_ALIMENTAR.md'), 'words':len(report.split()),
                      'curated_stories':12, 'canonical_campaigns':3, 'hours_each':10000},ensure_ascii=False))


if __name__ == '__main__':
    main()
