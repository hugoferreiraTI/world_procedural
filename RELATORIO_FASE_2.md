# Relatório da fase 2 — vida e continuidade

Data: 07/10/2026. Base utilizada: **[fase_2.md](</home/hugo/Área de trabalho/procedrual/fase_2.md>)**, com esse nome exato. Versão resultante: `mvp-3`.

Os quatro bugs foram corrigidos, a personalidade foi ampliada e as necessidades pessoais passaram a gerar objetivos e ações no motor existente. **Os 73 testes passaram e a campanha final percorreu 10.000 turnos.** Houve uma sequência real de busca familiar, descoberta de morte, transmissão da notícia, luto e pedido de companhia.

A variedade cotidiana ainda é limitada: **91,63% das seleções de necessidade dos NPCs foram fisiológicas**. A fase ampliou o que os personagens podem querer, mas não resolveu a economia, a continuidade populacional nem o predomínio da sobrevivência. Não foram reduzidos os pesos da fome para obter um resultado desejado.

## 1. Estado anterior encontrado

O `mvp-2` já possuía necessidades, prioridades, objetivos, alternativas, ações materiais, profissões, economia, memória individual, rumores, reputação, relacionamentos, quests e persistência determinística. Os 43 testes existentes passaram antes das alterações.

Dinheiro e trabalho já eram necessidades executáveis. A dimensão familiar existia em traços e relações, mas não produzia cuidado ou busca. Luto, retaliação pessoal, proteção civil, busca de reconhecimento e ascensão não tinham o ciclo completo de causa, objetivo e ação. O conhecimento já restringia diálogo e reputação, mas ainda não alimentava essas pressões pessoais.

O levantamento anterior às alterações está em [LEVANTAMENTO.md](</home/hugo/Área de trabalho/procedrual/reports/fase_2/LEVANTAMENTO.md>). Os relatórios antigos continuam preservados como registros do `mvp-2`; não descrevem integralmente o código atual.

## 2. Sistemas reutilizados

| Sistema existente | Uso na fase 2 |
| --- | --- |
| `Need` e `NeedSystem` | Pressões pessoais com alvo, contexto, fonte, prazo e transições de estado. |
| `Goal`, `Solution` e `GoalSystem` | Escolha de alternativas, deslocamento e execução dos novos objetivos. |
| Prioridade e `utility.evaluate` | Competição entre necessidades e pontuação por personalidade, relação, confiança e distância. |
| `KnowledgeSystem` | Gatilhos de fatos percebidos ou recebidos; atualização de evidência; transmissão de informação. |
| Grafo de relacionamentos | Parentesco, vínculo individual, amizade e confiança. |
| Eventos e interpretação social | Consequências de cuidado, informação, denúncia, companhia e trabalho realizado. |
| `QuestSystem` | Oferta, aceitação, recusa, conclusão, resolução por terceiros e expiração. |
| Economia, itens, profissões e navegação | Trabalho, compra, venda, coleta, transferência de provisões e deslocamento real. |
| Persistência e validação | Novos campos, RNG, regras de versão e invariantes. |

`personal.py` deriva pressões e acompanha seu ciclo de vida. `personal_actions.py` fornece candidatos e executa ações chamadas pelo `GoalSystem`. Esses auxiliares não escolhem decisões em um motor paralelo.

## 3. Sistemas deliberadamente não recriados

Não foram criados outro motor de decisões, outro sistema de quests, outra economia, outro grafo social, um planejador GOAP ou uma engine emocional. O fluxo permanece **necessidade → prioridade → alternativas → objetivo → ação → evento/conhecimento**.

Ficaram fora desta etapa: reposição profissional, materialização populacional, carreira completa, nascimentos, envelhecimento, herança, caravanas, viagens autônomas entre cidades, combate, guerras, exércitos, deuses, religião organizada e IA generativa. A revisão da população abstrata continua pendente da orientação do usuário.

## 4. Causa e correção dos quatro bugs

| Bug | Causa anterior | Correção e evidência |
| --- | --- | --- |
| Ordem temporal desigual | O jogador podia agir antes da fisiologia; o NPC podia sofrer a passagem do tempo e morrer antes de decidir comer. | As ações da hora precedem a fisiologia e a verificação de morte. O teste com vida 1, fome 100 e alimento disponível permite aos dois comer e sobreviver sob a mesma regra. Privação continua causando dano. |
| Pedido de comida bloqueado por moedas fixas | A condição `money >= 10` bloqueava ajuda mesmo quando a comida custava mais que o saldo. | Compra e pedido reutilizam `Economy.can_seek_food`. No mercado, verifica preço, estoque e dinheiro reais; longe dele, considera somente a possibilidade de ir a um mercado conhecido e conferir. O teste de 10 moedas com preço 14 permite pedir ajuda. |
| Ação inválida alterava estado | A intenção pública criava uma necessidade e consumia IDs antes de validar a ação. | A intenção usa um objetivo temporário sem alocação persistente. Trabalho inviável também é verificado antes da produção. A comparação do mundo serializado confirma que ações inválidas não alteram o save nem avançam o turno. |
| Evidência melhor descartada | Rumores eliminavam fatos cujo ID já existia, mesmo com confiança maior. | Uma evidência superior atualiza o fato. O registro de impacto social aplica apenas a diferença, sem repetir o favor. O teste eleva confiança de 30 para 80 e confirma que repetir a evidência não aumenta novamente a reputação. |

