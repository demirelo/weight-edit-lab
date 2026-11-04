"""Laya pilot: sequential hand-written edits to Laya's scorer.

  python laya_harness.py smoke
  python laya_harness.py edits <seeds,> <llm,llm> [workers] [mode]     # mode: text | code
  python laya_harness.py baselines

Ground truth: departments.py. Corrections and their intents: corrections.json.
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
import laya_lab as L

HERE = os.path.dirname(os.path.abspath(__file__))
PY = os.path.join(HERE, "..", ".venv", "bin", "python")
PY = os.path.abspath(PY)
# (tool, model, effort). Every editor gets an explicit effort, recorded in done.json.
# "opus" ran with no --effort flag, i.e. the Claude Code default "medium".
LLMS = {"astra": ("codex", "gpt-6-astra", "high"), "sol": ("codex", "gpt-6.1-sol", "high"),
        "opus": ("claude", "claude-opus-5-5", "medium"), "opus-high": ("claude", "claude-opus-5-5", "high"),
        "fable-high": ("claude", "claude-fable-5-1", "high")}
CORR = json.load(open(os.path.join(HERE, "corrections.json"))) if os.path.exists(os.path.join(HERE, "corrections.json")) else []
LEAK_RE = r"weight-edit-hidden|weight-edit-lab/laya/(laya_harness|corrections)|test\.npz|cache/train\.npz|weight-edit-lab/laya/runs"


def data(split):
    d = np.load(os.path.join(L.HIDDEN, f"{split}.npz"))
    return {k: d[k] for k in d.files}


# ---------------- metrics ----------------

def evaluate(pred, base, T, k):
    """pred, base: department indices on the test cache T. Corrections 1..k applied."""
    y = T["y"]
    out = {"acc_all": float((pred == y).mean())}
    corr_int = [set(c["intents"]) for c in CORR]
    inn = lambda j: np.isin(T["intents"], list(corr_int[j]))
    out["fix_latest"] = float((pred[inn(k - 1)] == y[inn(k - 1)]).mean())
    if k >= 2:
        reg = np.zeros(len(y), bool)
        for j in range(k - 1):
            reg |= inn(j)
        out["retain_earlier"] = float((pred[reg] == y[reg]).mean())
    other = ~np.any([inn(j) for j in range(len(CORR))], axis=0)
    out["drift_other"] = float((pred[other] != base[other]).mean())
    out["acc_other"] = float((pred[other] == y[other]).mean())
    return out


# ---------------- evidence ----------------

def evidence(k, seed, n_in=16, n_out=16):
    """Train messages for correction k: n_in from its intents, n_out near misses from
    intents whose true department is the correction's department or the wrong one."""
    Tr = data("train")
    base_S = L.load_scorer(os.path.join(HERE, "cache/scorer_base.npz"))
    p = L.predict(base_S, Tr["M"])
    rng = np.random.default_rng(1000 * seed + k)
    c = CORR[k - 1]
    inn = np.isin(Tr["intents"], c["intents"])
    wrong = np.flatnonzero(inn & (p != Tr["y"]))
    right = np.flatnonzero(inn & (p == Tr["y"]))
    take_in = list(rng.permutation(wrong)[:n_in])
    take_in += list(rng.permutation(right)[:n_in - len(take_in)])
    all_corr = np.isin(Tr["intents"], sum([x["intents"] for x in CORR], []))
    near_depts = [L.DEPTS.index(c["dept"]), L.DEPTS.index(c["from_dept"])]
    near = np.flatnonzero(~all_corr & np.isin(Tr["y"], near_depts) & (p == Tr["y"]))
    take_out = list(rng.permutation(near)[:n_out])
    idx = np.array(take_in + take_out)
    return Tr["texts"][idx], Tr["y"][idx], Tr["M"][idx]


# ---------------- editor workspace ----------------

