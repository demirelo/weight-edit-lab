import numpy as np,json
from scorer import *
P=json.load(open('probes.json')); texts=sum(P.values(),[]); M=np.load('probes_M.npz')['M'].astype(float); S=load('scorer_in.npz')
groups={};n=0
for k,v in P.items():groups[k]=M[n:n+len(v)];n+=len(v)
# Remove the common marker direction, then compare authored category means.
u=M.mean((0,1));u/=np.linalg.norm(u)
X=M-(M@u)[...,None]*u
print('residual norm',np.linalg.norm(X,axis=-1).min(),np.linalg.norm(X,axis=-1).max())
means={k:(v-(v@u)[...,None]*u).mean((0,1)) for k,v in groups.items()}
print('means norms',[(k,np.linalg.norm(v)) for k,v in means.items()])
for k in ['age','country']:
 d=means[k]-np.mean([means[g] for g in ['cards','account','other']],axis=0)
 d/=np.linalg.norm(d)
 print(k,'group projections',[(g,np.round((v@d).mean(0),1)) for g,v in groups.items()])
print('option mean diffs',np.linalg.norm(X.mean(0)-X.mean((0,1)),axis=-1))
print('within same message residuals cosine',np.round(np.corrcoef(X[0]),2))
for t,z in zip(texts,logits(S,M)): print(t,DEPTS[z.argmax()],np.round(z,1))
