# Histórias emergentes observadas

Leitura das três campanhas corrigidas, com 10.000 horas cada. Os turnos abaixo são os turnos absolutos do mundo: a auditoria começou no turno 24. IDs identificam pessoas dentro da campanha indicada; resultados de campanhas diferentes não devem ser misturados.

As evidências selecionadas estão em [historias_evidencias.json](</home/hugo/Área de trabalho/procedrual/reports/correcao_alimentar/historias_evidencias.json>). O catálogo contém eventos originais, conhecimento antes da ação, necessidades, resultados, relações e estados finais. Relações de confiança ali são valores finais; os valores de parentesco citados também aparecem no contexto das necessidades durante os episódios. “Sucesso” de uma ação significa execução aceita pelo motor: uma procura que não encontrou ninguém também pode ter sido executada com sucesso.

## S01 — Marie tenta ajudar Lyra, denuncia seus crimes e acaba encontrando os restos

**Campanha jogador.** Marie Luar **77**, cozinheiro; Lyra Luar **74**, agricultor; John Montes **91**, guarda. Marie e Lyra têm casamento de valor **94**. O jogador não intervém nesta cadeia registrada.

No turno **46**, Marie percebe a privação de Lyra: `FamilyConcern 10487`, necessidade familiar de cuidado, recurso comida. Marie conhece diretamente esse fato, confiança 100. A primeira tentativa de pedir ajuda falha porque o interlocutor não conhece informação útil. Portanto, o cuidado existe como intenção, mas não há provisão comprovada nessa tentativa.

Lyra rouba recursos da cidade. Marie conserva conhecimento de crimes e desenvolve proteção pessoal. Uma denúncia no turno **106**, ligada ao crime **14464**, falha. Outra, no turno **118**, transmite o crime **21346**, ocorrido no turno 115, ao guarda John: `InformationShared 21822` e `ThreatReported 21823`. A evidência estava conhecida antes da decisão, confiança 100. O guarda responde a Lyra no turno **120**, evento **22173**. A resposta local está registrada; o catálogo não demonstra que esse evento específico foi causado exclusivamente pela denúncia de Marie.

No turno **155**, surge outro cuidado familiar, evento **28609**. Marie coleta alimento no **160** e procura Lyra no **166**. O encontro **30885** confirma Lyra com fome 100, sede 62 e HP 96. Coletar para o objetivo familiar não comprova que a ração foi entregue: não há `HelpGiven` nessa sequência selecionada.

Lyra morre no turno **198** por **sede**, com fome 62 e sem comida. O registro da morte informa última refeição no turno 197. Marie investiga no **202** um crime anterior, **24539**, cometido por Lyra no turno 133. A necessidade selecionada é **vingança/reparação pelo crime contra a cidade**, não busca de familiar desaparecido. Durante a investigação, encontra os restos: **38086**, seguido de `InvestigationPerformed 38088`.

Essa descoberta cria luto familiar. No turno **208**, Marie executa `remember_relative`: `Remembrance 39312`, fonte explícita **38086**, parentesco 94, conhecimento direto 100. Marie permanece viva ao final, HP 98, fome 44.

**Cadeia comprovada:** privação conhecida → cuidado; crime conhecido → proteção/denúncia e investigação; descoberta dos restos durante a investigação → conhecimento da perda → luto → visita de lembrança. É o melhor exemplo de objetivos familiares e sociais coexistindo. O sistema não possui uma emoção completa de “conflito de lealdades”, mas as decisões efetivamente envolvem ajudar e denunciar a mesma pessoa.

## S02 — Lyra Valerius assume o reino e continua procurando Bela

**Campanha espectador, autônoma.** Silas Valerius **1452**, governante; Bela Valerius **1455**, conselheiro; Lyra Valerius **1458**, estudante. Silas e Bela têm casamento 90; ambos possuem relação parental 100 com Lyra. Os dados usam `pai_de`/`filho_de` sem um campo suficiente para deduzir o gênero dos personagens.

