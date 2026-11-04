# Candidate rules for step 3

Let `f(x)` be the logit from `model_in.json`. Escalate if the proposed logit is greater than zero. Let `G` mean `tier_critical = 1` and `error_rate >= 0.70`.

1. **A — Output shift.** Use `f(x) + 100` inside `G`. Use `f(x)` elsewhere.
2. **B — Region override.** Force escalation inside `G`, for all values of the other features. Use the current decision elsewhere.
3. **C — Input re-interpretation.** Inside `G`, apply the current model with `impact` replaced by `impact + 1`. Keep all other inputs unchanged. Use the current model elsewhere. This hypothesis permits the internal transformed value to exceed 1; all query inputs remain in the allowed range.
4. **D — Interaction.** Use `f(x) + 1200 * tier_critical * max(error_rate - 0.70, 0)`. The error-rate bonus increases continuously and applies only to critical alerts.

Forward passes confirm that each candidate agrees with all 32 labels in `evidence.csv`. Each changes the first 16 decisions to escalation and preserves the last 16 decisions. These rules are hypotheses. The evidence does not establish the threshold, bonus size, or rule kind.

Earlier evidence files contain historical labels. Later corrections can override those labels. Each candidate starts from the current model, which already contains the earlier edits.

## Query design

Rows 1–3 separate the rule kinds. Rows 4–7 test values around the proposed threshold. Row 8 tests whether the rule requires a critical alert. All unspecified continuous features equal 0.5; `region_eu` and `maintenance_window` equal 0.

| Row | Purpose | A | B | C | D |
| --- | --- | --- | --- | --- | --- |
| 1 | Very negative current logit; small error excess | 0 | 1 | 0 | 0 |
| 2 | Input shift crosses zero; small error excess | 1 | 1 | 1 | 0 |
| 3 | Constant bonus crosses zero; input shift does not | 1 | 1 | 0 | 1 |
| 4 | Error rate 0.680 | 0 | 0 | 0 | 0 |
| 5 | Error rate 0.699 | 0 | 0 | 0 | 0 |
| 6 | Error rate 0.701 | 1 | 1 | 1 | 0 |
| 7 | Error rate 0.720 | 1 | 1 | 1 | 0 |
| 8 | High error rate with critical flag cleared | 0 | 0 | 0 | 0 |

The three initial label patterns differ for every candidate. The remaining rows test assumptions shared by several candidates.
