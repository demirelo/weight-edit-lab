"""Gradient baselines given the same evidence the LLM editor sees.

replay:    fine-tune on the 24 correction examples plus 2048 random inputs
           soft-labelled by the current model (no ground truth leaks in).
no_replay: fine-tune on the 24 correction examples only.
"""
import json
import numpy as np
import lab


def read_evidence(k):
    d = np.genfromtxt(f"evidence/correction_{k}.csv", delimiter=",", skip_header=1)
    return d[:, :6], d[:, 6].astype(int)


def run(mode, seed, Xt, base):
    rng = np.random.default_rng(seed)
    layers = [{k: v.copy() for k, v in L.items()} for L in base]
    rows = []
    for k in (1, 2, 3):
        Xe, ye = read_evidence(k)
        if mode == "replay":
            Xr = lab.sample(2048, rng)
            soft_r = 1 / (1 + np.exp(-lab.forward(layers, Xr)))
            # Upweight the evidence by repeating it so it is not drowned out.
            Xtr = np.vstack([Xr] + [Xe] * 40)
            soft = np.concatenate([soft_r] + [ye.astype(float)] * 40)
        else:
            Xtr, soft = Xe, ye.astype(float)
        lab.train(layers, Xtr, None, steps=600, lr=3e-3, rng=rng, batch=128, soft=soft)
        rows.append({"step": k, **lab.evaluate(layers, base, Xt, k)})
    return rows


if __name__ == "__main__":
    Xt = np.load("hidden/test.npy")
    base = lab.load("runs/base/model.json")
    out = {"unedited": [{"step": k, **lab.evaluate(base, base, Xt, k)} for k in (1, 2, 3)]}
    for mode in ("replay", "no_replay"):
        out[mode] = [run(mode, s, Xt, base) for s in range(5)]
    with open("runs/baselines.json", "w") as f:
        json.dump(out, f, indent=1)
    for mode in ("replay", "no_replay"):
        for k in range(3):
            m = {key: np.mean([r[k][key] for r in out[mode]]) for key in out[mode][0][k] if key != "step"}
            print(mode, k + 1, {a: round(b, 3) for a, b in m.items()})
