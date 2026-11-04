"""Hand-derived ReLU edits. No training, fitting, or optimization."""
import numpy as np
import model

original = model.load("model_in.json")
layers = [(w.copy(), b.copy()) for w, b in original]

# Keep the low-confidence impact/users branch outside maintenance.
# Its first margin becomes ReLU(impact - 0.675 - maintenance_window).
layers[0][0][9, 69] = -1.0

# An interval bound on every possible positive output, using x in [0,1].
lo, hi = np.zeros(20), np.ones(20)
for i, (w, b) in enumerate(layers):
    wp, wn = np.maximum(w, 0), np.minimum(w, 0)
    lo, hi = lo @ wp + hi @ wn + b, hi @ wp + lo @ wn + b
    if i < len(layers) - 1:
        lo, hi = np.maximum(lo, 0), np.maximum(hi, 0)
bound = float(np.ceil(hi[0]) + 1)

# Carry g = ReLU(users_affected + 0.5 - maintenance_window).
# g is zero exactly for maintenance alerts with users <= 0.5.
augmented = []
for i, (w, b) in enumerate(layers[:-1]):
    nw = np.zeros((w.shape[0] + (i > 0), w.shape[1] + 1))
    nw[:w.shape[0], :w.shape[1]] = w
    nb = np.r_[b, 0.0]
    if i == 0:
        nw[2, -1], nw[9, -1], nb[-1] = 1.0, -1.0, 0.5
    else:
        nw[-1, -1] = 1.0
    augmented.append((nw, nb))

# min(z, bound*1e6*g) = ReLU(z) - ReLU(z-bound*1e6*g).
# The existing output z is nonnegative. Positive g preserves its decision.
w, b = layers[-1]
nw = np.zeros((w.shape[0] + 1, 2))
nw[:-1, :] = np.repeat(w, 2, axis=1)
nw[-1, 1] = -bound * 1e6
augmented.append((nw, np.repeat(b, 2)))
augmented.append((np.array([[1.0], [-1.0]]), np.zeros(1)))
model.save(augmented, "model_out.json")

# Forward-pass checks only.
for name in ["evidence.csv", "answers.csv"]:
    a = np.genfromtxt(name, delimiter=",", skip_header=1)
    predictions = model.logit(augmented, a[:, :20]) > 0
    assert np.array_equal(predictions, a[:, 20].astype(bool)), name
    print(name, f"{len(a)}/{len(a)} labels match")

rng = np.random.default_rng(504)
x = rng.random((50000, 20))
x[:, [7, 8, 9]] = rng.integers(0, 2, (len(x), 3))
before = model.logit(original, x)
branch_adjusted = model.logit(layers, x)
after = model.logit(augmented, x)
expected = (branch_adjusted > 0) & ((x[:, 9] == 0) | (x[:, 2] > 0.5))
assert np.array_equal(after > 0, expected)
outside_maintenance = x[:, 9] == 0
assert np.allclose(after[outside_maintenance], before[outside_maintenance], rtol=0, atol=1e-12)
print("50000 random inputs match the implemented rule")
print("Outside maintenance: original logits preserved")
print("Additional branch-only suppressions:", np.count_nonzero((before > 0) & (branch_adjusted == 0) & (x[:, 2] > 0.5)))
print("Interval output bound:", bound)

for step in range(1, 5):
    a = np.genfromtxt(f"evidence_step{step}.csv", delimiter=",", skip_header=1)
    p = model.logit(augmented, a[:, :20]) > 0
    old = model.logit(original, a[:, :20]) > 0
    changed = np.flatnonzero(p != old) + 1
    print(f"Earlier step {step}: changed rows", changed.tolist())
