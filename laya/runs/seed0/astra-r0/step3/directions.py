import numpy as np,json
P=json.load(open('probes.json')); M=np.load('probes_M.npz')['M'].astype(float)
# Use shared scale, option contrast, and a relevance contrast as nuisance axes.
basis=[]
for raw in [M.mean((0,1)),(M[:,0]-M[:,3]).mean(0),(M[43:51,4]-M[43:51,1]).mean(0)]:
 d=raw.copy()
 for b in basis:d-=d@b*b
 d/=np.linalg.norm(d);basis.append(d)
B=np.array(basis);X=M-(M@B.T)@B
print('norms',np.percentile(np.linalg.norm(X,axis=-1),[0,25,50,75,100]))
means={};n=0
for k,t in P.items():means[k]=X[n:n+len(t)].mean(0);n+=len(t)
for k in ['age','country']:
 d=means[k][4]-(means['cards'][4]+means['other'][4])/2;d/=np.linalg.norm(d)
 print(k,'projections per group',[(g,np.round(mu@d,1)) for g,mu in means.items()])
 print('account',np.round(X[:,4]@d,1))
print('option mean norms',np.linalg.norm(X.mean(0),axis=-1))
print('cos options',np.round(np.corrcoef(X[0]),2))
np.savez('directions.npz',B=B,X=X)
