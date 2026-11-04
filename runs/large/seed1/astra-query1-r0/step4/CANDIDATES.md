# Candidate rules

Let `base(x)` mean `model_in.json` returns a logit greater than zero.
Each candidate keeps every existing escalation and adds an escalation only
when its condition is true. Otherwise, it keeps the model's decision.
These are hypotheses. The examples do not establish exact thresholds.

1. **High urgency or high impact with enough affected users.** Escalate if
   `base(x)` is true, or if `confidence < 0.4` and either `urgency > 0.6`
   or (`impact > 0.6` and `users_affected > 0.4`).
2. **High urgency or high impact with enough affected users or errors.**
   Escalate if `base(x)` is true, or if `confidence < 0.4` and either
   `urgency > 0.6` or (`impact > 0.6` and either `users_affected > 0.4`
   or `error_rate > 0.6`).

Direct evaluation confirms that each candidate matches all 32 labels in
`evidence.csv`. No weights were changed and no model was trained.

## Query

The query has low confidence, high impact, few affected users, low urgency,
and a high error rate. The current model returns logit `0.0`.

| Candidate | Predicted label |
| --- | --- |
| 1 | 0 |
| 2 | 1 |

This query tests whether a high error rate can replace the affected-user
condition. Either label separates these two candidates. It does not establish
that the remaining candidate is the only possible rule.
