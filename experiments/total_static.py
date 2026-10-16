"""Inventário estático da autoridade atual: fontes, AST, pesos e testes."""
import ast
import dataclasses
import hashlib
import inspect
import json
from collections import Counter,defaultdict
from pathlib import Path

from procedural import RULES_VERSION,GENERATION_VERSION,utility,rules

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'reports/auditoria_total'
TRAITS=('honesty','compassion','courage','independence','greed','diligence','family_loyalty','persistence','temperament','vengefulness','ambition','sadism')
SERVICE={'access':'AccessActions','action_pressure':'ActionPressureSystem','aftermath':'AftermathSystem','agency':'AgencySystem',
 'collective':'CollectiveActionSystem','conflicts':'ConflictSystem','divine_relations':'DivineRelations','economy':'Economy','emotions':'EmotionSystem',
 'feeding':'FeedingSystem','geography':'Geography','goals':'GoalSystem','institutions':'Institutions','investigation':'InvestigationSystem',
 'items':'ItemService','justice':'JusticeSystem','knowledge':'KnowledgeSystem','lethal_decisions':'LethalDecisionSystem','lethality':'LethalPressure',
 'migration':'MigrationSystem','navigation':'Navigation','needs':'NeedSystem','personal':'PersonalNeeds','personal_actions':'PersonalActions',
 'population':'Population','professions':'ProfessionSystem','quests':'QuestSystem','recovery':'RecoverySystem','graph':'RelationshipGraph',
 'religious_health':'ReligiousHealth','renown':'RenownSystem','social':'SocialSystem','society':'SocietySystem','terminal_combat':'TerminalCombat',
 'faith':'FaithSystem','recorder':'EventRecorder','bus':'EventBus','spatial':'SpatialIndex','rng':'random.Random'}

def jwrite(path,value):path.write_text(json.dumps(value,ensure_ascii=False,indent=2),encoding='utf-8')
def expr(node):return ast.unparse(node) if node is not None else ''
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def fingerprint():
 h=hashlib.sha256()
 for p in sorted((ROOT/'procedural').glob('*.py')):h.update(p.name.encode());h.update(p.read_bytes())
 return h.hexdigest()
def nodes_own(fn):
 stack=list(reversed(fn.body))
 while stack:
  n=stack.pop();yield n
  if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef)):continue
  stack.extend(reversed(list(ast.iter_child_nodes(n))))
def literal_strings(node):
 if isinstance(node,ast.Constant) and isinstance(node.value,str):return {node.value}
 if isinstance(node,(ast.List,ast.Tuple,ast.Set)):
  return set().union(*(literal_strings(x) for x in node.elts)) if node.elts else set()
 return set()
def table(headers,rows):
 def fmt(x):
  if isinstance(x,(dict,list,tuple)):x=json.dumps(x,ensure_ascii=False,separators=(',',':'))
  return str(x).replace('|','\\|').replace('\n',' ')
 return '\n'.join(['| '+' | '.join(headers)+' |','| '+' | '.join('---' for x in headers)+' |']+['| '+' | '.join(fmt(x) for x in r)+' |' for r in rows])+'\n\n'

