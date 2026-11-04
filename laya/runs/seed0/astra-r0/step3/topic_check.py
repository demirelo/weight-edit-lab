import numpy as np,json
from scorer import *
M=np.load('probes_M.npz')['M'].astype(float); B=np.load('semantic_geometry.npz')['B'];X=M-(M@B.T)@B
# Separate option identity and message topic using paired option differences.
O=X[:25].mean(0); C=[]
for raw in [O[j]-O[4] for j in range(4)]:
 d=raw.copy()
 for b in C:d-=d@b*b
 C.append(d/np.linalg.norm(d))
C=np.array(C)
def unit(x):return x/np.linalg.norm(x,axis=-1,keepdims=True)
def topic(x):return x-(x@C.T)@C
U=unit(topic(X).mean(1));p=U[:25];n=U[25:]
# Paired department gates; zero at each midpoint, unit at each department mean.
dirs=[];bias=[]
for j in range(4):
 d=2*(O[4]-O[j])/np.sum((O[4]-O[j])**2);dirs.append(d);bias.append(-(O[4]+O[j])@d/2)
for file in ['probes','heldout']:
 Z=np.load(file+'_M.npz')['M'].astype(float);R=Z-(Z@B.T)@B;V=topic(R)
 sem=np.maximum(0,V@p.T).max(-1)-np.maximum(0,V@n.T).max(-1)
 gate=np.maximum(0,(R@np.array(dirs).T+np.array(bias)).min(-1))
 delta=np.minimum(12,np.maximum(0,np.minimum(16*sem,12*gate)))
 old=logits(load('scorer_in.npz'),Z);new=old+delta
 print(file)
 for t,o,k,a in zip(sum(json.load(open(file+'.json')).values(),[]),old.argmax(-1),new.argmax(-1),delta):
  print(t,DEPTS[o],'=>',DEPTS[k],np.round(a,1))
