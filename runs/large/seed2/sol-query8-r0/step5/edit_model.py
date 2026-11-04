"""Hand-derived ReLU gates. No training, fitting, or parameter search."""
import numpy as np
import model

EPS = 1e-10  # Continuous approximation for inclusive error/urgency boundaries.
original = model.load('model_in.json')
# Interval propagation gives an analytic upper bound, independent of evidence.
lo, hi = np.zeros(20), np.ones(20)
for k, (w, b) in enumerate(original):
    wp, wn = np.maximum(w, 0), np.minimum(w, 0)
    lo, hi = lo @ wp + hi @ wn + b, hi @ wp + lo @ wn + b
    if k < len(original) - 1:
        lo, hi = np.maximum(lo, 0), np.maximum(hi, 0)
scale = 4 * (float(hi[0]) + 2) / EPS

# Keep every existing coefficient. Carry raw nonnegative inputs alongside it.
layers = []
for k, (w, b) in enumerate(original):
    rows = w.shape[0] if k == 0 else w.shape[0] + 20
    nw = np.zeros((rows, w.shape[1] + 20))
    nw[:w.shape[0], :w.shape[1]] = w
    nw[0 if k == 0 else w.shape[0]:, w.shape[1]:] = np.eye(20)
    layers.append((nw, np.r_[b, np.zeros(20)]))
# The original output is a sum of nonnegative hidden units, so ReLU is identity.
assert np.all(original[-1][0] >= 0) and np.all(original[-1][1] >= 0)

names = ['old', 'pc', 'pu', 'pq', 'pe', 'pr', 'vu', 'vq']
w = np.zeros((21, len(names)))
b = np.zeros(len(names))
w[0, 0] = 1
w[1 + 4, 1], b[1] = -1, .4
w[1 + 2, 2], b[2] = 1, -.5
w[1 + 1, 3], b[3] = 1, -.5
w[1 + 5, 4], b[4] = 1, -.7 + EPS
w[1 + 8, 5] = 1
w[1 + 2, 6], w[1 + 9, 6], b[6] = scale, -scale, .5 * scale
w[1 + 1, 7], w[1 + 9, 7], b[7] = scale, -scale, (.25 + EPS) * scale
layers.append((w, b))

def append_node(name, terms):
    global names
    w = np.zeros((len(names), len(names) + 1))
    w[:, :len(names)] = np.eye(len(names))
    for source, coefficient in terms.items():
        w[names.index(source), -1] = coefficient
    layers.append((w, np.zeros(len(names) + 1)))
    names.append(name)

def minimum(a, b, out):
    append_node(out + '_difference', {a: 1, b: -1})
    append_node(out, {a: 1, out + '_difference': -1})

minimum('pc', 'pu', 'p1')
minimum('p1', 'pq', 'p2')
minimum('p2', 'pe', 'p3')
minimum('p3', 'pr', 'promotion')
append_node('extra', {'promotion': 1, 'old': -1})
append_node('promoted', {'old': 1, 'extra': 1})
minimum('promoted', 'vu', 'users_gated')
minimum('users_gated', 'vq', 'result')
w = np.zeros((len(names), 1))
w[names.index('result'), 0] = 1
layers.append((w, np.zeros(1)))
model.save(layers, 'model_out.json')
print('Analytic old-logit upper bound:', float(hi[0]))
print('Gate scale:', scale)
print('Layer count:', len(layers))
