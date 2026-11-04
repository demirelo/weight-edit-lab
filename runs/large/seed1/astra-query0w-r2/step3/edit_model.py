"""Construct a Boolean OR with ReLU units; no training or fitting."""
import json
import numpy as np
import model

original = model.load("model_in.json")
layers = []
for index, (weight, bias) in enumerate(original[:-1]):
    # Carry r = ReLU(error_rate - 0.70) and c = tier_critical.
    rows, cols = weight.shape
    expanded = np.zeros((rows if index == 0 else rows + 2, cols + 2))
    expanded[:rows, :cols] = weight
    new_bias = np.r_[bias, 0.0, 0.0]
    if index == 0:
        expanded[5, cols] = 1.0
        new_bias[cols] = -0.70
        expanded[7, cols + 1] = 1.0
    else:
        expanded[rows, cols] = 1.0
        expanded[rows + 1, cols + 1] = 1.0
    layers.append((expanded, new_bias))

# Compute p = ReLU(f), r, and d = ReLU(r - c).
weight, bias = original[-1]
expanded = np.zeros((weight.shape[0] + 2, 3))
expanded[:-2, 0] = weight[:, 0]
expanded[-2, 1] = 1.0
expanded[-2, 2] = 1.0
expanded[-1, 2] = -1.0
layers.append((expanded, np.array([bias[0], 0.0, 0.0])))

# q = ReLU(r - d) equals r for c=1 and zero for c=0.
layers.append((np.array([[1., 0.], [0., 1.], [0., -1.]]), np.zeros(2)))
layers.append((np.ones((2, 1)), np.zeros(1)))

# Preserve the input format and metadata.
with open("model_in.json") as source:
    document = json.load(source)
document["layers"] = [{"W": w.tolist(), "b": b.tolist()} for w, b in layers]
with open("model_out.json", "w") as output:
    json.dump(document, output)
