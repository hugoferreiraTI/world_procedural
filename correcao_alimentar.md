Antes de iniciar qualquer nova fase ampla do projeto, corrija o comportamento individual de alimentação revelado pelas auditorias da Fase 3.

Esta etapa NÃO é a Fase 4.

Não implemente migração entre cidades, recuperação de cidades falidas, caravanas, comércio intermunicipal, guerra, política nova, religião, deuses, nascimento, envelhecimento ou outros sistemas grandes.

O objetivo desta etapa é exclusivamente tornar a sobrevivência alimentar individual coerente sem mascarar escassez econômica real e, em seguida, repetir as auditorias longas.

Preserve a arquitetura atual:

State/Knowledge → Need → Priority → Solutions → Goal → Action → Consequence → New State.

Não crie um planejador paralelo, GOAP novo ou regras roteirizadas específicas por personagem.

## 1. Diagnóstico confirmado

As auditorias atuais demonstraram que o principal problema não é ausência de percepção de fome.

A necessidade `food` já existe e é selecionada.

O problema está na cadeia:

sentir fome
→ perceber que não há reserva
→ obter dinheiro/produto
→ deslocar-se
→ adquirir comida
→ efetivamente comer.

Nas três campanhas reproduzidas:

- 687 das 690 mortes ocorreram com fome no limite;
- 108 mortos carregavam comida;
- em 107 desses 108 casos, a comida havia acabado de entrar no inventário na última decisão;
- esses 107 personagens tinham apenas 1–3 HP;
- 318 mortes por fome tiveram `work` como última escolha;
- nas 318, a necessidade selecionada era `food`.

Portanto, não resolva isso simplesmente aumentando o score de `eat`.

O problema envolve prevenção, reserva, tempo, prioridade e viabilidade da cadeia de solução.

## 2. Separar três conceitos

O comportamento alimentar deve distinguir:

### Reserva alimentar

Quantidade de comida possuída para uso futuro.

O personagem deve tentar manter uma pequena reserva antes de entrar em fome significativa.

### Refeição

Ato de consumir comida quando a fome atingiu um nível razoável.

### Emergência alimentar

Estado no qual adiar a refeição ou iniciar uma cadeia longa de obtenção pode levar à morte antes do consumo.

Não colapse esses três conceitos numa única ação.

## 3. Reserva alimentar preventiva

NPCs não devem normalmente esperar ficar famintos para começar a procurar comida.

Implemente comportamento preventivo de reserva.

A reserva deve ser baseada preferencialmente em cobertura temporal e não em acumulação ilimitada.

Como ponto inicial para teste:

- reserva pessoal normal equivalente a aproximadamente 24 horas de segurança;
- com as regras atuais, isso provavelmente corresponde a cerca de duas rações;
- uma viagem planejada pode aumentar a reserva necessária de acordo com duração prevista + pequena margem;
- não permita acumulação preventiva arbitrária.

Os valores devem ficar centralizados/configuráveis.

Não hardcode números espalhados pelo código.

Se já existir armazenamento doméstico utilizável, ele pode participar da reserva.

Se não existir, NÃO crie agora um grande sistema de despensa doméstica. Use o inventário pessoal como representação temporária da reserva.

A reserva preventiva deve gerar comportamento de manutenção, mas NÃO deve automaticamente superar necessidades sociais, familiares, profissionais ou pessoais importantes quando não existe risco imediato.

## 4. Reposição da reserva

Quando a reserva estiver abaixo do alvo, o NPC pode considerar:

- comprar comida;
- obter comida por trabalho compatível;
- coletar;
- receber provisões;
- outras alternativas já existentes e legítimas.

Continue respeitando:

- conhecimento individual;
- cotação válida/stale/desconhecida;
- estoque conhecido;
- localização;
- distância;
- dinheiro;
- personalidade;
- disponibilidade real.

Não consulte estoque global magicamente.

Preço desconhecido continua diferente de falta de dinheiro.

Produto ausente continua diferente de falta de dinheiro.

## 5. Momento normal da refeição

Hoje esperar chegar a níveis extremos cria cadeias tardias.

Faça o personagem considerar uma refeição normal antes da emergência.

Use parâmetros configuráveis.

Como hipótese inicial de teste, avalie um limiar próximo de metade da escala de fome, aproximadamente 40–55.

Não assuma que esse valor é definitivo.

A intenção é que um NPC com comida disponível normalmente coma antes de atingir fome extrema.

Comer cedo demais também não deve desperdiçar sistematicamente grande parte dos 40 pontos de redução da ração.

Registre o consumo real para podermos avaliar posteriormente o limiar correto.

## 6. Prioridade alimentar

Não transforme qualquer necessidade de reposição de estoque em prioridade absoluta.

A regra desejada é:

MANUTENÇÃO DE RESERVA:
prioridade preventiva moderada.

FOME NORMAL:
prioridade crescente.

FOME ALTA:
prioridade elevada sobre atividades não essenciais.

RISCO IMEDIATO DE MORTE:
prioridade máxima de sobrevivência.

