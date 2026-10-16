"""Reproduções pequenas, separadas da campanha observada; nenhum save carregado."""
import json
from dataclasses import replace
from pathlib import Path
from procedural.engine import Engine
from procedural.generation import generate_world,GenerationConfig
from procedural.models import Goal

def fresh(seed):
    w=generate_world(seed,with_player=False,config=GenerationConfig(kingdom_count=1,historical_turns=0))
    return w,Engine(w)

def execute(e,p,action,target=None,need=None):
    return e.goals.execute(p,Goal(e.world.allocate_id(),need.id if need else 0,action,0,e.world.turn,target),1)

def duplicate_case():
    w,e=fresh('Micro-Lore-Autoridade')
    g=next(p for p in w.characters.values() if p.profession=='guarda')
    town=w.towns[g.town_id]
    suspect=next(p for p in w.characters.values() if p.town_id==town.id and p.id!=g.id and p.money>=10)
    for p in w.characters.values():e.navigation.relocate(p,p.home)
    for p in (g,suspect):e.navigation.relocate(p,town.market)
    initial_money=suspect.money
    assert execute(e,suspect,'steal')[0]
    old=e.justice.record_for(g,suspect.id);fact=g.knowledge[old.originating_fact]
    e.needs.refresh(g);assert execute(e,g,'secure',suspect.id,g.needs['security'])[0]
    after_fine=suspect.money
    known_status=old.known_status[g.id]
    # Simula o envelhecimento/evicção da memória curta, mantendo o caso julgado.
    w.turn=250;g.knowledge.pop(fact.event_id,None)
    e.knowledge.learn(g,replace(fact,source_kind='trusted',confidence=80),False)
    reopened=e.justice.record_for(g,suspect.id)
    before_capture=suspect.money
    if reopened:
        assert execute(e,suspect,'surrender',g.id)[0]
        capture=execute(e,g,'capture',suspect.id)
    else:capture=(False,'Caso antigo corretamente rejeitado.')
    return {'scenario':'Mesmo guarda reaprende o mesmo roubo depois de encerrar seu caso e perder a memória curta.',
      'loaded_save':False,'controlled_clock':250,'theft_events':w.metrics.get('ItemStolen',0),
      'source_fact_id':fact.event_id,'source_fact_turn':fact.turn,'guard_id':g.id,'suspect_id':suspect.id,
      'first_record':old.id,'first_known_status_after_fine':known_status,
      'reopened_record':reopened.id if reopened else None,
      'reopened_source':reopened.originating_fact if reopened else None,
      'capture_success':capture[0],'money_initial':initial_money,'money_after_first_fine':after_fine,
      'money_before_second_capture':before_capture,'money_after_second_capture':suspect.money,
      'same_old_fact_punished_again':bool(reopened and reopened.originating_fact==fact.event_id and suspect.money<before_capture)}

def residence_edges():
    w,e=fresh('Micro-Lore-Residencia')
    p=next(p for p in w.characters.values() if len(p.known_towns)>=2)
    origin=p.town_id;destinations=list(p.known_towns)[:2];visits=[]
    # Recursos de fixture para isolar residência; não pertencem à campanha.
    e.items.create(p.id,'food',12);e.items.create(p.id,'water',12)
    for destination in destinations:
        assert e.migration.execute(p,destination)[0]
        for _ in range(300):
            w.turn+=1;e.migration.execute(p,destination)
            if p.migration.arrived_at is not None:break
        assert p.migration.arrived_at is not None
        w.turn+=24;assert e.migration.settle(p);visits.append(destination)
    edges=[{'town':r.target_id,'value':r.value,'kind':r.kind} for r in w.relationships.values()
           if r.source_id==p.id and r.kind in ('reside_em','residente_de') and r.value>0]
    return {'scenario':'Duas mudanças físicas, com chegada e permanência; conferir censo e grafo.',
      'loaded_save':False,'fixture_resources':True,'person':p.id,'original_town':origin,'visited_towns':visits,
      'actual_town':p.town_id,'census_towns':[t.id for t in w.towns.values() if p.id in t.resident_ids],
      'positive_residence_edges':edges,'graph_has_multiple_current_residences':len(edges)>1}

def apology_reputation():
    w,e=fresh('Micro-Lore-Desculpa')
    p=next(iter(w.characters.values()));q=next(x for x in w.characters.values() if x.id!=p.id and x.town_id==p.town_id)
    for x in (p,q):e.navigation.relocate(x,w.towns[p.town_id].market)
    before=e.social.reputation(q,p.id)
    assert execute(e,p,'apologize',q.id)[0]
    r=q.reputations[p.id]
    return {'scenario':'Pedido de desculpas: interpretação reputacional de reparação.',
      'actor':p.id,'receiver':q.id,'tags':dict(r.tags),'fear':r.fear,'admiration':r.admiration,
      'reputation_before':before,'reputation_after':e.social.reputation(q,p.id),
      'apology_increases_fear':r.fear>0,'loaded_save':False}

def resolved_notice():
    w,e=fresh('Micro-Lore-Aviso-Encerrado')
    g=next(p for p in w.characters.values() if p.profession=='guarda');town=w.towns[g.town_id]
    suspect=next(p for p in w.characters.values() if p.town_id==town.id and p.id!=g.id and p.money>=10)
    for p in w.characters.values():e.navigation.relocate(p,p.home)
    for p in (g,suspect):e.navigation.relocate(p,town.market)
    assert execute(e,suspect,'steal')[0]
    record=e.justice.record_for(g,suspect.id)
    notice=next(f for f in g.knowledge.values() if f.kind=='WantedIssued' and f.context['record_id']==record.id)
    e.needs.refresh(g);assert execute(e,g,'secure',suspect.id,g.needs['security'])[0]
    closed=record.known_status[g.id];before=suspect.money
    w.turn=1;g.knowledge.pop(notice.event_id,None)
    e.knowledge.learn(g,replace(notice,source_kind='trusted',confidence=80),False)
    reopened=e.justice.record_for(g,suspect.id)
    assert execute(e,suspect,'surrender',g.id)[0]
    result=execute(e,g,'capture',suspect.id)
    return {'scenario':'Mesmo guarda reaprende seu aviso WantedIssued após resolver o caso, ainda dentro de 168h.',
      'loaded_save':False,'controlled_clock':1,'record':record.id,'notice_event_id':notice.event_id,
      'known_status_before':closed,'known_status_after_relearn':'active' if reopened else 'resolved',
      'global_status':record.status,'same_record_reactivated':reopened is record,
      'second_capture_success':result[0],'money_before_second_capture':before,'money_after_second_capture':suspect.money}

if __name__=='__main__':
    result={'authority_reopening':duplicate_case(),'residence_graph':residence_edges(),
            'apology_reputation':apology_reputation(),'resolved_notice_reactivation':resolved_notice()}
    Path('reports/lore_microchecks.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
    print(json.dumps(result,ensure_ascii=False,indent=2))
