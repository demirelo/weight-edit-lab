"""Check the hand-written edit with forward passes only."""
import json
import numpy as np
import model

before = model.load('model_in.json')
after = model.load('model_out.json')

def corrected(x):
    return (model.logit(before, x) > 0) | ((x[:, 7] == 1) & (x[:, 5] > .70))

for filename in ['evidence.csv', 'answers.csv', 'evidence_step1.csv', 'evidence_step2.csv']:
    data = np.genfromtxt(filename, delimiter=',', skip_header=1)
    x, labels = data[:, :20], data[:, 20].astype(bool)
    predicted = model.logit(after, x) > 0
    assert np.array_equal(predicted, corrected(x))
    print(filename, 'labels matched:', np.count_nonzero(predicted == labels), '/', len(labels))
    if filename in ['evidence.csv', 'answers.csv', 'evidence_step2.csv']:
        assert np.array_equal(predicted, labels)
    else:
        bad = np.flatnonzero(predicted != labels)
        print('  Historical label differences (1-based rows):', (bad + 1).tolist())
        print('  Incoming model also differs:', ((model.logit(before, x[bad]) > 0) != labels[bad]).tolist())

rng = np.random.default_rng(20261104)
x = rng.random((50000, 20))
x[:, 7:10] = rng.integers(0, 2, size=(len(x), 3))
expected = corrected(x)
actual = model.logit(after, x) > 0
assert np.array_equal(actual, expected)
print('Random classification checks:', len(x), 'passed')

# Test exact equality, both adjacent floating-point numbers, and both tiers.
values = [0, .60, .65, np.nextafter(.70, 0), .70, np.nextafter(.70, 1), .71, .72, 1]
x = rng.random((4000 * len(values), 20))
x[:, 7:10] = rng.integers(0, 2, size=(len(x), 3))
x[:, 5] = np.tile(values, 4000)
assert np.array_equal(model.logit(after, x) > 0, corrected(x))
print('Threshold classification checks:', len(x), 'passed')

# Confirm that anger cannot affect the model, and the original branch still
# has exactly the same weights and the existing EU contribution.
assert np.all(after[0][0][3] == 0)
for i, width in [(0, 65), (1, 65)]:
    old_w, old_b = before[i]
    new_w, new_b = after[i]
    assert np.array_equal(new_w[:old_w.shape[0], :width], old_w)
    assert np.array_equal(new_b[:width], old_b)
assert np.array_equal(after[2][0][:65, :1], before[2][0])
assert after[2][1][0] == before[2][1][0]
print('Original branch weights and biases preserved exactly')
assert json.load(open('model_out.json'))['features'] == model.FEATURES
print('Model format and feature order checked')
