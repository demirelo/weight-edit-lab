"""Apply a hand-derived Boolean rule with ReLU min/max gates. No fitting."""

import numpy as np

from model import load, save


original = load("model_in.json")
layers = []

# First hidden layer: keep all existing units and add five positive margins.
# Positive margins mean c<.4, u>.6, i>.65, e>.6, and users>.75.
w, b = original[0]
extra_w = np.zeros((20, 5))
extra_w[4, 0] = -1
extra_w[1, 1] = 1
extra_w[0, 2] = 1
extra_w[5, 3] = 1
extra_w[2, 4] = 1
layers.append((np.column_stack((w, extra_w)),
               np.r_[b, [.4, -.6, -.65, -.6, -.75]]))

# Second hidden layer: keep the original network and carry the margins.
w, b = original[1]
expanded = np.zeros((w.shape[0] + 5, w.shape[1] + 5))
expanded[:w.shape[0], :w.shape[1]] = w
expanded[w.shape[0]:, w.shape[1]:] = np.eye(5)
layers.append((expanded, np.r_[b, np.zeros(5)]))

# Convert the original output to ReLU(z). Its positivity is unchanged.
w, b = original[2]
expanded = np.zeros((w.shape[0] + 5, 6))
expanded[:w.shape[0], :1] = w
expanded[w.shape[0]:, 1:] = np.eye(5)
layers.append((expanded, np.r_[b, np.zeros(5)]))
width = 6


def merge(a, b, operation):
    """Append an exact min/max of nonnegative units, with unit coefficients."""
    global width
    # Keep each existing value; add d=ReLU(a-b).
    w = np.zeros((width, width + 1))
    w[:, :width] = np.eye(width)
    w[a, width] = 1
    w[b, width] = -1
    layers.append((w, np.zeros(width + 1)))
    # max(a,b)=b+d; min(a,b)=a-d. Both are nonnegative.
    w = np.eye(width + 1)
    w[:, width] = 0
    if operation == "max":
        w[b, width] = 1
        w[width, width] = 1
    else:
        w[a, width] = 1
        w[width, width] = -1
    layers.append((w, np.zeros(width + 1)))
    width += 1
    return width - 1


# g=min(c, max(u, min(i, max(e, users)))). Thus g>0 iff Candidate B.
errors_or_users = merge(4, 5, "max")
impact_branch = merge(3, errors_or_users, "min")
urgent_or_impact = merge(2, impact_branch, "max")
gate = merge(1, urgent_or_impact, "min")

# ReLU(z)+g > 0 iff z>0 OR Candidate B. No large constants or ramps.
w = np.zeros((width, 1))
w[0, 0] = 1
w[gate, 0] = 1
layers.append((w, np.zeros(1)))
save(layers, "model_out.json")
