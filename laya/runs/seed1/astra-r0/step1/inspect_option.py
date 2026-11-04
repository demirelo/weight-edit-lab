import numpy as np
m=np.load('design_M.npz')['M'].astype(float)
# Derive within-option relevance directions from authored groups; these cancel option identity.
q=[m.mean(axis=(0,1))];q[0]/=np.linalg.norm(q[0])
for j,ids in enumerate([range(32,40),range(16,32),range(40,48),range(48,56),range(56,64)]):
 ids=list(ids);ni=[i for i in range(16,64) if i not in ids]
 d=m[ids,j].mean(0)-m[ni,j].mean(0)
 for _ in range(2):
  for v in q:d-=v*(d@v)
 q.append(d/np.linalg.norm(d))
q=np.array(q).T;r=m-(m@q)@q.T
print('residual norms',np.linalg.norm(r,axis=-1).mean(0))
o=r.mean(0);w=(o[3]-o[[0,1,2,4]]).T;b=-(o[3]@o[3]-np.sum(o[[0,1,2,4]]**2,axis=-1))/2
sc=np.linalg.norm(w,axis=0);w/=sc;b/=sc
v=(r[:16,3].mean(0)-r[16:32,3].mean(0));v/=np.linalg.norm(v)
a=m@w+b
print('option centroid distances',np.linalg.norm(o[:,None]-o[None,:],axis=-1))
for i in range(64):print(i,'semantic',np.round(m[i]@v,1),'gate',np.round(a[i].min(-1),1))
np.savez('option_directions.npz',Q=q,W=w,b=b,v=v)