SCORER_PY = '''"""Laya scorer helper. M: [n, 5, 1024] marker vectors (one per department option)."""
import numpy as np, torch
DEPTS = {depts}
def load(path):
    d = np.load(path); return {{k: d[k] for k in d.files}}
def save(S, path):
    np.savez(path, **S)
def gelu(x):
    return 0.5 * x * (1 + torch.erf(torch.from_numpy(np.ascontiguousarray(x)) / np.sqrt(2)).numpy())
def logits(S, M):
    mu = M.mean(-1, keepdims=True); var = M.var(-1, keepdims=True)
    h = (M - mu) / np.sqrt(var + 1e-5) * S["ln_w"] + S["ln_b"]
    z = (gelu(h @ S["W1"] + S["b1"]) @ S["W2"] + S["b2"])[..., 0]
    i, e = 0, M
    while f"extra_W{{i}}" in S:
        e = e @ S[f"extra_W{{i}}"] + S[f"extra_b{{i}}"]
        if f"extra_W{{i + 1}}" in S:
            e = np.maximum(e, 0)
        i += 1
    return z + e[..., 0] if i else z
def predict(S, M):
    return [DEPTS[i] for i in logits(S, M).argmax(-1)]
'''

EMBED_PY = '''"""Run frozen Laya on your own messages: python embed.py out.npz "message 1" "message 2" ...
Writes M [n, 5, 1024]: the scorer input for each department option. Takes ~10 s to load."""
import sys
sys.path.insert(0, {laya!r})
import numpy as np, laya_lab as L
a = L.load_agent()
np.savez(sys.argv[1], M=L.marker_vectors(a, sys.argv[2:]))
print("wrote", sys.argv[1], len(sys.argv) - 2, "messages")
'''

TASK = """# Weight-editing task (step {k} of {K})

You are editing part of a neural network BY HAND. Do not train it.

## The model
Laya is a decision model. For a customer message it routes to one of 5 support
departments: {depts}. A frozen encoder turns (message, option) into one
1024-number vector per option (the "marker vector"). A small scorer gives each
option a logit; the highest logit wins. You edit ONLY the scorer.

- `scorer_in.npz`: scorer weights. Scorer = LayerNorm(ln_w, ln_b) -> W1 (1024x1024),
  b1 -> GELU -> W2 (1024x1), b2. You may also add a ReLU module on the raw marker
  vector: arrays extra_W0, extra_b0, extra_W1, extra_b1, ... (ReLU between layers,
  last layer has 1 output); its output is added to the logit.
- `scorer.py`: `load`, `save`, `logits(S, M)`, `predict(S, M)`.
- `embed.py`: run the frozen encoder on messages you write yourself:
  `{py} embed.py out.npz "message" ...` -> out.npz with M [n, 5, 1024].
- `evidence.csv` + `evidence_M.npz`: {n} labelled customer messages for this
  correction and their marker vectors (same order).
Use this Python, which has numpy and torch: `{py}`

## Department descriptions given to the model
{dept_doc}

## Corrections already applied in earlier steps (must stay true)
{history}

## New correction for this step
{correction}

## What to do
Write `scorer_out.npz` (same format) so that the model:
1. follows the new correction for all such messages, not only the examples;
2. still follows every earlier correction;
3. otherwise routes exactly as `scorer_in.npz` does.
A hidden test set of 3,080 real customer messages scores all three.

## Rules
- Allowed: read weights, run the scorer and the encoder on inputs you choose,
  reason about directions and units, change any scorer weights, add the extra module.
- Not allowed: gradient descent, optimizers, any training or fitting loop,
  least squares, logistic regression or any solver fitted to data. Every weight
  you write must come from your own reasoning. Computing a direction as a
  difference of means of marker vectors of messages YOU wrote is allowed;
  fitting to the evidence labels is not. Checking with forward passes is fine.
- Write `NOTES.md`: what you changed and why, in under 200 words.
"""

CODE_TASK = """# Patch task (step {k} of {K}): write a code override, not weights

Laya routes customer messages to one of 5 departments: {depts}.
`router.py` holds the current routing patch: `route(text, laya_dept) -> dept`.
It receives the message and Laya's current answer and returns the final answer.

## Department descriptions given to the model
{dept_doc}

## Corrections already applied in earlier steps (must stay true)
{history}

## New correction for this step
{correction}

`evidence.csv` has {n} labelled messages for this correction (text, Laya's
current answer, correct department).

Edit `router.py` so the final answers follow the new correction for all such
messages, keep earlier corrections, and otherwise keep Laya's answer. Plain Python
only (re, string ops); no ML libraries, no training. A hidden test set scores it.
Write `NOTES.md` (under 200 words).
"""


def tag(llm, rep, mode):
    return f"{llm}-r{rep}" if mode == "text" else f"{llm}-{mode}-r{rep}"


