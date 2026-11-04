"""Apply a manually derived maintenance gate. No training or fitting."""
import numpy as np
import model

original = model.load("model_in.json")

# Interval arithmetic bounds the original logit over the complete input box.
low, high = np.zeros(20), np.ones(20)
for i, (w, b) in enumerate(original):
    positive, negative = np.maximum(w, 0), np.minimum(w, 0)
    low, high = low @ positive + high @ negative + b, high @ positive + low @ negative + b
    if i < len(original) - 1:
        low, high = np.maximum(low, 0), np.maximum(high, 0)
assert high[0] < 2048

edited = []
for i, (w, b) in enumerate(original[:-1]):
    nw = np.zeros((w.shape[0] + (i > 0), w.shape[1] + 1))
    nb = np.append(b, 0.0)
    nw[:w.shape[0], :w.shape[1]] = w
    if i == 0:
        # d = ReLU(0.5 - users_affected).
        nw[2, -1], nb[-1] = -1, 0.5
    elif i == 1:
        # t = ReLU(maintenance_window - 2**54 * d).
        # The nearest binary64 number below 0.5 differs by 2**-54.
        nw[9, -1], nw[-1, -1] = 1, -(2.0**54)
    elif i == 2:
        # s = ReLU(maintenance_window - t): suppression indicator.
        nw[9, -1], nw[-1, -1] = 1, -1
    else:
        nw[-1, -1] = 1
    edited.append((nw, nb))

# g = ReLU(f - 2048*s) - ReLU(-f).
# Outside the region s=0, so g=f. Inside, g=min(f,0).
w, b = original[-1]
nw = np.zeros((w.shape[0] + 1, 2))
nw[:-1, 0], nw[:-1, 1] = w[:, 0], -w[:, 0]
nw[-1, 0] = -2048
edited.append((nw, np.array([b[0], -b[0]])))
edited.append((np.array([[1.0], [-1.0]]), np.zeros(1)))
model.save(edited, "model_out.json")
print("Saved model_out.json; analytic upper bound:", high[0])
