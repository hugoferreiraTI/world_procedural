# RELATÓRIO TÉCNICO — Fase 5.5

## Entrega e alcance

Versão `mvp-12-fase5.5`, especificação preservada em `fase_5_5.md`. A fase adapta os serviços existentes para ligar grupo, apoio político, política material, continuidade organizacional e decisão de adesão. Campanha natural **Vaelora-55**, do zero, sem jogador, **300 horas**. Houve um reinício estrutural na mesma seed, documentado abaixo; não houve seleção de seed por resultados interessantes.

## Arquitetura e implementação

Dataclasses, Engine, eventos, conhecimento individual, itens, trabalho, JSON e Need → Utility → Goal → ação continuam sendo a arquitetura. `institutions.py` concentra a integração institucional; não cria um segundo motor de agentes ou economia. A versão de geração continua `mvp-5.4`; regras/saves mudaram. O carregador aplica a incompatibilidade de versão existente. O baseline contém somente fontes anteriores, sem saves/dumps.

| Sistema | Implementado | Limite real |
| --- | --- | --- |
| Grupos conhecidos | Conhecimento por encontros/fatos; busca antes da criação; adesão por qualquer membro presente; motivos de incompatibilidade; até 64 participantes | Conhecer a existência não garante encontro. Cooperação por proposta comum; fusão automática não foi criada. |
| Propostas | Busca entre propostas conhecidas/publicadas; equivalência por jurisdição/setor/efeito/sujeito; apoio único por pessoa e diversos grupos/facções | Apoios remotos só chegam com representação física. Grupos desconhecidos podem legitimamente fragmentar. |
| Pressão e prefeito | Apoios vivos entregues, urgência, persistência, visibilidade e crise; avaliação contextual com personalidade e dinheiro | Pressão é simplificada: área afetada fica registrada; legitimidade/reputação não têm modelo político completo. |
| Política genérica | Estado persistente, dinheiro em reserva, trabalho, efeitos, obstáculos e devolução; aprovação não cria bens | Não há contratação administrativa completa nem garantia de trabalhador disponível. |
| WATER | Obra remunerada consome madeira/ferro; cada duas etapas amplia 20/dia e 40 de armazenamento; coleta diária usa a capacidade | Sem obra não há expansão; sem produção/acesso, estoque disponível continua limitado. Não foi aplicado aumento inicial global. |
| FOOD / PROCESSING / EMPLOYMENT | Profissão/trabalho existentes; matéria-prima e crédito fracionário de grão; alimento produzido em estoque real | A execução alimentar é o primeiro caminho material; não representa todos os empregos e produtos possíveis. |
| WEAPONS / RAW_MATERIAL / SECURITY | Encomenda consome ferro/madeira; produção profissional real com subsídio; guardas observam/patrulham | Matéria-prima segue remuneração normal mais subsídio reservado; patrulha não garante queda de crime. |
| TRANSPORT | Comerciante recebe carga real; rota conhecida e mantimentos; Journey existente; salário somente após entrega física | Primeiro serviço de transporte distribui grão/madeira/ferro dentro do mesmo reino. Comércio remunerado generalizado e contratos extensos ficam para depois. |
| Resultados | Fatos percebidos ligam resposta/efeito/frustração ao grupo; alívio depende da necessidade observada; sem dissolução automática por aprovação | Conhecimento de resultado ainda pode ser atrasado; aprovação isolada não significa resolução do problema. |
| Formalização | Pressão derivada de duração, falhas conhecidas, reuniões, participantes e contribuições; origem/fundadores/história preservados | Presença, financiamento e condições anteriores continuam exigidos; tamanho sozinho não formaliza. |
| Adesão | Benefício/custo por necessidade, profissão, confiança, autonomia, ambição e risco; condição de equipamento, adiamento, retomada, canal físico | Termos usam informação comunicada; benefícios anunciados dependem de recursos e execução posteriores. |
| Facções | Capacidades derivadas; compra, suprimento, patrulha, apoio a proposta, resposta a restrição e incursão com recursos próprios | Treinamento especializado, escolta remunerada e contratos CityContract extensos não foram adicionados; alguns caminhos reutilizam ações anteriores. |
| Crime e lei | Crimes próprios/reconhecidos e confiança permitem cooperação genérica; classificação por cidade e fatos conhecidos; reação institucional | Sem classe Bandit ou guerra automática. Multa, banimento, guerra e todos os modos de negociação não ganharam ciclo completo. |