class Inventory:
 def __init__(self):
  self.files=[];self.functions=[];self.models=[];self.constants=[];self.events=[];self.consumers=[];self.needs=[];self.gates=[];self.traits=[];self.rng=[];self.invariants=[];self.tests=[];self.thresholds=[];self.states=[];self.relationships=[];self.numeric_literals=[]
 def scan(self):
  for file in sorted((ROOT/'procedural').glob('*.py')):self.file(file)
  for file in sorted((ROOT/'tests').glob('test_*.py')):self.test_file(file)
  allids={f['symbol']:f for f in self.functions};byclass={}
  imported={}
  for path in (ROOT/'procedural').glob('*.py'):
   aliases={}
   for node in ast.walk(ast.parse(path.read_text())):
    if isinstance(node,ast.ImportFrom) and node.module:
     for a in node.names:aliases[a.asname or a.name]=node.module.rsplit('.',1)[-1]+'.'+a.name
   imported[path.stem]=aliases
  for f in self.functions:
   if f['class']:byclass[(f['class'],f['name'])]=f['symbol']
  callers=defaultdict(set)
  for f in self.functions:
   resolved={}
   for c in f['calls']:
    parts=c.split('.')
    if len(parts)==2 and parts[0]=='self' and (f['class'],parts[-1]) in byclass:resolved[c]=byclass[(f['class'],parts[-1])]
    elif len(parts)>1 and parts[-2] in SERVICE and (SERVICE[parts[-2]],parts[-1]) in byclass:resolved[c]=byclass[(SERVICE[parts[-2]],parts[-1])]
    elif c in allids:resolved[c]=c
    elif f"{f['module']}.{c}" in allids:resolved[c]=f"{f['module']}.{c}"
    elif c in imported[f['module']] and imported[f['module']][c] in allids:resolved[c]=imported[f['module']][c]
    elif '.' not in c:
     scope=f['symbol'].split('.')
     for size in range(len(scope),0,-1):
      candidate='.'.join(scope[:size])+'.'+c
      if candidate in allids:resolved[c]=candidate;break
   f['resolved_calls']=resolved
   for target in resolved.values():callers[target].add(f['symbol'])
  for f in self.functions:f['static_callers']=sorted(callers[f['symbol']])
  self.actions=[{'action':a,'base':base,'weights':utility.WEIGHTS.get(a,{}),'evaluated_in':'goals.GoalSystem._evaluate → utility.evaluate'} for a,base in sorted(utility.BASE.items())]
  for trait in TRAITS:
   for a,weights in utility.WEIGHTS.items():
    if trait in weights:self.traits.append({'trait':trait,'symbol':'utility.evaluate','line':None,'expression':f"WEIGHTS[{a!r}][{trait!r}] = {weights[trait]}",'classification':'Utility; traço normalizado; sinal do peso','action':a})
  self.rule_constants=[]
  for name,obj in vars(rules).items():
   if not name.isupper():continue
   if dataclasses.is_dataclass(obj) and not isinstance(obj,type):
    for field in dataclasses.fields(obj):self.rule_constants.append({'name':f'{name}.{field.name}','value':getattr(obj,field.name),'source':'procedural/rules.py'})
   elif isinstance(obj,(int,float,str,dict,tuple)):self.rule_constants.append({'name':name,'value':obj,'source':'procedural/rules.py'})
  return self
 def file(self,file):
  code=file.read_text();tree=ast.parse(code);module=file.stem;parents={child:n for n in ast.walk(tree) for child in ast.iter_child_nodes(n)}
  imports=[expr(n) for n in ast.walk(tree) if isinstance(n,(ast.Import,ast.ImportFrom))]
  self.files.append({'path':str(file.relative_to(ROOT)),'module':module,'sha256':sha(file),'lines':len(code.splitlines()),'responsibility':ast.get_docstring(tree) or 'Dados/rotinas do módulo.','imports':imports})
  constants={}
  for n in tree.body:
   if isinstance(n,(ast.Assign,ast.AnnAssign)):
    targets=n.targets if isinstance(n,ast.Assign) else [n.target]
    for target in targets:
     if isinstance(target,ast.Name) and target.id.isupper():
      constants[target.id]=n.value;self.constants.append({'module':module,'name':target.id,'line':n.lineno,'expression':expr(n.value)})
   if isinstance(n,ast.ClassDef):
    fields=[{'name':v.target.id,'annotation':expr(v.annotation),'default':expr(v.value),'line':v.lineno} for v in n.body if isinstance(v,ast.AnnAssign) and isinstance(v.target,ast.Name)]
    if any('dataclass' in expr(d) for d in n.decorator_list):self.models.append({'module':module,'class':n.name,'line':n.lineno,'fields':fields,'doc':ast.get_docstring(n)})
  def walk(body,cls='',scope=''):
   for fn in body:
    if isinstance(fn,ast.ClassDef):walk(fn.body,fn.name,fn.name)
    if not isinstance(fn,(ast.FunctionDef,ast.AsyncFunctionDef)):continue
    symbol=f'{module}.{scope+"." if scope else ""}{fn.name}';nodes=list(nodes_own(fn))
    bindings={}
    for n in nodes:
     if isinstance(n,ast.Constant) and isinstance(n.value,(int,float)) and not isinstance(n.value,bool):
      parent=parents.get(n)
      while parent is not None and not isinstance(parent,ast.stmt):parent=parents.get(parent)
      self.numeric_literals.append({'symbol':symbol,'line':n.lineno,'value':n.value,'context':expr(parent)[:2200] if parent else expr(n)})
     if isinstance(n,ast.Assign):
      for target in n.targets:
       if isinstance(target,ast.Name):bindings.setdefault(target.id,[]).append(n.value)
     elif isinstance(n,ast.For) and isinstance(n.target,ast.Name):
      bindings.setdefault(n.target.id,[]).append(n.iter)
    personality_aliases={name for name,values in bindings.items() if any(isinstance(v,ast.Attribute) and v.attr=='personality' for v in values)}
    def strings(node,seen=frozenset()):
     s=literal_strings(node)
     if s:return s
     if isinstance(node,ast.Name) and node.id not in seen:
      candidates=bindings.get(node.id,[]) + ([constants[node.id]] if node.id in constants else [])
      result=set()
      for v in candidates:result.update(strings(v,seen|{node.id}))
      return result
     if isinstance(node,ast.IfExp):return strings(node.body,seen)|strings(node.orelse,seen)
     if isinstance(node,ast.BinOp) and isinstance(node.op,ast.BitOr):return strings(node.left,seen)|strings(node.right,seen)
     if isinstance(node,ast.BinOp) and isinstance(node.op,ast.Add):
      aa,bb=strings(node.left,seen),strings(node.right,seen)
      return {a+b for a in aa for b in bb} if aa and bb else set()
     return set()
    calls=sorted({expr(n.func) for n in nodes if isinstance(n,ast.Call)})
    writes=set();reads=set();guards=[]
    for n in nodes:
     if isinstance(n,ast.Attribute) and isinstance(n.ctx,ast.Load) and not (isinstance(parents.get(n),ast.Call) and parents[n].func is n):reads.add(expr(n))
     if isinstance(n,(ast.Attribute,ast.Subscript)) and isinstance(n.ctx,ast.Store):writes.add(expr(n))
     if isinstance(n,ast.AugAssign) and isinstance(n.target,(ast.Attribute,ast.Subscript)):reads.add(expr(n.target));writes.add(expr(n.target))
     if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr in ('append','extend','pop','remove','discard','clear','update','setdefault','add'):writes.add(expr(n.func.value)+' [mutação por '+n.func.attr+']')
     if isinstance(n,ast.If):
      exits=[x for x in n.body if isinstance(x,(ast.Return,ast.Continue,ast.Raise))]
      if exits:
       g={'symbol':symbol,'line':n.lineno,'condition':expr(n.test),'effect':'; '.join(expr(x) for x in exits)};self.gates.append(g);guards.append(g)
     if isinstance(n,(ast.If,ast.IfExp,ast.comprehension)):
      test=n.test if hasattr(n,'test') else None
      if test and any(isinstance(x,ast.Constant) and isinstance(x.value,(int,float)) and not isinstance(x.value,bool) for x in ast.walk(test)):
       self.thresholds.append({'symbol':symbol,'line':n.lineno,'condition':expr(test)})
     if isinstance(n,ast.Assign):
      def state_targets(target,value):
       if isinstance(target,ast.Attribute) and target.attr in ('status','mode','kind','lod','condition','rank'):
        self.states.append({'symbol':symbol,'line':n.lineno,'field':expr(target),'value':expr(value)})
       elif isinstance(target,ast.Subscript) and isinstance(target.slice,ast.Constant) and target.slice.value in ('status','mode','kind','lod','condition','rank'):
        self.states.append({'symbol':symbol,'line':n.lineno,'field':expr(target),'value':expr(value)})
       elif isinstance(target,(ast.Tuple,ast.List)):
        if isinstance(value,(ast.Tuple,ast.List)) and len(target.elts)==len(value.elts):
         for a,b in zip(target.elts,value.elts):state_targets(a,b)
        else:
         for a in target.elts:state_targets(a,value)
      for target in n.targets:state_targets(target,n.value)
     if isinstance(n,ast.Dict):
      for key,value in zip(n.keys,n.values):
       if isinstance(key,ast.Constant) and key.value in ('status','mode','kind','lod','condition','rank'):
        self.states.append({'symbol':symbol,'line':n.lineno,'field':'dict['+repr(key.value)+']','value':expr(value)})
     if isinstance(n,ast.Attribute) and n.attr in TRAITS and ('personality' in expr(n.value) or expr(n.value) in personality_aliases):
      parent=parents.get(n)
      while parent is not None and not isinstance(parent,(ast.stmt,ast.comprehension)):parent=parents.get(parent)
      statement=expr(parent) if parent is not None else expr(n)
      self.traits.append({'trait':n.attr,'symbol':symbol,'line':n.lineno,'expression':statement[:2200],'classification':('gate' if isinstance(parent,ast.If) else 'prioridade' if 'priority' in fn.name else 'pressão/score/efeito; expressão exata abaixo')})
     if not isinstance(n,ast.Call):continue
     name=expr(n.func);last=name.rsplit('.',1)[-1];args=n.args;kws={k.arg:expr(k.value) for k in n.keywords}
     if last=='update':
      for key,value in kws.items():
       if key in ('status','mode','kind','lod','condition','rank'):self.states.append({'symbol':symbol,'line':n.lineno,'field':expr(n.func.value)+'.'+key,'value':value})
     if last in ('emit','event'):
      index=1 if last=='event' or cls=='LethalDecisionSystem' and name=='self.emit' else 0
      kinds=strings(args[index]) if len(args)>index else set()
      self.events.append({'symbol':symbol,'line':n.lineno,'call':expr(n),'kinds':sorted(kinds),'kind_expression':expr(args[index]) if len(args)>index else '<keyword/dynamic>','receiver':name,'keywords':kws})
     if last=='subscribe':self.consumers.append({'symbol':symbol,'line':n.lineno,'call':expr(n),'kinds':sorted(strings(args[0])) if args else [],'kind_expression':expr(args[0]) if args else '', 'handler':expr(args[1]) if len(args)>1 else ''})
     if last=='ensure' and len(args)>=2:
      keys=sorted(strings(args[1]));self.needs.append({'symbol':symbol,'line':n.lineno,'owner':expr(args[0]),'keys':keys,'kinds':sorted({k.split(':')[0] for k in keys}),'kind_expression':expr(args[1]),'arguments':[expr(a) for a in args[2:]],'keywords':kws,'call':expr(n)})
     if last=='create' and (module=='personal' and name=='self.create' or '.personal.create' in name) and len(args)>=2:
      self.needs.append({'symbol':symbol,'line':n.lineno,'owner':expr(args[0]),'keys':[],'kinds':sorted(strings(args[1])),'kind_expression':expr(args[1]),'arguments':[expr(a) for a in args[2:]],'keywords':kws,'call':expr(n)})
     if last in ('set','adjust','value','key') and ('.graph.' in name or name.startswith('graph.') or module=='relationships') and len(args)>=3:
      self.relationships.append({'symbol':symbol,'line':n.lineno,'kinds':sorted(strings(args[2])),'call':expr(n)})
     if last in ('random','randint','randrange','uniform','choice','choices','sample','shuffle','Random','getstate','setstate') and ('rng' in name or 'random' in name):self.rng.append({'symbol':symbol,'line':n.lineno,'call':expr(n)})
     if module=='validation' and last in ('append','extend') and 'errors' in name:
      ancestors=[];par=parents.get(n)
      while par is not None and par is not fn:
       if isinstance(par,ast.If):ancestors.append(expr(par.test))
       par=parents.get(par)
      self.invariants.append({'symbol':symbol,'line':n.lineno,'conditions':list(reversed(ancestors)),'error':expr(n.args[0]) if n.args else expr(n)})
    # Comparações de kind são o catálogo complementar; não tratá-las como criadores.
    need_checks=[];event_checks=[]
    for n in nodes:
     if isinstance(n,ast.Compare):
      if any(isinstance(v,ast.Attribute) and v.attr=='kind' for v in ast.walk(n.left)):
       values=set().union(*(literal_strings(x) for x in n.comparators))
       row={'line':n.lineno,'expression':expr(n),'values':sorted(values)}
       left=expr(n.left)
       if any(x in left for x in ('fact','event','ev.')) or left=='f.kind':event_checks.append(row)
       elif left in ('n.kind','need.kind') or 'need.kind' in left:need_checks.append(row)
    self.functions.append({'symbol':symbol,'module':module,'class':cls,'name':fn.name,'line':fn.lineno,'end_line':fn.end_lineno,'signature':expr(fn.args),
      'public':not fn.name.startswith('_'),'doc':ast.get_docstring(fn),'calls':calls,'reads':sorted(reads),'writes':sorted(writes),'gates':guards,'need_checks':need_checks,'event_checks':event_checks})
    walk(fn.body,cls,scope+'.'+fn.name if scope else fn.name)
  walk(tree.body)
 def test_file(self,file):
  tree=ast.parse(file.read_text())
  for cls in tree.body:
   if not isinstance(cls,ast.ClassDef):continue
   for fn in cls.body:
    if not isinstance(fn,ast.FunctionDef) or not fn.name.startswith('test_'):continue
    assertions=[expr(n) for n in nodes_own(fn) if isinstance(n,ast.Call) and expr(n.func).startswith('self.assert')]
    calls=sorted({expr(n.func) for n in nodes_own(fn) if isinstance(n,ast.Call) and not expr(n.func).startswith('self.assert')})
    self.tests.append({'file':str(file.relative_to(ROOT)),'class':cls.name,'name':fn.name,'line':fn.lineno,'description':ast.get_docstring(fn) or fn.name.removeprefix('test_').replace('_',' '),'assertions':assertions,'calls':calls,'evidence':'controle/regressão, não ocorrência natural'})
 def data(self):return {k:v for k,v in vars(self).items()}

