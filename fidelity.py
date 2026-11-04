"""Edit fidelity: agreement of each final edited net with the ideal edit of its own
base net (Large/XL only). Separates editor error from the base net's own error."""
import glob
import json
import os
import numpy as np
import lab
from tasks import TASKS

out = {}
for t in ("large", "xl"):
    T = TASKS[t]
    K = len(T.corrections)
    for f in sorted(glob.glob(f"runs/{t}/seed*/*-r*/step{K}/model_out.json")):
        sd = f.split("/")[2]
        base = lab.load(f"runs/{t}/{sd}/base.json")
        X = np.load(f"runs/{t}/{sd}/test.npy")
        ideal = T.oracle(lambda Z: lab.predict(base, Z), X, K)
        ideal_acc = float((ideal == T.target(X, K)).mean())
        fid = float((lab.predict(lab.load(f), X) == ideal).mean())
        key = f.split("/")[3].split("-r")[0]
        out.setdefault(t, {}).setdefault(key, []).append({"seed": sd, "fidelity": fid, "ideal_acc": ideal_acc})
for t, d in out.items():
    for k, v in d.items():
        fs = [x["fidelity"] for x in v]
        print(t, k, "n", len(v), "fidelity mean", round(np.mean(fs), 5), "min", round(min(fs), 5),
              "| ideal-edit acc", round(np.mean([x["ideal_acc"] for x in v]), 4))
json.dump(out, open("results/fidelity.json", "w"), indent=1)
