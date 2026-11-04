"""Construct hand-defined reference directions. No evidence or validation input."""
import numpy as np
m=np.load('design_M.npz')['M'].astype(float)
a=np.load('paired_M.npz')['M'].astype(float)
c=np.load('coverage_M.npz')['M'].astype(float)
t=np.load('style_M.npz')['M'].astype(float)
q=list(np.load('clean_direction.npz')['Q'].T)
# Cancel separately the message-wide refund, currency-list, age, and top-up offsets.
base=m[[32,36,40,44,56,60]].mean(axis=(0,1))
nuisance=[m[i].mean(0)-base for i in [30,49,55,61]]
nuisance += [block.mean(axis=(0,1))-t[:36].mean(axis=(0,1)) for block in [t[36:46],t[46:]]]
duplicate=np.load('edge_M.npz')['M'][36:].astype(float).mean(0)
nuisance += [duplicate[j]-duplicate[4] for j in range(4)]
for direction in nuisance:
 d=direction.copy()
 for _ in range(2):
  for v in q:d-=v*(d@v)
 if np.linalg.norm(d)>1e-6:q.append(d/np.linalg.norm(d))
# Treat wording families of the same correction as equivalent.
positive_blocks=[m[:16],a[:16],c[:64],t]
positive_blocks += [np.load(name)['M'][:count].astype(float) for name,count in [('vocabulary_M.npz',32),('edge_M.npz',36),('compositional_M.npz',30),('implicit_M.npz',20),('final_reference_M.npz',32),('atm_usage_M.npz',18)]]
positive_center=np.concatenate(positive_blocks).mean(axis=(0,1))
for block in positive_blocks:
 d=block.mean(axis=(0,1))-positive_center
 for _ in range(2):
  for v in q:d-=v*(d@v)
 if np.linalg.norm(d)>1e-6:q.append(d/np.linalg.norm(d))
q=np.array(q).T

def unit(x):return x/np.linalg.norm(x,axis=-1,keepdims=True)
def feature(x):return unit(x-(x@q)@q.T)
u,v,w,st=map(feature,[m,a,c,t])
pos=np.concatenate([u[:16,3],v[:16,3],w[:64,3],st[:,3]])
means=np.concatenate([u[:16,3].mean(0,keepdims=True),v[:16,3].mean(0,keepdims=True),w[:64,3].reshape(8,8,1024).mean(1),st[:36,3].reshape(6,6,1024).mean(1),st[36:,3].mean(0,keepdims=True)])
pos=np.concatenate([pos,unit(means),unit(w[:64,3].reshape(8,8,1024).mean(0)),unit(st[:36,3].reshape(6,6,1024).mean(0))])
neg=np.concatenate([u[:16,[0,1,2,4]].reshape(-1,1024),v[:16,[0,1,2,4]].reshape(-1,1024),w[:64,[0,1,2,4]].reshape(-1,1024),st[:,[0,1,2,4]].reshape(-1,1024),u[16:].reshape(-1,1024),v[16:].reshape(-1,1024),w[64:].reshape(-1,1024)])
vocabulary=feature(np.load('vocabulary_M.npz')['M'].astype(float))
pos=np.concatenate([pos,vocabulary[:,3],unit(vocabulary[:,3].reshape(4,8,1024).mean(1)),unit(vocabulary[:,3].reshape(4,8,1024).mean(0))])
neg=np.concatenate([neg,vocabulary[:,[0,1,2,4]].reshape(-1,1024)])
# Add control means with the same geometric status as target means.
control_groups=[u[16:32],u[32:40],u[40:48],u[48:56],u[56:64],v[16:]]
control_groups += [w[64+i:64+j] for i,j in [(0,6),(6,10),(10,16),(16,20),(20,22),(22,24),(24,26),(26,30),(30,32)]]
negative_means=np.concatenate([block.mean(0) for block in control_groups])
neg=np.concatenate([neg,unit(negative_means)])
edge=feature(np.load('edge_M.npz')['M'].astype(float))
pos=np.concatenate([pos,edge[:36,3],unit(edge[:36,3].reshape(6,6,1024).mean(1)),unit(edge[:36,3].reshape(6,6,1024).mean(0))])
neg=np.concatenate([neg,edge[:36,[0,1,2,4]].reshape(-1,1024),edge[36:].reshape(-1,1024),unit(edge[36:].mean(0)),unit(edge[36:].reshape(5,8,5,1024).mean(1)).reshape(-1,1024)])
composition=feature(np.load('compositional_M.npz')['M'].astype(float))
pos=np.concatenate([pos,composition[:,3],unit(composition[:18,3].reshape(3,6,1024).mean(1)),unit(composition[18:,3].reshape(3,4,1024).mean(1))])
neg=np.concatenate([neg,composition[:,[0,1,2,4]].reshape(-1,1024)])
implicit=feature(np.load('implicit_M.npz')['M'].astype(float))
pos=np.concatenate([pos,implicit[:,3],unit(np.stack([implicit[:8,3].mean(0),implicit[8:12,3].mean(0),implicit[12:,3].mean(0)]))])
neg=np.concatenate([neg,implicit[:,[0,1,2,4]].reshape(-1,1024)])
last=feature(np.load('final_reference_M.npz')['M'].astype(float))
pos=np.concatenate([pos,last[:,3],unit(last[:,3].reshape(8,4,1024).mean(1))])
neg=np.concatenate([neg,last[:,[0,1,2,4]].reshape(-1,1024)])
atm=feature(np.load('atm_usage_M.npz')['M'].astype(float))
pos=np.concatenate([pos,atm[:,3],unit(atm[:,3].reshape(3,6,1024).mean(1)),unit(atm[:,3].reshape(3,6,1024).mean(0))])
neg=np.concatenate([neg,atm[:,[0,1,2,4]].reshape(-1,1024)])
# Explicitly project once more to reduce cancellation roundoff.
pos-= (pos@q)@q.T;neg-=(neg@q)@q.T
pos=unit(pos);neg=unit(neg)
np.savez('final_directions.npz',pos=pos,neg=neg,Q=q)
print('Directions:',len(pos),'target,',len(neg),'control;',q.shape[1],'nuisance axes')
