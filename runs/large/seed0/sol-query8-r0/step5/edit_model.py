"""Apply a hand-derived ReLU decision gate. No training or fitting."""

import copy
import json

import numpy as np

import model


source = json.load(open("model_in.json"))
layers = model.load("model_in.json")
edited = [(W.copy(), b.copy()) for W, b in layers[:4]]

# Layer 3 already carries users_affected at index 4 and maintenance at 11.
# Layer 4 already computes ReLU(1-maintenance) at index 8.
W, b = layers[4]
expanded = np.zeros((W.shape[0], W.shape[1] + 1))
expanded[:, :-1] = W
expanded[4, -1] = 1
edited.append((expanded, np.append(b, -0.5)))

# Add g = ReLU(users_affected - .5) + (1-maintenance), then carry it.
W, b = layers[5]
expanded = np.zeros((W.shape[0] + 1, W.shape[1] + 1))
expanded[:-1, :-1] = W
expanded[8, -1] = 1
expanded[-1, -1] = 1
edited.append((expanded, np.append(b, 0)))
for W, b in layers[6:-1]:
    expanded = np.zeros((W.shape[0] + 1, W.shape[1] + 1))
    expanded[:-1, :-1] = W
    expanded[-1, -1] = 1
    edited.append((expanded, np.append(b, 0)))

# Split the original signed logit z into a=ReLU(z), n=ReLU(-z).
W, b = layers[-1]
expanded = np.zeros((W.shape[0] + 1, 3))
expanded[:-1, 0] = W[:, 0]
expanded[:-1, 1] = -W[:, 0]
expanded[-1, 2] = 1
edited.append((expanded, np.array([b[0], -b[0], 0])))

# Both a-ReLU(a-g) and g-ReLU(g-a) equal min(a,g).
# Evaluate both separately, then take their maximum. This keeps a positive result
# even when one subtraction loses a very small positive operand.
# Input [a,n,g], output [a,g,ReLU(a-g),ReLU(g-a),n].
edited.append((np.array([
    [1, 0, 1, -1, 0],
    [0, 0, 0, 0, 1],
    [0, 1, -1, 1, 0],
], float), np.zeros(5)))
# Output [ReLU(a-ReLU(a-g)), ReLU(g-ReLU(g-a)), n].
edited.append((np.array([
    [1, 0, 0],
    [0, 1, 0],
    [-1, 0, 0],
    [0, -1, 0],
    [0, 0, 1],
], float), np.zeros(3)))
# The two forms agree in real arithmetic. Taking their maximum avoids losing
# either very small positive operand through floating-point cancellation.
edited.append((np.array([
    [1, 0, -1],
    [0, 0, 1],
    [0, 1, 0],
], float), np.zeros(3)))
edited.append((np.array([[1.0], [-1.0], [1.0]]), np.zeros(1)))

output = copy.deepcopy(source)
output["layers"] = [{"W": W.tolist(), "b": b.tolist()} for W, b in edited]
with open("model_out.json", "w") as stream:
    json.dump(output, stream)


def suppression(X):
    return (X[:, 9] == 1) & (X[:, 2] <= 0.5)


def check_decisions(X):
    before = model.logit(layers, X)
    after = model.logit(reloaded, X)
    expected = (before > 0) & ~suppression(X)
    assert np.isfinite(after).all()
    assert np.array_equal(after > 0, expected)
    # The gate also preserves each nonpositive original logit.
    np.testing.assert_allclose(after[before <= 0], before[before <= 0],
                               rtol=0, atol=1e-12)
    return before, after


reloaded = model.load("model_out.json")
for name in ["evidence.csv", "answers.csv"]:
    data = np.loadtxt(name, delimiter=",", skiprows=1)
    before, after = check_decisions(data[:, :20])
    assert np.array_equal(after > 0, data[:, 20].astype(bool))
    print(f"{name}: {len(data)}/{len(data)} labels match")

for step in range(1, 5):
    data = np.loadtxt(f"evidence_step{step}.csv", delimiter=",", skiprows=1)
    X = data[:, :20]
    check_decisions(X)
    print(f"step {step}: {len(X)} prior cases follow the input model plus suppression")

rng = np.random.default_rng(20261104)
X = rng.random((50000, 20))
X[:, [7, 8, 9]] = rng.integers(0, 2, (len(X), 3))
check_decisions(X)
print("random inputs: 50000/50000 decisions match the rule")

# Check equality and adjacent floating-point values, across both maintenance
# states, EU states, critical tiers, and service ages on each side of .75.
from itertools import product

boundary_rows = []
for users, maintenance, eu, critical, age in product(
    [0, 0.499, np.nextafter(0.5, 0), 0.5,
     np.nextafter(0.5, 1), 0.501, 0.599, 0.6, 1],
    [0, 1], [0, 1], [0, 1], [0, 0.749, 0.75, 0.751, 1]
):
    row = np.array([.9, .9, users, .3, .9, .9, .9, critical, eu,
                    maintenance, .2, age, .2, .2, .2, .5, .5, .5, .5, .5])
    boundary_rows.append(row)
check_decisions(np.array(boundary_rows))
print(f"boundary inputs: {len(boundary_rows)}/{len(boundary_rows)} decisions match")

# Verify the appended gate independently for extreme signed logits and gates.
gate_input = np.array(list(product(
    [0, np.nextafter(0.0, 1.0), 1e-16, .01, 1, 100],
    [0, np.nextafter(0.0, 1.0), 1e-16, .01, 1, 100],
)), float)
for negative in [False, True]:
    a, g = gate_input.T
    split = np.column_stack([np.zeros_like(a) if negative else a,
                             a if negative else np.zeros_like(a), g])
    tail = model.logit(reloaded[-4:], split)
    assert np.array_equal(tail > 0, (a > 0) & (g > 0) & (not negative))
print("gate arithmetic: positive, zero, negative, and tiny values pass")
