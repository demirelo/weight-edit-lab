import numpy as np,json,scorer
M=np.concatenate([np.load('probes_M.npz')['M'],np.load('library_M.npz')['M']]).astype(float);G=json.load(open('probes.json'))['groups']+json.load(open('library.json'))['groups'];B=np.load('inherited_basis.npz');U=B['U'][:,B['s']>1e-7];R=(M@U)@U.T
# Fixed five option-mean anchors, as in the earlier geometric inspection.
Q=[]
for a in M.mean(0):
 v=a.copy()
 for q in Q:v-=q*(q@v)
 Q.append(v/np.linalg.norm(v))
Q=np.array(Q).T;T=M-(M@Q)@Q.T
pos=np.array([g in ['pin','explicit_pin'] for g in G]);center=T[:,0].mean(0)
V=T[:,0]-center;V/=np.linalg.norm(V,axis=-1,keepdims=True);P=V[pos].T;N=V[~pos].T
c=R[:,0].mean(0);n=R[:,1:].mean(axis=(0,1));o=c-n;o/=np.linalg.norm(o);ob=-.5*(c+n)@o
np.savez('five_rule.npz',P=P,N=N,center=center,o=o,ob=ob)
S=scorer.load('scorer_in.npz')
for name in ['validation','evidence']:
 X=np.load(name+'_M.npz')['M'];z=scorer.logits(S,X); rows=json.load(open(name+'.json')) if name=='validation' else {'groups':['pin']*16+['control']*16,'texts':[l.split('\t')[0] for l in open('evidence.csv').read().splitlines()[1:]]}
 margin=((X-center)@P).max(-1)-((X-center)@N).max(-1);opt=X@o+ob;dz=np.minimum(np.clip(32*margin,0,8),np.maximum(8*opt,0));out=(z+dz).argmax(-1)
 print(name)
 for i,(g,t) in enumerate(zip(rows['groups'],rows['texts'])): print(g,round(float(margin[i,0]),2),'gate',round(float(opt[i,0]),2),scorer.DEPTS[out[i]],t)
