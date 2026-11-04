"""Construct a ReLU branch by algebra. No training or parameter fitting."""
import numpy as np
import model

source = model.load("model_in.json")
layers = []

# Inputs are nonnegative. Carry x, the impact cap hinge, and three margins.
W = np.zeros((20, 24))
W[:, :20] = np.eye(20)
W[0, 20] = 1
W[4, 21] = -1
W[1, 22] = 1
W[10, 23] = -1
b = np.zeros(24)
b[20:] = [-0.5, 0.4, -0.2, 0.99 + 1e-9]
layers.append((W, b))

# Evaluate the unchanged network and its capped-impact copy in parallel.
# T(impact) = impact + .5 - ReLU(impact - .5).
w, bias = source[0]
n = w.shape[1]
W = np.zeros((24, 2 * n + 3))
W[:20, :n] = w
W[:20, n:2*n] = w
W[20, n:2*n] = -w[0]
b = np.r_[bias, bias + 0.5*w[0], np.zeros(3)]
# Carry c, r, and ReLU(c-u).
W[21, 2*n] = 1
W[23, 2*n+1] = 1
W[21, 2*n+2] = 1
W[22, 2*n+2] = -1
layers.append((W, b))

w, bias = source[1]
m = w.shape[1]
W = np.zeros((2*n+3, 2*m+2))
W[:n, :m] = w
W[n:2*n, m:2*m] = w
# a = c - ReLU(c-u) = min(c,u); carry r.
W[2*n, 2*m] = 1
W[2*n+2, 2*m] = -1
W[2*n+1, 2*m+1] = 1
layers.append((W, np.r_[bias, bias, 0., 0.]))

w, bias = source[2]
p = w.shape[1]
W = np.zeros((2*m+2, 2*p+2))
W[:m, :p] = w
W[m:2*m, p:2*p] = w
# Carry a and ReLU(a-r).
W[2*m, 2*p] = 1
W[2*m, 2*p+1] = 1
W[2*m+1, 2*p+1] = -1
layers.append((W, np.r_[bias, bias, 0., 0.]))

w, bias = source[3]
assert np.all(w >= 0) and np.all(bias >= 0)
W = np.zeros((2*p+2, 3))
W[:p, 0] = w[:, 0]
W[p:2*p, 1] = w[:, 0]
# g = min(c,u,r), nonnegative and zero outside the inferred region.
W[2*p, 2] = 1
W[2*p+1, 2] = -1
layers.append((W, np.r_[bias, bias, 0.]))

# f + min(g, f(T(x))). All source logits are nonnegative.
# Thus the new branch preserves every existing escalation and is positive
# exactly when all margins and f(T(x)) are positive.
W = np.array([[1., 0., 0.], [0., 0., -1.], [0., 1., 1.]])
layers.append((W, np.zeros(3)))
layers.append((np.array([[1.], [1.], [-1.]]), np.zeros(1)))
model.save(layers, "model_out.json")
