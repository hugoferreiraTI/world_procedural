# Levantamento anterior à fase 2

Base exata: `fase_2.md`, lido integralmente. O documento original, comparativo,
hardening, auditoria e histórias anteriores foram confrontados com o código.

## Estruturas a reutilizar

- `Need`, `Goal`, `Solution`, prioridade e `utility.evaluate` já representam o ciclo de decisão.
- `KnowledgeSystem.learn` é o ponto comum de percepção direta e rumor; o grafo contém parentesco e vínculos.
- `QuestSystem` já oferece, aceita, recusa, conclui e reconcilia pedidos; será ampliado para novos contratos executáveis.
- `EventBus` comunica acontecimentos; `EventRecorder` define testemunhas locais.
- `Character.applied_facts` deduplica efeitos sociais independentemente da memória curta.
- `Economy`, `ProfessionSystem`, `Navigation` e `ItemService` executam as ações materiais.
- `JsonRepository` serializa dataclasses e RNG; versão atual `mvp-2`.

## Personalidade atual

| Traço | Uso encontrado |
| --- | --- |
| honesty | Compra/roubo, interpretação social de crimes. |
| compassion | Pedido e oferta de ajuda, interpretação de favores e recusas. |
| courage | Roubo, investigação de crime e interpretação contextual. |
| independence | Preferência por coleta. |
| greed | Preferência por roubo. |
| diligence | Trabalho e prioridade financeira/profissional. |
| family_loyalty | Existe como predisposição persistente, mas não alimenta cuidado familiar executável. |
| persistence | Interpretação de recusa; não equivale a vingatividade. |

Gerados em `generation.add_character`, oito valores de 5 a 95 pelo RNG da seed.
Persistidos por `persistence.encode/decode`, validados em escala 0–100.

Reutilizar `family_loyalty` como predisposição familiar geral, distinta da força
de cada relacionamento. Não criar `falsehood`, outro eixo familiar ou um segundo
motor emocional. Ambição, vingatividade e temperamento representam dimensões
novas a avaliar para uso concreto; cinismo não é necessário ao escopo inicial.

## Quatro bugs reproduzíveis

1. Jogador age antes de fisiologia; NPC pode morrer antes de decidir comer.
2. Quest bloqueia ajuda com `money >= 10`, diferente da viabilidade de compra.
3. `_action` cria necessidade antes de saber se a ação é válida.
4. `gossip` elimina IDs já conhecidos sem avaliar melhoria de certeza.

## Lacunas comportamentais

Não há observações persistentes de familiares, pressões de luto/retaliação/
proteção/status/ascensão ou estabilização financeira de médio prazo.
O conhecimento verdadeiro do mundo não pode substituir percepção para criá-las.
Metas pessoais devem ter causa, prazo, alvo, soluções e fechamento rastreáveis.

## Exclusões mantidas

Reposição profissional e revisão populacional permanecem adiadas. Não adicionar
combate, guerras, viagens entre cidades, deuses, religião organizada, carreira,
nascimentos, GOAP, nova engine de quests/decisão ou IA generativa.

A medição final não terá uma cota artificial de ações sociais nem redução dos
pesos da fome. Resultados da versão nova não são comparação controlada da mesma
geografia se a versão usada no RNG for alterada.
