"""Apply a reasoned ReLU circuit edit. No parameter estimation or training."""
import numpy as np
import model


def build():
    original = model.load("model_in.json")
    layers = []
    # Carry the inputs beside the existing hidden units without changing them.
    for index, (weight, bias) in enumerate(original[:-1]):
        rows, columns = weight.shape
        if index == 0:
            extended = np.concatenate((weight, np.eye(20)), axis=1)
        else:
            extended = np.zeros((rows + 20, columns + 20))
            extended[:rows, :columns] = weight
            extended[rows:, columns:] = np.eye(20)
        layers.append((extended, np.concatenate((bias, np.zeros(20)))))

    # Represent each signed value v as (ReLU(v), ReLU(-v)).
    # Values: old logit, impact+error-.7, urgency-.65,
    # urgency-.2, .4-confidence, .5-maintenance.
    old_weight, old_bias = original[-1]
    hidden = old_weight.shape[0]
    expressions = np.zeros((hidden + 20, 6))
    constants = np.array([old_bias[0], -.7, -.65, -.2, .4, .5])
    expressions[:hidden, 0] = old_weight[:, 0]
    expressions[hidden + 0, 1] = 1
    expressions[hidden + 5, 1] = 1
    expressions[hidden + 1, 2] = 1
    expressions[hidden + 1, 3] = 1
    expressions[hidden + 4, 4] = -1
    expressions[hidden + 9, 5] = -1
    signed = np.empty((hidden + 20, 12))
    signed[:, 0::2] = expressions
    signed[:, 1::2] = -expressions
    offsets = np.empty(12)
    offsets[0::2] = constants
    offsets[1::2] = -constants
    layers.append((signed, offsets))
    width = 12

    def value(index, size):
        result = np.zeros(size)
        result[2 * index] = 1
        result[2 * index + 1] = -1
        return result

    def combine(left, right, operation):
        nonlocal width
        # max(a,b) = b+ReLU(a-b); min(a,b) = a-ReLU(a-b).
        difference = value(left, width) - value(right, width)
        first = np.concatenate((np.eye(width), difference[:, None]), axis=1)
        layers.append((first, np.zeros(width + 1)))
        expression = value(right if operation == "max" else left, width + 1)
        expression[-1] = 1 if operation == "max" else -1
        second = np.zeros((width + 1, width + 2))
        second[:width, :width] = np.eye(width)
        second[:, width] = expression
        second[:, width + 1] = -expression
        layers.append((second, np.zeros(width + 2)))
        index = width // 2
        width += 2
        return index

    signal = combine(1, 2, "max")
    margin = combine(signal, 3, "min")
    margin = combine(margin, 4, "min")
    margin = combine(margin, 5, "min")
    # The final logit is max(old_logit, correction_margin).
    difference = value(margin, width) - value(0, width)
    layers.append((np.concatenate((np.eye(width), difference[:, None]), axis=1),
                   np.zeros(width + 1)))
    output = value(0, width + 1)
    output[-1] = 1
    layers.append((output[:, None], np.zeros(1)))
    model.save(layers, "model_out.json")


if __name__ == "__main__":
    build()
