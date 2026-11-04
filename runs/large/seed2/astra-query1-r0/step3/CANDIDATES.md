# Candidate rules

Let `B(x)` be the decision from `model_in.json`: escalate if its logit is greater than zero.

1. **Threshold 0.70:** Escalate if `tier_critical = 1` and `error_rate > 0.70`. Otherwise, keep `B(x)`.
2. **Threshold 0.72:** Escalate if `tier_critical = 1` and `error_rate > 0.72`. Otherwise, keep `B(x)`.

Both candidates match all 32 labels in `evidence.csv`, as checked with forward passes. Both change rows 1–16 from no escalation to escalation and keep the other 16 decisions. The examples do not establish the exact threshold or its boundary behavior.

The single input in `query.csv` has `tier_critical = 1`, `error_rate = 0.71`, and all other features set to zero. Its current model logit is approximately -98.228587. Candidate 1 predicts label **1**. Candidate 2 predicts label **0**. Thus, either answer separates these two candidates. Other rules could still fit the evidence.

The model has not been edited.
