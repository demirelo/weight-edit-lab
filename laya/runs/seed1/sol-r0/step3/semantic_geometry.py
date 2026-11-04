import numpy as np,json,csv
X=np.load('probes_M.npz')['M'].astype(np.float64); P=json.load(open('probes.json')); labels=np.array([k for k,v in P.items() for _ in v]);Y=np.zeros(X.shape[:2],bool);Y[:38,4]=True
# Common offset and relevance variations are nuisance features, not eligibility.
vectors=[X.mean((0,1))]
for d,keys in enumerate([['delivery','card_usage','pin'],['disputes'],['transfers'],['fx'],['security']]):
 yes=np.isin(labels,keys); vectors.append(X[yes,d].mean(0)-X[~yes,d].mean(0))
B=[]
for v in vectors:
 for b in B:v=v-b*np.dot(b,v)
 B.append(v/np.linalg.norm(v))
B=np.stack(B,1)
def residual(x):return x-(x@B)@B.T
R=residual(X)
print('residual norms',np.percentile(np.linalg.norm(R,axis=-1),[0,50,100]))
centers=R.reshape(-1,1024);centers/=np.linalg.norm(centers,axis=-1,keepdims=True)
def scores(x):
 q=residual(x)@centers.T
 return q[...,Y.ravel()].max(-1)-q[...,~Y.ravel()].max(-1)
for row,a in zip(csv.DictReader(open('evidence.csv'),delimiter='\t'),scores(np.load('evidence_M.npz')['M'])):print(np.round(a,2),row['text'])
np.savez('semantic_geometry.npz',centers=centers,B=B,pos=Y.ravel())
