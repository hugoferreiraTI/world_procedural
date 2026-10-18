"""Dados persistentes; as regras pertencem aos serviços, não às entidades."""

from dataclasses import dataclass, field
from copy import deepcopy


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
    sadism: int = 0


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
    episode: int = 1

    @property
    def need_episode_id(self):
        return f'n{self.id}:{self.episode}'


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
    despair_sources: dict[str, float] = field(default_factory=dict)
    stable_material_hours: float = 0


@dataclass
class ActionPressure:
    value: float = 0
    world: float = 0
    failures: int = 0
    last_failure: int = -1000
    updated_at: int = -1
    source_facts: list[int] = field(default_factory=list)
    reason: str = ""


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
    violence_intents: dict[int, str] = field(default_factory=dict)
    pending_judgments: dict[int, int] = field(default_factory=dict)
    conflict_history: dict[int, dict] = field(default_factory=dict)


@dataclass
class LethalDecision:
    id: int
    actor_id: int
    target_id: int
    mode: str
    cause: str
    facts: list[int]
    created_at: int
    updated_at: int
    confidence: float
    intensity: float
    world_pressure: float
    action_pressure: float
    impellors: dict = field(default_factory=dict)
    inhibitors: dict = field(default_factory=dict)
    commitment_id: int | None = None
    status: str = 'active'
    rumination: float = 0
    last_reinforced: int = 0
    reason: str = ''
    context: dict = field(default_factory=dict)


@dataclass
class MigrationState:
    destination_id: int
    origin_id: int
    reason: str
    started_at: int
    arrived_at: int | None = None


@dataclass
class Route:
    id: int
    origin: int
    destination: int
    distance: int
    travel_time: int
    terrain: str
    danger: int = 0
    condition: str = 'open'
    route_type: str = 'road'
    toll: int = 0
    path: list[Location] = field(default_factory=list)
    history: list[int] = field(default_factory=list)
    uses: int = 0


@dataclass
class RouteKnowledge:
    actor: int
    origin: int
    destination: int
    route_id: int
    confidence: int
    source: str
    learned_at: int
    last_used_at: int = -1
    source_id: int | None = None
    travel_time: int = 0
    danger: int = 0
    condition: str = 'open'


@dataclass
class Journey:
    origin: int
    destination: int
    route_ids: list[int]
    nodes: list[int]
    reason: str
    started_at: int
    mode: str = 'known_route'
    guide_id: int | None = None
    leg: int = 0
    offset: int = 0
    last_step: int = -1
    entering: bool = False
    known_at_start: list[dict] = field(default_factory=list)


@dataclass
class DivineContract:
    id: int
    god: int
    mortal: int
    god_obligation: str
    mortal_obligation: str
    conditions: dict
    status: str
    created_at: int
    audience_id: int
    known_by_god: str = 'active'
    fulfilled_at: int | None = None


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
    institutional_fact: "Fact | None" = None
    institutional_available_at: int = -1
    institutional_clue: "Fact | None" = None
    clue_available_at: int = -1
    assignments: dict[int, str] = field(default_factory=dict)


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
    resource_kind: str | None = None
    amount: int = 1


@dataclass
class MaterialCandidate:
    """Alternativa transitória; desempacotamento antigo de três campos preservado."""
    action: str
    destination: Location | None
    target_id: int | None
    resource_kind: str
    amount: int = 1

    def __iter__(self):
        return iter((self.action,self.destination,self.target_id))


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

    def __post_init__(self):
        self.context=deepcopy(self.context)


@dataclass
class FactImpact:
    """Contribuição já contabilizada, independente da memória curta."""
    actor_id: int
    confidence: float
    tags: dict[str, int] = field(default_factory=dict)
    trust: int = 0
    emotion_confidence: int = 0
    renown_confidence: int = 0


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
class Clue:
    subject_id: int
    location: Location
    observed_at: int
    source_id: int | None
    confidence: float
    specificity: str
    related_fact: int | None
    direction: str | None = None
    status: str = "available"
    source_kind: str = "rumor"


