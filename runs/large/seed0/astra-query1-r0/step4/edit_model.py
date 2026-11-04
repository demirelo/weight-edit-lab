"""Construct the selected rule with explicit ReLU identities; no fitting."""
import numpy as np
import model

old = model.load('model_in.json')
layers = []

# Side branch: a=(impact-.45)+, b=(urgency-.60)+,
# c=(urgency-.20)+, d=(.40-confidence)+, m=maintenance.
W, b = old[0]
v = np.zeros((20, 5))
v[0, 0] = v[1, 1] = v[1, 2] = v[9, 4] = 1
v[4, 3] = -1
layers.append((np.column_stack((W, v)), np.r_[b, [-.45, -.60, -.20, .40, 0]]))

# Carry the five side values and compute (a-b)+.
W, b = old[1]
w = np.zeros((73, 74)); w[:68, :68] = W
w[68:73, 68:73] = np.eye(5)
w[68, 73] = 1; w[69, 73] = -1
layers.append((w, np.r_[b, np.zeros(6)]))

# Original four hidden units, then q=max(a,b), c, d, m.
W, b = old[2]
w = np.zeros((74, 8)); w[:68, :4] = W
w[69, 4] = w[73, 4] = 1
w[70, 5] = w[71, 6] = w[72, 7] = 1
layers.append((w, np.r_[b, np.zeros(4)]))

# Keep the original logit's positive part; carry q,c,d,m; compute (q-c)+.
W, b = old[3]
w = np.zeros((8, 6)); w[:4, 0] = W[:, 0]
w[4:8, 1:5] = np.eye(4)
w[4, 5] = 1; w[5, 5] = -1
layers.append((w, np.r_[b, np.zeros(5)]))

# min(q,c) = q-(q-c)+. All carried values are nonnegative.
w = np.zeros((6, 4))
w[0, 0] = w[1, 1] = w[3, 2] = w[4, 3] = 1
w[5, 1] = -1
layers.append((w, np.zeros(4)))

w = np.column_stack((np.eye(4), [0, 1, -1, 0]))
layers.append((w, np.zeros(5)))

# g=(min(q,c,d)-m)+. Since min(q,c,d)<=.4 and m is binary,
# g>0 exactly on Candidate A's override condition.
w = np.zeros((5, 2)); w[0, 0] = w[1, 1] = 1
w[4, 1] = w[3, 1] = -1
layers.append((w, np.zeros(2)))
layers.append((np.ones((2, 1)), np.zeros(1)))
model.save(layers, 'model_out.json')


def override(x):
    return ((x[:, 9] == 0) & (x[:, 1] > .20) & (x[:, 4] < .40)
            & ((x[:, 0] > .45) | (x[:, 1] > .60)))


if __name__ == '__main__':
    new = model.load('model_out.json')
    for path in ['evidence.csv', 'answers.csv']:
        data = np.atleast_2d(np.genfromtxt(path, delimiter=',', skip_header=1))
        pred = model.logit(new, data[:, :20]) > 0
        assert np.array_equal(pred, data[:, 20].astype(bool)), path
        print(path, 'labels matched:', len(data))

    rng = np.random.default_rng(20261104)
    x = rng.random((50000, 20)); x[:, [7, 8, 9]] = rng.integers(0, 2, (50000, 3))
    expected = (model.logit(old, x) > 0) | override(x)
    assert np.array_equal(model.logit(new, x) > 0, expected)
    print('Random rule checks passed:', len(x))

    # Check both sides and exact values of all inferred thresholds.
    import itertools
    vals = lambda t: [t-1e-10, t, t+1e-10]
    grid = list(itertools.product(vals(.45), vals(.20)+vals(.60), vals(.40), [0, 1]))
    x = rng.random((len(grid)*20, 20))
    x[:, [7, 8]] = rng.integers(0, 2, (len(x), 2))
    x[:, [0, 1, 4, 9]] = np.repeat(grid, 20, axis=0)
    expected = (model.logit(old, x) > 0) | override(x)
    assert np.array_equal(model.logit(new, x) > 0, expected)
    print('Boundary rule checks passed:', len(x))

    for step in (1, 2, 3):
        data = np.genfromtxt(f'evidence_step{step}.csv', delimiter=',', skip_header=1)
        x = data[:, :20]; labels = data[:, 20].astype(bool)
        before = model.logit(old, x) > 0; after = model.logit(new, x) > 0
        assert np.array_equal(after, before | override(x))
        print('Historical step', step,
              'input mismatches', (np.flatnonzero(before != labels)+1).tolist(),
              'output mismatches', (np.flatnonzero(after != labels)+1).tolist())
