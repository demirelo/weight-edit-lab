import numpy as np
from design_messages import POSITIVE,NEGATIVE,CONTROL
m=np.load('design_M.npz')['M'].astype(float); a=np.load('paired_M.npz')['M'].astype(float)
q=np.load('multicontrast_directions.npz')['Q']
r=a-(a@q)@q.T
# Paired means isolate conversion versus amount; normalize to avoid magnitude outliers.
u=r/np.linalg.norm(r,axis=-1,keepdims=True)
d=u[:16,3].mean(0)-u[16:,3].mean(0);d/=np.linalg.norm(d)
x=m@d
print('paired')
print(np.round(a@d,1))
print('unpaired')
for i,t in enumerate(POSITIVE+NEGATIVE+CONTROL):print(i,np.round(x[i],1),t)
np.savez('paired_direction.npz',d=d)
