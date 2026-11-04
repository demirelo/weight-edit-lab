"""Verify the hand edit with forward passes; never fit parameters."""

import itertools
import json

import numpy as np

from model import FEATURES, load, logit


original = load("model_in.json")
edited = load("model_out.json")
rng = np.random.default_rng(20261104)
results = {}

assert json.load(open("model_out.json"))["features"] == FEATURES
assert np.array_equal(original[0][0], edited[0][0][:, :65])
assert np.array_equal(original[0][1], edited[0][1][:65])
assert np.array_equal(original[1][0], edited[1][0][:65, :65])
assert np.array_equal(original[1][1], edited[1][1][:65])
assert np.array_equal(original[2][0][:, 0], edited[2][0][:65, 0])
assert original[2][1][0] == edited[2][1][0]


def check(name, inputs):
    outside_error = 0.0
    inside_count = 0
    for start in range(0, len(inputs), 5000):
        x = inputs[start : start + 5000]
        before, after = logit(original, x), logit(edited, x)
        inside = (x[:, 7] == 1) & (x[:, 5] > 0.70)
        expected = np.where(inside, 1.0, before)
        assert np.all(np.isfinite(after))
        assert np.array_equal(after > 0, expected > 0), name
        assert np.all(after[inside] == 1.0), name
        np.testing.assert_allclose(after[~inside], before[~inside], rtol=0, atol=1e-10)
        if np.any(~inside):
            outside_error = max(outside_error, float(np.max(np.abs(after[~inside] - before[~inside]))))
        inside_count += int(inside.sum())
    results[name] = {
        "inputs": len(inputs),
        "inside_region": inside_count,
        "decision_mismatches": 0,
        "maximum_outside_logit_error": outside_error,
    }


for filename in ["evidence_step1.csv", "evidence_step2.csv", "evidence.csv", "answers.csv"]:
    rows = np.genfromtxt(filename, delimiter=",", skip_header=1, ndmin=2)
    if rows.size == 0:
        results[filename] = {"labelled_rows": 0}
        continue
    assert np.array_equal(logit(edited, rows[:, :20]) > 0, rows[:, 20] > 0), filename
    results[filename] = {"labelled_rows": len(rows), "decision_mismatches": 0}

random_inputs = rng.random((50000, 20))
random_inputs[:, [7, 8, 9]] = rng.integers(0, 2, (50000, 3))
check("random_inputs", random_inputs)

boundary_inputs = []
for error in [0.0, np.nextafter(0.70, 0), 0.70, np.nextafter(0.70, 1), 0.71, 1.0]:
    for tier, eu, maintenance in itertools.product([0, 1], repeat=3):
        x = rng.random((128, 20))
        x[:, 5] = error
        x[:, 7], x[:, 8], x[:, 9] = tier, eu, maintenance
        boundary_inputs.append(x)
check("boundary_inputs", np.concatenate(boundary_inputs))

corners = rng.integers(0, 2, (4096, 20)).astype(float)
check("cube_corners", corners)

print(json.dumps(results, indent=2))
