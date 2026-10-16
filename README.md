# Mundo procedural — Fase 5.5: grupos, facções e ação institucional

Jogo de terminal em português, com núcleo da seção 60 de `instruction.md`,
vida pessoal de `fase_2.md` e economia adaptativa conforme `fase_3.md`.
Inclui a correção individual de alimentação, a Fase 3.2, os sistemas de `fase_4.md`
e a recuperação fisiológica descrita em `fase_4_1.md`.
Inclui impulso social e investigação das Fases 4.5/4.6 e o núcleo de `fase_5.md`:
prefeitos e patentes locais, grupos e propostas, facções ativas, fé executável,
divindades separadas de crença, renome, potencial mítico e decisão terminal de combate.
A Fase 5.2 acrescenta decisão letal persistente, reação do matador, afinidade com a morte,
padrões de homicídio conhecidos, afinidade dos deuses, vínculos raros, presença regional
e acompanhamento das camadas religiosas. A campanha de validação tem 500 horas,
com relatório técnico e crônica em `reports/fase_5_2/`.
A Fase 5.2.1 valida a escolha terminal corrigida e diferencia os Actors por domínio,
com uma campanha nova de 1.000 horas, conforme o pedido de ampliação do teste.
O relatório fica em `RELATORIO_5_2_1.md` e a crônica em `reports/fase_5_2_1/HISTORIAS_REAIS.md`.
A Fase 5.4 adapta a geração para quatro reinos e separa conhecimento de lugar,
rota e acesso físico. Inclui viagens com etapas, instruções presenciais, POIs
com estoque real, adesão organizacional e busca de contato divino. A validação
natural foi limitada a 200 horas, com três relatórios em `reports/fase_5_4/`:
`HISTORIAS_REAIS.md`, `RELATORIO_TECNICO.md` e `MUNDO.md`.
Python 3.11 ou superior; somente biblioteca padrão. O documento original permanece
como especificação do projeto.

A Fase 5.5 usa `mvp-12-fase5.5` nas regras e saves, mantendo a geração geográfica
da Fase 5.4. Grupos conhecidos recebem adesões; propostas compatíveis concentram
apoio de pessoas únicas, entregue fisicamente à autoridade. Políticas reservam
dinheiro, oferecem trabalho e dependem de materiais, profissionais e acesso.
Convites mantêm decisão, condição e retomada; a lei das facções varia por localidade
e depende de fatos conhecidos. A especificação recebida está em `fase_5_5.md`.

Os três relatórios atuais ficam em `reports/fase_5_5/`: `RELATORIO_TECNICO.md`,
`MUNDO.md` e `HISTORIAS_REAIS.md`. A auditoria usa uma campanha nova de 300 horas,
sem jogador, seed `Vaelora-55`; não continua saves anteriores. Uma interrupção
estrutural na hora 50 está documentada, com reinício na mesma seed.

**Retenção:** nesta fase, saves e dumps grandes regeneráveis das campanhas antigas
foram removidos após inventário, preservando os relatórios históricos e evidências
compactas. As referências antigas a saves preservados descrevem a entrega daquela
fase. Após auditar os três relatórios novos, o save completo novo também é removido;
ficam métricas, eventos selecionados e manifestos. Saves de jogo do usuário não
fazem parte dessa limpeza de artefatos em `reports/`.

```bash
python3 -m procedural --seed Dovha --nome Hugo
```

O jogador começa na posição de uma capital no mapa externo. Use `entrar`,
`listar` e `conversar ID`. `rotas` consulta as conexões conhecidas;
`perguntar_rota LOCAL_ID` procura instruções presenciais e `viajar LOCAL_ID`
inicia ou continua uma viagem com mantimentos reais. `ajuda` mostra os comandos.
As coordenadas são `(x, y)`;
norte reduz `y`. O mapa 5×5 fica no canto superior direito da interface.

Cada movimento ou ação bem-sucedida consome um turno de uma hora. Consultas,
ações inválidas, salvar e carregar não avançam o tempo. `esperar 24` simula um dia.
`salvar campanha.json` e `carregar campanha.json` preservam a campanha completa.

