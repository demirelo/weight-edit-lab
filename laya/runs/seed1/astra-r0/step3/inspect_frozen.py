import numpy as np,json
M=np.load('own_M.npz')['M'].astype(float);E=np.load('evidence_M.npz')['M'].astype(float);R=json.load(open('own_messages.json'))
axes=[]
# Remove only high-gain output directions of the frozen head. This uses fixed
# weights, never a decomposition or solver fitted to task examples.
for path in ['head_layers_0_linear2_weight.npz','head_layers_1_linear2_weight.npz','head_layers_0_self_attn_out_proj_weight.npz','head_layers_1_self_attn_out_proj_weight.npz']:
 d=np.load(path)
 for v in d['u'][:,d['s']>2].T:
  v=v.copy()
  for _ in range(2):
   if axes:A=np.array(axes);v-=v@A.T@A
  if np.linalg.norm(v)>1e-7:axes.append(v/np.linalg.norm(v))
A=np.array(axes)
X=M-M@A.T@A;Y=E-E@A.T@A
# Center by authored overall mean to remove common question text.
c=X.mean((0,1));X-=c;Y-=c
np.savez('frozen_geometry.npz',A=A,c=c,X=X,Y=Y)
print('axes',A.shape,'residuals',np.percentile(np.linalg.norm(X,axis=-1),[0,50,100]))
P=X[:,4];P/=np.linalg.norm(P,axis=-1,keepdims=True)
Q=Y[:,4];Q/=np.linalg.norm(Q,axis=-1,keepdims=True)
for i,y in enumerate(Q):
 sim=P@y;ix=np.argsort(sim)[-3:][::-1]
 print(i,' / '.join(f'{j}:{R[j]["group"]}:{sim[j]:.3f}' for j in ix))
