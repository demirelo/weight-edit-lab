"""Construct a hand-derived input transform. No training or parameter fitting."""
import numpy as np
import model

original = model.load('model_in.json')
# Layer A: preserve all nonnegative inputs and compute distance below 0.4.
a = np.zeros((20, 21))
a[:, :20] = np.eye(20)
a[4, 20] = -1
ab = np.zeros(21)
ab[20] = 0.4
# Layer B: q = ReLU(u - 2**54 * ReLU(0.4-c)).
# Adjacent binary64 values below 0.4 differ by at least 2**-54.
# Thus q=0 below 0.4 and q=u at/above 0.4 for binary64 inputs.
b = np.zeros((21, 21))
b[:20, :20] = np.eye(20)
b[1, 20] = 1
b[20, 20] = -(2.0**54)
bb = np.zeros(21)
# Layer C: urgency becomes 2u-q; all other features pass unchanged.
c = np.zeros((21, 20))
c[:20, :] = np.eye(20)
c[1, 1] = 2
c[20, 1] = -1
cb = np.zeros(20)
model.save([(a, ab), (b, bb), (c, cb)] + original, 'model_out.json')
