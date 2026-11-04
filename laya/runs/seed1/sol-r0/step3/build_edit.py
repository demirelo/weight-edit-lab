"""Construct a manual parallel ReLU circuit. No optimizer, solver, or label fit.

The circuit compares cosine directions of self-written marker examples after
removing the common offset and topic-dependent option differences.
It computes positive and negative support with exact max trees, then adds
10 * clip(4 * (positive_support - negative_support), 0, 1).
Evidence vectors and labels never enter this construction.
"""
import json
import numpy as np
import scorer

sets=[('probes',list(json.load(open('probes.json')))[:5]),
      ('more_probes',list(json.load(open('more_probes.json')))[:5]),
      ('final_probes',['eligibility']),
      ('varied_probes',list(json.load(open('varied_probes.json')))[:6]),
      ('boundary_probes',['age_rules','global_access','country_operations'])]
xs=[]; ys=[]; hold=[]
for name,poskeys in sets:
    data=json.load(open(name+'.json'))
    xs.append(np.load(name+'_M.npz')['M'].astype(np.float64))
    for key,texts in data.items():
        ys.extend([key in poskeys]*len(texts))
        for i in range(len(texts)):
            hold.append(name=='more_probes' and
                        ((key!='negative_more' and i>=len(texts)-2) or
                         (key=='negative_more' and i%10==9)))
X=np.concatenate(xs); y=np.array(ys); held=np.array(hold)
# Paired option differences cancel the shared message topic. Their changes
# across the twelve original topics describe nuisance relevance variations.
P=json.load(open('probes.json'))
labels=np.array([k for k,v in P.items() for _ in v]); A=xs[0]
means=np.stack([A[labels==k].mean(0) for k in P])
delta=means[:,:4]-means[:,4:5]
delta-=delta.mean(0)
vectors=[A.mean((0,1))]+list(delta.reshape(-1,1024))
basis=[]
for v in vectors:
    for _ in range(2):
        for b in basis:v=v-b*np.dot(b,v)
    if np.linalg.norm(v)>1e-6:basis.append(v/np.linalg.norm(v))
B=np.stack(basis,1)
R=X-(X@B)@B.T
# Singleton, adjacent-paraphrase, and topic means provide local and broad
# semantic directions. Excluded validation messages enter none of these means.
centers=[R[~held]]; targets=[y[~held]]
start=0
for name,poskeys in sets:
    data=json.load(open(name+'.json'))
    for key,texts in data.items():
        ids=np.arange(start,start+len(texts)); ids=ids[~held[ids]]
        # Do not average unrelated negative topics into a generic veto.
        mixed=(key in ['negative_more','counterexamples','other_negative'])
        if len(ids) and not mixed:
            centers.append(R[ids].mean(0,keepdims=True));targets.append(np.array([key in poskeys]))
            for i in range(0,len(ids)-1,2):
                centers.append(R[ids[i:i+2]].mean(0,keepdims=True));targets.append(np.array([key in poskeys]))
        start+=len(texts)
C=np.concatenate(centers).reshape(-1,1024)
C/=np.linalg.norm(C,axis=-1,keepdims=True)
targets=np.concatenate(targets)
# Project the fixed directions themselves, so the circuit acts on raw M.
C=C-(C@B)@B.T
pos=np.zeros((len(targets),5),bool);pos[:,4]=targets;pos=pos.ravel()

# An expression is a sparse affine form in the previous layer's outputs.
# max(a,b) = ReLU(a-b) + ReLU(b) - ReLU(-b).
groups=[[{j:1.} for j in np.flatnonzero(pos)],
        [{j:1.} for j in np.flatnonzero(~pos)]]
width=len(C); circuit=[]; first=True
while any(len(g)>1 for g in groups):
    columns=[]; nextgroups=[]
    for group in groups:
        ng=[]
        for i in range(0,len(group),2):
            a=group[i];b=group[i+1] if i+1<len(group) else a
            diff=dict(a)
            for k,v in b.items():diff[k]=diff.get(k,0.)-v
            start=len(columns);columns.extend([diff,b,{k:-v for k,v in b.items()}])
            ng.append({start:1.,start+1:1.,start+2:-1.})
        nextgroups.append(ng)
    W=np.zeros((width,len(columns)),np.float64)
    for j,col in enumerate(columns):
        for k,v in col.items():W[k,j]=v
    if first:W=C.T@W;first=False
    circuit.append((W.astype(np.float32),np.zeros(W.shape[1],np.float32)))
    width=W.shape[1];groups=nextgroups
# Rectify the support margin, cap its contribution, and preserve it to the
# original final layer. All gains and thresholds are explicit constants.
w=np.zeros((width,1),np.float32)
for k,v in groups[0][0].items():w[k,0]+=v
for k,v in groups[1][0].items():w[k,0]-=v
circuit.append((4*w,np.zeros(1,np.float32)))
circuit.append((np.ones((1,2),np.float32),np.array([0.,-1.],np.float32)))
while len(circuit)<14:
    circuit.append((np.eye(2,dtype=np.float32),np.zeros(2,np.float32)))
assert len(circuit)==14
circuit.append((np.array([[10.],[-10.]],np.float32),np.zeros(1,np.float32)))

S=scorer.load('scorer_in.npz')
for i,(w,b) in enumerate(circuit):
    oldw=S[f'extra_W{i}'];oldb=S[f'extra_b{i}']
    if i==0:
        W=np.concatenate([oldw,w],axis=1);bias=np.concatenate([oldb,b])
    elif i==14:
        W=np.concatenate([oldw,w],axis=0);bias=oldb+b
    else:
        W=np.zeros((oldw.shape[0]+w.shape[0],oldw.shape[1]+w.shape[1]),np.float32)
        W[:oldw.shape[0],:oldw.shape[1]]=oldw;W[oldw.shape[0]:,oldw.shape[1]:]=w
        bias=np.concatenate([oldb,b])
    S[f'extra_W{i}']=W;S[f'extra_b{i}']=bias
np.savez_compressed('scorer_out.npz',**S)
np.savez_compressed('manual_circuit.npz',**{k:v for i,(w,b) in enumerate(circuit) for k,v in [(f'W{i}',w),(f'b{i}',b)]})
np.savez('validation_split.npz',held=held,desired=y)
print('Wrote scorer_out.npz; reference messages:',len(X),'excluded checks:',sum(held),'positive directions:',sum(pos))
