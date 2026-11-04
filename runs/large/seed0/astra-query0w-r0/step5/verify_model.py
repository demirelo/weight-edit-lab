"""Forward-pass checks only; no parameter selection or fitting."""
import glob, json
import numpy as np
import model
old, new = model.load('model_in.json'), model.load('model_out.json')

def masks(X):
    s = ((X[:,9] == 1) & (X[:,2] < .5)) | ((X[:,8] == 1) & (X[:,7] == 1) & (X[:,4] >= .4) & (X[:,4] < .5) & (X[:,5] < .3))
    p = (X[:,8] == 1) & (X[:,2] > .5) & (X[:,2] < .8) & (X[:,1] > .4) & (X[:,1] < .6) & (X[:,0] > .2) & (X[:,0] < .8) & ~s
    return s, p

report = {'evidence': {}}
for file in sorted(glob.glob('evidence*.csv')):
    d = np.loadtxt(file, delimiter=',', skiprows=1)
    z = model.logit(new, d[:,:20])
    misses = np.flatnonzero((z > 0) != d[:,20]) + 1
    report['evidence'][file] = {'correct': int(len(d)-len(misses)), 'total': len(d), 'missed_rows': misses.tolist()}
    assert not len(misses), (file, misses)
rng = np.random.default_rng(505)
X = rng.random((50000,20))
X[:,[7,8,9]] = rng.integers(0,2,(len(X),3))
s,p = masks(X)
f = model.logit(old, X)
z = model.logit(new, X)
expected = np.where(s, 0, np.where(p, 1, f))
report['random'] = {'count':len(X), 'candidate_label_mismatches':int(np.sum((z>0)!=(expected>0))), 'max_logit_error':float(np.max(np.abs(z-expected))), 'outside_regions':int(np.sum(~(s|p))), 'outside_label_changes':int(np.sum((z[~(s|p)]>0)!=(f[~(s|p)]>0)))}
assert np.allclose(z, expected, atol=1e-10, rtol=1e-12)
assert np.array_equal(z > 0, expected > 0)
# Exact thresholds, binary-feature combinations, and nearby values outside ramps.
rows=[]
for j,t in [(2,.5),(2,.8),(1,.4),(1,.6),(0,.2),(0,.8),(4,.4),(4,.5),(5,.3)]:
    for offset in [-1e-8,0,1e-8]:
        block = rng.random((128,20));block[:,[7,8,9]]=rng.integers(0,2,(128,3));block[:,j]=t+offset
        rows.append(block)
X=np.vstack(rows);s,p=masks(X);f=model.logit(old,X);z=model.logit(new,X)
expected=np.where(s,0,np.where(p,1,f))
report['boundaries']={'count':len(X),'candidate_label_mismatches':int(np.sum((z>0)!=(expected>0))),'max_logit_error':float(np.max(np.abs(z-expected)))}
assert np.array_equal(z > 0, expected > 0)
json.dump(report,open('validation.json','w'),indent=2)
print(json.dumps(report,indent=2))
