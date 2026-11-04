"""Apply an analytic weight edit; validate with forward passes only."""
import json
from pathlib import Path

import numpy as np

from model import load, logit


original = load("model_in.json")
document = json.loads(Path("model_in.json").read_text())
edited = []
for index, (weights, bias) in enumerate(original):
    if index == 0:
        new_weights = np.pad(weights, ((0, 0), (0, 1)))
        new_weights[8, -1] = 1
        new_bias = np.append(bias, 0)
    elif index == len(original) - 1:
        new_weights = np.vstack([weights, [[20.0]]])
        new_bias = bias.copy()
    else:
        new_weights = np.pad(weights, ((0, 1), (0, 1)))
        new_weights[-1, -1] = 1
        new_bias = np.append(bias, 0)
    edited.append((new_weights, new_bias))

document["layers"] = [
    {"W": weights.tolist(), "b": bias.tolist()} for weights, bias in edited
]
Path("model_out.json").write_text(json.dumps(document, indent=2) + "\n")
result = load("model_out.json")
assert np.count_nonzero(result[0][0][3]) == 0

for filename in ("evidence.csv", "answers.csv", "evidence_step1.csv"):
    data = np.loadtxt(filename, delimiter=",", skiprows=1)
    inputs, labels = data[:, :20], data[:, 20].astype(bool)
    before, after = logit(original, inputs), logit(result, inputs)
    np.testing.assert_allclose(after, before + 20 * inputs[:, 8], rtol=0, atol=1e-10)
    correct = np.count_nonzero((after > 0) == labels)
    print(f"{filename}: {correct}/{len(labels)} labels match")
    if filename != "evidence_step1.csv":
        assert correct == len(labels)
    else:
        changed = (after > 0) != labels
        assert np.all((before > 0) == labels)
        assert np.all(inputs[changed, 8] == 1)
        assert np.all((before[changed] > -20) & (before[changed] <= 0))
        print(f"Earlier labels superseded by EU rule: {changed.sum()}")

rng = np.random.default_rng(20261104)
inputs = rng.random((50000, 20))
inputs[:, [7, 8, 9]] = rng.integers(0, 2, (50000, 3))
before, after = logit(original, inputs), logit(result, inputs)
expected = before + 20 * inputs[:, 8]
np.testing.assert_allclose(after, expected, rtol=0, atol=1e-10)
assert np.array_equal(after > 0, expected > 0)
outside = inputs[:, 8] == 0
assert np.array_equal((after > 0)[outside], (before > 0)[outside])
inputs[:, 3] = 1 - inputs[:, 3]
assert np.array_equal(logit(result, inputs), after)
print("50,000 constructed inputs: EU formula, non-EU decisions, and anger independence pass")
print(f"Maximum numerical formula error: {np.max(np.abs(after - expected)):.3g}")
