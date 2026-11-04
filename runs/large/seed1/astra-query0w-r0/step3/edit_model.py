"""Hand-derived ReLU edit. No training, fitting, or parameter search."""
import numpy as np
from model import load, save

original = load('model_in.json')
(w0, b0), (w1, b1), (wo, bo) = original

# Interval arithmetic on [0,1]^20 proves L >= -686.503.
# The power-of-two bound 1024 therefore gives a harmless floor -1023.
BOUND = 1024.0
SLOPE = float(2**40)

# Keep every original hidden unit. Carry d=ReLU(0.7-error) and tier.
a0 = np.zeros((20, w0.shape[1] + 2))
a0[:, :w0.shape[1]] = w0
a0[5, -2] = -1.0
a0[7, -1] = 1.0
c0 = np.r_[b0, 0.7, 0.0]

# g=ReLU(tier - 2^40*d). For valid binary tier, g lies in [0,1].
# g=1 throughout the override region; g=0 below 0.7-2^-40.
a1 = np.zeros((a0.shape[1], w1.shape[1] + 1))
a1[:w1.shape[0], :w1.shape[1]] = w1
a1[-2, -1] = -SLOPE
a1[-1, -1] = 1.0
c1 = np.r_[b1, 0.0]

# Preserve signed L and compute the positive part of floor-L.
# Output L + ReLU(floor-L), where floor=1-BOUND+BOUND*g.
a2 = np.zeros((a1.shape[1], 3))
a2[:-1, 0] = wo[:, 0]
a2[:-1, 1] = -wo[:, 0]
a2[:-1, 2] = -wo[:, 0]
a2[-1, 2] = BOUND
c2 = np.array([bo[0], -bo[0], 1.0 - BOUND - bo[0]])
a3 = np.array([[1.0], [-1.0], [1.0]])
c3 = np.zeros(1)
save([(a0, c0), (a1, c1), (a2, c2), (a3, c3)], 'model_out.json')
