# Histórias detalhadas — Vespera-47

Mundo novo, sem jogador, 5.000 horas. Os títulos interpretam registros reais. Há ligações explícitas por fonte e sequências apenas temporais, identificadas separadamente. IDs distinguem nomes repetidos.

Catálogo integral: [todos os arcos/lotes e IDs](</home/hugo/Área de trabalho/procedrual/reports/lore_vespera47_5000h/CATALOGO_COMPLETO_DE_ARCOS.jsonl.gz>). Biografias: [todos os personagens](</home/hugo/Área de trabalho/procedrual/reports/lore_vespera47_5000h/CATALOGO_POR_PERSONAGEM.md>).

## L01 — Conflito com morte violenta e continuidade causal — Bela Alvor (#4586)

Arco **58239**; h1675→h2016; 116 fatos; 9 participantes diretos. Tipo: `causal_or_single`.

**Leitura da história:** em h1675, Normar, o primeiro registro deste recorte diz: Bela Alvor roubou provisão de Arthus Arven.

Elena Arven (#4620) matou Darin Arven (#4571) em h1794.

Entre as consequências registradas: Elena Arven causou a morte de Darin Arven em confronto. O último fato disponível neste recorte ocorreu em h2016; isso não implica que a disputa tenha terminado definitivamente.

Os elos se conectam por fonte de evento/necessidade executada; o registro da fonte demonstra a referência causal do agente, sem garantir que aquela informação seja completa ou que toda a vida esteja neste arco.

Desfechos presentes: CharacterKilled: 1.

**Limite de qualidade:** o arco contém muita repetição de agressões. Continuidade causal aparece, mas a frequência de golpes não equivale a novos objetivos ou capítulos distintos.

- **h1675 · evento#1408570 · ItemStolen**: Bela Alvor roubou provisão de Arthus Arven. [ator Bela Alvor (#4586); alvo Arthus Arven (#4615)]

  Necessidade `money`; prioridade 80.89700000000003; origem interna `economy`, sem fato externo de referência. Ação `steal_person`, score do objetivo 81.10. Avaliação das alternativas em h1675; objetivo criado em h1675. Resultado: Provisão real roubada.
  Antes: HP 29, fome 70, dinheiro 0, comida 0; raiva 86.4, ressentimento 98.1, desespero 94.7. Depois: HP 29, dinheiro 0, comida 1.

- **h1675 · evento#1408572 · ConflictStarted**: Arthus Arven iniciou confronto físico com Bela Alvor. [ator Arthus Arven (#4615); alvo Bela Alvor (#4586)]

  Necessidade `protection`; prioridade 73.668; fato#1408570, confiança 100%, origem direct. Ação `attack`, score do objetivo 122.44; alternativa `demand_return`=83.15. Avaliação das alternativas em h1675; objetivo criado em h1675. Resultado: Ataque causou 5 de dano real.
  Antes: HP 84, fome 40, dinheiro 9, comida 0; raiva 99.7, ressentimento 100.0, desespero 100.0. Depois: HP 84, dinheiro 9, comida 0.

- **h1675 · evento#1408573 · CharacterAttacked**: Arthus Arven feriu Bela Alvor em 5 HP. [ator Arthus Arven (#4615); alvo Bela Alvor (#4586)]

  Necessidade `protection`; prioridade 73.668; fato#1408570, confiança 100%, origem direct. Ação `attack`, score do objetivo 122.44; alternativa `demand_return`=83.15. Avaliação das alternativas em h1675; objetivo criado em h1675. Resultado: Ataque causou 5 de dano real.
  Antes: HP 84, fome 40, dinheiro 9, comida 0; raiva 99.7, ressentimento 100.0, desespero 100.0. Depois: HP 84, dinheiro 9, comida 0.

- **h1676 · evento#1409366 · CharacterAttacked**: Aldren Vale feriu Bela Alvor em 3 HP. [ator Aldren Vale (#4569); alvo Bela Alvor (#4586)]

  Necessidade `protection`; prioridade 78.226; fato#1408570, confiança 100%, origem direct. Ação `attack`, score do objetivo 109.34; alternativa `confront`=76.33. Avaliação das alternativas em h1676; objetivo criado em h1676. Resultado: Ataque causou 3 de dano real.
  Antes: HP 77, fome 50, dinheiro 11, comida 0; raiva 97.9, ressentimento 99.7, desespero 100.0. Depois: HP 77, dinheiro 11, comida 0.

- **h1677 · evento#1410123 · CharacterAttacked**: Aldren Vale feriu Bela Alvor em 5 HP. [ator Aldren Vale (#4569); alvo Bela Alvor (#4586)]

  Necessidade `protection`; prioridade 78.244; fato#1408570, confiança 100%, origem direct. Ação `attack`, score do objetivo 122.02; alternativa `defend`=89.38. Avaliação das alternativas em h1677; objetivo criado em h1677. Resultado: Ataque causou 5 de dano real.
  Antes: HP 77, fome 52, dinheiro 11, comida 0; raiva 97.6, ressentimento 99.7, desespero 100.0. Depois: HP 77, dinheiro 11, comida 0.

- **h1677 · evento#1410135 · CharacterAttacked**: Arthus Arven feriu Bela Alvor em 2 HP. [ator Arthus Arven (#4615); alvo Bela Alvor (#4586)]

  Necessidade `protection`; prioridade 73.604; fato#1408570, confiança 100%, origem direct. Ação `attack`, score do objetivo 136.04; alternativa `defend`=92.42. Avaliação das alternativas em h1677; objetivo criado em h1677. Resultado: Ataque causou 2 de dano real.
  Antes: HP 84, fome 44, dinheiro 9, comida 0; raiva 99.1, ressentimento 99.9, desespero 100.0. Depois: HP 84, dinheiro 9, comida 0.

- **h1794 · evento#1502715 · CharacterKilled**: Elena Arven causou a morte de Darin Arven em confronto. [ator Elena Arven (#4620); alvo Darin Arven (#4571)]

  Necessidade `protection`; prioridade 100; fato#1501899, confiança 100%, origem direct. Ação `attack`, score do objetivo 91.55; alternativa `stay_near`=86.05. Avaliação das alternativas em h1794; objetivo criado em h1794. Resultado: Ataque causou 14 de dano real.
  Antes: HP 100, fome 54, dinheiro 0, comida 0; raiva 99.4, ressentimento 99.9, desespero 100.0. Depois: HP 100, dinheiro 0, comida 0.

- **h1916 · evento#1599604 · PursuitSearch**: Aldren Arven verificou a última localização conhecida sem encontrar o alvo. [ator Aldren Arven (#4617); alvo sem personagem identificado]
- **h1917 · evento#1600482 · PursuitSearch**: Aldren Arven verificou a última localização conhecida sem encontrar o alvo. [ator Aldren Arven (#4617); alvo sem personagem identificado]
- **h1992 · evento#1659525 · CharacterConfronted**: Aldren Arven: confront diante de Elena Arven. [ator Aldren Arven (#4617); alvo Elena Arven (#4620)]

  Necessidade `pursuit`; prioridade 84.9; fato#1528795 fora da memória curta amostrada; necessidade/caso pode conservar referência própria. Ação `confront`, score do objetivo 78.10; alternativa `attack`=71.65. Avaliação das alternativas em h1992; objetivo criado em h1992. Resultado: Interação estruturada registrada: confront.
  Antes: HP 84, fome 58, dinheiro 9, comida 0; raiva 98.8, ressentimento 99.8, desespero 100.0. Depois: HP 84, dinheiro 9, comida 0.

- **h2016 · evento#1678242 · PursuitSearch**: Arthus Arven verificou a última localização conhecida sem encontrar o alvo. [ator Arthus Arven (#4615); alvo sem personagem identificado]

  Necessidade `protection`; prioridade 74.108; fato#1659525, confiança 100%, origem direct. Ação `pursue`, score do objetivo 99.25. Avaliação das alternativas em h2016; objetivo criado em h2016. Resultado: Busca local sem encontro; não consulta posição remota.
  Antes: HP 61, fome 42, dinheiro 9, comida 0; raiva 98.2, ressentimento 99.8, desespero 100.0. Depois: HP 61, dinheiro 9, comida 0.

Fatos do arco não exibidos neste recorte: 105. IDs integrais no catálogo.

## L02 — Conflito com morte violenta e continuidade causal — Mira Solaris (#798)

Arco **93800**; h2789→h3104; 42 fatos; 6 participantes diretos. Tipo: `causal_or_single`.

**Leitura da história:** em h2789, Dormar, o primeiro registro deste recorte diz: Mira Solaris roubou provisão de Cael Ferros.

Aldren Kars (#3547) matou Cael Ferros (#3522) em h2847.

Entre as consequências registradas: Aldren Kars causou a morte de Cael Ferros em confronto. O último fato disponível neste recorte ocorreu em h3104; isso não implica que a disputa tenha terminado definitivamente.

Os elos se conectam por fonte de evento/necessidade executada; o registro da fonte demonstra a referência causal do agente, sem garantir que aquela informação seja completa ou que toda a vida esteja neste arco.

Desfechos presentes: CharacterKilled: 1.

**Limite de qualidade:** o arco contém muita repetição de agressões. Continuidade causal aparece, mas a frequência de golpes não equivale a novos objetivos ou capítulos distintos.

- **h2789 · evento#2270546 · ItemStolen**: Mira Solaris roubou provisão de Cael Ferros. [ator Mira Solaris (#798); alvo Cael Ferros (#3522)]

  Necessidade `money`; prioridade 96.0; origem interna `economy`, sem fato externo de referência. Ação `steal_person`, score do objetivo 59.60. Avaliação das alternativas em h2789; objetivo criado em h2789. Resultado: Provisão real roubada.
  Antes: HP 40, fome 42, dinheiro 3, comida 1; raiva 97.7, ressentimento 99.7, desespero 100.0. Depois: HP 40, dinheiro 3, comida 2.

- **h2789 · evento#2270952 · ConflictStarted**: Cael Ferros iniciou confronto físico com Mira Solaris. [ator Cael Ferros (#3522); alvo Mira Solaris (#798)]

  Necessidade `revenge`; prioridade 73.128; fato#2270546, confiança 100%, origem direct. Ação `attack`, score do objetivo 113.07; alternativa `denounce`=90.85. Avaliação das alternativas em h2789; objetivo criado em h2789. Resultado: Ataque causou 2 de dano real.
  Antes: HP 57, fome 64, dinheiro 9, comida 0; raiva 99.7, ressentimento 100.0, desespero 100.0. Depois: HP 57, dinheiro 9, comida 0.

- **h2789 · evento#2270953 · CharacterAttacked**: Cael Ferros feriu Mira Solaris em 2 HP. [ator Cael Ferros (#3522); alvo Mira Solaris (#798)]

  Necessidade `revenge`; prioridade 73.128; fato#2270546, confiança 100%, origem direct. Ação `attack`, score do objetivo 113.07; alternativa `denounce`=90.85. Avaliação das alternativas em h2789; objetivo criado em h2789. Resultado: Ataque causou 2 de dano real.
  Antes: HP 57, fome 64, dinheiro 9, comida 0; raiva 99.7, ressentimento 100.0, desespero 100.0. Depois: HP 57, dinheiro 9, comida 0.

- **h2790 · evento#2271700 · CharacterAttacked**: Cael Ferros feriu Mira Solaris em 3 HP. [ator Cael Ferros (#3522); alvo Mira Solaris (#798)]

  Necessidade `revenge`; prioridade 73.096; fato#2270546, confiança 100%, origem direct. Ação `attack`, score do objetivo 138.12; alternativa `defend`=90.91. Avaliação das alternativas em h2790; objetivo criado em h2790. Resultado: Ataque causou 3 de dano real.
  Antes: HP 57, fome 66, dinheiro 9, comida 0; raiva 99.4, ressentimento 99.9, desespero 100.0. Depois: HP 57, dinheiro 9, comida 0.

- **h2791 · evento#2272459 · CharacterAttacked**: Cael Ferros feriu Mira Solaris em 3 HP. [ator Cael Ferros (#3522); alvo Mira Solaris (#798)]

  Necessidade `revenge`; prioridade 73.064; fato#2270546, confiança 100%, origem direct. Ação `attack`, score do objetivo 138.27; alternativa `denounce`=90.85. Avaliação das alternativas em h2791; objetivo criado em h2791. Resultado: Ataque causou 3 de dano real.
  Antes: HP 57, fome 68, dinheiro 9, comida 0; raiva 99.1, ressentimento 99.9, desespero 100.0. Depois: HP 57, dinheiro 9, comida 0.

- **h2792 · evento#2273272 · CharacterAttacked**: Cael Ferros feriu Mira Solaris em 3 HP. [ator Cael Ferros (#3522); alvo Mira Solaris (#798)]

  Necessidade `revenge`; prioridade 73.032; fato#2270546, confiança 100%, origem direct. Ação `attack`, score do objetivo 138.44; alternativa `denounce`=90.85. Avaliação das alternativas em h2792; objetivo criado em h2792. Resultado: Ataque causou 3 de dano real.
  Antes: HP 57, fome 70, dinheiro 9, comida 0; raiva 98.8, ressentimento 99.8, desespero 100.0. Depois: HP 57, dinheiro 9, comida 0.

- **h2847 · evento#2314555 · CharacterKilled**: Aldren Kars causou a morte de Cael Ferros em confronto. [ator Aldren Kars (#3547); alvo Cael Ferros (#3522)]

  Necessidade `protection`; prioridade 97.88600000000002; fato#2271700, confiança 30%, origem rumor. Ação `attack`, score do objetivo 144.53; alternativa `denounce`=83.90. Avaliação das alternativas em h2847; objetivo criado em h2847. Resultado: Ataque causou 16 de dano real.
  Antes: HP 90, fome 64, dinheiro 2, comida 1; raiva 94.4, ressentimento 99.9, desespero 100.0. Depois: HP 90, dinheiro 2, comida 1.

- **h2942 · evento#2385353 · ProtectionGiven**: Arthus Alvor permaneceu próximo de Mira Solaris. [ator Arthus Alvor (#783); alvo Mira Solaris (#798)]

  Necessidade `protection`; prioridade 93.596; fato#2275634, confiança 30%, origem rumor. Ação `stay_near`, score do objetivo 71.20. Avaliação das alternativas em h2942; objetivo criado em h2942. Resultado: Acompanhou o protegido.
  Antes: HP 100, fome 62, dinheiro 16, comida 0; raiva 70.0, ressentimento 95.9, desespero 77.3. Depois: HP 100, dinheiro 16, comida 0.

- **h3048 · evento#2464700 · ThreatReported**: Darin Douran denunciou um acontecimento conhecido a Arthus Alvor. [ator Darin Douran (#801); alvo Arthus Alvor (#783)]

  Necessidade `protection`; prioridade 100; fato#2275634, confiança 30%, origem rumor. Ação `denounce`, score do objetivo 68.70; alternativa `pursue`=60.35. Avaliação das alternativas em h3048; objetivo criado em h3048. Resultado: Denúncia registrada por autoridade que já conhece o fato.
  Antes: HP 100, fome 68, dinheiro 3, comida 2; raiva 99.7, ressentimento 100.0, desespero 100.0. Depois: HP 100, dinheiro 3, comida 2.

- **h3104 · evento#2506301 · ThreatReported**: Arthus Alvor denunciou um acontecimento conhecido a Darin Douran. [ator Arthus Alvor (#783); alvo Darin Douran (#801)]

  Necessidade `protection`; prioridade 98.132; fato#2275634, confiança 30%, origem rumor. Ação `denounce`, score do objetivo 88.70. Avaliação das alternativas em h3104; objetivo criado em h3098. Resultado: Denúncia registrada por autoridade que já conhece o fato.
  Antes: HP 100, fome 66, dinheiro 1, comida 0; raiva 60.5, ressentimento 97.6, desespero 62.7. Depois: HP 100, dinheiro 1, comida 0.

Fatos do arco não exibidos neste recorte: 32. IDs integrais no catálogo.

## L03 — Conflito com morte violenta e continuidade causal — Bela Vale (#1266)

Arco **38361**; h1086→h1354; 44 fatos; 8 participantes diretos. Tipo: `causal_or_single`.

**Leitura da história:** em h1086, Normar, o primeiro registro deste recorte diz: Bela Vale roubou provisão de Nora Luar.

Darin Arven (#4571) matou Arthus Luar (#4594) em h1283.

Entre as consequências registradas: Darin Arven causou a morte de Arthus Luar em confronto. O último fato disponível neste recorte ocorreu em h1354; isso não implica que a disputa tenha terminado definitivamente.

Os elos se conectam por fonte de evento/necessidade executada; o registro da fonte demonstra a referência causal do agente, sem garantir que aquela informação seja completa ou que toda a vida esteja neste arco.

Desfechos presentes: CharacterKilled: 1.

- **h1086 · evento#927099 · ItemStolen**: Bela Vale roubou provisão de Nora Luar. [ator Bela Vale (#1266); alvo Nora Luar (#4592)]

  Necessidade `money`; prioridade 87.4; origem interna `economy`, sem fato externo de referência. Ação `steal_person`, score do objetivo 20.90. Avaliação das alternativas em h1086; objetivo criado em h1086. Resultado: Provisão real roubada.
  Antes: HP 100, fome 54, dinheiro 0, comida 0; raiva 99.3, ressentimento 99.9, desespero 100.0. Depois: HP 100, dinheiro 0, comida 1.

- **h1086 · evento#927101 · WantedIssued**: Darin Arven registrou procura por Bela Vale. [ator Darin Arven (#4571); alvo Normar (cidade#1257)]
- **h1086 · evento#927536 · GuardResponded**: Darin Arven interveio no roubo e cobrou 0 moedas de Bela Vale. [ator Darin Arven (#4571); alvo Bela Vale (#1266)]

  Necessidade `security`; prioridade 82.95; fato#927099, confiança 100%, origem direct. Ação `secure`, score do objetivo 79.33. Avaliação das alternativas em h1086; objetivo criado em h1086. Resultado: Suspeito encontrado; intervenção registrada.
  Antes: HP 95, fome 42, dinheiro 8, comida 1; raiva 99.5, ressentimento 99.9, desespero 100.0. Depois: HP 95, dinheiro 8, comida 1.

- **h1131 · evento#964437 · CharacterAttacked**: Arthus Luar feriu Bela Vale em 9 HP. [ator Arthus Luar (#4594); alvo Bela Vale (#1266)]

  Necessidade `protection`; prioridade 82.95000000000002; fato#927099, confiança 100%, origem direct. Ação `attack`, score do objetivo 89.91; alternativa `denounce`=86.95. Avaliação das alternativas em h1131; objetivo criado em h1131. Resultado: Ataque causou 9 de dano real.
  Antes: HP 87, fome 55, dinheiro 3, comida 0; raiva 86.9, ressentimento 98.2, desespero 100.0. Depois: HP 87, dinheiro 3, comida 0.

- **h1132 · evento#965260 · CharacterAttacked**: Darin Arven feriu Arthus Luar em 11 HP. [ator Darin Arven (#4571); alvo Arthus Luar (#4594)]

  Necessidade `protection`; prioridade 100; fato#964437, confiança 100%, origem direct. Ação `attack`, score do objetivo 80.51; alternativa `denounce`=74.65. Avaliação das alternativas em h1132; objetivo criado em h1132. Resultado: Ataque causou 11 de dano real.
  Antes: HP 100, fome 54, dinheiro 1, comida 2; raiva 96.4, ressentimento 99.5, desespero 100.0. Depois: HP 100, dinheiro 1, comida 2.

- **h1132 · evento#965265 · CharacterAttacked**: Arthus Luar feriu Darin Arven em 7 HP. [ator Arthus Luar (#4594); alvo Darin Arven (#4571)]

  Necessidade `response`; prioridade 89.968; fato#965260, confiança 100%, origem direct. Ação `attack`, score do objetivo 104.15; alternativa `defend`=97.28. Avaliação das alternativas em h1132; objetivo criado em h1132. Resultado: Ataque causou 7 de dano real.
  Antes: HP 76, fome 57, dinheiro 3, comida 0; raiva 99.7, ressentimento 100.0, desespero 100.0. Depois: HP 76, dinheiro 3, comida 0.

- **h1133 · evento#966048 · CharacterAttacked**: Darin Arven feriu Arthus Luar em 13 HP. [ator Darin Arven (#4571); alvo Arthus Luar (#4594)]

  Necessidade `protection`; prioridade 100; fato#964437, confiança 100%, origem direct. Ação `attack`, score do objetivo 107.09; alternativa `defend`=82.12. Avaliação das alternativas em h1133; objetivo criado em h1133. Resultado: Ataque causou 13 de dano real.
  Antes: HP 93, fome 56, dinheiro 1, comida 2; raiva 99.7, ressentimento 100.0, desespero 100.0. Depois: HP 93, dinheiro 1, comida 2.

- **h1283 · evento#1089167 · CharacterKilled**: Darin Arven causou a morte de Arthus Luar em confronto. [ator Darin Arven (#4571); alvo Arthus Luar (#4594)]

  Necessidade `pursuit`; prioridade 82.0; fato#964437 fora da memória curta amostrada; necessidade/caso pode conservar referência própria. Ação `attack`, score do objetivo 120.70; alternativa `defend`=81.72. Avaliação das alternativas em h1283; objetivo criado em h1283. Resultado: Ataque causou 14 de dano real.
  Antes: HP 100, fome 76, dinheiro 5, comida 1; raiva 97.0, ressentimento 99.6, desespero 100.0. Depois: HP 100, dinheiro 5, comida 1.

  Conhecimento familiar: Nora Luar (#4592) recebeu RemainsLocated em h1297, confiança 100%; pressões registradas: [('grief', 'active')]. Isso registra recepção/estado, não uma vingança concluída.

- **h1298 · evento#1101290 · PursuitSearch**: Aldren Arven verificou a última localização conhecida sem encontrar o alvo. [ator Aldren Arven (#4617); alvo sem personagem identificado]

  Necessidade `protection`; prioridade 97.108; fato#1079074, confiança 100%, origem direct. Ação `pursue`, score do objetivo 90.10; alternativa `ask_personal_help`=50.20. Avaliação das alternativas em h1298; objetivo criado em h1298. Resultado: Busca local sem encontro; não consulta posição remota.
  Antes: HP 100, fome 70, dinheiro 12, comida 0; raiva 98.2, ressentimento 99.8, desespero 100.0. Depois: HP 100, dinheiro 12, comida 0.

- **h1299 · evento#1102134 · PursuitSearch**: Aldren Arven verificou a última localização conhecida sem encontrar o alvo. [ator Aldren Arven (#4617); alvo sem personagem identificado]
- **h1301 · evento#1103695 · PursuitSearch**: Aldren Arven verificou a última localização conhecida sem encontrar o alvo. [ator Aldren Arven (#4617); alvo sem personagem identificado]
- **h1354 · evento#1146313 · SuspectLocated**: Aldren Luar encontrou a pessoa procurada. [ator Aldren Luar (#4589); alvo Darin Arven (#4571)]

  Necessidade `protection`; prioridade 87.0635; fato#1087446, confiança 30%, origem rumor. Ação `pursue`, score do objetivo 65.35; alternativa `denounce`=60.90. Avaliação das alternativas em h1354; objetivo criado em h1354. Resultado: Pessoa localizada fisicamente.
  Antes: HP 100, fome 56, dinheiro 0, comida 0; raiva 1.7, ressentimento 3.8, desespero 100.0. Depois: HP 100, dinheiro 0, comida 0.

Fatos do arco não exibidos neste recorte: 32. IDs integrais no catálogo.

## L04 — Conflito com morte violenta e continuidade causal — Marie Stone (#1136)

Arco **33441**; h950→h1150; 69 fatos; 6 participantes diretos. Tipo: `causal_or_single`.

**Leitura da história:** em h950, Arthon, o primeiro registro deste recorte diz: Marie Stone roubou comida no mercado de Arthon.

Silas Montes (#4293) matou Darin Stone (#4259) em h981.

Entre as consequências registradas: Silas Montes causou a morte de Darin Stone em confronto. O último fato disponível neste recorte ocorreu em h1150; isso não implica que a disputa tenha terminado definitivamente.

Os elos se conectam por fonte de evento/necessidade executada; o registro da fonte demonstra a referência causal do agente, sem garantir que aquela informação seja completa ou que toda a vida esteja neste arco.

Desfechos presentes: CharacterKilled: 1.

**Limite de qualidade:** o arco contém muita repetição de agressões. Continuidade causal aparece, mas a frequência de golpes não equivale a novos objetivos ou capítulos distintos.

- **h950 · evento#812105 · ItemStolen**: Marie Stone roubou comida no mercado de Arthon. [ator Marie Stone (#1136); alvo Arthon (cidade#1127)]

  Necessidade `food`; prioridade 100; origem interna `physiology`, sem fato externo de referência. Ação `steal`, score do objetivo 76.20; alternativa `forage`=56.50. Avaliação das alternativas em h950; objetivo criado em h946. Resultado: Alimento roubado.
  Antes: HP 54, fome 92, dinheiro 0, comida 0; raiva 10.6, ressentimento 88.0, desespero 26.6. Depois: HP 54, dinheiro 0, comida 1.

- **h951 · evento#813284 · ConflictStarted**: Darin Stone iniciou confronto físico com Marie Stone. [ator Darin Stone (#4259); alvo Marie Stone (#1136)]

  Necessidade `protection`; prioridade 63.42200000000001; fato#812105, confiança 100%, origem direct. Ação `attack`, score do objetivo 91.18; alternativa `confront`=74.65. Avaliação das alternativas em h951; objetivo criado em h951. Resultado: Ataque causou 5 de dano real.
  Antes: HP 100, fome 41, dinheiro 0, comida 0; raiva 75.8, ressentimento 99.8, desespero 100.0. Depois: HP 100, dinheiro 0, comida 0.

- **h951 · evento#813285 · CharacterAttacked**: Darin Stone feriu Marie Stone em 5 HP. [ator Darin Stone (#4259); alvo Marie Stone (#1136)]

  Necessidade `protection`; prioridade 63.42200000000001; fato#812105, confiança 100%, origem direct. Ação `attack`, score do objetivo 91.18; alternativa `confront`=74.65. Avaliação das alternativas em h951; objetivo criado em h951. Resultado: Ataque causou 5 de dano real.
  Antes: HP 100, fome 41, dinheiro 0, comida 0; raiva 75.8, ressentimento 99.8, desespero 100.0. Depois: HP 100, dinheiro 0, comida 0.

- **h952 · evento#814074 · CharacterAttacked**: Darin Stone feriu Marie Stone em 1 HP. [ator Darin Stone (#4259); alvo Marie Stone (#1136)]

  Necessidade `protection`; prioridade 63.54000000000001; fato#812105, confiança 100%, origem direct. Ação `attack`, score do objetivo 116.48; alternativa `defend`=92.52. Avaliação das alternativas em h952; objetivo criado em h952. Resultado: Ataque causou 1 de dano real.
  Antes: HP 100, fome 43, dinheiro 0, comida 0; raiva 75.5, ressentimento 99.8, desespero 100.0. Depois: HP 100, dinheiro 0, comida 0.

- **h953 · evento#814853 · CharacterAttacked**: Darin Stone feriu Marie Stone em 1 HP. [ator Darin Stone (#4259); alvo Marie Stone (#1136)]

  Necessidade `protection`; prioridade 63.658000000000015; fato#812105, confiança 100%, origem direct. Ação `attack`, score do objetivo 116.42; alternativa `defend`=92.48. Avaliação das alternativas em h953; objetivo criado em h953. Resultado: Ataque causou 1 de dano real.
  Antes: HP 100, fome 45, dinheiro 0, comida 0; raiva 75.2, ressentimento 99.7, desespero 100.0. Depois: HP 100, dinheiro 0, comida 0.

- **h954 · evento#815216 · CharacterAttacked**: Marie Stone feriu Darin Stone em 3 HP. [ator Marie Stone (#1136); alvo Darin Stone (#4259)]

  Necessidade `response`; prioridade 90.40400000000001; fato#814853, confiança 100%, origem direct. Ação `attack`, score do objetivo 90.80; alternativa `defend`=89.26. Avaliação das alternativas em h954; objetivo criado em h954. Resultado: Ataque causou 3 de dano real.
  Antes: HP 47, fome 60, dinheiro 0, comida 0; raiva 99.6, ressentimento 100.0, desespero 27.5. Depois: HP 47, dinheiro 0, comida 0.

- **h981 · evento#838882 · CharacterKilled**: Silas Montes causou a morte de Darin Stone em confronto. [ator Silas Montes (#4293); alvo Darin Stone (#4259)]

  Necessidade `protection`; prioridade 97.674; fato#816574, confiança 30%, origem rumor. Ação `attack`, score do objetivo 96.09; alternativa `confront`=77.52. Avaliação das alternativas em h981; objetivo criado em h981. Resultado: Ataque causou 11 de dano real.
  Antes: HP 100, fome 58, dinheiro 9, comida 0; raiva 87.1, ressentimento 98.3, desespero 100.0. Depois: HP 100, dinheiro 9, comida 0.

- **h1124 · evento#958599 · PursuitSearch**: Silas Montes verificou a última localização conhecida sem encontrar o alvo. [ator Silas Montes (#4293); alvo sem personagem identificado]

  Necessidade `pursuit`; prioridade 82.0; fato#856216 fora da memória curta amostrada; necessidade/caso pode conservar referência própria. Ação `pursue`, score do objetivo 91.05. Avaliação das alternativas em h1124; objetivo criado em h1124. Resultado: Busca local sem encontro; não consulta posição remota.
  Antes: HP 100, fome 64, dinheiro 7, comida 0; raiva 79.7, ressentimento 97.0, desespero 100.0. Depois: HP 100, dinheiro 7, comida 0.

- **h1131 · evento#964390 · PursuitSearch**: Silas Montes verificou a última localização conhecida sem encontrar o alvo. [ator Silas Montes (#4293); alvo sem personagem identificado]
- **h1134 · evento#966856 · PursuitSearch**: Silas Montes verificou a última localização conhecida sem encontrar o alvo. [ator Silas Montes (#4293); alvo sem personagem identificado]
- **h1150 · evento#979373 · CharacterConfronted**: Aldren Luar: confront diante de Arthus Bruma. [ator Aldren Luar (#1139); alvo Arthus Bruma (#1157)]

  Necessidade `pursuit`; prioridade 82.0; fato#829603 fora da memória curta amostrada; necessidade/caso pode conservar referência própria. Ação `confront`, score do objetivo 59.83; alternativa `attack`=60.11. Avaliação das alternativas em h1150; objetivo criado em h1150. Resultado: Interação estruturada registrada: confront.
  Antes: HP 100, fome 68, dinheiro 2, comida 0; raiva 94.6, ressentimento 99.3, desespero 98.4. Depois: HP 100, dinheiro 2, comida 0.

Fatos do arco não exibidos neste recorte: 58. IDs integrais no catálogo.

## L05 — Conflito com morte violenta e continuidade causal — Lyra Arven (#4684)

Arco **108333**; h3260→h3454; 30 fatos; 5 participantes diretos. Tipo: `causal_or_single`.

**Leitura da história:** em h3260, Silvia, o primeiro registro deste recorte diz: Lyra Arven roubou comida no mercado de Silvia.

Bela Ferros (#4675) matou Marie Montes (#4721) em h3433.

Entre as consequências registradas: Bela Ferros causou a morte de Marie Montes em confronto. O último fato disponível neste recorte ocorreu em h3454; isso não implica que a disputa tenha terminado definitivamente.

Os elos se conectam por fonte de evento/necessidade executada; o registro da fonte demonstra a referência causal do agente, sem garantir que aquela informação seja completa ou que toda a vida esteja neste arco.

Desfechos presentes: CharacterKilled: 1.

- **h3260 · evento#2620982 · ItemStolen**: Lyra Arven roubou comida no mercado de Silvia. [ator Lyra Arven (#4684); alvo Silvia (cidade#1304)]

  Necessidade `food`; prioridade 100; origem interna `physiology`, sem fato externo de referência. Ação `steal`, score do objetivo 56.43; alternativa `forage`=45.50. Avaliação das alternativas em h3260; objetivo criado em h3260. Resultado: Alimento roubado.
  Antes: HP 25, fome 97, dinheiro 1, comida 0; raiva 99.8, ressentimento 100.0, desespero 100.0. Depois: HP 25, dinheiro 1, comida 1.

- **h3260 · evento#2620984 · WantedIssued**: Marie Montes registrou procura por Lyra Arven. [ator Marie Montes (#4721); alvo Silvia (cidade#1304)]
- **h3260 · evento#2620992 · CharacterAttacked**: Marie Montes feriu Lyra Arven em 5 HP. [ator Marie Montes (#4721); alvo Lyra Arven (#4684)]

  Necessidade `security`; prioridade 86.2; fato#2620982, confiança 100%, origem direct. Ação `attack`, score do objetivo 134.60; alternativa `secure`=90.67. Avaliação das alternativas em h3260; objetivo criado em h3260. Resultado: Ataque causou 5 de dano real.
  Antes: HP 49, fome 44, dinheiro 10, comida 0; raiva 98.9, ressentimento 99.8, desespero 100.0. Depois: HP 49, dinheiro 10, comida 0.

- **h3261 · evento#2621726 · CharacterAttacked**: Marie Montes feriu Lyra Arven em 6 HP. [ator Marie Montes (#4721); alvo Lyra Arven (#4684)]

  Necessidade `security`; prioridade 86.35; fato#2620982, confiança 100%, origem direct. Ação `attack`, score do objetivo 134.77; alternativa `secure`=90.67. Avaliação das alternativas em h3261; objetivo criado em h3261. Resultado: Ataque causou 6 de dano real.
  Antes: HP 49, fome 46, dinheiro 10, comida 0; raiva 98.6, ressentimento 99.8, desespero 100.0. Depois: HP 49, dinheiro 10, comida 0.

- **h3261 · evento#2621740 · CharacterAttacked**: Lyra Corven feriu Lyra Arven em 5 HP. [ator Lyra Corven (#4846); alvo Lyra Arven (#4684)]

  Necessidade `protection`; prioridade 82.23599999999999; fato#2620982, confiança 100%, origem direct. Ação `attack`, score do objetivo 84.34; alternativa `confront`=71.61. Avaliação das alternativas em h3261; objetivo criado em h3261. Resultado: Ataque causou 5 de dano real.
  Antes: HP 100, fome 68, dinheiro 5, comida 2; raiva 99.4, ressentimento 99.9, desespero 42.0. Depois: HP 100, dinheiro 5, comida 2.

- **h3262 · evento#2622450 · CharacterAttacked**: Marie Montes feriu Lyra Corven em 8 HP. [ator Marie Montes (#4721); alvo Lyra Corven (#4846)]

  Necessidade `protection`; prioridade 100; fato#2621740, confiança 100%, origem direct. Ação `attack`, score do objetivo 92.65; alternativa `denounce`=80.25. Avaliação das alternativas em h3262; objetivo criado em h3262. Resultado: Ataque causou 8 de dano real.
  Antes: HP 49, fome 48, dinheiro 10, comida 0; raiva 98.3, ressentimento 99.8, desespero 100.0. Depois: HP 49, dinheiro 10, comida 0.

- **h3433 · evento#2748447 · CharacterKilled**: Bela Ferros causou a morte de Marie Montes em confronto. [ator Bela Ferros (#4675); alvo Marie Montes (#4721)]

  Necessidade `protection`; prioridade 94.454; fato#2744946, confiança 100%, origem direct. Ação `attack`, score do objetivo 105.84; alternativa `ask_personal_help`=89.95. Avaliação das alternativas em h3433; objetivo criado em h3433. Resultado: Ataque causou 13 de dano real.
  Antes: HP 94, fome 68, dinheiro 20, comida 1; raiva 99.1, ressentimento 99.9, desespero 75.9. Depois: HP 94, dinheiro 20, comida 1.

  Conhecimento familiar: Elena Montes (#4719) recebeu RemainsLocated em h3704, confiança 100%; pressões registradas: [('grief', 'active')]. Isso registra recepção/estado, não uma vingança concluída.

- **h3439 · evento#2752782 · PursuitSearch**: Lyra Corven verificou a última localização conhecida sem encontrar o alvo. [ator Lyra Corven (#4846); alvo sem personagem identificado]

  Necessidade `response`; prioridade 91.266; fato#2744946, confiança 100%, origem direct. Ação `pursue`, score do objetivo 86.20. Avaliação das alternativas em h3439; objetivo criado em h3435. Resultado: Busca local sem encontro; não consulta posição remota.
  Antes: HP 97, fome 64, dinheiro 6, comida 0; raiva 96.4, ressentimento 99.5, desespero 76.2. Depois: HP 97, dinheiro 6, comida 0.

- **h3449 · evento#2759924 · PursuitSearch**: Bela Solaris verificou a última localização conhecida sem encontrar o alvo. [ator Bela Solaris (#1392); alvo sem personagem identificado]

  Necessidade `protection`; prioridade 97.00800000000001; fato#2747733, confiança 100%, origem direct. Ação `pursue`, score do objetivo 81.45; alternativa `denounce`=80.70. Avaliação das alternativas em h3449; objetivo criado em h3449. Resultado: Busca local sem encontro; não consulta posição remota.
  Antes: HP 80, fome 61, dinheiro 0, comida 0; raiva 99.2, ressentimento 99.8, desespero 100.0. Depois: HP 80, dinheiro 0, comida 0.

- **h3454 · evento#2763279 · ThreatAvoided**: Bela Solaris buscou um local seguro conhecido. [ator Bela Solaris (#1392); alvo sem personagem identificado]

  Necessidade `protection`; prioridade 97.59800000000001; fato#2747733 fora da memória curta amostrada; necessidade/caso pode conservar referência própria. Ação `avoid_threat`, score do objetivo 11.80. Avaliação das alternativas em h3454; objetivo criado em h3450. Resultado: Afastou-se do local da ameaça.
  Antes: HP 80, fome 71, dinheiro 0, comida 0; raiva 97.7, ressentimento 99.6, desespero 100.0. Depois: HP 80, dinheiro 0, comida 0.

Fatos do arco não exibidos neste recorte: 20. IDs integrais no catálogo.

## L06 — Cobrança e devolução de um bem real — Arthus Kars (#843)

Arco **15410**; h442→h611; 19 fatos; 6 participantes diretos. Tipo: `causal_or_single`.

**Leitura da história:** em h442, Vallen, o primeiro registro deste recorte diz: Arthus Kars roubou provisão de Iria Douran.

Entre as consequências registradas: Arthus Kars devolveu uma provisão rastreável. O último fato disponível neste recorte ocorreu em h611; isso não implica que a disputa tenha terminado definitivamente.

Os elos se conectam por fonte de evento/necessidade executada; o registro da fonte demonstra a referência causal do agente, sem garantir que aquela informação seja completa ou que toda a vida esteja neste arco.

Desfechos presentes: RestitutionGiven: 1.

- **h442 · evento#376816 · ItemStolen**: Arthus Kars roubou provisão de Iria Douran. [ator Arthus Kars (#843); alvo Iria Douran (#3638)]

  Necessidade `money`; prioridade 76.18033333333334; origem interna `economy`, sem fato externo de referência. Ação `steal_person`, score do objetivo 59.90; alternativa `work`=47.50. Avaliação das alternativas em h442; objetivo criado em h442. Resultado: Provisão real roubada.
  Antes: HP 90, fome 48, dinheiro 0, comida 2; raiva 28.4, ressentimento 32.9, desespero 42.1. Depois: HP 90, dinheiro 0, comida 3.

- **h442 · evento#377212 · RestitutionDemanded**: Lyra Stone: demand_return diante de Arthus Kars. [ator Lyra Stone (#3615); alvo Arthus Kars (#843)]

  Necessidade `protection`; prioridade 74.84400000000001; fato#376816, confiança 100%, origem direct. Ação `demand_return`, score do objetivo 83.10; alternativa `attack`=82.53. Avaliação das alternativas em h442; objetivo criado em h442. Resultado: Interação estruturada registrada: demand_return.
  Antes: HP 100, fome 61, dinheiro 7, comida 0; raiva 97.6, ressentimento 99.7, desespero 26.5. Depois: HP 100, dinheiro 7, comida 0.

- **h443 · evento#378000 · ConflictStarted**: Lyra Stone iniciou confronto físico com Arthus Kars. [ator Lyra Stone (#3615); alvo Arthus Kars (#843)]

  Necessidade `protection`; prioridade 74.812; fato#376816, confiança 100%, origem direct. Ação `attack`, score do objetivo 69.88; alternativa `confront`=61.94. Avaliação das alternativas em h443; objetivo criado em h443. Resultado: Ataque causou 4 de dano real.
  Antes: HP 100, fome 63, dinheiro 7, comida 0; raiva 97.3, ressentimento 99.6, desespero 26.7. Depois: HP 100, dinheiro 7, comida 0.

- **h443 · evento#378001 · CharacterAttacked**: Lyra Stone feriu Arthus Kars em 4 HP. [ator Lyra Stone (#3615); alvo Arthus Kars (#843)]

  Necessidade `protection`; prioridade 74.812; fato#376816, confiança 100%, origem direct. Ação `attack`, score do objetivo 69.88; alternativa `confront`=61.94. Avaliação das alternativas em h443; objetivo criado em h443. Resultado: Ataque causou 4 de dano real.
  Antes: HP 100, fome 63, dinheiro 7, comida 0; raiva 97.3, ressentimento 99.6, desespero 26.7. Depois: HP 100, dinheiro 7, comida 0.

- **h444 · evento#378472 · RestitutionGiven**: Arthus Kars devolveu uma provisão rastreável. [ator Arthus Kars (#843); alvo Lyra Stone (#3615)]

  Necessidade `response`; prioridade 83.54899999999999; fato#378001, confiança 100%, origem direct. Ação `return_stolen`, score do objetivo 103.10; alternativa `defend`=94.20. Avaliação das alternativas em h444; objetivo criado em h444. Resultado: Restituição material real realizada.
  Antes: HP 86, fome 52, dinheiro 1, comida 2; raiva 57.8, ressentimento 49.3, desespero 42.4. Depois: HP 86, dinheiro 1, comida 1.

- **h477 · evento#407374 · ThreatAvoided**: Arthus Douran buscou um local seguro conhecido. [ator Arthus Douran (#3640); alvo sem personagem identificado]

  Necessidade `protection`; prioridade 76.96600000000001; fato#376816, confiança 30%, origem rumor. Ação `avoid_threat`, score do objetivo 18.20. Avaliação das alternativas em h477; objetivo criado em h470. Resultado: Afastou-se do local da ameaça.
  Antes: HP 100, fome 46, dinheiro 8, comida 1; raiva 96.4, ressentimento 99.5, desespero 62.8. Depois: HP 100, dinheiro 8, comida 1.

- **h487 · evento#416260 · ProtectionGiven**: Mira Ferros permaneceu próximo de Arthus Kars. [ator Mira Ferros (#3663); alvo Arthus Kars (#843)]

  Necessidade `protection`; prioridade 100; fato#378001 fora da memória curta amostrada; necessidade/caso pode conservar referência própria. Ação `stay_near`, score do objetivo 86.65; alternativa `ask_personal_help`=49.45. Avaliação das alternativas em h487; objetivo criado em h487. Resultado: Acompanhou o protegido.
  Antes: HP 92, fome 50, dinheiro 0, comida 0; raiva 91.1, ressentimento 91.9, desespero 100.0. Depois: HP 92, dinheiro 0, comida 0.

- **h537 · evento#459744 · InvestigationPerformed**: Arthus Douran verificou o último local conhecido do responsável. [ator Arthus Douran (#3640); alvo sem personagem identificado]

  Necessidade `revenge`; prioridade 72.676; fato#376816 fora da memória curta amostrada; necessidade/caso pode conservar referência própria. Ação `investigate`, score do objetivo 74.70; alternativa `ask_personal_help`=64.90. Avaliação das alternativas em h537; objetivo criado em h537. Resultado: Investigou o local conhecido; não houve confronto.
  Antes: HP 100, fome 46, dinheiro 10, comida 1; raiva 96.4, ressentimento 99.5, desespero 74.6. Depois: HP 100, dinheiro 10, comida 1.

- **h611 · evento#523288 · PursuitSearch**: Mira Ferros verificou a última localização conhecida sem encontrar o alvo. [ator Mira Ferros (#3663); alvo sem personagem identificado]

  Necessidade `pursuit`; prioridade 82.0; fato#378001 fora da memória curta amostrada; necessidade/caso pode conservar referência própria. Ação `pursue`, score do objetivo 85.00. Avaliação das alternativas em h611; objetivo criado em h611. Resultado: Busca local sem encontro; não consulta posição remota.
  Antes: HP 100, fome 42, dinheiro 7, comida 1; raiva 98.3, ressentimento 99.8, desespero 100.0. Depois: HP 100, dinheiro 7, comida 1.

Fatos do arco não exibidos neste recorte: 10. IDs integrais no catálogo.

## L07 — Cobrança e devolução de um bem real — Lyra Alvor (#5123)

Arco **129281**; h3981→h4150; 17 fatos; 3 participantes diretos. Tipo: `causal_or_single`.

**Leitura da história:** em h3981, Karlen, o primeiro registro deste recorte diz: Lyra Alvor roubou provisão de Aldren Valerius.

Entre as consequências registradas: Lyra Alvor devolveu uma provisão rastreável. O último fato disponível neste recorte ocorreu em h4150; isso não implica que a disputa tenha terminado definitivamente.

Os elos se conectam por fonte de evento/necessidade executada; o registro da fonte demonstra a referência causal do agente, sem garantir que aquela informação seja completa ou que toda a vida esteja neste arco.

Desfechos presentes: RestitutionGiven: 1.

- **h3981 · evento#3141922 · ItemStolen**: Lyra Alvor roubou provisão de Aldren Valerius. [ator Lyra Alvor (#5123); alvo Aldren Valerius (#5115)]

  Necessidade `money`; prioridade 100; origem interna `economy`, sem fato externo de referência. Ação `steal_person`, score do objetivo 37.20. Avaliação das alternativas em h3981; objetivo criado em h3981. Resultado: Provisão real roubada.
  Antes: HP 92, fome 44, dinheiro 0, comida 0; raiva 0.0, ressentimento 66.1, desespero 100.0. Depois: HP 92, dinheiro 0, comida 1.

- **h3983 · evento#3143426 · RestitutionDemanded**: Aldren Valerius: demand_return diante de Lyra Alvor. [ator Aldren Valerius (#5115); alvo Lyra Alvor (#5123)]

  Necessidade `protection`; prioridade 72.284; fato#3141922, confiança 100%, origem direct. Ação `demand_return`, score do objetivo 84.30; alternativa `attack`=66.74. Avaliação das alternativas em h3983; objetivo criado em h3983. Resultado: Interação estruturada registrada: demand_return.
  Antes: HP 100, fome 49, dinheiro 7, comida 0; raiva 28.9, ressentimento 89.8, desespero 47.8. Depois: HP 100, dinheiro 7, comida 0.

- **h3984 · evento#3144299 · ConflictStarted**: Aldren Valerius iniciou confronto físico com Lyra Alvor. [ator Aldren Valerius (#5115); alvo Lyra Alvor (#5123)]

  Necessidade `protection`; prioridade 72.25200000000001; fato#3141922, confiança 100%, origem direct. Ação `attack`, score do objetivo 66.60; alternativa `confront`=62.89. Avaliação das alternativas em h3984; objetivo criado em h3984. Resultado: Ataque causou 5 de dano real.
  Antes: HP 100, fome 51, dinheiro 7, comida 0; raiva 28.6, ressentimento 89.8, desespero 48.0. Depois: HP 100, dinheiro 7, comida 0.

- **h3984 · evento#3144300 · CharacterAttacked**: Aldren Valerius feriu Lyra Alvor em 5 HP. [ator Aldren Valerius (#5115); alvo Lyra Alvor (#5123)]

  Necessidade `protection`; prioridade 72.25200000000001; fato#3141922, confiança 100%, origem direct. Ação `attack`, score do objetivo 66.60; alternativa `confront`=62.89. Avaliação das alternativas em h3984; objetivo criado em h3984. Resultado: Ataque causou 5 de dano real.
  Antes: HP 100, fome 51, dinheiro 7, comida 0; raiva 28.6, ressentimento 89.8, desespero 48.0. Depois: HP 100, dinheiro 7, comida 0.

- **h3985 · evento#3145059 · RestitutionGiven**: Lyra Alvor devolveu uma provisão rastreável. [ator Lyra Alvor (#5123); alvo Aldren Valerius (#5115)]

  Necessidade `response`; prioridade 79.42099999999994; fato#3144300, confiança 100%, origem direct. Ação `return_stolen`, score do objetivo 87.55; alternativa `defend`=83.30. Avaliação das alternativas em h3985; objetivo criado em h3985. Resultado: Restituição material real realizada.
  Antes: HP 87, fome 52, dinheiro 0, comida 2; raiva 0.0, ressentimento 82.4, desespero 70.3. Depois: HP 87, dinheiro 0, comida 1.

- **h4012 · evento#3164277 · ProtectionGiven**: Marie Alvor permaneceu próximo de Lyra Alvor. [ator Marie Alvor (#5117); alvo Lyra Alvor (#5123)]

  Necessidade `protection`; prioridade 94.482; fato#3144300, confiança 100%, origem direct. Ação `stay_near`, score do objetivo 82.00; alternativa `denounce`=66.35. Avaliação das alternativas em h4012; objetivo criado em h4012. Resultado: Acompanhou o protegido.
  Antes: HP 100, fome 71, dinheiro 5, comida 0; raiva 21.9, ressentimento 98.8, desespero 100.0. Depois: HP 100, dinheiro 5, comida 0.

- **h4126 · evento#3244101 · CalmingAttempted**: Marie Alvor: calm diante de Aldren Valerius. [ator Marie Alvor (#5117); alvo Aldren Valerius (#5115)]

  Necessidade `pursuit`; prioridade 87.3; fato#3144300 fora da memória curta amostrada; necessidade/caso pode conservar referência própria. Ação `calm`, score do objetivo 69.67; alternativa `confront`=69.00. Avaliação das alternativas em h4126; objetivo criado em h4126. Resultado: Interação estruturada registrada: calm.
  Antes: HP 100, fome 59, dinheiro 9, comida 0; raiva 27.2, ressentimento 97.4, desespero 100.0. Depois: HP 100, dinheiro 9, comida 0.

- **h4132 · evento#3248361 · CharacterConfronted**: Marie Alvor: confront diante de Aldren Valerius. [ator Marie Alvor (#5117); alvo Aldren Valerius (#5115)]

  Necessidade `pursuit`; prioridade 87.3; fato#3144300 fora da memória curta amostrada; necessidade/caso pode conservar referência própria. Ação `confront`, score do objetivo 68.73; alternativa `defend`=60.38. Avaliação das alternativas em h4132; objetivo criado em h4132. Resultado: Interação estruturada registrada: confront.
  Antes: HP 100, fome 71, dinheiro 9, comida 0; raiva 25.4, ressentimento 97.1, desespero 100.0. Depois: HP 100, dinheiro 9, comida 0.

- **h4150 · evento#3261081 · PursuitSearch**: Marie Alvor verificou a última localização conhecida sem encontrar o alvo. [ator Marie Alvor (#5117); alvo sem personagem identificado]

  Necessidade `pursuit`; prioridade 87.3; fato#3144300 fora da memória curta amostrada; necessidade/caso pode conservar referência própria. Ação `pursue`, score do objetivo 96.40. Avaliação das alternativas em h4150; objetivo criado em h4150. Resultado: Busca local sem encontro; não consulta posição remota.
  Antes: HP 100, fome 67, dinheiro 12, comida 0; raiva 20.7, ressentimento 96.4, desespero 100.0. Depois: HP 100, dinheiro 12, comida 0.

Fatos do arco não exibidos neste recorte: 8. IDs integrais no catálogo.

## L08 — Desculpas em uma disputa — Marie Corven (#4279)

Arco **113068**; h3425→h3701; 103 fatos; 7 participantes diretos. Tipo: `causal_or_single`.

**Leitura da história:** em h3425, Arthon, o primeiro registro deste recorte diz: Marie Corven roubou comida no mercado de Arthon.

Entre as consequências registradas: Arthus Bruma: apologize diante de Marie Stone. O último fato disponível neste recorte ocorreu em h3701; isso não implica que a disputa tenha terminado definitivamente.

Os elos se conectam por fonte de evento/necessidade executada; o registro da fonte demonstra a referência causal do agente, sem garantir que aquela informação seja completa ou que toda a vida esteja neste arco.

Desfechos presentes: ApologyGiven: 1.

**Limite de qualidade:** o arco contém muita repetição de agressões. Continuidade causal aparece, mas a frequência de golpes não equivale a novos objetivos ou capítulos distintos.

- **h3425 · evento#2742732 · ItemStolen**: Marie Corven roubou comida no mercado de Arthon. [ator Marie Corven (#4279); alvo Arthon (cidade#1127)]

  Necessidade `food_reserve`; prioridade 69.78834796488428; origem interna `food_reserve`, sem fato externo de referência. Ação `steal`, score do objetivo 52.60; alternativa `forage`=45.50. Avaliação das alternativas em h3425; objetivo criado em h3425. Resultado: Alimento roubado.
  Antes: HP 86, fome 48, dinheiro 0, comida 0; raiva 90.6, ressentimento 98.6, desespero 100.0. Depois: HP 86, dinheiro 0, comida 1.

- **h3425 · evento#2742734 · WantedIssued**: Arthus Bruma registrou procura por Marie Corven. [ator Arthus Bruma (#1157); alvo Arthon (cidade#1127)]
- **h3426 · evento#2743009 · GuardResponded**: Arthus Bruma interveio no roubo e cobrou 0 moedas de Marie Corven. [ator Arthus Bruma (#1157); alvo Marie Corven (#4279)]

  Necessidade `security`; prioridade 81.0; fato#2742732, confiança 100%, origem direct. Ação `secure`, score do objetivo 73.33. Avaliação das alternativas em h3426; objetivo criado em h3426. Resultado: Suspeito encontrado; intervenção registrada.
  Antes: HP 100, fome 62, dinheiro 7, comida 2; raiva 22.8, ressentimento 100.0, desespero 73.8. Depois: HP 100, dinheiro 7, comida 2.

- **h3427 · evento#2743695 · CharacterAttacked**: Marie Stone feriu Marie Corven em 6 HP. [ator Marie Stone (#1136); alvo Marie Corven (#4279)]

  Necessidade `protection`; prioridade 74.058; fato#2742732, confiança 100%, origem direct. Ação `attack`, score do objetivo 68.35; alternativa `confront`=67.40. Avaliação das alternativas em h3427; objetivo criado em h3427. Resultado: Ataque causou 6 de dano real.
  Antes: HP 95, fome 46, dinheiro 0, comida 2; raiva 98.2, ressentimento 99.8, desespero 100.0. Depois: HP 95, dinheiro 0, comida 2.

- **h3427 · evento#2744161 · CharacterAttacked**: Marie Corven feriu Marie Stone em 4 HP. [ator Marie Corven (#4279); alvo Marie Stone (#1136)]

  Necessidade `response`; prioridade 89.968; fato#2743695, confiança 100%, origem direct. Ação `attack`, score do objetivo 91.97; alternativa `defend`=91.49. Avaliação das alternativas em h3427; objetivo criado em h3427. Resultado: Ataque causou 4 de dano real.
  Antes: HP 80, fome 52, dinheiro 0, comida 1; raiva 99.7, ressentimento 100.0, desespero 100.0. Depois: HP 80, dinheiro 0, comida 1.

- **h3428 · evento#2744451 · CharacterAttacked**: Marie Stone feriu Marie Corven em 2 HP. [ator Marie Stone (#1136); alvo Marie Corven (#4279)]

  Necessidade `response`; prioridade 90.11800000000001; fato#2744161, confiança 100%, origem direct. Ação `attack`, score do objetivo 94.02; alternativa `defend`=89.33. Avaliação das alternativas em h3428; objetivo criado em h3428. Resultado: Ataque causou 2 de dano real.
  Antes: HP 91, fome 48, dinheiro 0, comida 2; raiva 99.7, ressentimento 100.0, desespero 100.0. Depois: HP 91, dinheiro 0, comida 2.

- **h3428 · evento#2744456 · CharacterAttacked**: Arthus Bruma feriu Marie Corven em 14 HP. [ator Arthus Bruma (#1157); alvo Marie Corven (#4279)]

  Necessidade `protection`; prioridade 93.464; fato#2744161, confiança 100%, origem direct. Ação `attack`, score do objetivo 67.28; alternativa `alert`=61.78. Avaliação das alternativas em h3428; objetivo criado em h3428. Resultado: Ataque causou 14 de dano real.
  Antes: HP 100, fome 66, dinheiro 7, comida 2; raiva 22.2, ressentimento 99.9, desespero 74.1. Depois: HP 100, dinheiro 7, comida 2.

- **h3472 · evento#2776494 · ApologyGiven**: Arthus Bruma: apologize diante de Marie Stone. [ator Arthus Bruma (#1157); alvo Marie Stone (#1136)]

  Necessidade `pursuit`; prioridade 80.75; fato#2743695 fora da memória curta amostrada; necessidade/caso pode conservar referência própria. Ação `apologize`, score do objetivo 61.47; alternativa `warn`=56.45. Avaliação das alternativas em h3472; objetivo criado em h3472. Resultado: Interação estruturada registrada: apologize.
  Antes: HP 100, fome 74, dinheiro 7, comida 0; raiva 9.1, ressentimento 98.1, desespero 81.0. Depois: HP 100, dinheiro 7, comida 0.

- **h3697 · evento#2938589 · PursuitSearch**: Arthus Bruma verificou a última localização conhecida sem encontrar o alvo. [ator Arthus Bruma (#1157); alvo sem personagem identificado]

  Necessidade `protection`; prioridade 95.33; fato#2888975, confiança 30%, origem rumor. Ação `pursue`, score do objetivo 88.60; alternativa `ask_personal_help`=38.10. Avaliação das alternativas em h3697; objetivo criado em h3697. Resultado: Busca local sem encontro; não consulta posição remota.
  Antes: HP 100, fome 44, dinheiro 21, comida 0; raiva 43.1, ressentimento 95.3, desespero 84.2. Depois: HP 100, dinheiro 21, comida 0.

- **h3698 · evento#2939312 · PursuitSearch**: Arthus Bruma verificou a última localização conhecida sem encontrar o alvo. [ator Arthus Bruma (#1157); alvo sem personagem identificado]
- **h3699 · evento#2940027 · PursuitSearch**: Arthus Bruma verificou a última localização conhecida sem encontrar o alvo. [ator Arthus Bruma (#1157); alvo sem personagem identificado]
- **h3701 · evento#2941458 · ThreatAvoided**: Arthus Bruma buscou um local seguro conhecido. [ator Arthus Bruma (#1157); alvo sem personagem identificado]

  Necessidade `protection`; prioridade 95.80199999999999; fato#2888975, confiança 30%, origem rumor. Ação `avoid_threat`, score do objetivo 26.60. Avaliação das alternativas em h3701; objetivo criado em h3701. Resultado: Afastou-se do local da ameaça.
  Antes: HP 100, fome 52, dinheiro 21, comida 0; raiva 41.9, ressentimento 95.2, desespero 83.0. Depois: HP 100, dinheiro 21, comida 0.

Fatos do arco não exibidos neste recorte: 91. IDs integrais no catálogo.

## L09 — Desculpas em uma disputa — Bela Kars (#686)

Arco **133951**; h4159→h4430; 35 fatos; 4 participantes diretos. Tipo: `causal_or_single`.

**Leitura da história:** em h4159, Kardor, o primeiro registro deste recorte diz: Bela Kars roubou provisão de Iria Montes.

Entre as consequências registradas: Aldren Valerius: apologize diante de Bela Kars. O último fato disponível neste recorte ocorreu em h4430; isso não implica que a disputa tenha terminado definitivamente.

Os elos se conectam por fonte de evento/necessidade executada; o registro da fonte demonstra a referência causal do agente, sem garantir que aquela informação seja completa ou que toda a vida esteja neste arco.

Desfechos presentes: ApologyGiven: 1.

- **h4159 · evento#3266960 · ItemStolen**: Bela Kars roubou provisão de Iria Montes. [ator Bela Kars (#686); alvo Iria Montes (#3302)]

  Necessidade `money`; prioridade 100; origem interna `economy`, sem fato externo de referência. Ação `steal_person`, score do objetivo 51.00. Avaliação das alternativas em h4159; objetivo criado em h4159. Resultado: Provisão real roubada.
  Antes: HP 65, fome 58, dinheiro 0, comida 1; raiva 88.7, ressentimento 98.3, desespero 100.0. Depois: HP 65, dinheiro 0, comida 2.

- **h4159 · evento#3266962 · WantedIssued**: Marie Alvor registrou procura por Bela Kars. [ator Marie Alvor (#689); alvo Kardor (cidade#677)]
- **h4159 · evento#3266964 · GuardResponded**: Marie Alvor interveio no roubo e cobrou 0 moedas de Bela Kars. [ator Marie Alvor (#689); alvo Bela Kars (#686)]

  Necessidade `security`; prioridade 90.89999999999999; fato#3266960, confiança 100%, origem direct. Ação `secure`, score do objetivo 84.33. Avaliação das alternativas em h4159; objetivo criado em h4159. Resultado: Suspeito encontrado; intervenção registrada.
  Antes: HP 100, fome 49, dinheiro 12, comida 1; raiva 95.5, ressentimento 99.6, desespero 100.0. Depois: HP 100, dinheiro 12, comida 1.

- **h4236 · evento#3321947 · CharacterAttacked**: Marie Alvor feriu Bela Kars em 10 HP. [ator Marie Alvor (#689); alvo Bela Kars (#686)]

  Necessidade `pursuit`; prioridade 74.6; fato#3266962, confiança 60%, origem known. Ação `attack`, score do objetivo 92.40; alternativa `threaten`=69.21. Avaliação das alternativas em h4236; objetivo criado em h4236. Resultado: Ataque causou 10 de dano real.
  Antes: HP 100, fome 43, dinheiro 20, comida 0; raiva 79.4, ressentimento 98.7, desespero 94.0. Depois: HP 100, dinheiro 20, comida 0.

- **h4237 · evento#3322671 · CharacterAttacked**: Marie Alvor feriu Bela Kars em 10 HP. [ator Marie Alvor (#689); alvo Bela Kars (#686)]

  Necessidade `pursuit`; prioridade 74.75; fato#3266962, confiança 60%, origem known. Ação `attack`, score do objetivo 117.84; alternativa `defend`=82.58. Avaliação das alternativas em h4237; objetivo criado em h4237. Resultado: Ataque causou 10 de dano real.
  Antes: HP 100, fome 45, dinheiro 20, comida 0; raiva 79.1, ressentimento 98.7, desespero 94.2. Depois: HP 100, dinheiro 20, comida 0.

- **h4238 · evento#3323404 · CharacterAttacked**: Marie Alvor feriu Bela Kars em 11 HP. [ator Marie Alvor (#689); alvo Bela Kars (#686)]

  Necessidade `pursuit`; prioridade 74.89999999999999; fato#3266962, confiança 60%, origem known. Ação `attack`, score do objetivo 118.30; alternativa `defend`=82.31. Avaliação das alternativas em h4238; objetivo criado em h4238. Resultado: Ataque causou 11 de dano real.
  Antes: HP 100, fome 47, dinheiro 20, comida 0; raiva 78.8, ressentimento 98.6, desespero 94.3. Depois: HP 100, dinheiro 20, comida 0.

- **h4239 · evento#3324127 · CharacterAttacked**: Marie Alvor feriu Bela Kars em 5 HP. [ator Marie Alvor (#689); alvo Bela Kars (#686)]

  Necessidade `pursuit`; prioridade 75.05; fato#3266962, confiança 60%, origem known. Ação `attack`, score do objetivo 118.84; alternativa `defend`=82.00. Avaliação das alternativas em h4239; objetivo criado em h4239. Resultado: Ataque causou 5 de dano real.
  Antes: HP 100, fome 49, dinheiro 20, comida 0; raiva 78.5, ressentimento 98.6, desespero 94.5. Depois: HP 100, dinheiro 20, comida 0.

- **h4269 · evento#3345221 · ApologyGiven**: Aldren Valerius: apologize diante de Bela Kars. [ator Aldren Valerius (#3304); alvo Bela Kars (#686)]

  Necessidade `pursuit`; prioridade 76.0; fato#3266960 fora da memória curta amostrada; necessidade/caso pode conservar referência própria. Ação `apologize`, score do objetivo 49.04; alternativa `withdraw`=47.30. Avaliação das alternativas em h4269; objetivo criado em h4269. Resultado: Interação estruturada registrada: apologize.
  Antes: HP 100, fome 66, dinheiro 6, comida 2; raiva 0.8, ressentimento 95.6, desespero 100.0. Depois: HP 100, dinheiro 6, comida 2.

- **h4425 · evento#3454213 · PursuitSearch**: Aldren Valerius verificou a última localização conhecida sem encontrar o alvo. [ator Aldren Valerius (#3304); alvo sem personagem identificado]

  Necessidade `protection`; prioridade 97.49; fato#3368010, confiança 30%, origem rumor. Ação `pursue`, score do objetivo 63.05; alternativa `stay_near`=54.45. Avaliação das alternativas em h4425; objetivo criado em h4422. Resultado: Busca local sem encontro; não consulta posição remota.
  Antes: HP 100, fome 58, dinheiro 11, comida 0; raiva 24.2, ressentimento 98.3, desespero 100.0. Depois: HP 100, dinheiro 11, comida 0.

- **h4426 · evento#3454928 · PursuitSearch**: Aldren Valerius verificou a última localização conhecida sem encontrar o alvo. [ator Aldren Valerius (#3304); alvo sem personagem identificado]
- **h4427 · evento#3455636 · PursuitSearch**: Aldren Valerius verificou a última localização conhecida sem encontrar o alvo. [ator Aldren Valerius (#3304); alvo sem personagem identificado]
- **h4430 · evento#3457728 · ProtectionGiven**: Aldren Valerius permaneceu próximo de Bela Kars. [ator Aldren Valerius (#3304); alvo Bela Kars (#686)]

  Necessidade `protection`; prioridade 99.968; fato#3368010, confiança 30%, origem rumor. Ação `stay_near`, score do objetivo 54.45; alternativa `ask_personal_help`=49.35. Avaliação das alternativas em h4430; objetivo criado em h4430. Resultado: Acompanhou o protegido.
  Antes: HP 100, fome 68, dinheiro 11, comida 0; raiva 40.7, ressentimento 99.9, desespero 100.0. Depois: HP 100, dinheiro 11, comida 0.

Fatos do arco não exibidos neste recorte: 23. IDs integrais no catálogo.

## L10 — Autoridade, confronto e captura — Elena Arven (#2266)

Arco **101317**; h3038→h3377; 102 fatos; 9 participantes diretos. Tipo: `causal_or_single`.

**Leitura da história:** em h3038, Mordor, o primeiro registro deste recorte diz: Elena Arven roubou provisão de John Douran.

Entre as consequências registradas: Nora Luar deteve Iria Alvor e cobrou 2 moedas. Arthus Luar deteve Iria Alvor e cobrou 0 moedas. Mira Kars deteve Nora Luar e cobrou 5 moedas. O último fato disponível neste recorte ocorreu em h3377; isso não implica que a disputa tenha terminado definitivamente.

Os elos se conectam por fonte de evento/necessidade executada; o registro da fonte demonstra a referência causal do agente, sem garantir que aquela informação seja completa ou que toda a vida esteja neste arco.

Desfechos presentes: CharacterCaptured: 3.

**Limite de qualidade:** o arco contém muita repetição de agressões. Continuidade causal aparece, mas a frequência de golpes não equivale a novos objetivos ou capítulos distintos.

- **h3038 · evento#2457436 · ItemStolen**: Elena Arven roubou provisão de John Douran. [ator Elena Arven (#2266); alvo John Douran (#201)]

  Necessidade `money`; prioridade 97.2; origem interna `economy`, sem fato externo de referência. Ação `steal_person`, score do objetivo 17.90. Avaliação das alternativas em h3038; objetivo criado em h3038. Resultado: Provisão real roubada.
  Antes: HP 100, fome 56, dinheiro 0, comida 0; raiva 99.5, ressentimento 99.9, desespero 100.0. Depois: HP 100, dinheiro 0, comida 1.

- **h3038 · evento#2457438 · WantedIssued**: Arthus Luar registrou procura por Elena Arven. [ator Arthus Luar (#127); alvo Mordor (cidade#180)]
- **h3055 · evento#2469637 · PursuitSearch**: Elena Arven verificou a última localização conhecida sem encontrar o alvo. [ator Elena Arven (#221); alvo sem personagem identificado]

  Necessidade `pursuit`; prioridade 70.4; fato#2457436 fora da memória curta amostrada; necessidade/caso pode conservar referência própria. Ação `pursue`, score do objetivo 101.60. Avaliação das alternativas em h3055; objetivo criado em h3055. Resultado: Busca local sem encontro; não consulta posição remota.
  Antes: HP 93, fome 39, dinheiro 11, comida 0; raiva 98.5, ressentimento 99.8, desespero 100.0. Depois: HP 93, dinheiro 11, comida 0.

- **h3057 · evento#2471030 · CharacterAttacked**: Elena Arven feriu Elena Arven em 15 HP. [ator Elena Arven (#221); alvo Elena Arven (#2266)]

  Necessidade `pursuit`; prioridade 70.7; fato#2457436 fora da memória curta amostrada; necessidade/caso pode conservar referência própria. Ação `attack`, score do objetivo 103.51; alternativa `confront`=85.00. Avaliação das alternativas em h3057; objetivo criado em h3057. Resultado: Ataque causou 15 de dano real.
  Antes: HP 93, fome 43, dinheiro 11, comida 0; raiva 82.9, ressentimento 99.7, desespero 85.2. Depois: HP 93, dinheiro 11, comida 0.

- **h3058 · evento#2471752 · CharacterAttacked**: Elena Arven feriu Elena Arven em 15 HP. [ator Elena Arven (#221); alvo Elena Arven (#2266)]

  Necessidade `pursuit`; prioridade 70.85; fato#2457436 fora da memória curta amostrada; necessidade/caso pode conservar referência própria. Ação `attack`, score do objetivo 134.61; alternativa `defend`=89.20. Avaliação das alternativas em h3058; objetivo criado em h3058. Resultado: Ataque causou 15 de dano real.
  Antes: HP 93, fome 45, dinheiro 11, comida 0; raiva 94.6, ressentimento 100.0, desespero 85.3. Depois: HP 93, dinheiro 11, comida 0.

- **h3214 · evento#2586721 · CharacterAttacked**: Iria Alvor feriu Elena Arven em 12 HP. [ator Iria Alvor (#2315); alvo Elena Arven (#221)]

  Necessidade `pursuit`; prioridade 82.0; fato#2471752 fora da memória curta amostrada; necessidade/caso pode conservar referência própria. Ação `attack`, score do objetivo 80.21; alternativa `insult`=75.58. Avaliação das alternativas em h3214; objetivo criado em h3214. Resultado: Ataque causou 12 de dano real.
  Antes: HP 98, fome 70, dinheiro 4, comida 1; raiva 99.4, ressentimento 99.9, desespero 100.0. Depois: HP 98, dinheiro 4, comida 1.

- **h3215 · evento#2587206 · CharacterAttacked**: Elena Arven feriu Iria Alvor em 11 HP. [ator Elena Arven (#221); alvo Iria Alvor (#2315)]

  Necessidade `response`; prioridade 90.11800000000001; fato#2586721, confiança 100%, origem direct. Ação `attack`, score do objetivo 124.61; alternativa `defend`=94.18. Avaliação das alternativas em h3215; objetivo criado em h3215. Resultado: Ataque causou 11 de dano real.
  Antes: HP 88, fome 39, dinheiro 8, comida 1; raiva 99.7, ressentimento 100.0, desespero 99.2. Depois: HP 88, dinheiro 8, comida 1.

- **h3311 · evento#2657532 · CharacterCaptured**: Nora Luar deteve Iria Alvor e cobrou 2 moedas. [ator Nora Luar (#203); alvo Iria Alvor (#2315)]

  Necessidade `pursuit`; prioridade 82.0; fato#2589929 fora da memória curta amostrada; necessidade/caso pode conservar referência própria. Ação `capture`, score do objetivo 129.10. Avaliação das alternativas em h3311; objetivo criado em h3311. Resultado: Captura e detenção temporária registradas.
  Antes: HP 100, fome 70, dinheiro 10, comida 2; raiva 57.7, ressentimento 98.4, desespero 0.1. Depois: HP 100, dinheiro 10, comida 2.

- **h3337 · evento#2676854 · CharacterCaptured**: Arthus Luar deteve Iria Alvor e cobrou 0 moedas. [ator Arthus Luar (#127); alvo Iria Alvor (#2315)]

  Necessidade `pursuit`; prioridade 82.0; fato#2589929 fora da memória curta amostrada; necessidade/caso pode conservar referência própria. Ação `capture`, score do objetivo 118.60; alternativa `surrender`=70.08. Avaliação das alternativas em h3337; objetivo criado em h3337. Resultado: Captura e detenção temporária registradas.
  Antes: HP 100, fome 78, dinheiro 0, comida 1; raiva 99.4, ressentimento 99.9, desespero 0.4. Depois: HP 100, dinheiro 0, comida 1.

- **h3366 · evento#2698563 · ConflictEnded**: O confronto de Arthus Luar terminou: surrender. [ator Arthus Luar (#127); alvo Nora Luar (#203)]

  Necessidade `pursuit`; prioridade 82.0; fato#2640325 fora da memória curta amostrada; necessidade/caso pode conservar referência própria. Ação `surrender`, score do objetivo 73.73; alternativa `flee`=62.77. Avaliação das alternativas em h3366; objetivo criado em h3366. Resultado: Rendição registrada; não implica morte.
  Antes: HP 100, fome 56, dinheiro 0, comida 0; raiva 99.5, ressentimento 99.9, desespero 7.1. Depois: HP 100, dinheiro 0, comida 0.

- **h3366 · evento#2698564 · CharacterSurrendered**: Arthus Luar rendeu-se. [ator Arthus Luar (#127); alvo Nora Luar (#203)]

  Necessidade `pursuit`; prioridade 82.0; fato#2640325 fora da memória curta amostrada; necessidade/caso pode conservar referência própria. Ação `surrender`, score do objetivo 73.73; alternativa `flee`=62.77. Avaliação das alternativas em h3366; objetivo criado em h3366. Resultado: Rendição registrada; não implica morte.
  Antes: HP 100, fome 56, dinheiro 0, comida 0; raiva 99.5, ressentimento 99.9, desespero 7.1. Depois: HP 100, dinheiro 0, comida 0.

- **h3369 · evento#2700899 · CharacterDefended**: Mira Kars adotou defesa. [ator Mira Kars (#2234); alvo sem personagem identificado]

  Necessidade `pursuit`; prioridade 82.0; fato#2640325 fora da memória curta amostrada; necessidade/caso pode conservar referência própria. Ação `defend`, score do objetivo 62.92; alternativa `surrender`=57.52. Avaliação das alternativas em h3369; objetivo criado em h3369. Resultado: Defesa temporária adotada.
  Antes: HP 100, fome 66, dinheiro 2, comida 1; raiva 98.8, ressentimento 99.8, desespero 100.0. Depois: HP 100, dinheiro 2, comida 1.

- **h3377 · evento#2706753 · CharacterCaptured**: Mira Kars deteve Nora Luar e cobrou 5 moedas. [ator Mira Kars (#2234); alvo Nora Luar (#203)]

  Necessidade `pursuit`; prioridade 82.0; fato#2640325 fora da memória curta amostrada; necessidade/caso pode conservar referência própria. Ação `capture`, score do objetivo 123.70; alternativa `defend`=60.26. Avaliação das alternativas em h3377; objetivo criado em h3377. Resultado: Captura e detenção temporária registradas.
  Antes: HP 100, fome 42, dinheiro 2, comida 0; raiva 98.6, ressentimento 99.8, desespero 100.0. Depois: HP 100, dinheiro 2, comida 0.

Fatos do arco não exibidos neste recorte: 89. IDs integrais no catálogo.

## L11 — Autoridade, confronto e captura — John Luar (#4742)

Arco **10666**; h308→h644; 80 fatos; 9 participantes diretos. Tipo: `causal_or_single`.

**Leitura da história:** em h308, Karvia, o primeiro registro deste recorte diz: John Luar roubou comida no mercado de Karvia.

Entre as consequências registradas: Ruan Ferros deteve John Bruma e cobrou 5 moedas. O último fato disponível neste recorte ocorreu em h644; isso não implica que a disputa tenha terminado definitivamente.

Os elos se conectam por fonte de evento/necessidade executada; o registro da fonte demonstra a referência causal do agente, sem garantir que aquela informação seja completa ou que toda a vida esteja neste arco.

Desfechos presentes: CharacterCaptured: 1.

**Limite de qualidade:** o arco contém muita repetição de agressões. Continuidade causal aparece, mas a frequência de golpes não equivale a novos objetivos ou capítulos distintos.

- **h308 · evento#258131 · ItemStolen**: John Luar roubou comida no mercado de Karvia. [ator John Luar (#4742); alvo Karvia (cidade#1333)]

  Necessidade `food_reserve`; prioridade 84.58047493403694; origem interna `food_reserve`, sem fato externo de referência. Ação `steal`, score do objetivo 85.80; alternativa `forage`=78.00. Avaliação das alternativas em h308; objetivo criado em h308. Resultado: Alimento roubado.
  Antes: HP 57, fome 62, dinheiro 4, comida 0; raiva 41.1, ressentimento 100.0, desespero 0.3. Depois: HP 57, dinheiro 4, comida 1.

- **h309 · evento#258390 · CharacterAttacked**: Nora Montes feriu John Luar em 4 HP. [ator Nora Montes (#1342); alvo John Luar (#4742)]

  Necessidade `protection`; prioridade 72.84; fato#258131, confiança 100%, origem direct. Ação `attack`, score do objetivo 130.85; alternativa `defend`=90.74. Avaliação das alternativas em h309; objetivo criado em h309. Resultado: Ataque causou 4 de dano real.
  Antes: HP 100, fome 36, dinheiro 4, comida 0; raiva 99.7, ressentimento 99.4, desespero 47.1. Depois: HP 100, dinheiro 4, comida 0.

- **h309 · evento#258869 · CharacterAttacked**: John Luar feriu Nora Montes em 4 HP. [ator John Luar (#4742); alvo Nora Montes (#1342)]

  Necessidade `response`; prioridade 87.528; fato#258390, confiança 100%, origem direct. Ação `attack`, score do objetivo 81.67; alternativa `defend`=81.35. Avaliação das alternativas em h309; objetivo criado em h309. Resultado: Ataque causou 4 de dano real.
  Antes: HP 53, fome 64, dinheiro 4, comida 1; raiva 70.8, ressentimento 100.0, desespero 0.4. Depois: HP 53, dinheiro 4, comida 1.

- **h310 · evento#259164 · CharacterAttacked**: Nora Montes feriu John Luar em 3 HP. [ator Nora Montes (#1342); alvo John Luar (#4742)]

  Necessidade `response`; prioridade 90.11800000000001; fato#258869, confiança 100%, origem direct. Ação `attack`, score do objetivo 130.87; alternativa `defend`=90.41. Avaliação das alternativas em h310; objetivo criado em h310. Resultado: Ataque causou 3 de dano real.
  Antes: HP 96, fome 38, dinheiro 4, comida 0; raiva 99.7, ressentimento 100.0, desespero 47.2. Depois: HP 96, dinheiro 4, comida 0.

- **h311 · evento#259921 · CharacterAttacked**: Nora Montes feriu John Luar em 3 HP. [ator Nora Montes (#1342); alvo John Luar (#4742)]

  Necessidade `response`; prioridade 90.23599999999999; fato#258869, confiança 100%, origem direct. Ação `attack`, score do objetivo 124.05; alternativa `defend`=87.76. Avaliação das alternativas em h311; objetivo criado em h311. Resultado: Ataque causou 3 de dano real.
  Antes: HP 96, fome 40, dinheiro 4, comida 0; raiva 99.4, ressentimento 99.9, desespero 47.4. Depois: HP 96, dinheiro 4, comida 0.

- **h539 · evento#461197 · CharacterCaptured**: Ruan Ferros deteve John Bruma e cobrou 5 moedas. [ator Ruan Ferros (#1345); alvo John Bruma (#4744)]

  Necessidade `protection`; prioridade 100; fato#454984, confiança 100%, origem direct. Ação `capture`, score do objetivo 129.70; alternativa `avoid_threat`=6.90. Avaliação das alternativas em h539; objetivo criado em h539. Resultado: Captura e detenção temporária registradas.
  Antes: HP 90, fome 66, dinheiro 3, comida 0; raiva 83.7, ressentimento 97.8, desespero 100.0. Depois: HP 90, dinheiro 3, comida 0.

- **h609 · evento#521254 · ThreatReported**: John Alvor denunciou um acontecimento conhecido a Ruan Ferros. [ator John Alvor (#1348); alvo Ruan Ferros (#1345)]

  Necessidade `protection`; prioridade 100; fato#413033, confiança 30%, origem rumor. Ação `denounce`, score do objetivo 76.65; alternativa `pursue`=77.40. Avaliação das alternativas em h609; objetivo criado em h603. Resultado: Informação transmitida.
  Antes: HP 100, fome 59, dinheiro 0, comida 0; raiva 18.5, ressentimento 17.0, desespero 81.0. Depois: HP 100, dinheiro 0, comida 0.

- **h636 · evento#544481 · PursuitSearch**: Ruan Ferros verificou a última localização conhecida sem encontrar o alvo. [ator Ruan Ferros (#1345); alvo sem personagem identificado]

  Necessidade `response`; prioridade 93.066; fato#413033, confiança 30%, origem rumor. Ação `pursue`, score do objetivo 75.60. Avaliação das alternativas em h636; objetivo criado em h636. Resultado: Busca local sem encontro; não consulta posição remota.
  Antes: HP 100, fome 60, dinheiro 2, comida 0; raiva 90.9, ressentimento 98.6, desespero 100.0. Depois: HP 100, dinheiro 2, comida 0.

- **h642 · evento#549633 · PursuitSearch**: Ruan Ferros verificou a última localização conhecida sem encontrar o alvo. [ator Ruan Ferros (#1345); alvo sem personagem identificado]
- **h644 · evento#551180 · PursuitSearch**: Ruan Ferros verificou a última localização conhecida sem encontrar o alvo. [ator Ruan Ferros (#1345); alvo sem personagem identificado]
Fatos do arco não exibidos neste recorte: 70. IDs integrais no catálogo.

## L12 — Ferimento e auxílio com recursos — Bela Kars (#686)

Arco **108077**; h3252→h3582; 126 fatos; 7 participantes diretos. Tipo: `causal_or_single`.

**Leitura da história:** em h3252, Kardor, o primeiro registro deste recorte diz: Bela Kars roubou comida no mercado de Kardor.

Entre as consequências registradas: Aldren Valerius prestou auxílio inicial a Iria Montes. Aldren Valerius deteve Bela Kars e cobrou 1 moedas. O último fato disponível neste recorte ocorreu em h3582; isso não implica que a disputa tenha terminado definitivamente.

Os elos se conectam por fonte de evento/necessidade executada; o registro da fonte demonstra a referência causal do agente, sem garantir que aquela informação seja completa ou que toda a vida esteja neste arco.

Desfechos presentes: FirstAidGiven: 1, CharacterCaptured: 1.

**Limite de qualidade:** o arco contém muita repetição de agressões. Continuidade causal aparece, mas a frequência de golpes não equivale a novos objetivos ou capítulos distintos.

- **h3252 · evento#2614811 · ItemStolen**: Bela Kars roubou comida no mercado de Kardor. [ator Bela Kars (#686); alvo Kardor (cidade#677)]

  Necessidade `food`; prioridade 100; origem interna `physiology`, sem fato externo de referência. Ação `steal`, score do objetivo 69.47; alternativa `forage`=57.50. Avaliação das alternativas em h3252; objetivo criado em h3252. Resultado: Alimento roubado.
  Antes: HP 66, fome 84, dinheiro 1, comida 0; raiva 85.7, ressentimento 97.9, desespero 100.0. Depois: HP 66, dinheiro 1, comida 1.

- **h3252 · evento#2614813 · WantedIssued**: Marie Alvor registrou procura por Bela Kars. [ator Marie Alvor (#689); alvo Kardor (cidade#677)]
- **h3252 · evento#2614815 · GuardResponded**: Marie Alvor interveio no roubo e cobrou 1 moedas de Bela Kars. [ator Marie Alvor (#689); alvo Bela Kars (#686)]

  Necessidade `security`; prioridade 90.89999999999999; fato#2614811, confiança 100%, origem direct. Ação `secure`, score do objetivo 84.33. Avaliação das alternativas em h3252; objetivo criado em h3252. Resultado: Suspeito encontrado; intervenção registrada.
  Antes: HP 100, fome 75, dinheiro 3, comida 2; raiva 99.7, ressentimento 100.0, desespero 88.3. Depois: HP 100, dinheiro 3, comida 2.

- **h3257 · evento#2618252 · CharacterAttacked**: Marie Alvor feriu Iria Montes em 12 HP. [ator Marie Alvor (#689); alvo Iria Montes (#3302)]

  Necessidade `protection`; prioridade 82.358; fato#2617881, confiança 100%, origem direct. Ação `attack`, score do objetivo 119.82; alternativa `denounce`=86.85. Avaliação das alternativas em h3257; objetivo criado em h3257. Resultado: Ataque causou 12 de dano real.
  Antes: HP 100, fome 45, dinheiro 5, comida 1; raiva 98.2, ressentimento 99.8, desespero 89.1. Depois: HP 100, dinheiro 5, comida 1.

- **h3258 · evento#2618946 · CharacterAttacked**: Marie Alvor feriu Iria Montes em 4 HP. [ator Marie Alvor (#689); alvo Iria Montes (#3302)]

  Necessidade `protection`; prioridade 82.47599999999998; fato#2617881, confiança 100%, origem direct. Ação `attack`, score do objetivo 145.19; alternativa `denounce`=86.85. Avaliação das alternativas em h3258; objetivo criado em h3258. Resultado: Ataque causou 4 de dano real.
  Antes: HP 100, fome 47, dinheiro 5, comida 1; raiva 97.9, ressentimento 99.7, desespero 89.2. Depois: HP 100, dinheiro 5, comida 1.

- **h3259 · evento#2619669 · CharacterAttacked**: Marie Alvor feriu Iria Montes em 6 HP. [ator Marie Alvor (#689); alvo Iria Montes (#3302)]

  Necessidade `protection`; prioridade 82.594; fato#2617881, confiança 100%, origem direct. Ação `attack`, score do objetivo 145.21; alternativa `denounce`=86.85. Avaliação das alternativas em h3259; objetivo criado em h3259. Resultado: Ataque causou 6 de dano real.
  Antes: HP 100, fome 49, dinheiro 5, comida 1; raiva 97.6, ressentimento 99.7, desespero 89.4. Depois: HP 100, dinheiro 5, comida 1.

- **h3260 · evento#2620384 · CharacterAttacked**: Marie Alvor feriu Iria Montes em 4 HP. [ator Marie Alvor (#689); alvo Iria Montes (#3302)]

  Necessidade `protection`; prioridade 82.712; fato#2617881, confiança 100%, origem direct. Ação `attack`, score do objetivo 145.33; alternativa `denounce`=86.85. Avaliação das alternativas em h3260; objetivo criado em h3260. Resultado: Ataque causou 4 de dano real.
  Antes: HP 100, fome 51, dinheiro 5, comida 1; raiva 97.3, ressentimento 99.6, desespero 89.5. Depois: HP 100, dinheiro 5, comida 1.

- **h3349 · evento#2685954 · FirstAidGiven**: Aldren Valerius prestou auxílio inicial a Iria Montes. [ator Aldren Valerius (#3304); alvo Iria Montes (#3302)]

  Necessidade `protection`; prioridade 100; fato#2621216, confiança 30%, origem rumor. Ação `first_aid`, score do objetivo 79.25; alternativa `attack`=65.56. Avaliação das alternativas em h3349; objetivo criado em h3349. Resultado: Atendimento limitado realizado com provisões reais.
  Antes: HP 100, fome 77, dinheiro 19, comida 1; raiva 72.6, ressentimento 100.0, desespero 100.0. Depois: HP 100, dinheiro 19, comida 0.

- **h3494 · evento#2792683 · CharacterCaptured**: Aldren Valerius deteve Bela Kars e cobrou 1 moedas. [ator Aldren Valerius (#3304); alvo Bela Kars (#686)]

  Necessidade `pursuit`; prioridade 82.0; fato#2790921, confiança 100%, origem direct. Ação `capture`, score do objetivo 123.55. Avaliação das alternativas em h3494; objetivo criado em h3494. Resultado: Captura e detenção temporária registradas.
  Antes: HP 93, fome 47, dinheiro 7, comida 1; raiva 96.8, ressentimento 99.6, desespero 100.0. Depois: HP 93, dinheiro 7, comida 1.

- **h3548 · evento#2830960 · PursuitSearch**: Ruan Valerius verificou a última localização conhecida sem encontrar o alvo. [ator Ruan Valerius (#3310); alvo sem personagem identificado]
- **h3579 · evento#2852945 · SuspectLocated**: Ruan Valerius encontrou a pessoa procurada. [ator Ruan Valerius (#3310); alvo Aldren Valerius (#3304)]

  Necessidade `protection`; prioridade 100; fato#2778978, confiança 30%, origem rumor. Ação `pursue`, score do objetivo 81.80; alternativa `denounce`=67.00. Avaliação das alternativas em h3579; objetivo criado em h3579. Resultado: Pessoa localizada fisicamente.
  Antes: HP 100, fome 64, dinheiro 1, comida 0; raiva 75.8, ressentimento 98.6, desespero 100.0. Depois: HP 100, dinheiro 1, comida 0.

- **h3582 · evento#2855289 · ConflictEnded**: O confronto de Ruan Valerius terminou: flee. [ator Ruan Valerius (#3310); alvo Aldren Valerius (#3304)]

  Necessidade `protection`; prioridade 100; fato#2778978, confiança 30%, origem rumor. Ação `flee`, score do objetivo 91.93; alternativa `denounce`=75.00. Avaliação das alternativas em h3582; objetivo criado em h3582. Resultado: Afastamento físico realizado; o conflito social pode continuar.
  Antes: HP 100, fome 70, dinheiro 1, comida 0; raiva 92.9, ressentimento 99.9, desespero 100.0. Depois: HP 100, dinheiro 1, comida 0.

- **h3582 · evento#2855290 · CharacterFled**: Ruan Valerius afastou-se do confronto. [ator Ruan Valerius (#3310); alvo sem personagem identificado]

  Necessidade `protection`; prioridade 100; fato#2778978, confiança 30%, origem rumor. Ação `flee`, score do objetivo 91.93; alternativa `denounce`=75.00. Avaliação das alternativas em h3582; objetivo criado em h3582. Resultado: Afastamento físico realizado; o conflito social pode continuar.
  Antes: HP 100, fome 70, dinheiro 1, comida 0; raiva 92.9, ressentimento 99.9, desespero 100.0. Depois: HP 100, dinheiro 1, comida 0.

Fatos do arco não exibidos neste recorte: 113. IDs integrais no catálogo.

## L13 — Ferimento e auxílio com recursos — Nora Valerius (#621)

Arco **15998**; h463→h791; 96 fatos; 10 participantes diretos. Tipo: `causal_or_single`.

**Leitura da história:** em h463, Normir, o primeiro registro deste recorte diz: Nora Valerius roubou comida no mercado de Normir.

Entre as consequências registradas: Darin Solaris prestou auxílio inicial a Lyra Kars. O último fato disponível neste recorte ocorreu em h791; isso não implica que a disputa tenha terminado definitivamente.

Os elos se conectam por fonte de evento/necessidade executada; o registro da fonte demonstra a referência causal do agente, sem garantir que aquela informação seja completa ou que toda a vida esteja neste arco.

Desfechos presentes: FirstAidGiven: 1.

**Limite de qualidade:** o arco contém muita repetição de agressões. Continuidade causal aparece, mas a frequência de golpes não equivale a novos objetivos ou capítulos distintos.

- **h463 · evento#395150 · ItemStolen**: Nora Valerius roubou comida no mercado de Normir. [ator Nora Valerius (#621); alvo Normir (cidade#612)]

  Necessidade `food`; prioridade 100; origem interna `physiology`, sem fato externo de referência. Ação `steal`, score do objetivo 65.00; alternativa `forage`=49.00. Avaliação das alternativas em h463; objetivo criado em h463. Resultado: Alimento roubado.
  Antes: HP 11, fome 94, dinheiro 1, comida 0; raiva 99.5, ressentimento 99.9, desespero 57.1. Depois: HP 11, dinheiro 1, comida 1.

- **h463 · evento#395474 · CharacterInsulted**: Elena Kars: insult diante de Nora Valerius. [ator Elena Kars (#3151); alvo Nora Valerius (#621)]

  Necessidade `protection`; prioridade 80.968; fato#395150, confiança 100%, origem direct. Ação `insult`, score do objetivo 67.16; alternativa `confront`=62.45. Avaliação das alternativas em h463; objetivo criado em h463. Resultado: Interação estruturada registrada: insult.
  Antes: HP 100, fome 58, dinheiro 8, comida 0; raiva 99.7, ressentimento 100.0, desespero 49.9. Depois: HP 100, dinheiro 8, comida 0.

- **h464 · evento#395909 · CharacterThreatened**: Silas Valerius: threaten diante de Elena Kars. [ator Silas Valerius (#618); alvo Elena Kars (#3151)]

  Necessidade `protection`; prioridade 77.962; fato#395474, confiança 100%, origem direct. Ação `threaten`, score do objetivo 70.30; alternativa `confront`=68.40. Avaliação das alternativas em h464; objetivo criado em h464. Resultado: Interação estruturada registrada: threaten.
  Antes: HP 88, fome 59, dinheiro 4, comida 1; raiva 92.2, ressentimento 99.9, desespero 15.6. Depois: HP 88, dinheiro 4, comida 1.

- **h464 · evento#396228 · CharacterAttacked**: Lyra Kars feriu Nora Valerius em 5 HP. [ator Lyra Kars (#3174); alvo Nora Valerius (#621)]

  Necessidade `protection`; prioridade 70.654; fato#395150, confiança 100%, origem direct. Ação `attack`, score do objetivo 114.42; alternativa `denounce`=95.40. Avaliação das alternativas em h464; objetivo criado em h464. Resultado: Ataque causou 5 de dano real.
  Antes: HP 99, fome 67, dinheiro 3, comida 2; raiva 99.1, ressentimento 99.9, desespero 9.3. Depois: HP 99, dinheiro 3, comida 2.

- **h509 · evento#435082 · CharacterAttacked**: Elena Vale feriu Lyra Kars em 13 HP. [ator Elena Vale (#624); alvo Lyra Kars (#3174)]

  Necessidade `protection`; prioridade 100; fato#396228, confiança 30%, origem rumor. Ação `attack`, score do objetivo 82.35; alternativa `denounce`=78.05. Avaliação das alternativas em h509; objetivo criado em h509. Resultado: Ataque causou 13 de dano real.
  Antes: HP 100, fome 57, dinheiro 0, comida 0; raiva 75.9, ressentimento 98.0, desespero 35.2. Depois: HP 100, dinheiro 0, comida 0.

- **h509 · evento#435414 · FirstAidGiven**: Darin Solaris prestou auxílio inicial a Lyra Kars. [ator Darin Solaris (#3165); alvo Lyra Kars (#3174)]

  Necessidade `protection`; prioridade 90.13900000000001; fato#435082, confiança 100%, origem direct. Ação `first_aid`, score do objetivo 66.40; alternativa `alert`=64.95. Avaliação das alternativas em h509; objetivo criado em h509. Resultado: Atendimento limitado realizado com provisões reais.
  Antes: HP 100, fome 68, dinheiro 0, comida 1; raiva 34.0, ressentimento 46.7, desespero 66.7. Depois: HP 100, dinheiro 0, comida 0.

- **h518 · evento#443171 · CharacterAttacked**: Lyra Kars feriu Elena Vale em 5 HP. [ator Lyra Kars (#3174); alvo Elena Vale (#624)]

  Necessidade `response`; prioridade 91.258; fato#435082, confiança 100%, origem direct. Ação `attack`, score do objetivo 106.67; alternativa `defend`=101.01. Avaliação das alternativas em h518; objetivo criado em h518. Resultado: Ataque causou 5 de dano real.
  Antes: HP 92, fome 55, dinheiro 6, comida 0; raiva 99.1, ressentimento 100.0, desespero 3.8. Depois: HP 92, dinheiro 6, comida 0.

- **h519 · evento#443698 · CharacterAttacked**: Elena Vale feriu Lyra Kars em 12 HP. [ator Elena Vale (#624); alvo Lyra Kars (#3174)]

  Necessidade `response`; prioridade 90.11800000000001; fato#443171, confiança 100%, origem direct. Ação `attack`, score do objetivo 131.10; alternativa `defend`=86.86. Avaliação das alternativas em h519; objetivo criado em h519. Resultado: Ataque causou 12 de dano real.
  Antes: HP 95, fome 77, dinheiro 0, comida 2; raiva 99.7, ressentimento 100.0, desespero 36.7. Depois: HP 95, dinheiro 0, comida 2.

- **h667 · evento#570642 · ThreatAvoided**: Darin Solaris buscou um local seguro conhecido. [ator Darin Solaris (#3165); alvo sem personagem identificado]

  Necessidade `protection`; prioridade 100; fato#447378, confiança 30%, origem rumor. Ação `avoid_threat`, score do objetivo 4.60; alternativa `stay_near`=60.50. Avaliação das alternativas em h667; objetivo criado em h663. Resultado: Afastou-se do local da ameaça.
  Antes: HP 58, fome 64, dinheiro 3, comida 0; raiva 96.4, ressentimento 99.5, desespero 96.7. Depois: HP 58, dinheiro 3, comida 0.

- **h669 · evento#571840 · PursuitSearch**: Elena Vale verificou a última localização conhecida sem encontrar o alvo. [ator Elena Vale (#624); alvo sem personagem identificado]

  Necessidade `response`; prioridade 94.768; fato#564188, confiança 100%, origem direct. Ação `pursue`, score do objetivo 86.25. Avaliação das alternativas em h669; objetivo criado em h665. Resultado: Busca local sem encontro; não consulta posição remota.
  Antes: HP 24, fome 57, dinheiro 8, comida 0; raiva 99.7, ressentimento 100.0, desespero 51.2. Depois: HP 24, dinheiro 8, comida 0.

- **h791 · evento#676446 · ConflictEnded**: O confronto de Elena Vale terminou: flee. [ator Elena Vale (#624); alvo Darin Solaris (#3165)]

  Necessidade `response`; prioridade 90.25; fato#559982, confiança 30%, origem rumor. Ação `flee`, score do objetivo 85.95; alternativa `confront`=72.55. Avaliação das alternativas em h791; objetivo criado em h791. Resultado: Afastamento físico realizado; o conflito social pode continuar.
  Antes: HP 40, fome 61, dinheiro 6, comida 1; raiva 95.3, ressentimento 99.4, desespero 79.8. Depois: HP 40, dinheiro 6, comida 1.

- **h791 · evento#676447 · CharacterFled**: Elena Vale afastou-se do confronto. [ator Elena Vale (#624); alvo sem personagem identificado]

  Necessidade `response`; prioridade 90.25; fato#559982, confiança 30%, origem rumor. Ação `flee`, score do objetivo 85.95; alternativa `confront`=72.55. Avaliação das alternativas em h791; objetivo criado em h791. Resultado: Afastamento físico realizado; o conflito social pode continuar.
  Antes: HP 40, fome 61, dinheiro 6, comida 1; raiva 95.3, ressentimento 99.4, desespero 79.8. Depois: HP 40, dinheiro 6, comida 1.

Fatos do arco não exibidos neste recorte: 84. IDs integrais no catálogo.

## L14 — Proteção e intervenção de terceiros — Marie Stone (#5080)

Arco **62859**; h1808→h2414; 140 fatos; 6 participantes diretos. Tipo: `causal_or_single`.

**Leitura da história:** em h1808, Dorvia, o primeiro registro deste recorte diz: Marie Stone roubou comida no mercado de Dorvia.

Este recorte não contém morte, captura, reparação, socorro, consolo ou fixação residencial. A tensão/ação registrada não deve receber um encerramento inventado.

Os elos se conectam por fonte de evento/necessidade executada; o registro da fonte demonstra a referência causal do agente, sem garantir que aquela informação seja completa ou que toda a vida esteja neste arco.

Desfechos presentes: nenhum desfecho terminal registrado.

**Limite de qualidade:** o arco contém muita repetição de agressões. Continuidade causal aparece, mas a frequência de golpes não equivale a novos objetivos ou capítulos distintos.

- **h1808 · evento#1514186 · ItemStolen**: Marie Stone roubou comida no mercado de Dorvia. [ator Marie Stone (#5080); alvo Dorvia (cidade#1484)]

  Necessidade `food`; prioridade 100; origem interna `physiology`, sem fato externo de referência. Ação `steal`, score do objetivo 72.47; alternativa `buy_food`=76.40. Avaliação das alternativas em h1808; objetivo criado em h1805. Resultado: Alimento roubado.
  Antes: HP 75, fome 86, dinheiro 3, comida 0; raiva 90.4, ressentimento 98.6, desespero 20.8. Depois: HP 75, dinheiro 3, comida 1.

- **h1810 · evento#1515683 · ConflictStarted**: Iria Kars iniciou confronto físico com Marie Stone. [ator Iria Kars (#5065); alvo Marie Stone (#5080)]

  Necessidade `protection`; prioridade 74.67400000000002; fato#1514186, confiança 100%, origem direct. Ação `attack`, score do objetivo 88.48; alternativa `denounce`=86.95. Avaliação das alternativas em h1810; objetivo criado em h1810. Resultado: Ataque causou 6 de dano real.
  Antes: HP 100, fome 40, dinheiro 5, comida 1; raiva 86.3, ressentimento 99.8, desespero 100.0. Depois: HP 100, dinheiro 5, comida 1.

- **h1810 · evento#1515684 · CharacterAttacked**: Iria Kars feriu Marie Stone em 6 HP. [ator Iria Kars (#5065); alvo Marie Stone (#5080)]

  Necessidade `protection`; prioridade 74.67400000000002; fato#1514186, confiança 100%, origem direct. Ação `attack`, score do objetivo 88.48; alternativa `denounce`=86.95. Avaliação das alternativas em h1810; objetivo criado em h1810. Resultado: Ataque causou 6 de dano real.
  Antes: HP 100, fome 40, dinheiro 5, comida 1; raiva 86.3, ressentimento 99.8, desespero 100.0. Depois: HP 100, dinheiro 5, comida 1.

- **h1810 · evento#1515686 · CharacterAttacked**: Marie Stone feriu Iria Kars em 5 HP. [ator Marie Stone (#5080); alvo Iria Kars (#5065)]

  Necessidade `response`; prioridade 89.968; fato#1515684, confiança 100%, origem direct. Ação `attack`, score do objetivo 135.69; alternativa `defend`=96.00. Avaliação das alternativas em h1810; objetivo criado em h1810. Resultado: Ataque causou 5 de dano real.
  Antes: HP 69, fome 50, dinheiro 3, comida 0; raiva 99.7, ressentimento 100.0, desespero 21.3. Depois: HP 69, dinheiro 3, comida 0.

- **h1811 · evento#1516476 · CharacterAttacked**: Iria Kars feriu Marie Stone em 5 HP. [ator Iria Kars (#5065); alvo Marie Stone (#5080)]

  Necessidade `response`; prioridade 90.11800000000001; fato#1515686, confiança 100%, origem direct. Ação `attack`, score do objetivo 119.39; alternativa `defend`=87.68. Avaliação das alternativas em h1811; objetivo criado em h1811. Resultado: Ataque causou 5 de dano real.
  Antes: HP 95, fome 42, dinheiro 5, comida 1; raiva 99.7, ressentimento 100.0, desespero 100.0. Depois: HP 95, dinheiro 5, comida 1.

- **h1811 · evento#1516478 · CharacterAttacked**: Marie Stone feriu Iria Kars em 4 HP. [ator Marie Stone (#5080); alvo Iria Kars (#5065)]

  Necessidade `response`; prioridade 90.11800000000001; fato#1516476, confiança 100%, origem direct. Ação `attack`, score do objetivo 135.34; alternativa `defend`=95.66. Avaliação das alternativas em h1811; objetivo criado em h1811. Resultado: Ataque causou 4 de dano real.
  Antes: HP 64, fome 52, dinheiro 3, comida 0; raiva 99.7, ressentimento 100.0, desespero 21.5. Depois: HP 64, dinheiro 3, comida 0.

- **h2407 · evento#1981561 · CharacterAttacked**: Arthus Kars feriu Ruan Stone em 6 HP. [ator Arthus Kars (#5071); alvo Ruan Stone (#5077)]

  Necessidade `protection`; prioridade 92.16200000000008; fato#1620127, confiança 30%, origem rumor. Ação `attack`, score do objetivo 106.42; alternativa `defend`=90.90. Avaliação das alternativas em h2407; objetivo criado em h2407. Resultado: Ataque causou 6 de dano real.
  Antes: HP 100, fome 57, dinheiro 1, comida 0; raiva 47.9, ressentimento 94.4, desespero 100.0. Depois: HP 100, dinheiro 1, comida 0.

- **h2408 · evento#1982303 · CharacterAttacked**: Arthus Kars feriu Ruan Stone em 2 HP. [ator Arthus Kars (#5071); alvo Ruan Stone (#5077)]

  Necessidade `protection`; prioridade 92.28000000000009; fato#1620127, confiança 30%, origem rumor. Ação `attack`, score do objetivo 106.90; alternativa `defend`=90.62. Avaliação das alternativas em h2408; objetivo criado em h2408. Resultado: Ataque causou 2 de dano real.
  Antes: HP 100, fome 59, dinheiro 1, comida 0; raiva 47.6, ressentimento 94.4, desespero 100.0. Depois: HP 100, dinheiro 1, comida 0.

- **h2409 · evento#1983055 · PursuitSearch**: Arthus Kars verificou a última localização conhecida sem encontrar o alvo. [ator Arthus Kars (#5071); alvo sem personagem identificado]
- **h2414 · evento#1986857 · ThreatReported**: Arthus Kars denunciou um acontecimento conhecido a Iria Corven. [ator Arthus Kars (#5071); alvo Iria Corven (#5082)]

  Necessidade `protection`; prioridade 92.98800000000008; fato#1620127, confiança 30%, origem rumor. Ação `denounce`, score do objetivo 76.60. Avaliação das alternativas em h2414; objetivo criado em h2410. Resultado: Denúncia registrada por autoridade que já conhece o fato.
  Antes: HP 100, fome 71, dinheiro 1, comida 0; raiva 45.8, ressentimento 94.2, desespero 100.0. Depois: HP 100, dinheiro 1, comida 0.

Fatos do arco não exibidos neste recorte: 130. IDs integrais no catálogo.

## L15 — Proteção e intervenção de terceiros — Lyra Ferros (#2964)

Arco **55890**; h1601→h2206; 88 fatos; 6 participantes diretos. Tipo: `causal_or_single`.

**Leitura da história:** em h1601, Dorven, o primeiro registro deste recorte diz: Lyra Ferros roubou comida no mercado de Dorven.

Este recorte não contém morte, captura, reparação, socorro, consolo ou fixação residencial. A tensão/ação registrada não deve receber um encerramento inventado.

Os elos se conectam por fonte de evento/necessidade executada; o registro da fonte demonstra a referência causal do agente, sem garantir que aquela informação seja completa ou que toda a vida esteja neste arco.

Desfechos presentes: nenhum desfecho terminal registrado.

**Limite de qualidade:** o arco contém muita repetição de agressões. Continuidade causal aparece, mas a frequência de golpes não equivale a novos objetivos ou capítulos distintos.

- **h1601 · evento#1349500 · ItemStolen**: Lyra Ferros roubou comida no mercado de Dorven. [ator Lyra Ferros (#2964); alvo Dorven (cidade#555)]

  Necessidade `food_reserve`; prioridade 71.38461538461539; origem interna `food_reserve`, sem fato externo de referência. Ação `steal`, score do objetivo 77.97; alternativa `buy_food`=78.00. Avaliação das alternativas em h1601; objetivo criado em h1601. Resultado: Alimento roubado.
  Antes: HP 100, fome 65, dinheiro 10, comida 0; raiva 99.7, ressentimento 100.0, desespero 100.0. Depois: HP 100, dinheiro 10, comida 1.

- **h1601 · evento#1349502 · WantedIssued**: Iria Luar registrou procura por Lyra Ferros. [ator Iria Luar (#567); alvo Dorven (cidade#555)]
- **h1602 · evento#1350345 · ConflictEnded**: O confronto de Lyra Ferros terminou: flee. [ator Lyra Ferros (#2964); alvo Iria Luar (#567)]

  Necessidade `response`; prioridade 70.086; fato#1349502, confiança 100%, origem direct. Ação `flee`, score do objetivo 88.18; alternativa `confront`=68.15. Avaliação das alternativas em h1602; objetivo criado em h1602. Resultado: Afastamento físico realizado; o conflito social pode continuar.
  Antes: HP 100, fome 67, dinheiro 10, comida 1; raiva 99.4, ressentimento 99.9, desespero 100.0. Depois: HP 100, dinheiro 10, comida 1.

- **h1653 · evento#1390416 · CharacterAttacked**: Iria Luar feriu Lyra Ferros em 10 HP. [ator Iria Luar (#567); alvo Lyra Ferros (#2964)]

  Necessidade `pursuit`; prioridade 75.65; fato#1349500, confiança 100%, origem direct. Ação `attack`, score do objetivo 88.54; alternativa `demand_return`=66.20. Avaliação das alternativas em h1653; objetivo criado em h1653. Resultado: Ataque causou 10 de dano real.
  Antes: HP 100, fome 41, dinheiro 10, comida 0; raiva 88.9, ressentimento 99.7, desespero 100.0. Depois: HP 100, dinheiro 10, comida 0.

- **h1655 · evento#1392042 · CharacterAttacked**: Iria Luar feriu Lyra Ferros em 5 HP. [ator Iria Luar (#567); alvo Lyra Ferros (#2964)]

  Necessidade `pursuit`; prioridade 75.95; fato#1349500, confiança 100%, origem direct. Ação `attack`, score do objetivo 113.65; alternativa `defend`=79.38. Avaliação das alternativas em h1655; objetivo criado em h1655. Resultado: Ataque causou 5 de dano real.
  Antes: HP 100, fome 45, dinheiro 10, comida 0; raiva 88.3, ressentimento 99.6, desespero 100.0. Depois: HP 100, dinheiro 10, comida 0.

- **h1656 · evento#1392948 · CharacterAttacked**: Iria Luar feriu Lyra Ferros em 6 HP. [ator Iria Luar (#567); alvo Lyra Ferros (#2964)]

  Necessidade `pursuit`; prioridade 76.0; fato#1349500, confiança 100%, origem direct. Ação `attack`, score do objetivo 113.71; alternativa `defend`=79.29. Avaliação das alternativas em h1656; objetivo criado em h1656. Resultado: Ataque causou 6 de dano real.
  Antes: HP 100, fome 47, dinheiro 10, comida 0; raiva 88.0, ressentimento 99.6, desespero 100.0. Depois: HP 100, dinheiro 10, comida 0.

- **h1657 · evento#1393779 · CharacterAttacked**: Iria Luar feriu Lyra Ferros em 5 HP. [ator Iria Luar (#567); alvo Lyra Ferros (#2964)]

  Necessidade `pursuit`; prioridade 76.0; fato#1349500, confiança 100%, origem direct. Ação `attack`, score do objetivo 113.82; alternativa `defend`=79.17. Avaliação das alternativas em h1657; objetivo criado em h1657. Resultado: Ataque causou 5 de dano real.
  Antes: HP 100, fome 49, dinheiro 10, comida 0; raiva 87.7, ressentimento 99.6, desespero 100.0. Depois: HP 100, dinheiro 10, comida 0.

- **h2048 · evento#1703189 · PursuitSearch**: Iria Luar verificou a última localização conhecida sem encontrar o alvo. [ator Iria Luar (#567); alvo sem personagem identificado]
- **h2172 · evento#1799129 · InformationShared**: Bela Ferros informou John Ferros: Iria Luar feriu John Ferros em 10 HP. [ator Bela Ferros (#3038); alvo John Ferros (#3035)]

  Necessidade `protection`; prioridade 99.168; fato#1581380, confiança 30%, origem rumor. Ação `denounce`, score do objetivo 76.25; alternativa `pursue`=66.05. Avaliação das alternativas em h2172; objetivo criado em h2172. Resultado: Informação transmitida.
  Antes: HP 100, fome 61, dinheiro 1, comida 0; raiva 56.0, ressentimento 93.3, desespero 100.0. Depois: HP 100, dinheiro 1, comida 0.

- **h2172 · evento#1799130 · ThreatReported**: Bela Ferros denunciou um acontecimento conhecido a John Ferros. [ator Bela Ferros (#3038); alvo John Ferros (#3035)]

  Necessidade `protection`; prioridade 99.168; fato#1581380, confiança 30%, origem rumor. Ação `denounce`, score do objetivo 76.25; alternativa `pursue`=66.05. Avaliação das alternativas em h2172; objetivo criado em h2172. Resultado: Informação transmitida.
  Antes: HP 100, fome 61, dinheiro 1, comida 0; raiva 56.0, ressentimento 93.3, desespero 100.0. Depois: HP 100, dinheiro 1, comida 0.

- **h2206 · evento#1825339 · ThreatReported**: John Ferros denunciou um acontecimento conhecido a John Ferros. [ator John Ferros (#3041); alvo John Ferros (#3035)]

  Necessidade `protection`; prioridade 100; fato#1581380, confiança 30%, origem rumor. Ação `denounce`, score do objetivo 72.65; alternativa `pursue`=66.55. Avaliação das alternativas em h2206; objetivo criado em h2206. Resultado: Denúncia registrada por autoridade que já conhece o fato.
  Antes: HP 98, fome 72, dinheiro 0, comida 0; raiva 51.2, ressentimento 98.8, desespero 100.0. Depois: HP 98, dinheiro 0, comida 0.

Fatos do arco não exibidos neste recorte: 77. IDs integrais no catálogo.

## L16 — Tentativa de aliviar tensão — Cael Corven (#171)

Arco **71954**; h2095→h2504; 102 fatos; 6 participantes diretos. Tipo: `causal_or_single`.

**Leitura da história:** em h2095, Valria, o primeiro registro deste recorte diz: Cael Corven roubou comida no mercado de Valria.

Este recorte não contém morte, captura, reparação, socorro, consolo ou fixação residencial. A tensão/ação registrada não deve receber um encerramento inventado.

Os elos se conectam por fonte de evento/necessidade executada; o registro da fonte demonstra a referência causal do agente, sem garantir que aquela informação seja completa ou que toda a vida esteja neste arco.

Desfechos presentes: nenhum desfecho terminal registrado.

**Limite de qualidade:** o arco contém muita repetição de agressões. Continuidade causal aparece, mas a frequência de golpes não equivale a novos objetivos ou capítulos distintos.

- **h2095 · evento#1738829 · ItemStolen**: Cael Corven roubou comida no mercado de Valria. [ator Cael Corven (#171); alvo Valria (cidade#162)]

  Necessidade `food`; prioridade 100; origem interna `physiology`, sem fato externo de referência. Ação `steal`, score do objetivo 78.77; alternativa `buy_food`=78.40. Avaliação das alternativas em h2095; objetivo criado em h2093. Resultado: Alimento roubado.
  Antes: HP 100, fome 88, dinheiro 4, comida 0; raiva 92.2, ressentimento 98.9, desespero 100.0. Depois: HP 100, dinheiro 4, comida 1.

- **h2096 · evento#1739911 · ConflictStarted**: John Ferros iniciou confronto físico com Cael Corven. [ator John Ferros (#2162); alvo Cael Corven (#171)]

  Necessidade `protection`; prioridade 76.86800000000004; fato#1738829, confiança 100%, origem direct. Ação `attack`, score do objetivo 95.84; alternativa `denounce`=66.05. Avaliação das alternativas em h2096; objetivo criado em h2096. Resultado: Ataque causou 6 de dano real.
  Antes: HP 100, fome 62, dinheiro 0, comida 0; raiva 89.8, ressentimento 99.8, desespero 100.0. Depois: HP 100, dinheiro 0, comida 0.

- **h2096 · evento#1739912 · CharacterAttacked**: John Ferros feriu Cael Corven em 6 HP. [ator John Ferros (#2162); alvo Cael Corven (#171)]

  Necessidade `protection`; prioridade 76.86800000000004; fato#1738829, confiança 100%, origem direct. Ação `attack`, score do objetivo 95.84; alternativa `denounce`=66.05. Avaliação das alternativas em h2096; objetivo criado em h2096. Resultado: Ataque causou 6 de dano real.
  Antes: HP 100, fome 62, dinheiro 0, comida 0; raiva 89.8, ressentimento 99.8, desespero 100.0. Depois: HP 100, dinheiro 0, comida 0.

- **h2097 · evento#1740483 · CharacterAttacked**: Cael Corven feriu John Ferros em 2 HP. [ator Cael Corven (#171); alvo John Ferros (#2162)]

  Necessidade `response`; prioridade 90.11800000000001; fato#1739912, confiança 100%, origem direct. Ação `attack`, score do objetivo 100.25; alternativa `defend`=88.39. Avaliação das alternativas em h2097; objetivo criado em h2097. Resultado: Ataque causou 2 de dano real.
  Antes: HP 94, fome 52, dinheiro 4, comida 0; raiva 99.7, ressentimento 100.0, desespero 100.0. Depois: HP 94, dinheiro 4, comida 0.

- **h2097 · evento#1740744 · CharacterAttacked**: John Ferros feriu Cael Corven em 5 HP. [ator John Ferros (#2162); alvo Cael Corven (#171)]

  Necessidade `response`; prioridade 89.968; fato#1740483, confiança 100%, origem direct. Ação `attack`, score do objetivo 125.52; alternativa `defend`=87.32. Avaliação das alternativas em h2097; objetivo criado em h2097. Resultado: Ataque causou 5 de dano real.
  Antes: HP 98, fome 64, dinheiro 0, comida 0; raiva 99.7, ressentimento 100.0, desespero 100.0. Depois: HP 98, dinheiro 0, comida 0.

- **h2098 · evento#1741295 · CharacterAttacked**: Cael Corven feriu John Ferros em 2 HP. [ator Cael Corven (#171); alvo John Ferros (#2162)]

  Necessidade `response`; prioridade 90.268; fato#1740744, confiança 100%, origem direct. Ação `attack`, score do objetivo 99.75; alternativa `defend`=88.12. Avaliação das alternativas em h2098; objetivo criado em h2098. Resultado: Ataque causou 2 de dano real.
  Antes: HP 89, fome 54, dinheiro 4, comida 0; raiva 99.7, ressentimento 100.0, desespero 100.0. Depois: HP 89, dinheiro 4, comida 0.

- **h2421 · evento#1991878 · ConflictEnded**: O confronto de Elena Hammer terminou: flee. [ator Elena Hammer (#2182); alvo John Bruma (#174)]

  Necessidade `protection`; prioridade 91.51350000000001; fato#1881165, confiança 30%, origem rumor. Ação `flee`, score do objetivo 83.43; alternativa `defend`=70.16. Avaliação das alternativas em h2421; objetivo criado em h2421. Resultado: Afastamento físico realizado; o conflito social pode continuar.
  Antes: HP 100, fome 73, dinheiro 0, comida 0; raiva 0.0, ressentimento 27.3, desespero 100.0. Depois: HP 100, dinheiro 0, comida 0.

- **h2421 · evento#1991879 · CharacterFled**: Elena Hammer afastou-se do confronto. [ator Elena Hammer (#2182); alvo sem personagem identificado]

  Necessidade `protection`; prioridade 91.51350000000001; fato#1881165, confiança 30%, origem rumor. Ação `flee`, score do objetivo 83.43; alternativa `defend`=70.16. Avaliação das alternativas em h2421; objetivo criado em h2421. Resultado: Afastamento físico realizado; o conflito social pode continuar.
  Antes: HP 100, fome 73, dinheiro 0, comida 0; raiva 0.0, ressentimento 27.3, desespero 100.0. Depois: HP 100, dinheiro 0, comida 0.

- **h2503 · evento#2053783 · PursuitSearch**: Elena Hammer verificou a última localização conhecida sem encontrar o alvo. [ator Elena Hammer (#2182); alvo sem personagem identificado]

  Necessidade `protection`; prioridade 85.64950000000002; fato#1881165, confiança 30%, origem rumor. Ação `pursue`, score do objetivo 79.60; alternativa `ask_personal_help`=30.20. Avaliação das alternativas em h2503; objetivo criado em h2503. Resultado: Busca local sem encontro; não consulta posição remota.
  Antes: HP 100, fome 77, dinheiro 1, comida 0; raiva 0.0, ressentimento 24.0, desespero 100.0. Depois: HP 100, dinheiro 1, comida 0.

- **h2504 · evento#2054579 · PursuitSearch**: Elena Hammer verificou a última localização conhecida sem encontrar o alvo. [ator Elena Hammer (#2182); alvo sem personagem identificado]
Fatos do arco não exibidos neste recorte: 92. IDs integrais no catálogo.

## L17 — Tentativa de aliviar tensão — Lyra Luar (#3429)

Arco **68530**; h1987→h2381; 52 fatos; 8 participantes diretos. Tipo: `causal_or_single`.

**Leitura da história:** em h1987, Karmir, o primeiro registro deste recorte diz: Lyra Luar roubou comida no mercado de Karmir.

Este recorte não contém morte, captura, reparação, socorro, consolo ou fixação residencial. A tensão/ação registrada não deve receber um encerramento inventado.

Os elos se conectam por fonte de evento/necessidade executada; o registro da fonte demonstra a referência causal do agente, sem garantir que aquela informação seja completa ou que toda a vida esteja neste arco.

Desfechos presentes: nenhum desfecho terminal registrado.

- **h1987 · evento#1655469 · ItemStolen**: Lyra Luar roubou comida no mercado de Karmir. [ator Lyra Luar (#3429); alvo Karmir (cidade#742)]

  Necessidade `food_reserve`; prioridade 77.18872017353578; origem interna `food_reserve`, sem fato externo de referência. Ação `steal`, score do objetivo 84.17; alternativa `forage`=71.00. Avaliação das alternativas em h1987; objetivo criado em h1986. Resultado: Alimento roubado.
  Antes: HP 100, fome 60, dinheiro 0, comida 0; raiva 89.9, ressentimento 98.8, desespero 100.0. Depois: HP 100, dinheiro 0, comida 1.

- **h1989 · evento#1656982 · CharacterInsulted**: Nora Montes: insult diante de Lyra Luar. [ator Nora Montes (#3452); alvo Lyra Luar (#3429)]

  Necessidade `protection`; prioridade 81.154; fato#1655469, confiança 100%, origem direct. Ação `insult`, score do objetivo 72.07; alternativa `threaten`=70.48. Avaliação das alternativas em h1989; objetivo criado em h1989. Resultado: Interação estruturada registrada: insult.
  Antes: HP 100, fome 72, dinheiro 1, comida 1; raiva 99.1, ressentimento 99.9, desespero 100.0. Depois: HP 100, dinheiro 1, comida 1.

- **h1990 · evento#1657757 · CharacterThreatened**: Nora Montes: threaten diante de Lyra Luar. [ator Nora Montes (#3452); alvo Lyra Luar (#3429)]

  Necessidade `protection`; prioridade 81.272; fato#1655469, confiança 100%, origem direct. Ação `threaten`, score do objetivo 70.39; alternativa `demand_return`=62.50. Avaliação das alternativas em h1990; objetivo criado em h1990. Resultado: Interação estruturada registrada: threaten.
  Antes: HP 100, fome 74, dinheiro 1, comida 1; raiva 98.8, ressentimento 99.8, desespero 100.0. Depois: HP 100, dinheiro 1, comida 1.

- **h2118 · evento#1757242 · CharacterAttacked**: Lyra Ferros feriu Nora Montes em 10 HP. [ator Lyra Ferros (#3443); alvo Nora Montes (#3452)]

  Necessidade `protection`; prioridade 78.034; fato#1657757, confiança 30%, origem rumor. Ação `attack`, score do objetivo 87.52; alternativa `protect`=72.79. Avaliação das alternativas em h2118; objetivo criado em h2118. Resultado: Ataque causou 10 de dano real.
  Antes: HP 100, fome 47, dinheiro 5, comida 1; raiva 98.9, ressentimento 99.8, desespero 100.0. Depois: HP 100, dinheiro 5, comida 1.

- **h2186 · evento#1810275 · CharacterAttacked**: Lyra Ferros feriu Lyra Solaris em 5 HP. [ator Lyra Ferros (#3443); alvo Lyra Solaris (#754)]

  Necessidade `response`; prioridade 68.238; fato#1790800, confiança 100%, origem direct. Ação `attack`, score do objetivo 61.82; alternativa `confront`=61.20. Avaliação das alternativas em h2186; objetivo criado em h2186. Resultado: Ataque causou 5 de dano real.
  Antes: HP 100, fome 63, dinheiro 9, comida 3; raiva 95.2, ressentimento 99.4, desespero 100.0. Depois: HP 100, dinheiro 9, comida 3.

- **h2187 · evento#1810682 · CharacterAttacked**: Lyra Solaris feriu Lyra Ferros em 10 HP. [ator Lyra Solaris (#754); alvo Lyra Ferros (#3443)]

  Necessidade `response`; prioridade 97.968; fato#1810275, confiança 100%, origem direct. Ação `attack`, score do objetivo 92.09; alternativa `defend`=89.38. Avaliação das alternativas em h2187; objetivo criado em h2187. Resultado: Ataque causou 10 de dano real.
  Antes: HP 95, fome 69, dinheiro 4, comida 1; raiva 99.7, ressentimento 100.0, desespero 85.1. Depois: HP 95, dinheiro 4, comida 1.

- **h2187 · evento#1810991 · CharacterAttacked**: Lyra Ferros feriu Lyra Solaris em 4 HP. [ator Lyra Ferros (#3443); alvo Lyra Solaris (#754)]

  Necessidade `response`; prioridade 93.86800000000001; fato#1810682, confiança 100%, origem direct. Ação `attack`, score do objetivo 88.11; alternativa `defend`=86.89. Avaliação das alternativas em h2187; objetivo criado em h2187. Resultado: Ataque causou 4 de dano real.
  Antes: HP 90, fome 65, dinheiro 9, comida 3; raiva 99.7, ressentimento 100.0, desespero 100.0. Depois: HP 90, dinheiro 9, comida 3.

- **h2377 · evento#1958212 · PursuitSearch**: Darin Ferros verificou a última localização conhecida sem encontrar o alvo. [ator Darin Ferros (#3446); alvo sem personagem identificado]

  Necessidade `protection`; prioridade 92.913; fato#1818913, confiança 30%, origem rumor. Ação `pursue`, score do objetivo 63.30; alternativa `avoid_threat`=39.55. Avaliação das alternativas em h2377; objetivo criado em h2377. Resultado: Busca local sem encontro; não consulta posição remota.
  Antes: HP 100, fome 65, dinheiro 25, comida 0; raiva 7.2, ressentimento 4.9, desespero 0.0. Depois: HP 100, dinheiro 25, comida 0.

- **h2378 · evento#1959005 · PursuitSearch**: Darin Ferros verificou a última localização conhecida sem encontrar o alvo. [ator Darin Ferros (#3446); alvo sem personagem identificado]
- **h2380 · evento#1960578 · CalmingAttempted**: Darin Ferros: calm diante de Lyra Solaris. [ator Darin Ferros (#3446); alvo Lyra Solaris (#754)]

  Necessidade `protection`; prioridade 93.267; fato#1818913, confiança 30%, origem rumor. Ação `calm`, score do objetivo 58.36; alternativa `defend`=55.90. Avaliação das alternativas em h2380; objetivo criado em h2380. Resultado: Interação estruturada registrada: calm.
  Antes: HP 100, fome 71, dinheiro 25, comida 0; raiva 6.3, ressentimento 4.7, desespero 0.0. Depois: HP 100, dinheiro 25, comida 0.

- **h2381 · evento#1961310 · CharacterDefended**: Darin Ferros adotou defesa. [ator Darin Ferros (#3446); alvo sem personagem identificado]

  Necessidade `protection`; prioridade 93.38499999999999; fato#1818913, confiança 30%, origem rumor. Ação `defend`, score do objetivo 55.90; alternativa `withdraw`=54.35. Avaliação das alternativas em h2381; objetivo criado em h2381. Resultado: Defesa temporária adotada.
  Antes: HP 100, fome 73, dinheiro 25, comida 0; raiva 6.0, ressentimento 4.7, desespero 0.0. Depois: HP 100, dinheiro 25, comida 0.

Fatos do arco não exibidos neste recorte: 41. IDs integrais no catálogo.

## L18 — Rendição — Marie Ferros (#2064)

Arco **34090**; h970→h1351; 129 fatos; 9 participantes diretos. Tipo: `causal_or_single`.

**Leitura da história:** em h970, Mordor, o primeiro registro deste recorte diz: Marie Ferros roubou comida no mercado de Mordor.

Este recorte não contém morte, captura, reparação, socorro, consolo ou fixação residencial. A tensão/ação registrada não deve receber um encerramento inventado.

Os elos se conectam por fonte de evento/necessidade executada; o registro da fonte demonstra a referência causal do agente, sem garantir que aquela informação seja completa ou que toda a vida esteja neste arco.

Desfechos presentes: nenhum desfecho terminal registrado.

**Limite de qualidade:** o arco contém muita repetição de agressões. Continuidade causal aparece, mas a frequência de golpes não equivale a novos objetivos ou capítulos distintos.

- **h970 · evento#828920 · ItemStolen**: Marie Ferros roubou comida no mercado de Mordor. [ator Marie Ferros (#2064); alvo Mordor (cidade#180)]

  Necessidade `food`; prioridade 100; origem interna `physiology`, sem fato externo de referência. Ação `steal`, score do objetivo 82.00; alternativa `steal_person`=66.70. Avaliação das alternativas em h970; objetivo criado em h966. Resultado: Alimento roubado.
  Antes: HP 69, fome 92, dinheiro 0, comida 0; raiva 69.0, ressentimento 100.0, desespero 14.2. Depois: HP 69, dinheiro 0, comida 1.

- **h970 · evento#828922 · WantedIssued**: Arthus Luar registrou procura por Marie Ferros. [ator Arthus Luar (#127); alvo Mordor (cidade#180)]
- **h970 · evento#828954 · ConflictStarted**: Elena Bruma iniciou confronto físico com Marie Ferros. [ator Elena Bruma (#2209); alvo Marie Ferros (#2064)]

  Necessidade `protection`; prioridade 72.104; fato#828920, confiança 100%, origem direct. Ação `attack`, score do objetivo 97.67; alternativa `denounce`=94.45. Avaliação das alternativas em h970; objetivo criado em h970. Resultado: Ataque causou 6 de dano real.
  Antes: HP 100, fome 39, dinheiro 7, comida 0; raiva 99.1, ressentimento 99.9, desespero 71.7. Depois: HP 100, dinheiro 7, comida 0.

- **h970 · evento#828955 · CharacterAttacked**: Elena Bruma feriu Marie Ferros em 6 HP. [ator Elena Bruma (#2209); alvo Marie Ferros (#2064)]

  Necessidade `protection`; prioridade 72.104; fato#828920, confiança 100%, origem direct. Ação `attack`, score do objetivo 97.67; alternativa `denounce`=94.45. Avaliação das alternativas em h970; objetivo criado em h970. Resultado: Ataque causou 6 de dano real.
  Antes: HP 100, fome 39, dinheiro 7, comida 0; raiva 99.1, ressentimento 99.9, desespero 71.7. Depois: HP 100, dinheiro 7, comida 0.

- **h999 · evento#853647 · CharacterAttacked**: Arthus Luar feriu Elena Bruma em 12 HP. [ator Arthus Luar (#127); alvo Elena Bruma (#2209)]

  Necessidade `pursuit`; prioridade 78.2; fato#828955 fora da memória curta amostrada; necessidade/caso pode conservar referência própria. Ação `attack`, score do objetivo 70.07; alternativa `defend`=49.73. Avaliação das alternativas em h999; objetivo criado em h999. Resultado: Ataque causou 12 de dano real.
  Antes: HP 100, fome 57, dinheiro 5, comida 0; raiva 76.5, ressentimento 98.8, desespero 40.3. Depois: HP 100, dinheiro 5, comida 0.

- **h999 · evento#853912 · CharacterAttacked**: Elena Bruma feriu Arthus Luar em 6 HP. [ator Elena Bruma (#2209); alvo Arthus Luar (#127)]

  Necessidade `response`; prioridade 94.25399999999999; fato#853647, confiança 100%, origem direct. Ação `attack`, score do objetivo 104.20; alternativa `defend`=91.66. Avaliação das alternativas em h999; objetivo criado em h999. Resultado: Ataque causou 6 de dano real.
  Antes: HP 88, fome 57, dinheiro 5, comida 0; raiva 99.1, ressentimento 99.9, desespero 76.0. Depois: HP 88, dinheiro 5, comida 0.

- **h1000 · evento#854510 · CharacterAttacked**: Arthus Luar feriu Elena Bruma em 7 HP. [ator Arthus Luar (#127); alvo Elena Bruma (#2209)]

  Necessidade `response`; prioridade 90.11800000000001; fato#853912, confiança 100%, origem direct. Ação `attack`, score do objetivo 93.41; alternativa `defend`=79.09. Avaliação das alternativas em h1000; objetivo criado em h1000. Resultado: Ataque causou 7 de dano real.
  Antes: HP 94, fome 59, dinheiro 5, comida 0; raiva 99.7, ressentimento 100.0, desespero 40.5. Depois: HP 94, dinheiro 5, comida 0.

- **h1309 · evento#1109850 · CharacterConfronted**: Mira Kars: confront diante de Elena Bruma. [ator Mira Kars (#2234); alvo Elena Bruma (#2209)]

  Necessidade `pursuit`; prioridade 82.0; fato#977223 fora da memória curta amostrada; necessidade/caso pode conservar referência própria. Ação `confront`, score do objetivo 72.55; alternativa `surrender`=68.12. Avaliação das alternativas em h1309; objetivo criado em h1309. Resultado: Interação estruturada registrada: confront.
  Antes: HP 41, fome 66, dinheiro 8, comida 0; raiva 98.8, ressentimento 99.8, desespero 87.8. Depois: HP 41, dinheiro 8, comida 0.

- **h1310 · evento#1110573 · ConflictEnded**: O confronto de Mira Kars terminou: surrender. [ator Mira Kars (#2234); alvo Elena Bruma (#2209)]

  Necessidade `pursuit`; prioridade 82.0; fato#977223 fora da memória curta amostrada; necessidade/caso pode conservar referência própria. Ação `surrender`, score do objetivo 68.12; alternativa `flee`=65.09. Avaliação das alternativas em h1310; objetivo criado em h1310. Resultado: Rendição registrada; não implica morte.
  Antes: HP 41, fome 68, dinheiro 8, comida 0; raiva 98.5, ressentimento 99.8, desespero 88.0. Depois: HP 41, dinheiro 8, comida 0.

- **h1310 · evento#1110574 · CharacterSurrendered**: Mira Kars rendeu-se. [ator Mira Kars (#2234); alvo Elena Bruma (#2209)]

  Necessidade `pursuit`; prioridade 82.0; fato#977223 fora da memória curta amostrada; necessidade/caso pode conservar referência própria. Ação `surrender`, score do objetivo 68.12; alternativa `flee`=65.09. Avaliação das alternativas em h1310; objetivo criado em h1310. Resultado: Rendição registrada; não implica morte.
  Antes: HP 41, fome 68, dinheiro 8, comida 0; raiva 98.5, ressentimento 99.8, desespero 88.0. Depois: HP 41, dinheiro 8, comida 0.

- **h1351 · evento#1143623 · ProtectionGiven**: Tomas Solaris permaneceu próximo de Elena Bruma. [ator Tomas Solaris (#2257); alvo Elena Bruma (#2209)]

  Necessidade `protection`; prioridade 80.844; fato#1109850 fora da memória curta amostrada; necessidade/caso pode conservar referência própria. Ação `stay_near`, score do objetivo 52.40; alternativa `ask_personal_help`=51.15. Avaliação das alternativas em h1351; objetivo criado em h1351. Resultado: Acompanhou o protegido.
  Antes: HP 100, fome 46, dinheiro 5, comida 0; raiva 95.7, ressentimento 99.4, desespero 57.7. Depois: HP 100, dinheiro 5, comida 0.

Fatos do arco não exibidos neste recorte: 118. IDs integrais no catálogo.

## L19 — Rendição — Cael Bruma (#2697)

Arco **62336**; h1790→h2171; 110 fatos; 7 participantes diretos. Tipo: `causal_or_single`.

**Leitura da história:** em h1790, Normar, o primeiro registro deste recorte diz: Cael Bruma roubou provisão de Nora Kars.

Este recorte não contém morte, captura, reparação, socorro, consolo ou fixação residencial. A tensão/ação registrada não deve receber um encerramento inventado.

Os elos se conectam por fonte de evento/necessidade executada; o registro da fonte demonstra a referência causal do agente, sem garantir que aquela informação seja completa ou que toda a vida esteja neste arco.

Desfechos presentes: nenhum desfecho terminal registrado.

**Limite de qualidade:** o arco contém muita repetição de agressões. Continuidade causal aparece, mas a frequência de golpes não equivale a novos objetivos ou capítulos distintos.

- **h1790 · evento#1499354 · ItemStolen**: Cael Bruma roubou provisão de Nora Kars. [ator Cael Bruma (#2697); alvo Nora Kars (#2732)]

  Necessidade `money`; prioridade 87.6; origem interna `economy`, sem fato externo de referência. Ação `steal_person`, score do objetivo 31.20. Avaliação das alternativas em h1790; objetivo criado em h1790. Resultado: Provisão real roubada.
  Antes: HP 100, fome 50, dinheiro 2, comida 0; raiva 58.8, ressentimento 94.2, desespero 100.0. Depois: HP 100, dinheiro 2, comida 1.

- **h1790 · evento#1499358 · GuardResponded**: Aldren Kars interveio no roubo e cobrou 2 moedas de Cael Bruma. [ator Aldren Kars (#2734); alvo Cael Bruma (#2697)]

  Necessidade `security`; prioridade 84.4; fato#1499354, confiança 100%, origem direct. Ação `secure`, score do objetivo 84.67. Avaliação das alternativas em h1790; objetivo criado em h1790. Resultado: Suspeito encontrado; intervenção registrada.
  Antes: HP 100, fome 60, dinheiro 11, comida 1; raiva 92.2, ressentimento 99.8, desespero 100.0. Depois: HP 100, dinheiro 11, comida 1.

- **h1823 · evento#1525825 · InformationShared**: Aldren Kars informou Darin Corven: Cael Bruma roubou provisão de Nora Kars. [ator Aldren Kars (#2734); alvo Darin Corven (#2711)]

  Necessidade `protection`; prioridade 76.14800000000001; fato#1499354, confiança 100%, origem direct. Ação `denounce`, score do objetivo 94.15; alternativa `pursue`=90.65. Avaliação das alternativas em h1823; objetivo criado em h1823. Resultado: Informação transmitida.
  Antes: HP 100, fome 46, dinheiro 9, comida 0; raiva 83.7, ressentimento 98.5, desespero 100.0. Depois: HP 100, dinheiro 9, comida 0.

- **h1916 · evento#1599290 · CharacterAttacked**: Bela Montes feriu Cael Bruma em 11 HP. [ator Bela Montes (#2757); alvo Cael Bruma (#2697)]

  Necessidade `pursuit`; prioridade 76.0; fato#1555115, confiança 100%, origem direct. Ação `attack`, score do objetivo 90.62; alternativa `confront`=70.16. Avaliação das alternativas em h1916; objetivo criado em h1916. Resultado: Ataque causou 11 de dano real.
  Antes: HP 100, fome 66, dinheiro 15, comida 1; raiva 90.5, ressentimento 98.8, desespero 89.5. Depois: HP 100, dinheiro 15, comida 1.

- **h1917 · evento#1600179 · CharacterAttacked**: Bela Montes feriu Cael Bruma em 12 HP. [ator Bela Montes (#2757); alvo Cael Bruma (#2697)]

  Necessidade `pursuit`; prioridade 76.0; fato#1555115, confiança 100%, origem direct. Ação `attack`, score do objetivo 116.03; alternativa `defend`=83.28. Avaliação das alternativas em h1917; objetivo criado em h1917. Resultado: Ataque causou 12 de dano real.
  Antes: HP 100, fome 68, dinheiro 15, comida 1; raiva 90.2, ressentimento 98.8, desespero 89.7. Depois: HP 100, dinheiro 15, comida 1.

- **h1918 · evento#1601011 · CharacterAttacked**: Bela Montes feriu Cael Bruma em 13 HP. [ator Bela Montes (#2757); alvo Cael Bruma (#2697)]

  Necessidade `pursuit`; prioridade 76.0; fato#1555115 fora da memória curta amostrada; necessidade/caso pode conservar referência própria. Ação `attack`, score do objetivo 116.51; alternativa `defend`=82.99. Avaliação das alternativas em h1918; objetivo criado em h1918. Resultado: Ataque causou 13 de dano real.
  Antes: HP 100, fome 70, dinheiro 15, comida 1; raiva 89.9, ressentimento 98.8, desespero 89.8. Depois: HP 100, dinheiro 15, comida 1.

- **h1919 · evento#1601745 · CharacterAttacked**: Bela Montes feriu Cael Bruma em 12 HP. [ator Bela Montes (#2757); alvo Cael Bruma (#2697)]

  Necessidade `pursuit`; prioridade 76.0; fato#1555115 fora da memória curta amostrada; necessidade/caso pode conservar referência própria. Ação `attack`, score do objetivo 117.07; alternativa `defend`=82.67. Avaliação das alternativas em h1919; objetivo criado em h1919. Resultado: Ataque causou 12 de dano real.
  Antes: HP 100, fome 72, dinheiro 15, comida 1; raiva 89.6, ressentimento 98.7, desespero 90.0. Depois: HP 100, dinheiro 15, comida 1.

- **h2152 · evento#1783575 · ConflictEnded**: O confronto de Darin Corven terminou: surrender. [ator Darin Corven (#2711); alvo Bela Montes (#2757)]

  Necessidade `protection`; prioridade 100; fato#1726295, confiança 30%, origem rumor. Ação `surrender`, score do objetivo 56.83; alternativa `defend`=57.03. Avaliação das alternativas em h2152; objetivo criado em h2152. Resultado: Rendição registrada; não implica morte.
  Antes: HP 100, fome 68, dinheiro 3, comida 0; raiva 81.4, ressentimento 97.4, desespero 100.0. Depois: HP 100, dinheiro 3, comida 0.

- **h2152 · evento#1783576 · CharacterSurrendered**: Darin Corven rendeu-se. [ator Darin Corven (#2711); alvo Bela Montes (#2757)]

  Necessidade `protection`; prioridade 100; fato#1726295, confiança 30%, origem rumor. Ação `surrender`, score do objetivo 56.83; alternativa `defend`=57.03. Avaliação das alternativas em h2152; objetivo criado em h2152. Resultado: Rendição registrada; não implica morte.
  Antes: HP 100, fome 68, dinheiro 3, comida 0; raiva 81.4, ressentimento 97.4, desespero 100.0. Depois: HP 100, dinheiro 3, comida 0.

- **h2171 · evento#1798348 · InformationShared**: John Vale informou Aldren Kars: Darin Corven: insult diante de Bela Montes. [ator John Vale (#2688); alvo Aldren Kars (#2734)]

  Necessidade `protection`; prioridade 78.56200000000001; fato#1779878, confiança 100%, origem direct. Ação `denounce`, score do objetivo 70.70; alternativa `stay_near`=47.80. Avaliação das alternativas em h2171; objetivo criado em h2171. Resultado: Informação transmitida.
  Antes: HP 100, fome 48, dinheiro 7, comida 0; raiva 61.0, ressentimento 94.2, desespero 100.0. Depois: HP 100, dinheiro 7, comida 0.

- **h2171 · evento#1798349 · ThreatReported**: John Vale denunciou um acontecimento conhecido a Aldren Kars. [ator John Vale (#2688); alvo Aldren Kars (#2734)]

  Necessidade `protection`; prioridade 78.56200000000001; fato#1779878, confiança 100%, origem direct. Ação `denounce`, score do objetivo 70.70; alternativa `stay_near`=47.80. Avaliação das alternativas em h2171; objetivo criado em h2171. Resultado: Informação transmitida.
  Antes: HP 100, fome 48, dinheiro 7, comida 0; raiva 61.0, ressentimento 94.2, desespero 100.0. Depois: HP 100, dinheiro 7, comida 0.

Fatos do arco não exibidos neste recorte: 99. IDs integrais no catálogo.

## L20 — Fuga física — Ruan Kars (#917)

Arco **97245**; h2909→h3376; 70 fatos; 6 participantes diretos. Tipo: `causal_or_single`.

**Leitura da história:** em h2909, Kardor, o primeiro registro deste recorte diz: Ruan Kars roubou comida no mercado de Kardor.

Este recorte não contém morte, captura, reparação, socorro, consolo ou fixação residencial. A tensão/ação registrada não deve receber um encerramento inventado.

Os elos se conectam por fonte de evento/necessidade executada; o registro da fonte demonstra a referência causal do agente, sem garantir que aquela informação seja completa ou que toda a vida esteja neste arco.

Desfechos presentes: nenhum desfecho terminal registrado.

**Limite de qualidade:** o arco contém muita repetição de agressões. Continuidade causal aparece, mas a frequência de golpes não equivale a novos objetivos ou capítulos distintos.

- **h2909 · evento#2361115 · ItemStolen**: Ruan Kars roubou comida no mercado de Kardor. [ator Ruan Kars (#917); alvo Kardor (cidade#911)]

  Necessidade `food`; prioridade 100; origem interna `physiology`, sem fato externo de referência. Ação `steal`, score do objetivo 59.33; alternativa `forage`=46.50. Avaliação das alternativas em h2909; objetivo criado em h2907. Resultado: Alimento roubado.
  Antes: HP 92, fome 86, dinheiro 0, comida 0; raiva 84.8, ressentimento 100.0, desespero 85.4. Depois: HP 92, dinheiro 0, comida 1.

- **h2909 · evento#2361117 · CharacterAttacked**: Mira Douran feriu Ruan Kars em 12 HP. [ator Mira Douran (#923); alvo Ruan Kars (#917)]

  Necessidade `security`; prioridade 82.7; fato#2361115, confiança 100%, origem direct. Ação `attack`, score do objetivo 103.15; alternativa `defend`=81.17. Avaliação das alternativas em h2909; objetivo criado em h2909. Resultado: Ataque causou 12 de dano real.
  Antes: HP 100, fome 48, dinheiro 8, comida 1; raiva 97.9, ressentimento 99.7, desespero 100.0. Depois: HP 100, dinheiro 8, comida 1.

- **h2909 · evento#2361481 · ProtectionGiven**: Cael Ferros interveio para proteger Ruan Kars. [ator Cael Ferros (#3816); alvo Ruan Kars (#917)]

  Necessidade `protection`; prioridade 92.26800000000001; fato#2361117, confiança 100%, origem direct. Ação `protect`, score do objetivo 62.59; alternativa `stay_near`=60.45. Avaliação das alternativas em h2909; objetivo criado em h2909. Resultado: Intervenção física temporária adotada.
  Antes: HP 100, fome 65, dinheiro 1, comida 0; raiva 34.2, ressentimento 100.0, desespero 34.5. Depois: HP 100, dinheiro 1, comida 0.

- **h2911 · evento#2362580 · CharacterAttacked**: Mira Douran feriu Cael Ferros em 4 HP. [ator Mira Douran (#923); alvo Cael Ferros (#3816)]

  Necessidade `security`; prioridade 82.7; fato#2361115, confiança 100%, origem direct. Ação `attack`, score do objetivo 103.57; alternativa `defend`=80.85. Avaliação das alternativas em h2911; objetivo criado em h2911. Resultado: Ataque causou 4 de dano real.
  Antes: HP 100, fome 52, dinheiro 8, comida 1; raiva 97.3, ressentimento 99.6, desespero 100.0. Depois: HP 100, dinheiro 8, comida 1.

- **h2911 · evento#2362960 · CharacterAttacked**: Cael Ferros feriu Mira Douran em 10 HP. [ator Cael Ferros (#3816); alvo Mira Douran (#923)]

  Necessidade `protection`; prioridade 97.308; fato#2361117, confiança 100%, origem direct. Ação `attack`, score do objetivo 97.85; alternativa `defend`=86.22. Avaliação das alternativas em h2911; objetivo criado em h2911. Resultado: Ataque causou 10 de dano real.
  Antes: HP 96, fome 69, dinheiro 1, comida 0; raiva 81.6, ressentimento 100.0, desespero 34.8. Depois: HP 96, dinheiro 1, comida 0.

- **h2912 · evento#2363338 · CharacterAttacked**: Mira Douran feriu Cael Ferros em 4 HP. [ator Mira Douran (#923); alvo Cael Ferros (#3816)]

  Necessidade `response`; prioridade 90.568; fato#2362960, confiança 100%, origem direct. Ação `attack`, score do objetivo 94.67; alternativa `defend`=84.43. Avaliação das alternativas em h2912; objetivo criado em h2912. Resultado: Ataque causou 4 de dano real.
  Antes: HP 90, fome 54, dinheiro 8, comida 1; raiva 99.7, ressentimento 100.0, desespero 100.0. Depois: HP 90, dinheiro 8, comida 1.

- **h3162 · evento#2549355 · CharacterFled**: John Bruma afastou-se do confronto. [ator John Bruma (#926); alvo sem personagem identificado]

  Necessidade `protection`; prioridade 100; fato#2416801, confiança 30%, origem rumor. Ação `flee`, score do objetivo 99.48; alternativa `denounce`=98.00. Avaliação das alternativas em h3162; objetivo criado em h3162. Resultado: Afastamento físico realizado; o conflito social pode continuar.
  Antes: HP 24, fome 52, dinheiro 0, comida 0; raiva 99.4, ressentimento 99.9, desespero 100.0. Depois: HP 24, dinheiro 0, comida 0.

- **h3368 · evento#2700440 · InformationShared**: Cael Ferros informou Mira Douran: John Bruma feriu Cael Ferros em 5 HP. [ator Cael Ferros (#3822); alvo Mira Douran (#923)]

  Necessidade `protection`; prioridade 96.38800000000006; fato#2547184, confiança 30%, origem rumor. Ação `denounce`, score do objetivo 73.60; alternativa `pursue`=68.15. Avaliação das alternativas em h3368; objetivo criado em h3368. Resultado: Informação transmitida.
  Antes: HP 100, fome 64, dinheiro 0, comida 0; raiva 69.9, ressentimento 99.9, desespero 100.0. Depois: HP 100, dinheiro 0, comida 0.

- **h3368 · evento#2700441 · ThreatReported**: Cael Ferros denunciou um acontecimento conhecido a Mira Douran. [ator Cael Ferros (#3822); alvo Mira Douran (#923)]

  Necessidade `protection`; prioridade 96.38800000000006; fato#2547184, confiança 30%, origem rumor. Ação `denounce`, score do objetivo 73.60; alternativa `pursue`=68.15. Avaliação das alternativas em h3368; objetivo criado em h3368. Resultado: Informação transmitida.
  Antes: HP 100, fome 64, dinheiro 0, comida 0; raiva 69.9, ressentimento 99.9, desespero 100.0. Depois: HP 100, dinheiro 0, comida 0.

- **h3376 · evento#2705842 · PursuitSearch**: Mira Douran verificou a última localização conhecida sem encontrar o alvo. [ator Mira Douran (#923); alvo sem personagem identificado]

  Necessidade `protection`; prioridade 100; fato#2547184, confiança 30%, origem rumor. Ação `pursue`, score do objetivo 75.30; alternativa `avoid_threat`=22.25. Avaliação das alternativas em h3376; objetivo criado em h3372. Resultado: Busca local sem encontro; não consulta posição remota.
  Antes: HP 100, fome 62, dinheiro 10, comida 0; raiva 90.2, ressentimento 98.6, desespero 100.0. Depois: HP 100, dinheiro 10, comida 0.

Fatos do arco não exibidos neste recorte: 60. IDs integrais no catálogo.

## L21 — Fuga física — Silas Montes (#2538)

Arco **99382**; h2971→h3437; 113 fatos; 5 participantes diretos. Tipo: `causal_or_single`.

**Leitura da história:** em h2971, Karria, o primeiro registro deste recorte diz: Silas Montes roubou comida no mercado de Karria.

Este recorte não contém morte, captura, reparação, socorro, consolo ou fixação residencial. A tensão/ação registrada não deve receber um encerramento inventado.

Os elos se conectam por fonte de evento/necessidade executada; o registro da fonte demonstra a referência causal do agente, sem garantir que aquela informação seja completa ou que toda a vida esteja neste arco.

Desfechos presentes: nenhum desfecho terminal registrado.

**Limite de qualidade:** o arco contém muita repetição de agressões. Continuidade causal aparece, mas a frequência de golpes não equivale a novos objetivos ou capítulos distintos.

- **h2971 · evento#2407612 · ItemStolen**: Silas Montes roubou comida no mercado de Karria. [ator Silas Montes (#2538); alvo Karria (cidade#331)]

  Necessidade `food`; prioridade 100; origem interna `physiology`, sem fato externo de referência. Ação `steal`, score do objetivo 63.10; alternativa `forage`=50.50. Avaliação das alternativas em h2971; objetivo criado em h2967. Resultado: Alimento roubado.
  Antes: HP 100, fome 90, dinheiro 0, comida 0; raiva 95.8, ressentimento 99.3, desespero 100.0. Depois: HP 100, dinheiro 0, comida 1.

- **h2974 · evento#2409575 · ConflictStarted**: Ruan Douran iniciou confronto físico com Silas Montes. [ator Ruan Douran (#340); alvo Silas Montes (#2538)]

  Necessidade `protection`; prioridade 78.154; fato#2407612, confiança 100%, origem direct. Ação `attack`, score do objetivo 92.10; alternativa `denounce`=85.00. Avaliação das alternativas em h2974; objetivo criado em h2974. Resultado: Ataque causou 3 de dano real.
  Antes: HP 90, fome 64, dinheiro 0, comida 1; raiva 99.1, ressentimento 99.9, desespero 100.0. Depois: HP 90, dinheiro 0, comida 1.

- **h2974 · evento#2409576 · CharacterAttacked**: Ruan Douran feriu Silas Montes em 3 HP. [ator Ruan Douran (#340); alvo Silas Montes (#2538)]

  Necessidade `protection`; prioridade 78.154; fato#2407612, confiança 100%, origem direct. Ação `attack`, score do objetivo 92.10; alternativa `denounce`=85.00. Avaliação das alternativas em h2974; objetivo criado em h2974. Resultado: Ataque causou 3 de dano real.
  Antes: HP 90, fome 64, dinheiro 0, comida 1; raiva 99.1, ressentimento 99.9, desespero 100.0. Depois: HP 90, dinheiro 0, comida 1.

- **h2974 · evento#2409828 · CharacterAttacked**: Ruan Montes feriu Ruan Douran em 5 HP. [ator Ruan Montes (#2535); alvo Ruan Douran (#340)]

  Necessidade `protection`; prioridade 100; fato#2409576, confiança 100%, origem direct. Ação `attack`, score do objetivo 109.29; alternativa `denounce`=99.30. Avaliação das alternativas em h2974; objetivo criado em h2974. Resultado: Ataque causou 5 de dano real.
  Antes: HP 100, fome 63, dinheiro 1, comida 0; raiva 99.4, ressentimento 99.9, desespero 95.7. Depois: HP 100, dinheiro 1, comida 0.

- **h2975 · evento#2410570 · CharacterAttacked**: Ruan Montes feriu Ruan Douran em 4 HP. [ator Ruan Montes (#2535); alvo Ruan Douran (#340)]

  Necessidade `protection`; prioridade 100; fato#2409576, confiança 100%, origem direct. Ação `attack`, score do objetivo 134.43; alternativa `denounce`=99.30. Avaliação das alternativas em h2975; objetivo criado em h2975. Resultado: Ataque causou 4 de dano real.
  Antes: HP 100, fome 65, dinheiro 1, comida 0; raiva 99.1, ressentimento 99.9, desespero 95.8. Depois: HP 100, dinheiro 1, comida 0.

- **h2975 · evento#2410573 · CharacterAttacked**: Silas Montes feriu Ruan Douran em 4 HP. [ator Silas Montes (#2538); alvo Ruan Douran (#340)]

  Necessidade `response`; prioridade 90.054; fato#2409576, confiança 100%, origem direct. Ação `attack`, score do objetivo 120.62; alternativa `defend`=92.62. Avaliação das alternativas em h2975; objetivo criado em h2975. Resultado: Ataque causou 4 de dano real.
  Antes: HP 97, fome 58, dinheiro 0, comida 0; raiva 99.1, ressentimento 99.9, desespero 100.0. Depois: HP 97, dinheiro 0, comida 0.

- **h3301 · evento#2650249 · CharacterAttacked**: Ruan Valerius feriu Ruan Montes em 8 HP. [ator Ruan Valerius (#343); alvo Ruan Montes (#2535)]

  Necessidade `response`; prioridade 88.49800000000005; fato#2415206, confiança 30%, origem rumor. Ação `attack`, score do objetivo 126.62; alternativa `defend`=86.05. Avaliação das alternativas em h3301; objetivo criado em h3301. Resultado: Ataque causou 8 de dano real.
  Antes: HP 100, fome 66, dinheiro 10, comida 0; raiva 66.0, ressentimento 99.0, desespero 3.3. Depois: HP 100, dinheiro 10, comida 0.

- **h3310 · evento#2657076 · PursuitSearch**: Ruan Montes verificou a última localização conhecida sem encontrar o alvo. [ator Ruan Montes (#2535); alvo sem personagem identificado]

  Necessidade `response`; prioridade 92.38; fato#2650249, confiança 100%, origem direct. Ação `pursue`, score do objetivo 80.80. Avaliação das alternativas em h3310; objetivo criado em h3306. Resultado: Busca local sem encontro; não consulta posição remota.
  Antes: HP 18, fome 55, dinheiro 0, comida 0; raiva 97.0, ressentimento 99.6, desespero 100.0. Depois: HP 18, dinheiro 0, comida 0.

- **h3419 · evento#2737997 · ThreatAvoided**: Mira Montes buscou um local seguro conhecido. [ator Mira Montes (#2532); alvo sem personagem identificado]

  Necessidade `protection`; prioridade 100; fato#2650249, confiança 60%, origem known. Ação `avoid_threat`, score do objetivo 1.40; alternativa `pursue`=74.00. Avaliação das alternativas em h3419; objetivo criado em h3414. Resultado: Afastou-se do local da ameaça.
  Antes: HP 28, fome 70, dinheiro 1, comida 0; raiva 97.6, ressentimento 99.7, desespero 69.9. Depois: HP 28, dinheiro 1, comida 0.

- **h3437 · evento#2750995 · PursuitSearch**: Mira Montes verificou a última localização conhecida sem encontrar o alvo. [ator Mira Montes (#2532); alvo sem personagem identificado]

  Necessidade `protection`; prioridade 100; fato#2645272, confiança 60%, origem known. Ação `pursue`, score do objetivo 82.00; alternativa `avoid_threat`=1.40. Avaliação das alternativas em h3437; objetivo criado em h3437. Resultado: Busca local sem encontro; não consulta posição remota.
  Antes: HP 28, fome 66, dinheiro 1, comida 0; raiva 96.8, ressentimento 99.5, desespero 74.9. Depois: HP 28, dinheiro 1, comida 0.

Fatos do arco não exibidos neste recorte: 103. IDs integrais no catálogo.

## L22 — Retirada — Silas Arven (#1620)

Arco **130638**; h4038→h4366; 48 fatos; 5 participantes diretos. Tipo: `causal_or_single`.

**Leitura da história:** em h4038, Dormir, o primeiro registro deste recorte diz: Silas Arven roubou comida no mercado de Dormir.

Entre as consequências registradas: Darin Stone deteve Iria Montes e cobrou 5 moedas. O último fato disponível neste recorte ocorreu em h4366; isso não implica que a disputa tenha terminado definitivamente.

Os elos se conectam por fonte de evento/necessidade executada; o registro da fonte demonstra a referência causal do agente, sem garantir que aquela informação seja completa ou que toda a vida esteja neste arco.

Desfechos presentes: CharacterCaptured: 1.

- **h4038 · evento#3182166 · ItemStolen**: Silas Arven roubou comida no mercado de Dormir. [ator Silas Arven (#1620); alvo Dormir (cidade#1661)]

  Necessidade `food`; prioridade 100; origem interna `physiology`, sem fato externo de referência. Ação `steal`, score do objetivo 75.03; alternativa `forage`=70.00. Avaliação das alternativas em h4038; objetivo criado em h4036. Resultado: Alimento roubado.
  Antes: HP 100, fome 86, dinheiro 0, comida 0; raiva 95.3, ressentimento 99.2, desespero 100.0. Depois: HP 100, dinheiro 0, comida 1.

- **h4038 · evento#3182168 · WantedIssued**: Iria Montes registrou procura por Silas Arven. [ator Iria Montes (#1673); alvo Dormir (cidade#1661)]
- **h4039 · evento#3182879 · GuardResponded**: Iria Montes interveio no roubo e cobrou 0 moedas de Silas Arven. [ator Iria Montes (#1673); alvo Silas Arven (#1620)]

  Necessidade `security`; prioridade 88.65; fato#3182166, confiança 100%, origem direct. Ação `secure`, score do objetivo 98.33. Avaliação das alternativas em h4039; objetivo criado em h4039. Resultado: Suspeito encontrado; intervenção registrada.
  Antes: HP 48, fome 48, dinheiro 3, comida 0; raiva 61.2, ressentimento 98.7, desespero 70.3. Depois: HP 48, dinheiro 3, comida 0.

- **h4214 · evento#3305725 · CharacterAttacked**: Iria Montes feriu Darin Stone em 9 HP. [ator Iria Montes (#1673); alvo Darin Stone (#5464)]

  Necessidade `protection`; prioridade 76.22200000000001; fato#3252678, confiança 30%, origem rumor. Ação `attack`, score do objetivo 97.13; alternativa `denounce`=94.65. Avaliação das alternativas em h4214; objetivo criado em h4214. Resultado: Ataque causou 9 de dano real.
  Antes: HP 89, fome 38, dinheiro 8, comida 1; raiva 98.8, ressentimento 99.8, desespero 100.0. Depois: HP 89, dinheiro 8, comida 1.

- **h4223 · evento#3312475 · CharacterAttacked**: Darin Stone feriu Iria Montes em 15 HP. [ator Darin Stone (#5464); alvo Iria Montes (#1673)]

  Necessidade `response`; prioridade 91.03; fato#3305725, confiança 100%, origem direct. Ação `attack`, score do objetivo 77.66; alternativa `defend`=78.34. Avaliação das alternativas em h4223; objetivo criado em h4223. Resultado: Ataque causou 15 de dano real.
  Antes: HP 91, fome 50, dinheiro 6, comida 1; raiva 97.0, ressentimento 99.6, desespero 75.4. Depois: HP 91, dinheiro 6, comida 1.

- **h4224 · evento#3312756 · CharacterAttacked**: Iria Montes feriu Darin Stone em 6 HP. [ator Iria Montes (#1673); alvo Darin Stone (#5464)]

  Necessidade `response`; prioridade 91.468; fato#3312475, confiança 100%, origem direct. Ação `attack`, score do objetivo 121.24; alternativa `defend`=95.46. Avaliação das alternativas em h4224; objetivo criado em h4224. Resultado: Ataque causou 6 de dano real.
  Antes: HP 74, fome 58, dinheiro 7, comida 3; raiva 99.7, ressentimento 100.0, desespero 100.0. Depois: HP 74, dinheiro 7, comida 3.

- **h4224 · evento#3313324 · CharacterAttacked**: Darin Stone feriu Iria Montes em 13 HP. [ator Darin Stone (#5464); alvo Iria Montes (#1673)]

  Necessidade `response`; prioridade 91.468; fato#3312756, confiança 100%, origem direct. Ação `attack`, score do objetivo 79.25; alternativa `defend`=77.62. Avaliação das alternativas em h4224; objetivo criado em h4224. Resultado: Ataque causou 13 de dano real.
  Antes: HP 85, fome 52, dinheiro 6, comida 1; raiva 99.7, ressentimento 100.0, desespero 75.5. Depois: HP 85, dinheiro 6, comida 1.

- **h4364 · evento#3412253 · ConflictStarted**: Darin Stone iniciou confronto físico com Iria Montes. [ator Darin Stone (#5464); alvo Iria Montes (#1673)]

  Necessidade `pursuit`; prioridade 82.0; fato#3305725 fora da memória curta amostrada; necessidade/caso pode conservar referência própria. Ação `attack`, score do objetivo 56.37; alternativa `withdraw`=52.69. Avaliação das alternativas em h4364; objetivo criado em h4364. Resultado: Ataque causou 12 de dano real.
  Antes: HP 79, fome 52, dinheiro 2, comida 0; raiva 98.7, ressentimento 99.8, desespero 100.0. Depois: HP 79, dinheiro 2, comida 0.

- **h4364 · evento#3412254 · CharacterAttacked**: Darin Stone feriu Iria Montes em 12 HP. [ator Darin Stone (#5464); alvo Iria Montes (#1673)]

  Necessidade `pursuit`; prioridade 82.0; fato#3305725 fora da memória curta amostrada; necessidade/caso pode conservar referência própria. Ação `attack`, score do objetivo 56.37; alternativa `withdraw`=52.69. Avaliação das alternativas em h4364; objetivo criado em h4364. Resultado: Ataque causou 12 de dano real.
  Antes: HP 79, fome 52, dinheiro 2, comida 0; raiva 98.7, ressentimento 99.8, desespero 100.0. Depois: HP 79, dinheiro 2, comida 0.

- **h4365 · evento#3412886 · CharacterAttacked**: Darin Stone feriu Iria Montes em 12 HP. [ator Darin Stone (#5464); alvo Iria Montes (#1673)]

  Necessidade `pursuit`; prioridade 82.0; fato#3305725 fora da memória curta amostrada; necessidade/caso pode conservar referência própria. Ação `attack`, score do objetivo 77.88; alternativa `defend`=78.16. Avaliação das alternativas em h4365; objetivo criado em h4365. Resultado: Ataque causou 12 de dano real.
  Antes: HP 79, fome 54, dinheiro 2, comida 0; raiva 98.4, ressentimento 99.8, desespero 100.0. Depois: HP 79, dinheiro 2, comida 0.

- **h4366 · evento#3413513 · CharacterCaptured**: Darin Stone deteve Iria Montes e cobrou 5 moedas. [ator Darin Stone (#5464); alvo Iria Montes (#1673)]

  Necessidade `pursuit`; prioridade 82.0; fato#3305725 fora da memória curta amostrada; necessidade/caso pode conservar referência própria. Ação `capture`, score do objetivo 126.55. Avaliação das alternativas em h4366; objetivo criado em h4366. Resultado: Captura e detenção temporária registradas.
  Antes: HP 79, fome 56, dinheiro 2, comida 0; raiva 99.7, ressentimento 100.0, desespero 100.0. Depois: HP 79, dinheiro 2, comida 0.

Fatos do arco não exibidos neste recorte: 37. IDs integrais no catálogo.

## L23 — Retirada — Silas Solaris (#5462)

Arco **24582**; h719→h1014; 118 fatos; 6 participantes diretos. Tipo: `causal_or_single`.

**Leitura da história:** em h719, Dormir, o primeiro registro deste recorte diz: Silas Solaris roubou comida no mercado de Dormir.

Este recorte não contém morte, captura, reparação, socorro, consolo ou fixação residencial. A tensão/ação registrada não deve receber um encerramento inventado.

Os elos se conectam por fonte de evento/necessidade executada; o registro da fonte demonstra a referência causal do agente, sem garantir que aquela informação seja completa ou que toda a vida esteja neste arco.

Desfechos presentes: nenhum desfecho terminal registrado.

**Limite de qualidade:** o arco contém muita repetição de agressões. Continuidade causal aparece, mas a frequência de golpes não equivale a novos objetivos ou capítulos distintos.

- **h719 · evento#615262 · ItemStolen**: Silas Solaris roubou comida no mercado de Dormir. [ator Silas Solaris (#5462); alvo Dormir (cidade#1661)]

  Necessidade `food`; prioridade 100; origem interna `physiology`, sem fato externo de referência. Ação `steal`, score do objetivo 65.10; alternativa `work`=56.00. Avaliação das alternativas em h719; objetivo criado em h715. Resultado: Alimento roubado.
  Antes: HP 24, fome 90, dinheiro 1, comida 0; raiva 95.6, ressentimento 99.2, desespero 74.1. Depois: HP 24, dinheiro 1, comida 1.

- **h720 · evento#616226 · ConflictStarted**: Marie Valerius iniciou confronto físico com Silas Solaris. [ator Marie Valerius (#5358); alvo Silas Solaris (#5462)]

  Necessidade `protection`; prioridade 71.64; fato#615262, confiança 100%, origem direct. Ação `attack`, score do objetivo 89.36; alternativa `defend`=90.70. Avaliação das alternativas em h720; objetivo criado em h720. Resultado: Ataque causou 3 de dano real.
  Antes: HP 46, fome 34, dinheiro 17, comida 0; raiva 98.5, ressentimento 99.8, desespero 91.0. Depois: HP 46, dinheiro 17, comida 0.

- **h720 · evento#616227 · CharacterAttacked**: Marie Valerius feriu Silas Solaris em 3 HP. [ator Marie Valerius (#5358); alvo Silas Solaris (#5462)]

  Necessidade `protection`; prioridade 71.64; fato#615262, confiança 100%, origem direct. Ação `attack`, score do objetivo 89.36; alternativa `defend`=90.70. Avaliação das alternativas em h720; objetivo criado em h720. Resultado: Ataque causou 3 de dano real.
  Antes: HP 46, fome 34, dinheiro 17, comida 0; raiva 98.5, ressentimento 99.8, desespero 91.0. Depois: HP 46, dinheiro 17, comida 0.

- **h761 · evento#650859 · CharacterAttacked**: Iria Montes feriu Marie Valerius em 3 HP. [ator Iria Montes (#1673); alvo Marie Valerius (#5358)]

  Necessidade `protection`; prioridade 100; fato#616227, confiança 100%, origem direct. Ação `attack`, score do objetivo 97.83; alternativa `denounce`=95.65. Avaliação das alternativas em h761; objetivo criado em h761. Resultado: Ataque causou 3 de dano real.
  Antes: HP 39, fome 62, dinheiro 0, comida 0; raiva 99.5, ressentimento 99.9, desespero 85.3. Depois: HP 39, dinheiro 0, comida 0.

- **h762 · evento#651690 · CharacterAttacked**: Iria Montes feriu Darin Stone em 3 HP. [ator Iria Montes (#1673); alvo Darin Stone (#5464)]

  Necessidade `protection`; prioridade 100; fato#616227, confiança 100%, origem direct. Ação `attack`, score do objetivo 122.88; alternativa `denounce`=95.65. Avaliação das alternativas em h762; objetivo criado em h762. Resultado: Ataque causou 3 de dano real.
  Antes: HP 39, fome 64, dinheiro 0, comida 0; raiva 99.2, ressentimento 99.9, desespero 85.4. Depois: HP 39, dinheiro 0, comida 0.

- **h763 · evento#652529 · CharacterAttacked**: Iria Montes feriu Darin Stone em 2 HP. [ator Iria Montes (#1673); alvo Darin Stone (#5464)]

  Necessidade `protection`; prioridade 100; fato#616227, confiança 100%, origem direct. Ação `attack`, score do objetivo 120.07; alternativa `denounce`=95.65. Avaliação das alternativas em h763; objetivo criado em h763. Resultado: Ataque causou 2 de dano real.
  Antes: HP 39, fome 66, dinheiro 0, comida 0; raiva 98.9, ressentimento 99.8, desespero 85.6. Depois: HP 39, dinheiro 0, comida 0.

- **h960 · evento#820956 · CharacterFled**: Darin Stone afastou-se do confronto. [ator Darin Stone (#5470); alvo sem personagem identificado]

  Necessidade `protection`; prioridade 100; fato#819507, confiança 100%, origem direct. Ação `flee`, score do objetivo 101.82; alternativa `surrender`=74.22. Avaliação das alternativas em h960; objetivo criado em h960. Resultado: Afastamento físico realizado; o conflito social pode continuar.
  Antes: HP 87, fome 54, dinheiro 0, comida 0; raiva 99.5, ressentimento 99.9, desespero 67.0. Depois: HP 87, dinheiro 0, comida 0.

- **h981 · evento#839069 · ThreatReported**: Silas Solaris denunciou um acontecimento conhecido a Darin Stone. [ator Silas Solaris (#5462); alvo Darin Stone (#5464)]
- **h1014 · evento#867060 · ConflictEnded**: O confronto de Darin Stone terminou: flee. [ator Darin Stone (#5464); alvo Iria Montes (#1673)]

  Necessidade `pursuit`; prioridade 82.0; fato#817888 fora da memória curta amostrada; necessidade/caso pode conservar referência própria. Ação `flee`, score do objetivo 62.07; alternativa `withdraw`=55.36. Avaliação das alternativas em h1014; objetivo criado em h1014. Resultado: Afastamento físico realizado; o conflito social pode continuar.
  Antes: HP 57, fome 72, dinheiro 5, comida 0; raiva 95.9, ressentimento 99.4, desespero 100.0. Depois: HP 57, dinheiro 5, comida 0.

- **h1014 · evento#867061 · CharacterFled**: Darin Stone afastou-se do confronto. [ator Darin Stone (#5464); alvo sem personagem identificado]

  Necessidade `pursuit`; prioridade 82.0; fato#817888 fora da memória curta amostrada; necessidade/caso pode conservar referência própria. Ação `flee`, score do objetivo 62.07; alternativa `withdraw`=55.36. Avaliação das alternativas em h1014; objetivo criado em h1014. Resultado: Afastamento físico realizado; o conflito social pode continuar.
  Antes: HP 57, fome 72, dinheiro 5, comida 0; raiva 95.9, ressentimento 99.4, desespero 100.0. Depois: HP 57, dinheiro 5, comida 0.

Fatos do arco não exibidos neste recorte: 108. IDs integrais no catálogo.

## L24 — Apoio após perda — Bela Douran (#3139)

Arco **6101**; h173→h173; 1 fatos; 2 participantes diretos. Tipo: `causal_or_single`.

**Leitura da história:** em h173, Arvia, o primeiro registro deste recorte diz: Bela Douran ouviu Arthus Hammer durante seu luto.

Entre as consequências registradas: Bela Douran ouviu Arthus Hammer durante seu luto. O último fato disponível neste recorte ocorreu em h173; isso não implica que a disputa tenha terminado definitivamente.

Os elos se conectam por fonte de evento/necessidade executada; o registro da fonte demonstra a referência causal do agente, sem garantir que aquela informação seja completa ou que toda a vida esteja neste arco.

Desfechos presentes: ComfortGiven: 1.

- **h173 · evento#140210 · ComfortGiven**: Bela Douran ouviu Arthus Hammer durante seu luto. [ator Bela Douran (#3139); alvo Arthus Hammer (#3137)]
Fatos do arco não exibidos neste recorte: 0. IDs integrais no catálogo.

## L25 — Apoio após perda — Nora Douran (#3088)

Arco **20463**; h591→h591; 1 fatos; 2 participantes diretos. Tipo: `causal_or_single`.

**Leitura da história:** em h591, Arvia, o primeiro registro deste recorte diz: Nora Douran ouviu Cael Ferros durante seu luto.

Entre as consequências registradas: Nora Douran ouviu Cael Ferros durante seu luto. O último fato disponível neste recorte ocorreu em h591; isso não implica que a disputa tenha terminado definitivamente.

Os elos se conectam por fonte de evento/necessidade executada; o registro da fonte demonstra a referência causal do agente, sem garantir que aquela informação seja completa ou que toda a vida esteja neste arco.

Desfechos presentes: ComfortGiven: 1.

- **h591 · evento#506440 · ComfortGiven**: Nora Douran ouviu Cael Ferros durante seu luto. [ator Nora Douran (#3088); alvo Cael Ferros (#3076)]
Fatos do arco não exibidos neste recorte: 0. IDs integrais no catálogo.

## L26 — Morte e sucessão política — Nora Arven (#1091)

Arco **23468**; h691→h691; 2 fatos; 2 participantes diretos. Tipo: `causal_or_single`.

**Leitura da história:** em h691, Silmar, o primeiro registro deste recorte diz: Marie Arven morreu por privação.

Entre as consequências registradas: Marie Arven morreu por privação. Nora Arven assumiu Reino Arven. O último fato disponível neste recorte ocorreu em h691; isso não implica que a disputa tenha terminado definitivamente.

Os elos se conectam por fonte de evento/necessidade executada; o registro da fonte demonstra a referência causal do agente, sem garantir que aquela informação seja completa ou que toda a vida esteja neste arco.

Desfechos presentes: CharacterDied: 1, SuccessionChanged: 1.

- **h691 · evento#590441 · CharacterDied**: Marie Arven morreu por privação. [ator sem personagem identificado; alvo Marie Arven (#1088)]
- **h691 · evento#590442 · SuccessionChanged**: Nora Arven assumiu Reino Arven. [ator Nora Arven (#1091); alvo Reino Arven (reino#881)]
Fatos do arco não exibidos neste recorte: 0. IDs integrais no catálogo.

## L27 — Morte e sucessão política

Arco **24621**; h721→h721; 2 fatos; 1 participantes diretos. Tipo: `causal_or_single`.

**Leitura da história:** em h721, Silmar, o primeiro registro deste recorte diz: Nora Arven morreu por privação.

Entre as consequências registradas: Nora Arven morreu por privação. A dinastia de Reino Arven foi extinta; o território permanece em crise sucessória. O último fato disponível neste recorte ocorreu em h721; isso não implica que a disputa tenha terminado definitivamente.

Os elos se conectam por fonte de evento/necessidade executada; o registro da fonte demonstra a referência causal do agente, sem garantir que aquela informação seja completa ou que toda a vida esteja neste arco.

Desfechos presentes: CharacterDied: 1, SuccessionChanged: 1.

- **h721 · evento#616279 · CharacterDied**: Nora Arven morreu por privação. [ator sem personagem identificado; alvo Nora Arven (#1091)]
- **h721 · evento#616280 · SuccessionChanged**: A dinastia de Reino Arven foi extinta; o território permanece em crise sucessória. [ator sem personagem identificado; alvo Reino Arven (reino#881)]
Fatos do arco não exibidos neste recorte: 0. IDs integrais no catálogo.

## L28 — Descoberta de restos e conhecimento tardio — Tomas Kars (#4693)

Arco **59361**; h1704→h1854; 3 fatos; 2 participantes diretos. Tipo: `causal_or_single`.

**Leitura da história:** em h1704, Silvia, o primeiro registro deste recorte diz: Tomas Kars não localiza um familiar há 172 horas.

Este recorte não contém morte, captura, reparação, socorro, consolo ou fixação residencial. A tensão/ação registrada não deve receber um encerramento inventado.

Os elos se conectam por fonte de evento/necessidade executada; o registro da fonte demonstra a referência causal do agente, sem garantir que aquela informação seja completa ou que toda a vida esteja neste arco.

Desfechos presentes: nenhum desfecho terminal registrado.

- **h1704 · evento#1431477 · AbsenceNoticed**: Tomas Kars não localiza um familiar há 172 horas. [ator Tomas Kars (#4693); alvo sem personagem identificado]
- **h1710 · evento#1436254 · RemainsLocated**: Tomas Kars identificou os restos de Mira Kars. [ator Tomas Kars (#4693); alvo Mira Kars (#4698)]

  Necessidade `family`; prioridade 83.66666666666667; fato#1431477, confiança 100%, origem direct. Ação `check_relative`, score do objetivo 90.50. Avaliação das alternativas em h1710; objetivo criado em h1710. Resultado: Morte confirmada no local; o fato pode ser informado.
  Antes: HP 64, fome 62, dinheiro 0, comida 1; raiva 70.4, ressentimento 100.0, desespero 100.0. Depois: HP 64, dinheiro 0, comida 1.

- **h1854 · evento#1551101 · Remembrance**: Tomas Kars dedicou um momento à memória de uma pessoa próxima. [ator Tomas Kars (#4693); alvo sem personagem identificado]

  Necessidade `grief`; prioridade 75.6; fato#1436254 fora da memória curta amostrada; necessidade/caso pode conservar referência própria. Ação `remember_relative`, score do objetivo 55.00; alternativa `seek_company`=38.10. Avaliação das alternativas em h1854; objetivo criado em h1852. Resultado: Visitou um local relacionado à perda.
  Antes: HP 93, fome 70, dinheiro 0, comida 1; raiva 99.7, ressentimento 100.0, desespero 100.0. Depois: HP 93, dinheiro 0, comida 1.

Fatos do arco não exibidos neste recorte: 0. IDs integrais no catálogo.

## L29 — Descoberta de restos e conhecimento tardio — Lyra Ferros (#2961)

Arco **134267**; h4172→h4322; 3 fatos; 2 participantes diretos. Tipo: `causal_or_single`.

**Leitura da história:** em h4172, Morria, o primeiro registro deste recorte diz: Lyra Ferros não localiza um familiar há 218 horas.

Este recorte não contém morte, captura, reparação, socorro, consolo ou fixação residencial. A tensão/ação registrada não deve receber um encerramento inventado.

Os elos se conectam por fonte de evento/necessidade executada; o registro da fonte demonstra a referência causal do agente, sem garantir que aquela informação seja completa ou que toda a vida esteja neste arco.

Desfechos presentes: nenhum desfecho terminal registrado.

- **h4172 · evento#3276360 · AbsenceNoticed**: Lyra Ferros não localiza um familiar há 218 horas. [ator Lyra Ferros (#2961); alvo sem personagem identificado]
- **h4232 · evento#3319248 · RemainsLocated**: Lyra Ferros identificou os restos de Lyra Ferros. [ator Lyra Ferros (#2961); alvo Lyra Ferros (#2964)]

  Necessidade `family`; prioridade 87.2; fato#3276360, confiança 100%, origem direct. Ação `check_relative`, score do objetivo 69.50. Avaliação das alternativas em h4232; objetivo criado em h4232. Resultado: Morte confirmada no local; o fato pode ser informado.
  Antes: HP 100, fome 76, dinheiro 1, comida 0; raiva 0.0, ressentimento 56.2, desespero 100.0. Depois: HP 100, dinheiro 1, comida 0.

- **h4322 · evento#3382768 · Remembrance**: Lyra Ferros dedicou um momento à memória de uma pessoa próxima. [ator Lyra Ferros (#2961); alvo sem personagem identificado]

  Necessidade `grief`; prioridade 75.9; fato#3319248 fora da memória curta amostrada; necessidade/caso pode conservar referência própria. Ação `remember_relative`, score do objetivo 56.20. Avaliação das alternativas em h4322; objetivo criado em h4316. Resultado: Visitou um local relacionado à perda.
  Antes: HP 100, fome 56, dinheiro 1, comida 0; raiva 0.0, ressentimento 52.6, desespero 100.0. Depois: HP 100, dinheiro 1, comida 0.

Fatos do arco não exibidos neste recorte: 0. IDs integrais no catálogo.

## L30 — Crime por avanço financeiro — Cael Hammer (#5331)

Arco **59**; h2→h136; 21 fatos; 7 participantes diretos. Tipo: `causal_or_single`.

**Leitura da história:** em h2, Dormar, o primeiro registro deste recorte diz: Cael Hammer roubou provisão de Bela Vale.

Entre as consequências registradas: Cael Hammer: apologize diante de Ruan Vale. Iria Bruma: apologize diante de Ruan Vale. Iria Bruma: apologize diante de Bela Vale. O último fato disponível neste recorte ocorreu em h136; isso não implica que a disputa tenha terminado definitivamente.

Os elos se conectam por fonte de evento/necessidade executada; o registro da fonte demonstra a referência causal do agente, sem garantir que aquela informação seja completa ou que toda a vida esteja neste arco.

Desfechos presentes: ApologyGiven: 5.

- **h2 · evento#7853 · ItemStolen**: Cael Hammer roubou provisão de Bela Vale. [ator Cael Hammer (#5331); alvo Bela Vale (#5323)]

  Necessidade `advancement`; prioridade 37.5; origem interna `self_assessment:2`, sem fato externo de referência. Ação `steal_person`, score do objetivo 89.60; alternativa `work`=61.50. Avaliação das alternativas em h2; objetivo criado em h2. Resultado: Provisão real roubada.
  Antes: HP 100, fome 26, dinheiro 28, comida 1; raiva 0.0, ressentimento 0.0, desespero 0.0. Depois: HP 100, dinheiro 28, comida 2.

- **h3 · evento#8603 · PersonLocated**: Ruan Vale localizou Cael Hammer. [ator Ruan Vale (#5320); alvo Cael Hammer (#5331)]

  Necessidade `revenge`; prioridade 70.809; fato#7853, confiança 100%, origem direct. Ação `investigate`, score do objetivo 98.60; alternativa `demand_return`=56.60. Avaliação das alternativas em h3; objetivo criado em h3. Resultado: Investigou o local conhecido; não houve confronto.
  Antes: HP 100, fome 56, dinheiro 16, comida 2; raiva 17.1, ressentimento 9.8, desespero 0.0. Depois: HP 100, dinheiro 16, comida 2.

- **h3 · evento#8604 · InvestigationPerformed**: Ruan Vale verificou o último local conhecido do responsável. [ator Ruan Vale (#5320); alvo sem personagem identificado]

  Necessidade `revenge`; prioridade 70.809; fato#7853, confiança 100%, origem direct. Ação `investigate`, score do objetivo 98.60; alternativa `demand_return`=56.60. Avaliação das alternativas em h3; objetivo criado em h3. Resultado: Investigou o local conhecido; não houve confronto.
  Antes: HP 100, fome 56, dinheiro 16, comida 2; raiva 17.1, ressentimento 9.8, desespero 0.0. Depois: HP 100, dinheiro 16, comida 2.

- **h4 · evento#9522 · ApologyGiven**: Arthus Hammer: apologize diante de Bela Vale. [ator Arthus Hammer (#5328); alvo Bela Vale (#5323)]

  Necessidade `protection`; prioridade 58.9; fato#9516, confiança 100%, origem direct. Ação `apologize`, score do objetivo 71.50; alternativa `protect`=68.50. Avaliação das alternativas em h4; objetivo criado em h4. Resultado: Interação estruturada registrada: apologize.
  Antes: HP 100, fome 22, dinheiro 18, comida 1; raiva 0.0, ressentimento 0.0, desespero 0.0. Depois: HP 100, dinheiro 18, comida 1.

- **h5 · evento#10447 · ApologyGiven**: Bela Vale: apologize diante de Cael Hammer. [ator Bela Vale (#5323); alvo Cael Hammer (#5331)]

  Necessidade `protection`; prioridade 59.75; fato#7853, confiança 100%, origem direct. Ação `apologize`, score do objetivo 57.75; alternativa `defend`=54.87. Avaliação das alternativas em h5; objetivo criado em h5. Resultado: Interação estruturada registrada: apologize.
  Antes: HP 100, fome 21, dinheiro 19, comida 0; raiva 0.0, ressentimento 0.0, desespero 0.0. Depois: HP 100, dinheiro 19, comida 0.

- **h7 · evento#12209 · ApologyGiven**: Cael Hammer: apologize diante de Ruan Vale. [ator Cael Hammer (#5331); alvo Ruan Vale (#5320)]

  Necessidade `response`; prioridade 50.45; fato#9512, confiança 100%, origem direct. Ação `apologize`, score do objetivo 67.75; alternativa `return_stolen`=66.10. Avaliação das alternativas em h7; objetivo criado em h7. Resultado: Interação estruturada registrada: apologize.
  Antes: HP 100, fome 36, dinheiro 28, comida 2; raiva 0.0, ressentimento 0.0, desespero 0.0. Depois: HP 100, dinheiro 28, comida 2.

- **h22 · evento#28536 · ApologyGiven**: Iria Bruma: apologize diante de Ruan Vale. [ator Iria Bruma (#1608); alvo Ruan Vale (#5320)]

  Necessidade `protection`; prioridade 64.6; fato#9512, confiança 30%, origem rumor. Ação `apologize`, score do objetivo 80.00; alternativa `denounce`=75.00. Avaliação das alternativas em h22; objetivo criado em h22. Resultado: Interação estruturada registrada: apologize.
  Antes: HP 100, fome 54, dinheiro 6, comida 1; raiva 0.0, ressentimento 0.0, desespero 0.0. Depois: HP 100, dinheiro 6, comida 1.

- **h83 · evento#67631 · ApologyGiven**: Iria Bruma: apologize diante de Bela Vale. [ator Iria Bruma (#1608); alvo Bela Vale (#5323)]

  Necessidade `protection`; prioridade 65.65; fato#9516, confiança 30%, origem rumor. Ação `apologize`, score do objetivo 80.00; alternativa `denounce`=75.00. Avaliação das alternativas em h83; objetivo criado em h83. Resultado: Interação estruturada registrada: apologize.
  Antes: HP 100, fome 56, dinheiro 7, comida 1; raiva 0.0, ressentimento 0.0, desespero 9.4. Depois: HP 100, dinheiro 7, comida 1.

- **h83 · evento#67632 · ConflictEnded**: O confronto de Iria Bruma terminou: apologize. [ator Iria Bruma (#1608); alvo Bela Vale (#5323)]

  Necessidade `protection`; prioridade 65.65; fato#9516, confiança 30%, origem rumor. Ação `apologize`, score do objetivo 80.00; alternativa `denounce`=75.00. Avaliação das alternativas em h83; objetivo criado em h83. Resultado: Interação estruturada registrada: apologize.
  Antes: HP 100, fome 56, dinheiro 7, comida 1; raiva 0.0, ressentimento 0.0, desespero 9.4. Depois: HP 100, dinheiro 7, comida 1.

- **h98 · evento#80224 · InformationShared**: Iria Solaris informou Silas Arven: Ruan Vale: demand_return diante de Cael Hammer. [ator Iria Solaris (#5279); alvo Silas Arven (#5256)]

  Necessidade `protection`; prioridade 62.8; fato#9512, confiança 30%, origem rumor. Ação `denounce`, score do objetivo 84.40; alternativa `ask_personal_help`=48.05. Avaliação das alternativas em h98; objetivo criado em h98. Resultado: Informação transmitida.
  Antes: HP 100, fome 46, dinheiro 21, comida 1; raiva 0.0, ressentimento 0.0, desespero 0.0. Depois: HP 100, dinheiro 21, comida 1.

- **h98 · evento#80225 · ThreatReported**: Iria Solaris denunciou um acontecimento conhecido a Silas Arven. [ator Iria Solaris (#5279); alvo Silas Arven (#5256)]

  Necessidade `protection`; prioridade 62.8; fato#9512, confiança 30%, origem rumor. Ação `denounce`, score do objetivo 84.40; alternativa `ask_personal_help`=48.05. Avaliação das alternativas em h98; objetivo criado em h98. Resultado: Informação transmitida.
  Antes: HP 100, fome 46, dinheiro 21, comida 1; raiva 0.0, ressentimento 0.0, desespero 0.0. Depois: HP 100, dinheiro 21, comida 1.

- **h136 · evento#109066 · ThreatAvoided**: Silas Arven buscou um local seguro conhecido. [ator Silas Arven (#5256); alvo sem personagem identificado]

  Necessidade `protection`; prioridade 67.50200000000001; fato#9512 fora da memória curta amostrada; necessidade/caso pode conservar referência própria. Ação `avoid_threat`, score do objetivo 10.80. Avaliação das alternativas em h136; objetivo criado em h136. Resultado: Afastou-se do local da ameaça.
  Antes: HP 100, fome 44, dinheiro 21, comida 1; raiva 18.3, ressentimento 17.4, desespero 0.0. Depois: HP 100, dinheiro 21, comida 1.

Fatos do arco não exibidos neste recorte: 9. IDs integrais no catálogo.

## L31 — Crime por avanço financeiro — Cael Hammer (#5331)

Arco **589**; h26→h31; 8 fatos; 4 participantes diretos. Tipo: `causal_or_single`.

**Leitura da história:** em h26, Elivia, o primeiro registro deste recorte diz: Cael Hammer roubou provisão de Elena Vale.

Este recorte não contém morte, captura, reparação, socorro, consolo ou fixação residencial. A tensão/ação registrada não deve receber um encerramento inventado.

Os elos se conectam por fonte de evento/necessidade executada; o registro da fonte demonstra a referência causal do agente, sem garantir que aquela informação seja completa ou que toda a vida esteja neste arco.

Desfechos presentes: nenhum desfecho terminal registrado.

- **h26 · evento#32235 · ItemStolen**: Cael Hammer roubou provisão de Elena Vale. [ator Cael Hammer (#5331); alvo Elena Vale (#1588)]

  Necessidade `advancement`; prioridade 41.1; origem interna `self_assessment:2`, sem fato externo de referência. Ação `steal_person`, score do objetivo 69.60. Avaliação das alternativas em h26; objetivo criado em h26. Resultado: Provisão real roubada.
  Antes: HP 100, fome 34, dinheiro 28, comida 1; raiva 0.0, ressentimento 0.0, desespero 0.0. Depois: HP 100, dinheiro 28, comida 2.

- **h26 · evento#32239 · WantedIssued**: Bela Kars registrou procura por Cael Hammer. [ator Bela Kars (#5302); alvo Elivia (cidade#1567)]
- **h27 · evento#32379 · ThreatReported**: Mira Ferros denunciou um acontecimento conhecido a Bela Kars. [ator Mira Ferros (#1582); alvo Bela Kars (#5302)]

  Necessidade `protection`; prioridade 56.35; fato#32235, confiança 100%, origem direct. Ação `denounce`, score do objetivo 78.45; alternativa `demand_return`=71.25. Avaliação das alternativas em h27; objetivo criado em h27. Resultado: Denúncia registrada por autoridade que já conhece o fato.
  Antes: HP 100, fome 31, dinheiro 15, comida 1; raiva 0.0, ressentimento 0.0, desespero 0.0. Depois: HP 100, dinheiro 15, comida 1.

- **h27 · evento#32793 · ConflictEnded**: O confronto de Cael Hammer terminou: flee. [ator Cael Hammer (#5331); alvo Bela Kars (#5302)]

  Necessidade `response`; prioridade 55.15; fato#32239, confiança 100%, origem direct. Ação `flee`, score do objetivo 96.43; alternativa `defend`=62.36. Avaliação das alternativas em h27; objetivo criado em h27. Resultado: Afastamento físico realizado; o conflito social pode continuar.
  Antes: HP 100, fome 36, dinheiro 23, comida 2; raiva 0.0, ressentimento 0.0, desespero 0.0. Depois: HP 100, dinheiro 23, comida 2.

- **h27 · evento#32794 · CharacterFled**: Cael Hammer afastou-se do confronto. [ator Cael Hammer (#5331); alvo sem personagem identificado]

  Necessidade `response`; prioridade 55.15; fato#32239, confiança 100%, origem direct. Ação `flee`, score do objetivo 96.43; alternativa `defend`=62.36. Avaliação das alternativas em h27; objetivo criado em h27. Resultado: Afastamento físico realizado; o conflito social pode continuar.
  Antes: HP 100, fome 36, dinheiro 23, comida 2; raiva 0.0, ressentimento 0.0, desespero 0.0. Depois: HP 100, dinheiro 23, comida 2.

- **h29 · evento#33612 · PursuitSearch**: Elena Vale verificou a última localização conhecida sem encontrar o alvo. [ator Elena Vale (#1588); alvo sem personagem identificado]

  Necessidade `protection`; prioridade 56.689; fato#32235, confiança 100%, origem direct. Ação `pursue`, score do objetivo 84.55; alternativa `avoid_threat`=-2.95. Avaliação das alternativas em h29; objetivo criado em h29. Resultado: Busca local sem encontro; não consulta posição remota.
  Antes: HP 100, fome 56, dinheiro 7, comida 2; raiva 15.6, ressentimento 9.6, desespero 0.0. Depois: HP 100, dinheiro 7, comida 2.

- **h31 · evento#34821 · PursuitSearch**: Elena Vale verificou a última localização conhecida sem encontrar o alvo. [ator Elena Vale (#1588); alvo sem personagem identificado]
Fatos do arco não exibidos neste recorte: 1. IDs integrais no catálogo.

## L32 — Resposta de vingança após morte conhecida — Darin Vale (#4733)

Arco **78026**; h2279→h2378; 65 fatos; 6 participantes diretos. Tipo: `causal_or_single`.

**Leitura da história:** em h2279, Karvia, o primeiro registro deste recorte diz: Darin Vale roubou comida no mercado de Karvia.

John Luar (#4742) matou Darin Vale (#4733) em h2280.

Entre as consequências registradas: John Luar causou a morte de Darin Vale em confronto. O último fato disponível neste recorte ocorreu em h2378; isso não implica que a disputa tenha terminado definitivamente.

Os elos se conectam por fonte de evento/necessidade executada; o registro da fonte demonstra a referência causal do agente, sem garantir que aquela informação seja completa ou que toda a vida esteja neste arco.

Desfechos presentes: CharacterKilled: 1.

**Limite de qualidade:** o arco contém muita repetição de agressões. Continuidade causal aparece, mas a frequência de golpes não equivale a novos objetivos ou capítulos distintos.

- **h2279 · evento#1881832 · ItemStolen**: Darin Vale roubou comida no mercado de Karvia. [ator Darin Vale (#4733); alvo Karvia (cidade#1333)]

  Necessidade `food`; prioridade 100; origem interna `physiology`, sem fato externo de referência. Ação `steal_meal`, score do objetivo 18.40. Avaliação das alternativas em h2279; objetivo criado em h2279. Resultado: Alimento roubado. Fome reduzida.
  Antes: HP 2, fome 100, dinheiro 0, comida 0; raiva 79.2, ressentimento 96.3, desespero 100.0. Depois: HP 2, dinheiro 0, comida 0.

- **h2280 · evento#1882741 · ConflictStarted**: John Luar iniciou confronto físico com Darin Vale. [ator John Luar (#4742); alvo Darin Vale (#4733)]

  Necessidade `protection`; prioridade 81.85200000000002; fato#1881832, confiança 100%, origem direct. Ação `attack`, score do objetivo 76.39; alternativa `demand_return`=57.95. Avaliação das alternativas em h2280; objetivo criado em h2280. Resultado: Ataque causou 4 de dano real.
  Antes: HP 100, fome 68, dinheiro 12, comida 1; raiva 89.6, ressentimento 99.8, desespero 100.0. Depois: HP 100, dinheiro 12, comida 1.

- **h2280 · evento#1882742 · CharacterKilled**: John Luar causou a morte de Darin Vale em confronto. [ator John Luar (#4742); alvo Darin Vale (#4733)]

  Necessidade `protection`; prioridade 81.85200000000002; fato#1881832, confiança 100%, origem direct. Ação `attack`, score do objetivo 76.39; alternativa `demand_return`=57.95. Avaliação das alternativas em h2280; objetivo criado em h2280. Resultado: Ataque causou 4 de dano real.
  Antes: HP 100, fome 68, dinheiro 12, comida 1; raiva 89.6, ressentimento 99.8, desespero 100.0. Depois: HP 100, dinheiro 12, comida 1.

  Conhecimento familiar: Silas Vale (#4730) recebeu CharacterKilled em h2280, confiança 100%; pressões registradas: [('grief', 'active'), ('revenge', 'active')]. Isso registra recepção/estado, não uma vingança concluída.

- **h2284 · evento#1886062 · CharacterAttacked**: Silas Vale feriu John Luar em 3 HP. [ator Silas Vale (#4730); alvo John Luar (#4742)]

  Necessidade `revenge`; prioridade 72.592; fato#1882742, confiança 100%, origem direct. Ação `attack`, score do objetivo 94.66; alternativa `denounce`=83.20. Avaliação das alternativas em h2284; objetivo criado em h2284. Resultado: Ataque causou 3 de dano real.
  Antes: HP 100, fome 50, dinheiro 2, comida 1; raiva 98.8, ressentimento 99.8, desespero 100.0. Depois: HP 100, dinheiro 2, comida 1.

- **h2284 · evento#1886064 · CharacterAttacked**: John Luar feriu Silas Vale em 5 HP. [ator John Luar (#4742); alvo Silas Vale (#4730)]

  Necessidade `response`; prioridade 89.968; fato#1886062, confiança 100%, origem direct. Ação `attack`, score do objetivo 96.68; alternativa `defend`=85.07. Avaliação das alternativas em h2284; objetivo criado em h2284. Resultado: Ataque causou 5 de dano real.
  Antes: HP 97, fome 76, dinheiro 12, comida 1; raiva 99.7, ressentimento 100.0, desespero 100.0. Depois: HP 97, dinheiro 12, comida 1.

- **h2285 · evento#1886870 · CharacterAttacked**: Silas Vale feriu John Luar em 4 HP. [ator Silas Vale (#4730); alvo John Luar (#4742)]

  Necessidade `response`; prioridade 90.11800000000001; fato#1886064, confiança 100%, origem direct. Ação `attack`, score do objetivo 119.68; alternativa `defend`=90.44. Avaliação das alternativas em h2285; objetivo criado em h2285. Resultado: Ataque causou 4 de dano real.
  Antes: HP 95, fome 52, dinheiro 2, comida 1; raiva 99.7, ressentimento 100.0, desespero 100.0. Depois: HP 95, dinheiro 2, comida 1.

- **h2285 · evento#1886872 · CharacterAttacked**: John Luar feriu Silas Vale em 6 HP. [ator John Luar (#4742); alvo Silas Vale (#4730)]

  Necessidade `response`; prioridade 90.11800000000001; fato#1886870, confiança 100%, origem direct. Ação `attack`, score do objetivo 96.52; alternativa `defend`=84.74. Avaliação das alternativas em h2285; objetivo criado em h2285. Resultado: Ataque causou 6 de dano real.
  Antes: HP 93, fome 78, dinheiro 12, comida 1; raiva 99.7, ressentimento 100.0, desespero 100.0. Depois: HP 93, dinheiro 12, comida 1.

- **h2353 · evento#1940359 · ThreatAvoided**: Silas Vale buscou um local seguro conhecido. [ator Silas Vale (#4730); alvo sem personagem identificado]

  Necessidade `revenge`; prioridade 79.072; fato#1882742 fora da memória curta amostrada; necessidade/caso pode conservar referência própria. Ação `avoid_threat`, score do objetivo 12.65. Avaliação das alternativas em h2353; objetivo criado em h2353. Resultado: Afastou-se do local da ameaça.
  Antes: HP 56, fome 68, dinheiro 0, comida 0; raiva 90.2, ressentimento 98.6, desespero 100.0. Depois: HP 56, dinheiro 0, comida 0.

- **h2373 · evento#1955453 · PursuitSearch**: Silas Vale verificou a última localização conhecida sem encontrar o alvo. [ator Silas Vale (#4730); alvo sem personagem identificado]

  Necessidade `response`; prioridade 88.918; fato#1888360, confiança 30%, origem known. Ação `pursue`, score do objetivo 86.20. Avaliação das alternativas em h2373; objetivo criado em h2373. Resultado: Busca local sem encontro; não consulta posição remota.
  Antes: HP 56, fome 68, dinheiro 1, comida 0; raiva 85.8, ressentimento 97.8, desespero 100.0. Depois: HP 56, dinheiro 1, comida 0.

- **h2374 · evento#1956141 · PursuitSearch**: Silas Vale verificou a última localização conhecida sem encontrar o alvo. [ator Silas Vale (#4730); alvo sem personagem identificado]
- **h2378 · evento#1959225 · PursuitSearch**: Silas Vale verificou a última localização conhecida sem encontrar o alvo. [ator Silas Vale (#4730); alvo sem personagem identificado]
Fatos do arco não exibidos neste recorte: 54. IDs integrais no catálogo.

## L33 — Migração por procura criminal conhecida — Lyra Arven (#2807)

Arco **migration:53522**; h64→h100; 3 fatos; 1 participantes diretos. Tipo: `temporal_migration`.

**Leitura da história:** em h64, Norria, o primeiro registro deste recorte diz: Lyra Arven iniciou viagem para uma localidade conhecida.

Entre as consequências registradas: Lyra Arven estabeleceu residência em Silven. O último fato disponível neste recorte ocorreu em h100; isso não implica que a disputa tenha terminado definitivamente.

Partida, chegada e fixação pertencem à mesma viagem por ator/tempo. Antecedentes são contexto; não se presume que um crime específico seja a causa sem referência na decisão.

Desfechos presentes: ResidentMoved: 1.

- **h10 · evento#15142 · ItemStolen**: Lyra Arven roubou provisão de Nora Hammer. [ator Lyra Arven (#2807); alvo Nora Hammer (#2790)]

  Necessidade `money`; prioridade 48.2; origem interna `economy`, sem fato externo de referência. Ação `steal_person`, score do objetivo 89.70; alternativa `work`=71.50. Avaliação das alternativas em h10; objetivo criado em h10. Resultado: Provisão real roubada.
  Antes: HP 100, fome 44, dinheiro 6, comida 1; raiva 0.0, ressentimento 0.0, desespero 0.0. Depois: HP 100, dinheiro 6, comida 2.

- **h24 · evento#30170 · WantedIssued**: Lyra Montes registrou procura por Lyra Arven. [ator Lyra Montes (#2792); alvo Norria (cidade#443)]
- **h64 · evento#53522 · MigrationStarted**: Lyra Arven iniciou viagem para uma localidade conhecida. [ator Lyra Arven (#2807); alvo Silven (cidade#461)]

  Necessidade `migration`; prioridade 69.872; origem interna `known_towns`, sem fato externo de referência. Ação `migrate`, score do objetivo 84.35. Avaliação das alternativas em h64; objetivo criado em h64. Resultado: Uma etapa física da viagem foi realizada.
  Antes: HP 100, fome 32, dinheiro 2, comida 2; raiva 0.0, ressentimento 0.0, desespero 0.9. Depois: HP 100, dinheiro 2, comida 2.

- **h75 · evento#61795 · MigrationArrived**: Lyra Arven chegou como visitante a Silven. [ator Lyra Arven (#2807); alvo Silven (cidade#461)]

  Necessidade `migration`; prioridade 83.204; origem interna `migration`, sem fato externo de referência. Ação `migrate`, score do objetivo 84.35. Avaliação das alternativas em h75; objetivo criado em h75. Resultado: Uma etapa física da viagem foi realizada.
  Antes: HP 100, fome 54, dinheiro 2, comida 2; raiva 0.0, ressentimento 0.0, desespero 2.5. Depois: HP 100, dinheiro 2, comida 2.

- **h100 · evento#81297 · ResidentMoved**: Lyra Arven estabeleceu residência em Silven. [ator Lyra Arven (#2807); alvo Silven (cidade#461)]
Fatos do arco não exibidos neste recorte: 0. IDs integrais no catálogo.

## L34 — Migração por pobreza persistente — Silas Ferros (#579)

Arco **migration:533024**; h623→h659; 3 fatos; 1 participantes diretos. Tipo: `temporal_migration`.

**Leitura da história:** em h623, Morria, o primeiro registro deste recorte diz: Silas Ferros iniciou viagem para uma localidade conhecida.

Entre as consequências registradas: Silas Ferros estabeleceu residência em Dorvia. O último fato disponível neste recorte ocorreu em h659; isso não implica que a disputa tenha terminado definitivamente.

Partida, chegada e fixação pertencem à mesma viagem por ator/tempo. Antecedentes são contexto; não se presume que um crime específico seja a causa sem referência na decisão.

Desfechos presentes: ResidentMoved: 1.

- **h623 · evento#533024 · MigrationStarted**: Silas Ferros iniciou viagem para uma localidade conhecida. [ator Silas Ferros (#579); alvo Dorvia (cidade#526)]

  Necessidade `migration`; prioridade 42.47200000000001; origem interna `known_towns`, sem fato externo de referência. Ação `migrate`, score do objetivo 88.35. Avaliação das alternativas em h623; objetivo criado em h623. Resultado: Uma etapa física da viagem foi realizada.
  Antes: HP 100, fome 34, dinheiro 0, comida 2; raiva 0.0, ressentimento 0.0, desespero 48.4. Depois: HP 100, dinheiro 0, comida 2.

- **h635 · evento#543497 · MigrationArrived**: Silas Ferros chegou como visitante a Dorvia. [ator Silas Ferros (#579); alvo Dorvia (cidade#526)]

  Necessidade `migration`; prioridade 59.416000000000004; origem interna `migration`, sem fato externo de referência. Ação `migrate`, score do objetivo 88.35. Avaliação das alternativas em h635; objetivo criado em h635. Resultado: Uma etapa física da viagem foi realizada.
  Antes: HP 100, fome 58, dinheiro 0, comida 2; raiva 0.0, ressentimento 0.0, desespero 50.2. Depois: HP 100, dinheiro 0, comida 2.

- **h659 · evento#563829 · ResidentMoved**: Silas Ferros estabeleceu residência em Dorvia. [ator Silas Ferros (#579); alvo Dorvia (cidade#526)]
Fatos do arco não exibidos neste recorte: 0. IDs integrais no catálogo.

## L35 — Migração por ameaça conhecida — Tomas Luar (#891)

Arco **migration:8805**; h4→h44; 3 fatos; 1 participantes diretos. Tipo: `temporal_migration`.

**Leitura da história:** em h4, Silmar, o primeiro registro deste recorte diz: Tomas Luar iniciou viagem para uma localidade conhecida.

Entre as consequências registradas: Tomas Luar estabeleceu residência em Sildor. O último fato disponível neste recorte ocorreu em h44; isso não implica que a disputa tenha terminado definitivamente.

Partida, chegada e fixação pertencem à mesma viagem por ator/tempo. Antecedentes são contexto; não se presume que um crime específico seja a causa sem referência na decisão.

Desfechos presentes: ResidentMoved: 1.

- **h4 · evento#8805 · MigrationStarted**: Tomas Luar iniciou viagem para uma localidade conhecida. [ator Tomas Luar (#891); alvo Sildor (cidade#958)]

  Necessidade `migration`; prioridade 52.45; origem interna `known_towns`, sem fato externo de referência. Ação `migrate`, score do objetivo 93.95. Avaliação das alternativas em h4; objetivo criado em h4. Resultado: Uma etapa física da viagem foi realizada.
  Antes: HP 100, fome 25, dinheiro 18, comida 2; raiva 16.8, ressentimento 9.7, desespero 0.0. Depois: HP 100, dinheiro 18, comida 2.

- **h15 · evento#20845 · MigrationArrived**: Tomas Luar chegou como visitante a Sildor. [ator Tomas Luar (#891); alvo Sildor (cidade#958)]

  Necessidade `migration`; prioridade 52.1; origem interna `migration`, sem fato externo de referência. Ação `migrate`, score do objetivo 93.95. Avaliação das alternativas em h15; objetivo criado em h15. Resultado: Uma etapa física da viagem foi realizada.
  Antes: HP 100, fome 47, dinheiro 18, comida 2; raiva 13.5, ressentimento 9.3, desespero 0.0. Depois: HP 100, dinheiro 18, comida 2.

- **h44 · evento#42539 · ResidentMoved**: Tomas Luar estabeleceu residência em Sildor. [ator Tomas Luar (#891); alvo Sildor (cidade#958)]
Fatos do arco não exibidos neste recorte: 0. IDs integrais no catálogo.

## L36 — Ração obtida, mas morte antes da refeição — Bela Douran (#3139)

Arco **survival:3139**; h582→h583; 2 fatos; 2 participantes diretos. Tipo: `temporal_survival`.

**Leitura da história:** em h582, Arvia, o primeiro registro deste recorte diz: Bela Douran roubou provisão de Bela Vale.

Entre as consequências registradas: Bela Douran morreu por privação. O último fato disponível neste recorte ocorreu em h583; isso não implica que a disputa tenha terminado definitivamente.

A ação e a morte estão ligadas por personagem e fechamento da mesma hora: o estado após obter a ração conserva fome no máximo, e o registro da morte ainda contém esse alimento. É uma sequência temporal auditada, não um elo inventado por fonte.

Desfechos presentes: CharacterDied: 1.

- **h582 · evento#498585 · ItemStolen**: Bela Douran roubou provisão de Bela Vale. [ator Bela Douran (#3139); alvo Bela Vale (#604)]

  Necessidade `food`; prioridade 100; origem interna `physiology`, sem fato externo de referência. Ação `steal_person`, score do objetivo 61.10; alternativa `steal_meal`=59.03. Avaliação das alternativas em h582; objetivo criado em h582. Resultado: Provisão real roubada.
  Antes: HP 1, fome 100, dinheiro 0, comida 0; raiva 95.1, ressentimento 99.1, desespero 100.0. Depois: HP 1, dinheiro 0, comida 1.

- **h583 · evento#498991 · CharacterDied**: Bela Douran morreu por privação. [ator sem personagem identificado; alvo Bela Douran (#3139)]
  Conhecimento familiar: Elena Douran (#3142) recebeu RemainsLocated em h777, confiança 100%; pressões registradas: [('grief', 'active')]. Isso registra recepção/estado, não uma vingança concluída.

Fatos do arco não exibidos neste recorte: 0. IDs integrais no catálogo.
