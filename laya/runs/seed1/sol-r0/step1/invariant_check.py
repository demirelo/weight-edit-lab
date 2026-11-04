import numpy as np
from build_scorer import make_prototypes
from scorer import *
p,n=make_prototypes();m=np.load('pairs_M.npz')['M'].astype(float);e=np.load('evidence_M.npz')['M'];h=np.load('holdout_M.npz')['M'];s=load('scorer_in.npz');z=logits(s,h)
# Remove only variation among eight authored contexts of the same request.
# Fixed differences of means; no labels, covariance fitting, or optimizer.
for families in [[3],[3,4,5]]:
 axes=[]
 for family in families:
  block=m[family*8:(family+1)*8]
  for k in range(5):
   for i in range(1,8):
    d=block[i,k]-block[0,k]
    for ax in axes:d-=ax*d.dot(ax)
    d/=np.linalg.norm(d);axes.append(d)
 axes=np.array(axes)
 pp=p-p@axes.T@axes;nn=n-n@axes.T@axes
 def score(x):
  xx=x-x@axes.T@axes
  return (xx@pp.T-.5*(pp*pp).sum(-1)).max(-1)-(xx@nn.T-.5*(nn*nn).sum(-1)).max(-1)
 ee=score(e);he=score(h)
 print('axes',len(axes),'norm',np.linalg.norm(pp-p.mean(0),axis=-1).mean())
 print('evidence FX',np.round(ee[:16,3],2),'othersmax',np.round(ee[16:].max(-1),2))
 b=z+6*np.clip(he,0,1)
 print('holdout fx',sum(b[:20].argmax(-1)==3),'/20 preserved',sum(b[20:].argmax(-1)==z[20:].argmax(-1)),'/44','margins',np.round(he[20:,3],1))
 np.savez('invariant'+str(len(axes))+'.npz',axes=axes)
