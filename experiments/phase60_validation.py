"""Controles e campanha única da Fase 6.0, sobre a observabilidade nativa."""
import argparse
from collections import Counter,defaultdict
from dataclasses import asdict,fields,is_dataclass
import gzip,hashlib,json,time,traceback
from pathlib import Path
from procedural import RULES_VERSION,GENERATION_VERSION
from procedural.engine import Engine
from procedural.generation import generate_world,GenerationConfig
from procedural.persistence import dumps,loads,encode
from procedural.validation import assert_valid

ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'reports/fase_6_0'
SEED='Arvandor-Coerencia60'


def digest(data):return hashlib.sha256(data.encode() if isinstance(data,str) else data).hexdigest()
def json_value(value):
    if is_dataclass(value):return asdict(value)
    if isinstance(value,set):return sorted(value,key=repr)
    raise TypeError('Tipo não exportável: '+type(value).__name__)

def write(name,data):
    OUT.mkdir(exist_ok=True,parents=True)
    (OUT/name).write_text(json.dumps(data,ensure_ascii=False,indent=2,default=json_value)+'\n')
def sources():
    return {str(p.relative_to(ROOT)):digest(p.read_bytes()) for folder in ('procedural','tests') for p in sorted((ROOT/folder).glob('*.py'))}
def green():
    if not (OUT/'testes_final.log').read_text().rstrip().endswith('OK'):raise RuntimeError('Suíte final precisa estar verde.')
def new(seed,kingdoms=1,level='NORMAL'):
    return Engine(generate_world(seed,with_player=False,historical_trace_level=level,
        config=GenerationConfig(kingdom_count=kingdoms,historical_turns=0)))
def signature(w):
    return digest(json.dumps(encode({f.name:getattr(w,f.name) for f in fields(w) if f.name!='observability'}),sort_keys=True,separators=(',',':')))
def money(w):
    return (sum(p.money for p in w.characters.values())+sum(t.money+t.abstract_money for t in w.towns.values())+
        sum(k.treasury for k in w.kingdoms.values())+sum(f.money for f in w.factions.values())+
        sum(g.money for g in w.groups.values())+sum(p.money for p in w.institutional_policies.values()))
def aggregate_episodes(e):
    result={}
    for row in e.world.observability.causal.get('episodes',{}).values():
        n=result.setdefault(row['kind'],Counter())
        n['episodes']+=1
        for key in ('active_hours','top_rank_hours','solvable_hours','unknown_solvability_hours','selected_count',
                    'executed_count','successful_count','blocked_by_higher_need_count','reactivation_count','expiration_count'):
            n[key]+=row.get(key,0)
        first=row['time_until_first_selection'];resolution=row['time_until_resolution']
        if first is not None:n['first_selection_sum']+=first;n['selected_episodes']+=1;n['first_selection_max']=max(n['first_selection_max'],first)
        else:n['never_selected']+=1
        if resolution is not None:n['resolution_sum']+=resolution;n['closed_episodes']+=1;n['resolution_max']=max(n['resolution_max'],resolution)
    for row in result.values():
        row['first_selection_mean']=round(row['first_selection_sum']/row['selected_episodes'],3) if row['selected_episodes'] else None
        row['resolution_mean']=round(row['resolution_sum']/row['closed_episodes'],3) if row['closed_episodes'] else None
    return result

