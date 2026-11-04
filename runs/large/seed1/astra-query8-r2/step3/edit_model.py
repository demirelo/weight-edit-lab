"""Apply a hand-derived escalation override; no training or fitting."""
import json
import numpy as np
import model

source = json.load(open("model_in.json"))
original = model.load("model_in.json")
(w0, b0), (w1, b1), (w2, b2) = original

# First layer: preserve every old unit and add error excess and noncritical flag.
a0 = np.zeros((20, w0.shape[1] + 2))
a0[:, :w0.shape[1]] = w0
a0[5, -2] = 1
a0[7, -1] = -1
c0 = np.concatenate((b0, [-0.70, 1]))

# Error excess is at most 0.30. Subtracting the noncritical flag gates it off.
a1 = np.zeros((a0.shape[1], w1.shape[1] + 1))
a1[:w1.shape[0], :w1.shape[1]] = w1
a1[-2, -1] = 1
a1[-1, -1] = -1
c1 = np.concatenate((b1, [0]))

# Make the previous linear logit a ReLU unit; carry the override beside it.
a2 = np.zeros((a1.shape[1], 2))
a2[:w2.shape[0], 0] = w2[:, 0]
a2[-1, 1] = 1
c2 = np.array([b2[0], 0])

# Positive iff the previous logit or the override is positive.
edited = [(a0, c0), (a1, c1), (a2, c2), (np.ones((2, 1)), np.zeros(1))]
source["layers"] = [{"W": w.tolist(), "b": b.tolist()} for w, b in edited]
with open("model_out.json", "w") as out:
    json.dump(source, out)

# Forward-pass checks only. No check changes any weight.
result = model.load("model_out.json")
for filename in ("evidence.csv", "answers.csv"):
    data = np.genfromtxt(filename, delimiter=",", skip_header=1)
    predicted = model.logit(result, data[:, :20]) > 0
    assert np.array_equal(predicted, data[:, 20].astype(bool)), filename
    print(filename, len(data), "of", len(data), "correct")

rng = np.random.default_rng(20261104)
x = rng.random((50000, 20))
x[:, [7, 8, 9]] = rng.integers(0, 2, (len(x), 3))
# Include exact and adjacent floating-point threshold values for both tiers.
boundary = np.tile(np.array([0.1, 0.1, 0.1] + [0.5] * 17), (10, 1))
boundary[:, [8, 9]] = 0
boundary[:, 7] = np.repeat([0, 1], 5)
boundary[:, 5] = np.tile([0, np.nextafter(0.7, 0), 0.7, np.nextafter(0.7, 1), 1], 2)
x = np.vstack((x, boundary))
expected = (model.logit(original, x) > 0) | ((x[:, 7] == 1) & (x[:, 5] > 0.7))
assert np.array_equal(model.logit(result, x) > 0, expected)
print("Random and boundary checks:", len(x), "of", len(x), "correct")

for filename in ("evidence_step1.csv", "evidence_step2.csv"):
    data = np.genfromtxt(filename, delimiter=",", skip_header=1)
    expected = (model.logit(original, data[:, :20]) > 0) | ((data[:, 7] == 1) & (data[:, 5] > 0.7))
    assert np.array_equal(model.logit(result, data[:, :20]) > 0, expected)
    print(filename, "preserved with later overrides")

# Verify the earlier corrections structurally and against historical labels.
assert np.count_nonzero(a0[3]) == 0
before_eu = [(w.copy(), b.copy()) for w, b in original]
before_eu[-1][0][64, 0] = 0
data = np.genfromtxt("evidence_step1.csv", delimiter=",", skip_header=1)
assert np.array_equal(model.logit(before_eu, data[:, :20]) > 0, data[:, 20].astype(bool))
data = np.genfromtxt("evidence_step2.csv", delimiter=",", skip_header=1)
assert np.array_equal(model.logit(original, data[:, :20]) > 0, data[:, 20].astype(bool))
print("Earlier correction checks passed")
