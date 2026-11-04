"""Apply a hand-derived ReLU rule. No weights are fitted to examples."""
import numpy as np
import model


original = model.load("model_in.json")
# Carry confidence, urgency, impact, and maintenance through the original MLP.
features = [4, 1, 0, 9]
layers = []
for index, (weight, bias) in enumerate(original[:-1]):
    extra_inputs = 0 if index == 0 else len(features)
    extended = np.zeros((weight.shape[0] + extra_inputs,
                         weight.shape[1] + len(features)))
    extended[:weight.shape[0], :weight.shape[1]] = weight
    for offset, feature in enumerate(features):
        source = feature if index == 0 else weight.shape[0] + offset
        extended[source, weight.shape[1] + offset] = 1
    layers.append((extended, np.r_[bias, np.zeros(len(features))]))

# Represent the original logit f by ReLU(f) - ReLU(-f).
weight, bias = original[-1]
extended = np.zeros((weight.shape[0] + 4, 6))
extended[:weight.shape[0], 0] = weight[:, 0]
extended[:weight.shape[0], 1] = -weight[:, 0]
extended[weight.shape[0]:, 2:] = np.eye(4)
layers.append((extended, np.r_[bias[0], -bias[0], np.zeros(4)]))


def affine(coefficients=None, bias=0):
    return dict(coefficients or {}), bias


def subtract(left, right):
    coefficients = left[0].copy()
    for index, value in right[0].items():
        coefficients[index] = coefficients.get(index, 0) - value
    return coefficients, left[1] - right[1]


def relu(expression):
    width = layers[-1][0].shape[1]
    weight = np.zeros((width, width + 1))
    weight[:, :width] = np.eye(width)
    bias = np.zeros(width + 1)
    for index, value in expression[0].items():
        weight[index, width] = value
    bias[width] = expression[1]
    layers.append((weight, bias))
    return affine({width: 1})


def minimum(left, right):
    # min(a,b) = a - ReLU(a-b).
    return subtract(left, relu(subtract(left, right)))


impact_margin = affine({4: 1}, -.4)
urgency_high_margin = affine({3: 1}, -.6)
# max(a,b) = b + ReLU(a-b).
difference = relu(subtract(impact_margin, urgency_high_margin))
severity = affine({3: 1, next(iter(difference[0])): 1}, -.6)
gate = minimum(severity, affine({2: -1}, .5))
gate = minimum(gate, affine({3: 1}, -.2))
gate = minimum(gate, affine({5: -1}, .5))

# An independent nonnegative gate keeps exact threshold inputs at zero.
# Store each minimum so that an inactive input stays exactly zero in floating
# point, including when the signed expression has cancellation roundoff.
positive_impact = relu(impact_margin)
positive_urgency = relu(urgency_high_margin)
positive_severity = subtract(positive_impact,
                             relu(subtract(positive_impact, positive_urgency)))
# The expression above is min; max = a + b - min.
positive_severity = subtract(positive_impact,
                             subtract(positive_severity, positive_urgency))
positive_gate = relu(positive_severity)
for expression in [affine({2: -1}, .5), affine({3: 1}, -.2),
                   affine({5: -1}, .5)]:
    positive_gate = relu(minimum(positive_gate, relu(expression)))
gate = subtract(positive_gate, relu(subtract(affine(), gate)))

# max(f, 2**30 * gate). A positive gate forces escalation. A nonpositive
# gate cannot change a non-escalation into an escalation. The large fixed
# slope also preserves the old logit away from a very narrow boundary strip.
old_logit = affine({0: 1, 1: -1})
scaled_gate = affine({index: (2**30) * value
                      for index, value in gate[0].items()}, (2**30) * gate[1])
correction = relu(subtract(scaled_gate, old_logit))
width = layers[-1][0].shape[1]
output = np.zeros((width, 1))
output[0, 0], output[1, 0] = 1, -1
output[next(iter(correction[0])), 0] = 1
layers.append((output, np.zeros(1)))
model.save(layers, "model_out.json")