Os quatro testes de regressão **falharam no código anterior** e passaram após as correções. Registros: [falhas anteriores](</home/hugo/Área de trabalho/procedrual/reports/fase_2/regressoes_antes.txt>) e [correções verificadas](</home/hugo/Área de trabalho/procedrual/reports/fase_2/testes_bugs_corrigidos.txt>).

## 5. Traços existentes antes da mudança

Os oito traços anteriores foram preservados: honestidade, compaixão, coragem, independência, ganância, diligência, lealdade familiar e persistência.

Honestidade já influenciava compra, roubo e interpretação social; diligência influenciava trabalho; independência influenciava coleta. Lealdade familiar agora influencia também prioridades e ações familiares. Persistência permanece distinta da vontade de retaliar e participa, por exemplo, da preferência por recordar uma perda.

## 6. Traços adicionados

| Traço | Uso executável |
| --- | --- |
| `temperament` — temperamento | Predisposição estável à reação; modifica prioridade de retaliação e pontuação de investigação. Não representa uma emoção transitória. |
| `vengefulness` — vingatividade | Modifica prioridade, duração e alternativas de reação a dano conhecido. Não impõe um ataque. |
| `ambition` — ambição | Intensifica reconhecimento e reserva financeira de longo prazo, com metas concretas. |

Os 11 traços usam a escala existente de 0 a 100, são gerados pelo RNG da seed e sobrevivem ao save/load. A geração normal sorteia valores entre 5 e 95. Não há um estado emocional completo.

## 7. Traços deliberadamente não adicionados

Não foi criada **falsidade** como inverso duplicado de honestidade. Não foi criada outra **orientação familiar**, pois `family_loyalty` já representa essa predisposição; a força de cada vínculo permanece no grafo.

**Cinismo** também não foi adicionado: nesta implementação não havia uma alternativa executável própria que justificasse o campo. Isso é ausência deliberada de comportamento distinto nesta etapa, sem afirmar que cinismo e honestidade sejam a mesma coisa.

## 8. Novas necessidades e grau de implementação

| Capacidade | Situação | Alcance real |
| --- | --- | --- |
| Cuidado e busca familiar | **IMPLEMENTADO** | Percepção, necessidade, alvo, prioridade, deslocamento, provisões, busca, informação e fechamento. |
| Luto | **IMPLEMENTADO** | Morte conhecida, vínculo relevante, companhia ou recordação, prazo e deduplicação por pessoa perdida. |
| Reação a dano/vingança | **IMPLEMENTADO** | Investigação, denúncia, informação e afastamento; sem ataque automático. |
| Proteção pessoal/familiar/residencial | **PARCIAL** | Crime conhecido gera denúncia, afastamento ou acompanhamento. Não há defesa física nem construção de proteção da residência. |
| Pressão financeira persistente | **IMPLEMENTADO** | Amplia `money` e reutiliza `work`, salários, comércio e excedentes. Não cria uma necessidade financeira concorrente. |
| Reconhecimento/status | **IMPLEMENTADO; eficácia limitada na campanha** | Gera objetivo de realizar ajuda ou responsabilidade observável. Não concede popularidade ao criar a necessidade. |
| Ascensão | **PARCIAL** | Ambição gera uma meta concreta de aumentar a reserva de dinheiro. Não há promoção de profissão, título ou categoria social. |
| Fé pessoal executável e religião | **APENAS BASE/DADOS; ações AUSENTES** | Campos anteriores não foram convertidos em rituais, culto ou objetivos religiosos. Religião organizada permanece fora do escopo. |
| Reposição profissional e população completa | **AUSENTE** | Nenhum substituto nasce ou é materializado para preencher vagas. |

“Implementado” nesta tabela exige comportamento executável. As limitações de frequência e resultado estão nas seções de auditoria, sem transformar a presença do código em prova de eficácia cotidiana.

## 9. Gatilhos de cada necessidade

