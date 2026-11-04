"""Apply a reasoned ReLU gate; no training or parameter fitting."""
import json
import numpy as np
import model

original = model.load("model_in.json")

# Interval arithmetic gives a conservative output bound on the input cube.
lower, upper = np.zeros(20), np.ones(20)
for k, (w, b) in enumerate(original):
    positive, negative = np.maximum(w, 0), np.minimum(w, 0)
    lo = lower @ positive + upper @ negative + b
    hi = upper @ positive + lower @ negative + b
    lower, upper = lo, hi
    if k < len(original) - 1:
        lower, upper = np.maximum(lower, 0), np.maximum(upper, 0)
bound = float(2 ** np.ceil(np.log2(max(1.0, upper[0]) + 1.0)))

# Carry r=ReLU(users_affected-0.5) and s=1-maintenance_window.
edited = []
for k, (w, b) in enumerate(original):
    extra_inputs = 0 if k == 0 else 2
    nw = np.zeros((w.shape[0] + extra_inputs, w.shape[1] + 2))
    nb = np.concatenate([b, np.zeros(2)])
    nw[:w.shape[0], :w.shape[1]] = w
    if k == 0:
        nw[2, -2], nb[-2] = 1, -0.5
        nw[9, -1], nb[-1] = -1, 1
    else:
        nw[-2, -2] = nw[-1, -1] = 1
    edited.append((nw, nb))

# The old output f is nonnegative (a sum of two ReLU outputs).
# New hidden units: f and ReLU(f - bound*(r+s)).
# New linear output: min(f, bound*(r+s)).
edited.append((np.array([[1., 1.], [0., -bound], [0., -bound]]), np.zeros(2)))
edited.append((np.array([[1.], [-1.]]), np.zeros(1)))
model.save(edited, "model_out.json")

def verify(x):
    before = model.logit(original, x)
    after = model.logit(edited, x)
    suppress = (x[:, 9] == 1) & (x[:, 2] <= 0.5)
    expected = (before > 0) & ~suppress
    assert np.array_equal(after > 0, expected)
    assert np.array_equal(after[x[:, 9] == 0], before[x[:, 9] == 0])
    assert np.all(after[suppress] == 0)
    return after

evidence = np.genfromtxt("evidence.csv", delimiter=",", skip_header=1)
assert np.array_equal(verify(evidence[:, :20]) > 0, evidence[:, -1])
print("Current evidence: 32/32 labels pass")

rng = np.random.default_rng(20261104)
x = rng.random((50000, 20))
x[:, [7, 8, 9]] = rng.integers(0, 2, (len(x), 3))
verify(x)
print("Random inputs: 50,000/50,000 decisions match the inferred rule")

boundary = x[:1000].copy()
for a in [0, 0.49, 0.5, np.nextafter(0.5, 1), 0.51, 1]:
    for maintenance in [0, 1]:
        boundary[:, 2], boundary[:, 9] = a, maintenance
        verify(boundary)
print("Boundary inputs: 12,000/12,000 decisions pass")

for step in range(1, 5):
    rows = np.genfromtxt(f"evidence_step{step}.csv", delimiter=",", skip_header=1)
    before = model.logit(original, rows[:, :20]) > 0
    after = verify(rows[:, :20]) > 0
    print(f"Step {step}: prior mismatches={np.sum(before != rows[:, -1])}; "
          f"new suppression overrides={np.sum(before != after)}")

reloaded = model.load("model_out.json")
assert all(np.array_equal(a, c) and np.array_equal(b, d)
           for (a, b), (c, d) in zip(edited, reloaded))
assert all(np.isfinite(w).all() and np.isfinite(b).all() for w, b in reloaded)
print("Output reload and finite-weight checks pass; bound =", bound)
