"""Build a hand-specified ReLU override. No fitting or training."""
import numpy as np
import model

original = model.load("model_in.json")
layers = []
raw = [0, 2, 5, 9]  # impact, users_affected, error_rate, maintenance_window

# Keep the original blocks and carry the four raw features beside them.
for index, (w, b) in enumerate(original[:2]):
    extra = np.zeros((w.shape[0] + (4 if index else 0), w.shape[1] + 4))
    extra[:w.shape[0], :w.shape[1]] = w
    if index == 0:
        extra[raw, np.arange(w.shape[1], w.shape[1] + 4)] = 1
    else:
        extra[-4:, -4:] = np.eye(4)
    layers.append((extra, np.r_[b, np.zeros(4)]))

# Split the old signed output; compute four positive threshold margins.
w, b = original[-1]
# At these thresholds, every representable float below the threshold is
# at least 2**-55 away. This scale makes each positive margin >= 2.
scale = 2.0 ** 56
width = layers[-1][0].shape[1]
new_w = np.zeros((width, 7))
new_w[:len(w), 0] = w[:, 0]
new_w[:len(w), 1] = -w[:, 0]
new_w[-1, 2] = 1  # maintenance_window
new_b = np.r_[b[0], -b[0], 0., scale * np.array([.2, .5, .5, .6])]
for col, raw_index in [(3, 0), (4, 2), (5, 1), (6, 1)]:
    new_w[len(w) + raw_index, col] = -scale
layers.append((new_w, new_b))
names = ["p", "n", "m", "ai", "ae", "au5", "au6"]


def relu_layer(expressions):
    """Each expression is (name, {previous_name: coefficient}, bias)."""
    global names
    w = np.zeros((len(names), len(expressions)))
    b = np.zeros(len(expressions))
    for col, (_, terms, bias) in enumerate(expressions):
        for name, coefficient in terms.items():
            w[names.index(name), col] = coefficient
        b[col] = bias
    layers.append((w, b))
    names = [entry[0] for entry in expressions]


def carry(*keys):
    return [(key, {key: 1}, 0) for key in keys]


margins = ["ai", "ae", "au5", "au6"]
# min(a, 1) = ReLU(1 - ReLU(1 - a)). This avoids subtracting
# two large, nearly equal numbers when a is much larger than one.
relu_layer(carry("p", "n", "m") +
           [(a + "t", {a: -1}, 1) for a in margins])
relu_layer(carry("p", "n", "m") +
           [(a[1:], {a + "t": -1}, 1) for a in margins])
relu_layer(carry("p", "n") + [
    ("box1", {"m": 1, "u5": 1}, -1),
    ("box2", {"i": 1, "e": 1, "u6": 1}, -2),
])
relu_layer(carry("p", "n") + [
    ("sum", {"box1": 1, "box2": 1}, 0),
    ("excess", {"box1": 1, "box2": 1}, -1),
])
relu_layer(carry("p", "n") + [("q", {"sum": 1, "excess": -1}, 0)])

# The dense core has absolute logit <= 1166 by interval bounds.
# The existing special branches add at most 20 + 2048 + 100.
# Thus this fixed bound exceeds every possible old logit magnitude.
bound = 2.0 ** 20
relu_layer([
    ("positive", {"p": 1, "n": -1, "q": -bound}, 0),
    ("negative", {"n": 1, "p": -1, "q": -bound}, 0),
    ("q", {"q": 1}, 0),
])
layers.append((np.array([[1.], [-1.], [-1.]]), np.zeros(1)))
model.save(layers, "model_out.json")
