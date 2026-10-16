# Comparativo entre a especificação e o MVP atual

**Data:** 7 de outubro de 2026. **Versão analisada:** `mvp-2`.

**Conclusão:** o núcleo solicitado para o primeiro MVP está presente: geração, entidades, necessidades, decisões, ações, economia local, informação e persistência. O projeto completo descrito no documento ainda está parcialmente implementado. Vários sistemas possuem dados iniciais, mas não possuem os comportamentos que deveriam transformar o mundo ao longo do tempo.

A **reposição profissional de NPCs está ausente**. É uma das lacunas com maior impacto na continuidade: uma cidade pode manter milhares de habitantes contabilizados e perder todos os profissionais individualmente simulados. Implementar essa reposição pode recuperar funções comuns da cidade; não substitui a correção da sobrevivência, não resolve sozinho os bloqueios econômicos e não recria famílias reais.

Este relatório compara o documento original, o texto posterior de correções e o código atual. Não altera o motor, a população ou os saves. Os impactos de sistemas ausentes são **projeções de funcionamento**, não resultados de testes desses sistemas.

## 1. Como interpretar os estados

| Estado | Significado |
| --- | --- |
| Implementado no nível do MVP | Há execução concreta da funcionalidade básica, mesmo que a visão completa seja maior. |
| Parcial | Parte funciona, mas faltam comportamentos relevantes previstos no documento. |
| Apenas dados/base | Existem campos ou entidades, com pouca ou nenhuma execução do comportamento proposto. |
| Ausente | Não existe uma implementação funcional no motor atual. |

Um campo `religion` não equivale a religião organizada; um valor `military` não equivale a exército; uma relação `diplomacia` não equivale a negociação. Da mesma forma, a presença de uma família não significa que seus membros cuidem uns dos outros ou tenham descendentes durante a campanha.

A seção **60 — Escopo do Primeiro MVP** afirma que a primeira versão não deve implementar todos os sistemas. Assim, ausência de guerras ou deuses é uma etapa de expansão prevista. A reposição profissional tem outra origem: foi explicitamente pedida no texto posterior de correções, mas ficou adiada pela sua instrução de alterar a população abstrata depois.

## 2. O que foi colocado do escopo do primeiro MVP

Todos os 21 componentes listados na seção 60 possuem alguma implementação. A tabela mostra a profundidade efetiva, sem considerar cada componente como um sistema completo do projeto final.

| Componente do MVP | Estado atual | O que realmente acontece |
| --- | --- | --- |
| Seed determinística | Implementado no nível do MVP | Nome e versão das regras determinam o RNG; seu estado é salvo. |
| Mapa procedural | Implementado no nível do MVP | Mundo 500×500, até seis reinos, cidades, vilas, biomas e interiores. Estruturas essenciais seguem modelos recorrentes. |
| Movimentação em matriz | Implementado no nível do MVP | Jogador se move nos quatro sentidos e entra/sai de mapas; NPCs encontram caminhos dentro do próprio mapa. |
| NPCs | Implementado no nível do MVP | Personagens persistentes com posição, profissão, personalidade, recursos, decisões e morte. |
| Entity IDs | Implementado no nível do MVP | Entidades e eventos usam IDs estáveis; nomes repetidos não são identificadores. |
| Personalidade | Implementado no nível do MVP | Oito traços armazenados; parte deles pesa em decisões e interpretação social. Não há toda a variedade emocional da visão completa. |
| Necessidades | Implementado no nível do MVP | Fome, sede, descanso, dinheiro, trabalho e segurança; escassez alimentar também afeta cidades/reinos. |
| Prioridades | Implementado no nível do MVP | Urgência, duração, perigo e traços alteram qual pressão será atendida. |
| Objetivos | Implementado no nível do MVP | Alternativas competem por pontuação; objetivo pode viajar, executar, falhar e tentar outra solução. |
| Profissões básicas | Implementado no nível do MVP | Produção, conversão de materiais, salários, serviços e resposta de guardas a roubos. |
| Relacionamentos | Parcial | Grafo com casamento, parentesco, amizade, confiança, lealdade e diplomacia. Confiança/familiaridade mudam; a vida familiar dinâmica é limitada. |
| Memória básica | Implementado no nível do MVP | Memórias individuais limitadas e histórico separado; registro persistente evita repetir o efeito social do mesmo fato. |
| Conhecimento | Implementado no nível do MVP | Percepção local, fonte, confiança e transmissão por contatos. Há restrições e bugs conhecidos, descritos abaixo. |
| Itens | Implementado no nível do MVP | Recursos e armas/ferramentas com IDs, dono, qualidade, raridade, criador e origem. |
| Inventário | Implementado no nível do MVP | Posse, quantidades, pilhas, transferência, consumo e compra/venda. |
| Economia básica | Implementado no nível do MVP | Estoque finito, produção, consumo, salários, preços por escassez e subsídios limitados. |
| Facções simples | Apenas dados/base | Duas facções menores são geradas com líder e sede; não executam uma agenda coletiva de recrutamento, expansão ou conflito. |
| Reinos simples | Parcial | Territórios, localidades, família real, sucessão, tesouro e estados separados; respostas econômicas básicas. |
| Event Bus | Implementado no nível do MVP | Ações publicam eventos que alimentam conhecimento, reputação e sucessão. |
| Save e Load | Implementado no nível do MVP | JSON versionado guarda mundo e RNG; continuação determinística e validação estão cobertas por testes. |
| Interface textual | Implementado no nível do MVP | Terminal em português, mapa 5×5, consultas, interação, comércio e ações de sobrevivência. |

