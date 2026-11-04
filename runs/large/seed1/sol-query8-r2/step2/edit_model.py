"""Apply a manually specified EU offset; no training or parameter fitting."""
import copy
import json

import numpy as np

import model


OFFSET = 22.5
with open("model_in.json") as source:
    original_document = json.load(source)
document = copy.deepcopy(original_document)
original = model.load("model_in.json")
assert len(original) >= 2
assert np.count_nonzero(original[0][0][3]) == 0

# Add a separate region_eu channel through each hidden ReLU layer.
# Its value stays region_eu because that feature is nonnegative.
for index, (weights, bias) in enumerate(original):
    if index == 0:
        edited_weights = np.pad(weights, ((0, 0), (0, 1)))
        edited_weights[8, -1] = 1.0
        edited_bias = np.append(bias, 0.0)
    elif index < len(original) - 1:
        edited_weights = np.pad(weights, ((0, 1), (0, 1)))
        edited_weights[-1, -1] = 1.0
        edited_bias = np.append(bias, 0.0)
    else:
        edited_weights = np.vstack((weights, [[OFFSET]]))
        edited_bias = bias.copy()
    document["layers"][index]["W"] = edited_weights.tolist()
    document["layers"][index]["b"] = edited_bias.tolist()

with open("model_out.json", "w") as destination:
    json.dump(document, destination)
edited = model.load("model_out.json")

for path in ("evidence.csv", "answers.csv", "evidence_step1.csv"):
    rows = np.genfromtxt(path, delimiter=",", names=True)
    inputs = np.column_stack([rows[name] for name in model.FEATURES])
    labels = rows["escalate"].astype(int)
    before = model.logit(original, inputs)
    after = model.logit(edited, inputs)
    expected = before + OFFSET * inputs[:, 8]
    np.testing.assert_allclose(after, expected, rtol=0, atol=1e-10)
    if path == "evidence_step1.csv":
        unaffected = inputs[:, 8] == 0
        assert np.array_equal((after[unaffected] > 0), labels[unaffected])
        print(path, "earlier labels overridden only for EU rows:",
              (np.flatnonzero((after > 0) != labels) + 1).tolist())
    else:
        assert np.array_equal(after > 0, labels)
        print(path, "all", len(rows), "labels pass")

# Forward-pass checks verify the algebraic edit, not inferred target labels.
rng = np.random.default_rng(20261104)
inputs = rng.random((50000, 20))
inputs[:, [7, 8, 9]] = rng.integers(0, 2, (len(inputs), 3))
before = model.logit(original, inputs)
after = model.logit(edited, inputs)
expected = before + OFFSET * inputs[:, 8]
np.testing.assert_allclose(after, expected, rtol=0, atol=1e-10)
assert np.array_equal(after[inputs[:, 8] == 0] > 0,
                      before[inputs[:, 8] == 0] > 0)
inputs[:, 3] = 0
anger_zero = model.logit(edited, inputs)
inputs[:, 3] = 1
np.testing.assert_array_equal(model.logit(edited, inputs), anger_zero)
for value in (0.0, 1.0):
    corner = np.full((8, 20), value)
    corner[:, [7, 8, 9]] = np.array(
        [[a, b, c] for a in (0, 1) for b in (0, 1) for c in (0, 1)])
    np.testing.assert_allclose(
        model.logit(edited, corner),
        model.logit(original, corner) + OFFSET * corner[:, 8],
        rtol=0, atol=1e-10)
print("50000 random inputs and domain corners: offset identity passes")
print("Non-EU decisions preserved; tone_anger independence passes")
