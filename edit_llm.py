"""Apply the three corrections in sequence with a Codex model as the weight editor.

Each step gets a fresh workspace that holds only: the current weights, a tiny
forward-pass helper, the correction history (text), and that step's 24 labelled
examples. The ground truth (lab.py) and the hidden test set stay outside.

Usage: python edit_llm.py <codex-model-id> <tag>
"""
import json
import os
import shutil
import subprocess
import sys
import time
import numpy as np
import lab

MODEL, TAG = sys.argv[1], sys.argv[2]
ROOT = os.path.abspath(os.path.dirname(__file__))
PY = os.path.join(ROOT, ".venv/bin/python")
# Workspaces live outside the lab so the editor cannot stumble on lab.py or hidden/.
WSROOT = os.environ["WSROOT"]

HELPER = '''import json, numpy as np
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
'''

TASK = """# Weight-editing task (step {k} of 3)

You are editing a small neural network BY HAND. Do not train it.

## The model
`model_in.json` is a ReLU MLP. Input: 6 features, in this order:
- impact, urgency, users_affected, tone_anger, confidence: real numbers in [0, 1]
- startup_phase: 0 or 1

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


def run_step(k, model_in):
    ws = os.path.join(WSROOT, TAG, f"step{k}")
    shutil.rmtree(ws, ignore_errors=True)
    os.makedirs(ws)
    shutil.copy(model_in, os.path.join(ws, "model_in.json"))
    shutil.copy(os.path.join(ROOT, f"evidence/correction_{k}.csv"), os.path.join(ws, "evidence.csv"))
    open(os.path.join(ws, "model.py"), "w").write(HELPER)
    history = "\n".join(f"{j}. {lab.CORRECTIONS[j - 1]}" for j in range(1, k)) or "(none)"
    open(os.path.join(ws, "TASK.md"), "w").write(TASK.format(
        k=k, py=PY, history=history, correction=lab.CORRECTIONS[k - 1], n=24))
    t0 = time.time()
    with open(os.path.join(ws, "codex.log"), "w") as log:
        subprocess.run(["codex", "exec", "-m", MODEL, "-c", "model_reasoning_effort=high",
                        "--sandbox", "workspace-write", "--skip-git-repo-check", "-C", ws,
                        "Read TASK.md and complete the task exactly as written."],
                       stdin=subprocess.DEVNULL, stdout=log, stderr=subprocess.STDOUT, timeout=3600)
    secs = time.time() - t0
    keep = os.path.join(ROOT, "runs", TAG, f"step{k}")
    shutil.rmtree(keep, ignore_errors=True)
    shutil.copytree(ws, keep)
    log = open(os.path.join(keep, "codex.log")).read()
    leaks = [w for w in ("weight-edit-lab/lab.py", "hidden/test", "def target", "evidence/correction_") if w in log]
    if leaks:
        print(f"step {k}: LEAK SUSPECTED {leaks}", flush=True)
    return os.path.join(keep, "model_out.json"), secs


if __name__ == "__main__":
    Xt = np.load(os.path.join(ROOT, "hidden/test.npy"))
    base = lab.load(os.path.join(ROOT, "runs/base/model.json"))
    current = os.path.join(ROOT, "runs/base/model.json")
    rows = []
    for k in (1, 2, 3):
        out, secs = run_step(k, current)
        try:
            layers = lab.load(out)
        except Exception as e:  # missing or malformed output counts as "no edit"
            print(f"step {k}: invalid output ({e}); keeping previous model", flush=True)
            out, layers = current, lab.load(current)
        row = {"step": k, "seconds": round(secs), **lab.evaluate(layers, base, Xt, k)}
        print(json.dumps(row), flush=True)
        rows.append(row)
        current = out
    json.dump(rows, open(os.path.join(ROOT, "runs", TAG, "results.json"), "w"), indent=1)
