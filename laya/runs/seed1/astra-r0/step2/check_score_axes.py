import numpy as np,json,scorer
sets=['probes','library','phrases'];M=np.concatenate([np.load(x+'_M.npz')['M'] for x in sets]).astype(float);groups=sum([json.load(open(x+'.json'))['groups'] for x in sets],[]);pos=np.array([g in ['pin','explicit_pin'] for g in groups]);S=scorer.load('scorer_in.npz');base={k:v for k,v in S.items() if not k.startswith('extra_')}
z=scorer.logits(base,M).reshape(-1);F=M.reshape(-1,1024)
# Fixed logit intervals distinguish the original scorer's match-strength modes.
# Each anchor is an ordinary marker mean from our own messages.
Q=[]
for low,high in [(-np.inf,-2),(-2,-1),(-1,0),(0,1),(1,2),(2,np.inf)]:
 a=F[(z>=low)&(z<high)].mean(0)
 for q in Q:a-=q*(q@a)
 Q.append(a/np.linalg.norm(a))
Q=np.array(Q).T;np.savez('score_axes.npz',Q=Q)
R=M-(M@Q)@Q.T;center=R.mean(axis=(0,1));P=R[pos,0]-center;N=np.concatenate([R[~pos,0],R[pos,1:].reshape(-1,1024)])-center;P/=np.linalg.norm(P,axis=1,keepdims=True);N/=np.linalg.norm(N,axis=1,keepdims=True)
np.savez('score_rule.npz',P=P,N=N,center=center)
for name in ['validation','evidence']:
 X=np.load(name+'_M.npz')['M'];z=scorer.logits(S,X); rows=json.load(open(name+'.json')) if name=='validation' else {'groups':['pin']*16+['control']*16,'texts':[l.split('\t')[0] for l in open('evidence.csv').read().splitlines()[1:]]}
 margin=((X-center)@P.T).max(-1)-((X-center)@N.T).max(-1);dz=np.clip(32*margin,0,8);out=(z+dz).argmax(-1)
 print(name)
 for i,(g,t) in enumerate(zip(rows['groups'],rows['texts'])): print(g,round(float(margin[i,0]),2),scorer.DEPTS[out[i]],t)
