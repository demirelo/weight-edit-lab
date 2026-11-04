"""results/laya_error.png: final Laya test error per method in the sandboxed rerun (bars from zero,
one dot per seed), from results/summary_round2.json (`ROUND=2 python laya_analyze.py`)."""
import json
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

HERE = os.path.dirname(os.path.abspath(__file__))
S = json.load(open(f"{HERE}/results/summary_round2.json"))
A, B = S["arms"], S["baselines"]
SEEDS = {}
for c in S["per_chain"]:
    SEEDS.setdefault(c["arm"], []).append(c["acc_all"])

SURFACE, INK, INK2, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#e4e3df"
WEIGHTS, CODE, BASE = "#2a78d6", "#eb6834", "#b9b8b2"  # categorical slots 1 and 2, neutral

rows = [
    ("Unedited Laya", 0.7029, BASE, None),
    ("Fine-tune, 32 labels/fix", B["finetune_32_best"]["acc_all"], BASE, None),
    ("Code patch: Fable 5.1 (high)", A["fable-high-code"]["acc_all"], CODE, "fable-high-code"),
    ("Code patch: Opus 5.5 (high)", A["opus-high-code"]["acc_all"], CODE, "opus-high-code"),
    ("Weights: Opus 5.5 (high)", A["opus-high-text"]["acc_all"], WEIGHTS, "opus-high-text"),
    ("Weights: Fable 5.1 (high)", A["fable-high-text"]["acc_all"], WEIGHTS, "fable-high-text"),
    ("Weights: Opus 5.5 (medium)", A["opus-text"]["acc_all"], WEIGHTS, "opus-text"),
][::-1]

fig, ax = plt.subplots(figsize=(7.2, 3.8), facecolor=SURFACE)
vals = [100 * (1 - r[1]) for r in rows]
ax.barh([r[0] for r in rows], vals, color=[r[2] for r in rows], height=0.62, edgecolor=SURFACE, linewidth=2)
for i, (r, v) in enumerate(zip(rows, vals)):
    seeds = [100 * (1 - a) for a in SEEDS.get(r[3], [])]
    ax.scatter(seeds, [i] * len(seeds), s=22, color=INK, zorder=3, edgecolor=SURFACE, linewidth=1.2)
    # Value at the bar start: seed dots sit near the bar end and the dashed line past it.
    ax.text(0.5, i, f"{v:.1f}%", va="center", ha="left", fontsize=9, color=INK if r[2] == BASE else "white")
ax.axvline(100 * (1 - 0.7029), color=INK2, linewidth=0.8, linestyle=(0, (3, 3)))
ax.set_xlim(0, 44)
ax.set_facecolor(SURFACE)
ax.grid(axis="x", color=GRID, linewidth=0.8)
ax.set_axisbelow(True)
for s in ("top", "right", "left"):
    ax.spines[s].set_visible(False)
ax.spines["bottom"].set_color(GRID)
ax.tick_params(colors=INK2, labelsize=9, length=0)
ax.set_xlabel("test error (%), 3,080 messages; bar = mean of 2 seeds; dashed = unedited", fontsize=9, color=INK2)
ax.set_title("Laya test error after 3 fixes: lower is better", fontsize=11, color=INK, loc="left")
ax.legend(handles=[Patch(color=CODE, label="code patch"), Patch(color=WEIGHTS, label="weight edit"),
                   Patch(color=BASE, label="baseline"),
                   plt.Line2D([], [], marker="o", color=INK, linestyle="", markersize=4.5, label="one seed")], loc="upper right", frameon=False, fontsize=9)
fig.tight_layout()
os.makedirs(f"{HERE}/../results", exist_ok=True)
fig.savefig(f"{HERE}/../results/laya_error.png", dpi=200, facecolor=SURFACE)
print("wrote results/laya_error.png")
