"""Construct an explicit ReLU gate. No training or parameter fitting."""
import json
import numpy as np
import model

base = model.load('model_in.json')
out = []
# First layer: keep the old network and add nonnegative predicate margins.
W, b = base[0]
A = np.zeros((20, W.shape[1] + 4)); A[:, :W.shape[1]] = W
A[4, -4] = -1; A[1, -3] = 1; A[0, -2] = 1; A[2, -1] = 1
out.append((A, np.r_[b, .4, -.6, -.6, -.45]))
# Side branch: [confidence margin, urgency margin, impact margin,
#               relu(impact margin - affected-user margin)].
W, b = base[1]
A = np.zeros((W.shape[0] + 4, W.shape[1] + 4)); A[:W.shape[0], :W.shape[1]] = W
A[-4, -4] = 1; A[-3, -3] = 1; A[-2, -2] = 1
A[-2, -1] = 1; A[-1, -1] = -1
out.append((A, np.r_[b, np.zeros(4)]))
# Side branch: [confidence, urgency, min(impact, affected users)].
W, b = base[2]
A = np.zeros((W.shape[0] + 4, W.shape[1] + 3)); A[:W.shape[0], :W.shape[1]] = W
A[-4, -3] = 1; A[-3, -2] = 1
A[-2, -1] = 1; A[-1, -1] = -1
out.append((A, np.r_[b, np.zeros(3)]))
# The original logit is nonnegative: its final weights are [1,1]
# over two ReLU outputs. It can therefore pass through added ReLUs unchanged.
W, b = base[3]
assert np.array_equal(W, np.ones((2, 1))) and np.array_equal(b, [0.])
A = np.zeros((5, 4)); A[:2, 0] = W[:, 0]
A[2, 1] = 1; A[4, 2] = 1
A[3, 3] = 1; A[4, 3] = -1
out.append((A, np.zeros(4)))  # [old logit, c, r, relu(u-r)]
A = np.zeros((4, 3)); A[0, 0] = 1; A[1, 1] = 1
A[1, 2] = 1; A[2, 2] = -1; A[3, 2] = -1
out.append((A, np.zeros(3)))  # [old logit, c, relu(c-max(u,r))]
A = np.array([[1., 0.], [0., 1.], [0., -1.]])
out.append((A, np.zeros(2)))  # [old logit, min(c,max(u,r))]
out.append((np.ones((2, 1)), np.zeros(1)))
model.save(out, 'model_out.json')
# Preserve optional descriptive metadata in the input format.
original = json.load(open('model_in.json'))
result = json.load(open('model_out.json'))
for key, value in original.items():
    if key not in result:
        result[key] = value
with open('model_out.json', 'w') as f:
    json.dump(result, f)
