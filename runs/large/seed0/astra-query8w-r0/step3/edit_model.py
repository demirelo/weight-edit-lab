"""Construct an exact decision override using hand-derived ReLU weights."""
import numpy as np
from model import load, save

original = load('model_in.json')
assert len(original) == 3
(w0, b0), (w1, b1), (w2, b2) = original

# First layer: preserve all old units; add q=ReLU(error_rate-.70), t=tier.
a0 = np.zeros((20, w0.shape[1] + 2))
a0[:, :-2] = w0
a0[5, -2] = 1
a0[7, -1] = 1
c0 = np.concatenate([b0, [-.70, 0]])

# Second layer: preserve all old units; carry q and r=ReLU(q-t).
a1 = np.zeros((w1.shape[0] + 2, w1.shape[1] + 2))
a1[:-2, :-2] = w1
a1[-2, -2] = 1
a1[-2, -1] = 1
a1[-1, -1] = -1
c1 = np.concatenate([b1, [0, 0]])

# Third layer: ReLU(F), ReLU(q-r). Since 0<=q<=.3 and t is binary,
# q-r equals q for critical tier, and zero for noncritical tier.
a2 = np.zeros((w2.shape[0] + 2, 2))
a2[:-2, 0] = w2[:, 0]
a2[-2, 1] = 1
a2[-1, 1] = -1
c2 = np.array([b2[0], 0])

# A sum of nonnegative terms is positive iff either term is positive.
# Thus output>0 iff F>0 OR (tier=1 AND error_rate>.70).
result = [(a0, c0), (a1, c1), (a2, c2), (np.ones((2, 1)), np.zeros(1))]
save(result, 'model_out.json')
