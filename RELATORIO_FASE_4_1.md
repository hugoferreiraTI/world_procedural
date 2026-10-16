# Fase 4.1 — recuperação fisiológica e sobrevivência sustentável

Implementação e auditoria em 8 de outubro de 2026. Especificação: [fase_4_1.md](</home/hugo/Área de trabalho/procedrual/fase_4_1.md>). Versão `mvp-5-fase4.1`, SHA-256 `3206658685c769d82049bc62720e755b4a89c53840b26bc86c10342a459d32a6`. Base preservada: `mvp-5-fase4`, SHA-256 `74dee84cf3997e30f5b81840cf0c60f4edda6d053122e2300ca6bbf3c6b4da4e`. Todas as campanhas novas começaram em h 0, sem jogador e sem carregar save. A geração manteve `GENERATION_VERSION=mvp-4`, a mesma seed, elenco, geografia e população inicial. Após a primeira decisão diferente, os fluxos aleatórios e as histórias podem divergir.

## 1. Resumo executivo

A versão implementa a sequência adquirir → consumir → estabilizar → descansar → recuperar. Comer continua reduzindo fome, sem curar HP. Dano de privação passou a ser recuperável de forma distinta do dano físico, e HP baixo agora participa das decisões mesmo sem lesão.

Os 209 testes passaram, incluindo dez novos. A comparação controlada de 500 h precedeu uma única campanha nova de 5.000 h. No teste longo, houve 255 mortes, das quais 243 por fome ou fome+sede; antes eram 389 e 332, respectivamente. Consumo por dia de NPC vivo: 1,1846 → 1,1867 (0,18%).

**Resposta central:** há recuperação corporal real: 49 trajetórias registradas de refeição com HP<30 chegaram a HP≥80 em até 168 h. Nas janelas mais curtas, 0 personagens que entraram em HP <30 apareceram com HP >70 em pelo menos um prazo de 24/48/72 h. Há também fracassos e reincidência: 252 personagens com crises alimentares repetidas terminaram mortos. Portanto, o motor consegue recuperar um NPC; uma refeição isolada ainda pode apenas adiar a morte se a estabilidade não se sustentar. **A melhora é real, mas a recuperação rápida e duradoura ainda tem resultado parcial.**

Os invariantes estruturais passaram em todas as 50 verificações da campanha longa. Isso verifica integridade, não equilíbrio definitivo. Os resultados representam uma seed e uma execução, sem estimativa estatística de outros mundos.

## 2. Diagnóstico anterior

A suspeita do acúmulo de dano tinha base: havia descanso de até 3 HP/h, reduzido ou bloqueado por privação, mas faltava pressão específica de recuperação quando o HP baixo vinha de fome e não de lesões. O NPC podia obter comida, consumir, voltar à rotina e atravessar outra crise com a reserva de HP já reduzida. A necessidade alimentar normal começava em fome 50; decisões de background podiam demorar 12 h.

O caso confirmado de integração era Bela Douran #3139: em h 582, HP 1/fome 100, `steal_person` transferiu uma ração, mas a fome permaneceu 100; morreu em h 583 carregando-a. O relatório Vespera anterior registrou 329 mortes por fome, três por fome+sede, sete por sede e 50 por combate. Essa mortalidade não demonstra falta global de alimentos: distribuição, renda, conhecimento, tempo de deslocamento e fisiologia individual interferem no acesso.

## 3. `steal_person`

Roubo pessoal agora é fornecedor alimentar reconhecido pelo estimador comum. Em emergência fatal, a alternativa `person_meal` executa o roubo real e só consome se a transferência tiver sucesso. Quando há uma alternativa composta viável, a aquisição isolada equivalente não compete como se já fosse consumo. Se o alvo não possui ração ou o roubo não funciona, a cadeia falha sem criar alimento.

O teste 01 confirma HP 1/fome 100, perda de uma ração pelo alvo, consumo pelo ator, fome 100→60 e HP 1 preservado no fechamento seguinte. HP não aumenta com a refeição. Na campanha longa, houve 393.656 refeições e 0 mortes por fome/fome+sede carregando ração. Essa última contagem é observação global; o teste controla especificamente o roubo pessoal vital.

## 4. Pipeline comum de aquisição alimentar

`ACQUISITIONS` informa quais ações fornecem comida: compra, coleta, roubo municipal/pessoal, pedido de ajuda, trabalho por comida e serviço temporário. `MEALS` mapeia as cadeias reais de aquisição e refeição. Todas as alternativas são enumeradas, inclusive as da Fase 4, antes de montar e avaliar essas cadeias. O estimador inclui rota, tempo de aquisição, intervalo até consumir e margem de sobrevivência.

