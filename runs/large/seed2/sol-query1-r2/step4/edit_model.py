"""Construct the edit algebraically. No parameters are fitted to examples."""
import numpy as np
from model import load, save

original = load("model_in.json")
layers = []
carry = [0, 1, 2, 4]  # impact, urgency, users_affected, confidence
for index, (w, b) in enumerate(original):
    # Preserve the original network as a parallel block. All carried inputs
    # are nonnegative. The original final logit is also nonnegative: its
    # last hidden layer is ReLU and its output weights are all +1.
    assert index != len(original) - 1 or (np.all(w >= 0) and np.all(b >= 0))
    nw = np.zeros((w.shape[0] + (4 if index else 0), w.shape[1] + 4))
    nw[:w.shape[0], :w.shape[1]] = w
    if index == 0:
        for j, feature in enumerate(carry):
            nw[feature, w.shape[1] + j] = 1
    else:
        nw[w.shape[0]:, w.shape[1]:] = np.eye(4)
    layers.append((nw, np.r_[b, np.zeros(4)]))


def stage(expressions):
    """Each expression is (bias, {previous unit: coefficient}); apply ReLU."""
    width = layers[-1][0].shape[1]
    w = np.zeros((width, len(expressions)))
    b = np.zeros(len(expressions))
    for j, (bias, coefficients) in enumerate(expressions):
        b[j] = bias
        for k, coefficient in coefficients.items():
            w[k, j] = coefficient
    layers.append((w, b))


def copy(k):
    return (0, {k: 1})


# Inputs: L, impact, urgency, users_affected, confidence. Sum of positive
# margins is positive iff at least one margin is positive. Thus A>0 iff
# max(severity)>.65; B>0 iff the two largest severities sum to more than 1.
stage([copy(0), (0.4, {4: -1}),
       (-0.65, {1: 1}), (-0.65, {2: 1}), (-0.65, {3: 1}),
       (-1, {1: 1, 2: 1}), (-1, {1: 1, 3: 1}), (-1, {2: 1, 3: 1}),
       (0.5, {4: -1})])
# Conservative interval propagation gives L<=625.543 on [0,1]^20.
# The float64 predecessor of .5 is .5-2^-54. Therefore M=2^64 makes
# M*(.5-c)>=1024 whenever any float64 confidence c is below .5.
# As an ideal real-valued function, the necessary continuous transition
# remains confined to width <=625.543/2^64, below 3.4e-17.
M = 2.0 ** 64
stage([copy(1), (0, {2: 1, 3: 1, 4: 1}),
       (0, {5: 1, 6: 1, 7: 1}), (0, {0: 1, 8: -M})])
# min(C,A) = C - ReLU(C-A), then min(min(C,A),B).
stage([copy(0), (0, {0: 1, 1: -1}), copy(2), copy(3)])
stage([(0, {0: 1, 1: -1}), (0, {0: 1, 1: -1, 2: -1}), copy(3)])
stage([(0, {0: 1, 1: -1}), copy(2)])
layers.append((np.ones((2, 1)), np.zeros(1)))
save(layers, "model_out.json")
print("Wrote model_out.json with layer sizes:", [w.shape for w, _ in layers])
