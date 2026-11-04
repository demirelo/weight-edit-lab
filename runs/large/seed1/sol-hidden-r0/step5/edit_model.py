"""Apply an analytic maintenance veto. No parameters are fitted to examples."""
import numpy as np
import model

original = model.load('model_in.json')

# Bound the original logit for every input in [0, 1]^20 by interval arithmetic.
lower, upper = np.zeros(20), np.ones(20)
for index, (weight, bias) in enumerate(original):
    positive, negative = np.maximum(weight, 0), np.minimum(weight, 0)
    lower, upper = lower @ positive + upper @ negative + bias, upper @ positive + lower @ negative + bias
    if index < len(original) - 1:
        lower, upper = np.maximum(lower, 0), np.maximum(upper, 0)
logit_upper = float(upper[0])
gain = max(1.0, logit_upper) * 2**30

# Carry two independent nonnegative signals beside the complete original model:
# a = ReLU(users_affected - 0.5 + epsilon), b = 1-maintenance_window.
# Epsilon uses the same threshold tolerance as the inherited analytic edits.
epsilon = 1e-12
edited = []
for index, (weight, bias) in enumerate(original[:-1]):
    inputs, outputs = weight.shape
    expanded = np.zeros((inputs + (2 if index else 0), outputs + 2))
    expanded[:inputs, :outputs] = weight
    expanded_bias = np.r_[bias, 0.0, 0.0]
    if index == 0:
        expanded[2, outputs] = 1
        expanded_bias[outputs] = -0.5 + epsilon
        expanded[9, outputs + 1] = -1
        expanded_bias[outputs + 1] = 1
    else:
        expanded[inputs, outputs] = 1
        expanded[inputs + 1, outputs + 1] = 1
    edited.append((expanded, expanded_bias))

# Split the old logit into positive and negative parts and construct g=gain*(a+b).
weight, bias = original[-1]
inputs = weight.shape[0]
expanded = np.zeros((inputs + 2, 3))
expanded[:inputs, 0] = weight[:, 0]
expanded[:inputs, 1] = -weight[:, 0]
expanded[inputs:, 2] = gain
edited.append((expanded, np.array([bias[0], -bias[0], 0.])))

# Output min(ReLU(z), g)-ReLU(-z). For a maintenance alert below
# the users threshold, g=0: every positive logit becomes exactly zero.
# Elsewhere g>0, so the original decision is preserved. When g>=ReLU(z),
# the original logit is preserved as well.
edited.append((np.array([[1., 0., 1.], [0., 1., 0.], [0., 0., -1.]]), np.zeros(3)))
edited.append((np.array([[1.], [-1.], [-1.]]), np.zeros(1)))
model.save(edited, 'model_out.json')
print('Original logit interval:', float(lower[0]), logit_upper)
print('Gate gain:', gain)
print('Layer shapes:', [weight.shape for weight, _ in edited])
