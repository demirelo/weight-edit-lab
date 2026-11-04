"""Generic harness: base nets, LLM edit chains, gradient baselines.

  python harness.py base      <task> <seed>...
  python harness.py edits     <task> <seeds,> <reps> <llm,llm> [workers]
  python harness.py baselines <task> <seed>...

Edit chains are resumable: a finished step is not re-run.
Editor workspaces live under $WSROOT, outside this folder.
"""
import glob
import json
import os
import re
import shutil
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
import numpy as np
import lab
from tasks import TASKS

ROOT = os.path.abspath(os.path.dirname(__file__))
PY = os.path.join(ROOT, ".venv/bin/python")
LLMS = {"astra": "gpt-6-astra", "sol": "gpt-6.1-sol"}


def sdir(T, seed):
    return os.path.join(ROOT, "runs", T.name, f"seed{seed}")


# ---------------- base ----------------

def make_base(T, seed):
    d = sdir(T, seed)
    os.makedirs(d, exist_ok=True)
    rng = np.random.default_rng(seed)
    X = T.sample(T.train["n"], rng)
    layers = lab.init(T.sizes, rng)
    lab.train(layers, X, T.target(X, 0), steps=T.train["steps"], lr=T.train["lr"], rng=rng)
    lab.save(layers, os.path.join(d, "base.json"), T.features)
    np.save(os.path.join(d, "test.npy"), T.sample(50000, np.random.default_rng(10_000 + seed)))
    erng = np.random.default_rng(20_000 + seed)
    for k in range(1, len(T.corrections) + 1):
        Xe, ye = evidence(T, k, erng)
        np.save(os.path.join(d, f"evidence_{k}.npy"), np.column_stack([Xe, ye]))
    Xt = np.load(os.path.join(d, "test.npy"))
    K = len(T.corrections)
    print(T.name, seed, "params", lab.count_nonzero(layers),
          "acc vs defective", round(float((lab.predict(layers, Xt) == T.target(Xt, 0)).mean()), 4),
          "acc vs final", round(float((lab.predict(layers, Xt) == T.target(Xt, K)).mean()), 4),
          "pos rate", round(float(T.target(Xt, 0).mean()), 3), flush=True)


def evidence(T, k, rng, n=None):
    n_in, n_out = n or T.n_evidence
    pool = T.sample(400000, rng)
    changed = T.target(pool, k) != T.target(pool, k - 1)
    near = T.related(pool, k) & ~changed
    X = np.vstack([pool[np.flatnonzero(changed)[:n_in]], pool[np.flatnonzero(near)[:n_out]]])
    return X, T.target(X, k)


def evaluate(T, layers, base, X, k):
    pred = lab.predict(layers, X)
    y = T.target(X, k)
    out = {"acc_all": float((pred == y).mean())}
    ch = T.target(X, k) != T.target(X, k - 1)
    out["fix_latest"] = float((pred[ch] == y[ch]).mean())
    if k >= 2:
        reg = np.zeros(len(X), bool)
        for j in range(1, k):
            reg |= T.target(X, j) != T.target(X, j - 1)
        reg &= ~ch
        out["retain_earlier"] = float((pred[reg] == y[reg]).mean())
    K = len(T.corrections)
    agree = np.all([T.target(X, j) == T.target(X, 0) for j in range(1, K + 1)], axis=0)
    out["drift_untouched"] = float((pred[agree] != lab.predict(base, X[agree])).mean())
    out["acc_untouched"] = float((pred[agree] == y[agree]).mean())
    out["nonzero_params"] = lab.count_nonzero(layers)
    return out


# ---------------- LLM edit chains ----------------

HELPER = '''import json, numpy as np
FEATURES = {features}
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
    json.dump({{"features": FEATURES, "layers": [{{"W": np.asarray(W).tolist(), "b": np.asarray(b).tolist()}} for W, b in layers]}}, open(path, "w"))
'''