O ciclo **necessidade → prioridade → solução → objetivo → ação → consequência** existe. Isso permite NPCs agirem enquanto o jogador espera. O funcionamento prolongado ainda apresenta problemas: ter o ciclo não garante que economia, sobrevivência e sociedade se mantenham viáveis por milhares de horas.

## 3. Mundo, deslocamento e população

| Sistema previsto | Estado | O que existe / o que falta | Impacto esperado ao completar |
| --- | --- | --- | --- |
| Seed narrativa e história anterior à campanha | Parcial | A seed corresponde a um personagem persistente; há fundações e 24 horas iniciais de simulação na configuração padrão. Falta o personagem primordial desencadear uma história com guerras, destruição e remanescentes. | A campanha poderia começar em mundos marcados por acontecimentos anteriores, com relações e ruínas explicáveis pela história. |
| Geografia procedural e diferentes escalas | Parcial | Há mapa global, cidades, vilas, cavernas, castelos e sedes. Não há toda a diversidade de estruturas, usos e conteúdo desses lugares. | Explorar teria mais consequências e oportunidades, além da mudança de cenário e posição. |
| Biomas com influência na simulação | Parcial | Quatro terrenos são gerados; deserto aumenta a sede. Produção, vestuário e cultura não dependem profundamente do bioma. | Regiões passariam a exigir estratégias e cadeias de recursos diferentes. |
| Viagens autônomas entre cidades | Ausente para a IA atual | Jogador transita entre mapas. Caminhos e soluções dos NPCs ficam no mesmo mapa; não há planejamento de viagem entre localidades. | NPCs poderiam buscar recursos, mudar de cidade, transportar notícias e realizar objetivos distantes. |
| Rotas, caravanas e transporte | Ausente | Preços regionais existem, mas comerciantes não redistribuem automaticamente estoques entre cidades. | Excedente de uma vila poderia aliviar escassez de outra, com custo e demora; também abriria espaço para escoltas e bloqueios. |
| População abstrata | Parcial | Participa de consumo diário, renda e mobilização rural para produzir trigo. Não tem demografia completa nem materialização. | O total populacional passaria a influenciar capacidade de trabalho, disponibilidade de novos indivíduos e recuperação local de forma mais coerente. |
| Reposição de profissões essenciais | Ausente; adiada | Não há avaliação de vagas nem criação de trabalhadores a partir da população abstrata. | Evitaria que a morte de poucos NPCs eliminasse permanentemente funções básicas de localidades populosas. |
| Mudança de profissão e recrutamento | Ausente | Profissão é atribuída na geração; não há carreira, conversão de trabalhadores em soldados ou escolha de nova ocupação. | NPCs poderiam responder à falta de renda, às vagas e às crises. Recrutamento criaria custo real de mão de obra civil. |
| Nascimento, envelhecimento e mortalidade abstrata | Ausente | NPCs têm morte por privação, mas não idade, nascimento ou crescimento populacional. A população nominal das cidades não acompanha essas mortes. | Famílias e população poderiam persistir por gerações; perdas e recuperação deixariam de depender apenas do elenco inicial. |
| Níveis de simulação | Parcial | Decisões ocorrem em intervalos de 1, 3 ou 6 horas, conforme categoria/proximidade/urgência; fisiologia continua por hora. Não há resumo completo de atividades distantes. | Permitiria aumentar o elenco com custo controlado e conservar consequências de personagens distantes. |

