# FASE 5.2.1 — VALIDAÇÃO NATURAL DA LETALIDADE CORRIGIDA E AJUSTE RELIGIOSO MÍNIMO

## 0. OBJETIVO

Esta NÃO é uma nova fase estrutural.

Não adicionar grandes sistemas.

Não reformular combate, política, religião, personalidade ou ActionPressure.

A Fase 5.2 já implementou:

- LethalConsideration;
- LethalDecision persistente;
- histerese;
- ExecutionOpportunity;
- decisão terminal;
- PostKillAppraisal;
- DeathAffinity;
- sadismo;
- DivineAffinity;
- FaithHealth;
- presença divina regional;
- reação institucional a homicídios.

A campanha natural da Fase 5.2 ocorreu antes de correções importantes no caminho terminal.

Em especial, foi encontrado um caso em que:

```text
finish = 65.76
spare = 46.20
```

mas uma segunda competição genérica alterou o resultado para `spare`.

Esse bloqueio foi corrigido depois da campanha.

Portanto:

> NÃO recalibrar novamente a letalidade antes de observar a versão corrigida rodando naturalmente.

---

# 1. OBJETIVO PRINCIPAL

Executar uma campanha natural curta com a versão final corrigida da Fase 5.2 e responder:

```text
LethalDecision
→ LethalAttack
→ ExecutionOpportunity
→ TerminalDecision
→ finish / spare / capture / withdraw
→ CharacterKilled
→ PostKillAppraisal
```

O objetivo NÃO é produzir determinada quantidade de cadáveres.

O objetivo é verificar se o caminho completo agora consegue ocorrer naturalmente.

---

# 2. NÃO ALTERAR DANO

Não aumentar:

- dano;
- potência de arma;
- chance crítica;
- HP;
- frequência de ataque.

A Fase 5.2 já demonstrou grande quantidade de ataques com intenção letal.

O gargalo observado estava no desfecho terminal.

---

# 3. NÃO REDUZIR NOVAMENTE A BARREIRA LETAL

Não diminuir novamente os requisitos de:

```text
LethalConsideration
LethalDecision
```

A campanha anterior produziu:

```text
148 considerações
147 decisões
107 decisões que chegaram a ataque
632 ataques letais executados
30 oportunidades terminais
```

Logo:

> falta de intenção letal NÃO é atualmente o problema principal.

---

# 4. VALIDAR A ESCOLHA TERMINAL CORRIGIDA

Quando houver:

```text
ExecutionOpportunity
```

registrar obrigatoriamente:

- actor;
- target;
- LethalDecision;
- modo;
- causa original;
- ameaça atual;
- revenge/retribution;
- compassion;
- fear;
- attachment;
- DeathAffinity;
- sadism;
- divine/religious influence quando relevante;
- score de finish;
- score de spare;
- score de capture;
- score de help;
- score de withdraw;
- alternativa escolhida.

Não aplicar uma segunda Utility genérica depois disso.

A decisão terminal deve ser a decisão final daquele contexto.

---

# 5. SE FINISH VENCER

Se:

```text
finish
```

for realmente a alternativa vencedora e:

```text
target incapacitated
attacker present
attacker capable
LethalDecision active
```

então executar:

```text
CharacterKilled
death_context = deliberate_finish
```

sem novo teste arbitrário de coragem, agressividade ou Utility.

O NPC já:

1. decidiu matar;
2. chegou até a vítima;
3. venceu o confronto;
4. teve oportunidade terminal;
5. escolheu finalizar.

Não bloquear novamente a mesma decisão.

---

# 6. SE SPARE VENCER

Também preservar integralmente.

Não tentar produzir morte artificialmente.

Registrar por que:

```text
spare
```

venceu.

Exemplos possíveis:

- ameaça terminou;
- compaixão;
- vínculo;
- medo;
- autoridade;
- baixa retribuição;
- baixa DeathAffinity;
- contexto defensivo já resolvido.

---

