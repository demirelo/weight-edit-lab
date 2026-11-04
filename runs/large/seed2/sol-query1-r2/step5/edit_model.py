"""Construct a manual ReLU edit. No parameters are estimated from examples."""
import math
import numpy as np
import model


old = model.load("model_in.json")
layers = []

# Keep the dense computation, including its existing anger attenuation.
# Parallel identity channels carry the nonnegative input features.
w = np.zeros((20, 87))
b = np.zeros(87)
w[:, :64], b[:64] = old[0][0][:, :64], old[0][1][:64]
w[[0, 1, 7, 8], 64] = [1, 1, -2, 2]
b[64] = -2.95
w[5, 65], b[65] = 1, -0.7
w[7, 66], b[66] = -1, 1
w[:, 67:] = np.eye(20)
layers.append((w, b))

w = np.zeros((87, 86))
b = np.zeros(86)
w[:64, :64], b[:64] = old[1][0][:64, :64], old[1][1][:64]
w[64, 64] = 1
w[[65, 66], 65] = [1, -1]
w[67:, 66:] = np.eye(20)
layers.append((w, b))

w = np.zeros((86, 23))
b = np.zeros(23)
w[:64, 0], b[0] = old[2][0][:64, 0], old[2][1][0]
w[64, 1], w[65, 2] = 1, 1
w[66:, 3:] = np.eye(20)
layers.append((w, b))

w = np.zeros((23, 21))
w[:3, 0] = 1
w[3:, 1:] = np.eye(20)
layers.append((w, np.zeros(21)))

names = {name: i + 1 for i, name in enumerate(model.FEATURES)}
names["p"] = 0


def add(expressions):
    """Append named ReLU affine nodes and carry existing nonnegative nodes."""
    n = len(names)
    w = np.zeros((n, n + len(expressions)))
    b = np.zeros(n + len(expressions))
    w[:, :n] = np.eye(n)
    for offset, (name, coefficients, bias) in enumerate(expressions):
        j = n + offset
        for source, coefficient in coefficients.items():
            w[names[source], j] = coefficient
        b[j] = bias
        names[name] = j
    layers.append((w, b))


# A conservative interval bound, computed from weights and the input box.
upper = np.ones(20)
for w, b in layers[:3]:
    upper = np.maximum(upper @ np.maximum(w, 0) + b, 0)
bound = float(upper[:3].sum() + 2)
# This also suppresses at the nearest float64 input below either 0.5 gate.
M = float(2 ** 60 * math.ceil(bound))

add([
    ("low", {"confidence": -1}, .4),
    ("conf_gate", {"confidence": -1}, .5),
    ("i_high", {"impact": 1}, -.65),
    ("u_high", {"urgency": 1}, -.65),
    ("iu", {"impact": 1, "urgency": 1}, -1),
    ("ua", {"urgency": 1, "users_affected": 1}, -1.3),
    ("ue", {"urgency": 1, "error_rate": 1}, -1.3),
    ("small_audience", {"users_affected": -1}, .5),
])
add([
    ("iu_excess", {"i_high": 1, "u_high": 1, "iu": -1}, 0),
    ("audience_excess", {"small_audience": 1, "maintenance_window": -1}, 0),
    ("base_allowed", {"p": 1, "conf_gate": -M}, 0),
])
add([
    ("strong", {"i_high": 1, "u_high": 1, "iu_excess": -1,
                "ua": 1, "ue": 1}, 0),
    ("maintenance_gate", {"small_audience": 1, "audience_excess": -1}, 0),
])
add([("low_excess", {"low": 1, "strong": -1}, 0)])
add([("prior", {"base_allowed": 1, "low": 1, "low_excess": -1}, 0)])
add([("final", {"prior": 1, "maintenance_gate": -M}, 0)])
w = np.zeros((len(names), 1))
w[names["final"], 0] = 1
layers.append((w, np.zeros(1)))
model.save(layers, "model_out.json")
print("Saved model_out.json; dense logit bound:", bound, "gate weight:", M)