Silas morre por fome no turno **430**, evento **83444**. A sucessão **83445**, no mesmo turno, coloca Lyra na referência de governante do reino **1209**. Sua profissão registrada continua estudante: posição política e profissão são campos diferentes. Isso é sucessão simples, já existente, sem uma disputa dinástica nova.

Lyra percebe a ausência de Bela no turno **485**, evento **94161**, usando a última observação de **329**. Procura no **491**, `FamilySearch 95157`, sem localizar Bela. No **548**, encontra Bela com fome 60, sede 63 e **1 HP**: evento **105966**. A necessidade é familiar, modo `missing`; não há consulta à localização global da pessoa.

No **1097**, outra ausência é percebida, **201247**, última observação **1061**. A busca **209637**, no **1148**, ainda não encontra Bela. O encontro **211206**, no **1157**, confirma fome 100, sede 66 e HP 4. Bela finalmente morre por fome no **1689**, evento **299125**, sem comida. Lyra está viva ao final, HP 100, fome 78.

**Cadeia:** morte do governante → sucessão; observações familiares envelhecidas → ausência percebida → buscas → encontros que confirmam fragilidade. A morte final de Bela é conhecida pelo auditor; não atribuo a Lyra conhecimento dessa morte sem um fato correspondente. Na campanha antiga, Bela morreu no turno 242 carregando comida. Agora vive até 1689 e morre sem alimento. Essa diferença pertence ao conjunto da correção e de suas consequências, não a um experimento que isole uma única regra.

## S03 — Uma ausência real produz 54 horas de procura

**Campanha mundo, autônoma.** Lyra Douran **254**, agricultor, e Marie Douran **257**, cozinheiro, casamento **100**.

No turno **469**, Lyra percebe que não vê Marie desde **433**: `AbsenceNoticed 87191`. Isso cria uma necessidade familiar de busca com localização previamente conhecida. Lyra procura no **517**, evento **95738**, mas não encontra Marie. No **523**, encontra a pessoa: **96790**, HP 100, fome 76, sede 57. O fato da ausência estava conhecido com confiança 100 antes das duas ações.

**Cadeia:** ausência baseada em observação → necessidade de localizar familiar → busca sem resultado → reencontro confirmado. Dura **54 horas** desde a percepção até o encontro. Não existe evidência de sequestro, fuga deliberada ou aventura fora da cidade.

Marie segue viva no final, HP 100, fome 82. Lyra morre muito depois, no turno **7603**, por sede. Essa morte posterior encerra sua trajetória, mas não apaga o desfecho bem-sucedido da busca anterior nem prova que Marie soube da perda. É uma história pequena, independente de uma tarefa de obter comida, embora continue vivendo num mundo sujeito à privação.

## S04 — Duas pessoas reagem de maneira diferente ao mesmo crime

**Campanha espectador, autônoma.** Aldren Douran **1597**, guarda, rouba a cidade **1574** no turno **84**, `ItemStolen 16126`. Elena Vale **1595**, comerciante, e John Vale **1592**, lenhador, desenvolvem necessidades de vingança/reparação referentes ao mesmo crime. Elena e John possuem amizade registrada; as relações de confiança mudam ao longo da campanha.

Elena investiga no turno **154**. Conhece o crime diretamente, confiança **100**, e procura no local conhecido. `PersonLocated 28377` encontra Aldren; `InvestigationPerformed 28378` registra investigação sem confronto. No **160**, Elena tenta pedir mais informação e falha. Nesse segundo momento, o fato original já não aparece em seu conhecimento capturado, embora a necessidade ainda o referencie.

John tenta denunciar no turno **175**, com o fato original conhecido por rumor, confiança **30**. A tentativa falha com a mensagem “Faltam informante, guarda presente ou evidência conhecida”. Esse resultado não permite escolher uma dessas condições como causa exclusiva. No **181**, pedir ajuda também falha por falta de informação útil.

