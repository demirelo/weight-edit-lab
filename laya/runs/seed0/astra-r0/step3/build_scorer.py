"""Construct a fixed geometric rule from author-written messages; no training."""
import numpy as np
import json
from scorer import load, save, logits

M=np.load('probes_M.npz')['M'].astype(np.float64)
N=np.load('neutral_M.npz')['M'].astype(np.float64)
# Gram-Schmidt removes explicitly chosen nuisance directions: the common
# marker offset, changes between greetings within each department, and strong
# unrelated match-strength contrasts. There is no optimized loss or solver.
basis=[]
raw_directions=[N.mean((0,1))]
raw_directions += [N[i,j]-N[0,j] for i in range(1,len(N)) for j in range(5)]
raw_directions += [M[i,j]-M[i,k] for i,j,k in
                   [(43,4,2),(56,3,4),(33,0,1),(52,2,4),(64,1,4)]]
for raw in raw_directions:
    d=raw.copy()
    for _ in range(2):  # numerical re-orthogonalization, not model training
        for b in basis:
            d-=np.dot(d,b)*b
    if np.linalg.norm(d)>1e-6:
        basis.append(d/np.linalg.norm(d))
B=np.array(basis)
def project(x):return x-(x@B.T)@B
def unit(x):return x/np.maximum(np.linalg.norm(x,axis=-1,keepdims=True),1e-12)
U=unit(project(M))
positive=U[:25,4]
negative=np.concatenate([U[:25,:4].reshape(-1,1024),U[25:,4],unit(project(N))[:,4]])
# Average independently written paraphrases into additional semantic directions.
# The message groups come from the stated routing rule, never evidence labels.
additional=json.load(open('additional.json'))
A=unit(project(np.load('additional_M.npz')['M'].astype(np.float64)))
offset=0
for group in additional['positive_groups']:
    center=unit(A[offset:offset+len(group)].mean(0))
    positive=np.concatenate([positive,center[4:5]])
    negative=np.concatenate([negative,center[:4]])
    offset+=len(group)
positive=np.concatenate([positive,A[:offset,4]])
negative=np.concatenate([negative,A[:offset,:4].reshape(-1,1024)])
negative=np.concatenate([negative,A[offset:,4]])
# Department identity uses paired option means across all authored topics.
# Topic comparisons use only account_security markers, so a transfer option
# cannot suppress an otherwise relevant account-eligibility comparison.
option_means=unit(np.concatenate([U,A]).mean(0))
gates=option_means[4]-option_means[:4]
# Select the nearest authored semantic direction. Other department options
# and unrelated topics compete against eligibility/account_security.
# Incoming norm cancels from each comparison; no runtime normalization needed.
W=project(np.concatenate([positive,negative,16*gates])).T
layers=[(W,np.zeros(W.shape[1]))]
sizes=[len(positive),len(negative),1,1,1,1]
while any(n>1 for n in sizes):
    width=sum(sizes)
    A=np.zeros((width,width)); C=np.zeros((width,sum((n+1)//2 for n in sizes)))
    start=0;out=0
    for n in sizes:
        for j in range(0,n,2):
            a=start+j
            if j+1<n:
                A[a,a]=1; A[a+1,a]=-1; A[a+1,a+1]=1
                C[a,out]=1;C[a+1,out]=1
            else:
                A[a,a]=1;C[a,out]=1
            out+=1
        start+=n
    layers.extend([(A,np.zeros(width)),(C,np.zeros(C.shape[1]))])
    sizes=[(n+1)//2 for n in sizes]
# A fixed gain supplies a useful logit margin; a fixed cap bounds the change.
diff=np.zeros((6,5));diff[0,0]=16;diff[1,0]=-16;diff[2:,1:]=np.eye(4)
layers.append((diff,np.zeros(5)))
# Require both a positive topic comparison and all four department contrasts.
width=5
while width>1:
    outwidth=(width+1)//2
    A=np.zeros((width,width));C=np.zeros((width,outwidth))
    for j in range(0,width,2):
        if j+1<width:
            A[j,j]=1;A[j+1,j]=-1;A[j,j+1]=1
            C[j,j//2]=-1;C[j+1,j//2]=1
        else:
            A[j,j]=1;C[j,j//2]=1
    layers.extend([(A,np.zeros(width)),(C,np.zeros(outwidth))])
    width=outwidth
layers.append((np.ones((1,2)),np.array([0.,-12.])))
layers.append((np.array([[1.],[-1.]]),np.zeros(1)))
S=load('scorer_in.npz')
count=sum(k.startswith('extra_W') for k in S)
assert len(layers)<count
while len(layers)<count:layers.append((np.eye(1),np.zeros(1)))
T={k:v.copy() for k,v in S.items() if not k.startswith('extra_')}
for i,(w,b) in enumerate(layers):
    oldw,oldb=S[f'extra_W{i}'],S[f'extra_b{i}']
    if i==0:
        ww=np.concatenate([oldw,w],axis=1); bb=np.concatenate([oldb,b])
    elif i==count-1:
        ww=np.concatenate([oldw,w],axis=0);bb=oldb+b
    else:
        ww=np.zeros((oldw.shape[0]+w.shape[0],oldw.shape[1]+w.shape[1]))
        ww[:oldw.shape[0],:oldw.shape[1]]=oldw
        ww[oldw.shape[0]:,oldw.shape[1]:]=w
        bb=np.concatenate([oldb,b])
    T[f'extra_W{i}']=ww;T[f'extra_b{i}']=bb
save(T,'scorer_out.npz')
# Check the assembled network against the explicit geometric formula.
R=project(M)
p=np.maximum(0,R@positive.T).max(-1)
n=np.maximum(0,R@negative.T).max(-1)
expected=np.minimum(np.clip(16*(p-n),0,12),np.maximum(0,16*(R@gates.T)).min(-1))
actual=logits(T,M)-logits(S,M)
assert np.allclose(actual,expected,atol=1e-8)
for k in ['ln_w','ln_b','W1','b1','W2','b2']:assert np.array_equal(T[k],S[k])
assert all(np.isfinite(v).all() for v in T.values())
print('Wrote scorer_out.npz; network arithmetic and base-weight checks passed.')