Toda transferência real passa pelo serviço de itens e pelo observador de inventário: ajuda, pagamento e restituição não geram comida adicional. Restituição recebida e presentes são entradas passivas; não recebem uma ação inventada de “pedir restituição para curar”. A ração recebida torna-se comida possuída e pode ser consumida na próxima decisão. Ajuda solicitada ao jogador não é tratada como transferência garantida.

Aquisição fora de emergência continua separada da refeição. Comprar reserva não obriga o NPC a comer imediatamente. Comer só remove a ração que existe no inventário e aplica a redução normal de fome.

## 5. Novo limiar de refeição

O limiar centralizado caiu de 50 para 35. Em fome 36 existe a opção `eat`, mas ela pode perder para uma necessidade mais urgente. Em fome 15 não é criada necessidade de refeição. A refeição reduz até 40 pontos de fome; o ganho útil depende da fome presente.

A antecipação não significa que todas as refeições aconteçam em 35: a média longa foi 74,26, contra aproximadamente 83,38 antes. A curva, a atividade atual, a água, a reserva, a rota e outras necessidades continuam competindo. A média antiga vem do diagnóstico de consumo, que inclui 50 usos de comida em socorro; a nova média conta `FoodEaten` diretamente. A comparação curta usa o mesmo observador nas duas versões.

## 6. Curva de prioridade alimentar

Pressão base configurada: fome 35→20; fome 40→40; fome 60→70; fome 80→100. Entre os pontos há progressão linear. Idade da necessidade e modificadores existentes continuam atuando. Abaixo de 35 não há pressão de refeição normal. A faixa 35–40 permite aproveitar oportunidade; 40–60 é necessidade normal; 60–80 é alta; 80+ ou margem vital curta ativa emergência.

O limiar normal não foi transformado em prioridade 100. Reserva conserva sua avaliação de cobertura, déficit, preço observado, oportunidade presente e próxima reposição conhecida. Nenhuma mudança foi feita no crescimento da fome/sede ou no tamanho da redução por refeição.

## 7. Need de recuperação

`recovery` surge abaixo de 80 HP independentemente da lesão. A pressão base é `min(95,25+80−HP)`: aproximadamente 45 em HP 60,65 em HP 40,85 em HP 20 e 95 no estado mais grave. O contexto registra HP, dano recuperável e dano físico restante. Ao atingir 80, a necessidade pode ser satisfeita; não exige hospitalização até 100.

Se alimentação ou água ainda não estiverem suficientemente controladas, a necessidade reutiliza as soluções alimentares/hídricas existentes. Sem adversário ativo, pode voltar à própria casa e descansar; lesão relevante permite buscar tratamento e pedir socorro local. Com adversários, respostas defensivas continuam no sistema de conflitos. HP<20 pode interromper trabalho e objetivos não vitais para descanso/tratamento/água, sem apagar a necessidade de comida ou a defesa.

Na campanha longa: 5.098 seleções de recuperação, 3.392 satisfações e 6.706 esgotamentos do registro de dano por privação. São ocorrências, não necessariamente pessoas únicas. Descanso causado por cansaço também pode recuperar HP; essas contagens não abrangem toda cura.

## 8. Origem do dano

| Origem | HP realmente perdido na campanha |
| --- | --- |
| Fome | 176.552 |
| Sede | 422 |
| Fome e sede simultâneas | 670 |
| Combate | 89.833 |

A perda simultânea é contabilizada uma vez em `both`, sem duplicar fome+sede. O dano de combate registra a perda efetiva, limitada ao HP existente; a fórmula e a variação do ataque permaneceram as mesmas. 463 personagens sofreram tanto privação quanto combate em algum momento; essa contagem de trajetórias mistas não soma um quinto tipo de dano.

## 9. Dano recuperável por privação

`recoverable_deprivation_damage` acumula somente a perda real causada por fome, sede ou ambas. Um golpe fisiológico nominal de 5 em alguém com HP 1 registra 1. O registro nunca ultrapassa o HP ausente e é persistido no save. A barra de vida permanece única.

Cura fisiológica debita esse registro e aumenta HP na mesma quantidade. Na campanha foram recuperados 148.801 HP de privação. A contagem pode superar o HP máximo de um NPC ao longo de meses porque novas crises voltam a causar dano; ela não significa excesso de HP em uma ação.

O balanço global fechou exatamente: 177.644 HP perdidos por privação − 148.801 recuperados = 28.843 ainda registrados em vivos e mortos. Também fechou para todo o HP: 267.477 dano − 233.630 cura = 33.847 HP ausentes no elenco completo. Fonte: [BALANCO_GLOBAL_HP.json](</home/hugo/Área de trabalho/procedrual/reports/fase_4_1/BALANCO_GLOBAL_HP.json>).

## 10. Dano físico

