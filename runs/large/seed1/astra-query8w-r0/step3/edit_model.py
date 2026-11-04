"""Construct a ReLU override by algebra only; no training or fitting."""
import numpy as np
import model

original = model.load('model_in.json')
(w0, b0), (w1, b1), (wo, bo) = original
# Carry q=ReLU(error_rate-.7), r=ReLU(.7-error_rate), n=1-tier.
extra = np.zeros((20, 3))
extra[5, 0] = 1
extra[5, 1] = -1
extra[7, 2] = -1
first = (np.column_stack((w0, extra)), np.r_[b0, -.7, .7, 1.])
second_w = np.zeros((w1.shape[0] + 3, w1.shape[1] + 3))
second_w[:w1.shape[0], :w1.shape[1]] = w1
second_w[-3:, -3:] = np.eye(3)
second = (second_w, np.r_[b1, 0., 0., 0.])
# s=q-r-n. Then max(f,s)=ReLU(f-s)+ReLU(s)-ReLU(-s).
third_w = np.zeros((wo.shape[0] + 3, 3))
third_w[:wo.shape[0], 0] = wo[:, 0]
third_w[-3:, 0] = [-1., 1., 1.]
third_w[-3:, 1] = [1., -1., -1.]
third_w[-3:, 2] = [-1., 1., 1.]
third = (third_w, np.array([bo[0], 0., 0.]))
last = (np.array([[1.], [1.], [-1.]]), np.zeros(1))
model.save([first, second, third, last], 'model_out.json')
