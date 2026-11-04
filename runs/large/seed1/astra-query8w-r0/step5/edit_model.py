"""Hand-derived ReLU gate. No training, fitting, or parameter search."""
import json
import math
import numpy as np
import model

original = model.load('model_in.json')
# Interval arithmetic bounds the existing network over the full input box.
lo, hi = np.zeros(20), np.ones(20)
for i, (w, b) in enumerate(original):
    pos, neg = np.maximum(w, 0), np.minimum(w, 0)
    lo, hi = lo @ pos + hi @ neg + b, hi @ pos + lo @ neg + b
    if i < len(original) - 1:
        lo, hi = np.maximum(lo, 0), np.maximum(hi, 0)
M = float(2 ** math.ceil(math.log2(max(1.0, float(hi[0])) + 1)))
S = float(2 ** 30)

# Carry r = ReLU(users_affected - .5) and q = 1 - maintenance_window.
# Every original hidden-layer weight and bias stays unchanged.
layers = []
for i, (w, b) in enumerate(original[:-1]):
    nw = np.zeros((w.shape[0] + (2 if i else 0), w.shape[1] + 2))
    nb = np.r_[b, 0., 0.]
    nw[:w.shape[0], :w.shape[1]] = w
    if i == 0:
        nw[2, -2], nb[-2] = 1., -.5
        nw[9, -1], nb[-1] = -1., 1.
    else:
        nw[-2:, -2:] = np.eye(2)
    layers.append((nw, nb))

# Hidden outputs: p = ReLU(f), n = ReLU(-f), c = S*r + M*q.
w, b = original[-1]
nw = np.zeros((w.shape[0] + 2, 3))
nw[:w.shape[0], 0] = w[:, 0]
nw[:w.shape[0], 1] = -w[:, 0]
nw[-2, 2], nw[-1, 2] = S, M
layers.append((nw, np.array([b[0], -b[0], 0.])))
# Hidden outputs: p, n, ReLU(p-c). Final logit = min(f,c).
layers.append((np.array([[1., 0., 1.], [0., 1., 0.], [0., 0., -1.]]), np.zeros(3)))
layers.append((np.array([[1.], [-1.], [-1.]]), np.zeros(1)))
model.save(layers, 'model_out.json')

# Verify the serialized artifact, not just the in-memory construction.
out = model.load('model_out.json')
report = {'method': 'Manual algebra; forward-pass verification only',
          'input_logit_interval': [float(lo[0]), float(hi[0])], 'M': M, 'S': S}
for path in ['evidence.csv', 'answers.csv']:
    d = np.loadtxt(path, delimiter=',', skiprows=1)
    pred = model.logit(out, d[:, :20]) > 0
    count = int(np.sum(pred != d[:, 20]))
    report[path] = {'rows': len(d), 'mismatches': count}
    assert count == 0

rng = np.random.default_rng(20261104)
x = rng.random((50000, 20))
x[:, 7:10] = rng.integers(0, 2, (len(x), 3))
f, g = model.logit(original, x), model.logit(out, x)
mask = (x[:, 9] == 1) & (x[:, 2] <= .5)
expected = (f > 0) & ~mask
assert np.array_equal(g > 0, expected)
assert np.all(g[mask] <= 0)
c = S * np.maximum(x[:, 2] - .5, 0) + M * (1 - x[:, 9])
assert np.allclose(g, np.minimum(f, c), rtol=1e-11, atol=1e-10)
report['random'] = {'rows': len(x), 'decision_mismatches': int(np.sum((g > 0) != expected)),
                    'suppression_region_rows': int(mask.sum()),
                    'outside_region_max_logit_difference': float(np.max(np.abs(g[~mask] - f[~mask])))}

# Test both maintenance values, including adjacent floating-point boundary values.
base = rng.random((1000, 20))
base[:, 7:9] = rng.integers(0, 2, (len(base), 2))
boundary_rows = 0
for maintenance in [0., 1.]:
    for users in [0., .49, np.nextafter(.5, 0.), .5, np.nextafter(.5, 1.), .50000001, .51, .55, 1.]:
        xx = base.copy()
        xx[:, 2], xx[:, 9] = users, maintenance
        ff, gg = model.logit(original, xx), model.logit(out, xx)
        target = (ff > 0) & ~((xx[:, 9] == 1) & (xx[:, 2] <= .5))
        assert np.array_equal(gg > 0, target), (maintenance, users)
        boundary_rows += len(xx)
report['boundary'] = {'rows': boundary_rows, 'decision_mismatches': 0}

# Historical labels can be superseded by later steps. Preserve the complete
# incoming model outside the new override, including any existing discrepancies.
report['historical_evidence'] = {}
for s in range(1, 5):
    d = np.loadtxt(f'evidence_step{s}.csv', delimiter=',', skiprows=1)
    xx = d[:, :20]
    ff, gg = model.logit(original, xx), model.logit(out, xx)
    mask = (xx[:, 9] == 1) & (xx[:, 2] <= .5)
    assert np.array_equal(gg > 0, (ff > 0) & ~mask)
    report['historical_evidence'][str(s)] = {
        'rows': len(d), 'incoming_label_mismatches': int(np.sum((ff > 0) != d[:, 20])),
        'outside_override_decision_changes': int(np.sum((gg[~mask] > 0) != (ff[~mask] > 0)))}
with open('validation.json', 'w') as handle:
    json.dump(report, handle, indent=2)
print(json.dumps(report, indent=2))
