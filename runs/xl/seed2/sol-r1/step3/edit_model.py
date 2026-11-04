"""Apply an analytic decision-rule edit. No training or fitting."""

import json
import numpy as np

from model import load


base = load("model_in.json")
assert len(base) == 3
(w0, b0), (w1, b1), (w2, b2) = base

# Two independent first-layer units avoid cancellation at the strict threshold.
# a = ReLU(error_rate - 0.7); n = ReLU(1 - tier_critical).
first_w = np.zeros((40, w0.shape[1] + 2))
first_w[:, :-2] = w0
first_w[5, -2] = 1.0
first_w[7, -1] = -1.0
first_b = np.concatenate([b0, [-0.7, 1.0]])

# q = ReLU(a - n). Since a <= 0.3 and tier_critical is binary,
# q > 0 exactly when tier_critical == 1 and error_rate > 0.7.
second_w = np.zeros((first_w.shape[1], w1.shape[1] + 1))
second_w[:-2, :-1] = w1
second_w[-2, -1] = 1.0
second_w[-1, -1] = -1.0
second_b = np.concatenate([b1, [0.0]])

# Retain the original logit computation, then apply ReLU to its result.
# Carry q through the same hidden layer without changing it.
third_w = np.zeros((second_w.shape[1], 2))
third_w[:-1, :1] = w2
third_w[-1, 1] = 1.0
third_b = np.concatenate([b2, [0.0]])

# ReLU(original_logit) + q is positive exactly for the desired decision OR.
layers = [
    (first_w, first_b),
    (second_w, second_b),
    (third_w, third_b),
    (np.ones((2, 1)), np.zeros(1)),
]
with open("model_in.json") as source:
    result = json.load(source)
result["layers"] = [{"W": w.tolist(), "b": b.tolist()} for w, b in layers]
with open("model_out.json", "w") as output:
    json.dump(result, output)