O tempo básico também funciona: cada turno representa uma hora, há dia/hora na interface e horário de trabalho. Isso não constitui um calendário completo com envelhecimento, estações ou acontecimentos sazonais.

### Reposição profissional: como mudaria o jogo

**Hoje:** os trabalhadores são criados na geração. Se o cozinheiro morre, a localidade não procura outro. A produção de trigo da população abstrata não substitui automaticamente a conversão de trigo em comida feita pelo cozinheiro.

**Exemplo real deste save:** Karmir termina com população nominal **2.994**, os **11 NPCs fisicamente no mapa mortos**, **240 unidades de trigo** e **zero comida**. A cidade continua contabilizando habitantes, mas perdeu a mão de obra individual que executava suas atividades. Personagens vinculados à cidade em sedes externas não corrigem esse vazio local.

**Com reposição funcional**, uma sequência possível seria:

1. A cidade identifica que falta capacidade de cozinhar.
2. Verifica população disponível, estrutura, matéria-prima e demanda pela função.
3. Um habitante abstrato se torna um NPC persistente, com identidade própria.
4. Ele pode trabalhar, transformar trigo em comida e receber salário.
5. Comida e dinheiro circulam; disponibilidade, preços e necessidades mudam.

Esse resultado depende de o novo profissional conseguir se deslocar, sobreviver e trabalhar. **Criar o NPC não garante recuperação econômica.** A reposição de agricultores sem cozinheiros pode apenas aumentar trigo; criar comerciantes sem transporte não faz surgir comércio entre cidades.

O texto de correções pede demanda baseada em **população, economia, estruturas e necessidades locais**, e não uma quantidade fixa igual para todas as cidades. Também restringe reposição a funções comuns: reis, líderes, lendários e personagens com vínculos persistentes importantes não devem ser tratados como peças intercambiáveis.

Portanto, o novo cozinheiro não deveria ser uma cópia do morto, com suas memórias e relações. A vaga profissional pode ser ocupada; a morte do indivíduo deve continuar tendo consequências. E a extinção dos Corven não seria resolvida criando um novo trabalhador comum.

**Contabilidade populacional a definir:** hoje `Town.population` é o total nominal, e a parcela abstrata é calculada como `population - len(resident_ids)`. A lista inclui moradores mortos. Não há um contador independente e completo de habitantes abstratos vivos. Se o total representa abstratos + indivíduos, materializar uma pessoa é mover alguém de um grupo ao outro, não necessariamente reduzir o total. Reduzir o total e também aumentar a lista de residentes poderia descontar a mesma pessoa duas vezes. A alteração populacional que você pretende propor precisa esclarecer essas regras.

**Também precisa de limite e tempo:** geração contínua de trabalhadores sem consumir capacidade populacional transformaria mortes em reposição infinita. Reposição instantânea apagaria escassez e consequências. O objetivo previsto é manter capacidade funcional quando houver condições, com perdas ainda relevantes.

## 4. NPCs, vínculos e histórias pessoais

