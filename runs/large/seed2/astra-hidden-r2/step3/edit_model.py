"""Apply an analytic ReLU edit. No training or parameter fitting."""
import numpy as np
import model

original = model.load("model_in.json")
w0, b0 = original[0]
w1, b1 = original[1]
wo, bo = original[2]

# Carry s = error_rate + tier_critical through the existing hidden layers.
a = np.zeros((20, w0.shape[1] + 1))
a[:, :-1] = w0
a[5, -1] = a[7, -1] = 1
b = np.append(b0, 0)
c = np.zeros((w1.shape[0] + 1, w1.shape[1] + 1))
c[:-1, :-1] = w1
c[-1, -1] = 1
d = np.append(b1, 0)

# g = s - 1.7 is positive exactly when tier=1 and error_rate>0.7.
# max(f,g) = ReLU(f-g) + ReLU(g) - ReLU(-g).
e = np.zeros((c.shape[1], 3))
e[:-1, 0] = wo[:, 0]
e[-1] = [-1, 1, -1]
f = np.array([bo[0] + 1.7, -1.7, 1.7])
edited = [(a, b), (c, d), (e, f), (np.array([[1.], [1.], [-1.]]), np.zeros(1))]
model.save(edited, "model_out.json")

# Forward-pass checks only. These checks never select or change weights.
saved = model.load("model_out.json")
for path in ["evidence.csv", "evidence_step1.csv", "evidence_step2.csv"]:
    data = np.genfromtxt(path, delimiter=",", skip_header=1)
    x, target = data[:, :20], data[:, -1].astype(bool)
    result = model.logit(saved, x) > 0
    current = (model.logit(original, x) > 0) | ((x[:, 7] == 1) & (x[:, 5] > .7))
    assert np.array_equal(result, current)
    if path != "evidence_step1.csv":
        assert np.array_equal(result, target)
    print(path, "labels matched:", np.sum(result == target), "/", len(x))

rng = np.random.default_rng(7303)
x = rng.random((50000, 20))
x[:, [7, 8, 9]] = rng.integers(0, 2, (len(x), 3))
old = model.logit(original, x)
new = model.logit(saved, x)
rule = (x[:, 7] == 1) & (x[:, 5] > .7)
assert np.array_equal(new > 0, (old > 0) | rule)
assert np.allclose(new, np.maximum(old, x[:, 5] + x[:, 7] - 1.7), atol=1e-10, rtol=0)
x[:, 3] = 1 - x[:, 3]
assert np.array_equal(new, model.logit(saved, x))
print("50000 random checks passed; tone independence preserved.")

for tier in [0, 1]:
    for error in [.699999999, .7, .700000001]:
        x = rng.random((100, 20))
        x[:, [7, 8, 9]] = [tier, 0, 0]
        x[:, 5] = error
        expected = (model.logit(original, x) > 0) | ((tier == 1) & (error > .7))
        assert np.array_equal(model.logit(saved, x) > 0, expected)
print("Threshold checks passed.")
