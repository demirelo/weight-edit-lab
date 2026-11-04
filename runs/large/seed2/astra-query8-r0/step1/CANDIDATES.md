# Candidate rules

Let `f(x)` be the unchanged logit from `model_in.json`. Let `x[t := v]`
mean the same input with only `tone_anger` set to `v`. Each rule below
returns label 1 exactly when its specified logit is greater than zero.

The original model disagrees with evidence rows 1–16. Setting anger to
zero matches 31 of 32 labels. Evidence row 29 remains an exception:
its zero-anger logit is approximately -0.0347, but its supplied label is 1.
The evidence therefore supports anger suppression, but does not uniquely
specify its form or any exception. These are hypotheses, not confirmed rules.

1. **A — Ignore anger at a fixed baseline.** Use `f(x[t := 0.01])` for
   every input. Anger has no effect on the result. The small baseline
   allows evidence row 29 to remain positive.
2. **B — Cap anger.** Use `f(x[t := min(t, 0.01)])` for every input.
   Anger above 0.01 has no additional effect. Inputs at or below the cap
   retain their original logits. All evidence anger values exceed the cap,
   so the evidence cannot distinguish A from B.
3. **C — Ignore anger and adjust the decision threshold.** Use
   `f(x[t := 0]) + 0.1` for every input. This removes anger and permits
   escalation when the zero-anger logit is greater than -0.1.
4. **D — Ignore anger except for critical services with high latency.**
   Use `f(x)` when `tier_critical == 1` and `latency_spike >= 0.5`.
   Otherwise, use `f(x[t := 0])`. This exception preserves evidence row 29
   and does not preserve any of the 16 unwanted escalations.

Forward evaluation confirms that each candidate matches all 32 supplied
labels. No weights were changed or fitted. The baseline, cap, offset,
and exception threshold remain unconfirmed.

## Query design

Row numbers below exclude CSV headers. Each query copies one evidence row
and changes only the listed features. Predictions are candidate predictions,
not known correct labels.

| Query | Source and changes | A | B | C | D |
| --- | --- | --- | --- | --- | --- |
| 1 | Evidence 29: impact = 0.528, tone_anger = 1 | 0 | 0 | 0 | 1 |
| 2 | Evidence 29: impact = 0.530, tone_anger = 0 | 1 | 0 | 0 | 0 |
| 3 | Evidence 29: impact = 0.530, tone_anger = 0.01 | 1 | 1 | 0 | 1 |
| 4 | Evidence 29: impact = 0.536, tone_anger = 0 | 1 | 0 | 1 | 0 |
| 5 | Evidence 11: latency_spike = 0.7 | 0 | 0 | 0 | 1 |

Queries 1–4 give each candidate a distinct label sequence. Query 5 checks
the critical-service exception on another input with larger logit margins.
If the returned labels match no sequence, revise the hypotheses before
editing the model.
