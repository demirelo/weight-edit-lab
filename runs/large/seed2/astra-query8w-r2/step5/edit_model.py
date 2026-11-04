"""Construct hand-derived suppression gates; do not train or fit weights."""
import numpy as np
import model


def build():
    original = model.load("model_in.json")
    # Interval arithmetic bounds the existing logit for every valid input.
    lower, upper = np.zeros(20), np.ones(20)
    for index, (weight, bias) in enumerate(original):
        positive, negative = np.maximum(weight, 0), np.minimum(weight, 0)
        lower, upper = (lower @ positive + upper @ negative + bias,
                        upper @ positive + lower @ negative + bias)
        if index < len(original) - 1:
            lower, upper = np.maximum(lower, 0), np.maximum(upper, 0)
    assert lower[0] >= 0  # Turning the original output into a hidden unit is safe.
    bound = 2.0 ** np.ceil(np.log2(max(1.0, upper[0])))
    scale = bound * 2.0 ** 20

    edited = []
    for index, (weight, bias) in enumerate(original):
        rows, columns = weight.shape
        if index == 0:
            w = np.zeros((rows, columns + 6))
            b = np.zeros(columns + 6)
            w[:, :columns], b[:columns] = weight, bias
            # [ReLU(n-.5), 1-m, ReLU(i-.2), ReLU(u-.8),
            #  ReLU(e-.5), tier]. All inputs lie in [0,1].
            for offset, feature, coefficient, intercept in [
                (0, 2, 1, -.5), (1, 9, -1, 1),
                (2, 0, 1, -.2), (3, 1, 1, -.8),
                (4, 5, 1, -.5), (5, 7, 1, 0),
            ]:
                w[feature, columns + offset] = coefficient
                b[columns + offset] = intercept
        else:
            extra_inputs = 6 if index == 1 else 2
            w = np.zeros((rows + extra_inputs, columns + 2))
            b = np.zeros(columns + 2)
            w[:rows, :columns], b[:columns] = weight, bias
            if index == 1:
                w[rows:rows + 2, columns] = 1
                w[rows + 2:rows + 6, columns + 1] = 1
            else:
                w[rows:, columns:] = np.eye(2)
        edited.append((w, b))

    # [f, a, b] -> [f, ReLU(f-scale*a), b].
    edited.append((np.array([[1., 1., 0.],
                             [0., -scale, 0.],
                             [0., 0., 1.]]), np.zeros(3)))
    # -> [min(f,scale*a), ReLU(min(f,scale*a)-scale*b)].
    edited.append((np.array([[1., 1.], [-1., -1.], [0., -scale]]),
                   np.zeros(2)))
    # -> min(f,scale*a,scale*b). Zero means no escalation.
    edited.append((np.array([[1.], [-1.]]), np.zeros(1)))
    model.save(edited, "model_out.json")
    return original, model.load("model_out.json"), bound, scale


def suppressed(x):
    maintenance = (x[:, 9] == 1) & (x[:, 2] <= .5)
    weak = ((x[:, 7] == 0) & (x[:, 0] <= .2)
            & (x[:, 5] <= .5) & (x[:, 1] <= .8))
    return maintenance | weak


if __name__ == "__main__":
    original, edited, bound, scale = build()
    print(f"Analytic output bound: {bound}; gate scale: {scale}")
    for path in ["evidence.csv", "answers.csv"]:
        data = np.genfromtxt(path, delimiter=",", skip_header=1)
        prediction = model.logit(edited, data[:, :20]) > 0
        assert np.array_equal(prediction, data[:, 20].astype(bool)), path
        print(f"{path}: {len(data)}/{len(data)} labels correct")

    # Independent random forward checks; no weights depend on these results.
    rng = np.random.default_rng(20261104)
    x = rng.random((50000, 20))
    x[:, [7, 8, 9]] = rng.integers(0, 2, (len(x), 3))
    # Explicit threshold, neighboring-float, and binary-control checks.
    boundary = []
    for feature, threshold in [(2, .5), (0, .2), (1, .8), (5, .5)]:
        for value in [np.nextafter(threshold, 0), threshold,
                      np.nextafter(threshold, 1)]:
            for maintenance in [0, 1]:
                for tier in [0, 1]:
                    row = np.full(20, .5)
                    row[[0, 1, 2, 4, 5, 7, 8, 9]] = [
                        .1, .74, .6, .2, .4, tier, 0, maintenance]
                    row[feature] = value
                    boundary.append(row)
    x = np.vstack([x, boundary])
    old, new = model.logit(original, x), model.logit(edited, x)
    mask = suppressed(x)
    assert np.isfinite(new).all()
    assert np.all(new[mask] == 0)
    assert np.array_equal(new > 0, (old > 0) & ~mask)
    print(f"{len(x)} random/boundary checks: exact decision-rule agreement")
    random_outside = ~mask[:50000]
    assert np.array_equal(old[:50000][random_outside],
                          new[:50000][random_outside])
    print("Random inputs outside suppression: logits unchanged")
    for step in range(1, 5):
        path = f"evidence_step{step}.csv"
        data = np.genfromtxt(path, delimiter=",", skip_header=1)
        x, labels = data[:, :20], data[:, 20].astype(bool)
        old, new = model.logit(original, x) > 0, model.logit(edited, x) > 0
        mask = suppressed(x)
        assert np.array_equal(old[~mask], new[~mask])
        introduced = (~mask) & (old == labels) & (new != labels)
        assert not introduced.any()
        print(f"Step {step}: preserved all decisions outside suppression; "
              f"{np.count_nonzero(old != new)} decisions overridden; "
              f"{np.count_nonzero(new != labels)} historical-label differences")
