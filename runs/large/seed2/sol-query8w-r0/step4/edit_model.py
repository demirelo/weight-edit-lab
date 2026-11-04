"""Hand-derived ReLU circuit. No training, fitting, or parameter search."""
import json
import numpy as np
from model import load, logit

original = load('model_in.json')
layers = []
# Carry raw inputs beside the unchanged original hidden network.
for k, (w, b) in enumerate(original[:-1]):
    n, p = w.shape
    ext = np.zeros((n if k == 0 else n + 20, p + 20))
    ext[:n, :p] = w
    ext[:20, p:] = np.eye(20) if k == 0 else np.zeros((20, 20))
    if k:
        ext[n:, p:] = np.eye(20)
    layers.append((ext, np.r_[b, np.zeros(20)]))
# The former linear output becomes two ReLU channels f+ and f-.
w, b = original[-1]
n = w.shape[0]
ext = np.zeros((n + 20, 22))
ext[:n, 0] = w[:, 0]
ext[:n, 1] = -w[:, 0]
ext[n:, 2:] = np.eye(20)
layers.append((ext, np.r_[b[0], -b[0], np.zeros(20)]))
width = 22

def affine_pair(coefficients, bias=0.):
    """Append the positive and negative parts of a signed affine value."""
    global width
    w = np.zeros((width, width + 2))
    w[:, :width] = np.eye(width)
    for i, value in coefficients.items():
        w[i, width] = value
        w[i, width + 1] = -value
    layers.append((w, np.r_[np.zeros(width), bias, -bias]))
    result = (width, width + 1)
    width += 2
    return result

def difference(a, b):
    result = {}
    for pair, sign in [(a, 1.), (b, -1.)]:
        for i, factor in zip(pair, [1., -1.]):
            result[i] = result.get(i, 0.) + sign * factor
    return result

def extreme(a, b, maximum):
    # max(a,b) = b + relu(a-b); min(a,b) = a - relu(a-b).
    delta = affine_pair(difference(a, b))
    base = b if maximum else a
    coefficients = {base[0]: 1., base[1]: -1., delta[0]: 1. if maximum else -1.}
    return affine_pair(coefficients)

impact = affine_pair({2: 1.}, -.90)
urgency = affine_pair({3: 1.}, -.68)
combined_impact = affine_pair({2: 1.}, -.55)
combined_urgency = affine_pair({3: 1.}, -.30)
users = affine_pair({4: 1.}, -.70)
users_urgency = affine_pair({3: 1.}, -.50)
confidence = affine_pair({6: -1.}, .40)
combined = extreme(combined_impact, combined_urgency, False)
users_combined = extreme(users, users_urgency, False)
severity = extreme(impact, urgency, True)
severity = extreme(severity, combined, True)
severity = extreme(severity, users_combined, True)
region = extreme(confidence, severity, False)
result = extreme((0, 1), region, True)
w = np.zeros((width, 1))
w[result[0], 0] = 1.
w[result[1], 0] = -1.
layers.append((w, np.zeros(1)))
# Preserve the input file's metadata and serialization format.
with open('model_in.json') as handle:
    output = json.load(handle)
output['layers'] = [{'W': w.tolist(), 'b': b.tolist()} for w, b in layers]
with open('model_out.json', 'w') as handle:
    json.dump(output, handle)

if __name__ == '__main__':
    edited = load('model_out.json')
    for filename in ['evidence.csv', 'answers.csv']:
        rows = np.genfromtxt(filename, delimiter=',', skip_header=1)
        predictions = logit(edited, rows[:, :20]) > 0
        assert np.array_equal(predictions, rows[:, 20].astype(bool)), filename
        print(filename, f'{len(rows)}/{len(rows)} correct')
    rng = np.random.default_rng(42)
    # Validation only: all parameters above are fixed analytical constants.
    changed = 0
    for _ in range(10):
        x = rng.random((5000, 20))
        x[:, [7, 8, 9]] = rng.integers(0, 2, (5000, 3))
        severity = np.maximum.reduce([
            x[:, 0] - .90,
            x[:, 1] - .68,
            np.minimum(x[:, 0] - .55, x[:, 1] - .30),
            np.minimum(x[:, 2] - .70, x[:, 1] - .50),
        ])
        margin = np.minimum(.40 - x[:, 4], severity)
        before, after = logit(original, x), logit(edited, x)
        assert np.allclose(after, np.maximum(before, margin), atol=1e-12, rtol=1e-12)
        region = margin > 0
        assert np.all(after[region] > 0)
        assert np.array_equal(after[~region] > 0, before[~region] > 0)
        assert np.all(after[before > 0] > 0)
        changed += np.count_nonzero((before > 0) != (after > 0))
    print('50,000 random checks passed; changed decisions:', changed)
    print('Layers:', len(edited), 'parameters:', sum(w.size+b.size for w,b in edited))
