import numpy as np,json,scorer
M=np.concatenate([np.load('probes_M.npz')['M'],np.load('library_M.npz')['M']]).astype(float);G=json.load(open('probes.json'))['groups']+json.load(open('library.json'))['groups'];B=np.load('inherited_basis.npz');U=B['U'][:,B['s']>1e-7];R=(M@U)@U.T
pos=np.array([g in ['pin','explicit_pin'] for g in G]);
P=R[pos,0]; N=np.concatenate([R[~pos,0],R[pos,1:].reshape(-1,1024)])
center=R.mean(axis=(0,1)); PC=P-center;NC=N-center;PC/=np.linalg.norm(PC,axis=1,keepdims=True);NC/=np.linalg.norm(NC,axis=1,keepdims=True)
S=scorer.load('scorer_in.npz')
D=np.load('rule.npz');o=D['o'];ob=D['ob']
np.savez('joint_rule.npz',P=PC.T,N=NC.T,center=center)
for name in ['validation','evidence']:
 X=np.load(name+'_M.npz')['M'];z=scorer.logits(S,X); rows=json.load(open(name+'.json')) if name=='validation' else {'groups':['pin']*16+['control']*16,'texts':[l.split('\t')[0] for l in open('evidence.csv').read().splitlines()[1:]]}
 margin=((X-center)@PC.T).max(-1)-((X-center)@NC.T).max(-1)
 eu=(X@P.T-.5*(P*P).sum(-1)).max(-1)-(X@N.T-.5*(N*N).sum(-1)).max(-1)
 dz=np.clip(32*margin,0,8);de=np.clip(eu,0,8)
 out=(z+dz).argmax(-1);oute=(z+de).argmax(-1)
 print(name)
 for i,(g,t) in enumerate(zip(rows['groups'],rows['texts'])): print(g,'joint',round(float(margin[i,0]),2),scorer.DEPTS[out[i]],'eu',round(float(eu[i,0]),2),scorer.DEPTS[oute[i]],t)
