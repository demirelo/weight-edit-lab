import numpy as np
from build_edit import design
S,U,c,P,N=design();M=np.concatenate([np.load(f'{n}_M.npz')['M'] for n in ['own','more','final']]).astype(float);E=np.load('evidence_M.npz')['M'];V=np.load('validation_M.npz')['M'];X=M@U;Y=E@U;Z=V@U
for j in range(4):
 d=X[:,4]-X[:,j];d/=np.linalg.norm(d,axis=-1,keepdims=True)
 w=d.mean(0);w/=np.linalg.norm(w)
 # Difference of means on unit contrast directions, centered at pair midpoints.
 b=-.5*(X[:,4]+X[:,j]).mean(0)@w
 print('j',j,'own acc quantiles',np.percentile(X[:,4]@w+b,[0,10,50,90,100]),'other',np.percentile(X[:,j]@w+b,[0,10,50,90,100]))
 print('ev',np.round(Y@w+b,1));print('val',np.round((Z@w+b)[:20],1))
