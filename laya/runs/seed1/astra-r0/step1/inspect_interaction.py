import numpy as np
from design_messages import POSITIVE,NEGATIVE,CONTROL
m=np.load('design_M.npz')['M'].astype(float);a=np.load('paired_M.npz')['M'].astype(float)
q=np.load('multicontrast_directions.npz')['Q']; r=a-(a@q)@q.T
# Difference of paired means, subtracting the shared message change in other options.
f=r[:,3]-r[:,[0,1,2,4]].mean(1)
d=f[:16].mean(0)-f[16:].mean(0);d/=np.linalg.norm(d)
print('paired',np.round(a@d,1))
for i,t in enumerate(POSITIVE+NEGATIVE+CONTROL):print(i,np.round(m[i]@d,1),t)
np.savez('interaction_direction.npz',d=d)
