exec(open('inspect_probes.py').read().split('# Each direction')[0])
A=np.load('paired_M.npz')['M'].astype(np.float64)
# Three nuisance directions: common activation, clear matches, ambiguous matches.
basis=[]
def add(v):
 v=v.astype(np.float64).copy()
 for u in basis: v-=u*(v@u)
 basis.append(v/np.linalg.norm(v))
add(P.mean((0,1)))
strong=[(36,0),(38,2),(41,4),(50,3),(20,1)]
add(np.mean([P[i,j]-np.delete(P[i],j,0).mean(0) for i,j in strong],0))
# Common nuisance between related options on an ambiguous transaction complaint.
add(P[16:32,1].mean(0)-P[16:32,[0,2,4]].mean((0,1)))
def clean(d):
 for u in basis:d=d-u*(d@u)
 return d
# Shared exchange-rate language across all options.
p=A[:24].mean((0,1));n=A[24:].mean((0,1));d=clean(p-n)
w=d/(d@(p-n)); b=-(n@w)
# Option identity from paired texts; remove the same general relevance axes.
p=A[:,3].mean(0);n=A[:,[0,1,2,4]].mean((0,1));d=clean(p-n)
v=d/(d@(p-n));c=-(n@v)
np.savez('directions.npz',w=w,b=b,v=v,c=c)
for label,M,ts in [('probes',P,texts),('evidence',E,[r['text'] for r in csv.DictReader(open('evidence.csv'),delimiter='\t')])]:
 print('\n',label)
 x=M@w+b;y=M@v+c
 for i,t in enumerate(ts): print(i,'fx',np.round(x[i],2),'fee',np.round(y[i],2),t)
