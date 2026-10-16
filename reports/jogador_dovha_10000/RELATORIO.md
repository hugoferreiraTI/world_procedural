# Campanha de 10.000 turnos com jogador — Dovha

Experimento realizado em 7 de outubro de 2026. O jogador Codex foi controlado
por um script usando `Engine.execute`, os mesmos comandos do terminal. Nenhuma
vida, moeda, relação, necessidade ou personalidade foi alterada para facilitar
a campanha. O motor do jogo permaneceu inalterado.

```bash
python3 -m experiments.player_campaign --turnos 10000
```

A política foi de um mercador local: permanecer em Elithon, visitar a posição
vizinha, comprar e vender, conversar, ajudar, aceitar/recusar pedidos e cuidar
das próprias necessidades. As escolhas sociais usaram apenas NPCs presentes e
respostas de diálogo. A inspeção interna serviu para medir e explicar resultados.
Não foi uma campanha humana nem uma exploração completa do mapa.

## Resultado principal

Foram 10.000 turnos efetivamente avançados por ações, do turno 24 ao 10.024.
Ocorreram 79 conversas com 11 NPCs, 10 entregas de comida e 5 pedidos de ajuda.
Dois pedidos foram concluídos, um foi recusado e dois falharam com a morte dos
solicitantes. Todas as validações estruturais passaram.

- Elena Bruma recebeu comida no turno 34, pediu ajuda no 67 e teve seu pedido
  concluído no 81. Um novo pedido seu foi recusado no turno seguinte à oferta
  feita no 110. A recusa não produziu retaliação ao jogador.
- John Solaris pediu ajuda no turno 88 e recebeu comida no 90. Sua opinião
  final armazenou `prestativo: 100`, admiração 100 e confiança 90. Ele morreu
  posteriormente; a reputação permanece no registro da entidade.
- Dovha recebeu comida no turno 63. Sua relação com o jogador chegou a
  confiança 50, com reputação `prestativo: 15`.
- Onze NPCs adquiriram reputação positiva sobre Codex, incluindo personagens
  que conheceram favores por rumores e não receberam nenhuma entrega.

Os pedidos apareceram durante conversas iniciadas pelo jogador. Não houve
abordagem espontânea, perseguição, vingança ou pressão de facções. A interface
atual rejeita `roubar comida` e `atacar 26`: essas ações não existem para o jogador,
portanto o experimento não pode demonstrar reações a crimes cometidos por ele.

## Falhas observadas

**Sobrevivência por descanso:** a campanha usou 8.980 descansos. O jogador
terminou com vida 98/100 apesar de fome 100/100. Em 1.714 descansos, sua vida
líquida aumentou mesmo com privação máxima. A cura do descanso compensa a perda
por fome; isso invalida qualquer conclusão de que a sobrevivência esteja saudável.

**Cidade sem interlocutores:** os NPCs presentes no mapa de Elithon morreram.
No final, o mercado tinha zero comida, apesar das 271 moedas do jogador. As
interações sociais concentraram-se no início e não se sustentaram ao longo dos
10.000 turnos. O experimento expõe uma cidade funcionalmente paralisada.

**Arbitragem no mesmo mercado:** compra e revenda de grandes lotes elevaram
as moedas de 25 para 331 em seis ações. Madeira levou o saldo de 25 para 75,
trigo de 75 para 149 e ferro de 149 para 331. A retirada do estoque aumenta o
preço usado na revenda; o próprio mercado paga mais pelos produtos que acabou
de vender. Essa fonte de dinheiro precisa ser corrigida.

**Consequências sociais limitadas:** confiança, memória, reputação e pedidos
reagiram aos favores. Admiração ainda não gerou proteção, descontos ou ajuda
espontânea. A recusa não gerou uma reação emocional persistente. O jogador
continuou com o apelido `Desconhecido`, pois completou apenas dois pedidos,
abaixo do requisito atual de três pedidos locais para ganhar um título.

## Artefatos

- `relatorio.json`: eventos, opiniões, pedidos, ações e checkpoints.
- `acoes.jsonl`: cada comando executado, resultado, turno e estado do jogador.
- `save_final.json`: campanha completa para inspeção ou carregamento.

Uma primeira tentativa, conservada em `../jogador_dovha_10000_sobrevivencia`,
gastou quase todo o dinheiro com comida antes de negociar. Também rodou 10.000
turnos, com seis ajudas e um pedido que falhou; o descanso igualmente mascarou
a fome. A segunda tentativa mudou apenas a política do jogador, não as regras.