TASK = """# Weight-editing task (step {k} of {K})

You are editing a neural network BY HAND. Do not train it.

## The model
`model_in.json` is a ReLU MLP with {nin} inputs. Feature order:
{order}

{doc}

It decides whether an operations alert is escalated: escalate iff output logit > 0.
`model.py` has `load`, `logit`, `save`. Use this Python, which has numpy: `{py}`

## Corrections already applied in earlier steps (must stay true)
{history}

## New correction for this step
{correction}

`evidence.csv` has {n} labelled examples for this correction: cases whose label
changes, plus near-miss cases whose label must stay the same.

## What to do
Write `model_out.json` (same format as `model_in.json`) so that the model:
1. follows the new correction everywhere it applies, not only on the examples;
2. still follows every earlier correction;
3. otherwise behaves exactly as `model_in.json` does.

A hidden test set of 50,000 random inputs scores all three.

## Rules
- Allowed: read the weights, run forward passes on any inputs you construct,
  reason about what units compute, change any weights or biases, add or remove
  hidden units, add layers. Hidden activations must be ReLU; the output is one
  linear logit.
- Not allowed: gradient descent, optimizers, any training or fitting loop,
  least squares or any solver fitted to data. Every weight you write must come
  from your own reasoning. Checking your edit with forward passes is fine.
- Write `NOTES.md`: what you changed and why, in under 200 words.
"""

LEAK_RE = r"weight-edit-lab/(tasks|lab|harness|analyze)\.py|test\.npy|evidence_\d|weight-edit-lab/runs"


HIDDEN = ("(Not stated in words. Infer the intended behaviour change from evidence.csv "
          "and state your inferred rule in NOTES.md.)")


def tag(llm, rep, mode):
    return f"{llm}-r{rep}" if mode == "text" else f"{llm}-{mode}-r{rep}"


def corr_text(T, j, mode):
    return T.corrections[j - 1] if mode == "text" else HIDDEN


QUERY = """# Phase 1 of 2: ask before you edit

The examples may fit more than one rule. Do NOT edit the model in this phase.
1. Write `CANDIDATES.md`: 2-4 distinct candidate rules for this step's behaviour
   change, each consistent with every labelled example you have.
2. Write `query.csv`: at most {q} input row(s), header = the feature names in the
   same order as `evidence.csv`, no label column. Choose the inputs whose correct
   labels best tell your candidates apart. Binary features must be 0 or 1; all
   other features must be in [0, 1].
You will then receive the correct labels in `answers.csv` and do the edit.
"""
WIDE = """
## Cover several kinds of rule
Your candidates must come from at least 3 of these kinds (one candidate per kind
at least), not variations of one kind:
- Output shift: add a constant or a region-dependent bonus to the current logit.
- Region override: force escalate or suppress inside a box of raw feature values.
- Input re-interpretation: the current model applied to modified inputs (one
  feature scaled, shifted or zeroed), possibly only when a condition holds.
- Interaction: one feature's effect on the decision depends on another feature.
Say which kind each candidate is. {query_line}
"""
PHASE_A = "Read TASK.md for context, then do only what QUERY.md asks. Do not write model_out.json."
PHASE_B = ("Phase 2 of 2: answers.csv holds the correct labels for your queried inputs. "
           "Use CANDIDATES.md and answers.csv, then complete TASK.md exactly as written.")


def call_codex(llm, ws, prompt, logname, q=None, T=None):
    with open(os.path.join(ws, logname), "w") as log:
        if llm == "noop":  # smoke test: no editor
            if q is not None:
                X = T.sample(q, np.random.default_rng(0))
                np.savetxt(os.path.join(ws, "query.csv"), X, delimiter=",", header=",".join(T.features), comments="")
            else:
                shutil.copy(os.path.join(ws, "model_in.json"), os.path.join(ws, "model_out.json"))
            return "ok"
        try:
            subprocess.run(["codex", "exec", "-m", LLMS[llm], "-c", "model_reasoning_effort=high",
                            "--sandbox", "workspace-write", "--skip-git-repo-check", "-C", ws, prompt],
                           stdin=subprocess.DEVNULL, stdout=log, stderr=subprocess.STDOUT, timeout=3600)
            return "ok"
        except subprocess.TimeoutExpired:
            return "timeout"


def answer_queries(T, k, ws, q):
    """Label at most q queried inputs with the current target; clip to the valid domain."""
    X = np.zeros((0, len(T.features)))
    try:
        d = np.genfromtxt(os.path.join(ws, "query.csv"), delimiter=",", skip_header=1, ndmin=2)
        d = d[~np.isnan(d).any(axis=1)] if d.size else d
        if d.size and d.shape[1] == len(T.features):
            X = np.clip(d[:q], 0, 1)
            for f in getattr(T, "BIN", {}):
                X[:, T.features.index(f)] = np.round(X[:, T.features.index(f)])
    except Exception:  # missing or malformed query file: no answers
        pass
    y = T.target(X, k) if len(X) else np.zeros(0, int)
    np.save(os.path.join(ws, "answers.npy"), X)
    with open(os.path.join(ws, "answers.csv"), "w") as f:
        f.write(",".join(T.features) + ",escalate\n")
        for x, l in zip(X, y):
            f.write(",".join(f"{v:.17g}" for v in x) + f",{int(l)}\n")
    return len(X)


