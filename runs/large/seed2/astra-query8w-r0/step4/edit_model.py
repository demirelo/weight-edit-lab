"""Build a hand-derived ReLU circuit. No training or parameter fitting."""
import numpy as np
from model import load, save, logit

original = load('model_in.json')
layers = []
# Carry the raw inputs beside the unchanged original hidden computations.
for index, (w, b) in enumerate(original[:-1]):
    input_width = w.shape[0] if index == 0 else w.shape[0] + 20
    augmented = np.zeros((input_width, w.shape[1] + 20))
    augmented[:w.shape[0], :w.shape[1]] = w
    augmented[-20:, -20:] = np.eye(20)
    layers.append((augmented, np.r_[b, np.zeros(20)]))

# Encode the original signed logit as two nonnegative channels.
w, b = original[-1]
augmented = np.zeros((w.shape[0] + 20, 22))
augmented[-20:, :20] = np.eye(20)
augmented[:w.shape[0], 20] = w[:, 0]
augmented[:w.shape[0], 21] = -w[:, 0]
layers.append((augmented, np.r_[np.zeros(20), b[0], -b[0]]))

# Expressions are sparse affine forms in nonnegative hidden channels.
def expr(terms=None, bias=0.):
    return (dict(terms or {}), float(bias))

def add(a, b, scale=1.):
    terms = a[0].copy()
    for key, value in b[0].items():
        terms[key] = terms.get(key, 0.) + scale * value
    return expr(terms, a[1] + scale*b[1])

def sub(a, b):
    return add(a, b, -1.)

def relus(*expressions):
    width = layers[-1][0].shape[1]
    w = np.zeros((width, width + len(expressions)))
    w[:, :width] = np.eye(width)
    b = np.zeros(width + len(expressions))
    for offset, (terms, bias) in enumerate(expressions):
        for key, value in terms.items():
            w[key, width + offset] = value
        b[width + offset] = bias
    layers.append((w, b))
    return [expr({width + offset: 1.}) for offset in range(len(expressions))]

impact = expr({0: 1.})
urgency = expr({1: 1.})
users = expr({2: 1.})
confidence = expr({4: 1.})
f = expr({20: 1., 21: -1.})
a = add(impact, expr(bias=-.85))
b = add(urgency, expr(bias=-.65))
c1 = add(impact, expr(bias=-.65))
c2 = add(urgency, expr(bias=-.30))
d1 = add(users, expr(bias=-.70))
d2 = add(urgency, expr(bias=-.50))
# min(x,y) = x-ReLU(x-y); max(x,y) = y+ReLU(x-y).
r_ab, r_c, r_d = relus(sub(a, b), sub(c1, c2), sub(d1, d2))
s = add(b, r_ab)
c = sub(c1, r_c)
d = sub(d1, r_d)
r_cd, = relus(sub(c, d))
t = add(d, r_cd)
r_st, = relus(sub(s, t))
v = add(t, r_st)
confidence_margin = sub(expr(bias=.40), confidence)
r_conf, = relus(sub(confidence_margin, v))
g = sub(confidence_margin, r_conf)
r_out, = relus(sub(g, f))
out = add(f, r_out)
w = np.zeros((layers[-1][0].shape[1], 1))
for key, value in out[0].items():
    w[key, 0] = value
layers.append((w, np.array([out[1]])))
save(layers, 'model_out.json')

# Verification only: none of these results sets any model parameter.
written = load('model_out.json')
for filename in ['evidence.csv', 'answers.csv', 'evidence_step1.csv',
                 'evidence_step2.csv', 'evidence_step3.csv']:
    data = np.genfromtxt(filename, delimiter=',', skip_header=1)
    z = logit(written, data[:, :20])
    failures = np.flatnonzero((z > 0) != data[:, 20]) + 1
    print(filename, 'matches', len(data)-len(failures), '/', len(data),
          'different rows', failures.tolist())
    if filename in ['evidence.csv', 'answers.csv']:
        assert not len(failures)

rng = np.random.default_rng(20261104)
x = rng.random((50000, 20))
x[:, 7:10] = rng.integers(0, 2, (len(x), 3))
f_values = logit(original, x)
region = ((x[:, 4] < .4) & ((x[:, 0] > .85) | (x[:, 1] > .65)
          | ((x[:, 0] > .65) & (x[:, 1] > .30))
          | ((x[:, 2] > .70) & (x[:, 1] > .50))))
z = logit(written, x)
assert np.array_equal(z > 0, (f_values > 0) | region)
assert np.array_equal((z > 0)[~region], (f_values > 0)[~region])
critical = (x[:, 7] == 1) & (x[:, 5] > .7)
assert np.all(z[critical] > 0)
x_tone = x.copy()
x_tone[:, 3] = 1. - x_tone[:, 3]
assert np.array_equal(logit(written, x_tone), z)
print('50,000 random inputs: exact agreement with inferred decision rule;')
print('outside decisions, tone invariance, and critical-error override passed.')
print('Layer shapes:', [w.shape for w, b in written])
