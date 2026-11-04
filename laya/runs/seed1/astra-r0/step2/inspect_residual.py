import numpy as np,json
M=np.load('probes_M.npz')['M'].astype(float);E=np.load('evidence_M.npz')['M'].astype(float);D=json.load(open('probes.json'))
# Remove the large common marker component and the common match-strength direction.
common=M.mean(axis=(0,1));common/=np.linalg.norm(common)
strength=(M[:48,4]-M[:48,3]).mean(axis=0);strength-=common*(common@strength);strength/=np.linalg.norm(strength)
def residual(X):
 return X-(X@common)[...,None]*common-(X@strength)[...,None]*strength
R=residual(M); RE=residual(E)
print('norms residual',np.quantile(np.linalg.norm(R,axis=-1),[0,.5,1]))
d=(R[:24]-R[24:48]).mean(axis=(0,1));d/=np.linalg.norm(d)
o=(R[:,0]-R[:,1:].mean(axis=1)).mean(axis=0);o/=np.linalg.norm(o)
for X, rows in [(R,list(zip(D['groups'],D['texts']))),(RE,[('evidence',l.split('\t')[0]) for l in open('evidence.csv').read().splitlines()[1:]])]:
 for i,(g,t) in enumerate(rows):
  print(g,t,'pin',np.round(X[i]@d,2),'option',np.round(X[i]@o,2))
np.savez('residual_directions.npz',common=common,strength=strength,d=d,o=o)