Combate não aumenta o registro de privação. O dano físico ainda depende da cura normal de descanso/tratamento, sob as restrições antigas de fome/sede e ferimentos. Socorro continua limitado e consome provisão e água reais. Alimentar-se não cura espada.

Foram recuperados 84.829 HP físicos ao todo; 84.753 foram observados em descanso. A diferença corresponde ao socorro registrado pela função comum; não deve ser apresentada como cura fisiológica rápida. O teste misto 30 de fome+20 de combate confirma que a parcela rápida se limita aos 30, enquanto os outros 20 usam a recuperação física normal.

## 11. Recuperação por descanso

| Condição da maior fome/sede | Cura rápida de privação em local seguro |
| --- | --- |
| Até 50 | 8 HP/h |
| 51–70 | 4 HP/h |
| 71–80 | 1 HP/h |
| Acima 80 | 0 HP/h de cura rápida |

O local seguro inicial é a própria casa, sem adversários ativos. Chegar lá exige deslocamento real; não há teleporte. A cura física normal continua sendo até 3 HP/h, com as reduções antigas. `recover_hp` usa um único orçamento, `max(cura_normal,cura_fisiológica)`, e divide esse orçamento entre as parcelas; não soma 8+3 indevidamente. A cura rápida não ultrapassa o dano de privação registrado. A cura normal pode também reparar privação quando as condições antigas permitem, inclusive fora da condição de cura rápida.

A recuperação ocorre no descanso executado, sem regeneração passiva universal. Ela pode parar para beber/comer e recomeçar depois. Tratamento limitado segue a mesma função para manter a consistência entre HP ausente e registro recuperável.

O motor conserva a agregação existente de atividade pelo intervalo de LOD. Uma execução de descanso pode representar várias horas acumuladas, portanto uma linha pode mostrar +24 HP sob taxa de 8 HP/h; isso não é uma segunda função de cura. A condição usada é a observada na execução, sem reconstituir as condições de cada hora intermediária. Essa aproximação temporal foi preservada e precisa ser lembrada ao interpretar os quadros clínicos.

## 12. Integração com fome/sede

Com fome/sede acima 50, o plano de recuperação procura primeiro estabilizar recursos; se a sede é dominante, prioriza água. Aquisição real e consumo permanecem separados. Necessidades vitais críticas conservam a prioridade e o desempate anteriores, e comida possuída em emergência mantém a opção de consumo.

Aumentos por hora e dano progressivo da privação não foram reduzidos. A promoção de LOD antecipa decisões, mas a fisiologia continua passando uma vez por hora. Um NPC pode morrer quando não existe solução conhecida e viável a tempo, inclusive diante de duas necessidades vitais simultâneas. Isso é diferente de curar HP simplesmente porque uma compra aconteceu.

## 13. Integração com combate

| Evento/ação | Fase 4 anterior,5.000 h | Fase 4.1,5.000 h |
| --- | --- | --- |
| Ataques executados | 27.623 | 17.168 |
| Fugas bem-sucedidas (eventos) | 5.648 | 3.822 |
| Rendições | 1.545 | 1.551 |
| Mortes por combate | 50 | 9 |

HP crítico adiciona penalidade à Utility de ataque voluntário, ameaça e perseguição. Defesa recebe penalidade menor; fuga e rendição já consideravam HP. Foram observados 13 ataques iniciados com HP<20, de 17.168. Não há medição equivalente no longo antigo: no controle de 500 h foram dois antes e zero depois. Essas diferenças também refletem fome, emoções, encontros e trajetórias divergentes; não atribuem toda mudança à cura. Não houve rebalanceamento de dano/armas/defesa.

## 14. Integração com LOD

Personagens comuns em casa podiam decidir a cada 12 h. Ao cruzar fome 35, passam a decidir no máximo a cada 3 h; fome alta mantém decisões horárias como antes. HP<30 também força o intervalo de 1 h. Quando saem dessas condições, a mesma agenda retoma o LOD correspondente à categoria/local/contexto.

A promoção altera o intervalo da agenda existente; não executa uma segunda decisão por callback. O teste 10 verifica promoção, interrupção de trabalho por recuperação crítica e avanço normal. O save/load determinístico inclui estado da agenda e campos novos. No mundo longo, cada hora de vida entra apenas uma vez no denominador do consumo.

## 15. Desespero

O valor continua limitado a 0–100, mas contribuições agora distinguem privação, pobreza, luto, violência e perseguição conhecida. Valores sem fonte específica ficam em `unclassified`; suporte social e decaimento antigo mantêm as parcelas compatíveis com o total. Humilhação e isolamento não receberam decomposição completa nesta fase: seus estados/fatos continuam no sistema anterior.

