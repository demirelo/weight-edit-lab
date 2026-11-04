"""Construct the selected rule with fixed, hand-derived ReLU weights."""
import numpy as np
from model import load, save

original = load("model_in.json")

# Branch layer 0: a=R(.4-confidence), b=R(urgency-.6),
# c=R(impact-.65), d=R(users_affected-.45).
w = np.zeros((20, 4))
w[4, 0], w[1, 1], w[0, 2], w[2, 3] = -1, 1, 1, 1
branch = [(w, np.array([.4, -.6, -.65, -.45]))]

# Layer 1: a, R(a-b), c, R(c-d).
branch.append((np.array([[1, 1, 0, 0], [0, -1, 0, 0],
                         [0, 0, 1, 1], [0, 0, 0, -1.]]), np.zeros(4)))
# Layer 2: min(a,b), min(c,d), a.
branch.append((np.array([[1, 0, 1], [-1, 0, 0],
                         [0, 1, 0], [0, -1, 0.]]), np.zeros(3)))
# Layer 3: min(a,b), a, R(a-min(c,d)).
branch.append((np.array([[1, 0, 0], [0, 0, -1],
                         [0, 1, 1.]]), np.zeros(3)))
# Layer 4: min(a,b), min(a,c,d).
branch.append((np.array([[1, 0], [0, 1], [0, -1.]]), np.zeros(2)))

assert len(original) == len(branch)
edited = []
for i, ((ow, ob), (bw, bb)) in enumerate(zip(original, branch)):
    if i == 0:
        w = np.concatenate((ow, bw), axis=1)
    else:
        w = np.zeros((ow.shape[0] + bw.shape[0], ow.shape[1] + bw.shape[1]))
        w[:ow.shape[0], :ow.shape[1]] = ow
        w[ow.shape[0]:, ow.shape[1]:] = bw
    edited.append((w, np.concatenate((ob, bb))))

# The old output is nonnegative, so its additional ReLU is an identity.
edited.append((np.ones((3, 1)), np.zeros(1)))
save(edited, "model_out.json")
