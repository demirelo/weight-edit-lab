"""results/error_rates.png: test error after all corrections, per method, per network size."""
import json
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from tasks import TASKS

ROOT = os.path.abspath(os.path.dirname(__file__))
S = json.load(open(f"{ROOT}/results/summary.json"))

SURFACE, INK, INK2, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#e4e3df"
HL, BASE = "#2a78d6", "#b9b8b2"  # categorical slot 1 for hand-edits, neutral for baselines

PANELS = [("small", "129 params"), ("large", "5,569 params"), ("xl", "76,544 params")]
panels = [(t, title) for t, title in PANELS if t in S and S[t]["llm"]]


def rows(t):
    r, b = S[t], S[t]["baselines"]
    lc, sc = b.get("label_curve_acc_all", {}), b.get("scratch_curve_acc_all", {})
    out = [("Unedited base", b["unedited"]["acc_all"]["mean"], False)] if "unedited" in b else []
    if "32" in lc:
        out.append(("Fine-tune, 32 labels/fix", lc["32"]["mean"], False))
    if "8192" in lc:
        out.append(("Fine-tune, 8,192 labels/fix", lc["8192"]["mean"], False))
    if "64000" in sc:
        out.append(("Retrain, 64,000 labels", sc["64000"]["mean"], False))
    n = sum(TASKS[t].n_evidence)
    for llm, name in (("astra", "Astra writes the weights"), ("sol", "Sol writes the weights")):
        if llm in r["llm"]:
            out.append((name, r["llm"][llm]["acc_all"]["mean"], True))
    hid = [r["llm"][k]["acc_all"]["mean"] for k in ("astra-hidden", "sol-hidden") if k in r["llm"]]
    if hid:
        out.append(("LLM writes weights, examples only", sum(hid) / len(hid), False))
    return [(n, 100 * (1 - a), h) for n, a, h in out]


fig, axes = plt.subplots(1, len(panels), figsize=(4.2 * len(panels), 3.6), sharey=True, facecolor=SURFACE)
axes = [axes] if len(panels) == 1 else axes
for ax, (t, title) in zip(axes, panels):
    data = rows(t)[::-1]
    names_all = ["Unedited base", "Fine-tune, 32 labels/fix", "Fine-tune, 8,192 labels/fix", "Retrain, 64,000 labels",
                 "LLM writes weights, examples only", "Astra writes the weights", "Sol writes the weights"][::-1]
    # Same row order in every panel; missing rows stay empty.
    got = {d[0]: d for d in data}
    data = [got.get(n, (n, 0.0, False)) for n in names_all]
    names = [d[0] for d in data]
    ax.barh(names, [d[1] for d in data], color=[HL if d[2] else BASE for d in data], height=0.6,
            edgecolor=SURFACE, linewidth=2)
    xmax = max(d[1] for d in data)
    for i, d in enumerate(data):
        if d[1] == 0.0:
            ax.text(xmax * 0.02, i, "not run", va="center", fontsize=8, color=INK2)
            continue
        ax.text(d[1] + xmax * 0.02, i, f"{d[1]:.1f}%", va="center", fontsize=9, color=INK)
    ax.set_xlim(0, xmax * 1.25)
    ax.set_facecolor(SURFACE)
    ax.set_title(f"{title}\nLLM sees {sum(TASKS[t].n_evidence)} examples per fix", fontsize=10, color=INK, loc="left")
    ax.grid(axis="x", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(GRID)
    ax.tick_params(colors=INK2, labelsize=9, length=0)
    ax.set_xlabel("test error after 5 corrections (%)" if t != "small" else "test error after 3 corrections (%)",
                  fontsize=9, color=INK2)
fig.suptitle("LLM hand-writes weight patches for planted defects: lower is better",
             fontsize=12, color=INK, x=0.01, ha="left")
fig.tight_layout()
os.makedirs(f"{ROOT}/results", exist_ok=True)
fig.savefig(f"{ROOT}/results/error_rates.png", dpi=200, facecolor=SURFACE)
print("wrote results/error_rates.png")
