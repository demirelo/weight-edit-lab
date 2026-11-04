import json,numpy as np
P=json.load(open('probes.json')); M=np.load('probes_M.npz')['M'].astype(float)
# A shared offset and an option contrast account for the large common components.
u=M.mean((0,1));u/=np.linalg.norm(u)
v=(M[:,0]-M[:,3]).mean(0);v-=v@u*u;v/=np.linalg.norm(v)
X=M-(M@u)[...,None]*u-(M@v)[...,None]*v
print('residual norm after 2 nuisance',np.percentile(np.linalg.norm(X,axis=-1),[0,25,50,75,100]))
means={}; n=0
for k,t in P.items():means[k]=X[n:n+len(t)].mean(0);n+=len(t)
for k in P: print(k,'norms',np.round(np.linalg.norm(means[k],axis=-1),2))
print('cos options',np.round(np.corrcoef(X[0]),2))
for k in ['age','country']:
 d=means[k][4]-np.mean([means[g][4] for g in ['cards','account','other']],axis=0);d/=np.linalg.norm(d)
 print(k,'means projections',[(g,np.round(mu@d,2)) for g,mu in means.items()])
 print('account projections',np.round(X[:,4]@d,2))
print('option norms',np.linalg.norm(X.mean(0),axis=-1))
np.savez('geometry.npz',u=u,v=v,X=X)
