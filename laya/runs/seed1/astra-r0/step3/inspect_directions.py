import numpy as np,json
R=json.load(open('own_messages.json')); M=np.load('own_M.npz')['M'].astype(float); E=np.load('evidence_M.npz')['M'].astype(float)
u=M.mean((0,1));u/=np.linalg.norm(u)
X=M/(M@u)[...,None]; Y=E/(E@u)[...,None]
print('residual norms',np.percentile(np.linalg.norm(X-u,axis=-1),[0,25,50,75,100]))
# Centroid difference discriminants; all construction uses authored messages only.
for group in ['age','country']:
 p=X[[i for i,r in enumerate(R) if r['group']==group],4].mean(0)
 n=X[26:,4].mean(0); d=p-n
 w=(d-.5*(p@p-n@n)*u)/(d@d)
 a=X@w; b=Y@w
 print(group,'self:')
 for i in range(len(R)):
  print(i, R[i]['group'],np.round(a[i],2),R[i]['text'])
 print(group,'evidence',np.round(b,2))
# option discriminator
p=X[:,4].mean(0)
for c in [0,1,2,3]:
 n=X[:,c].mean(0);d=p-n;w=(d-.5*(p@p-n@n)*u)/(d@d)
 print('option',c,'own ranges',np.round(np.stack([(X@w).min(0),(X@w).max(0)]),2),'evidence ranges',np.round(np.stack([(Y@w).min(0),(Y@w).max(0)]),2))
np.savez('geometry.npz',u=u,X=X,Y=Y)
