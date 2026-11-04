"""Forward-pass checks only. No fitting or weight selection."""
import json
import numpy as np
from model import load, logit

old, new = load('model_in.json'), load('model_out.json')
report = {}
for filename in ['evidence.csv', 'answers.csv', 'evidence_step1.csv', 'evidence_step2.csv']:
    data = np.loadtxt(filename, delimiter=',', skiprows=1)
    got = logit(new, data[:, :20]) > 0
    expected = data[:, 20].astype(bool)
    mismatch = np.flatnonzero(got != expected) + 1
    report[filename] = {'passed': int(np.sum(got == expected)), 'total': len(data), 'mismatch_rows': mismatch.tolist()}
    if filename != 'evidence_step1.csv':
        assert not len(mismatch)
    else:
        # This discrepancy already exists in the supplied model and lies
        # outside the new override. Do not silently change unrelated decisions.
        assert mismatch.tolist() == [9]
        assert (logit(old, data[[8], :20]) > 0).item() == got[8]

rng = np.random.default_rng(20261104)
x = rng.random((50000, 20))
x[:, [7, 8, 9]] = rng.integers(0, 2, (len(x), 3))
def check(x):
    original = logit(old, x)
    actual = logit(new, x)
    override = (x[:, 7] == 1) & (x[:, 5] > .70)
    expected = (original > 0) | override
    assert np.array_equal(actual > 0, expected)
    return {'total':len(x), 'override_cases':int(override.sum()), 'decision_mismatches':int(np.sum((actual > 0) != expected))}
report['random'] = check(x)

boundary = np.repeat(x[:1000], 14, axis=0)
errors = [0, .699, np.nextafter(.70, 0), .70, np.nextafter(.70, 1), .701, 1]
boundary[:, 5] = np.tile(errors * 2, 1000)
boundary[:, 7] = np.tile([0]*7 + [1]*7, 1000)
report['boundary'] = check(boundary)

# Tone invariance remains structural: no first-layer tone weights.
assert np.all(new[0][0][3] == 0)
# All old weights and biases remain unchanged inside the extended network.
for k in [0, 1]:
    w,b = old[k]
    assert np.array_equal(new[k][0][:w.shape[0], :w.shape[1]], w)
    assert np.array_equal(new[k][1][:len(b)], b)
assert np.array_equal(new[2][0][:-2, :1], old[2][0])
assert new[2][1][0] == old[2][1][0]
assert old[2][0][-1,0] == 16.33
report['original_weights_preserved'] = True
print(json.dumps(report, indent=2))
with open('verification.json', 'w') as f:
    json.dump(report, f, indent=2)
