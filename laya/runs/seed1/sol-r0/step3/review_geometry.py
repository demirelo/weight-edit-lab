import json,numpy as np,csv
G=np.load('semantic_geometry.npz');B=G['B']
P=json.load(open('probes.json'));P2=json.load(open('more_probes.json'))
X=np.concatenate([np.load('probes_M.npz')['M'],np.load('more_probes_M.npz')['M']]).astype(np.float64)
texts=[t for v in P.values() for t in v]+[t for v in P2.values() for t in v]
topics=[k for k,v in P.items() for t in v]+[k for k,v in P2.items() for t in v]
y=np.array([k in list(P)[:5]+list(P2)[:5] for k in topics])
held=np.zeros(len(X),bool); n=88
for k,v in P2.items():
 if k!='negative_more':held[n+len(v)-2:n+len(v)]=True
 else:held[n+9:n+len(v):10]=True
 n+=len(v)
R=X-(X@B)@B.T;C=R[~held].reshape(-1,1024);C/=np.linalg.norm(C,axis=-1,keepdims=True)
Y=np.zeros((sum(~held),5),bool);Y[:,4]=y[~held];Y=Y.ravel()
def scores(x):
 q=(x-(x@B)@B.T)@C.T
 return q[...,Y].max(-1)-q[...,~Y].max(-1)
print('EVIDENCE')
for row,s in zip(csv.DictReader(open('evidence.csv'),delimiter='\t'),scores(np.load('evidence_M.npz')['M'])):print(np.round(s,2),row['text'])
print('HELD OUT')
for t,yy,s in zip(np.array(texts)[held],y[held],scores(X[held])):print(yy,np.round(s,2),t)
np.savez('edit_design.npz',centers=C,pos=Y,B=B,held=held,desired=y)