**Cadeia:** mesmo crime → conhecimentos com qualidade diferente → investigação bem-sucedida de Elena e denúncia malsucedida de John. Coragem/vingatividade também diferem: Elena 40/85, John 62/81. Isso comprova reações diferentes, mas não prova que a personalidade sozinha causou a diferença; conhecimento, posição e momento também participam. Os três seguem vivos no final. Não houve vingança física nem punição final demonstrada nesse recorte.

## S05 — Uma denúncia chega ao próprio guarda suspeito

**Campanha jogador, episódio autônomo.** Elena **1595** e o guarda Aldren **1597** reaparecem nesta campanha, com outros acontecimentos.

No turno **5406**, Aldren comete o crime **879781** contra a cidade 1574. Elena conhece o fato diretamente, confiança 100, e seleciona `denounce` por necessidade de vingança. No **5428**, **883259** transmite o crime e **883260** registra a denúncia. O destinatário de ambos é **1597**, o próprio Aldren.

**Cadeia:** crime conhecido → reparação → escolha de guarda presente → denúncia ao suspeito. A ação funciona tecnicamente, mas o alvo social é incoerente para uma denúncia que deveria procurar investigação independente. Os dois permanecem vivos. Não há resultado que demonstre punição.

Este é um **bug social remanescente**, não uma história de justiça bem-sucedida. A escolha de autoridade não exclui adequadamente o próprio culpado. Não alterei esse sistema durante a correção alimentar.

## S06 — O interlocutor repete informação anterior à própria ausência

**Campanha jogador, episódio autônomo.** Arthus Luar **41**, cozinheiro; Iria Luar **38**, agricultor, casamento 94; Marie Stone **44**, guarda, interlocutor conhecido.

Arthus já havia localizado Iria no turno **328**, evento **63306**. No **400**, percebe uma nova ausência, **77503**, pois a última observação é do **364**. A busca no **405**, **78420**, não encontra Iria.

Arthus pede informação a Marie. Nos turnos **406**, **407**, **418** e **419**, ocorrem **78608**, **78815**, **80984** e **81150**. Todos transmitem o mesmo fato **63306**, do turno 328, anterior tanto à última observação quanto à ausência atual. As ações retornam “Informação transmitida”, mas o registro da necessidade no turno 419 continua sendo busca, com `searched=True` e bloqueio por falta de solução já observado.

**Cadeia:** nova ausência → procura → pedidos de informação → repetição de fato antigo sem avanço demonstrado. A troca é real; a utilidade para essa procura é insuficiente. O registro persistente de reputação impede reaplicar indefinidamente o mesmo favor, mas não impede o diálogo repetitivo. Arthus e Iria estão vivos ao final. Não afirmo que a ausência ficou sem solução durante os 10.000 turnos: o problema demonstrado está nesse episódio.

## S07 — Cael quer reconhecimento e seu trabalho muda a reputação

**Campanha jogador, episódio autônomo.** Cael Hammer **687**, comerciante; Bela Douran **684**, lenhador, referência da necessidade de reconhecimento. Não há evidência para chamar Bela de monarca ou conceder a Cael um título político.

Um encontro no turno **4508** é a fonte `encounter:684:4508` da necessidade `status`. O contexto pede **um feito**, `deeds_target=1`. Após concorrência com outras prioridades, Cael trabalha no turno **4652**, 144 horas depois: `ResponsibilityFulfilled 762383`.

Elena Luar **675**, Lyra Kars **678**, Bela e Cael conhecem o evento diretamente, confiança 100. O estado persistente de Bela contém o impacto do fato sobre Cael: etiqueta **responsável +4**, confiança adicional **0**. Elena recebe contribuição +2; Lyra, +4. A ação fecha a necessidade de reconhecimento.

**Cadeia:** encontro → desejo de reconhecimento → trabalho observado → fato compartilhado pelos presentes → reputação contextual registrada. É um efeito social comprovado, sem promoção, poder ou mudança de profissão inventados. Cael continua vivo no final, HP 44, fome 68. O desfecho do episódio é reconhecimento local; a fragilidade posterior também permanece visível.

