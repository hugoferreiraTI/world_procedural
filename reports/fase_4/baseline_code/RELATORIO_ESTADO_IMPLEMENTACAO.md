# O que foi implementado e o que ainda falta no projeto

**Data:** 8 de outubro de 2026. **Versão conferida no código:** `mvp-4-fase3.2-final`. **Geração:** `mvp-4`.

Este relatório compara o motor atual com a visão de `instruction.md` e as entregas das Fases 2, 3, correção alimentar e 3.2. A conferência foi feita no código atual e nos registros das auditorias finais. O hash do motor continua idêntico ao da última auditoria. Não foram alteradas regras nem executadas novas campanhas para produzir este documento.

**O núcleo da simulação já funciona, com vida pessoal e economia local. O projeto completo ainda não está implementado.** A maior diferença entre o que já existe e a visão final está nas consequências: um NPC pode desejar reparação, mas não atacar; uma família pode procurar alguém e sofrer luto, mas não gerar novas gerações; um reino pode trocar de governante, mas não disputar territórios.

## Como interpretar os estados

| Estado | Critério usado neste relatório |
| --- | --- |
| Implementado | Existe comportamento executável no motor, dentro do escopo descrito. Não significa que o resultado esteja perfeitamente equilibrado. |
| Parcial | Existe execução, mas faltam partes relevantes para o sistema completo. |
| Apenas base/dados | Existem nomes, campos, relações ou estruturas, sem o comportamento principal esperado. |
| Ausente | Não existe um caminho funcional que execute o sistema durante o jogo. |

Não foi calculada uma porcentagem de conclusão: um campo de religião e um sistema de combate não têm o mesmo tamanho, e a especificação mistura funcionalidades básicas com expansões amplas.

## O que mudou ao longo das entregas

| Entrega | O que foi acrescentado | Limite principal |
| --- | --- | --- |
| MVP e correções iniciais | Geração, NPCs, decisões, profissões, economia, conhecimento, relações, quests básicas, terminal e persistência. Correções de descanso, comércio e reputação. | Provam a execução do mundo; não completam todos os sistemas da visão original. |
| Fase 2 | Cuidado e busca familiar, luto, reparação não violenta, proteção, reconhecimento, ascensão pessoal e novas quests. | Os caminhos sociais ainda são locais e relativamente curtos; não incluem combate, política ou descendência. |
| Fase 3 | Diagnóstico alimentar local, serviços temporários, treinamento de cozinheiros, materialização limitada de habitantes abstratos e censo coerente. | Adaptação concentrada na cadeia trigo → comida, sem reposição geral de profissões. |
| Correção alimentar | Separação entre reserva, refeição e emergência; margem de sobrevivência; rejeição de soluções lentas e refeições imediatas. | Ter comida no município continua diferente de conseguir alimento individualmente. |
| Fase 3.2 | Pressão preventiva contextual, financiamento da segunda ração, compra parcial/lote, crédito salarial correto, ofertas executáveis e correções sociais. | Corrige coerência, mas não elimina fome, pobreza ou a falta de diversidade das consequências. |

**Duas informações do comparativo antigo precisam ser atualizadas:** necessidades pessoais já não estão ausentes; reposição profissional também já não está totalmente ausente. Ambas existem, com os limites detalhados abaixo.

## Funcionalidades implementadas

### Motor, mundo e interação

