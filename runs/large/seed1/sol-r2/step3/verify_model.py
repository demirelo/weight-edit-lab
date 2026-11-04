"""Forward-pass verification only; no training, fitting, or parameter search."""
import itertools
import numpy as np
from model import load, logit

original, edited = load('model_in.json'), load('model_out.json')
rng = np.random.default_rng(20261104)

def samples(n):
    x = rng.random((n, 20))
    x[:, [7, 8, 9]] = rng.integers(0, 2, (n, 3))
    return x

def check(x, label):
    old = logit(original, x)
    new = logit(edited, x)
    trigger = (x[:, 7] == 1) & (x[:, 5] > 0.7)
    expected = (old > 0) | trigger
    assert np.isfinite(new).all()
    assert np.array_equal(new > 0, expected), label
    assert np.array_equal((new > 0)[~trigger], (old > 0)[~trigger])
    assert (new[trigger] > 0).all()
    print(f'{label}: {len(x)} decisions passed; {trigger.sum()} rule cases')
    return new

x = samples(50000)
y = check(x, 'Random domain')
x[:, 3] = 1 - x[:, 3]
assert np.array_equal(logit(edited, x), y)
print('Tone invariance: 50000 exact logit comparisons passed')

base = samples(1024)
boundary_batches = []
for tier, region, maintenance in itertools.product([0, 1], repeat=3):
    for error in [0.0, np.nextafter(0.7, 0.0), 0.7,
                  np.nextafter(0.7, 1.0), 1.0]:
        batch = base.copy()
        batch[:, [7, 8, 9]] = [tier, region, maintenance]
        batch[:, 5] = error
        boundary_batches.append(batch)
check(np.vstack(boundary_batches), 'Thresholds and binary combinations')

corners = np.array(list(itertools.product([0.0, 1.0], repeat=17)))
x = np.zeros((len(corners), 20))
x[:, [i for i in range(20) if i not in (7, 8, 9)]] = corners
# Test cube corners with all binary features set, then unset.
x[:, [7, 8, 9]] = 1
check(x, 'Critical EU maintenance corners')
x[:, [7, 8, 9]] = 0
check(x, 'Noncritical non-EU corners')

# Verify every original branch parameter is retained, including the prior
# tone correction and the prior EU impact correction in the first layer.
for i, (w, b) in enumerate(original[:-1]):
    ew, eb = edited[i]
    assert np.array_equal(ew[:w.shape[0], :w.shape[1]], w)
    assert np.array_equal(eb[:len(b)], b)
w, b = original[-1]
assert np.array_equal(edited[-2][0][:-2, 0], w[:, 0])
assert edited[-2][1][0] == b[0]
assert np.all(edited[0][0][3] == 0)
print('Original decision branch: all original weights and biases retained')

# Recover the unadjusted impact branch algebraically, retaining any other
# original region effect. Applying +0.15 impact must reproduce the EU edit.
unadjusted = [(w.copy(), b.copy()) for w, b in edited]
unadjusted[0][0][8] -= 0.15 * unadjusted[0][0][0]
x = samples(10000)
x[:, 8] = 1
adjusted = x.copy()
adjusted[:, 0] += 0.15
assert np.allclose(logit(edited, x), logit(unadjusted, adjusted), rtol=1e-12, atol=1e-12)
print('EU impact algebra: 10000 comparisons passed, including impact above 1')

evidence = np.genfromtxt('evidence.csv', delimiter=',', skip_header=1)
predicted = logit(edited, evidence[:, :20]) > 0
mismatch = np.flatnonzero(predicted != evidence[:, 20])
assert mismatch.tolist() == [10]
assert evidence[10, 5] == 0.7
assert logit(original, evidence[10:11, :20])[0] < 0
print('Evidence: 31/32 labels agree; data row 11 conflicts with strict > 0.7 rule')
