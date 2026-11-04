exec(open('inspect_probes.py').read().split('# Each direction')[0])
A=np.load('paired_M.npz')['M'].astype(np.float64)
basis=[]
def add(v):
 v=v.astype(np.float64).copy()
 for u in basis:v-=u*(v@u)
 basis.append(v/np.linalg.norm(v))
add(A.mean((0,1)))
for j in range(5):add(A[:24,j].mean(0)-A[24:,j].mean(0))
for i,j in [(36,0),(38,2),(41,4),(50,3),(20,1)]:add(P[i,j]-np.delete(P[i],j,0).mean(0))
p=A[:,3].mean(0);n=A[:,[0,1,2,4]].mean((0,1));d=p-n
for u in basis:d-=u*(d@u)
w=d/(d@(p-n));b=-(n@w)
np.savez('option.npz',w=w,b=b)
for label,M,ts in [('probes',P,texts),('evidence',E,[r['text'] for r in csv.DictReader(open('evidence.csv'),delimiter='\t')])]:
 print('\n',label)
 x=M@w+b
 for i,t in enumerate(ts): print(i,np.round(x[i],2),t)
