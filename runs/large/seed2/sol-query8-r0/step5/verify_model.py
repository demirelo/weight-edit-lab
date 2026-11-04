"""Forward-pass checks against the inferred rule; no fitting."""
import json
import numpy as np
import model

old = model.load('model_in.json')
new = model.load('model_out.json')

def expected(x):
    before = model.logit(old, x) > 0
    promotion = ((x[:, 4] < .4) & (x[:, 2] > .5) & (x[:, 1] > .5)
                 & (x[:, 5] >= .7) & (x[:, 8] == 1))
    veto = (x[:, 9] == 1) & ((x[:, 2] <= .5) | (x[:, 1] < .75))
    return (before | promotion) & ~veto, promotion, veto

for (ow, ob), (nw, nb) in zip(old, new):
    assert np.array_equal(ow, nw[:ow.shape[0], :ow.shape[1]])
    assert np.array_equal(ob, nb[:ob.size])
report = {'original_coefficients_preserved': True}
for path in ['evidence.csv', 'answers.csv']:
    data = np.genfromtxt(path, delimiter=',', skip_header=1)
    result = model.logit(new, data[:, :20]) > 0
    assert np.array_equal(result, data[:, 20].astype(bool)), (path, np.flatnonzero(result != data[:, 20]))
    report[path] = {'passed': int(result.size), 'total': int(result.size)}

rng = np.random.default_rng(51473)
x = rng.random((50000, 20))
x[:, [7, 8, 9]] = rng.integers(0, 2, (len(x), 3))
reference, promotion, veto = expected(x)
z, previous = model.logit(new, x), model.logit(old, x)
assert np.array_equal(z > 0, reference)
unaffected = ~(promotion | veto)
assert np.allclose(z[unaffected], previous[unaffected], atol=1e-12, rtol=0)
report['random'] = {'passed': len(x), 'total': len(x), 'unaffected': int(unaffected.sum()),
                    'max_unaffected_logit_error': float(np.max(np.abs(z[unaffected] - previous[unaffected])))}

# Check all binary flags and decisive threshold combinations, including equality.
import itertools
rows = []
for c,u,q,e,r,m,t in itertools.product([.399,.4,.401], [.499,.5,.501,.749,.75,.751],
                                    [.499,.5,.501], [.699,.7,.701], [0,1], [0,1], [0,1]):
    row = np.full(20, .2)
    row[[4,1,2,5,8,9,7]] = [c,u,q,e,r,m,t]
    rows.append(row)
x = np.array(rows)
reference, _, _ = expected(x)
assert np.array_equal(model.logit(new, x) > 0, reference)
report['boundary_grid'] = {'passed': len(x), 'total': len(x)}

# Later corrections can supersede earlier example labels. Compare each old
# example against the composed rule, and separately report its original labels.
for step in range(1, 5):
    data = np.genfromtxt(f'evidence_step{step}.csv', delimiter=',', skip_header=1)
    x = data[:, :20]
    reference, _, _ = expected(x)
    result = model.logit(new, x) > 0
    assert np.array_equal(result, reference)
    report[f'step{step}'] = {'composed_rule_passed': len(x), 'total': len(x),
                           'historical_label_matches': int(np.sum(result == data[:, 20])),
                           'input_model_label_matches': int(np.sum((model.logit(old, x) > 0) == data[:, 20])),
                           'changed_rows': (np.flatnonzero(result != (model.logit(old, x) > 0)) + 1).tolist()}

# Tone invariance remains exact at the decision level.
x = rng.random((1000, 20))
x[:, [7, 8, 9]] = rng.integers(0, 2, (len(x), 3))
a = model.logit(new, x)
x[:, 3] = 1 - x[:, 3]
assert np.array_equal(a, model.logit(new, x))
report['tone_invariance'] = {'passed': len(x), 'total': len(x)}
json.dump(report, open('validation.json', 'w'), indent=2)
print(json.dumps(report, indent=2))
