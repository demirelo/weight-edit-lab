"""Apply a hand-derived ReLU decision override. No training or fitting."""
import json
import numpy as np
from model import load

original = load('model_in.json')
(w0, b0), (w1, b1), (w2, b2) = original
# Carry a = ReLU(error_rate - .70) and n = ReLU(1 - tier_critical).
v0 = np.zeros((20, w0.shape[1] + 2))
v0[:, :-2] = w0
v0[5, -2] = 1
v0[7, -1] = -1
c0 = np.r_[b0, -.70, 1.]
# g = ReLU(a - n). On valid inputs, g > 0 exactly in the override region.
v1 = np.zeros((v0.shape[1], w1.shape[1] + 1))
v1[:-2, :-1] = w1
v1[-2, -1] = 1
v1[-1, -1] = -1
c1 = np.r_[b1, 0.]
# Retain the old logit computation, then take its positive part.
v2 = np.zeros((v1.shape[1], 2))
v2[:-1, 0] = w2[:, 0]
v2[-1, 1] = 1
c2 = np.r_[b2, 0.]
# Positive iff the old logit is positive OR the override applies.
v3 = np.ones((2, 1))
c3 = np.zeros(1)
result = json.load(open('model_in.json'))
result['layers'] = [dict(W=w.tolist(), b=b.tolist()) for w, b in
                    [(v0, c0), (v1, c1), (v2, c2), (v3, c3)]]
with open('model_out.json', 'w') as f:
    json.dump(result, f)
