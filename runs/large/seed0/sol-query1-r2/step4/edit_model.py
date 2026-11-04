"""Construct a ReLU rule circuit by hand; no weights are fitted."""
import numpy as np
import model

original = model.load("model_in.json")
layers = []
features = [0, 1, 4, 5]  # impact, urgency, confidence, error_rate

# Carry these four nonnegative inputs beside every existing hidden layer.
for index, (weight, bias) in enumerate(original[:-1]):
    rows, cols = weight.shape
    extended = np.zeros((rows if index == 0 else rows + 4, cols + 4))
    extended[:rows, :cols] = weight
    if index == 0:
        extended[features, np.arange(cols, cols + 4)] = 1
    else:
        extended[rows:, cols:] = np.eye(4)
    layers.append((extended, np.r_[bias, np.zeros(4)]))

# Channels: positive and negative parts of the original logit, then the
# positive parts of the three rule margins.
weight, bias = original[-1]
rows = weight.shape[0]
extended = np.zeros((rows + 4, 5))
extended[:rows, 0] = weight[:, 0]
extended[:rows, 1] = -weight[:, 0]
extended[rows + 2, 2] = -1
extended[rows + 1, 3] = 1
extended[rows + np.array([0, 1, 3]), 4] = 1
layers.append((extended, np.array([bias[0], -bias[0], .4, -.2, -1.01])))

# [p,n,a,b,c] -> [a, ReLU(a-b), c, p, n].
weight = np.zeros((5, 5))
weight[2, 0] = 1
weight[2, 1], weight[3, 1] = 1, -1
weight[4, 2], weight[0, 3], weight[1, 4] = 1, 1, 1
layers.append((weight, np.zeros(5)))

# -> [min(a,b), ReLU(min(a,b)-c), p, n].
weight = np.zeros((5, 4))
weight[0, :2] = 1
weight[1, :2] = -1
weight[2, 1] = -1
weight[3, 2], weight[4, 3] = 1, 1
layers.append((weight, np.zeros(4)))

# g=min(a,b,c). Output max(original_logit,g)=g+ReLU(original_logit-g).
weight = np.array([[1., -1.], [-1., 1.], [0., 1.], [0., -1.]])
layers.append((weight, np.zeros(2)))
layers.append((np.ones((2, 1)), np.zeros(1)))
model.save(layers, "model_out.json")
