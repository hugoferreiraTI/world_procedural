"""Recupera apenas métricas/checkpoint já obtidos; não repete a campanha curta."""
import gzip,hashlib,json,time,resource
from pathlib import Path
from collections import Counter
from dataclasses import asdict
from procedural.persistence import dumps,loads
from procedural.engine import Engine
p=Path('reports/fase_4/auditoria_curta')
raw=(p/'save_final.json').read_text();t=time.perf_counter();w=loads(raw);load_seconds=time.perf_counter()-t
progress=json.loads((p/'progresso.json').read_text())
events=0;event_counts=Counter()
with gzip.open(p/'eventos.jsonl.gz','rt') as f:
 for line in f:
  events+=1;event_counts[json.loads(line)['kind']]+=1
with gzip.open(p/'decisoes.jsonl.gz','rt') as f:decisions=sum(1 for _ in f)
t=time.perf_counter();encoded=dumps(w);save_seconds=time.perf_counter()-t
copy=loads(encoded);e1=Engine(w);e2=Engine(copy);e1.simulate(24);e2.simulate(24)
equal=dumps(w)==dumps(copy)
metrics=dict(progress['metrics']);metrics['KingdomFounded']-=6
summary={'rules':w.rules_version,'seed':'Mira','mode':'global','hours':1000,
'core_sha256':None,'note':'Auditoria concluída em1000h; callback observacional permaneceu em arquivo fechado e falhou na continuação pós-checkpoint. Motor/checkpoint1000h válidos. Instrumentação corrigida; somente teste24h recuperado, sem repetir campanha. Código recebeu correções de regressão/performance depois deste checkpoint.',
'initial':{'alive':1728,'abstract':4338},'final':progress,'samples':[progress],
'runtime_seconds':progress['seconds'],'seconds_per_1000h':progress['seconds'],
'metrics':metrics,'recorded_events':events,'recorded_decisions':decisions,
'save_bytes':len(raw.encode()),'save_seconds':save_seconds,'load_seconds':load_seconds,
'save_sha256':hashlib.sha256(raw.encode()).hexdigest(),'continuation_24h_equal':equal,
'continuation_scope':'Estado1000h carregado e serializado novamente contra cópia carregada, sob correções atuais; não é replay da campanha completa.',
'death_causes':dict(Counter(r['cause'] for r in loads(raw).death_records.values())),
'event_counts':dict(event_counts),'memory_peak_mib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024}
(p/'resumo.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2))
print(json.dumps({k:summary[k] for k in ('hours','runtime_seconds','death_causes','continuation_24h_equal','save_bytes')},ensure_ascii=False),flush=True)
