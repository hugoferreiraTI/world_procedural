# Limpeza Intuitiva

Estado funcional preservado: **mvp-12-fase5.5**, geração **mvp-5.4**. Não é nova fase.

| Medida | Antes | Depois |
| --- | --- | --- |
| `project_size` | 741,581,971 bytes | 7,795,222 bytes (7.80 MB) |
| Arquivos na árvore de trabalho | 2897 | 84 |
| `reports_size` | 734,851,476 bytes | 6,391,721 bytes (6.39 MB) |

Medição: soma de bytes lógicos dos arquivos, excluindo `.git`. A pasta inicial não
possuía Git. O histórico local criado antes da limpeza permanece em `.git`, fora
dessa comparação. Após a primeira limpeza, antes da nova auditoria, havia
4.302.339 bytes incluindo o Git então existente. Os números acima incluem toda
a documentação e evidência compacta da entrega atual.

Maiores diretórios remanescentes:

- `reports/`: 6,391,721 bytes (6.39 MB).
- `procedural/`: 719,658 bytes (0.72 MB).
- `tests/`: 265,745 bytes (0.27 MB).
- `experiments/`: 160,022 bytes (0.16 MB).

Foram retirados 22 diretórios históricos de reports, incluindo fases 2, 3/3.x,
4/4.x, 5/5.x anteriores à 5.5, auditorias de 10.000h, campanhas Vespera e três
perspectivas. Também saíram 66 experimentos antigos, 37 Markdown históricos da
raiz, snapshots/baselines duplicados, caches, bytecode, saves e dumps regeneráveis.
No diretório da 5.5 ficaram somente os três Markdown finais de Vaelora-55.

Entre os maiores arquivos removidos estavam
`reports/fase_4/auditoria_global_10000h/resumo.json` (46,55 MB) e as crônicas JSONL
antigas de três perspectivas (12,01 e 10,54 MB). Os maiores diretórios antigos
incluíam `reports/fase_3_2/` (217,77 MB), `reports/fase_4_5/` (102,06 MB) e
`reports/fase_3/` (100,59 MB). A lista resumida e o inventário inicial estão em
`reports/diagnostico_coesao/manifesto.json`.

Preservados: os 64 arquivos atuais de núcleo/testes, `.gitignore`, especificações
`instruction.md` e `fase_5_5.md`, documentação operacional e os três relatórios de
Vaelora-55, estes com hashes originais conferidos. O projeto usa biblioteca padrão;
não havia assets externos ou lockfiles necessários a retirar. Não foram encontradas
referências de runtime/testes aos snapshots e experimentos antigos removidos.

A única exceção no núcleo foi autorizada pelo usuário: duas linhas em
`procedural/geography.py`, renomeando o parâmetro de `Geography.emit` para evitar
colisão com `kind` do contexto. Nenhum teste, regra de decisão ou balanceamento foi
alterado. Os demais bugs encontrados foram apenas documentados.

O commit `c996d8c095f67479d36b43b9ddcbdf63420f4d39` preserva fontes e Markdown anteriores à limpeza,
sem saves/caches/dumps. A correção autorizada está em
`0b7bb14bc9a9130fb2041b46596bfce91ce0c614`. Não há envio remoto.

A campanha nova **Neravon-Coesao55** completou 300h naturais, sem jogador, com 12
verificações estruturais e auditoria de rotas sem erros. Passaram 28 testes
selecionados. O save de **204.986.245 bytes** foi removido depois de produzir e
auditar o relatório; sua assinatura e confirmação de remoção estão no manifesto.
A regeneração do relatório sem o save foi conferida byte a byte antes dos últimos
ajustes de apresentação. Pequenos controles, reproduções e falhas anteriores
foram consolidados no manifesto; não se mantiveram dumps completos.

`reports/` agora possui apenas `fase_5_5/` e `diagnostico_coesao/`. As referências
centrais são [PROJECT.md](PROJECT.md) e
[RELATORIO_COESAO.md](reports/diagnostico_coesao/RELATORIO_COESAO.md).
