"""Contabilidade de residentes; posição física não altera o censo."""


class Population:
    def __init__(self, world):
        self.world = world

    def counts(self, town):
        residents = [self.world.characters[i] for i in town.resident_ids]
        return {"total_living": town.population, "abstract": town.abstract_population,
                "persistent_alive": sum(c.alive for c in residents),
                "persistent_dead": sum(not c.alive for c in residents)}

    def register(self, town, character):
        if character.id in town.resident_ids:
            return False
        if town.abstract_population is None or town.abstract_population <= 0:
            raise ValueError("Não há habitante abstrato disponível.")
        town.abstract_population -= 1
        town.resident_ids.append(character.id)
        return True

    def on_death(self, event):
        person = self.world.characters.get(event.target_id)
        if not person or person.alive or person.is_player:
            return
        town = self.world.towns[person.town_id]
        if person.id not in town.resident_ids or person.id in town.counted_deaths:
            return
        town.counted_deaths.append(person.id)
        town.population -= 1
