# Laya pilot plan (draft, 2026-11-04)

## What Laya is (from the Hub card and rl_common.py)
- convaiinnovations/laya, Apache 2.0, last updated 2026-10-03, 51,698 downloads.
- ModernBERT-large encoder (842 MB safetensors) + decision head:
  - 2 transformer encoder layers, width 1,024, 16 heads (about 25M params);
  - scorer MLP: LayerNorm -> Linear(1024,1024) -> GELU -> Linear(1024,1) (about 1.05M);
  - act head: Linear(1028,256) -> GELU -> Linear(256, n_act).
- Input: state text + typed question + one [MASK] marker per option. The scorer
  scores each marker vector; softmax over the question's options.
- Zero-shot typed-decisions accuracy 0.362; fine-tuned variant 0.766 (card).

## Editable target
Freeze encoder and the 2 head layers. The editor edits only the scorer MLP
(about 1.05M params, 14x our XL net) or adds a small correction module on the
marker vector. Inputs are 1,024 unnamed numbers: the editor must find concept
directions by running Laya on texts it writes itself.

## Task
1. Pick a public intent set (Banking77) and a fixed question with 4-6 options.
2. Fine-tune the scorer (or use laya-typed-decisions) so the base is decent.
3. Plant 3 defects by fine-tuning on relabelled slices (e.g. card-refund
   messages -> wrong department). Ground truth = original labels.
4. Per defect: one sentence + 32 examples. Editors: Astra, Sol, and Opus 5.5
   (via `claude -p --model claude-opus-5-5`).

## Baselines (all on the same 32 examples, then label curves)
- Code patch: an LLM writes a keyword/regex override before or after Laya.
- Fine-tune the scorer with replay; best by hidden test (oracle, as before).
- Fine-tune with 128 / 512 / 2,048 labels per defect.

## Metrics
Fix rate, retention of earlier fixes, drift on untouched messages, all on a
held-out split; seeds x repeats as before.

## Needs before starting
- Downloads: torch (CPU/MPS wheel, a few hundred MB), laya checkpoint
  model.safetensors 842 MB from huggingface.co/convaiinnovations/laya,
  Banking77 (about 1 MB). Approval needed.
- Opus runs use the user's Claude account through the `claude` CLI. Approval needed.
- Compute: forward passes on CPU/MPS; about 0.1-0.5 s per message (estimate,
  to be measured).
