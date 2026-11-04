import numpy as np
x=np.load('probes_M.npz')['M'].astype(float);y=np.load('balanced_M.npz')['M'].astype(float);f=np.load('final_contrasts_M.npz')['M'].astype(float);q=np.load('invariant_direction.npz')['q']
ws=[];bs=[]
for name,p,n in [('short_security',f[:14,0].mean(0),f[14:28,0].mean(0)),('short_other',f[:14,0].mean(0),np.concatenate([f[28:42,0],y[:,0]]).mean(0)),('identity',x[:24,0].mean(0),f[42:50,0].mean(0)),('closure',x[:24,0].mean(0),f[50:,0].mean(0))]:
 d=p-n;d-=d@q.T@q;w=2*d/(d@d);b=-(p+n)@w/2;ws.append(w);bs.append(b)
 print(name,'own pin range',np.round([np.min(x[:24,0]@w+b),np.max(x[:24,0]@w+b)],2))
np.savez('final_contrast_gates.npz',w=np.array(ws).T,b=bs)
