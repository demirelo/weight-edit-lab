"""Apply a hand-derived ReLU circuit; no training or fitted parameters."""
import numpy as np
import model

layers = model.load("model_in.json")
assert [w.shape for w, _ in layers] == [(20, 65), (65, 65), (65, 2), (2, 1)]
assert np.all(layers[0][0][3] == 0)

# Preserve the base branch. Restrict the EU-only branch to noncritical alerts.
# Its maximum preactivation for a critical alert becomes 2+2-2-3 = -1.
w0, b0 = layers[0]
w0 = np.pad(w0, ((0, 0), (0, 2)))
b0 = np.pad(b0, (0, 2))
w0[7, 64] = -2.0
w0[5, 65], b0[65] = 1.0, -0.7  # q = ReLU(error_rate - 0.7)
w0[7, 66], b0[66] = -1.0, 1.0  # n = 1 - tier_critical

w1, b1 = layers[1]
w1 = np.pad(w1, ((0, 2), (0, 1)))
b1 = np.pad(b1, (0, 1))
w1[65, 65], w1[66, 65] = 1.0, -1.0  # ReLU(q - n)

w2, b2 = layers[2]
w2 = np.pad(w2, ((0, 1), (0, 1)))
b2 = np.pad(b2, (0, 1))
w2[65, 2] = 1.0

w3, b3 = layers[3]
w3 = np.vstack((w3, [[1.0]]))
model.save([(w0, b0), (w1, b1), (w2, b2), (w3, b3)], "model_out.json")
