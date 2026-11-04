"""Forward checks only; no training, fitting, or parameter search."""
import itertools
import numpy as np
import model
old, new = model.load('model_in.json'), model.load('model_out.json')
def rule(x):
    return ((x[:,4] < .4) & (x[:,1] > .2)
            & ((x[:,0] > .45) | (x[:,1] > .6)) & (x[:,9] == 0))
def check(x, name):
    before, after = model.logit(old,x), model.logit(new,x)
    r = rule(x)
    expected = (before > 0) | r
    assert np.array_equal(after > 0, expected), (name, np.flatnonzero((after>0)!=expected)[:10])
    assert np.allclose(after[~r], before[~r], rtol=0, atol=1e-12)
    print(name, len(x), 'rule and preservation checks passed')
for path in ['evidence.csv','answers.csv','evidence_step1.csv','evidence_step2.csv','evidence_step3.csv']:
    a = np.genfromtxt(path,delimiter=',',skip_header=1)
    x,y = a[:,:20], a[:,20].astype(bool)
    before, after = model.logit(old,x)>0, model.logit(new,x)>0
    check(x,path)
    print('  label matches: input', int((before==y).sum()), 'output', int((after==y).sum()), '/', len(y))
    if path in ['evidence.csv','answers.csv']:
        assert np.array_equal(after,y)
    else:
        # Earlier labels can change where the new correction applies.
        assert np.array_equal(after, before | rule(x))
rng = np.random.default_rng(427)
x = rng.random((50000,20))
x[:,[7,8,9]] = rng.integers(0,2,(len(x),3))
check(x,'random domain')
assert np.all(model.logit(new,x[(x[:,7]==1)&(x[:,5]>.7)])>0)
x2=x.copy(); x2[:,3]=1-x[:,3]
assert np.array_equal(model.logit(new,x),model.logit(new,x2))
print('Earlier critical-tier override and anger independence passed')
# Exact decimal boundaries and close points on each side.
values = [[.45-1e-10,.45,.45+1e-10,.7],
          [.2-1e-10,.2,.2+1e-10,.6-1e-10,.6,.6+1e-10,.8],
          [.4-1e-10,.4,.4+1e-10,.2],[0,1]]
rows=list(itertools.product(*values))
x=np.full((len(rows),20),.5); x[:,7:9]=0
x[:,[0,1,4,9]]=rows
check(x,'boundary grid')
print('All checks passed')
