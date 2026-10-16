# Diagnóstico e extensão da Fase 4.6

Base preservada: `mvp-6-fase4.5`, SHA-256 `20b26d3def72979fc3c03938856c8d8301ee39336089fb6088970a9cfe656442`, em `baseline_code/procedural`.

| Componente | Limitação demonstrada na base | Extensão necessária |
|---|---|---|
| Intenção de violência | `intent_scores` misturava emoção geral, uma soma linear e quantidade de golpes graves. Não havia pré-condição semântica para considerar matar. A longa anterior não apresentou intenção `kill`. | `LethalPressure` verifica autoria conhecida, grievance dirigida, perda/perigo grave e compromisso. Só depois compara o resultado com intenções não letais. |
| Reação a agressão grave | `response` não era elegível para Commitment; por isso uma vítima agredida repetidamente não sustentava intenção profunda por essa via. Sua intensidade também ficava presa à oportunidade percebida na adoção. | Reação só amadurece com dano próprio grave conhecido, grievance e reincidência/perigo sério. Dano novo atribuído ao mesmo alvo pode aprofundar compromisso já existente. Raiva e insulto isolados continuam insuficientes. |
| Histórico de conflito | `begin` incrementava `blows` em cada ataque. Isso não distingue uma discussão reincidente de dez golpes no mesmo combate. | Agregados por par: episódios, hostilidade conhecida, ferimento atribuído, alternativa tentada e violência posterior que demonstra seu fracasso. Oito pares por personagem; nenhum EventLog duplicado. |
| Investigação | `pursue` verificava a última célula três vezes; `investigate` marcava uma tentativa única. A resposta pessoal de vingança consultava principalmente a vítima. | Capacidade reutilizável de consultar fontes presentes e verificar locais conhecidos, usando o alvo da busca; informantes usam exclusivamente memória e observações próprias. |
| Continuidade | Ausência de progresso levava a pressão de abandono; não havia estado de espera por informação. | `waiting_for_information` conserva compromisso e causa, suspende buscas e preserva a vida diária. Informação útil reativa a competição entre Needs, sem ação no callback. |
| Rotina após viagem | O retorno padrão aproximava uma casa situada em outro mapa, o que a navegação local recusava. | Retorno físico ao mapa da própria residência através da navegação existente, conservando residência e recursos reais. |
| Guarda | Canal institucional compartilhava o crime inicial, sem campo para depositar e retransmitir uma nova pista. | Uma pista formal recente por caso, latência de seis horas, presença no serviço local, autorização conhecida e tarefas já existentes. |
| Recursos | A preparação de uma viagem podia ocorrer sob a Need longa, sem registrar ajuda verificável de uma Need canônica. | Contexto limitado em necessidades já existentes; bônus de quatro pontos na alternativa, com progresso somente quando provisões reais aumentam e havia déficit conhecido. |
| Depuração | Na primeira suíte completa, a contagem adicionada na enumeração de alternativas diferia quando a depuração enumerava novamente. Três testes apontaram divergência do save nos contadores. | A auditoria deve ocorrer na decisão real, e a enumeração deve ser consultável sem efeitos de auditoria ou dormência. As três regressões são repetidas após o reparo. |

A fórmula física de potência e o bloco de cálculo de dano não recebem modificadores de intenção. A fase também não acrescenta multiplicadores de ataques, armas, críticos ou HP. A decisão pós-incapacidade continua oferecendo poupar, afastar, pedir auxílio e capturar quando autorizado.

As principais barreiras registradas são compaixão, honestidade, medo, risco, vínculo, autoria incerta, autoridade, testemunhas, reputação e consequências criminais conhecidas. Raiva, vingatividade e desespero isolados não satisfazem as pré-condições. Uma suspeita fraca só pode ultrapassá-las quando há também perigo físico atribuído, reincidência extrema e contexto pessoal que explica a irracionalidade.

Limites: quatro compromissos por NPC, três pistas por compromisso, oito fontes consultadas e quatro áreas por pista, uma pista institucional recente por caso. A espera tem horizonte finito e os casos conservam seus prazos por gravidade. A fonte emocional não é reaplicada ao lembrar ou reativar.

Não há planner, geração de dinheiro/comida, teleporte, informação sobre posição remota ou histórias prontas. Nenhum sistema da Fase 5 faz parte desta entrega.

A auditoria final também protege a contagem causal contra reaprendizagem: melhorar confiança ou reaprender um fato antigo não duplica dano recebido nem substitui uma tentativa de resolução mais recente. A regressão 18 reproduz ambos os casos.

A confiança é avaliada no fato grave que justifica a decisão: uma agressão conhecida com 100% de confiança não confirma uma acusação de homicídio com 30%. Perda importante comprovada pode sustentar uma intenção grave sem exigir ataques anteriores do próprio vingador. As regressões 2 e 3 cobrem os dois casos.

Quando a autoria ainda é desconhecida, consultar uma fonte que realmente conhece o homicídio transmite o fato com a confiança permitida, identifica o autor e retargeta o mesmo compromisso. A pista do autor é avaliada separadamente da pista da vítima, para que encontrar seus restos não bloqueie a investigação do culpado. A regressão 11 verifica esta continuidade.
