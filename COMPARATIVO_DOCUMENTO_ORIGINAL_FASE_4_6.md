# Comparativo do documento original com a versão atual — Fase 4.6

**Data:** 9 de outubro de 2026. **Versão examinada:** `mvp-7-fase4.6`. **Geração:** `mvp-4`.

O núcleo do primeiro MVP está presente e recebeu uma camada funcional de vida pessoal, recuperação, conflitos, investigação e perseguição. **A visão completa do documento original ainda está parcialmente implementada.** A maior lacuna atual está na capacidade de organizações e reinos tomarem decisões e transformarem o mundo: facções ativas, diplomacia, guerras, continuidade dinástica, religião e deuses.

## 1. Qual documento foi comparado e como a conferência foi feita

Não há um arquivo chamado `document.md` na raiz deste projeto. O documento original disponível é [instruction.md](</home/hugo/Área de trabalho/procedrual/instruction.md>), também identificado como especificação original pelos comparativos históricos do próprio projeto. **Este relatório usa esse arquivo; não presume ter lido outro documento com nome diferente.** Se `document.md` for uma revisão distinta fora desta pasta, suas diferenças não estão incluídas aqui.

Foram conferidos o documento original, os módulos atuais de `procedural/`, as especificações das fases posteriores e as evidências já concluídas da Fase 4.6. Os arquivos Python atuais são idênticos aos do núcleo congelado da auditoria final. Assinatura registrada nessa auditoria: `e3866d29db349cbfc963bc0a7cd0036e65b9577a0f7cb16707a2f4a787b43c96`.

Não foi alterado o motor, carregado um save, rodada uma campanha ou repetida a suíte de testes para produzir este comparativo. Os números abaixo são resultados preservados das auditorias anteriores, identificados por versão.

### Significado das classificações

| Classificação | Critério |
|---|---|
| **Implementado** | Existe execução concreta do comportamento descrito na linha. Quando a linha especifica “básico”, a classificação se refere a esse alcance. |
| **Parcial** | Há uma parte funcional, mas faltam elementos relevantes da visão original. Campos, rótulos e entidades sem comportamento também ficam aqui, explicitamente identificados como base de dados. |
| **Não implementado** | O comportamento específico ainda não possui um mecanismo executável no motor. Uma ferramenta de relatório não conta como sistema de jogo. |
| **Mudado** | A solução atual difere da proposta original, ou fases posteriores acrescentaram uma regra nova. É uma segunda informação: um sistema pode ser parcial **e** ter sido mudado. As mudanças estão detalhadas na seção 6. |

“Implementado” não significa “perfeitamente equilibrado” nem “demonstrado em toda campanha”. Por exemplo, há escolha letal no código, mas a última campanha não produziu homicídio deliberado. Essa diferença é apresentada separadamente.

O original repete os capítulos de necessidades, reinos e reputação. A reputação reaparece extensamente dentro do trecho de popularidade; as exigências repetidas foram contadas conceitualmente uma única vez. Existem lacunas na numeração: não foram inventadas funcionalidades para preencher números ausentes. Nascimento/envelhecimento aparece sem uma regra final definida; sua ausência é registrada sem tratá-la como descumprimento de uma especificação pronta.

## 2. O primeiro MVP solicitado foi entregue?

A [seção 60 do original](</home/hugo/Área de trabalho/procedrual/instruction.md:5930>) pede 21 componentes. Todos possuem representação no projeto atual, mas **facções simples ainda são sobretudo uma estrutura inicial**, e a existência dos componentes não equivale à realização de toda a visão do jogo.

| Componente solicitado no primeiro MVP | Estado atual | Alcance real |
|---|---|---|
| Seed determinística | Implementado | Seed textual, RNG controlado e estado persistido. Geração e regras agora têm versões separadas. |
| Mapa procedural | Implementado no alcance básico | Mundo 500×500, biomas, reinos, cidades, vilas e interiores; diversidade interna limitada. |
| Movimentação em matriz | Implementado | Quatro direções, obstáculos, portões e passagem entre mapas. |
| NPCs | Implementado | Pessoas persistentes com recursos, personalidade, profissão, relações, decisões e morte. |
| Entity IDs | Implementado | Referências usam IDs estáveis; nomes repetidos são permitidos. |
| Personalidade | Implementado no alcance básico | Onze traços numéricos influenciam soluções; emoções são estados separados. |
| Necessidades | Implementado no alcance básico | Sobrevivência, renda, família, perdas, proteção, reconhecimento, ascensão, conflito, recuperação e migração. |
| Prioridades | Implementado | Pressões concorrentes, contexto, urgência, relações, personalidade e segurança vital. |
| Objetivos | Implementado | Alternativas executáveis, deslocamento, falha, reavaliação e interrupção. |
| Profissões básicas | Implementado | Produção, materiais, pagamento e serviços; não inclui todas as profissões da visão final. |
| Relacionamentos | Implementado no alcance básico | Grafo dirigido, família, casamento inicial, amizade, confiança e lealdade. |
| Memória básica | Implementado | Memória individual limitada, registro dos efeitos já aplicados e fatos preservados por compromissos. |
| Conhecimento | Implementado no alcance básico | Percepção local, fonte, confiança, rumor, informação antiga e investigação. |
| Itens | Implementado no alcance básico | Itens com ID, tipo, qualidade, raridade, origem, criador e dono. |
| Inventário | Implementado no alcance básico | Referências, quantidades, consumo, transferência, compra e venda. |
| Economia básica | Implementado | Estoques reais, produção, consumo, dinheiro, salários, preços locais e respostas alimentares. |
| Facções simples | Parcial — principalmente dados | Nome, líder, sede e filiação; falta atuação autônoma da organização. |
| Reinos simples | Implementado no alcance básico | Território inicial, localidades, governantes, sucessão e tesouro; governo estratégico continua parcial. |
| Event Bus | Implementado | Eventos internos alimentam conhecimento, necessidades e consequências. |
| Save e Load | Implementado na própria versão | Mundo e RNG persistidos; versões antigas são recusadas, sem migração geral. |
| Interface textual | Implementado | Terminal, mapa 5×5 à direita, consultas e comandos; motor separado da interface. |

**Avaliação:** o projeto já supera o primeiro MVP em interação e vida pessoal. Isso não significa que a seção de facções, os sistemas militares ou os sistemas religiosos estejam concluídos.

## 3. Funcionalidades originais implementadas

Estas linhas isolam comportamentos que já existem. Os sistemas mais amplos dos quais fazem parte podem continuar parciais, como mostrado na seção seguinte.

| Funcionalidade original | O que o motor faz hoje | Referência principal |
|---|---|---|
| Mundo finito e geração controlada | Gera o mapa 500×500, até seis reinos, quatro a seis cidades por reino, uma capital e vilas próximas. | `generation.py` |
| Geografia em múltiplas matrizes | Mantém mapas global, urbanos e interiores, associados por entradas/saídas. | `generation.py`, `navigation.py` |
| Distâncias configuráveis entre pontos | Evita gerar pontos relevantes sem respeitar a separação mínima configurada. | `GenerationConfig`, `choose_position` |
| Locomoção cardinal com obstáculos | Bloqueia muralhas e permite entrada/saída pelas condições espaciais reais. | `Navigation` |
| Um turno corresponde a uma hora | Ações válidas fazem o relógio avançar; o mundo acompanha. Consultas não gastam hora. | `Engine.step`, `Engine.execute` |
| Mundo funciona sem jogador | `simulate` avança decisões, fisiologia, economia, informação e consequências sem jogador presente. | `Engine.simulate` |
| Jogador com vida, inventário e identidade | Começa com HP 100, título “Desconhecido”, inventário próprio e sem facção. | `Character`, `generate_world` |
| NPC ligado à seed existe no mundo | O personagem primordial é um governante persistente, com ID e possibilidade de morrer. | `generate_world` |
| IDs independentes dos nomes | NPCs, localidades, itens, eventos e relações usam referências estáveis. | `WorldState.allocate_id` |
| Família e sobrenome coerente na geração | Produz vínculos familiares e casamentos iniciais; famílias densificadas compartilham sobrenome. | `generate_world`, `RelationshipGraph` |
| Grafo de relações | Armazena casamento, parentesco, amizade, confiança, lealdade e relações diplomáticas iniciais. | `RelationshipGraph` |
| Necessidade é pressão, não ordem automática | Need, prioridade, soluções, Goal e execução são etapas distintas. Fome ou raiva não executam uma ação diretamente. | `NeedSystem`, `GoalSystem` |
| Concorrência e falha de objetivos | Avalia alternativas disponíveis, risco/custo/distância, registra impedimentos e pode buscar outra solução. | `GoalSystem`, `utility.py` |
| Trabalho cede a necessidades relevantes | Rotina profissional participa da competição por prioridade; não obriga trabalhar durante toda crise. | `NeedSystem.refresh` |
| Conhecimento individual | NPC aprende acontecimentos que presencia ou recebe; informação global não é distribuída automaticamente. | `KnowledgeSystem` |
| Propagação por contato | Rumores passam entre interlocutores espacialmente próximos; a transmissão não percorre uma cadeia inteira no mesmo ciclo. | `KnowledgeSystem.gossip` |
| Fonte e confiança da informação | Distingue informação direta, conhecida, confiável e rumor; retransmitir não restaura certeza perdida. | `KnowledgeSystem.learn`, `transmitted` |
| Pedidos surgem de necessidades reais | Necessidade elegível pode virar pedido ao jogador; recusa mantém a possibilidade de outras soluções. | `QuestSystem` |
| Produção profissional concreta | Agricultor, cozinheiro, ferreiro, mineiro, lenhador e caçador produzem bens; guardas/comerciantes exercem serviços. | `ProfessionSystem.work` |
| Comércio e consumo com recursos reais | Comprar/vender transfere bens e moeda; comer remove comida; fabricar arma consome madeira e ferro. | `Economy`, `ItemService`, `ProfessionSystem` |
| Popularidade, reputação, confiança e medo separados | Opiniões individuais possuem tags, fontes, popularidade, admiração e medo; confiança fica no grafo. | `Reputation`, `SocialSystem`, `KnowledgeSystem` |
| Morte permanente | Fecha necessidades/compromissos do morto, registra causa e preserva a entidade e suas posses; não há ressurreição. | `Engine.finish_death` |
| Sucessão básica e preservação territorial | Governante morto é substituído por familiar vivo elegível; sem sucessor, registra crise e conserva o território. | `Politics.on_death` |
| Eventos e persistência modular | Motor, eventos, interface e repositório estão separados; saves incluem estado e RNG. | `events.py`, `persistence.py`, `ui.py` |
| Testes e diagnóstico da simulação | Há regressões, validação de referências/estado, auditorias sem jogador e rastreamento de decisões. | `tests/`, `validation.py`, `experiments/` |

Os registros históricos e as memórias não possuem a mesma retenção. Conhecimento cotidiano tem limite de 64 fatos, memória curta de 32 registros e os compromissos podem preservar fatos necessários. A crônica global é muito maior; seu custo continua sendo uma limitação.

## 4. Funcionalidades parcialmente implementadas

### 4.1 Mundo, população e personagens

