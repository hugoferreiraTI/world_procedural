# Correções do núcleo — mvp-2

Executado em 7 de outubro de 2026, Python 3.12.3, somente biblioteca padrão.
O escopo segue o texto anexado. A materialização de habitantes e a reposição
profissional foram adiadas pela instrução direta de alterar a população abstrata depois.
A regra existente de população, consumo e renda foi preservada; sua fonte monetária
agora é contabilizada para auditoria.

## Causas e correções dos 11 problemas

| Problema | Causa raiz | Resultado |
|---|---|---|
| Descanso anulava inanição | Cura do jogador e NPCs não consultava privação; jogador recuperava mais que o dano | Fisiologia compartilhada: cura reduzida em estado severo, bloqueada no crítico, dano crescente em inanição |
| Compra e revenda geravam lucro | Lote comprado a preço constante; revenda calculada depois de retirar estoque, em outro ponto da curva | Valor, compra e venda separados; preço marginal por unidade e curva inversa com spread |
| Cidade sem profissionais apesar da população | População contábil não materializa trabalhadores, nem repõe mortos | PENDENTE: aguarda a alteração populacional do usuário |
| Economia apagava crise sucessória | Um campo era escrito por dois domínios | Estados político, econômico, militar e social independentes; resumo somente para leitura |
| Mesmo favor era contabilizado novamente | Deduplicação dependia apenas de conhecimento curto, sujeito a expulsão | Registro persistente de contribuição por EventID, inclusive após load e esquecimento |
| Rumor e testemunho tinham o mesmo peso e interpretação | Quantidade fixa por tipo de evento, ignorando certeza e observador | Fontes com pesos 1 / 0,8 / 0,6 / 0,3 / 0,1; urgência, personalidade, relações e filiação interpretam o fato |
| Confiança podia ser farmada | Conversa e qualquer presente davam bônus fixos | Conversa aumenta familiaridade; ajuda só vale socialmente quando atende carência real; presentes extras sem carência não dão o mesmo bônus |
| NPC excluía o jogador da ajuda | Filtro removia explicitamente a entidade do jogador | Conhecidos presentes competem por confiança, reputação e contexto; pedido autônomo gera quest e espera a decisão humana |
| Boa reputação pouco mudava ações | Dados sociais estavam desconectados da utilidade e da aceitação de ajuda | Reputação altera seleção de interlocutor e disposição de alimentar quem pede |
| Recusa não tinha consequência social | Alterava apenas o status da quest | Evento PlayerRefusedRequest interpretado por urgência, expectativa, persistência, compaixão e incapacidade observável |
| Fome do jogador dependia do mercado | Comandos não expunham soluções já disponíveis ao motor | Comprar, coletar, trabalhar por alimento e pedir comida; execução comum a jogador/NPC |

## Mudanças arquiteturais

`rules.py` reúne faixas fisiológicas, pesos sociais, confiabilidade e variação entre
opções próximas. `social.py` concentra considerações sociais e interpretação;
`utility.py` avalia componentes normalizados. A escolha usa exclusivamente o RNG
existente e preserva objetivos em andamento quando continuam razoáveis.

O registro `Character.applied_facts` guarda a contribuição aplicada por fato.
Evidência mais forte acrescenta apenas a diferença: rumor e testemunho do mesmo
feito não se tornam dois favores. Memória curta permanece limitada a 32 registros
e conhecimento a 64; o registro de idempotência é persistente.

Uma quest pendente tem intervalo antes de novo pedido ao mesmo jogador; o NPC
continua tentando trabalhar ou coletar. O debug opcional guarda necessidade,
prioridade, candidatos, alvo, pontuação e considerações da última decisão.
Pedidos registram origem autônoma ou conversa para facilitar auditoria.

A correção de fisiologia expôs viagens repetidas para beber como causa de dano
acumulado. Os poços já existentes nas casas e na área rural passaram a ser opções
conhecidas, usando o mesmo estoque físico de água da cidade.