def render(inv):
 text='# MAPA DO CÓDIGO — inventário integral\n\n'
 text+=f"Autoridade: {len(inv.files)} arquivos de produção, {len(inv.functions)} funções/métodos (incluindo privados e funções locais), {len(inv.models)} dataclasses. SHA agregado `{fingerprint()}`. Regras `{RULES_VERSION}`, geração `{GENERATION_VERSION}`. Inventário-base concluído antes de qualquer simulação desta tarefa; aprofundamento de aliases, dicionários e literais na análise está registrado no manifesto.\n\n"
 text+='A análise de chamadores é estática e conservadora: resolve self e receptores dos serviços do Engine; despacho dinâmico, aliases e callbacks podem acrescentar chamadas. A campanha mede as arestas efetivamente vistas. Estado lido/alterado é expresso como no código (p, q, self.w etc.); mutação indireta por serviço deve ser seguida pela cadeia de chamadas. Uma condição listada não prova que foi atingida naturalmente. Não se anuncia ausência de chamada estática como código morto.\n\n'
 text+='## Navegação por arquivo\n\n'
 for file in inv.files:
  anchor=file['path'].replace('/','').replace('.','')
  text+=f"- [{file['path']}](#{anchor}) — {file['responsibility'].splitlines()[0]}\n"
 text+='\n'
 for file in inv.files:
  module=file['module'];fs=[f for f in inv.functions if f['module']==module]
  text+=f"## `{file['path']}`\n\n{file['responsibility']}\n\n{file['lines']} linhas; SHA256 `{file['sha256']}`.\n\n"
  text+='Imports/dependências: '+', '.join(f'`{x}`' for x in file['imports'])+'.\n\n'
  for f in fs:
   text+=f"### {f['symbol']} — L{f['line']}\n\nFonte: [{f['symbol']}](<{ROOT}/procedural/{module}.py:{f['line']}>).\n\n`{f['name']}({f['signature']})`\n\n"
   if f['doc']:text+=f['doc']+'\n\n'
   text+=table(['Aspecto','Extração direta'],[
    ('Chamadores resolvidos',f['static_callers']),('Chamadas resolvidas',f['resolved_calls']),('Outras chamadas/expressões', [c for c in f['calls'] if c not in f['resolved_calls']]),
    ('Estado lido',f['reads']),('Estado alterado diretamente',f['writes']),('Emissões neste símbolo',[e['call'] for e in inv.events if e['symbol']==f['symbol']]),
    ('Consumo/inscrição',[e['call'] for e in inv.consumers if e['symbol']==f['symbol']]+[e['expression'] for e in f['event_checks']])])
   if f['gates']:text+=table(['Linha','Condição de saída/continue/erro','Efeito'],[(g['line'],g['condition'],g['effect']) for g in f['gates']])
 text+='## Modelos, campos e persistência\n\nTodas as dataclasses conhecidas por persistence.TYPES são serializadas genericamente. Solution/WorkResult/CommandResult são valores operacionais: estar catalogado não significa fazer parte de WorldState. Os campos abaixo são os declarados, sem inventar propriedades.\n\n'
 for model in inv.models:
  text+=f"### {model['module']}.{model['class']}\n\n"+table(['Campo','Tipo','Padrão','Linha'],[(f['name'],f['annotation'],f['default'],f['line']) for f in model['fields']])
 text+='## Character — índice conservador de leitores e escritores por campo\n\nCorrespondência de acesso por nome de campo (não inferência de tipos). Campos homônimos de outro modelo podem aparecer; confirmar receptor/expressão no método. A criação de Character também inicializa campos por construtor/default, mesmo sem uma escrita p.campo na função.\n\n'
 character=next(m for m in inv.models if m['class']=='Character')
 import re
 rows=[]
 for field in character['fields']:
  pattern=re.compile(r'\.'+re.escape(field['name'])+r'(?![\w])')
  readers=[f['symbol'] for f in inv.functions if any(pattern.search(x) for x in f['reads'])]
  writers=[f['symbol'] for f in inv.functions if any(pattern.search(x) for x in f['writes'])]
  rows.append((field['name'],readers,writers))
 text+=table(['Campo','Leitores diretos candidatos','Escritores/mutações diretos candidatos'],rows)
 text+='## Todas as criações de Need e expressões dinâmicas\n\nKind dinâmico não foi convertido em uma lista fictícia. As condições exatas dos criadores estão no método correspondente acima; fonte, alvo e context são expressões reais.\n\n'
 text+=table(['Criador / linha','Dono','Kinds literais/resolvidos','Kind/urgência/fonte/motivo/alvo e keywords'],[(f"{x['symbol']}:{x['line']}",x['owner'],x['kinds'],x['call']) for x in inv.needs])
 text+='## Leitura de Need.kind / dispatch e alternativas\n\nCada criador deve ser lido junto dos dispatchers abaixo e do catálogo de ações. Condições são código real; associação exaustiva de ação a um kind pode depender de replace(kind=...), funções delegadas e estado. O relatório principal fornece a tabela semântica de Need→ações.\n\n'
 text+=table(['Símbolo','Linha','Condição real'],[(f['symbol'],x['line'],x['expression']) for f in inv.functions for x in f['need_checks']])
 text+='## Todas as ações Utility.BASE / WEIGHTS\n\nO nome correto é utility.BASE, não UTILITY.BASE. UTILITY em rules contém parâmetros de distância/desempate. MEALS usa ações de aquisição mapeadas ao score da ação-base; terminal, agency, mythic e ActionPressure podem modificar o resultado.\n\n'
 text+=table(['Ação','Base','Pesos (valor normalizado × peso)'],[(x['action'],x['base'],x['weights']) for x in inv.actions])
 text+='## Personalidade — todas as referências diretas e pesos dinâmicos\n\nCada linha mostra a expressão completa que dá peso/sinal/contexto; ternários e gates não têm um peso escalar universal. leituras dinâmicas de getattr/trait estão nos métodos de utility/generation e não são omitidas: os pesos por ação abaixo expandem esse caso.\n\n'
 for trait in TRAITS:
  text+=f'### {trait}\n\n'+table(['Símbolo / linha','Tipo','Expressão/peso/contexto'],[(f"{x['symbol']}:{x['line']}",x['classification'],x['expression']) for x in inv.traits if x['trait']==trait])
 text+='## Constantes declaradas e parâmetros de rules\n\n'
 text+=table(['Constante','Valor/expressão exata','Fonte'],[(x['name'],x['expression'],f"{x['module']}:{x['line']}") for x in inv.constants])
 text+=table(['Parâmetro expandido','Valor','Fonte'],[(x['name'],x['value'],x['source']) for x in inv.rule_constants])
 text+='## Thresholds numéricos embutidos e estados atribuídos\n\nAs condições abaixo completam os parâmetros nomeados: abrangem gates e ramificações sem saída imediata. Expressões preservam sinal, ranges, contexto e função.\n\n'
 text+=table(['Símbolo / linha','Condição numérica'],[(f"{x['symbol']}:{x['line']}",x['condition']) for x in inv.thresholds])
 text+=table(['Símbolo / linha','Campo de estado','Atribuição'],[(f"{x['symbol']}:{x['line']}",x['field'],x['value']) for x in inv.states])
 text+='## Literais numéricos nas funções — complemento de fórmulas/caps/ranges\n\nInclui cada ocorrência numérica com linha/contexto, mesmo fora de If (min/max, lotes, multiplicadores, divisores, índices e ranges). Um literal não é automaticamente um threshold: a expressão distingue escala, fórmula, índice e limite. Defaults de dataclasses e constantes de módulo estão nas seções próprias.\n\n'
 text+=table(['Símbolo / linha','Valor literal','Expressão de contexto'],[(f"{x['symbol']}:{x['line']}",x['value'],x['context']) for x in inv.numeric_literals])
 text+='## Relações — todos os sites de leitura/criação/alteração do grafo\n\nO grafo é dirigido; reciprocidade só existe quando o código a escreve. A chamada mostra origem, destino, espécie e valor/default exatos. Espécies dinâmicas são preservadas como expressão.\n\n'
 text+=table(['Símbolo / linha','Kinds resolvidos','Operação'],[(f"{x['symbol']}:{x['line']}",x['kinds'],x['call']) for x in inv.relationships])
 text+='## Todos os sites de RNG\n\nAs distribuições/ranges são os argumentos exatos das chamadas. RNG de simulação pertence ao Engine/world; o observador usa amostragem por hash separado, sem chamar estes métodos.\n\n'
 text+=table(['Símbolo','Linha','Chamada/range'],[(x['symbol'],x['line'],x['call']) for x in inv.rng])
 text+='## Todos os sites de emissão de evento\n\nCada chamada abaixo está catalogada, inclusive templates/nomes dinâmicos. Wrappers constroem actor/target/location/historical/context: seguir sua definição no módulo. Expressão dinâmica não é um evento adicional observado. EventRecorder é o único registrador final; seu perfil em runtime identifica nomes expandidos e emissores concretos.\n\n'
 text+=table(['Símbolo / linha','Kinds resolvidos / expressão','Chamada completa com contexto'],[(f"{x['symbol']}:{x['line']}",x['kinds'] or x['kind_expression'],x['call']) for x in inv.events])
 text+='## Inscrições e consumidores de fatos/eventos\n\n'
 text+=table(['Símbolo / linha','Inscrição'],[(f"{x['symbol']}:{x['line']}",x['call']) for x in inv.consumers])
 text+=table(['Símbolo','Linha','Filtro consumido'],[(f['symbol'],x['line'],x['expression']) for f in inv.functions for x in f['event_checks']])
 text+='## Todos os invariantes com diagnóstico do validador\n\nCada condição é a cadeia de If que envolve errors.append/extend. A ordem/loop/else deve ser lida na fonte: a tabela não transforma condições sintáticas em um novo validador. Fontes de assert_valid e persistência também estão no inventário de funções.\n\n'
 text+=table(['Símbolo / linha','Condições envolventes','Diagnóstico'],[(f"{x['symbol']}:{x['line']}",x['conditions'],x['error']) for x in inv.invariants])
 text+='## Suíte inteira — cada método de teste\n\nAssertivas e funções chamadas delimitam o que o teste prova. Nome descritivo não amplia sua garantia. Fixtures/setUp preparam o cenário; isto é evidência controlada, não emergência natural. Resultado da execução da suíte consta no manifesto e relatório principal.\n\n'
 text+=table(['Teste / linha','Capacidade declarada','Assertivas reais','Chamadas do cenário'],[(f"{x['file']}::{x['class']}.{x['name']}:{x['line']}",x['description'],x['assertions'],x['calls']) for x in inv.tests])
 (OUT/'MAPA_CODIGO.md').write_text(text,encoding='utf-8')
 return len(text.encode())

