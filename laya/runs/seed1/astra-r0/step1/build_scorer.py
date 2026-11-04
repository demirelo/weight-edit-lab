"""Compile fixed reference comparisons and department gates; no fitting."""
import numpy as np
from scorer import load,save
s=load('scorer_in.npz');d=np.load('final_directions.npz');op=np.load('option_identity.npz')
p=d['pos'];n=d['neg'];layers=[]
# A shared offset keeps the max-tree inputs nonnegative. It cancels exactly.
w=np.concatenate([p.T,n.T,op['W']],axis=1)
b=np.r_[np.full(len(p)+len(n),1000.0),op['b']+1000.0]
layers.append((w,b));identity=np.eye(w.shape[1])
groups=[list(identity[:len(p)]),list(identity[len(p):len(p)+len(n)])]
groups += [[identity[len(p)+len(n)+j]] for j in range(4)]
while any(len(g)>1 for g in groups):
 columns=[];spec=[]
 for group in groups:
  entries=[]
  for i in range(0,len(group),2):
   j=len(columns)
   if i+1<len(group):
    columns.extend([group[i]-group[i+1],group[i+1]]);entries.append([j,j+1])
   else:columns.append(group[i]);entries.append([j])
  spec.append(entries)
 matrix=np.stack(columns,axis=1);layers.append((matrix,np.zeros(matrix.shape[1])))
 groups=[]
 for entries in spec:
  group=[]
  for indices in entries:
   expr=np.zeros(matrix.shape[1]);expr[indices]=1;group.append(expr)
  groups.append(group)
# Rectify the semantic margin and four department margins; include a fixed cap.
cols=[16*(groups[0][0]-groups[1][0])]+[16*groups[j][0] for j in range(2,6)]
cols.append(np.zeros_like(cols[0]))
layers.append((np.stack(cols,axis=1),np.array([0.,-16000.,-16000.,-16000.,-16000.,6.])))
exprs=list(np.eye(6))
# min(a,b)=a-ReLU(a-b) for nonnegative a and b.
while len(exprs)>1:
 columns=[];spec=[]
 for i in range(0,len(exprs),2):
  j=len(columns)
  if i+1<len(exprs):
   columns.extend([exprs[i],exprs[i]-exprs[i+1]]);spec.append((j,j+1))
  else:columns.append(exprs[i]);spec.append((j,))
 matrix=np.stack(columns,axis=1);layers.append((matrix,np.zeros(matrix.shape[1])))
 exprs=[]
 for indices in spec:
  expr=np.zeros(matrix.shape[1]);expr[indices[0]]=1
  if len(indices)==2:expr[indices[1]]=-1
  exprs.append(expr)
layers.append((exprs[0][:,None],np.zeros(1)))
for i,(w,b) in enumerate(layers):s[f'extra_W{i}']=w;s[f'extra_b{i}']=b
np.savez_compressed('scorer_out.npz',**s)
print('Saved scorer_out.npz;',len(layers),'extra layers;',sum(w.size+b.size for w,b in layers),'extra scalars')
