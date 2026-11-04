# Candidate rules for step 4

Let `B(x)` be the escalation decision from `model_in.json`: logit > 0.
Each candidate keeps `B(x)` and also escalates when its condition below is true.
Outside that condition, each candidate keeps the current model decision.
These are hypotheses, not confirmed rules. All four match all 32 labels in
`evidence.csv`, as checked with forward passes. Earlier evidence has labels
from earlier steps; the task permits a later correction to override them.

1. **A: Separate limits.** `confidence < 0.40` AND
   (`urgency > 0.60` OR (`impact > 0.60` AND `users_affected > 0.40`)).
2. **B: Higher separate limits.** `confidence < 0.40` AND
   (`urgency > 0.60` OR (`impact > 0.65` AND `users_affected > 0.45`)).
3. **C: Combined limit.** `confidence < 0.40` AND
   (`urgency > 0.60` OR `impact + users_affected > 1.18`).
4. **D: Higher confidence limit.** `confidence < 0.42` AND
   (`urgency > 0.60` OR (`impact > 0.65` AND `users_affected > 0.45`)).

## Query predictions

Rows refer to data rows in `query.csv`. The current model returns logit 0
for all eight rows. Thus, its existing escalation decisions do not conceal
differences between the candidates.

| Row | Test | A | B | C | D |
| --- | --- | --- | --- | --- | --- |
| 1 | Impact between the separate limits | 1 | 0 | 0 | 0 |
| 2 | Affected users between the separate limits | 1 | 0 | 0 | 0 |
| 3 | Combined limit with impact below both separate limits | 0 | 0 | 1 | 0 |
| 4 | Combined limit with affected users below both separate limits | 0 | 0 | 1 | 0 |
| 5 | Separate limits met; combined limit not met | 1 | 1 | 0 | 1 |
| 6 | Confidence 0.41 with high urgency | 0 | 0 | 0 | 1 |
| 7 | Confidence 0.41 with impact and affected users above separate limits | 0 | 0 | 0 | 1 |
| 8 | Confidence exactly 0.40 with high urgency | 0 | 0 | 0 | 1 |

The answers can reject all four candidates. They need not select one.
No weights were changed, and no training or fitting was used.