def main():
 OUT.mkdir(parents=True,exist_ok=True)
 manifest=OUT/'manifesto.json'
 if manifest.exists():raise RuntimeError('Inventário já registrado; não sobrescrever campanha existente.')
 inv=Inventory().scan();size=render(inv)
 data={'static':inv.data(),'systems':[],'natural':{}}
 jwrite(OUT/'coverage_matrix.json',data)
 jwrite(manifest,{'task':'Auditoria Total — Radiografia Integral','rules':RULES_VERSION,'generation':GENERATION_VERSION,'code_sha256':fingerprint(),
  'core_and_tests_sha256':{str(p.relative_to(ROOT)):sha(p) for directory in ('procedural','tests') for p in sorted((ROOT/directory).glob('*.py'))},
  'initial_commit':'c2f6178','static_complete_before_simulation':True,'inventory':{'production_files':len(inv.files),'functions':len(inv.functions),'dataclasses':len(inv.models),'event_sites':len(inv.events),'need_creation_sites':len(inv.needs),'gates':len(inv.gates),'test_methods':len(inv.tests),'map_bytes':size},
  'source_policy':'Sem alterações no núcleo, regras, testes ou balanceamento. Somente observador, análises e documentação externos.'})
 print(json.dumps(json.loads(manifest.read_text())['inventory'],ensure_ascii=False))

if __name__=='__main__':main()