Condição material estável exige fome/sede≤50, HP≥60 ou melhora recente, casa segura, ausência de perseguição conhecida e ao menos uma ração e água possuídas. Depois de seis horas observadas nessa condição, as parcelas de pobreza/privação podem cair gradualmente a 0,25 por hora cada. Uma refeição não dá queda fixa de 30. Luto ativo e grievances não são apagados pela melhora material.

A média de desespero entre vivos foi 91,68 antes e 89,25 depois. Houve 1.224,06 pontos de redução material específica somados em toda a população. A média também recebe suporte, perdas e decaimento anteriores; não mede apenas essa nova regra. O tempo estável usa os intervalos observados pelo LOD, sem reconstituir cada hora intermediária de apoio/segurança subjetiva.

| Fonte registrada | Vivos com parcela positiva | Parcela média entre todos os vivos |
| --- | --- | --- |
| poverty | 1.432 | 66,66 |
| deprivation | 1.409 | 20,00 |
| grief | 21 | 0,15 |
| violence | 521 | 0,53 |
| pursuit | 623 | 1,90 |
| unclassified | 0 | 0,00 |

O requisito material usa recursos possuídos e segurança local, portanto existir comida no município ou ter acabado de comer não assegura várias horas estáveis com comida e água em reserva. Pressões persistentes podem continuar acrescentando desespero. A tabela é o estado final das parcelas remanescentes, depois de reduções, e não o total histórico de todas as causas. A contagem de parcelas positivas ignora resíduos numéricos menores que 0,000001.

## 16. Testes direcionados

| Teste | Cenário | Verificação |
| --- | --- | --- |
| 01 | Roubo pessoal vital | Transfere e consome ração real antes de fisiologia fatal; não cura HP |
| 02 | Compra+refeição | Dinheiro/estoque reais; consumo salva sem restaurar HP |
| 03 | Fome 36 | Eat válido, prioridade normal e sem emergência artificial |
| 04 | Fome 15 | Não cria refeição; reserva continua separada |
| 05 | Perda por privação | Registra só HP realmente perdido, inclusive sobre-dano nominal |
| 06 | Recuperação e desespero | Descanso retira estado grave, Need termina e melhora material gradual preserva luto |
| 07 | Dano de combate | Não entra no registro rápido; descanso breve segue cura física |
| 08 | Dano misto | 30 privação+20 combate; parcela rápida limitada e sem orçamento duplicado |
| 09 | Persistência | Campos novos e Need sobrevivem ao save/load com continuação exata |
| 10 | LOD/interrupção | Antecipação e recuperação crítica usam a agenda existente |

Todos os dez passaram. A suíte completa de 209 testes passou em 61,79s. Os quatro cenários antigos que inicialmente falharam tinham pressupostos afetados pela refeição antecipada e pelas alternativas reais de ajuda. Foram ajustados o limiar, o valor útil da refeição, o indicador de autonomia em vez de um estoque específico e a ausência de ajudantes no cenário sem rota conhecida. Não foram suprimidas falhas do motor.

Logs: [testes_direcionados.txt](</home/hugo/Área de trabalho/procedrual/reports/fase_4_1/testes_direcionados.txt>), [testes_completos.txt](</home/hugo/Área de trabalho/procedrual/reports/fase_4_1/testes_completos.txt>), [testes_primeira_execucao.txt](</home/hugo/Área de trabalho/procedrual/reports/fase_4_1/testes_primeira_execucao.txt>). A quantidade de regressões novas permaneceu dentro dos 8–12 solicitados. Save/load e conservação material são cobertos pela suíte; não houve nova bateria de dezenas de testes para esta etapa.

## 17. Auditoria curta

| Indicador em 500 h | Anterior | Nova |
| --- | --- | --- |
| Mortes totais | 50 | 23 |
| Fome ou fome+sede | 41 | 22 |
| Sede isolada | 0 | 1 |
| Combate | 9 | 0 |
| Mortes de fome com ração | 0 | 0 |
| Fome média ao comer | 80,09 | 63,89 |
| HP médio ao comer | 92,81 | 97,08 |
| HP médio dos vivos em 500 h | 85,42 | 92,33 |
| Vivos com HP<30 em 500 h | 139 | 66 |
| Desespero médio dos vivos | 70,00 | 43,92 |
| Raç./dia de NPC vivo | 1,1429 | 1,1641 |

Mesma seed Vespera-47, perfil completo, sem história prévia:1.776 persistentes,4.461 abstratos,75 localidades,seis reinos. Os núcleos foram executados separadamente com o mesmo observador passivo. A comparação curta terminou antes de iniciar a longa. Consumo subiu 1,86%; não dobrou. Mercado vazio na última amostra diária: 1→0. Não houve aumento artificial de produção para compensar antecipação.

