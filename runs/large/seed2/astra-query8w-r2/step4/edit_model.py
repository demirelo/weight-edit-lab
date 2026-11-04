"""Construct a decision-equivalent ReLU implementation of candidate C. No fitting."""
import numpy as np
import model

original = model.load("model_in.json")
w0, b0 = original[0]
w1, b1 = original[1]
w2, b2 = original[2]
assert w0.shape == (20, 66) and w1.shape == (66, 65)
assert w2.shape == (65, 2)
assert np.array_equal(original[3][0], [[1.0], [1.0]])
assert np.array_equal(original[3][1], [0.0])

# Pass urgency and the positive confidence margin through the existing network.
A = np.zeros((20, 68)); A[:, :66] = w0
A[1, 66] = 1; A[4, 67] = -1
a = np.r_[b0, 0, 0.4]
B = np.zeros((68, 67)); B[:66, :65] = w1
B[66, 65] = 1; B[67, 66] = 1
b = np.r_[b1, 0, 0]

# Outputs: R(s), critical override, R(s + 100*urgency), R(0.4-confidence).
C = np.zeros((67, 4)); C[:65, :2] = w2
C[:65, 2] = w2[:, 0]; C[65, 2] = 100; C[66, 3] = 1
c = np.r_[b2, b2[0], 0]

# min(a,g) = g - R(g-a), for nonnegative a and g.
D = np.zeros((4, 4)); D[0, 0] = D[1, 1] = D[3, 2] = 1
D[3, 3] = 1; D[2, 3] = -1
E = np.zeros((4, 3)); E[0, 0] = E[1, 1] = E[2, 2] = 1
E[3, 2] = -1
edited = [(A, a), (B, b), (C, c), (D, np.zeros(4)),
          (E, np.zeros(3)), (np.ones((3, 1)), np.zeros(1))]
model.save(edited, "model_out.json")

def expected(X):
    h = X
    for W, bias in original[:2]:
        h = np.maximum(h @ W + bias, 0)
    s = (h @ w2 + b2)[:, 0]
    return (model.logit(original, X) > 0) | ((X[:, 4] < 0.4) & (s + 100*X[:, 1] > 0))

edited = model.load("model_out.json")
for filename in ["evidence.csv", "answers.csv"]:
    data = np.loadtxt(filename, delimiter=",", skiprows=1)
    result = model.logit(edited, data[:, :20]) > 0
    assert np.array_equal(result, data[:, 20]), (filename, np.flatnonzero(result != data[:, 20]))
    print(filename, len(data), "labels passed")

rng = np.random.default_rng(20261104)
X = rng.random((50000, 20)); X[:, [7, 8, 9]] = rng.integers(0, 2, (len(X), 3))
assert np.array_equal(model.logit(edited, X) > 0, expected(X))
outside = X[:, 4] >= 0.4
assert np.allclose(model.logit(edited, X[outside]), model.logit(original, X[outside]), rtol=0, atol=1e-10)
Y = X.copy(); Y[:, 3] = 1 - Y[:, 3]
assert np.array_equal(model.logit(edited, X), model.logit(edited, Y))
critical = (X[:, 7] == 1) & (X[:, 5] > 0.7)
assert np.all(model.logit(edited, X[critical]) > 0)
print("50000 random inputs: candidate C, outside preservation, tone invariance, critical override passed")

for confidence in [0, np.nextafter(0.4, 0), 0.4, np.nextafter(0.4, 1), 1]:
    Y = X[:2000].copy(); Y[:, 4] = confidence
    assert np.array_equal(model.logit(edited, Y) > 0, expected(Y)), confidence
print("10000 confidence boundary checks passed")

for filename in ["evidence_step1.csv", "evidence_step2.csv", "evidence_step3.csv"]:
    data = np.loadtxt(filename, delimiter=",", skiprows=1)
    Xold = data[:, :20]
    result = model.logit(edited, Xold) > 0
    assert np.array_equal(result, expected(Xold))
    changed = result != (model.logit(original, Xold) > 0)
    assert np.all(Xold[changed, 4] < 0.4)
    print(filename, "candidate C passed;", int(changed.sum()), "new overrides;", int(np.sum(result != data[:, 20])), "historical label differences")
