# Fase 5 — implementação, evidências e limites

Base recebida: `mvp-7-fase4.6`. Entrega: **`mvp-8-fase5`**, Python, interface de terminal. O documento enviado foi preservado integralmente em [fase_5.md](</home/hugo/Área de trabalho/procedrual/fase_5.md>). A geração continua identificada como `mvp-4`; a mudança de versão refere-se às regras e ao formato compatível de campanha.

Foram acrescentados organização coletiva, administração municipal, hierarquia militar local, facções com estrutura, fé executável, entidades divinas objetivas, fama por conhecimento, potencial mítico, história de itens e decisões terminais de combate. A implementação amplia os mecanismos que podem produzir histórias; a existência de código e testes não demonstra que todos esses arcos ocorreram espontaneamente.

## Arquitetura e preservação

As novas escolhas usam a sequência existente **Need → Priority → Solution/Utility → Goal**, com compromissos, aspirações, conhecimento subjetivo e o RNG do mundo. Não existe um gerador de sagas, uma meta de acontecimentos épicos nem uma rotina que obriga NPCs a guerrear, matar deuses ou se tornar lendários.

Os módulos centrais novos são [society.py](</home/hugo/Área de trabalho/procedrual/procedural/society.py>), [faith.py](</home/hugo/Área de trabalho/procedrual/procedural/faith.py>), [renown.py](</home/hugo/Área de trabalho/procedrual/procedural/renown.py>) e [terminal_combat.py](</home/hugo/Área de trabalho/procedrual/procedural/terminal_combat.py>). Foram integrados a modelos, necessidades, decisões, agência, conhecimento, itens, conflitos, persistência, validação e comandos do motor.

Os personagens dos cargos são pessoas existentes. Prefeitos são escolhidos entre moradores comuns disponíveis; os guardas recebem a cadeia local General → Captain → Lieutenant → Sergeant → Soldier. O patrulhamento fora do mapa não remove uma patente. Não foram acrescentados milhares de NPCs para preencher cargos, nem recursos gratuitos para sustentar organizações.

A base anterior foi copiada para `reports/fase_5/baseline_code/procedural`. A comparação de geração com a mesma seed, `Fase5-preservacao`, preservou mapas, personagens/traços, população e itens/estoques: 81 personagens, 14 localidades e 227 itens, nos quatro conjuntos comparados. Isso comprova preservação da geração física examinada, não identidade da trajetória posterior: novas escolhas consomem RNG e mudam o mundo.

As regras anteriores de alimentação, recuperação, economia, investigação e relações continuam ativas. A potência e a rolagem ordinária de combate continuam sendo usadas. Há modificadores físicos limitados para potencial mítico desenvolvido e proteção divina temporária, além do novo encerramento terminal sem rolagem de dano. Portanto, a regra física não é inteiramente idêntica em todos os casos excepcionais.

Saves antigos continuam vinculados às versões de motor correspondentes; o carregamento rejeita versões incompatíveis. **Não há migração automática de saves da Fase 4.6.** A campanha de auditoria foi criada do zero, sem jogador, sem save anterior e sem aquecimento histórico.

## O que existe, o que é parcial e o que ficou fora

