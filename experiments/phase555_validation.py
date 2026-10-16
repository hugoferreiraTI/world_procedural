"""Validação da 5.5.5. Sem profiler, monkeypatch, consultas de decisão ou seed-shopping."""
import argparse
from dataclasses import asdict, fields
import gzip
import hashlib
import json
from pathlib import Path
import time
import traceback

from procedural import RULES_VERSION, GENERATION_VERSION
from procedural.engine import Engine
from procedural.generation import generate_world, GenerationConfig
from procedural.observability import HistoricalObserver, IMPORTANT
from procedural.persistence import dumps, loads, encode, JsonRepository
from procedural.validation import assert_valid

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'reports/fase_5_5_5'
CAMPAIGN_SEED='Elyndar-Estabilidade555'


def digest(value):
    return hashlib.sha256(value.encode() if isinstance(value,str) else value).hexdigest()


def sources():
    return {str(p.relative_to(ROOT)):digest(p.read_bytes())
            for folder in ('procedural','tests') for p in sorted((ROOT/folder).glob('*.py'))}


def write(name,data):
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')


def require_green():
    text=(OUT/'testes_final.log').read_text()
    if not text.rstrip().endswith('OK'):raise RuntimeError('A suíte completa precisa estar verde antes desta etapa.')


def game_signature(world):
    # Mantém inclusive todos os metadados dos Events, IDs e RNG. Só exclui a
    # coleção privada de observabilidade; geração/config permanecem comparadas.
    data={f.name:getattr(world,f.name) for f in fields(world) if f.name!='observability'}
    return digest(json.dumps(encode(data),ensure_ascii=False,sort_keys=True,separators=(',',':')))


def new(seed,level='NORMAL',kingdoms=1):
    return Engine(generate_world(seed,with_player=False,historical_trace_level=level,
        config=GenerationConfig(kingdom_count=kingdoms,historical_turns=0)))


def money(w):
    return (sum(p.money for p in w.characters.values())+sum(t.money+t.abstract_money for t in w.towns.values())
            +sum(k.treasury for k in w.kingdoms.values())+sum(f.money for f in w.factions.values())
            +sum(g.money for g in w.groups.values())+sum(p.money for p in w.institutional_policies.values()))


def controls():
    require_green();started=time.monotonic();initial=sources();result={'rules':RULES_VERSION,'generation':GENERATION_VERSION,'sources':initial}
    # Ordem pedida: save/load, A/B, smoke. Cada controle usa um único nome fixo.
    a=new('Controle-Continuidade555');b=new('Controle-Continuidade555')
    a.simulate(100);b.simulate(50)
    text=dumps(b.world);b=Engine(loads(text));b.simulate(50)
    da=dumps(a.world);db=dumps(b.world)
    assert da==db,'Divergência de save/load, incluindo história e recebimentos.'
    assert_valid(a.world);assert_valid(b.world)
    result['continuity']={'seed':a.world.seed,'continuous_hours':100,'split_hours':[50,50],
        'all_persistent_fields_equal':True,'sha256':digest(da),'rng_equal':a.rng.getstate()==b.rng.getstate(),
        'next_gameplay_id':a.world.next_id,'next_private_id':a.world.observability.next_id,
        'learning_receipts_equal':a.world.observability.learning==b.world.observability.learning,
        'history_equal':a.world.history==b.world.history,'bytes':len(da.encode())}
    del a,b,da,db,text
    a=new('Controle-Neutralidade555','OFF');b=new('Controle-Neutralidade555','NORMAL')
    a.simulate(24);b.simulate(24)
    ga=game_signature(a.world);gb=game_signature(b.world)
    assert ga==gb,'Observabilidade alterou estado fora da coleção privada.'
    assert_valid(a.world);assert_valid(b.world)
    result['neutrality']={'seed':a.world.seed,'hours_each':24,'levels':['OFF','NORMAL'],
        'all_gameplay_fields_including_event_metadata_equal':True,'sha256':ga,
        'rng_equal':a.rng.getstate()==b.rng.getstate(),
        'off_decisions_retained':len(a.world.observability.decisions),
        'on_decisions_retained':len(b.world.observability.decisions),
        'on_learning_receipts':len(b.world.observability.learning)}
    # AUDIT usa o mesmo algoritmo; valida também o nível detalhado sem campanha longa.
    c=new('Controle-Neutralidade555','AUDIT');c.simulate(24)
    assert game_signature(c.world)==ga
    result['neutrality']['audit_equal']=True
    del a,b,c
    smoke=new('Controle-Smoke555',kingdoms=4);smoke.simulate(12);assert_valid(smoke.world)
    assert not smoke.geography.audit()
    result['smoke']={'seed':smoke.world.seed,'hours':12,'npcs':len(smoke.world.characters),'invariants':True}
    assert sources()==initial,'Fontes mudaram durante os controles.'
    result['seconds']=round(time.monotonic()-started,3)
    write('controles.json',result)
    print(json.dumps({k:v for k,v in result.items() if k!='sources'},ensure_ascii=False),flush=True)


