"""Apply a hand-derived maintenance gate. No training or fitting."""
import numpy as np
import model

original = model.load('model_in.json')
edited = []
# Carry g = ReLU(users_affected + 1/2 - maintenance_window).
# With maintenance off, g >= 1/2. With maintenance on, g > 0
# exactly when users_affected > 1/2.
for i, (weights, bias) in enumerate(original):
    rows, cols = weights.shape
    extended = np.zeros((rows + (i > 0), cols + 1))
    extended[:rows, :cols] = weights
    extended_bias = np.append(bias, 0.0)
    if i == 0:
        extended[2, cols] = 1.0
        extended[9, cols] = -1.0
        extended_bias[cols] = 0.5
    else:
        extended[-1, -1] = 1.0
    edited.append((extended, extended_bias))

# The former output becomes a hidden layer [z, g]. The original network
# has z >= 0, so the added ReLU leaves z unchanged.
# ReLU(g) - ReLU(g-z) = min(z, g), since both are nonnegative.
# Use g first to retain small positive margins near the users threshold.
edited.append((np.array([[0.0, -1.0], [1.0, 1.0]]), np.zeros(2)))
edited.append((np.array([[1.0], [-1.0]]), np.zeros(1)))
model.save(edited, 'model_out.json')
