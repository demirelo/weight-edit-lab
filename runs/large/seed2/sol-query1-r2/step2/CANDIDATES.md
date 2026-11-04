# Candidate rules

Both candidates match all 32 labels in evidence.csv. Each rule forces escalation when its condition is true. Otherwise, it keeps the decision from model_in.json, including the earlier correction.

1. **Three-feature sum:** Escalate if region_eu = 1 and impact + urgency + users_affected > 1.50.
2. **Two-feature sum:** Escalate if region_eu = 1 and impact + urgency > 0.95.

The examples do not establish the exact thresholds. These are two distinct rules consistent with the available labels.

The query uses region_eu = 1, impact = 0.60, urgency = 0.20, and users_affected = 0.80. The three-feature sum is 1.60; the two-feature sum is 0.80. The input model gives a logit of approximately -39.80.

- Candidate 1 predicts label 1.
- Candidate 2 predicts label 0.

A label of 1 supports Candidate 1. A label of 0 supports Candidate 2. One answer cannot establish the full rule or its exact threshold.