def event_hash(event):
    return digest(json.dumps(encode(event),sort_keys=True,ensure_ascii=False,separators=(',',':')))


def storage(w):
    o=w.observability
    return {'history_events':len(w.history),'operational_buffer':len(w.events),
        'decisions_retained':len(o.decisions),'important_decisions':sum(t.important for t in o.decisions.values()),
        'ordinary_decisions':sum(not t.important for t in o.decisions.values()),
        'recent_decisions':len(o.recent_decisions),'last_decision_ids':len(o.last_decision_ids),
        'attempts':len(o.attempts),'permanent_receipts':len(o.learning),'recent_receipts':len(o.recent_learning),
        'archived_nonhistorical_events':len(o.event_archive)}


def example(e):
    o=e.world.observability
    # Seleção determinística de um caso que realmente conserve todos os elos.
    # Não muda o mundo nem exige evento raro na campanha.
    for trace in o.decisions.values():
        if not trace.important or not trace.action_attempt_id or not trace.source_fact_ids:continue
        attempt=o.attempts.get(trace.action_attempt_id)
        if not attempt or attempt.success is None:continue
        for id in trace.emitted_event_ids:
            details=e.observability.event_details(id)
            if not details or not details['learning_receipts'] or not details['event'].historical:continue
            source=next((e.observability.index.events.get(i) for i in trace.source_fact_ids
                         if e.observability.index.events.get(i)),None)
            if source is None:continue
            learned=next((r for r in o.learning if r.receiver_id==trace.actor_id and r.event_id==source.id),None)
            if not learned:
                learned=next((r for r in o.recent_learning if r.receiver_id==trace.actor_id and r.event_id==source.id),None)
            if not learned:continue
            return {'natural':True,'source_event':asdict(source),'source_learning_receipt':asdict(learned),
                'need_episode_id':trace.need_episode_id,'decision':asdict(trace),'goal_id':trace.goal_id,
                'action_attempt':asdict(attempt),'result_event':asdict(details['event']),
                'result_learning_receipt':asdict(details['learning_receipts'][0])}
    return None