Para executar o mundo sem jogador:

```bash
python3 -m procedural --seed Vaelora-55 --simular 300
PYTHONPATH=tests python3 -m unittest test_phase55 test_phase54
```

## Regras do MVP

- Mundo finito 500×500; quatro reinos, cada um com uma capital, quatro outras
  cidades e seis a oito vilas subordinadas, biomas e pontos de interesse.
  Capitais têm maior população e área. Cidades e interiores têm matrizes
  próprias, muralhas e portões. Distâncias são configuráveis.
- Seed textual vinculada a um NPC real. Geração e simulação usam uma única fonte
  de aleatoriedade, derivada de SHA-256 e da versão das regras.
- Necessidades geram prioridades, alternativas pontuadas pela personalidade,
  objetivos e ações. Rotinas profissionais cedem a necessidades urgentes.
- Profissões produzem recursos e itens, consomem materiais, recebem salários e
  patrulham. Estoques, dinheiro e preços são reais e regionais.
- Conhecimento e memória são individuais. Eventos são percebidos localmente;
  rumores percorrem um contato por rodada. Diálogos usam apenas conhecimento do
  interlocutor. Pedidos de comida surgem de necessidades reais e podem virar quests.
- Famílias e relações usam IDs em um grafo dirigido. Fé, confiança, lealdade,
  popularidade e reputação contextual são campos separados.
- O motor funciona sem interface e sem IA generativa. NPCs distantes atualizam
  decisões em intervalos maiores; necessidades fisiológicas continuam avançando.
- Saves JSON versionados incluem matrizes, entidades, relações, necessidades,
  objetivos, memórias, economia, eventos e estado do gerador aleatório.

## Organização

`models` contém dados; `generation` cria o mundo; `needs` e `goals` fazem a
tomada de decisão; `professions`, `economy` e `items` executam as regras de
produção e comércio. `knowledge`, `relationships`, `events` e `quests` tratam
as consequências sociais. `navigation` cuida das matrizes; `geography` trata
conexões e viagens conhecidas; `access` integra POIs, organizações e contato
divino às decisões. `engine` coordena
os serviços e recebe comandos. `persistence` salva dados; `ui` apenas apresenta
resultados e encaminha comandos.

Combate por membros, guerras com exércitos, herança,
boatos falsificados deliberadamente e dinastias completas são
etapas posteriores. A história inicial registra fundações e um período limitado
de simulação econômica; não força a destruição de um reino.

População abstrata consome e compra alimentos em lotes diários. Produção rural
representa recursos renováveis, com limite de estoque. Não há simulação de cada
habitante abstrato. Memórias, conhecimento cotidiano e eventos recentes têm
limites de retenção; acontecimentos históricos importantes ficam na crônica.

Os testes executados e os limites atuais estão descritos em [VALIDACAO.md](VALIDACAO.md).

## Correções das regras (mvp-2)

Descanso usa a mesma fisiologia para jogador e NPCs: fome ou sede severa reduzem
cura; estado crítico impede cura; privação total causa dano crescente. Os poços
conhecidos nas casas e na área rural também utilizam o estoque de água da cidade.

O mercado possui valor de referência e preços separados de compra e venda.
Lotes percorrem a curva de estoque unidade por unidade. O preço mostrado é para
uma unidade; um lote pode custar mais que esse preço multiplicado pela quantidade.
Revender percorre a curva inversa, com spread, sem gerar lucro no mesmo mercado.
Renda abstrata é uma fonte explícita de moeda; compras, salários, multas e subsídios
são transferências. Preparar alimentos converte trigo; consumo remove bens.

Além de comprar, você pode `coletar` na área rural A, `trabalhar` em A por uma
ração (exige trigo local) e `pedir comida ID` a um NPC presente. Todas essas ações
usam serviços compartilhados com os NPCs. Coleta esgota uma reserva local renovada
diariamente; pedidos dependem da disposição de quem recebe.

