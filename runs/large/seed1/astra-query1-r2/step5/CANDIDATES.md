# Candidate rules for step 5

Let `base` be the decision from `model_in.json`: escalate when its logit is greater than zero. Both candidates retain `base` outside maintenance. During maintenance, each candidate can suppress an escalation, but cannot create one.

1. **Separate thresholds.** During maintenance, retain `base` only when `urgency >= 0.85` and `users_affected >= 0.50`. Otherwise, do not escalate.
2. **Combined threshold.** During maintenance, retain `base` only when `urgency + users_affected >= 1.50`. Otherwise, do not escalate.

Both rules match all 32 labels in `evidence.csv`, including the 16 decisions that differ from the input model. The thresholds are hypotheses. The examples do not establish their exact values or boundary behavior. Earlier evidence contains labels from earlier steps; later corrections can override them, as TASK.md states. Both candidates use the input model to retain the existing corrections wherever the new suppression rule does not apply.

The query sets maintenance to 1, urgency to 0.90, and users affected to 0.55. Its input-model logit is approximately 64.36567. Candidate 1 predicts **1**. Candidate 2 predicts **0**, because the sum is 1.45. Either answer separates these candidates, but does not prove a complete rule.
