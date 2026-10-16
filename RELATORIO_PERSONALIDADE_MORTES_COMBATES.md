# Personalidade, combates e mortes — Fase 4.1

Análise do código atual e da campanha já auditada de 5.000 horas, seed **Vespera-47**. Não foi necessária uma nova simulação. Os resultados mostram o comportamento conjunto do sistema; não houve um experimento isolando cada traço de personalidade.

## Como a personalidade funciona

Cada NPC tem 11 traços: honestidade, compaixão, coragem, independência, ganância, diligência, lealdade familiar, persistência, temperamento, vingatividade e ambição. Eles influenciam a pontuação das ações disponíveis.

A decisão passa por **necessidade prioritária → alternativas conhecidas e viáveis → avaliação de personalidade, emoções e risco → execução**. Portanto, a personalidade influencia como resolver um problema, mas não garante que uma necessidade menos prioritária seja atendida.

| Traços | Tendência nas decisões |
|---|---|
| Coragem e vingatividade | Favorecem confrontar, investigar e atacar; coragem reduz a preferência por fugir ou se render. |
| Temperamento | Favorece ameaças e insultos, que podem alimentar a escalada do conflito. |
| Compaixão e lealdade familiar | Favorecem ajuda e proteção; compaixão também favorece perdão e reduz agressão. |
| Honestidade e ganância | Honestidade desestimula roubos e favorece restituição; ganância favorece apropriação de recursos. |
| Independência | Favorece buscar recursos por conta própria e reduz a preferência por algumas formas de ajuda. |
| Diligência, ambição e persistência | Favorecem trabalho, treinamento, avanço pessoal ou insistência em cobrar devoluções. |

**Traços e emoções são coisas diferentes.** Raiva, medo e ressentimento mudam conforme os acontecimentos. A personalidade também pode se adaptar à pressão prolongada, mas atualmente essa mudança é pequena: até cinco incrementos de um ponto em independência e vingatividade por NPC.

## Como um conflito vira combate

Uma relação ruim, sozinha, não obriga o NPC a atacar. Precisa existir um motivo conhecido, como agressão, vingança, proteção ou perseguição. Para atacar, o alvo precisa estar presente, vivo e fora de uma trégua ou rendição protegida.

A agressão fica disponível quando há raiva suficiente e vingatividade, um oponente ativo ou uma perseguição de gravidade suficiente. Depois, ainda disputa com ameaçar, confrontar, defender, fugir, pedir ajuda, perdoar e se render.

O risco considera força observada, aliados, inimigos, guardas, ferimentos e saúde. **A coragem não aumenta diretamente o dano:** o golpe depende da arma, sua qualidade, HP, ferimentos, defesa e variação aleatória. A personalidade muda principalmente a decisão de entrar, continuar ou sair do confronto.

## O que aconteceu nas 5.000 horas

| Resultado registrado | Quantidade |
|---|---:|
| Ataques individuais — golpes, não combates distintos | 17.168 |
| Eventos de fuga bem-sucedida | 3.822 |
| Eventos de rendição | 1.551 |
| Mortes classificadas como combate | 9 |
| Mortes classificadas como fome | 243 |
| Mortes classificadas como sede | 3 |

Os muitos golpes produziram poucas mortes porque existem defesa, fuga, rendição e interrupção por incapacidade. Também ocorreram ajuda e proteção. Isso permite conflitos com sobreviventes e consequências posteriores.

A causa registrada de morte corresponde ao **dano final que matou**, não a toda a trajetória. Entre os 243 mortos por fome, 32 também tinham dano físico ainda não recuperado. Portanto, fome e violência podem participar da mesma morte, mesmo quando o registro final diz “fome”.

## Onde a personalidade encontra seus limites

Ela pode influenciar sobrevivência indiretamente: escolher roubar ou pedir ajuda, aceitar risco, fugir ou trabalhar. Entretanto, os dados disponíveis não permitem afirmar que um traço específico causou determinada morte.

O problema dominante continua sendo material e de prioridades: obter comida, recuperar HP e conseguir descansar a tempo. Um NPC diligente pode preferir trabalhar, mas a prioridade da necessidade econômica também pode impedir a recuperação antes dessa comparação entre ações.

**Avaliação:** a personalidade já produz respostas diferentes e combates com saídas alternativas. A mortalidade ainda depende muito mais da cadeia de alimentação e recuperação: fome representa **95,3% das 255 mortes**. O próximo ajuste mais útil é investigar quando recuperação perde prioridade para dinheiro ou trabalho, mesmo havendo condições de descanso.

Fontes locais: `procedural/models.py`, `procedural/utility.py`, `procedural/conflicts.py`, `procedural/emotions.py` e `reports/fase_4_1/global_5000h/resumo.json`.
