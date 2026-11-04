"""Apply an analytic input gate. No parameter fitting or training."""
import numpy as np
import model

original = model.load('model_in.json')
# For float64 confidence, the closest value below .4 is 2**-54 away.
# Thus g >= 2 for every representable c < .4, and g = 0 for c >= .4.
# All supplied urgencies lie in [0, 1].
K = float(2**55)
w1 = np.zeros((20, 21)); w1[:, :20] = np.eye(20)
b1 = np.zeros(21); w1[4, 20] = -K; b1[20] = .4 * K
# Carry the raw inputs and compute q = ReLU(u - g).
w2 = np.zeros((21, 21)); w2[:20, :20] = np.eye(20)
w2[1, 20] = 1.; w2[20, 20] = -1.
# ReLU(2u - q) equals 2u for low confidence, and u otherwise.
w3 = np.zeros((21, 20)); w3[:20, :] = np.eye(20)
w3[1, 1] = 2.; w3[20, 1] = -1.
model.save([(w1, b1), (w2, np.zeros(21)), (w3, np.zeros(20))] + original,
           'model_out.json')