| Necessidade | Fonte e condição |
| --- | --- |
| Cuidado familiar | Encontro real com familiar que apresenta fome ou sede de pelo menos 55; relacionamento e gravidade modificam a pressão. |
| Busca familiar | Ausência percebida por pelo menos 36 horas após uma observação anterior. Parentesco sozinho não revela onde o familiar está. |
| Luto | Fato conhecido de morte ou identificação de restos, confiança mínima 30 e vínculo relevante de pelo menos 40. Morte desconhecida não produz luto. |
| Vingança/retaliação | Dano conhecido contra si ou familiar; morte atribuída a responsável conhecido; em circunstâncias específicas, roubo local presenciado durante privação. |
| Proteção | Crime conhecido contra si/familiar, na residência ou recorrente no local. A segurança profissional do guarda continua no sistema anterior. |
| Dinheiro/renda | Reserva baixa persistente. Após 48 horas, a meta de estabilização passa de 10 para 20 moedas; insucessos financeiros também aumentam a pressão existente. |
| Status | Personagem comum com ambição alta encontra alguém importante/lendário ou alguém que ele próprio admira. Não consulta fama global invisível. |
| Ascensão | Ambição alta e reserva de pelo menos 10 moedas permitem formular uma meta superior: saldo atual + 10 + uma parcela da ambição. |

As necessidades registram fonte, motivo, alvo quando aplicável, contexto e datas. Pessoais possuem prazos: cuidado 48 horas, busca 72, proteção 48, status 168 e ascensão 240; vínculo prolonga luto e vingatividade prolonga reação a dano. Um novo episódio pode reutilizar o mesmo ID sem apagar o histórico contado nas métricas.

## 10. Soluções executáveis e fechamento

| Necessidade | Alternativas e condições de encerramento |
| --- | --- |
| Cuidado familiar | Entregar comida ou água disponível; obter comida por compra/coleta; pedir ajuda. Fecha com ajuda pertinente ou melhora observada. Obter uma provisão é uma etapa, não a entrega automática. |
| Busca familiar | Ir ao último local conhecido, verificar presença e pedir informação. Reencontro ou informação válida resolve a busca; morte confirmada pode convertê-la em luto. Procurar sem encontrar gera evento de tentativa. |
| Luto | Procurar companhia de alguém conhecido ou visitar um local relacionado à perda para recordar. Ajuda recebida/recordação fecha o episódio; também pode expirar. |
| Vingança/retaliação | Investigar último local conhecido do responsável, denunciar fato conhecido, buscar informação ou afastar-se. Intervenção conhecida do guarda ou morte conhecida da ameaça também pode encerrar a pressão. Investigar não garante encontrar o responsável. |
| Proteção | Denunciar a guarda conhecido, buscar local seguro ou acompanhar pessoa protegida presente. Não executa combate. |
| Dinheiro/renda | Trabalhar na profissão e vender excedente real, com estoque e dinheiro do mercado. Não cria moeda ao formular uma meta. |
| Status | Ajudar materialmente ou cumprir uma responsabilidade profissional. Observadores podem interpretar o feito; o autor não recebe pontos automáticos de fama. |
| Ascensão | Trabalho e venda até alcançar a reserva alvo; possibilidade de bloqueio ou expiração. |

Sem alternativas viáveis, a pressão pode ser marcada como bloqueada. Uma alternativa disponível ainda pode falhar: o interlocutor pode não saber a resposta, o guarda pode ter saído, o estoque pode faltar ou o local conhecido pode estar desatualizado.

Limitação concreta: cuidado com água pode entregar água já disponível, mas ainda não inclui uma alternativa autônoma específica de comprar água para o familiar.

## 11. Integração com personalidade

O traço altera pontuação ou prioridade; não determina sozinho a ação. Independência favorece busca direta e recordação, compaixão favorece ajuda/companhia, coragem e vingatividade afetam investigação, honestidade favorece denúncia e diligência favorece trabalho. Distância, estoque, conhecimento, confiança e vínculo continuam influenciando as alternativas.

As necessidades pessoais competem com fome, sede e descanso no sistema atual. Testes demonstram que uma necessidade não fisiológica pode superar fome leve, e que sobrevivência crítica pode superar ambição de baixa prioridade. As regras de dano, recuperação e os pesos anteriores da fome foram preservados.

O debug registra necessidades ativas, prioridade, fonte, motivo, contexto, alvo e considerações de cada candidato, incluindo contribuição da personalidade. Pode ser habilitado com `engine.goals.debug = True`; os registros ficam em `engine.goals.traces[npc_id]`.

## 12. Integração com conhecimento

Observações guardam posição e sinais do encontro; não acompanham automaticamente o personagem distante. Notícias passam por `KnowledgeSystem.learn`, inclusive rumores com confiança limitada. O fato conhecido alimenta a pressão; a verdade acessível internamente ao simulador não substitui essa percepção.

Foi mantida a deduplicação de impactos sociais e adicionada a deduplicação de reações pessoais. Repetir notícia de morte ou reaprendê-la depois do esquecimento não cria outro luto pela mesma pessoa. Evidência superior reforça o contexto existente. Informação de localização anterior à nova busca não resolve uma ausência posterior.

