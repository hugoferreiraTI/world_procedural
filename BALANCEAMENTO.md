# BALANCEAMENTO — Fase 6.0

Regra: alteração mínima causal, sem quota de eventos. A campanha não foi usada para escolher seed ou reajustar parâmetros depois de observar resultados.

| Parâmetro/regra | Anterior | Novo | Motivo / evidência | Efeito controlado / natural |
| --- | --- | --- | --- | --- |
| Capacidade hídrica inicial | 80/dia para toda localidade | 80 mínimo; acima disso ceil((N×48/45)/poços)×poços | Censo persistente final supera capacidade nas capitais; projeto depois da densificação | A/B: {'thirst': 20, 'hunger': 9, 'both': 3} → {'hunger': 12, 'thirst': 1}; natural {'hunger': 116, 'both': 2, 'thirst': 3, 'combat': 2} |
| Armazenamento de água | 160 | 2×capacidade projetada | Dois dias da infraestrutura inicial; estoque inicial não cresce | Cidades/vilas pequenas mantêm 160; capital típica 222 |
| Demanda alimentar local | 1,2×residentes presentes + ceil(abstratos/120) | 1,2×todos os persistentes presentes + ceil(abstratos/120) | Visitante também consome; não muda residência/censo | Controle +1 visitante = +1,2 de demanda; efeito natural incluído nas janelas |
| Gate de adesão social | Afinidade >=25 como requisito isolado | Adequação organizacional >=50; afinidade componente limitado a15 | Causa e utilidade da instituição não se reduzem à amizade | Controle aceita causa comum com afinidade<25; hostilidade/estratégia continuam vetando |
| Adequação organizacional: componentes | Sem índice separado | causa40, objetivo15, estratégia10, localidade10 ou3, eficácia -20..10, afinidade0..15; autonomia -0,1×independência; dues -3×custo; risco ilegal -0,25×honestidade; adesões -4 cada; hostilidade -0,2×valor | Componentes conhecidos ou observados, sem bônus por existência global da organização | Natural 61 grupos e 1112 adesões; não atribuir tudo ao score |
| Representantes de grupo | Líder exclusivo para entrega | Até2 representantes presentes autorizados | Eliminar falha por ausência do emissor sem execução automática | Controle de delegado/save-load passa; tarefas naturais no relatório |
| Tarefa institucional: prioridade/utility | Sem fila persistente | Prioridade55; utility55 + diligence20 + persistence20; execução dentro da Need organizacional ou obrigação conhecida | Continuidade sem furar prioridade vital; pesos análogos a funções existentes | {'total': 168, 'statuses': {'pending': 75, 'completed': 88, 'blocked': 5}, 'kinds': {'hold_meeting': 118, 'deliver_proposal': 40, 'work_policy': 5, 'return_response': 5}, 'delegated_successes': 42} |
| Reunião | Candidatura a cada24h; execução direta não limitava repetição | Mantém24h também na execução, exceto primeiro encontro | Candidato/execução devem representar a mesma cadência | Não foi reduzido intervalo para gerar mais investimento |
| LOD por pressão | Promoção por fisiologia/combate/migração e janelas ativas | Também perseguição/obrigação conhecida ativa com prioridade>=65 | Resolução temporária enquanto existe pressão operacional | Controle com obrigação70 promove 12→1; baixa pressão não promove |
| Aprendizagem produtiva geral | Cozinha: progresso12..36, salário proporcional | Interface comum; outros caminhos exigem instrutor e déficit, progresso max(12,36-diligence//5), 1 unidade/h salvo arma1/operação; crédito2 sextos/unidade | Mesmo modelo de prática material, sem conversão instantânea ou renda grátis | Controles de produto/pagamento/profissão passam; eventos naturais discriminados |
| Demanda agrária | Sem déficit publicado geral | ceil(max(0,demanda_food-capacidade_caça)×2/3 /20) agricultores requeridos; publicar somente com déficit e grain baixo | 20 = duas unidades/h por dez horas de expediente nominal; não aumenta output real | Instrutor e tempo continuam gates; nominal não é produção realizada |
| Formalização | 168h, investimento4, membros3, presentes3, score65, contribuições/fundos reais | Inalterado | Medir gates antes de rever proxy | Natural 0 formalizações |
| Fisiologia/dano/recuperação/letalidade/religião | Valores 5.5.5 | Inalterados | Sem resolver resultado por limiar arbitrário | Regressões antigas e cenários específicos passam |

### A/B de uma variável

| Medida | Capacidade antiga no motor 6.0 | Capacidade dimensionada no motor 6.0 |
| --- | --- | --- |
| Seed | Controle-Capacidade60 | Controle-Capacidade60 |
| Horas | 144 | 144 |
| Mortes | 32 | 13 |
| Causas | {'thirst': 20, 'hunger': 9, 'both': 3} | {'hunger': 12, 'thirst': 1} |
| Fração de decisões de sobrevivência | 70.61% | 70.71% |
| Furtos de mercado | 868 | 863 |
| Propostas criadas | 38 | 35 |

Mesmo mundo inicial e RNG; os dois braços usam as demais regras 6.0. Alteração de water_daily/storage é um único conjunto de infraestrutura. Não equivale a todas as mudanças 5.5.5→6.0 isoladas. Sem repetição por resultados.

### Efeitos colaterais

Furtos de mercado no A/B: **868→863**. Propostas **38→35**. Fração vital **70.61%→70.71%**. Nenhuma taxa foi restaurada para fabricar conflito. A campanha final serve à observação integrada, não à atribuição causal de cada mudança numérica.

### Versões

RULES_VERSION passa a mvp-14-fase6.0. GENERATION_VERSION passa a mvp-6.0 porque há nova regra de infraestrutura inicial; essa versão participa do hash da seed, logo nomes iguais não garantem mesmo mundo entre versões. Formato de save continua2: campos novos possuem defaults, sem troca de codec. O carregador mantém a recusa de outra rules_version; saves 5.5.5 não são compatíveis com6.0 e não houve migração silenciosa.
