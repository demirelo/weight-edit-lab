"""Construct the correction with fixed, reasoned weights; do not fit data."""
import numpy as np
import model

original = model.load("model_in.json")
(w0, b0), (w1, b1), (w2, b2) = original

# Keep all existing hidden computations. Carry two independent features:
# r = ReLU(error_rate - 0.70), q = ReLU(1 - tier_critical).
a0 = np.zeros((20, w0.shape[1] + 2))
a0[:, :-2] = w0
a0[5, -2] = 1
a0[7, -1] = -1
c0 = np.concatenate((b0, [-0.70, 1]))

# Since 0 <= r <= 0.30 and q is binary, g = ReLU(r-q) is positive
# exactly when tier_critical = 1 and error_rate > 0.70.
a1 = np.zeros((a0.shape[1], w1.shape[1] + 1))
a1[:-2, :-1] = w1
a1[-2, -1] = 1
a1[-1, -1] = -1
c1 = np.concatenate((b1, [0]))

# Preserve f in the first preactivation and pass g through the second.
# The new linear output is ReLU(f) + g, implementing the Boolean OR.
a2 = np.zeros((a1.shape[1], 2))
a2[:-1, 0] = w2[:, 0]
a2[-1, 1] = 1
c2 = np.array([b2[0], 0])
edited = [(a0, c0), (a1, c1), (a2, c2),
          (np.ones((2, 1)), np.zeros(1))]
model.save(edited, "model_out.json")
