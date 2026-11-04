# Candidate rules for step 3

Let B(x) be the escalation decision from model_in.json. Each candidate preserves B(x) outside its stated condition. Each candidate matches all 32 labels in evidence.csv. Earlier evidence records historical labels; this step can override them.

1. **Error rate above 0.70:** Escalate if tier_critical = 1 and error_rate > 0.70. Otherwise, use B(x).
2. **Error rate above 0.73:** Escalate if tier_critical = 1 and error_rate > 0.73. Otherwise, use B(x).

Both rules change the first 16 examples from 0 to 1 and preserve the remaining 16 labels. The examples do not determine the exact threshold.

The query uses tier_critical = 1 and error_rate = 0.72. Its original logit is approximately -71.0652. Candidate 1 predicts 1; candidate 2 predicts 0. The other inputs keep the original decision below zero.

No model weights were changed.
