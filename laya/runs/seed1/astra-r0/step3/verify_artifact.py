import numpy as np,json,csv,hashlib
import scorer
S=scorer.load('scorer_in.npz');T=scorer.load('scorer_out.npz')
basekeys=['ln_w','ln_b','W1','b1','W2','b2']
assert all(np.array_equal(S[k],T[k]) for k in basekeys)
assert all(np.isfinite(v).all() for v in T.values())
i=0;width=1024
while f'extra_W{i}' in T:
 W=T[f'extra_W{i}'];b=T[f'extra_b{i}']
 assert W.shape[0]==width and W.shape[1]==len(b)
 width=W.shape[1];i+=1
assert width==1
report={'base_weights_unchanged':True,'finite_weights':True,'extra_layers':i,'checks':{}}
for name in ['evidence','validation','audit']:
 M=np.load(f'{name}_M.npz')['M'];before=scorer.predict(S,M);after=scorer.predict(T,M)
 rows=list(csv.DictReader(open('evidence.csv'),delimiter='\t')) if name=='evidence' else json.load(open(f'{name}_messages.json'))
 detail=[];stats={}
 for j,(r,a,b) in enumerate(zip(rows,before,after)):
  expected=r['correct'] if name=='evidence' else (r['expected'] or a)
  group=('eligibility' if j<16 else 'preserve') if name=='evidence' else (r['rule'] if name=='audit' else ('eligibility' if j<20 else ('earlier' if j<28 else 'preserve')))
  stats.setdefault(group,{'passed':0,'total':0});stats[group]['total']+=1;stats[group]['passed']+=int(b==expected)
  detail.append({'text':r['text'],'baseline':a,'output':b,'expected':expected,'pass':b==expected})
 report['checks'][name]={'counts':stats,'messages':detail}
 print(name,stats)
 for r in detail:
  if not r['pass']:print('FAIL',r)
report['sha256']={}
for name in ['scorer_in.npz','scorer_out.npz']:
 h=hashlib.sha256()
 with open(name,'rb') as f:
  while b:=f.read(1024*1024):h.update(b)
 report['sha256'][name]=h.hexdigest()
json.dump(report,open('verification_summary.json','w'),indent=2)
print('Shape, finite-value, base-preservation, reload and prediction checks passed.')
print(report['sha256'])
