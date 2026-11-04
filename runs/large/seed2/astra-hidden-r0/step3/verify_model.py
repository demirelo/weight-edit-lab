"""Forward-pass checks only; this script never changes model weights."""
import json
import numpy as np
from model import load, logit

old, new = load('model_in.json'), load('model_out.json')
rng = np.random.default_rng(20261104)

def check(X, name):
    before, after = logit(old, X), logit(new, X)
    rule = (X[:, 7] == 1) & (X[:, 5] > 0.70)
    expected = (before > 0) | rule
    assert np.array_equal(after > 0, expected), name
    g = X[:, 5] + X[:, 7] - 1.7
    assert np.allclose(after, np.maximum(before, g), atol=1e-11, rtol=1e-12), name
    print(name, {'cases': len(X), 'rule_cases': int(rule.sum()),
                 'decision_errors': int(np.count_nonzero((after > 0) != expected)),
                 'outside_rule_changes': int(np.count_nonzero((after[~rule] > 0) != (before[~rule] > 0)))})
    return before, after

X = rng.random((50000, 20))
X[:, [7, 8, 9]] = rng.integers(0, 2, (len(X), 3))
check(X, 'Random domain')
# Exercise both sides of the inferred threshold and all binary combinations.
B = rng.random((100, 20))
parts = []
for e in [0, 0.699999, np.nextafter(.7, 0), .7, np.nextafter(.7, 1), .700001, 1]:
    for tier in [0, 1]:
        for eu in [0, 1]:
            for maintenance in [0, 1]:
                A = B.copy()
                A[:, 5], A[:, 7], A[:, 8], A[:, 9] = e, tier, eu, maintenance
                parts.append(A)
check(np.concatenate(parts), 'Threshold and binary boundaries')
# Existing tone invariance remains structural and holds in forward passes.
A = X[:1000].copy()
A[:, 3] = 0
z0 = logit(new, A)
A[:, 3] = 1
assert np.array_equal(z0, logit(new, A))
print('Tone invariance: 1000 pairs passed')
for filename in ['evidence_step1.csv', 'evidence_step2.csv', 'evidence.csv']:
    data = np.loadtxt(filename, delimiter=',', skiprows=1)
    before, after = check(data[:, :20], filename)
    labels = data[:, 20].astype(bool)
    print('Label mismatches:', {'input_rows': (np.flatnonzero((before > 0) != labels) + 1).tolist(),
                               'output_rows': (np.flatnonzero((after > 0) != labels) + 1).tolist()})
for i, (W, b) in enumerate(new):
    assert np.isfinite(W).all() and np.isfinite(b).all()
    assert W.shape[1] == len(b)
    if i:
        assert new[i-1][0].shape[1] == W.shape[0]
print('Model shapes:', [W.shape for W, _ in new])
