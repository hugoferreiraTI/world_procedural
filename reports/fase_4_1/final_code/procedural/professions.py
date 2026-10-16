"""Trabalho concreto, preparo parcial e aprendizagem dentro das profissões."""
import math
from dataclasses import dataclass
from .items import NAMES
from .models import Character, Location, Personality
from .population import Population
from .relationships import RelationshipGraph

SIMPLE_WORKERS = {None, 'agricultor', 'mineiro', 'lenhador', 'ferreiro', 'caçador', 'comerciante', 'cozinheiro'}
TRAINABLE = {None, 'agricultor', 'mineiro', 'lenhador', 'ferreiro', 'caçador', 'comerciante'}


@dataclass(frozen=True)
class WorkResult:
    status: str
    message: str
    produced: int = 0
    paid: int = 0
    credit_added: int = 0

    @property
    def success(self):
        return self.status in ('paid', 'credited')

    def __iter__(self):
        return iter((self.success, self.message))

    def __getitem__(self, index):
        return (self.success, self.message)[index]


class ProfessionSystem:
    def __init__(self, world, items, economy, recorder, rng):
        self.world, self.items, self.economy = world, items, economy
        self.recorder, self.rng = recorder, rng

    def record_production(self, town, kind, quantity):
        for bucket in (town.production_today, town.production_total):
            bucket[kind] = bucket.get(kind, 0) + quantity

    def prepare(self, town, limit):
        """2/3 grain por food; sobras exatas, inventário de grãos inteiros."""
        amount = min(limit, (self.items.count(town.id, 'grain') * 3 + town.grain_credit) // 2)
        if amount <= 0:
            return 0
        grain = max(0, math.ceil((amount * 2 - town.grain_credit) / 3))
        if grain:
            self.items.consume(town.id, 'grain', grain)
        town.grain_credit += grain * 3 - amount * 2
        return amount

    def saturated(self, person, observation):
        kind = {'agricultor':'grain','mineiro':'iron','lenhador':'wood','caçador':'food','cozinheiro':'food'}.get(person.profession)
        stock = observation.get('stock', {})
        return bool(kind and stock.get(kind, 0) >= (240 if kind in ('food','grain') else 120))

    def temporary_eligible(self, person):
        return person.profession in SIMPLE_WORKERS and not person.training_target

    def compatible_workplace(self, person):
        town = self.world.towns.get(person.town_id)
        return bool(town and person.workplace.map_id == town.id and person.position.map_id == town.id
                    and person.profession not in (None, 'estudante'))

    def temporary_capacity(self, town):
        """Capacidade real no instante de observação; não reserva vaga futura."""
        offers = {}
        demand = max(0, math.ceil((town.abstract_population or 0)/120)-town.meals_served_today)
        portions = min(demand, self.items.count(town.id, 'food')//2)
        if portions:
            offers['meal_distribution'] = {'capacity': portions, 'local': vars(town.market).copy(),
                                          'required_food_per_unit': 2}
        rural = self.world.maps[town.id]
        location = next(((x,y) for y,row in enumerate(rural.rows) for x,s in enumerate(row) if s == 'A'), None)
        prepare = min(max(0, 240-self.items.count(town.id, 'food')),
                      (self.items.count(town.id, 'grain')*3+town.grain_credit)//2)
        if prepare >= 3 and location:
            offers['food_preparation'] = {'capacity': prepare//3, 'local': {'map_id':town.id,'x':location[0],'y':location[1]},
                                         'required_grain_thirds': 6, 'paid_food_per_unit': 1}
        return offers

    def temporary_service(self, person, hours=1):
        town = self.world.towns[person.town_id]
        if person.position != town.market or not self.temporary_eligible(person):
            return False, 'Distribuição disponível no mercado para trabalhador compatível.'
        demand = max(0,math.ceil((town.abstract_population or 0)/120)-town.meals_served_today)
        portions = min(hours, self.items.count(town.id,'food')//2,demand)
        if not portions:
            return False, 'Não há refeições para distribuir.'
        # Uma porção paga o trabalhador; outra é efetivamente servida à população.
        self.items.transfer(town.id,person.id,self.items.first(town.id,'food'),portions)
        self.items.consume(town.id,'food',portions)
        town.meals_served_today += portions
        self.recorder.emit('TemporaryWorkPerformed',f'{person.name} distribuiu {portions} refeições locais.',
            person.id,town.id,person.position,context={'service':'meal_distribution','paid_food':portions,'served_food':portions})
        return True, 'Refeições distribuídas e pagamento físico recebido.'

    def casual_work(self, character, hours=1):
        town = self.world.towns.get(character.position.map_id)
        if not town or self.world.maps[town.id].rows[character.position.y][character.position.x] != 'A':
            return False, 'Vá à área rural (A) para trabalhar por alimento.'
        if not self.temporary_eligible(character):
            return False, 'Esta tarefa não é compatível com a ocupação atual.'
        room = max(0, 240-self.items.count(town.id,'food'))
        if room <= 0 or self.items.count(town.id,'grain') * 3 + town.grain_credit < 2:
            return False, 'Faltam insumos ou espaço para preparo.'
        # O pagamento físico sai do produto; não duplica a produção contabilizada.
        produced = self.prepare(town, min(room, 3*hours))
        paid_food = min(hours, produced//3)
        if produced > paid_food:
            self.items.create(town.id,'food',produced-paid_food,creator_id=character.id,origin='Trabalho avulso')
        if paid_food:
            self.items.create(character.id,'food',paid_food,creator_id=character.id,origin='Pagamento por trabalho avulso')
        else:
            self.economy.wage(character, produced*2, sixths=True)
        self.record_production(town,'food',produced)
        self.recorder.emit('TemporaryWorkPerformed',f'{character.name} preparou {produced} rações em trabalho temporário.',
                           character.id,town.id,character.position,context={'food':produced,'paid_food':paid_food})
        self.recorder.emit('ItemCreated',f'{character.name} produziu {produced} rações.',character.id,town.id,character.position)
        return True, 'Trabalho realizado com pagamento do produto ou proporcional.'

    def work(self, character, hours=1):
        town = self.world.towns[character.town_id]
        if not self.compatible_workplace(character):
            return WorkResult('incompatible_local', 'Esta instalação não participa da economia produtiva exigida.')
        if character.position != character.workplace:
            return WorkResult('not_arrived', 'O local de trabalho ainda não foi alcançado.')
        if town.money <= 0:
            return WorkResult('no_payer', 'O pagador local não possui recursos para remunerar agora.')
        if character.combat.injured>=20:
            hours=max(1,int(hours*(1-character.combat.injured/150)))
        profession = character.profession
        kind, produced, rate = None, 0, 1
        if profession in ('agricultor','mineiro','lenhador','caçador'):
            kind = {'agricultor':'grain','mineiro':'iron','lenhador':'wood','caçador':'food'}[profession]
            rate = 3 if kind == town.specialization else 2
            produced = min(rate*hours,max(0,(240 if kind in ('grain','food') else 120)-self.items.count(town.id,kind)))
        elif profession == 'cozinheiro':
            kind, rate = 'food', 3
            produced = self.prepare(town,min(3*hours,max(0,240-self.items.count(town.id,'food'))))
        elif profession == 'ferreiro':
            kind = 'weapon'
            if (self.items.count(town.id,'weapon')<8 and self.items.count(town.id,'iron')>=2 and self.items.count(town.id,'wood')>=1):
                self.items.consume(town.id,'iron',2); self.items.consume(town.id,'wood',1)
                produced = 1  # Arma indivisível, uma operação por ação.
        elif profession in ('guarda','comerciante','governante','conselheiro','soldado'):
            paid = self.economy.wage(character,hours)
            metric = 'PatrolPerformed' if profession in ('guarda','soldado') else 'ServicePerformed'
            self.world.metrics[metric] = self.world.metrics.get(metric,0)+hours
            return WorkResult('paid' if paid else 'credited', 'Serviço realizado.', paid=paid, credit_added=hours*6)
        else:
            return WorkResult('no_activity', 'Esta ocupação não possui uma atividade remunerada.')
        if not produced:
            full = self.items.count(town.id,kind) >= (8 if kind == 'weapon' else 240 if kind in ('food','grain') else 120)
            return WorkResult('saturated' if full else 'no_input',
                              'O estoque já atende à demanda.' if full else 'Faltam materiais para produzir.')
        self.items.create(town.id,kind,produced,creator_id=character.id,origin=f'Produzido em {town.name} por {character.name}')
        credit = produced*(6//rate)
        paid = self.economy.wage(character,credit,sixths=True)
        self.record_production(town,kind,produced)
        self.recorder.emit('ItemCreated',f'{character.name} produziu {produced} unidade(s) de {NAMES[kind].lower()}.',
                           character.id,town.id,character.position)
        return WorkResult('paid' if paid else 'credited', 'Produção concluída com pagamento.' if paid else
                          'Produção concluída com crédito salarial parcial.', produced, paid, credit)

    def suitable_candidate(self, person, town):
        return (person.alive and not person.is_player and person.category=='comum' and
                person.position.map_id==town.id and person.profession in TRAINABLE and
                (person.money<20 or person.personality.ambition>=60 or
                 self.saturated(person,{'stock':{k:self.items.count(town.id,k) for k in ('food','grain','iron','wood')}})))

    def train(self, person, hours=1):
        town = self.world.towns[person.town_id]
        target = person.training_target or person.market_observation.get('training_offer')
        if target != 'cozinheiro' or person.position != town.market:
            return False, 'Treinamento disponível somente na taverna conhecida.'
        if not person.training_target:
            vacancy = town.professional_demand.get('cozinheiro',{})
            occupied = sum(c.alive and (c.profession=='cozinheiro' or c.training_target=='cozinheiro')
                and c.position.map_id==town.id for c in (self.world.characters[i] for i in town.resident_ids))
            if (not vacancy.get('projected_deficit',vacancy.get('deficit')) or not self.suitable_candidate(person,town) or
                    not self.economy.has_kitchen(town) or occupied>=town.cooking_slots):
                return False, 'Não há vaga compatível para este trabalhador.'
        room = max(0,240-self.items.count(town.id,'food'))
        if room<=0 or town.money<=0:
            return False, 'O treinamento produtivo não pode ocorrer agora.'
        # Aprendiz faz uma ração/hora, recebe 1/3 do salário pleno, usa insumos reais.
        produced = self.prepare(town,min(hours,room))
        if not produced:
            return False, 'Não há insumo para a aprendizagem.'
        if not person.training_target:
            person.training_target, person.training_started = target, self.world.turn
            person.training_required = max(12, 36-person.personality.diligence//5-(8 if person.profession=='agricultor' else 0))
            self.recorder.emit('TrainingStarted',f'{person.name} começou a aprender cozinha.',person.id,town.id,person.position,
                               context={'previous':person.profession,'target':target,'required':person.training_required})
        self.items.create(town.id,'food',produced,creator_id=person.id,origin='Preparo de aprendiz')
        self.record_production(town,'food',produced)
        self.economy.wage(person,produced*2,sixths=True)
        person.training_progress += produced
        person.training_last_practice = self.world.turn
        self.recorder.emit('TrainingProgress',f'{person.name} praticou cozinha por {produced} hora(s).',person.id,town.id,person.position,
                           context={'progress':person.training_progress,'required':person.training_required})
        if person.training_progress>=person.training_required:
            previous = person.profession
            person.profession, person.workplace = target, town.market
            person.known_places['work'] = town.market
            person.training_target = None
            self.recorder.emit('ProfessionChanged',f'{person.name} deixou {previous or "o desemprego"} e tornou-se cozinheiro.',
                               person.id,town.id,person.position,context={'previous':previous,'profession':target})
        return True, 'Aprendizagem produtiva realizada.'

    def can_materialize(self, town):
        vacancy = town.professional_demand.get('cozinheiro',{})
        if (not vacancy.get('deficit') or self.world.turn-vacancy.get('since',self.world.turn)<72 or
                self.world.turn<town.replacement_after or not town.abstract_population or
                town.money<24 or town.abstract_money<12 or self.items.count(town.id,'grain')<2 or
                self.items.count(town.id,'water')<2 or not self.economy.has_kitchen(town)):
            return False
        people = [self.world.characters[i] for i in town.resident_ids]
        projected = sum(c.training_target=='cozinheiro' for c in people if c.alive)
        if projected>=vacancy['deficit'] or any(self.suitable_candidate(c,town) for c in people):
            return False
        cooks = sum(c.alive and c.profession=='cozinheiro' and c.position.map_id==town.id for c in people)
        if cooks+projected>=town.cooking_slots:
            return False
        return True

    def materialize(self, town):
        if not self.can_materialize(town):
            return False
        vacancy = town.professional_demand['cozinheiro']
        from .generation import FIRST_NAMES,FAMILY_NAMES
        surname = self.rng.choice(FAMILY_NAMES)
        person = Character(self.world.allocate_id(),f'{self.rng.choice(FIRST_NAMES)} {surname}',surname,
            town.market,Location(town.id,2,2),town.market,town.id,None,
            Personality(*(self.rng.randint(5,95) for _ in range(11))),
            money=12,faction=town.kingdom_id,origin=f'Habitante abstrato de {town.name}',last_update=self.world.turn)
        town.abstract_money-=12
        person.known_places={'market':town.market,'home':person.home,'work':town.market,
            'forage':Location(town.id,1,self.world.maps[town.id].height-2),'well_home':person.home,
            'well_rural':Location(town.id,1,self.world.maps[town.id].height-2)}
        person.training_target, person.training_started, person.training_required = 'cozinheiro',self.world.turn,24
        person.training_last_practice = self.world.turn
        person.religion = self.world.kingdoms[town.kingdom_id].religion if town.kingdom_id else ''
        Population(self.world).register(town,person)
        person.emotions.last_updated=person.emotions.last_adapted=self.world.turn
        self.world.characters[person.id]=person
        graph = RelationshipGraph(self.world)
        graph.set(person.id,town.id,'residente_de',100)
        if town.kingdom_id:
            graph.set(person.id,town.kingdom_id,'lealdade',self.rng.randint(15,95))
        for kind,quantity in (('food',min(2,self.items.count(town.id,'food'))),('water',2)):
            if quantity: self.items.transfer(town.id,person.id,self.items.first(town.id,kind),quantity)
        self.recorder.spatial.move(person.id,person.position,person.position)
        town.replacement_after=self.world.turn+72
        self.recorder.emit('WorkerMaterialized',f'{person.name} passou a trabalhar como aprendiz em {town.name}.',
            person.id,town.id,person.position,historical=True,context={'profession':'cozinheiro','abstract_remaining':town.abstract_population,
            'vacancy_duration':self.world.turn-vacancy['since']})
        self.recorder.emit('TrainingStarted',f'{person.name} iniciou aprendizagem de cozinha.',person.id,town.id,
            person.position,context={'previous':None,'target':'cozinheiro','required':24,'origin':'materialization'})
        return True
