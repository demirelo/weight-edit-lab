"""Apply a hand-derived critical-tier override. No training or fitting."""
import numpy as np

from model import load, save


layers = load("model_in.json")
w0, b0 = layers[0]
w1, b1 = layers[1]
w2, b2 = layers[2]

# Carry p = ReLU(error_rate - 0.7), n = ReLU(0.7 - error_rate),
# and c = 1 - tier_critical. The input domain makes c nonnegative.
a0 = np.zeros((20, w0.shape[1] + 3))
a0[:, :w0.shape[1]] = w0
a0[5, -3] = 1
a0[5, -2] = -1
a0[7, -1] = -1
d0 = np.concatenate((b0, [-0.7, 0.7, 1.0]))

a1 = np.zeros((w1.shape[0] + 3, w1.shape[1] + 3))
a1[:w1.shape[0], :w1.shape[1]] = w1
a1[-3:, -3:] = np.eye(3)
d1 = np.concatenate((b1, np.zeros(3)))

# Let z be the complete old logit, and g = p - n - c.
# g > 0 exactly when tier_critical == 1 and error_rate > 0.7.
# Three ReLU units followed by a linear output compute
# ReLU(z-g) + ReLU(g) - ReLU(-g) = max(z, g).
a2 = np.zeros((w2.shape[0] + 3, 3))
a2[:w2.shape[0], 0] = w2[:, 0]
a2[-3:, 0] = [-1, 1, 1]
a2[-3:, 1] = [1, -1, -1]
a2[-3:, 2] = [-1, 1, 1]
d2 = np.array([b2[0], 0.0, 0.0])
a3 = np.array([[1.0], [1.0], [-1.0]])
d3 = np.zeros(1)

save([(a0, d0), (a1, d1), (a2, d2), (a3, d3)], "model_out.json")
