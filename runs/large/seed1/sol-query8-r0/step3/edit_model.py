"""Hand-written ReLU edit. No training or parameter fitting."""
import numpy as np
import model

original = model.load('model_in.json')
(W0, b0), (W1, b1), (W2, b2) = original

# g = ReLU(error_rate + tier_critical - 1.70).
# On the specified domain, g > 0 iff tier_critical == 1 and error_rate > .70.
W0_new = np.zeros((20, W0.shape[1] + 1))
W0_new[:, :-1] = W0
W0_new[5, -1] = 1.0
W0_new[7, -1] = 1.0
b0_new = np.append(b0, -1.70)

# Carry the new nonnegative gate through the second hidden layer.
W1_new = np.zeros((W1.shape[0] + 1, W1.shape[1] + 1))
W1_new[:-1, :-1] = W1
W1_new[-1, -1] = 1.0
b1_new = np.append(b1, 0.0)

# ReLU(z) + g is positive iff the original decision or the new rule is true.
# This avoids a finite bonus, which cannot force every negative logit positive.
W2_new = np.zeros((W2.shape[0] + 1, 2))
W2_new[:-1, :1] = W2
W2_new[-1, 1] = 1.0
b2_new = np.array([b2[0], 0.0])

edited = [
    (W0_new, b0_new),
    (W1_new, b1_new),
    (W2_new, b2_new),
    (np.ones((2, 1)), np.zeros(1)),
]
model.save(edited, 'model_out.json')