| Funcionalidade original | Parte implementada | Parte que ainda falta | Consequência atual |
|---|---|---|---|
| Geração procedural de conteúdo praticamente total | Varia nomes, posições, biomas, personalidade, relações, itens e composição do mundo. | Grande variedade de regras culturais, estruturas, profissões, organizações e acontecimentos. Muitos locais seguem um mesmo modelo. | Seeds diferentes mudam o elenco e os encontros, mas várias cidades oferecem oportunidades semelhantes. |
| História inicial ligada ao personagem primordial | Personagem real, eventos de fundação e simulação inicial configurável, padrão de 24 horas. | O primordial desencadear conquista, destruição de reino, ruínas, refugiados e remanescentes por mecanismos históricos. | A seed ainda não cria o tipo de grande passado exemplificado com Dovha no original. |
| Conteúdo dos distritos e interiores | Áreas, estruturas e interiores navegáveis existem. | Cada loja, templo, quartel ou ruína possuir funções e conteúdo próprios amplos. Estradas e exploração não formam uma rede econômica completa. | Há diversidade espacial maior que a diversidade de atividades oferecidas. |
| Biomas influenciam necessidades | Deserto aumenta sede. | Influência ampla em fome, sono, vestuário, cultura e cadeias de produção. | Bioma tem efeito fisiológico restrito; terreno não é um sistema tático complexo, coerente com a simplificação original. |
| NPCs comuns, importantes e lendários | Categorias existem; importância afeta parte da geração de itens e frequência de decisão. | Promoção/rebaixamento por feitos e capacidades excepcionais realmente construídas pela história. | O rótulo “lendário” inicial não prova que a campanha criou uma lenda. |
| Níveis alto, médio e baixo de simulação | Agenda adapta decisões por proximidade, categoria, perigo, HP e atividade; fisiologia avança continuamente. | Simulação baixa realmente agregada, como resumir produção diária sem executar as mesmas etapas individuais. | É principalmente uma redução de frequência, não toda a abstração proposta no original. |
| População abstrata | Contabilidade, dinheiro e consumo agregados; conversão limitada em persistente. | Mortalidade abstrata, crescimento, recrutamento, criminalidade e produção diversificada de todos os setores. | A parcela abstrata ainda não sustenta sozinha toda a sociedade simulada. |
| Materialização de habitantes quando necessário | Pode materializar aprendiz de cozinha, com déficit persistente, limites e transferência de recursos existentes. | Materializar outras ocupações por demanda funcional, contratação, interação do jogador e renovação social geral. | **Reposição profissional já existe, mas apenas em alcance limitado; não repõe automaticamente guardas, ferreiros, governantes e todas as demais funções.** |
| Família dinâmica | Parentes conhecidos podem gerar cuidado, procura, luto, proteção e vingança. | Novos casamentos, filhos durante a campanha, novos lares e dinâmica patrimonial completa. | Famílias reagem, mas não se renovam como linhagens ao longo de gerações. |
| Lealdade ativa | Valores no grafo e vínculos participam de interpretações e escolhas sociais. | Deserção organizada, traição institucional, disputa de fidelidades e mudanças políticas decorrentes. | Existe conflito pessoal; não existe toda a consequência coletiva prometida. |

### 4.2 Necessidades, personalidade, informação e histórias

| Funcionalidade original | Parte implementada | Parte que ainda falta | Consequência atual |
|---|---|---|---|
| Personalidade influencia todas as respostas | Onze traços, emoções, agravos e contexto modificam prioridade e utilidade. | Comportamentos como manipulação, dissimulação, fé executável e projetos políticos, que dependem de ações ainda ausentes. | Personalidades diferem dentro do conjunto de oportunidades existentes; não podem escolher sistemas inexistentes. |
| Necessidades pessoais além de sobreviver | Família, luto, vingança, proteção, status, ascensão, recuperação e migração têm ações. | Fé, casamento desejado, conquista de poder político, propriedade/residência ameaçada como sistema amplo e demais desejos específicos. | A lacuna do MVP inicial diminuiu bastante, mas sobrevivência ainda disputa grande parte do tempo. |
| Aspirações e objetivos de longo prazo | Riqueza, competência, reconhecimento e família podem formar aspirações; compromissos atravessam interrupções. | Projetos muito longos e variados: tornar-se rei, fundar organização, conquistar território, construir patrimônio e outras trajetórias. | Muitos compromissos ainda expiram ou são abandonados; persistência não equivale a uma saga concluída. |
| Aprendizado por resultado | Falhas, bloqueios, tentativas sociais e estratégias influenciam reavaliações. | Aprendizagem generalizada e duradoura de todas as consequências, como rever uma carreira ou um padrão de crime por experiência passada. | Há adaptação limitada, não um modelo completo de aprendizado individual. |
| Memórias de feitos influenciam escolhas | Fatos conhecidos, reputação e causa preservada alimentam decisões. | Retenção diferenciada ampla para lendas, gerações, história de grupos e reconstrução de grandes trajetórias. | Fatos importantes de um compromisso podem persistir; a memória individual geral continua curta. |
| Informação imperfeita | Fontes, confiança, rumores, recusa e pistas antigas são executáveis. | Mentira deliberada, exagero de fatos, autoria falsamente atribuída, propaganda e correção social de falsas acusações. | Informação incerta ou desatualizada existe; isso não comprova falsidade intencional. |
| Investigação de desaparecimento/culpado | Busca áreas, consulta pessoas, segue pista conhecida, encontra pessoa/restos, suspende e retoma busca. | Investigação forense ampla, objetos/evidências materiais complexos, contratos de investigadores e todas as situações de autoria desconhecida. | Funciona em casos pessoais e institucionais limitados; não é um sistema criminal completo. |
| Perseguição informada | Guardas e NPCs podem procurar alvos por informação conhecida, viajar fisicamente e receber novas pistas. | Caçadores de recompensa, organização de buscas por facções e continuidade comprovada de perseguições fatais longas. | Há procura ativa; captura e desfecho fatal não são garantidos. |
| Quests emergentes | Comida, cuidado familiar, localização/informação, companhia e proteção possuem contratos causados pelo estado do NPC. | Pedidos de facções/reinos, recuperação de artefatos, guerra, religião, patrimônio e outros contratos. | A causa é emergente, mas os tipos de contrato e critérios de conclusão são definidos no código. |
| Diálogo contextual | Usa profissão, fome, objetivo, relação, reputação e alguns fatos conhecidos; conversa pode transmitir informação e oferecer pedido. | Conversa extensa, contextualização de todos os sistemas novos e camada narrativa mais expressiva. | Existe interação útil, mas o texto ainda resume pouco da trajetória do NPC. |
| Reputação contextual | Observadores interpretam ajuda, crimes e violência por personalidade, vínculos e confiança da fonte. | Reputação institucional ampla, feitos únicos, reconhecimento pela aparência/equipamento, alcance regional explícito e mais efeitos econômicos/políticos. | Nem todos enxergam alguém da mesma forma, mas a identidade pública ainda é pouco diversa. |
| Popularidade e reconhecimento | Popularidade individual cresce por fatos conhecidos; familiaridade e confiança restringem algumas interações. | Modelo completo de reconhecer a pessoa por descrição, título, região ou artefato, sem confundir fama com identificação. | Ainda não realiza toda a diferença entre “ouvi falar dele” e “reconheci quem está aqui”. |
| Títulos e apelidos por feitos | “Desconhecido” inicial e título de protetor local após pedidos alimentares concluídos. | Títulos variados de NPCs e jogador, específicos da história e diferentes por região. | Não há geração ampla de identidade lendária por feitos. |
| História procedural | Eventos causais, mortes, sucessões, respostas, compromissos e pistas produzem crônica; relatórios externos selecionam trajetórias. | Grandes acontecimentos dos sistemas ausentes e seleção narrativa eficiente dentro do jogo. | O log contém muito material, mas evento, compromisso e história completa são medidas diferentes. |

### 4.3 Economia, profissões, itens, combate e justiça

| Funcionalidade original | Parte implementada | Parte que ainda falta | Consequência atual |
|---|---|---|---|
| Economia regional dinâmica | Produção/consumo/estoque, especialização, preços locais, dinheiro e dificuldades de compra influenciam comportamento. | Transporte autônomo regional, demanda multissetorial ativa, guerra, bloqueios e negociação social. | Recursos existem localmente, mas excedentes não abastecem automaticamente outras localidades. |
| Demanda econômica detalhada | Demanda alimentar e déficit culinário são calculados; há campo de demanda no preço. | Construção ativa da demanda de armas, ferro, madeira e outros bens por recrutamento, obras e projetos. | O campo genérico de demanda não representa uma cadeia completa de procura gerada pelo mundo. |
| Trabalho adaptativo e mudança profissional | Produção parcial, crédito salarial, trabalho temporário, distribuição de refeições e formação em cozinha. | Carreiras variadas, mercado geral de vagas, aprendizagem de outras profissões e recrutamento militar. | A adaptação se concentra na alimentação; uma mudança social não reorganiza todos os setores. |
| Profissões propostas no original | Produção para oito profissões iniciais; serviços para alguns cargos e suporte de rotina a soldado. | Pesca, curandeiro profissional, sacerdote/clero, artesanato variado, cadeia militar e comerciante itinerante. | Caça é produção simplificada de comida; não envolve uma população animal caçada no exterior. |
| Guardas protegem/patrulham/respondem | Serviço remunerado, conhecimento de crime, denúncia, busca, perseguição, intervenção e captura. | Rotas de patrulha territorial completas, hierarquia policial e cobertura sistêmica de bairros/fronteiras. | “Patrulha realizada” como serviço não significa que uma ronda percorreu o território. |
| Itens procedurais com origem | Qualidade, raridade, dono, criador, origem e data; armas possuem dano. | Raridades superiores e divinas executáveis, peculiaridades únicas, mudança de valor por feitos e reconhecimento histórico. | O item pode ter procedência, mas ainda não se torna famoso por ter matado um rei. |
| Equipamento funcional | Arma possuída influencia potência/dano e sinais observáveis influenciam avaliação do adversário. | Slots, equipar/desequipar, armaduras, escudos, acessórios, durabilidade, peso e resistências. | **Armas já têm efeito físico; o sistema completo de equipamentos continua ausente.** |
| Inventário completo | Adicionar/remover, consumir, transferir, comprar, vender e entregar. | Abandonar no chão, recuperar do chão/corpo, equipamentos por slots e herança. | Posse circula por comércio/ajuda/roubo, mas a morte não redistribui automaticamente patrimônio. |
| Combate | Ataque, defesa, fuga, rendição, recuo, proteção, intenções e incapacidade. | **Combate por partes do corpo**, perda funcional de membros, cabeça/tórax letais e efeitos por região. | O sistema atual usa HP único; é uma mudança de modelo além de uma implementação parcial. |
| Ferimentos e condições | Lesão geral afeta ação, trabalho e movimento; descanso/tratamento limitado recuperam. | Ferimentos localizados e demais condições específicas propostas. | Lesão não se resolve automaticamente ao sair do combate, diferindo do original. |
| Vingança e decisão de matar | Dano/perda conhecida, episódios, agravo, compromisso e barreiras podem tornar a intenção letal elegível; há escolha após incapacidade sob intenção letal. | Continuidade natural suficiente para concretizar homicídio deliberado e sagas fatais nas campanhas. | Capacidade técnica demonstrada em testes; nenhum homicídio deliberado na última longa. |
| Crime e resposta institucional | Roubo, agressão e morte conhecida podem gerar casos; guardas compartilham informação local, perseguem e capturam sob condições. | Processo judicial amplo, instituições penais, confisco, penas variadas e recompensas financeiras. | Captura/detenção existem; isso não equivale a uma justiça completa. |

### 4.4 Reinos, organizações e infraestrutura

| Funcionalidade original | Parte implementada | Parte que ainda falta | Consequência atual |
|---|---|---|---|
| Reinos vivos e interdependentes | Território, família real, cidades/vilas, tesouro, estados separados, sucessão e resposta alimentar. | Governante escolher políticas por personalidade, defesa, expansão, alianças, obras e crises políticas dinâmicas. | Reinos reagem pouco fora da alimentação e da troca de governante. |
| Necessidades coletivas | Cidades diagnosticam a cadeia alimentar, abrem # FASE 5 — PODER LOCAL, ORGANIZAÇÕES, FÉ, DIVINIZAÇÃO E LENDAS EMERGENTES

## 0. CONTEXTO E PRINCÍPIO CENTRAL

Basear esta fase na versão atual `mvp-7-fase4.6`.

Esta fase NÃO é uma reescrita do motor.

Preserve os sistemas existentes sempre que possível:

- Need;
- prioridade dinâmica;
- Solution;
- Goal;
- Commitment;
- Aspiration;
- personalidade;
- emoção;
- grievance;
- Knowledge;
- rumores;
- investigação;
- relações;
- economia;
- profissões;
- migração;
- combate;
- justiça;
- reputação;
- Event Bus;
- persistência;
- geração procedural;
- sucessão básica;
- instituições já existentes.

