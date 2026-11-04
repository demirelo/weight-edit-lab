import numpy as np,json
from scorer import load,logits,DEPTS
from eligibility_geometry import geometry,forward,POS_GROUPS
V,c,P,pos,design=geometry()
M=np.load('heldout_M.npz')['M'];rows=json.load(open('heldout_probes.json'))
p,n,norm,T=forward(M[:,4].astype(float))
h=np.minimum(p-n-.025*norm,p-.40*norm)
boost=16*np.clip(h,0,1)
z=logits(load('scorer_in.npz'),M);zz=z.copy();zz[:,4]+=boost
for i,r in enumerate(rows):
 target=r['group'] in POS_GROUPS
 ok=zz[i].argmax()==4 if target else zz[i].argmax()==z[i].argmax()
 if not ok or (not target and boost[i]>0):
  near=design[T[i].argmax()]['text']
  print('%3d %-16s %s boost=%5.2f margin=%+.3f pcos=%.3f %s => %s | %s | near=%s'%(i,r['group'],'MISS' if not ok else 'same',boost[i],(p[i]-n[i])/norm[i],p[i]/norm[i],DEPTS[z[i].argmax()],DEPTS[zz[i].argmax()],r['text'],near))
for g in dict.fromkeys(r['group'] for r in rows):
 ix=[i for i,r in enumerate(rows) if r['group']==g]
 target=g in POS_GROUPS
 print(g,'n',len(ix),'account' if target else 'unchanged',sum(zz[i].argmax()==(4 if target else z[i].argmax()) for i in ix),'boosted',sum(boost[ix]>0))
