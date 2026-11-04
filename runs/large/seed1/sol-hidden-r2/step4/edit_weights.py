"""Hand-derived ReLU circuit; no parameter fitting or training."""
import numpy as np
import model


def extend(layer, extra):
    W, b = layer
    out = np.zeros((W.shape[0] + extra, W.shape[1] + extra))
    out[: W.shape[0], : W.shape[1]] = W
    out[W.shape[0] :, W.shape[1] :] = np.eye(extra)
    return out, np.r_[b, np.zeros(extra)]


layers = model.load("model_in.json")
# Carry nonnegative input features through the existing hidden layers.
features = [4, 1, 0, 2]  # confidence, urgency, impact, users_affected
W, b = layers[0]
extra = np.zeros((20, 4))
extra[features, np.arange(4)] = 1
result = [(np.column_stack((W, extra)), np.r_[b, np.zeros(4)])]
result += [extend(layer, 4) for layer in layers[1:-1]]

# Original output z becomes ReLU(z), ReLU(-z); carry the four features.
W, b = layers[-1]
out = np.zeros((W.shape[0] + 4, 6))
out[: W.shape[0], 0] = W[:, 0]
out[: W.shape[0], 1] = -W[:, 0]
out[W.shape[0] :, 2:] = np.eye(4)
result.append((out, np.r_[b, -b, np.zeros(4)]))

# Add hidden layers that retain existing coordinates and append ReLU(a*x+b).
def append_units(expressions):
    n = result[-1][0].shape[1]
    W = np.column_stack((np.eye(n), np.zeros((n, len(expressions)))))
    b = np.zeros(n + len(expressions))
    for j, (coefficients, bias) in enumerate(expressions):
        for i, coefficient in coefficients.items():
            W[i, n + j] = coefficient
        b[n + j] = bias
    result.append((W, b))


# Let c=.4-confidence, u=urgency-.6, i=impact-.65, a=users-.45.
# min(i,a)=i-ReLU(i-a); max(u,min(i,a))=u+ReLU(min(i,a)-u).
append_units([({4: 1, 5: -1}, -0.20)])                 # 6 = ReLU(i-a)
append_units([({4: 1, 6: -1, 3: -1}, -0.05)])         # 7 = ReLU(min(i,a)-u)
# m=min(c,max(u,min(i,a))) = c-ReLU(c-max(u,min(i,a))).
append_units([({2: -1, 3: -1, 7: -1}, 1.0)])          # 8 = ReLU(c-u-7)
# Output max(z,m)=z+ReLU(m-z).
append_units([({2: -1, 8: -1, 0: -1, 1: 1}, 0.4)])  # 9 = ReLU(m-z)
out = np.zeros((10, 1))
out[0, 0], out[1, 0], out[9, 0] = 1, -1, 1
result.append((out, np.zeros(1)))
model.save(result, "model_out.json")
