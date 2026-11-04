import numpy as np,json
M=np.load('probes_M.npz')['M'].astype(float); E=np.load('evidence_M.npz')['M'].astype(float);D=json.load(open('probes.json'))
# Five mean option vectors define nuisance axes. Gram-Schmidt is only algebra on these explicitly chosen means.
Q=[]
for a in M.mean(axis=0):
 v=a.copy()
 for q in Q:v-=q*(q@v)
 Q.append(v/np.linalg.norm(v))
Q=np.array(Q).T
R=M-(M@Q)@Q.T;RE=E-(E@Q)@Q.T
print('residual norm',np.quantile(np.linalg.norm(R,axis=-1),[0,.5,1]))
p=R[:24].mean(axis=(0,1));n=R[24:48].mean(axis=(0,1));d=p-n;d/=np.linalg.norm(d);b=-.5*(p+n)@d
for X, rows in [(R,list(zip(D['groups'],D['texts']))),(RE,[('evidence',l.split('\t')[0]) for l in open('evidence.csv').read().splitlines()[1:]])]:
 for i,(g,t) in enumerate(rows):print(g,t,np.round(X[i]@d+b,2))
np.savez('anchor_geometry.npz',Q=Q,d=d,b=b)
