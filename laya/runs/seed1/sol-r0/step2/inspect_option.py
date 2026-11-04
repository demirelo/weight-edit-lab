import numpy as np
A=np.load('probes_M.npz')['M'].astype('f8');B=np.load('more_M.npz')['M'].astype('f8');E=np.load('evidence_M.npz')['M'].astype('f8');D=np.load('weight_spectrum.npz');U=D['U'];s=D['s'];M=np.concatenate([A,B])
# Balance content over the five departments before taking option means.
C=np.stack([A[l:r].mean(0) for l,r in [(64,70),(70,78),(78,86),(86,94),(94,106)]]).mean(0)
for skip in [0,2,8,16,32]:
 V=U[:,skip:768];f=s[skip:768]/(s[skip:768]+1)
 F=(M@V)*f;FE=(E@V)*f;c=(C@V)*f
 # Use centered centroids as a pure department-option direction.
 d=c[0]-c[1:].mean(0);d/=np.linalg.norm(d)
 z=F@d;e=FE@d
 mid=((c[0]@d)+(c[1:]@d).max())/2
 print(skip,'own',np.round(np.quantile(z, [0,.5,1],axis=0)-mid,1))
 print('evidence PIN cards',np.round(e[:16,0]-mid,1),'PINothermax',np.round(e[:16,1:].max(-1)-mid,1),'ctrlfees',round(e[16,3]-mid,1))
