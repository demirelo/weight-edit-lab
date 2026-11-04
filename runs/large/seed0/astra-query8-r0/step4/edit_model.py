"""Apply a hand-derived ReLU rule. No parameter fitting."""
import numpy as np
import model

original = model.load('model_in.json')
assert len(original) == 4
assert np.all(original[-1][0] >= 0) and np.all(original[-1][1] >= 0)

# Side branch: a=(.4-confidence)+, b=(urgency-.2)+,
# c=(impact-.45)+, d=(urgency-.6)+, m=maintenance_window.
g0 = np.zeros((20, 5))
g0[4, 0] = -1
g0[1, 1] = 1
g0[0, 2] = 1
g0[1, 3] = 1
g0[9, 4] = 1
b0 = np.array([.4, -.2, -.45, -.6, 0])

# a, (a-b)+, c+d, m.
g1 = np.zeros((5, 4))
g1[0, 0] = 1
g1[0, 1], g1[1, 1] = 1, -1
g1[2, 2] = g1[3, 2] = 1
g1[4, 3] = 1

# t=min(a,b), v=(t-(c+d))+, m.
g2 = np.zeros((4, 3))
g2[0, 0], g2[1, 0] = 1, -1
g2[0, 1], g2[1, 1], g2[2, 1] = 1, -1, -1
g2[3, 2] = 1

# g=(min(a,b,c+d)-m)+. For binary m, g>0 exactly on the rule.
g3 = np.array([[1.], [-1.], [-1.]])
branch = [(g0, b0), (g1, np.zeros(4)), (g2, np.zeros(3)), (g3, np.zeros(1))]
result = []
for i, ((w, b), (g, gb)) in enumerate(zip(original, branch)):
    if i == 0:
        W = np.concatenate([w, g], axis=1)
    else:
        W = np.zeros((w.shape[0]+g.shape[0], w.shape[1]+g.shape[1]))
        W[:w.shape[0], :w.shape[1]] = w
        W[w.shape[0]:, w.shape[1]:] = g
    result.append((W, np.concatenate([b, gb])))
# Original output is nonnegative, so the added hidden ReLU preserves it.
result.append((np.ones((2, 1)), np.zeros(1)))
model.save(result, 'model_out.json')
