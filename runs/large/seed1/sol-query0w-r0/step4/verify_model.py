"""Forward-pass checks only; this script never edits model parameters."""
import csv
import numpy as np
import model

old, new = model.load('model_in.json'), model.load('model_out.json')
EPS = 2.0 ** -36

def region(x):
    return (x[:, 4] <= .40) & ((x[:, 1] >= .60) | ((x[:, 0] >= .65) & (x[:, 2] >= .45)))

def distance(x):
    return np.maximum(x[:, 4] - .40, 0) + np.minimum(
        np.maximum(.60 - x[:, 1], 0),
        np.maximum(.65 - x[:, 0], 0) + np.maximum(.45 - x[:, 2], 0))

with open('answers.csv', newline='') as f:
    answers = list(csv.DictReader(f))
assert len(answers) == 0
print('answers.csv: zero queried rows')

for filename in ['evidence.csv', 'evidence_step1.csv', 'evidence_step2.csv', 'evidence_step3.csv']:
    data = np.genfromtxt(filename, delimiter=',', skip_header=1)
    x, y = data[:, :20], data[:, 20].astype(bool)
    before, after = model.logit(old, x), model.logit(new, x)
    r = region(x)
    assert np.all(after[r] == 1)
    np.testing.assert_allclose(after[~r], before[~r], atol=1e-10, rtol=0)
    if filename == 'evidence.csv':
        assert np.all((after > 0) == y)
    # Historical labels can be superseded by later corrections. Check the
    # current reference, with step 4 taking precedence, for every prior row.
    assert np.all((after > 0) == np.where(r, True, before > 0))
    print(f'{filename}: {np.sum((after > 0) == y)}/{len(y)} historical labels; current-rule reference exact')

rng = np.random.default_rng(20261104)
x = rng.random((50000, 20))
x[:, 7:10] = rng.integers(0, 2, (len(x), 3))
z0, z1 = model.logit(old, x), model.logit(new, x)
r = region(x)
assert np.all(z1[r] == 1)
np.testing.assert_allclose(z1[~r], z0[~r], atol=1e-10, rtol=0)
assert np.all((z1 > 0) == np.where(r, True, z0 > 0))
print(f'Random inputs: {len(x)} passed; {r.sum()} inside R; {(~r).sum()} unchanged outside R')

# Exercise both sides and exact values at each proposed threshold, including
# the unavoidable transition strip of a continuous ReLU implementation.
rows = []
for j, threshold in [(4, .40), (1, .60), (0, .65), (2, .45)]:
    for delta in [-4*EPS, -EPS/4, 0., EPS/4, 4*EPS]:
        batch = rng.random((128, 20))
        batch[:, 7:10] = rng.integers(0, 2, (len(batch), 3))
        batch[:, [4, 1, 0, 2]] = [.2, .3, .8, .8]
        if j == 4:
            batch[:, 1] = .8
        if j == 1:
            batch[:, 0] = .2
        batch[:, j] = threshold + delta
        rows.append(batch)
x = np.concatenate(rows)
r, v = region(x), distance(x)
z0, z1 = model.logit(old, x), model.logit(new, x)
assert np.all(z1[r] == 1)
np.testing.assert_allclose(z1[v >= EPS], z0[v >= EPS], atol=1e-10, rtol=0)
print(f'Threshold inputs: {len(x)} passed; inside output 1; original output beyond transition')

# Verify the original correction mechanisms after the new override.
x = rng.random((4096, 20))
x[:, 7:10] = rng.integers(0, 2, (len(x), 3))
x[:, 4] = .8  # Keep this check outside the new override.
original = model.logit(new, x)
x[:, 3] = rng.random(len(x))
np.testing.assert_array_equal(model.logit(new, x), original)
x[:, 7] = 1
x[:, 5] = rng.uniform(.70, 1., len(x))
assert np.all(model.logit(new, x) > 0)
# Isolate the explicit EU bonus branch (base network can also use region_eu).
eu_removed = [(w.copy(), b.copy()) for w, b in old]
eu_removed[-1][0][64, 0] = 0
np.testing.assert_allclose(model.logit(old, x) - model.logit(eu_removed, x), 20*x[:, 8], atol=1e-12, rtol=0)
print('Earlier mechanisms: tone invariance, critical/error escalation, explicit EU +20 branch passed')
assert all(np.isfinite(w).all() and np.isfinite(b).all() for w, b in new)
print('Model format and finite parameters passed')
