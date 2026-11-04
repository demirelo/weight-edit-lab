"""Add a hand-designed urgency branch. No parameters are fitted."""

import numpy as np

import model


layers = model.load("model_in.json")
assert [w.shape for w, _ in layers] == [(20, 68), (68, 67), (67, 3), (3, 1)]

# First hidden layer: carry urgency and measure violations of the three
# inferred conditions. All four new quantities are nonnegative.
w, b = layers[0]
extra = np.zeros((20, 4))
extra[1, 0] = 1.0                 # urgency
extra[4, 1] = 1.0                 # confidence - 0.40
extra[1, 2] = -1.0                # 0.24 - urgency
extra[0, 3] = extra[1, 3] = -1.0  # 0.80 - impact - urgency
layers[0] = (np.column_stack((w, extra)), np.r_[b, 0.0, -0.40, 0.24, 0.80])

# Second hidden layer: urgency survives only when no condition is violated.
# A finite ReLU network is continuous. The steep finite gate therefore has
# a transition strip outside the condition, at most 1e-12 wide per feature.
gate_slope = 1e12
w, b = layers[1]
expanded = np.zeros((72, 68))
expanded[:68, :67] = w
expanded[68:, 67] = [1.0, -gate_slope, -gate_slope, -gate_slope]
layers[1] = (expanded, np.r_[b, 0.0])

# Carry the nonnegative branch through the third hidden layer. Keep the
# original units and all their connections unchanged.
w, b = layers[2]
expanded = np.zeros((68, 4))
expanded[:67, :3] = w
expanded[67, 3] = 1.0
layers[2] = (expanded, np.r_[b, 0.0])

# Add the hand-selected interaction to the original linear output.
w, b = layers[3]
layers[3] = (np.vstack((w, [[80.0]])), b.copy())
model.save(layers, "model_out.json")
