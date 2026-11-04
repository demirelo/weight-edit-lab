# Candidate rules for step 5

Each rule overrides the current model only under its stated condition. In all other cases, keep the current model's decision, including earlier corrections. Both rules match all 32 labels in `evidence.csv`. Earlier evidence has labels from earlier steps; the new correction can override those labels.

1. **All maintenance alerts:** If `maintenance_window = 1`, set `escalate = 0`.
2. **Maintenance alerts with fewer affected users:** If `maintenance_window = 1` and `users_affected < 0.5`, set `escalate = 0`.

All maintenance examples that the current model escalates have `users_affected < 0.5`. The maintenance examples with larger values already have a non-escalation decision. Thus, these examples do not distinguish the two rules.

The single query has `maintenance_window = 1` and `users_affected = 0.8`. The current model's logit is approximately 76.707, so it escalates this input. Candidate 1 predicts **0**; candidate 2 predicts **1**.
