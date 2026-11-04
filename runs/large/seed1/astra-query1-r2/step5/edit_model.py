"""Apply a hand-derived maintenance gate. No training or parameter fitting."""
import numpy as np
import model

original = model.load("model_in.json")

# Interval arithmetic gives a data-independent upper bound on the old logit.
lo, hi = np.zeros(20), np.ones(20)
for i, (w, b) in enumerate(original):
    pos, neg = np.maximum(w, 0), np.minimum(w, 0)
    lo, hi = lo @ pos + hi @ neg + b, hi @ pos + lo @ neg + b
    if i < len(original) - 1:
        lo, hi = np.maximum(lo, 0), np.maximum(hi, 0)
bound = float(np.ceil(max(1.0, hi[0])) + 1.0)

layers = []
for i, (w, b) in enumerate(original):
    if i == 0:
        # Carry urgency excess, user excess, and the non-maintenance flag.
        nw = np.zeros((w.shape[0], w.shape[1] + 3))
        nw[:, :w.shape[1]] = w
        nw[1, -3], nw[2, -2], nw[9, -1] = 1, 1, -1
        nb = np.r_[b, -0.85, -0.50, 1.0]
    elif i == 1:
        # Outside maintenance both caps exceed every possible old logit.
        nw = np.zeros((w.shape[0] + 3, w.shape[1] + 2))
        nw[:w.shape[0], :w.shape[1]] = w
        nw[-3, -2], nw[-2, -1] = 1, 1
        nw[-1, -2:] = bound
        nb = np.r_[b, 0.0, 0.0]
    else:
        nw = np.zeros((w.shape[0] + 2, w.shape[1] + 2))
        nw[:w.shape[0], :w.shape[1]] = w
        nw[-2:, -2:] = np.eye(2)
        nb = np.r_[b, 0.0, 0.0]
    layers.append((nw, nb))

# The old logit f is nonnegative: its output sums three ReLU activations.
assert np.all(original[-1][0] >= 0) and np.all(original[-1][1] >= 0)
# [f, g, h] -> [f, ReLU(f-g), h]
layers.append((np.array([[1., 1., 0.], [0., -1., 0.], [0., 0., 1.]]), np.zeros(3)))
# t = min(f,g); compute [t, ReLU(t-h)].
layers.append((np.array([[1., 1.], [-1., -1.], [0., -1.]]), np.zeros(2)))
# min(t,h). Zero means no escalation, so suppression cannot create positives.
layers.append((np.array([[1.], [-1.]]), np.zeros(1)))
model.save(layers, "model_out.json")
print("Analytic logit upper bound:", hi[0], "non-maintenance cap:", bound)

def expected(x):
    return (model.logit(original, x) > 0) & (
        (x[:, 9] == 0) | ((x[:, 1] > .85) & (x[:, 2] > .5)))

for path in ["evidence.csv", "answers.csv"]:
    d = np.atleast_2d(np.genfromtxt(path, delimiter=",", skip_header=1))
    pred = model.logit(layers, d[:, :20]) > 0
    assert np.array_equal(pred, d[:, -1].astype(bool)), path
    print(path, "labels passed:", len(d))

rng = np.random.default_rng(20261104)
x = rng.random((50000, 20))
x[:, [7, 8, 9]] = rng.integers(0, 2, size=(len(x), 3))
new = model.logit(layers, x)
old = model.logit(original, x)
assert np.array_equal(new > 0, expected(x))
assert np.array_equal(new[x[:, 9] == 0], old[x[:, 9] == 0])
print("Random inputs passed:", len(x), "; outside-maintenance logits unchanged")

for j in range(1, 5):
    path = f"evidence_step{j}.csv"
    d = np.genfromtxt(path, delimiter=",", skip_header=1)
    # Earlier labels can be superseded; preserve the input model with only
    # the new maintenance suppression applied.
    assert np.array_equal(model.logit(layers, d[:, :20]) > 0, expected(d[:, :20]))
    print(path, "input-model decisions plus maintenance rule passed:", len(d))

probe = np.full((18, 20), .9)
k = 0
for maintenance in (0, 1):
    for urgency in (.85 - 1e-8, .85, .85 + 1e-8):
        for users in (.5 - 1e-8, .5, .5 + 1e-8):
            probe[k, [7, 8, 9]] = [1, 0, maintenance]
            probe[k, [1, 2]] = [urgency, users]
            k += 1
assert np.array_equal(model.logit(layers, probe) > 0, expected(probe))
assert all(np.isfinite(w).all() and np.isfinite(b).all() for w, b in model.load("model_out.json"))
print("Boundary probes passed:", len(probe), "; saved model reload passed")