Os comandos públicos `fatos`, `investigar NPC_ID`, `informar NPC_ID FACT_ID` e `acompanhar NPC_ID` permitem participar dessas histórias. Investigar identifica pessoa ou restos presentes na posição atual. Informar exige fato conhecido e encontro com quem recebe; não transmite uma resposta instantânea entre mapas. Restos são exibidos somente na posição do jogador.

## 13. Integração com relacionamentos

Parentesco usa as relações existentes de casamento, pai/filho. A intensidade do vínculo individual modifica cuidado e luto; `family_loyalty` é a predisposição geral do personagem, não o valor de cada relação.

Amizade, familiaridade, confiança e reputação contextual influenciam interlocutores, companhia e disposição para pedidos. Ajuda, informação e cumprimento de responsabilidade emitem eventos que podem modificar a opinião de quem soube deles. Criar uma necessidade não melhora diretamente relacionamento ou popularidade.

Limitação: companhia já pode ser prestada, mas não há uma negociação extensa de consentimento, disponibilidade e duração emocional de cada acompanhante.

## 14. Integração com quests existentes

O mesmo `QuestSystem` agora suporta contratos de comida, localização familiar, cuidado material familiar, companhia, proteção e informação. A oferta depende de necessidade real, prioridade, contato/confiança e limitações de pedidos pendentes.

Aceitar e recusar exigem encontro com o solicitante vivo. Conclusão depende da entrega, informação pertinente ou companhia efetivamente prestada. Se a necessidade for resolvida por outro meio, a quest pode receber `resolved_elsewhere`; expirando a necessidade, o pedido pode falhar. Não foi criada uma segunda engine de quests.

Na campanha final surgiram apenas **comida, busca familiar e companhia**. Cuidado, proteção e informação possuem fluxo executável, mas não tiveram quests observadas nessa execução. Dinheiro, status e ascensão não oferecem contratos específicos ao jogador nesta implementação.

## 15. Testes antigos e novos

Resultado final: **43 testes antigos + 30 novos = 73 aprovados**, em 20,043 segundos. Evidência: [testes.txt](</home/hugo/Área de trabalho/procedrual/reports/fase_2/testes.txt>); casos novos: [test_phase2.py](</home/hugo/Área de trabalho/procedrual/tests/test_phase2.py>).

Os equivalentes exigidos pelo documento cobrem:

- Os quatro bugs, com reprodução anterior e ausência de reputação duplicada.
- Personalidade determinística, persistência dos traços e ausência de falsidade redundante.
- Família executável, ausência dependente de observação, morte desconhecida sem luto e morte conhecida com luto único.
- Efeito de vingatividade e coragem, alvo conhecido/acreditado e ameaça conhecida para proteção.
- Renda reutilizando dinheiro/trabalho; status sem popularidade instantânea; ambição com meta concreta.
- Competição com fome leve e sobrevivência crítica; quest emergente; bloqueio e expiração.
- Mesma seed com mesmas decisões e estado pessoal após save/load.
- Ações pessoais inválidas sem mutação, informação antiga, restos locais e impedimento de respostas entre mapas.

Os testes comportamentais usam cenários controlados para isolar regras. A campanha abaixo usa o mundo gerado normalmente, sem inserir perdas, NPCs, recursos ou personalidade manualmente para fabricar exemplos.

## 16. Resultado da auditoria de 10.000 turnos

Campanha final: seed `Dovha`, regras `mvp-3`, turno inicial 24 e final 10.024. Foram **10.000 avanços individuais de uma hora**, por comandos públicos de jogador automatizado. A preparação normal do mundo ocupa as primeiras 24 horas e é separada dos resultados desta campanha.

O controlador cuidou da sobrevivência, trabalhou, coletou, comprou, vendeu, conversou, aceitou/recusou pedidos, entregou itens, investigou e informou. Não houve teleporte, reposição manual de inventário, edição de atributos nem alteração de RNG. Leituras do auditor servem para medir, sem orientar o jogador por informações ocultas.

| Indicador | Resultado final |
| --- | ---: |
| Tempo de execução | 177,03 segundos |
| Vida final/mínima do jogador | 100 / 100 |
| Dinheiro final | 28 |
| Fome / sede / cansaço final | 40 / 20 / 61,6 |
| NPCs vivos no início / final | 456 / 317 |
| Mortes durante a campanha | 139 |
| Mercados sem comida no final | 26 de 79 localidades |
| Localidades sem residentes locais vivos | 4 |
| Reinos sem governante | 5 de 6 |
| Quests concluídas | 11 de 49 |
| Ações inválidas com mutação persistente detectada | 0 |
| Checkpoints com erro de invariantes | 0 de 10 |
| Diferença no balanço monetário em cada checkpoint | 0 |

