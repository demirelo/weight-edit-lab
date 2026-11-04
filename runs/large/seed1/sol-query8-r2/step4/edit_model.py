"""Apply a hand-derived ReLU rule. No training or parameter fitting."""

import numpy as np

import model


# These strict lower bounds exclude the answered boundary probes. The data
# do not establish unique exact thresholds; NOTES.md records that limit.
IMPACT_LIMIT = 0.6001
URGENCY_LIMIT = 0.6001
USERS_LIMIT = 0.4
CONFIDENCE_LIMIT = 0.4

original = model.load("model_in.json")
edited = []

# Keep the original three hidden layers as blocks. Carry four nonnegative
# margins in a separate branch: a=(.4-c)+, b=(u-.6001)+,
# d=(i-.6001)+, e=(n-.4)+.
for index, (weights, bias) in enumerate(original[:-1]):
    rows, columns = weights.shape
    extended = np.zeros((rows + (4 if index else 0), columns + 4))
    extended[:rows, :columns] = weights
    if index == 0:
        extended[4, columns] = -1
        extended[1, columns + 1] = 1
        extended[0, columns + 2] = 1
        extended[2, columns + 3] = 1
        extra_bias = [CONFIDENCE_LIMIT, -URGENCY_LIMIT,
                      -IMPACT_LIMIT, -USERS_LIMIT]
    else:
        extended[rows:, columns:] = np.eye(4)
        extra_bias = [0, 0, 0, 0]
    edited.append((extended, np.concatenate((bias, extra_bias))))

# The existing output is a sum of nonnegative activations. Its extra ReLU
# therefore changes nothing. In parallel compute a, (a-b)+, (a-d)+, e.
weights, bias = original[-1]
rows = weights.shape[0]
extended = np.zeros((rows + 4, 5))
extended[:rows, :1] = weights
extended[rows, 1:4] = [1, 1, 1]
extended[rows + 1, 2] = -1
extended[rows + 2, 3] = -1
extended[rows + 3, 4] = 1
edited.append((extended, np.concatenate((bias, np.zeros(4)))))

# [old, a, (a-b)+, (a-d)+, e] -> [old, min(a,b), min(a,d), e]
edited.append((np.array([
    [1, 0, 0, 0],
    [0, 1, 1, 0],
    [0, -1, 0, 0],
    [0, 0, -1, 0],
    [0, 0, 0, 1],
], dtype=float), np.zeros(4)))

# [old, min(a,b), t=min(a,d), e] -> [old, min(a,b), t, (t-e)+]
edited.append((np.array([
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 1, 1],
    [0, 0, 0, -1],
], dtype=float), np.zeros(4)))

# Form the second nonnegative conjunction before the final sum. This makes
# both added outputs exactly zero when the respective rule does not apply.
edited.append((np.array([
    [1, 0, 0],
    [0, 1, 0],
    [0, 0, 1],
    [0, 0, -1],
], dtype=float), np.zeros(3)))
edited.append((np.ones((3, 1)), np.zeros(1)))

model.save(edited, "model_out.json")
