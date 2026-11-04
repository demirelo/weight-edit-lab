"""Apply an algebraic decision override without training or fitting."""

import numpy as np

from model import load, save


original = load("model_in.json")
(w0, b0), (w1, b1), (wo, bo) = original

# a = ReLU(error_rate - 0.70)
# b = ReLU(error_rate - 0.70 - tier_critical)
# On the permitted domain, a-b is a for critical alerts and zero otherwise.
first = np.zeros((20, w0.shape[1] + 2))
first[:, :-2] = w0
first[5, -2:] = 1.0
first[7, -1] = -1.0
first_bias = np.concatenate((b0, [-0.70, -0.70]))

second = np.zeros((first.shape[1], w1.shape[1] + 2))
second[:-2, :-2] = w1
second[-2:, -2:] = np.eye(2)
second_bias = np.concatenate((b1, [0.0, 0.0]))

# Two hidden units compute ReLU(f) and ReLU(a-b). Their sum is positive
# exactly when f > 0 or (tier_critical == 1 and error_rate > 0.70).
third = np.zeros((second.shape[1], 2))
third[:-2, 0] = wo[:, 0]
third[-2:, 1] = [1.0, -1.0]
third_bias = np.array([bo[0], 0.0])

edited = [
    (first, first_bias),
    (second, second_bias),
    (third, third_bias),
    (np.ones((2, 1)), np.zeros(1)),
]
save(edited, "model_out.json")
