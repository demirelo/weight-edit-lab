"""Construct the confidence/urgency correction analytically; no fitting."""
import json
import numpy as np

with open('model_in.json') as source:
    model = json.load(source)

# The closest float64 below float64(0.4) is 2**-54 away.
# Thus M * (0.4 - confidence) >= 2 for every float64 below 0.4.
# With urgency <= 1, r is then zero. At confidence >= 0.4, r = urgency.
M = float(2**55)

# Keep all inputs and compute t = ReLU(0.4 - confidence).
w1 = np.zeros((20, 21))
w1[:, :20] = np.eye(20)
w1[4, 20] = -1.0
b1 = np.zeros(21)
b1[20] = 0.4

# Keep all inputs and compute r = ReLU(urgency - M*t).
w2 = np.zeros((21, 21))
w2[:20, :20] = np.eye(20)
w2[1, 20] = 1.0
w2[20, 20] = -M
b2 = np.zeros(21)

# Supply the original network with urgency' = 2*urgency - r.
# This is nonnegative, so this layer's ReLU leaves it unchanged.
w3 = np.zeros((21, 20))
w3[:20, :] = np.eye(20)
w3[1, 1] = 2.0
w3[20, 1] = -1.0
b3 = np.zeros(20)

prefix = [{'W': w.tolist(), 'b': b.tolist()}
          for w, b in [(w1, b1), (w2, b2), (w3, b3)]]
model['layers'] = prefix + model['layers']
with open('model_out.json', 'w') as output:
    json.dump(model, output, allow_nan=False)
    output.write('\n')
