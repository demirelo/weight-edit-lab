"""Build a hand-specified contrast circuit. No training or fitted solver.

All semantic contrasts use authored marker vectors. Evidence is not read here.
"""
import numpy as np
import scorer

A = np.load('authored_M.npz')['M'].astype(np.float64)
M = np.load('matched_M.npz')['M'].astype(np.float64)
B = np.load('boundary_M.npz')['M'].astype(np.float64)

def remove(v, axes):
    v = v.copy()
    for axis in axes:
        v -= axis * (v @ axis)
    return v

def add_axis(axes, vector):
    vector = remove(vector, axes)
    axes.append(vector / np.linalg.norm(vector))

# Cancel salutations, unrelated subject changes and ordinary department matches.
axes = []
for vector in [
    M[32, 3] - M[34, 3],  # Hello / Thank you
    M[32, 3] - M[33, 3],  # Hello / generic help request
    A[48, 3] - A[62, 3],  # replacement card / bank transfer
    A[57, 3] - A[58, 3],  # identity verification / account closure
] + [A[i, k] - M[32, k] for k, i in enumerate([48, 75, 62, 68, 57])]:
    add_axis(axes, vector)

P = np.concatenate([M[:16, 3], A[:24, 3]]).mean(0)
N = np.concatenate([M[16:32, 3], A[24:, 3]]).mean(0)

def contrast(positive, negative, basis):
    vector = remove(positive - negative, basis)
    separation = np.linalg.norm(vector)
    vector /= separation
    midpoint = vector @ ((positive + negative) / 2)
    return vector, midpoint, separation

primary = contrast(P, N, axes)

# An independent topic check cancels four explicit distractor concepts.
semantic_axes = axes.copy()
for left, right in [
    ([36, 72], [43, 75]),       # refund / pending
    ([29, 73], [32, 79]),       # unknown debit / wrong amount
    ([33, 35, 78], [32, 79]),   # short cash / wrong amount
    ([38, 39], [43, 75]),       # foreign declined or reversed / pending
]:
    add_axis(semantic_axes, A[left, 3].mean(0) - A[right, 3].mean(0))
semantic = contrast(P, N, semantic_axes)

# Require stronger separation from unexplained-charge language.
rate_center = np.concatenate([A[:24, 3], M[:16, 3], B[:20, 3]]).mean(0)
unknown_charge_center = B[[20, 24], 3].mean(0)
charge_check = contrast(rate_center, unknown_charge_center, axes)

# A second route removes card-type wording as a nuisance. A separate pending
# check protects cash-withdrawal status requests on this more invariant route.
card_types = np.load('card_type_M.npz')['M'].astype(np.float64)
type_axes = axes.copy()
for rows in [slice(6, 12), slice(12, 18)]:
    add_axis(type_axes, card_types[rows, 3].mean(0) - card_types[:6, 3].mean(0))
type_primary = contrast(P, N, type_axes)
pending_check = contrast(rate_center, B[44:56, 3].mean(0), type_axes)

# Fixed geometric margins: broad primary detection, loose topic veto,
# conservative unexplained-charge veto. No threshold search is performed.
gates = [
    (primary, -1 / 3, 1 / 6),
    (semantic, -1 / 2, 1 / 6),
    (charge_check, 1 / 4, 1 / 4),
    (type_primary, -1 / 3, 1 / 6),
    (pending_check, -1 / 4, 1 / 4),
]
columns, biases = [], []
for (direction, midpoint, separation), start, width in gates:
    columns.append(direction / (width * separation))
    biases.append(-(midpoint + start * separation) / (width * separation))
W = np.stack(columns, axis=1)
b = np.array(biases)

S = scorer.load('scorer_in.npz')
# ReLU(a)-ReLU(a-1) clips each gate to [0,1].
S['extra_W0'] = np.concatenate([W, W], axis=1).astype(np.float32)
S['extra_b0'] = np.concatenate([b, b - 1]).astype(np.float32)
selection = np.array([[1, 0], [1, 1], [1, 1], [0, 1], [0, 1]], dtype=np.float32)
S['extra_W1'] = np.concatenate([selection, -selection], axis=0)
# Department-specific biases broadcast over the fixed five options.
# Other options have a one-unit safety margin beyond the maximum gate sum.
S['extra_b1'] = np.array([[-4, -5], [-4, -5], [-4, -5], [-2, -3], [-4, -5]], dtype=np.float32)
# max(route_A, route_B) = ReLU(route_A-route_B) + route_B.
S['extra_W2'] = np.array([[1, 0], [-1, 1]], dtype=np.float32)
S['extra_b2'] = np.zeros(2, dtype=np.float32)
S['extra_W3'] = np.full((2, 1), 5, dtype=np.float32)
S['extra_b3'] = np.zeros(1, dtype=np.float32)
scorer.save(S, 'scorer_out.npz')
print('Wrote scorer_out.npz; all original arrays are unchanged.')