def summary(e):
    w=e.world;o=w.observability;c=o.causal;counts=c.get('counts',{})
    selected={k.split(':',1)[1]:v for k,v in counts.items() if k.startswith('selected_need:')}
    from procedural.causal_audit import SURVIVAL
    parents={id for ev in w.history for id in ev.parent_event_ids}
    return {'seed':w.seed,'hours':w.turn,'rules':w.rules_version,'generation':w.generation_version,
        'named':len(w.characters),'alive':sum(p.alive for p in w.characters.values()),
        'abstract':sum(t.abstract_population for t in w.towns.values()),
        'death_causes':dict(Counter(d['cause'] for d in w.death_records.values())),
        'survival_decision_share':sum(v for k,v in selected.items() if k in SURVIVAL)/max(1,sum(selected.values())),
        'counts':counts,'need_funnel':aggregate_episodes(e),
        'lod_latency':{lod:{'episodes':sum(r.get('first_selection_lod')==lod for r in c.get('episodes',{}).values()),
            'mean_first_selection_hours':None} for lod in ('active','local','background')},
        'world_metrics':dict(w.metrics),'native_counters':dict(o.counters),
        'groups':{'objects':len(w.groups),'statuses':dict(Counter(g.status for g in w.groups.values())),
            'memberships':sum(len(g.member_ids) for g in w.groups.values())},
        'tasks':{'total':len(w.institutional_tasks),'statuses':dict(Counter(t.status for t in w.institutional_tasks.values())),
            'kinds':dict(Counter(t.kind for t in w.institutional_tasks.values())),
            'delegated_successes':sum(any(i!=t.issuer for i in t.executor_ids) for t in w.institutional_tasks.values())},
        'proposals':[{'id':p.id,'created':p.created_at,'decided':p.decided_at,'status':p.status,
            'support':p.support,'delivered_support':len(p.delivered_supporter_ids),'groups':p.supporting_group_ids,
            'latency':p.decided_at-p.created_at if p.decided_at is not None else None} for p in w.proposals.values()],
        'policies':{'total':len(w.institutional_policies),'statuses':dict(Counter(p.status for p in w.institutional_policies.values())),
            'worker_rotation':sum(len(p.workers)>1 for p in w.institutional_policies.values())},
        'factions':len(w.factions),'religion':{'gods':len(w.divinities),'audiences':w.metrics.get('DivineAudience',0),
            'interventions':w.metrics.get('DivineIntervention',0),'apotheoses':w.metrics.get('Apotheosis',0)},
        'history_events':len(w.history),'traces_retained':len(o.decisions),'tombstones':len(o.tombstones),
        'parent_ids':len(parents),'missing_full_payloads':len(parents-set(e.observability.index.events)),
        'missing_even_metadata':sorted(parents-set(e.observability.index.events)-set(o.tombstones)),
        'death_funnel':c.get('deaths',{}),'town_days':c.get('town_days',[])}

def fill_lod(e,result):
    for lod,row in result['lod_latency'].items():
        values=[r['time_until_first_selection'] for r in e.world.observability.causal.get('episodes',{}).values()
                if r.get('first_selection_lod')==lod and r['time_until_first_selection'] is not None]
        row['mean_first_selection_hours']=sum(values)/len(values) if values else None

def controls():
    green();initial=sources();started=time.monotonic();result={'sources':initial,'scenarios_log':'testes_causais.log'}
    signatures=[]
    for level in ('OFF','NORMAL','AUDIT'):
        e=new('Controle-Neutralidade60',level=level);e.simulate(36);assert_valid(e.world)
        signatures.append(signature(e.world))
    assert len(set(signatures))==1
    result['neutrality']={'levels':['OFF','NORMAL','AUDIT'],'hours_each':36,'equal_all_gameplay_fields_and_rng':True,'sha256':signatures[0]}
    a=new('Controle-Continuidade60');b=new('Controle-Continuidade60')
    a.simulate(100);b.simulate(50);raw=dumps(b.world);b=Engine(loads(raw));b.simulate(50)
    assert dumps(a.world)==dumps(b.world)
    result['continuity']={'hours':100,'split':[50,50],'all_fields_equal':True,'sha256':digest(dumps(a.world))}
    del a,b,raw
    # Uma variável: capacidade hídrica. Mesmo mundo inicial, pessoas e RNG.
    base=new('Controle-Capacidade60',kingdoms=4)
    raw=dumps(base.world);treated=Engine(loads(raw));del raw
    for t in base.world.towns.values():t.infrastructure.update(water_daily=80,water_storage=160)
    design=[{'id':t.id,'capital':t.capital,'persistent':len(t.resident_ids),'before':80,
             'after':t.infrastructure['water_daily'],'design_demand':t.infrastructure['water_design_demand']} for t in treated.world.towns.values()]
    print('Iniciando A/B de água: 144h por braço, mesmo estado inicial.',flush=True)
    base.simulate(144);treated.simulate(144);assert_valid(base.world);assert_valid(treated.world)
    result['water_capacity_ab']={'seed':'Controle-Capacidade60','hours_each':144,'variable':'water_daily/storage only',
        'design':design,'before':summary(base),'after':summary(treated)}
    fill_lod(base,result['water_capacity_ab']['before']);fill_lod(treated,result['water_capacity_ab']['after'])
    del base,treated
    smoke=new('Controle-Smoke60',kingdoms=4);smoke.simulate(12);assert_valid(smoke.world);assert not smoke.geography.audit()
    result['smoke']={'hours':12,'kingdoms':4,'valid':True,'named':len(smoke.world.characters)}
    assert sources()==initial
    result['seconds']=round(time.monotonic()-started,3);write('controles.json',result)
    print(json.dumps({'controls':'passed','seconds':result['seconds']},ensure_ascii=False),flush=True)