| Funcionalidade | O que funciona hoje | Limite do escopo |
| --- | --- | --- |
| Seed e aleatoriedade determinísticas | Geração reproduzível e estado do gerador salvo. Versões de geração e de regras são identificadas separadamente. | Comparações entre versões antigas nem sempre mantinham a mesma geração; a auditoria atual verificou a preservação da geração inicial. |
| Mundo procedural | Mapa global finito 500×500, reinos, cidades, vilas, biomas e grades locais de pontos de interesse. | A existência dos lugares não implica conteúdo profundo em cada um. |
| Movimentação e tempo | Movimento em matriz, entrada/saída de mapas pelo jogador e passagem conjunta do tempo. Uma ação válida normalmente representa uma hora; consultas não avançam o mundo. | Não há calendário demográfico ou sazonal completo. |
| NPCs persistentes e IDs | Identidade, posição, profissão, personalidade, dinheiro, inventário, estado físico, necessidades e conhecimento próprios. | Não equivale a simular individualmente todos os habitantes contabilizados. |
| Decisão autônoma | Estado/conhecimento → necessidade → prioridade → soluções → objetivo → ação → consequência. O mundo também roda sem jogador. | Não há garantia de uma solução viável para toda necessidade. |
| Personalidade nas decisões | Onze traços persistentes, incluindo ambição, vingatividade e temperamento; parte deles influencia prioridades, escolhas e interpretação social. | Não existe uma simulação emocional completa. |
| Eventos e consequências | Event Bus conecta ações, conhecimento, reputação, população e sucessão. | Só pode produzir consequências dos comportamentos realmente existentes. |
| Persistência | Save/load JSON versionado, incluindo RNG, entidades, itens, memórias, necessidades, objetivos e economia. | Não há migração automática geral de saves antigos para regras novas. |
| Interface e comandos | Terminal em português, mapa visível, consultas, conversa, comércio, coleta, trabalho, informação, acompanhamento e quests. | Não há interface gráfica de jogo completa. |
| Instrumentação | Traces de decisão, métricas, registros alimentares, narrativos, econômicos, censo, checkpoints e relatórios. | Observações do auditor não são automaticamente conhecimento dos NPCs. |

Fontes principais: [geração](</home/hugo/Área de trabalho/procedrual/procedural/generation.py>), [motor](</home/hugo/Área de trabalho/procedrual/procedural/engine.py>), [necessidades](</home/hugo/Área de trabalho/procedrual/procedural/needs.py>), [objetivos](</home/hugo/Área de trabalho/procedrual/procedural/goals.py>) e [persistência](</home/hugo/Área de trabalho/procedrual/procedural/persistence.py>).

### Sobrevivência e economia executável

| Funcionalidade | O que foi implementado | O que isso não garante |
| --- | --- | --- |
| Fome, sede, fadiga e HP | Fisiologia compartilhada por jogador e NPCs; descanso, consumo e dano progressivo por privação. | Sobrevivência de todos os indivíduos. |
| Consumo de comida | A ação de comer consome uma ração real do inventário e reduz fome. Compra e alimentação são efeitos distintos. | O NPC alcançar comida antes de morrer. |
| Reserva alimentar | Alvo normalmente de duas rações, ajustável por viagem conhecida; prioridade considera cobertura, oportunidade, espera e reposição conhecida. | Reserva completa permanente. |
| Emergência alimentar | Necessidades vitais podem interromper objetivos; alternativas lentas são avaliadas contra a margem de sobrevivência. Há aquisição com refeição imediata. | Resgatar um estado em que nenhuma ação isolada evita a morte. |
| Itens e inventários | Dono, quantidade, qualidade, raridade, origem, criador, criação, transferência e consumo. | Equipamento funcional em combate. |
| Mercado local | Compra, venda, preços por estoque, cotação marginal de lotes e diferença entre preço de compra e venda. | Transporte de mercadorias entre localidades. |
| Produção básica | Agricultura, mineração, madeira, caça simplificada, cozinha e ferraria geram bens; atividades de conversão usam insumos. | Cadeias industriais completas ou caça de animais simulados. |
| Remuneração | Salários usam caixa real; crédito fracionário em sextos persiste e é convertido em moeda quando devido. | Emprego disponível ou renda suficiente em qualquer situação. |
| Serviços locais | Preparo avulso e distribuição de refeições dependem de quota, estoque, local e elegibilidade. | Uma oferta permanecer disponível até a chegada do interessado. |

A economia contém fontes agregadas já declaradas, como renda do trabalho abstrato, renovação de coleta e produção rural. Por isso, não deve ser descrita como um sistema totalmente fechado. A Fase 3.2 não acrescentou renda universal, redistribuição automática nem comida garantida para todos.

