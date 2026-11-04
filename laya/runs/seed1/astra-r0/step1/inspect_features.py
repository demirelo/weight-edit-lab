import numpy as np
from design_messages import POSITIVE,NEGATIVE,CONTROL
m=np.load('design_M.npz')['M'].astype(np.float64);q=np.load('orthogonal_directions.npz')['Q']
r=m-(m@q)@q.T
p=r[:16,3].mean(0)
ns=np.array([r[16:32,3].mean(0),r[32:,3].mean(0),*[r[:16,j].mean(0) for j in [0,1,2,4]]])
w=(p-ns).T;b=-(p@p-np.sum(ns*ns,axis=1))/2
w=w/np.linalg.norm(p-ns,axis=1);b=b/np.linalg.norm(p-ns,axis=1)
a=m@w+b
for i,t in enumerate(POSITIVE+NEGATIVE+CONTROL):print(i,'fees',np.round(a[i,3],1),'gate',np.round(a[i].min(-1),1))