O princípio central continua sendo:

**histórias devem emergir de pessoas, necessidades, conhecimento, crenças, relações e consequências reais.**

Não construir um `StoryManager`.

Não criar acontecimentos apenas porque seriam narrativamente interessantes.

Não criar guerras, revoluções ou grandes tragédias para “dar história” ao mundo.

A prioridade desta fase é:

> fazer indivíduos começarem a agir coletivamente, politicamente, religiosamente e miticamente através dos mesmos princípios causais que já regem suas vidas pessoais.

Uma história pequena é válida.

Uma vida comum é válida.

Um objetivo abandonado é válido.

Um grupo que desaparece depois de conseguir o que queria é válido.

Um personagem extraordinário que nunca realiza seu potencial é válido.

Grandes arcos devem surgir raramente.

---

# 1. OBJETIVOS DESTA FASE

Implementar cinco pilares que devem conversar entre si:

1. grupos sociais emergentes;
2. política local;
3. organizações e facções ativas;
4. fé, deuses reais e divinização;
5. fama, indivíduos míticos e itens históricos.

Esses sistemas NÃO devem existir isoladamente.

O objetivo é permitir circuitos como:

```text
Need individual
→ problema compartilhado
→ grupo
→ proposta
→ pressão sobre autoridade
→ decisão política
→ consequência material
→ novas Needs
```

e:

```text
evento sobrenatural real
→ testemunhas
→ interpretação
→ rumor
→ fé
→ grupo religioso
→ pressão social/política
```

e raramente:

```text
indivíduo excepcional
→ feitos
→ fama
→ epíteto
→ seguidores
→ culto
→ confronto com entidade divina
→ possível apoteose
```

---

# 2. FORA DO ESCOPO

NÃO implementar nesta fase:

- guerras entre reinos;
- diplomacia completa entre reinos;
- tratados;
- alianças internacionais;
- cerco;
- conquista territorial;
- anexação;
- ocupação militar;
- batalhas de exércitos;
- guerra civil completa;
- revolução completa;
- sistema estratégico de exército entre mapas;
- caravanas militares;
- destruição de cidades por guerra;
- nascimento/envelhecimento geracional;
- IA generativa controlando regras;
- roteiro principal;
- profecia obrigatória;
- “chosen one” automático;
- alinhamento global GOOD/EVIL;
- sistema automático de herói/vilão.

Podem surgir condições que no futuro levem a guerra, golpe ou revolução.

Não implementar ainda a resolução desses fenômenos em escala nacional.

---

# 3. POLÍTICA LOCAL: ESTRUTURA DE PODER

Adicionar política executável principalmente na escala da cidade.

Cada cidade de reino deve possuir uma autoridade política local:

```text
Mayor / Prefeito
```

O prefeito representa a cidade perante a família real e o reino.

Nesta fase, para um cidadão comum, o maior cargo político formal alcançável é prefeito.

Não implementar ainda ascensão comum direta ao trono.

O prefeito deve ser uma pessoa real existente no mundo.

Deve possuir:

- CharacterID;
- cidade representada;
- início do mandato/ocupação;
- origem da nomeação/ascensão;
- apoio conhecido;
- grupos relevantes;
- decisões tomadas;
- propostas recebidas;
- reputação política;
- relações com autoridades locais;
- relação com família real.

Não transformar prefeito em controlador absoluto da cidade.

Ele é uma autoridade que precisa lidar com pressões concorrentes.

---

# 4. RELAÇÃO ENTRE PREFEITO E FAMÍLIA REAL

A família real continua sendo autoridade superior do reino.

O prefeito:

- representa necessidades da cidade;
- recebe ou transmite decisões;
- pode buscar recursos do reino;
- pode entrar em desacordo com interesses reais;
- pode ganhar ou perder apoio;
- pode ignorar ou atender pressões locais;
- pode ter interesses próprios.

Não implementar ainda uma máquina completa de política nacional.

Nesta fase é suficiente que exista uma relação executável entre:

```text
cidade
↕
prefeito
↕
família real / autoridade central
```

A personalidade do prefeito deve influenciar suas respostas.

Não usar decisões aleatórias independentes de contexto.

---

# 5. GRUPOS POPULARES EMERGENTES

Adicionar `Group` como entidade social distinta de facção.

Um grupo popular deve surgir porque pessoas compartilham algum problema, desejo, crença, interesse ou ameaça.

Exemplos possíveis:

- falta de comida;
- salários ruins;
- insegurança;
- medo de criminosos;
- desejo por mais armamento;
- oposição a alguma decisão;
- demanda religiosa;
- defesa de culto;
- perseguição a culto rival;
- proteção de profissão;
- apoio a determinada figura;
- demanda por justiça;
- reclamação contra tributos;
- defesa de determinada política.

NÃO criar grupos aleatoriamente apenas para povoar o mundo.

O fluxo deve ser aproximadamente:

```text
Needs / crenças / interesses individuais
→ reconhecimento de problema compartilhado
→ contato social
→ percepção de afinidade
→ formação de grupo
```

---

# 6. GRUPO NÃO É FACÇÃO

Separar claramente:

## Grupo

Pode ser:

- temporário;
- informal;
- local;
- sem recursos próprios relevantes;
- criado por um problema específico;
- dissolvido após sucesso, fracasso ou perda de relevância.

## Facção

É uma organização mais persistente.

Possui:

- identidade;
- liderança;
- membros;
- sede ou área de operação;
- recursos;
- objetivos;
- hierarquia;
- continuidade;
- capacidade organizacional.

Um grupo pode eventualmente amadurecer e virar facção.

Isso deve emergir de continuidade, liderança, recursos, identidade e investimento.

Não fazer:

```text
qualquer Group
→ Faction
```

automaticamente.

---

# 7. FORMAÇÃO DE GRUPOS

A formação deve considerar:

- necessidade compartilhada;
- severidade;
- repetição;
- relações sociais;
- proximidade;
- profissão;
- crença;
- reputação;
- confiança;
- personalidade;
- liderança disponível;
- capacidade percebida;
- informação disponível.

Uma pessoa pode concordar com o problema mas não entrar no grupo.

Outra pode entrar e depois abandonar.

Outra pode radicalizar o grupo.

Outra pode tentar moderá-lo.

---

# 8. LIDERANÇA DE GRUPO

Grupos podem possuir liderança formal ou informal.

A liderança deve emergir de fatores como:

- iniciativa;
- reputação;
- reconhecimento;
- ambição;
- persistência;
- coragem;
- competência percebida;
- relações;
- capacidade de mobilização;
- confiança do grupo.

Não escolher líder apenas pelo maior atributo numérico.

Não teleportar autoridade.

A pessoa precisa estar socialmente conectada ao grupo.

---

# 9. OBJETIVOS COLETIVOS

Grupos podem possuir um objetivo coletivo derivado das necessidades de seus membros.

Exemplo:

```text
escassez alimentar
→ membros percebem privação comum
→ grupo se forma
→ objetivo: aumentar acesso a comida
```

Não transformar isso diretamente em uma ação.

Aplicar princípio semelhante ao individual:

```text
Collective Pressure
→ alternatives
→ collective objective
→ chosen strategy
→ action
→ consequence
```

Evitar criar um segundo motor completamente separado se os conceitos atuais puderem ser generalizados/reutilizados.

---

# 10. PROPOSTAS

Nesta fase, propostas políticas formais devem surgir principalmente através de grupos.

Não permitir que qualquer NPC gere propostas políticas arbitrárias sem representação coletiva.

Uma proposta deve conter pelo menos:

- grupo de origem;
- problema causal;
- objetivo;
- alvo político;
- solução proposta;
- urgência;
- apoio conhecido;
- oposição conhecida;
- data;
- status;
- resultado.

Exemplos:

- mais distribuição de comida;
- redução/aumento de determinada cobrança;
- mais investimento em segurança;
- mais armas para militares;
- proteção de determinada profissão;
- reconhecimento de culto;
- restrição de culto;
- aumento de recursos para alguma instituição;
- apoio a determinado grupo.

---

# 11. PROPOSTAS DEVEM ALTERAR O MUNDO REAL

Proposta não pode ser apenas texto.

Se aprovada, deve afetar algum sistema existente.

Exemplo:

```text
mais distribuição alimentar
→ recursos realmente saem de algum estoque/tesouro
```

```text
mais armamento
→ demanda real por armas/materiais
```

```text
mais guardas
→ necessidade real de pessoal, pagamento ou recursos
```

```text
restrição religiosa
→ comportamento institucional/social real
```

Não criar benefícios sem custo.

---

# 12. DECISÃO DO PREFEITO

O prefeito deve avaliar propostas segundo:

- personalidade;
- interesses;
- reputação;
- relações;
- recursos;
- apoio social;
- oposição;
- posição da família real;
- risco;
- necessidade da cidade;
- crenças;
- autoridade disponível.

Não usar:

```text
proposal_support > X
→ approve
```

como única lógica.

A decisão precisa competir com alternativas.

---

# 13. REAÇÃO DOS GRUPOS

Uma proposta pode ser:

- aceita;
- aceita parcialmente;
- recusada;
- adiada;
- ignorada;
- substituída;
- negociada.

O grupo deve reagir ao resultado.

Possíveis respostas:

- aceitar;
- dissolver;
- insistir;
- reorganizar;
- mudar proposta;
- aumentar pressão;
- protestar;
- procurar apoio;
- denunciar;
- ameaçar;
- abandonar;
- radicalizar.

Radicalização não deve ser automática.

---

# 14. PRIVAÇÃO, RAIVA E RADICALIZAÇÃO

Privação extrema pode gerar grupos muito mais perigosos.

Mas NÃO usar:

```text
hunger high + anger high
→ overthrow government
```

Exigir combinação causal.

Possíveis fatores:

- privação coletiva;
- duração;
- raiva;
- ressentimento;
- fracasso de alternativas;
- responsabilidade atribuída;
- baixa confiança institucional;
- percepção de injustiça;
- liderança;
- apoio;
- capacidade percebida;
- repressão;
- crenças.

A responsabilidade percebida é fundamental.

A mesma fome pode gerar interpretações distintas:

```text
"foi a seca"
```

```text
"o prefeito roubou"
```

```text
"os comerciantes esconderam comida"
```

```text
"os deuses estão nos punindo"
```

Essas interpretações devem produzir comportamentos diferentes.

---

# 15. GRUPOS DE DOMÍNIO

Em circunstâncias extremas, alguns grupos podem desenvolver objetivo de tomar controle político local.

Chamar internamente como conceito equivalente a:

```text
domination / seize_local_power
```

Não significa revolução nacional.

Pode ser:

- remover prefeito;
- controlar determinada instituição;
- impor autoridade local;
- ocupar função administrativa.

Não implementar guerra civil completa.

Esses grupos devem ser raros.

---

# 16. CONFLITO ENTRE GRUPOS

Grupos podem possuir objetivos incompatíveis.

Isso pode gerar:

- rivalidade;
- desconfiança;
- propaganda;
- boicote;
- intimidação;
- disputa por apoio;
- denúncias;
- ameaças;
- brigas;
- conspiração;
- assassinato;
- negociação;
- acordo.

NÃO transformar antagonismo em violência automaticamente.

Usar os mesmos princípios sociais já existentes.

---

# 17. GRIEVANCE ENTRE GRUPOS

Adicionar uma representação compacta de agravos coletivos quando necessária.

Não copiar toda emoção humana para organizações.

Registrar apenas o suficiente para explicar:

- por que determinado grupo considera outro uma ameaça;
- qual fato originou isso;
- severidade;
- continuidade;
- resolução ou abandono.

Evitar crescimento ilimitado de pares.

---

# 18. FACÇÕES ATIVAS

Transformar facção de estrutura majoritariamente passiva em organização executável.

Uma facção deve possuir:

- líder;
- membros;
- propósito;
- recursos;
- sede;
- hierarquia;
- regras;
- interesses;
- objetivos;
- relações;
- memória organizacional compacta.

O comportamento da facção deve ser fortemente influenciado pelo propósito de sua existência.

---

