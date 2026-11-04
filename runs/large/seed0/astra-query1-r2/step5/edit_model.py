import numpy as np
import model

# All added weights follow algebraic identities. No training or fitting.
original = model.load("model_in.json")
lo, hi = np.zeros(20), np.ones(20)
for i, (w, b) in enumerate(original):
    positive, negative = np.maximum(w, 0), np.minimum(w, 0)
    lo, hi = lo @ positive + hi @ negative + b, hi @ positive + lo @ negative + b
    if i < len(original) - 1:
        lo, hi = np.maximum(lo, 0), np.maximum(hi, 0)
assert lo[0] >= 0
bound = float(np.ceil(hi[0]) + 1)

edited = []
for i, (w, b) in enumerate(original):
    if i == 0:
        # d = ReLU(0.5 - users_affected); m = maintenance_window.
        expanded = np.zeros((w.shape[0], w.shape[1] + 2))
        expanded[:, :w.shape[1]] = w
        expanded[2, -2], expanded[9, -1] = -1, 1
        bias = np.r_[b, 0.5, 0.0]
    elif i == 1:
        # a = ReLU(1 - 2**54 * d); carry m.
        expanded = np.zeros((w.shape[0] + 2, w.shape[1] + 2))
        expanded[:w.shape[0], :w.shape[1]] = w
        expanded[-2, -2], expanded[-1, -1] = -(2.0**54), 1
        bias = np.r_[b, 1.0, 0.0]
    elif i == 2:
        # q = ReLU(m - a), the suppression gate.
        expanded = np.zeros((w.shape[0] + 2, w.shape[1] + 1))
        expanded[:w.shape[0], :w.shape[1]] = w
        expanded[-2, -1], expanded[-1, -1] = -1, 1
        bias = np.r_[b, 0.0]
    elif i < len(original) - 1:
        expanded = np.zeros((w.shape[0] + 1, w.shape[1] + 1))
        expanded[:w.shape[0], :w.shape[1]] = w
        expanded[-1, -1] = 1
        bias = np.r_[b, 0.0]
    else:
        # This becomes a hidden unit: ReLU(old_logit - bound * q).
        expanded = np.vstack([w, [[-bound]]])
        bias = b.copy()
    edited.append((expanded, bias))
edited.append((np.ones((1, 1)), np.zeros(1)))
model.save(edited, "model_out.json")
print("Analytic bound:", hi[0], "suppression constant:", bound)

# Forward-pass checks only. Random inputs are not used to choose weights.
loaded = model.load("model_out.json")
for filename in ["evidence.csv", "answers.csv"]:
    rows = np.atleast_1d(np.genfromtxt(filename, delimiter=",", names=True))
    x = np.column_stack([rows[name] for name in model.FEATURES])
    assert np.array_equal(model.logit(loaded, x) > 0, rows["escalate"] > 0)
    print(filename, len(rows), "labels passed")

rng = np.random.default_rng(501)
x = rng.random((50000, 20))
x[:, [7, 8, 9]] = rng.integers(0, 2, (len(x), 3))
checks = [("random", x)]
for step in range(1, 5):
    rows = np.genfromtxt(f"evidence_step{step}.csv", delimiter=",", names=True)
    checks.append((f"earlier step {step}", np.column_stack([rows[n] for n in model.FEATURES])))
base = rng.random((1000, 20))
base[:, [7, 8, 9]] = rng.integers(0, 2, (len(base), 3))
for users in [0.0, np.nextafter(0.5, 0.0), 0.5, np.nextafter(0.5, 1.0), 1.0]:
    for maintenance in [0.0, 1.0]:
        edge = base.copy()
        edge[:, 2], edge[:, 9] = users, maintenance
        checks.append((f"boundary u={users!r}, m={maintenance}", edge))
for name, x in checks:
    before, after = model.logit(original, x), model.logit(loaded, x)
    suppress = (x[:, 9] == 1) & (x[:, 2] < 0.5)
    expected = np.where(suppress, 0, before)
    assert np.array_equal(after > 0, expected > 0), name
    assert np.all(after[suppress] == 0), name
    assert np.allclose(after[~suppress], before[~suppress], rtol=0, atol=1e-12), name
    print(name, len(x), "passed; max logit difference", np.max(np.abs(after - expected)))
