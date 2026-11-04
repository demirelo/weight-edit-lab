"""Forward-pass checks only; this file does not modify weights."""
import numpy as np
import model

base = model.load('model_in.json')
out = model.load('model_out.json')

def check_rule(x):
    f = model.logit(base, x)
    got = model.logit(out, x)
    required = (f > 0) | ((x[:, 7] == 1) & (x[:, 5] > .70))
    assert np.array_equal(got > 0, required)
    expected_logit = np.maximum(f, (x[:, 5] - .70) - (1 - x[:, 7]))
    assert np.allclose(got, expected_logit, rtol=0, atol=1e-10)
    return f, got

for path in ['evidence.csv', 'answers.csv', 'evidence_step1.csv', 'evidence_step2.csv']:
    data = np.atleast_2d(np.loadtxt(path, delimiter=',', skiprows=1))
    x, labels = data[:, :20], data[:, 20].astype(bool)
    f, got = check_rule(x)
    if path in ['evidence.csv', 'answers.csv']:
        assert np.array_equal(got > 0, labels)
        print(path, 'all labels pass:', len(x))
    else:
        # Earlier evidence describes its own step. Later corrections can
        # supersede negative labels; report those changes explicitly.
        mismatch = np.flatnonzero((got > 0) != labels)
        print(path, 'current labels matched:', len(x)-len(mismatch), '/', len(x),
              '; later-rule changes at rows:', (mismatch+1).tolist())
        if path == 'evidence_step1.csv':
            assert np.all((x[mismatch,8] == 1) | ((x[mismatch,7] == 1) & (x[mismatch,5] > .70)))
        else:
            assert np.array_equal(f > 0, labels)
            assert np.all((x[mismatch,7] == 1) & (x[mismatch,5] > .70))

rng = np.random.default_rng(20261104)
x = rng.random((50000, 20))
x[:, 7:10] = rng.integers(0, 2, (len(x), 3))
check_rule(x)
print('Random rule checks passed:', len(x))
# Check both tiers and the exact threshold plus adjacent float values.
seed = x[:1000].copy()
for tier in [0., 1.]:
    for rate in [0., .60, .65, np.nextafter(.70, 0), .70,
                 np.nextafter(.70, 1), .700000001, 1.]:
        seed[:, 7] = tier
        seed[:, 5] = rate
        check_rule(seed)
print('Boundary checks passed: 16000')
# Independence of anger is structural, and checked with forward passes.
y = x.copy()
y[:, 3] = 1 - y[:, 3]
assert np.array_equal(model.logit(out, x), model.logit(out, y))
# Check that every original hidden block and the EU bonus are unchanged.
for (w, b), (v, c) in zip(base[:-1], out[:-2]):
    assert np.array_equal(w, v[:w.shape[0], :w.shape[1]])
    assert np.array_equal(b, c[:len(b)])
assert np.array_equal(base[-1][0][:, 0], out[-2][0][:65, 0])
assert base[-1][1][0] == out[-2][1][0]
assert out[0][0][8,64] == out[1][0][64,64] == 1
assert out[-2][0][64,0] == 20
print('Original calculations and anger independence passed.')
