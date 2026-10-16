"""Estado dinâmico causal: modifica prioridades/utility, nunca escolhe ações."""
from .models import Grievance
from .rules import INTERACTION, RECOVERY
from .needs import FINISHED


def clamp(value):
    return max(0., min(100., value))


class EmotionSystem:
    def __init__(self, engine):
        self.engine, self.world = engine, engine.world

    @staticmethod
    def sync_desperation(state):
        total = sum(state.despair_sources.values())
        if total < state.desperation:
            state.despair_sources['unclassified'] = state.despair_sources.get('unclassified', 0)+state.desperation-total
        elif total > state.desperation and total:
            state.despair_sources = {k:v*state.desperation/total for k,v in state.despair_sources.items()}

    def add_desperation(self, person, source, amount):
        state = person.emotions
        self.sync_desperation(state)
        actual = clamp(state.desperation+amount)-state.desperation
        state.desperation += actual
        state.despair_sources[source] = state.despair_sources.get(source, 0)+actual

    def support(self, person, amount=12):
        state = person.emotions
        state.anger = clamp(state.anger-amount)
        state.desperation = clamp(state.desperation-amount)
        self.sync_desperation(state)
        state.humiliation = clamp(state.humiliation-amount/2)
        state.last_support = self.world.turn

    def repair(self, person, target_id, amount=30):
        self.support(person, amount)
        grievance = person.grievances.get(target_id)
        if grievance:
            grievance.intensity = clamp(grievance.intensity-amount)
        person.emotions.resentment = clamp(person.emotions.resentment-amount/2)

    def on_fact(self, person, fact):
        harmful = {'ItemStolen', 'CharacterAttacked', 'CharacterThreatened', 'CharacterInsulted', 'CharacterKilled', 'CharacterDied'}
        supportive = {'HelpGiven', 'ComfortGiven', 'ProtectionGiven', 'FirstAidGiven', 'RestitutionGiven', 'ApologyGiven', 'ConflictForgiven'}
        if fact.kind not in harmful | supportive or fact.confidence < 30:
            return
        state = person.emotions
        impact=person.applied_facts.get(fact.event_id)
        previous = max(state.processed.get(fact.event_id, 0),impact.emotion_confidence if impact else 0)
        if fact.kind=='CharacterDied':previous=max(previous,state.loss_confidence.get(fact.target_id,0))
        if previous >= fact.confidence:
            return
        state.processed[fact.event_id] = fact.confidence
        if impact:impact.emotion_confidence=fact.confidence
        if fact.kind=='CharacterDied':state.loss_confidence[fact.target_id]=fact.confidence
        while len(state.processed)>128:del state.processed[next(iter(state.processed))]
        certainty = (fact.confidence-previous)/100
        kin = self.engine.needs.personal.kin.get(person.id, ())
        harmed = (fact.target_id == person.id or fact.target_id in kin or
                  fact.kind == 'ItemStolen' and fact.target_id == person.town_id and
                  fact.location == person.position and person.hunger >= 55)
        if fact.kind in supportive:
            if fact.target_id == person.id:
                self.support(person, 15*certainty)
                if fact.kind in ('RestitutionGiven', 'ApologyGiven', 'ConflictForgiven'):
                    self.repair(person, fact.actor_id, 20*certainty)
            return
        if not harmed or fact.actor_id == person.id:
            return
        intensity = {'ItemStolen': 18, 'CharacterAttacked': 30, 'CharacterThreatened': 16,
                     'CharacterInsulted': 12, 'CharacterKilled': 45, 'CharacterDied':8}[fact.kind]*certainty
        state.anger = clamp(state.anger+intensity)
        state.resentment = clamp(state.resentment+intensity*.55)
        if fact.kind in ('ItemStolen', 'CharacterThreatened', 'CharacterInsulted') and fact.confidence >= 70:
            state.humiliation = clamp(state.humiliation+intensity*.5)
        if fact.kind in ('CharacterKilled','CharacterDied') and fact.target_id in kin:
            if fact.target_id not in state.losses:
                state.losses.append(fact.target_id)
            self.add_desperation(person, 'grief', 20*certainty)
        state.causes[fact.kind] = state.causes.get(fact.kind, 0)+1
        if fact.actor_id is not None and fact.actor_id != person.id:
            old = person.grievances.get(fact.actor_id)
            if old:
                old.intensity = clamp(old.intensity+intensity)
                old.last_reinforced, old.source_fact = self.world.turn, fact.event_id
            else:
                person.grievances[fact.actor_id] = Grievance(fact.actor_id, fact.kind, intensity,
                    self.world.turn, self.world.turn, fact.event_id)
                self.world.metrics['GrievanceCreated'] = self.world.metrics.get('GrievanceCreated', 0)+1
            if len(person.grievances)>16:
                weakest = min(person.grievances, key=lambda i: person.grievances[i].intensity)
                del person.grievances[weakest]
        # Promoção de LOD: estado/necessidade são atualizados pela percepção;
        # a ação continua sendo escolhida na próxima hora, nunca no callback.
        person.active_until = max(person.active_until, self.world.turn+6)

    def update(self, person):
        state = person.emotions
        elapsed = max(0, self.world.turn-state.last_updated)
        if not elapsed:
            return
        state.last_updated = self.world.turn
        self.sync_desperation(state)
        state.anger = clamp(state.anger-INTERACTION.anger_decay*elapsed)
        state.resentment = clamp(state.resentment-INTERACTION.resentment_decay*elapsed)
        state.humiliation = clamp(state.humiliation-INTERACTION.humiliation_decay*elapsed)
        grief = any(n.kind == 'grief' and n.status not in FINISHED for n in person.needs.values())
        poverty = person.financial_since is not None and self.world.turn-person.financial_since>48
        stable = self.engine.recovery.material_stable(person)
        state.stable_material_hours = state.stable_material_hours+elapsed if stable else 0
        deprivation = max(person.hunger, person.thirst) >= 80
        sources = ([ 'deprivation' ] if deprivation else []) + ([ 'poverty' ] if poverty and not stable else [])
        sources += ([ 'grief' ] if grief else []) + ([ 'violence' ] if person.combat.opponents else [])
        pursued = self.engine.recovery.known_pursuit(person)
        if pursued:sources.append('pursuit')
        pressure = bool(sources)
        if pressure:
            for source in sources:
                self.add_desperation(person, source, min(elapsed,12)*.15/len(sources))
            if deprivation:
                self.add_desperation(person, 'deprivation', min(elapsed,12)*.25)
            state.strain += elapsed*(.3+state.desperation/100)
            if person.hunger>=80:
                state.anger = clamp(state.anger+min(elapsed,12)*.12)
        else:
            state.desperation = clamp(state.desperation-.3*elapsed)
            self.sync_desperation(state)
            state.strain = max(0,state.strain-elapsed*.4)
        if state.stable_material_hours >= RECOVERY.stable_hours:
            # Melhorar condições materiais não elimina luto ou grievance.
            for source in ('deprivation', 'poverty'):
                reduction = min(state.despair_sources.get(source, 0), RECOVERY.material_desperation_decay*elapsed)
                state.despair_sources[source] = max(0, state.despair_sources.get(source, 0)-reduction)
                state.desperation = clamp(state.desperation-reduction)
                key='Emotion:MaterialDesperationRecovered'
                self.world.metrics[key]=self.world.metrics.get(key,0)+reduction
        for grievance in person.grievances.values():
            grievance.intensity = clamp(grievance.intensity-.025*elapsed)
        # Uma mudança pequena por mês de pressão acumulada, máximo cinco.
        if (state.strain>=INTERACTION.adaptation_hours and state.adaptation<5
                and self.world.turn-state.last_adapted>=INTERACTION.adaptation_hours):
            person.personality.vengefulness = min(100,person.personality.vengefulness+1)
            person.personality.independence = min(100,person.personality.independence+1)
            state.strain-=INTERACTION.adaptation_hours
            state.adaptation+=1
            state.last_adapted=self.world.turn
            self.engine.recorder.emit('PersonalityAdapted',f'{person.name} mudou lentamente após pressão prolongada.',
                person.id,location=person.position,witnesses=[person.id],
                context={'changes':{'vengefulness':1,'independence':1},'months':state.adaptation})

    def priority_modifier(self, person, need):
        state = person.emotions
        if need.kind in ('revenge','protection','response'):
            return min(15,state.anger*.1+state.resentment*.05)
        if need.kind == 'status':
            return min(8,state.humiliation*.08)
        if need.kind in ('money','migration'):
            return min(8,state.desperation*.08)
        return 0
