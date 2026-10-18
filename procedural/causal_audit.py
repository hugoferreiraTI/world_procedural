"""Métricas V1.1 privadas. Não escolhe ações, consulta RNG ou publica Facts.

Solvabilidade não avaliada permanece UNKNOWN. Probes só cobrem ações vitais
imediatas e emprego local; não simulam fornecedores COMMAND em consultas.
"""
from collections import Counter
from statistics import median
from .needs import FINISHED
from .navigation import distance

SURVIVAL = {'food','water','food_reserve','rest','recovery','healing'}


class CausalAudit:
    def __init__(self, engine):
        self.e, self.w = engine, engine.world
        self.data = self.w.observability.causal
        self.e.items.listeners.append(self.inventory)

    @property
    def enabled(self): return self.w.observability.level != 'OFF'

    def count(self, key, amount=1):
        if self.enabled:
            counts=self.data.setdefault('counts',{})
            counts[key]=counts.get(key,0)+amount

    def sample(self, category, row, limit=128):
        if not self.enabled:return
        rows=self.data.setdefault(category,[]); rows.append(row)
        del rows[:-limit]

    def inventory(self, operation, owner, kind, quantity):
        if not self.enabled or kind not in ('food','water','grain'):return
        town=self.w.towns.get(owner)
        if town:
            self.count(f'flow:{town.id}:{kind}:{operation}',quantity)
        elif operation=='consumed' and owner in self.w.characters:
            p=self.w.characters[owner]
            if p.position.map_id in self.w.towns:
                self.count(f'persistent_consumption:{p.position.map_id}:{kind}',quantity)

    def need_row(self,p,n):
        key=n.need_episode_id
        row=self.data.setdefault('episodes',{}).setdefault(key,{
            'actor':p.id,'kind':n.kind,'created':n.created_at,'active_hours':0,
            'top_rank_hours':0,'solvable_hours':0,'unknown_solvability_hours':0,
            'selected_count':0,'executed_count':0,'successful_count':0,
            'blocked_by_higher_need_count':0,'time_until_first_selection':None,
            'time_until_resolution':None,'reactivation_count':int(n.episode>1),
            'expiration_count':0,'lod':p.lod})
        return row

    def probe(self,p,n):
        """QUERY parcial: True prova ao menos uma alternativa; None não inventa."""
        if n.kind=='food' and p.hunger>=35 and self.e.items.count(p.id,'food'):return True
        if n.kind=='water':
            if self.e.items.count(p.id,'water'):return True
            t=self.w.towns.get(p.position.map_id)
            if t and self.e.items.count(t.id,'water') and 'Poço' in self.e.navigation.describe(p.position)[1]:return True
        if n.kind in ('work','money') and p.position==p.workplace:
            return self.e.professions.work_gate(p) is None
        return None

    def end_episode(self,p,n,status):
        if not self.enabled or not hasattr(p,'is_player'):return
        row=self.need_row(p,n)
        if row['time_until_resolution'] is None:
            row['time_until_resolution']=self.w.turn-n.created_at
            row['expiration_count']=int(status!='satisfied')

    def physiology(self,p,before):
        if not self.enabled:return
        state=self.data.setdefault('actors',{}).setdefault(p.id,{})
        growth=state.setdefault('physiology_growth',{})
        for kind,value in before.items():
            delta=max(0,getattr(p,kind)-value)
            growth[kind]=growth.get(kind,0)+delta
            self.count('physiology_hourly:'+p.lod+':'+kind,delta)

    def selection(self,p,active,selected):
        if not self.enabled:return
        state=self.data.setdefault('actors',{}).setdefault(p.id,{})
        state.update(top=active[0].need_episode_id if active else None, last_decision=self.w.turn,
                     hunger=p.hunger,thirst=p.thirst,fatigue=p.fatigue,lod=p.lod)
        trace=self.e.observability.current
        for n in active:
            row=self.need_row(p,n)
            evaluated=self.e.goals.evaluated_choices.get((p.id,n.id))
            solvable=bool(evaluated) if evaluated is not None else self.probe(p,n)
            row.update(last_solvable=solvable,last_evaluated=self.w.turn,lod=p.lod)
            if trace:self.e.observability.detail('need_options',{'episode':n.need_episode_id,
                'kind':n.kind,'priority':n.priority,'solvable':solvable,'selected':n is selected})
            if n is selected:
                row['selected_count']+=1
                if row['time_until_first_selection'] is None:
                    row['time_until_first_selection']=self.w.turn-n.created_at
                    row['first_selection_lod']=p.lod
                self.count('selected_need:'+n.kind);self.count('selected_lod:'+p.lod)
            elif selected and solvable and selected.priority>=n.priority:
                row['blocked_by_higher_need_count']+=1
                self.count('need_lost:'+n.kind+':'+selected.kind)
        self.count('decisions_lod:'+p.lod)
        old=state.get('previous_decision')
        if old is not None:
            gap=self.w.turn-old;self.count('decision_gap_sum:'+p.lod,gap);self.count('decision_gap_count:'+p.lod)
            for kind in ('hunger','thirst','fatigue'):
                self.count('net_gap:'+p.lod+':'+kind,max(0,getattr(p,kind)-state.get('previous_'+kind,getattr(p,kind))))
                self.count('physiology_gap:'+p.lod+':'+kind,state.get('physiology_growth',{}).get(kind,0))
        state['physiology_growth']={}
        state['previous_decision']=self.w.turn
        for kind in ('hunger','thirst','fatigue'):state['previous_'+kind]=getattr(p,kind)

    def outcome(self,p,goal,success):
        if not self.enabled or p.is_player and not success:return
        n=next((n for n in p.needs.values() if n.id==goal.need_id),None)
        if n:
            row=self.need_row(p,n);row['executed_count']+=1;row['successful_count']+=int(success)
        self.count('attempt:'+goal.action);self.count(('success:' if success else 'failure:')+goal.action)

    def hourly(self):
        if not self.enabled:return
        for p in self.w.characters.values():
            state=self.data.get('actors',{}).get(p.id,{})
            if p.alive:
                critical=max(p.hunger,p.thirst)>=80
                if critical and not state.get('critical',False):self.count('critical_episodes:'+p.lod)
                if state:state['critical']=critical
            for n in p.needs.values():
                if n.need_episode_id not in self.data.get('episodes',{}):continue
                row=self.need_row(p,n)
                if n.status not in FINISHED and p.alive:
                    row['active_hours']+=1
                    self.count('need_active_lod:'+p.lod+':'+n.kind)
                    row['top_rank_hours']+=int(state.get('top')==n.need_episode_id)
                    # Solvabilidade só é afirmada na hora da observação, sem
                    # extrapolar estoque/rotas/autoridade entre decisões.
                    current=row.get('last_evaluated')==self.w.turn-1
                    if current and row.get('last_solvable') is True:row['solvable_hours']+=1
                    elif not current or row.get('last_solvable') is None:row['unknown_solvability_hours']+=1
                elif row['time_until_resolution'] is None:
                    row['time_until_resolution']=self.w.turn-n.created_at
                    row['expiration_count']=int(n.status!='satisfied')
        if self.w.turn%24==0:self.daily()

    def daily(self):
        rows=self.data.setdefault('town_days',[])
        for t in self.w.towns.values():
            people=[p for p in self.w.characters.values() if p.alive and p.position.map_id==t.id]
            d=self.e.economy.food_diagnosis(t);stock=d['stock'];water_need=len(people)*48/45
            food_need=d['expected_demand'];water_real=t.production_today.get('water',0)
            rows.append({'turn':self.w.turn,'town':t.id,'kind':'capital' if t.capital else t.kind,
                'persistent_population':len(people),'abstract_population':t.abstract_population,
                'food_stock':stock['food'],'water_stock':stock['water'],'grain_stock':stock['grain'],
                'potential_food':d['production_capacity'],'potential_water':t.infrastructure['water_daily'],
                'realized_food':t.production_previous.get('food',0),'realized_water':water_real,
                'abstract_food_consumption':self.data.get('counts',{}).get(f'abstract_consumption:{t.id}:food',0),
                'abstract_water_consumption':0,'abstract_water_model':'not modeled; no consumption invented',
                'consumption_window':'cumulative since creation; difference adjacent rows for daily flow',
                'persistent_food_consumption':self.data.get('counts',{}).get(f'persistent_consumption:{t.id}:food',0),
                'persistent_water_consumption':self.data.get('counts',{}).get(f'persistent_consumption:{t.id}:water',0),
                'well_water_consumption':self.data.get('counts',{}).get(f'flow:{t.id}:water:consumed',0),
                'market_price':d.get('price',self.e.economy.price(t.id,'food')),
                'median_personal_money':median([p.money for p in people]) if people else 0,
                'food_affordability':sum(p.money>=self.e.economy.price(t.id,'food') for p in people)/max(1,len(people)),
                'water_accessibility':sum(any(k.startswith('well') for k in p.known_places) for p in people)/max(1,len(people)),
                'reserve_days_food':round(stock['food']/food_need,3) if food_need else None,
                'reserve_days_water':round(stock['water']/water_need,3) if water_need else None})
        self.sample('gods',[{'id':g.id,'turn':self.w.turn,'messages_received':len(g.messages),
            'facts_known':len({m['source_fact'] for m in g.messages}),'presence_regions':list(g.presence_regions),
            'energy':g.energy,'last_intervention':g.last_intervention,'affinities':len(g.affinities)}
            for g in self.w.divinities.values()],32)
        # Janelas por dia, contadores permanecem cumulativos e podem ser subtraídos.

    def death(self,p):
        if not self.enabled:return
        factors=[];stock={};causes=[k for k,v in (('food',p.hunger),('water',p.thirst)) if v>=100]
        t=self.w.towns.get(p.position.map_id)
        for kind in causes:
            total=sum(self.e.items.count(t.id,kind) for t in self.w.towns.values())
            material=sum(self.e.items.owner(i.owner_id).inventory.get(i.id,0) for i in self.w.items.values() if i.kind==kind)
            local=self.e.items.count(t.id,kind) if t else 0
            owned=self.e.items.count(p.id,kind);stock[kind]={'world_market':total,'world_material_stock':material,'local_market':local,'owned':owned}
            if not material:factors.append('WORLD_SHORTAGE')
            if not local:factors.append('LOCAL_SHORTAGE')
            if owned:
                factors.append('RESOURCE_OWNED_AT_DEATH')
                if kind=='food' and self.w.turn-p.food_state.get('last_acquisition',-1000)<=1:factors.append('ACQUIRED_TOO_LATE')
            if kind=='food' and local and not owned:
                if p.money==0:factors.append('NO_MONEY')
                elif t and p.money<self.e.economy.price(t.id,kind):factors.append('AFFORDABILITY')
                if 'market' not in p.known_places:factors.append('KNOWLEDGE_FAILURE')
            if kind=='water' and not any(k.startswith('well') for k in p.known_places):factors.append('KNOWLEDGE_FAILURE')
        goal=p.goal
        if goal and goal.destination and goal.destination!=p.position:factors.append('TRAVEL_TIME')
        if self.w.turn-p.last_update>1:factors.append('LOD_OPPORTUNITY')
        last=self.e.observability.data.decisions.get(self.e.observability.data.last_decision_ids.get(p.id))
        if last and last.need_kind not in SURVIVAL and max(p.hunger,p.thirst)>=100:factors.append('PRIORITY_COMPETITION')
        if last and last.success is False and last.selected_action in ('buy_food','forage','drink_well','work_for_food'):factors.append('FAILED_ACQUISITION')
        if last and last.success is False and last.selected_action in ('eat','drink'):factors.append('FAILED_CONSUMPTION')
        if not factors:factors=['OTHER_UNKNOWN']
        row={'actor':p.id,'turn':self.w.turn,'lod':p.lod,'factors':sorted(set(factors)),
             'stock':stock,'last_decision':last.id if last else None,'goal':goal.action if goal else None,
             'last_update':p.last_update,'hunger':p.hunger,'thirst':p.thirst,'health':p.health}
        self.data.setdefault('deaths',{})[p.id]=row
        self.count('deaths_lod:'+p.lod)
        for f in set(factors):self.count('death_factor:'+f)

    def event(self,event):
        if not self.enabled:return
        self.count('event:'+event.kind)
        trace=self.e.observability.current
        p=self.w.characters.get(event.actor_id)
        if p:self.count('activity_lod:'+p.lod+':'+event.kind)
        if event.kind in ('ItemStolen','PersonalItemStolen','CharacterAttacked','CharacterKilled') and not event.context.get('lawful') and not event.context.get('self_defense'):
            self.count('crime_event:'+event.kind)
            self.count('crime_with_witness:'+event.kind,int(any(i not in (event.actor_id,event.target_id) for i in event.witnesses)))
        if event.kind=='CharacterAttacked':
            c=event.context
            trace=self.e.observability.current
            nk=trace.need_kind if trace else None
            motive=('law_enforcement' if c.get('lawful') else 'self_defense' if c.get('self_defense') else 'protective' if nk=='protection' else 'retributive' if nk=='revenge' else 'theft_response' if nk=='response' else 'hedonic' if c.get('lethal_mode')=='hedonic' else 'instrumental' if c.get('violence_intent')=='kill' else 'other')
            self.count('attack_motive:'+str(motive))
        if event.kind in ('TrainingStarted','ProfessionChanged','CharacterCaptured','FactionFormalized','InstitutionalTaskCompleted'):
            self.sample('cases',{'event':event.id,'kind':event.kind,'turn':event.turn,'actor':event.actor_id,'target':event.target_id,'parents':event.parent_event_ids},256)
