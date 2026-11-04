"""Synthetic testbed for sequential weight-space corrections.

Task: decide whether an ops alert should be escalated (1) or not (0).
The base net is trained on a *defective* rule. Three corrections, applied in
order, move the target toward the true rule. Each correction changes labels
only inside its own region, so we can measure fix rate, retention of earlier
fixes, and collateral drift separately.

This file holds the ground truth. It must never be copied into an editor's
workspace.
"""
import json
import numpy as np

FEATURES = ["impact", "urgency", "users_affected", "tone_anger", "startup_phase", "confidence"]
# startup_phase is binary {0,1}; all others are uniform in [0,1].

CORRECTIONS = [
    "Tone must not drive escalation. Right now angry-sounding alerts with low "
    "impact get escalated. An alert's tone_anger should have no effect: decide "
    "on impact and urgency as usual.",
    "During the startup phase (startup_phase = 1), alerts with impact below 0.6 "
    "are expected startup noise and must NOT be escalated, however urgent they "
    "look. Outside startup, and for startup alerts with impact >= 0.6, keep the "
    "current behaviour.",
    "Any alert with users_affected above 0.85 must ALWAYS be escalated. This "
    "overrides every other consideration, including startup noise and low impact.",
]


def base_score(X):
    return 0.6 * X[:, 0] + 0.4 * X[:, 1] > 0.5


def target(X, k):
    """Target labels after the first k corrections (k=0 is the defective rule)."""
    y = base_score(X)
    if k < 1:
        y = y | ((X[:, 3] > 0.8) & (X[:, 0] < 0.4))
    if k >= 2:
        y = y & ~((X[:, 4] == 1) & (X[:, 0] < 0.6))
    if k >= 3:
        y = y | (X[:, 2] > 0.85)
    return y.astype(int)


def sample(n, rng):
    X = rng.random((n, 6))
    X[:, 4] = (rng.random(n) < 0.3).astype(float)
    return X


# ---------- MLP with arbitrary layer shapes, ReLU hidden, logit output ----------

def init(sizes, rng):
    return [{"W": rng.normal(0, np.sqrt(2 / a), (a, b)), "b": np.zeros(b)}
            for a, b in zip(sizes[:-1], sizes[1:])]


def forward(layers, X):
    h = X
    for i, L in enumerate(layers):
        h = h @ L["W"] + L["b"]
        if i < len(layers) - 1:
            h = np.maximum(h, 0)
    return h[:, 0]


def predict(layers, X):
    return (forward(layers, X) > 0).astype(int)


def save(layers, path, features=FEATURES):
    with open(path, "w") as f:
        json.dump({"features": features,
                   "activation": "relu hidden layers, linear output logit; escalate iff logit > 0",
                   "layers": [{"W": L["W"].tolist(), "b": L["b"].tolist()} for L in layers]}, f)


def load(path):
    with open(path) as f:
        d = json.load(f)
    layers = [{"W": np.array(L["W"], float), "b": np.array(L["b"], float)} for L in d["layers"]]
    assert layers[0]["W"].shape[0] == len(d["features"]) and layers[-1]["W"].shape[1] == 1
    for a, b in zip(layers[:-1], layers[1:]):
        assert a["W"].shape[1] == b["W"].shape[0] == a["b"].shape[0]
    return layers


def count_nonzero(layers):
    return int(sum((np.abs(L["W"]) > 0).sum() + (np.abs(L["b"]) > 0).sum() for L in layers))


def train(layers, X, y, steps, lr, rng, batch=256, soft=None):
    """Adam on binary cross-entropy. `soft` lets replay use soft targets."""
    t = y.astype(float) if soft is None else soft
    m = [{k: np.zeros_like(v) for k, v in L.items()} for L in layers]
    v = [{k: np.zeros_like(x) for k, x in L.items()} for L in layers]
    b1, b2, eps = 0.9, 0.999, 1e-8
    for step in range(1, steps + 1):
        idx = rng.choice(len(X), min(batch, len(X)), replace=False)
        xb, tb = X[idx], t[idx]
        acts = [xb]
        h = xb
        for i, L in enumerate(layers):
            h = h @ L["W"] + L["b"]
            if i < len(layers) - 1:
                h = np.maximum(h, 0)
            acts.append(h)
        p = 1 / (1 + np.exp(-acts[-1][:, 0]))
        g = ((p - tb) / len(xb))[:, None]
        for i in range(len(layers) - 1, -1, -1):
            gW, gb = acts[i].T @ g, g.sum(0)
            if i > 0:
                g = (g @ layers[i]["W"].T) * (acts[i] > 0)
            for k, gr in (("W", gW), ("b", gb)):
                m[i][k] = b1 * m[i][k] + (1 - b1) * gr
                v[i][k] = b2 * v[i][k] + (1 - b2) * gr ** 2
                mh, vh = m[i][k] / (1 - b1 ** step), v[i][k] / (1 - b2 ** step)
                layers[i][k] -= lr * mh / (np.sqrt(vh) + eps)
    return layers


# ---------- correction evidence and evaluation ----------

def correction_examples(k, rng, n_in=12, n_out=12):
    """Labelled evidence for correction k (1-based): cases whose label changes,
    plus near-miss cases whose label stays the same."""
    pool = sample(200000, rng)
    changed = target(pool, k) != target(pool, k - 1)
    near = {1: (pool[:, 3] > 0.6) | (pool[:, 0] < 0.5),
            2: (pool[:, 4] == 1) | ((pool[:, 0] > 0.5) & (pool[:, 0] < 0.7)),
            3: (pool[:, 2] > 0.7)}[k] & ~changed
    Xi = pool[np.flatnonzero(changed)[:n_in]]
    Xo = pool[np.flatnonzero(near)[:n_out]]
    X = np.vstack([Xi, Xo])
    return X, target(X, k)


def evaluate(layers, base_layers, X, k):
    """Metrics after k corrections on a hidden test set X."""
    pred = predict(layers, X)
    out = {"acc_all": float((pred == target(X, k)).mean())}
    if k >= 1:
        reg = target(X, k) != target(X, k - 1)
        out["fix_latest"] = float((pred[reg] == target(X, k)[reg]).mean())
    if k >= 2:
        reg = np.zeros(len(X), bool)
        for j in range(1, k):
            reg |= target(X, j) != target(X, j - 1)
        reg &= ~(target(X, k) != target(X, k - 1))
        out["retain_earlier"] = float((pred[reg] == target(X, k)[reg]).mean())
    agree = np.all([target(X, j) == target(X, 0) for j in range(1, 4)], axis=0)
    out["drift_untouched"] = float((pred[agree] != predict(base_layers, X[agree])).mean())
    out["nonzero_params"] = count_nonzero(layers)
    return out
