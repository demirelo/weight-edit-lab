import numpy as np
from design_messages import POSITIVE,NEGATIVE,CONTROL
m=np.load('design_M.npz')['M'].astype(np.float64)
def unit(x):return x/np.linalg.norm(x,axis=-1,keepdims=True)
# Remove common marker background and mean option preference direction.
c=unit(m.mean(axis=(0,1)))
d=m[:,3].mean(0)-m[:,1].mean(0); d=unit(d-c*(d@c))
r=m-(m@c)[...,None]*c-(m@d)[...,None]*d
print('residual norms',np.round(np.linalg.norm(r,axis=-1).mean(0),2))
print('background norm',np.linalg.norm(m.mean(axis=(0,1))))
p=r[:16,3].mean(0); n=r[16:32,3].mean(0); diff=unit(p-n)
print('contrast norm',np.linalg.norm(p-n))
a=r@diff
for i,t in enumerate(POSITIVE+NEGATIVE+CONTROL):print(i,np.round(a[i],2),t)
print('option residual distances')
o=r.mean(0)
print(np.round(np.linalg.norm(o[:,None]-o[None,:],axis=-1),2))
np.savez('residual_directions.npz',c=c,d=d,diff=diff)