@dataclass
class Commitment:
    id: int
    owner_id: int
    originating_need: int
    originating_fact: int | None
    target_id: int | None
    motivation: str
    intensity: float
    created_at: int
    last_progress_at: int
    last_attempt_at: int = -1
    progress: float = 0
    setbacks: int = 0
    failures: int = 0
    investment: int = 0
    status: str = "active"
    abandonment_pressure: float = 0
    resolution_condition: str = "need_state"
    activity_count: int = 0
    meaningful_progress: int = 0
    last_strategy: str = ""
    strategy_changes: int = 0
    stalled_actions: dict[str, int] = field(default_factory=dict)
    context: dict = field(default_factory=dict)


@dataclass
class Aspiration:
    domain: str
    intensity: float
    created_at: int
    principal: bool = True
    status: str = "active"
    progress: float = 0
    context: dict = field(default_factory=dict)


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
    recoverable_deprivation_damage: int = 0
    damage_by_origin: dict[str, int] = field(default_factory=dict)
    recovery_state: dict = field(default_factory=dict)
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
    commitments: dict[int, Commitment] = field(default_factory=dict)
    aspirations: list[Aspiration] = field(default_factory=list)
    agency_state: dict = field(default_factory=dict)
    group_ids: list[int] = field(default_factory=list)
    organization_ids: list[int] = field(default_factory=list)
    beliefs: dict[int, dict] = field(default_factory=dict)
    renown: dict[int, dict] = field(default_factory=dict)
    item_beliefs: dict[int, dict] = field(default_factory=dict)
    mythic_trait: str | None = None
    mythic_development: float = 0
    social_state: dict = field(default_factory=dict)
    action_pressures: dict[str, ActionPressure] = field(default_factory=dict)
    lethal_decisions: dict[int, LethalDecision] = field(default_factory=dict)
    route_knowledge: dict[str, RouteKnowledge] = field(default_factory=dict)
    place_knowledge: dict[int, dict] = field(default_factory=dict)
    journey: Journey | None = None
    access_state: dict = field(default_factory=dict)
    known_factions: dict[int, dict] = field(default_factory=dict)
    known_sacred_sites: dict[int, dict] = field(default_factory=dict)
    known_groups: dict[int, dict] = field(default_factory=dict)
    known_proposals: dict[int, dict] = field(default_factory=dict)
    known_policies: dict[int, dict] = field(default_factory=dict)
    death_affinity: float = 0
    death_state: dict = field(default_factory=dict)


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
    previous_owners: list[int] = field(default_factory=list)
    important_events: list[int] = field(default_factory=list)
    divine_contact: int | None = None
    actual_properties: dict = field(default_factory=dict)
    historical_title: str = ""
    creation_location: Location | None = None


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
    mayor_id: int | None = None
    office: dict = field(default_factory=dict)
    military_ranks: dict[int, str] = field(default_factory=dict)
    general_id: int | None = None
    authority_town_id: int | None = None
    proposal_ids: list[int] = field(default_factory=list)
    policies: dict = field(default_factory=dict)
    infrastructure: dict = field(default_factory=dict)


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
    member_ids: list[int] = field(default_factory=list)
    purpose: str = ""
    ranks: list[str] = field(default_factory=list)
    assignments: dict[int, dict] = field(default_factory=dict)
    knowledge: dict[int, Fact] = field(default_factory=dict)
    needs: dict[str, Need] = field(default_factory=dict)
    goal: Goal | None = None
    commitment: Commitment | None = None
    inventory: dict[int, int] = field(default_factory=dict)
    money: int = 0
    norms: dict = field(default_factory=dict)
    memory: list[int] = field(default_factory=list)
    created_at: int = 0
    status: str = "active"
    action_pressure: ActionPressure = field(default_factory=ActionPressure)
    plan: dict = field(default_factory=dict)
    local_status: dict[int, dict] = field(default_factory=dict)


