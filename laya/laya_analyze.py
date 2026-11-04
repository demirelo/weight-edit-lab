"""Summarize the Laya pilot: final step per arm, plus gradient baselines.

  python laya_analyze.py   -> prints a table and writes results/summary.json
"""
import glob
import json
import os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
KEYS = ("acc_all", "fix_all", "fix_latest", "retain_earlier", "drift_other", "acc_other")


def mean(xs):
    return round(float(np.mean(xs)), 4)


import sys
sys.path.insert(0, HERE)
import laya_harness as H  # noqa: E402
_T = H.data("test")
_ALL = np.isin(_T["intents"], sum([c["intents"] for c in H.CORR], []))


def fix_all(pred):
    """Share of all test messages covered by any correction that are routed correctly."""
    return float((pred[_ALL] == _T["y"][_ALL]).mean())


out = {"arms": {}, "per_chain": [], "baselines": {}}
for f in sorted(glob.glob(f"{HERE}/runs/seed*/*-r*/results.json")):
    rows = json.load(open(f))
    last = rows[-1]
    arm = f"{last['llm']}-{last['mode']}"
    last = dict(last, fix_all=fix_all(np.load(os.path.join(os.path.dirname(f), f"step{last['step']}", "test_pred.npy"))))
    out["per_chain"].append({"arm": arm, "seed": last["seed"], "effort": rows[0].get("effort", "high" if last["llm"] in ("astra", "sol") else "medium"),
                             **{k: last.get(k) for k in KEYS},
                             "minutes": round(sum(r["seconds"] for r in rows) / 60, 1),
                             "leaks": sorted({w for r in rows for w in r["leaks"]})})
for c in out["per_chain"]:
    out["arms"].setdefault(c["arm"], []).append(c)
summary = {arm: {**{k: mean([c[k] for c in cs]) for k in KEYS}, "n": len(cs),
                 "acc_range": [min(c["acc_all"] for c in cs), max(c["acc_all"] for c in cs)],
                 "minutes": mean([c["minutes"] for c in cs])} for arm, cs in out["arms"].items()}
out["arms"] = summary

bl = [json.load(open(f)) for f in sorted(glob.glob(f"{HERE}/runs/seed*/baselines.json"))]
if bl:
    best = [max(b["grid"], key=lambda g: g["rows"][-1]["acc_all"]) for b in bl]
    out["baselines"]["finetune_32_best"] = {k: mean([g["rows"][-1].get(k, np.nan) for g in best]) for k in KEYS if k != "fix_all"}
    out["baselines"]["finetune_32_best_configs"] = [{k: g[k] for k in ("lr", "steps", "ratio")} for g in best]
    # Guard: a best setting at the edge of the grid means the grid is too small.
    for b, g in zip(bl, best):
        for key in ("lr", "steps"):
            vals = sorted({x[key] for x in b["grid"]})
            if g[key] in (vals[0], vals[-1]):
                print(f"GRID EDGE WARNING: best {key}={g[key]} is at the grid edge {vals}")
    curve = {}
    for b in bl:
        for c in b["label_curve"]:
            curve.setdefault(c["n_labels"], []).append(c["rows"][-1])
    out["baselines"]["label_curve"] = {n: {k: mean([r[k] for r in rs]) for k in ("acc_all", "fix_latest", "drift_other")}
                                       for n, rs in sorted(curve.items())}

os.makedirs(f"{HERE}/results", exist_ok=True)
json.dump(out, open(f"{HERE}/results/summary.json", "w"), indent=1)
print("unedited base: acc_all 0.7029 (laya_lab.py base)")
for arm, s in sorted(summary.items()):
    print(f"{arm:16s} n={s['n']} acc {s['acc_all']} range {s['acc_range']} | fix_all {s['fix_all']} | fix3 {s['fix_latest']} retain {s['retain_earlier']}"
          f" | drift {s['drift_other']} acc_other {s['acc_other']} | {s['minutes']} min/chain")
for c in out["per_chain"]:
    if c["leaks"]:
        print("LEAKS", c)
for k, v in out["baselines"].items():
    print(k, v)