Economia: renda abstrata é Source explícita e contabilizada; compras, salários,
multas e subsídios são Transfer; consumo é Sink de bens; trigo transformado em
rações é Converter. Trabalho avulso reutiliza a proporção de cozinha 2 trigo →
3 rações: 2 para a cidade e 1 como pagamento. Não cria moeda.

A versão é `mvp-2`; saves `mvp-1` são recusados por incompatibilidade. Como a versão
participa da seed, a geografia também muda: números antigos não são comparações
controladas de um mundo idêntico. Os relatórios antigos foram preservados.

## Arquivos alterados e adicionados

- Dados e infraestrutura: `procedural/models.py`, `events.py`, `validation.py`, `__init__.py`.
- Regras e decisões: `needs.py`, `goals.py`, novos `rules.py`, `utility.py`, `social.py`.
- Economia e política: `economy.py`, `professions.py`, `politics.py`.
- Percepção e interação: `knowledge.py`, `quests.py`, `engine.py`, `navigation.py`, `generation.py`, `ui.py`.
- Regressões: novo `tests/test_hardening.py`; testes anteriores preservados.
- Experimentos: novos `experiments/hardening_validation.py` e `survival_campaign.py`.
- Documentação: `README.md`, identificação histórica em `VALIDACAO.md`, este relatório e evidências em `reports/hardening/`.

## Testes automatizados

43 testes passaram, sendo 18 anteriores e 25 novos. A rodada inicial, antes das
correções, reproduziu dez problemas (nove falhas e ausência do novo estado político).
O teste de reposição populacional não foi implementado porque essa parte está adiada.

As regressões verificam privação tanto do jogador quanto de NPCs; revenda em lote
e em unidades; conservação de moeda; estado político preservado; fato que retorna
após sair da memória; atualização de certeza sem duplicação, inclusive após save;
fontes com confiabilidade distinta; interpretação oposta de uma morte; conversa,
presentes úteis e irrelevantes; pedido recebido durante `esperar`, sem conversa;
concorrência com outro NPC; pedido pendente sem bloquear alternativas; reputação
mudando a aceitação de ajuda; recusa contextual; limites materiais das alternativas
de fome; observabilidade sem alterar RNG; conhecimento de estoque apenas local.

```bash
python3 -m unittest discover -s tests -v
```

Saída integral: [testes.txt](reports/hardening/testes.txt).

## Simulações completas

Três mundos com seis reinos foram executados até 10.000 turnos adicionais,
verificados nos checkpoints de 1.000, 5.000 e 10.000. A coluna moeda é a renda
abstrata legítima acumulada desde o início da campanha. Incluímos dinheiro de
mortos no balanço: morte não destrói automaticamente a carteira.

| Seed | Turnos | NPCs vivos / iniciais | Cidades/vilas sem NPC local vivo | Moeda criada pela fonte registrada | Balanço / invariantes |
|---|---:|---:|---:|---:|---|
| Dovha | 1.000 | 334/416 | 3 | 24.477 | Exato / válidos |
| Dovha | 5.000 | 308/416 | 3 | 124.176 | Exato / válidos |
| Dovha | 10.000 | 305/416 | 3 | 248.352 | Exato / válidos |
| Mira | 1.000 | 366/456 | 3 | 25.379 | Exato / válidos |
| Mira | 5.000 | 324/456 | 4 | 128.752 | Exato / válidos |
| Mira | 10.000 | 323/456 | 4 | 257.504 | Exato / válidos |
| Arven | 1.000 | 372/444 | 1 | 23.903 | Exato / válidos |
| Arven | 5.000 | 347/444 | 2 | 121.264 | Exato / válidos |
| Arven | 10.000 | 342/444 | 2 | 242.528 | Exato / válidos |

Nenhuma exceção nem divergência monetária ocorreu. Em todos os checkpoints,
moeda final = moeda inicial + renda explicitamente registrada. IDs, referências,
inventários, limites fisiológicos, memória, reputação e estados políticos passaram.