Conversas aumentam familiaridade. Confiança e reputação dependem de ajuda útil,
personalidade, urgência e qualidade da informação. Um registro persistente por
fato impede aplicar novamente o mesmo favor após o esquecimento ou o load. Uma
fonte melhor pode atualizar apenas a diferença do efeito já registrado.
Boa reputação altera a escolha de interlocutores e a disposição de dar comida.
NPCs podem escolher pedir ajuda ao jogador; o pedido pendente não interrompe
suas outras tentativas de sobrevivência. Recusas produzem consequências contextuais.

Reinos possuem estados político, econômico, militar e social independentes.
O campo `status` é um resumo somente para leitura. Para investigar decisões,
ative `engine.goals.debug = True` e consulte `engine.goals.traces[npc_id]`.

```bash
python3 -m experiments.hardening_validation --seed Dovha
python3 -m experiments.hardening_validation --seed Mira
python3 -m experiments.hardening_validation --seed Arven
python3 -m experiments.survival_campaign
```

As correções desta seção foram introduzidas em `mvp-2`. Na etapa de alimentação,
os saves usavam `mvp-4-alimentacao`. A versão atual é `mvp-11-fase5.4`;
saves de versões anteriores são recusados explicitamente. Os
relatórios das campanhas anteriores continuam preservados como evidência histórica.
A reposição profissional foi acrescentada no escopo limitado da fase 3 abaixo.
Veja o diagnóstico histórico em [RELATORIO_HARDENING.md](RELATORIO_HARDENING.md).

## Fase 2

Reutiliza `Need`, `Goal`, prioridade, utility, conhecimento, grafo, eventos e quests.
Acrescenta ambição, vingatividade e temperamento estável, mantendo honestidade e
predisposição familiar existentes. Não há um sistema emocional completo.

Observações locais podem gerar cuidado familiar ou busca após ausência percebida.
Morte conhecida pode gerar luto; dano conhecido pode gerar busca não violenta de
informação/reparação. Proteção, reconhecimento e ascensão competem com as pressões
fisiológicas. Renda persistente amplia `money`, sem criar uma necessidade financeira
paralela. Necessidades possuem fonte, motivo, alvo, fechamento e prazo; podem ficar
bloqueadas quando faltam alternativas.

As ações da hora precedem a passagem do tempo, fisiologia e morte para jogador
e NPCs. Compra e pedido de comida compartilham viabilidade observável. Intenções
inválidas não criam necessidades/IDs, e rumores podem reforçar fatos já conhecidos
sem duplicar reputação.

Novos comandos: `fatos`, `investigar NPC_ID`, `informar NPC_ID FACT_ID` e
`acompanhar NPC_ID`. Investigação confirma somente pessoas ou restos presentes
na posição atual. Informações transmitidas respeitam fonte e confiança. Pedidos
devem ser respondidos num encontro com o solicitante.

```bash
python3 -m unittest discover -s tests -v
python3 -m experiments.phase2_audit --seed Dovha --turnos 10000 --output reports/fase_2/auditoria_10000_final
```

O debug `engine.goals.debug = True` agora mostra pressões ativas, fontes,
prioridades e considerações dos candidatos. Nenhum peso de fome foi reduzido
para impor uma distribuição de comportamentos.

`mvp-3` não migra saves antigos: os novos campos e a semântica temporal justificam
incompatibilidade explícita. Saves e relatórios anteriores permanecem preservados.
Como a versão participa da seed, a geografia inicial muda entre versões.

Resultados, exemplos de histórias e limitações da campanha de 10.000 turnos:
[RELATORIO_FASE_2.md](RELATORIO_FASE_2.md).

Três campanhas posteriores, como jogador, espectador e observador de todo o mundo:
[relatório das três perspectivas](reports/tres_perspectivas_20261007/RELATORIO.md).

Análise das causas da predominância de sobrevivência, funcionalidades pendentes
e sugestões de solução:
[abastecimento e continuidade das histórias](RELATORIO_ABASTECIMENTO_E_CONTINUIDADE.md).

