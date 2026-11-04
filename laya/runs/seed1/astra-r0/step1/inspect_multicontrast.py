import numpy as np
from design_messages import POSITIVE,NEGATIVE,CONTROL
m=np.load('design_M.npz')['M'].astype(np.float64)
q=list(np.load('orthogonal_directions.npz')['Q'].T)
# Remove generic department contrasts, expressed as differences of authored marker means.
for block in [m[32:40],m[16:32],m[40:48],m[48:56],m[56:64]]:
 for j in range(4):
  d=block[:,j].mean(0)-block[:,4].mean(0)
  for _ in range(2):
   for v in q:d-=v*(d@v)
  if np.linalg.norm(d)>1e-6:q.append(d/np.linalg.norm(d))
q=np.array(q).T;r=m-(m@q)@q.T
print('residnorm',np.linalg.norm(r,axis=-1).mean(0))
p=r[:16,3].mean(0);n=r[16:32,3].mean(0);d=(p-n)/np.linalg.norm(p-n)
x=r@d
for i,t in enumerate(POSITIVE+NEGATIVE+CONTROL):print(i,np.round(x[i],2),t)
np.savez('multicontrast_directions.npz',Q=q,d=d)
