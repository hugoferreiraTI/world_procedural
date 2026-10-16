# FASE 4.1 — RECUPERAÇÃO FISIOLÓGICA E SOBREVIVÊNCIA SUSTENTÁVEL

Base atual: `mvp-5-fase4`.

Esta NÃO é uma nova fase de expansão social.

Não adicionar novos sistemas políticos, religiosos, militares ou narrativos.

A Fase 4.1 é uma etapa curta e cirúrgica para corrigir um problema observado após a implementação de interação, combate e resposta:

**os NPCs conseguem sobreviver a uma crise alimentar imediata, mas frequentemente não conseguem se recuperar do dano fisiológico acumulado antes da próxima crise.**

O resultado pode formar um ciclo:

fome extrema  
→ dano em HP  
→ NPC consegue alimento  
→ fome cai  
→ HP continua muito baixo  
→ volta para rotina normal  
→ fome volta a níveis críticos  
→ novo dano  
→ come novamente  
→ continua com HP baixo  
→ eventualmente morre.

Isso faz com que um personagem possa tecnicamente “resolver” várias necessidades alimentares e ainda assim morrer lentamente pelo acúmulo das crises anteriores.

O problema NÃO é simplesmente falta de cura.

Existe recuperação por descanso.

O problema é:

- refeição normal ainda começa relativamente tarde;
- a recuperação disponível pode ser lenta demais;
- HP baixo por privação não possui pressão suficientemente forte de recuperação;
- dano de privação e dano físico de combate compartilham HP, mas possuem causas semanticamente diferentes;
- algumas novas formas de aquisição da Fase 4 ainda não passam corretamente pelo sistema alimentar.

---

# 1. OBJETIVO PRINCIPAL

A Fase 4.1 deve fazer com que um NPC que:

- consiga alimento;
- consiga água;
- saia de uma crise;
- tenha oportunidade de descansar;

possa realmente recuperar sua condição física ao longo das horas/dias seguintes.

Não queremos apenas:

“não morreu nesta hora.”

Queremos:

“sobreviveu à crise e conseguiu sair do estado fisiológico de colapso.”

---

# 2. NÃO FACILITAR ARTIFICIALMENTE A SOBREVIVÊNCIA

Não:

- reduzir crescimento da fome;
- reduzir crescimento da sede;
- reduzir dano de fome somente para melhorar estatística;
- aumentar HP máximo;
- gerar comida;
- dar comida gratuita;
- aumentar estoque municipal magicamente;
- teleportar NPC para mercado;
- recuperar HP instantaneamente ao comprar alimento;
- transformar qualquer refeição em poção de cura.

As regras materiais permanecem reais.

O foco é melhorar:

- prevenção;
- recuperação;
- interpretação correta de dano;
- continuidade fisiológica.

---

# 3. PRESERVAR TODA A FASE 4

Não alterar estruturalmente:

- combate;
- ataque;
- defesa;
- fuga;
- rendição;
- perseguição;
- captura;
- migração;
- emoções;
- grievances;
- reputação;
- população ampliada;
- LOD;
- crime;
- testemunhas;
- sucessão;
- relações;
- Need/Goal/Utility.

Só alterar esses sistemas quando necessário para integrar a sobrevivência.

---

# 4. PRIMEIRO BUG CONFIRMADO — `steal_person`

Na auditoria de Vespera ocorreu:

Bela Douran #3139:

- HP = 1;
- fome = 100;
- comida = 0;
- necessidade = `food`;
- prioridade = 100.

Alternativas:

`steal_person` = 61,10  
`steal_meal` = 59,03

`steal_person` venceu.

A ação transferiu uma ração real:

comida 0 → 1.

Porém:

fome permaneceu 100.

No fechamento seguinte, Bela morreu carregando a ração.

Isto é bug de integração.

A aquisição `steal_person` não estava integrada ao mesmo raciocínio de sobrevivência usado pelas demais aquisições alimentares.

---

# 5. CORRIGIR TODA AQUISIÇÃO ALIMENTAR, NÃO APENAS ROUBO

Não faça:

`if action == steal_person: eat`.

Isso seria correção específica demais.

Crie/reutilize uma interface semântica comum:

**esta ação pode fornecer alimento?**

Exemplos:

- compra;
- coleta;
- ajuda recebida;
- pagamento em alimento;
- roubo;
- restituição recebida;
- outra transferência real.

