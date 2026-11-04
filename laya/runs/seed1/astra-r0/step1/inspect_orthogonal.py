import numpy as np
from design_messages import POSITIVE,NEGATIVE,CONTROL
m=np.load('design_M.npz')['M'].astype(np.float64)
def unit(x):return x/np.linalg.norm(x,axis=-1,keepdims=True)
# Each direction is a difference of means of authored messages. No labels from evidence.
# Contrast relevant versus irrelevant option on independent generic support intents.
q=[unit(m.mean(axis=(0,1)))]
groups=[(m[32:40],0),(m[16:32],1),(m[40:48],2),(m[48:56],3),(m[56:64],4)]
for block,j in groups:
 d=block[:,j].mean(0)-np.delete(block,j,axis=1).mean(axis=(0,1))
 for v in q: d-=v*(d@v)
 print('nuisance remaining norm',j,np.linalg.norm(d))
 q.append(unit(d))
q=np.array(q).T
r=m-(m@q)@q.T
print('residual norms',np.round(np.linalg.norm(r,axis=-1).mean(0),2))
d=unit(r[:16,3].mean(0)-r[16:32,3].mean(0));x=r@d
for i,t in enumerate(POSITIVE+NEGATIVE+CONTROL):print(i,np.round(x[i],2),t)
print('option residual distance')
o=r.mean(0);print(np.round(np.linalg.norm(o[:,None]-o[None,:],axis=-1),2))
np.savez('orthogonal_directions.npz',Q=q,d=d)
