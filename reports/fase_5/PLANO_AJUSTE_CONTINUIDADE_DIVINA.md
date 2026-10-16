# Ajuste final de continuidade divina

Registro do plano elaborado durante a campanha. Sua execução ficou preservada em `ENTREGA_INTERMEDIARIA_DIVINA.json`. A revisão posterior encontrou também problemas sociais; o conjunto completo de ajustes de entrega e sua validação estão em `ENTREGA_FINAL.json` e no relatório técnico.

O microcenário em `DIAGNOSTICO_CONTINUIDADE_DIVINA.json` reproduziu duas falhas no núcleo congelado da campanha (`2a2ede5c51058e8e5ee849dc04a08f7002dd8d7da8db8278312f2460e6e4d8e1`):

1. Um seguidor cultural do deus anterior, presente na morte e apoteose, não recebia hipótese sobre o sucessor se ainda não venerava o mortal.
2. Uma oração ao mortal ascendido era executada, mas não alcançava sua Divinity objetiva porque os IDs de corpo e divindade são diferentes.

O código da campanha permanecerá intacto até as 5.000 horas e exportação final. Depois, será ajustado apenas esse circuito e ampliada a regressão composta de apoteose. A entrega final e o código da campanha terão hashes separados, ambos preservados. Não será iniciada outra longa para substituir o resultado.

Regras do ajuste:

- Receber um fato de apoteose pode criar hipótese incerta em quem já conhecia o culto anterior; não converte automaticamente, não informa seguidores remotos e não concede certeza ontológica.
- Uma oração ao mortal só é encaminhada a uma Divinity vinculada se essa entidade existe objetivamente e sua origem corresponde ao mortal.
- Adoração de mortal comum não cria entidade nem pedidos divinos.
- Fonte, confiança, limites de crença e escolha posterior continuam preservados.
- Validar entrega do fato, escolha posterior, encaminhamento, falsa divinização, save/load e suíte anterior; manter os casos controlados separados das histórias naturais.