Fontes: [alimentação](</home/hugo/Área de trabalho/procedrual/procedural/feeding.py>), [economia](</home/hugo/Área de trabalho/procedrual/procedural/economy.py>), [profissões](</home/hugo/Área de trabalho/procedrual/procedural/professions.py>) e [itens](</home/hugo/Área de trabalho/procedrual/procedural/items.py>).

## Sistemas que existem, mas ainda estão parciais

### Vida pessoal, informação e histórias

| Sistema | O que já acontece | O que ainda falta | Impacto esperado ao completar |
| --- | --- | --- | --- |
| Família e vínculos | Parentesco, casamento e amizade; cuidado material, ausência percebida, busca, reencontro e luto. | Formação e transformação ampla das famílias durante a campanha, separação, novos descendentes e patrimônio familiar. | Continuidade entre gerações e conflitos familiares mais variados. |
| Busca familiar | Usa observações e fatos conhecidos; procura locais, pede informação e confirma presença ou restos. | Busca entre cidades, investigação mais extensa e caminhos informativos mais produtivos. | Desaparecimentos deixariam de depender tanto de um encontro local. |
| Luto | Morte conhecida pode gerar busca de companhia e lembrança. | Evolução emocional prolongada e mais consequências sobre relações e projetos pessoais. | Perdas poderiam alterar uma trajetória por mais tempo. |
| Vingança/reparação | Dano conhecido gera investigação, denúncia ou afastamento. | Agressão, defesa, punição, cobrança persistente e outras formas de reparação. | Hostilidade passaria a produzir conflitos materiais e continuidade. |
| Proteção | Acompanhamento, permanência perto de protegido, denúncia e afastamento de ameaça. | Interceptar agressão, lutar, resgatar de perigo físico e defender residência. | Proteção teria consequências físicas além do apoio social. |
| Reconhecimento e ascensão | Necessidades executáveis podem motivar ajuda, trabalho, venda de excedente e treinamento. | Disputa de cargos, conquista de poder, promoção geral de categoria e títulos por diferentes feitos. | Ambição poderia gerar histórias além de renda e um gesto de ajuda. |
| Conhecimento e rumores | Fatos individuais, fonte, confiança, propagação por contatos, memória limitada e efeitos deduplicados. | Mentira deliberada, propaganda, versões falsas construídas e investigação complexa de contradições. | O conflito sobre informação poderia criar mistérios e manipulação. |
| Reputação e confiança | Ajuda, roubo, apoio e recusas podem mudar interpretação e disposição para interagir. | Reputação coletiva completa, recompensas, perseguição organizada e herança de reputação. | Feitos poderiam alterar acesso a grupos, cargos e ameaças futuras. |
| Quests emergentes | Tipos executáveis de comida, cuidado familiar, localização, informação, companhia e proteção. | Missões de combate, resgate físico, conquista e grandes cadeias dependentes de sistemas ainda ausentes. | Mais variedade de objetivos e consequências. |
| Diálogo | Frases por regras usam necessidades, fatos e relações conhecidas. | Voz individual mais rica e apresentação narrativa sofisticada. | Melhoraria a leitura das histórias; não criaria comportamentos ausentes. |
| Títulos e categorias | Comum/importante/lendário existem; há um apelido específico do jogador por cumprir pedidos alimentares. | Evolução geral de NPC comum a importante/lendário por feitos e títulos amplos. | Relevância histórica poderia surgir durante a campanha. |

Uma necessidade chamada `revenge` não significa que o NPC possua uma ação de matar. Da mesma forma, uma necessidade satisfeita não significa que o conflito social terminou de maneira duradoura.

Fontes: [necessidades pessoais](</home/hugo/Área de trabalho/procedrual/procedural/personal.py>), [ações pessoais](</home/hugo/Área de trabalho/procedrual/procedural/personal_actions.py>), [conhecimento](</home/hugo/Área de trabalho/procedrual/procedural/knowledge.py>), [interpretação social](</home/hugo/Área de trabalho/procedrual/procedural/social.py>) e [quests](</home/hugo/Área de trabalho/procedrual/procedural/quests.py>).

