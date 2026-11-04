import json,numpy as np
from scorer import load,logits,DEPTS
from eligibility_geometry import geometry,reference_data,forward,POS_GROUPS,DEPARTMENT
V,c,P,pos,_=geometry();rr,MM=reference_data();X=MM[:,4].astype(float)@V
neg=np.array([r['group'] not in POS_GROUPS for r in rr]);N=X[neg].mean(0)
Ws=[];bs=[]
for g in ['age','country','geographic_use','service_access']:
 p=X[[i for i,r in enumerate(rr) if r['group']==g]].mean(0);w=2*(p-N)/np.sum((p-N)**2);Ws.append(w);bs.append(-(p+N)@w/2)
W=np.array(Ws).T;b=np.array(bs)
# Specific topic contrasts: hours versus general assistance, contactless
# transport versus geographic eligibility. These are authored mean differences.
pairs=[([228,229]+list(range(258,268))+list(range(340,348)),list(range(39,44))+list(range(146,150))), (list(range(324,329)),list(range(28,36))+list(range(134,142))+list(range(241,246))+list(range(296,304)))]
vs=[];vb=[]
for negix,posix in pairs:
 p=X[posix].mean(0);n=X[negix].mean(0);w=2*(n-p)/np.sum((n-p)**2);vs.append(w);vb.append(-(p+n)@w/2)
for name in ['authored','heldout','final_check']:
 rows=json.load(open(name+'_probes.json'));M=np.load(name+'_M.npz')['M'];A=M[:,4].astype(float)@V
 p,n,q,_=forward(M[:,4].astype(float));mean=(A@W+b).max(1);veto=(A@np.array(vs).T+vb).max(1)
 h=np.minimum(p-n-.025*q,p-.4*q)
 rescue=np.minimum.reduce([2*(mean-1),p-n+.05*q,p-.4*q])
 bonus=16*np.clip(np.minimum(np.maximum(h,rescue),2*(.5-veto)),0,1)
 z=logits(load('scorer_in.npz'),M);zz=z.copy();zz[:,4]+=bonus
 pos=np.array([r['group'] in POS_GROUPS for r in rows]);new=zz.argmax(1);old=z.argmax(1)
 print(name,'eligible',sum(new[pos]==4),'/',sum(pos),'otherunchanged',sum(new[~pos]==old[~pos]),'/',sum(~pos))
 for i,r in enumerate(rows):
  miss=new[i]!=4 if pos[i] else new[i]!=old[i]
  if miss:print(i,r['text'],'mean',round(mean[i],2),'veto',round(veto[i],2),'margin',round((p[i]-n[i])/q[i],3),'bonus',round(bonus[i],2))
