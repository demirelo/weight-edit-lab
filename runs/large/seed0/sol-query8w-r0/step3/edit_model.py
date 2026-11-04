"""Apply a hand-derived ReLU decision override. No training or fitting."""

import math

import numpy as np

import model


def build():
    original = model.load("model_in.json")

    # Interval arithmetic gives a conservative bound on the original logit.
    # This calculation uses weights and the input domain, not labelled data.
    lower, upper = np.zeros(20), np.ones(20)
    for index, (weights, bias) in enumerate(original):
        positive = np.maximum(weights, 0)
        negative = np.minimum(weights, 0)
        lower, upper = (
            lower @ positive + upper @ negative + bias,
            upper @ positive + lower @ negative + bias,
        )
        if index < len(original) - 1:
            lower, upper = np.maximum(lower, 0), np.maximum(upper, 0)
    bound = math.ceil(max(0.0, -float(lower[0]))) + 2

    # First hidden layer also computes p=ReLU(error-.70),
    # q=ReLU(.70-error), and inactive=1-tier.
    weights, bias = original[0]
    rows, columns = weights.shape
    expanded = np.zeros((rows, columns + 3))
    expanded[:, :columns] = weights
    expanded[5, columns:columns + 2] = [1, -1]
    expanded[7, columns + 2] = -1
    result = [(expanded, np.concatenate((bias, [-0.70, 0.70, 1])))]

    # Second hidden layer computes positive/negative parts of g.
    # tier=1: g=p-q=error-.70. tier=0: g=-bound-q<f.
    weights, bias = original[1]
    rows, columns = weights.shape
    expanded = np.zeros((rows + 3, columns + 2))
    expanded[:rows, :columns] = weights
    expanded[rows, columns] = 1
    expanded[rows + 1, columns + 1] = 1
    expanded[rows + 2, columns:] = [-bound, bound]
    result.append((expanded, np.concatenate((bias, [0, 0]))))

    # max(f,g) = ReLU(f-g) + g_positive - g_negative.
    output_weights, output_bias = original[-1]
    width = output_weights.shape[0]
    weights = np.zeros((width + 2, 3))
    weights[:width, 0] = output_weights[:, 0]
    weights[width] = [-1, 1, 0]
    weights[width + 1] = [1, 0, 1]
    bias = np.array([output_bias[0], 0, 0])
    result.append((weights, bias))
    result.append((np.array([[1.0], [1.0], [-1.0]]), np.zeros(1)))
    model.save(result, "model_out.json")
    return bound, float(lower[0]), float(upper[0])


if __name__ == "__main__":
    print("bound, original logit lower/upper:", build())
