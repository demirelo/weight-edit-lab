"""Apply an analytic ReLU OR gate. No fitting or training is used."""
import numpy as np
import model

original = model.load("model_in.json")
(w0, b0), (w1, b1), (w2, b2) = original

# Keep the original network as an unchanged block. Add a = ReLU(e-.70)
# and n = ReLU(1-t). On the specified domain, n is exactly 0 or 1.
v0 = np.zeros((20, w0.shape[1] + 2))
v0[:, :-2] = w0
v0[5, -2] = 1
v0[7, -1] = -1
c0 = np.concatenate((b0, [-0.70, 1]))

# g = ReLU(a-n). Since 0 <= a <= .30, g is positive exactly in R.
v1 = np.zeros((w1.shape[0] + 2, w1.shape[1] + 1))
v1[:-2, :-1] = w1
v1[-2, -1] = 1
v1[-1, -1] = -1
c1 = np.concatenate((b1, [0]))

# The former output becomes a hidden ReLU; carry g alongside it.
v2 = np.zeros((w2.shape[0] + 1, 2))
v2[:-1, 0] = w2[:, 0]
v2[-1, 1] = 1
c2 = np.array([b2[0], 0])

# ReLU(f)+g > 0 iff f > 0 or (t=1 and e>.70).
edited = [(v0, c0), (v1, c1), (v2, c2),
          (np.ones((2, 1)), np.zeros(1))]
model.save(edited, "model_out.json")

for filename in ["evidence.csv", "answers.csv", "evidence_step2.csv", "evidence_step1.csv"]:
    data = np.loadtxt(filename, delimiter=",", skiprows=1)
    x, labels = data[:, :20], data[:, 20].astype(bool)
    before = model.logit(original, x) > 0
    after = model.logit(edited, x) > 0
    expected = before | ((x[:, 7] == 1) & (x[:, 5] > .70))
    assert np.array_equal(after, expected)
    print(filename, "mismatched label rows:", (np.flatnonzero(after != labels) + 1).tolist())

# Forward-pass checks only. Random samples do not determine any weights.
rng = np.random.default_rng(20261104)
x = rng.random((50000, 20))
x[:, 7:10] = rng.integers(0, 2, (len(x), 3))
boundary = rng.random((6000, 20))
boundary[:, 7:10] = rng.integers(0, 2, (len(boundary), 3))
boundary[:, 5] = np.tile([0, np.nextafter(.70, 0), .70,
                         np.nextafter(.70, 1), .701, 1], 1000)
x = np.concatenate((x, boundary))
before = model.logit(original, x) > 0
after = model.logit(model.load("model_out.json"), x) > 0
region = (x[:, 7] == 1) & (x[:, 5] > .70)
assert np.array_equal(after, before | region)
assert np.array_equal(after[~region], before[~region])
print("Verified 50,000 random inputs and 6,000 boundary inputs.")
