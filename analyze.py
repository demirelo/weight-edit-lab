"""Aggregate edit chains and baselines into results/summary.json and a text table.

A chain "succeeds" if, at every step, the latest fix is >= 95% right, earlier
fixes are >= 95% kept, and untouched cases keep >= 95% accuracy.
"""
import glob
import json
import os
import re
import numpy as np
from tasks import TASKS
from harness import LEAK_RE

ROOT = os.path.abspath(os.path.dirname(__file__))
OK = 0.95


def tokens(log):
    t = re.findall(r"tokens used\s*\n?\s*([\d,'’]+)", open(log, errors="replace").read())
    return int(re.sub(r"\D", "", t[-1])) if t else 0


def step_ok(r):
    return (r["fix_latest"] >= OK and r.get("retain_earlier", 1) >= OK
            and r["acc_untouched"] >= OK and r["valid"])


def chains(task):
    out = []
    for f in sorted(glob.glob(f"{ROOT}/runs/{task}/seed*/*-r*/results.json")):
        rows = json.load(open(f))
        d = os.path.dirname(f)
        tok = sum(tokens(p) for p in glob.glob(f"{d}/step*/codex.log"))
        leaks = sorted({m.group(0) for p in glob.glob(f"{d}/step*/codex.log")
                        for m in re.finditer(LEAK_RE, open(p, errors="replace").read())})
        mode = rows[0].get("mode", "text")
        out.append({"llm": rows[0]["llm"] + ("" if mode == "text" else f"-{mode}"), "seed": rows[0]["seed"], "rep": rows[0]["rep"],
                    "final": rows[-1], "steps_ok": [step_ok(r) for r in rows],
                    "success": all(step_ok(r) for r in rows), "tokens": tok, "leaks": leaks,
                    "minutes": round(sum(r["seconds"] for r in rows) / 60, 1)})
    return out


def stat(xs):
    xs = np.array(xs, float)
    return {"mean": round(float(xs.mean()), 4), "min": round(float(xs.min()), 4),
            "max": round(float(xs.max()), 4), "n": int(len(xs))}


def summarize(task):
    T = TASKS[task]
    res = {"task": task, "params_base": None, "llm": {}, "baselines": {}}
    cs = chains(task)
    for llm in sorted({c["llm"] for c in cs}):
        sel = [c for c in cs if c["llm"] == llm]
        res["llm"][llm] = {
            "chains": len(sel), "success": sum(c["success"] for c in sel),
            **{m: stat([c["final"][m] for c in sel]) for m in
               ("acc_all", "fix_latest", "retain_earlier", "acc_untouched", "drift_untouched", "nonzero_params")},
            "tokens_per_chain": stat([c["tokens"] for c in sel]),
            "minutes_per_chain": stat([c["minutes"] for c in sel]),
            "failed_steps": [(c["seed"], c["rep"], i + 1) for c in sel for i, ok in enumerate(c["steps_ok"]) if not ok],
            "leaks": sorted({w for c in sel for w in c["leaks"]}),
        }
    bl = [json.load(open(f)) for f in sorted(glob.glob(f"{ROOT}/runs/{task}/seed*/baselines.json"))]
    if bl:
        fin = lambda rows: rows[-1]
        res["baselines"]["unedited"] = {m: stat([fin(b["unedited"])[m] for b in bl]) for m in ("acc_all", "acc_untouched")}
        for name, rep in (("finetune_replay_best", True), ("finetune_noreplay_best", False)):
            picks = [max((g for g in b["grid"] if g["replay"] == rep), key=lambda g: g["rows"][-1]["acc_all"]) for b in bl]
            res["baselines"][name + "_configs"] = [{k: v for k, v in p.items() if k != "rows"} for p in picks]
            res["baselines"][name] = {m: stat([p["rows"][-1].get(m, np.nan) for p in picks])
                                      for m in ("acc_all", "fix_latest", "retain_earlier", "acc_untouched")}
        curve = {}
        for b in bl:
            for c in b["label_curve"]:
                curve.setdefault(c["n_labels"], []).append(c["rows"][-1]["acc_all"])
        res["baselines"]["label_curve_acc_all"] = {n: stat(v) for n, v in sorted(curve.items())}
        # Guard: more labels must not hurt a tuned baseline. A drop means the baseline is broken.
        means = [stat(v)["mean"] for _, v in sorted(curve.items())]
        if any(b < a - 0.02 for a, b in zip(means, means[1:])):
            print(f"BASELINE WARNING {task}: label curve drops with more labels: {means}")
        sc = {}
        for b in bl:
            for c in b.get("scratch_curve", []):
                sc.setdefault(c["n_labels"], []).append(c["acc_all"])
        res["baselines"]["scratch_curve_acc_all"] = {n: stat(v) for n, v in sorted(sc.items())}
    return res


if __name__ == "__main__":
    os.makedirs(f"{ROOT}/results", exist_ok=True)
    allres = {t: summarize(t) for t in TASKS if glob.glob(f"{ROOT}/runs/{t}/seed*")}
    json.dump(allres, open(f"{ROOT}/results/summary.json", "w"), indent=1)
    for t, r in allres.items():
        print(f"== {t}")
        for llm, s in r["llm"].items():
            print(f"  {llm}: {s['success']}/{s['chains']} chains succeed | acc {s['acc_all']} | "
                  f"fix {s['fix_latest']['mean']} retain {s['retain_earlier']['mean']} | "
                  f"untouched {s['acc_untouched']['mean']} | params {s['nonzero_params']} | "
                  f"tokens {s['tokens_per_chain']['mean']} | min {s['minutes_per_chain']['mean']} | "
                  f"failed steps {s['failed_steps']} | leaks {s['leaks']}")
        for name, s in r["baselines"].items():
            if name.endswith("_configs"):
                print(f"  {name}: {s}")
            elif "curve" in name:
                print(f"  {name}: " + ", ".join(f"{n}: {v['mean']}" for n, v in s.items()))
            else:
                print(f"  {name}: " + ", ".join(f"{m} {v['mean']}" for m, v in s.items()))
