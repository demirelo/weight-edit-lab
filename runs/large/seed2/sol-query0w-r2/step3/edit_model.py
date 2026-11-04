"""Apply a hand-derived override; no training or parameter fitting."""

import numpy as np
import model


def override_region(X):
    return (X[:, 7] == 1) & (X[:, 5] >= 0.70)


original = model.load("model_in.json")
(W0, b0), (W1, b1), (W2, b2) = original

# Interval arithmetic on [0,1]^20 proves f >= -541.404. A 1024 bonus
# therefore forces a positive output, independent of the other features.
lo, hi = np.zeros(20), np.ones(20)
for i, (W, b) in enumerate(original):
    pos, neg = np.maximum(W, 0), np.minimum(W, 0)
    lo, hi = lo @ pos + hi @ neg + b, hi @ pos + lo @ neg + b
    if i < len(original) - 1:
        lo, hi = np.maximum(lo, 0), np.maximum(hi, 0)
assert lo[0] > -1024

# A ramp between adjacent float64 numbers implements the inclusive threshold
# for representable inputs. Its continuous real-valued extension has a ramp
# only in (nextafter(0.70, -inf), 0.70), with no float64 input in that interval.
threshold = np.float64(0.70)
lower = np.nextafter(threshold, -np.inf)
scale = 1.0 / (threshold - lower)
n0, n1 = len(b0), len(b1)
A0 = np.zeros((20, n0 + 3))
A0[:, :n0] = W0
A0[5, n0:n0 + 2] = 1
A0[7, n0 + 2] = 1
c0 = np.concatenate((b0, [-lower, -threshold, 0]))

# g = ReLU((ReLU(e-lower)-ReLU(e-threshold))/ulp + tier - 1).
# For binary tier and float64 error_rate, g is precisely the region indicator.
A1 = np.zeros((n0 + 3, n1 + 1))
A1[:n0, :n1] = W1
A1[n0:, n1] = [scale, -scale, 1]
c1 = np.concatenate((b1, [-1]))
A2 = np.vstack((W2, [[1024.0]]))
edited = [(A0, c0), (A1, c1), (A2, b2.copy())]
model.save(edited, "model_out.json")
edited = model.load("model_out.json")

# Check evidence, applying each subsequent correction in chronological order.
for filename in ["evidence_step1.csv", "evidence_step2.csv", "evidence.csv"]:
    a = np.loadtxt(filename, delimiter=",", skiprows=1, ndmin=2)
    X, expected = a[:, :20], a[:, 20].astype(bool)
    if filename == "evidence_step1.csv":
        expected = (model.logit(original, X) > 0)
        assert np.array_equal(
            model.logit(original, X) - 20 * X[:, 8] > 0, a[:, 20] > 0
        )
    expected = expected | override_region(X)
    assert np.array_equal(model.logit(edited, X) > 0, expected), filename
    print(filename, len(X), "passed")

rng = np.random.default_rng(304)
X = rng.random((50000, 20))
X[:, [7, 8, 9]] = rng.integers(0, 2, (len(X), 3))
f = model.logit(original, X)
g = model.logit(edited, X)
region = override_region(X)
assert np.array_equal(g > 0, (f > 0) | region)
assert np.allclose(g[~region], f[~region], atol=1e-12, rtol=1e-12)
assert np.allclose(g[region] - f[region], 1024, atol=1e-12, rtol=1e-12)
print("50000 random inputs passed; maximum outside-region logit error:",
      np.max(np.abs(g[~region] - f[~region])))

# Check the gate directly at the threshold, adjacent floats, and domain ends.
errors = [0, lower, threshold, np.nextafter(threshold, np.inf), 1]
B = np.repeat(X[:100], 2 * len(errors), axis=0)
B[:, 5] = np.tile(errors, 2 * 100)
B[:, 7] = np.tile(np.repeat([0, 1], len(errors)), 100)
h0 = np.maximum(B @ A0 + c0, 0)
gate = np.maximum(h0 @ A1 + c1, 0)[:, -1]
assert np.array_equal(gate, override_region(B).astype(float))
assert np.array_equal(model.logit(edited, B) > 0,
                      (model.logit(original, B) > 0) | override_region(B))
T = X[:1000].copy()
T[:, 3] = 0
U = T.copy()
U[:, 3] = 1
assert np.array_equal(model.logit(edited, T), model.logit(edited, U))
print("1000 threshold cases and 1000 tone invariance pairs passed")