O jogador visitou Vallen e o mapa externo. As decisões dos NPCs foram medidas no mundo inteiro; a campanha não equivale a um jogador que percorreu todas as cidades ou testou todas as combinações de interação.

| Tipo de quest | Total | Concluída | Recusada | Falhou | Resolvida por outro meio |
| --- | ---: | ---: | ---: | ---: | ---: |
| Comida | 43 | 10 | 13 | 0 | 20 |
| Busca familiar | 5 | 1 | 1 | 3 | 0 |
| Companhia | 1 | 0 | 1 | 0 | 0 |
| **Total** | **49** | **11** | **15** | **3** | **20** |

O save final carrega, valida e serializa novamente de forma idêntica. Duas cópias independentes continuaram mais 24 horas com estados e RNG idênticos, sem modificar o arquivo final.

Foi preservada também uma auditoria intermediária em `reports/fase_2/auditoria_10000`. A campanha final acima inclui a conclusão de busca familiar por identificação local de restos. Os números deste relatório pertencem à pasta **`auditoria_10000_final`**.

## 17. Distribuição e ciclo de vida das necessidades

Houve **930.703 seleções de necessidade de NPCs** durante as 10.000 horas. Uma seleção não é necessariamente uma ação concluída: pode resultar em deslocamento, tentativa ou falha. Esses percentuais não representam turnos do jogador nem divisão direta de tempo; necessidades urgentes também fazem o NPC decidir com maior frequência.

| Categoria | Seleções | Percentual |
| --- | ---: | ---: |
| Fisiológicas: fome, sede e descanso | 852.814 | 91,6312% |
| Trabalho/renda | 62.985 | 6,7675% |
| Família | 7.395 | 0,7946% |
| Segurança profissional dos guardas | 7.021 | 0,7544% |
| Ambição/ascensão | 364 | 0,0391% |
| Proteção pessoal | 101 | 0,0109% |
| Vingança/retaliação | 15 | 0,0016% |
| Luto | 8 | 0,0009% |
| Status | 0 | 0% |

Fisiológicas separadas: fome 546.561, sede 147.379 e descanso 158.874. Portanto, **91,63% não significa apenas fome**.

| Categoria | Criadas | Satisfeitas | Expiradas | Bloqueadas | Geraram quest |
| --- | ---: | ---: | ---: | ---: | ---: |
| Fisiológicas | 33.842 | 33.420 | 416 | 0 | 43 |
| Trabalho/renda | 138.710 | 138.065 | 145 | 1.002 | 0 |
| Família | 12.259 | 1.262 | 10.946 | 1.186 | 5 |
| Segurança profissional | 7.575 | 7.570 | 0 | 0 | 0 |
| Ascensão | 2.428 | 7 | 2.498 | 34 | 0 |
| Proteção | 4.976 | 58 | 4.860 | 0 | 0 |
| Vingança/retaliação | 3.610 | 3.342 | 236 | 0 | 0 |
| Luto | 32 | 5 | 27 | 0 | 1 |
| Status | 19 | 0 | 29 | 0 | 0 |

São contagens de **episódios/transições**, incluindo reativação de um mesmo ID. Bloqueio é contado uma vez por episódio e pode posteriormente ser superado. Uma necessidade gerada antes do turno 24 pode terminar dentro da campanha; por isso expirações de status/ascensão podem superar criações do período. Não são categorias mutuamente exclusivas de resultado para calcular uma taxa simples de sucesso.

Trabalho/renda agregam `work` e `money`. Grande parte das transições de `work` vem da rotina profissional existente, inclusive seu encerramento diário; não representa 138 mil conquistas financeiras de longo prazo.

**Vingança exige uma ressalva:** 3.342 episódios satisfeitos não significam 3.342 ações de retaliação. O encerramento ocorre sobretudo por conhecimento de intervenção dos guardas. Houve somente 15 seleções explícitas dessa necessidade e 9 eventos de investigação na campanha.

Eventos pessoais medidos no período:

| Evento | Quantidade |
| --- | ---: |
| Preocupação familiar | 10.032 |
| Ausência percebida | 2.227 |
| Verificação de local sem encontrar familiar | 2.369 |
| Pessoa localizada | 520 |
| Informação transmitida | 310 |
| Denúncia de ameaça | 58 |
| Investigação de responsável | 9 |
| Restos identificados | 3 |
| Recordação de pessoa perdida | 4 |
| Companhia prestada no luto | 1 |

Não foram observados `ThreatAvoided`, `ProtectionGiven` ou `ResponsibilityFulfilled` durante as 10.000 horas. Na preparação inicial houve 11 seleções de status e 7 eventos de responsabilidade cumprida; esses números não foram misturados à campanha. Status é executável, mas não conseguiu ser selecionado no período longo.

