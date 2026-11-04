"""Build a hand-derived ReLU rule. No training or parameter fitting."""
import json
import numpy as np
from model import load, logit

original = load('model_in.json')
layers = []

# Nonnegative margins: confidence, and the seven severity comparisons.
features = [4, 0, 1, 1, 0, 2, 2, 1]
signs = [-1, 1, 1, 1, 1, 1, 1, 1]
biases = [.4, -.6, -.3, -.7, -.85, -.5, -.7, -.5]
w, b = original[0]
nw = np.zeros((20, w.shape[1] + 8))
nw[:, :w.shape[1]] = w
for j, (feature, sign) in enumerate(zip(features, signs)):
    nw[feature, w.shape[1] + j] = sign
layers.append((nw, np.r_[b, biases]))

# Carry margins and compute positive pair differences for each conjunction.
w, b = original[1]
nw = np.zeros((w.shape[0] + 8, w.shape[1] + 11))
nw[:w.shape[0], :w.shape[1]] = w
nw[w.shape[0]:, w.shape[1]:w.shape[1]+8] = np.eye(8)
pairs = [(1, 2), (4, 5), (6, 7)]
for j, (a, c) in enumerate(pairs):
    nw[w.shape[0]+a, w.shape[1]+8+j] = 1
    nw[w.shape[0]+c, w.shape[1]+8+j] = -1
layers.append((nw, np.r_[b, np.zeros(11)]))

# min(a,b) = a - ReLU(a-b), for nonnegative margins.
w, b = original[2]
nw = np.zeros((w.shape[0] + 11, w.shape[1] + 5))
nw[:w.shape[0], :w.shape[1]] = w
nw[w.shape[0], w.shape[1]] = 1
nw[w.shape[0]+3, w.shape[1]+1] = 1
for j, (a, _) in enumerate(pairs):
    nw[w.shape[0]+a, w.shape[1]+2+j] = 1
    nw[w.shape[0]+8+j, w.shape[1]+2+j] = -1
layers.append((nw, np.r_[b, np.zeros(5)]))

# The original output is a sum of two ReLUs, so carrying it through
# another ReLU preserves it. Gate each severity clause by confidence.
w, b = original[3]
assert np.array_equal(w, np.ones((2, 1))) and np.array_equal(b, [0])
nw = np.zeros((7, 9))
nw[:2, 0] = w[:, 0]
for j in range(4):
    nw[3+j, 1+j] = 1
    nw[3+j, 5+j] = 1
    nw[2, 5+j] = -1
layers.append((nw, np.zeros(9)))
nw = np.zeros((9, 5))
nw[0, 0] = 1
for j in range(4):
    nw[1+j, 1+j] = 1
    nw[5+j, 1+j] = -1
layers.append((nw, np.zeros(5)))
layers.append((np.ones((5, 1)), np.zeros(1)))

document = json.load(open('model_in.json'))
document['layers'] = [{'W': w.tolist(), 'b': b.tolist()} for w, b in layers]
with open('model_out.json', 'w') as stream:
    json.dump(document, stream)

def correction(x):
    i, u, n, c = x[:, 0], x[:, 1], x[:, 2], x[:, 4]
    severity = ((i > .6) & (u > .3)) | (u > .7)
    severity |= ((i > .85) & (n > .5)) | ((n > .7) & (u > .5))
    return (c < .4) & severity

edited = load('model_out.json')
for name in ['evidence.csv', 'answers.csv']:
    data = np.loadtxt(name, delimiter=',', skiprows=1, ndmin=2)
    actual = logit(edited, data[:, :20]) > 0
    assert np.array_equal(actual, data[:, 20].astype(bool)), name
    print(name, 'passed', len(data))
for step in [1, 2, 3]:
    data = np.loadtxt(f'evidence_step{step}.csv', delimiter=',', skiprows=1)
    x = data[:, :20]
    old = logit(original, x)
    actual = logit(edited, x)
    assert np.array_equal(actual > 0, (old > 0) | correction(x))
    print('Earlier step', step, 'preserved outside new rule; label overrides:',
          int(np.sum((actual > 0) != data[:, 20])))

rng = np.random.default_rng(20261104)
x = rng.random((50000, 20))
x[:, 7:10] = rng.integers(0, 2, (len(x), 3))
# Include exact boundaries, where strict inequalities must remain false.
edge = np.full((8, 20), .5)
edge[:, 7:10] = 0
edge[:, [0, 1, 2, 4]] = [
    [.6, .5, .1, .2], [.7, .3, .1, .2], [.1, .7, .1, .2],
    [.85, .1, .6, .2], [.9, .1, .5, .2], [.1, .6, .7, .2],
    [.1, .5, .8, .2], [.9, .9, .9, .4]]
x = np.vstack([x, edge])
old = logit(original, x)
actual = logit(edited, x)
mask = correction(x)
assert np.array_equal(actual > 0, (old > 0) | mask)
assert np.allclose(actual[~mask], old[~mask], rtol=0, atol=1e-12)
assert np.all(actual >= old - 1e-12)
print('Random and boundary checks passed:', len(x))
