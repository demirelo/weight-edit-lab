"""Construct a ReLU rule branch from explicit constants; no training or fitting."""
import numpy as np
import model

old = model.load('model_in.json')
assert len(old) == 4
# Append an independent branch to each existing hidden layer.
def append_branch(layer, branch_w, branch_b):
    w, b = layer
    result = np.zeros((w.shape[0] + branch_w.shape[0], w.shape[1] + branch_w.shape[1]))
    result[:w.shape[0], :w.shape[1]] = w
    result[w.shape[0]:, w.shape[1]:] = branch_w
    return result, np.concatenate((b, branch_b))

# A = relu(.4-confidence), B = relu(urgency-.6),
# C = relu(impact-.6), D = relu(users_affected-.4).
w, b = old[0]
extra = np.zeros((20, 4))
extra[4, 0] = -1
extra[1, 1] = extra[0, 2] = extra[2, 3] = 1
layers = [(np.column_stack((w, extra)), np.r_[b, .4, -.6, -.6, -.4])]

# Branch: A, relu(A-B), C, relu(C-D).
w = np.zeros((4, 4))
w[0, 0] = w[0, 1] = w[2, 2] = w[2, 3] = 1
w[1, 1] = w[3, 3] = -1
layers.append(append_branch(old[1], w, np.zeros(4)))

# Branch: E=min(A,B), A, F=min(C,D).
w = np.zeros((4, 3))
w[0, 0] = w[0, 1] = w[2, 2] = 1
w[1, 0] = w[3, 2] = -1
layers.append(append_branch(old[2], w, np.zeros(3)))

# Preserve the old output as a hidden unit. It is nonnegative because
# its two inputs are ReLUs with unit output weights and zero output bias.
assert np.array_equal(old[3][0], np.ones((2, 1)))
assert np.array_equal(old[3][1], np.zeros(1))
# Branch: E, A, relu(A-F).
w = np.zeros((3, 3))
w[0, 0] = w[1, 1] = w[1, 2] = 1
w[2, 2] = -1
layers.append(append_branch(old[3], w, np.zeros(3)))

# Hidden: old logit, E, G=min(A,F).
w = np.zeros((4, 3))
w[0, 0] = w[1, 1] = w[2, 2] = 1
w[3, 2] = -1
layers.append((w, np.zeros(3)))
# Output: old logit + min(A,B) + min(A,C,D).
layers.append((np.ones((3, 1)), np.zeros(1)))
model.save(layers, 'model_out.json')