**Correção da medição:** o observador inicialmente podia recontar um registro antigo de decisão quando o NPC voltava a atualizar sem gerar outro registro. A distribuição oficial foi obtida pela diferença dos contadores persistentes `NPCNeedSelected` do motor, entre os turnos 24 e 10.024. As amostras antigas foram mantidas em `trace_observation_counts`, e o observador foi corrigido para execuções futuras. Essa correção de contagem não altera as decisões, o RNG ou o save da campanha. A fonte oficial é [metricas_fase2.json](</home/hugo/Área de trabalho/procedrual/reports/fase_2/auditoria_10000_final/metricas_fase2.json>), não a contagem de amostras impressa no log de execução.

## 18. Exemplos reais de comportamento emergente

### Bela Douran: ausência, descoberta e luto

Bela, ID 345, era estudante e filha de Dovha, ID 339, e Lyra Douran, ID 342. Dovha morreu no turno 378; Lyra morreu no turno 471. A morte verdadeira e a notícia conhecida não foram tratadas como a mesma coisa.

No turno 667, Bela selecionou `remember_relative` por conhecer a morte de Lyra, com vínculo 100 e prioridade de luto 71,7. Seus traços incluíam independência 76, lealdade familiar 73, compaixão 19 e persistência 60. Ela foi recordar a perda, sem receber um roteiro especial para essa família.

Para Dovha, entretanto, continuou procurando informação. Ofereceu pedidos de localização nos turnos 627, 695, 818, 845 e 926. Três falharam, um foi recusado e o último, **quest 146390**, foi concluído.

1. No turno **968**, o jogador executou `investigar 339` onde os restos estavam presentes e obteve o fato **152367** de morte confirmada.
2. No turno **975**, executou `informar 345 152367` num encontro com Bela. A informação concluiu a busca e gerou luto conhecido pela morte do pai.
3. No turno **976**, conversar com Bela abriu a **quest 153527**, “Acompanhar Bela Douran em seu luto”.
4. No turno **977**, o controlador recusou o pedido. A recusa foi uma escolha da política de auditoria, que também recusa outros pedidos; não foi um desfecho programado para Bela.

Essa sequência demonstra continuidade causal: **ausência percebida → busca → evidência local → comunicação → encerramento da busca → nova necessidade → novo pedido**. O texto ainda é simples, mas a história tem causas verificáveis e consequências para o jogador.

### Respostas diferentes à pressão familiar

| NPC e turno | Escolha observada | Resultado e contexto |
| --- | --- | --- |
| Marie Valerius, ID 787, turno 24 | Dar provisões | Entregou a um familiar; vínculo 81, prioridade 69,35 e recursos disponíveis. |
| Marie Montes, ID 1544, turno 25 | Comprar comida | Selecionou compra como etapa para atender necessidade familiar; não equivale à entrega concluída. |
| Darin Bruma, ID 1808, turno 28 | Pedir informação/ajuda | Tentou ajudar familiar com necessidade de água, mas o interlocutor não conhecia informação útil. A tentativa falhou. |
| Tomas Luar, ID 355, turno 36 | Verificar familiar | Localizou o alvo. Lealdade familiar 84 e prioridade 58 contribuíram para a busca. |
| Iria Alvor, ID 672, turno 53 | Coletar | Selecionou coleta para cuidado familiar, prioridade 78,05, independência e lealdade familiar 89. O registro mostra a etapa em andamento, sem provar entrega posterior. |

Os cinco demonstram alternativas diferentes diante do mesmo tipo de pressão. Recursos, posição, conhecimento e vínculos também variam; não é uma comparação que isola apenas personalidade. Darin, por exemplo, possui independência 95 e ainda assim pediu ajuda: traço não é comando determinístico.

### Dois modos de lidar com luto

Além de Bela recordar Lyra, **Marie Stone, ID 485**, procurou companhia no turno 1.978 após conhecer a morte do cônjuge **Marie Stone, ID 488**. Os nomes são iguais, mas os IDs e personagens são diferentes. Ela buscou **Mira Stone, ID 491**, e concluiu a ação `seek_company`.

Seu vínculo com a pessoa perdida era 98, independência 11 e compaixão 49. O luto alcançou prioridade **82,5**, superando fome com prioridade **80** naquele momento. É um exemplo real de necessidade pessoal vencendo uma pressão fisiológica relevante, sem desativar a fome.

### Denúncia, investigação e ambição

**Silas Kars, ID 1619**, denunciou uma ameaça conhecida ao guarda ID 1633 no turno 28. Proteção teve prioridade 53,25 e fome 51,8. Honestidade 73 e coragem 85 contribuíram para denunciar; houve transmissão real do fato.

**Darin Stone, ID 1693**, investigou o último local conhecido do responsável ID 1696 no turno 42, por roubo local conhecido. Vingatividade 93 elevou a reação; coragem 19 reduziu sua preferência pela investigação, mas não a proibiu. O evento confirma a verificação do local, sem confronto ou garantia de capturar alguém.

