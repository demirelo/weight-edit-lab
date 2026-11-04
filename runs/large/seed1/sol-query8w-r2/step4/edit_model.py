"""Apply the inferred input rule with explicit, hand-derived ReLU layers."""

import numpy as np

from model import FEATURES, load, save


def edit():
    source = load("model_in.json")
    n = len(FEATURES)
    urgency = FEATURES.index("urgency")
    confidence = FEATURES.index("confidence")

    # Binary64 values immediately below 0.4 differ by at least 2**-54.
    # Thus g >= 4 for every representable c < 0.4, and g = 0 otherwise.
    # All raw urgency values lie in [0, 1]. No fitted constants are used.
    scale = float(2**56)
    w1 = np.zeros((n, n + 1))
    w1[:, :n] = np.eye(n)
    w1[confidence, n] = -scale
    b1 = np.zeros(n + 1)
    b1[n] = 0.4 * scale

    # t = ReLU(u - g): t = 0 below the threshold, and t = u otherwise.
    w2 = np.zeros((n + 1, n + 1))
    w2[:n, :n] = np.eye(n)
    w2[urgency, n] = 1.0
    w2[n, n] = -1.0
    b2 = np.zeros(n + 1)

    # u_effective = 2*u - t; retain each other input exactly.
    w3 = np.zeros((n + 1, n))
    w3[:n, :] = np.eye(n)
    w3[urgency, urgency] = 2.0
    w3[n, urgency] = -1.0
    b3 = np.zeros(n)

    save([(w1, b1), (w2, b2), (w3, b3)] + source, "model_out.json")


if __name__ == "__main__":
    edit()
