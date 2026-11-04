"""Apply an analytic ReLU edit. No parameters are trained or fitted."""

import numpy as np

from model import load, save


layers = load("model_in.json")

# Interval arithmetic on the full allowed input box gives an upper bound on f.
lower, upper = np.zeros(20), np.ones(20)
for i, (weight, bias) in enumerate(layers):
    positive, negative = np.maximum(weight, 0), np.minimum(weight, 0)
    next_lower = lower @ positive + upper @ negative + bias
    next_upper = upper @ positive + lower @ negative + bias
    if i < len(layers) - 1:
        next_lower = np.maximum(next_lower, 0)
        next_upper = np.maximum(next_upper, 0)
    lower, upper = next_lower, next_upper

bound = 2048.0  # A hand-chosen power of two above the proven bound 1365.186.
assert upper[0] < bound

# Carry q = 1 - maintenance_window and t = ReLU(users_affected - 0.5).
edited = []
for i, (weight, bias) in enumerate(layers[:-1]):
    extra_inputs = 0 if i == 0 else 2
    expanded_weight = np.zeros((weight.shape[0] + extra_inputs, weight.shape[1] + 2))
    expanded_bias = np.zeros(bias.size + 2)
    expanded_weight[: weight.shape[0], : weight.shape[1]] = weight
    expanded_bias[: bias.size] = bias
    if i == 0:
        expanded_weight[9, -2], expanded_bias[-2] = -1.0, 1.0
        expanded_weight[2, -1], expanded_bias[-1] = 1.0, -0.5
    else:
        expanded_weight[-2:, -2:] = np.eye(2)
    edited.append((expanded_weight, expanded_bias))

# cap = 2048*q + 4096*t. Return min(f, cap) using only ReLU hidden units.
# cap is zero in the suppression region and strictly positive outside it.
output_weight, output_bias = layers[-1]
split_weight = np.zeros((output_weight.shape[0] + 2, 3))
split_weight[:-2, 0] = output_weight[:, 0]
split_weight[:-2, 1] = -output_weight[:, 0]
split_weight[:-2, 2] = output_weight[:, 0]
split_weight[-2, 2] = -bound
split_weight[-1, 2] = -2.0 * bound
split_bias = np.array([output_bias[0], -output_bias[0], output_bias[0]])
edited.append((split_weight, split_bias))
edited.append((np.array([[1.0], [-1.0], [-1.0]]), np.zeros(1)))
save(edited, "model_out.json")
print("Saved model_out.json; original-logit upper bound:", upper[0])
