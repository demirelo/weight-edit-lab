import numpy as np
from scorer import *
from validation import fx,other
from probes import positive,negative,controls
from pairs import pos,neg,neutral
a=np.load('authored_M.npz')['M'].astype(float);m=np.load('pairs_M.npz')['M'].astype(float);v=np.load('validation_M.npz')['M'].astype(float);e=np.load('evidence_M.npz')['M'].astype(float)
g=np.load('head_geometry.npz');u=g['basis'];ev=g['values']
p=np.concatenate([a[:20,3],m[:24,3]])
n=np.concatenate([a[:20][:,[0,1,2,4]].reshape(-1,1024),m[:24][:,[0,1,2,4]].reshape(-1,1024),a[20:].reshape(-1,1024),m[24:].reshape(-1,1024)])
c=np.concatenate([p,n]).mean(0)
t=lambda x:((x-c)@u)/np.sqrt(ev+1)
pp=t(p);nn=t(n)
def score(x):
 xx=t(x);return (xx@pp.T-(pp*pp).sum(-1)/2).max(-1)-(xx@nn.T-(nn*nn).sum(-1)/2).max(-1)
z=logits(load('scorer_in.npz'),v);q=score(v);zz=z+5*np.clip(q+5,0,1)
print('FX',np.sum(zz[:len(fx)].argmax(-1)==3),'/',len(fx),'other preservation',np.sum(zz[len(fx):].argmax(-1)==z[len(fx):].argmax(-1)),'/',len(other))
for i,text in enumerate(fx+other):
 print('FX' if i<len(fx) else 'OTHER',DEPTS[z[i].argmax()],DEPTS[zz[i].argmax()],'margin',np.round(q[i],1),text)