Quando uma solução é considerada para uma necessidade alimentar, o estimador precisa saber:

1. ela adquire comida?
2. quanto tempo demora?
3. o alimento estará realmente no inventário?
4. ainda será necessário gastar outra ação/hora para comer?
5. o personagem sobreviverá até esse consumo?

---

# 6. AQUISIÇÃO EM EMERGÊNCIA DEVE CONSIDERAR CONSUMO

Preserve o princípio:

**adquirir != comer.**

Porém, em uma emergência na qual esperar outra decisão é fatal, soluções reais de:

`acquire + consume`

devem competir corretamente.

Exemplo:

HP 1  
fome 100  
alvo possui comida roubável.

Alternativas:

`steal_person`
→ obtém ração
→ não come
→ morte certa no fechamento.

`steal_meal`
→ obtém ração
→ consome de forma real
→ fome reduz
→ sobrevive.

O segundo deve receber preferência porque a cadeia completa é biologicamente viável.

Não porque roubo alimentar recebe bônus arbitrário.

---

# 7. NÃO CRIAR CONSUMO MÁGICO

Uma operação composta `acquire_and_eat` só pode existir quando:

- o alimento realmente foi adquirido;
- a transferência ocorreu;
- quantidade foi debitada da origem;
- quantidade entrou no inventário ou foi imediatamente consumida;
- o consumo foi registrado;
- fome foi reduzida pelo consumo real.

Nada de:

roubou
→ `hunger -= 40`

sem item real.

---

# 8. REFEIÇÃO NORMAL ESTÁ TARDE DEMAIS

A refeição normal atualmente começa aproximadamente em fome 50.

Isso ainda permite que NPCs comuns, principalmente sob LOD de 3/6/12h, iniciem a alimentação já bastante pressionados.

A Fase 4.1 deve antecipar a janela de refeição normal.

Use inicialmente:

`NORMAL_MEAL_START ≈ 35`

como parâmetro central configurável.

Não espalhar números pelo código.

---

# 9. CURVA DE PRESSÃO DE REFEIÇÃO

Não transformar fome 35 em emergência.

Use uma curva.

Conceitualmente:

## fome 0–30

Estado normal.

Comer possui Utility baixa, exceto contexto especial.

## fome 30–40

NPC começa a considerar refeição se:

- possui comida;
- refeição é acessível;
- não existe prioridade relevante maior.

## fome 40–60

Refeição passa a ser uma necessidade normal importante.

## fome 60–80

Alta prioridade.

## fome 80+

Situação crítica.

## risco de morte imediato

Prioridade vital absoluta conforme regras existentes.

Esses limites devem ser centralizados.

Pode ajustar números durante a auditoria curta se dados mostrarem comportamento claramente ruim.

Não calibrar visando uma taxa de mortalidade específica.

---

# 10. COMER CEDO NÃO SIGNIFICA COMER O TEMPO TODO

Evitar:

fome 31  
→ come.

fome 31 novamente pouco depois  
→ come.

Isso aumentaria consumo artificialmente.

A Utility deve considerar:

- quantidade reduzida pela refeição;
- cobertura;
- reserva;
- próxima refeição provável;
- atividade atual;
- oportunidade presente.

Queremos refeições normais.

Não compulsão alimentar algorítmica.

---

# 11. HP BAIXO PRECISA SER UMA NECESSIDADE REAL

Hoje recuperação/tratamento está fortemente associada a ferimentos/lesões.

Porém um personagem pode possuir:

HP 20  
lesão 0

porque perdeu 80 HP em crises de fome.

Esse personagem está em estado grave mesmo sem ferimento de combate.

Crie ou generalize uma Need de recuperação física.

Nome conceitual:

`recovery`

ou equivalente.

---

# 12. A NECESSIDADE DE RECUPERAÇÃO

Deve surgir quando HP está significativamente abaixo do máximo.

Exemplo inicial configurável:

HP >= 80:
pressão pequena ou nenhuma.

HP 60–80:
pressão moderada.

HP 40–60:
importante.

HP 20–40:
alta.

HP <20:
muito alta.

Não necessariamente substituir necessidades vitais.

Se fome = 90:

comer continua mais importante.

Se sede = 95:

beber continua mais importante.

Depois da crise:

recuperar ganha espaço.

---

# 13. RECUPERAÇÃO NÃO É SOMENTE DORMIR

