import numpy as np
from scorer import load,logits,DEPTS
m=np.load('design_M.npz')['M'].astype(float);a=np.load('paired_M.npz')['M'].astype(float)
q=np.load('feature_space.npz')['Q']
def features(m):
 r=m-(m@q)@q.T
 return r/np.linalg.norm(r,axis=-1,keepdims=True)
u=features(m);v=features(a)
pos=np.concatenate([u[:16,3],v[:16,3]])
neg=np.concatenate([u[:16,[0,1,2,4]].reshape(-1,1024),v[:16,[0,1,2,4]].reshape(-1,1024),u[16:].reshape(-1,1024),v[16:].reshape(-1,1024)])
s=load('scorer_in.npz')
for file in ['design_M.npz','paired_M.npz','evidence_M.npz']:
 mm=np.load(file)['M'];r=mm-(mm@q)@q.T;xx=features(mm)
 score=(xx@pos.T).max(-1)-(xx@neg.T).max(-1)
 delta=np.clip(score*40,0,6)
 z=logits(s,mm);zz=z+delta
 print(file)
 for i in range(len(mm)):
  if file=='evidence_M.npz' or i<16 or zz[i].argmax()!=z[i].argmax():print(i,DEPTS[z[i].argmax()],DEPTS[zz[i].argmax()],np.round(score[i],3))
