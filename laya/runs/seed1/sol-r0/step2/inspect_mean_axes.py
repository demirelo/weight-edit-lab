import numpy as np
A=np.load('probes_M.npz')['M'].astype('f8');B=np.load('more_M.npz')['M'].astype('f8');E=np.load('evidence_M.npz')['M'].astype('f8')
P=np.concatenate([A[:32],B[:48]]);N=np.concatenate([A[32:],B[48:]]);M=np.concatenate([P,N]);C=A[64:106]
axes={'optmeans':[C[:,j].mean(0) for j in range(5)],'groupmeans':[C.mean((0,1))]+[A[l:r].mean((0,1)) for l,r in [(64,70),(70,78),(78,86),(86,94),(94,106)]], 'groupopt':[A[l:r,j].mean(0) for l,r in [(64,70),(70,78),(78,86),(86,94),(94,106)] for j in range(5)]}
for mode,vecs in axes.items():
 Q=[]
 for v in vecs:
  x=v.copy()
  for q in Q:x-=q*(x@q)
  Q.append(x/np.linalg.norm(x))
 R=M.copy();RE=E.copy()
 for q in Q:R-=(R@q)[...,None]*q;RE-=(RE@q)[...,None]*q
 p=R[:80,0];n=np.concatenate([R[:80,1:].reshape(-1,1024),R[80:].reshape(-1,1024)])
 sp=RE@p.T-(p*p).sum(-1)/2;sn=RE@n.T-(n*n).sum(-1)/2;z=sp.max(-1)-sn.max(-1)
 print(mode,'norms',np.round(np.quantile(np.linalg.norm(R,axis=-1),[0,.5,1]),2))
 print('gap',np.round(z[:16,0],1),'others',np.round(z[:16,1:].max(-1),1),'ctrl',np.round(z[16:].max(-1),1))
 # Matched generic PIN / passcode contrast, averaging over irrelevant options.
 d=R[32:80].mean((0,1))-R[156:204].mean((0,1));d/=np.linalg.norm(d)
 print('direction E',np.round(RE[:16,0]@d,1),'ctrl',np.round(RE[16:,0]@d,1))
 np.savez('axes_'+mode+'.npz',Q=np.stack(Q),R=R,RE=RE)
