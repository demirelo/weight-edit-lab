exec(open('inspect_pair_direction.py').read().split('d=A[:24,3]')[0])
groups=[[0,1,6,7,10,11,18,19,20,21],[2,3,8,9,12,13,16,17,22,23],[4,5,14,15]]
ws=[];bs=[]
for g in groups:
 p=A[g,3].mean(0);n=A[np.array(g)+24,3].mean(0);d=p-n
 for u in basis:d-=u*(d@u)
 w=d/(d@(p-n));b=-(n@w);ws.append(w);bs.append(b)
np.savez('multi.npz',w=np.array(ws).T,b=np.array(bs))
O=np.load('option.npz');S=load('scorer_in.npz')
for name,M,ts in [('probes',P,texts),('evidence',E,[r['text'] for r in csv.DictReader(open('evidence.csv'),delimiter='\t')])]:
 x=(M@np.array(ws).T+bs).max(-1);y=M@O['w']+O['b'];z=logits(S,M)
 bonus=np.minimum(3,6*np.minimum(np.maximum(0,x-.15),np.maximum(0,y-.5)));zz=z+bonus
 print(name)
 for i,t in enumerate(ts):
  if name=='evidence' or z[i].argmax()!=zz[i].argmax():print(i,DEPTS[z[i].argmax()],DEPTS[zz[i].argmax()],np.round(x[i],2),t)