def run_step(T, seed, llm, rep, k, model_in, mode="text"):
    K = len(T.corrections)
    keep = os.path.join(sdir(T, seed), tag(llm, rep, mode), f"step{k}")
    if os.path.exists(os.path.join(keep, "done.json")):
        return json.load(open(os.path.join(keep, "done.json")))
    ws = os.path.join(os.environ["WSROOT"], T.name, f"s{seed}", tag(llm, rep, mode), f"step{k}")
    shutil.rmtree(ws, ignore_errors=True)
    os.makedirs(ws)
    shutil.copy(model_in, os.path.join(ws, "model_in.json"))
    ev = np.load(os.path.join(sdir(T, seed), f"evidence_{k}.npy"))
    with open(os.path.join(ws, "evidence.csv"), "w") as f:
        f.write(",".join(T.features) + ",escalate\n")
        for row in ev:
            f.write(",".join(f"{v:.17g}" for v in row[:-1]) + f",{int(row[-1])}\n")
    open(os.path.join(ws, "model.py"), "w").write(HELPER.format(features=json.dumps(T.features)))
    history = "\n".join(f"{j}. {corr_text(T, j, mode)}" for j in range(1, k)) or "(none)"
    open(os.path.join(ws, "TASK.md"), "w").write(TASK.format(
        k=k, K=K, nin=len(T.features), order=", ".join(T.features), doc=T.feature_doc, py=PY,
        history=history, correction=corr_text(T, k, mode), n=len(ev)))
    if mode != "text":
        # Earlier steps' evidence stays available so earlier inferred rules can be checked.
        for j in range(1, k):
            ej = np.load(os.path.join(sdir(T, seed), f"evidence_{j}.npy"))
            with open(os.path.join(ws, f"evidence_step{j}.csv"), "w") as f:
                f.write(",".join(T.features) + ",escalate\n")
                rows_j = [row[:-1] for row in ej]
                ans = os.path.join(sdir(T, seed), tag(llm, rep, mode), f"step{j}", "answers.npy")
                if os.path.exists(ans):
                    rows_j += list(np.load(ans))
                for x in rows_j:
                    f.write(",".join(f"{v:.17g}" for v in x) + f",{int(T.target(np.asarray(x)[None, :], k)[0])}\n")
    t0 = time.time()
    status = "ok"
    if mode.startswith("query"):
        # Phase 1: candidates + label queries. The harness answers from ground truth.
        q = int(re.findall(r"\d+", mode)[0])
        text = QUERY.format(q=q)
        if mode.endswith("w"):
            # Wide mode: the candidate list must span several kinds of rule.
            text += WIDE.format(query_line=("Pick queries that separate the kinds first, then values." if q
                                            else "Then choose the best-supported candidate yourself."))
        if q == 0:
            text = text.replace("2. Write `query.csv`", "2. (Skipped: no queries in this run.) Do not write `query.csv`")
        open(os.path.join(ws, "QUERY.md"), "w").write(text)
        status = call_codex(llm, ws, PHASE_A, "codex_a.log", q=q, T=T)
        answer_queries(T, k, ws, q)
        status = call_codex(llm, ws, PHASE_B, "codex.log") if status == "ok" else status
    else:
        status = call_codex(llm, ws, "Read TASK.md and complete the task exactly as written.", "codex.log")
    secs = time.time() - t0
    shutil.rmtree(keep, ignore_errors=True)
    shutil.copytree(ws, keep, ignore=shutil.ignore_patterns("*.profraw"))
    logtxt = "".join(open(p, errors="replace").read() for p in sorted(glob.glob(os.path.join(keep, "codex*.log"))))
    leaks = sorted({m.group(0) for m in re.finditer(LEAK_RE, logtxt)})
    tok = re.findall(r"tokens used\s*\n?\s*([\d,'’]+)", logtxt)
    info = {"status": status, "seconds": round(secs), "leaks": leaks,
            "tokens": sum(int(re.sub(r"\D", "", t)) for t in tok) if tok else None}
    json.dump(info, open(os.path.join(keep, "done.json"), "w"))
    return info


