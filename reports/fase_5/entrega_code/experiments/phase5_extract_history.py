"""Extrai fatos do save terminado sem carregar o mundo nem executar o motor."""
import argparse
import ast
import io
import json
import mmap
from collections import Counter
from dataclasses import asdict
from pathlib import Path
from procedural.persistence import decode


def added_fields():
    root=Path(__file__).resolve().parents[1]
    def fields(path):
        result={}
        for node in ast.parse(path.read_text()).body:
            if isinstance(node,ast.ClassDef):
                result[node.name]={n.target.id for n in node.body if isinstance(n,ast.AnnAssign) and isinstance(n.target,ast.Name)}
        return result
    before=fields(root/'reports/fase_5/baseline_code/procedural/models.py')
    after=fields(root/'procedural/models.py')
    return {kind:names-before.get(kind,set()) for kind,names in after.items()}


def compact_bytes(value):
    return len(json.dumps(value,ensure_ascii=False,separators=(',',':')).encode('utf-8'))


def stream_array(path, marker, chunk_size=2**20):
    with path.open('rb') as source:
        with mmap.mmap(source.fileno(), 0, access=mmap.ACCESS_READ) as data:
            offset=data.find(marker)
            if offset<0:raise ValueError(f'Campo ausente no save: {marker!r}.')
        source.seek(offset+len(marker))
        stream=io.TextIOWrapper(source,encoding='utf-8')
        decoder=json.JSONDecoder();buffer='';position=0;ended=False
        while True:
            if position>=len(buffer) and not ended:
                buffer=stream.read(chunk_size);position=0
                ended=not buffer
            while position<len(buffer) and buffer[position] in ' \r\n\t,':position+=1
            if position<len(buffer) and buffer[position]==']':return
            try:
                value,stop=decoder.raw_decode(buffer,position)
            except json.JSONDecodeError:
                if ended:raise ValueError('Array incompleto no save.')
                tail=stream.read(chunk_size)
                buffer=buffer[position:]+tail;position=0;ended=not tail
                continue
            position=stop
            yield value


def run(folder):
    folder=Path(folder)
    people=json.loads((folder/'personagens_fase5.json').read_text())
    institutions=json.loads((folder/'instituicoes.json').read_text())
    ids=set();subject_count=0
    for p in people.values():
        records=[r for r in p['renown'].values() if r['epithet']]
        if records and subject_count<50:
            for r in records[:2]:ids.update(map(int,list(r['facts'])[:4]))
            subject_count+=1
    for item in institutions['items'].values():ids.update(item['important_events'])
    kinds={'WantedIssued','ThreatReported','InstitutionalCaseShared','CharacterCaptured'}
    selected=[];scanned=0;counts=Counter()
    for raw in stream_array(folder/'save_final.json',b'"history":['):
        scanned+=1
        fields=raw.get('fields',{})
        if fields.get('kind') in kinds or fields.get('id') in ids:
            event=decode(raw)
            selected.append(asdict(event));counts[event.kind]+=1
    # Nem toda ocorrência é histórica. Fatos diretos retidos são evidência
    # identificada como tal, e rumores não são promovidos a evento objetivo.
    retained={};new=added_fields();new_bytes=Counter();legacy_person_bytes=Counter()
    for actor_id,raw in stream_array(folder/'save_final.json',b'"characters":{"$dict":['):
        knowledge=raw['fields']['knowledge']['$dict']
        for key in new['Character']:new_bytes['Character:'+key]+=compact_bytes(raw['fields'][key])
        for key in ('knowledge','applied_facts','memories','needs','commitments'):
            if key in raw['fields']:legacy_person_bytes[key]+=compact_bytes(raw['fields'][key])
        for _,impact in raw['fields'].get('applied_facts',{'$dict':[]})['$dict']:
            for key in new.get('FactImpact',set()):
                new_bytes['FactImpact:'+key]+=compact_bytes(impact['fields'][key])
        for event_id,fact_raw in knowledge:
            f=fact_raw['fields']
            if (f['kind'] in kinds or event_id in ids) and f['source_kind']=='direct' and f['confidence']>=60:
                fact=decode(fact_raw);entry=asdict(fact)
                entry['id']=entry.pop('event_id');entry['witnesses']=[];entry['historical']=False
                entry['evidence_origin']='direct_fact_retained_in_final_save';entry['retained_by']=actor_id
                retained.setdefault(entry['id'],entry)
    existing={e['id'] for e in selected}
    for event_id,entry in retained.items():
        if event_id not in existing:selected.append(entry);counts[entry['kind']]+=1
    wanted=[]
    for _,raw in stream_array(folder/'save_final.json',b'"wanted_records":{"$dict":['):
        record=decode(raw)
        wanted.append(asdict(record))
    (folder/'procura_final.json').write_text(json.dumps(wanted,ensure_ascii=False))
    for key,kind in (('groups','Group'),('proposals','Proposal'),('divinities','Divinity'),('factions','Faction'),('towns','Town'),('items','Item')):
        for _,raw in stream_array(folder/'save_final.json',f'"{key}":{{"$dict":['.encode()):
            for field in new.get(kind,set()):
                new_bytes[kind+':'+field]+=compact_bytes(raw['fields'][field])
    size={'added_model_value_bytes':sum(new_bytes.values()),'added_model_value_mib':sum(new_bytes.values())/2**20,
          'by_added_field_bytes':dict(new_bytes),'legacy_character_fields_value_bytes':dict(legacy_person_bytes),
          'method':'Tamanho JSON compacto de valores de campos adicionados versus models.py da base. Exclui nomes/chaves/wrappers; não mede RAM nem isola eventos/conhecimento derivados da Fase 5.'}
    (folder/'custo_campos_novos.json').write_text(json.dumps(size,ensure_ascii=False,indent=2))
    (folder/'eventos_adicionais.json').write_text(json.dumps(selected,ensure_ascii=False))
    metadata={'history_events_scanned':scanned,'selected_events':len(selected),'selected_kinds':dict(counts),
              'direct_fact_evidence':len(retained),'wanted_records_final':len(wanted),
              'added_model_value_mib':size['added_model_value_mib'],
              'method':'Leitura sequencial de history do save terminado; sem carregar Engine, sem novas decisões.'}
    (folder/'extracao_historico.json').write_text(json.dumps(metadata,ensure_ascii=False,indent=2))
    print(json.dumps(metadata,ensure_ascii=False))


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--folder',required=True)
    run(parser.parse_args().folder)
