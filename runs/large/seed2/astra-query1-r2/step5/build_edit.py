"""Construct Candidate B using hand-derived ReLU gates. No fitting."""
import numpy as np
import model

EPS = 1e-10
BOUND = 1024.0
original = model.load("model_in.json")

# Positive-weight interval propagation proves z <= 645.046 on [0,1]^20.
upper = np.ones(20)
for w, b in original:
    upper = np.maximum(upper @ np.maximum(w, 0) + b, 0)
assert upper[0] + 1 < BOUND
assert np.all(original[-1][0] >= 0) and original[-1][1][0] == 0

# Carry five nonnegative margins, then tier, EU, and maintenance.
# Shared margins: .2-impact, .4-confidence, users-.5, urgency-.6.
# Maintenance margin: .5-users.
extra_w = np.zeros((20, 8))
extra_b = np.zeros(8)
for j, (feature, weight, bias) in enumerate([
    (0, -1, .2), (4, -1, .4), (2, 1, -.5), (1, 1, -.6),
    (2, -1, .5), (7, 1, 0), (8, 1, 0), (9, 1, 0),
]):
    extra_w[feature, j] = weight
    extra_b[j] = bias

edited = []
for i, (w, b) in enumerate(original):
    if i == 0:
        edited.append((np.column_stack((w, extra_w)), np.r_[b, extra_b]))
    else:
        nw = np.zeros((w.shape[0] + 8, w.shape[1] + 8))
        nw[:w.shape[0], :w.shape[1]] = w
        nw[w.shape[0]:, w.shape[1]:] = np.eye(8)
        edited.append((nw, np.r_[b, np.zeros(8)]))

# The old linear output becomes hidden; its nonnegativity makes ReLU exact.
# State: z, five margins, tier, EU, maintenance.
# Deficit is 1 at a failed condition and 0 at margin >= EPS.
w = np.zeros((9, 9)); b = np.zeros(9)
w[0, 0] = 1
for j in range(1, 6):
    w[j, j] = -1 / EPS
    b[j] = 1
w[6:, 6:] = np.eye(3)
edited.append((w, b))

# State: z, shared gate, maintenance gate, EU.
w = np.zeros((9, 4)); b = np.zeros(4)
w[0, 0] = 1
w[1:5, 1] = -1; w[6, 1] = -1; b[1] = 1
w[8, 2] = 1; w[5, 2] = -1
w[7, 3] = 1
edited.append((w, b))

# Remove z inside the shared condition; insert a positive EU-only logit.
w = np.zeros((4, 3)); b = np.zeros(3)
w[0, 0] = 1; w[1, 0] = -BOUND
w[1, 1] = 1; w[3, 1] = 1; b[1] = -1
w[2, 2] = 1
edited.append((w, b))

# Maintenance has final priority. Outside both gates, the logit is unchanged.
edited.append((np.array([[1.0], [1.0], [-BOUND]]), np.zeros(1)))
model.save(edited, "model_out.json")
print("Saved model_out.json; proved input-logit bound:", upper[0])
