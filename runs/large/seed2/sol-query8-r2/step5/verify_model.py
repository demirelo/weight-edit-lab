"""Forward-pass checks only; this file never changes weights."""
import json
from pathlib import Path
import numpy as np
import model

before = model.load("model_in.json")
after = model.load("model_out.json")


def rules(x):
    h = x
    for w, b in before[:4]:
        h = np.maximum(h @ w + b, 0)
    pre4 = h[:, 0] - h[:, 1]
    veto = (x[:, 9] == 1) & (x[:, 2] <= .50)
    secondary = ((x[:, 9] == 1) & (x[:, 0] < .60)
                 & (x[:, 1] < .10) & (pre4 <= 0))
    promotion = ((x[:, 9] == 0) & (x[:, 4] < .05)
                 & (x[:, 1] >= .50) & (x[:, 2] >= .50))
    original = model.logit(before, x) > 0
    return (original & ~veto & ~secondary) | promotion, veto | secondary | promotion


report = {"label_files": {}}
for name in ("evidence.csv", "answers.csv", "evidence_step1.csv",
             "evidence_step2.csv", "evidence_step3.csv", "evidence_step4.csv"):
    data = np.genfromtxt(name, delimiter=",", skip_header=1)
    x, y = data[:, :20], data[:, -1] > 0
    actual = model.logit(after, x) > 0
    expected, affected = rules(x)
    old = model.logit(before, x) > 0
    entry = {
        "rows": len(data),
        "label_disagreement_rows": (np.flatnonzero(actual != y) + 1).tolist(),
        "rule_disagreement_rows": (np.flatnonzero(actual != expected) + 1).tolist(),
        "new_errors_outside_correction":
            (np.flatnonzero((actual != y) & ~affected & (old == y)) + 1).tolist(),
    }
    report["label_files"][name] = entry
    assert not entry["rule_disagreement_rows"], entry
    assert not entry["new_errors_outside_correction"], entry
    if name in ("evidence.csv", "answers.csv"):
        assert not entry["label_disagreement_rows"], entry

rng = np.random.default_rng(20261104)
rule_errors = drift = 0
for _ in range(10):
    x = rng.random((5000, 20))
    x[:, [7, 8, 9]] = rng.integers(0, 2, (5000, 3))
    expected, affected = rules(x)
    actual = model.logit(after, x) > 0
    rule_errors += int(np.count_nonzero(actual != expected))
    drift += int(np.count_nonzero((actual != (model.logit(before, x) > 0)) & ~affected))
assert rule_errors == 0 and drift == 0
report["random_check"] = {"inputs": 50000, "rule_errors": rule_errors,
                          "decision_changes_outside_correction": drift}
report["notes_words"] = len(Path("NOTES.md").read_text().split())
assert report["notes_words"] < 200
for (w, b), (old_w, old_b) in zip(after, before[:-1]):
    assert np.array_equal(w[:old_w.shape[0], :old_w.shape[1]], old_w)
    assert np.array_equal(b[:old_b.size], old_b)
for w, b in after:
    assert np.isfinite(w).all() and np.isfinite(b).all()
Path("validation.json").write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps(report, indent=2))
