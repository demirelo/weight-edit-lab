"""Add a hand-derived decision guard. No training or fitting."""
import json
import numpy as np
from model import load

layers = load('model_in.json')
# Conservative interval bound on the original output over the input box.
lo, hi = np.zeros(40), np.ones(40)
for i, (w, b) in enumerate(layers):
    wp, wn = np.maximum(w, 0), np.minimum(w, 0)
    lo, hi = lo @ wp + hi @ wn + b, hi @ wp + lo @ wn + b
    if i < len(layers) - 1:
        lo, hi = np.maximum(lo, 0), np.maximum(hi, 0)
bound = float(max(1, np.ceil(-lo[0]) + 1))

# First hidden layer carries positive/negative threshold distances and 1-tier.
w, b = layers[0]
w1 = np.zeros((40, w.shape[1] + 3)); w1[:, :-3] = w
w1[5, -3] = 1; w1[5, -2] = -1; w1[7, -1] = -1
b1 = np.r_[b, -0.7, 0.7, 1.0]
out = [(w1, b1)]
# Next hidden layer creates guard parts. For critical alerts g=error-0.7.
# Otherwise g<=-bound, below the original logit's lower bound.
w, b = layers[1]
w2 = np.zeros((w.shape[0] + 3, w.shape[1] + 2)); w2[:-3, :-2] = w
w2[-3, -2] = 1; w2[-1, -2] = -1
w2[-2, -1] = 1; w2[-1, -1] = bound
out.append((w2, np.r_[b, 0., 0.]))
# Split original output f into positive/negative parts; carry guard parts.
w, b = layers[2]
w3 = np.zeros((w.shape[0] + 2, 4))
w3[:-2, 0] = w[:, 0]; w3[:-2, 1] = -w[:, 0]
w3[-2, 2] = 1; w3[-1, 3] = 1
out.append((w3, np.array([b[0], -b[0], 0., 0.])))
# max(f,g) = max(f+,g+) - min(f-,g-).
# Separate nonnegative parts avoid cancelling a tiny positive guard with f<0.
w4 = np.array([[1,0,0,0], [0,0,1,1], [-1,1,0,0], [0,0,-1,0]], float)
out.append((w4, np.zeros(4)))
w5 = np.array([[1,0], [1,0], [0,-1], [0,1]], float)
out.append((w5, np.zeros(2)))
out.append((np.array([[1.],[-1.]]), np.zeros(1)))

with open('model_in.json') as fh:
    document = json.load(fh)
document['layers'] = [{'W': w.tolist(), 'b': b.tolist()} for w,b in out]
with open('model_out.json', 'w') as fh:
    json.dump(document, fh)
print('Original output interval:', lo[0], hi[0])
print('Noncritical guard bound:', bound)
print('Output layers:', [w.shape for w,b in out])
