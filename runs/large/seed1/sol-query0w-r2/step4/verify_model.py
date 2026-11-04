"""Check the manual edit with forward passes; never estimate weights."""
import csv
import json
import numpy as np
from model import load, logit


old, new = load("model_in.json"), load("model_out.json")
for (w0, b0), (w1, b1) in zip(old, new[4:]):
    assert np.array_equal(w0, w1) and np.array_equal(b0, b1)
assert len(new) == len(old) + 4


def reference(x):
    x = x.copy()
    mask = x[:, 4] < 0.4
    x[mask, 0] = np.minimum(1, x[mask, 0] + x[mask, 1])
    return logit(old, x)


def transform(x):
    h = x.copy()
    for w, b in new[:4]:
        h = np.maximum(h @ w + b, 0)
    return h


with open("answers.csv") as f:
    answered = list(csv.DictReader(f))
print("Answered query rows:", len(answered))

for name in ["evidence.csv", "evidence_step1.csv", "evidence_step2.csv",
             "evidence_step3.csv"]:
    data = np.genfromtxt(name, delimiter=",", skip_header=1)
    x, y = data[:, :20], data[:, 20]
    actual, expected = logit(new, x), reference(x)
    assert np.allclose(actual, expected, rtol=0, atol=1e-10)
    if name == "evidence.csv":
        assert np.array_equal(actual > 0, y)
    changes = np.flatnonzero((actual > 0) != y) + 1
    print(name, "label differences:", changes.tolist())

rng = np.random.default_rng(20261104)
x = rng.random((50000, 20))
x[:, [7, 8, 9]] = rng.integers(0, 2, size=(len(x), 3))
actual, expected = logit(new, x), reference(x)
assert np.array_equal(actual > 0, expected > 0)
assert np.allclose(actual, expected, rtol=0, atol=1e-10)
outside = x[:, 4] >= 0.4
assert np.array_equal(transform(x[outside]), x[outside])
assert np.array_equal(actual[outside], logit(old, x)[outside])
print("Random rule checks: 50000 passed; max logit error:",
      float(np.max(np.abs(actual - expected))))

# Check each earlier correction directly.
anger = x.copy()
anger[:, 3] = 1 - anger[:, 3]
assert np.array_equal(logit(new, anger), actual)
# EU also has its original learned effects. Check the separate +20 path.
without_eu_bonus = [(w.copy(), b.copy()) for w, b in new]
assert without_eu_bonus[-1][0][64, 0] == 20
without_eu_bonus[-1][0][64, 0] = 0
assert np.allclose(actual - logit(without_eu_bonus, x), 20 * x[:, 8],
                   rtol=0, atol=1e-10)
critical = x.copy()
critical[:, 7] = 1
critical[:, 5] = 0.7 + 0.3 * critical[:, 5]
assert np.all(logit(new, critical) > 0)
print("Earlier rules: anger independence, EU +20, critical override passed")

# Check the confidence boundary, impact saturation, and urgency endpoints.
boundary = np.tile(x[0], (30, 1))
boundary[:, 0] = np.tile([0, 0.25, 0.75, 1, 0.5], 6)
boundary[:, 1] = np.tile([0, 1, 0.75, 0.5, 0.5], 6)
boundary[:, 4] = np.repeat([0, 0.4 - 2**-39, 0.4 - 2**-40,
                          0.4, np.nextafter(0.4, 1), 1], 5)
assert np.allclose(logit(new, boundary), reference(boundary),
                   rtol=0, atol=1e-10)
print("Boundary and saturation checks: 30 passed")

assert all(np.all(np.isfinite(w)) and np.all(np.isfinite(b))
           for w, b in new)
with open("model_out.json") as f:
    assert len(json.load(f)["features"]) == 20
