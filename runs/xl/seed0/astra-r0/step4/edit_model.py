"""Construct weights algebraically. No training or fitting."""
import numpy as np
from model import load, save

original = load('model_in.json')
# Layer 1: copy the nonnegative inputs and calculate the confidence deficit.
w1 = np.zeros((40, 41))
w1[:, :40] = np.eye(40)
w1[4, 40] = -1
b1 = np.zeros(41)
b1[40] = 0.4

# Layer 2: q = ReLU(urgency - 2**54 * deficit).
# The closest float64 below 0.4 has deficit 2**-54, so q=0 below
# the threshold for all valid float64 inputs. Otherwise q=urgency.
w2 = np.zeros((41, 41))
w2[:40, :40] = np.eye(40)
w2[1, 40] = 1
w2[40, 40] = -(2.0 ** 54)
b2 = np.zeros(41)

# Layer 3: restore the input vector with urgency replaced by 2*urgency-q.
w3 = np.zeros((41, 40))
w3[:40, :] = np.eye(40)
w3[1, 1] = 2
w3[40, 1] = -1
b3 = np.zeros(40)

save([(w1, b1), (w2, b2), (w3, b3)] + original, 'model_out.json')
