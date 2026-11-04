import numpy as np, json, csv
from scorer import *
P=np.load('probes_M.npz')['M']; E=np.load('evidence_M.npz')['M']; data=json.load(open('probes.json')); texts=sum(data.values(),[])
# Each direction uses only the manually authored contrasts.
p=P[:16,3].mean(0); n=P[16:32,3].mean(0); d=p-n
w=2*d/(d@d); b=-((p+n)/2)@w
p2=P[:,3].mean(0); n2=P[:,[0,1,2,4]].mean((0,1)); d2=p2-n2
v=2*d2/(d2@d2); c=-((p2+n2)/2)@v
np.savez('directions.npz',w=w,b=b,v=v,c=c)
for label,M,ts in [('probes',P,texts),('evidence',E,[r['text'] for r in csv.DictReader(open('evidence.csv'),delimiter='\t')])]:
 print('\n',label)
 x=M@w+b; y=M@v+c
 for i,t in enumerate(ts): print(i,'fx',np.round(x[i],2),'option',np.round(y[i],2),t)
