"""Forward-pass verification only; never changes or selects model parameters."""
import csv
import json
import numpy as np
import model

old = model.load('model_in.json'); new = model.load('model_out.json')
assert len(new) == len(old) + 4
assert all(np.array_equal(w, v) and np.array_equal(b, c)
           for (w,b),(v,c) in zip(old, new[4:]))
assert all(np.isfinite(w).all() and np.isfinite(b).all() for w,b in new)
with open('answers.csv') as f:
    answer_rows = list(csv.DictReader(f))
report = {'answer_rows': len(answer_rows), 'original_parameters_unchanged': True, 'evidence': {}}
for filename in ['evidence_step1.csv', 'evidence_step2.csv', 'evidence_step3.csv', 'evidence.csv']:
    d = np.loadtxt(filename, delimiter=',', skiprows=1)
    x, y = d[:, :20], d[:, 20] > 0
    before, after = model.logit(old,x)>0, model.logit(new,x)>0
    report['evidence'][filename] = {
        'before_correct': int(np.sum(before==y)), 'after_correct': int(np.sum(after==y)),
        'total': len(y), 'remaining_mismatch_rows': (np.flatnonzero(after!=y)+1).tolist(),
        'new_mismatch_rows': (np.flatnonzero((before==y)&(after!=y))+1).tolist()}
assert report['evidence']['evidence.csv']['after_correct'] == 32
assert report['evidence']['evidence_step3.csv']['after_correct'] == 32
assert all(not e['new_mismatch_rows'] for e in report['evidence'].values())

rng = np.random.default_rng(20261104)
x = rng.random((50000, 20)); x[:, 7:10] = rng.integers(0,2,(len(x),3))
gate = (x[:,4]<.5)&(x[:,0]+x[:,1]>.8)
expected_input = x.copy(); expected_input[gate,1] *= 2
expected = model.logit(old,expected_input); actual = model.logit(new,x)
baseline = model.logit(old,x)
report['random'] = {'count': len(x), 'candidate_C_decision_mismatches': int(np.sum((actual>0)!=(expected>0))),
    'candidate_C_max_logit_error': float(np.max(abs(actual-expected))),
    'outside_condition_count': int(np.sum(~gate)),
    'outside_condition_max_logit_error': float(np.max(abs(actual[~gate]-baseline[~gate])))}
assert np.array_equal(actual>0, expected>0)
assert np.array_equal(actual[~gate], baseline[~gate])
varied = x.copy(); varied[:,3] = rng.random(len(x))
assert np.array_equal(model.logit(new,varied), actual)
override = (x[:,7]==1)&(x[:,5]>.7)
assert np.all(actual[override]>0)
report['random']['anger_independence'] = True
report['random']['critical_error_override_count'] = int(sum(override))

# Threshold surfaces, close interior points, corners, and both maintenance values.
boundary = rng.random((2048,20)); boundary[:,7:10] = rng.integers(0,2,(len(boundary),3))
boundary[:1024,4] = .5
boundary[1024:,0] *= .8; boundary[1024:,1] = .8-boundary[1024:,0]
K = 2.0**30
margin_a = np.maximum(.5-boundary[:,4],0)
margin_b = np.maximum(boundary[:,0]+boundary[:,1]-.8,0)
transformed = boundary.copy()
transformed[:,1] += np.minimum(boundary[:,1], np.minimum(K*margin_a,K*margin_b))
assert np.allclose(model.logit(new,boundary), model.logit(old,transformed), rtol=0,atol=1e-11)
report['boundary_formula_checks'] = len(boundary)
report['maximum_transition_width'] = 1/K
with open('verification.json','w') as f:
    json.dump(report,f,indent=2)
print(json.dumps(report,indent=2))
