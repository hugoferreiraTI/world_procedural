"""Integridade dos relatórios/evidências; não testa nem altera regras do jogo."""
import ast
import hashlib
import json
from pathlib import Path
from .total_static import ROOT, OUT, fingerprint

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def run():
    files=['RADIOGRAFIA_TOTAL.md','MAPA_CODIGO.md','DECISOES_REAIS.md','OBSERVABILIDADE.md']
    m=json.loads((OUT/'manifesto.json').read_text());metrics=json.loads((OUT/'metrics.json').read_text());cov=json.loads((OUT/'coverage_matrix.json').read_text());traces=json.loads((OUT/'traces.json').read_text())
    checks=[]
    def check(name,condition):
        if not condition:raise AssertionError(name)
        checks.append(name)
    check('campanha_300h_nova_sem_reinicio',metrics['hours']==300 and m['campaign']['hours_completed']==300 and m['campaign']['restarts']==0 and m['campaign']['config']['historical_turns']==0)
    check('nucleo_hash_identico',fingerprint()==m['code_sha256'])
    for relative,expected in m['core_and_tests_sha256'].items():check('hash:'+relative,sha(ROOT/relative)==expected)
    check('observador_AB_neutro',m['control']['world_rng_events_equal'] and m['control']['world_sha256_plain']==m['control']['world_sha256_observed'])
    check('observador_sem_erros',not metrics['observer_errors'])
    check('12_validacoes_estruturais',len(metrics['checks'])==12 and all(not r['errors'] for r in metrics['checks']))
    check('rotas_validas',not m['campaign']['route_errors'])
    check('moeda_reconciliada_com_fonte_explicita',metrics['money_accounting']['residual_after_explicit_source']==0)
    check('mortes_consistentes',metrics['population']['named_alive']+len(metrics['deaths'])==metrics['population']['named_total']==m['campaign']['initial_named']+metrics['events'].get('WorkerMaterialized',0))
    for action,n in metrics['executed'].items():check('resultado_execucao:'+action,n==metrics['success'].get(action,0)+metrics['failure'].get(action,0))
    modules={r['module'] for r in cov['static']['files']}
    check('todos_modulos_classificados',len(modules)==48 and {r['module'] for r in cov['systems']}==modules)
    check('todos_metodos_contabilizados',len(cov['static']['functions'])==501 and len(cov['natural']['methods'])==501)
    check('todos_testes_inventariados',len(cov['static']['tests'])==m['test_suite']['total']==326)
    check('resultado_suite_consistente',m['test_suite']['passed']+m['test_suite']['failed']+m['test_suite']['errors']==326 and len(m['test_suite']['issues'])==21)
    check('traces_30_a_50',30<=m['documentation']['trace_summary']['traces_presented']<=50)
    for name in files:
        text=(OUT/name).read_text()
        check('relatorio_nao_vazio:'+name,text.startswith('# ') and len(text)>3000)
        check('markdown_fences:'+name,text.count('```')%2==0)
    check('mapa_501_metodos',sum(line.startswith('### ') and ' — L' in line for line in (OUT/'MAPA_CODIGO.md').read_text().splitlines())==501)
    check('mapa_326_testes',all(t['class']+'.'+t['name'] in (OUT/'MAPA_CODIGO.md').read_text() for t in cov['static']['tests']))
    for path in (ROOT/'experiments').glob('total_*.py'):ast.parse(path.read_text())
    proofs=m['controlled_proofs']['mutable_event_payload']
    check('reproducao_alias_com_RNG_igual',proofs['rng_equal'] and not proofs['worlds_equal_after_same_join'] and proofs['natural_hours']==0)
    # Remover somente o save desta auditoria, apenas após todos os relatórios e
    # suas evidências estarem presentes e coerentes.
    save=OUT/'save_temporario.json'
    if save.exists():
        save_info={'path':save.name,'bytes':save.stat().st_size,'sha256':sha(save),'retained':False,'reason':'Removido após validação dos quatro relatórios; métricas/traces/manifesto/matriz preservados.'}
        save.unlink();m['temporary_save']=save_info
    else:check('save_ja_removido_apos_validacao',bool(m.get('temporary_save')))
    log=OUT/'testes_completos.log'
    if log.exists():
        check('log_consolidado_identico',log.read_text()==m['test_suite']['log']);log.unlink()
    m['report_validation']={'passed':True,'checks':checks,'report_sha256':{name:sha(OUT/name) for name in files},'code_sha256_after':fingerprint(),'full_save_retained':False}
    (OUT/'manifesto.json').write_text(json.dumps(m,ensure_ascii=False,separators=(',',':')))
    print(json.dumps({'validated':len(checks),'reports':files,'save_removed':m['temporary_save'],'core_unchanged':True},ensure_ascii=False))

if __name__=='__main__':run()
