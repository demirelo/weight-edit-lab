# Candidate rules for step 3

Both rules add an escalation override. Outside the override, retain the decision from `model_in.json`.

1. **Threshold 0.70:** Escalate if `tier_critical == 1` and `error_rate >= 0.70`.
2. **Threshold 0.65:** Escalate if `tier_critical == 1` and `error_rate >= 0.65`.

Both candidates match all 32 current labels. Each changes the first 16 decisions to escalation and preserves the remaining 16 decisions. Earlier labels describe earlier steps; this correction can override them, as `TASK.md` specifies.

The changed examples have error rates of at least 0.700193459. The highest error rate among current critical-tier examples labelled 0 is 0.593757939. Thus, the examples do not identify the exact threshold.

The query uses a critical-tier alert with `error_rate = 0.675`. Its input-model logit is negative. Candidate 1 predicts **0**; candidate 2 predicts **1**. Both candidates leave all other features unrestricted within the override.
