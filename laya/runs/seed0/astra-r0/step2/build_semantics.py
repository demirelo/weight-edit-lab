import numpy as np
x=np.load('probes_M.npz')['M'].astype(float)
y=np.load('balanced_M.npz')['M'].astype(float)
c=np.load('contrasts_M.npz')['M'].astype(float)
a=np.load('more_contrasts_M.npz')['M'].astype(float)
s=np.load('security_contrasts_M.npz')['M'].astype(float)
base=np.load('directions.npz');basis=list(base['topic_basis'])
def res(d):
 d=d.copy()
 for v in basis:d-=v*(d@v)
 return d
# Topic-balanced context means: PIN has half the weight, login terms half.
contexts=(a[:80].reshape(2,40,5,1024).mean((0,2))+np.concatenate([a[80:],s]).reshape(4,40,5,1024).mean((0,2)))/2
for i in range(1,40):
 d=res(contexts[i]-contexts[0]);basis.append(d/np.linalg.norm(d))
p=(x[:24,0].mean(0)+c[:16,0].mean(0)+a[:80,0].mean(0))/3
n=(x[24:48,0].mean(0)+c[16:32,0].mean(0)+np.concatenate([a[80:,0],s[:,0]]).mean(0))/3
ws=[];bs=[]
for name,neg in [('security',n),('broad',y[:,0].mean(0)),('fx',x[64:,0].mean(0))]:
 d=res(p-neg);w=2*d/(d@d);b=-(p+neg)@w/2;ws.append(w);bs.append(b)
 t=x@w+b
 print(name,'norm',np.linalg.norm(w));print('pin',np.round(t[:24,0],2));print('control',np.round(t[24:64,0],2));print('fx',np.round(t[64:,0],2))
np.savez('semantic_gates.npz',w=np.array(ws).T,b=bs)
