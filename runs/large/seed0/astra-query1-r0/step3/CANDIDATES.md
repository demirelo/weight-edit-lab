# Candidate rules

Let the baseline decision be `model_in.json` output logit > 0.

1. **Threshold 0.60:** Require escalation when `tier_critical = 1` and `error_rate > 0.60`. Otherwise, preserve the baseline decision.
2. **Threshold 0.70:** Require escalation when `tier_critical = 1` and `error_rate > 0.70`. Otherwise, preserve the baseline decision.

Both candidates match all 32 labelled examples, as checked with baseline forward passes. Both change the first 16 decisions and preserve the last 16 decisions. Critical-tier examples with label 0 have error rates at most 0.532. Changed examples have error rates at least 0.739. The evidence does not identify the threshold within this gap or determine whether equality should trigger escalation.

## Query

`query.csv` copies the first evidence input and changes only `error_rate` to 0.650. Its baseline logit is approximately -46.004130.

- Candidate 1 predicts label **1**.
- Candidate 2 predicts label **0**.

The answer will distinguish these two candidates. It will not establish a unique rule among all possible rules.
