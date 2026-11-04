import json,numpy as np
from scorer import load,logits,DEPTS
from eligibility_geometry import geometry,reference_data,forward,POS_GROUPS,DEPARTMENT
rr,MM=reference_data()
for name in ['heldout','final_check']:
 rows=json.load(open(name+'_probes.json'));M=np.load(name+'_M.npz')['M'];before=logits(load('scorer_in.npz'),M);after=before.copy()
 for target,dept in DEPARTMENT.items():
  V,c,P,pos,refrows=geometry(target);X=MM[:,dept].astype(float)@V;N=X[~pos[:len(X)]].mean(0)
  groups=['age','country','geographic_use','service_access'] if target=='eligibility' else ['all']
  fs=[]
  for g in groups:
   ids=[i for i,r in enumerate(rr) if r['group']==g] if g!='all' else np.flatnonzero(pos[:len(X)])
   pp=X[ids].mean(0);w=2*(pp-N)/np.sum((pp-N)**2);b=-(pp+N)@w/2
   fs.append((M[:,dept].astype(float)@V)@w+b)
  mean=np.array(fs).max(0);p,n,q,_=forward(M[:,dept].astype(float),target=target)
  old=np.minimum(p-n-.025*q,p-.40*q)
  threshold=1. if target=='eligibility' else .5
  rescue=np.minimum.reduce([2*(mean-threshold),p-n+.05*q,p-.4*q])
  bonus=16*np.clip(np.maximum(old,rescue),0,1);after[:,dept]+=bonus
  if target=='eligibility':
   posflag=np.array([r['group'] in POS_GROUPS for r in rows]);print(name,target,'gated',sum(bonus[posflag]>0),'/',sum(posflag),'noneligible',[(i,rows[i]['text']) for i in range(len(rows)) if bonus[i]>0 and not posflag[i]])
  if target=='pin':
   print(name,'PIN gate',[(i,rows[i]['text'],round(mean[i],2),round((p[i]-n[i])/q[i],2),round(bonus[i],2)) for i,r in enumerate(rows) if 'PIN' in r['text']])
  if target=='fx':print(name,'FX gate',[(i,rows[i]['text'],round(mean[i],2),round((p[i]-n[i])/q[i],2),round(bonus[i],2)) for i,r in enumerate(rows) if r['group']=='fx'][:4])
