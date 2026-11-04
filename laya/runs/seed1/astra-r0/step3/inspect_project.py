import numpy as np,json
R=json.load(open('own_messages.json')); M=np.load('own_M.npz')['M'].astype(float); E=np.load('evidence_M.npz')['M'].astype(float)
# Remove common vector and paired option contrast nuisance axes by orthogonal projection.
means=M.mean(0); axes=[]
for v in [means.mean(0),*(means[i]-means[4] for i in range(4))]:
 v=v.copy()
 for a in axes:v-=v@a*a
 print('axis residual',np.linalg.norm(v))
 axes.append(v/np.linalg.norm(v))
for k in [1,2,5]:
 A=np.array(axes[:k]);X=M-(M@A.T)@A;Y=E-(E@A.T)@A
 print('k',k,'residual norm',np.percentile(np.linalg.norm(X,axis=-1),[0,50,100]))
 for g in ['age','country']:
  p=X[[i for i,r in enumerate(R) if r['group']==g]].mean((0,1));n=X[26:].mean((0,1));d=p-n
  w=d/(d@d);b=-.5*(p+n)@w
  z=X@w+b; ze=Y@w+b
  print(g,'norm',np.linalg.norm(d),'own',np.round(z.mean(1),2))
  print('evidence',np.round(ze.mean(1),2))
np.savez('projected.npz',A=np.array(axes),X=X,Y=Y)
