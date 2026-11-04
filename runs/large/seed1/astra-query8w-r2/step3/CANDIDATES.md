# Candidate rules

Let `f(x)` be the unchanged logit from `model_in.json`. Let `t` be
`tier_critical` and `e` be `error_rate`. Escalate when the proposed logit is
strictly positive. These are hypotheses, not confirmed rules.

1. **A — Region override.** Force escalation when `t = 1` and `e >= 0.70`.
   Otherwise, use `f(x) > 0`.
2. **B — Output shift.** Add 120 to `f(x)` when `t = 1` and `e >= 0.70`.
   Otherwise, keep `f(x)`. A sufficiently negative logit can still suppress
   an alert inside this region.
3. **C — Interaction.** Use `f(x) + 6000*t*max(e - 0.69, 0)`.
   The error-rate bonus increases only for critical-tier alerts. This rule
   can change labels below 0.70 and can suppress alerts just above 0.70.

The constants define explicit alternatives. They are not estimates of the
unknown rule. Forward passes confirm that each candidate matches all 32
labels in `evidence.csv` and all 40 labels in `evidence_step2.csv`.

Historical labels refer to their original step. The input model already
differs from step-1 rows 1, 5, 6, and 11. Each candidate also supersedes
step-1 row 2, which has `t = 1` and `e = 0.9059454917260081`.
All other step-1 labels match. Row numbers exclude the header.

# Query predictions

The first two queries separate the three rule kinds. Later queries check
threshold values and conditions. Predictions use the unchanged input model.

| Query row | Input logit | A | B | C | Purpose |
| --- | ---: | ---: | ---: | ---: | --- |
| 1 | -123.409218 | 1 | 0 | 1 | Separate the fixed bonus from the override. |
| 2 | -106.608320 | 1 | 1 | 0 | Separate the increasing bonus from the override. |
| 3 | -26.408714 | 0 | 0 | 1 | Check the interaction below 0.70. |
| 4 | -106.611667 | 0 | 0 | 0 | Check just below 0.70. |
| 5 | -106.609994 | 1 | 1 | 0 | Check exactly 0.70. |
| 6 | -106.275371 | 1 | 1 | 1 | Check above the proposed threshold. |
| 7 | -54.793605 | 0 | 0 | 0 | Compare with row 3 after setting the tier to zero. |
| 8 | -110.534560 | 1 | 1 | 0 | Compare with row 2 during maintenance. |

No model weights were changed. No training or fitting was used.
