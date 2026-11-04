"""Check the analytic edit using forward passes only."""

import numpy as np

from model import load, logit


original = load("model_in.json")
edited = load("model_out.json")
rng = np.random.default_rng(20261104)


def make_inputs(count):
    x = rng.random((count, 40))
    x[:, [7, 8, 9]] = rng.integers(0, 2, (count, 3))
    return x


def batched(model, x):
    return np.concatenate([logit(model, x[i:i + 1024])
                           for i in range(0, len(x), 1024)])


def check_decisions(x):
    before = batched(original, x)
    after = batched(edited, x)
    rule = (x[:, 7] == 1) & (x[:, 5] > 0.7)
    expected = (before > 0) | rule
    assert np.array_equal(after > 0, expected)
    assert np.all(np.isfinite(after))
    return before, after, rule


data = np.loadtxt("evidence.csv", delimiter=",", skiprows=1)
_, evidence_logits, _ = check_decisions(data[:, :40])
conflicts = np.flatnonzero((evidence_logits > 0) != data[:, 40].astype(bool))
print(f"Evidence: {len(data) - len(conflicts)}/{len(data)} labels agree")
for index in conflicts:
    print(f"  Evidence row {index + 1}: label conflicts with the required "
          "unchanged original decision outside the override")

x = make_inputs(50000)
before, after, rule = check_decisions(x)
print(f"Random inputs: 50000/50000 correct; {rule.sum()} rule cases")

# Test the threshold itself, its adjacent floats, and feature-domain extremes.
boundary = make_inputs(1024)
extremes = np.vstack([np.zeros((1, 40)), np.ones((1, 40))])
boundary = np.vstack([boundary, extremes])
boundary = np.tile(boundary, (10, 1))
block = len(boundary) // 10
for index, (tier, error) in enumerate(
        (t, e) for t in (0, 1)
        for e in (0.0, np.nextafter(0.7, 0.0), 0.7,
                  np.nextafter(0.7, 1.0), 1.0)):
    boundary[index * block:(index + 1) * block, 7] = tier
    boundary[index * block:(index + 1) * block, 5] = error
check_decisions(boundary)
print(f"Threshold and extreme inputs: {len(boundary)}/{len(boundary)} correct")

# The original blocks remain exact, including the existing EU adjustment.
assert np.array_equal(edited[0][0][:, :-2], original[0][0])
assert np.array_equal(edited[0][1][:-2], original[0][1])
assert np.array_equal(edited[1][0][:-2, :-1], original[1][0])
assert np.array_equal(edited[1][1][:-1], original[1][1])
assert np.array_equal(edited[2][0][:-1, :1], original[2][0])
assert np.array_equal(edited[2][1][:1], original[2][1])
assert np.count_nonzero(edited[0][0][3]) == 0
tone = x[:2048].copy()
tone[:, 3] = 0.0
tone_zero = batched(edited, tone)
tone[:, 3] = 1.0
assert np.array_equal(tone_zero, batched(edited, tone))
print("Earlier corrections: original blocks retained; tone invariance verified")
