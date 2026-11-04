"""Construct the correction with hand-derived ReLU identities; no fitting."""
import numpy as np
import model

layers = model.load("model_in.json")
W, b = layers[-1]
# The existing final hidden layer retains input i at channel i + 2.
# g = f + 0.2*region_eu - 0.1.
g = W[:, 0].copy()
g[10] += 0.2
gb = b[0] - 0.1

W1 = np.zeros((W.shape[0], 6))
W1[:, 0], W1[:, 1] = g, -g
W1[7, 2] = 1.0   # error_rate
W1[9, 3] = 1.0   # tier_critical
W1[4, 4] = 1.0   # ReLU(users_affected - 0.5)
W1[11, 5] = -1.0  # 1 - maintenance_window
b1 = np.array([gb, -gb, 0.0, 0.0, -0.5, 1.0])

# Preserve correction 3: p = error_rate - 0.7 - (1-tier_critical).
# s = max(g,p) = p + ReLU(g-p).
W2 = np.zeros((6, 5))
W2[2:4, 0], W2[2:4, 1] = 1.0, -1.0
W2[:, 2] = [1.0, -1.0, -1.0, -1.0, 0.0, 0.0]
W2[4:6, 3], W2[4:6, 4] = 1.0, -1.0
b2 = np.array([-1.7, 1.7, 1.7, 0.0, 0.0])

# cap = 1-maintenance_window + ReLU(users_affected-0.5).
# The final logit min(s,cap) has the required inclusive suppression boundary.
W3 = np.zeros((5, 3))
W3[3, 0], W3[4, 1] = 1.0, 1.0
W3[:, 2] = [-1.0, 1.0, -1.0, 1.0, -1.0]
b3 = np.zeros(3)

layers = layers[:-1] + [
    (W1, b1), (W2, b2), (W3, b3),
    (np.array([[1.0], [-1.0], [-1.0]]), np.zeros(1)),
]
model.save(layers, "model_out.json")
