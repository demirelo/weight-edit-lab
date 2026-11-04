exec(open('inspect_probes.py').read().split('# Each direction')[0])
# Remove background and non-target option contrast directions. These all
# come from authored messages, never from the supplied evidence.
basis=[]
def add(v):
 v=v.astype(np.float64).copy()
 for u in basis: v-=u*(v@u)
 if np.linalg.norm(v)>1e-6: basis.append(v/np.linalg.norm(v))
for j in [0,1,2,4]:
 add(P[:,j].mean(0))
 add(P[:16,j].mean(0)-P[16:32,j].mean(0))
add(P[16:,3].mean(0))
# Generic high-confidence matching-option signal.
add(P[50:52,3].mean(0)-P[32:47,3].mean(0))
d=P[:16,3].mean(0)-P[16:32,3].mean(0)
for u in basis: d-=u*(d@u)
p=P[:16,3].mean(0)@d; n=P[16:32,3].mean(0)@d
w=d/(p-n); b=-n/(p-n)
np.savez('directions.npz',w=w,b=b)
for label,M,ts in [('probes',P,texts),('evidence',E,[r['text'] for r in csv.DictReader(open('evidence.csv'),delimiter='\t')])]:
 print('\n',label)
 x=M@w+b
 for i,t in enumerate(ts): print(i,np.round(x[i],2),t)
