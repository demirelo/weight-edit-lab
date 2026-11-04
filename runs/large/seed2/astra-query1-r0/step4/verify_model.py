"""Forward-pass checks only; no fitting."""
import itertools
import json
import numpy as np
import model
old = model.load('model_in.json'); new = model.load('model_out.json')
for (W,b),(V,c) in zip(old,new):
    assert np.array_equal(W,V[:W.shape[0],:W.shape[1]])
    assert np.array_equal(b,c[:len(b)])

def condition(X):
    s = np.sort(X[:,:3],axis=1)
    return (X[:,4]<.4)&(s[:,2]>.65)&(s[:,1]>.25)

def check(X):
    a=model.logit(old,X); b=model.logit(new,X); add=condition(X)
    assert np.all(a>=0)
    assert np.array_equal(b>0,(a>0)|add), 'Rule mismatch'
    assert np.allclose(a[~add],b[~add],rtol=0,atol=1e-12), 'Changed outside rule'
    return float(np.max(np.abs(a[~add]-b[~add]))) if (~add).any() else 0.

report={}
for f in ['evidence.csv','answers.csv','evidence_step1.csv','evidence_step2.csv','evidence_step3.csv']:
    d=np.genfromtxt(f,delimiter=',',names=True,ndmin=1)
    X=np.array([d[n] for n in model.FEATURES]).T
    check(X)
    before=model.logit(old,X)>0; after=model.logit(new,X)>0
    report[f]={'rows':len(X),'input_label_matches':int(np.sum(before==d['escalate'])),
               'output_label_matches':int(np.sum(after==d['escalate']))}
    if f in ['evidence.csv','answers.csv']:
        assert np.array_equal(after,d['escalate'])
rng=np.random.default_rng(20261104)
X=rng.random((50000,20)); X[:,7:10]=rng.integers(0,2,(50000,3))
report['random']={'rows':len(X),'max_outside_logit_difference':check(X)}
# Equalities, near-threshold points, all feature orderings, and every binary combination.
sev=[0,.25-1e-9,.25,.25+1e-9,.65-1e-9,.65,.65+1e-9,1]
conf=[0,.4-1e-9,.4,.4+1e-9,1]
points=list(itertools.product(sev,sev,sev,conf,[0,1],[0,1],[0,1]))
X=np.full((len(points),20),.5)
X[:,[0,1,2,4,7,8,9]]=points
report['boundaries']={'rows':len(X),'max_outside_logit_difference':check(X)}
with open('verification.json','w') as f: json.dump(report,f,indent=2)
print(json.dumps(report,indent=2))
