import numpy as np,csv
from scorer import *
from probes import positive,negative,controls
m=np.load('authored_M.npz')['M']; s=load('scorer_in.npz'); z=logits(s,m)
p=len(positive); n=len(negative)
# A semantic contrast, using only authored messages and the fees option.
a=m[:p,3].mean(0);b=m[p:p+n,3].mean(0)
d=a-b; w=d/np.dot(d,d);bias=-(a+b).dot(w)/2
v=m@w+bias
# Option direction, using authored messages uniformly across semantics.
c=m.mean(0);o=c[3]-c[[0,1,2,4]].mean(0);ow=o/np.dot(o,o); ob=-(c[3]+c[[0,1,2,4]].mean(0)).dot(ow)/2
q=m@ow+ob
print('semantic mean separation',float(np.linalg.norm(d)), 'option',float(np.linalg.norm(o)))
print('semantic ranges by option',v.min(0),v.max(0))
print('option ranges',q.min(0),q.max(0))
for i,t in enumerate(positive+negative+controls):
 print(i,DEPTS[z[i].argmax()],round(float(z[i].max()-z[i,3]),2),'s',np.round(v[i],2),'o',np.round(q[i],2),t)
e=np.load('evidence_M.npz')['M'];ev=e@w+bias;eq=e@ow+ob
print('EVIDENCE')
for i,r in enumerate(csv.DictReader(open('evidence.csv'),delimiter='\t')):print(i,'s',np.round(ev[i],2),'o',np.round(eq[i],2),r['text'])
np.savez('directions.npz',w=w,bias=bias,ow=ow,ob=ob)