## S08 — Ruan Kars troca de carreira para estabilizar renda

**Campanha espectador, autônoma.** Ruan Kars **1480**, inicialmente lenhador, aprende a cozinhar na cidade **1462**.

A primeira ação de formação capturada no turno **1263** seleciona necessidade **money**, motivo “Estabilizar renda baixa persistente”, meta 20 moedas e 1.200 horas de renda baixa. Não é uma personalidade recém-inventada nem uma ordem do jogador. A oferta local de formação passa pelas regras existentes de observação e disponibilidade.

`TrainingStarted 228807`, no **1263**, exige **34 horas de prática**. Há 14 registros de progresso, que podem contabilizar mais de uma hora de prática por atualização. No **1599**, `ProfessionChanged 284503` altera a profissão de lenhador para cozinheiro; a ação desse turno ainda está ligada à necessidade de renda.

**Cadeia:** dificuldade persistente de renda + oportunidade local → formação produtiva → prática distribuída → mudança de carreira. Foram **336 horas de calendário**, não 336 horas contínuas de aula. Não houve intervenção do jogador. Ruan segue vivo ao final, cozinheiro, HP 100, fome 74. A aquisição de profissão não comprova que deixou de ser pobre definitivamente.

## S09 — Mira Montes abandona dez formações antes de concluir a décima primeira

**Campanha espectador, autônoma.** Mira Montes **915**, mineiro, aprende a ser cozinheiro na cidade **900**.

O primeiro `TrainingStarted`, **130575**, acontece no turno **685**, com requisito **35 horas de prática**. A ação inicial está ligada a **food**, fome 92: a formação também podia ser um caminho legítimo de obtenção de recursos. No turno 4478, outra retomada está ligada a **money**. A trajetória não preserva uma única motivação imutável.

Os inícios são **685, 1107, 1801, 2186, 2522, 2719, 3044, 3578, 4028, 4478 e 5180**. Os abandonos são **1100, 1368, 2132, 2360, 2696, 2966, 3524, 3915, 4404 e 4917**. O catálogo conserva os 108 eventos do recorte: 11 inícios, 10 abandonos, 86 registros de progresso e a mudança de profissão.

No turno **5719**, `ProfessionChanged 924221` finalmente registra cozinheiro. Da primeira tentativa à conclusão passam **5.034 horas**, aproximadamente **210 dias**. A regra antiga encerra formação após mais de 168 horas sem prática, perdendo o progresso daquela tentativa. O log prova as interrupções; não prova que cada abandono teve exatamente a fome como causa.

**Cadeia:** oportunidade → prática → lacuna → abandono → nova tentativa, repetida dez vezes → conclusão. Existe continuidade longa do mesmo personagem, mas o conteúdo é bastante repetitivo. Mira termina viva, HP 92, fome 100. O sistema produziu uma trajetória identificável; ainda não produziu uma biografia rica em decisões profissionais variadas.

## S10 — Bela Solaris sai da população abstrata e se torna cozinheiro

**Campanha mundo, autônoma.** Bela Solaris **152312**, origem registrada “Habitante abstrato de Valria”, cidade **342**. Não possui parentesco gerado nesta materialização.

No turno **864**, `WorkerMaterialized 152314` registra conversão de um habitante abstrato em personagem persistente, após **72 horas de vaga**; o contingente abstrato restante é **414**. `TrainingStarted 152315`, no mesmo turno, exige **24 horas de prática**. É o mecanismo limitado da Fase 3, preservado nesta correção, com condições locais de recursos e contratação.

No **865**, a ação capturada seleciona **advancement**, domínio riqueza, meta 29 moedas. Já no **961**, a ação final de treinamento está ligada a **food**. O objetivo econômico e a sobrevivência podem utilizar a mesma atividade produtiva. `ProfessionChanged 167776`, no **961**, registra a conclusão após **97 horas de calendário**.

