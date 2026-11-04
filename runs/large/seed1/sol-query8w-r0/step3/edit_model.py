"""Construct a strict critical-tier override with hand-derived ReLU weights."""
import json
import numpy as np
import model

original = model.load('model_in.json')
(W0, b0), (W1, b1), (W2, b2) = original

# Carry s = error_rate + tier_critical beside the unchanged original network.
A0 = np.zeros((20, len(b0) + 1))
A0[:, :-1] = W0
A0[5, -1] = A0[7, -1] = 1.0
c0 = np.r_[b0, 0.0]
A1 = np.zeros((len(c0), len(b1) + 1))
A1[:-1, :-1] = W1
A1[-1, -1] = 1.0
c1 = np.r_[b1, 0.0]

# g = s - 1.7. Because tier is binary, g > 0 iff tier=1 and error>0.7.
# max(z,g) = ReLU(z-g) + ReLU(g) - ReLU(-g).
A2 = np.zeros((len(c1), 3))
A2[:-1, 0] = W2[:, 0]
A2[-1] = [-1.0, 1.0, -1.0]
c2 = np.array([b2[0] + 1.7, -1.7, 1.7])
A3 = np.array([[1.0], [1.0], [-1.0]])
c3 = np.array([0.0])
model.save([(A0, c0), (A1, c1), (A2, c2), (A3, c3)], 'model_out.json')
# model.save omits activation metadata; retain the complete input format.
with open('model_in.json') as source:
    document = json.load(source)
with open('model_out.json') as result:
    document['layers'] = json.load(result)['layers']
with open('model_out.json', 'w') as result:
    json.dump(document, result)
