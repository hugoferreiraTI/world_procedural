"""Reproduções controladas de auditoria; zero horas naturais, núcleo intacto."""
import json
import sys
from pathlib import Path

from procedural.engine import Engine
from procedural.persistence import dumps, loads
from .total_static import ROOT, fingerprint

def run():
    sys.path.insert(0,str(ROOT/'tests'))
    from test_phase55 import InstitutionalTests
    before=fingerprint()
    x=InstitutionalTests();x.setUp()
    x.share(x.q)
    n=x.e.needs.ensure(x.p,'political_pressure',70,'fixture','Criar grupo controlado')
    g=x.e.society.form(x.p,'security',None,n)
    assert g and g.member_ids==[x.p.id,x.q.id]
    event=next(e for e in x.w.history if e.kind=='GroupFormed' and e.target_id==g.id)
    initial=list(event.context['members'])
    # A fixture chama serviços fora de Engine.step/execute; sincronizar antes
    # do snapshot para não confundir RNG antigo da fixture com bug de load.
    x.w.rng_state=x.e.rng.getstate()
    loaded=loads(dumps(x.w));other=Engine(loaded)
    assert dumps(x.w)==dumps(loaded) and x.e.rng.getstate()==other.rng.getstate()
    for e in (x.e,other):
        person=e.world.characters[x.r.id];group=e.world.groups[g.id]
        e.institutions.know_group(person,group,'controlled_contact')
        assert e.institutions.join(person,group)[0]
    restored=next(e for e in loaded.history if e.id==event.id)
    row={'controlled_fixture':True,'natural_hours':0,'rng_synchronized_before_snapshot':True,
         'event':event.id,'kind':event.kind,'members_at_original_emission':initial,
         'live_original_context_members':list(event.context['members']),
         'loaded_context_members':list(restored.context['members']),
         'current_group_members_original':list(g.member_ids),
         'current_group_members_loaded':list(loaded.groups[g.id].member_ids),
         'rng_equal':x.e.rng.getstate()==other.rng.getstate(),
         'worlds_equal_after_same_join':dumps(x.w)==dumps(loaded),
         'main_changed':fingerprint()!=before}
    assert row['rng_equal'] and not row['worlds_equal_after_same_join']
    assert row['live_original_context_members']!=row['loaded_context_members']
    # Um relato religioso é enumerável por um estado realmente construído com
    # orações presenciadas e notícias locais de duas mortes; nenhuma hora passa.
    god=next(iter(x.w.divinities.values()))
    for p in (x.p,x.q,x.r):x.e.navigation.relocate(p,x.p.known_places['sacred'])
    for p in (x.q,x.r):
        x.e.recorder.emit('PrayerOffered','Oração presenciada no controle.',p.id,god.id,p.position,
                          context={'request':'sign','offering':0,'reported_severity':0})
        p.health=0;p.hunger=100
        x.e.finish_death(p,'deprivation')
    n=x.e.needs.ensure(x.p,'religious_interest',60,'controlled_loss','Relatar congregação conhecida',god.id)
    options=[a for a,d,t in x.e.faith.candidates(x.p,n)]
    assert 'report_congregation' in options
    try:x.e.goals.solutions(x.p,n)
    except KeyError as error:missing=str(error)
    else:raise AssertionError('A ausência da ação em Utility.BASE deixou de reproduzir')
    assert missing=="'report_congregation'"
    missing_action={'controlled_fixture':True,'natural_hours':0,'producer':'FaithSystem.candidates',
                    'options':options,'path':'GoalSystem.solutions → _evaluate → utility.evaluate',
                    'exception':'KeyError: '+missing,'reason':'report_congregation não possui Utility.BASE'}
    x.p.health=0
    x.e.finish_death(x.p,'exploration')
    death=next(e for e in reversed(x.w.history) if e.kind=='CharacterDied' and e.target_id==x.p.id)
    exploration={'controlled_fixture':True,'natural_hours':0,'cause':death.context['cause'],
                 'description':death.description,'contradiction':'causa exploration descrita como autoinfligida'}
    assert exploration['cause']=='exploration' and 'autoinfligida' in exploration['description']
    assert fingerprint()==before
    result={'mutable_event_payload':row,'missing_religious_utility_action':missing_action,'exploration_death_description':exploration,
            'reproduction_command':'PYTHONDONTWRITEBYTECODE=1 python3 -m experiments.total_proofs'}
    Path('/tmp/procedural_total_proofs.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
    print(json.dumps(result,ensure_ascii=False))

if __name__=='__main__':run()
