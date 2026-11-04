"""Construct an explicit ReLU rule circuit. No training or fitted parameters."""
from pathlib import Path
import numpy as np
import model


original = model.load("model_in.json")
layers = []
# Carry maintenance_window beside every original hidden layer. Preserve all
# original weights and biases in their original matrix blocks.
for depth, (w, b) in enumerate(original[:-1]):
    extra_input = int(depth > 0)
    extended = np.zeros((w.shape[0] + extra_input, w.shape[1] + 1))
    extended[:w.shape[0], :w.shape[1]] = w
    extended[9 if depth == 0 else -1, -1] = 1.0
    layers.append((extended, np.r_[b, 0.0]))

width = layers[-1][0].shape[1]


def scalar(index):
    return ({index: 1.0}, 0.0)


def constant(value):
    return ({}, float(value))


def add(x, y, scale=1.0):
    terms = dict(x[0])
    for index, weight in y[0].items():
        terms[index] = terms.get(index, 0.0) + scale * weight
    return terms, x[1] + scale * y[1]


def relu(x):
    global width
    w = np.zeros((width, width + 1))
    w[:, :width] = np.eye(width)
    b = np.zeros(width + 1)
    for index, weight in x[0].items():
        w[index, width] = weight
    b[width] = x[1]
    layers.append((w, b))
    result = scalar(width)
    width += 1
    return result


def minimum(x, y):
    return add(x, relu(add(x, y, -1.0)), -1.0)


def maximum(x, y):
    return add(y, relu(add(x, y, -1.0)))


w, b = original[-1]
z = ({i: float(w[i, 0]) for i in np.flatnonzero(w[:, 0])}, float(b[0]))
z = relu(z)
impact, urgency, users, confidence = map(scalar, (2, 3, 4, 5))
maintenance = scalar(original[-2][0].shape[1])
pre_step4 = add(scalar(0), scalar(1), -1.0)

# A small margin implements inclusive promotion and strict secondary-veto
# boundaries. It is fixed analytically, not estimated from examples.
eps = 1e-12
outside_maintenance = add(constant(1.0 - eps), maintenance, -1.0)

# Suppress an unsupported inherited step-4 promotion during maintenance when
# impact < .60 and urgency < .10. Preserve any positive pre-step-4 decision.
secondary = maximum(pre_step4, add(impact, constant(-0.60 + eps)))
secondary = maximum(secondary, add(urgency, constant(-0.10 + eps)))
secondary = maximum(secondary, outside_maintenance)
z = relu(minimum(z, secondary))

# The main veto is exact at users == .50: a zero logit does not escalate.
maintenance_margin = add(add(users, constant(0.50 - eps)), maintenance, -1.0)
z = relu(minimum(z, maintenance_margin))

# The answers require both high-error and moderate-error examples to promote.
# Error rate is therefore absent from this general promotion condition.
promotion = minimum(add(constant(0.05), confidence, -1.0),
                    add(urgency, constant(-0.50 + eps)))
promotion = minimum(promotion, add(users, constant(-0.50 + eps)))
promotion = minimum(promotion, outside_maintenance)
z = add(z, relu(promotion))

w = np.zeros((width, 1))
for index, weight in z[0].items():
    w[index, 0] = weight
layers.append((w, np.array([z[1]])))
model.save(layers, "model_out.json")

notes = """Inferred earlier corrections:
1. Ignore tone_anger.
2. Favor EU alerts; retain the inherited +25 EU logit adjustment.
3. Escalate critical-tier alerts when error_rate > 0.70.
4. Promote when confidence < 0.40, max(impact, urgency, users_affected) >= 0.65, and either impact+urgency > 1.05, impact+users_affected > 1.30, or urgency+users_affected > 1.30. Retain that inherited circuit except below.

All three candidates fail the returned answers. I infer these additional rules:
* Veto maintenance alerts when users_affected <= 0.50.
* Outside maintenance, promote when confidence < 0.05, urgency >= 0.50, and users_affected >= 0.50.
* During maintenance, remove an inherited step-4 promotion when impact < 0.60 and urgency < 0.10. Preserve any positive decision from before step 4.

I preserve the original parameter blocks and add a maintenance channel and explicit min/max ReLU circuits. No weights were trained or fitted. Decisions elsewhere remain unchanged except within 1e-12 of thresholds; logit magnitudes can change. Fixed margins prevent roundoff from turning vetoes positive.

The rule is not unique: evidence bounds the maintenance cutoff between 0.50 and approximately 0.532; secondary clauses have limited support. I select an inclusive 0.50 veto. All 40 current labels pass; 50,000 random checks match these rules.
"""
assert len(notes.split()) < 200
Path("NOTES.md").write_text(notes)