Ao final, Dovha e Mira tinham os seis reinos em crise sucessória; Arven tinha cinco
em crise sucessória e um com governante. Todos tinham os seis reinos em crise
econômica. Os dois fatos coexistem e o sistema econômico não apagou a sucessão.

Dados reproduzíveis e exemplos de decisões:
[dovha.json](reports/hardening/dovha.json),
[mira.json](reports/hardening/mira.json),
[arven.json](reports/hardening/arven.json).

## Campanha pelos comandos do jogador

A política automática usou apenas comandos públicos e estado/locais conhecidos
pelo próprio jogador, sem teleporte ou alterações diretas de atributos. Ficou
principalmente na área rural da primeira capital; não representa exploração
completa nem comportamento humano. Resultados e ações estão em
[jogador.json](reports/hardening/jogador.json) e
[jogador_acoes.jsonl](reports/hardening/jogador_acoes.jsonl).

Completou **10.000 ações/horas** (equivalente à campanha anterior),
terminando vivo com vida **100**, fome **40**, sede **20** e
**25 moedas**. Houve **499 refeições**, **1.431 coletas**,
**995 descansos** e **0 curas por descanso em inanição**.
A sobrevivência decorreu da alimentação real. Trabalho por comida e pedido a NPC
foram exercitados com sucesso nos testes; essa política não precisou recorrer a eles.

Foram **10 contatos**, **933 entregas**, sete pedidos recebidos,
**5 quests concluídas** e **2 resolvidas por outra solução.
As sete ofertas desta política vieram de conversas (origem registrada nos eventos);
a emissão autônoma foi comprovada em teste separado, durante espera sem conversar.
Presentes repetidos não equivalem a favores válidos: entregas sem carência não
concedem confiança. Esta campanha não provocou recusas; os testes verificam
recusa grave com ressentimento e recusa compreendida quando o jogador está ferido.


A aceitação dos pedidos depende também de uma decisão humana; o NPC não retira
comida do inventário do jogador automaticamente. O teste de espera comprova
emissão autônoma, separadamente da política da campanha.

## Problemas que permanecem

- Cidades com população contábil podem perder todos os NPCs locais simulados. A
  reposição e os critérios de população disponível continuam pendentes por decisão do usuário.
- Houve 111 mortes em Dovha, 133 em Mira e 102 em Arven. Dinastias continuam muito
  frágeis. Consumo abstrato, mão de obra, distribuição e produção precisam ser
  revistos junto com o modelo populacional; não foram escondidos por cura artificial.
- O teste comprova coerência das regras e execução longa, não equilíbrio final
  nem garantia de sobrevivência em todos os lugares e políticas possíveis.

## Dívida técnica

O registro por fato cresce com o número de acontecimentos socialmente relevantes;
os mundos terminaram com 10.589, 14.654 e 21.748 entradas no total. Compactar esse
registro exige preservar a prova de idempotência, e não simplesmente apagá-lo.
Interpretação atual permite reforçar evidência; retratação de notícias falsas,
reinterpretação geral da história e múltiplas fontes com conflito permanecem futuras.
A curva comercial ainda não tem transporte regional, custos reais de logística ou
balanço de comerciantes individuais. Poços compartilham o estoque municipal;
sua distribuição espacial é simplificada. Ações sociais usam encontro local e
sinais visíveis, sem busca de pessoas distantes. Guardas investigam o último local
conhecido e não executam perseguição completa. Não foi feita migração de saves antigos.

## Deliberadamente fora desta etapa

Materialização/reposição populacional; guerras e exércitos; combate completo;
deuses e intervenção divina; religião organizada; dinastias completas; notícias
falsas e retratação; mercados regionais com caravanas; descontos, abrigo e proteção
adicionais por reputação; interface nova; frameworks ou infraestrutura externa.