Se existe comida no inventário e adiar a refeição pode produzir dano fatal ou tornar a sobrevivência improvável, `eat` deve poder interromper:

- trabalho;
- treinamento;
- viagem;
- descanso;
- preparação de viagem;
- objetivo persistente anterior;
- necessidade empatada por ID.

Não permita que o desempate por menor ID decida entre uma refeição necessária para sobreviver e uma ação não vital.

## 7. Avaliação temporal de sobrevivência

Uma solução pode ser economicamente possível e biologicamente impossível.

Adicione uma avaliação comum e pequena de prazo de sobrevivência.

Conceitualmente:

EstimatedTimeUntilFoodConsumed

versus

EstimatedSurvivalMargin.

Não crie um planejador complexo.

Precisamos apenas impedir soluções obviamente impossíveis como:

trabalhar
→ ganhar dinheiro
→ caminhar ao mercado
→ comprar
→ comer

quando o personagem morrerá antes de completar a sequência.

Uma alternativa pode ser marcada como:

economically_viable = true
survival_viable = false.

Registre o motivo.

Leve em conta, no mínimo:

- HP atual;
- fome;
- horas consecutivas em privação;
- dano previsto;
- distância;
- duração da ação;
- necessidade de uma etapa adicional de consumo.

## 8. Aquisição não significa alimentação

Preserve a diferença semântica:

comprar comida != comer;
coletar comida != comer;
receber comida != comer.

Entretanto, introduza, se arquiteturalmente adequado, variantes explícitas de refeição imediata, por exemplo:

- comprar e consumir uma refeição no local;
- receber e consumir uma refeição;
- trabalho pago diretamente com refeição consumida.

Essas ações devem:

- consumir estoque real;
- transferir dinheiro/bens reais quando aplicável;
- consumir tempo;
- reduzir fome somente porque houve consumo real.

Não faça toda compra reduzir fome automaticamente, pois comprar para formar reserva é comportamento válido.

## 9. Objetivos ativos podem ser interrompidos

Preserve continuidade de objetivos em condições normais.

Porém, um objetivo ativo NÃO pode impedir uma ação imediatamente necessária para sobreviver.

Um personagem carregando comida, com risco de morte por fome antes da próxima oportunidade, deve interromper uma viagem, treinamento, trabalho ou outro objetivo para comer.

Após estabilização, o objetivo anterior pode ser retomado se ainda for válido.

Não destrua a continuidade normal apenas para corrigir emergência.

## 10. Preparação de viagem

A preparação atual não pode priorizar água, destino ou outro preparo ignorando risco alimentar imediato.

Antes de iniciar ou continuar viagem, estime:

- duração conhecida;
- comida necessária;
- água necessária;
- reserva atual;
- fome/sede atuais;
- margem mínima.

Se já houver comida disponível e a refeição for necessária antes da viagem, coma antes.

Não use conhecimento global.

## 11. Não alterar ainda

Nesta etapa, NÃO:

- reduza crescimento de fome;
- reduza dano de privação;
- aumente HP;
- gere comida gratuita;
- aumente estoque magicamente;
- crie salário infinito;
- teletransporte comida;
- force formação profissional;
- crie migração entre cidades;
- implemente recuperação de cidades falidas;
- faça rebalanceamento amplo da economia.

Primeiro corrija o comportamento de sobrevivência individual.

## 12. Testes obrigatórios

Preserve todos os testes anteriores.

Adicione regressões para, no mínimo:

NPC com fome moderada + reserva suficiente:
não precisa sair procurando comida.

NPC saudável + reserva abaixo do alvo:
pode planejar reposição preventivamente sem transformar isso em emergência.

NPC com comida + fome próxima do limiar normal:
come antes de entrar em estado crítico.

NPC com fome crítica + comida no inventário + trabalho ativo:
interrompe e come.

NPC com fome crítica + comida + descanso empatado:
comida vence por risco de sobrevivência, não por ID.

NPC com fome crítica + objetivo de viagem ativo:
interrompe para comer quando necessário.

NPC pobre com cadeia trabalho→compra→consumo longa demais para sobreviver:
não considera essa cadeia uma solução salvadora válida.

NPC pobre mas com tempo suficiente:
trabalho continua sendo solução legítima.

NPC chega a mercado em emergência:
consegue usar uma ação real de refeição imediata quando aplicável.

Compra para reserva:
produto entra no inventário sem reduzir fome se não houver consumo.

Reserva para viagem:
quantidade planejada considera duração conhecida sem consultar mapa global.

Mesma seed + mesmas ações:
resultado determinístico.

Save/load:
estado de reserva, objetivos e novos campos persistem corretamente.

## 13. Instrumentação

Registre para análise:

- HungerAtFoodSearchStart;
- HungerAtAcquisition;
- HungerAtConsumption;
- HPAtFoodSearchStart;
- HPAtAcquisition;
- HPAtConsumption;
- FoodOwnedAtSearchStart;
- ReserveTarget;
- ReserveDeficit;
- TimeFromSearchToAcquisition;
- TimeFromAcquisitionToConsumption;
- EstimatedTimeUntilFoodConsumed;
- EstimatedSurvivalMargin;
- EmergencyGoalInterrupted;
- DeathBeforeConsumption;
- LastSuccessfulAction;
- reason why an apparently viable food solution was rejected.

