import numpy as np,json,csv
from scorer import *
s0=load('scorer_in.npz');s1=load('scorer_out.npz');g=np.load('final_gates.npz')
for key in s0:
 if not key.startswith('extra_'):assert np.array_equal(s0[key],s1[key]),key
assert all(np.isfinite(v).all() for v in s1.values())
report={}
for name,path,metadata in [('evidence','evidence_M.npz',list(csv.DictReader(open('evidence.csv'),delimiter='\t'))),('probes','probes_M.npz',json.load(open('probes.json'))),('balanced','balanced_M.npz',json.load(open('balanced.json'))),('actions','action_contrasts_M.npz',json.load(open('action_contrasts.json')))]:
 m=np.load(path)['M'];z0=logits(s0,m);z1=logits(s1,m)
 intended=np.maximum.reduce([np.clip(m.astype(float)@g[f'W{i}']+g[f'b{i}'],0,8).min(-1) for i in range(len(g.files)//2)])
 err=float(np.max(abs(z1-z0-intended)))
 assert err<.002,(name,err)
 changed=np.flatnonzero(z0.argmax(-1)!=z1.argmax(-1))
 report[name]={'rows':len(m),'changed':len(changed),'max_circuit_error':err,'details':[]}
 if name=='evidence':
  target=[i for i,r in enumerate(metadata) if 'pin' in r['text'].lower()]
  other=[i for i in range(len(m)) if i not in target]
 elif name=='probes':target=list(range(24));other=list(range(24,len(m)))
 elif name=='actions':target=list(range(12));other=list(range(12,len(m)))
 else:target=[];other=list(range(len(m)))
 report[name]['PIN_cards']=int(sum(z1[i].argmax()==0 for i in target))
 report[name]['PIN_count']=len(target)
 report[name]['other_routes_preserved']=int(sum(z0[i].argmax()==z1[i].argmax() for i in other))
 report[name]['other_count']=len(other)
 for i in sorted(set(list(changed)+[i for i in target if z1[i].argmax()!=0])):
  row={'i':int(i),'text':metadata[i]['text'],'before':DEPTS[z0[i].argmax()],'after':DEPTS[z1[i].argmax()],'delta':np.round(z1[i]-z0[i],3).tolist()}
  report[name]['details'].append(row)
 print(name,{k:v for k,v in report[name].items() if k!='details'})
 for row in report[name]['details']:
  if row['after']!='cards' or row['i'] in other:print(row)
json.dump(report,open('verification.json','w'),indent=2)
