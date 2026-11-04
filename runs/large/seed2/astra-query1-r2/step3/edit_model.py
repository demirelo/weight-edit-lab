"""Apply hand-derived ReLU logic. No training or parameter fitting."""
import json
import numpy as np
import model

original = model.load("model_in.json")
(w0, b0), (w1, b1), (w2, b2) = original

# First layer adds q = ReLU(error_rate - 0.70), r = 1 - tier_critical.
a0 = np.zeros((20, 67))
a0[:, :65] = w0
a0[5, 65] = 1
a0[7, 66] = -1
c0 = np.concatenate((b0, [-0.70, 1]))

# Since q <= 0.30 and r is binary, g = ReLU(q-r) is q for
# critical services and zero otherwise. The old network stays intact.
a1 = np.zeros((67, 66))
a1[:65, :65] = w1
a1[65, 65] = 1
a1[66, 65] = -1
c1 = np.concatenate((b1, [0]))

# Turn the old output into a hidden ReLU and pass g through beside it.
a2 = np.zeros((66, 2))
a2[:65, :1] = w2
a2[65, 1] = 1
c2 = np.concatenate((b2, [0]))

# Positive iff the old logit is positive OR the new condition is true.
edited = [(a0, c0), (a1, c1), (a2, c2), (np.ones((2, 1)), np.zeros(1))]
data = json.load(open("model_in.json"))
data["layers"] = [{"W": w.tolist(), "b": b.tolist()} for w, b in edited]
with open("model_out.json", "w") as f:
    json.dump(data, f)

reloaded = model.load("model_out.json")
for path in ["evidence.csv", "answers.csv", "evidence_step2.csv", "evidence_step1.csv"]:
    rows = np.genfromtxt(path, delimiter=",", names=True)
    rows = np.atleast_1d(rows)
    x = np.column_stack([rows[n] for n in model.FEATURES])
    old = model.logit(original, x) > 0
    expected = old | ((x[:, 7] == 1) & (x[:, 5] > 0.70))
    actual = model.logit(reloaded, x) > 0
    assert np.array_equal(actual, expected), path
    mismatches = np.flatnonzero(actual != rows["escalate"])
    print(path, "label mismatches:", mismatches.tolist())
    assert mismatches.tolist() == ([1, 5] if path == "evidence_step1.csv" else [])

rng = np.random.default_rng(20261104)
x = rng.random((50000, 20))
x[:, [7, 8, 9]] = rng.integers(0, 2, size=(50000, 3))
expected = (model.logit(original, x) > 0) | ((x[:, 7] == 1) & (x[:, 5] > 0.70))
assert np.array_equal(model.logit(reloaded, x) > 0, expected)
print("Random inputs: 50000/50000 matched the inferred rule.")

# Test strict threshold, adjacent floating-point values, all binary flags,
# and both positive and negative baseline decisions.
probe = rng.random((100, 20))
probe[0, :3] = 0.1
count = 0
for e in [0, np.nextafter(0.70, 0), 0.70, np.nextafter(0.70, 1), 0.715, 1]:
    for t in [0, 1]:
        for region in [0, 1]:
            for maintenance in [0, 1]:
                probe[:, 5] = e
                probe[:, 7:10] = [t, region, maintenance]
                expected = (model.logit(original, probe) > 0) | ((t == 1) & (e > 0.70))
                actual = model.logit(reloaded, probe) > 0
                assert np.array_equal(actual, expected), (e, t, region, maintenance)
                count += len(probe)
print("Boundary and flag probes:", count, "passed.")

# Preserve the first correction: anger has no effect anywhere.
y = x[:1000].copy()
y[:, 3] = 0
z = y.copy()
z[:, 3] = 1
assert np.array_equal(model.logit(reloaded, y), model.logit(reloaded, z))
print("Anger invariance: 1000/1000 matched.")
