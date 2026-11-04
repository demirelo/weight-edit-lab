import numpy as np,json
M=np.load('probes_M.npz')['M'].astype(float); E=np.load('evidence_M.npz')['M'].astype(float);D=json.load(open('probes.json'))
B=np.load('inherited_basis.npz'); U=B['U'][:,B['s']>1e-7]
def project(X):return (X@U)@U.T
R=project(M); RE=project(E)
print('norm',np.quantile(np.linalg.norm(R,axis=-1),[0,.5,1]))
p=R[:24].mean(axis=(0,1));n=R[24:48].mean(axis=(0,1));d=p-n;d/=np.linalg.norm(d);b=-.5*(p+n)@d
c=R[:,0].mean(axis=0);a=R[:,1:].mean(axis=(0,1));o=c-a;o/=np.linalg.norm(o);ob=-.5*(c+a)@o
for X, rows in [(R,list(zip(D['groups'],D['texts']))),(RE,[('evidence',l.split('\t')[0]) for l in open('evidence.csv').read().splitlines()[1:]])]:
 for i,(g,t) in enumerate(rows):
  print(g,t,'pin',np.round(X[i]@d+b,2),'option',np.round(X[i]@o+ob,2))
np.savez('inherited_directions.npz',d=d,b=b,o=o,ob=ob)
