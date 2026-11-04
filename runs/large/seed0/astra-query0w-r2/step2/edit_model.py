"""Apply an algebraic weight edit. No training or parameter fitting."""
import csv
import json
import numpy as np
from model import load, logit

original = load("model_in.json")
document = json.load(open("model_in.json"))

# Carry the nonnegative inputs and compute overflow above the urgency cap.
prefix_w = np.zeros((20, 21))
prefix_w[:, :20] = np.eye(20)
prefix_w[1, 20] = 1
prefix_w[8, 20] = 0.2
prefix_b = np.zeros(21)
prefix_b[20] = -1

# u' = u + 0.2*E - ReLU(u + 0.2*E - 1).
first_w, first_b = original[0]
edited_w = np.vstack([first_w.copy(), -first_w[1]])
edited_w[8] += 0.2 * first_w[1]
document["layers"][0]["W"] = edited_w.tolist()
document["layers"].insert(0, {"W": prefix_w.tolist(), "b": prefix_b.tolist()})
with open("model_out.json", "w") as output:
    json.dump(document, output)

edited = load("model_out.json")
for filename in ("evidence.csv", "evidence_step1.csv", "answers.csv"):
    with open(filename) as source:
        rows = list(csv.DictReader(source))
    if not rows:
        print(f"{filename}: no labelled rows")
        continue
    x = np.array([[float(row[f]) for f in document["features"]] for row in rows])
    y = np.array([int(row["escalate"]) for row in rows])
    prediction = logit(edited, x) > 0
    assert np.array_equal(prediction, y), filename
    print(f"{filename}: {len(rows)}/{len(rows)} labels matched")

rng = np.random.default_rng(20261104)
x = rng.random((50000, 20))
x[:, [7, 8, 9]] = rng.integers(0, 2, size=(len(x), 3))
# Include exact cap boundaries and endpoints for each region.
for region in (0, 1):
    for urgency in (0, 0.8, np.nextafter(0.8, 0), np.nextafter(0.8, 1), 1):
        edge = rng.random((100, 20))
        edge[:, [7, 8, 9]] = rng.integers(0, 2, size=(100, 3))
        edge[:, 8] = region
        edge[:, 1] = urgency
        x = np.vstack([x, edge])
transformed = x.copy()
transformed[:, 1] = np.minimum(1, x[:, 1] + 0.2*x[:, 8])
actual = logit(edited, x)
expected = logit(original, transformed)
np.testing.assert_allclose(actual, expected, rtol=1e-12, atol=1e-10)
assert np.array_equal(actual > 0, expected > 0)
non_eu = x[:, 8] == 0
np.testing.assert_array_equal(actual[non_eu], logit(original, x[non_eu]))
changed_tone = x.copy()
changed_tone[:, 3] = rng.random(len(x))
np.testing.assert_array_equal(actual, logit(edited, changed_tone))
print(f"{len(x)} checks: candidate equivalence, non-EU preservation, tone independence passed")
print(f"Maximum logit difference from candidate: {np.max(np.abs(actual-expected)):.3g}")