## Fase 3

Diagnóstico local distingue matéria-prima, capacidade, mão de obra, poder de compra,
acesso, estoque bloqueado e transporte. Trabalho avulso, produção parcial e salários
proporcionais usam bens e dinheiro reais. A alternativa de renda para obter comida
usa preço observado; cotação desconhecida permite visitar o mercado para verificar.

A cadeia adaptativa é trigo → alimento: cidades publicam trabalho temporário e
formação de cozinheiros. Residentes existentes podem aprender com prática produtiva.
Só depois de uma falta persistente, sem candidato adequado e com reservas, uma
pessoa abstrata pode tornar-se um novo aprendiz persistente. O censo conserva
`população viva = abstratos + residentes persistentes vivos`; mortes são contadas
uma vez. Não há reposição de governantes nem formação completa de todas as carreiras.

Prevenção de viagem usa fontes e cotações conhecidas. Instrumentação registra
condições de morte e separa perda por prioridade, falta de solução, expiração e
morte do dono de necessidades pessoais. Fisiologia e prazos sociais foram preservados.

```bash
python3 -m unittest discover -s tests -v
python3 -m experiments.phase3_scenarios
python3 -m experiments.phase3_audit --mode jogador --seed Dovha --turnos 10000 --output reports/fase_3/nova_campanha_jogador
python3 -m experiments.phase3_audit --mode espectador --seed Dovha --turnos 10000 --output reports/fase_3/nova_campanha_espectador
python3 -m experiments.phase3_audit --mode mundo --seed Mira --turnos 10000 --output reports/fase_3/nova_campanha_mundo
```

Relatório de implementação, comparação e limites: [RELATORIO_FASE_3.md](RELATORIO_FASE_3.md).
Diagnóstico específico das mortes por fome, com reprodução das três campanhas e
exemplos de decisões: [RELATORIO_FOME_E_MORTES.md](</home/hugo/Área de trabalho/procedrual/RELATORIO_FOME_E_MORTES.md>).
Unidades e contratos: [modelo econômico](reports/fase_3/MODELO_ECONOMICO.md).
Histórias realmente observadas: [HISTORIAS.md](reports/fase_3/HISTORIAS.md).
Os saves e registros das três campanhas estão em `reports/fase_3/auditorias/`.
As campanhas que revelaram as confusões entre cotação, estoque e renda foram
preservadas em `reports/fase_3/auditorias_pre_correcao/` e
`reports/fase_3/auditorias_pre_correcao_estoque/`.

Os saves anteriores continuam intactos, com incompatibilidade explícita; não há
migração automática. Nas mudanças entre fases antigas, a versão participava da seed,
portanto a comparação histórica não isolava causalmente cada alteração. A fase cria mecanismos de recuperação,
mas não garante que toda cidade ou todo NPC sobreviva.

## Correção alimentar individual

Esta etapa antecede a Fase 4. Distingue reserva preventiva de 24 horas (normalmente
duas rações), refeição com fome a partir de 50 e emergência. Comida vital pode
interromper objetivos; caminhos alimentares que demoram mais que a margem de
sobrevivência são rejeitados. Compra para reserva continua distinta de consumo.
`refeicao` (ou `refeição`) compra e consome uma ração real no mercado em uma hora.

Os parâmetros estão em `rules.FEEDING`. Crescimento de fome, dano, cura, estoques
e regras de salário não foram facilitados. A versão de geração permanece `mvp-4`,
conservando geografia e elenco anteriores à história inicial; regras/saves usam
`mvp-4-alimentacao`. As decisões da história inicial já respondem à correção.

