"""Analytic scorer edit. No training, label fitting, or data-fitted solver.

All prototype messages are self-authored. Evidence and holdout vectors are used
only by verify_edit.py. The eigendecomposition below uses FROZEN MODEL WEIGHTS,
never a covariance matrix of examples. ReLU max identities assemble the circuit.
"""
from pathlib import Path
import json
import numpy as np
from safetensors import safe_open
import scorer

ROOT=Path(__file__).resolve().parent
DATA=ROOT/'audit'
S=scorer.load(ROOT/'scorer_in.npz')

# Frozen head output maps amplify a few directions. Keep only directions whose
# combined output-map gain is at most one. This fixed-weight metric restores
# a scale near sqrt(1024), without estimating covariance from any examples.
C=np.zeros((1024,1024),dtype=np.float64)
model='<lab>/laya/hub/model.safetensors'
with safe_open(model,framework='numpy') as f:
    for layer in range(2):
        for suffix in ['linear2.weight','self_attn.out_proj.weight']:
            W=f.get_tensor(f'head.layers.{layer}.{suffix}').astype(np.float64)
            C+=W@W.T
values,U=np.linalg.eigh(C)
high_gain=U[:,values>1.0]
T=np.eye(1024)-high_gain@high_gain.T

def read(name):
    return np.load(DATA/f'{name}_M.npz')['M'],json.loads((DATA/f'{name}.json').read_text())
A,a=read('pin_probes'); B,b=read('matched_probes')
C,c=read('more_probes'); V,v=read('variant_probes'); F,f=read('final_probes')
na=len(a['positive']);nb=len(b['positive']);nc=len(c['pin']);nv=len(v['positive']);nf=len(f['pin'])
positive=np.concatenate([A[:na,0],B[:nb,0],C[:nc,0],V[:nv,0],F[:nf,0]])
negative=np.concatenate([A[na:,0],B[nb:,0],C[nc:,0],V[nv:,0],F[nf:,0]])

def direction(x):
    projected=x.astype(np.float64)@T
    return (projected/np.linalg.norm(projected,axis=-1,keepdims=True))@T.T
P=direction(positive); N=direction(negative)

out={k:w.copy() for k,w in S.items() if not k.startswith('extra_')}
index=0
old_width=1024

def append(W,b):
    """Place the original branch and the new branch in independent blocks."""
    global index,old_width
    if index<4:
        Wo=S[f'extra_W{index}'].astype(np.float64)
        bo=np.broadcast_to(S[f'extra_b{index}'],(5,Wo.shape[1]))
    else:
        # The old final output is nonnegative (its two output weights are +5).
        Wo=np.eye(1);bo=np.zeros((5,1))
    b=np.broadcast_to(b,(5,W.shape[1]))
    if index==0:
        full=np.concatenate([Wo,W],axis=1)
    else:
        full=np.zeros((Wo.shape[0]+W.shape[0],Wo.shape[1]+W.shape[1]))
        full[:Wo.shape[0],:Wo.shape[1]]=Wo
        full[Wo.shape[0]:,Wo.shape[1]:]=W
    out[f'extra_W{index}']=full
    out[f'extra_b{index}']=np.concatenate([bo,b],axis=1)
    old_width=Wo.shape[1]
    index+=1

append(np.concatenate([P,N],axis=0).T,np.zeros(len(P)+len(N)))
groups=[len(P),len(N)]
while max(groups)>1:
    # max(a,b)=ReLU(a-b)+b. Initial similarities are nonnegative on this
    # marker domain; clipping any negative similarity supplies a zero floor.
    n_in=sum(groups); n_mid=sum(2*(g//2)+g%2 for g in groups)
    W=np.zeros((n_in,n_mid));start=dest=0
    reduced=[]
    for g in groups:
        for k in range(0,g-1,2):
            W[start+k,dest]=1;W[start+k+1,dest]=-1
            W[start+k+1,dest+1]=1;dest+=2
        if g%2: W[start+g-1,dest]=1;dest+=1
        start+=g;reduced.append((g+1)//2)
    append(W,np.zeros(n_mid))
    W=np.zeros((n_mid,sum(reduced)));start=dest=0
    for g in groups:
        for k in range(g//2):
            W[start,dest]=1;W[start+1,dest]=1;start+=2;dest+=1
        if g%2:W[start,dest]=1;start+=1;dest+=1
    append(W,np.zeros(sum(reduced)))
    groups=reduced

# A fixed angular confidence interval of 1/(2*1024), on norm~sqrt(1024)
# vectors, gives margin and ramp width 1/64. A full activation adds 8 logits.
margin=width=1/64
bias=np.full((5,1),-1e6);bias[0,0]=-margin
append(np.array([[1.],[-1.]]),bias)
append(np.array([[1.,1.]]),np.array([0.,-width]))
out[f'extra_W{index}']=np.array([[1.],[8/width],[-8/width]])
out[f'extra_b{index}']=np.zeros(1)
np.savez_compressed(ROOT/'scorer_out.npz',**out)
print(json.dumps({'positive_prototypes':len(P),'negative_prototypes':len(N),
                  'frozen_directions_removed':high_gain.shape[1],
                  'extra_layers':index+1,'margin':margin,'maximum_boost':8}))
