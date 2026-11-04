"""Construct analytic ReLU arithmetic. No parameter fitting or training."""
import json
from pathlib import Path

import numpy as np
import model

DEPTH = 18
GATE_SLOPE = 1e10
prefix = []

def layer(n, m):
    return np.zeros((n, m)), np.zeros(m)

# State: original inputs (20), confidence margin (1), tent states (3),
# square approximations (3). Each square starts with q_0(z) = z.
w, b = layer(20, 27)
w[:, :20] = np.eye(20)
w[4, 20], b[20] = -1, 0.4
for j in (21, 24):
    w[1, j] = 1
for j in (22, 25):
    w[4, j], b[j] = -1, 1
for j in (23, 26):
    w[1, j], w[4, j], b[j] = 0.5, -0.5, 0.5
prefix.append((w, b))

# T(z) = 2z - 4 ReLU(z - 1/2) on [0,1].
# q_m(z) = z - sum_{k=1}^m 4^-k T^k(z) interpolates z^2
# on the dyadic grid. Its uniform error is at most 4^-m / 4.
for k in range(1, DEPTH + 1):
    w, b = layer(27, 30)
    w[:21, :21] = np.eye(21)
    for j in range(3):
        w[24+j, 21+j] = 1
        w[21+j, 24+j] = 2
        w[21+j, 27+j], b[27+j] = 2, -1
    prefix.append((w, b))
    w, b = layer(30, 27)
    w[:21, :21] = np.eye(21)
    for j in range(3):
        w[24+j, 21+j], w[27+j, 21+j] = 1, -2
        w[21+j, 24+j] = 1
        w[24+j, 24+j] = -4.0**(-k)
        w[27+j, 24+j] = 2 * 4.0**(-k)
    prefix.append((w, b))

# uv = 2((u+v)/2)^2 - (u^2+v^2)/2, u=urgency, v=1-confidence.
w, b = layer(27, 22)
w[:21, :21] = np.eye(21)
w[24:27, 21] = [-0.5, -0.5, 2]
prefix.append((w, b))

# Cap the increase at 1-impact.
w, b = layer(22, 23)
w[:22, :22] = np.eye(22)
w[0, 22], w[21, 22], b[22] = 1, 1, -1
prefix.append((w, b))
w, b = layer(23, 22)
w[:21, :21] = np.eye(21)
w[21, 21], w[22, 21] = 1, -1
prefix.append((w, b))

# min(increase, slope*ReLU(0.4-confidence)). This is exactly zero
# for confidence >= 0.4; the transition lies within 1e-10 below it.
w, b = layer(22, 23)
w[:22, :22] = np.eye(22)
w[21, 22], w[20, 22] = 1, -GATE_SLOPE
prefix.append((w, b))
w, b = layer(23, 21)
w[:20, :20] = np.eye(20)
w[21, 20], w[22, 20] = 1, -1
prefix.append((w, b))
w, b = layer(21, 20)
w[:20] = np.eye(20)
w[20, 0] = 1
prefix.append((w, b))

baseline = model.load('model_in.json')
model.save(prefix + baseline, 'model_out.json')

def forward(layers, x):
    for w, b in layers:
        x = np.maximum(x @ w + b, 0)
    return x

def reference(x):
    y = x.copy()
    low = x[:, 4] < 0.4
    y[low, 0] = np.minimum(1, x[low, 0] + x[low, 1]*(1-x[low, 4]))
    return y

if __name__ == '__main__':
    edited = model.load('model_out.json')
    report = {'square_depth': DEPTH, 'product_error_bound': 0.75*4.0**(-DEPTH),
              'confidence_transition_width': 1/GATE_SLOPE, 'checks': {}}
    for file in ('evidence.csv', 'answers.csv', 'evidence_step1.csv',
                 'evidence_step2.csv', 'evidence_step3.csv'):
        a = np.genfromtxt(file, delimiter=',', skip_header=1)
        x, labels = a[:, :20], a[:, 20].astype(bool)
        predicted = model.logit(edited, x) > 0
        expected = model.logit(baseline, reference(x)) > 0
        report['checks'][file] = {
            'rows': len(x), 'label_matches': int(np.sum(predicted == labels)),
            'rule_matches': int(np.sum(predicted == expected)),
            'labels_superseded_by_rule': int(np.sum(expected != labels))}
        assert np.array_equal(predicted, expected)
        if file in ('evidence.csv', 'answers.csv'):
            assert np.array_equal(predicted, labels)

    rng = np.random.default_rng(4004)
    count = 50000
    mismatches = 0
    max_input_error = 0
    max_logit_error = 0
    outside_error = 0
    for start in range(0, count, 1000):
        x = rng.random((min(1000, count-start), 20))
        x[:, 7:10] = rng.integers(0, 2, (len(x), 3))
        target = reference(x)
        actual = forward(prefix, x)
        max_input_error = max(max_input_error, float(np.max(np.abs(target-actual))))
        old = model.logit(baseline, x)
        expected = model.logit(baseline, target)
        got = model.logit(edited, x)
        max_logit_error = max(max_logit_error, float(np.max(np.abs(expected-got))))
        outside = x[:, 4] >= 0.4
        outside_error = max(outside_error, float(np.max(np.abs(old[outside]-got[outside]))))
        mismatches += int(np.sum((expected > 0) != (got > 0)))
    report['random_check'] = dict(rows=count, label_mismatches=mismatches,
        max_input_error=max_input_error, max_logit_error=max_logit_error,
        outside_region_max_logit_error=outside_error)
    assert mismatches == 0
    assert outside_error == 0
    # Check switch endpoints and saturation without adapting any weights.
    x = np.full((7, 20), 0.5)
    x[:, 7:10] = 0
    x[:, 4] = [0, 0.399, 0.4-1e-9, 0.4, 0.4+1e-9, 0.401, 1]
    assert np.max(np.abs(forward(prefix, x)-reference(x))) < 2e-11
    x[:, 0] = 1
    assert np.max(np.abs(forward(prefix, x)-reference(x))) < 2e-11
    assert all(np.array_equal(a, c) and np.array_equal(b, d)
               for (a,b),(c,d) in zip(baseline, edited[-len(baseline):]))
    report['baseline_weights_unchanged'] = True
    Path('verification.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))
