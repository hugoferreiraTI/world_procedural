"""Invariantes usadas tanto por testes longos quanto pelo carregamento de saves."""

from dataclasses import fields

from .knowledge import KNOWLEDGE_LIMIT, MEMORY_LIMIT
from .navigation import passable


def validate_world(world) -> list[str]:
    errors = []
    groups = (world.characters, world.towns, world.kingdoms, world.factions, world.points, world.items)
    entity_ids = {world.world_map_id}
    for group in groups:
        for key, entity in group.items():
            if key != entity.id or key in entity_ids:
                errors.append(f"ID inválido ou duplicado: {key}")
            entity_ids.add(key)
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
        if not (-100 if relation.kind == "diplomacia" else 0) <= relation.value <= 100:
            errors.append("Valor de relacionamento fora da escala.")
    inventory_ids = set()
    auxiliary_ids = set()
    for owner in (*world.characters.values(), *world.towns.values(), *world.kingdoms.values()):
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
        emotion=character.emotions
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
            if fact_id <= 0 or impact.actor_id not in world.characters or not 0 <= impact.confidence <= 1:
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
        auxiliary_ids.add(key)
    event_ids = {event.id for event in (*world.events, *world.history)}
    if entity_ids & auxiliary_ids or event_ids & (entity_ids | auxiliary_ids):
        errors.append("IDs colidem entre sistemas.")
    if world.next_id <= max(entity_ids | auxiliary_ids | event_ids):
        errors.append("Contador de IDs inválido.")
    return errors


def assert_valid(world) -> None:
    errors = validate_world(world)
    if errors:
        raise ValueError("Estado do mundo inválido: " + "; ".join(errors[:12]))