# 7. DECISÕES LETAIS ATIVAS

A campanha anterior terminou com muitas decisões abertas.

Monitorar:

```text
active LethalDecision
```

por idade.

Registrar de forma compacta:

```text
<24h
24–72h
72–168h
>168h
```

e motivo de encerramento quando existir:

```text
target death learned
forgiveness
repair
reconciliation
new innocence evidence
fear
moral change
rumination decay
grievance resolved
```

O objetivo é verificar se histerese virou persistência plausível e NÃO memória eterna.

---

# 8. MORTE DO ALVO DEVE PODER ENCERRAR A DECISÃO — MAS SÓ QUANDO CONHECIDA

Se o alvo morrer:

```text
objective target death
```

NÃO apagar imediatamente a `LethalDecision` de quem não sabe.

Quando o agente aprender de forma suficientemente confiável:

```text
target is dead
```

a decisão deve ser resolvida/encerrada.

Preservar casos como:

> Silas continua procurando Ruan porque ainda não sabe que ele morreu.

Isso é comportamento correto.

---

# 9. TELEMETRIA DE CONSIDERAÇÃO

A campanha anterior teve:

```text
148 LethalConsideration
147 LethalDecision
```

porque `LethalConsideration` já representava um candidato que venceu uma etapa avançada.

Sem reformular a arquitetura, melhorar a telemetria para distinguir, quando barato:

```text
LethalCandidateEvaluated
LethalCandidateRejected
LethalConsideration
LethalDecision
```

Não registrar toda consulta por tick.

Registrar apenas transições relevantes.

O objetivo é saber futuramente:

> quantas vezes matar foi realmente plausível mas ainda rejeitado?

---

# 10. HIPÓTESE FUTURA — LINHA EXTREMA DE LETALIDADE

NÃO implementar nesta fase.

Deixar documentada a hipótese:

> pode existir futuramente uma faixa extremamente distante de pressão/compromisso letal na qual, caso exista oportunidade real de execução e nenhuma mudança factual relevante, o NPC finalize inevitavelmente.

Conceitualmente:

```text
ordinary lethal decision
→ terminal choice remains contextual

EXTREME irreversible lethal resolution
→ if valid execution opportunity exists:
   finish = guaranteed
```

Mas NÃO adicionar isso agora.

Primeiro observar a versão corrigida.

Registrar, entretanto, casos em que:

```text
LethalDecision intensity
WorldPressure
rumination
retribution
DeathAffinity
sadism
```

atinjam valores excepcionalmente altos.

Isso dará evidência para decidir depois se essa faixa extrema é realmente necessária.

---

# 11. POST-KILL

Caso aconteça uma morte deliberada natural:

executar obrigatoriamente:

```text
PostKillAppraisal
```

Registrar:

- culpa;
- vergonha;
- medo;
- alívio;
- orgulho;
- prazer;
- fascinação;
- numbness;
- grief;
- moral conflict.

Não exigir que todos tenham reação intensa.

---

# 12. DEATH AFFINITY

Se uma morte deliberada produzir:

```text
pleasure
pride
fascination
```

e o perfil for coerente:

permitir:

```text
DeathAffinityIncrease
```

Mas NÃO criar imediatamente:

```text
seek_killing
```

salvo se os requisitos atuais já justificarem.

Uma morte não cria assassino recorrente automaticamente.

---

# 13. SADISMO

Preservar:

```text
sadism != murderer
```

A campanha anterior já demonstrou um NPC com predisposição elevada ao sadismo que:

- agrediu;
- foi capturado;
- foi poupado;
- não matou;
- não ganhou DeathAffinity.

Isso é comportamento desejado.

Não aumentar ação violenta apenas por sadismo.

---

# 14. PEQUENO AJUSTE RELIGIOSO — DIFFERENTIATION OF ACTORS

A campanha anterior terminou com:

```text
Aurion Actors = 404
Neruma Actors = 404
Elar Actors = 404
```

e eram essencialmente as mesmas pessoas.