### Adaptação econômica, população e reinos

| Sistema | O que já acontece | O que ainda falta | Impacto esperado ao completar |
| --- | --- | --- | --- |
| Diagnóstico e resposta econômica | Localidades distinguem matéria-prima, capacidade, mão de obra, acesso e poder de compra; podem ampliar cultivo, publicar serviços e abrir formação. | Adaptação equivalente para várias cadeias e profissões. | Crises teriam respostas mais variadas, com novas dependências reais. |
| Reposição profissional | Moradores adequados podem aprender cozinha. Sem candidato e após déficit persistente, recursos e condições permitem materializar um aprendiz da população abstrata. | Reposição geral de agricultores, ferreiros, guardas, comerciantes etc. | Evitaria perda definitiva de outras funções, sem substituir a pessoa falecida. |
| Carreira | Treino produtivo, remuneração, progresso, abandono e mudança para cozinheiro. | Carreiras completas, múltiplos ofícios, contratação ampla e progressão institucional. | Falta de renda poderia mudar trajetórias por mais caminhos. |
| População abstrata | Consumo e renda agregados, disponibilidade para materialização e separação entre abstratos e residentes persistentes. | Nascimento, envelhecimento, mortes abstratas por privação e migração. | O total populacional teria evolução demográfica real. |
| Censo e perdas individuais | Materializar transfere alguém do grupo abstrato para o persistente; morte de residente reduz o total uma vez. | Acompanhamento demográfico de todos os habitantes agregados. | Evitaria tratar o número populacional como uma sociedade completamente simulada. |
| Níveis de simulação | Decisões de NPCs ocorrem em intervalos de 1, 3 ou 6 horas; a fisiologia continua por hora. | LOD completo, com atividades resumidas de personagens distantes e preservação de consequências. | Poderia permitir mais indivíduos, dependendo de validação de custo e comportamento. |
| Reinos | Território inicial, localidades, família real, tesouro, estados separados e ajuda financeira alimentar limitada. | Administração ampla, impostos, disputas internas e mudanças territoriais. | Reinos passariam a agir como organizações políticas mais completas. |
| Sucessão | Escolha de familiar vivo após morte do governante; crise quando a dinastia acaba. | Pretendentes, golpes, eleição, nova dinastia e transformação completa da rotina do sucessor. | A morte de um governante abriria caminhos políticos diferentes. |
| Criminalidade e guarda | Roubo real de alimento, percepção, reputação negativa, resposta local e multa. | Justiça persistente, prisão, julgamento, perseguição e captura. | Crimes deixariam consequências mais duradouras. |
| História procedural | Fundações, simulação inicial limitada e eventos posteriores com causas rastreáveis. | História prévia ampla com guerras, destruição, ruínas resultantes e reconstrução. | O cenário inicial poderia refletir grandes acontecimentos reais da simulação. |

**Reposição profissional atual: sequência concreta**

Déficit culinário → diagnóstico local → procura de candidato existente → aprendizagem produtiva; na falta de candidato, condições suficientes podem permitir um habitante abstrato virar aprendiz persistente → prática → mudança de profissão.

Isso não recria o morto com as mesmas memórias, família ou reputação. Não repõe reis ou personagens lendários. A presença de um novo cozinheiro também não garante que ele sobreviva ou que a cidade se recupere.

Fontes: [treinamento e materialização](</home/hugo/Área de trabalho/procedrual/procedural/professions.py:164>), [população](</home/hugo/Área de trabalho/procedrual/procedural/population.py>) e [sucessão](</home/hugo/Área de trabalho/procedrual/procedural/politics.py>).

## O que ainda não foi implementado como comportamento funcional

