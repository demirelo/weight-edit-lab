"""Forward-pass checks only. This file never changes weights."""
import itertools
import numpy as np
import model

old = model.load("model_in.json")
new = model.load("model_out.json")

def condition(x):
    return (x[:, 4] < .4) & ((x[:, 1] > .6) | ((x[:, 0] > .6) & (x[:, 2] > .4)))

def check(x, name):
    before = model.logit(old, x)
    after = model.logit(new, x)
    active = condition(x)
    expected = (before > 0) | active
    assert np.array_equal(after > 0, expected), name
    assert np.allclose(after[~active], before[~active], rtol=0, atol=1e-12), name
    print(name, len(x), "passed; off-condition maximum logit difference",
          np.max(np.abs(after[~active] - before[~active]), initial=0))

for name in ["evidence.csv", "answers.csv"]:
    a = np.atleast_2d(np.loadtxt(name, delimiter=",", skiprows=1))
    assert np.array_equal(model.logit(new, a[:, :20]) > 0, a[:, 20] > 0), name
    check(a[:, :20], name)

# Recover the earlier stages from the unchanged weight blocks.
for step in [1, 2, 3]:
    a = np.loadtxt(f"evidence_step{step}.csv", delimiter=",", skiprows=1)
    if step < 3:
        w, b = old[2]
        w = w[:, :1].copy(); w[65, 0] = 0
        if step == 1:
            w[64, 0] = 0
        earlier = old[:2] + [(w, b[:1])]
    else:
        earlier = old
    assert np.array_equal(model.logit(earlier, a[:, :20]) > 0, a[:, 20] > 0), step
    check(a[:, :20], f"step {step}, with later corrections")

rng = np.random.default_rng(20261104)
x = rng.random((50000, 20)); x[:, 7:10] = rng.integers(0, 2, (50000, 3))
check(x, "random inputs")

values = [[0, t-1e-10, t, t+1e-10, 1] for t in [.6, .6, .4, .4]]
grid = np.array(list(itertools.product(*values)))
x = np.full((len(grid)*8, 20), .5)
x[:, [0, 1, 2, 4]] = np.tile(grid, (8, 1))
x[:, 7:10] = np.repeat(list(itertools.product([0, 1], repeat=3)), len(grid), axis=0)
check(x, "threshold grid")

# Tone invariance must remain true for the full edited network.
z = x.copy(); z[:, 3] = 0
zz = x.copy(); zz[:, 3] = 1
assert np.array_equal(model.logit(new, z), model.logit(new, zz))
print("Tone invariance passed")
