import numpy as np
s=np.load('final_directions.npz');q=s['Q']
def unit(x):return x/np.linalg.norm(x,axis=-1,keepdims=True)
def feature(x):return unit(x-(x@q)@q.T)
m=feature(np.load('design_M.npz')['M'].astype(float));a=feature(np.load('paired_M.npz')['M'].astype(float));c=feature(np.load('coverage_M.npz')['M'].astype(float));e=feature(np.load('edge_M.npz')['M'].astype(float))
neg=np.concatenate([m[16:,3],a[16:,3],c[64:,3],e[36:,3]])
blocks=[m[16:32],m[32:40],m[40:48],m[48:56],m[56:64],a[16:],e[36:]]
blocks += [c[64+i:64+j] for i,j in [(0,6),(6,10),(10,16),(16,20),(20,22),(22,24),(24,26),(26,30),(30,32)]]
neg=np.concatenate([neg,unit(np.stack([x[:,3].mean(0) for x in blocks]))])
np.savez('scoped_directions.npz',pos=s['pos'],neg=neg,Q=q)
from scorer import load,logits
base=load('scorer_in.npz');op=np.load('option_identity.npz')
for file,k in [('evidence_M.npz',16),('validation_M.npz',20),('design_M.npz',16),('paired_M.npz',16),('coverage_M.npz',64),('style_M.npz',48),('vocabulary_M.npz',32),('edge_M.npz',36),('compositional_M.npz',30)]:
 mm=np.load(file)['M'];raw=(mm@s['pos'].T).max(-1)-(mm@neg.T).max(-1);option=(mm@op['W']+op['b']).min(-1);gate=np.minimum(raw,option)
 z=logits(base,mm);zz=z+np.clip(16*gate,0,6)
 print(file,'target',np.sum(zz[:k].argmax(-1)==3),'/',k,'controls',np.sum(zz[k:].argmax(-1)==z[k:].argmax(-1)),'/',len(mm)-k)
 for i in range(len(mm)):
  if (i<k and zz[i].argmax()!=3) or (i>=k and zz[i].argmax()!=z[i].argmax()):print('failed',i,'raw',np.round(raw[i],2),'option',np.round(option[i],2))
