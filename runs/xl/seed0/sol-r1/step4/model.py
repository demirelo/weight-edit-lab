import json, numpy as np
FEATURES = ["impact", "urgency", "users_affected", "tone_anger", "confidence", "error_rate", "latency_spike", "tier_critical", "region_eu", "maintenance_window", "retry_count", "service_age", "on_call_load", "dup_alerts", "sensor_drift", "aux_1", "aux_2", "aux_3", "aux_4", "aux_5", "aux_6", "aux_7", "aux_8", "aux_9", "aux_10", "aux_11", "aux_12", "aux_13", "aux_14", "aux_15", "aux_16", "aux_17", "aux_18", "aux_19", "aux_20", "aux_21", "aux_22", "aux_23", "aux_24", "aux_25"]
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
