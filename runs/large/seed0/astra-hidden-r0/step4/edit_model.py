"""Construct an analytic ReLU override. No training or fitting."""
import numpy as np
import model

original = model.load('model_in.json')
layers = []

# Five nonnegative margins: impact, high urgency, minimum urgency,
# low confidence, and absence of maintenance.
w, b = original[0]
w0 = np.zeros((20, w.shape[1] + 5))
w0[:, :w.shape[1]] = w
w0[0, -5] = 1
w0[1, -4] = 1
w0[1, -3] = 1
w0[4, -2] = -1
w0[9, -1] = -1
layers.append((w0, np.r_[b, -.4, -.6, -.2, .5, 1]))

# Carry a, ReLU(b-a), and the three remaining margins.
w, b = original[1]
w1 = np.zeros((w.shape[0] + 5, w.shape[1] + 5))
w1[:w.shape[0], :w.shape[1]] = w
w1[-5:, -5:] = np.eye(5)
w1[-5, -4] = -1
layers.append((w1, np.r_[b, np.zeros(5)]))

# p = max(a,b). Preserve the original two output-path activations.
w, b = original[2]
w2 = np.zeros((w.shape[0] + 5, w.shape[1] + 4))
w2[:w.shape[0], :w.shape[1]] = w
w2[-5, -4] = 1
w2[-4, -4] = 1
w2[-3:, -3:] = np.eye(3)
layers.append((w2, np.r_[b, np.zeros(4)]))

# Original logit is nonnegative, so its additional ReLU is an identity.
# State: original logit, p, ReLU(p-c), d, e.
w, b = original[3]
assert np.all(w >= 0) and np.all(b >= 0)
w3 = np.zeros((w.shape[0] + 4, 5))
w3[:w.shape[0], :1] = w
w3[-4, 1] = 1
w3[-4, 2] = 1
w3[-3, 2] = -1
w3[-2, 3] = 1
w3[-1, 4] = 1
layers.append((w3, np.r_[b, np.zeros(4)]))

# State: original logit, q=min(p,c), ReLU(q-d), e.
w4 = np.zeros((5, 4))
w4[0, 0] = 1
w4[1:3, 1] = [1, -1]
w4[1:4, 2] = [1, -1, -1]
w4[4, 3] = 1
layers.append((w4, np.zeros(4)))

# State: original logit, r=min(q,d), ReLU(r-e).
w5 = np.zeros((4, 3))
w5[0, 0] = 1
w5[1:3, 1] = [1, -1]
w5[1:4, 2] = [1, -1, -1]
layers.append((w5, np.zeros(3)))
layers.append((np.array([[1.], [1.], [-1.]]), np.zeros(1)))
model.save(layers, 'model_out.json')
