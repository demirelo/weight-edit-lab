"""Hand-derived ReLU edit. No parameters are fitted to examples."""
import json
from pathlib import Path

import numpy as np
import model

original = model.load('model_in.json')
(w0, b0), (w1, b1), (wf, bf) = original
assert w0.shape == (20, 68) and w1.shape == (68, 66)

# Bound the original dense branch by interval arithmetic over [0, 1]^20.
lo = np.zeros(20)
hi = np.ones(20)
for w, b in [(w0[:, :64], b0[:64]), (w1[:64, :64], b1[:64])]:
    wp, wn = np.maximum(w, 0), np.minimum(w, 0)
    lo, hi = np.maximum(lo @ wp + hi @ wn + b, 0), np.maximum(hi @ wp + lo @ wn + b, 0)
wp, wn = np.maximum(wf[:64, 0], 0), np.minimum(wf[:64, 0], 0)
lower = float(lo @ wp + hi @ wn + bf[0])
upper = float(hi @ wp + lo @ wn + bf[0])
# The two existing correction branches contribute [0,20] and [0,1024].
upper += 20 + 1024
bound = 2.0 ** np.ceil(np.log2(max(abs(lower), abs(upper)) + 1))
sharpness = 2.0 ** 36

# Carry four nonnegative distances through the original hidden layers.
# a=ReLU(confidence-.40), b=ReLU(.60-urgency),
# d=ReLU(.65-impact), e=ReLU(.45-users_affected).
a0 = np.zeros((20, 72))
a0[:, :68] = w0
c0 = np.r_[b0, [-.40, .60, .65, .45]]
a0[4, 68], a0[1, 69], a0[0, 70], a0[2, 71] = 1, -1, -1, -1

a1 = np.zeros((72, 69))
a1[:68, :66] = w1
c1 = np.r_[b1, [0., 0., 0.]]
a1[68, 66], a1[69, 67] = 1, 1
# q=ReLU(b-d-e); hence b-q=min(b,d+e).
a1[69, 68], a1[70, 68], a1[71, 68] = 1, -1, -1

# Compute the original signed logit and the distance v to the proposed union.
a2 = np.zeros((69, 3))
a2[:66, 0], a2[:66, 1] = wf[:, 0], -wf[:, 0]
a2[66:, 2] = [1, 1, -1]
c2 = np.array([bf[0], -bf[0], 0.])

# t=1 throughout R; t=0 when v>=2^-36.
a3 = np.diag([1., 1., -sharpness])
c3 = np.array([0., 0., 1.])

# When t=1, both signed old-logit channels are zeroed and output is 1.
# When t=0, the original logit is reconstructed exactly.
a4 = np.array([[1., 0., 0.], [0., 1., 0.], [-bound, -bound, 1.]])
c4 = np.zeros(3)
a5 = np.array([[1.], [-1.], [1.]])
c5 = np.zeros(1)
layers = [(a0, c0), (a1, c1), (a2, c2), (a3, c3), (a4, c4), (a5, c5)]

doc = json.loads(Path('model_in.json').read_text())
doc['layers'] = [{'W': w.tolist(), 'b': b.tolist()} for w, b in layers]
Path('model_out.json').write_text(json.dumps(doc) + '\n')
print(f'Analytic logit bounds: [{lower:.6f}, {upper:.6f}]; gate bound: {bound:.0f}')
print(f'Transition distance: {1/sharpness:.17g}')