# 19. PROPÓSITO DA FACÇÃO

Exemplos:

- caçadores de recompensa;
- mercadores;
- ordem religiosa;
- proteção local;
- grupo de justiça;
- associação profissional;
- exploradores;
- criminosos;
- estudiosos;
- culto;
- organização militar privada.

Não restringir a esses exemplos.

O propósito deve alterar:

- recrutamento;
- hierarquia;
- ações plausíveis;
- necessidades coletivas;
- uso de recursos;
- reputação.

---

# 20. LIDERANÇA DE FACÇÃO

O líder deve ser personagem real.

Sua personalidade deve influenciar:

- prioridades;
- tolerância a risco;
- recrutamento;
- punição;
- expansão;
- negociação;
- relação com autoridade;
- interpretação do propósito.

A facção NÃO deve ser simplesmente a personalidade do líder.

Ela também possui:

- membros;
- história;
- interesses;
- recursos;
- normas.

Mas o líder deve exercer influência forte.

---

# 21. PATENTES DE FACÇÃO

Facções devem possuir hierarquias coerentes com seu propósito.

Os nomes podem ser definidos durante criação/fundação segundo contexto da organização.

Exemplo:

```text
Guilda de Caçadores
Novato
Caçador
Veterano
Mestre
```

Outra facção pode usar títulos totalmente diferentes.

Evitar depender de IA generativa.

Utilizar repertórios/configurações e composição procedural controlada.

---

# 22. PROMOÇÃO EM FACÇÕES

Promoção deve depender de:

- feitos relevantes;
- confiança;
- tempo;
- competência;
- lealdade;
- reputação interna;
- vagas;
- decisão de liderança;
- necessidade organizacional.

Não usar apenas XP.

---

# 23. ESTRUTURA MILITAR LOCAL

Adicionar hierarquia militar das cidades do reino:

```text
General
Captain
Lieutenant
Sergeant
Soldier
```

Regras iniciais:

- exatamente um General ativo por cidade quando estrutura militar existir;
- múltiplos capitães;
- múltiplos tenentes;
- múltiplos sargentos;
- soldados.

Cada patente deve possuir autoridade real compatível.

---

# 24. GENERAL DA CIDADE

O General é a maior autoridade militar local.

Ele não substitui o prefeito.

Prefeito:

```text
autoridade política local
```

General:

```text
autoridade militar local
```

Pode existir tensão entre os dois.

---

# 25. MILITARES COMO GRUPO SOCIAL

Soldados não são apenas unidades de combate.

Eles são NPCs.

Podem:

- possuir necessidades;
- criar relações;
- formar grupos;
- apoiar propostas;
- rejeitar propostas;
- pressionar prefeito;
- apoiar general;
- entrar em conflito interno;
- possuir religião;
- espalhar rumores;
- venerar figuras.

Isso prepara futuros golpes e guerras sem implementá-los agora.

---

# 26. PRESSÃO MILITAR

Militares podem formar grupos em torno de interesses como:

- pagamento;
- equipamento;
- comida;
- segurança;
- prestígio;
- liderança;
- religião;
- tratamento recebido.

Esses grupos podem produzir propostas.

Não permitir golpe automático nesta fase.

---

# 27. FÉ OBJETIVAMENTE REAL

A cosmologia deste mundo deve assumir:

**deuses existem objetivamente.**

Isso não é ambíguo para o motor.

Mas a percepção das pessoas continua imperfeita.

Separar:

```text
Objective Divinity
Faith
Knowledge
Worship
Interpretation
```

---

# 28. DEUS REAL ≠ SER ADORADO

Um Deus pode:

- existir e ser adorado;
- existir e ser desconhecido;
- existir e ser interpretado incorretamente.

Um mortal pode:

- ser adorado;
- ser considerado divino;
- possuir culto;
- NÃO ser um Deus real.

Não usar adoração como prova ontológica.

---

# 29. ENTIDADE DIVINA

Criar estrutura de entidade divina com pelo menos:

- ID;
- nome;
- domínio atual;
- personalidade/valores próprios;
- poder;
- seguidores conhecidos;
- áreas de influência;
- relações;
- memória divina compacta;
- intervenções;
- estado vivo/morto;
- origem;
- possíveis vínculos com objetos/locais.

Não transformar Deus em apenas NPC com HP enorme.

Pode compartilhar conceitos com Character, mas deve possuir semântica divina própria.

---

# 30. DOMÍNIO DIVINO

Cada Deus possui domínio ou conjunto limitado de conceitos associados.

Exemplos:

- amor;
- justiça;
- guerra;
- morte;
- conhecimento;
- caça;
- fome;
- tempestade;
- proteção;
- vingança.

O domínio deve afetar:

- comportamento;
- tipos de intervenção;
- valores;
- relação com seguidores;
- culto.

---

# 31. DEVOÇÃO

A devoção individual deve continuar variável.

Não assumir que todo religioso é fanático.

A devoção deve influenciar:

- prioridade religiosa;
- interpretação;
- ritual;
- disposição a obedecer doutrina;
- participação em grupo religioso;
- reação a blasfêmia;
- disposição a defender culto;
- impacto de sinais divinos.

---

# 32. FÉ COMO COMPORTAMENTO

Transformar fé de simples campo em sistema executável.

Um NPC pode:

- rezar;
- buscar templo/local sagrado;
- oferecer recurso;
- pedir intervenção;
- espalhar crença;
- defender fé;
- abandonar fé;
- mudar fé;
- formar culto;
- denunciar heresia percebida;
- reinterpretar evento.

Não implementar tudo obrigatoriamente de uma vez se algumas ações exigirem sistemas inexistentes.

Priorizar um núcleo funcional e auditável.

---

# 33. EXPANSÃO DE FÉ

Fé pode se espalhar para fora de sua região original.

Usar:

- contato;
- relações;
- migração;
- testemunho;
- reputação;
- rumor;
- intervenção percebida;
- grupos;
- líderes religiosos.

Não converter automaticamente por proximidade.

---

# 34. EVENTO SOBRENATURAL: VERDADE E INTERPRETAÇÃO

O motor deve preservar a verdade objetiva.

Exemplo:

```text
God 17 caused DivineIntervention 991
```

Personagens podem interpretar como:

```text
milagre
maldição
coincidência
ação de outro Deus
ação de um mortal
evento incompreendido
```

Não sobrescrever verdade com interpretação.

---

# 35. RUMOR ESPIRITUAL

Knowledge deve poder transmitir rumores religiosos e sobrenaturais.

Rumor não precisa ser informação operacional imediata.

Pode ser:

- relato de milagre;
- suposta aparição;
- feito extraordinário;
- bênção;
- maldição;
- profecia percebida;
- fama de indivíduo;
- reputação de objeto.

Preservar:

- fonte;
- confiança;
- idade;
- cadeia de transmissão quando relevante.

---

# 36. DEUSES PODEM INTERVIR

Adicionar intervenções divinas executáveis.

Não torná-las frequentes.

Possíveis categorias iniciais:

- bênção;
- maldição;
- sinal;
- proteção;
- aumento temporário;
- punição;
- manifestação;
- influência sobre item.

Cada intervenção deve possuir:

- causa;
- Deus;
- alvo;
- custo/regra;
- consequência;
- testemunhas;
- conhecimento produzido.

---

# 37. NÃO USAR INTERVENÇÃO COMO ROTEIRO

Deus não intervém porque “seria épico”.

Deve existir motivação.

Exemplos:

- seguidor relevante;
- afronta;
- pedido;
- ameaça;
- domínio;
- relacionamento;
- rivalidade;
- interesse.

---

# 38. RELAÇÃO ENTRE DEUSES

Pode existir relação básica entre deuses nesta fase.

Não implementar guerra divina completa.

Permitir apenas estados suficientes para:

- afinidade;
- hostilidade;
- rivalidade;
- interesse.

---

# 39. MORTE DE UM DEUS

Deuses podem morrer.

Isso deve ser extremamente raro.

Não simplificar para:

```text
HP <= 0
→ ordinary death
```

Pode utilizar combate, mas a morte divina deve produzir consequências especiais.

Registrar:

- autor;
- causa;
- testemunhas;
- local;
- domínio;
- seguidores afetados;
- essência/divindade liberada;
- repercussão.

---

# 40. APOTEOSE REAL

Um mortal pode se tornar Deus REAL caso consiga:

1. matar um Deus;
2. sobreviver;
3. possuir acesso legítimo à essência/posição divina;
4. conseguir assumir essa divindade segundo as regras implementadas.

Não fazer automaticamente:

```text
kill God
→ isGod = true
```

Deve existir uma etapa de apropriação/assunção.

---

# 41. DOMÍNIO NÃO É HERDADO AUTOMATICAMENTE

Se um mortal mata o Deus do Amor, ele não precisa virar Deus do Amor.

O novo domínio pode ser influenciado por:

- personalidade;
- MythicTrait;
- trajetória;
- crenças;
- feitos;
- aspirações;
- reputação;
- circunstância da ascensão.

Exemplo:

```text
Deus do Amor morre
↓
mortal da Justiça assume essência
↓
novo Deus do Julgamento
```

A sucessão divina deve permitir transformação religiosa real.

---

# 42. USURPAÇÃO DIVINA

Seguidores do Deus morto podem:

- aceitar;
- rejeitar;
- considerar novo Deus usurpador;
- manter culto antigo;
- migrar para outra fé;
- formar grupos;
- perseguir seguidores rivais.

Não implementar guerra religiosa nacional automaticamente.

---

# 43. DIVINIZAÇÃO SOCIAL

Separar apoteose real de divinização social.

Um mortal pode ser considerado Deus sem possuir Divinity.

Exemplo:

```text
General vence dezenas de batalhas/duelos locais
↓
soldados espalham histórias
↓
ganha epíteto
↓
alguns passam a considerá-lo divino
↓
culto pode surgir
```

Motor:

```text
actual_divinity = false
```

Sociedade:

```text
believed_divine = true para certos grupos/personagens
```

---

# 44. FAMA / RENOWN

Expandir conhecimento social para incluir:

```text
Renown
```

Renown responde:

> pelo que essa pessoa é conhecida?

Não substituir fatos individuais.

Agregar reputação derivada de feitos conhecidos.

Possíveis áreas:

- swordsmanship;
- cooking;
- hunting;
- leadership;
- justice;
- cruelty;
- generosity;
- divine association;
- survival;
- craftsmanship;
- military success.

---

# 45. FATO, FAMA E EPÍTETO

Separar:

```text
Fact
Renown
Epithet
```

Fact:

```text
Daemon derrotou NPC X em duelo.
```

Renown:

```text
Daemon é conhecido por habilidade com espada.
```

Epithet:

```text
Daemon, o Espadachim.
```

---

# 46. FAMA DEPENDE DE CONHECIMENTO

Feito desconhecido não gera fama automática.

Se alguém mata 100 inimigos sem testemunhas, sobreviventes, evidência ou propagação:

```text
Renown não cresce automaticamente.
```

O EventLog sabe.

A sociedade não necessariamente sabe.

---

# 47. ALCANCE DA FAMA

Renown deve possuir alcance.

Possíveis escalas:

- círculo pessoal;
- local;
- cidade;
- regional;
- reino;
- continental.

Não usar thresholds rígidos isolados.

Considerar:

- quantidade de pessoas que conhecem;
- alcance geográfico;
- repetição;
- importância dos feitos;
- credibilidade;
- testemunhas;
- rumores.

---

# 48. EPÍTETOS

Personagens podem receber apelidos/títulos emergentes baseados em sua fama.

Exemplos:

```text
Daemon, o Espadachim
```

```text
Arthus, o Caçador Feroz
```

```text
Iria, a Cozinheira dos Deuses
```

```text
Daemon, o Deus Espadachim
```

O epíteto deve refletir:

- pelo que é conhecido;
- intensidade;
- alcance;
- cultura;
- crença social.

---

# 49. "DEUS" EM EPÍTETO NÃO SIGNIFICA DIVINDADE

Fundamental:

```text
epithet contains "God"
≠
actual_divinity
```

Um homem chamado “Deus Espadachim” pode continuar mortal.

