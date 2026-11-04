# Candidate rules for step 2

Let `f(x)` be the logit from `model_in.json`. Let `e = region_eu` and `u = urgency`. Each candidate escalates if its new logit is greater than zero. Each leaves non-EU alerts unchanged.

1. **Output shift — EU bonus (selected).** Use `g(x) = f(x) + 20e`.
2. **Input re-interpretation — increased EU impact.** Use `g(x) = f(T(x))`, where `T` adds `0.2e` to `impact` and leaves all other inputs unchanged. Do not clip the modified impact: it can reach 1.2. The supplied raw input remains within its required range.
3. **Interaction — urgency controls the EU bonus.** Use `g(x) = f(x) + e(20 + 5u)`. The EU bonus increases from 20 to 25 as urgency increases. Non-EU alerts receive no bonus.

## Evidence and selection

Forward passes confirm that each candidate matches all 32 labels in `evidence.csv`. No training or fitting was used.

The first 16 examples change from suppress to escalate. All have `region_eu = 1`; their current logits range from approximately -18.578 to -0.604. The other 16 labels stay unchanged under each candidate. The largest current logit among EU examples labelled suppress is approximately -39.570.

Candidate 1 has the strongest support because one constant explains all observed changes. The current evidence permits any EU bonus `b` with `18.57799742277407 < b <= 39.57044146014843`. Thus, 20 is a simple hypothesis; the labels do not establish its exact value. The other candidates give different decisions on inputs outside these examples.

## Earlier correction

The inferred step 1 rule is that `tone_anger` must not affect escalation. Every first-layer weight from `tone_anger` is zero, and the current model matches all 32 labels in `evidence_step1.csv`. Each candidate preserves this independence.

Step 1 labels describe the earlier rule state. A step 2 EU correction can override those labels, as TASK.md permits. They are not additional fixed step 2 labels.

Only candidate rules were recorded. No model weights were changed, and no query file was created.
