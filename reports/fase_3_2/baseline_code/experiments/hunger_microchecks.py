"""Cenários artificiais para explicar fome; usa regras intactas do motor."""
from dataclasses import asdict
import json
from pathlib import Path
from procedural.engine import Engine
from procedural.generation import GenerationConfig,generate_world
from procedural.models import Goal,Personality
from procedural.validation import validate_world

ROOT=Path(__file__).resolve().parents[1]


def fixture(hunger=100,food=1,health=2,market=True):
    e=Engine(generate_world('DiagnosticoFome',with_player=False,
             config=GenerationConfig(kingdom_count=1,historical_turns=0)))
    c=next(c for c in e.world.characters.values() if c.profession=='agricultor')
    t=e.world.towns[c.town_id]
    c.needs={};c.goal=None;c.market_observation={};c.failures={}
    c.hunger=hunger;c.thirst=c.fatigue=0;c.health=health;c.money=99
    c.starvation_hours=0;c.personality=Personality(honesty=100,independence=0,diligence=0,ambition=0)
    e.items.consume(c.id,'food',e.items.count(c.id,'food'))
    if food:e.items.create(c.id,'food',food,origin='Fixture explícita do diagnóstico')
    e.items.consume(t.id,'food',e.items.count(t.id,'food'))
    e.items.create(t.id,'food',200,origin='Fixture explícita do diagnóstico')
    e.navigation.relocate(c,t.market if market else c.home)
    e.goals.debug=True
    return e,c,t


def state(e,c):
    return {'health':c.health,'hunger':c.hunger,'thirst':c.thirst,'fatigue':c.fatigue,
            'food':e.items.count(c.id,'food'),'alive':c.alive,'position':asdict(c.position)}


def main():
    rows=[]
    for key in ('sem_fome_com_reserva','faminto_com_reserva','compra_sem_tempo_para_comer',
                'descanso_mais_antigo_empata_com_fome','viagem_continua_apesar_de_reserva'):
        e,c,t=fixture(hunger=0 if key=='sem_fome_com_reserva' else 100,
                      food=0 if key=='compra_sem_tempo_para_comer' else 1,
                      health=100 if key=='sem_fome_com_reserva' else 2,
                      market=key not in ('descanso_mais_antigo_empata_com_fome','viagem_continua_apesar_de_reserva'))
        if key=='descanso_mais_antigo_empata_com_fome':
            c.fatigue=100
            e.needs.ensure(c,'rest',100,'fixture','Descanso criado antes da fome')
            e.needs.ensure(c,'food',100,'fixture','Fome com comida carregada')
        if key=='viagem_continua_apesar_de_reserva':
            need=e.needs.ensure(c,'food',100,'fixture','Fome durante viagem')
            c.goal=Goal(e.world.allocate_id(),need.id,'buy_food',75,e.world.turn,destination=t.market)
        if key=='sem_fome_com_reserva':
            # Coloca o primeiro fechamento na hora normal de decisão deste comum.
            e.world.turn=(c.id%6-1)%6;c.last_update=e.world.turn
        before=state(e,c);e.step();after=state(e,c)
        trace=e.goals.traces.get(c.id,{'need':None,'selected':None,'active_needs':[],'candidates':[]})
        row={'case':key,'fixture':True,'before':before,'after':after,'need':trace['need'],
             'selected':trace['selected'],'priorities':trace['active_needs'],
             'candidates':trace['candidates'],'goal':asdict(c.goal) if c.goal else None,
             'validation_errors':validate_world(e.world)}
        assert not row['validation_errors']
        if key=='sem_fome_com_reserva':assert after['food']==1 and trace['selected']!='eat'
        elif key=='faminto_com_reserva':assert after['alive'] and after['hunger']==62 and trace['selected']=='eat'
        elif key=='compra_sem_tempo_para_comer':assert not after['alive'] and after['food']==1 and trace['selected']=='buy_food'
        elif key=='descanso_mais_antigo_empata_com_fome':assert not after['alive'] and after['food']==1 and trace['selected']=='sleep'
        elif key=='viagem_continua_apesar_de_reserva':assert not after['alive'] and after['food']==1 and trace['selected']=='buy_food'
        rows.append(row)
    dest=ROOT/'reports/diagnostico_fome';dest.mkdir(exist_ok=True)
    (dest/'microverificacoes.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print([{k:r[k] for k in ('case','selected','after')} for r in rows])


if __name__=='__main__':main()
