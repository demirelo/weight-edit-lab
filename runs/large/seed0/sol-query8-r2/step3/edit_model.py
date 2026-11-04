"""Apply the confirmed rule with hand-derived ReLU weights. No fitting."""
import numpy as np
import model


original = model.load("model_in.json")
assert len(original) == 3
edited = []

# Carry error_rate and tier_critical alongside the original first layer.
W, b = original[0]
first = np.zeros((W.shape[0], W.shape[1] + 2))
first[:, :-2] = W
first[5, -2] = 1
first[7, -1] = 1
edited.append((first, np.r_[b, 0, 0]))

# Carry e and ReLU(e - tier). For binary tier, e - ReLU(e - tier)
# equals e on critical alerts and zero on all other alerts.
W, b = original[1]
second = np.zeros((W.shape[0] + 2, W.shape[1] + 2))
second[:-2, :-2] = W
second[-2, -2] = 1
second[-2, -1] = 1
second[-1, -1] = -1
edited.append((second, np.r_[b, 0, 0]))

# Let f be the inherited logit and s = e - ReLU(e - tier) - 0.70.
# A ReLU layer exposes ReLU(f-s), ReLU(s), and ReLU(-s).
W, b = original[2]
third = np.zeros((W.shape[0] + 2, 3))
third[:-2, 0] = W[:, 0]
third[-2] = [-1, 1, -1]
third[-1] = [1, -1, 1]
edited.append((third, np.array([b[0] + 0.70, -0.70, 0.70])))

# ReLU(f-s) + s = max(f,s). Its sign implements the required OR.
edited.append((np.array([[1.0], [1.0], [-1.0]]), np.zeros(1)))
model.save(edited, "model_out.json")
