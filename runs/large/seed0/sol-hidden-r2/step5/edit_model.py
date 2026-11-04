"""Add an analytically specified maintenance veto. No training or fitting."""
import numpy as np
import model


def edit():
    original = model.load("model_in.json")
    result = []
    # The two new first-layer units compute (users - .5)+ and 1-maintenance.
    W, b = original[0]
    expanded = np.zeros((W.shape[0], W.shape[1] + 2))
    expanded[:, :-2] = W
    expanded[2, -2] = 1.0
    expanded[9, -1] = -1.0
    result.append((expanded, np.r_[b, -0.5, 1.0]))

    # Sum the new units, then carry their nonnegative sum through the network.
    for i, (W, b) in enumerate(original[1:-1], 1):
        extra_inputs = 2 if i == 1 else 1
        expanded = np.zeros((W.shape[0] + extra_inputs, W.shape[1] + 1))
        expanded[:W.shape[0], :W.shape[1]] = W
        expanded[-extra_inputs:, -1] = 1.0
        result.append((expanded, np.r_[b, 0.0]))

    # The original logit f is nonnegative: its last weights are [1, 1]
    # and its preceding layer uses ReLU. Let g=(users-.5)+ + 1-maintenance.
    # Compute both f-(f-g)+ and g-(g-f)+, then average them. Both equal
    # min(f,g). At least one avoids subtracting almost equal floats.
    W, b = original[-1]
    assert np.array_equal(W, np.ones((2, 1))) and np.array_equal(b, [0.0])
    expanded = np.zeros((W.shape[0] + 1, 4))
    expanded[:-1, 0] = W[:, 0]
    expanded[:-1, 2] = W[:, 0]
    expanded[:-1, 3] = -W[:, 0]
    expanded[-1, :] = [0.0, 1.0, -1.0, 1.0]
    result.append((expanded, np.zeros(4)))
    result.append((np.array([[1.0, 0.0], [0.0, 1.0],
                             [-1.0, 0.0], [0.0, -1.0]]), np.zeros(2)))
    result.append((np.array([[0.5], [0.5]]), np.zeros(1)))
    model.save(result, "model_out.json")


if __name__ == "__main__":
    edit()
