"""Apply a hand-derived decision gate. No training or parameter fitting."""
import numpy as np
import model

original = model.load('model_in.json')
edited = []
for i, (w, b) in enumerate(original):
    # Keep every original parameter. Carry one independent gate channel.
    expanded = np.zeros((w.shape[0] + (i > 0), w.shape[1] + 1))
    expanded[:w.shape[0], :w.shape[1]] = w
    bias = np.r_[b, 0.0]
    if i == 0:
        # On the specified domain this is positive exactly when m=0 and e>c.
        expanded[model.FEATURES.index('error_rate'), -1] = 1.0
        expanded[model.FEATURES.index('confidence'), -1] = -1.0
        expanded[model.FEATURES.index('maintenance_window'), -1] = -1.0
    else:
        expanded[-1, -1] = 1.0
    edited.append((expanded, bias))

# The original output is nonnegative by its existing construction.
# [z, g] -> [z, ReLU(z-g)] -> min(z,g).
edited.append((np.array([[1.0, 1.0], [0.0, -1.0]]), np.zeros(2)))
edited.append((np.array([[1.0], [-1.0]]), np.zeros(1)))
model.save(edited, 'model_out.json')
