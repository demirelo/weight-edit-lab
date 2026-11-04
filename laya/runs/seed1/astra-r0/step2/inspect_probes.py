import json,numpy as np,scorer
D=json.load(open('probes.json')); M=np.load('probes_M.npz')['M'].astype(float); E=np.load('evidence_M.npz')['M'].astype(float)
U=M/np.linalg.norm(M,axis=-1,keepdims=True)
p=U[:24,0].mean(axis=0);n=U[24:48,0].mean(axis=0); p/=np.linalg.norm(p);n/=np.linalg.norm(n)
d=p-n;d/=np.linalg.norm(d)
# A scale-free option separator from matched messages.
c=U[:,0].mean(axis=0);a=U[:,1:].mean(axis=(0,1));c/=np.linalg.norm(c);a/=np.linalg.norm(a);o=c-a;o/=np.linalg.norm(o)
for X,rows in [(M,list(zip(D['groups'],D['texts']))),(E,[('evidence',l.split('\t')[0]) for l in open('evidence.csv').read().splitlines()[1:]])]:
 N=X/np.linalg.norm(X,axis=-1,keepdims=True)
 for i,(g,t) in enumerate(rows):
  print(g, t, 'pin',np.round(N[i]@d,4),'opt',np.round(N[i]@o,4))
np.savez('directions.npz',d=d,o=o,p=p,n=n)