| Partes do documento | Entrega concreta | Limite |
|---|---|---|
| 3–4, 82, 87–90: poder local e representação | Prefeito, sucessão por vacância, apoio, personalidade, representação e pedido presencial de auxílio real | Administração simples das cidades. Vilas não têm prefeito nem encaminhamento de demandas à cidade. Não há eleição complexa, carreira política completa ou disputa nacional. |
| 5–9, 13–17: grupos | Formação por problema comunicado, encontro e afinidade; adesão, liderança, reuniões, pressão, responsabilização, dissolução e grievance coletivo | Nem toda privação produz grupo; nem todo grupo consegue manter encontros. Antagonismo não dispara ataque obrigatório. |
| 10–12: propostas | Escolhas concorrentes, entrega à autoridade, aprovação/parcial/recusa/adiamento e efeitos materiais | Conjunto pequeno de soluções. A aprovação não garante que todos os membros serão atendidos. |
| 11: consequência política real | Distribuição de estoque, serviço temporário existente, pagamento/armamento de guardas e política local de culto | Comida, dinheiro, ferro e madeira saem de recursos existentes. Não há orçamento macroeconômico completo. |
| 13–14, 80–83: resposta e conhecimento coletivo | Grupo conserva Need, Goal, Commitment e conhecimento recebido; representante consulta respostas públicas presencialmente | O conhecimento do grupo não se converte integralmente em conhecimento de cada membro. A resposta ainda depende da comunicação efetiva ao representante. |
| 18–22, 68: facções | Membros, propósito, patentes, recursos, recrutamento, relatórios presenciais, ordens, serviço, promoção, sucessão e deserção | Serviços e propósitos são básicos. Não há contratos complexos nem revisão estratégica completa do propósito. Organizações nativas podem continuar isoladas. |
| 23–26, 69, 89: militares | General único, cadeia local, transmissão de casos conhecidos a subordinados presentes e participação em grupos | Sem exércitos, batalhas militares ou campanhas. Nem todo comando encontra destinatários presentes. |
| 27–37: fé e divindades | Três deuses objetivos com domínio, valores, energia, memória e conhecimento; oração/oferta, interpretação, relato, reavaliação, defesa de culto e intervenção custeada | Panteão inicial usa três modelos culturais. Difusão exige um fato conhecido que sustente a crença; a tradição inicial sozinha não oferece essa solução. A crença não concede certeza ontológica automática; não há um sistema completo de revelação comprovada. |
| 38, 67–70: relações divinas e cruzamentos sociais | Relações divinas registradas; intervenções julgam feitos observados; demandas de culto podem entrar na política e em facções | Diplomacia entre deuses e consequências teológicas extensas são parciais. Não há disputa ativa completa entre panteões. |
| 39–43: morte divina e apoteose | Morte especial, essência com acesso legítimo, reivindicação separada e nova Divinity com domínio ligado ao mortal | A representação do mortal e da nova divindade são separadas. Sincronização completa entre corpo, avatar e vida divina não foi modelada. |
| 43–50: veneração, fama e epítetos | Observadores aprendem feitos; fonte/confiança/repetição alteram renome; podem atribuir epítetos e venerar mortais sem criar deuses | Alcance é classificação do auditor. Não existe fama universal nem disseminação geográfica completa garantida. |
| 51–62: MythicTraits | Heroism, Justice e Coldness raros; afetam utilidade e aspiração; treino custa esforço e pode falhar ou perder prioridade | Quatro potenciais por seed auditada. Bônus físico desenvolvido é limitado; não existe destino reservado ou alinhamento moral objetivo. |
| 63–66, 77: itens históricos | Identidade, antigos donos, fatos importantes, contato divino, propriedades reais e histórias/crenças separadas | Um título não concede buff. Relatos reutilizam história conhecida; não há geração completa de falsas lendas ou catálogo de artefatos mágicos. |
| 71–76: combate terminal | Oportunidade exige incapacidade, presença, capacidade e intenção; escolhas incluem finalizar, poupar, capturar, ajudar e retirar-se | Intenção isolada não mata. A apuração de consequências reutiliza justiça, conhecimento, relações e agência existentes. |
| 74–75: letalidade situacional | Ameaça grave recente, dano/HP, emoções, vínculos, compaixão, medo e autoridades entram na avaliação | Medo isolado e raiva genérica não bastam. As barreiras da letalidade persistente foram preservadas. |
| 78, 92–110: limites e auditoria | Limites explícitos nos novos estados; regressões, microcenários, curta e longa, dados e seleção de histórias reais | O histórico e alguns registros anteriores continuam crescendo. Novos limites não tornam o save inteiro limitado. |
| 2: fora do escopo | Escopo preservado | Guerras continentais, conquista, diplomacia completa, exércitos, revolução nacional, demografia geracional, roteiros épicos e regras por LLM não foram implementados. |

Esses limites devem ser considerados ao comparar a entrega com os exemplos amplos do documento. A presença de peças para um arco não comprova que todas as suas transições estejam frequentes, completas ou equilibradas.

## Como uma reação passa a existir

Um morador precisa ter pressão própria ou informação recebida. Ele pode comunicá-la, tentar organizar pessoas presentes com afinidade ou aderir a um grupo acessível. Reunir membros não cria automaticamente uma facção: a continuidade, o investimento, o propósito, os membros e contribuições materiais precisam existir.

