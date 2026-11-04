"""results/laya_error.png: final Laya test error per method (bars from zero), from results/summary.json."""
import json
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

HERE = os.path.dirname(os.path.abspath(__file__))
S = json.load(open(f"{HERE}/results/summary.json"))
A, B = S["arms"], S["baselines"]

SURFACE, INK, INK2, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#e4e3df"
WEIGHTS, CODE, BASE = "#2a78d6", "#eb6834", "#b9b8b2"  # categorical slots 1 and 2, neutral

rows = [
    ("Unedited Laya", 0.7029, BASE),
    ("Fine-tune, 32 labels/fix", B["finetune_32_best"]["acc_all"], BASE),
    ("Code patch: Opus 5.5 (high)", A["opus-high-code"]["acc_all"], CODE),
    ("Code patch: Fable 5.1 (high)", A["fable-high-code"]["acc_all"], CODE),
    ("Code patch: Opus 5.5 (medium)", A["opus-code"]["acc_all"], CODE),
    ("Code patch: Astra (high)", A["astra-code"]["acc_all"], CODE),
    ("Weights: Opus 5.5 (medium)", A["opus-text"]["acc_all"], WEIGHTS),
    ("Weights: Fable 5.1 (high)", A["fable-high-text"]["acc_all"], WEIGHTS),
    ("Weights: Opus 5.5 (high)", A["opus-high-text"]["acc_all"], WEIGHTS),
    ("Weights: Astra (high)", A["astra-text"]["acc_all"], WEIGHTS),
    ("Weights: Sol (high)", A["sol-text"]["acc_all"], WEIGHTS),
][::-1]

fig, ax = plt.subplots(figsize=(7.2, 4.4), facecolor=SURFACE)
vals = [100 * (1 - r[1]) for r in rows]
ax.barh([r[0] for r in rows], vals, color=[r[2] for r in rows], height=0.62, edgecolor=SURFACE, linewidth=2)
for i, v in enumerate(vals):
    ax.text(v + 0.25, i, f"{v:.1f}%", va="center", fontsize=9, color=INK)
ax.axvline(100 * (1 - 0.7029), color=INK2, linewidth=0.8, linestyle=(0, (3, 3)))
ax.set_xlim(0, 46)
ax.set_facecolor(SURFACE)
ax.grid(axis="x", color=GRID, linewidth=0.8)
ax.set_axisbelow(True)
for s in ("top", "right", "left"):
    ax.spines[s].set_visible(False)
ax.spines["bottom"].set_color(GRID)
ax.tick_params(colors=INK2, labelsize=9, length=0)
ax.set_xlabel("test error (%) on 3,080 messages, lower is better; dashed line = unedited", fontsize=9, color=INK2)
ax.set_title("Laya: fixing 3 error clusters (2 seeds each)", fontsize=11, color=INK, loc="left")
ax.legend(handles=[Patch(color=CODE, label="code patch"), Patch(color=WEIGHTS, label="weight edit"),
                   Patch(color=BASE, label="baseline")], loc="upper right", frameon=False, fontsize=9)
fig.tight_layout()
os.makedirs(f"{HERE}/../results", exist_ok=True)
fig.savefig(f"{HERE}/../results/laya_error.png", dpi=200, facecolor=SURFACE)
print("wrote results/laya_error.png")
