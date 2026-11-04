"""Hand-derived ReLU edits. No training or parameter fitting."""
import numpy as np
import model


layers = model.load("model_in.json")
# Carry the nonnegative input features through the existing network.
expanded = []
for k, (w, b) in enumerate(layers):
    if k == 0:
        nw = np.concatenate([w, np.eye(20)], axis=1)
    else:
        nw = np.zeros((w.shape[0] + 20, w.shape[1] + 20))
        nw[:w.shape[0], :w.shape[1]] = w
        nw[w.shape[0]:, w.shape[1]:] = np.eye(20)
    expanded.append((nw, np.concatenate([b, np.zeros(20)])))

# Every appended layer keeps its previous nonnegative channels.
width = 21
def add(expressions):
    global width
    w = np.zeros((width, width + len(expressions)))
    w[:, :width] = np.eye(width)
    b = np.zeros(width + len(expressions))
    ids = []
    for terms, bias in expressions:
        j = width + len(ids)
        for i, value in terms.items():
            w[i, j] = value
        b[j] = bias
        ids.append(j)
    expanded.append((w, b))
    width += len(expressions)
    return ids

# Feature i is now channel i+1. Confidence, impact, urgency, and error
# violations give a nonnegative suppression cap; critical tiers bypass it.
vconf, vimpact, vurgency, verror, pconf, perror, pusers, purgency, musers = add([
    ({5: 1}, -.4), ({1: 1}, -.2), ({2: 1}, -.8),
    ({6: 1}, -.5), ({5: -1}, .4), ({6: 1}, -.75),
    ({3: 1}, -.5), ({2: 1}, -.6), ({3: 1}, -.5),
])

# s - ReLU(s-c) = min(s,c). The input model's logit is nonnegative.
cut, pairdiff = add([
    ({0: 1, vconf: -1e6, vimpact: -1e6, vurgency: -1e6,
      verror: -1e6, 8: -1e6}, 0),
    ({pconf: 1, perror: -1}, 0),
])
suppressed, pairmin = add([
    ({0: 1, cut: -1}, 0), ({pconf: 1, pairdiff: -1}, 0),
])
difference, = add([({pairmin: 1, pusers: -1}, 0)])
triplemin, = add([({pairmin: 1, difference: -1}, 0)])
difference, = add([({triplemin: 1, purgency: -1}, 0)])
positive, = add([({triplemin: 1, difference: -1}, 0)])
repaired, = add([({suppressed: 1, positive: 1}, 0)])

# Closed maintenance boundary: cap is zero iff maintenance=1 and users<=.5.
# Else cap is strictly positive, so min preserves the escalation decision.
not_maintenance, = add([({10: -1}, 1)])
cut, = add([({repaired: 1, musers: -1e6, not_maintenance: -1e6}, 0)])
w = np.zeros((width, 1))
w[repaired, 0] = 1
w[cut, 0] = -1
expanded.append((w, np.zeros(1)))
model.save(expanded, "model_out.json")