Isso pode inclusive contribuir para culto futuro.

---

# 50. EPÍTETO PODE VARIAR POR REGIÃO

Não exigir título global único.

Uma pessoa pode ser conhecida de formas diferentes em lugares diferentes.

Exemplo:

```text
cidade A:
Daemon, o Protetor
```

```text
cidade B:
Daemon, o Açougueiro
```

Mesma pessoa.

Diferentes histórias/conhecimento.

---

# 51. PERSONAGENS MÍTICOS RAROS

Adicionar uma característica excepcional raríssima ao nascimento de alguns personagens.

Nome estrutural sugerido:

```text
MythicTrait
```

Não confundir com personality normal.

---

# 52. EXEMPLOS DE MYTHIC TRAITS

Exemplos iniciais:

- Heroism;
- Justice;
- Coldness.

Pode haver outros futuramente.

Não transformar isso em GOOD / EVIL.

---

# 53. RARIDADE

Pouquíssimos NPCs devem possuir MythicTrait.

Não gerar dezenas de figuras especiais em cada cidade.

Esses indivíduos representam potencial histórico extraordinário.

A maioria da população deve continuar comum.

---

# 54. MYTHIC TRAIT COMO FORÇA DE PERSONALIDADE

O MythicTrait deve exercer influência muito forte sobre:

- Utility;
- Aspirations;
- Commitment;
- percepção moral;
- risco;
- busca de poder;
- escolha de aliados;
- escolha de grupos;
- resposta a eventos.

Exemplo:

```text
Justice
```

não significa:

```text
always morally correct
```

Significa:

> forte impulso para agir segundo aquilo que o personagem acredita ser justo.

---

# 55. JUSTIÇA É SUBJETIVA AO PERSONAGEM

Dois personagens com Justice podem divergir.

Um pode acreditar:

```text
todo acusado merece julgamento.
```

Outro:

```text
criminosos perigosos merecem morte.
```

Usar:

- personalidade;
- fé;
- cultura;
- conhecimento;
- experiências.

---

# 56. HEROISM

Heroism pode aumentar tendência a:

- enfrentar perigo;
- proteger;
- aceitar custo pessoal;
- buscar feitos;
- responder a ameaças.

Não significa comportamento sempre bom.

Um personagem pode buscar heroísmo por fama ou orgulho.

---

# 57. COLDNESS

Coldness pode influenciar:

- tolerância emocional;
- cálculo de risco;
- baixa hesitação;
- decisões duras;
- resistência a certas barreiras emocionais.

Não transformar automaticamente em psicopatia ou maldade.

---

# 58. PODER FÍSICO EXCEPCIONAL

MythicTrait pode fornecer potencial físico acima do humano comum.

Permitir bônus limitados e explícitos em:

- HP máximo;
- dano;
- resistência;
- crescimento;
- capacidade futura.

Mas evitar:

```text
bebê mítico
→ força absurda imediata
```

Preferir:

```text
potencial elevado
→ desenvolvimento através da vida
```

---

# 59. BUSCA POR PODER

Personagens míticos podem desenvolver Aspiration relacionada a:

```text
become_stronger
```

quando coerente com:

- MythicTrait;
- personalidade;
- experiências;
- ameaças;
- crenças;
- objetivos.

Não executar automaticamente.

---

# 60. EXEMPLO: JUSTICE

Um personagem com Justice forte pode:

```text
perceber injustiça
→ formar Commitment
→ treinar/buscar força
→ entrar em grupo
→ criar grupo
→ defender vítimas
→ confrontar instituição
```

Raramente:

```text
considerar Deus injusto
→ buscar força
→ formar aliados
→ tentar confrontá-lo
```

Nada disso deve ser roteirizado.

---

# 61. PERSONAGEM MÍTICO PODE FRACASSAR

Fundamental.

Pode:

- morrer jovem;
- nunca encontrar oportunidade;
- abandonar objetivo;
- ser desconhecido;
- escolher vida comum;
- ser derrotado;
- nunca virar lenda.

MythicTrait é potencial e influência, não destino.

---

# 62. GRANDES ARCOS DEVEM SER RAROS

Não calibrar o sistema para que todo MythicTrait vire uma saga.

Distribuição desejada conceitualmente:

```text
maioria:
vidas ordinárias
```

```text
alguns:
acontecimentos marcantes
```

```text
poucos:
trajetórias históricas
```

```text
raríssimos:
figuras míticas / divinas
```

---

# 63. ITENS HISTÓRICOS

Expandir Item.

Já existe procedência básica.

Adicionar possibilidade de histórico relevante.

Campos/conceitos possíveis:

- previous_owners;
- important_events;
- famous_kills;
- divine_contact;
- religious_association;
- creator;
- creation_location;
- creation_time;
- renown;
- epithet/title;
- believed_properties;
- actual_properties.

---

# 64. ITEM PODE SE TORNAR LENDÁRIO

Não gerar todo item lendário como lendário desde o início.

Uma espada comum pode adquirir importância por:

- dono famoso;
- matar figura importante;
- matar Deus;
- participação em evento conhecido;
- associação religiosa;
- sucessivas transmissões.

---

# 65. PROPRIEDADE REAL ≠ PROPRIEDADE ACREDITADA

Separar:

```text
actual_item_effects
```

de:

```text
beliefs_about_item
```

Uma espada pode ser considerada amaldiçoada sem ser.

Um artefato realmente divino pode ser tratado como comum.

---

# 66. RUMORES SOBRE ITENS

Knowledge/Renown deve permitir rumores como:

```text
"esta espada matou um rei"
```

```text
"esta lâmina foi tocada por Deus X"
```

A verdade objetiva continua separada.

---

# 67. POLÍTICA + RELIGIÃO

Permitir interação.

Exemplo:

```text
culto cresce
→ grupo religioso
→ proposta ao prefeito
```

ou:

```text
prefeito restringe culto
→ grievance religioso
→ grupo reage
```

ou:

```text
General é divinizado pelos soldados
→ grupo militar-religioso
→ pressão política
```

Não roteirizar esses casos.

---

# 68. FACÇÃO + RELIGIÃO

Uma facção pode possuir religião predominante ou tornar-se religiosa.

Não criar automaticamente uma facção para cada fé.

Cultos/grupos podem amadurecer em facção conforme continuidade.

---

# 69. MILITAR + RELIGIÃO

Militares podem:

- seguir Deus;
- formar culto;
- idolatrar general;
- interpretar vitórias como sinais;
- pressionar autoridade religiosa/política.

Isso deve usar comportamento social normal.

---

# 70. DEUS + POLÍTICA

Deus pode influenciar política através de:

- seguidores;
- intervenções;
- líderes;
- grupos religiosos.

Evitar:

```text
God directly sets city policy
```

a menos que exista ação causal real e autoridade suficiente.

---

# 71. FINALIZAÇÃO LETAL / EXECUTION OPPORTUNITY

Incorporar também o refinamento pendente da Fase 4.6.

A Fase 4.6 demonstrou intenção natural de matar, mas não homicídio deliberado concluído.

Não aumentar dano apenas para produzir mortes.

Adicionar conceito equivalente a:

```text
ExecutionOpportunity
```

quando:

```text
target incapacitated
AND attacker present
AND attacker capable
AND lethal intent active
```

---

# 72. DECISÃO TERMINAL

Ao surgir oportunidade de conclusão, reavaliar:

- finish;
- spare;
- capture;
- withdraw;
- help;
- outra resposta plausível.

Não executar morte automaticamente apenas porque intenção anterior era `kill`.

---

# 73. FINISH

Se:

```text
finish
```

for escolhido e realmente executado em alvo incapaz de resistir, tratar como desfecho fatal certo dentro da abstração.

Não retornar à rolagem normal de dano.

Registrar:

```text
CharacterKilled
death_context = deliberate_finish
```

ou equivalente.

---

# 74. MATAR NO CALOR DO MOMENTO

Intenção letal NÃO precisa vir apenas de compromisso longo.

Permitir letalidade situacional.

Exemplo:

```text
assalto
→ defesa
→ ameaça extrema
→ medo / raiva / personalidade / risco
→ resposta letal torna-se plausível
```

A pessoa pode matar sem possuir histórico de ódio.

Isso não torna automaticamente o personagem mau.

---

# 75. LETALIDADE CONSTRUÍDA VS SITUACIONAL

Distinguir conceitualmente:

```text
Persistent Lethal Intent
```

de:

```text
Situational Lethal Intent
```

Persistente:

- grievance;
- histórico;
- compromisso;
- perseguição.

Situacional:

- perigo imediato;
- defesa;
- emoção intensa;
- oportunidade;
- personalidade.

Ambas usam barreiras e contexto.

---

# 76. CONSEQUÊNCIA DE MATAR

Matar deve afetar a vida do autor.

Possíveis consequências:

- culpa;
- medo;
- reputação;
- investigação;
- perseguição;
- fuga;
- reação da família;
- reação religiosa;
- fama;
- epíteto;
- mudança pessoal.

Não criar trauma obrigatório.

A reação depende do personagem.

---

# 77. MEMÓRIA DE FEITOS IMPORTANTES

Eventos excepcionais devem possuir maior capacidade de persistência histórica do que fatos cotidianos.

Exemplos:

- matar prefeito;
- matar general;
- matar Deus;
- salvar cidade;
- fundar facção;
- ascender divinamente;
- causar massacre;
- derrotar figura famosa.

Não manter EventLog infinito adicional por entidade.

Usar resumos/identificadores compactos quando possível.

---

# 78. NÃO EXPLODIR SAVE

A Fase 4.6 já mostrou histórico global volumoso.

Esta fase não precisa resolver toda retenção histórica.

Mas NÃO adicionar estruturas sem limites.

Aplicar limites para:

- grupos antigos;
- agravos;
- pistas;
- rumores;
- memória organizacional;
- eventos de fama;
- histórico de item.

Preservar eventos importantes por referência compacta.

---

# 79. NECESSIDADES COLETIVAS

Não criar dezenas de Needs coletivas específicas.

Reutilizar categorias gerais quando possível.

Exemplo:

```text
resource_pressure
security
recognition
religious_interest
political_pressure
organizational_survival
```

Manter semântica limpa.

---

# 80. COMMITMENT COLETIVO

Se necessário, generalizar conceito de Commitment para organizações/grupos.

Não duplicar motor inteiro.

Um compromisso coletivo deve possuir:

- origem;
- objetivo;
- intensidade;
- progresso;
- falhas;
- investimento;
- status;
- resolução.

Mas deve continuar diferente de Need.

---

# 81. KNOWLEDGE COLETIVO

Organização não deve saber tudo que seus membros sabem.

Criar conhecimento institucional somente quando houver mecanismo de transmissão.

Exemplos:

- reunião;
- relatório;
- testemunho;
- líder informado;
- canal institucional.

Sem telepatia organizacional.

---

# 82. REPRESENTAÇÃO

Um prefeito não deve automaticamente conhecer todas as necessidades da cidade.

Grupos, informantes, instituições e eventos precisam transmitir problemas.

Isso mantém informação imperfeita na política.

---

# 83. FACÇÃO NÃO É MENTE COLETIVA

A facção age através de pessoas, liderança e estrutura.

Evitar:

```text
Faction thinks X
```

sem fonte.

Pode existir estado organizacional agregado, mas precisa derivar de seus agentes.

---

# 84. PERSONALIDADE DO LÍDER

Liderança importa muito.

Mas não apagar divergências internas.

Um líder extremamente agressivo pode tentar conduzir facção para confronto.

Membros podem:

- apoiar;
- resistir;
- abandonar;
- conspirar;
- criar subgrupo.

Não implementar golpe interno completo se extrapolar escopo.

---

# 85. NOMES DE GRUPOS E FACÇÕES

Nomes devem refletir:

- origem;
- profissão;
- lugar;
- causa;
- figura fundadora;
- religião;
- objetivo.

Não exigir LLM.

Gerar proceduralmente por regras controladas.

---

# 86. NOMES DE PATENTES

Facções podem receber repertório de patentes coerente com seu tipo.

O líder/fundador pode influenciar escolha do repertório.

