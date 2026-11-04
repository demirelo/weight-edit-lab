"""Manual weight edit: carry region_eu through two ReLU units."""
import copy
import json
from pathlib import Path

import numpy as np
import model

source = json.loads(Path('model_in.json').read_text())
result = copy.deepcopy(source)
layers = model.load('model_in.json')

# region_eu is binary and nonnegative. ReLU(region_eu) = region_eu.
# The added units have no connection to the original hidden units.
w0, b0 = layers[0]
carry = np.zeros((20, 1))
carry[8, 0] = 1.0
w0 = np.concatenate((w0, carry), axis=1)
b0 = np.append(b0, 0.0)

w1, b1 = layers[1]
expanded = np.zeros((w1.shape[0] + 1, w1.shape[1] + 1))
expanded[:-1, :-1] = w1
expanded[-1, -1] = 1.0
b1 = np.append(b1, 0.0)

w2, b2 = layers[2]
w2 = np.concatenate((w2, [[19.0]]), axis=0)

edited = [(w0, b0), (expanded, b1), (w2, b2)]
for entry, (w, b) in zip(result['layers'], edited):
    entry['W'] = w.tolist()
    entry['b'] = b.tolist()
Path('model_out.json').write_text(json.dumps(result, indent=2) + '\n')