A pressão usada é `min(100, 2×apoiadores vivos entregues + 0,3×urgência + persistência até 20 + visibilidade (2/10) + crise (0/10))`. Esse valor compete com personalidade e custo: apoio não determina aprovação. Recursos institucionais usam ItemService e dinheiro dos mesmos donos; os setores não mantêm estoques paralelos fictícios.

## Testes controlados e smoke

**28 verificações passaram**: os 14 métodos da Fase 5.5, dez da Fase 5.4 e quatro regressões críticas de alimentação/letalidade. Não houve repetição da suíte histórica inteira. Os controles novos cobrem busca conhecida/desconhecida, incompatibilidade, grupo de 20 pessoas, proposta reutilizada, contagem única entre grupos/facção, pressão no julgamento, reserva monetária sem geração de bens, água/alimento/entrega por rota, falta material, formalização, capacidades, estados de convite e retomada, infrações sucessivas e organização criminosa genérica. Log: `testes_regressoes.log`.

Dois smokes pequenos de 48h usaram mundos reduzidos: o natural teve 77 NPCs, cinco grupos e duas propostas; o controlado teve 69 NPCs, três grupos, três propostas e uma política. Ambos passaram integridade, rotas e ida/volta JSON; seus saves temporários foram apagados automaticamente. `smoke.json` e `smoke_politica.json` conservam apenas resultados.

Esses controles demonstram capacidade sob condições preparadas. Aceite, formalização, ilegalidade, banditismo, produção e transporte controlados não são lore da campanha. A ocorrência natural aparece nas métricas seguintes.

## Falha encontrada e correções

A primeira execução parou na hora **50**, porque o validador ainda rejeitava grupos acima de **16** pessoas, embora a adesão nova permitisse crescimento. Doze grupos acionaram a invariante antiga. O registro mínimo está em `interrompida_50h/falha.json`, com manifesto e log. Não foi preservado um dump completo. O limite foi alinhado a 64 e um controle foi ampliado para validar 20 membros. A campanha foi reiniciada do zero com **a mesma Vaelora-55**.

| Correção | Razão |
| --- | --- |
| Limites de membros e estado ignored no validador | Dados novos precisam ser aceitos pela integridade, preservando os limites de memória anteriores. |
| Avaliação da utilidade de policy_work | O peso financeiro usa a consideração financeira existente, evitando chave ausente no percurso real Need/Goal. |
| Entrega presencial dos apoios | Registrar assinatura num grupo distante não pode elevar instantaneamente a pressão recebida pelo prefeito. |
| Fontes de infrações sucessivas | Uma nova infração deve ser registrada mesmo se RESTRICTED não mudou; a terceira evidência pode levar a ILLEGAL. |
| Proteção de propostas vinculadas a políticas | A limpeza periódica anterior não pode excluir a proposta que uma política ainda referencia. |
| Fundadores presentes | A formalização usa participantes presentes, preservando origens sem transferir pessoas remotas. |

## Campanha natural concluída

