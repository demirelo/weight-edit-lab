import numpy as np
from build_scorer import make_prototypes
from scorer import *
p,n=make_prototypes();g=np.load('head_geometry.npz');u=g['basis'];ev=g['values'];pcount=len(p)
e=np.load('evidence_M.npz')['M'];h=np.load('holdout_M.npz')['M'];s=load('scorer_in.npz');z=logits(s,h)
for metric in ['raw','whiten']:
 for centername in ['zero','mean']:
  c=0 if centername=='zero' else np.concatenate([p,n]).mean(0)
  def t(x):return x-c if metric=='raw' else ((x-c)@u)/np.sqrt(ev+1)
  pp=t(p);nn=t(n);pp/=np.linalg.norm(pp,axis=-1,keepdims=True);nn/=np.linalg.norm(nn,axis=-1,keepdims=True)
  def score(x):
   xx=t(x);return (xx@pp.T).max(-1)-(xx@nn.T).max(-1)
  he=score(h);ee=score(e)
  print(metric,centername,'evidence fx',np.round(ee[:16,3],3),'nonFX max',np.round(ee[16:].max(-1),3))
  b=z+6*np.clip(he,0,1)
  print('holdout fx',sum(b[:20].argmax(-1)==3),'/20; unchanged',sum(b[20:].argmax(-1)==z[20:].argmax(-1)),'/44; fx margin',np.round(he[:20,3],2),'nonFX margin',np.round(he[20:,3],2))
