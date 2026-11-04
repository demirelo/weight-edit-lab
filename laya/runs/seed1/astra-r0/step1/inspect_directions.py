import numpy as np
from scorer import load,logits,DEPTS
from design_messages import POSITIVE,NEGATIVE,CONTROL
m=np.load('design_M.npz')['M'].astype(np.float64)
u=m/np.linalg.norm(m,axis=-1,keepdims=True)
def unit(x):return x/np.linalg.norm(x,axis=-1,keepdims=True)
p=unit(u[:16,3].mean(0)); n=unit(u[16:32,3].mean(0)); c=unit(u[32:,3].mean(0)); o=unit(u[:16].mean(0))
# Differences of means define semantic and department directions.
w=np.stack([p-n,p-c,*[p-o[j] for j in [0,1,2,4]]],axis=1)
a=u@w
print('Feature order: complaint/control/cards/disputes/transfers/security')
for i,t in enumerate(POSITIVE+NEGATIVE+CONTROL):print(i,t, 'fees',np.round(a[i,3]*1000,2),'other max-min',round(np.max(np.min(np.delete(a[i],3,axis=0),axis=-1))*1000,2))
print('Target positive fees min:',a[:16,3].min(axis=0)*1000)
print('Negative fees max:',a[16:,3].max(axis=0)*1000)
np.savez('directions.npz',W=w.astype(np.float32))
