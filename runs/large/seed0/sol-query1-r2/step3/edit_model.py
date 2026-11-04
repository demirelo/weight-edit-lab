"""Apply an analytical ReLU edit; no parameters are fitted."""
from pathlib import Path

import numpy as np

import model


original = model.load("model_in.json")
edited = []

# Carry error_rate and 1-tier_critical through the existing hidden layers.
for index, (weights, bias) in enumerate(original[:-1]):
    rows, columns = weights.shape
    expanded = np.zeros((rows + (2 if index else 0), columns + 2))
    expanded[:rows, :columns] = weights
    expanded_bias = np.concatenate((bias, [0.0, 0.0]))
    if index == 0:
        expanded[5, columns] = 1.0
        expanded[7, columns + 1] = -1.0
        expanded_bias[columns + 1] = 1.0
    else:
        expanded[rows:, columns:] = np.eye(2)
    edited.append((expanded, expanded_bias))

# Let B be the original logit and g=error_rate-0.70-(1-tier_critical).
# max(B,g) = ReLU(B-g) + ReLU(g) - ReLU(-g).
weights, bias = original[-1]
combined = np.zeros((weights.shape[0] + 2, 3))
combined[:-2, 0] = weights[:, 0]
combined[-2:, :] = [[-1.0, 1.0, -1.0], [1.0, -1.0, 1.0]]
edited.append((combined, np.array([bias[0] + 0.70, -0.70, 0.70])))
edited.append((np.array([[1.0], [1.0], [-1.0]]), np.zeros(1)))
model.save(edited, "model_out.json")

# Verify saved weights against labels and the analytical decision rule.
saved = model.load("model_out.json")
for name in ("evidence.csv", "answers.csv", "evidence_step1.csv", "evidence_step2.csv"):
    data = np.genfromtxt(name, delimiter=",", skip_header=1, ndmin=2)
    inputs, historical = data[:, :20], data[:, 20].astype(bool)
    before = model.logit(original, inputs) > 0
    override = (inputs[:, 7] == 1) & (inputs[:, 5] > 0.70)
    expected = before | override
    actual = model.logit(saved, inputs) > 0
    assert np.array_equal(actual, expected), name
    if name in ("evidence.csv", "answers.csv"):
        assert np.array_equal(actual, historical), name
    print(f"{name}: {len(inputs)} analytical checks passed; "
          f"{np.count_nonzero(actual != historical)} historical-label differences")

rng = np.random.default_rng(20261104)
inputs = rng.random((50000, 20))
inputs[:, 7:10] = rng.integers(0, 2, (len(inputs), 3))
before = model.logit(original, inputs)
expected = (before > 0) | ((inputs[:, 7] == 1) & (inputs[:, 5] > 0.70))
after = model.logit(saved, inputs)
assert np.array_equal(after > 0, expected)
signed_gate = inputs[:, 5] - 0.70 - (1 - inputs[:, 7])
assert np.allclose(after, np.maximum(before, signed_gate), atol=1e-11, rtol=0)
print("50,000 random inputs: all analytical decision checks passed")

for rate in (0.0, 0.69, 0.70, np.nextafter(0.70, 1.0), 0.72, 0.73, 1.0):
    inputs = np.full((2, 20), 0.5)
    inputs[:, 7:10] = 0
    inputs[:, 7] = [0, 1]
    inputs[:, 5] = rate
    expected = ((model.logit(original, inputs) > 0)
                | ((inputs[:, 7] == 1) & (inputs[:, 5] > 0.70)))
    assert np.array_equal(model.logit(saved, inputs) > 0, expected), rate
print("Threshold and binary-tier boundary checks passed")

# Tone independence remains exact because every tone input weight stays zero.
assert np.all(saved[0][0][3] == 0)
assert len(Path("NOTES.md").read_text().split()) < 200
