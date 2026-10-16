# Comparativo de implementação — Fase4

Este arquivo descreve o escopo entregue, incluindo a correção posterior de
casos criminais acumulados. Os resultados longos pertencem ao código congelado,
preservado separadamente. O relatório de 34 seções
apresenta as métricas e os exemplos da campanha oficial única de Mira.

| Sistema | Situação | Consequência/limite |
|---|---|---|
| Fome/sede/reserva preventiva | Reaproveitado | Mesmos parâmetros vitais; combate/captura podem alterar acesso e prioridades. |
| Profissões/reposição/treinamento | Reaproveitado | Produção com insumos/pagador reais; trabalhador novo vem de abstrato, sem identidade herdada. |
| Necessidades pessoais | Expandido | Família, luto, vingança, proteção, avanço/status recebem alternativas físicas e sociais. |
| Emoções | Implementado | Raiva, ressentimento, humilhação e desespero têm causas e decaimento próprios. |
| Mudança de personalidade | Mínimo | Pequenas mudanças após pressão e intervalo720h; não há psicologia extensa. |
| Grievance | Implementado | Alvo e fonte conhecidos, intensidade limitada, sem culpa automática de governante. |
| Crime econômico | Mínimo/parcial | Roubo transfere provisão real e pode ser escolhido por fome, dinheiro ou avanço. Sem cadeia específica de revenda ou ganho monetário direto do roubo. |
| Confronto/ameaça/restituição | Implementado | Geram fatos e pressões; devolução é decisão posterior, usando bem real. |
| Pedido de desculpas/perdão/acalmar | Implementado | Podem aliviar tensão/encerrar episódio; não garantem amizade duradoura. |
| Combate NPC×NPC/jogador | Implementado mínimo | HP, arma própria, avaliação aproximada alheia, defesa, lesão e RNG. |
| Intervenção de terceiros | Implementado | Protetor presente pode receber o ataque; socorro depende de recursos. |
| Fuga/rendição | Implementado | Deslocamento físico e término de confronto; tentativa fracassada usa hora. |
| Ferimentos | Implementado mínimo | Afetam combate, eficiência dos lotes, fuga e pressão de recuperação. |
| Tratamento | Parcial | Socorro inicial com comida/água e descanso; sem curandeiro/hospital/anatomia. |
| Mortes violentas | Implementado | Caminho comum de morte preserva corpo/posses e censo/sucessão. |
| Conhecimento de morte | Reaproveitado/expandido | Testemunha aprende; familiar remoto depende de informação. |
| Procurados/perseguição | Parcial | Evidência/status/posição conhecidos por cada guarda; busca local limitada. Não cruza mapas automaticamente. |
| Captura/detenção | Mínimo | Presença, prova, rendição/incapacidade, multa real e12h; sem tribunal/prisão logística. |
| Migração individual | Implementado mínimo/parcial | Rotas conhecidas/provisões, portões/caminho/visita24h e censo transferido. Fuga, ameaça e pobreza atuam; metadados de família/trabalho ainda não alimentam completamente os outros motivos. |
| População persistente | Expandido | Mira1728; mais famílias e encontros, geografia original conservada. |
| Abstratos | Redimensionado/agregado | Mira4338; continuam sem histórias individuais. Não é um mundo sem abstratos. |
| LOD | Expandido | Decisões1/3/6/12h e promoção por fatos; fisiologia toda hora. |
| Reputação | Expandido | Agressão/auxílio/reparação são interpretados individualmente; sem reputação universal. |
| Sucessão | Expandida na causa | Morte violenta também aciona sucessão simples. Sem disputa formal de poder. |
| Save/load | Implementado/corrigido | Estados novos persistidos. A campanha revelou divergência do índice criminal; correção posterior validada em regressões e continuação curta. Save volumoso permanece como limite. |
| Religião/fé como objetivo executável | Não implementado | Campos antigos continuam existentes, sem instituição/reação divina ativa. |
| Deuses/magia | Não implementado | Sem intervenção divina ou combate mágico. |
| Facções políticas/revoluções | Não implementado | Lealdade/metadados não representam política coletiva autônoma. |
| Guerra/exércitos/cerco | Não implementado | Violência desta fase é entre indivíduos presentes. |
| Nascimento/idade/herança | Não implementado | Famílias iniciais não constituem ciclo demográfico/dinástico completo. |
| Caravanas/comércio interurbano físico | Não implementado | Migração não cria caravanas ou transporta economia coletiva. |
| Destruição de cidades | Não implementado | Nem morte de governante apaga cidade/reino. |

A Fase4 amplia o repertório de respostas e as consequências entre personagens.
Ela não garante que a fome deixe de ser a principal causa de morte, nem que
uma cadeia de eventos tenha profundidade literária. Isso exige observar as
métricas e as histórias reais, além de continuar avaliando acesso individual,
continuidade de informação e oportunidades sociais/econômicas.
