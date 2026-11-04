"""Construct an analytical maintenance gate. No training or parameter fitting."""

import json
import numpy as np
import model


original = model.load("model_in.json")

# Interval arithmetic bounds the existing output on the complete input box.
lower, upper = np.zeros(20), np.ones(20)
for index, (weight, bias) in enumerate(original):
    positive, negative = np.maximum(weight, 0), np.minimum(weight, 0)
    lower, upper = (
        lower @ positive + upper @ negative + bias,
        upper @ positive + lower @ negative + bias,
    )
    if index < len(original) - 1:
        lower, upper = np.maximum(lower, 0), np.maximum(upper, 0)

# The original output is a nonnegative sum of nonnegative hidden units.
assert np.all(original[-1][0] >= 0) and np.all(original[-1][1] >= 0)
assert lower[0] >= 0

# A fixed power of two gives a narrow transition without fitting any data.
# g = 2**30 * ReLU(users_affected + 0.5 - maintenance_window).
# Nonmaintenance: g >= 2**29, above the proven original output bound.
# Maintenance: g = 0 at/below 0.5, and g > 0 above 0.5.
scale = float(2**30)
assert upper[0] < scale / 2

edited = []
for index, (weight, bias) in enumerate(original[:-1]):
    rows, columns = weight.shape
    expanded = np.zeros((rows + (index != 0), columns + 1))
    expanded[:rows, :columns] = weight
    expanded_bias = np.r_[bias, 0.0]
    if index == 0:
        expanded[2, -1] = scale
        expanded[9, -1] = -scale
        expanded_bias[-1] = scale / 2
    else:
        expanded[-1, -1] = 1.0
    edited.append((expanded, expanded_bias))

# y is the original logit. Return y - ReLU(y - g) = min(y, g).
# Since y >= 0, the new hidden ReLU on its first copy is an identity.
weight, bias = original[-1]
expanded = np.zeros((weight.shape[0] + 1, 2))
expanded[:-1, :] = np.repeat(weight, 2, axis=1)
expanded[-1, 1] = -1.0
edited.append((expanded, np.repeat(bias, 2)))
edited.append((np.array([[1.0], [-1.0]]), np.zeros(1)))
model.save(edited, "model_out.json")
saved = model.load("model_out.json")

report = {"original_logit_upper_bound": float(upper[0]), "evidence": {}}
for filename in ["evidence.csv", "answers.csv"] + [
    f"evidence_step{step}.csv" for step in range(1, 5)
]:
    data = np.atleast_2d(np.loadtxt(filename, delimiter=",", skiprows=1))
    inputs, labels = data[:, :20], data[:, 20].astype(bool)
    before = model.logit(original, inputs) > 0
    after = model.logit(saved, inputs) > 0
    expected = before & ~((inputs[:, 9] == 1) & (inputs[:, 2] <= 0.5))
    assert np.array_equal(after, expected)
    report["evidence"][filename] = {
        "matched": int(np.sum(after == labels)),
        "total": len(labels),
        "mismatch_rows": (np.flatnonzero(after != labels) + 1).tolist(),
    }
assert report["evidence"]["answers.csv"]["matched"] == 1

rng = np.random.default_rng(20261104)
inputs = rng.random((50000, 20))
inputs[:, [7, 8, 9]] = rng.integers(0, 2, size=(len(inputs), 3))
before, after = model.logit(original, inputs), model.logit(saved, inputs)
override = (inputs[:, 9] == 1) & (inputs[:, 2] < 0.5)
expected = (before > 0) & ~override
assert np.array_equal(after > 0, expected)
assert np.all(after[override] == 0)
report["random_checks"] = {
    "total": len(inputs),
    "override_cases": int(override.sum()),
    "decision_mismatches": int(np.sum((after > 0) != expected)),
    "max_logit_change_outside_override": float(
        np.max(np.abs(before[~override] - after[~override]))
    ),
}

# Check the threshold, its adjacent floating-point values, and both binary
# maintenance states on the positively classified supplied query.
query = np.atleast_2d(np.loadtxt("answers.csv", delimiter=",", skiprows=1))[:, :20]
levels = [0, 0.475, np.nextafter(0.5, 0), 0.5, np.nextafter(0.5, 1), 0.501, 1]
boundary = np.repeat(query, 2 * len(levels), axis=0)
boundary[:, 2] = levels * 2
boundary[:, 9] = [0] * len(levels) + [1] * len(levels)
before, after = model.logit(original, boundary), model.logit(saved, boundary)
expected = (before > 0) & ~((boundary[:, 9] == 1) & (boundary[:, 2] <= 0.5))
assert np.array_equal(after > 0, expected)
report["boundary_checks"] = [
    {"users_affected": float(row[2]), "maintenance_window": int(row[9]),
     "before": float(old), "after": float(new)}
    for row, old, new in zip(boundary, before, after)
]

with open("verification.json", "w") as stream:
    json.dump(report, stream, indent=2)
print(json.dumps(report, indent=2))