Isso indica que os valores usados para classificar atos alinhados estão amplos demais.

Não reformular religião.

Apenas tornar a classificação de `Actor` mais específica ao domínio e valores de cada Deus.

---

# 15. AURION — JUSTIÇA

Exemplos de atos potencialmente alinhados:

```text
punish known offender
resolve dispute fairly
protect falsely accused
investigate wrongdoing
report proven crime
enforce justified sentence
defend victim of injustice
```

Ajuda genérica pode contribuir pouco quando coerente.

Mas:

```text
help_person
```

sozinho não deve transformar automaticamente alguém em Actor de Aurion.

---

# 16. NERUMA — PROTEÇÃO

Exemplos:

```text
protect vulnerable
intervene in attack
escort endangered person
defend family/group member
provide emergency aid
rescue person
stand between aggressor and victim
```

Aqui ajuda/proteção pode possuir peso muito maior.

---

# 17. ELAR — CONHECIMENTO

Exemplos:

```text
discover important fact
teach
share reliable information
investigate successfully
correct false belief
preserve knowledge
solve information problem
expose false rumor
```

Ajudar alguém fisicamente não deve automaticamente tornar o NPC Actor de Elar.

---

# 18. SOBREPOSIÇÃO CONTINUA POSSÍVEL

Não tornar os Deuses artificialmente exclusivos.

Um mesmo evento pode agradar dois ou três Deuses quando realmente possuir significados compatíveis.

Exemplo:

```text
guard investigates false accusation
↓
Aurion: justice
Elar: truth/knowledge
```

Mas a coincidência total de centenas de Actors entre três divindades deve deixar de ser o padrão.

---

# 19. NÃO AUMENTAR INTERVENÇÃO DIVINA

Não mexer em:

- chance;
- Utility;
- custos;
- energia;
- thresholds de intervenção.

A campanha anterior já demonstrou que FaithHealth objetivo pode deteriorar enquanto o Deus continua sem saber.

Esse comportamento é correto.

---

# 20. RELATOS RELIGIOSOS

Sem criar um novo sistema grande, verificar apenas se os canais existentes conseguem eventualmente transmitir informações agregadas como:

```text
nossa congregação está diminuindo
nossos Actors estão desaparecendo
a fé rival está crescendo
```

Se não existir caminho natural utilizável, documentar como gargalo.

Não adicionar telepatia divina.

---

# 21. TESTES

Criar apenas aproximadamente:

```text
4–6 testes novos/ajustados
```

Foco:

1. `finish` vencedor realmente executa finalização;
2. `spare` vencedor continua poupando;
3. morte conhecida do alvo encerra decisão, morte desconhecida não;
4. decisão muito antiga pode desaparecer por resolução/ruminação sem timeout arbitrário;
5. Actors religiosos divergem entre Aurion/Neruma/Elar;
6. sobreposição coerente entre dois deuses ainda é possível.

Depois rodar pequeno smoke crítico.

Não repetir suíte completa de centenas de testes.

---

# 22. CAMPANHA NATURAL

Executar:

```text
1 seed nova
250–300 horas
```

Preferência:

```text
300h
```

Sem jogador.

Sem save anterior.

Não trocar seed.

Não reiniciar buscando assassinato.

Não mudar parâmetros durante execução.

Se bug estrutural invalidar a campanha cedo:

corrigir e permitir UM reinício com a mesma seed.

---

# 23. NÃO EXIGIR HOMICÍDIO

O resultado:

```text
0 deliberate kills
```

ainda pode ser válido.

Mas desta vez a campanha deve permitir responder:

> `finish` teve chance real de vencer na versão corrigida?

Se ocorrerem várias oportunidades terminais e `finish` nunca vencer mesmo em perfis/contextos extremamente favoráveis:

registrar como possível amortecimento residual.

Não corrigir durante a campanha.

---

# 24. MÉTRICAS PRINCIPAIS

Entregar funil:

```text
LethalCandidateEvaluated
LethalCandidateRejected
LethalConsideration
LethalDecision
LethalAttack
ExecutionOpportunity
TerminalFinishChosen
TerminalSpareChosen
TerminalCaptureChosen
TerminalWithdrawChosen
IntentionalCombatKill
DeliberateFinish
PostKillAppraisal
DeathAffinityIncrease
LethalDecisionResolved
LethalDecisionAbandoned
```

Se `CandidateEvaluated` for caro demais:

não registrar cada avaliação.

Usar transições compactas.

---

# 25. RELIGIÃO

Mostrar por Deus:

```text
Followers
Devoted
Cultists
Actors
```

e principalmente:

```text
unique Actors
Actors shared with God B
Actors shared with God C
```

Queremos verificar se os domínios realmente passaram a produzir comunidades comportamentais diferentes.

---

# 26. RELATÓRIO TÉCNICO

Criar relatório pequeno:

```text
RELATORIO_5_2_1.md
```

com:

- testes;
- campanha;
- funil letal;
- decisões abertas/resolvidas;
- terminal choices;
- mortes deliberadas;
- PostKill;
- DeathAffinity;
- idade das decisões;
- composição religiosa;
- overlap de Actors;
- gargalos;
- bugs.

Não repetir toda documentação da Fase 5.2.

---

# 27. HISTORIAS_REAIS.MD

Criar uma pequena crônica novamente.

NÃO transformar em relatório.

Começar com:

- seed;
- população;
- reinos;
- localidades;
- profissões principais;
- Deuses;
- composição religiosa resumida;
- primeiro acontecimento relevante.

Depois selecionar no máximo:

```text
5–6 histórias
```

Priorizar:

1. decisão letal que chegou ao terminal;
2. finish, se existir;
3. spare contextual convincente;
4. decisão que morreu porque o alvo morreu e a notícia chegou;
5. decisão persistindo porque a morte ainda era desconhecida;
6. comportamento religioso que diferenciou favor entre os Deuses.

Se nenhuma morte deliberada ocorrer:

não inventar.

Se houver:

contar também o pós-morte.

---

# 28. CRITÉRIO DE ENCERRAMENTO

Se a campanha corrigida demonstrar naturalmente pelo menos:

```text
LethalDecision
→ ExecutionOpportunity
→ decisão terminal coerente
```

e os testes provarem que `finish` consegue executar quando realmente vence:

não continuar mexendo na letalidade só porque houve poucas mortes.

Se aparecer `finish` natural + PostKill:

considerar o núcleo letal da Fase 5.2 validado.

---

# 29. NÃO IMPLEMENTAR A LINHA EXTREMA AINDA

Reforçando:

NÃO implementar nesta fase a regra:

```text
passou de X
→ se tiver oportunidade
→ mata 100%
```

Mas manter a hipótese documentada.

Depois da campanha, separar os casos mais extremos e responder:

> algum personagem chegou a um estado em que, narrativamente, seria estranho ele ainda reconsiderar a finalização?

Se SIM:

registrar os valores/contexto.

Isso será evidência para uma fase futura de:

```text
IrreversibleLethalResolution
```

ou equivalente.

---

# 30. RESULTADO ESPERADO

Quero terminar esta validação sabendo se o sistema corrigido consegue produzir naturalmente algo como:

```text
agressão
↓
LethalDecision
↓
perseguição
↓
combate
↓
incapacitação
↓
finish vence
↓
CharacterKilled
↓
PostKillAppraisal
```

ou:

```text
agressão
↓
LethalDecision
↓
combate
↓
incapacitação
↓
ameaça desaparece
↓
spare vence
↓
LethalDecision encerrada
```

Ambos são resultados válidos.

A pergunta desta fase NÃO é:

> “conseguimos matar alguém?”

É:

> “quando o mundo finalmente coloca alguém diante da escolha real de matar, a escolha final funciona de forma causal e definitiva?”

Não adicionar novos grandes sistemas até responder isso.