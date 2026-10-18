"""Planejamento inicial, sem reposição adaptativa automática de recursos."""
import math


def initial_water_infrastructure(world,town):
    wells=sum('Poço' in area.structures for area in world.maps[town.id].areas.values())
    persistent=len(town.resident_ids)
    # Uma unidade consumida reduz 45 de sede; fisiologia aumenta 2/h.
    # Abstratos ainda não têm fisiologia de água: não se inventa consumo.
    demand=persistent*24*2/45
    per_well=math.ceil(max(80,demand)/max(1,wells)) if wells else 0
    capacity=(80 if demand<=80 else per_well*wells) if wells else 0
    return {'water_daily':capacity,'water_storage':2*capacity,'water_work':0,
            'well_count':wells,'well_rated_daily':per_well,
            'water_design_population':persistent,'water_design_demand':demand}