def campaign():
    require_green()
    control=json.loads((OUT/'controles.json').read_text())
    if control['sources']!=sources():raise RuntimeError('Os controles pertencem a outro estado do código.')
    if (OUT/'campanha.json').exists():raise RuntimeError('Campanha já registrada; não repetir nem trocar seed silenciosamente.')
    started=time.monotonic();initial=sources();e=new(CAMPAIGN_SEED,kingdoms=4);w=e.world
    initial_money=money(w);initial_source=w.metrics.get('MoneySourceAbstractWork',0)
    result={'rules':RULES_VERSION,'generation_version':w.generation_version,'generation_config':w.generation_config,
        'seed':w.seed,'start_turn':w.turn,'requested_hours':300,'with_player':False,'initial_named':len(w.characters),
        'initial_abstract':sum(t.abstract_population for t in w.towns.values()),'sources':initial,'checkpoints':[]}
    historical={ev.id:event_hash(ev) for ev in w.history}
    write('campanha_em_andamento.json',{'seed':w.seed,'hours':0,'sources':initial})
    try:
        for _ in range(300):
            e.step()
            if w.turn%25==0:
                assert_valid(w)
                geography=e.geography.audit();assert not geography,geography
                for ev in (*w.history,*w.observability.event_archive.values()):
                    stamp=event_hash(ev)
                    if ev.id in historical:assert historical[ev.id]==stamp,('Histórico reescrito',ev.id)
                    else:historical[ev.id]=stamp
                supplied=w.metrics.get('MoneySourceAbstractWork',0)-initial_source
                residual=money(w)-initial_money-supplied
                assert residual==0,('Saldo monetário não explicado',residual)
                row={'hour':w.turn,'alive':sum(p.alive for p in w.characters.values()),'deaths':len(w.death_records),
                     'money':money(w),'explicit_currency_source':supplied,'money_residual':residual,
                     'history_immutable':True,'invariants':True,**storage(w)}
                result['checkpoints'].append(row)
                print(json.dumps(row,ensure_ascii=False),flush=True)
                write('campanha_em_andamento.json',{'seed':w.seed,'hours':w.turn,'checkpoints':result['checkpoints']})
        assert sources()==initial,'Fontes mudaram durante a campanha.'
        result.update(status='completed',hours=w.turn,final_named=len(w.characters),final_alive=sum(p.alive for p in w.characters.values()),
            final_abstract=sum(t.abstract_population for t in w.towns.values()),world_metrics=dict(w.metrics),
            death_causes={},final_storage=storage(w),initial_money=initial_money,final_money=money(w),
            explicit_money_source=w.metrics.get('MoneySourceAbstractWork',0)-initial_source)
        for r in w.death_records.values():
            cause=r.get('cause','unknown');result['death_causes'][cause]=result['death_causes'].get(cause,0)+1
        result['observability_counters']=dict(w.observability.counters)
        result['causal_events']=sum(bool(ev.parent_event_ids) for ev in w.history)
        result['causal_links']=sum(len(ev.parent_event_ids) for ev in w.history)
        result['important_events']=sum(ev.kind in IMPORTANT for ev in w.history)
        result['unavailable_parent_ids']=sorted({id for ev in w.history for id in ev.parent_event_ids if id not in e.observability.index.events})
        result['organizations']={'groups':len(w.groups),'factions':len(w.factions),'proposals':len(w.proposals),
            'policies':len(w.institutional_policies),'group_statuses':{},'policy_statuses':{}}
        for key,collection in (('group_statuses',w.groups),('policy_statuses',w.institutional_policies)):
            for obj in collection.values():
                status=obj.status;d=result['organizations'][key];d[status]=d.get(status,0)+1
        result['religion']={'divinities':len(w.divinities),'audiences':w.metrics.get('DivineAudience',0),
            'interventions':w.metrics.get('DivineIntervention',0),'apotheoses':w.metrics.get('Apotheosis',0),
            'congregation_reports':w.metrics.get('Faith:congregation_report',0)}
        ex=example(e);write('cadeia_real.json',ex)
        result['complete_natural_example']=bool(ex)
        temporary=OUT/'save_temporario.json'
        JsonRepository().save(w,temporary)
        raw=temporary.read_text();restored=loads(raw)
        assert dumps(restored)==raw,'O save final não reproduziu todos os campos.'
        read=HistoricalObserver(restored)
        sample=next((ev for ev in reversed(w.history) if ev.kind in IMPORTANT),None)
        if sample:assert read.event_details(sample.id)['event']==sample
        result['save']={'format_version':2,'bytes':temporary.stat().st_size,'sha256':digest(raw),
            'all_fields_equal_after_load':True,'indices_rebuilt':True,'removed_after_validation':True}
        result['observability_bytes']=len(json.dumps(encode(w.observability),ensure_ascii=False,separators=(',',':')).encode())
        del raw,restored,read
        temporary.unlink()
        # Evidência compactada, sem snapshots completos de Character/mundo.
        archive={'rules':RULES_VERSION,'seed':w.seed,'turn':w.turn,'generation_version':w.generation_version,
            'generation_config':w.generation_config,'characters':{id:{'name':p.name,'profession':p.profession,'alive':p.alive,'town_id':p.town_id} for id,p in w.characters.items()},
            'events':{ev.id:ev for ev in w.history},'observability':w.observability}
        path=OUT/'historico_nativo.json.gz'
        with gzip.open(path,'wt',encoding='utf-8',compresslevel=6) as stream:
            json.dump(encode(archive),stream,ensure_ascii=False,separators=(',',':'))
        result['historical_archive']={'path':str(path.relative_to(ROOT)),'bytes':path.stat().st_size,'sha256':digest(path.read_bytes()),
                                      'contains_full_character_snapshots':False,'contains_full_save':False}
        result['seconds']=round(time.monotonic()-started,3)
        write('campanha.json',result)
        (OUT/'campanha_em_andamento.json').unlink()
        print(json.dumps({'status':'completed','hours':w.turn,'seconds':result['seconds'],'storage':result['final_storage']},ensure_ascii=False),flush=True)
    except Exception:
        result.update(status='failed',hours=w.turn,exception=traceback.format_exc(),seconds=round(time.monotonic()-started,3))
        write('campanha.json',result)
        raise


def main():
    parser=argparse.ArgumentParser();parser.add_argument('stage',choices=('controls','campaign'));args=parser.parse_args()
    (controls if args.stage=='controls' else campaign)()

if __name__=='__main__':main()
