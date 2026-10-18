# Simulador procedural — estado atual 6.0

Jogo de terminal em português, Python 3.11+, somente biblioteca padrão.
Regras e saves: `mvp-14-fase6.0`; geração: `mvp-6.0`.

```bash
python3 -m procedural --seed Dovha --nome Viajante
python3 -m procedural --seed MinhaSeed --simular 100 --salvar campanha.json
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
```

No terminal, `ajuda` lista os comandos. Movimento/ações válidas consomem horas;
consultas e ações inválidas não avançam o mundo. Salvar/carregar inclui RNG e estado tipado; versões incompatíveis são recusadas.
Eventos e Facts são snapshots. A observabilidade V1 separa história do mundo, decisões privadas e aprendizagem. Saves anteriores ao formato 2 são incompatíveis; não há migração automática.

- [Fase 6.0](FASE_6_0.md): aprofundamento, controles, métricas e campanha.
- [Coerência](COERENCIA.md), [decisões reais](DECISOES_6.md) e [balanceamento](BALANCEAMENTO.md).
- [Fase 5.5.5](FASE_5_5_5.md): baseline de correções e observabilidade.
- [PROJECT.md](PROJECT.md): arquitetura, modelos, fórmulas, sistemas, arquivos e testes.
- [Radiografia total](reports/auditoria_total/RADIOGRAFIA_TOTAL.md): auditoria integral, decisões reais e observabilidade.
- [Relatório de coesão](reports/diagnostico_coesao/RELATORIO_COESAO.md): campanha diagnóstica nova de 300h.
- [LIMPEZA.md](LIMPEZA.md): o que foi retirado e preservado.
- Referência anterior Vaelora-55: [técnico](reports/fase_5_5/RELATORIO_TECNICO.md),
  [mundo](reports/fase_5_5/MUNDO.md), [histórias](reports/fase_5_5/HISTORIAS_REAIS.md).

Na Limpeza Intuitiva anterior, a única mudança no núcleo foi a correção de crash em `Geography.emit`, autorizada pelo usuário e
registrada no relatório e manifesto. O histórico de fontes/documentos retirados da árvore está no
Git local. Relatórios antigos podem citar evidências e saves já removidos pela
retenção; os três Markdown de Vaelora-55 são a baseline documental preservada.

Configuração histórica por API: `generate_world(..., historical_trace_level="OFF" | "NORMAL" | "AUDIT")`. O padrão é `NORMAL`. Na Fase 6.0, infraestrutura inicial usa o censo final; há tarefas institucionais e observabilidade V1.1. Fisiologia, dano e thresholds raros foram preservados. Save format2 continua, mas outra rules_version é recusada.