| Sistema | Estado atual | Consequência da ausência | O que sua implementação poderia acrescentar |
| --- | --- | --- | --- |
| Ataques e combate entre NPCs | Ausente. Não há ação de ataque causando dano a outro personagem. | Inimigos não podem ferir ou matar uns aos outros. | Confronto, defesa, fuga, ferimentos, testemunhas e repercussão familiar. |
| Combate do jogador | Ausente. Armas existentes não compõem um sistema de luta. | Não é possível cumprir uma vingança por combate. | Intervenção física do jogador e consequências sociais correspondentes. |
| Equipamento e combate por membros | Apenas itens/base para equipamento; combate por membros ausente. | Qualidade ou dano nominal de uma arma não altera confrontos que não existem. | Escolhas táticas, proteção corporal e utilidade funcional de armas/armaduras. |
| Ferimentos e doenças | Ausentes como sistemas próprios. Há HP e privação. | Não há lesões de combate, tratamento médico ou epidemias executáveis. | Novas causas de necessidade, incapacidade e morte. |
| Guerras e exércitos | Ausentes. Soldados e campo militar não constituem guerra. | Não há batalha, cerco, recrutamento militar dinâmico ou conquista. | Conflitos coletivos com custo populacional e econômico. |
| Diplomacia dinâmica | Apenas base de relações iniciais entre entidades. | Reinos não negociam tratados, alianças ou guerras. | Relações políticas capazes de mudar a história territorial. |
| Facções atuantes | Apenas base de grupos, líder, sede e filiação. | Não há agenda coletiva, recrutamento amplo, disputa de poder ou expansão. | Conflitos organizados além de necessidades individuais. |
| Política ampla e revoluções | Ausentes. Sucessão e auxílio econômico não equivalem a política completa. | Pobreza não gera automaticamente organização anti-Estado ou revolta. | Disputas de legitimidade, medidas públicas e reação coletiva. |
| Religião organizada | Apenas nomes, religião declarada e devoção. | Fé não produz culto organizado, conversão, perseguição ou objetivos religiosos completos. | Motivações e conflitos independentes da alimentação. |
| Deuses e intervenção divina | Ausentes. | Não há entidade divina agindo, milagre ou punição divina. | Novas causas e consequências, conforme regras futuras. |
| Migração e viagens autônomas entre cidades | Ausentes para a IA atual. O jogador pode transitar. | NPC não resolve seus problemas mudando espontaneamente de localidade. | Busca distante, deslocamento por crise e reorganização da população. |
| Caravanas e comércio intermunicipal | Ausentes. | Estoque excedente de uma cidade não chega automaticamente a outra. | Transporte real, oportunidades de trabalho, escolta e risco logístico. |
| Nascimento, envelhecimento e descendência | Ausentes. | Não existem novas gerações nem morte por idade. | Continuidade demográfica e familiar de longo prazo. |
| Herança de bens e reputação | Ausente como sistema sucessório patrimonial. | Trocar o governante não executa herança geral. | Disputa e transmissão de patrimônio, identidade e legado. |
| Ruínas, destruição e reconstrução dinâmicas | Ausentes. Pontos abandonados podem vir da geração inicial. | Localidades não são destruídas por uma guerra e reconstruídas depois. | Alteração persistente do mapa pela história. |
| Recompensas e caçada a criminosos | Ausentes. | Reputação criminosa não cria uma perseguição organizada com recompensa. | Histórias de caça, fuga, proteção e captura. |
| IA generativa durante o jogo | Ausente. Textos e decisões são produzidos por regras locais. | Não há modelo generativo redigindo diálogo/lore em tempo de execução. | Poderia melhorar a apresentação dos fatos; não substitui os sistemas de ação. |

Os impactos da última coluna são possibilidades de projeto, não resultados já demonstrados por testes.

### Por que os inimigos não atacam

O motor já pode interpretar um fato `CharacterKilled` e reagir socialmente a ele em cenários controlados. Porém, falta a ação que produziria essa morte durante a campanha. Um consumidor de evento não equivale ao sistema que causa o evento.

Hoje, uma cadeia executável é **roubo conhecido → necessidade de reparação → investigação → denúncia**. A continuação **confronto → dano → morte violenta** ainda não existe. Combate local poderia ser desenvolvido como uma etapa própria; não exige que guerras entre reinos já estejam implementadas.

