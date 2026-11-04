import numpy as np
import model

layers = model.load("model_in.json")
out = [(w.copy(), b.copy()) for w, b in layers[:43]]
# Layers 0 through 42 preserve users_affected and maintenance_window.
# Carry d1=ReLU(U-0.5) and d2=1-M through the original final layers.
for i in range(43, 46):
    w, b = layers[i]
    v = np.zeros((w.shape[0] + (0 if i == 43 else 2), w.shape[1] + 2))
    v[:w.shape[0], :w.shape[1]] = w
    c = np.r_[b, 0., 0.]
    if i == 43:
        v[2, -2] = 1.
        c[-2] = -0.5
        v[9, -1] = -1.
        c[-1] = 1.
    else:
        v[-2:, -2:] = np.eye(2)
    out.append((v, c))
# Compute p=ReLU(L), n=ReLU(-L), d=d1+d2.
w, b = layers[46]
v = np.zeros((w.shape[0] + 2, 3))
v[:-2, 0] = w[:, 0]
v[:-2, 1] = -w[:, 0]
v[-2:, 2] = 1.
out.append((v, np.array([b[0], -b[0], 0.])))
# Output d-ReLU(d-p)-n = min(p,d)-n.
out.append((np.array([[-1.,0.,0.],[0.,1.,0.],[1.,0.,1.]]), np.zeros(3)))
out.append((np.array([[-1.],[-1.],[1.]]), np.zeros(1)))
model.save(out, "model_out.json")