Passaram 130 testes e três campanhas de 10.000 horas. Não houve morte por fome
com alimento possuído nessas campanhas; reserva efetiva e acesso econômico ainda
são limitados. O relatório apresenta os resultados e essas limitações:
[RELATORIO_CORRECAO_ALIMENTAR.md](</home/hugo/Área de trabalho/procedrual/RELATORIO_CORRECAO_ALIMENTAR.md>).
As [12 histórias selecionadas](</home/hugo/Área de trabalho/procedrual/reports/correcao_alimentar/HISTORIAS_EMERGENTES.md>)
também estão separadas para leitura. Evidências, saves e métricas ficam em
`reports/correcao_alimentar/`; as campanhas anteriores permanecem preservadas.

```bash
python3 -m experiments.feeding_audit --mode jogador --turnos 10000 --output reports/correcao_alimentar/nova_jogador
python3 -m experiments.feeding_audit --mode espectador --turnos 10000 --output reports/correcao_alimentar/nova_espectador
python3 -m experiments.feeding_audit --mode mundo --turnos 10000 --output reports/correcao_alimentar/nova_mundo
```

Use diretórios novos e vazios para campanhas adicionais. O auditor recusa
sobrescrever resultados e verifica a assinatura das regras congeladas.

## Fase 4 (`mvp-5-fase4`)

NPCs e jogador podem confrontar, ameaçar, atacar, defender, fugir, render-se e
prestar auxílio limitado. Os NPCs avaliam essas alternativas nas necessidades
existentes; raiva não executa ataques automaticamente. Ferimentos afetam combate,
trabalho e movimento. Descanso adequado recupera ferimentos gradualmente;
`socorrer ID` consome uma provisão e água reais.

No terminal: `atacar ID`, `defender`, `fugir`, `render`, `recuar`, `confrontar ID`,
`ameacar ID`, `cobrar ID`, `avisar ID`, `insultar ID`, `desculpar ID`, `acalmar ID`,
`perdoar ID`, `socorrer ID`. `capturar ID` exige guarda com evidência conhecida,
alvo presente e rendido ou incapacitado. Cada tentativa válida consome uma hora,
inclusive uma fuga que falha. Rendição e detenção restringem movimento/violência;
o personagem ainda pode cuidar de suas necessidades acessíveis.

Autoridades possuem informação individual sobre casos, gravidade e última
posição conhecida. Migração atravessa portões e o mapa externo; chegada é visita,
e residência só muda após 24h no destino. Quem muda precisa de provisões e uma
rota conhecida. Há um período de adaptação antes de considerar outra mudança.

O mundo completo padrão usa quatro vezes o elenco original. Mira começa com
1.728 persistentes e 4.338 abstratos, mantendo seis reinos, 73 localidades e a
geografia anterior. Esta decisão redimensiona o total populacional para manter
2–3 abstratos por persistente. Mundos reduzidos de um a cinco reinos conservam
por padrão a densidade dos cenários anteriores; `GenerationConfig` permite
escolher explicitamente `density_multiplier` de 1 a 6.

Fórmula do dano: `(4 + bônus_da_arma) × (0,5 + HP/200) × (1 − ferimento/250)`,
com bônus `min(12, dano_da_arma × (0,5 + qualidade/200))`, variação inteira
entre −2 e +2 e multiplicador defensivo 0,45. Dano mínimo 1; coragem afeta escolha,
e não força física. O adversário é avaliado pela aparência aproximada da arma e
pelos sinais visíveis, sem consultar sua qualidade exata para decidir.

Saves antigos continuam preservados, porém o carregador exige a versão atual.
Para ler ou executar a versão anterior, use o núcleo preservado em
`reports/fase_4/baseline_code`. A auditoria oficial, métricas, relatório e
histórias estão em `reports/fase_4` e `RELATORIO_FASE_4.md`.

A campanha única completou 10.000h. Sua verificação de continuidade revelou
um bug em casos criminais acumulados, corrigido depois da campanha. Os 20 testes
direcionados passaram novamente, e o save final passou por uma verificação curta
de continuidade com recarga no meio. O código auditado e o corrigido estão
preservados separadamente; o relatório distingue os resultados de cada versão.

## Fase 4.1 (`mvp-5-fase4.1`)

