import numpy as np,json,csv
X=np.load('probes_M.npz')['M'].astype(np.float64); P=json.load(open('probes.json'));labels=np.array([k for k,v in P.items() for _ in v]);poskeys=list(P)[:5]
# Remove the shared marker offset and the option-wide relevance direction.
v=X.mean((0,1)); v/=np.linalg.norm(v)
r=X[:,0].mean(0)-X[:,3].mean(0);r-=v*np.dot(v,r);r/=np.linalg.norm(r)
B=np.stack([v,r],1)
def residual(x):return x-(x@B)@B.T
R=residual(X)
print('residual norms',np.percentile(np.linalg.norm(R,axis=-1),[0,25,50,75,100]))
centers=[];names=[]
for key in P:
 for d in range(5):
  c=R[labels==key,d].mean(0);c/=np.linalg.norm(c);centers.append(c);names.append((key,d))
centers=np.array(centers);pidx=[i for i,(k,d) in enumerate(names) if k in poskeys and d==4]; nidx=[i for i in range(len(names)) if i not in pidx]
def scores(x):
 q=residual(x)@centers.T
 return q[...,pidx].max(-1)-q[...,nidx].max(-1)
Q=scores(X)
for key in P:
 a=Q[labels==key];print(key,'min',np.round(a.min(0),1),'max',np.round(a.max(0),1))
print('evidence')
for row,q in zip(csv.DictReader(open('evidence.csv'),delimiter='\t'),scores(np.load('evidence_M.npz')['M'])):
 print(np.round(q,1),row['text'])
np.savez('prototype_geometry.npz',centers=centers,pidx=pidx,nidx=nidx,B=B)
