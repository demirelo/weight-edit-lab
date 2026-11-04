"""Gradient baselines for the Laya pilot: fine-tune the scorer on cached marker vectors.

Same evidence as the editors (32 messages per correction), sequential, with replay of
the current scorer's own soft answers on 2,048 random training messages. The best grid
point is picked by hidden-test accuracy (an oracle choice that favours the baseline).
Label curve: all training messages of the corrected intents, subsampled.

  python laya_baselines.py <seed>...
"""
import json
import os
import sys
import numpy as np
import torch
import laya_lab as L
import laya_harness as H

HERE = os.path.dirname(os.path.abspath(__file__))


def to_torch(S):
    import torch.nn as nn
    sc = nn.Sequential(nn.LayerNorm(1024), nn.Linear(1024, 1024), nn.GELU(), nn.Linear(1024, 1))
    with torch.no_grad():
        sc[0].weight.copy_(torch.tensor(S["ln_w"])); sc[0].bias.copy_(torch.tensor(S["ln_b"]))
        sc[1].weight.copy_(torch.tensor(S["W1"].T)); sc[1].bias.copy_(torch.tensor(S["b1"]))
        sc[3].weight.copy_(torch.tensor(S["W2"].T)); sc[3].bias.copy_(torch.tensor(S["b2"]))
    return sc


def from_torch(sc):
    g = lambda t: t.detach().numpy().copy()
    return {"ln_w": g(sc[0].weight), "ln_b": g(sc[0].bias), "W1": g(sc[1].weight).T, "b1": g(sc[1].bias),
            "W2": g(sc[3].weight).T, "b2": g(sc[3].bias)}


def labelled(k, seed, n):
    """n training messages for correction k: half from its intents, half near misses."""
    if n is None:
        _, y, M = H.evidence(k, seed)
        return M, y
    _, y, M = H.evidence(k, seed, n_in=n // 2, n_out=n // 2)
    return M, y


def chain(seed, lr, steps, ratio, n=None, run_seed=0):
    torch.manual_seed(run_seed)
    rng = np.random.default_rng(run_seed)
    Tr, T = H.data("train"), H.data("test")
    base_S = L.load_scorer(os.path.join(HERE, "cache/scorer_base.npz"))
    base_pred = L.predict(base_S, T["M"])
    sc = to_torch(base_S)
    rows, seenM, seeny = [], [], []
    for k in range(1, len(H.CORR) + 1):
        M, y = labelled(k, seed, n)
        seenM.append(M); seeny.append(y)
        Me, ye = np.concatenate(seenM), np.concatenate(seeny)
        Mr = Tr["M"][rng.choice(len(Tr["M"]), 2048, replace=False)]
        with torch.no_grad():
            pr = torch.softmax(sc(torch.tensor(Mr)).squeeze(-1), -1)
        Xe, Ye = torch.tensor(Me), torch.nn.functional.one_hot(torch.tensor(ye), 5).float()
        Xr = torch.tensor(Mr)
        opt = torch.optim.Adam(sc.parameters(), lr=lr)
        for _ in range(steps):
            ie = torch.randint(len(Xe), (32,))
            ir = torch.randint(len(Xr), (32,))
            le = -(Ye[ie] * torch.log_softmax(sc(Xe[ie]).squeeze(-1), -1)).sum(-1).mean()
            lr_ = -(pr[ir] * torch.log_softmax(sc(Xr[ir]).squeeze(-1), -1)).sum(-1).mean()
            loss = ratio * le + (1 - ratio) * lr_
            opt.zero_grad(); loss.backward(); opt.step()
        pred = L.predict(from_torch(sc), T["M"])
        rows.append({"step": k, **H.evaluate(pred, base_pred, T, k)})
    return rows


if __name__ == "__main__":
    torch.set_num_threads(4)
    for seed in [int(s) for s in sys.argv[1:]]:
        out = {"grid": [], "label_curve": []}
        for lr in (3e-4, 1e-3, 3e-3, 1e-2):
            for steps in (300, 1000, 3000, 10000):
                for ratio in (0.5, 0.8):
                    rows = chain(seed, lr, steps, ratio)
                    out["grid"].append({"lr": lr, "steps": steps, "ratio": ratio, "rows": rows})
                    print(seed, "grid", lr, steps, ratio, round(rows[-1]["acc_all"], 4), flush=True)
        for n in (32, 64, 128, 256):
            cands = [chain(seed, lr, st, ra, n=n) for lr in (1e-3, 3e-3) for st in (1000, 3000) for ra in (0.5, 0.8)]
            rows = max(cands, key=lambda r: r[-1]["acc_all"])
            out["label_curve"].append({"n_labels": n, "rows": rows})
            print(seed, "labels", n, round(rows[-1]["acc_all"], 4), flush=True)
        os.makedirs(os.path.join(HERE, "runs", f"seed{seed}"), exist_ok=True)
        json.dump(out, open(os.path.join(HERE, "runs", f"seed{seed}", "baselines.json"), "w"), indent=1)
