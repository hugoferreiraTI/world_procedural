"""Comparação e episódios documentados, sem converter correlações em motivos."""
from collections import Counter,defaultdict
import gzip
import json
from pathlib import Path

from experiments import feeding_narratives
from procedural.engine import Engine
from procedural.persistence import JsonRepository
from procedural.needs import FINISHED

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'reports/fase_3_2'
OLD=ROOT/'reports/correcao_alimentar'
MODES=('jogador','espectador','mundo')
def read(p):return json.loads(p.read_text())
def rows(p):
    with gzip.open(p,'rt',encoding='utf-8') as f:
        for line in f:yield json.loads(line)
def write(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')


def main():
    feeding_narratives.OUT=OUT;feeding_narratives.main()
    compare={};extras={};census={};evidence={}
    for mode in MODES:
        directory=OUT/'auditorias'/mode
        engine=Engine(JsonRepository().load(directory/'save_final.json'));world=engine.world
        before=read(OLD/'comparativo.json')[mode]['after']
        food=read(directory/'metricas_alimentacao.json');econ=read(directory/'metricas_fase3.json')
        personal=read(directory/'metricas_fase2.json');detail=read(directory/'metricas_fase32.json')
        frames=read(directory/'quadros_reserva.json')
        counts=detail['counts']
        compare[mode]={'before':before,'after':{'deaths':sum(econ['death_conditions'].values()),
          'hunger_deaths':econ['death_conditions'].get('hunger',0)+econ['death_conditions'].get('both',0),
          'thirst_deaths':econ['death_conditions'].get('thirst',0)+econ['death_conditions'].get('both',0),
          'physiological_percent':100*personal['selected_distribution']['physiological']/sum(personal['selected_distribution'].values()),
          'personal_selections':sum(v for k,v in personal['selected_distribution'].items() if k in ('family','grief','revenge','protection','status','advancement')),
          'personal_satisfied':sum(sum(v.values()) for k,v in personal['lifecycle']['Satisfied'].items() if k in ('family','grief','revenge','protection','status','advancement')),
          'reserve_selections':counts['reserve_selected'],'healthy_reserve_percent':100*counts['healthy_reserve_selected']/counts['healthy_deficit'],
          'final':econ['final']['summary'],'trained':econ['workers_trained'],'retrained_existing':econ['workers_retrained'],
          'materialized':econ['workers_materialized'],'means':food['means'],'reserve_final':food['final_reserve'],
          'average_snapshot_reserve_percent':sum(f['maintaining_reserve_percent'] for f in frames)/len(frames),
          'average_snapshot_personal_food':sum(f['average_personal_food'] for f in frames)/len(frames),
          'hunger_deaths_with_food':food['hunger_deaths_with_food']}}
        episodes=read(directory/'episodios_narrativos.json')['episodes']
        events=list(rows(directory/'narrativa.jsonl.gz'));by_id={e['id']:e for e in events}
        actions=list(rows(directory/'acoes_pessoais.jsonl.gz'))
        income=list(rows(directory/'economia_acoes.jsonl.gz'))
        by_actor=defaultdict(list)
        for e in events:
            if e['actor_id'] is not None:by_actor[e['actor_id']].append(e)
        def strict_food(ep):
            return (ep['need']['kind']=='family' and ep['need']['context'].get('mode')=='care'
                    and ep['need']['context'].get('resource','food')=='food') or any(e['kind']=='ItemStolen' for e in ep['events'])
        def player_in(ep):
            return any(world.player_id in (e.get('actor_id'),e.get('target_id')) for e in ep['events']) if world.player_id else False
        extras[mode]={'episodes_at_least_3_events':sum(e['event_count']>=3 for e in episodes),
           'episodes_at_least_4_events':sum(e['event_count']>=4 for e in episodes),
           'episodes_without_direct_food_care_or_food_crime':sum(not strict_food(e) for e in episodes),
           'episodes_with_player_event':sum(player_in(e) for e in episodes),
           'episodes_without_player_event':sum(not player_in(e) for e in episodes),
           'personal_needs_interrupted_by_death':sum(v for k,v in econ['personal_outcomes'].items() if k.endswith(':OwnerDied')),
           'actual_attack_events':world.metrics.get('CharacterKilled',0),
           'material_poverty_is_not_political_consciousness':True}
        poor=[];towns=[]
        for town in world.towns.values():
            local=[c for c in world.characters.values() if c.alive and not c.is_player and c.position.map_id==town.id]
            price=engine.economy.price(town.id,'food');stock=engine.items.count(town.id,'food')
            offers=engine.professions.temporary_capacity(town)
            townpoor=[c for c in local if c.money<price]
            towns.append({'id':town.id,'name':town.name,'money':town.money,'food':stock,'price':price,
                          'local_living':len(local),'poor':len(townpoor),'resident_cash':sum(c.money for c in local)})
            for c in townpoor:
                poor.append({'id':c.id,'name':c.name,'profession':c.profession,'money':c.money,'food':engine.items.count(c.id,'food'),
                 'health':c.health,'hunger':c.hunger,'town_id':town.id,'town_money':town.money,'municipal_food':stock,'real_price_for_auditor':price,
                 'profession_saturated':engine.professions.saturated(c,{'stock':{k:engine.items.count(town.id,k) for k in ('grain','food','iron','wood')}}),
                 'temporary_eligible':engine.professions.temporary_eligible(c),'temporary_capacity':offers,
                 'known_places':{k:vars(v) for k,v in c.known_places.items()},'known_market':c.market_observation,
                 'active_needs':[{'kind':n.kind,'priority':n.priority,'status':n.status} for n in c.needs.values() if n.status not in FINISHED]})
        census[mode]={'municipal_money':sum(t.money for t in world.towns.values()),
          'living_npc_money':sum(c.money for c in world.characters.values() if c.alive and not c.is_player),
          'poor_on_town_maps':len(poor),'poor_with_municipal_food':sum(p['municipal_food']>0 for p in poor),
          'poor_saturated':sum(p['profession_saturated'] for p in poor),'poor_temporary_ineligible':sum(not p['temporary_eligible'] for p in poor),
          'towns':towns,'poor_people':poor}
        # Cada seleção conserva a evidência original. A prosa descreve só o que os registros permitem.
        selected=[]
        def choose(label,predicate,sort=None):
            candidates=[e for e in episodes if predicate(e)]
            if candidates:
                selected.append({'label':label,'episode':max(candidates,key=sort or (lambda e:(e['event_count'],e['span_hours'])) )})
        choose('Busca familiar e localização',lambda e:e['need']['kind']=='family' and e['need']['context'].get('mode')=='missing' and any(x['kind']=='PersonLocated' for x in e['events']))
        choose('Luto e lembrança',lambda e:e['need']['kind']=='grief')
        choose('Investigação de responsável conhecido',lambda e:e['need']['kind']=='revenge' and any(a['action']=='investigate' for a in e['actions']))
        choose('Denúncia a autoridade independente',lambda e:any(a['action']=='denounce' and a['success'] for a in e['actions']))
        choose('Proteção concreta',lambda e:e['need']['kind']=='protection' and any(a['action'] in ('stay_near','avoid_threat') for a in e['actions']))
        choose('Ajuda familiar material',lambda e:e['need']['kind']=='family' and e['need']['context'].get('mode')=='care' and any(a['action']=='give_supplies' and a['success'] for a in e['actions']))
        choose('Reconhecimento',lambda e:e['need']['kind']=='status')
        changes=[e for e in events if e['kind']=='ProfessionChanged']
        careers=[]
        for change in changes:
            actor=change['actor_id'];history=[e for e in by_actor[actor] if e['kind'] in ('TrainingStarted','TrainingProgress','TrainingAbandoned','ProfessionChanged') and e['turn']<=change['turn']]
            failures=[a for a in income if a['npc_id']==actor and not a['success'] and a['turn']<=change['turn']]
            careers.append({'actor_id':actor,'profession_change':change,'history':history,'work_failures_before_change':failures[:12],
                            'final':{'name':world.characters[actor].name,'alive':world.characters[actor].alive,'profession':world.characters[actor].profession,'money':world.characters[actor].money}})
        fractional=[a for a in income if a['goal']['action']=='work' and a['success'] and a['money_after']==a['money_before'] and a['credit_after']>a['credit_before']]
        quota=[a for a in income if a['goal']['action'] in ('temporary_service','service_meal') and not a['success']]
        saturated=[a for a in income if a['goal']['action']=='work' and not a['success'] and a['outcome']=='O estoque já atende à demanda.']
        player_events=[e for e in events if world.player_id is not None and world.player_id in (e['actor_id'],e['target_id'])]
        evidence[mode]={'personal_stories':selected,'careers':sorted(careers,key=lambda c:-sum(e['kind']=='TrainingAbandoned' for e in c['history']))[:3],
          'fractional_credit_examples':fractional[:3],'lost_temporary_offer_examples':quota[:3],
          'saturated_work_examples':saturated[:3],'player_events':player_events[:12],
          'succession': [e for e in events if e['kind']=='SuccessionChanged'][:3]}
    write(OUT/'comparativo.json',compare);write(OUT/'diversidade_complementar.json',extras)
    write(OUT/'censo_economico.json',census);write(OUT/'historias_evidencias.json',evidence)
    print(json.dumps({m:compare[m]['after'] for m in MODES},ensure_ascii=False))


if __name__=='__main__':main()
