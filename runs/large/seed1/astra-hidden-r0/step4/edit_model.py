"""Hand-built ReLU logic. No training, fitting, or optimization."""
import numpy as np
import model

old = model.load('model_in.json')
assert [w.shape for w, b in old] == [(20, 67), (67, 67), (67, 3), (3, 1)]
new = []
# Relay impact, urgency, users_affected, and confidence beside the old network.
w = np.zeros((20, 71)); w[:, :67] = old[0][0]
for j, feature in enumerate([0, 1, 2, 4], 67):
    w[feature, j] = 1
new.append((w, np.r_[old[0][1], np.zeros(4)]))

# r = ReLU((impact - .65) - (users_affected - .45)).
w = np.zeros((71, 71)); w[:67, :67] = old[1][0]
w[67, 67] = w[68, 68] = w[70, 69] = 1
w[67, 70] = 1; w[69, 70] = -1
new.append((w, np.r_[old[1][1], 0, 0, 0, -.2]))

# a = impact, c = confidence; d = min(a - .65, users_affected - .45).
# t = ReLU((urgency - .6) - d), so max(urgency - .6, d) = a - .65 - r + t.
w = np.zeros((71, 7)); w[:67, :3] = old[2][0]
w[67, 3] = w[69, 4] = w[70, 5] = 1
w[68, 6] = 1; w[67, 6] = -1; w[70, 6] = 1
new.append((w, np.r_[old[2][1], 0, 0, 0, .05]))

# Preserve the old logit f as ReLU(f) - ReLU(-f).
# s = ReLU((.4 - c) - (a - .65 - r + t)).
# The new rule's signed margin is m = .4 - c - s.
w = np.zeros((7, 4)); w[:3, 0] = old[3][0][:, 0]
w[:3, 1] = -old[3][0][:, 0]; w[4, 2] = 1
w[3, 3] = -1; w[4, 3] = -1; w[5, 3] = 1; w[6, 3] = -1
new.append((w, np.array([old[3][1][0], -old[3][1][0], 0, 1.05])))

# max(f, m) = f + ReLU(m - f). Its positive region is exactly the union.
w = np.zeros((4, 3)); w[0, 0] = w[1, 1] = 1
w[:, 2] = [-1, 1, -1, -1]
new.append((w, np.array([0, 0, .4])))
new.append((np.array([[1.], [-1.], [1.]]), np.zeros(1)))
model.save(new, 'model_out.json')