**Diferença entre código medido e entrega final:** após a campanha, a revisão constatou que a alternativa `ignore` era sempre matematicamente superada por `reject`. A entrega acrescenta contexto de falta de orçamento/exaustão para tornar ignorar uma decisão possível, e reconsideração quando a pressão recebida aumenta. Também conserva o quadro público de propostas na substituição de prefeito. Os controles 4 e 6 verificam esses ajustes. Eles não foram aplicados retroativamente à campanha, que não teve decisões `ignore`. `versoes.json` identifica os hashes; duas fontes auditadas permitem reconstruir o núcleo medido. Não houve nova campanha nem horas extras.

| Indicador | Resultado |
| --- | --- |
| Escala inicial | 1880 persistentes + 4644 abstratos; 4 reinos, 48 localidades |
| Grupos criados / adesões | 132 / 998 (555 pessoas distintas) |
| Buscas / encontros compatíveis / recusas | 5325 / 1230 / 4273 |
| Grupos finais / maior | 132 / 24 membros |
| Dissoluções / fusões | 18 / 0 |
| Propostas criadas / reutilizações | 46 / 22 |
| Apoios / entregas de apoio / submissões | 261 / 33 / 16 |
| Decisões | partial: 2 |
| Políticas / etapas pagas | 2 / 8 |
| Setores / estados | SECURITY: 2; completed: 2 |
| Materiais consumidos / salários | nenhum; 8 moedas |
| Capacidade hídrica ampliada | 0 localidades |
| Formalizações naturais | 0 |
| Convites / pedidos / aceites | 19 / 0 / 4 |
| Recusas / adiamentos / condições | 1 / 0 / 0 |
| Ações de facção / mudanças legais | 3 / 0 |
| Cooperação criminosa registrada | 0 |
| Mortes | 315; both: 13, combat: 1, hunger: 175, thirst: 126 |
| Integridade / rotas | Zero erros em seis marcos (50–300h); zero erros de rota |
| Tempo da execução | 397.87s |

Apoios são únicos **por proposta**; a mesma pessoa pode apoiar diferentes propostas. Adesões e recusas são contagens de acontecimentos; não representam igual número de pessoas ou grupos redundantes evitados. O registro de apoio entre grupos mostra cooperação. Não houve deduplicação global onisciente nem fusão forçada.

Motivos registrados para recusa de grupo: contact_or_capacity: 146, different_objective: 219, hostility_or_distrust: 3, leader_unavailable: 29, low_social_affinity: 3631, too_many_commitments: 245. Alguns acontecimentos são tentativas repetidas; esses números não representam igual número de pessoas incompatíveis.

## O que os resultados permitem concluir

A integração natural produziu 998 adesões a grupos existentes, 22 reutilizações de propostas e 4 ingressos em facções. Esses resultados distinguem continuidade efetiva de mera criação de objetos. As políticas tiveram 8 etapas pagas; 2 concluídas e 0 paralisadas no encerramento. Aprovação e efeito material permaneceram separados.

A campanha da Fase 5.4 tinha 179 grupos criados, 87 propostas e nenhum ingresso em facção, em 200h, seed Arandor-54, com 1.826 persistentes iniciais. Esta campanha tem outra seed, elenco e duração: a comparação descritiva sugere continuidade onde existia fragmentação, mas não mede isoladamente um efeito causal ou percentual de melhoria. Não foi feita outra campanha comparativa longa.

## Limites e gargalos

**Gargalo observado:** houve 16 grupos de água, mas somente duas propostas WATER, criadas nas horas 94 e 125, ambas ainda em rascunho e sem apoio entregue. Não surgiu política WATER ou FOOD: as duas políticas naturais foram de segurança. Ao final, os representantes de água estavam com fome 90/70 e HP 37/8; um coletava alimento e o outro dormia. Esse retrato final comprova concorrência vital naquele momento, sem reconstituir cada decisão anterior. Das 315 mortes, 314 (99,7%) foram por fome, sede ou ambas.

