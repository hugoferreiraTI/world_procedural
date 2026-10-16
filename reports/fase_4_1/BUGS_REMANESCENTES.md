# Tentativas redundantes após falha de aquisição composta

Verificado no núcleo congelado da Fase 4.1, SHA-256
`3206658685c769d82049bc62720e755b4a89c53840b26bc86c10342a459d32a6`.
O padrão de bloqueio já existia na versão anterior; a campanha longa conserva o
código auditado para permitir atribuir todos os resultados ao mesmo núcleo.

Mira Bruma #1922, Vespera-47 nova:

- h287: `steal_meal` bem-sucedido, HP8, fome100→60; nenhuma cura nessa refeição.
- h306: `forage_meal` falha: “Os alimentos silvestres locais acabaram por hoje.”
- h307: `forage` tenta o mesmo fornecedor e falha com a mesma mensagem.
- h308–309: obtém água e bebe; não obtém outra ração.
- h310: morre de fome sem comida no inventário.

`GoalSystem.decide` guarda o bloqueio sob `current.action`; ao falhar a cadeia,
fica `forage_meal`. `_evaluate` consulta o nome da alternativa e seu fornecedor
normalizado. A alternativa simples `forage` consulta `forage`, sem encontrar o
bloqueio armazenado em `forage_meal`. Por isso uma tentativa equivalente passa.
O efeito é uma tentativa redundante; não se demonstrou que evitar essa tentativa,
isoladamente, salvaria a personagem, pois a coleta realmente estava esgotada.

Melhoria limitada sugerida: quando falhar a aquisição da cadeia composta,
registrar o bloqueio no fornecedor base e reutilizá-lo em ambas as formas.
Distinguir falha de aquisição de falha posterior de consumo antes de aplicar
esse bloqueio. Validar em cenário composto, preservando as dez regressões.
Esta melhoria não altera automaticamente estoque, conhecimento ou mortalidade.

As linhas originais e a morte estão em `evidencia_falha_alias.json`, extraídas
sem reexecutar escolhas de `curta_nova/decisoes.jsonl.gz` e `resumo.json`.