A Need de recuperação deve avaliar:

- fome;
- sede;
- local seguro;
- possibilidade de descanso;
- lesão;
- HP;
- recursos;
- tratamento disponível.

Possíveis soluções:

- comer primeiro;
- beber primeiro;
- descansar;
- procurar lugar seguro;
- pedir ajuda;
- receber socorro;
- buscar tratamento quando houver lesão.

Não precisa criar novo sistema médico.

---

# 14. DISTINGUIR CAUSA DO DANO

HP continua sendo uma barra comum.

Porém, para recuperação, precisamos distinguir pelo menos:

### dano recuperável por privação

causado por:

- fome;
- sede;
- efeitos fisiológicos equivalentes.

### dano físico

causado por:

- combate;
- agressão;
- lesão.

Não é necessário criar duas barras visíveis.

Pode existir internamente algo equivalente a:

`recoverable_deprivation_damage`

ou ledger de origem do dano.

---

# 15. PRINCÍPIO DA RECUPERAÇÃO

Se alguém perdeu:

40 HP por fome

e depois:

- consegue comida;
- consegue água;
- descansa;

o organismo deve conseguir recuperar esses 40 HP relativamente rápido.

Se alguém perdeu:

40 HP por espada

com lesão grave,

não deve recuperar tudo porque comeu e dormiu algumas horas.

---

# 16. COMO RASTREAR DANO RECUPERÁVEL

Ao aplicar dano por fome/sede:

```
hp -= X
recoverable_deprivation_damage += X
```

Limitado por:

- HP máximo;
- dano realmente sofrido.

Ao recuperar HP fisiológico:

```
healed = min(
    recovery_amount,
    recoverable_deprivation_damage,
    max_hp - hp
)
```

Depois:

```
recoverable_deprivation_damage -= healed
hp += healed
```

Nunca ultrapassar HP máximo.

---

# 17. DANO DE COMBATE NÃO ENTRA NESSA RESERVA

Quando ataque causa dano:

```
hp -= damage
```

Esse dano NÃO aumenta `recoverable_deprivation_damage`.

A recuperação dele continua dependendo do sistema físico:

- descanso;
- tratamento;
- first aid;
- recuperação de lesão.

Isso evita:

espada  
→ sanduíche  
→ +30 HP.

---

# 18. CASOS MISTOS

NPC pode ter:

HP máximo 100.

Perde:

30 por fome.

Depois:

20 em combate.

HP = 50.

Então:

`recoverable_deprivation_damage = 30`.

Mesmo perfeitamente alimentado e descansado, recuperação fisiológica rápida pode elevar:

50 → 80.

Os outros 20 dependem das regras normais de dano físico.

Esse é o comportamento desejado.

---

# 19. RECUPERAÇÃO FISIOLÓGICA DEVE SER SIGNIFICATIVA

A recuperação atual de 1–3 HP/h pode ser pequena demais para retirar um NPC do ciclo de colapso.

Use inicialmente uma curva mais forte para dano recuperável de privação.

Parâmetros iniciais:

### condição excelente

- descansando;
- fome <= 50;
- sede <= 50;
- local seguro.

Recuperação fisiológica:

**+8 HP/h**

limitada ao dano recuperável.

### condição aceitável

maior entre fome/sede = 51–70.

Recuperação:

**+4 HP/h**

### condição ruim

maior entre fome/sede = 71–80.

Recuperação:

**+1 HP/h**

### >80

sem recuperação fisiológica rápida.

Esses valores são hipóteses iniciais.

Centralizar configuração.

---

# 20. NÃO ACUMULAR DUAS CURAS INDEVIDAMENTE

Se o sistema antigo já cura HP por descanso:

não permitir:

cura antiga +8  
mais cura nova +8

sem intenção.

Reestruture para que exista uma função clara de recuperação.

Exemplo conceitual:

```
recover_hp(character, context)
```

Ela separa:

- recuperação fisiológica;
- recuperação de dano físico;
- tratamento.

Não duplicar cura.

---

# 21. DESCANSO PRECISA SER FERRAMENTA DE RECUPERAÇÃO

Quando:

HP baixo  
fome estável  
sede estável

descanso deve possuir Utility relevante.

Não queremos:

HP 12  
fome 42  
sede 35

→ “vou trabalhar 6 horas.”

