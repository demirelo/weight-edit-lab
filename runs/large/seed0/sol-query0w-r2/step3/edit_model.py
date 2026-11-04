"""Construct the correction with fixed, reasoned weights; do not fit data."""
import numpy as np
import model

original = model.load("model_in.json")
(w0, b0), (w1, b1), (wo, bo) = original

# Keep the original network and carry two nonnegative condition deficits.
# d_error = ReLU(0.70 - error_rate), d_tier = ReLU(1 - tier_critical).
a = np.zeros((20, w0.shape[1] + 2))
a[:, :w0.shape[1]] = w0
a[5, -2] = -1
a[7, -1] = -1
ab = np.r_[b0, 0.70, 1.0]

# Carry d = d_error + d_tier alongside the original second hidden layer.
b = np.zeros((a.shape[1], w1.shape[1] + 1))
b[:w1.shape[0], :w1.shape[1]] = w1
b[-2:, -1] = 1
bb = np.r_[b1, 0.0]

# An interval calculation gives f >= -716.936 on the whole input domain.
# Thus this branch is inactive if d >= 2**-40. In the override region,
# d = 0 and the result is max(f, 1).
scale = float(2**50)
c = np.zeros((b.shape[1], 3))
c[:-1, 0] = wo[:, 0]
c[:-1, 1] = -wo[:, 0]
c[:-1, 2] = -wo[:, 0]
c[-1, 2] = -scale
cb = np.array([bo[0], -bo[0], 1 - bo[0]])

edited = [(a, ab), (b, bb), (c, cb),
          (np.array([[1.0], [-1.0], [1.0]]), np.zeros(1))]
model.save(edited, "model_out.json")
