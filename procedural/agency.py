"""Intenção persistente: informa Need/Utility, nunca executa ações."""
from dataclasses import replace
from .models import Aspiration, Commitment, Location
from .needs import FINISHED
from .navigation import distance
from .rules import AGENCY, RECOVERY

LONG_KINDS = {'revenge','protection','family','grief','pursuit','migration','status','advancement','response',
              'power','political_pressure','organizational_survival','religious_interest'}
LIVE = {'active','paused','waiting_for_information'}


def clamp(x):
    return max(0., min(100., x))


class AgencySystem:
    def __init__(self, engine):
        self.e, self.w = engine, engine.world

    def event(self, person, kind, commitment=None, **context):
        if commitment:
            context.update(commitment_id=commitment.id,need_id=commitment.originating_need,
                origin=commitment.motivation,source_fact=commitment.originating_fact,
                target=commitment.target_id,progress=commitment.progress)
        return self.e.recorder.emit(kind,f'{person.name}: {kind}.',person.id,
            location=person.position,witnesses=[person.id],historical=True,context=context)

    @staticmethod
    def identity(need):
        return (need.kind,need.target_id,need.context.get("record_id"),need.context.get("victim"),
                need.context.get("threat"),need.context.get("mode"),need.context.get("reason"))

    def current(self, person, need):
        return next((c for c in person.commitments.values()
                     if c.originating_need==need.id and c.status in LIVE),None)

    def pinned(self, person):
        pins=set()
        for c in person.commitments.values():
            if c.status not in LIVE:continue
            if c.originating_fact is not None:pins.add(c.originating_fact)
            pins.update(c.context.get('supporting_facts',[]))
        for d in person.lethal_decisions.values():
            if d.status=='active':pins.update(d.facts)
        return pins

    def pressure(self, person, need):
        history=need.context.get('unresolved',{})
        elapsed=max(0,self.w.turn-need.created_at)
        return min(1,elapsed/168+history.get('failures',0)/8+history.get('blocks',0)/16)

    def profile(self, person, need, choices=None):
        """Somente sinais próprios, encontros, lugares e notícias conhecidos."""
        p=person.personality;target=need.context.get('threat',need.target_id) if need.kind=='protection' else need.target_id
        observed=person.observations.get(target)
        location=observed.position if observed else None
        if location is None and need.context.get('known_location'):
            location=Location(**need.context['known_location'])
        risk=fear=0.;travel=0
        if need.kind in ('revenge','response','protection','pursuit') and target is not None:
            t=self.e.conflicts.terms(person,target);risk=t['risk'];fear=t['fear']
        if location:
            travel=min(1,distance(person.position,location)/40)
        uncertainty=.6 if need.kind in ('revenge','family','pursuit') and target not in person.observations else .1
        if location and location.map_id!=person.position.map_id:
            uncertainty=.35 if location.map_id in person.known_towns else 1.
        resources=min(1,(person.money/20+self.e.items.count(person.id,'food')/2)/2)
        conventional=bool(person.known_places or observed or person.known_towns)
        opportunities=(min(1,len(choices)/4) if choices is not None else float(conventional))
        history=need.context.get('unresolved',{})
        experience=max(-1,min(1,(history.get('progress',0)-history.get('failures',0))/8))
        agency=clamp(15+25*opportunities+20*resources+25*person.health/100+10*experience
                     +p.courage*.1-20*risk-20*uncertainty-10*travel)/100
        compatible=(p.vengefulness if need.kind in ('revenge','response') else p.family_loyalty if need.kind in ('family','grief','protection')
                    else p.diligence if need.kind=='pursuit' else p.ambition if need.kind in ('status','advancement') else p.independence)/100
        c=self.current(person,need);duration=self.pressure(person,need)
        emotion=(person.emotions.anger+person.emotions.resentment)/200 if need.kind in ('revenge','response','protection') else person.emotions.desperation/100
        importance=need.context.get('relationship',0)/100
        origin=person.knowledge.get(need.context.get('source_event'))
        known_severity={'CharacterKilled':5,'CharacterAttacked':3,'CharacterThreatened':2,'ItemStolen':1}.get(origin.kind,0) if origin else 0
        severity=max(need.context.get('severity',0),known_severity)/5
        urgent=need.base_urgency/100
        competing=max(person.hunger,person.thirst)/100 if need.kind not in ('food','water') else 0
        aspiration=next((a for a in person.aspirations if a.status=='active' and a.domain==need.context.get('aspiration_domain')),None)
        drive=aspiration.intensity*AGENCY.aspiration_drive_weight if aspiration else 0
        impulse=clamp(drive+28*urgent+18*duration+15*emotion+16*compatible+10*importance+10*severity
                      +18*agency+(10*c.intensity/100 if c else 0)-12*fear-12*risk
                      -10*(1-person.health/100)-8*travel-8*uncertainty-12*competing)
        if person.mythic_trait and need.kind in ('power','protection','revenge','political_pressure'):
            impulse=clamp(impulse+12)
        return {'impulse':impulse,'perceived_agency':agency,'unresolved_pressure':duration,
                'risk':risk,'uncertainty':uncertainty,'opportunity':opportunities,'aspiration_drive':drive}

    def extreme(self, person, need):
        if need.kind not in ('food','water'):return False
        return bool(need.context.get('emergency') and self.pressure(person,need)>.25
                    and self.profile(person,need)['perceived_agency']>.15)

    def adopt(self, person, need, force=False):
        previous=self.current(person,need)
        if previous:return previous
        if person.is_player or need.kind not in LONG_KINDS:return None
        if need.kind=='response' and not self.e.lethality.sustained_response(person,need):return None
        profile=self.profile(person,need)
        if not force and profile['impulse']<AGENCY.adoption_pressure:return None
        source=need.context.get('source_event')
        if source is not None and source not in person.knowledge:return None
        if source is None and not (need.kind in ('advancement','status','migration','power','political_pressure','organizational_survival','religious_interest') or need.source.startswith('encounter:')):
            return None
        for cid,c in list(person.commitments.items()):
            if c.status not in LIVE:del person.commitments[cid]
        if len(person.commitments)>=AGENCY.maximum_commitments:return None
        c=Commitment(self.w.allocate_id(),person.id,need.id,source,need.target_id,need.kind,
            clamp(profile['impulse']),self.w.turn,self.w.turn,
            context={'need_key':next(k for k,n in person.needs.items() if n is need),
                     'confidence':person.knowledge[source].confidence if source in person.knowledge else need.context.get('confidence',100),'source':need.source,
                     'initial_urgency':need.base_urgency,'cause_identity':self.identity(need),
                     'current_source':need.source})
        if need.kind=='response':
            grievance=person.grievances.get(need.target_id)
            if grievance:c.intensity=max(c.intensity,grievance.intensity*c.context['confidence']/100)
        person.commitments[c.id]=c
        self.event(person,'CommitmentCreated',c,impulse=profile['impulse'],agency=profile['perceived_agency'])
        return c

    def close(self, person, c, status, reason):
        if c.status not in LIVE:return
        c.status=status;c.context['ending_reason']=reason;c.context['ended_at']=self.w.turn
        self.event(person,{'satisfied':'CommitmentCompleted','abandoned':'CommitmentAbandoned',
                          'expired':'CommitmentExpired'}[status],c,reason=reason,
                          duration=self.w.turn-c.created_at,activity=c.activity_count,
                          meaningful_progress=c.meaningful_progress,strategy_changes=c.strategy_changes)

    def aspirations(self, person):
        if person.is_player:return
        if not person.aspirations:
            p=person.personality
            domains={'wealth':p.greed*.6+p.ambition*.4+(10 if person.money<20 else 0),
                     'competence':p.diligence*.6+p.ambition*.4+(10 if person.training_target else 0),
                     'recognition':p.ambition*.7+p.temperament*.15+p.compassion*.15,
                     'family':p.family_loyalty*.65+p.compassion*.35 if self.e.needs.personal.kin.get(person.id) else -1}
            domain=max(domains,key=lambda k:(domains[k],k))
            a=Aspiration(domain,clamp(20+p.ambition*.55+domains[domain]*.2),self.w.turn,
                context={'initial_money':person.money,'money_target':person.money+15+p.ambition//5,
                         'initial_profession':person.profession,'recognition_target':3,
                         'last_offered':-1000,'reason':'personality_and_personal_state'})
            person.aspirations.append(a);self.event(person,'AspirationAdopted',domain=domain,intensity=a.intensity)
        for a in person.aspirations:
            if a.status!='active':continue
            if a.domain=='seek_violent_opportunity':
                if not self.e.lethal_decisions.seeking(person):a.status='abandoned'
                continue
            if a.domain=='become_stronger':
                a.progress=min(1,person.mythic_development/75)
                # A necessidade e as oportunidades de treino pertencem ao serviço de fé/potencial.
                if a.progress>=1:
                    a.status='satisfied';self.event(person,'AspirationSatisfied',domain=a.domain,progress=a.progress)
                continue
            if a.domain=='wealth':
                delta=max(0,person.money-a.context['initial_money'])
                a.progress=min(1,delta/max(1,a.context['money_target']-a.context['initial_money']))
            elif a.domain=='competence':
                a.progress=1. if person.profession!=a.context['initial_profession'] else min(.9,person.training_progress/max(1,person.training_required))
            elif a.domain=='recognition':a.progress=min(1,person.agency_state.get('recognition',0)/a.context['recognition_target'])
            if a.domain=='competence' and self.w.turn-a.created_at>AGENCY.maximum_duration and not person.training_target and not a.progress:
                a.status='abandoned';self.event(person,'AspirationAbandoned',domain=a.domain,reason='no_known_training_opportunity');continue
            if a.progress>=1:
                a.status='satisfied';self.event(person,'AspirationSatisfied',domain=a.domain,progress=a.progress)
                for n in person.needs.values():
                    if n.context.get('aspiration_domain')==a.domain and n.status not in FINISHED:self.e.needs.finish(person,n)
                continue
            if person.health<RECOVERY.target_hp or max(person.hunger,person.thirst)>=80:continue
            if self.w.turn-a.context['last_offered']<AGENCY.aspiration_return_hours:continue
            # Todas as oportunidades são próprias/conhecidas; não procura oferta remota.
            fresh=person.market_observation.get('town_id')==person.town_id and self.w.turn-person.market_observation.get('turn',-1000)<=24
            if a.domain=='family':
                n=next((n for n in person.needs.values() if n.kind=='family' and n.status not in FINISHED),None)
                if n:n.context['aspiration_domain']='family'
                continue
            kind='status' if a.domain=='recognition' else 'advancement'
            if a.domain=='competence' and not (person.training_target or fresh and person.market_observation.get('training_offer')):continue
            if a.domain=='wealth' and person.profession in (None,'estudante') and not self.e.personal_actions.available_surplus(person):continue
            key=kind if a.domain in ('wealth','recognition') else kind+':aspiration:'+a.domain
            current=person.needs.get(key)
            if current and current.status not in FINISHED:
                current.base_urgency=max(current.base_urgency,12+a.intensity*.18)
                if not current.context.get('aspiration_domain'):
                    current.context['aspiration_domain']=a.domain
                    if a.domain=='wealth':current.context['money_target']=max(current.context.get('money_target',0),a.context['money_target'])
                    if a.domain=='recognition':current.context.update(deeds=0,deeds_target=3)
                a.context['last_offered']=self.w.turn
                continue
            n=self.e.needs.ensure(person,key,12+a.intensity*.18,'aspiration:'+a.domain,
                'Melhorar condição pessoal por oportunidade conhecida')
            n.expires_at=self.w.turn+240
            n.context.update(aspiration_domain=a.domain,domain=a.domain,deeds=0,deeds_target=3)
            if a.domain=='wealth':n.context['money_target']=a.context['money_target']
            a.context['last_offered']=self.w.turn

    def refresh(self, person):
        now=self.w.turn
        self.aspirations(person)
        for c in list(person.commitments.values()):
            if c.status not in LIVE:continue
            n=next((n for n in person.needs.values() if n.id==c.originating_need),None)
            if not n:
                self.close(person,c,'abandoned','need_missing');continue
            if n.kind=='pursuit':
                record=self.w.wanted_records.get(n.context.get('record_id'))
                known_status=record.known_status.get(person.id) if record else None
                if known_status in ('captured','resolved','dead'):
                    self.e.needs.finish(person,n)
                    self.close(person,c,'satisfied','known_institutional_case_closed');continue
                if (known_status!='active' or
                        now>record.created_at+self.e.justice.duration(record,person.id)):
                    self.e.needs.finish(person,n,'expired')
                    self.close(person,c,'expired','known_evidence_expired');continue
            if c.status=='waiting_for_information' and n.status in ('satisfied','failed','inactive'):
                self.close(person,c,'satisfied' if n.status=='satisfied' else 'abandoned','known_resolution_while_waiting');continue
            if c.status=='waiting_for_information' and self.identity(n)!=tuple(c.context.get('cause_identity',())):
                self.close(person,c,'abandoned','cause_replaced');continue
            if c.status=='waiting_for_information':
                if now-c.created_at>=AGENCY.maximum_duration+person.personality.persistence*3:
                    self.close(person,c,'expired','finite_intention_horizon')
                    self.e.needs.finish(person,n,'expired')
                else:n.status='waiting_for_information'
                continue
            if n.source!=c.context.get('current_source',c.context['source']):
                if self.identity(n)!=tuple(c.context.get('cause_identity',())):
                    self.close(person,c,'abandoned','cause_replaced');continue
                source=n.context.get('source_event')
                if source is not None and source in person.knowledge:
                    supporting=c.context.setdefault('supporting_facts',[])
                    if source not in supporting:supporting.append(source);del supporting[:-3]
                c.context['current_source']=n.source;c.last_progress_at=now;c.meaningful_progress+=1
                self.event(person,'CommitmentInformation',c,need_source=n.source,reason='same_intention_new_stage')
            if n.status=='satisfied':
                self.close(person,c,'satisfied',n.context.get('resolution','need_satisfied'));continue
            if n.status in ('failed','inactive'):
                self.close(person,c,'abandoned','need_no_longer_valid');continue
            if self.e.lethal_decisions.active(person,c.target_id):
                n.expires_at=None
                if n.status=='expired':n.status='active'
                continue
            idle=now-c.last_progress_at
            c.abandonment_pressure=clamp(idle/8+c.failures*8+c.setbacks*3-person.personality.persistence*.25-person.personality.ambition*.1)
            tolerance=55+person.personality.persistence*.3
            if c.abandonment_pressure>tolerance:
                self.close(person,c,'abandoned','no_progress_or_lost_agency');
                if n.status not in FINISHED:self.e.needs.finish(person,n,'inactive')
                continue
            if now-c.created_at>=AGENCY.maximum_duration+person.personality.persistence*3:
                self.close(person,c,'expired','finite_intention_horizon');continue
            if n.status=='expired':
                n.status='active';n.expires_at=now+48
                # Não reaprende a notícia: mantém ID, pressão e causalidade.
            elif n.expires_at is not None and n.expires_at<=now+12:n.expires_at=now+48
            if c.target_id!=n.target_id:
                old=c.target_id;c.target_id=n.target_id;c.last_progress_at=now;c.context['cause_identity']=self.identity(n)
                c.meaningful_progress+=1;self.event(person,'CommitmentRetargeted',c,old_target=old)
        for n in list(person.needs.values()):
            if n.status in FINISHED or n.status=='waiting_for_information':continue
            self.adopt(person,n)
            profile=self.profile(person,n);n.context['agency']=profile
        self.e.investigation.refresh(person)

    def priority_modifier(self, person, need):
        if need.kind in ('food','water','rest','recovery','food_reserve','work','money'):return 0
        profile=need.context.get('agency',{})
        return max(0,profile.get('impulse',0)-40)/60*AGENCY.priority_bonus

    def adjust(self, person, need, action, score, terms):
        profile=need.context.get('agency') or self.profile(person,need)
        c=self.current(person,need)
        if c:
            stalled=c.stalled_actions.get(action,0)
            penalty=min(80,stalled*18)
            score-=penalty;terms['no_progress']=-penalty/200
        pressure=profile['unresolved_pressure']*profile['impulse']/100
        # Alivia uma parte do custo moral/risco sob pressão, sem removê-lo.
        if action in ('steal','steal_person'):
            bonus=pressure*person.personality.honesty*.65
            score+=bonus;terms['pressure_moral_tolerance']=bonus/200
        if action=='attack' and self.e.conflicts.pending_judgment(person,need.target_id):
            target=self.w.characters.get(need.target_id)
            if target:
                drive=self.e.conflicts.intent_scores(person,target,need)['kill']
                bonus=max(0,drive)*.7
                score+=bonus;terms['post_incapacity_intent']=bonus/200
        if action in ('attack','pursue','threaten','migrate'):
            bonus=pressure*profile['perceived_agency']*20
            score+=bonus;terms['pressure_risk_tolerance']=bonus/200
        reputation=person.reputations.get(need.target_id)
        if reputation and action in ('attack','flee','withdraw','forgive','ask_personal_help'):
            fear=reputation.fear/100
            delta=fear*(12 if action in ('flee','withdraw') else -12)
            score+=delta;terms['known_reputation']=delta/200
        target=need.context.get('threat') if need.kind=='protection' else need.target_id
        d=self.e.lethal_decisions.active(person,target)
        if d and action in ('attack','pursue','confront','follow_lead','search_area','ask_about_person'):
            bonus=20+d.intensity*.25+d.rumination*.15
            score+=bonus;terms['lethal_continuity']=bonus/200
        if d and action in ('finish','spare','capture','first_aid','withdraw') and target in self.e.spatial.at(person.position):
            terminal=self.e.lethal_decisions.terminal(person,self.w.characters[target])
            if self.w.characters[target].health<=12:
                bonus=terminal['scores'].get('help' if action=='first_aid' else action,0)
                score+=bonus;terms['terminal_context']=bonus/200
        prep=person.commitments.get(need.context.get('preparing_commitment'))
        if prep and prep.status in ('active','paused') and action in ('buy_food','forage','work','sleep','drink_well'):
            bonus=4.;score+=bonus;terms['contextual_preparation']=bonus/200
        return score

    def selected(self, person, active, chosen, action):
        c=self.adopt(person,chosen)
        for other in person.commitments.values():
            if other.status not in LIVE or other.status=='waiting_for_information':continue
            status='active' if other is c else 'paused'
            if other.status!=status:
                other.status=status
                kind='CommitmentResumed' if status=='active' else 'CommitmentPaused'
                if self.w.turn-other.context.get('last_transition_event',-1000)>=6:
                    self.event(person,kind,other,competing=chosen.kind)
                    other.context['last_transition_event']=self.w.turn
                else:
                    key='Agency:Transitions:'+kind;self.w.metrics[key]=self.w.metrics.get(key,0)+1
        for n in active:
            if n.status in FINISHED or n is chosen:continue
            if n.kind in ('revenge','pursuit','protection') and self.current(person,n):
                reason='distance' if not n.context.get('known_location') or n.target_id not in self.e.spatial.at(person.position) else 'other_need'
                self.diagnostic(person,'lethal',n,reason,chosen.kind)

    def diagnostic(self, person, category, need, reason, competing=None):
        key=f'Agency:Passivity:{category}:{reason}';self.w.metrics[key]=self.w.metrics.get(key,0)+1
        last=person.agency_state.setdefault('diagnostics',{}).get(category)
        marker=(need.id,reason,competing)
        if last and tuple(last.get('marker',()))==marker and self.w.turn-last['turn']<48:return
        person.agency_state['diagnostics'][category]={'marker':marker,'turn':self.w.turn}
        self.event(person,'AgencyDiagnostic',need_id=need.id,category=category,reason=reason,
                   competing=competing,profile=self.profile(person,need))

    def blocked(self, person, need):
        h=need.context.setdefault('unresolved',{});h['blocks']=h.get('blocks',0)+1
        if need.kind in ('food','water') and need.context.get('emergency'):
            self.diagnostic(person,'vital',need,'no_viable_known_solution')
        elif need.kind in ('revenge','pursuit'):
            self.diagnostic(person,'lethal',need,'no_solution_or_lost_lead')

    def snapshot(self, person, need):
        target=need.context.get('threat',need.target_id) if need.kind=='protection' else need.target_id
        observed=person.observations.get(target)
        loc=Location(**need.context['known_location']) if need.context.get('known_location') else None
        known_distance=distance(person.position,loc) if loc else None
        if loc and loc.map_id!=person.position.map_id and person.known_towns.get(loc.map_id,{}).get('position'):
            point=Location(**person.known_towns[loc.map_id]['position'])
            if person.position.map_id==self.w.world_map_id:known_distance=distance(person.position,point)+3
            else:
                grid=self.w.maps[person.position.map_id]
                if grid.exit_to:known_distance=distance(person.position,Location(grid.id,grid.width//2,grid.height-1))+1+distance(grid.exit_to,point)+3
        if target in self.e.spatial.at(person.position):
            actual=self.w.characters[target];observed_health=actual.health
        else:observed_health=observed.health if observed else None
        if need.kind=='migration' and person.migration:known_distance=self.e.migration.remaining(person)
        return {'position':person.position,'distance':known_distance,'migration':bool(person.migration),
                'money':person.money,'training':person.training_progress,'profession':person.profession,
                'information':observed.turn if observed else -1,'health':person.health,
                'food':self.e.items.count(person.id,'food'),'water':self.e.items.count(person.id,'water'),'reported':need.context.get('reported',False),
                'target_health':observed_health,
                'recognition':person.agency_state.get('recognition',0),'mythic_development':person.mythic_development,
                'social_progress':person.social_state.get('meaningful_social_actions',0),
                'group_count':len(person.group_ids),'organization_count':len(person.organization_ids)}

    def outcome(self, person, need, action, before, success, hours=1):
        after=self.snapshot(person,need);h=need.context.setdefault('unresolved',{})
        prep=person.commitments.get(need.context.get('preparing_commitment'))
        if prep and prep.status in ('active','paused') and success:
            requirements=prep.context.get('required_provisions',{})
            gained=any(after[k]>before[k] and before[k]<requirements.get(k,0) for k in ('food','water'))
            if gained:
                prep.last_progress_at=self.w.turn;prep.meaningful_progress+=1
                self.event(person,'CommitmentPreparation',prep,action=action,resources={k:after[k] for k in ('food','water')})
        h['attempts']=h.get('attempts',0)+1
        advanced=[]
        domain=need.context.get('aspiration_domain') or need.context.get('domain')
        dimensions=('mythic_development',) if need.kind=='power' else ('group_count','organization_count') if need.kind in ('political_pressure','organizational_survival') else ('training',) if domain=='competence' else ('money',) if need.kind=='advancement' else ('recognition',) if need.kind=='status' else ('information',)
        if need.kind in ('political_pressure','organizational_survival','governance'):dimensions=dimensions+('social_progress',)
        for k in dimensions:
            if after[k]>before[k]:advanced.append(k)
        if domain=='competence' and after['profession']!=before['profession']:advanced.append('profession')
        if need.kind=='migration' and after['migration'] and not before['migration']:advanced.append('journey_started')
        if need.kind in ('migration','revenge','pursuit','family') and (after['food']>before['food'] or after['water']>before['water']):advanced.append('provisions')
        if before['position']!=after['position'] and before['distance'] is not None and after['distance']<before['distance']:advanced.append('approach')
        if after['reported'] and not before['reported']:advanced.append('report')
        if need.status=='satisfied':
            advanced.append('resolution')
            if need.context.get('aspiration_domain')=='family':
                a=next((a for a in person.aspirations if a.domain=='family' and a.status=='active'),None)
                if a:
                    marker=(need.id,need.context.get('source_event'))
                    solved=a.context.setdefault('resolved_care',[])
                    if marker not in solved:
                        solved.append(marker);del solved[:-3];a.progress=min(1,len(solved)/3)
        if need.kind in ('food','family') and after['food']>before['food']:advanced.append('resource')
        # Golpes isolados são atividade. Consequências graves contam separadamente.
        if before['target_health'] is not None and after['target_health'] is not None and before['target_health']>12>=after['target_health']:advanced.append('incapacity')
        if not success:h['failures']=h.get('failures',0)+1
        if advanced:h['progress']=h.get('progress',0)+1
        c=self.current(person,need)
        if not c:return
        c.activity_count+=1;c.investment+=hours;c.last_attempt_at=self.w.turn
        if c.last_strategy and c.last_strategy!=action:
            c.strategy_changes+=1;self.event(person,'CommitmentStrategyChanged',c,previous=c.last_strategy,next=action)
        c.last_strategy=action
        if advanced:
            c.meaningful_progress+=1;c.progress+=1;c.last_progress_at=self.w.turn;c.stalled_actions[action]=0
            self.event(person,'CommitmentProgress',c,changes=advanced,action=action)
        else:
            c.setbacks+=1;c.failures+=int(not success)
            c.stalled_actions[action]=min(10,c.stalled_actions.get(action,0)+1)
        if need.status=='satisfied':self.close(person,c,'satisfied','verified_need_resolution')

    def on_fact(self, person, fact):
        if fact.kind=='ResponsibilityFulfilled' and fact.actor_id==person.id and fact.context.get('recognized_by'):
            person.agency_state['recognition']=person.agency_state.get('recognition',0)+1
            for n in person.needs.values():
                c=self.current(person,n)
                if c and n.kind=='status' and n.source==fact.context.get('need_source'):
                    c.meaningful_progress+=1;c.progress+=1;c.last_progress_at=self.w.turn
                    self.event(person,'CommitmentProgress',c,changes=['public_recognition'],action='work')
        if fact.kind=='CharacterKilled' and fact.confidence>=60:
            for n in person.needs.values():
                c=self.current(person,n)
                if c and n.kind=='revenge' and n.context.get('victim')==fact.target_id and n.target_id is not None:
                    c.context.setdefault('supporting_facts',[]).append(fact.event_id)
                    c.context['supporting_facts']=list(dict.fromkeys(c.context['supporting_facts']))[-3:]
                    if c.target_id!=n.target_id:
                        old=c.target_id;c.target_id=n.target_id;c.last_progress_at=self.w.turn;c.context['cause_identity']=self.identity(n)
                        c.meaningful_progress+=1;self.event(person,'CommitmentRetargeted',c,old_target=old,evidence=fact.event_id)
        if fact.kind in ('CharacterKilled','CharacterDied','CharacterCaptured','ConflictForgiven','RestitutionGiven','ApologyGiven'):
            for c in list(person.commitments.values()):
                if c.status not in LIVE:continue
                if fact.kind in ('CharacterKilled','CharacterDied','CharacterCaptured') and fact.target_id==c.target_id:
                    self.close(person,c,'satisfied','known_target_unavailable');continue
                if fact.kind in ('ConflictForgiven','RestitutionGiven','ApologyGiven') and fact.target_id==person.id and fact.actor_id==c.target_id:
                    self.close(person,c,'satisfied','known_reconciliation')

    def travel_candidates(self, person, need):
        if need.kind not in ('revenge','response','pursuit','family','protection'):return []
        data=need.context.get('known_location')
        if not data:return []
        target=Location(**data)
        if target.map_id==person.position.map_id:return []
        return self.e.geography.candidates(person,target.map_id,need.kind,need)

    def follow_lead(self, person, town_id, need):
        return self.e.geography.travel(person,town_id,need.kind if need else 'return_home')
