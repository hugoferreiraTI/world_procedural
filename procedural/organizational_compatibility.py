"""Adequação organizacional percebida; afinidade pessoal é um componente."""
from dataclasses import dataclass,field


@dataclass(frozen=True)
class OrganizationalCompatibility:
    acceptable: bool
    score: float
    reason: str
    components: dict = field(default_factory=dict)


def assess(engine,p,g,cause,subject):
    if g.cause!=cause or g.subject_id!=subject:return OrganizationalCompatibility(False,0,'different_objective')
    if g.status!='active':return OrganizationalCompatibility(False,0,'inactive')
    if g.plan.get('closed'):return OrganizationalCompatibility(False,0,'closed')
    if len(g.member_ids)>=64:return OrganizationalCompatibility(False,0,'capacity_reached')
    if len(p.group_ids)>=3:return OrganizationalCompatibility(False,0,'too_many_commitments')
    leader=engine.world.characters.get(g.leader_id)
    if not leader or not leader.alive:return OrganizationalCompatibility(False,0,'leader_unavailable')
    known=p.known_groups.get(g.id,{})
    trust=engine.graph.value(p.id,leader.id,'confiança',10)
    hostility=engine.graph.value(p.id,leader.id,'inimizade')
    if trust<5 or hostility>=50:return OrganizationalCompatibility(False,0,'hostility_or_distrust')
    if cause=='religious_interest' and subject not in p.beliefs:return OrganizationalCompatibility(False,0,'incompatible_belief')
    if p.position.map_id!=g.town_id and not engine.geography.plan(p,g.town_id):return OrganizationalCompatibility(False,0,'route_unknown')
    strategy=known.get('strategy','cooperation')
    illegal=strategy=='criminal_cooperation'
    if illegal and p.personality.honesty>=60:return OrganizationalCompatibility(False,0,'strategy_conflict')
    # Apenas fracassos comunicados a ESTE personagem entram no juízo.
    evidence=[f for f in p.knowledge.values() if f.confidence>=60 and
              (f.context.get('group_id')==g.id or g.id in f.context.get('supporting_groups',()))]
    failures=sum(f.kind in ('PolicyBlocked','PolicyDecided') and
                 (f.kind=='PolicyBlocked' or f.context.get('result',{}).get('decision')=='reject') for f in evidence[-24:])
    successes=sum(f.kind in ('PolicyEffect','PolicyCompleted') for f in evidence[-24:])
    affinity=engine.society.affinity(p,leader,cause)
    components={'shared_cause':40,'objective_alignment':15,'known_strategy':10,
        'locality':10 if p.position.map_id==g.town_id else 3,
        'known_effectiveness':min(10,successes*3)-min(20,failures*4),
        'social_affinity':min(15,max(0,affinity*.2)),
        'dues':-max(0,known.get('dues',0))*3,
        'autonomy_cost':-p.personality.independence*.1,
        'legal_risk':-p.personality.honesty*.25 if illegal else 0,
        'existing_membership':-len(p.group_ids)*4,'hostility':-max(0,hostility)*.2}
    score=round(sum(components.values()),2)
    if failures>=3 and p.personality.independence>=80 and p.personality.ambition>=85:
        return OrganizationalCompatibility(False,score,'known_failure_and_leadership_preference',components)
    return OrganizationalCompatibility(score>=50,score,'shared_problem_and_access' if score>=50 else 'cost_or_known_ineffectiveness',components)