A proposta é criada pelo representante, mas só chega ao prefeito durante um encontro. O prefeito compara respostas pelo contexto, personalidade, urgência, apoio, oposição e recursos. Se aceitar uma distribuição, a comida é transferida do estoque; se armar guardas, os insumos são consumidos e o item é real. Uma recusa remota não informa o grupo: a decisão vira fato público, que precisa ser consultado ou recebido. Reaprender o mesmo fato não aumenta a pressão repetidamente.

Fé funciona de maneira semelhante: oração é uma ação, intervenção é uma escolha separada do deus, e os observadores interpretam o acontecimento conforme sua devoção e conhecimento. Um rumor conserva sua fonte e limite de confiança. Adorar alguém, chamá-lo de “deus” ou atribuir-lhe um epíteto não cria uma entidade divina objetiva.

No combate, a oportunidade terminal não é a execução. O NPC precisa decidir diante de um alvo incapacitado e presente. Uma finalização válida causa morte certa, sem repetir a rolagem comum de dano; poupar preserva a vida e não apaga automaticamente os motivos anteriores.

## Correções durante o desenvolvimento

| Problema encontrado | Correção e evidência |
|---|---|
| Uma regressão antiga de recuperação e duas de letalidade | Atividade religiosa deixou de interromper recuperação fisiológica rápida; barreiras de medo/autoridade da intenção persistente foram preservadas e a via situacional foi restrita a ameaça extrema. A suíte anterior voltou a passar. |
| Renome excedendo 12 sujeitos após reaprender fato de sujeito removido | Verificação de idempotência passou a acontecer antes de criar o registro. A curta parcial foi interrompida; a curta final e seus limites passaram. |
| Propostas sem contato útil com o prefeito | Acrescentado atendimento local com condições físicas próprias, sem dar conhecimento remoto de propostas ao prefeito. Entrega continua presencial. |
| Preparação de viagem de líder de facção sem rota conhecida | Acrescentado destino natal conhecido e deslocamento físico por entrada/saída, preservando residência; aquisição de suprimentos continua sujeita à economia. |
| Grupo consultava o estado remoto da proposta | Acrescentado `proposal_knowledge` próprio e leitura presencial de respostas públicas. Recusa só causa reação após aprendizado e não se repete pelo mesmo fato. |
| Novo alvo coletivo referenciava proposta removida | Alvo do compromisso institucional passou a ser o representante existente; assunto e fonte continuam no contexto. |
| Aspiração de poder fora das suposições antigas da agência | Integrada a categoria nova e limitado progresso da aspiração. |
| Ação antiga de ataque diante de oportunidade terminal | Mantida a compatibilidade dessa ação com o novo encerramento terminal, sem alterar a rolagem dos ataques ordinários. |
| Exportador de auditoria não serializava Fact em estruturas auxiliares | Corrigido o exportador. A execução de 500h com exportação incompleta foi preservada e a curta final foi repetida com o mesmo núcleo. |
| Quem conhecia o culto anterior não registrava hipótese sobre o sucessor após receber a apoteose | Corrigido depois da longa: o fato recebido pode gerar hipótese com confiança limitada, sem certeza ontológica ou conversão automática. Teste 22 ampliado. |
| Oração dirigida ao mortal ascendido não alcançava sua Divinity separada | Encaminhamento pela associação objetiva validada; oração a mortal apenas venerado continua sem entidade divina destinatária. Teste 22 e save/load. |
| Prefeita permanecia ligada à cidade antiga depois de migrar | A revisão diária verifica residência real; viagem temporária conserva cargo. O caso foi observado em Nora Solaris #195 na longa. Teste 29 ampliado. |
| Adesão era oferecida mesmo após atingir três grupos | Candidatos passam a respeitar a capacidade própria conhecida. Isso elimina essa tentativa inviável específica; não resolve outras falhas de encontro, afinidade e lotação. Teste 02 ampliado. |
| Troca de prefeito apagava pedidos formais e respostas públicas | Sucessão conserva registros institucionais limitados e redireciona demandas já recebidas ao novo titular. Não transmite propostas desconhecidas. Teste 29 ampliado. |

As execuções de diagnóstico e os logs com falhas permanecem na pasta. Eles não entram como resultados finais. Não foi escondida uma falha de teste nem substituída uma campanha longa por uma seed mais conveniente.

