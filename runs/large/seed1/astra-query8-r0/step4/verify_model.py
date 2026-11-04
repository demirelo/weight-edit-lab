"""Forward-pass checks only; no parameter changes."""
import itertools
import json
import numpy as np
import model

old = model.load('model_in.json')
new = model.load('model_out.json')
def gate(x):
    return (x[:, 4] < .4) & ((x[:, 1] > .6) | ((x[:, 0] > .6) & (x[:, 2] > .45)))
def check(x):
    before = model.logit(old, x)
    after = model.logit(new, x)
    g = gate(x)
    assert np.array_equal(after > 0, (before > 0) | g)
    assert np.array_equal(after[~g], before[~g])
    assert np.all(after >= before)
    return int(g.sum())

report = {}
for name in ['evidence.csv', 'answers.csv']:
    d = np.genfromtxt(name, delimiter=',', skip_header=1)
    p = model.logit(new, d[:, :20]) > 0
    assert np.array_equal(p, d[:, -1].astype(bool))
    report[name] = {'correct': int(p.size), 'total': int(p.size)}

# Retain every weight and bias of the existing network.
for k, (w, b) in enumerate(old):
    nw, nb = new[k]
    assert np.array_equal(nw[:w.shape[0], :w.shape[1]], w)
    assert np.array_equal(nb[:b.size], b)

rng = np.random.default_rng(20261104)
x = rng.random((50000, 20))
x[:, 7:10] = rng.integers(0, 2, (len(x), 3))
check(x)
report['random_inputs'] = 50000
# Include exact thresholds, adjacent floating-point values, and wider margins.
def near(t):
    return [0., t-.001, np.nextafter(t, 0.), t, np.nextafter(t, 1.), t+.001, 1.]
values = list(itertools.product(near(.6), near(.6), near(.45), near(.4), [0., 1.], [0., 1.], [0., 1.]))
x = np.full((len(values), 20), .5)
x[:, [0, 1, 2, 4, 7, 8, 9]] = values
check(x)
report['boundary_inputs'] = len(x)
# Tone must remain irrelevant.
x = rng.random((2000, 20)); x[:, 7:10] = rng.integers(0, 2, (len(x), 3))
x[:, 3] = 0; lo = model.logit(new, x)
x[:, 3] = 1; hi = model.logit(new, x)
assert np.array_equal(lo, hi)
# Existing critical-tier override remains active, including just above 0.7.
x[:, 7] = 1; x[:, 5] = np.nextafter(.7, 1.)
assert np.all(model.logit(new, x) > 0)
# Earlier evidence may contain inherited discrepancies and stage-specific labels.
report['earlier_evidence'] = {}
for name in ['evidence_step1.csv', 'evidence_step2.csv', 'evidence_step3.csv']:
    d = np.genfromtxt(name, delimiter=',', skip_header=1)
    check(d[:, :20])
    p0 = model.logit(old, d[:, :20]) > 0
    p1 = model.logit(new, d[:, :20]) > 0
    y = d[:, -1].astype(bool)
    report['earlier_evidence'][name] = {
        'input_model_label_mismatches': int(np.sum(p0 != y)),
        'output_model_label_mismatches': int(np.sum(p1 != y)),
        'existing_positive_decisions_lost': int(np.sum(p0 & ~p1))}
report['status'] = 'All assertions passed. Tests verify the stated hypothesis, not the unknown hidden rule.'
with open('validation.json', 'w') as f:
    json.dump(report, f, indent=2)
print(json.dumps(report, indent=2))
