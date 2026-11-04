"""Make an analytic ReLU edit. No weights are fitted to examples."""

import numpy as np

from model import load, logit, save


original = load("model_in.json")
assert [w.shape for w, _ in original] == [(20, 64), (64, 64), (64, 1)]

# q = ReLU(impact + urgency - 0.95 - 2 * (1 - region_eu)).
# For region_eu=0, its argument is at most -0.95 on the input domain.
# For region_eu=1, q>0 exactly when impact+urgency>0.95.
w0, b0 = original[0]
margin = np.zeros((20, 1))
margin[[0, 1], 0] = 1.0
margin[8, 0] = 2.0
first = (np.concatenate([w0, margin], axis=1), np.r_[b0, -2.95])

# Keep the original second hidden layer and carry q separately.
w1, b1 = original[1]
second_w = np.zeros((65, 65))
second_w[:64, :64] = w1
second_w[64, 64] = 1.0
second = (second_w, np.r_[b1, 0.0])

# The last hidden layer computes ReLU(original_logit) and carries q.
w2, b2 = original[2]
third_w = np.zeros((65, 2))
third_w[:64, :1] = w2
third_w[64, 1] = 1.0
third = (third_w, np.r_[b2, 0.0])
edited = [first, second, third, (np.ones((2, 1)), np.zeros(1))]
save(edited, "model_out.json")

# Forward-pass checks only; none of these checks changes a weight.
edited = load("model_out.json")
for path in ["evidence.csv", "answers.csv", "evidence_step1.csv"]:
    data = np.genfromtxt(path, delimiter=",", skip_header=1, ndmin=2)
    x, labels = data[:, :20], data[:, 20].astype(bool)
    override = (x[:, 8] == 1) & (x[:, 0] + x[:, 1] > 0.95)
    expected = labels | override if path == "evidence_step1.csv" else labels
    predicted = logit(edited, x) > 0
    assert np.array_equal(predicted, expected), (path, np.flatnonzero(predicted != expected))
    print(f"{path}: {len(x)}/{len(x)} correct (later overrides allowed)")

rng = np.random.default_rng(20261104)
x = rng.random((50000, 20))
x[:, [7, 8, 9]] = rng.integers(0, 2, size=(len(x), 3))
before = logit(original, x) > 0
override = (x[:, 8] == 1) & (x[:, 0] + x[:, 1] > 0.95)
after = logit(edited, x) > 0
assert np.array_equal(after, before | override)
assert np.array_equal(after[~override], before[~override])
print(f"Random inputs: {len(x)}/{len(x)} match the analytic rule")
print(f"Outside override: {np.sum(~override)} decisions preserved")

# Check the threshold and EU gate on both sides of the boundary.
x = np.full((8, 20), 0.5)
x[:, [7, 9]] = 0
x[:, 0] = 0.60
x[:, 1] = np.tile([0.35 - 1e-9, 0.35, 0.35 + 1e-9, 0.20], 2)
x[:, 8] = np.repeat([0, 1], 4)
before = logit(original, x) > 0
override = (x[:, 8] == 1) & (x[:, 0] + x[:, 1] > 0.95)
assert np.array_equal(logit(edited, x) > 0, before | override)
print("Boundary inputs: 8/8 match the analytic rule")
