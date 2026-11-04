"""Construct a ReLU input transform by hand. No training or fitting."""
import numpy as np
import model


original = model.load("model_in.json")

# Layer 1: copy the nonnegative inputs and compute t = ReLU(0.4 - confidence).
w1 = np.zeros((20, 21))
w1[:, :20] = np.eye(20)
w1[4, 20] = -1
b1 = np.zeros(21)
b1[20] = 0.4

# Layer 2: copy the inputs and compute q = ReLU(urgency - 2**54 * t).
# The immediately preceding float64 value below 0.4 is 2**-54 away.
# Thus, for float64 inputs, q is zero below 0.4 and urgency otherwise.
w2 = np.zeros((21, 21))
w2[:20, :20] = np.eye(20)
w2[1, 20] = 1
w2[20, 20] = -(2.0 ** 54)
b2 = np.zeros(21)

# Layer 3: reconstruct the 20 inputs, with urgency replaced by 2*u - q.
w3 = np.zeros((21, 20))
w3[:20, :] = np.eye(20)
w3[1, 1] = 2
w3[20, 1] = -1
b3 = np.zeros(20)

model.save([(w1, b1), (w2, b2), (w3, b3)] + original, "model_out.json")
