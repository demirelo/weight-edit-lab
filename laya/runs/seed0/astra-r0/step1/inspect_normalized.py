exec(open('inspect_probes.py').read().split('# Each direction')[0])
# Normalize each authored marker before taking a semantic contrast. Raw markers
# share a large positive common direction; it supplies a linear scale estimate.
C=P/np.linalg.norm(P,axis=-1,keepdims=True)
u=C.mean((0,1)); u/=np.linalg.norm(u)
basis=[]
def add(v):
 v=v.astype(np.float64).copy()
 for x in basis: v-=x*(v@x)
 if np.linalg.norm(v)>1e-8: basis.append(v/np.linalg.norm(v))
add(u)
for j in [0,1,2,4]:
 add(C[:,j].mean(0)-C[:,3].mean(0))
 add(C[:16,j].mean(0)-C[16:32,j].mean(0))
add(C[50:52,3].mean(0)-C[32:47,3].mean(0))
d=C[:16,3].mean(0)-C[16:32,3].mean(0)
for v in basis: d-=v*(d@v)
p=C[:16,3].mean(0)@d; n=C[16:32,3].mean(0)@d
w=(d-n*u)/(p-n)
np.savez('directions.npz',w=w,u=u)
for label,M,ts in [('probes',P,texts),('evidence',E,[r['text'] for r in csv.DictReader(open('evidence.csv'),delimiter='\t')])]:
 print('\n',label)
 x=(M@w)/(M@u)
 for i,t in enumerate(ts): print(i,np.round(x[i],2),t)
