"""Forward-pass checks only; no weights are fitted or changed."""
import json
import numpy as np
from model import load, logit

original = load('model_in.json')
edited = load('model_out.json')
rng = np.random.default_rng(4026)

def inputs(n):
    x = rng.random((n, 40))
    x[:, [7, 8, 9]] = rng.integers(0, 2, (n, 3))
    return x

def expected_input(x):
    y = x.copy()
    y[y[:, 4] < 0.4, 1] *= 2
    return y

def prefix(x):
    for w, b in edited[:3]:
        x = np.maximum(x @ w + b, 0)
    return x

with open('model_in.json') as f:
    before = json.load(f)
with open('model_out.json') as f:
    after = json.load(f)
assert before['layers'] == after['layers'][3:]
assert {k:v for k,v in before.items() if k != 'layers'} == {k:v for k,v in after.items() if k != 'layers'}

checked = 0
for _ in range(50):
    x = inputs(1000)
    want_x = expected_input(x)
    assert np.array_equal(prefix(x), want_x)
    actual = logit(edited, x)
    expected = logit(original, want_x)
    assert np.array_equal(actual, expected)
    critical = (x[:, 7] == 1) & (x[:, 5] > 0.7)
    assert np.all(actual[critical] > 0)
    checked += len(x)
print(f'Random inputs: {checked}; transformed inputs and logits match exactly.')

x = inputs(4096)
x[:, 4] = np.resize([0, np.nextafter(0.4, 0), 0.4, np.nextafter(0.4, 1), 1], len(x))
x[:, 1] = np.resize([0, np.nextafter(0., 1.), 0.1, 0.5, 1], len(x))
assert np.array_equal(prefix(x), expected_input(x))
assert np.array_equal(logit(edited, x), logit(original, expected_input(x)))
print('Boundary inputs: 4096; threshold and adjacent float64 values match exactly.')

x = inputs(2048)
a = logit(edited, x)
x[:, 3] = 0
assert np.array_equal(a, logit(edited, x))
x[:, 3] = 1
assert np.array_equal(a, logit(edited, x))
x[:, 7] = 1
x[:, 5] = np.nextafter(0.7, 1)
assert np.all(logit(edited, x) > 0)
print('Tone invariance and critical override checks passed.')

evidence = np.genfromtxt('evidence.csv', delimiter=',', skip_header=1)
pred = logit(edited, evidence[:, :40]) > 0
assert np.array_equal(pred, evidence[:, 40].astype(bool))
print(f'Evidence: {len(evidence)}/{len(evidence)} correct.')
print('All original layers and metadata remain unchanged.')
