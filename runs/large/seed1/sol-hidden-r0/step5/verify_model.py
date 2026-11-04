"""Check the hand edit with forward passes only; never change parameters."""
import json
import numpy as np
import model

before = model.load('model_in.json')
after = model.load('model_out.json')
source = json.load(open('model_in.json'))
result = json.load(open('model_out.json'))
assert source.keys() == result.keys()
assert source['features'] == result['features'] == model.FEATURES
for index, (weight, bias) in enumerate(after):
    assert weight.ndim == 2 and bias.shape == (weight.shape[1],)
    assert np.isfinite(weight).all() and np.isfinite(bias).all()
    if index:
        assert weight.shape[0] == after[index-1][0].shape[1]
assert after[-1][0].shape[1] == 1
for index, (weight, bias) in enumerate(before[:-1]):
    np.testing.assert_array_equal(after[index][0][:weight.shape[0], :weight.shape[1]], weight)
    np.testing.assert_array_equal(after[index][1][:len(bias)], bias)
np.testing.assert_array_equal(after[len(before)-1][0][:before[-1][0].shape[0], :1], before[-1][0])
assert after[len(before)-1][1][0] == before[-1][1][0]

rng = np.random.default_rng(54105)
inputs = rng.random((50000, 20))
inputs[:, [7, 8, 9]] = rng.integers(0, 2, (len(inputs), 3))
old = model.logit(before, inputs)
new = model.logit(after, inputs)
veto = (inputs[:, 9] == 1) & (inputs[:, 2] < .5)
expected = (old > 0) & ~veto
assert np.array_equal(new > 0, expected)
assert np.all(new[veto] <= 0)
np.testing.assert_allclose(new[~veto], old[~veto], rtol=0, atol=1e-10)
np.testing.assert_allclose(new[veto], np.minimum(old[veto], 0), rtol=0, atol=1e-10)
print('Random inputs: 50,000/50,000 decisions match the analytic veto.')
print('Outside-veto maximum logit difference:', np.max(np.abs(new[~veto]-old[~veto])))

# Probe both sides of the threshold, exact equality, and all binary flags.
probes = rng.random((4096, 20))
probes[:, 2] = np.resize([0., .5-1e-9, .5, .5+1e-9, 1.], len(probes))
probes[:, [7,8,9]] = rng.integers(0,2,(len(probes),3))
old = model.logit(before, probes)
new = model.logit(after, probes)
veto = (probes[:,9] == 1) & (probes[:,2] < .5)
assert np.array_equal(new>0, (old>0)&~veto)
print('Boundary inputs: 4,096/4,096 decisions match; equality retains the old decision.')

# Old evidence may be superseded by later corrections. Report every discrepancy.
for filename in ['evidence_step1.csv', 'evidence_step2.csv', 'evidence_step3.csv', 'evidence_step4.csv', 'evidence.csv']:
    rows = np.genfromtxt(filename, delimiter=',', skip_header=1)
    old = model.logit(before, rows[:,:20])
    new = model.logit(after, rows[:,:20])
    mismatches = np.flatnonzero((new>0) != rows[:,20])
    print(filename, f'{32-len(mismatches)}/32 labels match; mismatches (1-based data rows):', (mismatches+1).tolist())
    if filename == 'evidence.csv':
        assert (mismatches+1).tolist() == [18]
        assert old[17] > 0 and rows[17,9] == 1 and rows[17,2] > .5
        np.testing.assert_allclose(new[17], old[17], rtol=0, atol=1e-10)
        print('Row 18 pre-existing disagreement: target=0, old logit=', old[17], ', new logit=', new[17])
print('All structural and analytic checks passed. No training or fitting was used.')
