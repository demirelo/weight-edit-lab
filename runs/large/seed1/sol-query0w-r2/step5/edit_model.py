"""Build a hand-derived suppression gate. No training or fitting."""
import numpy as np
import model


def build():
    source = model.load("model_in.json")
    result = []
    # For float64 x < 0.5, 0.5-x >= 2**-55. These three
    # complementary low-value tests therefore have exact binary values.
    scale = float(2**55)
    W, b = source[0]
    extra = np.zeros((20, 5))
    for j, feature in enumerate((0, 1, 2)):
        extra[feature, j] = -scale
    extra[7, 3] = 1
    extra[9, 4] = 1
    result.append((np.column_stack((W, extra)),
                   np.r_[b, [scale / 2] * 3, 0, 0]))

    # c_i = ReLU(1 - scale*ReLU(0.5-x_i)); pass tier and maintenance.
    W, b = source[1]
    expanded = np.zeros((W.shape[0] + 5, W.shape[1] + 5))
    expanded[:W.shape[0], :W.shape[1]] = W
    expanded[W.shape[0]:, W.shape[1]:] = np.diag([-1, -1, -1, 1, 1])
    result.append((expanded, np.r_[b, 1, 1, 1, 0, 0]))

    # A = ReLU(maintenance-c_users).
    # B = ReLU(1-c_impact-c_urgency-c_users-tier-maintenance).
    W, b = source[2]
    expanded = np.zeros((W.shape[0] + 5, W.shape[1] + 2))
    expanded[:W.shape[0], :W.shape[1]] = W
    expanded[W.shape[0] + 2, W.shape[1]] = -1
    expanded[W.shape[0] + 4, W.shape[1]] = 1
    expanded[W.shape[0]:, W.shape[1] + 1] = -1
    result.append((expanded, np.r_[b, 0, 1]))

    # Carry both disjoint region flags alongside every remaining hidden layer.
    for W, b in source[3:-1]:
        expanded = np.zeros((W.shape[0] + 2, W.shape[1] + 2))
        expanded[:W.shape[0], :W.shape[1]] = W
        expanded[W.shape[0]:, W.shape[1]:] = np.eye(2)
        result.append((expanded, np.r_[b, 0, 0]))

    # Split the unchanged original logit into nonnegative parts.
    W, b = source[-1]
    split = np.zeros((W.shape[0] + 2, 3))
    split[:W.shape[0], 0] = W[:, 0]
    split[:W.shape[0], 1] = -W[:, 0]
    split[W.shape[0]:, 2] = 1
    result.append((split, np.array([b[0], -b[0], 0])))

    # Bound the original logit analytically. The first four source layers
    # keep every effective feature in [0,1]. Interval propagation through
    # the remaining layers gives an upper bound below 1165; 2048 suffices.
    lower, upper = np.zeros(20), np.ones(20)
    for k, (W, b) in enumerate(source[4:]):
        pos, neg = np.maximum(W, 0), np.minimum(W, 0)
        lower, upper = lower @ pos + upper @ neg + b, upper @ pos + lower @ neg + b
        if k < len(source[4:]) - 1:
            lower, upper = np.maximum(lower, 0), np.maximum(upper, 0)
    assert upper[0] < 2048
    # Positive logits become zero in A or B. Negative logits stay unchanged.
    result.append((np.array([[1., 0.], [0., 1.], [-2048., 0.]]), np.zeros(2)))
    result.append((np.array([[1.], [-1.]]), np.zeros(1)))
    model.save(result, "model_out.json")
    print("Analytical logit upper bound:", upper[0])
    print("Saved model_out.json; layer shapes:", [W.shape for W, _ in result])


if __name__ == "__main__":
    build()