A recuperação precisa competir de forma coerente.

---

# 22. HP CRÍTICO PODE INTERROMPER OBJETIVOS

Se HP está extremamente baixo, recuperação pode interromper:

- trabalho;
- carreira;
- migração não urgente;
- socialização;
- busca não vital.

Mas não necessariamente:

- fuga de agressor;
- combate inevitável;
- procurar comida;
- procurar água.

Preserve contexto.

---

# 23. HP BAIXO DEVE AFETAR DECISÃO DE COMBATE

A Fase 4 já utiliza HP na força de combate.

Verificar também se um NPC em recuperação crítica não continua iniciando conflitos triviais.

HP baixo deve reduzir Utility de:

- ataque voluntário;
- ameaça física;
- perseguição arriscada.

E aumentar:

- fuga;
- rendição;
- recuperação;
- pedido de ajuda.

Não impedir autodefesa.

---

# 24. HP BAIXO DEVE AFETAR TRABALHO

Não proibir totalmente.

Porém:

HP muito baixo

pode reduzir Utility de trabalho pesado.

O personagem pode ainda trabalhar se:

- precisa desesperadamente;
- não possui outra solução;
- personalidade/contexto favorecem.

Não criar incapacidade absoluta sem motivo.

---

# 25. RECUPERAÇÃO DE DESESPERO

A Fase 4 terminou com desespero extremamente elevado.

Vespera chegou a média aproximada de 91,68 entre vivos.

Isso pode ser parcialmente resultado de:

- privação;
- pobreza;
- conflitos;
- perdas.

Não zerar isso artificialmente.

Mas um NPC que passa tempo com:

- fome controlada;
- sede controlada;
- HP melhorando;
- renda ou recursos suficientes;
- segurança;
- ausência de perseguição;
- apoio social;

deve recuperar parte do desespero ao longo do tempo.

---

# 26. DESESPERO NÃO DEVE DESAPARECER EM UMA REFEIÇÃO

Não fazer:

comeu
→ desperation -= 30.

Use recuperação gradual.

Exemplo conceitual:

condições materiais estáveis por várias horas/dias  
→ pequena queda acumulativa.

Perda grave, luto e grievance podem manter parte do desespero.

---

# 27. DIFERENCIAR FONTES DE DESESPERO

Sempre que possível, não tratar todo desespero como um único “nível de fome”.

Registrar contribuições:

- privação;
- pobreza;
- violência;
- perseguição;
- luto;
- humilhação;
- isolamento.

Não precisa criar sistema psicológico enorme.

Mas recuperação material deve poder reduzir principalmente a parcela material.

---

# 28. RESERVA CONTINUA IMPORTANTE

Preserve:

- food_reserve;
- compra preventiva;
- compra em lote;
- segunda ração;
- viagem.

A refeição começar antes não substitui reserva.

Conceitualmente:

`food_reserve`
= garantir comida futura.

`food`
= hora de fazer refeição.

`recovery`
= recuperar corpo após dano.

São problemas diferentes.

---

# 29. NÃO AUMENTAR RESERVA ALÉM DO NECESSÁRIO

Não usar Fase 4.1 para fazer NPC carregar dez rações.

Preserve alvo atual normal.

Viagem pode aumentar conforme duração conhecida.

---

# 30. LOD PRECISA CONSIDERAR LIMIAR DE REFEIÇÃO

Com decisões em:

1 / 3 / 6 / 12 horas,

um NPC background pode atravessar muito rapidamente a faixa normal.

Quando fome cruza limiar relevante, considere promoção temporária de decisão.

Exemplo:

background  
fome passou de 35/40.

Não necessariamente decisão imediata toda hora.

Mas não esperar automaticamente mais 12h.

Use mecanismo de promoção já existente.

---

# 31. RECOVERY TAMBÉM PODE PROMOVER LOD

NPC com:

HP <30

não deve permanecer 12h entre decisões de recuperação apenas porque está em background.

Promova temporariamente.

Quando estabilizar:

volta ao LOD normal.

---

# 32. NÃO REABRIR O PROBLEMA DE MORTE COM COMIDA

Manter regressões anteriores:

- comida possuída em emergência → comer;
- aquisição vital + refeição;
- viagem interrompida;
- descanso não vence alimentação fatal;
- empate não mata com alimento disponível.

Adicionar `steal_person` a essa semântica.

---

