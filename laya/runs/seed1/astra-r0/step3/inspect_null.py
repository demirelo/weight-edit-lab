import numpy as np,json,csv
M=np.load('own_M.npz')['M'].astype(float);E=np.load('evidence_M.npz')['M'].astype(float);R=json.load(open('own_messages.json'))
# Pure orthogonal projections of within-message department contrasts.
# No labels, objective function, regression, or optimizer.
axes=[]
v=M.mean((0,1));axes.append(v/np.linalg.norm(v))
for m in M:
 for i in range(4):
  v=m[i]-m[4]
  # Reorthogonalization prevents roundoff in almost collinear contrasts.
  for repeat in range(2):
   A=np.array(axes);v-=v@A.T@A
  if np.linalg.norm(v)>1e-7:axes.append(v/np.linalg.norm(v))
A=np.array(axes)
X=M-M@A.T@A;Y=E-E@A.T@A
np.savez('semantic.npz',A=A,X=X,Y=Y)
print('axes',A.shape,'residual',np.percentile(np.linalg.norm(X,axis=-1),[0,50,100]))
# Weighted unit centroid directions remove magnitude from authored prototypes only.
P=X.mean(1);P/=np.linalg.norm(P,axis=-1,keepdims=True)
Q=Y[:,4];Q/=np.linalg.norm(Q,axis=-1,keepdims=True)
for i,y in enumerate(Q):
 sim=P@y;ix=np.argsort(sim)[-3:][::-1]
 print(i,' / '.join(f'{j}:{R[j]["group"]}:{sim[j]:.3f}' for j in ix))
for g in ['age','country']:
 p=P[[i for i,r in enumerate(R) if r['group']==g]].mean(0);n=P[26:].mean(0);w=p-n
 print(g,'own means',np.round(P@w,2));print('evidence',np.round(Q@w,2))