Registrar a hierarquia explicitamente.

---

# 87. GOVERNANÇA SEM ELEIÇÃO COMPLEXA

Não é necessário implementar sistema eleitoral completo nesta fase.

O prefeito pode chegar ao cargo através de mecanismo inicial simplificado, desde que:

- seja pessoa real;
- exista causa;
- exista registro;
- possa ser substituído;
- suporte futura expansão.

Evitar fixar arquitetura que impeça eleições futuras.

---

# 88. SUBSTITUIÇÃO DO PREFEITO

Prefeito pode deixar cargo por:

- morte;
- perda de autoridade;
- decisão superior;
- crise;
- substituição.

Não implementar golpes/revolução completos.

Garantir continuidade institucional mínima.

---

# 89. RELAÇÃO PREFEITO–GENERAL

Manter separação institucional.

Registrar relação.

Ela pode afetar:

- apoio;
- confiança;
- propostas;
- segurança;
- resposta a grupos.

Não implementar conflito militar automaticamente.

---

# 90. RELAÇÃO PREFEITO–FACÇÕES

Prefeito pode:

- reconhecer;
- ignorar;
- negociar;
- rejeitar;
- tentar restringir.

Facção reage segundo seus interesses.

---

# 91. REPUTAÇÃO INSTITUCIONAL

Expandir reputação de forma limitada para permitir opinião sobre:

- prefeito;
- general;
- facção;
- grupo;
- culto.

Não criar matriz completa de todos contra todos sem limites.

---

# 92. AUDITORIA: POLÍTICA

Registrar métricas como:

- grupos formados;
- grupos dissolvidos;
- grupos convertidos em facção;
- propostas criadas;
- propostas aceitas;
- parcialmente aceitas;
- recusadas;
- abandonadas;
- pressão aumentada;
- grupos antagonistas;
- conflitos entre grupos;
- mudanças materiais causadas por proposta.

---

# 93. AUDITORIA: FACÇÕES

Registrar:

- facções ativas;
- novos membros;
- promoções;
- deserções;
- recursos;
- objetivos;
- ações organizacionais;
- liderança;
- mudanças de propósito, se houver.

---

# 94. AUDITORIA: MILITARES

Registrar:

- distribuição por patente;
- substituições;
- grupos militares;
- propostas militares;
- tensões com autoridade civil;
- ações realizadas por cadeia de comando.

---

# 95. AUDITORIA: RELIGIÃO

Registrar:

- seguidores por fé;
- conversões;
- abandono;
- grupos religiosos;
- cultos;
- propagação entre localidades;
- intervenções;
- rumores espirituais;
- divergências de interpretação.

---

# 96. AUDITORIA: DIVINIZAÇÃO

Registrar separadamente:

```text
believed_divine
actual_divine
```

Medir:

- mortais divinizados socialmente;
- cultos de mortais;
- deuses reais desconhecidos;
- deuses reais conhecidos;
- morte divina;
- tentativa de apoteose;
- apoteose bem-sucedida.

Não exigir que alguma apoteose aconteça naturalmente em uma única seed.

---

# 97. AUDITORIA: MYTHIC TRAITS

Registrar:

- quantidade total;
- distribuição;
- sobrevivência;
- aspirations;
- Commitments;
- busca de poder;
- grupos fundados;
- feitos importantes;
- fama;
- morte.

Não considerar ausência de grande feito como bug.

---

# 98. AUDITORIA: FAMA

Registrar:

- criação de Renown;
- alcance;
- mudança de alcance;
- epítetos;
- variação regional;
- fama sem conhecimento real;
- cultos derivados de fama.

---

# 99. AUDITORIA: ITENS

Registrar:

- itens que ganharam eventos históricos;
- itens conhecidos regionalmente;
- itens associados a figuras importantes;
- itens ligados a Deus;
- diferença entre propriedade real e rumor.

---

# 100. HISTÓRIAS REAIS

Gerar novamente:

```text
reports/fase_5/HISTORIAS_REAIS.md
```

Sem inventar pensamentos.

Selecionar exemplos reais, se existirem, de:

1. grupo formado por privação;
2. grupo que conseguiu proposta e se dissolveu;
3. proposta recusada que aumentou tensão;
4. grupos antagonistas;
5. grupo que amadureceu em facção;
6. prefeito reagindo a pressões diferentes;
7. general/militares pressionando autoridade;
8. promoção em facção;
9. fé atravessando região;
10. rumor espiritual;
11. intervenção divina conhecida de formas diferentes;
12. mortal divinizado socialmente sem ser Deus;
13. personagem ganhando epíteto;
14. epítetos diferentes em regiões distintas;
15. MythicTrait produzindo trajetória;
16. MythicTrait sem grande arco;
17. item ganhando importância histórica;
18. intenção letal situacional;
19. execução deliberada;
20. misericórdia após oportunidade de execução;
21. morte alterando vida do autor;
22. caso político/religioso inacabado no fim da campanha.

Se determinada categoria não ocorrer naturalmente:

**dizer explicitamente que não ocorreu.**

Não criar exemplo artificial.

---

# 101. EVITAR FALSA PROFUNDIDADE

Não considerar:

```text
100 ações repetidas
```

uma grande história.

Preferir transformações:

- mudança de objetivo;
- mudança de relação;
- mudança institucional;
- mudança de crença;
- mudança geográfica;
- mudança de reputação;
- mudança de cargo;
- criação/dissolução de grupo;
- consequência material;
- descoberta importante;
- intervenção;
- morte;
- ascensão.

---

# 102. TESTES

Criar aproximadamente 20–30 regressões direcionadas cobrindo pelo menos:

- formação de grupo;
- grupo sem formação quando afinidade insuficiente;
- proposta;
- reação do prefeito;
- efeito material;
- oposição entre grupos;
- conversão de grupo em facção;
- patente militar;
- promoção de facção;
- Knowledge institucional não onisciente;
- Deus real separado de fé;
- mortal adorado sem Divinity;
- rumor espiritual;
- intervenção;
- Renown;
- epíteto;
- alcance regional;
- MythicTrait;
- busca de poder;
- morte divina controlada;
- apoteose controlada;
- ExecutionOpportunity;
- finish;
- spare;
- letalidade situacional.

Preservar testes anteriores.

---

# 103. VALIDAÇÃO CONTROLADA

Antes da campanha longa, utilizar microcenários para comportamentos raros:

- mortal divinizado;
- Deus morto;
- apoteose;
- execução;
- misericórdia;
- grupo radical;
- oposição política;
- item tornando-se famoso.

Esses cenários comprovam capacidade técnica.

NÃO usar esses resultados como frequência natural.

---

# 104. CAMPANHA CURTA

Rodar aproximadamente:

```text
500 h
```

para verificar:

- integridade;
- explosão de entidades;
- crescimento de save;
- loops;
- grupos excessivos;
- política excessivamente ativa;
- religiões convertendo todos;
- MythicTraits dominando população;
- intervenção divina excessiva.

Corrigir apenas bugs/erros conceituais claros.

---

# 105. CAMPANHA LONGA

Depois executar:

```text
uma única campanha nova de 5000 horas
```

Não executar 10k/50k nesta fase.

5000 horas são suficientes para auditoria atual.

Registrar seed e versão.

---

# 106. NÃO OTIMIZAR PARA RESULTADOS ÉPICOS

Não definir metas como:

```text
precisamos de 3 deuses mortos
precisamos de 10 revoltas
precisamos de 20 personagens lendários
```

O objetivo é verificar se os mecanismos existem e interagem.

Zero mortes divinas pode ser resultado válido.

Zero apoteoses pode ser válido.

Poucos personagens míticos com grandes feitos é desejável.

---

# 107. CRITÉRIO DE SUCESSO

A fase é bem-sucedida se demonstrar que:

- necessidades individuais podem produzir organização coletiva;
- grupos conseguem produzir propostas;
- autoridades respondem segundo contexto;
- decisões políticas alteram sistemas reais;
- grupos podem entrar em conflito sem violência obrigatória;
- facções agem através de estrutura real;
- militares possuem hierarquia e interesses;
- fé produz comportamento;
- deuses existem objetivamente;
- crença continua subjetiva;
- rumor espiritual funciona;
- mortais podem ser divinizados socialmente;
- fama nasce de conhecimento real;
- epítetos refletem fama;
- indivíduos excepcionais influenciam suas próprias vidas sem roteiro;
- itens acumulam história;
- política, religião e indivíduos conseguem afetar uns aos outros;
- grandes histórias permanecem raras.

---

# 108. PRINCÍPIOS QUE NÃO PODEM SER QUEBRADOS

1. Need não é Action.

2. Conhecimento não é verdade objetiva.

3. Informação nova não executa ação automaticamente.

4. Grupo não é mente coletiva onisciente.

5. Facção não é apenas o líder.

6. Fé não prova divindade.

7. Adoração não cria automaticamente um Deus real.

8. Epíteto não prova habilidade real.

9. Feito desconhecido não gera fama social.

10. MythicTrait não garante destino.

11. Justiça não significa moralidade objetiva.

12. Poder não obriga heroísmo ou maldade.

13. Privação não gera revolta automaticamente.

14. Antagonismo não gera violência automaticamente.

15. `kill intent` não mata automaticamente.

16. `finish` só é fatal quando existe oportunidade terminal válida e a decisão foi tomada.

17. Deus morto não transfere automaticamente seu antigo domínio.

18. Política deve alterar estado real do mundo.

19. Grandes acontecimentos devem ser consequência, não objetivo da simulação.

20. Não maximizar quantidade de histórias.

Maximizar:

**coerência causal.**

---

# 109. RESULTADO ESPERADO

Ao final da Fase 5, quero que o mundo possa produzir naturalmente situações como:

```text
escassez
→ trabalhadores se organizam
→ exigem distribuição
→ prefeito recusa
→ militares recebem prioridade
→ ressentimento cresce
→ grupo se radicaliza
```

ou:

```text
general vence repetidamente
→ soldados contam feitos
→ fama cresce
→ recebe epíteto
→ parte dos soldados passa a tratá-lo como divino
→ culto informal surge
→ prefeito/religião local precisa reagir
```

ou:

```text
Deus intervém
→ poucas pessoas testemunham
→ versões diferentes circulam
→ fé se espalha
→ grupo religioso aparece
```

ou, extremamente raramente:

```text
mortal excepcional
→ trajetória de poder
→ conflito com Deus
→ vence
→ reivindica essência divina
→ torna-se Deus real
→ antigo culto precisa decidir como reagir
```

Nenhuma dessas sequências deve existir como script.

O motor fornece pessoas, conhecimento, necessidades, crenças, poder, organizações e consequências.

A história deve aparecer depois.

---

# 110. ENTREGA FINAL

Entregar:

- código;
- testes;
- relatório técnico;
- métricas;
- preservação das fases anteriores;
- `HISTORIAS_REAIS.md`;
- lista explícita de comportamentos não observados naturalmente;
- bugs/limitações;
- análise de custo de save/memória;
- separação entre capacidade comprovada em teste e emergência observada na campanha.

Não esconder regressões.

Não preencher lacunas com histórias inventadas.

Não chamar um comportamento de emergente se ele apareceu apenas em teste controlado.

Se algo não acontecer em 5000 horas:

**registrar isso como evidência.**

O objetivo desta fase não é provar que o mundo é épico.

O objetivo é provar que ele agora consegue formar:

