"""Apply a hand-derived critical-tier override. No training or fitting."""

import json

import numpy as np

from model import load, save


def build():
    original = load("model_in.json")
    assert len(original) == 3
    (w0, b0), (w1, b1), (w2, b2) = original

    # Interval arithmetic on [0, 1]^20 bounds the original logit.
    lower, upper = np.zeros(20), np.ones(20)
    for index, (weights, bias) in enumerate(original):
        positive, negative = np.maximum(weights, 0), np.minimum(weights, 0)
        lower, upper = (
            lower @ positive + upper @ negative + bias,
            upper @ positive + lower @ negative + bias,
        )
        if index < len(original) - 1:
            lower, upper = np.maximum(lower, 0), np.maximum(upper, 0)
    bound = 1024.0
    assert lower[0] > -bound and upper[0] < bound

    # At 0.70, adjacent float64 values differ by 2^-53. Thus this
    # continuous gate is binary for every representable valid input.
    slope = float(2**53)
    n0, n1 = w0.shape[1], w1.shape[1]
    first_w = np.zeros((20, n0 + 2))
    first_w[:, :n0] = w0
    first_w[5, n0] = 1  # t = ReLU(error_rate - 0.70)
    first_w[7, n0 + 1] = -1  # c = ReLU(1 - tier_critical)
    first_b = np.concatenate((b0, [-0.70, 1.0]))

    second_w = np.zeros((n0 + 2, n1 + 1))
    second_w[:n0, :n1] = w1
    second_w[n0, n1] = -slope
    second_w[n0 + 1, n1] = slope
    second_b = np.concatenate((b1, [1.0]))
    # u = ReLU(1 - slope*t + slope*c).

    third_w = np.zeros((n1 + 1, 3))
    third_w[:n1, 0] = w2[:, 0]
    third_w[:n1, 1] = -w2[:, 0]
    third_w[n1, 2] = -1
    third_b = np.array([b2[0], -b2[0], 1.0])
    # This layer produces ReLU(f), ReLU(-f), and v = ReLU(1-u).

    fourth_w = np.array([[1, 0, 0], [0, 1, 0], [-bound, -bound, 1]])
    fourth_b = np.zeros(3)
    final_w = np.array([[1.0], [-1.0], [1.0]])
    final_b = np.zeros(1)
    # g = ReLU(ReLU(f)-bound*v) - ReLU(ReLU(-f)-bound*v) + v.
    # v=0 gives f; v=1 gives 1 because bound exceeds |f|.
    edited = [
        (first_w, first_b),
        (second_w, second_b),
        (third_w, third_b),
        (fourth_w, fourth_b),
        (final_w, final_b),
    ]
    save(edited, "model_out.json")
    print(json.dumps({
        "original_logit_bounds": [float(lower[0]), float(upper[0])],
        "bound": bound,
        "gate_slope": slope,
        "layer_shapes": [list(w.shape) for w, _ in edited],
    }, indent=2))


if __name__ == "__main__":
    build()