# 33. SOBREVIVÊNCIA NÃO SIGNIFICA IMORTALIDADE

Mortes por fome continuam possíveis quando:

- não existe alimento;
- não existe renda;
- comida não é conhecida;
- não existe rota;
- crime falha;
- ajuda falha;
- NPC está preso/perseguido;
- múltiplas necessidades vitais convergem;
- nenhuma ação disponível consegue salvá-lo a tempo.

Não usar taxa de morte baixa como objetivo.

---

# 34. TESTES — MANTER PEQUENO

A Fase 4 já reduziu a filosofia de testes.

Continuar.

Não adicionar 40 testes.

Adicionar aproximadamente:

**8–12 regressões direcionadas.**

---

# 35. TESTES ESSENCIAIS

## Teste 1 — steal_person em emergência

HP 1  
fome 100  
sem comida  
alvo presente com ração.

Se `steal_person` isolado não permite sobreviver:

não pode vencer uma alternativa real `steal_meal` biologicamente viável.

## Teste 2 — aquisição comum

HP crítico  
fome crítica  
compra possível.

Compra + refeição deve continuar funcionando.

## Teste 3 — refeição antecipada

NPC fome 36  
com comida  
sem prioridade crítica.

`eat` deve existir como solução válida.

Não precisa obrigatoriamente vencer uma prioridade muito maior.

## Teste 4 — sem comer cedo demais

fome 15  
comida disponível.

Não criar pressão relevante de refeição.

## Teste 5 — dano de fome

HP 100.

Dano de fome 20.

Resultado:

HP 80  
recoverable_deprivation_damage 20.

## Teste 6 — recuperação

HP 60  
40 recuperáveis por privação  
fome/sede baixas  
descanso.

Após horas adequadas:

HP sobe significativamente.

## Teste 7 — espada não vira dano recuperável

Dano de combate 30.

Comer e descansar brevemente não deve restaurar os 30 como recuperação fisiológica.

## Teste 8 — dano misto

30 fome +20 combate.

Recuperação fisiológica máxima rápida =30.

## Teste 9 — save/load

Persistir corretamente:

- HP;
- dano recuperável;
- recovery need;
- origem necessária.

## Teste 10 — LOD

HP crítico ou fome entrando na faixa de refeição deve antecipar decisão sem duplicar ações.

---

# 36. AUDITORIA CURTA

Rodar primeiro:

**500–1.000 horas**

em um mundo novo equivalente ao perfil da Fase 4.

Não rodar imediatamente 10.000h.

Registrar:

- mortes por fome;
- mortes com comida;
- fome média ao comer;
- HP médio ao comer;
- quantidade de refeições em fome 30–40;
- refeições 40–60;
- refeições 60–80;
- refeições 80+;
- dano fisiológico acumulado;
- dano fisiológico recuperado;
- HP baixo;
- recovery selecionada;
- recuperação completa;
- desespero.

---

# 37. MÉTRICA MAIS IMPORTANTE — REINCIDÊNCIA

Para cada NPC que alcança:

fome >=90

registrar se:

- sobrevive;
- come;
- recupera HP;
- volta a fome >=90;
- quantas vezes.

Queremos saber se existe padrão:

crise  
→ refeição  
→ crise  
→ refeição  
→ morte.

---

# 38. JANELAS DE RECUPERAÇÃO

Registrar episódios:

HP <30.

Depois acompanhar:

- 24h;
- 48h;
- 72h.

Classificar:

- morreu;
- continuou <30;
- recuperou 30–50;
- recuperou 50–70;
- recuperou >70.

Isso será mais útil que somente contar mortes.

---

# 39. DANOS POR ORIGEM

No relatório, separar:

- dano por fome;
- dano por sede;
- dano por combate;
- dano misto;
- HP recuperado de privação;
- HP recuperado por tratamento físico.

Não misturar.

---

# 40. AVALIAR IMPACTO SOBRE COMBATE

Verificar se recuperação melhor:

- reduz personagens lutando com HP extremamente baixo;
- altera rendições;
- altera fugas;
- altera mortes violentas.

Não rebalancear combate automaticamente.

Apenas observar.

---

# 41. AVALIAR IMPACTO SOBRE ECONOMIA

Comer mais cedo pode aumentar consumo.

Portanto medir:

- comida produzida;
- comida comprada;
- estoque;
- mercados vazios;
- preço;
- reserva;
- quantidade consumida por NPC/dia.

