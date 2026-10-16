"""Dados persistentes; as regras pertencem aos serviços, não às entidades."""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Location:
    map_id: int
    x: int
    y: int


@dataclass
class Area:
    name: str
    structures: list[str] = field(default_factory=list)


@dataclass
class Grid:
    id: int
    name: str
    width: int
    height: int
    rows: list[str]
    areas: dict[str, Area] = field(default_factory=dict)
    exit_to: Location | None = None


@dataclass
class Personality:
    honesty: int = 50
    compassion: int = 50
    courage: int = 50
    independence: int = 50
    greed: int = 50
    diligence: int = 50
    family_loyalty: int = 50
    persistence: int = 50
    temperament: int = 50
    vengefulness: int = 50
    ambition: int = 50


@dataclass
class Need:
    id: int
    owner_id: int
    kind: str
    target_id: int | None
    base_urgency: float
    priority: float
    created_at: int
    updated_at: int
    status: str
    source: str
    reason: str
    context: dict = field(default_factory=dict)
    expires_at: int | None = None


@dataclass
class Observation:
    """Sinais vistos num encontro; não acompanha a posição real remotamente."""
    turn: int
    position: Location
    hunger: float | None
    thirst: float | None
    health: int | None
    alive: bool = True
    profession: str | None = None
    weapon_power: float | None = None
    injured: int = 0


@dataclass
class Grievance:
    target_id: int
    cause: str
    intensity: float
    created_at: int
    last_reinforced: int
    source_fact: int


@dataclass
class EmotionalState:
    anger: float = 0
    resentment: float = 0
    humiliation: float = 0
    desperation: float = 0
    last_updated: int = 0
    last_support: int = -10000
    strain: float = 0
    adaptation: int = 0
    last_adapted: int = 0
    losses: list[int] = field(default_factory=list)
    processed: dict[int, int] = field(default_factory=dict)
    causes: dict[str, int] = field(default_factory=dict)
    loss_confidence: dict[int, int] = field(default_factory=dict)


@dataclass
class CombatState:
    opponents: list[int] = field(default_factory=list)
    defending_until: int = -1
    surrendered_until: int = -1
    protected_by: list[int] = field(default_factory=list)
    last_active: int = -10000
    injured: float = 0
    detention_until: int = -1
    captor_id: int | None = None
    truces: dict[int, int] = field(default_factory=dict)


@dataclass
class MigrationState:
    destination_id: int
    origin_id: int
    reason: str
    started_at: int
    arrived_at: int | None = None


@dataclass
class WantedRecord:
    id: int
    suspect_id: int
    jurisdiction: int
    originating_fact: int
    severity: int
    confidence: int
    created_at: int
    last_known_location: Location
    known_by: list[int] = field(default_factory=list)
    status: str = 'active'
    resolved_at: int | None = None
    known_locations: dict[int, Location] = field(default_factory=dict)
    location_turns: dict[int, int] = field(default_factory=dict)
    known_status: dict[int, str] = field(default_factory=dict)
    known_severity: dict[int, int] = field(default_factory=dict)
    known_facts: dict[int, int] = field(default_factory=dict)


@dataclass
class Goal:
    id: int
    need_id: int
    action: str
    score: float
    created_at: int
    target_id: int | None = None
    destination: Location | None = None
    status: str = "active"
    outcome: str = ""


@dataclass
class Fact:
    event_id: int
    kind: str
    actor_id: int | None
    target_id: int | None
    location: Location | None
    turn: int
    description: str
    confidence: int = 100
    required_trust: int = 0
    source_id: int | None = None
    source_kind: str = "rumor"
    context: dict = field(default_factory=dict)


@dataclass
class FactImpact:
    """Contribuição já contabilizada, independente da memória curta."""
    actor_id: int
    confidence: float
    tags: dict[str, int] = field(default_factory=dict)
    trust: int = 0
    emotion_confidence: int = 0


@dataclass
class Memory:
    event_id: int
    turn: int
    description: str
    firsthand: bool


@dataclass
class Reputation:
    tags: dict[str, int] = field(default_factory=dict)
    sources: list[int] = field(default_factory=list)
    popularity: int = 0
    admiration: int = 0
    fear: int = 0


@dataclass
class Character:
    id: int
    name: str
    surname: str
    position: Location
    home: Location
    workplace: Location
    town_id: int
    profession: str | None
    personality: Personality
    category: str = "comum"
    nickname: str = "Desconhecido"
    faction: int | None = None
    religion: str = ""
    devotion: int = 0
    health: int = 100
    alive: bool = True
    is_player: bool = False
    money: int = 0
    hunger: float = 0
    thirst: float = 0
    fatigue: float = 0
    inventory: dict[int, int] = field(default_factory=dict)
    needs: dict[str, Need] = field(default_factory=dict)
    goal: Goal | None = None
    knowledge: dict[int, Fact] = field(default_factory=dict)
    memories: list[Memory] = field(default_factory=list)
    reputations: dict[int, Reputation] = field(default_factory=dict)
    known_places: dict[str, Location] = field(default_factory=dict)
    failures: dict[str, int] = field(default_factory=dict)
    last_update: int = 0
    starvation_hours: int = 0
    applied_facts: dict[int, FactImpact] = field(default_factory=dict)
    observations: dict[int, Observation] = field(default_factory=dict)
    processed_personal_facts: dict[int, int] = field(default_factory=dict)
    personal_cooldowns: dict[str, int] = field(default_factory=dict)
    financial_since: int | None = None
    financial_setbacks: int = 0
    wage_credit: int = 0  # Sextos de moeda de trabalho efetivamente realizado.
    training_target: str | None = None
    training_progress: int = 0
    training_required: int = 0
    training_started: int | None = None
    training_last_practice: int | None = None
    market_observation: dict = field(default_factory=dict)
    last_meal: int | None = None
    last_drink: int | None = None
    last_successful_action: dict = field(default_factory=dict)
    origin: str = "Geração inicial"
    food_state: dict = field(default_factory=dict)
    suspended_goal: Goal | None = None
    emotions: EmotionalState = field(default_factory=EmotionalState)
    grievances: dict[int, Grievance] = field(default_factory=dict)
    combat: CombatState = field(default_factory=CombatState)
    known_towns: dict[int, dict] = field(default_factory=dict)
    migration: MigrationState | None = None
    active_until: int = 0
    lod: str = 'local'


