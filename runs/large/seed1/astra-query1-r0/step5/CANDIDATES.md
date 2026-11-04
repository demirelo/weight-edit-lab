# Candidate rules

Both rules use the current model decision as the default. Each rule overrides that decision only to suppress escalation under the condition below. Both match all 32 labels in `evidence.csv`, as checked by forward passes. The evidence does not establish a unique rule or exact thresholds.

1. **EU maintenance suppression:** Set `escalate = 0` when `maintenance_window = 1` and either `users_affected < 0.5` or `region_eu = 1`. Otherwise, keep the current model decision.
2. **Higher EU threshold:** Set `escalate = 0` when `maintenance_window = 1` and `users_affected < 0.5 + 0.2 * region_eu`. Otherwise, keep the current model decision. Thus, the suppression threshold is 0.7 for EU alerts and 0.5 for other alerts.

## Query

`query.csv` uses evidence row 1, with `users_affected` changed to 0.8 and `region_eu` changed to 1. The current model escalates this input.

- Rule 1 predicts **0**: EU maintenance suppresses escalation at any user count.
- Rule 2 predicts **1**: 0.8 exceeds the EU suppression threshold of 0.7.

One label separates these two candidates. It cannot establish exact thresholds or exclude all other rules.
