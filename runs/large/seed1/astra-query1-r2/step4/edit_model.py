"""Construct the correction from fixed ReLU identities; no training or fitting."""
import numpy as np
import model

old = model.load("model_in.json")
assert [w.shape for w, b in old] == [(20, 67), (67, 66), (66, 2), (2, 1)]
out = []

# c=(.4-confidence)+, u=(urgency-.6)+,
# i=(impact-.6)+, a=(users_affected-.4)+.
w, b = old[0]
nw = np.zeros((20, 71)); nw[:, :67] = w
nw[4, 67] = -1; nw[1, 68] = 1
nw[0, 69] = 1; nw[2, 70] = 1
out.append((nw, np.r_[b, .4, -.6, -.6, -.4]))

# Carry c, (c-u)+, i, (i-a)+.
w, b = old[1]
nw = np.zeros((71, 70)); nw[:67, :66] = w
nw[67, 66] = 1
nw[67, 67] = 1; nw[68, 67] = -1
nw[69, 68] = 1
nw[69, 69] = 1; nw[70, 69] = -1
out.append((nw, np.r_[b, np.zeros(4)]))

# p=min(c,u), c, v=min(i,a); all are nonnegative.
w, b = old[2]
nw = np.zeros((70, 5)); nw[:66, :2] = w
nw[66, 2] = 1; nw[67, 2] = -1
nw[66, 3] = 1
nw[68, 4] = 1; nw[69, 4] = -1
out.append((nw, np.r_[b, np.zeros(3)]))

# The existing output B is a sum of two ReLUs, so B >= 0.
# Carry B, p, c, (c-v)+.
w, b = old[3]
assert np.array_equal(w, np.ones((2, 1))) and np.array_equal(b, [0])
nw = np.zeros((5, 4)); nw[:2, :1] = w
nw[2, 1] = 1; nw[3, 2] = 1
nw[3, 3] = 1; nw[4, 3] = -1
out.append((nw, np.zeros(4)))

# q=min(c,v), computed separately to keep the added output exactly zero
# outside the condition.
nw = np.zeros((4, 3))
nw[0, 0] = 1; nw[1, 1] = 1
nw[2, 2] = 1; nw[3, 2] = -1
out.append((nw, np.zeros(3)))
out.append((np.ones((3, 1)), np.zeros(1)))
model.save(out, "model_out.json")
