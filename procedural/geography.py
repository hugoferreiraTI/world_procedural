"""Rotas físicas e conhecimento individual, usando os mapas e o Event Bus existentes."""
from collections import defaultdict
from dataclasses import asdict, replace
import heapq
import math

from .models import Journey, Location, Route, RouteKnowledge
from .navigation import distance

TRAVEL_ACTIONS = {'route_travel', 'ask_route', 'explore_route'}


class Geography:
    def __init__(self, engine):
        self.e, self.w = engine, engine.world
        self.adjacent = defaultdict(list)
        for route in self.w.routes.values():
            self.adjacent[route.origin].append(route.id)
            self.adjacent[route.destination].append(route.id)

    def emit(self, event_kind, p, target=None, **context):
        return self.e.recorder.emit(event_kind, f'{p.name}: {event_kind}.', p.id, target,
                                   p.position, historical=True, context=context)

    def place(self, id):
        return self.w.towns.get(id) or self.w.points.get(id)

    def connect(self, a, b, kind='road'):
        if any({r.origin, r.destination} == {a, b} for r in self.w.routes.values()):
            return
        start, end = self.place(a).position, self.place(b).position
        path = [start]
        current = start
        while current != end:
            dx = (end.x > current.x) - (end.x < current.x)
            dy = 0 if dx else (end.y > current.y) - (end.y < current.y)
            current = Location(self.w.world_map_id, current.x + dx, current.y + dy)
            path.append(current)
        terrain = self.w.maps[self.w.world_map_id].rows[start.y][start.x]
        speed = 2 if terrain in ('S', 'D') or kind == 'trail' else 3
        route = Route(self.w.allocate_id(), a, b, len(path)-1,
                      math.ceil((len(path)-1)/speed), terrain,
                      12 if kind == 'trail' else 4, route_type=kind, path=path)
        self.w.routes[route.id] = route
        self.adjacent[a].append(route.id); self.adjacent[b].append(route.id)

    def know_place(self, p, id, source, confidence=100, state='KNOWN', source_id=None):
        place = self.place(id)
        if not place:
            return
        old = p.place_knowledge.get(id, {})
        rank = {'RUMORED': 1, 'KNOWN': 2, 'VISITED': 3, 'EXPLORED': 4, 'CLAIMED': 5}
        if rank.get(old.get('state'), 0) > rank.get(state, 0):
            state = old['state']
        p.place_knowledge[id] = {'name': place.name, 'position': asdict(place.position),
                                'confidence': max(confidence, old.get('confidence', 0)),
                                'source': source, 'source_id': source_id,
                                'learned_at': self.w.turn, 'state': state}
        if id in self.w.towns:
            if id in p.known_towns and p.known_towns[id].get('position') is None:p.known_towns.pop(id)
            p.known_towns.setdefault(id, {'position': asdict(place.position), 'confidence': confidence,
                                        'source': source, 'source_fact': source_id, 'learned_at': self.w.turn})

    def learn(self, p, route, origin, source, confidence=100, source_id=None):
        destination = route.destination if route.origin == origin else route.origin
        key = f'{origin}:{destination}'
        old = p.route_knowledge.get(key)
        if old and old.confidence >= confidence:
            return False
        p.route_knowledge[key] = RouteKnowledge(p.id, origin, destination, route.id, confidence,
                                               source, self.w.turn, source_id=source_id,
                                               travel_time=route.travel_time, danger=route.danger,
                                               condition=route.condition)
        for id in (origin, destination):
            self.know_place(p, id, source, confidence, source_id=source_id)
        self.emit('RouteKnowledgeCreated', p, destination, origin=origin, route_id=route.id,
                  confidence=confidence, source=source, source_id=source_id)
        return True

    def bootstrap(self):
        if self.w.geography_initialized:
            return
        self.w.geography_initialized = True
        for kingdom in self.w.kingdoms.values():
            for id in kingdom.city_ids:
                if id != kingdom.capital_id:
                    self.connect(kingdom.capital_id, id)
            for id in kingdom.village_ids:
                t = self.w.towns[id]
                parent = t.authority_town_id or min(kingdom.city_ids, key=lambda c: distance(t.position, self.w.towns[c].position))
                t.authority_town_id = parent
                self.connect(id, parent)
        capitals = [k.capital_id for k in self.w.kingdoms.values()]
        # Uma árvore de estradas entre capitais; conhecer esses enlaces exige história própria.
        connected = capitals[:1]
        while len(connected) < len(capitals):
            _, a, b = min((distance(self.place(a).position, self.place(b).position), a, b)
                         for a in connected for b in capitals if b not in connected)
            self.connect(a, b); connected.append(b)
        for point in self.w.points.values():
            nearest = min(self.w.towns.values(), key=lambda t: distance(t.position, point.position))
            self.connect(nearest.id, point.id, 'trail')
        for p in self.w.characters.values():
            self.know_place(p, p.town_id, 'residence')
            local = p.position.map_id if self.place(p.position.map_id) else p.town_id
            candidates = [self.w.routes[i] for i in self.adjacent[local]]
            if p.organization_ids and local in self.w.points:
                selected = candidates
            elif self.w.towns[p.town_id].kind == 'vila':
                selected = [r for r in candidates if self.w.towns[p.town_id].authority_town_id in (r.origin, r.destination)]
            elif p.profession in ('governante', 'conselheiro'):
                kingdom = self.w.kingdoms[self.w.towns[p.town_id].kingdom_id]
                selected = [r for r in self.w.routes.values() if r.origin in kingdom.city_ids and r.destination in kingdom.city_ids]
            elif p.profession in ('comerciante', 'guarda', 'caçador'):
                selected = candidates[:3]
                if p.profession=='comerciante' and candidates:
                    selected=list({r.id:r for r in selected+[candidates[p.id % len(candidates)]]}.values())
            else:
                selected = candidates[:1]
            for route in selected:
                for origin in (route.origin, route.destination):
                    self.learn(p, route, origin, 'initial_professional_life' if p.profession in ('comerciante','guarda','caçador','governante','conselheiro') else 'initial_local_life')
            # O próprio quartel é conhecido por quem já vive nele.
            if local in self.w.points:
                self.know_place(p, local, 'residence', state='VISITED')

    def on_fact(self, p, fact):
        if fact.kind in ('PersonLocated','ResidentMoved','SearchClueShared','InvestigationClue') and fact.location and fact.confidence>=60:
            id=fact.location.map_id
            if self.place(id) and id not in p.place_knowledge:
                self.know_place(p,id,'location_report',fact.confidence,source_id=fact.event_id)
                if p.position.map_id!=id:
                    p.place_knowledge[id]['position']=None
                    if id in p.known_towns:p.known_towns[id]['position']=None
            return
        if fact.kind not in ('POIDiscovered','POIVisited','POIExplored','POIRumor','FactionKnown','FactionInvite','SacredSiteKnown','DivineManifestation'):
            return
        id = fact.context.get('place_id') or fact.context.get('headquarters') or (fact.location.map_id if fact.location else None)
        if id and self.place(id):
            # Testemunhar um relato revela sua alegação de lugar; jamais ensina suas estradas.
            own = fact.actor_id == p.id and fact.kind in ('POIDiscovered','POIVisited','POIExplored')
            state = 'VISITED' if own else 'RUMORED'
            prior=p.place_knowledge.get(id,{}).get('position')
            self.know_place(p, id, 'visit' if own else 'place_report', fact.confidence, state, fact.event_id)
            if not own and state=='RUMORED' and prior is None:
                p.place_knowledge[id]['position']=fact.context.get('reported_position')

    def plan(self, p, destination, origin=None):
        origin = origin if origin is not None else p.position.map_id
        if origin == destination:
            return [], [origin]
        graph = defaultdict(list)
        for rk in p.route_knowledge.values():
            if rk.confidence >= 60 and rk.condition != 'closed':
                graph[rk.origin].append(rk)
        heap = [(0, origin, [], [origin])]; seen = set()
        while heap:
            cost, node, routes, nodes = heapq.heappop(heap)
            if node in seen: continue
            seen.add(node)
            if node == destination: return routes, nodes
            for rk in graph[node]:
                if rk.destination not in seen:
                    heapq.heappush(heap, (cost+max(1,rk.travel_time)+rk.danger/10,
                                         rk.destination, routes+[rk.route_id], nodes+[rk.destination]))
        return None

    def hours(self, p, plan):
        return sum(p.route_knowledge[f'{a}:{b}'].travel_time for a,b in zip(plan[1],plan[1][1:])) + 10

    def block(self, p, target, reason):
        self.e.observability.gate('route_travel','NO_KNOWN_TARGET' if reason=='place_unknown' else 'NO_KNOWN_ROUTE',target,reason)
        key = f'blocked:{target}:{reason}'
        if self.w.turn-p.access_state.get(key, -1000) < 24: return
        p.access_state[key] = self.w.turn
        self.emit('RouteUnknownBlockedTravel', p, target, reason=reason,
                  origin=p.position.map_id, place_known=target in p.known_towns or target in p.place_knowledge)

    def partial(self,p,target):
        visited=p.access_state.get(f'waypoints:{target}',[])
        choices=[]
        for id,k in p.place_knowledge.items():
            if id in visited or id==p.position.map_id or id not in self.w.towns:continue
            plan=self.plan(p,id)
            if not plan or not plan[0]:continue
            # Instituições conhecidas são lugares onde procurar mais informação.
            t=self.w.towns[id]
            merit=40 if t.capital else 20 if t.kind=='cidade' else 0
            choices.append((self.hours(p,plan)-merit,id))
        return min(choices)[1] if choices else None

    def ask_candidates(self, p, target):
        local = self.w.towns.get(p.position.map_id)
        peers = [self.w.characters[i] for i in self.e.spatial.at(p.position) if i != p.id]
        if not peers and local:
            return [('ask_route', local.market, target)]
        if peers:
            return [('ask_route', None, target)]
        return []

    def candidates(self, p, target, reason, need=None):
        if p.journey:
            return [('route_travel', None, p.journey.destination)]
        if p.position.map_id == target: return []
        if target not in p.known_towns and target not in p.place_knowledge:
            self.block(p, target, 'place_unknown'); return []
        if need and need.context.get('route_waypoint')==p.position.map_id:
            need.context.pop('route_waypoint',None)
        plan = self.plan(p, target)
        if plan is None:
            self.block(p, target, 'route_unknown')
            if f'unanswered_route:{target}' in p.access_state:
                waypoint=need.context.get('route_waypoint') if need else None
                if waypoint is None:waypoint=self.partial(p,target)
                if waypoint is not None:
                    if need:need.context['route_waypoint']=waypoint
                    p.access_state[f'waypoints:{target}']=list(dict.fromkeys(p.access_state.get(f'waypoints:{target}',[])+[p.position.map_id]))
                    return self.candidates(p,waypoint,reason,need)
            return self.ask_candidates(p, target)
        food, water = self.e.migration.supplies(p, self.hours(p, plan))
        point = self.w.points.get(p.position.map_id)
        if point:
            if self.e.items.count(p.id,'food') < food and self.e.items.count(point.id,'food'):
                return [('take_site_supplies', None, point.id)]
            if self.e.items.count(p.id,'water') < water and self.e.items.count(point.id,'water'):
                return [('take_site_supplies', None, point.id)]
        local = self.w.towns.get(p.position.map_id)
        if local:
            if self.e.items.count(p.id,'food') < food:
                return [('buy_food', local.market, None)] if self.e.economy.can_seek_food(p) else [('forage', Location(local.id,1,self.w.maps[local.id].height-2),None)]
            if self.e.items.count(p.id,'water') < water: return [('fill_water', local.market,None)]
        return [('route_travel', None, target)]

    def ask(self, p, target):
        peers = [self.w.characters[i] for i in self.e.spatial.at(p.position) if i != p.id]
        peers.sort(key=lambda q: (q.profession not in ('guarda','comerciante'), -self.e.graph.value(p.id,q.id,'confiança',10), q.id))
        for q in peers:
            key=f'asked:{target}:{q.id}'
            if self.w.turn-p.access_state.get(key,-1000)<24: continue
            p.access_state[key]=self.w.turn
            self.emit('AskRoute',p,target,informant=q.id,origin=p.position.map_id)
            plan=self.plan(q,target,p.position.map_id)
            if not plan:
                p.access_state[f'unanswered_route:{target}']=self.w.turn
                return True,'A pessoa consultada não conhece esse caminho.'
            trust=self.e.graph.value(p.id,q.id,'confiança',10)
            confidence=80 if q.profession=='guarda' else 70 if trust>=30 else 45
            changed=0
            for a,b in zip(plan[1],plan[1][1:]):
                rk=q.route_knowledge[f'{a}:{b}'];route=self.w.routes.get(rk.route_id)
                if not route:continue
                confidence=min(confidence,rk.confidence)
                if {a,b}!={route.origin,route.destination}:
                    p.route_knowledge[f'{a}:{b}']=replace(rk,actor=p.id,source='directions',source_id=q.id,learned_at=self.w.turn,confidence=confidence)
                    changed+=1
                else:
                    for origin in (a,b):changed+=self.learn(p,route,origin,'directions',confidence,q.id)
            if changed:self.emit('RouteKnowledgeShared',q,p.id,destination=target,route_ids=plan[0],confidence=confidence)
            return True,'Instruções transmitidas com confiança limitada; o mapa global não foi consultado.'
        return False,'Nenhum interlocutor disponível para novas instruções.'

    def begin(self, p, target, reason, mode='known_route', guide=None):
        if not p.alive or p.combat.detention_until>self.w.turn or p.combat.surrendered_until>self.w.turn or p.health<=15:
            return False,'Condição física ou detenção impede partida.'
        if p.journey: return p.journey.destination==target,'Já existe uma viagem em andamento.'
        if target not in p.known_towns and target not in p.place_knowledge and mode=='known_route':
            self.block(p,target,'place_unknown');return False,'Localidade desconhecida.'
        guided=mode in ('follow_person','escort')
        if guided:
            if not guide or not guide.alive or guide.position!=p.position or not guide.journey or guide.journey.destination!=target:
                return False,'Não existe guia presente com viagem válida.'
            plan=(list(guide.journey.route_ids),list(guide.journey.nodes))
            knowledge=list(guide.journey.known_at_start)
            hours=sum(x['travel_time'] for x in knowledge)+10
        else:
            plan=self.plan(p,target)
            if not plan or not plan[0]:
                self.block(p,target,'route_unknown');return False,'Conexões desconhecidas.'
            knowledge=[asdict(p.route_knowledge[f'{a}:{b}']) for a,b in zip(plan[1],plan[1][1:])]
            hours=self.hours(p,plan)
        food,water=self.e.migration.supplies(p,hours)
        if self.e.items.count(p.id,'food')<food or self.e.items.count(p.id,'water')<water:
            return False,'Mantimentos reais insuficientes para o trajeto.'
        toll=sum(self.w.routes[i].toll for i in plan[0] if i in self.w.routes)
        if p.money<toll:return False,'Dinheiro insuficiente para pedágios conhecidos.'
        for a,b,rid in zip(plan[1],plan[1][1:],plan[0]):
            route=self.w.routes.get(rid)
            if not route or {a,b}!={route.origin,route.destination}:
                self.emit('RouteMismatch',p,target,route_id=rid);return False,'As instruções não correspondem à estrada encontrada.'
        if toll:
            p.money-=toll
            for rid in plan[0]:
                route=self.w.routes[rid];collector=self.w.towns.get(route.origin)
                if collector:collector.money+=route.toll
        p.journey=Journey(p.position.map_id,target,plan[0],plan[1],reason,self.w.turn,mode,guide.id if guide else None,known_at_start=knowledge)
        self.emit('JourneyStarted',p,target,origin=p.position.map_id,reason=reason,mode=mode,
                  guide_id=guide.id if guide else None,route_ids=plan[0],nodes=plan[1],
                  known_at_start=knowledge,food_owned=self.e.items.count(p.id,'food'),
                  water_owned=self.e.items.count(p.id,'water'),required_food=food,required_water=water,estimated_hours=hours,toll=toll)
        if len(plan[0])>1:self.emit('MultiHopJourney',p,target,route_ids=plan[0],nodes=plan[1])
        if guided:self.emit('EscortJourney' if mode=='escort' else 'FollowJourney',p,target,guide_id=guide.id,route_ids=plan[0])
        if reason=='divine_contact':self.emit('SacredJourney',p,target,route_ids=plan[0])
        return True,'Viagem planejada exclusivamente pelas conexões conhecidas.'

    def step(self, p):
        j=p.journey
        if not j:return False,'Nenhuma viagem em andamento.'
        if j.last_step==self.w.turn:return True,'Etapa desta hora já consumida.'
        if not p.alive or p.health<=15 or p.combat.detention_until>self.w.turn or p.combat.surrendered_until>self.w.turn:
            return False,'Viagem interrompida pela condição do viajante.'
        j.last_step=self.w.turn;p.active_until=max(p.active_until,self.w.turn+6)
        route=self.w.routes[j.route_ids[j.leg]];a,b=j.nodes[j.leg:j.leg+2]
        path=route.path if a==route.origin else list(reversed(route.path))
        if route.condition=='closed':
            self.emit('RouteObstructed',p,b,route_id=route.id);p.journey=None
            for rk in p.route_knowledge.values():
                if rk.route_id==route.id:rk.condition='closed'
            return False,'Estrada encontrada fechada; é preciso outro plano.'
        if j.guide_id:
            guide=self.w.characters.get(j.guide_id)
            certificate=guide.access_state.get('last_journey',{}) if guide else {}
            if not guide or not guide.alive or not (guide.journey and guide.journey.started_at<=j.started_at or certificate.get('destination')==j.destination and certificate.get('completed_at',-1)>=j.started_at):
                return False,'Guia perdido; conhecimento não foi concedido.'
            if guide.position==p.position and p.position.map_id!=b:return True,'Aguardar o guia avançar.'
            if guide.journey and (j.leg>guide.journey.leg or j.leg==guide.journey.leg and j.offset>=guide.journey.offset and p.position.map_id==self.w.world_map_id):
                return True,'Aguardar a etapa física do guia.'
        if p.position.map_id==a:
            grid=self.w.maps[a];gate=Location(a,grid.width//2,grid.height-1)
            if p.position==gate:self.e.navigation.leave(p)
            else:self.e.navigation.approach(p,gate,1)
            return True,'Caminhada até a saída da localidade.'
        if p.position.map_id==self.w.world_map_id:
            speed=max(1,math.ceil(route.distance/max(1,route.travel_time))-(1 if p.combat.injured>=20 else 0))
            limit=len(path)-1
            if j.guide_id and guide.journey and guide.journey.leg==j.leg:limit=min(limit,guide.journey.offset)
            j.offset=min(limit,j.offset+speed)
            self.e.navigation.relocate(p,path[j.offset])
            p.fatigue=min(100,p.fatigue+.5)
            if j.offset==len(path)-1:
                self.e.navigation.enter(p)
            return True,'Trecho da estrada percorrido fisicamente.'
        if p.position.map_id!=b:return False,'Viajante fora do trecho planejado.'
        route.uses+=1
        for origin in (a,b):self.learn(p,route,origin,'traveled',100)
        for rk in p.route_knowledge.values():
            if rk.route_id==route.id:rk.last_used_at=self.w.turn
        self.know_place(p,b,'arrival',state='VISITED')
        self.emit('RouteTraversed',p,b,route_id=route.id,origin=a,mode=j.mode,source=j.known_at_start[j.leg]['source'])
        self.visit(p,b)
        j.leg+=1;j.offset=0
        if j.leg>=len(j.route_ids):
            self.emit('JourneyArrived',p,j.destination,origin=j.origin,reason=j.reason,mode=j.mode,route_ids=j.route_ids,duration=self.w.turn-j.started_at)
            p.access_state['last_journey']={'destination':j.destination,'origin':j.origin,'completed_at':self.w.turn,'route_ids':list(j.route_ids)}
            p.journey=None
        return True,'Chegada ao destino ou à conexão intermediária.'

    def visit(self,p,id):
        point=self.w.points.get(id)
        if not point:return
        before=p.access_state.get(f'visited:{id}')
        if before is None:
            self.emit('POIDiscovered',p,id,place_id=id,kind=point.kind)
            self.emit('POIVisited',p,id,place_id=id,kind=point.kind)
        p.access_state[f'visited:{id}']=self.w.turn

    def travel(self,p,target,reason):
        if p.position.map_id==target and not p.journey:return True,'Destino já alcançado.'
        if not p.journey:
            success,message=self.begin(p,target,reason)
            if not success:return success,message
        return self.step(p)

    def audit(self):
        errors=[]
        for e in self.w.history:
            if e.kind!='JourneyStarted':continue
            c=e.context
            if c['mode']=='known_route':
                for a,b,rid,rk in zip(c['nodes'],c['nodes'][1:],c['route_ids'],c['known_at_start']):
                    if rk['actor']!=e.actor_id or rk['origin']!=a or rk['destination']!=b or rk['route_id']!=rid or rk['confidence']<60 or rk['learned_at']>e.turn:
                        errors.append(f'Viagem {e.id} usou conexão desconhecida.')
            elif c['mode'] not in ('follow_person','escort','exploration'):errors.append(f'Modo de viagem inválido: {e.id}')
            if c['food_owned']<c['required_food'] or c['water_owned']<c['required_water']:errors.append(f'Viagem {e.id} partiu sem reservas.')
        return errors
