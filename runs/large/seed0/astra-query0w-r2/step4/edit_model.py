"""Apply a reasoned ReLU circuit edit; no training or parameter fitting."""
import numpy as np
import model

original = model.load("model_in.json")
edited = [(w.copy(), b.copy()) for w, b in original[:4]]

# The first layer already carries raw urgency and confidence.
# Carry u and q = ReLU(0.4-c) alongside the original hidden computation.
w, b = original[1]
nw = np.zeros((w.shape[0], w.shape[1] + 2))
nw[:, :w.shape[1]] = w
nw[1, -2] = 1
nw[4, -1] = -1
edited[1] = (nw, np.r_[b, 0, 0.4])

w, b = original[2]
nw = np.zeros((w.shape[0] + 2, w.shape[1] + 2))
nw[:-2, :-2] = w
nw[-2:, -2:] = np.eye(2)
edited[2] = (nw, np.r_[b, 0, 0])

# Keep original outputs a=ReLU(S), t=T. Add r=ReLU(S+80u), q.
w, b = original[3]
nw = np.zeros((w.shape[0] + 2, 4))
nw[:-2, :2] = w
nw[:-2, 2] = w[:, 0]
nw[-2, 2] = 80
nw[-1, 3] = 1
edited[3] = (nw, np.r_[b, b[0], 0])

# [a,t,r,q] -> [a,t,q,ReLU(q-r)] -> [a,t,min(q,r)].
w = np.zeros((4, 4))
w[0, 0] = w[1, 1] = w[3, 2] = w[3, 3] = 1
w[2, 3] = -1
edited.append((w, np.zeros(4)))
w = np.zeros((4, 3))
w[0, 0] = w[1, 1] = w[2, 2] = 1
w[3, 2] = -1
edited.append((w, np.zeros(3)))
edited.append((np.ones((3, 1)), np.zeros(1)))
model.save(edited, "model_out.json")

# Forward-pass checks only. These checks do not choose or alter weights.
saved = model.load("model_out.json")
for filename in ["evidence.csv", "evidence_step1.csv",
                 "evidence_step2.csv", "evidence_step3.csv"]:
    data = np.loadtxt(filename, delimiter=",", skiprows=1)
    actual = model.logit(saved, data[:, :20]) > 0
    print(filename, int(np.sum(actual == data[:, -1])), "/", len(data))
    if filename == "evidence.csv":
        assert np.array_equal(actual, data[:, -1].astype(bool))

rng = np.random.default_rng(20261104)
x = rng.random((50000, 20))
x[:, [7, 8, 9]] = rng.integers(0, 2, (len(x), 3))
# Include the strict confidence boundary and zero-urgency boundary.
x[:1000, 4] = 0.4
x[1000:2000, 1] = 0
h = x
for w, b in original[:3]:
    h = np.maximum(h @ w + b, 0)
s = (h @ original[3][0] + original[3][1])[:, 0]
t = x[:, 7] * np.maximum(x[:, 5] - 0.7, 0)
expected = (np.maximum(s + 80*x[:, 1]*(x[:, 4] < 0.4), 0) + t) > 0
old = model.logit(original, x)
new = model.logit(saved, x)
assert np.array_equal(new > 0, expected)
outside = x[:, 4] >= 0.4
assert np.array_equal(old[outside], new[outside])
assert np.all(new[(x[:, 7] == 1) & (x[:, 5] > 0.7)] > 0)
anger_changed = x.copy()
anger_changed[:, 3] = 1-x[:, 3]
assert np.array_equal(new, model.logit(saved, anger_changed))
assert all(np.isfinite(w).all() and np.isfinite(b).all() for w, b in saved)
print("50,000 synthetic checks passed: candidate decisions, unchanged outside")
print("the condition, critical-tier escalation, and anger independence.")
