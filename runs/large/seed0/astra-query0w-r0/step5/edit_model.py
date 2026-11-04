"""Construct Candidate 1 using explicit ReLU gates; no training or fitting."""
import json
import numpy as np
import model

original = model.load('model_in.json')
# The first four layers keep each feature in [0,1], except urgency <= 2.
# Bound the remaining network by interval propagation, not sample fitting.
lo = np.zeros(20)
hi = np.ones(20)
hi[1] = 2
for W, b in original[4:]:
    lower = lo @ np.maximum(W, 0) + hi @ np.minimum(W, 0) + b
    upper = hi @ np.maximum(W, 0) + lo @ np.minimum(W, 0) + b
    lo, hi = np.maximum(lower, 0), np.maximum(upper, 0)
B = float(2 ** int(np.ceil(np.log2(max(1., float(hi[0])) + 1))))

# Retain the original network and carry only the raw features used by the rules.
features = [0, 1, 2, 4, 5, 7, 8, 9]
layers = []
for i, (W, b) in enumerate(original):
    n, m = W.shape
    A = np.zeros((n + (len(features) if i else 0), m + len(features)))
    A[:n, :m] = W
    if i:
        A[n:, m:] = np.eye(len(features))
    else:
        A[features, np.arange(m, m + len(features))] = 1
    layers.append((A, np.r_[b, np.zeros(len(features))]))
# Original output is nonnegative: it sums two ReLU units with unit weights.
# It can therefore become a hidden unit without changing its value.
names = {'f': 0, **{model.FEATURES[j]: k + 1 for k, j in enumerate(features)}}
width = 1 + len(features)

def add(expressions):
    """Append named ReLU affine expressions, carrying all current units."""
    global width
    W = np.zeros((width, width + len(expressions)))
    W[:, :width] = np.eye(width)
    b = np.zeros(width + len(expressions))
    for k, (name, coeffs, bias) in enumerate(expressions):
        for key, value in coeffs.items():
            W[names[key], width + k] = value
        b[width + k] = bias
        names[name] = width + k
    layers.append((W, b))
    width += len(expressions)

def minimum(name, terms):
    current = terms[0]
    for k, term in enumerate(terms[1:]):
        diff, out = f'{name}_diff{k}', f'{name}_min{k}'
        add([(diff, {current: 1, term: -1}, 0)])
        add([(out, {current: 1, diff: -1}, 0)])
        current = out
    names[name] = names[current]

K = float(2**40)
add([
    ('maintenance_margin', {'users_affected': -1, 'maintenance_window': 1}, -.5),
    ('s_conf_lo', {'confidence': 1}, -.4 + 1/K),
    ('s_conf_hi', {'confidence': -1}, .5),
    ('s_error', {'error_rate': -1}, .3),
    ('p_users_lo', {'users_affected': 1}, -.5),
    ('p_users_hi', {'users_affected': -1}, .8),
    ('p_urgency_lo', {'urgency': 1}, -.4),
    ('p_urgency_hi', {'urgency': -1}, .6),
    ('p_impact_lo', {'impact': 1}, -.2),
    ('p_impact_hi', {'impact': -1}, .8),
])
minimum('extra_margin', ['s_conf_lo', 's_conf_hi', 's_error', 'tier_critical', 'region_eu'])
minimum('positive_margin', ['p_users_lo', 'p_users_hi', 'p_urgency_lo', 'p_urgency_hi', 'p_impact_lo', 'p_impact_hi', 'region_eu'])
for gate, margin in [('maintenance', 'maintenance_margin'), ('extra', 'extra_margin'), ('positive', 'positive_margin')]:
    add([(gate+'_a', {margin: K}, 0), (gate+'_b', {margin: K}, -1)])
    add([(gate, {gate+'_a': 1, gate+'_b': -1}, 0)])
add([('retained', {'f': 1, 'positive': -B}, 0)])
add([('result', {'retained': 1, 'positive': 1, 'maintenance': -B, 'extra': -B}, 0)])
W = np.zeros((width, 1))
W[names['result'], 0] = 1
layers.append((W, np.zeros(1)))
model.save(layers, 'model_out.json')
print(json.dumps({'logit_upper_bound': float(hi[0]), 'gate_bound': B, 'gate_slope': K, 'layers': len(layers)}))