**sociedade, poder, fé, mito e figuras históricas através de causalidade.**treinamento/trabalho e podem ampliar produção; reinos financiam resposta local. | Motor estratégico amplo de famílias, facções e reinos com alternativas coletivas concorrentes. | Na escala individual há mais diversidade de resposta que na escala coletiva. |
| Facções autônomas | Há líder real, nome, sede, tipo e filiação. | Membros organizados, recursos, recrutamento, ordens, ideologia executável, conflitos e sucessão interna. | A facção é principalmente base de dados; o líder agir sozinho não faz a organização agir. |
| Diplomacia | Relações numéricas iniciais existem no grafo. | Negociações, acordos, tratados, mudança diplomática causal, alianças e paz executável. | Relação inicial não produz um sistema diplomático autônomo. |
| Cultura | Rótulo cultural do reino e religião associada a residentes. | Formação por bioma/família real/história, influência ampla em personalidade, regras sociais, vestimentas e mudança cultural. | Cultura não evolui pela história militar/econômica como previsto. |
| Fé | Religião e devoção são campos distintos. | Devoção gerar necessidade religiosa e modificar escolhas por crença, ritual ou obrigação. | **Dados de fé existem; comportamento religioso executável ainda não.** |
| Persistência para campanhas extensas | Save versionado completo e continuidade determinística na mesma versão. | Migração geral entre fases e solução de armazenamento/retenção para crônicas muito grandes. | A longa atual exportou cerca de 1,1 GiB; persistir tudo tem custo prático. |
| Observabilidade e estabilidade | Testes dirigidos, diagnósticos, integridade e auditorias longas. | Cobertura dos sistemas ausentes, explicação integral das trajetórias e controle melhor do crescimento histórico. | Zero erros nas verificações não prova ausência de todos os bugs nem equilíbrio narrativo. |

## 5. Funcionalidades ainda não implementadas

Algumas já possuem um campo ou rótulo; aqui está classificado o **comportamento que falta**, não a mera existência desses dados.

| Funcionalidade prevista no original | O que falta concretamente | Impacto esperado quando existir |
|---|---|---|
| Governo por personalidade do rei | Governante avaliar decisões coletivas e executar impostos, expansão, negociação e outras políticas. | Reis diferentes passariam a produzir decisões e crises diferentes. |
| Rebelião, golpe e guerra civil | Organizadores, apoio, recursos, objetivos e resolução de disputa interna. | Crise e deslealdade poderiam transformar a liderança, em vez de permanecerem como estado ou conflito pessoal. |
| Novas dinastias após extinção | Pretendentes, tomada de poder e legitimação de nova liderança. | O fim de uma família real abriria uma nova trajetória política. |
| Mudança territorial, ocupação e anexação | Controle espacial alterado por ação política/militar real. | O mapa político passaria a ser consequência da história. |
| Destruição/reconstrução de localidades | Eventos modificarem mapas, instalações e população. | Ruínas teriam causa histórica; reconstrução criaria trabalho, deslocamento e conflitos. |
| Exércitos e guerra entre reinos/facções | Tropas, mobilização, deslocamento, poder de destacamentos, batalha e negociação de término. | Histórias de escala grande e consequências materiais em várias localidades. |
| Alistamento forçado e carreira militar dinâmica | Recrutar habitantes, mudar função e afetar mão de obra/produção. | A guerra reduziria trabalhadores e alteraria economia e famílias. |
| Comércio autônomo entre cidades | Mercadores itinerantes, carga, rota, custos e compra/revenda por observação. | Excedentes poderiam chegar a locais escassos, com risco e oportunidades. |
| Bloqueios e saques de carregamentos | Fluxos físicos e agentes capazes de interrompê-los. | Segurança e hostilidade ganhariam efeitos econômicos regionais. |
| Negociação, permuta e preço por relação | Acordos influenciados por vendedor, personalidade, confiança e reputação. | Relações teriam efeito direto no valor dos negócios. |
| Recompensa por criminoso e caça remunerada | Emissão/financiamento de recompensa e contrato conhecido por caçador. | NPCs poderiam perseguir alguém por renda, além de vingança ou dever de guarda. |
| Recrutamento e expansão de facções | Organização contratar membros, controlar recursos e criar objetivos. | Companhias e irmandades produziriam histórias próprias. |
| Religião organizada | Entidades religiosas, hierarquia, clero, recursos, ritos e agendas. | Fé passaria a gerar relações, obrigações e disputas executáveis. |
| Penitentes e perseguição de hereges | Subfacção, definição de heresia conhecida, alvos e escolha de resposta. | Conflitos religiosos poderiam surgir sem precisar de escassez alimentar. |
| Deuses como entidades ativas | Domínios, valores, desejos, memória divina, seguidores e relações entre deuses. | Abriria outra escala de histórias, além da humana/institucional. |
| Intervenções divinas | Visões, bênçãos, maldições, campeões, manifestações e consequências materiais. | Eventos excepcionais teriam causa e continuidade no mundo. |
| Ritual/contrato de invocação | Custos, condições, objetos, acordo e resultado executado pelo motor. | Jogador e NPCs poderiam participar da relação com divindades. |
| Itens divinos e artefatos históricos ativos | Propriedades, fama, reconhecimento e objetivos ligados ao objeto. | Itens poderiam concentrar histórias de posse, recuperação e conflito. |
| Loot físico de cadáver e herança | Transferência de posses a quem saqueia ou ao herdeiro; patrimônio/localidades transmitidos. | Morte também mudaria distribuição de bens e poder. |
| Combate por membros e slots completos | Vida/efeitos por região, armadura e equipamentos selecionados. | Diferenciaria incapacitação, perda funcional e morte pela região atingida. |
| Reputação falsa/manipulada | Criar e propagar afirmação falsa, atribuição incorreta e possível contestação. | Investigação teria disputa entre verdade objetiva e crença social. |
| Reputação coletiva completa | Opinião e políticas de cidade, reino, culto ou facção, com conflito frente à opinião individual. | Organizações reagiriam a feitos além dos guardas envolvidos num caso. |
| Decaimento e herança de reputação | Reduzir reputações menores com o tempo e efeitos contextuais sobre descendentes/associados. | Permitiria mudança de identidade pública e legado familiar. |
| Reconhecimento por aparência/equipamento famoso | Distinguir notícia de identificação pessoal e reconhecer objetos históricos. | Fama e identidade poderiam circular separadamente. |
| Lendas emergentes e promoção por feitos | Elevar importância/categoria e produzir títulos/capacidades/reconhecimento por trajetória real. | Um comum poderia se tornar uma figura histórica pelo que fez. |
| IA generativa para diálogo/lore | Camada narrativa conectada ao contexto do motor, sem decidir regras nem inventar consequências. | Melhoraria apresentação; não criaria, sozinha, guerras, deuses ou ações inexistentes. |
| Nascimento/envelhecimento durante a campanha | Regras de idade, descendência e passagem de gerações. **O original não fecha esse escopo.** | Poderia renovar famílias e dinastias, caso essa funcionalidade venha a ser definida. |

Os impactos desta tabela são **projeções**, não resultados de sistemas já testados. A ausência de guerra ou deuses não é um bug do combate ou do rumor: são mecanismos distintos que ainda precisam existir.

## 6. O que foi mudado ou acrescentado em relação ao original

| Tema | Proposta original | Implementação atual / mudança | Avaliação |
|---|---|---|---|
| Vida e combate | Atingir partes do corpo; cabeça/tórax zerados matam, demais regiões geram efeitos. | HP único, lesão geral, incapacidade, defesa e intenções de violência. | **Mudança efetiva de modelo.** Combate funcional, mas não é a mecânica corporal original. |
| Ferimentos após combate | Fora do combate, membros voltam ao normal e resta a vida restante. | Lesão geral permanece e melhora gradualmente por descanso/tratamento. | **Mudança efetiva.** Favorece consequência e recuperação persistentes, mas diverge da regra original. |
| Cálculo de dano | Dano da arma e modificadores de equipamento. | Base física + bônus limitado da arma, qualidade, HP, lesão, defesa e variação controlada; ainda sem equipamentos por slots. | **Mudado/parcial.** O dano não depende só do valor bruto da arma. A Fase 4.6 preservou a fórmula da base anterior. |
| Decisão de matar | Necessidade, personalidade e contexto escolhem resposta, incluindo vingança fatal. | Pressão letal dirigida, causa grave conhecida, compromisso, episódios, confiança e barreiras; depois compete com intenções não letais. | **Detalhamento posterior**, não uma ordem “raiva alta = matar”. Possibilidade técnica não garante execução natural. |
| População e densidade | Populações locais grandes, com parte individual e parte abstrata; números do original são exemplos. | Mundo completo padrão usa densificação de 4× e total redimensionado para cerca de 2–3 abstratos por persistente. | **Mudança posterior autorizada no equilíbrio da Fase 4.** Aumentou indivíduos simulados e reduziu totais anteriores; não preserva os antigos totais censitários. |
| Materialização/reposição | Habitante abstrato pode se tornar NPC quando necessário; profissão reage ao mundo. | Déficit persistente pode gerar aprendiz de cozinha, após considerar candidatos e recursos. | **Recorte funcional**, não reposição geral. Não cria população nova: converte um habitante já contado. |
| Personalidade e emoção | Valores exemplificados podem ultrapassar 100; descrição inicial mistura características e raiva. | Onze traços humanos estáveis em escala de 0–100, separados de raiva, mágoa, humilhação e desespero. | **Formalização/reorganização.** Personalidade divina extrema ainda não existe. |
| Persistência de intenção | Necessidades longas podem continuar com prioridade variável. | `Commitment` guarda causa, alvo, investimento, progresso e fracasso; aspirações têm registro próprio. | **Extensão posterior** do princípio original de continuidade. |
| Busca bloqueada | Need pode ficar `Blocked`, perguntar ou esperar por informação. | Estado explícito `waiting_for_information`, com preservação de causa, retomada por pista útil e retorno à rotina. | **Detalhamento posterior.** A informação não executa uma ação automaticamente. |
| Recuperação fisiológica | O original não detalha um circuito equivalente de recuperação de dano acumulado por privação. | Registro recuperável de dano real por fome/sede; recuperação segura, Need específica e orçamento único de cura. | **Acréscimo da Fase 4.1.** Continua um HP único; comer não cura automaticamente. |
| Alimentação preventiva | Necessidades gerais de fome e obtenção de comida. | Refeição normal considerada desde fome 35, reserva separada de 24h e caminhos de emergência com prazo biológico. | **Detalhamento posterior.** Ter reserva, adquirir alimento e comer são ações/condições distintas. |
| Investigação institucional | Percepção, rumor, segurança e guardas descritos de forma geral. | Caso formal, evidência individual, até três papéis de guarda e canal local com latência de seis horas. | **Acréscimo concreto.** Não é transmissão global nem uma instituição judicial completa. |
| Viagens de NPCs | Locomoção em matrizes e procura de pessoas/recursos. | Viagem física, pistas/rotas conhecidas, provisões, retorno e migração; residência muda apenas após permanência. | **Detalhamento posterior.** Deslocamento de pessoa não equivale a transporte comercial de carga. |
| Seed e versões | Mesma seed e versão das regras de geração produzem o mesmo início. | `GENERATION_VERSION` separado de `RULES_VERSION`; geografia/elenco podem ser preservados entre mudanças de comportamento. | **Reorganização técnica.** A simulação histórica continua dependente das regras vigentes. |
| Save e memória | Preservar estado importante e permitir continuidade. | JSON completo versionado, memórias/fatos cotidianos limitados, registros históricos extensos, recusa explícita de versões antigas. | **Escolha técnica com limites.** Não há migração geral e o histórico ocupa muito espaço. |
| Quests | Pedidos decorrentes de necessidades; nenhuma história principal obrigatória. | Causas reais, mas contratos implementados em categorias concretas e limitadas. | **Concretização limitada**, não criação arbitrária de qualquer missão possível. |
| Diálogo por IA | IA pode ser integrada depois do núcleo, apenas para apresentação. | Texto por regras/templates, sem IA generativa. | **Adiamento previsto**, não quebra do requisito do primeiro MVP. |

Não foi identificada uma substituição do princípio central por ações automáticas globais: o fluxo Need → alternativas → escolha → execução continua sendo a base. Entretanto, algumas escolhas coletivas ainda usam respostas muito estreitas, em vez da variedade estratégica prevista.

A diferença do combate foi explicitamente prevista pela [Fase 4, seção 22](</home/hugo/Área de trabalho/procedrual/fase_4.md:861>): ela pediu combate local simples e orientou não implementar membros individuais naquele momento. Portanto, é uma simplificação de fase, não evidência de que o requisito original tenha sido descartado definitivamente. A persistência de ferimentos também foi acrescentada pelas etapas posteriores.