Não permitir que antecipação de refeição acidentalmente dobre demanda alimentar.

---

# 42. MEDIR CONSUMO REAL

Calcular:

`rations_per_persistent_npc_day`

antes/depois.

Se o valor subir excessivamente:

investigar threshold e desperdício.

Não aumentar produção automaticamente para compensar.

---

# 43. AUDITORIA LONGA

Somente depois da curta estabilizar.

Rodar:

**uma campanha global de 5.000 ou 10.000 horas.**

Não precisa repetir três seeds.

Preferencialmente usar uma seed conhecida para comparação, mas mundo novo.

Registrar versão/hash.

---

# 44. NÃO INVALIDAR RELATÓRIOS ANTERIORES

Preservar:

- Fase 4 oficial Mira;
- Vespera-47;
- saves;
- métricas;
- histórias.

A Fase 4.1 é nova versão.

Não sobrescrever resultados anteriores.

---

# 45. HISTÓRIAS EMERGENTES CONTINUAM SENDO AUDITADAS

Não focar somente em fisiologia.

Verificar se a recuperação afeta histórias.

Exemplos reais a procurar:

- personagem quase morre de fome e se recupera;
- volta ao trabalho depois;
- migra depois da crise;
- recebe ajuda;
- familiar cuida durante recuperação;
- ferido em combate e faminto possui recuperações diferentes;
- personagem que anteriormente morreria consegue continuar trajetória.

Não inventar histórias.

---

# 46. EVITAR "HOSPITALIZAÇÃO ETERNA"

Se recovery tiver prioridade alta demais:

NPC pode ficar eternamente:

descansa  
descansa  
descansa.

Quando HP recuperável acabou e condições físicas são adequadas:

Need deve satisfazer/baixar.

Se ainda existe dano físico:

tratamento/lesão usa seu próprio caminho.

---

# 47. CRITÉRIO DE SUCESSO

Não considerar sucesso porque:

“morreram menos.”

Considerar sucesso se:

1. `steal_person` não repetir morte com comida obtida mas não consumida quando existe solução imediata viável;
2. refeições começam antes da crise extrema;
3. NPCs podem sair de HP muito baixo após estabilizar alimentação/água;
4. dano por fome é recuperável de forma plausível;
5. dano de combate não é curado magicamente por alimentação;
6. HP baixo cria comportamento de recuperação;
7. desespero material pode cair quando condições melhoram;
8. consumo alimentar não explode;
9. economia permanece física;
10. histórias da Fase 4 continuam funcionando.

---

# 48. PERGUNTA QUE O RELATÓRIO PRECISA RESPONDER

No final, responda com evidência:

**“Quando um NPC quase morre de fome, consegue alimento e sai da emergência, ele realmente consegue se recuperar — ou apenas adia sua morte?”**

Mostre exemplos reais.

---

# 49. RELATÓRIO FINAL

Estrutura:

1. Resumo executivo.
2. Diagnóstico anterior.
3. `steal_person`.
4. Pipeline comum de aquisição alimentar.
5. Novo limiar de refeição.
6. Curva de prioridade alimentar.
7. Need de recuperação.
8. Origem do dano.
9. Dano recuperável por privação.
10. Dano físico.
11. Recuperação por descanso.
12. Integração com fome/sede.
13. Integração com combate.
14. Integração com LOD.
15. Desespero.
16. Testes direcionados.
17. Auditoria curta.
18. Auditoria longa.
19. Consumo alimentar.
20. Economia.
21. Mortalidade.
22. Reincidência de crises.
23. Recuperação de HP.
24. Histórias reais.
25. Limitações.
26. Bugs encontrados.
27. Recomendação para próxima fase.

---

# 50. PRINCÍPIO FINAL

Até agora o sistema aprendeu:

**“preciso conseguir comida antes de morrer.”**

A Fase 4.1 deve acrescentar:

**“depois de sobreviver, preciso recuperar meu corpo antes de voltar ao limite.”**

A diferença é fundamental.

Sobrevivência não é apenas impedir o HP de chegar a zero nesta hora.

Sobrevivência sustentável é:

crise  
→ aquisição  
→ consumo  
→ estabilização  
→ descanso  
→ recuperação  
→ retorno à vida normal.

É esse ciclo completo que a Fase 4.1 deve validar.