| Sistema previsto | Estado | O que existe / o que falta | Impacto esperado ao completar |
| --- | --- | --- | --- |
| Personalidade influenciando ações | Parcial | Honestidade, ganância, coragem, independência, compaixão e diligência afetam escolhas. Persistência participa da reação à recusa; lealdade familiar não gera uma rotina de cuidado. Não há todo o modelo de ira, cinismo ou emoções citado no documento. | Personagens teriam motivações mais variadas; o mesmo problema poderia gerar negociação, confronto, espera ou manipulação. |
| Necessidades pessoais além da sobrevivência | Ausente em grande parte | Segurança de guardas existe, mas não busca de familiar, vingança, fé, ambição, status, poder ou proteção de residência como objetivos executáveis. | Abriria histórias com conflito e continuidade mesmo quando há comida disponível. |
| Família e relacionamentos dinâmicos | Parcial | Casamentos, parentesco e sobrenomes são gerados. Falta desenvolvimento de cuidado, desaparecimento percebido, luto, separação e decisões familiares. | Vínculos passariam a gerar ações: procurar alguém, ajudar parentes ou reagir a perdas. |
| Hereditariedade, descendência e herança | Ausente | A família real inicial permite sucessão, mas não há novos descendentes, transmissão de patrimônio ou herança de características/reputação. | Sustentaria dinastias e histórias familiares longas, com conflitos entre gerações. |
| Memória e crenças complexas | Parcial | Fatos possuem origem/confiança e efeitos deduplicados. Não há construção completa de suspeitas, versões conflitantes, investigação ou revisão por novas interpretações. | NPCs poderiam agir sobre hipóteses e corrigir crenças, produzindo mistérios e consequências sociais mais variadas. |
| Rumores falsos, mentira e propaganda | Ausente | A transmissão atual compartilha fatos do motor, reduzindo certeza; não fabrica versões falsas deliberadamente. | Informações passariam a ser disputadas; confiança na fonte e investigação teriam maior valor. |
| Quests emergentes variadas | Parcial | Pedidos de comida surgem de necessidade real, inclusive por iniciativa do NPC. Não há execução de resgates, investigação, recuperação de artefato, vingança ou conquista. | As quests deixariam de repetir principalmente entrega de alimento e envolveriam diferentes sistemas do mundo. |
| Diálogo contextual e vozes individuais | Parcial | Apresentação, necessidade, objetivo, rumor e alguns sinais de reputação compõem frases por regras. Personalidade e vínculo não geram uma voz narrativa rica. | O jogador perceberia melhor gratidão, medo, ressentimento, relações e mudanças de objetivo. |
| IA generativa para texto/lore | Ausente; integração posterior prevista | Motor funciona sem modelos generativos. Não existe integração que redija diálogos ou crônicas durante o jogo. | Poderia apresentar os fatos de forma mais natural; não criaria, sozinha, família dinâmica, guerras ou decisões ausentes no motor. |
| Ascensão a importante/lendário por feitos | Ausente como evolução | Categorias existem e afetam frequência de decisão/itens iniciais. Não há promoção ou perda de categoria durante a campanha. | Um NPC comum poderia ganhar relevância histórica por suas ações, em vez de depender da classificação inicial. |

**Evidência da limitação narrativa:** das 95 quests registradas na campanha, todas pedem alimento: 85 de Marie Arven, nove de Iria Arven e uma de Mira Corven. Reposição profissional ajuda a manter pessoas e serviços disponíveis, mas não cria novos tipos de desejo ou quest. Para diversificar histórias, ela precisa ser acompanhada de novas necessidades e ações.

## 5. Economia, profissões, itens e criminalidade

| Sistema previsto | Estado | O que existe / o que falta | Impacto esperado ao completar |
| --- | --- | --- | --- |
| Produção e consumo | Parcial | Agricultura, cozinha, mineração, madeira, caça simplificada e ferraria alteram estoque. Caça não procura animais; a maioria das atividades usa locais e recursos simplificados. | Profissões teriam cadeias e riscos próprios, criando dependências e oportunidades mais distintas. |
| Variedade profissional | Parcial | Oito profissões comuns são geradas; governantes, conselheiros e estudantes também existem. Soldado tem ramo de serviço, mas não é gerado como força militar. Pescador, curandeiro, sacerdote e artesão não têm atividades próprias. | Novas funções poderiam sustentar saúde, religião, materiais e guerra, desde que suas ações existam. |
| Mercado e comércio local | Implementado no nível do MVP | Comprar/vender transfere bens e dinheiro reais; escassez altera preço, com margens e cálculo por unidade. | A base já sustenta consequências materiais; sua expansão depende de novos participantes e circulação. |
| Comércio entre localidades | Ausente para os NPCs | Não há caravanas, transporte, rotas ativas, bloqueios ou compra/revenda autônoma regional. O jogador pode viajar e negociar nos mercados. | Produção de uma região passaria a abastecer outra; crises poderiam se espalhar ou ser mitigadas. |
| Negociação e preços sociais | Ausente | Preço depende principalmente de tipo, estoque e população; não muda pela personalidade do vendedor ou relação com o comprador. | Confiança e ganância afetariam acordos; reputação teria consequência econômica direta. |
| Demanda econômica detalhada | Apenas dados/base | Existe `town.demand` na fórmula, mas não há atualização que gere demanda ativa pelas ações atuais. Guerra, distância e equipamento não alimentam uma cadeia completa de preços. | Necessidades de armas, materiais ou alimentos poderiam pressionar setores específicos. |
| Trabalho adaptável e acesso à renda | Parcial | Salários e materiais são reais, mas estoque cheio pode bloquear produção e remuneração. Não há mercado de vagas ou resposta profissional à perda de renda. | Evitaria que excedente de mercadoria deixasse trabalhadores sem alternativas para comprar comida; afetaria pedidos e crimes. |
| Itens procedurais e histórico | Parcial | Qualidade/raridade variam, com influência da categoria do proprietário. Tipos/nome são limitados; história de feitos não transforma a importância do item. Pilhas não preservam toda a proveniência por unidade. | Objetos poderiam adquirir identidade e valor histórico, gerando reconhecimento e quests de recuperação. |
| Equipamento utilizável | Ausente | Armas e ferramentas existem no inventário, mas não há slots, armadura, escudo, durabilidade ou efeitos de equipamento em combate. | Escolha de equipamento passaria a afetar sobrevivência, força e reconhecimento social. |
| Ações completas do inventário | Parcial | Adicionar, remover, consumir, transferir, entregar, comprar e vender funcionam. Equipar/desequipar, abandonar no chão e pegar do corpo não estão disponíveis. | Bens poderiam circular também por exploração, perda, recuperação e morte. |
| Loot de corpos e herança de objetos | Ausente como interação | Itens permanecem com personagens mortos; não há comando para saquear cadáver nem distribuição por herança. | A morte faria bens circularem, com oportunidades e consequências de posse. |
| Crime e resposta local | Parcial | Roubo de comida gera conhecimento/reputação; guardas investigam local conhecido e cobram até cinco moedas. Não há prisão, confisco, processo ou perseguição complexa. | Crimes teriam custos e trajetórias mais variados, além da multa e repetição do roubo. |
| Recompensas e caça a criminosos | Ausente | Não há recompensa criada por facções nem objetivos de mercenários para caçar alvos. | Crimes do jogador e NPCs poderiam atrair perseguidores e gerar conflitos persistentes. |

