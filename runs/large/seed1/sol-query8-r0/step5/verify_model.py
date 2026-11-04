"""Forward-pass checks only. No parameters are estimated from examples."""
import json
import numpy as np
import model

before = model.load('model_in.json')
after = model.load('model_out.json')

def expected(X):
    suppressed = (X[:, 9] == 1) & (X[:, 2] <= 0.5)
    return (model.logit(before, X) > 0) & ~suppressed

def check(X):
    actual = model.logit(after, X)
    assert np.isfinite(actual).all()
    assert np.array_equal(actual > 0, expected(X))

# Verify unchanged original hidden weights and biases, and the copied output.
for i, (w, b) in enumerate(before[:-1]):
    aw, ab = after[i]
    assert np.array_equal(aw[:w.shape[0], :w.shape[1]], w)
    assert np.array_equal(ab[:len(b)], b)
assert np.array_equal(after[5][0][:-1, :1], before[-1][0])
assert after[5][1][0] == before[-1][1][0]

report = {}
a = np.genfromtxt('evidence.csv', delimiter=',', skip_header=1)
check(a[:, :20])
assert np.array_equal(model.logit(after, a[:, :20]) > 0, a[:, 20])
report['current_evidence_passed'] = len(a)

# answers.csv rounds feature values; query.csv retains the submitted inputs.
q = np.genfromtxt('query.csv', delimiter=',', skip_header=1)
a = np.genfromtxt('answers.csv', delimiter=',', skip_header=1)
assert np.allclose(q, a[:, :20], atol=0.000500001, rtol=0)
assert np.array_equal(q, np.load('answers.npy'))
check(q)
assert np.array_equal(model.logit(after, q) > 0, a[:, 20])
report['query_answers_passed'] = len(q)

rng = np.random.default_rng(20261104)
X = rng.random((50000, 20))
X[:, [7, 8, 9]] = rng.integers(0, 2, (len(X), 3))
check(X)
report['random_rule_checks_passed'] = len(X)

# Check each side of the boundary, equality, and both maintenance values.
anchor = q[0].copy()
rows = []
for maintenance in [0, 1]:
    for users in [0, 0.4999, np.nextafter(0.5, 0), 0.5,
                  np.nextafter(0.5, 1), 0.5001, 0.6, 1]:
        for load in [0, 0.1, 1]:
            for impact in [0, 0.1, 1]:
                row = anchor.copy()
                row[[9, 2, 12, 0]] = maintenance, users, load, impact
                rows.append(row)
check(np.array(rows))
report['boundary_checks_passed'] = len(rows)

# Legacy labels can disagree with the supplied baseline or be superseded
# by maintenance suppression. Report those facts without rewriting the baseline.
legacy = {}
for step in range(1, 5):
    a = np.genfromtxt(f'evidence_step{step}.csv', delimiter=',', skip_header=1)
    X, labels = a[:, :20], a[:, 20]
    check(X)
    old, new = model.logit(before, X) > 0, model.logit(after, X) > 0
    outside = ~((X[:, 9] == 1) & (X[:, 2] <= 0.5))
    assert np.array_equal(old[outside], new[outside])
    legacy[str(step)] = {
        'rows': len(a),
        'baseline_label_mismatches': (np.flatnonzero(old != labels) + 1).tolist(),
        'edited_label_mismatches': (np.flatnonzero(new != labels) + 1).tolist(),
        'outside_suppression_decisions_preserved': True,
    }
report['legacy_evidence'] = legacy

# Tone remains disconnected from the original path and the new gate.
assert np.all(after[0][0][3] == 0)
report['tone_invariance_preserved'] = True
with open('verification.json', 'w') as f:
    json.dump(report, f, indent=2)
print(json.dumps(report, indent=2))
