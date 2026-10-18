"""Invariantes usadas tanto por testes longos quanto pelo carregamento de saves."""

from dataclasses import fields

from .knowledge import KNOWLEDGE_LIMIT, MEMORY_LIMIT
from .navigation import passable


def validate_world(world) -> list[str]:
    errors = []
    groups = (world.characters, world.towns, world.kingdoms, world.factions, world.points, world.items, world.groups, world.proposals, world.divinities, world.routes, world.divine_contracts, world.institutional_policies, world.institutional_tasks)
    entity_ids = {world.world_map_id}
    for group in groups:
        for key, entity in group.items():
            if key != entity.id or key in entity_ids:
                errors.append(f"ID inválido ou duplicado: {key}")
            entity_ids.add(key)
    for task in world.institutional_tasks.values():
        institution=world.groups.get(task.institution_id) if task.institution_type=='group' else world.towns.get(task.institution_id)
        if (not institution and task.status in ('pending','blocked')) or task.issuer not in world.characters or task.status not in ('pending','blocked','completed','cancelled') or task.attempts<0:
            errors.append('Obrigação institucional inválida.')
        if not passable(world,task.location):errors.append('Local de obrigação inacessível.')
    if world.world_map_id not in world.maps:
        errors.append("Mapa global ausente.")
    if world.player_id is not None and (world.player_id not in world.characters or
                                       not world.characters[world.player_id].is_player):
        errors.append("Referência ao jogador inválida.")
    if world.primordial_id not in world.characters:
        errors.append("Personagem primordial ausente.")
    for map_id, grid in world.maps.items():
        if (map_id != grid.id or grid.width <= 0 or grid.height <= 0 or
                len(grid.rows) != grid.height or any(len(row) != grid.width for row in grid.rows)):
            errors.append(f"Matriz inválida: {map_id}")
        if grid.exit_to and not passable(world, grid.exit_to):
            errors.append(f"Saída inválida: {map_id}")
    for relation in world.relationships.values():
        if relation.source_id not in entity_ids or relation.target_id not in entity_ids:
            errors.append("Relação referencia entidade inexistente.")
        if not (-100 if relation.kind in ("diplomacia","afinidade_divina") else 0) <= relation.value <= 100:
            errors.append("Valor de relacionamento fora da escala.")
    inventory_ids = set()
    auxiliary_ids = set()
    for owner in (*world.characters.values(), *world.towns.values(), *world.kingdoms.values(), *world.groups.values(), *world.factions.values(), *world.points.values()):
        if hasattr(owner, "inventory"):
            for item_id, quantity in owner.inventory.items():
                item = world.items.get(item_id)
                if item is None or item.owner_id != owner.id or quantity <= 0 or item_id in inventory_ids:
                    errors.append(f"Referência de inventário inválida: {item_id}")
                if item and not item.stackable and quantity != 1:
                    errors.append(f"Item único empilhado: {item_id}")
                inventory_ids.add(item_id)
        if hasattr(owner, "money") and owner.money < 0:
            errors.append(f"Dinheiro negativo: {owner.id}")
        for need in owner.needs.values():
            if need.id in entity_ids or need.id in auxiliary_ids or need.owner_id != owner.id:
                errors.append(f"ID ou dono inválido da necessidade: {need.id}")
            auxiliary_ids.add(need.id)
            if need.target_id is not None and need.target_id not in entity_ids:
                errors.append(f"Alvo inválido da necessidade: {need.id}")
            if not 0 <= need.priority <= 100 or not 0 <= need.base_urgency <= 100:
                errors.append(f"Prioridade inválida: {need.id}")
        if owner.goal:
            goal = owner.goal
            if goal.id in entity_ids or goal.id in auxiliary_ids:
                errors.append(f"ID de objetivo duplicado: {goal.id}")
            auxiliary_ids.add(goal.id)
            if goal.need_id not in {need.id for need in owner.needs.values()}:
                errors.append(f"Objetivo sem necessidade: {goal.id}")
    if inventory_ids != set(world.items):
        errors.append("Existem itens sem inventário proprietário.")
    for item in world.items.values():
        if item.creator_id is not None and item.creator_id not in world.characters:
            errors.append(f"Criador inexistente: {item.id}")
        if not 0 <= item.quality <= 100:
            errors.append(f"Qualidade fora da escala: {item.id}")
    for character in world.characters.values():
        if not passable(world, character.position):
            errors.append(f"Personagem fora de área acessível: {character.id}")
        if not 0 <= character.health <= 100 or character.alive != (character.health > 0):
            errors.append(f"Estado de vida inválido: {character.id}")
        if any(not 0 <= level <= 100 for level in (character.hunger, character.thirst, character.fatigue)):
            errors.append(f"Necessidade fisiológica fora da escala: {character.id}")
        if any(not 0 <= getattr(character.personality, trait.name) <= 100 for trait in fields(character.personality)):
            errors.append(f"Traço de personalidade fora da escala: {character.id}")
        if len(character.memories) > MEMORY_LIMIT or len(character.knowledge) > KNOWLEDGE_LIMIT:
            errors.append(f"Memórias sem limite: {character.id}")
        if character.town_id not in world.towns:
            errors.append(f"Cidade natal inexistente: {character.id}")
        if character.faction is not None and character.faction not in (*world.kingdoms, *world.factions):
            errors.append(f"Facção inexistente: {character.id}")
        if character.starvation_hours < 0:
            errors.append(f"Duração de privação inválida: {character.id}")
        if (not 0 <= character.recoverable_deprivation_damage <= 100-character.health or
                any(k not in ('hunger','thirst','both','combat') or v < 0 for k,v in character.damage_by_origin.items())):
            errors.append(f'Origem de dano inválida: {character.id}')
        if len(character.commitments)>4 or len(character.aspirations)>2:
            errors.append(f'Intenções sem limite: {character.id}')
        for key,c in character.commitments.items():
            if (key!=c.id or c.id in entity_ids or c.id in auxiliary_ids or c.owner_id!=character.id
                    or c.originating_need not in {n.id for n in character.needs.values()}
                    or c.target_id is not None and c.target_id not in entity_ids
                    or c.status not in ('active','paused','waiting_for_information','satisfied','abandoned','expired')
                    or not 0<=c.intensity<=100 or not 0<=c.abandonment_pressure<=100
                    or min(c.progress,c.failures,c.setbacks,c.investment,c.activity_count,c.meaningful_progress)<0):
                errors.append(f'Compromisso inválido: {character.id}')
            auxiliary_ids.add(c.id)
            if c.status in ('active','paused','waiting_for_information') and c.originating_fact is not None and c.originating_fact not in character.knowledge:
                errors.append(f'Compromisso sem causa lembrada: {c.id}')
            if c.status in ('active','paused','waiting_for_information') and any(i not in character.knowledge for i in c.context.get('supporting_facts',[])):
                errors.append(f'Compromisso sem evidência complementar: {c.id}')
        for c in character.commitments.values():
            search=c.context.get('investigation',{})
            if len(search.get('clues',[]))>3 or len(search.get('asked',[]))>8 or len(search.get('areas',[]))>4:
                errors.append(f'Investigação sem limite: {c.id}')
            for clue in search.get('clues',[]):
                if clue.subject_id not in world.characters or not passable(world,clue.location) or not 0<=clue.confidence<=100 or clue.observed_at>world.turn:
                    errors.append(f'Pista inválida: {c.id}')
        if any(not 0<=a.intensity<=100 or not 0<=a.progress<=1 or
               a.status not in ('active','satisfied','abandoned') for a in character.aspirations):
            errors.append(f'Aspiração inválida: {character.id}')
        if any(i not in world.characters or intent not in ('repel','contain','subdue','hurt','kill')
               for i,intent in character.combat.violence_intents.items()):
            errors.append(f'Intenção de violência inválida: {character.id}')
        if len(character.lethal_decisions)>4 or not 0<=character.death_affinity<=100:
            errors.append(f'Estado de decisão/morte fora do limite: {character.id}')
        for target,d in character.lethal_decisions.items():
            if (target!=d.target_id or d.actor_id!=character.id or target not in world.characters
                    or d.id in entity_ids or d.id in auxiliary_ids or d.mode not in
                    ('reactive_threat','retributive','protective','instrumental','moral_punishment','hedonic')
                    or d.status not in ('active','abandoned','resolved') or len(d.facts)>3
                    or not 0<=d.rumination<=100 or not 0<=d.intensity<=100 or not 0<=d.confidence<=100
                    or d.status=='active' and any(i not in character.knowledge for i in d.facts)):
                errors.append(f'Decisão letal inválida: {character.id}')
            auxiliary_ids.add(d.id)
        if len(character.death_state.get('appraisals',[]))>4 or len(character.death_state.get('kill_facts',[]))>8:
            errors.append(f'Avaliação de morte sem limite: {character.id}')
        emotion=character.emotions
        if (any(v < 0 or v > 100 for v in emotion.despair_sources.values()) or
                sum(emotion.despair_sources.values()) > 100.00001 or emotion.stable_material_hours < 0):
            errors.append(f'Fontes de desespero inválidas: {character.id}')
        if any(not 0<=getattr(emotion,k)<=100 for k in ('anger','resentment','humiliation','desperation')):
            errors.append(f'Emoção fora da escala: {character.id}')
        if len(character.grievances)>16 or len(emotion.processed)>128 or not 0<=emotion.adaptation<=5:
            errors.append(f'Estado emocional sem limite: {character.id}')
        if any(i not in world.characters or g.target_id!=i or not 0<=g.intensity<=100
               for i,g in character.grievances.items()):
            errors.append(f'Grievance inválida: {character.id}')
        combat=character.combat
        if (not 0<=combat.injured<=100 or len(set(combat.opponents))!=len(combat.opponents) or
                any(i not in world.characters or i==character.id for i in combat.opponents) or
                not character.alive and combat.opponents or
                combat.captor_id is not None and combat.captor_id not in world.characters):
            errors.append(f'Estado de confronto inválido: {character.id}')
        if character.lod not in ('active','local','background'):
            errors.append(f'LOD inválido: {character.id}')
        if any(i not in world.towns or not 0<=known.get('confidence',0)<=100
               for i,known in character.known_towns.items()):
            errors.append(f'Destino conhecido inválido: {character.id}')
        migration=character.migration
        if migration and (migration.origin_id!=character.town_id or migration.destination_id not in world.towns or
                          migration.origin_id==migration.destination_id or migration.started_at>world.turn):
            errors.append(f'Migração inválida: {character.id}')
        if character.suspended_goal:
            paused = character.suspended_goal
            if paused.id in entity_ids or paused.id in auxiliary_ids or paused.status != "suspended":
                errors.append(f"Objetivo suspenso inválido: {character.id}")
            auxiliary_ids.add(paused.id)
            if paused.need_id not in {n.id for n in character.needs.values()}:
                errors.append(f"Objetivo suspenso sem necessidade: {character.id}")
        state = character.food_state
        if (state.get('reserve_target', 0) < 0 or state.get('reserve_deficit', 0) < 0 or
                any(b.get('quantity', 0) <= 0 or b.get('turn', 0) > world.turn
                    for b in state.get('acquisitions', []))):
            errors.append(f"Estado alimentar inválido: {character.id}")
        if (character.wage_credit < 0 or character.training_progress < 0 or character.training_required < 0 or
                character.training_target not in (None,"cozinheiro") or
                character.training_target and character.training_required <= 0):
            errors.append(f"Estado profissional inválido: {character.id}")
        if character.market_observation.get("turn",0)>world.turn:
            errors.append(f"Observação econômica futura: {character.id}")
        for fact_id, impact in character.applied_facts.items():
            if fact_id <= 0 or impact.actor_id not in (*world.characters,*world.divinities) or not 0 <= impact.confidence <= 1:
                errors.append(f"Registro factual inválido: {character.id}")
        for fact in character.knowledge.values():
            if not 0 <= fact.confidence <= 100:
                errors.append(f"Confiança factual inválida: {character.id}")
        if len(character.observations) > 64:
            errors.append(f"Observações sem limite: {character.id}")
        for target, observed in character.observations.items():
            if target not in world.characters or not passable(world, observed.position) or observed.turn > world.turn:
                errors.append(f"Observação pessoal inválida: {character.id}")
            if any(value is not None and not 0 <= value <= 100 for value in (observed.hunger, observed.thirst, observed.health)):
                errors.append(f"Sinais observados inválidos: {character.id}")
        if character.financial_setbacks < 0 or character.financial_since is not None and character.financial_since > world.turn:
            errors.append(f"Histórico financeiro inválido: {character.id}")
        if any(fact_id <= 0 or not 0 <= confidence <= 100 for fact_id, confidence in character.processed_personal_facts.items()):
            errors.append(f"Registro de pressões pessoais inválido: {character.id}")
        for reputation in character.reputations.values():
            if (any(not 0 <= value <= 100 for value in reputation.tags.values()) or
                    any(not 0 <= value <= 100 for value in
                        (reputation.popularity, reputation.admiration, reputation.fear)) or
                    len(set(reputation.sources)) != len(reputation.sources)):
                errors.append(f"Reputação inválida: {character.id}")
    for kingdom in world.kingdoms.values():
        if kingdom.capital_id not in kingdom.city_ids or kingdom.capital_id not in world.towns:
            errors.append(f"Capital inválida: {kingdom.id}")
        if kingdom.treasury < 0:
            errors.append(f"Tesouro negativo: {kingdom.id}")
        if not 4 <= len(kingdom.city_ids) <= 6:
            errors.append(f"Quantidade inicial de cidades inválida: {kingdom.id}")
        if kingdom.ruler_id is not None and (kingdom.ruler_id not in world.characters or
                                            not world.characters[kingdom.ruler_id].alive):
            errors.append(f"Governante morto no cargo: {kingdom.id}")
        if kingdom.ruler_id is None and kingdom.political_state != "crise sucessória":
            errors.append(f"Reino sem governante e sem crise política: {kingdom.id}")
        if kingdom.political_state not in ("estável", "crise sucessória") or kingdom.economic_state not in ("estável", "em crise"):
            errors.append(f"Estado independente inválido: {kingdom.id}")
    for town in world.towns.values():
        if town.id not in world.maps or town.abstract_money < 0 or town.wild_food < 0:
            errors.append(f"Estado da cidade inválido: {town.id}")
        residents = [world.characters.get(i) for i in town.resident_ids]
        if (len(set(town.resident_ids)) != len(town.resident_ids) or
                any(c is None or c.is_player or c.town_id != town.id for c in residents)):
            errors.append(f"Censo residente inválido: {town.id}")
        elif (not isinstance(town.abstract_population,int) or town.abstract_population < 0 or
              town.population != town.abstract_population + sum(c.alive for c in residents)):
            errors.append(f"Contabilidade populacional inválida: {town.id}")
        if len(set(town.counted_deaths)) != len(town.counted_deaths) or any(i not in town.resident_ids or world.characters[i].alive for i in town.counted_deaths):
            errors.append(f"Mortalidade populacional inválida: {town.id}")
        if town.grain_credit not in (0,1,2) or town.cooking_slots < 0 or town.meals_served_today < 0:
            errors.append(f"Capacidade/insumos inválidos: {town.id}")
    for quest in world.quests.values():
        if quest.id in entity_ids or quest.id in auxiliary_ids or quest.owner_id not in world.characters:
            errors.append(f"Quest inválida: {quest.id}")
        auxiliary_ids.add(quest.id)
        if quest.target_id is not None and quest.target_id not in entity_ids:
            errors.append(f"Alvo de quest inválido: {quest.id}")
    if len(world.events) > 256:
        errors.append("Registro cotidiano sem limite.")
    for key,record in world.wanted_records.items():
        if (key!=record.id or key in entity_ids or key in auxiliary_ids or
                record.suspect_id not in world.characters or record.jurisdiction not in world.towns or
                not 0<=record.confidence<=100 or not 1<=record.severity<=5 or
                record.status not in ('active','captured','expired','resolved') or
                any(i not in world.characters for i in record.known_by) or
                any(i not in record.known_by or not passable(world,loc) for i,loc in record.known_locations.items())):
            errors.append(f'Registro de procura inválido: {key}')
        if len(record.assignments)>3 or any(i not in record.known_by or role not in ('search','watch','inquire') for i,role in record.assignments.items()):
            errors.append(f'Coordenação institucional inválida: {key}')
        auxiliary_ids.add(key)
    for t in world.towns.values():
        if t.mayor_id is not None and t.mayor_id not in world.characters:errors.append(f'Prefeito inexistente: {t.id}')
        generals=[i for i,r in t.military_ranks.items() if r=='General']
        if (t.general_id is not None and generals!=[t.general_id] or
                any(i not in world.characters for i in t.military_ranks)):errors.append(f'Hierarquia militar inválida: {t.id}')
        if len(t.proposal_ids)>24 or any(i not in world.proposals for i in t.proposal_ids):errors.append(f'Propostas locais inválidas: {t.id}')
    for g in world.groups.values():
        if g.town_id not in world.towns or g.leader_id not in world.characters or any(i not in world.characters for i in g.member_ids):errors.append(f'Grupo inválido: {g.id}')
        if len(g.member_ids)>64 or len(g.knowledge)>24 or len(g.memory)>16 or len(g.grievances)>4 or len(g.proposal_knowledge)>6:errors.append(f'Grupo sem limite: {g.id}')
        if g.commitment:
            if g.commitment.id in entity_ids|auxiliary_ids or g.commitment.owner_id!=g.id or g.commitment.originating_need not in {n.id for n in g.needs.values()}:
                errors.append(f'Compromisso coletivo inválido: {g.id}')
            auxiliary_ids.add(g.commitment.id)
    for f in world.factions.values():
        if len(f.member_ids)>64 or len(f.knowledge)>24 or len(f.memory)>16:errors.append(f'Facção sem limite: {f.id}')
        if f.money<0 or any(i not in world.characters for i in f.member_ids):errors.append(f'Recurso/membro de facção inválido: {f.id}')
        if f.commitment:
            # Uma associação recebe sua própria intenção; não duplica IDs do grupo de origem.
            if f.commitment.id in entity_ids|auxiliary_ids or f.commitment.owner_id!=f.id or f.commitment.originating_need not in {n.id for n in f.needs.values()}:
                errors.append(f'Compromisso institucional inválido: {f.id}')
            auxiliary_ids.add(f.commitment.id)
    for god in world.divinities.values():
        if not 0<=god.energy<=100 or len(god.memory)>16 or len(god.interventions)>16 or len(god.known_followers)>64:errors.append(f'Divindade inválida: {god.id}')
        if not passable(world,god.location):errors.append(f'Local divino inválido: {god.id}')
    for p in world.characters.values():
        if len(p.group_ids)>3 or len(p.organization_ids)>3 or len(p.beliefs)>6 or len(p.renown)>12 or len(p.item_beliefs)>8:errors.append(f'Estado social sem limite: {p.id}')
        if len(p.action_pressures)>8:errors.append(f'Pressões individuais sem limite: {p.id}')
        if p.mythic_trait not in (None,'Heroism','Justice','Coldness') or not 0<=p.mythic_development<=100:errors.append(f'Potencial mítico inválido: {p.id}')
    for prop in world.proposals.values():
        if prop.town_id not in world.towns or prop.target_id not in world.characters or prop.status not in ('draft','submitted','deferred','ignored','accepted','partial','rejected','abandoned'):errors.append(f'Proposta inválida: {prop.id}')
    pressures=[(p.id,r) for p in world.characters.values() for r in p.action_pressures.values()]
    pressures.extend((o.id,o.action_pressure) for o in (*world.groups.values(),*world.factions.values(),*world.divinities.values()))
    for owner,r in pressures:
        if not (0<=r.value<=100 and 0<=r.world<=100 and 0<=r.failures<=6) or len(r.source_facts)>3:
            errors.append(f'Pressão de ação inválida: {owner}')
    for god in world.divinities.values():
        if len(god.essence.get('follower_regions',{}))>64 or len(god.essence.get('known_faith_losses',[]))>8:
            errors.append(f'Influência divina sem limite: {god.id}')
    event_ids = {event.id for event in (*world.events, *world.history)}
    if entity_ids & auxiliary_ids or event_ids & (entity_ids | auxiliary_ids):
        errors.append("IDs colidem entre sistemas.")
    if world.next_id <= max(entity_ids | auxiliary_ids | event_ids):
        errors.append("Contador de IDs inválido.")
    for god in world.divinities.values():
        if len(god.affinities)>64 or len(god.messages)>16 or len(god.bonds)>8 or len(god.presence_regions)>3:
            errors.append(f'Relações divinas sem limite: {god.id}')
        if any(i not in world.maps for i in god.presence_regions):errors.append(f'Presença divina inválida: {god.id}')
        for subject,r in god.affinities.items():
            if subject not in world.characters or not -100<=r['value']<=100 or len(r.get('facts',{}))>12:
                errors.append(f'Afinidade divina inválida: {god.id}')
        for message in god.messages:
            if not 0<=message['confidence']<=100 or message['region'] not in world.maps:
                errors.append(f'Mensagem divina inválida: {god.id}')
    for health in world.faith_health.values():
        for record in (*health.get('regions',{}).values(),health.get('global',{})):
            if len(record.get('snapshots',[]))>3 or any(v<0 for v in record.get('counts',{}).values()):
                errors.append('Tendência religiosa inválida.')
    for route in world.routes.values():
        a=world.towns.get(route.origin) or world.points.get(route.origin)
        b=world.towns.get(route.destination) or world.points.get(route.destination)
        if not a or not b or not route.path or route.path[0]!=a.position or route.path[-1]!=b.position or route.distance!=len(route.path)-1 or route.travel_time<1 or not 0<=route.danger<=100 or route.condition not in ('open','damaged','closed'):
            errors.append(f'Rota física inválida: {route.id}')
        elif any(distance_step.map_id!=world.world_map_id or not passable(world,distance_step) for distance_step in route.path):
            errors.append(f'Rota fora do mapa: {route.id}')
    for p in world.characters.values():
        for key,rk in p.route_knowledge.items():
            if rk.actor!=p.id or rk.route_id not in world.routes or key!=f'{rk.origin}:{rk.destination}' or not 0<=rk.confidence<=100 or rk.learned_at>world.turn:
                errors.append(f'Conhecimento de rota inválido: {p.id}')
        if p.journey:
            j=p.journey
            if len(j.nodes)!=len(j.route_ids)+1 or not 0<=j.leg<len(j.route_ids) or any(i not in world.routes for i in j.route_ids) or len(j.known_at_start)!=len(j.route_ids):
                errors.append(f'Viagem inválida: {p.id}')
    for c in world.divine_contracts.values():
        if c.god not in world.divinities or c.mortal not in world.characters or c.status not in ('offered','active','fulfilled','failed','refused','abandoned','betrayed'):
            errors.append(f'Contrato divino inválido: {c.id}')
    for prop in world.proposals.values():
        if len(prop.supporter_ids)!=len(set(prop.supporter_ids)) or prop.support!=len(prop.supporter_ids):
            errors.append(f'Apoio duplicado ou inconsistente: {prop.id}')
        if prop.policy_id is not None and prop.policy_id not in world.institutional_policies:
            errors.append(f'Política ausente: {prop.id}')
    for policy in world.institutional_policies.values():
        if policy.jurisdiction not in world.towns or policy.proposal_id not in world.proposals:
            errors.append(f'Jurisdição/proposta de política inválida: {policy.id}')
        if min(policy.money,policy.spent,policy.refunded)<0 or policy.money+policy.spent+policy.refunded!=policy.budget:
            errors.append(f'Orçamento institucional inconsistente: {policy.id}')
    for town in world.towns.values():
        if town.infrastructure.get('water_daily',80)<80 or town.infrastructure.get('water_storage',160)<160:
            errors.append(f'Infraestrutura inválida: {town.id}')
    for owner in (*world.characters.values(),*world.groups.values(),*world.factions.values(),*world.towns.values()):
        for need in owner.needs.values():
            if need.episode<1:errors.append(f'Episódio de Need inválido: {need.id}')
            ctx=need.context;kind=ctx.get('organization_type')
            if ctx.get('group_id') is not None and ctx.get('faction_id') is not None:
                errors.append(f'Contexto institucional ambíguo: {need.id}')
            if kind and (kind not in ('group','faction') or ctx.get(kind+'_id')!=ctx.get('organization_id')):
                errors.append(f'Identidade institucional inconsistente: {need.id}')
    for id,row in world.observability.tombstones.items():
        if id!=row.get('event_id') or not isinstance(id,int) or id<=0 or id>=world.next_id or any(not isinstance(parent,int) or parent<=0 or parent>=id for parent in row.get('parent_ids',())):
            errors.append('Metadado histórico mínimo inválido.')
    data=world.observability
    if data.level not in ('OFF','NORMAL','AUDIT') or data.schema_version!=1 or data.next_id<1:
        errors.append('Observabilidade histórica incompatível.')
    recent_limit=1024 if data.level=='AUDIT' else 256
    receipt_limit=4096 if data.level=='AUDIT' else 1024
    if len(data.recent_decisions)>recent_limit or len(data.recent_learning)>receipt_limit:
        errors.append('Retenção histórica ordinária excedida.')
    for event in (*world.history,*world.events,*data.event_archive.values()):
        if event.schema_version!=1 or any(not isinstance(i,int) or i>=event.id or i<1 for i in event.parent_event_ids):
            errors.append(f'Causalidade histórica inválida: {event.id}')
    for id,trace in data.decisions.items():
        if trace.id!=id or trace.actor_id not in entity_ids:
            errors.append('DecisionTrace inválido.')
        if trace.action_attempt_id and trace.action_attempt_id not in data.attempts:
            errors.append(f'ActionAttempt ausente: {id}')
    for receipt in (*data.learning,*data.recent_learning):
        if receipt.receiver_id not in world.characters or not 0<=receipt.confidence_before<=receipt.confidence_after<=100:
            errors.append('LearningReceipt inválido.')
    return errors


def assert_valid(world) -> None:
    errors = validate_world(world)
    if errors:
        raise ValueError("Estado do mundo inválido: " + "; ".join(errors[:12]))
