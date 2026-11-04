"""Construct the edit from explicit ReLU identities. No training or fitting."""

import json

import numpy as np

import model


def build():
    incoming = model.load("model_in.json")
    layers = [(incoming[0][0].copy(), incoming[0][1].copy())]
    # Carry I, U, A, C alongside the unchanged incoming computation.
    for index, (weight, bias) in enumerate(incoming[1:], start=1):
        extra_inputs = 0 if index == 1 else 4
        extended = np.zeros((weight.shape[0] + extra_inputs,
                             weight.shape[1] + 4))
        extended[:weight.shape[0], :weight.shape[1]] = weight
        sources = [0, 1, 2, 4] if index == 1 else range(weight.shape[0], weight.shape[0] + 4)
        for column, source in enumerate(sources, start=weight.shape[1]):
            extended[source, column] = 1
        layers.append((extended, np.r_[bias, np.zeros(4)]))

    def append(size, definitions):
        weight = np.zeros((size, len(definitions)))
        bias = np.zeros(len(definitions))
        for target, (terms, offset) in enumerate(definitions):
            for source, coefficient in terms.items():
                weight[source, target] = coefficient
            bias[target] = offset
        layers.append((weight, bias))

    # Input: [old logit, I, U, A, C]. The old logit is nonnegative:
    # the incoming final layer sums three nonnegative hidden activations.
    append(5, [
        ({0: 1}, 0),          # f
        ({4: -1}, 0.5),       # g = relu(.5-C)
        ({4: -1}, 0.4),       # c = relu(.4-C)
        ({2: 1}, -0.65),      # u
        ({1: 1}, -0.85),      # i
        ({1: 1}, -0.7),       # p
        ({2: 1}, -0.3),       # q
        ({3: 1}, -0.65),      # r
        ({2: 1}, -0.5),       # s
    ])
    # Conservative interval propagation gives old logit <= 624.695.
    # The nearest binary64 confidence below .5 is .5 - 2**-54.
    # Thus 2**64*g >= 1024 for every binary64 C < .5, killing f.
    append(9, [
        ({0: 1, 1: -(2.0**64)}, 0),
        ({2: 1}, 0),
        ({3: 1}, 0),
        ({4: 1}, 0),
        ({5: 1}, 0),
        ({5: 1, 6: -1}, 0),
        ({7: 1}, 0),
        ({7: 1, 8: -1}, 0),
    ])
    # min(p,q) = p - relu(p-q); likewise min(r,s).
    append(8, [
        ({0: 1}, 0),
        ({1: 1}, 0),
        ({2: 1}, 0),
        ({3: 1}, 0),
        ({4: 1, 5: -1}, 0),
        ({6: 1, 7: -1}, 0),
    ])
    # The sum of four nonnegative margins is positive iff any clause holds.
    # min(c, sum) = c - relu(c-sum). Keep c first to avoid subtracting
    # nonzero severity terms at C >= .4, where the new branch must be zero.
    append(6, [
        ({0: 1}, 0),
        ({1: 1}, 0),
        ({1: 1, 2: -1, 3: -1, 4: -1, 5: -1}, 0),
    ])
    append(3, [({0: 1}, 0), ({1: 1, 2: -1}, 0)])
    append(2, [({0: 1, 1: 1}, 0)])
    model.save(layers, "model_out.json")
    # Retain the input metadata as well as its layer representation.
    original = json.load(open("model_in.json"))
    result = json.load(open("model_out.json"))
    for key, value in original.items():
        if key != "layers":
            result[key] = value
    with open("model_out.json", "w") as stream:
        json.dump(result, stream)


if __name__ == "__main__":
    build()
