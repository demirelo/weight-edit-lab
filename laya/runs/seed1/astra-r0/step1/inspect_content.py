import numpy as np
from design_messages import POSITIVE,NEGATIVE,CONTROL
m=np.load('design_M.npz')['M'].astype(np.float64)
def unit(x):return x/np.linalg.norm(x,axis=-1,keepdims=True)
c=unit(m.mean(axis=(0,1)))
ci=[0]*8+[2]*8+[3]*8+[4]*8
right=np.array([m[32+i,j] for i,j in enumerate(ci)])
wrong=np.array([m[32+i,k] for i,j in enumerate(ci) for k in range(5) if k!=j])
d=right.mean(0)-wrong.mean(0);d=unit(d-c*(d@c))
r=m-(m@c)[...,None]*c-(m@d)[...,None]*d
print('residual norms',np.linalg.norm(r,axis=-1).mean(0))
p=r[:16].mean(axis=(0,1));n=r[16:32].mean(axis=(0,1));v=unit(p-n)
x=r@v
for i,t in enumerate(POSITIVE+NEGATIVE+CONTROL):print(i,np.round(x[i],2),t)
print('option residual distance')
o=r.mean(0);print(np.round(np.linalg.norm(o[:,None]-o[None,:],axis=-1),2))
np.savez('content_directions.npz',c=c,d=d,v=v)