## Testes e capacidade controlada

A suíte completa passou em **275 testes**, com **30 regressões novas compostas** e os 245 testes anteriores preservados. O log da suíte do código de entrega está em [testes_275_entrega_social_final.txt](</home/hugo/Área de trabalho/procedrual/reports/fase_5/testes_275_entrega_social_final.txt>); os casos novos estão em [test_phase5.py](</home/hugo/Área de trabalho/procedrual/tests/test_phase5.py>). Os logs de validação anteriores permanecem preservados.

Os cenários controlados demonstraram formação/ausência de grupo, entrega e custo de proposta, resposta contextual, oposição sem violência automática, maturação, hierarquia, promoção, conhecimento institucional recebido, fé separada de verdade, rumor, intervenção, veneração mortal, fama, potencial mítico, treino, morte divina, apoteose, finalização e misericórdia. O teste de resposta pública também verifica save/load do conhecimento e dos fatos públicos. Continuação após save/load conserva o RNG nos cenários pequenos examinados.

As condições raras foram ajustadas explicitamente nos testes. **Deus morto, apoteose, veneração e execução em microcenário não contam como acontecimento natural.** A separação está em [MICROCENARIOS_CONTROLADOS.md](</home/hugo/Área de trabalho/procedrual/reports/fase_5/MICROCENARIOS_CONTROLADOS.md>).

## Bugs e limitações que a entrega não esconde

1. **Contato e continuidade continuam sendo gargalos.** É fácil comunicar uma pressão, mas reunir pessoas, manter representantes disponíveis e consultar respostas envolve competição com alimentação, descanso e outras necessidades. Muitas tentativas de organizar ou aderir falham. Na curta do núcleo da longa, 107 de 319 formações ocorreram em vilas sem prefeito; não há caminho implementado para levar essas demandas à cidade. A longa registrou 53.258 falhas de organizar e 69.990 de aderir; a entrega corrige apenas o caso específico de adesão com três vagas já ocupadas. O contador de ações não deve ser vendido como quantidade de histórias.
2. **Organizações nativas podem permanecer com apenas o fundador.** Na curta final, os dois líderes ficaram saudáveis na sede, mas a preparação de saída enfrentou ausência de reabastecimento de água no local. A rota física funciona em teste; a campanha não comprova expansão útil dessas organizações.
3. **Conhecimento coletivo ainda é incompleto.** Uma reunião armazena fatos recebidos pelo grupo, mas não redistribui automaticamente todos eles à mente de cada membro. Isso evita onisciência, mas a comunicação dirigida e a passagem de respostas por membros merecem aprofundamento.
4. **Culto e cosmologia têm fronteiras simples.** A política de restrição é tratada como regra pública local; o descobrimento individual da lei não é simulado em todas as etapas. A tradição inicial permite oração, mas a difusão e a organização religiosa exigem fato causal conhecido; sem uma fonte posterior, a entrada cultural é restrita. Relações entre deuses existem, mas não constituem uma diplomacia divina ativa completa. Certeza ontológica e continuidade entre corpo/novo deus são parciais.
5. **Causa final da morte não descreve toda a causalidade.** Na curta, Cael Montes morreu com uma ração após receber 16 de dano no mesmo ciclo em que roubou comida. A fome deu o dano final, mas o ataque reduziu seu HP de 18 a 2. O caso está documentado em [CASO_COMIDA_CARREGADA_CURTA.md](</home/hugo/Área de trabalho/procedrual/reports/fase_5/CASO_COMIDA_CARREGADA_CURTA.md>). Não é evidência de comida anterior ignorada ao decidir.
6. **Fome e acesso econômico continuam relevantes.** Poder local e organização não substituem sobrevivência, renda, acesso, capacidade profissional ou transporte. Não se deve concluir que uma nova camada social resolveu as mortes por privação.
7. **Save e exportação ainda custam muito.** Há histórico e registros anteriores que continuam crescendo, e `dumps` materializa uma representação grande antes de escrever. Limites dos campos novos reduzem multiplicação local, mas não resolvem essa arquitetura de persistência.
8. **Usurpação local precisa de refinamento institucional.** A nomeação por pressão verifica causa, apoio e ambição, mas não exclui explicitamente o ocupante da patente de General nessa via excepcional. A nomeação inicial e a reposição normal excluem guardas. Uma eventual sobreposição deve ser distinguida de um caso realmente observado na auditoria.
9. **Rascunho retido não equivale a conflito político ativo.** No fim da longa, a proposta #4875348 continuava com status `draft`, mas seu grupo já estava dissolvido. O objeto pode permanecer até a limpeza; o status não comunica sozinho esse encerramento. Não foi contado como caso político inacabado na seleção de histórias.

