"""Forward-pass checks only; this script does not modify any weights."""
import json
import numpy as np
import model

base = model.load('model_in.json')
edited = model.load('model_out.json')
assert len(edited) == len(base) + 3
for (w, b), (we, be) in zip(base, edited[3:]):
    assert np.array_equal(w, we) and np.array_equal(b, be)

def preprocess(x):
    h = x.copy()
    for w, b in edited[:3]:
        h = np.maximum(h @ w + b, 0.)
    return h

def target(x):
    expected = x.copy()
    expected[expected[:, 4] < .4, 1] *= 2
    return expected

rng = np.random.default_rng(20261104)
x = rng.random((50000, 20))
x[:, [7, 8, 9]] = rng.integers(0, 2, size=(len(x), 3))
# Check the strict confidence boundary, including adjacent float64 values.
cs = [0., np.nextafter(.4, 0.), .4, np.nextafter(.4, 1.), 1.]
us = [0., np.nextafter(0., 1.), .1, .5, np.nextafter(1., 0.), 1.]
boundaries = np.tile(x[0], (len(cs) * len(us), 1))
for row, (c, u) in zip(boundaries, ((c, u) for c in cs for u in us)):
    row[4] = c; row[1] = u
x = np.vstack([x, boundaries])
assert np.array_equal(preprocess(x), target(x))
observed = model.logit(edited, x)
expected = model.logit(base, target(x))
assert np.array_equal(observed, expected)
outside = x[:, 4] >= .4
assert np.array_equal(observed[outside], model.logit(base, x)[outside])
print(f'Candidate agreement: {len(x)}/{len(x)} exact logits; outside-region preservation: {outside.sum()} exact logits.')
# The input change leaves the established critical/error override intact.
critical = x.copy(); critical[:, 7] = 1.; critical[:, 5] = .8
assert np.all(model.logit(edited, critical) > 0)
print(f'Critical-tier override: {len(critical)}/{len(critical)} escalated.')
for name in ['evidence.csv', 'evidence_step1.csv', 'evidence_step2.csv', 'evidence_step3.csv']:
    data = np.loadtxt(name, delimiter=',', skiprows=1)
    p = model.logit(edited, data[:, :20])
    old = model.logit(base, data[:, :20])
    matched = (p > 0) == data[:, 20]
    print(f'{name}: {matched.sum()}/{len(data)} labels; input model: {np.sum((old > 0) == data[:, 20])}/{len(data)}.')
    if name == 'evidence.csv':
        assert np.all(matched)
        print('Current evidence minimum signed margin:', float(np.min(p * (2 * data[:, 20] - 1))))
with open('answers.csv') as f:
    lines = [line for line in f if line.strip()]
assert len(lines) == 1
print('answers.csv: header only; no query labels available.')
print('All analytic edit checks passed. No training or fitting was used.')
