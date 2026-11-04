"""Deterministic, hand-specified prototype rule. No optimizer or fitted solver.
The SVD below decomposes existing weights, not examples or evidence labels.
All exemplars come from make_probes.py, make_library.py and make_phrases.py.
"""
import json
import numpy as np
import scorer

S=scorer.load('scorer_in.npz')
# Reuse the exact input subspace of the inherited correction.
U,s,_=np.linalg.svd(S['extra_W0'],full_matrices=False)
U=U[:,s>1e-7]
sets=['probes','library','phrases']
M=np.concatenate([np.load(f'{name}_M.npz')['M'] for name in sets]).astype(np.float64)
groups=sum([json.load(open(f'{name}.json'))['groups'] for name in sets],[])
R=(M@U)@U.T
positive=np.array([g in ('pin','explicit_pin') for g in groups])
center=R.mean(axis=(0,1))
P=R[positive,0]
# Add means of deliberately matched phrase families. These remove incidental
# sentence wording while retaining the PIN/passcode distinction.
pmeans=[];nmeans=[]
phrase_start=len(np.load('probes_M.npz')['M'])+len(np.load('library_M.npz')['M'])
for action in range(10):
 ix=phrase_start+np.arange(action*12,(action+1)*12)
 pmeans.append(R[ix,0].mean(0));nmeans.append(R[ix+150,0].mean(0))
state_groups=[[0,1,2],[3,4,5,18,19,20,24,29],[6,7,10,11,12],[13,14,15],[16,17,21,22,23],[25,26],[8,9,27,28]]
for indices in state_groups:
 ix=phrase_start+120+np.array(indices)
 pmeans.append(R[ix,0].mean(0))
 nmeans.extend([R[ix+150,0].mean(0),R[ix+180,0].mean(0)])
# A broad exchange-rate control mean protects the earlier correction.
texts=sum([json.load(open(f'{name}.json'))['texts'] for name in sets],[])
fx=[i for i,t in enumerate(texts) if not positive[i] and any(k in t.lower() for k in ['exchange rate','conversion rate','currency rate','converted','currency conversion'])]
nmeans.append(R[fx,0].mean(0))
# Other departments on the same PIN requests remain explicit negative options.
N=np.concatenate([R[~positive,0],R[positive,1:].reshape(-1,1024),np.array(nmeans)])
P=np.concatenate([P,np.array(pmeans)])-center
N=N-center
P/=np.linalg.norm(P,axis=1,keepdims=True)
N/=np.linalg.norm(N,axis=1,keepdims=True)
np.savez('final_rule.npz',P=P,N=N,center=center)

# An affine expression has weights w and bias b. The exact max identity is
# max(a,b) = ReLU(a-b) + ReLU(b) - ReLU(-b).
# This implements a maximum tree without an assumed bound or a large offset.
exprs=[[(v,-center@v) for v in P],[(v,-center@v) for v in N]]
branch=[]
while any(len(g)>1 for g in exprs):
 columns=[];biases=[];descriptions=[]
 for group in exprs:
  desc=[]
  for j in range(0,len(group),2):
   wa,ba=group[j]
   k=len(columns)
   if j+1<len(group):
    wb,bb=group[j+1]
    columns.extend([wa-wb,wb,-wb]);biases.extend([ba-bb,bb,-bb]);desc.append([(k,1),(k+1,1),(k+2,-1)])
   else:
    columns.extend([wa,-wa]);biases.extend([ba,-ba]);desc.append([(k,1),(k+1,-1)])
  descriptions.append(desc)
 W=np.column_stack(columns);b=np.array(biases);branch.append((W,b))
 exprs=[]
 for desc in descriptions:
  group=[]
  for terms in desc:
   w=np.zeros(len(columns))
   for k,v in terms:w[k]=v
   group.append((w,0.))
  exprs.append(group)

# Fixed smooth step: 0 outside the positive region, at most +8 logits within it.
# The 1/4-unit transition avoids making near ties into a hard override.
w=32*(exprs[0][0][0]-exprs[1][0][0]);b=32*(exprs[0][0][1]-exprs[1][0][1])
branch.append((np.column_stack([w,w]),np.array([b,b-8.])))
branch.append((np.array([[1.],[-1.]]),np.zeros(1)))
# All following hidden activations are nonnegative identity wires.
old_depth=sum(k.startswith('extra_W') for k in S)
assert len(branch)<old_depth
while len(branch)<old_depth-1:branch.append((np.ones((1,1)),np.zeros(1)))
branch.append((np.ones((1,1)),np.zeros(1)))

T={k:v.copy() for k,v in S.items() if not k.startswith('extra_')}
for i,(nw,nb) in enumerate(branch):
 ow=S[f'extra_W{i}'];ob=S[f'extra_b{i}']
 if i==0:
  w=np.concatenate([ow,nw],axis=1);b=np.concatenate([ob,nb])
 elif i==old_depth-1:
  w=np.concatenate([ow,nw],axis=0);b=ob+nb
 else:
  w=np.zeros((ow.shape[0]+nw.shape[0],ow.shape[1]+nw.shape[1]))
  w[:ow.shape[0],:ow.shape[1]]=ow;w[ow.shape[0]:,ow.shape[1]:]=nw
  b=np.concatenate([ob,nb])
 T[f'extra_W{i}']=w;T[f'extra_b{i}']=b
np.savez_compressed('scorer_out.npz',**T)
print('Wrote scorer_out.npz; positive prototypes',len(P),'negative prototypes',len(N),'layers',len(branch))
