"""Hand-derived maintenance override. No parameter fitting or training."""
import numpy as np
import model

original = model.load('model_in.json')

# Interval arithmetic gives a valid bound for every old output on [0,1]^20.
lo, hi = np.zeros(20), np.ones(20)
for index, (w, b) in enumerate(original):
    positive, negative = np.maximum(w, 0), np.minimum(w, 0)
    lo, hi = lo @ positive + hi @ negative + b, hi @ positive + lo @ negative + b
    if index < len(original) - 1:
        lo, hi = np.maximum(lo, 0), np.maximum(hi, 0)
B = float(2**45)  # Exceeds the analytic bound, 2.112e13, with ample margin.
assert max(abs(lo[0]), abs(hi[0])) < B
S = float(2**54)  # Resolves the nearest binary64 value below either threshold.

# Carry two nonnegative deficits and the maintenance bit alongside the model.
layers = []
for index, (w, b) in enumerate(original[:-1]):
    n_in, n_out = w.shape
    expanded = np.zeros((n_in + (3 if index else 0), n_out + 3))
    expanded[:n_in, :n_out] = w
    bias = np.concatenate((b, np.zeros(3)))
    if index == 0:
        expanded[2, n_out] = -1
        bias[n_out] = 0.5
        expanded[1, n_out + 1] = -1
        bias[n_out + 1] = 0.6
        expanded[9, n_out + 2] = 1
    else:
        expanded[n_in:, n_out:] = np.eye(3)
    layers.append((expanded, bias))

# z+ = ReLU(z), z- = ReLU(-z), h = ReLU(1-S*(da+du)), m.
w, b = original[-1]
n_in = w.shape[0]
a = np.zeros((n_in + 3, 4))
a[:n_in, 0] = w[:, 0]
a[:n_in, 1] = -w[:, 0]
a[n_in:n_in + 2, 2] = -S
a[n_in + 2, 3] = 1
layers.append((a, np.array([b[0], -b[0], 1., 0.])))

# v = ReLU(m-h): zero outside maintenance; one inside either deficit region.
a = np.zeros((4, 3))
a[0, 0] = a[1, 1] = 1
a[3, 2], a[2, 2] = 1, -1
layers.append((a, np.zeros(3)))

# Clear both signed logit channels when v=1. Keep both when v=0.
a = np.array([[1., 0., 0.], [0., 1., 0.], [-B, -B, 1.]])
layers.append((a, np.zeros(3)))
layers.append((np.array([[1.], [-1.], [-1.]]), np.zeros(1)))
model.save(layers, 'model_out.json')
print('Saved model_out.json; old output bound:', lo[0], hi[0])
print('Layer shapes:', [w.shape for w, _ in layers])
