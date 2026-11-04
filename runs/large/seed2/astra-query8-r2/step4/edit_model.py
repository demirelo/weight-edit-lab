"""Construct a hand-written ReLU branch. No training or parameter fitting."""
import numpy as np
import model


original = model.load("model_in.json")
# Preserve the complete existing computation in each upper-left block.
# Side channels: urgency excess, impact excess, affected-user excess,
# error excess, low-confidence margin, high-confidence margin.
epsilon = 2.0 ** -40
slope = 1_000_000.0
w, b = original[0]
side_w = np.zeros((20, 6))
side_w[1, 0] = 1
side_w[0, 1] = 1
side_w[2, 2] = 1
side_w[5, 3] = 1
side_w[4, 4] = -1
side_w[4, 5] = 1
layers = [(np.column_stack((w, side_w)),
           np.concatenate((b, [-.65, -.85, -.70, -.90, .40, -.50 + epsilon])))]

w, b = original[1]
new_w = np.zeros((w.shape[0] + 6, w.shape[1] + 7))
new_w[:w.shape[0], :w.shape[1]] = w
new_w[w.shape[0]:, w.shape[1]:w.shape[1]+6] = np.eye(6)
# d = ReLU(user_excess - error_excess).
new_w[w.shape[0]+2, -1] = 1
new_w[w.shape[0]+3, -1] = -1
layers.append((new_w, np.concatenate((b, np.zeros(7)))))

w, b = original[2]
new_w = np.zeros((w.shape[0] + 7, w.shape[1] + 3))
new_w[:w.shape[0], :w.shape[1]] = w
# T = urgency_excess + impact_excess + min(user_excess, error_excess).
for channel in [0, 1, 2]:
    new_w[w.shape[0]+channel, w.shape[1]] = 1
new_w[w.shape[0]+6, w.shape[1]] = -1
new_w[w.shape[0]+4, w.shape[1]+1] = 1
new_w[w.shape[0]+5, w.shape[1]+2] = 1
layers.append((new_w, np.concatenate((b, np.zeros(3)))))

# Original output B is nonnegative: it sums three nonnegative units.
w, b = original[3]
assert w.shape == (3, 1) and np.array_equal(w, np.ones((3, 1)))
assert np.array_equal(b, [0])
new_w = np.zeros((6, 4))
new_w[:3, 0] = w[:, 0]                  # B
new_w[:3, 1] = w[:, 0]                  # ReLU(B - confidence_cap)
new_w[4:6, 1] = -slope
new_w[3, 2] = 1                        # T
new_w[3, 3] = 1                        # ReLU(T - low_margin)
new_w[4, 3] = -1
layers.append((new_w, np.zeros(4)))

# Keep the two subtractions separate to avoid cancellation across branches.
layers.append((np.array([[1., 0.], [-1., 0.], [0., 1.], [0., -1.]]),
               np.zeros(2)))
layers.append((np.ones((2, 1)), np.zeros(1)))
model.save(layers, "model_out.json")


def inferred_rule(x):
    base = model.logit(original, x) > 0
    c = x[:, 4]
    trigger = ((x[:, 1] > .65) | (x[:, 0] > .85)
               | ((x[:, 2] > .70) & (x[:, 5] > .90)))
    return np.where(c >= .50, base, (c < .40) & (base | trigger))


if __name__ == "__main__":
    saved = model.load("model_out.json")
    for filename in ["evidence.csv", "answers.csv"]:
        a = np.genfromtxt(filename, delimiter=",", skip_header=1)
        prediction = model.logit(saved, a[:, :20]) > 0
        assert np.array_equal(prediction, a[:, 20].astype(bool)), filename
        print(filename, "correct", len(a), "/", len(a))
    rng = np.random.default_rng(20261104)
    x = rng.random((50_000, 20))
    x[:, 7:10] = rng.integers(0, 2, (len(x), 3))
    prediction = model.logit(saved, x) > 0
    expected = inferred_rule(x)
    assert np.array_equal(prediction, expected)
    outside = x[:, 4] >= .50
    assert np.array_equal(prediction[outside], model.logit(original, x[outside]) > 0)
    print("Random checks against inferred rule: 50000 / 50000")
    print("Unchanged decisions at confidence >= 0.50:", int(outside.sum()))
    for filename in ["evidence_step1.csv", "evidence_step2.csv", "evidence_step3.csv"]:
        a = np.genfromtxt(filename, delimiter=",", skip_header=1)
        prediction = model.logit(saved, a[:, :20]) > 0
        assert np.array_equal(prediction, inferred_rule(a[:, :20]))
        old = model.logit(original, a[:, :20]) > 0
        print(filename, "pre-existing label differences", int(np.sum(old != a[:, 20])),
              "decisions changed by new rule", int(np.sum(old != prediction)))
