# RELATÓRIO TÉCNICO — Fase 5.4

## Resultado e alcance

A Fase 5.4 foi adaptada ao motor existente. A geração padrão passa a quatro reinos, com capital, quatro outras cidades e seis a oito vilas por reino. Conhecer o destino já não autoriza uma viagem entre localidades: o agente precisa das conexões, de condição física e de mantimentos reais, ou acompanhar um guia presente.

Campanha natural: **Arandor-54**, criada do zero, sem jogador, **200 horas**, regras `mvp-11-fase5.4`. O limite de 200 horas segue o pedido mais recente do usuário, prevalecendo sobre as 350 horas sugeridas no documento. Não houve seleção de seeds para produzir resultados desejados. Esta campanha mostra integração e comportamentos de curto/médio prazo; não demonstra equilíbrio econômico ou raridade em milhares de horas.

## Arquitetura preservada

Os dados continuam em dataclasses de `models`; o `Engine` coordena serviços; decisões seguem Need → alternativas → Utility → Goal → ação. Navegação, índice espacial, eventos, conhecimento, itens, sociedade, fé e JSON continuam sendo os mesmos serviços do projeto. Foram adicionados `geography.py` e `access.py`, ligados a esse fluxo, sem outro motor de agentes, sistema de combate ou arquitetura de persistência.

`Route`, `RouteKnowledge`, `Journey` e `DivineContract` são dados persistentes. Novos campos de personagem e POI usam o serializador existente. A versão de geração mudou: saves anteriores são recusados pelo mecanismo de versão já existente. O snapshot do código anterior foi preservado em `baseline_code/procedural/`.

## Comparativo com o documento

| Sistema | Entrega | Limite real |
| --- | --- | --- |
| Escala e densidade | 4 reinos; 1 capital + 4 cidades; 6–8 vilas subordinadas; capitais maiores | Abastecimento herdado ainda tem capacidade fixa por localidade. |
| Grafo e memória de rotas | Conexões persistentes, fonte/confiança/datas; planejamento só no grafo pessoal | Estradas/trilhas simples; terreno usa classificação resumida. Não há formação dinâmica de redes comerciais. |
| Destino, rumor e localização | Conhecimento de lugar separado da rota; relato remoto pode conservar coordenadas desconhecidas | Rumores de POI dependem de fatos e contatos reais; não há emissor artificial para garantir descobertas. |
| Instruções | Perguntar presencialmente; interlocutor usa suas próprias conexões; confiança insuficiente não libera viagem | Mapas como objetos negociáveis e contratação remunerada de guias continuam pendentes. |
| Viagem e multietapas | Saída pelo portão, caminho externo, entrada e conexões; alimento/água/dinheiro reais; seguir/escoltar guia | Exploração deliberada de estradas desconhecidas ainda não é alternativa autônoma; seguir/escoltar exige guia que já tenha viagem válida. |
| Migração e buscas | Migração, pistas remotas, proteção, ordens e representações usam o acesso conhecido | Sem rota, a ação pode pedir informação ou visitar um ponto intermediário conhecido. Isso não garante conseguir a informação. |
| POIs e cavernas | Estoque finito, minério/item incomum, risco físico, abrigo, restos e história; estados de lugar por personagem | Exploração é uma ação resumida. Profundidade/áreas são dados, sem percurso por câmaras. Propriedades especiais de ferramentas não ganharam cadeia produtiva própria. |
| Expedições e ocupação | Grupo existente temporário, companheiros presentes, aprendizado ao acompanhar; ocupação com companhia e capacidade | Negociação/disputa longa, aluguel e construção de sede ficam para depois. Reivindicação não é propriedade legal. |
| Facções e adesão | Conhecimento por contato; interesse por poucos membros/recursos; convite, pedido, aceite, recusa, adiamento ou condição | Critérios usam sobretudo profissão/coragem/ambição/necessidade/independência. Serviço condicional e retomada do adiamento não têm ciclo completo. |
| Organização e recursos | Formalização de Group duradouro reutiliza Society; contribuições e estoque usam transferências reais | Não foram criadas todas as estratégias possíveis de financiamento ou logística de comércio entre cidades. |
| Contato divino | Busca por motivo pessoal, local conhecido, viagem, rito; audiência exige favor, canal válido, presença e energia | Alcançar o rito não obriga resposta. Pactos oferecidos são do tipo proteção em troca de proteção a uma pessoa. |
| Pactos e manifestação | Aceitar/recusar/abandonar; conhecimento divino do descumprimento por canal válido; manifestação física temporária com custo | Não há ritual de manifestação forçada, nem objetivo automático de caçar deuses. Presença invisível continua sem acesso físico. |
| Morte divina | Morte exige manifestação física alcançável; apoteose não decorre automaticamente da morte | Essência, fragmentos e caminhos excepcionais de ascensão continuam sob regras existentes. |

