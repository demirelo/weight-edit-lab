"""Frozen Laya up to the scorer input, plus an editable scorer.

The encoder and the 2 head layers stay frozen. For each message we cache the
5 option-marker vectors (5 x 1024) that the scorer sees. The scorer is the
editable part: LayerNorm -> Linear(1024,1024) -> GELU -> Linear(1024,1).

  python laya_lab.py cache      # embed Banking77 train/test, write cache/*.npz
  python laya_lab.py base       # zero-shot accuracy and confusion
"""
import json
import os
import sys
import numpy as np
import torch

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "hub"))
from departments import DEPARTMENTS  # noqa: E402
# Test data, labels and the intent->department truth live outside the lab, out of editors' reach.
HIDDEN = os.environ.get("WEIGHT_EDIT_HIDDEN", os.path.expanduser("~/.weight-edit-hidden/laya"))

DEPTS = list(DEPARTMENTS)
QUESTION = {"type": "choice", "instructions": "Which support department should handle this customer message?",
            "criteria": DEPARTMENTS}


def device():
    # CPU on purpose: MPS hung mid-run (2026-11-04) and editor sandboxes may not reach the GPU.
    return torch.device(os.environ.get("LAYA_DEVICE", "cpu"))


def load_agent():
    from rl_agent_api import RLAgent
    return RLAgent(os.path.join(HERE, "hub"), device=device().type)


@torch.no_grad()
def marker_vectors(agent, texts, batch=32):
    """Return array [n, 5, 1024]: the scorer's input for each option of each message."""
    from rl_common import QTYPES, build_sequence, collate_items
    q = agent._to_internal(QUESTION)
    grabbed = []
    hook = agent.model.scorer.register_forward_hook(lambda m, i, o: grabbed.append(i[0].float().cpu()))
    out = []
    try:
        for s in range(0, len(texts), batch):
            if s and s % (batch * 50) == 0:
                print(f"  {s}/{len(texts)}", flush=True)
            items = []
            for t in texts[s:s + batch]:
                ids, markers = build_sequence(agent.tok, t, q, agent.cfg["max_len"], agent.cfg["head_max_len"])
                assert len(markers) == len(DEPTS)
                items.append({"ids": ids, "markers": markers, "qtype": QTYPES["choice"], "target": [0.0] * 5,
                              "label": -1, "episode": 0, "ep_step": 0, "ep_len": 1, "src": "lab"})
            b = collate_items([items], agent.tok.pad_token_id)
            grabbed.clear()
            dev = agent.device
            agent.model(b["input_ids"].to(dev), b["attention_mask"].to(dev), b["marker_pos"].to(dev),
                        b["marker_mask"].to(dev), b["qtype"].to(dev))
            out.append(grabbed[0].numpy())
    finally:
        hook.remove()
    return np.concatenate(out)


# ---------------- editable scorer (numpy) ----------------

def scorer_from_agent(agent):
    sc = agent.model.scorer
    g = lambda t: t.detach().float().cpu().numpy()
    return {"ln_w": g(sc[0].weight), "ln_b": g(sc[0].bias), "W1": g(sc[1].weight).T, "b1": g(sc[1].bias),
            "W2": g(sc[3].weight).T, "b2": g(sc[3].bias)}


def gelu(x):
    # Exact (erf) GELU, as nn.GELU() uses by default.
    return 0.5 * x * (1 + torch.erf(torch.from_numpy(np.ascontiguousarray(x)) / np.sqrt(2)).numpy())


def scorer_logits(S, M):
    """S: scorer dict; M: [n, k, 1024] marker vectors -> [n, k] logits. Optional extra module 'extra'
    (list of ReLU layers on the raw marker vector) is added to the logit if present."""
    mu = M.mean(-1, keepdims=True)
    var = M.var(-1, keepdims=True)
    h = (M - mu) / np.sqrt(var + 1e-5) * S["ln_w"] + S["ln_b"]
    h = gelu(h @ S["W1"] + S["b1"])
    z = (h @ S["W2"] + S["b2"])[..., 0]
    # Optional added module: ReLU layers extra_W0/extra_b0, extra_W1/extra_b1, ... on the raw
    # marker vector; its scalar output is added to the logit.
    i, e = 0, M
    while f"extra_W{i}" in S:
        e = e @ S[f"extra_W{i}"] + S[f"extra_b{i}"]
        if f"extra_W{i + 1}" in S:
            e = np.maximum(e, 0)
        i += 1
    if i:
        z = z + e[..., 0]
    return z


def predict(S, M):
    return scorer_logits(S, M).argmax(-1)


def save_scorer(S, path):
    np.savez(path, **S)


def load_scorer(path):
    d = np.load(path)
    return {k: d[k] for k in d.files}


# ---------------- data ----------------

def load_split(split):
    import pyarrow.parquet as pq
    sys.path.insert(0, HIDDEN)
    from departments_truth import INTENT_DEPT
    names = json.load(open(os.path.join(HIDDEN, "data/intent_names.json")))
    t = pq.read_table(os.path.join(HIDDEN, f"data/data/{split}-00000-of-00001.parquet")).to_pydict()
    intents = [names[i] for i in t["label"]]
    y = np.array([DEPTS.index(INTENT_DEPT[n]) for n in intents])
    return t["text"], intents, y


if __name__ == "__main__":
    cmd = sys.argv[1]
    os.makedirs(os.path.join(HERE, "cache"), exist_ok=True)
    if cmd == "cache":
        import time
        agent = load_agent()
        save_scorer(scorer_from_agent(agent), os.path.join(HERE, "cache/scorer_base.npz"))
        for split in ("test", "train"):
            texts, intents, y = load_split(split)
            t0 = time.time()
            M = marker_vectors(agent, texts)
            np.savez_compressed(os.path.join(HIDDEN, f"{split}.npz"), M=M.astype(np.float32), y=y,
                                intents=np.array(intents), texts=np.array(texts))
            print(split, M.shape, f"{time.time() - t0:.0f}s", flush=True)
    elif cmd == "base":
        S = load_scorer(os.path.join(HERE, "cache/scorer_base.npz"))
        names = json.load(open(os.path.join(HIDDEN, "data/intent_names.json")))
        for split in ("test", "train"):
            d = np.load(os.path.join(HIDDEN, f"{split}.npz"))
            p = predict(S, d["M"])
            print(split, "zero-shot acc", round(float((p == d["y"]).mean()), 4))
        d = np.load(os.path.join(HIDDEN, "train.npz"))
        p = predict(S, d["M"])
        errs = {}
        for it, yy, pp in zip(d["intents"], d["y"], p):
            if yy != pp:
                errs[(it, DEPTS[pp])] = errs.get((it, DEPTS[pp]), 0) + 1
        tot = {}
        for it in d["intents"]:
            tot[it] = tot.get(it, 0) + 1
        print("largest error clusters (intent -> predicted dept: errors / intent count):")
        for (it, dp), n in sorted(errs.items(), key=lambda x: -x[1])[:15]:
            sys.path.insert(0, HIDDEN)
            from departments_truth import INTENT_DEPT
            print(f"  {it} [{INTENT_DEPT[it]}] -> {dp}: {n}/{tot[it]}")