A nova campanha curta restaurou 8.294 HP de privação, selecionou recuperação 271 vezes e registrou 327 esgotamentos do registro recuperável. As janelas de 72 h ainda tinham 47 episódios em HP<30,13 mortes,21 em 30–50 e quatro em 50–70; nenhum acima 70. Isso motivou acompanhamento longo, sem calibrar parâmetros para uma taxa desejada de mortes.

Fontes: [resumo.json](</home/hugo/Área de trabalho/procedrual/reports/fase_4_1/curta_base/resumo.json>), [resumo.json](</home/hugo/Área de trabalho/procedrual/reports/fase_4_1/curta_nova/resumo.json>). O contador antigo de máximo de HP após refeição teve erro no observador; não é usado para decidir sucesso. A correção e a contagem válida de cura medida estão nos arquivos `correcao_observador.json` de ambas as pastas.

## 18. Auditoria longa

| Indicador | Vespera antiga | Nova Fase 4.1 |
| --- | --- | --- |
| Duração | 5.000 h | 5.000 h |
| NPCs vivos | 1.387 | 1.521 |
| Mortes totais | 389 | 255 |
| Fome ou fome+sede | 332 | 243 |
| Fome média ao consumir | 83,38 | 74,26 |
| HP médio ao consumir | 85,89 | 94,03 |
| HP médio dos vivos | 87,51 | 94,51 |
| Vivos com HP<30 | 104 | 23 |
| Desespero médio | 91,68 | 89,25 |

Uma campanha global nova de 5.000 h, após o controle de 500 h e a suíte aprovados. Não carregou o save Vespera antigo. Núcleo congelado antes de iniciar; o SHA foi conferido novamente ao terminar. As primeiras 500 h repetiram os indicadores do teste curto, mostrando que a ampliação passiva dos registros não mudou a trajetória do motor.

Tempo de simulação: 2.379,24s, sem contar a gravação do save ao final; pico de memória registrado até a medição anterior à gravação:538,32MiB. A exportação e a recarga de validação não estão incluídas nesse pico. Amostras fisiológicas a cada 100 h e economia a cada 24 h. Eventos e decisões clínicas foram exportados sem executar decisões adicionais. Manifesto: [manifesto.json](</home/hugo/Área de trabalho/procedrual/reports/fase_4_1/global_5000h/manifesto.json>); resumo:[resumo.json](</home/hugo/Área de trabalho/procedrual/reports/fase_4_1/global_5000h/resumo.json>); save:[save_final.json](</home/hugo/Área de trabalho/procedrual/reports/fase_4_1/global_5000h/save_final.json>).

Depois da campanha, o save exportado foi recarregado somente para verificar formato, versão, invariantes e total do registro de dano; nenhuma hora adicional foi simulada nessa conferência. Resultado: [save_verificado.json](</home/hugo/Área de trabalho/procedrual/reports/fase_4_1/save_verificado.json>). A campanha foi gerada do zero e os resultados históricos não foram carregados para iniciá-la.

A longa anterior não coletou as novas parcelas de cura nem as janelas 24/48/72 h. Essas colunas não foram preenchidas por estimativa. O controle de 500 h fornece a comparação equivalente das janelas. A comparação longa é descritiva: mesma população inicial, regras diferentes, sequência de escolhas subsequentes divergente.

## 19. Consumo alimentar

| Fome na refeição | Anterior 500 h | Nova 500 h | Nova 5.000 h |
| --- | --- | --- | --- |
| below 30 | 0 | 0 | 0 (0,00%) |
| 30-40 | 0 | 198 | 567 (0,14%) |
| 40-60 | 2.591 | 18.636 | 53.271 (13,53%) |
| 60-80 | 12.458 | 16.958 | 185.690 (47,17%) |
| 80+ | 26.944 | 7.163 | 154.128 (39,15%) |

A campanha nova consumiu 393.656 rações em refeições de personagens persistentes, distribuídas em 7.961.263 horas de vida. Fórmula: `FoodEaten/(soma_das_horas_vivas/24)` = 1,1867. A antiga tinha 375.502 refeições e 7.607.788 horas de vida, obtidas a partir do elenco inicial e horários de morte, dando 1,1846. Não houve materialização de novos NPCs no denominador antigo; se existisse nascimento/materialização, seria necessário incorporar o horário de entrada.

Contar apenas população inicial×duração subestimaria consumo por sobrevivente, porque parte do elenco morre. Alimentos abstratos e provisões gastas no socorro não contam como `FoodEaten`; são outros usos físicos de comida. O diagnóstico de nutrição antiga também registrava socorro, motivo da pequena diferença entre médias históricas e refeições.

Variação normalizada:0,18%. Refeições abaixo 40 constituem 0,14%. Não se alterou produção para esconder eventual desperdício. A refeição em 35 pode desperdiçar até 5 dos 40 pontos de capacidade; as contagens e o consumo permitem acompanhar esse custo.