O serviço de um guarda contabiliza patrulha e remuneração, mas não percorre uma rota de ronda territorial. A investigação de um roubo conhecido pode gerar deslocamento ao local do fato. São comportamentos diferentes.

**Exemplo de impacto limitado da reposição:** Dorven termina com 239 unidades de comida e 240 de trigo. Marie tem zero moedas e Iria uma; comida custa duas. Mais trabalhadores, por si só, não garantiriam acesso à comida: o agricultor está sujeito ao teto de trigo, e o cozinheiro precisa de espaço para produzir um lote de três rações. A guarda pode receber por serviço sem produzir mercadoria. Esse problema exige também revisar disponibilidade de trabalho e renda.

## 6. Reinos, facções, guerra, religião e deuses

| Sistema previsto | Estado | O que existe / o que falta | Impacto esperado ao completar |
| --- | --- | --- | --- |
| Reinos territoriais | Parcial | Território inicial, cidades, vilas, capital, cultura, religião, tesouro e família real existem. Não há mudanças territoriais ou estrutura administrativa completa. | Territórios passariam a ser resultado da história, com localidades mudando de controle. |
| Destruição de localidades e ruínas dinâmicas | Ausente | Castelos abandonados são gerados como pontos de interesse. Cidades não são destruídas, convertidas em ruínas ou reconstruídas por acontecimentos da campanha. | Guerras e calamidades poderiam alterar o mapa, deslocar habitantes e deixar remanescentes históricos. |
| Sucessão simples | Implementado no nível do MVP | Na morte do governante, escolhe familiar vivo; sem familiar, registra crise sucessória. | A base já muda liderança de forma persistente. |
| Política e decisões do governante | Parcial | Sucessão funciona. Falta personalidade do rei controlando alternativas coletivas, impostos, rebelião, golpe e negociação. Sucessor não recebe uma nova profissão/rotina automaticamente. | Reis diferentes poderiam governar de formas diferentes e criar consequências para habitantes e vizinhos. |
| Recuperação após extinção dinástica | Ausente | Sem familiar vivo, o reino fica em crise. Não há pretendentes, eleição, nova casa, tomada de poder ou anexação como soluções. | O fim da família abriria disputa política em vez de encerrar a evolução da liderança. |
| Necessidades coletivas amplas | Parcial | Cidades/reinos respondem à falta de alimento com produção de trigo e subsídio. Não há seleção coletiva completa entre comércio, diplomacia, recrutamento ou conquista. Famílias/facções não têm motor equivalente. | A escassez poderia gerar acordos, reformas, conflitos e novas quests em múltiplas escalas. |
| Facções com agenda própria | Apenas dados/base | Nome, líder, sede e filiação existem. Faltam membros organizados, recursos coletivos, recrutamento e objetivos da organização. | Companhias e irmandades poderiam agir independentemente dos interesses pessoais de um único líder. |
| Diplomacia dinâmica | Apenas dados/base | Relações iniciais positivas/negativas estão no grafo e podem contextualizar interpretação social. Não há negociação, tratados ou evolução diplomática por acontecimentos. | Relações teriam consequências em abastecimento, alianças, conflitos e acesso a territórios. |
| Exércitos e guerra | Ausente | Há número de força militar e estado `paz`; não há exército, mobilização, poder por destacamento, batalhas, ocupação ou paz negociada. | Produziria perdas territoriais, recrutamento, escassez, deslocamentos e histórias de escala maior. |
| Combate por partes do corpo | Ausente | Vida geral e dano por privação existem. Não há atacar, defesa, membros, ferimentos localizados ou combate entre NPCs. | Permitiria confrontos com desfechos distintos, mutilação, incapacitação e morte por combate. |
| Ferimentos e condições | Ausente além de privação | Não há sistema de doenças, lesões, tratamento, curandeiros ou consequências por região do corpo. | Sobrevivência envolveria recuperação e ajuda médica, gerando novos objetivos e dependências. |
| Cultura dinâmica | Apenas dados/base | Rótulo cultural sorteado; personalidade não é formada pela soma de família real, bioma e história do reino. | Guerras e escolhas políticas poderiam mudar costumes e preferências ao longo da campanha. |
| Fé influenciando decisões | Apenas dados/base | Religião e devoção são campos separados. Devoção não participa das decisões atuais. | Um devoto poderia priorizar obrigação religiosa e interpretar fatos por seus valores. |
| Religião organizada | Ausente | Cultos têm nomes, mas não há entidade religiosa, hierarquia, padre, clero, penitentes ou perseguição de hereges. | Religiões passariam a ter recursos, conflitos, líderes e objetivos próprios. |
| Deuses | Ausente | Não existem entidades divinas, domínios, seguidores, desejos, memória divina, contratos ou intervenções. Categoria `lendário` não cria um deus. | Abriria histórias de campeões, rivalidades, bênçãos, maldições e artefatos, com consequências persistentes. |
| Rituais e invocação | Ausente | Não há execução do ritual descrito, custos, contrato ou manifestação. | O jogador poderia participar de ações religiosas materiais, com efeitos definidos pelo motor. |

