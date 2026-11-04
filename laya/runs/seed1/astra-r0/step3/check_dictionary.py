import json,numpy as np,csv,scorer
R=json.load(open('own_messages.json'))+json.load(open('more_messages.json'))
M=np.concatenate([np.load('own_M.npz')['M'],np.load('more_M.npz')['M']]).astype(float)
D=np.load('old_geometry.npz');U=D['U'];c=(M@U).mean((0,1));X=M@U-c
X/=np.linalg.norm(X,axis=-1,keepdims=True)
posidx=[i for i,r in enumerate(R) if r['group']!='control'];negidx=[i for i,r in enumerate(R) if r['group']=='control']
pos=X[posidx,4];neg=np.concatenate([X[posidx,:4].reshape(-1,X.shape[-1]),X[negidx].reshape(-1,X.shape[-1])])
E=np.load('evidence_M.npz')['M'].astype(float);Y=E@U-c;Y/=np.linalg.norm(Y,axis=-1,keepdims=True)
for i,y in enumerate(Y):
 p=y@pos.T;n=y@neg.T
 print(i,np.round(p.max(-1)-n.max(-1),3),'best account p',R[posidx[p[4].argmax()]]['text'])
np.savez('dictionary.npz',U=U,c=c,pos=pos,neg=neg)
