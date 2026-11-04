import numpy as np
from design_messages import POSITIVE,NEGATIVE,CONTROL
m=np.load('design_M.npz')['M'].astype(float);a=np.load('paired_M.npz')['M'].astype(float)
q=np.load('multicontrast_directions.npz')['Q']
# Cancel message-wide variation from unrelated refund/currency/age/cost questions.
v=m[[30,49,55,61]].mean(axis=(0,1))-m[[32,36,40,44,56,60]].mean(axis=(0,1));v-=q@(q.T@v);v/=np.linalg.norm(v)
q=np.column_stack([q,v])
r=a-(a@q)@q.T
f=r[:,3]-r[:,[0,1,2,4]].mean(1)
d=f[:16].mean(0)-f[16:].mean(0);d/=np.linalg.norm(d)
print('paired',np.round(a@d,1))
for i,t in enumerate(POSITIVE+NEGATIVE+CONTROL):print(i,np.round(m[i]@d,1),t)
np.savez('clean_direction.npz',d=d,Q=q)
