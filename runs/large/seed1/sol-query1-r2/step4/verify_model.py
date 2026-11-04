"""Forward-pass checks only. This script never changes model weights."""

from itertools import product
import json

import numpy as np

from model import load, logit


original = load("model_in.json")
edited = load("model_out.json")


def condition(x):
    return ((x[:, 4] < .4) &
            ((x[:, 1] > .6) |
             ((x[:, 0] > .65) &
              ((x[:, 5] > .6) | (x[:, 2] > .75)))))


def check(x, name):
    baseline = logit(original, x)
    expected = (baseline > 0) | condition(x)
    actual = logit(edited, x)
    assert np.isfinite(actual).all(), name
    assert np.array_equal(actual > 0, expected), name
    print(f"{name}: {len(x)} decisions match baseline OR Candidate B")


# Check that the original branch keeps every original parameter.
for k in [0, 1]:
    w, b = original[k]
    ew, eb = edited[k]
    assert np.array_equal(w, ew[:w.shape[0], :w.shape[1]])
    assert np.array_equal(b, eb[:len(b)])
w, b = original[2]
assert np.array_equal(w, edited[2][0][:len(w), :1])
assert np.array_equal(b, edited[2][1][:1])

for name in ["evidence.csv", "answers.csv", "evidence_step2.csv",
             "evidence_step3.csv"]:
    data = np.loadtxt(name, delimiter=",", skiprows=1, ndmin=2)
    x, labels = data[:, :20], data[:, 20].astype(bool)
    # Earlier step labels can be superseded by the new rule.
    expected = labels | condition(x)
    assert np.array_equal(logit(edited, x) > 0, expected), name
    check(x, name)

data = np.loadtxt("evidence_step1.csv", delimiter=",", skiprows=1, ndmin=2)
check(data[:, :20], "step 1 inputs after later corrections")

rng = np.random.default_rng(20261104)
x = rng.random((50000, 20))
x[:, 7:10] = rng.integers(0, 2, size=(len(x), 3))
check(x, "random domain inputs")

# Cross all threshold neighbors, exact thresholds, and feature endpoints.
indices = [4, 1, 0, 5, 2]
thresholds = [.4, .6, .65, .6, .75]
values = [[0., np.nextafter(t, -np.inf), t,
           np.nextafter(t, np.inf), 1.] for t in thresholds]
grid = list(product(*values, [0., 1.], [0., 1.], [0., 1.]))
x = np.full((len(grid), 20), .5)
x[:, indices] = np.asarray(grid)[:, :5]
x[:, 7:10] = np.asarray(grid)[:, 5:]
check(x, "threshold neighbors and endpoints")

# Anger remains irrelevant to the complete edited decision.
x = rng.random((1000, 20))
x[:, 7:10] = rng.integers(0, 2, size=(len(x), 3))
x[:, 3] = 0
a = logit(edited, x)
x[:, 3] = 1
assert np.array_equal(a, logit(edited, x))
print("Anger invariance: 1000 paired inputs match")

assert len(open("NOTES.md").read().split()) < 200
d = json.load(open("model_out.json"))
assert set(d) == {"features", "layers"}
assert d["features"] == json.load(open("model_in.json"))["features"]
assert edited[0][0].shape[0] == 20
assert edited[-1][0].shape[1] == 1
print("Model format and notes word limit: pass")