### Diferenças e indefinições dentro do próprio original

- O original primeiro descreve devoção variável, inclusive personagem pouco devoto, e depois pede religiões sempre fanáticas. O estado atual tem religião e devoção numérica, mas nenhum desses modelos religiosos está implementado como agenda executável. Essa divergência precisa ser resolvida ao definir a religião.
- A visão inicial de facções associa fim do reino à morte de toda a família; o capítulo detalhado distingue **fim da dinastia** de **fim do território/reino**. A sucessão atual segue essa segunda distinção: registra crise e mantém o território.
- Nascimento/envelhecimento não possui uma regra final. Não convém afirmar que uma especificação demográfica completa foi removida: ela ainda precisava ser definida.

## 7. O que as últimas evidências permitem afirmar

Campanha da Fase 4.6: mundo novo, seed **Corven-46**, 5.000 horas, sem jogador, 1.568 NPCs persistentes iniciais, 3.926 habitantes abstratos e 66 localidades. Núcleo igual ao examinado neste relatório.

| Evidência preservada | O que demonstra | O que não demonstra |
|---|---|---|
| 91.167 compromissos adotados | Muitas intenções pessoais e institucionais são criadas e acompanham acontecimentos. | Não são 91.167 histórias completas nem 91.167 conflitos independentes. |
| 887 ocorrências de cadeias causais estritas | Violência pode gerar resposta de terceiro, nova violência e nova resposta por referências de fatos. | Não são automaticamente 887 guerras familiares únicas. |
| 13.792 verificações de área, 3.744 consultas e 845 respostas úteis | Investigação executa ações e algumas consultas renovam informação útil. | Toda pergunta resolver uma busca ou todo avistamento representar progresso importante. |
| 3.149 entradas em espera e 1.545 reativações | Busca pode suspender e voltar quando chegam informações. | Continuidade indefinida de toda perseguição ou conclusão garantida. |
| 23 mudanças para matar, envolvendo 12 NPCs; 57 ataques com intenção letal | A escolha letal já emerge naturalmente. | Homicídio deliberado realizado: foram **zero** nesta campanha, assim como incapacidade sob intenção letal. |
| 294 mortes: 260 fome, 11 fome+sede, 6 sede e 17 combate | Existe mortalidade por confronto, além da fisiológica. | A fome estar resolvida: 271 mortes envolveram fome, aproximadamente 92,2% do total. |
| Zero mortes alimentares com comida carregada | Não apareceu essa inconsistência específica nas campanhas finais de 500/5.000h. | Todo NPC conseguir acesso à comida disponível na cidade ou recuperar HP a tempo. |
| Zero erros nas 50 verificações de integridade da longa | Não apareceram violações dos invariantes verificadas nesses pontos. | Ausência de todo bug, perfeição de decisões ou boa qualidade narrativa em todos os casos. |
| 59 testes dirigidos finais aprovados; 18 regressões novas compostas | Comportamentos novos e preservação dirigida foram verificados. | Toda a suíte atual de 245 testes ter sido executada novamente de uma vez. |
| Save final de cerca de 1.101,6 MiB e 1.619.772 eventos históricos | História e estado foram exportados; há custo mensurável de retenção. | Escalabilidade já resolvida para campanhas muito maiores. |

A suíte completa anterior dessa entrega tinha 243 testes: 240 passaram e três falharam por efeitos de consultas/debug nos contadores. Os três foram corrigidos e passaram nos retestes. Após acrescentar os últimos casos, a coleção tem 245 testes; a validação final foi dirigida, com 59 aprovados. Não há falha pendente registrada, mas não se afirma uma nova execução integral dos 245.

**Qualidade narrativa atual:** há bastante material de conflito pessoal, cuidado, busca, fuga e resposta institucional. O avanço em relação ao primeiro MVP é real. A variedade de grandes acontecimentos permanece limitada porque os agentes coletivos e os sistemas históricos amplos ainda não existem; o fechamento de conflitos letais também permanece empiricamente limitado.

## 8. O que esta comparação sugere priorizar

Estas são recomendações de análise/implementação futura; **nenhuma mudança foi executada neste relatório**.

1. **Concluir melhor as trajetórias já possíveis.** Investigar por que ataques com intenção letal não chegaram à incapacidade e por que muitas buscas acabam sem desfecho. Observar encontros, retiradas, recuperação, informação e concorrência de necessidades antes de mexer em dano ou limiares.
2. **Estabilizar acesso individual e continuidade profissional.** Recuperação de HP existe, mas fome continua predominante. Ampliar a adaptação para outras funções e conectar excedentes/escassez por transporte real pode melhorar continuidade material; não deve ser tratado como solução automática.
3. **Dar agência às organizações.** Facções com recursos, membros, recrutamento e objetivos abririam histórias de grupo. Governos com decisões e saída de crise sucessória dariam continuidade a reinos.
4. **Criar identidade e consequência duradouras.** Títulos por feitos, reputação institucional, item histórico e herança poderiam transformar acontecimentos locais em trajetórias reconhecíveis.
5. **Só então integrar as escalas mais amplas conforme suas dependências.** Guerra precisa de tropas, recursos e objetivos; religião precisa de entidades, crenças e ações; deuses precisam de regras de intervenção. Acrescentar nomes ou textos não implementa essas funcionalidades.

Combate por membros merece uma decisão de projeto própria: o motor atual já usa outro modelo. Implementá-lo significaria revisar a mecânica física e os ferimentos, não apenas ativar uma função esquecida. A camada de IA narrativa pode melhorar a leitura do material existente, mas não substitui o trabalho nos comportamentos.

## 9. Fontes e arquivos para conferência

### Documento original

- [Visão geral, relações, conhecimento e profissões](</home/hugo/Área de trabalho/procedrual/instruction.md:1>)
- [Geração, seed e mapas](</home/hugo/Área de trabalho/procedrual/instruction.md:201>)
- [Necessidades e prioridades](</home/hugo/Área de trabalho/procedrual/instruction.md:600>)
- [Facções e reinos](</home/hugo/Área de trabalho/procedrual/instruction.md:1838>)
- [Política, diplomacia, guerra e cultura](</home/hugo/Área de trabalho/procedrual/instruction.md:2539>)
- [Religião e deuses](</home/hugo/Área de trabalho/procedrual/instruction.md:2634>)
- [Itens, equipamentos e inventário](</home/hugo/Área de trabalho/procedrual/instruction.md:2944>)
- [Economia, comércio e profissões](</home/hugo/Área de trabalho/procedrual/instruction.md:3178>)
- [Combate, ferimentos, morte e hereditariedade](</home/hugo/Área de trabalho/procedrual/instruction.md:3594>)
- [Reputação](</home/hugo/Área de trabalho/procedrual/instruction.md:3608>)
- [Títulos, quests e história](</home/hugo/Área de trabalho/procedrual/instruction.md:5341>)
- [Categorias, população abstrata e níveis de simulação](</home/hugo/Área de trabalho/procedrual/instruction.md:5463>)
- [Diálogo, arquitetura, persistência e testes](</home/hugo/Área de trabalho/procedrual/instruction.md:5639>)
- [Escopo do primeiro MVP](</home/hugo/Área de trabalho/procedrual/instruction.md:5930>)

### Código atual

- [Versões](</home/hugo/Área de trabalho/procedrual/procedural/__init__.py:3>) e [geração/configuração](</home/hugo/Área de trabalho/procedrual/procedural/generation.py:24>)
- [Entidades e personalidade](</home/hugo/Área de trabalho/procedrual/procedural/models.py:31>) e [grafo](</home/hugo/Área de trabalho/procedrual/procedural/relationships.py:6>)
- [Turno e morte](</home/hugo/Área de trabalho/procedrual/procedural/engine.py:102>)
- [Necessidades](</home/hugo/Área de trabalho/procedrual/procedural/needs.py:117>), [objetivos](</home/hugo/Área de trabalho/procedrual/procedural/goals.py:39>) e [respostas coletivas](</home/hugo/Área de trabalho/procedrual/procedural/goals.py:579>)
- [Vida pessoal](</home/hugo/Área de trabalho/procedrual/procedural/personal.py:13>), [compromissos/aspirações](</home/hugo/Área de trabalho/procedrual/procedural/agency.py:16>) e [quests](</home/hugo/Área de trabalho/procedrual/procedural/quests.py:8>)
- [Alimentação e agenda de decisão](</home/hugo/Área de trabalho/procedrual/procedural/feeding.py:24>), [recuperação](</home/hugo/Área de trabalho/procedrual/procedural/recovery.py:5>) e [migração](</home/hugo/Área de trabalho/procedrual/procedural/migration.py:9>)
- [Economia](</home/hugo/Área de trabalho/procedrual/procedural/economy.py:12>), [profissões/reposição](</home/hugo/Área de trabalho/procedrual/procedural/professions.py:166>) e [população](</home/hugo/Área de trabalho/procedrual/procedural/population.py:4>)
- [Itens](</home/hugo/Área de trabalho/procedrual/procedural/items.py:10>) e [combate](</home/hugo/Área de trabalho/procedrual/procedural/conflicts.py:15>)
- [Pressão letal](</home/hugo/Área de trabalho/procedrual/procedural/lethality.py:67>), [investigação](</home/hugo/Área de trabalho/procedrual/procedural/investigation.py:10>) e [justiça](</home/hugo/Área de trabalho/procedrual/procedural/justice.py:13>)
- [Conhecimento/diálogo](</home/hugo/Área de trabalho/procedrual/procedural/knowledge.py:12>), [interpretação social](</home/hugo/Área de trabalho/procedrual/procedural/social.py:10>) e [sucessão política](</home/hugo/Área de trabalho/procedrual/procedural/politics.py:3>)
- [Eventos](</home/hugo/Área de trabalho/procedrual/procedural/events.py:9>), [save/load](</home/hugo/Área de trabalho/procedrual/procedural/persistence.py:48>), [interface](</home/hugo/Área de trabalho/procedrual/procedural/ui.py:54>) e [validação](</home/hugo/Área de trabalho/procedrual/procedural/validation.py:9>)

### Mudanças posteriores e evidências

- Especificações: [Fase 2](</home/hugo/Área de trabalho/procedrual/fase_2.md>), [Fase 3](</home/hugo/Área de trabalho/procedrual/fase_3.md>), [Fase 3.2](</home/hugo/Área de trabalho/procedrual/fase_3_2.md>), [Fase 4](</home/hugo/Área de trabalho/procedrual/fase_4.md>), [Fase 4.1](</home/hugo/Área de trabalho/procedrual/fase_4_1.md>), [Fase 4.5](</home/hugo/Área de trabalho/procedrual/fase_4_5.md>) e [Fase 4.6](</home/hugo/Área de trabalho/procedrual/fase_4_6.md>)
- [Relatório técnico atual](</home/hugo/Área de trabalho/procedrual/RELATORIO_FASE_4_6.md>)
- [Histórias reais e fatalidades](</home/hugo/Área de trabalho/procedrual/reports/fase_4_6/HISTORIAS_REAIS.md>)
- [Validação dos testes](</home/hugo/Área de trabalho/procedrual/reports/fase_4_6/validacao_testes.json>) e [registro de execuções](</home/hugo/Área de trabalho/procedrual/reports/fase_4_6/EXECUCOES.json>)
- [Resumo da campanha de 5.000h](</home/hugo/Área de trabalho/procedrual/reports/fase_4_6/global_5000h/resumo.json>) e [análise narrativa](</home/hugo/Área de trabalho/procedrual/reports/fase_4_6/analise_narrativa.json>)

Os relatórios [COMPARATIVO_ESPECIFICACAO_MVP.md](</home/hugo/Área de trabalho/procedrual/COMPARATIVO_ESPECIFICACAO_MVP.md>) e [RELATORIO_ESTADO_IMPLEMENTACAO.md](</home/hugo/Área de trabalho/procedrual/RELATORIO_ESTADO_IMPLEMENTACAO.md>) permanecem como registros históricos das versões anteriores. Suas descrições do alcance de combate, recuperação, investigação e reposição profissional não devem ser usadas como inventário da versão atual.
