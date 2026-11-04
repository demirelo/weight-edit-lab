"""Compile a hand-designed eligibility rule into ordinary ReLU weights.

Only fixed scorer weights and embeddings of authored reference messages enter
this construction. Evidence and held-out checks do not enter it. Loops below
assemble exact arithmetic circuits; none optimize or update fitted parameters.
"""
import numpy as np
from scorer import load,save
from eligibility_geometry import geometry,DEPARTMENT,mean_rules,RESCUE

MARGIN=.025
PROXIMITY=.40
BONUS=16.

def correction_layers(target='eligibility'):
 V,c,P,pos,_=geometry(target)
 P=np.concatenate([P[pos],P[~pos]],axis=0)
 npos=int(pos.sum()); nneg=int((~pos).sum()); rank=V.shape[1]
 # Scores are dot products with unit directions from authored vectors minus
 # their common mean. Absolute coordinates give a homogeneous norm estimate.
 mean_W,mean_b=mean_rules(target)
 W=np.concatenate([V@P.T,mean_W,V,-V],axis=1)
 b=np.tile(np.concatenate([-c@P.T,mean_b+4.,-c,c]),(5,1))
 layers=[(W,b)]
 groups=[npos,nneg,mean_W.shape[1]];width=len(P)+mean_W.shape[1]+2*rank
 first=True
 # max(a,b) = ReLU(a-b) + b, for nonnegative a,b.
 while max(groups)>1:
  outputs=[]; nextgroups=[]; offset=0
  for count in groups:
   g=[]
   for j in range(0,count,2):
    a=offset+j
    if j+1<count:
     d=np.zeros(width);d[a]=1;d[a+1]=-1
     carry=np.zeros(width);carry[a+1]=1
     outputs.extend([d,carry]);g.append(2)
    else:
     carry=np.zeros(width);carry[a]=1
     outputs.append(carry);g.append(1)
   nextgroups.append(g);offset+=count
  q=np.zeros(width)
  if first:q[offset:]=np.sqrt(np.pi/(2*rank))
  else:q[-1]=1
  outputs.append(q)
  A=np.stack(outputs,axis=1);layers.append((A,np.zeros((5,A.shape[1]))))
  out=[];k=0
  for g in nextgroups:
   for count in g:
    v=np.zeros(A.shape[1]);v[k:k+count]=1;out.append(v);k+=count
  q=np.zeros(A.shape[1]);q[-1]=1;out.append(q)
  B=np.stack(out,axis=1);layers.append((B,np.zeros((5,B.shape[1]))))
  groups=[len(g) for g in nextgroups];width=B.shape[1];first=False
 assert groups==[1,1,1] and width==4
 # Five nonnegative margins form two conjunctions: the reference rule and
 # a mean-direction rule guarded by proximity and a weak reference margin.
 threshold,weak,rescue_proximity=RESCUE[target]
 W=np.array([[1.,1.,0.,1.,1.],[-1.,0.,0.,-1.,0.],
             [0.,0.,2.,0.,0.],[-MARGIN,-PROXIMITY,0.,weak,-rescue_proximity]])
 b=np.zeros((5,5));b[:,2]=-2*(4.+threshold)
 b[np.arange(5)!=DEPARTMENT[target]]=-1e6
 layers.append((W,b))
 # [a,b,c,d,e] -> [a,ReLU(a-b),c,ReLU(c-d),e]
 W=np.array([[1,1,0,0,0],[0,-1,0,0,0],[0,0,1,1,0],[0,0,0,-1,0],[0,0,0,0,1]],float)
 layers.append((W,np.zeros((5,5))))
 # -> [min(a,b), min(c,d), e]
 W=np.array([[1,0,0],[-1,0,0],[0,1,0],[0,-1,0],[0,0,1]],float)
 layers.append((W,np.zeros((5,3))))
 # -> [h,j,ReLU(j-e)] -> [h,min(j,e)]
 layers.append((np.array([[1,0,0],[0,1,1],[0,0,-1]],float),np.zeros((5,3))))
 layers.append((np.array([[1,0],[0,1],[0,-1]],float),np.zeros((5,2))))
 # max(h,rescue) = ReLU(h-rescue)+rescue.
 layers.append((np.array([[1,0],[-1,1]],float),np.zeros((5,2))))
 layers.append((np.ones((2,1)),np.zeros((5,1))))
 # bonus = 16*(ReLU(h)-ReLU(h-1)), bounded between 0 and 16.
 layers.append((np.ones((1,2)),np.tile([0.,-1.],(5,1))))
 layers.append((np.array([[BONUS],[-BONUS]]),np.zeros((5,1))))
 return layers

def build():
 S=load('scorer_in.npz');old=[];i=0
 while f'extra_W{i}' in S:
  old.append((S[f'extra_W{i}'],S[f'extra_b{i}']));i+=1
 branches=[old]+[correction_layers(target) for target in DEPARTMENT]
 # Insert identity layers BEFORE each branch's final affine map, preserving
 # signed outputs and all original biases. Hidden states are nonnegative.
 depth=max(map(len,branches))
 for branch in branches:
  while len(branch)<depth:
   d=branch[-1][0].shape[0]
   branch.insert(-1,(np.eye(d),np.zeros((5,d))))
 out={k:v.copy() for k,v in S.items() if not k.startswith('extra_')}
 for i in range(depth):
  matrices=[branch[i][0] for branch in branches]
  biases=[np.broadcast_to(branch[i][1],(5,branch[i][0].shape[1])) for branch in branches]
  if i==0:
   W=np.concatenate(matrices,axis=1);bias=np.concatenate(biases,axis=1)
  elif i==depth-1:
   W=np.concatenate(matrices,axis=0);bias=sum(biases)
  else:
   W=np.zeros((sum(A.shape[0] for A in matrices),sum(A.shape[1] for A in matrices)))
   ro=co=0
   for A in matrices:
    W[ro:ro+A.shape[0],co:co+A.shape[1]]=A
    ro+=A.shape[0];co+=A.shape[1]
   bias=np.concatenate(biases,axis=1)
  out[f'extra_W{i}']=W;out[f'extra_b{i}']=bias
 np.savez_compressed('scorer_out.npz',**out)
 return out
if __name__=='__main__':
 S=build()
 print('Wrote scorer_out.npz; layers:',[(S[f'extra_W{i}'].shape) for i in range(sum(k.startswith('extra_W') for k in S))])