**Aldren Valerius, ID 579**, trabalhou no turno 26 sob ascensão financeira, com ambição 71, diligência 72 e meta de 43 moedas. Houve produção executada; isso não significa promoção de carreira nem prova de que alcançou a reserva naquele turno.

### Quantidade de diferenças observadas e limite da conclusão

As amostras preservadas mostram cinco NPCs com cinco alternativas familiares e dois NPCs com duas alternativas de luto: **sete NPCs em dois tipos de pressão com respostas diferentes**. Há ainda os exemplos individuais de denúncia, investigação e trabalho por ascensão.

O auditor **não encontrou dois NPCs com escolhas diferentes vinculadas ao mesmo evento-fonte de luto, vingança ou proteção**. O contador desse critério estrito é zero. A campanha demonstra diversidade entre situações do mesmo tipo; a influência isolada dos traços está nos testes controlados. Não há evidência suficiente para afirmar que esta seed demonstrou toda a diferenciação pretendida diante de um único acontecimento compartilhado.

## 19. Bugs ou limitações restantes

Não apareceu crash, corrupção de save, quebra de invariantes ou mutação por ação inválida na campanha final. Isso cobre o percurso executado e não constitui garantia de ausência de qualquer bug.

| Limitação | Evidência e impacto |
| --- | --- |
| Sobrevivência domina a seleção | 91,63% das seleções fisiológicas. A variedade existe, mas permanece rara no cotidiano. |
| Status perde a competição no período longo | 19 episódios novos, zero seleções e zero feitos de responsabilidade no período. Implementação executável não se converteu em participação significativa nesta campanha. |
| Luto costuma expirar | 32 criados, 27 expirados, 8 seleções e 5 satisfeitos. Há histórias válidas, mas muitas perdas não geram ação visível. |
| Proteção tem pouca execução | 4.976 episódios, 101 seleções, 58 satisfeitos e 4.860 expirados; acompanhamento e afastamento não apareceram nesta campanha. |
| Cuidado familiar ainda gira frequentemente em torno de provisões | 10.032 eventos de preocupação familiar são principalmente sinais de privação, não 10 mil histórias sociais distintas. Busca e luto oferecem continuidade diferente. |
| Ausência e tentativas podem se repetir | O último local conhecido pode permanecer desatualizado; depois de prazos/cooldowns a busca pode voltar. As três quests familiares falhadas mostram esse limite. |
| Água para familiar tem alternativas restritas | Entrega existe; aquisição autônoma específica para esse cuidado ainda é incompleta. |
| Ascensão tem alcance financeiro | Meta de reserva executável, sem progressão profissional, títulos ou poder político. Apenas 7 episódios satisfeitos no período. |
| Vingança pode acabar por ação alheia | O conhecimento da resposta do guarda fecha episódios. Contar esses fechamentos como façanhas do dono da necessidade inflaria a narrativa. |
| Continuidade populacional/profissional ausente | 139 mortes, quatro localidades sem residentes locais vivos e cinco reinos sem governante. Não houve reposição nesta fase. |
| Personalidade qualitativa ainda exige mais amostragem | Zero casos estritos de escolhas diferentes no mesmo evento-fonte nas categorias auditadas. Uma seed e uma rota de jogador têm alcance limitado. |
| Companhia é simplificada | Encontro útil pode fechar o luto; não há duração emocional profunda ou negociação extensa de apoio. |
| Registros de idempotência crescem | O registro factual persistente totalizou 43.698 entradas no último checkpoint. Memórias/observações têm limites, mas registros contra repetição merecem análise de crescimento em campanhas maiores. |

### Por que a sobrevivência continuou dominando

Há evidência de **pressão material real**, não apenas falta de enums pessoais. No save final, 164 dos 317 NPCs vivos apresentavam fome ou sede de pelo menos 70; 49 estavam em 85 ou mais. Dos vivos, 171 tinham menos de 10 moedas, incluindo 21 sem dinheiro. A fisiologia continua avançando por hora, e a atualização fica mais frequente sob urgência.

A economia também restringe soluções: 26 mercados estavam sem comida, enquanto 47 localidades tinham pelo menos 240 unidades de grão. Isso indica que ter matéria-prima no mundo não garante comida preparada, dinheiro, acesso e momento adequado para cada NPC. Salários dependem do caixa local; estoques e capacidades de produção são limitados. Não há reposição profissional nem distribuição autônoma entre cidades para compensar perdas.

Das 139 mortes registradas, 25 ocorreram com algum alimento carregado e nenhuma com água carregada. Isso recomenda examinar sede, deslocamento e competição entre ações, em vez de atribuir todas as mortes somente à quantidade global de comida. O teste temporal corrigido continua passando: possuir um recurso não equivale a ter tempo para obter água, comer e descansar na mesma hora.

