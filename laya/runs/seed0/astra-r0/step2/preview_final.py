import numpy as np,csv,json
from scorer import *
a=np.load('directions.npz');g=np.load('semantic_gates.npz');orig=np.load('topic_directions.npz')
s=load('scorer_in.npz')
def correction(m):
 sem=m@g['w']+g['b'];v=m@orig['w'][3]+orig['b'][3]
 option=np.maximum(0,40*(m@a['ow'].T+a['ob']+.4)).min(-1)
 primary=np.minimum.reduce([10*(sem[...,0]+.3),6*(v+.8),12*(sem[...,1]+.2),16*sem[...,2],option])
 strong=np.minimum.reduce([20*(v-1),16*(sem[...,1]-.3),16*sem[...,2],option])
 return np.clip(np.maximum(primary,strong),0,8)
for name,m,rows in [('evidence',np.load('evidence_M.npz')['M'],list(csv.DictReader(open('evidence.csv'),delimiter='\t'))),('probes',np.load('probes_M.npz')['M'],json.load(open('probes.json'))),('balanced',np.load('balanced_M.npz')['M'],json.load(open('balanced.json')))]:
 z=logits(s,m);delta=correction(m);zz=z+delta
 print(name,'changed',sum(z.argmax(-1)!=zz.argmax(-1)))
 for i,(z0,z1,d,r) in enumerate(zip(z,zz,delta,rows)):
  if name=='evidence' or z0.argmax()!=z1.argmax():print(i,DEPTS[z0.argmax()],DEPTS[z1.argmax()],np.round(d,1),r['text'])
