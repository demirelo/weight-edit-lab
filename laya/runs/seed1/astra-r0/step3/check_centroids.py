import numpy as np,json
D=np.load('dictionary.npz');U=D['U'];c=D['c'];R=json.load(open('own_messages.json'))+json.load(open('more_messages.json'));M=np.concatenate([np.load('own_M.npz')['M'],np.load('more_M.npz')['M']]).astype(float);X=M@U-c;X/=np.linalg.norm(X,axis=-1,keepdims=True)
# Semantic groups are explicit authored-message ranges, not evidence labels.
groups=[list(range(0,10))+list(range(72,100)),list(range(10,26))+list(range(100,148)), list(range(72,87))+[0,1,2,3,7,8],list(range(87,100))+[4,5,6,9],list(range(100,122))+[10,16,17,18,22,24,25],list(range(122,148))+[11,12,13,14,15,19,20,21,23]]
C=np.array([X[idx,4].mean(0) for idx in groups]);C/=np.linalg.norm(C,axis=-1,keepdims=True)
P=np.concatenate([D['pos'],C]);N=D['neg']
E=np.load('evidence_M.npz')['M'].astype(float);Y=E@U-c;Y/=np.linalg.norm(Y,axis=-1,keepdims=True)
for i,y in enumerate(Y):
 p=y@P.T;n=y@N.T
 print(i,np.round(p.max(-1)-n.max(-1),3),'best',p.argmax(-1))
np.savez('dictionary_centroids.npz',U=U,c=c,pos=P,neg=N)
