"""Profissões executam trabalho concreto; fabricação exige matéria-prima."""

from .items import NAMES

class ProfessionSystem:
    def __init__(self, world, items, economy, recorder, rng):
        self.world, self.items, self.economy = world, items, economy
        self.recorder, self.rng = recorder, rng

    def casual_work(self, character, hours: int = 1) -> tuple[bool, str]:
        """Trabalho avulso na área rural: conversão e pagamento físico."""
        town = self.world.towns.get(character.position.map_id)
        if not town or self.world.maps[town.id].rows[character.position.y][character.position.x] != "A":
            return False, "Vá à área rural (A) para trabalhar por alimento."
        if self.items.count(town.id, "grain") < 2:
            return False, "Não há trigo disponível para preparar alimentos."
        if self.items.count(town.id, "food") > 237:
            return False, "O estoque local já atende à produção."
        self.items.consume(town.id, "grain", 2)
        self.items.create(town.id, "food", 2, creator_id=character.id, origin="Trabalho avulso")
        self.items.create(character.id, "food", creator_id=character.id, origin="Pagamento por trabalho avulso")
        self.recorder.emit("ItemCreated", f"{character.name} preparou três rações e recebeu uma pelo trabalho.",
                           character.id, town.id, character.position)
        return True, "Trabalho realizado; você recebeu uma ração."

    def work(self, character, hours: int = 1) -> tuple[bool, str]:
        town = self.world.towns[character.town_id]
        if character.position != character.workplace or character.position.map_id != town.id:
            return False, "O local de trabalho ainda não foi alcançado."
        profession = character.profession
        kind, produced = None, 0
        if profession in ("agricultor", "mineiro", "lenhador", "caçador"):
            kind = {"agricultor": "grain", "mineiro": "iron", "lenhador": "wood", "caçador": "food"}[profession]
            limit = 240 if kind in ("grain", "food") else 120
            produced = min((3 if kind == town.specialization else 2) * hours,
                           max(0, limit - self.items.count(town.id, kind)))
        elif profession == "cozinheiro":
            kind = "food"
            batches = min(hours, self.items.count(town.id, "grain") // 2,
                          max(0, (240 - self.items.count(town.id, "food")) // 3))
            if batches:
                self.items.consume(town.id, "grain", batches * 2)
                produced = batches * 3
        elif profession == "ferreiro":
            kind = "weapon"
            if (self.items.count(town.id, "weapon") < 8 and self.items.count(town.id, "iron") >= 2
                    and self.items.count(town.id, "wood") >= 1):
                self.items.consume(town.id, "iron", 2)
                self.items.consume(town.id, "wood", 1)
                produced = 1
        elif profession in ("guarda", "comerciante", "governante", "conselheiro", "soldado"):
            self.economy.wage(character, hours)
            # Serviços alteram reservas e atividades; guardas também respondem
            # a crimes conhecidos através do sistema de necessidades.
            metric = "PatrolPerformed" if profession in ("guarda", "soldado") else "ServicePerformed"
            self.world.metrics[metric] = self.world.metrics.get(metric, 0) + hours
            return True, "Serviço realizado."
        else:
            return False, "Esta ocupação não possui uma atividade remunerada."
        if not produced:
            return False, "Faltam materiais ou o estoque já atende à demanda."
        self.items.create(town.id, kind, produced, creator_id=character.id,
                          origin=f"Produzido em {town.name} por {character.name}")
        self.economy.wage(character, hours)
        self.recorder.emit("ItemCreated", f"{character.name} produziu {produced} unidade(s) de {NAMES[kind].lower()}.",
                           character.id, town.id, character.position)
        return True, "Produção concluída."
