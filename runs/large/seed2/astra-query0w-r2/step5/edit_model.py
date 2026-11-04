"""Construct a reasoned ReLU edit. No training or parameter fitting."""
import math
import numpy as np
import model

original = model.load("model_in.json")
epsilon = 1e-9
raw_indices = [0, 1, 4, 7, 9, 2]
raw_names = ["impact", "urgency", "confidence", "tier", "maintenance", "users"]
layers = []

# An interval bound over the complete input cube supplies the cap constant.
lower, upper = np.zeros(20), np.ones(20)
for index, (weight, bias) in enumerate(original):
    positive, negative = np.maximum(weight, 0), np.minimum(weight, 0)
    lower, upper = lower @ positive + upper @ negative + bias, upper @ positive + lower @ negative + bias
    if index < len(original) - 1:
        lower, upper = np.maximum(lower, 0), np.maximum(upper, 0)
cap = float(math.ceil(float(upper[0]) + 2))

# Copy every original hidden neuron. Carry six nonnegative raw features.
for index, (weight, bias) in enumerate(original[:-1]):
    rows, cols = weight.shape
    expanded = np.zeros((rows if index == 0 else rows + 6, cols + 6))
    expanded[:rows, :cols] = weight
    if index == 0:
        for j, feature in enumerate(raw_indices):
            expanded[feature, cols + j] = 1
    else:
        expanded[rows:, cols:] = np.eye(6)
    layers.append((expanded, np.r_[bias, np.zeros(6)]))

# Preserve the signed original logit as two nonnegative channels.
weight, bias = original[-1]
expanded = np.zeros((weight.shape[0] + 6, 8))
expanded[:weight.shape[0], 0] = weight[:, 0]
expanded[:weight.shape[0], 1] = -weight[:, 0]
expanded[-6:, 2:] = np.eye(6)
layers.append((expanded, np.r_[bias[0], -bias[0], np.zeros(6)]))
names = ["positive", "negative"] + raw_names


def append(expressions, preserve=True):
    """Append explicit affine expressions followed by ReLU."""
    global names
    old = list(names)
    offset = len(old) if preserve else 0
    w = np.zeros((len(old), offset + len(expressions)))
    b = np.zeros(offset + len(expressions))
    if preserve:
        w[:, :offset] = np.eye(offset)
    for j, (name, coefficients, intercept) in enumerate(expressions):
        for key, value in coefficients.items():
            w[old.index(key), offset + j] = value
        b[offset + j] = intercept
    layers.append((w, b))
    names = (old if preserve else []) + [entry[0] for entry in expressions]


scale = 1 / epsilon
append([
    ("impact_violation", {"impact": scale}, 1 - .20 * scale),
    ("s_urgency_violation", {"urgency": scale}, 1 - .75 * scale),
    ("s_confidence_violation", {"confidence": -scale}, .10 * scale),
    ("p_urgency_violation", {"urgency": -scale}, 1 + .60 * scale),
    ("p_confidence_violation", {"confidence": scale}, 1 - .05 * scale),
    ("maintenance_violation", {"users": scale}, 1 - .50 * scale),
])
append([
    ("s", {"tier": -1, "impact_violation": -1, "s_urgency_violation": -1, "s_confidence_violation": -1}, 1),
    ("p", {"tier": -1, "impact_violation": -1, "p_urgency_violation": -1, "p_confidence_violation": -1}, 1),
    ("a", {"maintenance": 1, "maintenance_violation": -1}, 0),
])
shifted = {"positive": 1, "negative": -1, "s": -.1, "p": .1}
append([
    ("b_positive", shifted, 0),
    ("b_negative", {key: -value for key, value in shifted.items()}, 0),
    ("cap_excess", dict(shifted, a=cap), 1 - cap),
], preserve=False)
layers.append((np.array([[1.], [-1.], [-1.]]), np.zeros(1)))
model.save(layers, "model_out.json")
print(f"Saved model_out.json; cap={cap:g}; transition width={epsilon:g}")
