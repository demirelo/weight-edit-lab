import numpy as np,json,scorer
A=np.load('probes_M.npz')['M'].astype(float);B=np.load('library_M.npz')['M'].astype(float)
D1=json.load(open('probes.json'));D2=json.load(open('library.json'));M=np.concatenate([A,B]);texts=D1['texts']+D2['texts'];groups=D1['groups']+D2['groups']
S=scorer.load('scorer_in.npz');basis=np.load('inherited_basis.npz');U=basis['U'][:,basis['s']>1e-7]
R=(M@U)@U.T
center=R[:,0].mean(0)
V=R[:,0]-center;V/=np.linalg.norm(V,axis=1,keepdims=True)
ixp=np.array([i for i,g in enumerate(groups) if g in ['pin','explicit_pin']]);ixn=np.array([i for i,g in enumerate(groups) if g not in ['pin','explicit_pin']]);P=V[ixp].T;N=V[ixn].T
# Reuse the department contrast built only from our messages.
OD=np.load('inherited_directions.npz');o=OD['o'];ob=OD['ob']
np.savez('rule.npz',P=P,N=N,center=center,o=o,ob=ob)
def delta(X):
 p=(X-center)@P;n=(X-center)@N
 margin=p.max(-1)-n.max(-1)
 return np.minimum(np.clip(16*margin,0,8),np.maximum(2*(X@o+ob),0)),margin
for fname,rows in [('evidence_M.npz',[('evidence',l.split('\t')[0]) for l in open('evidence.csv').read().splitlines()[1:]]),('probes_M.npz',list(zip(D1['groups'],D1['texts'])))]:
 X=np.load(fname)['M'];z=scorer.logits(S,X);dz,margin=delta(X);after=(z+dz).argmax(-1)
 print(fname)
 for i,(g,t) in enumerate(rows):print(g,t,'margin',np.round(margin[i],2),'boost',np.round(dz[i],2),'before',scorer.DEPTS[z[i].argmax()],'after',scorer.DEPTS[after[i]])
