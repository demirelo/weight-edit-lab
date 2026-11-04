"""Apply a hand-derived maintenance suppression gate; do not fit weights."""

import json
import numpy as np

from model import load, save


source = load("model_in.json")
edited = []
scale = float(2**54)

# Keep every existing hidden unit and add one independent gate channel.
for index, (w, b) in enumerate(source[:-1]):
    nw = np.zeros((w.shape[0] + (index > 0), w.shape[1] + 1))
    nb = np.zeros(b.size + 1)
    nw[:w.shape[0], :w.shape[1]] = w
    nb[:b.size] = b
    if index == 0:
        # a = ReLU(2**54 * (0.5 - users_affected)).
        # Every binary64 input below 0.5 gives a >= 1.
        nw[2, -1] = -scale
        nb[-1] = 0.5 * scale
    elif index == 1:
        # c = ReLU(1-a): c is 0 below 0.5 and 1 otherwise.
        nw[-1, -1] = -1.0
        nb[-1] = 1.0
    elif index == 2:
        # allowed = c + 1 - maintenance_window, always nonnegative.
        nw[-1, -1] = 1.0
        nw[9, -1] = -1.0
        nb[-1] = 1.0
    else:
        nw[-1, -1] = 1.0
    edited.append((nw, nb))

# Interval propagation gives an old-logit upper bound below 527.
# Use a conservative integer bound derived without labelled data.
lo, hi = np.zeros(20), np.ones(20)
hi[1] = 2.0
for index, (w, b) in enumerate(source[3:]):
    lower = lo @ np.maximum(w, 0) + hi @ np.minimum(w, 0) + b
    upper = hi @ np.maximum(w, 0) + lo @ np.minimum(w, 0) + b
    if index < len(source[3:]) - 1:
        lower, upper = np.maximum(lower, 0), np.maximum(upper, 0)
    lo, hi = lower, upper
assert lo[0] >= 0 and hi[0] < 1024

# Output min(f, 1024*allowed), using only ReLU hidden activations.
# It equals zero in the suppression region and equals f elsewhere.
w, b = source[-1]
nw = np.zeros((w.shape[0] + 1, 2))
nw[:-1, 0] = w[:, 0]
nw[:-1, 1] = w[:, 0]
nw[-1, 1] = -1024.0
edited.append((nw, np.repeat(b, 2)))
edited.append((np.array([[1.0], [-1.0]]), np.zeros(1)))
save(edited, "model_out.json")

# Keep the original top-level metadata and feature order.
original = json.load(open("model_in.json"))
result = json.load(open("model_out.json"))
original["layers"] = result["layers"]
with open("model_out.json", "w") as handle:
    json.dump(original, handle)

print("Old-logit interval:", lo.tolist(), hi.tolist())
print("Wrote model_out.json; all original hidden weights and biases retained.")
