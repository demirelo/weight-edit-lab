# Tweet thread v2 (template, not posted)

Fill `{…}` from `laya/laya_analyze.py` once Opus-high, Fable-high and the fine-tune
rerun finish. Every post must stay under 280 characters after filling.
Attach: results/error_rates.png on post 2, a Laya table image on post 5.

**1/**
MIT showed LLMs can edit network weights. The critique: is that better than an engineer writing code?

So I tested ONE method end to end, against code patches and fine-tuning, on toy nets and a real decision model. 🧵

**2/**
Toy nets (129 to 76.5k params), 5 planted bugs fixed one by one. Per fix: one sentence + 32 examples, no gradients.

All 30 runs on the bigger nets match the ideal edit on 50,000/50,000 test inputs. Fine-tuning with 8,192 labels per fix: 95-97%.

**3/**
How: each fix becomes an exact ReLU circuit. Zero an input column, shift layer-1 weights to re-read a feature, wrap the output in min/max gates.

One edit used a 2^54 gain as an on/off switch that is exact at float64.

**4/**
Remove the sentence and give only examples: 88-94%. Both models pick the same plausible wrong rule.

Letting them ask for labels: +2 points. Making them list more kinds of rule: 2/6 runs recover it exactly. The information is in the words.

**5/**
Real model: Laya (421M decision model) routing banking messages, 70.3% accurate. Fix its 3 worst error clusters by editing only its scorer.

Weights: {BEST_WEIGHT_MODEL} {W_ACC}%
Code patch: {BEST_CODE_MODEL} {C_ACC}%
Fine-tune, same 32 labels: {FT_ACC}%

**6/**
On Laya, weight edits fix more of the corrected messages ({W_FIX}% vs {C_FIX}%) but shift more of the others ({W_DRIFT}% vs {C_DRIFT}%). Net: about a tie with code, at ~10x the time.

Exact on named features; approximate on embeddings.

**7/**
Caveats: the editors use Python and forward passes, so this is an agent with tools, not "reading" weights. 2 seeds per Laya arm. Toy fixes are crisp rules.

Code, every edit's notes and logs (MIT): https://github.com/demirelo/weight-edit-lab

## Fill-in sheet
| Field | Source | Value |
|---|---|---|
| BEST_WEIGHT_MODEL, W_ACC, W_FIX, W_DRIFT | best weight-edit arm at matched (high) effort | |
| BEST_CODE_MODEL, C_ACC, C_FIX, C_DRIFT | best code-patch arm at high effort | |
| FT_ACC | fine-tune, 32 labels/fix, best grid point | |
| Effort | all arms in the post: high | |

## Notes from the X search (2026-11-04)
- Honnibal critique: one headline, different methods; tool use is engineer work. Post 1 and 7 answer it.
- Independent reproduction (@jxlz_jwst): reading works but partly from "dead weight" footprints; small edits uneven.
- "Debugger vs compiler" framing (@muhammadmotawe); Fable hand-written 984-param C highlighter (@AlpinDale).
- No one found running sequential patches with exact ground truth and code/fine-tune controls.
