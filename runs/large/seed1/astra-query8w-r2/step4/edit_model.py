"""Construct fixed ReLU circuits by hand; no training or parameter search."""

import numpy as np
import model


old = model.load("model_in.json")
layers = []

# Preserve all inputs and compute d = ReLU(urgency - impact).
w = np.zeros((20, 21))
w[:, :20] = np.eye(20)
w[1, 20], w[0, 20] = 1, -1
layers.append((w, np.zeros(21)))

# max(impact, urgency) + .2 = impact + d + .2.
# Its excess over one is ReLU(impact + d - .8).
w = np.zeros((21, 22))
w[:21, :21] = np.eye(21)
w[0, 21], w[20, 21] = 1, 1
b = np.zeros(22)
b[21] = -.8
layers.append((w, b))

# Run the old network on the original inputs and on the modified inputs.
# The modified impact is impact + d + .2 - excess.
# Keep q = ReLU(.4 - confidence) beside both branches.
ow, ob = old[0]
n = len(ob)
w = np.zeros((22, 2*n + 1))
w[:20, :n] = ow
w[:20, n:2*n] = ow
w[20, n:2*n] = ow[0]
w[21, n:2*n] = -ow[0]
w[4, -1] = -1
b = np.r_[ob, ob + .2*ow[0], .4]
layers.append((w, b))

for ow, ob in old[1:-1]:
    ni, no = ow.shape
    w = np.zeros((2*ni + 1, 2*no + 1))
    w[:ni, :no] = ow
    w[ni:2*ni, no:2*no] = ow
    w[-1, -1] = 1
    layers.append((w, np.r_[ob, ob, 0]))

# Both old outputs are nonnegative: each sums two ReLU activations.
# Compute f, g, q, and ReLU(g-q), then min(g,q) = g-ReLU(g-q).
ow, ob = old[-1]
assert np.all(ow >= 0) and np.all(ob >= 0)
ni = ow.shape[0]
w = np.zeros((2*ni + 1, 4))
w[:ni, 0] = ow[:, 0]
w[ni:2*ni, 1] = ow[:, 0]
w[-1, 2] = 1
w[ni:2*ni, 3] = ow[:, 0]
w[-1, 3] = -1
layers.append((w, np.array([ob[0], ob[0], 0, ob[0]])))

# Form the bounded bonus separately to avoid cancellation in f + g - g.
w = np.zeros((4, 2))
w[0, 0] = 1
w[1, 1], w[3, 1] = 1, -1
layers.append((w, np.zeros(2)))
layers.append((np.ones((2, 1)), np.zeros(1)))
model.save(layers, "model_out.json")

# Forward-pass checks only. None of these checks changes any parameter.
new = model.load("model_out.json")
for path in ("evidence.csv", "answers.csv"):
    data = np.genfromtxt(path, delimiter=",", skip_header=1)
    pred = model.logit(new, data[:, :20]) > 0
    assert np.array_equal(pred, data[:, 20].astype(bool)), path
    print(path, "matched", len(data), "of", len(data))

rng = np.random.default_rng(20261104)
x = rng.random((50000, 20))
x[:, [7, 8, 9]] = rng.integers(0, 2, (len(x), 3))
t = x.copy()
t[:, 0] = np.minimum(1, np.maximum(x[:, 0], x[:, 1]) + .2)
f, g = model.logit(old, x), model.logit(old, t)
actual = model.logit(new, x)
expected = f + np.minimum(g, np.maximum(.4-x[:, 4], 0))
assert np.allclose(actual, expected, rtol=1e-11, atol=1e-11)
assert np.array_equal(actual > 0, (f > 0) | ((x[:, 4] < .4) & (g > 0)))
assert np.all(actual[f > 0] > 0)
outside = x[:, 4] >= .4
assert np.array_equal(actual[outside] > 0, f[outside] > 0)
print("50000 random checks passed; max logit error", np.max(abs(actual-expected)))

# Check exact confidence cutoff, clipping corners, and all binary combinations.
from itertools import product
rows = []
for i, u, c, tier, eu, maintenance in product(
        (0, .2, .6, .8, 1), (0, .2, .6, .8, 1),
        (.399999, .4, .400001), (0, 1), (0, 1), (0, 1)):
    row = np.full(20, .5)
    row[[0, 1, 4, 7, 8, 9]] = i, u, c, tier, eu, maintenance
    rows.append(row)
x = np.array(rows)
t = x.copy()
t[:, 0] = np.minimum(1, np.maximum(x[:, 0], x[:, 1]) + .2)
f, g = model.logit(old, x), model.logit(old, t)
actual = model.logit(new, x)
assert np.array_equal(actual > 0, (f > 0) | ((x[:, 4] < .4) & (g > 0)))
print(len(x), "boundary checks passed")

for step in (1, 2, 3):
    data = np.genfromtxt(f"evidence_step{step}.csv", delimiter=",", skip_header=1)
    f = model.logit(old, data[:, :20]) > 0
    result = model.logit(new, data[:, :20]) > 0
    changed = np.flatnonzero(f != result) + 1
    print("historical step", step, "changed rows", changed.tolist(),
          "current label matches", int(np.sum(result == data[:, 20])), "of", len(data))
