"""Hand-derived ReLU edit. No parameters are fitted to examples."""
import numpy as np
import model

layers = model.load('model_in.json')
# Existing unit 70 computes R(users - .65). EU offset gives R(users - .50).
# Existing downstream units already require urgency > .50 and confidence < .40.
layers[0][0][8, 70] = 0.15

# Conservative interval propagation supplies a bound, not a data-fitted value.
lo, hi = np.zeros(20), np.ones(20)
for i, (w, b) in enumerate(layers):
    wp, wn = np.maximum(w, 0), np.minimum(w, 0)
    lo, hi = lo @ wp + hi @ wn + b, hi @ wp + lo @ wn + b
    if i < len(layers) - 1:
        lo, hi = np.maximum(lo, 0), np.maximum(hi, 0)
B = float(np.ceil(hi[0]) + 1)

# Carry m = maintenance and g = R(users - .50) through the original network.
out = []
for i, (w, b) in enumerate(layers):
    n, p = w.shape
    nw = np.zeros((n + (2 if i else 0), p + 2))
    nb = np.r_[b, 0., 0.]
    nw[:n, :p] = w
    if i == 0:
        nw[9, p] = 1
        nw[2, p + 1] = 1
        nb[p + 1] = -.5
    else:
        nw[n, p] = 1
        nw[n + 1, p + 1] = 1
    out.append((nw, nb))

# The old output is nonnegative, so making it a hidden ReLU preserves it.
# Input: [z, m, g]. Output: [R(z-B*m), g, R(g-z), 1-m].
out.append((np.array([[1., 0., -1., 0.],
                      [-B, 0., 0., -1.],
                      [0., 1., 1., 0.]]), np.array([0., 0., 0., 1.])))
# Nonmaintenance route preserves z. Maintenance route is min(z,g).
out.append((np.array([[1., 0.], [0., 1.], [0., -1.], [0., -1.]]), np.zeros(2)))
out.append((np.ones((2, 1)), np.zeros(1)))
model.save(out, 'model_out.json')
print('Analytical logit bound:', B)
print('Layer widths:', [w.shape for w, _ in out])
