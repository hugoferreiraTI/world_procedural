"""Soluções e execução de interação. Decisão pertence a Need/Goal/Utility."""
import hashlib

from .models import Location, Observation
from .navigation import distance, passable
from .needs import FINISHED
from .rules import INTERACTION

ACTIONS = {'attack','defend','flee','surrender','intervene','protect','confront','threaten',
           'demand_return','warn','insult','apologize','withdraw','call_help','alert','calm',
           'forgive','first_aid','seek_treatment','pursue','capture','steal_person','return_stolen','self_harm','spare','watch_case'}
SOCIAL_ONCE = {'confront','threaten','demand_return','warn','insult','call_help','alert','calm'}


class ConflictSystem:
    def __init__(self, engine):
        self.engine,self.world=engine,engine.world

    def weapon(self, person):
        weapons=[self.world.items[i] for i in person.inventory if self.world.items[i].kind=='weapon']
        return max(weapons,key=lambda w:w.damage*(.5+w.quality/200)) if weapons else None

    def power(self, person):
        weapon=self.weapon(person)
        bonus=min(INTERACTION.maximum_weapon_bonus,weapon.damage*(.5+weapon.quality/200)) if weapon else 0
        return (INTERACTION.unarmed_damage+bonus)*(.5+person.health/200)*(1-person.combat.injured/250)

    def observe(self, person):
        for i in self.engine.spatial.at(person.position):
            if i==person.id:continue
            target=self.world.characters[i]
            weapon=self.weapon(target)
            # Aparência aproximada, sem revelar qualidade/exata força física.
            visible=4 if not weapon else 10 if weapon.damage<15 else 15
            person.observations[i]=Observation(self.world.turn,target.position,target.hunger,target.thirst,
                target.health,target.alive,target.profession,visible,int(target.combat.injured))
        while len(person.observations)>64:del person.observations[next(iter(person.observations))]

    def on_fact(self, person, fact):
        if fact.confidence<30:return
        if fact.kind in ('ImmediateHelpRequested','ThirdPartyAlerted') and fact.target_id==person.id:
            if fact.actor_id!=person.id:
                need=self.engine.needs.ensure(person,f'assistance:{fact.actor_id}',60,f'event:{fact.event_id}',
                    'Avaliar pedido imediato de auxílio conhecido',fact.actor_id)
                need.context.update(source_event=fact.event_id)
                need.expires_at=self.world.turn+12
                person.active_until=max(person.active_until,self.world.turn+6)
            return
        if fact.kind in ('CharacterAttacked','CharacterThreatened','CharacterInsulted','CharacterConfronted','RestitutionDemanded'):
            if fact.actor_id in (None,person.id):return
            victim=fact.target_id
            kin=self.engine.needs.personal.kin.get(person.id,())
            friend=self.engine.graph.value(person.id,victim,'amizade') if victim else 0
            direct=victim==person.id
            protect=victim in kin or friend>=45 or person.profession=='guarda'
            if not direct and not protect:return
            kind='response' if direct else 'protection'
            key=f'{kind}:{fact.actor_id if direct else victim}'
            severity=75 if fact.kind=='CharacterAttacked' else 50
            need=self.engine.needs.ensure(person,key,severity,f'event:{fact.event_id}',
                'Responder a agressão/pressão conhecida' if direct else 'Proteger pessoa diante de conflito conhecido',
                fact.actor_id if direct else victim)
            need.context.update(source_event=fact.event_id,threat=fact.actor_id,victim=victim,
                protected=victim,known_location=vars(fact.location) if fact.location else None,
                fact_kind=fact.kind,last_hostility=fact.turn)
            if fact.kind=='RestitutionDemanded':need.context['stolen_fact']=fact.context.get('source_fact')
            need.expires_at=self.world.turn+48
            person.active_until=max(person.active_until,self.world.turn+6)
        elif fact.kind=='WantedIssued' and fact.context.get('suspect_id')==person.id:
            need=self.engine.needs.ensure(person,f'response:{fact.actor_id}',55,f'event:{fact.event_id}',
                'Responder à procura institucional conhecida',fact.actor_id)
            need.context.update(source_event=fact.event_id,threat=fact.actor_id,record_id=fact.context.get('record_id'),
                fact_kind=fact.kind,known_location=vars(fact.location) if fact.location else None)
            need.expires_at=self.world.turn+72
            person.active_until=max(person.active_until,self.world.turn+6)
        elif fact.kind in ('ApologyGiven','RestitutionGiven','ConflictForgiven') and fact.target_id==person.id:
            for need in person.needs.values():
                if need.kind in ('revenge','response','protection') and (
                        need.target_id==fact.actor_id or need.context.get('threat')==fact.actor_id):
                    self.engine.needs.finish(person,need)

    def refresh(self, person):
        self.observe(person)
        self.engine.emotions.update(person)
        state=person.combat
        state.truces={i:t for i,t in state.truces.items() if t>self.world.turn}
        if state.opponents and self.world.turn-state.last_active>INTERACTION.conflict_timeout:
            self.end(person,'timeout')
        if self.extreme_despair(person):
            self.engine.needs.ensure(person,'despair',45,'prolonged_known_losses',
                'Desespero extremo prolongado com isolamento')
        else:self.engine.needs.satisfy(person,'despair')
        if state.injured>=6:
            self.engine.needs.ensure(person,'healing',min(90,40+state.injured*.5),
                'injury','Buscar recuperação de ferimento',person.id)
        else:self.engine.needs.satisfy(person,'healing')
        for need in person.needs.values():
            if need.kind in ('response','assistance') and need.status not in FINISHED:
                if need.kind=='response' and need.target_id in state.truces or need.expires_at is not None and self.world.turn>=need.expires_at:
                    self.engine.needs.finish(person,need,'expired')

    def terms(self, person, target_id):
        observed=person.observations.get(target_id)
        seen_strength=(observed.weapon_power or 6)*(.5+(observed.health or 50)/200) if observed else 8
        ratio=seen_strength/max(1,self.power(person))
        here=self.engine.spatial.at(person.position)
        allies=sum(self.engine.graph.value(person.id,i,'amizade')>=40 for i in here if i not in (person.id,target_id))
        enemies=sum(i in person.combat.opponents for i in here if i!=target_id)
        ratio*=1+enemies*.3
        guards=sum(o.profession=='guarda' and o.turn==self.world.turn and o.position==person.position
                   for o in person.observations.values())
        friendship=max(self.engine.graph.value(person.id,target_id,'amizade'),
                       self.engine.graph.value(person.id,target_id,'casamento')) if target_id else 0
        return {'anger':person.emotions.anger/100,'resentment':person.emotions.resentment/100,
            'desperation':person.emotions.desperation/100,'humiliation':person.emotions.humiliation/100,
            'risk':min(1,ratio/(1+ratio)/(1+allies*.3)),'fear':min(1,max(0,ratio-1)+person.combat.injured/100),
            'authority':min(1,guards*.5),'bond':friendship/100,'injury':person.combat.injured/100,
            'low_health':max(0,(60-person.health)/60),'hungry_target':(observed.hunger or 0)/100 if observed else 0,
            'defensive':float(bool(person.combat.opponents))}

    def candidates(self, person, need):
        choices=[]
        state=person.combat
        if state.detention_until>self.world.turn or state.surrendered_until>self.world.turn:
            return choices
        if need.kind=='despair':
            if self.rare_despair_solution(person):choices.append(('self_harm',None,None))
            choices.append(('seek_treatment',person.home,None))
            return choices
        if need.kind=='assistance':
            if need.target_id in self.engine.spatial.at(person.position):
                patient=self.world.characters[need.target_id]
                if patient.combat.injured>=6 and self.engine.items.count(person.id,'food') and self.engine.items.count(person.id,'water'):
                    choices.append(('first_aid',None,patient.id))
                choices.append(('calm',None,patient.id))
            return choices
        if need.kind=='healing':
            choices.append(('seek_treatment',person.home,None))
            for i in self.engine.spatial.at(person.position):
                if i!=person.id and self.engine.social.can_request(person,self.world.characters[i]):
                    choices.append(('call_help',None,i))
            return choices
        if need.kind in ('food','money','advancement') and (person.personality.honesty<55 or
                self.engine.agency.extreme(person,need)):
            for i in self.engine.spatial.at(person.position)[:8]:
                if i!=person.id and person.observations.get(i) and person.observations[i].profession=='comerciante':
                    choices.append(('steal_person',None,i))
        if need.kind not in ('revenge','protection','response','pursuit','security'):
            return choices
        target_id=(need.context.get('threat') if need.kind=='protection' else need.target_id)
        target_id=target_id or need.context.get('culprit')
        if not target_id or target_id==person.id or target_id not in self.world.characters:
            return choices
        truced=target_id in state.truces
        known=(need.context.get('source_event') in person.knowledge or target_id in state.opponents or
               need.kind=='pursuit' and self.engine.justice.record_for(person,target_id) is not None)
        if not known:return choices
        judgment = self.pending_judgment(person,target_id)
        if judgment and target_id in self.engine.spatial.at(person.position):
            return [('attack',None,target_id),('spare',None,target_id),('withdraw',None,target_id),
                    ('call_help',None,target_id)] + ([('capture',None,target_id)] if
                    person.profession=='guarda' and self.engine.justice.record_for(person,target_id) else [])
        here=self.engine.spatial.at(person.position)
        if target_id not in here:
            observed=person.observations.get(target_id)
            location=observed.position if observed else (Location(**need.context['known_location']) if need.context.get('known_location') else None)
            if location and location.map_id==person.position.map_id and need.context.get('search_attempts',0)<3:
                role=need.context.get('institutional_role','search')
                if role=='watch':choices.append(('watch_case',location,target_id))
                elif role=='inquire':
                    for i in here:
                        if i!=person.id and self.engine.social.can_request(person,self.world.characters[i]):
                            choices.append(('ask_personal_help',None,i))
                    if not choices:choices.append(('pursue',location,target_id))
                else:choices.append(('pursue',location,target_id))
            return choices
        target=self.world.characters[target_id]
        if not target.alive:return choices
        if person.profession=='guarda' and self.engine.justice.record_for(person,target_id) and (
                target.combat.surrendered_until>self.world.turn or target.health<=INTERACTION.incapacity_health):
            choices.append(('capture',None,target_id))
        if truced:return choices
        stolen=person.knowledge.get(need.context.get('stolen_fact'))
        if stolen and stolen.actor_id==person.id and stolen.context.get('item_id') in person.inventory:
            choices.append(('return_stolen',None,target_id))
        evidence=person.knowledge.get(need.context.get('source_event'))
        theft=evidence if evidence and evidence.kind=='ItemStolen' else None
        if evidence and evidence.context.get('source_fact') in person.knowledge:
            candidate=person.knowledge[evidence.context['source_fact']]
            if candidate.kind=='ItemStolen':theft=candidate
        for action in ('confront','threaten','demand_return','warn','insult','call_help','calm'):
            if action=='demand_return' and theft is None:continue
            if action not in need.context.get('social_attempts',{}):choices.append((action,None,target_id))
        choices.extend((a,None,target_id) for a in ('withdraw','flee','defend','forgive','apologize','surrender'))
        if target.combat.detention_until>self.world.turn or target.combat.surrendered_until>self.world.turn:
            if person.profession=='guarda' and self.engine.justice.record_for(person,target_id):
                choices.append(('capture',None,target_id))
        else:
            aggression=(person.emotions.anger>=12 and person.personality.vengefulness>=45 or
                        target_id in state.opponents or need.kind=='pursuit' and need.context.get('severity',0)>=3)
            if aggression and person.health>INTERACTION.incapacity_health:
                choices.append(('attack',None,target_id))
        protected=need.context.get('protected')
        if need.kind=='protection' and protected in here and protected!=person.id:
            choices.extend((a,None,target_id) for a in ('intervene','protect','alert'))
            patient=self.world.characters[protected]
            if patient.combat.injured>=6 and self.engine.items.count(person.id,'water') and self.engine.items.count(person.id,'food'):
                choices.append(('first_aid',None,protected))
        return choices

    def begin(self, actor, target, need):
        new=target.id not in actor.combat.opponents
        for a,b in ((actor,target),(target,actor)):
            if b.id not in a.combat.opponents:a.combat.opponents.append(b.id)
            a.combat.last_active=self.world.turn
            a.active_until=max(a.active_until,self.world.turn+6)
        history=actor.combat.conflict_history.setdefault(target.id,{'started':self.world.turn,'blows':0,'severe':0})
        history['blows']+=1
        if target.health<=30:history['severe']+=1
        while len(actor.combat.conflict_history)>8:del actor.combat.conflict_history[next(iter(actor.combat.conflict_history))]
        if new:self.engine.recorder.emit('ConflictStarted',f'{actor.name} iniciou confronto físico com {target.name}.',
            actor.id,target.id,actor.position,historical=True,
            context={'source_fact':need.context.get('source_event') if need else None})

    def end(self, person, reason, other=None):
        partners=list(person.combat.opponents)
        if other and other.id not in partners:partners.append(other.id)
        person.combat.opponents.clear();person.combat.protected_by.clear()
        for i in partners:
            person.combat.pending_judgments.pop(i,None)
            person.combat.violence_intents.pop(i,None)
        for i in partners:
            target=self.world.characters.get(i)
            if target:
                if person.id in target.combat.opponents:target.combat.opponents.remove(person.id)
                target.combat.pending_judgments.pop(person.id,None)
                target.combat.violence_intents.pop(person.id,None)
                person.combat.truces[i]=self.world.turn+INTERACTION.truce_hours
                target.combat.truces[person.id]=self.world.turn+INTERACTION.truce_hours
        if partners:self.engine.recorder.emit('ConflictEnded',f'O confronto de {person.name} terminou: {reason}.',
            person.id,other.id if other else None,person.position,historical=True,
            context={'reason':reason,'participants':partners})

    def first_aid(self, helper, patient):
        if (not patient.alive or helper.position!=patient.position or patient.combat.injured<6 or
                not self.engine.items.count(helper.id,'food') or not self.engine.items.count(helper.id,'water')):
            return False,'Faltam paciente presente, provisões ou água para atendimento.'
        self.engine.items.consume(helper.id,'water');self.engine.items.consume(helper.id,'food')
        patient.combat.injured=max(0,patient.combat.injured-6)
        self.engine.recovery.recover_hp(patient, treatment=2)
        self.engine.recorder.emit('FirstAidGiven',f'{helper.name} prestou auxílio inicial a {patient.name}.',
            helper.id,patient.id,helper.position,context={'injury_after':patient.combat.injured,'food_used':1,'water_used':1})
        return True,'Atendimento limitado realizado com provisões reais.'

    def execute(self, person, goal, need=None):
        action=goal.action;target=self.world.characters.get(goal.target_id)
        if not person.alive:return False,'Um morto não pode agir.'
        if person.combat.detention_until>self.world.turn:return False,'A detenção ainda restringe esta ação.'
        if action=='seek_treatment':
            if person.position!=person.home:return False,'O local seguro ainda não foi alcançado.'
            self.engine.needs.rest(person,1)
            if max(person.hunger,person.thirst)<80:person.combat.injured=max(0,person.combat.injured-2)
            return True,'Descanso de recuperação realizado; ferimento não some instantaneamente.'
        if action=='first_aid':return self.first_aid(person,target) if target else (False,'Paciente inexistente.')
        if action=='self_harm':
            if not self.extreme_despair(person):return False,'A condição extrema não permanece.'
            self.engine.finish_death(person,'self_harm')
            return True,'Morte de causa autoinfligida abstrata registrada.'
        if action=='watch_case':
            self.observe(person)
            if target and target.id in self.engine.spatial.at(person.position):
                self.engine.recorder.emit('SuspectLocated',f'{person.name} encontrou o suspeito durante vigilância.',
                    person.id,target.id,person.position,context={'source_fact':need.context.get('source_event') if need else None})
            return True,'Vigilância local realizada sem consultar localização remota.'
        if action=='pursue':
            if not need:return False,'Falta objetivo baseado em conhecimento.'
            if target and target.id in self.engine.spatial.at(person.position) and target.alive:
                self.observe(person);need.context['search_attempts']=0
                self.engine.recorder.emit('SuspectLocated',f'{person.name} encontrou a pessoa procurada.',
                    person.id,target.id,person.position,context={'source_fact':need.context.get('source_event')})
                return True,'Pessoa localizada fisicamente.'
            need.context['search_attempts']=need.context.get('search_attempts',0)+1
            self.engine.recorder.emit('PursuitSearch',f'{person.name} verificou a última localização conhecida sem encontrar o alvo.',
                person.id,location=person.position,witnesses=[person.id],context={'target_id':goal.target_id,
                'source_fact':need.context.get('source_event'),'attempt':need.context['search_attempts']})
            return True,'Busca local sem encontro; não consulta posição remota.'
        if action in ('flee','withdraw','surrender','defend'):
            if action=='defend':
                person.combat.defending_until=self.world.turn+2
                self.engine.recorder.emit('CharacterDefended',f'{person.name} adotou defesa.',person.id,location=person.position)
                return True,'Defesa temporária adotada.'
            if action=='surrender':
                person.combat.surrendered_until=self.world.turn+12
                self.end(person,'surrender',target)
                self.engine.recorder.emit('CharacterSurrendered',f'{person.name} rendeu-se.',person.id,
                    target.id if target and target.position==person.position else None,person.position,historical=True)
                return True,'Rendição registrada; não implica morte.'
            old=person.position
            peers=self.engine.spatial.at(old)
            safe=person.home if person.home!=old and person.home.map_id==old.map_id else person.known_places.get('forage')
            if not safe or safe==old:
                safe=next((Location(old.map_id,old.x+dx,old.y+dy) for dx,dy in ((0,1),(0,-1),(1,0),(-1,0))
                           if passable(self.world,Location(old.map_id,old.x+dx,old.y+dy))),None)
            if not safe:return False,'Não existe passagem de fuga conhecida.'
            chance=max(.15,min(.95,.7+person.health/500-person.combat.injured/150))
            if action=='flee' and self.engine.rng.random()>chance:
                self.engine.recorder.emit('EscapeFailed',f'{person.name} não conseguiu afastar-se nesta hora.',person.id,location=old)
                return True,'A tentativa de fuga consumiu esta hora, mas não houve afastamento.'
            self.engine.navigation.approach(person,safe,1)
            if person.position==old:return False,'A passagem permanece bloqueada.'
            self.end(person,'flee' if action=='flee' else 'withdraw',target)
            self.engine.recorder.emit('CharacterFled' if action=='flee' else 'CharacterWithdrew',
                f'{person.name} afastou-se do confronto.',person.id,location=old,witnesses=peers,
                context={'new_location':vars(person.position)},historical=True)
            if need:self.engine.needs.finish(person,need)
            return True,'Afastamento físico realizado; o conflito social pode continuar.'
        if not target or not target.alive or target.id==person.id or target.position!=person.position:
            return False,'O interlocutor/alvo vivo não está nesta posição.'
        if action=='spare':
            if not self.pending_judgment(person,target.id):return False,'Não há decisão pendente diante de incapacidade.'
            self.engine.recorder.emit('IncapacitatedSpared',f'{person.name} poupou {target.name} após incapacidade.',
                person.id,target.id,person.position,historical=True,context={'source_fact':need.context.get('source_event') if need else None})
            self.end(person,'spared',target)
            if need:self.engine.needs.finish(person,need)
            return True,'A intenção foi abandonada diante do alvo incapacitado.'
        if action=='capture':return self.engine.justice.capture(person,target)
        if action=='steal_person':
            item_id=self.engine.items.first(target.id,'food')
            if item_id is None:return False,'Não havia provisão acessível no alvo.'
            moved=self.engine.items.transfer(target.id,person.id,item_id)
            self.engine.recorder.emit('ItemStolen',f'{person.name} roubou provisão de {target.name}.',person.id,target.id,
                person.position,context={'item_id':moved.id,'item_kind':'food'})
            return True,'Provisão real roubada.'
        if action=='attack':
            judgment = self.pending_judgment(person,target.id)
            if (person.combat.surrendered_until>self.world.turn or target.combat.surrendered_until>self.world.turn and not judgment or
                    target.combat.detention_until>self.world.turn or person.combat.truces.get(target.id,0)>self.world.turn):
                return False,'Rendição, detenção ou trégua impede continuar o ataque.'
            intended=target.id
            for i in target.combat.protected_by:
                defender=self.world.characters.get(i)
                if (defender and defender.id!=person.id and defender.alive and defender.position==target.position
                        and defender.combat.defending_until>self.world.turn
                        and defender.combat.surrendered_until<=self.world.turn
                        and defender.combat.detention_until<=self.world.turn):
                    target=defender;break
            intent=self.intent(person,target,need)
            if judgment and intent!='kill':return False,'A reavaliação não sustenta intenção letal.'
            self.begin(person,target,need)
            weapon=self.weapon(person)
            damage=max(1,round(self.power(person)+self.engine.rng.randint(-INTERACTION.damage_variation,INTERACTION.damage_variation)))
            if target.combat.defending_until>self.world.turn:damage=max(1,round(damage*INTERACTION.defense_multiplier))
            self.engine.recovery.damage(target, damage, 'combat')
            target.combat.injured=min(100,target.combat.injured+damage)
            record=self.engine.justice.record_for(person,target.id)
            lawful=bool(record and record.known_severity.get(person.id,1)>=3 and person.profession=='guarda')
            self_defense=any(f.kind=='CharacterAttacked' and f.actor_id==target.id and f.target_id==person.id
                and self.world.turn-f.turn<=12 for f in person.knowledge.values())
            context={'damage':damage,'weapon_id':weapon.id if weapon else None,'intended_target':intended,
                'source_fact':need.context.get('source_event') if need else None,'lawful':lawful,'self_defense':self_defense,
                'violence_intent':intent,'post_incapacity':judgment}
            self.world.metrics['AttackExecuted']=self.world.metrics.get('AttackExecuted',0)+1
            if target.health<=0:
                self.engine.finish_death(target,'combat',person,weapon.id if weapon else None,context)
                self.end(target,'death',person)
            else:
                self.engine.recorder.emit('CharacterAttacked',f'{person.name} feriu {target.name} em {damage} HP.',
                    person.id,target.id,person.position,historical=True,context=context)
                if target.health<=INTERACTION.incapacity_health:
                    target.combat.surrendered_until=self.world.turn+6
                    self.engine.recorder.emit('CharacterIncapacitated',f'{target.name} ficou incapacitado.',
                        person.id,target.id,person.position,historical=True,context=context)
                    if intent=='kill':
                        person.combat.pending_judgments[target.id]=self.world.turn+6
                        if need:need.context['pending_judgment']=True
                    else:self.end(target,'incapacity',person)
            return True,f'Ataque causou {damage} de dano real.'
        if action in ('intervene','protect'):
            protected_id=need.context.get('protected') if need else None
            protected=self.world.characters.get(protected_id)
            if not protected or protected.position!=person.position or not protected.alive:
                return False,'O protegido não está presente.'
            person.combat.defending_until=self.world.turn+3
            if person.id not in protected.combat.protected_by:protected.combat.protected_by.append(person.id)
            self.engine.recorder.emit('ProtectionGiven',f'{person.name} interveio para proteger {protected.name}.',
                person.id,protected.id,person.position,context={'aggressor_id':target.id,'physical':True,
                'source_fact':need.context.get('source_event')})
            return True,'Intervenção física temporária adotada.'
        if action=='return_stolen':
            fact=person.knowledge.get(need.context.get('stolen_fact')) if need else None
            item_id=fact.context.get('item_id') if fact else None
            if fact and fact.actor_id==person.id and item_id in person.inventory:
                owner=fact.target_id
                if owner not in self.world.characters and owner not in self.world.towns:owner=person.id
                if owner==person.id:return False,'O bem não possui destinatário de restituição válido.'
                self.engine.items.transfer(person.id,owner,item_id,1)
                self.engine.recorder.emit('RestitutionGiven',f'{person.name} devolveu uma provisão rastreável.',person.id,
                    target.id,person.position,context={'source_fact':fact.event_id,'item_id':item_id,'owner_id':owner,'quantity':1})
                self.end(person,'restitution',target)
                return True,'Restituição material real realizada.'
            return False,'A provisão rastreável já não está com o autor.'
        if action in SOCIAL_ONCE and need:
            if action in need.context.get('social_attempts',{}):return False,'Essa abordagem já foi feita neste episódio.'
            need.context.setdefault('social_attempts',{})[action]=self.world.turn
        kinds={'confront':'CharacterConfronted','threaten':'CharacterThreatened','demand_return':'RestitutionDemanded',
            'warn':'CharacterWarned','insult':'CharacterInsulted','apologize':'ApologyGiven','call_help':'ImmediateHelpRequested',
            'alert':'ThirdPartyAlerted','calm':'CalmingAttempted','forgive':'ConflictForgiven'}
        kind=kinds.get(action)
        if kind:
            context={'source_fact':need.context.get('source_event') if need else None}
            record=self.engine.justice.record_for(person,target.id)
            if record:context.update(record_id=record.id,lawful=True)
            self.engine.recorder.emit(kind,f'{person.name}: {action} diante de {target.name}.',person.id,target.id,
                person.position,context=context)
            if action in ('apologize','forgive'):
                self.engine.emotions.repair(target,person.id)
                self.end(person,action,target)
                if need:self.engine.needs.finish(person,need)
            elif action=='calm':
                self.engine.emotions.support(target,8)
                if need and need.kind=='assistance':self.engine.needs.finish(person,need)
            return True,'Interação estruturada registrada: '+action+'.'
        return False,'Ação de interação indisponível.'

    def extreme_despair(self, person):
        state=person.emotions
        support=any(o.alive and self.world.turn-o.turn<=168 and
                    self.engine.graph.value(person.id,i,'amizade')>=40 for i,o in person.observations.items())
        return (state.desperation>=98 and len(state.losses)>=3 and self.world.turn>=720 and
                self.world.turn-state.last_support>336 and not support and not person.combat.opponents)

    def rare_despair_solution(self, person):
        if not self.extreme_despair(person):return False
        key=f'{self.world.seed}:{person.id}:{self.world.turn//24}:despair'.encode()
        return int.from_bytes(hashlib.sha256(key).digest()[:4],'big')%4096==0

    def pending_judgment(self, person, target_id):
        until=person.combat.pending_judgments.get(target_id,-1)
        observed=person.observations.get(target_id)
        return (until>self.world.turn and observed is not None and observed.alive
                and observed.health is not None and observed.health<=INTERACTION.incapacity_health
                and person.combat.violence_intents.get(target_id)=='kill')

    def intent_scores(self, person, target, need):
        p=person.personality;terms=self.terms(person,target.id)
        grievance=person.grievances.get(target.id)
        harm=grievance.intensity if grievance else 0
        fact=person.knowledge.get(need.context.get('source_event')) if need else None
        serious=30 if fact and fact.kind=='CharacterKilled' else 8 if fact and fact.kind=='CharacterAttacked' else 0
        c=self.engine.agency.current(person,need) if need else None
        commitment=c.intensity*.2 if c else 0
        history=person.combat.conflict_history.get(target.id,{})
        guard=person.profession=='guarda' and self.engine.justice.record_for(person,target.id) is not None
        return {'repel':20+p.compassion*.2+terms['risk']*20,
                'contain':25+p.honesty*.15+p.compassion*.15,
                'subdue':20+(40 if guard else 0)+p.honesty*.1,
                'hurt':15+p.vengefulness*.2+person.emotions.anger*.2-p.compassion*.2,
                'kill':-75+harm*.5+person.emotions.anger*.25+p.vengefulness*.3+p.persistence*.1
                    -p.compassion*.65-terms['risk']*25-terms['authority']*40-terms['bond']*40
                    +serious+commitment+min(10,history.get('severe',0)*2)-(35 if guard else 0)}

    def intent(self, person, target, need):
        scores=self.intent_scores(person,target,need)
        selected=max(scores,key=lambda k:(scores[k],k))
        previous=person.combat.violence_intents.get(target.id)
        if previous!=selected:
            person.combat.violence_intents[target.id]=selected
            self.engine.recorder.emit('ViolenceIntentChanged',f'{person.name} reavaliou a intenção do confronto.',
                person.id,target.id,person.position,historical=True,
                context={'previous':previous,'intent':selected,'scores':scores,
                         'source_fact':need.context.get('source_event') if need else None})
        while len(person.combat.violence_intents)>8:
            old=next(iter(person.combat.violence_intents));person.combat.violence_intents.pop(old)
            person.combat.pending_judgments.pop(old,None)
        return selected