@dataclass
class Group:
    id: int
    name: str
    town_id: int
    cause: str
    subject_id: int | None
    leader_id: int
    member_ids: list[int]
    created_at: int
    originating_need: int
    originating_fact: int | None = None
    status: str = "active"
    needs: dict[str, Need] = field(default_factory=dict)
    goal: Goal | None = None
    commitment: Commitment | None = None
    knowledge: dict[int, Fact] = field(default_factory=dict)
    grievances: dict[int, dict] = field(default_factory=dict)
    support: dict[int, float] = field(default_factory=dict)
    proposal_ids: list[int] = field(default_factory=list)
    proposal_knowledge: dict[int, dict] = field(default_factory=dict)
    pressure: float = 0
    failures: int = 0
    investment: int = 0
    last_meeting: int = -1
    last_relevant: int = 0
    responsibility_id: int | None = None
    memory: list[int] = field(default_factory=list)
    action_pressure: ActionPressure = field(default_factory=ActionPressure)
    plan: dict = field(default_factory=dict)
    money: int = 0
    inventory: dict[int, int] = field(default_factory=dict)


@dataclass
class Proposal:
    id: int
    group_id: int
    town_id: int
    target_id: int
    cause: str
    objective: str
    solution: str
    urgency: float
    support: int
    created_at: int
    source_fact: int | None = None
    opposition: int = 0
    status: str = "draft"
    result: dict = field(default_factory=dict)
    decided_at: int | None = None
    subject_id: int | None = None
    sector: str = ''
    desired_effect: str = ''
    supporter_ids: list[int] = field(default_factory=list)
    supporting_group_ids: list[int] = field(default_factory=list)
    supporting_faction_ids: list[int] = field(default_factory=list)
    affected_locality_ids: list[int] = field(default_factory=list)
    pressure: float = 0
    pressure_state: dict = field(default_factory=dict)
    policy_id: int | None = None
    support_by_group: dict[int, list[int]] = field(default_factory=dict)
    delivered_supporter_ids: list[int] = field(default_factory=list)


@dataclass
class InstitutionalTask:
    id: int
    issuer: int
    institution_type: str
    institution_id: int
    kind: str
    target: int
    location: Location
    created: int
    priority: float
    requirements: dict = field(default_factory=dict)
    authorized_roles: list[str] = field(default_factory=list)
    status: str = 'pending'
    attempts: int = 0
    block_reason: str | None = None
    event_id: int | None = None
    executor_ids: list[int] = field(default_factory=list)
    last_event_id: int | None = None


@dataclass
class Policy:
    id: int
    jurisdiction: int
    proposal_id: int
    sector: str
    objective: str
    intensity: float
    budget: int
    money: int
    start_time: int
    status: str = 'active'
    spent: int = 0
    refunded: int = 0
    work_done: int = 0
    work_required: int = 8
    last_work: int = -1
    workers: list[int] = field(default_factory=list)
    effects: dict = field(default_factory=dict)
    barriers: dict = field(default_factory=dict)
    history: list[int] = field(default_factory=list)
    source_fact: int | None = None


@dataclass
class Divinity:
    id: int
    name: str
    domain: str
    values: dict
    power: float
    origin: str
    location: Location
    alive: bool = True
    known_followers: list[int] = field(default_factory=list)
    influence: list[int] = field(default_factory=list)
    relations: dict[int, int] = field(default_factory=dict)
    memory: list[int] = field(default_factory=list)
    interventions: list[int] = field(default_factory=list)
    energy: float = 100
    last_intervention: int = -1000
    essence: dict = field(default_factory=dict)
    mortal_origin: int | None = None
    bonds: list[int] = field(default_factory=list)
    action_pressure: ActionPressure = field(default_factory=ActionPressure)
    affinities: dict[int, dict] = field(default_factory=dict)
    presence_regions: list[int] = field(default_factory=list)
    messages: list[dict] = field(default_factory=list)


