import numpy as np
from scorer import *
a=np.load('authored_M.npz')['M'].astype(float);m=np.load('pairs_M.npz')['M'].astype(float);e=np.load('evidence_M.npz')['M'].astype(float)
# All contrasts below come solely from authored messages.
contrasts=[a[49,1]-a[49,[0,2,3,4]].mean(0),a[[62,65,66],3].mean(0)-a[[62,65,66]][:,[0,1,2,4]].mean((0,1)),a[[40,41,43,45],0].mean(0)-a[[40,41,43,45]][:,[1,2,3,4]].mean((0,1)),a[[55,57,59],2].mean(0)-a[[55,57,59]][:,[0,1,3,4]].mean((0,1)),a[[69,70,73],4].mean(0)-a[[69,70,73]][:,[0,1,2,3]].mean((0,1))]
axes=[]
p=m[:24].mean((0,1));n=m[24:48].mean((0,1))
for mode,r in enumerate(contrasts):
 for q in axes:r-=q*r.dot(q)
 r/=np.linalg.norm(r);axes.append(r)
 d=p-n
 for q in axes:d-=q*d.dot(q)
 w=d/d.dot(d);bias=-(p+n).dot(w)/2
 v=a@w+bias;ev=e@w+bias
 print('modes',mode+1,'d norm',np.linalg.norm(d));print('pos',np.round(v[:20,3],2));print('neg',np.round(v[20:40,3],2));print('controls',np.round(v[40:,3],2));print('ev',np.round(ev[:16,3],2))
 np.savez('modes'+str(mode+1)+'.npz',w=w,bias=bias,axes=np.array(axes))
