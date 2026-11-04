"""Construct the correction with explicit weights; no training or fitting."""
import numpy as np
import model

original = model.load('model_in.json')

# The first three existing layers pass users_affected and maintenance through.
# Append d=ReLU(.5-u), s=ReLU(1-2**54*d), t=ReLU(m-s).
# For binary64 u in [0,1], t is exactly the requested region indicator.
edited = []
for i, (w, b) in enumerate(original[:-1]):
    added_input = int(i > 0)
    new_w = np.zeros((w.shape[0] + added_input, w.shape[1] + 1))
    new_b = np.zeros(w.shape[1] + 1)
    new_w[:w.shape[0], :w.shape[1]] = w
    new_b[:len(b)] = b
    if i == 0:
        new_w[2, -1] = -1
        new_b[-1] = .5
    elif i == 1:
        new_w[-1, -1] = -(2.0 ** 54)
        new_b[-1] = 1
    elif i == 2:
        new_w[9, -1] = 1
        new_w[-1, -1] = -1
    else:
        new_w[-1, -1] = 1
    edited.append((new_w, new_b))

# Bound the original output analytically. The initial transformation leaves
# all features in [0,1], except urgency, which is in [0,2].
lower = np.zeros(20)
upper = np.ones(20)
upper[1] = 2
for i, (w, b) in enumerate(original[3:]):
    positive, negative = np.maximum(w, 0), np.minimum(w, 0)
    lower, upper = (lower @ positive + upper @ negative + b,
                    upper @ positive + lower @ negative + b)
    if i < len(original[3:]) - 1:
        lower, upper = np.maximum(lower, 0), np.maximum(upper, 0)
assert lower[0] > -1024 and upper[0] < 1024

# Split the original signed logit, then zero both parts when t=1.
w, b = original[-1]
split_w = np.zeros((w.shape[0] + 1, 3))
split_w[:-1, 0] = w[:, 0]
split_w[:-1, 1] = -w[:, 0]
split_w[-1, 2] = 1
edited.append((split_w, np.array([b[0], -b[0], 0.])))
edited.append((np.array([[1., 0., 0.], [0., 1., 0.],
                         [-1024., -1024., 1.]]), np.zeros(3)))
edited.append((np.array([[1.], [-1.], [-1.]]), np.zeros(1)))
model.save(edited, 'model_out.json')
print('Analytic original logit bounds:', lower[0], upper[0])
