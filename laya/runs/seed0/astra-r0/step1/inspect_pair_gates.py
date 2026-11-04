exec(open('inspect_option.py').read().split('p=A[:,3]')[0])
ws=[];bs=[]
for j in [0,1,2,4]:
 p=A[:,3].mean(0);n=A[:,j].mean(0);d=p-n
 for u in basis:d-=u*(d@u)
 w=d/(d@(p-n));b=-(n@w);ws.append(w);bs.append(b)
G=np.array(ws).T;B=np.array(bs)
np.savez('gates.npz',w=G,b=B)
for name,M,ts in [('probes',P,texts),('evidence',E,[r['text'] for r in csv.DictReader(open('evidence.csv'),delimiter='\t')])]:
 print(name)
 y=(M@G+B).min(-1)
 for i,t in enumerate(ts):print(i,np.round(y[i],2),t)
