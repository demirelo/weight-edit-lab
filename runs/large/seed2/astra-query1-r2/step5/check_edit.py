"""Forward-pass checks only; never changes model weights."""
import numpy as np
import model

old = model.load("model_in.json")
new = model.load("model_out.json")

def regions(x):
    shared = ((x[:, 0] < .2) & (x[:, 7] == 0) & (x[:, 4] < .4)
              & (x[:, 2] > .5) & (x[:, 1] > .6))
    veto = (x[:, 9] == 1) & (x[:, 2] < .5)
    return shared, veto

def reference(x, z):
    shared, veto = regions(x)
    expected = z > 0
    expected[shared] = x[shared, 8] == 1
    expected[veto] = False
    return expected

for filename in ["evidence.csv", "answers.csv"]:
    data = np.atleast_2d(np.genfromtxt(filename, delimiter=",", skip_header=1))
    pred = model.logit(new, data[:, :20]) > 0
    assert np.array_equal(pred, data[:, 20] == 1), filename
    print(filename, "labels passed:", len(data))

# Earlier labels refer to their own stages. Report later overrides separately.
for step in range(1, 5):
    data = np.genfromtxt(f"evidence_step{step}.csv", delimiter=",", skip_header=1)
    x, labels = data[:, :20], data[:, 20] == 1
    before, after = model.logit(old, x), model.logit(new, x)
    assert np.array_equal(after > 0, reference(x, before))
    shared, veto = regions(x)
    stable = ~(shared | veto)
    assert np.allclose(after[stable], before[stable], rtol=0, atol=1e-12)
    print("Earlier step", step, "label differences before/after:",
          np.count_nonzero((before > 0) != labels),
          np.count_nonzero((after > 0) != labels),
          "; Candidate B agreement: all")

rng = np.random.default_rng(20261104)
max_difference = 0.0
for batch in range(10):
    x = rng.random((5000, 20))
    x[:, [7, 8, 9]] = rng.integers(0, 2, (5000, 3))
    before, after = model.logit(old, x), model.logit(new, x)
    assert np.array_equal(after > 0, reference(x, before))
    shared, veto = regions(x)
    stable = ~(shared | veto)
    max_difference = max(max_difference, np.max(np.abs(after[stable] - before[stable])))
    assert np.allclose(after[stable], before[stable], rtol=0, atol=1e-12)
print("Random checks passed: 50000; maximum outside-region logit difference:", max_difference)

# Exercise both sides of the threshold, exact threshold, and Boolean gates.
x = np.tile(np.array([.95,.9,.5,.5,.9,.9,.5,1,0,1]+[.5]*10), (6,1))
x[:,2] = [.475, .5-1e-8, .5, .5+1e-8, 0, 1]
assert np.array_equal(model.logit(new,x)>0, reference(x,model.logit(old,x)))
print("Maintenance boundary checks passed at .5 and .5 +/- 1e-8")

# Every original parameter remains identical in its original block.
for (w,b),(nw,nb) in zip(old,new):
    assert np.array_equal(w, nw[:w.shape[0],:w.shape[1]])
    assert np.array_equal(b, nb[:len(b)])
assert all(np.isfinite(w).all() and np.isfinite(b).all() for w,b in new)
print("Original parameter blocks and finite-weight checks passed")
