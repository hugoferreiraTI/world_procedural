"""Recupera evidências da única campanha; verifica só uma continuação curta.

Não refaz os 10.000 turnos. Mantém a falha da continuidade original explícita.
"""
import gzip,hashlib,json,re,resource,time
from collections import Counter
from dataclasses import asdict,fields
from pathlib import Path
from procedural.engine import Engine
from procedural.persistence import dumps,loads
from procedural.validation import validate_world
from experiments.phase4_audit import core_hash

def recover():
    folder=Path('reports/fase_4/auditoria_global_10000h')
    progress=json.loads((folder/'progresso.json').read_text())
    assert progress['turn']==10000
    raw=(folder/'save_final.json').read_text()
    sha=hashlib.sha256(raw.encode()).hexdigest();size=len(raw.encode())
    t=time.perf_counter();w=loads(raw);load_seconds=time.perf_counter()-t
    del raw
    deaths={i:dict(r) for i,r in w.death_records.items()}
    wanted={i:asdict(r) for i,r in w.wanted_records.items()}
    emotion_causes=dict(sum((Counter(c.emotions.causes) for c in w.characters.values()),Counter()))
    t=time.perf_counter();encoded=dumps(w);save_seconds=time.perf_counter()-t
    assert hashlib.sha256(encoded.encode()).hexdigest()==sha
    del encoded
    event_count=0;counts=Counter();samples=[]
    # Só os campos escritos no log podem ser recuperados nas horas intermediárias.
    for line in (folder.parent/'auditoria_global_10000h.log').read_text().splitlines():
        match=re.fullmatch(r'(\d+)/10000h; vivos=(\d+); ataques=(\d+); migrações=(\d+); ([\d.]+)s',line)
        if match and int(match[1])%1000==0 and int(match[1])<10000:
            hour,alive,attacks,migrations,seconds=match.groups()
            samples.append({'turn':int(hour),'alive':int(alive),'dead':1728-int(alive),
                'seconds':float(seconds),'attacks':int(attacks),'migrations':int(migrations),
                'recovered_from_log':True})
    samples.append(progress)
    with gzip.open(folder/'eventos.jsonl.gz','rt') as stream:
        for line in stream:event_count+=1;counts[json.loads(line)['kind']]+=1
    with gzip.open(folder/'decisoes.jsonl.gz','rt') as stream:
        decisions=sum(1 for _ in stream)
    metrics=dict(progress['metrics']);metrics['KingdomFounded']-=6
    summary={'rules':w.rules_version,'seed':'Mira','mode':'global','hours':10000,
      'core_sha256':'1ed1227dae6b8e7a31e9b262489e0d73b2f240d06fbd94ca507d337891871b2e',
      'initial':{'alive':1728,'abstract':4338},'samples':samples,'final':progress,
      'metrics':metrics,'runtime_seconds':progress['seconds'],
      'seconds_per_1000h':round(progress['seconds']/10,3),
      'recorded_events':event_count,'recorded_decisions':decisions,'event_counts':dict(counts),
      'save_bytes':size,'save_seconds':round(save_seconds,3),'load_seconds':round(load_seconds,3),
      'persistence_timing_scope':'Serialização/carga medidas novamente no checkpoint10000h; tempos originais não foram gravados antes da falha.',
      'save_sha256':sha,'continuation_24h_equal':False,
      'continuation_scope':'A campanha completou10000h e escreveu save válido; a continuidade original versus save carregado divergiu nas24h posteriores. Não foi repetida a campanha.',
      'death_causes':dict(Counter(r['cause'] for r in deaths.values())),
      'emotion_causes':emotion_causes,'death_records':deaths,'wanted':wanted,
      'peak_after_persistence_mib':round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024,2),
      'recovered_summary':True,
      'note':'Dados oficiais pertencem ao núcleo congelado. Correções posteriores têm validação curta separada. Emoções/lesões intermediárias não são recuperáveis do log; apenas checkpoint final as preserva.'}
    (folder/'resumo.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2))
    print('Resumo recuperado; causas:',summary['death_causes'],flush=True)
    # Continuidade real de um motor em andamento contra a reconstrução no meio
    # da execução, não duas cargas idênticas comparadas desde a mesma origem.
    e=Engine(w);cache_checks=[];cache_differences=[]
    def cache_check(engine):
        canonical={(r.jurisdiction,r.suspect_id):r.id for r in engine.world.wanted_records.values()
          if r.status=='active' and engine.world.turn-r.created_at<=168}
        equal=canonical==engine.justice.active
        if not equal:
            cache_differences.append({'turn':engine.world.turn,'keys':[
                {'key':key,'expected':canonical.get(key),'actual':engine.justice.active.get(key)}
                for key in set(canonical)|set(engine.justice.active)
                if canonical.get(key)!=engine.justice.active.get(key)][:10]})
        return equal
    for _ in range(12):e.step();cache_checks.append(cache_check(e))
    resumed=loads(dumps(w));other=Engine(resumed)
    for _ in range(12):e.step();other.step();cache_checks.append(cache_check(e))
    diffs=[field.name for field in fields(w) if getattr(w,field.name)!=getattr(resumed,field.name)]
    left=dumps(w);right=dumps(resumed)
    check={'source_turn':10000,'hours':24,'reload_at':10012,'final_turn':w.turn,
       'scope':'Motor contínuo10000→10024 contra motor recarregado em10012; código corrigido, sem replay longo.',
       'core_sha256':core_hash(),'exact_equal':left==right,'different_fields':diffs,
       'justice_active_index_equal_to_world_each_hour':all(cache_checks),
       'cache_differences':cache_differences,
       'invariants':validate_world(w),'continuous_sha256':hashlib.sha256(left.encode()).hexdigest(),
       'resumed_sha256':hashlib.sha256(right.encode()).hexdigest()}
    if diffs:
        check['different_characters']=[i for i,c in w.characters.items() if c!=resumed.characters[i]][:20]
        check['metric_diff']={k:[w.metrics.get(k),resumed.metrics.get(k)] for k in set(w.metrics)|set(resumed.metrics) if w.metrics.get(k)!=resumed.metrics.get(k)}
    (folder.parent/'verificacao_continuidade_pos_auditoria.json').write_text(json.dumps(check,ensure_ascii=False,indent=2))
    print(json.dumps(check,ensure_ascii=False),flush=True)
    if not check['exact_equal'] or not all(cache_checks):raise RuntimeError('Continuidade/índice ainda diverge.')

if __name__=='__main__':recover()
