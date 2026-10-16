"""Auditoria observacional da Fase 3.2; reutiliza seeds e política pública anterior."""
import argparse
from collections import Counter
from dataclasses import asdict
import gzip
import json
import math
from pathlib import Path
import statistics

from experiments import phase3_audit
from experiments.feeding_audit import FeedingAudit, core_hash
from experiments.perspective_audit import write_json
from procedural.navigation import distance
from procedural.rules import FEEDING
from procedural.personal import PERSONAL_KINDS

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'reports/fase_3_2'


class Phase32Audit(FeedingAudit):
    def __init__(self, directory, mode):
        super().__init__(directory, mode)
        self.counts = Counter();self.winners = Counter();self.healthy_winners = Counter()
        self.work = Counter();self.information = Counter();self.samples = Counter()
        self.economic_stream = gzip.open(directory/'economia_acoes.jsonl.gz', 'wt', encoding='utf-8')
        self.decision_stream = gzip.open(directory/'decisoes_amostras.jsonl.gz', 'wt', encoding='utf-8')
        self.personal_context_stream = gzip.open(directory/'contexto_pessoal.jsonl.gz', 'wt', encoding='utf-8')
        self.economic_frames = []
        self.phase32_installed = False
        self.context = None
        self.dedup_turn = None;self.dedup = set()

    def sample(self, category, row):
        if self.samples[category] < 10:
            self.line(self.decision_stream, {'category':category, **row});self.samples[category] += 1

    def __call__(self, engine):
        super().__call__(engine)
        if not self.phase32_installed:
            self.phase32_installed = True
            original_refresh = engine.needs.refresh
            def refresh(person):
                active = original_refresh(person)
                if self.context is not None and person.id == self.context['npc_id']:
                    reserve = next((n for n in active if n.kind == 'food_reserve'), None)
                    if reserve:
                        self.context['reserve'] = asdict(reserve)
                return active
            engine.needs.refresh = refresh
            original_count = engine.needs.count
            def count(transition, kind, owner=None):
                original_count(transition,kind,owner)
                if self.context is not None and transition == 'Selected' and getattr(owner,'id',None) == self.context['npc_id']:
                    self.context['selected'] = kind
            engine.needs.count = count
            original_decide = engine.goals.decide
            def decide(person, elapsed=1):
                town = engine.world.towns[person.town_id]
                previous_position = person.position
                self.context = {'turn':engine.world.turn,'npc_id':person.id,'name':person.name,
                    'hunger':person.hunger,'money':person.money,'food_before':engine.items.count(person.id,'food'),
                    'real_affordable_market_for_auditor':engine.items.count(town.id,'food')>0 and person.money>=engine.economy.price(town.id,'food'),
                    'previous_goal':asdict(person.goal) if person.goal else None,'selected':None}
                original_decide(person,elapsed)
                row = self.context;self.context = None
                self.counts['decisions'] += 1
                if 'reserve' in row:
                    ctx = row['reserve']['context'];selected = row['selected'] or 'none'
                    self.counts['reserve_active'] += 1;self.winners[selected] += 1
                    self.counts['reserve_selected'] += selected == 'food_reserve'
                    self.counts['coverage_hours_sum'] += ctx['coverage_hours']
                    if row['hunger'] < 50:
                        self.counts['healthy_deficit'] += 1;self.healthy_winners[selected] += 1
                        self.counts['healthy_reserve_selected'] += selected == 'food_reserve'
                        known = ctx['affordable_observed_market']
                        self.counts['healthy_known_opportunity'] += known
                        self.counts['healthy_known_opportunity_lost'] += known and selected != 'food_reserve'
                        self.counts['healthy_real_opportunity_lost'] += row['real_affordable_market_for_auditor'] and selected != 'food_reserve'
                        self.sample('healthy_reserve_'+selected,row)
                    self.sample('reserve_'+selected,row)
                if person.goal and person.goal.status == 'active' and person.goal.destination:
                    self.counts['travel_decisions_with_deficit'] += engine.feeding.reserve_target(person)>engine.items.count(person.id,'food')
                if person.goal and person.goal.created_at == engine.world.turn and person.goal.destination and person.position != previous_position:
                    hours = distance(previous_position,person.goal.destination)
                    if hours < 1000:
                        target = min(FEEDING.maximum_reserve,math.ceil(max(FEEDING.reserve_hours,hours+FEEDING.travel_margin_hours)*FEEDING.hunger_per_hour/FEEDING.meal_reduction))
                        self.counts['trips_started'] += 1
                        self.counts['trips_started_with_deficit'] += row['food_before'] < target
            engine.goals.decide = decide
            original_execute = engine.goals.execute
            def execute(person, goal, hours):
                need = next((n for n in person.needs.values() if n.id == goal.need_id), None)
                income = goal.action in ('work','train','work_for_food','temporary_service','work_for_meal','service_meal')
                personal = {'turn':engine.world.turn,'npc_id':person.id,'profession':person.profession,
                            'goal_id':goal.id,'money':person.money,'food':engine.items.count(person.id,'food'),
                            'need_id':need.id,'need_created_at':need.created_at} if need and need.kind in PERSONAL_KINDS else None
                row = None
                if income:
                    row = {'turn':engine.world.turn,'npc_id':person.id,'name':person.name,'profession':person.profession,
                        'goal':asdict(goal),'need':asdict(need) if need else None,'hours':hours,
                        'money_before':person.money,'credit_before':person.wage_credit,
                        'food_before':engine.items.count(person.id,'food'),
                        'known_offer':dict(person.market_observation),
                        'town_money':engine.world.towns[person.town_id].money}
                result = original_execute(person,goal,hours)
                if personal is not None:
                    personal.update(success=result[0],money_after=person.money,food_after=engine.items.count(person.id,'food'))
                    self.line(self.personal_context_stream,personal)
                if row is not None:
                    row.update(success=result[0],outcome=result[1],money_after=person.money,credit_after=person.wage_credit,
                               food_after=engine.items.count(person.id,'food'))
                    self.line(self.economic_stream,row)
                    self.work[goal.action+':attempts'] += 1
                    self.work[goal.action+':success'] += bool(result[0])
                    self.work[goal.action+':paid_coins'] += max(0,person.money-row['money_before'])
                    self.work[goal.action+':fractional_credit_success'] += bool(result[0] and person.money == row['money_before'] and person.wage_credit>row['credit_before'])
                    if not result[0]:self.work[goal.action+':failure:'+result[1]] += 1
                return result
            engine.goals.execute = execute
            original_work = engine.professions.work
            def work(person,hours=1):
                result = original_work(person,hours)
                self.work['status:'+result.status] += 1
                self.work['produced_units'] += result.produced
                self.work['wage_sixths_accrued'] += result.credit_added
                return result
            engine.professions.work = work
            original_buy = engine.economy.buy_reserve
            def buy_reserve(person, target, bulk=False):
                before = engine.items.count(person.id,'food')
                result = original_buy(person,target,bulk)
                after = engine.items.count(person.id,'food')
                if result[0]:
                    self.counts['reserve_purchase_first_ration'] += before == 0 and after >= 1
                    self.counts['reserve_purchase_second_ration'] += before <= 1 and after >= 2
                    self.counts['reserve_purchase_only_second'] += before == 1 and after >= 2
                    self.counts['reserve_purchase_partial'] += after < target
                return result
            engine.economy.buy_reserve = buy_reserve
            original_repeated = engine.personal_actions.repeated_reply
            def repeated(receiver,giver,need):
                result = original_repeated(receiver,giver,need)
                if result:
                    if self.dedup_turn != engine.world.turn:
                        self.dedup.clear();self.dedup_turn = engine.world.turn
                    key = receiver.id,giver.id,need.id
                    if key not in self.dedup:
                        self.dedup.add(key);self.information['repeated_reply_avoided'] += 1
                return result
            engine.personal_actions.repeated_reply = repeated
        elapsed = engine.world.turn-self.start
        if elapsed % 250 == 0 and (not self.economic_frames or self.economic_frames[-1]['elapsed'] != elapsed):
            self.economic_frames.append(self.inequality(engine,elapsed))

    @staticmethod
    def inequality(engine, elapsed):
        towns = []
        for town in engine.world.towns.values():
            people = [c for c in engine.world.characters.values() if c.alive and not c.is_player and c.position.map_id == town.id]
            wealth = [c.money for c in people];price = engine.economy.price(town.id,'food')
            stock = {k:engine.items.count(town.id,k) for k in ('food','grain','iron','wood')}
            poor = [c for c in people if c.money < price]
            towns.append({'id':town.id,'name':town.name,'municipal_money':town.money,'stock':stock,'price':price,
                'resident_money':sum(wealth),'mean_money':statistics.mean(wealth) if wealth else 0,
                'median_money':statistics.median(wealth) if wealth else 0,'poor':len(poor),
                'poor_with_municipal_food':len(poor) if stock['food'] else 0,
                'poor_saturated':sum(engine.professions.saturated(c,{'stock':stock}) for c in poor),
                'poor_without_professional_activity':sum(not engine.professions.compatible_workplace(c) for c in poor),
                'unemployed':sum(c.profession is None for c in people),
                'meal_distribution_capacity':engine.professions.temporary_capacity(town).get('meal_distribution',{}).get('capacity',0),
                'resident_wealth':{str(c.id):c.money for c in people}})
        return {'elapsed':elapsed,'turn':engine.world.turn,'towns':towns}

    def finish(self, report):
        self.economic_stream.close();self.decision_stream.close();self.personal_context_stream.close()
        write_json(self.directory/'quadros_desigualdade.json',self.economic_frames)
        metrics = self.engine.world.metrics
        result = {'mode':self.mode,'counts':dict(self.counts),'reserve_winners':dict(self.winners),
            'healthy_reserve_winners':dict(self.healthy_winners),'income':dict(self.work),
            'information':dict(self.information),
            'social_metrics':{k:v-self.initial.get(k,0) for k,v in metrics.items() if k.startswith(('InformationReply:','ReportBlocked','ReservePurchase','WorkOutcome:'))},
            'method':'Observadores envolvem chamadas originais; não acrescentam decisões, fatos ou sorteios. Contagens de reserva são avaliações, não pessoas. Riqueza local é informação do auditor.'}
        write_json(self.directory/'metricas_fase32.json',result)
        super().finish(report)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--mode',required=True,choices=('jogador','espectador','mundo'))
    p.add_argument('--turnos',type=int,default=1000)
    p.add_argument('--stage',default='curta_v1')
    a = p.parse_args();directory = OUT/a.stage/a.mode
    if directory.exists() and any(directory.iterdir()):raise ValueError('Auditoria não sobrescreve resultados.')
    before = core_hash()
    if a.stage == 'auditorias':
        assert before == json.loads((OUT/'manifesto_auditoria.json').read_text())['core_sha256']
    original = phase3_audit.Phase3Audit;phase3_audit.Phase3Audit = Phase32Audit
    try:phase3_audit.run('Mira' if a.mode == 'mundo' else 'Dovha',a.turnos,directory,a.mode)
    finally:phase3_audit.Phase3Audit = original
    assert core_hash() == before


if __name__ == '__main__':main()