As novas pressões **recebem gatilhos**, como mostram milhares de episódios familiares, de proteção e de retaliação. Algumas alternativas conseguem vencer: denúncia de Silas, luto de Marie e busca de Tomas. Muitas, porém, perdem prioridade, dependem de encontro/informação ou terminam antes de ganhar uma ação. Status e ascensão começam com pressão moderada e mostram o maior limite de competição.

Esses dados e as regras apontam para a combinação de economia/acesso, frequência fisiológica e disponibilidade/prioridade das ações pessoais. A campanha não isolou experimentalmente o peso de cada causa; não há fundamento para declarar que um único ajuste resolveria o problema. Nenhum peso foi alterado para mascará-lo.

### Compatibilidade

O motor usa **`mvp-3`**, com novos campos e nova semântica temporal. Saves `mvp-1` e `mvp-2` são recusados explicitamente; não há migração automática. A versão participa da derivação da seed, portanto `Dovha` não gera a mesma geografia entre versões. Resultados populacionais de campanhas antigas não são uma comparação controlada de antes/depois.

O save anterior de 10.000 turnos foi preservado sem alterações. Seu SHA-256 continua `9e7c83ae32df3898c52705ac0f1d7094119e84662204c28b851ad5bb678b7ed7`.

## 20. Recomendações para a próxima etapa

1. **Revisar a população abstrata conforme a próxima especificação do usuário.** Em seguida, definir como reposição profissional mantém produção e sucessão, sem introduzir habitantes apenas para corrigir uma estatística.
2. **Auditar acesso a comida e água por profissão/localidade.** Registrar deslocamentos, caixas sem salário, conversão de grão, mortes com provisões e momento das ações; testar correções de causa antes de reduzir dano ou prioridade de sobrevivência.
3. **Aprofundar alternativas pessoais que ficaram pouco viáveis.** Aquisição de água para familiar, pistas de busca desatualizadas, negociação de companhia e continuidade de proteção são lacunas concretas.
4. **Medir separadamente prioridade e disponibilidade.** Para status, luto e ascensão, registrar quando havia alternativa viável e qual pressão a superou. Isso permite calibrar competição com evidência, sem impor cotas de ações sociais.
5. **Expandir a auditoria a outras seeds e rotas.** Incluir acompanhamento aceito, proteção e dois parentes recebendo o mesmo evento; comparar personalidade sob condições controladas além dos testes unitários.
6. **Revisar retenção de registros persistentes.** Preservar a idempotência sem crescimento desnecessário de informação derivável ou irrelevante em campanhas muito mais longas.

Essas recomendações não foram implementadas antecipadamente. A fase 2 entregue já permite novas causas e encadeamentos de história, enquanto a sustentação material e a frequência dessas histórias seguem como trabalho posterior.

## Evidências e reprodução

- [Relatório bruto da campanha](</home/hugo/Área de trabalho/procedrual/reports/fase_2/auditoria_10000_final/relatorio.json>): comandos agregados, quests, mortes e checkpoints.
- [Métricas da fase 2](</home/hugo/Área de trabalho/procedrual/reports/fase_2/auditoria_10000_final/metricas_fase2.json>): distribuição oficial, ciclo de vida, personalidade, fontes e exemplos de decisão.
- [Ações do jogador](</home/hugo/Área de trabalho/procedrual/reports/fase_2/auditoria_10000_final/acoes.jsonl>) e [eventos pessoais](</home/hugo/Área de trabalho/procedrual/reports/fase_2/auditoria_10000_final/eventos_pessoais.jsonl>): sequência verificável das histórias.
- [Save final](</home/hugo/Área de trabalho/procedrual/reports/fase_2/auditoria_10000_final/save_final.json>): mundo atual, versão `mvp-3`.
- [Verificação final](</home/hugo/Área de trabalho/procedrual/reports/fase_2/verificacao_final.json>): invariantes, hashes e contagens do save utilizadas na análise das limitações.
- [README](</home/hugo/Área de trabalho/procedrual/README.md>): execução e comandos atuais.

```bash
python3 -m unittest discover -s tests -v
python3 -m experiments.phase2_audit --seed Dovha --turnos 10000 --output reports/fase_2/nova_auditoria
python3 -m procedural --seed Dovha --nome Hugo
```

Uma nova auditoria deve usar outra pasta para preservar a evidência entregue. O observador corrigido também registra quantas necessidades já estavam ativas no início.

SHA-256 do save final: `8697505ec5279b791b0184babc0b9e2ed273a557e634c34997e2bc5354094396`.

SHA-256 dos arquivos `procedural/*.py`, concatenados em ordem de caminho: `984cefd941906afb9e35f70a1fb01f82322290b6fc132dcf9576d3b102b9de0c`.