As mortes reais das últimas campanhas foram por fome/sede. Chamá-las de “morte natural” pode confundir essa privação com envelhecimento, que ainda não existe.

## O que a Fase 3.2 corrigiu e o que continua sem solução completa

| Problema | Correção implementada | Limite que permanece |
| --- | --- | --- |
| Reserva preventiva quase nunca vencia | Pressão por cobertura, oportunidade observada, reposição conhecida, espera limitada e viagem planejada. | Sede, sono, renda e necessidades pessoais podem vencer; reserva não é garantia de sobrevivência. |
| Uma ração impedia buscar renda para a segunda | Viabilidade econômica passa a considerar o déficit até o alvo. | Pode não existir renda executável. |
| Compra incompleta ou lote incoerente | Compra parcial ou lote limitado por déficit, orçamento, estoque e preços marginais. | Mercado pode estar inacessível ou caro para aquele indivíduo. |
| Crédito salarial parcial considerado fracasso | Trabalho pago e creditado são sucessos distintos; não recebem falha só por faltar moeda inteira. | Crédito ainda não convertido não compra alimento imediatamente. |
| Trabalho anunciado sem capacidade real | Oferta observada respeita quota/insumos; informação expira e execução revalida. | Oferta verdadeira pode desaparecer antes da chegada. |
| Intenção profissional incompatível | Local/economia exigidos são verificados; não foi criado acesso remoto ao caixa natal. | Algumas ocupações/localizações continuam sem atividade viável. |
| Denúncia ao próprio culpado | Exclusão pela informação conhecida e revalidação na execução. | Sem guarda independente ou evidência conhecida, o episódio pode continuar bloqueado. |
| Informação velha ou repetida parecia progresso | Utilidade contextual, retorno honesto de aprendizagem e memória curta de respostas inúteis. | Interlocutor pode não saber nada útil; não foi criado conhecimento perfeito. |
| Aquisição adiada empatava com refeição urgente | Quando há solução equivalente viável de adquirir e comer, o adiamento é descartado na emergência pertinente. | Falta de recurso e convergência de fome/sede ainda podem gerar morte. |

**A fome não foi resolvida como problema geral.** Há melhoria de prevenção e correção de bugs, mas continuam existindo desigualdade de acesso, saturação de trabalho, pouca liquidez individual, limitações de ajuda e bloqueios locais. Não seria correto chamar o sistema de abastecimento completo ou declarar sucesso apenas porque a cidade possui estoque.

## Evidências da última versão validada

Esta seção resume testes já executados na entrega anterior, sem apresentá-los como uma nova rodada feita para este relatório.

- **179 testes passaram:** 130 anteriores preservados e 49 novos.
- Três campanhas de **10.000 horas**: Dovha jogador, Dovha espectador e Mira mundo.
- Reprodução integral idêntica dos três saves; save/load e continuação determinística de 24 horas verificados.
- Invariantes e balanços monetários sem erro nos checkpoints finais.
- Nenhuma denúncia validada ao próprio acusado e nenhuma morte com comida carregada nas campanhas finais.

| Campanha | Mortes finais | NPCs com alvo alimentar completo no final | Materializações de aprendizes | Mudanças para cozinheiro concluídas |
| --- | --- | --- | --- | --- |
| Dovha jogador | 113 | 14,78% | 10 | 11 |
| Dovha espectador | 103 | 17,48% | 4 | 5 |
| Mira mundo | 119 | 15,63% | 7 | 10 |

Materializações e mudanças profissionais são contagens diferentes: tornar-se persistente não significa concluir a formação. As mudanças incluem candidatos existentes e aprendizes materializados.

No conjunto, a versão anterior registrou **331 mortes**, e a atual **335**. As reservas finais melhoraram, mas esse resultado não demonstra redução geral da mortalidade. Há mais satisfações de necessidades pessoais, mas menos seleções pessoais; nenhum desses números, sozinho, prova histórias melhores.

