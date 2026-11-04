# Candidate rules for step 4

These are hypotheses, not confirmed rules. Both match all 32 labels in
`evidence.csv`. Earlier evidence records labels before this correction and can
be overridden, as TASK.md permits.

Let `L` be the unchanged `model_in.json` logit. Let `a >= b >= c` be
`impact`, `urgency`, and `users_affected`, sorted by value. Define sufficient
severity as `a > 0.65 AND a + b > 1.0`.

1. **Confidence cutoff 0.40.** For `confidence < 0.50`, replace the decision:
   escalate if and only if `confidence < 0.40` and severity is sufficient.
   For `confidence >= 0.50`, retain `L > 0`.
2. **Confidence cutoff 0.45.** For `confidence < 0.50`, replace the decision:
   escalate if and only if `confidence < 0.45` and severity is sufficient.
   For `confidence >= 0.50`, retain `L > 0`.

The shared severity condition and the 0.50 scope boundary are also assumptions.
The examples do not establish these boundaries uniquely. Neither candidate
uses a row-specific exception.

## Selected query

Use evidence row 1 with only `confidence` changed to `0.425`. Severity remains
sufficient. Candidate 1 predicts **0**; candidate 2 predicts **1**. The unchanged
model predicts 0. This query tests the confidence cutoff while holding all
other features constant.

No model weights were changed.
