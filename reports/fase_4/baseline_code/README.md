# Mundo procedural — correção alimentar anterior à Fase 4

Jogo de terminal em português, com núcleo da seção 60 de `instruction.md`,
vida pessoal de `fase_2.md` e economia adaptativa conforme `fase_3.md`.
Inclui a correção individual de alimentação descrita em `correcao_alimentar.md`.
Python 3.11 ou superior; somente biblioteca padrão. O documento original permanece
como especificação do projeto.

```bash
python3 -m procedural --seed Dovha --nome Hugo
```

O jogador começa na posição de uma capital no mapa externo. Use `entrar`,
`listar` e `conversar ID`. `ajuda` mostra os comandos. As coordenadas são `(x, y)`;
norte reduz `y`. O mapa 5×5 fica no canto superior direito da interface.

Cada movimento ou ação bem-sucedida consome um turno de uma hora. Consultas,
ações inválidas, salvar e carregar não avançam o tempo. `esperar 24` simula um dia.
`salvar campanha.json` e `carregar campanha.json` preservam a campanha completa.

Para executar o mundo sem jogador:

```bash
python3 -m procedural --seed Dovha --simular 10000
python3 -m unittest discover -s tests -v
```

## Regras do MVP

- Mundo finito 500×500; seis reinos com quatro a seis cidades cada, uma capital
  maior, vilas, biomas e pontos de interesse. Cidades e interiores têm matrizes
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
as consequências sociais. `navigation` cuida das matrizes. `engine` coordena
os serviços e recebe comandos. `persistence` salva dados; `ui` apenas apresenta
resultados e encaminha comandos.

Combate por membros, guerras com exércitos, intervenção
divina, herança, religião organizada, rumores falsos e dinastias completas são
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

As correções desta seção foram introduzidas em `mvp-2`. Os saves atuais usam
`mvp-4-alimentacao`; saves `mvp-1`, `mvp-2`, `mvp-3` e `mvp-4` são recusados explicitamente. Os
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