@dataclass
class Item:
    id: int
    name: str
    kind: str
    owner_id: int
    quality: int
    rarity: str
    creator_id: int | None
    created_at: int
    origin: str
    stackable: bool = True
    damage: int = 0


@dataclass
class Town:
    id: int
    name: str
    kingdom_id: int | None
    position: Location
    market: Location
    kind: str
    capital: bool
    population: int
    specialization: str
    money: int
    abstract_money: int
    inventory: dict[int, int] = field(default_factory=dict)
    resident_ids: list[int] = field(default_factory=list)
    wild_food: int = 30
    demand: dict[str, int] = field(default_factory=dict)
    needs: dict[str, Need] = field(default_factory=dict)
    goal: Goal | None = None
    abstract_population: int | None = None
    counted_deaths: list[int] = field(default_factory=list)
    cooking_slots: int = 1
    grain_credit: int = 0  # Terços de grão ainda utilizáveis na cozinha.
    professional_demand: dict = field(default_factory=dict)
    economic_report: dict = field(default_factory=dict)
    replacement_after: int = 0
    production_today: dict[str, int] = field(default_factory=dict)
    production_previous: dict[str, int] = field(default_factory=dict)
    production_total: dict[str, int] = field(default_factory=dict)
    meals_served_today: int = 0


@dataclass
class Kingdom:
    id: int
    name: str
    family_name: str
    bounds: tuple[int, int, int, int]
    great: bool
    culture: str
    religion: str
    city_ids: list[int] = field(default_factory=list)
    village_ids: list[int] = field(default_factory=list)
    royal_family: list[int] = field(default_factory=list)
    ruler_id: int | None = None
    heir_id: int | None = None
    capital_id: int | None = None
    political_state: str = "estável"
    economic_state: str = "estável"
    military_state: str = "paz"
    social_state: str = "estável"
    treasury: int = 2000
    military: int = 100
    needs: dict[str, Need] = field(default_factory=dict)
    goal: Goal | None = None

    @property
    def status(self) -> str:
        """Compatibilidade de leitura; nenhum domínio escreve neste resumo."""
        if self.political_state != "estável":
            return self.political_state
        states = (self.economic_state, self.military_state, self.social_state)
        return " / ".join(s for s in states if s not in ("estável", "paz")) or "estável"


@dataclass
class Faction:
    id: int
    name: str
    leader_id: int
    headquarters_id: int
    kind: str


@dataclass
class PointOfInterest:
    id: int
    name: str
    kind: str
    position: Location


@dataclass
class Relationship:
    source_id: int
    target_id: int
    kind: str
    value: int


@dataclass
class Event:
    id: int
    kind: str
    turn: int
    description: str
    actor_id: int | None = None
    target_id: int | None = None
    location: Location | None = None
    witnesses: list[int] = field(default_factory=list)
    historical: bool = False
    context: dict = field(default_factory=dict)


@dataclass
class Quest:
    id: int
    owner_id: int
    need_id: int
    title: str
    created_at: int
    status: str = "offered"
    completed_at: int | None = None
    kind: str = "food"
    target_id: int | None = None
    context: dict = field(default_factory=dict)


@dataclass
class WorldState:
    seed: str
    rules_version: str
    world_map_id: int
    next_id: int = 2
    turn: int = 0
    player_id: int | None = None
    primordial_id: int | None = None
    maps: dict[int, Grid] = field(default_factory=dict)
    characters: dict[int, Character] = field(default_factory=dict)
    towns: dict[int, Town] = field(default_factory=dict)
    kingdoms: dict[int, Kingdom] = field(default_factory=dict)
    factions: dict[int, Faction] = field(default_factory=dict)
    points: dict[int, PointOfInterest] = field(default_factory=dict)
    items: dict[int, Item] = field(default_factory=dict)
    relationships: dict[str, Relationship] = field(default_factory=dict)
    quests: dict[int, Quest] = field(default_factory=dict)
    events: list[Event] = field(default_factory=list)
    history: list[Event] = field(default_factory=list)
    metrics: dict[str, int] = field(default_factory=dict)
    rng_state: tuple = ()
    death_records: dict[int, dict] = field(default_factory=dict)
    decision_diagnostics: list[dict] = field(default_factory=list)
    feeding_diagnostics: list[dict] = field(default_factory=list)
    wanted_records: dict[int, WantedRecord] = field(default_factory=dict)

    def allocate_id(self) -> int:
        entity_id = self.next_id
        self.next_id += 1
        return entity_id