Não houve aumento de probabilidades para preencher as categorias narrativas. Os comportamentos ausentes no teste natural devem permanecer explícitos e orientar a próxima análise, sem exigir quantidade mínima de milagres, execuções ou lendas.

## Auditoria natural e custo

A curta validada **Serevan-5**, de 500h, e a única longa **Nhalven-5**, de 5.000h, usaram o mesmo núcleo SHA-256 `2a2ede5c51058e8e5ee849dc04a08f7002dd8d7da8db8278312f2460e6e4d8e1`, anterior aos ajustes finais explicitados abaixo. A longa começou com 1632 NPCs persistentes, 4092 habitantes abstratos, 69 localidades, 6 reinos, 28 prefeitos, 28 generais, 2 facções nativas e 3 deuses.

| Métrica | Curta do núcleo da longa | Longa | Curta de entrega |
|---|---|---|---|
| Seed | Serevan-5 | Nhalven-5 | Serevan-5 |
| Horas | 500 | 5000 | 500 |
| NPCs persistentes iniciais | 1616 | 1632 | 1616 |
| População abstrata inicial | 4043 | 4092 | 4043 |
| Localidades | 67 | 69 | 67 |
| NPCs vivos finais | 1597 | 1339 | 1590 |
| Mortes | 19 | 293 | 26 |
| Causas das mortes | {'hunger': 19} | {'hunger': 287, 'both': 1, 'combat': 5} | {'combat': 2, 'hunger': 23, 'thirst': 1} |
| Mortes alimentares com comida | 1 | 0 | 0 |
| Erros de integridade | 0 | 0 | 0 |
| Histórico de eventos | 66549 | 1453799 | 65168 |
| Save (MiB) | 150.04 | 1039.82 | 150.37 |
| Pico de memória do processo, incluindo exportação (MiB) | 1306.63 | 8437.92 | 1311.34 |
| Simulação (min) | 5.23 | 74.06 | 5.15 |
| Exportação do save (s) | 13.67 | 113.87 | 14.09 |

Na longa passaram **50 verificações periódicas**, além da validação inicial e final. Na curta passaram cinco periódicas, além da inicial e final. Não foi carregado save antigo. O núcleo não foi alterado durante a longa. As repetições curtas de diagnóstico estão identificadas em [EXECUCOES.json](</home/hugo/Área de trabalho/procedrual/reports/fase_5/EXECUCOES.json>); houve somente uma campanha longa iniciada nesta fase.

**Ajustes posteriores explicitados:** a entrega usa SHA-256 `cb972af78af4063d25173d1165355617317f6f702ffccc4b888ad087f15977de`. Depois da longa, foram corrigidos: hipótese recebida sobre o sucessor após apoteose; oração dirigida ao mortal realmente ascendido; prefeito que continuava no cargo após mudar de residência; oferta de adesão para quem já tinha três grupos; preservação de demandas formais e respostas públicas na sucessão municipal. O código da campanha permanece em `reports/fase_5/final_code`; o da entrega está em `reports/fase_5/entrega_code`. São hashes diferentes e não devem ser confundidos.

A suíte completa de **275 testes** passou novamente no código de entrega. Uma nova curta de **500h**, seed Serevan-5, validou esse mesmo núcleo, com 26 mortes e zero erros de integridade. Os microcenários ampliados verificaram as condições raras e save/load. A campanha longa registrou 0 apoteoses, portanto não validou frequência natural dos caminhos divinos corrigidos. Não houve segunda longa. Registro: [ENTREGA_FINAL.json](</home/hugo/Área de trabalho/procedrual/reports/fase_5/ENTREGA_FINAL.json>); curta: [resumo.json](</home/hugo/Área de trabalho/procedrual/reports/fase_5/curta_entrega_500h/resumo.json>).

