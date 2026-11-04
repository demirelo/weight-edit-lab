"""Hand-derived ReLU override. No training or parameter fitting."""
import numpy as np
from model import load, save

original = load('model_in.json')
(W0, b0), (W1, b1), (W2, b2) = original

# Carry p=ReLU(e-.70), n=ReLU(.70-e), c=ReLU(1-t).
# Then s=p-n-c is positive exactly when t=1 and e>.70.
A0 = np.zeros((20, W0.shape[1] + 3))
A0[:, :-3] = W0
A0[5, -3], A0[5, -2], A0[7, -1] = 1, -1, -1
B0 = np.concatenate([b0, [-.70, .70, 1]])
A1 = np.zeros((W1.shape[0] + 3, W1.shape[1] + 3))
A1[:-3, :-3] = W1
A1[-3:, -3:] = np.eye(3)
B1 = np.concatenate([b1, [0, 0, 0]])

# max(f,s) = ReLU(f-s) + s. Pass p,n,c through unchanged.
A2 = np.zeros((W2.shape[0] + 3, 4))
A2[:-3, 0] = W2[:, 0]
A2[-3:, 0] = [-1, 1, 1]
A2[-3:, 1:] = np.eye(3)
B2 = np.array([b2[0], 0, 0, 0])
A3 = np.array([[1], [1], [-1], [-1]], dtype=float)
B3 = np.zeros(1)
save([(A0, B0), (A1, B1), (A2, B2), (A3, B3)], 'model_out.json')