def real_cases(e):
    w=e.world;cases=[]
    kinds={'InstitutionalTaskCompleted','InstitutionalTaskProgress','TrainingStarted','ProfessionChanged','GroupJoined',
           'NewGroupCreated','InstitutionalCaseFiled','InstitutionalCaseShared','CharacterCaptured','FactionFormalized','DivineAccessAchieved','DivineAudience','TerminalDecision'}
    selected=Counter()
    for ev in w.history:
        if ev.kind not in kinds or selected[ev.kind]>=4:continue
        selected[ev.kind]+=1
        trace=w.observability.decisions.get(ev.decision_id)
        cases.append({'event':asdict(ev),'trace':asdict(trace) if trace else None,
            'attempt':asdict(w.observability.attempts[ev.action_attempt_id]) if ev.action_attempt_id in w.observability.attempts else None,
            'receipts':[asdict(r) for r in e.observability.important_receipts.get(ev.id,())[:3]],
            'parents':[asdict(e.observability.index.events[i]) if i in e.observability.index.events else w.observability.tombstones.get(i) for i in ev.parent_event_ids]})
    return cases

def campaign(recover=False):
    green();initial=sources();controls=json.loads((OUT/'controles.json').read_text());assert initial==controls['sources']
    expected=None
    if recover:
        expected=json.loads((OUT/'falha_exportacao_300h.json').read_text())
        assert expected['hours']==300 and expected['sources']==initial and expected['seed']==SEED
        assert 'Location is not JSON serializable' in expected['exception']
    elif (OUT/'campanha.json').exists() or (OUT/'campanha_em_andamento.json').exists():raise RuntimeError('Campanha já iniciada; não repetir ou trocar seed.')
    from procedural.persistence import JsonRepository
    started=time.monotonic();checkpoint=OUT/'save_temporario.json'
    restored=bool(recover and checkpoint.exists())
    e=Engine(JsonRepository().load(checkpoint)) if restored else new(SEED,kingdoms=4)
    w=e.world
    cash=expected['initial_money'] if restored else money(w)
    source=w.metrics.get('MoneySourceAbstractWork',0)-expected['explicit_currency_source'] if restored else w.metrics.get('MoneySourceAbstractWork',0)
    result={'seed':SEED,'sources':initial,'rules':RULES_VERSION,'generation':GENERATION_VERSION,
        'generation_config':w.generation_config,'initial_named':expected['initial_named'] if restored else len(w.characters),
        'initial_abstract':expected['initial_abstract'] if restored else sum(t.abstract_population for t in w.towns.values()),
        'restarts':2 if recover else 0,'checkpoints':list(expected['checkpoints']) if restored else []}
    stable={}
    write('campanha_em_andamento.json',{'seed':SEED,'hours':w.turn,'sources':initial,'restored_checkpoint':restored})
    try:
        for _ in range(300-w.turn):
            e.step()
            if w.turn%25==0:
                assert_valid(w);assert not e.geography.audit()
                if w.turn%50==0:
                    for event in (*w.history,*w.observability.event_archive.values()):
                        stamp=digest(json.dumps(encode(event),sort_keys=True))
                        assert stable.get(event.id,stamp)==stamp,('History changed',event.id)
                        stable[event.id]=stamp
                residual=money(w)-cash-(w.metrics.get('MoneySourceAbstractWork',0)-source)
                assert residual==0,('Unexplained currency',residual)
                row={'hour':w.turn,'alive':sum(p.alive for p in w.characters.values()),'deaths':len(w.death_records),
                     'money_residual':residual,'invariants':True,'tasks':len(w.institutional_tasks)}
                result['checkpoints'].append(row);write('campanha_em_andamento.json',{'seed':SEED,'hours':w.turn,'checkpoints':result['checkpoints']})
                print(json.dumps(row),flush=True)
        # Primeiro conserva o mundo completo, inclusive se a própria análise falhar.
        if not restored:JsonRepository().save(w,checkpoint)
        assert sources()==initial
        final=summary(e);result.update(final);fill_lod(e,result)
        if expected is not None:
            for key in final:
                comparable=json.loads(json.dumps(result[key],ensure_ascii=False,default=json_value))
                if restored and key=='missing_full_payloads':continue  # Cache efêmero não é salvo.
                assert comparable==expected[key],('Reprodução divergiu nas métricas',key)
            assert result['checkpoints']==expected['checkpoints']
            result['restarts']=2
            result['export_recovery']={'same_seed':True,'same_gameplay_sources':True,'all_final_metrics_and_checkpoints_equal':True,
                'executions':3,'simulated_hours_total':900,'first_execution_completed_hours':300,'reason':'Location no exportador e comparação int/str de chaves JSON; nenhuma alteração do jogo',
                'second_execution_serialized_metrics_equal':True,'restored_checkpoint_without_simulating':restored}
        result.update(status='completed',initial_money=cash,final_money=money(w),explicit_currency_source=w.metrics.get('MoneySourceAbstractWork',0)-source)
        # Checkpoint completo ANTES de relatórios auxiliares: eventual falha
        # de exportação posterior pode ser reparada sem simular novamente.
        write('casos_reais.json',real_cases(e))
        write('detalhes_nativos.json',{'seed':SEED,'death_records':w.death_records,
            'episodes':w.observability.causal.get('episodes',{}),'native_samples':{k:v for k,v in w.observability.causal.items() if k not in ('counts','episodes','town_days','actors','deaths')},
            'tasks':[asdict(t) for t in w.institutional_tasks.values()],
            'names':{i:p.name for i,p in w.characters.items()},'town_names':{i:t.name for i,t in w.towns.items()}})
        archive={'seed':SEED,'rules':RULES_VERSION,'generation':GENERATION_VERSION,'turn':w.turn,
                 'events':w.history,'observability':w.observability}
        path=OUT/'historico_nativo.json.gz'
        with gzip.open(path,'wt',encoding='utf-8') as stream:json.dump(encode(archive),stream,ensure_ascii=False,separators=(',',':'))
        result['archive']={'path':str(path.relative_to(ROOT)),'bytes':path.stat().st_size,'sha256':digest(path.read_bytes()),'full_save':False}
        result['seconds']=round(time.monotonic()-started,3)
        write('campanha.json',result);(OUT/'campanha_em_andamento.json').unlink()
        (OUT/'save_temporario.json').unlink()
        print(json.dumps({'completed':300,'seconds':result['seconds'],'death_causes':result['death_causes']}),flush=True)
    except Exception:
        result.update(status='failed',hours=w.turn,exception=traceback.format_exc());write('campanha.json',result);raise

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('stage',choices=('controls','campaign','recover-export'))
    args=parser.parse_args()
    if args.stage=='controls':controls()
    else:campaign(recover=args.stage=='recover-export')
