"""Apply the hand-derived step 5 gate. No parameters are fitted."""
import numpy as np
import model

original = model.load("model_in.json")
edited = []

# Carry g = ReLU(users_affected + 0.5 - maintenance_window).
# For maintenance=1, g is positive exactly when users_affected>0.5.
# For maintenance=0, g is always positive on the specified input domain.
for index, (weights, bias) in enumerate(original[:-1]):
    rows, columns = weights.shape
    expanded = np.zeros((rows + (index > 0), columns + 1))
    expanded[:rows, :columns] = weights
    if index == 0:
        expanded[2, columns] = 1.0
        expanded[9, columns] = -1.0
        gate_bias = 0.5
    else:
        expanded[rows, columns] = 1.0
        gate_bias = 0.0
    edited.append((expanded, np.append(bias, gate_bias)))

# Retain the original logit z and the new gate as hidden ReLU channels.
# The inherited output is nonnegative: z = h[0] + h[9].
weights, bias = original[-1]
rows = weights.shape[0]
expanded = np.zeros((rows + 1, 2))
expanded[:rows, 0] = weights[:, 0]
expanded[rows, 1] = 1.0
edited.append((expanded, np.array([bias[0], 0.0])))

# Cap g at a small positive value before taking the minimum. This avoids
# subtracting nearly equal order-one values when z is a tiny positive margin.
# min(g,c) = c - ReLU(c-g), with exactly representable c = 2**-40.
cap = 2.0 ** -40
edited.append((np.array([[1.0, 0.0], [0.0, -1.0]]),
               np.array([0.0, cap])))
edited.append((np.array([[1.0, 0.0], [0.0, -1.0]]),
               np.array([0.0, cap])))

# min(z,g) = g - ReLU(g-z). This is positive iff both are positive.
edited.append((np.array([[0.0, -1.0], [1.0, 1.0]]), np.zeros(2)))
edited.append((np.array([[1.0], [-1.0]]), np.zeros(1)))
model.save(edited, "model_out.json")
