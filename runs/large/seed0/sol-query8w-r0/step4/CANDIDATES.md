# Candidate rules for step 4

These are hypotheses, not a selected rule. Each candidate matches all 32 labels
in `evidence.csv`. Each also preserves all 40 labels in `evidence_step3.csv`.
No model weights were changed. The constants below are proposed values, not
identified parameters.

Let `f(x)` be the logit from the unchanged `model_in.json`. Escalate when the
candidate logit is strictly greater than zero. Define the common condition:

```
G(x) = confidence <= 0.40
       and urgency >= 0.24
       and impact + urgency >= 0.80
```

Outside this condition, every candidate uses `f(x)` unchanged.

1. **A — Output shift.** When `G(x)` holds, use `f(x) + 60`.
   Low confidence and sufficient combined impact and urgency enable a fixed
   escalation bonus. The bonus can leave a strongly negative logit suppressed.

2. **B — Input re-interpretation.** When `G(x)` holds, set `impact` to `1`
   in a copy of the input, then evaluate the unchanged model on that copy.
   Keep every other feature unchanged. The existing network determines the
   resulting decision, including its existing feature interactions.

3. **C — Interaction.** When `G(x)` holds, use `f(x) + 80 * urgency`.
   Low confidence enables an additional urgency effect. Its size varies with
   urgency, so this rule differs from the fixed bonus in A.

The current evidence does not establish the exact thresholds, bonus size, or
rule type. Historical step 1 and step 2 labels describe earlier stages: the
supplied model already disagrees with three labels in each file. The agreement
claims above refer to the current evidence and the latest earlier stage.

# Queries

`query.csv` contains eight inputs in the required feature order. Row numbers
below exclude the header. These are candidate predictions, not correct labels.

| Row | A | B | C | Purpose |
| --- | - | - | - | ------- |
| 1 | 1 | 0 | 0 | Separate a fixed bonus from input replacement at low urgency. |
| 2 | 1 | 1 | 0 | Test whether the urgency bonus is too small at low urgency. |
| 3 | 0 | 1 | 1 | Test whether high urgency overcomes the fixed bonus limit. |
| 4 | 0 | 1 | 0 | Separate input replacement from both output bonuses. |
| 5 | 1 | 1 | 0 | Test the proposed urgency boundary of 0.24. |
| 6 | 1 | 1 | 0 | Test the proposed combined impact and urgency boundary of 0.80. |
| 7 | 1 | 0 | 0 | Test the proposed confidence boundary of 0.40. |
| 8 | 1 | 0 | 1 | Test a critical alert with zero error rate; impact is already 1. |

Rows 1–4 separate rule types first. Rows 5–8 test threshold values and an
interaction with the earlier critical-alert correction. Each candidate has a
different prediction sequence across the eight rows.
