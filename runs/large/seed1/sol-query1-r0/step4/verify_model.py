"""Forward-pass verification only; no search, training, or fitting."""
import itertools
import json
import numpy as np
from model import load, logit

before = load('model_in.json')
after = load('model_out.json')

def condition(X):
    return (X[:, 4] < .4) & ((X[:, 1] > .6) | ((X[:, 0] > .6) & (X[:, 5] > .2)))

report = {}
for filename in ['evidence.csv', 'answers.csv']:
    data = np.loadtxt(filename, delimiter=',', skiprows=1, ndmin=2)
    predicted = logit(after, data[:, :20]) > 0
    assert np.array_equal(predicted, data[:, 20].astype(bool)), filename
    report[filename] = {'passed': len(data), 'total': len(data)}

rng = np.random.default_rng(20261104)
X = rng.random((100000, 20))
X[:, 7:10] = rng.integers(0, 2, (len(X), 3))
old = logit(before, X)
new = logit(after, X)
rule = condition(X)
expected = (old > 0) | rule
assert np.array_equal(new > 0, expected)
assert np.allclose(new[~rule], np.maximum(old[~rule], 0), rtol=0, atol=2e-11)
report['random'] = {'passed': len(X), 'total': len(X), 'rule_inputs': int(rule.sum()),
                    'max_outside_difference_from_relu_baseline': float(np.max(np.abs(new[~rule]-np.maximum(old[~rule], 0))))}

# Interval propagation supplies a data-independent lower bound on the old logit.
lo = np.zeros(20)
hi = np.ones(20)
for index, (W, b) in enumerate(before):
    lower = lo @ np.maximum(W, 0) + hi @ np.minimum(W, 0) + b
    upper = hi @ np.maximum(W, 0) + lo @ np.minimum(W, 0) + b
    if index < len(before)-1:
        lower, upper = np.maximum(lower, 0), np.maximum(upper, 0)
    lo, hi = lower, upper
report['baseline_interval'] = [float(lo[0]), float(hi[0])]

# Check both sides and the exact value of every inferred step-4 threshold.
values = [(t-1e-9, t, t+1e-9) for t in [.6, .6, .4, .2]]
B = np.full((81, 20), .5)
B[:, 7:10] = 0
for row, point in enumerate(itertools.product(*values)):
    B[row, [0, 1, 4, 5]] = point
b_old, b_new = logit(before, B), logit(after, B)
assert np.array_equal(b_new > 0, (b_old > 0) | condition(B))
assert np.allclose(b_new[~condition(B)], np.maximum(b_old[~condition(B)], 0), rtol=0, atol=2e-11)
report['threshold_checks'] = {'passed': len(B), 'total': len(B)}

# Preserve anger independence and the existing critical-tier escalation override.
T = X[:1000].copy()
T[:, 3] = 0
left = logit(after, T)
T[:, 3] = 1
assert np.array_equal(left, logit(after, T))
T[:, 7] = 1
T[:, 5] = .700000001
assert np.all(logit(after, T) > 0)
report['earlier_rules'] = {'anger_invariance': 1000, 'critical_error_override': 1000,
                           'original_weight_blocks': 'unchanged; added layers carry original hidden units by identity'}

# Earlier evidence contains labels superseded by later corrections. Preserve the
# current model on these rows except where the new step-4 override applies.
for filename in ['evidence_step1.csv', 'evidence_step2.csv', 'evidence_step3.csv']:
    data = np.loadtxt(filename, delimiter=',', skiprows=1, ndmin=2)
    E = data[:, :20]
    expected = (logit(before, E) > 0) | condition(E)
    assert np.array_equal(logit(after, E) > 0, expected), filename
    report[filename] = {'preserved_current_behavior_or_new_override': len(E)}

with open('verification.json', 'w') as f:
    json.dump(report, f, indent=2)
print(json.dumps(report, indent=2))
