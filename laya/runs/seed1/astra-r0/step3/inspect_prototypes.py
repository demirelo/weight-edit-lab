import numpy as np,json,csv
D=np.load('old_geometry.npz');U=D['U'];c=D['c'];M=np.load('own_M.npz')['M'].astype(float); E=np.load('evidence_M.npz')['M'].astype(float); R=json.load(open('own_messages.json'))
X=M@U-c;Y=E@U-c
X/=np.linalg.norm(X,axis=-1,keepdims=True);Y/=np.linalg.norm(Y,axis=-1,keepdims=True)
pos=X[:26,4];neg=np.concatenate([X[:26,:4].reshape(-1,X.shape[-1]),X[26:].reshape(-1,X.shape[-1])])
print('evidence max positive minus negative')
for i,y in enumerate(Y):
 p=y@pos.T;n=y@neg.T
 print(i,np.round(p.max(-1)-n.max(-1),3),'best p',p.argmax(-1))
