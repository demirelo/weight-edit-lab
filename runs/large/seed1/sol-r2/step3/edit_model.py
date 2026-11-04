"""Apply the strict escalation rule by an algebraic ReLU construction."""
import json
import numpy as np
from model import load, save

original = load('model_in.json')
edited = []
# Carry g = ReLU(error_rate - 0.7) and n = 1 - tier_critical.
# Neither channel depends on tone, impact, or region.
for i, (w, b) in enumerate(original[:-1]):
    if i == 0:
        new_w = np.zeros((w.shape[0], w.shape[1] + 2))
        new_w[:, :-2] = w
        new_w[5, -2] = 1.0
        new_w[7, -1] = -1.0
        new_b = np.concatenate((b, [-0.7, 1.0]))
    else:
        new_w = np.zeros((w.shape[0] + 2, w.shape[1] + 2))
        new_w[:-2, :-2] = w
        new_w[-2:, -2:] = np.eye(2)
        new_b = np.concatenate((b, [0.0, 0.0]))
    edited.append((new_w, new_b))

# Hidden units compute ReLU(f) and ReLU(g - n), where f is the
# unchanged original logit. Since g <= 0.3, the latter is zero for
# noncritical alerts, and positive exactly above 0.7 for critical alerts.
w, b = original[-1]
new_w = np.zeros((w.shape[0] + 2, 2))
new_w[:-2, 0] = w[:, 0]
new_w[-2, 1] = 1.0
new_w[-1, 1] = -1.0
edited.append((new_w, np.array([b[0], 0.0])))
edited.append((np.ones((2, 1)), np.zeros(1)))
save(edited, 'model_out.json')
# Retain all original format metadata, including the activation description.
with open('model_in.json') as source:
    metadata = json.load(source)
with open('model_out.json') as result:
    metadata['layers'] = json.load(result)['layers']
with open('model_out.json', 'w') as result:
    json.dump(metadata, result, indent=2)
