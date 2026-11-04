"""Laya scorer helper. M: [n, 5, 1024] marker vectors (one per department option)."""
import numpy as np, torch
DEPTS = ["cards", "disputes", "transfers_topups", "fees_fx", "account_security"]
def load(path):
    d = np.load(path); return {k: d[k] for k in d.files}
def save(S, path):
    np.savez(path, **S)
def gelu(x):
    return 0.5 * x * (1 + torch.erf(torch.from_numpy(np.ascontiguousarray(x)) / np.sqrt(2)).numpy())
def logits(S, M):
    mu = M.mean(-1, keepdims=True); var = M.var(-1, keepdims=True)
    h = (M - mu) / np.sqrt(var + 1e-5) * S["ln_w"] + S["ln_b"]
    z = (gelu(h @ S["W1"] + S["b1"]) @ S["W2"] + S["b2"])[..., 0]
    i, e = 0, M
    while f"extra_W{i}" in S:
        e = e @ S[f"extra_W{i}"] + S[f"extra_b{i}"]
        if f"extra_W{i + 1}" in S:
            e = np.maximum(e, 0)
        i += 1
    return z + e[..., 0] if i else z
def predict(S, M):
    return [DEPTS[i] for i in logits(S, M).argmax(-1)]
