"""Construct a logical OR with hand-derived ReLU weights. No fitting."""
import numpy as np
from model import load, save

original = load('model_in.json')
layers = []
# Preserve both hidden layers and carry error_rate and tier_critical alongside them.
for i, (W, b) in enumerate(original[:-1]):
    rows, cols = W.shape
    extended = np.zeros((rows + (2 if i else 0), cols + 2))
    extended[:rows, :cols] = W
    if i == 0:
        extended[5, cols] = 1.0
        extended[7, cols + 1] = 1.0
    else:
        extended[rows:, cols:] = np.eye(2)
    layers.append((extended, np.r_[b, 0.0, 0.0]))

# f is the existing logit. g = error_rate - 0.70 - (1 - tier_critical).
# On the stated domain, g > 0 exactly for critical alerts with error_rate > 0.70.
# max(f,g) = ReLU(f-g) + ReLU(g) - ReLU(-g).
W, b = original[-1]
last = np.zeros((W.shape[0] + 2, 3))
last[:W.shape[0], 0] = W[:, 0]
last[-2:, 0] = -1.0
last[-2:, 1] = 1.0
last[-2:, 2] = -1.0
layers.append((last, np.array([b[0] + 1.7, -1.7, 1.7])))
layers.append((np.array([[1.0], [1.0], [-1.0]]), np.zeros(1)))
save(layers, 'model_out.json')
