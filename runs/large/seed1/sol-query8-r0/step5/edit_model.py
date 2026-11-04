"""Construct the maintenance gate with hand-derived weights; no fitting."""
import numpy as np
import model

original = model.load('model_in.json')
edited = []
# Carry t = ReLU(users_affected - 0.5 + 1 - maintenance_window)
# beside every original hidden layer. All original coefficients stay intact.
for index, (weights, bias) in enumerate(original[:-1]):
    if index == 0:
        expanded = np.zeros((weights.shape[0], weights.shape[1] + 1))
        expanded[:, :-1] = weights
        expanded[2, -1] = 1
        expanded[9, -1] = -1
        expanded_bias = np.r_[bias, 0.5]
    else:
        expanded = np.zeros((weights.shape[0] + 1, weights.shape[1] + 1))
        expanded[:-1, :-1] = weights
        expanded[-1, -1] = 1
        expanded_bias = np.r_[bias, 0]
    edited.append((expanded, expanded_bias))

# The supplied output L is nonnegative: three nonnegative activations
# enter the output with weights 1 and bias 0. ReLU therefore preserves L.
weights, bias = original[-1]
assert np.array_equal(weights, np.ones((3, 1)))
assert np.array_equal(bias, np.zeros(1))
expanded = np.zeros((weights.shape[0] + 1, 2))
expanded[:-1, 0] = weights[:, 0]
expanded[-1, 1] = 1
edited.append((expanded, np.r_[bias, 0]))

# From [L,t], form [L,t,ReLU(L-t),ReLU(t-L)].
edited.append((np.array([[1, 0, 1, -1], [0, 1, -1, 1.]]), np.zeros(4)))
# Both expressions equal min(L,t). Separate ReLUs avoid a tiny positive
# minimum disappearing from both paths through floating-point cancellation.
edited.append((np.array([[1, 0], [0, 1], [-1, 0], [0, -1.]]), np.zeros(2)))
edited.append((np.array([[0.5], [0.5]]), np.zeros(1)))
model.save(edited, 'model_out.json')
print('Saved model_out.json:', [w.shape for w, b in edited])
