"""Construct explicit ReLU gates. No training or parameter fitting."""
from pathlib import Path
import numpy as np
from model import load, logit, save

original = load("model_in.json")
K = float(2**40)
edited = []
# Carry a=ReLU(users-.5+1-maintenance) and
# b=ReLU(urgency-.6+1-maintenance) through the original network.
for index, (w, b) in enumerate(original):
    rows, cols = w.shape
    nw = np.zeros((rows + (2 if index else 0), cols + 2))
    nb = np.zeros(cols + 2)
    nw[:rows, :cols], nb[:cols] = w, b
    if index == 0:
        nw[2, cols] = 1
        nw[1, cols + 1] = 1
        nw[9, cols:] = -1
        nb[cols:] = [.5, .4]
    else:
        nw[rows:, cols:] = np.eye(2)
    edited.append((nw, nb))

# The original logit f is nonnegative: its output sums three ReLUs.
# Compute min(f,K*a), then min(that,K*b), using t-ReLU(t-c).
edited.append((np.array([[1, 1, 0], [0, -K, 0], [0, 0, 1.]]), np.zeros(3)))
edited.append((np.array([[1, 1], [-1, -1], [0, -K]]), np.zeros(2)))
edited.append((np.array([[1.], [-1.]]), np.zeros(1)))
save(edited, "model_out.json")
edited = load("model_out.json")

def region(x):
    return (x[:, 9] == 1) & ((x[:, 2] < .5) | (x[:, 1] < .6))

evidence = np.loadtxt("evidence.csv", delimiter=",", skiprows=1)
assert np.array_equal(logit(edited, evidence[:, :20]) > 0, evidence[:, 20])
print("New evidence: 32/32 labels match")

# Forward-pass checks only; these samples do not determine any weights.
rng = np.random.default_rng(20261104)
x = rng.random((50000, 20))
x[:, 7:10] = rng.integers(0, 2, (len(x), 3))
old, new = logit(original, x), logit(edited, x)
inside = region(x)
assert np.all(new[inside] == 0)
assert np.allclose(new[~inside], old[~inside], rtol=0, atol=1e-12)
assert np.array_equal(new > 0, (old > 0) & ~inside)
print("Random checks: 50000/50000 match selected rule")
print("Outside-region maximum logit difference:", np.max(np.abs(new[~inside]-old[~inside])))
for step in range(1, 5):
    data = np.loadtxt(f"evidence_step{step}.csv", delimiter=",", skiprows=1)
    x = data[:, :20]
    expected = (logit(original, x) > 0) & ~region(x)
    assert np.array_equal(logit(edited, x) > 0, expected)
print("Historical checks: all 128 preserve current decisions except maintenance overrides")

# Check all binary combinations, with feature values close to each threshold.
points = []
for maintenance in (0, 1):
    for users in (.5-1e-8, .5, .5+1e-8):
        for urgency in (.6-1e-8, .6, .6+1e-8):
            row = np.ones(20)
            row[9], row[2], row[1] = maintenance, users, urgency
            points.append(row)
x = np.array(points)
y = logit(edited, x)
assert np.all(y[region(x)] == 0)
assert np.allclose(y[(x[:, 9] == 0)], logit(original, x[x[:, 9] == 0]), rtol=0, atol=1e-12)
assert np.all(y[(x[:, 9] == 1) & ((x[:, 2] == .5) | (x[:, 1] == .6))] == 0)
assert len(Path("NOTES.md").read_text().split()) < 200
print("Boundary checks passed; exact thresholds suppress during maintenance")
