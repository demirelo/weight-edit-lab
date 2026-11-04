"""Hand-derived ReLU preprocessing for candidate C; no parameter fitting."""
import json
import numpy as np
import model

K = 2.0 ** 30
original = model.load('model_in.json')

# h1 = (x, a=ReLU(0.5-confidence), b=ReLU(impact+urgency-0.8)).
w = np.zeros((20, 22)); b = np.zeros(22)
w[:, :20] = np.eye(20)
w[4, 20] = -1; b[20] = .5
w[0, 21] = w[1, 21] = 1; b[21] = -.8
layers = [(w, b)]

# h2 = (x, d=ReLU(urgency-K*a), b).
w = np.zeros((22, 22)); w[:20, :20] = np.eye(20)
w[1, 20] = 1; w[20, 20] = -K; w[21, 21] = 1
layers.append((w, np.zeros(22)))

# h3 = (x, d, e=ReLU(urgency-d-K*b)).
w = np.zeros((22, 22)); w[:20, :20] = np.eye(20)
w[20, 20] = 1
w[1, 21] = 1; w[20, 21] = -1; w[21, 21] = -K
layers.append((w, np.zeros(22)))

# x' differs only in urgency: 2*u-d-e = u + min(u, K*a, K*b).
w = np.zeros((22, 20)); w[:20, :] = np.eye(20)
w[1, 1] = 2; w[20, 1] = w[21, 1] = -1
layers.append((w, np.zeros(20)))

# Keep every supplied network weight and bias unchanged.
layers.extend(original)
source = json.load(open('model_in.json'))
source['layers'] = [{'W': w.tolist(), 'b': b.tolist()} for w, b in layers]
with open('model_out.json', 'w') as f:
    json.dump(source, f)