Foram reconstruídos **16 relatos reais**, com buscas, luto, ajuda, denúncia, carreiras, crédito, oferta perdida, quest e sucessão. Existem cadeias além de uma lista de mortes, mas não foram observadas guerras, ataques ou intervenção divina — esses comportamentos não existem no motor.

Fontes: [relatório da Fase 3.2](</home/hugo/Área de trabalho/procedrual/RELATORIO_FASE_3_2.md>), [comparação numérica](</home/hugo/Área de trabalho/procedrual/reports/fase_3_2/comparativo.json>), [verificação final](</home/hugo/Área de trabalho/procedrual/reports/fase_3_2/verificacao_final.json>), [saída dos testes](</home/hugo/Área de trabalho/procedrual/reports/fase_3_2/testes_finais.txt>) e [histórias observadas](</home/hugo/Área de trabalho/procedrual/reports/fase_3_2/HISTORIAS_EMERGENTES.md>).

## O que falta para as histórias ganharem mais variedade

Para a ausência de ataques, a funcionalidade necessária é **agressão/combate local**, com motivação, risco, defesa, fuga, dano e consequências conhecidas pelas testemunhas. Apenas aumentar vingatividade ou hostilidade não cria essa ação.

Para a predominância alimentar, importa aprofundar **acesso e continuidade dos caminhos já existentes**: renda realmente alcançável, ajuda material, alternativas profissionais e circulação de recursos. Adicionar um novo desejo sem uma solução executável pode apenas gerar mais necessidades bloqueadas.

Para histórias de poder, são necessários **cargos, facções atuantes, decisões políticas e disputa institucional**. A ambição atual possui saídas limitadas; um valor alto não transforma alguém em pretendente ao trono.

Para histórias entre gerações, faltam **nascimento, envelhecimento, descendência e herança**. Para histórias religiosas, faltam ações e consequências de fé; para grandes guerras, faltam recrutamento, logística, diplomacia e combate coletivo.

A ampliação da população e um LOD completo podem aumentar o elenco e permitir continuidade, mas não geram por si mesmos novos tipos de consequência. Este documento não define nem implementa a Fase 4; seu escopo deve seguir a especificação que for aprovada para ela.

## Documentos de referência e cuidado com comparativos antigos

| Documento | Como deve ser usado |
| --- | --- |
| [instruction.md](</home/hugo/Área de trabalho/procedrual/instruction.md>) | Visão geral e escopo original; não é prova de que cada sistema descrito foi implementado. |
| [fase_2.md](</home/hugo/Área de trabalho/procedrual/fase_2.md>) | Especificação da expansão pessoal e social. |
| [fase_3.md](</home/hugo/Área de trabalho/procedrual/fase_3.md>) | Especificação da adaptação econômica e trabalho. |
| [correcao_alimentar.md](</home/hugo/Área de trabalho/procedrual/correcao_alimentar.md>) | Correção da alimentação individual. |
| [fase_3_2.md](</home/hugo/Área de trabalho/procedrual/fase_3_2.md>) | Escopo das últimas correções locais. |
| [COMPARATIVO_ESPECIFICACAO_MVP.md](</home/hugo/Área de trabalho/procedrual/COMPARATIVO_ESPECIFICACAO_MVP.md>) | Retrato histórico de `mvp-2`; seus estados de ausência de necessidades pessoais e reposição profissional estão superados. |
| [README.md](</home/hugo/Área de trabalho/procedrual/README.md>) | Orientações gerais; ainda cita a identificação anterior dos saves em alguns trechos. A versão atual foi confirmada em [procedural/__init__.py](</home/hugo/Área de trabalho/procedrual/procedural/__init__.py>) e no [manifesto final](</home/hugo/Área de trabalho/procedrual/reports/fase_3_2/manifesto_auditoria.json>). |

Os relatórios anteriores continuam preservados como evidência de suas respectivas versões. Este documento é o inventário atualizado de implementação, não uma reclassificação retroativa dos testes antigos.
