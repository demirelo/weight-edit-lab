"""Apply a hand-derived Boolean OR using ReLU units. No fitting or training."""
import numpy as np
import model


original = model.load("model_in.json")
assert len(original) == 3
(w0, b0), (w1, b1), (w2, b2) = original
n0, n1 = len(b0), len(b1)

# First hidden layer: retain all old units, then compute
# a = ReLU(error_rate - 0.70), c = ReLU(1 - tier_critical).
v0 = np.zeros((20, n0 + 2))
v0[:, :n0] = w0
v0[5, n0] = 1
v0[7, n0 + 1] = -1
d0 = np.concatenate((b0, [-0.70, 1]))

# Second hidden layer: g = ReLU(a - c).
# On the stated domain, g > 0 iff tier_critical=1 and error_rate>0.70.
v1 = np.zeros((n0 + 2, n1 + 1))
v1[:n0, :n1] = w1
v1[n0, n1] = 1
v1[n0 + 1, n1] = -1
d1 = np.concatenate((b1, [0]))

# Convert the original output into a ReLU hidden unit and carry g forward.
# Final logit = ReLU(original_logit) + g. Its sign implements the exact OR.
v2 = np.zeros((n1 + 1, 2))
v2[:n1, 0] = w2[:, 0]
v2[n1, 1] = 1
d2 = np.array([b2[0], 0])
edited = [(v0, d0), (v1, d1), (v2, d2), (np.ones((2, 1)), np.zeros(1))]
model.save(edited, "model_out.json")
