"""Sucessão simples preserva o reino e seus habitantes após uma morte."""

class Politics:
    def __init__(self, world, bus, recorder):
        self.world, self.recorder = world, recorder
        bus.subscribe("CharacterDied", self.on_death)

    def on_death(self, event):
        for kingdom in self.world.kingdoms.values():
            if kingdom.ruler_id != event.target_id:
                continue
            candidates = [entity_id for entity_id in kingdom.royal_family
                          if self.world.characters[entity_id].alive]
            successor = (kingdom.heir_id if kingdom.heir_id in candidates else
                         candidates[0] if candidates else None)
            kingdom.ruler_id = successor
            kingdom.heir_id = next((entity_id for entity_id in candidates if entity_id != successor), None)
            kingdom.political_state = "estável" if successor else "crise sucessória"
            description = (f"{self.world.characters[successor].name} assumiu {kingdom.name}." if successor
                           else f"A dinastia de {kingdom.name} foi extinta; o território permanece em crise sucessória.")
            self.recorder.emit("SuccessionChanged", description, successor, kingdom.id,
                               historical=True, witnesses=candidates)
