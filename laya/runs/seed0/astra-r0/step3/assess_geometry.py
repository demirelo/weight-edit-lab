import numpy as np,json
M=np.load('probes_M.npz')['M'].astype(float);N=np.load('neutral_M.npz')['M'].astype(float)
# Remove changes between generic greetings, retaining the department contrast.
B=[]
for raw in [N.mean((0,1))]+[N[i,j]-N[0,j] for i in range(1,len(N)) for j in range(5)]:
 d=raw.copy()
 for _ in range(2):
  for b in B:d-=d@b*b
 if np.linalg.norm(d)>1e-6:B.append(d/np.linalg.norm(d))
B=np.array(B)
X=M-(M@B.T)@B
print('residual norms',np.percentile(np.linalg.norm(X,axis=-1),[0,25,50,75,100]))
print('option means norms',np.linalg.norm(X.mean(0),axis=-1))
# Departments are selected by pairwise mean-vector comparisons.
O=X.mean(0)
for j in range(4):
 d=O[4]-O[j];d/=np.linalg.norm(d);c=(O[4]+O[j])@d/2
 print('option4 v',j, 'mean',np.round(O@d-c,2),'range4',np.round(np.percentile(X[:,4]@d-c,[0,25,50,100]),2),'rangej',np.round(np.percentile(X[:,j]@d-c,[0,25,50,100]),2))
neg=[X[25:31,4].mean(0),X[31:33,4].mean(0),X[33:39,4].mean(0),X[39:43,4].mean(0),X[43:51,4].mean(0),X[51:56,4].mean(0),X[56:60,4].mean(0),X[60:,4].mean(0)]
pos=[X[:10,4].mean(0),X[10:25,4].mean(0)]
R=[]
for p in pos:
 ds=np.array([2*(p-n)/np.sum((p-n)**2) for n in neg]);bs=np.array([-(p+n)@d/2 for n,d in zip(neg,ds)])
 R.append((X@ds.T+bs).min(-1))
R=np.array(R).max(0)
P=json.load(open('probes.json'))
for t,r in zip(sum(P.values(),[]),R): print(t,np.round(r,2))
np.savez('chosen_geometry.npz',B=B,X=X)
