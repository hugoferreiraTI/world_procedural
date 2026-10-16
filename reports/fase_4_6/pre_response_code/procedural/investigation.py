"""Busca geral por informação conhecida; pistas são locais de busca, não GPS."""
from dataclasses import replace
from .models import Clue, Location
from .navigation import distance
from .rules import INTERACTION, AGENCY

SEARCH_KINDS={'revenge','pursuit','family'}
SEARCH_ACTIONS={'search_area','ask_about_person'}

class InvestigationSystem:
    def __init__(self,e):self.e,self.w=e,e.world
    def count(self,key):
        key='Investigation:'+key;self.w.metrics[key]=self.w.metrics.get(key,0)+1
    @staticmethod
    def subject(n):return n.target_id if n.target_id is not None else n.context.get('victim')
    def eligible(self,n):return n.kind in SEARCH_KINDS and (n.kind!='family' or n.context.get('mode')=='missing')
    def state(self,p,n):
        c=self.e.agency.current(p,n)
        return c,c.context.setdefault('investigation',{'clues':[],'asked':[],'areas':[],'attempts':0,'started':self.w.turn}) if c else None
    def from_fact(self,f,subject):
        if not f.location:return None
        who=(f.actor_id if f.kind in ('CharacterFled','ResidentMoved') else
             f.context.get('subject') if f.kind=='SearchClueShared' else f.context.get('suspect_id') if f.kind=='WantedIssued' else f.target_id)
        if f.actor_id==subject and f.kind in ('CharacterAttacked','CharacterThreatened','CharacterKilled'):who=subject
        if who!=subject:return None
        if f.kind not in ('PersonLocated','SuspectLocated','CharacterFled','ResidentMoved','SearchClueShared','WantedIssued') and f.actor_id!=subject:return None
        loc=Location(**f.context['new_location']) if f.kind=='CharacterFled' else Location(**f.context['last_known_location']) if f.kind=='WantedIssued' else f.location
        return Clue(subject,loc,f.context.get('observed_at',f.turn),f.source_id,f.confidence,
                    f.context.get('specificity','cell'),f.event_id,source_kind=f.source_kind)
    def better(self,new,old):
        if old is None:return True
        if new.observed_at<old.observed_at:return False
        if new.observed_at==old.observed_at:return new.confidence>old.confidence or new.confidence==old.confidence and new.specificity=='cell' and old.specificity!='cell'
        return new.confidence>=30 and (new.confidence>=old.confidence-40 or new.observed_at-old.observed_at>=48)
    def accept(self,p,n,clue):
        c,s=self.state(p,n)
        if not c or not s or clue.subject_id!=self.subject(n) or clue.confidence<30:return False
        old=s['clues'][-1] if s['clues'] else None
        if not self.better(clue,old):return False
        s['clues'].append(clue);del s['clues'][:-3]
        s.update(asked=[],areas=[],attempts=0,started=self.w.turn)
        n.context.update(known_location=vars(clue.location),lead_turn=clue.observed_at,search_attempts=0,investigated=False)
        c.last_progress_at=self.w.turn;c.meaningful_progress+=1;c.stalled_actions.clear()
        self.count('new_clue');self.count('rumor' if clue.source_kind=='rumor' else 'known_clue')
        self.e.agency.event(p,'InvestigationClue',c,clue=vars(clue)|{'location':vars(clue.location)},
                            age=max(0,self.w.turn-clue.observed_at))
        if c.status=='waiting_for_information':
            c.status=n.status='active';n.expires_at=self.w.turn+48
            self.count('reactivated');self.e.agency.event(p,'CommitmentReactivated',c,clue_fact=clue.related_fact)
        return True
    def on_fact(self,p,f):
        for n in list(p.needs.values()):
            if not self.eligible(n) or n.status in ('satisfied','failed','expired','inactive'):continue
            clue=self.from_fact(f,self.subject(n))
            if clue:self.accept(p,n,clue)
        if p.profession=='guarda' and f.kind in ('SearchClueShared','PersonLocated','SuspectLocated','CharacterFled'):self.e.justice.submit_clue(p,f)
    def refresh(self,p):
        for other in p.needs.values():other.context.pop('preparing_commitment',None)
        for n in list(p.needs.values()):
            if not self.eligible(n):continue
            c,s=self.state(p,n)
            if not c:continue
            subject=self.subject(n)
            obs=p.observations.get(subject)
            if obs and obs.alive and not (subject in self.e.spatial.at(p.position) and s['clues'] and s['clues'][-1].location==obs.position):
                self.accept(p,n,Clue(subject,obs.position,obs.turn,p.id,100,'cell',None,source_kind='direct'))
            if not s['clues']:
                facts=[self.from_fact(f,subject) for f in p.knowledge.values()]
                for clue in sorted((f for f in facts if f),key=lambda f:f.observed_at):self.accept(p,n,clue)
                if not s['clues'] and n.context.get('known_location'):
                    f=p.knowledge.get(n.context.get('source_event'))
                    if f:self.accept(p,n,Clue(subject,Location(**n.context['known_location']),f.turn,f.source_id,f.confidence,'cell',f.event_id,source_kind=f.source_kind))
            if c.status=='waiting_for_information':n.status='waiting_for_information';continue
            if s['clues'] and s['clues'][-1].location.map_id!=p.position.map_id and c.intensity>=60:
                destination=p.known_towns.get(s['clues'][-1].location.map_id)
                if destination:
                    origin=self.w.towns[p.town_id].position
                    point=Location(**destination['position'])
                    hours=distance(origin,point)+8
                    food,water=self.e.migration.supplies(p,hours)
                    c.context['required_provisions']={'food':food,'water':water}
                else:c.context['required_provisions']={}
                for other in p.needs.values():
                    if other.kind in ('food_reserve','water','money','rest') and other.status not in ('satisfied','failed','expired','inactive'):
                        other.context['preparing_commitment']=c.id
            if subject in self.e.spatial.at(p.position):continue
            limit=3+min(5,n.context.get('severity',1)) if n.kind=='pursuit' else 6
            duration=96+24*n.context.get('severity',0)
            if s['attempts']>=limit or s['attempts'] and self.w.turn-s['started']>=duration:self.sleep(p,n,'local_sources_exhausted')
            elif (not s['clues'] or s['clues'][-1].location.map_id==p.position.map_id) and not self.candidates(p,n):self.sleep(p,n,'no_remaining_known_source')
    def sleep(self,p,n,reason):
        c,s=self.state(p,n)
        if not c or c.status=='waiting_for_information':return
        c.status=n.status='waiting_for_information';n.expires_at=None
        if p.goal and p.goal.need_id==n.id:p.goal=None
        self.count('dormant');self.e.agency.event(p,'CommitmentDormant',c,reason=reason,attempts=s['attempts'])
    def candidates(self,p,n):
        if not self.eligible(n):return None
        c,s=self.state(p,n)
        if not c:return None
        if c.status=='waiting_for_information':return []
        subject=self.subject(n)
        if subject in self.e.spatial.at(p.position):return None
        clue=s['clues'][-1] if s['clues'] else None
        if clue and clue.location.map_id!=p.position.map_id:return []
        choices=[]
        for i in self.e.spatial.at(p.position)[:12]:
            if i not in (p.id,subject) and i not in s['asked'] and self.e.social.can_request(p,self.w.characters[i]):choices.append(('ask_about_person',None,i))
        locations=[clue.location] if clue else []
        locations.extend(p.known_places[k] for k in ('market','forage') if k in p.known_places)
        for loc in dict.fromkeys(locations):
            if loc.map_id==p.position.map_id and loc not in s['areas']:choices.append(('search_area',loc,subject))
        return choices
    def execute(self,p,goal,n):
        c,s=self.state(p,n)
        if not c or c.status=='waiting_for_information':return False,'Busca em espera.'
        subject=self.subject(n);s['attempts']+=1
        if goal.action=='search_area':
            if p.position not in s['areas']:s['areas'].append(p.position);del s['areas'][:-4]
            self.count('area_searched');self.e.conflicts.observe(p)
            visible=self.w.characters.get(subject)
            if visible and visible.position==p.position:
                self.e.personal_actions.locate(p,subject);self.count('found' if visible.alive else 'remains_found')
            else:
                self.e.agency.event(p,'InvestigationSearched',c,area=vars(p.position),attempt=s['attempts'])
                if s['clues'] and self.w.turn-s['clues'][-1].observed_at>24:self.count('stale_clue')
            return True,'Área conhecida observada; ausência não revela destino remoto.'
        informant=self.w.characters.get(goal.target_id)
        if not informant or informant.id not in self.e.spatial.at(p.position):return False,'Informante ausente.'
        if informant.id in s['asked']:return False,'Fonte já consultada nesta pista.'
        s['asked'].append(informant.id);del s['asked'][:-8];self.count('asked')
        trust=self.e.graph.value(informant.id,p.id,'confiança')
        loyalty=max(self.e.graph.value(informant.id,subject,'amizade'),self.e.graph.value(informant.id,subject,'casamento'))
        feared=informant.reputations.get(p.id);fear=feared.fear if feared else 0
        willingness=informant.personality.honesty*.35+informant.personality.compassion*.25+trust*.3-fear*.25-loyalty*.4
        facts=[(f,self.from_fact(f,subject)) for f in informant.knowledge.values()]
        facts=[(f,clue) for f,clue in facts if clue]
        # Uma observação física própria também é conhecimento do informante.
        obs=informant.observations.get(subject)
        if obs and obs.alive:
            clue=Clue(subject,obs.position,obs.turn,informant.id,100,'cell',None,source_kind='direct')
            facts.append((None,clue))
        best=max(facts,key=lambda pair:(pair[1].observed_at,pair[1].confidence),default=None) if willingness>=10 else None
        if not best:
            self.count('useless');self.e.agency.event(p,'InvestigationReply',c,informant=informant.id,result='refused' if willingness<10 else 'no_information')
            return True,'Fonte recusou ou não possui conhecimento relevante.'
        f,clue=best
        receiving_trust=self.e.graph.value(p.id,informant.id,'confiança',10)
        confidence=min(clue.confidence,60 if receiving_trust>=30 else 30)
        kind='known' if receiving_trust>=30 and clue.source_kind!='rumor' and confidence>30 else 'rumor'
        old=s['clues'][-1] if s['clues'] else None
        shared=replace(clue,confidence=confidence,source_kind=kind,source_id=informant.id)
        useful=self.better(shared,old)
        self.count('useful' if useful else 'useless')
        self.e.recorder.emit('SearchClueShared',f'{informant.name} informou uma pista conhecida a {p.name}.',
            informant.id,p.id,clue.location,witnesses=[informant.id,p.id],historical=True,
            context={'subject':subject,'observed_at':clue.observed_at,'specificity':clue.specificity,
                     'confidence':confidence,'clue_source_kind':kind,'related_fact':f.event_id if f else None})
        return True,'Informação derivada exclusivamente da memória/observação da fonte.'
    def return_home(self,p,n=None):
        if p.position.map_id==p.home.map_id:
            self.e.navigation.approach(p,p.home,1);return True,'Retorno local à rotina.'
        town_id=p.home.map_id
        # A localização da própria residência/cidade é conhecimento próprio.
        known=p.known_towns.get(town_id)
        if not known:p.known_towns[town_id]={'position':vars(self.w.towns[town_id].position),'confidence':100}
        return self.e.agency.follow_lead(p,town_id,n)
