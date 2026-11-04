exec(open('inspect_probes.py').read().split('# Each direction')[0])
u=P.mean((0,1)); u=u/np.linalg.norm(u)
# A nuisance direction for general option relevance from unambiguous controls.
labels=[0,0,0,0,0,0,2,2,2,4,4,4,4,4,4,3,3,3,3,3,0,1,1,1,1,1,0,1,3,0,0,0]
Q=P[32:]; good=Q[np.arange(len(Q)),labels].mean(0); bad=np.array([np.delete(q,l,axis=0).mean(0) for q,l in zip(Q,labels)]).mean(0)
r=good-bad; r=r-u*(r@u); r=r/np.linalg.norm(r)
def clean(x):
 return x-(x@u)[...,None]*u-(x@r)[...,None]*r
C=clean(P)
p=C[:16,3].mean(0); n=C[16:32,3].mean(0); d=p-n
w=2*d/(d@d); b=-((p+n)/2)@w
p2=C[:,3].mean(0); n2=C[:,[0,1,2,4]].mean((0,1)); d2=p2-n2
v=2*d2/(d2@d2); c=-((p2+n2)/2)@v
np.savez('directions.npz',w=w,b=b,v=v,c=c)
for label,M,ts in [('probes',P,texts),('evidence',E,[r['text'] for r in csv.DictReader(open('evidence.csv'),delimiter='\t')])]:
 print('\n',label)
 x=M@w+b; y=M@v+c
 for i,t in enumerate(ts): print(i,'fx',np.round(x[i],2),'option',np.round(y[i],2),t)
