import numpy as np,json
M=np.load('authored_M.npz')['M'].astype(float); X=M[:,4]; C=np.load('carrier_M.npz')['M'][:,4].astype(float)
r=json.load(open('authored_probes.json'));pos=np.array([a['group'] in ['age','country','geographic_use','service_access'] for a in r])
# Difference vectors of the same greeting with changed punctuation are nuisance probes.
dirs=[C[0],C[1]-C[0],C[2]-C[0],C[3]-C[0],C[5]-C[4],C[7]-C[6],C[9]-C[8],C[11]-C[10]]
Q=[]
for i,d in enumerate(dirs):
 v=d.copy()
 for q in Q: v-=q*(q@v)
 print('nuisance',i,'original/residual norm',np.linalg.norm(d),np.linalg.norm(v))
 Q.append(v/np.linalg.norm(v))
 if i>3:continue
 A=X.copy()
 for q in Q:A-=np.outer(A@q,q)
 nr=np.linalg.norm(A,axis=1)
 A/=nr[:,None];T=A@A.T;np.fill_diagonal(T,-np.inf);delta=T[:,pos].max(1)-T[:,~pos].max(1)
 print('removed',i+1,'pos/neg',np.sum(delta[pos]>0),np.sum(delta[~pos]<0),'norms',np.percentile(nr,[0,25,50,75,100]).round(3),'cos',np.percentile(T[np.isfinite(T)],[0,50,100]).round(3))
 if i==2:
  for j in [0,1,2,3,12,14,24,28,29,41,74]:
   k=T[j].argmax(); print(j,r[j]['text'], 'near', r[k]['text'],T[j,k].round(3),'delta',delta[j].round(3))
