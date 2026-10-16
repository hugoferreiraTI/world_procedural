"""Censo dos saves e dos logs canônicos, sem modificar as campanhas."""
from collections import Counter, defaultdict
import gzip
import json
from pathlib import Path

from procedural.engine import Engine
from procedural.persistence import dumps, loads

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT/'reports/correcao_alimentar/auditorias'
OUT = ROOT/'reports/fase_3_2_diagnostico'


def rows(path):
    with gzip.open(path, 'rt', encoding='utf-8') as stream:
        for line in stream:
            yield json.loads(line)


def main():
    OUT.mkdir(exist_ok=True)
    result = {}
    for mode in ('jogador', 'espectador', 'mundo'):
        directory = BASE/mode
        save_text = (directory/'save_final.json').read_text()
        engine = Engine(loads(save_text))
        world = engine.world
        economy, examples = Counter(), defaultdict(list)
        def sample(category, row):
            if len(examples[category]) < 10:
                examples[category].append(row)
        for c in world.characters.values():
            if not c.alive or c.is_player:
                continue
            t = world.towns[c.town_id]
            food = engine.items.count(c.id,'food')
            local_food = engine.items.count(t.id,'food')
            stocks = {k:engine.items.count(t.id,k) for k in ('food','grain','wood','iron')}
            price = engine.economy.price(t.id,'food')
            poor = c.money < price
            saturated = engine.professions.saturated(c, {'stock':stocks})
            economy['alive'] += 1
            economy['money_below_one_current_meal'] += poor
            economy['no_food_and_money_below_meal'] += food == 0 and poor
            economy['poor_with_local_food'] += poor and local_food > 0
            economy['poor_with_local_food_and_town_cash'] += poor and local_food > 0 and t.money > 0
            economy['poor_with_food_and_cash_in_same_map'] += poor and local_food > 0 and t.money > 0 and c.position.map_id == t.id
            economy['poor_with_saturated_profession'] += poor and saturated
            economy['poor_ineligible_for_temporary_product_work'] += poor and not engine.professions.temporary_eligible(c)
            economy['poor_with_whole_coin_wage_credit'] += poor and c.wage_credit >= 6
            economy['poor_with_whole_coin_credit_and_town_cash'] += poor and c.wage_credit >= 6 and t.money > 0
            economy['local_profession_saturated'] += saturated
            economy['town_money_zero_for_alive_resident'] += t.money == 0
            economy['npc_money_total'] += c.money
            economy['wage_credit_sixths_total'] += c.wage_credit
            if poor:
                sample('poor', {'npc_id':c.id,'name':c.name,'profession':c.profession,'money':c.money,
                    'food':food,'hunger':c.hunger,'wage_credit_sixths':c.wage_credit,
                    'town_id':t.id,'town_name':t.name,'town_money':t.money,
                    'stock':stocks,'price_for_auditor':price,'profession_saturated':saturated,
                    'temporary_product_work_eligible':engine.professions.temporary_eligible(c)})
            if poor and c.wage_credit >= 6:
                sample('poor_with_wage_credit', {'npc_id':c.id,'name':c.name,'money':c.money,
                    'wage_credit_sixths':c.wage_credit,'town_money':t.money})
        economy['municipal_money_total'] = sum(t.money for t in world.towns.values())
        economy['abstract_money_total'] = sum(t.abstract_money for t in world.towns.values())
        economy['kingdom_treasury_total'] = sum(k.treasury for k in world.kingdoms.values())
        events = list(rows(directory/'narrativa.jsonl.gz'))
        by_id = {e['id']:e for e in events}
        shared_by_parties_time = defaultdict(list)
        missing_reports = {}
        social = Counter()
        for e in events:
            if e['kind'] == 'ThreatReported':
                social['reports'] += 1
                fact = by_id.get(e['context'].get('fact_id'))
                if fact is None:
                    social['reports_without_source_in_stream'] += 1
                    missing_reports[e['actor_id'],e['turn'],e['context'].get('fact_id')]=e
                elif e['target_id'] == fact['actor_id']:
                    social['reports_to_culprit'] += 1
                    sample('self_suspect_report', {'report':e,'source_fact':fact,
                        'recipient_final_profession':world.characters[e['target_id']].profession})
            elif e['kind'] == 'InformationShared':
                shared_by_parties_time[e['actor_id'],e['target_id'],e['turn']].append(e)
        for a in rows(directory/'acoes_pessoais.jsonl.gz'):
            n = a['need']
            missing = (a['npc_id'],a['turn'],n['context'].get('source_event'))
            if a['goal']['action']=='denounce' and a['success'] and missing in missing_reports:
                fact=next((f for f in a['knowledge_before'] if f['event_id']==missing[2]),None)
                if fact:
                    event=missing_reports.pop(missing)
                    social['reports_source_recovered_from_action_knowledge'] += 1
                    if event['target_id']==fact['actor_id']:
                        social['reports_to_culprit'] += 1
                        sample('self_suspect_report', {'report':event,'source_fact':fact,
                            'source_recovered_from_pre_action_knowledge':True,
                            'recipient_final_profession':world.characters[event['target_id']].profession})
            if a['goal']['action'] != 'ask_personal_help' or n['kind'] != 'family' or n['context'].get('mode') != 'missing':
                continue
            social['missing_information_requests'] += 1
            social['missing_information_requests_successful_execution'] += bool(a['success'])
            for e in shared_by_parties_time[a['goal']['target_id'],a['npc_id'],a['turn']]:
                f = by_id.get(e['context'].get('fact_id'))
                if not f or f['kind'] != 'PersonLocated':
                    continue
                social['missing_request_person_location_transmissions'] += 1
                stale = f['turn'] <= n['context'].get('last_seen',-1)
                too_old = f['turn'] < n['created_at']
                known = next((fact for fact in a['knowledge_before'] if fact['event_id']==f['id']),None)
                social['location_not_newer_than_last_seen'] += stale
                social['location_older_than_need_created_at'] += too_old
                social['location_already_known_before_request'] += known is not None
                if stale:
                    sample('stale_person_location', {'request_turn':a['turn'],'npc_id':a['npc_id'],
                        'name':world.characters[a['npc_id']].name, 'need':n, 'event':e,
                        'source_fact':f,'already_known_fact_before':known,'outcome':a['outcome']})
        social['reports_source_unresolved'] = len(missing_reports)
        assert dumps(world)==save_text, 'O censo alterou o mundo carregado.'
        result[mode] = {'economy_final_snapshot':dict(economy),'social_full_10000_hours':dict(social),
            'examples':dict(examples),
            'method':'Dinheiro/preço/estoque finais são diagnóstico do auditor, não conhecimento remoto entregue a NPCs. Categorias podem se sobrepor. Informações antigas contam transmissões ligadas a pedidos executados; não todos os diálogos ou eventos genéricos.'}
    (OUT/'censo_economico_e_social.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({m:{k:r[k] for k in ('economy_final_snapshot','social_full_10000_hours')} for m,r in result.items()},ensure_ascii=False,indent=2))


if __name__ == '__main__':
    main()
