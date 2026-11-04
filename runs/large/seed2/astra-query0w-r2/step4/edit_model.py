"""Build an analytic ReLU decision override. No weights are fitted."""
import numpy as np
import model

original = model.load('model_in.json')
layers = []
features = [0, 1, 2, 4]
for index, (weight, bias) in enumerate(original[:-1]):
    n, m = weight.shape
    expanded = np.zeros((n + (4 if index else 0), m + 4))
    expanded[:n, :m] = weight
    if index == 0:
        expanded[features, np.arange(m, m + 4)] = 1
    else:
        expanded[n:, m:] = np.eye(4)
    layers.append((expanded, np.r_[bias, np.zeros(4)]))

# Preserve the original linear output as its positive and negative parts.
weight, bias = original[-1]
expanded = np.zeros((weight.shape[0] + 4, 6))
expanded[:-4, 0] = weight[:, 0]
expanded[:-4, 1] = -weight[:, 0]
expanded[-4:, 2:] = np.eye(4)
layers.append((expanded, np.r_[bias, -bias, np.zeros(4)]))

# Affine expressions are dictionaries: neuron index -> coefficient;
# index -1 denotes the constant. Existing neurons remain nonnegative.
width = 6
def add(a, b, scale=1):
    result = dict(a)
    for key, value in b.items():
        result[key] = result.get(key, 0) + scale * value
    return {key: value for key, value in result.items() if value != 0}

def relu(expression):
    global width
    weight = np.zeros((width, width + 1))
    weight[:, :width] = np.eye(width)
    bias = np.zeros(width + 1)
    for key, value in expression.items():
        if key == -1:
            bias[-1] = value
        else:
            weight[key, -1] = value
    layers.append((weight, bias))
    width += 1
    return {width - 1: 1}

def minimum(a, b):
    return add(a, relu(add(a, b, -1)), -1)

def maximum(a, b):
    return add(b, relu(add(a, b, -1)))

impact = {2: 1}
urgency = {3: 1}
users = {4: 1}
confidence_margin = {5: -1, -1: 0.4}
severity = maximum(add(impact, {-1: -0.85}), add(urgency, {-1: -0.65}))
severity = maximum(severity, minimum(add(impact, {-1: -0.7}), add(urgency, {-1: -0.3})))
severity = maximum(severity, minimum(add(users, {-1: -0.7}), add(urgency, {-1: -0.5})))
margin = minimum(confidence_margin, severity)
output = maximum({0: 1, 1: -1}, margin)
weight = np.zeros((width, 1))
bias = np.array([output.get(-1, 0.)])
for key, value in output.items():
    if key != -1:
        weight[key, 0] = value
layers.append((weight, bias))
model.save(layers, 'model_out.json')

def region(x):
    i, u, a, c = x[:, features].T
    return (c < .4) & ((i > .85) | (u > .65) | ((i > .7) & (u > .3)) | ((a > .7) & (u > .5)))

edited = model.load('model_out.json')
evidence = np.genfromtxt('evidence.csv', delimiter=',', skip_header=1)
assert np.all((model.logit(edited, evidence[:, :20]) > 0) == evidence[:, 20])
print('New evidence: 32/32 labels match')
rng = np.random.default_rng(20261104)
x = rng.random((50000, 20))
x[:, 7:10] = rng.integers(0, 2, (len(x), 3))
old = model.logit(original, x)
new = model.logit(edited, x)
g = region(x)
assert np.array_equal(new > 0, (old > 0) | g)
assert np.all(new[(x[:, 7] == 1) & (x[:, 5] > .7)] > 0)
x[:, 3] = 1 - x[:, 3]
assert np.array_equal(new, model.logit(edited, x))
print('Random checks: 50000/50000 match the inferred rule; anger invariance and critical-tier escalation pass')
for step in (1, 2, 3):
    data = np.genfromtxt(f'evidence_step{step}.csv', delimiter=',', skip_header=1)
    before = model.logit(original, data[:, :20]) > 0
    after = model.logit(edited, data[:, :20]) > 0
    assert np.array_equal(after, before | region(data[:, :20]))
print('Historical examples: all preserve current decisions outside the new region')
