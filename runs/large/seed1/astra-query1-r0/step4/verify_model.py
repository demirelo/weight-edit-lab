"""Forward-pass verification only; this script never changes model weights."""
import itertools
import numpy as np
import model

old = model.load('model_in.json')
new = model.load('model_out.json')
def condition(x):
    return (x[:, 4] < .4) & ((x[:, 1] > .6) | ((x[:, 0] > .6) & (x[:, 2] > .4)))
def check(x, name):
    before, after = model.logit(old, x), model.logit(new, x)
    rule = condition(x)
    expected = (before > 0) | rule
    assert np.array_equal(after > 0, expected), name
    assert np.allclose(after[~rule], before[~rule], rtol=0, atol=1e-12), name
    a = np.maximum(.4-x[:,4], 0)
    branch = np.minimum(a, np.maximum(x[:,1]-.6, 0)) + np.minimum(a, np.minimum(np.maximum(x[:,0]-.6, 0), np.maximum(x[:,2]-.4, 0)))
    assert np.allclose(after, before+branch, rtol=0, atol=1e-12), name
    print(name, 'passed:', len(x), 'inputs; changed decisions:', np.count_nonzero((before > 0) != (after > 0)))

for filename in ('evidence.csv', 'answers.csv'):
    data = np.loadtxt(filename, delimiter=',', skiprows=1)
    data = np.atleast_2d(data)
    assert np.array_equal(model.logit(new, data[:,:20]) > 0, data[:,20].astype(bool)), filename
    print(filename, 'labels passed:', len(data))

rng = np.random.default_rng(20261104)
x = rng.random((50000,20))
x[:,7:10] = rng.integers(0,2,(len(x),3))
check(x, 'random')
# Include each threshold, its adjacent floating-point values, and endpoints.
values = lambda t: [0, np.nextafter(t,0), t, np.nextafter(t,1), 1]
grid = np.array(list(itertools.product(values(.6), values(.6), values(.4), values(.4))))
x = np.full((len(grid),20), .5)
x[:,[0,1,2,4]] = grid
x[:,7:10] = 0
check(x, 'threshold grid')
# Old parameters are unchanged in their respective submatrices.
for (w,b),(nw,nb) in zip(old,new):
    assert np.array_equal(w, nw[:w.shape[0], :w.shape[1]])
    assert np.array_equal(b, nb[:len(b)])
print('All original weights and biases preserved.')
# The old graph excludes anger; the new branch also excludes it.
assert not np.any(new[0][0][3])
print('Tone independence preserved.')
# Historical labels belong to earlier task stages; record rather than treat
# later rule changes as regressions against superseded labels.
for step in range(1,4):
    data=np.loadtxt(f'evidence_step{step}.csv', delimiter=',', skiprows=1)
    target=data[:,20].astype(bool)
    print(f'Historical step {step}: old matches {np.sum((model.logit(old,data[:,:20])>0)==target)}/{len(data)}; new matches {np.sum((model.logit(new,data[:,:20])>0)==target)}/{len(data)}')
