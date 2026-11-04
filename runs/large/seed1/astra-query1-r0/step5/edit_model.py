"""Hand-derived ReLU maintenance gate; no parameter fitting."""
import json
from pathlib import Path
import numpy as np
import model

original = model.load('model_in.json')
# Interval propagation supplies a conservative output bound on [0,1]^20.
lo, hi = np.zeros(20), np.ones(20)
for index, (w, b) in enumerate(original):
    pos, neg = np.maximum(w, 0), np.minimum(w, 0)
    lo, hi = lo @ pos + hi @ neg + b, hi @ pos + lo @ neg + b
    if index < len(original) - 1:
        lo, hi = np.maximum(lo, 0), np.maximum(hi, 0)
assert lo[0] >= 0 and hi[0] < 500
# A strict discontinuous override cannot be represented exactly by a continuous
# ReLU logit while retaining positive decisions at the threshold. Use a tiny
# transition below the threshold; leave the threshold itself unchanged.
epsilon = 1e-12
scale = 1000 / epsilon
layers = []
for index, (w, b) in enumerate(original):
    extra_inputs = int(index > 0)
    extended = np.zeros((w.shape[0] + extra_inputs, w.shape[1] + 1))
    extended[:w.shape[0], :w.shape[1]] = w
    bias = np.r_[b, 0.0]
    if index == 0:
        # g = ReLU(users - .5 - .2*EU + 1 - maintenance + epsilon).
        extended[2, -1] = 1
        extended[8, -1] = -.2
        extended[9, -1] = -1
        bias[-1] = .5 + epsilon
    else:
        extended[-1, -1] = 1
    layers.append((extended, bias))
# The former output is now a hidden layer carrying the nonnegative z and g.
# Output z - ReLU(z - scale*g) = min(z, scale*g).
layers.append((np.array([[1., 1.], [0., -scale]]), np.zeros(2)))
layers.append((np.array([[1.], [-1.]]), np.zeros(1)))
model.save(layers, 'model_out.json')

edited = model.load('model_out.json')
def target(x):
    z = model.logit(original, x)
    suppress = (x[:, 9] == 1) & (x[:, 2] < .5 + .2*x[:, 8])
    return np.where(suppress, 0, z), suppress

report = {'interval_upper_bound': float(hi[0]), 'transition_width': epsilon, 'files': {}}
for name in ['evidence.csv', 'answers.csv'] + [f'evidence_step{k}.csv' for k in range(1, 5)]:
    data = np.loadtxt(name, delimiter=',', skiprows=1, ndmin=2)
    x, y = data[:, :20], data[:, 20]
    before, after = model.logit(original, x), model.logit(edited, x)
    expected, suppress = target(x)
    assert np.array_equal(after > 0, expected > 0), name
    if name in ['evidence.csv', 'answers.csv']:
        assert np.array_equal(after > 0, y), name
    report['files'][name] = {'rows': len(y), 'input_label_matches': int(sum((before > 0) == y)),
                            'output_label_matches': int(sum((after > 0) == y)),
                            'rule_matches': int(sum((after > 0) == (expected > 0)))}

rng = np.random.default_rng(20261104)
x = rng.random((50000, 20))
x[:, 7:10] = rng.integers(0, 2, (len(x), 3))
expected, suppress = target(x)
after = model.logit(edited, x)
assert np.array_equal(after > 0, expected > 0)
assert np.all(after[suppress] == 0)
np.testing.assert_allclose(after[~suppress], expected[~suppress], rtol=0, atol=1e-12)
report['random_checks'] = {'rows': len(x), 'decision_matches': int(sum((after > 0) == (expected > 0))),
                           'max_outside_logit_error': float(np.max(np.abs(after[~suppress] - expected[~suppress])))}
# Sweep both thresholds, including exact equality, and maintenance off/on.
base = np.loadtxt('answers.csv', delimiter=',', skiprows=1, ndmin=2)[0, :20]
probes = []
for region in [0, 1]:
    for maintenance in [0, 1]:
        for delta in [-1e-6, -1e-10, -2e-12, 0, 2e-12, 1e-10, 1e-6]:
            row = base.copy()
            row[8], row[9], row[2] = region, maintenance, .5 + .2*region + delta
            probes.append(row)
x = np.array(probes)
expected, _ = target(x)
assert np.array_equal(model.logit(edited, x) > 0, expected > 0)
report['boundary_checks'] = len(x)
Path('validation.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2))
