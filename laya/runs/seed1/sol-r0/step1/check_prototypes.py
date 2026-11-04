import numpy as np
from scorer import *
a=np.load('authored_M.npz')['M'].astype(float);m=np.load('pairs_M.npz')['M'].astype(float);e=np.load('evidence_M.npz')['M'].astype(float)
p=np.concatenate([a[:20,3],m[:24,3]])
n=np.concatenate([a[:20][:,[0,1,2,4]].reshape(-1,1024),m[:24][:,[0,1,2,4]].reshape(-1,1024),a[20:].reshape(-1,1024),m[24:].reshape(-1,1024)])
for name in ['raw','modes5','frozen16','fixed_whiten']:
 axes=np.load('modes5.npz')['axes'];g=np.load('head_geometry.npz');u=g['basis'];ev=g['values']
 def trans(x):
  if name=='raw':return x
  if name=='modes5':return x-x@axes.T@axes
  if name=='frozen16':return x-x@u[:,:16]@u[:,:16].T
  return (x@u)/np.sqrt(ev+1)
 pp=trans(p);nn=trans(n)
 def score(x):
  xx=trans(x)
  ps=xx@pp.T-(pp*pp).sum(-1)/2;ns=xx@nn.T-(nn*nn).sum(-1)/2
  return ps.max(-1)-ns.max(-1)
 v=score(e);av=score(a)
 print(name,'EVIDENCE FX fees',np.round(v[:16,3],1),'othersmax',np.round(v[:16][:,[0,1,2,4]].max(-1),1))
 print('evidence negatives activation',np.round(v[16:].max(-1),1));print('own controls max',np.round(av[20:].max(-1),1))