**Cadeia:** falta profissional persistente → conversão de residente existente → aprendizagem produtiva → profissão permanente. Não é nascimento, imigração nem cópia de um personagem morto. Bela permanece viva ao final, cozinheiro, HP 100, fome 80. É um exemplo de recuperação de capacidade local limitada, sem garantir recuperação econômica completa da cidade.

## S11 — O jogador aceita uma missão de água e não a conclui

**Campanha jogador.** Iria Luar **38**, agricultor; Arthus Luar **41**, cozinheiro, casamento 94; jogador Auditor **7676**.

Iria percebe privação de Arthus no turno **9512**, evento **1507116**. Na conversa do turno **9514**, cria pedido ao jogador: `HelpRequested 1507428`, quest **1507427**, tipo `family_care`, recurso exigido **water**, destinatário **41**, localização conhecida no contexto.

O comando `conversar 38` avança **9514→9515** e oferece o pedido. `aceitar 1507427` avança **9515→9516**. Depois o controlador automático do jogador continua com outras ações. Não há comando de entrega durante o intervalo ativo. `esperar 1`, de **9560→9561**, registra a quest como **failed**.

**Cadeia:** observação familiar → cuidado → pedido por conversa → aceitação do jogador → ausência de entrega → expiração. Iria e Arthus continuam vivos ao final, HP 100. Portanto, não há “família salva pela quest”. Há mudança real causada pela aceitação e pelo não cumprimento, com consequência formal de falha.

A política de teste foi preservada para comparação; ela reage melhor a pedidos simples de comida do que a essa tarefa familiar de água. Isso limita a qualidade da atuação do jogador automático. Não é um bug do jogo a missão exigir água e expirar sem entrega.

## S12 — Uma ração entregue pelo jogador é consumida na hora seguinte

**Campanha jogador.** Auditor **7676** entrega comida ao comerciante Arthus Valerius **24** no turno **100**: `HelpGiven 18732`, urgência 62.

A instrumentação registra `FoodAcquired` no mesmo turno, HP **90**, fome **62**, inventário após entrega **1 ração**. No **101**, `FoodConsumed` registra a mesma aquisição, `acquired_turn=100`, fome antes de comer **64**, HP 90, inventário após consumo **0**. Assim, o item recebido foi de fato utilizado: receber alimento e comer são consequências distintas.

Arthus conhece diretamente a ajuda. Seu registro persistente do fato atribui ao jogador **prestativo +6** e confiança **+5**. Arthus continua vivo ao final, HP 88, fome 62.

**Cadeia:** decisão pública de entregar → transferência real → posse → consumo posterior → efeito social persistente. É uma intervenção comprovada do jogador. Não podemos dizer que ela evitou uma morte certa: Arthus tinha 90 HP. O resultado interessante é a coerência entre ajuda, consumo e reputação, sem necessidade de criar uma catástrofe artificial.

## Avaliação da qualidade deste material

Os casos S01–S10 mostram decisões de NPCs sem intervenção direta do jogador nos encadeamentos apresentados; quatro deles vêm da campanha espectador e dois do mundo sem jogador. S11 e S12 têm intervenção pública registrada. S02 e S03 permitem acompanhar personagens por longos intervalos; S09 possui a trajetória profissional mais longa selecionada. S01 encadeia necessidades diferentes com fontes identificadas.

Busca familiar, reconhecimento e parte das mudanças profissionais possuem objetivos próprios além da sobrevivência. Entretanto, crimes, cuidado, perdas e formação frequentemente continuam ligados à comida ou à renda. Não classifico qualquer necessidade social como uma história economicamente independente.

Há material suficiente para estes **12 casos**, incluindo dois casos de incoerência social e uma quest fracassada. O conjunto não justifica afirmar que já existem grandes guerras, aventuras épicas, religião ativa ou relações emocionais profundas. O melhor resultado é continuidade causal local; as principais limitações são repetição, pouca transformação das relações e conclusões sociais curtas.