**Evidência neste save:** as seis dinastias se extinguem até o turno 1.573. As 8.451 horas restantes terminam sem governante em nenhum reino. Reposição de funções comuns não preencheria esse vazio político. Também não houve guerra ou ação divina: os sistemas que produziriam esses acontecimentos ainda não existem.

O interpretador social contém uma regra para `CharacterKilled`, inclusive diferenças por filiação e relações. Isso é uma base para futuras mortes violentas; **o motor não possui atualmente combate que produza esse acontecimento durante uma partida normal**. Um teste que injeta um evento não significa que o sistema causador desse evento foi implementado.

## 7. Reputação, história e infraestrutura

| Sistema previsto | Estado | O que existe / o que falta | Impacto esperado ao completar |
| --- | --- | --- | --- |
| Reputação contextual e confiança | Parcial | Ajuda, roubo, recusa e interpretação de morte violenta têm regras; fonte e personalidade mudam efeitos. Reputação altera pedidos e disposição de dar comida. | Mais tipos de feitos poderiam influenciar proteção, abrigo, atendimento, negociação e decisões coletivas. |
| Reputação coletiva/facções | Ausente como sistema completo | Reputações são principalmente opiniões de personagens; não há agregação institucional com políticas próprias. | A notícia de um crime ou favor poderia alterar a postura de uma organização inteira, com alcance definido. |
| Decaimento e herança de reputação | Ausente | Memória curta descarta fatos, mas isso não equivale a decair os rótulos acumulados. Familiares não recebem reputação por associação. | Pequenos feitos poderiam perder peso; feitos históricos poderiam afetar gerações de forma contextual. |
| Títulos e apelidos | Parcial | Há `Desconhecido` e uma regra de `Protetor de [local]` após três pedidos concluídos. Não há variedade ampla por feitos. | A identidade pública passaria a refletir conquistas, crimes, funções e histórias diversas. |
| História procedural persistente | Parcial | Fundações, mortes por privação e sucessões são registradas. Eventos cotidianos têm retenção curta; faltam os acontecimentos cujos sistemas estão ausentes. | Novos sistemas ampliariam a crônica; seleção de fatos relevantes ajudaria a preservar arcos longos. |
| Arquitetura modular e eventos | Implementado no nível do MVP | Regras são separadas em serviços; o motor coordena sem depender da interface. | A base permite adicionar ações e consequências sem entregar regras à interface ou ao gerador de texto. |
| Persistência e compatibilidade | Implementado no nível do MVP | Save inclui o estado atual e RNG; `mvp-1` é recusado pela versão atual. Não há migração geral entre formatos/regras. | Novas entidades e regras exigirão definir migração ou incompatibilidade explícita, especialmente para continuar saves existentes. |
| Testes e observabilidade | Implementado no nível do MVP | Há 43 testes existentes, campanhas longas e reprodução de bugs. Debug explica a última decisão. Não há cobertura de sistemas ausentes. | Novos sistemas precisarão provar seus comportamentos e consequências, não apenas a presença de campos. |

