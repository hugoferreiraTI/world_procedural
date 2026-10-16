# Histórias reais — Fase 5.1

Seed **Selvaren-51**, mundo novo, sem jogador; 1.000 horas totais, incluindo o marco de 200h.
A seleção abaixo contém fatos da campanha, anterior aos ajustes finais de integração. Microcenários não entram como lore natural.
São episódios representativos; alguns pertencem ao mesmo arco. Os eventos não registram pensamentos privados dos personagens.

## 1. Uma proposta chegou à autoridade local

O grupo **Círculo de Karvia — Proteção**, de **Karvia**, surgiu na hora 6 por `security`. O representante registrado na formação era Arthus Valerius (NPC #864).
Na hora 26, Arthus Valerius (NPC #864) entregou a proposta #43455 a Mira Ferros (NPC #3113), em **Karvia**. A entrega ocorreu no encontro físico; o evento não equivale a aprovação nem a solução completa do problema.
Encadeamento retido: GroupFormed #19005 (h6) → ProposalCreated #43457 (h23) → GroupMeeting #43458 (h23) → ProposalSubmitted #46405 (h26).
Evidência central: **ProposalSubmitted #46405**, hora **26**.

## 2. Representação de uma vila na cidade

O grupo **Círculo de Norlen — Proteção**, de **Norlen**, surgiu na hora 20 por `security`. O representante registrado na formação era Darin Luar (NPC #852).
Na hora 58, Darin Luar (NPC #852) entregou a proposta #43445 a Iria Solaris (NPC #3567), em **Dormir**. A entrega ocorreu no encontro físico; o evento não equivale a aprovação nem a solução completa do problema.
Encadeamento retido: GroupFormed #40186 (h20) → ProposalCreated #43447 (h23) → GroupMeeting #43448 (h23) → ProposalSubmitted #78157 (h58).
Evidência central: **ProposalSubmitted #78157**, hora **58**.

## 3. Resposta da autoridade e efeito material

O grupo **Círculo de Elithon — Proteção**, de **Elithon**, surgiu na hora 33 por `security`. O representante registrado na formação era Elena Valerius (NPC #2395).
Na hora 38, Ruan Montes (NPC #2340) produziu a resposta **partial** à proposta #54381. Efeito material registrado: `{"food": 0, "money": 2, "recipients": [2328], "weapon_id": 58027}`. Isso demonstra resposta institucional; não prova que todos os membros foram atendidos.
Evidência central: **PolicyDecided #58028**, hora **38**.

## 4. A informação voltou presencialmente ao grupo

Na hora 179, Cael Luar (NPC #5276) retransmitiu presencialmente as respostas [123182] a Cael Luar (NPC #5276), Lyra Kars (NPC #5279). A existência da decisão na cidade, sozinha, não havia informado esses membros.
Evidência central: **ResponseRelayed #196623**, hora **179**.

## 5. Falhas recebidas chegaram ao protesto

O grupo **Círculo de Valthon — Proteção**, de **Valthon**, surgiu na hora 49 por `security`. O representante registrado na formação era Lyra Arven (NPC #68).
Na hora 225, Lyra Arven (NPC #68) protestou após 1 falhas registradas; fonte recebida #192959. Houve reação política, sem violência coletiva automática.
Encadeamento retido: ProposalCreated #71847 (h52) → GroupMeeting #71848 (h52) → ProposalSubmitted #135943 (h118) → PolicyDecided #136180 (h118) → PolicyDecided #192959 (h176) → GroupProtested #242596 (h225).
Evidência central: **GroupProtested #242596**, hora **225**.

## 6. A intenção letal chegou ao ataque, sem finalização

Na hora 328, Cael Luar (NPC #473) atacou Bela Solaris (NPC #2817) com intenção **kill**, causando 10 de dano. As fontes registram dano anterior conhecido; a campanha não chegou a uma oportunidade terminal desse confronto.
Mudança de intenção documentada: ViolenceIntentChanged #349026, hora 328.
Evidência central: **CharacterAttacked #349027**, hora **328**.
Auditoria da ação: WorldPressure=85; ActionPressure=38.74; capacidade=34.44; barreiras=[]; fontes=[346149, 348372]; alternativa=attack.
Fontes anteriores: Bela Solaris feriu Cael Luar em 12 HP. (#346149, h325); Bela Solaris feriu Cael Luar em 9 HP. (#348372, h327).

## 7. Morte em combate

Na hora 731, Nora Arven (NPC #2423) matou Aldren Vale (NPC #2409). Intenção registrada: `subdue`; contexto: `ataque físico`. Uma morte física com intenção não letal não constitui finalização deliberada.
Evidência central: **CharacterKilled #819026**, hora **731**.
Auditoria da ação: WorldPressure=80; ActionPressure=40.19; capacidade=34.73; barreiras=[]; fontes=[812447, 813774, 815032]; alternativa=attack.
Fontes anteriores: Aldren Vale feriu Elena Arven em 1 HP. (#812447, h726); Aldren Vale feriu Elena Arven em 1 HP. (#813774, h727); Aldren Vale feriu Elena Arven em 1 HP. (#815032, h728).

## Ausências e histórias que não avançaram

Dos 886 grupos formados, 128 chegaram a entrega, protesto ou retransmissão. Há muito mais articulação que mudança concluída; formar grupo continua sem garantir ação.
Facções: 0 ações, 0 preparações e 0 adesões. As sedes naturais continuaram limitando a saída e a capacidade; o êxito do raid controlado não é uma invasão desta seed.
Deuses: 75 orações, 931 avaliações e 0 intervenções. A causa conhecida não ultrapassou o filtro semântico; oração isolada não bastou. O cenário controlado de perda de fiéis não ocorreu aqui como arco confirmado.
Intenções de matar: 7 mudanças, 6 autores; 0 oportunidades e 0 decisões terminais. Destruição de localidades, apoteose e morte divina não foram produzidas para preencher categorias.

Não há base para afirmar que esta fase já produz guerras ou grandes sagas com regularidade. A evidência mais forte é a continuidade política; facções e divindades permanecem gargalos naturais.

[Evidência filtrada](</home/hugo/Área de trabalho/procedrual/reports/fase_5_1/campanha/exemplos_filtrados.json>) · [Métricas da campanha](</home/hugo/Área de trabalho/procedrual/reports/fase_5_1/campanha/principal_1000h.json>) · [Único save final](</home/hugo/Área de trabalho/procedrual/reports/fase_5_1/campanha/save_final.json>)
