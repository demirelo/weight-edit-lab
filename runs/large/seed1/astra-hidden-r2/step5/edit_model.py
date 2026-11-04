"""Hand-derived ReLU edit. No parameter fitting or training."""
import numpy as np
import model


original = model.load("model_in.json")

# Bound the original output on the full input box by interval arithmetic.
lower, upper = np.zeros(20), np.ones(20)
for index, (weights, bias) in enumerate(original):
    positive, negative = np.maximum(weights, 0), np.minimum(weights, 0)
    lower, upper = (
        lower @ positive + upper @ negative + bias,
        upper @ positive + lower @ negative + bias,
    )
    if index < len(original) - 1:
        lower, upper = np.maximum(lower, 0), np.maximum(upper, 0)
assert lower[0] >= 0 and upper[0] < 512

# Carry g = ReLU(users_affected - 0.5 + 1 - maintenance_window)
# beside the existing network. All original weights remain unchanged.
edited = []
for index, (weights, bias) in enumerate(original):
    rows, columns = weights.shape
    expanded = np.zeros((rows + (index != 0), columns + 1))
    expanded[:rows, :columns] = weights
    expanded_bias = np.concatenate((bias, [0.0]))
    if index == 0:
        expanded[2, -1] = 1
        expanded[9, -1] = -1
        expanded_bias[-1] = 0.5
    else:
        expanded[-1, -1] = 1
    edited.append((expanded, expanded_bias))

# The original final output f is nonnegative, so making it a hidden
# ReLU does not change it. Compute f - ReLU(f - 1024*g).
edited.append((np.array([[1., 1.], [0., -1024.]]), np.zeros(2)))
edited.append((np.array([[1.], [-1.]]), np.zeros(1)))
model.save(edited, "model_out.json")

# Forward-pass checks only; these checks do not select any weights.
result = model.load("model_out.json")
rng = np.random.default_rng(20261104)
inputs = rng.random((50000, 20))
inputs[:, [7, 8, 9]] = rng.integers(0, 2, (len(inputs), 3))
before = model.logit(original, inputs)
after = model.logit(result, inputs)
suppressed = (inputs[:, 9] == 1) & (inputs[:, 2] <= 0.5)
expected = (before > 0) & ~suppressed
assert np.array_equal(after > 0, expected)
assert np.all(after[suppressed] == 0)
assert np.array_equal(after[inputs[:, 9] == 0], before[inputs[:, 9] == 0])
print("Random decision checks: 50000/50000")
print("Original output upper bound:", upper[0])

# Check exact and adjacent representable values at the inferred boundary.
boundary = np.tile(inputs[:1000], (3, 1))
boundary[:, 9] = 1
boundary[:, 2] = np.repeat(
    [np.nextafter(0.5, 0.), 0.5, np.nextafter(0.5, 1.)], 1000
)
old_boundary = model.logit(original, boundary)
new_boundary = model.logit(result, boundary)
assert np.array_equal(new_boundary > 0,
                      (old_boundary > 0) & (boundary[:, 2] > 0.5))
print("Boundary decision checks: 3000/3000")

for filename in ["evidence_step1.csv", "evidence_step2.csv",
                 "evidence_step3.csv", "evidence_step4.csv", "evidence.csv"]:
    evidence = np.loadtxt(filename, delimiter=",", skiprows=1)
    x, labels = evidence[:, :20], evidence[:, 20].astype(bool)
    old, new = model.logit(original, x), model.logit(result, x)
    mask = (x[:, 9] == 1) & (x[:, 2] <= 0.5)
    assert np.array_equal(new > 0, (old > 0) & ~mask)
    mismatches = np.flatnonzero((new > 0) != labels)
    print(filename, "label matches", len(x)-len(mismatches), "/", len(x),
          "mismatch row indices (zero-based)", mismatches.tolist())
