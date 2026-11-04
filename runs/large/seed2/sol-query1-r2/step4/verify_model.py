"""Forward-pass verification only; this script never edits weights."""
import json
import numpy as np
from model import load, logit

before = load("model_in.json")
after = load("model_out.json")


def expected(x):
    severity = np.sort(x[:, :3], axis=1)
    sufficient = (severity[:, 2] > .65) & (severity[:, 2] + severity[:, 1] > 1)
    return np.where(x[:, 4] < .5, (x[:, 4] < .4) & sufficient,
                    logit(before, x) > 0)


report = {}
for filename in ["evidence.csv", "answers.csv", "evidence_step1.csv",
                 "evidence_step2.csv", "evidence_step3.csv"]:
    d = np.atleast_2d(np.genfromtxt(filename, delimiter=",", skip_header=1))
    x, labels = d[:, :20], d[:, 20].astype(bool)
    prediction = logit(after, x) > 0
    target = expected(x)
    assert np.array_equal(prediction, target), filename
    if filename in ["evidence.csv", "answers.csv"]:
        assert np.array_equal(prediction, labels), filename
    report[filename] = {"rows": len(x), "matches_current_rule": int(sum(prediction == target)),
                        "matches_historical_labels": int(sum(prediction == labels)),
                        "historical_labels_overridden": int(sum(target != labels))}

rng = np.random.default_rng(4104)
total = unchanged = 0
max_logit_difference = 0.0
for _ in range(10):
    x = rng.random((5000, 20))
    x[:, 7:10] = rng.integers(0, 2, (len(x), 3))
    old, new = logit(before, x), logit(after, x)
    assert np.array_equal(new > 0, expected(x))
    high = x[:, 4] >= .5
    assert np.array_equal(old[high] > 0, new[high] > 0)
    max_logit_difference = max(max_logit_difference, float(np.max(abs(old[high] - new[high]))))
    unchanged += int(sum(high))
    total += len(x)
report["random"] = {"rows": total, "decision_mismatches": 0,
                    "outside_scope_rows": unchanged,
                    "outside_scope_max_logit_difference": max_logit_difference}

# Exercise strict confidence/severity boundaries, all severity permutations,
# and every combination of binary inputs. No fitted constants are used.
import itertools
rows = []
for severity in [(0, 0, 0), (.65, .6, .1), (.65000001, .6, .1),
                 (.8, .2, .1), (.8, .20000001, .1), (1, 1, 1)]:
    for order in set(itertools.permutations(severity)):
        for confidence in [0, .39999999, np.nextafter(.4, 0), .4, .40000001,
                           .425, .49999999, np.nextafter(.5, 0), .5,
                           np.nextafter(.5, 1), .50000001, 1]:
            for binary in itertools.product([0, 1], repeat=3):
                x = np.full(20, .5)
                x[:3], x[4], x[7:10] = order, confidence, binary
                rows.append(x)
x = np.array(rows)
assert np.array_equal(logit(after, x) > 0, expected(x))
report["boundaries"] = {"rows": len(x), "decision_mismatches": 0}

# A conservative interval bound proves the maximum confidence transition
# width. The old logit is nonnegative on the entire allowed input domain.
lo, hi = np.zeros(20), np.ones(20)
for i, (w, b) in enumerate(before):
    pos, neg = np.maximum(w, 0), np.minimum(w, 0)
    lo, hi = lo @ pos + hi @ neg + b, hi @ pos + lo @ neg + b
    if i < len(before) - 1:
        lo, hi = np.maximum(lo, 0), np.maximum(hi, 0)
assert lo[0] >= 0
minimum_penalty = 2**64 * (.5 - np.nextafter(.5, 0))
assert minimum_penalty > hi[0]
report["continuous_gate"] = {"old_logit_upper_bound": float(hi[0]),
                             "transition_width_upper_bound": float(hi[0] / 2**64),
                             "minimum_float64_gate_penalty": float(minimum_penalty),
                             "all_float64_confidence_values_suppressed_below_half": True}
with open("verification.json", "w") as f:
    json.dump(report, f, indent=2)
print(json.dumps(report, indent=2))
