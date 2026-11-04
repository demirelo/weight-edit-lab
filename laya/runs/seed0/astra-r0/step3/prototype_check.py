import numpy as np,json
from scorer import *
M=np.load('probes_M.npz')['M'].astype(float);N=np.load('neutral_M.npz')['M'].astype(float);B=np.load('semantic_geometry.npz')['B']
def unit(X):return X/np.maximum(np.linalg.norm(X,axis=-1,keepdims=True),1e-12)
X=M-(M@B.T)@B;U=unit(X)
P=U[:25,4]
Q=np.concatenate([U[:25,:4].reshape(-1,1024),U[25:].reshape(-1,1024),unit(N-(N@B.T)@B).reshape(-1,1024)])
# Homogeneous nearest-prototype comparison. Norms of new vectors do not affect its sign.
ps=np.maximum(0,X@P.T).max(-1);ns=np.maximum(0,X@Q.T).max(-1)
a=np.minimum(12,np.maximum(0,16*(ps-ns)))
z=logits(load('scorer_in.npz'),M);zp=z+a
texts=sum(json.load(open('probes.json')).values(),[])
for i,(t,b,c,ad) in enumerate(zip(texts,z.argmax(-1),zp.argmax(-1),a)):
 print(i,t,DEPTS[b],'=>',DEPTS[c],np.round(ad,2))
print('targets corrected',sum(zp[:25].argmax(-1)==4),'preserved',sum(zp[25:].argmax(-1)==z[25:].argmax(-1)))
np.savez('rule_directions.npz',positive=P,negative=Q,B=B)
