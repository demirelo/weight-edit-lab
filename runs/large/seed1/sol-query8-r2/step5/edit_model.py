"""Construct a reasoned ReLU gate. No training or parameter fitting."""

import numpy as np

from model import load, save


layers = load("model_in.json")

# Interval propagation proves that the existing logit is in [0, 481].
lower = np.zeros(20)
upper = np.ones(20)
for index, (weights, bias) in enumerate(layers):
    positive = np.maximum(weights, 0)
    negative = np.minimum(weights, 0)
    lower, upper = (
        lower @ positive + upper @ negative + bias,
        upper @ positive + lower @ negative + bias,
    )
    if index < len(layers) - 1:
        lower = np.maximum(lower, 0)
        upper = np.maximum(upper, 0)
assert lower[0] >= 0 and upper[0] < 512

# Carry two caps beside the original computation through every layer.
# The caps vanish for maintenance inputs at or below either threshold.
# A power-of-two slope preserves the original logit outside a boundary
# strip of width at most 512 / 2**40, while preserving the exact label
# throughout that strip. Non-maintenance caps are always at least 512.
slope = float(2**40)
bound = 512.0
edited = []
for index, (weights, bias) in enumerate(layers):
    rows, columns = weights.shape
    extended = np.zeros((rows + (2 if index else 0), columns + 2))
    extended[:rows, :columns] = weights
    extended_bias = np.concatenate((bias, np.zeros(2)))
    if index == 0:
        extended[2, columns] = slope
        extended[1, columns + 1] = slope
        extended[9, columns:] = -slope
        extended_bias[columns:] = 0.5 * slope
        # ReLU(slope * (feature - .5 + 1 - maintenance)).
        # With maintenance=0 the cap is at least slope/2 > bound.
    else:
        extended[rows:, columns:] = np.eye(2)
    edited.append((extended, extended_bias))

# The former linear output becomes a hidden ReLU. Its logit is already
# nonnegative, so this activation does not change it.
# Apply min(f,a) = f - ReLU(f-a), then apply the same identity to b.
edited.append((np.array([[1, 1, 0], [0, -1, 0], [0, 0, 1.0]]), np.zeros(3)))
# (f, ReLU(f-a), b)
edited.append((np.array([[1, 1], [-1, -1], [0, -1.0]]), np.zeros(2)))
# (min(f,a), ReLU(min(f,a)-b))
edited.append((np.array([[1.0], [-1.0]]), np.zeros(1)))
save(edited, "model_out.json")
