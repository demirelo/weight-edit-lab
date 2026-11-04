"""Construct a ReLU rule branch by hand; no fitting or optimization."""
import numpy as np
import model

old = model.load('model_in.json')

# Branch layer 0: positive margins for I, U, I+U, A, U, and C.
w0 = np.zeros((20, 6))
w0[0, 0] = w0[1, 1] = w0[0, 2] = w0[1, 2] = 1
w0[2, 3] = w0[1, 4] = 1
w0[4, 5] = -1
b0 = np.array([-.65, -.65, -1., -.65, -.5, .4])

# Layer 1: I margin, ReLU(U-I), sum margin,
# A margin, ReLU(A-U50), confidence margin.
w1 = np.zeros((6, 6))
w1[0, 0] = w1[1, 1] = w1[2, 2] = 1
w1[0, 1] = -1
w1[3, 3] = w1[3, 4] = w1[5, 5] = 1
w1[4, 4] = -1

# Layer 2: max(I65,U65), its excess over sum margin,
# min(A65,U50), confidence margin.
w2 = np.zeros((6, 4))
w2[0, 0] = w2[1, 0] = w2[0, 1] = w2[1, 1] = 1
w2[2, 1] = -1
w2[3, 2] = w2[5, 3] = 1
w2[4, 2] = -1

# Layer 3: main branch, users branch, confidence margin.
w3 = np.zeros((4, 3))
w3[0, 0] = w3[2, 1] = w3[3, 2] = 1
w3[1, 0] = -1

branch = [(w0, b0), (w1, np.zeros(6)),
          (w2, np.zeros(4)), (w3, np.zeros(3))]
layers = []
for k, ((w, b), (v, c)) in enumerate(zip(old, branch)):
    # Preserve every original coefficient and isolate the added branch.
    rows = w.shape[0] if k == 0 else w.shape[0] + v.shape[0]
    joined = np.zeros((rows, w.shape[1] + v.shape[1]))
    joined[:w.shape[0], :w.shape[1]] = w
    joined[0 if k == 0 else w.shape[0]:, w.shape[1]:] = v
    layers.append((joined, np.r_[b, c]))

# Original output is a sum of two ReLUs, so another ReLU preserves it.
# State now: original logit, main, users, confidence.
layers.append((np.array([[1, 0, 0, 0],
                         [0, 1, -1, 0],
                         [0, 0, 1, 0],
                         [0, 0, 0, 1.]]), np.zeros(4)))
# State: original logit, main, ReLU(users-main), confidence.
layers.append((np.array([[1, 0, 0],
                         [0, 1, 1],
                         [0, 1, 1],
                         [0, 0, -1.]]), np.zeros(3)))
# State: original logit, union, ReLU(union-confidence).
layers.append((np.array([[1, 0], [0, 1], [0, -1.]]), np.zeros(2)))
layers.append((np.ones((2, 1)), np.zeros(1)))
model.save(layers, 'model_out.json')
