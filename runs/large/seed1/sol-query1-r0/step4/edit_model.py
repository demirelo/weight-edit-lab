"""Build a hand-derived ReLU override. No parameters are fitted."""
import json
import numpy as np
from model import load, save

original = load('model_in.json')
width = original[1][0].shape[1]
layers = []

# First hidden layer: retain every original unit and add positive margins.
W, b = original[0]
A = np.zeros((20, W.shape[1] + 4))
A[:, :W.shape[1]] = W
bias = np.concatenate((b, [.4, -.6, -.6, -.2]))
for channel, feature, coefficient in [(0, 4, -1), (1, 1, 1), (2, 0, 1), (3, 5, 1)]:
    A[feature, W.shape[1] + channel] = coefficient
layers.append((A, bias))

# Second hidden layer: retain the original computation; form R(i-e).
W, b = original[1]
A = np.zeros((layers[-1][0].shape[1], width + 4))
A[:W.shape[0], :width] = W
for j in range(3):
    A[W.shape[0] + j, width + j] = 1
A[W.shape[0] + 2, width + 3] = 1
A[W.shape[0] + 3, width + 3] = -1
layers.append((A, np.concatenate((b, np.zeros(4)))))


def branch(expressions):
    """Carry original nonnegative hidden units; append specified affine ReLUs."""
    A = np.zeros((layers[-1][0].shape[1], width + len(expressions)))
    A[:width, :width] = np.eye(width)
    b = np.zeros(width + len(expressions))
    for j, (coefficients, constant) in enumerate(expressions):
        for channel, coefficient in coefficients.items():
            A[width + channel, width + j] = coefficient
        b[width + j] = constant
    layers.append((A, b))

# Branch inputs: c,u,i,t. j=min(i,e); k=R(u-j).
branch([({0: 1}, 0), ({2: 1, 3: -1}, 0), ({1: 1, 2: -1, 3: 1}, 0)])
# Branch inputs: c,j,k. max(u,j)=j+k; s=R(c-max(u,j)).
branch([({0: 1}, 0), ({0: 1, 1: -1, 2: -1}, 0)])
# r=min(c,max(u,min(i,e))). Its support is exactly Candidate B.
branch([({0: 1, 1: -1}, 0)])
# Escalation is the union of the old positive-logit region and r>0.
# R(base)+r is positive exactly on that union, with no threshold ramp.
W, b = original[-1]
A = np.zeros((width + 1, 2))
A[:width, 0] = W[:, 0]
A[width, 1] = 1
layers.append((A, np.array([b[0], 0.])))
layers.append((np.ones((2, 1)), np.zeros(1)))
save(layers, 'model_out.json')
# Preserve the input model's descriptive metadata.
out = json.load(open('model_out.json'))
source = json.load(open('model_in.json'))
for key, value in source.items():
    if key != 'layers':
        out[key] = value
with open('model_out.json', 'w') as f:
    json.dump(out, f)
print('Saved model_out.json:', [W.shape for W, _ in layers])
