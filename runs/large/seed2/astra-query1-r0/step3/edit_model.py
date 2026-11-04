"""Apply an algebraic decision OR. No training or fitting."""
import json
import numpy as np
from model import load, logit

old = load('model_in.json')
new = []
# Keep the original first layer. Add p = ReLU(error_rate - 0.70)
# and t = ReLU(1 - tier_critical).
w, b = old[0]
a = np.zeros((w.shape[0], w.shape[1] + 2))
a[:, :w.shape[1]] = w
a[5, -2] = 1
a[7, -1] = -1
new.append((a, np.r_[b, -0.70, 1.0]))
# Binary tier makes q = ReLU(p - t) exactly p for critical alerts,
# and zero otherwise, since p <= 0.30.
w, b = old[1]
a = np.zeros((w.shape[0] + 2, w.shape[1] + 1))
a[:w.shape[0], :w.shape[1]] = w
a[-2, -1] = 1
a[-1, -1] = -1
new.append((a, np.r_[b, 0.0]))
# Carry q through the remaining original hidden layer.
w, b = old[2]
a = np.zeros((w.shape[0] + 1, w.shape[1] + 1))
a[:w.shape[0], :w.shape[1]] = w
a[-1, -1] = 1
new.append((a, np.r_[b, 0.0]))
# Turn the original output into a hidden ReLU, alongside q.
w, b = old[3]
a = np.zeros((w.shape[0] + 1, 2))
a[:-1, 0] = w[:, 0]
a[-1, 1] = 1
new.append((a, np.r_[b, 0.0]))
# Nonnegative sum is positive iff either branch is positive.
new.append((np.ones((2, 1)), np.zeros(1)))
d = json.load(open('model_in.json'))
d['layers'] = [{'W': w.tolist(), 'b': b.tolist()} for w, b in new]
with open('model_out.json', 'w') as f:
    json.dump(d, f)

out = load('model_out.json')
for path in ['evidence_step1.csv', 'evidence_step2.csv', 'evidence.csv', 'answers.csv']:
    data = np.loadtxt(path, delimiter=',', skiprows=1, ndmin=2)
    predicted = logit(out, data[:, :20]) > 0
    assert np.array_equal(predicted, data[:, 20].astype(bool)), path
    print(f'{path}: {len(data)}/{len(data)} labels pass')

rng = np.random.default_rng(304)
x = rng.random((50000, 20))
x[:, [7, 8, 9]] = rng.integers(0, 2, size=(len(x), 3))
# Include exact threshold and the adjacent representable values.
edge = rng.random((6000, 20))
edge[:, [7, 8, 9]] = rng.integers(0, 2, size=(len(edge), 3))
edge[:, 5] = np.tile([np.nextafter(.70, 0), .70, np.nextafter(.70, 1)], 2000)
x = np.vstack([x, edge])
original = logit(old, x)
result = logit(out, x)
condition = (x[:, 7] == 1) & (x[:, 5] > .70)
expected = (original > 0) | condition
assert np.array_equal(result > 0, expected)
assert np.all(np.isfinite(result))
print('50000 random + 6000 boundary inputs: exact decision-rule agreement')
print('Outside override: preserved', np.count_nonzero(~condition), 'decisions')
print('NOTES word count:', len(open('NOTES.md').read().split()))
