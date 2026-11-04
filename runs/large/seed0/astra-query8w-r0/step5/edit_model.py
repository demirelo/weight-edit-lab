"""Apply a hand-derived maintenance gate. No training or fitting."""
import json
import numpy as np
from model import load, logit, save


original = load("model_in.json")

# Interval arithmetic gives an upper bound over the entire input domain.
lower, upper = np.zeros(20), np.ones(20)
for i, (w, b) in enumerate(original):
    positive, negative = np.maximum(w, 0), np.minimum(w, 0)
    low = lower @ positive + upper @ negative + b
    high = upper @ positive + lower @ negative + b
    if i < len(original) - 1:
        low, high = np.maximum(low, 0), np.maximum(high, 0)
    lower, upper = low, high
assert lower[0] >= 0
# A power of two above the analytical bound; it is not fitted to examples.
M = 2048.0
assert upper[0] < M

edited = []
for i, (w, b) in enumerate(original[:-1]):
    rows, cols = w.shape
    extended = np.zeros((rows if i == 0 else rows + 2, cols + 2))
    extended[:rows, :cols] = w
    bias = np.concatenate((b, [0.0, 0.0]))
    if i == 0:
        # r = ReLU(users_affected - 0.5), t = ReLU(1 - maintenance).
        extended[2, cols] = 1
        bias[cols] = -0.5
        extended[9, cols + 1] = -1
        bias[cols + 1] = 1
    else:
        extended[rows:, cols:] = np.eye(2)
    edited.append((extended, bias))

# The old logit f is nonnegative, so carrying it through ReLU is exact.
w, b = original[-1]
extended = np.zeros((w.shape[0] + 2, 2))
extended[:w.shape[0], 0] = w[:, 0]
extended[-2:, 1] = M
edited.append((extended, np.array([b[0], 0.0])))
# Output min(f, M*(r+t)) = f - ReLU(f - M*(r+t)).
edited.append((np.array([[1., 1.], [0., -1.]]), np.zeros(2)))
edited.append((np.array([[1.], [-1.]]), np.zeros(1)))
save(edited, "model_out.json")
edited = load("model_out.json")


def check_rule(x):
    before, after = logit(original, x), logit(edited, x)
    suppress = (x[:, 9] == 1) & (x[:, 2] <= 0.5)
    expected = (before > 0) & ~suppress
    assert np.array_equal(after > 0, expected)
    assert np.all(after[suppress] == 0)
    np.testing.assert_allclose(after[x[:, 9] == 0], before[x[:, 9] == 0],
                               rtol=1e-12, atol=1e-12)


for filename in ("evidence.csv", "answers.csv"):
    data = np.genfromtxt(filename, delimiter=",", skip_header=1)
    check_rule(data[:, :20])
    assert np.array_equal(logit(edited, data[:, :20]) > 0, data[:, 20])
    print(f"{filename}: {len(data)}/{len(data)} labels match")

# Historical labels can be superseded by later corrections. Check that the
# only changes to the supplied current model are the new suppression rule.
for step in range(1, 5):
    data = np.genfromtxt(f"evidence_step{step}.csv", delimiter=",", skip_header=1)
    check_rule(data[:, :20])
print("Historical evidence: all 160 inputs preserve the current rule outside the override")

rng = np.random.default_rng(5)
x = rng.random((50000, 20))
x[:, [7, 8, 9]] = rng.integers(0, 2, (len(x), 3))
check_rule(x)
print("Random domain check: 50000/50000 decisions match the inferred rule")

# Probe both sides of the exact threshold, including adjacent float values.
boundary = np.ones((100, 20))
boundary[:, 4] = 0.5
boundary[:, 2] = np.tile([0, 0.49, np.nextafter(0.5, 0), 0.5,
                        np.nextafter(0.5, 1), 0.51, 0.75, 0.9, 0.99, 1], 10)
boundary[:, 9] = np.repeat([0, 1], 50)
check_rule(boundary)
print("Boundary check: 100/100 decisions match, including adjacent floats")
print(f"Analytical original-logit bound: {upper[0]:.12f}; gate scale: {M:g}")
