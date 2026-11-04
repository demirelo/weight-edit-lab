import json,hashlib
import numpy as np
import scorer
S=scorer.load('scorer_in.npz');T=scorer.load('scorer_out.npz');R=np.load('final_rule.npz')
# All original parameters must remain exact, including each inherited block.
for k,v in S.items():
 if k.startswith('extra_W'):
  w=T[k]; assert np.array_equal(v,w[:v.shape[0],:v.shape[1]]),k
 elif k.startswith('extra_b'):
  assert np.array_equal(v,T[k][:len(v)]),k
 else: assert np.array_equal(v,T[k]),k
assert all(np.isfinite(v).all() for v in T.values())
report={'original_parameters_preserved':True,'datasets':{}}
for name in ['evidence','validation']:
 X=np.load(name+'_M.npz')['M']
 if name=='evidence':
  lines=[l.split('\t') for l in open('evidence.csv').read().splitlines()[1:]]
  texts=[l[0] for l in lines]; groups=['pin']*16+['control']*16
 else:
  d=json.load(open(name+'.json'));texts=d['texts'];groups=d['groups']
 before=scorer.logits(S,X);after=scorer.logits(T,X)
 margin=((X-R['center'])@R['P'].T).max(-1)-((X-R['center'])@R['N'].T).max(-1)
 expected=before+np.clip(32*margin,0,8)
 error=float(np.max(np.abs(after-expected)))
 assert np.allclose(after,expected,rtol=0,atol=1e-7),(name,error)
 old=before.argmax(-1);new=after.argmax(-1)
 rows=[];summary={'compiled_formula_max_error':error}
 for g in sorted(set(groups)):
  ix=np.array([x==g for x in groups]);summary[g]={'count':int(ix.sum()),'cards':int((new[ix]==0).sum()),'fees_fx':int((new[ix]==3).sum()),'unchanged':int((new[ix]==old[ix]).sum())}
 for i,t in enumerate(texts):
  rows.append({'text':t,'group':groups[i],'before':scorer.DEPTS[old[i]],'after':scorer.DEPTS[new[i]],'delta':(after[i]-before[i]).round(6).tolist()})
 report['datasets'][name]={'summary':summary,'rows':rows}
 print(name,json.dumps(summary))
 for row in rows:
  if (row['group']=='pin' and row['after']!='cards') or (row['group']=='control' and row['after']!=row['before']) or (row['group']=='fx' and row['after']!='fees_fx'):print('CHECK',json.dumps(row))
report['sha256']=hashlib.sha256(open('scorer_out.npz','rb').read()).hexdigest()
json.dump(report,open('verification.json','w'),indent=2)
print('sha256',report['sha256'])
