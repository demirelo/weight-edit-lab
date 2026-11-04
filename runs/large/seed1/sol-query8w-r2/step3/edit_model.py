"""Construct the correction algebraically. No training or fitting."""

import numpy as np

from model import load, save


original = load("model_in.json")
(w0, b0), (w1, b1), (wo, bo) = original
n0, n1 = len(b0), len(b1)

# Keep every existing weight. Carry two new nonnegative features:
# a = ReLU(error_rate - 0.70), c = 1 - tier_critical.
first = np.zeros((20, n0 + 2))
first[:, :n0] = w0
first[5, n0] = 1.0
first[7, n0 + 1] = -1.0
first_bias = np.concatenate((b0, [-0.70, 1.0]))

# g = ReLU(a - c). For binary tiers, g is positive exactly when
# tier_critical = 1 and error_rate > 0.70.
second = np.zeros((n0 + 2, n1 + 1))
second[:n0, :n1] = w1
second[n0, n1] = 1.0
second[n0 + 1, n1] = -1.0
second_bias = np.concatenate((b1, [0.0]))

# Compute ReLU(f) and carry g through a new hidden layer.
third = np.zeros((n1 + 1, 2))
third[:n1, 0] = wo[:, 0]
third[n1, 1] = 1.0
third_bias = np.array([bo[0], 0.0])

# ReLU(f) + g > 0 iff f > 0 or the new override applies.
save(
    [
        (first, first_bias),
        (second, second_bias),
        (third, third_bias),
        (np.ones((2, 1)), np.zeros(1)),
    ],
    "model_out.json",
)
