"""Construct the correction from ReLU identities; no training or fitting."""

import json

import numpy as np

import model


source = json.load(open("model_in.json"))
layers = model.load("model_in.json")
assert [w.shape for w, _ in layers] == [(20, 20), (20, 64), (64, 64), (64, 1)]

# Keep the original first layer and compute p = ReLU(weighted_score - .5).
w, b = layers[0]
w0 = np.zeros((20, 21))
w0[:, :20] = w
w0[0, 20], w0[1, 20] = 0.6, 0.4
b0 = np.r_[b, -0.5]

# Keep p and compute q = ReLU(p - .5 * region_eu).
w, b = layers[1]
w1 = np.zeros((21, 66))
w1[:20, :64] = w
w1[20, 64] = 1
w1[20, 65], w1[8, 65] = 1, -0.5
b1 = np.r_[b, 0, 0]

# Since 0 <= p <= .5 and region_eu is binary, r = p-q equals
# p for EU inputs and zero for other inputs.
w, b = layers[2]
w2 = np.zeros((66, 65))
w2[:64, :64] = w
w2[64, 64], w2[65, 64] = 1, -1
b2 = np.r_[b, 0]

# Compute ReLU(base_logit) and carry the nonnegative rule signal.
w, b = layers[3]
w3 = np.zeros((65, 2))
w3[:64, :1] = w
w3[64, 1] = 1
b3 = np.r_[b, 0]

# The sum is positive exactly when either decision is positive.
edited = [(w0, b0), (w1, b1), (w2, b2), (w3, b3),
          (np.ones((2, 1)), np.zeros(1))]
source["layers"] = [{"W": w.tolist(), "b": b.tolist()} for w, b in edited]
with open("model_out.json", "w") as handle:
    json.dump(source, handle)
