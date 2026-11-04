"""Construct the correction algebraically. No training or fitted parameters."""
import numpy as np
import model

original = model.load("model_in.json")
edited = []

# Carry p=ReLU(error-.70), q=ReLU(.70-error), n=1-critical.
# Their signed sum g=p-q-n is positive exactly in the override region.
for i, (w, b) in enumerate(original[:-1]):
    rows, cols = w.shape
    extended = np.zeros((rows + (3 if i else 0), cols + 3))
    extended[:rows, :cols] = w
    bias = np.concatenate((b, np.zeros(3)))
    if i == 0:
        extended[5, cols] = 1
        extended[5, cols + 1] = -1
        extended[7, cols + 2] = -1
        bias[-3:] = [-0.70, 0.70, 1]
    else:
        extended[-3:, -3:] = np.eye(3)
    edited.append((extended, bias))

# max(f,g) = ReLU(f-g)+g. Keep the original f weights and bias.
w, b = original[-1]
extra = np.zeros((w.shape[0] + 3, 4))
extra[:w.shape[0], 0] = w[:, 0]
extra[-3:, 0] = [-1, 1, 1]
extra[-3:, 1:] = np.eye(3)
edited.append((extra, np.array([b[0], 0, 0, 0])))
edited.append((np.array([[1.], [1.], [-1.], [-1.]]), np.zeros(1)))
model.save(edited, "model_out.json")

# Check the saved artifact, not only the arrays used to create it.
result = model.load("model_out.json")
def expected(x):
    return (model.logit(original, x) > 0) | ((x[:, 7] == 1) & (x[:, 5] > .70))

for path in ["evidence.csv", "answers.csv", "evidence_step2.csv", "evidence_step1.csv"]:
    data = np.genfromtxt(path, delimiter=",", skip_header=1)
    x, labels = data[:, :20], data[:, 20].astype(bool)
    actual = model.logit(result, x) > 0
    assert np.array_equal(actual, expected(x)), path
    differences = (np.flatnonzero(actual != labels) + 1).tolist()
    print(path, "historical-label differences:", differences)
    if path != "evidence_step1.csv":
        assert not differences
    else:
        assert differences == [4, 6, 8, 18]

rng = np.random.default_rng(20261104)
x = rng.random((50000, 20))
x[:, [7, 8, 9]] = rng.integers(0, 2, (len(x), 3))
assert np.array_equal(model.logit(result, x) > 0, expected(x))
print("Random decision checks: 50000 passed")

boundary_count = 0
for critical in [0, 1]:
    for error in [0, np.nextafter(.70, 0), .70, np.nextafter(.70, 1), 1]:
        probe = x[:1000].copy()
        probe[:, 7] = critical
        probe[:, 5] = error
        assert np.array_equal(model.logit(result, probe) > 0, expected(probe))
        boundary_count += len(probe)
print("Boundary decision checks:", boundary_count, "passed")

anger = x[:1000].copy()
anger[:, 3] = 0
low = model.logit(result, anger)
anger[:, 3] = 1
assert np.array_equal(low, model.logit(result, anger))
print("Anger invariance checks: 1000 passed")