Refeições normais passam a ser consideradas a partir de fome 35, com pressão
progressiva. Reserva preventiva continua separada e o alvo normal permanece em
duas rações. Em emergência, aquisição e consumo são estimados em conjunto;
roubo pessoal participa da mesma cadeia alimentar de compra, coleta e ajuda.
A comida precisa existir e ser transferida antes de ser consumida.

HP abaixo de 80 gera necessidade de recuperação, mesmo sem lesão. O NPC pode
buscar alimento/água, voltar para casa e descansar ou procurar tratamento para
ferimentos. HP crítico reduz a disposição para trabalho pesado e conflitos
voluntários; defesa e necessidades vitais continuam possíveis. Fome no limiar
normal antecipa decisões para até três horas; HP abaixo de 30 promove decisões
horárias, pela mesma agenda existente.

O HP continua único. Dano realmente sofrido por fome/sede entra num registro
recuperável; combate fica separado. Descanso seguro recupera esse dano a
8/4/1 HP por hora conforme a maior entre fome e sede seja até 50/70/80.
A cura física continua usando as regras anteriores. Um único orçamento impede
somar as duas curas indevidamente. Comer ou comprar não restaura HP.
O desespero material pode diminuir gradualmente em condições estáveis; luto e
agravos pessoais conservam suas causas.

Há dez regressões novas em `tests/test_phase41.py`. A comparação curta usa dois
mundos novos Vespera-47 de 500h, com os núcleos anterior e atual preservados em
`reports/fase_4_1/baseline_code` e `reports/fase_4_1/final_code`.
O relatório e as evidências da campanha longa ficam em `reports/fase_4_1`.

```bash
python3 -m experiments.phase41_audit --hours 500 --folder reports/minha_auditoria_41
```

Esse comando sempre gera um mundo novo; exige pasta vazia, registra versão/hash
e exporta um save ao terminar. Não carrega nem sobrescreve os saves anteriores.

A auditoria longa terminou em 5.000h. Leia [o relatório da Fase 4.1](RELATORIO_FASE_4_1.md)
e [as histórias reais](reports/fase_4_1/HISTORIAS_REAIS.md).
A mortalidade e o HP geral melhoraram, mas a recuperação de episódios críticos
em até 72h continua limitada; os resultados não encerram todo o ciclo alimentar.

## Fase 4.5 (`mvp-6-fase4.5`)

Especificação em `fase_4_5.md`. Compromissos preservam intenções e fatos causais
através de interrupções; impulso e agência percebida influenciam Need/Utility,
sem executar ações por conta própria. Aspirações derivam dos traços e da condição
pessoal. Conflitos distinguem afastamento, contenção, submissão, ferimento e
intenção letal, mantendo a fórmula física de dano.

Casos formais podem circular entre guardas pelo serviço local no mercado, com
latência e até três tarefas distintas. Pistas conhecidas permitem viagens físicas
sem alterar residência ou revelar posições remotas. Os estados novos entram no
save; campanhas antigas permanecem preservadas e exigem a versão correspondente.

Resultados e limites: [relatório da Fase 4.5](RELATORIO_FASE_4_5.md).
[Histórias reais e decisões dos NPCs](reports/fase_4_5/HISTORIAS_REAIS.md)
incluem abandono, objetivos pendentes e fatalidades. As 227 regressões passaram;
a entrega foi validada em 500h. Uma longa de 5.000h preserva o código anterior
aos cinco ajustes finais encontrados na revisão. Nela, a mortalidade piorou
frente à Fase 4.1; continuidade não significa fome resolvida ou histórias profundas.
Esta fase não adiciona política, guerra ou religião.

## Fase 4.6 — investigação e escalada fatal

A especificação está em `fase_4_6.md`; a versão de regras/save é `mvp-7-fase4.6`.
`lethality` avalia motivos dirigidos e barreiras antes de considerar matar. Intenção
não modifica dano ou armas. Incapacidade comum encerra combate; a decisão letal
sustentada exige nova escolha moral, incluindo poupar.

