"""Gera os três relatórios a partir da campanha já concluída, sem simular horas."""
import hashlib
import json
from collections import Counter
from pathlib import Path
import shutil

BASE = Path(__file__).resolve().parents[1]
OUT = BASE / 'reports/fase_5_4'
DATA = OUT / 'campanha_200h'

def main():
    r = json.loads((DATA / 'resultado.json').read_text())
    events = json.loads((DATA / 'eventos_espaciais.json').read_text())
    extra = json.loads((DATA / 'campos_para_relatorios.json').read_text())
    chars = r['characters']
    towns = {t['id']: t for t in r['final']}
    places = {**{i: t['name'] for i, t in towns.items()}, **{p['id']: p['name'] for p in r['points']}}
    factions = {f['id']: f for f in r['factions']}
    gods = {g['id']: g for g in r['gods']}
    groups = {g['id']: g for g in r['groups']}
    def person(id):
        c = chars.get(str(id))
        return f"{c['name']} (NPC {id})" + (' †' if not c['alive'] else '') if c else f'NPC {id}'
    def place(id):
        return f'{places.get(id, "Lugar")} ({id})'
    def inv(inventory):
        return ', '.join(f"{n} × {extra['items'].get(str(id), {}).get('name', 'item '+str(id))}" for id,n in inventory.items()) or 'vazio'
    def table(headers, rows):
        return '\n'.join(['| ' + ' | '.join(headers) + ' |', '| ' + ' | '.join(['---']*len(headers)) + ' |'] + ['| ' + ' | '.join(str(v).replace('|','/') for v in row) + ' |' for row in rows]) + '\n\n'
    def refs(ids):
        selected = [e for e in events if e['id'] in ids]
        assert len(selected) == len(ids), (ids, selected)
        return 'Registros: ' + '; '.join(f"{e['kind']} #{e['id']} (h{e['turn']})" for e in selected) + '.'
    def write(name, text):
        (OUT / name).write_text(text, encoding='utf-8')
    labels = {'capital':'capital','cidade':'cidade','vila':'vila','active':'ativo',
              'dissolved':'dissolvido','security':'segurança','resource_pressure':'recursos',
              'hunters':'caçadores','mercenaries':'mercenários','justice':'justiça',
              'knowledge':'conhecimento','protection':'proteção','road':'estrada','trail':'trilha',
              'offered':'convite oferecido','rejected':'recusado','delayed':'adiado',
              'accepted':'aceito','conditional':'condicional','draft':'rascunho',
              'submitted':'entregue','partial':'parcial','deferred':'adiado',
              'threat':'ameaça','wanted':'perseguição judicial','family':'família',
              'divine_contact':'contato divino','organizational_access':'contato organizacional',
              'organizational_survival':'sobrevivência organizacional','response':'resposta',
              'arms_funding':'financiar armamento','security_funding':'financiar segurança',
              'food_aid':'auxílio alimentar','work_offer':'oferta de trabalho',
              'Coldness':'Frieza','Heroism':'Heroísmo','Justice':'Justiça'}
    def label(value):
        return labels.get(value,value)

    initial_named = sum(t['named'] for t in r['initial'])
    alive = sum(c['alive'] for c in chars.values())
    initial_abstract = sum(t['abstract'] for t in r['initial'])
    final_abstract = sum(t['abstract'] for t in r['final'])
    known = Counter()
    for route in r['routes']:
        known[route['origin']] += 1
        known[route['destination']] += 1
    submissions = {e['target_id'] for e in events if e['kind']=='ProposalSubmitted'}
    decisions = [e for e in events if e['kind']=='PolicyDecided']
    positive_favor = {}
    for god in r['gods']:
        for id,record in god['affinities'].items():
            if record['value'] > 0:
                positive_favor.setdefault(int(id), []).append((god['name'],record['value'],record['deeds']))
    invited = {int(id) for f in r['factions'] for id in f['norms'].get('invitations',{}) if f['norms']['invitations'][id].get('inviter')==f['leader_id']}
    # Um pedido espontâneo também cria registro; ele não conta como convite entregue.
    invited = {e['context']['candidate'] for e in events if e['kind']=='FactionInvite'}

    tech = '''# RELATÓRIO TÉCNICO — Fase 5.4

## Resultado e alcance

A Fase 5.4 foi adaptada ao motor existente. A geração padrão passa a quatro reinos, com capital, quatro outras cidades e seis a oito vilas por reino. Conhecer o destino já não autoriza uma viagem entre localidades: o agente precisa das conexões, de condição física e de mantimentos reais, ou acompanhar um guia presente.

Campanha natural: **Arandor-54**, criada do zero, sem jogador, **200 horas**, regras `mvp-11-fase5.4`. O limite de 200 horas segue o pedido mais recente do usuário, prevalecendo sobre as 350 horas sugeridas no documento. Não houve seleção de seeds para produzir resultados desejados. Esta campanha mostra integração e comportamentos de curto/médio prazo; não demonstra equilíbrio econômico ou raridade em milhares de horas.

## Arquitetura preservada

Os dados continuam em dataclasses de `models`; o `Engine` coordena serviços; decisões seguem Need → alternativas → Utility → Goal → ação. Navegação, índice espacial, eventos, conhecimento, itens, sociedade, fé e JSON continuam sendo os mesmos serviços do projeto. Foram adicionados `geography.py` e `access.py`, ligados a esse fluxo, sem outro motor de agentes, sistema de combate ou arquitetura de persistência.

`Route`, `RouteKnowledge`, `Journey` e `DivineContract` são dados persistentes. Novos campos de personagem e POI usam o serializador existente. A versão de geração mudou: saves anteriores são recusados pelo mecanismo de versão já existente. O snapshot do código anterior foi preservado em `baseline_code/procedural/`.

## Comparativo com o documento

'''
    tech += table(['Sistema','Entrega','Limite real'], [
        ['Escala e densidade','4 reinos; 1 capital + 4 cidades; 6–8 vilas subordinadas; capitais maiores','Abastecimento herdado ainda tem capacidade fixa por localidade.'],
        ['Grafo e memória de rotas','Conexões persistentes, fonte/confiança/datas; planejamento só no grafo pessoal','Estradas/trilhas simples; terreno usa classificação resumida. Não há formação dinâmica de redes comerciais.'],
        ['Destino, rumor e localização','Conhecimento de lugar separado da rota; relato remoto pode conservar coordenadas desconhecidas','Rumores de POI dependem de fatos e contatos reais; não há emissor artificial para garantir descobertas.'],
        ['Instruções','Perguntar presencialmente; interlocutor usa suas próprias conexões; confiança insuficiente não libera viagem','Mapas como objetos negociáveis e contratação remunerada de guias continuam pendentes.'],
        ['Viagem e multietapas','Saída pelo portão, caminho externo, entrada e conexões; alimento/água/dinheiro reais; seguir/escoltar guia','Exploração deliberada de estradas desconhecidas ainda não é alternativa autônoma; seguir/escoltar exige guia que já tenha viagem válida.'],
        ['Migração e buscas','Migração, pistas remotas, proteção, ordens e representações usam o acesso conhecido','Sem rota, a ação pode pedir informação ou visitar um ponto intermediário conhecido. Isso não garante conseguir a informação.'],
        ['POIs e cavernas','Estoque finito, minério/item incomum, risco físico, abrigo, restos e história; estados de lugar por personagem','Exploração é uma ação resumida. Profundidade/áreas são dados, sem percurso por câmaras. Propriedades especiais de ferramentas não ganharam cadeia produtiva própria.'],
        ['Expedições e ocupação','Grupo existente temporário, companheiros presentes, aprendizado ao acompanhar; ocupação com companhia e capacidade','Negociação/disputa longa, aluguel e construção de sede ficam para depois. Reivindicação não é propriedade legal.'],
        ['Facções e adesão','Conhecimento por contato; interesse por poucos membros/recursos; convite, pedido, aceite, recusa, adiamento ou condição','Critérios usam sobretudo profissão/coragem/ambição/necessidade/independência. Serviço condicional e retomada do adiamento não têm ciclo completo.'],
        ['Organização e recursos','Formalização de Group duradouro reutiliza Society; contribuições e estoque usam transferências reais','Não foram criadas todas as estratégias possíveis de financiamento ou logística de comércio entre cidades.'],
        ['Contato divino','Busca por motivo pessoal, local conhecido, viagem, rito; audiência exige favor, canal válido, presença e energia','Alcançar o rito não obriga resposta. Pactos oferecidos são do tipo proteção em troca de proteção a uma pessoa.'],
        ['Pactos e manifestação','Aceitar/recusar/abandonar; conhecimento divino do descumprimento por canal válido; manifestação física temporária com custo','Não há ritual de manifestação forçada, nem objetivo automático de caçar deuses. Presença invisível continua sem acesso físico.'],
        ['Morte divina','Morte exige manifestação física alcançável; apoteose não decorre automaticamente da morte','Essência, fragmentos e caminhos excepcionais de ascensão continuam sob regras existentes.'],
    ])
    tech += '''## Validação curta

**14 testes passaram**: dez métodos novos da Fase 5.4 e quatro regressões críticas de alimentação/letalidade. Os novos métodos cobrem: destino sem rota e JSON; instruções e deslocamento; multietapas sem aresta desconhecida; seguir e escoltar com aprendizado posterior; rumor de POI sem rota; contato e aceitação para adesão; formalização sem moeda criada; ocupação e conservação de estoque, exploração e retorno; contato sem resposta obrigatória/pacto opcional; deus invisível versus manifestação física, sem ascensão automática.

Os cenários controlados alteram condições para verificar regras. Adesão, ocupação, exploração e pacto demonstrados nesses testes **não são acontecimentos naturais de Arandor-54**. Também houve uma verificação pequena de 48 horas com 69 NPCs. Não foi executada a suíte histórica completa nem outra campanha longa.

### Interrupção e correções

A primeira tentativa natural com esta mesma seed parou na hora 100: o NPC 2290 ultrapassou o limite de 64 observações ao receber notícia de localização entre decisões. A poda existia na atualização periódica, mas faltava no ponto de inserção do fato. A poda foi centralizada e aplicada imediatamente; a regressão está no teste 1. A evidência da interrupção foi preservada em `tentativa_interrompida_100h/`. Houve **um reinício da mesma seed**, por essa falha estrutural, sem trocar resultados naturais.

Na integração curta também foram corrigidos o cálculo de utilidade com proxies coletivos sem campo `devotion`, a conservação de coordenadas já conhecidas após rumor mais fraco e a conclusão de chegada acompanhando guia. Após a campanha concluída, o cenário controlado de exploração motivou dois ajustes pequenos: criar intenção de retorno ao lar e reconhecer corretamente “explorado na hora 0”. Os 14 testes passaram novamente. Não houve exploração natural na campanha, portanto nenhum episódio reportado depende desses ajustes posteriores. Os hashes do código da campanha e da entrega ficam separados no manifesto de entrega.

## Campanha natural: acontecimentos observados

'''
    metric_rows = [
        ['NPCs no início / vivos no fim',f'{initial_named} / {alive}'],
        ['Reinos / localidades / POIs / conexões',f"4 / 45 / 8 / {len(r['routes'])}"],
        ['Viagens iniciadas / concluídas / ainda registradas',f"{r['events']['JourneyStarted']} / {r['events']['JourneyArrived']} / {len(r['traveling'])}"],
        ['Trechos efetivamente atravessados',r['events']['RouteTraversed']],
        ['Viagens com várias conexões',r['events']['MultiHopJourney']],
        ['Pedidos de rota / transmissões / destinatários distintos',f"128 / 5 / {len({e['target_id'] for e in events if e['kind']=='RouteKnowledgeShared'})}"],
        ['Registros de rota criada ou melhorada depois da geração',r['events']['RouteKnowledgeCreated']],
        ['Bloqueios registrados / pessoas distintas bloqueadas',f"115 / {len({e['actor_id'] for e in events if e['kind']=='RouteUnknownBlockedTravel'})}"],
        ['Migrações iniciadas / mudanças de residência concluídas','28 / 25'],
        ['Conhecimento organizacional novo / convites / novos membros','230 / 22 / 0'],
        ['Pedido espontâneo de adesão / recusas ou adiamentos respondidos','1 / 2'],
        ['Grupos formados / propostas criadas / entregues / decididas','179 / 87 / 32 / 12'],
        ['Intenções de contato divino / viagens religiosas / ritos alcançados','157 / 18 / 8'],
        ['Audiências / pactos / manifestações físicas','0 / 0 / 0'],
        ['Novas visitas, explorações, expedições ou ocupações de POI','0'],
        ['Seguir/escoltar em campanha natural','0'],
    ]
    tech += table(['Medida','Resultado'],metric_rows)
    tech += '''A contagem separa geração e campanha: por exemplo, os 5.256 registros iniciais de conhecimento de rotas não são aprendizado durante as 200 horas. Um evento é uma ocorrência, e não uma pessoa nova. As 157 intenções religiosas também não são 157 respostas de deuses.

Houve validação do estado a cada 25 horas, em **oito checkpoints sem erros**, e auditoria dos registros de partida sem violações de conexões conhecidas ou reservas mínimas. Essa auditoria verifica o conhecimento apresentado e a reserva na partida; não demonstra que toda viagem terminou, que a estimativa suportou todas as interrupções ou que toda movimentação possível do motor foi coberta. As regras não foram alteradas durante a execução. Tempo de simulação: 227,12 segundos; save final: aproximadamente 152 MiB.

## Problemas e limites observados

1. **Abastecimento de água inadequado à nova densidade.** Das 133 mortes, 92 foram classificadas como sede, 32 como fome, oito como privação combinada e uma como combate. A sede responde por 69,2%; todas as privações somam 99,2%. A classificação é a dos registros de morte, não uma prova de causa exclusiva durante toda a vida. Noventa e uma das mortes por sede ocorreram nas quatro capitais. Os registros incluem NPCs com zero água, objetivo `fill_water` e distância zero ao ponto de água: chegar ao poço não assegurou obter água.

   `Economy.daily()` mantém reposição de até 80 unidades/dia e limite de estoque 160 em qualquer localidade. Uma capital nasce com 104 NPCs. Como referência, sede de 2/h e redução de 45 por unidade exigem cerca de 111 unidades/dia para esses NPCs, mesmo sem o agravamento do deserto. Esse cálculo explica a incompatibilidade de capacidade, mas não substitui medir filas, interrupções, distribuição e deslocamentos. Não foi alterada a fisiologia nem criada água para melhorar os resultados. Próximo ajuste recomendado: capacidade material de abastecimento proporcional à população e infraestrutura, conservando estoque e custo, com diagnóstico da distribuição.

2. **Contato organizacional cresceu, adesão natural não.** Houve 22 convites a 22 pessoas, mas nenhuma aceitação; 21 registros permanecem oferecidos, um foi recusado, e o pedido espontâneo de Lyra Corven foi adiado. A prioridade da resposta compete com sobrevivência e exige reencontro com o líder. A Irmandade de Nordor acabou dissolvida após a morte de Elena. Isso prova contato causal e dificuldade concreta; não prova que o gargalo de crescimento das facções foi resolvido. Adiamento e condição precisam de continuação executável, em vez de encerrar a primeira resposta.

3. **POIs funcionam nos cenários controlados, mas não alimentaram histórias naturais.** Esta seed possui seis cavernas, nenhuma ruína de castelo. Ninguém novo visitou ou explorou esses lugares. Um detalhe da inicialização ajuda a explicar: a regra geral de morador de vila é aplicada antes da especialização profissional, ensinando sobretudo a ligação à autoridade; o caçador da vila pode não conhecer a trilha local da caverna. Rumor e rota não surgem sem fonte. Vale melhorar conhecimento local justificado de profissões e observação física de trilhas, sem distribuir todos os POIs ao mundo. Ainda não existe exploração autônoma de estrada desconhecida.

4. **Continuidade de viagem ainda disputa prioridade.** Nove viagens permanecem registradas no fim. Algumas começaram perto da hora 200; outras estão antigas: Cael Montes começou a viagem com duas conexões na hora 55 e só concluiu o primeiro trecho; Bela Bruma iniciou outra na hora 170 e não concluiu o retorno intermediário. Deslocar-se até um posto conhecido para perguntar sobre destino distante também pode produzir desvios longos. É necessário distinguir pausa fisiológica legítima de estagnação, registrar a barreira atual e revisar a escolha de pontos intermediários. O prazo nominal da estrada não é a duração final do personagem.

5. **Atividade coletiva repetitiva.** Dos 179 grupos, 177 são de segurança e apenas dois de recursos. Só 12 das 87 propostas foram decididas. A densidade gera encontros e mobilização, mas muitos grupos locais tratam causas parecidas; esses números não equivalem a 179 enredos independentes. A política e a sobrevivência herdadas ainda restringem a variedade.

6. **Religião permaneceu em busca e rito.** Oito contatos alcançaram o local; não houve audiência, pacto ou manifestação. Os requisitos de favor/devoção/canal/energia não foram reduzidos para produzir cenas. O resultado de 200 horas não permite concluir que eventos raros jamais acontecerão, mas também não valida sua frequência natural.

7. **Escopo parcial explicitado.** Permanecem sem ciclo completo: mapas negociáveis, guias contratados, exploração de estrada desconhecida, serviço exigido na adesão, retomada de decisões adiadas e logística material entre localidades. Perigo da estrada é custo/avaliação e histórico de fatos reais, sem ataques aleatórios inseridos por esta fase. Itens e áreas de caverna persistem, mas não há dungeon ou novo sistema artesanal. Ritual de manifestação forçada é extensão futura expressamente permitida pelo documento.

## Avaliação

A geografia agora interfere em migração, busca, organização e religião; a viagem pode falhar por desconhecimento e aprender com pessoa identificada. Os dois casos de instrução fraca seguida de instrução confiável são o melhor resultado narrativo desta fase. Contudo, a campanha não justifica declarar sobrevivência sustentável, crescimento natural de facções ou exploração emergente resolvidos. A próxima intervenção útil é estabilizar água e continuidade de acesso/adesão antes de expandir sistemas maiores.

## Evidência preservada

- `campanha_200h/resultado.json`: censos, contadores, entidades e oito verificações.
- `campanha_200h/eventos_espaciais.json`: eventos identificados usados nas histórias.
- `campanha_200h/save_final.json`: estado completo na hora 200.
- `campanha_200h/manifesto.json`: seed, versão, censo inicial e hash de código da campanha.
- `testes_14.log` e `tests/test_phase54.py`: execução e cenários controlados.
- `tentativa_interrompida_100h/`: falha preservada da primeira tentativa.
- `ENTREGA_FINAL.json`: hashes e pequenos ajustes posteriores à campanha.
'''
    write('RELATORIO_TECNICO.md',tech)

    lore = '''# HISTÓRIAS REAIS — Arandor-54

Campanha de espectador, iniciada do zero e encerrada na hora **200**. As oito trajetórias abaixo foram reconstruídas de eventos reais. Os nomes dos lugares podem se repetir; os números distinguem localidades e pessoas. † indica falecimento ao fim da campanha. Não foram inventados diálogos, descobertas, pactos, motivos psicológicos ou conclusões de viagem.

## 1. Elena aprende o caminho de volta antes de perder a irmandade

Elena Arven (NPC 1075) liderava a **Irmandade de Nordor**, instalada no Quartel-general de Arria (1072). Sua organização precisava de pessoas e recursos. Ela não conhecia uma sequência completa até Dorven (3): primeiro saiu pela trilha conhecida para Arthon (32), na hora 6, chegando na hora 20.

Na hora 22, perguntou pela rota de Dorven. **Marie Corven (1393)** transmitiu instruções com confiança 45, insuficiente para partir. Na hora 24, o guarda **Silas Stone (1395)** ensinou a mesma conexão com confiança 80. Só então Elena iniciou a viagem à capital, na hora 25, e concluiu a chegada na hora 45. A estrada já existia; a diferença foi adquirir informação utilizável.

Elena entregou 15 convites presenciais ao longo da campanha. Nenhum gerou ingresso. Morreu por privação na hora 186, em Dorven; a irmandade terminou dissolvida, sem membros. A história conectou isolamento, informação, deslocamento, tentativa de crescimento e perda de continuidade organizacional.

'''
    lore += refs([26750,47811,50248,52419,53356,72645,216714])+'\n\n'
    lore += '''## 2. Bela descobre uma ligação, mas ainda não alcança o deus

**Bela Corven (3281)**, comerciante de Karria (483), queria contato religioso em Silvia (266). A intenção não lhe deu uma rota completa. Na hora 71, viajou por uma conexão já conhecida até Valmir (454), onde chegou na hora 79, procurando continuar a busca por informações.

Na hora 81, o comerciante **Silas Valerius (475)** ofereceu instruções para Silvia com confiança 45. Na hora 83, o guarda **Aldren Valerius (3110)** elevou a informação para 80. Houve progresso real de conhecimento, mas os registros desta campanha não mostram uma nova partida de Bela até Silvia nem o rito final. Ao encerrar, ela continuava viva. Saber mais abriu uma possibilidade, sem garantir executá-la.

'''
    lore += refs([97908,106645,108445,110086])+'\n\n'
    lore += '''## 3. Cael faz uma peregrinação em duas conexões e fica pelo caminho

O guarda **Cael Montes (4796)** conhecia estradas por sua vida profissional. Saiu de Elithon (857) na hora 17, movido por busca de contato divino, e chegou à capital Elilen (810) na hora 42.

Na hora 55, iniciou uma viagem com duas conexões: **Elilen → Elithon → Arven (886)**. Ele possuía conhecimento próprio das duas estradas e partiu com três unidades de alimento e duas de água. A duração estimada era 35 horas, sem assegurar todas as pausas pessoais.

Na hora 86, atravessou o primeiro trecho, voltando a Elithon. Até a hora 200, não apareceu a conclusão até Arven: sua viagem ainda estava registrada no segundo trecho. Não houve acesso ritual registrado para Cael. O mundo produziu uma busca prolongada, cuja resolução permanece aberta.

'''
    lore += refs([44594,70537,83823,83824,112896])+'\n\n'
    lore += '''## 4. Bela Bruma prepara uma jornada maior que o tempo restante

A guarda **Bela Bruma (4626)** saiu de Elilen (810) para Elithon (857) na hora 21, também buscando contato religioso. Concluiu essa viagem na hora 48.

Na hora 170, iniciou outro itinerário: **Elithon → Elilen → Elivia (969)**. As duas conexões estavam em sua memória antes da partida. Levava sete unidades de alimento e três de água; a estimativa era 54 horas, enquanto restavam apenas 30 horas de observação.

O fim da campanha não é o fim de sua intenção: não há chegada a Elivia registrada. Bela continuava viva e a jornada permanecia no primeiro trecho. A peregrinação não foi resumida a um evento imediato de “chegou ao templo”.

'''
    lore += refs([49859,75915,201783,201784])+'\n\n'
    lore += '''## 5. Lyra chega ao rito, depois procura uma companhia

**Lyra Corven (2952)**, cozinheira de Silven (407), partiu para Silvia (266) na hora 17, por uma estrada conhecida de sua vida local. Chegou na hora 33. Na hora 56, alcançou o ponto de contato com **Aurion** e realizou o rito. Não houve audiência, pacto ou manifestação divina; alcançar o lugar encerrou a etapa de acesso, sem obrigar uma resposta excepcional.

Mais tarde, Lyra passou a buscar aproximação da **Companhia de Silthon**. Na hora 108 perguntou sobre o acesso ao quartel. Na hora 115 fez um pedido de adesão presencial ao líder **Aldren Valerius (1083)**. A resposta foi adiar, por condição física/fadiga, sem ingressar. Lyra terminou viva, ainda registrada como moradora de Silven: visitar Silvia não mudou automaticamente sua residência.

'''
    lore += refs([44147,61552,84517,134280,140833])+'\n\n'
    lore += '''## 6. Aldren encontra candidatos; a companhia continua com um só membro

O caçador **Aldren Valerius (1083)** começou na sede da **Companhia de Silthon**, o Quartel-general de Silmir (1080). Na hora 2 iniciou viagem por sua trilha conhecida até Silvia, concluída na hora 14. Sua procura organizacional precisava encontrar pessoas onde elas de fato estavam.

Entre as horas 19 e 92, entregou sete convites presenciais. Um destinatário, **Ruan Douran (307)**, recusou; os seis outros registros ficaram oferecidos. O pedido espontâneo de Lyra, na hora 115, foi adiado. Aldren sobreviveu, mas a companhia terminou com ele como único membro ativo e sem moedas institucionais. Houve tentativa concreta de organização, sem expansão consumada.

'''
    lore += refs([19659,38854,140833])+'\n\n'
    lore += '''## 7. Marie atravessa a estrada antes de se tornar moradora

**Marie Vale (250)**, guarda da vila Elivia (238), iniciou migração por ameaça na hora 9. O destino foi Norria (209), cidade à qual sua vila era subordinada. Ela já conhecia a conexão profissional e partiu com duas unidades de alimento e duas de água.

A viagem física terminou na hora 13. A mudança oficial de residência só ocorreu na hora 39. Portanto, estrada percorrida, chegada e estabelecimento foram etapas distintas. Marie permaneceu viva na nova cidade até o encerramento. O registro da migração identifica “ameaça”; não atribuímos um agressor específico sem uma cadeia de fatos adicional.

'''
    lore += refs([30797,30798,36771,66954])+'\n\n'
    lore += '''## 8. Uma mobilização local consegue uma arma material

Em Mordor (623), um grupo local de segurança levou uma proposta de financiamento de armas à autoridade municipal. **Lyra Douran (3951)** entregou a proposta 54736 presencialmente na hora 27, representando o grupo 34902. Na hora 30, o prefeito **Cael Kars (3844)** aprovou o pedido.

A decisão transferiu duas moedas e entregou uma arma a **Ruan Kars (3838)**, guarda da cidade. A resposta ocorreu na própria localidade, no ponto municipal de encontro: a política teve presença e consequência material. Não houve viagem intermunicipal nesse episódio, nem registro suficiente para dizer que a arma depois venceu um combate ou solucionou permanentemente a insegurança.

'''
    lore += refs([55604,58647])+'\n\n'
    lore += '''## O que esta campanha efetivamente conta

O núcleo mais interessante foi a informação que muda uma trajetória: duas pessoas precisaram de fontes mais confiáveis antes de ter uma conexão utilizável. Também houve migração com estabelecimento separado da chegada, peregrinações incompletas, rito sem resposta obrigatória e organizações que tentam crescer mas não conseguem.

Não surgiram histórias naturais de exploração de caverna, tomada de castelo, expedição, pacto ou morte divina. Os quartéis existiam desde a criação do mundo. As trajetórias abertas foram mantidas como abertas; as demonstrações controladas não foram usadas para completar a lore.

Fonte: `campanha_200h/eventos_espaciais.json`, cruzada com o censo, organizações e viagens pendentes em `campanha_200h/resultado.json`.
'''
    write('HISTORIAS_REAIS.md',lore)

    world = '''# MUNDO — Arandor-54

Mundo criado do zero, acompanhado como espectador por **200 horas**. Este é o catálogo dos lugares, organizações e acontecimentos; a análise de problemas está no relatório técnico. Contadores de ações não representam necessariamente pessoas distintas. Listas de membros e autoridades mostram o estado final. † indica falecimento; IDs distinguem nomes e localidades repetidos.

## Panorama

'''
    world += table(['Elemento','Quantidade'], [
        ['Reinos','4'],['Localidades','45: 4 capitais, 16 outras cidades e 25 vilas'],
        ['NPCs no início / vivos no fim / falecidos',f'{initial_named} / {alive} / {initial_named-alive}'],
        ['Habitantes abstratos no início / fim',f'{initial_abstract} / {final_abstract}'],
        ['População total inicial / final',f'{initial_named+initial_abstract} / {alive+final_abstract}'],
        ['POIs','8: 6 cavernas e 2 quartéis; nenhum castelo abandonado nesta seed'],
        ['Conexões físicas',len(r['routes'])],['Grupos formados / ativos / dissolvidos','179 / 171 / 8'],
        ['Propostas criadas / entregues / decididas','87 / 32 / 12'],
        ['Facções iniciais / ativas no fim / membros ativos','2 / 1 / 1'],
        ['Convites entregues / pessoas convidadas / novas adesões',f'22 / {len(invited)} / 0'],
        ['Deuses existentes / novos deuses / mortes divinas','3 / 0 / 0'],
        ['Abençoados por intervenção / mortais venerados como divinos','0 / 0'],
        ['Pessoas com algum favor divino positivo preservado',len(positive_favor)],
        ['Audiências / contratos / manifestações físicas','0 / 0 / 0'],
    ])
    world += '## Densidade e reinos\n\n'
    world += table(['Tipo','Localidades','NPCs iniciais por lugar','NPCs vivos no fim, somados'],[
        [kind,len([t for t in r['initial'] if t['kind']==k]),str(density),sum(t['named'] for t in r['final'] if t['kind']==k)]
        for kind,k,density in [('Capital','capital',104),('Cidade','cidade',60),('Vila','vila',18)]])
    world += table(['Reino','Capital','Governante final','Cidades além da capital','Vilas','Situação'],[
        [k['name'],place(k['capital_id']),person(k['ruler_id']),', '.join(place(i) for i in k['city_ids'] if i!=k['capital_id']),len(k['village_ids']),f"{k['political_state']}; {k['economic_state']}; {k['military_state']}"] for k in r['kingdoms']])
    world += '### Todas as localidades\n\n'
    world += table(['Localidade','Tipo','NPCs vivos','Abstratos','Autoridade ou subordinação'],[
        [place(t['id']),t['kind'],t['named'],t['abstract'],place(t['authority']) if t['authority'] else person(t['mayor'])] for t in r['final']])
    world += '## Estradas, trilhas e viagens\n\n'
    world += table(['Acontecimento','Quantidade'],[
        ['Viagens iniciadas / concluídas / em andamento','70 / 61 / 9'],['Trechos atravessados','62'],['Viagens com duas conexões','2'],
        ['Pedidos de instrução / transmissões recebidas','128 / 5'],['Novos registros ou melhorias de rota durante a campanha','12'],
        ['Tentativas bloqueadas por desconhecimento','115, envolvendo 53 pessoas'],['Migrações iniciadas / mudanças efetivas de residência','28 / 25'],
        ['Viagens acompanhando/escoltando guia registradas','0']])
    world += 'Lugares com mais conexões físicas: ' + '; '.join(f'{place(id)}: {n}' for id,n in known.most_common(7)) + '. Nenhuma das 45 localidades ficou sem conexão física; isso não significa que todos os moradores conheçam suas estradas.\n\n'
    world += '### Todas as conexões\n\n'
    world += table(['Rota','Origem','Destino','Tipo','Distância / horas de estrada','Travessias concluídas'],[
        [x['id'],place(x['origin']),place(x['destination']),label(x['route_type']),f"{x['distance']} / {x['travel_time']}",x['uses']] for x in r['routes']])
    world += 'As horas de estrada não incluem todas as pausas e deslocamentos interiores do viajante.\n\n### Viajantes com jornada ainda aberta\n\n'
    world += table(['Pessoa','Partida','Destino','Motivo','Trecho atual'],[
        [person(j['actor']),f"h{j['started_at']}",place(j['destination']),label(j['reason']),f"{place(j['nodes'][j['leg']])} → {place(j['nodes'][j['leg']+1])}"] for j in r['traveling']])
    world += '## Pontos de interesse\n\n'
    world += table(['Lugar','Tipo','Áreas','Perigo / profundidade','Reivindicação','Estoque final'],[
        [place(p['id']),p['kind'],', '.join(p['areas']),f"{p['danger']} / {p['depth']}",factions[p['claimant_id']]['name'] if p['claimant_id'] in factions else 'nenhuma',inv(p['inventory'])] for p in r['points']])
    world += 'Nesta campanha, não houve nova visita, exploração, expedição, descoberta ou ocupação de POI registrada. As duas sedes já eram residências de líderes no início; suas saídas para procurar pessoas foram viagens reais. As seis cavernas continuaram sem exploração registrada.\n\n## Facções e seus membros\n\n'
    for f in r['factions']:
        world += f"### {f['name']} ({f['id']})\n\n"
        world += f"Atividade: {label(f['purpose'])}. Sede: {place(f['headquarters_id'])}. Estado final: {label(f['status'])}. Líder registrado: {person(f['leader_id'])}. Recursos finais: {f['money']} moedas; {inv(f['inventory'])}.\n\n"
        world += 'Hierarquia: ' + ' → '.join(f['ranks']) + '. Tradição religiosa: ' + f['norms'].get('religion','não registrada') + '.\n\n'
        world += 'Membros no fim: ' + ('; '.join(person(i)+' — '+f['assignments'].get(str(i),{}).get('rank','líder' if i==f['leader_id'] else 'membro') for i in f['member_ids']) or 'nenhum') + '.\n\n'
        former=f['norms'].get('former_members',[])
        if former:world += 'Ex-membros registrados: ' + '; '.join(person(i) for i in former) + '.\n\n'
        world += table(['Pessoa','Hora do contato','Situação'],[
            [person(int(id)),f"h{record['created_at']}",label(record['status'])] for id,record in f['norms'].get('invitations',{}).items()])
    world += 'Não houve nova formalização de grupo, troca de sede ou adesão consumada. Foram registradas duas contribuições institucionais, cinco preparações organizacionais, três ordens e três ações organizacionais.\n\n## Religião, deuses e pessoas marcadas\n\n'
    world += table(['Deus','Domínio','Estado','Seguidores vivos','Praticantes recentes','Região de presença','Vínculos raros'],[
        [g['name'],label(g['domain']),'vivo' if g['alive'] else 'morto',r['religion'][str(g['id'])]['followers'],r['religion'][str(g['id'])]['cultists'],', '.join(place(i) for i in g['presence_regions']),len(g['bonds'])] for g in r['gods']])
    world += 'Seguidores contam crença divina com confiança ≥30; praticantes recentes contam atividade de culto nas 200 horas observadas. Presença regional não implica corpo físico visível. Dorven abriga referências de contato de Neruma e Elar; Silvia, de Aurion.\n\n'
    world += 'Houve 157 intenções de busca de contato, 18 viagens religiosas e oito ritos de acesso alcançados. Também ocorreram 57 mensagens divinas, 15 avaliações de ação divina e sete mudanças de afinidade. Mensagem ou afinidade não equivale a bênção. Não houve audiência excepcional, contrato, manifestação física, apoteose ou mortal venerado como deus.\n\n'
    world += table(['Hora','Pessoa que alcançou o rito','Deus','Lugar'],[
        [e['turn'],person(e['actor_id']),gods[e['target_id']]['name'],place(e['context']['place_id'])] for e in events if e['kind']=='DivineAccessAchieved'])
    world += '### Favor divino positivo preservado\n\nFavor numérico baixo não representa pacto ou bênção. A lista inclui falecidos quando o deus ainda conserva o registro.\n\n'
    world += table(['Pessoa','Favor conhecido pelos deuses'],[
        [person(id),'; '.join(f'{name}: {value:g} (feitos reconhecidos: {deeds})' for name,value,deeds in rows)] for id,rows in sorted(positive_favor.items())])
    world += '### Potencial mítico\n\nOito pessoas nasceram com potencial mítico; nenhuma se tornou deus. Desenvolvimento não equivale a divinização.\n\n'
    world += table(['Pessoa','Traço','Desenvolvimento final'],[
        [person(c['id']),label(c['mythic_trait']),c['mythic_development']] for c in chars.values() if c['mythic_trait']])
    world += '## Mobilização e política\n\n'
    world += table(['Causa de grupo','Formados','Ativos no fim'],[
        [cause,sum(g['cause']==key for g in r['groups']),sum(g['cause']==key and g['status']=='active' for g in r['groups'])] for cause,key in [('Segurança','security'),('Recursos','resource_pressure')]])
    world += 'Das 87 propostas, 55 permaneceram em rascunho, 20 estavam entregues sem decisão, dez receberam decisão parcial, uma foi aprovada e uma foi adiada. As 12 decisões envolveram 28 moedas, cinco armas e nenhuma unidade de alimento.\n\n'
    # Validar os totais materiais antes de apresentá-los como fatos.
    assert sum(e['context']['result']['material']['money'] for e in decisions)==28
    assert sum(bool(e['context']['result']['material'].get('weapon_id')) for e in decisions)==5
    world += '### Decisões municipais\n\n'
    world += table(['Hora','Autoridade','Lugar','Proposta','Decisão','Consequência'],[
        [e['turn'],person(e['actor_id']),place(e['context']['town_id']),e['target_id'],label(e['context']['result']['decision']),f"{e['context']['result']['material']['money']} moedas; beneficiários: "+(', '.join(person(i) for i in e['context']['result']['material']['recipients']) or 'nenhum')+('; uma arma' if e['context']['result']['material'].get('weapon_id') else '')] for e in decisions])
    world += '### Todos os grupos registrados\n\nMembros abaixo são os registrados no encerramento, sem presumir que todos estavam juntos. Grupos com nomes semelhantes continuam distintos pelos IDs.\n\n'
    world += table(['ID / grupo','Lugar','Causa / estado','Líder','Membros finais'],[
        [f"{g['id']} — {g['name']}",place(g['town_id']),f"{label(g['cause'])} / {label(g['status'])}",person(g['leader_id']),'; '.join(person(i) for i in g['member_ids']) or 'nenhum'] for g in r['groups']])
    world += '### Todas as propostas registradas\n\n'
    world += table(['ID','Hora de criação','Grupo','Lugar','Solução','Autoridade destinatária','Estado final'],[
        [p['id'],p['created_at'],p['group_id'],place(p['town_id']),label(p['solution']),person(p['target_id']),label(p['status'])] for p in extra['proposals'].values()])
    world += '## Acontecimentos de vida e conflito\n\n'
    world += table(['Acontecimento','Ocorrências'],[[name,r['events'].get(key,0)] for key,name in (
        ('HelpGiven','Ajudas'),('ProtectionGiven','Proteções'),('FirstAidGiven','Primeiros socorros'),
        ('FamilySearch','Buscas de familiares'),('InvestigationPerformed','Investigações'),
        ('InformationShared','Informações transmitidas'),('ItemStolen','Furtos'),
        ('GuardResponded','Respostas de guardas'),('CharacterConfronted','Confrontações'),
        ('CharacterDefended','Defesas'),('CharacterFled','Fugas'),('CharacterSurrendered','Rendições'),
        ('CharacterKilled','Mortes em combate'),('FoodEaten','Refeições consumidas'),
        ('FoodGathered','Coletas de comida'),('TemporaryWorkPerformed','Trabalhos temporários'))])
    world += '**Um confronto terminou em morte:** na hora 154, em Elilen (810), Darin Douran (4721), caçador, causou a morte de Nora Montes (4664), mineira. O evento registrou intenção de conter e morte não intencional; não foi execução planejada. O matador manifestou culpa, vergonha e medo na reação registrada. Os outros 132 falecimentos foram classificados como privação: 92 por sede, 32 por fome e oito combinados.\n\n'
    world += 'Os quatro reinos terminaram politicamente estáveis e em paz, com economia em crise. Não houve guerra, conquista territorial ou divinização registrada. As oito trajetórias pessoais estão em `HISTORIAS_REAIS.md`; os números e listas provêm exclusivamente de Arandor-54, sem somar a campanha anterior de Thalendor.\n'
    write('MUNDO.md',world)

    old=BASE/'MUNDO.md'
    archive=BASE/'reports/fase_5_2_1/mundo_thalendor/MUNDO.md'
    if old.exists() and 'Thalendor-521' in old.read_text()[:150] and not archive.exists():
        archive.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(old,archive)
    shutil.copy2(OUT/'MUNDO.md',old)
    shutil.copy2(OUT/'RELATORIO_TECNICO.md',BASE/'RELATORIO_5_4.md')
    h=hashlib.sha256()
    for p in sorted((BASE/'procedural').glob('*.py')):
        h.update(p.name.encode());h.update(p.read_bytes())
    hs=hashlib.sha256()
    with (DATA/'save_final.json').open('rb') as stream:
        while chunk:=stream.read(1024*1024):hs.update(chunk)
    delivery={'status':'completed','rules':r['rules'],'seed':r['seed'],'hours':r['hours'],
              'campaign_code_sha256':r['code_sha256'],'delivered_code_sha256':h.hexdigest(),
              'save_sha256':hs.hexdigest(),'tests_passed':14,'checkpoints_without_errors':8,
              'route_audit_errors':r['route_audit'],'restart':{'same_seed':True,'stopped_hour':100,'reason':'observation_memory_limit'},
              'after_campaign_adjustments':['exploration return need','hour-zero explored-state guard','generation comment'],
              'after_campaign_natural_events_affected':0,
              'reports':[str(OUT/name) for name in ('HISTORIAS_REAIS.md','RELATORIO_TECNICO.md','MUNDO.md')]}
    (OUT/'ENTREGA_FINAL.json').write_text(json.dumps(delivery,ensure_ascii=False,indent=2))
    print(json.dumps({'reports_written':3,'tests':14,'hours':r['hours'],'groups_listed':len(groups),'proposals_listed':len(extra['proposals']),'positive_favor_people':len(positive_favor)},ensure_ascii=False))

if __name__=='__main__':main()
