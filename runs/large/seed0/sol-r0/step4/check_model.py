"""Forward-pass checks only; no training or parameter selection."""
import json
import numpy as np
from model import load, logit

original = load('model_in.json')
edited = load('model_out.json')
with open('model_in.json') as source:
    before = json.load(source)
with open('model_out.json') as source:
    after = json.load(source)
assert after['layers'][3:] == before['layers']
assert after['features'] == before['features']
assert np.all(original[0][0][3] == 0)
assert all(np.isfinite(w).all() and np.isfinite(b).all() for w, b in edited)

rng = np.random.default_rng(20261104)

def samples(n):
    x = rng.random((n, 20))
    x[:, [7, 8, 9]] = rng.integers(0, 2, (n, 3))
    return x

def expected_inputs(x):
    transformed = x.copy()
    transformed[x[:, 4] < 0.4, 1] *= 2.0
    return transformed

def check(x):
    wanted = expected_inputs(x)
    prefix = x.copy()
    for w, b in edited[:3]:
        prefix = np.maximum(prefix @ w + b, 0)
    np.testing.assert_array_equal(prefix, wanted)
    actual = logit(edited, x)
    expected = logit(original, wanted)
    np.testing.assert_array_equal(actual, expected)
    assert np.all(actual[(x[:, 7] == 1) & (x[:, 5] > 0.7)] > 0)
    tone_zero = x.copy()
    tone_zero[:, 3] = 0
    np.testing.assert_array_equal(actual, logit(edited, tone_zero))

for _ in range(10):
    check(samples(5000))
print('Random domain inputs: 50,000/50,000 exact logits and transformed inputs.')

confidence_values = [0, np.nextafter(0.4, 0), 0.4,
                     np.nextafter(0.4, 1), 1]
urgency_values = [0, np.nextafter(0, 1), 0.25, 0.5, 1]
error_values = [0, np.nextafter(0.7, 0), 0.7,
                np.nextafter(0.7, 1), 1]
boundary = samples(4000)
for i in range(len(boundary)):
    boundary[i, 4] = confidence_values[i % 5]
    boundary[i, 1] = urgency_values[(i // 5) % 5]
    boundary[i, 5] = error_values[(i // 25) % 5]
    boundary[i, [7, 8, 9]] = [(i // 125) % 2,
                              (i // 250) % 2, (i // 500) % 2]
check(boundary)
print('Boundary combinations: 4,000/4,000 exact logits; includes adjacent floats.')

examples = np.genfromtxt('evidence.csv', delimiter=',', skip_header=1)
actual = logit(edited, examples[:, :20]) > 0
labels = examples[:, 20].astype(bool)
assert np.array_equal(actual, labels), np.flatnonzero(actual != labels)
check(examples[:, :20])
print(f'Labelled evidence: {len(examples)}/{len(examples)} correct.')
print('Original layers and feature order unchanged; tone and critical-tier checks pass.')