## Validação curta

**14 testes passaram**: dez métodos novos da Fase 5.4 e quatro regressões críticas de alimentação/letalidade. Os novos métodos cobrem: destino sem rota e JSON; instruções e deslocamento; multietapas sem aresta desconhecida; seguir e escoltar com aprendizado posterior; rumor de POI sem rota; contato e aceitação para adesão; formalização sem moeda criada; ocupação e conservação de estoque, exploração e retorno; contato sem resposta obrigatória/pacto opcional; deus invisível versus manifestação física, sem ascensão automática.

Os cenários controlados alteram condições para verificar regras. Adesão, ocupação, exploração e pacto demonstrados nesses testes **não são acontecimentos naturais de Arandor-54**. Também houve uma verificação pequena de 48 horas com 69 NPCs. Não foi executada a suíte histórica completa nem outra campanha longa.

### Interrupção e correções

A primeira tentativa natural com esta mesma seed parou na hora 100: o NPC 2290 ultrapassou o limite de 64 observações ao receber notícia de localização entre decisões. A poda existia na atualização periódica, mas faltava no ponto de inserção do fato. A poda foi centralizada e aplicada imediatamente; a regressão está no teste 1. A evidência da interrupção foi preservada em `tentativa_interrompida_100h/`. Houve **um reinício da mesma seed**, por essa falha estrutural, sem trocar resultados naturais.

Na integração curta também foram corrigidos o cálculo de utilidade com proxies coletivos sem campo `devotion`, a conservação de coordenadas já conhecidas após rumor mais fraco e a conclusão de chegada acompanhando guia. Após a campanha concluída, o cenário controlado de exploração motivou dois ajustes pequenos: criar intenção de retorno ao lar e reconhecer corretamente “explorado na hora 0”. Os 14 testes passaram novamente. Não houve exploração natural na campanha, portanto nenhum episódio reportado depende desses ajustes posteriores. Os hashes do código da campanha e da entrega ficam separados no manifesto de entrega.

## Campanha natural: acontecimentos observados

| Medida | Resultado |
| --- | --- |
| NPCs no início / vivos no fim | 1826 / 1693 |
| Reinos / localidades / POIs / conexões | 4 / 45 / 8 / 52 |
| Viagens iniciadas / concluídas / ainda registradas | 70 / 61 / 9 |
| Trechos efetivamente atravessados | 62 |
| Viagens com várias conexões | 2 |
| Pedidos de rota / transmissões / destinatários distintos | 128 / 5 / 3 |
| Registros de rota criada ou melhorada depois da geração | 12 |
| Bloqueios registrados / pessoas distintas bloqueadas | 115 / 53 |
| Migrações iniciadas / mudanças de residência concluídas | 28 / 25 |
| Conhecimento organizacional novo / convites / novos membros | 230 / 22 / 0 |
| Pedido espontâneo de adesão / recusas ou adiamentos respondidos | 1 / 2 |
| Grupos formados / propostas criadas / entregues / decididas | 179 / 87 / 32 / 12 |
| Intenções de contato divino / viagens religiosas / ritos alcançados | 157 / 18 / 8 |
| Audiências / pactos / manifestações físicas | 0 / 0 / 0 |
| Novas visitas, explorações, expedições ou ocupações de POI | 0 |
| Seguir/escoltar em campanha natural | 0 |

A contagem separa geração e campanha: por exemplo, os 5.256 registros iniciais de conhecimento de rotas não são aprendizado durante as 200 horas. Um evento é uma ocorrência, e não uma pessoa nova. As 157 intenções religiosas também não são 157 respostas de deuses.

Houve validação do estado a cada 25 horas, em **oito checkpoints sem erros**, e auditoria dos registros de partida sem violações de conexões conhecidas ou reservas mínimas. Essa auditoria verifica o conhecimento apresentado e a reserva na partida; não demonstra que toda viagem terminou, que a estimativa suportou todas as interrupções ou que toda movimentação possível do motor foi coberta. As regras não foram alteradas durante a execução. Tempo de simulação: 227,12 segundos; save final: aproximadamente 152 MiB.

## Problemas e limites observados

1. **Abastecimento de água inadequado à nova densidade.** Das 133 mortes, 92 foram classificadas como sede, 32 como fome, oito como privação combinada e uma como combate. A sede responde por 69,2%; todas as privações somam 99,2%. A classificação é a dos registros de morte, não uma prova de causa exclusiva durante toda a vida. Noventa e uma das mortes por sede ocorreram nas quatro capitais. Os registros incluem NPCs com zero água, objetivo `fill_water` e distância zero ao ponto de água: chegar ao poço não assegurou obter água.

   `Economy.daily()` mantém reposição de até 80 unidades/dia e limite de estoque 160 em qualquer localidade. Uma capital nasce com 104 NPCs. Como referência, sede de 2/h e redução de 45 por unidade exigem cerca de 111 unidades/dia para esses NPCs, mesmo sem o agravamento do deserto. Esse cálculo explica a incompatibilidade de capacidade, mas não substitui medir filas, interrupções, distribuição e deslocamentos. Não foi alterada a fisiologia nem criada água para melhorar os resultados. Próximo ajuste recomendado: capacidade material de abastecimento proporcional à população e infraestrutura, conservando estoque e custo, com diagnóstico da distribuição.

