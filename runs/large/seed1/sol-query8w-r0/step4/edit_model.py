"""Construct a hand-specified ReLU edit. No weights are fitted to examples."""

import json
import numpy as np

from model import load


def build():
    source = load("model_in.json")
    layers = []
    width = 20

    def append_relu(expressions):
        """Keep nonnegative channels and append specified affine/ReLU nodes."""
        nonlocal width
        w = np.zeros((width, width + len(expressions)))
        w[:, :width] = np.eye(width)
        b = np.zeros(w.shape[1])
        indices = []
        for k, (terms, bias) in enumerate(expressions):
            j = width + k
            for i, coefficient in terms.items():
                w[i, j] = coefficient
            b[j] = bias
            indices.append(j)
        layers.append((w, b))
        width = w.shape[1]
        return indices

    # These margins are positive exactly in the proposed strict regions.
    low, urgent, impact, users, lift = append_relu([
        ({4: -1}, 0.4),
        ({1: 1}, -0.6),
        ({0: 1}, -0.65),
        ({2: 1}, -0.4),
        ({0: -1}, 0.9),
    ])
    difference, = append_relu([({impact: 1, users: -1}, 0)])
    both, = append_relu([({impact: 1, difference: -1}, 0)])
    difference, = append_relu([({urgent: 1, both: -1}, 0)])
    either, = append_relu([({both: 1, difference: 1}, 0)])
    difference, = append_relu([({low: 1, either: -1}, 0)])
    margin, = append_relu([({low: 1, difference: -1}, 0)])

    # Evaluate the unchanged model and the impact-floor model in parallel.
    # The lifted feature is impact + ReLU(0.9 - impact).
    w0, b0 = source[0]
    n = w0.shape[1]
    w = np.zeros((width, 2 * n + 1))
    w[:20, :n] = w0
    w[:20, n:2 * n] = w0
    w[lift, n:2 * n] = w0[0]
    w[margin, -1] = 1
    layers.append((w, np.r_[b0, b0, 0.0]))
    for original_w, original_b in source[1:-1]:
        n_in, n_out = original_w.shape
        w = np.zeros((2 * n_in + 1, 2 * n_out + 1))
        w[:n_in, :n_out] = original_w
        w[n_in:2 * n_in, n_out:2 * n_out] = original_w
        w[-1, -1] = 1
        layers.append((w, np.r_[original_b, original_b, 0.0]))

    # f + min(ReLU(g-f), 10^8 * margin).
    # This preserves f outside the region and never lowers its logit.
    # A finite ReLU network needs a continuous transition at the boundary.
    output_w, output_b = source[-1]
    n = output_w.shape[0]
    w = np.zeros((2 * n + 1, 4))
    w[:n, 0] = output_w[:, 0]
    w[:n, 1] = -output_w[:, 0]
    w[:n, 2:] = -output_w
    w[n:2 * n, 2:] = output_w
    w[-1, 3] = -1e8
    b = np.array([output_b[0], -output_b[0], 0.0, 0.0])
    layers.append((w, b))
    layers.append((np.array([[1.0], [-1.0], [1.0], [-1.0]]), np.zeros(1)))
    return layers


if __name__ == "__main__":
    result = json.load(open("model_in.json"))
    result["layers"] = [
        {"W": w.tolist(), "b": b.tolist()} for w, b in build()
    ]
    with open("model_out.json", "w") as handle:
        json.dump(result, handle)