Diferencie claramente:

sem produto;
sem dinheiro;
preço desconhecido;
mercado desconhecido;
produto distante;
solução lenta demais;
comida já disponível;
objetivo ativo interrompido.

## 14. Auditorias longas

Depois dos testes, execute novamente:

- jogador Dovha — 10.000 horas;
- espectador Dovha — 10.000 horas;
- observador global Mira — 10.000 horas.

Preserve os resultados anteriores para comparação.

Não altere regras no meio da execução para obter números melhores.

Compare especialmente:

- mortes totais;
- mortes por fome;
- mortes com comida já possuída;
- mortes após adquirir comida na última decisão;
- HP médio na aquisição de alimento;
- fome média quando começa a procura;
- tempo médio entre início da procura e consumo;
- porcentagem de NPCs mantendo reserva;
- quantidade média de rações pessoais;
- impacto da reserva sobre estoque municipal;
- pobreza;
- mercados vazios;
- seleção fisiológica;
- seleções pessoais;
- necessidades pessoais satisfeitas;
- treinamento e profissões.

Não estabeleça meta artificial de mortalidade.

Queremos descobrir o comportamento resultante.

## 15. Auditoria narrativa obrigatória

O relatório final NÃO deve ser somente um relatório sobre fome.

A fome é o principal problema técnico desta etapa, mas o projeto também precisa ser avaliado como gerador de histórias emergentes.

Faça uma leitura separada dos logs procurando histórias reais produzidas pelas campanhas.

Crie uma seção grande chamada:

# Histórias emergentes observadas

Procure cadeias causais envolvendo, quando existirem:

- família;
- desaparecimento e procura;
- morte e descoberta;
- luto;
- amizade;
- crime;
- investigação;
- vingança;
- proteção;
- profissão;
- treinamento;
- abandono e retomada;
- mudança de carreira;
- ambição;
- reconhecimento;
- reputação;
- relações;
- quests;
- sucessão;
- acontecimentos locais inesperados.

Não invente causas que os registros não provam.

Para cada história interessante, informe:

personagens e IDs;
relações relevantes;
turnos;
eventos principais;
o que cada personagem sabia;
necessidades envolvidas;
ações tomadas;
consequências;
desfecho atual.

Mostre a cadeia causal de maneira legível.

Exemplo conceitual:

evento
→ conhecimento
→ necessidade
→ decisão
→ consequência
→ nova necessidade.

Tente trazer pelo menos 8–12 histórias interessantes entre as três campanhas se os logs realmente contiverem material suficiente.

Procure deliberadamente histórias NÃO centradas em comida.

Se não existirem histórias não alimentares suficientes, NÃO invente.

Diga claramente que variedade narrativa continua limitada e mostre a evidência.

Também registre:

- quantidade de temas narrativos diferentes observados;
- histórias com 2, 3, 4 ou mais eventos causalmente conectados;
- histórias envolvendo o mesmo personagem ao longo de períodos longos;
- histórias totalmente autônomas, sem jogador;
- histórias alteradas pela intervenção do jogador;
- histórias interrompidas pela morte do personagem;
- histórias que surgiram de profissão/treinamento;
- exemplos de personagens reagindo de maneiras diferentes a situações comparáveis, se existirem.

O relatório deve permitir avaliar simultaneamente:

1. se a sobrevivência ficou mais coerente;
2. se o mundo continua gerando histórias;
3. se as histórias estão ficando mais diversas;
4. se a correção de alimentação abriu espaço para necessidades não fisiológicas.

## 16. Relatório final

O relatório deve conter separadamente:

- resumo executivo;
- alterações realizadas;
- arquitetura preservada;
- regras de reserva alimentar;
- regras de refeição;
- regras de emergência;
- avaliação temporal de sobrevivência;
- testes;
- auditorias de 10.000 horas;
- comparação com Fase 3 original;
- análise das mortes;
- análise de estoque pessoal;
- impacto nos mercados;
- impacto sobre necessidades pessoais;
- Histórias emergentes observadas;
- diversidade narrativa;
- limitações;
- bugs ainda existentes;
- recomendações para a próxima fase.

Não declare sucesso apenas porque as mortes diminuíram.

Não declare fracasso apenas porque ainda houve mortes.

O critério é coerência causal.

Escassez, pobreza e fome ainda podem matar.

O que não deve acontecer é um NPC morrer de fome porque:

- decidiu trabalhar apesar de já possuir uma refeição;
- começou a procurar comida somente quando estava praticamente morto;
- comprou uma refeição salvadora e morreu esperando uma nova decisão para comê-la;
- perdeu uma refeição vital para descanso por desempate de ID;
- manteve uma viagem ou objetivo não essencial quando comer imediatamente era necessário.

A meta desta etapa é transformar alimentação de uma reação de emergência tardia em um comportamento preventivo e coerente, preservando as consequências reais da economia e a autonomia dos agentes.