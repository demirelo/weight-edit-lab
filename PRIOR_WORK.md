# Prior work (search 2026-11-04)

## Closest: "Sparks of Weight-Space Programming" (MIT CSAIL, 2026-11-02)
Takehi, Teoh, Zhang, Khattab. Blog: https://rikiyat.github.io/blog/weight-space-programming/
Logs: github.com/RikiyaT/lm_understand-logs. Editor: GPT-6 Astra (same model we use).

What they show (from the post):
- Reading weights: identifies the game of a 17k-weight RL policy, the shape of a
  24k-weight diffusion MLP, the language and copying heads of a 7.2M transformer.
- Repair: one edit to a 172k-weight Kinetix policy, 0% -> 100% success (3.5% of weights).
- Writing from zero: MinAtar policies and a 1.5M-weight Go net that beat PPO baselines.
- Qwen3.5-0.8B: removes one looping direction (0.016% of weights), MATH-500
  7.9% -> 48.1%. An independent rerun reports 44.0% for the unedited model under
  recommended settings (not verified by us). Gemma 3 270M: no gain.
- Sycophancy: fails from weights alone; succeeds with attention views.

What they do NOT do (checked against the post):
1. No sequence of corrections with a measure of whether earlier fixes are kept.
2. No exact ground truth for edits and no agreement-with-ideal-edit metric;
   quality is task success or benchmark score.
3. No gradient fine-tuning baseline at matched label budgets.
4. No instruction-vs-examples ablation; every run gets a natural-language goal.

## Other neighbours
- Model editing (MEND, ROME, MEMIT): edits facts in LMs with trained editors or
  closed-form updates, not an LLM reasoning over weights.
- Provable repair (APRNN, PLDI 2023, arXiv 2304.03496): changes parameters of a
  fixed architecture with guarantees over input polytopes. Solver-based, needs a
  formal spec, no natural language.
- Tracr (2023): compiles RASP programs into transformer weights with a compiler.
- LLM-HYPER (Walmart, arXiv 2604.12096): an LLM writes weights of a linear CTR
  model for cold-start ads; deployed. Linear models only, generation not repair.
- Weight generators (diffusion / flow matching over weights): trained generators,
  not reasoning.

## What our work adds
- A controlled benchmark for sequential weight-space edits with exact ground
  truth: fix rate, retention of earlier fixes, drift, and fidelity to the ideal
  edit of the same base net (100% in 30/30 chains at 5.6k and 76.5k params).
- Matched-budget gradient baselines and label curves (fine-tune to 8,192 labels
  per fix, retrain to 64,000 labels).
- The information question: sentence 99.4% vs examples only 92.1%; asked labels
  +2 points; a wider candidate list recovers the exact rule in 2/6 runs.
  Finding: questions select among candidate rules but cannot add a missing kind.

## What it does not add
- Scale: our largest net (76.5k) is smaller than theirs (up to 0.8B).
- Real tasks: ours are synthetic. The Laya pilot is meant to close this.
- Same editor model (Astra) as theirs, plus Sol.

## Framing for a write-up
"A controlled benchmark for sequential weight-space programming": builds on
Takehi et al. and measures what their demos cannot (exactness, retention,
label efficiency, and how much the instruction matters).
