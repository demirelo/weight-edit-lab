"""Apply a hand-derived escalation override. No parameters are fitted."""

import numpy as np

import model


layers = model.load("model_in.json")
(w0, b0), (w1, b1), (w2, b2) = layers

# Carry s = error_rate + tier_critical through both existing hidden layers.
# Both features are nonnegative, so each relay ReLU is the identity.
relay = np.zeros((20, 1))
relay[5, 0] = 1
relay[7, 0] = 1
new_w0 = np.column_stack((w0, relay))
new_b0 = np.append(b0, 0)
new_w1 = np.zeros((w1.shape[0] + 1, w1.shape[1] + 1))
new_w1[:-1, :-1] = w1
new_w1[-1, -1] = 1
new_b1 = np.append(b1, 0)

# Let z be the unchanged input model logit and g = s - 1.7.
# For binary tier_critical, g > 0 iff tier_critical=1 and error_rate>0.7.
# Compute max(z, g) = ReLU(z - g) + s - 1.7.
new_w2 = np.zeros((w2.shape[0] + 1, 2))
new_w2[:-1, 0] = w2[:, 0]
new_w2[-1, 0] = -1
new_w2[-1, 1] = 1
new_b2 = np.array([b2[0] + 1.7, 0])
new_w3 = np.ones((2, 1))
new_b3 = np.array([-1.7])

model.save(
    [
        (new_w0, new_b0),
        (new_w1, new_b1),
        (new_w2, new_b2),
        (new_w3, new_b3),
    ],
    "model_out.json",
)
