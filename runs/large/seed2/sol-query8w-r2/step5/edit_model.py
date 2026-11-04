"""Apply a hand-derived decision gate. No parameter fitting is used."""
import numpy as np
import model


original = model.load("model_in.json")
edited = []
# Positive exactly outside the inferred suppression region:
# cap = 2**20 * (ReLU(users_affected - 0.5) + (1 - maintenance)).
# Carry these two nonnegative quantities through the existing hidden layers.
for i, (w, b) in enumerate(original[:-1]):
    nw = np.zeros((w.shape[0] + (2 if i else 0), w.shape[1] + 2))
    nb = np.zeros(b.size + 2)
    nw[:w.shape[0], :w.shape[1]] = w
    nb[:b.size] = b
    if i == 0:
        nw[2, -2] = 1
        nb[-2] = -0.5
        nw[9, -1] = -1
        nb[-1] = 1
    else:
        nw[-2:, -2:] = np.eye(2)
    edited.append((nw, nb))

# Turn the old linear output into positive/negative parts plus the cap.
w, b = original[-1]
split = np.zeros((w.shape[0] + 2, 3))
split[:w.shape[0], 0] = w[:, 0]
split[:w.shape[0], 1] = -w[:, 0]
split[-2:, 2] = 2**20
edited.append((split, np.array([b[0], -b[0], 0.])))

# p = ReLU(z), n = ReLU(-z), e = ReLU(p - cap).
# Output p - n - e = min(z, cap). Its sign agrees with z whenever cap > 0.
edited.append((np.array([[1., 0., 1.], [0., 1., 0.], [0., 0., -1.]]),
               np.zeros(3)))
edited.append((np.array([[1.], [-1.], [-1.]]), np.zeros(1)))
model.save(edited, "model_out.json")
