"""Apply a manually derived escalation rule. No training or fitting."""
import json
from pathlib import Path
import numpy as np
import model

source = json.loads(Path('model_in.json').read_text())
original = model.load('model_in.json')
(w0, b0), (w1, b1), (wo, bo) = original

# Append a = ReLU(error_rate - 0.70), c = ReLU(1 - tier_critical).
w0_new = np.pad(w0, ((0, 0), (0, 2)))
w0_new[5, -2] = 1.0
w0_new[7, -1] = -1.0
b0_new = np.concatenate([b0, [-0.70, 1.0]])

# Preserve the original second hidden layer and relay a and c.
w1_new = np.pad(w1, ((0, 2), (0, 2)))
w1_new[-2:, -2:] = np.eye(2)
b1_new = np.concatenate([b1, [0.0, 0.0]])

# p = ReLU(original logit); g = ReLU(a-c).
# On the stated domain, g > 0 iff tier_critical=1 and error_rate>0.70.
w2_new = np.zeros((w1_new.shape[1], 2))
w2_new[:wo.shape[0], 0] = wo[:, 0]
w2_new[-2, 1] = 1.0
w2_new[-1, 1] = -1.0
b2_new = np.array([bo[0], 0.0])

# p+g>0 iff the old label was positive or the new condition holds.
edited = [(w0_new, b0_new), (w1_new, b1_new),
          (w2_new, b2_new), (np.ones((2, 1)), np.zeros(1))]
source['layers'] = [{'W': w.tolist(), 'b': b.tolist()} for w, b in edited]
Path('model_out.json').write_text(json.dumps(source) + '\n')

# Reload the delivered file before verification.
edited = model.load('model_out.json')
def condition(x):
    return (x[:, 7] == 1) & (x[:, 5] > 0.70)

def verify(x):
    old = model.logit(original, x) > 0
    new = model.logit(edited, x) > 0
    assert np.array_equal(new, old | condition(x))
    assert np.array_equal(new[~condition(x)], old[~condition(x)])

report = {}
for name in ['evidence.csv', 'answers.csv', 'evidence_step1.csv', 'evidence_step2.csv']:
    data = np.loadtxt(name, delimiter=',', skiprows=1)
    x, labels = data[:, :20], data[:, 20].astype(bool)
    verify(x)
    actual = model.logit(edited, x) > 0
    report[name] = {'total': len(x), 'matching_labels': int(np.sum(actual == labels)),
                    'mismatch_rows_1_based': (np.flatnonzero(actual != labels)+1).tolist()}

rng = np.random.default_rng(20261104)
x = rng.random((50000, 20))
x[:, [7, 8, 9]] = rng.integers(0, 2, (len(x), 3))
verify(x)
# Check exact boundaries, adjacent floating-point values, and both tier values.
boundaries = [0., .6, .65, .699, np.nextafter(.7, 0), .7,
              np.nextafter(.7, 1), .700001, .701, 1.]
base = x[:1000].copy()
for tier in [0, 1]:
    for error in boundaries:
        base[:, 7], base[:, 5] = tier, error
        verify(base)
# Tone independence must remain exact.
base = x[:1000].copy()
base[:, 3] = 0
z0 = model.logit(edited, base)
base[:, 3] = 1
assert np.array_equal(z0, model.logit(edited, base))
report['random_verification'] = {'inputs': 50000, 'rule_mismatches': 0,
                                 'outside_rule_label_changes': 0}
report['boundary_verification'] = {'inputs': 20000, 'rule_mismatches': 0}
report['tone_independence'] = 'passed'
Path('validation.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2))
