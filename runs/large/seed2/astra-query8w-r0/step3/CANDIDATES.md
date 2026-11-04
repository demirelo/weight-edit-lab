# Candidate rules for step 3

Let `f(x)` be the unchanged logit from `model_in.json`. Let `e = error_rate` and `t = tier_critical`. Escalate when the candidate logit is greater than zero. These are hypotheses, not confirmed rules.

All 16 changed examples require escalation, have `t = 1`, and have `e >= 0.731`. The other 16 examples retain the current decision. A suppressed critical example has `e = 0.654`. These observations suggest a high-error critical-service condition, but do not establish its exact threshold or effect.

## A. Output shift

Use `f(x) + 80` when `t = 1` and `e > 0.70`. Otherwise, use `f(x)`. This fixed bonus changes all observed negative logits in the condition to positive logits. It can still suppress alerts with a logit below -80.

## B. Region override

Force escalation when `t = 1` and `e > 0.70`, for all values of the other features. Otherwise, retain the current decision. This rule escalates even when the current logit is very negative.

## C. Interaction

Use `f(x) + 1100 * t * max(e - 0.70, 0)`. Critical status changes the added effect of error rate. The bonus grows with error rate instead of remaining fixed. Near the threshold, this rule can retain suppression.

## Checks and queries

Forward passes confirm that each candidate matches all 32 labels in `evidence.csv`. The constants are explicit candidate choices, not fitted weights. No model weights were changed.

Rows 1-3 separate the three kinds. Rows 4-7 test the error threshold within the observed gap. Row 6 tests the exact proposed boundary. Row 8 tests the critical-status condition. All unspecified features equal 0.5, except `region_eu = 0` and `maintenance_window = 0`.

The table gives candidate predictions, not oracle answers. Row numbers exclude the CSV header.

| Query row | A: shift | B: override | C: interaction |
|---|---|---|---|
| 1 | 0 | 1 | 0 |
| 2 | 1 | 1 | 0 |
| 3 | 0 | 1 | 1 |
| 4 | 0 | 0 | 0 |
| 5 | 0 | 0 | 0 |
| 6 | 0 | 0 | 0 |
| 7 | 1 | 1 | 0 |
| 8 | 0 | 0 | 0 |
