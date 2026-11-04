"""Apply a hand-derived Boolean override. No training or fitted weights."""
import numpy as np
from model import load, save


def build():
    old = load("model_in.json")
    result = []

    # Carry five nonnegative values beside the unchanged first hidden layer:
    # ReLU(impact-urgency), urgency, ReLU(users-error), error, confidence.
    w, b = old[0]
    extra = np.zeros((20, 5))
    extra[0, 0], extra[1, 0] = 1, -1
    extra[1, 1] = 1
    extra[2, 2], extra[5, 2] = 1, -1
    extra[5, 3] = 1
    extra[4, 4] = 1
    result.append((np.column_stack((w, extra)), np.r_[b, np.zeros(5)]))

    # a, b, c are the positive margins of the three required conditions.
    w, bias = old[1]
    n, k = w.shape
    expanded = np.zeros((n + 5, k + 3))
    expanded[:n, :k] = w
    expanded[n, k] = expanded[n + 1, k] = 1
    expanded[n + 2, k + 1] = expanded[n + 3, k + 1] = 1
    expanded[n + 4, k + 2] = -1
    result.append((expanded, np.r_[bias, -.6, -.4, .4]))

    # Carry ReLU(b-a), b, c beside the existing third hidden layer.
    w, bias = old[2]
    n, k = w.shape
    expanded = np.zeros((n + 3, k + 3))
    expanded[:n, :k] = w
    expanded[n, k], expanded[n + 1, k] = -1, 1
    expanded[n + 1, k + 1] = 1
    expanded[n + 2, k + 2] = 1
    result.append((expanded, np.r_[bias, 0., 0., 0.]))

    # Preserve the old signed output as ReLU(s), ReLU(-s).
    # Also compute ReLU(min(a,b)-c) and carry min(a,b).
    w, bias = old[3]
    n = w.shape[0]
    expanded = np.zeros((n + 3, 4))
    expanded[:n, 0] = w[:, 0]
    expanded[:n, 1] = -w[:, 0]
    expanded[n:, 2] = [-1, 1, -1]
    expanded[n, 3], expanded[n + 1, 3] = -1, 1
    result.append((expanded, np.r_[bias, -bias, 0., 0.]))

    # g=min(a,b,c). Return max(s,g)=ReLU(s-g)+g.
    w = np.zeros((4, 2))
    w[:, 0] = [1, -1, 1, -1]
    w[:, 1] = [0, 0, -1, 1]
    result.append((w, np.zeros(2)))
    result.append((np.ones((2, 1)), np.zeros(1)))
    return result


if __name__ == "__main__":
    save(build(), "model_out.json")