## 20. Economia

| Indicador | Controle antigo 500 h | Controle novo 500 h | Nova 5.000 h |
| --- | --- | --- | --- |
| Produção acumulada de comida na última amostra diária | 38.548 | 42.853 | 275.764 |
| Estoque municipal nessa amostra | 9.329 | 11.159 | 16.342 |
| Mercados vazios nessa amostra | 1 | 0 | 0 |
| Preço médio de uma ração | 2,27 | 2,29 | 2,00 |
| Compras de comida (transações) | 19.859 | 18.778 | 129.599 |
| Unidades compradas para reserva | 10.232 | 18.643 | 51.147 |
| Compras que deixaram segunda ração | 4.659 | 9.086 | 22.607 |

As últimas amostras diárias são h 480 nos testes curtos e h 4992 na longa; não são exatamente o estoque de h 500/h 5.000. Na longa houve 48 observações de município sem comida em 15.600 observações município/dia. Produção antiga em h 5.000:254.707 rações; sua amostragem não é idêntica à nova diária.

Compra/transferência, matéria-prima, preparo e remoção por consumo continuam nos serviços antigos. Reserva normal permanece duas rações; até seis somente conforme a avaliação existente de viagem conhecida. Nesta auditoria sem jogador, as chamadas de compra dos NPCs usam somente comida, portanto `ItemBought` conta transações alimentares. Não equivale ao total de unidades: compras de reserva podem ser em lote. `ReservePurchaseUnits` mede unidades reais desse caminho específico e não inclui todas as compras individuais nem doações, coleta ou pagamento. O total de unidades de todas as compras não foi exportado separadamente.

Preservar estoque global não garante acesso econômico de cadaNPC. Uma localidade pode terminar abastecida enquanto alguém distante, pobre ou sem alternativa conhecida morre. Esse limite continua sendo material e decisório, e deve ser investigado por trajetórias, sem corrigir com dinheiro/comida gratuitos.

## 21. Mortalidade

| Causa | Anterior 5.000 h | Nova 5.000 h |
| --- | --- | --- |
| hunger | 329 | 243 |
| thirst | 7 | 3 |
| both | 3 | 0 |
| combat | 50 | 9 |

Fome/fome+sede respondem por 95,29% das mortes novas; privação incluindo sede por 96,47%. Esses percentuais mudam também quando há mais/menos mortes violentas. A predominância alimentar por si só não mostra que a cura falhou nem que o acesso foi resolvido.

Mortes por fome carregando ração: 0. O arquivo de resumo registra ID, hora, HP, fome/sede, objetivo final, recursos e dano por origem nas mortes fisiológicas. Quando não há alimento possuído, deve-se investigar alternativas disponíveis a tempo; o agregado não prova ausência de alimento na região nem impossibilidade de ajuda.

A causa registrada identifica o dano que encerrou a vida; não descreve sozinha todo o dano anterior. Das 243 mortes por fome/fome+sede,32 ainda tinham parcela física ausente no HPno momento da morte. Nas demais, o HPausente era integralmente registrado como privação. Essa separação evita chamar de exclusivamente alimentar uma trajetória que também acumulou dano de combate não recuperado.

## 22. Reincidência de crises

Crise é uma entrada observada em fome≥90 após estar abaixo 90. A refeição é ligada à crise mais recente; uma nova entrada fecha a sequência anterior. Foram observadas 63.490 crises em 1.524 personagens; 1.436 tiveram mais de uma. 63.186 episódios tiveram refeição posterior registrada; 31.379 tiveram cura de descanso medida após essa refeição, e 30.254 tiveram HP posterior maior que o da primeira refeição.

Entre as entradas recorrentes, o intervalo médio foi 70,34 h. 252 personagens com crises repetidas terminaram mortos. O número de crises mede também a amplitude do período e a população que sobrevive para repetir; não deve ser interpretado como uma taxa independente da exposição.

Uma recuperação curta não impede retorno à fome 90. O critério clínico útil é observar se a vida realmente sobe entre crises e se a pessoa permanece viva/ativa depois. Cura medida é diferente de melhora líquida: se houver novos danos após comer, o NPC pode recuperar alguns pontos e ainda ficar abaixo do HP de partida. Dados por ID: [crises_por_npc.json](</home/hugo/Área de trabalho/procedrual/reports/fase_4_1/global_5000h/crises_por_npc.json>).

## 23. Recuperação de HP

| Prazo | Observados | Morreu | HP <30 | HP 30–50 | HP 50–70 | HP >70 |
| --- | --- | --- | --- | --- | --- | --- |
| 24 h | 1.301 | 36 | 983 | 279 | 3 | 0 |
| 48 h | 1.294 | 52 | 684 | 546 | 12 | 0 |
| 72 h | 1.289 | 87 | 571 | 596 | 35 | 0 |