## 8. O que já foi corrigido e o que continua pendente

O texto posterior de correções produziu alterações concretas: descanso limitado pela privação; compra/venda sem lucro circular no mesmo mercado; separação dos estados do reino; deduplicação de efeitos sociais por fato; pesos de confiabilidade; confiança baseada em ajuda relevante; pedidos autônomos ao jogador; efeito social da recusa; múltiplas soluções para fome; pontuação de alternativas e debug.

**A reposição populacional/profissional não foi feita**, conforme registrado no relatório de correções. Além disso, a auditoria posterior encontrou problemas que continuam no código atual:

| Pendência | Categoria | Por que importa para os próximos sistemas |
| --- | --- | --- |
| NPC pode morrer antes de decidir comer, enquanto jogador come antes do tick | Bug confirmado | Repor trabalhadores sem corrigir a ordem de sobrevivência pode repetir mortes evitáveis nos novos NPCs. |
| Dez moedas bloqueiam pedido de comida mesmo quando o preço é maior | Bug confirmado | Capacidade real de resolver a necessidade deve ser consistente entre escolha e execução. |
| Rumor mais forte é excluído quando o fato já é conhecido | Bug confirmado | Investigações e reputação ampliada dependeriam de atualização coerente das evidências. |
| Ação inválida pode criar necessidade e consumir um ID | Bug confirmado | Novas ações precisam separar tentativa de execução e efeitos persistentes. |
| Estoque cheio bloqueia produção e salário de certas profissões | Limitação econômica | Reposição sozinha não cria trabalho viável nem distribui acesso a comida. |
| Família real inteira pode morrer e o reino não encontra outra solução | Sistema ausente após a sucessão básica | Profissionais comuns novos não sustentam a continuidade política. |
| Rótulos sociais opostos chegam ao teto e achatam a interpretação | Limitação do modelo | Mais acontecimentos podem aumentar saturação sem aumentar profundidade. |
| Reações remotas e conclusão do pedido pela entrega | Decisões de modelo/inconsistências a revisar | Comunicação e critério de sucesso ficam mais relevantes em viagens, investigações e missões longas. |

Os 43 testes aprovados demonstram os comportamentos cobertos por eles; não eliminam os bugs encontrados pela campanha posterior. Este comparativo não executou uma nova simulação ou uma nova rodada de testes.

## 9. Qual expansão teria maior impacto agora

Esta é uma sugestão de priorização baseada nas evidências. Algumas frentes podem ser desenvolvidas independentemente, desde que suas dependências estejam atendidas.

| Frente | Principal efeito no jogo | Dependência ou limite |
| --- | --- | --- |
| Correções de sobrevivência e coerência de ações | Tornar perdas e soluções mais confiáveis. | Base para avaliar se um novo sistema melhora a simulação. |
| Sua revisão da população + reposição profissional | Manter cidades funcionalmente ativas e criar novos indivíduos comuns. | Precisa definir contagem, capacidade, demora e limites de reposição. |
| Trabalho adaptável + deslocamento/comércio entre localidades | Dar saída para falta de renda e conectar excedentes a escassez. | Exige viagem, informação e transporte reais. |
| Necessidades familiares e pessoais + quests correspondentes | Aumentar variedade e continuidade das histórias de NPCs. | Cada necessidade precisa de soluções executáveis e percepção coerente. |
| Governo, diplomacia e continuidade política | Transformar crises em negociações, disputas e mudanças de liderança. | Não pode depender apenas da lista inicial de três familiares. |
| Equipamentos, combate, recrutamento e guerra | Criar confrontos e consequências militares materiais. | Deve integrar perdas, produção, população e objetivos. |
| Religião organizada e deuses | Acrescentar conflitos e histórias religiosas próprias. | Precisa de entidades, necessidades, custos e consequências, além de nomes e texto. |
| Diálogo e crônicas mais expressivos | Tornar as histórias existentes perceptíveis ao jogador. | Deve narrar o estado produzido pelo motor e respeitar o conhecimento do interlocutor. |

