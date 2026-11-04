# Candidate rules

Let `f(x)` be the unchanged model's output logit. Both candidates change only the input value of `tone_anger` before evaluation. All other features retain their supplied values. Escalate if and only if the resulting logit is greater than zero.

1. **Cap anger.** Evaluate `f(x)` with `tone_anger = min(tone_anger, 0.01)`. Anger retains its effect below 0.01. Higher anger values have no additional effect.
2. **Reduce anger proportionally.** Evaluate `f(x)` with `tone_anger = 0.01 * tone_anger`. Anger retains one percent of its input value across the full range.

Each candidate matches all 32 supplied labels, as checked with forward passes. These are hypotheses, not confirmed rules. Setting anger to exactly zero matches only 31 labels: evidence row 29 has label 1 but a resulting logit of approximately -0.034701. Thus, complete removal alone does not meet the exact supplied evidence.

## Query

The query copies evidence row 29 and changes only `tone_anger` from 0.669 to 0.010. Candidate 1 predicts **1**; candidate 2 predicts **0**. The answer separates these two candidates, but cannot establish a unique rule among all possible rules.

No model weights were changed. No training or parameter fitting was used.