def call_editor(llm, ws, prompt, logname):
    tool, model, effort = LLMS.get(llm, (None, None, None))
    with open(os.path.join(ws, logname), "w") as log:
        if llm == "noop":
            if os.path.exists(os.path.join(ws, "scorer_in.npz")):
                shutil.copy(os.path.join(ws, "scorer_in.npz"), os.path.join(ws, "scorer_out.npz"))
            return "ok"
        if tool == "codex":
            cmd = ["codex", "exec", "-m", model, "-c", f"model_reasoning_effort={effort}", "--sandbox", "workspace-write",
                   "--skip-git-repo-check", "-C", ws, prompt]
        else:
            # Opus: file tools plus this venv's python and read-only shell tools; nothing else.
            # stream-json + verbose keeps the full tool transcript, so reads can be audited.
            cmd = ["claude", "-p", prompt, "--model", model, "--output-format", "stream-json", "--verbose"] + (["--effort", effort] if effort and llm != "opus" else []) + ["--permission-mode", "acceptEdits",
                   "--allowedTools", "Read", "Write", "Edit", "Glob", "Grep", f"Bash({PY}:*)",
                   "Bash(ls:*)", "Bash(head:*)", "Bash(cat:*)", "Bash(wc:*)"]
        try:
            subprocess.run(cmd, cwd=ws, stdin=subprocess.DEVNULL, stdout=log, stderr=subprocess.STDOUT, timeout=3600)
            return "ok"
        except subprocess.TimeoutExpired:
            return "timeout"


def dept_doc():
    return "\n".join(f"- {k}: {v}" for k, v in L.DEPARTMENTS.items())


def run_step(seed, llm, rep, k, model_in, mode):
    K = len(CORR)
    keep = os.path.join(HERE, "runs", f"seed{seed}", tag(llm, rep, mode), f"step{k}")
    if os.path.exists(os.path.join(keep, "done.json")):
        return json.load(open(os.path.join(keep, "done.json")))
    ws = os.path.join(os.environ["WSROOT"], "laya", f"s{seed}", tag(llm, rep, mode), f"step{k}")
    shutil.rmtree(ws, ignore_errors=True)
    os.makedirs(ws)
    texts, y, M = evidence(k, seed)
    history = "\n".join(f"{j}. {CORR[j - 1]['text']}" for j in range(1, k)) or "(none)"
    fmt = dict(k=k, K=K, depts=", ".join(L.DEPTS), dept_doc=dept_doc(), history=history,
               correction=CORR[k - 1]["text"], n=len(y), py=PY)
    if mode == "code":
        shutil.copy(model_in, os.path.join(ws, "router.py"))
        base_S = L.load_scorer(os.path.join(HERE, "cache/scorer_base.npz"))
        cur = apply_router(model_in, list(texts), [L.DEPTS[i] for i in L.predict(base_S, M)])
        with open(os.path.join(ws, "evidence.csv"), "w") as f:
            f.write("text\tlaya_answer\tcorrect\n")
            for t, c, yy in zip(texts, cur, y):
                f.write(f"{t}\t{c}\t{L.DEPTS[yy]}\n")
        open(os.path.join(ws, "TASK.md"), "w").write(CODE_TASK.format(**fmt))
    else:
        shutil.copy(model_in, os.path.join(ws, "scorer_in.npz"))
        np.savez(os.path.join(ws, "evidence_M.npz"), M=M)
        with open(os.path.join(ws, "evidence.csv"), "w") as f:
            f.write("text\tcorrect\n")
            for t, yy in zip(texts, y):
                f.write(f"{t}\t{L.DEPTS[yy]}\n")
        open(os.path.join(ws, "scorer.py"), "w").write(SCORER_PY.format(depts=json.dumps(L.DEPTS)))
        open(os.path.join(ws, "embed.py"), "w").write(EMBED_PY.format(laya=HERE))
        open(os.path.join(ws, "TASK.md"), "w").write(TASK.format(**fmt))
    t0 = time.time()
    status = call_editor(llm, ws, "Read TASK.md and complete the task exactly as written.", "editor.log")
    secs = time.time() - t0
    shutil.rmtree(keep, ignore_errors=True)
    shutil.copytree(ws, keep, ignore=shutil.ignore_patterns("*.profraw", "out*.npz"))
    logtxt = open(os.path.join(keep, "editor.log"), errors="replace").read()
    info = {"status": status, "seconds": round(secs), "effort": LLMS.get(llm, (None, None, None))[2] or "cli-default",
            "leaks": sorted({m.group(0) for m in re.finditer(LEAK_RE, logtxt)})}
    json.dump(info, open(os.path.join(keep, "done.json"), "w"))
    return info