`investigation` permite buscar pessoas usando memória, fontes presentes e locais
conhecidos. Pistas conservam fonte, idade e confiança; buscas esgotadas entram em
`waiting_for_information`, preservando causa e rotina. Informação útil reativa a
Need, sem ação automática. Guardas depositam pistas no serviço local e as recebem
após a latência institucional. Viagem e retorno continuam físicos.

Relatório técnico: `RELATORIO_FASE_4_6.md`. Histórias e falhas observadas:
`reports/fase_4_6/HISTORIAS_REAIS.md`. Evidências da única longa de 5.000 horas:
`reports/fase_4_6/global_5000h`. As curtas diagnósticas ficam preservadas e a curta
do código congelado da longa está em `reports/fase_4_6/curta_validacao_final_500h`.

## Fase 5 — comandos e validação

`crencas`, `renome`, `grupos` e `organizacoes` mostram apenas informações
conhecidas pelo jogador. `cargos` consulta a administração no mercado local.
`orar ID`, `ofertar ID`, `difundir_fe ID` e `reavaliar_fe ID` executam ações
religiosas sobre um sujeito conhecido. `compartilhar_problema`, `organizar`,
`aderir_grupo ID`, `reunir_grupo ID` e `apresentar_proposta ID` reutilizam as
mesmas condições de encontro, afinidade e representação dos NPCs.

Fama e adoração não criam divindade. Um potencial mítico nasce raro, precisa
de desenvolvimento e não garante destino. Apropriação de essência divina é
separada da morte do deus. Finalização deliberada válida encerra a vida sem
repetir uma rolagem de dano; intenção, incapacidade e decisão são estados distintos.

A Fase 5 usa saves `mvp-8-fase5`. Saves de fases anteriores continuam vinculados
aos respectivos motores preservados; não há conversão automática de campanhas.
O documento recebido foi preservado integralmente em `fase_5.md`.

A auditoria e suas limitações estão em `RELATORIO_FASE_5.md` e as histórias
observadas em `reports/fase_5/HISTORIAS_REAIS.md`.

Os 275 testes passaram no código de entrega, incluindo 30 regressões novas.
A curta de entrega terminou em 500h, seed Serevan-5, sem erros de integridade:
26 mortes, contra 19 na curta anterior. A única longa, seed Nhalven-5, terminou
em 5.000h com 293 mortes e zero erros de integridade. Ela preserva o núcleo
anterior aos ajustes finais de continuidade divina, residência municipal e
adesão; a curta posterior valida o núcleo entregue. Códigos e métricas estão
identificados separadamente em `reports/fase_5/ENTREGA_FINAL.json`.

## Fase 5.1 — entrega atual

A versão atual usa saves `mvp-9-fase5.1`; o texto recebido está em `fase_5_1.md`.
ActionPressure é contextual, com causa conhecida, capacidade e continuidade
separadas. Representação de vilas e retorno de respostas usam deslocamento
físico. Facções podem preparar recursos, cumprir serviços e realizar incursões
limitadas; deuses consideram perdas de fé recebidas, com custo e oportunidade.

Passaram 11 testes novos, oito verificações críticas antigas e oito regressões
da letalidade. A suíte antiga de 275 não foi repetida. A única campanha nova
teve marco de 200h e continuou até 1.000h, seed Selvaren-51, com um save final.
Produziu 134 entregas de propostas, 59 decisões e 183 mortes; 182 por fome.
Não produziu ações organizacionais ou intervenções divinas naturais.

Os ajustes finais passaram nos controles; a campanha conserva o núcleo anterior
a eles. Hashes, limitações, métricas e tamanhos estão em
`RELATORIO_FASE_5_1.md` e `reports/fase_5_1/ENTREGA_FINAL.json`.
Os sete episódios naturais selecionados estão em
`reports/fase_5_1/HISTORIAS_REAIS.md`.

Na longa houve grupos, decisões locais, epítetos e veneração de mortais,
mas não surgiram apoteoses, mortes divinas, crescimento de facções ou execuções
deliberadas. Capacidade controlada e ocorrência natural são resultados distintos.
