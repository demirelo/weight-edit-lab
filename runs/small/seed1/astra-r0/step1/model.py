import json, numpy as np
FEATURES = ["impact", "urgency", "users_affected", "tone_anger", "startup_phase", "confidence"]
def load(path):
    d = json.load(open(path))
    return [(np.array(L["W"], float), np.array(L["b"], float)) for L in d["layers"]]
def logit(layers, X):
    h = np.asarray(X, float)
    for i, (W, b) in enumerate(layers):
        h = h @ W + b
        if i < len(layers) - 1:
            h = np.maximum(h, 0)
    return h[:, 0]
def save(layers, path):
    json.dump({"features": FEATURES, "layers": [{"W": np.asarray(W).tolist(), "b": np.asarray(b).tolist()} for W, b in layers]}, open(path, "w"))
