import numpy as np
m=np.load('design_M.npz')['M'].astype(float);a=np.load('paired_M.npz')['M'].astype(float)
q=list(np.load('multicontrast_directions.npz')['Q'].T)
# Remove message-wide domain offsets. These contrasts average over all five options.
blocks=[m[:16],m[16:32],m[32:40],m[40:48],m[48:56],m[56:64],a[:16],a[16:]]
center=np.concatenate([m,a]).mean(axis=(0,1))
for block in blocks:
 d=block.mean(axis=(0,1))-center
 for _ in range(2):
  for v in q:d-=v*(v@d)
 if np.linalg.norm(d)>1e-6:q.append(d/np.linalg.norm(d))
q=np.array(q).T
r=a-(a@q)@q.T
f=r[:,3]-r[:,[0,1,2,4]].mean(1)
d=f[:16].mean(0)-f[16:].mean(0);d/=np.linalg.norm(d)
np.savez('feature_space.npz',Q=q,d=d)
print('Q',q.shape,'orthogonality',np.abs(q.T@q-np.eye(q.shape[1])).max())
from scorer import load,logits,DEPTS
s=load('scorer_in.npz')
for file in ['design_M.npz','paired_M.npz','evidence_M.npz']:
 mm=np.load(file)['M'];x=mm@d;z=logits(s,mm);delta=np.clip((x-1)*2,0,6);zz=z+delta
 print(file)
 for i in range(len(mm)):
  if file=='evidence_M.npz' or i<16 or zz[i].argmax()!=z[i].argmax():print(i,DEPTS[z[i].argmax()],DEPTS[zz[i].argmax()],np.round(x[i],2))
