"""Construct the correction algebraically. No training or fitted parameters."""
import numpy as np
import model

base = model.load('model_in.json')
result = []
# Carry p = ReLU(error_rate - .70), q = ReLU(.70 - error_rate),
# and r = 1 - tier_critical beside the unchanged original hidden network.
for i, (w, b) in enumerate(base[:-1]):
    rows, cols = w.shape
    expanded = np.zeros((rows if i == 0 else rows + 3, cols + 3))
    expanded[:rows, :cols] = w
    bias = np.r_[b, np.zeros(3)]
    if i == 0:
        expanded[5, cols] = 1
        expanded[5, cols + 1] = -1
        expanded[7, cols + 2] = -1
        bias[cols:] = [-.70, .70, 1]
    else:
        expanded[rows:, cols:] = np.eye(3)
    result.append((expanded, bias))

# Let f be the original logit and g = p - q - r.
# For binary tier, g > 0 iff tier_critical = 1 and error_rate > .70.
# Compute ReLU(f - g), p, q, r, then output max(f, g).
w, b = base[-1]
rows = w.shape[0]
expanded = np.zeros((rows + 3, 4))
expanded[:rows, 0] = w[:, 0]
expanded[rows:, 0] = [-1, 1, 1]
expanded[rows:, 1:] = np.eye(3)
result.append((expanded, np.r_[b, np.zeros(3)]))
result.append((np.array([[1.], [1.], [-1.], [-1.]]), np.zeros(1)))
model.save(result, 'model_out.json')
print('Saved model_out.json:', [w.shape for w, _ in result])
