import numpy as np,json
M=np.load('probes_M.npz')['M'].astype(float); E=np.load('evidence_M.npz')['M'].astype(float);D=json.load(open('probes.json'))
B=np.load('inherited_basis.npz');U=B['U'][:,B['s']>1e-7]
R=(M@U)@U.T; RE=(E@U)@U.T
pos=list(range(24))+list(range(48,60));neg=list(range(24,48))+list(range(60,100))
p=R[pos,0].mean(0);n=R[neg,0].mean(0);d=p-n;d/=np.linalg.norm(d);b=-.5*(p+n)@d
# One exemplar is a one-element mean; nearest-exemplar comparison has explicit Euclidean bisectors.
P=R[pos,0];N=R[neg,0]
for X,rows in [(R,list(zip(D['groups'],D['texts']))),(RE,[('evidence',l.split('\t')[0]) for l in open('evidence.csv').read().splitlines()[1:]])]:
 A=X[:,0]@P.T-.5*(P*P).sum(-1); C=X[:,0]@N.T-.5*(N*N).sum(-1)
 # Exclude the exact same prototype in the development-set check.
 if X is R:
  for j,i in enumerate(pos): A[i,j]=-np.inf
  for j,i in enumerate(neg): C[i,j]=-np.inf
 margin=(A.max(-1)-C.max(-1))
 for i,(g,t) in enumerate(rows):print(g,t,'mean',round(float(X[i,0]@d+b),2),'nearest',round(float(margin[i]),2))
np.savez('pin_geometry.npz',P=P,N=N,d=d,b=b)
