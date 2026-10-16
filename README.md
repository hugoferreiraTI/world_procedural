# Simulador procedural — estado atual 5.5

Jogo de terminal em português, Python 3.11+, somente biblioteca padrão.
Regras e saves: `mvp-12-fase5.5`; geração: `mvp-5.4`.

```bash
python3 -m procedural --seed Dovha --nome Viajante
python3 -m procedural --seed MinhaSeed --simular 100 --salvar campanha.json
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=tests python3 -m unittest test_phase55 test_phase54
```

No terminal, `ajuda` lista os comandos. Movimento/ações válidas consomem horas;
consultas e ações inválidas não avançam o mundo. Salvar/carregar preserva RNG e
estado completo; versões incompatíveis são recusadas.

- [PROJECT.md](PROJECT.md): arquitetura, modelos, fórmulas, sistemas, arquivos e testes.
- [Relatório de coesão](reports/diagnostico_coesao/RELATORIO_COESAO.md): campanha diagnóstica nova de 300h.
- [LIMPEZA.md](LIMPEZA.md): o que foi retirado e preservado.
- Referência anterior Vaelora-55: [técnico](reports/fase_5_5/RELATORIO_TECNICO.md),
  [mundo](reports/fase_5_5/MUNDO.md), [histórias](reports/fase_5_5/HISTORIAS_REAIS.md).

A Limpeza Intuitiva não é uma nova fase e não rebalanceia o jogo. A única mudança
no núcleo foi a correção de crash em `Geography.emit`, autorizada pelo usuário e
registrada no relatório e manifesto. O histórico de fontes/documentos retirados da árvore está no
Git local. Relatórios antigos podem citar evidências e saves já removidos pela
retenção; os três Markdown de Vaelora-55 são a baseline documental preservada.
