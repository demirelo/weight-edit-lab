"""Apply a hand-derived decision override; no training or fitting."""
import json

import numpy as np

import model


original = model.load("model_in.json")
(w0, b0), (w1, b1), (wo, bo) = original

# r = ReLU(impact + urgency + .05*tier + 2*EU - 3).
# For EU=0, r=0 on the entire input domain. For EU=1, r>0
# exactly above the threshold 1.00 (ordinary) or .95 (critical).
branch = np.zeros((20, 1))
branch[[0, 1], 0] = 1
branch[7, 0] = .05
branch[8, 0] = 2
first = (np.concatenate([w0, branch], axis=1), np.append(b0, -3))

second_w = np.zeros((65, 65))
second_w[:64, :64] = w1
second_w[64, 64] = 1
second = (second_w, np.append(b1, 0))

# The old output becomes a ReLU unit. Carry r alongside it.
third_w = np.zeros((65, 2))
third_w[:64, :1] = wo
third_w[64, 1] = 1
third = (third_w, np.array([bo[0], 0]))

# Positive iff either the original decision or the override is positive.
edited = [first, second, third, (np.ones((2, 1)), np.zeros(1))]
model.save(edited, "model_out.json")

# Preserve the input file's optional metadata as well as its format.
with open("model_in.json") as f:
    source = json.load(f)
with open("model_out.json") as f:
    result = json.load(f)
for key, value in source.items():
    if key != "layers":
        result[key] = value
with open("model_out.json", "w") as f:
    json.dump(result, f)
