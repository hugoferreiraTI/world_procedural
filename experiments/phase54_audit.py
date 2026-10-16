"""Uma campanha natural de 200h, com dados compactos para os três relatórios."""
import hashlib
import json
from collections import Counter,defaultdict
from dataclasses import asdict
from pathlib import Path
import time

from procedural.engine import Engine
from procedural.generation import GenerationConfig,generate_world
from procedural.persistence import JsonRepository
from procedural.validation import validate_world

BASE=Path(__file__).resolve().parents[1]
OUT=BASE/'reports/fase_5_4/campanha_200h'
SEED='Arandor-54'
HOURS=200
SPATIAL={'JourneyStarted','JourneyArrived','RouteTraversed','RouteKnowledgeShared','AskRoute','RouteUnknownBlockedTravel','MultiHopJourney','FollowJourney','EscortJourney','MigrationStarted','MigrationArrived','ResidentMoved','POIDiscovered','POIVisited','POIExplored','POIClaimed','POIClaimContested','ExpeditionFormed','FactionKnown','FactionRecruitmentInterest','FactionInvite','FactionJoinRequest','FactionMemberJoined','GroupFormalized','FactionHQChanged','SeekDivineContact','SacredJourney','DivineAccessAchieved','DivineAudience','DivineContract','DivineContractOffered','DivineManifestation','CharacterKilled','CharacterDied','ProposalSubmitted','PolicyDecided'}
def fingerprint():
 h=hashlib.sha256()
 for p in sorted((BASE/'procedural').glob('*.py')):h.update(p.name.encode());h.update(p.read_bytes())
 return h.hexdigest()
def census(e):
 w=e.world
 return [{'id':t.id,'name':t.name,'kind':'capital' if t.capital else t.kind,'kingdom':t.kingdom_id,'named':sum(w.characters[i].alive for i in t.resident_ids),'abstract':t.abstract_population,'population':t.population,'mayor':t.mayor_id,'general':t.general_id,'authority':t.authority_town_id,'food':e.items.count(t.id,'food')} for t in w.towns.values()]
def main():
 OUT.mkdir(parents=True,exist_ok=True)
 code=fingerprint();start=time.monotonic()
 w=generate_world(SEED,with_player=False,config=GenerationConfig(historical_turns=0));e=Engine(w)
 initial=census(e);initial_metrics=dict(w.metrics);cutoff=w.next_id
 result={'seed':SEED,'hours_requested':HOURS,'rules':w.rules_version,'code_sha256':code,'initial':initial,'initial_metrics':initial_metrics,'initial_event_cutoff':cutoff,'errors':[]}
 (OUT/'manifesto.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
 counts=Counter();places=defaultdict(Counter);spatial=[];checks=[]
 def observe(ev):
  counts[ev.kind]+=1
  if ev.location:places[ev.location.map_id][ev.kind]+=1
  if ev.kind in SPATIAL:spatial.append(asdict(ev))
 e.bus.subscribe('*',observe)
 print(json.dumps({'seed':SEED,'named':len(w.characters),'localities':len(w.towns),'routes':len(w.routes)}),flush=True)
 try:
  for _ in range(HOURS):
   e.step()
   if w.turn%25==0:
    errors=validate_world(w)
    checks.append({'hour':w.turn,'errors':errors})
    if errors:raise RuntimeError(str(errors[:8]))
    print(json.dumps({'hour':w.turn,'alive':sum(c.alive for c in w.characters.values()),'journeys':counts['JourneyStarted'],'arrivals':counts['JourneyArrived'],'joins':counts['FactionMemberJoined']}),flush=True)
  errors=e.geography.audit()
  if errors:raise RuntimeError(str(errors[:8]))
  if fingerprint()!=code:raise RuntimeError('Regras foram alteradas durante a campanha.')
 except Exception as ex:
  result['errors'].append({'hour':w.turn,'error':repr(ex)})
  (OUT/'falha.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
  raise
 result.update(hours=w.turn,events=dict(counts),metrics={k:v-initial_metrics.get(k,0) for k,v in w.metrics.items()},final=census(e),place_events={k:dict(v) for k,v in places.items()},checks=checks,route_audit=errors,runtime_seconds=round(time.monotonic()-start,2),
  characters={c.id:{k:getattr(c,k) for k in ('id','name','profession','town_id','alive','religion','devotion','mythic_trait','mythic_development','money')} for c in w.characters.values()},
  kingdoms=[{k:getattr(v,k) for k in ('id','name','capital_id','city_ids','village_ids','ruler_id','political_state','economic_state','military_state','religion')} for v in w.kingdoms.values()],
  factions=[{k:getattr(f,k) for k in ('id','name','leader_id','headquarters_id','member_ids','purpose','ranks','assignments','money','inventory','status','norms')} for f in w.factions.values()],
  groups=[{k:getattr(g,k) for k in ('id','name','cause','town_id','leader_id','member_ids','status','created_at','plan')} for g in w.groups.values()],
  points=[asdict(p) for p in w.points.values()],routes=[asdict(x) for x in w.routes.values()],
  gods=[{k:getattr(g,k) for k in ('id','name','domain','alive','energy','affinities','presence_regions','bonds')} for g in w.divinities.values()],
  contracts=[asdict(c) for c in w.divine_contracts.values()],deaths=list(w.death_records.values()),
  social_veneration=[{'observer':p.id,'subject':id,**b} for p in w.characters.values() for id,b in p.beliefs.items() if b.get('interpretation')=='social_veneration'],
  traveling=[{'actor':p.id,**asdict(p.journey)} for p in w.characters.values() if p.alive and p.journey],
  route_sources=dict(Counter(rk.source for p in w.characters.values() for rk in p.route_knowledge.values())),
  religion={g.id:{'followers':sum(p.alive and p.beliefs.get(g.id,{}).get('believed_divine',False) and p.beliefs[g.id].get('confidence',0)>=30 for p in w.characters.values()),'cultists':sum(p.alive and w.turn-p.social_state.get('religious_activity',{}).get(g.id,{}).get('last_cult',-1000)<=200 for p in w.characters.values())} for g in w.divinities.values()})
 (OUT/'resultado.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
 (OUT/'eventos_espaciais.json').write_text(json.dumps(spatial,ensure_ascii=False,indent=2))
 JsonRepository().save(w,OUT/'save_final.json')
 print(json.dumps({'completed':w.turn,'seconds':result['runtime_seconds'],'save_bytes':(OUT/'save_final.json').stat().st_size,'route_errors':len(errors)}),flush=True)

if __name__=='__main__':main()
