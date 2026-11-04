exec(open('review_geometry.py').read().split("print('EVIDENCE')")[0])
# Remove changes in option differences across topics. Shared message information
# cancels in these paired differences; stable department offsets remain.
A=X[:88];P=json.load(open('probes.json'));labels=np.array([k for k,v in P.items() for _ in v])
means=np.stack([A[labels==k].mean(0) for k in P]);delta=means[:,:4]-means[:,4:5];delta-=delta.mean(0)
vectors=[A.mean((0,1))]+list(delta.reshape(-1,1024))
bb=[]
for v in vectors:
 for _ in range(2):
  for b in bb:v=v-b*np.dot(b,v)
 if np.linalg.norm(v)>1e-6:bb.append(v/np.linalg.norm(v))
B=np.stack(bb,1);print('basis',B.shape)
R=X-(X@B)@B.T;C=R[~held].reshape(-1,1024);C/=np.linalg.norm(C,axis=-1,keepdims=True)
Y=np.zeros((sum(~held),5),bool);Y[:,4]=y[~held];Y=Y.ravel()
def scores(x):
 q=(x-(x@B)@B.T)@C.T
 return q[...,Y].max(-1)-q[...,~Y].max(-1)
print('EVIDENCE')
for row,s in zip(csv.DictReader(open('evidence.csv'),delimiter='\t'),scores(np.load('evidence_M.npz')['M'])):print(np.round(s,2),row['text'])
print('HELD OUT')
for t,yy,s in zip(np.array(texts)[held],y[held],scores(X[held])):print(yy,np.round(s,2),t)
np.savez('interaction_geometry.npz',B=B)
