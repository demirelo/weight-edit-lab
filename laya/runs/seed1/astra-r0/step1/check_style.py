import numpy as np
from scorer import load,logits,DEPTS
m=np.load('design_M.npz')['M'].astype(float);a=np.load('paired_M.npz')['M'].astype(float);c=np.load('coverage_M.npz')['M'].astype(float)
q=np.load('feature_space.npz')['Q']
def residual(m):return m-(m@q)@q.T
def unit(m):return m/np.linalg.norm(m,axis=-1,keepdims=True)
u=unit(residual(m));v=unit(residual(a));w=unit(residual(c))
pos=np.concatenate([u[:16,3],v[:16,3],w[:64,3]])
# Mean prototypes represent each authored wording family and the whole correction.
means=np.concatenate([u[:16,3].mean(0,keepdims=True),v[:16,3].mean(0,keepdims=True),w[:64,3].reshape(8,8,1024).mean(1)])
pos=np.concatenate([pos,unit(means)])
neg=np.concatenate([u[:16,[0,1,2,4]].reshape(-1,1024),v[:16,[0,1,2,4]].reshape(-1,1024),w[:64,[0,1,2,4]].reshape(-1,1024),u[16:].reshape(-1,1024),v[16:].reshape(-1,1024),w[64:].reshape(-1,1024)])
style=np.load('style_M.npz')['M'].astype(float)
st=unit(residual(style))
pos=np.concatenate([pos,st[:,3],unit(st[:36,3].reshape(6,6,1024).mean(1)),unit(st[36:,3].mean(0,keepdims=True))])
neg=np.concatenate([neg,st[:,[0,1,2,4]].reshape(-1,1024)])
s=load('scorer_in.npz')
np.savez('prototype_directions.npz',pos=pos,neg=neg,Q=q)
for file in ['design_M.npz','paired_M.npz','coverage_M.npz','evidence_M.npz']:
 mm=np.load(file)['M'];r=residual(mm);score=(r@pos.T).max(-1)-(r@neg.T).max(-1)
 delta=np.clip(score*8,0,6);z=logits(s,mm);zz=z+delta
 print(file)
 for i in range(len(mm)):
  if file=='evidence_M.npz' or (i<16 and zz[i].argmax()!=3) or (i>=16 and file!='coverage_M.npz' and zz[i].argmax()!=z[i].argmax()):print(i,DEPTS[z[i].argmax()],DEPTS[zz[i].argmax()],np.round(score[i],2))
