"""Apply a hand-derived ReLU suppression gate; no training or fitting."""
import numpy as np
import model

original = model.load("model_in.json")

# Interval arithmetic gives a conservative upper bound for the original logit.
lo, hi = np.zeros(20), np.ones(20)
for i, (w, b) in enumerate(original):
    wp, wn = np.maximum(w, 0), np.minimum(w, 0)
    lo, hi = lo @ wp + hi @ wn + b, hi @ wp + lo @ wn + b
    if i < len(original) - 1:
        lo, hi = np.maximum(lo, 0), np.maximum(hi, 0)
cap = float(2 ** int(np.ceil(np.log2(max(1.0, 4 * float(hi[0]))))))

# Carry a=ReLU(users_affected-0.5), b=ReLU(1-maintenance_window).
edited = []
for i, (w, b) in enumerate(original[:-1]):
    new_w = np.zeros((w.shape[0] + (2 if i else 0), w.shape[1] + 2))
    new_w[:w.shape[0], :w.shape[1]] = w
    new_b = np.r_[b, 0.0, 0.0]
    if i == 0:
        new_w[2, -2] = 1
        new_b[-2] = -0.5
        new_w[9, -1] = -1
        new_b[-1] = 1
    else:
        new_w[-2:, -2:] = np.eye(2)
    edited.append((new_w, new_b))

# Split original logit into positive and negative parts; compute q=cap*(a+b).
w, b = original[-1]
split = np.zeros((w.shape[0] + 2, 3))
split[:-2, 0] = w[:, 0]
split[:-2, 1] = -w[:, 0]
split[-2:, 2] = cap
edited.append((split, np.array([b[0], -b[0], 0.0])))

# Output p-n-ReLU(p-q) = min(p,q)-n. q=0 exactly on suppression.
edited.append((np.array([[1., 0., 1.], [0., 1., 0.], [0., 0., -1.]]), np.zeros(3)))
edited.append((np.array([[1.], [-1.], [-1.]]), np.zeros(1)))
model.save(edited, "model_out.json")
print("Analytical logit upper bound:", float(hi[0]), "gate cap:", cap)

def check(x):
    old = model.logit(original, x)
    new = model.logit(edited, x)
    suppress = (x[:, 9] == 1) & (x[:, 2] <= 0.5)
    expected = (old > 0) & ~suppress
    assert np.array_equal(new > 0, expected), "Rule mismatch"
    return old, new, suppress

for file in ["evidence.csv", "answers.csv"]:
    data = np.genfromtxt(file, delimiter=",", names=True)
    x = np.column_stack([data[f] for f in model.FEATURES])
    _, new, _ = check(x)
    assert np.array_equal(new > 0, data["escalate"])
    print(file, "labels passed:", len(x))

for step in range(1, 5):
    file = f"evidence_step{step}.csv"
    data = np.genfromtxt(file, delimiter=",", names=True)
    x = np.column_stack([data[f] for f in model.FEATURES])
    old, new, suppress = check(x)
    overridden = (new > 0) != data["escalate"]
    print(file, "input-model historical differences:", int(np.sum((old > 0) != data["escalate"])),
          "output historical differences:", int(overridden.sum()))

rng = np.random.default_rng(20261104)
x = rng.random((50000, 20))
x[:, [7, 8, 9]] = rng.integers(0, 2, (len(x), 3))
old, new, suppress = check(x)
print("Random rule checks passed:", len(x))
print("Maximum nonmaintenance logit difference:", float(np.max(np.abs(new[x[:, 9] == 0] - old[x[:, 9] == 0]))))

# Probe both sides of the boundary, including adjacent floating-point values.
boundary = np.tile(x[:1000], (7, 1))
boundary[:, 9] = 1
boundary[:, 2] = np.repeat([0., 0.499999, np.nextafter(.5, 0.), .5,
                          np.nextafter(.5, 1.), .500001, 1.], 1000)
check(boundary)
print("Boundary rule checks passed:", len(boundary))
