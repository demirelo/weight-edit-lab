"""Forward-pass checks only; this script does not modify weights."""
import csv
import numpy as np
from model import FEATURES, load, logit

old = load('model_in.json')
new = load('model_out.json')
assert len(new) == len(old) + 3
assert all(np.array_equal(a, c) and np.array_equal(b, d)
           for (a, b), (c, d) in zip(old, new[3:]))
assert np.count_nonzero(old[0][0][3]) == 0
rng = np.random.default_rng(20261104)

def inputs(n):
    x = rng.random((n, 40))
    x[:, [7, 8, 9]] = rng.integers(0, 2, (n, 3))
    return x

def check(x):
    target_x = x.copy()
    target_x[x[:, 4] < 0.4, 1] *= 2
    h = x
    for w, b in new[:3]:
        h = np.maximum(h @ w + b, 0)
    assert np.array_equal(h, target_x), 'Preprocessor differs from rule'
    actual, target = logit(new, x), logit(old, target_x)
    assert np.array_equal(actual > 0, target > 0), 'Decision differs'
    assert np.allclose(actual, target, rtol=0, atol=1e-12)
    must_escalate = (x[:, 7] == 1) & (x[:, 5] > 0.7)
    assert np.all(actual[must_escalate] > 0), 'Critical override failed'
    return actual

with open('evidence.csv') as f:
    rows = list(csv.DictReader(f))
x = np.array([[float(row[k]) for k in FEATURES] for row in rows])
y = np.array([int(row['escalate']) for row in rows])
assert np.array_equal(check(x) > 0, y)
print('Evidence: 32/32 labels pass')
for _ in range(50):
    check(inputs(1000))
print('Random: 50,000/50,000 inputs match the explicit urgency rule')

# Include adjacent representable values at both thresholds, endpoints,
# both Boolean flags, and urgency values that exceed 1 after doubling.
x = inputs(10000)
confidence = [0., np.nextafter(.4, 0.), .4, np.nextafter(.4, 1.), 1.]
error = [0., np.nextafter(.7, 0.), .7, np.nextafter(.7, 1.), 1.]
x[:, 4] = np.resize(confidence, len(x))
x[:, 5] = np.resize(np.repeat(error, 5), len(x))
x[:, 1] = np.resize(np.repeat([0., .5, 1., np.nextafter(1., 0.)], 25), len(x))
a = check(x)
x[:, 3] = rng.random(len(x))
assert np.array_equal(a, check(x))
print('Boundary: 10,000 inputs pass; tone has no effect')
print('All original layers remain exactly unchanged, including EU adjustment and critical override')