@dataclass
class PointOfInterest:
    id: int
    name: str
    kind: str
    position: Location
    depth: int = 1
    areas: list[str] = field(default_factory=list)
    danger: int = 0
    shelter: bool = True
    inventory: dict[int, int] = field(default_factory=dict)
    remains: list[int] = field(default_factory=list)
    history: list[int] = field(default_factory=list)
    claimant_id: int | None = None
    contested_by: list[int] = field(default_factory=list)
    sacred_to: list[int] = field(default_factory=list)
    needs: dict[str, Need] = field(default_factory=dict)
    goal: Goal | None = None


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
    schema_version: int = 1
    parent_event_ids: list[int] = field(default_factory=list)
    decision_id: str | None = None
    action_attempt_id: str | None = None
    related_decision_ids: list[str] = field(default_factory=list)

    def __post_init__(self):
        self.context=deepcopy(self.context)
        self.witnesses=list(self.witnesses)
        self.parent_event_ids=list(self.parent_event_ids)
        self.related_decision_ids=list(self.related_decision_ids)


@dataclass
class ActionAttempt:
    id: str
    actor_id: int
    turn: int
    goal_id: int
    action: str
    target_id: int | None
    success: bool | None = None
    outcome: str = ''
    emitted_event_ids: list[int] = field(default_factory=list)


@dataclass
class DecisionTrace:
    id: str
    actor_id: int
    turn: int
    lod: int
    need_episode_id: str | None = None
    need_kind: str | None = None
    need_priority: float = 0
    source_fact_ids: list[int] = field(default_factory=list)
    generated_actions: list[dict] = field(default_factory=list)
    blocked_actions: list[dict] = field(default_factory=list)
    evaluated_scores: list[dict] = field(default_factory=list)
    selected_action: str | None = None
    selected_score: float | None = None
    selected_target_id: int | None = None
    selected_resource_kind: str | None = None
    goal_id: int | None = None
    action_attempt_id: str | None = None
    success: bool | None = None
    outcome: str = ''
    emitted_event_ids: list[int] = field(default_factory=list)
    important: bool = False
    truncated: dict[str,int] = field(default_factory=dict)
    schema_version: int = 1
    related_event_ids: list[int] = field(default_factory=list)

    need_options: list[dict] = field(default_factory=list)


@dataclass
class LearningReceipt:
    receiver_id: int
    event_id: int
    turn: int
    channel: str
    source_id: int | None
    confidence_before: int
    confidence_after: int


@dataclass
class HistoricalObservability:
    schema_version: int = 1
    level: str = 'NORMAL'
    next_id: int = 1
    decisions: dict[str,DecisionTrace] = field(default_factory=dict)
    attempts: dict[str,ActionAttempt] = field(default_factory=dict)
    recent_decisions: list[str] = field(default_factory=list)
    learning: list[LearningReceipt] = field(default_factory=list)
    recent_learning: list[LearningReceipt] = field(default_factory=list)
    event_archive: dict[int,Event] = field(default_factory=dict)
    counters: dict[str,int] = field(default_factory=dict)
    causal: dict = field(default_factory=dict)
    tombstones: dict[int, dict] = field(default_factory=dict)
    last_decision_ids: dict[int,str] = field(default_factory=dict)


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
    groups: dict[int, Group] = field(default_factory=dict)
    proposals: dict[int, Proposal] = field(default_factory=dict)
    divinities: dict[int, Divinity] = field(default_factory=dict)
    social_initialized: bool = False
    faith_health: dict[int, dict] = field(default_factory=dict)
    routes: dict[int, Route] = field(default_factory=dict)
    divine_contracts: dict[int, DivineContract] = field(default_factory=dict)
    sacred_sites: dict[int, dict] = field(default_factory=dict)
    geography_initialized: bool = False
    institutional_tasks: dict[int, InstitutionalTask] = field(default_factory=dict)
    institutional_policies: dict[int, Policy] = field(default_factory=dict)
    generation_version: str = ''
    generation_config: dict = field(default_factory=dict)
    observability: HistoricalObservability = field(default_factory=HistoricalObservability)

    def allocate_id(self) -> int:
        entity_id = self.next_id
        self.next_id += 1
        return entity_id