def apply_router(path, texts, laya_depts):
    ns = {}
    exec(compile(open(path).read(), path, "exec"), ns)
    out = []
    for t, d in zip(texts, laya_depts):
        try:
            r = ns["route"](str(t), d)
            out.append(r if r in L.DEPTS else d)
        except Exception:  # a crashing patch keeps Laya's answer
            out.append(d)
    return out


def chain(seed, llm, rep, mode="text"):
    T = data("test")
    base_S = L.load_scorer(os.path.join(HERE, "cache/scorer_base.npz"))
    d = os.path.join(HERE, "runs", f"seed{seed}", tag(llm, rep, mode))
    os.makedirs(d, exist_ok=True)
    if mode == "code":
        current = os.path.join(d, "router0.py")
        open(current, "w").write("def route(text, laya_dept):\n    return laya_dept\n")
    else:
        current = os.path.join(HERE, "cache/scorer_base.npz")
    rows = []
    for k in range(1, len(CORR) + 1):
        info = run_step(seed, llm, rep, k, current, mode)
        out = os.path.join(d, f"step{k}", "router.py" if mode == "code" else "scorer_out.npz")
        base_pred = L.predict(base_S, T["M"])
        try:
            if mode == "code":
                final = apply_router(out, list(T["texts"]), [L.DEPTS[i] for i in base_pred])
                pred = np.array([L.DEPTS.index(x) for x in final])
            else:
                S = L.load_scorer(out)
                assert np.all(np.isfinite(L.scorer_logits(S, T["M"][:4])))
                pred = L.predict(S, T["M"])
            valid = True
        except Exception:  # missing or broken output: keep the previous model
            out, valid = current, False
            pred = rows[-1]["_pred"] if rows else base_pred
        row = {"seed": seed, "llm": llm, "mode": mode, "rep": rep, "step": k, "valid": valid, **info,
               **evaluate(pred, base_pred, T, k)}
        row["_pred"] = pred
        rows.append(row)
        print(json.dumps({a: (round(b, 4) if isinstance(b, float) else b) for a, b in row.items() if a != "_pred"}), flush=True)
        current = out
    for r in rows:
        np.save(os.path.join(d, f"step{r['step']}", "test_pred.npy"), r.pop("_pred"))
    json.dump(rows, open(os.path.join(d, "results.json"), "w"), indent=1)
    return rows


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "smoke":
        import tempfile
        os.environ.setdefault("WSROOT", tempfile.mkdtemp())
        for mode in ("text", "code"):
            rows = chain(99, "noop", 0, mode)
            assert len(rows) == len(CORR) and all(r["valid"] for r in rows), rows
            assert rows[0]["drift_other"] == 0.0
            shutil.rmtree(os.path.join(HERE, "runs", "seed99"))
        # Nothing an editor can reach under the lab may hold test data, raw labels or the truth map.
        assert not any(os.path.exists(os.path.join(HERE, "cache", f)) for f in ("test.npz", "train.npz"))
        assert not os.path.exists(os.path.join(HERE, "data"))
        assert "INTENT_DEPT" not in open(os.path.join(HERE, "departments.py")).read()
        hit = lambda t: bool(re.search(LEAK_RE, t))
        assert hit("cat ~/.weight-edit-hidden/laya/departments_truth.py") and hit("np.load('cache/test.npz')")
        assert not hit("evidence.csv") and not hit("scorer_in.npz")
        print("SMOKE OK", flush=True)
    elif cmd == "edits":
        seeds = [int(s) for s in sys.argv[2].split(",")]
        llms = sys.argv[3].split(",")
        workers = int(sys.argv[4]) if len(sys.argv) > 4 else 6
        mode = sys.argv[5] if len(sys.argv) > 5 else "text"
        jobs = [(s, m) for s in seeds for m in llms]
        with ThreadPoolExecutor(workers) as ex:
            for f in [ex.submit(chain, s, m, 0, mode) for s, m in jobs]:
                try:
                    f.result()
                except Exception as e:
                    print("CHAIN ERROR", repr(e), flush=True)
