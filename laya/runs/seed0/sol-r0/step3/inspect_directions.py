import json, numpy as np
from scorer import load, logits, DEPTS
rows=json.load(open('authored_probes.json')); M=np.load('authored_M.npz')['M'].astype(float)
X=M[:,4]; c=X.mean(0); c/=np.linalg.norm(c)
R=X-np.outer(X@c,c); norms=np.linalg.norm(R,axis=1)
P=R/norms[:,None]
pos=np.array([r['group'] in ['age','country','geographic_use','service_access'] for r in rows])
T=P@P.T
np.fill_diagonal(T,-np.inf)
a=T[:,pos].max(1); b=T[:,~pos].max(1)
z=logits(load('scorer_in.npz'),M.astype('float32'))
print('residual norms',np.percentile(norms,[0,25,50,75,100]))
for i,r in enumerate(rows):
 j=np.argmax(T[i]); pred=a[i]>b[i]
 print('%3d %-16s %+.3f %s %s | near=%s'%(i,r['group'],a[i]-b[i], 'OK' if pos[i]==pred else 'MISS',r['text'],rows[j]['text']))
print('group summaries')
for g in dict.fromkeys(r['group'] for r in rows):
 ix=[i for i,r in enumerate(rows) if r['group']==g]
 print(g,np.round(np.percentile((a-b)[ix],[0,25,50,75,100]),3))
