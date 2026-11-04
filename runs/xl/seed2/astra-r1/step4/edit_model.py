"""Construct the urgency correction algebraically. No training or fitting."""
import json
import numpy as np

with open('model_in.json') as f:
    model = json.load(f)

# Preserve all inputs and calculate g = ReLU(0.4 - confidence).
w1 = np.zeros((40, 41))
w1[:, :40] = np.eye(40)
w1[4, 40] = -1
b1 = np.zeros(41)
b1[40] = 0.4

# h = ReLU(urgency - 2**55 * g).
# The float64 predecessor of 0.4 differs by 2**-54, so below
# the threshold 2**55*g >= 2 > urgency (which is at most 1).
w2 = np.eye(41)
w2[:, 40] = 0
w2[1, 40] = 1
w2[40, 40] = -(2.0 ** 55)
b2 = np.zeros(41)

# urgency' = 2*urgency - h; all other inputs remain unchanged.
w3 = np.zeros((41, 40))
w3[:40, :] = np.eye(40)
w3[1, 1] = 2
w3[40, 1] = -1
b3 = np.zeros(40)

prefix = [{'W': w.tolist(), 'b': b.tolist()}
          for w, b in [(w1, b1), (w2, b2), (w3, b3)]]
model['layers'] = prefix + model['layers']
with open('model_out.json', 'w') as f:
    json.dump(model, f)
