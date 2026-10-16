# Cael Montes: comida carregada e causa da morte

Campanha curta final, seed Serevan-5, regras `mvp-8-fase5`, NPC #3881. Este caso deve ser incluído nas estatísticas: houve **uma morte alimentar com comida no inventário**. Ele não demonstra que o NPC ignorou uma ração que já carregava ao decidir sua ação.

| Hora | Evidência | Consequência |
|---:|---|---|
| 298 | Decisão `steal`, necessidade de comida com prioridade 100 | Antes: HP 18, fome 100, comida 0. Depois: HP 18, fome 100, comida 1. A aquisição consumiu a ação. |
| 298 | `ItemStolen` #282765 | Cael conseguiu uma ração no mercado de Silven. |
| 298 | `CharacterAttacked` #282779 | Ruan Valerius causou **16 de dano**, com intenção `contain`, reduzindo Cael a 2 HP antes do fechamento da hora. |
| 299 | `CharacterDied` #283044 | O dano fisiológico restante matou Cael. O registro final conserva comida 1 e separa dano acumulado: fome 88, combate 16. |

A ordem do motor é: cada NPC realiza sua ação, outros NPCs também podem agir, depois a fisiologia fecha a hora. Cael não ganhou uma segunda ação para consumir a ração antes do ataque e do dano final. Comer tampouco restaura HP instantaneamente: a recuperação exige suas condições próprias.

**Conclusão:** a fome forneceu o dano final, mas o combate foi decisivo nesta morte. A classificação agregada `hunger` simplifica uma causalidade mista. Contar este caso como ausência de comida seria errado; contar apenas a causa final também esconderia o papel da violência. Não foi alterado o motor para conceder consumo gratuito ou imunidade durante a aquisição.

Melhoria de diagnóstico: distinguir causa final, danos contribuintes e oportunidade efetiva de consumo. Isso preserva a regra de uma ação e permite entender melhor as mortes.

Dados rastreáveis: [sequência extraída](</home/hugo/Área de trabalho/procedrual/reports/fase_5/evidencia_comida_carregada_curta.json>), [decisões](</home/hugo/Área de trabalho/procedrual/reports/fase_5/curta_validada_500h/decisoes.jsonl.gz>) e [eventos](</home/hugo/Área de trabalho/procedrual/reports/fase_5/curta_validada_500h/eventos.jsonl.gz>).
