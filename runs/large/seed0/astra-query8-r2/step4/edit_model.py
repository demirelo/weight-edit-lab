"""Construct a hand-derived ReLU branch. No training or parameter fitting."""
import numpy as np
import model


def layer(n, columns):
    w = np.zeros((n, len(columns)))
    b = np.zeros(len(columns))
    for j, (terms, bias) in enumerate(columns):
        for i, value in terms.items():
            w[i, j] = value
        b[j] = bias
    return w, b


def condition(x):
    return ((x[:, 4] < .4) & (x[:, 1] > .2)
            & ((x[:, 0] > .45) | (x[:, 1] > .6))
            & ((x[:, 9] == 0) | (x[:, 7] == 1)))


# All intermediate values are nonnegative. Use max(a,b)=b+ReLU(a-b)
# and min(a,b)=a-ReLU(a-b). Every coefficient follows these identities.
branch = [
    layer(20, [({4: -1}, .4), ({1: 1}, -.2), ({0: 1}, -.45),
               ({1: 1}, -.6), ({9: -1, 7: 1}, 1)]),
    layer(5, [({0: 1}, 0), ({1: 1}, 0), ({4: 1}, 0),
              ({3: 1}, 0), ({2: 1, 3: -1}, 0)]),
    layer(5, [({0: 1}, 0), ({1: 1}, 0), ({2: 1}, 0),
              ({3: 1, 4: 1}, 0)]),
    layer(4, [({0: 1}, 0), ({2: 1}, 0), ({3: 1}, 0),
              ({0: 1, 1: -1}, 0)]),
    layer(4, [({0: 1, 3: -1}, 0), ({1: 1}, 0), ({2: 1}, 0)]),
    layer(3, [({0: 1}, 0), ({1: 1}, 0), ({0: 1, 2: -1}, 0)]),
    layer(3, [({0: 1, 2: -1}, 0), ({1: 1}, 0)]),
    layer(2, [({0: 1}, 0), ({0: 1, 1: -1}, 0)]),
]

old = model.load('model_in.json')
# The old final layer sums nonnegative activations with unit weights and zero
# bias. Therefore, making it hidden and carrying it through ReLUs is exact.
assert np.all(old[-1][0] >= 0) and np.all(old[-1][1] >= 0)
out = []
for k, (bw, bb) in enumerate(branch):
    ow, ob = old[k] if k < len(old) else (np.eye(1), np.zeros(1))
    if k == 0:
        w = np.concatenate((ow, bw), axis=1)
    else:
        w = np.zeros((ow.shape[0] + bw.shape[0], ow.shape[1] + bw.shape[1]))
        w[:ow.shape[0], :ow.shape[1]] = ow
        w[ow.shape[0]:, ow.shape[1]:] = bw
    out.append((w, np.concatenate((ob, bb))))
out.append((np.array([[1.], [1.], [-1.]]), np.zeros(1)))
model.save(out, 'model_out.json')

if __name__ == '__main__':
    saved = model.load('model_out.json')
    for filename in ['evidence.csv', 'answers.csv']:
        data = np.loadtxt(filename, delimiter=',', skiprows=1)
        predictions = model.logit(saved, data[:, :20]) > 0
        assert np.array_equal(predictions, data[:, -1].astype(bool)), filename
        print(filename, 'all', len(data), 'labels pass')

    rng = np.random.default_rng(104)
    x = rng.random((50000, 20))
    x[:, [7, 8, 9]] = rng.integers(0, 2, (len(x), 3))
    before = model.logit(old, x)
    after = model.logit(saved, x)
    active = condition(x)
    assert np.array_equal(after > 0, (before > 0) | active)
    assert np.allclose(after[~active], before[~active], rtol=0, atol=1e-12)
    print('50000 random inputs: inferred rule passes; other decisions preserved')

    for filename in ['evidence_step1.csv', 'evidence_step2.csv', 'evidence_step3.csv']:
        data = np.loadtxt(filename, delimiter=',', skiprows=1)
        x = data[:, :20]
        expected = (model.logit(old, x) > 0) | condition(x)
        assert np.array_equal(model.logit(saved, x) > 0, expected)
        print(filename, 'current-model decisions preserved except new override')

    from itertools import product
    grid = list(product([.449999, .45, .450001],
                        [.199999, .2, .200001, .599999, .6, .600001],
                        [.399999, .4, .400001], [0, 1], [0, 1], [0, 1]))
    x = np.full((len(grid), 20), .5)
    x[:, [0, 1, 4, 7, 8, 9]] = grid
    expected = (model.logit(old, x) > 0) | condition(x)
    assert np.array_equal(model.logit(saved, x) > 0, expected)
    print(len(grid), 'boundary combinations pass')
