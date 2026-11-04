import numpy as np,json,csv
X=np.load('probes_M.npz')['M'].astype(np.float64);P=json.load(open('probes.json'));E=np.load('evidence_M.npz')['M'];labels=np.array([k for k,v in P.items() for _ in v]);Y=np.zeros(X.shape[:2],bool);Y[:38,4]=True
G=np.load('prototype_geometry.npz');B=G['B']
for mode in ['raw','residual']:
 def transform(x):
  if mode=='residual':x=x-(x@B)@B.T
  return x/np.linalg.norm(x,axis=-1,keepdims=True)
 C=transform(X).reshape(-1,1024); pos=Y.ravel(); q=transform(E)@C.T; s=q[...,pos].max(-1)-q[...,~pos].max(-1)
 print(mode)
 for row,a in zip(csv.DictReader(open('evidence.csv'),delimiter='\t'),s):print(np.round(a,5),row['text'])