Uma leitura do save, sem avançar horas, encontrou 14 propostas entregues ainda sem decisão e 13 convites oferecidos com necessidade de adesão ativa. Os responsáveis e candidatos frequentemente estavam exaustos, sem dinheiro pessoal ou atendendo alimentação/recuperação. Um prefeito citado havia morrido no fechamento, antes da próxima rodada de reposição. `diagnostico_gargalos.json` preserva somente esses estados mínimos; não substitui um histórico de decisões. Tesouro municipal e dinheiro do NPC são donos distintos: atender a administração não paga salário automaticamente no código atual.

**Próximos ajustes recomendados:** remunerar serviço administrativo com o tesouro real e trabalho efetivo; permitir representação delegada e resposta institucional com continuidade mesmo quando o líder precisa se recuperar; registrar por que cada tarefa institucional perdeu a disputa de prioridades. Esses caminhos devem ser testados com estoques e dinheiro reais, sem rebaixar necessidades vitais ou garantir aprovação. A hipótese é que reduzam a dependência da disponibilidade de uma única pessoa; esta campanha não mede esse efeito futuro.

- A oferta de trabalho concorre com sede, fome, descanso e compromissos. `no_effective_work` identifica a falta de execução, sem atribuir por si só a culpa a um traço ou NPC específico. Obras dependem de madeira/ferro e de trabalhadores que saibam da política.
- A capacidade hídrica pode responder por obras; esta fase não demonstra equilíbrio demográfico/material definitivo. Mortalidade ou mercados vazios não devem ser tratados como resolvidos por existir uma política.
- Há limite de 24 propostas por administração, 64 membros por grupo/facção, memórias e históricos curtos. Políticas referenciadas são preservadas; ainda falta arquivamento compacto completo para sucessivos anos de campanhas políticas. A execução de 300h não demonstra estabilidade indefinida de memória.
- Fusão negociada, carreira/treinamento institucional completo, todos os contratos administrativos e conflitos territoriais longos continuam fora da implementação mínima. Capacidades declaradas para ações futuras não são prova de execução.
- Não há eleições, guerra entre reinos nem economia paralela. Raridades ausentes naturalmente não justificam reiniciar ou manipular a seed.

## Disco e retenção

Os artefatos regeneráveis foram inventariados antes de qualquer remoção. Foram removidos 377 arquivos grandes de execução, preservando fontes, testes, configuração, baselines de código, documentação, relatórios finais históricos e evidências compactas. O manifesto de limpeza registra caminho, tamanho, tipo e relatório preservado; não foi removida a árvore do projeto.

| Medida (bytes lógicos) | Resultado |
| --- | --- |
| `project_size_before` | 13,973,308,392 bytes (13.97 GB) |
| `project_size_after_cleanup` | 739,818,331 bytes (739.82 MB) |
| Projeto após entrega/retenção | cerca de 741.58 MB |
| `reports_size` | cerca de 734.85 MB |
| Recuperado na limpeza inicial | 13,233,664,141 bytes (13.23 GB) |

Maiores diretórios históricos ainda preservados:

- `reports/fase_3_2`: 217.77 MB.
- `reports/fase_4_5`: 102.06 MB.
- `reports/fase_3`: 100.59 MB.
- `reports/fase_5`: 77.55 MB.
- `reports/fase_4_6`: 68.05 MB.

O save completo de 199.875.217 bytes foi apagado **depois de** gravar e auditar os três relatórios. `retencao.json` registra hash, tamanho e confirmação da remoção. Os eventos retidos em `eventos_relevantes.json` são os usados nas histórias; métricas e `resumo.json` preservam cadastro mínimo, sem mapas, itens completos, memória individual ou milhões de ações. O dump intermediário de eventos também foi removido.

Arquivos principais: [MUNDO.md](MUNDO.md), [HISTORIAS_REAIS.md](HISTORIAS_REAIS.md). Auditoria: `campanha_300h/{manifesto,resumo,metrics,eventos_relevantes}.json`, `testes_regressoes.log`, `limpeza.json` e `auditoria_disco_antes.json`.