**A sobrevivência não melhorou na curta de entrega:** com a mesma seed, as mortes passaram de 19 para 26, causas finais {'combat': 2, 'hunger': 23, 'thirst': 1}. Houve 0 mortes alimentares com comida carregada nessa execução. Mudanças nas escolhas sociais alteram a sequência de ações e a trajetória do RNG; essa comparação não isola qual ajuste contribuiu para cada morte. A piora observada permanece um limite da entrega, sem extrapolar a frequência da curta para 5.000h nem substituir a longa anterior.

### Política, organizações e fé observadas

| Acontecimento | Curta do núcleo da longa | Longa | Curta de entrega |
|---|---:|---:|---:|
| ProblemShared | 4664 | 85044 | 4614 |
| GroupFormed | 319 | 4332 | 299 |
| GroupJoined | 171 | 3661 | 147 |
| GroupMeeting | 38 | 241 | 33 |
| GroupDissolved | 219 | 4100 | 195 |
| ProposalCreated | 12 | 44 | 15 |
| ProposalSubmitted | 3 | 6 | 1 |
| PolicyDecided | 4 | 4 | 1 |
| PolicyRead | 2 | 2 | 1 |
| GroupProtested | 0 | 0 | 0 |
| MayorAppointed | 1 | 11 | 1 |
| RoyalAidDecided | 0 | 0 | 0 |
| FactionFounded | 0 | 0 | 0 |
| FactionJoined | 0 | 0 | 0 |
| FactionPromoted | 0 | 0 | 0 |
| FactionReport | 0 | 0 | 0 |
| OrganizationalAction | 0 | 0 | 0 |
| MilitaryOrder | 438 | 378 | 417 |
| PrayerOffered | 184 | 227 | 186 |
| DivineIntervention | 0 | 0 | 0 |
| SpiritualReport | 0 | 0 | 0 |
| FaithReinterpreted | 0 | 0 | 0 |
| DivinityKilled | 0 | 0 | 0 |
| Apotheosis | 0 | 0 | 0 |
| PowerTrained | 9 | 29 | 8 |
| ExecutionOpportunity | 0 | 0 | 0 |
| TerminalDecision | 0 | 0 | 0 |
| IncapacitatedSpared | 0 | 0 | 0 |
| ItemLegendReported | 0 | 0 | 0 |

Causas dos grupos formados na longa: **{'security': 244, 'resource_pressure': 4088}**. Encerramentos: {'problem_no_longer_shared': 42, 'lost_relevance_or_members': 4058}. Estado final dos grupos: {'active': 232, 'dissolved': 234}; propostas ainda conservadas: {'draft': 1}; facções: {'active': 2}. Os objetos encerrados são removidos após o prazo; portanto, quantidade final é diferente da quantidade histórica.

Formações por tipo de localidade: {'vila': 2563, 'cidade': 1769}. Grupos de vila não têm encaminhamento para uma autoridade urbana; esse limite se soma à dificuldade de contato entre prefeito e representante.

Houve 4 unidades de comida e 2 moedas contabilizadas nos efeitos políticos. Uma decisão pode ser parcial, adiada ou não encontrar beneficiário presente. Decisões e ações militares sem destinatários úteis não equivalem a mudança efetiva de vida.

Potenciais míticos: 4 gerados, distribuição {'Heroism': 2, 'Coldness': 2}, 3 vivos ao fim. Mudanças para intenção matar por modo: {'situational': 25, 'persistent': 1}. Os modos representam escolhas registradas; não são mortes.

Divindades objetivas no fim: 3; divindades com conhecimento ontológico confirmado: 0. Mortais venerados ainda registrados: [174, 437, 689, 1035, 1082, 2408, 2582]; mortais com apoteose objetiva: []. O contador de veneração registrou 9 atualizações de observadores e não deve ser confundido com esse número de mortais.

Personagens com epíteto retido por algum observador: 699. Alcance final calculado: {'local': 1086, 'personal': 98, 'regional': 125}. Itens históricos: 0; com contato divino: 0; com crença registrada: 0. Epítetos associados a ofício/proteção podem predominar sobre figuras épicas.

Sobreposição prefeito/General no estado final: nenhuma observada. Isso não elimina a limitação potencial da via de usurpação apontada acima.

### Qualidade das histórias e ausências