2. **Contato organizacional cresceu, adesão natural não.** Houve 22 convites a 22 pessoas, mas nenhuma aceitação; 21 registros permanecem oferecidos, um foi recusado, e o pedido espontâneo de Lyra Corven foi adiado. A prioridade da resposta compete com sobrevivência e exige reencontro com o líder. A Irmandade de Nordor acabou dissolvida após a morte de Elena. Isso prova contato causal e dificuldade concreta; não prova que o gargalo de crescimento das facções foi resolvido. Adiamento e condição precisam de continuação executável, em vez de encerrar a primeira resposta.

3. **POIs funcionam nos cenários controlados, mas não alimentaram histórias naturais.** Esta seed possui seis cavernas, nenhuma ruína de castelo. Ninguém novo visitou ou explorou esses lugares. Um detalhe da inicialização ajuda a explicar: a regra geral de morador de vila é aplicada antes da especialização profissional, ensinando sobretudo a ligação à autoridade; o caçador da vila pode não conhecer a trilha local da caverna. Rumor e rota não surgem sem fonte. Vale melhorar conhecimento local justificado de profissões e observação física de trilhas, sem distribuir todos os POIs ao mundo. Ainda não existe exploração autônoma de estrada desconhecida.

4. **Continuidade de viagem ainda disputa prioridade.** Nove viagens permanecem registradas no fim. Algumas começaram perto da hora 200; outras estão antigas: Cael Montes começou a viagem com duas conexões na hora 55 e só concluiu o primeiro trecho; Bela Bruma iniciou outra na hora 170 e não concluiu o retorno intermediário. Deslocar-se até um posto conhecido para perguntar sobre destino distante também pode produzir desvios longos. É necessário distinguir pausa fisiológica legítima de estagnação, registrar a barreira atual e revisar a escolha de pontos intermediários. O prazo nominal da estrada não é a duração final do personagem.

5. **Atividade coletiva repetitiva.** Dos 179 grupos, 177 são de segurança e apenas dois de recursos. Só 12 das 87 propostas foram decididas. A densidade gera encontros e mobilização, mas muitos grupos locais tratam causas parecidas; esses números não equivalem a 179 enredos independentes. A política e a sobrevivência herdadas ainda restringem a variedade.

6. **Religião permaneceu em busca e rito.** Oito contatos alcançaram o local; não houve audiência, pacto ou manifestação. Os requisitos de favor/devoção/canal/energia não foram reduzidos para produzir cenas. O resultado de 200 horas não permite concluir que eventos raros jamais acontecerão, mas também não valida sua frequência natural.

7. **Escopo parcial explicitado.** Permanecem sem ciclo completo: mapas negociáveis, guias contratados, exploração de estrada desconhecida, serviço exigido na adesão, retomada de decisões adiadas e logística material entre localidades. Perigo da estrada é custo/avaliação e histórico de fatos reais, sem ataques aleatórios inseridos por esta fase. Itens e áreas de caverna persistem, mas não há dungeon ou novo sistema artesanal. Ritual de manifestação forçada é extensão futura expressamente permitida pelo documento.

## Avaliação

A geografia agora interfere em migração, busca, organização e religião; a viagem pode falhar por desconhecimento e aprender com pessoa identificada. Os dois casos de instrução fraca seguida de instrução confiável são o melhor resultado narrativo desta fase. Contudo, a campanha não justifica declarar sobrevivência sustentável, crescimento natural de facções ou exploração emergente resolvidos. A próxima intervenção útil é estabilizar água e continuidade de acesso/adesão antes de expandir sistemas maiores.

## Evidência preservada

- `campanha_200h/resultado.json`: censos, contadores, entidades e oito verificações.
- `campanha_200h/eventos_espaciais.json`: eventos identificados usados nas histórias.
- `campanha_200h/save_final.json`: estado completo na hora 200.
- `campanha_200h/manifesto.json`: seed, versão, censo inicial e hash de código da campanha.
- `testes_14.log` e `tests/test_phase54.py`: execução e cenários controlados.
- `tentativa_interrompida_100h/`: falha preservada da primeira tentativa.
- `ENTREGA_FINAL.json`: hashes e pequenos ajustes posteriores à campanha.
