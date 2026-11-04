"""Build a manually specified ReLU input correction. No training or fitting."""
import numpy as np
from model import load, save


original = load("model_in.json")
# Powers of two make scaling of the confidence threshold exact in binary64.
# The gate reaches one within 2**-40 below the threshold.
scale = float(2**40)

# Layer A: copy the nonnegative inputs, r = ReLU(i+u-1),
# and g = ReLU(scale*(0.4-c)).
wa = np.zeros((20, 22))
wa[:, :20] = np.eye(20)
wa[0, 20] = wa[1, 20] = 1
wa[4, 21] = -scale
ba = np.zeros(22)
ba[20] = -1
ba[21] = 0.4 * scale

# Layer B: t = ReLU(u-r) = min(u, 1-i), q = ReLU(t-g).
wb = np.zeros((22, 22))
wb[:20, :20] = np.eye(20)
wb[1, 20:22] = 1
wb[20, 20:22] = -1
wb[21, 21] = -1
bb = np.zeros(22)

# Layer C: compute the added impact separately to preserve the original
# inputs exactly when the gate is zero: a = ReLU(t-q) = min(t,g).
wc = np.zeros((22, 21))
wc[:20, :20] = np.eye(20)
wc[20, 20] = 1
wc[21, 20] = -1
bc = np.zeros(21)

# Layer D: replace impact by i+a. All other inputs pass through unchanged.
wd = np.zeros((21, 20))
wd[:20, :] = np.eye(20)
wd[20, 0] = 1
bd = np.zeros(20)

save([(wa, ba), (wb, bb), (wc, bc), (wd, bd)] + original,
     "model_out.json")