A reposição profissional tem **alto impacto na duração e na funcionalidade** do mundo. Necessidades familiares, agendas políticas e religião têm **alto impacto na variedade das histórias**. Texto melhor tem impacto na apresentação. São melhorias diferentes, que podem se apoiar, mas não substituem umas às outras.

Não há estimativa confiável de quantos NPCs seriam salvos, quanto os preços cairiam ou quantas histórias novas surgiriam: esses números dependem das regras que ainda serão definidas e testadas. Adicionar mais entidades também aumenta processamento e tamanho do save. A expansão precisa preservar IDs, RNG controlado, percepção local e consequências materiais.

## 10. Fontes verificadas

### Especificação

- [Documento original — visão geral](</home/hugo/Área de trabalho/procedrual/instruction.md:1>)
- [Escopo do primeiro MVP](</home/hugo/Área de trabalho/procedrual/instruction.md:5930>)
- [Profissões e mudança de ocupação](</home/hugo/Área de trabalho/procedrual/instruction.md:3459>)
- [População abstrata e materialização](</home/hugo/Área de trabalho/procedrual/instruction.md:5547>)
- [Política, diplomacia e guerra](</home/hugo/Área de trabalho/procedrual/instruction.md:2539>)
- [Religião e deuses](</home/hugo/Área de trabalho/procedrual/instruction.md:2634>)
- [Texto posterior de correções — reposição profissional](</home/hugo/.codex/attachments/811381bc-7dd0-4453-aa80-40793355ffc0/Texto colado.txt:243>)

### Implementação

- [Dados das entidades](</home/hugo/Área de trabalho/procedrual/procedural/models.py>)
- [Geração do mundo e elenco inicial](</home/hugo/Área de trabalho/procedrual/procedural/generation.py:85>)
- [Relógio, morte e frequência de decisão](</home/hugo/Área de trabalho/procedrual/procedural/engine.py:59>)
- [Necessidades](</home/hugo/Área de trabalho/procedrual/procedural/needs.py>)
- [Alternativas e execução de objetivos](</home/hugo/Área de trabalho/procedrual/procedural/goals.py:30>)
- [Produção profissional](</home/hugo/Área de trabalho/procedrual/procedural/professions.py:26>)
- [Economia local e população abstrata](</home/hugo/Área de trabalho/procedrual/procedural/economy.py:88>)
- [Sucessão política](</home/hugo/Área de trabalho/procedrual/procedural/politics.py:8>)
- [Conhecimento, rumor e diálogo](</home/hugo/Área de trabalho/procedrual/procedural/knowledge.py>)
- [Interpretação social](</home/hugo/Área de trabalho/procedrual/procedural/social.py:53>)
- [Quests e título local](</home/hugo/Área de trabalho/procedrual/procedural/quests.py>)
- [Itens e inventários](</home/hugo/Área de trabalho/procedrual/procedural/items.py>)
- [Persistência](</home/hugo/Área de trabalho/procedrual/procedural/persistence.py>)

### Evidências anteriores

- [Relatório das correções e adiamento populacional](</home/hugo/Área de trabalho/procedrual/RELATORIO_HARDENING.md>)
- [Auditoria de 10.000 turnos e bugs](</home/hugo/Área de trabalho/procedrual/reports/auditoria_jogador_10000/RELATORIO.md>)
- [Histórias e comportamento dos NPCs](</home/hugo/Área de trabalho/procedrual/reports/auditoria_jogador_10000/HISTORIAS_E_NPCS.md>)
- [Dados extraídos do save](</home/hugo/Área de trabalho/procedrual/reports/auditoria_jogador_10000/evidencias_historias.json>)

**Síntese do estado atual:** existe um simulador funcional de sobrevivência, produção local, interação social básica e sucessão. Para chegar à visão completa, faltam principalmente renovação populacional/profissional, circulação entre localidades, relações que gerem novos objetivos, continuidade política e os sistemas militares e religiosos. Essas ausências explicam boa parte da repetição e dos vazios observados nas histórias do save.