Cada linha acompanha entradas em HP<30. Uma pessoa pode entrar várias vezes; portanto são episódios, não indivíduos independentes. Os prazos que ultrapassaramh 5.000 ficaram censurados (37 janelas) e não foram contados como mortes nem recuperações. Os limites são <30,30≤HP<50,50≤HP≤70 e HP>70.

Pessoas únicas com pelo menos uma janela>70:0. Janelas incluem todas as causas de HP baixo; a história clínica e o registro por origem ajudam a distinguir privação e combate. No controle de 500 h, a versão anterior não teve nenhuma janela>70 em 72 h; a nova também não, embora tivesse menos episódios graves. **Na longa também não houve HP acima 70 nas observações de 24/48/72 h.** São fotografias nos prazos, não acompanhamento de todos os picos intermediários. A cura disponível e o resultado corporal geral melhoraram, mas a saída rápida do colapso ainda não foi demonstrada por essas janelas.

Fontes: [janelas_recuperacao.json](</home/hugo/Área de trabalho/procedrual/reports/fase_4_1/global_5000h/janelas_recuperacao.json>). A cura não acontece só ao abrir `recovery`: descanso por cansaço e tratamento também podem recuperar. Não foi criado um teto de mortalidade para calibrar esses resultados.

Na busca das 49 trajetórias completas, o menor intervalo registrado entre uma refeição em HP<30 e uma ação de cura que levou a HP≥80 foi 102 h. A busca encontrou 0 dessas trajetórias completas dentro de 72 h. Essa medição parte da refeição, enquanto as janelas acima partem da entrada em HP<30; os denominadores são diferentes.

## 24. Histórias reais

Foram encontrados 49 personagens com refeição em HP<30 e ação de cura levando a HP≥80 em até 168 h; 5 trajetórias foram detalhadas. O catálogo contém valores antes/depois, ações reais, horários e eventos de ajuda/migração quando próximos. Há 224 mortes por fome ligadas a refeição crítica anterior no recorte; três exemplos são usados como contraponto.

226 IDs que morreram na campanha antiga estão vivos nesta. É evidência de trajetórias diferentes com o mesmo elenco inicial, sem afirmar que cada resultado foi causado exclusivamente pela cura. Vínculo familiar só é afirmado quando consta do elenco inicial. A busca encontrou um caso verificável de familiar ajudando um destinatário com HP baixo no recorte disponível.

Leitura: [HISTORIAS_REAIS.md](</home/hugo/Área de trabalho/procedrual/reports/fase_4_1/HISTORIAS_REAIS.md>). Evidências: [evidencias_historias.json](</home/hugo/Área de trabalho/procedrual/reports/fase_4_1/evidencias_historias.json>). Combate, proteção, rendição, ajuda, migração e sucessão continuam produzindo eventos; isso não implica que todos os arcos já tenham qualidade narrativa completa.

| Consequência social | Eventos na campanha nova |
| --- | --- |
| HelpGiven | 3.822 |
| FirstAidGiven | 38 |
| ProtectionGiven | 4.965 |
| MigrationStarted | 967 |
| MigrationArrived | 922 |
| ResidentMoved | 920 |
| SuccessionChanged | 10 |

## 25. Limitações

- Uma seed longa não demonstra robustez para todos os mundos ou todos os perfis de jogador. Não houve novo ensaio como jogador nesta etapa; o núcleo compartilhado e os cenários controlados cobrem a integração, e a auditoria longa é global sem jogador.
- Segurança inicial significa própria casa sem adversário ativo. Não há avaliação nova de abrigo coletivo, enfermaria ou ameaça distante desconhecida; o NPC não recebe conhecimento onisciente.
- HP≥80 pode satisfazer recuperação mesmo com pequena parcela recuperável restante. Esse limite evita descanso prioritário eterno; não garante retorno imediato a 100.
- Desespero por humilhação/isolamento não tem decomposição completa. Estabilidade material é observada nos intervalos de LOD, e não uma prova de segurança constante em cada hora intermediária.
- Socorro ainda exige lesão; não foi acrescentado sistema médico para desnutrição nem cuidador com tratamento contínuo. Pedidos existentes, comida/água e descanso resolvem parte desse caminho.
- Estoque regional, acesso individual e continuidade de renda são problemas diferentes. A fase não criou crédito/dinheiro/comida para remover dificuldades materiais.
- Contagens de crises/janelas repetem pessoas; resultados censurados e sobreviventes finais têm exposição diferente. Não calcular intervalos estatísticos fingindo independência.
- Observador clínico registra todas as ações com HP<30, recuperação selecionada e recortes de retorno 72 h após HP 80; outras ações normais são amostradas. Ausência de uma história no catálogo não prova ausência no mundo.
- Relatórios/saves históricos foram preservados. O carregador recusa versões anteriores; não houve migração automática de saves sem a origem antiga de dano.

