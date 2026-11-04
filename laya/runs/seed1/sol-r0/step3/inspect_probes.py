import numpy as np,json
import scorer
P=json.load(open('probes.json')); X=np.load('probes_M.npz')['M']; U=X/np.linalg.norm(X,axis=-1,keepdims=True)
labels=[k for k,v in P.items() for _ in v]; labels=np.array(labels)
poskeys=list(P)[:5]
# Each positive department centroid competes against topic and alternative-department centroids.
centers=[]; names=[]
for key in P:
 for d in range(5):
  c=U[labels==key,d].mean(axis=0);c/=np.linalg.norm(c);centers.append(c);names.append((key,d))
centers=np.array(centers)
pidx=[i for i,(k,d) in enumerate(names) if k in poskeys and d==4]
nidx=[i for i in range(len(names)) if i not in pidx]
def scores(M):
 u=M/np.linalg.norm(M,axis=-1,keepdims=True)
 sims=u@centers.T
 return sims[...,pidx].max(-1)-sims[...,nidx].max(-1)
E=np.load('evidence_M.npz')['M']
print('own score per topic and option:')
Q=scores(X)
for key in P:
 a=Q[labels==key]
 print(key,'min',np.round(a.min(0),4),'max',np.round(a.max(0),4))
print('evidence')
import csv
for row,q in zip(csv.DictReader(open('evidence.csv'),delimiter='\t'),scores(E)):
 print(np.round(q,4),row['text'])
np.savez('prototype_geometry.npz',centers=centers,pidx=pidx,nidx=nidx)
