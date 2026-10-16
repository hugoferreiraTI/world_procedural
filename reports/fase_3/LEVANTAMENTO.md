# Levantamento antes da implementação da fase 3

Base: documento colado pelo usuário, preservado integralmente em `fase_3.md`.
Foram lidos `instruction.md`, `fase_2.md`, relatório final da fase 2, relatório das
três perspectivas, diagnóstico de abastecimento/continuidade, código e testes.
O diagnóstico fisiológico e o relatório técnico de abastecimento são seções dos
dois últimos relatórios disponíveis; não existe um quarto relatório separado.
Núcleo anterior preservado em `baseline_code/procedural` (mvp-3).

1. **Existente:** Need/Goal/Solution, utility determinístico, mercado real,
   produção e salários, trabalho rural por comida, população nominal,
   conhecimento/observações, necessidades pessoais, eventos e saves.
2. **Reutilizar:** esses serviços; ampliar Economy e ProfessionSystem, inserir
   candidatos no GoalSystem e considerações em utility. População será um auxiliar
   contábil; observabilidade não decidirá nem criará necessidades paralelas.
3. **Confirmado:** cidade responde apenas com trigo; salários materiais param
   em estoque cheio; preparo em lote recusa espaço parcial; fome oferece trabalho
   apenas com saldo <5; elenco profissional fixo; nenhuma reposição/treinamento;
   contador populacional não distingue mortos; fisiologia avança em toda hora,
   decisões comuns a cada seis; necessidades pessoais não registram perdas.
4. **Hipóteses:** parcela das mortes por sede/acesso; capacidade realizada versus
   nominal; frequência de decisão; quanto cada intervenção libera comportamento
   pessoal. Instrumentar água no núcleo preservado antes de preparar reservas.
5. **Mudanças:** diagnóstico local e demanda/capacidade; tarefas temporárias;
   produção parcial e salário acumulado proporcional; preços/boletins observados;
   treinamento por ações de tempo real; materialização tardia, limitada e
   financiada; sobrevivência preventiva limitada por conhecimento; métricas de
   mortes, água e motivos das necessidades; testes e três auditorias de 10.000h.
6. **Não recriar:** Utility AI, NeedSystem, GoalSystem, economia, profissões,
   quests, eventos, grafo, persistência, GOAP. Não criar guerra, política complexa,
   deuses, caravanas, nascimentos ou envelhecimento. Não mudar fisiologia ou
   prazos sociais para melhorar percentuais.

## Modelo formal escolhido antes de implementar

`Town.population` será o total vivo de residentes administrativos, independente
da posição atual. `abstract_population` será explícita. Vivos persistentes e
mortos persistentes serão derivados de IDs residentes. O jogador é visitante e
não entra nesse censo. Total vivo = abstratos + persistentes vivos. Na geração,
materializar o elenco retira um abstrato; morte reduz total uma vez via evento
idempotente; treinamento não muda população; materialização não muda total.

Preservar a escala agregada anterior: 1 food é uma ração de 40 pontos para um
persistente; 3 food requerem 2 grain. Consumo abstrato é um fluxo amostral
`ceil(abstratos/120)` rações/dia, zero se não há abstratos. Não representa que
uma ração física alimenta 120 pessoas; representa somente a fração do consumo
abstrato que participa do mercado detalhado. A renda abstrata anterior representa
atividade fora desse mercado e continua registrada como fonte monetária.
Não criar produção culinária abstrata adicional: trabalhadores materializados e
temporários suprirão esse fluxo explícito, com insumos reais. Colheita coletiva
existente continua limitada a população/tesouro/estrutura/tempo diário.

Para permitir produção parcial sem perda ou criação de insumo, a cozinha guarda
resto processável em terços: cada food utiliza 2/3 grain; retira grãos inteiros e
preserva o restante numa reserva de 0 a 2 terços. Inventários continuam inteiros.
Pagamento usa crédito em sextos exatos de hora, acumulado até moeda inteira;
uma produção parcial não arredonda sempre para cima. Compra/venda de grain
permanece em unidades inteiras e usa a mesma curva de preços.

Capacidade nominal de cozinheiro: 3 rações/hora × janela profissional 10h/dia,
limitada por postos da taverna. Demanda inclui fluxo abstrato + 1,2 ração/dia por
persistente no mapa local. Capacidade realizada e motivo de subutilização serão
registrados separadamente. Ter profissional vivo não basta para contratar outro;
resposta verifica trabalhadores, auxiliares e candidatos antes de materializar.

Versão resultante mvp-4. Saves anteriores serão preservados e recusados pelo
carregamento normal, sem migração silenciosa. Auditorias compararão as três
campanhas históricas, com limite causal explícito: geração depende da versão.
