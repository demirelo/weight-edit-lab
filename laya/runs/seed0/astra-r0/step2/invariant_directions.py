import numpy as np
base=np.load('directions.npz');q=list(base['topic_basis'])
c=np.load('more_contrasts_M.npz')['M'].astype(float)
x=np.load('probes_M.npz')['M'].astype(float)
def res(d):
 d=d.copy()
 for u in q:d-=u*(u@d)
 return d
# Each vector is a difference between equally PIN/passcode-balanced means.
# Remove shared phrasing effects, preserving the topic difference.
contexts=c.reshape(4,40,5,1024).mean((0,2))
for i in range(1,40):
 d=res(contexts[i]-contexts[0]);q.append(d/np.linalg.norm(d))
p=c[:80].mean((0,1));n=c[80:].mean((0,1));d=res(p-n);w=2*d/(d@d);b=-(p+n)@w/2
np.savez('invariant_direction.npz',w=w,b=b,q=q)
print('norm',np.linalg.norm(w))
for name,m in [('pin',x[:24]),('control',x[24:64]),('fx',x[64:])]:print(name,np.round((m@w+b)[:,0],2))
