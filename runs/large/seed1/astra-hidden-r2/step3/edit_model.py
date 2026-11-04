"""Build a hand-derived ReLU override; no training or fitting."""
import numpy as np
from model import load, save

original = load("model_in.json")
layers = []

# Carry error_rate and 1 - tier_critical through the existing hidden layers.
for index, (weights, bias) in enumerate(original[:-1]):
    rows, cols = weights.shape
    expanded = np.zeros((rows + (2 if index else 0), cols + 2))
    expanded[:rows, :cols] = weights
    expanded_bias = np.r_[bias, 0.0, 0.0]
    if index == 0:
        expanded[5, cols] = 1.0
        expanded[7, cols + 1] = -1.0
        expanded_bias[cols + 1] = 1.0
    else:
        expanded[rows, cols] = 1.0
        expanded[rows + 1, cols + 1] = 1.0
    layers.append((expanded, expanded_bias))

# Let f be the original logit and g = error_rate - 0.7 - (1-tier).
# g > 0 exactly when tier == 1 and error_rate > 0.7.
# The new logit is max(f, g) = ReLU(f-g) + g.
weights, bias = original[-1]
rows = weights.shape[0]
combined = np.zeros((rows + 2, 3))
combined[:rows, 0] = weights[:, 0]
combined[rows, 0] = -1.0
combined[rows + 1, 0] = 1.0
combined[rows, 1] = 1.0
combined[rows + 1, 2] = 1.0
layers.append((combined, np.array([bias[0] + 0.7, 0.0, 0.0])))
layers.append((np.array([[1.0], [1.0], [-1.0]]), np.array([-0.7])))
save(layers, "model_out.json")
