"""Conferência dos artefatos e manifesto reprodutível, sem simulação."""
from pathlib import Path
import hashlib,json,re,subprocess,ast
from .phase60_validation import sources,ROOT,OUT


def main():
    campaign=json.loads((OUT/'campanha.json').read_text())
    assert campaign['status']=='completed' and campaign['hours']==300
    control=json.loads((OUT/'controles.json').read_text());suite=json.loads((OUT/'suite_fontes.json').read_text())
    assert sources()==suite['sources']==control['sources']==campaign['sources']
    assert 'Ran 366 tests' in (OUT/'testes_final.log').read_text()
    assert (OUT/'testes_final.log').read_text().rstrip().endswith('OK')
    assert not (OUT/'save_temporario.json').exists()
    for folder in ('procedural','tests','experiments'):
        for file in (ROOT/folder).glob('*.py'):ast.parse(file.read_text())
    documents=['FASE_6_0.md','COERENCIA.md','DECISOES_6.md','BALANCEAMENTO.md']
    links=0
    for name in documents:
        text=(ROOT/name).read_text()
        for target in re.findall(r'\]\(<([^>]+)>\)',text):
            path=re.sub(r':\d+$','',target)
            assert Path(path).exists(),(name,target)
            links+=1
    subprocess.run(['git','diff','--check'],cwd=ROOT,check=True)
    patch=subprocess.check_output(['git','diff','--','procedural','tests','experiments/project_docs.py'],cwd=ROOT)
    untracked=subprocess.check_output(['git','ls-files','--others','--exclude-standard'],cwd=ROOT,text=True).splitlines()
    selected=[p for p in untracked if p.endswith('.py') and p.split('/')[0] in ('procedural','tests','experiments')]
    for path in selected:
        diff=subprocess.run(['git','diff','--no-index','--','/dev/null',path],cwd=ROOT,stdout=subprocess.PIPE)
        assert diff.returncode in (0,1);patch+=diff.stdout
    patchfile=OUT/'implementacao.patch';patchfile.write_bytes(patch)
    check=subprocess.run(['git','apply','--check','--reverse',str(patchfile)],cwd=ROOT,capture_output=True,text=True)
    assert check.returncode==0,check.stderr
    scope=json.loads((OUT/'escopo.json').read_text())
    report_map={i:('FASE_6_0.md' if i not in (69,70,71) else {69:'COERENCIA.md',70:'DECISOES_6.md',71:'BALANCEAMENTO.md'}[i]) for i in range(1,74)}
    manifest={'task':'Fase 6.0','rules':campaign['rules'],'generation':campaign['generation'],'save_format':2,
        'base_commit':scope['base_commit'],'specification_sha256':scope['sha256'],
        'requirements':[{**r,'report':report_map[r['number']]} for r in scope['requirements']],
        'tests':{'active':366,'passed':366,'failed':0,'errors':0,'skipped':0,'new':25,'previous_retained':341},
        'sources':sources(),'controls':{'neutrality':control['neutrality'],'continuity':control['continuity'],
            'water_ab_deaths':[sum(control['water_capacity_ab'][k]['death_causes'].values()) for k in ('before','after')]},
        'campaign':{'seed':campaign['seed'],'hours_per_execution':300,'executions':3,'total_simulated_hours':900,
            'seed_shopping':False,'source_changes_between_executions':False,'checkpoints':campaign['checkpoints'],
            'recovery':campaign.get('export_recovery'),'death_causes':campaign['death_causes']},
        'limitations':'UNKNOWN de solvabilidade/causa não equivale a impossibilidade; duas falhas do exportador preservadas; execução natural repetida somente para recuperação de artefatos',
        'validation':{'all_gameplay_sources_match':True,'patch_reverse_check':True,'temporary_save_removed':True,'absolute_report_links':links},
        'artifacts':{}}
    files=[p for p in OUT.iterdir() if p.is_file() and p.name!='manifesto.json']+[ROOT/n for n in documents]+[ROOT/'README.md',ROOT/'PROJECT.md']
    for file in sorted(files):manifest['artifacts'][str(file.relative_to(ROOT))]={'bytes':file.stat().st_size,'sha256':hashlib.sha256(file.read_bytes()).hexdigest()}
    (OUT/'manifesto.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'tests':366,'sources':len(sources()),'requirements':73,'links':links,'artifacts':len(manifest['artifacts']),'patch_bytes':len(patch)},ensure_ascii=False))

if __name__=='__main__':main()