A seleção documentou **10/22 categorias** com alguma evidência natural. Isso inclui transformações pequenas ou incompletas; não significa 10 sagas grandes. O arquivo [HISTORIAS_REAIS.md](</home/hugo/Área de trabalho/procedrual/reports/fase_5/HISTORIAS_REAIS.md>) explica cada caso com fatos, estados e limites, sem inventar pensamentos.

Categorias sem exemplo natural suficiente nesta campanha:
- grupo que conseguiu proposta e se dissolveu.
- proposta recusada que aumentou tensão.
- grupo que amadureceu em facção.
- promoção em facção.
- fé atravessando região.
- rumor espiritual.
- intervenção conhecida de formas diferentes.
- epítetos diferentes em regiões distintas.
- item ganhando importância histórica.
- execução deliberada.
- misericórdia após oportunidade de execução.
- caso político/religioso inacabado.

A ausência de um arco raro não prova um bug. Porém, a persistência de poucos encontros, propostas entregues e serviços concluídos, diante de muitas tentativas, aponta um gargalo de continuidade. A próxima melhoria útil é transformar comunicação e participação em transições reais, preservando custos e conhecimento individual.

### Custo e comparação com a base

O save da longa ocupa **1039.82 MiB**. O processo alcançou **8437.92 MiB**, incluindo a serialização/exportação. A simulação levou 74.06 minutos e a escrita do save 113.87 segundos. Essas medidas dependem desta máquina e incluem o custo da auditoria. Não medem apenas a Fase 5.

Entre as duas campanhas independentes, o save cresceu 6.93 vezes. Não é uma medida da taxa exata de crescimento da mesma seed. O histórico final tem 1453799 acontecimentos, e existem fatos, memória aplicada e registros anteriores que crescem além dos novos campos limitados.

Os valores compactos dos campos de modelo acrescentados ocupam aproximadamente **8.50 MiB**, sem nomes de campos e wrappers. A medida inclui os campos novos de fama, grupos, divindades, cargos, facções e itens, mas não isola os eventos/fatos/necessidades que eles geram nos campos anteriores. Não é medida de RAM nem custo total da Fase 5. A decomposição está em [custo_campos_novos.json](</home/hugo/Área de trabalho/procedrual/reports/fase_5/longa_5000h/custo_campos_novos.json>).

A longa histórica da Fase 4.6, seed Corven-46, terminou com 1.274 vivos e 294 mortos de 1.568 NPCs iniciais: 260 por fome, 11 por fome+sede, seis por sede e 17 em combate. Seu save tinha 1.101,64 MiB. A seed, população e RNG diferem; não é possível atribuir a diferença inteira à Fase 5. O pico de memória antigo foi medido antes da exportação e não é diretamente comparável ao pico atual.

### Prioridades justificadas para continuidade

1. Melhorar representação e contato útil entre membros e autoridade: incluir encaminhamento conhecido de demandas das vilas às cidades e passagem de respostas de um membro ao representante, sem leitura remota de estado. Isso pode concluir arcos existentes, em vez de criar novas pressões sem resposta.
2. Reduzir tentativas previsivelmente inviáveis de organização/adesão com o conhecimento do NPC. Limites locais e ausência de interlocutor não deveriam produzir ação repetida sem progresso indefinidamente.
3. Tornar a sobrevivência e a saída física das sedes das facções possíveis por abastecimento real, descoberta e vínculos. Criar membros ou suprimentos por script apagaria o problema em vez de resolvê-lo.
4. Registrar mudanças de crença, título e consequências materiais de forma compacta e rastreável. Um contador agregado pode perder a identidade de quem mudou e a transformação concreta.
5. Separar causalidade contribuinte da causa final das mortes e reduzir o custo de persistência. Isso melhora diagnóstico e permite campanhas maiores sem confundir dano acumulado, fome e combate.

Dados completos: [métricas consolidadas](</home/hugo/Área de trabalho/procedrual/reports/fase_5/METRICAS_FASE_5.json>), [resumo da longa](</home/hugo/Área de trabalho/procedrual/reports/fase_5/longa_5000h/resumo.json>), [save final](</home/hugo/Área de trabalho/procedrual/reports/fase_5/longa_5000h/save_final.json>) e [preservação da geração](</home/hugo/Área de trabalho/procedrual/reports/fase_5/PRESERVACAO_GERACAO.json>).
