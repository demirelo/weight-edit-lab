import numpy as np,csv,json
from scorer import *
x=np.load('probes_M.npz')['M'].astype(float);y=np.load('balanced_M.npz')['M'].astype(float)
a=np.load('directions.npz');q=a['topic_basis'];ow=a['ow'];ob=a['ob']
def diff(p,n):
 d=p-n;d-=d@q.T@q;w=2*d/(d@d);return w,-(p+n)@w/2
# Require support from a security contrast and from a broad topic contrast.
w1,b1=diff(x[:24,0].mean(0),x[24:48,0].mean(0))
w2,b2=diff(x[:24,0].mean(0),y[:,0].mean(0))
w3,b3=diff(x[:24,0].mean(0),x[64:,0].mean(0))
w=np.column_stack([w1,w2,w3,ow.T]);b=np.r_[b1,b2,b3,ob]
offset=np.array([.3,.3,0,.4,.4,.4,.4]);gain=np.array([12,12,12,40,40,40,40])
np.savez('patch_gates.npz',w=w*gain,b=(b+offset)*gain)
s=load('scorer_in.npz')
for name,m,rows in [('evidence',np.load('evidence_M.npz')['M'],list(csv.DictReader(open('evidence.csv'),delimiter='\t'))),('probes',x,json.load(open('probes.json'))),('balanced',y,json.load(open('balanced.json')))]:
 z=logits(s,m);delta=np.clip((m@w+b+offset)*gain,0,8).min(-1);zz=z+delta
 print(name,'changed',sum(z.argmax(-1)!=zz.argmax(-1)))
 for i,(z0,z1,d,r) in enumerate(zip(z,zz,delta,rows)):
  if name=='evidence' or z0.argmax()!=z1.argmax():print(i,DEPTS[z0.argmax()],DEPTS[z1.argmax()],np.round(d,1),r['text'])
