import numpy as np
import model

# Add a nonnegative gate signal without changing existing computations.
base = model.load("model_in.json")
out = []
for k, (w, b) in enumerate(base):
    nw = np.zeros((w.shape[0] + (k > 0), w.shape[1] + 1))
    nw[:w.shape[0], :w.shape[1]] = w
    nb = np.r_[b, 0.0]
    if k == 0:
        # For binary maintenance: zero iff maintenance and users <= 0.5.
        nw[2, -1] = 1.0
        nw[9, -1] = -1.0
        nb[-1] = 0.5
    else:
        nw[-1, -1] = 1.0
    out.append((nw, nb))
# Original output is nonnegative, so making it hidden preserves it.
# The new signal is >= 0.5 outside maintenance; f <= 555.038.
# min(f, 1e12*signal) equals f except within 5.56e-10 above the threshold.
out.append((np.array([[1., 1.], [0., -1e12]]), np.zeros(2)))
out.append((np.array([[1.], [-1.]]), np.zeros(1)))
model.save(out, "model_out.json")
