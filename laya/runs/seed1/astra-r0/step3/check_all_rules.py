import numpy as np,json,scorer,re
from build_edit import design,bonus
S,U,c,_,_=design();names=['own','more','final','boundary'];R=sum([json.load(open(f'{n}_messages.json')) for n in names],[]);M=np.concatenate([np.load(f'{n}_M.npz')['M'] for n in names]).astype(float);F=M@U-c;F/=np.linalg.norm(F,axis=-1,keepdims=True)
P=[];N=[]
for i,r in enumerate(R):
 t=r['text'].lower();target=None
 if r['group']!='control':target=4
 elif re.search(r'\bpin\b',t) and ('card' in t or 'debit' in t):target=0
 elif ('rate' in t or 'conversion' in t) and any(k in t for k in ['card','cash','atm','withdrawal','paid in euros']):target=3
 if target is None:N.extend(F[i])
 else:
  P.append(F[i,target]);N.extend(F[i,j] for j in range(5) if j!=target)
P=np.array(P);N=np.array(N)
for name in ['evidence','validation']:
 M=np.load(name+'_M.npz')['M'];d=bonus(M,U,c,P,N);z=scorer.logits(S,M);out=(z+d).argmax(-1)
 print(name)
 for i in range(len(M)):print(i,out[i],np.round(d[i],1))
