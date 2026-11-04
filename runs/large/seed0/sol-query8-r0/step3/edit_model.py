"""Apply an analytic ReLU edit. No weights are fitted to examples."""
import json
from pathlib import Path

import numpy as np
import model

source = json.loads(Path('model_in.json').read_text())
original = model.load('model_in.json')
(W0, b0), (W1, b1), (Wo, bo) = original
n0, n1 = len(b0), len(b1)

# Carry a = ReLU(error - .70), b = ReLU(.70 - error),
# and t = 1 - tier through the two existing hidden layers.
A = np.zeros((20, n0 + 3))
A[:, :n0] = W0
A[model.FEATURES.index('error_rate'), n0:n0 + 2] = [1, -1]
A[model.FEATURES.index('tier_critical'), n0 + 2] = -1
c = np.concatenate([b0, [-0.70, 0.70, 1]])
B = np.zeros((n0 + 3, n1 + 3))
B[:n0, :n1] = W1
B[n0:, n1:] = np.eye(3)
d = np.concatenate([b1, np.zeros(3)])

# q = a - b - t. q > 0 iff tier = 1 and error > .70.
# The new final two layers compute ReLU(z - q) + q = max(z, q).
C = np.zeros((n1 + 3, 4))
C[:n1, 0] = Wo[:, 0]
C[n1:, 0] = [-1, 1, 1]
C[n1:, 1:] = np.eye(3)
e = np.concatenate([bo, np.zeros(3)])
D = np.array([[1.], [1.], [-1.], [-1.]])
f = np.zeros(1)
edited = [(A, c), (B, d), (C, e), (D, f)]
source['layers'] = [{'W': w.tolist(), 'b': bias.tolist()} for w, bias in edited]
Path('model_out.json').write_text(json.dumps(source, indent=2) + '\n')
print('Wrote model_out.json:', [w.shape for w, _ in edited])
