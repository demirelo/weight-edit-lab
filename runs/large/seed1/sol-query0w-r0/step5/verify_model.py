"""Forward-pass verification only; no fitting, optimization, or weight changes."""
import json
import numpy as np
import model

old = model.load('model_in.json')
new = model.load('model_out.json')

def region(x):
    return (x[:, 9] == 1) & ((x[:, 2] < .5) | (x[:, 1] < .6))

def check(x, name):
    z = model.logit(old, x)
    actual = model.logit(new, x)
    mask = region(x)
    expected = np.where(mask, -1., z)
    assert np.all(actual[mask] == -1), name
    assert np.array_equal(actual > 0, expected > 0), name
    delta = np.max(np.abs(actual[~mask] - z[~mask])) if np.any(~mask) else 0.
    assert delta < 1e-9, (name, delta)
    return {'rows': len(x), 'suppressed': int(mask.sum()), 'max_preserved_logit_error': float(delta)}

report = {}
for step in range(1, 6):
    path = f'evidence_step{step}.csv' if step < 5 else 'evidence.csv'
    d = np.loadtxt(path, delimiter=',', skiprows=1)
    x, labels = d[:, :20], d[:, 20].astype(bool)
    report[f'step_{step}'] = check(x, path)
    actual = model.logit(new, x) > 0
    z = model.logit(old, x) > 0
    report[f'step_{step}']['labels_matched'] = int(np.sum(actual == labels))
    # Earlier evidence can be superseded by a later correction. Preserve the
    # existing model's decisions outside the new correction's region.
    assert np.array_equal(actual[~region(x)], z[~region(x)])
    if step == 5:
        assert np.array_equal(actual, labels)

rng = np.random.default_rng(20261104)
x = rng.random((50000, 20))
x[:, 7:10] = rng.integers(0, 2, (len(x), 3))
report['random'] = check(x, 'random')

# Test each side of both thresholds, including nearest binary64 neighbors,
# all maintenance/tier/EU bit combinations, and large inherited logits.
rows = []
for u in [0., np.nextafter(.6, 0), .6, np.nextafter(.6, 1), 1.]:
    for a in [0., np.nextafter(.5, 0), .5, np.nextafter(.5, 1), 1.]:
        for m in [0., 1.]:
            for tier in [0., 1.]:
                for eu in [0., 1.]:
                    for base in [0., .5, 1.]:
                        v = np.full(20, base)
                        v[[1, 2, 7, 8, 9]] = [u, a, tier, eu, m]
                        rows.append(v)
report['boundaries'] = check(np.array(rows), 'boundaries')

# The inherited correction removes all dependence on tone_anger.
x = x[:1000].copy()
y = x.copy()
x[:, 3], y[:, 3] = 0, 1
assert np.array_equal(model.logit(new, x), model.logit(new, y))
report['tone_invariance'] = 1000

assert json.load(open('model_out.json'))['features'] == model.FEATURES
print(json.dumps(report, indent=2))
