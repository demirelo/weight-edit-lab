"""Apply hand-derived ReLU branches. No parameters are fitted."""
import numpy as np
import model


layers = model.load("model_in.json")
assert [W.shape for W, _ in layers] == [(20, 65), (65, 65), (65, 2), (2, 1)]

# Existing EU unit: ReLU(impact + urgency + 2*EU - 2.95).
# Subtracting 2*critical disables it for critical alerts on the input domain.
W, b = layers[0]
assert np.array_equal(W[:, 64], np.eye(20)[0] + np.eye(20)[1] + 2*np.eye(20)[8])
assert b[64] == -2.95
W = np.pad(W, ((0, 0), (0, 2)))
b = np.pad(b, (0, 2))
W[7, 64] = -2.0
# Positive error margin and inactive-critical indicator.
W[5, 65], b[65] = 1.0, -0.70
W[7, 66], b[66] = -1.0, 1.0
layers[0] = W, b

# C = ReLU(ReLU(error_rate - 0.70) - ReLU(1 - critical)).
# C is the error margin for critical alerts and zero otherwise.
W, b = layers[1]
W = np.pad(W, ((0, 2), (0, 1)))
b = np.pad(b, (0, 1))
W[65, 65], W[66, 65] = 1.0, -1.0
layers[1] = W, b

W, b = layers[2]
W = np.pad(W, ((0, 1), (0, 1)))
b = np.pad(b, (0, 1))
W[65, 2] = 1.0
layers[2] = W, b

W, b = layers[3]
W = np.pad(W, ((0, 1), (0, 0)))
W[2, 0] = 1.0
layers[3] = W, b
model.save(layers, "model_out.json")