def chain(T, seed, llm, rep, mode="text"):
    d = sdir(T, seed)
    base = lab.load(os.path.join(d, "base.json"))
    Xt = np.load(os.path.join(d, "test.npy"))
    current = os.path.join(d, "base.json")
    rows = []
    for k in range(1, len(T.corrections) + 1):
        info = run_step(T, seed, llm, rep, k, current, mode)
        out = os.path.join(d, tag(llm, rep, mode), f"step{k}", "model_out.json")
        try:
            layers = lab.load(out)
            assert np.all(np.isfinite(lab.forward(layers, Xt[:10])))
            valid = True
        except Exception:  # missing or malformed output counts as "no edit this step"
            layers, out, valid = lab.load(current), current, False
        row = {"task": T.name, "seed": seed, "llm": llm, "mode": mode, "rep": rep, "step": k, "valid": valid,
               **info, **evaluate(T, layers, base, Xt, k)}
        rows.append(row)
        print(json.dumps({key: (round(v, 4) if isinstance(v, float) else v) for key, v in row.items()}), flush=True)
        current = out
    json.dump(rows, open(os.path.join(d, tag(llm, rep, mode), "results.json"), "w"), indent=1)
    return rows


# ---------------- gradient baselines ----------------

def finetune_chain(T, seed, lr, steps, ratio, cumulative, replay=True, n_labels=None, run_seed=0):
    """Sequential fine-tune. Replay: 4096 random inputs soft-labelled by the current
    model. Evidence is repeated so it makes up `ratio` of the training rows, whatever
    its size. cumulative=True keeps every earlier correction's labels too."""
    d = sdir(T, seed)
    base = lab.load(os.path.join(d, "base.json"))
    Xt = np.load(os.path.join(d, "test.npy"))
    rng = np.random.default_rng(run_seed)
    layers = [{a: b.copy() for a, b in L.items()} for L in base]
    rows, seen = [], []
    for k in range(1, len(T.corrections) + 1):
        if n_labels is None:
            ev = np.load(os.path.join(d, f"evidence_{k}.npy"))
            Xe, ye = ev[:, :-1], ev[:, -1]
        else:
            Xe, ye = evidence(T, k, np.random.default_rng(30_000 + 97 * seed + k), (n_labels // 2, n_labels // 2))
        seen.append((Xe, ye))
        if cumulative:
            # Earlier labels are relabelled with the current target: a later correction
            # can override an earlier one (e.g. maintenance beats critical tier).
            Xe = np.vstack([x for x, _ in seen])
            ye = T.target(Xe, k)
        if replay:
            Xr = T.sample(4096, rng)
            soft_r = 1 / (1 + np.exp(-lab.forward(layers, Xr)))
            rep = max(1, round(ratio / (1 - ratio) * len(Xr) / len(Xe)))
            Xtr = np.vstack([Xr] + [Xe] * rep)
            soft = np.concatenate([soft_r] + [ye.astype(float)] * rep)
        else:
            Xtr, soft = Xe, ye.astype(float)
        lab.train(layers, Xtr, None, steps=steps, lr=lr, rng=rng, batch=256, soft=soft)
        rows.append({"step": k, **evaluate(T, layers, base, Xt, k)})
    return rows


def scratch(T, seed, n):
    """Train a fresh net of the base size on n uniform labels of the final rule."""
    d = sdir(T, seed)
    base = lab.load(os.path.join(d, "base.json"))
    Xt = np.load(os.path.join(d, "test.npy"))
    rng = np.random.default_rng(40_000 + seed)
    X = T.sample(n, rng)
    K = len(T.corrections)
    layers = lab.init(T.sizes, rng)
    lab.train(layers, X, T.target(X, K), steps=min(30000, max(3000, 30 * n // 256 * 8)), lr=1e-3, rng=rng)
    return evaluate(T, layers, base, Xt, K)


def baselines(T, seed):
    d = sdir(T, seed)
    base = lab.load(os.path.join(d, "base.json"))
    Xt = np.load(os.path.join(d, "test.npy"))
    K = len(T.corrections)
    out = {"unedited": [{"step": k, **evaluate(T, base, base, Xt, k)} for k in range(1, K + 1)],
           "grid": [], "label_curve": [], "scratch_curve": []}
    # Picking the best grid point by hidden-test accuracy is an oracle choice that
    # favours the baseline; that is deliberate.
    for cumulative in (False, True):
        for lr in (1e-3, 3e-3):
            for steps in (300, 1000, 3000):
                for ratio in (0.25, 0.5):
                    rows = finetune_chain(T, seed, lr, steps, ratio, cumulative)
                    out["grid"].append({"replay": True, "cumulative": cumulative, "lr": lr, "steps": steps,
                                        "ratio": ratio, "rows": rows})
                    print(T.name, seed, "grid cum", cumulative, lr, steps, ratio, round(rows[-1]["acc_all"], 4), flush=True)
    for lr in (1e-3, 3e-3):
        for steps in (300, 1000):
            rows = finetune_chain(T, seed, lr, steps, 0.5, False, replay=False)
            out["grid"].append({"replay": False, "cumulative": False, "lr": lr, "steps": steps, "rows": rows})
    best = max((g for g in out["grid"] if g["replay"]), key=lambda g: g["rows"][-1]["acc_all"])
    for n in (32, 128, 512, 2048, 8192):
        # Re-tune steps, lr and ratio for each label count (oracle pick again).
        cands = [finetune_chain(T, seed, lr, st, ra, True, n_labels=n)
                 for lr in (1e-3, 3e-3) for st in (300, 1000, 3000) for ra in (0.5, 0.8)]
        rows = max(cands, key=lambda r: r[-1]["acc_all"])
        out["label_curve"].append({"n_labels": n, "rows": rows})
        print(T.name, seed, "labels", n, round(rows[-1]["acc_all"], 4), flush=True)
    for n in (1000, 4000, 16000, 64000):
        r = scratch(T, seed, n)
        out["scratch_curve"].append({"n_labels": n, **r})
        print(T.name, seed, "scratch", n, round(r["acc_all"], 4), flush=True)
    json.dump(out, open(os.path.join(d, "baselines.json"), "w"), indent=1)


if __name__ == "__main__":
    cmd, T = sys.argv[1], TASKS[sys.argv[2]]
    if cmd == "base":
        for s in sys.argv[3:]:
            make_base(T, int(s))
    elif cmd == "baselines":
        with ThreadPoolExecutor(len(sys.argv[3:])) as ex:
            list(ex.map(lambda s: baselines(T, int(s)), sys.argv[3:]))
    elif cmd == "smoke":
        # End-to-end dry run with a no-op editor and a short baseline; must pass before launches.
        import tempfile
        os.environ.setdefault("WSROOT", tempfile.mkdtemp())
        s = int(sys.argv[3])
        rows = chain(T, s, "noop", 0)
        assert len(rows) == len(T.corrections) and all(r["valid"] for r in rows)
        assert rows[0]["drift_untouched"] == 0.0
        finetune_chain(T, s, 1e-3, 5, 0.5, True)
        scratch(T, s, 300)
        shutil.rmtree(os.path.join(sdir(T, s), "noop-r0"))
        # Leak pattern: must catch real ground-truth reads and ignore look-alike names.
        hit = lambda t: bool(re.search(LEAK_RE, t))
        assert hit("cat /x/weight-edit-lab/tasks.py") and hit("np.load('test.npy')") and hit("evidence_3.npy")
        assert not hit("'evidence_passed': 32") and not hit("evidence.csv") and not hit("def target(x):")
        # Written evidence must reproduce its labels from the written numbers (no rounding drift).
        ws0 = os.path.join(os.environ["WSROOT"], T.name, f"s{s}", "noop-r0")
        for k in range(1, len(T.corrections) + 1):
            d = np.genfromtxt(os.path.join(ws0, f"step{k}", "evidence.csv"), delimiter=",", skip_header=1)
            assert np.array_equal(T.target(d[:, :-1], k), d[:, -1].astype(int)), f"label drift in step {k} evidence"
        print("SMOKE OK", T.name, flush=True)
    elif cmd == "edits":
        seeds = [int(s) for s in sys.argv[3].split(",")]
        reps, llms = int(sys.argv[4]), sys.argv[5].split(",")
        workers = int(sys.argv[6]) if len(sys.argv) > 6 else 6
        mode = sys.argv[7] if len(sys.argv) > 7 else "text"
        jobs = [(s, m, r) for r in range(reps) for s in seeds for m in llms]
        with ThreadPoolExecutor(workers) as ex:
            futs = [ex.submit(chain, T, s, m, r, mode) for s, m, r in jobs]
            for f in futs:
                try:
                    f.result()
                except Exception as e:
                    print("CHAIN ERROR", repr(e), flush=True)
