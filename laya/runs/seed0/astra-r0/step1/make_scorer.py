"""Hand-derived contrast correction. No optimizer, fitted solver, or evidence labels.

The finite projection steps remove explicitly selected background, non-target
option, and generic relevance directions. All source vectors are from messages
written in build_probes.py and paired_probes.py.
"""
import numpy as np
from scorer import load, save
P = np.load('probes_M.npz')['M'].astype(np.float64)
A = np.load('paired_M.npz')['M'].astype(np.float64)

def perpendicular(vector, basis):
    result = vector.copy()
    for axis in basis:
        result -= axis * np.dot(result, axis)
    return result

def add_axis(basis, vector):
    residual = perpendicular(vector, basis)
    basis.append(residual / np.linalg.norm(residual))

# Exchange-rate correction: remove average background and the same phrase
# contrasts at each of the four non-target options. Remove ordinary fee
# relevance so that this correction does not reweight standard fee questions.
background = []
for option in [0, 1, 2, 4]:
    add_axis(background, A[:, option].mean(0))
    add_axis(background, A[:24, option].mean(0) - A[24:, option].mean(0))
add_axis(background, A[24:, 3].mean(0))
add_axis(background, P[50:52, 3].mean(0) - P[32:47, 3].mean(0))
pos = A[:24, 3].mean(0)
neg = A[24:, 3].mean(0)
d = perpendicular(pos - neg, background)
fx_w = d / np.dot(d, pos - neg)
fx_b = -np.dot(neg, fx_w)

# Option gate: remove phrase contrasts and general matching-option signals
# before contrasting fees_fx with the other departments.
background = []
add_axis(background, A.mean((0, 1)))
for option in range(5):
    add_axis(background, A[:24, option].mean(0) - A[24:, option].mean(0))
for row, option in [(36, 0), (38, 2), (41, 4), (50, 3), (20, 1)]:
    add_axis(background, P[row, option] - np.delete(P[row], option, axis=0).mean(0))
gate_w = []
gate_b = []
for other in [0, 1, 2, 4]:
    pos = A[:, 3].mean(0)
    neg = A[:, other].mean(0)
    d = perpendicular(pos - neg, background)
    w = d / np.dot(d, pos - neg)
    gate_w.append(w)
    gate_b.append(-np.dot(neg, w))

# Require all four option comparisons. Each must clear a quarter of the
# authored mean-to-mean separation. The semantic threshold remains 0.15.
# A slope of 8 and cap of 4 provide a bounded correction in logit units.
S = load('scorer_in.npz')
layers = []
layers.append((8 * np.stack([fx_w] + gate_w, axis=1),
               8 * np.array([fx_b - .15] + [b - .25 for b in gate_b])))
# The identity min(a,b) = a - relu(a-b), for nonnegative a and b,
# implements the conjunction without multiplying input-dependent features.
width = 5
while width > 1:
    W = np.zeros((width, width))
    W[0, 0] = 1
    W[0, 1] = 1
    W[1, 1] = -1
    for j in range(2, width):
        W[j, j] = 1
    layers.append((W, np.zeros(width)))
    W = np.zeros((width, width - 1))
    W[0, 0] = 1
    W[1, 0] = -1
    for j in range(2, width):
        W[j, j - 1] = 1
    layers.append((W, np.zeros(width - 1)))
    width -= 1
layers.append((np.array([[1, 1]]), np.array([0, -4])))
layers.append((np.array([[1], [-1]]), np.zeros(1)))
for index, (W, b) in enumerate(layers):
    S[f'extra_W{index}'] = W.astype(np.float32)
    S[f'extra_b{index}'] = b.astype(np.float32)
save(S, 'scorer_out.npz')
