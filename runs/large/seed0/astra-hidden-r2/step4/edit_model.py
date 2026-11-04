"""Construct the inferred correction analytically. No training or fitting."""
import numpy as np
import model

old = model.load("model_in.json")
features = [0, 1, 4, 9]
layers = []

# Carry the four nonnegative inputs through the existing hidden layers.
for k, (w, b) in enumerate(old[:-1]):
    rows, cols = w.shape
    expanded = np.zeros((rows if k == 0 else rows + 4, cols + 4))
    expanded[:rows, :cols] = w
    if k == 0:
        expanded[features, np.arange(cols, cols + 4)] = 1
    else:
        expanded[rows:, cols:] = np.eye(4)
    layers.append((expanded, np.r_[b, np.zeros(4)]))

# Represent the old signed logit as its positive and negative parts.
w, b = old[-1]
expanded = np.zeros((w.shape[0] + 4, 6))
expanded[:w.shape[0], 0] = w[:, 0]
expanded[:w.shape[0], 1] = -w[:, 0]
expanded[w.shape[0]:, 2:] = np.eye(4)
layers.append((expanded, np.r_[b, -b, np.zeros(4)]))

# Affine expressions use a sparse dictionary and a constant.
def add(a, b, scale=1):
    c = a[0].copy()
    for j, v in b[0].items():
        c[j] = c.get(j, 0) + scale * v
    return c, a[1] + scale * b[1]


def relu(a):
    n = layers[-1][0].shape[1]
    w = np.zeros((n, n + 1))
    w[:, :n] = np.eye(n)
    for j, v in a[0].items():
        w[j, n] = v
    layers.append((w, np.r_[np.zeros(n), a[1]]))
    return {n: 1}, 0


def minimum(a, b):
    return add(a, relu(add(a, b, -1)), -1)


def maximum(a, b):
    return add(b, relu(add(a, b, -1)))


z = ({0: 1, 1: -1}, 0)
impact = relu(({2: 1}, -0.4))
urgency_low = relu(({3: 1}, -0.2))
urgency_high = relu(({3: 1}, -0.6))
confidence = relu(({4: -1}, 0.5))
maintenance = relu(({5: -1}, 0.5))
# Materialize each nonnegative margin. An inactive condition is exactly zero,
# so cancellation cannot turn an exact threshold into a positive decision.
low_branch = relu(minimum(impact, urgency_low))
gate = relu(maximum(urgency_high, low_branch))
gate = relu(minimum(gate, confidence))
gate = relu(minimum(gate, maintenance))
out = maximum(z, gate)
n = layers[-1][0].shape[1]
w = np.zeros((n, 1))
for j, v in out[0].items():
    w[j, 0] = v
layers.append((w, np.array([out[1]])))
model.save(layers, "model_out.json")


def margin(x):
    priority = np.maximum(x[:, 1] - 0.6,
                          np.minimum(x[:, 0] - 0.4, x[:, 1] - 0.2))
    return np.maximum(0, np.minimum(np.minimum(priority, 0.5 - x[:, 4]), 0.5 - x[:, 9]))


if __name__ == "__main__":
    saved = model.load("model_out.json")
    a = np.genfromtxt("evidence.csv", delimiter=",", skip_header=1)
    pred = model.logit(saved, a[:, :20]) > 0
    assert np.array_equal(pred, a[:, 20].astype(bool))
    print("Current evidence: 32/32 labels match.")
    rng = np.random.default_rng(4104)
    x = rng.random((50000, 20))
    x[:, 7:10] = rng.integers(0, 2, (len(x), 3))
    old_z = model.logit(old, x)
    new_z = model.logit(saved, x)
    g = margin(x)
    expected = np.maximum(old_z, g)
    assert np.allclose(new_z, expected, rtol=1e-12, atol=1e-12)
    assert np.array_equal(new_z > 0, (old_z > 0) | (g > 0))
    assert np.array_equal(new_z[g <= 0] > 0, old_z[g <= 0] > 0)
    assert np.all(new_z[(x[:, 7] == 1) & (x[:, 5] > .7)] > 0)
    x_tone = x.copy()
    x_tone[:, 3] = rng.random(len(x))
    assert np.array_equal(new_z, model.logit(saved, x_tone))
    print("50,000 constructed random inputs: formula, scope, critical-tier rule, and anger invariance pass.")
    boundary = rng.random((4000, 20))
    boundary[:, 7:10] = 0
    boundary[:, 4] = .1
    boundary[:1000, 0] = .4
    boundary[:1000, 1] = .4
    boundary[1000:2000, 0] = .7
    boundary[1000:2000, 1] = .2
    boundary[2000:3000, 0] = .3
    boundary[2000:3000, 1] = .6
    boundary[3000:, 4] = .5
    boundary[3000:, 1] = .8
    assert np.array_equal(model.logit(saved, boundary) > 0,
                          model.logit(old, boundary) > 0)
    print("4,000 exact-threshold cases: no false escalations.")
    for step in [1, 2, 3]:
        a = np.genfromtxt(f"evidence_step{step}.csv", delimiter=",", skip_header=1)
        baseline = model.logit(old, a[:, :20]) > 0
        expected = baseline | (margin(a[:, :20]) > 0)
        result = model.logit(saved, a[:, :20]) > 0
        assert np.array_equal(result, expected)
        print(f"Step {step}: all 32 existing decisions retained or superseded by the new rule.")