## 26. Bugs encontrados

1. **Corrigido: aquisição pessoal fora da semântica alimentar.** `steal_person` podia vencer consumo viável e deixar fome 100 com a ração recém-adquirida; passou a participar do pipeline e da cadeia vital.
2. **Corrigido: falta de necessidade para HP baixo sem lesão.** Dano fisiológico acumulado não recebia pressão própria suficiente; `recovery` independe de ferimento.
3. **Corrigido: ausência de registro separado da privação.** A cura forte precisava distinguir a parcela recuperável do combate; origem real e debitação agora são persistidas e verificadas.
4. **Corrigido: decisões tardias na faixa normal e HP crítico.** A agenda existente promove refeições e recuperação; não há callback executando ação duplicada.
5. **Corrigido no observador, antes da longa:** máximo de HP pós-refeição do teste curto iniciava com HP anterior. O erro afetava um indicador derivado, sem mudar o motor. Os registros curtos originais foram mantidos e anotados; a longa inicializa o máximo no HP da primeira refeição.

Não foi observada morte por fome carregando comida nesta campanha; isso reforça a regressão corrigida, sem garantir ausência em todas as condições futuras.

**Permanece uma falha de integração pré-existente:** `forage_meal` que falha bloqueia esse nome, mas `forage` pode tentar o mesmo fornecedor na hora seguinte. Mira Bruma #1922 falhou por coleta esgotada em h 306 e repetiu em h 307; morreu em h 310 sem comida. Evitar a repetição não prova que existia alimento alternativo capaz de salvá-la. O núcleo foi conservado durante a longa; a proposta limitada é compartilhar o bloqueio quando a falha ocorreu na aquisição, distinguindo-a de falha de consumo. Evidência e causa: [BUGS_REMANESCENTES.md](</home/hugo/Área de trabalho/procedrual/reports/fase_4_1/BUGS_REMANESCENTES.md>), [evidencia_falha_alias.json](</home/hugo/Área de trabalho/procedrual/reports/fase_4_1/evidencia_falha_alias.json>).

Reincidência, pobreza, desespero elevado e história social repetitiva são limitações medidas, não automaticamente bugs com causa única demonstrada. Problemas sociais já listados na auditoria anterior — duplicação de casos após resolução, interpretação de medo na reputação e residência associada à chegada — não foram reabertos como expansão desta fase. Não foram declarados corrigidos por terem ocorrido menos vezes.

## 27. Recomendação para próxima fase

A recuperação fisiológica existe, diferencia origem, compete por ações e aparece em trajetórias reais. O limiar alimentar antecipado passou pelas regressões, e o consumo mudou 0,18% por dia de NPC vivo. A implementação passou pelos testes; o resultado de sobrevivência sustentável é **parcial**, porque nenhuma janela crítica apresentava HP>70 nos prazos de 24/48/72 h e 224 mortes por fome tinham refeição crítica anterior registrada. Não recomendo tratar o ciclo de colapso como encerrado nem avançar com base somente na redução de mortes.

Antes de expandir conteúdo social, usar os episódios que comeram em HP baixo e morreram depois para localizar a próxima quebra concreta: impossibilidade econômica, trajeto, bloqueio por necessidades concorrentes ou ausência de descanso materialmente viável. A evidência desta campanha deve orientar mudanças pequenas, não novos sistemas amplos para mascarar o ciclo.

Uma hipótese específica a verificar é a competição de renda/reserva com recuperação depois que o HPpassa de 20–30. A necessidade de renda pode atingir prioridades altas por idade, diligência, desespero e reveses; reduzir aUtility do trabalho não muda a ordem das necessidades. O motor escolhe a primeira necessidade prioritária com solução viável. Isso pode deixar recuperação esperando mesmo com uma alternativa de descanso disponível. É uma inferência do fluxo de decisão, não prova de que explica todos os 224 desfechos.

A próxima correção limitada recomendada é unificar o bloqueio de tentativas equivalentes após falha real do fornecedor alimentar. Ela deve ser validada separadamente; a campanha presente mede o núcleo congelado anterior a essa melhoria proposta.

Se a próxima fase mexer em sobrevivência/economia, preservar o conjunto de dez regressões e comparar consumo, reincidência e janelas de HP novamente. Revisar os problemas sociais conhecidos separadamente e acrescentar cuidados/abrigo somente com objetivos e recursos reais. O teste já responde à pergunta central: **o NPC pode sair do colapso e continuar sua vida, mas só obter uma refeição não garante recuperação sustentável.**
