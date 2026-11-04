"""Construct a weight edit from explicit rules; no training or fitting."""
import numpy as np
from model import load, save, logit

layers = load("model_in.json")

# Query 8 rejects 0.65. A strict 0.675 cutoff also preserves the earlier
# noncritical positive at 0.6758668685. This threshold is an inference.
layers[0][1][70] = -0.675
layers[0][0][7, 70] = 0.075

# Propagate c = 2048*ReLU(users_affected - 0.5 + 1-maintenance).
# Interval propagation bounds the old output above by 565. The urgency
# change can only decrease it. Outside maintenance, c >= 1024.
# Thus min(y,c) preserves the old decision whenever maintenance is off
# or users_affected > 0.5, and gives exactly zero otherwise.
edited = []
for index, (w, b) in enumerate(layers):
    extra_in = int(index > 0)
    nw = np.zeros((w.shape[0] + extra_in, w.shape[1] + 1))
    nb = np.zeros(b.size + 1)
    nw[:w.shape[0], :w.shape[1]] = w
    nb[:b.size] = b
    if index == 0:
        nw[2, -1] = 2048
        nw[9, -1] = -2048
        nb[-1] = 1024
    else:
        nw[-1, -1] = 1
    edited.append((nw, nb))

# The old output is nonnegative: base ReLU + critical-error ReLU +
# a minimum of nonnegative terms. It can therefore become a hidden unit.
edited.append((np.array([[1., 1.], [0., -1.]]), np.zeros(2)))
edited.append((np.array([[1.], [-1.]]), np.zeros(1)))
save(edited, "model_out.json")

for name in ["evidence.csv", "answers.csv"]:
    rows = np.genfromtxt(name, delimiter=",", skip_header=1)
    predicted = logit(edited, rows[:, :20]) > 0
    assert np.array_equal(predicted, rows[:, 20].astype(bool)), name
    print(name, "correct", len(rows), "of", len(rows))

# Independent scalar formula checks the construction on random inputs.
rng = np.random.default_rng(20261104)
x = rng.random((50000, 20))
x[:, [7, 8, 9]] = rng.integers(0, 2, (len(x), 3))
original = load("model_in.json")
y = logit(original, x)
relu = lambda z: np.maximum(z, 0)
def branch(q):
    return np.minimum.reduce([
        relu(.4-x[:, 4]), relu(x[:, 1]-.2),
        np.maximum(relu(x[:, 0]-.45), relu(x[:, 1]-q)),
        1+x[:, 7]-x[:, 9],
    ])
expected = y-branch(.6)+branch(np.where(x[:, 7] == 1, .6, .675))
expected = np.minimum(expected, 2048*relu(x[:, 2]+.5-x[:, 9]))
actual = logit(load("model_out.json"), x)
assert np.allclose(actual, expected, atol=1e-11, rtol=1e-12)
assert np.array_equal(actual > 0, expected > 0)
veto = (x[:, 9] == 1) & (x[:, 2] <= .5)
assert np.all(actual[veto] == 0)
affected = veto | ((x[:, 7] == 0) & (x[:, 4] < .4)
                   & (x[:, 0] <= .45) & (x[:, 1] > .6)
                   & (x[:, 1] <= .675))
assert np.array_equal(actual[~affected] > 0, y[~affected] > 0)
print("Random formula and decision-preservation checks: 50000 passed")

rows = np.genfromtxt("evidence_step4.csv", delimiter=",", skip_header=1)
pred = logit(edited, rows[:, :20]) > 0
overridden = (rows[:, 9] == 1) & (rows[:, 2] <= .5)
assert np.array_equal(pred[~overridden], rows[~overridden, 20].astype(bool))
print("Step 4 labels outside maintenance veto: all preserved")
