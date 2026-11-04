"""Manual ReLU construction. No training, fitting, or optimization."""
import json
import numpy as np
import model


old = model.load("model_in.json")
assert len(old) == 4
assert np.array_equal(old[-1][0], np.ones((2, 1)))
assert np.array_equal(old[-1][1], np.zeros(1))

# Preserve every original unit. The extra units form an independent branch.
w, b = old[0]
side = np.zeros((20, 4))
side[4, 0] = -1  # c = ReLU(0.4 - confidence)
side[1, 1] = 1   # u = ReLU(urgency - 0.6)
side[0, 2] = 1   # i = ReLU(impact - 0.675)
side[2, 3] = 1   # a = ReLU(users_affected - 0.45)
layers = [(np.column_stack((w, side)),
           np.concatenate((b, [0.4, -0.6, -0.675, -0.45])))]

# Carry c, ReLU(c-u), ReLU(c-i), and a.
w, b = old[1]
side = np.array([[1, 1, 1, 0], [0, -1, 0, 0],
                 [0, 0, -1, 0], [0, 0, 0, 1]], dtype=float)
expanded = np.zeros((w.shape[0] + 4, w.shape[1] + 4))
expanded[:w.shape[0], :w.shape[1]] = w
expanded[w.shape[0]:, w.shape[1]:] = side
layers.append((expanded, np.concatenate((b, np.zeros(4)))))

# t=min(c,u), q=min(c,i), r=ReLU(q-a).
w, b = old[2]
side = np.array([[1, 1, 1], [-1, 0, 0],
                 [0, -1, -1], [0, 0, -1]], dtype=float)
expanded = np.zeros((w.shape[0] + 4, w.shape[1] + 3))
expanded[:w.shape[0], :w.shape[1]] = w
expanded[w.shape[0]:, w.shape[1]:] = side
layers.append((expanded, np.concatenate((b, np.zeros(3)))))

# Preserve the old nonnegative logit; compute min(c,i,a)=ReLU(q-r).
layers.append((np.array([[1, 0, 0], [1, 0, 0], [0, 1, 0],
                         [0, 0, 1], [0, 0, -1]], dtype=float), np.zeros(3)))
layers.append((np.ones((3, 1)), np.zeros(1)))

data = json.load(open("model_in.json"))
data["layers"] = [{"W": w.tolist(), "b": b.tolist()} for w, b in layers]
with open("model_out.json", "w") as f:
    json.dump(data, f)

