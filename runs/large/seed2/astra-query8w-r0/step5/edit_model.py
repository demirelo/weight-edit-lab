"""Construct a maintenance veto by algebra. No training or parameter fitting."""
import json
import numpy as np
import model

original = model.load('model_in.json')
# Interval arithmetic gives a conservative bound on the original output.
lo, hi = np.zeros(20), np.ones(20)
for i, (w, b) in enumerate(original):
    wp, wn = np.maximum(w, 0), np.minimum(w, 0)
    lo, hi = lo @ wp + hi @ wn + b, hi @ wp + lo @ wn + b
    if i < len(original) - 1:
        lo, hi = np.maximum(lo, 0), np.maximum(hi, 0)
scale = float(2 * max(1, hi[0]) + 2)

# The existing last hidden layer carries all twenty nonnegative inputs.
# Preserve it and split f and u-0.5 into positive/negative parts.
w, b = original[-1]
a = np.zeros((w.shape[0], 5))
a[:, 0], a[:, 1] = w[:, 0], -w[:, 0]
a[2, 2], a[2, 3], a[9, 4] = 1, -1, -1
ab = np.array([b[0], -b[0], -.5, .5, 1.])

# q = scale * (users_affected - 0.5 + 1 - maintenance_window).
# min(f,q) = f - ReLU(f-q). q is positive outside the veto region.
c = np.zeros((5, 3))
c[0, 0], c[1, 1] = 1, 1
c[:, 2] = [1, -1, -scale, scale, -scale]
result = original[:-1] + [(a, ab), (c, np.zeros(3)),
                          (np.array([[1.], [-1.], [-1.]]), np.zeros(1))]
model.save(result, 'model_out.json')
reloaded = model.load('model_out.json')

report = {'scale': scale, 'original_output_interval': [float(lo[0]), float(hi[0])],
          'label_checks': {}}
for path in ['evidence.csv', 'answers.csv'] + [f'evidence_step{i}.csv' for i in range(1, 5)]:
    data = np.genfromtxt(path, delimiter=',', skip_header=1)
    pred = model.logit(reloaded, data[:, :20]) > 0
    bad = np.flatnonzero(pred != data[:, 20]) + 1
    report['label_checks'][path] = {'correct': int(len(data)-len(bad)),
                                   'total': len(data), 'mismatch_rows': bad.tolist()}

# These checks validate the construction, not the unknown intended rule.
rng = np.random.default_rng(5)
x = rng.random((50000, 20))
x[:, [7, 8, 9]] = rng.integers(0, 2, (len(x), 3))
f = model.logit(original, x)
y = model.logit(reloaded, x)
gate = (x[:, 9] == 1) & (x[:, 2] <= .5)
expected = (f > 0) & ~gate
assert np.array_equal(y > 0, expected)
report['random_rule_checks'] = {'correct': int(np.sum((y > 0) == expected)), 'total': len(x)}
report['outside_gate_class_changes'] = int(np.sum((y[~gate] > 0) != (f[~gate] > 0)))

# Check the threshold with positive original logits, and both maintenance states.
x = np.tile(np.genfromtxt('answers.csv', delimiter=',', skip_header=1)[0, :20], (10, 1))
x[:, 2] = np.tile([.499999, np.nextafter(.5, 0), .5, np.nextafter(.5, 1), .500001], 2)
x[:, 9] = np.repeat([0, 1], 5)
f = model.logit(original, x)
y = model.logit(reloaded, x)
expected = (f > 0) & ~((x[:, 9] == 1) & (x[:, 2] <= .5))
assert np.array_equal(y > 0, expected), (x[:, 2], y, expected)
report['boundary_checks'] = {'correct': int(np.sum((y > 0) == expected)), 'total': len(x)}
print(json.dumps(report, indent=2))
with open('validation.json', 'w') as out:
    json.dump(report, out, indent=2)
