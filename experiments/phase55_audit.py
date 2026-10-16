"""Uma campanha natural nova de 300h. Evidência compacta e retenção curta do save."""
from collections import Counter
from dataclasses import asdict
import hashlib,json,time
from pathlib import Path
from procedural.generation import generate_world,GenerationConfig
from procedural.engine import Engine
from procedural.persistence import JsonRepository
from procedural.validation import validate_world

BASE=Path(__file__).resolve().parents[1]
OUT=BASE/'reports/fase_5_5/campanha_300h'
SEED='Vaelora-55'
HOURS=300
KINDS={'GroupSearchAttempt','NewGroupCreated','ExistingGroupFound','GroupJoined','GroupJoinRejected','GroupDissolved','GroupMeeting',
       'ProposalCreated','CompatibleProposalFound','ProposalSupported','ProposalSupportDelivered','ProposalSubmitted',
       'PoliticalPressureChanged','PolicyDecided','PolicyCreated','PolicyEffect','PolicyBlocked','PolicyCompleted','PolicyTransportAssigned','FactionProposalSupported',
       'FactionInvite','FactionJoinRequest','FactionMembershipAccepted','FactionMembershipRejected','FactionMembershipDeferred',
       'FactionMembershipConditioned','FormalizationConsidered','FactionFormalized','FactionAction','FactionLocalStatusChanged','CharacterKilled',
       'JourneyStarted','JourneyArrived','DivineIntervention','DivineAudience','DivineContract','DivineManifestation'}

def fingerprint():
 h=hashlib.sha256()
 for p in sorted((BASE/'procedural').glob('*.py')):h.update(p.name.encode());h.update(p.read_bytes())
 return h.hexdigest()

def main():
 OUT.mkdir(parents=True,exist_ok=True)
 if (OUT/'manifesto.json').exists():raise RuntimeError('Campanha já existe: preservar execução anterior antes de qualquer reinício estrutural.')
 start=time.monotonic();code=fingerprint();w=generate_world(SEED,with_player=False,config=GenerationConfig(historical_turns=0));e=Engine(w)
 initial={'named':len(w.characters),'abstract':sum(t.abstract_population for t in w.towns.values()),'localities':len(w.towns),'kingdoms':len(w.kingdoms)}
 manifest={'seed':SEED,'rules':w.rules_version,'hours':HOURS,'code_sha256':code,'initial':initial,
           'restarts':1 if (OUT.parent/'interrompida_50h/falha.json').exists() else 0}
 (OUT/'manifesto.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
 counts=Counter();relevant=[];checks=[]
 def observe(ev):
  counts[ev.kind]+=1
  if ev.kind in KINDS:relevant.append(asdict(ev))
 e.bus.subscribe('*',observe)
 print(json.dumps({'started':SEED,**initial}),flush=True)
 try:
  for _ in range(HOURS):
   e.step()
   if w.turn%50==0:
    errors=validate_world(w);checks.append({'hour':w.turn,'errors':errors})
    if errors:raise RuntimeError(str(errors[:6]))
    print(json.dumps({'hour':w.turn,'alive':sum(c.alive for c in w.characters.values()),'groups':counts['NewGroupCreated'],'joins':counts['GroupJoined'],'proposals':counts['ProposalCreated'],'reuse':counts['CompatibleProposalFound'],'policies':counts['PolicyCreated'],'effects':counts['PolicyEffect'],'memberships':counts['FactionMembershipAccepted']}),flush=True)
  assert fingerprint()==code,'Código alterado durante a campanha.'
  audit=e.geography.audit()
  if audit:raise RuntimeError(str(audit[:5]))
 except Exception as ex:
  (OUT/'falha.json').write_text(json.dumps({'seed':SEED,'hour':w.turn,'error':repr(ex),'checks':checks},ensure_ascii=False,indent=2))
  raise
 chars={c.id:{k:getattr(c,k) for k in ('name','profession','town_id','alive','religion','mythic_trait','mythic_development')} for c in w.characters.values()}
 data={**manifest,'completed_hours':w.turn,'runtime_seconds':round(time.monotonic()-start,2),'events':dict(counts),'checks':checks,'route_errors':audit,
       'final_named':sum(c.alive for c in w.characters.values()),'final_abstract':sum(t.abstract_population for t in w.towns.values()),'characters':chars,
       'kingdoms':[{k:getattr(x,k) for k in ('id','name','capital_id','city_ids','village_ids','ruler_id','political_state','economic_state','military_state')} for x in w.kingdoms.values()],
       'towns':[{'id':t.id,'name':t.name,'capital':t.capital,'kind':t.kind,'kingdom_id':t.kingdom_id,'named':sum(w.characters[i].alive for i in t.resident_ids),'abstract':t.abstract_population,'money':t.money,'food':e.items.count(t.id,'food'),'water':e.items.count(t.id,'water'),'infrastructure':t.infrastructure,'mayor':t.mayor_id} for t in w.towns.values()],
       'groups':[{k:getattr(g,k) for k in ('id','name','town_id','cause','leader_id','member_ids','status','created_at','pressure','failures','investment','proposal_ids','money')} for g in w.groups.values()],
       'proposals':[asdict(x) for x in w.proposals.values()],'policies':[asdict(x) for x in w.institutional_policies.values()],
       'factions':[{**{k:getattr(f,k) for k in ('id','name','leader_id','headquarters_id','member_ids','status','purpose','money','norms','local_status')},'inventory':{kind:e.items.count(f.id,kind) for kind in ('food','water','weapon','tool','grain')},'capabilities':e.institutions.capabilities(f,w.characters[f.leader_id])} for f in w.factions.values()],
       'deaths':dict(Counter(x['cause'] for x in w.death_records.values())),
       'gods':[{k:getattr(g,k) for k in ('id','name','domain','alive','energy','bonds')} for g in w.divinities.values()],
       'followers':{g.id:sum(p.alive and p.beliefs.get(g.id,{}).get('believed_divine',False) for p in w.characters.values()) for g in w.divinities.values()},
       'points':[{k:getattr(p,k) for k in ('id','name','kind','claimant_id','history')} for p in w.points.values()],
       'routes':{'count':len(w.routes),'traversals':sum(x.uses for x in w.routes.values())}}
 (OUT/'resumo.json').write_text(json.dumps(data,ensure_ascii=False,indent=2))
 (OUT/'eventos_para_selecao.json').write_text(json.dumps(relevant,ensure_ascii=False,indent=2))
 JsonRepository().save(w,OUT/'save_final.json')
 print(json.dumps({'completed':w.turn,'seconds':data['runtime_seconds'],'save_bytes':(OUT/'save_final.json').stat().st_size,'evidence_events':len(relevant)}),flush=True)

if __name__=='__main__':main()
