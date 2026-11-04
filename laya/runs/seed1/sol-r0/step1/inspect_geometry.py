import numpy as np
m=np.load('pairs_M.npz')['M'].astype(float);a=np.load('authored_M.npz')['M'].astype(float);e=np.load('evidence_M.npz')['M'].astype(float);u=np.load('frozen_geometry.npz')['basis']
p=m[:24].mean((0,1));n=m[24:48].mean((0,1))
for count in [2,4,8,16,32,64]:
 b=u[:,:count];d=p-n;d-=b@(b.T@d);w=d/d.dot(d);bias=-(p+n).dot(w)/2
 v=a@w+bias;ev=e@w+bias
 print('remove',count,'norm',np.linalg.norm(d),'optionmeans',np.round(v.mean(0),2));print('pos',np.round(v[:20,3],2));print('neg',np.round(v[20:40,3],2));print('controls',np.round(v[40:,3],2));print('ev',np.round(ev[:16,3],2))
