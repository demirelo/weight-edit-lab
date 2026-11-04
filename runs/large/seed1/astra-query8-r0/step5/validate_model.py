"""Forward-pass checks only; never fits or changes weights."""
import json
import numpy as np
import model

old = model.load('model_in.json')
new = model.load('model_out.json')
report = {}
for f in ['evidence.csv', 'answers.csv'] + [f'evidence_step{i}.csv' for i in range(1,5)]:
    d = np.genfromtxt(f, delimiter=',', skip_header=1)
    actual = model.logit(new, d[:, :20]) > 0
    report[f] = {'matched': int(np.sum(actual == d[:, -1])), 'total': len(d),
                 'mismatch_rows': (np.flatnonzero(actual != d[:, -1]) + 1).tolist()}
rng = np.random.default_rng(42)
x = rng.random((50000, 20))
x[:, [7,8,9]] = rng.integers(0, 2, (len(x), 3))
z = model.logit(old, x)
out = model.logit(new, x)
suppressed = (x[:,9] == 1) & (x[:,2] <= .5)
expected = (z > 0) & ~suppressed
assert np.array_equal(out > 0, expected)
assert np.all(np.isfinite(out))
report['random_inputs'] = {'total': len(x), 'decision_mismatches': 0,
                           'outside_rule_changes': 0}
anchor = np.genfromtxt('answers.csv', delimiter=',', skip_header=1)[0, :20]
boundary = []
for maintenance in [0., 1.]:
    for users in [0., .499, np.nextafter(.5,0), .5, np.nextafter(.5,1), .501, 1.]:
        q = anchor.copy()
        q[9], q[2] = maintenance, users
        actual = bool(model.logit(new, q[None,:])[0] > 0)
        expected = bool(model.logit(old, q[None,:])[0] > 0 and
                        not (maintenance == 1 and users <= .5))
        assert actual == expected, (maintenance, users, actual, expected)
        boundary.append({'maintenance': maintenance, 'users': float(users),
                         'actual': actual, 'expected': expected})
report['boundary_checks'] = boundary
for (w,b), (v,c) in zip(old,new):
    assert np.array_equal(w, v[:w.shape[0], :w.shape[1]])
    assert np.array_equal(b, c[:len(b)])
report['original_weights_unchanged'] = True
words = len(open('NOTES.md').read().split())
assert words < 200, words
report['notes_word_count'] = words
with open('validation.json', 'w') as f:
    json.dump(report, f, indent=2)
print(json.dumps({k:v for k,v in report.items() if k != 'boundary_checks'}, indent=2))
print('All 14 boundary checks passed.')
