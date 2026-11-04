"""Construct a hand-designed ReLU override. No weights are fitted."""
from pathlib import Path

import numpy as np

from model import load, logit, save


def inferred_rule(X):
    i, u, n, c = X[:, 0], X[:, 1], X[:, 2], X[:, 4]
    return ((c < 0.40)
            & (np.maximum.reduce([i, u, n]) >= 0.65)
            & ((i + u > 1.05) | (i + n > 1.30) | (u + n > 1.30)))


original = load("model_in.json")
layers = []
raw_features = [0, 1, 2, 4]

# Carry severity and confidence alongside the unchanged original network.
for k, (W, b) in enumerate(original[:-1]):
    extra_rows = 0 if k == 0 else 4
    V = np.zeros((W.shape[0] + extra_rows, W.shape[1] + 4))
    V[:W.shape[0], :W.shape[1]] = W
    if k == 0:
        for j, feature in enumerate(raw_features):
            V[feature, W.shape[1] + j] = 1
    else:
        V[W.shape[0]:, W.shape[1]:] = np.eye(4)
    layers.append((V, np.r_[b, np.zeros(4)]))

# Convert the original output to its positive and negative parts.
W, b = original[-1]
V = np.zeros((W.shape[0] + 4, 6))
V[:W.shape[0], 0] = W[:, 0]
V[:W.shape[0], 1] = -W[:, 0]
V[W.shape[0]:, 2:] = np.eye(4)
layers.append((V, np.r_[b, -b, np.zeros(4)]))
names = ["z_pos", "z_neg", "i", "u", "n", "c"]


def stage(specifications):
    """Append specified affine ReLU units; carry all existing units unchanged."""
    global names
    width = len(names)
    V = np.zeros((width, width + len(specifications)))
    V[:, :width] = np.eye(width)
    bias = np.zeros(V.shape[1])
    added = []
    for j, (name, coefficients, intercept) in enumerate(specifications):
        for source, weight in coefficients.items():
            V[names.index(source), width + j] = weight
        bias[width + j] = intercept
        added.append(name)
    layers.append((V, bias))
    names += added


# max(a,b) = b + ReLU(a-b).
stage([
    ("i_minus_u", {"i": 1, "u": -1}, 0),
    ("pair_iu", {"i": 1, "u": 1}, 0.95),
    ("pair_in", {"i": 1, "n": 1}, 0.70),
    ("pair_un", {"u": 1, "n": 1}, 0.70),
    ("confidence_margin", {"c": -1}, 2.40),
])
stage([
    ("max_iu", {"u": 1, "i_minus_u": 1}, 0),
    ("pair_iu_minus_in", {"pair_iu": 1, "pair_in": -1}, 0),
])
stage([
    ("max_iu_minus_n", {"max_iu": 1, "n": -1}, 0),
    ("max_pair_first", {"pair_in": 1, "pair_iu_minus_in": 1}, 0),
])
stage([
    # Include the answered m=0.65 boundary using a numerical-width shift.
    ("severity_margin", {"n": 1, "max_iu_minus_n": 1}, 1.35 + 1e-12),
    ("pair_first_minus_un", {"max_pair_first": 1, "pair_un": -1}, 0),
])
stage([
    ("pair_margin", {"pair_un": 1, "pair_first_minus_un": 1}, 0),
    ("confidence_minus_severity", {"confidence_margin": 1, "severity_margin": -1}, 0),
])
# min(a,b) = a - ReLU(a-b). Margins are shifted by 2 to stay nonnegative.
stage([
    ("min_first", {"confidence_margin": 1, "confidence_minus_severity": -1}, 0),
])
stage([
    ("min_first_minus_pair", {"min_first": 1, "pair_margin": -1}, 0),
])
stage([
    ("rule_margin", {"min_first": 1, "min_first_minus_pair": -1}, 0),
])
stage([
    ("z_minus_rule", {"z_pos": 1, "z_neg": -1, "rule_margin": -1}, 2),
])

# Output max(original_logit, minimum signed rule margin).
out = np.zeros((len(names), 1))
out[names.index("z_minus_rule"), 0] = 1
out[names.index("rule_margin"), 0] = 1
layers.append((out, np.array([-2.0])))
save(layers, "model_out.json")

# Verification uses forward passes only.
edited = load("model_out.json")
for filename in ["evidence.csv", "answers.csv", "evidence_step1.csv",
                 "evidence_step2.csv", "evidence_step3.csv"]:
    data = np.genfromtxt(filename, delimiter=",", skip_header=1)
    X, labels = data[:, :20], data[:, 20].astype(bool)
    expected = (logit(original, X) > 0) | inferred_rule(X)
    predicted = logit(edited, X) > 0
    assert np.array_equal(predicted, expected), filename
    if filename in ["evidence.csv", "answers.csv"]:
        assert np.array_equal(predicted, labels), filename
    print(filename, "labels matched:", int(np.sum(predicted == labels)),
          "/", len(labels), "(earlier labels can be overridden)")

rng = np.random.default_rng(404)
X = rng.random((50000, 20))
X[:, 7:10] = rng.integers(0, 2, (len(X), 3))
before = logit(original, X)
after = logit(edited, X)
rule = inferred_rule(X)
assert np.array_equal(after > 0, (before > 0) | rule)
print("Random inputs: 50000/50000 match the inferred rule and original decisions.")

# Step 1: tone cannot affect any result.
X_tone = X[:2000].copy()
X_tone[:, 3] = 1 - X_tone[:, 3]
assert np.array_equal(logit(edited, X_tone), after[:2000])

# Step 3: critical-tier alerts with error_rate > 0.70 must escalate.
critical = (X[:, 7] == 1) & (X[:, 5] > 0.70)
assert np.all(after[critical] > 0)
print("Tone invariance and critical-tier error override checks passed.")
print("Layers:", [W.shape for W, _ in edited])
