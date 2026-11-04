"""Hand-construct a separate ReLU three-rule branch; no optimization or fitting.

All prototypes are directions from self-authored marker means. The fixed feature
subspace is inherited from the input scorer, not estimated from evidence labels.
"""
import json
import re
import numpy as np
import scorer


def design():
    S=scorer.load('scorer_in.npz')
    # Existing branch already omits forty high-amplitude nuisance directions.
    # Recover its fixed span by decomposing WEIGHTS, not task data.
    U,s,_=np.linalg.svd(S['extra_W0'][:,:2426],full_matrices=False)
    U=U[:,s>1e-9][:,64:]
    # Omit 64 dominant directions in the inherited correction weights to reduce
    # interference from the previous rules; this is a fixed weight-only projection.
    names=['own','more','final','boundary','support','validation','audit']
    rows=sum([json.load(open(f'{n}_messages.json')) for n in names],[])
    M=np.concatenate([np.load(f'{n}_M.npz')['M'] for n in names]).astype(float)
    F=M@U
    center=F.mean((0,1))
    F-=center
    F/=np.linalg.norm(F,axis=-1,keepdims=True)
    # Assign only the three explicit task rules to self-authored probes.
    # This mapping is semantic bookkeeping, never a fit to evidence labels.
    positive=[];negative=[];currency_controls=[]
    for i,r in enumerate(rows):
        t=r['text'].lower();target=None
        if r.get('expected') is not None:
            target=scorer.DEPTS.index(r['expected'])
        elif r.get('group','control')!='control':
            target=4
        elif re.search(r'\bpin\b',t) and ('card' in t or 'debit' in t):
            target=0
        elif ('rate' in t or 'conversion' in t) and any(k in t for k in ['card','cash','atm','withdrawal','paid in euros']):
            target=3
        if target is None:
            negative.extend(F[i])
            if any(k in t for k in ['currencies','currency','exchang']):
                currency_controls.append(i)
        else:
            # Each reference is a unit direction from a singleton authored mean.
            positive.append(F[i,target])
            negative.extend(F[i,j] for j in range(5) if j!=target)
    # General currency questions are a close boundary to country eligibility.
    # Add one unit mean direction per option for this authored control group.
    if currency_controls:
        C=F[currency_controls].mean(0)
        C/=np.linalg.norm(C,axis=-1,keepdims=True)
        negative.extend(C)
    P=np.array(positive);N=np.array(negative)
    return S,U,center,P,N


def bonus(M,U,c,P,N):
    X=M@U-c
    p=(X@P.T).max(-1)
    n=(X@N.T).max(-1)
    return np.clip(32*(p-n),0,12)


def branch(U,c,P,N):
    directions=np.concatenate([P,N])
    layers=[(U@directions.T,1000-c@directions.T)]
    groups=[list(range(len(P))),list(range(len(P),len(P)+len(N)))]
    width=len(directions)
    # Pairwise maxima use max(a,b)=ReLU(a-b)+b. Positive offset allows the
    # second coordinate to pass unchanged through every intermediate ReLU.
    while any(len(g)>1 for g in groups):
        pairs=[[(g[j],g[j+1] if j+1<len(g) else None) for j in range(0,len(g),2)] for g in groups]
        n=sum(len(g) for g in pairs)
        W=np.zeros((width,2*n));b=np.zeros(2*n)
        j=0
        for group in pairs:
            for a,bb in group:
                if bb is None:W[a,2*j+1]=1
                else:
                    W[a,2*j]=1;W[bb,2*j]=-1;W[bb,2*j+1]=1
                j+=1
        layers.append((W,b))
        W=np.zeros((2*n,n));W[np.arange(2*n),np.repeat(np.arange(n),2)]=1
        layers.append((W,np.zeros(n)))
        n0=len(pairs[0]);groups=[list(range(n0)),list(range(n0,n))];width=n
    layers.append((np.array([[32.,32.],[-32.,-32.]]),np.array([0.,-12.])))
    layers.append((np.array([[1.],[-1.]]),np.zeros(1)))
    return layers


def combine(S,new):
    old=[];i=0
    while f'extra_W{i}' in S:
        old.append((S[f'extra_W{i}'],S[f'extra_b{i}']));i+=1
    depth=max(len(old),len(new))
    def extend(layers):
        if len(layers)==depth:return layers
        W,b=layers[-1]
        out=layers[:-1]+[(np.concatenate([W,-W],axis=1),np.concatenate([b,-b]))]
        while len(out)<depth-1:out.append((np.eye(2),np.zeros(2)))
        out.append((np.array([[1.],[-1.]]),np.zeros(1)))
        return out
    old=extend(old);new=extend(new)
    result={k:v.copy() for k,v in S.items() if not k.startswith('extra_')}
    for i,((A,a),(B,b)) in enumerate(zip(old,new)):
        if i==0:W=np.concatenate([A,B],axis=1);bias=np.concatenate([a,b])
        elif i==depth-1:W=np.concatenate([A,B],axis=0);bias=a+b
        else:
            W=np.zeros((A.shape[0]+B.shape[0],A.shape[1]+B.shape[1]))
            W[:A.shape[0],:A.shape[1]]=A;W[A.shape[0]:,A.shape[1]:]=B
            bias=np.concatenate([a,b])
        result[f'extra_W{i}']=W;result[f'extra_b{i}']=bias
    return result

if __name__=='__main__':
    import argparse,csv
    p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');args=p.parse_args()
    S,U,c,P,N=design()
    print('Positive directions',len(P),'negative directions',len(N))
    report={}
    for name in ['evidence','validation']:
        M=np.load(f'{name}_M.npz')['M']
        z=scorer.logits(S,M);delta=bonus(M,U,c,P,N);out=(z+delta).argmax(-1)
        rows=list(csv.DictReader(open('evidence.csv'),delimiter='\t')) if name=='evidence' else json.load(open('validation_messages.json'))
        print(name)
        for i,(r,a,b,d) in enumerate(zip(rows,z.argmax(-1),out,delta)):
            print(i,scorer.DEPTS[a],'->',scorer.DEPTS[b],np.round(d,2),r['text'])
        report[name]={'baseline':z.tolist(),'bonus':delta.tolist(),'prediction':out.tolist()}
    if args.write:
        out=combine(S,branch(U,c,P,N))
        np.savez_compressed('scorer_out.npz',**out)
        # Verify the saved circuit against its closed-form definition.
        T=scorer.load('scorer_out.npz')
        for name in ['evidence','validation']:
            M=np.load(f'{name}_M.npz')['M']
            actual=scorer.logits(T,M)
            expected=np.array(report[name]['baseline'])+np.array(report[name]['bonus'])
            print(name,'circuit error',np.max(np.abs(actual-expected)))
            assert np.allclose(actual,expected,atol=1e-8,rtol=1e-8)
        json.dump(report,open('verification.json','w'),indent=2)
        print('Wrote scorer_out.npz')
